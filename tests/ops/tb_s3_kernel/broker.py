"""Offline evidence producer for TB-S3 (not a qualified live route).

Broker truth (positions, working orders, lots, trailing anchors) lives only here. The kernel
never reads it directly: it receives detached ``Evidence`` captures through ``snapshot()``.
Production telemetry does not currently supply this complete E1–E3 protocol.

Capabilities are the spec's L-2 items (a)–(g), each ``supported`` / ``not supported`` /
``unrecorded``. Failure injection (``reject`` / ``unknown`` / ``partial``) drives the
rejection, unknown-outcome and partial-fill branches of the spec's sequences. An ``unknown``
outcome is reported to the caller as such while the broker may or may not have executed it —
the two flavours the spec's S9 distinguishes. Market triggers are explicit harness events;
there is no price-path/slippage simulator. Prices use abstract unit ticks by default;
instrument fixtures must supply ``tick_sizes``. Supported flags characterize this model,
not live L-2 qualification. Scoped close after FIFO owner/allocation divergence is refused;
full-symbol close and triggered-protection allocation are distinct implemented transitions.
"""
from __future__ import annotations

import copy
import inspect
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta

BAR = timedelta(minutes=15)
STALENESS_WINDOW = 2 * BAR + timedelta(seconds=30)   # S2b build ADR §2 Staleness row
BARRIER_TIMEOUT = BAR + timedelta(seconds=30)         # spec S6

L2_ITEMS = ("a", "b", "c", "d", "e", "f", "g")
SUPPORTED = "supported"
NOT_SUPPORTED = "not supported"
UNRECORDED = "unrecorded"

PROTECTIVE_KINDS = ("stop", "limit", "trail")


@dataclass
class Clock:
    """Explicit clock; nothing in the model reads wall-clock time."""

    now: datetime
    sequence: int = 0

    def tick(self) -> int:
        """Harness event order, independent of wall time and evidence delivery order."""
        self.sequence += 1
        return self.sequence

    def advance(self, delta: timedelta) -> datetime:
        """Move time forward and return the new instant."""
        self.now = self.now + delta
        return self.now


@dataclass(frozen=True)
class Outcome:
    """What the route answers to one request (never a fill)."""

    status: str                 # accepted | rejected | unknown
    ref: str | None = None
    detail: str = ""


@dataclass
class BrokerOrder:
    """One order as the broker holds it."""

    ref: str
    sym: str
    leg_id: str
    kind: str                   # entry | add | exit | flat | stop | limit | trail
    side: str                   # buy | sell
    qty: int
    order_type: str             # market | stop | limit | trail
    price: float | None = None
    attached_to: str | None = None      # the lot (fill id) a protective order belongs to
    status: str = "working"             # working | filled | partial | cancelled | rejected
    filled_qty: int = 0
    trail_activation: int | None = None
    trail_offset: int | None = None
    trail_active: bool = False
    trail_anchor: float | None = None

    def view(self) -> dict:
        """The working-order view the spec's ``W`` carries."""
        return {
            "ref": self.ref, "sym": self.sym, "leg_id": self.leg_id,
            "kind": self.kind, "side": self.side, "qty": self.qty,
            "type": self.order_type, "price": self.price, "attached_to": self.attached_to,
            "trail_active": self.trail_active, "trail_anchor": self.trail_anchor,
            "trail_activation": self.trail_activation, "trail_offset": self.trail_offset,
            "remaining": self.qty - self.filled_qty, "filled_qty": self.filled_qty,
        }


@dataclass(frozen=True)
class Execution:  # pylint: disable=too-many-instance-attributes
    """Immutable broker-origin identity captured at execution, before later order edits."""

    execution_id: int
    ref: str
    fill_id: str
    sym: str
    leg_id: str
    kind: str
    side: str
    qty: int
    order_qty: int
    order_type: str
    order_price: float | None
    attached_to: str | None


@dataclass(frozen=True)
class Reduction:
    """One atomic exit, with its protection identity separate from accounting lots."""

    execution_id: int
    sym: str
    transition: str
    order_ref: str | None
    protection_owner: str | None
    allocations: tuple[tuple[str, int], ...]
    execution_allocations: tuple[tuple[int, int], ...]


@dataclass
class Lot:
    """An open fill (one lot) with the protective orders linked to it."""

    fill_id: str
    sym: str
    leg_id: str
    side: str
    qty: int
    entry_ref: str
    price: float = 100.0
    protection: dict[str, str] = field(default_factory=dict)   # component -> order ref
    protection_qty: int = 0     # independent of FIFO accounting quantity
    protection_consumed: bool = False


@dataclass(frozen=True)
class Evidence:
    """Detached symbol facts plus global fences; nested maps permit adversarial delivery tests."""

    sym: str
    as_of: datetime
    position: int
    working: tuple[dict, ...]
    order_status: dict[str, str]
    fills: dict[str, int]       # order ref -> cumulative filled quantity
    lots: dict[str, int] = field(default_factory=dict)   # lot id -> open quantity
    order_level: bool = True    # False for a position-only read (no working list, no status)
    acquired: int = 0           # harness acquisition identity; 0 supplies no causal proof
    request_fence: bool = False # read accounts for every earlier request, including pending
    pending_requests: frozenset[str] = frozenset()
    request_outcomes: dict[str, str] = field(default_factory=dict)
    order_facts: dict[str, dict] = field(default_factory=dict)  # includes terminal orders
    executions: tuple[Execution, ...] = ()  # complete immutable entry execution history
    order_symbols: dict[str, str] | None = None  # global ref location, including terminal refs
    lot_facts: dict[str, dict] = field(default_factory=dict)
    protection_owners: dict[str, dict] = field(default_factory=dict)
    reductions: tuple[Reduction, ...] = ()

    def working_refs(self) -> set[str]:
        """Refs of every working order in this read."""
        return {w["ref"] for w in self.working}


class CapabilityError(RuntimeError):
    """The route was asked for something the spec says it must not be asked for."""


@dataclass
class FakeBroker:  # pylint: disable=too-many-instance-attributes
    """Route with exactly the L-2 capabilities, failure injection and stamped evidence."""

    clock: Clock
    caps: dict[str, str] = field(default_factory=lambda: {i: SUPPORTED for i in L2_ITEMS})
    modify_resets_trail_anchor: bool = False     # the L2(g) sub-record
    positions: dict[str, int] = field(default_factory=dict)
    orders: dict[str, BrokerOrder] = field(default_factory=dict)
    lots: dict[str, Lot] = field(default_factory=dict)
    inject: dict[str, object] = field(default_factory=dict)
    log: list[dict] = field(default_factory=list)
    pending_bracket: dict[str, dict | None] = field(default_factory=dict)
    drop_attached_at_fill: bool = False          # route bug: bracketed fill, no child orders
    _seq: int = 0
    queued_requests: list[tuple[str, str, dict]] = field(default_factory=list)
    request_outcomes: dict[str, str] = field(default_factory=dict)
    executions: list[Execution] = field(default_factory=list)
    reductions: list[Reduction] = field(default_factory=list)
    tick_sizes: dict[str, float] = field(default_factory=dict)  # abstract unit tick unless supplied

    def request(self, action: str, request_id: str, **payload) -> Outcome:
        """Transport acceptance can precede route execution by arbitrarily many events."""
        if (not request_id or request_id in self.request_outcomes
                or any(r[0] == request_id for r in self.queued_requests)):
            return Outcome("rejected", detail="request identity must be new")
        if action not in ("place", "modify", "attach", "cancel", "close"):
            return Outcome("rejected", detail="unknown route action")
        try:
            inspect.signature(getattr(self, action)).bind(**payload)
        except TypeError:
            return Outcome("rejected", detail="invalid route payload")
        if self.inject.get(action) == "defer":
            self.inject.pop(action)
            self.queued_requests.append((request_id, action, copy.deepcopy(payload)))
            self._note("accepted_pending", request_id=request_id, action=action)
            return Outcome("accepted")
        self.queued_requests.append((request_id, action, copy.deepcopy(payload)))
        return self._execute_request(len(self.queued_requests) - 1)

    def execute_next(self) -> Outcome:
        """Independent broker execution event; it never calls back into the listener."""
        request_id, action, _ = self.queued_requests[0]
        result = self._execute_request(0)
        self._note("request_executed", request_id=request_id, action=action)
        return result

    def _execute_request(self, index: int) -> Outcome:
        # Unexpected harness failures retain unresolved ownership; never manufacture a fence.
        request_id, action, payload = self.queued_requests[index]
        result = getattr(self, action)(**payload)
        self.request_outcomes[request_id] = result.status
        self.queued_requests.pop(index)
        return result

    # ── helpers ────────────────────────────────────────────────────────────
    def supports(self, item: str) -> bool:
        """True only for a recorded ``supported`` item (unrecorded is not support)."""
        return self.caps.get(item) == SUPPORTED

    def _take(self, action: str):
        value = self.inject.get(action)
        if isinstance(value, list):
            result = value.pop(0)
            if not value:
                self.inject.pop(action)
            return result
        return self.inject.pop(action, None)

    def _ref(self, prefix: str) -> str:
        self._seq += 1
        while f"{prefix}-{self._seq}" in self.orders:
            self._seq += 1
        return f"{prefix}-{self._seq}"

    @staticmethod
    def _positive_qty(qty) -> bool:
        return type(qty) is int and qty > 0

    def _valid_bracket(self, bracket: dict | None) -> bool:
        if bracket is None:
            return True
        if not isinstance(bracket, dict):
            return False
        if any(k not in ("stop", "limit", "trail_activation_ticks", "trail_offset_ticks")
               for k in bracket):
            return False
        for key in ("stop", "limit"):
            value = bracket.get(key)
            if value is not None and (type(value) not in (int, float)
                                      or not math.isfinite(value)):
                return False
        activation, offset = bracket.get("trail_activation_ticks"), bracket.get("trail_offset_ticks")
        if activation is None and offset is None:
            return True
        return (self.supports("g") and type(activation) is int and activation >= 0
                and self._positive_qty(offset))

    def _note(self, event: str, **detail) -> None:
        self.log.append({"event": event, "at": self.clock.now, **detail})

    @staticmethod
    def lot_id(ref: str) -> str:
        """Initial lot identity only; later generations must use returned/evidenced IDs."""
        return f"{ref}#lot"

    # ── placing ────────────────────────────────────────────────────────────
    def place(self, *, sym: str, leg_id: str, kind: str, side: str, qty: int,
              order_type: str = "market", price: float | None = None,
              bracket: dict | None = None, ref: str | None = None) -> Outcome:
        """Place an entry/add (market or stop) with an optional attached bracket."""
        if (not self._positive_qty(qty) or side not in ("buy", "sell")
                or kind not in ("entry", "add") or not self._valid_bracket(bracket)):
            return Outcome("rejected", detail="invalid entry or bracket")
        if (order_type not in ("market", "stop", "limit")
                or price is not None and (type(price) not in (int, float)
                                         or not math.isfinite(price))
                or order_type in ("stop", "limit") and price is None):
            return Outcome("rejected", detail="invalid order type or price")
        if ref is not None and (not ref or ref in self.orders):
            return Outcome("rejected", detail="order identity must be new")
        if order_type == "stop" and not self.supports("a"):
            return Outcome("rejected", detail="route has no resting stop-entry order type")
        if bracket and not self.supports("b"):
            return Outcome("rejected", detail="route cannot attach brackets at entry")
        inj = self._take("place")
        if inj == "reject":
            return Outcome("rejected", detail="injected reject")
        ref = ref or self._ref("o")
        order = BrokerOrder(ref, sym, leg_id, kind, side, qty, order_type, price)
        if bracket:
            order.trail_activation = bracket.get("trail_activation_ticks")
            order.trail_offset = bracket.get("trail_offset_ticks")
        self.orders[ref] = order
        self.pending_bracket[ref] = dict(bracket) if bracket else None
        self._note("place", ref=ref, kind=kind, qty=qty, order_type=order_type)
        if inj == "unknown_executed":
            return Outcome("unknown", detail="placed; acknowledgement lost")
        if inj == "unknown_lost":
            del self.orders[ref]
            return Outcome("unknown", detail="never reached the route")
        return Outcome("accepted", ref=ref)

    def fill(self, ref: str, qty: int | None = None, price: float = 100.0) -> str:
        """Execute a working entry/add (fully or partially) and create/extend its lot."""
        order = self.orders[ref]
        if (order.kind not in ("entry", "add") or order.attached_to is not None
                or qty is not None and not self._positive_qty(qty)):
            raise CapabilityError("fill requires an entry/add and a positive integer quantity")
        if order.status not in ("working", "partial"):
            raise CapabilityError(f"{ref} is {order.status}, cannot fill")
        remaining = order.qty - order.filled_qty
        if not self._positive_qty(remaining):
            raise CapabilityError("order has no valid working remainder")
        take = remaining if qty is None else min(qty, remaining)
        order.filled_qty += take
        order.status = "filled" if order.filled_qty == order.qty else "partial"
        signed = take if order.side == "buy" else -take
        self.positions[order.sym] = self.positions.get(order.sym, 0) + signed
        execution_id = self.clock.tick()
        lot_id = self.lot_id(ref)
        if lot_id in self.lots:
            active = next((l for l in reversed(list(self.lots.values()))
                           if l.entry_ref == ref and l.qty > 0 and not l.protection_consumed
                           and (l.sym, l.leg_id, l.side)
                           == (order.sym, order.leg_id, order.side)), None)
            lot_id = active.fill_id if active else f"{lot_id}:{execution_id}"
        self.executions.append(Execution(execution_id, ref, lot_id, order.sym,
                                         order.leg_id, order.kind, order.side, take,
                                         order.qty, order.order_type, order.price,
                                         order.attached_to))
        lot = self.lots.get(lot_id)
        if lot is None:
            lot = Lot(lot_id, order.sym, order.leg_id, order.side, 0, ref, price)
            self.lots[lot_id] = lot
        lot.qty += take
        bracket = self.pending_bracket.get(ref)
        if bracket and not lot.protection and not self.drop_attached_at_fill:
            self._attach_protection(lot, bracket, price)
        elif lot.protection and self.supports("e"):
            lot.protection_qty += take
            for pref in lot.protection.values():
                self.orders[pref].qty = lot.protection_qty
        self._note("fill", ref=ref, qty=take, lot=lot_id)
        return lot_id

    def _attach_protection(self, lot: Lot, bracket: dict, price: float) -> None:
        if not lot.protection:
            lot.protection_qty = lot.qty
        exit_side = "sell" if lot.side == "buy" else "buy"
        for component in PROTECTIVE_KINDS:
            level = bracket.get(component)
            if component == "trail":
                if bracket.get("trail_activation_ticks") is None:
                    continue
                if not self.supports("g"):
                    continue
            elif level is None:
                continue
            pref = self._ref(component)
            order = BrokerOrder(pref, lot.sym, lot.leg_id, component, exit_side, lot.protection_qty,
                                component if component != "trail" else "trail",
                                level if component != "trail" else None, attached_to=lot.fill_id)
            if component == "trail":
                order.trail_activation = bracket["trail_activation_ticks"]
                order.trail_offset = bracket["trail_offset_ticks"]
                order.trail_anchor = price
            self.orders[pref] = order
            lot.protection[component] = pref

    # ── modifying / attaching / cancelling ───────────────────────────────────
    def modify(self, ref: str, **changes) -> Outcome:
        """Atomic native modify of one working order (L2(c))."""
        if not self.supports("c"):
            return Outcome("rejected", detail="route has no atomic modify")
        order = self.orders.get(ref)
        if order is None or order.status not in ("working", "partial"):
            return Outcome("rejected", detail="order not working")
        if (not changes or any(k not in ("qty", "price", "trail_activation", "trail_offset")
                               for k in changes)):
            return Outcome("rejected", detail="unsupported modify field")
        qty = changes.get("qty", order.qty)
        price = changes.get("price", order.price)
        if (not self._positive_qty(qty) or qty <= order.filled_qty
                or price is not None and (type(price) not in (int, float)
                                         or not math.isfinite(price))
                or order.order_type in ("stop", "limit") and price is None):
            return Outcome("rejected", detail="invalid quantity or price")
        if "trail_activation" in changes or "trail_offset" in changes:
            activation = changes.get("trail_activation", order.trail_activation)
            offset = changes.get("trail_offset", order.trail_offset)
            if (order.kind != "trail" or not self.supports("g")
                    or type(activation) is not int or activation < 0
                    or not self._positive_qty(offset)):
                return Outcome("rejected", detail="invalid native trail")
        inj = self._take("modify")
        if inj == "reject":
            return Outcome("rejected", detail="injected reject")
        touches_trail = "trail_activation" in changes or "trail_offset" in changes
        if inj == "unknown_lost":
            return Outcome("unknown", detail="modify never reached the route")
        for key, value in changes.items():
            setattr(order, key, value)
        if touches_trail and self.modify_resets_trail_anchor:
            order.trail_active, order.trail_anchor = False, None
        self._note("modify", ref=ref, changes=dict(changes))
        if inj == "unknown":
            return Outcome("unknown", detail="modified; acknowledgement lost")
        return Outcome("accepted", ref=ref)

    def attach(self, fill_id: str, bracket: dict, price: float = 100.0) -> Outcome:
        """Attach protection to an existing open lot, linked to the position (L2(f))."""
        if not self.supports("f"):
            return Outcome("rejected", detail="route cannot attach protection to an open fill")
        lot = self.lots.get(fill_id)
        if lot is None or lot.qty == 0:
            return Outcome("rejected", detail="no open lot")
        if not bracket or not self._valid_bracket(bracket) or lot.protection_consumed:
            return Outcome("rejected", detail="invalid bracket or consumed protection owner")
        components = {c for c in ("stop", "limit") if bracket.get(c) is not None}
        if bracket.get("trail_activation_ticks") is not None:
            components.add("trail")
        if not components:
            return Outcome("rejected", detail="no protection component")
        if components.intersection(lot.protection):
            return Outcome("rejected", detail="defined components require native modify")
        inj = self._take("attach")
        if inj == "reject":
            return Outcome("rejected", detail="injected reject")
        if inj == "unknown_lost":
            return Outcome("unknown", detail="attach never reached the route")
        self._attach_protection(lot, bracket, price)
        self._note("attach", lot=fill_id)
        if inj == "unknown":
            return Outcome("unknown", detail="attached; acknowledgement lost")
        return Outcome("accepted", ref=fill_id)

    def cancel(self, ref: str) -> Outcome:
        """Cancel a working order."""
        order = self.orders.get(ref)
        if order is None or order.status not in ("working", "partial"):
            return Outcome("rejected", detail="order not working")
        inj = self._take("cancel")
        if inj == "reject":
            return Outcome("rejected", detail="injected reject")
        if inj == "unknown_lost":
            return Outcome("unknown", detail="cancel never reached the route")
        order.status = "cancelled"
        self._note("cancel", ref=ref)
        if inj == "unknown":
            return Outcome("unknown", detail="cancelled; acknowledgement lost")
        return Outcome("accepted", ref=ref)

    # ── closing ────────────────────────────────────────────────────────────
    def close(self, *, sym: str, fill_id: str | None = None,
              qty: int | None = None) -> Outcome:
        """Scoped or quantity-less close with atomic attached-order handling (L2(d)/(e))."""
        if not self.supports("d") or not self.supports("e"):
            return Outcome("rejected", detail="route has no atomic scoped close")
        if qty is not None and not self._positive_qty(qty):
            return Outcome("rejected", detail="close quantity must be a positive integer")
        if fill_id is not None and (fill_id not in self.lots or self.lots[fill_id].sym != sym):
            return Outcome("rejected", detail="unknown or foreign lot scope")
        inj = self._take("close")
        if inj == "reject":
            return Outcome("rejected", detail="injected reject")
        if inj == "unknown_lost":
            return Outcome("unknown", detail="close never reached the route")
        sides = {l.side for l in self.lots.values() if l.sym == sym and l.qty > 0}
        if len(sides) > 1 and (fill_id is not None or qty is not None
                              or isinstance(inj, tuple) and inj[0] == "partial"):
            return Outcome("rejected",
                           detail="mixed-side exposure requires atomic full-symbol close")
        lots = ([self.lots[fill_id]] if fill_id else
                [l for l in self.lots.values() if l.sym == sym and l.qty > 0])
        allowance = inj[1] if isinstance(inj, tuple) and inj[0] == "partial" else None
        full_symbol = fill_id is None and qty is None and allowance is None
        if not full_symbol and any(l.protection and l.protection_qty != l.qty
                                   for l in self.lots.values() if l.sym == sym):
            return Outcome("rejected", detail="scoped owner/allocation divergence is unqualified")
        wanted = sum(l.qty for l in lots) if qty is None else qty
        if allowance is not None:
            wanted = min(wanted, allowance)
        plan = self._allocation_plan(lots, wanted)
        for _, lot, take in plan:
            self._reduce_lot(lot, take)
        if full_symbol:
            for owner in self.lots.values():
                if owner.sym == sym:
                    self._consume_protection(owner)
        if plan:
            self.reductions.append(Reduction(self.clock.tick(), sym, "explicit_scope",
                                             None, None, tuple((l.fill_id, q) for _, l, q in plan),
                                             tuple((e.execution_id, q) for e, _, q in plan)))
        self._note("close", sym=sym, fill_id=fill_id, qty=qty)
        if inj == "unknown":
            return Outcome("unknown", detail="closed; acknowledgement lost")
        return Outcome("accepted", ref=fill_id or sym)

    def _allocation_plan(self, lots: list[Lot], wanted: int) -> list[tuple[Execution, Lot, int]]:
        """FIFO is execution order, including interleaved partial fills of one order."""
        by_id = {l.fill_id: l for l in lots}
        available = {l.fill_id: l.qty for l in lots}
        spent: dict[int, int] = {}
        for reduction in self.reductions:
            for execution_id, qty in reduction.execution_allocations:
                spent[execution_id] = spent.get(execution_id, 0) + qty
        plan = []
        for execution in sorted(self.executions, key=lambda e: e.execution_id):
            if execution.fill_id not in by_id:
                continue
            take = min(wanted, available[execution.fill_id],
                       execution.qty - spent.get(execution.execution_id, 0))
            if take > 0:
                plan.append((execution, by_id[execution.fill_id], take))
                available[execution.fill_id] -= take
                wanted -= take
        if wanted > 0 and any(available.values()):
            raise CapabilityError("gross lots lack complete entry execution history")
        return plan

    def _reduce_lot(self, lot: Lot, take: int) -> None:
        if take <= 0:
            return
        signed = -take if lot.side == "buy" else take
        self.positions[lot.sym] = self.positions.get(lot.sym, 0) + signed
        lot.qty -= take
        for component, pref in list(lot.protection.items()):
            order = self.orders[pref]
            if lot.qty == 0:
                order.status = "cancelled"
                del lot.protection[component]
            elif self.supports("e"):
                order.qty = lot.qty
        lot.protection_qty = lot.qty if lot.protection else 0
        if lot.qty == 0:
            lot.protection_consumed = True

    def _consume_protection(self, owner: Lot, triggered: str | None = None) -> None:
        for ref in owner.protection.values():
            if ref != triggered and self.orders[ref].status in ("working", "partial"):
                self.orders[ref].status = "cancelled"
        owner.protection.clear()
        owner.protection_qty = 0
        owner.protection_consumed = True

    # ── market events ──────────────────────────────────────────────────────
    def trigger(self, ref: str) -> None:
        """A working stop/limit/trail order is hit intrabar and executes."""
        order = self.orders[ref]
        if order.status != "working":
            raise CapabilityError(f"{ref} is {order.status}")
        if order.attached_to:
            owner = self.lots[order.attached_to]
            if owner.protection_consumed or ref not in owner.protection.values():
                raise CapabilityError("trigger requires an unconsumed protection owner")
            lots = [l for l in self.lots.values() if l.sym == owner.sym
                    and l.leg_id == owner.leg_id and l.side == owner.side and l.qty > 0]
            plan = self._allocation_plan(lots, order.qty)
            total = sum(q for _, _, q in plan)
            if total <= 0:
                raise CapabilityError("no exposure for protective execution")
            order.status, order.filled_qty = "filled", total
            for _, lot, take in plan:
                lot.qty -= take
                self.positions[lot.sym] += -take if lot.side == "buy" else take
            self._consume_protection(owner, triggered=ref)
            if not any(l.qty > 0 for l in self.lots.values() if l.sym == owner.sym):
                for sibling in self.lots.values():
                    if sibling.sym == owner.sym:
                        self._consume_protection(sibling)
            self.reductions.append(Reduction(self.clock.tick(), owner.sym, "triggered_protection",
                                             ref, owner.fill_id,
                                             tuple((l.fill_id, q) for _, l, q in plan),
                                             tuple((e.execution_id, q) for e, _, q in plan)))
        else:
            self.fill(ref)
        self._note("trigger", ref=ref)

    def move_price(self, sym: str, price: float) -> None:
        """A traded price: native trails activate and follow the favourable extreme."""
        for order in self.orders.values():
            if order.sym != sym or order.status != "working" or order.order_type != "trail":
                continue
            lot = self.lots[order.attached_to]
            base = lot.price
            long = lot.side == "buy"
            distance = order.trail_activation * self.tick_sizes.get(sym, 1.0)
            activation = base + distance if long else base - distance
            if not order.trail_active and ((long and price >= activation)
                                           or (not long and price <= activation)):
                order.trail_active, order.trail_anchor = True, price
            elif order.trail_active:
                order.trail_anchor = (max(order.trail_anchor, price) if long
                                      else min(order.trail_anchor, price))

    # ── evidence ───────────────────────────────────────────────────────────
    def snapshot(self, sym: str, as_of: datetime | None = None) -> Evidence:
        """A read of the broker truth for ``sym`` stamped ``as_of`` (default: now)."""
        working = tuple(o.view() for o in self.orders.values()
                        if o.sym == sym and o.status in ("working", "partial"))
        status = {o.ref: o.status for o in self.orders.values() if o.sym == sym}
        fills = {o.ref: o.filled_qty for o in self.orders.values()
                 if o.sym == sym and o.filled_qty}
        lots = {l.fill_id: l.qty for l in self.lots.values() if l.sym == sym}
        return Evidence(sym, as_of or self.clock.now, self.positions.get(sym, 0),
                        copy.deepcopy(working), status, fills, lots,
                        acquired=self.clock.tick(), request_fence=True,
                        pending_requests=frozenset(r[0] for r in self.queued_requests),
                        request_outcomes=dict(self.request_outcomes),
                        order_facts={o.ref: o.view() for o in self.orders.values() if o.sym == sym},
                        executions=tuple(e for e in self.executions if e.sym == sym),
                        order_symbols={o.ref: o.sym for o in self.orders.values()},
                        lot_facts={l.fill_id: {"sym": l.sym, "leg_id": l.leg_id, "side": l.side,
                                              "entry_ref": l.entry_ref, "qty": l.qty}
                                   for l in self.lots.values() if l.sym == sym},
                        protection_owners={l.fill_id: {"qty": l.protection_qty,
                                                      "consumed": l.protection_consumed,
                                                      "orders": dict(l.protection)}
                                           for l in self.lots.values() if l.sym == sym},
                        reductions=tuple(r for r in self.reductions if r.sym == sym))
