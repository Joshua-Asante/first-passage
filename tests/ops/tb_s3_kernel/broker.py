"""Fake broker for the TB-S3 kernel model (spec §1: broker truth, L-2 capabilities, evidence).

Broker truth (positions, working orders, lots, trailing anchors) lives only here. The kernel
never reads it directly: it receives ``Evidence`` objects stamped with ``as_of`` through
``snapshot()``, exactly as the listener would receive an execution/position read (L-1).

Capabilities are the spec's L-2 items (a)–(g), each ``supported`` / ``not supported`` /
``unrecorded``. Failure injection (``reject`` / ``unknown`` / ``partial``) drives the
rejection, unknown-outcome and partial-fill branches of the spec's sequences. An ``unknown``
outcome is reported to the caller as such while the broker may or may not have executed it —
the two flavours the spec's S9 distinguishes.
"""
from __future__ import annotations

import copy
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
            "ref": self.ref, "kind": self.kind, "side": self.side, "qty": self.qty,
            "type": self.order_type, "price": self.price, "attached_to": self.attached_to,
            "trail_active": self.trail_active, "trail_anchor": self.trail_anchor,
            "trail_activation": self.trail_activation, "trail_offset": self.trail_offset,
            "remaining": self.qty - self.filled_qty,
        }


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


@dataclass(frozen=True)
class Evidence:
    """A broker read of one symbol at ``as_of`` (positions, working orders, order status)."""

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

    def request(self, action: str, request_id: str, **payload) -> Outcome:
        """Transport acceptance can precede route execution by arbitrarily many events."""
        if self.inject.get(action) == "defer":
            self.inject.pop(action)
            self.queued_requests.append((request_id, action, copy.deepcopy(payload)))
            self._note("accepted_pending", request_id=request_id, action=action)
            return Outcome("accepted")
        result = getattr(self, action)(**payload)
        self.request_outcomes[request_id] = result.status
        return result

    def execute_next(self) -> Outcome:
        """Independent broker execution event; it never calls back into the listener."""
        request_id, action, payload = self.queued_requests.pop(0)
        result = getattr(self, action)(**payload)
        self.request_outcomes[request_id] = result.status
        self._note("request_executed", request_id=request_id, action=action)
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
        return f"{prefix}-{self._seq}"

    def _note(self, event: str, **detail) -> None:
        self.log.append({"event": event, "at": self.clock.now, **detail})

    @staticmethod
    def lot_id(ref: str) -> str:
        """The lot id a fill of order ``ref`` produces (shared with the kernel)."""
        return f"{ref}#lot"

    # ── placing ────────────────────────────────────────────────────────────
    def place(self, *, sym: str, leg_id: str, kind: str, side: str, qty: int,
              order_type: str = "market", price: float | None = None,
              bracket: dict | None = None, ref: str | None = None) -> Outcome:
        """Place an entry/add (market or stop) with an optional attached bracket."""
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
        if order.status not in ("working", "partial"):
            raise CapabilityError(f"{ref} is {order.status}, cannot fill")
        remaining = order.qty - order.filled_qty
        take = remaining if qty is None else min(qty, remaining)
        order.filled_qty += take
        order.status = "filled" if order.filled_qty == order.qty else "partial"
        signed = take if order.side == "buy" else -take
        self.positions[order.sym] = self.positions.get(order.sym, 0) + signed
        lot_id = self.lot_id(ref)
        lot = self.lots.get(lot_id)
        if lot is None:
            lot = Lot(lot_id, order.sym, order.leg_id, order.side, 0, ref, price)
            self.lots[lot_id] = lot
        lot.qty += take
        bracket = self.pending_bracket.get(ref)
        if bracket and not lot.protection and not self.drop_attached_at_fill:
            self._attach_protection(lot, bracket, price)
        elif lot.protection and self.supports("e"):
            for pref in lot.protection.values():
                self.orders[pref].qty = lot.qty
        self._note("fill", ref=ref, qty=take, lot=lot_id)
        return lot_id

    def _attach_protection(self, lot: Lot, bracket: dict, price: float) -> None:
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
            order = BrokerOrder(pref, lot.sym, lot.leg_id, component, exit_side, lot.qty,
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
        if order is None or order.status != "working":
            return Outcome("rejected", detail="order not working")
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
        if not self.supports("d"):
            return Outcome("rejected", detail="route has no atomic scoped close")
        inj = self._take("close")
        if inj == "reject":
            return Outcome("rejected", detail="injected reject")
        if inj == "unknown_lost":
            return Outcome("unknown", detail="close never reached the route")
        lots = ([self.lots[fill_id]] if fill_id else
                [l for l in self.lots.values() if l.sym == sym and l.qty > 0])
        wanted = qty
        for lot in lots:
            take = lot.qty if wanted is None else min(wanted, lot.qty)
            if isinstance(inj, tuple) and inj[0] == "partial":
                take = min(take, inj[1])
            self._reduce_lot(lot, take)
            if wanted is not None:
                wanted -= take
        self._note("close", sym=sym, fill_id=fill_id, qty=qty)
        if inj == "unknown":
            return Outcome("unknown", detail="closed; acknowledgement lost")
        return Outcome("accepted", ref=fill_id or sym)

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

    # ── market events ──────────────────────────────────────────────────────
    def trigger(self, ref: str) -> None:
        """A working stop/limit/trail order is hit intrabar and executes."""
        order = self.orders[ref]
        if order.status != "working":
            raise CapabilityError(f"{ref} is {order.status}")
        if order.attached_to:
            order.status, order.filled_qty = "filled", order.qty
            lot = self.lots[order.attached_to]
            lot.protection = {c: r for c, r in lot.protection.items() if r != ref}
            self._reduce_lot(lot, order.qty)
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
            activation = base + order.trail_activation if long else base - order.trail_activation
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
                        request_outcomes=dict(self.request_outcomes))
