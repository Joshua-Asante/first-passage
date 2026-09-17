"""Acyclic logical assessment snapshots. This module never opens a database."""
import re
from .contract import canonical_json_bytes, parse_canonical_json, _fields, _sha256, _positive_int

CHECKPOINTS = ('N1', 'N2', 'PART_A')
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
