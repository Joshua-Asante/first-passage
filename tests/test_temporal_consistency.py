"""Tests for the Stage-6 temporal-consistency battery
lab/research_utils/temporal_consistency.py.

Research-venv-only (imports arch for the CUSUM null). `importorskip` so tests
SKIP cleanly in the ops venv / CI and RUN in .venv-research — same posture as
tests/test_universe_gate.py. Planted defects must each FAIL their sub-test;
a clean edge must PASS all four (handoff §4 falsifier set).
"""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pytest

pytest.importorskip("arch")

# Canonical lab modules (lab is on pytest pythonpath).
import research_utils.temporal_consistency as tc  # noqa: E402
import research_utils.universe_gate as ug  # noqa: E402
from research_utils.prereg_paths import DISC_CAMP_0_PREREG  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parent.parent
_PREREG = DISC_CAMP_0_PREREG
_TC_PATH = _REPO_ROOT / "lab" / "research_utils" / "temporal_consistency.py"


def _daily_index(start_year: int, n_years: int, per_year: int = 20):
    """Build ISO timestamp strings spanning n_years calendar years (evenly spaced)."""
    stamps = []
    for y in range(start_year, start_year + n_years):
        for i in range(per_year):
            d = date(y, 1, 1) + timedelta(days=int(i * 365 / per_year))
            stamps.append(d.isoformat())
    return stamps


def _thresholds():
    return ug.load_thresholds_from_prereg(_PREREG)


# ---------------------------------------------------------------- 6a sign consistency

def test_6a_consistent_series_passes():
    """Known-consistent edge (positive every year) PASSES 6a."""
    thr = _thresholds()
    n_years = thr.consistency_years
    per_year = 20
    edge = np.full(n_years * per_year, 0.01)
    stamps = _daily_index(2019, n_years, per_year)
    result = tc.sign_consistency(edge, stamps, thr)
    assert result["verdict"] == "PASS"
    assert result["positive_years"] == n_years


def test_6a_four_of_seven_fails():
    """Series positive in only 4/7 years FAILS 6a (DISC-CAMP-0 bar is 5/7)."""
    thr = _thresholds()
    n_years = thr.consistency_years
    per_year = 20
    chunks = []
    for y in range(n_years):
        sign = 0.01 if y < 4 else -0.01
        chunks.append(np.full(per_year, sign))
    edge = np.concatenate(chunks)
    stamps = _daily_index(2019, n_years, per_year)
    result = tc.sign_consistency(edge, stamps, thr)
    assert result["verdict"] == "FAIL"
    assert result["positive_years"] == 4


# ---------------------------------------------------------------- 6b drop-top-year

def test_6b_concentrated_edge_fails():
    """Single-year-concentrated edge (one huge year, flat rest) FAILS 6b."""
    n_years, per_year = 7, 20
    chunks = []
    for y in range(n_years):
        if y == 3:
            chunks.append(np.full(per_year, 1.0))
        else:
            chunks.append(np.zeros(per_year))
    edge = np.concatenate(chunks)
    stamps = _daily_index(2019, n_years, per_year)
    result = tc.drop_top_year(edge, stamps)
    assert result["verdict"] == "FAIL"
    assert result["remaining_edge"] <= 0


def test_6b_distributed_edge_passes():
    """Broadly-distributed positive edge PASSES 6b (stays net-positive after drop)."""
    n_years, per_year = 7, 20
    edge = np.full(n_years * per_year, 0.01)
    stamps = _daily_index(2019, n_years, per_year)
    result = tc.drop_top_year(edge, stamps)
    assert result["verdict"] == "PASS"
    assert result["remaining_edge"] > 0


# ---------------------------------------------------------------- 6c regime-slice

def test_6c_no_labels_skipped():
    """No labels supplied → SKIPPED (not silently PASS)."""
    edge = np.full(100, 0.01)
    result = tc.regime_slice_survival(edge, labels=None)
    assert result["verdict"] == "SKIPPED"


def test_6c_regime_confined_fails():
    """Edge positive in one slice, negative in others FAILS 6c."""
    edge = np.concatenate([
        np.full(30, 0.05),
        np.full(30, -0.02),
        np.full(30, -0.02),
    ])
    labels = np.array(["A"] * 30 + ["B"] * 30 + ["C"] * 30)
    result = tc.regime_slice_survival(edge, labels=labels)
    assert result["verdict"] == "FAIL"


def test_6c_regime_robust_passes():
    """Edge positive across all slices PASSES 6c."""
    n = 90
    edge = np.full(n, 0.02)
    labels = np.array(["A"] * 30 + ["B"] * 30 + ["C"] * 30)
    result = tc.regime_slice_survival(edge, labels=labels)
    assert result["verdict"] == "PASS"
    assert all(v > 0 for v in result["edge_per_slice"].values())


# ---------------------------------------------------------------- 6d CUSUM

def test_6d_stationary_edge_does_not_trip():
    """Stationary positive edge does NOT trip the CUSUM."""
    rng = np.random.default_rng(11)
    edge = rng.normal(0.01, 0.005, size=400)
    result = tc.edge_cusum(edge, seed=11, reps=200)
    assert result["verdict"] == "PASS"
    assert "block_size" in result["cusum_spec"]
    assert "null_quantile" in result["cusum_spec"]


def test_6d_decaying_edge_trips():
    """Linearly-decaying edge (early+/late− regimes) TRIPS the CUSUM."""
    rng = np.random.default_rng(22)
    edge = tc._planted_decaying_edge(400, rng)
    result = tc.edge_cusum(edge, seed=22, reps=200)
    assert result["verdict"] == "FAIL"
    assert result["observed_stat"] > result["cusum_spec"]["null_quantile"]


# ---------------------------------------------------------------- battery + self-test

def test_battery_clean_passes_all():
    """Clean consistent+robust series → overall PASS; all four sub-tests clear."""
    thr = _thresholds()
    n_years, per_year = thr.consistency_years, 20
    edge = np.full(n_years * per_year, 0.02)
    stamps = _daily_index(2019, n_years, per_year)
    labels = np.array(["A", "B"] * (len(edge) // 2))
    if len(labels) < len(edge):
        labels = np.append(labels, "A")
    result = tc.run_temporal_battery(
        edge, stamps, thr, labels=labels, seed=3, reps=200,
    )
    assert result["overall"] == "PASS"
    assert result["subtests"]["6a"]["verdict"] == "PASS"
    assert result["subtests"]["6b"]["verdict"] == "PASS"
    assert result["subtests"]["6c"]["verdict"] == "PASS"
    assert result["subtests"]["6d"]["verdict"] == "PASS"
    assert "cusum_spec" in result


def test_self_test_discriminates():
    """Self-test: clean edge PASSES; each planted defect FAILS its sub-test."""
    thr = _thresholds()
    out = tc.self_test(thresholds=thr, seed=5, reps=200)
    assert out["clean"]["overall"] == "PASS"
    assert out["concentrated"]["subtests"]["6b"]["verdict"] == "FAIL"
    assert out["decaying"]["subtests"]["6d"]["verdict"] == "FAIL"
    assert out["regime_confined"]["subtests"]["6c"]["verdict"] == "FAIL"
    assert out["four_of_seven"]["subtests"]["6a"]["verdict"] == "FAIL"


def test_thresholds_reused_not_hardcoded():
    """Battery reads consistency thresholds via universe_gate, never hardcodes 5/7."""
    thr = _thresholds()
    assert thr.consistency_min == 5
    assert thr.consistency_years == 7
    assert hasattr(tc, "load_thresholds_from_prereg")
    src = _TC_PATH.read_text(encoding="utf-8")
    assert "load_thresholds_from_prereg" in src
    assert "acf_block_size" in src
    assert "from arch" in src or "import arch" in src
    assert "research_utils" in src
