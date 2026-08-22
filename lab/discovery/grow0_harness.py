"""GROW-0 synthetic calibration harness orchestrator.

Frozen per docs/briefs/pre-registration/2026-08-22-grow-0-synthetic-calibration-prereg.md
(FROZEN, operator GO 2026-08-22). This module runs Limb A, Limb B, and RED-LEAK/RED-BLIND
exactly as that prereg specifies -- RED-PATCH lives separately in grow0_red_patch.py, per the
prereg's own framing of it as independent of the stochastic panels.
"""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from discovery.cost_model import resolve_commission
from discovery.grow0_dgp import TRUE_EDGE_VARIANT_INDEX, build_root_branches, spawn_panel_streams
from discovery.grow0_scoring import PanelResult, run_panel, run_panel_leaked
from research_utils.axis_screen import floor_at_k
from research_utils.repo_root import repo_root

FLOOR = floor_at_k(10, years=6.5)  # prereg §4: floor_at_k(10, 6.5) = 1.265

_logger = logging.getLogger(__name__)

_COST_FIRM_KEY = "Tradeify_Select_100K"
_COST_RESOLVABLE_INSTRUMENT = "MNQ"
_COST_UNRESOLVABLE_INSTRUMENT = "MGC"
_COST_RESOLVABLE_EXPECTED = 0.91  # prereg §3: resolve_commission("Tradeify_Select_100K", "MNQ") = 0.91


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


def _evaluate_limb_a_shaped_verdict(
    result: PanelResult, nominee_grammar_index: int, edge_index: int
) -> tuple[str, dict]:
    """Shared conjunct evaluation behind both Limb A's own PASS/FAIL verdict
    (prereg §6.1 step 6) and RED-BLIND's identically-shaped boolean check
    (prereg §6.4 v3) -- the two callers differ only in what they DO with the
    result afterward (RED-BLIND inverts it into
    PASSED_UNEXPECTEDLY/FAILED_AS_EXPECTED; see run_red_blind), not in the
    underlying three-conjunct test itself, which is now written once.

    Returns ``(verdict, conjuncts)`` where ``conjuncts`` exposes each of the
    three gates individually, so a caller (or a human reading the debug log)
    can see WHICH conjunct -- abandoned / nominee-mismatch / clears -- drove
    a FAIL, rather than just the opaque final string.

    ``nominee_grammar_index`` is the winning variant's ORIGINAL grammar index
    (Limb A passes ``result.nominee`` directly, since it draws from the full
    K=10 grammar; RED-BLIND passes it already remapped through its own
    ``_RED_BLIND_NULL_INDICES``, since its own ``result.nominee`` is an array
    position into a 9-element subset, not a grammar index).
    """
    conjuncts = {
        "not_abandoned": not result.abandoned,
        "nominee_matches": nominee_grammar_index == edge_index,
        "clears": result.clears,
    }
    passed = all(conjuncts.values())
    return ("PASS" if passed else "FAIL"), conjuncts


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
    verdict, conjuncts = _evaluate_limb_a_shaped_verdict(
        result, result.nominee, TRUE_EDGE_VARIANT_INDEX
    )
    _logger.debug("run_limb_a conjuncts=%s -> verdict=%s", conjuncts, verdict)
    return verdict, result


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
    results = []
    leaves = []
    for panel_seq in panel_seqs:
        train_children, _ = spawn_panel_streams(panel_seq, 10)
        leaves.extend(train_children)  # confirm_children discarded above -- RED-LEAK never
        # spawns them at all (run_panel_leaked replays TRAIN as its own CONFIRM), so only
        # the 10 train leaves per panel are actually consumed; hence min_distinct=n*10
        # below, not Limb B's n*20 (which also spawns and consumes a confirm side).
        result = run_panel_leaked(train_children, edge_variant_index=None, floor=FLOOR)
        results.append(result)
    assert_seed_diversity(leaves, min_distinct=n * 10)
    sum_clears = sum(1 for r in results if r.clears)
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

    Shares its three-conjunct evaluation with run_limb_a via
    _evaluate_limb_a_shaped_verdict -- the boolean shape is identical, only the
    downstream PASS/FAIL-to-PASSED_UNEXPECTEDLY/FAILED_AS_EXPECTED inversion
    below is RED-BLIND-specific (verdict semantics unchanged from before that
    extraction; do NOT read this refactor as touching the frozen §6.4 v3
    design).
    """
    branches = build_root_branches()
    train_children, confirm_children = spawn_panel_streams(branches["red_blind"], 9)
    result = run_panel(train_children, confirm_children, edge_variant_index=None, floor=FLOOR)
    grammar_nominee = _RED_BLIND_NULL_INDICES[result.nominee]
    limb_a_shaped_verdict, conjuncts = _evaluate_limb_a_shaped_verdict(
        result, grammar_nominee, TRUE_EDGE_VARIANT_INDEX
    )
    _logger.debug(
        "run_red_blind conjuncts=%s -> limb_a_shaped_verdict=%s", conjuncts, limb_a_shaped_verdict
    )
    # RED-BLIND inverts Limb A's own PASS/FAIL semantics: a Limb-A-shaped PASS here means the
    # structural impossibility happened (bad -- the control failed to fire), so RED-BLIND's own
    # vocabulary is the opposite of the shared helper's PASS/FAIL.
    return "PASSED_UNEXPECTEDLY" if limb_a_shaped_verdict == "PASS" else "FAILED_AS_EXPECTED"


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


_PREREG_COMMIT_PLACEHOLDER = "unset"  # overwritten by --prereg-commit at CLI invocation time;
# the prereg itself has no fixed commit hash known ahead of its own freeze commit landing


def run_grow0(
    *,
    run_id: str,
    started_at_arg: str,
    limb_b_n: int = LIMB_B_N,
    limb_b_c: int = LIMB_B_C,
    prereg_commit: str = _PREREG_COMMIT_PLACEHOLDER,
    ledger_path: Path | None = None,
) -> dict:
    """Runs Limb A, Limb B, RED-LEAK, RED-BLIND, RED-PATCH in that order and
    computes the prereg §6.7 Gate verdict. Appends one line to the retry ledger
    (prereg §6.6) regardless of outcome -- including a mid-run exception, so no
    invocation goes un-ledgered (prereg §6.6: "Every invocation ... regardless
    of outcome") -- then returns the same dict. On a mid-run exception, the
    ledger entry records whichever tokens completed before the raise (the
    rest default to None) plus an "error" field, and the original exception
    is re-raised after the ledger write.
    """
    limb_a_verdict = None
    limb_b_verdict = None
    red_leak_verdict = None
    red_blind_verdict = None
    red_patch_verdict = None

    try:
        from discovery.grow0_red_patch import run_red_patch

        check_cost_wiring()

        limb_a_verdict, _ = run_limb_a()
        limb_b_verdict, _, _ = run_limb_b(n=limb_b_n, c=limb_b_c)
        red_leak_verdict = run_red_leak(n=limb_b_n, c=limb_b_c)
        red_blind_verdict = run_red_blind()
        red_patch_verdict = run_red_patch()
    except Exception as e:
        failure_entry = {
            "run_id": run_id,
            "started_at_arg": started_at_arg,
            "prereg_commit": prereg_commit,
            "limb_b_n": limb_b_n,
            "limb_b_c": limb_b_c,
            "limb_a": limb_a_verdict,
            "limb_b": limb_b_verdict,
            "red_leak": red_leak_verdict,
            "red_blind": red_blind_verdict,
            "red_patch": red_patch_verdict,
            "overall": None,
            "error": str(e),
        }
        append_retry_ledger(failure_entry, path=ledger_path)
        raise

    all_red_green = (
        red_leak_verdict == "FAILED_AS_EXPECTED"
        and red_blind_verdict == "FAILED_AS_EXPECTED"
        and red_patch_verdict == "FAILED_AS_EXPECTED"
    )
    resolved = all_red_green and limb_a_verdict == "PASS" and limb_b_verdict == "PASS"

    result = {
        "run_id": run_id,
        "started_at_arg": started_at_arg,
        "prereg_commit": prereg_commit,
        "limb_b_n": limb_b_n,
        "limb_b_c": limb_b_c,
        "limb_a": limb_a_verdict,
        "limb_b": limb_b_verdict,
        "red_leak": red_leak_verdict,
        "red_blind": red_blind_verdict,
        "red_patch": red_patch_verdict,
        "overall": "RESOLVED" if resolved else "FALSIFIED",
    }
    append_retry_ledger(result, path=ledger_path)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="GROW-0 synthetic calibration harness")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--started-at", required=True, help="ISO timestamp, caller-supplied")
    parser.add_argument(
        "--prereg-commit",
        required=True,
        help="commit hash pinning the frozen prereg this run is authoritative against",
    )
    parser.add_argument("--limb-b-n", type=int, default=LIMB_B_N)
    parser.add_argument("--limb-b-c", type=int, default=LIMB_B_C)
    args = parser.parse_args(argv)

    result = run_grow0(
        run_id=args.run_id,
        started_at_arg=args.started_at,
        limb_b_n=args.limb_b_n,
        limb_b_c=args.limb_b_c,
        prereg_commit=args.prereg_commit,
    )
    print(json.dumps(result, indent=2))
    return 0 if result["overall"] == "RESOLVED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
