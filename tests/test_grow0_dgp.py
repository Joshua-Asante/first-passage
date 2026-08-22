import numpy as np

from discovery.grow0_dgp import (
    EDGE_DOLLARS,
    N_TRAIN_DAYS,
    NULL_PARAMS,
    TRUE_EDGE_VARIANT_INDEX,
    draw_daily_pnl,
)


def test_constants_match_prereg_section_3():
    assert N_TRAIN_DAYS == 1638
    assert EDGE_DOLLARS == 64.4412
    assert TRUE_EDGE_VARIANT_INDEX == 5
    assert NULL_PARAMS == {
        "p_active": 0.60,
        "p_win": 0.45,
        "win_mean": 200.0,
        "win_sd": 80.0,
        "loss_mean": -163.60,
        "loss_sd": 60.0,
    }


def test_draw_daily_pnl_shape_and_reproducibility():
    pnl_a = draw_daily_pnl(42, n_days=100)
    pnl_b = draw_daily_pnl(42, n_days=100)
    assert pnl_a.shape == (100,)
    np.testing.assert_array_equal(pnl_a, pnl_b)  # same seed -> bit-identical


def test_draw_daily_pnl_null_vs_edge_differ_only_in_active_day_mean():
    n = 200_000  # large n so sample means are stable to ~1% for this smoke test
    null_pnl = draw_daily_pnl(7, n_days=n, edge=False)
    edge_pnl = draw_daily_pnl(8, n_days=n, edge=True)  # different seed -> independent draw
    # active-day means: null ~= $0.02, edge ~= $64.46 (prereg §3) -- loose bounds, not a
    # statistical power test, just a sanity check the shift is wired correctly
    null_active_mean = null_pnl[null_pnl != 0.0].mean()
    edge_active_mean = edge_pnl[edge_pnl != 0.0].mean()
    assert -5.0 < null_active_mean < 5.0
    assert 55.0 < edge_active_mean < 75.0


def test_draw_daily_pnl_active_fraction_matches_p_active():
    n = 200_000
    pnl = draw_daily_pnl(9, n_days=n)
    active_fraction = float(np.count_nonzero(pnl)) / n
    assert 0.59 < active_fraction < 0.61  # p_active = 0.60
