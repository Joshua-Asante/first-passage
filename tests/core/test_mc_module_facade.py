"""Characterization tests for the portfolio-MC compatibility facade."""

from __future__ import annotations

import inspect

import numpy as np
import pandas as pd
import pytest

import portfolio_mc


def test_focused_mc_modules_own_facade_exports():
    from mc import ingest, modes, simulation

    assert portfolio_mc.load_trades is ingest.load_trades
    assert portfolio_mc.build_daily_panel is ingest.build_daily_panel
    assert portfolio_mc.build_week_blocks is ingest.build_week_blocks
    assert portfolio_mc._simulate_path is simulation.simulate_path
    assert portfolio_mc.run_seed is simulation.run_seed
    assert portfolio_mc.report_default is modes.report_default


def test_simulation_facade_preserves_signature_and_small_path_semantics():
    from mc.simulation import simulate_path

    assert inspect.signature(portfolio_mc._simulate_path) == inspect.signature(simulate_path)

    path = np.array([[1_000.0, 0.0], [1_000.0, 0.0]])
    expected = ("horizon_cap", 2, 0.0, None)
    assert simulate_path(path, 0.015, 0.40, 2) == expected
    assert portfolio_mc._simulate_path(path, 0.015, 0.40, 2) == expected


def test_seeded_run_seed_characterization_is_stable():
    from mc.simulation import run_seed

    blocks = np.array(
        [[[1_000.0, -500.0], [0.0, 0.0], [200.0, 0.0], [-100.0, 0.0], [0.0, 0.0]]]
    )
    result = run_seed(
        7, 3, blocks, 0.015, 0.40, horizon=10, strats=("a", "b")
    )

    assert result["outcomes"] == {
        "pass": 0,
        "bust_daily": 0,
        "bust_static": 0,
        "bust_trailing": 0,
        "bust_inactivity": 0,
        "horizon_cap": 3,
    }
    assert result["days_to_pass"] == []
    assert result["max_dds"] == pytest.approx([0.0004982561036372695] * 3)
    assert result["bust_attribution"] == {"a": 0, "b": 0}
    assert portfolio_mc.run_seed is run_seed


def test_run_seeds_forwards_facade_sims_per_seed(monkeypatch):
    from mc import modes

    delegated = {}

    def record_run_seeds(*args, **kwargs):
        delegated.update(kwargs)
        return ["delegated"]

    monkeypatch.setattr(portfolio_mc, "SIMS_PER_SEED", 50)
    monkeypatch.setattr(modes, "_run_seeds", record_run_seeds)

    result = portfolio_mc._run_seeds(
        np.zeros((1, 5, 1)),
        0.015,
        0.40,
        seeds=(7, 11),
        strats=("guardian",),
    )

    assert result == ["delegated"]
    assert delegated["sims_per_seed"] == 50


def test_run_seeds_does_not_contaminate_concurrent_direct_call(monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event

    from mc import modes

    facade_entered = Event()
    release_facade = Event()
    calls = {}

    def record_run_seed(seed, n_sims, blocks, dd_trigger, dd_scale, **kwargs):
        calls[seed] = n_sims
        if seed == 7:
            facade_entered.set()
            assert release_facade.wait(timeout=5)
        return {"seed": seed}

    implementation_current = 75
    monkeypatch.setattr(modes, "SIMS_PER_SEED", implementation_current)
    monkeypatch.setattr(portfolio_mc, "SIMS_PER_SEED", 50)
    monkeypatch.setattr(modes, "run_seed", record_run_seed)

    with ThreadPoolExecutor(max_workers=2) as executor:
        facade_future = executor.submit(
            portfolio_mc._run_seeds,
            np.zeros((1, 5, 1)),
            0.015,
            0.40,
            (7,),
        )
        assert facade_entered.wait(timeout=5)
        direct_future = executor.submit(
            modes._run_seeds,
            np.zeros((1, 5, 1)),
            0.015,
            0.40,
            (11,),
        )
        direct_future.result(timeout=5)
        release_facade.set()
        facade_future.result(timeout=5)

    assert calls == {7: 50, 11: implementation_current}
    assert modes.SIMS_PER_SEED == implementation_current


def test_run_seeds_delegated_exception_leaves_implementation_global_stable(monkeypatch):
    from mc import modes

    implementation_default = modes.SIMS_PER_SEED

    def raise_delegated(*args, **kwargs):
        assert modes.SIMS_PER_SEED == implementation_default
        raise RuntimeError("delegated failure")

    monkeypatch.setattr(portfolio_mc, "SIMS_PER_SEED", 50)
    monkeypatch.setattr(modes, "_run_seeds", raise_delegated)

    with pytest.raises(RuntimeError, match="delegated failure"):
        portfolio_mc._run_seeds(np.zeros((1, 5, 1)), 0.015, 0.40)

    assert modes.SIMS_PER_SEED == implementation_default


def test_ingestion_builds_expected_business_day_panel():
    from mc.ingest import build_daily_panel, build_week_blocks

    trades = {
        "guardian": pd.DataFrame(
            {
                "exit_date": pd.to_datetime(["2026-07-06", "2026-07-08"]),
                "pnl": [-100.0, 200.0],
            }
        )
    }
    panel, scale_info = build_daily_panel(
        trades,
        {"guardian": 0.0034},
        fixed_1r_reference={"guardian": 100.0},
    )

    assert panel.index.tolist() == list(pd.bdate_range("2026-07-06", "2026-07-08"))
    assert panel["guardian"].tolist() == [-680.0, 0.0, 1_360.0]
    assert scale_info["guardian"] == {
        "implied_1r": 100.0,
        "scale": 6.8,
        "n_trades": 2,
        "fell_back": False,
    }
    assert build_week_blocks(panel).shape == (0,)


def test_default_report_bytes_are_stable(capsys):
    from mc.modes import report_default

    result = {
        "seeds_results": [{}, {}],
        "panel_strats": ("guardian",),
        "pass_rate": 0.75,
        "pass_sigma": 0.01,
        "bust_rate": 0.25,
        "bust_sigma": 0.01,
        "bust_daily_rate": 0.10,
        "bust_static_rate": 0.15,
        "bust_inactivity_rate": 0.0,
        "horizon_cap_rate": 0.0,
        "median_days_to_pass": 12,
        "p50_dd": 0.01,
        "p95_dd": 0.02,
        "p99_dd": 0.03,
        "bust_attribution": {"guardian": 2},
        "apply_swap": False,
        "fixed_1r_reference": None,
    }

    report_default(result, 0.015, 0.40, {"guardian": 0.0034}, False)

    output = capsys.readouterr().out
    assert output.startswith(
        "=== Portfolio MC ===\n"
        "Config: DD 1.5% / 0.4× (single-tier)\n"
        "Allocations: G 0.34%\n"
    )
    assert "Pass:               75.00% (sigma 1.00%)\n" in output
    assert output.endswith("  guardian       100.0%\n")
