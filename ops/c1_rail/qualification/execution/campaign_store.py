"""Dormant campaigns sharing ExecutionStore's lock, database and validity authority.

Only the protected service supplies verified contexts and trusted observations.
Private metered intents do not activate a release or launch a process.
"""
import base64
from contextlib import contextmanager
import uuid

from ..contract import canonical_json_bytes as encoded, parse_canonical_json
from ..checkpoint_plan import _CAMPAIGN_MAX_BYTES
from .campaign_protocol import parse_campaign_request
from .protocol import sha256
from .campaign_budget import WORK_PREDECESSORS

SCHEMA = '''
CREATE TABLE IF NOT EXISTS full_campaigns (
 attempt_id TEXT PRIMARY KEY, campaign_id TEXT NOT NULL UNIQUE,
 request_bytes BLOB NOT NULL, receipt_bytes BLOB NOT NULL,
 validity TEXT NOT NULL CHECK(validity IN ('VALID','VOID')),
 void_request BLOB, void_receipt BLOB);
CREATE TABLE IF NOT EXISTS full_campaign_objects (
 attempt_id TEXT NOT NULL REFERENCES full_campaigns(attempt_id), role TEXT NOT NULL,
 sha256 TEXT NOT NULL, byte_length INTEGER NOT NULL, body BLOB NOT NULL,
 PRIMARY KEY(attempt_id,role));
'''


from .campaign_funding import FundingStoreMixin, SCHEMA as FUNDING_SCHEMA, PROFILE as FUNDED_PROFILE, _put as _put_funding

# Funded post-admission cancellation authentication (S2-G2, 2026-09-19). A
# queued operator body is transport, never authority. Each signature check is
# preceded by one durable, one-use charge object folded into the funding
# projection; the outcome is a VOID receipt or a retained refusal object.
VOID_AUTHENTICATION_SCHEMA = 'qualification_campaign_void_authentication/v1'
VOID_REFUSAL_SCHEMA = 'qualification_campaign_void_refusal/v1'
VOID_ADMISSION_REFUSAL_SCHEMA = 'qualification_campaign_void_admission_refusal/v1'
VOID_AUTHENTICATION_PREFIX = 'void_authentication_'
VOID_REFUSAL_PREFIX = 'void_refusal_'
# A pre-admission body is authenticated under the guardian's charged admission
# work; its refusal is retained without a charge object and pairs with nothing.
VOID_ADMISSION_REFUSAL_PREFIX = 'void_admission_refusal_'
# S2-G4 A1 (2026-09-20): on a terminal-but-VALID funded campaign there is no
# allowance to charge and no positive authority to protect, so a queued body is
# authenticated once, uncharged, under the controller guard. Its refusal is
# retained under a role keyed by the body digest, which makes "once per
# distinct body" structural (the queue refuses a digest already refused).
VOID_TERMINAL_REFUSAL_SCHEMA = 'qualification_campaign_void_terminal_refusal/v1'
VOID_TERMINAL_REFUSAL_PREFIX = 'void_terminal_refusal_'
CANCELLATION_PENDING = 'campaign cancellation pending; new authority unavailable'
TERMINAL_BODY_REFUSED = 'cancellation body already refused on the terminal campaign; no unmetered retry'


def void_authentication_bound():
    """Installed one-use controller charge: control CPU plus its granularity margin, control wall."""
    from .profile import CAMPAIGN_RESOURCE_SCOPE as policy
    return dict(cpu_ns=(policy['control_cpu_seconds'] + policy['cpu_granularity_seconds']) * 10**9,
                wall_ns=policy['control_wall_seconds'] * 10**9)


def _void_role(prefix, sequence):
    from .campaign_budget import integer
    return prefix + '%06d' % integer(sequence, positive=True)


def parse_void_authentication(raw):
    from .protocol import fields, identity, digest
    from .campaign_budget import clock, integer
    doc = fields(parse_canonical_json(raw, label='cancellation charge'),
                 {'schema', 'attempt_id', 'sequence', 'request_sha256', 'charge_cpu_ns', 'wall_ns', 'clock'})
    if doc['schema'] != VOID_AUTHENTICATION_SCHEMA:
        raise ValueError('cancellation charge schema required')
    identity(doc['attempt_id']); digest(doc['request_sha256'])
    integer(doc['sequence'], positive=True); clock(encoded(doc['clock']))
    bound = void_authentication_bound()
    if doc['charge_cpu_ns'] != bound['cpu_ns'] or doc['wall_ns'] != bound['wall_ns']:
        raise ValueError('installed cancellation charge differs')
    return doc


def parse_void_refusal(raw, *, schema=VOID_REFUSAL_SCHEMA):
    from .protocol import fields, identity, digest
    from .campaign_budget import clock, integer
    doc = fields(parse_canonical_json(raw, label='cancellation refusal'),
                 {'schema', 'attempt_id', 'sequence', 'request_sha256', 'reason', 'clock'})
    if doc['schema'] != schema:
        raise ValueError('cancellation refusal schema required')
    identity(doc['attempt_id']); digest(doc['request_sha256'])
    integer(doc['sequence'], positive=True); clock(encoded(doc['clock']))
    if type(doc['reason']) is not str or not doc['reason'] or len(doc['reason']) > 1024:
        raise ValueError('bounded cancellation refusal reason required')
    return doc


CHECKPOINT_SCHEMA = '''
CREATE TABLE IF NOT EXISTS full_campaign_checkpoint_captures (
 attempt_id TEXT PRIMARY KEY REFERENCES full_campaigns(attempt_id),
 checkpoint TEXT NOT NULL CHECK(checkpoint='N1'),
 work_id TEXT NOT NULL,
 result_bytes BLOB NOT NULL CHECK(length(result_bytes)<=262144),
 payload_bytes BLOB NOT NULL CHECK(length(payload_bytes)<=268435456),
 attestation_bytes BLOB);
CREATE TABLE IF NOT EXISTS full_campaign_checkpoint_staged (
 attempt_id TEXT NOT NULL REFERENCES full_campaigns(attempt_id),
 role TEXT NOT NULL, sha256 TEXT NOT NULL, body BLOB NOT NULL CHECK(length(body)<=268435456),
 PRIMARY KEY(attempt_id,role,sha256));
CREATE TABLE IF NOT EXISTS full_campaign_checkpoint_intents (
 attempt_id TEXT PRIMARY KEY REFERENCES full_campaigns(attempt_id),
 checkpoint TEXT NOT NULL CHECK(checkpoint='N1'),
 work_id TEXT NOT NULL,
 snapshot_bytes BLOB NOT NULL CHECK(length(snapshot_bytes)<=262144),
 intent_bytes BLOB NOT NULL CHECK(length(intent_bytes)<=262144),
 candidate_bytes BLOB NOT NULL CHECK(length(candidate_bytes)<=262144),
 cutoff_bytes BLOB, receipt_bytes BLOB);
'''

from ..evidence import (CHECKPOINT_RESULT_SCHEMA, CHECKPOINT_ATTESTATION_SCHEMA,
    CHECKPOINT_ASSESSMENT_SCHEMA, CHECKPOINT_RECEIPT_SCHEMA, CHECKPOINT_CUTOFF_SCHEMA,
    CHECKPOINT_INTENT_SCHEMA, parse_checkpoint_result, parse_checkpoint_attestation,
    parse_checkpoint_assessment, parse_checkpoint_cutoff)


class CheckpointStoreMixin:
    """The D1 custody surface: FULL_E1 checkpoint capture, staging, intent and commit.

    Mixed into CampaignStore, which supplies the budget/work projections, the
    funding gate and the save helpers. Every writer first performs the lazy
    exact-layout user_version 7 -> 8 migration inside its own transaction; the
    tables below are the only home for the checkpoint evidence family bytes.
    """

    def _ensure_checkpoint_layout(self, connection):
        version = connection.execute('PRAGMA user_version').fetchone()[0]
        if version == 8:
            return
        if version != 7:
            raise ValueError('checkpoint custody requires database v7')
        self.store.validate_layout(connection, 7)
        for statement in CHECKPOINT_SCHEMA.split(';'):
            if statement.strip():
                connection.execute(statement)
        connection.execute('PRAGMA user_version=8')

    def _family(self, budget, checkpoint='N1', **row):
        """Move the checkpoint family projection; `state` names the family state."""
        family = dict(budget.get('checkpoints') or {})
        if set(family) - {'N1'} or (checkpoint in family and family[checkpoint]['work_id'] != row.get('work_id', family[checkpoint]['work_id'])):
            raise ValueError('checkpoint family identity differs')
        family[checkpoint] = row
        budget['schema'] = 'qualification_campaign_budget_snapshot/v6'
        budget['checkpoints'] = family
        return budget

    def _require_family(self, state, checkpoint='N1'):
        family = state.get('checkpoints') or {}
        if checkpoint not in family:
            raise ValueError('checkpoint family absent')
        return family[checkpoint]

    def retain_checkpoint_capture(self, attempt_id, work_id, result_bytes, payload_bytes, capture_transition_bytes):
        """Archive the finalized capture byte-for-byte and record the work's CAPTURED.

        One transaction: the capture row (result + payload), the snapshot's v6
        family projection and the work's CAPTURED transition commit together, so
        a restart either sees the whole family or none of it. An exact retry of
        the same bytes is idempotent; any difference refuses.
        """
        result = parse_checkpoint_result(result_bytes, attempt_id=attempt_id)
        if result['work_id'] != work_id or sha256(payload_bytes) != result['payload_sha256'] \
                or result['payload_byte_length'] != len(payload_bytes):
            raise ValueError('archived payload differs from the checkpoint result')
        from .campaign_budget import clock, transition as parse_transition
        document = parse_transition(capture_transition_bytes, attempt_id, work_id)
        if document['state'] != 'CAPTURED':
            raise ValueError('capture transition required')
        with self.store.transaction() as connection:
            self._ensure_checkpoint_layout(connection)
            prior = connection.execute('SELECT result_bytes,payload_bytes FROM full_campaign_checkpoint_captures '
                                       'WHERE attempt_id=?', (attempt_id,)).fetchone()
            if prior is not None:
                if (bytes(prior[0]), bytes(prior[1])) != (result_bytes, payload_bytes):
                    raise ValueError('immutable checkpoint capture differs')
            state = self._budget(connection, attempt_id)
            work = self._work(state, work_id)
            if work['phase'] != 'N1':
                raise ValueError('checkpoint capture requires the N1 compute work')
            self.record_work_transition(attempt_id, work_id, capture_transition_bytes,
                                        expected_revision=state['authority_revision'])
            state = self._budget(connection, attempt_id)
            self._family(state, work_id=work_id, state='CAPTURED',
                         payload_sha256=result['payload_sha256'])
            if prior is None:
                connection.execute('INSERT INTO full_campaign_checkpoint_captures VALUES(?,?,?,?,?,?)',
                    (attempt_id, 'N1', work_id, result_bytes, payload_bytes, None))
            return self._save_budget(connection, state, 'CHECKPOINT_CAPTURED', authority=False)

    def retain_checkpoint_attestation(self, attempt_id, attestation_bytes, *, verify):
        """Attest exactly the archived bytes; idempotent on the same signature.

        `verify` re-checks the attestation envelope against the retained capture
        row and current enrollment (the caller owns signature policy); only the
        durable family move to ATTESTED lives here.
        """
        with self.store.transaction() as connection:
            self._ensure_checkpoint_layout(connection)
            row = connection.execute('SELECT work_id,result_bytes,payload_bytes,attestation_bytes '
                                     'FROM full_campaign_checkpoint_captures WHERE attempt_id=?', (attempt_id,)).fetchone()
            if row is None:
                raise ValueError('archived checkpoint capture required')
            prior = row[3]
            if prior is not None and bytes(prior) != attestation_bytes:
                raise ValueError('immutable checkpoint attestation differs')
            verify(attempt_id, bytes(row[1]), bytes(row[2]), attestation_bytes)
            state = self._budget(connection, attempt_id)
            family = self._require_family(state)
            if prior is not None:
                return self._negative_budget_response(connection, state)
            if family['state'] != 'CAPTURED':
                raise ValueError('checkpoint family state differs')
            self._family(state, work_id=family['work_id'], state='ATTESTED',
                         payload_sha256=family['payload_sha256'], result_sha256=sha256(bytes(row[1])),
                         attestation_sha256=sha256(attestation_bytes))
            if prior is None:
                connection.execute('UPDATE full_campaign_checkpoint_captures SET attestation_bytes=? '
                                   'WHERE attempt_id=?', (attestation_bytes, attempt_id))
            return self._save_budget(connection, state, 'CHECKPOINT_ATTESTED', authority=False)

    def checkpoint_capture(self, attempt_id):
        """One bounded family view for the G5-facing snapshot and member fetches."""
        with self.store.transaction() as connection:
            if connection.execute('PRAGMA user_version').fetchone()[0] < 8:
                raise ValueError('no checkpoint family retained')
            row = connection.execute('SELECT work_id,result_bytes,payload_bytes,attestation_bytes '
                                     'FROM full_campaign_checkpoint_captures WHERE attempt_id=?', (attempt_id,)).fetchone()
            if row is None:
                raise ValueError('no checkpoint family retained')
            if row[3] is None:
                raise ValueError('checkpoint family attestation absent')
            return dict(work_id=row[0], result_bytes=bytes(row[1]), payload_bytes=bytes(row[2]),
                        attestation_bytes=bytes(row[3]))

    def stage_checkpoint_artifact(self, attempt_id, role, raw):
        from .protocol import identity
        identity(role)
        if len(raw) > 268435456:
            raise ValueError('staged checkpoint artifact exceeds bound')
        with self.store.transaction() as connection:
            self._ensure_checkpoint_layout(connection)
            self._budget(connection, attempt_id)
            digest_value = sha256(raw)
            connection.execute('INSERT OR IGNORE INTO full_campaign_checkpoint_staged VALUES(?,?,?,?)',
                               (attempt_id, role, digest_value, raw))
            return digest_value

    def checkpoint_members(self, attempt_id):
        """The served member inventory: family bytes plus retained inputs, by digest."""
        from ..checkpoint_plan import derive_checkpoint_plan
        with self.store.transaction() as connection:
            self._funding_gate(connection, attempt_id)
            state = self._budget(connection, attempt_id)
            self._require_family(state)
            capture = self.checkpoint_capture(attempt_id)
            plan_bytes = derive_checkpoint_plan(self.retained_object(attempt_id, 'plan'), 'N1', None)
            members = [dict(role=name, sha256=sha256(raw), byte_length=len(raw)) for name, raw in (
                ('plan', plan_bytes), ('result', capture['result_bytes']),
                ('payload', capture['payload_bytes']), ('attestation', capture['attestation_bytes']))]
            for role, raw in sorted(self.objects(attempt_id).items()):
                if role.startswith('context_') or role == 'bundle_index':
                    members.append(dict(role='retained_' + role, sha256=sha256(raw), byte_length=len(raw)))
            # Staged artifacts are G5 transport, not campaign state: they stay
            # out of the served snapshot so a candidate's snapshot binding is
            # stable across its own staging (the fetch path resolves them by
            # digest from the staging table). The persisted candidate itself
            # IS served when an intent exists -- an exact retry must redeliver
            # those bytes, never a fresh signature.
            intent = connection.execute('SELECT candidate_bytes FROM full_campaign_checkpoint_intents '
                                        'WHERE attempt_id=?', (attempt_id,)).fetchone()
            if intent is not None:
                raw = bytes(intent[0])
                members.append(dict(role='candidate', sha256=sha256(raw), byte_length=len(raw)))
            return members

    def fetch_checkpoint_member(self, attempt_id, object_sha256, offset, length):
        """One bounded chunk of one served member; the plan-chunk pattern."""
        from ..checkpoint_plan import derive_checkpoint_plan
        from .campaign_protocol import CHECKPOINT_CHUNK_LIMIT
        from .protocol import digest as parse_digest
        from .campaign_budget import integer
        parse_digest(object_sha256)
        integer(offset); integer(length, positive=True)
        if length > CHECKPOINT_CHUNK_LIMIT:
            raise ValueError('bounded integer chunk length required')
        with self.store.transaction() as connection:
            self._funding_gate(connection, attempt_id)
            state = self._budget(connection, attempt_id)
            self._require_family(state)
            capture = self.checkpoint_capture(attempt_id)
            plan_bytes = derive_checkpoint_plan(self.retained_object(attempt_id, 'plan'), 'N1', None)
            sources = {'plan': plan_bytes, 'result': capture['result_bytes'],
                       'payload': capture['payload_bytes'], 'attestation': capture['attestation_bytes']}
            for role, raw in self.objects(attempt_id).items():
                if role.startswith('context_') or role == 'bundle_index':
                    sources['retained_' + role] = raw
            row = connection.execute('SELECT role,body FROM full_campaign_checkpoint_staged '
                                     'WHERE attempt_id=? AND sha256=?', (attempt_id, object_sha256)).fetchone()
            if row is not None:
                sources['staged_' + row[0]] = bytes(row[1])
            intent = connection.execute('SELECT candidate_bytes FROM full_campaign_checkpoint_intents '
                                        'WHERE attempt_id=?', (attempt_id,)).fetchone()
            if intent is not None:
                sources['candidate'] = bytes(intent[0])
            raw = next((value for value in sources.values() if sha256(value) == object_sha256), None)
            if raw is None:
                raise ValueError('checkpoint member membership differs')
            if offset >= len(raw):
                raise ValueError('chunk offset outside member')
            chunk = raw[offset:offset + length]
            return encoded(dict(schema='qualification_campaign_checkpoint_chunk/v1',
                attempt_id=attempt_id, object_sha256=object_sha256, offset=offset,
                total_byte_length=len(raw), byte_length=len(chunk),
                bytes_b64=self._b64(chunk)))

    def checkpoint_snapshot(self, attempt_id, checkpoint='N1'):
        from ..journal_snapshot import encode_campaign_checkpoint_snapshot
        with self.store.transaction() as connection:
            self._funding_gate(connection, attempt_id)
            state = self._budget(connection, attempt_id)
            family = self._require_family(state, checkpoint)
            capture = self.checkpoint_capture(attempt_id)
            plan = parse_canonical_json(self.retained_object(attempt_id, 'plan'), label='campaign plan')
            intent = connection.execute('SELECT work_id,candidate_bytes FROM '
                                        'full_campaign_checkpoint_intents WHERE attempt_id=?', (attempt_id,)).fetchone()
            return encode_campaign_checkpoint_snapshot(attempt_id=attempt_id, checkpoint=checkpoint,
                contract_sha256=plan['contract_sha256'], trust_domain_sha256=plan['trust_domain_sha256'],
                policy_sha256=plan['policy_sha256'], validity=self.row(attempt_id)['validity'],
                campaign_revision=state['authority_revision'], authority_head=state['authority_head'],
                event_head=state['event_head'], campaign_state=state['state'],
                works=[dict(work_id=work['work_id'], phase=work['phase'], state=work['state'],
                            settled=work['observation_bytes_b64'] is not None) for work in state['works']],
                capture=dict(work_id=capture['work_id'], result_sha256=sha256(capture['result_bytes']),
                             payload_sha256=sha256(capture['payload_bytes']),
                             attestation_sha256=sha256(capture['attestation_bytes'])),
                intent=dict(work_id=intent[0] if intent is not None else family['work_id'],
                            candidate_sha256=None if intent is None else sha256(bytes(intent[1]))),
                members=self.checkpoint_members(attempt_id))

    def _checkpoint_integrity(self, connection):
        """The D1 family walk: table rows bind to the snapshot's own projection."""
        from ..journal_snapshot import parse_campaign_checkpoint_snapshot
        for row in connection.execute('SELECT attempt_id,checkpoint,work_id,result_bytes,payload_bytes,attestation_bytes '
                                      'FROM full_campaign_checkpoint_captures'):
            attempt = row[0]
            state = self._budget(connection, attempt)
            family = (state.get('checkpoints') or {}).get(row[1])
            if (family is None or family['work_id'] != row[2]
                    or family['payload_sha256'] != sha256(bytes(row[4]))
                    or (row[5] is not None and family.get('attestation_sha256') != sha256(bytes(row[5])))):
                raise ValueError('checkpoint capture projection differs')
            parse_checkpoint_result(bytes(row[3]), attempt_id=attempt)
            if row[5] is not None:
                parse_checkpoint_attestation(bytes(row[5]), attempt_id=attempt)
                if family['state'] == 'CAPTURED':
                    raise ValueError('checkpoint family state differs')
            elif family['state'] != 'CAPTURED':
                raise ValueError('checkpoint family state differs')
        for row in connection.execute('SELECT attempt_id,checkpoint,work_id,snapshot_bytes,intent_bytes,candidate_bytes,cutoff_bytes,receipt_bytes '
                                      'FROM full_campaign_checkpoint_intents'):
            attempt = row[0]
            state = self._budget(connection, attempt)
            family = (state.get('checkpoints') or {}).get(row[1])
            if family is None or family.get('assessment_sha256') != (None if row[7] is None else sha256(bytes(row[5]))):
                raise ValueError('checkpoint intent projection differs')
            parse_campaign_checkpoint_snapshot(bytes(row[3]))
            parse_checkpoint_assessment(bytes(row[5]), attempt_id=attempt)
            if row[7] is not None:
                if row[6] is None:
                    raise ValueError('committed checkpoint cutoff absent')
                parse_checkpoint_cutoff(bytes(row[6]), attempt_id=attempt)
                receipt = parse_canonical_json(bytes(row[7]), label='receipt')
                if (receipt['schema'] != CHECKPOINT_RECEIPT_SCHEMA or receipt['attempt_id'] != attempt
                        or receipt['assessment_sha256'] != sha256(bytes(row[5]))
                        or receipt['cutoff_sha256'] != sha256(bytes(row[6]))
                        or family.get('receipt_sha256') != sha256(bytes(row[7]))):
                    raise ValueError('checkpoint receipt integrity differs')
        for row in connection.execute('SELECT attempt_id,role,sha256,body FROM full_campaign_checkpoint_staged'):
            if sha256(bytes(row[3])) != row[2]:
                raise ValueError('checkpoint staged artifact integrity differs')

    def persist_checkpoint_intent(self, attempt_id, work_id, snapshot_bytes, intent_bytes,
                                  candidate_bytes, capture_transition_bytes, signing_transition_bytes):
        """T1 of the D1 commit: the g5 work's CAPTURED + SIGNING_INTENT and the durable
        candidate, all in one transaction.

        An exact retry of the same candidate is idempotent and returns the
        persisted projection; a different candidate under a persisted intent
        refuses (no second signing time, no fresh signature). The candidate and
        snapshot bytes stay private until :meth:`commit_checkpoint_assessment`.
        """
        from ..journal_snapshot import parse_campaign_checkpoint_snapshot
        from .protocol import fields
        candidate = parse_checkpoint_assessment(candidate_bytes, attempt_id=attempt_id)
        snapshot = parse_campaign_checkpoint_snapshot(snapshot_bytes)
        intent = fields(parse_canonical_json(intent_bytes, label='checkpoint signing intent'),
                        {'schema', 'attempt_id', 'checkpoint', 'work_id', 'key_id',
                         'signing_at_utc', 'candidate_sha256', 'snapshot_sha256'})
        from .campaign_budget import utc
        if (intent['schema'] != CHECKPOINT_INTENT_SCHEMA or intent['attempt_id'] != attempt_id
                or intent['checkpoint'] != 'N1' or intent['work_id'] != work_id
                or intent['candidate_sha256'] != sha256(candidate_bytes)):
            raise ValueError('checkpoint signing intent binding differs')
        utc(intent['signing_at_utc'])
        # The candidate's work_id names the captured N1 work; the intent and
        # the signing window belong to the assessing N1_G5 work.
        if (candidate['attempt_id'] != attempt_id or snapshot['attempt_id'] != attempt_id
                or intent['snapshot_sha256'] != sha256(snapshot_bytes)):
            raise ValueError('checkpoint signing intent identity differs')
        with self.store.transaction() as connection:
            self._ensure_checkpoint_layout(connection)
            prior = connection.execute('SELECT snapshot_bytes,intent_bytes,candidate_bytes FROM '
                                       'full_campaign_checkpoint_intents WHERE attempt_id=?', (attempt_id,)).fetchone()
            if prior is not None:
                if (bytes(prior[1]), bytes(prior[2])) != (intent_bytes, candidate_bytes):
                    raise ValueError('immutable checkpoint signing candidate differs')
                return self._negative_budget_response(connection, self._budget(connection, attempt_id))
            state = self._budget(connection, attempt_id)
            work = self._work(state, work_id)
            if work['phase'] != 'N1_G5':
                raise ValueError('checkpoint assessment requires the N1_G5 work')
            family = self._require_family(state)
            if family['state'] not in ('ATTESTED', 'ASSESSING'):
                raise ValueError('attested checkpoint family required')
            from .campaign_budget import transition as parse_transition
            for raw, expected in ((capture_transition_bytes, 'CAPTURED'), (signing_transition_bytes, 'SIGNING_INTENT')):
                document = parse_transition(raw, attempt_id, work_id)
                if document['state'] != expected:
                    raise ValueError(expected.lower().replace('_', ' ') + ' transition required')
            # CAPTURED bumps the authority revision; re-read before SIGNING_INTENT.
            self.record_work_transition(attempt_id, work_id, capture_transition_bytes,
                                        expected_revision=state['authority_revision'])
            state = self._budget(connection, attempt_id)
            self.record_work_transition(attempt_id, work_id, signing_transition_bytes,
                                        expected_revision=state['authority_revision'])
            state = self._budget(connection, attempt_id)
            # The family's work_id stays the captured N1 work; the assessing
            # N1_G5 work is bound by the intent row below.
            self._family(state, work_id=family['work_id'], state='ASSESSING',
                         payload_sha256=family['payload_sha256'], result_sha256=family['result_sha256'],
                         attestation_sha256=family['attestation_sha256'])
            connection.execute('INSERT INTO full_campaign_checkpoint_intents VALUES(?,?,?,?,?,?,NULL,NULL)',
                               (attempt_id, 'N1', work_id, snapshot_bytes, intent_bytes, candidate_bytes))
            return self._save_budget(connection, state, 'CHECKPOINT_INTENT', authority=False)

    def commit_checkpoint_assessment(self, attempt_id, work_id, candidate_bytes, cutoff_bytes,
                                     *, now, clock_bytes):
        """T2 of the D1 commit: validate structurally, commit, advance the campaign.

        Requires the persisted T1 intent with the exact candidate bytes. The
        committed receipt binds the assessment, cutoff, decision and the intent's
        own signing instant; the campaign advances to N2_READY on CONTINUE and to
        N1_FAILED on FAILURE. An exact retry after a lost reply returns the
        byte-identical persisted receipt (no fresh time or signature).
        """
        from .store import instant
        candidate = parse_checkpoint_assessment(candidate_bytes, attempt_id=attempt_id)
        cutoff = parse_checkpoint_cutoff(cutoff_bytes, attempt_id=attempt_id)
        from .campaign_budget import clock as parse_clock
        with self.store.transaction() as connection:
            self._ensure_checkpoint_layout(connection)
            row = connection.execute('SELECT work_id,snapshot_bytes,intent_bytes,candidate_bytes,cutoff_bytes,receipt_bytes '
                                     'FROM full_campaign_checkpoint_intents WHERE attempt_id=?', (attempt_id,)).fetchone()
            if row is None or bytes(row[3]) != candidate_bytes:
                raise ValueError('exact checkpoint candidate retry required')
            if row[5] is not None:
                if bytes(row[4] or b'') != cutoff_bytes:
                    raise ValueError('immutable checkpoint commit differs')
                return encoded(dict(receipt=parse_canonical_json(bytes(row[5]), label='receipt'),
                                    validity=self.row(attempt_id)['validity'], historical=True))
            state = self._budget(connection, attempt_id)
            work = self._work(state, work_id)
            if work['phase'] != 'N1_G5' or work['state'] != 'SIGNING_INTENT':
                raise ValueError('signing intent window required')
            family = self._require_family(state)
            if family['state'] != 'ASSESSING':
                raise ValueError('checkpoint family assessment state differs')
            intent = parse_canonical_json(bytes(row[2]), label='persisted intent')
            from ..journal_snapshot import parse_campaign_checkpoint_snapshot as _parse_snapshot
            persisted_snapshot = _parse_snapshot(bytes(row[1]))
            if (candidate['snapshot']['snapshot_sha256'] != sha256(bytes(row[1]))
                    or candidate['snapshot']['campaign_revision'] != persisted_snapshot['campaign_revision']):
                raise ValueError('assessment snapshot identity differs')
            # Freshness: since the persisted T1 snapshot's head, no FOREIGN
            # authority may have changed. The intent's own CAPTURED/SIGNING_
            # INTENT events are authority events by construction, and the exact
            # redelivery path (the retry work's reserve/start/run/settle and
            # the dispatch bookkeeping) is non-authority by construction -- the
            # walk judges each interim event by its own recorded authority flag
            # plus the intent kinds, and refuses anything else.
            head = state['event_head']
            guard = 0
            while head != persisted_snapshot['event_head']:
                event = connection.execute('SELECT body,previous_sha256 FROM full_campaign_budget_events '
                                           'WHERE attempt_id=? AND sha256=?', (attempt_id, head)).fetchone()
                if event is None or (guard := guard + 1) > 64:
                    raise ValueError('assessment snapshot identity differs')
                interim = parse_canonical_json(bytes(event[0]), label='interim event')
                if interim['kind'] not in ('CAPTURED', 'SIGNING_INTENT', 'CHECKPOINT_INTENT') and interim['authority']:
                    raise ValueError('assessment snapshot identity differs')
                head = event[1]
            if (candidate['capture']['result_sha256'] != family.get('result_sha256')
                    or candidate['capture']['attestation_sha256'] != family.get('attestation_sha256')
                    or cutoff['assessment_sha256'] != sha256(candidate_bytes)):
                raise ValueError('assessment capture binding differs')
            if self.row(attempt_id)['validity'] != 'VALID' or state['validity'] != 'VALID':
                raise ValueError('VOID campaign')
            # Budget freshness at commit: the SIGNED transition below observes the
            # trusted clock (deadline) inside this same transaction.
            decision = candidate['decision']
            receipt = encoded(dict(schema=CHECKPOINT_RECEIPT_SCHEMA, attempt_id=attempt_id,
                checkpoint='N1', work_id=work_id, campaign_id=self.row(attempt_id)['campaign_id'],
                assessment_sha256=sha256(candidate_bytes), cutoff_sha256=sha256(cutoff_bytes),
                decision=decision, campaign_state='N2_READY' if decision == 'CONTINUE' else 'N1_FAILED',
                signing_at_utc=intent['signing_at_utc'], committed_at_utc=instant(now),
                intent_sha256=sha256(bytes(row[2]))))
            parse_canonical_json(receipt, label='receipt')
            signed_transition = encoded(dict(schema='qualification_campaign_work_transition/v1',
                attempt_id=attempt_id, work_id=work_id, state='SIGNED',
                clock=parse_clock(clock_bytes), data=dict(candidate_bytes_b64=self._b64(receipt))))
            # SIGNED while the campaign is still BOUND (the transition's own gate
            # refuses terminal budgets); the terminal advance rides this event.
            self.record_work_transition(attempt_id, work_id, signed_transition,
                                        expected_revision=state['authority_revision'])
            state = self._budget(connection, attempt_id)
            if state['state'] not in ('PROVISIONAL', 'BOUND'):
                return self._negative_budget_response(connection, state)
            state['state'] = 'N2_READY' if decision == 'CONTINUE' else 'N1_FAILED'
            self._family(state, work_id=family['work_id'], state='COMMITTED',
                         payload_sha256=family['payload_sha256'], result_sha256=family['result_sha256'],
                         attestation_sha256=family['attestation_sha256'],
                         assessment_sha256=sha256(candidate_bytes), receipt_sha256=sha256(receipt),
                         decision=decision)
            connection.execute('UPDATE full_campaign_checkpoint_intents SET cutoff_bytes=?,receipt_bytes=? '
                               'WHERE attempt_id=?', (cutoff_bytes, receipt, attempt_id))
            self._save_budget(connection, state,
                'CHECKPOINT_COMMITTED' if decision == 'CONTINUE' else 'CHECKPOINT_FAILED',
                authority=True)
            return encoded(dict(receipt=parse_canonical_json(receipt, label='receipt'),
                                validity=self.row(attempt_id)['validity'], historical=False))


class CampaignStore(FundingStoreMixin, CheckpointStoreMixin):
    def __init__(self, store):
        self.store = store

    def row(self, attempt):
        with self.store.transaction() as connection:
            row = connection.execute('SELECT * FROM full_campaigns WHERE attempt_id=?', (attempt,)).fetchone()
            if row is None:
                raise KeyError(attempt)
            return row

    def retry(self, request_bytes):
        request = parse_campaign_request(request_bytes)
        with self.store.transaction():
            try:
                row = self.row(request['attempt_id'])
            except KeyError:
                return None
            if row['request_bytes'] != request_bytes:
                raise ValueError('campaign request identity conflict')
            return self.status(request['attempt_id'])

    def status(self, attempt):
        row = self.row(attempt)
        if parse_canonical_json(row['receipt_bytes'], label='receipt')['schema'] == 'qualification_campaign_provisional_intent/v1':
            raise ValueError('private provisional intent is not dormant admission')
        return dict(schema='qualification_campaign_status/v1',
            receipt=parse_canonical_json(row['receipt_bytes'], label='campaign receipt'),
            validity=row['validity'])

    def objects(self, attempt):
        with self.store.transaction() as connection:
            self.row(attempt)
            return {row['role']: bytes(row['body']) for row in connection.execute(
                'SELECT * FROM full_campaign_objects WHERE attempt_id=?', (attempt,))}

    def admit(self, request_bytes, context, plan, *, now):
        from .store import instant
        request = parse_campaign_request(request_bytes)
        if (request['operation'] != 'SUBMIT_E1' or context.attempt_id != request['attempt_id']
                or context.bundle_sha256 != request['bundle_sha256']
                or context.release.document['capability'] != 'FULL_E1'):
            raise ValueError('campaign admission binding differs')
        if len(plan) > min(_CAMPAIGN_MAX_BYTES, context.profile.input_byte_limit):
            raise ValueError('campaign plan exceeds storage bound')
        with self.store.transaction() as connection:
            retry = self.retry(request_bytes)
            if retry is not None:
                return retry
            attempt = context.attempt_id
            if connection.execute('SELECT 1 FROM campaigns WHERE attempt_id=?', (attempt,)).fetchone():
                raise ValueError('N1 attempt cannot promote to FULL_E1')
            doc = parse_canonical_json(plan, label='campaign plan')
            if (doc['attempt_id'] != attempt or doc['source_bundle_sha256'] != context.bundle_sha256
                    or doc['contract_sha256'] != context.contract.contract_sha256
                    or doc['execution_release_sha256'] != context.release.sha256):
                raise ValueError('campaign plan binding differs')
            receipt = encoded(dict(schema='qualification_campaign_admission_receipt/v1',
                campaign_id=str(uuid.uuid4()), attempt_id=attempt, state='ADMITTED',
                authority_class='TEST_ONLY', dispatch_enabled=False,
                request_sha256=sha256(request_bytes), bundle_sha256=context.bundle_sha256,
                plan_sha256=sha256(plan), plan_byte_length=len(plan),
                contract_sha256=context.contract.contract_sha256,
                trust_domain_sha256=context.domain.sha256,
                execution_release_sha256=context.release.sha256,
                profile_sha256=context.profile.sha256, policy_sha256=context.policy.sha256,
                budget_sha256=sha256(encoded(doc['budget'])),
                admitted_at_utc=instant(now)))
            campaign_id = parse_canonical_json(receipt, label='receipt')['campaign_id']
            connection.execute('INSERT INTO full_campaigns VALUES(?,?,?,?,?,?,?)',
                (attempt, campaign_id, request_bytes, receipt, 'VALID', None, None))
            objects = {'plan': plan, 'bundle_index': context.retained_bundle_index,
                       **{'context_' + role: raw for role, raw in context.retained_bytes.items()}}
            for role, raw in objects.items():
                connection.execute('INSERT INTO full_campaign_objects VALUES(?,?,?,?,?)',
                    (attempt, role, sha256(raw), len(raw), raw))
            return self.status(attempt)

    def claim_supervision_control(self, attempt, work_id, slot, clock_bytes, *, recovery_owner_token=None):
        """Start a new active control operation, never a historical replay.

        Recovery claims/denials commit independently. A lost owner cannot resume;
        a new recovery need after completion creates an unfunded durable barrier.
        """
        from .campaign_supervisor import parse_supervision_event, SUPERVISION_EVENT_V2
        from .campaign_budget import clock
        if slot == 'RECOVERY_OWNER' and getattr(self.store._local, 'connection', None) is not None:
            raise ValueError('active recovery claim requires independent transaction')
        raw = encoded(dict(schema=SUPERVISION_EVENT_V2, attempt_id=attempt,
            work_id=work_id, kind='CONTROL', clock=clock(clock_bytes), data=dict(slot=slot)))
        parse_supervision_event(raw)
        role = 'supervision_control_' + sha256(encoded([work_id, slot]))
        spent = False
        with self.store.transaction() as connection:
            state = self._budget(connection, attempt)
            self._work(state, work_id)
            if state['profile']['schema'] not in ('qualification_campaign_budget_profile/v2', 'qualification_campaign_budget_profile/v3'):
                raise ValueError('installed metered control slots required')
            spent = connection.execute('SELECT 1 FROM full_campaign_objects WHERE attempt_id=? AND role=?', (attempt, role)).fetchone() is not None
            if spent:
                if slot == 'RECOVERY_OWNER':
                    recovery = next((r for r in state.get('recoveries', ()) if r['work_id'] == work_id), None)
                    if recovery is not None and recovery['completion_bytes_b64'] is not None and not recovery['continuation_required']:
                        before = state['state']
                        recovery['continuation_required'] = True
                        self._observe_clock(state, clock(clock_bytes))
                        self._save_budget(connection, state, 'RECOVERY_CONTINUATION_REQUIRED', authority=state['state'] != before)
            else:
                if slot != 'RECOVERY_OWNER':
                    if recovery_owner_token is not None:
                        raise ValueError('only recovery has an owner token')
                    self._check_budget(state, state['authority_revision'])
                else:
                    # Omission deliberately creates an uncompletable claim.
                    # Production supplies an ephemeral, never persisted token.
                    import secrets
                    token = secrets.token_bytes(32) if recovery_owner_token is None else recovery_owner_token
                    self._validate_recovery_token(token)
                    state['schema'] = ('qualification_campaign_budget_snapshot/v6' if 'checkpoints' in state else 'qualification_campaign_budget_snapshot/v5') if state['profile']['schema'] == 'qualification_campaign_budget_profile/v3' else 'qualification_campaign_budget_snapshot/v4'
                    state.setdefault('dispatches', [])
                    state.setdefault('recoveries', []).append(dict(work_id=work_id,
                        claim_sha256=sha256(raw), owner_sha256=sha256(token),
                        observations_bytes_b64=None, completion_bytes_b64=None, continuation_required=False))
                    state['recoveries'].sort(key=lambda row: row['work_id'])
                    self._save_budget(connection, state, 'RECOVERY_CLAIM', authority=False)
                connection.execute('INSERT INTO full_campaign_objects VALUES(?,?,?,?,?)',
                                   (attempt, role, sha256(raw), len(raw), raw))
        # Refusal follows commit, including the negative continuation marker.
        if spent:
            raise ValueError('control slot already spent; no unmetered retry')
        return raw

    def _dispatch_clock(self, connection, state, work, clock_source):
        from .campaign_budget import clock
        current = clock(clock_source())  # Sample while the serialized decision is held.
        before = state['state']
        self._observe_clock(state, current)
        reservation = parse_canonical_json(self._raw(work['reservation_bytes_b64']), label='reservation')
        deadline = min(state['deadline_boottime_ns'], reservation['clock']['boottime_ns'] + work['limits']['wall_ns'])
        if current['boottime_ns'] is not None and current['boottime_ns'] >= deadline:
            self._terminal(state, 'BUDGET_EXHAUSTED')
        self._save_budget(connection, state, 'DISPATCH_CLOCK', authority=state['state'] != before)
        return current, deadline

    @contextmanager
    def launch_gate(self, attempt_id, work_id, clock_source, *, role='guardian'):
        """Commit uncertainty before an effect; serialize only its bounded request.

        The live caller alone may acknowledge acceptance. Losing it leaves a
        durable barrier, even when every post-effect database write fails.
        """
        import secrets
        if getattr(self.store._local, 'connection', None) is not None:
            raise ValueError('launch gate requires independent transaction')
        if role not in ('guardian', 'payload'):
            raise ValueError('fixed dispatch role required')
        token = secrets.token_bytes(32)
        owner = sha256(token)
        with self.store.transaction() as connection:
            state = self._budget(connection, attempt_id)
            work = self._work(state, work_id)
            self._check_budget(state, state['authority_revision'])
            if work['state'] not in ('START_INTENT', 'RUNNING') or work['observation_bytes_b64'] is not None:
                raise ValueError('durable unconsumed start intent required')
            if any(r['work_id'] == work_id and r['role'] == role for r in state.get('dispatches', ())):
                raise ValueError('dispatch already spent; no relaunch')
            current, deadline = self._dispatch_clock(connection, state, work, clock_source)
            refused = state['state'] not in ('PROVISIONAL', 'BOUND')
            if not refused:
                state['schema'] = ('qualification_campaign_budget_snapshot/v6' if 'checkpoints' in state else 'qualification_campaign_budget_snapshot/v5') if state['profile']['schema'] == 'qualification_campaign_budget_profile/v3' else 'qualification_campaign_budget_snapshot/v4'
                state.setdefault('recoveries', [])
                state.setdefault('dispatches', []).append(dict(work_id=work_id, role=role,
                    owner_sha256=owner, started_clock=current, acknowledged_clock=None))
                state['dispatches'].sort(key=lambda r: (r['work_id'], r['role']))
                self._save_budget(connection, state, 'DISPATCH_PENDING', authority=False)
        if refused:
            raise ValueError('original dispatch deadline or clock is terminal')
        with self.store.transaction() as connection:
            state = self._budget(connection, attempt_id)
            work = self._work(state, work_id)
            self._check_budget(state, state['authority_revision'], dispatch_owner=owner)
            if work['state'] not in ('START_INTENT', 'RUNNING') or work['observation_bytes_b64'] is not None:
                raise ValueError('durable unconsumed start intent required')
            current, deadline = self._dispatch_clock(connection, state, work, clock_source)
            refused = state['state'] not in ('PROVISIONAL', 'BOUND')
            if not refused:
                yield dict(token=token, clock=current, deadline_boottime_ns=deadline)
        if refused:
            raise ValueError('original dispatch deadline or clock is terminal')

    def acknowledge_dispatch(self, attempt_id, work_id, role, token, clock_source):
        """Record bounded request acceptance, never application completion.

        This clears only its owner's marker, including a late acknowledgement;
        recovery, VOID and terminal facts are unchanged and still gate authority.
        """
        from .campaign_budget import clock
        self._validate_recovery_token(token)
        if getattr(self.store._local, 'connection', None) is not None:
            raise ValueError('dispatch acknowledgement requires independent transaction')
        with self.store.transaction() as connection:
            state = self._budget(connection, attempt_id)
            row = next((r for r in state.get('dispatches', ()) if r['work_id'] == work_id and r['role'] == role), None)
            if row is None or row['owner_sha256'] != sha256(token):
                raise ValueError('dispatch owner differs')
            if row['acknowledged_clock'] is not None:
                return self._negative_budget_response(connection, state)
            current = clock(clock_source())
            before = state['state']
            self._observe_clock(state, current)
            row['acknowledged_clock'] = current
            return self._save_budget(connection, state, 'DISPATCH_ACKNOWLEDGED', authority=state['state'] != before)

    @staticmethod
    def _validate_recovery_token(token):
        if type(token) is not bytes or len(token) != 32:
            raise ValueError('ephemeral recovery owner token required')

    def _recovery_owner(self, state, work_id, token):
        self._validate_recovery_token(token)
        row = next((r for r in state.get('recoveries', ()) if r['work_id'] == work_id), None)
        if row is None or row['owner_sha256'] != sha256(token):
            raise ValueError('recovery owner differs')
        return row

    def _recovery_pending(self, state):
        from .campaign_budget import recovery_pending
        if recovery_pending(state):
            return True
        # Historical v3 claims remain readable but cannot acquire authority by
        # omitting the new projection. No successful completion is fabricated.
        known = {r['claim_sha256'] for r in state.get('recoveries', ())}
        with self.store.transaction() as connection:
            # GLOB, not LIKE: LIKE's '_' wildcard also matched 'supervision_controller'
            # (an enrollment object for a work named 'controller'), whose body has no
            # 'data' (S2 run 35459484982, KeyError 'data').
            rows = connection.execute("SELECT body,sha256 FROM full_campaign_objects WHERE attempt_id=? AND role GLOB 'supervision_control_*'", (state['attempt_id'],))
            for raw, identity in rows:
                event = parse_canonical_json(bytes(raw), label='control claim')
                if event['data']['slot'] == 'RECOVERY_OWNER' and identity not in known:
                    return True
        return False

    def complete_recovery(self, attempt_id, work_id, completion_bytes, *, recovery_owner_token):
        """Clear only this live owner's barrier after committed facts and absence."""
        from .campaign_budget import recovery_completion
        from .campaign_supervisor import parse_supervision_event
        doc = recovery_completion(completion_bytes, attempt_id=attempt_id, work_id=work_id)
        if getattr(self.store._local, 'connection', None) is not None:
            raise ValueError('recovery completion must commit independently')
        with self.store.transaction() as connection:
            state = self._budget(connection, attempt_id)
            row = self._recovery_owner(state, work_id, recovery_owner_token)
            if row['completion_bytes_b64'] is not None:
                if self._raw(row['completion_bytes_b64']) != completion_bytes:
                    raise ValueError('immutable recovery completion differs')
                return self._negative_budget_response(connection, state)
            if (row['observations_bytes_b64'] is None or doc['claim_sha256'] != row['claim_sha256']
                    or doc['observations_sha256'] != sha256(self._raw(row['observations_bytes_b64']))):
                raise ValueError('committed recovery facts required')
            saved = connection.execute('SELECT body FROM full_campaign_objects WHERE attempt_id=? AND role=?',
                (attempt_id, 'supervision_event_' + doc['cleanup_event_sha256'])).fetchone()
            if saved is None:
                raise ValueError('durable cleanup absence required')
            cleanup = parse_supervision_event(bytes(saved[0]))
            if (cleanup['work_id'] != work_id or cleanup['attempt_id'] != attempt_id or cleanup['kind'] != 'CLEANUP'
                    or cleanup['data']['status'] != 'ABSENT' or cleanup['clock'] != doc['clock']):
                raise ValueError('owned cleanup absence differs')
            before = state['state']
            self._observe_clock(state, doc['clock'])
            row['completion_bytes_b64'] = self._b64(completion_bytes)
            return self._save_budget(connection, state, 'RECOVERY_COMPLETE', authority=state['state'] != before)

    def retain_supervision_event(self, raw):
        from .campaign_supervisor import parse_supervision_event
        event = parse_supervision_event(raw)
        with self.store.transaction() as connection:
            state = self._budget(connection, event['attempt_id'])
            self._work(state, event['work_id'])
            if len(raw) > state['profile']['record_byte_limit']:
                raise ValueError('supervision event exceeds storage bound')
            role = 'supervision_event_' + sha256(raw)
            connection.execute('INSERT OR IGNORE INTO full_campaign_objects VALUES(?,?,?,?,?)',
                (event['attempt_id'], role, sha256(raw), len(raw), raw))

    def retain_supervision(self, attempt, work_id, raw):
        from .campaign_supervisor import parse_enrollment
        enrollment = parse_enrollment(raw)
        if enrollment['attempt_id'] != attempt or enrollment['work_id'] != work_id:
            raise ValueError('supervision enrollment identity differs')
        with self.store.transaction() as connection:
            state = self._budget(connection, attempt)
            self._work(state, work_id)
            if len(raw) > state['profile']['record_byte_limit']:
                raise ValueError('supervision enrollment exceeds storage bound')
            role = 'supervision_' + work_id
            prior = connection.execute('SELECT body FROM full_campaign_objects WHERE attempt_id=? AND role=?', (attempt, role)).fetchone()
            if prior is not None:
                if bytes(prior[0]) != raw:
                    raise ValueError('immutable supervision enrollment differs')
                return
            connection.execute('INSERT INTO full_campaign_objects VALUES(?,?,?,?,?)',
                               (attempt, role, sha256(raw), len(raw), raw))

    @staticmethod
    def _under_payload_slice(cgroup, payload_slice):
        """True when a retained absolute cgroup path lies strictly beneath the enrolled payload slice."""
        from pathlib import PurePosixPath
        parts = PurePosixPath(cgroup).parts
        return payload_slice in parts[:-1]

    def _payload_identity(self, connection, attempt, work_id):
        """Alive-verified PROCESS identities retained for a work, inside its enrolled payload slice.

        Returns None when the work carries no supervision enrollment (there is
        no payload slice to bind to), otherwise the list of qualifying PROCESS
        events. The guardian retains its own startup identity under the same
        kind/work_id, in the guardian unit's cgroup outside the payload slice;
        that proves the guardian, never the payload, and does not qualify.
        Event bodies are read only for the keys this rule needs.
        """
        from .campaign_supervisor import parse_enrollment
        saved = connection.execute('SELECT body FROM full_campaign_objects WHERE attempt_id=? AND role=?',
                                   (attempt, 'supervision_' + work_id)).fetchone()
        if saved is None:
            return None
        payload_slice = parse_enrollment(bytes(saved[0]))['scopes']['payload_slice']
        identities = []
        for raw, in connection.execute("SELECT body FROM full_campaign_objects WHERE attempt_id=? AND role GLOB 'supervision_event_*'", (attempt,)):
            event = parse_canonical_json(bytes(raw), label='supervision event')
            if (type(event) is dict and event.get('kind') == 'PROCESS' and event.get('work_id') == work_id
                    and type(event.get('data')) is dict and type(event['data'].get('cgroup')) is str
                    and self._under_payload_slice(event['data']['cgroup'], payload_slice)):
                identities.append(event)
        return identities

    def _require_payload_identity(self, connection, state, work):
        """S2-G5 R1: credit for an enrolled work needs a retained payload identity.

        The authoritative execution contract is the enrollment itself: a retained
        supervision_<work_id> object exists only because a supervised launch was
        prepared, so an enrolled non-admission work is by construction a
        container-supervised work and cannot reach CAPTURED/SIGNING_INTENT/
        COMPLETED without at least one alive-verified PROCESS event (either
        event version) inside its enrolled payload slice -- a linked signing
        retry included: on the host it runs a container like any other work.
        A work with no enrollment is a persistence-layer object (the S1-era
        store-only budget model, funding-model unit scenes) and is outside
        this rule entirely. The guardian's own PROCESS event is in the
        guardian unit's cgroup, outside the payload slice; it proves the
        guardian, never the payload. Event bodies are read only for the keys
        this rule needs, so both event versions bind identically here.
        """
        if work['phase'] == 'ADMISSION':
            return
        identities = self._payload_identity(connection, state['attempt_id'], work['work_id'])
        if identities is None:
            return  # no enrollment: a persistence-layer object, outside the rule
        if not identities:
            raise ValueError('alive-verified payload identity required before credit')

    def queue_diagnostic_void(self, raw):
        """Operator-role transport queues one bounded request, granting no authority."""
        request = parse_campaign_request(raw)
        if request['schema'] != 'qualification_campaign_request/v2' or request['operation'] != 'VOID':
            raise ValueError('versioned diagnostic cancellation required')
        attempt = request['attempt_id']
        with self.store.transaction() as connection:
            state = self._budget(connection, attempt)
            if state['profile']['schema'] not in ('qualification_campaign_budget_profile/v2', 'qualification_campaign_budget_profile/v3') or len(raw) > state['profile']['record_byte_limit']:
                raise ValueError('bounded metered cancellation required')
            prior = connection.execute("SELECT body FROM full_campaign_objects WHERE attempt_id=? AND role='pending_void'", (attempt,)).fetchone()
            if prior is not None and bytes(prior[0]) != raw:
                raise ValueError('pending cancellation differs')
            if prior is None:
                # A body already refused uncharged on the terminal campaign gets
                # no second attempt (A1): terminal is permanent and the retained
                # refusal is its answer. One indexed read; no verification.
                if connection.execute('SELECT 1 FROM full_campaign_objects WHERE attempt_id=? AND role=?',
                                      (attempt, VOID_TERMINAL_REFUSAL_PREFIX + sha256(raw))).fetchone():
                    raise ValueError(TERMINAL_BODY_REFUSED)
                connection.execute('INSERT INTO full_campaign_objects VALUES(?,?,?,?,?)',
                    (attempt, 'pending_void', sha256(raw), len(raw), raw))
            return encoded(self.diagnostic_status(attempt))

    def retained_object(self, attempt, role):
        """One bounded retained object; never the whole inventory."""
        with self.store.transaction() as connection:
            self.row(attempt)
            saved = connection.execute('SELECT body FROM full_campaign_objects WHERE attempt_id=? AND role=?',
                                       (attempt, role)).fetchone()
            if saved is None:
                raise KeyError(role)
            return bytes(saved[0])

    def _cancellation_pending(self, connection, attempt):
        """A durable operator body awaiting charged authentication; itself never authority."""
        if connection.execute("SELECT 1 FROM full_campaigns WHERE attempt_id=? AND validity='VALID'", (attempt,)).fetchone() is None:
            return False
        return connection.execute("SELECT 1 FROM full_campaign_objects WHERE attempt_id=? AND role='pending_void'",
                                  (attempt,)).fetchone() is not None

    def _admitted(self, connection, attempt):
        return connection.execute("SELECT 1 FROM full_campaign_objects WHERE attempt_id=? AND role='diagnostic_receipt'",
                                  (attempt,)).fetchone() is not None

    def _cancellation_barrier(self, connection, attempt, *, admitted_only):
        """Coordinator ruling 2026-09-19: a queued cancellation bars new positive authority.

        Fail-closed and transient: the fundable case authenticates the same
        request immediately; the unfundable case is already terminal or
        pending. It never sets validity and clears only by charged
        authentication. Before the receipt the admission guardian itself
        authenticates the body (finish_diagnostic_admission) and must keep
        binding and settling to reach that point, so the general gate is
        scoped to admitted campaigns; the two new-work grants refuse always.
        """
        if self._cancellation_pending(connection, attempt) and (not admitted_only or self._admitted(connection, attempt)):
            raise ValueError(CANCELLATION_PENDING)

    def _void_authentications(self, connection, attempt):
        rows = connection.execute('SELECT role, body FROM full_campaign_objects WHERE attempt_id=? AND role GLOB ? ORDER BY role',
                                  (attempt, VOID_AUTHENTICATION_PREFIX + '*'))
        result = []
        for role, raw in rows:
            doc = parse_void_authentication(bytes(raw))
            if doc['attempt_id'] != attempt or role != _void_role(VOID_AUTHENTICATION_PREFIX, doc['sequence']):
                raise ValueError('cancellation charge binding differs')
            result.append(doc)
        if [doc['sequence'] for doc in result] != list(range(1, len(result) + 1)):
            raise ValueError('cancellation charge sequence differs')
        return result

    def _void_refusals(self, connection, attempt):
        rows = connection.execute('SELECT role, body FROM full_campaign_objects WHERE attempt_id=? AND role GLOB ? ORDER BY role',
                                  (attempt, VOID_REFUSAL_PREFIX + '*'))
        result = []
        for role, raw in rows:
            doc = parse_void_refusal(bytes(raw))
            if doc['attempt_id'] != attempt or role != _void_role(VOID_REFUSAL_PREFIX, doc['sequence']):
                raise ValueError('cancellation refusal binding differs')
            result.append(doc)
        return result

    def _void_admission_refusals(self, connection, attempt):
        rows = connection.execute('SELECT role, body FROM full_campaign_objects WHERE attempt_id=? AND role GLOB ? ORDER BY role',
                                  (attempt, VOID_ADMISSION_REFUSAL_PREFIX + '*'))
        result = []
        for role, raw in rows:
            doc = parse_void_refusal(bytes(raw), schema=VOID_ADMISSION_REFUSAL_SCHEMA)
            if doc['attempt_id'] != attempt or role != _void_role(VOID_ADMISSION_REFUSAL_PREFIX, doc['sequence']):
                raise ValueError('admission cancellation refusal binding differs')
            result.append(doc)
        if [doc['sequence'] for doc in result] != list(range(1, len(result) + 1)):
            raise ValueError('admission cancellation refusal sequence differs')
        return result

    def _void_terminal_refusals(self, connection, attempt):
        rows = connection.execute('SELECT role, body FROM full_campaign_objects WHERE attempt_id=? AND role GLOB ? ORDER BY role',
                                  (attempt, VOID_TERMINAL_REFUSAL_PREFIX + '*'))
        result = []
        for role, raw in rows:
            doc = parse_void_refusal(bytes(raw), schema=VOID_TERMINAL_REFUSAL_SCHEMA)
            if doc['attempt_id'] != attempt or role != VOID_TERMINAL_REFUSAL_PREFIX + doc['request_sha256']:
                raise ValueError('terminal cancellation refusal binding differs')
            result.append(doc)
        result.sort(key=lambda doc: doc['sequence'])
        if [doc['sequence'] for doc in result] != list(range(1, len(result) + 1)):
            raise ValueError('terminal cancellation refusal sequence differs')
        return result

    def _refuse_admission_void(self, connection, attempt, request_bytes, reason, clock_doc):
        """Retain a pre-admission refusal (charged under the admission work) and clear the body."""
        sequence = len(self._void_admission_refusals(connection, attempt)) + 1
        refusal = encoded(dict(schema=VOID_ADMISSION_REFUSAL_SCHEMA, attempt_id=attempt, sequence=sequence,
            request_sha256=sha256(request_bytes), reason=(reason or 'refused')[:1024], clock=clock_doc))
        parse_void_refusal(refusal, schema=VOID_ADMISSION_REFUSAL_SCHEMA)
        connection.execute('INSERT INTO full_campaign_objects VALUES(?,?,?,?,?)',
                           (attempt, _void_role(VOID_ADMISSION_REFUSAL_PREFIX, sequence), sha256(refusal), len(refusal), refusal))
        connection.execute("DELETE FROM full_campaign_objects WHERE attempt_id=? AND role='pending_void' AND body=?",
                           (attempt, request_bytes))

    def void_authentication_charge(self, connection, attempt):
        """Settled controller CPU already spent on cancellation authentication."""
        return sum(doc['charge_cpu_ns'] for doc in self._void_authentications(connection, attempt))

    def claim_void_authentication(self, request_bytes, clock_bytes):
        """Durably charge one bounded authentication attempt before any verification.

        Mirrors claim_scheduler_bootstrap: bounded reads, one-use, a refusal
        returns compact historical status and leaves the queued body in place.
        The charge is settled at claim time from the original allowance and is
        never refunded; the outcome is recorded separately (VOID receipt or
        retained refusal). Returns (sequence, status): sequence is None when
        refused (pending funding/recovery/dispatch, insufficient allowance on a
        fundable campaign, VOID already, or no funding projection to charge);
        sequence 0 is the uncharged one-use attempt of a terminal-but-VALID
        campaign (A1); sequence >= 1 is a charged attempt.
        """
        from .campaign_budget import clock
        request = parse_campaign_request(request_bytes)
        if request['schema'] != 'qualification_campaign_request/v2' or request['operation'] != 'VOID':
            raise ValueError('versioned diagnostic cancellation required')
        observed = clock(clock_bytes)
        attempt = request['attempt_id']
        bound = void_authentication_bound()
        with self.store.transaction() as c:
            row = self.row(attempt)
            pending = c.execute("SELECT body FROM full_campaign_objects WHERE attempt_id=? AND role='pending_void'", (attempt,)).fetchone()
            if pending is None or bytes(pending[0]) != request_bytes:
                raise ValueError('queued cancellation body required')
            if not self._admitted(c, attempt):
                raise ValueError('post-admission cancellation authentication requires a retained receipt')
            doc = self._funding(c, attempt)
            # The transient windows keep their refusals: a sibling bootstrap claim,
            # a recovery or a dispatch closes on its own and the exact retry then
            # takes one of the outcomes below.
            if (row['validity'] != 'VALID' or doc is None or doc['bootstrap_pending_work_id'] is not None
                    or doc['recovery_pending'] or doc['dispatch_pending']):
                return None, encoded(self.diagnostic_status(attempt))
            if doc['state'] == 'BOUND' and doc['terminal_overlay'] is None:
                if bound['cpu_ns'] > doc['remaining_cpu_ns']:
                    return None, encoded(self.diagnostic_status(attempt))
                sequence = len(self._void_authentications(c, attempt)) + 1
                record = encoded(dict(schema=VOID_AUTHENTICATION_SCHEMA, attempt_id=attempt, sequence=sequence,
                    request_sha256=sha256(request_bytes), charge_cpu_ns=bound['cpu_ns'], wall_ns=bound['wall_ns'], clock=observed))
                parse_void_authentication(record)
                c.execute('INSERT INTO full_campaign_objects VALUES(?,?,?,?,?)',
                          (attempt, _void_role(VOID_AUTHENTICATION_PREFIX, sequence), sha256(record), len(record), record))
                doc.update(settled_cpu_ns=doc['settled_cpu_ns'] + bound['cpu_ns'],
                           remaining_cpu_ns=doc['remaining_cpu_ns'] - bound['cpu_ns'])
                _put_funding(c, 'full_campaign_funding', attempt, doc)
                return sequence, encoded(self.diagnostic_status(attempt))
            # S2-G4 A1: a VALID campaign whose budget is terminal or not BOUND
            # (IN_DOUBT, BUDGET_*, ABORTED, ...) has no allowance to charge and
            # no positive authority to protect, yet the operator's VOID intent
            # must remain recordable as a negative fact (spec 2.8; mirrors the
            # N1_ONLY VOID). One uncharged attempt under the caller's controller
            # guard: sequence 0 marks it, the outcome is retained by body digest
            # (refusal) or as the VOID receipt, and the queued body is cleared
            # either way; re-queueing the same digest is refused at queue time.
            return 0, encoded(self.diagnostic_status(attempt))

    def _charged_attempt(self, connection, attempt, sequence, request_bytes):
        claim = next((r for r in self._void_authentications(connection, attempt) if r['sequence'] == sequence), None)
        if claim is None or claim['request_sha256'] != sha256(request_bytes):
            raise ValueError('charged attempt differs')
        if any(r['sequence'] == sequence for r in self._void_refusals(connection, attempt)):
            raise ValueError('charged attempt already resolved')
        return claim

    def refuse_void_authentication(self, request_bytes, sequence, reason, clock_bytes):
        """Retain the refusal of one charged attempt and clear the queued body; no refund.

        Sequence 0 records the outcome of the uncharged terminal-campaign attempt
        (A1): the refusal is retained keyed by the body digest, so re-queueing
        the same body on that campaign is refused outright.
        """
        from .campaign_budget import clock
        request = parse_campaign_request(request_bytes)
        attempt = request['attempt_id']
        with self.store.transaction() as c:
            if sequence == 0:
                pending = c.execute("SELECT body FROM full_campaign_objects WHERE attempt_id=? AND role='pending_void'", (attempt,)).fetchone()
                if pending is None or bytes(pending[0]) != request_bytes:
                    raise ValueError('queued cancellation body required')
                refusal = encoded(dict(schema=VOID_TERMINAL_REFUSAL_SCHEMA, attempt_id=attempt,
                    sequence=len(self._void_terminal_refusals(c, attempt)) + 1,
                    request_sha256=sha256(request_bytes), reason=(reason or 'refused')[:1024], clock=clock(clock_bytes)))
                parse_void_refusal(refusal, schema=VOID_TERMINAL_REFUSAL_SCHEMA)
                c.execute('INSERT INTO full_campaign_objects VALUES(?,?,?,?,?)',
                          (attempt, VOID_TERMINAL_REFUSAL_PREFIX + sha256(request_bytes), sha256(refusal), len(refusal), refusal))
                c.execute("DELETE FROM full_campaign_objects WHERE attempt_id=? AND role='pending_void' AND body=?",
                          (attempt, request_bytes))
                return encoded(self.diagnostic_status(attempt))
            self._charged_attempt(c, attempt, sequence, request_bytes)
            refusal = encoded(dict(schema=VOID_REFUSAL_SCHEMA, attempt_id=attempt, sequence=sequence,
                request_sha256=sha256(request_bytes), reason=(reason or 'refused')[:1024], clock=clock(clock_bytes)))
            parse_void_refusal(refusal)
            c.execute('INSERT INTO full_campaign_objects VALUES(?,?,?,?,?)',
                      (attempt, _void_role(VOID_REFUSAL_PREFIX, sequence), sha256(refusal), len(refusal), refusal))
            c.execute("DELETE FROM full_campaign_objects WHERE attempt_id=? AND role='pending_void' AND body=?",
                      (attempt, request_bytes))
            return encoded(self.diagnostic_status(attempt))

    def complete_void_authentication(self, request_bytes, sequence, *, now):
        """Record VOID for one charged, verified attempt and clear the queued body.

        Sequence 0 completes the uncharged terminal-campaign attempt (A1): there
        is no charge object to bind, so the still-queued body is itself the
        one-use token.
        """
        request = parse_campaign_request(request_bytes)
        attempt = request['attempt_id']
        with self.store.transaction() as c:
            if sequence == 0:
                pending = c.execute("SELECT body FROM full_campaign_objects WHERE attempt_id=? AND role='pending_void'", (attempt,)).fetchone()
                if pending is None or bytes(pending[0]) != request_bytes:
                    raise ValueError('queued cancellation body required')
                receipt = self.void(request_bytes, now=now)
                c.execute("DELETE FROM full_campaign_objects WHERE attempt_id=? AND role='pending_void' AND body=?",
                          (attempt, request_bytes))
                return receipt
            self._charged_attempt(c, attempt, sequence, request_bytes)
            receipt = self.void(request_bytes, now=now)
            c.execute("DELETE FROM full_campaign_objects WHERE attempt_id=? AND role='pending_void' AND body=?",
                      (attempt, request_bytes))
            return receipt

    def inspect_unstarted_admission(self, attempt, clock_source):
        """Structurally absent admission: RESERVED and never prepared, so no OS effect exists.

        Returns None unless the admission work is RESERVED with no transition,
        enrollment, control slot, dispatch row or recovery row (START_INTENT
        precedes every OS effect, R1). Otherwise samples the trusted clock once
        and reports whether an exact SUBMIT_E1 retry may perform the first
        launch now: VALID, PROVISIONAL, no funding/recovery/dispatch pending,
        same boot, clock not backward and before the admission deadline.
        Grants nothing by itself. A funded campaign answers the common case
        (started work) from its bounded funding work row without decoding the
        snapshot.
        """
        from .campaign_budget import clock, dispatch_pending
        from .campaign_funding import _decode
        with self.store.transaction() as c:
            row = self.row(attempt)
            compact = c.execute("SELECT substr(body,1,2049) FROM full_campaign_funding_works WHERE attempt_id=? AND work_id='admission'",
                                (attempt,)).fetchone() if self._funding(c, attempt) is not None else None
            if compact is not None and _decode(bytes(compact[0]), 2048)['state'] != 'RESERVED':
                return None
            state = self._budget(c, attempt)
            work = next((w for w in state['works'] if w['work_id'] == 'admission'), None)
            if (work is None or work['state'] != 'RESERVED' or work['transitions']
                    or work['observation_bytes_b64'] is not None
                    or any(r['work_id'] == 'admission' for r in state.get('dispatches', ()))
                    or any(r['work_id'] == 'admission' for r in state.get('recoveries', ()))):
                return None
            roles = ['supervision_admission'] + ['supervision_control_' + sha256(encoded(['admission', slot]))
                                                 for slot in ('START_OWNER', 'START_CLIENT', 'RECOVERY_OWNER')]
            if c.execute('SELECT 1 FROM full_campaign_objects WHERE attempt_id=? AND role IN (?,?,?,?)',
                         (attempt, *roles)).fetchone():
                return None
            funding = self._funding(c, attempt)
            clock_bytes = clock_source()
            observed = clock(clock_bytes)
            # Expired: the original admission deadline has passed, the boot changed
            # or the trusted clock is unavailable. Nothing can ever launch it; the
            # same observation makes the budget terminal through recover_work.
            expired = (observed['boottime_ns'] is None or observed['boot_id'] != state['start_clock']['boot_id']
                       or observed['boottime_ns'] >= state['deadline_boottime_ns'])
            resumable = (row['validity'] == 'VALID' and state['state'] == 'PROVISIONAL' and not expired
                and (funding is None or (funding['bootstrap_pending_work_id'] is None and funding['terminal_overlay'] is None))
                and not self._recovery_pending(state) and not dispatch_pending(state)
                and state['last_clock']['boottime_ns'] is not None
                and state['last_clock']['boottime_ns'] <= observed['boottime_ns'])
            return dict(resumable=resumable, expired=expired and row['validity'] == 'VALID' and state['state'] in ('PROVISIONAL', 'BOUND'),
                        clock_bytes=clock_bytes, reservation_bytes=self._raw(work['reservation_bytes_b64']))

    def diagnostic_status(self, attempt):
        """Bounded historical projection; never reconstructs current eligibility."""
        from .campaign_protocol import PLAN_CHUNK_LIMIT
        with self.store.transaction() as connection:
            row = self.row(attempt)
            saved = connection.execute("SELECT body FROM full_campaign_objects WHERE attempt_id=? AND role='diagnostic_receipt'", (attempt,)).fetchone()
            funding = self._funding(connection, attempt)
            # A queued body is reported whenever it awaits authentication, before
            # or after the receipt; the charged attempt count and the last retained
            # refusal let the operator read why validity is still VALID.
            # Post-admission refusals always follow admission ones, so the last of
            # either kind is the most recent.
            refusals = self._void_refusals(connection, attempt) or self._void_admission_refusals(connection, attempt)
            cancellation = dict(
                void_pending=self._cancellation_pending(connection, attempt),
                void_authentication_attempts=len(self._void_authentications(connection, attempt)),
                void_refusal=None if not refusals else refusals[-1]['reason'])
            if funding is not None:
                return dict(schema='qualification_campaign_status/v2',validity=funding['validity'],
                    state='METERED_INSPECTION_REQUIRED' if funding['bootstrap_pending_work_id'] is not None or funding['terminal_overlay'] is not None else funding['state'],
                    receipt=None if saved is None else parse_canonical_json(bytes(saved[0]),label='diagnostic receipt'),
                    settled_cpu_ns=funding['settled_cpu_ns'],reserved_cpu_ns=funding['reserved_cpu_ns'],remaining_cpu_ns=funding['remaining_cpu_ns'],
                    historical=True,current_policy_eligible=False,dispatch_enabled=False, **cancellation)
            budget = connection.execute('SELECT substr(snapshot_bytes,1,?) FROM full_campaign_budgets WHERE attempt_id=?',
                                        (PLAN_CHUNK_LIMIT + 1, attempt)).fetchone()
            if budget is None:
                raise ValueError('no diagnostic metered history')
            state = parse_canonical_json(bytes(budget[0]), label='budget projection') if len(budget[0]) <= PLAN_CHUNK_LIMIT else {}
            return dict(schema='qualification_campaign_status/v2', validity=row['validity'],
                state=state.get('state', 'METERED_INSPECTION_REQUIRED'),
                receipt=None if saved is None else parse_canonical_json(bytes(saved[0]), label='diagnostic receipt'),
                settled_cpu_ns=state.get('settled_cpu_ns'), reserved_cpu_ns=state.get('reserved_cpu_ns'),
                remaining_cpu_ns=state.get('remaining_cpu_ns'), historical=True,
                current_policy_eligible=False, dispatch_enabled=False, **cancellation)

    def finish_diagnostic_admission(self, request_bytes, context, plan, observations_bytes, *, now, trusted_keys=None):
        """Trusted guardian only: settle/refuse or atomically retain admission.

        A refusal returns normally so terminal facts commit. Expensive retained
        revalidation and source proof belong in charged guardian work before this
        call; transport never constructs a verified context or supplies counters.
        """
        from .store import instant
        request = parse_campaign_request(request_bytes)
        document = parse_canonical_json(plan, label='campaign plan')
        if (request['schema'] != 'qualification_campaign_request/v2'
                or context.release.document['schema'] not in ('qualification_execution_release/v3', 'qualification_execution_release/v4', 'qualification_execution_release/v5')
                or context.attempt_id != request['attempt_id']
                or context.bundle_sha256 != request['bundle_sha256']
                or document['attempt_id'] != context.attempt_id
                or document['source_bundle_sha256'] != context.bundle_sha256
                or document['execution_release_sha256'] != context.release.sha256
                or document['contract_sha256'] != context.contract.contract_sha256
                or document['budget'] != parse_canonical_json(context.contract.canonical_bytes, label='frozen contract')['replay']['budget']
                or len(plan) > min(_CAMPAIGN_MAX_BYTES, context.profile.input_byte_limit)):
            raise ValueError('diagnostic admission binding differs')
        attempt = context.attempt_id
        with self.store.transaction() as connection:
            owner = self.row(attempt)
            if owner['request_bytes'] != request_bytes:
                raise ValueError('immutable diagnostic admission request differs')
            prior = self.diagnostic_status(attempt)
            if prior['receipt'] is not None:
                if prior['receipt']['plan_sha256'] != sha256(plan):
                    raise ValueError('immutable diagnostic plan differs')
                return prior
            self._funding_gate(connection, attempt)
            state = self._budget(connection, attempt)
            if (state['profile'] != context.release.document['campaign_budget_profile']
                    or state['profile']['installed_profile_sha256'] != context.profile.sha256):
                raise ValueError('installed diagnostic profile differs')
            pending = connection.execute("SELECT body FROM full_campaign_objects WHERE attempt_id=? AND role='pending_void'", (attempt,)).fetchone()
            if pending is not None and owner['validity'] == 'VALID':
                from ..contract import verify_detached_approval
                from .protocol import decode_base64
                if trusted_keys is None:
                    raise ValueError('fresh cancellation authentication required')
                cancel_raw = bytes(pending[0])
                cancel = parse_campaign_request(cancel_raw)
                domain = parse_canonical_json(context.domain.canonical_bytes, label='enrolled domain')
                # Authenticated under this charged admission work. A refusal is a
                # retained fact, never an admission failure: the body is cleared
                # and admission continues; only a verified enrolled key sets VOID.
                try:
                    approval = verify_detached_approval(decode_base64(cancel['operator_approval_bytes']),
                        trusted_keys=trusted_keys, expected_scope='VOID_QUALIFICATION_ATTEMPT',
                        expected_subject_sha256=sha256(encoded(dict(attempt_id=attempt, reason=cancel['reason'],
                            contract_sha256=context.contract.contract_sha256))),
                        expected_contract_sha256=context.contract.contract_sha256, now=now, allow_test_authority=True)
                    if (approval.authority_class != 'TEST_ONLY' or approval.key_id not in domain['freeze_key_ids']
                            or sha256(trusted_keys[approval.key_id].public_key) != domain['trusted_key_sha256'][approval.key_id]):
                        raise ValueError('pending cancellation authority is not enrolled')
                except (ValueError, KeyError) as refusal:
                    self._refuse_admission_void(connection, attempt, cancel_raw, str(refusal)[:1024],
                                                parse_canonical_json(observations_bytes, label='observation')['clock'])
                else:
                    self.void(cancel_raw, now=now)
                    owner = self.row(attempt)
            from .campaign_budget import dispatch_pending
            if dispatch_pending(state):
                return self.diagnostic_status(attempt)
            if self._recovery_pending(state):
                return self.diagnostic_status(attempt)
            if state['state'] == 'PROVISIONAL' and owner['validity'] == 'VALID':
                self.bind_budget(attempt, encoded(document['budget']), expected_revision=state['authority_revision'])
            state = parse_canonical_json(self.settle_work(attempt, 'admission', observations_bytes), label='settled admission')
            if state['state'] != 'BOUND' or state['validity'] != 'VALID':
                return self.diagnostic_status(attempt)
            clock = parse_canonical_json(observations_bytes, label='observation')['clock']
            state = parse_canonical_json(self.record_work_transition(attempt, 'admission', encoded(dict(
                schema='qualification_campaign_work_transition/v1', attempt_id=attempt, work_id='admission',
                state='COMPLETED', clock=clock, data={})), expected_revision=state['authority_revision']), label='admission completion')
            if state['state'] != 'BOUND' or state['validity'] != 'VALID':
                return self.diagnostic_status(attempt)
            receipt = encoded(dict(schema='qualification_campaign_admission_receipt/v2',
                campaign_id=owner['campaign_id'], attempt_id=attempt, state='ADMITTED_DIAGNOSTIC',
                authority_class='TEST_ONLY', dispatch_enabled=False, request_sha256=sha256(request_bytes),
                bundle_sha256=context.bundle_sha256, plan_sha256=sha256(plan), plan_byte_length=len(plan),
                contract_sha256=context.contract.contract_sha256, trust_domain_sha256=context.domain.sha256,
                execution_release_sha256=context.release.sha256, profile_sha256=context.profile.sha256,
                policy_sha256=context.policy.sha256, budget_sha256=sha256(encoded(document['budget'])),
                budget_profile_sha256=sha256(encoded(state['profile'])), start_clock=state['start_clock'],
                settled_cpu_ns=state['settled_cpu_ns'], admitted_at_utc=instant(now)))
            objects = {'diagnostic_receipt': receipt, 'plan': plan, 'bundle_index': context.retained_bundle_index,
                       **{'context_' + role: raw for role, raw in context.retained_bytes.items()}}
            for role, raw in objects.items():
                connection.execute('INSERT INTO full_campaign_objects VALUES(?,?,?,?,?)',
                                   (attempt, role, sha256(raw), len(raw), raw))
            # The campaign row's receipt column stops being the private
            # provisional intent: every later reader (CampaignStore.context and
            # the funded route's status) must see the admitted diagnostic
            # receipt without decoding retained objects.
            connection.execute('UPDATE full_campaigns SET receipt_bytes=? WHERE attempt_id=?',
                               (receipt, attempt))
            return self.diagnostic_status(attempt)

    def context(self, attempt, installed_release, keys, *, now):
        from .admission import verify_retained_bundle
        objects = self.objects(attempt)
        retained = {role.removeprefix('context_'): raw for role, raw in objects.items() if role.startswith('context_')}
        context = verify_retained_bundle(objects['bundle_index'], retained, installed_release, keys, now)
        receipt = self.status(attempt)['receipt']
        if context.bundle_sha256 != receipt['bundle_sha256'] or context.attempt_id != attempt:
            raise ValueError('retained campaign context differs')
        return context

    def chunk(self, request):
        with self.store.transaction() as connection:
            row = self.row(request['attempt_id'])
            plan = connection.execute("SELECT sha256,byte_length,substr(body,?,?) AS chunk FROM full_campaign_objects WHERE attempt_id=? AND role='plan'",
                (request['offset'] + 1, request['length'], request['attempt_id'])).fetchone()
            if plan is None:
                raise ValueError('campaign has no admitted plan')
            if plan['sha256'] != request['object_sha256']:
                raise ValueError('campaign plan membership differs')
            total, offset = plan['byte_length'], request['offset']
            if offset >= total:
                raise ValueError('chunk offset outside plan')
            raw = bytes(plan['chunk'])
            return encoded(dict(schema='qualification_campaign_plan_chunk/v1',
                attempt_id=row['attempt_id'], object_sha256=plan['sha256'], offset=offset,
                total_byte_length=total, byte_length=len(raw), bytes_b64=base64.b64encode(raw).decode('ascii')))

    def void_retry(self, request_bytes):
        request = parse_campaign_request(request_bytes)
        row = self.row(request['attempt_id'])
        if row['validity'] != 'VOID':
            return None
        if row['void_request'] != request_bytes:
            raise ValueError('campaign VOID request conflict')
        return bytes(row['void_receipt'])

    def void(self, request_bytes, *, now):
        from .store import instant
        request = parse_campaign_request(request_bytes)
        with self.store.transaction() as connection:
            retry = self.void_retry(request_bytes)
            if retry is not None:
                return retry
            row = self.row(request['attempt_id'])
            receipt = encoded(dict(schema='qualification_campaign_void_receipt/v1',
                campaign_id=row['campaign_id'], attempt_id=row['attempt_id'],
                validity='VOID', request_sha256=sha256(request_bytes), voided_at_utc=instant(now)))
            connection.execute("UPDATE full_campaigns SET validity='VOID',void_request=?,void_receipt=? WHERE attempt_id=?",
                (request_bytes, receipt, request['attempt_id']))
            if connection.execute('PRAGMA user_version').fetchone()[0] in (6, 7, 8):
                exists = connection.execute('SELECT 1 FROM full_campaign_budgets WHERE attempt_id=?', (request['attempt_id'],)).fetchone()
                if exists:
                    state = self._budget(connection, request['attempt_id'])
                    self._save_budget(connection, state, 'VOID', authority=True)
            return receipt

    def _budget(self, connection, attempt):
        from .protocol import identity
        identity(attempt)
        from ..journal_snapshot import parse_campaign_budget_snapshot
        if connection.execute('PRAGMA user_version').fetchone()[0] not in (6, 7, 8):
            raise ValueError('no metered campaign')
        row = connection.execute('SELECT snapshot_bytes FROM full_campaign_budgets WHERE attempt_id=?', (attempt,)).fetchone()
        if row is None:
            raise ValueError('dormant campaign has no metered history')
        return parse_campaign_budget_snapshot(bytes(row[0]))

    @staticmethod
    def _b64(raw):
        return base64.b64encode(raw).decode('ascii')

    @staticmethod
    def _raw(value):
        from .protocol import decode_base64
        return decode_base64(value)

    @staticmethod
    def _work(state, work_id):
        from .protocol import identity
        identity(work_id)
        for work in state['works']:
            if work['work_id'] == work_id:
                return work
        raise ValueError('unknown campaign work')

    @staticmethod
    def _totals(state):
        from .campaign_budget import remaining_cpu
        settled = [w['charge_cpu_ns'] for w in state['works'] if w['observation_bytes_b64'] is not None]
        reserved = [w['limits']['cpu_ns'] for w in state['works'] if w['observation_bytes_b64'] is None]
        cap = (state['budget']['maximum_cpu_seconds'] * 10**9 if state['budget'] is not None
               else state['profile']['phases']['ADMISSION']['cpu_ns'])
        state.update(settled_cpu_ns=sum(settled), reserved_cpu_ns=sum(reserved),
                     remaining_cpu_ns=remaining_cpu(cap, settled, reserved))

    def _save_budget(self, connection, state, kind, *, authority, funding_transfer=None):
        from ..journal_snapshot import encode_campaign_budget_snapshot
        if kind != 'BEGIN_ADMISSION':
            self._validate_funding_predecessor(connection, state)
        if funding_transfer is not None and kind != 'MATERIALIZE_BOOTSTRAP':
            raise ValueError('funding transfer requires materialization')
        self._totals(state)
        state['validity'] = self.row(state['attempt_id'])['validity']
        previous = state['event_head']
        state['accounting_revision'] += 1
        if authority:
            state['authority_revision'] += 1
        # The event carries the pre-event heads. No digest contains itself or a
        # later receipt/signature. Accounting and authority heads are distinct.
        body = encoded(dict(kind=kind, authority=authority, snapshot=state))
        head = sha256(previous.encode('ascii') + body)
        state['event_head'] = head
        if authority:
            state['authority_head'] = head
        raw = encode_campaign_budget_snapshot(state)
        connection.execute('INSERT INTO full_campaign_budgets VALUES(?,?) ON CONFLICT(attempt_id) DO UPDATE SET snapshot_bytes=excluded.snapshot_bytes',
                           (state['attempt_id'], raw))
        connection.execute('INSERT INTO full_campaign_budget_events VALUES(?,?,?,?,?)',
                           (state['attempt_id'], state['accounting_revision'], body, previous, head))
        self._project_funding(connection, state, enroll=kind == 'BEGIN_ADMISSION', transfer=funding_transfer)
        return self._negative_budget_response(connection, state)

    def _check_budget(self, state, expected_revision, *, allow_recovery_pending=False, dispatch_owner=None, negative_transition=False):
        from .campaign_budget import integer, dispatch_pending
        integer(expected_revision)
        if not negative_transition:
            with self.store.transaction() as connection:
                self._funding_gate(connection, state['attempt_id'])
                self._cancellation_barrier(connection, state['attempt_id'], admitted_only=True)
        if not allow_recovery_pending and self._recovery_pending(state):
            raise ValueError('campaign recovery pending')
        if not allow_recovery_pending and dispatch_pending(state, dispatch_owner):
            raise ValueError('campaign dispatch pending')
        if expected_revision != state['authority_revision']:
            raise ValueError('campaign authority revision conflict')
        if self.row(state['attempt_id'])['validity'] != 'VALID':
            raise ValueError('VOID campaign')
        if state['state'] not in ('PROVISIONAL', 'BOUND'):
            raise ValueError('terminal campaign budget')

    @staticmethod
    def _terminal(state, reason):
        if state['state'] in ('PROVISIONAL', 'BOUND'):
            state['state'] = reason

    def _observe_clock(self, state, value):
        from .campaign_budget import clock
        observed = clock(encoded(value))
        if (observed['boottime_ns'] is None or state['last_clock']['boottime_ns'] is None or observed['boot_id'] != state['start_clock']['boot_id'] or
                observed['boottime_ns'] < state['last_clock']['boottime_ns']):
            self._terminal(state, 'BUDGET_UNCERTAIN')
        elif observed['boottime_ns'] >= state['deadline_boottime_ns']:
            self._terminal(state, 'BUDGET_EXHAUSTED')
        state['last_clock'] = observed

    def begin_admission(self, request_bytes, profile_bytes, clock_bytes) -> bytes:
        from .profile import parse_campaign_budget_profile
        from .campaign_budget import clock, integer
        request = parse_campaign_request(request_bytes)
        if request['operation'] != 'SUBMIT_E1':
            raise ValueError('campaign submission required')
        profile = parse_campaign_budget_profile(profile_bytes)
        started = clock(clock_bytes)
        integer(started['boottime_ns'])
        from .protocol import identity
        identity(started['boot_id'])
        attempt = request['attempt_id']
        deadline = integer(started['boottime_ns'] + profile['phases']['ADMISSION']['wall_ns'])
        with self.store.transaction() as connection:
            existing = connection.execute('SELECT * FROM full_campaigns WHERE attempt_id=?', (attempt,)).fetchone()
            if existing is not None:
                state = self._budget(connection, attempt)
                if (existing['request_bytes'] != request_bytes or encoded(state['profile']) != profile_bytes
                        or encoded(state['start_clock']) != clock_bytes):
                    raise ValueError('immutable admission identity conflict')
                return self.budget_snapshot(attempt)
            if connection.execute('SELECT 1 FROM campaigns WHERE attempt_id=?', (attempt,)).fetchone():
                raise ValueError('N1 attempt cannot promote to metered campaign')
            if connection.execute('PRAGMA user_version').fetchone()[0] == 5:
                self.store.validate_layout(connection, 5)
                for statement in BUDGET_SCHEMA.split(';'):
                    if statement.strip():
                        connection.execute(statement)
                connection.execute('PRAGMA user_version=6')
            if profile['schema'] == 'qualification_campaign_budget_profile/v3' and connection.execute('PRAGMA user_version').fetchone()[0] == 6:
                self.store.validate_layout(connection, 6)
                for statement in FUNDING_SCHEMA.split(';'):
                    if statement.strip(): connection.execute(statement)
                connection.execute('PRAGMA user_version=7')
            receipt = encoded(dict(schema='qualification_campaign_provisional_intent/v1',
                attempt_id=attempt, request_sha256=sha256(request_bytes), profile_sha256=sha256(profile_bytes),
                start_clock=started, dispatch_enabled=False))
            connection.execute('INSERT INTO full_campaigns VALUES(?,?,?,?,?,?,?)',
                               (attempt, str(uuid.uuid4()), request_bytes, receipt, 'VALID', None, None))
            limits = profile['phases']['ADMISSION']
            reservation = encoded(dict(limits=limits, clock=started, input_sha256=sha256(request_bytes)))
            work = dict(work_id='admission', phase='ADMISSION', limits=limits,
                input_sha256=sha256(request_bytes), reservation_bytes_b64=self._b64(reservation),
                state='RESERVED', transitions=[], observation_bytes_b64=None, charge_cpu_ns=0)
            version = 'v2' if profile['schema'] in ('qualification_campaign_budget_profile/v2', 'qualification_campaign_budget_profile/v3') else 'v1'
            snapshot_version = 'v3' if version == 'v2' else 'v1'
            state = dict(schema='qualification_campaign_budget_snapshot/' + snapshot_version, attempt_id=attempt,
                request_sha256=sha256(request_bytes), profile=profile, budget=None,
                start_clock=started, last_clock=started, deadline_boottime_ns=deadline,
                state='PROVISIONAL', validity='VALID', authority_revision=0, accounting_revision=0,
                authority_head='0'*64, event_head='0'*64, campaign_scope_id=None,
                memory_peak_bytes=0, oom_events=0, works=[work],
                settled_cpu_ns=0, reserved_cpu_ns=0, remaining_cpu_ns=0)
            if profile['schema'] == 'qualification_campaign_budget_profile/v3':
                state.update(schema='qualification_campaign_budget_snapshot/v5', recoveries=[], dispatches=[])
            return self._save_budget(connection, state, 'BEGIN_ADMISSION', authority=True)

    def bind_budget(self, attempt_id, contract_budget_bytes, *, expected_revision, clock_bytes=None) -> bytes:
        from .campaign_budget import budget, integer, clock
        integer(expected_revision)
        fresh_clock = None if clock_bytes is None else clock(clock_bytes)
        binding = budget(contract_budget_bytes)
        with self.store.transaction() as connection:
            state = self._budget(connection, attempt_id)
            if fresh_clock is not None and state['profile']['schema'] not in ('qualification_campaign_budget_profile/v2', 'qualification_campaign_budget_profile/v3'):
                raise ValueError('fresh binding clock requires profile v2')
            if state['budget'] is not None:
                if encoded(state['budget']) != contract_budget_bytes:
                    raise ValueError('immutable budget binding conflict')
                if fresh_clock is not None:
                    self._check_budget(state, expected_revision)
                    self._observe_clock(state, fresh_clock)
                    return self._save_budget(connection, state, 'BIND_BUDGET_CLOCK', authority=True)
                return self._negative_budget_response(connection, state)
            self._check_budget(state, expected_revision)
            if fresh_clock is not None:
                self._observe_clock(state, fresh_clock)
            ceilings = state['profile']['phases'].values()
            cap = binding['maximum_cpu_seconds'] * 10**9
            if (sum(p['cpu_ns'] for p in ceilings) > cap or
                    sum(p['wall_ns'] for p in ceilings) > binding['maximum_wall_seconds'] * 10**9 or
                    max(p['memory_bytes'] for p in ceilings) > binding['maximum_memory_bytes']):
                self._terminal(state, 'BUDGET_EXHAUSTED')
            state['budget'] = binding
            state['deadline_boottime_ns'] = integer(state['start_clock']['boottime_ns'] + binding['maximum_wall_seconds'] * 10**9)
            if state['state'] == 'PROVISIONAL':
                state['state'] = 'BOUND'
            self._observe_clock(state, state['last_clock'])
            self._totals(state)
            # Charged authentications require the receipt, which follows this
            # binding; the term is zero here and kept for the one-view rule (A7).
            if state['settled_cpu_ns'] + state['reserved_cpu_ns'] + self.void_authentication_charge(connection, attempt_id) > cap:
                self._terminal(state, 'BUDGET_EXHAUSTED')
            return self._save_budget(connection, state, 'BIND_BUDGET', authority=True)

    @classmethod
    def _retry_parent(cls, work):
        reservation = parse_canonical_json(cls._raw(work['reservation_bytes_b64']), label='reservation')
        return reservation.get('signing_retry_of')

    @classmethod
    def _open_retries(cls, state, parent_id):
        return [w for w in state['works'] if cls._retry_parent(w) == parent_id and
                (w['state'] not in ('COMPLETED', 'ABORTED') or w['observation_bytes_b64'] is None)]

    @classmethod
    def _signing_intent(cls, work):
        return next((t for raw in work['transitions']
                     if (t := parse_canonical_json(cls._raw(raw), label='transition'))['state'] == 'SIGNING_INTENT'), None)

    def reserve_work(self, attempt_id, work_id, phase, limits_bytes, *, expected_revision) -> bytes:
        from .campaign_budget import clock, limits, integer, validate_work_id
        integer(expected_revision)
        from .protocol import fields, identity, digest
        # The admission work is reserved only by begin_admission; a work id that
        # would collide with a supervision object role is refused at this entry
        # (S2-G4 A9-3), before any state is read.
        validate_work_id(work_id)
        identity(phase)
        specification = parse_canonical_json(limits_bytes, label='work reservation')
        keys = {'limits', 'clock', 'input_sha256'}
        if type(specification) is dict and 'signing_retry_of' in specification:
            keys.add('signing_retry_of')
        fields(specification, keys)
        retry_of = specification.get('signing_retry_of')
        if 'signing_retry_of' in specification:
            identity(retry_of)
        limits(specification['limits']); clock(encoded(specification['clock'])); digest(specification['input_sha256'])
        with self.store.transaction() as connection:
            state = self._budget(connection, attempt_id)
            existing = next((w for w in state['works'] if w['work_id'] == work_id), None)
            if existing is not None:
                if existing['phase'] != phase or self._raw(existing['reservation_bytes_b64']) != limits_bytes:
                    raise ValueError('work reservation identity conflict')
                return self._negative_budget_response(connection, state)
            # A new work grant refuses a queued cancellation even before the receipt.
            self._cancellation_barrier(connection, attempt_id, admitted_only=False)
            self._check_budget(state, expected_revision)
            if state['state'] != 'BOUND' or phase not in state['profile']['phases']:
                raise ValueError('bound budget and installed phase required')
            if specification['limits'] != state['profile']['phases'][phase]:
                raise ValueError('reservation must use installed phase configuration')
            if retry_of is not None:
                parent = self._work(state, retry_of)
                intent = self._signing_intent(parent)
                if (parent['state'] != 'SIGNING_INTENT' or parent['observation_bytes_b64'] is None or
                        self._retry_parent(parent) is not None or phase != parent['phase'] or
                        phase in ('N1', 'N2', 'PART_A') or intent is None or
                        specification['input_sha256'] != sha256(self._raw(intent['data']['payload_bytes_b64'])) or
                        self._open_retries(state, retry_of)):
                    raise ValueError('signing retry requires a settled fixed intent and no open retry')
            if retry_of is None and phase in ('ADMISSION', 'N1', 'N2', 'PART_A') and any(w['phase'] == phase for w in state['works']):
                raise ValueError('compute phase already reserved; no replacement draws')
            self._observe_clock(state, specification['clock'])
            # S2-G4 A7: one allowance view. The snapshot's remaining is
            # pre-charge; the charged cancellation authentications live in
            # object rows and the funding projection. A reservation that fits
            # the snapshot but not the projection is refused the same way the
            # projection refuses it (terminal, no reservation, never a raise).
            if specification['limits']['cpu_ns'] > self._remaining_after_charges(connection, state):
                self._terminal(state, 'BUDGET_EXHAUSTED')
            if state['state'] == 'BOUND':
                if any(w['state'] in ('SIGNING_INTENT', 'SIGNED') and w['work_id'] != retry_of for w in state['works']):
                    raise ValueError('authority-changing work is serialized during signing')
                if retry_of is not None and state['schema'] == 'qualification_campaign_budget_snapshot/v1':
                    state['schema'] = 'qualification_campaign_budget_snapshot/v2'
                state['works'].append(dict(work_id=work_id, phase=phase, limits=specification['limits'],
                    input_sha256=specification['input_sha256'], reservation_bytes_b64=self._b64(limits_bytes),
                    state='RESERVED', transitions=[], observation_bytes_b64=None, charge_cpu_ns=0))
                state['works'].sort(key=lambda w: w['work_id'])
            return self._save_budget(connection, state, 'RESERVE_WORK',
                authority=retry_of is None or state['state'] != 'BOUND')

    def _observation(self, state, work, raw):
        from .campaign_budget import observation
        doc = observation(raw, attempt_id=state['attempt_id'], work_id=work['work_id'],
                          phase=work['phase'], profile=state['profile'])
        intents = [parse_canonical_json(self._raw(t), label='transition') for t in work['transitions']]
        start = next((t for t in intents if t['state'] == 'START_INTENT'), None)
        if start is None or any(doc[k] != start['data'][k] for k in ('campaign_scope_id', 'work_scope_id')):
            raise ValueError('observation has no matching owned work scope')
        return doc

    def _observe_resources(self, state, doc):
        if doc.get('termination_known') is False:
            self._terminal(state, 'BUDGET_UNCERTAIN')
        if doc['memory_peak_bytes'] is None or doc['oom_events'] is None:
            self._terminal(state, 'BUDGET_UNCERTAIN')
        if doc['memory_peak_bytes'] is not None:
            if doc['memory_peak_bytes'] < state['memory_peak_bytes']:
                self._terminal(state, 'BUDGET_UNCERTAIN')
            state['memory_peak_bytes'] = max(state['memory_peak_bytes'], doc['memory_peak_bytes'])
        if doc['oom_events'] is not None:
            if doc['oom_events'] < state['oom_events']:
                self._terminal(state, 'BUDGET_UNCERTAIN')
            state['oom_events'] = max(state['oom_events'], doc['oom_events'])
        memory_cap = (state['budget']['maximum_memory_bytes'] if state['budget'] else
                  state['profile']['phases']['ADMISSION']['memory_bytes'])
        if state['memory_peak_bytes'] > memory_cap or state['oom_events'] > 0:
            self._terminal(state, 'BUDGET_EXHAUSTED')

    def settle_work(self, attempt_id, work_id, observations_bytes) -> bytes:
        with self.store.transaction() as connection:
            state = self._budget(connection, attempt_id)
            work = self._work(state, work_id)
            doc = self._observation(state, work, observations_bytes)
            if work['observation_bytes_b64'] is not None:
                if self._raw(work['observation_bytes_b64']) != observations_bytes:
                    raise ValueError('settlement observation conflict')
                return self._negative_budget_response(connection, state)
            previous_state = state['state']
            self._observe_clock(state, doc['clock'])
            intent = next(parse_canonical_json(self._raw(t), label='start') for t in work['transitions'] if parse_canonical_json(self._raw(t), label='start')['state'] == 'START_INTENT')
            if (doc['clock']['boottime_ns'] is not None and doc['clock']['boot_id'] == state['start_clock']['boot_id'] and
                    doc['clock']['boottime_ns'] - intent['clock']['boottime_ns'] >= work['limits']['wall_ns']):
                self._terminal(state, 'BUDGET_EXHAUSTED')
            work['observation_bytes_b64'] = self._b64(observations_bytes)
            from .campaign_budget import observation_charge
            work['charge_cpu_ns'] = observation_charge(doc, work['limits'])
            if any(doc[key] is None for key in ('cpu_ns', 'memory_peak_bytes', 'oom_events')):
                self._terminal(state, 'BUDGET_UNCERTAIN')
            self._observe_resources(state, doc)
            if work['charge_cpu_ns'] > work['limits']['cpu_ns']:
                self._terminal(state, 'BUDGET_EXHAUSTED')
            return self._save_budget(connection, state, 'SETTLE_WORK', authority=state['state'] != previous_state)

    def record_work_transition(self, attempt_id, work_id, transition_bytes, *, expected_revision) -> bytes:
        from .campaign_budget import transition, integer
        integer(expected_revision)
        doc = transition(transition_bytes, attempt_id, work_id)
        target, data = doc['state'], doc['data']
        allowed = WORK_PREDECESSORS
        with self.store.transaction() as connection:
            state = self._budget(connection, attempt_id)
            work = self._work(state, work_id)
            for saved in work['transitions']:
                previous = parse_canonical_json(self._raw(saved), label='saved transition')
                if previous['state'] == target:
                    if self._raw(saved) != transition_bytes:
                        raise ValueError('immutable work transition conflict')
                    return self._negative_budget_response(connection, state)
            self._check_budget(state, expected_revision, allow_recovery_pending=target in ('IN_DOUBT', 'ABORTED'), negative_transition=target in ('IN_DOUBT', 'ABORTED'))
            if work['state'] not in allowed[target]:
                raise ValueError('illegal work transition; no reexecution')
            retry_of = self._retry_parent(work)
            if retry_of is not None:
                parent = self._work(state, retry_of)
                if parent['state'] != 'SIGNING_INTENT' or target not in ('START_INTENT', 'RUNNING', 'COMPLETED'):
                    raise ValueError('linked retry is deterministic signing work only')
            if target in ('SIGNED', 'COMPLETED') and self._open_retries(state, work_id):
                raise ValueError('signing retry must finish and settle before candidate finalization')
            if any(w['work_id'] not in (work_id, retry_of) and w['state'] in ('SIGNING_INTENT', 'SIGNED') for w in state['works']):
                raise ValueError('authority-changing work is serialized during signing')
            self._observe_clock(state, doc['clock'])
            starts = [parse_canonical_json(self._raw(t), label='start') for t in work['transitions']]
            intent = next((t for t in starts if t['state'] == 'START_INTENT'), None)
            if (intent is not None and work['observation_bytes_b64'] is None and doc['clock']['boottime_ns'] is not None and doc['clock']['boot_id'] == state['start_clock']['boot_id'] and
                    doc['clock']['boottime_ns'] - intent['clock']['boottime_ns'] >= work['limits']['wall_ns']):
                self._terminal(state, 'BUDGET_EXHAUSTED')
            if state['state'] not in ('PROVISIONAL', 'BOUND'):
                return self._save_budget(connection, state, 'CLOCK_TERMINAL', authority=True)
            if target in ('START_INTENT', 'RUNNING') and work['observation_bytes_b64'] is not None:
                raise ValueError('settled work cannot resume')
            # S2-G4 A2: settlement closes the window in which credit can be
            # established. CAPTURED and SIGNING_INTENT are credit facts the
            # supervisor records before settling; after the observation is
            # retained they are refused outright. COMPLETED needs the
            # settlement (below) and is accepted only for credit established
            # before it (CAPTURED/SIGNED), or for the two capture-less
            # productions: the admission (no container; its guardian is the
            # supervised process) and a linked deterministic signing retry.
            if target in ('CAPTURED', 'SIGNING_INTENT') and work['observation_bytes_b64'] is not None:
                raise ValueError('settled work cannot acquire credit')
            if (target == 'COMPLETED' and work['state'] not in ('CAPTURED', 'SIGNED')
                    and work['phase'] != 'ADMISSION' and retry_of is None):
                raise ValueError('completion requires credit established before settlement')
            # S2-G4 A5: the identity gate, store-side.
            if target in ('CAPTURED', 'SIGNING_INTENT', 'COMPLETED'):
                self._require_payload_identity(connection, state, work)
            if target == 'START_INTENT':
                if state['campaign_scope_id'] not in (None, data['campaign_scope_id']):
                    raise ValueError('common campaign memory scope required')
                for other in state['works']:
                    for saved in other['transitions']:
                        item = parse_canonical_json(self._raw(saved), label='saved transition')
                        if item['state'] == 'START_INTENT' and item['data']['work_scope_id'] == data['work_scope_id']:
                            raise ValueError('work scope already attributed')
                state['campaign_scope_id'] = data['campaign_scope_id']
            if target in ('CAPTURED', 'SIGNING_INTENT', 'SIGNED') and len(transition_bytes) > state['profile']['record_byte_limit']:
                raise ValueError('work metadata exceeds bounded storage')
            if target == 'COMPLETED' and work['phase'] in ('N1', 'N2', 'PART_A') and work['state'] not in ('CAPTURED', 'SIGNED'):
                raise ValueError('compute completion requires saved capture')
            if target == 'COMPLETED' and work['observation_bytes_b64'] is None:
                raise ValueError('settlement required before finalization')
            if target in ('IN_DOUBT', 'ABORTED'):
                self._terminal(state, target)
            work['state'] = target
            work['transitions'].append(self._b64(transition_bytes))
            return self._save_budget(connection, state, target, authority=retry_of is None and target != 'SIGNED')

    def recover_work(self, attempt_id, work_id, observations_bytes, *, recovery_owner_token=None) -> bytes:
        """Commit current recovery facts independently of immutable settlement.

        RESERVED takes a clock. Started work takes an attributed observation;
        an existing final charge is never replaced by a later observation.
        Only linked deterministic signing retries may close an interrupted
        process without making the original captured operation IN_DOUBT.
        """
        from .campaign_budget import clock
        if getattr(self.store._local, 'connection', None) is not None:
            raise ValueError('recovery must commit before cleanup; outer transaction forbidden')
        with self.store.transaction() as connection:
            state = self._budget(connection, attempt_id)
            work = self._work(state, work_id)
            if recovery_owner_token is not None:
                owner = self._recovery_owner(state, work_id, recovery_owner_token)
                if owner['completion_bytes_b64'] is not None:
                    raise ValueError('completed recovery cannot resume active work')
            before = encoded(state)
            old_state = state['state']
            if work['state'] == 'RESERVED':
                self._observe_clock(state, clock(observations_bytes))
            elif work['observation_bytes_b64'] is None:
                self.settle_work(attempt_id, work_id, observations_bytes)
                state = self._budget(connection, attempt_id)
                work = self._work(state, work_id)
                before = encoded(state)
                old_state = state['state']
            else:
                doc = self._observation(state, work, observations_bytes)
                self._observe_clock(state, doc['clock'])
                self._observe_resources(state, doc)
                saved = parse_canonical_json(self._raw(work['observation_bytes_b64']), label='settlement')
                if doc['cpu_ns'] is not None and doc['cpu_ns'] != saved['cpu_ns']:
                    self._terminal(state, 'BUDGET_UNCERTAIN')
            changed_work = work['state'] in ('START_INTENT', 'RUNNING')
            if changed_work:
                if self._retry_parent(work) is not None:
                    work['state'] = 'ABORTED'
                else:
                    work['state'] = 'IN_DOUBT'
                    self._terminal(state, 'IN_DOUBT')
            if recovery_owner_token is not None:
                owner = self._recovery_owner(state, work_id, recovery_owner_token)
                owner['observations_bytes_b64'] = self._b64(observations_bytes)
            if encoded(state) == before:
                return self._negative_budget_response(connection, state)
            return self._save_budget(connection, state, 'RECOVER_WORK',
                authority=state['state'] != old_state or (changed_work and self._retry_parent(work) is None))

    def _remaining_after_charges(self, connection, state):
        """The projection's remaining allowance: snapshot remaining less the charged authentications."""
        return max(0, state['remaining_cpu_ns'] - self.void_authentication_charge(connection, state['attempt_id']))

    def budget_snapshot(self, attempt_id) -> bytes:
        """The campaign's budget snapshot, whose totals are pre-charge.

        `settled_cpu_ns` / `reserved_cpu_ns` / `remaining_cpu_ns` sum the
        per-work facts only. Charged cancellation authentications (S2-G2) are
        one-use object rows outside the snapshot; `diagnostic_status`,
        `scheduler_status` and the funding projection fold them in and are the
        authoritative allowance view. Every store-side grant (`reserve_work`,
        `bind_budget`, `claim_scheduler_bootstrap`, `claim_void_authentication`)
        consults the charged total; a reader of this snapshot's remaining must
        not treat it as spendable.
        """
        from ..journal_snapshot import encode_campaign_budget_snapshot
        with self.store.transaction() as connection:
            self._funding_gate(connection, attempt_id)
            return encode_campaign_budget_snapshot(self._budget(connection, attempt_id))

    def _budget_integrity(self, connection):
        from ..journal_snapshot import parse_campaign_budget_snapshot
        from .profile import parse_campaign_budget_profile
        from .campaign_budget import budget, clock
        for row in connection.execute('SELECT * FROM full_campaign_budgets'):
            state = parse_campaign_budget_snapshot(bytes(row['snapshot_bytes']))
            if state['profile']['schema'] == 'qualification_campaign_budget_profile/v3' and connection.execute('PRAGMA user_version').fetchone()[0] not in (7, 8):
                raise ValueError('funding profile requires database v7')
            owner = self.row(row['attempt_id'])
            receipt = parse_canonical_json(owner['receipt_bytes'], label='campaign receipt')
            if receipt['schema'] == 'qualification_campaign_admission_receipt/v2':
                # The admitted campaign's row carries the diagnostic receipt;
                # it must be byte-identical to the retained receipt object.
                saved = connection.execute("SELECT body FROM full_campaign_objects WHERE attempt_id=? AND role='diagnostic_receipt'",
                                           (state['attempt_id'],)).fetchone()
                if saved is None or bytes(saved[0]) != owner['receipt_bytes']:
                    raise ValueError('admitted receipt integrity differs')
            else:
                expected_receipt = encoded(dict(schema='qualification_campaign_provisional_intent/v1',
                    attempt_id=state['attempt_id'], request_sha256=state['request_sha256'],
                    profile_sha256=sha256(encoded(state['profile'])), start_clock=state['start_clock'],
                    dispatch_enabled=False))
                if owner['receipt_bytes'] != expected_receipt:
                    raise ValueError('provisional receipt integrity differs')
            # The v2 diagnostic receipt binds the budget profile through its own
            # budget_profile_sha256; its profile_sha256 is the installed
            # execution profile the admission verified against.
            profile_binding = (receipt['budget_profile_sha256']
                               if receipt['schema'] == 'qualification_campaign_admission_receipt/v2'
                               else receipt['profile_sha256'])
            if (state['attempt_id'] != owner['attempt_id'] or state['validity'] != owner['validity'] or
                    state['request_sha256'] != sha256(owner['request_bytes']) or
                    profile_binding != sha256(encoded(state['profile'])) or
                    receipt['start_clock'] != state['start_clock']):
                raise ValueError('metered campaign binding integrity differs')
            parse_campaign_budget_profile(encoded(state['profile']))
            clock(encoded(state['start_clock'])); clock(encoded(state['last_clock']))
            if state['budget'] is not None:
                budget(encoded(state['budget']))
            from .campaign_budget import recovery_completion
            from .campaign_supervisor import parse_supervision_event
            for recovery in state.get('recoveries', ()):
                role = 'supervision_control_' + sha256(encoded([recovery['work_id'], 'RECOVERY_OWNER']))
                claim = connection.execute('SELECT body FROM full_campaign_objects WHERE attempt_id=? AND role=?',
                                           (state['attempt_id'], role)).fetchone()
                if claim is None or sha256(bytes(claim[0])) != recovery['claim_sha256']:
                    raise ValueError('recovery claim projection differs')
                if recovery['completion_bytes_b64'] is not None:
                    completion = recovery_completion(self._raw(recovery['completion_bytes_b64']),
                        attempt_id=state['attempt_id'], work_id=recovery['work_id'])
                    cleanup = connection.execute('SELECT body FROM full_campaign_objects WHERE attempt_id=? AND role=?',
                        (state['attempt_id'], 'supervision_event_' + completion['cleanup_event_sha256'])).fetchone()
                    if cleanup is None:
                        raise ValueError('recovery completion cleanup absent')
                    event = parse_supervision_event(bytes(cleanup[0]))
                    if (event['work_id'] != recovery['work_id'] or event['kind'] != 'CLEANUP'
                            or event['data']['status'] != 'ABSENT' or event['clock'] != completion['clock']):
                        raise ValueError('recovery completion cleanup differs')
            previous, authority_head, revision, authority_revision = '0'*64, '0'*64, 0, 0
            saved = None
            for event in connection.execute('SELECT * FROM full_campaign_budget_events WHERE attempt_id=? ORDER BY sequence', (row['attempt_id'],)):
                body = parse_canonical_json(event['body'], label='budget event')
                from .protocol import fields
                fields(body, {'kind', 'authority', 'snapshot'})
                if type(body['authority']) is not bool:
                    raise ValueError('event authority flag differs')
                revision += 1
                authority_revision += int(body['authority'])
                saved = body['snapshot']
                if (event['sequence'] != revision or event['previous_sha256'] != previous or
                        event['sha256'] != sha256(previous.encode('ascii') + event['body']) or
                        saved['event_head'] != previous or saved['authority_head'] != authority_head or
                        saved['accounting_revision'] != revision or saved['authority_revision'] != authority_revision):
                    raise ValueError('budget event chain integrity differs')
                previous = event['sha256']
                if body['authority']:
                    authority_head = previous
                saved.update(event_head=previous, authority_head=authority_head)
                parse_campaign_budget_snapshot(encoded(saved))
            if saved != state:
                raise ValueError('budget projection integrity differs')
            totals = {k: state[k] for k in ('settled_cpu_ns', 'reserved_cpu_ns', 'remaining_cpu_ns')}
            self._totals(state)
            if totals != {k: state[k] for k in totals}:
                raise ValueError('budget arithmetic integrity differs')

    def _diagnostic_integrity(self, owner, state, objects):
        receipt = parse_canonical_json(objects['diagnostic_receipt'], label='diagnostic receipt')
        plan = parse_canonical_json(objects['plan'], label='diagnostic plan')
        index = parse_canonical_json(objects['bundle_index'], label='diagnostic bundle')
        work = self._work(state, 'admission')
        if (receipt['schema'] != 'qualification_campaign_admission_receipt/v2'
                or receipt['state'] != 'ADMITTED_DIAGNOSTIC' or receipt['dispatch_enabled'] is not False
                or receipt['attempt_id'] != owner['attempt_id'] or receipt['campaign_id'] != owner['campaign_id']
                or receipt['request_sha256'] != sha256(owner['request_bytes'])
                or receipt['bundle_sha256'] != sha256(objects['bundle_index'])
                or receipt['plan_sha256'] != sha256(objects['plan'])
                or receipt['plan_byte_length'] != len(objects['plan'])
                or receipt['budget_sha256'] != sha256(encoded(plan['budget']))
                or plan['budget'] != parse_canonical_json(objects['context_contract'], label='retained contract')['replay']['budget']
                or receipt['budget_profile_sha256'] != sha256(encoded(state['profile']))
                or receipt['profile_sha256'] != state['profile']['installed_profile_sha256']
                or receipt['start_clock'] != state['start_clock']
                or work['state'] != 'COMPLETED' or work['observation_bytes_b64'] is None):
            raise ValueError('diagnostic admission integrity differs')
        if set(objects) != {'diagnostic_receipt', 'plan', 'bundle_index'} | {'context_' + entry['role'] for entry in index['entries']}:
            raise ValueError('diagnostic retained inventory differs')
        for entry in index['entries']:
            raw = objects['context_' + entry['role']]
            if sha256(raw) != entry['sha256'] or len(raw) != entry['byte_length']:
                raise ValueError('diagnostic retained input differs')
        for name in ('contract_sha256', 'trust_domain_sha256', 'execution_release_sha256', 'policy_sha256'):
            if receipt[name] != plan[name]:
                raise ValueError('diagnostic plan binding differs')

    def integrity(self, connection):
        version = connection.execute('PRAGMA user_version').fetchone()[0]
        if version in (6, 7, 8):
            self._budget_integrity(connection)
            self._funding_integrity(connection)
        if version == 8:
            self._checkpoint_integrity(connection)
        for row in connection.execute('SELECT * FROM full_campaigns'):
            if connection.execute('SELECT 1 FROM campaigns WHERE attempt_id=?', (row['attempt_id'],)).fetchone():
                raise ValueError('cross-capability attempt collision')
            request = parse_campaign_request(row['request_bytes'])
            receipt = parse_canonical_json(row['receipt_bytes'], label='campaign receipt')
            if receipt.get('schema') in ('qualification_campaign_provisional_intent/v1',
                                         'qualification_campaign_admission_receipt/v2'):
                state = self._budget(connection, row['attempt_id'])
                retained = self.objects(row['attempt_id'])
                from .campaign_supervisor import parse_enrollment, parse_supervision_event
                if 'pending_void' in retained:
                    pending = parse_campaign_request(retained.pop('pending_void'))
                    if (pending['schema'] != 'qualification_campaign_request/v2' or pending['operation'] != 'VOID'
                            or pending['attempt_id'] != row['attempt_id']
                            or state['profile']['schema'] not in ('qualification_campaign_budget_profile/v2', 'qualification_campaign_budget_profile/v3')):
                        raise ValueError('pending cancellation binding differs')
                # Charged cancellation attempts exist only for funded, admitted
                # campaigns; every refusal pairs with the charge it resolved.
                charges = {}
                for name in tuple(retained):
                    if name.startswith(VOID_AUTHENTICATION_PREFIX):
                        charge = parse_void_authentication(retained.pop(name))
                        if (charge['attempt_id'] != row['attempt_id'] or name != _void_role(VOID_AUTHENTICATION_PREFIX, charge['sequence'])
                                or state['profile']['schema'] != FUNDED_PROFILE or 'diagnostic_receipt' not in retained):
                            raise ValueError('cancellation charge binding differs')
                        charges[charge['sequence']] = charge
                if sorted(charges) != list(range(1, len(charges) + 1)):
                    raise ValueError('cancellation charge sequence differs')
                for name in tuple(retained):
                    if name.startswith(VOID_REFUSAL_PREFIX):
                        refusal = parse_void_refusal(retained.pop(name))
                        charge = charges.get(refusal['sequence'])
                        if (refusal['attempt_id'] != row['attempt_id'] or name != _void_role(VOID_REFUSAL_PREFIX, refusal['sequence'])
                                or charge is None or charge['request_sha256'] != refusal['request_sha256']):
                            raise ValueError('cancellation refusal binding differs')
                # Pre-admission refusals are charged under the admission work: no
                # charge object, a contiguous sequence of their own, funded or not.
                admission_refusals = []
                for name in tuple(retained):
                    if name.startswith(VOID_ADMISSION_REFUSAL_PREFIX):
                        refusal = parse_void_refusal(retained.pop(name), schema=VOID_ADMISSION_REFUSAL_SCHEMA)
                        if refusal['attempt_id'] != row['attempt_id'] or name != _void_role(VOID_ADMISSION_REFUSAL_PREFIX, refusal['sequence']):
                            raise ValueError('admission cancellation refusal binding differs')
                        admission_refusals.append(refusal['sequence'])
                if sorted(admission_refusals) != list(range(1, len(admission_refusals) + 1)):
                    raise ValueError('admission cancellation refusal sequence differs')
                # Terminal-campaign refusals (A1) are uncharged: post-admission,
                # keyed by the body digest, contiguous in their own sequence.
                for name in tuple(retained):
                    if name.startswith(VOID_TERMINAL_REFUSAL_PREFIX):
                        refusal = parse_void_refusal(retained.pop(name), schema=VOID_TERMINAL_REFUSAL_SCHEMA)
                        if (refusal['attempt_id'] != row['attempt_id']
                                or name != VOID_TERMINAL_REFUSAL_PREFIX + refusal['request_sha256']
                                or 'diagnostic_receipt' not in retained):
                            raise ValueError('terminal cancellation refusal binding differs')
                self._void_terminal_refusals(connection, row['attempt_id'])
                payload_slices, process_events = {}, []
                for name in tuple(retained):
                    if name.startswith('supervision_control_'):
                        event = parse_supervision_event(retained.pop(name))
                        if (event['kind'] != 'CONTROL' or event['attempt_id'] != row['attempt_id']
                                or name != 'supervision_control_' + sha256(encoded([event['work_id'], event['data']['slot']]))):
                            raise ValueError('durable control slot binding differs')
                        self._work(state, event['work_id'])
                    elif name.startswith('supervision_event_'):
                        raw_event = retained.pop(name)
                        event = parse_supervision_event(raw_event)
                        if event['attempt_id'] != row['attempt_id'] or name != 'supervision_event_' + sha256(raw_event):
                            raise ValueError('supervision event projection differs')
                        self._work(state, event['work_id'])
                        if event['kind'] == 'PROCESS':
                            process_events.append(event)
                    elif name.startswith('supervision_'):
                        enrollment = parse_enrollment(retained.pop(name))
                        if enrollment['attempt_id'] != row['attempt_id'] or name != 'supervision_' + enrollment['work_id']:
                            raise ValueError('supervision enrollment projection differs')
                        self._work(state, enrollment['work_id'])
                        payload_slices[enrollment['work_id']] = enrollment['scopes']['payload_slice']
                # S2-G5 R1: the identity rule binds by execution contract, not
                # evidence presence. Every credited work other than the
                # admission that carries an enrollment (by construction a
                # container-supervised work -- the enrollment is retained only
                # by a prepared supervised launch) must hold at least one
                # alive-verified PROCESS identity (either event version) inside
                # its enrolled payload slice; the guardian's own identity,
                # outside it, never counts. Stripping every PROCESS row from a
                # credited journal therefore fails reopen. An un-enrolled
                # credited work is a persistence-layer object and is outside
                # the rule. Same scope as record_work_transition's rule.
                for work in state['works']:
                    if (work['phase'] == 'ADMISSION'
                            or work['state'] not in ('CAPTURED', 'SIGNING_INTENT', 'SIGNED', 'COMPLETED')):
                        continue
                    payload_slice = payload_slices.get(work['work_id'])
                    if payload_slice is None:
                        continue
                    if not any(e['work_id'] == work['work_id'] and self._under_payload_slice(e['data']['cgroup'], payload_slice)
                               for e in process_events):
                        raise ValueError('credited work lacks alive-verified payload identity')
                if retained:
                    if 'diagnostic_receipt' not in retained:
                        raise ValueError('provisional intent cannot claim admitted objects')
                    self._diagnostic_integrity(row, state, dict(retained, diagnostic_receipt=row['receipt_bytes'])
                                               if bytes(retained['diagnostic_receipt']) != row['receipt_bytes']
                                               else retained)
                if row['validity'] == 'VOID':
                    if type(row['void_request']) is not bytes or type(row['void_receipt']) is not bytes:
                        raise ValueError('metered VOID receipt absent')
                    void = parse_campaign_request(row['void_request'])
                    saved = parse_canonical_json(row['void_receipt'], label='VOID')
                    if void['attempt_id'] != row['attempt_id'] or saved['request_sha256'] != sha256(row['void_request']):
                        raise ValueError('metered VOID integrity differs')
                elif row['void_request'] is not None or row['void_receipt'] is not None:
                    raise ValueError('metered validity integrity differs')
                continue
            objects = self.objects(row['attempt_id'])
            plan = parse_canonical_json(objects['plan'], label='campaign plan')
            index = parse_canonical_json(objects['bundle_index'], label='retained index')
            if (request['operation'] != 'SUBMIT_E1' or request['attempt_id'] != row['attempt_id']
                    or receipt['campaign_id'] != row['campaign_id'] or receipt['attempt_id'] != row['attempt_id']
                    or receipt['request_sha256'] != sha256(row['request_bytes'])
                    or receipt['bundle_sha256'] != request['bundle_sha256']
                    or receipt['bundle_sha256'] != sha256(objects['bundle_index'])
                    or receipt['plan_sha256'] != sha256(objects['plan'])
                    or receipt['plan_byte_length'] != len(objects['plan'])
                    or receipt['budget_sha256'] != sha256(encoded(plan['budget']))
                    or receipt['dispatch_enabled'] is not False or receipt['state'] != 'ADMITTED'):
                raise ValueError('campaign receipt integrity differs')
            if set(objects) != {'plan', 'bundle_index'} | {'context_' + entry['role'] for entry in index['entries']}:
                raise ValueError('campaign retained inventory differs')
            for entry in index['entries']:
                raw = objects['context_' + entry['role']]
                if sha256(raw) != entry['sha256'] or len(raw) != entry['byte_length']:
                    raise ValueError('campaign retained identity differs')
            for name in ('contract_sha256', 'trust_domain_sha256', 'execution_release_sha256', 'policy_sha256'):
                if receipt[name] != plan[name]:
                    raise ValueError('campaign plan receipt binding differs')
            if row['validity'] == 'VALID':
                if row['void_request'] is not None or row['void_receipt'] is not None:
                    raise ValueError('campaign validity projection differs')
            else:
                if type(row['void_request']) is not bytes or type(row['void_receipt']) is not bytes:
                    raise ValueError('campaign VOID receipt absent')
                void = parse_campaign_request(row['void_request'])
                saved = parse_canonical_json(row['void_receipt'], label='void receipt')
                if (void['operation'] != 'VOID' or void['attempt_id'] != row['attempt_id']
                        or saved['request_sha256'] != sha256(row['void_request'])
                        or saved['campaign_id'] != row['campaign_id'] or saved['validity'] != 'VOID'):
                    raise ValueError('campaign VOID integrity differs')
        for row in connection.execute('SELECT * FROM full_campaign_objects'):
            if sha256(row['body']) != row['sha256'] or len(row['body']) != row['byte_length']:
                raise ValueError('campaign object integrity differs')

# Added only when the first private metered intent is created. Opening an exact
# v4/v5 journal alone never fabricates a budget history for dormant campaigns.
BUDGET_SCHEMA = '''
CREATE TABLE IF NOT EXISTS full_campaign_budgets (
 attempt_id TEXT PRIMARY KEY REFERENCES full_campaigns(attempt_id), snapshot_bytes BLOB NOT NULL);
CREATE TABLE IF NOT EXISTS full_campaign_budget_events (
 attempt_id TEXT NOT NULL REFERENCES full_campaign_budgets(attempt_id), sequence INTEGER NOT NULL,
 body BLOB NOT NULL, previous_sha256 TEXT NOT NULL, sha256 TEXT NOT NULL,
 PRIMARY KEY(attempt_id,sequence));
'''
