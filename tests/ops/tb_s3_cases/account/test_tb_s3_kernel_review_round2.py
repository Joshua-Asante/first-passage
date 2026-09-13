"""TB-S3 kernel model — regressions for the Codex round on PR #365 (`f8e39af`, eight P1s).

Each test reproduces one finding as reported (spec §2e review contract: a §1/§2 finding is
accepted only with a reproducing scenario), then the kernel fix makes it pass.
"""


from __future__ import annotations


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.broker import STALENESS_WINDOW


from tests.ops.tb_s3_kernel.account_harness import BAR, MIN, entry, fill_lot, make_world


def _book_with_partial_striker(world):
    decision = world.kernel.admit_entry(entry("dj30_mym_p250", 22), world.now)
    world.broker.fill(decision.ref, qty=10)                           # 12 still working
    fill_lot(world, "vanguard_mgc", 2, Bracket(stop=2_400.0))
    fill_lot(world, "orb_mnq_v7", 1, Bracket(stop=18_450.0))
    assert world.kernel.pending[decision.ref].status == "partial"
    assert world.kernel.ledger.reserved["dj30_mym_p250"] == 12
    return decision.ref


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
