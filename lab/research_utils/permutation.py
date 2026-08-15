"""Broker-agnostic permutation tests for research gates.

The observed label cohort is supplied first for ``label_permutation_test``.
Both helpers return ``(observed_mean, null_distribution, two_sided_p_value)``.
"""

from __future__ import annotations

import numpy as np


def label_permutation_test(
    population_values: np.ndarray,
    n_blocked: int,
    *,
    n_perm: int = 1000,
    seed: int = 42,
) -> tuple[float, np.ndarray, float]:
    """Test an observed leading subset against random labels."""
    population = np.asarray(population_values, dtype=float)
    if n_blocked < 2 or n_blocked >= len(population):
        raise AssertionError(
            "label_permutation_test: "
            f"n_blocked={n_blocked} not in (2, len(pop)={len(population)})"
        )

    observed = float(population[:n_blocked].mean())
    population_mean = population.mean()
    rng = np.random.default_rng(seed)
    null = np.empty(n_perm, dtype=float)
    for index in range(n_perm):
        sample = rng.choice(len(population), size=n_blocked, replace=False)
        null[index] = population[sample].mean()

    p_value = (
        np.abs(null - population_mean) >= abs(observed - population_mean)
    ).mean()
    return observed, null, float(p_value)


def window_permutation_test(
    observed_values: np.ndarray,
    null_pool_values: np.ndarray,
    *,
    n_perm: int = 1000,
    seed: int = 42,
) -> tuple[float, np.ndarray, float]:
    """Test observed windows against samples from a null pool."""
    observed_values = np.asarray(observed_values, dtype=float)
    observed_values = observed_values[~np.isnan(observed_values)]
    null_pool = np.asarray(null_pool_values, dtype=float)
    null_pool = null_pool[~np.isnan(null_pool)]
    if len(observed_values) < 2 or len(null_pool) < len(observed_values):
        raise AssertionError(
            "window_permutation_test: "
            f"|obs|={len(observed_values)}, |pool|={len(null_pool)}"
        )

    observed = float(observed_values.mean())
    null_pool_mean = null_pool.mean()
    rng = np.random.default_rng(seed)
    null = np.empty(n_perm, dtype=float)
    for index in range(n_perm):
        sample = rng.choice(
            len(null_pool), size=len(observed_values), replace=False
        )
        null[index] = null_pool[sample].mean()

    p_value = (
        np.abs(null - null_pool_mean) >= abs(observed - null_pool_mean)
    ).mean()
    return observed, null, float(p_value)
