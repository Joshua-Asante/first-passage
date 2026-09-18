"""Continuous synthetic seam for TB-S2; no loading or qualification authority.

The caller supplies accepted adapters, prices and full risk inputs. Production
identity, coverage and attempted-stage authorization belong to the controller.
Unsupported intrabar schedule evidence is refused, never approximated.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, replace
from datetime import timedelta
from typing import Callable, Mapping

from c1_rail.book_policy import (
    BOOK_LEGS, BookProtectionClock, CapacityLedger, add_quantity,
    entry_quantities, leg, require_policy,
)
from c1_rail.book_schedule import SchedulePhase, classify_execution_phase
from c1_signal_daemon.book_protocol import (
    Cancel, ExecutionEvent, FillTiming, OrderIntent, Side,
)
from c1_signal_daemon.feed import Bar
from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator


class ReplayNeedsContext(RuntimeError):
    """Missing evidence or unsupported semantics: no successful result exists."""


class ReplayDeadlineFailure(RuntimeError):
    """Confirmed nonflat deadline is T=infinity, never a coverage exclusion."""

    def __init__(self, result):
        super().__init__("own-flat deadline violated")
        self.result = result


@dataclass(frozen=True)
class Instrument:
    mintick: float
    pointvalue: float
    slippage_ticks: int
    commission_per_side: float
    orders_on_close: bool = False

    def __post_init__(self):
        for name in ("mintick", "pointvalue"):
            if not math.isfinite(getattr(self, name)) or getattr(self, name) <= 0:
                raise ValueError(f"{name} must be finite and positive")
        if type(self.slippage_ticks) is not int or self.slippage_ticks < 0:
            raise ValueError("slippage_ticks must be a nonnegative integer")
        if not math.isfinite(self.commission_per_side) or self.commission_per_side < 0:
            raise ValueError("commission_per_side must be finite and nonnegative")


def lifetime_adverse_mark(bar, side, entry_price, qty, pointvalue, timing, trigger=None):
    """Position contribution under RC-6, independently of its same-bar exit.

    ``midbar`` requires the un-slipped triggering price. The first directed
    crossing in the emulator's OHLC path determines the remaining lifetime.
    A close-only fill contributes zero, including no invented earlier extreme.
    """
    if timing == "close":
        return 0.0
    if timing == "open":
        extreme = bar.low if side is Side.BUY else bar.high
    elif timing == "midbar":
        if trigger is None or not math.isfinite(trigger):
            raise ValueError("midbar marking requires a finite trigger")
        seq = ([bar.open, bar.high, bar.low, bar.close]
               if bar.high - bar.open <= bar.open - bar.low
               else [bar.open, bar.low, bar.high, bar.close])
        remaining = None
        for i, (a, b) in enumerate(zip(seq, seq[1:])):
            crossed = a <= trigger <= b if side is Side.BUY else b <= trigger <= a
            if crossed:
                remaining = [trigger, *seq[i + 1:]]
                break
        if remaining is None:
            raise ValueError("trigger is not crossed by the OHLC path")
        extreme = min(remaining) if side is Side.BUY else max(remaining)
    else:
        raise ValueError("unknown lifetime timing")
    direction = 1 if side is Side.BUY else -1
    return min(0.0, (extreme - entry_price) * direction * qty * pointvalue)


class BookReplay:
    """One fresh instance per path; all four adapters persist across splices.

    ``sizing_inputs`` returns lifecycle_tier and the actual entry_quantities
    inputs. In particular Striker requires unrounded risk dollars, risk per
    contract and allocation. Adapter-normal integer size is never inverted.
    ``schedule_quotes`` returns an evidenced price at the requested instant.
    ``broker_factory`` is an explicit deterministic synthetic-injection seam;
    it does not approve a stress fill model for qualification. Injected brokers
    must provide confirmed fills plus definitive terminal remainder facts and
    preserve the pinned emulator queue/state interface used below.
    """

    def __init__(self, adapters: Mapping, instruments: Mapping[str, Instrument], *,
                 policy, initial_state, sizing_inputs: Callable,
                 schedule_quotes: Callable, broker_factory: Callable = TVBrokerEmulator):
        expected = {x.leg_id for x in BOOK_LEGS}
        if set(adapters) != expected or set(instruments) != expected:
            raise ValueError("exactly the four fixed book legs are required")
        if initial_state is None:
            raise ValueError("initial_state is required")
        self.policy = require_policy(policy)
        self.adapters = dict(adapters)
        self.instruments = dict(instruments)
        self.clock = BookProtectionClock(policy, initial_state.current_equity,
                                         initial_state.historical_eod_peak)
        self.initial_equity = initial_state.current_equity
        self.sizing_inputs = sizing_inputs
        self.schedule_quotes = schedule_quotes
        self.brokers = {k: broker_factory(k, v.mintick, v.pointvalue,
                        v.slippage_ticks, v.commission_per_side,
                        margin_pct=0, orders_on_close=v.orders_on_close)
                        for k, v in instruments.items()}
        self.ledger = CapacityLedger()
        self.orders = {}  # (leg, order id) -> (sized intent, path ordinal)
        self.base = {k: 0 for k in expected}
        self.base_order = {k: None for k in expected}
        self.accepted = set()
        self.events = []
        self.cash = self.initial_equity
        self.confirmed_fill_count = 0
        self.lots = {}  # confirmed remaining lots, never emitted intents
        self._used = False
        self._index = 0
        self._path_time = None

    def _log(self, kind, leg_id="", detail=""):
        from .model import ReplayEvent
        self.events.append(ReplayEvent(self._path_time, kind, leg_id, str(detail)))

    def _edge(self):
        from .model import EdgeState
        keys = sorted(self.brokers)
        return EdgeState(tuple((k, abs(self.brokers[k].position())) for k in keys),
                         tuple((k, len(self.brokers[k].pending_order_ids())) for k in keys),
                         tuple((k, self.ledger.reserved.get(k, 0)) for k in keys))

    def _feedback(self, events):
        exited = set()
        for event in events:
            k, fill = event.leg_id, event.fill
            key = (k, event.order_id)
            if fill is not None:
                self.confirmed_fill_count += 1
                self.cash -= fill.commission
                if fill.kind in ("entry", "add"):
                    if key not in self.orders:
                        raise ReplayNeedsContext("entry fill lacks outstanding reservation identity")
                    requested, created = self.orders[key]
                    if fill.qty > requested.qty:
                        raise ReplayNeedsContext("entry fill exceeds outstanding order quantity")
                    self.ledger.confirm_fill(k, fill.qty)
                    self.lots[fill.fill_id] = fill
                    if fill.kind == "entry":
                        if self.base_order[k] != fill.order_id:
                            self.base[k] = 0
                            self.base_order[k] = fill.order_id
                        self.base[k] += fill.qty
                    remaining = requested.qty - fill.qty
                    if remaining:
                        self.orders[key] = (replace(requested, qty=remaining), created)
                    else:
                        self.orders.pop(key)
                else:
                    original = self.lots.get(fill.entry_fill_id)
                    if original is None or fill.qty > original.qty:
                        raise ReplayNeedsContext("exit lacks confirmed lot evidence")
                    direction = 1 if original.side is Side.BUY else -1
                    self.cash += ((fill.price - original.price) * direction * fill.qty
                                  * self.instruments[k].pointvalue)
                    if fill.qty == original.qty:
                        del self.lots[original.fill_id]
                    else:
                        self.lots[original.fill_id] = replace(original, qty=original.qty - fill.qty)
                    exited.add(k)
                self._log("fill", k, json.dumps({
                    "kind": fill.kind, "qty": fill.qty, "price": fill.price,
                    "side": fill.side.value, "commission": fill.commission,
                    "fill_id": fill.fill_id, "order_id": fill.order_id,
                    "entry_fill_id": fill.entry_fill_id, "reason": fill.reason,
                    "source_time": fill.bar_time.isoformat(),
                }, sort_keys=True, separators=(",", ":")))
            if event.event in ("cancel", "reject") and key in self.orders:
                intent, _ = self.orders[key]
                self.ledger.release_reservation(k, intent.qty)
                self._log(event.event, k, event.detail)
            if event.event in ("cancel", "reject"):
                self.orders.pop(key, None)
            self.adapters[k].on_execution(event)
            if not any(f.leg_id == k for f in self.lots.values()):
                self.base[k] = 0
                self.base_order[k] = None
        # One broker submission can close multiple FIFO lots. Reconcile its
        # confirmed final position once, rather than mislabel an intermediate
        # lot event as a partially completed takeover command.
        for k in exited:
            self.ledger.confirm_position(k, sum(f.qty for f in self.lots.values() if f.leg_id == k))

    def _process_segment(self, bars):
        # The emulator snaps every OHLC value before path selection. Adverse
        # lifetime uses those same prices and tie-breaking, never raw decimals.
        bars = {k: Bar(b.ts, *(self.brokers[k]._snap(v)
                    for v in (b.open,b.high,b.low,b.close)), b.volume)
                for k, b in bars.items()}
        cash_before = self.cash
        carried = tuple(self.lots.values())
        # Read the pinned emulator's effective queue, not raw strategy intent:
        # stop levels are tick-rounded and marketable stops become NEXT_OPEN
        # markets at submit. These private read-only views are an explicit
        # transitive identity dependency until the emulator exposes a receipt.
        pending = {(k, intent.order_id): intent for k, broker in self.brokers.items()
                   for intent in [*broker._pending_market, *broker._pending_stop.values()]}
        entries = []
        exits = {}
        fees = 0.0
        for k, bar in bars.items():
            broker = self.brokers[k]
            events = broker.process_bar(bar)
            entries.extend(e.fill for e in events if e.fill and e.fill.kind in ("entry", "add"))
            for event in events:
                if event.fill is not None and event.fill.entry_fill_id is not None:
                    exits.setdefault(event.fill.entry_fill_id, []).append(event.fill)
            fees += sum(e.fill.commission for e in events if e.fill)
            self._feedback(events)
        def contribution(fill, timing, trigger=None):
            pointvalue = self.instruments[fill.leg_id].pointvalue
            per_contract = lifetime_adverse_mark(bars[fill.leg_id], fill.side, fill.price, 1,
                                                pointvalue, timing, trigger)
            remaining = fill.qty
            value = 0.0
            direction = 1 if fill.side is Side.BUY else -1
            for closed in exits.get(fill.fill_id, ()):
                remaining -= closed.qty
                realized = (closed.price - fill.price) * direction * closed.qty * pointvalue
                value += min(per_contract * closed.qty, realized)
            if remaining < 0:
                raise ReplayNeedsContext("bar exits exceed confirmed lifetime quantity")
            return value + remaining * per_contract

        adverse = sum(contribution(f, "open") for f in carried)
        for f in entries:
            intent = pending[(f.leg_id, f.order_id)]
            b = bars[f.leg_id]
            at_open = (intent.order_type == "market" or
                       (b.open >= intent.price if f.side is Side.BUY else b.open <= intent.price))
            adverse += contribution(f, "open" if at_open else "midbar", intent.price)
        return cash_before + adverse - fees

    def _split(self, session, pb, bars, instant):
        splitter = getattr(self.schedule_quotes, "split_bar", None)
        if splitter is None:
            raise ReplayNeedsContext("intrabar schedule requires split OHLC lifetime evidence")
        left, right = {}, {}
        def vertices(b):
            return ([b.open, b.high, b.low, b.close] if b.high-b.open <= b.open-b.low
                    else [b.open, b.low, b.high, b.close])

        def turns(values):
            result = []
            for value in values:
                if result and value == result[-1]:
                    continue
                while len(result) >= 2 and (result[-1]-result[-2])*(value-result[-1]) >= 0:
                    result.pop()
                result.append(value)
            return result
        for k, original in bars.items():
            if original.ts != pb.source_bar_time:
                interval_splitter = getattr(self.schedule_quotes, "split_interval", None)
                if interval_splitter is None:
                    raise ReplayNeedsContext("multiple intrabar boundaries require interval split evidence")
                prefix, suffix = interval_splitter(session, pb, original, instant, k)
            else:
                prefix, suffix = splitter(session, pb, instant, k)
            if (not isinstance(prefix, Bar) or not isinstance(suffix, Bar)
                    or prefix.ts != original.ts or suffix.ts != instant
                    or prefix.open != original.open or suffix.close != original.close
                    or prefix.close != suffix.open
                    or max(prefix.high, suffix.high) != original.high
                    or min(prefix.low, suffix.low) != original.low
                    or prefix.volume + suffix.volume != original.volume):
                raise ReplayNeedsContext("split bars do not aggregate to original source bar")
            for segment in (prefix, suffix):
                values = (segment.open, segment.high, segment.low, segment.close)
                if (not all(math.isfinite(v) for v in values)
                        or not 0 < segment.low <= min(segment.open, segment.close)
                        <= max(segment.open, segment.close) <= segment.high):
                    raise ReplayNeedsContext("invalid split OHLC evidence")
            if prefix.close != self.schedule_quotes(session, instant, k):
                raise ReplayNeedsContext("split boundary differs from schedule price")
            if turns(vertices(prefix) + vertices(suffix)) != turns(vertices(original)):
                raise ReplayNeedsContext("split evidence changes the accepted emulator path")
            left[k], right[k] = prefix, suffix
        return left, right

    def _submit(self, k, actions, bar):
        events = self.brokers[k].submit(actions, bar)
        self._feedback(events)
        for action in actions:
            if (isinstance(action, OrderIntent) and action.kind in ("exit", "flat")
                    and not any(e.order_id == action.order_id for e in events)
                    and action.order_id not in self.brokers[k].pending_order_ids()
                    and not any(fill.leg_id == k and (action.scope_fill_ids is None
                        or fill.fill_id in action.scope_fill_ids) for fill in self.lots.values())):
                self._log("empty_exit_dropped", k, action.order_id)
        return events

    def _cancel_pending(self, k, action, bar):
        # A controller cancellation is not a Pine calculation. Calling submit
        # would also evaluate orders_on_close brackets. Use the pinned native
        # cancellation operation, delivering its exact confirmed events.
        self._feedback(self.brokers[k]._cancel(action, bar))

    def _reject(self, intent, bar, reason):
        self._log("refused", intent.leg_id, reason)
        self.adapters[intent.leg_id].on_execution(ExecutionEvent(
            "reject", intent.leg_id, bar.ts, order_id=intent.order_id, detail=reason))

    def _flatten(self, k, bar, reason):
        # Scheduler supersedes every working order, including queued closes.
        # Pine's unscoped Cancel intentionally only cancels entry/add orders.
        for order_id in self.brokers[k].pending_order_ids():
            self._cancel_pending(k, Cancel(k, order_id), bar)
        pos = self.brokers[k].position()
        if pos:
            self._submit(k, [OrderIntent(f"{reason}:{self._index}:{k}", k, "flat",
                         Side.SELL if pos > 0 else Side.BUY, None,
                         timing=FillTiming.THIS_CLOSE, reason=reason)], bar)

    def _admit(self, intent, pb, mode, schedule):
        k = intent.leg_id
        bar = dict(pb.bars)[k]
        if intent.bar_time is not None and intent.bar_time != pb.source_bar_time:
            raise ReplayNeedsContext("adapter intent timestamp differs from source bar")
        key = (k, intent.kind, pb.path_time)
        if key in self.accepted:
            self._log("duplicate_dropped", k, intent.kind)
            return
        if intent.kind in ("entry", "add"):
            if intent.side is not leg(k).entry_side:
                self._reject(intent, bar, "side differs from fixed book")
                return
            phase = classify_execution_phase(cutoff=schedule.cutoff,
                flatten_start=schedule.flatten_start, own_flat_deadline=schedule.own_flat_deadline,
                now=pb.source_bar_time + timedelta(minutes=15))
            if phase is not SchedulePhase.RISK_ADD:
                self._reject(intent, bar, "scheduled entry cutoff")
                return
            values = dict(self.sizing_inputs(k, intent, pb))
            tier = values.pop("lifecycle_tier", None)
            if tier is None:
                raise ReplayNeedsContext("explicit lifecycle authorization required")
            qty = (entry_quantities(k, mode=mode, policy=self.policy,
                                    lifecycle_tier=tier, **values)[0]
                   if intent.kind == "entry" else
                   add_quantity(k, self.base[k], mode=mode, policy=self.policy,
                                lifecycle_tier=tier))
            if qty == 0:
                self._reject(intent, bar, "zero policy quantity")
                return
            if (k, intent.order_id) in self.orders:
                self._reject(intent, bar, "existing working order id")
                return
            decision = self.ledger.request(k, qty)
            if decision.takeover is not None:
                takeover = self.ledger.begin_takeover(decision.takeover)
                for displaced in decision.takeover.displaced:
                    displaced_bar = dict(pb.bars).get(displaced)
                    if displaced_bar is None:
                        takeover.fail(displaced, "missing synchronous close price")
                        break
                    self._cancel_pending(displaced, Cancel(displaced), displaced_bar)
                    if takeover.state != "pending":
                        break
                    if self.brokers[displaced].pending_order_ids():
                        takeover.fail(displaced, "cancel not confirmed")
                        break
                    takeover.ack_cancel(displaced)
                    self._log("capacity_takeover_cancel_ack", displaced)
                    self._flatten(displaced, displaced_bar, "capacity_takeover_close")
                    if takeover.state != "pending":
                        break
                    takeover.confirm_close(displaced, abs(self.brokers[displaced].position()))
                    self._log("capacity_takeover_close_confirmed", displaced,
                              abs(self.brokers[displaced].position()))
                decision = self.ledger.settle_takeover()
                self._log("capacity_takeover_admitted" if decision.admitted else
                          "capacity_takeover_refused", k, decision.reason)
            if not decision.admitted:
                self._reject(intent, bar, decision.reason)
                return
            intent = replace(intent, qty=qty)
            self.orders[(k, intent.order_id)] = (intent, self._index)
        self.accepted.add(key)
        return intent

    def _schedule(self, session, instant, flatten):
        schedule = session.source.schedule
        phase = classify_execution_phase(cutoff=schedule.cutoff,
            flatten_start=schedule.flatten_start, own_flat_deadline=schedule.own_flat_deadline,
            now=instant)
        expected = (SchedulePhase.DEADLINE if flatten is None else
                    SchedulePhase.FLATTEN if flatten else SchedulePhase.CUTOFF)
        if phase is not expected:
            raise ReplayNeedsContext("scheduled action differs from shared execution phase")
        mapped = next((pb for pb in reversed(session.bars)
                       if pb.source_bar_time <= instant <= pb.source_bar_time + timedelta(minutes=15)), None)
        if mapped is None:
            raise ReplayNeedsContext("schedule instant lacks retained path interval")
        self._path_time = mapped.path_time + (instant - mapped.source_bar_time)
        if flatten is None:
            edge = self._edge()
            if not edge.is_flat:
                from .model import ReplayResult, SessionRecord
                self._log("deadline_failure")
                record = SessionRecord(session.occurrence, session.path_session_date,
                    session.source.session_id, self.cash - self._opening,
                    min(self._session_low, self.cash - self._opening),
                    self.confirmed_fill_count - self._session_fill_start,
                    False, self._start_edge, edge)
                raise ReplayDeadlineFailure(ReplayResult(tuple([*self._records, record]), tuple(self.events)))
            self._log("deadline_flat_confirmed")
            return
        for k in self.brokers:
            if not (self.brokers[k].pending_order_ids() or self.brokers[k].position()):
                continue
            try:
                price = self.schedule_quotes(session, instant, k)
            except (KeyError, LookupError) as exc:
                raise ReplayNeedsContext("missing source-instant schedule price") from exc
            if not isinstance(price, (int, float)) or not math.isfinite(price):
                raise ReplayNeedsContext("invalid source-instant schedule price")
            bar = Bar(instant, price, price, price, price)
            if flatten:
                self._flatten(k, bar, "scheduled_flatten")
            else:
                self._cancel_pending(k, Cancel(k), bar)
        self._log("scheduled_flatten" if flatten else "scheduled_cutoff", detail=instant.isoformat())

    def run(self, path):
        from .model import ReplayResult, SessionRecord
        if self._used:
            raise ValueError("a replay instance is single-use")
        self._used = True
        records = []
        self._records = records
        last_path_time = None
        for session in path:
            start = self._edge()
            if session.block_start and not start.is_flat:
                raise ReplayNeedsContext("block start is not joint-flat")
            if not session.bars:
                raise ReplayNeedsContext("session has no covered bars")
            opening = self.cash
            self._session_fill_start = self.confirmed_fill_count
            self._opening, self._start_edge = opening, start
            low = 0.0
            self._session_low = low
            mode = self.clock.mode_for(session.path_session_date)
            self._path_time = session.bars[0].path_time
            self._log("session_mode", detail=mode.value)
            for k, adapter in self.adapters.items():
                changes = adapter.set_mode(mode)
                if any(not isinstance(a, Cancel) for a in changes):
                    raise ReplayNeedsContext("mode transition emitted non-cancel action")
                if changes:
                    first = dict(session.bars[0].bars).get(k)
                    if first is None and self.brokers[k].pending_order_ids():
                        raise ReplayNeedsContext("mode cancel lacks source bar")
                    if first is not None:
                        for action in changes:
                            self._cancel_pending(k, action, first)
            schedule = session.source.schedule
            for instant in (schedule.cutoff, schedule.flatten_start, schedule.own_flat_deadline):
                if not any(pb.source_bar_time <= instant <= pb.source_bar_time + timedelta(minutes=15)
                           for pb in session.bars):
                    raise ReplayNeedsContext("schedule instant lacks retained path interval")
            schedule_events = [(schedule.cutoff, False), (schedule.flatten_start, True),
                               (schedule.own_flat_deadline, None)]
            next_schedule = 0
            for pb in session.bars:
                if last_path_time is not None and pb.path_time <= last_path_time:
                    raise ValueError("path_time must strictly increase")
                last_path_time = self._path_time = pb.path_time
                self._index += 1
                bars = dict(pb.bars)
                for k in set(self.brokers) - set(bars):
                    if self.brokers[k].position() or self.brokers[k].pending_order_ids():
                        raise ReplayNeedsContext("missing bar for exposed leg")
                while next_schedule < len(schedule_events) and schedule_events[next_schedule][0] <= pb.source_bar_time:
                    self._schedule(session, *schedule_events[next_schedule])
                    next_schedule += 1
                for (k, oid), (_, created) in list(self.orders.items()):
                    if self._index - created > 1:
                        self._cancel_pending(k, Cancel(k, oid), bars[k])
                segment_bars = bars
                while (next_schedule < len(schedule_events)
                       and schedule_events[next_schedule][0] < pb.source_bar_time + timedelta(minutes=15)):
                    instant, flatten = schedule_events[next_schedule]
                    if not self._edge().is_flat:
                        exposed = {k:bar for k,bar in segment_bars.items()
                            if (self.brokers[k].position() or self.brokers[k].pending_order_ids()
                                or self.ledger.confirmed.get(k,0) or self.ledger.reserved.get(k,0))}
                        # _split remains a pure all-supplied-bars validator for
                        # source-evidence consumers. Inert legs need no price
                        # evidence; retain their original bar for completion.
                        prefix, suffix = self._split(session, pb, exposed, instant)
                        segment_bars = {**segment_bars, **suffix}
                        low = min(low, self._process_segment(prefix) - opening)
                        self._session_low = low
                    self._path_time = pb.path_time + (instant - pb.source_bar_time)
                    self._schedule(session, instant, flatten)
                    next_schedule += 1
                low = min(low, self._process_segment(segment_bars) - opening)
                self._session_low = low
                self._path_time = pb.path_time + timedelta(minutes=15)
                batches = {}
                for k, adapter in self.adapters.items():
                    if k not in bars:
                        continue
                    emitted = list(adapter.on_bar(bars[k]))
                    for action in emitted:
                        if action.leg_id != k:
                            raise ReplayNeedsContext("adapter emitted another leg's action")
                    batches[k] = emitted
                for k in sorted(batches, key=lambda k: (leg(k).priority, k)):
                    emitted = batches[k]
                    for action in emitted:
                        if isinstance(action, Cancel):
                            # Acknowledge removal of old working risk before
                            # admission. Keep this action at its original place
                            # in the final batch for its effect on new orders.
                            self._cancel_pending(k, action, bars[k])
                    admitted = {}
                    intents = [(index, action) for index, action in enumerate(emitted)
                               if isinstance(action, OrderIntent)]
                    intents.sort(key=lambda pair: (0 if pair[1].kind == "entry" else
                                                  1 if pair[1].kind == "add" else 2, pair[0]))
                    for index, action in intents:
                        admitted[index] = self._admit(action, pb, mode, schedule)
                    actions = [admitted[index] if isinstance(action, OrderIntent) else action
                               for index, action in enumerate(emitted)
                               if not isinstance(action, OrderIntent) or admitted[index] is not None]
                    # Native batch registration matters: crossed stop entries,
                    # OCA cancellations and orders_on_close bracket evaluation
                    # happen only after every action of this calculation exists.
                    self._submit(k, actions, bars[k])
                close_equity = self.cash + sum(self.brokers[k].open_pnl(bar.close) for k, bar in bars.items())
                low = min(low, close_equity - opening)
                self._session_low = low
                self._log("bar_equity", detail=repr(close_equity))
            while next_schedule < len(schedule_events):
                self._schedule(session, *schedule_events[next_schedule])
                next_schedule += 1
            end = self._edge()
            flat = end.is_flat
            if session.block_end and not flat:
                self._log("joint_flat_edge_failed")
            if not flat:
                raise ReplayNeedsContext("unresolved residual at session settlement")
            low = min(low, self.cash - opening)
            self.clock.settle(session.path_session_date, max(0.0, self.cash))
            records.append(SessionRecord(session.occurrence, session.path_session_date,
                session.source.session_id, self.cash - opening, low,
                self.confirmed_fill_count - self._session_fill_start, flat, start, end))
        return ReplayResult(tuple(records), tuple(self.events))
