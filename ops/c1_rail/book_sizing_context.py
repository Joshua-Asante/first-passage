"""TB-I1 pure account-context boundary; never an execution authorization.

TB-C1 supplies the session window. TB-T1 verifies seals and their contents;
TB-I3 supplies current account evidence, boot epoch, lifecycle state and operation
identity. Bindings come from those trusted owners, not the adapter payload.
Here digests are compared, NOT cryptographically verified or computed (Task 4).
The immutable result is a sizing demand. Even a successful capacity observation
must be revalidated and reserved atomically by TB-I3 before any submission.
This module neither persists settlements nor deduplicates broker operations.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from fractions import Fraction

from book_policy import (
    ACCOUNT_MICRO_CAP, BOOK_LEGS, PolicyAbsent, PolicyMismatch, add_quantity,
    as_mode, entry_quantities, is_protected, leg, lifecycle_multiplier, require_policy,
)
from c1_signal_daemon.book_protocol import Mode


@dataclass(frozen=True)
class BookSession:
    session_id: str
    prior_session_id: str
    opens_at: datetime
    risk_add_cutoff: datetime
    closes_at: datetime
    calendar_digest: str
    flatten_start: datetime | None = None
    own_flat_deadline: datetime | None = None


@dataclass(frozen=True)
class SettledClose:
    session_id: str
    as_of: datetime
    equity: float
    peak: float
    seal_digest: str


@dataclass(frozen=True)
class BookSizingBinding:
    """Explicit caller-owned expectations, not an admission or seal verifier."""
    account_id: str
    owner_epoch: str
    policy_digest: str
    snapshot_digest: str
    settlement: SettledClose  # full record obtained from the caller's seal verifier
    session: BookSession
    max_evidence_age: timedelta
    leg_id: str
    order_symbol: str
    cap_alloc: int
    risk_dollars: object  # explicit unscaled account-basis risk; Striker only


@dataclass(frozen=True)
class BookExposure:
    """Gross contract counts; reservations include every unresolved outcome."""
    leg_id: str
    confirmed: int
    reserved: int


@dataclass(frozen=True)
class BookAccountContext:
    account_id: str
    owner_epoch: str
    operation_id: str
    leg_id: str
    order_symbol: str
    session_id: str
    mode: Mode
    policy_digest: str
    snapshot_digest: str
    calendar_digest: str
    settled: SettledClose
    lifecycle_key: str
    lifecycle_tier: str
    as_of: datetime
    valid_until: datetime
    intended_base: int  # previous base operation's intended quantity; zero for entry
    confirmed_base: int  # cumulative confirmed base fill, never intended quantity
    base_operation_id: str | None
    exposures: tuple[BookExposure, ...]  # exactly all four legs, including zeros
    pending_operation_ids: tuple[str, ...]
    blocks: tuple[str, ...]  # owner latches, including unresolved transition cancels


@dataclass(frozen=True)
class BookSizingRequest:
    operation_id: str
    leg_id: str
    order_symbol: str
    kind: str
    normal_base: int | None
    per_contract_risk: object


@dataclass(frozen=True)
class BookSizingDecision:
    operation_id: str | None
    leg_id: str | None
    qty_out: int = 0
    prospective_add: int = 0
    halt: bool = True
    halt_reason: str | None = None
    session_id: str | None = None
    mode: Mode | None = None
    policy_digest: str | None = None
    snapshot_digest: str | None = None
    evidence_as_of: datetime | None = None
    observed_used_micro: int | None = None
    requested_micro: int = 0

    @property
    def submit(self) -> bool:
        """Sizing results cannot authorize an order, even when they fit."""
        return False


def _require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def _text(value) -> bool:
    return isinstance(value, str) and bool(value.strip()) and value == value.strip()


def _digest(value) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _time(value) -> bool:
    return isinstance(value, datetime) and value.tzinfo is not None and value.utcoffset() is not None


def _count(value) -> bool:
    return type(value) is int and value >= 0


def _number(value) -> bool:
    return (not isinstance(value, bool) and isinstance(value, (int, float, Fraction, Decimal))
            and math.isfinite(value) and value >= 0)


def _identities(request, context, binding):
    _require(isinstance(request, BookSizingRequest), "missing_typed_request")
    _require(isinstance(context, BookAccountContext), "missing_typed_context")
    _require(isinstance(binding, BookSizingBinding), "missing_typed_binding")
    spec = leg(request.leg_id)
    for name in ("operation_id", "leg_id", "order_symbol"):
        _require(_text(getattr(request, name)) and
                 getattr(request, name) == getattr(context, name), f"{name}_mismatch")
    for name in ("account_id", "owner_epoch", "leg_id", "order_symbol"):
        _require(_text(getattr(binding, name)) and
                 getattr(binding, name) == getattr(context, name), f"{name}_binding_mismatch")
    for name in ("policy_digest", "snapshot_digest"):
        _require(_digest(getattr(binding, name)) and
                 getattr(binding, name) == getattr(context, name), f"{name}_mismatch")
    _require(request.kind in ("entry", "add"), "risk_reducing_request_requires_account_owner")
    _require(context.lifecycle_key == spec.lifecycle_key, "lifecycle_key_mismatch")
    lifecycle_multiplier(context.lifecycle_tier)
    _require(_count(binding.cap_alloc) and binding.cap_alloc <= ACCOUNT_MICRO_CAP,
             "invalid_cap_alloc")
    return spec


def _session_mode(context, binding, policy, now):
    session, settled = binding.session, context.settled
    _require(isinstance(session, BookSession), "missing_session")
    _require(isinstance(settled, SettledClose), "missing_settled_close")
    _require(all(_time(item) for item in (now, session.opens_at, session.risk_add_cutoff,
                                         session.closes_at, settled.as_of, context.as_of,
                                         context.valid_until)), "invalid_evidence_time")
    _require(session.opens_at < session.risk_add_cutoff <= session.closes_at,
             "invalid_session_window")
    _require(session.opens_at <= now < session.risk_add_cutoff, "outside_risk_add_window")
    _require(_text(session.session_id) and _text(session.prior_session_id) and
             session.session_id != session.prior_session_id and
             context.session_id == session.session_id and
             settled.session_id == session.prior_session_id, "settlement_session_mismatch")
    _require(_digest(session.calendar_digest) and
             context.calendar_digest == session.calendar_digest, "calendar_digest_mismatch")
    _require(isinstance(binding.settlement, SettledClose) and
             _digest(binding.settlement.seal_digest) and
             settled == binding.settlement, "settlement_seal_or_contents_mismatch")
    _require(settled.as_of < session.opens_at <= context.as_of <= now < context.valid_until,
             "stale_or_future_account_evidence")
    _require(isinstance(binding.max_evidence_age, timedelta) and
             binding.max_evidence_age > timedelta(0) and
             now - context.as_of <= binding.max_evidence_age, "stale_account_evidence")
    _require(_number(settled.equity) and _number(settled.peak) and
             settled.peak > 0 and settled.peak >= settled.equity, "invalid_settled_equity_peak")
    expected_mode = (Mode.PROTECTED if is_protected(float(settled.equity),
                     float(settled.peak), policy) else Mode.NORMAL)
    _require(as_mode(context.mode) == expected_mode, "settled_mode_mismatch")
    return expected_mode


def _exposure(context, request):
    _require(isinstance(context.exposures, tuple) and
             all(isinstance(row, BookExposure) for row in context.exposures), "invalid_exposures")
    ids = [row.leg_id for row in context.exposures]
    _require(len(ids) == len(BOOK_LEGS) and set(ids) == {row.leg_id for row in BOOK_LEGS},
             "incomplete_or_duplicate_exposures")
    for row in context.exposures:
        _require(_count(row.confirmed) and _count(row.reserved), "invalid_exposure_quantity")
    for name in ("pending_operation_ids", "blocks"):
        values = getattr(context, name)
        _require(isinstance(values, tuple) and all(_text(item) for item in values) and
                 len(set(values)) == len(values), f"invalid_{name}")
    _require(not context.blocks, "account_owner_blocked")
    _require(request.operation_id not in context.pending_operation_ids, "operation_already_pending")
    own = next(row for row in context.exposures if row.leg_id == request.leg_id)
    used = sum((row.confirmed + row.reserved) * leg(row.leg_id).micro_equiv
               for row in context.exposures)
    _require(used <= ACCOUNT_MICRO_CAP, "observed_capacity_exceeded")
    _require(_count(context.intended_base) and _count(context.confirmed_base) and
             context.confirmed_base <= context.intended_base, "invalid_base_evidence")
    if request.kind == "entry":
        _require(context.intended_base == context.confirmed_base == 0 and
                 context.base_operation_id is None and own.confirmed == own.reserved == 0,
                 "entry_requires_empty_leg")
    else:
        _require(_text(context.base_operation_id) and
                 context.base_operation_id != request.operation_id and
                 0 < context.confirmed_base <= own.confirmed and
                 context.intended_base <= max(leg(request.leg_id).normal_base_values),
                 "add_requires_confirmed_base")
    return own, used


def size_book_request(request, *, context, binding, policy, now) -> BookSizingDecision:
    """Validate supplied evidence relationships and evaluate shared sizing laws.

    No legacy files or current-equity input participate. Capacity is an observation,
    not a reservation: a stale or contended observation cannot authorize execution.
    Takeover, terminal releases and completed-operation dedupe belong to TB-I3.
    """
    identity = (request.operation_id, request.leg_id) if isinstance(request, BookSizingRequest) else (None, None)
    try:
        require_policy(policy)
        spec = _identities(request, context, binding)
        mode = _session_mode(context, binding, policy, now)
        own, used = _exposure(context, request)
        if request.kind == "entry":
            qty, prospective = entry_quantities(
                request.leg_id, mode=mode, policy=policy, lifecycle_tier=context.lifecycle_tier,
                normal_base=request.normal_base, risk_dollars=binding.risk_dollars,
                per_contract_risk=request.per_contract_risk, cap_alloc=binding.cap_alloc)
        else:
            qty = add_quantity(request.leg_id, context.confirmed_base, mode=mode,
                               policy=policy, lifecycle_tier=context.lifecycle_tier)
            prospective = 0
        needed = qty * spec.micro_equiv
        _require((own.confirmed + own.reserved) * spec.micro_equiv + needed <= binding.cap_alloc,
                 "leg_allocation_refusal")
        if used + needed > ACCOUNT_MICRO_CAP:
            lower_used = sum((row.confirmed + row.reserved) * leg(row.leg_id).micro_equiv
                             for row in context.exposures
                             if leg(row.leg_id).priority > spec.priority)
            _require(spec.priority == 1 and used - lower_used + needed <= ACCOUNT_MICRO_CAP,
                     "insufficient_observed_capacity")
        return BookSizingDecision(*identity, qty_out=qty, prospective_add=prospective,
                                  halt=False, session_id=context.session_id, mode=mode,
                                  policy_digest=context.policy_digest, snapshot_digest=context.snapshot_digest,
                                  evidence_as_of=context.as_of, observed_used_micro=used,
                                  requested_micro=needed)
    except (ValueError, TypeError, KeyError, OverflowError, PolicyAbsent, PolicyMismatch) as exc:
        return BookSizingDecision(*identity, halt_reason=str(exc))
