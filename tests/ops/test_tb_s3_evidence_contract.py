"""Producer characterization with literal broker facts and no listener imports."""
from datetime import datetime, timedelta

import pytest

from tests.ops.tb_s3_kernel.broker import Clock, FakeBroker


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
