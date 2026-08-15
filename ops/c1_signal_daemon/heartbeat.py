"""Operator-visible liveness snapshot for GET /."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class HeartbeatState:
    ok: bool
    last_bar_age_s: float | None
    feed_healthy: bool
    emit_enabled: bool
    connected: bool

    def as_json_dict(self) -> dict[str, Any]:
        return asdict(self)
