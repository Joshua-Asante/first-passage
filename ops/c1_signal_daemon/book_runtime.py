"""Durable completed-bar coordinator for the fixed four-leg book.

The coordinator is deliberately transport-free.  It records one complete bar
boundary and its deterministic action batch through :class:`BookAccountOwner`
before asking that owner to dispatch anything.  Recovery replays retained bars
and confirmed feedback only; it never resends a broker command.
"""
from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timedelta
from enum import Enum
import threading

from c1_rail.book_policy import BOOK_LEGS, is_protected
from c1_rail.book_account_owner import AccountOwnerError, BookAccountOwner
from c1_rail.c1_rail_listener import handle_book_action
from c1_signal_daemon.book_adapters import AdapterRegistry
from c1_signal_daemon.book_protocol import ExecutionEvent, Fill, Mode
from c1_signal_daemon.feed import Bar


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
        self._mode = None
        for retained in owner.retained_partial_bars:
            instant = datetime.fromisoformat(retained["bar_time"])
            self._pending.setdefault(instant, {})[retained["leg_id"]] = _bar(retained["body"])

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

    def _mode_actions(self, mode):
        if not isinstance(mode, Mode):
            raise ValueError("typed protection mode required")
        actions = []
        if mode != self._mode:
            for leg_id in LEG_ORDER:
                actions.extend(self.adapters[leg_id].set_mode(mode))
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

    def _retain_local_refusal(self, action, result, *, now):
        reason = result.refusal_reason
        if reason is None or reason in ("takeover_pending", "duplicate_operation"):
            return ()
        return self.owner.record_local_refusal(action, reason, now=now)

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
            return events

    def on_completed_bar(self, leg_id, bar, *, now):
        with self._application_lock:
            return self._on_completed_bar(leg_id, bar, now=now)

    def _on_completed_bar(self, leg_id, bar, *, now):
        if leg_id not in _LEG_RANK or not isinstance(bar, Bar):
            raise ValueError("typed known-leg bar required")
        if bar.ts.utcoffset() is None or now.utcoffset() is None:
            raise ValueError("bar and acquisition times must be timezone-aware")
        session = self.owner.binding["session"]
        if (bar.ts < session.opens_at or bar.ts >= session.closes_at
                or bar.ts > now or now > bar.ts + BAR_PERIOD + BAR_SLACK):
            self.owner.halt("invalid-bar-time:" + bar.ts.isoformat(), "barrier", now=now)
            raise AccountOwnerError("bar is stale, future, or outside the bound session")
        single_body = _jsonable(asdict(bar))
        retained_barriers = self.owner.retained_barriers
        retained_same = next((row for row in retained_barriers
                              if row["bar_time"] == bar.ts.isoformat()), None)
        if retained_same is not None:
            if retained_same["body"].get(leg_id) != single_body:
                self.owner.halt("bar-conflict:" + bar.ts.isoformat(), "barrier", now=now)
                raise AccountOwnerError("conflicting bar identity")
            return None
        retained_times = [datetime.fromisoformat(row["bar_time"])
                          for row in retained_barriers
                          if row["session_id"] == session.session_id]
        known_times = retained_times + list(self._pending)
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
        actions = self._mode_actions(mode)
        for ordered_leg in LEG_ORDER:
            actions.extend(self.adapters[ordered_leg].on_bar(slot[ordered_leg]))
        actions = self._sort_actions(actions)
        action_body = [_action_body(action) for action in actions]
        self.owner.record_barrier_actions(bar.ts, action_body)

        results = []
        for action in actions:
            result = handle_book_action(action, self.owner, now=now)
            if result.refusal_reason == "takeover_pending":
                control_results, completed = self.owner.advance_takeover(now=now)
                for control in control_results:
                    self._deliver(control)
                if completed:
                    result = handle_book_action(action, self.owner, now=now)
            results.append(result)
            local_feedback = self._retain_local_refusal(action, result, now=now)
            if (result.confirmed_events or local_feedback) and self.crash_after_dispatch:
                raise SimulatedRuntimeCrash("fact committed before adapter feedback")
            self._deliver(result)
            self._deliver_events(local_feedback)
        self.owner.complete_barrier(bar.ts)
        del self._pending[bar.ts]
        return tuple(results)

    def advance_schedule(self, *, now):
        with self._application_lock:
            results = self.owner.advance_schedule(now=now)
            for result in results:
                self._deliver(result)
            return results

    def expire_barrier(self, bar_time, *, now):
        with self._application_lock:
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
                bars = {leg_id: _bar(retained["body"][leg_id]) for leg_id in LEG_ORDER}
                actions = runtime._mode_actions(Mode(retained["mode"]))
                for leg_id in LEG_ORDER:
                    actions.extend(adapters[leg_id].on_bar(bars[leg_id]))
                rebuilt = [_action_body(action) for action in runtime._sort_actions(actions)]
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
