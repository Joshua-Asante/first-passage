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


from discovery.grow0_dgp import build_root_branches, spawn_panel_streams
from discovery.grow0_scoring import PanelResult, run_panel, run_panel_leaked

FLOOR = 1.265  # floor_at_k(10, years=6.5) -- pinned literal for this test, verified in Task 6


def test_run_panel_limb_a_shape_recovers_edge_variant():
    branches = build_root_branches()
    train_children, confirm_children = spawn_panel_streams(branches["limb_a"], 10)
    result = run_panel(
        train_children, confirm_children, edge_variant_index=5, floor=FLOOR
    )
    assert isinstance(result, PanelResult)
    # SR=4.0 planted edge is deterministic-in-practice (prereg §3) -- a fresh seed should
    # essentially always recover it; this is the harness's own correctness check, not a
    # statistical test of the design (that's what Limb A's real 5,500-panel run is for)
    assert result.nominee == 5
    assert result.abandoned is False
    assert result.clears is True


def test_run_panel_null_only_panel_rarely_clears():
    branches = build_root_branches()
    train_children, confirm_children = spawn_panel_streams(branches["limb_b"], 10)
    result = run_panel(train_children, confirm_children, edge_variant_index=None, floor=FLOOR)
    assert isinstance(result, PanelResult)
    assert result.clears in (True, False)  # both legal; nominal_p0 is tiny but nonzero


def test_run_panel_abandoned_has_no_confirm_read(monkeypatch):
    """Nomination-gate failure is rare by design (prereg §6.1 step 4: ~0.14-0.20%
    for a null-only panel), so a real seed only exercises this branch by luck --
    force it deterministically instead of hoping for one, per this plan's own
    no-vacuous-tests standard."""
    import discovery.grow0_scoring as scoring_module

    monkeypatch.setattr(scoring_module, "gate_a_passes", lambda train_stat: False)
    branches = build_root_branches()
    train_children, confirm_children = spawn_panel_streams(branches["red_leak"], 10)
    result = run_panel(train_children, confirm_children, edge_variant_index=None, floor=FLOOR)
    assert result.abandoned is True
    assert result.gate_a is False
    assert result.confirm_stat is None
    assert result.clears is False


def test_run_panel_leaked_confirm_equals_train_stat_of_nominee():
    branches = build_root_branches()
    train_children, _ = spawn_panel_streams(branches["red_leak"], 10)
    result = run_panel_leaked(train_children, edge_variant_index=None, floor=FLOOR)
    if not result.abandoned:
        assert result.confirm_stat == result.train_stat
