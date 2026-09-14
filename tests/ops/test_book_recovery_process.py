"""SYNTHETIC transport with real SQLite, OS locks and killed child processes."""
from dataclasses import replace
from pathlib import Path
import sqlite3
import subprocess
import sys

import pytest

from book_recovery import RecoveryOwner
from test_book_recovery_owner import SyntheticRoute, demand, evidence, owner_at


ROOT = Path(__file__).resolve().parents[2]
CHILD = r'''
import sys, os, sqlite3
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
root, path, boot_id, mode = sys.argv[1:]
sys.path[:0] = [root + '/ops/c1_rail', root + '/core', root + '/tests/ops']
from book_halt import BookHaltStore
from book_recovery import RecoveryOwner
from test_book_recovery_owner import SyntheticRoute, demand, evidence
path = Path(path)
if mode == 'boot':
    print('BOOT_WAIT', flush=True)
    RecoveryOwner.boot(path, 'account', controlled_products=('MYM', 'MNQ'))
    print('BOOTED', flush=True)
    sys.exit(0)
if mode == 'migration':
    import book_recovery_schema
    original = book_recovery_schema.migrate
    def migrate(db):
        original(db)
        os._exit(71)
    book_recovery_schema.migrate = migrate
    RecoveryOwner.boot(path, 'account', controlled_products=('MYM', 'MNQ'))
store = BookHaltStore(path, 'account', boot_id, controlled_symbols=('MYM', 'MNQ'))
route = SyntheticRoute('partial')
route.sequence = 20
def send(command):
    with sqlite3.connect(str(path) + '.broker') as db:
        db.execute('CREATE TABLE IF NOT EXISTS calls (request_id TEXT)')
        db.execute('INSERT INTO calls VALUES (?)', (command['request_id'],))
    if mode == 'sent':
        os._exit(71)
    return {'state': 'partial', 'filled_quantity': 1}
route.send = send
owner = RecoveryOwner.synthetic(RecoveryOwner(store), route)
original = store._transaction
count = 0
@contextmanager
def transaction(**kwargs):
    global count
    count += 1
    number = count
    with original(**kwargs) as db:
        if mode == 'mid_batch':
            db.create_function('die', 0, lambda: os._exit(71))
            db.execute("CREATE TEMP TRIGGER fail_mid_batch BEFORE INSERT ON recovery_operations "
                       "WHEN NEW.operation_id='close-2' BEGIN SELECT die(); END")
        yield db
        if mode in ('prepared_before', 'attempt_before') and number == 1:
            os._exit(71)
        if mode == 'response_before' and number == 2:
            os._exit(71)
    if mode in ('prepared_after', 'attempt_after') and number == 1:
        os._exit(71)
    if mode == 'response_after' and number == 2:
        os._exit(71)
    if mode == 'paused' and number == 1:
        print('ATTEMPT_COMMITTED', flush=True)
        sys.stdin.readline()
store._transaction = transaction
if mode in ('prepared_before', 'prepared_after', 'mid_batch'):
    a, b = evidence(), evidence('MNQZ6', 'MNQ')
    both = replace(a, orders=a.orders+b.orders, allocations=a.allocations+b.allocations,
                   protection=a.protection+b.protection, observed_symbols=('MYMZ6', 'MNQZ6'),
                   bindings=a.bindings+b.bindings)
    owner.prepare_recovery((demand(), demand('MNQZ6', 'MNQ', 'close-2')), evidence=both)
else:
    owner.dispatch('close-1')
'''


def child(owner, mode):
    return subprocess.Popen([sys.executable, '-c', CHILD, str(ROOT), str(owner.path),
                             owner.store.boot_id, mode], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def calls(path):
    broker = Path(str(path) + '.broker')
    if not broker.exists():
        return []
    with sqlite3.connect(broker) as db:
        return db.execute('SELECT request_id FROM calls').fetchall()


@pytest.mark.parametrize('cut,committed', [('prepared_before', False),
                                         ('mid_batch', False), ('prepared_after', True)])
def test_process_death_during_account_graph(tmp_path, cut, committed):
    owner = owner_at(tmp_path, products=('MYM', 'MNQ'))
    proc = child(owner, cut)
    stdout, stderr = proc.communicate(timeout=15)
    assert proc.returncode == 71, (stdout, stderr)
    restarted = RecoveryOwner.boot(owner.path, 'account', controlled_products=('MYM', 'MNQ'))
    assert len(restarted.snapshot()['operations']) == (2 if committed else 0)
    assert calls(owner.path) == []


@pytest.mark.parametrize('cut,attempts,sends', [('attempt_before', 0, 0),
                                              ('attempt_after', 1, 0), ('sent', 1, 1),
                                              ('response_before', 1, 1)])
def test_process_death_attempt_boundary_and_reboot_no_resend(tmp_path, cut, attempts, sends):
    owner = owner_at(tmp_path, SyntheticRoute(), products=('MYM', 'MNQ'))
    owner.prepare(demand(), evidence=evidence())
    proc = child(owner, cut)
    stdout, stderr = proc.communicate(timeout=15)
    assert proc.returncode == 71, (stdout, stderr)
    restarted = RecoveryOwner.boot(owner.path, 'account', controlled_products=('MYM', 'MNQ'))
    restarted = RecoveryOwner.synthetic(restarted, SyntheticRoute())
    restarted.dispatch('close-1')
    state = restarted.snapshot()
    assert len(state['attempts']) == attempts
    assert len(calls(owner.path)) == sends
    if attempts:
        assert state['attempts'][0]['state'] == 'UNKNOWN'
        assert state['attempts'][0]['observation'] is None


def test_new_boot_cannot_cross_committed_attempt_to_transport_gap(tmp_path):
    owner = owner_at(tmp_path, SyntheticRoute(), products=('MYM', 'MNQ'))
    owner.prepare(demand(), evidence=evidence())
    dispatch = child(owner, 'paused')
    boot = None
    try:
        assert dispatch.stdout.readline().strip() == 'ATTEMPT_COMMITTED'
        boot = child(owner, 'boot')
        assert boot.stdout.readline().strip() == 'BOOT_WAIT'
        # Bounded negative assertion after a pipe barrier, not a sleep-based race.
        with pytest.raises(subprocess.TimeoutExpired):
            boot.communicate(timeout=0.25)
        with sqlite3.connect(owner.path) as db:
            assert db.execute('SELECT boot_id FROM state').fetchone()[0] == owner.store.boot_id
        assert calls(owner.path) == []
        stdout, stderr = dispatch.communicate(input='continue\n', timeout=15)
        assert dispatch.returncode == 0, (stdout, stderr)
        stdout, stderr = boot.communicate(timeout=15)
        assert boot.returncode == 0 and 'BOOTED' in stdout, stderr
        from book_halt import HaltStoreError
        with pytest.raises(HaltStoreError):
            owner.dispatch('close-1')
        assert len(calls(owner.path)) == 1
    finally:
        for proc in (dispatch, boot):
            if proc is not None and proc.poll() is None:
                proc.kill()
                proc.communicate(timeout=5)


def test_process_death_inside_schema_migration_rolls_back(tmp_path):
    path = tmp_path / 'book.db'
    with sqlite3.connect(path) as db:
        db.execute('CREATE TABLE state (version INTEGER, account TEXT, boot_id TEXT, generation INTEGER, permission TEXT)')
        db.execute('CREATE TABLE incidents (incident_id TEXT PRIMARY KEY, reason TEXT, generation INTEGER UNIQUE)')
        db.execute("INSERT INTO state VALUES (1, 'account', 'old', 1, 'HALTED')")
        db.execute("INSERT INTO incidents VALUES ('boot:old', 'boot', 1)")
    proc = subprocess.run([sys.executable, '-c', CHILD, str(ROOT), str(path), 'old', 'migration'],
                          capture_output=True, text=True, timeout=15, check=False)
    assert proc.returncode == 71, proc.stderr
    with sqlite3.connect(path) as db:
        assert db.execute('SELECT version, boot_id FROM state').fetchone() == (1, 'old')
    restarted = RecoveryOwner.boot(path, 'account', controlled_products=('MYM', 'MNQ'))
    assert restarted.snapshot()['incidents'][0]['incident_id'] == 'boot:old'


def test_two_symbol_partial_response_commit_survives_death_without_resend(tmp_path):
    owner = owner_at(tmp_path, SyntheticRoute(), products=('MYM', 'MNQ'))
    a, b = evidence(), evidence('MNQZ6', 'MNQ')
    both = replace(a, orders=a.orders+b.orders, allocations=a.allocations+b.allocations,
                   protection=a.protection+b.protection, observed_symbols=('MYMZ6', 'MNQZ6'),
                   bindings=a.bindings+b.bindings)
    owner.prepare_recovery((demand(), demand('MNQZ6', 'MNQ', 'close-2')), evidence=both)
    proc = child(owner, 'response_after')
    stdout, stderr = proc.communicate(timeout=15)
    assert proc.returncode == 71, (stdout, stderr)
    restarted = RecoveryOwner.boot(owner.path, 'account', controlled_products=('MYM', 'MNQ'))
    state = restarted.snapshot()
    assert state['attempts'][0]['observation'] == {'state': 'partial', 'filled_quantity': 1}
    assert [(o['operation_id'], o['status']) for o in state['operations']] == [
        ('close-1', 'unresolved'), ('close-2', 'prepared')]
    assert len(calls(owner.path)) == 1
    assert state['permission'] == 'HALTED'
