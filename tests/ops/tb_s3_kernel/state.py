"""Durable ownership and dispatch records for the offline kernel contract."""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Obligation:
    """One independent owner of a risk-add block, retained until its discharge event."""

    reason: str
    owner: str
    detail: str = ""


@dataclass
class Attempt:
    """One component's actual dispatch; desired siblings are never implicit attempts."""

    effect_id: str
    fields: dict = field(default_factory=dict)
    status: str = "planned"
    boundary: int = 0
    sent_at: datetime | None = None


@dataclass
class Effect:
    """Persisted before dispatch. Dispatching without an outcome means unknown on restart."""

    effect_id: str
    kind: str
    owner: str
    payload: dict
    status: str = "planned"
    boundary: int = 0
    sent_at: datetime | None = None
    outcome: str | None = None
