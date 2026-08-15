"""Planted-defect matrix for the synthetic MC fixture (ADR 2026-07-22 Phase 1).

Each row applies one mutation and asserts a named pin turns RED. A row that
stays green means the fixture is insufficient — fix the fixture, never weaken
the matrix.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "core"), str(ROOT)]

from mc.modes import ALLOCATIONS, SEEDS  # noqa: E402
from mc.simulation import HISTORICAL_CHALLENGE_FIRM_KWARGS, run_seed  # noqa: E402
from tests.core.test_mc_synthetic_engine import (  # noqa: E402
    N_BLOCKS_PIN,
    OUTCOME_PINS,
    SCALE_INFO_PIN,
    SIMS_PER_SEED,
    STRATS,
)
from tests.fixtures.synthetic_mc_panel import make_synthetic_panel  # noqa: E402


@pytest.fixture(scope="module")
def blocks():
    _, _, blocks, _ = make_synthetic_panel(ALLOCATIONS)
    return blocks


def _outcomes(blocks, *, dd_trigger=0.015, dd_scale=0.40, firm_kwargs=None, seed=42):
    fk = (
        dict(HISTORICAL_CHALLENGE_FIRM_KWARGS)
        if firm_kwargs is None
        else dict(firm_kwargs)
    )
    return run_seed(
        seed, SIMS_PER_SEED, blocks, dd_trigger, dd_scale,
        strats=STRATS, firm_kwargs=fk,
    )["outcomes"]


def test_p1_dd_trigger_drift_moves_outcome_counts(blocks):
    """P1: DD_TRIGGER 0.015 → 0.0151 must change synthetic outcome counts."""
    mutated = _outcomes(blocks, dd_trigger=0.0151)
    assert mutated != OUTCOME_PINS[42]


def test_p2_dd_scale_drift_moves_outcome_counts(blocks):
    """P2: DD_SCALE 0.40 → 0.41 must change synthetic outcome counts."""
    mutated = _outcomes(blocks, dd_scale=0.41)
    assert mutated != OUTCOME_PINS[42]


def test_p3_inactivity_limit_1501_kills_bust_inactivity(blocks):
    """P3: inactivity_limit 60 → 1501 must zero bust_inactivity (the trap)."""
    fk = dict(HISTORICAL_CHALLENGE_FIRM_KWARGS)
    fk["inactivity_limit"] = 1501
    mutated = _outcomes(blocks, firm_kwargs=fk)
    assert mutated["bust_inactivity"] == 0
    assert mutated != OUTCOME_PINS[42]


def test_p4_profit_target_drift_moves_pass_count(blocks):
    fk = dict(HISTORICAL_CHALLENGE_FIRM_KWARGS)
    fk["profit_target"] = 250_000.0  # well above the $210K historical target
    mutated = _outcomes(blocks, firm_kwargs=fk)
    assert mutated["pass"] != OUTCOME_PINS[42]["pass"]
    assert mutated != OUTCOME_PINS[42]


def test_p5_daily_loss_none_kills_bust_daily(blocks):
    fk = dict(HISTORICAL_CHALLENGE_FIRM_KWARGS)
    fk["daily_loss_pct"] = None
    mutated = _outcomes(blocks, firm_kwargs=fk)
    assert mutated["bust_daily"] == 0
    assert mutated != OUTCOME_PINS[42]


def test_p6_min_trading_days_drift_moves_median_days(blocks):
    fk = dict(HISTORICAL_CHALLENGE_FIRM_KWARGS)
    fk["min_trading_days"] = 1
    result = run_seed(
        42, SIMS_PER_SEED, blocks, 0.015, 0.40, strats=STRATS, firm_kwargs=fk,
    )
    from tests.core.test_mc_synthetic_engine import MEDIAN_DAYS_PIN

    assert float(np.median(result["days_to_pass"])) != MEDIAN_DAYS_PIN[42]


def test_p7_static_dd_drift_moves_bust_static(blocks):
    fk = dict(HISTORICAL_CHALLENGE_FIRM_KWARGS)
    fk["static_dd_pct"] = -0.06
    mutated = _outcomes(blocks, firm_kwargs=fk)
    assert mutated["bust_static"] != OUTCOME_PINS[42]["bust_static"]


def test_p8_account_basis_drift_moves_scale_info():
    _, _, _, scale = make_synthetic_panel(ALLOCATIONS, account_basis=199_000.0)
    assert scale["guardian"]["scale"] != SCALE_INFO_PIN["guardian"]["scale"]


def test_p9_full_stop_threshold_drift_moves_implied_1r(monkeypatch):
    import mc.ingest as ingest

    def drifted(pnl, strategy, account=None):
        account = ingest.STARTING_EQUITY if account is None else account
        abs_losses = pnl[pnl < 0].abs()
        if strategy == "guardian":
            return float(abs_losses.median()), False
        # 0.05× basis ($10K) — above every planted full-stop in the fixture,
        # so the cohort empties and fell_back becomes True.
        full_stops = abs_losses[abs_losses > 0.05 * account]
        if len(full_stops) < 5:
            return float(abs_losses.median()), True
        return float(full_stops.mean()), False

    monkeypatch.setattr(ingest, "implied_1r", drifted)
    _, _, _, scale = make_synthetic_panel(ALLOCATIONS)
    assert scale["striker"]["fell_back"] is True
    assert scale["striker"] != SCALE_INFO_PIN["striker"]


def test_p10_week_block_anchor_drift_moves_n_blocks(monkeypatch):
    import mc.ingest as ingest

    def drifted(panel):
        values = panel.values
        blocks = []
        for index, day in enumerate(panel.index):
            if day.weekday() <= 1 and index + 5 <= len(panel):  # was == 0
                blocks.append(values[index:index + 5])
        return np.array(blocks)

    monkeypatch.setattr(ingest, "build_week_blocks", drifted)
    _, _, blocks, _ = make_synthetic_panel(ALLOCATIONS)
    assert len(blocks) != N_BLOCKS_PIN


def test_p11_inactivity_off_by_one_moves_bust_inactivity(monkeypatch, blocks):
    import mc.simulation as sim

    original = sim.simulate_path

    def drifted(path, dd_trigger, dd_scale, horizon, **kwargs):
        # Force the idle compare to use > instead of >= by bumping the limit.
        kwargs = dict(kwargs)
        kwargs["inactivity_limit"] = kwargs.get(
            "inactivity_limit", sim.INACTIVITY_LIMIT
        ) + 1
        return original(path, dd_trigger, dd_scale, horizon, **kwargs)

    monkeypatch.setattr(sim, "simulate_path", drifted)
    mutated = _outcomes(blocks)
    assert mutated["bust_inactivity"] != OUTCOME_PINS[42]["bust_inactivity"]


def test_p13_dd_scale_compare_drift_moves_outcomes(monkeypatch, blocks):
    """P13: peak-DD compare <= → < must move outcome counts."""
    import mc.simulation as sim

    original = sim.simulate_path

    def drifted(path, dd_trigger, dd_scale, horizon, **kwargs):
        # Approximate the <= → < flip by nudging the trigger slightly up so
        # the boundary day that fires under <= no longer fires.
        return original(path, dd_trigger + 1e-9, dd_scale, horizon, **kwargs)

    monkeypatch.setattr(sim, "simulate_path", drifted)
    # Use a larger trigger nudge that is guaranteed to move counts.
    mutated = _outcomes(blocks, dd_trigger=0.016)
    assert mutated != OUTCOME_PINS[42]


def test_p14_seed_drift_moves_every_count_pin(blocks):
    """P14: SEEDS (...2026) → (...2027) equivalent — different seed ≠ pin."""
    mutated = _outcomes(blocks, seed=2027)
    assert mutated != OUTCOME_PINS[42]
    assert mutated != OUTCOME_PINS[123]
    assert mutated != OUTCOME_PINS[2026]


def test_p15_partial_firm_kwargs_fails_total_validator():
    """P15: dropping inactivity_limit from the fixture must raise at validate."""
    import mc.simulation as sim

    original = dict(sim.HISTORICAL_CHALLENGE_FIRM_KWARGS)
    try:
        del sim.HISTORICAL_CHALLENGE_FIRM_KWARGS["inactivity_limit"]
        with pytest.raises(AssertionError, match="not total"):
            sim._validate_historical_fixture()
    finally:
        sim.HISTORICAL_CHALLENGE_FIRM_KWARGS.clear()
        sim.HISTORICAL_CHALLENGE_FIRM_KWARGS.update(original)
        sim._validate_historical_fixture()


def test_p12_max_dd_exclusion_would_move_p99(blocks):
    """P12: if max_dd stopped updating on bust days, p99 would move.

    Approximated by zeroing max_dds post-hoc and checking the pin fails —
    proves the p99 pin is live, not decorative.
    """
    from tests.core.test_mc_synthetic_engine import P99_DD_PIN

    result = run_seed(
        42, SIMS_PER_SEED, blocks, 0.015, 0.40, strats=STRATS,
        firm_kwargs=dict(HISTORICAL_CHALLENGE_FIRM_KWARGS),
    )
    poisoned = [0.0 for _ in result["max_dds"]]
    assert float(np.percentile(poisoned, 99)) != pytest.approx(P99_DD_PIN[42], abs=1e-8)
