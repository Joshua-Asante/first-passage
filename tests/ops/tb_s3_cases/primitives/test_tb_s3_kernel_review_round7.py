"""PR365 at23cf0e1: complete histories, gross exposure, future requests and bracket reissues."""


from dataclasses import replace


import pytest


from book_protocol import Bracket, BracketAmend


from tests.ops.tb_s3_kernel.broker import STALENESS_WINDOW


from tests.ops.tb_s3_kernel.harness import MIN, Sequence, entry, fill_lot, make_world


from tests.ops.tb_s3_cases.support.test_tb_s3_kernel_redesign import Crash, crash_once


def offsetting_lots(w):
    """Actual buy1/sell1 executions, zero net position, two open lots."""
    d = w.kernel.admit_entry(entry("vanguard_mgc", 2), w.now)
    w.broker.fill(d.ref, 1)
    w.advance(MIN)
    w.snap()
    w.broker.orders[d.ref].side = "sell"
    w.broker.fill(d.ref)
    w.advance(MIN)
    w.snap()
    assert w.broker.positions["MGC"] == 0
    assert sum(l.qty for l in w.broker.lots.values()) == 2


def defer_external(w, request_id, sym="MGC"):
    """An accepted external risk-add has no local reservation, effect or working ref yet."""
    w.broker.inject["place"] = "defer"
    w.broker.request("place", request_id, sym=sym, leg_id="external", kind="entry",
                     side="buy", qty=99, ref=request_id + "-order")


@pytest.mark.parametrize("reboot", [False, True])
@pytest.mark.parametrize("at_boundary", [False, True])
def test_new_execution_cannot_predate_a_previously_complete_history(reboot, at_boundary):
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 1), w.now)
    absent_id = w.clock.tick()
    w.advance(MIN)
    complete = w.broker.snapshot("MGC")
    w.kernel.apply_evidence(complete)
    if reboot:
        Sequence.start(w).restart()
    w.broker.fill(d.ref)
    w.advance(MIN)
    ev = w.broker.snapshot("MGC")
    history = tuple(replace(e, execution_id=complete.acquired if at_boundary else absent_id)
                    for e in ev.executions)
    w.kernel.apply_evidence(replace(ev, executions=history))
    assert w.kernel.risk_add_blocked
    assert w.kernel.ledger.confirmed.get("vanguard_mgc", 0) == 0
    assert not [e for e in w.kernel.telemetry if e["kind"] == "fill"]


def test_later_execution_after_a_complete_empty_read_is_allocated_once_after_restart():
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 2), w.now)
    w.advance(MIN)
    w.snap()
    Sequence.start(w).restart()
    w.broker.fill(d.ref, 1)
    w.advance(MIN)
    ev = w.broker.snapshot("MGC")
    w.kernel.apply_evidence(ev)
    w.kernel.apply_evidence(ev)
    assert w.kernel.ledger.confirmed["vanguard_mgc"] == 1
    assert w.kernel.ledger.reserved["vanguard_mgc"] == 1


@pytest.mark.parametrize("reboot", [False, True])
def test_unowned_accepted_request_blocks_admission_before_a_working_order_exists(reboot):
    w = make_world()
    defer_external(w, "external-request")
    w.advance(MIN)
    w.snap()
    if reboot:
        Sequence.start(w).restart()
        w.advance(MIN)
        w.snap()
        w.kernel.reconcile_restart(w.now)
    assert not w.kernel.quiescent("MGC", w.now)
    assert w.kernel.risk_add_blocked
    assert not w.kernel.admit_entry(entry("dj30_mym_p250", 1), w.now).ok


@pytest.mark.parametrize("old", [Bracket(stop=90, limit=120),
                                 Bracket(stop=90, trail_activation_ticks=40, trail_offset_ticks=20)])
@pytest.mark.parametrize("new", [Bracket(stop=95), Bracket()])
def test_replacement_removing_a_component_is_refused_without_partial_application(old, new):
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 1, old)
    original = dict(w.kernel.expected[lot].intended)
    refs = dict(w.broker.lots[lot].protection)
    assert w.kernel.amend_action(lot, new, w.now) is None
    assert not w.kernel.amend(lot, new, w.now).ok
    assert w.kernel.expected[lot].intended == original
    assert w.broker.lots[lot].protection == refs
    assert w.broker.orders[refs["stop"]].price == 90
    assert not [e for e in w.broker.log if e["event"] in ("modify", "cancel")]


def test_request_owner_bridges_completion_to_a_working_order_on_another_symbol():
    w = make_world()
    defer_external(w, "outside")
    w.advance(MIN)
    w.snap()
    w.broker.execute_next()
    w.advance(MIN)
    w.snap("MYM")  # global completion, but the affected MGC order has not been read
    assert w.kernel.risk_add_blocked
    assert not w.kernel.admit_entry(entry("dj30_mym_p250", 1), w.now).ok
    w.snap()
    assert w.kernel.risk_add_blocked
    assert w.kernel.cancel("outside-order", w.now).ok
    w.advance(MIN)
    w.snap()
    assert not w.kernel.risk_add_blocked


@pytest.mark.parametrize("reboot", [False, True])
def test_completed_external_request_is_discovered_even_without_its_pending_read(reboot):
    w = make_world()
    defer_external(w, "unseen")
    w.broker.execute_next()
    w.broker.fill("unseen-order")
    w.advance(MIN)
    w.snap("MYM")
    assert w.kernel.risk_add_blocked
    if reboot:
        Sequence.start(w).restart()
    w.advance(MIN)
    w.snap()
    assert w.broker.positions["MGC"] == 99
    assert w.kernel.risk_add_blocked
    assert w.kernel.ledger.confirmed.get("vanguard_mgc", 0) == 0


def test_reordered_global_fences_cannot_drop_or_resurrect_request_owners_after_restart():
    w = make_world()
    trace = Sequence.start(w)
    trace.acquire("old-no-request", "MGC")
    defer_external(w, "reordered")
    w.advance(MIN)
    trace.acquire("pending", "MYM")
    trace.deliver("pending")
    trace.deliver("old-no-request")
    assert w.kernel.risk_add_blocked
    trace.restart()
    w.broker.inject["place"] = "reject"
    w.broker.execute_next()
    w.advance(MIN)
    w.snap()
    assert w.kernel.reconcile_restart(w.now).ok
    assert not w.kernel.risk_add_blocked
    trace.deliver("pending")
    w.advance(MIN)
    w.snap()  # retained global outcome must not create the resolved request again
    assert not w.kernel.risk_add_blocked
