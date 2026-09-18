"""Service-private schema-v4 persistence. OS ownership is the write boundary.

These methods are not RPC operations and do not authenticate callers. The
supervisor verifies authority while holding ``transaction()`` for acceptance;
the store independently enforces identity, revision, validity and byte custody.
"""
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
import os
import sqlite3
import threading
import uuid

from ..contract import canonical_json_bytes as encoded, parse_canonical_json
from ..journal_snapshot import encode_assessment_snapshot
from ..evidence import parse_proposed_artifact, InspectedEvidence, compare_n1_evidence
from ..policy import N1_ARTIFACT_ROLES
from .files import archive_bytes, read_regular
from .protocol import ExecutionRecord, ValidatedEvidence, digest, fields, identity, parse_request, sha256

_SCHEMA = '''
CREATE TABLE IF NOT EXISTS campaigns (
 attempt_id TEXT PRIMARY KEY, contract_sha256 TEXT NOT NULL, trust_domain_sha256 TEXT NOT NULL,
 validity TEXT NOT NULL CHECK(validity IN ('VALID','VOID')), reason TEXT,
 event_head TEXT NOT NULL, event_count INTEGER NOT NULL, policy_sha256 TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS executions (
 execution_id TEXT PRIMARY KEY, attempt_id TEXT NOT NULL UNIQUE REFERENCES campaigns(attempt_id),
 checkpoint TEXT NOT NULL CHECK(checkpoint='N1'), plan_bytes BLOB NOT NULL, request_bytes BLOB NOT NULL,
 plan_sha256 TEXT NOT NULL, request_sha256 TEXT NOT NULL, release_sha256 TEXT NOT NULL,
 state TEXT NOT NULL CHECK(state IN ('DISPATCHED','START_INTENT','RUNNING','CAPTURED','ATTESTED','ABORTED','IN_DOUBT')),
 revision INTEGER NOT NULL, container_id TEXT, authorized_at_utc TEXT,
 captured_payload BLOB, attestation_sha256 TEXT,
 UNIQUE(attempt_id,checkpoint));
CREATE TABLE IF NOT EXISTS events (
 attempt_id TEXT NOT NULL REFERENCES campaigns(attempt_id), sequence INTEGER NOT NULL,
 execution_id TEXT NOT NULL REFERENCES executions(execution_id), body BLOB NOT NULL,
 previous_sha256 TEXT NOT NULL, sha256 TEXT NOT NULL UNIQUE, PRIMARY KEY(attempt_id,sequence));
CREATE TABLE IF NOT EXISTS objects (
 sha256 TEXT PRIMARY KEY, byte_length INTEGER NOT NULL, archive_location TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS execution_objects (
 execution_id TEXT NOT NULL REFERENCES executions(execution_id), role TEXT NOT NULL,
 sha256 TEXT NOT NULL REFERENCES objects(sha256), PRIMARY KEY(execution_id,role));
CREATE TABLE IF NOT EXISTS proposed_artifacts (
 execution_id TEXT NOT NULL REFERENCES executions(execution_id), role TEXT NOT NULL,
 sha256 TEXT NOT NULL REFERENCES objects(sha256), PRIMARY KEY(execution_id,role,sha256));
CREATE TABLE IF NOT EXISTS assessments (
 execution_id TEXT PRIMARY KEY REFERENCES executions(execution_id), result_sha256 TEXT NOT NULL REFERENCES objects(sha256),
 authentication_sha256 TEXT NOT NULL REFERENCES objects(sha256), cutoff_bytes BLOB NOT NULL,
 commit_event_sha256 TEXT NOT NULL REFERENCES events(sha256), receipt_bytes BLOB NOT NULL);
'''


def instant(value):
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError('trusted aware instant required')
    return value.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')


def _time(value):
    if type(value) is not str or not value.endswith('Z'):
        raise ValueError('UTC execution timestamp required')
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    return result


def _capture_payload(row, facts, *, capture_head, capture_revision, dispatch_head):
    plan = parse_canonical_json(row['plan_bytes'], label='plan')
    payload = {key: plan[key] for key in ('attempt_id', 'contract_sha256', 'trust_domain_sha256',
        'execution_release_sha256', 'exact_depth_approval_sha256', 'authority_class')}
    payload.update({key: facts[key] for key in ('service_id', 'profile_sha256', 'runtime_manifest_sha256',
        'worker_image_digest', 'authorized_at_utc', 'started_utc', 'completed_utc', 'artifacts', 'observations')})
    payload.update(schema='qualification_execution_attestation_payload/v1', scope='ATTEST_CHECKPOINT_EXECUTION',
        execution_id=row['execution_id'], checkpoint='N1', completion='COMPLETED', plan_sha256=row['plan_sha256'],
        retained_bundle_sha256=parse_request(row['request_bytes'])['bundle_sha256'],
        dispatch_event_sha256=dispatch_head, capture_event_sha256=capture_head, capture_revision=capture_revision)
    return encoded(payload)


def _assessment_receipt(row, data, head):
    return encoded(dict(schema='qualification_assessment_receipt/v1', attempt_id=row['attempt_id'],
        execution_id=row['execution_id'], result_sha256=data['result_sha256'],
        authentication_sha256=data['authentication_sha256'], cutoff_sha256=data['cutoff_sha256'],
        commit_event_sha256=head, committed_at_utc=data['committed_at_utc']))


class ExecutionStore:
    def __init__(self, path, *, installation_dir=None):
        self.path = Path(path)
        self.installation_dir = Path(installation_dir) if installation_dir is not None else self.path.parent / 'installation'
        self.archive_dir = self.path.parent / 'objects'
        self._local = threading.local()
        if self.path.is_symlink():
            raise ValueError('journal link forbidden')
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = self._connect()
        try:
            version = connection.execute('PRAGMA user_version').fetchone()[0]
            if version not in (0, 4):
                raise ValueError('unsupported journal schema; no in-flight migration')
            if version == 0:
                if connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchone():
                    raise ValueError('unknown journal schema; no migration')
                connection.execute('PRAGMA journal_mode=WAL')
                connection.executescript('BEGIN IMMEDIATE;\n' + _SCHEMA + '\nPRAGMA user_version=4;\nCOMMIT;')
                os.chmod(self.path, 0o600)
        finally:
            connection.close()
        with self.transaction() as connection:
            # Derive the expected layout from the one schema owner. An empty
            # prototype with the same version number is not a valid journal.
            reference = sqlite3.connect(':memory:')
            try:
                reference.executescript(_SCHEMA)
                query = 'SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name'
                expected = reference.execute(query).fetchall()
                actual = [tuple(row) for row in connection.execute(query)]
                if actual != expected:
                    raise ValueError('unsupported journal schema layout; no migration')
            finally:
                reference.close()
            self._integrity(connection)

    def _connect(self):
        connection = sqlite3.connect(self.path, isolation_level=None, timeout=30)
        connection.row_factory = sqlite3.Row
        connection.execute('PRAGMA foreign_keys=ON')
        connection.execute('PRAGMA synchronous=FULL')
        return connection

    @contextmanager
    def transaction(self):
        """Trusted service may keep revalidation and assessment in one short lock."""
        current = getattr(self._local, 'connection', None)
        if current is not None:
            yield current
            return
        connection = self._connect()
        self._local.connection = connection
        try:
            connection.execute('BEGIN IMMEDIATE')
            yield connection
            connection.execute('COMMIT')
        except BaseException:
            if connection.in_transaction:
                connection.execute('ROLLBACK')
            raise
        finally:
            self._local.connection = None
            connection.close()

    def _row(self, connection, execution_id):
        row = connection.execute('SELECT e.*,c.validity,c.event_count,c.event_head,c.contract_sha256,c.trust_domain_sha256,c.policy_sha256 '
            'FROM executions e JOIN campaigns c USING(attempt_id) WHERE execution_id=?', (execution_id,)).fetchone()
        if row is None:
            raise ValueError('unknown execution')
        return row

    @staticmethod
    def _record(row):
        return ExecutionRecord(row['execution_id'], row['attempt_id'], row['state'], row['revision'],
                               row['plan_sha256'], row['attestation_sha256'])

    @staticmethod
    def _check(row, expected_revision, state):
        if row['validity'] != 'VALID':
            raise ValueError('VOID campaign')
        if row['revision'] != expected_revision:
            raise ValueError('journal revision conflict')
        if row['state'] not in state:
            raise ValueError('illegal execution transition')

    def _append(self, connection, row, kind, state, data):
        revision = row['event_count'] + 1
        body = encoded(dict(kind=kind, execution_id=row['execution_id'], attempt_id=row['attempt_id'],
                            revision=revision, state=state, data=data))
        head = sha256(row['event_head'].encode('ascii') + body)
        connection.execute('INSERT INTO events VALUES(?,?,?,?,?,?)',
            (row['attempt_id'], revision, row['execution_id'], body, row['event_head'], head))
        connection.execute('UPDATE campaigns SET event_head=?,event_count=? WHERE attempt_id=?',
            (head, revision, row['attempt_id']))
        connection.execute('UPDATE executions SET state=?,revision=? WHERE execution_id=?',
            (state, revision, row['execution_id']))
        return head

    def _object(self, connection, execution_id, role, raw):
        identity(role)
        digest_value = archive_bytes(self.archive_dir, raw)
        connection.execute('INSERT OR IGNORE INTO objects VALUES(?,?,?)', (digest_value, len(raw), digest_value))
        existing = connection.execute('SELECT sha256 FROM execution_objects WHERE execution_id=? AND role=?',
                                      (execution_id, role)).fetchone()
        if existing is not None and existing[0] != digest_value:
            raise ValueError('immutable object membership conflict')
        connection.execute('INSERT OR IGNORE INTO execution_objects VALUES(?,?,?)', (execution_id, role, digest_value))
        return digest_value

    def archive_object(self, execution_id, role, raw):
        with self.transaction() as connection:
            self._row(connection, execution_id)
            return self._object(connection, execution_id, role, raw)

    def reserve(self, request_bytes, plan_bytes, *, now):
        request = parse_request(request_bytes)
        if request['operation'] != 'SUBMIT_N1':
            raise ValueError('N1 submit required')
        plan = parse_canonical_json(plan_bytes, label='plan')
        if (plan.get('schema') != 'qualification_checkpoint_plan/v2' or plan.get('checkpoint') != 'N1'
                or plan.get('attempt_id') != request['attempt_id']):
            raise ValueError('N1 plan binding differs')
        for name in ('contract_sha256', 'trust_domain_sha256', 'execution_release_sha256','policy_sha256'):
            digest(plan[name])
        with self.transaction() as connection:
            previous = connection.execute('SELECT execution_id FROM executions WHERE attempt_id=?',
                                          (request['attempt_id'],)).fetchone()
            if previous:
                row = self._row(connection, previous[0])
                if row['request_bytes'] != request_bytes or row['plan_bytes'] != plan_bytes:
                    raise ValueError('approved attempt binding conflict')
                return self._record(row)
            execution_id = str(uuid.uuid4())
            connection.execute('INSERT INTO campaigns VALUES(?,?,?,?,?,?,?,?)',
                (request['attempt_id'], plan['contract_sha256'], plan['trust_domain_sha256'], 'VALID', None, '0' * 64, 0,plan['policy_sha256']))
            connection.execute('INSERT INTO executions VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                (execution_id, request['attempt_id'], 'N1', plan_bytes, request_bytes, sha256(plan_bytes),
                 sha256(request_bytes), plan['execution_release_sha256'], 'DISPATCHED', 0, None, None, None, None))
            self._object(connection, execution_id, 'plan', plan_bytes)
            row = self._row(connection, execution_id)
            self._append(connection, row, 'DISPATCHED', 'DISPATCHED', dict(
                request_sha256=sha256(request_bytes), plan_sha256=sha256(plan_bytes), reserved_at_utc=instant(now)))
            return self._record(self._row(connection, execution_id))

    def record_container(self, execution_id, container_id, *, expected_revision):
        digest(container_id)
        with self.transaction() as connection:
            row = self._row(connection, execution_id)
            self._check(row, expected_revision, ('DISPATCHED',))
            if row['container_id'] is not None:
                raise ValueError('container already recorded; no replacement')
            connection.execute('UPDATE executions SET container_id=? WHERE execution_id=?', (container_id, execution_id))
            self._append(connection, row, 'CONTAINER', 'DISPATCHED', dict(container_id=container_id))
            return self._record(self._row(connection, execution_id))

    def record_start_intent(self, execution_id, *, expected_revision, now):
        with self.transaction() as connection:
            row = self._row(connection, execution_id)
            self._check(row, expected_revision, ('DISPATCHED',))
            if row['container_id'] is None or row['authorized_at_utc'] is not None:
                raise ValueError('start transition requires exact unstarted container')
            authorized = instant(now)
            connection.execute('UPDATE executions SET authorized_at_utc=? WHERE execution_id=?', (authorized, execution_id))
            self._append(connection, row, 'START_INTENT', 'START_INTENT', dict(authorized_at_utc=authorized))
            return self._record(self._row(connection, execution_id))

    def record_running(self, execution_id, *, expected_revision, now):
        with self.transaction() as connection:
            row = self._row(connection, execution_id)
            self._check(row, expected_revision, ('START_INTENT',))
            self._append(connection, row, 'RUNNING', 'RUNNING', dict(observed_at_utc=instant(now)))
            return self._record(self._row(connection, execution_id))

    def record_capture(self, execution_id, capture_bytes, *, expected_revision):
        facts = fields(parse_canonical_json(capture_bytes, label='capture'), {
            'schema', 'container_id', 'service_id', 'profile_sha256', 'runtime_manifest_sha256',
            'worker_image_digest', 'authorized_at_utc', 'started_utc', 'completed_utc', 'artifacts', 'observations'})
        if facts['schema'] != 'qualification_capture/v1':
            raise ValueError('capture schema differs')
        with self.transaction() as connection:
            row = self._row(connection, execution_id)
            self._check(row, expected_revision, ('RUNNING',))
            if facts['container_id'] != row['container_id'] or facts['authorized_at_utc'] != row['authorized_at_utc']:
                raise ValueError('capture launch identity differs')
            if not _time(facts['authorized_at_utc']) <= _time(facts['started_utc']) <= _time(facts['completed_utc']):
                raise ValueError('contradictory execution timestamps')
            if type(facts['artifacts']) is not list or [item.get('role') for item in facts['artifacts']] != ['plan', 'worker_result']:
                raise ValueError('closed ordered capture artifact roles required')
            for item in facts['artifacts']:
                fields(item, {'role', 'sha256', 'byte_length'})
                digest(item['sha256'])
                if type(item['byte_length']) is not int or item['byte_length'] <= 0:
                    raise ValueError('artifact byte length required')
                raw = read_regular(self.archive_dir, item['sha256'], limit=item['byte_length'])
                if len(raw) != item['byte_length'] or sha256(raw) != item['sha256']:
                    raise ValueError('capture archive integrity differs')
                self._object(connection, execution_id, item['role'], raw)
            if facts['artifacts'][0]['sha256'] != row['plan_sha256']:
                raise ValueError('captured plan differs')
            observations = fields(facts['observations'], {'exit_code', 'oom_killed', 'supervisor_wall_ns',
                'worker_compute_wall_ns', 'worker_cpu_ns', 'worker_peak_memory_bytes'})
            if type(observations['exit_code']) is not int or observations['exit_code'] != 0 or observations['oom_killed'] is not False:
                raise ValueError('abnormal execution cannot complete')
            for name in ('supervisor_wall_ns', 'worker_compute_wall_ns', 'worker_cpu_ns', 'worker_peak_memory_bytes'):
                if type(observations[name]) is not int or observations[name] < 0:
                    raise ValueError('execution observations must be nonnegative integers')
            plan = parse_canonical_json(row['plan_bytes'], label='plan')
            budget = plan['budget']
            if (observations['worker_compute_wall_ns'] >= budget['maximum_wall_seconds'] * 1000000000
                    or observations['worker_cpu_ns'] > budget['maximum_cpu_seconds'] * 1000000000
                    or observations['worker_peak_memory_bytes'] > budget['maximum_memory_bytes']):
                raise ValueError('capture exceeds frozen budget')
            head = self._append(connection, row, 'CAPTURED', 'CAPTURED', facts)
            dispatch = connection.execute("SELECT sha256 FROM events WHERE execution_id=? AND sequence=1", (execution_id,)).fetchone()[0]
            payload = _capture_payload(row, facts, capture_head=head, capture_revision=row['event_count'] + 1,
                                       dispatch_head=dispatch)
            connection.execute('UPDATE executions SET captured_payload=? WHERE execution_id=?', (payload, execution_id))
            return self._record(self._row(connection, execution_id))

    def get_captured_payload(self, execution_id):
        with self.transaction() as connection:
            row = self._row(connection, execution_id)
            if row['state'] not in ('CAPTURED', 'ATTESTED') or row['captured_payload'] is None:
                raise ValueError('no durable capture')
            return bytes(row['captured_payload'])

    def execution_rows(self):
        with self.transaction() as connection:
            return [dict(self._row(connection, row[0])) for row in connection.execute('SELECT execution_id FROM executions')]

    def context(self, execution_id, *, now):
        from .admission import verify_bundle
        from .keys import load_keys
        with self.transaction() as connection:
            row = self._row(connection, execution_id)
            bundle = parse_request(row['request_bytes'])['bundle_sha256']
            release = read_regular(self.installation_dir, 'release.json', limit=16 * 1024 * 1024)
            authority = parse_canonical_json(release, label='release')['authority_class']
            keys = load_keys(read_regular(self.installation_dir, 'keys.json', limit=1024 * 1024), authority_class=authority)
            context = verify_bundle(self.path.parent / 'bundles' / bundle, release, keys, now)
            if context.bundle_sha256 != bundle or context.attempt_id != row['attempt_id']:
                raise ValueError('stored original context differs')
            return context, keys

    def cancellation_enrollment(self, execution_id):
        """Original enrollment only; no executable context or current authority.

        Cancellation outlives admission. Reconstruct signed enrollment at the
        durable reservation time, then give the service the *unmodified current*
        keys for its separate current-time VOID approval verification.
        """
        from dataclasses import replace
        from .admission import verify_bundle
        from .keys import load_keys
        with self.transaction() as connection:
            row = self._row(connection, execution_id)
            first = connection.execute('SELECT body FROM events WHERE attempt_id=? AND sequence=1',
                                       (row['attempt_id'],)).fetchone()
            event = parse_canonical_json(first[0], label='original reservation')
            if event['kind'] != 'DISPATCHED' or event['execution_id'] != execution_id:
                raise ValueError('original reservation differs')
            bundle = parse_request(row['request_bytes'])['bundle_sha256']
            release = read_regular(self.installation_dir, 'release.json', limit=16*1024*1024)
            authority = parse_canonical_json(release, label='release')['authority_class']
            keys = load_keys(read_regular(self.installation_dir, 'keys.json', limit=1024*1024), authority_class=authority)
            historical_keys = {name: replace(key, revoked_at=None) for name,key in keys.items()}
            context = verify_bundle(self.path.parent/'bundles'/bundle, release, historical_keys,
                                    _time(event['data']['reserved_at_utc']))
            if (context.bundle_sha256 != bundle or context.attempt_id != row['attempt_id']
                    or context.contract.contract_sha256 != row['contract_sha256']
                    or context.domain.sha256 != row['trust_domain_sha256']):
                raise ValueError('original cancellation enrollment differs')
            return dict(contract_sha256=row['contract_sha256'], authority_class=context.domain.authority_class,
                freeze_key_ids=context.domain.freeze_key_ids,
                trusted_key_sha256=dict(context.domain.trusted_key_sha256)), keys

    def publish_attestation(self, execution_id, attestation_bytes, *, expected_revision):
        envelope = fields(parse_canonical_json(attestation_bytes, label='attestation'), {'schema', 'payload', 'signature'})
        if envelope['schema'] != 'qualification_execution_attestation/v1':
            raise ValueError('attestation schema differs')
        with self.transaction() as connection:
            row = self._row(connection, execution_id)
            self._check(row, expected_revision, ('CAPTURED',))
            if encoded(envelope['payload']) != row['captured_payload']:
                raise ValueError('attestation payload differs from durable capture')
            digest_value = self._object(connection, execution_id, 'attestation', attestation_bytes)
            connection.execute('UPDATE executions SET attestation_sha256=? WHERE execution_id=?', (digest_value, execution_id))
            self._append(connection, row, 'ATTESTED', 'ATTESTED', dict(attestation_sha256=digest_value))
            return self._record(self._row(connection, execution_id))

    def record_abort(self, execution_id, reason, *, uncertain):
        if type(uncertain) is not bool or type(reason) is not str or not reason:
            raise ValueError('explicit bounded abort reason required')
        with self.transaction() as connection:
            row = self._row(connection, execution_id)
            if row['state'] not in ('DISPATCHED', 'START_INTENT', 'RUNNING'):
                raise ValueError('illegal abort transition')
            state = 'IN_DOUBT' if uncertain else 'ABORTED'
            self._append(connection, row, state, state, dict(reason=reason))
            return self._record(self._row(connection, execution_id))

    def void(self, attempt_id, reason, approval_bytes, *, now):
        parse_canonical_json(approval_bytes, label='validated VOID approval')
        with self.transaction() as connection:
            status = self._status(connection, attempt_id)
            row = self._row(connection, status['execution_id'])
            if row['validity'] == 'VOID':
                raise ValueError('already VOID')
            connection.execute("UPDATE campaigns SET validity='VOID',reason=? WHERE attempt_id=?", (reason, attempt_id))
            self._object(connection, row['execution_id'], 'void_approval', approval_bytes)
            self._append(connection, row, 'VOID', row['state'], dict(reason=reason,
                approval_sha256=sha256(approval_bytes), voided_at_utc=instant(now)))
            return encoded(self._status(connection, attempt_id))

    def _status(self, connection, attempt_id):
        row = connection.execute('SELECT execution_id FROM executions WHERE attempt_id=?', (attempt_id,)).fetchone()
        if row is None:
            raise KeyError('unknown attempt')
        row = self._row(connection, row[0])
        kinds = [parse_canonical_json(event[0], label='event')['kind'] for event in
                 connection.execute('SELECT body FROM events WHERE attempt_id=? ORDER BY sequence', (attempt_id,))]
        status = dict(attempt_id=attempt_id, execution_id=row['execution_id'], state=row['state'],
            validity=row['validity'], revision=row['revision'], plan_sha256=row['plan_sha256'],
            attestation_sha256=row['attestation_sha256'], container_id=row['container_id'],
            launch_intent_count=kinds.count('START_INTENT'), attestation_count=kinds.count('ATTESTED'),
              next_checkpoint='UNSUPPORTED')
        preflight=connection.execute('SELECT sha256 FROM execution_objects WHERE execution_id=? AND role=?',
            (row['execution_id'],'preflight')).fetchone()
        if preflight is not None:
            status['preflight_sha256']=preflight[0]
        assessment = connection.execute('SELECT * FROM assessments WHERE execution_id=?', (row['execution_id'],)).fetchone()
        if assessment is not None:
            result = parse_canonical_json(self.fetch(attempt_id, assessment['result_sha256']), label='committed result')
            status.update(result_sha256=assessment['result_sha256'], cutoff_sha256=sha256(assessment['cutoff_bytes']),
                          authentication_sha256=assessment['authentication_sha256'],
                          receipt_sha256=sha256(assessment['receipt_bytes']),
                          completion=result['completion'], verdict=result['verdict'],
                          n1_decision=result['checkpoint_assessment']['decision'])
        return status

    def status(self, attempt_id):
        with self.transaction() as connection:
            return encoded(self._status(connection, attempt_id))

    def retry_assessment(self, attempt_id, result_sha256, authentication_bytes):
        """Historical equality only; the service authenticates transport first.

        No current approval checks or new signatures belong in this branch. The
        service separately reports current policy eligibility on the response.
        """
        digest(result_sha256)
        with self.transaction() as connection:
            status = self._status(connection, attempt_id)
            saved = connection.execute('SELECT * FROM assessments WHERE execution_id=?',
                                       (status['execution_id'],)).fetchone()
            if saved is None:
                return None
            if (saved['result_sha256'] != result_sha256
                    or saved['authentication_sha256'] != sha256(authentication_bytes)
                    or self.fetch(attempt_id, saved['authentication_sha256']) != authentication_bytes):
                raise ValueError('assessment idempotency conflict')
            # Fetch verifies retained content, including after a service restart.
            self.fetch(attempt_id, saved['result_sha256'])
            return encoded(dict(receipt=parse_canonical_json(saved['receipt_bytes'],label='receipt'),
                                validity=status['validity'],historical=True))

    def commit_assessment(self, evidence, authentication_bytes, *, now):
        if type(evidence) is not ValidatedEvidence:
            raise TypeError('validated evidence value required')
        doc = parse_canonical_json(evidence.result_bytes,label='assessment')
        with self.transaction() as connection:
            retry = self.retry_assessment(doc['attempt_id'],sha256(evidence.result_bytes),authentication_bytes)
            if retry is not None:
                return retry
            inspected = InspectedEvidence(evidence.result_bytes,evidence.output_bytes_by_role)
            compare_n1_evidence(inspected,expected=inspected)
            entry = connection.execute('SELECT execution_id FROM executions WHERE attempt_id=?',
                                       (doc['attempt_id'],)).fetchone()
            row = self._row(connection,entry[0])
            self._check(row,evidence.expected_revision,('ATTESTED',))
            snapshot = self._snapshot(connection,row['attempt_id'])
            if (snapshot != evidence.output_bytes_by_role['attempt_journal']
                    or sha256(snapshot) != evidence.journal_snapshot_sha256
                    or doc['journal_snapshot_sha256'] != sha256(snapshot)):
                raise ValueError('assessment precommit snapshot differs')
            expected = dict(contract_sha256=row['contract_sha256'],trust_domain_sha256=row['trust_domain_sha256'],
                policy_sha256=row['policy_sha256'],journal_revision=row['revision'],
                execution_attestations={'N1':row['attestation_sha256']},
                checkpoint_assessment=dict(checkpoint='N1',decision=evidence.n1_decision))
            if (any(encoded(doc.get(key)) != encoded(value) for key,value in expected.items())
                    or evidence.attestation_sha256 != row['attestation_sha256']):
                raise ValueError('assessment identity/revision/decision binding differs')
            auth = fields(parse_canonical_json(authentication_bytes,label='verified authentication'),{'schema','payload','signature'})
            expected_auth = dict(schema='qualification_result_authentication_payload/v2',scope='ATTEST_E1_RESULT',
                authority_class=parse_canonical_json(row['plan_bytes'],label='plan')['authority_class'],
                attempt_id=row['attempt_id'],contract_sha256=row['contract_sha256'],trust_domain_sha256=row['trust_domain_sha256'],
                journal_revision=row['revision'],result_sha256=sha256(evidence.result_bytes))
            if auth['schema'] != 'qualification_result_authentication/v2' or encoded(auth['payload']) != encoded(expected_auth):
                raise ValueError('assessment authentication binding differs')
            for item in doc['outputs']:
                raw = evidence.output_bytes_by_role[item['role']]
                member = connection.execute('SELECT 1 FROM proposed_artifacts WHERE execution_id=? AND role=? AND sha256=?',
                    (row['execution_id'],item['role'],item['sha256'])).fetchone()
                if member is None or self.fetch_candidate(row['attempt_id'],item['sha256']) != raw:
                    raise ValueError('candidate result output membership differs')
            members = {item['role']:item['sha256'] for item in connection.execute(
                'SELECT role,sha256 FROM execution_objects WHERE execution_id=?',(row['execution_id'],))}
            if members.get('context_contract') != row['contract_sha256']:
                raise ValueError('original frozen contract membership required')
            contract = parse_canonical_json(self.fetch(row['attempt_id'],row['contract_sha256']),label='contract')
            stage = next(item for item in contract['replay']['stages'] if item['name']=='N1')
            cutoff = stage['max_failures_per_population']
            if type(cutoff) is not int or cutoff < 0:
                raise ValueError('frozen N1 cutoff required')
            plan = parse_canonical_json(row['plan_bytes'],label='plan')
            cutoff_bytes = encoded(dict(schema='qualification_n1_cutoff/v1',attempt_id=row['attempt_id'],
                contract_sha256=row['contract_sha256'],trust_domain_sha256=row['trust_domain_sha256'],
                n1_attestation_sha256=row['attestation_sha256'],n1_decision=evidence.n1_decision,
                decision_sha256=sha256(encoded(doc['checkpoint_assessment'])),
                cutoffs={item['population']:cutoff for item in plan['depths']}))
            for role,raw in evidence.output_bytes_by_role.items():
                self._object(connection,row['execution_id'],role,raw)
            result_digest = self._object(connection,row['execution_id'],'result',evidence.result_bytes)
            auth_digest = self._object(connection,row['execution_id'],'result_authentication',authentication_bytes)
            cutoff_digest = self._object(connection,row['execution_id'],'cutoff',cutoff_bytes)
            data = dict(result_sha256=result_digest,authentication_sha256=auth_digest,cutoff_sha256=cutoff_digest,
                        outputs=doc['outputs'],committed_at_utc=instant(now))
            head = self._append(connection,row,'ASSESSMENT','ATTESTED',data)
            receipt = _assessment_receipt(row,data,head)
            self._object(connection,row['execution_id'],'assessment_receipt',receipt)
            connection.execute('INSERT INTO assessments VALUES(?,?,?,?,?,?)',
                (row['execution_id'],result_digest,auth_digest,cutoff_bytes,head,receipt))
            return encoded(dict(receipt=parse_canonical_json(receipt,label='receipt'),validity=row['validity'],historical=False))

    def _snapshot(self, connection, attempt_id):
        campaign = connection.execute('SELECT * FROM campaigns WHERE attempt_id=?',(attempt_id,)).fetchone()
        if campaign is None: raise KeyError('unknown attempt')
        executions = [dict(checkpoint=row['checkpoint'],execution_id=row['execution_id'],execution_revision=row['revision'],
                           state=row['state'],plan_sha256=row['plan_sha256'],attestation_sha256=row['attestation_sha256'])
                      for row in connection.execute('SELECT * FROM executions WHERE attempt_id=?',(attempt_id,))]
        return encode_assessment_snapshot(attempt_id=attempt_id,contract_sha256=campaign['contract_sha256'],
            trust_domain_sha256=campaign['trust_domain_sha256'],policy_sha256=campaign['policy_sha256'],
            validity=campaign['validity'],campaign_revision=campaign['event_count'],event_head=campaign['event_head'],executions=executions)

    def snapshot_for_assessment(self, attempt_id):
        current = getattr(self._local,'connection',None)
        if current is not None: return self._snapshot(current,attempt_id)
        connection = self._connect()
        try:
            connection.execute('BEGIN')
            return self._snapshot(connection,attempt_id)
        finally:
            if connection.in_transaction: connection.execute('ROLLBACK')
            connection.close()

    def store_proposed_artifact(self, attempt_id, role, payload):
        doc = parse_proposed_artifact(role,payload)
        with self.transaction() as connection:
            entry = connection.execute('SELECT execution_id FROM executions WHERE attempt_id=?',(attempt_id,)).fetchone()
            if entry is None: raise KeyError('unknown attempt')
            row = self._row(connection,entry[0])
            self._check(row,row['revision'],('ATTESTED',))
            for name in ('attempt_id','contract_sha256','trust_domain_sha256','policy_sha256','execution_id'):
                if name in doc and doc[name] != row[name]: raise ValueError('candidate attempt membership differs')
            if role == 'attempt_journal' and payload != self._snapshot(connection,attempt_id):
                raise ValueError('candidate snapshot differs')
            digest_value = archive_bytes(self.archive_dir,payload)
            connection.execute('INSERT OR IGNORE INTO objects VALUES(?,?,?)',(digest_value,len(payload),digest_value))
            connection.execute('INSERT OR IGNORE INTO proposed_artifacts VALUES(?,?,?)',(row['execution_id'],role,digest_value))
            return digest_value

    def fetch_candidate(self, attempt_id, object_sha256):
        digest(object_sha256)
        with self.transaction() as connection:
            obj = connection.execute('SELECT o.* FROM objects o JOIN proposed_artifacts p USING(sha256) '
                'JOIN executions e USING(execution_id) WHERE e.attempt_id=? AND o.sha256=?',(attempt_id,object_sha256)).fetchone()
            if obj is None: raise ValueError('candidate is not a member of this attempt')
            raw = read_regular(self.archive_dir,obj['archive_location'],limit=max(1,obj['byte_length']))
            if len(raw) != obj['byte_length'] or sha256(raw) != object_sha256: raise ValueError('archive integrity failure')
            return raw

    def store_proposed_result(self, attempt_id, payload):
        doc = parse_canonical_json(payload,label='proposed result')
        if type(doc) is not dict or doc.get('schema') != 'qualification_result_envelope/v2' or doc.get('attempt_id') != attempt_id:
            raise ValueError('proposed result identity differs')
        inventory = doc.get('outputs')
        if type(inventory) is not list:
            raise ValueError('ordered proposal output inventory required')
        for item in inventory:
            fields(item,{'role','sha256','byte_length','privacy'})
            digest(item['sha256'])
            if type(item['role']) is not str or type(item['byte_length']) is not int or item['byte_length'] <= 0 or item['privacy'] != 'PRIVATE':
                raise ValueError('private proposal output identity required')
        if [item['role'] for item in inventory] != list(N1_ARTIFACT_ROLES):
            raise ValueError('complete ordered proposal roles required')
        with self.transaction() as connection:
            status = self._status(connection,attempt_id)
            row = self._row(connection,status['execution_id'])
            self._check(row,row['revision'],('ATTESTED',))
            outputs = {item['role']:self.fetch_candidate(attempt_id,item['sha256']) for item in doc['outputs']}
            inspected = InspectedEvidence(payload,outputs)
            compare_n1_evidence(inspected,expected=inspected)
            for name in ('contract_sha256','trust_domain_sha256','policy_sha256'):
                if doc[name] != row[name]: raise ValueError('proposed result attempt binding differs')
            for item in doc['outputs']:
                if connection.execute('SELECT 1 FROM proposed_artifacts WHERE execution_id=? AND role=? AND sha256=?',
                    (row['execution_id'],item['role'],item['sha256'])).fetchone() is None:
                    raise ValueError('candidate role membership differs')
            digest_value = archive_bytes(self.archive_dir,payload)
            connection.execute('INSERT OR IGNORE INTO objects VALUES(?,?,?)',(digest_value,len(payload),digest_value))
            connection.execute('INSERT OR IGNORE INTO proposed_artifacts VALUES(?,?,?)',(row['execution_id'],'proposed_result',digest_value))
            return digest_value

    def fetch(self, attempt_id, object_sha256):
        digest(object_sha256)
        with self.transaction() as connection:
            obj = connection.execute('SELECT o.byte_length,o.archive_location,eo.role,e.state FROM objects o '
                'JOIN execution_objects eo ON eo.sha256=o.sha256 JOIN executions e USING(execution_id) '
                'WHERE e.attempt_id=? AND o.sha256=?', (attempt_id, object_sha256)).fetchone()
            if obj is None or (obj['role'] == 'attestation' and obj['state'] != 'ATTESTED'):
                raise ValueError('object is not a published member of this attempt')
            raw = read_regular(self.archive_dir, obj['archive_location'], limit=max(1, obj['byte_length']))
            if len(raw) != obj['byte_length'] or sha256(raw) != object_sha256:
                raise ValueError('archive integrity failure')
            return raw

    def _integrity(self, connection):
        try:
            if connection.execute('PRAGMA integrity_check').fetchone()[0] != 'ok' or connection.execute('PRAGMA foreign_key_check').fetchone():
                raise ValueError('SQLite consistency')
            for campaign in connection.execute('SELECT * FROM campaigns'):
                previous, count, latest = '0' * 64, 0, None
                row = connection.execute('SELECT * FROM executions WHERE attempt_id=?', (campaign['attempt_id'],)).fetchone()
                if row is None:
                    raise ValueError('campaign execution absent')
                state, validity, reason = None, 'VALID', None
                container, authorized, capture, attestation, assessment = None, None, None, None, None
                dispatch = None
                for event in connection.execute('SELECT * FROM events WHERE attempt_id=? ORDER BY sequence', (campaign['attempt_id'],)):
                    count += 1
                    latest = parse_canonical_json(event['body'], label='event')
                    if (event['sequence'] != count or event['previous_sha256'] != previous or latest['revision'] != count
                            or event['sha256'] != sha256(previous.encode('ascii') + event['body'])):
                        raise ValueError('event chain')
                    fields(latest, {'kind', 'execution_id', 'attempt_id', 'revision', 'state', 'data'})
                    if latest['execution_id'] != row['execution_id'] or latest['attempt_id'] != campaign['attempt_id']:
                        raise ValueError('event identity')
                    kind, data = latest['kind'], latest['data']
                    if kind == 'DISPATCHED' and state is None:
                        fields(data, {'request_sha256', 'plan_sha256', 'reserved_at_utc'})
                        if data['request_sha256'] != row['request_sha256'] or data['plan_sha256'] != row['plan_sha256']:
                            raise ValueError('dispatch bindings')
                        state, dispatch = 'DISPATCHED', event['sha256']
                    elif kind == 'CONTAINER' and state == 'DISPATCHED' and container is None and validity == 'VALID':
                        container = fields(data, {'container_id'})['container_id']
                        digest(container)
                    elif kind == 'START_INTENT' and state == 'DISPATCHED' and container is not None and validity == 'VALID':
                        authorized = fields(data, {'authorized_at_utc'})['authorized_at_utc']
                        _time(authorized)
                        state = 'START_INTENT'
                    elif kind == 'RUNNING' and state == 'START_INTENT' and validity == 'VALID':
                        _time(fields(data, {'observed_at_utc'})['observed_at_utc'])
                        state = 'RUNNING'
                    elif kind == 'CAPTURED' and state == 'RUNNING' and validity == 'VALID':
                        if data['container_id'] != container or data['authorized_at_utc'] != authorized:
                            raise ValueError('capture launch binding')
                        capture = _capture_payload(row, data, capture_head=event['sha256'],
                            capture_revision=count, dispatch_head=dispatch)
                        state = 'CAPTURED'
                    elif kind == 'ATTESTED' and state == 'CAPTURED' and validity == 'VALID':
                        attestation = fields(data, {'attestation_sha256'})['attestation_sha256']
                        state = 'ATTESTED'
                    elif kind == 'VOID' and validity == 'VALID':
                        fields(data, {'reason', 'approval_sha256', 'voided_at_utc'})
                        validity, reason = 'VOID', data['reason']
                    elif kind in ('ABORTED', 'IN_DOUBT') and state in ('DISPATCHED', 'START_INTENT', 'RUNNING'):
                        fields(data, {'reason'})
                        state = kind
                    elif kind == 'ASSESSMENT' and state == 'ATTESTED' and validity == 'VALID' and assessment is None:
                        fields(data, {'result_sha256', 'authentication_sha256', 'cutoff_sha256', 'outputs', 'committed_at_utc'})
                        assessment = (data, event['sha256'])
                    else:
                        raise ValueError('event transition')
                    if latest['state'] != state:
                        raise ValueError('event state')
                    previous = event['sha256']
                if previous != campaign['event_head'] or count != campaign['event_count'] or latest is None:
                    raise ValueError('campaign head')
                row = self._row(connection, latest['execution_id'])
                if row['state'] != latest['state'] or row['revision'] != count:
                    raise ValueError('execution transition')
                if (campaign['validity'] != validity or campaign['reason'] != reason
                        or row['container_id'] != container or row['authorized_at_utc'] != authorized
                        or row['captured_payload'] != capture or row['attestation_sha256'] != attestation):
                    raise ValueError('event projection differs')
                if sha256(row['plan_bytes']) != row['plan_sha256'] or sha256(row['request_bytes']) != row['request_sha256']:
                    raise ValueError('execution bindings')
                plan = parse_canonical_json(row['plan_bytes'],label='plan')
                for name in ('contract_sha256','trust_domain_sha256','policy_sha256'):
                    if campaign[name] != plan[name]: raise ValueError('campaign plan binding')
                members = {item['role']: item['sha256'] for item in connection.execute(
                    'SELECT role,sha256 FROM execution_objects WHERE execution_id=?', (row['execution_id'],))}
                if members.get('plan') != row['plan_sha256']:
                    raise ValueError('plan membership')
                if row['state'] in ('CAPTURED', 'ATTESTED'):
                    payload = parse_canonical_json(row['captured_payload'], label='captured payload')
                    for item in payload['artifacts']:
                        if members.get(item['role']) != item['sha256']:
                            raise ValueError('capture membership')
                    event = connection.execute('SELECT sha256,body FROM events WHERE attempt_id=? AND sequence=?',
                        (row['attempt_id'], payload['capture_revision'])).fetchone()
                    if event is None or event[0] != payload['capture_event_sha256']:
                        raise ValueError('capture event')
                if row['state'] == 'ATTESTED' and members.get('attestation') != row['attestation_sha256']:
                    raise ValueError('attestation membership')
                if attestation is not None:
                    envelope = parse_canonical_json(self.fetch(row['attempt_id'], attestation), label='attestation')
                    if encoded(envelope['payload']) != capture:
                        raise ValueError('attestation capture differs')
                saved = connection.execute('SELECT * FROM assessments WHERE execution_id=?', (row['execution_id'],)).fetchone()
                if (saved is None) != (assessment is None):
                    raise ValueError('assessment projection absent')
                if saved is not None:
                    data, head = assessment
                    if (saved['result_sha256'] != data['result_sha256']
                            or saved['authentication_sha256'] != data['authentication_sha256']
                            or sha256(saved['cutoff_bytes']) != data['cutoff_sha256']
                            or saved['commit_event_sha256'] != head):
                        raise ValueError('assessment projection differs')
                    if saved['receipt_bytes'] != _assessment_receipt(row,data,head):
                        raise ValueError('assessment receipt differs')
                    if members.get('assessment_receipt') != sha256(saved['receipt_bytes']):
                        raise ValueError('assessment receipt membership differs')
                    for item in data['outputs']:
                        if members.get(item['role']) != item['sha256']:
                            raise ValueError('assessment output membership differs')
                    for role, key in (('result', 'result_sha256'), ('result_authentication', 'authentication_sha256'), ('cutoff', 'cutoff_sha256')):
                        if members.get(role) != data[key]:
                            raise ValueError('assessment membership')
            for obj in connection.execute('SELECT * FROM objects'):
                if obj['archive_location'] != obj['sha256']:
                    raise ValueError('archive location')
                raw = read_regular(self.archive_dir, obj['archive_location'], limit=max(1, obj['byte_length']))
                if len(raw) != obj['byte_length'] or sha256(raw) != obj['sha256']:
                    raise ValueError('object content')
        except (ValueError, TypeError, KeyError, OSError) as exc:
            raise ValueError(f'journal integrity failure: {exc}') from exc
