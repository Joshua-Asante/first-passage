"""Offline broker emulator with TradingView fill semantics (Track B, TB-S3 (H)/(M)).

The four fixed-book adapters emit :class:`OrderIntent`s and learn their
position only from the :class:`ExecutionEvent`s this emulator (or, live, the
broker) confirms. Replaying an adapter through this emulator on the frozen
CME panels must reproduce the captured TradingView export — that parity is
the adapter's acceptance test, so the semantics below are TradingView's
broker emulator as documented and as evidenced by the exports:

* Intrabar path without bar magnifier: open -> high -> low -> close when the
  open is closer to the high, else open -> low -> high -> close; no gaps
  inside a bar; a level crossed in the gap between bars fills at the open.
* Market orders: ``THIS_CLOSE`` (process_orders_on_close=true) fills at the
  generating bar's close; ``NEXT_OPEN`` fills at the next bar's open.
* A buy-stop entry already at or below the market when generated activates
  immediately (fills at the generating close for THIS_CLOSE scripts, else at
  the next open).
* Slippage (ticks) applies to market and stop fills, never to limit fills.
* One exit bracket per entry fill; stop / limit / trailing evaluated along
  the path; trailing activates when the activation level is reached and then
  follows the extreme by the offset; the effective stop is the tighter of the
  fixed stop and the trailing stop.
* Commission is cash per contract per side.

SCOPE (fixed at PR #356 review close, 2026-09-12): this is the offline
replay broker for the four ported bodies, judged by exact parity against
their pinned exports plus the tests in tests/ops. It is not a general broker.
Order shapes none of the four adapters emits are refused fail-closed at
submit (``NotImplementedError``) rather than modelled: a marketable next-open
stop that belongs to an OCA group is the one such shape identified so far.

Deliberately NOT modelled: bar magnifier, partial fills, margin calls, order
rejects other than insufficient margin. Partial fills and rejects are the live broker's outcomes and reach
the adapter through the same event path (TB-S3 (M)); tests inject them.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from datetime import datetime

from c1_signal_daemon.book_protocol import (
    Action,
    Bracket,
    BracketAmend,
    Cancel,
    ExecutionEvent,
    Fill,
    FillTiming,
    OrderIntent,
    Side,
)
from c1_signal_daemon.feed import Bar
from c1_signal_daemon.pine_ta import pine_round


@dataclass
class _OpenFill:
    fill: Fill
    bracket: Bracket | None
    fill_seq: int = 0
    lot_qty: int = 0          # contracts of this entry lot still open (FIFO accounting)
    bracket_qty: int = 0      # contracts this exit order covers (its entry's quantity)
    bracket_consumed: bool = False   # this entry's exit order has filled; never re-created
    trail_active: bool = False
    trail_extreme: float | None = None

    @property
    def is_long(self) -> bool:
        return self.fill.side is Side.BUY


@dataclass(frozen=True)
class ClosedTrade:
    entry: Fill
    exit: Fill
    gross_pnl: float
    commission: float

    @property
    def net_pnl(self) -> float:
        return self.gross_pnl - self.commission


@dataclass
class TVBrokerEmulator:
    leg_id: str
    mintick: float
    pointvalue: float
    slippage_ticks: int
    commission_per_side: float
    # Pine v6 strategy() defaults margin_long/margin_short to 100 (v5 defaulted 0):
    # a body that omits them cannot fill an entry/add whose value exceeds the
    # equity not already committed to open positions. 0 disables the check.
    initial_capital: float = 100_000.0
    margin_pct: float = 0.0
    # process_orders_on_close=true scripts: an exit order issued at a bar's close
    # whose level is already crossed by that close activates at once and fills
    # at the close (evidence: Striker 'Exit Long' one bar after entry when the
    # next close is through the stop).
    orders_on_close: bool = False
    rejected: list[OrderIntent] = field(default_factory=list)
    events: list[ExecutionEvent] = field(default_factory=list)
    closed_trades: list[ClosedTrade] = field(default_factory=list)
    _pending_market: list[OrderIntent] = field(default_factory=list)
    _pending_stop: dict[str, OrderIntent] = field(default_factory=dict)
    _open: dict[str, _OpenFill] = field(default_factory=dict)
    _seq: int = 0
    _last_bar: Bar | None = None

    # ── public state views ───────────────────────────────────────────────
    @property
    def open_fills(self) -> list[Fill]:
        return [o.fill for o in self._open.values() if o.lot_qty > 0]

    def position(self) -> int:
        return sum(o.lot_qty if o.is_long else -o.lot_qty for o in self._open.values())

    def position_avg_price(self) -> float | None:
        qty = sum(o.lot_qty for o in self._open.values())
        if qty == 0:
            return None
        return sum(o.fill.price * o.lot_qty for o in self._open.values()) / qty

    def open_pnl(self, price: float) -> float:
        total = 0.0
        for o in self._open.values():
            direction = 1.0 if o.is_long else -1.0
            total += (price - o.fill.price) * direction * self.pointvalue * o.lot_qty
        return total

    def realized_net(self) -> float:
        return sum(t.net_pnl for t in self.closed_trades)

    def pending_order_ids(self) -> list[str]:
        return [i.order_id for i in self._pending_market] + list(self._pending_stop)

    # ── adapter -> broker ────────────────────────────────────────────────
    def submit(self, actions: list[Action], bar: Bar) -> list[ExecutionEvent]:
        """Register the adapter's actions generated at ``bar``'s close."""
        out: list[ExecutionEvent] = []
        crossed_now: list[str] = []
        for act in actions:
            if getattr(act, "leg_id", None) != self.leg_id:
                raise ValueError(f"action for {getattr(act, 'leg_id', None)!r} sent to "
                                 f"{self.leg_id!r} emulator: {type(act).__name__}")
            if isinstance(act, Cancel):
                out.extend(self._cancel(act, bar))
            elif isinstance(act, BracketAmend):
                self._amend(act)
            elif isinstance(act, OrderIntent):
                out.extend(self._place(act, bar, crossed_now))
            else:  # pragma: no cover - defensive
                raise TypeError(f"unknown action {act!r}")
        # Stops already through the close activate only after EVERY order of this
        # script run is registered, so an OCA sibling placed later in the same
        # run is cancelled by the fill (TradingView places the run's orders together).
        for oid in crossed_now:
            intent = self._pending_stop.pop(oid, None)
            if intent is None:
                continue        # cancelled by an earlier sibling's fill
            start = len(self.events)
            ev = self._fill_entry(intent, bar.close, bar.ts, slip=True)
            if ev.event == "fill":
                self._cancel_oca(intent, bar.ts)   # siblings go only on a confirmed fill
            out.extend(self.events[start:])
        if self.orders_on_close:
            out.extend(self._evaluate_at_close(bar))
        return out

    def _evaluate_at_close(self, bar: Bar) -> list[ExecutionEvent]:
        start = len(self.events)
        c, ts = self._snap(bar.close), bar.ts
        for fid, of in list(self._open.items()):
            if fid not in self._open or of.bracket is None:
                continue
            br = of.bracket
            if of.is_long:
                stop = self._long_effective_stop(of)
                if stop is not None and c <= stop:
                    self._fill_exit(of, c, ts, slip=True, reason="stop_close"); continue
                if br.limit is not None and c >= br.limit:
                    self._fill_exit(of, c, ts, slip=False, reason="limit_close")
            else:
                stop = self._short_effective_stop(of)
                if stop is not None and c >= stop:
                    self._fill_exit(of, c, ts, slip=True, reason="stop_close"); continue
                if br.limit is not None and c <= br.limit:
                    self._fill_exit(of, c, ts, slip=False, reason="limit_close")
        return self.events[start:]

    def _place(self, intent: OrderIntent, bar: Bar, crossed_now: list[str] | None = None) -> list[ExecutionEvent]:
        if intent.leg_id != self.leg_id:
            raise ValueError(f"intent for {intent.leg_id!r} sent to {self.leg_id!r} emulator")
        if intent.kind in ("exit", "flat"):
            bad = self._close_side_mismatch(intent)
            if bad:
                self.rejected.append(intent)
                return [self._emit("reject", bar.ts, order_id=intent.order_id, detail=bad)]
            if intent.timing is FillTiming.THIS_CLOSE:
                return self._close_scope(intent, bar.close, bar.ts, slip=True)
            # A next-open close is sized at the position that exists when it is
            # issued (Vanguard: an add issued on the same bar fills at that open
            # and survives until the next bar's close order).
            if intent.scope_fill_ids is None:
                intent = replace(intent, scope_fill_ids=tuple(
                    fid for fid, o in self._open.items() if o.lot_qty > 0))
            self._pending_market.append(intent)
            return []
        if intent.order_type == "market":
            if intent.timing is FillTiming.THIS_CLOSE:
                return [self._fill_entry(intent, bar.close, bar.ts, slip=True)]
            self._pending_market.append(intent)
            return []
        # stop entry
        crossed = (bar.close >= intent.price) if intent.side is Side.BUY else (bar.close <= intent.price)
        if crossed:
            # "a stop order at a better value than the current market price activates
            # immediately": THIS_CLOSE scripts fill at this close (after the whole
            # script run is registered - see submit), others at the next open.
            if intent.timing is FillTiming.THIS_CLOSE:
                self._pending_stop[intent.order_id] = replace(intent, price=self._tick(intent.price))
                if crossed_now is not None:
                    crossed_now.append(intent.order_id)
                return []
            if intent.oca_group is not None:
                raise NotImplementedError(
                    "marketable next-open stop inside an OCA group: no fixed-book adapter "
                    "emits this shape; refused fail-closed (emulator scope)")
            self._pending_market.append(replace(intent, order_type="market", price=None))
            return []
        self._pending_stop[intent.order_id] = replace(intent, price=self._tick(intent.price))
        return []

    def _close_side_mismatch(self, intent: OrderIntent) -> str:
        """An exit must oppose every lot it targets; a same-side 'exit' would ADD live."""
        lots = [o for o in self._open.values() if o.lot_qty > 0
                and (intent.scope_fill_ids is None or o.fill.fill_id in intent.scope_fill_ids)]
        for o in lots:
            closing = Side.SELL if o.is_long else Side.BUY
            if intent.side is not closing:
                return f"exit_side_mismatch:{intent.side.value}_vs_{o.fill.side.value}_lot"
        return ""

    def _cancel(self, act: Cancel, bar: Bar) -> list[ExecutionEvent]:
        out = []
        ids = ([act.order_id] if act.order_id is not None
               else list(self._pending_stop) + [i.order_id for i in self._pending_market
                                                  if i.kind in ("entry", "add")])
        for oid in ids:
            if oid in self._pending_stop:
                del self._pending_stop[oid]
                out.append(self._emit("cancel", bar.ts, order_id=oid, detail="cancelled"))
            else:
                before = len(self._pending_market)
                self._pending_market = [i for i in self._pending_market if i.order_id != oid]
                if len(self._pending_market) != before:
                    out.append(self._emit("cancel", bar.ts, order_id=oid, detail="cancelled"))
        return out

    def _cancel_oca(self, filled: OrderIntent, ts: datetime) -> None:
        if filled.oca_group is None:
            return
        for oid, other in list(self._pending_stop.items()):
            if other.oca_group == filled.oca_group and oid != filled.order_id:
                del self._pending_stop[oid]
                self._emit("cancel", ts, order_id=oid, detail="oca_cancel")

    def _snap(self, price: float) -> float:
        """Canonical float for an on-tick price so equal levels compare equal
        (1/x arithmetic and CSV parsing can differ in the last bits)."""
        return round(price, 10)

    def _tick(self, price: float | None) -> float | None:
        """Pine math.round to the tick: ties away from zero, not Python's ties-to-even."""
        if price is None:
            return None
        return self._snap(pine_round(price / self.mintick) * self.mintick)

    def _tick_floor(self, price: float | None) -> float | None:
        if price is None:
            return None
        return self._snap(math.floor(price / self.mintick + 1e-9) * self.mintick)

    def _tick_ceil(self, price: float | None) -> float | None:
        if price is None:
            return None
        return self._snap(math.ceil(price / self.mintick - 1e-9) * self.mintick)

    def _rounded(self, br: Bracket | None, *, long: bool = True) -> Bracket | None:
        """TV snaps bracket levels to the tick AWAY from the market for the holder:
        a long's protective stop is floored (evidence: ORB stop fills at floor-0.25
        on every non-tick stop level in the captured export); mirrored for shorts."""
        if br is None:
            return None
        if long:
            return replace(br, stop=self._tick_floor(br.stop), limit=self._tick_ceil(br.limit))
        return replace(br, stop=self._tick_ceil(br.stop), limit=self._tick_floor(br.limit))

    def _amend(self, act: BracketAmend) -> None:
        """Pine re-calls strategy.exit every bar.

        Evidence from the captured ORB export (three days where base and add
        left on different bars): exit orders belong to their ORIGINAL entry
        order and persist with their own trailing state after a sibling fills
        (FIFO closes the oldest lot, whichever order triggered); an order that
        has filled is not re-created while the position lasts. So an amend
        modifies live orders' levels, attaches an order to a lot that never had
        one (Striker issues its exit a bar after the entry), and leaves a
        consumed order dead.
        """
        for fid, o in self._open.items():
            if act.scope_fill_ids is not None and fid not in act.scope_fill_ids:
                continue
            if o.bracket is not None:
                o.bracket = self._rounded(act.bracket, long=o.is_long)
            elif not o.bracket_consumed and o.lot_qty > 0:
                o.bracket = self._rounded(act.bracket, long=o.is_long)
                o.bracket_qty = o.lot_qty
                o.trail_active = False
                o.trail_extreme = None

    # ── bar processing (before the adapter sees the bar) ──────────────────
    def process_bar(self, bar: Bar) -> list[ExecutionEvent]:
        start = len(self.events)
        bar = Bar(ts=bar.ts, open=self._snap(bar.open), high=self._snap(bar.high),
                  low=self._snap(bar.low), close=self._snap(bar.close), volume=bar.volume)
        self._last_bar = bar
        # 1. queued market orders fill at the open
        queued, self._pending_market = self._pending_market, []
        for intent in queued:
            if intent.kind in ("exit", "flat"):
                self._close_scope(intent, bar.open, bar.ts, slip=True)
            else:
                self._fill_entry(intent, bar.open, bar.ts, slip=True)
        # 2. gap handling at the open
        self._at_open(bar)
        # 3. intrabar path
        o, h, l, c = bar.open, bar.high, bar.low, bar.close
        seq = [o, h, l, c] if (h - o) <= (o - l) else [o, l, h, c]
        for a, b in zip(seq, seq[1:]):
            if a != b:
                self._segment(a, b, bar)
        return self.events[start:]

    def _at_open(self, bar: Bar) -> None:
        o, ts = bar.open, bar.ts
        for oid, intent in list(self._pending_stop.items()):
            if oid not in self._pending_stop:
                continue
            crossed = (o >= intent.price) if intent.side is Side.BUY else (o <= intent.price)
            if crossed:
                del self._pending_stop[oid]
                if self._fill_entry(intent, o, ts, slip=True).event == "fill":
                    self._cancel_oca(intent, ts)
        for fid, of in list(self._open.items()):
            if fid not in self._open or of.bracket is None:
                continue
            br = of.bracket
            if of.is_long:
                stop = self._long_effective_stop(of)
                if stop is not None and o <= stop:
                    self._fill_exit(of, o, ts, slip=True, reason="stop_gap"); continue
                if br.limit is not None and o >= br.limit:
                    self._fill_exit(of, o, ts, slip=False, reason="limit_gap"); continue
                self._activate_trail_if_crossed(of, o)
                self._trail_touch(of, o, up=True)
            else:
                stop = self._short_effective_stop(of)
                if stop is not None and o >= stop:
                    self._fill_exit(of, o, ts, slip=True, reason="stop_gap"); continue
                if br.limit is not None and o <= br.limit:
                    self._fill_exit(of, o, ts, slip=False, reason="limit_gap"); continue
                self._activate_trail_if_crossed(of, o)
                self._trail_touch(of, o, up=False)

    def _segment(self, a: float, b: float, bar: Bar) -> None:
        up = b > a
        cur = a
        ts = bar.ts
        while True:
            best_level: float | None = None
            best = None   # ("stop_entry", intent) | ("exit", of, kind)
            # candidate: pending stop entries
            for intent in self._pending_stop.values():
                lvl = intent.price
                if intent.side is Side.BUY and up and cur <= lvl <= b:
                    cand = lvl
                elif intent.side is Side.SELL and not up and b <= lvl <= cur:
                    cand = lvl
                else:
                    continue
                if best_level is None or (cand < best_level if up else cand > best_level):
                    best_level, best = cand, ("stop_entry", intent)
            # candidate: open-fill exits
            for of in self._open.values():
                if of.bracket is None:
                    continue
                for kind, lvl in self._exit_levels(of, up):
                    if lvl is None:
                        continue
                    if up and cur <= lvl <= b:
                        cand = lvl
                    elif (not up) and b <= lvl <= cur:
                        cand = lvl
                    else:
                        continue
                    if best_level is None or (cand < best_level if up else cand > best_level):
                        best_level, best = cand, ("exit", of, kind)
            if best is None:
                break
            cur = best_level
            if best[0] == "stop_entry":
                intent = best[1]
                del self._pending_stop[intent.order_id]
                if self._fill_entry(intent, best_level, ts, slip=True).event == "fill":
                    self._cancel_oca(intent, ts)
            else:
                _, of, kind = best
                if kind == "trail_activate":
                    of.trail_active = True
                    of.trail_extreme = best_level
                elif kind == "limit":
                    self._fill_exit(of, best_level, ts, slip=False, reason="limit")
                else:
                    self._fill_exit(of, best_level, ts, slip=True, reason=kind)
        # end of segment: trailing extremes follow the move
        for of in self._open.values():
            self._trail_touch(of, b, up=up)

    def _exit_levels(self, of: _OpenFill, up: bool):
        br = of.bracket
        if of.is_long:
            if up:
                yield "limit", br.limit
                if (br.trail_activation_ticks is not None and not of.trail_active):
                    yield "trail_activate", self._snap(of.fill.price + br.trail_activation_ticks * self.mintick)
            else:
                yield "stop", self._long_effective_stop(of)
        else:
            if not up:
                yield "limit", br.limit
                if (br.trail_activation_ticks is not None and not of.trail_active):
                    yield "trail_activate", self._snap(of.fill.price - br.trail_activation_ticks * self.mintick)
            else:
                yield "stop", self._short_effective_stop(of)

    def _long_effective_stop(self, of: _OpenFill) -> float | None:
        br = of.bracket
        levels = []
        if br.stop is not None:
            levels.append(br.stop)
        if of.trail_active and br.trail_offset_ticks is not None and of.trail_extreme is not None:
            levels.append(self._snap(of.trail_extreme - br.trail_offset_ticks * self.mintick))
        return max(levels) if levels else None

    def _short_effective_stop(self, of: _OpenFill) -> float | None:
        br = of.bracket
        levels = []
        if br.stop is not None:
            levels.append(br.stop)
        if of.trail_active and br.trail_offset_ticks is not None and of.trail_extreme is not None:
            levels.append(self._snap(of.trail_extreme + br.trail_offset_ticks * self.mintick))
        return min(levels) if levels else None

    def _activate_trail_if_crossed(self, of: _OpenFill, price: float) -> None:
        """A bar opening beyond the activation level activates the trail there (gap rule)."""
        br = of.bracket
        if br is None or of.trail_active or br.trail_activation_ticks is None:
            return
        if of.is_long and price >= self._snap(of.fill.price + br.trail_activation_ticks * self.mintick):
            of.trail_active, of.trail_extreme = True, price
        elif (not of.is_long) and price <= self._snap(of.fill.price - br.trail_activation_ticks * self.mintick):
            of.trail_active, of.trail_extreme = True, price

    def _trail_touch(self, of: _OpenFill, price: float, *, up: bool) -> None:
        """Let an active trail follow a favourable extreme (long: highs, short: lows)."""
        if of.bracket is None or not of.trail_active:
            return
        if of.is_long and up:
            of.trail_extreme = max(of.trail_extreme, price)
        elif (not of.is_long) and (not up):
            of.trail_extreme = min(of.trail_extreme, price)

    # ── fills ─────────────────────────────────────────────────────────────
    def _slipped(self, price: float, side: Side, slip: bool) -> float:
        if not slip or self.slippage_ticks == 0:
            return self._snap(price)
        delta = self.slippage_ticks * self.mintick
        return self._snap(price + delta if side is Side.BUY else price - delta)

    def _affordable(self, intent: OrderIntent, fill_price: float) -> bool:
        if self.margin_pct <= 0:
            return True
        # Equity and the margin already committed are both marked at the price the
        # decision is taken at (the captured ORB export is reproduced exactly under
        # either marking; marking both at the same price is the consistent choice).
        open_commission = sum(o.fill.commission * (o.lot_qty / o.fill.qty)
                              for o in self._open.values() if o.fill.qty > 0)
        equity = (self.initial_capital + self.realized_net() + self.open_pnl(fill_price)
                  - open_commission)          # fees already charged on the open lots
        used = sum(fill_price * self.pointvalue * o.lot_qty for o in self._open.values())
        used *= self.margin_pct / 100.0
        need = fill_price * self.pointvalue * intent.qty * self.margin_pct / 100.0
        return need <= equity - used

    def _fill_entry(self, intent: OrderIntent, price: float, ts: datetime, *, slip: bool) -> ExecutionEvent:
        fill_price = self._slipped(price, intent.side, slip)
        if not self._affordable(intent, fill_price):
            self.rejected.append(intent)
            return self._emit("reject", ts, order_id=intent.order_id, detail="insufficient_margin")
        self._seq += 1
        fill = Fill(
            fill_id=f"{self.leg_id}:{self._seq}", order_id=intent.order_id, leg_id=self.leg_id,
            kind=intent.kind, side=intent.side, qty=intent.qty,
            price=fill_price, bar_time=ts,
            commission=self.commission_per_side * intent.qty, reason=intent.reason,
        )
        self._open[fill.fill_id] = _OpenFill(fill=fill, bracket=self._rounded(intent.bracket, long=intent.side is Side.BUY),
                                             fill_seq=self._seq, lot_qty=fill.qty,
                                             bracket_qty=fill.qty if intent.bracket is not None else 0)
        return self._emit("fill", ts, fill=fill, order_id=intent.order_id)

    def _fill_exit(self, of: _OpenFill, price: float, ts: datetime, *, slip: bool, reason: str,
                   order_id: str | None = None, kind: str = "exit") -> ExecutionEvent | None:
        """Execute the exit order held by bracket ``of``.

        TradingView semantics evidenced by the captured ORB export:
        * entries close FIFO (close_entries_rule="FIFO" default) - the filled
          quantity comes off the OLDEST open lots whichever order triggered;
        * every strategy.exit order belongs to one strategy.oca.reduce group -
          a fill reduces the sibling orders by the filled quantity (cancelling
          them at zero); the next strategy.exit call re-creates a fresh order for
          any lot left uncovered (see _amend).
        """
        side = Side.SELL if of.is_long else Side.BUY
        fill_price = self._slipped(price, side, slip)
        remaining = min(of.bracket_qty, sum(o.lot_qty for o in self._open.values() if o.is_long == of.is_long))
        filled_total = 0
        lots = sorted((o for o in self._open.values() if o.lot_qty > 0 and o.is_long == of.is_long),
                      key=lambda o: o.fill_seq)
        last_event: ExecutionEvent | None = None
        for lot in lots:
            if remaining <= 0:
                break
            take = min(lot.lot_qty, remaining)
            self._seq += 1
            fill = Fill(
                fill_id=f"{self.leg_id}:{self._seq}", order_id=order_id or f"bracket:{of.fill.fill_id}",
                leg_id=self.leg_id, kind=kind, side=side, qty=take, price=fill_price, bar_time=ts,
                entry_fill_id=lot.fill.fill_id, commission=self.commission_per_side * take,
                reason=reason,
            )
            direction = 1.0 if lot.is_long else -1.0
            gross = (fill.price - lot.fill.price) * direction * self.pointvalue * take
            entry_comm = self.commission_per_side * take
            entry_fill = (replace(lot.fill, qty=take, commission=entry_comm)
                          if take != lot.fill.qty else lot.fill)
            self.closed_trades.append(ClosedTrade(entry_fill, fill, gross, entry_comm + fill.commission))
            lot.lot_qty -= take
            remaining -= take
            filled_total += take
            last_event = self._emit("fill", ts, fill=fill, order_id=fill.order_id)
        of.bracket = None
        of.bracket_qty = 0
        of.bracket_consumed = True
        for fid in [fid for fid, o in self._open.items() if o.lot_qty == 0 and o.bracket is None]:
            del self._open[fid]
        if not any(o.lot_qty > 0 for o in self._open.values()):
            self._open.clear()
        return last_event

    def _close_scope(self, intent: OrderIntent, price: float, ts: datetime, *, slip: bool) -> list[ExecutionEvent]:
        out = []
        lots = sorted((o for o in self._open.values() if o.lot_qty > 0), key=lambda o: o.fill_seq)
        if intent.scope_fill_ids is not None:
            lots = [o for o in lots if o.fill.fill_id in intent.scope_fill_ids]
        remaining = intent.qty if intent.qty is not None else sum(o.lot_qty for o in lots)
        for lot in lots:
            if remaining <= 0:
                break
            side = Side.SELL if lot.is_long else Side.BUY
            fill_price = self._slipped(price, side, slip)
            take = min(lot.lot_qty, remaining)
            remaining -= take
            self._seq += 1
            fill = Fill(
                fill_id=f"{self.leg_id}:{self._seq}", order_id=intent.order_id, leg_id=self.leg_id,
                kind=intent.kind, side=side, qty=take, price=fill_price, bar_time=ts,
                entry_fill_id=lot.fill.fill_id, commission=self.commission_per_side * take,
                reason=intent.reason or intent.kind,
            )
            direction = 1.0 if lot.is_long else -1.0
            gross = (fill.price - lot.fill.price) * direction * self.pointvalue * take
            entry_comm = self.commission_per_side * take
            entry_fill = (replace(lot.fill, qty=take, commission=entry_comm)
                          if take != lot.fill.qty else lot.fill)
            self.closed_trades.append(ClosedTrade(entry_fill, fill, gross, entry_comm + fill.commission))
            lot.lot_qty -= take
            out.append(self._emit("fill", ts, fill=fill, order_id=fill.order_id))
        if not any(o.lot_qty > 0 for o in self._open.values()):
            self._open.clear()
        else:
            for fid in [fid for fid, o in self._open.items() if o.lot_qty == 0]:
                del self._open[fid]
        return out

    def _emit(self, event: str, ts: datetime, *, fill: Fill | None = None,
              order_id: str | None = None, detail: str = "") -> ExecutionEvent:
        ev = ExecutionEvent(event=event, leg_id=self.leg_id, bar_time=ts, fill=fill,
                            order_id=order_id, detail=detail)
        self.events.append(ev)
        return ev


def run_adapter(adapter, bars, emulator: TVBrokerEmulator, *, on_bar_hook=None) -> TVBrokerEmulator:
    """Drive an adapter through bars: broker fills first, then the adapter evaluates.

    ``on_bar_hook(bar)`` (optional) runs before each bar — the replay uses it to
    switch the protection mode at session boundaries.
    """
    for bar in bars:
        if on_bar_hook is not None:
            for act in on_bar_hook(bar) or []:
                for ev in emulator.submit([act], bar):
                    adapter.on_execution(ev)
        for ev in emulator.process_bar(bar):
            adapter.on_execution(ev)
        actions = adapter.on_bar(bar)
        for ev in emulator.submit(actions, bar):
            adapter.on_execution(ev)
    return emulator
