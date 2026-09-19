"""Acyclic logical assessment snapshots. This module never opens a database."""
import re
from .contract import canonical_json_bytes, parse_canonical_json, _fields, _sha256, _positive_int

from .policy import ATTESTED_CHECKPOINTS as CHECKPOINTS
EXECUTION_STATES = ('PENDING', 'DISPATCHED', 'START_INTENT', 'RUNNING', 'CAPTURED', 'ATTESTED', 'ABORTED', 'IN_DOUBT')


def _identity(value):
    if type(value) is not str or re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}', value) is None:
        raise ValueError('SNAPSHOT_IDENTITY_MISMATCH')


def parse_assessment_snapshot(raw: bytes) -> dict:
    doc = _fields(parse_canonical_json(raw, label='journal snapshot'), {
        'schema', 'attempt_id', 'contract_sha256', 'trust_domain_sha256', 'policy_sha256',
        'validity', 'campaign_revision', 'event_head', 'executions'}, label='journal snapshot')
    if doc['schema'] != 'qualification_journal_snapshot/v1' or doc['validity'] not in ('VALID', 'VOID'):
        raise ValueError('SNAPSHOT_STATE_MISMATCH')
    _identity(doc['attempt_id'])
    for field in ('contract_sha256', 'trust_domain_sha256', 'policy_sha256', 'event_head'):
        _sha256(doc[field], label=field)
    _positive_int(doc['campaign_revision'], label='campaign revision', allow_zero=True)
    rows = doc['executions']
    if type(rows) is not list:
        raise ValueError('SNAPSHOT_EXECUTIONS_MISMATCH')
    checkpoints, identities = [], set()
    for row in rows:
        _fields(row, {'checkpoint', 'execution_id', 'execution_revision', 'state', 'plan_sha256', 'attestation_sha256'}, label='snapshot execution')
        if row['checkpoint'] not in CHECKPOINTS or row['state'] not in EXECUTION_STATES:
            raise ValueError('SNAPSHOT_EXECUTION_STATE_MISMATCH')
        _identity(row['execution_id'])
        _positive_int(row['execution_revision'], label='execution revision', allow_zero=True)
        if row['execution_revision'] > doc['campaign_revision']:
            raise ValueError('SNAPSHOT_REVISION_MISMATCH')
        _sha256(row['plan_sha256'], label='plan')
        if row['state'] == 'ATTESTED':
            _sha256(row['attestation_sha256'], label='attestation')
        elif row['attestation_sha256'] is not None:
            raise ValueError('SNAPSHOT_PREMATURE_ATTESTATION')
        if row['execution_id'] in identities:
            raise ValueError('SNAPSHOT_DUPLICATE_EXECUTION')
        identities.add(row['execution_id'])
        checkpoints.append(CHECKPOINTS.index(row['checkpoint']))
    if checkpoints != sorted(set(checkpoints)):
        raise ValueError('SNAPSHOT_CHECKPOINT_ORDER_MISMATCH')
    return doc


def encode_assessment_snapshot(*, attempt_id, contract_sha256, trust_domain_sha256,
                               policy_sha256, validity, campaign_revision, event_head, executions) -> bytes:
    rows = list(executions)
    if any(type(row) is not dict or row.get('checkpoint') not in CHECKPOINTS for row in rows):
        raise ValueError('SNAPSHOT_EXECUTIONS_MISMATCH')
    raw = canonical_json_bytes(dict(schema='qualification_journal_snapshot/v1', attempt_id=attempt_id,
        contract_sha256=contract_sha256, trust_domain_sha256=trust_domain_sha256, policy_sha256=policy_sha256,
        validity=validity, campaign_revision=campaign_revision, event_head=event_head,
        executions=sorted(rows, key=lambda row: CHECKPOINTS.index(row['checkpoint']))))
    parse_assessment_snapshot(raw)
    return raw


CAMPAIGN_BUDGET_STATES = ('PROVISIONAL', 'BOUND', 'BUDGET_EXHAUSTED', 'BUDGET_UNCERTAIN', 'IN_DOUBT', 'ABORTED')
CAMPAIGN_WORK_STATES = ('RESERVED', 'START_INTENT', 'RUNNING', 'CAPTURED', 'SIGNING_INTENT', 'SIGNED', 'COMPLETED', 'IN_DOUBT', 'ABORTED')


def parse_campaign_budget_snapshot(raw: bytes) -> dict:
    """Private accounting snapshot, deliberately separate from N1 snapshots.

    Authority revision/head exclude non-terminal accounting events. A signer
    binds authority revision plus its reserved work/intent; publication checks
    those values and the CURRENT ledger together inside ExecutionStore's lock.
    Full snapshot byte equality is not the publication freshness predicate.
    """
    doc = _fields(parse_canonical_json(raw, label='campaign budget snapshot'), {
        'schema', 'attempt_id', 'request_sha256', 'profile', 'budget', 'start_clock',
        'last_clock', 'deadline_boottime_ns', 'state', 'validity', 'authority_revision',
        'accounting_revision', 'authority_head', 'event_head', 'campaign_scope_id',
        'memory_peak_bytes', 'oom_events', 'works', 'settled_cpu_ns', 'reserved_cpu_ns',
        'remaining_cpu_ns'}, label='campaign budget snapshot')
    if doc['schema'] not in ('qualification_campaign_budget_snapshot/v1', 'qualification_campaign_budget_snapshot/v2'):
        raise ValueError('campaign budget snapshot schema required')
    if doc['state'] not in CAMPAIGN_BUDGET_STATES or doc['validity'] not in ('VALID', 'VOID'):
        raise ValueError('campaign budget state differs')
    _identity(doc['attempt_id'])
    for name in ('request_sha256', 'authority_head', 'event_head'):
        _sha256(doc[name], label=name)
    for name in ('authority_revision', 'accounting_revision', 'memory_peak_bytes', 'oom_events',
                 'settled_cpu_ns', 'reserved_cpu_ns', 'remaining_cpu_ns', 'deadline_boottime_ns'):
        _positive_int(doc[name], label=name, allow_zero=True)
    from .execution.campaign_budget import budget, clock, limits, integer, transition
    from .execution.profile import parse_campaign_budget_profile
    from .execution.protocol import decode_base64, fields
    parse_campaign_budget_profile(canonical_json_bytes(doc['profile']))
    clock(canonical_json_bytes(doc['start_clock']))
    clock(canonical_json_bytes(doc['last_clock']))
    if doc['campaign_scope_id'] is not None:
        _identity(doc['campaign_scope_id'])
    if doc['budget'] is not None:
        budget(canonical_json_bytes(doc['budget']))
    if doc['state'] == 'BOUND' and doc['budget'] is None:
        raise ValueError('bound budget absent')
    if doc['state'] == 'PROVISIONAL' and doc['budget'] is not None:
        raise ValueError('provisional budget already bound')
    if type(doc['works']) is not list:
        raise ValueError('campaign works required')
    identities = set()
    for work in doc['works']:
        _fields(work, {'work_id', 'phase', 'limits', 'input_sha256', 'reservation_bytes_b64',
                      'state', 'transitions', 'observation_bytes_b64', 'charge_cpu_ns'}, label='campaign work')
        _identity(work['work_id'])
        if work['work_id'] in identities or work['state'] not in CAMPAIGN_WORK_STATES:
            raise ValueError('campaign work identity/state differs')
        identities.add(work['work_id'])
        limits(work['limits'])
        if work['phase'] not in doc['profile']['phases'] or work['limits'] != doc['profile']['phases'][work['phase']]:
            raise ValueError('work phase configuration differs')
        reservation = parse_canonical_json(decode_base64(work['reservation_bytes_b64']), label='reservation')
        keys = {'limits', 'clock', 'input_sha256'}
        if type(reservation) is dict and 'signing_retry_of' in reservation:
            keys.add('signing_retry_of')
        fields(reservation, keys)
        if 'signing_retry_of' in reservation:
            if doc['schema'] != 'qualification_campaign_budget_snapshot/v2':
                raise ValueError('signing retry requires snapshot v2')
            _identity(reservation['signing_retry_of'])
        clock(canonical_json_bytes(reservation['clock']))
        if reservation['limits'] != work['limits'] or reservation['input_sha256'] != work['input_sha256']:
            raise ValueError('reservation identity differs')
        if work['observation_bytes_b64'] is not None:
            observation = fields(parse_canonical_json(decode_base64(work['observation_bytes_b64']), label='observation'), {'schema', 'attempt_id', 'work_id', 'clock', 'campaign_scope_id', 'work_scope_id', 'cpu_ns', 'memory_peak_bytes', 'oom_events'})
            if observation['schema'] != 'qualification_campaign_observation/v1' or observation['attempt_id'] != doc['attempt_id'] or observation['work_id'] != work['work_id']:
                raise ValueError('observation identity differs')
            clock(canonical_json_bytes(observation['clock']))
            _identity(observation['campaign_scope_id']); _identity(observation['work_scope_id'])
            for key in ('cpu_ns', 'memory_peak_bytes', 'oom_events'):
                if observation[key] is not None:
                    integer(observation[key])
            expected_charge = work['limits']['cpu_ns'] if observation['cpu_ns'] is None else observation['cpu_ns']
            if work['charge_cpu_ns'] != expected_charge:
                raise ValueError('settlement charge differs')
        elif work['charge_cpu_ns'] != 0:
            raise ValueError('unsettled work charge differs')
        _sha256(work['input_sha256'], label='work input')
        _positive_int(work['charge_cpu_ns'], label='charge', allow_zero=True)
        if type(work['transitions']) is not list:
            raise ValueError('work transitions required')
        for saved in work['transitions']:
            raw_transition = decode_base64(saved)
            if len(raw_transition) > doc['profile']['record_byte_limit']:
                raise ValueError('work metadata exceeds bounded storage')
            transition(raw_transition, doc['attempt_id'], work['work_id'])
    # Linked retries preserve a fixed intent while accounting new process work.
    # Older unlinked v1 snapshots remain byte-readable; no table migration.
    from .execution.protocol import sha256
    works = {w['work_id']: w for w in doc['works']}
    for work in doc['works']:
        reservation = parse_canonical_json(decode_base64(work['reservation_bytes_b64']), label='reservation')
        if 'signing_retry_of' not in reservation:
            continue
        parent = works.get(reservation['signing_retry_of'])
        if parent is None or parent is work or work['phase'] in ('N1', 'N2', 'PART_A'):
            raise ValueError('invalid signing retry parent')
        parent_reservation = parse_canonical_json(decode_base64(parent['reservation_bytes_b64']), label='reservation')
        intents = [parse_canonical_json(decode_base64(t), label='transition') for t in parent['transitions']]
        intent = next((t for t in intents if t['state'] == 'SIGNING_INTENT'), None)
        if ('signing_retry_of' in parent_reservation or parent['phase'] != work['phase'] or
                parent['observation_bytes_b64'] is None or intent is None or
                work['input_sha256'] != sha256(decode_base64(intent['data']['payload_bytes_b64']))):
            raise ValueError('signing retry binding differs')
        if work['state'] not in ('RESERVED', 'START_INTENT', 'RUNNING', 'COMPLETED', 'ABORTED'):
            raise ValueError('signing retry cannot create capture or authority')
        for raw_transition in work['transitions']:
            item = parse_canonical_json(decode_base64(raw_transition), label='retry transition')
            if item['state'] not in ('START_INTENT', 'RUNNING', 'COMPLETED'):
                raise ValueError('signing retry transition differs')
    if [w['work_id'] for w in doc['works']] != sorted(identities):
        raise ValueError('canonical work order required')
    return doc


def encode_campaign_budget_snapshot(document: dict) -> bytes:
    raw = canonical_json_bytes(document)
    parse_campaign_budget_snapshot(raw)
    return raw
