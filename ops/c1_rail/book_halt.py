"""TB-S3 durable halt-only gate. No resume, broker commands or flatness claims.

Every boot is a new fenced owner. Incident history is never cleared. The future
recovery and authorization owners must be integrated before a RUNNING transition
can be added; this schema deliberately rejects RUNNING even if written externally.
"""
from contextlib import closing, contextmanager
from pathlib import Path
import sqlite3
from uuid import uuid4


class HaltStoreError(RuntimeError):
    """Missing, corrupt, conflicting or stale durable state; refuse risk-add."""


_REASONS = frozenset({'boot', 'operator', 'feed', 'control', 'barrier', 'execution',
                      'protection', 'identity', 'schedule', 'expiry'})


def _text(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 256:
        raise HaltStoreError('invalid halt identity')
    return value


class BookHaltStore:
    """SQLite FULL-synchronous, account-bound boot and incident ledger."""

    def __init__(self, path, account, boot_id):
        self.path = Path(path)
        self.account = _text(account)
        self.boot_id = _text(boot_id)

    @contextmanager
    def _transaction(self, *, create=False):
        try:
            uri = self.path.resolve().as_uri() + ('?mode=rwc' if create else '?mode=rw')
            with closing(sqlite3.connect(uri, uri=True, timeout=5, isolation_level=None)) as db:
                db.execute('PRAGMA synchronous=FULL')
                db.execute('BEGIN IMMEDIATE')
                yield db
                db.commit()
        except (sqlite3.Error, OSError, ValueError) as exc:
            raise HaltStoreError('halt state unavailable') from exc

    def _state(self, db, *, check_boot=True):
        rows = db.execute('SELECT version, account, boot_id, generation, permission FROM state').fetchall()
        if len(rows) != 1:
            raise HaltStoreError('invalid halt state')
        version, account, boot, generation, permission = rows[0]
        if (version != 1 or account != self.account or permission != 'HALTED'
                or not isinstance(generation, int) or generation < 1
                or (check_boot and boot != self.boot_id)):
            raise HaltStoreError('invalid or stale halt owner')
        _text(boot)
        facts = db.execute('SELECT incident_id, reason, generation FROM incidents ORDER BY generation').fetchall()
        if len(facts) != generation:
            raise HaltStoreError('incomplete halt history')
        for expected, (incident, reason, number) in enumerate(facts, 1):
            _text(incident)
            if number != expected or reason not in _REASONS:
                raise HaltStoreError('invalid halt history')
        return {'account': account, 'boot_id': boot, 'generation': generation,
                'permission': permission, 'recovery_required': True,
                'incidents': [{'incident_id': i, 'reason': r, 'generation': g}
                              for i, r, g in facts]}

    @classmethod
    def boot(cls, path, account):
        """One call per handler/process boot, never per request."""
        if not isinstance(path, (str, Path)) or not str(path).strip():
            raise HaltStoreError('book_halt_path must name a durable database')
        store = cls(path, account, str(uuid4()))
        existed = store.path.exists()
        with store._transaction(create=True) as db:
            tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if not tables and not existed:
                db.execute('CREATE TABLE state (version INTEGER, account TEXT, boot_id TEXT, '
                           'generation INTEGER, permission TEXT)')
                db.execute('CREATE TABLE incidents (incident_id TEXT PRIMARY KEY, reason TEXT, '
                           'generation INTEGER UNIQUE)')
                db.execute('INSERT INTO state VALUES (1, ?, ?, 1, ?)',
                           (store.account, store.boot_id, 'HALTED'))
                generation = 1
            else:
                old = store._state(db, check_boot=False)
                generation = old['generation'] + 1
                db.execute('UPDATE state SET boot_id=?, generation=?', (store.boot_id, generation))
            db.execute('INSERT INTO incidents VALUES (?, ?, ?)',
                       ('boot:' + store.boot_id, 'boot', generation))
            store._state(db)
        return store

    def halt(self, incident_id, reason):
        """Persist/deduplicate a halt report; no dispatch or completion claim."""
        _text(incident_id)
        if reason not in _REASONS or reason == 'boot' or incident_id.startswith('boot:'):
            raise HaltStoreError('invalid incident reason or reserved identity')
        with self._transaction() as db:
            state = self._state(db)
            previous = next((i for i in state['incidents'] if i['incident_id'] == incident_id), None)
            if previous:
                if previous['reason'] != reason:
                    raise HaltStoreError('conflicting incident identity')
                return state
            generation = state['generation'] + 1
            db.execute('INSERT INTO incidents VALUES (?, ?, ?)', (incident_id, reason, generation))
            db.execute('UPDATE state SET generation=?', (generation,))
            return self._state(db)

    def snapshot(self):
        """Validated read; it never completes recovery or changes permission."""
        with self._transaction() as db:
            return self._state(db)

    def rejection_reason(self):
        """Fail closed, including deletion, corruption and a fenced old boot."""
        try:
            self.snapshot()
        except HaltStoreError:
            return 'book halt state unavailable; risk-add refused'
        return 'book HALTED; recovery and operator resume are not implemented'
