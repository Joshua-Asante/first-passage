"""PR 365 at e46a4fa: admission ownership and complete protection commands."""


from dataclasses import replace


import pytest


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.broker import BrokerOrder, NOT_SUPPORTED, UNRECORDED


from tests.ops.tb_s3_kernel.harness import MIN, Sequence, entry, fill_lot, make_world


from tests.ops.tb_s3_cases.support.test_tb_s3_kernel_redesign import Crash, crash_once


from tests.ops.tb_s3_cases.support.test_tb_s3_kernel_review_round4 import CutStore


@pytest.mark.parametrize("position_only", [False, True])
def test_unallocated_broker_exposure_blocks_other_leg_admission(position_only):
    w = make_world()
    w.broker.orders["outside"] = BrokerOrder("outside", "MGC", "vanguard_mgc", "entry",
                                           "buy", 99, "market")
    w.broker.fill("outside")
    w.advance(MIN)
    w.kernel.apply_evidence(replace(w.broker.snapshot("MGC"), order_level=not position_only))
    assert not w.kernel.admit_entry(entry("dj30_mym_p250", 1), w.now).ok
    w.kernel.close("sym", "MGC", w.now, "attended_external_recovery")
    w.advance(MIN)
    w.snap()
    assert not w.kernel.risk_add_blocked


def test_unknown_order_kind_cannot_use_the_protective_orphan_cancel_path():
    w = make_world()
    w.broker.orders["unclassified"] = BrokerOrder("unclassified", "MGC", "vanguard_mgc",
                                                "unrecognized", "buy", 1, "stop", price=110)
    w.advance(MIN)
    w.snap()
    assert not w.kernel.cancel("unclassified", w.now).ok
    assert w.broker.orders["unclassified"].status == "working"
    assert w.kernel.risk_add_blocked
    assert not [e for e in w.broker.log if e["event"] == "cancel"]


@pytest.mark.parametrize("kind", ["entry", "add"])
@pytest.mark.parametrize("allocated", [False, True])
def test_known_external_entry_cancel_preserves_existing_allocated_exposure(kind, allocated):
    w = make_world()
    if allocated:
        lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
        protection = w.broker.lots[lot].protection["stop"]
    w.broker.orders["outside"] = BrokerOrder("outside", "MGC", "vanguard_mgc", kind,
                                           "buy", 1, "stop", price=110)
    w.advance(MIN)
    w.snap()
    assert w.kernel.cancel("outside", w.now).ok
    w.advance(MIN)
    w.snap()
    assert not w.kernel.risk_add_blocked
    assert w.broker.positions.get("MGC", 0) == (2 if allocated else 0)
    if allocated:
        assert w.broker.orders[protection].status == "working"
    assert not [e for e in w.broker.log if e["event"] == "close"]


@pytest.mark.parametrize("reboot", [False, True])
def test_external_entry_fill_racing_cancel_retains_its_unallocated_exposure_owner(reboot):
    w = make_world()
    fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    w.broker.orders["outside"] = BrokerOrder("outside", "MGC", "vanguard_mgc", "entry",
                                           "buy", 1, "stop", price=110)
    w.advance(MIN)
    w.snap()
    w.broker.inject["cancel"] = "defer"
    assert w.kernel.cancel("outside", w.now).ok
    if reboot:
        Sequence.start(w).restart()
    w.broker.fill("outside")
    w.broker.execute_next()
    w.advance(MIN)
    w.snap()
    assert w.kernel.risk_add_blocked
    assert not w.kernel.admit_entry(entry("dj30_mym_p250", 1), w.now).ok
    assert w.kernel.ledger.confirmed["vanguard_mgc"] == 2
    assert w.broker.positions["MGC"] == 3
    assert not [e for e in w.broker.log if e["event"] == "close"]


@pytest.mark.parametrize("outcome,stop", [("unknown", 95), ("unknown_lost", 90)])
def test_unknown_component_reconciles_before_its_durable_sibling_resumes(outcome, stop):
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90, limit=120))
    refs = dict(w.broker.lots[lot].protection)
    stale = w.broker.snapshot("MGC")
    w.broker.inject["modify"] = outcome
    w.kernel.amend(lot, Bracket(stop=95, limit=125), w.now)
    w.kernel.apply_evidence(stale)
    assert w.broker.orders[refs["limit"]].price == 120
    assert w.kernel.risk_add_blocked
    w.advance(MIN)
    w.snap()
    assert w.broker.orders[refs["stop"]].price == stop
    assert w.broker.orders[refs["limit"]].price == 125
    w.advance(MIN)
    w.snap()
    assert not w.kernel.risk_add_blocked


@pytest.mark.parametrize("boundary", ["planned", "dispatching", "executed", "recorded"])
def test_multi_component_amendment_keeps_every_effect_across_a_dispatch_crash(boundary):
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90, limit=120))
    refs = dict(w.broker.lots[lot].protection)
    crash_once(w.kernel, "modify", boundary)
    with pytest.raises(Crash):
        w.kernel.amend(lot, Bracket(stop=95, limit=125), w.now)
    Sequence.start(w).restart()
    w.kernel.progress(w.now)
    if boundary in ("dispatching", "executed"):
        assert w.broker.orders[refs["limit"]].price == 120  # unknown sibling must reconcile first
    w.advance(MIN)
    w.snap()
    w.advance(MIN)
    w.snap()
    assert w.broker.orders[refs["limit"]].price == 125
    assert w.broker.orders[refs["stop"]].price == (90 if boundary == "dispatching" else 95)
    assert w.broker.positions["MGC"] == 2
    assert "protection_gap" not in w.kernel.blocks
    if boundary == "dispatching":
        # The first attempt is proven not applied; only that component needs reissue.
        assert w.kernel.amend(lot, Bracket(stop=95, limit=125), w.now).ok
        w.advance(MIN)
        w.snap()
    assert not w.kernel.risk_add_blocked or w.kernel.reconcile_restart(w.now).ok
    assert w.kernel.expected[lot].intended == {"stop": {"price": 95}, "limit": {"price": 125}}


def test_multi_component_amendment_first_write_contains_all_work():
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90, limit=120))
    refs = dict(w.broker.lots[lot].protection)
    w.kernel.store = CutStore(w.kernel.store.data, 1)
    with pytest.raises(Crash):
        w.kernel.amend(lot, Bracket(stop=95, limit=125), w.now)
    Sequence.start(w).restart()
    w.kernel.progress(w.now)
    w.advance(MIN)
    w.snap()
    assert w.broker.orders[refs["stop"]].price == 95
    assert w.broker.orders[refs["limit"]].price == 125
    assert w.kernel.reconcile_restart(w.now).ok


@pytest.mark.parametrize("capability", [NOT_SUPPORTED, UNRECORDED])
@pytest.mark.parametrize("with_stop", [False, True])
def test_first_trail_attachment_requires_its_route_capability_before_definition(capability, with_stop):
    w = make_world(caps={"g": capability})
    lot = fill_lot(w, "dj30_mym_p250", 1)
    bracket = Bracket(stop=90 if with_stop else None,
                      trail_activation_ticks=40, trail_offset_ticks=20)
    assert w.kernel.amend(lot, bracket, w.now).reason == "l2_refused"
    assert w.kernel.expected[lot].is_bare
    assert not [e for e in w.broker.log if e["event"] == "attach"]
    w.advance(MIN)
    w.snap()
    assert w.broker.positions["MYM"] == 1
    assert "protection_gap" not in w.kernel.blocks
