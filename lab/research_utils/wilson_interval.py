"""95% Wilson score confidence interval for a binomial proportion.

Used by mechanism_prior.py so every reported rate carries an N-aware
interval instead of a bare percentage (this repo's Rule 1 -- small-cell
variance prior).
"""

from __future__ import annotations

import math

Z_95 = 1.959963984540054  # two-sided 95% normal quantile


def wilson_interval(successes: int, n: int, z: float = Z_95) -> tuple[float, float]:
    """Return (lower, upper) Wilson score bounds for successes/n.

    Raises ValueError if n <= 0 or successes is out of [0, n].
    """
    if n <= 0:
        raise ValueError("n must be positive")
    if not (0 <= successes <= n):
        raise ValueError("successes must be within [0, n]")

    p_hat = successes / n
    denom = 1 + z ** 2 / n
    center = p_hat + z ** 2 / (2 * n)
    margin = z * math.sqrt((p_hat * (1 - p_hat) + z ** 2 / (4 * n)) / n)
    lower = (center - margin) / denom
    upper = (center + margin) / denom
    return max(0.0, lower), min(1.0, upper)
