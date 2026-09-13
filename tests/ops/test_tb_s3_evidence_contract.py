"""Producer characterization with literal broker facts and no listener imports."""
from datetime import datetime, timedelta

import pytest

from tests.ops.tb_s3_kernel.broker import CapabilityError, Clock, FakeBroker


def broker():
    """External causal clock survives any consumer restart."""
    return FakeBroker(Clock(datetime(2026, 9, 14, 9, 45)))


def place(route, ref="entry", side="buy", qty=2, sym="MGC"):
    """Named external event, with no listener-generated expectations."""
    return route.place(sym=sym, leg_id="vanguard_mgc", kind="entry", side=side,
                       qty=qty, order_type="market", ref=ref, bracket={"stop": 90})


def test_acquisition_is_causal_and_queued_facts_do_not_change():
    route = broker()
    place(route)
    old = route.snapshot("MGC")
    route.fill("entry", qty=1)
    route.clock.advance(timedelta(minutes=1))
    new = route.snapshot("MGC")
    assert old.position == 0 and old.fills == {} and old.lots == {}
    assert old.working[0]["remaining"] == 2
    assert new.position == 1 and new.fills == {"entry": 1}
    assert old.acquired < new.executions[0].execution_id < new.acquired
    assert old.as_of < new.as_of


def test_pending_fence_and_terminal_history_are_global_and_stable():
    route = broker()
    route.inject["place"] = "defer"
    route.request("place", "external", sym="MGC", leg_id="vanguard_mgc",
                  kind="entry", side="buy", qty=1, order_type="market", ref="outside")
    pending = route.snapshot("MYM")
    assert pending.request_fence and pending.pending_requests == {"external"}
    assert pending.working == () and pending.position == 0
    route.execute_next()
    complete = route.snapshot("MYM")
    assert complete.pending_requests == frozenset()
    assert complete.request_outcomes == {"external": "accepted"}
    assert complete.order_symbols == {"outside": "MGC"}
    route.fill("outside")
    full = route.snapshot("MGC")
    assert full.order_status["outside"] == "filled"
    assert full.order_facts["outside"]["qty"] == 1
    assert full.executions[0].qty == 1
    assert pending.pending_requests == {"external"}
    assert route.snapshot("MYM").request_outcomes == {"external": "accepted"}


def test_execution_identity_survives_mutable_order_edits():
    route = broker()
    place(route)
    route.fill("entry", qty=1)
    first = route.snapshot("MGC").executions[0]
    route.orders["entry"].side = "sell"
    route.fill("entry", qty=1)
    evidence = route.snapshot("MGC")
    assert evidence.executions[0] == first
    assert [e.side for e in evidence.executions] == ["buy", "sell"]
    assert len({e.fill_id for e in evidence.executions}) == 2
    assert evidence.position == 0
    assert sorted(evidence.lots.values()) == [1, 1]


@pytest.mark.parametrize("qty", [1, 2])
def test_native_reduction_conserves_quantity_and_linked_protection(qty):
    route = broker()
    place(route)
    lot = route.fill("entry")
    result = route.close(sym="MGC", fill_id=lot, qty=qty)
    assert result.status == "accepted"
    evidence = route.snapshot("MGC")
    assert evidence.position == 2 - qty
    assert evidence.lots[lot] == 2 - qty
    assert [w["qty"] for w in evidence.working] == ([1] if qty == 1 else [])


def test_rejected_request_has_no_execution_or_working_order():
    route = broker()
    route.inject["place"] = "reject"
    result = route.request("place", "denied", sym="MGC", leg_id="vanguard_mgc",
                           kind="entry", side="buy", qty=1, order_type="market")
    evidence = route.snapshot("MGC")
    assert result.status == "rejected"
    assert evidence.request_outcomes == {"denied": "rejected"}
    assert evidence.position == 0 and evidence.working == () and evidence.executions == ()


@pytest.mark.parametrize("qty", [0, -1, 1.5, True])
def test_invalid_fill_cannot_change_broker_truth(qty):
    route = broker()
    place(route)
    with pytest.raises(CapabilityError):
        route.fill("entry", qty=qty)
    evidence = route.snapshot("MGC")
    assert evidence.position == 0 and evidence.executions == ()
    assert evidence.working[0]["remaining"] == 2


def test_close_rejects_foreign_or_unknown_lot_without_mutation():
    route = broker()
    place(route)
    lot = route.fill("entry")
    assert route.close(sym="MYM", fill_id=lot).status == "rejected"
    assert route.close(sym="MGC", fill_id="absent").status == "rejected"
    assert route.snapshot("MGC").position == 2


def test_trigger_consumes_owner_but_allocates_fifo_and_retains_sibling_anchor():
    route = broker()
    bracket = {"stop": 90, "trail_activation_ticks": 2, "trail_offset_ticks": 1}
    for ref, kind in [("base", "entry"), ("add", "add")]:
        route.place(sym="MGC", leg_id="vanguard_mgc", kind=kind, side="buy",
                    qty=2, ref=ref, bracket=bracket)
        route.fill(ref)
    route.move_price("MGC", 105)
    before = route.snapshot("MGC")
    add_trail = route.lots["add#lot"].protection["trail"]
    base_trail = route.lots["base#lot"].protection["trail"]
    route.trigger(add_trail)
    after = route.snapshot("MGC")
    assert after.position == 2
    assert after.lots == {"base#lot": 0, "add#lot": 2}
    assert after.protection_owners["base#lot"]["qty"] == 2
    assert after.protection_owners["add#lot"]["consumed"] is True
    assert after.order_facts[base_trail]["trail_anchor"] == 105
    assert after.order_status[base_trail] == "working"
    assert len(after.reductions) == 1
    reduction = after.reductions[0]
    assert (reduction.transition, reduction.order_ref, reduction.protection_owner) == (
        "triggered_protection", add_trail, "add#lot")
    assert reduction.allocations == (("base#lot", 2),)
    assert before.acquired < reduction.execution_id < after.acquired
    assert before.lots == {"base#lot": 2, "add#lot": 2}
    assert route.attach("add#lot", bracket).status == "rejected"
    # Reissue to a surviving owner is legal even after its original lot is gone.
    assert route.modify(base_trail, trail_offset=2).status == "accepted"
    route.trigger(base_trail)
    final = route.snapshot("MGC")
    assert final.position == 0 and final.working == ()
    assert final.reductions[-1].allocations == (("add#lot", 2),)
    assert final.reductions[0] == reduction


def test_explicit_scope_is_not_a_triggered_fifo_exit():
    route = broker()
    place(route, ref="base")
    route.fill("base")
    place(route, ref="add")
    route.fill("add")
    assert route.close(sym="MGC", fill_id="add#lot", qty=1).status == "accepted"
    evidence = route.snapshot("MGC")
    assert evidence.lots == {"base#lot": 2, "add#lot": 1}
    assert evidence.reductions[-1].transition == "explicit_scope"
    assert evidence.reductions[-1].allocations == (("add#lot", 1),)
    assert evidence.lot_facts["add#lot"]["side"] == "buy"


def test_request_identity_cannot_erase_pending_or_completed_history():
    route = broker()
    payload = dict(sym="MGC", leg_id="vanguard_mgc", kind="entry", side="buy", qty=1)
    route.inject["place"] = "defer"
    route.request("place", "unique", **payload)
    assert route.request("place", "unique", **payload).status == "rejected"
    assert len(route.queued_requests) == 1 and route.orders == {}
    route.execute_next()
    assert route.request("place", "unique", **payload).status == "rejected"
    assert len(route.orders) == 1
    assert route.snapshot("MGC").request_outcomes == {"unique": "accepted"}


def test_duplicate_attach_cannot_orphan_executable_protection():
    route = broker()
    place(route)
    lot = route.fill("entry")
    assert route.attach(lot, {"stop": 91}).status == "rejected"
    assert route.close(sym="MGC").status == "accepted"
    assert route.snapshot("MGC").working == ()


def test_generated_refs_do_not_overwrite_explicit_or_terminal_orders():
    route = broker()
    place(route, ref="stop-1")
    route.fill("stop-1")
    assert place(route, ref="stop-1").status == "rejected"
    evidence = route.snapshot("MGC")
    assert evidence.order_status["stop-1"] == "filled"
    assert evidence.fills == {"stop-1": 2}
    assert evidence.working[0]["ref"] != "stop-1"


def test_incomplete_bracket_is_rejected_atomically_even_when_deferred():
    route = broker()
    route.place(sym="MGC", leg_id="vanguard_mgc", kind="entry", side="buy", qty=2,
                ref="bare")
    route.fill("bare")
    route.inject["attach"] = "defer"
    route.request("attach", "bad-bracket", fill_id="bare#lot",
                  bracket={"stop": 90, "trail_activation_ticks": 2})
    assert route.execute_next().status == "rejected"
    evidence = route.snapshot("MGC")
    assert evidence.working == ()
    assert evidence.pending_requests == frozenset()
    assert evidence.request_outcomes == {"bad-bracket": "rejected"}


def test_close_requires_atomic_residual_protection_capability():
    route = broker()
    place(route)
    route.fill("entry")
    route.caps["e"] = "not supported"
    assert route.close(sym="MGC", qty=1).status == "rejected"
    assert route.snapshot("MGC").position == 2


def test_fresh_fill_after_consumption_has_new_owner_and_keeps_old_history():
    route = broker()
    place(route)
    first_lot = route.fill("entry", qty=1)
    route.trigger(route.lots[first_lot].protection["stop"])
    second_lot = route.fill("entry", qty=1)
    assert first_lot != second_lot
    evidence = route.snapshot("MGC")
    assert evidence.protection_owners[first_lot]["consumed"] is True
    assert evidence.protection_owners[second_lot]["consumed"] is False
    assert evidence.lots[first_lot] == 0 and evidence.lots[second_lot] == 1


def test_trailing_activation_uses_explicit_symbol_tick_geometry():
    route = broker()
    route.tick_sizes = {"MGC": 0.1}
    route.place(sym="MGC", leg_id="vanguard_mgc", kind="entry", side="buy", qty=1,
                ref="trail-entry", bracket={"trail_activation_ticks": 2, "trail_offset_ticks": 1})
    lot = route.fill("trail-entry")
    route.move_price("MGC", 100.1)
    assert route.snapshot("MGC").working[0]["trail_active"] is False
    route.move_price("MGC", 100.2)
    assert route.snapshot("MGC").working[0]["trail_active"] is True
    assert route.lots[lot].qty == 1


def test_interleaved_partial_fills_exit_in_execution_order():
    route = broker()
    place(route, ref="a")
    route.fill("a", qty=1)
    place(route, ref="b", qty=1)
    route.fill("b")
    route.fill("a", qty=1)
    place(route, ref="c")
    route.fill("c")
    route.trigger(route.lots["c#lot"].protection["stop"])
    evidence = route.snapshot("MGC")
    assert evidence.lots == {"a#lot": 1, "b#lot": 0, "c#lot": 2}
    assert evidence.reductions[-1].allocations == (("a#lot", 1), ("b#lot", 1))
    assert evidence.reductions[-1].execution_allocations == ((1, 1), (2, 1))


@pytest.mark.parametrize("bracket", [None, {}, {"stop": None}])
def test_empty_attach_resolves_as_rejection_without_losing_request(bracket):
    route = broker()
    route.place(sym="MGC", leg_id="vanguard_mgc", kind="entry", side="buy", qty=1,
                ref="bare")
    route.fill("bare")
    route.inject["attach"] = "defer"
    route.request("attach", "empty", fill_id="bare#lot", bracket=bracket)
    assert route.execute_next().status == "rejected"
    assert route.snapshot("MGC").request_outcomes == {"empty": "rejected"}


@pytest.mark.parametrize("changes", [{"qty": -1}, {"side": "buy"},
                                     {"trail_offset": None}, {"price": float("nan")}])
def test_native_modify_rejects_invalid_candidate_atomically(changes):
    route = broker()
    place(route)
    lot = route.fill("entry")
    stop = route.lots[lot].protection["stop"]
    assert route.modify(stop, **changes).status == "rejected"
    evidence = route.snapshot("MGC")
    assert evidence.working[0]["qty"] == 2 and evidence.working[0]["price"] == 90
    assert evidence.order_symbols[stop] == "MGC"


def test_invalid_request_signature_is_rejected_before_acceptance():
    route = broker()
    route.inject["close"] = "defer"
    route.request("close", "bad-payload", sym="MGC", unexpected=True)
    # Signature errors are rejected before acceptance, with no pending request.
    assert route.snapshot("MGC").pending_requests == frozenset()


def test_unexpected_execution_failure_keeps_accepted_request_pending():
    route = broker()
    place(route)
    route.fill("entry")
    route.inject["close"] = "defer"
    route.request("close", "close-1", sym="MGC")
    # Deliberate contradictory broker history must not produce a covering fence.
    route.executions.clear()
    with pytest.raises(CapabilityError):
        route.execute_next()
    evidence = route.snapshot("MGC")
    assert evidence.pending_requests == {"close-1"}
    assert "close-1" not in evidence.request_outcomes
    assert evidence.position == 2


def test_two_requests_keep_distinct_global_fences_across_delayed_delivery():
    route = broker()
    for request_id, ref, sym in [("r1", "a", "MGC"), ("r2", "b", "MYM")]:
        route.inject["place"] = "defer"
        route.request("place", request_id, sym=sym, ref=ref, leg_id="external",
                      kind="entry", side="buy", qty=1)
    old = route.snapshot("MNQ")
    route.execute_next()
    middle = route.snapshot("MNQ")
    route.fill("a")
    route.execute_next()
    newest = route.snapshot("MNQ")
    # A restarted consumer can receive these in any order; the external domain persists.
    delivered = [newest, old, middle]
    assert [e.pending_requests for e in delivered] == [frozenset(), {"r1", "r2"}, {"r2"}]
    assert middle.request_outcomes == {"r1": "accepted"}
    assert newest.order_symbols == {"a": "MGC", "b": "MYM"}
    assert old.acquired < middle.acquired < newest.acquired
    assert newest.request_outcomes == {"r1": "accepted", "r2": "accepted"}


@pytest.mark.parametrize("fault,position", [("unknown_executed", 0), ("unknown_lost", 0)])
def test_unknown_place_preserves_actual_working_facts(fault, position):
    route = broker()
    route.inject["place"] = fault
    result = route.request("place", "uncertain", sym="MGC", leg_id="external",
                           kind="entry", side="buy", qty=1, ref="order")
    evidence = route.snapshot("MGC")
    assert result.status == "unknown" and evidence.position == position
    assert evidence.request_outcomes == {"uncertain": "unknown"}
    assert evidence.working_refs() == ({"order"} if fault == "unknown_executed" else set())


def test_scoped_reduction_after_fifo_divergence_refuses_then_full_close_removes_all():
    route = broker()
    for ref in ("base", "add"):
        place(route, ref=ref)
        route.fill(ref)
    route.trigger(route.lots["add#lot"].protection["stop"])
    assert route.close(sym="MGC", fill_id="add#lot", qty=1).status == "rejected"
    assert route.snapshot("MGC").position == 2
    assert route.close(sym="MGC").status == "accepted"
    final = route.snapshot("MGC")
    assert final.position == 0 and final.working == ()
    assert final.reductions[-1].allocations == (("add#lot", 2),)
    assert all(o["consumed"] for o in final.protection_owners.values())


def test_captured_nested_facts_do_not_alias_broker_or_future_captures():
    route = broker()
    place(route)
    route.fill("entry")
    old = route.snapshot("MGC")
    old.working[0]["qty"] = 999
    old.lot_facts["entry#lot"]["side"] = "sell"
    old.protection_owners["entry#lot"]["orders"].clear()
    new = route.snapshot("MGC")
    assert new.working[0]["qty"] == 2
    assert new.lot_facts["entry#lot"]["side"] == "buy"
    assert len(new.protection_owners["entry#lot"]["orders"]) == 1


def test_adding_component_preserves_surviving_owner_quantity_after_fifo():
    route = broker()
    place(route, ref="base", qty=3)
    route.fill("base")
    place(route, ref="add", qty=2)
    route.fill("add")
    route.trigger(route.lots["add#lot"].protection["stop"])
    assert route.attach("base#lot", {"limit": 110}).status == "accepted"
    evidence = route.snapshot("MGC")
    assert evidence.protection_owners["base#lot"]["qty"] == 3
    assert [w["qty"] for w in evidence.working] == [3, 3]
    assert route.close(sym="MGC", fill_id="base#lot", qty=1).status == "rejected"
    assert route.snapshot("MGC").position == 3


def test_stop_price_cannot_be_absent_at_place_or_modify():
    route = broker()
    result = route.place(sym="MGC", leg_id="vanguard_mgc", kind="entry", side="buy",
                         qty=1, order_type="stop")
    assert result.status == "rejected"
    place(route)
    lot = route.fill("entry")
    stop = route.lots[lot].protection["stop"]
    assert route.modify(stop, price=None).status == "rejected"
    assert route.snapshot("MGC").working[0]["price"] == 90
