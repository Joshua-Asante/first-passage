"""TB-S3 kernel model — one test per review-finding class from PR #360's Codex rounds.

Each test is the scenario the finding described, encoded against the model so that the
composition it exposed cannot regress silently. Names cite the spec clause that closed it.
"""


from __future__ import annotations


import pytest


from book_policy import TakeoverPlan


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.broker import NOT_SUPPORTED


from tests.ops.tb_s3_kernel.account_harness import BAR, MIN, entry, fill_lot, make_world


from tests.ops.tb_s3_kernel.account import AccountKernel as Kernel
from tests.ops.tb_s3_kernel.kernel import KernelRefusal


_lot = fill_lot


def _fill_book_except_aegis(world):
    _lot(world, "dj30_mym_p250", 22)
    _lot(world, "vanguard_mgc", 2, Bracket(stop=2_400.0))
    _lot(world, "orb_mnq_v7", 1, Bracket(stop=18_450.0))
    assert world.kernel.ledger.micro_used() == 25


def test_kill_and_stale_control_read_suppress_only_risk_adds():
    """Kill and stale control read suppress only risk adds."""
    world = make_world()
    assert world.daemon.may_emit("entry", world.now)
    world.kernel.kill(world.now)
    world.daemon.control_read(world.now)
    assert not world.daemon.may_emit("entry", world.now)
    assert world.daemon.may_emit("exit", world.now)
    assert world.daemon.may_emit("feed_loss_flat", world.now)
    world.advance(2 * BAR)                                           # control read stale
    assert not world.daemon.may_emit("add", world.now)
    assert world.daemon.may_emit("tightening_amend", world.now)
    world.daemon.emit_enabled = False                                 # the operator's ack
    assert not world.daemon.may_emit("exit", world.now)


def test_takeover_refused_when_a_displaced_close_is_unknown():
    """Takeover refused when a displaced close is unknown."""
    world = make_world()
    _fill_book_except_aegis(world)
    aegis = entry("aegis_6j", 8, Bracket(stop=0.0069))
    decision = world.kernel.admit_entry(aegis, world.now)
    assert decision.reason == "takeover_required"
    plan: TakeoverPlan = decision.takeover
    assert set(plan.displaced) == {"orb_mnq_v7", "vanguard_mgc", "dj30_mym_p250"}
    world.broker.inject["close"] = "unknown"
    world.kernel.takeover(plan, world.now)
    world.advance(MIN)
    stripped = [world.broker.snapshot(s) for s in ("MNQ", "MGC", "MYM")]
    for ev in stripped[1:]:
        world.kernel.apply_evidence(ev)
    settled = world.kernel.settle_takeover(aegis, world.now)
    assert not settled.ok and settled.reason == "takeover_refused"
    assert "aegis_6j" not in world.kernel.ledger.reserved or \
        world.kernel.ledger.reserved["aegis_6j"] == 0


def test_takeover_admits_aegis_only_after_every_displaced_leg_is_confirmed_flat():
    """Takeover admits aegis only after every displaced leg is confirmed flat."""
    world = make_world()
    _fill_book_except_aegis(world)
    aegis = entry("aegis_6j", 8, Bracket(stop=0.0069))
    plan = world.kernel.admit_entry(aegis, world.now).takeover
    world.kernel.takeover(plan, world.now)
    world.advance(MIN)
    world.snap()
    settled = world.kernel.settle_takeover(aegis, world.now)
    assert settled.ok and world.kernel.pending[settled.ref].qty == 8
    assert world.kernel.ledger.micro_used() == 80
