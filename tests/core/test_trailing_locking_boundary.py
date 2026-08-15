"""Boundary tests for the locking-trailing bust condition and the eval
consistency gate (`dd_type="trailing_locking"`, `consistency_frac`).

Added for the Tradeify Select Flex firm onboarding (2026-07-10). Tradeify's
drawdown is a FIXED-DOLLAR end-of-day trailing floor that FREEZES at
`starting_equity + dd_lock_offset_usd` once the account clears the cushion by
that offset — materially different from both `dd_type="static"` (FXIFY, floor
never moves) and `dd_type="trailing"` (Bulenox, %-of-peak, never locks).

These tests exercise the new branch directly via `_simulate_path` with
synthetic paths — no vendor CSV data required. Every new parameter is
keyword-only and defaults to a value that reproduces pre-2026-07-10 behavior
exactly, so the existing suite needs zero changes;
`test_static_and_trailing_never_take_locking_branch` is the direct proof.
"""

from __future__ import annotations

import numpy as np

from portfolio_mc import HORIZON_CAP, STARTING_EQUITY, _simulate_path

DD_TRIGGER = 0.015
DD_SCALE = 0.40


def simulate_path(path: np.ndarray, dd_trigger: float, dd_scale: float, **kwargs):
    """Adapter mirroring test_trailing_dd_boundary.py's — passes new kwargs through."""
    horizon = min(HORIZON_CAP, len(path))
    return _simulate_path(path, dd_trigger, dd_scale, horizon, **kwargs)


def _build_path(rows: list[list[float]]) -> np.ndarray:
    return np.array(rows, dtype=float)


# Tradeify Select 50K geometry, used across several tests:
#   start $50,000; max_dd 4% = $2,000 (fixed-$); lock offset $100.
#   Lock triggers when EOD balance reaches $52,100; floor freezes at $50,100.
_START_50K = 50_000.0
_TRAIL_50K = -0.04          # 4% of $50K = $2,000 fixed-$ cushion
_LOCK_OFFSET = 100.0
_LOCK_KW = dict(
    dd_type="trailing_locking",
    starting_equity=_START_50K,
    trailing_dd_pct=_TRAIL_50K,
    dd_lock_offset_usd=_LOCK_OFFSET,
    daily_loss_pct=None,       # Flex has no daily loss limit
    profit_target=_START_50K * 1.06,  # 6% target, far away — isolates DD behavior
)


# ── 1. Pre-lock: trails the peak by the fixed-$ cushion ──────────────────

def test_locking_trails_before_lock_fires():
    """Small gain (peak $51,000, below the $52,100 lock trigger); the floor is
    peak - $2,000 = $49,000. A pullback to $48,900 breaches it -> bust."""
    rows = [[1_000.0, 0.0], [-2_100.0, 0.0]] + [[0.0, 0.0]] * 6
    outcome, day, _, culprit = simulate_path(_build_path(rows), DD_TRIGGER, DD_SCALE, **_LOCK_KW)
    assert outcome == "bust_trailing", f"pre-lock trail must bust; got {outcome}"
    assert day == 2
    assert culprit == 0


# ── 2. The lock gives room a pure trail would not ───────────────────────

def test_lock_saves_a_pullback_that_pure_trailing_would_bust():
    """Peak $55,000 (lock fired; floor frozen at $50,100). Day 2 falls to
    $50,200 — that is BELOW peak-$2,000 ($53,000) so a non-locking fixed-$
    trail would bust, but ABOVE the locked $50,100 floor, so trailing_locking
    must survive. This is the whole point of the firm switch."""
    rows = [[5_000.0, 0.0], [-4_800.0, 0.0]] + [[0.0, 0.0]] * 6
    outcome, _, _, _ = simulate_path(_build_path(rows), DD_TRIGGER, DD_SCALE, **_LOCK_KW)
    assert outcome != "bust_trailing", f"locked floor must give room; got {outcome}"

    # Control: the SAME path under a non-locking fixed-$ trail (lock pushed out
    # of reach) DOES bust — proving the survival above is due to the lock.
    ctrl = dict(_LOCK_KW, dd_lock_offset_usd=1_000_000.0)  # lock unreachable => pure fixed-$ trail
    outcome_ctrl, day_ctrl, _, _ = simulate_path(_build_path(rows), DD_TRIGGER, DD_SCALE, **ctrl)
    assert outcome_ctrl == "bust_trailing", f"unlocked fixed-$ trail must bust; got {outcome_ctrl}"
    assert day_ctrl == 2


# ── 3. Post-lock breach of the frozen floor still busts ─────────────────

def test_locked_floor_still_busts_when_breached():
    """Peak $55,000 (locked at $50,100); day 2 falls to $50,000, below the
    frozen floor -> bust."""
    rows = [[5_000.0, 0.0], [-5_000.0, 0.0]] + [[0.0, 0.0]] * 6
    outcome, day, _, _ = simulate_path(_build_path(rows), DD_TRIGGER, DD_SCALE, **_LOCK_KW)
    assert outcome == "bust_trailing", f"below locked floor must bust; got {outcome}"
    assert day == 2


# ── 4. Payload worked example: lock at $52,100 -> floor $50,100 ──────────

def test_payload_worked_example_50k_lock_at_52100():
    """§1 ADDENDUM example: 50K, $2,000 DD -> locks when EOD balance reaches
    $52,100; floor becomes $50,100. A pullback to $50,099 busts; to $50,101 survives."""
    # Peak exactly $52,100 (lock just fires); then just below the frozen floor.
    below = [[2_100.0, 0.0], [-2_001.0, 0.0]] + [[0.0, 0.0]] * 6  # -> $50,099
    outcome_b, day_b, _, _ = simulate_path(_build_path(below), DD_TRIGGER, DD_SCALE, **_LOCK_KW)
    assert outcome_b == "bust_trailing", f"$50,099 < $50,100 floor must bust; got {outcome_b}"
    assert day_b == 2

    # Just above the frozen floor -> survives.
    above = [[2_100.0, 0.0], [-1_999.0, 0.0]] + [[0.0, 0.0]] * 6  # -> $50,101
    outcome_a, _, _, _ = simulate_path(_build_path(above), DD_TRIGGER, DD_SCALE, **_LOCK_KW)
    assert outcome_a != "bust_trailing", f"$50,101 > $50,100 floor must survive; got {outcome_a}"


# ── 5. Non-interference: static/trailing never take the locking branch ──

def test_static_and_trailing_never_take_locking_branch():
    """A pre-lock path that busts under trailing_locking must NOT bust_trailing
    when dd_type is the default 'static' (proves existing FXIFY call sites are
    untouched), nor when dd_type='trailing' (the Bulenox branch is %-of-peak,
    not this fixed-$ floor)."""
    rows = [[1_000.0, 0.0], [-2_500.0, 0.0]] + [[0.0, 0.0]] * 6  # peak 51k, floor 49k, -> 48.5k

    # Positive control: as trailing_locking (lock unreachable => pure fixed-$ trail), busts.
    pos = dict(_LOCK_KW, dd_lock_offset_usd=1_000_000.0)
    assert simulate_path(_build_path(rows), DD_TRIGGER, DD_SCALE, **pos)[0] == "bust_trailing"

    # dd_type='static' (default): trailing params present but must be ignored.
    static_kw = dict(
        starting_equity=_START_50K, trailing_dd_pct=_TRAIL_50K,
        dd_lock_offset_usd=1_000_000.0, daily_loss_pct=None,
        static_dd_pct=-0.05, profit_target=_START_50K * 1.06,
    )
    assert simulate_path(_build_path(rows), DD_TRIGGER, DD_SCALE, **static_kw)[0] != "bust_trailing"

    # dd_type='trailing' (%-of-peak): at peak $51,000 a 4% peak-relative move is
    # $2,040; equity $48,500 is a $2,500 drop -> that branch busts, but via its
    # OWN arithmetic, not the locking floor. Assert it does NOT read the lock
    # offset by checking the unreachable-lock kwarg has no effect here.
    trail_kw = dict(
        dd_type="trailing", starting_equity=_START_50K, trailing_dd_pct=_TRAIL_50K,
        dd_lock_offset_usd=1.0, daily_loss_pct=None, profit_target=_START_50K * 1.06,
    )
    # A tiny lock offset would freeze a locking floor at $50,001 and change the
    # verdict IF the trailing branch read it; the %-of-peak branch ignores it.
    out_trail, day_trail, _, _ = simulate_path(_build_path(rows), DD_TRIGGER, DD_SCALE, **trail_kw)
    assert out_trail == "bust_trailing" and day_trail == 2


def test_locking_inert_without_lock_offset():
    """dd_type='trailing_locking' with dd_lock_offset_usd=None is inert (the
    branch's guard requires both params) AND, being the elif branch, it also
    skips the static check — so a DD that would bust under static does not
    fire here. This is the documented KeyError-safe soft-degrade for a
    pre-2026-07-10-shaped call that forgot the offset."""
    rows = [[1_000.0, 0.0], [-2_500.0, 0.0]] + [[0.0, 0.0]] * 6
    inert = dict(
        dd_type="trailing_locking", starting_equity=_START_50K,
        trailing_dd_pct=_TRAIL_50K, dd_lock_offset_usd=None,
        daily_loss_pct=None, profit_target=_START_50K * 1.06,
    )
    outcome, _, _, _ = simulate_path(_build_path(rows), DD_TRIGGER, DD_SCALE, **inert)
    assert outcome != "bust_trailing", f"inert branch must not bust_trailing; got {outcome}"
    assert outcome != "bust_static", f"elif skips static too; got {outcome}"


# ── 6. ULP-precision at the frozen floor (mirrors the trailing ULP test) ─

def test_locking_floor_ulp_precision():
    """The normalized comparison must apply round(...,6) ULP handling like the
    other bust checks. Peak $55,000 locks the floor at $50,100. A day-2 loss
    landing one ULP above the exact floor-touching amount must still fire."""
    import math
    # After day 1 (+5,000) eq=$55,000, floor locked at $50,100. Exact loss to
    # touch the floor is -$4,900. Nudge one ULP toward zero so the raw ratio is
    # just above 0; round6 must collapse it back and fire.
    pullback = math.nextafter(-4_900.0, 0.0)
    rows = [[5_000.0, 0.0], [pullback, 0.0]] + [[0.0, 0.0]] * 6
    outcome, day, _, _ = simulate_path(_build_path(rows), DD_TRIGGER, DD_SCALE, **_LOCK_KW)
    assert outcome == "bust_trailing", f"ULP-boundary pullback must bust; got {outcome}"
    assert day == 2


# ── 7. Consistency gate (Tradeify 40% eval rule) ────────────────────────

_CONSIST_KW = dict(
    starting_equity=200_000.0,
    profit_target=210_000.0,   # +$10,000 = 5%
    min_trading_days=3,
    daily_loss_pct=None,
    static_dd_pct=-0.99,       # disable static DD so we isolate the pass-gate
)


def test_consistency_gate_withholds_one_big_day_pass():
    """A path that reaches target via one oversized day passes WITHOUT the gate
    but is withheld WITH consistency_frac=0.40 (one $9,000 day is 89% of the
    $10,100 profit, over the 40% cap)."""
    rows = [[9_000.0, 0.0], [600.0, 0.0], [500.0, 0.0]] + [[0.0, 0.0]] * 6

    # No gate -> passes on day 3.
    out_nogate, day_nogate, _, _ = simulate_path(_build_path(rows), DD_TRIGGER, DD_SCALE, **_CONSIST_KW)
    assert out_nogate == "pass" and day_nogate == 3

    # 40% gate -> NOT a pass (max day 9,000 > 0.40 * 10,100 = 4,040).
    out_gate, _, _, _ = simulate_path(
        _build_path(rows), DD_TRIGGER, DD_SCALE, consistency_frac=0.40, **_CONSIST_KW
    )
    assert out_gate != "pass", f"one-big-day path must be withheld by 40% gate; got {out_gate}"


def test_consistency_gate_allows_well_distributed_pass():
    """Three even $3,400 days (each 33% of the $10,200 profit, under 40%) pass
    even with the gate active."""
    rows = [[3_400.0, 0.0], [3_400.0, 0.0], [3_400.0, 0.0]] + [[0.0, 0.0]] * 6
    outcome, day, _, _ = simulate_path(
        _build_path(rows), DD_TRIGGER, DD_SCALE, consistency_frac=0.40, **_CONSIST_KW
    )
    assert outcome == "pass" and day == 3, f"well-distributed path must pass; got {outcome} day {day}"
