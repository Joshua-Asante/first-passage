"""Signature fixtures test verification only, not service execution provenance."""
import base64
import copy
from dataclasses import replace
import importlib
import json

import pytest
from bundle_fixture import build_bundle
from test_contract import NOW
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.admission import verify_bundle
from c1_rail.qualification.execution.plan import derive_n1_plan
from c1_rail.qualification.execution.protocol import sha256


@pytest.fixture(scope='module')
def signed_case(tmp_path_factory):
    case = build_bundle(tmp_path_factory.mktemp('signed-unit') / 'bundle')
    context = verify_bundle(case['root'], case['release'], case['keys'], NOW)
    plan = derive_n1_plan(context.contract, attempt_id=context.attempt_id,
        exact_depth_approval_sha256=context.exact_depth_approval.approval_sha256)
    result = b'{"unit_capture":true}'
    payload = dict(schema='qualification_execution_attestation_payload/v1', scope='ATTEST_CHECKPOINT_EXECUTION',
        authority_class='TEST_ONLY', service_id='test-service', execution_id='unit-execution',
        attempt_id=context.attempt_id, checkpoint='N1', contract_sha256=context.contract.contract_sha256,
        trust_domain_sha256=context.domain.sha256, exact_depth_approval_sha256=context.exact_depth_approval.approval_sha256,
        execution_release_sha256=context.release.sha256, profile_sha256=context.profile.sha256, plan_sha256=sha256(plan),
        retained_bundle_sha256=context.bundle_sha256, runtime_manifest_sha256=context.release.runtime_sha256('worker'),
        worker_image_digest=context.release.document['worker_image_digest'], dispatch_event_sha256='a' * 64,
        capture_event_sha256='b' * 64, capture_revision=5, authorized_at_utc='2026-09-15T20:00:00Z',
        started_utc='2026-09-15T20:00:00Z', completed_utc='2026-09-15T20:00:01Z', completion='COMPLETED',
        artifacts=[dict(role=role, sha256=sha256(raw), byte_length=len(raw))
                   for role, raw in (('plan', plan), ('worker_result', result))],
        observations=dict(exit_code=0, oom_killed=False, supervisor_wall_ns=1000000000,
            worker_compute_wall_ns=1000000, worker_cpu_ns=1000000, worker_peak_memory_bytes=1000000))
    return context, case, payload, {sha256(plan): plan, sha256(result): result}


def signed(case, payload):
    return encoded(dict(schema='qualification_execution_attestation/v1', payload=payload,
        signature=dict(algorithm='Ed25519', key_id='test-execution', value_b64=base64.b64encode(
            case['private']['test-execution'].sign(encoded(payload))).decode())))


def verify(signed_case, *, mutation=None, keys=None):
    context, case, original, original_objects = signed_case
    payload, objects = copy.deepcopy(original), dict(original_objects)
    if mutation:
        mutation(payload, objects)
    module = importlib.import_module('c1_rail.qualification.execution.verification')
    return module.verify_execution(signed(case, payload), objects, context=context,
        expected_attempt_id=context.attempt_id, current_keys=keys or case['keys'])


def test_signed_bytes_bind_only_the_designated_plan_and_artifacts(signed_case):
    verified = verify(signed_case)
    assert verified.execution_id == 'unit-execution'
    assert verified.worker_result_bytes == b'{"unit_capture":true}'


def test_consistently_resigned_wrong_seed_namespace_and_pool_is_rejected(signed_case):
    def mutate(payload, objects):
        plan = json.loads(objects[payload['plan_sha256']])
        for seed in plan['seed_inputs']:
            seed.update(seed=seed['seed'] + 1, root_rng_namespace='substituted', source_session_ids_sha256='0' * 64)
        raw = encoded(plan)
        objects[sha256(raw)] = raw
        payload['plan_sha256'] = sha256(raw)
        payload['artifacts'][0].update(sha256=sha256(raw), byte_length=len(raw))
    with pytest.raises(ValueError, match='derived plan'):
        verify(signed_case, mutation=mutate)


@pytest.mark.parametrize('field,value', [
    ('checkpoint', 'N2'), ('service_id', 'other'), ('authority_class', 'OPERATOR'),
    ('retained_bundle_sha256', 'f' * 64), ('worker_image_digest', 'sha256:' + 'e' * 64),
    ('started_utc', '2026-09-16T20:00:00Z'), ('completed_utc', '2026-09-15T19:00:00Z'),
])
def test_signed_wrong_context_or_expired_actual_start_is_rejected(signed_case, field, value):
    with pytest.raises(ValueError):
        verify(signed_case, mutation=lambda p, o: p.update({field: value}))


def test_current_key_revocation_prevents_new_verification(signed_case):
    keys = dict(signed_case[1]['keys'])
    keys['test-execution'] = replace(keys['test-execution'], revoked_at=NOW)
    with pytest.raises(ValueError, match='revoked'):
        verify(signed_case, keys=keys)
