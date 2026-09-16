"""Crash cuts and late observations retain obligations without send authority."""
from dataclasses import replace
from datetime import timedelta

import pytest

from c1_rail.book_account_owner import BookAccountOwner, BrokerResult, SimulatedOwnerCrash
from c1_rail.book_protection import ProtectionRead
from c1_signal_daemon.book_protocol import Bracket, BracketAmend
from book_protection_fixtures import ProtectionScenario
from test_book_account_owner import binding


@pytest.mark.parametrize('cut', ['after_reservation', 'before_send', 'after_send'])
def test_protection_crash_restart_preserves_owner_and_never_sends(tmp_path, cut):
    s = ProtectionScenario(tmp_path)
    s.enter()
    occurrence = s.occurrence('crash-change')
    action = BracketAmend('dj30_mym_p250', Bracket(stop=98), ('base',))
    assert s.dispatch(action, occurrence).refusal_reason == 'awaiting_evidence'
    s.advance()
    s.broker.queue(BrokerResult('accepted'))
    s.owner.crash_at = cut
    with pytest.raises(SimulatedOwnerCrash):
        s.dispatch(action, occurrence)
    before = s.owner.protection_owners
    count = len(s.broker.commands)
    restarted = BookAccountOwner.boot(s.owner.path, s.owner.account,
                                     binding=binding(), synthetic_broker=s.broker)
    assert restarted.protection_owners == before
    restarted.dispatch(action, occurrence=occurrence, now=s.now)
    assert len(s.broker.commands) == count
    assert restarted.authority == 'INTERVENTION'


def test_late_application_is_observed_without_clearing_deadline_intervention(tmp_path):
    s = ProtectionScenario(tmp_path)
    s.enter()
    result = s.prepare(BracketAmend('dj30_mym_p250', Bracket(stop=98), ('base',)), s.occurrence('late'))
    deadline = s.protection('base').deadline
    command = s.protection_commands[-1]
    s.now = deadline
    s.broker.apply(command.operation_id, outcome='applied', at=s.now)
    snapshot = s.broker.read_protection(ProtectionRead(command.occurrence, ('dj30_mym_p250',),
                                                     deadline - timedelta(minutes=15)))
    s.owner.observe_protection(snapshot, now=s.now)
    assert s.protection('base').observed == Bracket(stop=98)
    assert s.owner.authority == 'INTERVENTION'
    assert s.owner.incidents
    count = len(s.broker.commands)
    s.dispatch(BracketAmend('dj30_mym_p250', Bracket(stop=99), ('base',)), s.occurrence('after-late'))
    assert len(s.broker.commands) == count


def test_empty_bare_demand_has_no_expected_protection_deadline(tmp_path):
    s = ProtectionScenario(tmp_path)
    s.enter()
    result = s.prepare(BracketAmend('dj30_mym_p250', Bracket(), ('base',)),
                       s.occurrence('empty'), command_count=0)
    assert result.refusal_reason == 'unchanged_protection'
    assert s.protection('base').deadline is None
    s.owner.check_protection_deadlines(now=s.now + timedelta(minutes=16))
    assert s.owner.authority == 'NORMAL'


def test_boolean_execution_allocation_cannot_masquerade_as_one_contract(tmp_path):
    s = ProtectionScenario(tmp_path)
    s.enter(bracket=Bracket(stop=98))
    event = s.broker.execute_protection('protection:base', quantity=1, price=98,
                                       terminal=False, at=s.advance())
    malformed = replace(event, allocations=(('base', True),))
    before = s.owner.all_feedback
    assert s.owner.observe_protection_execution(malformed, now=s.now) == ()
    assert s.owner.exposure('dj30_mym_p250') == (3, 0)
    assert s.owner.all_feedback == before
    assert s.owner.authority == 'INTERVENTION'


def test_execution_does_not_erase_separate_pending_mutation_obligation(tmp_path):
    s = ProtectionScenario(tmp_path)
    s.enter(bracket=Bracket(stop=98))
    s.prepare(BracketAmend('dj30_mym_p250', Bracket(stop=99), ('base',)), s.occurrence('pending'))
    before = s.protection('base')
    event = s.broker.execute_protection('protection:base', quantity=3, price=98,
                                       terminal=True, at=s.advance())
    assert len(s.owner.observe_protection_execution(event, now=s.now)) == 1
    after = s.protection('base')
    assert after.consumed
    assert after.pending_operation == before.pending_operation
    assert after.deadline == before.deadline
    s.owner.check_protection_deadlines(now=after.deadline)
    assert s.owner.authority == 'INTERVENTION'


def test_restart_after_broker_application_observes_without_send_authority(tmp_path):
    s = ProtectionScenario(tmp_path)
    s.enter()
    s.prepare(BracketAmend('dj30_mym_p250', Bracket(stop=98), ('base',)), s.occurrence('apply-cut'))
    command = s.protection_commands[-1]
    s.broker.apply(command.operation_id, outcome='applied', at=s.advance())
    snapshot = s.broker.read_protection(ProtectionRead(command.occurrence, ('dj30_mym_p250',),
                                                     s.now - timedelta(seconds=1)))
    restarted = BookAccountOwner.boot(s.owner.path, s.owner.account,
                                     binding=binding(), synthetic_broker=s.broker)
    count = len(s.broker.commands)
    restarted.observe_protection(snapshot, now=s.now)
    assert restarted.protection_owners[0].observed == Bracket(stop=98)
    assert restarted.protection_owners[0].pending_operation is None
    assert restarted.authority == 'INTERVENTION'
    assert len(s.broker.commands) == count


def test_execution_commit_before_feedback_survives_restart_once(tmp_path):
    s = ProtectionScenario(tmp_path)
    s.enter(bracket=Bracket(stop=98))
    event = s.broker.execute_protection('protection:base', quantity=3, price=98,
                                       terminal=True, at=s.advance())
    feedback = s.owner.observe_protection_execution(event, now=s.now)
    assert len(feedback) == 1
    undelivered = s.owner.pending_feedback
    restarted = BookAccountOwner.boot(s.owner.path, s.owner.account,
                                     binding=binding(), synthetic_broker=s.broker)
    assert restarted.pending_feedback == undelivered
    assert restarted.protection_owners[0].consumed
    assert restarted.observe_protection_execution(event, now=s.now) == ()
    assert restarted.pending_feedback == undelivered
    assert restarted.exposure('dj30_mym_p250') == (0, 0)


def test_concurrent_read_and_continuation_cannot_send_after_serialized_halt(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event
    s = ProtectionScenario(tmp_path)
    s.enter(bracket=Bracket(stop=98))
    action = BracketAmend('dj30_mym_p250', Bracket(stop=99), ('base',))
    occurrence = s.occurrence('racing-change')
    assert s.dispatch(action, occurrence).refusal_reason == 'awaiting_evidence'
    s.advance()
    snapshot = s.broker.read_protection(ProtectionRead(occurrence, ('dj30_mym_p250',),
                                                     s.now - timedelta(milliseconds=100)))
    locked, release, reader_started, dispatch_started = (Event() for _ in range(4))
    original_halt = s.owner._halt_db
    def paused_halt(*args):
        locked.set()
        assert release.wait(5)
        return original_halt(*args)
    monkeypatch.setattr(s.owner, '_halt_db', paused_halt)
    def observe():
        reader_started.set()
        s.owner.observe_protection(snapshot, now=s.now)
    def dispatch():
        dispatch_started.set()
        return s.dispatch(action, occurrence)
    count = len(s.broker.commands)
    with ThreadPoolExecutor(max_workers=3) as pool:
        halt = pool.submit(s.owner.halt, 'race-fence', 'operator', now=s.now)
        assert locked.wait(5)
        reader = pool.submit(observe)
        mutation = pool.submit(dispatch)
        try:
            assert reader_started.wait(5) and dispatch_started.wait(5)
        finally:
            release.set()
        halt.result(timeout=5)
        reader.result(timeout=5)
        # Halt changes generation: redelivery returns its retained disposition,
        # rather than continuing the earlier generation's preparation.
        assert mutation.result(timeout=5).refusal_reason == 'awaiting_evidence'
    assert s.owner.authority == 'INTERVENTION'
    assert len(s.broker.commands) == count
    assert s.dispatch(action, s.occurrence('post-fence')).refusal_reason == 'intervention_fence'
    assert len(s.broker.commands) == count
