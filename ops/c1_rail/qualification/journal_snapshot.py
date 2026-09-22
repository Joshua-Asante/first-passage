"""Acyclic logical assessment snapshots. This module never opens a database."""

import re
from .contract import canonical_json_bytes, parse_canonical_json, _fields, _sha256, _positive_int

from .policy import ATTESTED_CHECKPOINTS as CHECKPOINTS

EXECUTION_STATES = (
    'PENDING',
    'DISPATCHED',
    'START_INTENT',
    'RUNNING',
    'CAPTURED',
    'ATTESTED',
    'ABORTED',
    'IN_DOUBT',
)


def _identity(value):
    if type(value) is not str or re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}', value) is None:
        raise ValueError('SNAPSHOT_IDENTITY_MISMATCH')


def parse_assessment_snapshot(raw: bytes) -> dict:
    doc = _fields(
        parse_canonical_json(raw, label='journal snapshot'),
        {
            'schema',
            'attempt_id',
            'contract_sha256',
            'trust_domain_sha256',
            'policy_sha256',
            'validity',
            'campaign_revision',
            'event_head',
            'executions',
        },
        label='journal snapshot',
    )
    if doc['schema'] != 'qualification_journal_snapshot/v1' or doc['validity'] not in (
        'VALID',
        'VOID',
    ):
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
        _fields(
            row,
            {
                'checkpoint',
                'execution_id',
                'execution_revision',
                'state',
                'plan_sha256',
                'attestation_sha256',
            },
            label='snapshot execution',
        )
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


def encode_assessment_snapshot(
    *,
    attempt_id,
    contract_sha256,
    trust_domain_sha256,
    policy_sha256,
    validity,
    campaign_revision,
    event_head,
    executions,
) -> bytes:
    rows = list(executions)
    if any(type(row) is not dict or row.get('checkpoint') not in CHECKPOINTS for row in rows):
        raise ValueError('SNAPSHOT_EXECUTIONS_MISMATCH')
    raw = canonical_json_bytes(
        {
            'schema': 'qualification_journal_snapshot/v1',
            'attempt_id': attempt_id,
            'contract_sha256': contract_sha256,
            'trust_domain_sha256': trust_domain_sha256,
            'policy_sha256': policy_sha256,
            'validity': validity,
            'campaign_revision': campaign_revision,
            'event_head': event_head,
            'executions': sorted(rows, key=lambda row: CHECKPOINTS.index(row['checkpoint'])),
        }
    )
    parse_assessment_snapshot(raw)
    return raw


CAMPAIGN_BUDGET_STATES = (
    'PROVISIONAL',
    'BOUND',
    'BUDGET_EXHAUSTED',
    'BUDGET_UNCERTAIN',
    'IN_DOUBT',
    'ABORTED',
    'N2_READY',
    'N1_FAILED',
    'PART_A_READY',
    'N2_FAILED',
)
CAMPAIGN_WORK_STATES = (
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
CHECKPOINT_FAMILY_STATES = ('CAPTURED', 'ATTESTED', 'ASSESSING', 'COMMITTED')


def _checkpoint_projection(value):
    """The closed `checkpoints` field of a /v6-or-/v7 snapshot; N1 only in S3
    (D1), N1 plus the joint N2 entry in S4 (T05 F3 names for the advance)."""
    if type(value) is not dict or set(value) - {'N1', 'N2'}:
        raise ValueError('checkpoint family projection differs')
    for checkpoint, row in value.items():
        required = {'state', 'work_id', 'payload_sha256'}
        if row.get('state') in ('ATTESTED', 'ASSESSING', 'COMMITTED'):
            required |= {'result_sha256', 'attestation_sha256'}
        if row.get('state') == 'COMMITTED':
            required |= {'assessment_sha256', 'receipt_sha256', 'decision'}
            if checkpoint == 'N2':
                required |= {'stage_decisions'}
        _fields(row, required, label='checkpoint family')
        if type(row) is not dict or row['state'] not in CHECKPOINT_FAMILY_STATES:
            raise ValueError('checkpoint family state differs')
        _identity(row['work_id'])
        for name in (
            'payload_sha256',
            'result_sha256',
            'attestation_sha256',
            'assessment_sha256',
            'receipt_sha256',
        ):
            if row.get(name) is not None:
                _sha256(row[name], label=name)
        if row['state'] != 'COMMITTED' and row.get('decision') is not None:
            raise ValueError('checkpoint decision requires a committed assessment')
        if row['state'] == 'COMMITTED' and row['decision'] not in ('CONTINUE', 'FAILURE'):
            raise ValueError('committed checkpoint decision differs')
        if checkpoint == 'N2':
            decisions = row.get('stage_decisions')
            if row['state'] == 'COMMITTED':
                if (
                    type(decisions) is not dict
                    or set(decisions) != {'N2', 'PART_B'}
                    or any(item not in ('PASS', 'FAIL') for item in decisions.values())
                ):
                    raise ValueError('committed joint stage decisions differ')
                if (row['decision'] == 'CONTINUE') != all(
                    item == 'PASS' for item in decisions.values()
                ):
                    raise ValueError('committed joint decision consistency differs')
            elif decisions is not None:
                raise ValueError('joint stage decisions require a committed assessment')
    return value


def parse_campaign_budget_snapshot(raw: bytes) -> dict:
    """Private accounting snapshot, deliberately separate from N1 snapshots.

    Authority revision/head exclude non-terminal accounting events. A signer
    binds authority revision plus its reserved work/intent; publication checks
    those values and the CURRENT ledger together inside ExecutionStore's lock.
    Full snapshot byte equality is not the publication freshness predicate.
    """
    document = parse_canonical_json(raw, label='campaign budget snapshot')
    revised = type(document) is dict and document.get('schema') in (
        'qualification_campaign_budget_snapshot/v4',
        'qualification_campaign_budget_snapshot/v5',
        'qualification_campaign_budget_snapshot/v6',
        'qualification_campaign_budget_snapshot/v7',
    )
    dispatched = type(document) is dict and document.get('schema') in (
        'qualification_campaign_budget_snapshot/v6',
        'qualification_campaign_budget_snapshot/v7',
    )
    doc = _fields(
        document,
        {
            'schema',
            'attempt_id',
            'request_sha256',
            'profile',
            'budget',
            'start_clock',
            'last_clock',
            'deadline_boottime_ns',
            'state',
            'validity',
            'authority_revision',
            'accounting_revision',
            'authority_head',
            'event_head',
            'campaign_scope_id',
            'memory_peak_bytes',
            'oom_events',
            'works',
            'settled_cpu_ns',
            'reserved_cpu_ns',
            'remaining_cpu_ns',
        }
        | ({'recoveries', 'dispatches'} if revised else set())
        | ({'checkpoints'} if dispatched else set()),
        label='campaign budget snapshot',
    )
    if doc['schema'] not in (
        'qualification_campaign_budget_snapshot/v1',
        'qualification_campaign_budget_snapshot/v2',
        'qualification_campaign_budget_snapshot/v3',
        'qualification_campaign_budget_snapshot/v4',
        'qualification_campaign_budget_snapshot/v5',
        'qualification_campaign_budget_snapshot/v6',
        'qualification_campaign_budget_snapshot/v7',
    ):
        raise ValueError('campaign budget snapshot schema required')
    if dispatched:
        _checkpoint_projection(doc['checkpoints'])
    if doc['state'] not in CAMPAIGN_BUDGET_STATES or doc['validity'] not in ('VALID', 'VOID'):
        raise ValueError('campaign budget state differs')
    _identity(doc['attempt_id'])
    for name in ('request_sha256', 'authority_head', 'event_head'):
        _sha256(doc[name], label=name)
    for name in (
        'authority_revision',
        'accounting_revision',
        'memory_peak_bytes',
        'oom_events',
        'settled_cpu_ns',
        'reserved_cpu_ns',
        'remaining_cpu_ns',
        'deadline_boottime_ns',
    ):
        _positive_int(doc[name], label=name, allow_zero=True)
    from .execution.campaign_budget import budget, clock, limits, integer, transition
    from .execution.profile import parse_campaign_budget_profile
    from .execution.protocol import decode_base64, fields

    parse_campaign_budget_profile(canonical_json_bytes(doc['profile']))
    if (
        doc['profile']['schema']
        in ('qualification_campaign_budget_profile/v2', 'qualification_campaign_budget_profile/v3')
    ) != (
        doc['schema']
        in (
            'qualification_campaign_budget_snapshot/v3',
            'qualification_campaign_budget_snapshot/v4',
            'qualification_campaign_budget_snapshot/v5',
            'qualification_campaign_budget_snapshot/v6',
            'qualification_campaign_budget_snapshot/v7',
        )
    ):
        raise ValueError('profile requires compatible snapshot version')
    if (doc['profile']['schema'] == 'qualification_campaign_budget_profile/v3') != (
        doc['schema']
        in (
            'qualification_campaign_budget_snapshot/v5',
            'qualification_campaign_budget_snapshot/v6',
            'qualification_campaign_budget_snapshot/v7',
        )
    ):
        raise ValueError('funding profile requires snapshot v5')
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
        _fields(
            work,
            {
                'work_id',
                'phase',
                'limits',
                'input_sha256',
                'reservation_bytes_b64',
                'state',
                'transitions',
                'observation_bytes_b64',
                'charge_cpu_ns',
            },
            label='campaign work',
        )
        _identity(work['work_id'])
        if work['work_id'] in identities or work['state'] not in CAMPAIGN_WORK_STATES:
            raise ValueError('campaign work identity/state differs')
        identities.add(work['work_id'])
        limits(work['limits'])
        if (
            work['phase'] not in doc['profile']['phases']
            or work['limits'] != doc['profile']['phases'][work['phase']]
        ):
            raise ValueError('work phase configuration differs')
        reservation = parse_canonical_json(
            decode_base64(work['reservation_bytes_b64']), label='reservation'
        )
        keys = {'limits', 'clock', 'input_sha256'}
        if type(reservation) is dict and 'signing_retry_of' in reservation:
            keys.add('signing_retry_of')
        fields(reservation, keys)
        if 'signing_retry_of' in reservation:
            if doc['schema'] not in (
                'qualification_campaign_budget_snapshot/v2',
                'qualification_campaign_budget_snapshot/v3',
                'qualification_campaign_budget_snapshot/v4',
                'qualification_campaign_budget_snapshot/v5',
                'qualification_campaign_budget_snapshot/v6',
                'qualification_campaign_budget_snapshot/v7',
            ):
                raise ValueError('signing retry requires snapshot v2')
            _identity(reservation['signing_retry_of'])
        clock(canonical_json_bytes(reservation['clock']))
        if (
            reservation['limits'] != work['limits']
            or reservation['input_sha256'] != work['input_sha256']
        ):
            raise ValueError('reservation identity differs')
        if work['observation_bytes_b64'] is not None:
            from .execution.campaign_budget import (
                observation as parse_observation,
                observation_charge,
            )

            observation = parse_observation(
                decode_base64(work['observation_bytes_b64']),
                attempt_id=doc['attempt_id'],
                work_id=work['work_id'],
                phase=work['phase'],
                profile=doc['profile'],
            )
            expected_charge = observation_charge(observation, work['limits'])
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
        reservation = parse_canonical_json(
            decode_base64(work['reservation_bytes_b64']), label='reservation'
        )
        if 'signing_retry_of' not in reservation:
            continue
        parent = works.get(reservation['signing_retry_of'])
        if parent is None or parent is work or work['phase'] in ('N1', 'N2', 'PART_A'):
            raise ValueError('invalid signing retry parent')
        parent_reservation = parse_canonical_json(
            decode_base64(parent['reservation_bytes_b64']), label='reservation'
        )
        intents = [
            parse_canonical_json(decode_base64(t), label='transition')
            for t in parent['transitions']
        ]
        intent = next((t for t in intents if t['state'] == 'SIGNING_INTENT'), None)
        if (
            'signing_retry_of' in parent_reservation
            or parent['phase'] != work['phase']
            or parent['observation_bytes_b64'] is None
            or intent is None
            or work['input_sha256'] != sha256(decode_base64(intent['data']['payload_bytes_b64']))
        ):
            raise ValueError('signing retry binding differs')
        if work['state'] not in ('RESERVED', 'START_INTENT', 'RUNNING', 'COMPLETED', 'ABORTED'):
            raise ValueError('signing retry cannot create capture or authority')
        for raw_transition in work['transitions']:
            item = parse_canonical_json(decode_base64(raw_transition), label='retry transition')
            if item['state'] not in ('START_INTENT', 'RUNNING', 'COMPLETED'):
                raise ValueError('signing retry transition differs')
    if revised:
        from .execution.campaign_budget import validate_recoveries, validate_dispatches

        validate_recoveries(doc)
        validate_dispatches(doc)
    if [w['work_id'] for w in doc['works']] != sorted(identities):
        raise ValueError('canonical work order required')
    return doc


def encode_campaign_budget_snapshot(document: dict) -> bytes:
    raw = canonical_json_bytes(document)
    parse_campaign_budget_snapshot(raw)
    return raw


# The FULL_E1 assessment snapshot (D1): the G5-facing view the service binds an
# assessment to -- authority revision plus the reserved work/intent and the
# checkpoint family identity -- deliberately separate from the N1_ONLY journal
# snapshot above and from the private budget snapshot.
CHECKPOINT_SNAPSHOT_SCHEMA = 'qualification_campaign_checkpoint_snapshot/v1'
CAMPAIGN_CHECKPOINT_STATES = (
    'PROVISIONAL',
    'BOUND',
    'BUDGET_EXHAUSTED',
    'BUDGET_UNCERTAIN',
    'IN_DOUBT',
    'ABORTED',
    'N2_READY',
    'N1_FAILED',
    'PART_A_READY',
    'N2_FAILED',
)
CAMPAIGN_CHECKPOINT_PHASES = (
    'ADMISSION',
    'N1',
    'N1_CAPTURE',
    'N1_G5',
    'N2',
    'N2_CAPTURE',
    'N2_G5',
    'PART_A',
    'PART_A_CAPTURE',
    'PART_A_G5',
    'RESULT',
    'SEAL',
)


def parse_campaign_checkpoint_snapshot(raw: bytes) -> dict:
    parsed = parse_canonical_json(raw, label='campaign checkpoint snapshot')
    required = {
        'schema',
        'attempt_id',
        'checkpoint',
        'contract_sha256',
        'trust_domain_sha256',
        'policy_sha256',
        'validity',
        'campaign_revision',
        'authority_head',
        'event_head',
        'campaign_state',
        'works',
        'capture',
        'intent',
        'members',
    }
    if type(parsed) is dict and parsed.get('checkpoint') == 'N2':
        required |= {'predecessor'}
    doc = _fields(parsed, required, label='campaign checkpoint snapshot')
    if (
        doc['schema'] != CHECKPOINT_SNAPSHOT_SCHEMA
        or doc['checkpoint'] not in ('N1', 'N2')
    ):
        raise ValueError('campaign checkpoint snapshot schema required')
    if doc['checkpoint'] == 'N2':
        predecessor = _fields(
            doc['predecessor'],
            {'checkpoint', 'assessment_sha256', 'receipt_sha256'},
            label='predecessor binding',
        )
        if predecessor['checkpoint'] != 'N1':
            raise ValueError('predecessor checkpoint differs')
        _sha256(predecessor['assessment_sha256'], label='predecessor assessment')
        _sha256(predecessor['receipt_sha256'], label='predecessor receipt')
    _identity(doc['attempt_id'])
    for name in (
        'contract_sha256',
        'trust_domain_sha256',
        'policy_sha256',
        'authority_head',
        'event_head',
    ):
        _sha256(doc[name], label=name)
    if (
        doc['validity'] not in ('VALID', 'VOID')
        or doc['campaign_state'] not in CAMPAIGN_CHECKPOINT_STATES
    ):
        raise ValueError('campaign checkpoint snapshot state differs')
    _positive_int(doc['campaign_revision'], label='campaign revision')
    if type(doc['works']) is not list:
        raise ValueError('campaign checkpoint works required')
    identities = set()
    for work in doc['works']:
        _fields(work, {'work_id', 'phase', 'state', 'settled'}, label='checkpoint snapshot work')
        _identity(work['work_id'])
        if (
            work['work_id'] in identities
            or work['state'] not in CAMPAIGN_WORK_STATES
            or work['phase'] not in CAMPAIGN_CHECKPOINT_PHASES
        ):
            raise ValueError('campaign checkpoint work identity differs')
        if type(work['settled']) is not bool:
            raise ValueError('campaign checkpoint settlement fact required')
        identities.add(work['work_id'])
    capture = doc['capture']
    _fields(
        capture,
        {'work_id', 'result_sha256', 'payload_sha256', 'attestation_sha256'},
        label='checkpoint snapshot capture',
    )
    _identity(capture['work_id'])
    for name in ('result_sha256', 'payload_sha256', 'attestation_sha256'):
        _sha256(capture[name], label=name)
    intent = doc['intent']
    _fields(intent, {'work_id', 'candidate_sha256'}, label='checkpoint snapshot intent')
    _identity(intent['work_id'])
    if intent['candidate_sha256'] is not None:
        _sha256(intent['candidate_sha256'], label='candidate')
    if type(doc['members']) is not list:
        raise ValueError('checkpoint member inventory required')
    member_ids = set()
    for member in doc['members']:
        _fields(member, {'role', 'sha256', 'byte_length'}, label='checkpoint member')
        _identity(member['role'])
        _sha256(member['sha256'], label='member bytes')
        _positive_int(member['byte_length'], label='member length')
        if member['role'] in member_ids:
            raise ValueError('duplicate checkpoint member role')
        member_ids.add(member['role'])
    required_members = {'plan', 'result', 'payload', 'attestation', 'retained_bundle_index'}
    if doc['checkpoint'] == 'N2':
        required_members |= {
            'predecessor_receipt',
            'predecessor_assessment',
            'predecessor_plan',
            'predecessor_payload',
        }
    if not required_members <= member_ids:
        raise ValueError('checkpoint member inventory incomplete')
    return doc


def encode_campaign_checkpoint_snapshot(
    *,
    attempt_id,
    checkpoint,
    contract_sha256,
    trust_domain_sha256,
    policy_sha256,
    validity,
    campaign_revision,
    authority_head,
    event_head,
    campaign_state,
    works,
    capture,
    intent,
    members,
    predecessor=None,
) -> bytes:
    document = {
        'schema': CHECKPOINT_SNAPSHOT_SCHEMA,
        'attempt_id': attempt_id,
        'checkpoint': checkpoint,
        'contract_sha256': contract_sha256,
        'trust_domain_sha256': trust_domain_sha256,
        'policy_sha256': policy_sha256,
        'validity': validity,
        'campaign_revision': campaign_revision,
        'authority_head': authority_head,
        'event_head': event_head,
        'campaign_state': campaign_state,
        'works': sorted(works, key=lambda row: row['work_id']),
        'capture': capture,
        'intent': intent,
        'members': sorted(members, key=lambda row: row['role']),
    }
    if checkpoint == 'N2':
        document['predecessor'] = predecessor
    raw = canonical_json_bytes(document)
    parse_campaign_checkpoint_snapshot(raw)
    return raw
