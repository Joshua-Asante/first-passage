"""Account-bound observation journal. Local ordering conveys no broker authority."""
from datetime import datetime, timezone
import hashlib
import json
import sqlite3
from uuid import uuid4


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


class Journal:
    """Private observations persist per request; interrupted runs stay running."""

    def __init__(self, path, account):
        if not isinstance(account, str) or not account.strip():
            raise ValueError('invalid account')
        self.account = account
        self.db = sqlite3.connect(path, timeout=10)
        try:
            self.db.execute('PRAGMA foreign_keys=ON')
            self.db.execute('PRAGMA synchronous=FULL')
            self.db.execute('BEGIN IMMEDIATE')
            tables = {r[0] for r in self.db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if not tables:
                self.db.execute('CREATE TABLE meta (version INTEGER NOT NULL, account_digest TEXT NOT NULL)')
                self.db.execute('INSERT INTO meta VALUES (1, ?)', (digest(account.casefold()),))
                self.db.execute('''CREATE TABLE runs (
                    id TEXT PRIMARY KEY, started TEXT NOT NULL, ended TEXT,
                    state TEXT NOT NULL, exhausted INTEGER NOT NULL DEFAULT 0)''')
                self.db.execute('''CREATE TABLE observations (
                    id INTEGER PRIMARY KEY, run_id TEXT NOT NULL REFERENCES runs(id),
                    kind TEXT NOT NULL, started TEXT NOT NULL, ended TEXT NOT NULL,
                    status INTEGER, body TEXT NOT NULL, flags TEXT NOT NULL)''')
                self.db.execute('''CREATE TABLE fill_versions (
                    id INTEGER PRIMARY KEY, observation_id INTEGER NOT NULL REFERENCES observations(id),
                    execution_id TEXT NOT NULL, body_digest TEXT NOT NULL,
                    body TEXT NOT NULL, classification TEXT NOT NULL,
                    UNIQUE(execution_id, body_digest))''')
            elif tables != {'meta', 'runs', 'observations', 'fill_versions'}:
                raise ValueError('unrecognized journal')
            if self.db.execute('SELECT version, account_digest FROM meta').fetchall() != [
                    (1, digest(account.casefold()))]:
                raise ValueError('journal version or account mismatch')
            self.db.commit()
        except Exception:
            self.db.rollback()
            self.db.close()
            raise

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.db.close()

    def start(self):
        run_id = str(uuid4())
        with self.db:
            self.db.execute('INSERT INTO runs(id, started, state) VALUES (?, ?, ?)',
                            (run_id, utc_now(), 'running'))
        return run_id

    def previous_snapshot(self):
        row = self.db.execute("SELECT body FROM observations WHERE kind='snapshot' ORDER BY id DESC LIMIT 1").fetchone()
        return json.loads(row[0]) if row else None

    def record(self, run_id, kind, started, status, body, flags, fills=()):
        flags = set(flags)
        with self.db:
            observation = self.db.execute('''INSERT INTO observations
                (run_id, kind, started, ended, status, body, flags) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (run_id, kind, started, utc_now(), status, canonical(body), '[]')).lastrowid
            for fill in fills:
                execution_id = fill['executionId']
                old = self.db.execute('''SELECT body FROM fill_versions WHERE execution_id=?
                    ORDER BY id DESC LIMIT 1''', (execution_id,)).fetchone()
                classification = 'first_observation'
                if old:
                    previous = json.loads(old[0])
                    economic = lambda row: {k: v for k, v in row.items() if k not in ('commission', 'fees')}
                    if economic(previous) != economic(fill):
                        classification = 'economic_conflict'
                        flags.add(classification)
                    elif previous != fill:
                        classification = 'fee_revision'
                        flags.add(classification)
                self.db.execute('''INSERT OR IGNORE INTO fill_versions
                    (observation_id, execution_id, body_digest, body, classification) VALUES (?, ?, ?, ?, ?)''',
                    (observation, execution_id, digest(fill), canonical(fill), classification))
            self.db.execute('UPDATE observations SET flags=? WHERE id=?',
                            (canonical(sorted(flags)), observation))

    def finish(self, run_id, exhausted):
        report = self.report(run_id)
        warning_only = {'cached_snapshot', 'fee_revision', 'duplicate_execution'}
        state = 'limited' if set(report['flags']) - warning_only else 'collected'
        with self.db:
            self.db.execute('UPDATE runs SET state=?, ended=?, exhausted=? WHERE id=?',
                            (state, utc_now(), int(exhausted), run_id))
        return self.report(run_id)

    def report(self, run_id):
        row = self.db.execute('SELECT state, exhausted, rowid FROM runs WHERE id=?', (run_id,)).fetchone()
        if row is None:
            raise ValueError('unknown run')
        observations = self.db.execute('SELECT flags FROM observations WHERE run_id=?', (run_id,)).fetchall()
        flags = {f for value, in observations for f in json.loads(value)}
        # A previous conflict is not cleared by a later stable observation.
        if self.db.execute("SELECT 1 FROM fill_versions WHERE classification='economic_conflict' LIMIT 1").fetchone():
            flags.add('economic_conflict')
        count = self.db.execute('''SELECT COUNT(*) FROM fill_versions f JOIN observations o
            ON o.id=f.observation_id WHERE o.run_id=?''', (run_id,)).fetchone()[0]
        unfinished = self.db.execute("SELECT COUNT(*) FROM runs WHERE state='running' AND rowid<?", (row[2],)).fetchone()[0]
        return dict(run_id=run_id, state=row[0], observations=len(observations),
                    fill_versions=count, flags=sorted(flags), prior_unfinished_runs=unfinished,
                    history_stored_rows_exhausted=bool(row[1]),
                    qualification=dict(E1='unproven', E2='unproven', E3='unproven'))
