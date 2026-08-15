"""Validation primitives for load-bearing numeric and JSON state boundaries."""

from __future__ import annotations

import json
import math
from numbers import Real
from pathlib import Path
from typing import Any


def require_finite_number(
    value: object,
    *,
    field: str,
    minimum: float | None = None,
    strictly_positive: bool = False,
) -> float:
    """Return a finite float that satisfies the declared bounds."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{field} must be a number")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{field} must be finite")
    if strictly_positive and number <= 0:
        raise ValueError(f"{field} must be > 0")
    if minimum is not None and number < minimum:
        raise ValueError(f"{field} must be >= {minimum}")
    return number


def load_strict_json(path: Path) -> Any:
    """Load JSON while rejecting non-standard numeric constants."""
    def reject_constant(token: str) -> None:
        raise ValueError(f"non-standard numeric constant {token!r}")

    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=reject_constant,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"State file {path} is not strict JSON: {exc}") from exc


def dump_strict_json(value: Any, *, indent: int = 2) -> str:
    """Serialize JSON while rejecting non-finite values."""
    try:
        return json.dumps(value, indent=indent, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"State contains a non-JSON value: {exc}") from exc
