"""Pure, service-private lifetime budget arithmetic and trusted input validation.

Values are not capabilities. Only the installed supervisor may supply clocks or
cgroup counters; worker-reported measurements must never reach these parsers.
"""
from datetime import datetime

from ..contract import canonical_json_bytes as encoded, parse_canonical_json
from .protocol import fields, identity, digest

MAX_INTEGER = 2**63 - 1
PHASES = ('ADMISSION', 'N1', 'N1_CAPTURE', 'N1_G5', 'N2', 'N2_CAPTURE',
          'N2_G5', 'PART_A', 'PART_A_CAPTURE', 'PART_A_G5', 'RESULT', 'SEAL')


def integer(value, *, positive=False):
    if type(value) is not int or not (1 if positive else 0) <= value <= MAX_INTEGER:
        raise ValueError('bounded exact integer required')
    return value


def remaining_cpu(cap, settled, reserved):
    integer(cap, positive=True)
    values = tuple(settled) + tuple(reserved)
    for value in values:
        integer(value)
    return max(0, cap - sum(values))


def clock(raw):
    doc = fields(parse_canonical_json(raw, label='trusted clock'),
                 {'schema', 'boot_id', 'boottime_ns', 'utc'})
    if doc['schema'] != 'qualification_campaign_clock/v1':
        raise ValueError('trusted clock schema required')
    if doc['boot_id'] is not None:
        identity(doc['boot_id'])
    if doc['boottime_ns'] is not None:
        integer(doc['boottime_ns'])
    utc(doc['utc'])
    return doc


def utc(value):
    if type(value) is not str or not value.endswith('Z'):
        raise ValueError('UTC audit timestamp required')
    parsed = datetime.fromisoformat(value.removesuffix('Z') + '+00:00')
    if parsed.tzinfo is None:
        raise ValueError('aware UTC audit timestamp required')


def limits(value):
    fields(value, {'cpu_ns', 'wall_ns', 'memory_bytes'})
    for number in value.values():
        integer(number, positive=True)
    return value


def budget(raw):
    doc = fields(parse_canonical_json(raw, label='contract budget'), {
        'identity_sha256', 'maximum_cpu_seconds', 'maximum_wall_seconds',
        'maximum_memory_bytes', 'n1_paths', 'n2_paths', 'part_a_initial_paths',
        'part_a_expanded_paths', 'n3_paths'})
    digest(doc['identity_sha256'])
    for key, value in doc.items():
        if key != 'identity_sha256':
            integer(value, positive=True)
    integer(doc['maximum_cpu_seconds'] * 10**9, positive=True)
    integer(doc['maximum_wall_seconds'] * 10**9, positive=True)
    return doc


WORK_PREDECESSORS = {'START_INTENT': ('RESERVED',), 'RUNNING': ('START_INTENT',),
        'CAPTURED': ('START_INTENT', 'RUNNING'), 'SIGNING_INTENT': ('CAPTURED',),
        'SIGNED': ('SIGNING_INTENT',), 'COMPLETED': ('START_INTENT', 'RUNNING', 'CAPTURED', 'SIGNED'),
        'ABORTED': ('RESERVED',), 'IN_DOUBT': ('START_INTENT', 'RUNNING')}

def transition(raw, attempt_id, work_id):
    from .protocol import fields, identity, decode_base64

    doc = fields(parse_canonical_json(raw, label='work transition'),
                 {'schema', 'attempt_id', 'work_id', 'state', 'clock', 'data'})
    if (doc['schema'] != 'qualification_campaign_work_transition/v1' or
            doc['attempt_id'] != attempt_id or doc['work_id'] != work_id):
        raise ValueError('transition identity differs')
    clock(encoded(doc['clock']))
    target = doc['state']
    allowed = WORK_PREDECESSORS
    if target not in allowed:
        raise ValueError('unsupported work transition')
    data = doc['data']
    if target == 'START_INTENT':
        fields(data, {'campaign_scope_id', 'work_scope_id'})
        identity(data['campaign_scope_id']); identity(data['work_scope_id'])
    elif target == 'CAPTURED':
        fields(data, {'capture_bytes_b64'})
        if not decode_base64(data['capture_bytes_b64']):
            raise ValueError('complete saved capture required')
    elif target == 'SIGNING_INTENT':
        fields(data, {'intent_id', 'payload_bytes_b64', 'key_id', 'signing_at_utc'})
        identity(data['intent_id']); identity(data['key_id']); utc(data['signing_at_utc'])
        if not decode_base64(data['payload_bytes_b64']):
            raise ValueError('fixed signing payload required')
    elif target == 'SIGNED':
        fields(data, {'candidate_bytes_b64'})
        if not decode_base64(data['candidate_bytes_b64']):
            raise ValueError('saved candidate required')
    else:
        fields(data, set())
    return doc
