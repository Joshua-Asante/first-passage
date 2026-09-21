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


# Retained-object roles derived from a work identity ('supervision_' + work_id)
# share the namespace with the GLOB-queried 'supervision_control_*' and
# 'supervision_event_*' roles (_recovery_pending, integrity, campaign_host
# cleanup). A work named 'control_x' or 'event_x' would be parsed as a control
# claim or event body. 'admission' is the fixed, service-reserved first work.
RESERVED_WORK_ID_PREFIXES = ('control_', 'event_')
FIXED_WORK_IDS = ('admission',)


def validate_work_id(value, *, fixed=None):
    """A canonical work identity that cannot collide with a supervision object role.

    `fixed` names the one fixed identity a caller may use ('admission' for the
    service's own first work); every other producer is refused it.
    """
    identity(value)
    if value.startswith(RESERVED_WORK_ID_PREFIXES):
        raise ValueError('work identity collides with a supervision object role')
    if value in FIXED_WORK_IDS and value != fixed:
        raise ValueError('fixed work identity is reserved')
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


def observation(raw, *, attempt_id, work_id, phase, profile):
    """Canonical raw-counter evidence and distinct installed conservative charge."""
    revised = profile['schema'] in ('qualification_campaign_budget_profile/v2', 'qualification_campaign_budget_profile/v3')
    doc = fields(parse_canonical_json(raw, label='trusted campaign observation'), {
        'schema', 'attempt_id', 'work_id', 'clock', 'campaign_scope_id', 'work_scope_id',
        'cpu_ns', 'memory_peak_bytes', 'oom_events'} |
        ({'orchestration_charge_cpu_ns', 'termination_known'} if revised else set()))
    schema = 'qualification_campaign_observation/v2' if revised else 'qualification_campaign_observation/v1'
    if doc['schema'] != schema or doc['attempt_id'] != attempt_id or doc['work_id'] != work_id:
        raise ValueError('observation identity or version differs')
    clock(encoded(doc['clock']))
    identity(doc['campaign_scope_id']); identity(doc['work_scope_id'])
    for key in ('cpu_ns', 'memory_peak_bytes', 'oom_events'):
        if doc[key] is not None:
            integer(doc[key])
    if revised:
        if type(doc['termination_known']) is not bool:
            raise ValueError('trusted termination fact required')
        integer(doc['orchestration_charge_cpu_ns'], positive=True)
        if doc['orchestration_charge_cpu_ns'] != profile['orchestration_cpu_ns'][phase]:
            raise ValueError('full installed orchestration charge required')
    return doc


def observation_charge(doc, reservation):
    # Unknown work consumes the total reservation, never reservation + overhead.
    if doc['cpu_ns'] is None:
        return reservation['cpu_ns']
    return integer(doc['cpu_ns'] + doc.get('orchestration_charge_cpu_ns', 0))


def recovery_pending(state):
    """Temporary recovery barriers are separate from irreversible budget facts."""
    return any(row['completion_bytes_b64'] is None or row['continuation_required'] for row in state.get('recoveries', ()))


def recovery_completion(raw, *, attempt_id, work_id):
    doc = fields(parse_canonical_json(raw, label='recovery completion'), {
        'schema', 'attempt_id', 'work_id', 'claim_sha256', 'observations_sha256',
        'cleanup_event_sha256', 'clock'})
    if (doc['schema'] != 'qualification_campaign_recovery_completion/v1'
            or doc['attempt_id'] != attempt_id or doc['work_id'] != work_id):
        raise ValueError('recovery completion identity differs')
    for name in ('claim_sha256', 'observations_sha256', 'cleanup_event_sha256'):
        digest(doc[name])
    clock(encoded(doc['clock']))
    return doc


def validate_recoveries(state):
    from .protocol import decode_base64, sha256
    rows = state['recoveries']
    if type(rows) is not list or (not rows and not state['dispatches'] and state['schema'] != 'qualification_campaign_budget_snapshot/v5'):
        raise ValueError('versioned recovery records required')
    works = {w['work_id']: w for w in state['works']}
    identities = []
    for row in rows:
        fields(row, {'work_id', 'claim_sha256', 'owner_sha256',
                     'observations_bytes_b64', 'completion_bytes_b64', 'continuation_required'})
        identity(row['work_id']); digest(row['claim_sha256']); digest(row['owner_sha256'])
        if type(row['continuation_required']) is not bool:
            raise ValueError('strict continuation barrier required')
        if row['continuation_required'] and row['completion_bytes_b64'] is None:
            raise ValueError('continuation barrier requires historical completion')
        if row['work_id'] not in works:
            raise ValueError('recovery work absent')
        identities.append(row['work_id'])
        raw = None
        if row['observations_bytes_b64'] is not None:
            raw = decode_base64(row['observations_bytes_b64'])
            work = works[row['work_id']]
            # Recovery facts are historical: a RESERVED clock remains a
            # clock after a later abort or a post-completion first dispatch.
            fact = parse_canonical_json(raw, label='recovery facts')
            if type(fact) is dict and fact.get('schema') == 'qualification_campaign_clock/v1':
                clock(raw)
            else:
                observation(raw, attempt_id=state['attempt_id'], work_id=work['work_id'],
                            phase=work['phase'], profile=state['profile'])
        if row['completion_bytes_b64'] is not None:
            completed = recovery_completion(decode_base64(row['completion_bytes_b64']),
                attempt_id=state['attempt_id'], work_id=row['work_id'])
            if raw is None or completed['claim_sha256'] != row['claim_sha256'] or completed['observations_sha256'] != sha256(raw):
                raise ValueError('recovery completion facts differ')
    if identities != sorted(set(identities)):
        raise ValueError('canonical unique recovery order required')


def dispatch_pending(state, owner_sha256=None):
    return any(row['acknowledged_clock'] is None and row['owner_sha256'] != owner_sha256
               for row in state.get('dispatches', ()))


def validate_dispatches(state):
    rows = state['dispatches']
    if type(rows) is not list:
        raise ValueError('versioned dispatch records required')
    works = {w['work_id']: w for w in state['works']}
    identities = []
    owners = set()
    for row in rows:
        fields(row, {'work_id', 'role', 'owner_sha256', 'started_clock', 'acknowledged_clock'})
        identity(row['work_id']); digest(row['owner_sha256'])
        if row['work_id'] not in works or row['role'] not in ('guardian', 'payload'):
            raise ValueError('dispatch identity differs')
        if row['owner_sha256'] in owners:
            raise ValueError('dispatch owner must be unique')
        owners.add(row['owner_sha256'])
        clock(encoded(row['started_clock']))
        if row['acknowledged_clock'] is not None:
            clock(encoded(row['acknowledged_clock']))
        identities.append((row['work_id'], row['role']))
    if identities != sorted(set(identities)):
        raise ValueError('canonical unique dispatch order required')
