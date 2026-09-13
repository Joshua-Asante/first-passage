"""Pure TB-I1 capacity reducer for normalized, owner-validated facts.

No broker commands, persistence, authentication or policy admission. TB-I3 must
serialize access, durably retain the ENTIRE state before sending, and authenticate
complete account evidence. Construct an empty state only from an explicitly
verified flat account; this constructor is not a snapshot importer. Conflicts
retain sticky blocks; reconciliation/epoch migration is deliberately not offered.
Event sequence is the producer's external acquisition/command ordering, not a
consumer-local counter. Broker fact IDs retain immutable execution identity.
"""
from dataclasses import dataclass, replace
from datetime import datetime, timedelta

from book_policy import ACCOUNT_MICRO_CAP, BOOK_LEGS, leg
from book_sizing_context import BookAccountContext, BookExposure


@dataclass(frozen=True)
class Reserve:
    operation_id: str
    leg_id: str
    order_symbol: str
    quantity: int


@dataclass(frozen=True)
class Fill:
    execution_id: str
    operation_id: str
    quantity: int


@dataclass(frozen=True)
class Terminal:
    operation_id: str
    status: str
    cumulative_filled: int


@dataclass(frozen=True)
class Reduction:
    reduction_id: str
    close_request_id: str
    allocations: tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class Quiescence:
    sequence: int
    legs: tuple[str, ...]
    gross: int
    working: int
    protection: int
    pending: int


@dataclass(frozen=True)
class CompleteTakeover:
    operation_id: str
    proof: Quiescence


@dataclass(frozen=True)
class Event:
    event_id: str
    sequence: int
    as_of: datetime
    account_id: str
    owner_epoch: str
    fact: Reserve | Fill | Terminal | Reduction | CompleteTakeover


@dataclass(frozen=True)
class Operation:
    request: Reserve
    status: str  # active, refused, takeover
    terminal: Terminal | None = None


@dataclass(frozen=True)
class Takeover:
    operation_id: str
    displaced: tuple[str, ...]


@dataclass(frozen=True)
class CapacityState:
    account_id: str
    owner_epoch: str
    sequence: int = 0
    operations: tuple[Operation, ...] = ()
    fills: tuple[Fill, ...] = ()
    reductions: tuple[Reduction, ...] = ()
    receipts: tuple[Event, ...] = ()
    blocks: tuple[str, ...] = ()
    takeover: Takeover | None = None
    completed_takeovers: tuple[CompleteTakeover, ...] = ()


def _integer(value, minimum=0):
    return type(value) is int and value >= minimum


def _identity(value):
    return isinstance(value, str) and bool(value.strip())


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _operation(state, identity):
    result = next((o for o in state.operations if o.request.operation_id == identity), None)
    _require(result is not None, "unknown operation")
    return result


def _filled(state, operation_id):
    return sum(f.quantity for f in state.fills if f.operation_id == operation_id)


def _remaining(state, execution_id):
    fill = next((f for f in state.fills if f.execution_id == execution_id), None)
    _require(fill is not None, "unknown execution")
    return fill.quantity - sum(q for r in state.reductions
                               for identity, q in r.allocations if identity == execution_id)


def _reserved(state, operation):
    if operation.status != "active" or operation.terminal is not None:
        return 0
    return operation.request.quantity - _filled(state, operation.request.operation_id)


def exposures(state: CapacityState) -> tuple[BookExposure, ...]:
    """Known gross accounting; blocks signal any incompleteness, never netting."""
    return tuple(BookExposure(
        spec.leg_id,
        sum(_remaining(state, f.execution_id) for f in state.fills
            if _operation(state, f.operation_id).request.leg_id == spec.leg_id),
        sum(_reserved(state, o) for o in state.operations if o.request.leg_id == spec.leg_id),
    ) for spec in BOOK_LEGS)


def used_micro(state: CapacityState) -> int:
    return sum((e.confirmed + e.reserved) * leg(e.leg_id).micro_equiv for e in exposures(state))


def _replace_operation(state, operation):
    return replace(state, operations=tuple(
        operation if o.request.operation_id == operation.request.operation_id else o
        for o in state.operations))


def _reserve(state, request):
    _require(all(_identity(v) for v in (request.operation_id, request.leg_id,
                                       request.order_symbol)), "invalid reservation identity")
    _require(_integer(request.quantity, 1), "invalid reservation quantity")
    _require(not any(r.close_request_id == request.operation_id for r in state.reductions),
             "entry request reuses close identity")
    spec = leg(request.leg_id)
    old = next((o for o in state.operations if o.request.operation_id == request.operation_id), None)
    if old:
        _require(old.request == request, "conflicting operation identity")
        return state
    needed = request.quantity * spec.micro_equiv
    status = "refused"
    takeover = state.takeover
    blocks = state.blocks
    if not blocks and not takeover and needed <= ACCOUNT_MICRO_CAP:
        if used_micro(state) + needed <= ACCOUNT_MICRO_CAP:
            status = "active"
        elif request.leg_id == "aegis_6j":
            displaced = []
            available = ACCOUNT_MICRO_CAP - used_micro(state)
            by_leg = {e.leg_id: e.confirmed + e.reserved for e in exposures(state)}
            for lower in sorted(BOOK_LEGS, key=lambda item: item.priority, reverse=True):
                if lower.priority <= spec.priority or not by_leg[lower.leg_id]:
                    continue
                displaced.append(lower.leg_id)
                available += by_leg[lower.leg_id] * lower.micro_equiv
                if available >= needed:
                    status = "takeover"
                    takeover = Takeover(request.operation_id, tuple(displaced))
                    blocks = ("takeover:" + request.operation_id,)
                    break
    return replace(state, operations=state.operations + (Operation(request, status),),
                   takeover=takeover, blocks=blocks)


def _fill(state, fact):
    _require(_identity(fact.execution_id) and _integer(fact.quantity, 1), "invalid fill")
    old = next((f for f in state.fills if f.execution_id == fact.execution_id), None)
    if old:
        _require(old == fact, "conflicting execution identity")
        return state
    operation = _operation(state, fact.operation_id)
    _require(operation.status == "active" and operation.terminal is None,
             "fill without active reservation")
    _require(fact.quantity <= _reserved(state, operation), "fill exceeds reservation")
    return replace(state, fills=state.fills + (fact,))


def _terminal(state, fact):
    operation = _operation(state, fact.operation_id)
    if operation.terminal:
        _require(operation.terminal == fact, "conflicting terminal")
        return state
    _require(operation.status == "active", "terminal without active operation")
    _require(fact.status in ("filled", "cancelled", "rejected")
             and _integer(fact.cumulative_filled), "invalid terminal")
    _require(fact.cumulative_filled == _filled(state, fact.operation_id),
             "terminal missing execution facts")
    _require(fact.status != "filled" or fact.cumulative_filled == operation.request.quantity,
             "incomplete filled terminal")
    return _replace_operation(state, replace(operation, terminal=fact))


def _reduce(state, fact):
    _require(_identity(fact.reduction_id) and _identity(fact.close_request_id),
             "invalid reduction identity")
    _require(not any(o.request.operation_id == fact.close_request_id for o in state.operations),
             "close request reuses entry identity")
    old = next((r for r in state.reductions if r.reduction_id == fact.reduction_id), None)
    if old:
        _require(old == fact, "conflicting reduction identity")
        return state
    _require(type(fact.allocations) is tuple and bool(fact.allocations), "missing allocations")
    seen = set()
    scopes = set()
    for allocation in fact.allocations:
        _require(type(allocation) is tuple and len(allocation) == 2, "invalid allocation")
        identity, quantity = allocation
        _require(_identity(identity) and identity not in seen and _integer(quantity, 1),
                 "invalid reduction allocation")
        _require(quantity <= _remaining(state, identity), "reduction exceeds execution")
        seen.add(identity)
        fill = next(f for f in state.fills if f.execution_id == identity)
        request = _operation(state, fill.operation_id).request
        scopes.add((request.leg_id, request.order_symbol))
    _require(len(scopes) == 1, "reduction crosses leg or symbol")
    for previous in state.reductions:
        if previous.close_request_id == fact.close_request_id:
            execution_id = previous.allocations[0][0]
            fill = next(f for f in state.fills if f.execution_id == execution_id)
            request = _operation(state, fill.operation_id).request
            _require((request.leg_id, request.order_symbol) in scopes,
                     "close request changed leg or symbol")
    return replace(state, reductions=state.reductions + (fact,))


def _complete(state, fact, sequence):
    previous = next((f for f in state.completed_takeovers
                     if f.operation_id == fact.operation_id), None)
    if previous:
        _require(previous == fact, "conflicting completed takeover")
        return state
    takeover = state.takeover
    _require(takeover is not None and takeover.operation_id == fact.operation_id,
             "unknown takeover")
    _require(state.blocks == ("takeover:" + fact.operation_id,), "other retained blocks")
    proof = fact.proof
    _require(isinstance(proof, Quiescence) and _integer(proof.sequence, 1)
             and state.sequence < proof.sequence <= sequence
             and proof.legs == takeover.displaced, "stale or incomplete quiescence")
    _require(all(type(v) is int and v == 0 for v in
                 (proof.gross, proof.working, proof.protection, proof.pending)),
             "account not quiescent")
    _require(all(e.confirmed == 0 and e.reserved == 0 for e in exposures(state)
                 if e.leg_id in takeover.displaced), "displaced capacity still occupied")
    _require(all(o.terminal is not None for o in state.operations
                 if o.status == "active" and o.request.leg_id in takeover.displaced),
             "displaced operation not terminal")
    operation = _operation(state, fact.operation_id)
    _require(used_micro(state) + operation.request.quantity * leg(operation.request.leg_id).micro_equiv
             <= ACCOUNT_MICRO_CAP, "takeover exceeds cap")
    return replace(_replace_operation(state, replace(operation, status="active")),
                   takeover=None, blocks=(),
                   completed_takeovers=state.completed_takeovers + (fact,))


def apply_event(state: CapacityState, event: Event, *, now: datetime,
                max_age: timedelta) -> CapacityState:
    """Return new retained state. Invalid evidence adds a block, never a release.

    Exact deliveries are no-ops, including after restart; reacquired broker facts
    use a new envelope sequence but their immutable payload must remain identical.
    Invalid deliveries remain in receipts for later explicit reconciliation.
    """
    _require(isinstance(state, CapacityState) and isinstance(event, Event), "typed state/event required")
    if event in state.receipts:
        return state
    try:
        _require(not any(e.event_id == event.event_id for e in state.receipts),
                 "conflicting event identity")
        _require(_identity(event.event_id) and _identity(state.account_id)
                 and _identity(state.owner_epoch) and event.account_id == state.account_id
                 and event.owner_epoch == state.owner_epoch, "account or epoch mismatch")
        _require(_integer(event.sequence, 1) and event.sequence > state.sequence,
                 "nonadvancing sequence")
        _require(isinstance(now, datetime) and now.utcoffset() is not None
                 and isinstance(event.as_of, datetime) and event.as_of.utcoffset() is not None
                 and isinstance(max_age, timedelta) and max_age > timedelta(0)
                 and timedelta(0) <= now - event.as_of <= max_age, "stale evidence")
        fact = event.fact
        handlers = {Reserve: _reserve, Fill: _fill, Terminal: _terminal, Reduction: _reduce}
        if type(fact) is CompleteTakeover:
            result = _complete(state, fact, event.sequence)
        else:
            _require(type(fact) in handlers, "unknown fact type")
            result = handlers[type(fact)](state, fact)
        return replace(result, sequence=event.sequence, receipts=state.receipts + (event,))
    except (ValueError, KeyError, TypeError, AttributeError) as exc:
        block = "capacity:" + str(exc)
        return replace(state, receipts=state.receipts + (event,),
                       blocks=state.blocks if block in state.blocks else state.blocks + (block,))


def project_capacity(state: CapacityState, context: BookAccountContext) -> BookAccountContext:
    """Attach known accounting without renewing or inventing any evidence seal.

    Owner must bind this state to the context's verified snapshot acquisition;
    identity comparison is not snapshot authentication or a fresh broker read.
    """
    _require(state.account_id == context.account_id and state.owner_epoch == context.owner_epoch,
             "capacity/context identity mismatch")
    pending = tuple(o.request.operation_id for o in state.operations
                    if o.status in ("active", "takeover") and o.terminal is None)
    return replace(context, exposures=exposures(state),
                   pending_operation_ids=tuple(dict.fromkeys(context.pending_operation_ids + pending)),
                   blocks=tuple(dict.fromkeys(context.blocks + state.blocks)))
