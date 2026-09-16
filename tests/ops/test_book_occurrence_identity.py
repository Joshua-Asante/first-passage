import sqlite3
import pytest
from c1_rail.book_account_owner import AccountOwnerError, BookAccountOwner, BrokerResult
from c1_signal_daemon.book_protocol import Cancel
from test_book_account_owner import NOW, binding, intent, owner


def test_valid_action_requires_explicit_occurrence(tmp_path):
    account, route = owner(tmp_path, [BrokerResult('accepted')])
    result = account.dispatch(intent(), now=NOW)
    assert result.refusal_reason == 'source_occurrence_required'
    assert route.commands == []


def test_legacy_schema_refusal_preserves_file(tmp_path):
    account, route = owner(tmp_path, [])
    with sqlite3.connect(account.path) as db:
        db.execute('UPDATE owner_state SET schema=1')
    before = account.path.read_bytes()
    with pytest.raises(AccountOwnerError, match='legacy'):
        BookAccountOwner.boot(account.path, account.account, binding=binding(), synthetic_broker=route)
    assert account.path.read_bytes() == before


def test_occurrence_retains_refusal_and_detects_source_conflict(tmp_path):
    account, route = owner(tmp_path, [BrokerResult('accepted')])
    occurrence = account.make_occurrence('direct', 'event-1')
    first = account.dispatch(Cancel('dj30_mym_p250', 'base'), occurrence=occurrence, now=NOW)
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    again = account.dispatch(Cancel('dj30_mym_p250', 'base'), occurrence=occurrence, now=NOW)
    assert again == first
    assert len(route.commands) == 1
    conflict = account.dispatch(Cancel('dj30_mym_p250', 'different'), occurrence=occurrence, now=NOW)
    assert conflict.refusal_reason == 'occurrence_conflict'
    assert account.authority == 'INTERVENTION'


def test_distinct_events_do_not_share_control_identity(tmp_path):
    account, _ = owner(tmp_path, [])
    action = Cancel('dj30_mym_p250', 'missing')
    first = account.dispatch(action, occurrence=account.make_occurrence('direct', 'first'), now=NOW)
    second = account.dispatch(action, occurrence=account.make_occurrence('direct', 'second'), now=NOW)
    assert first.operation_id != second.operation_id


def test_same_occurrence_replays_original_transport_result(tmp_path):
    account, route = owner(tmp_path, [BrokerResult('accepted')])
    event = account.make_occurrence('direct', 'accepted-entry')
    first = account.dispatch(intent(), occurrence=event, now=NOW)
    second = account.dispatch(intent(), occurrence=event, now=NOW)
    assert second == first
    assert len(route.commands) == 1
    assert route.commands[0].occurrence == event


def test_new_occurrence_cannot_reuse_intent_operation(tmp_path):
    account, route = owner(tmp_path, [BrokerResult('accepted')])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'first'), now=NOW)
    second = account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'second'), now=NOW)
    assert second.refusal_reason == 'duplicate_operation'
    assert len(route.commands) == 1


def test_cancel_all_empty_scope_is_retained(tmp_path):
    account, route = owner(tmp_path, [BrokerResult('accepted')])
    event = account.make_occurrence('direct', 'cancel-empty')
    first = account.dispatch(Cancel('dj30_mym_p250', None), occurrence=event, now=NOW)
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry-later'), now=NOW)
    assert account.dispatch(Cancel('dj30_mym_p250', None), occurrence=event, now=NOW) == first
    assert len(route.commands) == 1


def test_missing_schema_two_table_refuses_without_writes(tmp_path):
    account, route = owner(tmp_path, [])
    with sqlite3.connect(account.path) as db:
        db.execute('DROP TABLE action_occurrences')
    before = account.path.read_bytes()
    with pytest.raises(AccountOwnerError, match='schema'):
        BookAccountOwner.boot(account.path, account.account, binding=binding(), synthetic_broker=route)
    assert account.path.read_bytes() == before


def test_retained_legacy_attempt_is_not_migrated(tmp_path):
    account, route = owner(tmp_path, [BrokerResult('accepted')])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    with sqlite3.connect(account.path) as db:
        db.execute('UPDATE owner_state SET schema=1')
        db.execute('DROP TABLE feed_watch')
    before = account.path.read_bytes()
    with pytest.raises(AccountOwnerError, match='legacy'):
        BookAccountOwner.boot(account.path, account.account, binding=binding(), synthetic_broker=route)
    assert account.path.read_bytes() == before
    assert len(route.commands) == 1


def test_restart_preserves_completed_occurrence_and_never_sends(tmp_path):
    account, route = owner(tmp_path, [BrokerResult('accepted')])
    event = account.make_occurrence('direct', 'before-restart')
    first = account.dispatch(intent(), occurrence=event, now=NOW)
    restarted = BookAccountOwner.boot(account.path, account.account, binding=binding(), synthetic_broker=route)
    assert restarted.dispatch(intent(), occurrence=event, now=NOW) == first
    assert restarted.permission == 'HALTED'
    assert len(route.commands) == 1


@pytest.mark.parametrize('cut', ['after_reservation', 'before_send', 'after_send'])
def test_crash_occurrence_never_recreates_attempt(tmp_path, cut):
    from c1_rail.book_account_owner import SimulatedOwnerCrash
    account, route = owner(tmp_path, [BrokerResult('accepted')])
    account.crash_at = cut
    event = account.make_occurrence('direct', 'crash')
    with pytest.raises(SimulatedOwnerCrash):
        account.dispatch(intent(), occurrence=event, now=NOW)
    count = len(route.commands)
    restarted = BookAccountOwner.boot(account.path, account.account, binding=binding(), synthetic_broker=route)
    result = restarted.dispatch(intent(), occurrence=event, now=NOW)
    assert result.refusal_reason == 'retained_preparation'
    assert len(route.commands) == count


def test_conflicting_occurrence_storage_failure_latches_suppression(tmp_path):
    account, route = owner(tmp_path, [])
    event = account.make_occurrence('direct', 'conflict')
    account.dispatch(Cancel('dj30_mym_p250', 'one'), occurrence=event, now=NOW)
    with sqlite3.connect(account.path) as db:
        db.execute("CREATE TRIGGER fail_fence BEFORE UPDATE ON owner_state BEGIN SELECT RAISE(ABORT, 'storage failure'); END")
    with pytest.raises(AccountOwnerError, match='state unavailable'):
        account.dispatch(Cancel('dj30_mym_p250', 'two'), occurrence=event, now=NOW)
    with sqlite3.connect(account.path) as db:
        db.execute('DROP TRIGGER fail_fence')
    assert account.incidents == ()
    with pytest.raises(AccountOwnerError, match='local send suppression'):
        account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'later'), now=NOW)
    assert route.commands == []


def test_executable_entry_checks_pending_protection_deadline(tmp_path):
    from book_occurrence_fixtures import bare_protection_owner, prepare_protection
    from c1_signal_daemon.book_protocol import Bracket, BracketAmend
    from datetime import timedelta
    account, route = bare_protection_owner(tmp_path)
    route.queue(BrokerResult('accepted'))
    prepare_protection(account, route, BracketAmend('dj30_mym_p250', Bracket(stop=98), ('base-fill',)), 'pending')
    count = len(route.commands)
    account.dispatch(intent('after-deadline'), occurrence=account.make_occurrence('direct', 'after-deadline'), now=NOW+timedelta(minutes=16))
    assert account.authority == 'INTERVENTION'
    assert len(route.commands) == count


def test_attempted_read_continuation_never_retries_after_crash(tmp_path):
    from book_occurrence_fixtures import bare_protection_owner
    from c1_signal_daemon.book_protocol import Bracket, BracketAmend
    from c1_rail.book_account_owner import SimulatedOwnerCrash
    from datetime import timedelta
    account, route = bare_protection_owner(tmp_path)
    route.queue(BrokerResult('accepted'))
    event = account.make_occurrence('direct', 'pending')
    action = BracketAmend('dj30_mym_p250', Bracket(stop=98), ('base-fill',))
    assert account.dispatch(action, occurrence=event, now=NOW).refusal_reason == 'awaiting_evidence'
    later = NOW+timedelta(seconds=1)
    route.advance(later)
    account.crash_at = 'after_send'
    with pytest.raises(SimulatedOwnerCrash):
        account.dispatch(action, occurrence=event, now=later)
    count = len(route.commands)
    account.crash_at = None
    result = account.dispatch(action, occurrence=event, now=later)
    assert result.refusal_reason == 'retained_attempt'
    assert account.occurrence_state(event)['attempted'] is True
    assert len(route.commands) == count
