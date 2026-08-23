"""Invariant + determinism tests for the A2 synthetic payoff-shape generator.

Does not call the MC engine (no core.mc import) -- pure tests of
shape_generator.py's own output. Run: pytest lab/analysis/c1/shape_feasibility_map_2026-08/test_shape_generator.py --import-mode=importlib
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import shape_generator as sg  # noqa: E402


def test_grid_size():
    assert len(sg.WIN_RATES) == 7
    assert len(sg.SHAPES) == 3
    assert len(sg.CADENCES) == 5
    assert len(sg.RISK_USD) == 3
    assert len(sg.all_tuples()) == 7 * 3 * 5 * 3 == 315


def test_tuple_index_is_a_bijection_over_the_grid():
    idxs = [sg.tuple_index(*t) for t in sg.all_tuples()]
    assert sorted(idxs) == list(range(315))


def test_em2_frontier_never_exceeds_top_published_cell():
    assert max(sg.RISK_USD) == 325.0
    assert set(sg.RISK_USD) == {250.0, 275.0, 325.0}


@pytest.mark.parametrize("cadence", sg.CADENCES)
def test_weekday_pattern_every_week_has_at_least_one_trade(cadence):
    pattern = sg.WEEKDAY_PATTERN[cadence]
    assert len(pattern) == cadence
    assert all(0 <= wd <= 4 for wd in pattern)


def test_build_panel_is_deterministic():
    a1, i1 = sg.build_panel(0.55, "mild_right_skew", 3, 275.0)
    a2, i2 = sg.build_panel(0.55, "mild_right_skew", 3, 275.0)
    np.testing.assert_array_equal(a1, a2)
    np.testing.assert_array_equal(i1, i2)


def test_build_panel_shape_and_length():
    daily, intraday = sg.build_panel(0.50, "symmetric", 5, 250.0)
    assert daily.shape == (sg.N_WEEKS * 5,)
    assert intraday.shape == daily.shape


def test_intraday_low_never_positive_and_never_deeper_than_daily_pnl():
    for shape in sg.SHAPES:
        daily, intraday = sg.build_panel(0.45, shape, 8, 325.0)
        assert np.all(intraday <= 0.0)
        # the day's worst mark can never be BETTER than its own close
        assert np.all(intraday <= daily + 1e-9)


def test_zero_trade_days_are_exactly_zero():
    daily, intraday = sg.build_panel(0.60, "bounded_clustered", 1, 250.0)
    # cadence=1 trades only on Monday (weekday index 0 of each 5-day week)
    non_monday = np.ones_like(daily, dtype=bool)
    non_monday[0::5] = False
    assert np.all(daily[non_monday] == 0.0)
    assert np.all(intraday[non_monday] == 0.0)


def test_bounded_clustered_losses_are_exactly_one_stop():
    # deterministic hard-stop loss: every losing trade == -risk exactly.
    # cadence=1 (single Monday trade/week) makes this directly checkable
    # against the raw per-week P&L (no same-day compounding to unwind).
    risk = 250.0
    daily, _ = sg.build_panel(0.40, "bounded_clustered", 1, risk)
    mondays = daily[0::5]
    losses = mondays[mondays < 0]
    assert losses.size > 0
    np.testing.assert_allclose(losses, -risk, rtol=0, atol=1e-9)


def test_expectancy_r_ordering_matches_intuition():
    # Higher win rate must raise expectancy for a fixed shape.
    lo = sg.expectancy_r(0.40, "symmetric")
    hi = sg.expectancy_r(0.70, "symmetric")
    assert hi > lo
    # At equal win rate, mild_right_skew's fatter win tail beats symmetric.
    sym = sg.expectancy_r(0.50, "symmetric")
    skew = sg.expectancy_r(0.50, "mild_right_skew")
    assert skew > sym


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
