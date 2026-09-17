"""Execution-signature and immutable-byte verification; no signing or journal."""
from datetime import datetime, timezone
import re

from c1_rail.ed25519_verify import verify as verify_ed25519
from ..contract import canonical_json_bytes as encoded, parse_canonical_json
from .admission import verify_bundle
from .plan import derive_n1_plan
from .protocol import VerifiedExecution, decode_base64, digest, fields, identity, positive, sha256
from .protocol import utc_instant, parse_execution_attestation

def verify_role_signature(envelope, *, context, current_keys, role):
    """Verify current enrollment as well as the signature over exact payload bytes."""
    signature = fields(envelope['signature'], {'algorithm', 'key_id', 'value_b64'})
    if signature['algorithm'] != 'Ed25519':
        raise ValueError('Ed25519 signature required')
    now = datetime.now(timezone.utc)
    registry = context.release.document['trusted_key_sha256']
    for key_id, fingerprint in registry.items():
        key = current_keys.get(key_id)
        if key is None or key.key_id != key_id or key.authority_class != context.domain.authority_class:
            raise ValueError('current signing identity or authority differs')
        if sha256(key.public_key) != fingerprint or context.domain.trusted_key_sha256.get(key_id) != fingerprint:
            raise ValueError('current signing public key differs')
        if key.revoked_at is not None and key.revoked_at <= now:
            raise ValueError('current signing key revoked')
    key_id = signature['key_id']
    if (type(key_id) is not str or key_id not in getattr(context.domain, role + '_key_ids')
            or key_id not in context.release.document['key_roles'][role]):
        raise ValueError('signature key is not enrolled for role')
    raw = decode_base64(signature['value_b64'])
    if len(raw) != 64 or not verify_ed25519(current_keys[key_id].public_key, encoded(envelope['payload']), raw):
        raise ValueError('invalid signature')
    return key_id


def verify_execution(attestation: bytes, artifacts: dict, *, context, expected_attempt_id: str,
                     current_keys: dict) -> VerifiedExecution:
    if type(attestation) is not bytes or len(attestation) > context.profile.rpc_byte_limit:
        raise ValueError('bounded immutable attestation required')
    envelope = parse_execution_attestation(attestation)
    payload = envelope['payload']
    verify_role_signature(envelope, context=context, current_keys=current_keys, role='execution')
    expected = dict(schema='qualification_execution_attestation_payload/v1', scope='ATTEST_CHECKPOINT_EXECUTION',
        authority_class=context.domain.authority_class, service_id=context.domain.execution_service_id,
        attempt_id=expected_attempt_id, checkpoint='N1', contract_sha256=context.contract.contract_sha256,
        trust_domain_sha256=context.domain.sha256, exact_depth_approval_sha256=context.exact_depth_approval.approval_sha256,
        execution_release_sha256=context.release.sha256, profile_sha256=context.profile.sha256,
        retained_bundle_sha256=context.bundle_sha256, runtime_manifest_sha256=context.release.runtime_sha256('worker'),
        worker_image_digest=context.release.document['worker_image_digest'], completion='COMPLETED')
    if expected_attempt_id != context.attempt_id:
        raise ValueError('attestation attempt differs from retained bundle')
    for name, value in expected.items():
        if payload[name] != value:
            raise ValueError(f'execution attestation {name} differs')
    identity(payload['execution_id']); identity(payload['attempt_id'])
    for name, value in payload.items():
        if name.endswith('_sha256'):
            digest(value)
    positive(payload['capture_revision'])
    authorized, started, completed = (utc_instant(payload[name]) for name in
                                       ('authorized_at_utc', 'started_utc', 'completed_utc'))
    if not authorized <= started <= completed <= datetime.now(timezone.utc):
        raise ValueError('missing or contradictory execution timestamps')
    # Historical evidence uses actual admission/start instants. G5 separately
    # revalidates authority at its current acceptance time.
    for instant in (authorized, started):
        original = verify_bundle(context.bundle_dir, context.installed_release, current_keys, instant)
        if original.bundle_sha256 != context.bundle_sha256 or original.contract.contract_sha256 != context.contract.contract_sha256:
            raise ValueError('original captured context differs')
    inventory = payload['artifacts']
    if type(inventory) is not list or len(inventory) != 2:
        raise ValueError('closed attested artifact inventory required')
    retained = {}
    for item, role in zip(inventory, ('plan', 'worker_result')):
        fields(item, {'role', 'sha256', 'byte_length'})
        if item['role'] != role:
            raise ValueError('ordered attested artifact roles differ')
        digest(item['sha256']); positive(item['byte_length'])
        raw = artifacts.get(item['sha256'])
        limit = context.profile.input_byte_limit if role == 'plan' else context.profile.output_byte_limit
        if (type(raw) is not bytes or len(raw) != item['byte_length'] or len(raw) > limit
                or sha256(raw) != item['sha256']):
            raise ValueError('attested artifact bytes or length differ')
        retained[role] = raw
    expected_plan = derive_n1_plan(context.contract, attempt_id=expected_attempt_id,
        exact_depth_approval_sha256=context.exact_depth_approval.approval_sha256)
    if retained['plan'] != expected_plan or sha256(expected_plan) != payload['plan_sha256']:
        raise ValueError('independently derived plan differs')
    observations = fields(payload['observations'], {'exit_code', 'oom_killed', 'supervisor_wall_ns',
        'worker_compute_wall_ns', 'worker_cpu_ns', 'worker_peak_memory_bytes'})
    if type(observations['exit_code']) is not int or observations['exit_code'] != 0 or observations['oom_killed'] is not False:
        raise ValueError('abnormal execution cannot attest completion')
    for name in ('supervisor_wall_ns', 'worker_compute_wall_ns', 'worker_cpu_ns', 'worker_peak_memory_bytes'):
        if type(observations[name]) is not int or observations[name] < 0:
            raise ValueError('nonnegative execution observations required')
    budget = context.contract.replay.budget
    if (observations['worker_compute_wall_ns'] >= budget.maximum_wall_seconds * 1000000000
            or observations['worker_cpu_ns'] > budget.maximum_cpu_seconds * 1000000000
            or observations['worker_peak_memory_bytes'] > min(budget.maximum_memory_bytes, context.profile.memory_bytes)
            or observations['supervisor_wall_ns'] > (budget.maximum_wall_seconds + context.profile.admission_seconds
                                                   + context.profile.capture_seconds) * 1000000000):
        raise ValueError('attested execution exceeds budget')
    return VerifiedExecution(attestation, retained['worker_result'], retained['plan'], payload['execution_id'], expected_attempt_id)
