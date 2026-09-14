"""Corruption and caller regressions for the approved 2a/2b boundary."""
import sqlite3

import pytest

from book_halt import BookHaltStore, HaltStoreError
from c1_rail_listener import handle_signal


def test_duplicate_reports_in_malformed_schema_refuse_read_and_boot(tmp_path):
    store = BookHaltStore.boot(tmp_path / 'book.db', 'account')
    store.halt('fault', 'execution', observed_symbols=('EXT',))
    with sqlite3.connect(store.path) as db:
        db.execute('ALTER TABLE recovery_reports RENAME TO old_reports')
        db.execute('CREATE TABLE recovery_reports (incident_id TEXT, observed TEXT)')
        db.execute("INSERT INTO recovery_reports VALUES ('fault', '[]')")
        db.execute('INSERT INTO recovery_reports SELECT * FROM old_reports')
        db.execute('DROP TABLE old_reports')
    with pytest.raises(HaltStoreError):
        store.snapshot()
    with pytest.raises(HaltStoreError):
        BookHaltStore.boot(store.path, 'account')


def test_handle_pins_configured_coverage(tmp_path):
    store = BookHaltStore.boot(tmp_path / 'book.db', 'account',
                               controlled_symbols=('MYM', 'MNQ'))
    with sqlite3.connect(store.path) as db:
        db.execute('UPDATE recovery_config SET products=?', ('["MNQ"]',))
        db.execute("DELETE FROM recovery_scopes WHERE symbol='MYM'")
    with pytest.raises(HaltStoreError):
        store.snapshot()


@pytest.mark.parametrize('kind', ['exit', 'flat'])
def test_configured_exit_never_enters_legacy_sizing_or_transport(tmp_path, kind):
    store = BookHaltStore.boot(tmp_path / 'book.db', 'account')
    action = handle_signal({'leg_id': 'dj30_mym', 'signal_type': kind}, object(), 0,
                           config={'dry_run': False}, book_halt=store,
                           sender=lambda *a: pytest.fail('legacy send'))
    assert action.decision.halt and not action.sent
    assert 'recovery' in action.decision.halt_reason


def test_configured_path_with_missing_owner_refuses_legacy_exit():
    action = handle_signal({'leg_id': 'dj30_mym', 'signal_type': 'exit'}, object(), 0,
                           config={'dry_run': False, 'book_halt_path': 'unavailable'},
                           sender=lambda *a: pytest.fail('legacy send'))
    assert action.decision.halt and not action.sent


def test_exit_refusal_retains_incident_and_alert(tmp_path):
    from book_recovery import RecoveryOwner
    owner = RecoveryOwner.boot(tmp_path / 'book.db', 'account')
    alerts = []
    class Notifier:
        def notify(self, level, message, **kwargs):
            alerts.append((level, message))
    action = handle_signal({'leg_id': 'dj30_mym', 'signal_type': 'exit'}, object(), 0,
                           config={'dry_run': False}, book_halt=owner, notifier=Notifier())
    assert action.decision.halt and alerts
    assert len(owner.snapshot()['incidents']) == 2
