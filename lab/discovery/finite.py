"""finite.py — shared finite-number guard for discovery admission inputs.

NaN compares False against every threshold, so a ``value < floor`` refusal
silently passes a NaN and the admission reads ADMIT (issue #1145). Callers
validate supplied numeric inputs here before scoring them.

Numeric strings stay accepted (``float("0.5")``), matching the existing
``float(x)`` intake; ``"NaN"``, ``"inf"``, ``1e999`` and ints beyond a C
double's range are refused. Imports nothing internal, so admission_schema,
deep_lane_admission and register_search can all use it without a cycle.
"""
from __future__ import annotations

import math
from typing import Any


def require_finite(value: Any, name: str) -> float:
    """Return ``float(value)``; raise ``ValueError`` naming ``name`` unless finite."""
    try:
        f = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a finite number, got {value!r}") from exc
    if not math.isfinite(f):
        raise ValueError(f"{name} must be a finite number, got {value!r}")
    return f
