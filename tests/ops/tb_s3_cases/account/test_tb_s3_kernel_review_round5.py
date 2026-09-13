"""PR 365 at e46a4fa: admission ownership and complete protection commands."""


from dataclasses import replace


import pytest


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.broker import BrokerOrder, NOT_SUPPORTED, UNRECORDED


from tests.ops.tb_s3_kernel.account_harness import MIN, Sequence, entry, fill_lot, make_world


from tests.ops.tb_s3_cases.support.test_tb_s3_kernel_redesign import Crash, crash_once


from tests.ops.tb_s3_cases.support.test_tb_s3_kernel_review_round4 import CutStore


@pytest.mark.parametrize("leg", ["vanguard_mgc", "dj30_mym_p250"])
@pytest.mark.parametrize("first_removed", ["outside-mgc", "outside-mnq"])
def test_unowned_executable_orders_block_new_entries_across_the_account(leg, first_removed):
    w = make_world()
    w.broker.orders["outside-mgc"] = BrokerOrder("outside-mgc", "MGC", "vanguard_mgc",
                                                "entry", "buy", 99, "stop", price=110)
    w.broker.orders["outside-mnq"] = BrokerOrder("outside-mnq", "MNQ", "orb_mnq_v7",
                                                "unrecognized", "buy", 7, "stop", price=110)
    w.advance(MIN)
    w.snap()
    assert not w.kernel.admit_entry(entry(leg, 1), w.now).ok
    assert w.kernel.risk_add_blocked
    assert len(w.kernel.blocks["unknown_order"]) == 2
    w.broker.cancel(first_removed)  # outside actor removes only one independent owner
    w.advance(MIN)
    w.snap()
    assert w.kernel.risk_add_blocked
    assert len(w.kernel.blocks["unknown_order"]) == 1
    w.kernel.session_open()
    assert w.kernel.risk_add_blocked
    w.broker.cancel("outside-mnq" if first_removed == "outside-mgc" else "outside-mgc")
    w.advance(MIN)
    w.snap()
    assert not w.kernel.risk_add_blocked
    assert w.kernel.admit_entry(entry(leg, 1), w.now).ok


@pytest.mark.parametrize("via_daemon", [False, True])
def test_amendment_defers_when_a_position_read_supersedes_its_working_read(via_daemon):
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    ref = w.broker.lots[lot].protection["stop"]
    w.broker.orders[ref].price = 100
    w.advance(MIN)
    w.kernel.apply_evidence(replace(w.broker.snapshot("MGC"), order_level=False))
    w.kernel.block("overlay", "test")
    if via_daemon:
        result = w.daemon.reissue("vanguard_mgc", lot, {"stop": 95}, 110, w.now)
    else:
        result = w.kernel.amend(lot, Bracket(stop=95), w.now).reason
    assert result == "amend_deferred"
    assert w.kernel.amend_action(lot, Bracket(stop=95), w.now) is None
    assert w.broker.orders[ref].price == 100
    assert not [e for e in w.broker.log if e["event"] == "modify"]
