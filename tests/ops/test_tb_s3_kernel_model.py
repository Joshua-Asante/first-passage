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


# ── AC-1: Striker bare entry, first protection through ATTACH (L2(f)) ─────────────────────
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


# ── AC-2: close-time crossed level on an orders_on_close leg → market exit at the signal ─
def test_ac2_close_time_crossed_stop_becomes_market_exit():
    """Ac2 close time crossed stop becomes market exit."""
    world = make_world()
    lot = _fill_entry(world, "dj30_mym_p250", 22)
    world.advance(BAR)
    world.kernel.amend(lot, Bracket(stop=41_200.0), world.now)
    world.advance(MIN)
    world.snap("MYM")
    world.advance(BAR)
    result = world.daemon.reissue("dj30_mym_p250", lot, {"stop": 41_250.0}, bar_close=41_240.0,
                                  now=world.now)
    assert result == "close_time_exit"
    op = [o for o in world.kernel.operations.values() if o.reason == "exit"][-1]
    assert op.status == "sent" and world.broker.positions["MYM"] == 0
    world.advance(MIN)
    world.snap("MYM")
    assert op.status == "complete" and world.kernel.lots[lot].qty == 0
    assert not world.kernel.w_ev["MYM"][0]                          # protection went with the lot


# ── AC-3: ORB resting stop entry with a trailing bracket; mode change cancels the add ────
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


# ── AC-4: Vanguard add, partial fill; protection adjusted to the residual (L2(e)) ────────
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


# ── AC-5: entry with an unknown outcome; order-level evidence only resolves it ───────────
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


# ── AC-6: feed loss with the daemon up → one flat per episode, idempotent redelivery ─────
def test_ac6_feed_loss_flat_once_per_episode_and_session_scoped_feed_block():
    """Ac6 feed loss flat once per episode and session scoped feed block."""
    world = make_world()
    lot = _fill_entry(world, "vanguard_mgc", 2, Bracket(stop=2_400.0))
    for sym in ("6J", "MYM", "MNQ"):
        world.daemon.on_bar(sym, world.now)                             # only MGC goes stale
    world.advance(STALENESS_WINDOW + MIN)
    op_id = world.daemon.feed_loss_check("vanguard_mgc", world.now)
    assert op_id and op_id.startswith("feedloss:vanguard_mgc:")
    op = world.kernel.operations[op_id]
    assert op.status == "sent" and "feed" in world.kernel.blocks
    assert world.daemon.feed_loss_check("vanguard_mgc", world.now) == op_id   # redelivery
    assert len([e for e in world.broker.log if e["event"] == "close"]) == 1  # one close only
    world.advance(MIN)
    world.snap("MGC")
    assert op.status == "complete" and world.kernel.lots[lot].qty == 0
    world.kernel.session_open()
    assert "feed" not in world.kernel.blocks


# ── AC-7: daemon down before it can emit; the listener's persisted timer is not reset ────
def test_ac7_daemon_loss_timer_survives_listener_restart_and_absent_timestamp_is_expired():
    """Ac7 daemon loss timer survives listener restart and absent timestamp is expired."""
    world = make_world()
    lot = _fill_entry(world, "dj30_mym_p250", 22)
    t_read = world.now
    world.daemon.control_read(t_read)                                # 10:00-equivalent
    world.advance(20 * MIN)
    restarted = Kernel.restart(world.kernel.store, world.broker, world.clock, world.now,
                               protection_cases=world.kernel.protection_cases)
    assert restarted.last_control_read == t_read                    # restored, not reset
    assert restarted.daemon_loss_check(world.now) == []              # 20 min < window
    world.advance(STALENESS_WINDOW - 20 * MIN + MIN)
    ops = restarted.daemon_loss_check(world.now)
    # Every symbol not CONFIRMED(0) is closed — after 20 minutes without reads the other
    # three are UNKNOWN, and a quantity-less close on a flat symbol is harmless (spec S6).
    assert {o.sym for o in ops} == {"6J", "MYM", "MGC", "MNQ"}
    assert all(o.reason == "daemon_loss_flat" for o in ops)
    assert "feed" in restarted.blocks
    world.advance(MIN)
    for sym in ("6J", "MYM", "MGC", "MNQ"):
        restarted.apply_evidence(world.broker.snapshot(sym))
    assert all(o.status == "complete" for o in ops) and restarted.lots[lot].qty == 0
    bare = Kernel.restart(world.kernel.store, world.broker, world.clock, world.now)
    bare.last_control_read = None                                    # never persisted
    bare.p_ev["6J"] = (3, world.now)                                 # some exposure
    assert bare.daemon_loss_check(world.now)                          # absent = expired


# ── AC-8: a fresh pre-buffer snapshot cannot complete an EOD close ───────────────────────
def test_ac8_eod_close_prepared_at_buffer_needs_postdating_evidence():
    """Ac8 eod close prepared at buffer needs postdating evidence."""
    world = make_world(start=datetime(2026, 9, 14, 16, 20))
    decision = world.kernel.admit_entry(
        entry("orb_mnq_v7", 1, Bracket(stop=18_450.0), order_type="stop", price=18_500.0),
        world.now)
    world.advance(5 * MIN)
    world.snap()                                                     # 16:25: flat, entry resting
    world.advance(2 * MIN)
    world.broker.trigger(decision.ref)                               # 16:27: the entry fills
    world.advance(3 * MIN)
    ops = world.kernel.eod(world.now)                                # 16:30
    assert len(ops) == 4 and all(o.prepared_at == world.now for o in ops)
    mnq = next(o for o in ops if o.sym == "MNQ")
    assert mnq.status == "sent"                                      # not skipped on 16:25 data
    assert world.kernel.events("close_noop") == []
    assert not world.kernel.flatten_complete("eod_flatten", world.now)
    world.advance(MIN)
    world.snap()                                                     # 16:31: postdating reads
    assert mnq.status == "complete"
    assert world.kernel.flatten_complete("eod_flatten", world.now)


# ── AC-9: an amend on a stale working-order view is deferred, never guessed ──────────────
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


# ── AC-10: kill with the daemon down completes on the listener alone ────────────────────
def test_ac10_kill_with_daemon_down_completes_and_flags_not_reached():
    """Ac10 kill with daemon down completes and flags not reached."""
    world = make_world()
    lot = _fill_entry(world, "aegis_6j", 3, Bracket(stop=0.0069))
    ops = world.kernel.kill(world.now)
    assert list(world.kernel.blocks)[0] == "kill"                    # the block came first
    assert any(o.sym == "6J" and o.status == "sent" for o in ops)
    world.advance(MIN)
    world.snap()
    status = world.kernel.kill_status(daemon_reachable=False, now=world.now)
    assert status == {"complete": True, "disarmed": True, "daemon_control": "not_reached"}
    assert world.kernel.lots[lot].qty == 0 and world.kernel.dry_run
    assert "kill" in world.kernel.blocks                             # only the operator clears it


# ── L-2 gating (R-B3): every item a port uses must be supported ─────────────────────────
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
