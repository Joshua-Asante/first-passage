"""GROW-0 synthetic calibration harness orchestrator.

Frozen per docs/briefs/pre-registration/2026-08-22-grow-0-synthetic-calibration-prereg.md
(FROZEN, operator GO 2026-08-22). This module runs Limb A, Limb B, and RED-LEAK/RED-BLIND
exactly as that prereg specifies -- RED-PATCH lives separately in grow0_red_patch.py, per the
prereg's own framing of it as independent of the stochastic panels.
"""
from __future__ import annotations

import json
from pathlib import Path

from discovery.cost_model import resolve_commission
from discovery.grow0_dgp import TRUE_EDGE_VARIANT_INDEX, build_root_branches, spawn_panel_streams
from discovery.grow0_scoring import PanelResult, run_panel, run_panel_leaked
from research_utils.axis_screen import floor_at_k
from research_utils.repo_root import repo_root

FLOOR = floor_at_k(10, years=6.5)  # prereg §4: floor_at_k(10, 6.5) = 1.265

_COST_FIRM_KEY = "Tradeify_Select_100K"
_COST_RESOLVABLE_INSTRUMENT = "MNQ"
_COST_UNRESOLVABLE_INSTRUMENT = "MGC"
_COST_RESOLVABLE_EXPECTED = 0.91


def check_cost_wiring() -> None:
    """Prereg §3 'Cost-wiring construction check' -- two-sided: MNQ must resolve
    to the real (index-micro) rate, and MGC must raise rather than silently
    falling back to a hardcoded literal. Called once at harness startup.
    """
    try:
        resolved = resolve_commission(_COST_FIRM_KEY, _COST_RESOLVABLE_INSTRUMENT)
    except ValueError as e:
        raise AssertionError(
            f"cost_model.resolve_commission({_COST_FIRM_KEY!r}, "
            f"{_COST_RESOLVABLE_INSTRUMENT!r}) raised {type(e).__name__}: {e} -- "
            f"cost-wiring check failed (resolvable side should not raise)"
        ) from e
    if resolved != _COST_RESOLVABLE_EXPECTED:
        raise AssertionError(
            f"cost_model.resolve_commission({_COST_FIRM_KEY!r}, "
            f"{_COST_RESOLVABLE_INSTRUMENT!r}) returned {resolved}, expected "
            f"{_COST_RESOLVABLE_EXPECTED} -- cost-wiring check failed (resolvable side)"
        )
    try:
        resolve_commission(_COST_FIRM_KEY, _COST_UNRESOLVABLE_INSTRUMENT)
    except ValueError:
        pass
    else:
        raise AssertionError(
            f"cost_model.resolve_commission({_COST_FIRM_KEY!r}, "
            f"{_COST_UNRESOLVABLE_INSTRUMENT!r}) did not raise -- cost-wiring check failed "
            "(unresolvable side; the module should refuse this instrument, not resolve it)"
        )


def run_limb_a() -> tuple[str, PanelResult]:
    """Prereg §6.1: single panel, K=10 grammar with theta* at index 5."""
    branches = build_root_branches()
    train_children, confirm_children = spawn_panel_streams(branches["limb_a"], 10)
    result = run_panel(
        train_children,
        confirm_children,
        edge_variant_index=TRUE_EDGE_VARIANT_INDEX,
        floor=FLOOR,
    )
    passed = (not result.abandoned) and result.nominee == TRUE_EDGE_VARIANT_INDEX and result.clears
    return ("PASS" if passed else "FAIL"), result


LIMB_B_N = 5500  # prereg §4 (measured nominal_p0=0.00059070, N/c sized with CI margin)
LIMB_B_C = 7


def assert_seed_diversity(leaves, *, min_distinct: int) -> None:
    """Prereg §3 'Runtime diversity assertion' -- a lightweight-review-round fix.

    The design-time SeedSequence spawn tree is collision-proof by construction, but that does
    NOT prove the harness's own consuming loop reads a distinct panel_seqs[i] per panel i --
    a vectorization broadcast mistake or Python loop-variable-capture bug could silently
    collapse many/all panels onto the same seed while the spawn tree itself stays perfectly
    distinct. This must run against every leaf actually consumed in a real run, not a
    design-time sample.
    """
    states = {tuple(s.generate_state(4)) for s in leaves}
    if len(states) < min_distinct:
        raise AssertionError(
            f"seed-diversity check failed: {len(leaves)} leaves consumed, only "
            f"{len(states)} distinct states (expected >= {min_distinct}) -- likely a "
            "cross-panel seed-collapse bug (prereg §3), not a design-time collision"
        )


def run_limb_b(n: int = LIMB_B_N, c: int = LIMB_B_C):
    """Prereg §6.2: N null-only panels, sum(clears) >= c -> FAIL, else PASS."""
    branches = build_root_branches()
    panel_seqs = branches["limb_b"].spawn(n)
    results = []
    leaves = []
    for panel_seq in panel_seqs:
        train_children, confirm_children = spawn_panel_streams(panel_seq, 10)
        leaves.extend(train_children)
        leaves.extend(confirm_children)
        result = run_panel(
            train_children, confirm_children, edge_variant_index=None, floor=FLOOR
        )
        results.append(result)
    assert_seed_diversity(leaves, min_distinct=n * 20)
    sum_clears = sum(1 for r in results if r.clears)
    verdict = "FAIL" if sum_clears >= c else "PASS"
    return verdict, sum_clears, results


def run_red_leak(n: int = LIMB_B_N, c: int = LIMB_B_C) -> str:
    """Prereg §6.3: same N/c structure as Limb B, but CONFIRM is the panel's own
    TRAIN max replayed (run_panel_leaked) instead of an independent draw.
    Expected clear rate ~0.63% (~9.97x baseline) -- this rig is EXPECTED to make
    Limb B's own binomial check report FAIL; that FAIL is what "FAILED_AS_EXPECTED"
    means (the calibration check correctly detected the injected leak).
    """
    branches = build_root_branches()
    panel_seqs = branches["red_leak"].spawn(n)
    sum_clears = 0
    for panel_seq in panel_seqs:
        train_children, _ = spawn_panel_streams(panel_seq, 10)
        result = run_panel_leaked(train_children, edge_variant_index=None, floor=FLOOR)
        if result.clears:
            sum_clears += 1
    detected_leak = sum_clears >= c  # Limb-B-shaped check applied to this rigged run
    return "FAILED_AS_EXPECTED" if detected_leak else "PASSED_UNEXPECTEDLY"


_RED_BLIND_NULL_INDICES = tuple(i for i in range(10) if i != TRUE_EDGE_VARIANT_INDEX)
# (0, 1, 2, 3, 4, 6, 7, 8, 9) -- the 9 original grammar indices RED-BLIND draws from,
# in the same order spawn_panel_streams(..., 9) below produces its 9 leaves. theta*
# (index 5) is not a member of this tuple by construction.


def run_red_blind() -> str:
    """Prereg §6.4 (v3 mechanism): full K=10 grammar's theta* is structurally
    excluded from RED-BLIND's own draw set (only 9 null-shape leaves, at
    original grammar indices _RED_BLIND_NULL_INDICES, are ever spawned from
    the red_blind branch). run_panel's own `nominee` field is an array
    position (0-8) into THIS 9-element list, not an original grammar index --
    mapping it back via _RED_BLIND_NULL_INDICES[result.nominee] is what makes
    "== TRUE_EDGE_VARIANT_INDEX" a genuine structural impossibility rather
    than comparing two different index spaces as if they were the same one.
    Because the nominee is still the MAXIMUM of several draws (positively
    biased, like the normal flow), it passes nomination gates (a)/(b) in the
    overwhelming majority of trials and reaches the real comparison -- unlike
    v2's abandoned argmin design, which mostly re-tested gate (a) instead.
    """
    branches = build_root_branches()
    train_children, confirm_children = spawn_panel_streams(branches["red_blind"], 9)
    result = run_panel(train_children, confirm_children, edge_variant_index=None, floor=FLOOR)
    grammar_nominee = _RED_BLIND_NULL_INDICES[result.nominee]
    passed = (not result.abandoned) and grammar_nominee == TRUE_EDGE_VARIANT_INDEX and result.clears
    return "PASSED_UNEXPECTEDLY" if passed else "FAILED_AS_EXPECTED"


RETRY_LEDGER_PATH = repo_root() / "discovery_manifests" / "grow0_retry_ledger.jsonl"


def append_retry_ledger(entry: dict, *, path: Path | None = None) -> None:
    """Prereg §6.6: append-only, one JSON line per harness invocation. Never
    edits or deletes an existing line. ``path`` defaults to RETRY_LEDGER_PATH;
    tests override it with a tmp_path.
    """
    target = path if path is not None else RETRY_LEDGER_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
