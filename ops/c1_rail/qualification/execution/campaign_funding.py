"""Compact pre-bootstrap funding in ExecutionStore's transaction authority.

Full history is projected only by already-funded writers. Claim reads a fixed
number of bounded indexed rows and never decodes the campaign snapshot.
"""

import secrets
from ..contract import canonical_json_bytes as encoded, parse_canonical_json
from .protocol import fields, identity, digest, sha256
from .campaign_budget import clock, integer, PHASES, dispatch_pending, validate_work_id

SCHEMA = '''
CREATE TABLE IF NOT EXISTS full_campaign_funding (
 attempt_id TEXT PRIMARY KEY REFERENCES full_campaign_budgets(attempt_id),
 body BLOB NOT NULL CHECK(length(body)<=8192));
CREATE TABLE IF NOT EXISTS full_campaign_funding_works (
 attempt_id TEXT NOT NULL REFERENCES full_campaign_funding(attempt_id),
 work_id TEXT NOT NULL, body BLOB NOT NULL CHECK(length(body)<=2048),
 PRIMARY KEY(attempt_id,work_id));
CREATE TABLE IF NOT EXISTS full_campaign_bootstraps (
 attempt_id TEXT NOT NULL REFERENCES full_campaign_funding(attempt_id),
 work_id TEXT NOT NULL, request_bytes BLOB NOT NULL CHECK(length(request_bytes)<=1024),
 body BLOB NOT NULL CHECK(length(body)<=4096), PRIMARY KEY(attempt_id,work_id));
'''
PROFILE = 'qualification_campaign_budget_profile/v3'
WORK_PHASES = {
    'admission': 'ADMISSION',
    'probe_worker': 'N1',
    'probe_g5': 'N1_G5',
    'probe_result': 'RESULT',
    'probe_seal': 'SEAL',
    # S3 dispatch roles (D2/D4): the genuine N1 compute work and the metered G5
    # assessment work. Admitted only under the /v5 dispatch release (the service's
    # startup-fixed gate) and only after the admission work completed.
    'n1_worker': 'N1',
    'n1_g5': 'N1_G5',
}
WORK_ROLES = tuple(WORK_PHASES)
PROBES = ('noop', 'cpu', 'descendants', 'memory', 'wall', 'intent', 'controller_cpu')
DISPATCH_ROLES = ('n1_worker', 'n1_g5')
PHASE_BY_ROLE = {role: phase for role, phase in WORK_PHASES.items() if role != 'admission'}


def parse_request(raw):
    if type(raw) is not bytes or len(raw) > 1024:
        raise ValueError('bounded scheduler request required')
    document = parse_canonical_json(raw, label='scheduler request')
    if type(document) is dict and 'fault' not in document:
        # S2-era producers (the accepted supervision suite among them) predate
        # the diagnostic fault input; an absent fault is absent -- inject it
        # rather than widen the closed set for them.
        document = dict(document, fault=None)
    doc = fields(
        document,
        {'schema', 'attempt_id', 'work_id', 'role', 'probe', 'signing_retry_of', 'fault'},
    )
    if (
        doc['schema'] != 'qualification_campaign_schedule_request/v1'
        or type(doc['role']) is not str
        or doc['role'] not in PHASE_BY_ROLE
    ):
        raise ValueError('private fixed scheduler role required')
    if doc['probe'] not in PROBES:
        raise ValueError('fixed scheduler probe required')
    if doc['probe'] == 'intent' and doc['role'] != 'probe_seal':
        raise ValueError('intent requires seal probe')
    identity(doc['attempt_id'])
    # The private route never names the fixed admission work or an identity
    # that collides with a supervision object role (S2-G4 A9-3).
    validate_work_id(doc['work_id'])
    if doc['signing_retry_of'] is not None:
        validate_work_id(doc['signing_retry_of'])
    # TEST_ONLY diagnostic fault input (coordinator-authorized for the E06/E07
    # scene): the only fault holds the assessment commit open between its two
    # durable transactions so a killed qg5 unit lands in the observable window.
    # Refused for every role but the g5 dispatch work; absent means absent.
    if doc['fault'] not in (None, 'hold_after_intent'):
        raise ValueError('installed diagnostic fault required')
    if doc['fault'] is not None and doc['role'] != 'n1_g5':
        raise ValueError('diagnostic fault requires the g5 dispatch role')
    return doc


def _decode(raw, limit):
    from .profile import parse_campaign_budget_profile
    from .campaign_budget import limits

    if type(raw) is not bytes or len(raw) > limit:
        raise ValueError('bounded funding record required')
    doc = parse_canonical_json(raw, label='funding record')
    if type(doc) is not dict:
        raise ValueError('closed funding object required')
    schema = doc.get('schema')
    if schema == 'qualification_campaign_funding/v1':
        fields(
            doc,
            {
                'schema',
                'attempt_id',
                'profile',
                'snapshot_accounting_revision',
                'snapshot_authority_revision',
                'snapshot_event_head',
                'snapshot_authority_head',
                'state',
                'validity',
                'start_clock',
                'last_clock',
                'deadline_boottime_ns',
                'settled_cpu_ns',
                'reserved_cpu_ns',
                'remaining_cpu_ns',
                'reserved_compute_phases',
                'signing_work_ids',
                'recovery_pending',
                'dispatch_pending',
                'bootstrap_pending_work_id',
                'terminal_overlay',
            },
        )
        if doc['state'] not in (
            'PROVISIONAL',
            'BOUND',
            'BUDGET_EXHAUSTED',
            'BUDGET_UNCERTAIN',
            'IN_DOUBT',
            'ABORTED',
            'N2_READY',
            'N1_FAILED',
        ) or doc['validity'] not in ('VALID', 'VOID'):
            raise ValueError('funding state differs')
        profile = parse_campaign_budget_profile(encoded(doc['profile']))
        if profile['schema'] != PROFILE:
            raise ValueError('fresh funding profile required')
        for key in (
            'snapshot_accounting_revision',
            'snapshot_authority_revision',
            'deadline_boottime_ns',
            'settled_cpu_ns',
            'reserved_cpu_ns',
            'remaining_cpu_ns',
        ):
            integer(doc[key])
        for key in ('snapshot_event_head', 'snapshot_authority_head'):
            digest(doc[key])
        for key in ('start_clock', 'last_clock'):
            clock(encoded(doc[key]))
        for key in ('recovery_pending', 'dispatch_pending'):
            if type(doc[key]) is not bool:
                raise ValueError('exact funding barrier boolean required')
        if doc['bootstrap_pending_work_id'] is not None:
            identity(doc['bootstrap_pending_work_id'])
        phases = doc['reserved_compute_phases']
        if (
            type(phases) is not list
            or len(phases) > 4
            or any(
                type(p) is not str or p not in ('ADMISSION', 'N1', 'N2', 'PART_A') for p in phases
            )
            or phases != sorted(set(phases))
        ):
            raise ValueError('finite compute phase set required')
        names = doc['signing_work_ids']
        if type(names) is not list or len(names) > 1:
            raise ValueError('single signing owner required')
        for name in names:
            identity(name)
        overlay = doc['terminal_overlay']
        if overlay is not None:
            fields(overlay, {'state', 'clock'})
            if overlay['state'] not in ('BUDGET_EXHAUSTED', 'BUDGET_UNCERTAIN'):
                raise ValueError('funding terminal overlay differs')
            clock(encoded(overlay['clock']))
            if doc['state'] != overlay['state']:
                raise ValueError('funding terminal state differs')
    elif schema == 'qualification_campaign_funding_work/v1':
        fields(
            doc,
            {
                'schema',
                'attempt_id',
                'work_id',
                'phase',
                'state',
                'input_sha256',
                'settled',
                'signing_retry_of',
                'signing_intent_sha256',
                'open_retry_work_ids',
            },
        )
        if (
            doc['state']
            not in (
                'RESERVED',
                'START_INTENT',
                'RUNNING',
                'CAPTURED',
                'SIGNING_INTENT',
                'SIGNED',
                'COMPLETED',
                'IN_DOUBT',
                'ABORTED',
            )
            or type(doc['settled']) is not bool
        ):
            raise ValueError('funding work state differs')
        if doc['signing_intent_sha256'] is not None:
            digest(doc['signing_intent_sha256'])
        names = doc['open_retry_work_ids']
        if type(names) is not list or len(names) > 1:
            raise ValueError('single open retry required')
        for name in names:
            identity(name)
    elif schema == 'qualification_campaign_bootstrap/v1':
        fields(
            doc,
            {
                'schema',
                'attempt_id',
                'work_id',
                'request_sha256',
                'owner_sha256',
                'profile_sha256',
                'phase',
                'limits',
                'clock',
                'input_sha256',
                'signing_retry_of',
                'claimed_event_head',
                'claimed_authority_head',
                'state',
            },
        )
        if doc['state'] not in ('PENDING', 'MATERIALIZED'):
            raise ValueError('funding intent state differs')
        for key in (
            'request_sha256',
            'owner_sha256',
            'profile_sha256',
            'claimed_event_head',
            'claimed_authority_head',
        ):
            digest(doc[key])
        limits(doc['limits'])
        clock(encoded(doc['clock']))
    else:
        raise ValueError('funding schema differs')
    identity(doc['attempt_id'])
    if 'work_id' in doc:
        identity(doc['work_id'])
        digest(doc['input_sha256'])
        if doc['phase'] not in PHASES:
            raise ValueError('installed funding phase required')
        if doc['signing_retry_of'] is not None:
            identity(doc['signing_retry_of'])
    return doc


def _overlay_clock(current, retained):
    """last_clock under a terminal overlay is monotone within one boot.

    The claim path persists this value and the projection reconstructs it, so
    both must apply the same rule. An incomparable (changed-boot or unavailable)
    or backward observed clock survives only as the overlay fact.
    """
    if (
        current['boot_id'] == retained['boot_id']
        and current['boottime_ns'] is not None
        and retained['boottime_ns'] is not None
        and current['boottime_ns'] < retained['boottime_ns']
    ):
        return retained
    return current


def _put(connection, table, attempt, doc, work=None, request=None):
    raw = encoded(doc)
    if table == 'full_campaign_funding':
        _decode(raw, 8192)
        connection.execute(
            'INSERT INTO full_campaign_funding VALUES(?,?) ON CONFLICT(attempt_id) DO UPDATE SET body=excluded.body',
            (attempt, raw),
        )
    elif table == 'full_campaign_funding_works':
        _decode(raw, 2048)
        connection.execute(
            'INSERT INTO full_campaign_funding_works VALUES(?,?,?) ON CONFLICT(attempt_id,work_id) DO UPDATE SET body=excluded.body',
            (attempt, work, raw),
        )
    else:
        _decode(raw, 4096)
        connection.execute(
            'INSERT INTO full_campaign_bootstraps VALUES(?,?,?,?) ON CONFLICT(attempt_id,work_id) DO UPDATE SET body=excluded.body',
            (attempt, work, request, raw),
        )


class FundingStoreMixin:
    """Funding operations mixed into CampaignStore, which supplies the
    budget/work/raw projections and the token, clock and save helpers."""

    def _funding(self, c, attempt):
        identity(attempt)
        if c.execute('PRAGMA user_version').fetchone()[0] not in (7, 8):
            return None
        row = c.execute(
            'SELECT substr(body,1,8193) FROM full_campaign_funding WHERE attempt_id=?', (attempt,)
        ).fetchone()
        if row is None:
            return None
        doc = _decode(bytes(row[0]), 8192)
        if doc['schema'] != 'qualification_campaign_funding/v1' or doc['attempt_id'] != attempt:
            raise ValueError('funding row identity differs')
        return doc

    def _bootstrap(self, c, attempt, work):
        row = c.execute(
            'SELECT substr(request_bytes,1,1025),substr(body,1,4097) FROM full_campaign_bootstraps WHERE attempt_id=? AND work_id=?',
            (attempt, work),
        ).fetchone()
        if row is None:
            return None
        raw = bytes(row[0])
        request = parse_request(raw)
        doc = _decode(bytes(row[1]), 4096)
        if (
            doc['schema'] != 'qualification_campaign_bootstrap/v1'
            or doc['attempt_id'] != attempt
            or doc['work_id'] != work
            or request['attempt_id'] != attempt
            or request['work_id'] != work
            or doc['request_sha256'] != sha256(raw)
        ):
            raise ValueError('funding request row identity differs')
        return raw, doc

    def _funding_gate(self, c, attempt):
        doc = self._funding(c, attempt)
        if doc is None:
            exists = c.execute(
                'SELECT 1 FROM full_campaign_budgets WHERE attempt_id=?', (attempt,)
            ).fetchone()
            if exists and self._budget(c, attempt)['profile']['schema'] == PROFILE:
                raise ValueError('enrolled funding projection absent')
        if doc is not None and (
            doc['bootstrap_pending_work_id'] is not None or doc['terminal_overlay'] is not None
        ):
            raise ValueError('campaign funding pending; current authority unavailable')

    def _funding_projection(self, state, previous=None):
        pending = None if previous is None else previous['bootstrap_pending_work_id']
        overlay = None if previous is None else previous['terminal_overlay']
        rows = {}
        for work in state['works']:
            intent = self._signing_intent(work)
            rows[work['work_id']] = {
                'schema': 'qualification_campaign_funding_work/v1',
                'attempt_id': state['attempt_id'],
                'work_id': work['work_id'],
                'phase': work['phase'],
                'state': work['state'],
                'input_sha256': work['input_sha256'],
                'settled': work['observation_bytes_b64'] is not None,
                'signing_retry_of': self._retry_parent(work),
                'signing_intent_sha256': (
                    None
                    if intent is None
                    else sha256(self._raw(intent['data']['payload_bytes_b64']))
                ),
                'open_retry_work_ids': [
                    w['work_id'] for w in self._open_retries(state, work['work_id'])
                ],
            }
        # Store enforces at most one open linked retry. Never accept a growing list.
        if any(len(w['open_retry_work_ids']) > 1 for w in rows.values()):
            raise ValueError('ambiguous open retry funding')
        doc = {
            'schema': 'qualification_campaign_funding/v1',
            'attempt_id': state['attempt_id'],
            'profile': state['profile'],
            'snapshot_accounting_revision': state['accounting_revision'],
            'snapshot_authority_revision': state['authority_revision'],
            'snapshot_event_head': state['event_head'],
            'snapshot_authority_head': state['authority_head'],
            'state': state['state'],
            'validity': state['validity'],
            'start_clock': state['start_clock'],
            'last_clock': state['last_clock'],
            'deadline_boottime_ns': state['deadline_boottime_ns'],
            'settled_cpu_ns': state['settled_cpu_ns'],
            'reserved_cpu_ns': state['reserved_cpu_ns'],
            'remaining_cpu_ns': state['remaining_cpu_ns'],
            'reserved_compute_phases': sorted(
                {
                    w['phase']
                    for w in state['works']
                    if w['phase'] in ('ADMISSION', 'N1', 'N2', 'PART_A')
                }
            ),
            'signing_work_ids': sorted(
                w['work_id'] for w in state['works'] if w['state'] in ('SIGNING_INTENT', 'SIGNED')
            ),
            'recovery_pending': self._recovery_pending(state),
            'dispatch_pending': dispatch_pending(state),
            'bootstrap_pending_work_id': pending,
            'terminal_overlay': overlay,
        }
        if len(doc['signing_work_ids']) > 1:
            raise ValueError('ambiguous signing authority')
        if overlay is not None:
            doc['state'] = overlay['state']
            doc['last_clock'] = _overlay_clock(doc['last_clock'], overlay['clock'])
        if pending is not None:
            with self.store.transaction() as c:
                retained = self._bootstrap(c, state['attempt_id'], pending)
                if retained is None or retained[1]['state'] != 'PENDING':
                    raise ValueError('funding pending intent absent or spent')
                saved = retained[1]
            amount = saved['limits']['cpu_ns']
            doc['reserved_cpu_ns'] += amount
            doc['remaining_cpu_ns'] = max(0, doc['remaining_cpu_ns'] - amount)
        # Charged cancellation authentication attempts (one-use object rows) are
        # settled controller CPU of this campaign, absent from the snapshot's
        # per-work totals; the claim path applies the identical arithmetic.
        with self.store.transaction() as c:
            charged = self.void_authentication_charge(c, state['attempt_id'])
        if charged:
            doc['settled_cpu_ns'] += charged
            doc['remaining_cpu_ns'] = max(0, doc['remaining_cpu_ns'] - charged)
        return doc, rows

    def _validate_materialized_coverage(self, c, attempt):
        # Only funded writers/offline integrity call this history walk. The
        # bounded scheduler claim never reconstructs canonical events.
        previous = set()
        expected = set()
        for row in c.execute(
            'SELECT body FROM full_campaign_budget_events WHERE attempt_id=? ORDER BY sequence',
            (attempt,),
        ):
            event = parse_canonical_json(bytes(row[0]), label='funding materialization history')
            works = {work['work_id'] for work in event['snapshot']['works']}
            if event['kind'] == 'MATERIALIZE_BOOTSTRAP':
                added = works - previous
                if len(added) != 1 or expected.intersection(added):
                    raise ValueError('funding materialization history differs')
                expected.update(added)
            previous = works
        actual = set()
        for row in c.execute(
            'SELECT work_id FROM full_campaign_bootstraps WHERE attempt_id=?', (attempt,)
        ):
            _, intent = self._bootstrap(c, attempt, row[0])
            if intent['state'] == 'MATERIALIZED':
                actual.add(row[0])
        if actual != expected:
            raise ValueError('funding materialized intent coverage differs')

    def _validate_funding_predecessor(self, c, state):
        if state['profile']['schema'] != PROFILE:
            return
        if c.execute('PRAGMA user_version').fetchone()[0] not in (7, 8):
            raise ValueError('funding profile requires database v7')
        attempt = state['attempt_id']
        previous = self._funding(c, attempt)
        if previous is None:
            raise ValueError('enrolled funding projection absent; no reconstruction')
        prior = self._budget(c, attempt)
        expected, works = self._funding_projection(prior, previous)
        if previous != expected:
            raise ValueError('funding predecessor projection differs')
        actual = {
            row['work_id']: _decode(bytes(row['body']), 2048)
            for row in c.execute(
                'SELECT work_id,substr(body,1,2049) AS body FROM full_campaign_funding_works WHERE attempt_id=?',
                (attempt,),
            )
        }
        if works != actual:
            raise ValueError('funding predecessor work projection differs')
        pending = []
        for row in c.execute(
            'SELECT work_id FROM full_campaign_bootstraps WHERE attempt_id=?', (attempt,)
        ):
            _, intent = self._bootstrap(c, attempt, row[0])
            if intent['state'] == 'PENDING':
                pending.append(row[0])
                if row[0] in works:
                    raise ValueError('funding pending work already materialized')
            elif row[0] not in works:
                raise ValueError('funding materialized work absent')
        if pending != (
            [previous['bootstrap_pending_work_id']] if previous['bootstrap_pending_work_id'] else []
        ):
            raise ValueError('funding pending predecessor differs')
        self._validate_materialized_coverage(c, attempt)

    def _project_funding(self, c, state, *, enroll=False, transfer=None):
        if state['profile']['schema'] != PROFILE:
            return
        previous = self._funding(c, state['attempt_id'])
        if previous is None and not enroll:
            raise ValueError('enrolled funding projection absent; no reconstruction')
        if previous is not None and enroll:
            raise ValueError('funding enrollment already exists')
        if transfer is not None:
            work_id, owner_token = transfer
            self._validate_recovery_token(owner_token)
            saved = self._bootstrap(c, state['attempt_id'], work_id)
            if saved is None:
                raise ValueError('funding transfer intent absent')
            request_raw, intent = saved
            if (
                previous is None
                or previous['bootstrap_pending_work_id'] != work_id
                or intent['state'] != 'PENDING'
                or intent['owner_sha256'] != sha256(owner_token)
            ):
                raise ValueError('funding transfer owner differs')
            work = self._work(state, work_id)
            reservation = {
                'limits': intent['limits'],
                'clock': intent['clock'],
                'input_sha256': intent['input_sha256'],
            }
            if intent['signing_retry_of'] is not None:
                reservation['signing_retry_of'] = intent['signing_retry_of']
            if work['state'] != 'START_INTENT' or self._raw(
                work['reservation_bytes_b64']
            ) != encoded(reservation):
                raise ValueError('funding transfer reservation differs')
            intent['state'] = 'MATERIALIZED'
            _put(c, 'full_campaign_bootstraps', state['attempt_id'], intent, work_id, request_raw)
            previous = dict(previous, bootstrap_pending_work_id=None, terminal_overlay=None)
        doc, rows = self._funding_projection(state, previous)
        _put(c, 'full_campaign_funding', state['attempt_id'], doc)
        for work, row in rows.items():
            _put(c, 'full_campaign_funding_works', state['attempt_id'], row, work)

    def scheduler_status(self, attempt_id):
        with self.store.transaction() as c:
            doc = self._funding(c, attempt_id)
            if doc is None:
                raise ValueError('fresh funding enrollment required')
            return encoded(
                {
                    'schema': 'qualification_campaign_scheduler_status/v1',
                    'attempt_id': attempt_id,
                    'state': doc['state'],
                    'validity': doc['validity'],
                    'pending': doc['bootstrap_pending_work_id'] is not None,
                    'settled_cpu_ns': doc['settled_cpu_ns'],
                    'reserved_cpu_ns': doc['reserved_cpu_ns'],
                    'remaining_cpu_ns': doc['remaining_cpu_ns'],
                    'historical': True,
                    'current_policy_eligible': False,
                }
            )

    def claim_scheduler_bootstrap(self, request_bytes, clock_bytes):
        request = parse_request(request_bytes)
        observed = clock(clock_bytes)
        attempt, work = request['attempt_id'], request['work_id']
        with self.store.transaction() as c:
            if c.execute('PRAGMA user_version').fetchone()[0] not in (7, 8):
                raise ValueError('fresh funding enrollment required')
            existing = self._bootstrap(c, attempt, work)
            if existing is not None:
                if existing[0] != request_bytes:
                    raise ValueError('scheduler request identity conflict')
                return None, self.scheduler_status(attempt)
            doc = self._funding(c, attempt)
            if doc is None:
                raise ValueError('fresh funding enrollment required')
            # A queued operator cancellation bars this new-work grant outright,
            # before or after the receipt (coordinator ruling 2026-09-19).
            self._cancellation_barrier(c, attempt, admitted_only=False)
            if (
                doc['state'] != 'BOUND'
                or doc['validity'] != 'VALID'
                or doc['terminal_overlay'] is not None
            ):
                return None, self.scheduler_status(attempt)
            if (
                doc['bootstrap_pending_work_id'] is not None
                or doc['recovery_pending']
                or doc['dispatch_pending']
            ):
                raise ValueError('campaign funding or recovery/dispatch pending')
            if c.execute(
                'SELECT 1 FROM full_campaign_funding_works WHERE attempt_id=? AND work_id=?',
                (attempt, work),
            ).fetchone():
                raise ValueError('scheduler work identity conflict')
            phase = PHASE_BY_ROLE[request['role']]
            if request['role'] in DISPATCH_ROLES:
                # Genuine dispatch follows a completed admission (the retained
                # diagnostic receipt), on the /v5 release the service fixed at
                # startup; harmless probe dispatch keeps its weaker S2 gate.
                if request['probe'] != 'noop':
                    raise ValueError('dispatch roles require the fixed noop probe')
                if not c.execute(
                    "SELECT 1 FROM full_campaign_objects WHERE attempt_id=? AND role='diagnostic_receipt'",
                    (attempt,),
                ).fetchone():
                    raise ValueError('completed campaign admission required before dispatch')
            parent = request['signing_retry_of']
            if phase in doc['reserved_compute_phases']:
                raise ValueError('compute phase already reserved')
            manifest = {
                'schema': 'qualification_campaign_work_manifest/v1',
                'attempt_id': attempt,
                'work_id': work,
                'role': request['role'],
                'probe': request['probe'],
            }
            input_hash = sha256(encoded(manifest))
            if any(w != parent for w in doc['signing_work_ids']):
                raise ValueError('signing authority serialized')
            if parent is not None:
                row = c.execute(
                    'SELECT substr(body,1,2049) FROM full_campaign_funding_works WHERE attempt_id=? AND work_id=?',
                    (attempt, parent),
                ).fetchone()
                if row is None:
                    raise ValueError('fixed signing parent required')
                p = _decode(bytes(row[0]), 2048)
                if (
                    p['schema'] != 'qualification_campaign_funding_work/v1'
                    or p['attempt_id'] != attempt
                    or p['work_id'] != parent
                ):
                    raise ValueError('funding parent row identity differs')
                if (
                    p['state'] != 'SIGNING_INTENT'
                    or not p['settled']
                    or p['phase'] != phase
                    or p['signing_retry_of'] is not None
                    or p['signing_intent_sha256'] is None
                    or p['open_retry_work_ids']
                    or phase in ('N1', 'N2', 'PART_A')
                ):
                    raise ValueError('fixed settled signing parent required')
                input_hash = p['signing_intent_sha256']
            ceiling = doc['profile']['phases'][phase]
            terminal = None
            if (
                observed['boottime_ns'] is None
                or observed['boot_id'] != doc['start_clock']['boot_id']
                or observed['boottime_ns'] < doc['last_clock']['boottime_ns']
            ):
                terminal = 'BUDGET_UNCERTAIN'
            elif (
                observed['boottime_ns'] >= doc['deadline_boottime_ns']
                or ceiling['cpu_ns'] > doc['remaining_cpu_ns']
            ):
                terminal = 'BUDGET_EXHAUSTED'
            if terminal is not None:
                doc.update(
                    state=terminal,
                    last_clock=_overlay_clock(doc['last_clock'], observed),
                    terminal_overlay={'state': terminal, 'clock': observed},
                )
                _put(c, 'full_campaign_funding', attempt, doc)
                return None, self.scheduler_status(attempt)
            token = secrets.token_bytes(32)
            intent = {
                'schema': 'qualification_campaign_bootstrap/v1',
                'attempt_id': attempt,
                'work_id': work,
                'request_sha256': sha256(request_bytes),
                'owner_sha256': sha256(token),
                'profile_sha256': sha256(encoded(doc['profile'])),
                'phase': phase,
                'limits': ceiling,
                'clock': observed,
                'input_sha256': input_hash,
                'signing_retry_of': parent,
                'claimed_event_head': doc['snapshot_event_head'],
                'claimed_authority_head': doc['snapshot_authority_head'],
                'state': 'PENDING',
            }
            _put(c, 'full_campaign_bootstraps', attempt, intent, work, request_bytes)
            doc.update(
                bootstrap_pending_work_id=work,
                reserved_cpu_ns=doc['reserved_cpu_ns'] + ceiling['cpu_ns'],
                remaining_cpu_ns=doc['remaining_cpu_ns'] - ceiling['cpu_ns'],
            )
            _put(c, 'full_campaign_funding', attempt, doc)
            return token, self.scheduler_status(attempt)

    def materialize_scheduler_bootstrap(self, attempt_id, work_id, owner_token, host_run_id):
        from .campaign_supervisor import work_enrollment, parse_enrollment, parse_supervision_event

        self._validate_recovery_token(owner_token)
        with self.store.transaction() as c:
            saved = self._bootstrap(c, attempt_id, work_id)
            if saved is None or saved[1]['owner_sha256'] != sha256(owner_token):
                raise ValueError('funding owner differs')
            request_raw, intent = saved
            doc = self._funding(c, attempt_id)
            if intent['state'] != 'PENDING' or doc['bootstrap_pending_work_id'] != work_id:
                raise ValueError('funding owner already spent')
            self._funding_integrity(c, attempt_id=attempt_id)
            state = self._budget(c, attempt_id)
            if (
                state['event_head'] != doc['snapshot_event_head']
                or state['authority_head'] != doc['snapshot_authority_head']
            ):
                raise ValueError('funding projection differs')
            request = parse_request(request_raw)
            manifest = encoded(
                {
                    'schema': 'qualification_campaign_work_manifest/v1',
                    'attempt_id': attempt_id,
                    'work_id': work_id,
                    'role': request['role'],
                    'probe': request['probe'],
                }
            )
            scopes = work_enrollment(host_run_id, attempt_id, work_id)
            if state['campaign_scope_id'] not in (None, scopes['campaign_slice']):
                raise ValueError('common campaign memory scope required')
            reservation = {
                'limits': intent['limits'],
                'clock': intent['clock'],
                'input_sha256': intent['input_sha256'],
            }
            if intent['signing_retry_of'] is not None:
                reservation['signing_retry_of'] = intent['signing_retry_of']
            raw = encoded(reservation)
            transition = encoded(
                {
                    'schema': 'qualification_campaign_work_transition/v1',
                    'attempt_id': attempt_id,
                    'work_id': work_id,
                    'state': 'START_INTENT',
                    'clock': intent['clock'],
                    'data': {
                        'campaign_scope_id': scopes['campaign_slice'],
                        'work_scope_id': scopes['payload_slice'],
                    },
                }
            )
            state['works'].append(
                {
                    'work_id': work_id,
                    'phase': intent['phase'],
                    'limits': intent['limits'],
                    'input_sha256': intent['input_sha256'],
                    'reservation_bytes_b64': self._b64(raw),
                    'state': 'START_INTENT',
                    'transitions': [self._b64(transition)],
                    'observation_bytes_b64': None,
                    'charge_cpu_ns': 0,
                }
            )
            state['works'].sort(key=lambda w: w['work_id'])
            state['campaign_scope_id'] = scopes['campaign_slice']
            enrollment = encoded(
                {
                    'schema': 'qualification_campaign_supervision/v1',
                    'host_run_id': host_run_id,
                    'attempt_id': attempt_id,
                    'work_id': work_id,
                    'manifest_bytes_b64': self._b64(manifest),
                    'scopes': scopes,
                }
            )
            parse_enrollment(enrollment)
            control = encoded(
                {
                    'schema': 'qualification_campaign_supervision_event/v2',
                    'attempt_id': attempt_id,
                    'work_id': work_id,
                    'kind': 'CONTROL',
                    'clock': intent['clock'],
                    'data': {'slot': 'START_OWNER'},
                }
            )
            parse_supervision_event(control)
            for role, body in [
                ('supervision_' + work_id, enrollment),
                ('supervision_control_' + sha256(encoded([work_id, 'START_OWNER'])), control),
            ]:
                c.execute(
                    'INSERT INTO full_campaign_objects VALUES(?,?,?,?,?)',
                    (attempt_id, role, sha256(body), len(body), body),
                )
            if doc['terminal_overlay'] is not None:
                self._terminal(state, doc['terminal_overlay']['state'])
                state['last_clock'] = doc['terminal_overlay']['clock']
            elif intent['clock']['boottime_ns'] >= state['last_clock']['boottime_ns']:
                self._observe_clock(state, intent['clock'])
            self._save_budget(
                c,
                state,
                'MATERIALIZE_BOOTSTRAP',
                authority=intent['signing_retry_of'] is None,
                funding_transfer=(work_id, owner_token),
            )
            return raw, enrollment

    def _negative_budget_response(self, connection, state):
        doc = self._funding(connection, state['attempt_id'])
        if doc is not None and (
            doc['bootstrap_pending_work_id'] is not None or doc['terminal_overlay'] is not None
        ):
            return self.scheduler_status(state['attempt_id'])
        return encoded(state)

    def recovery_budget_snapshot(self, attempt_id, work_id, owner_token):
        """Existing funded recovery owner only; never a positive-authority view."""
        self._validate_recovery_token(owner_token)
        with self.store.transaction() as c:
            state = self._budget(c, attempt_id)
            owner = self._recovery_owner(state, work_id, owner_token)
            if owner['completion_bytes_b64'] is not None:
                raise ValueError('completed recovery owner cannot resume')
            return encoded(state)

    def _funding_integrity(self, c, *, attempt_id=None):
        if c.execute('PRAGMA user_version').fetchone()[0] not in (7, 8):
            return
        attempts = (
            [(attempt_id,)]
            if attempt_id is not None
            else list(c.execute('SELECT attempt_id FROM full_campaign_budgets'))
        )
        for row in attempts:
            state = self._budget(c, row[0])
            enrolled = self._funding(c, row[0]) is not None
            if enrolled != (state['profile']['schema'] == PROFILE):
                raise ValueError('funding enrollment integrity differs')
        for row in attempts:
            attempt = row[0]
            doc = self._funding(c, attempt)
            if doc is None:
                continue
            state = self._budget(c, attempt)
            expected, works = self._funding_projection(state, doc)
            if doc != expected:
                raise ValueError('funding projection integrity differs')
            actual = {
                row['work_id']: _decode(bytes(row['body']), 2048)
                for row in c.execute(
                    'SELECT * FROM full_campaign_funding_works WHERE attempt_id=?', (attempt,)
                )
            }
            if works != actual:
                raise ValueError('funding work projection integrity differs')
            pending = []
            for row in c.execute(
                'SELECT work_id FROM full_campaign_bootstraps WHERE attempt_id=?', (attempt,)
            ):
                raw, intent = self._bootstrap(c, attempt, row[0])
                request = parse_request(raw)
                fields(
                    intent,
                    {
                        'schema',
                        'attempt_id',
                        'work_id',
                        'request_sha256',
                        'owner_sha256',
                        'profile_sha256',
                        'phase',
                        'limits',
                        'clock',
                        'input_sha256',
                        'signing_retry_of',
                        'claimed_event_head',
                        'claimed_authority_head',
                        'state',
                    },
                )
                if (
                    intent['schema'] != 'qualification_campaign_bootstrap/v1'
                    or intent['attempt_id'] != attempt
                    or intent['work_id'] != row[0]
                    or intent['request_sha256'] != sha256(raw)
                    or intent['profile_sha256'] != sha256(encoded(state['profile']))
                    or intent['phase'] != PHASE_BY_ROLE[request['role']]
                    or intent['limits'] != state['profile']['phases'][intent['phase']]
                    or intent['signing_retry_of'] != request['signing_retry_of']
                ):
                    raise ValueError('funding intent identity differs')
                for key in (
                    'owner_sha256',
                    'input_sha256',
                    'claimed_event_head',
                    'claimed_authority_head',
                ):
                    digest(intent[key])
                clock(encoded(intent['clock']))
                if request['attempt_id'] != attempt or request['work_id'] != row[0]:
                    raise ValueError('funding request row identity differs')
                event = c.execute(
                    'SELECT body FROM full_campaign_budget_events WHERE attempt_id=? AND sha256=?',
                    (attempt, intent['claimed_event_head']),
                ).fetchone()
                if event is None:
                    raise ValueError('funding claimed history absent')
                event_doc = parse_canonical_json(bytes(event[0]), label='funding predecessor')
                claimed = event_doc['snapshot']
                from .campaign_budget import recovery_pending

                claimed_clock = intent['clock']
                if (
                    claimed['state'] != 'BOUND'
                    or claimed['validity'] != 'VALID'
                    or recovery_pending(claimed)
                    or dispatch_pending(claimed)
                    or intent['limits']['cpu_ns'] > claimed['remaining_cpu_ns']
                    or claimed_clock['boottime_ns'] is None
                    or claimed_clock['boot_id'] != claimed['start_clock']['boot_id']
                    or claimed_clock['boottime_ns'] < claimed['last_clock']['boottime_ns']
                    or claimed_clock['boottime_ns'] >= claimed['deadline_boottime_ns']
                ):
                    raise ValueError('funding claimed history was ineligible')
                if intent['phase'] in ('ADMISSION', 'N1', 'N2', 'PART_A') and any(
                    w['phase'] == intent['phase'] for w in claimed['works']
                ):
                    raise ValueError('funding claimed compute phase already existed')
                if any(
                    w['state'] in ('SIGNING_INTENT', 'SIGNED')
                    and w['work_id'] != intent['signing_retry_of']
                    for w in claimed['works']
                ):
                    raise ValueError('funding claimed signing authority conflict')
                claimed_authority = (
                    intent['claimed_event_head']
                    if event_doc['authority']
                    else claimed['authority_head']
                )
                if claimed_authority != intent['claimed_authority_head']:
                    raise ValueError('funding claimed authority differs')
                if any(w['work_id'] == row[0] for w in claimed['works']):
                    raise ValueError('funding claimed work already existed')
                if intent['signing_retry_of'] is None:
                    manifest = {
                        'schema': 'qualification_campaign_work_manifest/v1',
                        'attempt_id': attempt,
                        'work_id': row[0],
                        'role': request['role'],
                        'probe': request['probe'],
                    }
                    expected_input = sha256(encoded(manifest))
                else:
                    parent = self._work(claimed, intent['signing_retry_of'])
                    fixed = self._signing_intent(parent)
                    if (
                        fixed is None
                        or parent['state'] != 'SIGNING_INTENT'
                        or parent['observation_bytes_b64'] is None
                        or parent['phase'] != intent['phase']
                        or self._retry_parent(parent) is not None
                        or self._open_retries(claimed, parent['work_id'])
                    ):
                        raise ValueError('funding signing provenance absent')
                    expected_input = sha256(self._raw(fixed['data']['payload_bytes_b64']))
                if expected_input != intent['input_sha256']:
                    raise ValueError('funding input provenance differs')
                if intent['state'] == 'PENDING':
                    pending.append(row[0])
                    if row[0] in works:
                        raise ValueError('pending funding already materialized')
                elif intent['state'] == 'MATERIALIZED':
                    work = self._work(state, row[0])
                    specification = {
                        'limits': intent['limits'],
                        'clock': intent['clock'],
                        'input_sha256': intent['input_sha256'],
                    }
                    if intent['signing_retry_of'] is not None:
                        specification['signing_retry_of'] = intent['signing_retry_of']
                    if self._raw(work['reservation_bytes_b64']) != encoded(specification):
                        raise ValueError('funding transfer differs')
                else:
                    raise ValueError('funding intent state differs')
            if pending != (
                [doc['bootstrap_pending_work_id']] if doc['bootstrap_pending_work_id'] else []
            ):
                raise ValueError('funding pending projection differs')
            self._validate_materialized_coverage(c, attempt)
