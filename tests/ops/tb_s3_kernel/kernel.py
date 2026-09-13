"""Listener-side kernel of the TB-S3 spec (rev 5.4 §1 state table, primitives, §2 sequences).

One writer per state, exactly as the spec's §1 table: broker truth reaches the kernel only as
``Evidence`` stamped ``as_of``; intent moves ``pending`` to ``sent``, takes a reservation and
records the *intended* protection, nothing else (I2); blocks are account-wide, sticky, one
owner each (I3); ``CLOSE`` / ``AMEND`` / ``ATTACH`` are the only ways protection changes (I7);
completion and no-op determinations use only evidence that postdates the operation's
``prepared_at`` (evidence currency). ``Store`` is the durable state the listener restarts from.

The kernel does not size orders (that is the sizing host's law, R-Q); ``size`` is injectable
and defaults to the adapter-normal quantity so the acceptance cases can use the spec's public
quantities directly.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable

from book_policy import BOOK_LEGS, CapacityDecision, CapacityLedger, TakeoverPlan
from book_policy import leg as leg_spec
from book_protocol import Bracket, OrderIntent, Side

from .broker import (BAR, PROTECTIVE_KINDS, STALENESS_WINDOW, Clock, Evidence, FakeBroker,
                     Outcome)

BLOCK_REASONS = ("kill", "eod", "overlay", "restart_unreconciled", "unknown_order",
                 "close_rejected", "feed", "protection_gap", "arming")
EQUITY_INDEX_SYMBOLS = frozenset({"MYM", "MNQ"})
OWNED_SYMBOLS = tuple(spec.symbol for spec in BOOK_LEGS)
LEG_BY_SYMBOL = {spec.symbol: spec.leg_id for spec in BOOK_LEGS}
UNRESOLVED = ("sent", "unknown", "partial")


def components_of(bracket: Bracket | dict | None) -> dict[str, dict]:
    """The protective components a port-defined bracket carries (empty for a bare lot)."""
    if bracket is None:
        return {}
    if isinstance(bracket, Bracket):
        raw = {"stop": bracket.stop, "limit": bracket.limit,
               "trail_activation_ticks": bracket.trail_activation_ticks,
               "trail_offset_ticks": bracket.trail_offset_ticks}
    else:
        raw = dict(bracket)
    out: dict[str, dict] = {}
    if raw.get("stop") is not None:
        out["stop"] = {"price": raw["stop"]}
    if raw.get("limit") is not None:
        out["limit"] = {"price": raw["limit"]}
    if raw.get("trail_activation_ticks") is not None:
        out["trail"] = {"trail_activation": raw["trail_activation_ticks"],
                        "trail_offset": raw.get("trail_offset_ticks")}
    return out


def bracket_dict(bracket: Bracket | dict | None) -> dict | None:
    """The bracket in the route's field shape (spec R-B1 fields)."""
    if bracket is None:
        return None
    if isinstance(bracket, Bracket):
        return {"stop": bracket.stop, "limit": bracket.limit,
                "trail_activation_ticks": bracket.trail_activation_ticks,
                "trail_offset_ticks": bracket.trail_offset_ticks}
    return dict(bracket)


@dataclass
class PendingOrder:  # pylint: disable=too-many-instance-attributes
    """A risk-adding order the listener sent (spec §1 ``pending[order_ref]``)."""

    ref: str
    leg_id: str
    sym: str
    kind: str
    side: str
    qty: int
    status: str = "sent"        # sent|accepted|filled|partial|cancelled|rejected|unknown
    sent_at: datetime | None = None
    reserved: int = 0           # contracts still reserved (not yet converted or released)
    filled_qty: int = 0
    intended: dict[str, dict] = field(default_factory=dict)   # port-defined protection
    lot_id: str | None = None
    cancel_requested: bool = False
    last_evidence_at: datetime | None = None    # last order-level read that mentioned it


@dataclass
class Operation:  # pylint: disable=too-many-instance-attributes
    """A durable protection operation (spec §1 ``operations[operation_id]``)."""

    op_id: str
    kind: str                   # CLOSE | AMEND | ATTACH
    scope_kind: str             # fill | leg | sym
    scope_id: str
    sym: str
    leg_id: str | None
    reason: str
    prepared_at: datetime
    status: str = "prepared"    # prepared|queued|sent|partial|rejected|unknown|complete|refused
    sent_at: datetime | None = None
    target: str | None = None   # AMEND: the working order modified
    payload: dict = field(default_factory=dict)
    reconciled_at: datetime | None = None
    attempts: int = 0
    detail: str = ""


@dataclass
class Expectation:
    """Spec §1 ``expected_protection[fill]``: intended (from intent) vs working (from evidence)."""

    fill_id: str
    sym: str
    leg_id: str
    intended: dict[str, dict]
    working: dict[str, str | None] = field(default_factory=dict)
    status: dict[str, str] = field(default_factory=dict)      # intended | working | missing
    defined_at: datetime | None = None

    def define(self, components: dict[str, dict], at: datetime) -> None:
        """The port defined (or redefined) protection for this lot."""
        self.intended = dict(components)
        for component in components:
            self.status.setdefault(component, "intended")
            self.working.setdefault(component, None)
        self.defined_at = at

    @property
    def is_bare(self) -> bool:
        """A lot the port has not protected yet (qualified, not a gap)."""
        return not self.intended


@dataclass
class Lot:
    """An open fill as the listener knows it from evidence."""

    fill_id: str
    leg_id: str
    sym: str
    side: str
    qty: int
    entry_ref: str
    filled_at: datetime


@dataclass
class Decision:
    """Outcome of an admission or primitive call."""

    ok: bool
    reason: str
    ref: str | None = None
    op: Operation | None = None
    takeover: TakeoverPlan | None = None


@dataclass
class Store:
    """Durable listener state (the ``ProtectionOperationStore`` and its siblings)."""

    data: dict | None = None


class KernelRefusal(RuntimeError):
    """A call the spec forbids in the current state."""


@dataclass
class Kernel:  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """The listener's execution kernel."""

    broker: FakeBroker
    clock: Clock
    store: Store = field(default_factory=Store)
    protection_cases: dict[str, set[str]] = field(default_factory=dict)
    size: Callable[[str, int], int] = field(default=lambda leg_id, qty_normal: qty_normal)
    ledger: CapacityLedger = field(default_factory=CapacityLedger)
    pending: dict[str, PendingOrder] = field(default_factory=dict)
    operations: dict[str, Operation] = field(default_factory=dict)
    expected: dict[str, Expectation] = field(default_factory=dict)
    lots: dict[str, Lot] = field(default_factory=dict)
    blocks: dict[str, str] = field(default_factory=dict)
    p_ev: dict[str, tuple[int, datetime]] = field(default_factory=dict)
    w_ev: dict[str, tuple[tuple[dict, ...], datetime]] = field(default_factory=dict)
    lot_ev: dict[str, tuple[int, datetime]] = field(default_factory=dict)
    status_ev: dict[str, tuple[str, datetime]] = field(default_factory=dict)
    last_control_read: datetime | None = None
    dry_run: bool = False
    telemetry: list[dict] = field(default_factory=list)
    restarted_at: datetime | None = None
    halted_legs: set[str] = field(default_factory=set)
    _seq: int = 0

    # ── persistence ────────────────────────────────────────────────────────
    PERSISTED = ("pending", "operations", "expected", "lots", "blocks", "p_ev", "w_ev",
                 "lot_ev", "status_ev", "last_control_read", "dry_run", "halted_legs", "_seq")

    def persist(self) -> None:
        """Atomic snapshot of every durable state (one write, as the spec requires)."""
        snap = {name: copy.deepcopy(getattr(self, name)) for name in self.PERSISTED}
        snap["ledger"] = copy.deepcopy({"confirmed": self.ledger.confirmed,
                                        "reserved": self.ledger.reserved})
        self.store.data = snap

    @classmethod
    def restart(cls, store: Store, broker: FakeBroker, clock: Clock, now: datetime,
                **kwargs) -> "Kernel":
        """Spec S9: rebuild from the store; nothing is trusted until reconciled."""
        kernel = cls(broker, clock, store=store, **kwargs)
        if store.data is not None:
            for name in cls.PERSISTED:
                setattr(kernel, name, copy.deepcopy(store.data[name]))
            kernel.ledger.confirmed = dict(store.data["ledger"]["confirmed"])
            kernel.ledger.reserved = dict(store.data["ledger"]["reserved"])
        kernel.restarted_at = now
        kernel.block("restart_unreconciled", "restart")
        return kernel

    # ── blocks (account-wide, sticky, one owner each) ──────────────────────
    def block(self, reason: str, detail: str = "") -> None:
        """Set a sticky account-wide risk-add block."""
        assert reason in BLOCK_REASONS, reason
        self.blocks[reason] = detail
        self._emit(reason, detail=detail)
        self.persist()

    def unblock(self, reason: str) -> None:
        """Only the reason's owner calls this, on confirmed completion."""
        if reason in self.blocks:
            del self.blocks[reason]
            self.persist()

    @property
    def risk_add_blocked(self) -> bool:
        """Any member of ``blocks`` refuses every risk-add (I1/I6)."""
        return bool(self.blocks)

    # ── evidence views (spec §1: CONFIRMED within one bar, else UNKNOWN) ────
    def position(self, sym: str, now: datetime) -> tuple[str, int | None]:
        """``P[sym]`` as the spec defines it."""
        ev = self.p_ev.get(sym)
        if ev is None or now - ev[1] > BAR:
            return ("UNKNOWN", None)
        return ("CONFIRMED", ev[0])

    def working(self, sym: str, now: datetime) -> tuple[str, tuple[dict, ...] | None]:
        """``W[sym]`` as the spec defines it."""
        ev = self.w_ev.get(sym)
        if ev is None or now - ev[1] > BAR:
            return ("UNKNOWN", None)
        return ("CONFIRMED", ev[0])

    def evidence_after(self, sym: str, at: datetime) -> bool:
        """True when both position and working-order evidence postdate ``at``."""
        p, w = self.p_ev.get(sym), self.w_ev.get(sym)
        return bool(p and w and p[1] > at and w[1] > at)   # equal instants prove no order

    def _confirmed_position(self, sym: str) -> int:
        return sum(l.qty for l in self.lots.values() if l.sym == sym and l.qty > 0)

    # ── evidence application (the only writer of P, W, pending outcomes, lots) ─
    def apply_evidence(self, ev: Evidence) -> None:  # pylint: disable=too-many-branches
        """Spec I2: broker evidence alone moves ``P``, ``W``, ``pending`` and the lots."""
        self._sweep_timeouts(ev.as_of)
        self.p_ev[ev.sym] = (ev.position, ev.as_of)
        if not ev.order_level:
            self.persist()
            return
        if ev.order_level:
            self.w_ev[ev.sym] = (ev.working, ev.as_of)
        for ref, status in ev.order_status.items():
            self.status_ev[ref] = (status, ev.as_of)
        for lot_id, open_qty in ev.lots.items():
            self.lot_ev[lot_id] = (open_qty, ev.as_of)
        working_refs = ev.working_refs()
        for order in list(self.pending.values()):
            if order.sym != ev.sym or order.status in ("filled", "cancelled", "rejected"):
                continue
            status = ev.order_status.get(order.ref)
            filled = ev.fills.get(order.ref, 0)
            if ev.order_level and (status is not None or order.ref in working_refs):
                order.last_evidence_at = ev.as_of
            if filled > order.filled_qty:
                self._on_fill(order, filled - order.filled_qty, ev)
                order.filled_qty = filled
                order.status = "filled" if status == "filled" else "partial"
            if status in ("rejected", "cancelled"):
                self._release(order)
                order.status = status
                if status == "cancelled":
                    self._emit("cancel_acknowledged", ref=order.ref)
            elif status == "working" and order.status in ("sent", "unknown"):
                order.status = "accepted"
            elif status == "partial":
                order.status = "partial"
            elif (order.status == "unknown" and status is None and ev.order_level
                  and order.ref not in working_refs and order.sent_at is not None
                  and ev.as_of > order.sent_at
                  and ev.position == self._signed_position(ev.sym)):
                # Order-level absence plus a consistent position: it never executed.
                self._release(order)
                order.status = "rejected"
                self._emit("unknown_resolved_not_executed", ref=order.ref)
        self._settle_operations(ev)          # an amend's completion updates intent first
        self._check_expectations(ev)
        self._sync_lots(ev)
        self._maybe_clear_unknown_order()
        self._maybe_disarm(ev.as_of)
        self.persist()

    def _signed_position(self, sym: str) -> int:
        signed = 0
        for lot in self.lots.values():
            if lot.sym == sym:
                signed += lot.qty if lot.side == "buy" else -lot.qty
        return signed

    def _release(self, order: PendingOrder) -> None:
        if order.reserved:
            self.ledger.release_reservation(order.leg_id, order.reserved)
            order.reserved = 0

    def _on_fill(self, order: PendingOrder, delta: int, ev: Evidence) -> None:
        self.ledger.confirm_fill(order.leg_id, delta)
        order.reserved = max(0, order.reserved - delta)
        lot_id = self.broker.lot_id(order.ref)
        lot = self.lots.get(lot_id)
        if lot is None:
            lot = Lot(lot_id, order.leg_id, order.sym, order.side, 0, order.ref, ev.as_of)
            self.lots[lot_id] = lot
        lot.qty += delta
        order.lot_id = lot_id
        exp = self.expected.get(lot_id)
        if exp is None:
            exp = Expectation(lot_id, order.sym, order.leg_id, {})
            self.expected[lot_id] = exp
        if order.intended and exp.is_bare:
            exp.define(order.intended, ev.as_of)
        self._emit("fill", ref=order.ref, qty=delta, lot=lot_id)

    def _check_expectations(self, ev: Evidence) -> None:
        if not ev.order_level:
            return
        for exp in list(self.expected.values()):
            if exp.sym != ev.sym or exp.is_bare or exp.defined_at is None:
                continue
            lot = self.lots.get(exp.fill_id)
            if (lot is None or lot.qty == 0 or ev.lots.get(exp.fill_id) == 0
                    or ev.as_of < exp.defined_at):
                continue
            attached = {w["kind"]: w for w in ev.working if w.get("attached_to") == exp.fill_id}
            for component, params in exp.intended.items():
                if component in attached and self._matches(attached[component],
                                                            self._fields(params)):
                    exp.working[component] = attached[component]["ref"]
                    exp.status[component] = "working"
                elif exp.status.get(component) != "missing":
                    exp.status[component] = "missing"
                    self.block("protection_gap", f"{exp.fill_id}:{component}")
                    self._emit("protection_gap", fill=exp.fill_id, component=component)
                    self.close("fill", exp.fill_id, ev.as_of, "protection_gap_recovery")

    def _scope_flat(self, op: Operation, ev: Evidence) -> bool:
        """Flat on THIS read: order-level reads only; absent data is never flatness."""
        if not ev.order_level:
            return False
        if op.scope_kind == "fill":
            open_qty = ev.lots.get(op.scope_id)
            if open_qty is None:
                return False
            attached = any(w.get("attached_to") == op.scope_id for w in ev.working)
            return open_qty == 0 and not attached
        protective = any(w["kind"] in PROTECTIVE_KINDS for w in ev.working)
        return ev.position == 0 and not protective

    def _settle_operations(self, ev: Evidence) -> None:
        if not ev.order_level:
            return                                        # position-only reads settle nothing
        for op in list(self.operations.values()):
            if (op.sym != ev.sym or op.status in ("complete", "refused", "queued")
                    or ev.as_of <= op.prepared_at):
                continue
            if op.kind == "CLOSE":
                self._settle_close(op, ev)
            else:
                self._settle_protection_op(op, ev)
        self._dispatch_queued(ev.sym, ev.as_of)

    def _settle_close(self, op: Operation, ev: Evidence) -> None:
        if self._scope_flat(op, ev):
            self._complete_close(op, ev)
            return
        if op.status not in ("sent", "unknown", "rejected", "partial"):
            return
        before = op.payload.get("last_exposure", self._scope_exposure(op))
        self._sync_lots(ev)
        after = self._scope_exposure(op)
        op.payload["last_exposure"] = after
        if op.status in ("sent", "unknown", "partial") and after < before:
            op.status = "partial"
            op.payload["closed"] = op.payload.get("closed", 0) + (before - after)
            self._emit("operation_outcome", op=op.op_id, status="partial", remaining=after)
        requested = op.payload.get("qty")
        if (requested is not None and op.payload.get("closed", 0) >= requested
                and self._residual_protected(op, ev)):
            self._complete_close(op, ev)
        op.reconciled_at = ev.as_of

    def _residual_protected(self, op: Operation, ev: Evidence) -> bool:
        """A bounded reduction is done only with the expected residual protection."""
        exp = self.expected.get(op.scope_id)
        if exp is None:
            return False
        attached = {w["kind"]: w for w in ev.working
                    if w.get("attached_to") == op.scope_id}
        return all(c in attached and attached[c]["qty"] == ev.lots.get(op.scope_id)
                   and self._matches(attached[c], self._fields(params))
                   for c, params in exp.intended.items())

    def _scope_exposure(self, op: Operation) -> int:
        if op.scope_kind == "fill":
            lot = self.lots.get(op.scope_id)
            return lot.qty if lot else 0
        return self._confirmed_position(op.sym)

    def _settle_protection_op(self, op: Operation, ev: Evidence) -> None:
        if self._scope_flat(op, ev):
            op.status, op.detail = "complete", "scope consumed"
            return
        exp = self.expected.get(op.scope_id)
        if exp is None:
            return
        attached = {w["kind"]: w for w in ev.working if w.get("attached_to") == exp.fill_id}
        if op.kind == "AMEND":
            wanted = op.payload.get("changes", {})
            done = all(c in attached and self._matches(attached[c], ch["fields"])
                       for c, ch in wanted.items())
            if done:
                for component, change in wanted.items():
                    exp.intended[component] = change["intended"]
                    exp.working[component] = attached[component]["ref"]
                    exp.status[component] = "working"
                op.status = "complete"
            elif op.status in ("sent", "unknown", "rejected"):
                op.reconciled_at = ev.as_of
            return
        if all(c in attached and self._matches(attached[c], self._fields(p))
               for c, p in exp.intended.items()):
            for component in exp.intended:
                exp.working[component] = attached[component]["ref"]
                exp.status[component] = "working"
            op.status = "complete"
        elif op.status in ("sent", "unknown", "rejected"):
            op.reconciled_at = ev.as_of

    @staticmethod
    def _fields(params: dict) -> dict:
        """Route-field shape of one intended component."""
        return {key: value for key, value in params.items()
                if key in ("price", "trail_activation", "trail_offset")}

    @staticmethod
    def _matches(working: dict, fields: dict) -> bool:
        """The working order carries every requested parameter."""
        return all(working.get(key) == value for key, value in fields.items()
                   if value is not None)

    def _sync_lots(self, ev: Evidence) -> None:
        for lot_id, open_qty in ev.lots.items():
            lot = self.lots.get(lot_id)
            if lot is not None and lot.sym == ev.sym:
                lot.qty = open_qty
                if open_qty == 0 and not any(w.get("attached_to") == lot_id
                                            for w in ev.working):
                    self.expected.pop(lot_id, None)
        for leg_id in {l.leg_id for l in self.lots.values() if l.sym == ev.sym}:
            self.ledger.confirm_position(leg_id, sum(l.qty for l in self.lots.values()
                                                     if l.leg_id == leg_id))

    def _complete_close(self, op: Operation, ev: Evidence) -> None:
        op.status = "complete"
        self._sync_lots(ev)
        for lot in self.lots.values():
            if lot.sym == ev.sym and lot.qty == 0:
                self.expected.pop(lot.fill_id, None)
        if "close_rejected" in self.blocks and not any(
                o.kind == "CLOSE" and o.status in ("rejected", "refused")
                for o in self.operations.values()):
            self.unblock("close_rejected")
        if op.reason == "protection_gap_recovery" and not any(
                s == "missing" for e in self.expected.values() for s in e.status.values()):
            self.unblock("protection_gap")
        self._emit("close_complete", op=op.op_id, reason=op.reason)

    def _maybe_clear_unknown_order(self) -> None:
        unresolved_orders = any(o.status == "unknown" for o in self.pending.values())
        unresolved_ops = any(o.status in ("sent", "unknown", "partial")
                             for o in self.operations.values())
        if "unknown_order" in self.blocks and not unresolved_orders and not unresolved_ops:
            self.unblock("unknown_order")

    # ── admission (spec S1 (5)) ────────────────────────────────────────────
    def _required_l2(self, leg_id: str, intent: OrderIntent) -> set[str]:
        cases = self.protection_cases.get(leg_id, set())
        components = components_of(intent.bracket)
        required = {"c", "d", "e"}
        if intent.order_type == "stop":
            required.add("a")
        if "bracket_at_entry" in cases or components:
            required.add("b")
        if "bare_entry" in cases:
            required.add("f")
        if "trailing" in cases or "trail" in components:
            required.add("g")
        return required

    def admit_entry(self, intent: OrderIntent, now: datetime) -> Decision:
        """Spec S1 (5)–(6): admission in the frozen order, then send; I4 sizing authority."""
        if intent.kind not in ("entry", "add"):
            raise KernelRefusal("admit_entry takes risk-adds only")
        self._sweep_timeouts(now)
        spec = leg_spec(intent.leg_id)
        sym = spec.symbol
        if self.risk_add_blocked:
            return self._refuse("policy_block", ",".join(sorted(self.blocks)))
        if intent.leg_id in self.halted_legs:
            return self._refuse("leg_halted", intent.leg_id)
        if intent.side != spec.entry_side or (sym in EQUITY_INDEX_SYMBOLS
                                              and intent.side == Side.SELL):
            return self._refuse("side_refused", f"{intent.leg_id}:{intent.side.value}")
        missing = sorted(i for i in self._required_l2(intent.leg_id, intent)
                         if not self.broker.supports(i))
        if missing:
            return self._refuse("l2_refused", ",".join(missing))
        for state in (self.position(sym, now), self.working(sym, now)):
            if state[0] == "UNKNOWN":
                return self._refuse("unknown_state", sym)
        qty = self.size(intent.leg_id, intent.qty)
        if qty <= 0:
            return self._refuse("floored", intent.leg_id)
        decision: CapacityDecision = self.ledger.request(intent.leg_id, qty)
        if not decision.admitted:
            if decision.takeover is not None:
                return Decision(False, "takeover_required", takeover=decision.takeover)
            return self._refuse("capacity_refused", decision.reason)
        return self._place(intent, qty, now)

    def _refuse(self, reason: str, detail: str) -> Decision:
        self._emit(reason, detail=detail)
        return Decision(False, reason)

    def _place(self, intent: OrderIntent, qty: int, now: datetime) -> Decision:
        spec = leg_spec(intent.leg_id)
        ref = self._next("ord")
        order = PendingOrder(ref, intent.leg_id, spec.symbol, intent.kind, intent.side.value, qty,
                             sent_at=now, reserved=qty, intended=components_of(intent.bracket))
        self.pending[ref] = order
        self.persist()                                    # pending + reservation before send
        if self.dry_run:
            order.status = "not_sent"
            self._release(order)
            self.persist()
            return Decision(True, "dry_run", ref=ref)
        outcome = self.broker.place(sym=spec.symbol, leg_id=intent.leg_id, kind=intent.kind,
                                    side=intent.side.value, qty=qty,
                                    order_type=intent.order_type, price=intent.price,
                                    bracket=bracket_dict(intent.bracket), ref=ref)
        self._apply_send_outcome(order, outcome)
        self.persist()
        return Decision(outcome.status == "accepted", outcome.status, ref=ref)

    def _apply_send_outcome(self, order: PendingOrder, outcome: Outcome) -> None:
        if outcome.status == "accepted":
            order.status = "accepted"
        elif outcome.status == "rejected":
            self._release(order)
            order.status = "rejected"
        else:
            order.status = "unknown"
            self.block("unknown_order", order.ref)

    # ── takeover (spec S10) ────────────────────────────────────────────────
    def takeover(self, plan: TakeoverPlan, now: datetime) -> list[Operation]:
        """Cancel every displaced resting or partially filled risk-add, then ``CLOSE`` each
        displaced symbol; cancellation counts only when evidence confirms it (settle)."""
        if self.risk_add_blocked:
            raise KernelRefusal("takeover under a block")
        self.ledger.begin_takeover(plan)
        ops = []
        for leg_id in plan.displaced:
            sym = leg_spec(leg_id).symbol
            resting = [o for o in self.pending.values() if o.leg_id == leg_id
                       and o.status in ("accepted", "sent", "unknown", "partial")]
            for order in resting:
                order.cancel_requested = self.broker.cancel(order.ref).status == "accepted"
            op = self.close("sym", sym, now, "capacity_takeover")
            op.payload["cancel_refs"] = [o.ref for o in resting]
            ops.append(op)
        self.persist()
        return ops

    def settle_takeover(self, intent: OrderIntent, now: datetime) -> Decision:
        """Admit the requester only when every displaced cancel is confirmed by evidence and
        every displaced symbol is flat on postdating evidence."""
        takeover = self.ledger._takeover  # pylint: disable=protected-access
        if takeover is None:
            raise KernelRefusal("no takeover pending")
        for leg_id in takeover.plan.displaced:
            sym = leg_spec(leg_id).symbol
            ops = [o for o in self.operations.values()
                   if o.reason == "capacity_takeover" and o.sym == sym]
            if not ops:
                takeover.fail(leg_id, "no close operation")
                break
            op = ops[-1]
            unconfirmed = [r for r in op.payload.get("cancel_refs", [])
                           if self.pending[r].status not in ("cancelled", "filled", "rejected")]
            if unconfirmed:
                takeover.fail(leg_id, f"cancel not confirmed for {unconfirmed}")
                break
            takeover.ack_cancel(leg_id)
            if op.status != "complete":
                takeover.fail(leg_id, f"close not confirmed ({op.status})")
                break
            takeover.confirm_close(leg_id, self.p_ev[sym][0])
        decision = self.ledger.settle_takeover()
        if not decision.admitted:
            self._emit("capacity_takeover_refused", reason=decision.reason)
            return Decision(False, "takeover_refused")
        return self._place(intent, takeover.plan.contracts, now)

    # ── CLOSE (spec §1 primitive) ──────────────────────────────────────────
    def close(self, scope_kind: str, scope_id: str, now: datetime, reason: str,
              op_id: str | None = None, qty: int | None = None) -> Operation:
        """Prepare a durable close; send only when postdating evidence does not show it flat.
        Overlapping scopes serialize: one close in flight per symbol, later ones queue."""
        if op_id and op_id in self.operations:
            return self.operations[op_id]            # idempotent by operation identity
        self._sweep_timeouts(now)
        sym, leg_id = self._scope(scope_kind, scope_id)
        for other in self.operations.values():
            if (other.sym == sym and other.kind == "CLOSE" and other.scope_id == scope_id
                    and other.scope_kind == scope_kind and other.reason == reason
                    and (op_id is None or other.op_id == op_id)
                    and other.status in ("prepared", "queued", "rejected", *UNRESOLVED)):
                return other                          # idempotent by scope (retry path)
        op = Operation(op_id or self._next("op"), "CLOSE", scope_kind, scope_id, sym, leg_id,
                       reason, prepared_at=now, payload={"qty": qty})
        self.operations[op.op_id] = op
        self._emit("operation_prepared", op=op.op_id, reason=reason)
        self.persist()
        if not (self.broker.supports("d") and self.broker.supports("e")):
            op.status, op.detail = "refused", "route lacks L2(d)/(e)"
            self.block("close_rejected", f"{op.op_id}:capability")
            return op
        if any(o is not op and o.sym == sym and o.kind == "CLOSE" and o.status in UNRESOLVED
               for o in self.operations.values()):
            op.status = "queued"                      # never dropped: dispatched in turn
            self._emit("operation_queued", op=op.op_id)
            self.persist()
            return op
        self._progress_one(op, now)
        self.persist()
        return op

    def progress(self, now: datetime) -> None:
        """Send every prepared close that postdating evidence does not show as a no-op,
        then dispatch queued closes on symbols with nothing in flight."""
        self._sweep_timeouts(now)
        for op in list(self.operations.values()):
            if op.kind == "CLOSE" and op.status == "prepared":
                self._progress_one(op, now)
        for sym in OWNED_SYMBOLS:
            self._dispatch_queued(sym, now)
        self.persist()

    def _dispatch_queued(self, sym: str, now: datetime) -> None:
        if any(o.sym == sym and o.kind == "CLOSE" and o.status in UNRESOLVED
               for o in self.operations.values()):
            return
        for op in list(self.operations.values()):
            if op.sym == sym and op.kind == "CLOSE" and op.status == "queued":
                op.status = "prepared"
                self._progress_one(op, now)
                if op.status in UNRESOLVED:
                    return                            # one in flight per symbol

    def _sweep_timeouts(self, now: datetime) -> None:
        """Spec S1 cut: no order-level evidence about a sent/accepted order within one bar
        makes it UNKNOWN and blocks every risk-add account-wide until evidence resolves it."""
        for order in self.pending.values():
            if order.status not in ("sent", "accepted", "partial") or order.sent_at is None:
                continue
            last = order.last_evidence_at or order.sent_at
            if now - last > BAR:
                order.status = "unknown"
                self.block("unknown_order", order.ref)
                self._emit("unknown_order", ref=order.ref, since=last.isoformat())

    def _progress_one(self, op: Operation, now: datetime) -> None:
        # A no-op needs evidence that postdates the operation; without it the close is sent
        # (a pre-buffer snapshot, however fresh, never skips a symbol — spec S7 (3), AC-8).
        if self.evidence_after(op.sym, op.prepared_at):
            ev = self._latest_evidence(op.sym)
            if self._scope_flat(op, ev):
                self._complete_close(op, ev)
                self._emit("close_noop", op=op.op_id)
                return
        self._send_close(op, now)

    def cancel(self, ref: str, now: datetime) -> Decision:
        """Spec S4: a cancel is classified by the listener from ``pending`` and fresh ``W``."""
        order = self.pending.get(ref)
        if order is not None and order.kind in ("entry", "add"):
            outcome = self.broker.cancel(ref)
            order.cancel_requested = outcome.status == "accepted"
            self._emit("cancel_sent", ref=ref, outcome=outcome.status)
            self.persist()
            return Decision(outcome.status == "accepted", outcome.status, ref=ref)
        # A protective order: only orphan removal on a confirmed-flat position is admissible.
        sym = next((w_sym for w_sym, (orders, _) in self.w_ev.items()
                    if any(w["ref"] == ref for w in orders)), None)
        if sym is None:
            return self._refuse("cancel_unknown_ref", ref)
        state, qty = self.position(sym, now)
        if state == "CONFIRMED" and qty == 0:
            outcome = self.broker.cancel(ref)
            return Decision(outcome.status == "accepted", "orphan_removed", ref=ref)
        return self._refuse("protective_cancel_refused", ref)

    def kill_status(self, daemon_reachable: bool, now: datetime) -> dict:
        """S8 (7): completion reported beside the daemon-app acknowledgement."""
        return {"complete": self.flatten_complete("kill", now), "disarmed": self.dry_run,
                "daemon_control": "acknowledged" if daemon_reachable else "not_reached"}

    def _latest_evidence(self, sym: str) -> Evidence:
        position, p_at = self.p_ev[sym]
        working, _ = self.w_ev[sym]
        status = {r: s for r, (s, _) in self.status_ev.items()}
        lots = {lid: q for lid, (q, _) in self.lot_ev.items()}
        return Evidence(sym, p_at, position, working, status, {}, lots)

    def _send_close(self, op: Operation, now: datetime) -> None:
        op.payload["last_exposure"] = self._scope_exposure(op)
        if op.scope_kind == "fill":
            qty = op.payload.get("qty")
            if qty is not None:
                qty = max(0, qty - op.payload.get("closed", 0))
            outcome = self.broker.close(sym=op.sym, fill_id=op.scope_id, qty=qty)
        else:
            outcome = self.broker.close(sym=op.sym)           # quantity-less, exclusively owned
        op.sent_at, op.attempts = now, op.attempts + 1
        self._emit("operation_sent", op=op.op_id, outcome=outcome.status)
        if outcome.status == "accepted":
            op.status = "sent"
            self.block("unknown_order", op.op_id)      # unresolved close blocks risk-adds
        elif outcome.status == "rejected":
            op.status, op.detail = "rejected", outcome.detail
            self.block("close_rejected", op.op_id)
        else:
            op.status = "unknown"
            self.block("unknown_order", op.op_id)

    def retry(self, op_id: str, now: datetime) -> Operation:
        """Resubmit a rejected, unknown or partial close only after reconciliation on
        postdating evidence — never blindly; a rejected close at most once per bar."""
        op = self.operations[op_id]
        if op.kind != "CLOSE":
            raise KernelRefusal("retry requires a CLOSE operation")
        if op.status not in ("rejected", "unknown", "partial"):
            raise KernelRefusal(f"{op_id} is {op.status}")
        if op.reconciled_at is None or op.reconciled_at < (op.sent_at or op.prepared_at):
            raise KernelRefusal("reconcile on postdating evidence before resubmitting")
        if op.status == "rejected" and op.sent_at is not None and now - op.sent_at < BAR:
            raise KernelRefusal("a rejected close is retried at most once per bar")
        op.reconciled_at = None
        self._send_close(op, now)
        self.persist()
        return op

    # ── AMEND / ATTACH (spec §1 primitives) ────────────────────────────────
    def amend(self, fill_id: str, bracket: Bracket | dict, now: datetime) -> Decision:
        """The port re-issued its bracket for a lot: component-wise modify, or first attach."""
        self._sweep_timeouts(now)
        lot = self.lots.get(fill_id)
        if lot is None or lot.qty == 0:
            return self._refuse("amend_no_lot", fill_id)
        exp = self.expected.setdefault(fill_id, Expectation(fill_id, lot.sym, lot.leg_id, {}))
        unresolved = [o for o in self.operations.values()
                      if o.scope_id == fill_id and o.status in UNRESOLVED]
        if unresolved:
            return self._refuse("amend_deferred", f"operation {unresolved[0].op_id} unresolved")
        new = components_of(bracket)
        if exp.is_bare:
            return self._attach(exp, new, now)
        w_state, w_orders = self.working(lot.sym, now)
        w_at = self.w_ev.get(lot.sym, (None, None))[1]
        last_op = max((o.sent_at or o.prepared_at for o in self.operations.values()
                       if o.scope_id == fill_id and o.sent_at), default=None)
        if w_state == "UNKNOWN" or (last_op is not None and w_at is not None and w_at < last_op):
            return self._refuse("amend_deferred", "W unknown; reconcile before modifying")
        if not self.broker.supports("c"):
            return self._refuse("l2_refused", "c")
        current = {w["kind"]: w for w in w_orders if w.get("attached_to") == fill_id}
        changes = self._diff(exp, new, current, lot.side)
        if changes is None:
            return self._refuse("amend_deferred", "trail parameters change would reset the anchor")
        if not changes:
            return Decision(True, "unchanged")
        if any(c["loosening"] for c in changes.values()) and self.risk_add_blocked:
            return self._refuse("policy_block", "loosening amend under a block")
        op = Operation(self._next("op"), "AMEND", "fill", fill_id, lot.sym, lot.leg_id, "amend",
                       prepared_at=now, payload={"changes": changes})
        self.operations[op.op_id] = op
        self.persist()
        for component, change in changes.items():
            ref = current[component]["ref"]
            op.target = ref
            outcome = self.broker.modify(ref, **change["fields"])
            op.sent_at, op.attempts = now, op.attempts + 1
            if outcome.status == "accepted":
                op.status = "sent"                    # complete only on broker evidence
            elif outcome.status == "rejected":
                op.status, op.detail = "rejected", outcome.detail   # old protection stands
            else:
                op.status = "unknown"
                self.block("unknown_order", op.op_id)
                break
        self.persist()
        return Decision(op.status == "sent", op.status, op=op)

    def _diff(self, exp: Expectation, new: dict, current: dict, side: str):
        changes: dict[str, dict] = {}
        for component, params in new.items():
            old = exp.intended.get(component)
            if old == params:
                continue                                  # unchanged: never re-sent
            if component == "trail":
                live = current.get("trail")
                if live and live.get("trail_active") and self.broker.modify_resets_trail_anchor:
                    return None                           # would move the effective stop back
                loosening = bool(old) and (
                    params.get("trail_activation", 0) > old.get("trail_activation", 0)
                    or (params.get("trail_offset") or 0) > (old.get("trail_offset") or 0))
                changes[component] = {"fields": dict(params), "loosening": loosening,
                                      "intended": params}
                continue
            if component not in current:
                continue
            new_price, old_price = params["price"], (old or {}).get("price")
            if component == "stop" and old_price is not None:
                loosening = new_price < old_price if side == "buy" else new_price > old_price
            else:
                loosening = False
            changes[component] = {"fields": {"price": new_price}, "loosening": loosening,
                                  "intended": params}
        return changes

    def _attach(self, exp: Expectation, components: dict[str, dict], now: datetime) -> Decision:
        if not self.broker.supports("f"):
            return self._refuse("l2_refused", "f")
        exp.define(components, now)                       # intended before send
        op = Operation(self._next("op"), "ATTACH", "fill", exp.fill_id, exp.sym, exp.leg_id,
                       "attach", prepared_at=now, payload={"components": components})
        self.operations[op.op_id] = op
        self.persist()
        outcome = self.broker.attach(exp.fill_id, self._bracket_from(components))
        op.sent_at, op.attempts = now, op.attempts + 1
        if outcome.status == "accepted":
            op.status = "sent"                           # working only on evidence
        elif outcome.status == "rejected":
            op.status, op.detail = "rejected", outcome.detail
            for component in exp.intended:               # known unprotected exposure: now
                exp.status[component] = "missing"
            self.block("protection_gap", f"{exp.fill_id}:attach_rejected")
            self._emit("protection_gap", fill=exp.fill_id, component="attach")
            self.close("fill", exp.fill_id, now, "protection_gap_recovery")
        else:
            op.status = "unknown"
            self.block("unknown_order", op.op_id)
        self.persist()
        return Decision(outcome.status == "accepted", outcome.status, op=op)

    @staticmethod
    def _bracket_from(components: dict[str, dict]) -> dict:
        out: dict = {}
        if "stop" in components:
            out["stop"] = components["stop"]["price"]
        if "limit" in components:
            out["limit"] = components["limit"]["price"]
        if "trail" in components:
            out["trail_activation_ticks"] = components["trail"]["trail_activation"]
            out["trail_offset_ticks"] = components["trail"]["trail_offset"]
        return out

    # ── exits (spec S5) ────────────────────────────────────────────────────
    def handle_exit(self, leg_id: str, now: datetime, fill_id: str | None = None,
                    qty: int | None = None) -> Operation:
        """A strategy exit or flat: ``CLOSE(fill)`` with a clamped quantity, or ``CLOSE(leg)``."""
        if fill_id is None:
            return self.close("leg", leg_id, now, "exit")
        lot = self.lots[fill_id]
        if qty is not None and qty > lot.qty:
            self._emit("exit_qty_clamped", fill=fill_id, requested=qty, clamped=lot.qty)
            qty = lot.qty
        return self.close("fill", fill_id, now, "exit", qty=qty)

    # ── EOD and kill (spec S7, S8) ─────────────────────────────────────────
    def eod(self, now: datetime) -> list[Operation]:
        """S7 (1)–(3): block, cancel resting risk-adds, prepare a close for every owned symbol."""
        self.block("eod", now.isoformat())
        return self._flatten_all(now, "eod_flatten")

    def kill(self, now: datetime) -> list[Operation]:
        """S8: the listener block first, then the S7 steps."""
        self.block("kill", now.isoformat())
        return self._flatten_all(now, "kill")

    def _flatten_all(self, now: datetime, reason: str) -> list[Operation]:
        for order in self.pending.values():
            if order.kind in ("entry", "add") and order.status in ("accepted", "sent", "unknown",
                                                                   "partial"):
                if self.broker.cancel(order.ref).status == "accepted":
                    order.cancel_requested = True
        ops = [self.close("sym", sym, now, reason) for sym in OWNED_SYMBOLS]
        self.persist()
        return ops

    def flatten_complete(self, reason: str, now: datetime) -> bool:
        """S7 (4)–(5) / S8 completion: every owned symbol flat with no working order,
        on evidence that postdates its close operation (pure; no side effect)."""
        del now
        ops = [o for o in self.operations.values() if o.reason == reason]
        if len(ops) < len(OWNED_SYMBOLS) or any(o.status != "complete" for o in ops):
            return False
        for sym in OWNED_SYMBOLS:
            prepared = max(o.prepared_at for o in ops if o.sym == sym)
            if not self.evidence_after(sym, prepared):
                return False
            if self.p_ev[sym][0] != 0 or self.w_ev[sym][0]:
                return False
        return True

    def _maybe_disarm(self, now: datetime) -> None:
        """S8 (6): the disarm is part of the kill-completion transition itself."""
        if self.dry_run or not any(o.reason == "kill" for o in self.operations.values()):
            return
        if self.flatten_complete("kill", now):
            self.dry_run = True
            self._emit("disarmed", at=now.isoformat())

    # ── feed loss / daemon loss (spec S6) ──────────────────────────────────
    def on_flat_intent(self, op_id: str, leg_id: str, now: datetime) -> Operation:
        """The daemon's feed-loss flat; idempotent by operation identity. A resting risk-add
        of the leg is cancelled too — it must not trigger after its source has failed."""
        if op_id not in self.operations:
            for order in self.pending.values():
                if (order.leg_id == leg_id and order.kind in ("entry", "add")
                        and order.status in ("accepted", "sent", "unknown", "partial")
                        and not order.cancel_requested):
                    order.cancel_requested = self.broker.cancel(order.ref).status == "accepted"
                    self._emit("cancel_sent", ref=order.ref, reason="feed_loss")
        op = self.close("leg", leg_id, now, "feed_loss_flat", op_id=op_id)
        self.block("feed", op_id)
        return op

    def record_control_read(self, now: datetime) -> None:
        """R-N: the listener persists the time of every control read."""
        self.last_control_read = now
        self.persist()

    def daemon_loss_check(self, now: datetime) -> list[Operation]:
        """S6 daemon-loss flat: absent timestamp counts as expired."""
        expired = self.last_control_read is None or now - self.last_control_read > STALENESS_WINDOW
        if not expired:
            return []
        ops = []
        for sym in OWNED_SYMBOLS:
            p_state, qty = self.position(sym, now)
            w_state, orders = self.working(sym, now)
            if p_state == "CONFIRMED" and qty == 0 and w_state == "CONFIRMED" and not orders:
                continue
            ops.append(self.close("sym", sym, now, "daemon_loss_flat"))
        if ops:
            self.block("feed", "daemon_loss")
        return ops

    def session_open(self) -> None:
        """R-1: the ``feed`` block clears only at the next session open; ``eod`` likewise."""
        self.unblock("feed")
        self.unblock("eod")

    # ── restart reconciliation (spec S9) ───────────────────────────────────
    def reconcile_restart(self, now: datetime) -> Decision:  # pylint: disable=too-many-branches
        """Requires postdating P and W for every owned symbol; halts on orphans; never
        auto-cancels an orphan of unknown kind; a missing expected protection is a gap."""
        if self.restarted_at is None:
            raise KernelRefusal("not a restarted kernel")
        for sym in OWNED_SYMBOLS:
            if not self.evidence_after(sym, self.restarted_at):
                return Decision(False, "evidence_owed", ref=sym)
        halted = False
        known = set(self.pending) | {r for e in self.expected.values()
                                     for r in e.working.values() if r}
        for sym in OWNED_SYMBOLS:
            working, _ = self.w_ev[sym]
            for order in working:
                if order["ref"] in known or (order.get("attached_to") in self.lots):
                    continue
                self._emit("restart_orphan_order", ref=order["ref"],
                           order_kind=order.get("kind"))
                self.halted_legs.add(LEG_BY_SYMBOL[sym])
                halted = True                              # never auto-cancelled
        for order in self.pending.values():
            if order.status in ("sent", "accepted"):
                terminal = self.status_ev.get(order.ref)
                in_w = any(w["ref"] == order.ref for w in self.w_ev[order.sym][0])
                if terminal is None and not in_w:
                    self._emit("restart_orphan_order", ref=order.ref,
                               order_kind="pending_absent")
                    self.halted_legs.add(order.leg_id)
                    halted = True
        for sym in OWNED_SYMBOLS:
            self._check_expectations(self._latest_evidence(sym))
        self.progress(now)
        if halted or "protection_gap" in self.blocks:
            self.persist()
            return Decision(False, "halted" if halted else "protection_gap")
        self.unblock("restart_unreconciled")
        return Decision(True, "reconciled")

    # ── helpers ────────────────────────────────────────────────────────────
    def _scope(self, scope_kind: str, scope_id: str) -> tuple[str, str | None]:
        if scope_kind == "fill":
            lot = self.lots[scope_id]
            return lot.sym, lot.leg_id
        if scope_kind == "leg":
            return leg_spec(scope_id).symbol, scope_id
        return scope_id, LEG_BY_SYMBOL.get(scope_id)

    def _next(self, prefix: str) -> str:
        self._seq += 1
        return f"{prefix}-{self._seq}"

    def _emit(self, kind: str, **detail) -> None:
        self.telemetry.append({"kind": kind, **detail})

    def events(self, kind: str) -> list[dict]:
        """Telemetry of one kind (tests assert on these)."""
        return [e for e in self.telemetry if e["kind"] == kind]
