"""Contract regressions: independently stated outcomes across composed events."""


import copy


from dataclasses import replace


import pytest


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.account_harness import BAR, MIN, entry, fill_lot, make_world


from tests.ops.tb_s3_kernel.account import AccountKernel as Kernel
from tests.ops.tb_s3_kernel.kernel import KernelRefusal, Store


def restart(world):
    """Replace the listener, retaining only its durable store and external broker."""
    world.kernel = type(world.kernel).restart(world.kernel.store, world.broker, world.clock, world.now,
                                  protection_cases=world.kernel.protection_cases)
    if hasattr(world, "daemon"):
        world.daemon.kernel = world.kernel
    return world.kernel


class Crash(RuntimeError):
    """Abrupt process death; callers may not finish their current transition."""


def crash_once(kernel, kind, boundary):
    """Interrupt one real dispatch at a persisted boundary, without changing its result."""
    def hook(stage, effect):
        if effect.kind == kind and stage == boundary:
            kernel.effect_hook = None
            raise Crash(stage)
    kernel.effect_hook = hook


def test_flat_position_with_rejected_cancel_does_not_complete_feed_obligation():
    """Zero exposure cannot hide an executable remainder after feed loss."""
    w = make_world()
    d = w.kernel.admit_entry(entry("orb_mnq_v7", 2, Bracket(stop=90),
                                  order_type="stop", price=100), w.now)
    w.broker.fill(d.ref, qty=1)
    w.advance(MIN)
    w.snap()
    w.broker.inject["cancel"] = "reject"
    op = w.kernel.on_flat_intent("feed-episode", "orb_mnq_v7", w.now)
    w.advance(MIN)
    w.snap()
    assert op.status != "complete"
    assert w.kernel.pending[d.ref].reserved == 1
    w.broker.fill(d.ref)                    # fill races the rejected cancel
    w.advance(MIN)
    w.snap()
    w.advance(MIN)
    w.snap()
    assert w.broker.positions["MNQ"] == 0
    assert op.status == "complete"
    assert w.kernel.pending[d.ref].reserved == 0
    assert "feed" in w.kernel.blocks


def test_session_open_does_not_abandon_unresolved_feed_work():
    """Session latch expiry does not resolve the cancellation owner's obligation."""
    w = make_world()
    d = w.kernel.admit_entry(entry("orb_mnq_v7", 1, order_type="stop", price=100), w.now)
    w.broker.inject["cancel"] = "reject"
    w.kernel.on_flat_intent("feed-episode", "orb_mnq_v7", w.now)
    w.advance(MIN)
    w.snap()
    w.kernel.session_open()
    assert w.kernel.risk_add_blocked
    assert w.kernel.pending[d.ref].reserved == 1


def test_takeover_and_reservations_survive_restart_before_confirmation():
    """Restart cannot forget an in-progress takeover or erase its remaining reserve."""
    w = make_world()
    d = w.kernel.admit_entry(entry("dj30_mym_p250", 22), w.now)
    w.broker.fill(d.ref, qty=10)
    w.advance(MIN)
    w.snap()
    request = entry("aegis_6j", 8)
    plan = w.kernel.admit_entry(request, w.now).takeover
    w.kernel.takeover(plan, w.now)
    restart(w)
    w.advance(MIN)
    w.snap()
    w.kernel.reconcile_restart(w.now)
    result = w.kernel.settle_takeover(request, w.now)
    assert result.ok
    assert w.kernel.ledger.micro_used() == 80
    assert w.kernel.pending[d.ref].reserved == 0


def test_kill_queries_are_pure_and_disarm_survives_restart():
    """Completion performs disarm; any number of queries leave durable state unchanged."""
    w = make_world()
    fill_lot(w, "vanguard_mgc", 1)
    w.kernel.kill(w.now)
    w.advance(MIN)
    w.snap()
    before = copy.deepcopy(w.kernel.store.data)
    for _ in range(3):
        assert w.kernel.kill_status(False, w.now)["disarmed"]
    assert w.kernel.store.data == before
    restart(w)
    assert w.kernel.dry_run


@pytest.mark.parametrize("boundary", ["planned", "dispatching", "executed", "recorded"])
def test_kill_crash_retains_all_symbol_work_and_drives_disarm(boundary):
    """Crashing on the first close cannot lose the rest of the kill request."""
    w = make_world()
    fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    crash_once(w.kernel, "close", boundary)
    with pytest.raises(Crash):
        w.kernel.kill(w.now)
    restart(w)
    w.kernel.progress(w.now)
    w.advance(MIN)
    w.snap()
    assert {o.sym for o in w.kernel.operations.values() if o.reason == "kill"} == {
        "6J", "MGC", "MYM", "MNQ"}
    assert w.kernel.dry_run
    assert w.kernel.store.data["dry_run"]


def test_feed_block_and_operation_are_durable_before_cancel_dispatch():
    """Crash on cancellation must retain both the session latch and remaining work."""
    w = make_world()
    d = w.kernel.admit_entry(entry("orb_mnq_v7", 1, order_type="stop", price=100), w.now)
    crash_once(w.kernel, "cancel", "dispatching")
    with pytest.raises(Crash):
        w.kernel.on_flat_intent("feed-test", "orb_mnq_v7", w.now)
    restart(w)
    assert "feed" in w.kernel.blocks
    assert "feed-test" in w.kernel.operations
    assert w.kernel.pending[d.ref].reserved == 1
    w.advance(MIN)
    w.snap()
    assert w.kernel.operations["feed-test"].status != "complete"


@pytest.mark.parametrize("gate", ["overlay", "capability", "stale", "wrong_requester"])
def test_takeover_settlement_rechecks_current_admission_conditions(gate):
    """A completed displacement is no authority to bypass the requester's admission."""
    w = make_world()
    fill_lot(w, "dj30_mym_p250", 22)
    request = entry("aegis_6j", 8)
    plan = w.kernel.admit_entry(request, w.now).takeover
    w.kernel.takeover(plan, w.now)
    w.advance(MIN)
    w.snap()
    if gate == "overlay":
        w.kernel.block("overlay", "new-condition")
    elif gate == "capability":
        w.broker.caps["d"] = "not supported"
    elif gate == "stale":
        w.advance(2 * BAR)
    else:
        request = entry("orb_mnq_v7", 1)
    count = len([e for e in w.broker.log if e["event"] == "place"])
    assert not w.kernel.settle_takeover(request, w.now).ok
    assert len([e for e in w.broker.log if e["event"] == "place"]) == count


@pytest.mark.parametrize("boundary", ["planned", "dispatching", "executed", "recorded"])
def test_takeover_crash_preserves_every_displaced_leg(boundary):
    """All displaced legs are durably owned before cancellation/close dispatch starts."""
    w = make_world()
    fill_lot(w, "dj30_mym_p250", 22)
    fill_lot(w, "orb_mnq_v7", 10, Bracket(stop=90))
    request = entry("aegis_6j", 8)
    plan = w.kernel.admit_entry(request, w.now).takeover
    crash_once(w.kernel, "close", boundary)
    with pytest.raises(Crash):
        w.kernel.takeover(plan, w.now)
    restart(w)
    w.kernel.progress(w.now)
    assert {o.sym for o in w.kernel.operations.values() if o.reason == "capacity_takeover"} == {
        "MYM", "MNQ"}


def test_kill_does_not_report_complete_before_the_disarm_effect_is_applied():
    """Flatness alone is not completed kill while disarm is still planned."""
    w = make_world()
    w.kernel.kill(w.now)
    crash_once(w.kernel, "disarm", "planned")
    w.advance(MIN)
    with pytest.raises(Crash):
        w.snap()
    restart(w)
    assert w.kernel.kill_status(False, w.now)["complete"] is False
    w.kernel.progress(w.now)
    assert w.kernel.kill_status(False, w.now)["complete"] is False
    w.advance(MIN)
    w.snap()  # rev7: a planned disarm also needs post-restart account proof
    assert w.kernel.kill_status(False, w.now)["complete"] is True
