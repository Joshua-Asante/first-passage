"""Intraday barrier enforcement in simulate_path (opt-in `intraday_low`).

Tradeify's rule page (help.tradeify.co art. 10495897, read 2026-07-30) states the
drawdown LIMIT updates end-of-day but the BREACH is enforced in real time. The engine
carried one P&L scalar per business day and tested only the CLOSE, so it could not see
a path that touched the floor intraday and recovered.

The load-bearing property is that passing nothing changes nothing: the historical MC
anchor (99.83/0.17/4.37) must reproduce byte-for-byte.
"""
from __future__ import annotations

import numpy as np
import pytest

from core.mc.simulation import HISTORICAL_CHALLENGE_FIRM_KWARGS, simulate_path

START = 100_000.0
# Tradeify Select 100K eval geometry, corrected: an unreachable lock reduces
# `trailing_locking` to a pure fixed-$3,000 end-of-day trail off peak.
TRADEIFY = dict(
    starting_equity=START,
    daily_loss_pct=None,
    dd_type="trailing_locking",
    trailing_dd_pct=-0.03,
    dd_lock_offset_usd=1_000_000.0,
    profit_target=START * 10,      # unreachable: isolate the barrier
    min_trading_days=0,
    inactivity_limit=10_000,
    consistency_frac=None,
)


def _path(daily_pnls):
    return np.array([[p] for p in daily_pnls], dtype=float)


def test_omitting_and_passing_none_are_identical():
    """The legacy call surface must be untouched."""
    path = _path([-500.0, -400.0, -300.0])
    a = simulate_path(path, 0.015, 0.40, 3, **TRADEIFY)
    b = simulate_path(path, 0.015, 0.40, 3, intraday_low=None, **TRADEIFY)
    assert a == b


def test_close_above_floor_but_intraday_touch_busts():
    """The whole point: a day that dips to the floor and recovers by the close.

    Floor is peak - $3,000 = $97,000. The day closes at $99,900 (safe on the close)
    but reaches $96,500 intraday, which the venue treats as an immediate failure.
    """
    path = _path([-100.0])
    survives = simulate_path(path, 0.015, 0.40, 1, **TRADEIFY)
    assert survives[0] != "bust_trailing", "control: the close alone must survive"

    busts = simulate_path(path, 0.015, 0.40, 1,
                          intraday_low=np.array([-3_500.0]), **TRADEIFY)
    assert busts[0] == "bust_trailing"
    assert busts[1] == 1


def test_shallow_intraday_excursion_does_not_bust():
    """The barrier must not fire merely because an intraday series was supplied."""
    path = _path([-100.0])
    out = simulate_path(path, 0.015, 0.40, 1,
                        intraday_low=np.array([-500.0]), **TRADEIFY)
    assert out[0] != "bust_trailing"


def test_floor_still_ratchets_on_END_OF_DAY_equity_only():
    """Two-clock geometry: intraday moves the TESTED equity, never the floor.

    Day 1 closes +$2,000 so the EOD peak becomes $102,000 and the floor $99,000.
    Day 2 dips $2,500 below its open ($99,500) — above the floor, so it survives.
    Were the floor (wrongly) trailing intraday highs, this would fail.
    """
    path = _path([2_000.0, -100.0])
    out = simulate_path(path, 0.015, 0.40, 2,
                        intraday_low=np.array([0.0, -2_500.0]), **TRADEIFY)
    assert out[0] != "bust_trailing"

    deeper = simulate_path(path, 0.015, 0.40, 2,
                           intraday_low=np.array([0.0, -3_100.0]), **TRADEIFY)
    assert deeper[0] == "bust_trailing"


def test_intraday_low_is_scaled_by_dd_protection_exactly_like_path():
    """A de-risked day takes a proportionally smaller excursion.

    Day 1 loses 2%, putting equity below the 1.5% DD trigger, so day 2 is sized at
    0.40x. Its raw -$4,000 excursion must be scaled to -$1,600, not applied whole.
    """
    path = _path([-2_000.0, -10.0])
    # Day 1 closes at $98,000, which is -2.0% from the $100,000 peak and so trips the
    # 1.5% DD trigger; day 2 is therefore sized at 0.40x. Floor stays peak - $3,000 =
    # $97,000 (the peak never rose).
    #
    # DISCRIMINATING CASE: a raw -$2,000 excursion on day 2.
    #   scaled   0.40 x -2,000 = -800   -> 98,000 - 800   = $97,200  SURVIVES
    #   unscaled          -2,000        -> 98,000 - 2,000 = $96,000  would BUST
    # So this assertion fails if and only if the scaling is not applied.
    scaled_ok = simulate_path(path, 0.015, 0.40, 2,
                              intraday_low=np.array([0.0, -2_000.0]), **TRADEIFY)
    assert scaled_ok[0] != "bust_trailing", "dd_scale was not applied to intraday_low"

    # CONTROL: scaling must not become a blanket exemption. A raw -$4,000 excursion
    # still breaches after scaling (0.40 x -4,000 = -1,600 -> $96,400 < $97,000).
    deep = simulate_path(path, 0.015, 0.40, 2,
                         intraday_low=np.array([0.0, -4_000.0]), **TRADEIFY)
    assert deep[0] == "bust_trailing", "a genuinely deep excursion must still bust"


def test_rejects_a_positive_excursion():
    with pytest.raises(ValueError, match="must be <= 0.0"):
        simulate_path(_path([-100.0]), 0.015, 0.40, 1,
                      intraday_low=np.array([50.0]), **TRADEIFY)


def test_rejects_a_series_shorter_than_the_horizon():
    with pytest.raises(ValueError, match="must cover the horizon"):
        simulate_path(_path([-100.0, -100.0]), 0.015, 0.40, 2,
                      intraday_low=np.array([-10.0]), **TRADEIFY)


def test_historical_fixture_does_not_carry_the_new_keyword():
    """`intraday_low` is PATH data, not firm semantics.

    If it ever appears in the firm-kwargs fixture, a firm config would be implying an
    intraday series, and the historical anchor's calibration basis would have changed.
    """
    assert "intraday_low" not in HISTORICAL_CHALLENGE_FIRM_KWARGS


def test_static_and_trailing_branches_also_see_the_intraday_low():
    """The venue finding is not Tradeify-specific; intraday-trailing firms exist."""
    static_cfg = dict(TRADEIFY)
    static_cfg.update(dd_type="static", static_dd_pct=-0.03,
                      trailing_dd_pct=None, dd_lock_offset_usd=None)
    out = simulate_path(_path([-100.0]), 0.015, 0.40, 1,
                        intraday_low=np.array([-3_500.0]), **static_cfg)
    assert out[0] == "bust_static"

    trail_cfg = dict(TRADEIFY)
    trail_cfg.update(dd_type="trailing", dd_lock_offset_usd=None)
    out2 = simulate_path(_path([-100.0]), 0.015, 0.40, 1,
                         intraday_low=np.array([-3_500.0]), **trail_cfg)
    assert out2[0] == "bust_trailing"
