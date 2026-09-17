"""Closed byte protocol shared by separately installed trusted processes.

The dataclasses are values, not capabilities. Filesystem ownership and authenticated
peer credentials, not Python object identity, protect the authoritative journal.
"""
from __future__ import annotations

import base64
from dataclasses import dataclass
import hashlib
import re
import struct
from datetime import datetime

from ..contract import canonical_json_bytes, parse_canonical_json

JsonObject = dict[str, object]
ArtifactBytes = dict[str, bytes]


@dataclass(frozen=True)
class ExecutionRecord:
    execution_id: str
    attempt_id: str
    state: str
    revision: int
    plan_sha256: str
    attestation_sha256: str | None


@dataclass(frozen=True)
class CapturedOutput:
    container_id: str
    result_bytes: bytes
    exit_code: int
    oom_killed: bool
    supervisor_wall_ns: int


@dataclass(frozen=True)
class VerifiedExecution:
    attestation_bytes: bytes
    worker_result_bytes: bytes
    plan_bytes: bytes
    execution_id: str
    attempt_id: str


@dataclass(frozen=True)
class ValidatedEvidence:
    result_bytes: bytes
    attestation_sha256: str
    n1_decision: str
    expected_revision: int
    output_bytes_by_role: object
    journal_snapshot_sha256: str


def sha256(raw: bytes) -> str:
    if type(raw) is not bytes:
        raise TypeError('immutable bytes required')
    return hashlib.sha256(raw).hexdigest()


def fields(value, names):
    if type(value) is not dict or set(value) != set(names):
        raise ValueError('closed schema fields required')
    return value


def digest(value):
    if type(value) is not str or re.fullmatch('[0-9a-f]{64}', value) is None:
        raise ValueError('canonical SHA256 required')
    return value


def identity(value):
    if type(value) is not str or re.fullmatch('[A-Za-z0-9][A-Za-z0-9_.-]{0,127}', value) is None:
        raise ValueError('canonical identity required')
    return value


def positive(value):
    if type(value) is not int or not 0 < value <= 2**63 - 1:
        raise ValueError('bounded positive integer required')
    return value


def decode_base64(value):
    if type(value) is not str:
        raise ValueError('canonical base64 required')
    try:
        raw = base64.b64decode(value, validate=True)
    except (ValueError, UnicodeError) as exc:
        raise ValueError('canonical base64 required') from exc
    if base64.b64encode(raw).decode('ascii') != value:
        raise ValueError('canonical base64 required')
    return raw


ATTESTATION_PAYLOAD_FIELDS = frozenset({
    'schema','scope','authority_class','service_id','execution_id','attempt_id','checkpoint',
    'contract_sha256','trust_domain_sha256','exact_depth_approval_sha256','execution_release_sha256',
    'profile_sha256','plan_sha256','retained_bundle_sha256','runtime_manifest_sha256','worker_image_digest',
    'dispatch_event_sha256','capture_event_sha256','capture_revision','authorized_at_utc','started_utc',
    'completed_utc','completion','artifacts','observations'})


def utc_instant(value):
    if type(value) is not str or re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d{1,9})?Z', value) is None:
        raise ValueError('canonical UTC execution timestamp required')
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def parse_execution_attestation(raw):
    """Closed wire validation only; does not verify signatures or custody."""
    envelope = fields(parse_canonical_json(raw,label='execution attestation'), {'schema','payload','signature'})
    payload = fields(envelope['payload'], ATTESTATION_PAYLOAD_FIELDS)
    if (envelope['schema'] != 'qualification_execution_attestation/v1'
            or payload['schema'] != 'qualification_execution_attestation_payload/v1'
            or payload['scope'] != 'ATTEST_CHECKPOINT_EXECUTION'
            or payload['authority_class'] not in ('TEST_ONLY','OPERATOR')
            or payload['checkpoint'] != 'N1' or payload['completion'] != 'COMPLETED'):
        raise ValueError('unsupported execution attestation')
    for name in ('service_id','execution_id','attempt_id'):
        identity(payload[name])
    for name,value in payload.items():
        if name.endswith('_sha256'):
            digest(value)
    if type(payload['worker_image_digest']) is not str or re.fullmatch('sha256:[0-9a-f]{64}',payload['worker_image_digest']) is None:
        raise ValueError('immutable worker image identity required')
    positive(payload['capture_revision'])
    authorized,started,completed = (utc_instant(payload[name]) for name in ('authorized_at_utc','started_utc','completed_utc'))
    if not authorized <= started <= completed:
        raise ValueError('contradictory execution timestamps')
    if type(payload['artifacts']) is not list or len(payload['artifacts']) != 2:
        raise ValueError('closed captured artifact inventory required')
    for row,role in zip(payload['artifacts'], ('plan','worker_result')):
        fields(row, {'role','sha256','byte_length'})
        if row['role'] != role:
            raise ValueError('ordered captured artifact inventory required')
        digest(row['sha256']); positive(row['byte_length'])
    observations = fields(payload['observations'], {'exit_code','oom_killed','supervisor_wall_ns',
        'worker_compute_wall_ns','worker_cpu_ns','worker_peak_memory_bytes'})
    if type(observations['exit_code']) is not int or observations['exit_code'] != 0 or observations['oom_killed'] is not False:
        raise ValueError('abnormal execution cannot attest completion')
    for name in ('supervisor_wall_ns','worker_compute_wall_ns','worker_cpu_ns','worker_peak_memory_bytes'):
        if type(observations[name]) is not int or not 0 <= observations[name] <= 2**63-1:
            raise ValueError('bounded nonnegative observation required')
    signature = fields(envelope['signature'], {'algorithm','key_id','value_b64'})
    identity(signature['key_id'])
    if signature['algorithm'] != 'Ed25519' or len(decode_base64(signature['value_b64'])) != 64:
        raise ValueError('canonical Ed25519 signature required')
    return envelope


REQUEST_FIELDS = {
    'SUBMIT_N1': ('attempt_id', 'bundle_sha256'),
    'STATUS': ('attempt_id',),
    'FETCH': ('attempt_id', 'object_sha256'),
    'STORE_RESULT': ('attempt_id', 'envelope_bytes_b64'),
    'COMMIT_N1_RESULT': ('attempt_id', 'envelope_sha256', 'authentication_bytes'),
    'VOID': ('attempt_id', 'reason', 'operator_approval_bytes'),
}


def parse_request(raw: bytes) -> JsonObject:
    doc = parse_canonical_json(raw, label='execution request')
    if type(doc) is not dict or type(doc.get('operation')) is not str or doc['operation'] not in REQUEST_FIELDS:
        raise ValueError('UNKNOWN_OPERATION')
    fields(doc, ('operation', *REQUEST_FIELDS[doc['operation']]))
    identity(doc['attempt_id'])
    for name, value in doc.items():
        if name.endswith('_sha256'):
            digest(value)
        elif name in ('envelope_bytes_b64', 'authentication_bytes', 'operator_approval_bytes'):
            decode_base64(value)
    if 'reason' in doc and (type(doc['reason']) is not str or not doc['reason'].strip()
                            or len(doc['reason']) > 1024):
        raise ValueError('bounded invalidation reason required')
    return doc


def encode_frame(raw: bytes, *, limit: int) -> bytes:
    positive(limit)
    if type(raw) is not bytes or not 0 < len(raw) <= min(limit, 2**32 - 1):
        raise ValueError('frame size exceeds limit')
    parse_canonical_json(raw, label='frame')
    return struct.pack('!I', len(raw)) + raw


def decode_frame(raw: bytes, *, limit: int) -> bytes:
    positive(limit)
    if type(raw) is not bytes or len(raw) < 4:
        raise ValueError('truncated frame')
    length = struct.unpack('!I', raw[:4])[0]
    if not 0 < length <= limit or len(raw) != length + 4:
        raise ValueError('frame size, truncation or trailing frame')
    parse_canonical_json(raw[4:], label='frame')
    return raw[4:]
