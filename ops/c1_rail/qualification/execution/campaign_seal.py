"""S7: the separate seal authority -- PASS-only eligibility, atomic publication.

The seal family (F2): ``qualification_campaign_seal_intent/v1`` (T1: the fixed
payload digests, intent id, seal key id and signing instant persisted before
any signature), ``qualification_campaign_seal/v1`` (qseal's seal-key signature
over exactly the intent's fixed payload -- produced only inside the qseal
process) and ``qualification_campaign_seal_receipt/v1`` (the one immutable
publication record). The bytes live in the v9 ``full_campaign_seal_intents``
table mounted by :mod:`campaign_result`.

Separation (F4): ``seal_service.sign_committed_pass`` runs only in the qseal
process under the seal principal and its own credential root; it recomputes
PASS from the committed result (a caller-supplied verdict is never accepted)
and has no publication path. This module's store companion publishes; the
service seam (:func:`request_seal`) owns the locked signing phase. No
module-level mutable state anywhere (the frozen-adjudicator walk).
"""
import json

from ..contract import canonical_json_bytes as encoded, parse_canonical_json
from .campaign_budget import integer, limits as parse_limits, validate_work_id
from .campaign_result import (REFUSED_BUDGET_STATES, SEAL_ELIGIBLE_STATE, SEAL_PHASE,
                              SEALED_PASS, ResultStore, parse_campaign_result,
                              supervise_unit_to_exit)
from .protocol import digest, fields, identity, sha256

SEAL_INTENT_SCHEMA = 'qualification_campaign_seal_intent/v1'
SEAL_SCHEMA_LITERAL = 'qualification_campaign_seal/v1'
SEAL_RECEIPT_SCHEMA = 'qualification_campaign_seal_receipt/v1'
SEAL_OPERATION_SCHEMA = 'qualification_campaign_seal_request/v1'

SEAL_OPERATIONS = ('REQUEST_SEAL', 'INSPECT_SEAL')
_SEAL_OPERATION_FIELDS = {'REQUEST_SEAL': set(), 'INSPECT_SEAL': set()}


def parse_seal_operation(raw):
    """The closed shape of the two S7 operations (registered by the seam)."""
    wire = parse_canonical_json(raw, label='campaign request')
    operation = wire.get('operation') if type(wire) is dict else None
    if operation not in _SEAL_OPERATION_FIELDS:
        raise ValueError('UNKNOWN_OPERATION')
    doc = fields(wire, {'schema', 'operation', 'attempt_id'} | _SEAL_OPERATION_FIELDS[operation])
    if doc['schema'] not in ('qualification_campaign_request/v1', 'qualification_campaign_request/v2'):
        raise ValueError('unsupported campaign request schema')
    identity(doc['attempt_id'])
    return doc


def parse_seal_intent(raw, *, attempt_id):
    doc = fields(parse_canonical_json(raw, label='seal intent'), {
        'schema', 'attempt_id', 'intent_id', 'result_sha256', 'authentication_sha256',
        'result_receipt_sha256', 'release_sha256', 'domain_sha256', 'key_id',
        'signing_at_utc'})
    from .campaign_budget import utc
    if doc['schema'] != SEAL_INTENT_SCHEMA or doc['attempt_id'] != attempt_id:
        raise ValueError('seal intent binding differs')
    identity(doc['intent_id'])
    identity(doc['key_id'])
    utc(doc['signing_at_utc'])
    for name in ('result_sha256', 'authentication_sha256', 'result_receipt_sha256',
                 'release_sha256', 'domain_sha256'):
        digest(doc[name])
    return doc


def parse_seal_signature(raw, *, attempt_id):
    """qseal's seal document: the signature over exactly the intent's fixed
    payload with the seal key named by the intent."""
    doc = fields(parse_canonical_json(raw, label='seal signature'), {
        'schema', 'attempt_id', 'intent_id', 'result_sha256', 'authentication_sha256',
        'result_receipt_sha256', 'release_sha256', 'domain_sha256', 'signed_at_utc',
        'signature'})
    from .campaign_budget import utc
    if doc['schema'] != SEAL_SCHEMA_LITERAL or doc['attempt_id'] != attempt_id:
        raise ValueError('seal signature binding differs')
    identity(doc['intent_id'])
    utc(doc['signed_at_utc'])
    for name in ('result_sha256', 'authentication_sha256', 'result_receipt_sha256',
                 'release_sha256', 'domain_sha256'):
        digest(doc[name])
    signature = fields(doc['signature'], {'algorithm', 'key_id', 'value_b64'})
    if signature['algorithm'] != 'Ed25519':
        raise ValueError('canonical signing algorithm required')
    return doc


def seal_core(attempt_id, *, intent_id, result_sha256, authentication_sha256,
              result_receipt_sha256, release_sha256, domain_sha256, signed_at_utc):
    """The fixed signed payload: exactly the intent's fields, no fresh time."""
    return encoded(dict(schema=SEAL_SCHEMA_LITERAL, attempt_id=attempt_id,
        intent_id=intent_id, result_sha256=result_sha256,
        authentication_sha256=authentication_sha256,
        result_receipt_sha256=result_receipt_sha256, release_sha256=release_sha256,
        domain_sha256=domain_sha256, signed_at_utc=signed_at_utc))


def parse_seal_receipt(raw, *, attempt_id):
    doc = fields(parse_canonical_json(raw, label='seal receipt'), {
        'schema', 'attempt_id', 'work_id', 'campaign_id', 'intent_id', 'seal_sha256',
        'result_sha256', 'result_receipt_sha256', 'campaign_state', 'campaign_revision',
        'authority_head', 'signing_at_utc', 'committed_at_utc', 'intent_sha256'})
    from .campaign_budget import utc
    if (doc['schema'] != SEAL_RECEIPT_SCHEMA or doc['attempt_id'] != attempt_id
            or doc['campaign_state'] != SEALED_PASS):
        raise ValueError('seal receipt binding differs')
    identity(doc['work_id'])
    identity(doc['campaign_id'])
    identity(doc['intent_id'])
    for name in ('seal_sha256', 'result_sha256', 'result_receipt_sha256', 'authority_head',
                 'intent_sha256'):
        digest(doc[name])
    integer(doc['campaign_revision'])
    utc(doc['signing_at_utc'])
    utc(doc['committed_at_utc'])
    return doc


class SealStore(ResultStore):
    """S7 custody over the v9 seal tables: the SEAL-phase work, T1 and T2.

    Inherits the v9 reads/writes from :class:`campaign_result.ResultStore`
    (same DB, same frozen-bytes constraints, no funding projection).
    """

    # -- the SEAL-phase work ---------------------------------------------------
    def _seal_predecessor(self, connection, attempt_id):
        """Only a currently-valid committed PASS outcome whose budget
        authority still stands may reserve SEAL; a settlement that ended
        authority (the a8a983e rule) never grants a new seal."""
        if connection.execute('PRAGMA user_version').fetchone()[0] < 9:
            return 'result custody absent'
        if self.campaigns.row(attempt_id)['validity'] != 'VALID':
            return 'VOID campaign'
        if self.campaigns._cancellation_pending(connection, attempt_id):
            return 'campaign cancellation pending'
        family = self._result_family(connection, attempt_id)
        if family['state'] != 'COMMITTED':
            return 'no committed campaign result'
        if family['outcome'] != 'PASS':
            return 'committed FAIL outcome is never sealed'
        budget_state = self._state(connection, attempt_id)['state']
        if budget_state in REFUSED_BUDGET_STATES:
            return budget_state
        return None

    def reserve_seal_work(self, attempt_id, work_id, limits_bytes, *, expected_revision,
                          start_transition_bytes=None):
        """Reserve the SEAL phase from a committed PASS (the reserve_result_work
        mirror: installed phase, one SEAL work, cancellation barrier, remaining
        allowance, explicit deadline)."""
        from .campaign_budget import clock
        integer(expected_revision)
        validate_work_id(work_id)
        specification = parse_canonical_json(limits_bytes, label='work reservation')
        fields(specification, {'limits', 'clock', 'input_sha256'})
        parse_limits(specification['limits'])
        clock(encoded(specification['clock']))
        digest(specification['input_sha256'])
        with self.store.transaction() as connection:
            self._ensure_result_layout(connection)
            state = self._state(connection, attempt_id)
            existing = next((w for w in state['works'] if w['work_id'] == work_id), None)
            if existing is not None:
                from .protocol import decode_base64
                if (existing['phase'] != SEAL_PHASE
                        or decode_base64(existing['reservation_bytes_b64']) != limits_bytes):
                    raise ValueError('work reservation identity conflict')
                return encoded(state)
            self.campaigns._cancellation_barrier(connection, attempt_id, admitted_only=False)
            if expected_revision != state['authority_revision']:
                raise ValueError('campaign authority revision conflict')
            reason = self._seal_predecessor(connection, attempt_id)
            if reason is not None:
                raise ValueError('seal predecessor refuses: ' + reason)
            if SEAL_PHASE not in state['profile']['phases']:
                raise ValueError('installed SEAL phase required')
            if specification['limits'] != state['profile']['phases'][SEAL_PHASE]:
                raise ValueError('reservation must use installed phase configuration')
            if any(w['phase'] == SEAL_PHASE for w in state['works']):
                raise ValueError('seal phase already reserved')
            if any(w['state'] == 'SIGNING_INTENT' for w in state['works']):
                raise ValueError('authority-changing work is serialized during signing')
            self.campaigns._observe_clock(state, specification['clock'])
            boottime = specification['clock']['boottime_ns']
            if (boottime is None or boottime >= state['deadline_boottime_ns']
                    or specification['limits']['cpu_ns'] > self.campaigns._remaining_after_charges(
                        connection, state)):
                self._advance(connection, state, 'RESERVE_SEAL_WORK', authority=True)
                raise ValueError('seal reservation refused by campaign budget')
            transitions = []
            state_after_start = 'RESERVED'
            if start_transition_bytes is not None:
                from .campaign_budget import transition as parse_transition
                start = parse_transition(start_transition_bytes, attempt_id, work_id)
                if start['state'] != 'START_INTENT' or state['campaign_scope_id'] not in (
                        None, start['data']['campaign_scope_id']):
                    raise ValueError('common campaign memory scope required')
                state['campaign_scope_id'] = start['data']['campaign_scope_id']
                transitions.append(self.campaigns._b64(start_transition_bytes))
                state_after_start = 'START_INTENT'
            state['works'].append(dict(work_id=work_id, phase=SEAL_PHASE,
                limits=specification['limits'], input_sha256=specification['input_sha256'],
                reservation_bytes_b64=self.campaigns._b64(limits_bytes),
                state=state_after_start, transitions=transitions,
                observation_bytes_b64=None, charge_cpu_ns=0))
            state['works'].sort(key=lambda w: w['work_id'])
            return encoded(self._advance(connection, state, 'RESERVE_SEAL_WORK', authority=True))

    # -- T1 -------------------------------------------------------------------
    def prepare_seal_intent(self, attempt_id, intent_bytes, *, expected_revision):
        """T1 (F5): the fixed intent persisted before any signature. An exact
        retry is idempotent; a different intent under a persisted one refuses.
        Requires the committed PASS, current validity and the SEAL reservation.
        The committing qseal work enters the signing window here (the
        persist_result_intent shape: CAPTURED -> SIGNING_INTENT), so its own
        T2 can record SIGNED and, after settlement, COMPLETED (a8a983e)."""
        integer(expected_revision)
        intent = parse_seal_intent(intent_bytes, attempt_id=attempt_id)
        with self.store.transaction() as connection:
            self._ensure_result_layout(connection)
            prior = connection.execute('SELECT intent_bytes FROM full_campaign_seal_intents '
                                       'WHERE attempt_id=?', (attempt_id,)).fetchone()
            if prior is not None:
                if bytes(prior[0]) != intent_bytes:
                    raise ValueError('exact seal intent retry required')
                return encoded(self._state(connection, attempt_id))
            state = self._state(connection, attempt_id)
            reason = self._seal_predecessor(connection, attempt_id)
            if reason is not None:
                raise ValueError('seal predecessor refuses: ' + reason)
            if expected_revision != state['authority_revision']:
                raise ValueError('campaign authority revision conflict')
            work = next((w for w in state['works'] if w['phase'] == SEAL_PHASE), None)
            if work is None:
                raise ValueError('SEAL reservation required')
            # No fresh clock at T1 (the frozen signature carries no clock
            # source); the fixed intent is the work's capture fact.
            capture = encoded(dict(schema='qualification_campaign_seal_capture/v1',
                attempt_id=attempt_id, work_id=work['work_id'],
                intent_sha256=sha256(intent_bytes)))
            captured = encoded(dict(schema='qualification_campaign_work_transition/v1',
                attempt_id=attempt_id, work_id=work['work_id'], state='CAPTURED',
                clock=state['last_clock'], data=dict(
                    capture_bytes_b64=self.campaigns._b64(capture))))
            state = parse_canonical_json(self.record_result_transition(
                attempt_id, work['work_id'], captured,
                expected_revision=state['authority_revision']),
                label='seal captured state')
            signing = encoded(dict(schema='qualification_campaign_work_transition/v1',
                attempt_id=attempt_id, work_id=work['work_id'], state='SIGNING_INTENT',
                clock=state['last_clock'], data=dict(
                    intent_id=intent['intent_id'],
                    payload_bytes_b64=self.campaigns._b64(intent_bytes),
                    key_id=intent['key_id'], signing_at_utc=intent['signing_at_utc'])))
            state = parse_canonical_json(self.record_result_transition(
                attempt_id, work['work_id'], signing,
                expected_revision=state['authority_revision']),
                label='seal signing state')
            connection.execute('INSERT INTO full_campaign_seal_intents VALUES(?,?,NULL,NULL)',
                               (attempt_id, intent_bytes))
            return encoded(self._advance(connection, state, 'SEAL_INTENT', authority=False))

    # -- T2 -------------------------------------------------------------------
    def commit_campaign_seal(self, attempt_id, intent_bytes, signature_bytes, *, now):
        """T2: publish the seal bytes and one immutable receipt atomically,
        advancing to SEALED_PASS. An exact retry returns the byte-identical
        receipt; a different signature under the persisted intent refuses;
        VOID before the commit refuses; VOID after flips the wrapper's
        validity only."""
        from .store import instant
        with self.store.transaction() as connection:
            self._ensure_result_layout(connection)
            row = connection.execute('SELECT intent_bytes,signature_bytes,receipt_bytes '
                                     'FROM full_campaign_seal_intents WHERE attempt_id=?',
                                     (attempt_id,)).fetchone()
            if row is None or bytes(row[0]) != intent_bytes:
                raise ValueError('exact seal intent retry required')
            if row[2] is not None:
                if bytes(row[1] or b'') != signature_bytes:
                    raise ValueError('exact seal signature retry required')
                receipt = parse_seal_receipt(bytes(row[2]), attempt_id=attempt_id)
                eligibility = self._seal_eligibility_view(connection, attempt_id)
                return encoded(dict(receipt=receipt,
                                    validity=self.campaigns.row(attempt_id)['validity'],
                                    historical=True, eligibility=eligibility))
            state = self._state(connection, attempt_id)
            if self.campaigns.row(attempt_id)['validity'] != 'VALID' or state['validity'] != 'VALID':
                raise ValueError('VOID campaign')
            if self.campaigns._cancellation_pending(connection, attempt_id):
                raise ValueError('campaign cancellation pending')
            reason = self._seal_predecessor(connection, attempt_id)
            if reason is not None:
                raise ValueError('seal predecessor refuses: ' + reason)
            work = next((w for w in state['works'] if w['phase'] == SEAL_PHASE), None)
            if work is None:
                raise ValueError('SEAL reservation required')
            intent = parse_seal_intent(bytes(row[0]), attempt_id=attempt_id)
            seal = parse_seal_signature(signature_bytes, attempt_id=attempt_id)
            if (seal['intent_id'] != intent['intent_id']
                    or seal['result_sha256'] != intent['result_sha256']
                    or seal['authentication_sha256'] != intent['authentication_sha256']
                    or seal['result_receipt_sha256'] != intent['result_receipt_sha256']
                    or seal['release_sha256'] != intent['release_sha256']
                    or seal['domain_sha256'] != intent['domain_sha256']
                    or seal['signature']['key_id'] != intent['key_id']
                    or seal['signed_at_utc'] != intent['signing_at_utc']):
                raise ValueError('seal signature differs from the persisted intent')
            # The sealed result is exactly the committed aggregate.
            result_bytes, authentication_bytes, result_receipt_bytes = self.committed_result(attempt_id)
            if (intent['result_sha256'] != sha256(result_bytes)
                    or intent['authentication_sha256'] != sha256(authentication_bytes)
                    or intent['result_receipt_sha256'] != sha256(result_receipt_bytes)):
                raise ValueError('seal intent binding differs from the committed result')
            result = parse_campaign_result(result_bytes, attempt_id=attempt_id)
            committed_receipt = parse_canonical_json(result_receipt_bytes, label='result receipt')
            if (result['outcome'] != 'PASS'
                    or committed_receipt['campaign_state'] != SEAL_ELIGIBLE_STATE):
                raise ValueError('committed PASS result required')
            if (state['last_clock']['boottime_ns'] is None
                    or state['last_clock']['boottime_ns'] >= state['deadline_boottime_ns']):
                raise ValueError('seal commit refused by campaign budget: BUDGET_EXHAUSTED')
            receipt = encoded(dict(schema=SEAL_RECEIPT_SCHEMA, attempt_id=attempt_id,
                work_id=work['work_id'],
                campaign_id=self.campaigns.row(attempt_id)['campaign_id'],
                intent_id=intent['intent_id'], seal_sha256=sha256(signature_bytes),
                result_sha256=intent['result_sha256'],
                result_receipt_sha256=intent['result_receipt_sha256'],
                campaign_state=SEALED_PASS,
                campaign_revision=state['authority_revision'],
                authority_head=state['event_head'],
                signing_at_utc=intent['signing_at_utc'], committed_at_utc=instant(now),
                intent_sha256=sha256(bytes(row[0]))))
            parse_seal_receipt(receipt, attempt_id=attempt_id)
            # The committing qseal work's own T2 fact (commit_campaign_result's
            # SIGNED shape): the seal receipt is the saved candidate, and the
            # work settles -- and completes -- in the state this commit
            # produces (a8a983e).
            signed = encoded(dict(schema='qualification_campaign_work_transition/v1',
                attempt_id=attempt_id, work_id=work['work_id'], state='SIGNED',
                clock=state['last_clock'], data=dict(
                    candidate_bytes_b64=self.campaigns._b64(receipt))))
            self.record_result_transition(attempt_id, work['work_id'], signed,
                                          expected_revision=state['authority_revision'])
            connection.execute('UPDATE full_campaign_seal_intents SET signature_bytes=?,'
                               'receipt_bytes=? WHERE attempt_id=?',
                               (signature_bytes, receipt, attempt_id))
            state = self._state(connection, attempt_id)
            self._advance(connection, state, 'SEAL_COMMITTED', authority=True,
                          state_name=SEALED_PASS)
            return encoded(dict(receipt=parse_canonical_json(receipt, label='receipt'),
                                validity=self.campaigns.row(attempt_id)['validity'],
                                historical=False))

    # -- receipts ---------------------------------------------------------------
    def _seal_family(self, connection, attempt_id):
        row = connection.execute('SELECT signature_bytes,receipt_bytes FROM '
                                 'full_campaign_seal_intents WHERE attempt_id=?',
                                 (attempt_id,)).fetchone()
        if row is None:
            return 'ABSENT'
        return 'SEALED' if row[1] is not None else 'INTENT'

    def _seal_eligibility_view(self, connection, attempt_id):
        eligible = self.seal_eligibility(attempt_id)
        return dict(eligible=eligible['eligible'], reason=eligible['reason'])

    def seal_receipt(self, attempt_id):
        """(receipt_bytes, historical, current_validity, eligibility) -- the
        historical record with the truthful present view; never infers present
        authorization from the signature's existence."""
        with self.store.transaction() as connection:
            row = connection.execute('SELECT receipt_bytes FROM full_campaign_seal_intents '
                                     'WHERE attempt_id=?', (attempt_id,)).fetchone()
            if row is None or row[0] is None:
                raise ValueError('no committed campaign seal')
            receipt_bytes = bytes(row[0])
            parse_seal_receipt(receipt_bytes, attempt_id=attempt_id)
            eligibility = self._seal_eligibility_view(connection, attempt_id)
            return receipt_bytes, True, self.campaigns.row(attempt_id)['validity'], eligibility

    def seal_integrity(self, connection):
        """The v9 seal family walk (offline integrity)."""
        for row in connection.execute('SELECT attempt_id,intent_bytes,signature_bytes,'
                                      'receipt_bytes FROM full_campaign_seal_intents'):
            attempt = row[0]
            intent = parse_seal_intent(bytes(row[1]), attempt_id=attempt)
            if row[3] is not None:
                if row[2] is None:
                    raise ValueError('sealed signature absent')
                seal = parse_seal_signature(bytes(row[2]), attempt_id=attempt)
                receipt = parse_seal_receipt(bytes(row[3]), attempt_id=attempt)
                if (receipt['intent_sha256'] != sha256(bytes(row[1]))
                        or receipt['seal_sha256'] != sha256(bytes(row[2]))
                        or seal['intent_id'] != intent['intent_id']):
                    raise ValueError('seal receipt integrity differs')
            elif row[2] is not None:
                raise ValueError('seal signature without a receipt')


# ---------------------------------------------------------------------------
# The service seam functions (§1).


def request_seal(service, attempt_id):
    """The locked signing phase: eligibility -> durable T1 intent -> qseal over
    the private bounded IPC -> recheck -> atomic T2 publication. A signing
    failure rolls back publication, never the durable intent."""
    from .campaign_store import CampaignStore
    from .store import instant
    from . import seal_service
    from datetime import datetime, timezone
    campaigns = getattr(service, 'campaigns', None) or CampaignStore(service.store)
    seals = SealStore(campaigns)
    keys = service.keys()
    eligibility = seals.seal_eligibility(attempt_id)
    if not eligibility['eligible']:
        raise ValueError(eligibility['reason'])
    context = _enrollment_context(service, campaigns, attempt_id, keys)
    result_bytes, authentication_bytes, receipt_bytes = seals.committed_result(attempt_id)
    revision = json.loads(seals.result_state_bytes(attempt_id))['authority_revision']
    live = [key_id for key_id in sorted(context.domain.seal_key_ids)
            if key_id in keys and keys[key_id].revoked_at is None]
    if not live:
        raise ValueError('no live seal key is enrolled')
    intent_bytes = encoded(dict(schema=SEAL_INTENT_SCHEMA, attempt_id=attempt_id,
        intent_id=attempt_id + '-seal', result_sha256=sha256(result_bytes),
        authentication_sha256=sha256(authentication_bytes),
        result_receipt_sha256=sha256(receipt_bytes),
        release_sha256=sha256(service.release), domain_sha256=context.domain.sha256,
        key_id=live[0], signing_at_utc=instant(datetime.now(timezone.utc))))
    with service.dispatch_lock:
        seals.prepare_seal_intent(attempt_id, intent_bytes, expected_revision=revision)
        signer = getattr(service, 'qseal_sign', None)
        if signer is not None:
            signature_bytes = signer(intent_bytes, result_bytes, authentication_bytes,
                                     receipt_bytes)
        else:
            signature_bytes = seal_service.exchange(
                service, intent_bytes, result_bytes, authentication_bytes, receipt_bytes)
        # Recheck immediately before publication: enrollment digests,
        # validity, family, budget.
        verify_seal_intent(intent_bytes, context, service.release)
        eligibility = seals.seal_eligibility(attempt_id)
        if not eligibility['eligible']:
            raise ValueError(eligibility['reason'])
        return seals.commit_campaign_seal(attempt_id, intent_bytes, signature_bytes,
                                          now=datetime.now(timezone.utc))


def verify_seal_intent(intent_bytes, context, release):
    """The service-side enrollment check the signer cannot make: the intent's
    release and domain digests must be the live enrollment's (seam #19 note:
    the domain reference comes from the service's enrollment context)."""
    intent = parse_seal_intent(intent_bytes, attempt_id=parse_canonical_json(
        intent_bytes, label='seal intent')['attempt_id'])
    if (intent['release_sha256'] != sha256(release)
            or intent['domain_sha256'] != context.domain.sha256):
        raise ValueError('seal intent domain differs')
    return intent


def _enrollment_context(service, campaigns, attempt_id, keys):
    """The service's enrollment context. CampaignStore.context refuses metered
    campaigns at this revision (seam #19, S3's); the service/double supplies
    ``seal_enrollment_context`` until that seam lands."""
    provider = getattr(service, 'seal_enrollment_context', None)
    if provider is not None:
        return provider(attempt_id)
    from datetime import datetime, timezone
    return campaigns.context(attempt_id, service.release, keys,
                             now=datetime.now(timezone.utc))


def inspect_seal(campaigns, attempt_id):
    """The protected read-only view: the historical receipt plus the current
    validity and eligibility. Consumers must not infer present authorization
    from the offline signature's existence -- ``eligibility`` is the current
    fact."""
    seals = SealStore(campaigns)
    with seals.store.transaction() as connection:
        family = seals._seal_family(connection, attempt_id)
        validity = seals.campaigns.row(attempt_id)['validity']
        eligibility = seals._seal_eligibility_view(connection, attempt_id)
        if family != 'SEALED':
            return encoded(dict(schema='qualification_campaign_seal_inspection/v1',
                attempt_id=attempt_id, receipt=None, historical=False,
                current_validity=validity, seal_state=family, eligibility=eligibility))
        receipt_bytes, _, _, _ = seals.seal_receipt(attempt_id)
        return encoded(dict(schema='qualification_campaign_seal_inspection/v1',
            attempt_id=attempt_id, receipt=parse_canonical_json(receipt_bytes,
                                                                label='receipt'),
            historical=True, current_validity=validity, seal_state=family,
            eligibility=eligibility))


def run_seal_unit(context, campaigns, runtime, state, work, enrollment, manifest):
    """The guardian body for the qseal unit (F4): the unit hosts the private
    IPC listener; the guardian supervises its identities and settles. Same
    signature as ``_run_n1_g5``; Linux evidence at acceptance."""
    from . import campaign_supervisor as supervisor
    from .runtime import installed_code_root
    import sys
    seals = SealStore(campaigns)
    deadline = min(state['deadline_boottime_ns'],
                   parse_canonical_json(seals.campaigns._raw(work['reservation_bytes_b64']),
                                        label='reservation')['clock']['boottime_ns']
                   + work['limits']['wall_ns'])
    now_clock = supervisor.clock(supervisor.observe_campaign_clock())
    remaining_wall_ns = deadline - now_clock['boottime_ns']
    spec = supervisor.g5_unit_spec(enrollment['scopes'], attempt_id=state['attempt_id'],
        work_id=work['work_id'], code_root=str(installed_code_root()),
        interpreter=sys.executable, g5_uid=context.config['seal_probe_uid'],
        orchestration_cpu_ns=state['profile']['orchestration_cpu_ns'][work['phase']],
        remaining_wall_ns=remaining_wall_ns, cpu_ns=work['limits']['cpu_ns'])
    unit = enrollment['scopes']['payload_slice'][:-6] + '-seal.service'
    with campaigns.launch_gate(state['attempt_id'], work['work_id'],
                               supervisor.observe_campaign_clock, role='payload') as permit:
        supervisor._guardian_bus_call(campaigns, unit, spec['g5'])
    campaigns.acknowledge_dispatch(state['attempt_id'], work['work_id'], 'payload',
                                   permit['token'], supervisor.observe_campaign_clock)
    group = supervisor._scope_path(runtime.parent, enrollment['scopes']['payload_slice']) / unit
    supervise_unit_to_exit(supervisor, seals, state, work, group, phase=SEAL_PHASE,
                           uid=context.config['seal_probe_uid'], deadline=deadline,
                           role='seal')
    state = parse_canonical_json(seals.result_state_bytes(state['attempt_id']),
                                 label='seal final state')
    work = campaigns._work(state, work['work_id'])
    if work['state'] == 'RUNNING':
        in_doubt = encoded(dict(schema='qualification_campaign_work_transition/v1',
            attempt_id=state['attempt_id'], work_id=work['work_id'], state='IN_DOUBT',
            clock=state['last_clock'], data={}))
        seals.record_result_transition(state['attempt_id'], work['work_id'], in_doubt,
                                       expected_revision=state['authority_revision'])
        state = parse_canonical_json(seals.result_state_bytes(state['attempt_id']),
                                     label='seal in-doubt')
        work = campaigns._work(state, work['work_id'])
    observed = runtime.observation(state, work, enrollment)
    state = parse_canonical_json(seals.settle_result_work(
        state['attempt_id'], work['work_id'], observed), label='seal settlement')
    work = campaigns._work(state, work['work_id'])
    with campaigns.store.transaction() as connection:
        family = seals._seal_family(connection, state['attempt_id'])
    # The committing work completes in the state its own commit produced; a
    # settlement that ended authority (overrun/uncertain) skips the
    # completion -- the receipt is history and the store would refuse it
    # (S3's _run_n1_g5 tail guard, a8a983e shape).
    if (work['state'] == 'SIGNED' and state['validity'] == 'VALID' and family == 'SEALED'
            and state['state'] in seals._completion_states(work)):
        completed = encoded(dict(schema='qualification_campaign_work_transition/v1',
            attempt_id=state['attempt_id'], work_id=work['work_id'], state='COMPLETED',
            clock=state['last_clock'], data={}))
        seals.record_result_transition(state['attempt_id'], work['work_id'], completed,
                                       expected_revision=state['authority_revision'])
