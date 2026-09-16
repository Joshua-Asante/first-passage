"""Independent review regressions for protection evidence qualification."""
from dataclasses import replace
from datetime import timedelta
import json

from c1_rail.book_account_owner import BookAccountOwner, BrokerResult
from c1_rail.book_protection import ProtectionRead
from c1_rail.book_synthetic_protection import SyntheticProtectionBroker
from c1_signal_daemon.book_protocol import Bracket, BracketAmend
from book_occurrence_fixtures import bare_protection_owner, prepare_protection
from test_book_account_owner import NOW, binding, intent


def test_missing_original_owner_is_nonmutating_boot_corruption(tmp_path):
    import sqlite3
    import pytest
    from c1_rail.book_account_owner import AccountOwnerError
    account, route = bare_protection_owner(tmp_path)
    with sqlite3.connect(account.path) as db:
        db.execute('DELETE FROM protection_owners')
    before = account.path.read_bytes()
    with pytest.raises(AccountOwnerError, match='protection journal'):
        BookAccountOwner.boot(account.path, account.account, binding=binding(), synthetic_broker=route)
    assert account.path.read_bytes() == before


def working(tmp_path):
    account, route = bare_protection_owner(tmp_path)
    route.queue(BrokerResult('accepted'))
    action = BracketAmend('dj30_mym_p250', Bracket(stop=98), ('base-fill',))
    prepare_protection(account, route, action, 'initial-attachment')
    later = NOW + timedelta(seconds=2)
    route.apply(route.commands[-1].operation_id, outcome='applied', at=later)
    read = route.read_protection(ProtectionRead(account.make_occurrence('direct', 'confirm'), ('dj30_mym_p250',), NOW))
    account.observe_protection(read, now=later)
    assert account.protection_owners[0].observed == Bracket(stop=98)
    return account, route


def test_invalid_residual_order_rolls_back_capacity_and_feedback(tmp_path):
    account, route = working(tmp_path)
    before = account.all_feedback
    at = NOW + timedelta(seconds=3)
    event = route.execute_protection('protection:base-fill', quantity=1, price=98, terminal=False, at=at)
    corrupt = replace(event.snapshot.orders[0], effective=Bracket(stop=97))
    event = replace(event, snapshot=replace(event.snapshot, orders=(corrupt,)))
    assert account.observe_protection_execution(event, now=at) == ()
    assert account.exposure('dj30_mym_p250') == (3, 0)
    assert account.all_feedback == before
    assert account.protection_owners[0].observed == Bracket(stop=98)
    assert account.authority == 'INTERVENTION'


def test_equal_time_entry_protection_is_not_observed(tmp_path):
    route = SyntheticProtectionBroker(account='synthetic-account', account_epoch='unbound', at=NOW)
    account = BookAccountOwner.boot(tmp_path / 'owner.sqlite', 'synthetic-account', binding=binding(), synthetic_broker=route)
    route.account_epoch = account.make_occurrence('direct', 'bind').account_epoch
    account.activate_synthetic(now=NOW)
    route.queue(BrokerResult('accepted'))
    result = account.dispatch(replace(intent(), bracket=Bracket(stop=98)),
                              occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    fact = route.execute_entry(result.operation_id, fill_id='base-fill', quantity=result.quantity, price=100, at=NOW)
    account.observe(fact, now=NOW)
    snapshot = route.read_protection(ProtectionRead(account.make_occurrence('direct', 'read'), ('dj30_mym_p250',), NOW-timedelta(seconds=1)))
    account.observe_protection(snapshot, now=NOW)
    assert account.protection_owners[0].observed is None
    assert account.protection_owners[0].pending_operation is not None


def test_rejected_amendment_requires_intact_quantity_before_resolution(tmp_path):
    account, route = working(tmp_path)
    route.queue(BrokerResult('rejected'))
    at = NOW + timedelta(seconds=3)
    route.advance(at)
    action = BracketAmend('dj30_mym_p250', Bracket(stop=99), ('base-fill',))
    prepare_protection(account, route, action, 'rejected-change', now=at)
    operation_id = route.commands[-1].operation_id
    later = at + timedelta(seconds=2)
    route.advance(later)
    snapshot = route.read_protection(ProtectionRead(account.make_occurrence('direct', 'rejected-read'), ('dj30_mym_p250',), at))
    snapshot = replace(snapshot, orders=(replace(snapshot.orders[0], quantity=1),))
    account.observe_protection(snapshot, now=later)
    assert account.authority == 'INTERVENTION'
    assert account.protection_owners[0].pending_operation == operation_id
    with account._transaction() as db:
        body = json.loads(db.execute('SELECT body FROM protection_operations WHERE operation_id=?', (operation_id,)).fetchone()[0])
    assert body['status'] != 'rejected_intact'


def test_retained_bare_snapshot_cannot_be_reused_as_execution_residual(tmp_path):
    from c1_rail.book_protection import ProtectionSnapshot
    from datetime import datetime
    account, route = working(tmp_path)
    with account._transaction() as db:
        raw = json.loads(db.execute("SELECT body FROM protection_facts WHERE kind='snapshot' ORDER BY rowid LIMIT 1").fetchone()[0])
    assert raw['orders'] == []
    old = ProtectionSnapshot(raw['fact_id'], raw['account'], raw['account_epoch'], raw['stream_id'], raw['sequence'],
          datetime.fromisoformat(raw['as_of']), tuple(raw['scope_legs']), raw['complete'], (),
          tuple(tuple(pair) for pair in raw['positions']), tuple(tuple(pair) for pair in raw['resolved_operations']))
    at = NOW + timedelta(seconds=3)
    event = route.execute_protection('protection:base-fill', quantity=3, price=98, terminal=True, at=at)
    event = replace(event, as_of=old.as_of, snapshot=old)
    before = account.all_feedback
    assert account.observe_protection_execution(event, now=at) == ()
    assert account.exposure('dj30_mym_p250') == (3, 0)
    assert account.all_feedback == before
    assert account.authority == 'INTERVENTION'


def test_execution_snapshot_must_cover_trigger_leg(tmp_path):
    account, route = working(tmp_path)
    at = NOW + timedelta(seconds=3)
    event = route.execute_protection('protection:base-fill', quantity=3, price=98, terminal=True, at=at)
    event = replace(event, snapshot=replace(event.snapshot, scope_legs=('orb_mnq_v7',), orders=(), positions=()))
    before = account.all_feedback
    assert account.observe_protection_execution(event, now=at) == ()
    assert account.exposure('dj30_mym_p250') == (3, 0)
    assert account.all_feedback == before


import pytest


@pytest.mark.parametrize('mutation', ['missing_quantity', 'bad_deadline'])
def test_corrupt_protection_owner_boot_refuses_without_writes(tmp_path, mutation):
    from c1_rail.book_account_owner import AccountOwnerError
    import sqlite3
    account, route = working(tmp_path)
    with sqlite3.connect(account.path) as db:
        body = json.loads(db.execute('SELECT body FROM protection_owners').fetchone()[0])
        if mutation == 'missing_quantity':
            del body['quantity']
        else:
            body['deadline'] = 'not-a-time'
        db.execute('UPDATE protection_owners SET body=?', (json.dumps(body),))
    before = account.path.read_bytes()
    with pytest.raises(AccountOwnerError, match='protection'):
        BookAccountOwner.boot(account.path, account.account, binding=binding(), synthetic_broker=route)
    assert account.path.read_bytes() == before


def test_execution_cannot_predate_latest_complete_working_evidence(tmp_path):
    account, route = working(tmp_path)
    at = NOW + timedelta(seconds=3)
    event = route.execute_protection('protection:base-fill', quantity=1, price=98, terminal=False, at=at)
    event = replace(event, as_of=NOW + timedelta(seconds=1))
    before = account.all_feedback
    assert account.observe_protection_execution(event, now=at) == ()
    assert account.exposure('dj30_mym_p250') == (3, 0)
    assert account.all_feedback == before
    assert account.authority == 'INTERVENTION'
