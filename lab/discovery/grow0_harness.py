"""GROW-0 synthetic calibration harness orchestrator.

Frozen per docs/briefs/pre-registration/2026-08-22-grow-0-synthetic-calibration-prereg.md
(FROZEN, operator GO 2026-08-22). This module runs Limb A, Limb B, and RED-LEAK/RED-BLIND
exactly as that prereg specifies -- RED-PATCH lives separately in grow0_red_patch.py, per the
prereg's own framing of it as independent of the stochastic panels.
"""
from __future__ import annotations

from discovery.cost_model import resolve_commission
from discovery.grow0_dgp import TRUE_EDGE_VARIANT_INDEX, build_root_branches, spawn_panel_streams
from discovery.grow0_scoring import PanelResult, run_panel
from research_utils.axis_screen import floor_at_k

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
