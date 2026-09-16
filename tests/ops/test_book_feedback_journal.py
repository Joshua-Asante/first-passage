"""Accepted facts, held feedback, and emitted events have distinct journals."""
from datetime import timedelta
import sqlite3

import pytest

from c1_rail.book_account_owner import AccountOwnerError, BookAccountOwner, BrokerFact, BrokerResult
from c1_rail.book_migration import migrate_book_owner, validate_records
from c1_signal_daemon.book_protocol import Bracket
from book_protection_fixtures import ProtectionScenario
from test_book_account_owner import NOW, intent, owner
from test_book_bootstrap_migration import restore_fixture, normal_binding
from test_book_close_reconciliation import close


@pytest.mark.parametrize('version', [1, 2, 3])
@pytest.mark.parametrize('legacy_json_null', [False, True])
def test_eventless_terminal_preserves_converted_account_idempotence(tmp_path, version, legacy_json_null):
    path = tmp_path / 'owner.sqlite'
    restore_fixture(path, f'{version}-filled.json')
    original = migrate_book_owner(path, 'synthetic-account', now=NOW)
    account = BookAccountOwner.boot(path, 'synthetic-account', binding=normal_binding())
    at = NOW + timedelta(seconds=1)
    account.observe(BrokerFact.fill('late-fill', 'entry:vanguard_mgc', 'vanguard_mgc',
                                   'entry', 1, 100, at), now=at)
    before = account.all_feedback
    terminal = BrokerFact.terminal('entry:vanguard_mgc', 'filled', 2, at)
    assert account.observe(terminal, now=at) == ()
    assert account.all_feedback == before
    with sqlite3.connect(path) as db:
        assert db.execute('SELECT feedback FROM broker_facts WHERE fact_id=?',
                          (terminal.fact_id,)).fetchone() == (None,)
        if legacy_json_null:
            db.execute("UPDATE broker_facts SET feedback='null' WHERE fact_id=?", (terminal.fact_id,))
    untouched = path.read_bytes()
    result = migrate_book_owner(path, 'synthetic-account', now=at)
    assert result.disposition == 'already_converted'
    assert result.migration_id == original.migration_id
    assert path.read_bytes() == untouched


@pytest.mark.parametrize('outcome', ['unknown', 'accepted'])
def test_eventless_terminal_resolves_ordinary_fence_from_capacity_evidence(tmp_path, outcome):
    account, _ = owner(tmp_path, [BrokerResult(outcome)])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    at = NOW + timedelta(minutes=15)
    with account._transaction() as db:
        assert account._ordinary_unknown_orders_db(db, now=at) == ('base',)
    account.observe(BrokerFact.fill('full', 'base', 'dj30_mym_p250', 'entry', 3, 100, at), now=at)
    terminal = BrokerFact.terminal('base', 'filled', 3, at)
    account.observe(terminal, now=at)
    with account._transaction() as db:
        assert db.execute('SELECT feedback FROM broker_facts WHERE fact_id=?',
                          (terminal.fact_id,)).fetchone() == (None,)
        assert account._ordinary_unknown_orders_db(db, now=at) == ()


@pytest.mark.parametrize('invalid', ['stale', 'gap', 'equal_time'])
def test_unaccepted_or_nonpostdating_eventless_terminal_cannot_clear_fence(tmp_path, invalid):
    account, _ = owner(tmp_path, [BrokerResult('unknown')])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    if invalid != 'gap':
        account.observe(BrokerFact.fill('full', 'base', 'dj30_mym_p250', 'entry', 3, 100, NOW), now=NOW)
    at = NOW if invalid == 'equal_time' else NOW + timedelta(seconds=1)
    received = at + timedelta(hours=1) if invalid == 'stale' else at
    account.observe(BrokerFact.terminal('base', 'filled', 3, at), now=received)
    with account._transaction() as db:
        assert account._ordinary_unknown_orders_db(db, now=received) == ('base',)


@pytest.mark.parametrize('terminal_status', ['filled', 'cancelled'])
def test_held_close_feedback_is_valid_until_residual_reconciliation(tmp_path, terminal_status):
    case = ProtectionScenario(tmp_path)
    case.enter(bracket=Bracket(stop=98))
    case.broker.queue(BrokerResult('accepted'))
    case.dispatch(close('close', quantity=1 if terminal_status == 'filled' else 3), case.occurrence('close'))
    for fact in case.broker.execute_close('close', execution_id='closed', quantity=1,
                                         price=100, terminal=terminal_status == 'filled', at=case.advance()):
        assert case.owner.observe(fact, now=case.now) == ()
    if terminal_status == 'cancelled':
        assert case.owner.observe(BrokerFact.terminal('close', 'cancelled', 1, case.now), now=case.now) == ()
    with case.owner._transaction() as db:
        validate_records(case.owner, db, 4)
    case.observe()
    with case.owner._transaction() as db:
        validate_records(case.owner, db, 4)


def test_missing_emitted_feedback_is_still_journal_corruption(tmp_path):
    account, _ = owner(tmp_path, [BrokerResult('accepted')])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    account.observe(BrokerFact.fill('full', 'base', 'dj30_mym_p250', 'entry', 3, 100, NOW), now=NOW)
    with account._transaction() as db:
        db.execute('DELETE FROM feedback')
        with pytest.raises(AccountOwnerError, match='fact feedback'):
            validate_records(account, db, 4)


def test_new_held_fill_cannot_hide_missing_previously_emitted_close_feedback(tmp_path):
    case = ProtectionScenario(tmp_path)
    case.enter(bracket=Bracket(stop=98))
    case.broker.queue(BrokerResult('accepted'))
    case.dispatch(close('close'), case.occurrence('close'))
    first = case.broker.execute_close('close', execution_id='first', quantity=1,
                                      price=100, terminal=False, at=case.advance())[0]
    case.owner.observe(first, now=case.now)
    case.observe()
    for fact in case.broker.execute_close('close', execution_id='second', quantity=1,
                                         price=100, terminal=False, at=case.advance()):
        case.owner.observe(fact, now=case.now)
    with case.owner._transaction() as db:
        db.execute('DELETE FROM feedback WHERE fact_id=?', (first.fact_id,))
        with pytest.raises(AccountOwnerError, match='fact feedback'):
            validate_records(case.owner, db, 4)


def test_legacy_json_null_cannot_hide_a_fill_event(tmp_path):
    account, _ = owner(tmp_path, [BrokerResult('accepted')])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    account.observe(BrokerFact.fill('full', 'base', 'dj30_mym_p250', 'entry', 3, 100, NOW), now=NOW)
    with account._transaction() as db:
        db.execute("UPDATE broker_facts SET feedback='null'")
        db.execute('DELETE FROM feedback')
        with pytest.raises(AccountOwnerError, match='eventless terminal'):
            validate_records(account, db, 4)


@pytest.mark.parametrize('legacy_json_null', [False, True])
def test_eventless_close_terminal_journal_remains_valid(tmp_path, legacy_json_null):
    account, _ = owner(tmp_path, [BrokerResult('accepted'), BrokerResult('accepted')])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    account.observe(BrokerFact.fill('full', 'base', 'dj30_mym_p250', 'entry', 3, 100, NOW), now=NOW)
    account.dispatch(close('close'), occurrence=account.make_occurrence('direct', 'close'), now=NOW)
    at = NOW + timedelta(seconds=1)
    account.observe(BrokerFact.fill('closed', 'close', 'dj30_mym_p250', 'exit', 3, 100, at,
                                   entry_execution_id='full'), now=at)
    terminal = BrokerFact.terminal('close', 'filled', 3, at)
    assert account.observe(terminal, now=at) == ()
    with account._transaction() as db:
        assert db.execute('SELECT feedback FROM broker_facts WHERE fact_id=?',
                          (terminal.fact_id,)).fetchone() == (None,)
        if legacy_json_null:
            db.execute("UPDATE broker_facts SET feedback='null' WHERE fact_id=?", (terminal.fact_id,))
        validate_records(account, db, 4)
