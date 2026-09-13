"""TB-S3 kernel model — regressions for the Codex round on PR #365 (`f8e39af`, eight P1s).

Each test reproduces one finding as reported (spec §2e review contract: a §1/§2 finding is
accepted only with a reproducing scenario), then the kernel fix makes it pass.
"""
from __future__ import annotations

from book_protocol import Bracket

from tests.ops.tb_s3_kernel.broker import STALENESS_WINDOW
from tests.ops.tb_s3_kernel.harness import BAR, MIN, entry, fill_lot, make_world


# 1 — a resting stop entry on a lost feed is cancelled, not left to trigger later
def test_feed_loss_cancels_a_resting_entry_even_when_the_symbol_is_flat():
    """Feed loss cancels a resting entry even when the symbol is flat."""
    world = make_world()
    decision = world.kernel.admit_entry(
        entry("orb_mnq_v7", 1, Bracket(stop=18_450.0), order_type="stop", price=18_500.0),
        world.now)
    world.advance(MIN)
    world.snap("MNQ")                                                # flat, entry working
    for sym in ("6J", "MYM", "MGC"):
        world.daemon.on_bar(sym, world.now)
    world.advance(STALENESS_WINDOW + MIN)
    world.snap("MNQ")                                                # still flat, still working
    op_id = world.daemon.feed_loss_check("orb_mnq_v7", world.now)
    assert op_id is not None                                          # flatness is not a no-op
    assert "feed" in world.kernel.blocks
    assert world.kernel.pending[decision.ref].cancel_requested
    assert world.broker.orders[decision.ref].status == "cancelled"    # cannot trigger later
    world.advance(MIN)
    world.snap("MNQ")
    assert world.kernel.pending[decision.ref].status == "cancelled"
    assert world.kernel.ledger.reserved["orb_mnq_v7"] == 0


# 2 — the close_rejected block survives until every rejected close is resolved
def test_close_rejected_block_retained_while_any_rejected_close_remains():
    """Close-rejected block retained while any rejected close remains."""
    world = make_world()
    lot_mgc = fill_lot(world, "vanguard_mgc", 1, Bracket(stop=2_400.0))
    lot_mnq = fill_lot(world, "orb_mnq_v7", 1, Bracket(stop=18_450.0))
    world.broker.inject["close"] = "reject"
    first = world.kernel.handle_exit("vanguard_mgc", world.now, fill_id=lot_mgc)
    world.broker.inject["close"] = "reject"
    second = world.kernel.handle_exit("orb_mnq_v7", world.now, fill_id=lot_mnq)
    assert first.status == second.status == "rejected"
    world.advance(BAR + MIN)
    world.snap()
    world.kernel.retry(second.op_id, world.now)
    world.advance(MIN)
    world.snap()
    assert second.status == "complete" and first.status == "rejected"
    assert "close_rejected" in world.kernel.blocks                    # first still unresolved
    assert world.kernel.admit_entry(entry("aegis_6j", 1), world.now).reason == "policy_block"
    world.kernel.retry(first.op_id, world.now)
    world.advance(MIN)
    world.snap()
    assert first.status == "complete" and "close_rejected" not in world.kernel.blocks


# 3 — evidence must be strictly newer than the operation it completes
def test_read_stamped_at_the_same_instant_never_completes_a_close_as_a_noop():
    """Read stamped at the same instant never completes a close as a no-op."""
    world = make_world()
    decision = world.kernel.admit_entry(
        entry("orb_mnq_v7", 1, Bracket(stop=18_450.0), order_type="stop", price=18_500.0),
        world.now)
    world.advance(BAR)
    world.snap("MNQ")                                                # read at T: flat, resting
    world.broker.trigger(decision.ref)                               # fills at T, no clock move
    op = world.kernel.close("sym", "MNQ", world.now, "eod_flatten")   # prepared at T
    assert op.status == "sent" and world.kernel.events("close_noop") == []
    assert world.broker.positions["MNQ"] == 0                         # the close reached the route
    world.advance(MIN)
    world.snap("MNQ")
    assert op.status == "complete"


# 4 — protection is working only with the intended parameters
def test_stop_at_the_wrong_price_is_a_protection_gap():
    """Stop at the wrong price is a protection gap."""
    world = make_world()
    lot = fill_lot(world, "vanguard_mgc", 1, Bracket(stop=2_400.0))
    stop_ref = world.kernel.expected[lot].working["stop"]
    world.broker.orders[stop_ref].price = 2_380.0                     # moved behind our back
    world.advance(MIN)
    world.snap("MGC")
    assert world.kernel.expected[lot].status["stop"] == "missing"
    assert "protection_gap" in world.kernel.blocks
    assert any(o.reason == "protection_gap_recovery" and o.scope_id == lot
               for o in world.kernel.operations.values())


# 5 — a rejected first protection blocks immediately, not on the next read
def test_rejected_attach_blocks_and_recovers_immediately():
    """Rejected attach blocks and recovers immediately."""
    world = make_world()
    lot = fill_lot(world, "dj30_mym_p250", 22)
    world.broker.inject["attach"] = "reject"
    world.advance(BAR)
    decision = world.kernel.amend(lot, Bracket(stop=41_200.0), world.now)
    assert decision.op.status == "rejected"
    assert "protection_gap" in world.kernel.blocks                    # before any evidence
    recovery = [o for o in world.kernel.operations.values()
                if o.reason == "protection_gap_recovery" and o.scope_id == lot]
    assert recovery and recovery[0].status == "sent"
    assert world.kernel.admit_entry(entry("vanguard_mgc", 1), world.now).reason == "policy_block"


# 6 — a takeover cancels partially filled orders and waits for confirmed cancellation
def _book_with_partial_striker(world):
    decision = world.kernel.admit_entry(entry("dj30_mym_p250", 22), world.now)
    world.broker.fill(decision.ref, qty=10)                           # 12 still working
    fill_lot(world, "vanguard_mgc", 2, Bracket(stop=2_400.0))
    fill_lot(world, "orb_mnq_v7", 1, Bracket(stop=18_450.0))
    assert world.kernel.pending[decision.ref].status == "partial"
    assert world.kernel.ledger.reserved["dj30_mym_p250"] == 12
    return decision.ref


def test_takeover_cancels_a_partially_filled_order_before_admitting_aegis():
    """Takeover cancels a partially filled order before admitting Aegis."""
    world = make_world()
    partial_ref = _book_with_partial_striker(world)
    aegis = entry("aegis_6j", 8, Bracket(stop=0.0069))
    plan = world.kernel.admit_entry(aegis, world.now).takeover
    assert plan is not None
    world.kernel.takeover(plan, world.now)
    assert world.broker.orders[partial_ref].status == "cancelled"     # the remainder was cancelled
    world.advance(MIN)
    world.snap()
    settled = world.kernel.settle_takeover(aegis, world.now)
    assert settled.ok and world.kernel.ledger.micro_used() == 80


def test_takeover_refused_when_a_cancel_is_not_confirmed_by_evidence():
    """Takeover refused when a cancel is not confirmed by evidence."""
    world = make_world()
    partial_ref = _book_with_partial_striker(world)
    aegis = entry("aegis_6j", 8, Bracket(stop=0.0069))
    plan = world.kernel.admit_entry(aegis, world.now).takeover
    world.broker.inject["cancel"] = "unknown"                         # cancel lost at the route
    world.kernel.takeover(plan, world.now)
    world.broker.orders[partial_ref].status = "working"               # it never cancelled
    world.advance(MIN)
    world.snap()
    settled = world.kernel.settle_takeover(aegis, world.now)
    assert not settled.ok and settled.reason == "takeover_refused"


# 7 — a trail change that delays or widens the stop is a loosening amend
def test_loosening_trail_change_refused_under_a_block_tightening_admitted():
    """Loosening trail change refused under a block; tightening admitted."""
    world = make_world()
    bracket = Bracket(stop=18_450.0, trail_activation_ticks=40, trail_offset_ticks=20)
    lot = fill_lot(world, "orb_mnq_v7", 1, bracket)
    world.kernel.block("eod", "test")
    world.advance(MIN)
    world.snap("MNQ")
    wider = world.kernel.amend(lot, Bracket(stop=18_450.0, trail_activation_ticks=40,
                                            trail_offset_ticks=30), world.now)
    assert wider.reason == "policy_block"
    later = world.kernel.amend(lot, Bracket(stop=18_450.0, trail_activation_ticks=50,
                                            trail_offset_ticks=20), world.now)
    assert later.reason == "policy_block"
    tighter = world.kernel.amend(lot, Bracket(stop=18_450.0, trail_activation_ticks=30,
                                              trail_offset_ticks=20), world.now)
    assert tighter.ok


# 8 — kill disarms on the completion transition itself, not on a status poll
def test_kill_disarms_when_evidence_completes_the_flatten():
    """Kill disarms when evidence completes the flatten."""
    world = make_world()
    fill_lot(world, "aegis_6j", 3, Bracket(stop=0.0069))
    world.kernel.kill(world.now)
    assert not world.kernel.dry_run
    world.advance(MIN)
    world.snap()                                                     # no status call in between
    assert world.kernel.dry_run
    assert world.kernel.events("disarmed")
