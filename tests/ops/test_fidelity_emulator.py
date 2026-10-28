"""Bounding execution semantics of ops/c1_signal_daemon/fidelity_emulator.py on synthetic bars.

Synthetic only: a toy breakout adapter stands in for a strategy port, so no
private input is read.
"""
from __future__ import annotations

import random
from collections import deque
from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from c1_signal_daemon.book_protocol import Bracket, ExecutionEvent, FillTiming, OrderIntent, Side
from c1_signal_daemon.feed import Bar
from c1_signal_daemon.fidelity_emulator import MODES, FidelityEmulator, bracket, replay, summarize
from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator, run_adapter

T0 = datetime(2026, 9, 14, 14, 0, tzinfo=timezone.utc)
LEG = "toy_breakout"
TICK = 0.25
KW = dict(leg_id=LEG, mintick=TICK, pointvalue=2.0, slippage_ticks=1, commission_per_side=0.91)
THIS_CLOSE, NEXT_OPEN = FillTiming.THIS_CLOSE, FillTiming.NEXT_OPEN


def bar(i: int, o: float, h: float, l: float, c: float) -> Bar:
    return Bar(ts=T0 + timedelta(minutes=15 * i), open=o, high=h, low=l, close=c, volume=1.0)


def order(oid: str, side: Side = Side.BUY, *, order_type="market", price=None, timing=NEXT_OPEN,
          bracket=None, oca=None, kind="entry") -> OrderIntent:
    qty = None if kind in ("exit", "flat") else 1
    return OrderIntent(order_id=oid, leg_id=LEG, kind=kind, side=side, qty=qty, order_type=order_type,
                       price=price, timing=timing, bracket=bracket, oca_group=oca, bar_time=T0)


def fills(events: list[ExecutionEvent]):
    return [e.fill for e in events if e.event == "fill"]


def random_bars(n: int = 600, seed: int = 7) -> list[Bar]:
    rng = random.Random(seed)
    px, out = 100.0, []
    for i in range(n):
        o = px + TICK * rng.choice((0, 0, 0, 1, -1, 6, -6))      # occasional gaps
        h = o + TICK * rng.randint(0, 16)
        l = o - TICK * rng.randint(0, 16)
        c = l + TICK * rng.randint(0, round((h - l) / TICK))
        out.append(bar(i, o, h, l, c))
        px = c
    return out


class ToyBreakout:
    """Prior-bar channel breakout both ways in one OCA group: THIS_CLOSE stop
    entries (marketable when the close is already through the channel), a
    trailing bracket, and a THIS_CLOSE time stop."""

    leg_id = LEG

    def __init__(self, lookback: int = 6, hold: int = 4):
        self.highs: deque[float] = deque(maxlen=lookback)
        self.lows: deque[float] = deque(maxlen=lookback)
        self.hold = hold
        self.pos = 0
        self.held = 0

    def on_execution(self, ev: ExecutionEvent) -> None:
        if ev.event == "fill":
            self.pos += ev.fill.qty if ev.fill.side is Side.BUY else -ev.fill.qty

    def on_bar(self, b: Bar) -> list:
        acts = []
        if self.pos:
            self.held += 1
            if self.held >= self.hold:
                acts.append(order("time", Side.SELL if self.pos > 0 else Side.BUY, kind="flat", timing=THIS_CLOSE))
        elif len(self.highs) == self.highs.maxlen:
            self.held = 0
            hh, ll = max(self.highs), min(self.lows)
            trail = dict(trail_activation_ticks=12, trail_offset_ticks=8)
            acts += [order("L", Side.BUY, order_type="stop", price=hh + TICK, timing=THIS_CLOSE, oca="brk",
                           bracket=Bracket(stop=hh - 6.0, limit=hh + 4.0, **trail)),
                     order("S", Side.SELL, order_type="stop", price=ll - TICK, timing=THIS_CLOSE, oca="brk",
                           bracket=Bracket(stop=ll + 6.0, limit=ll - 4.0, **trail))]
        self.highs.append(b.high)
        self.lows.append(b.low)
        return acts


@pytest.mark.parametrize("orders_on_close", (False, True))
def test_tv_mode_reproduces_the_parent_trade_for_trade(orders_on_close):
    bars = random_bars()
    kw = dict(KW, orders_on_close=orders_on_close)
    parent = run_adapter(ToyBreakout(), bars, TVBrokerEmulator(**kw))
    tv = replay(ToyBreakout, bars, kw, "tv")
    assert len(parent.closed_trades) > 50
    assert {"stop", "limit", "flat", "stop_gap"} <= {t.exit.reason for t in parent.closed_trades}
    assert tv.closed_trades == parent.closed_trades
    assert tv.events == parent.events and tv.rejected == parent.rejected == []


def test_forced_path_bounds_a_trailing_exit():
    kw = dict(leg_id=LEG, mintick=1.0, pointvalue=1.0, slippage_ticks=0, commission_per_side=0.0)
    br = Bracket(stop=95.0, trail_activation_ticks=4, trail_offset_ticks=2)
    got = {}
    for mode in ("high_first", "low_first", "tv"):
        e = FidelityEmulator(**kw, **MODES[mode])
        e.submit([order("a", timing=THIS_CLOSE, bracket=br)], bar(0, 100, 100, 100, 100))
        got[mode] = [f.price for f in fills(e.process_bar(bar(1, 100, 108, 94, 101)))]
    # high first: trail activates at 104, follows to 108, stops at 106; low first: fixed stop 95
    assert got == {"high_first": [106.0], "low_first": [95.0], "tv": [95.0]}   # tv: open nearer the low


def test_next_open_moves_a_this_close_market_entry_to_the_next_open():
    e = FidelityEmulator(**KW, orders_on_close=True, **MODES["next_open"])
    assert e.orders_on_close is False
    assert e.submit([order("a", timing=THIS_CLOSE)], bar(0, 100, 101, 99, 100.5)) == []
    assert e.pending_order_ids() == ["a"]
    b1 = bar(1, 102, 103, 101, 102.5)
    assert [(f.price, f.bar_time) for f in fills(e.process_bar(b1))] == [(102.25, b1.ts)]   # open + slip


def test_close_marketable_oca_stop_entry_fills_at_the_next_open_and_cancels_siblings():
    b0 = bar(0, 100, 104, 99, 103)
    pair = [order("l", Side.BUY, order_type="stop", price=102.0, timing=THIS_CLOSE, oca="G"),
            order("s", Side.SELL, order_type="stop", price=98.0, timing=THIS_CLOSE, oca="G")]
    assert [f.price for f in fills(FidelityEmulator(**KW).submit(pair, b0))] == [103.25]   # tv: this close
    with pytest.raises(NotImplementedError):                     # the parent refuses the next-open shape
        FidelityEmulator(**KW).submit([replace(pair[0], timing=NEXT_OPEN)], b0)
    e = FidelityEmulator(**KW, **MODES["next_open"])
    assert e.submit(pair, b0) == []
    got = e.process_bar(bar(1, 101, 101.5, 97, 100))             # the sibling's 98 would fill intrabar
    assert [(x.event, x.order_id, x.detail) for x in got] == [("fill", "l", ""), ("cancel", "s", "oca_cancel")]
    assert fills(got)[0].price == 101.25 and e.position() == 1 and e.pending_order_ids() == []
    # both sides through the close: the first fills, its converted sibling is cancelled
    e = FidelityEmulator(**KW, **MODES["next_open"])
    e.submit([pair[0], replace(pair[1], price=104.0)], b0)
    got = e.process_bar(bar(1, 101, 101.5, 97, 100))
    assert [(x.event, x.order_id, x.detail) for x in got] == [("fill", "l", ""), ("cancel", "s", "oca_cancel")]
    assert e.position() == 1


def test_next_open_conversion_replaces_the_working_stop_of_its_id():
    e = FidelityEmulator(**KW, **MODES["next_open"])
    e.submit([order("L", order_type="stop", price=105.0, timing=THIS_CLOSE)], bar(0, 100, 101, 99, 100))
    e.submit([order("L", order_type="stop", price=102.0, timing=THIS_CLOSE)], bar(1, 100, 103, 99, 103))
    assert e.pending_order_ids() == ["L"]
    assert [f.price for f in fills(e.process_bar(bar(2, 103, 106, 102, 105)))] == [103.25]
    assert e.position() == 1                                     # the stale 105 stop is gone


def test_trade_through_needs_a_tick_beyond_the_limit_and_fills_at_the_limit():
    br = Bracket(stop=90.0, limit=105.0)
    bars = [bar(1, 101, 105, 100.5, 105),       # touches 105 intrabar and closes on it
            bar(2, 105, 105, 104, 104.5),       # opens on it
            bar(3, 104.5, 105.25, 104, 105)]    # trades one tick through

    def run(mode):
        e = FidelityEmulator(**KW, orders_on_close=True, **MODES[mode])
        e.submit([order("a", timing=THIS_CLOSE, bracket=br)], bar(0, 100, 100, 100, 100))
        return [[(f.price, f.reason) for f in fills(e.process_bar(b) + e.submit([], b))] for b in bars]

    assert run("tv") == [[(105.0, "limit")], [], []]
    assert run("trade_through") == [[], [], [(105.0, "limit")]]


def test_bracket_runs_every_mode_without_rejects():
    bars = random_bars()
    rep = bracket(ToyBreakout, bars, KW)
    assert set(rep["modes"]) == set(MODES)
    for name, s in rep["modes"].items():
        assert s["rejects"] == 0 and s["trades"] > 0, name
        assert sum(s["exit_reasons"].values()) == s["trades"], name
        assert s["mean_net"] == pytest.approx(s["net"] / s["trades"]), name
    assert rep["path_sensitive_entries"] > 0
    assert rep["modes"]["tv"] == summarize(replay(ToyBreakout, bars, KW))


def test_invalid_settings_are_refused():
    with pytest.raises(ValueError, match="path_mode"):
        FidelityEmulator(**KW, path_mode="random")
    with pytest.raises(ValueError, match="limit_through_ticks"):
        FidelityEmulator(**KW, limit_through_ticks=-1)
