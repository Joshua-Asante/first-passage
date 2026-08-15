"""Stable, broker-agnostic utilities shared by active research.

Permutation helpers are re-exported here. Gen-2 DSR lives in the submodule::

    from research_utils.deflated_sharpe import deflated_sharpe, moments_from_returns
"""

from .permutation import (
    label_permutation_test,
    window_permutation_test,
)

__all__ = ["label_permutation_test", "window_permutation_test"]
