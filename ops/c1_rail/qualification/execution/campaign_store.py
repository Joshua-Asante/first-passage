"""Dormant campaigns sharing ExecutionStore's lock, database and validity authority.

Only the protected service supplies verified contexts and trusted observations.
Private metered intents do not activate a release or launch a process.
"""
import base64
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


class CampaignStore:
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
            if connection.execute('PRAGMA user_version').fetchone()[0] == 6:
                exists = connection.execute('SELECT 1 FROM full_campaign_budgets WHERE attempt_id=?', (request['attempt_id'],)).fetchone()
                if exists:
                    state = self._budget(connection, request['attempt_id'])
                    self._save_budget(connection, state, 'VOID', authority=True)
            return receipt

    def _budget(self, connection, attempt):
        from .protocol import identity
        identity(attempt)
        from ..journal_snapshot import parse_campaign_budget_snapshot
        if connection.execute('PRAGMA user_version').fetchone()[0] != 6:
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

    def _save_budget(self, connection, state, kind, *, authority):
        from ..journal_snapshot import encode_campaign_budget_snapshot
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
        return raw

    def _check_budget(self, state, expected_revision):
        from .campaign_budget import integer
        integer(expected_revision)
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
            state = dict(schema='qualification_campaign_budget_snapshot/v1', attempt_id=attempt,
                request_sha256=sha256(request_bytes), profile=profile, budget=None,
                start_clock=started, last_clock=started, deadline_boottime_ns=deadline,
                state='PROVISIONAL', validity='VALID', authority_revision=0, accounting_revision=0,
                authority_head='0'*64, event_head='0'*64, campaign_scope_id=None,
                memory_peak_bytes=0, oom_events=0, works=[work],
                settled_cpu_ns=0, reserved_cpu_ns=0, remaining_cpu_ns=0)
            return self._save_budget(connection, state, 'BEGIN_ADMISSION', authority=True)

    def bind_budget(self, attempt_id, contract_budget_bytes, *, expected_revision) -> bytes:
        from .campaign_budget import budget, integer
        integer(expected_revision)
        binding = budget(contract_budget_bytes)
        with self.store.transaction() as connection:
            state = self._budget(connection, attempt_id)
            if state['budget'] is not None:
                if encoded(state['budget']) != contract_budget_bytes:
                    raise ValueError('immutable budget binding conflict')
                return self.budget_snapshot(attempt_id)
            self._check_budget(state, expected_revision)
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
            if state['settled_cpu_ns'] + state['reserved_cpu_ns'] > cap:
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
        from .campaign_budget import clock, limits, integer
        integer(expected_revision)
        from .protocol import fields, identity, digest
        identity(work_id)
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
                return self.budget_snapshot(attempt_id)
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
            if specification['limits']['cpu_ns'] > state['remaining_cpu_ns']:
                self._terminal(state, 'BUDGET_EXHAUSTED')
            if state['state'] == 'BOUND':
                if any(w['state'] in ('SIGNING_INTENT', 'SIGNED') and w['work_id'] != retry_of for w in state['works']):
                    raise ValueError('authority-changing work is serialized during signing')
                if retry_of is not None:
                    state['schema'] = 'qualification_campaign_budget_snapshot/v2'
                state['works'].append(dict(work_id=work_id, phase=phase, limits=specification['limits'],
                    input_sha256=specification['input_sha256'], reservation_bytes_b64=self._b64(limits_bytes),
                    state='RESERVED', transitions=[], observation_bytes_b64=None, charge_cpu_ns=0))
                state['works'].sort(key=lambda w: w['work_id'])
            return self._save_budget(connection, state, 'RESERVE_WORK',
                authority=retry_of is None or state['state'] != 'BOUND')

    def _observation(self, state, work, raw):
        from .campaign_budget import clock, integer
        from .protocol import fields, identity
        doc = fields(parse_canonical_json(raw, label='trusted campaign observation'), {
            'schema', 'attempt_id', 'work_id', 'clock', 'campaign_scope_id', 'work_scope_id',
            'cpu_ns', 'memory_peak_bytes', 'oom_events'})
        if (doc['schema'] != 'qualification_campaign_observation/v1' or
                doc['attempt_id'] != state['attempt_id'] or doc['work_id'] != work['work_id']):
            raise ValueError('observation identity differs')
        clock(encoded(doc['clock']))
        for key in ('campaign_scope_id', 'work_scope_id'):
            identity(doc[key])
        for key in ('cpu_ns', 'memory_peak_bytes', 'oom_events'):
            if doc[key] is not None:
                integer(doc[key])
        intents = [parse_canonical_json(self._raw(t), label='transition') for t in work['transitions']]
        start = next((t for t in intents if t['state'] == 'START_INTENT'), None)
        if start is None or any(doc[k] != start['data'][k] for k in ('campaign_scope_id', 'work_scope_id')):
            raise ValueError('observation has no matching owned work scope')
        return doc

    def _observe_resources(self, state, doc):
        if doc['memory_peak_bytes'] is None or doc['oom_events'] is None:
            self._terminal(state, 'BUDGET_UNCERTAIN')
        if doc['memory_peak_bytes'] is not None:
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
                return self.budget_snapshot(attempt_id)
            previous_state = state['state']
            self._observe_clock(state, doc['clock'])
            intent = next(parse_canonical_json(self._raw(t), label='start') for t in work['transitions'] if parse_canonical_json(self._raw(t), label='start')['state'] == 'START_INTENT')
            if (doc['clock']['boottime_ns'] is not None and doc['clock']['boot_id'] == state['start_clock']['boot_id'] and
                    doc['clock']['boottime_ns'] - intent['clock']['boottime_ns'] >= work['limits']['wall_ns']):
                self._terminal(state, 'BUDGET_EXHAUSTED')
            work['observation_bytes_b64'] = self._b64(observations_bytes)
            work['charge_cpu_ns'] = work['limits']['cpu_ns'] if doc['cpu_ns'] is None else doc['cpu_ns']
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
                    return self.budget_snapshot(attempt_id)
            self._check_budget(state, expected_revision)
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

    def recover_work(self, attempt_id, work_id, observations_bytes) -> bytes:
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
            if encoded(state) == before:
                return self.budget_snapshot(attempt_id)
            return self._save_budget(connection, state, 'RECOVER_WORK',
                authority=state['state'] != old_state or (changed_work and self._retry_parent(work) is None))

    def budget_snapshot(self, attempt_id) -> bytes:
        from ..journal_snapshot import encode_campaign_budget_snapshot
        with self.store.transaction() as connection:
            return encode_campaign_budget_snapshot(self._budget(connection, attempt_id))

    def _budget_integrity(self, connection):
        from ..journal_snapshot import parse_campaign_budget_snapshot
        from .profile import parse_campaign_budget_profile
        from .campaign_budget import budget, clock
        for row in connection.execute('SELECT * FROM full_campaign_budgets'):
            state = parse_campaign_budget_snapshot(bytes(row['snapshot_bytes']))
            owner = self.row(row['attempt_id'])
            receipt = parse_canonical_json(owner['receipt_bytes'], label='provisional receipt')
            expected_receipt = encoded(dict(schema='qualification_campaign_provisional_intent/v1',
                attempt_id=state['attempt_id'], request_sha256=state['request_sha256'],
                profile_sha256=sha256(encoded(state['profile'])), start_clock=state['start_clock'],
                dispatch_enabled=False))
            if owner['receipt_bytes'] != expected_receipt:
                raise ValueError('provisional receipt integrity differs')
            if (state['attempt_id'] != owner['attempt_id'] or state['validity'] != owner['validity'] or
                    state['request_sha256'] != sha256(owner['request_bytes']) or
                    receipt['profile_sha256'] != sha256(encoded(state['profile'])) or
                    receipt['start_clock'] != state['start_clock']):
                raise ValueError('metered campaign binding integrity differs')
            parse_campaign_budget_profile(encoded(state['profile']))
            clock(encoded(state['start_clock'])); clock(encoded(state['last_clock']))
            if state['budget'] is not None:
                budget(encoded(state['budget']))
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

    def integrity(self, connection):
        if connection.execute('PRAGMA user_version').fetchone()[0] == 6:
            self._budget_integrity(connection)
        for row in connection.execute('SELECT * FROM full_campaigns'):
            if connection.execute('SELECT 1 FROM campaigns WHERE attempt_id=?', (row['attempt_id'],)).fetchone():
                raise ValueError('cross-capability attempt collision')
            request = parse_campaign_request(row['request_bytes'])
            receipt = parse_canonical_json(row['receipt_bytes'], label='campaign receipt')
            if receipt.get('schema') == 'qualification_campaign_provisional_intent/v1':
                state = self._budget(connection, row['attempt_id'])
                if self.objects(row['attempt_id']):
                    raise ValueError('provisional intent cannot claim admitted objects')
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
