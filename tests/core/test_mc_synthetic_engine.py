"""Synthetic MC engine pins — vendor-free replacement for the Pepperstone anchor's
engine-correctness role (ADR 2026-07-22 §2-C / Phase 1 Step 9).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "core"), str(ROOT)]

from mc.modes import ALLOCATIONS, SEEDS, _run_seeds  # noqa: E402
from mc.preflight import firm_kwargs  # noqa: E402
from mc.simulation import (  # noqa: E402
    HISTORICAL_CHALLENGE_BASIS,
    HISTORICAL_CHALLENGE_FIRM_KWARGS,
    run_seed,
)
from tests.fixtures.synthetic_mc_panel import make_synthetic_panel  # noqa: E402

SIMS_PER_SEED = 2000
STRATS = tuple(ALLOCATIONS)

# Empirically locked 2026-07-22 against make_synthetic_panel(seed=20260722).
# Integer counts — no rate tolerance.
SCALE_INFO_PIN = {
    "guardian": {
        "implied_1r": 1100.0,
        "scale": 0.6181818181818182,
        "n_trades": 122,
        "fell_back": False,
    },
    "striker": {
        "implied_1r": 3000.0,
        "scale": 0.4666666666666667,
        "n_trades": 152,
        "fell_back": False,
    },
    "aegis": {
        "implied_1r": 3500.0,
        "scale": 0.8571428571428571,
        "n_trades": 155,
        "fell_back": False,
    },
    "striker_nas100": {
        "implied_1r": 4000.0,
        "scale": 0.185,
        "n_trades": 156,
        "fell_back": False,
    },
}
N_BDAYS_PIN = 1140
N_BLOCKS_PIN = 228
OUTCOME_PINS = {
    42: {
        "pass": 204,
        "bust_daily": 559,
        "bust_static": 192,
        "bust_trailing": 0,
        "bust_inactivity": 1045,
        "horizon_cap": 0,
    },
    123: {
        "pass": 196,
        "bust_daily": 567,
        "bust_static": 187,
        "bust_trailing": 0,
        "bust_inactivity": 1049,
        "horizon_cap": 1,
    },
    2026: {
        "pass": 180,
        "bust_daily": 551,
        "bust_static": 178,
        "bust_trailing": 0,
        "bust_inactivity": 1090,
        "horizon_cap": 1,
    },
}
MEDIAN_DAYS_PIN = {42: 158.0, 123: 148.5, 2026: 153.0}
P99_DD_PIN = {
    42: 0.07944693,
    123: 0.08060006,
    2026: 0.07765301,
}
SCALE_AT_100K_PIN = {
    "guardian": 0.309091,
    "striker": 0.233333,
    "aegis": 0.428571,
    "striker_nas100": 0.0925,
}


@pytest.fixture(scope="module")
def synthetic():
    trades, panel, blocks, scale_info = make_synthetic_panel(ALLOCATIONS)
    return trades, panel, blocks, scale_info


@pytest.fixture(scope="module")
def seed_results(synthetic):
    _, _, blocks, _ = synthetic
    out = {}
    for seed in SEEDS:
        out[seed] = run_seed(
            seed,
            SIMS_PER_SEED,
            blocks,
            0.015,
            0.40,
            strats=STRATS,
            firm_kwargs=dict(HISTORICAL_CHALLENGE_FIRM_KWARGS),
        )
    return out


def test_synthetic_scale_info_pins(synthetic):
    _, _, _, scale_info = synthetic
    for strat, pin in SCALE_INFO_PIN.items():
        got = scale_info[strat]
        assert got["fell_back"] is pin["fell_back"]
        assert got["n_trades"] == pin["n_trades"]
        assert got["implied_1r"] == pytest.approx(pin["implied_1r"])
        assert got["scale"] == pytest.approx(pin["scale"])


def test_synthetic_panel_shape_pins(synthetic):
    _, panel, blocks, _ = synthetic
    assert len(panel) == N_BDAYS_PIN
    assert len(blocks) == N_BLOCKS_PIN


def test_synthetic_outcome_counts_pins(seed_results):
    for seed, pin in OUTCOME_PINS.items():
        assert seed_results[seed]["outcomes"] == pin


def test_synthetic_dd_and_days_pins(seed_results):
    for seed in SEEDS:
        days = seed_results[seed]["days_to_pass"]
        dds = seed_results[seed]["max_dds"]
        assert float(np.median(days)) == pytest.approx(MEDIAN_DAYS_PIN[seed])
        assert float(np.percentile(dds, 99)) == pytest.approx(P99_DD_PIN[seed], abs=1e-8)


def test_synthetic_bucket_partition(seed_results):
    for seed in SEEDS:
        assert sum(seed_results[seed]["outcomes"].values()) == SIMS_PER_SEED


def test_synthetic_serial_parallel_equivalence(synthetic):
    _, _, blocks, _ = synthetic
    try:
        import joblib  # noqa: F401
    except ImportError:
        pytest.skip("joblib not installed")
    serial = _run_seeds(
        blocks, 0.015, 0.40, seeds=SEEDS, parallel=False, strats=STRATS,
        firm_kwargs=dict(HISTORICAL_CHALLENGE_FIRM_KWARGS), sims_per_seed=SIMS_PER_SEED,
    )
    parallel = _run_seeds(
        blocks, 0.015, 0.40, seeds=SEEDS, parallel=True, strats=STRATS,
        firm_kwargs=dict(HISTORICAL_CHALLENGE_FIRM_KWARGS), sims_per_seed=SIMS_PER_SEED,
    )
    assert [r["outcomes"] for r in serial] == [r["outcomes"] for r in parallel]


def test_explicit_fixture_kwargs_equal_default(synthetic):
    _, _, blocks, _ = synthetic
    a = run_seed(42, 500, blocks, 0.015, 0.40, strats=STRATS)
    b = run_seed(
        42, 500, blocks, 0.015, 0.40, strats=STRATS,
        firm_kwargs=dict(HISTORICAL_CHALLENGE_FIRM_KWARGS),
    )
    assert a == b


def test_account_basis_is_live():
    _, _, _, scale_100 = make_synthetic_panel(ALLOCATIONS, account_basis=100_000.0)
    for strat, pin in SCALE_AT_100K_PIN.items():
        assert scale_100[strat]["scale"] == pytest.approx(pin, abs=1e-6)
    # Must differ from the $200K default pin — otherwise the seam is inert.
    _, _, _, scale_200 = make_synthetic_panel(ALLOCATIONS)
    for strat in STRATS:
        assert scale_100[strat]["scale"] != scale_200[strat]["scale"]


def test_named_firm_routes_to_trailing(synthetic):
    _, _, blocks, _ = synthetic
    kw = firm_kwargs("Tradeify_Select_100K", inactivity_off=False)
    result = run_seed(
        42, SIMS_PER_SEED, blocks, 0.015, 0.40, strats=STRATS, firm_kwargs=kw
    )
    assert result["outcomes"]["bust_static"] == 0
    assert result["outcomes"]["bust_trailing"] > 0


def test_preflight_rejects_retired_fxify_key():
    """FXIFY is not in FIRM_RULES; historical kwargs come from the fixture."""
    with pytest.raises(KeyError, match="FXIFY"):
        firm_kwargs("FXIFY")
    assert HISTORICAL_CHALLENGE_BASIS == 200_000
    assert HISTORICAL_CHALLENGE_FIRM_KWARGS["inactivity_limit"] == 60


def test_mode_historical_smoke(synthetic, monkeypatch, capsys):
    """First coverage for mode_historical — synthetic panel, no vendor bytes."""
    from mc import modes

    trades, panel, blocks, scale_info = synthetic
    panel_strats = STRATS

    def _fake_load_all(*args, **kwargs):
        return trades, panel, blocks, scale_info, panel_strats

    monkeypatch.setattr(modes, "_load_all", _fake_load_all)
    modes.mode_historical(0.015, 0.40, False, dict(ALLOCATIONS))
    out = capsys.readouterr().out
    assert "Outcome:" in out
    assert "Day terminated:" in out
