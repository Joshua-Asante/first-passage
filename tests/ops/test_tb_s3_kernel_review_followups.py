"""Composed evidence and recovery regressions from the second PR #365 review."""
import pytest

from book_protocol import Bracket

from tests.ops.tb_s3_kernel.harness import BAR, MIN, entry, fill_lot, make_world
from tests.ops.tb_s3_kernel.kernel import KernelRefusal
from tests.ops.test_tb_s3_kernel_review import _position_only


def test_position_only_read_preserves_healthy_protection():
    """Missing order data is not evidence of missing protection."""
    world = make_world()
    lot = fill_lot(world, "vanguard_mgc", 2, Bracket(stop=90))
    world.advance(MIN)
    world.kernel.apply_evidence(_position_only(world.broker.snapshot("MGC")))
    assert world.broker.positions["MGC"] == 2
    assert world.kernel.expected[lot].status["stop"] == "working"
    assert not world.kernel.blocks
    assert not world.kernel.operations


def test_protective_fill_updates_allocation_without_recovery_close():
    """A consumed bracket is a normal exit, not a protection gap."""
    world = make_world()
    lot = fill_lot(world, "vanguard_mgc", 2, Bracket(stop=90))
    world.broker.trigger(world.kernel.expected[lot].working["stop"])
    world.advance(MIN)
    world.snap("MGC")
    assert world.kernel.lots[lot].qty == 0
    assert world.kernel.ledger.confirmed["vanguard_mgc"] == 0
    assert lot not in world.kernel.expected
    assert not world.kernel.events("protection_gap")


def test_kill_after_eod_preserves_both_completion_requests():
    """Two reasons sharing a symbol must each reach a confirmed outcome."""
    world = make_world()
    fill_lot(world, "vanguard_mgc", 2)
    world.kernel.eod(world.now)
    world.kernel.kill(world.now)
    world.advance(MIN)
    world.snap()
    assert world.kernel.flatten_complete("eod_flatten", world.now)
    assert world.kernel.kill_status(False, world.now)["complete"]
    assert world.kernel.dry_run


def test_partial_entry_timeout_resolves_on_unchanged_partial_evidence():
    """A fresh partial status resolves uncertainty even with no additional fill."""
    world = make_world()
    decision = world.kernel.admit_entry(entry("vanguard_mgc", 2), world.now)
    world.broker.fill(decision.ref, qty=1)
    world.advance(MIN)
    world.snap("MGC")
    world.advance(2 * BAR)
    world.kernel.progress(world.now)
    assert world.kernel.pending[decision.ref].status == "unknown"
    world.snap("MGC")
    assert world.kernel.pending[decision.ref].status == "partial"
    assert world.kernel.ledger.reserved["vanguard_mgc"] == 1
    assert "unknown_order" not in world.kernel.blocks


def test_first_read_after_partial_fill_and_cancel_releases_only_remainder():
    """A single read may carry both an unseen fill and a terminal cancellation."""
    world = make_world()
    decision = world.kernel.admit_entry(entry("vanguard_mgc", 2), world.now)
    world.broker.fill(decision.ref, qty=1)
    world.kernel.cancel(decision.ref, world.now)
    world.advance(MIN)
    world.snap("MGC")
    assert world.kernel.pending[decision.ref].status == "cancelled"
    assert world.kernel.ledger.confirmed["vanguard_mgc"] == 1
    assert world.kernel.ledger.reserved["vanguard_mgc"] == 0


def test_requested_reduction_completes_with_protected_residual():
    """Finishing a quantity-limited reduction must not wait for the whole lot to exit."""
    world = make_world()
    lot = fill_lot(world, "vanguard_mgc", 3, Bracket(stop=90))
    op = world.kernel.handle_exit("vanguard_mgc", world.now, fill_id=lot, qty=1)
    world.advance(MIN)
    world.snap("MGC")
    assert op.status == "complete"
    assert world.kernel.lots[lot].qty == 2
    assert world.kernel.ledger.confirmed["vanguard_mgc"] == 2
    assert world.kernel.expected[lot].status["stop"] == "working"
    assert "unknown_order" not in world.kernel.blocks


def test_retry_unknown_amend_never_sends_close():
    """The close retry API must not turn protection uncertainty into an exit."""
    world = make_world()
    lot = fill_lot(world, "vanguard_mgc", 2, Bracket(stop=90))
    world.broker.inject["modify"] = "unknown"
    op = world.kernel.amend(lot, Bracket(stop=95), world.now).op
    stop_ref = world.kernel.expected[lot].working["stop"]
    world.broker.orders[stop_ref].price = 90
    world.advance(MIN)
    world.snap("MGC")
    with pytest.raises(KernelRefusal):
        world.kernel.retry(op.op_id, world.now)
    assert world.broker.positions["MGC"] == 2


def test_rejected_symbol_close_cannot_consume_bounded_close_progress():
    """Each close accounts for its own progress from the same broker read."""
    world = make_world()
    lot = fill_lot(world, "vanguard_mgc", 3, Bracket(stop=90))
    world.broker.inject["close"] = "reject"
    rejected = world.kernel.close("sym", "MGC", world.now, "exit")
    reduced = world.kernel.handle_exit("vanguard_mgc", world.now, fill_id=lot, qty=1)
    world.advance(MIN)
    world.snap("MGC")
    assert reduced.status == "complete"
    assert rejected.status == "rejected"
    assert world.kernel.lots[lot].qty == 2
    assert "close_rejected" in world.kernel.blocks


def test_protective_fill_settles_unknown_amend_as_consumed():
    """No protection operation remains unresolved after its lot is confirmed flat."""
    world = make_world()
    lot = fill_lot(world, "vanguard_mgc", 2, Bracket(stop=90))
    world.broker.inject["modify"] = "unknown"
    op = world.kernel.amend(lot, Bracket(stop=95), world.now).op
    world.broker.trigger(world.kernel.expected[lot].working["stop"])
    world.advance(MIN)
    world.snap("MGC")
    assert op.status == "complete"
    assert op.detail == "scope consumed"
    assert world.kernel.lots[lot].qty == 0
    assert "unknown_order" not in world.kernel.blocks
