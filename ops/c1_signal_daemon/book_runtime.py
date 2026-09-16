"""Durable completed-bar coordinator for the fixed four-leg book.

The coordinator is deliberately transport-free.  It records one complete bar
boundary and its deterministic action batch through :class:`BookAccountOwner`
before asking that owner to dispatch anything.  Recovery replays retained bars
and confirmed feedback only; it never resends a broker command.
"""
from __future__ import annotations

from dataclasses import asdict, replace
from datetime import datetime, timedelta, timezone
from enum import Enum
import threading
from uuid import uuid4

from c1_rail.book_policy import BOOK_LEGS, is_protected
from c1_rail.book_account_owner import AccountOwnerError, BookAccountOwner
from c1_rail.c1_rail_listener import handle_book_action
from c1_signal_daemon.book_adapters import AdapterRegistry
from c1_signal_daemon.book_protocol import ExecutionEvent, Fill, Mode, OrderIntent
from c1_signal_daemon.feed import Bar
from c1_signal_daemon.book_validation import InputViolation, validate_action, validate_bar


BAR_PERIOD = timedelta(minutes=15)
BAR_SLACK = timedelta(seconds=30)
LEG_ORDER = tuple(row.leg_id for row in sorted(BOOK_LEGS, key=lambda row: row.priority))
_LEG_RANK = {leg_id: index for index, leg_id in enumerate(LEG_ORDER)}


class SimulatedRuntimeCrash(RuntimeError):
    """Test seam representing process loss after an owner commit."""


def _jsonable(value):
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    return value


def _bar_body(bars):
    return {leg_id: _jsonable(asdict(bars[leg_id])) for leg_id in LEG_ORDER}


def _action_body(action):
    return {"type": type(action).__name__, "value": _jsonable(asdict(action))}


def _retained_action(body):
    from c1_signal_daemon.book_protocol import Bracket, BracketAmend, Cancel, OrderIntent, Side, FillTiming
    value = dict(body["value"])
    if value.get("bracket") is not None:
        value["bracket"] = Bracket(**value["bracket"])
    if value.get("scope_fill_ids") is not None:
        value["scope_fill_ids"] = tuple(value["scope_fill_ids"])
    if body["type"] == "OrderIntent":
        value["side"] = Side(value["side"])
        value["timing"] = FillTiming(value["timing"])
        if value.get("bar_time") is not None:
            value["bar_time"] = datetime.fromisoformat(value["bar_time"])
    return {"OrderIntent": OrderIntent, "BracketAmend": BracketAmend, "Cancel": Cancel}[body["type"]](**value)


def _bar(data):
    return Bar(datetime.fromisoformat(data["ts"]), data["open"], data["high"],
               data["low"], data["close"], data["volume"])


def _feedback(data):
    fill_data = data.get("fill")
    fill = None
    if fill_data is not None:
        from c1_signal_daemon.book_protocol import Side
        fill = Fill(
            fill_data["fill_id"], fill_data["order_id"], fill_data["leg_id"],
            fill_data["kind"], Side(fill_data["side"]), fill_data["qty"],
            fill_data["price"], datetime.fromisoformat(fill_data["bar_time"]),
            fill_data.get("entry_fill_id"), fill_data.get("commission", 0.0),
            fill_data.get("reason", ""),
        )
    return ExecutionEvent(data["event"], data["leg_id"],
                          datetime.fromisoformat(data["bar_time"]), fill,
                          data.get("order_id"), data.get("detail", ""))


class FourLegRuntime:
    """One deterministic barrier for four adapters and one account owner."""

    def __init__(self, owner, adapters, *, crash_after_dispatch=False):
        if not isinstance(owner, BookAccountOwner):
            raise TypeError("BookAccountOwner required")
        if not isinstance(adapters, AdapterRegistry) or set(adapters) != set(LEG_ORDER):
            raise ValueError("exact four-leg adapter registry required")
        if any(getattr(adapters[leg_id], "leg_id", None) != leg_id for leg_id in LEG_ORDER):
            raise ValueError("adapter registry identity mismatch")
        self.owner = owner
        self.adapters = adapters
        owner.register_runtime_actor(
            kind=adapters.kind, runtime_identities=adapters.runtime_identities,
            effective_inputs_sha256=adapters.effective_inputs_sha256)
        self.crash_after_dispatch = bool(crash_after_dispatch)
        self._application_lock = threading.RLock()
        self._pending = {}
        # Only boundaries prepared by this runtime may continue. Recovery never
        # restores this set, even when the retained batch is awaiting evidence.
        self._prepared_here = set()
        self._mode = None
        partials = owner.retained_partial_bars
        self._validate_retained_chronology(partials)
        for retained in partials:
            instant = datetime.fromisoformat(retained["bar_time"])
            self._pending.setdefault(instant, {})[retained["leg_id"]] = self._validated_retained_bar(
                retained["body"], boundary=instant, leg_id=retained["leg_id"])

    def _validate_retained_chronology(self, partials):
        sessions = self.owner.retained_sessions
        boundaries = {session_id: set() for session_id in sessions}
        try:
            for retained in self.owner.retained_barriers:
                times = boundaries[retained["session_id"]]
                instant = datetime.fromisoformat(retained["bar_time"])
                if instant in times:
                    raise ValueError("duplicate retained boundary instant")
                times.add(instant)
            partial_times = set()
            partial_identities = set()
            for retained in partials:
                instant = datetime.fromisoformat(retained["bar_time"])
                identity = (instant, retained["leg_id"])
                if identity in partial_identities:
                    raise ValueError("duplicate retained partial identity")
                partial_identities.add(identity)
                # Live ingestion uses canonical UTC keys. The owner's promotion
                # and expiry transactions match those persisted keys as text.
                if (instant.utcoffset() is None or retained["bar_time"]
                        != instant.astimezone(timezone.utc).isoformat()):
                    raise ValueError("retained partial key cannot resume in UTC")
                partial_times.add(instant)
            for instant in partial_times:
                matches = [session_id for session_id, session in sessions.items()
                           if datetime.fromisoformat(session["opens_at"]) <= instant
                           < datetime.fromisoformat(session["closes_at"])]
                if len(matches) != 1:
                    raise ValueError("partial has no unique session")
                times = boundaries[matches[0]]
                if instant in times:
                    raise ValueError("partial duplicates retained boundary instant")
                times.add(instant)
            for session_id, times in boundaries.items():
                expected = datetime.fromisoformat(sessions[session_id]["opens_at"])
                close = datetime.fromisoformat(sessions[session_id]["closes_at"])
                for instant in sorted(times):
                    if instant != expected or instant >= close:
                        raise ValueError("retained history skips a boundary")
                    expected += BAR_PERIOD
        except (KeyError, TypeError, ValueError):
            self.owner.halt("retained-bar-sequence", "barrier", now=self.owner.binding["as_of"])
            raise AccountOwnerError("noncontiguous retained bar boundary") from None

    def _validated_retained_bar(self, data, *, boundary, leg_id):
        try:
            bar = _bar(data)
            violation = validate_bar(bar)
            if violation is None and bar.ts != boundary:
                violation = InputViolation("boundary_identity", "ts")
        except (KeyError, TypeError, ValueError, AttributeError):
            violation = InputViolation("type", "bar")
        if type(leg_id) is not str or leg_id not in _LEG_RANK:
            violation = InputViolation("known_identity", "leg_id")
        if violation is not None:
            self.owner.record_input_incident("input:retained:" + boundary.isoformat(),
                violation, source="replay", now=self.owner.binding["as_of"])
            raise AccountOwnerError("invalid retained bar")
        return bar

    @property
    def pending_feedback(self):
        return self.owner.pending_feedback

    @property
    def pending_bar_times(self):
        return tuple(sorted(self._pending))

    def _desired_mode(self):
        settlement = self.owner.binding["settlement"]
        return Mode.PROTECTED if is_protected(
            settlement.equity, settlement.peak, self.owner.binding["policy"]
        ) else Mode.NORMAL

    def _validated_actions(self, actions, *, boundary, source, now, leg_id=None):
        violation = None
        ordinal = "container"
        if type(actions) not in (list, tuple):
            violation = InputViolation("container", "actions")
        else:
            for index, action in enumerate(actions):
                violation = validate_action(action)
                if violation is None and leg_id is not None and action.leg_id != leg_id:
                    violation = InputViolation("source_identity", "leg_id")
                if (violation is None and isinstance(action, OrderIntent)
                        and action.bar_time != boundary):
                    violation = InputViolation("boundary_identity", "bar_time")
                if violation is not None:
                    ordinal = str(index)
                    break
        if violation is not None:
            identity = "input:" + self.owner.binding["session"].session_id + ":" + boundary.isoformat() + ":" + source + ":" + ordinal
            self.owner.record_input_incident(identity, violation, source=source, now=now)
            raise AccountOwnerError("invalid adapter output: " + violation.code + ":" + violation.field)
        return actions

    def _mode_actions(self, mode, *, boundary=None, now=None):
        if not isinstance(mode, Mode):
            raise ValueError("typed protection mode required")
        # Direct mode application has no completed-bar occurrence identity.
        now = now if now is not None else self.owner.binding["as_of"]
        boundary = boundary if boundary is not None else now
        actions = []
        if mode != self._mode:
            for leg_id in LEG_ORDER:
                actions.extend(self._validated_actions(self.adapters[leg_id].set_mode(mode),
                    boundary=boundary, source="set_mode:" + leg_id, now=now, leg_id=leg_id))
            self._mode = mode
        return actions

    @staticmethod
    def _sort_actions(actions):
        # Risk reductions/cancels are serialized before risk-add; within a class
        # the accepted D-B8 leg priority chooses the capacity winner. Entry
        # precedes add only as a same-leg tie-break, never across leg priority.
        class_rank = {"exit": 0, "flat": 0, "Cancel": 0, "BracketAmend": 1,
                      "entry": 2, "add": 2}
        subtype_rank = {"entry": 0, "add": 1}
        return sorted(actions, key=lambda action: (
            class_rank.get(getattr(action, "kind", type(action).__name__), 9),
            _LEG_RANK[action.leg_id],
            subtype_rank.get(getattr(action, "kind", type(action).__name__), 0),
            getattr(action, "order_id", "") or "",
        ))

    def _deliver_events(self, events):
        for event in events:
            self.adapters[event.leg_id].on_execution(event)
            fact_id = event.fill.fill_id if event.fill else next(
                fact for fact, raw in self.owner.pending_feedback
                if raw.get("order_id") == event.order_id)
            self.owner.commit_feedback(
                fact_id, self.adapters[event.leg_id].checkpoint(), now=event.bar_time)

    def _deliver(self, result):
        self._deliver_events(result.confirmed_events)

    def _retain_local_refusal(self, action, result, *, now, boundary_time=None):
        reason = result.refusal_reason
        if reason is None or reason in ("takeover_pending", "duplicate_operation", "awaiting_evidence", "close_pending"):
            return ()
        if any(event.event == "reject" and event.order_id == result.operation_id
               for event in result.confirmed_events):
            return ()
        return self.owner.record_local_refusal(action, reason, now=now,
                                               operation_id=result.operation_id,
                                               boundary_time=boundary_time)

    def deliver_confirmed(self, result):
        """Deliver owner-committed broker facts to adapters and checkpoint them."""
        with self._application_lock:
            self._deliver(result)

    def deliver_confirmed_events(self, events):
        """Deliver an asynchronous listener observation after its durable commit."""
        with self._application_lock:
            self._deliver_events(events)

    def observe_fact(self, fact, *, now):
        """Serialize durable asynchronous observation with adapter application."""
        with self._application_lock:
            events = self.owner.observe(fact, now=now)
            self._deliver_events(events)
            for result in self.owner.resume_takeover(now=now):
                self._deliver(result)
            for result in self.owner.resume_closes(now=now):
                self._deliver(result)
            return events

    def observe_protection(self, snapshot, *, now):
        """Reconcile residual protection before releasing feedback and queues."""
        with self._application_lock:
            events = self.owner.observe_protection(snapshot, now=now)
            self._deliver_events(events)
            for result in self.owner.resume_closes(now=now):
                self._deliver(result)
            return events

    def observe_protection_execution(self, event, *, now):
        """Commit protective execution before serialized adapter delivery."""
        with self._application_lock:
            events = self.owner.observe_protection_execution(event, now=now)
            self._deliver_events(events)
            for result in self.owner.resume_closes(now=now):
                self._deliver(result)
            return events

    def observe_takeover_inventory(self, snapshot, *, now):
        """Apply complete broker evidence before qualified takeover continuation."""
        with self._application_lock:
            events = self.owner.observe_takeover_inventory(snapshot, now=now)
            self._deliver_events(events)
            for result in self.owner.resume_takeover(now=now):
                self._deliver(result)
            for result in self.owner.resume_closes(now=now):
                self._deliver(result)
            return events

    def on_completed_bar(self, leg_id, bar, *, now):
        with self._application_lock:
            return self._on_completed_bar(leg_id, bar, now=now)

    def _on_completed_bar(self, leg_id, bar, *, now):
        violation = validate_bar(bar)
        if type(leg_id) is not str or leg_id not in _LEG_RANK:
            violation = InputViolation("known_identity", "leg_id")
        if violation is not None:
            self.owner.record_input_incident("input:" + str(uuid4()), violation,
                                             source="bar", now=now)
            raise AccountOwnerError("invalid bar: " + violation.code + ":" + violation.field)
        if not isinstance(now, datetime) or now.utcoffset() is None:
            raise AccountOwnerError("acquisition time must be timezone-aware")
        # Equivalent aware timestamps name one occurrence, independently of
        # provider timezone and the order in which the four legs arrive.
        bar = replace(bar, ts=bar.ts.astimezone(timezone.utc))
        session = self.owner.binding["session"]
        if (bar.ts < session.opens_at or bar.ts >= session.closes_at
                or bar.ts > now or now > bar.ts + BAR_PERIOD + BAR_SLACK):
            self.owner.halt("invalid-bar-time:" + bar.ts.isoformat(), "barrier", now=now)
            raise AccountOwnerError("bar is stale, future, or outside the bound session")
        single_body = _jsonable(asdict(bar))
        retained_barriers = self.owner.retained_barriers
        retained_same = next((row for row in retained_barriers
                              if datetime.fromisoformat(row["bar_time"]) == bar.ts), None)
        if retained_same is not None:
            retained_bar = self._validated_retained_bar(retained_same["body"].get(leg_id),
                boundary=bar.ts, leg_id=leg_id)
            if retained_bar != bar:
                self.owner.halt("bar-conflict:" + bar.ts.isoformat(), "barrier", now=now)
                raise AccountOwnerError("conflicting bar identity")
            return None
        retained_times = [datetime.fromisoformat(row["bar_time"])
                          for row in retained_barriers
                          if row["session_id"] == session.session_id]
        known_times = retained_times + list(self._pending)
        # Bar.ts is the bar-open timestamp used by the Pine adapters. Without
        # retained history, only the session's first bar may seed their state.
        if not known_times and bar.ts != session.opens_at:
            self.owner.halt("bar-sequence:" + bar.ts.isoformat(), "barrier", now=now)
            raise AccountOwnerError("noncontiguous first bar boundary")
        if known_times:
            latest = max(known_times)
            invalid = bar.ts < latest
            if bar.ts > latest:
                invalid = (latest in self._pending or bar.ts != latest + BAR_PERIOD)
            if invalid:
                self.owner.halt("bar-sequence:" + bar.ts.isoformat(), "barrier", now=now)
                raise AccountOwnerError("noncontiguous bar boundary")
        if leg_id in self._pending.get(bar.ts, {}):
            if self._pending[bar.ts][leg_id] != bar:
                self.owner.halt("bar-conflict:" + bar.ts.isoformat(), "barrier", now=now)
                raise AccountOwnerError("conflicting bar identity")
            return None
        self.owner.record_partial_bar(leg_id, bar.ts, single_body, acquired_at=now)
        slot = self._pending.setdefault(bar.ts, {})
        slot[leg_id] = bar
        if len(slot) != len(LEG_ORDER):
            return None

        body = _bar_body(slot)
        mode = self._desired_mode()
        self.owner.record_barrier(
            bar.ts, body, session_id=session.session_id, mode=mode)
        actions = self._mode_actions(mode, boundary=bar.ts, now=now)
        for ordered_leg in LEG_ORDER:
            actions.extend(self._validated_actions(self.adapters[ordered_leg].on_bar(slot[ordered_leg]),
                boundary=bar.ts, source="on_bar:" + ordered_leg, now=now, leg_id=ordered_leg))
        self._validated_actions(actions, boundary=bar.ts, source="batch", now=now)
        actions = self._sort_actions(actions)
        occurrences = [self.owner.make_occurrence("runtime", bar.ts.isoformat(), ordinal)
                       for ordinal in range(len(actions))]
        action_body = [dict(_action_body(action), occurrence=asdict(occurrence))
                       for action, occurrence in zip(actions, occurrences)]
        self.owner.record_barrier_actions(bar.ts, action_body)
        self._prepared_here.add(bar.ts)

        results = []
        for action, occurrence in zip(actions, occurrences):
            result = handle_book_action(action, self.owner, occurrence=occurrence, now=now)
            if result.refusal_reason == "takeover_pending":
                control_results, completed = self.owner.advance_takeover(now=now)
                for control in control_results:
                    self._deliver(control)
                if completed:
                    result = handle_book_action(action, self.owner, occurrence=occurrence, now=now)
            results.append(result)
            local_feedback = self._retain_local_refusal(action, result, now=now,
                                                        boundary_time=bar.ts)
            if (result.confirmed_events or local_feedback) and self.crash_after_dispatch:
                raise SimulatedRuntimeCrash("fact committed before adapter feedback")
            self._deliver(result)
            self._deliver_events(local_feedback)
        if not any(result.refusal_reason == "awaiting_evidence" for result in results):
            self.owner.complete_barrier(bar.ts)
            del self._pending[bar.ts]
            self._prepared_here.discard(bar.ts)
        return tuple(results)

    def redeliver_prepared_boundary(self, bar_time, *, now):
        """Continue only same-runtime, unattempted evidence waits from disk."""
        from c1_rail.book_protection import ActionOccurrence
        with self._application_lock:
            if bar_time not in self._prepared_here:
                return ()
            if (not isinstance(now, datetime) or now.utcoffset() is None
                    or now < bar_time or now > bar_time + BAR_PERIOD + BAR_SLACK):
                raise AccountOwnerError("prepared boundary continuation time is invalid")
            retained = next(row for row in self.owner.retained_barriers
                            if row["bar_time"] == bar_time.isoformat())
            results = []
            waiting = False
            for ordinal, body in enumerate(retained["actions"]):
                occurrence = ActionOccurrence(**body["occurrence"])
                if occurrence != self.owner.make_occurrence("runtime", bar_time.isoformat(), ordinal):
                    self.owner.halt("occurrence-replay:" + bar_time.isoformat(), "identity", now=now)
                    raise AccountOwnerError("retained occurrence does not replay")
                state = self.owner.occurrence_state(occurrence)
                if state is None or state["state"] == "prepared":
                    raise AccountOwnerError("retained batch has an undispatched member")
                if state["state"] != "awaiting_evidence" or state["attempted"]:
                    continue
                action = _retained_action(body)
                result = handle_book_action(action, self.owner, occurrence=occurrence, now=now)
                results.append(result)
                waiting |= result.refusal_reason == "awaiting_evidence"
                local = self._retain_local_refusal(action, result, now=now, boundary_time=bar_time)
                if (result.confirmed_events or local) and self.crash_after_dispatch:
                    raise SimulatedRuntimeCrash("fact committed before adapter feedback")
                self._deliver(result)
                self._deliver_events(local)
            if not waiting:
                self.owner.complete_barrier(bar_time)
                self._pending.pop(bar_time, None)
                self._prepared_here.discard(bar_time)
            return tuple(results)

    def advance_schedule(self, *, now):
        with self._application_lock:
            results = self.owner.advance_schedule(now=now) + self.owner.resume_closes(now=now)
            for result in results:
                self._deliver(result)
            return results

    def expire_barrier(self, bar_time, *, now):
        with self._application_lock:
            # A complete, retained batch waiting for protection evidence is no
            # longer a partial input barrier. Its deadline belongs to the owner.
            if bar_time in self._prepared_here:
                return
            if bar_time in self._pending and now > bar_time + BAR_PERIOD + BAR_SLACK:
                self.owner.expire_partial_barrier(bar_time, now=now)
                del self._pending[bar_time]

    @classmethod
    def recover(cls, owner, adapters):
        runtime = cls(owner, adapters)
        feedback = {row["fact_id"]: row for row in owner.all_feedback}
        barriers = {row["bar_time"]: row for row in owner.retained_barriers}
        consumed = set()

        def replay_feedback(row):
            event = _feedback(row["body"])
            adapters[event.leg_id].on_execution(event)
            checkpoint = _jsonable(adapters[event.leg_id].checkpoint())
            if row["delivered"]:
                if row["checkpoint"] != checkpoint:
                    owner.halt("checkpoint-replay:" + row["fact_id"], "identity",
                               now=event.bar_time)
                    raise AccountOwnerError("retained checkpoint does not replay")
            else:
                owner.commit_feedback(row["fact_id"], checkpoint, now=event.bar_time)
            consumed.add(row["fact_id"])

        seen_barriers = set()
        for item in owner.replay_timeline:
            if item["kind"] == "barrier":
                retained = barriers.get(item["ref_id"])
                if retained is None:
                    raise AccountOwnerError("timeline references unknown barrier")
                boundary = datetime.fromisoformat(retained["bar_time"])
                bars = {leg_id: runtime._validated_retained_bar(retained["body"][leg_id],
                    boundary=boundary, leg_id=leg_id) for leg_id in LEG_ORDER}
                if retained["actions"] is None:
                    raise AccountOwnerError("incomplete retained action boundary")
                actions = runtime._mode_actions(Mode(retained["mode"]), boundary=boundary, now=boundary)
                for leg_id in LEG_ORDER:
                    actions.extend(runtime._validated_actions(adapters[leg_id].on_bar(bars[leg_id]),
                        boundary=boundary, source="on_bar:" + leg_id, now=boundary, leg_id=leg_id))
                runtime._validated_actions(actions, boundary=boundary, source="batch", now=boundary)
                rebuilt = [dict(_action_body(action), occurrence=asdict(owner.make_occurrence(
                    "runtime", boundary.isoformat(), ordinal)))
                    for ordinal, action in enumerate(runtime._sort_actions(actions))]
                if retained["actions"] != rebuilt:
                    owner.halt("replay-conflict:" + retained["bar_time"], "identity",
                               now=datetime.fromisoformat(retained["bar_time"]))
                    raise AccountOwnerError("retained action batch does not replay")
                seen_barriers.add(item["ref_id"])
            elif item["kind"] == "feedback":
                row = feedback.get(item["ref_id"])
                if row is None:
                    raise AccountOwnerError("timeline references unknown feedback")
                replay_feedback(row)
            else:
                raise AccountOwnerError("unknown replay timeline item")
        if seen_barriers != set(barriers) or consumed != set(feedback):
            raise AccountOwnerError("incomplete durable replay timeline")
        return runtime

    def observable_state(self):
        return {
            "account": self.owner.observable_accounting(),
            "adapters": {leg_id: self.adapters[leg_id].checkpoint()
                         for leg_id in LEG_ORDER},
        }
