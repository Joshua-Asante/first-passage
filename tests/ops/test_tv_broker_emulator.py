"""TradingView fill semantics of ops/c1_signal_daemon/tv_broker_emulator.py on synthetic bars.

Each rule below was pinned by a captured export during Track B parity (four
legs, every trade matched); the synthetic cases keep them from drifting.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from c1_signal_daemon.book_protocol import (
    Bracket, BracketAmend, Cancel, ExecutionEvent, FillTiming, OrderIntent, Side,
)
from c1_signal_daemon.feed import Bar
from c1_signal_daemon.pine_ta import ET, Ema, Rma, Stdev, pine_round, tv_daily_key
from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator

T0 = datetime(2026, 9, 14, 14, 0, tzinfo=timezone.utc)
LEG = "orb_mnq_v7"


def bar(i: int, o: float, h: float, l: float, c: float) -> Bar:
    return Bar(ts=T0 + timedelta(minutes=15 * i), open=o, high=h, low=l, close=c, volume=1.0)


def emu(**kw) -> TVBrokerEmulator:
    base = dict(leg_id=LEG, mintick=0.25, pointvalue=2.0, slippage_ticks=1, commission_per_side=0.91)
    base.update(kw)
    return TVBrokerEmulator(**base)


def entry(oid: str, qty: int = 1, *, order_type="market", price=None, timing=FillTiming.NEXT_OPEN,
          bracket=None, kind="entry", oca=None) -> OrderIntent:
    return OrderIntent(order_id=oid, leg_id=LEG, kind=kind, side=Side.BUY, qty=qty, order_type=order_type,
                       price=price, timing=timing, bracket=bracket, oca_group=oca, bar_time=T0)


def flat(oid: str, timing=FillTiming.NEXT_OPEN) -> OrderIntent:
    return OrderIntent(order_id=oid, leg_id=LEG, kind="flat", side=Side.SELL, qty=None, timing=timing, bar_time=T0)


def fills(events: list[ExecutionEvent]):
    return [e.fill for e in events if e.event == "fill"]


def test_market_timing_and_slippage():
    e = emu()
    b0 = bar(0, 100, 101, 99, 100.5)
    got = e.submit([entry("a", timing=FillTiming.THIS_CLOSE)], b0)
    assert fills(got)[0].price == 100.75                  # this close + 1 tick
    e2 = emu()
    assert e2.submit([entry("b")], b0) == []              # next-open: queued
    got = e2.process_bar(bar(1, 102, 103, 101, 102.5))
    assert fills(got)[0].price == 102.25 and fills(got)[0].bar_time == bar(1, 0, 0, 0, 0).ts


def test_stop_entry_fills_at_level_or_at_open_after_gap_and_activates_when_crossed():
    e = emu()
    e.submit([entry("s", order_type="stop", price=105.0, timing=FillTiming.THIS_CLOSE)], bar(0, 100, 104, 99, 103))
    got = e.process_bar(bar(1, 103, 106, 102, 104))
    assert fills(got)[0].price == 105.25                  # level + slip, intrabar
    e = emu()
    e.submit([entry("g", order_type="stop", price=105.0)], bar(0, 100, 104, 99, 103))
    got = e.process_bar(bar(1, 107, 108, 106, 107))
    assert fills(got)[0].price == 107.25                  # gap: fills at the open
    e = emu()
    got = e.submit([entry("c", order_type="stop", price=102.0, timing=FillTiming.THIS_CLOSE)], bar(0, 100, 104, 99, 103))
    assert fills(got)[0].price == 103.25                  # already crossed: activates at the close (poc)


def test_bracket_levels_slippage_and_long_stop_floor_rounding():
    e = emu()
    br = Bracket(stop=98.30, limit=110.0)
    e.submit([entry("a", timing=FillTiming.THIS_CLOSE, bracket=br)], bar(0, 100, 101, 99, 100))
    got = e.process_bar(bar(1, 100, 100.5, 97, 98))      # path O->H->L->C, stop then
    f = fills(got)[0]
    assert f.kind == "exit" and f.price == 98.0           # floor(98.30 -> 98.25) - slip
    e = emu()
    e.submit([entry("b", timing=FillTiming.THIS_CLOSE, bracket=br)], bar(0, 100, 101, 99, 100))
    got = e.process_bar(bar(1, 100, 111, 99, 110))
    assert fills(got)[0].price == 110.0                   # limit: no slippage


def test_trailing_activates_then_follows_and_can_fill_on_the_activation_bar():
    e = emu()
    br = Bracket(stop=90.0, limit=200.0, trail_activation_ticks=20, trail_offset_ticks=4)   # +5.0 / 1.0
    e.submit([entry("a", timing=FillTiming.THIS_CLOSE, bracket=br)], bar(0, 100, 100, 100, 100))   # fill 100.25
    got = e.process_bar(bar(1, 100, 104, 99, 103))        # 105.25 not reached
    assert fills(got) == []
    got = e.process_bar(bar(2, 103, 108, 101, 102))       # O closer to L -> O->L->H->C: activate at 105.25, extreme 108
    assert fills(got)[0].price == 106.75                  # (108 - 1.0) - slip, on the same bar


def test_fifo_attribution_and_persistent_sibling_orders():
    e = emu()
    br = Bracket(stop=90.0, trail_activation_ticks=8, trail_offset_ticks=2)          # +2.0 / 0.5
    e.submit([entry("base", 2, timing=FillTiming.THIS_CLOSE, bracket=br)], bar(0, 100, 100, 100, 100))   # 100.25
    e.submit([entry("add", 2, kind="add", timing=FillTiming.THIS_CLOSE, bracket=br)], bar(1, 99, 99, 99, 99))  # 99.25 (lower)
    got = e.process_bar(bar(2, 99, 101.5, 98, 99))        # add activates at 101.25, extreme 101.5, stop 101.0 -> fill 100.75
    f = fills(got)
    assert len(f) == 1 and f[0].qty == 2 and f[0].entry_fill_id.endswith(":1")   # FIFO: the BASE lot closes
    assert e.position() == 2                              # add lot remains, covered by the base's order
    got = e.process_bar(bar(3, 99, 103, 98, 98.5))        # base order activates at 102.25 -> stop 102.5 -> 102.25
    f = fills(got)
    assert len(f) == 1 and f[0].price == 102.25 and e.position() == 0


def test_consumed_order_is_not_recreated_but_a_bare_lot_gets_one():
    e = emu()
    br = Bracket(stop=95.0)
    e.submit([entry("base", 1, timing=FillTiming.THIS_CLOSE, bracket=br)], bar(0, 100, 100, 100, 100))
    e.submit([entry("add", 1, kind="add", timing=FillTiming.THIS_CLOSE, bracket=Bracket(stop=99.0))], bar(1, 100, 100, 100, 100))
    got = e.process_bar(bar(2, 100, 100.5, 98.9, 100))    # add's 99.0 stop fires -> FIFO closes the base lot
    assert fills(got)[0].entry_fill_id.endswith(":1") and e.position() == 1
    e.submit([BracketAmend(LEG, Bracket(stop=99.5))], bar(2, 100, 100.5, 98.9, 100))
    # the add's own order is consumed; the base's order (stop 95 -> amended 99.5) still covers the add lot
    got = e.process_bar(bar(3, 100, 100.2, 99.4, 100))
    assert fills(got)[0].price == 99.25 and e.position() == 0
    e2 = emu()
    e2.submit([entry("bare", 1, timing=FillTiming.THIS_CLOSE)], bar(0, 100, 100, 100, 100))   # no bracket (Striker base)
    assert e2.process_bar(bar(1, 100, 100, 80, 90)) == [] and e2.position() == 1
    e2.submit([BracketAmend(LEG, Bracket(stop=85.0))], bar(1, 100, 100, 80, 90))
    got = e2.process_bar(bar(2, 90, 91, 84, 88))
    assert fills(got)[0].price == 84.75


def test_oca_cancel_and_explicit_cancel():
    e = emu()
    e.submit([entry("l", order_type="stop", price=105.0, oca="G"),
              entry("s", order_type="stop", price=104.0, oca="G")], bar(0, 100, 101, 99, 100))
    got = e.process_bar(bar(1, 100, 106, 100, 105))
    assert [x.event for x in got] == ["fill", "cancel"]
    assert got[1].order_id == "l" and got[1].detail == "oca_cancel"
    e2 = emu()
    e2.submit([entry("p", order_type="stop", price=105.0)], bar(0, 100, 101, 99, 100))
    got = e2.submit([Cancel(LEG, None)], bar(1, 100, 101, 99, 100))
    assert got[0].event == "cancel" and e2.pending_order_ids() == []


def test_margin_rejects_unaffordable_add_pine_v6_default():
    e = emu(initial_capital=100_000.0, margin_pct=100.0, pointvalue=2.0)
    e.submit([entry("base", 2, timing=FillTiming.THIS_CLOSE)], bar(0, 20_000, 20_000, 20_000, 20_000))  # $80,001
    got = e.submit([entry("add", 2, kind="add", timing=FillTiming.THIS_CLOSE)], bar(1, 20_000, 20_000, 20_000, 20_000))
    assert got[0].event == "reject" and got[0].detail == "insufficient_margin" and e.position() == 2
    e_off = emu(initial_capital=100_000.0, margin_pct=0.0, pointvalue=2.0)
    e_off.submit([entry("base", 2, timing=FillTiming.THIS_CLOSE)], bar(0, 20_000, 20_000, 20_000, 20_000))
    got = e_off.submit([entry("add", 2, kind="add", timing=FillTiming.THIS_CLOSE)], bar(1, 20_000, 20_000, 20_000, 20_000))
    assert got[0].event == "fill" and e_off.position() == 4


def test_next_open_close_is_sized_when_issued():
    e = emu()
    e.submit([entry("base", 2, timing=FillTiming.THIS_CLOSE)], bar(0, 100, 100, 100, 100))
    e.submit([entry("add", 2, kind="add"), flat("eod")], bar(1, 100, 100, 100, 100))   # add + close issued together
    got = e.process_bar(bar(2, 101, 101, 101, 101))
    kinds = [f.kind for f in fills(got)]
    assert kinds == ["add", "flat"] and e.position() == 2     # the add filled at the open and survives


def test_orders_on_close_evaluates_a_crossed_stop_at_the_close():
    e = emu(orders_on_close=True)
    e.submit([entry("base", 1, timing=FillTiming.THIS_CLOSE)], bar(0, 100, 100, 100, 100))
    b1 = bar(1, 100, 100, 95, 96)
    e.process_bar(b1)
    got = e.submit([BracketAmend(LEG, Bracket(stop=98.0))], b1)   # issued at a close already through it
    assert fills(got)[0].reason == "stop_close" and fills(got)[0].price == 95.75


def test_pine_helpers():
    assert pine_round(2.5) == 3 and pine_round(-2.5) == -3 and pine_round(1.4999) == 1
    r = Rma(3)
    assert r.update(1.0) is None and r.update(2.0) is None and r.update(3.0) == 2.0   # SMA seed
    assert abs(r.update(5.0) - (2.0 * 2 / 3 + 5.0 / 3)) < 1e-12
    e = Ema(3)
    assert e.update(10.0) == 10.0 and abs(e.update(20.0) - 15.0) < 1e-12               # first-value seed
    s = Stdev(2)
    assert s.update(1.0) is None and s.update(3.0) == 1.0                              # population stdev


def test_tv_daily_key_merges_holiday_sessions():
    def at(y, m, d, hh, mm=0):
        return datetime(y, m, d, hh, mm, tzinfo=ET)
    assert tv_daily_key(at(2023, 1, 15, 18)) == date(2023, 1, 17)    # Sunday reopen before MLK -> Tuesday's bar
    assert tv_daily_key(at(2023, 1, 16, 18)) == date(2023, 1, 17)    # MLK evening reopen: no new daily bar
    assert tv_daily_key(at(2023, 1, 17, 18)) == date(2023, 1, 18)
    assert tv_daily_key(at(2026, 7, 2, 18)) == date(2026, 7, 6)      # Fri 07-03 holiday, weekend -> Monday
    assert tv_daily_key(at(2026, 7, 5, 18)) == date(2026, 7, 6)
    assert tv_daily_key(at(2024, 12, 25, 18)) == date(2024, 12, 26)  # Christmas evening reopen -> 12-26's bar
    assert tv_daily_key(at(2023, 7, 3, 18)) == date(2023, 7, 5)      # July 4 has no bar; Mon 18:00 starts Wed's
    assert tv_daily_key(at(2026, 9, 15, 18)) == date(2026, 9, 16)    # ordinary Tuesday evening
