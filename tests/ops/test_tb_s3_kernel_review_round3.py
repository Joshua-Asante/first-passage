"""PR 365 review at 2eb6c12: composed outcomes, with external event expectations."""
from dataclasses import replace

import pytest

from book_protocol import Bracket
from tests.ops.tb_s3_kernel.broker import BrokerOrder
from tests.ops.tb_s3_kernel.harness import BAR, MIN, Sequence, entry, fill_lot, make_world
from tests.ops.test_tb_s3_kernel_redesign import Crash, crash_once


@pytest.mark.parametrize("reboot", [False, True])
def test_full_fill_exit_owns_the_entry_remainder_and_its_late_fill(reboot):
    """Zero current lot cannot discharge an exit while its entry can fill again."""
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 2, Bracket(stop=90)), w.now)
    lot = w.broker.fill(d.ref, qty=1)
    w.advance(MIN)
    w.snap()
    w.broker.inject["cancel"] = "defer"
    op = w.kernel.close("fill", lot, w.now, "exit")
    if reboot:
        Sequence.start(w).restart()
    w.advance(MIN)
    w.snap()
    op = w.kernel.operations[op.op_id]
    assert op.status != "complete"
    assert w.kernel.risk_add_blocked
    assert w.kernel.pending[d.ref].reserved == 1
    w.broker.fill(d.ref)  # cancellation loses the race; the full exit still owns this fill
    w.broker.execute_next()
    w.advance(MIN)
    w.snap()
    w.advance(MIN)
    w.snap()
    assert w.broker.positions["MGC"] == 0
    assert w.kernel.lots[lot].qty == 0
    assert op.status == "complete"
    assert w.kernel.pending[d.ref].reserved == 0


@pytest.mark.parametrize("reboot", [False, True])
def test_later_acquisition_cannot_replace_a_newer_position_timestamp(reboot):
    """A lagging full-read source cannot undo a newer position-only fact."""
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 1, Bracket(stop=90)), w.now)
    w.advance(MIN)
    old = w.broker.snapshot("MGC")
    w.advance(MIN)
    w.broker.fill(d.ref)
    newest = replace(w.broker.snapshot("MGC"), order_level=False)
    w.kernel.apply_evidence(newest)
    if reboot:
        Sequence.start(w).restart()
    lagging = replace(old, acquired=w.clock.tick())
    w.kernel.apply_evidence(lagging)
    assert w.kernel.position("MGC", w.now) == ("CONFIRMED", 1)
    assert w.kernel.p_ev["MGC"][1] == newest.as_of
    w.advance(MIN)
    w.snap()
    assert w.kernel.lots[w.broker.lot_id(d.ref)].qty == 1


def test_sequence_restart_preserves_sizing_for_new_admission():
    """Restart does not silently revert the configured quantity law to identity."""
    w = make_world(size=lambda _leg, qty: qty * 2)
    Sequence.start(w).restart()
    w.advance(MIN)
    w.snap()
    assert w.kernel.reconcile_restart(w.now).ok
    d = w.kernel.admit_entry(entry("vanguard_mgc", 1, Bracket(stop=90)), w.now)
    assert d.ok
    assert w.broker.orders[d.ref].qty == 2
    assert w.kernel.ledger.reserved["vanguard_mgc"] == 2


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


@pytest.mark.parametrize("outcome", ["defer", "unknown_lost", "reject"])
@pytest.mark.parametrize("reboot", [False, True])
def test_orphan_cancel_stays_owned_until_terminal_broker_evidence(outcome, reboot):
    """Accepted, lost and rejected orphan cancels cannot reopen account admission."""
    w = make_world()
    ref = "orphan-stop"
    w.broker.orders[ref] = BrokerOrder(ref, "MGC", "vanguard_mgc", "stop", "sell", 1,
                                     "stop", price=90)
    w.advance(MIN)
    w.snap()
    w.broker.inject["cancel"] = outcome
    d = w.kernel.cancel(ref, w.now)
    assert d.reason != "orphan_removed"
    assert w.kernel.risk_add_blocked
    if reboot:
        Sequence.start(w).restart()
    w.advance(MIN)
    w.snap()
    assert w.kernel.admit_entry(entry("orb_mnq_v7", 1), w.now).reason == "policy_block"
    if outcome == "defer":
        assert not w.kernel.cancel(ref, w.now).ok
        w.broker.execute_next()
    else:
        assert w.kernel.cancel(ref, w.now).ok
    assert w.kernel.risk_add_blocked  # route acceptance is still not terminal evidence
    w.advance(MIN)
    w.snap()
    if reboot:
        assert w.kernel.reconcile_restart(w.now).ok
    assert w.broker.orders[ref].status == "cancelled"
    assert not w.kernel.risk_add_blocked
    assert w.kernel.events("orphan_removed")


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


@pytest.mark.parametrize("scope", ["leg", "sym"])
@pytest.mark.parametrize("boundary", ["planned", "dispatching", "executed", "recorded"])
def test_broad_flat_crash_preserves_every_required_cancel(scope, boundary):
    """The first cancel's crash cannot lose another resting order's cancellation."""
    w = make_world()
    first = w.kernel.admit_entry(entry("vanguard_mgc", 1), w.now).ref
    second = w.kernel.admit_entry(entry("vanguard_mgc", 1, kind="add"), w.now).ref
    crash_once(w.kernel, "cancel", boundary)
    with pytest.raises(Crash):
        w.kernel.close(scope, "vanguard_mgc" if scope == "leg" else "MGC", w.now,
                       "exit", op_id="flat-two")
    Sequence.start(w).restart()
    w.kernel.progress(w.now)
    assert w.broker.orders[second].status == "cancelled"
    w.advance(MIN)
    w.snap()
    if boundary == "dispatching":
        assert w.kernel.cancel(first, w.now).ok
        w.advance(MIN)
        w.snap()
    assert w.broker.orders[first].status == "cancelled"
    assert w.kernel.operations["flat-two"].status == "complete"
    assert w.kernel.ledger.reserved["vanguard_mgc"] == 0


def test_fenced_pending_attach_absence_still_requires_contract_gap_recovery():
    """Rev 5.6 requires working protection after definition, not just a pending request."""
    w = make_world()
    lot = fill_lot(w, "dj30_mym_p250", 2)
    w.broker.inject["attach"] = "defer"
    op = w.kernel.amend(lot, Bracket(stop=90), w.now).op
    w.advance(MIN)
    ev = w.broker.snapshot("MYM")
    assert ev.pending_requests and not ev.working
    w.kernel.apply_evidence(ev)
    assert "protection_gap" in w.kernel.blocks
    assert w.broker.positions["MYM"] == 0
    w.broker.execute_next()  # a linked attach cannot open exposure after the close
    w.advance(MIN)
    w.snap()
    assert op.status == "complete"
    assert not w.broker.snapshot("MYM").working


@pytest.mark.parametrize("reboot", [False, True])
def test_orphan_cancel_fill_race_retains_ownership_through_recovery(reboot):
    """A terminal protective fill is not successful orphan removal if it opened exposure."""
    w = make_world()
    ref = "orphan-stop"
    w.broker.orders[ref] = BrokerOrder(ref, "MGC", "vanguard_mgc", "stop", "sell", 1,
                                     "stop", price=90)
    w.advance(MIN)
    w.snap()
    w.broker.inject["cancel"] = "defer"
    w.kernel.cancel(ref, w.now)
    if reboot:
        Sequence.start(w).restart()
    w.broker.trigger(ref)
    w.broker.execute_next()
    w.advance(MIN)
    w.snap()
    assert "unknown_order" in w.kernel.blocks
    assert w.broker.positions["MGC"] == 0  # owned recovery was sent on the new fill evidence
    w.advance(MIN)
    w.snap()
    if reboot:
        assert w.kernel.reconcile_restart(w.now).ok
    assert not w.kernel.risk_add_blocked


def test_consumed_amendment_does_not_strand_a_later_partial_entry_fill():
    """A consumed protective target resolves independently of its entry's remaining quantity."""
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 2, Bracket(stop=90)), w.now)
    lot = w.broker.fill(d.ref, qty=1)
    w.advance(MIN)
    w.snap()
    op = w.kernel.amend(lot, Bracket(stop=95), w.now).op
    w.broker.trigger(w.broker.lots[lot].protection["stop"])
    w.advance(MIN)
    w.snap()
    assert op.status == "complete"
    assert w.kernel.pending[d.ref].reserved == 1
    w.broker.fill(d.ref)
    w.advance(MIN)
    w.snap()
    assert w.kernel.amend(lot, Bracket(stop=96), w.now).ok
    w.advance(MIN)
    w.snap()
    assert w.kernel.expected[lot].intended["stop"] == {"price": 96}


def test_partial_orphan_recovery_counts_broker_exposure_and_retries_same_operation():
    """A partly closed orphan is real exposure even though no entry reserved it locally."""
    w = make_world()
    ref = "orphan-stop"
    w.broker.orders[ref] = BrokerOrder(ref, "MGC", "vanguard_mgc", "stop", "sell", 2,
                                     "stop", price=90)
    w.advance(MIN)
    w.snap()
    w.broker.inject["cancel"] = "defer"
    w.kernel.cancel(ref, w.now)
    w.broker.trigger(ref)
    w.broker.execute_next()
    w.broker.inject["close"] = ("partial", 1)
    w.advance(MIN)
    w.snap()
    w.advance(MIN)
    w.snap()
    recovery = next(o for o in w.kernel.operations.values() if o.kind == "CLOSE")
    assert recovery.status == "partial"
    assert w.broker.positions["MGC"] == -1
    w.kernel.retry(recovery.op_id, w.now)
    w.advance(MIN)
    w.snap()
    assert recovery.status == "complete"
    assert w.broker.positions["MGC"] == 0
    assert not w.kernel.risk_add_blocked


def test_full_close_can_retry_residual_first_observed_after_dispatch():
    """A completed route request with remaining exposure is retryable without a prior delta."""
    w = make_world()
    ref = "orphan-stop"
    w.broker.orders[ref] = BrokerOrder(ref, "MGC", "vanguard_mgc", "stop", "sell", 2,
                                     "stop", price=90)
    w.advance(MIN)
    w.snap()
    w.broker.inject["cancel"] = "defer"
    w.kernel.cancel(ref, w.now)
    w.broker.trigger(ref)
    w.broker.inject["close"] = ("partial", 1)
    op = w.kernel.close("sym", "MGC", w.now, "exit")
    w.broker.execute_next()
    w.advance(MIN)
    w.snap()
    assert op.status == "partial"
    assert w.broker.positions["MGC"] == -1
    w.kernel.retry(op.op_id, w.now)
    w.advance(MIN)
    w.snap()
    w.advance(MIN)
    w.snap()
    assert w.broker.positions["MGC"] == 0
    assert not w.kernel.risk_add_blocked
