"""Rev7 account integration: literal event-sequence outcomes."""
from book_protocol import Bracket
from tests.ops.tb_s3_kernel.account_harness import make_world, fill_lot, MIN


def test_crossed_add_owner_allocates_fifo_and_retains_base_protection():
    w = make_world()
    base = fill_lot(w, 'dj30_mym_p250', 2)
    w.kernel.amend(base, Bracket(stop=90), w.now)
    w.advance(MIN)
    w.snap()
    add = fill_lot(w, 'dj30_mym_p250', 2, kind='add')
    assert w.daemon.reissue('dj30_mym_p250', add, Bracket(stop=95), 94, w.now) == 'close_time_exit'
    w.advance(MIN)
    w.snap()
    assert w.broker.lots[base].qty == 0
    assert w.broker.lots[add].qty == 2
    assert w.broker.lots[base].protection_qty == 2
    assert w.broker.lots[add].protection_consumed
    assert w.broker.reductions[-1].transition == 'triggered_protection'
    assert all(o.status == 'complete' for o in w.kernel.operations.values())


def test_expired_flat_source_owns_latch_and_episode_across_rollover():
    from tests.ops.tb_s3_kernel.broker import STALENESS_WINDOW
    w = make_world()
    w.advance(STALENESS_WINDOW + MIN)
    w.snap()
    op_id = w.daemon.feed_loss_check('vanguard_mgc', w.now)
    assert op_id and 'feed' in w.kernel.blocks
    w.advance(MIN)
    w.snap()
    w.kernel.session_open()
    assert 'feed' in w.kernel.blocks


def test_expired_flat_daemon_owns_every_scope_before_new_evidence():
    from tests.ops.tb_s3_kernel.broker import STALENESS_WINDOW
    w = make_world()
    w.advance(STALENESS_WINDOW + MIN)
    w.snap()
    ops = w.kernel.daemon_loss_check(w.now)
    assert len(ops) == 4 and 'feed' in w.kernel.blocks
    assert not w.kernel.flatten_complete('daemon_loss_flat', w.now)


def test_kill_does_not_ignore_observed_foreign_position():
    w = make_world()
    w.broker.place(sym='X', leg_id='outside', kind='entry', side='buy', qty=1, ref='outside')
    w.broker.fill('outside')
    w.advance(MIN)
    w.snap('X')
    w.kernel.kill(w.now)
    w.advance(MIN)
    w.snap()
    assert not w.kernel.kill_status(True, w.now)['complete']
    assert not w.kernel.dry_run


def test_kill_status_cannot_invent_daemon_acknowledgment():
    w = make_world()
    w.kernel.kill(w.now)
    assert w.kernel.kill_status(True, w.now)['daemon_control'] == 'not_reached'


def test_restart_does_not_acknowledge_a_disarm_that_never_executed():
    import pytest
    from tests.ops.tb_s3_kernel.account_harness import Sequence
    w = make_world()
    w.kernel.kill(w.now)
    def crash(stage, effect):
        if effect.kind == 'disarm' and stage == 'dispatching':
            raise RuntimeError('power loss')
    w.kernel.effect_hook = crash
    w.advance(MIN)
    with pytest.raises(RuntimeError, match='power loss'):
        w.snap()
    Sequence.start(w).restart()
    assert not w.kernel.dry_run
    assert not w.kernel.kill_status(False, w.now)['complete']


def test_source_episode_survives_daemon_restart_and_old_open_replay():
    from tests.ops.tb_s3_kernel.broker import STALENESS_WINDOW
    from tests.ops.tb_s3_kernel.daemon import Daemon
    from tests.ops.tb_s3_kernel.account_harness import Sequence
    w = make_world()
    w.advance(STALENESS_WINDOW + MIN)
    episode = w.daemon.feed_loss_check('vanguard_mgc', w.now)
    opened = dict(w.kernel.source_reports['vanguard_mgc'])
    w.daemon = Daemon(w.kernel, w.clock, store=w.daemon.store)
    assert w.daemon.feed_loss_check('vanguard_mgc', w.now) == episode
    w.daemon.on_bar('MGC', w.now)
    Sequence.start(w).restart()
    assert w.kernel.source_report(opened)
    assert not w.kernel.feed_episodes[episode]['active']
    assert len([o for o in w.kernel.operations.values() if o.reason == 'feed_loss_flat']) == 1


def test_unknown_config_write_is_pending_until_readback_or_idempotent_retry():
    from tests.ops.tb_s3_kernel.account_harness import Sequence
    for mode in ('reject', 'unknown_lost', 'unknown'):
        w = make_world()
        w.broker.control_owner.inject = mode
        w.kernel.kill(w.now)
        w.advance(MIN)
        w.snap()
        assert not w.kernel.kill_status(False, w.now)['complete']
        Sequence.start(w).restart()
        w.advance(MIN)
        w.snap()
        w.kernel.progress(w.now)
        assert w.kernel.kill_status(False, w.now)['complete']
        assert w.broker.control_owner.armed_until is None
        assert len(w.broker.control_owner.applied) == 1


def test_explicit_daemon_ack_is_verified_and_survives_listener_restart():
    from tests.ops.tb_s3_kernel.account_harness import Sequence
    w = make_world()
    w.kernel.kill(w.now)
    kill_id = w.kernel.account_runs['kill']['id']
    assert not w.kernel.acknowledge_daemon_control(kill_id, 'command', w.now)
    w.broker.control_owner.daemon_heartbeats['command'] = {'emit_enabled': False, 'at': w.now}
    assert w.kernel.acknowledge_daemon_control(kill_id, 'command', w.now)
    Sequence.start(w).restart()
    assert w.kernel.kill_status(False, w.now)['daemon_control'] == 'acknowledged'


def test_new_session_eod_gets_new_work_and_old_run_does_not_expand():
    w = make_world()
    first = w.kernel.eod(w.now)
    w.advance(MIN)
    w.snap()
    w.kernel.session_open()
    lot = fill_lot(w, 'vanguard_mgc', 1)
    assert w.broker.lots[lot].qty == 1
    second = w.kernel.eod(w.now)
    assert {o.op_id for o in first}.isdisjoint(o.op_id for o in second)
    assert w.broker.lots[lot].qty == 0


def test_retired_eod_cannot_close_a_newly_observed_location():
    w = make_world()
    w.kernel.eod(w.now)
    w.advance(MIN)
    w.snap()
    w.kernel.session_open()
    w.broker.place(sym='X', leg_id='outside', kind='entry', side='buy', qty=1, ref='new')
    w.broker.fill('new')
    w.snap('X')
    assert w.broker.positions['X'] == 1


def test_unacknowledged_source_report_blocks_daemon_risk_adds():
    from tests.ops.tb_s3_kernel.broker import STALENESS_WINDOW
    w = make_world()
    w.advance(STALENESS_WINDOW + MIN)
    w.kernel.source_report = lambda report: False
    w.daemon.feed_loss_check('vanguard_mgc', w.now)
    w.daemon.control_read(w.now)
    assert not w.daemon.emit_risk_add(w.now)


def test_reissue_cannot_borrow_another_legs_orders_on_close_policy():
    w = make_world()
    lot = fill_lot(w, 'vanguard_mgc', 1, Bracket(stop=90))
    before = len(w.broker.reductions)
    assert w.daemon.reissue('dj30_mym_p250', lot, Bracket(stop=95), 94, w.now) == 'invalid_owner'
    assert len(w.broker.reductions) == before


def test_crossed_branch_refuses_incomplete_trailing_shape():
    w = make_world()
    lot = fill_lot(w, 'dj30_mym_p250', 1)
    assert w.daemon.reissue('dj30_mym_p250', lot, Bracket(stop=95, trail_offset_ticks=2),
                           94, w.now) == 'invalid_bracket'
    assert w.broker.lots[lot].qty == 1


def test_reordered_source_reports_keep_gap_owned_until_contiguous():
    from tests.ops.tb_s3_kernel.broker import STALENESS_WINDOW
    w = make_world()
    w.advance(STALENESS_WINDOW + MIN)
    at = w.now
    source = at - STALENESS_WINDOW - MIN
    first = dict(kind='open', leg_id='vanguard_mgc', episode='episode', seq=1, at=at, source_at=source)
    second = dict(first, kind='recovery', seq=2, source_at=at)
    w.advance(STALENESS_WINDOW + MIN)
    third = dict(first, kind='open', seq=3, episode='episode-next', at=w.now, source_at=at)
    assert not w.kernel.source_report(third)
    assert w.kernel.source_report(first)
    assert 'report-gap:vanguard_mgc' in w.kernel.blocks['unknown_order']
    assert w.kernel.source_report(second)
    assert w.kernel.source_report(third)
    assert 'report-gap:vanguard_mgc' not in w.kernel.blocks.get('unknown_order', ())
    assert not w.kernel.source_report(dict(first, episode='rewritten'))
    w.kernel.session_open()
    assert 'report-conflict:vanguard_mgc:1' in w.kernel.blocks['unknown_order']


def test_planned_disarm_waits_for_post_restart_account_evidence():
    import pytest
    from tests.ops.tb_s3_kernel.account_harness import Sequence
    w = make_world()
    w.kernel.kill(w.now)
    def crash(stage, effect):
        if effect.kind == 'disarm' and stage == 'planned':
            raise RuntimeError('power loss')
    w.kernel.effect_hook = crash
    w.advance(MIN)
    with pytest.raises(RuntimeError, match='power loss'):
        w.snap()
    Sequence.start(w).restart()
    w.kernel.progress(w.now)
    assert not w.kernel.dry_run


def test_stale_recovery_bar_does_not_lose_the_durable_outage():
    from tests.ops.tb_s3_kernel.broker import STALENESS_WINDOW
    w = make_world()
    old = w.now
    w.advance(STALENESS_WINDOW + MIN)
    episode = w.daemon.feed_loss_check('vanguard_mgc', w.now)
    opened = w.kernel.source_reports['vanguard_mgc']
    assert not w.kernel.source_report(dict(opened, kind='recovery', seq=2))
    w.daemon.on_bar('MGC', old + MIN)
    assert w.daemon.feed_loss_ops['vanguard_mgc'] == episode
    w.daemon.on_bar('MGC', w.now)
    assert not w.kernel.feed_episodes[episode]['active']
    assert not w.daemon.reports


def test_unfinished_eod_retains_future_locations_after_rollover():
    w = make_world()
    w.broker.inject['place'] = 'defer'
    w.broker.request('place', 'external-pending', sym='X', leg_id='outside', kind='entry',
                     side='buy', qty=1, ref='late')
    w.snap()
    w.kernel.eod(w.now)
    w.advance(MIN)
    w.snap()
    w.kernel.session_open()
    w.broker.execute_next()
    w.broker.fill('late')
    w.advance(MIN)
    w.snap('X')
    w.snap()
    assert any(o.sym == 'X' and o.reason == 'eod_flatten' for o in w.kernel.operations.values())
    assert w.broker.positions['X'] == 0


def test_continuing_healthy_bars_do_not_age_the_old_recovery_report():
    from tests.ops.tb_s3_kernel.broker import STALENESS_WINDOW
    w = make_world()
    w.advance(STALENESS_WINDOW + MIN)
    w.daemon.feed_loss_check('vanguard_mgc', w.now)
    w.daemon.on_bar('MGC', w.now)
    w.advance(MIN)
    w.snap()
    w.kernel.session_open()
    for _ in range(7):
        w.advance(5 * MIN)
        w.daemon.on_bar('MGC', w.now)
        w.daemon.control_read(w.now)
        w.snap()
        w.kernel.progress(w.now)
    assert not w.daemon.source_unhealthy('MGC', w.now)
    assert 'feed' not in w.kernel.blocks
