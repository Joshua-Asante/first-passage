"""Closed admission-only FULL_E1 protocol; no execution or publication operations."""
from ..contract import parse_canonical_json
from ..checkpoint_plan import _CAMPAIGN_MAX_BYTES
from .protocol import fields, identity, digest, decode_base64

CAMPAIGN_REQUEST_SCHEMA = 'qualification_campaign_request/v1'
PLAN_CHUNK_LIMIT = 1024 * 1024
CAMPAIGN_RPC_MINIMUM = 2 * 1024 * 1024
_OPERATION_FIELDS = {
    'SUBMIT_E1': {'bundle_sha256', 'request_id'},
    'STATUS': set(),
    'FETCH_PLAN_CHUNK': {'object_sha256', 'offset', 'length'},
    'VOID': {'reason', 'operator_approval_bytes'},
    # The S3 checkpoint operations (G5 role only): the D1 assessment snapshot,
    # chunked member reads of the capture family and retained inputs, private
    # bounded staging, and the assessment commit inside the signing window.
    'CHECKPOINT_SNAPSHOT': {'checkpoint'},
    'FETCH_CHECKPOINT_MEMBER': {'checkpoint', 'object_sha256', 'offset', 'length'},
    'STAGE_CHECKPOINT_ARTIFACT': {'checkpoint', 'role', 'bytes_b64'},
    'COMMIT_CHECKPOINT_ASSESSMENT': {'checkpoint', 'work_id', 'candidate_bytes_b64', 'artifacts'},
}
CHECKPOINT_OPERATIONS = ('CHECKPOINT_SNAPSHOT', 'FETCH_CHECKPOINT_MEMBER',
                         'STAGE_CHECKPOINT_ARTIFACT', 'COMMIT_CHECKPOINT_ASSESSMENT')
CHECKPOINT_CHUNK_LIMIT = 1024 * 1024


def parse_campaign_request(raw: bytes) -> dict:
    if type(raw) is not bytes:
        raise ValueError('immutable campaign request bytes required')
    doc = parse_canonical_json(raw, label='campaign request')
    if (type(doc) is not dict or type(doc.get('operation')) is not str
            or doc['operation'] not in _OPERATION_FIELDS):
        raise ValueError('UNKNOWN_OPERATION')
    fields(doc, {'schema', 'operation', 'attempt_id'} | _OPERATION_FIELDS[doc['operation']])
    if doc['schema'] not in (CAMPAIGN_REQUEST_SCHEMA, 'qualification_campaign_request/v2'):
        raise ValueError('unsupported campaign request schema')
    identity(doc['attempt_id'])
    if doc['operation'] == 'SUBMIT_E1':
        digest(doc['bundle_sha256']); identity(doc['request_id'])
    elif doc['operation'] == 'FETCH_PLAN_CHUNK':
        digest(doc['object_sha256'])
        if type(doc['offset']) is not int or not 0 <= doc['offset'] < _CAMPAIGN_MAX_BYTES:
            raise ValueError('bounded integer chunk offset required')
        if type(doc['length']) is not int or not 1 <= doc['length'] <= PLAN_CHUNK_LIMIT:
            raise ValueError('bounded integer chunk length required')
    elif doc['operation'] == 'VOID':
        if type(doc['reason']) is not str or not doc['reason'] or len(doc['reason']) > 1000:
            raise ValueError('bounded VOID reason required')
        approval = decode_base64(doc['operator_approval_bytes'])
        if not approval or len(approval) > 65536:
            raise ValueError('bounded VOID approval required')
    elif doc['operation'] in CHECKPOINT_OPERATIONS:
        if doc['checkpoint'] != 'N1':
            raise ValueError('installed checkpoint required')
        if doc['operation'] == 'FETCH_CHECKPOINT_MEMBER':
            digest(doc['object_sha256'])
            if type(doc['offset']) is not int or not 0 <= doc['offset'] < _CAMPAIGN_MAX_BYTES:
                raise ValueError('bounded integer chunk offset required')
            if type(doc['length']) is not int or not 1 <= doc['length'] <= CHECKPOINT_CHUNK_LIMIT:
                raise ValueError('bounded integer chunk length required')
        elif doc['operation'] == 'STAGE_CHECKPOINT_ARTIFACT':
            identity(doc['role'])
            raw = decode_base64(doc['bytes_b64'])
            if not raw or len(raw) > 64 * 1024 * 1024:
                raise ValueError('bounded staged checkpoint artifact required')
        else:
            identity(doc['work_id'])
            candidate = decode_base64(doc['candidate_bytes_b64'])
            if not candidate or len(candidate) > 262144:
                raise ValueError('bounded checkpoint candidate required')
            if (type(doc['artifacts']) is not list
                    or any(type(row) is not dict or set(row) != {'role', 'sha256'} for row in doc['artifacts'])):
                raise ValueError('closed staged artifact inventory required')
            for row in doc['artifacts']:
                identity(row['role']); digest(row['sha256'])
    return doc


def permitted(role, operation):
    return operation in {'client': {'SUBMIT_E1', 'STATUS', 'FETCH_PLAN_CHUNK'},
        'g5': {'STATUS', *CHECKPOINT_OPERATIONS}, 'operator': {'STATUS', 'VOID'}}.get(role, set())
