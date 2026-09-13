"""TB-S3 kernel model — regressions for the review findings on PR #365 (`2015eef`).

Each test reproduces one finding against the model exactly as reported, so the composition
it exposed cannot return silently.
"""


from __future__ import annotations


from dataclasses import replace


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.harness import BAR, MIN, entry, fill_lot, make_world


def _position_only(ev):
    """A read that carries the position but no order-level data (spec: aggregate P)."""
    return replace(ev, working=(), order_status={}, fills={}, lots={}, order_level=False)


def test_position_only_evidence_never_completes_a_close():
    """Position-only evidence never completes a close."""
    world = make_world()
    lot = fill_lot(world, "vanguard_mgc", 2, Bracket(stop=2_400.0))
    world.broker.inject["close"] = "reject"
    op = world.kernel.handle_exit("vanguard_mgc", world.now, fill_id=lot)
    assert op.status == "rejected" and "close_rejected" in world.kernel.blocks
    world.advance(MIN)
    world.kernel.apply_evidence(_position_only(world.broker.snapshot("MGC")))
    assert op.status == "rejected"
    assert world.kernel.lots[lot].qty == 2
    assert "close_rejected" in world.kernel.blocks
    assert world.kernel.events("close_complete") == []


def test_accepted_entry_without_evidence_for_one_bar_becomes_unknown_and_blocks():
    """Accepted entry without evidence for one bar becomes unknown and blocks."""
    world = make_world()
    decision = world.kernel.admit_entry(entry("aegis_6j", 8), world.now)
    assert decision.ok and world.kernel.pending[decision.ref].status == "accepted"
    world.advance(2 * BAR)
    world.snap("MGC")                                                # another symbol only
    other = world.kernel.admit_entry(entry("vanguard_mgc", 1), world.now)
    assert other.reason == "policy_block"
    order = world.kernel.pending[decision.ref]
    assert order.status == "unknown" and "unknown_order" in world.kernel.blocks
    assert world.kernel.ledger.reserved["aegis_6j"] == 8              # still held
    world.snap("6J")                                                 # working: resolved
    assert order.status == "accepted" and "unknown_order" not in world.kernel.blocks


def test_resting_order_evidenced_every_bar_never_times_out():
    """Resting order evidenced every bar never times out."""
    world = make_world()
    decision = world.kernel.admit_entry(
        entry("orb_mnq_v7", 1, Bracket(stop=18_450.0), order_type="stop", price=18_500.0),
        world.now)
    for _ in range(4):
        world.advance(BAR - MIN)
        world.snap("MNQ")
    assert world.kernel.pending[decision.ref].status == "accepted"
    assert "unknown_order" not in world.kernel.blocks


def test_amend_completes_only_when_evidence_shows_the_requested_level():
    """Amend completes only when evidence shows the requested level."""
    world = make_world()
    lot = fill_lot(world, "vanguard_mgc", 1, Bracket(stop=2_400.0))
    world.advance(MIN)
    world.snap("MGC")
    decision = world.kernel.amend(lot, Bracket(stop=2_410.0), world.now)
    assert decision.ok and decision.op.status == "sent"              # accepted ≠ complete
    assert world.kernel.expected[lot].intended["stop"]["price"] == 2_400.0
    stop_ref = world.kernel.expected[lot].working["stop"]
    world.broker.orders[stop_ref].price = 2_400.0                     # the level did not move
    world.advance(MIN)
    world.snap("MGC")
    assert decision.op.status == "sent"
    world.broker.orders[stop_ref].price = 2_410.0
    world.advance(MIN)
    world.snap("MGC")
    assert decision.op.status == "complete"
    assert world.kernel.expected[lot].intended["stop"]["price"] == 2_410.0


def test_partial_close_is_resubmitted_for_the_remainder_after_reconciliation():
    """Partial close is resubmitted for the remainder after reconciliation."""
    world = make_world()
    lot = fill_lot(world, "dj30_mym_p250", 22)
    world.broker.inject["close"] = ("partial", 10)
    op = world.kernel.handle_exit("dj30_mym_p250", world.now, fill_id=lot)
    world.advance(MIN)
    world.snap("MYM")
    assert op.status == "partial" and world.kernel.lots[lot].qty == 12
    assert "unknown_order" in world.kernel.blocks                     # still unresolved
    again = world.kernel.handle_exit("dj30_mym_p250", world.now, fill_id=lot)
    assert again is op                                                # same durable operation
    world.kernel.retry(op.op_id, world.now)
    assert op.status == "sent" and op.attempts == 2
    world.advance(MIN)
    world.snap("MYM")
    assert op.status == "complete" and world.kernel.lots[lot].qty == 0
    assert "unknown_order" not in world.kernel.blocks
