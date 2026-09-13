"""Rev7 acceptance traces; expected owners and quantities come from external events."""
from dataclasses import replace

import pytest

from book_protocol import Bracket
from tests.ops.tb_s3_kernel.harness import MIN, Sequence, entry, fill_lot, make_world


@pytest.mark.parametrize("reboot", [False, True])
def test_fifo_surviving_owner_can_amend_after_its_accounting_lot_is_exhausted(reboot):
    w = make_world()
    base = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    add = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=91), kind="add")
    w.broker.trigger(w.broker.lots[add].protection["stop"])
    w.advance(MIN)
    w.snap()
    if reboot:
        Sequence.start(w).restart()
        w.advance(MIN)
        w.snap()
        assert w.kernel.reconcile_restart(w.now).ok
    assert w.kernel.lots[base].qty == 0 and w.kernel.lots[add].qty == 2
    assert "protection_gap" not in w.kernel.blocks
    assert not w.kernel.amend(add, Bracket(stop=95), w.now).ok
    assert w.kernel.amend(base, Bracket(stop=95), w.now).ok
    w.advance(MIN)
    w.snap()
    assert w.kernel.expected[base].intended["stop"] == {"price": 95}
    assert w.kernel.ledger.confirmed["vanguard_mgc"] == 2


def test_multiple_new_fill_generations_in_one_capture_receive_separate_credit():
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 2, Bracket(stop=90)), w.now)
    first = w.broker.fill(d.ref, qty=1)
    w.broker.trigger(w.broker.lots[first].protection["stop"])
    second = w.broker.fill(d.ref, qty=1)
    w.advance(MIN)
    w.snap()
    assert not w.kernel.pending[d.ref].quarantined
    assert w.kernel.lots[first].qty == 0 and w.kernel.lots[second].qty == 1
    assert w.kernel.ledger.confirmed["vanguard_mgc"] == 1
    assert w.kernel.pending[d.ref].reserved == 0


@pytest.mark.parametrize("reboot", [False, True])
def test_completed_requests_transfer_to_gross_lot_owners_even_at_net_zero(reboot):
    w = make_world()
    for request_id, side in [("external-buy", "buy"), ("external-sell", "sell")]:
        w.broker.request("place", request_id, sym="MGC", leg_id="external",
                         kind="entry", side=side, qty=1, ref=request_id)
        w.broker.fill(request_id)
    if reboot:
        Sequence.start(w).restart()
    w.advance(MIN)
    w.snap()
    assert w.kernel.risk_add_blocked
    assert len([owner for reason, owner in w.kernel.obligations
                if reason == "unknown_order" and owner.startswith("unowned-lot:MGC:")]) == 2
    assert not w.kernel.admit_entry(entry("dj30_mym_p250", 1), w.now).ok


def test_later_registry_expands_covering_request_even_when_outcome_is_omitted():
    w = make_world()
    w.broker.inject["place"] = "reject"
    w.broker.request("place", "external", sym="MGC", leg_id="external",
                     kind="entry", side="buy", qty=1)
    w.advance(MIN)
    w.snap("MGC")
    old = [w.broker.snapshot(sym) for sym in ("6J", "MYM", "MNQ")]
    w.broker.place(sym="X", leg_id="external", kind="entry", side="buy", qty=1, ref="foreign")
    w.broker.fill("foreign")
    w.kernel.apply_evidence(replace(w.broker.snapshot("MGC"), request_outcomes={}))
    for ev in old:
        w.kernel.apply_evidence(ev)
    assert "X" in w.kernel.unowned_requests["external"].symbols
    assert w.kernel.unresolved_requests
    assert w.kernel.risk_add_blocked


def test_request_identity_renewal_before_coverage_is_sticky_across_restart():
    w = make_world()
    w.broker.inject["place"] = "reject"
    w.broker.request("place", "external", sym="MGC", leg_id="external",
                     kind="entry", side="buy", qty=1)
    w.advance(MIN)
    w.snap("MGC")
    w.kernel.apply_evidence(replace(w.broker.snapshot("MYM"),
                                   pending_requests=frozenset({"external"}), request_outcomes={}))
    Sequence.start(w).restart()
    w.advance(MIN)
    w.snap()
    assert w.kernel.unowned_requests["external"].status == "conflict"
    assert w.kernel.unresolved_requests and w.kernel.risk_add_blocked


def test_missing_reduction_history_cannot_release_confirmed_capacity():
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    w.broker.close(sym="MGC")
    w.advance(MIN)
    ev = w.broker.snapshot("MGC")
    w.kernel.apply_evidence(replace(ev, reductions=()))
    assert w.kernel.lots[lot].qty == 2
    assert w.kernel.ledger.confirmed["vanguard_mgc"] == 2
    assert w.kernel.risk_add_blocked
    w.advance(MIN)
    w.snap()
    assert w.kernel.lots[lot].qty == 0


def test_fabricated_consumed_owner_cannot_hide_surviving_gap():
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 1, Bracket(stop=90))
    w.broker.cancel(w.broker.lots[lot].protection["stop"])
    w.advance(MIN)
    ev = w.broker.snapshot("MGC")
    ev.protection_owners[lot] = {"qty": 0, "consumed": True, "orders": {}}
    w.kernel.apply_evidence(ev)
    assert w.kernel.risk_add_blocked
    assert lot in w.kernel.expected


def test_gap_on_surviving_owner_cannot_complete_from_original_lot_zero():
    w = make_world()
    base = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    add = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=91), kind="add")
    w.broker.trigger(w.broker.lots[add].protection["stop"])
    w.advance(MIN)
    w.snap()
    w.broker.cancel(w.broker.lots[base].protection["stop"])
    for _ in range(2):
        w.advance(MIN)
        w.snap()
    assert w.broker.positions["MGC"] == 2
    assert "protection_gap" in w.kernel.blocks and w.kernel.risk_add_blocked
    assert not w.kernel.admit_entry(entry("dj30_mym_p250", 1), w.now).ok
    w.kernel.close("sym", "MGC", w.now, "attended")
    w.advance(MIN)
    w.snap()
    assert w.broker.positions["MGC"] == 0
    assert not w.kernel.risk_add_blocked


@pytest.mark.parametrize("reboot", [False, True])
def test_late_fill_cannot_mask_already_executed_bounded_close(reboot):
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 3, Bracket(stop=90)), w.now)
    lot = w.broker.fill(d.ref, qty=2)
    w.advance(MIN)
    w.snap()
    w.broker.inject["cancel"] = "unknown_lost"
    w.broker.inject["close"] = "unknown"
    op = w.kernel.close("fill", lot, w.now, "exit", qty=1)
    w.broker.fill(d.ref, qty=1)
    if reboot:
        Sequence.start(w).restart()
    w.advance(MIN)
    w.snap()
    op = w.kernel.operations[op.op_id]
    assert op.payload["closed"] == 1
    assert op.status == "complete"
    assert w.broker.positions["MGC"] == 2
    assert len(w.broker.reductions) == 1


def test_retained_close_gets_target_gross_evidence_before_other_restart_reads():
    from tests.ops.tb_s3_cases.support.test_tb_s3_kernel_redesign import Crash, crash_once
    w = make_world()
    for ref, side in [("buy", "buy"), ("sell", "sell")]:
        w.broker.place(sym="MGC", leg_id="external", kind="entry", side=side, qty=1, ref=ref)
        w.broker.fill(ref)
    w.advance(MIN)
    w.snap("MGC")
    crash_once(w.kernel, "close", "planned")
    with pytest.raises(Crash):
        w.kernel.close("sym", "MGC", w.now, "attended", op_id="gross-close")
    Sequence.start(w).restart()
    assert not [e for e in w.broker.log if e["event"] == "close"]
    w.advance(MIN)
    w.snap("MGC")  # Must precede unrelated symbol reads that would drain retained work.
    assert len([e for e in w.broker.log if e["event"] == "close"]) == 1
    assert sum(w.broker.snapshot("MGC").lots.values()) == 0
    w.advance(MIN)
    w.snap()
    assert w.kernel.operations["gross-close"].status == "complete"


def test_reused_close_id_cannot_alias_a_different_demand():
    from tests.ops.tb_s3_kernel.kernel import KernelRefusal
    w = make_world()
    w.kernel.close("sym", "MGC", w.now, "exit", op_id="one")
    with pytest.raises(KernelRefusal):
        w.kernel.close("sym", "MYM", w.now, "exit", op_id="one")


def test_net_zero_with_gross_lots_cannot_authorize_protective_cancellation():
    w = make_world()
    for ref, side in [("buy", "buy"), ("sell", "sell")]:
        w.broker.place(sym="MGC", leg_id="external", kind="entry", side=side,
                       qty=1, ref=ref, bracket={"stop": 90})
        w.broker.fill(ref)
    w.advance(MIN)
    w.snap()
    stop = w.broker.lots["buy#lot"].protection["stop"]
    assert not w.kernel.cancel(stop, w.now).ok
    assert w.broker.orders[stop].status == "working"


def test_reduction_cannot_claim_another_attempts_scope():
    w = make_world()
    first = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    second = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=91), kind="add")
    w.broker.inject["close"] = "unknown_lost"
    op = w.kernel.close("fill", first, w.now, "exit", qty=1)
    effect = next(e for e in w.kernel.effects.values() if e.owner == op.op_id and e.kind == "close")
    w.broker.close(sym="MGC", fill_id=second, qty=1)
    w.advance(MIN)
    ev = w.broker.snapshot("MGC")
    forged = replace(ev.reductions[-1], request_id=effect.effect_id)
    w.kernel.apply_evidence(replace(ev, reductions=(forged,)))
    assert op.status != "complete" and w.kernel.risk_add_blocked
    assert w.kernel.coherent_evidence("MGC", w.now) is None


def test_bounded_symbol_close_is_explicitly_refused_without_full_flatten():
    from tests.ops.tb_s3_kernel.kernel import KernelRefusal
    w = make_world()
    fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    with pytest.raises(KernelRefusal):
        w.kernel.close("sym", "MGC", w.now, "exit", qty=1)
    with pytest.raises(KernelRefusal):
        w.kernel.handle_exit("vanguard_mgc", w.now, qty=1)
    assert w.broker.positions["MGC"] == 2


@pytest.mark.parametrize("capture_flat", [False, True])
def test_historical_owner_consumption_survives_a_later_entry(capture_flat):
    w = make_world()
    base = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    add = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=91), kind="add")
    w.broker.trigger(w.broker.lots[add].protection["stop"])
    w.broker.close(sym="MGC")
    if capture_flat:
        w.advance(MIN)
        w.snap()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 1, Bracket(stop=92)), w.now)
    assert d.ok
    current = w.broker.fill(d.ref)
    w.advance(MIN)
    w.snap()
    assert w.kernel.lots[current].qty == 1
    assert w.kernel.ledger.confirmed["vanguard_mgc"] == 1
    assert not w.kernel.risk_add_blocked
    assert base not in w.kernel.expected and add not in w.kernel.expected


def test_external_working_fact_cannot_disappear_from_full_working_list():
    w = make_world()
    w.broker.request("place", "external", sym="MGC", leg_id="external", kind="entry",
                     side="buy", qty=1, ref="outside")
    w.advance(MIN)
    w.kernel.apply_evidence(replace(w.broker.snapshot("MGC"), working=()))
    w.snap("6J", "MYM", "MNQ")
    assert w.kernel.unresolved_requests and w.kernel.risk_add_blocked
    assert not w.kernel.admit_entry(entry("dj30_mym_p250", 1), w.now).ok


def test_retained_external_order_cannot_disappear_from_all_registry_facts():
    w = make_world()
    w.broker.request("place", "external", sym="MGC", leg_id="external", kind="entry",
                     side="buy", qty=1, ref="outside")
    w.advance(MIN)
    w.snap()
    w.advance(MIN)
    ev = w.broker.snapshot("MGC")
    w.kernel.apply_evidence(replace(ev, working=(), order_facts={}, order_status={},
                                   order_symbols={}, fills={}))
    assert w.kernel.risk_add_blocked
    assert not w.kernel.admit_entry(entry("dj30_mym_p250", 1), w.now).ok


def test_missing_global_registry_cannot_be_coherent_flat_evidence():
    w = make_world()
    w.advance(MIN)
    w.kernel.apply_evidence(replace(w.broker.snapshot("MGC"), order_symbols=None))
    assert w.kernel.coherent_evidence("MGC", w.now) is None
    assert not w.kernel.admit_entry(entry("vanguard_mgc", 1), w.now).ok


def test_execution_identity_is_global_across_symbols():
    w = make_world()
    a = w.kernel.admit_entry(entry("vanguard_mgc", 1), w.now)
    b = w.kernel.admit_entry(entry("dj30_mym_p250", 1), w.now)
    w.broker.fill(a.ref)
    w.broker.fill(b.ref)
    w.advance(MIN)
    mgc = w.broker.snapshot("MGC")
    w.kernel.apply_evidence(mgc)
    mym = w.broker.snapshot("MYM")
    forged = replace(mym.executions[0], execution_id=mgc.executions[0].execution_id)
    w.kernel.apply_evidence(replace(mym, executions=(forged,)))
    assert w.kernel.ledger.confirmed.get("dj30_mym_p250", 0) == 0
    assert w.kernel.risk_add_blocked


def test_renewed_known_request_id_blocks_even_after_operation_completion():
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 1), w.now)
    w.advance(MIN)
    w.snap()
    request_id = w.kernel.pending[d.ref].place_effect
    ev = w.broker.snapshot("MYM")
    w.kernel.apply_evidence(replace(ev, pending_requests=frozenset({request_id})))
    Sequence.start(w).restart()
    w.advance(MIN)
    w.snap()
    assert w.kernel.risk_add_blocked
    assert any(owner == f"request-conflict:{request_id}" for _, owner in w.kernel.obligations)


def test_bounded_close_can_complete_with_protected_later_generation():
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 2, Bracket(stop=90)), w.now)
    first = w.broker.fill(d.ref, qty=1)
    w.advance(MIN)
    w.snap()
    w.broker.inject["cancel"] = "unknown_lost"
    op = w.kernel.close("fill", first, w.now, "exit", qty=1)
    second = w.broker.fill(d.ref, qty=1)
    w.advance(MIN)
    w.snap()
    assert first != second and w.kernel.lots[second].qty == 1
    assert op.status == "complete"
    assert not w.kernel.risk_add_blocked
    assert len(w.broker.reductions) == 1
