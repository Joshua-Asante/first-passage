"""B1 JSON payload builder — same five fields the TV path used."""
from __future__ import annotations

from typing import Any

REQUIRED_FIELDS = ("leg_id", "signal_type", "bar_time", "close", "stop_dist_pts")
SIGNAL_TYPES = frozenset({"entry", "add", "exit", "flat"})


class B1PayloadError(ValueError):
    """Malformed or incomplete B1 payload."""


def fresh_bar_time(leg_id: str, signal_type: str, bar_ts: str | int | float) -> str:
    """Fresh tag every fire — CrossTrade does not idempotent-dedupe order_id."""
    return f"{leg_id}-{signal_type}-{bar_ts}"


def build_b1_payload(
    *,
    leg_id: str,
    signal_type: str,
    bar_time: str | int | float,
    close: float,
    stop_dist_pts: float,
) -> dict[str, Any]:
    """Build the five-field B1 object for POST /c1/<path_token>."""
    if signal_type not in SIGNAL_TYPES:
        raise B1PayloadError(
            f"unknown signal_type {signal_type!r}; valid: {sorted(SIGNAL_TYPES)}"
        )
    payload = {
        "leg_id": str(leg_id),
        "signal_type": str(signal_type),
        "bar_time": bar_time,
        "close": float(close),
        "stop_dist_pts": float(stop_dist_pts),
    }
    for fld in REQUIRED_FIELDS:
        if fld not in payload:
            raise B1PayloadError(f"payload missing required field {fld!r}")
    return payload
