"""PR #356 review follow-ups (Codex, 2026-09-12): each finding as a failing-first test."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from c1_rail.book_policy import PolicyMismatch, is_protected, leg_quantities
from c1_signal_daemon.book_parity import ExportTrade, PortTrade, compare, load_effective_inputs
from c1_signal_daemon.book_protocol import Bracket, FillTiming, Mode, OrderIntent, Side
from c1_signal_daemon.feed import Bar
from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator
from dd_geometry import ProtectionPolicy

T0 = datetime(2026, 9, 14, 14, 0, tzinfo=timezone.utc)
LEG = "orb_mnq_v7"


def bar(i, o, h, l, c):
    return Bar(ts=T0 + timedelta(minutes=15 * i), open=o, high=h, low=l, close=c, volume=1.0)


def emu(**kw):
    base = dict(leg_id=LEG, mintick=0.25, pointvalue=2.0, slippage_ticks=1, commission_per_side=0.91)
    base.update(kw)
    return TVBrokerEmulator(**base)


def entry(oid, qty=1, *, order_type="market", price=None, timing=FillTiming.NEXT_OPEN, bracket=None,
          kind="entry", oca=None):
    return OrderIntent(order_id=oid, leg_id=LEG, kind=kind, side=Side.BUY, qty=qty, order_type=order_type,
                       price=price, timing=timing, bracket=bracket, oca_group=oca, bar_time=T0)


def fills(events):
    return [e.fill for e in events if e.event == "fill"]


# ── book_policy ──────────────────────────────────────────────────────────

def test_policy_outside_the_fixed_instance_halts():
    for bad in (ProtectionPolicy("trailing", 0.015, 0.40, "x"),
                ProtectionPolicy("trailing", 0.01, 0.50, "x"),
                ProtectionPolicy("static", 0.01, 0.40, "x")):
        with pytest.raises(PolicyMismatch):
            is_protected(99_000.0, 100_000.0, bad)
        with pytest.raises(PolicyMismatch):
            leg_quantities("aegis_6j", 8, mode=Mode.PROTECTED, policy=bad)


# ── emulator ─────────────────────────────────────────────────────────────

def test_trail_activates_on_a_gap_open_beyond_the_activation_level():
    e = emu()
    br = Bracket(stop=90.0, trail_activation_ticks=20, trail_offset_ticks=4)     # +5.0 / 1.0
    e.submit([entry("a", timing=FillTiming.THIS_CLOSE, bracket=br)], bar(0, 100, 100, 100, 100))   # 100.25
    got = e.process_bar(bar(1, 110, 110.5, 104, 105))     # opens above 105.25: activate at 110, extreme 110.5
    assert fills(got)[0].price == 109.25                  # (110.5 - 1.0) - slip


def test_marketable_next_open_stop_fills_at_the_next_open():
    e = emu()
    assert e.submit([entry("s", order_type="stop", price=105.0)], bar(0, 100, 111, 99, 110)) == []
    got = e.process_bar(bar(1, 100, 101, 99, 100.5))      # opens back under the level: still fills
    assert fills(got)[0].price == 100.25 and e.pending_order_ids() == []


def test_partial_explicit_exit_honours_quantity_fifo():
    e = emu()
    e.submit([entry("base", 2, timing=FillTiming.THIS_CLOSE)], bar(0, 100, 100, 100, 100))
    e.submit([entry("add", 2, kind="add", timing=FillTiming.THIS_CLOSE)], bar(1, 101, 101, 101, 101))
    intent = OrderIntent(order_id="x", leg_id=LEG, kind="exit", side=Side.SELL, qty=3,
                         timing=FillTiming.THIS_CLOSE, bar_time=T0)
    got = e.submit([intent], bar(2, 102, 102, 102, 102))
    assert [(f.qty, f.entry_fill_id[-2:]) for f in fills(got)] == [(2, ":1"), (1, ":2")]
    assert e.position() == 1


def test_immediate_fill_returns_oca_cancel_events():
    e = emu()
    got = e.submit([entry("l", order_type="stop", price=105.0, oca="G", timing=FillTiming.THIS_CLOSE),
                    entry("s", order_type="stop", price=200.0, oca="G", timing=FillTiming.THIS_CLOSE)],
                   bar(0, 100, 111, 99, 110))
    assert [x.event for x in got] == ["fill", "cancel"] and got[1].order_id == "s"


def test_exit_with_the_wrong_side_is_rejected_not_corrected():
    e = emu()
    e.submit([entry("base", 1, timing=FillTiming.THIS_CLOSE)], bar(0, 100, 100, 100, 100))
    wrong = OrderIntent(order_id="w", leg_id=LEG, kind="flat", side=Side.BUY, qty=None,
                        timing=FillTiming.THIS_CLOSE, bar_time=T0)
    got = e.submit([wrong], bar(1, 101, 101, 101, 101))
    assert got[0].event == "reject" and got[0].detail.startswith("exit_side_mismatch") and e.position() == 1


def test_margin_marks_existing_exposure_at_the_decision_price():
    e = emu(initial_capital=100_000.0, margin_pct=100.0, pointvalue=2.0)
    e.submit([entry("base", 2, timing=FillTiming.THIS_CLOSE)], bar(0, 20_000, 20_000, 20_000, 20_000))  # $80k
    # price +20 %: equity 116k, existing exposure marked 96k -> a 1-lot add ($48k) does not fit
    got = e.submit([entry("add", 1, kind="add", timing=FillTiming.THIS_CLOSE)], bar(1, 24_000, 24_000, 24_000, 24_000))
    assert got[0].event == "reject"


# ── parity harness ───────────────────────────────────────────────────────

def test_effective_inputs_are_digest_pinned(tmp_path, monkeypatch):
    from c1_signal_daemon.book_adapters import EFFECTIVE_INPUTS_SHA256
    assert len(EFFECTIVE_INPUTS_SHA256) == 64
    (tmp_path / "effective_inputs.json").write_text('{"aegis_6j": {"adapter": {"risk_pct": 9}}}', encoding="utf-8")
    monkeypatch.setenv("FP_PORT_ROOT", str(tmp_path))
    with pytest.raises(ValueError):
        load_effective_inputs()
    assert load_effective_inputs(verify=False)["aegis_6j"]["adapter"]["risk_pct"] == 9


def test_pnl_is_part_of_the_verdict():
    t0, t1 = datetime(2026, 9, 14, 10, 0), datetime(2026, 9, 14, 11, 0)
    exp = [ExportTrade(1, t0, "Long", 100.0, t1, "Exit", 101.0, 1, 123.0, 1.82)]
    prt = [PortTrade(t0, "entry", 100.0, t1, "stop", 101.0, 1, -999.0)]
    rep = compare("orb_mnq_v7", exp, prt, price_tol=0.01, window_start=t0, window_end=t1)
    assert rep.matched == 1 and rep.pnl_mismatches == 1 and not rep.passed


# ── round 2 (2026-09-12 16:05) ───────────────────────────────────────────

def test_open_entry_commission_reduces_margin_equity():
    # $100 capital, 100 % margin, $50 contract, $1 commission: after one fill $49 is left
    e = emu(initial_capital=100.0, margin_pct=100.0, pointvalue=1.0, commission_per_side=1.0, slippage_ticks=0)
    e.submit([entry("a", 1, timing=FillTiming.THIS_CLOSE)], bar(0, 50, 50, 50, 50))
    got = e.submit([entry("b", 1, kind="add", timing=FillTiming.THIS_CLOSE)], bar(1, 50, 50, 50, 50))
    assert got[0].event == "reject"


def test_pending_stop_snaps_with_pine_tie_breaking():
    e = emu()
    e.submit([entry("s", order_type="stop", price=100.125)], bar(0, 99, 99, 99, 99))   # halfway: 100.25, not 100.0
    assert e._pending_stop["s"].price == 100.25


def test_serialized_mode_values_are_honoured_and_junk_is_rejected():
    from c1_rail.book_policy import as_mode, candidate_book_protection_policy
    pol = candidate_book_protection_policy()
    assert leg_quantities("aegis_6j", 8, mode="protected", policy=pol) == (3, 0)
    assert leg_quantities("orb_mnq_v7", 1, mode="protected", policy=pol) == (1, 0)
    assert as_mode("normal") is Mode.NORMAL
    for junk in ("PROTECTED", "off", None, 1):
        with pytest.raises(ValueError):
            leg_quantities("aegis_6j", 8, mode=junk, policy=pol)


# ── round 3 (2026-09-12 16:23) — final bounded pass ─────────────────────

def test_close_quantity_must_be_none_or_positive_int():
    for bad in (0, -1, 1.5, True):
        with pytest.raises(ValueError):
            OrderIntent(order_id="x", leg_id=LEG, kind="exit", side=Side.SELL, qty=bad)
    OrderIntent(order_id="ok", leg_id=LEG, kind="flat", side=Side.SELL, qty=None)


def test_non_finite_values_fail_parity():
    t0, t1 = datetime(2026, 9, 14, 10, 0), datetime(2026, 9, 14, 11, 0)
    exp = [ExportTrade(1, t0, "Long", 100.0, t1, "Exit", 101.0, 1, 1.0, 0.0)]
    prt = [PortTrade(t0, "entry", 100.0, t1, "stop", 101.0, 1, float("nan"))]
    rep = compare("orb_mnq_v7", exp, prt, price_tol=0.01, window_start=t0, window_end=t1)
    assert not rep.passed and rep.pnl_mismatches == 1


def test_misrouted_cancel_and_amend_are_refused():
    from c1_signal_daemon.book_protocol import BracketAmend, Cancel
    e = emu()
    with pytest.raises(ValueError):
        e.submit([Cancel("aegis_6j", None)], bar(0, 100, 100, 100, 100))
    with pytest.raises(ValueError):
        e.submit([BracketAmend("aegis_6j", Bracket(stop=1.0))], bar(0, 100, 100, 100, 100))


def test_oca_siblings_cancelled_only_on_a_confirmed_fill():
    e = emu(initial_capital=10.0, margin_pct=100.0, pointvalue=1.0)   # nothing is affordable
    got = e.submit([entry("l", order_type="stop", price=105.0, oca="G", timing=FillTiming.THIS_CLOSE),
                    entry("s", order_type="stop", price=200.0, oca="G", timing=FillTiming.THIS_CLOSE)],
                   bar(0, 100, 111, 99, 110))
    assert [x.event for x in got] == ["reject"] and "s" in e.pending_order_ids()


def test_marketable_next_open_stop_in_an_oca_group_is_out_of_scope():
    e = emu()
    with pytest.raises(NotImplementedError):
        e.submit([entry("l", order_type="stop", price=105.0, oca="G")], bar(0, 100, 111, 99, 110))


def test_parity_cli_fails_when_panel_has_no_comparable_trades(monkeypatch, capsys):
    from c1_signal_daemon import book_adapters, book_parity
    t0, t1, t2 = datetime(2026, 9, 1), datetime(2026, 9, 2), datetime(2026, 9, 3)
    export = [ExportTrade(1, t0, "Long", 100.0, t1, "Exit", 101.0, 1, 1.0, 0.0)]
    # Keep real comparison and CLI verdict handling; replace private replay inputs.
    monkeypatch.setattr(book_parity, "load_effective_inputs", lambda: {})
    monkeypatch.setattr(book_parity, "parity_for", lambda leg_id, effective: compare(
        leg_id, export, [], price_tol=0.01, window_start=t2, window_end=t2))
    monkeypatch.setattr(book_adapters, "port_available", lambda leg_id: True)
    monkeypatch.setattr(book_adapters, "port_sha256", lambda leg_id: "0" * 64)
    assert book_parity.main(["--leg", "orb_mnq_v7"]) == 1
    output = capsys.readouterr().out
    assert "FAIL" in output and "PASS" not in output

