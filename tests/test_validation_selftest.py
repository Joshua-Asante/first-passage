"""Tests for lab/validation_selftest.py — synthetic control generators."""

from __future__ import annotations

import numpy as np

from validation_selftest import (
    generate_negative_control,
    generate_positive_control,
)


def test_negative_control_shape_and_label():
    data = generate_negative_control(n_trials=10, n_trades=50, seed=1)
    assert data.n_trials == 10
    assert len(data.trial_returns) == 10
    assert all(len(r) == 50 for r in data.trial_returns)
    assert len(data.entry_times) == 50
    assert "negative" in data.label


def test_positive_control_heterogeneous_drifts():
    data = generate_positive_control(n_trials=20, n_trades=100, edge=0.003, seed=2)
    means = [r.mean() for r in data.trial_returns]
    assert means[-1] > means[0]
    assert 0 <= data.best_index < data.n_trials


def test_best_index_within_family():
    data = generate_negative_control(n_trials=5, n_trades=30, seed=3)
    assert 0 <= data.best_index < data.n_trials
    assert np.array_equal(data.best_returns, data.trial_returns[data.best_index])
