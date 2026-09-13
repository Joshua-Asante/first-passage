"""TB-S3 kernel model — one test per review-finding class from PR #360's Codex rounds.

Each test is the scenario the finding described, encoded against the model so that the
composition it exposed cannot regress silently. Names cite the spec clause that closed it.
"""
from __future__ import annotations

import pytest

from book_policy import TakeoverPlan
from book_protocol import Bracket

from tests.ops.tb_s3_kernel.broker import NOT_SUPPORTED
from tests.ops.tb_s3_kernel.harness import BAR, MIN, entry, fill_lot, make_world
from tests.ops.tb_s3_kernel.kernel import Kernel, KernelRefusal

_lot = fill_lot


# rev 5.3 round — "Separate kill from the all-emission gate" (§1 emit; S8; R-N)
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


# rev 5.3 round — "Prepare EOD closes before trusting cached flatness" (S7 (3), AC-8)
def test_close_noop_only_on_postdating_evidence_and_never_on_a_pre_buffer_snapshot():
    """Close noop only on postdating evidence and never on a pre buffer snapshot."""
    world = make_world()
    world.advance(BAR)
    stale = world.now
    world.snap("MGC")                                                 # flat, stale by the buffer
    world.advance(5 * MIN)
    sent = world.kernel.close("sym", "MGC", world.now, "eod_flatten")
    assert sent.status == "sent" and world.kernel.events("close_noop") == []
    noop = world.kernel.close("sym", "MGC", world.now, "kill", op_id="queued-noop")
    assert noop.status == "queued"
    world.advance(MIN)
    world.snap("MGC")
    assert sent.status == "complete"
    # The read was acquired after both real commands; backdating a new command is no proof.
    assert noop.status == "complete" and world.kernel.events("close_noop")
    assert stale < noop.prepared_at


# rev 5.3 round — "Require amendments to preserve native trailing state" (AMEND, L2(g))
def test_component_wise_amend_leaves_an_active_native_trail_untouched():
    """Component wise amend leaves an active native trail untouched."""
    world = make_world()
    bracket = Bracket(stop=18_450.0, trail_activation_ticks=40, trail_offset_ticks=20)
    lot = _lot(world, "orb_mnq_v7", 1, bracket)
    world.broker.move_price("MNQ", 160.0)                             # activates and anchors
    trail_ref = world.kernel.expected[lot].working["trail"]
    anchor = world.broker.orders[trail_ref].trail_anchor
    assert world.broker.orders[trail_ref].trail_active and anchor == 160.0
    world.advance(BAR)
    world.snap("MNQ")
    decision = world.kernel.amend(lot, Bracket(stop=18_470.0, trail_activation_ticks=40,
                                               trail_offset_ticks=20), world.now)
    assert decision.ok
    modifies = [e for e in world.broker.log if e["event"] == "modify"]
    assert len(modifies) == 1 and modifies[0]["ref"] != trail_ref     # only the stop moved
    assert world.broker.orders[trail_ref].trail_anchor == anchor
    world.broker.modify_resets_trail_anchor = True
    world.snap("MNQ")
    changed = world.kernel.amend(lot, Bracket(stop=18_470.0, trail_activation_ticks=50,
                                              trail_offset_ticks=20), world.now)
    assert changed.reason == "amend_deferred"                         # never moves the stop back


# rev 5.3 round — "Record intended entry brackets before confirmation" (I2, S1 (7), S9)
def test_intended_bracket_recorded_before_send_and_missing_child_orders_are_a_gap():
    """Intended bracket recorded before send and missing child orders are a gap."""
    world = make_world()
    world.broker.drop_attached_at_fill = True
    decision = world.kernel.admit_entry(entry("vanguard_mgc", 1, Bracket(stop=2_400.0)),
                                        world.now)
    assert world.kernel.pending[decision.ref].intended == {"stop": {"price": 2_400.0}}
    world.broker.fill(decision.ref)
    world.advance(MIN)
    world.snap("MGC")
    lot = world.broker.lot_id(decision.ref)
    assert world.kernel.expected[lot].status["stop"] == "missing"
    assert "protection_gap" in world.kernel.blocks
    recovery = [o for o in world.kernel.operations.values()
                if o.reason == "protection_gap_recovery"]
    assert recovery and recovery[0].scope_id == lot and recovery[0].status == "sent"
    world.advance(MIN)
    world.snap("MGC")
    assert recovery[0].status == "complete" and "protection_gap" not in world.kernel.blocks


# rev 5.3 round — "Gate bare entries on attachment capability" (S1 (5), L2(f))
def test_bare_entry_refused_at_admission_without_attach_capability():
    """Bare entry refused at admission without attach capability."""
    world = make_world(caps={"f": NOT_SUPPORTED})
    decision = world.kernel.admit_entry(entry("dj30_mym_p250", 22), world.now)
    assert decision.reason == "l2_refused"
    assert not world.broker.orders                                    # nothing reached the route


# rev 5.3 round — "Assign a durable block for rejected closes" (CLOSE; `close_rejected`)
def test_rejected_close_keeps_a_durable_block_until_confirmed_flat():
    """Rejected close keeps a durable block until confirmed flat."""
    world = make_world()
    lot = _lot(world, "vanguard_mgc", 1, Bracket(stop=2_400.0))
    world.broker.inject["close"] = "reject"
    op = world.kernel.handle_exit("vanguard_mgc", world.now, fill_id=lot)
    assert op.status == "rejected" and "close_rejected" in world.kernel.blocks
    assert world.kernel.admit_entry(entry("orb_mnq_v7", 1, Bracket(stop=1.0)), world.now).reason \
        == "policy_block"
    with pytest.raises(KernelRefusal):
        world.kernel.retry(op.op_id, world.now)                       # not reconciled yet
    world.advance(MIN)
    world.snap("MGC")                                                 # still open: reconciled
    with pytest.raises(KernelRefusal):
        world.kernel.retry(op.op_id, world.now)                       # once per bar at most
    world.advance(BAR)
    world.kernel.retry(op.op_id, world.now)
    assert op.status == "sent"
    world.advance(MIN)
    world.snap("MGC")
    assert op.status == "complete" and "close_rejected" not in world.kernel.blocks


# rev 5.3 round — "Require order-level evidence to resolve AC-5" (pending row; S1 cut)
def test_aggregate_position_evidence_never_resolves_an_unknown_order():
    """Aggregate position evidence never resolves an unknown order."""
    world = make_world()
    world.broker.inject["place"] = "unknown_executed"
    decision = world.kernel.admit_entry(entry("dj30_mym_p250", 22), world.now)
    ref = decision.ref
    # A position-only read (no working list, no order status) cannot resolve the order.
    world.advance(MIN)
    ev = world.broker.snapshot("MYM")
    stripped = type(ev)(ev.sym, ev.as_of, ev.position, (), {}, {}, {}, order_level=False)
    world.kernel.apply_evidence(stripped)
    assert world.kernel.pending[ref].status == "unknown"              # P alone proves nothing
    assert world.kernel.ledger.reserved["dj30_mym_p250"] == 22
    world.advance(MIN)
    world.snap("MYM")                                                 # order-level: working
    assert world.kernel.pending[ref].status == "accepted"


# rev 5 round — "Wait for cancellation / reconcile an unknown close" (rev 5.1 atomic CLOSE)
def test_unknown_close_is_reconciled_before_resubmission_never_blindly_retried():
    """Unknown close is reconciled before resubmission never blindly retried."""
    world = make_world()
    lot = _lot(world, "aegis_6j", 3, Bracket(stop=0.0069))
    world.broker.inject["close"] = "unknown"
    op = world.kernel.handle_exit("aegis_6j", world.now, fill_id=lot)
    assert op.status == "unknown" and "unknown_order" in world.kernel.blocks
    with pytest.raises(KernelRefusal):
        world.kernel.retry(op.op_id, world.now)
    world.advance(MIN)
    world.snap("6J")                                                  # it had executed
    assert op.status == "complete" and "unknown_order" not in world.kernel.blocks
    assert len([e for e in world.broker.log if e["event"] == "close"]) == 1


def test_route_without_atomic_close_never_receives_a_close_and_blocks_new_exposure():
    """Route without atomic close never receives a close and blocks new exposure."""
    world = make_world()
    lot = _lot(world, "vanguard_mgc", 1, Bracket(stop=2_400.0))
    world.broker.caps["d"] = NOT_SUPPORTED                            # discovered with exposure
    op = world.kernel.handle_exit("vanguard_mgc", world.now, fill_id=lot)
    assert op.status == "refused" and "close_rejected" in world.kernel.blocks
    assert not [e for e in world.broker.log if e["event"] == "close"]
    assert world.kernel.lots[lot].qty == 1                            # protection retained


# rev 4 round — "orphan of unknown kind is never auto-cancelled" (S9)
def test_restart_halts_on_an_orphan_working_order_and_never_cancels_it():
    """Restart halts on an orphan working order and never cancels it."""
    world = make_world()
    _lot(world, "dj30_mym_p250", 22)
    orphan = world.broker.place(sym="MYM", leg_id="dj30_mym_p250", kind="unknown", side="sell",
                                qty=5, order_type="stop", price=41_000.0)
    world.advance(MIN)
    restarted = Kernel.restart(world.kernel.store, world.broker, world.clock, world.now,
                               protection_cases=world.kernel.protection_cases)
    assert restarted.reconcile_restart(world.now).reason == "evidence_owed"
    world.advance(MIN)
    for sym in ("6J", "MYM", "MGC", "MNQ"):
        restarted.apply_evidence(world.broker.snapshot(sym))
    result = restarted.reconcile_restart(world.now)
    assert result.reason == "halted" and "dj30_mym_p250" in restarted.halted_legs
    assert world.broker.orders[orphan.ref].status == "working"        # never auto-cancelled
    assert "restart_unreconciled" in restarted.blocks
    assert restarted.admit_entry(entry("dj30_mym_p250", 1), world.now).reason == "policy_block"


def test_restart_recovers_a_lot_whose_expected_protection_is_missing():
    """Restart recovers a lot whose expected protection is missing."""
    world = make_world()
    lot = _lot(world, "vanguard_mgc", 1, Bracket(stop=2_400.0))
    stop_ref = world.kernel.expected[lot].working["stop"]
    world.broker.orders[stop_ref].status = "cancelled"                # vanished at the broker
    world.advance(MIN)
    restarted = Kernel.restart(world.kernel.store, world.broker, world.clock, world.now,
                               protection_cases=world.kernel.protection_cases)
    world.advance(MIN)
    for sym in ("6J", "MYM", "MGC", "MNQ"):
        restarted.apply_evidence(world.broker.snapshot(sym))
    result = restarted.reconcile_restart(world.now)
    assert result.reason == "protection_gap"
    assert any(o.reason == "protection_gap_recovery" and o.scope_id == lot
               for o in restarted.operations.values())


# rev 4/5 rounds — takeover failure classes refuse Aegis (S10, D-B8)
def _fill_book_except_aegis(world):
    _lot(world, "dj30_mym_p250", 22)
    _lot(world, "vanguard_mgc", 2, Bracket(stop=2_400.0))
    _lot(world, "orb_mnq_v7", 1, Bracket(stop=18_450.0))
    assert world.kernel.ledger.micro_used() == 25


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


# refuse-never-clip at the cap (R-E)
def test_capacity_refuses_and_never_clips_a_lower_priority_leg():
    """Capacity refuses and never clips a lower priority leg."""
    world = make_world()
    _lot(world, "dj30_mym_p250", 22)
    _lot(world, "dj30_mym_p250", 55, kind="add")
    _lot(world, "vanguard_mgc", 2, Bracket(stop=2_400.0))
    assert world.kernel.ledger.micro_used() == 79
    refused = world.kernel.admit_entry(entry("vanguard_mgc", 2, kind="add"), world.now)
    assert refused.reason == "capacity_refused"
    assert world.kernel.ledger.micro_used() == 79                     # nothing was clipped in


# S4 — a stale resting entry is cancelled and its reservation released only on the ack
def test_resting_entry_cancel_releases_reservation_only_on_evidence():
    """Resting entry cancel releases reservation only on evidence."""
    world = make_world()
    decision = world.kernel.admit_entry(
        entry("orb_mnq_v7", 1, Bracket(stop=18_450.0), order_type="stop", price=18_500.0),
        world.now)
    world.advance(BAR + MIN)
    assert world.kernel.cancel(decision.ref, world.now).ok
    assert world.kernel.ledger.reserved["orb_mnq_v7"] == 1            # ack not yet evidenced
    world.advance(MIN)
    world.snap("MNQ")
    assert world.kernel.ledger.reserved["orb_mnq_v7"] == 0


# AMEND — a loosening change is a risk-add and is refused under any block (§1 action classes)
def test_loosening_amend_refused_under_a_block_tightening_admitted():
    """Loosening amend refused under a block tightening admitted."""
    world = make_world()
    lot = _lot(world, "vanguard_mgc", 1, Bracket(stop=2_400.0))
    world.kernel.block("eod", "test")
    world.advance(MIN)
    world.snap("MGC")
    loosen = world.kernel.amend(lot, Bracket(stop=2_390.0), world.now)
    assert loosen.reason == "policy_block"
    tighten = world.kernel.amend(lot, Bracket(stop=2_410.0), world.now)
    assert tighten.ok and world.broker.log[-1]["event"] == "modify"


# ATTACH — a rejected first protection is a gap once the port has defined it (I7)
def test_rejected_attach_becomes_a_protection_gap_with_recovery_close():
    """Rejected attach becomes a protection gap with recovery close."""
    world = make_world()
    lot = _lot(world, "dj30_mym_p250", 22)
    world.broker.inject["attach"] = "reject"
    world.advance(BAR)
    decision = world.kernel.amend(lot, Bracket(stop=41_200.0), world.now)
    assert decision.op.kind == "ATTACH" and decision.op.status == "rejected"
    assert world.kernel.expected[lot].status["stop"] == "missing"     # immediately
    assert "protection_gap" in world.kernel.blocks
    recovery = [o for o in world.kernel.operations.values()
                if o.reason == "protection_gap_recovery"]
    assert recovery and recovery[0].scope_id == lot
    world.advance(MIN)
    world.snap("MYM")
    assert recovery[0].status == "complete" and world.kernel.lots[lot].qty == 0
    assert "protection_gap" not in world.kernel.blocks


# CLOSE — an unknown close that never executed is resubmitted under the same identity
def test_unknown_close_that_did_not_execute_is_resubmitted_with_the_same_identity():
    """Unknown close that did not execute is resubmitted with the same identity."""
    world = make_world()
    lot = _lot(world, "vanguard_mgc", 1, Bracket(stop=2_400.0))
    world.broker.inject["close"] = "unknown_lost"
    op = world.kernel.handle_exit("vanguard_mgc", world.now, fill_id=lot)
    world.advance(MIN)
    world.snap("MGC")
    assert op.status == "unknown" and op.reconciled_at is not None
    world.kernel.retry(op.op_id, world.now)
    assert op.status == "sent" and op.attempts == 2
    assert len(world.kernel.operations) == 1                          # same durable operation
    world.advance(MIN)
    world.snap("MGC")
    assert op.status == "complete"
