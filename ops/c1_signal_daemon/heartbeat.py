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
    strategy: str = "NullStrategy"
    feed_mode: str = "idle"
    boot_id: str | None = None
    ceremony_id: str | None = None
    ceremony_state: str = "DISABLED"
    effective_emit: bool = False
    poll_interval_s: float | None = None

    def as_json_dict(self) -> dict[str, Any]:
        return asdict(self)
