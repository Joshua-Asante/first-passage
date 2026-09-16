"""Pure occurrence and observed protection contracts; no transport or persistence."""
from dataclasses import asdict, dataclass, replace
from datetime import datetime
import hashlib
import json
import math

from c1_signal_daemon.book_protocol import Bracket, Side


@dataclass(frozen=True)
class ActionOccurrence:
    account: str
    account_epoch: str
    session_id: str
    producer: str
    event_id: str
    ordinal: int


@dataclass(frozen=True)
class ProtectionTarget:
    owner_id: str
    entry_fill_id: str
    leg_id: str
    order_symbol: str
    side: Side
    quantity: int
    primitive: str


@dataclass(frozen=True)
class ProtectionChange:
    target: ProtectionTarget
    desired: Bracket
    effective: Bracket
    changed_components: tuple[str, ...]


@dataclass(frozen=True)
class ObservedProtection:
    owner_id: str
    entry_fill_id: str
    leg_id: str
    order_symbol: str
    broker_order_ids: tuple[str, ...]
    operation_id: str | None
    revision: int
    quantity: int
    effective: Bracket
    trail_active: bool
    trail_anchor: float | None


@dataclass(frozen=True)
class ProtectionSnapshot:
    fact_id: str
    account: str
    account_epoch: str
    stream_id: str
    sequence: int
    as_of: datetime
    scope_legs: tuple[str, ...]
    complete: bool
    orders: tuple[ObservedProtection, ...]
    positions: tuple[tuple[str, int], ...]
    resolved_operations: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class ProtectionExecution:
    fact_id: str
    account: str
    account_epoch: str
    owner_id: str
    broker_order_id: str
    as_of: datetime
    quantity: int
    price: float
    allocations: tuple[tuple[str, int], ...]
    terminal: bool
    snapshot: ProtectionSnapshot


@dataclass(frozen=True)
class ProtectionRead:
    occurrence: ActionOccurrence
    scope_legs: tuple[str, ...]
    prepared_at: datetime


def validate_occurrence(occurrence) -> bool:
    return (isinstance(occurrence, ActionOccurrence)
            and all(type(v) is str and bool(v) and v == v.strip() for v in
                    (occurrence.account, occurrence.account_epoch, occurrence.session_id,
                     occurrence.producer, occurrence.event_id))
            and occurrence.producer in ('runtime', 'schedule', 'takeover', 'mode', 'direct')
            and type(occurrence.ordinal) is int and occurrence.ordinal >= 0)


def occurrence_key(occurrence) -> str:
    if not validate_occurrence(occurrence):
        raise ValueError('invalid source occurrence')
    return hashlib.sha256(json.dumps(asdict(occurrence), sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def bracket_from_dict(data) -> Bracket | None:
    return None if data is None else Bracket(**data)


def has_components(bracket) -> bool:
    return bracket is not None and any(v is not None for v in asdict(bracket).values())


def normalize_bracket(bracket, side, mintick):
    if bracket is None:
        return None
    if type(mintick) not in (int, float) or not math.isfinite(mintick) or mintick <= 0:
        raise ValueError('invalid mintick')
    if side not in (Side.BUY, Side.SELL):
        raise ValueError('invalid side')
    def level(value, up):
        if value is None:
            return None
        return round((math.ceil(value / mintick - 1e-9) if up else
                      math.floor(value / mintick + 1e-9)) * mintick, 10)
    return replace(bracket, stop=level(bracket.stop, side == Side.SELL),
                   limit=level(bracket.limit, side == Side.BUY))


def changed_components(old, new) -> tuple[str, ...]:
    old, new = old or Bracket(), new or Bracket()
    return tuple(name for name, changed in (
        ('stop', old.stop != new.stop), ('limit', old.limit != new.limit),
        ('trail', (old.trail_activation_ticks, old.trail_offset_ticks) !=
                  (new.trail_activation_ticks, new.trail_offset_ticks))) if changed)


def is_loosening(old, new, side) -> bool:
    old, new = old or Bracket(), new or Bracket()
    if old.limit != new.limit:
        return True  # No established non-weakening classification for limit changes.
    if old.stop is not None and (new.stop is None or
            (new.stop < old.stop if side == Side.BUY else new.stop > old.stop)):
        return True
    return any(a is not None and (b is None or b > a) for a, b in (
        (old.trail_activation_ticks, new.trail_activation_ticks),
        (old.trail_offset_ticks, new.trail_offset_ticks)))
