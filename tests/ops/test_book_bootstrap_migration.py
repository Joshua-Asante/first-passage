"""Fresh bootstrap is a one-use entitlement; conversion never grants authority."""
from dataclasses import replace
from datetime import timedelta
import sqlite3

import pytest

from c1_rail.book_account_owner import AccountOwnerError, BookAccountOwner, BrokerResult
from test_book_account_owner import NOW, binding, owner, intent
from pathlib import Path
import hashlib
import json


FIXTURES = Path(__file__).parents[1] / 'fixtures/book_migration'


def restore_fixture(path, name):
    fixture = json.loads((FIXTURES / name).read_text())
    tables = fixture['tables']
    assert hashlib.sha256(json.dumps(tables, sort_keys=True, separators=(',', ':')).encode()).hexdigest() == fixture['logical_digest']
    with sqlite3.connect(path) as db:
        for table, data in tables.items():
            if table != 'sqlite_sequence':
                db.execute(data['sql'])
        for table, data in tables.items():
            if table == 'sqlite_sequence':
                db.execute('DELETE FROM sqlite_sequence')
            if data['rows']:
                rows = [[bytes.fromhex(v['sqlite_blob_hex']) if isinstance(v, dict) and set(v) == {'sqlite_blob_hex'} else v for v in row] for row in data['rows']]
                db.executemany(f"INSERT INTO {table} VALUES ({','.join('?' for _ in data['columns'])})", rows)
    return fixture


@pytest.mark.parametrize('version', [1, 2, 3])
@pytest.mark.parametrize('scenario', ['empty', 'filled', 'pending_takeover', 'completed_takeover', 'amend_accepted', 'amend_unknown'])
def test_conversion_preserves_source_rows_and_never_rearms(tmp_path, version, scenario):
    from c1_rail.book_migration import migrate_book_owner
    from test_four_leg_runtime import binding as normal_binding
    path = tmp_path / 'owner.sqlite'
    fixture = restore_fixture(path, f'{version}-{scenario}.json')
    result = migrate_book_owner(path, 'synthetic-account', now=NOW)
    assert result.source_version == version and result.target_version == 4
    with sqlite3.connect(path) as db:
        for table, data in fixture['tables'].items():
            if table not in ('owner_state', 'sqlite_sequence'):
                assert db.execute(f'SELECT * FROM {table} ORDER BY rowid').fetchall() == [tuple(r) for r in data['rows']], table
    before = path.read_bytes()
    repeated = migrate_book_owner(path, 'synthetic-account', now=NOW + timedelta(seconds=1))
    assert repeated.disposition == 'already_converted'
    assert repeated.migration_id == result.migration_id and path.read_bytes() == before
    account = BookAccountOwner.boot(path, 'synthetic-account', binding=normal_binding())
    assert account.permission == 'HALTED' and account.authority == 'INTERVENTION'
    with pytest.raises(AccountOwnerError):
        account.activate_synthetic(now=NOW)


@pytest.mark.parametrize('damage', ['missing_table', 'bad_version', 'missing_owner', 'bad_binding', 'missing_occurrences', 'wrong_symbol', 'wrong_quantity', 'fact_quantity'])
def test_bad_source_is_not_repaired(tmp_path, damage):
    from c1_rail.book_migration import migrate_book_owner
    path = tmp_path / 'owner.sqlite'
    restore_fixture(path, '2-filled.json')
    with sqlite3.connect(path) as db:
        if damage == 'missing_table': db.execute('DROP TABLE feed_watch')
        if damage == 'bad_version': db.execute('UPDATE owner_state SET schema=17')
        if damage == 'missing_owner': db.execute('DELETE FROM protection_owners')
        if damage == 'bad_binding': db.execute("UPDATE runtime_bindings SET digest='bad'")
        if damage == 'missing_occurrences': db.execute('DELETE FROM action_occurrences')
        if damage == 'wrong_symbol': db.execute("UPDATE operations SET order_symbol='WRONG'")
        if damage == 'wrong_quantity': db.execute('UPDATE operations SET quantity=999')
        if damage == 'fact_quantity':
            fact = json.loads(db.execute("SELECT body FROM broker_facts WHERE fact_id='original-fill'").fetchone()[0])
            fact['quantity'] = 999
            db.execute("UPDATE broker_facts SET body=? WHERE fact_id='original-fill'", (json.dumps(fact),))
    before = path.read_bytes()
    with pytest.raises(AccountOwnerError):
        migrate_book_owner(path, 'synthetic-account', now=NOW)
    assert path.read_bytes() == before


@pytest.mark.parametrize('history', ['incident', 'restart'])
def test_empty_history_cannot_rearm(tmp_path, history):
    account, broker = owner(tmp_path, [])
    if history == 'incident':
        account.halt('incident', 'execution', now=NOW)
    else:
        account = BookAccountOwner.boot(account.path, account.account, binding=account.binding, synthetic_broker=broker)
    with pytest.raises(AccountOwnerError):
        account.activate_synthetic(now=NOW)
    assert account.permission == 'HALTED'
    assert account.authority == 'INTERVENTION'
    assert broker.commands == []


def test_running_activation_is_noop_after_activity(tmp_path):
    account, broker = owner(tmp_path, [BrokerResult('accepted')])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    before = account.path.read_bytes()
    account.activate_synthetic(now=NOW + timedelta(seconds=1))
    assert account.path.read_bytes() == before
    assert len(broker.commands) == 1


def test_receipt_only_provider_cannot_establish_empty_account(tmp_path):
    from c1_rail.book_account_owner import SyntheticBroker
    account = BookAccountOwner.boot(tmp_path / 'owner.sqlite', 'synthetic-account', binding=binding(), synthetic_broker=SyntheticBroker([]))
    with pytest.raises(AccountOwnerError):
        account.activate_synthetic(now=NOW)
    assert account.permission == 'HALTED'


def fresh(tmp_path):
    from book_bootstrap_fixtures import BootstrapBroker
    broker = BootstrapBroker()
    account = BookAccountOwner.boot(tmp_path / 'owner.sqlite', 'synthetic-account', binding=binding(), synthetic_broker=broker)
    broker.account_epoch = account.make_occurrence('direct', 'bind').account_epoch
    return account, broker


@pytest.mark.parametrize('damage', ['position', 'working', 'request', 'incomplete', 'foreign', 'stale', 'nested_position', 'nested_request'])
def test_bootstrap_requires_independent_complete_empty_inventory(tmp_path, monkeypatch, damage):
    from c1_rail.book_takeover import InventoryPosition, WorkingOrder, RequestOutcome
    account, broker = fresh(tmp_path)
    original = broker.read_bootstrap_inventory
    def corrupt(read):
        snap = original(read)
        changes = {
            'position': dict(positions=(InventoryPosition('outside', 'external', 'vanguard_mgc', 'MGC1!', 'buy', 1),)),
            'working': dict(working_orders=(WorkingOrder('outside', 'external', 'vanguard_mgc', 'MGC1!', 'entry', 1),)),
            'request': dict(requests=(RequestOutcome('external', 'attempt', None, 'unknown', None),)),
            'incomplete': dict(complete=False), 'foreign': dict(account_epoch='foreign'),
            'stale': dict(as_of=NOW - timedelta(seconds=1)),
            'nested_position': dict(protection=replace(snap.protection, positions=(('external', 1),))),
            'nested_request': dict(protection=replace(snap.protection, resolved_operations=('external',))),
        }
        return replace(snap, **changes[damage])
    monkeypatch.setattr(broker, 'read_bootstrap_inventory', corrupt)
    with pytest.raises(AccountOwnerError):
        account.activate_synthetic(now=NOW)
    assert account.permission == 'HALTED' and broker.commands == []


def test_restart_before_first_activation_consumes_freshness(tmp_path):
    account, broker = fresh(tmp_path)
    restarted = BookAccountOwner.boot(account.path, account.account, binding=account.binding, synthetic_broker=broker)
    for actor in (account, restarted):
        with pytest.raises(AccountOwnerError):
            actor.activate_synthetic(now=NOW)
    assert restarted.permission == 'HALTED'


@pytest.mark.parametrize('damage', ['bootstrap', 'read', 'read_body', 'migration_record', 'legacy_fill', 'legacy_operation'])
def test_current_missing_authority_record_is_corruption(tmp_path, damage):
    from c1_rail.book_migration import migrate_book_owner
    from test_four_leg_runtime import binding as normal_binding
    if damage in ('migration_record', 'legacy_fill', 'legacy_operation'):
        path = tmp_path / 'owner.sqlite'
        restore_fixture(path, '1-filled.json')
        migrate_book_owner(path, 'synthetic-account', now=NOW)
        bound = normal_binding()
    else:
        account, _ = owner(tmp_path, [])
        path, bound = account.path, account.binding
    with sqlite3.connect(path) as db:
        if damage == 'bootstrap': db.execute('DELETE FROM bootstrap_identity')
        if damage == 'read': db.execute('DELETE FROM bootstrap_reads')
        if damage == 'read_body': db.execute("UPDATE bootstrap_reads SET body='{}'")
        if damage == 'migration_record': db.execute('DELETE FROM migration_records')
        if damage == 'legacy_fill': db.execute("DELETE FROM legacy_obligations WHERE kind='fill'")
        if damage == 'legacy_operation': db.execute("DELETE FROM legacy_obligations WHERE kind='operation'")
    before = path.read_bytes()
    with pytest.raises(AccountOwnerError):
        BookAccountOwner.boot(path, 'synthetic-account', binding=bound)
    assert path.read_bytes() == before


@pytest.mark.parametrize('cut', ['ddl:bootstrap_identity', 'ddl:legacy_obligations', 'before_validation', 'before_commit', 'after_commit'])
def test_interrupted_migration_is_original_or_complete_target(tmp_path, cut):
    from c1_rail.book_migration import migrate_book_owner
    path = tmp_path / 'owner.sqlite'
    restore_fixture(path, '1-filled.json')
    before = path.read_bytes()
    with pytest.raises(AccountOwnerError):
        migrate_book_owner(path, 'synthetic-account', now=NOW, crash_at=cut)
    if cut != 'after_commit':
        assert path.read_bytes() == before
    result = migrate_book_owner(path, 'synthetic-account', now=NOW)
    assert result.disposition == ('already_converted' if cut == 'after_commit' else 'converted')


def test_late_legacy_fill_extends_quarantine_without_inventing_protection(tmp_path):
    from c1_rail.book_migration import migrate_book_owner
    from c1_rail.book_account_owner import BrokerFact
    from test_four_leg_runtime import binding as normal_binding
    path = tmp_path / 'owner.sqlite'
    restore_fixture(path, '1-filled.json')
    migrate_book_owner(path, 'synthetic-account', now=NOW)
    account = BookAccountOwner.boot(path, 'synthetic-account', binding=normal_binding())
    account.observe(BrokerFact.fill('late', 'entry:vanguard_mgc', 'vanguard_mgc', 'entry', 1, 100, NOW), now=NOW)
    assert account.exposure('vanguard_mgc') == (2, 0)
    assert account.protection_owners == ()
    assert account.permission == 'HALTED'
    assert {row['source_id'] for row in account.status()['legacy_obligations'] if row['kind'] == 'fill'} == {'late', 'original-fill'}
    with sqlite3.connect(path) as db:
        assert db.execute("SELECT source_id FROM legacy_obligations WHERE kind='fill' ORDER BY source_id").fetchall() == [('late',), ('original-fill',)]


@pytest.mark.parametrize('version', [2, 3])
@pytest.mark.parametrize('outcome', ['accepted', 'unknown'])
def test_consumed_pending_owner_and_original_deadline_survive_migration(tmp_path, version, outcome):
    from c1_rail.book_migration import migrate_book_owner
    path = tmp_path / 'owner.sqlite'
    fixture = restore_fixture(path, f'{version}-consumed_pending_{outcome}.json')
    expected = fixture['tables']['protection_owners']['rows']
    migrate_book_owner(path, 'synthetic-account', now=NOW)
    account = BookAccountOwner.boot(path, 'synthetic-account', binding=binding())
    state = account.protection_owners[0]
    assert state.consumed and state.pending_operation and state.deadline
    with sqlite3.connect(path) as db:
        assert db.execute('SELECT * FROM protection_owners').fetchall() == [tuple(row) for row in expected]
    account.check_protection_deadlines(now=state.deadline)
    assert account.authority == 'INTERVENTION'


def test_failed_bootstrap_storage_latches_send_suppression(tmp_path):
    account, broker = fresh(tmp_path)
    with sqlite3.connect(account.path) as db:
        db.execute("CREATE TRIGGER fail_bootstrap BEFORE INSERT ON bootstrap_reads BEGIN SELECT RAISE(ABORT, 'storage unavailable'); END")
    with pytest.raises(AccountOwnerError):
        account.activate_synthetic(now=NOW)
    with sqlite3.connect(account.path) as db:
        db.execute('DROP TRIGGER fail_bootstrap')
    with pytest.raises(AccountOwnerError):
        account.activate_synthetic(now=NOW)
    assert account.permission == 'HALTED' and broker.commands == []


def test_schema_three_cannot_quarantine_a_missing_takeover_plan(tmp_path):
    from c1_rail.book_migration import migrate_book_owner, add_obligation
    from test_four_leg_runtime import binding as normal_binding
    path = tmp_path / 'owner.sqlite'
    fixture = restore_fixture(path, '3-pending_takeover.json')
    result = migrate_book_owner(path, 'synthetic-account', now=NOW)
    with sqlite3.connect(path) as db:
        db.execute('DELETE FROM takeover_plans')
        digest = db.execute('SELECT source_digest FROM migration_records').fetchone()[0]
        row = next(row for row in fixture['tables']['operations']['rows'] if row[0] == 'entry:aegis_6j')
        add_obligation(db, result.migration_id, digest, 'operations', row[0], 'takeover', row)
    with pytest.raises(AccountOwnerError):
        BookAccountOwner.boot(path, 'synthetic-account', binding=normal_binding())


def test_attached_settlement_migration_preserves_blob_sources_and_sealed_chain(tmp_path):
    from c1_rail.book_migration import migrate_book_owner
    path = tmp_path / 'owner.sqlite'
    restore_fixture(path, '3-attached_settlement.json')
    with sqlite3.connect(path) as db:
        before = db.execute('SELECT * FROM sources ORDER BY rowid').fetchall()
    assert before and any(isinstance(v, bytes) for row in before for v in row)
    result = migrate_book_owner(path, 'synthetic-account', now=NOW)
    assert result.disposition == 'converted'
    with sqlite3.connect(path) as db:
        assert db.execute('SELECT * FROM sources ORDER BY rowid').fetchall() == before
    assert migrate_book_owner(path, 'synthetic-account', now=NOW).disposition == 'already_converted'


def test_unprovable_legacy_protection_execution_is_retained_without_accounting(tmp_path):
    from c1_rail.book_migration import migrate_book_owner
    from c1_rail.book_protection import ProtectionExecution, ProtectionSnapshot
    from test_four_leg_runtime import binding as normal_binding
    path = tmp_path / 'owner.sqlite'
    restore_fixture(path, '1-filled.json')
    migrate_book_owner(path, 'synthetic-account', now=NOW)
    account = BookAccountOwner.boot(path, 'synthetic-account', binding=normal_binding())
    epoch = account.status()['account_epoch']
    snapshot = ProtectionSnapshot('legacy-inventory', account.account, epoch, 'legacy-stream', 1,
        NOW, ('vanguard_mgc',), True, (), (), ())
    event = ProtectionExecution('legacy-execution', account.account, epoch, 'protection:original-fill',
        'unprovable-order', NOW, 1, 98, (('original-fill', 1),), True, snapshot)
    before = account.exposure('vanguard_mgc')
    assert account.observe_protection_execution(event, now=NOW) == ()
    assert account.exposure('vanguard_mgc') == before
    with sqlite3.connect(path) as db:
        assert db.execute('SELECT kind FROM protection_facts WHERE fact_id=?', (event.fact_id,)).fetchone() == ('legacy_unresolved',)


def test_halt_wins_serialized_race_with_fresh_activation(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event
    account, broker = fresh(tmp_path)
    locked, release, started = Event(), Event(), Event()
    original = account._halt_db
    def paused_halt(*args):
        locked.set()
        assert release.wait(5)
        return original(*args)
    monkeypatch.setattr(account, '_halt_db', paused_halt)
    def activate():
        started.set()
        with pytest.raises(AccountOwnerError):
            account.activate_synthetic(now=NOW)
    with ThreadPoolExecutor(max_workers=2) as pool:
        halt = pool.submit(account.halt, 'race', 'operator', now=NOW)
        assert locked.wait(5)
        activation = pool.submit(activate)
        try:
            assert started.wait(5)
        finally:
            release.set()
        halt.result(timeout=5)
        activation.result(timeout=5)
    assert account.permission == 'HALTED' and broker.commands == []


def test_current_schema_does_not_accept_weakened_identity_constraints(tmp_path):
    account, _ = owner(tmp_path, [])
    with sqlite3.connect(account.path) as db:
        record = db.execute('SELECT * FROM bootstrap_identity').fetchone()
        db.execute('DROP TABLE bootstrap_identity')
        db.execute('CREATE TABLE bootstrap_identity (singleton INTEGER, body TEXT)')
        db.execute('INSERT INTO bootstrap_identity VALUES (?, ?)', record)
    before = account.path.read_bytes()
    with pytest.raises(AccountOwnerError):
        BookAccountOwner.boot(account.path, account.account, binding=account.binding)
    assert account.path.read_bytes() == before


@pytest.mark.parametrize('version', [1, 2])
def test_quarantined_takeover_has_no_inventory_or_send_continuation(tmp_path, version):
    from c1_rail.book_migration import migrate_book_owner
    from test_four_leg_runtime import binding as normal_binding
    from c1_rail.book_account_owner import SyntheticBroker
    path = tmp_path / 'owner.sqlite'
    restore_fixture(path, f'{version}-pending_takeover.json')
    migrate_book_owner(path, 'synthetic-account', now=NOW)
    broker = SyntheticBroker([])
    account = BookAccountOwner.boot(path, 'synthetic-account', binding=normal_binding(), synthetic_broker=broker)
    assert account.prepare_takeover_inventory(now=NOW) is None
    account.resume_takeover(now=NOW)
    assert broker.commands == []


@pytest.mark.parametrize('table', ['attempts', 'broker_facts', 'feedback', 'capacity_events', 'action_occurrences'])
def test_original_migrated_history_cannot_disappear(tmp_path, table):
    from c1_rail.book_migration import migrate_book_owner
    from test_four_leg_runtime import binding as normal_binding
    path = tmp_path / 'owner.sqlite'
    restore_fixture(path, '2-filled.json')
    migrate_book_owner(path, 'synthetic-account', now=NOW)
    with sqlite3.connect(path) as db:
        db.execute(f'DELETE FROM {table}')
    before = path.read_bytes()
    with pytest.raises(AccountOwnerError):
        BookAccountOwner.boot(path, 'synthetic-account', binding=normal_binding())
    assert path.read_bytes() == before


@pytest.mark.parametrize('field', ['fact_id', 'stream_id', 'sequence'])
def test_retained_bootstrap_proof_requires_all_inventory_identities(tmp_path, field):
    account, _ = owner(tmp_path, [])
    with sqlite3.connect(account.path) as db:
        body = json.loads(db.execute('SELECT body FROM bootstrap_reads').fetchone()[0])
        del body['snapshot'][field]
        db.execute('UPDATE bootstrap_reads SET body=?', (json.dumps(body),))
    with pytest.raises(AccountOwnerError):
        BookAccountOwner.boot(account.path, account.account, binding=account.binding)


@pytest.mark.parametrize('field,value', [('cap_allocations', 999), ('lifecycle_tiers', 'UNKNOWN')])
def test_fresh_boot_rejects_invalid_admission_binding_before_retention(tmp_path, field, value):
    from book_bootstrap_fixtures import BootstrapBroker
    bound = binding()
    bound[field] = dict(bound[field], vanguard_mgc=value)
    path = tmp_path / 'owner.sqlite'
    with pytest.raises(AccountOwnerError):
        BookAccountOwner.boot(path, 'synthetic-account', binding=bound, synthetic_broker=BootstrapBroker())
    assert not path.exists()


@pytest.mark.parametrize('version', [1, 2, 3])
def test_migrated_feedback_replays_and_checkpoints_without_sends(tmp_path, version):
    from c1_rail.book_migration import migrate_book_owner
    from c1_rail.book_account_owner import SyntheticBroker
    from c1_signal_daemon.book_runtime import FourLegRuntime
    from c1_signal_daemon.book_protocol import Mode
    from test_four_leg_runtime import binding as normal_binding, inert_adapters
    path = tmp_path / 'owner.sqlite'
    restore_fixture(path, f'{version}-filled.json')
    migrate_book_owner(path, 'synthetic-account', now=NOW)
    broker = SyntheticBroker([])
    account = BookAccountOwner.boot(path, 'synthetic-account', binding=normal_binding(), synthetic_broker=broker)
    adapters = inert_adapters()
    # Historical direct harnesses configured NORMAL before entry; no barrier
    # exists in these fixtures to initialize an adapter's mode during replay.
    for adapter in adapters.values():
        adapter.set_mode(Mode.NORMAL)
    FourLegRuntime.recover(account, adapters)
    first = account.all_feedback
    assert all(row['delivered'] and row['checkpoint'] is not None for row in first)
    restarted = BookAccountOwner.boot(path, 'synthetic-account', binding=normal_binding(), synthetic_broker=broker)
    fresh_adapters = inert_adapters()
    for adapter in fresh_adapters.values():
        adapter.set_mode(Mode.NORMAL)
    FourLegRuntime.recover(restarted, fresh_adapters)
    assert restarted.all_feedback == first
    assert broker.commands == [] and restarted.permission == 'HALTED'

@pytest.mark.parametrize('mutation', ['pending', 'attempt', 'scope', 'effective'])
def test_migrated_pending_protection_preserves_frozen_obligations(tmp_path, mutation):
    from c1_rail.book_migration import migrate_book_owner
    path = tmp_path / 'owner.sqlite'
    restore_fixture(path, '2-consumed_pending_unknown.json')
    migrate_book_owner(path, 'synthetic-account', now=NOW)
    with sqlite3.connect(path) as db:
        if mutation == 'pending':
            identity, raw = db.execute('SELECT owner_id,body FROM protection_owners').fetchone()
            body = json.loads(raw)
            body.update(pending_operation=None, deadline=None)
            db.execute('UPDATE protection_owners SET body=? WHERE owner_id=?', (json.dumps(body), identity))
        elif mutation == 'attempt':
            db.execute("UPDATE attempts SET state='ACCEPTED',observation='rewritten'")
        elif mutation == 'scope':
            db.execute("UPDATE action_occurrences SET scope='[]' WHERE scope IS NOT NULL")
        else:
            identity, raw = db.execute('SELECT operation_id,body FROM protection_operations ORDER BY rowid DESC').fetchone()
            body = json.loads(raw)
            body['quantity'] += 1
            db.execute('UPDATE protection_operations SET body=? WHERE operation_id=?', (json.dumps(body), identity))
    before = path.read_bytes()
    with pytest.raises(AccountOwnerError):
        BookAccountOwner.boot(path, 'synthetic-account', binding=binding())
    assert path.read_bytes() == before

@pytest.mark.parametrize('mutation', ['clear', 'extend'])
def test_migrated_live_pending_obligation_requires_resolution(tmp_path, mutation):
    from c1_rail.book_migration import migrate_book_owner
    path = tmp_path / 'owner.sqlite'
    restore_fixture(path, '2-amend_unknown.json')
    migrate_book_owner(path, 'synthetic-account', now=NOW)
    with sqlite3.connect(path) as db:
        identity, raw = db.execute('SELECT owner_id,body FROM protection_owners').fetchone()
        body = json.loads(raw)
        if mutation == 'clear':
            body.update(pending_operation=None, deadline=None)
        else:
            body['deadline'] = (NOW + timedelta(days=1)).isoformat()
        db.execute('UPDATE protection_owners SET body=? WHERE owner_id=?', (json.dumps(body), identity))
    before = path.read_bytes()
    with pytest.raises(AccountOwnerError):
        BookAccountOwner.boot(path, 'synthetic-account', binding=binding())
    assert path.read_bytes() == before

def test_migrated_pending_resolution_survives_later_unrelated_snapshot(tmp_path):
    from datetime import datetime
    from c1_rail.book_migration import migrate_book_owner
    from c1_rail.book_protection import ProtectionSnapshot, ObservedProtection, bracket_from_dict
    path = tmp_path / 'owner.sqlite'
    fixture = restore_fixture(path, '2-live_pending_unknown.json')
    migrate_book_owner(path, 'synthetic-account', now=NOW)
    account = BookAccountOwner.boot(path, 'synthetic-account', binding=binding())
    data = fixture['resolution_snapshot']
    snapshot = ProtectionSnapshot(**{**data, 'as_of': datetime.fromisoformat(data['as_of']),
        'scope_legs': tuple(data['scope_legs']), 'positions': tuple(map(tuple, data['positions'])),
        'resolved_operations': tuple(map(tuple, data['resolved_operations'])),
        'orders': tuple(ObservedProtection(**{**r, 'broker_order_ids': tuple(r['broker_order_ids']),
            'effective': bracket_from_dict(r['effective'])}) for r in data['orders'])})
    account.observe_protection(snapshot, now=snapshot.as_of)
    assert account.protection_owners[0].pending_operation is None
    later = replace(snapshot, fact_id='later-unrelated', sequence=snapshot.sequence+1,
                    as_of=snapshot.as_of+timedelta(milliseconds=100), resolved_operations=())
    account.observe_protection(later, now=later.as_of)
    restarted = BookAccountOwner.boot(path, 'synthetic-account', binding=binding())
    assert restarted.protection_owners[0].pending_operation is None
    assert restarted.permission == 'HALTED'
