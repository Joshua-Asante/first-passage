"""Boundary tests for the trailing-drawdown bust condition (`bust_trailing`).

Added for the futures-prop (Bulenox) pivot: Bulenox Option 1 busts on a
drawdown from the account's *peak* equity, not from its *starting* equity
(the only kind `_simulate_path` could express before this change). These
tests exercise the new `dd_type="trailing"` branch directly via
`_simulate_path`, with synthetic paths — no vendor CSV data required.

Every new parameter on `_simulate_path` is keyword-only and defaults to the
value that reproduces today's FXIFY/static behavior exactly, so the existing
suite (`test_inactivity_boundary.py`, `test_mc_fp_boundaries.py`, the
Pepperstone-gated anchor tests) needs zero changes. `test_static_dd_type_never_takes_trailing_branch`
below is the direct proof of that non-interference claim.
"""

from __future__ import annotations

import math

import numpy as np

from portfolio_mc import HORIZON_CAP, STARTING_EQUITY, _simulate_path

N_STRATS = 4
DD_TRIGGER = 0.015
DD_SCALE = 0.40


def simulate_path(path: np.ndarray, dd_trigger: float, dd_scale: float, **kwargs):
    """Adapter mirroring test_inactivity_boundary.py's — passes new kwargs through."""
    horizon = min(HORIZON_CAP, len(path))
    return _simulate_path(path, dd_trigger, dd_scale, horizon, **kwargs)


def _build_path(rows: list[list[float]]) -> np.ndarray:
    arr = np.array(rows, dtype=float)
    assert arr.shape[1] == N_STRATS, f"each row must have {N_STRATS} pnl values"
    return arr


# ── 1. Fires on a pullback from a new peak ──────────────────────────────

def test_trailing_bust_fires_on_pullback_from_peak():
    """Day 1 makes a new peak ($250K); day 2 pulls back by more than 3% of
    that peak. Must bust_trailing on day 2, attributed to the strat that lost."""
    rows = [[50_000.0, 0.0, 0.0, 0.0], [-10_000.0, 0.0, 0.0, 0.0]] + [[0.0] * 4] * 10
    path = _build_path(rows)
    outcome, day, max_dd, culprit = simulate_path(
        path, DD_TRIGGER, DD_SCALE, dd_type="trailing", trailing_dd_pct=-0.03,
        daily_loss_pct=None,  # Bulenox Option 1 pairs trailing DD with no daily limit
    )
    assert outcome == "bust_trailing", f"expected bust_trailing, got {outcome}"
    assert day == 2
    assert culprit == 0


# ── 2. Does not fire below threshold ────────────────────────────────────

def test_trailing_bust_does_not_fire_below_threshold():
    """Same peak, a pullback clearly smaller than the 3% trailing threshold."""
    rows = [[50_000.0, 0.0, 0.0, 0.0], [-2_000.0, 0.0, 0.0, 0.0]] + [[0.0] * 4] * 10
    path = _build_path(rows)
    outcome, day, max_dd, culprit = simulate_path(
        path, DD_TRIGGER, DD_SCALE, dd_type="trailing", trailing_dd_pct=-0.03,
        daily_loss_pct=None,
    )
    assert outcome != "bust_trailing", f"pullback under threshold must not bust; got {outcome}"


# ── 3. ULP-precision boundary (mirrors test_simulate_path_direct_call_at_daily_loss_boundary) ──

def test_trailing_dd_boundary_ulp_precision():
    """Rule 0-T: the new comparison must apply the same round(...,6) ULP
    handling as the existing daily/static checks (Q-MCFP-1), not a raw <=.

    Construction: day 1 makes a $250,000 peak. Day 2's loss is one ULP
    toward zero from the *exact* 3%-of-peak dollar amount ($7,500), so the
    raw ratio lands just above -0.03 (less negative) — the raw comparison
    would silently fail to fire. round(ratio, 6) collapses this back to
    -0.03 and must fire on day 2.
    """
    peak = STARTING_EQUITY + 50_000.0  # 250,000 after day 1's gain
    trailing_dd_pct = -0.03
    pullback = math.nextafter(-7_500.0, 0.0)  # exact 3% of 250,000, nudged toward zero

    raw_ratio = pullback / peak
    assert raw_ratio > trailing_dd_pct, (
        f"construction invariant: raw FP must land above -0.03; got {raw_ratio!r}"
    )
    assert round(raw_ratio, 6) <= trailing_dd_pct, (
        f"construction invariant: round6 must collapse to -0.03 and fire; got {round(raw_ratio, 6)!r}"
    )

    rows = [[50_000.0, 0.0, 0.0, 0.0], [pullback, 0.0, 0.0, 0.0]] + [[0.0] * 4] * 10
    path = _build_path(rows)
    outcome, day, max_dd, culprit = simulate_path(
        path, DD_TRIGGER, DD_SCALE, dd_type="trailing", trailing_dd_pct=trailing_dd_pct,
        daily_loss_pct=None,
    )
    assert outcome == "bust_trailing", f"ULP-boundary pullback must bust; got {outcome}"
    assert day == 2
    assert culprit == 0


# ── 4. Culprit attribution matches bust_daily/bust_static (int, not None) ──

def test_trailing_bust_has_int_culprit():
    rows = [[0.0, 30_000.0, 0.0, 0.0], [0.0, -20_000.0, 0.0, 0.0]] + [[0.0] * 4] * 5
    path = _build_path(rows)
    outcome, _, _, culprit = simulate_path(
        path, DD_TRIGGER, DD_SCALE, dd_type="trailing", trailing_dd_pct=-0.03,
        daily_loss_pct=None,
    )
    assert outcome == "bust_trailing"
    assert culprit == 1


# ── 5. dd_type="static" (the default) never takes the trailing branch ──

def test_static_dd_type_never_takes_trailing_branch():
    """Safety proof: even with an absurdly tight trailing_dd_pct that would
    fire immediately if evaluated, the default dd_type="static" must never
    read it. This is what makes every existing call site (which never
    passes dd_type) provably unaffected by this change."""
    rows = [[50_000.0, 0.0, 0.0, 0.0], [-100.0, 0.0, 0.0, 0.0]] + [[0.0] * 4] * 10
    path = _build_path(rows)
    outcome, day, max_dd, culprit = simulate_path(
        path, DD_TRIGGER, DD_SCALE, trailing_dd_pct=-0.0001,  # dd_type omitted -> "static" default
    )
    assert outcome != "bust_trailing", (
        f"dd_type default must stay 'static' and ignore trailing_dd_pct; got {outcome}"
    )


# ── 6. Trailing busts even while still cumulatively profitable from start ──

def test_trailing_busts_even_when_cumulatively_profitable_from_start():
    """The semantic difference from bust_static: equity ends well ABOVE
    STARTING_EQUITY (still net profitable), yet trailing-from-peak still
    busts on the pullback. A static-from-start check would never fire here."""
    rows = [[100_000.0, 0.0, 0.0, 0.0], [-9_000.0, 0.0, 0.0, 0.0]] + [[0.0] * 4] * 10
    path = _build_path(rows)
    outcome, day, max_dd, culprit = simulate_path(
        path, DD_TRIGGER, DD_SCALE, dd_type="trailing", trailing_dd_pct=-0.03,
        daily_loss_pct=None,
    )
    assert outcome == "bust_trailing"
    # Sanity: equity after day 2 (300,000 - 9,000 = 291,000) is still far above
    # STARTING_EQUITY (200,000) -- confirms this is genuinely a peak-relative
    # bust, not something a from-start check would also have caught.
    assert (STARTING_EQUITY + 100_000.0 - 9_000.0) > STARTING_EQUITY


# ── 7. daily_loss_pct=None disables the daily-loss bust (Bulenox Option 1) ──

def test_daily_loss_pct_none_disables_daily_bust_check():
    """Bulenox Option 1 has no daily loss limit. A single-day loss that would
    trigger bust_daily under the FXIFY default must NOT bust when the caller
    passes daily_loss_pct=None — even though the account is still far enough
    above STARTING_EQUITY that the (unrelated) static-DD check can't fire
    either, isolating that it's specifically the daily check being disabled.

    Day 1 banks a $30K gain. Day 2 loses $15K (7.5% of STARTING_EQUITY —
    over the FXIFY 5% daily limit) but equity is still $15K net ABOVE start,
    so bust_static (from-start) can never fire regardless of daily_loss_pct.
    """
    rows = [[30_000.0, 0.0, 0.0, 0.0], [-15_000.0, 0.0, 0.0, 0.0]] + [[0.0] * 4] * 10
    path = _build_path(rows)
    outcome, day, max_dd, culprit = simulate_path(
        path, DD_TRIGGER, DD_SCALE, daily_loss_pct=None,
    )
    assert outcome not in ("bust_daily", "bust_static"), (
        f"daily_loss_pct=None must disable only the daily check, with static "
        f"structurally unable to fire here; got {outcome}"
    )


# ── 8. starting_equity override scales the static-DD threshold correctly ──

def test_starting_equity_override_scales_static_bust_threshold():
    """A Bulenox $50K-tier account must bust on 5%-of-$50K, not 5%-of-$200K.
    Proves the parameterization is genuinely load-bearing, not decorative."""
    tier_balance = 50_000.0
    rows = [[-0.06 * tier_balance, 0.0, 0.0, 0.0]] + [[0.0] * 4] * 10  # -6% of the $50K tier
    path = _build_path(rows)
    outcome, day, max_dd, culprit = simulate_path(
        path, DD_TRIGGER, DD_SCALE,
        starting_equity=tier_balance, static_dd_pct=-0.05, daily_loss_pct=None,
    )
    assert outcome == "bust_static", (
        f"a -6% day on a $50K account must bust a -5% static-DD rule; got {outcome}"
    )
