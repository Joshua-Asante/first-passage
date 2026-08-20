"""Pairwise near-duplicate report over aligned bar-return series (ic_similarity.py).

Advisory only -- pairwise_similarity_report never raises on a below-threshold
pair and never filters anything; it only reports. Paired positive/negative
per this repo's own house style.
"""
from __future__ import annotations

import numpy as np
import pytest

from discovery.ic_similarity import pairwise_similarity_report


def test_identical_series_report_perfect_correlation():
    x = [0.01, -0.02, 0.03, 0.0, -0.01, 0.02]
    result = pairwise_similarity_report({"a": x, "b": list(x)})
    assert len(result) == 1
    assert result[0].candidate_a == "a"
    assert result[0].candidate_b == "b"
    assert result[0].correlation == pytest.approx(1.0, abs=1e-9)


def test_unrelated_series_below_threshold_not_reported():
    rng = np.random.default_rng(0)
    a = rng.normal(size=200)
    b = rng.normal(size=200)
    result = pairwise_similarity_report({"a": a, "b": b})
    assert result == []


def test_scaled_series_still_perfectly_correlated():
    """Correlation is scale-invariant -- 2x the return magnitude is still the
    same trade, reported as a near-duplicate."""
    x = [0.01, -0.02, 0.03, 0.0, -0.01, 0.02]
    scaled = [2.0 * v for v in x]
    result = pairwise_similarity_report({"a": x, "b": scaled})
    assert len(result) == 1
    assert result[0].correlation == pytest.approx(1.0, abs=1e-9)


def test_anti_correlated_series_not_reported():
    x = [0.01, -0.02, 0.03, 0.0, -0.01, 0.02]
    inverted = [-v for v in x]
    result = pairwise_similarity_report({"a": x, "b": inverted})
    assert result == []


def test_zero_variance_series_skipped_not_reported():
    """A rule that never fired (all-zero bar_returns) carries no signal to be
    redundant with -- must not report a spurious 1.0/NaN pairing."""
    zeros = [0.0] * 10
    live = [0.01, -0.02, 0.03, 0.0, -0.01, 0.02, 0.01, -0.03, 0.02, 0.0]
    result = pairwise_similarity_report({"dead": zeros, "live": live, "dead2": list(zeros)})
    assert result == []


def test_mismatched_lengths_raise():
    with pytest.raises(ValueError, match="equal-length"):
        pairwise_similarity_report({"a": [0.01, 0.02], "b": [0.01, 0.02, 0.03]})


def test_three_candidates_two_near_duplicates_one_distinct():
    x = [0.01, -0.02, 0.03, 0.0, -0.01, 0.02, 0.015, -0.01]
    rng = np.random.default_rng(1)
    y = rng.normal(size=len(x))
    result = pairwise_similarity_report({"a": x, "b": list(x), "c": y})
    pairs = {(f.candidate_a, f.candidate_b) for f in result}
    assert ("a", "b") in pairs
    assert not any("c" in p for p in pairs)


def test_threshold_is_configurable():
    # A uniform additive shift leaves Pearson correlation exactly 1.0 (shift-
    # invariant); per-element noise is needed to land strictly below 1.0.
    x = [0.01, -0.02, 0.03, 0.0, -0.01, 0.02]
    noise = [0.0003, -0.0002, 0.0004, -0.0003, 0.0002, -0.0004]
    near = [v + n for v, n in zip(x, noise)]
    correlation = pairwise_similarity_report({"a": x, "b": near}, threshold=-1.0)[0].correlation
    assert 0.9 < correlation < 1.0

    strict = pairwise_similarity_report({"a": x, "b": near}, threshold=correlation + 1e-6)
    loose = pairwise_similarity_report({"a": x, "b": near}, threshold=correlation - 1e-6)
    assert strict == []
    assert len(loose) == 1
