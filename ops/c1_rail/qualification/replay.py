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
from fractions import Fraction
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


#: Legs whose base entry follows lifecycle L1 (§59 Rulings 6 and 7(a)): placed once,
#: it rests until it fills or an applicable cancellation ends it (the port's
#: own cancel, the RC-8 cutoff, a takeover or incident handling). RC-9's
#: one-bar cancel keeps applying to every other resting entry or add.
L1_BASE_ENTRY_LEGS = frozenset({"orb_mnq_v7"})


def _one_bar_cancel_applies(leg_id, intent):
    return not (leg_id in L1_BASE_ENTRY_LEGS and intent.kind == "entry")


#: T00 Tier-2 attribution sidecar (card 2026-10-08 §3.1 (i)). Lot kinds split each
#: leg's value; forced closes are the replay's own flatten reasons.
ATTRIBUTION_SCHEMA = "t00_tier2_attribution/v1"
LOT_KINDS = ("entry", "add")
FORCED_CLOSE_REASONS = ("scheduled_flatten", "capacity_takeover_close")


class AttributionSidecar:
    """Opt-in per-session, per-leg recorder for the T00 Tier-2 diagnostic.

    It only reads replay state: nothing it holds enters ``events``,
    ``SessionRecord``, ``ReplayResult`` or a digest. Leg cash is realized P&L
    net of commission, split by lot kind (an exit's P&L and commission belong
    to the lot it closes). At every observed point a leg's value is its
    session-relative cash plus its mark, and leg values sum to the combined
    value the replay compares against its intraday low. The low point is the
    first point at which the combined low is set; ``open`` if none is lower.
    """

    def __init__(self, legs):
        self.legs = tuple(sorted(legs))
        self.cash = {(k, kind): 0.0 for k in self.legs for kind in LOT_KINDS}
        self.commission = dict.fromkeys(self.cash, 0.0)
        self.sessions = []
        self.current = None
        self._open_cash, self._open_commission, self._forced_orders = {}, {}, set()

    def _by_leg(self, values):
        return {k: {kind: values[(k, kind)] for kind in LOT_KINDS} for k in self.legs}

    def _relative(self, cash):
        return {key: cash[key] - self._open_cash[key] for key in cash}

    def begin(self, session, mode):
        self._open_cash, self._open_commission = dict(self.cash), dict(self.commission)
        self._forced_orders = set()
        zero = dict.fromkeys(self.cash, 0.0)
        self.current = {
            "occurrence": session.occurrence, "source_session_id": session.source.session_id,
            "path_session_date": session.path_session_date.isoformat(), "session_mode": mode.value,
            "legs": {k: {"requests": [], "filled": dict.fromkeys(LOT_KINDS, 0), "fills": dict.fromkeys(LOT_KINDS, 0),
                         "forced_closes": {r: {"count": 0, "qty": 0, "pnl": 0.0, "commission": 0.0}
                                           for r in FORCED_CLOSE_REASONS}} for k in self.legs},
            "low": {"where": "open", "bar_index": None, "path_time": None, "value": 0.0,
                    "cash": self._by_leg(zero), "mark": self._by_leg(zero)},
            "last_bar_mark": self._by_leg(zero),
        }

    def entry_fill(self, fill):
        self.cash[(fill.leg_id, fill.kind)] -= fill.commission
        self.commission[(fill.leg_id, fill.kind)] += fill.commission
        row = self.current["legs"][fill.leg_id]
        row["filled"][fill.kind] += fill.qty
        row["fills"][fill.kind] += 1

    def exit_fill(self, fill, lot_kind, realized):
        key = (fill.leg_id, lot_kind)
        self.cash[key] += realized - fill.commission
        self.commission[key] += fill.commission
        if fill.reason in FORCED_CLOSE_REASONS:
            forced = self.current["legs"][fill.leg_id]["forced_closes"][fill.reason]
            if (fill.leg_id, fill.order_id) not in self._forced_orders:
                self._forced_orders.add((fill.leg_id, fill.order_id))
                forced["count"] += 1
            forced["qty"] += fill.qty
            forced["pnl"] += realized - fill.commission
            forced["commission"] += fill.commission

    def request(self, leg_id, kind, qty):
        row = {"kind": kind, "requested": qty, "policy": None, "admitted": 0, "outcome": None}
        self.current["legs"][leg_id]["requests"].append(row)
        return row

    def reject(self, leg_id, reason):
        row = self.current["legs"][leg_id]["requests"][-1]
        if row["outcome"] is None:
            row["outcome"] = reason

    def observe(self, where, bar_index, path_time, value, cash, marks):
        """``value`` is exactly the combined value the replay compares; ``cash`` is absolute."""
        if value < self.current["low"]["value"]:
            self.current["low"] = {
                "where": where, "bar_index": bar_index,
                "path_time": None if path_time is None else path_time.isoformat(), "value": value,
                "cash": self._by_leg(self._relative(cash)), "mark": self._by_leg(marks)}

    def bar_close(self, bar_index, path_time, value, marks):
        self.current["last_bar_mark"] = self._by_leg(marks)
        self.observe("bar_close", bar_index, path_time, value, self.cash, marks)

    def finish(self, where, bar_index, path_time, value, open_at_deadline=None):
        self.observe(where, bar_index, path_time, value, self.cash, dict.fromkeys(self.cash, 0.0))
        current = self.current
        if open_at_deadline is not None:
            current["open_at_deadline"] = open_at_deadline
        current["close"] = {"cash": self._by_leg(self._relative(self.cash)),
                            "commission": self._by_leg({key: self.commission[key] - self._open_commission[key]
                                                        for key in self.commission})}
        for k, row in current["legs"].items():
            requests = row["requests"]
            row["capacity_refusals"] = sum(1 for r in requests if "capacity_reason" in r and r["admitted"] == 0)
            row["takeovers_won"] = sum(1 for r in requests if r.get("takeover", {}).get("admitted") is True)
            row["takeovers_refused"] = sum(1 for r in requests if r.get("takeover", {}).get("admitted") is False)
            row["takeovers_displaced"] = sum(1 for other in current["legs"].values() for r in other["requests"]
                                             if k in r.get("takeover", {}).get("cancel_acked", ()))
        self.sessions.append(current)
        self.current = None

    def result(self):
        """A detached, JSON-safe copy: no caller can reach the live accumulator."""
        return tuple(json.loads(json.dumps(self.sessions, allow_nan=False)))


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


def accepted_path(bar):
    """The emulator's OHLC path: open, the extreme nearer the open, far extreme, close."""
    return ([bar.open, bar.high, bar.low, bar.close] if bar.high-bar.open <= bar.open-bar.low
            else [bar.open, bar.low, bar.high, bar.close])


def path_turns(values):
    """Turning points of a price path; repeats and monotone interiors drop out."""
    result = []
    for value in values:
        if result and value == result[-1]:
            continue
        while len(result) >= 2 and (result[-1]-result[-2])*(value-result[-1]) >= 0:
            result.pop()
        result.append(value)
    return result


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
        self._attribution = None  # opt-in Tier-2 sidecar; off by default

    def enable_attribution(self):
        """Turn on the per-session, per-leg sidecar before ``run``; it changes no replay output."""
        if self._used:
            raise ValueError("attribution must be enabled before the single run")
        self._attribution = AttributionSidecar(self.brokers)

    def attribution(self):
        if self._attribution is None:
            raise ValueError("attribution was not enabled")
        return self._attribution.result()

    def _attribution_marks(self, bars):
        """Bar-close marks by lot kind; the leg total is the broker's own open_pnl."""
        marks = dict.fromkeys(self._attribution.cash, 0.0)
        for k, bar in bars.items():
            pointvalue = self.instruments[k].pointvalue
            add = sum((bar.close - lot.price) * (1 if lot.side is Side.BUY else -1) * lot.qty * pointvalue
                      for lot in self.lots.values() if lot.leg_id == k and lot.kind == "add")
            marks[(k, "add")] = add
            marks[(k, "entry")] = self.brokers[k].open_pnl(bar.close) - add
        return marks

    def _cap_term(self, k, qty, mode, tier, values):
        """Whether the risk-sized leg's cap term wins the policy's min, from the production call.

        ``entry_quantities`` is called again with the risk term made unbounded (risk dollars a
        billion times the per-contract risk), so it returns the cap term alone; the formula is
        never re-implemented. The cap binds when the policy base equals it (a tie counts).
        """
        unbounded = dict(values, risk_dollars=Fraction(str(values["per_contract_risk"])) * 10**9)
        cap_only = entry_quantities(k, mode=mode, policy=self.policy, lifecycle_tier=tier, **unbounded)[0]
        return {"cap_only_policy": cap_only, "cap_binds": qty == cap_only}

    def _open_at_deadline(self, edge):
        """Each leg's open position, working orders, reservation and open lots by kind."""
        rows = {k: {"position": q} for k, q in edge.positions}
        for k, n in edge.working_orders:
            rows[k]["working_orders"] = n
        for k, n in edge.reservations:
            rows[k]["reserved"] = n
        for k, row in rows.items():
            row["lots"] = {kind: sum(lot.qty for lot in self.lots.values() if lot.leg_id == k and lot.kind == kind)
                           for kind in LOT_KINDS}
        return rows

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
                    if self._attribution is not None:
                        self._attribution.entry_fill(fill)
                else:
                    original = self.lots.get(fill.entry_fill_id)
                    if original is None or fill.qty > original.qty:
                        raise ReplayNeedsContext("exit lacks confirmed lot evidence")
                    direction = 1 if original.side is Side.BUY else -1
                    realized = ((fill.price - original.price) * direction * fill.qty
                                * self.instruments[k].pointvalue)
                    self.cash += realized
                    if self._attribution is not None:
                        self._attribution.exit_fill(fill, original.kind, realized)
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
        attribution = self._attribution
        before = None if attribution is None else (dict(attribution.cash), dict(attribution.commission))
        leg_marks = None if attribution is None else dict.fromkeys(attribution.cash, 0.0)
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

        def mark(fill, timing, trigger=None):
            value = contribution(fill, timing, trigger)
            if attribution is not None:
                leg_marks[(fill.leg_id, fill.kind)] += value
            return value

        adverse = sum(mark(f, "open") for f in carried)
        for f in entries:
            intent = pending[(f.leg_id, f.order_id)]
            b = bars[f.leg_id]
            at_open = (intent.order_type == "market" or
                       (b.open >= intent.price if f.side is Side.BUY else b.open <= intent.price))
            adverse += mark(f, "open" if at_open else "midbar", intent.price)
        value = cash_before + adverse - fees
        if attribution is not None:
            # The segment value replaces this segment's realized exits by lifetime marks, so a
            # leg's cash here is its cash before the segment less this segment's commissions.
            cash = {key: before[0][key] - (attribution.commission[key] - before[1][key]) for key in before[0]}
            attribution.observe("segment", self._index, self._path_time, value - self._opening, cash, leg_marks)
        return value

    def _capture_exposure(self, k):
        """One immutable exposure snapshot, enforcing the reservation invariant.

        The reservation equals the still-outstanding admitted entry/add
        quantity, and a positive reservation has a broker-pending order.
        Native evidence does not guarantee this for injected brokers.
        """
        from .model import ScheduleExposure
        exposure = ScheduleExposure(self.brokers[k].position(),
                                    bool(self.brokers[k].pending_order_ids()),
                                    self.ledger.reserved.get(k, 0))
        if exposure.reserved > 0 and not exposure.pending:
            raise ReplayNeedsContext("reservation without a broker-pending order has no ratified branch")
        outstanding = sum(intent.qty for (leg_id, _), (intent, _) in self.orders.items() if leg_id == k)
        if exposure.reserved != outstanding:
            raise ReplayNeedsContext(f"{k}: reserved {exposure.reserved} differs from outstanding {outstanding}"
                                     " admitted entry/add quantity")
        return exposure

    def _split(self, session, pb, bars, instant, exposures):
        """Validate each leg's ScheduleSplit; returns {leg: ScheduleSplit}.

        Both segments are validated even when the prefix does not execute.
        Execution is never inferred from timestamps, prices, volume or shape.
        """
        from .model import ScheduleExposure, ScheduleSplit
        provider = self.schedule_quotes
        splitter = getattr(provider, "split_bar", None)
        if splitter is None:
            raise ReplayNeedsContext("intrabar schedule requires split OHLC lifetime evidence")
        if any(hasattr(provider, name) for name in ("observe_exposure", "prefix_is_empty")):
            raise ReplayNeedsContext("schedule exposure side channels are not part of the split interface")
        splits = {}
        vertices, turns = accepted_path, path_turns
        for k, original in bars.items():
            exposure = exposures.get(k)
            if type(exposure) is not ScheduleExposure:
                raise ReplayNeedsContext("schedule split requires a captured exposure snapshot")
            if original.ts != pb.source_bar_time:
                interval_splitter = getattr(provider, "split_interval", None)
                if interval_splitter is None:
                    raise ReplayNeedsContext("multiple intrabar boundaries require interval split evidence")
                split = interval_splitter(session, pb, original, instant, k, exposure=exposure)
            else:
                split = splitter(session, pb, instant, k, exposure=exposure)
            if type(split) is not ScheduleSplit:
                raise ReplayNeedsContext("split provider must return one ScheduleSplit")
            prefix, suffix = split.prefix, split.suffix
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
            if prefix.close != provider(session, instant, k):
                raise ReplayNeedsContext("split boundary differs from schedule price")
            if turns(vertices(prefix) + vertices(suffix)) != turns(vertices(original)):
                raise ReplayNeedsContext("split evidence changes the accepted emulator path")
            splits[k] = split
        return splits

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
        if self._attribution is not None:
            self._attribution.reject(intent.leg_id, reason)
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
        # Sidecar row for a port entry/add request; _reject records its refusal reason.
        row = (self._attribution.request(k, intent.kind, intent.qty)
               if self._attribution is not None and intent.kind in ("entry", "add") else None)
        key = (k, intent.kind, pb.path_time)
        if key in self.accepted:
            self._log("duplicate_dropped", k, intent.kind)
            if row is not None:
                row["outcome"] = "duplicate_dropped"
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
            if row is not None:
                # The production policy's own return and an entry's inputs, recorded, never re-implemented.
                row.update(policy=qty, lifecycle_tier=tier)
                if intent.kind == "entry":
                    row["sizing_inputs"] = {name: str(value) for name, value in sorted(values.items())}
                if intent.kind == "entry" and "risk_dollars" in values:
                    row.update(self._cap_term(k, qty, mode, tier, values))
            if qty == 0:
                self._reject(intent, bar, "zero policy quantity")
                return
            if (k, intent.order_id) in self.orders:
                self._reject(intent, bar, "existing working order id")
                return
            if row is not None:
                row["capacity_before"] = {other: self.ledger.leg_micro(other) for other in sorted(self.brokers)}
            decision = self.ledger.request(k, qty)
            if row is not None:
                row.update(capacity_reason=decision.reason, micro_requested=decision.micro_requested)
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
                if row is not None:
                    row["takeover"] = {"displaced": list(takeover.plan.displaced),
                                       "cancel_acked": sorted(takeover.cancel_acked),
                                       "admitted": decision.admitted, "reason": decision.reason}
            if not decision.admitted:
                self._reject(intent, bar, decision.reason)
                return
            if row is not None:
                row.update(admitted=qty, outcome="admitted")
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
                if self._attribution is not None:
                    self._attribution.finish("deadline", self._index, self._path_time, self.cash - self._opening,
                                             self._open_at_deadline(edge))
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
            if self._attribution is not None:
                self._attribution.begin(session, mode)
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
                for (k, oid), (intent, created) in list(self.orders.items()):
                    if self._index - created > 1 and _one_bar_cancel_applies(k, intent):
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
                        # Frozen boundary order: snapshot exposure (after any
                        # earlier boundary's action), validate splits, execute
                        # only executing prefixes, act, then keep every suffix.
                        exposures = {k: self._capture_exposure(k) for k in exposed}
                        splits = self._split(session, pb, exposed, instant, exposures)
                        prefix = {}
                        for k, split in splits.items():
                            if split.prefix_executes is True:
                                prefix[k] = split.prefix
                            elif exposures[k].position or not exposures[k].pending or not (
                                    split.prefix.open == split.prefix.high == split.prefix.low
                                    == split.prefix.close):
                                # Only a pending-only leg may act before any
                                # price event, and a skipped prefix has one price.
                                raise ReplayNeedsContext("non-executing prefix requires a pending-only leg and one price")
                        segment_bars = {**segment_bars, **{k: split.suffix for k, split in splits.items()}}
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
                if self._attribution is not None:
                    self._attribution.bar_close(self._index, self._path_time, close_equity - opening,
                                                self._attribution_marks(bars))
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
            if self._attribution is not None:
                self._attribution.finish("settlement", self._index, self._path_time, self.cash - opening)
            self.clock.settle(session.path_session_date, max(0.0, self.cash))
            records.append(SessionRecord(session.occurrence, session.path_session_date,
                session.source.session_id, self.cash - opening, low,
                self.confirmed_fill_count - self._session_fill_start, flat, start, end))
        return ReplayResult(tuple(records), tuple(self.events))
