"""Listener-side offline kernel of TB-S3 rev7 and KERNEL_CONTRACT.md.

Broker facts arrive through ordered, fenced Evidence. Intent owns individual obligations
and planned effects; the dispatch journal persists before touching the broker. Account-wide
blocks are derived from every unresolved owner. Per-component attempts describe valid
protection transitions. Completion drives required effects, including local kill disarm;
status queries are pure. Store is the versioned durable state used after listener restart.

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

from .broker import (BAR, STALENESS_WINDOW, Clock, Evidence, Execution, FakeBroker,
                     Outcome)
from .provenance import entry_evidence_matches, order_matches
from .acquisition import allocation_error
from .rules import covers, protection_consumed, scope_quiescent, valid_component
from .state import Attempt, Effect, Obligation, UnownedRequest
from .effects import dispatch, planned_command

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
    if (raw.get("trail_activation_ticks") is None) != (raw.get("trail_offset_ticks") is None):
        raise ValueError("trailing protection requires both activation and offset")
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
    lot_ids: set[str] = field(default_factory=set)
    cancel_requested: bool = False
    last_evidence_at: datetime | None = None    # last order-level read that mentioned it
    sent_seq: int = 0
    cancel_effect: str | None = None
    place_effect: str | None = None
    executions_seen: dict[int, Execution] = field(default_factory=dict)
    quarantined: bool = False
    suspect_lots: set[str] = field(default_factory=set)
    suspect_executions: dict[int, Execution] = field(default_factory=dict)
    suspect_symbols: set[str] = field(default_factory=set)
    identity_conflict: bool = False
    history_acquired: int = 0


@dataclass
class Operation:  # pylint: disable=too-many-instance-attributes
    """A durable protection operation (spec §1 ``operations[operation_id]``)."""

    op_id: str
    kind: str                   # CLOSE | AMEND | ATTACH | CANCEL
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
    prepared_seq: int = 0
    sent_seq: int = 0
    components: dict[str, Attempt] = field(default_factory=dict)


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
    obligations: dict[tuple[str, str], Obligation] = field(default_factory=dict)
    evidence: dict[str, Evidence] = field(default_factory=dict)
    position_cursor: dict[str, int] = field(default_factory=dict)
    unowned_requests: dict[str, UnownedRequest] = field(default_factory=dict)
    request_cursor: int = 0
    request_as_of: datetime | None = None
    history_conflicts: set[str] = field(default_factory=set)
    completed_requests: set[str] = field(default_factory=set)
    effects: dict[str, Effect] = field(default_factory=dict)
    restart_seq: int = 0
    effect_hook: Callable | None = None   # deterministic harness crash boundaries
    _in_evidence: bool = False
    _plan_depth: int = 0
    _draining: bool = False
    p_ev: dict[str, tuple[int, datetime]] = field(default_factory=dict)
    w_ev: dict[str, tuple[tuple[dict, ...], datetime]] = field(default_factory=dict)
    lot_ev: dict[str, tuple[int, datetime]] = field(default_factory=dict)
    status_ev: dict[str, tuple[str, datetime]] = field(default_factory=dict)
    dry_run: bool = False
    telemetry: list[dict] = field(default_factory=list)
    restarted_at: datetime | None = None
    halted_legs: set[str] = field(default_factory=set)
    _seq: int = 0

    def completion_actions(self, now: datetime) -> None:
        """Transactional extension point for account completion; primitive status is pure.

        Called after reconciliation and during progress before the final store write.
        Overrides may only plan journaled effects in this same state transaction.
        """

    # ── persistence ────────────────────────────────────────────────────────
    SCHEMA = 6
    PERSISTED = ("pending", "operations", "expected", "lots", "obligations", "p_ev", "w_ev",
                 "lot_ev", "status_ev", "dry_run", "halted_legs", "_seq",
                 "evidence", "position_cursor", "effects", "restart_seq", "unowned_requests",
                 "request_cursor", "request_as_of", "history_conflicts", "completed_requests")

    def persist(self) -> None:
        """Atomic snapshot of every durable state (one write, as the spec requires)."""
        if self._plan_depth:
            return
        snap = {name: copy.deepcopy(getattr(self, name)) for name in self.PERSISTED}
        snap["ledger"] = copy.deepcopy({"confirmed": self.ledger.confirmed,
                                        "reserved": self.ledger.reserved,
                                        "takeover": self.ledger._takeover})
        snap["schema"] = self.SCHEMA
        self.store.data = snap

    def _effect(self, kind: str, owner: str, payload: dict) -> Effect:
        effect = Effect(self._next("effect"), kind, owner, copy.deepcopy(payload))
        self.effects[effect.effect_id] = effect
        if kind == "place":
            self.pending[owner].place_effect = effect.effect_id
        elif kind == "modify":
            op = self.operations[owner]
            component = payload["component"]
            op.components[component] = Attempt(effect.effect_id, op.payload["changes"][component]["fields"])
        elif kind == "cancel" and owner in self.pending:
            self.pending[owner].cancel_effect = effect.effect_id
            self.block("unknown_order", f"cancel:{owner}")
        self.persist()
        self._drain_effects()
        return effect

    def _mark_dispatch(self, effect: Effect) -> None:
        """Record every actual attempt before the route can observe it."""
        if effect.kind == "place":
            self.pending[effect.owner].sent_seq = effect.boundary
            return
        op = self.operations.get(effect.owner)
        if op is None:
            return
        op.sent_seq, op.sent_at = effect.boundary, effect.sent_at
        op.attempts += 1
        op.reconciled_at = None
        if effect.kind == "modify":
            attempt = op.components[effect.payload["component"]]
            attempt.status, attempt.boundary = "dispatching", effect.boundary
            attempt.sent_at = effect.sent_at

    @planned_command(drain=False)
    def _effect_outcome(self, effect: Effect, outcome: Outcome) -> None:
        """Transport outcomes never substitute for broker confirmation."""
        effect.status, effect.outcome = "recorded", outcome.status
        if effect.kind == "place":
            self._apply_send_outcome(self.pending[effect.owner], outcome)
            return
        if effect.kind == "cancel":
            order = self.pending.get(effect.owner)
            if order:
                order.cancel_requested = outcome.status == "accepted"
            op = self.operations.get(effect.owner)
            if op:
                op.status = "sent" if outcome.status == "accepted" else outcome.status
                op.detail = outcome.detail
            self._emit("cancel_sent", ref=effect.payload["ref"], outcome=outcome.status)
            return
        if effect.kind == "disarm":
            if outcome.status == "accepted":
                self.dry_run = True
                self._emit("disarmed", at=self.clock.now.isoformat())
            return
        op = self.operations[effect.owner]
        status = "sent" if outcome.status == "accepted" else outcome.status
        op.status, op.detail = status, outcome.detail
        self._emit("operation_sent", op=op.op_id, outcome=outcome.status)
        if effect.kind == "modify":
            op.components[effect.payload["component"]].status = status
            states = {a.status for a in op.components.values()}
            if "unknown" in states:
                op.status = "unknown"
            elif "rejected" in states and "sent" in states:
                op.status = "partial"
        if effect.kind == "close":
            if status == "rejected":
                self.block("close_rejected", op.op_id)
            else:
                self.block("unknown_order", op.op_id)
        elif status == "unknown":
            self.block("unknown_order", op.op_id)
        if effect.kind == "attach" and status == "rejected":
            exp = self.expected.get(op.scope_id)
            if exp is None and self.lots.get(op.scope_id) and self.lots[op.scope_id].qty == 0:
                op.status, op.detail = "complete", "scope consumed"
                self.unblock("unknown_order", op.op_id)
                return
            if exp is None:
                self.block("protection_gap", f"{op.scope_id}:missing_expectation")
                return
            for component in exp.intended:
                exp.status[component] = "missing"
                self.block("protection_gap", f"{exp.fill_id}:{component}")
            self._emit("protection_gap", fill=exp.fill_id, component="attach")
            self.close("fill", exp.fill_id, self.clock.now, "protection_gap_recovery")

    def _drain_effects(self) -> None:
        if self._in_evidence or self._plan_depth or self._draining:
            return
        self._draining = True
        try:
            while effect := next((e for e in self.effects.values() if self._effect_ready(e)), None):
                dispatch(self, effect)
        finally:
            self._draining = False

    def _effect_ready(self, effect: Effect) -> bool:
        if effect.status != "planned":
            return False
        op = self.operations.get(effect.owner)
        if effect.kind != "modify" or op.status == "complete":
            return True
        if any(a.status in ("unknown", "dispatching") for a in op.components.values()):
            return False
        ev = self.coherent_evidence(op.sym, self.clock.now)
        if ev is None:
            return False
        if self.restarted_at is not None and not covers(
                ev, self.restarted_at, self.restart_seq, self.clock.now):
            return False
        component = effect.payload["component"]
        current = next((w for w in ev.working if w["ref"] == effect.payload["ref"]), None)
        lot = self.lots[op.scope_id]
        if current is None or not valid_component(current, component, {}, op.scope_id,
                                                  self._protection_qty(ev, op.scope_id), lot.side):
            return False
        change = op.payload["changes"][component]
        classified = self._diff({component: change["fields"]}, {component: current}, lot.side)
        return classified is not None and not (
            self.risk_add_blocked and any(c["loosening"] for c in classified.values()))

    @classmethod
    def restart(cls, store: Store, broker: FakeBroker, clock: Clock, now: datetime,
                **kwargs) -> "Kernel":
        """Spec S9: rebuild from the store; nothing is trusted until reconciled."""
        if store.data is None:
            raise KernelRefusal("missing store schema; attended reconciliation required")
        kernel = cls(broker, clock, store=store, **kwargs)
        if store.data is not None:
            if (store.data.get("schema") != cls.SCHEMA
                    or not set(cls.PERSISTED) <= store.data.keys()
                    or not {"confirmed", "reserved", "takeover"}
                    <= store.data.get("ledger", {}).keys()):
                raise KernelRefusal("incompatible store schema; attended reconciliation required")
            for name in cls.PERSISTED:
                setattr(kernel, name, copy.deepcopy(store.data[name]))
            kernel.ledger.confirmed = dict(store.data["ledger"]["confirmed"])
            kernel.ledger.reserved = dict(store.data["ledger"]["reserved"])
            kernel.ledger._takeover = copy.deepcopy(store.data["ledger"]["takeover"])
        kernel.restarted_at = now
        kernel.restart_seq = clock.tick()
        for effect in kernel.effects.values():
            if effect.status == "planned" and effect.kind == "place":
                effect.status = "cancelled"
                order = kernel.pending[effect.owner]
                order.status = "not_sent"
                kernel._release(order)
            elif effect.status == "planned" and effect.kind == "modify":
                op = kernel.operations[effect.owner]
                component = effect.payload["component"]
                if op.payload["changes"][component]["loosening"]:
                    effect.status = "cancelled"
                    op.components[component].status = "rejected"
                    op.status = "rejected"
            elif effect.status == "dispatching":
                kernel._effect_outcome(effect, Outcome("unknown", detail="restart during dispatch"))
        kernel.block("restart_unreconciled", "restart")
        return kernel

    # ── obligations and their derived account-wide blocks ────────────────
    @property
    def blocks(self) -> dict[str, tuple[str, ...]]:
        """Read-only aggregate: every unresolved owner contributes to its reason."""
        return {reason: tuple(sorted(o.owner for o in self.obligations.values()
                                      if o.reason == reason))
                for reason in sorted({o.reason for o in self.obligations.values()})}

    def block(self, reason: str, detail: str = "", *, owner: str | None = None) -> None:
        """Set a sticky account-wide risk-add block."""
        assert reason in BLOCK_REASONS, reason
        owner = owner or detail or reason
        self.obligations[(reason, owner)] = Obligation(reason, owner, detail)
        self._emit(reason, detail=detail)
        self.persist()

    def unblock(self, reason: str, owner: str | None = None) -> None:
        """Only the reason's owner calls this, on confirmed completion."""
        if owner is None and reason in ("unknown_order", "close_rejected", "protection_gap"):
            raise KernelRefusal("an obligation owner is required")
        for key in list(self.obligations):
            if key[0] == reason and (owner is None or key[1] == owner):
                del self.obligations[key]
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

    def evidence_after(self, sym: str, at: datetime, boundary: int = 0) -> bool:
        """True when both position and working-order evidence postdate ``at``."""
        ev = self.coherent_evidence(sym, self.clock.now)
        return bool(ev and covers(ev, at, boundary, self.clock.now))

    def coherent_evidence(self, sym: str, now: datetime) -> Evidence | None:
        """One fresh, full acquisition must support every combined position/order decision."""
        ev = self.evidence.get(sym)
        if (ev and ev.order_level and ev.request_fence and ev.as_of <= now
                and now - ev.as_of <= BAR and ev.acquired == self.position_cursor.get(sym)):
            return ev
        return None

    def _confirmed_position(self, sym: str) -> int:
        return sum(l.qty for l in self.lots.values() if l.sym == sym and l.qty > 0)

    # ── evidence application (the only writer of P, W, pending outcomes, lots) ─
    @planned_command
    def apply_evidence(self, ev: Evidence) -> None:  # pylint: disable=too-many-branches
        """Spec I2: broker evidence alone moves ``P``, ``W``, ``pending`` and the lots."""
        self._sweep_timeouts(self.clock.now)
        previous = self.evidence.get(ev.sym)
        if (ev.acquired <= 0 or not ev.request_fence or ev.as_of > self.clock.now
                or self.clock.now - ev.as_of > BAR
                or (ev.sym in self.p_ev and ev.as_of < self.p_ev[ev.sym][1])
                or (previous and (ev.acquired <= previous.acquired
                                  or ev.as_of < previous.as_of))):
            self._emit("evidence_ignored", sym=ev.sym, acquired=ev.acquired)
            self.persist()
            return
        if ev.acquired > self.position_cursor.get(ev.sym, 0):
            self.p_ev[ev.sym] = (ev.position, ev.as_of)
            self.position_cursor[ev.sym] = ev.acquired
        if not ev.order_level:
            self._reconcile_ownership(ev)
            self.persist()
            return
        # Never use an older full read to settle against a newer position-only view.
        if ev.acquired < self.position_cursor.get(ev.sym, 0):
            self.persist()
            return
        self._observe_unowned_requests(ev)
        error = (allocation_error(ev, previous) or self._global_identity_error(ev)
                 or self._reduction_authority_error(ev))
        if error:
            if error.startswith("identity conflict"):
                self.history_conflicts.add(ev.sym)
            self.block("unknown_order", f"evidence:{ev.sym}")
            self._emit("invalid_acquisition", sym=ev.sym, detail=error)
            for order in self.pending.values():
                authority = self._order_authority(order)
                if order.sym == ev.sym and authority and not entry_evidence_matches(
                        ev, authority, order.executions_seen, order.reserved, order.sent_seq,
                        order.history_acquired):
                    self._quarantine(order, ev)
            return
        if ev.sym in self.history_conflicts:
            self.block("unknown_order", f"evidence:{ev.sym}")
            return
        self.unblock("unknown_order", f"evidence:{ev.sym}")
        self.evidence[ev.sym] = copy.deepcopy(ev)
        self._in_evidence = True
        for effect in list(self.effects.values()):
            outcome = ev.request_outcomes.get(effect.effect_id)
            op = self.operations.get(effect.owner)
            order = self.pending.get(effect.owner)
            sym = op.sym if op else (order.sym if order else None)
            if (sym == ev.sym and effect.boundary < ev.acquired
                    and effect.status == "recorded" and outcome in ("rejected", "unknown")
                    and effect.outcome != outcome):
                self._effect_outcome(effect, Outcome(outcome, detail="broker execution outcome"))
        if ev.order_level:
            self.w_ev[ev.sym] = (ev.working, ev.as_of)
        for ref, status in ev.order_status.items():
            self.status_ev[ref] = (status, ev.as_of)
        for lot_id, open_qty in ev.lots.items():
            self.lot_ev[lot_id] = (open_qty, ev.as_of)
        working_refs = ev.working_refs()
        for order in list(self.pending.values()):
            location = (ev.order_symbols or {}).get(order.ref)
            if ((location is not None and location != order.sym)
                    or (order.sym != ev.sym and (order.ref in working_refs
                        or order.ref in ev.order_facts
                        or any(e.ref == order.ref for e in ev.executions)))):
                self._quarantine(order, ev)
            if order.sym != ev.sym:
                continue
            if (ev.acquired <= order.sent_seq or order.place_effect in ev.pending_requests):
                continue
            status = ev.order_status.get(order.ref)
            authority = self._order_authority(order)
            if (not authority and status is None and order.ref not in ev.order_facts
                    and order.ref not in working_refs and not ev.fills.get(order.ref)
                    and not any(e.ref == order.ref for e in ev.executions)):
                continue  # a dry-run intent never created broker risk
            if not authority or not entry_evidence_matches(
                    ev, authority, order.executions_seen, order.reserved, order.sent_seq,
                    order.history_acquired):
                self._quarantine(order, ev)
            if order.quarantined:
                self._quarantine(order, ev)
                continue
            order.history_acquired = ev.acquired
            filled = ev.fills.get(order.ref, 0)
            if ev.order_level and (status is not None or order.ref in working_refs):
                order.last_evidence_at = ev.as_of
            if filled > order.filled_qty:
                executions = [e for e in ev.executions if e.ref == order.ref
                              and e.execution_id not in order.executions_seen]
                for execution in sorted(executions, key=lambda e: e.execution_id):
                    self._on_fill(order, execution.qty, ev, execution.fill_id)
                order.executions_seen.update((e.execution_id, e) for e in executions)
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
        self._settle_quarantines(release_only=True)
        self._settle_operations(ev)          # all operations use this immutable read
        self._check_expectations(ev)
        self._sync_lots(ev)
        self._settle_quarantines()
        self._reconcile_ownership(ev)
        self._settle_unowned_requests()
        self._maybe_clear_unknown_order()
        self._advance_flat_work(ev)
        self._dispatch_queued(ev.sym, self.clock.now)
        self.completion_actions(ev.as_of)
        self.persist()
        self._in_evidence = False
        self._drain_effects()
        self.persist()

    def _signed_position(self, sym: str) -> int:
        signed = 0
        for lot in self.lots.values():
            if lot.sym == sym:
                signed += lot.qty if lot.side == "buy" else -lot.qty
        return signed

    def _reduction_authority_error(self, ev: Evidence) -> str | None:
        totals: dict[str, int] = {}
        for reduction in ev.reductions:
            effect = self.effects.get(reduction.request_id)
            if effect is None:
                continue  # external executions reduce broker exposure, not our attempt budget
            scope = effect.payload.get("fill_id")
            owner = effect.payload.get("protection_owner")
            if (effect.kind != "close" or not 0 < effect.boundary < reduction.execution_id
                    or effect.payload.get("sym") != reduction.sym
                    or reduction.transition != ("triggered_protection" if owner else "explicit_scope")
                    or owner is not None and reduction.protection_owner != owner
                    or scope is not None and any(i != scope for i, _ in reduction.allocations)):
                return "reduction does not match dispatched authority"
            totals[effect.effect_id] = totals.get(effect.effect_id, 0) + sum(
                qty for _, qty in reduction.allocations)
            budget = effect.payload.get("qty")
            if budget is not None and totals[effect.effect_id] > budget:
                return "reduction exceeds dispatched budget"
        return None

    def _global_identity_error(self, ev: Evidence) -> str | None:
        retained_refs = {ref for prior in self.evidence.values()
                         if prior.acquired < ev.acquired
                         for ref in (prior.order_symbols or {})}
        if not retained_refs <= set(ev.order_symbols or {}):
            return "incomplete retained global order registry"
        ids = {item.execution_id for prior in self.evidence.values() if prior.sym != ev.sym
               for item in (*prior.executions, *prior.reductions)}
        if any(item.execution_id in ids for item in (*ev.executions, *ev.reductions)):
            return "identity conflict: execution ID reused across symbols"
        return None

    @property
    def unresolved_requests(self) -> bool:
        """Unknown future scope prevents account and per-scope quiescence claims."""
        return any(r.status != "resolved" for r in self.unowned_requests.values())

    def _observe_unowned_requests(self, ev: Evidence) -> None:
        """Global fence ordering is independent of each symbol's position/order cursor."""
        if (ev.acquired <= self.request_cursor
                or self.request_as_of is not None and ev.as_of < self.request_as_of):
            return
        self.request_cursor, self.request_as_of = ev.acquired, ev.as_of
        for request_id in ev.pending_requests & self.completed_requests:
            self.block("unknown_order", f"request-conflict:{request_id}")
        self.completed_requests.update(ev.request_outcomes)
        known = {i for i, effect in self.effects.items() if 0 < effect.boundary < ev.acquired}
        observed = ((set(ev.pending_requests) | set(ev.request_outcomes)) - known
                    | {i for i, r in self.unowned_requests.items() if r.status != "resolved"})
        symbols = set(OWNED_SYMBOLS) | set((ev.order_symbols or {}).values())
        for request_id in observed:
            record = self.unowned_requests.setdefault(request_id, UnownedRequest(request_id))
            if request_id in ev.pending_requests and record.completion_seq:
                record.status = "conflict"  # completion is final even before all coverage arrives
            if record.status == "resolved":
                continue  # retained outcome history is a tombstone, not new work
            added_scope = symbols - record.symbols
            record.symbols.update(symbols)
            self.block("unknown_order", f"unowned-request:{request_id}")
            if record.status == "conflict":
                continue
            if request_id in ev.pending_requests:
                record.status = "pending"
                record.completion_seq, record.completed_at = 0, None
            elif record.completion_seq == 0 or added_scope:
                record.status = "covering"
                record.completion_seq, record.completed_at = ev.acquired, ev.as_of
        # A previously observed pending ID may disappear from a complete fence without
        # a transport outcome; its resulting broker facts still require full coverage.
        for record in self.unowned_requests.values():
            if record.status == "pending" and record.request_id not in ev.pending_requests:
                record.status = "covering"
                record.completion_seq, record.completed_at = ev.acquired, ev.as_of

    def _settle_unowned_requests(self) -> None:
        """Transfer future-request ownership to observed broker risk in one atomic transition."""
        resolved = False
        for record in self.unowned_requests.values():
            if record.status != "covering":
                continue
            reads = [self.coherent_evidence(sym, self.clock.now) for sym in record.symbols]
            if any(ev is None or ev.acquired < record.completion_seq
                   or ev.as_of < record.completed_at or ev.order_symbols is None
                   or record.request_id in ev.pending_requests for ev in reads):
                continue
            # These complete acquisitions include the completion fence itself; unlike
            # dispatch boundaries, the same acquisition can prove its own captured facts.
            for ev in reads:
                self._check_expectations(ev)
                self._reconcile_ownership(ev)
            record.status = "resolved"
            self.unblock("unknown_order", f"unowned-request:{record.request_id}")
            resolved = True
        if resolved and not self.unresolved_requests:
            # Finishing account coverage must also finish now-quiescent close owners;
            # no status polling or second evidence delivery is required.
            for op in self.operations.values():
                ev = self.coherent_evidence(op.sym, self.clock.now)
                if (op.kind == "CLOSE" and op.status not in ("complete", "queued") and ev
                        and self._operation_covered(op, ev) and self._scope_flat(op, ev)):
                    self._complete_close(op, ev)

    def _order_authority(self, order: PendingOrder) -> dict | None:
        effect = self.effects.get(order.place_effect)
        return effect.payload if effect else None

    def _quarantine(self, order: PendingOrder, ev: Evidence) -> None:
        """Retain suspect broker exposure without assigning it to an authorized allocation."""
        if not order.quarantined:
            self._emit("order_mismatch", ref=order.ref)
        order.quarantined = True
        order.suspect_symbols.add(order.sym)
        location = (ev.order_symbols or {}).get(order.ref)
        if location:
            order.suspect_symbols.add(location)
        for execution in ev.executions:
            if execution.ref == order.ref:
                if ((execution.execution_id not in order.executions_seen
                     and execution.execution_id <= order.history_acquired)
                        or any(execution.execution_id in preserved
                       and preserved[execution.execution_id] != execution
                       for preserved in (order.executions_seen, order.suspect_executions))):
                    order.identity_conflict = True
                order.suspect_executions.setdefault(execution.execution_id, execution)
                order.suspect_lots.add(execution.fill_id)
                order.suspect_symbols.add(execution.sym)
        candidate = f"{order.ref}#lot"  # the fake broker's explicit one-order/one-lot contract
        if candidate in ev.lots:
            order.suspect_lots.add(candidate)
        if order.lot_id:
            order.suspect_lots.add(order.lot_id)
        self.block("unknown_order", f"mismatch:{order.ref}")

    def _quarantine_terminal_reads(self, order: PendingOrder) -> tuple[list[Evidence], Evidence] | None:
        """Original-symbol absence cannot resolve a ref observed at another broker location."""
        reads = [self.coherent_evidence(sym, self.clock.now) for sym in order.suspect_symbols]
        if not reads or any(ev is None or not covers(ev, order.sent_at, order.sent_seq, self.clock.now)
                            or order.place_effect in ev.pending_requests
                            or order.ref in ev.working_refs() or ev.order_symbols is None
                            for ev in reads):
            return None
        locations = {ev.order_symbols.get(order.ref) for ev in reads}
        if len(locations) != 1:
            return None
        terminal = next((ev for ev in reads if ev.sym in locations
                         and ev.order_status.get(order.ref) in ("filled", "cancelled", "rejected")
                         and ev.order_facts.get(order.ref, {}).get("sym") == ev.sym), None)
        return (reads, terminal) if terminal else None

    def _settle_quarantines(self, release_only: bool = False) -> None:
        for order in self.pending.values():
            if not order.quarantined:
                continue
            proof = self._quarantine_terminal_reads(order)
            if proof is None:
                continue
            reads, terminal = proof
            self._release(order)
            order.status = terminal.order_status[order.ref]
            if release_only:
                continue
            # Compare both preserved histories; suspect identities cannot overwrite trusted ones.
            records = [e for ev in reads for e in ev.executions if e.ref == order.ref]
            history = {e.execution_id: e for e in records}
            history_complete = (len(records) == len(history)
                                and all(history.get(i) == e for preserved in
                                        (order.executions_seen, order.suspect_executions)
                                        for i, e in preserved.items())
                                and sum(e.qty for e in records) == terminal.fills.get(order.ref, 0)
                                and terminal.order_facts[order.ref].get("filled_qty")
                                == terminal.fills.get(order.ref, 0))
            lots = {lot: qty for ev in reads for lot, qty in ev.lots.items()}
            if (not order.identity_conflict and history_complete
                    and all(lots.get(lot) == 0 for lot in order.suspect_lots)
                    and not any(w.get("attached_to") in order.suspect_lots
                                for ev in reads for w in ev.working)
                    and all(ev.position == self._signed_position(ev.sym) for ev in reads)):
                self.unblock("unknown_order", f"mismatch:{order.ref}")

    def _known_order_refs(self, ev: Evidence) -> set[str]:
        known = {r for r, o in self.pending.items() if not o.quarantined and o.sym == ev.sym
                 and self._order_authority(o)
                 and all(order_matches(w, self._order_authority(o)) for w in ev.working
                         if w["ref"] == r)}
        known.update(r for e in self.expected.values() for r in e.working.values() if r)
        known.update(o.target for o in self.operations.values()
                     if o.kind == "CANCEL" and o.status != "complete")
        return known

    def _reconcile_ownership(self, ev: Evidence) -> None:
        """Every observed unowned risk source blocks the account until full evidence resolves it."""
        if ev.acquired != self.position_cursor.get(ev.sym):
            return
        position_owner = f"unallocated:{ev.sym}"
        if ev.position != self._signed_position(ev.sym):
            self.block("unknown_order", position_owner)
        elif ev.order_level:
            self.unblock("unknown_order", position_owner)
        if not ev.order_level:
            return
        prefix = f"unowned-order:{ev.sym}:"
        known = self._known_order_refs(ev)
        owners = {prefix + order["ref"] for order in ev.working if order["ref"] not in known}
        for owner in owners:
            self.block("unknown_order", owner)
        for reason, owner in list(self.obligations):
            if reason == "unknown_order" and owner.startswith(prefix) and owner not in owners:
                self.unblock(reason, owner)
        lot_prefix = f"unowned-lot:{ev.sym}:"
        for lot_id, qty in ev.lots.items():
            lot = self.lots.get(lot_id)
            facts = ev.lot_facts.get(lot_id, {})
            owned = (lot is not None and not self.pending[lot.entry_ref].quarantined
                     and facts.get("entry_ref") == lot.entry_ref and facts.get("side") == lot.side
                     and facts.get("sym") == lot.sym and facts.get("leg_id") == lot.leg_id
                     and qty == lot.qty)
            if qty != 0 and not owned:
                self.block("unknown_order", lot_prefix + lot_id)
            elif qty == 0 or owned:
                self.unblock("unknown_order", lot_prefix + lot_id)

    def _release(self, order: PendingOrder) -> None:
        if order.reserved:
            self.ledger.release_reservation(order.leg_id, order.reserved)
            order.reserved = 0

    def _on_fill(self, order: PendingOrder, delta: int, ev: Evidence, lot_id: str) -> None:
        self.ledger.confirm_fill(order.leg_id, delta)
        order.reserved = max(0, order.reserved - delta)
        lot = self.lots.get(lot_id)
        if lot is None:
            lot = Lot(lot_id, order.leg_id, order.sym, order.side, 0, order.ref, ev.as_of)
            self.lots[lot_id] = lot
        lot.qty += delta
        order.lot_id = lot_id
        order.lot_ids.add(lot_id)
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
            if (lot is None or protection_consumed(ev, exp.fill_id)
                    or ev.as_of < exp.defined_at):
                continue
            for component, params in exp.intended.items():
                choices = [params]
                for op in self.operations.values():
                    attempt = op.components.get(component)
                    if (op.scope_id == exp.fill_id and op.kind == "AMEND" and attempt
                            and attempt.status in ("dispatching", "sent", "unknown")
                            and attempt.boundary < ev.acquired):
                        choices.append(attempt.fields)
                candidates = [w for w in ev.working if w.get("attached_to") == exp.fill_id
                              and w["kind"] == component]
                valid = (len(candidates) == 1 and any(valid_component(
                    candidates[0], component, self._fields(p), exp.fill_id,
                    self._protection_qty(ev, exp.fill_id), lot.side) for p in choices))
                if valid:
                    exp.working[component] = candidates[0]["ref"]
                    exp.status[component] = "working"
                elif exp.status.get(component) != "missing":
                    exp.status[component] = "missing"
                    self.block("protection_gap", f"{exp.fill_id}:{component}")
                    self._emit("protection_gap", fill=exp.fill_id, component=component)
                    self.close("fill", exp.fill_id, ev.as_of, "protection_gap_recovery")

    def _scope_flat(self, op: Operation, ev: Evidence) -> bool:
        """Flat on THIS read: order-level reads only; absent data is never flatness."""
        if self.unresolved_requests:
            return False
        if op.payload.get("transition") == "triggered_protection":
            return (protection_consumed(ev, op.scope_id)
                    and all(self.pending[r].status in ("filled", "cancelled", "rejected", "not_sent")
                            for r in op.payload.get("cancel_refs", []))
                    and self._residual_protected(op, ev))
        return scope_quiescent(ev, op.scope_kind, op.scope_id, self.pending)

    @staticmethod
    def _protection_qty(ev: Evidence, fill_id: str) -> int | None:
        return ev.protection_owners.get(fill_id, {}).get("qty")

    def _close_lot_ids(self, op: Operation) -> set[str]:
        if op.payload.get("qty") is None and op.payload.get("entry_ref") in self.pending:
            return self.pending[op.payload["entry_ref"]].lot_ids | {op.scope_id}
        return {op.scope_id}

    def _operation_covered(self, op: Operation, ev: Evidence) -> bool:
        current = self.coherent_evidence(op.sym, self.clock.now)
        if current is None or current.acquired != ev.acquired:
            return False
        if not covers(ev, op.sent_at or op.prepared_at,
                      max(op.prepared_seq, op.sent_seq), self.clock.now):
            return False
        owners = {op.op_id, *op.payload.get("cancel_refs", [])}
        return not any(e.owner in owners and e.effect_id in ev.pending_requests
                       for e in self.effects.values())

    def quiescent(self, sym: str, now: datetime) -> bool:
        """Shared daemon/listener view of confirmed absence of future exposure."""
        if self.unresolved_requests:
            return False
        ev = self.coherent_evidence(sym, now)
        return bool(ev and scope_quiescent(ev, "sym", sym, self.pending))

    def _settle_operations(self, ev: Evidence) -> None:
        if not ev.order_level:
            return                                        # position-only reads settle nothing
        for op in list(self.operations.values()):
            if (op.sym != ev.sym or op.status in ("complete", "queued")
                    or not self._operation_covered(op, ev)):
                continue
            if op.kind == "CLOSE":
                self._settle_close(op, ev)
            elif op.kind == "CANCEL":
                op.reconciled_at = ev.as_of
                if (ev.order_status.get(op.target) in ("filled", "cancelled", "rejected")
                        and op.target not in ev.working_refs()):
                    entry_cancel = op.payload.get("cancel_kind") in ("entry", "add")
                    if ev.position == 0 or entry_cancel:
                        op.status = "complete"
                        self.unblock("unknown_order", op.op_id)
                        self._emit("cancel_acknowledged" if entry_cancel else "orphan_removed",
                                   ref=op.target)
                    else:
                        self.close("sym", op.sym, ev.as_of, "orphan_cancel_recovery")
            else:
                self._settle_protection_op(op, ev)

    def _settle_close(self, op: Operation, ev: Evidence) -> None:
        attempts = {e.effect_id for e in self.effects.values() if e.owner == op.op_id
                    and e.kind == "close" and 0 < e.boundary < ev.acquired}
        op.payload["closed"] = sum(qty for r in ev.reductions if r.request_id in attempts
                                   for _, qty in r.allocations)
        if self._scope_flat(op, ev):
            self._complete_close(op, ev)
            return
        if op.status not in ("sent", "unknown", "rejected", "partial"):
            return
        before = op.payload.get("last_exposure", self._scope_exposure(op))
        if op.scope_kind == "fill":
            after = sum(ev.lots.get(i, before) for i in self._close_lot_ids(op))
        else:
            after = max(abs(ev.position), sum(ev.lots.values()))
        op.payload["last_exposure"] = after
        if op.status in ("sent", "unknown", "partial") and (
                after < before or op.payload["closed"] > 0):
            op.status = "partial"
            self._emit("operation_outcome", op=op.op_id, status="partial", remaining=after)
        requested = op.payload.get("qty")
        if requested is None and op.status == "sent" and after > 0:
            # A fenced, nonpending full close still owes this observed remainder,
            # even if no pre-dispatch read ever measured the exposure it reduced.
            op.status = "partial"
        if (requested is not None and op.payload.get("closed", 0) >= requested
                and self._residual_protected(op, ev)):
            self._complete_close(op, ev)
        op.reconciled_at = ev.as_of

    def _residual_protected(self, op: Operation, ev: Evidence) -> bool:
        """A bounded reduction is done only with the expected residual protection."""
        if op.payload.get("transition") != "triggered_protection" and self._scope_flat(op, ev):
            return True
        if any(self.pending[r].status not in ("filled", "cancelled", "rejected", "not_sent")
               for r in op.payload.get("cancel_refs", [])):
            return False
        if any(qty > 0 and lot_id not in self.lots for lot_id, qty in ev.lots.items()):
            return False
        for lot_id, lot in self.lots.items():
            if lot.sym != ev.sym or protection_consumed(ev, lot_id):
                continue
            exp = self.expected.get(lot_id)
            if exp is None:
                return False
            for component, params in exp.intended.items():
                attached = [w for w in ev.working if w.get("attached_to") == lot_id
                            and w["kind"] == component]
                if len(attached) != 1 or not valid_component(
                        attached[0], component, self._fields(params), lot_id,
                        self._protection_qty(ev, lot_id), lot.side):
                    return False
        return True

    def _scope_exposure(self, op: Operation) -> int:
        if op.scope_kind == "fill":
            return sum(self.lots[i].qty for i in self._close_lot_ids(op) if i in self.lots)
        ev = self.evidence.get(op.sym)
        return max(abs(self.p_ev.get(op.sym, (0, None))[0]),
                   sum(ev.lots.values()) if ev else 0)

    def _settle_protection_op(self, op: Operation, ev: Evidence) -> None:
        if protection_consumed(ev, op.scope_id):
            op.status, op.detail = "complete", "scope consumed"
            return
        exp = self.expected.get(op.scope_id)
        if exp is None:
            return
        attached = {w["kind"]: w for w in ev.working if w.get("attached_to") == exp.fill_id}
        if op.kind == "AMEND":
            wanted = op.payload.get("changes", {})
            for component, change in wanted.items():
                attempt = op.components.get(component)
                if (attempt and attempt.status in ("sent", "unknown", "dispatching")
                        and covers(ev, attempt.sent_at, attempt.boundary, self.clock.now)
                        and component in attached and valid_component(
                            attached[component], component, change["fields"], op.scope_id,
                            self._protection_qty(ev, op.scope_id), self.lots[op.scope_id].side)):
                    exp.intended[component] = change["intended"]
                    exp.working[component] = attached[component]["ref"]
                    exp.status[component] = "working"
                    attempt.status = "confirmed"
                elif (attempt and attempt.status == "unknown" and component in attached
                      and covers(ev, attempt.sent_at, attempt.boundary, self.clock.now)
                      and attempt.effect_id not in ev.pending_requests
                      and valid_component(attached[component], component,
                                          self._fields(exp.intended[component]), op.scope_id,
                                          self._protection_qty(ev, op.scope_id), self.lots[op.scope_id].side)):
                    attempt.status = "rejected"   # fenced read: no application or pending send
            if all(a.status == "confirmed" for a in op.components.values()):
                op.status = "complete"
            elif any(a.status == "planned" for a in op.components.values()):
                op.status = "unknown" if any(a.status == "unknown" for a in op.components.values()) \
                    else "partial"
            elif not any(a.status in ("sent", "unknown", "dispatching")
                         for a in op.components.values()):
                op.status, op.detail = "rejected", "partial mutation; reissue remaining components"
            op.reconciled_at = ev.as_of
            return
        if all(c in attached and valid_component(attached[c], c, self._fields(p),
                                                op.scope_id, self._protection_qty(ev, op.scope_id),
                                                self.lots[op.scope_id].side)
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

    def _sync_lots(self, ev: Evidence) -> None:
        for lot_id, open_qty in ev.lots.items():
            lot = self.lots.get(lot_id)
            if lot is not None and lot.sym == ev.sym:
                order = self.pending[lot.entry_ref]
                if open_qty > lot.qty or open_qty < 0:
                    self._quarantine(order, ev)
                elif not order.quarantined or open_qty == 0:
                    lot.qty = open_qty
                if protection_consumed(ev, lot_id):
                    self.expected.pop(lot_id, None)
        for leg_id in {l.leg_id for l in self.lots.values() if l.sym == ev.sym}:
            qty = sum(l.qty for l in self.lots.values() if l.leg_id == leg_id)
            if self.ledger.confirmed.get(leg_id) != qty:
                self.ledger.confirm_position(leg_id, qty)

    def _complete_close(self, op: Operation, ev: Evidence) -> None:
        op.status = "complete"
        self.unblock("unknown_order", op.op_id)
        self.unblock("close_rejected", op.op_id)
        if self._scope_flat(op, ev):
            for key in list(self.obligations):
                if key[0] == "protection_gap":
                    fill_id = key[1].rsplit(":", 1)[0]
                    if scope_quiescent(ev, "fill", fill_id, self.pending):
                        self.unblock(*key)
        self._emit("close_complete", op=op.op_id, reason=op.reason)

    def _maybe_clear_unknown_order(self) -> None:
        for key in list(self.obligations):
            if key[0] != "unknown_order":
                continue
            owner = key[1]
            if owner in self.pending and self.pending[owner].status != "unknown":
                self.unblock(*key)
            elif owner.startswith("cancel:"):
                order = self.pending.get(owner[7:])
                if order and order.status in ("filled", "cancelled", "rejected"):
                    self.unblock(*key)
            elif owner in self.operations:
                op = self.operations[owner]
                if op.status == "complete" or (op.kind == "AMEND"
                        and op.reconciled_at is not None
                        and not any(a.status in ("unknown", "dispatching")
                                    for a in op.components.values())):
                    self.unblock(*key)

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

    def _entry_refusal(self, intent: OrderIntent, now: datetime) -> Decision | None:
        """Common admission checks for ordinary requests and takeover settlement."""
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
        try:
            components_of(intent.bracket)
        except ValueError as exc:
            return self._refuse("invalid_bracket", str(exc))
        missing = sorted(i for i in self._required_l2(intent.leg_id, intent)
                         if not self.broker.supports(i))
        if missing:
            return self._refuse("l2_refused", ",".join(missing))
        if self.coherent_evidence(sym, now) is None:
            return self._refuse("unknown_state", sym)
        return None

    def admit_entry(self, intent: OrderIntent, now: datetime) -> Decision:
        """Spec S1 (5)–(6): admission in the frozen order, then send; I4 sizing authority."""
        refusal = self._entry_refusal(intent, now)
        if refusal:
            return refusal
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
        result = self._plan_place(intent, qty, now)
        if isinstance(result, Decision):
            return result
        return Decision(result.outcome == "accepted", result.outcome or "planned", ref=result.owner)

    @planned_command
    def _plan_place(self, intent: OrderIntent, qty: int, now: datetime) -> Effect | Decision:
        """Persist reservation, pending order and dispatch intent in one recoverable write."""
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
        effect = self._effect("place", ref, dict(sym=spec.symbol, leg_id=intent.leg_id,
                             kind=intent.kind, side=intent.side.value, qty=qty,
                             order_type=intent.order_type, price=intent.price,
                             bracket=bracket_dict(intent.bracket), ref=ref))
        self.persist()
        return effect

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


    # ── CLOSE (spec §1 primitive) ──────────────────────────────────────────
    @planned_command
    def close(self, scope_kind: str, scope_id: str, now: datetime, reason: str,
              op_id: str | None = None, qty: int | None = None,
              transition: str = "explicit_scope", trigger_bracket: dict | None = None) -> Operation:
        """Prepare a durable close; send only when postdating evidence does not show it flat.
        Overlapping scopes serialize: one close in flight per symbol, later ones queue."""
        if transition not in ("explicit_scope", "triggered_protection"):
            raise KernelRefusal("unknown close transition")
        if transition == "triggered_protection" and (scope_kind != "fill" or not trigger_bracket):
            raise KernelRefusal("trigger requires an identified owner and issued bracket")
        if transition == "explicit_scope" and trigger_bracket is not None:
            raise KernelRefusal("ambiguous close transition")
        if (scope_kind not in ("fill", "leg", "sym")
                or qty is not None and (scope_kind != "fill" or type(qty) is not int or qty <= 0)):
            raise KernelRefusal("bounded CLOSE requires an explicit fill and positive quantity")
        if op_id and op_id in self.operations:
            previous = self.operations[op_id]
            if (previous.kind, previous.scope_kind, previous.scope_id, previous.reason,
                    previous.payload.get("qty"), previous.payload.get("transition", "explicit_scope"),
                    previous.payload.get("trigger_bracket")) != (
                        "CLOSE", scope_kind, scope_id, reason, qty, transition, trigger_bracket):
                raise KernelRefusal("operation identity conflicts with durable demand")
            return previous
        self._sweep_timeouts(now)
        sym, leg_id = self._scope(scope_kind, scope_id)
        for other in self.operations.values():
            if (other.sym == sym and other.kind == "CLOSE" and other.scope_id == scope_id
                    and other.scope_kind == scope_kind and other.reason == reason
                    and other.payload.get("qty") == qty
                    and other.payload.get("transition", "explicit_scope") == transition
                    and other.payload.get("trigger_bracket") == trigger_bracket
                    and (op_id is None or other.op_id == op_id)
                    and other.status in ("prepared", "queued", "rejected", *UNRESOLVED)):
                return other                          # idempotent by scope (retry path)
        op = Operation(op_id or self._next("op"), "CLOSE", scope_kind, scope_id, sym, leg_id,
                       reason, prepared_at=now, prepared_seq=self.clock.tick(),
                       payload={"qty": qty, "transition": transition,
                                "trigger_bracket": trigger_bracket})
        if scope_kind == "fill":
            op.payload["entry_ref"] = self.lots[scope_id].entry_ref
        self.operations[op.op_id] = op
        self.block("unknown_order", op.op_id)
        self._emit("operation_prepared", op=op.op_id, reason=reason)
        self.persist()
        if not (self.broker.supports("d") and self.broker.supports("e")):
            op.status, op.detail = "refused", "route lacks L2(d)/(e)"
            self.block("close_rejected", f"{op.op_id}:capability", owner=op.op_id)
            return op
        # Persist every cancellation and the close before any member can dispatch.
        already_deferring = self._in_evidence
        self._in_evidence = True
        resting = [o for o in self.pending.values() if o.sym == sym
                   and (scope_kind != "fill" or scope_id in o.lot_ids)
                   and o.status not in ("filled", "cancelled", "rejected", "not_sent")]
        op.payload["cancel_refs"] = [o.ref for o in resting]
        self.persist()
        for order in resting:
            if order.cancel_effect is None:
                self.cancel(order.ref, now)
        if any(o is not op and o.sym == sym and o.kind == "CLOSE" and o.status in UNRESOLVED
               for o in self.operations.values()):
            op.status = "queued"                      # never dropped: dispatched in turn
            self._emit("operation_queued", op=op.op_id)
        else:
            self._progress_one(op, now)
        self.persist()
        self._in_evidence = already_deferring
        if not already_deferring:
            self._drain_effects()
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
        self._drain_effects()
        self.completion_actions(now)
        self.persist()
        self._drain_effects()

    def _dispatch_queued(self, sym: str, now: datetime) -> None:
        if any(o.sym == sym and o.kind == "CLOSE" and o.status in UNRESOLVED
               and not self._reduction_executed(o)
               for o in self.operations.values()):
            return
        for op in list(self.operations.values()):
            if op.sym == sym and op.kind == "CLOSE" and op.status == "queued":
                op.status = "prepared"
                self._progress_one(op, now)
                if op.status in UNRESOLVED:
                    return                            # one in flight per symbol

    @staticmethod
    def _reduction_executed(op: Operation) -> bool:
        """A fenced bounded attempt can owe protection but cannot execute more quantity."""
        qty = op.payload.get("qty")
        return (qty is not None and op.reconciled_at is not None
                and op.payload.get("closed", 0) >= qty)

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
        if self.evidence_after(op.sym, op.prepared_at, op.prepared_seq):
            ev = self._latest_evidence(op.sym)
            if self._scope_flat(op, ev):
                self._complete_close(op, ev)
                self._emit("close_noop", op=op.op_id)
                return
        self._send_close(op, now)

    def cancel(self, ref: str, now: datetime) -> Decision:
        """Spec S4: a cancel is classified by the listener from ``pending`` and fresh ``W``."""
        result = self._plan_cancel(ref, now)
        if isinstance(result, Decision):
            return result
        return Decision(result.outcome == "accepted", result.outcome or "planned", ref=ref,
                        op=self.operations.get(result.owner))

    @planned_command
    def _plan_cancel(self, ref: str, now: datetime) -> Effect | Decision:
        """Persist the cancellation owner and effect together; report after dispatch."""
        order = self.pending.get(ref)
        if order is not None and not order.quarantined and order.kind in ("entry", "add"):
            if order.cancel_effect:
                prior = self.effects[order.cancel_effect]
                ev = self.evidence.get(order.sym)
                retryable = (prior.outcome == "unknown" and ev
                             and covers(ev, prior.sent_at, prior.boundary, now)
                             and prior.effect_id not in ev.pending_requests)
                if prior.outcome != "rejected" and not retryable:
                    return Decision(False, "cancel_pending", ref=ref)
            effect = self._effect("cancel", ref, {"ref": ref})
            self.persist()
            return effect
        # Fresh W can classify an external entry/add; protective removal also requires flatness.
        sym = next((w_sym for w_sym, (orders, _) in self.w_ev.items()
                    if any(w["ref"] == ref for w in orders)), None)
        if sym is None:
            return self._refuse("cancel_unknown_ref", ref)
        ev = self.coherent_evidence(sym, now)
        if ev is None:
            return self._refuse("protective_cancel_refused", ref)
        target = next(w for w in ev.working if w["ref"] == ref)
        cancel_kind = target.get("kind")
        if cancel_kind not in ("entry", "add", "stop", "limit", "trail"):
            return self._refuse("cancel_unknown_kind", ref)
        if cancel_kind not in ("entry", "add") and (ev.position != 0 or any(ev.lots.values())):
            return self._refuse("protective_cancel_refused", ref)
        op = next((o for o in self.operations.values() if o.kind == "CANCEL"
                   and o.target == ref and o.status != "complete"), None)
        if op:
            ev = self.evidence.get(sym)
            if (op.status not in ("rejected", "unknown") or ev is None
                    or not self._operation_covered(op, ev)):
                return Decision(False, "cancel_pending", ref=ref, op=op)
        else:
            op = Operation(self._next("op"), "CANCEL", "sym", sym, sym, LEG_BY_SYMBOL[sym],
                           "orphan_cancel", prepared_at=now, prepared_seq=self.clock.tick(),
                           target=ref, payload={"cancel_kind": cancel_kind})
            self.operations[op.op_id] = op
            self.block("unknown_order", op.op_id)
        return self._effect("cancel", op.op_id, {"ref": ref})


    def _latest_evidence(self, sym: str) -> Evidence:
        return self.evidence[sym]

    def _send_close(self, op: Operation, now: datetime) -> None:
        del now
        op.payload["last_exposure"] = self._scope_exposure(op)
        payload = {"sym": op.sym}
        if op.payload.get("transition") == "triggered_protection":
            payload.update(protection_owner=op.scope_id, bracket=op.payload["trigger_bracket"],
                           qty=op.payload["qty"])
            op.status = "sent"
            self._effect("close", op.op_id, payload)
            return
        if op.scope_kind == "fill":
            qty = op.payload.get("qty")
            if qty is not None:
                qty = max(0, qty - op.payload.get("closed", 0))
            target = next((i for i in sorted(self._close_lot_ids(op))
                           if self.lots.get(i) and self.lots[i].qty > 0), op.scope_id)
            payload.update(fill_id=target, qty=qty)
        op.status = "sent"
        self._effect("close", op.op_id, payload)

    def retry(self, op_id: str, now: datetime) -> Operation:
        """Resubmit a rejected, unknown or partial close only after reconciliation on
        postdating evidence — never blindly; a rejected close at most once per bar."""
        op = self.operations[op_id]
        if op.kind != "CLOSE":
            raise KernelRefusal("retry requires a CLOSE operation")
        if op.status not in ("rejected", "unknown", "partial"):
            raise KernelRefusal(f"{op_id} is {op.status}")
        if self._reduction_executed(op):
            raise KernelRefusal("reduction already executed; residual protection recovery owed")
        if (op.reconciled_at is None or op.sym not in self.evidence
                or not self._operation_covered(op, self.evidence[op.sym])):
            raise KernelRefusal("reconcile on postdating evidence before resubmitting")
        if op.status == "rejected" and op.sent_at is not None and now - op.sent_at < BAR:
            raise KernelRefusal("a rejected close is retried at most once per bar")
        op.reconciled_at = None
        self._send_close(op, now)
        self.persist()
        return op

    # ── AMEND / ATTACH (spec §1 primitives) ────────────────────────────────
    def amend_action(self, fill_id: str, bracket: Bracket | dict, now: datetime) -> str | None:
        """Pure action classification for the daemon, using the listener's same direction rule."""
        lot = self.lots.get(fill_id)
        ev = self.coherent_evidence(lot.sym, now) if lot else None
        if (lot is None or ev is None or protection_consumed(ev, fill_id)
                or lot.qty == 0 and not self._protection_qty(ev, fill_id)):
            return None
        exp = self.expected.get(fill_id)
        if exp is None or exp.is_bare:
            return "attach"
        ev = self.coherent_evidence(lot.sym, now)
        if ev is None:
            return None
        current = {w["kind"]: w for w in ev.working if w.get("attached_to") == fill_id}
        try:
            new = components_of(bracket)
        except ValueError:
            return None
        if set(exp.intended) - set(new):
            return None
        if any(c not in current for c in new):
            return None
        changes = self._diff(new, current, lot.side)
        if changes is None:
            return None
        return "loosening_amend" if any(c["loosening"] for c in changes.values()) else "tightening_amend"

    def amend(self, fill_id: str, bracket: Bracket | dict, now: datetime) -> Decision:
        """The port re-issued its bracket for a lot: component-wise modify, or first attach."""
        self._sweep_timeouts(now)
        lot = self.lots.get(fill_id)
        ev = self.coherent_evidence(lot.sym, now) if lot else None
        if (lot is None or ev is not None and protection_consumed(ev, fill_id)
                or lot.qty == 0 and (ev is None or not self._protection_qty(ev, fill_id))):
            return self._refuse("amend_no_lot", fill_id)
        exp = self.expected.setdefault(fill_id, Expectation(fill_id, lot.sym, lot.leg_id, {}))
        unresolved = [o for o in self.operations.values()
                      if o.scope_id == fill_id and (o.status in UNRESOLVED or any(
                          e.owner == o.op_id and e.status == "planned" for e in self.effects.values()))]
        if unresolved:
            return self._refuse("amend_deferred", f"operation {unresolved[0].op_id} unresolved")
        try:
            new = components_of(bracket)
        except ValueError as exc:
            return self._refuse("invalid_bracket", str(exc))
        if set(exp.intended) - set(new):
            return self._refuse("component_removal_refused", "replacement would remove protection")
        if exp.is_bare:
            return self._attach(exp, new, now)
        ev = self.coherent_evidence(lot.sym, now)
        last_op = max((o.sent_at or o.prepared_at for o in self.operations.values()
                       if o.scope_id == fill_id and o.sent_at), default=None)
        if ev is None or (last_op is not None and ev.as_of < last_op):
            return self._refuse("amend_deferred", "W unknown; reconcile before modifying")
        if not self.broker.supports("c"):
            return self._refuse("l2_refused", "c")
        current = {w["kind"]: w for w in ev.working if w.get("attached_to") == fill_id}
        if any(c not in current for c in new):
            return self._refuse("amend_deferred", "target absent from fresh W")
        changes = self._diff(new, current, lot.side)
        if changes is None:
            return self._refuse("amend_deferred", "trail parameters change would reset the anchor")
        if not changes:
            return Decision(True, "unchanged")
        if any(c["loosening"] for c in changes.values()) and self.risk_add_blocked:
            return self._refuse("policy_block", "loosening amend under a block")
        op = self._plan_amend(lot, changes, current, now)
        return Decision(op.status == "sent", op.status, op=op)

    @planned_command
    def _plan_amend(self, lot: Lot, changes: dict, current: dict, now: datetime) -> Operation:
        """Journal every changed component before any dispatch; unknown siblings wait for evidence."""
        op = Operation(self._next("op"), "AMEND", "fill", lot.fill_id, lot.sym, lot.leg_id, "amend",
                       prepared_at=now, prepared_seq=self.clock.tick(), payload={"changes": changes})
        self.operations[op.op_id] = op
        self.persist()
        for component, change in changes.items():
            ref = current[component]["ref"]
            op.target = ref
            self._effect("modify", op.op_id,
                         {"ref": ref, "component": component, **change["fields"]})
        self.persist()
        return op

    def _diff(self, new: dict, current: dict, side: str):
        changes: dict[str, dict] = {}
        for component, params in new.items():
            old = ({key: current[component].get(key) for key in params}
                   if component in current else None)
            if old == params:
                continue                                  # unchanged: never re-sent
            if component == "trail":
                live = current.get("trail")
                if self.broker.modify_resets_trail_anchor:
                    # An inactive trail can activate between the read and route execution.
                    return None
                if (not live or live.get("trail_activation") is None
                        or live.get("trail_offset") is None
                        or params.get("trail_offset") is None):
                    return None
                loosening = (params["trail_activation"] > live["trail_activation"]
                             or params["trail_offset"] > live["trail_offset"])
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
        required = {"f", "g"} if "trail" in components else {"f"}
        missing = sorted(item for item in required if not self.broker.supports(item))
        if missing:
            return self._refuse("l2_refused", ",".join(missing))
        effect = self._plan_attach(exp, components, now)
        return Decision(effect.outcome == "accepted", effect.outcome or "planned",
                        op=self.operations[effect.owner])

    @planned_command
    def _plan_attach(self, exp: Expectation, components: dict[str, dict], now: datetime) -> Effect:
        """Commit the first defined protection, its owner and its send intent together."""
        exp.define(components, now)                       # intended before send
        op = Operation(self._next("op"), "ATTACH", "fill", exp.fill_id, exp.sym, exp.leg_id,
                       "attach", prepared_at=now, prepared_seq=self.clock.tick(),
                       payload={"components": components})
        self.operations[op.op_id] = op
        self.persist()
        effect = self._effect("attach", op.op_id,
                              {"fill_id": exp.fill_id, "bracket": self._bracket_from(components)})
        self.persist()
        return effect

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
            if qty is not None:
                raise KernelRefusal("bounded exit requires an explicit fill")
            return self.close("leg", leg_id, now, "exit")
        lot = self.lots[fill_id]
        if qty is not None and qty > lot.qty:
            self._emit("exit_qty_clamped", fill=fill_id, requested=qty, clamped=lot.qty)
            qty = lot.qty
        return self.close("fill", fill_id, now, "exit", qty=qty)

    # ── EOD and kill (spec S7, S8) ─────────────────────────────────────────





    def _advance_flat_work(self, ev: Evidence) -> None:
        """A broad flat retains ownership of fills racing cancellation until quiescent."""
        for op in list(self.operations.values()):
            if (op.kind != "CLOSE" or op.payload.get("qty") is not None or op.sym != ev.sym
                    or op.status not in ("sent", "partial") or op.reconciled_at is None):
                continue
            # A previously dispatched all-scope close observed before a late entry fill
            # must close that new exposure. Rejected/unknown outcomes remain attended.
            if self._scope_exposure(op) > 0 and op.payload.get("cancel_refs"):
                self._send_close(op, self.clock.now)

    # ── feed loss / daemon loss (spec S6) ──────────────────────────────────




    # ── restart reconciliation (spec S9) ───────────────────────────────────
    def reconcile_restart(self, now: datetime) -> Decision:  # pylint: disable=too-many-branches
        """Requires postdating P and W for every owned symbol; halts on orphans; never
        auto-cancels an orphan of unknown kind; a missing expected protection is a gap."""
        if self.restarted_at is None:
            raise KernelRefusal("not a restarted kernel")
        for sym in OWNED_SYMBOLS:
            if not self.evidence_after(sym, self.restarted_at, self.restart_seq):
                return Decision(False, "evidence_owed", ref=sym)
        halted = False
        for sym in OWNED_SYMBOLS:
            known = self._known_order_refs(self.evidence[sym])
            working, _ = self.w_ev[sym]
            if self.p_ev[sym][0] != self._signed_position(sym):
                self.halted_legs.add(LEG_BY_SYMBOL[sym])
                self._emit("restart_unallocated_exposure", sym=sym)
                halted = True
            for order in working:
                if order["ref"] in known:
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
        if self.unresolved_requests:
            return Decision(False, "external_requests_owed")
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
