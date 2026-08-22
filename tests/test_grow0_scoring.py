import numpy as np

from discovery.grow0_scoring import annualized_sharpe, gate_a_passes, gate_b_passes


def test_annualized_sharpe_known_value():
    # constant positive series: mean=$100, sd=0 is undefined (div by zero) -- use a
    # simple two-value alternating series with a known closed-form Sharpe
    pnl = np.array([100.0, -100.0] * 819)  # 1638 days, mean=0, sd=100
    assert annualized_sharpe(pnl) == 0.0

    pnl2 = np.full(252, 10.0)
    pnl2[0] = 20.0  # tiny variance so sd != 0
    sr = annualized_sharpe(pnl2)
    expected_mean = pnl2.mean()
    expected_sd = pnl2.std(ddof=0)
    assert sr == expected_mean / expected_sd * np.sqrt(252)


def test_gate_a_passes_boundary():
    assert gate_a_passes(0.0001) is True
    assert gate_a_passes(0.0) is False
    assert gate_a_passes(-0.5) is False


def test_gate_b_passes_active_cadence():
    # 1638 days, active every day -> cadence >> 1/week -> passes
    always_active = np.full(1638, 50.0)
    assert gate_b_passes(always_active) is True

    # 1638 days, active only 1 day total -> cadence << 1/week -> fails
    barely_active = np.zeros(1638)
    barely_active[0] = 50.0
    assert gate_b_passes(barely_active) is False
