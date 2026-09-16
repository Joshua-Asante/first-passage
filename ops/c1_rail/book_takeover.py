"""Immutable offline takeover evidence; accounting is not an inventory producer."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from .book_protection import ActionOccurrence, ProtectionSnapshot

if TYPE_CHECKING:
    from .book_account_owner import BrokerFact


@dataclass(frozen=True)
class WorkingOrder:
    broker_order_id: str
    operation_id: str
    leg_id: str
    order_symbol: str
    kind: str
    remaining: int


@dataclass(frozen=True)
class InventoryPosition:
    fill_id: str
    operation_id: str
    leg_id: str
    order_symbol: str
    side: str
    remaining: int


@dataclass(frozen=True)
class RequestOutcome:
    operation_id: str
    attempt_id: str
    target_operation_id: str | None
    status: str
    terminal_fact_id: str | None


@dataclass(frozen=True)
class InventoryRead:
    read_id: str
    occurrence: ActionOccurrence
    scope_legs: tuple[str, ...]
    prepared_at: datetime
    after_sequence: int


@dataclass(frozen=True)
class AccountInventory:
    fact_id: str
    account: str
    account_epoch: str
    stream_id: str
    sequence: int
    read_id: str
    as_of: datetime
    scope_legs: tuple[str, ...]
    complete: bool
    positions: tuple[InventoryPosition, ...]
    working_orders: tuple[WorkingOrder, ...]
    protection: ProtectionSnapshot
    requests: tuple[RequestOutcome, ...]
    facts: tuple[BrokerFact, ...]
