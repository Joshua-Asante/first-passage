"""TB-S3 kernel model — the spec's §2d acceptance cases AC-1..AC-10, executable.

Spec: docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md (rev 5.4). Each test names the
case it encodes; the acceptance question is the spec's: can the complete behavior execute and
reach a confirmed outcome under the stated failure case?
"""


from __future__ import annotations


from datetime import datetime


import pytest


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.broker import NOT_SUPPORTED, STALENESS_WINDOW


from tests.ops.tb_s3_kernel.harness import BAR, MIN, entry, fill_lot, make_world


from tests.ops.tb_s3_kernel.kernel import Kernel, KernelRefusal


_fill_entry = fill_lot


def test_ac1_striker_bare_entry_then_attach_on_first_amend():
    """Ac1 striker bare entry then attach on first amend."""
    world = make_world()
    lot = _fill_entry(world, "dj30_mym_p250", 22)
    assert world.kernel.expected[lot].is_bare
    assert "protection_gap" not in world.kernel.blocks           # bare is qualified, not a gap
    world.advance(BAR)
    decision = world.kernel.amend(lot, Bracket(stop=41_200.0), world.now)
    assert decision.ok and decision.op.kind == "ATTACH"
    world.advance(MIN)
    world.snap("MYM")
    exp = world.kernel.expected[lot]
    assert exp.status["stop"] == "working" and decision.op.status == "complete"
    stop_ref = exp.working["stop"]
    assert world.broker.orders[stop_ref].attached_to == lot        # linked to the position


def test_ac3_orb_stop_entry_trailing_bracket_and_resting_add_cancel():
    """Ac3 orb stop entry trailing bracket and resting add cancel."""
    world = make_world()
    bracket = Bracket(stop=18_450.0, trail_activation_ticks=40, trail_offset_ticks=20)
    decision = world.kernel.admit_entry(
        entry("orb_mnq_v7", 1, bracket, order_type="stop", price=18_500.0), world.now)
    assert decision.ok
    world.broker.trigger(decision.ref)                               # fills intrabar when crossed
    world.advance(MIN)
    world.snap("MNQ")
    lot = world.broker.lot_id(decision.ref)
    kinds = {w["kind"] for w in world.kernel.w_ev["MNQ"][0] if w["attached_to"] == lot}
    assert kinds == {"stop", "trail"}
    add = world.kernel.admit_entry(
        entry("orb_mnq_v7", 1, bracket, kind="add", order_type="stop", price=18_520.0), world.now)
    assert add.ok
    world.advance(MIN)
    world.snap("MNQ")
    assert world.kernel.ledger.reserved["orb_mnq_v7"] == 1          # resting add holds its slot
    # set_mode(PROTECTED) at the session open: the port cancels its resting add (S4).
    cancel = world.kernel.cancel(add.ref, world.now)
    assert cancel.ok
    world.advance(MIN)
    world.snap("MNQ")
    assert world.kernel.pending[add.ref].status == "cancelled"
    assert world.kernel.ledger.reserved["orb_mnq_v7"] == 0          # released by the ack


def test_ac4_partial_fill_adjusts_protection_and_confirmed_base():
    """Ac4 partial fill adjusts protection and confirmed base."""
    world = make_world()
    _fill_entry(world, "vanguard_mgc", 1, Bracket(stop=2_400.0))
    add = world.kernel.admit_entry(entry("vanguard_mgc", 2, Bracket(stop=2_400.0), kind="add"),
                                   world.now)
    assert add.ok
    world.broker.fill(add.ref, qty=1)
    world.advance(MIN)
    world.snap("MGC")
    order = world.kernel.pending[add.ref]
    assert order.status == "partial" and order.filled_qty == 1 and order.reserved == 1
    assert world.kernel.ledger.confirmed["vanguard_mgc"] == 2
    lot = world.broker.lot_id(add.ref)
    stops = [w for w in world.kernel.w_ev["MGC"][0] if w["attached_to"] == lot]
    assert stops and stops[0]["qty"] == 1                           # residual quantity protected
    op = world.kernel.handle_exit("vanguard_mgc", world.now, fill_id=lot, qty=1)
    world.advance(MIN)
    world.snap("MGC")
    assert op.status == "complete" and world.kernel.lots[lot].qty == 0


def test_ac5_unknown_entry_outcome_blocks_account_wide_until_order_level_evidence():
    """Ac5 unknown entry outcome blocks account wide until order level evidence."""
    world = make_world()
    world.broker.inject["place"] = "unknown_executed"
    decision = world.kernel.admit_entry(entry("aegis_6j", 8), world.now)
    assert decision.reason == "unknown"
    assert "unknown_order" in world.kernel.blocks
    assert world.kernel.ledger.reserved["aegis_6j"] == 8
    other = world.kernel.admit_entry(entry("vanguard_mgc", 1), world.now)
    assert other.reason == "policy_block"                            # every leg refused
    world.advance(BAR)
    world.snap("6J")                                                 # order is working, unfilled
    order = world.kernel.pending[decision.ref]
    assert order.status == "accepted" and order.reserved == 8       # reservation never released
    world.broker.fill(decision.ref)
    world.advance(MIN)
    world.snap("6J")
    assert order.status == "filled" and world.kernel.ledger.confirmed["aegis_6j"] == 8
    assert "unknown_order" not in world.kernel.blocks


def test_ac5_unknown_entry_never_placed_resolves_on_absence_plus_consistent_position():
    """Ac5 unknown entry never placed resolves on absence plus consistent position."""
    world = make_world()
    world.broker.inject["place"] = "unknown_lost"
    decision = world.kernel.admit_entry(entry("aegis_6j", 8), world.now)
    assert world.kernel.pending[decision.ref].status == "unknown"
    world.snap("6J", at=world.now)                                   # same instant: not postdating
    assert world.kernel.pending[decision.ref].status == "unknown"
    world.advance(MIN)
    world.snap("6J")                                                 # absent from W, P consistent
    assert world.kernel.pending[decision.ref].status == "rejected"
    assert world.kernel.ledger.reserved.get("aegis_6j", 0) == 0
    assert "unknown_order" not in world.kernel.blocks


def test_ac9_amend_deferred_while_w_unknown_then_admitted_on_fresh_evidence():
    """Ac9 amend deferred while w unknown then admitted on fresh evidence."""
    world = make_world()
    lot = _fill_entry(world, "dj30_mym_p250", 22)
    world.advance(BAR)
    world.kernel.amend(lot, Bracket(stop=41_200.0), world.now)
    world.advance(MIN)
    world.snap("MYM")
    world.advance(20 * MIN)                                          # W now 20 minutes old
    deferred = world.kernel.amend(lot, Bracket(stop=41_220.0), world.now)
    assert deferred.reason == "amend_deferred"
    assert not [e for e in world.broker.log if e["event"] == "modify"]
    world.snap("MYM")
    admitted = world.kernel.amend(lot, Bracket(stop=41_220.0), world.now)
    assert admitted.ok and world.broker.log[-1]["event"] == "modify"


@pytest.mark.parametrize("item,leg_id", [("f", "dj30_mym_p250"), ("g", "orb_mnq_v7"),
                                         ("c", "vanguard_mgc"), ("d", "aegis_6j")])
def test_l2_item_not_supported_refuses_the_leg_at_admission(item, leg_id):
    """L2 item not supported refuses the leg at admission."""
    world = make_world(caps={item: NOT_SUPPORTED})
    decision = world.kernel.admit_entry(entry(leg_id, 1), world.now)
    assert decision.reason == "l2_refused"
    assert world.kernel.events("l2_refused")[-1]["detail"] == item


def test_kernel_refuses_risk_adds_under_any_block_but_admits_exits():
    """Kernel refuses risk adds under any block but admits exits."""
    world = make_world()
    lot = _fill_entry(world, "vanguard_mgc", 1, Bracket(stop=2_400.0))
    world.kernel.block("eod", "test")
    assert world.kernel.admit_entry(entry("vanguard_mgc", 1, kind="add"), world.now).reason \
        == "policy_block"
    op = world.kernel.handle_exit("vanguard_mgc", world.now, fill_id=lot)
    assert op.status == "sent"
    with pytest.raises(KernelRefusal):
        world.kernel.retry(op.op_id, world.now)                      # nothing to retry
