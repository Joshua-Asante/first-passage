"""TB-S3 durable halt-only gate. No resume, broker commands or flatness claims.

Every boot is a new fenced owner. Incident history is never cleared. The future
recovery and authorization owners must be integrated before a RUNNING transition
can be added; this schema deliberately rejects RUNNING even if written externally.
"""
from contextlib import closing, contextmanager, nullcontext
from pathlib import Path
import json
import sqlite3
from uuid import uuid4

from book_account_lock import AccountSerializer


class HaltStoreError(RuntimeError):
    """Missing, corrupt, conflicting or stale durable state; refuse risk-add."""


_REASONS = frozenset({'boot', 'operator', 'feed', 'control', 'barrier', 'execution',
                      'protection', 'identity', 'schedule', 'expiry'})

_BASE_SCHEMA = {
    'state': 'version INTEGER, account TEXT, boot_id TEXT, generation INTEGER, permission TEXT',
    'incidents': 'incident_id TEXT PRIMARY KEY, reason TEXT, generation INTEGER UNIQUE',
    'recovery_config': 'products TEXT NOT NULL',
    'recovery_reports': 'incident_id TEXT PRIMARY KEY, observed TEXT NOT NULL',
    'recovery_scopes': 'scope_id TEXT PRIMARY KEY, kind TEXT NOT NULL, symbol TEXT NOT NULL, incident_id TEXT NOT NULL',
}


def validate_schema(db, schema):
    """Compare columns, keys and foreign keys, not merely SELECT compatibility."""
    def signature(conn, name):
        columns = conn.execute(f'PRAGMA table_info({name})').fetchall()
        keys = sorted((row[2], row[3], row[4],
                       tuple(r[2] for r in conn.execute(f'PRAGMA index_info({row[1]})')))
                      for row in conn.execute(f'PRAGMA index_list({name})'))
        foreign = conn.execute(f'PRAGMA foreign_key_list({name})').fetchall()
        sql = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone()
        normalized = ''.join(sql[0].lower().split()).replace('"', '') if sql else None
        return columns, keys, foreign, normalized

    with closing(sqlite3.connect(':memory:')) as expected:
        for name, body in schema.items():
            expected.execute(f'CREATE TABLE {name} ({body})')
        for name in schema:
            if signature(db, name) != signature(expected, name):
                raise HaltStoreError('incompatible halt schema: ' + name)


def _text(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 256:
        raise HaltStoreError('invalid halt identity')
    return value


def _symbols(values):
    if not isinstance(values, (tuple, list)):
        raise HaltStoreError('symbols must be an explicit sequence')
    result = [_text(value) for value in values]
    if len(result) != len(set(result)):
        raise HaltStoreError('duplicate symbol')
    return sorted(result)


class BookHaltStore:
    """SQLite FULL-synchronous, account-bound boot and incident ledger."""

    def __init__(self, path, account, boot_id, *, controlled_symbols=()):
        self.path = Path(path).resolve()
        self.account = _text(account)
        self.boot_id = _text(boot_id)
        self.controlled_symbols = _symbols(controlled_symbols)
        self.serializer = AccountSerializer(self.path)

    @contextmanager
    def _transaction(self, *, create=False, locked=False):
        try:
            uri = self.path.resolve().as_uri() + ('?mode=rwc' if create else '?mode=rw')
            with (nullcontext() if locked else self.serializer.acquire()), closing(
                    sqlite3.connect(uri, uri=True, timeout=5, isolation_level=None)) as db:
                db.execute('PRAGMA synchronous=FULL')
                db.execute('PRAGMA foreign_keys=ON')
                db.execute('BEGIN IMMEDIATE')
                yield db
                db.commit()
        except (sqlite3.Error, OSError, ValueError, KeyError, TypeError) as exc:
            raise HaltStoreError('halt state unavailable') from exc

    def _state(self, db, *, check_boot=True, allow_v1=False):
        rows = db.execute('SELECT version, account, boot_id, generation, permission FROM state').fetchall()
        if len(rows) != 1:
            raise HaltStoreError('invalid halt state')
        version, account, boot, generation, permission = rows[0]
        if (version not in ((1, 2, 3) if allow_v1 else (2, 3))
                or account != self.account or permission != 'HALTED'
                or not isinstance(generation, int) or generation < 1
                or (check_boot and boot != self.boot_id)):
            raise HaltStoreError('invalid or stale halt owner')
        validate_schema(db, {k: v for k, v in _BASE_SCHEMA.items()
                             if version >= 2 or k in ('state', 'incidents')})
        _text(boot)
        facts = db.execute('SELECT incident_id, reason, generation FROM incidents ORDER BY generation').fetchall()
        if len(facts) != generation:
            raise HaltStoreError('incomplete halt history')
        for expected, (incident, reason, number) in enumerate(facts, 1):
            _text(incident)
            if number != expected or reason not in _REASONS:
                raise HaltStoreError('invalid halt history')
        result = {'account': account, 'boot_id': boot, 'generation': generation,
                'permission': permission, 'recovery_required': True,
                'incidents': [{'incident_id': i, 'reason': r, 'generation': g}
                              for i, r, g in facts]}
        if version >= 2:
            result.update(self._recovery(db, facts))
        if version == 3:
            from book_recovery_schema import validate
            result.update(validate(db))
        return result

    @staticmethod
    def _controlled(db):
        rows = db.execute('SELECT products FROM recovery_config').fetchall()
        if len(rows) != 1:
            raise HaltStoreError('invalid recovery configuration')
        return _symbols(json.loads(rows[0][0]))

    def _publish(self, db, incident_id, observed):
        db.execute('INSERT INTO recovery_reports VALUES (?, ?)',
                   (incident_id, json.dumps(observed)))
        for kind, symbols in (('product', self._controlled(db)), ('location', observed)):
            for symbol in symbols:
                db.execute('INSERT OR IGNORE INTO recovery_scopes VALUES (?, ?, ?, ?)',
                           (kind + ':' + symbol, kind, symbol, incident_id))

    def _recovery(self, db, facts):
        controlled = self._controlled(db)
        if controlled != self.controlled_symbols:
            raise HaltStoreError('controlled coverage changed')
        rows = db.execute('SELECT incident_id, observed FROM recovery_reports').fetchall()
        reports = dict(rows)
        if len(reports) != len(rows):
            raise HaltStoreError('duplicate recovery reports')
        if set(reports) != {i for i, _, _ in facts}:
            raise HaltStoreError('incomplete recovery reports')
        expected = {}
        decoded = []
        for incident, _, _ in facts:
            observed = _symbols(json.loads(reports[incident]))
            decoded.append({'incident_id': incident, 'observed_symbols': observed})
            for kind, symbols in (('product', controlled), ('location', observed)):
                for symbol in symbols:
                    key = kind + ':' + symbol
                    expected.setdefault(key, (key, kind, symbol, incident))
        actual = db.execute('SELECT scope_id, kind, symbol, incident_id '
                            'FROM recovery_scopes ORDER BY scope_id').fetchall()
        if actual != sorted(expected.values()):
            raise HaltStoreError('incomplete or conflicting recovery scope')
        return {'controlled_symbols': controlled, 'recovery_reports': decoded,
                'recovery_scopes': [dict(scope_id=k, kind=t, symbol=s, incident_id=i,
                                         status='reconciliation_required')
                                    for k, t, s, i in actual]}

    def _migrate(self, db, controlled, incidents):
        db.execute('CREATE TABLE recovery_config (products TEXT NOT NULL)')
        db.execute('INSERT INTO recovery_config VALUES (?)', (json.dumps(controlled),))
        db.execute('CREATE TABLE recovery_reports (incident_id TEXT PRIMARY KEY, observed TEXT NOT NULL)')
        db.execute('CREATE TABLE recovery_scopes (scope_id TEXT PRIMARY KEY, kind TEXT NOT NULL, '
                   'symbol TEXT NOT NULL, incident_id TEXT NOT NULL)')
        for incident in incidents:
            self._publish(db, incident['incident_id'], [])
        db.execute('UPDATE state SET version=2')

    @classmethod
    def boot(cls, path, account, *, controlled_symbols=()):
        """One call per handler/process boot, never per request."""
        if not isinstance(path, (str, Path)) or not str(path).strip():
            raise HaltStoreError('book_halt_path must name a durable database')
        controlled = _symbols(controlled_symbols)
        store = cls(path, account, str(uuid4()), controlled_symbols=controlled)
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
                store._migrate(db, controlled, [])
            else:
                old = store._state(db, check_boot=False, allow_v1=True)
                if 'controlled_symbols' not in old:
                    store._migrate(db, controlled, old['incidents'])
                elif old['controlled_symbols'] != controlled:
                    raise HaltStoreError('controlled coverage changed')
                generation = old['generation'] + 1
                db.execute('UPDATE state SET boot_id=?, generation=?', (store.boot_id, generation))
            db.execute('INSERT INTO incidents VALUES (?, ?, ?)',
                       ('boot:' + store.boot_id, 'boot', generation))
            store._publish(db, 'boot:' + store.boot_id, [])
            if db.execute('SELECT version FROM state').fetchone()[0] == 2:
                from book_recovery_schema import migrate
                migrate(db)
            store._state(db)
        return store

    def halt(self, incident_id, reason, *, observed_symbols=()):
        """Persist/deduplicate a halt report; no dispatch or completion claim."""
        _text(incident_id)
        observed = _symbols(observed_symbols)
        if reason not in _REASONS or reason == 'boot' or incident_id.startswith('boot:'):
            raise HaltStoreError('invalid incident reason or reserved identity')
        with self._transaction() as db:
            state = self._state(db)
            previous = next((i for i in state['incidents'] if i['incident_id'] == incident_id), None)
            if previous:
                report = next(r for r in state['recovery_reports'] if r['incident_id'] == incident_id)
                if previous['reason'] != reason or report['observed_symbols'] != observed:
                    raise HaltStoreError('conflicting incident identity')
                return state
            generation = state['generation'] + 1
            db.execute('INSERT INTO incidents VALUES (?, ?, ?)', (incident_id, reason, generation))
            db.execute('UPDATE state SET generation=?', (generation,))
            self._publish(db, incident_id, observed)
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
