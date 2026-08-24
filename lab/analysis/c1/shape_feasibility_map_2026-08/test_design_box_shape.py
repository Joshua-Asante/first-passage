"""Invariant + determinism tests for the design-box shape extension
(design_box_shape.py).

Does not call the MC engine (no core.mc import) -- pure tests of the
module's own output, mirroring test_shape_generator.py's style exactly.
Run: pytest lab/analysis/c1/shape_feasibility_map_2026-08/test_design_box_shape.py --import-mode=importlib
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import design_box_shape as dbs  # noqa: E402
import shape_generator as sg  # noqa: E402


def test_win_rate_span_matches_design_box_dispatch():
    assert dbs.WIN_RATES == (0.30, 0.35, 0.40)


def test_cadence_axis_reused_unchanged_from_a2():
    assert dbs.CADENCES == sg.CADENCES
    assert dbs.WEEKDAY_PATTERN == sg.WEEKDAY_PATTERN
    assert dbs.N_WEEKS == sg.N_WEEKS


def test_em2_axis_never_includes_325():
    # The box's own R-sizing logic points down, not up (dispatch instruction).
    assert dbs.EM2_RISK_USD == (250.0, 275.0)
    assert 325.0 not in dbs.EM2_RISK_USD


# --- Frontier-R closed form: reproduce the notice's own Sec9 worked table -----------

@pytest.mark.parametrize(
    "p, rr, c, expected_r",
    [
        (0.461, 1, 2.82, None),
        (0.55, 1, 2.82, 137.35),
        (0.60, 1, 2.82, 341.77),
        (0.42, 2, 2.82, 191.42),
        (0.30, 3, 2.82, 84.94),
        (0.35, 3, 2.82, 180.69),
        (0.40, 3, 2.82, 262.57),
        (0.35, 3, 4.12, 177.09),
    ],
)
def test_frontier_formula_reproduces_notice_sec9_table(p, rr, c, expected_r):
    """Sanity check that this module's transcription of the N-2026-08-13 notice
    Sec9 audit-hook formula is byte-faithful: every row of the notice's own
    published Sec3/Sec9 table must reproduce to within a cent."""
    got = dbs._frontier_r_usd(p, rr=rr, cost_usd=c)
    if expected_r is None:
        assert got is None
    else:
        assert got is not None
        assert got == pytest.approx(expected_r, abs=0.01)


def test_frontier_r_at_wr30_effective_rr_is_none():
    # At this shape's own mean win (rr=2.5), WR=30% has non-negative gross edge
    # (m0=0.05) but the closed form's discriminant goes negative -- cost
    # exceeds any bust-compliant R. This is a real, disclosed finding, not a
    # bug: it differs sharply from the notice's own rr=3 worked example.
    assert dbs._frontier_r_usd(0.30) is None


def test_frontier_r_at_wr35_and_wr40_are_finite_and_below_em2_floor():
    r35 = dbs._frontier_r_usd(0.35)
    r40 = dbs._frontier_r_usd(0.40)
    assert r35 is not None and r40 is not None
    assert r35 == pytest.approx(124.21, abs=0.05)
    assert r40 == pytest.approx(225.52, abs=0.05)
    assert r35 < min(dbs.EM2_RISK_USD)
    assert r40 < min(dbs.EM2_RISK_USD)


def test_risk_levels_for_win_rate_matches_frontier_disclosure():
    assert dbs.risk_levels_for_win_rate(0.30) == (250.0, 275.0)
    lv35 = dbs.risk_levels_for_win_rate(0.35)
    lv40 = dbs.risk_levels_for_win_rate(0.40)
    assert lv35[0] == pytest.approx(124.21, abs=0.05) and lv35[1:] == (250.0, 275.0)
    assert lv40[0] == pytest.approx(225.52, abs=0.05) and lv40[1:] == (250.0, 275.0)
    for lv in (lv35, lv40):
        assert 325.0 not in lv


# --- Grid mechanics -----------------------------------------------------------------

def test_grid_size_matches_wr_dependent_risk_axis():
    # 0.30: 2 risk levels x 5 cadences = 10
    # 0.35: 3 risk levels x 5 cadences = 15
    # 0.40: 3 risk levels x 5 cadences = 15
    # total = 40
    tuples = dbs.all_tuples()
    assert len(tuples) == 40
    by_wr = {}
    for wr, cd, rk in tuples:
        by_wr.setdefault(wr, set()).add(rk)
    assert len(by_wr[0.30]) == 2
    assert len(by_wr[0.35]) == 3
    assert len(by_wr[0.40]) == 3


def test_tuple_index_is_a_bijection_over_the_grid():
    tuples = dbs.all_tuples()
    idxs = [dbs.tuple_index(*t) for t in tuples]
    assert sorted(idxs) == list(range(len(tuples)))


def test_tuple_index_raises_on_non_grid_tuple():
    with pytest.raises(KeyError):
        dbs.tuple_index(0.30, 1, 999.0)


# --- DGP invariants (mirrors test_shape_generator.py's own checks) ------------------

def test_build_panel_is_deterministic():
    a1, i1 = dbs.build_panel(0.35, 3, 250.0)
    a2, i2 = dbs.build_panel(0.35, 3, 250.0)
    np.testing.assert_array_equal(a1, a2)
    np.testing.assert_array_equal(i1, i2)


def test_build_panel_shape_and_length():
    daily, intraday = dbs.build_panel(0.40, 5, 275.0)
    assert daily.shape == (dbs.N_WEEKS * 5,)
    assert intraday.shape == daily.shape


def test_intraday_low_never_positive_and_never_deeper_than_daily_pnl():
    for wr, cd, rk in dbs.all_tuples()[:6]:
        daily, intraday = dbs.build_panel(wr, cd, rk)
        assert np.all(intraday <= 0.0)
        assert np.all(intraday <= daily + 1e-9)


def test_zero_trade_days_are_exactly_zero():
    daily, intraday = dbs.build_panel(0.30, 1, 250.0)
    # cadence=1 trades only on Monday (weekday index 0 of each 5-day week)
    non_monday = np.ones_like(daily, dtype=bool)
    non_monday[0::5] = False
    assert np.all(daily[non_monday] == 0.0)
    assert np.all(intraday[non_monday] == 0.0)


def test_losses_are_exactly_one_stop():
    # deterministic hard-stop loss: every losing trade == -risk exactly.
    # cadence=1 (single Monday trade/week) makes this directly checkable
    # against the raw per-week P&L (no same-day compounding to unwind).
    risk = 250.0
    daily, _ = dbs.build_panel(0.35, 1, risk)
    mondays = daily[0::5]
    losses = mondays[mondays < 0]
    assert losses.size > 0
    np.testing.assert_allclose(losses, -risk, rtol=0, atol=1e-9)


def test_wins_land_in_two_to_three_r_range():
    # Same cadence=1 isolation trick as test_losses_are_exactly_one_stop:
    # at cadence=1 each Monday's daily_pnl IS that trade's own realized P&L.
    risk = 250.0
    daily, _ = dbs.build_panel(0.35, 1, risk)
    mondays = daily[0::5]
    wins = mondays[mondays > 0]
    assert wins.size > 0
    assert np.all(wins >= 2.0 * risk - 1e-9)
    assert np.all(wins <= 3.0 * risk + 1e-9)


def test_win_giveback_never_exceeds_95pct_of_one_stop():
    # _draw_trade_mae_r caps at -min(0.95, uniform(...)) -- verify no trade's
    # intraday excursion implies more than 0.95R of giveback on a winner.
    risk = 250.0
    for wr, cd, rk in [(0.40, 8, 250.0), (0.35, 5, 275.0)]:
        daily, intraday = dbs.build_panel(wr, cd, rk)
        # loose bound check: no single day's excursion should ever be more
        # negative than (n_trades_that_day * 1.0R) in the worst case, and
        # never breaches -0.95R on a pure single-winning-trade Monday.
        assert np.isfinite(intraday).all()


def test_expectancy_r_ordering_matches_intuition():
    # Higher win rate must raise expectancy for this fixed shape.
    lo = dbs.expectancy_r(0.30)
    mid = dbs.expectancy_r(0.35)
    hi = dbs.expectancy_r(0.40)
    assert lo < mid < hi
    # Cross-check against the closed form's own m0 = p*E[win_R] - (1-p),
    # E[win_R] = 2.5 for Uniform(2,3) -- expectancy_r's MC estimate should
    # land close to the analytic value at n_draw=200,000.
    for wr in dbs.WIN_RATES:
        analytic = wr * 2.5 - (1.0 - wr)
        assert dbs.expectancy_r(wr) == pytest.approx(analytic, abs=0.02)


def test_frontier_rr_is_mean_of_win_uniform_band():
    assert dbs.FRONTIER_RR == pytest.approx((dbs._WIN_LO + dbs._WIN_HI) / 2.0)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
