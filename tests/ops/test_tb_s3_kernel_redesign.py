"""Contract regressions: independently stated outcomes across composed events."""
import copy
from dataclasses import replace

import pytest

from book_protocol import Bracket
from tests.ops.tb_s3_kernel.harness import BAR, MIN, entry, fill_lot, make_world
from tests.ops.tb_s3_kernel.kernel import Kernel, KernelRefusal, Store


def restart(world):
    """Replace the listener, retaining only its durable store and external broker."""
    world.kernel = Kernel.restart(world.kernel.store, world.broker, world.clock, world.now,
                                  protection_cases=world.kernel.protection_cases)
    world.daemon.kernel = world.kernel
    return world.kernel


@pytest.mark.parametrize("reboot", [False, True])
def test_retried_rejection_still_owns_its_block_after_another_owner_completes(reboot):
    """Changing A from rejected to sent must not let B discharge A's rejection."""
    w = make_world()
    a = fill_lot(w, "vanguard_mgc", 1, Bracket(stop=90))
    b = fill_lot(w, "orb_mnq_v7", 1, Bracket(stop=90))
    ops = []
    for lot in (a, b):
        w.broker.inject["close"] = "reject"
        ops.append(w.kernel.close("fill", lot, w.now, "exit"))
    w.advance(BAR)
    w.snap()
    w.broker.inject["close"] = "unknown_lost"
    w.kernel.retry(ops[0].op_id, w.now)
    w.kernel.retry(ops[1].op_id, w.now)
    if reboot:
        restart(w)
    w.advance(MIN)
    w.snap("MNQ")
    assert "close_rejected" in w.kernel.blocks
    assert w.kernel.operations[ops[0].op_id].status == "unknown"
    assert w.kernel.admit_entry(entry("aegis_6j", 1), w.now).reason == "policy_block"


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


def test_old_full_read_cannot_regress_position_after_newer_position_only_read():
    """Order evidence cannot overwrite newer position evidence when delivered late."""
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 1), w.now)
    w.advance(MIN)
    old = w.broker.snapshot("MGC")
    w.broker.fill(d.ref)
    w.advance(MIN)
    latest = w.broker.snapshot("MGC")
    w.kernel.apply_evidence(replace(latest, working=(), order_status={}, fills={}, lots={},
                                   order_level=False))
    w.kernel.apply_evidence(old)
    assert w.kernel.position("MGC", w.now) == ("CONFIRMED", 1)


@pytest.mark.parametrize("reboot", [False, True])
def test_replayed_read_cannot_restore_consumed_exposure(reboot):
    """A delayed pre-close read must not resurrect lots or protection after flatness."""
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    old = w.broker.snapshot("MGC")
    w.kernel.handle_exit("vanguard_mgc", w.now, fill_id=lot)
    w.advance(MIN)
    w.snap()
    if reboot:
        restart(w)
    w.kernel.apply_evidence(old)
    assert w.kernel.lots[lot].qty == 0
    assert w.kernel.position("MGC", w.now) == ("CONFIRMED", 0)
    assert w.kernel.ledger.confirmed["vanguard_mgc"] == 0


def test_cached_read_cannot_reconcile_a_later_retry():
    """Evidence after prepare but before the latest dispatch cannot authorize retry."""
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    w.broker.inject["close"] = "unknown_lost"
    op = w.kernel.close("fill", lot, w.now, "exit")
    w.advance(MIN)
    cached = w.broker.snapshot("MGC")
    w.kernel.apply_evidence(cached)
    w.broker.inject["close"] = "unknown_lost"
    w.kernel.retry(op.op_id, w.now)
    w.kernel.apply_evidence(cached)
    with pytest.raises(KernelRefusal):
        w.kernel.retry(op.op_id, w.now)


def test_unknown_component_does_not_whitelist_an_unsent_sibling():
    """Only an actually dispatched component may explain a transitional value."""
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90, limit=120))
    w.broker.inject["modify"] = "unknown"
    d = w.kernel.amend(lot, Bracket(stop=95, limit=125), w.now)
    w.advance(MIN)
    w.snap()
    assert "protection_gap" not in w.kernel.blocks     # 95/120 is legitimate
    assert d.op.status != "complete"                  # unsent limit still owed
    limit = w.kernel.expected[lot].working["limit"]
    w.broker.orders[limit].price = 125                  # unexplained unsent value
    w.advance(MIN)
    w.snap()
    assert "protection_gap" in w.kernel.blocks


def test_protection_quantity_mismatch_is_a_gap():
    """Presence and price alone do not protect the complete residual quantity."""
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    ref = w.kernel.expected[lot].working["stop"]
    w.broker.orders[ref].qty = 1
    w.advance(MIN)
    w.snap()
    assert "protection_gap" in w.kernel.blocks


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


def test_legacy_store_is_rejected_explicitly_instead_of_booting_empty():
    """An incompatible snapshot has a specific fail-closed schema outcome."""
    w = make_world()
    w.kernel.store.data = {"pending": {}, "dry_run": False}
    with pytest.raises(KernelRefusal, match="schema"):
        restart(w)


class Crash(RuntimeError):
    """Abrupt process death; callers may not finish their current transition."""


def crash_once(kernel, kind, boundary):
    """Interrupt one real dispatch at a persisted boundary, without changing its result."""
    def hook(stage, effect):
        if effect.kind == kind and stage == boundary:
            kernel.effect_hook = None
            raise Crash(stage)
    kernel.effect_hook = hook


@pytest.mark.parametrize("boundary", ["planned", "dispatching", "executed", "recorded"])
def test_close_crash_never_duplicates_an_unreconciled_dispatch(boundary):
    """A crash preserves planned work or an unknown attempt, never an automatic retry."""
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    crash_once(w.kernel, "close", boundary)
    with pytest.raises(Crash):
        w.kernel.close("fill", lot, w.now, "exit", op_id="crash-close")
    restart(w)
    before = len([e for e in w.broker.log if e["event"] == "close"])
    w.kernel.progress(w.now)
    after = len([e for e in w.broker.log if e["event"] == "close"])
    assert after - before == (1 if boundary == "planned" else 0)
    w.advance(MIN)
    w.snap()
    op = w.kernel.operations["crash-close"]
    if boundary == "dispatching":
        w.kernel.retry(op.op_id, w.now)
        w.advance(MIN)
        w.snap()
    assert op.status == "complete"
    assert w.kernel.lots[lot].qty == 0
    assert len([e for e in w.broker.log if e["event"] == "close"]) == 1


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


@pytest.mark.parametrize("boundary", ["planned", "dispatching", "executed", "recorded"])
def test_first_attach_crash_preserves_protection_or_owned_recovery(boundary):
    """A lost attach outcome leaves a recoverable attempt; missing protection is owned."""
    w = make_world()
    lot = fill_lot(w, "dj30_mym_p250", 2)
    crash_once(w.kernel, "attach", boundary)
    with pytest.raises(Crash):
        w.kernel.amend(lot, Bracket(stop=90), w.now)
    restart(w)
    w.kernel.progress(w.now)
    w.advance(MIN)
    w.snap()
    assert w.kernel.lots[lot].qty == 0 or (
        w.kernel.expected[lot].status["stop"] == "working"
        or "protection_gap" in w.kernel.blocks)
    w.advance(MIN)
    w.snap()
    assert w.kernel.lots[lot].qty == (0 if boundary == "dispatching" else 2)


@pytest.mark.parametrize("first,second", [("unknown", "reject"), (None, "reject"),
                                         ("reject", None), ("unknown_lost", None)])
def test_mixed_component_outcomes_preserve_only_observed_or_dispatched_values(first, second):
    """A successful sibling is legitimate; an unsent or rejected value is not."""
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90, limit=120))
    w.broker.inject["modify"] = [first, second]
    w.kernel.amend(lot, Bracket(stop=95, limit=125), w.now)
    restart(w)
    w.advance(MIN)
    w.snap()
    assert "protection_gap" not in w.kernel.blocks
    assert w.broker.positions["MGC"] == 2
    assert w.kernel.expected[lot].status == {"stop": "working", "limit": "working"}


@pytest.mark.parametrize("active", [False, True])
@pytest.mark.parametrize("activation,offset,expected", [
    (50, 20, "policy_block"), (40, 30, "policy_block"),
    (30, 30, "policy_block"), (50, 10, "policy_block"), (30, 10, "sent")])
def test_trail_direction_table_uses_observed_static_parameters(active, activation, offset, expected):
    """Mixed directions are risk-adds; active native anchors remain untouched."""
    w = make_world()
    lot = fill_lot(w, "orb_mnq_v7", 1, Bracket(trail_activation_ticks=40, trail_offset_ticks=20))
    if active:
        w.broker.move_price("MNQ", 160)
    w.advance(MIN)
    w.snap()
    w.kernel.block("eod", "test")
    d = w.kernel.amend(lot, Bracket(trail_activation_ticks=activation,
                                  trail_offset_ticks=offset), w.now)
    assert d.reason == expected
    if d.ok:
        w.advance(MIN)
        w.snap()
        assert d.op.status == "complete"


def test_future_dated_or_unordered_read_cannot_complete_an_operation():
    """Neither claimed future time nor missing acquisition identity proves completion."""
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 1)
    op = w.kernel.close("fill", lot, w.now, "exit")
    read = w.broker.snapshot("MGC")
    w.kernel.apply_evidence(replace(read, as_of=w.now + MIN))
    assert op.status == "sent"
    w.advance(MIN)
    w.kernel.apply_evidence(replace(w.broker.snapshot("MGC"), acquired=0))
    assert op.status == "sent"


def test_backdated_command_does_not_make_preacquired_evidence_causal():
    """The command's supplied timestamp is not evidence of its acquisition order."""
    w = make_world()
    w.advance(MIN)
    w.snap()
    op = w.kernel.close("sym", "MGC", w.now - MIN, "exit")
    assert op.status == "sent"


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


def test_accepted_close_is_not_executed_until_the_broker_processes_it():
    """Acceptance, execution and evidence are three distinct inputs."""
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    w.broker.inject["close"] = "defer"
    op = w.kernel.close("fill", lot, w.now, "exit")
    assert op.status == "sent"
    assert w.broker.positions["MGC"] == 2
    w.advance(MIN)
    w.snap()
    assert op.status != "complete"
    w.broker.execute_next()
    assert op.status != "complete"
    w.advance(MIN)
    w.snap()
    assert op.status == "complete"


def test_restart_cannot_retry_a_request_still_pending_at_the_broker():
    """A covering read must exclude a pending original before another send is possible."""
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    w.broker.inject["close"] = "defer"
    crash_once(w.kernel, "close", "executed")
    with pytest.raises(Crash):
        w.kernel.close("fill", lot, w.now, "exit", op_id="pending-close")
    assert w.broker.positions["MGC"] == 2
    restart(w)
    w.advance(MIN)
    w.snap()
    with pytest.raises(KernelRefusal):
        w.kernel.retry("pending-close", w.now)
    w.broker.execute_next()
    w.advance(MIN)
    w.snap()
    assert w.kernel.operations["pending-close"].status == "complete"


def test_pending_entry_cannot_be_resolved_as_absent_after_restart():
    """An acknowledged request waiting at the route still owns its reservation."""
    w = make_world()
    w.broker.inject["place"] = "defer"
    crash_once(w.kernel, "place", "executed")
    with pytest.raises(Crash):
        w.kernel.admit_entry(entry("vanguard_mgc", 2), w.now)
    assert w.broker.orders == {}
    restart(w)
    w.advance(MIN)
    w.snap()
    assert w.kernel.ledger.reserved["vanguard_mgc"] == 2
    assert "unknown_order" in w.kernel.blocks
    w.broker.execute_next()
    w.advance(MIN)
    w.snap()
    assert w.kernel.pending["ord-1"].status == "accepted"


def test_completed_bounded_reduction_discharges_its_rejection_obligation():
    """Recovery of the requested reduction must not require an unrequested full exit."""
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 3, Bracket(stop=90))
    w.broker.inject["close"] = "reject"
    op = w.kernel.close("fill", lot, w.now, "exit", qty=1)
    w.advance(BAR)
    w.snap()
    w.kernel.retry(op.op_id, w.now)
    w.advance(MIN)
    w.snap()
    assert op.status == "complete"
    assert w.kernel.lots[lot].qty == 2
    assert "close_rejected" not in w.kernel.blocks


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


def test_unknown_unapplied_amend_can_be_reissued_after_covering_old_value_evidence():
    """A fenced read proving the old component remains permits the port's next reissue."""
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    w.broker.inject["modify"] = "unknown_lost"
    w.kernel.amend(lot, Bracket(stop=95), w.now)
    w.advance(MIN)
    w.snap()
    assert w.kernel.amend(lot, Bracket(stop=95), w.now).ok


def test_later_full_fill_exit_does_not_collapse_into_a_pending_bounded_exit():
    """Different requested reductions own different work even on the same fill."""
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 3, Bracket(stop=90))
    first = w.kernel.handle_exit("vanguard_mgc", w.now, fill_id=lot, qty=1)
    second = w.kernel.handle_exit("vanguard_mgc", w.now, fill_id=lot)
    assert first is not second
    w.advance(MIN)
    w.snap()
    w.advance(MIN)
    w.snap()
    assert first.status == second.status == "complete"
    assert w.kernel.lots[lot].qty == 0


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


def test_restart_cancels_never_dispatched_entry_before_timeout_and_absence():
    """A planned entry cannot be sent after absence resolution released its reservation."""
    w = make_world()
    crash_once(w.kernel, "place", "planned")
    with pytest.raises(Crash):
        w.kernel.admit_entry(entry("vanguard_mgc", 2), w.now)
    restart(w)
    w.advance(2 * BAR)
    w.snap("MGC")                  # deliberately deliver the entry symbol first
    w.kernel.progress(w.now)
    assert w.broker.orders == {}
    assert w.kernel.pending["ord-1"].status == "not_sent"
    assert w.kernel.pending["ord-1"].reserved == 0
    assert w.kernel.ledger.reserved["vanguard_mgc"] == 0


def test_restart_does_not_dispatch_a_planned_loosening_amend_under_its_block():
    """A never-dispatched risk-add requires new admission after restart reconciliation."""
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    ref = w.kernel.expected[lot].working["stop"]
    crash_once(w.kernel, "modify", "planned")
    with pytest.raises(Crash):
        w.kernel.amend(lot, Bracket(stop=85), w.now)
    restart(w)
    w.kernel.progress(w.now)
    w.advance(MIN)
    w.snap()
    assert w.broker.orders[ref].price == 90


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
    assert w.kernel.kill_status(False, w.now)["complete"] is True


@pytest.mark.parametrize("bad_field,bad_value", [("side", "buy"), ("order_type", "market")])
def test_bounded_close_requires_the_same_residual_protection_contract(bad_field, bad_value):
    """Wrong-side or wrong-type protection cannot complete a bounded reduction."""
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 3, Bracket(stop=90))
    op = w.kernel.close("fill", lot, w.now, "exit", qty=1)
    ref = w.kernel.expected[lot].working["stop"]
    setattr(w.broker.orders[ref], bad_field, bad_value)
    w.advance(MIN)
    w.snap()
    assert op.status != "complete"
    assert "protection_gap" in w.kernel.blocks
    w.advance(MIN)
    w.snap()
    assert op.status == "complete"
    assert w.kernel.lots[lot].qty == 0


def test_restart_with_missing_store_refuses_to_boot_empty():
    """Loss of durable ownership must not admit against an empty capacity ledger."""
    w = make_world()
    fill_lot(w, "dj30_mym_p250", 22)
    with pytest.raises(KernelRefusal, match="schema"):
        Kernel.restart(Store(), w.broker, w.clock, w.now)


def test_restart_halts_on_unallocated_bare_broker_exposure():
    """A bare orphan has no protective order for the existing orphan-order scan to find."""
    w = make_world()
    w.broker.place(sym="MYM", leg_id="dj30_mym_p250", kind="entry", side="buy", qty=22,
                   ref="external")
    w.broker.fill("external")
    restart(w)
    w.advance(MIN)
    w.snap()
    assert not w.kernel.reconcile_restart(w.now).ok
    assert w.kernel.admit_entry(entry("aegis_6j", 8), w.now).reason == "policy_block"


def test_resetting_route_cannot_modify_an_inactive_trail_that_might_activate_before_execution():
    """Admission cannot promise anchor preservation from an earlier inactive observation."""
    w = make_world()
    lot = fill_lot(w, "orb_mnq_v7", 1, Bracket(trail_activation_ticks=40, trail_offset_ticks=20))
    w.broker.modify_resets_trail_anchor = True
    w.broker.inject["modify"] = "defer"
    decision = w.kernel.amend(lot, Bracket(trail_activation_ticks=30, trail_offset_ticks=10), w.now)
    assert decision.reason == "amend_deferred"
    w.broker.move_price("MNQ", 160)
    ref = w.kernel.expected[lot].working["trail"]
    assert w.broker.orders[ref].trail_active
    assert w.broker.orders[ref].trail_anchor == 160


@pytest.mark.parametrize("outcome,want", [("reject", "rejected"), ("unknown_lost", "unknown")])
def test_deferred_close_rejection_reaches_same_operation_recovery(outcome, want):
    """A rejection after transport acceptance is evidence, not a permanently sent close."""
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    w.broker.inject["close"] = "defer"
    op = w.kernel.close("fill", lot, w.now, "exit")
    w.broker.inject["close"] = outcome
    w.broker.execute_next()
    w.advance(BAR)
    w.snap()
    assert op.status == want
    assert w.kernel.risk_add_blocked
    w.kernel.retry(op.op_id, w.now)
    w.advance(MIN)
    w.snap()
    assert op.status == "complete"


def test_unknown_cancel_can_retry_only_after_covering_nonpending_evidence():
    """Unknown cancellation retains the remainder but is recoverable after reconciliation."""
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 2), w.now)
    w.broker.inject["cancel"] = "unknown_lost"
    w.kernel.cancel(d.ref, w.now)
    assert not w.kernel.cancel(d.ref, w.now).ok
    w.advance(MIN)
    w.snap()
    assert w.kernel.cancel(d.ref, w.now).ok
    w.advance(MIN)
    w.snap()
    assert w.kernel.pending[d.ref].reserved == 0


def test_late_attach_rejection_after_gap_recovery_preserves_consumed_scope():
    """A late outcome cannot require protection records already retired by flat evidence."""
    w = make_world()
    lot = fill_lot(w, "dj30_mym_p250", 2)
    w.broker.inject["attach"] = "defer"
    op = w.kernel.amend(lot, Bracket(stop=90), w.now).op
    w.advance(MIN)
    w.snap()
    w.advance(MIN)
    w.snap()
    assert lot not in w.kernel.expected
    w.broker.execute_next()
    w.advance(MIN)
    w.snap()
    assert op.status == "complete"
    assert w.kernel.lots[lot].qty == 0
    assert "protection_gap" not in w.kernel.blocks
