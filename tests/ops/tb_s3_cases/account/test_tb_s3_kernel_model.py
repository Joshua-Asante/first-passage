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


from tests.ops.tb_s3_kernel.account_harness import BAR, MIN, entry, fill_lot, make_world


from tests.ops.tb_s3_kernel.account import AccountKernel as Kernel
from tests.ops.tb_s3_kernel.kernel import KernelRefusal


_fill_entry = fill_lot


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


def test_ac7_daemon_loss_timer_survives_listener_restart_and_absent_timestamp_is_expired():
    """Ac7 daemon loss timer survives listener restart and absent timestamp is expired."""
    world = make_world()
    lot = _fill_entry(world, "dj30_mym_p250", 22)
    t_read = world.now
    world.daemon.control_read(t_read)                                # 10:00-equivalent
    world.advance(20 * MIN)
    restarted = type(world.kernel).restart(world.kernel.store, world.broker, world.clock, world.now,
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
    bare = type(world.kernel).restart(world.kernel.store, world.broker, world.clock, world.now)
    bare.last_control_read = None                                    # never persisted
    world.broker.positions["6J"] = -3                              # external exposure
    world.advance(MIN)
    bare.apply_evidence(world.broker.snapshot("6J"))
    assert bare.daemon_loss_check(world.now)                          # absent = expired


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
