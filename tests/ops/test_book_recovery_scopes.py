"""Recovery ownership publication; no synthetic broker capability claims."""
from concurrent.futures import ThreadPoolExecutor
import sqlite3
from pathlib import Path
import subprocess
import sys

import pytest

from book_halt import BookHaltStore, HaltStoreError
from c1_rail_http_server import make_handler
from c1_rail_listener import handle_signal


PRODUCTS = ('6J', 'MGC', 'MYM', 'MNQ')


def boot(path):
    return BookHaltStore.boot(path, 'account', controlled_symbols=PRODUCTS)


def test_handler_publishes_all_product_coverage_before_serving(tmp_path):
    path = tmp_path / 'halt.sqlite'
    make_handler(object(), {'account': 'account', 'book_halt_path': str(path)})
    state = boot(path).snapshot()
    assert {s['symbol'] for s in state['recovery_scopes'] if s['kind'] == 'product'} == set(PRODUCTS)
    assert all(s['status'] == 'reconciliation_required' for s in state['recovery_scopes'])
    assert state['permission'] == 'HALTED'


def test_report_is_atomic_and_duplicate_preserves_external_scope_identity(tmp_path):
    store = boot(tmp_path / 'halt.sqlite')
    state = store.halt('fault', 'execution', observed_symbols=('OTHERZ6', 'MYMZ6'))
    assert {s['symbol'] for s in state['recovery_scopes']} == {*PRODUCTS, 'OTHERZ6', 'MYMZ6'}
    assert store.halt('fault', 'execution', observed_symbols=('MYMZ6', 'OTHERZ6')) == state
    with pytest.raises(HaltStoreError):
        store.halt('fault', 'execution', observed_symbols=('MYMZ6',))
    assert store.snapshot() == state
    restarted = boot(store.path)
    assert restarted.snapshot()['recovery_scopes'] == state['recovery_scopes']
    with pytest.raises(HaltStoreError):
        store.halt('stale', 'feed', observed_symbols=('NEWZ6',))


def test_concurrent_reports_preserve_every_location(tmp_path):
    store = boot(tmp_path / 'halt.sqlite')
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda i: store.halt(f'fault-{i}', 'execution',
                                          observed_symbols=(f'EXT{i}',)), range(8)))
    state = store.snapshot()
    assert len(state['incidents']) == 9
    assert {s['symbol'] for s in state['recovery_scopes']} == {*PRODUCTS, *(f'EXT{i}' for i in range(8))}


def test_failed_scope_publication_rolls_back_incident_and_generation(tmp_path):
    store = boot(tmp_path / 'halt.sqlite')
    before = store.snapshot()
    with sqlite3.connect(store.path) as db:
        db.execute("CREATE TRIGGER fail_scope BEFORE INSERT ON recovery_scopes "
                   "WHEN NEW.symbol='FAIL' BEGIN SELECT RAISE(ABORT, 'crash cut'); END")
    with pytest.raises(HaltStoreError):
        store.halt('fault', 'execution', observed_symbols=('OK', 'FAIL'))
    assert store.snapshot() == before


def test_deleted_scope_is_not_silently_repaired_or_allowed_to_route(tmp_path):
    store = boot(tmp_path / 'halt.sqlite')
    with sqlite3.connect(store.path) as db:
        db.execute("DELETE FROM recovery_scopes WHERE symbol='MYM'")
    with pytest.raises(HaltStoreError):
        store.snapshot()
    with pytest.raises(HaltStoreError):
        boot(store.path)
    action = handle_signal({'leg_id': 'dj30_mym_p250', 'signal_type': 'entry'},
                           object(), 0, config={'dry_run': False}, book_halt=store,
                           sender=lambda *args: pytest.fail('send'))
    assert action.decision.halt and not action.sent


def test_schema_one_migration_preserves_original_incidents(tmp_path):
    path = tmp_path / 'halt.sqlite'
    with sqlite3.connect(path) as db:
        db.execute('CREATE TABLE state (version INTEGER, account TEXT, boot_id TEXT, generation INTEGER, permission TEXT)')
        db.execute('CREATE TABLE incidents (incident_id TEXT PRIMARY KEY, reason TEXT, generation INTEGER UNIQUE)')
        db.execute("INSERT INTO state VALUES (1, 'account', 'old', 2, 'HALTED')")
        db.execute("INSERT INTO incidents VALUES ('boot:old', 'boot', 1)")
        db.execute("INSERT INTO incidents VALUES ('fault', 'feed', 2)")
    state = boot(path).snapshot()
    assert state['incidents'][:2] == [
        {'incident_id': 'boot:old', 'reason': 'boot', 'generation': 1},
        {'incident_id': 'fault', 'reason': 'feed', 'generation': 2}]
    assert len(state['recovery_scopes']) == 4
    assert state['permission'] == 'HALTED'


@pytest.mark.parametrize('symbols', ['MYMZ6', (None,), ('',), ('A', 'A')])
def test_invalid_report_does_not_mutate_store(tmp_path, symbols):
    store = boot(tmp_path / 'halt.sqlite')
    before = store.snapshot()
    with pytest.raises(HaltStoreError):
        store.halt('bad', 'execution', observed_symbols=symbols)
    assert store.snapshot() == before


def test_reboot_cannot_drop_controlled_coverage(tmp_path):
    store = boot(tmp_path / 'halt.sqlite')
    before = store.snapshot()
    with pytest.raises(HaltStoreError):
        BookHaltStore.boot(store.path, 'account', controlled_symbols=('MYM',))
    assert store.snapshot() == before


@pytest.mark.parametrize('during_publication', [True, False])
def test_process_death_keeps_whole_report_or_no_report(tmp_path, during_publication):
    path = tmp_path / 'halt.sqlite'
    boot(path)
    script = tmp_path / 'crash.py'
    script.write_text('''import os, sqlite3, sys
sys.path.insert(0, sys.argv[2])
from book_halt import BookHaltStore
store = BookHaltStore.boot(sys.argv[1], 'account', controlled_symbols=('6J', 'MGC', 'MYM', 'MNQ'))
if sys.argv[3] == 'True':
    original = sqlite3.connect
    def connect(*args, **kwargs):
        db = original(*args, **kwargs)
        db.create_function('crash_now', 0, lambda: os._exit(17))
        return db
    sqlite3.connect = connect
    with sqlite3.connect(store.path) as db:
        db.execute("CREATE TRIGGER crash BEFORE INSERT ON recovery_scopes WHEN NEW.symbol='CRASH' BEGIN SELECT crash_now(); END")
store.halt('crash-fault', 'execution', observed_symbols=('CRASH', 'OTHER'))
os._exit(17)
''', encoding='utf-8')
    rail = Path(__file__).resolve().parents[2] / 'ops' / 'c1_rail'
    result = subprocess.run([sys.executable, str(script), str(path), str(rail),
                             str(during_publication)], check=False, timeout=20)
    assert result.returncode == 17
    if during_publication:
        # Remove only the fault injector; recovery rows are left untouched.
        with sqlite3.connect(path) as db:
            db.execute('DROP TRIGGER crash')
    state = boot(path).snapshot()
    assert ('crash-fault' in {i['incident_id'] for i in state['incidents']}) is (not during_publication)
    locations = {s['symbol'] for s in state['recovery_scopes'] if s['kind'] == 'location'}
    assert locations == (set() if during_publication else {'CRASH', 'OTHER'})
    assert state['permission'] == 'HALTED'
