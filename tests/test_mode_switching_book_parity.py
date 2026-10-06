"""Kernel mode rule vs ``ops/c1_rail/book_policy.py`` (frozen card §0.5 item 6).

The mode-switching kernel in ``core/mc/simulation.simulate_path`` decides a day is
protected when ``round((equity - peak) / peak, 6) <= -mode_trigger``, on the settled
prior close against the end-of-day peak ratchet. ``ops/c1_rail/book_policy.py``
expresses the SAME rule from the accepted book side as
``round((peak - equity) / peak, 6) >= policy.trigger`` with no latch and prior-close
timing. This file pins that parity — the only place in the repo allowed to import
both surfaces (``tests/`` is contract-exempt; ``lab`` may not import ``ops``).

No new public API is added by the kernel for this: the mode sequence is observed
end-to-end by giving ``simulate_path`` a protected twin whose P&L is zero, so the
equity path itself (and, per day, a bust-inducing probe on exactly one protected
day) reveals which channel each session read. Synthetic inputs only.
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pytest

from c1_signal_daemon.book_protocol import Mode
from c1_rail.book_policy import (
    BookProtectionClock,
    candidate_book_protection_policy,
    is_protected,
)
from core.mc.simulation import simulate_path

START = 100_000.0
MODE_TRIGGER = 0.01
# One protection mechanism only: dd_trigger >= 1.0 keeps continuous scaling off.
NO_SCALING_TRIGGER = 10.0
UNIT_SCALE = 1.0
# A reachable static floor at $90,000: every hand-designed sequence below stays above
# it on its own, while a single -$30,000 protected probe day busts from any of them.
PROBE = -30_000.0

BARRIER = dict(
    starting_equity=START,
    daily_loss_pct=None,
    dd_type="static",
    static_dd_pct=-0.10,
    profit_target=START * 100.0,
    min_trading_days=0,
    inactivity_limit=10_000_000,
    consistency_frac=None,
)

FIRST_SESSION = date(2026, 1, 5)


def _path(daily_pnls) -> np.ndarray:
    return np.array([[float(p)] for p in daily_pnls], dtype=float)


# ── parity of the predicate itself ──────────────────────────────────────────


BOUNDARY_PAIRS = [
    (100_000.0, 100_000.0),   # at peak
    (101_000.0, 100_000.0),   # above peak: kernel dd is +1%, book clamps to 0
    (99_000.0, 100_000.0),    # exactly -1.000000% -> protected
    (99_000.01, 100_000.0),   # -0.0099999 rounds UP to 1% -> protected
    (99_000.6, 100_000.0),    # -0.009994 rounds below -> not protected
    (99_999.0, 100_000.0),    # -0.001% -> not protected
    (0.0, 100_000.0),         # wiped out -> protected
    (50_000.0, 100_000.0),
    (2.97, 3.0),              # exactly -1% on a $3 peak
    (2.98, 3.0),
    (1.0, 1.0),
    (0.5, 1.0),
    (98_765.43, 99_999.99),
]


@pytest.mark.parametrize("equity,peak", BOUNDARY_PAIRS)
def test_kernel_predicate_equals_book_policy_is_protected(equity, peak):
    policy = candidate_book_protection_policy()
    kernel = round((equity - peak) / peak, 6) <= -MODE_TRIGGER
    assert kernel == is_protected(equity, peak, policy)


@pytest.mark.parametrize(
    "peak", [1.0, 3.0, 123.45, 1_000.0, 99_999.99, 100_000.0, 250_000.0]
)
def test_kernel_predicate_grid_matches_book_policy(peak):
    """Dense grid across the trigger, including the ULP rounding band around 1%."""
    policy = candidate_book_protection_policy()
    for equity in np.linspace(0.0, 2.0 * peak, 401):
        kernel = round((float(equity) - peak) / peak, 6) <= -MODE_TRIGGER
        assert kernel == is_protected(float(equity), peak, policy), (equity, peak)


@pytest.mark.parametrize("peak", [1.0, 3.0, 100_000.0])
def test_the_rounded_boundary_is_inclusive_on_both_sides(peak):
    """Equity exactly 1% below peak is protected by both surfaces."""
    policy = candidate_book_protection_policy()
    equity = peak * (1.0 - MODE_TRIGGER)
    assert round((equity - peak) / peak, 6) == -MODE_TRIGGER
    assert round((peak - equity) / peak, 6) == MODE_TRIGGER
    assert is_protected(equity, peak, policy) is True


# ── the clock replay (the book-side mode sequence for a P&L series) ─────────


def replay_with_book_clock(daily_pnls):
    """Step ``BookProtectionClock`` over the closes and record its per-session modes.

    Returns (modes, max_dd, final_equity). The peak ratchet and the mode timing are
    the clock's own: mode for session i from the last settled close strictly before
    it, no latch.
    """
    clock = BookProtectionClock(
        policy=candidate_book_protection_policy(),
        initial_equity=START,
        initial_peak=START,
    )
    equity = START
    peak = START
    max_dd = 0.0
    modes = []
    for i, pnl in enumerate(daily_pnls):
        session = FIRST_SESSION + timedelta(days=i)
        protected = clock.mode_for(session) is Mode.PROTECTED
        modes.append(protected)
        equity += 0.0 if protected else float(pnl)
        dd = (peak - equity) / peak
        if dd > max_dd:
            max_dd = dd
        clock.settle(session, equity)  # ratchets the clock's own EOD peak, no latch
        if equity > peak:
            peak = equity
    return modes, max_dd, equity


SEQUENCES = [
    ("never-draws-down", [100.0, 250.0, -50.0, 400.0, 120.0, 80.0]),
    (
        "protected-from-day-2-and-stays",
        [-2_000.0, -50.0, -40.0, -60.0, -50.0, -50.0, -70.0],
    ),
    (
        "protected-then-recovered-then-protected-again",
        [-2_000.0, -50.0, 3_000.0, -500.0, -2_500.0, -40.0, 6_000.0, -1_200.0],
    ),
    (
        "exact-one-percent-boundary",
        [-1_000.0, -10.0, 2_500.0, -1_100.0, -30.0, 900.0],
    ),
    ("just-above-one-percent", [-999.0, -900.0, -1_500.0, -2_000.0, 4_000.0, -1_900.0]),
]


@pytest.mark.parametrize("label,pnls", SEQUENCES, ids=[s[0] for s in SEQUENCES])
def test_kernel_mode_sequence_matches_the_book_clock(label, pnls):
    """A zero-P&L protected twin makes the equity path the mode sequence itself."""
    modes, clock_max_dd, _final_equity = replay_with_book_clock(pnls)
    n = len(pnls)
    outcome, day, max_dd, culprit = simulate_path(
        _path(pnls),
        NO_SCALING_TRIGGER,
        UNIT_SCALE,
        n,
        protected_path=_path([0.0] * n),
        mode_trigger=MODE_TRIGGER,
        **BARRIER,
    )
    assert outcome == "horizon_cap"
    assert day == n
    assert culprit is None
    assert max_dd == pytest.approx(clock_max_dd, rel=1e-15, abs=1e-15)
    # Sanity: the replay is not degenerate for the sequences designed to switch.
    if label != "never-draws-down":
        assert any(modes), "expected at least one protected session"


@pytest.mark.parametrize("label,pnls", SEQUENCES, ids=[s[0] for s in SEQUENCES])
def test_kernel_switches_exactly_on_the_day_the_clock_protects(label, pnls):
    """Per-day probe: a bust is possible on day k+1 if and only if day k was protected.

    The protected twin is zero everywhere except day k, where it is a -$30,000 loss.
    Reading it busts the $90,000 static floor from every equity level reached here;
    not reading it leaves the path identical to the all-zero twin, which never busts.
    """
    modes, _max_dd, _equity = replay_with_book_clock(pnls)
    n = len(pnls)
    for k in range(n):
        protected = [0.0] * n
        protected[k] = PROBE
        outcome, day, _max_dd, _culprit = simulate_path(
            _path(pnls),
            NO_SCALING_TRIGGER,
            UNIT_SCALE,
            n,
            protected_path=_path(protected),
            mode_trigger=MODE_TRIGGER,
            **BARRIER,
        )
        if modes[k]:
            assert outcome == "bust_static"
            assert day == k + 1
        else:
            assert outcome == "horizon_cap"


def test_boundary_sequence_mode_days_are_the_expected_ones():
    """Cross-check the replay's own shape: exactly-1% day 2 is protected, and the
    just-above-1% variant is not."""
    boundary_modes, _, _ = replay_with_book_clock(SEQUENCES[3][1])
    assert boundary_modes[0] is False          # pristine start
    assert boundary_modes[1] is True           # equity exactly 99,000

    above_modes, _, _ = replay_with_book_clock(SEQUENCES[4][1])
    assert above_modes[0] is False
    assert above_modes[1] is False             # equity 99,001 = -0.999%
    assert any(above_modes[2:])


def test_clock_peak_ratchet_matches_the_kernel_peak():
    """The clock's EOD peak ratchet and the kernel's are the same sequence."""
    pnls = [-2_000.0, 5_000.0, -4_000.0, 2_000.0, -1_500.0, 500.0, -3_000.0, 100.0]
    modes, clock_max_dd, _ = replay_with_book_clock(pnls)
    # Independent kernel-side replay of the identical peak/max-dd law, using the
    # clock's own modes to select the channel (zero P&L when protected).
    equity = peak = START
    max_dd = 0.0
    for pnl, protected in zip(pnls, modes):
        equity += 0.0 if protected else float(pnl)
        dd = (peak - equity) / peak
        if dd > max_dd:
            max_dd = dd
        if equity > peak:
            peak = equity
    out = simulate_path(
        _path(pnls), NO_SCALING_TRIGGER, UNIT_SCALE, len(pnls),
        protected_path=_path([0.0] * len(pnls)), mode_trigger=MODE_TRIGGER, **BARRIER,
    )
    assert out[2] == pytest.approx(max_dd, rel=1e-15, abs=1e-15)
    assert out[2] == pytest.approx(clock_max_dd, rel=1e-15, abs=1e-15)
