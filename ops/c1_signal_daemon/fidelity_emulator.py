"""Re-price a frozen adapter replay under bounding execution semantics.

:class:`TVBrokerEmulator` reproduces TradingView's fills: the nearer-extreme-
first intrabar path, ``process_orders_on_close`` fills at the signal bar's
close, and take-profit limits filled on a touch. A native venue cannot obtain
those, so :class:`FidelityEmulator` changes only how orders fill, never what
the adapter decides:

* ``path_mode`` — ``tv`` is the parent unchanged; ``high_first`` / ``low_first``
  force every bar's intrabar path to O->H->L->C / O->L->H->C, bounding the
  unknown native path from both sides.
* ``next_open_fills`` — every ``THIS_CLOSE`` order becomes ``NEXT_OPEN`` and
  ``orders_on_close`` is off. A stop entry already through the close becomes a
  next-open market order replacing any working stop of its id; inside an OCA
  group (which the parent refuses) its fill cancels the siblings, as a stop
  fill does.
* ``limit_through_ticks`` — a take-profit triggers only once price trades that
  many ticks through the limit. The stored bracket limit is that trigger level,
  so the parent's gap, intrabar and at-close checks all require the
  trade-through; an intrabar trigger still fills at the limit, and a gap or
  close already through the trigger fills at that price, as in the parent.

Offline research tooling on adapter replays; nothing here emits or touches the
rail.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field, replace
from datetime import datetime

from c1_signal_daemon.book_protocol import Action, Bracket, ExecutionEvent, FillTiming, OrderIntent, Side
from c1_signal_daemon.feed import Bar
from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator, _OpenFill, run_adapter

PATH_MODES = ("tv", "high_first", "low_first")

MODES: dict[str, dict] = {
    "tv": {},
    "high_first": {"path_mode": "high_first"},
    "low_first": {"path_mode": "low_first"},
    "next_open": {"next_open_fills": True},
    "trade_through": {"limit_through_ticks": 1},
    "native_low": {"path_mode": "low_first", "next_open_fills": True, "limit_through_ticks": 1},
    "native_high": {"path_mode": "high_first", "next_open_fills": True, "limit_through_ticks": 1},
}


@dataclass
class FidelityEmulator(TVBrokerEmulator):
    path_mode: str = "tv"
    next_open_fills: bool = False
    limit_through_ticks: int = 0
    # converted OCA stops awaiting the next open (identity, not order_id)
    _converted: list[OrderIntent] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.path_mode not in PATH_MODES:
            raise ValueError(f"unknown path_mode {self.path_mode!r}; valid: {list(PATH_MODES)}")
        if (isinstance(self.limit_through_ticks, bool) or not isinstance(self.limit_through_ticks, int)
                or self.limit_through_ticks < 0):
            raise ValueError(f"limit_through_ticks must be a non-negative int, got {self.limit_through_ticks!r}")
        if self.next_open_fills:
            self.orders_on_close = False

    # ── adapter -> broker ────────────────────────────────────────────────
    def submit(self, actions: list[Action], bar: Bar) -> list[ExecutionEvent]:
        if self.next_open_fills:
            actions = [replace(a, timing=FillTiming.NEXT_OPEN)
                       if isinstance(a, OrderIntent) and a.timing is FillTiming.THIS_CLOSE else a
                       for a in actions]
        return super().submit(actions, bar)

    def _place(self, intent: OrderIntent, bar: Bar, crossed_now: list[str] | None = None) -> list[ExecutionEvent]:
        if (self.next_open_fills and intent.leg_id == self.leg_id and intent.kind in ("entry", "add")
                and intent.order_type == "stop"):
            crossed = (bar.close >= intent.price) if intent.side is Side.BUY else (bar.close <= intent.price)
            if crossed:
                # A re-issued id replaces its working stop, as the parent's THIS_CLOSE
                # path does through the _pending_stop key; its next-open path keeps both.
                self._pending_stop.pop(intent.order_id, None)
                market = replace(intent, order_type="market", price=None)
                self._pending_market.append(market)
                if intent.oca_group is not None:
                    self._converted.append(market)
                return []
        return super()._place(intent, bar, crossed_now)

    def _rounded(self, br: Bracket | None, *, long: bool = True) -> Bracket | None:
        br = super()._rounded(br, long=long)
        if br is None or br.limit is None or not self.limit_through_ticks:
            return br
        through = self.limit_through_ticks * self.mintick
        return replace(br, limit=self._snap(br.limit + through if long else br.limit - through))

    # ── bar processing ───────────────────────────────────────────────────
    def process_bar(self, bar: Bar) -> list[ExecutionEvent]:
        if self.path_mode == "tv" and not self._converted:
            return super().process_bar(bar)
        # TVBrokerEmulator.process_bar with two changes: a converted stop's fill
        # at the open cancels its OCA siblings before anything else can fill,
        # and the intrabar path comes from path_mode.
        start = len(self.events)
        bar = Bar(ts=bar.ts, open=self._snap(bar.open), high=self._snap(bar.high),
                  low=self._snap(bar.low), close=self._snap(bar.close), volume=bar.volume)
        self._last_bar = bar
        queued, self._pending_market = self._pending_market, []
        converted, self._converted = self._converted, []
        filled_groups: set[str] = set()
        for intent in queued:
            if intent.kind in ("exit", "flat"):
                self._close_scope(intent, bar.open, bar.ts, slip=True)
            elif not any(intent is c for c in converted):
                self._fill_entry(intent, bar.open, bar.ts, slip=True)
            elif intent.oca_group in filled_groups:
                self._emit("cancel", bar.ts, order_id=intent.order_id, detail="oca_cancel")
            elif self._fill_entry(intent, bar.open, bar.ts, slip=True).event == "fill":
                filled_groups.add(intent.oca_group)
                self._cancel_oca(intent, bar.ts)
        self._at_open(bar)
        seq = self._path(bar.open, bar.high, bar.low, bar.close)
        for a, b in zip(seq, seq[1:]):
            if a != b:
                self._segment(a, b, bar)
        return self.events[start:]

    def _path(self, o: float, h: float, l: float, c: float) -> list[float]:
        if self.path_mode == "high_first":
            return [o, h, l, c]
        if self.path_mode == "low_first":
            return [o, l, h, c]
        return [o, h, l, c] if (h - o) <= (o - l) else [o, l, h, c]

    def _fill_exit(self, of: _OpenFill, price: float, ts: datetime, *, slip: bool, reason: str,
                   order_id: str | None = None, kind: str = "exit") -> ExecutionEvent | None:
        if reason == "limit" and self.limit_through_ticks:
            # triggered at the stored trade-through level; the order fills at its limit
            through = self.limit_through_ticks * self.mintick
            price = self._snap(of.bracket.limit - through if of.is_long else of.bracket.limit + through)
        return super()._fill_exit(of, price, ts, slip=slip, reason=reason, order_id=order_id, kind=kind)


def replay(make_adapter, bars, emulator_kwargs: dict, mode: str = "tv", *, on_bar_hook=None) -> FidelityEmulator:
    """Replay a fresh adapter from ``make_adapter()`` under one of :data:`MODES`."""
    emu = FidelityEmulator(**{**emulator_kwargs, **MODES[mode]})
    return run_adapter(make_adapter(), bars, emu, on_bar_hook=on_bar_hook)


def summarize(emu: TVBrokerEmulator) -> dict:
    trades = len(emu.closed_trades)
    net = emu.realized_net()
    return {
        "trades": trades,
        "net": net,
        "mean_net": net / trades if trades else 0.0,
        "rejects": len(emu.rejected),
        "exit_reasons": dict(Counter(t.exit.reason for t in emu.closed_trades)),
    }


def _outcomes(emu: TVBrokerEmulator) -> dict[tuple, tuple]:
    by_entry: dict[tuple, list] = {}
    for t in emu.closed_trades:
        key = (t.entry.bar_time, t.entry.order_id, t.entry.side, t.entry.kind)
        by_entry.setdefault(key, []).append((t.exit.bar_time, t.exit.price, t.exit.reason, t.exit.qty))
    return {k: tuple(sorted(v)) for k, v in by_entry.items()}


def bracket(make_adapter, bars, emulator_kwargs: dict, *, modes=None, on_bar_hook=None) -> dict:
    """Run every mode; report each mode's summary and the path-sensitive entry count.

    ``path_sensitive_entries`` counts entries (bar time, order id, side, kind)
    whose exits differ between ``high_first`` and ``low_first``, including an
    entry present in only one of them; None unless both modes ran.
    """
    names = list(MODES) if modes is None else list(modes)
    bars = list(bars)
    runs = {m: replay(make_adapter, bars, emulator_kwargs, m, on_bar_hook=on_bar_hook) for m in names}
    flips = None
    if "high_first" in runs and "low_first" in runs:
        hi, lo = _outcomes(runs["high_first"]), _outcomes(runs["low_first"])
        flips = sum(1 for k in hi.keys() | lo.keys() if hi.get(k) != lo.get(k))
    return {"modes": {m: summarize(e) for m, e in runs.items()}, "path_sensitive_entries": flips}
