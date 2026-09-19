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
}


def parse_campaign_request(raw: bytes) -> dict:
    if type(raw) is not bytes:
        raise ValueError('immutable campaign request bytes required')
    doc = parse_canonical_json(raw, label='campaign request')
    if (type(doc) is not dict or type(doc.get('operation')) is not str
            or doc['operation'] not in _OPERATION_FIELDS):
        raise ValueError('UNKNOWN_OPERATION')
    fields(doc, {'schema', 'operation', 'attempt_id'} | _OPERATION_FIELDS[doc['operation']])
    if doc['schema'] != CAMPAIGN_REQUEST_SCHEMA:
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
    return doc


def permitted(role, operation):
    return operation in {'client': {'SUBMIT_E1', 'STATUS', 'FETCH_PLAN_CHUNK'},
        'g5': {'STATUS'}, 'operator': {'STATUS', 'VOID'}}.get(role, set())
