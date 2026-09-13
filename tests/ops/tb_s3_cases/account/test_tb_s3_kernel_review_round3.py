"""PR 365 review at 2eb6c12: composed outcomes, with external event expectations."""


from dataclasses import replace


import pytest


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.broker import BrokerOrder


from tests.ops.tb_s3_kernel.account_harness import BAR, MIN, Sequence, entry, fill_lot, make_world


from tests.ops.tb_s3_cases.support.test_tb_s3_kernel_redesign import Crash, crash_once


def test_sequence_restart_preserves_sizing_for_takeover_settlement():
    """The pending takeover is checked against the same injected sizing host after restart."""
    w = make_world(size=lambda leg, qty: qty * 2 if leg == "aegis_6j" else qty)
    fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    request = entry("aegis_6j", 4, Bracket(stop=0.0069))
    plan = w.kernel.admit_entry(request, w.now).takeover
    assert plan is not None
    w.kernel.takeover(plan, w.now)
    Sequence.start(w).restart()
    w.advance(MIN)
    w.snap()
    assert w.kernel.reconcile_restart(w.now).ok
    d = w.kernel.settle_takeover(request, w.now)
    assert d.ok
    assert w.broker.orders[d.ref].qty == 8


@pytest.mark.parametrize("stop,want", [(80, "suppressed"), (95, "sent")])
def test_daemon_reissue_classifies_fixed_stop_before_stale_control_gate(stop, want):
    """Fresh broker state does not replace the daemon's required risk-add control read."""
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 1, Bracket(stop=90))
    w.advance(BAR + MIN)
    w.snap()
    assert not w.daemon.emit_risk_add(w.now)
    result = w.daemon.reissue("vanguard_mgc", lot, {"stop": stop}, 100, w.now)
    assert result == want
    ref = w.broker.lots[lot].protection["stop"]
    assert w.broker.orders[ref].price == (90 if stop == 80 else 95)


@pytest.mark.parametrize("offset,want", [(30, "suppressed"), (10, "sent")])
def test_daemon_reissue_classifies_trail_before_stale_control_gate(offset, want):
    """Wider trail reissues need fresh control; tightening remains available."""
    w = make_world()
    lot = fill_lot(w, "orb_mnq_v7", 1,
                   Bracket(trail_activation_ticks=40, trail_offset_ticks=20))
    w.advance(BAR + MIN)
    w.snap()
    result = w.daemon.reissue("orb_mnq_v7", lot,
                             {"trail_activation_ticks": 40, "trail_offset_ticks": offset}, 100, w.now)
    assert result == want
    ref = w.broker.lots[lot].protection["trail"]
    assert w.broker.orders[ref].trail_offset == (20 if offset == 30 else 10)
