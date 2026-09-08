"""Durable local evidence with a disposable, revision-stamped SQLite projection."""
from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import subprocess
import uuid
from contextlib import closing, contextmanager
from datetime import datetime, timezone
from pathlib import Path

from .model import EvidenceError, canonical, relative_path, replay, source_version, timestamp, verify_excerpt
from .retrieval import ancestors, candidates, request, selectable, temporal


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise EvidenceError(f'duplicate JSON field: {key}')
        result[key] = value
    return result


class Store:
    """Single-writer store. Source bytes and journal, not SQLite, are durable inputs."""

    def __init__(self, repo, root, clock=None):
        self.repo = Path(repo).resolve()
        self.root = Path(root).resolve()
        if not self.repo.is_dir():
            raise EvidenceError('repository directory does not exist')
        self.clock = clock or (lambda: datetime.now(timezone.utc).isoformat())

    @contextmanager
    def _lock(self):
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.root / 'writer.lock'
        try:
            handle = path.open('x', encoding='utf-8')
        except FileExistsError as exc:
            raise EvidenceError('store is locked; verify no writer is active before removing writer.lock') from exc
        try:
            with handle:
                handle.write(str(os.getpid()))
                handle.flush()
            yield
        finally:
            path.unlink()

    def _load(self):
        path = self.root / 'events.jsonl'
        raw = path.read_bytes() if path.exists() else b''
        if raw and not raw.endswith(b'\n'):
            raise EvidenceError('journal has an incomplete final line; restore from verified backup')
        try:
            events = [json.loads(line, object_pairs_hook=_unique_object) for line in raw.decode('utf-8').splitlines()]
            state = replay(events)
            prefix = hashlib.sha256()
            for line, event in zip(raw.splitlines(keepends=True), events):
                if event['type'] == 'retrieval' and event['data']['revision'] != prefix.hexdigest():
                    raise EvidenceError('receipt journal digest does not match its history')
                prefix.update(line)
            for event in state['records'].values():
                data = event['data']
                content, _ = self._preserved(state['versions'][data['source_version']])
                if content is not None:
                    verify_excerpt(data, content)
        except (UnicodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
            raise EvidenceError(f'invalid journal: {exc}') from exc
        return events, state, hashlib.sha256(raw).hexdigest()

    def _path(self, path):
        rel = relative_path(path)
        resolved = (self.repo / rel).resolve()
        if not resolved.is_relative_to(self.repo) or resolved.is_relative_to(self.root):
            raise EvidenceError('source resolves outside repository or into the evidence store')
        relative_path(resolved.relative_to(self.repo).as_posix())
        return rel, resolved

    def _bytes(self, path, commit=None):
        rel, resolved = self._path(path)
        if commit is not None:
            if not isinstance(commit, str) or not re.fullmatch(r'[0-9a-f]{40}', commit):
                raise EvidenceError('historical capture requires a full lowercase Git SHA-1')
            try:
                object_name = f'{commit}:{rel}'
                # Hook bindings must not override the explicitly selected repository.
                env = {key: value for key, value in os.environ.items()
                       if not key.startswith('GIT_')}
                kind = subprocess.run(['git', '-C', str(self.repo), 'cat-file', '-t', object_name],
                                      env=env, capture_output=True, check=False, timeout=30)
                if kind.returncode != 0:
                    return None, 'unavailable'
                if kind.stdout.strip() != b'blob':
                    raise EvidenceError('historical source must be a Git blob, not a directory/tree')
                result = subprocess.run(['git', '-C', str(self.repo), 'cat-file', 'blob', object_name],
                                        env=env, capture_output=True, check=False, timeout=30)
            except (OSError, subprocess.TimeoutExpired):
                return None, 'unavailable'
            return (result.stdout, 'available') if result.returncode == 0 else (None, 'unavailable')
        try:
            return resolved.read_bytes(), 'available'
        except FileNotFoundError:
            return None, 'missing'
        except IsADirectoryError as exc:
            raise EvidenceError('source must be a file') from exc
        except OSError:
            return None, 'unavailable'

    def _blob(self, digest, content):
        directory = self.root / 'blobs'
        directory.mkdir(exist_ok=True)
        path = directory / digest
        if path.exists():
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise EvidenceError('existing preserved blob is corrupt; restore it before writing')
            return
        temp = directory / f'.{uuid.uuid4()}.tmp'
        try:
            with temp.open('xb') as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp, path)
        finally:
            temp.unlink(missing_ok=True)

    def _append(self, kind, data, content=None, expected_revision=None):
        with self._lock():
            events, _, revision = self._load()
            if expected_revision is not None and expected_revision != revision:
                raise EvidenceError('journal changed during retrieval; retry the request')
            event = {'schema': 2 if kind in {'retrieval', 'use'} else 1,
                     'seq': len(events) + 1, 'id': str(uuid.uuid4()),
                     'recorded_at': timestamp(self.clock()), 'type': kind, 'data': data}
            state = replay([*events, event])
            if kind in {'record', 'dependency'}:
                key = 'source_version' if kind == 'record' else 'evidence_version'
                preserved, status = self._preserved(state['versions'][data[key]])
                if preserved is None:
                    raise EvidenceError(f'annotation evidence is {status}')
                if kind == 'record':
                    verify_excerpt(data, preserved)
            if content is not None:
                self._blob(data['sha256'], content)
            with (self.root / 'events.jsonl').open('ab') as handle:
                handle.write((canonical(event) + '\n').encode('utf-8'))
                handle.flush()
                os.fsync(handle.fileno())
            return event

    def capture(self, source_id, path, kind, commit=None):
        rel, _ = self._path(path)
        content, availability = self._bytes(rel, commit)
        data = {'source_id': source_id, 'kind': kind, 'path': rel, 'commit': commit,
                'sha256': hashlib.sha256(content).hexdigest() if content is not None else None,
                'availability': availability}
        data['version_id'] = source_version(data)
        event = self._append('capture', data, content)
        return dict(data, id=event['id'], recorded_at=event['recorded_at'])

    def record(self, *, record_id, kind, source_version, section, statement,
               status, conditions, effective_at=None, supersedes=None):
        data = dict(record_id=record_id, kind=kind, source_version=source_version,
                    section=section, statement=statement, status=status, conditions=conditions,
                    effective_at=timestamp(effective_at) if effective_at is not None else None,
                    supersedes=supersedes)
        event = self._append('record', data)
        return dict(data, id=event['id'], recorded_at=event['recorded_at'])

    def depend(self, *, consumer, dependency, evidence_version, note):
        data = dict(consumer=consumer, dependency=dependency,
                    evidence_version=evidence_version, note=note)
        event = self._append('dependency', data)
        return dict(data, id=event['id'], recorded_at=event['recorded_at'])

    def _build(self, events, state, revision):
        temp = self.root / f'.index-{uuid.uuid4()}.sqlite'
        try:
            with closing(sqlite3.connect(temp)) as conn, conn:
                conn.executescript('''
                    CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                    CREATE TABLE versions (id TEXT PRIMARY KEY, source_id TEXT NOT NULL, data TEXT NOT NULL);
                    CREATE TABLE captures (seq INTEGER PRIMARY KEY, source_id TEXT NOT NULL,
                        version_id TEXT NOT NULL, path TEXT NOT NULL, recorded_at TEXT NOT NULL);
                    CREATE TABLE records (id TEXT PRIMARY KEY, record_id TEXT NOT NULL,
                        seq INTEGER UNIQUE NOT NULL, recorded_at TEXT NOT NULL,
                        effective_at TEXT, source_version TEXT NOT NULL, data TEXT NOT NULL);
                    CREATE INDEX records_identity ON records(record_id, seq);
                    CREATE TABLE dependencies (id TEXT PRIMARY KEY, consumer TEXT NOT NULL,
                        dependency TEXT NOT NULL, evidence_version TEXT NOT NULL, data TEXT NOT NULL);
                    CREATE TABLE receipts (id TEXT PRIMARY KEY, data TEXT NOT NULL);
                    CREATE TABLE uses (id TEXT PRIMARY KEY, receipt_id TEXT NOT NULL,
                        decision_revision TEXT NOT NULL, data TEXT NOT NULL,
                        UNIQUE(receipt_id, decision_revision));
                    CREATE VIEW edges AS
                        SELECT id AS consumer, source_version AS dependency FROM records
                        UNION SELECT consumer, dependency FROM dependencies
                        UNION SELECT consumer, evidence_version FROM dependencies;
                ''')
                conn.execute('INSERT INTO meta VALUES (?, ?)', ('revision', revision))
                conn.execute('INSERT INTO meta VALUES (?, ?)', ('schema', '2'))
                conn.executemany('INSERT INTO versions VALUES (?, ?, ?)',
                                 [(key, data['source_id'], canonical(data)) for key, data in sorted(state['versions'].items())])
                conn.executemany('INSERT INTO captures VALUES (?, ?, ?, ?, ?)', [
                    (event['seq'], event['data']['source_id'], event['data']['version_id'],
                     event['data']['path'], event['recorded_at']) for event in state['captures']])
                conn.executemany('INSERT INTO records VALUES (?, ?, ?, ?, ?, ?, ?)', [
                    (event['id'], event['data']['record_id'], event['seq'], event['recorded_at'],
                     event['data']['effective_at'], event['data']['source_version'], canonical(event['data']))
                    for event in state['records'].values()])
                conn.executemany('INSERT INTO dependencies VALUES (?, ?, ?, ?, ?)', [
                    (event['id'], event['data']['consumer'], event['data']['dependency'],
                     event['data']['evidence_version'], canonical(event['data']))
                    for event in state['dependencies']])
                conn.executemany('INSERT INTO receipts VALUES (?, ?)',
                                 [(key, canonical(event)) for key, event in state['receipts'].items()])
                conn.executemany('INSERT INTO uses VALUES (?, ?, ?, ?)',
                                 [(key, event['data']['receipt_id'], event['data']['decision_revision'], canonical(event))
                                  for key, event in state['uses'].items()])
            os.replace(temp, self.root / 'index.sqlite')
        finally:
            temp.unlink(missing_ok=True)

    @contextmanager
    def _read(self, force=False):
        with self._lock():
            events, state, revision = self._load()
            index = self.root / 'index.sqlite'
            fresh = False
            if index.exists() and not force:
                try:
                    conn = sqlite3.connect(index.as_uri() + '?mode=ro', uri=True)
                    try:
                        fresh = (conn.execute('SELECT value FROM meta WHERE key=?', ('revision',)).fetchone() == (revision,)
                                 and conn.execute('SELECT value FROM meta WHERE key=?', ('schema',)).fetchone() == ('2',))
                    finally:
                        conn.close()
                except sqlite3.DatabaseError:
                    fresh = False
            if not fresh:
                self._build(events, state, revision)
            conn = sqlite3.connect(index.as_uri() + '?mode=ro', uri=True)
            conn.row_factory = sqlite3.Row
            try:
                yield conn, state, revision
            finally:
                conn.close()

    def rebuild(self):
        with self._read(force=True) as (_, state, revision):
            return {'revision': revision, 'source_versions': len(state['versions'])}

    def _preserved(self, version):
        if version['sha256'] is None:
            return None, version['availability']
        try:
            content = (self.root / 'blobs' / version['sha256']).read_bytes()
        except FileNotFoundError:
            return None, 'missing'
        except OSError:
            return None, 'unavailable'
        if hashlib.sha256(content).hexdigest() != version['sha256']:
            return None, 'corrupt'
        return content, 'available'

    def _source(self, conn, version_id):
        row = conn.execute('SELECT data FROM versions WHERE id=?', (version_id,)).fetchone()
        if row is None:
            raise EvidenceError(f'unknown source version: {version_id}')
        data = json.loads(row['data'])
        _, preserved = self._preserved(data)
        current_path = conn.execute('SELECT path FROM captures WHERE source_id=? ORDER BY seq DESC LIMIT 1',
                                    (data['source_id'],)).fetchone()['path']
        content, current = self._bytes(current_path)
        if content is not None:
            current = 'unchanged' if hashlib.sha256(content).hexdigest() == data['sha256'] else 'changed'
        return dict(data, preserved=preserved, current=current, current_path=current_path)

    def source(self, version_id):
        with self._read() as (conn, _, _):
            return self._source(conn, version_id)

    def read_bytes(self, version_id):
        with self._read() as (_, state, _):
            if version_id not in state['versions']:
                raise EvidenceError(f'unknown source version: {version_id}')
            content, status = self._preserved(state['versions'][version_id])
            if content is None:
                raise EvidenceError(f'preserved source is {status}')
            return content

    @staticmethod
    def _record_row(row):
        return dict(json.loads(row['data']), id=row['id'], recorded_at=row['recorded_at'])

    def decision(self, record_id, known_at=None, as_of=None):
        known = timestamp(known_at or self.clock())
        effective = timestamp(as_of or self.clock())
        with self._read() as (conn, _, revision):
            rows = conn.execute('SELECT * FROM records WHERE record_id=? AND recorded_at<=? ORDER BY seq',
                                (record_id, known)).fetchall()
            if not rows:
                raise EvidenceError('no record revisions known at the requested time')
            history = [self._record_row(row) for row in rows]
            current, undated = temporal(history, effective)
            warnings = ['unknown_effective_time'] if undated else []
            verification = None
            if current:
                verification = self._source(conn, current['source_version'])
                if verification['current'] != 'unchanged':
                    warnings.append('source_needs_review')
                if verification['preserved'] != 'available':
                    warnings.append('preserved_source_unavailable')
            return {'record_id': record_id, 'known_at': known, 'as_of': effective,
                    'revision': revision, 'current': current,
                    'history': history, 'undated': undated,
                    'warnings': warnings, 'current_source_verification': verification}

    def _impact(self, conn, node_id):
        exists = conn.execute('SELECT id FROM versions WHERE id=? UNION SELECT id FROM records WHERE id=?',
                              (node_id, node_id)).fetchone()
        if exists is None:
            raise EvidenceError(f'unknown source version or record revision: {node_id}')
        rows = conn.execute('''
            WITH RECURSIVE affected(id) AS (
                SELECT consumer FROM edges WHERE dependency=?
                UNION SELECT edges.consumer FROM edges JOIN affected ON edges.dependency=affected.id
            )
            SELECT records.* FROM records JOIN affected ON records.id=affected.id
            WHERE records.id<>? ORDER BY records.record_id, records.seq
        ''', (node_id, node_id)).fetchall()
        return [dict(self._record_row(row), status='needs_review',
                     recorded_status=json.loads(row['data'])['status']) for row in rows]

    def impact(self, node_id):
        with self._read() as (conn, _, revision):
            return {'node_id': node_id, 'revision': revision,
                    'coverage': 'declared dependencies and cited source versions only',
                    'dependents': self._impact(conn, node_id)}

    def check(self):
        with self._read() as (conn, _, revision):
            findings = []
            for row in conn.execute('SELECT id FROM versions ORDER BY id'):
                source = self._source(conn, row['id'])
                if source['current'] != 'unchanged' or source['preserved'] != 'available':
                    findings.append({'version_id': row['id'], 'status': 'needs_review',
                                     'source': source, 'dependents': self._impact(conn, row['id'])})
            return {'revision': revision, 'coverage': 'registered sources and declared dependencies only',
                    'findings': findings}

    def retrieve(self, context=None, record_ids=None, known_at=None, as_of=None):
        """Persist observations over one journal revision, with explicit coverage."""
        observed = timestamp(self.clock())
        query = request({} if context is None else context, record_ids,
                        known_at or observed, as_of or observed)
        with self._read() as (conn, state, revision):
            results = candidates(state, query, revision)
            sources = {}

            def source(identity):
                if identity not in sources:
                    sources[identity] = self._source(conn, identity)
                return sources[identity]

            for row in results:
                current = row['current']
                warnings = ['unknown_effective_time'] if row['undated'] else []
                verification, corrections = None, []
                if current:
                    verification = source(current['source_version'])
                    if verification['current'] != 'unchanged':
                        warnings.append('source_needs_review')
                    if verification['preserved'] != 'available':
                        warnings.append('preserved_source_unavailable')
                    for identity in sorted(ancestors(state, current['id'])):
                        if identity in state['versions']:
                            observation = source(identity)
                            if observation['current'] != 'unchanged' or observation['preserved'] != 'available':
                                corrections.append(dict(id=identity, reason='source_needs_review', source=observation))
                        else:
                            latest = state['latest'][state['records'][identity]['data']['record_id']]
                            if latest != identity:
                                corrections.append(dict(id=identity, reason='dependency_superseded', replacement=latest))
                if corrections:
                    warnings.append('dependencies_need_review')
                row.update(warnings=warnings, current_source_verification=verification, corrections=corrections)
        return self._append('retrieval', dict(request=query, observed_at=observed,
                                             revision=revision, results=results), expected_revision=revision)

    def use(self, receipt_id, decision_revision, selections):
        """Record reported evidence use; never imply causality or authorization."""
        return self._append('use', dict(receipt_id=receipt_id, decision_revision=decision_revision,
                                       selections=selections))

    def receipt(self, receipt_id):
        with self._read() as (conn, _, revision):
            row = conn.execute('SELECT data FROM receipts WHERE id=?', (receipt_id,)).fetchone()
            if row is None:
                raise EvidenceError('unknown retrieval receipt')
            receipt = json.loads(row['data'])
            uses = []
            for row in conn.execute('SELECT data FROM uses WHERE receipt_id=? ORDER BY rowid', (receipt_id,)):
                event = json.loads(row['data'])
                assessed = {item['revision_id'] for item in event['data']['selections']}
                uses.append(dict(event=event, unassessed=sorted(selectable(receipt) - assessed)))
            return dict(receipt=receipt, uses=uses, revision=revision,
                        selectable=sorted(selectable(receipt)),
                        coverage='registered records and declared dependencies; observations are not live verification')

    def export(self):
        """Portable graph contract, not a connection to or authority grant for Neo4j."""
        with self._read() as (conn, state, revision):
            nodes, edges = {}, []
            for version_id, data in sorted(state['versions'].items()):
                source_id = 'source:' + data['source_id']
                nodes[source_id] = {'id': source_id, 'label': 'Source', 'source_id': data['source_id']}
                nodes[version_id] = dict(data, id=version_id, label='SourceVersion')
                edges.append({'id': 'version-of:' + version_id, 'from': version_id,
                              'to': source_id, 'type': 'VERSION_OF'})
            for row in conn.execute('SELECT * FROM records ORDER BY id'):
                data = self._record_row(row)
                nodes[row['id']] = dict(data, label='RecordRevision')
                edges.append({'id': 'based-on:' + row['id'], 'from': row['id'],
                              'to': row['source_version'], 'type': 'BASED_ON', 'section': data['section']})
                if data['supersedes']:
                    edges.append({'id': 'supersedes:' + row['id'], 'from': row['id'],
                                  'to': data['supersedes'], 'type': 'SUPERSEDES',
                                  'evidence_version': data['source_version']})
            for event in state['dependencies']:
                data = event['data']
                edges.append({'id': event['id'], 'from': data['consumer'], 'to': data['dependency'],
                              'type': 'DEPENDS_ON', 'evidence_version': data['evidence_version'],
                              'note': data['note'], 'recorded_at': event['recorded_at']})
                edges.append({'id': 'declaration-evidence:' + event['id'], 'from': data['consumer'],
                              'to': data['evidence_version'], 'type': 'BASED_ON',
                              'declaration_id': event['id']})
            for identity, event in state['receipts'].items():
                nodes[identity] = dict(id=identity, label='RetrievalReceipt', event=event)
                for position, result in enumerate(event['data']['results']):
                    if result['current']:
                        edges.append(dict(id=f'retrieved:{identity}:{position}', type='RETRIEVED',
                                          **{'from': identity, 'to': result['current']['id']}, position=position,
                                          applicability=result['applicability']['status']))
            for identity, event in state['uses'].items():
                data = event['data']
                nodes[identity] = dict(id=identity, label='EvidenceUse', event=event)
                for relation, target in [('FOR_DECISION', data['decision_revision']), ('FROM_RECEIPT', data['receipt_id'])]:
                    edges.append(dict(id=f'{relation}:{identity}', type=relation, **{'from': identity, 'to': target}))
                for item in data['selections']:
                    edges.append(dict(id=f'assessed:{identity}:{item["revision_id"]}', type='ASSESSED',
                                      **{'from': identity, 'to': item['revision_id']},
                                      disposition=item['disposition'], reason=item['reason']))
            return {'schema': 2, 'revision': revision,
                    'nodes': [nodes[key] for key in sorted(nodes)],
                    'edges': sorted(edges, key=lambda edge: edge['id'])}
