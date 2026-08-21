"""Tests for lab/research_utils/breadth.py (discovery-campaign Stage 8: incremental
5th-column N_eff). Synthetic-mechanics tests run unconditionally (no vendor data).
Design: docs/superpowers/specs/2026-07-12-track-c-incremental-breadth-design.md
"""
from __future__ import annotations

import numpy as np
import pytest

import pandas as pd

from research_utils.breadth import (
    MIN_OVERLAP_BLOCKS,
    _align_candidate,
    baseline_panel_available,
    effective_number_of_bets,
    load_baseline_panel,
    participation_ratio,
)


def test_baseline_panel_available_false_when_registry_empty():
    """Pepperstone is unregistered after substrate Phase 3 — that panel does not load."""
    assert baseline_panel_available("pepperstone") is False


def test_load_baseline_panel_raises_when_registry_empty():
    with pytest.raises(KeyError, match="not registered"):
        load_baseline_panel("pepperstone")


def test_participation_ratio_identity_matrix_equals_n():
    """Uncorrelated (identity) 4x4 -> eigenvalues all 1 -> PR = 4^2/4 = 4 exactly."""
    assert participation_ratio(np.eye(4)) == pytest.approx(4.0, abs=1e-9)


def test_participation_ratio_rank_one_matrix_equals_one():
    """Fully-degenerate (all-ones) 4x4 -> eigenvalues [4,0,0,0] -> PR = 16/16 = 1."""
    assert participation_ratio(np.ones((4, 4))) == pytest.approx(1.0, abs=1e-9)


def test_participation_ratio_known_mixed_eigenvalues():
    """Diagonal matrix with eigenvalues [2,1,1,0] -> PR = 16/6 = 2.6667."""
    matrix = np.diag([2.0, 1.0, 1.0, 0.0])
    assert participation_ratio(matrix) == pytest.approx(16.0 / 6.0, abs=1e-9)


def test_effective_number_of_bets_identity_matrix_equals_n():
    """Uncorrelated (identity) 4x4 -> maximum entropy -> ENB = n = 4 exactly."""
    assert effective_number_of_bets(np.eye(4)) == pytest.approx(4.0, abs=1e-9)


def test_effective_number_of_bets_rank_one_matrix_equals_one():
    """Fully-degenerate (all-ones) 4x4 -> one dominant eigenvalue -> ENB ~= 1."""
    assert effective_number_of_bets(np.ones((4, 4))) == pytest.approx(1.0, abs=1e-6)


def _synthetic_panel(n_weeks: int, n_strats: int = 4, seed: int = 1) -> pd.DataFrame:
    """n_weeks Mon-anchored 5-bday blocks of iid noise, n_strats columns.
    2022-01-03 is a Monday, so this is byte-clean for build_week_blocks."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2022-01-03", periods=n_weeks * 5)
    cols = [f"leg{i}" for i in range(n_strats)]
    data = rng.normal(0, 1.0, size=(len(dates), n_strats))
    return pd.DataFrame(data, index=dates, columns=cols)


def test_align_candidate_trims_to_intersection_window():
    panel = _synthetic_panel(n_weeks=52)
    candidate = pd.Series(
        np.ones(50),
        index=pd.bdate_range("2022-06-01", periods=50),
        name="candidate_a",
    )
    trimmed, window = _align_candidate(panel, candidate)
    assert window["start"] == "2022-06-01"
    assert window["end"] == str(candidate.index.max().date())
    assert trimmed.index.min() == candidate.index.min()
    assert trimmed.index.max() == candidate.index.max()
    assert "candidate_a" in trimmed.columns
    assert window["n_bdays"] == len(trimmed)


def test_align_candidate_no_overlap_raises():
    panel = _synthetic_panel(n_weeks=10)  # ends ~2022-03-11
    candidate = pd.Series(
        np.ones(10),
        index=pd.bdate_range("2023-01-02", periods=10),
        name="candidate_b",
    )
    with pytest.raises(ValueError, match="does not overlap"):
        _align_candidate(panel, candidate)


def test_align_candidate_name_collision_raises():
    panel = _synthetic_panel(n_weeks=10)
    candidate = pd.Series(
        np.ones(10),
        index=panel.index[:10],
        name="leg0",  # collides with an existing panel column
    )
    with pytest.raises(ValueError, match="collides"):
        _align_candidate(panel, candidate)


def test_align_candidate_too_short_overlap_raises():
    """A candidate whose overlap with the panel spans fewer than 2 weekly
    blocks cannot produce a meaningful 2-point-minimum correlation/covariance
    estimate downstream in compute_breadth -> must raise a clear ValueError
    here rather than an opaque numpy AxisError/LinAlgError deep in
    _weekly/participation_ratio."""
    panel = _synthetic_panel(n_weeks=52)
    candidate = pd.Series(
        np.ones(4),
        index=pd.bdate_range("2022-06-01", periods=4),
        name="too_short",
    )
    with pytest.raises(ValueError, match="too short"):
        _align_candidate(panel, candidate)


def test_align_candidate_thin_overlap_flag():
    panel = _synthetic_panel(n_weeks=52)
    short_candidate = pd.Series(
        np.ones(10),
        index=pd.bdate_range("2022-01-03", periods=10),
        name="short_candidate",
    )
    _, window = _align_candidate(panel, short_candidate)
    assert window["n_blocks"] < MIN_OVERLAP_BLOCKS
    assert window["thin_overlap"] is True


from research_utils.breadth import compute_breadth


def test_compute_breadth_uncorrelated_synthetic_panel_neff_near_n():
    """4 independent columns -> both PR(corr) and PR(cov) should land close to
    4 (allowing finite-sample noise) — the same "near-full-breadth" shape as
    the real anchor, on data with no hidden calibration."""
    panel = _synthetic_panel(n_weeks=200, n_strats=4, seed=7)
    result = compute_breadth(panel)
    assert result["n_bdays"] == len(panel)
    assert result["n_blocks"] == 200
    assert result["n_eff_dependence"] == pytest.approx(4.0, abs=0.5)
    assert result["n_eff_risk"] == pytest.approx(4.0, abs=0.5)


def test_compute_breadth_duplicate_leg_candidate_adds_near_zero_breadth():
    """A candidate that's an exact copy of an existing leg is perfectly
    correlated with it -> adds well under a full unit of independent breadth
    (contrast with the independent-candidate test below, which adds ~1)."""
    panel = _synthetic_panel(n_weeks=200, n_strats=4, seed=11)
    duplicate = panel["leg0"].rename("duplicate_of_leg0")
    result = compute_breadth(panel, candidate=duplicate)

    assert result["candidate_vs_leg_corr"]["leg0"] == pytest.approx(1.0, abs=1e-9)
    assert result["n_eff_dependence_delta"] < 0.6


def test_compute_breadth_independent_candidate_adds_near_one_breadth():
    """A candidate drawn independently of the synthetic panel adds close to
    one full unit of independent breadth (delta near +1)."""
    panel = _synthetic_panel(n_weeks=200, n_strats=4, seed=13)
    rng = np.random.default_rng(99)
    independent = pd.Series(
        rng.normal(0, 1.0, size=len(panel)),
        index=panel.index,
        name="independent_candidate",
    )
    result = compute_breadth(panel, candidate=independent)

    for leg, corr in result["candidate_vs_leg_corr"].items():
        assert abs(corr) < 0.3, f"synthetic independence violated for {leg}: corr={corr}"
    assert result["n_eff_dependence_delta"] == pytest.approx(1.0, abs=0.5)


def test_compute_breadth_candidate_vs_composite_corr_positive():
    """candidate = leg1 (literally one of the 4 summands) -> must correlate
    positively and non-trivially with the sum of all 4 legs."""
    panel = _synthetic_panel(n_weeks=200, n_strats=4, seed=17)
    candidate = panel["leg1"].rename("candidate_c")
    result = compute_breadth(panel, candidate=candidate)
    assert result["candidate_vs_composite_corr"] > 0.2


import io
from contextlib import redirect_stdout

from research_utils.breadth import _load_candidates, _self_test


def test_self_test_skips_when_panel_unregistered():
    buf = io.StringIO()
    with redirect_stdout(buf):
        exit_code = _self_test("pepperstone")
    assert exit_code == 2
    assert "SKIP" in buf.getvalue()


def test_load_candidates_excludes_benchmark_column(tmp_path):
    csv_path = tmp_path / "candidates.csv"
    df = pd.DataFrame(
        {
            "candidate_x": [1.0, 2.0, 3.0],
            "benchmark": [0.1, 0.1, 0.1],
        },
        index=pd.bdate_range("2024-01-01", periods=3),
    )
    df.index.name = "date"
    df.to_csv(csv_path)

    candidates = _load_candidates(csv_path, benchmark_col="benchmark")
    assert list(candidates.keys()) == ["candidate_x"]
    assert candidates["candidate_x"].name == "candidate_x"
    assert len(candidates["candidate_x"]) == 3


def test_load_candidates_no_benchmark_col_keeps_all_columns(tmp_path):
    csv_path = tmp_path / "candidates_no_bench.csv"
    df = pd.DataFrame(
        {"candidate_x": [1.0, 2.0], "candidate_y": [3.0, 4.0]},
        index=pd.bdate_range("2024-01-01", periods=2),
    )
    df.index.name = "date"
    df.to_csv(csv_path)

    candidates = _load_candidates(csv_path, benchmark_col=None)
    assert set(candidates.keys()) == {"candidate_x", "candidate_y"}
