# OANDA Stage-1 investigation frozen 2026-06-24
# (docs/adr/2026-06-24-oanda-retirement.md).
"""Compatibility exports for frozen Stage-1 research.

The broker-agnostic implementation moved to ``research_utils.permutation``.
Frozen OANDA scripts retain this import path so their historical reproducer
commands do not need a broad rewrite.
"""

from research_utils.permutation import (
    label_permutation_test,
    window_permutation_test,
)

__all__ = ["label_permutation_test", "window_permutation_test"]
