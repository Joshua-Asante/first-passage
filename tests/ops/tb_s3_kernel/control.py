"""Offline configuration owner, separate from listener snapshots and broker evidence."""
from dataclasses import dataclass, field

from .broker import Outcome


@dataclass
class ConfigOwner:
    """Idempotent config writes and read-back, with explicit lost/failed outcomes."""
    dry_run: bool = False
    armed_until: object = "armed"
    applied: set = field(default_factory=set)
    inject: str | None = None
    daemon_heartbeats: dict = field(default_factory=dict)

    def disarm(self, request_id):
        mode, self.inject = self.inject, None
        if request_id in self.applied:
            return Outcome("accepted")
        if mode == "reject":
            return Outcome("rejected")
        if mode == "unknown_lost":
            return Outcome("unknown")
        self.dry_run, self.armed_until = True, None
        self.applied.add(request_id)
        return Outcome("unknown" if mode == "unknown" else "accepted")

    def confirms(self, request_id):
        return request_id in self.applied and self.dry_run and self.armed_until is None
