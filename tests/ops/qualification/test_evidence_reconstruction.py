"""Consistency-only reconstruction with real source admission, no signatures."""

import copy
import base64
import hashlib
import json
import pytest

from c1_rail.qualification.contract import canonical_json_bytes as encode
from c1_rail.qualification.policy import parse_policy
from c1_rail.qualification.policy_sources import build_qualification_policy
from c1_rail.qualification.source_admission import admit_source
from c1_rail.qualification.journal_snapshot import encode_assessment_snapshot
from c1_rail.qualification.orchestration import seed_input
from test_legality_evidence import signed_source_case


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def rebind_capture(args):
    """Coherent fixture hashes only; deliberately supplies no valid signature."""
    payload = json.loads(args['execution_attestation_bytes'])
    payload['payload']['plan_sha256'] = sha(args['plan_bytes'])
    payload['payload']['artifacts'] = [
        {'role': role, 'sha256': sha(raw), 'byte_length': len(raw)}
        for role, raw in [
            ('plan', args['plan_bytes']),
            ('worker_result', args['worker_result_bytes']),
        ]
    ]
    args['execution_attestation_bytes'] = encode(payload)
    snapshot = json.loads(args['journal_snapshot_bytes'])
    if snapshot['executions']:
        snapshot['executions'][0].update(
            attestation_sha256=sha(args['execution_attestation_bytes']),
            plan_sha256=sha(args['plan_bytes']),
        )
    args['journal_snapshot_bytes'] = encode(snapshot)


def test_continue_is_partial_even_with_completed_n1_time(captured_case):
    from c1_rail.qualification.evidence import build_n1_evidence

    args = dict(captured_case)
    worker = json.loads(args['worker_result_bytes'])
    records = iter(worker['path_inventory']['records'])
    for pop in worker['populations']:
        for row in pop['outcomes']:
            row.update(status='PASS', sessions_to_pass=1, failure_reason=None)
            next(records)['outcome_sha256'] = sha(encode(row))
    args['worker_result_bytes'] = encode(worker)
    rebind_capture(args)
    doc = json.loads(build_n1_evidence(**args).envelope_bytes)
    assert (doc['completion'], doc['verdict'], doc['terminal_reason']) == ('PARTIAL', 'NONE', None)
    assert doc['checkpoint_assessment'] == {'checkpoint': 'N1', 'decision': 'CONTINUE'}
    assert doc['completed_utc'] == '2026-09-15T20:00:01Z'


@pytest.fixture(scope='module')
def captured_case(tmp_path_factory):
    root = tmp_path_factory.mktemp('inspected-source')
    c, domain = signed_source_case(root)
    p = parse_policy(build_qualification_policy())
    admitted = admit_source(c, artifact_root=root, policy=p)
    runtime = {
        'python_version': '3.13.2',
        'platform': 'win32',
        'dependency_lock_sha256': 'd' * 64,
        'signing_configuration_sha256': 'e' * 64,
        'sources': {'consistency.fixture': {'path': 'fixture.py', 'sha256': 'e' * 64}},
    }
    release = {
        'schema': 'qualification_execution_release/v1',
        'service_id': 'fixture-service',
        'capability': 'N1_ONLY',
        'production_execution': False,
        'qualification_policy_sha256': p.sha256,
        'source_owner_sha256': json.loads(p.canonical_bytes)['source_owner_sha256'],
        'profile_sha256': 'f' * 64,
        'worker_image_digest': 'sha256:' + 'e' * 64,
        'runtime_manifests': {name: runtime for name in ('worker', 'g5', 'supervisor')},
    }
    profile = {
        'schema': 'qualification_execution_profile/v1',
        'protocol_version': 1,
        'supported_checkpoints': ['N1'],
        'capability': 'N1_ONLY',
        'production_execution': False,
        'input_byte_limit': 100000000,
        'output_byte_limit': 10000000,
        'log_byte_limit': 1000000,
        'rpc_byte_limit': 15000000,
        'worker_uid': 65532,
        'memory_bytes': 1000000000,
        'pids_limit': 64,
        'scratch_bytes': 10000000,
        'admission_seconds': 60,
        'capture_seconds': 10,
        'network': 'none',
        'read_only': True,
        'capabilities': [],
        'no_new_privileges': True,
        'privileged': False,
        'pid_mode': 'private',
        'ipc_mode': 'private',
        'restart': 'no',
    }
    release.update(
        release_id='consistency-release',
        authority_class='TEST_ONLY',
        profile=profile,
        profile_sha256=sha(encode(profile)),
        ordinary_code={
            'fixture': {'module': 'consistency.fixture', 'path': 'fixture.py', 'sha256': 'e' * 64}
        },
        worker_entrypoint=[
            '/opt/ops/bin/python',
            '-I',
            '/opt/qualification/bootstrap.py',
            'worker',
        ],
        port_roles=[
            'aegis_runtime_port',
            'orb_runtime_port',
            'striker_runtime_port',
            'vanguard_runtime_port',
        ],
        key_roles={role: [role] for role in ('freeze', 'result', 'seal', 'execution')},
        trusted_key_sha256={
            role: str(index) * 64
            for index, role in enumerate(('freeze', 'result', 'seal', 'execution'), 1)
        },
    )
    plan = {
        'schema': 'qualification_checkpoint_plan/v2',
        'checkpoint': 'N1',
        'attempt_id': 'attempt-1',
        'contract_sha256': c.contract_sha256,
        'trust_domain_sha256': domain.sha256,
        'policy_sha256': p.sha256,
        'execution_release_sha256': sha(encode(release)),
        'exact_depth_approval_sha256': 'c' * 64,
        'seed_inputs': [
            json.loads(
                seed_input(
                    c, stage='n1', population=pop, panel_index=None, path_index=i, synthetic=True
                ).canonical_bytes
            )
            for pop in ('FULL', 'H1', 'H2')
            for i in range(2)
        ],
    }
    original = json.loads(c.canonical_bytes)
    plan.update(
        authority_class='TEST_ONLY',
        depths=[{'population': pop, 'depth': 2} for pop in ('FULL', 'H1', 'H2')],
        horizon_sessions=c.replay.horizon_sessions,
        initial_state_sha256=sha(encode(original['initial_state'])),
        replay_sha256=sha(encode(original['replay'])),
        budget=original['replay']['budget'],
        mechanics_version='tb-s2-rng-v2',
        source_proofs=[
            {
                'population': pop,
                'horizon_sessions': len(c.populations[pop]),
                'source_session_ids_sha256': sha(encode(list(c.populations[pop]))),
            }
            for pop in ('FULL', 'H1', 'H2')
        ],
        probe=json.loads(
            seed_input(
                c, stage='probe', population='FULL', panel_index=None, path_index=0, synthetic=True
            ).canonical_bytes
        ),
    )
    populations, records = [], []
    for pop in ('FULL', 'H1', 'H2'):
        rows = []
        for i in range(2):
            row = {
                'status': 'UNRESOLVED',
                'sessions_to_pass': None,
                'failure_reason': 'horizon_cap',
                'diagnostics': [],
            }
            rows.append(row)
            seed = seed_input(
                c, stage='n1', population=pop, panel_index=None, path_index=i, synthetic=True
            )
            records.append(
                {
                    'stage': 'N1',
                    'population': pop,
                    'path_index': i,
                    'panel_id': None,
                    'seed_input_sha256': seed.sha256,
                    'outcome_sha256': sha(encode(row)),
                }
            )
        populations.append({'population': pop, 'outcomes': rows})
    worker = {
        'schema': 'qualification_worker_result/v1',
        'execution_id': 'exec-1',
        'plan_sha256': sha(encode(plan)),
        'source_admission': json.loads(admitted.source_admission_bytes),
        'legality': json.loads(admitted.legality_bytes),
        'populations': populations,
        'path_inventory': {
            'schema': 'qualification_path_inventory/v1',
            'trust_domain_sha256': domain.sha256,
            'records': records,
        },
        'runtime_load_manifest': [
            {'role': role, 'sha256': digest}
            for role, digest in sorted(c.runtime_load_sha256.items())
        ],
        'observations': {
            'worker_compute_wall_ns': 1,
            'worker_cpu_ns': 1,
            'worker_peak_memory_bytes': 1,
        },
    }
    payload = {
        'schema': 'qualification_execution_attestation_payload/v1',
        'scope': 'ATTEST_CHECKPOINT_EXECUTION',
        'authority_class': 'TEST_ONLY',
        'retained_bundle_sha256': '1' * 64,
        'dispatch_event_sha256': '2' * 64,
        'capture_event_sha256': '3' * 64,
        'capture_revision': 3,
        'authorized_at_utc': '2026-09-15T19:59:59Z',
        'attempt_id': 'attempt-1',
        'execution_id': 'exec-1',
        'checkpoint': 'N1',
        'contract_sha256': c.contract_sha256,
        'trust_domain_sha256': domain.sha256,
        'execution_release_sha256': sha(encode(release)),
        'service_id': 'fixture-service',
        'profile_sha256': release['profile_sha256'],
        'worker_image_digest': 'sha256:' + 'e' * 64,
        'runtime_manifest_sha256': sha(encode(runtime)),
        'plan_sha256': sha(encode(plan)),
        'exact_depth_approval_sha256': 'c' * 64,
        'completion': 'COMPLETED',
        'started_utc': '2026-09-15T20:00:00Z',
        'completed_utc': '2026-09-15T20:00:01Z',
        'artifacts': [
            {'role': role, 'sha256': sha(raw), 'byte_length': len(raw)}
            for role, raw in [('plan', encode(plan)), ('worker_result', encode(worker))]
        ],
        'observations': dict(
            exit_code=0, oom_killed=False, supervisor_wall_ns=2, **worker['observations']
        ),
    }
    attestation = encode(
        {
            'schema': 'qualification_execution_attestation/v1',
            'payload': payload,
            'signature': {
                'algorithm': 'Ed25519',
                'key_id': 'consistency-only',
                'value_b64': base64.b64encode(bytes(64)).decode('ascii'),
            },
        }
    )
    snapshot = encode_assessment_snapshot(
        attempt_id='attempt-1',
        contract_sha256=c.contract_sha256,
        trust_domain_sha256=domain.sha256,
        policy_sha256=p.sha256,
        validity='VALID',
        campaign_revision=5,
        event_head='a' * 64,
        executions=(
            {
                'checkpoint': 'N1',
                'execution_id': 'exec-1',
                'execution_revision': 4,
                'state': 'ATTESTED',
                'plan_sha256': sha(encode(plan)),
                'attestation_sha256': sha(attestation),
            },
        ),
    )
    return {
        'contract': c,
        'policy': p,
        'worker_result_bytes': encode(worker),
        'plan_bytes': encode(plan),
        'execution_attestation_bytes': attestation,
        'journal_snapshot_bytes': snapshot,
        'installed_release_bytes': encode(release),
    }


def test_reconstruction_retains_exact_adjudicated_artifacts(captured_case):
    from c1_rail.qualification.evidence import build_n1_evidence, compare_n1_evidence

    result = build_n1_evidence(**captured_case)
    compare_n1_evidence(result, expected=result)
    doc = json.loads(result.envelope_bytes)
    assert (doc['completion'], doc['verdict'], doc['terminal_reason']) == (
        'COMPLETE',
        'FAIL',
        'N1_SCREEN_FAILURE',
    )
    assert doc['journal_snapshot_sha256'] == sha(result.output_bytes_by_role['attempt_journal'])
    assert doc['stage_results'][1]['output_sha256'] == sha(result.output_bytes_by_role['n1_result'])
    assert json.loads(result.output_bytes_by_role['n1_result'])['population_counts'] == {
        'FULL': 2,
        'H1': 2,
        'H2': 2,
    }
    assert len(doc['outputs']) == 5


def test_n1_only_rejects_joint_continuation(captured_case):
    from c1_rail.qualification.evidence import (
        build_n1_evidence, compare_n1_evidence, InspectedEvidence,
    )
    result = build_n1_evidence(**captured_case)
    doc = json.loads(result.envelope_bytes)
    doc.update(completion='PARTIAL', verdict='NONE', terminal_reason=None)
    doc['checkpoint_assessment'] = {'checkpoint': 'N2', 'decision': 'CONTINUE'}
    changed = InspectedEvidence(encode(doc), result.output_bytes_by_role)
    with pytest.raises(ValueError, match='EVIDENCE_SEMANTIC_MISMATCH'):
        compare_n1_evidence(changed, expected=changed)


@pytest.mark.parametrize(
    'role',
    ['n1_result', 'legality_result', 'attempt_journal', 'runtime_load_trace', 'path_inventory'],
)
def test_consistently_rehashed_artifact_is_not_equivalent(captured_case, role):
    from c1_rail.qualification.evidence import (
        build_n1_evidence,
        compare_n1_evidence,
        InspectedEvidence,
    )

    expected = build_n1_evidence(**captured_case)
    outputs = dict(expected.output_bytes_by_role)
    outputs[role] = b'{"unrelated":true}'
    doc = json.loads(expected.envelope_bytes)
    entry = next(row for row in doc['outputs'] if row['role'] == role)
    entry.update(sha256=sha(outputs[role]), byte_length=len(outputs[role]))
    with pytest.raises(ValueError, match='EVIDENCE_SEMANTIC_MISMATCH'):
        compare_n1_evidence(InspectedEvidence(encode(doc), outputs), expected=expected)


@pytest.mark.parametrize(
    'change',
    [
        'void',
        'attempt',
        'policy',
        'unattested',
        'worker_hash',
        'legality_empty',
        'runtime',
        'plan_seed',
    ],
)
def test_input_relationship_substitutions_fail(captured_case, change):
    from c1_rail.qualification.evidence import build_n1_evidence

    args = dict(captured_case)
    key = 'journal_snapshot_bytes'
    if change in ('worker_hash', 'legality_empty', 'runtime'):
        key = 'worker_result_bytes'
    if change == 'plan_seed':
        key = 'plan_bytes'
    doc = json.loads(args[key])
    if change == 'void':
        doc['validity'] = 'VOID'
    elif change == 'attempt':
        doc['attempt_id'] = 'another'
    elif change == 'policy':
        doc['policy_sha256'] = '0' * 64
    elif change == 'unattested':
        doc['executions'] = []
    elif change == 'worker_hash':
        doc['execution_id'] = 'other'
    elif change == 'legality_empty':
        doc['legality'] = {}
    elif change == 'runtime':
        doc['runtime_load_manifest'] = []
    elif change == 'plan_seed':
        doc['seed_inputs'][0]['seed'] = 0
    args[key] = encode(doc)
    if key == 'worker_result_bytes':
        rebind_capture(args)
    if key == 'plan_bytes':
        worker = json.loads(args['worker_result_bytes'])
        worker['plan_sha256'] = sha(args['plan_bytes'])
        args['worker_result_bytes'] = encode(worker)
        rebind_capture(args)
    with pytest.raises(ValueError):
        build_n1_evidence(**args)


def test_equal_but_malformed_envelopes_cannot_compare(captured_case):
    from c1_rail.qualification.evidence import (
        build_n1_evidence,
        compare_n1_evidence,
        InspectedEvidence,
    )

    good = build_n1_evidence(**captured_case)
    doc = json.loads(good.envelope_bytes)
    doc['unexpected_authority'] = True
    malformed = InspectedEvidence(encode(doc), good.output_bytes_by_role)
    with pytest.raises(ValueError, match='EVIDENCE_SEMANTIC_MISMATCH'):
        compare_n1_evidence(malformed, expected=malformed)


@pytest.mark.parametrize(
    'change',
    [
        'runtime_manifest',
        'runtime_hash',
        'image',
        'empty_paths',
        'duplicate_paths',
        'reordered_paths',
    ],
)
def test_equal_but_malformed_artifacts_cannot_compare(captured_case, change):
    from c1_rail.qualification.evidence import (
        build_n1_evidence,
        compare_n1_evidence,
        InspectedEvidence,
    )

    good = build_n1_evidence(**captured_case)
    outputs = dict(good.output_bytes_by_role)
    role = (
        'runtime_load_trace'
        if change in ('runtime_manifest', 'runtime_hash', 'image')
        else 'path_inventory'
    )
    artifact = json.loads(outputs[role])
    if change == 'runtime_manifest':
        artifact['worker_load_manifest'] = None
    elif change == 'runtime_hash':
        artifact['profile_sha256'] = 42
    elif change == 'image':
        artifact['worker_image_digest'] = 'mutable:latest'
    elif change == 'empty_paths':
        artifact['records'] = []
    elif change == 'duplicate_paths':
        artifact['records'][1] = artifact['records'][0]
    elif change == 'reordered_paths':
        artifact['records'].reverse()
    outputs[role] = encode(artifact)
    doc = json.loads(good.envelope_bytes)
    doc[role + '_sha256'] = sha(outputs[role])
    next(row for row in doc['outputs'] if row['role'] == role).update(
        sha256=sha(outputs[role]), byte_length=len(outputs[role])
    )
    malformed = InspectedEvidence(encode(doc), outputs)
    with pytest.raises(ValueError, match='EVIDENCE_SEMANTIC_MISMATCH'):
        compare_n1_evidence(malformed, expected=malformed)


@pytest.mark.parametrize(
    'field',
    [
        'horizon_sessions',
        'budget',
        'source_proofs',
        'probe',
        'mechanics_version',
        'initial_state_sha256',
        'depths',
        'unknown',
    ],
)
def test_coherent_plan_changes_reject_before_reconstruction(captured_case, field):
    from c1_rail.qualification.evidence import build_n1_evidence

    args = dict(captured_case)
    plan = json.loads(args['plan_bytes'])
    plan[field] = None
    args['plan_bytes'] = encode(plan)
    worker = json.loads(args['worker_result_bytes'])
    worker['plan_sha256'] = sha(args['plan_bytes'])
    args['worker_result_bytes'] = encode(worker)
    rebind_capture(args)
    with pytest.raises(ValueError, match='EVIDENCE_PLAN_MISMATCH'):
        build_n1_evidence(**args)


@pytest.mark.parametrize(
    'field',
    [
        'authority_class',
        'retained_bundle_sha256',
        'dispatch_event_sha256',
        'capture_event_sha256',
        'capture_revision',
        'authorized_at_utc',
    ],
)
def test_incomplete_attestation_is_not_reconstruction_input(captured_case, field):
    from c1_rail.qualification.evidence import build_n1_evidence

    args = dict(captured_case)
    attestation = json.loads(args['execution_attestation_bytes'])
    del attestation['payload'][field]
    args['execution_attestation_bytes'] = encode(attestation)
    rebind_capture(args)
    with pytest.raises(ValueError, match='closed schema'):
        build_n1_evidence(**args)


@pytest.mark.parametrize(
    'field',
    [
        'ordinary_code',
        'profile',
        'key_roles',
        'trusted_key_sha256',
        'worker_entrypoint',
        'port_roles',
    ],
)
def test_incomplete_release_is_not_reconstruction_input(captured_case, field):
    from c1_rail.qualification.evidence import build_n1_evidence

    args = dict(captured_case)
    release = json.loads(args['installed_release_bytes'])
    del release[field]
    args['installed_release_bytes'] = encode(release)
    plan = json.loads(args['plan_bytes'])
    plan['execution_release_sha256'] = sha(args['installed_release_bytes'])
    args['plan_bytes'] = encode(plan)
    worker = json.loads(args['worker_result_bytes'])
    worker['plan_sha256'] = sha(args['plan_bytes'])
    args['worker_result_bytes'] = encode(worker)
    attestation = json.loads(args['execution_attestation_bytes'])
    attestation['payload']['execution_release_sha256'] = sha(args['installed_release_bytes'])
    args['execution_attestation_bytes'] = encode(attestation)
    rebind_capture(args)
    with pytest.raises(ValueError, match='closed schema'):
        build_n1_evidence(**args)


@pytest.mark.parametrize('kind', ['bytes', 'dict', 'proxy_bytes', 'value', 'evidence'])
def test_evidence_comparison_cannot_use_overloaded_equality(captured_case, kind):
    from types import MappingProxyType
    from c1_rail.qualification.evidence import (
        build_n1_evidence,
        compare_n1_evidence,
        InspectedEvidence,
    )

    good = build_n1_evidence(**captured_case)
    called = []

    class EqualBytes(bytes):
        def __eq__(self, other):
            called.append('bytes')
            return True

        def __ne__(self, other):
            called.append('bytes')
            return False

    class EqualDict(dict):
        def __eq__(self, other):
            called.append('dict')
            return True

    class EqualEvidence(InspectedEvidence):
        def __eq__(self, other):
            called.append('evidence')
            return True

    outputs = dict(good.output_bytes_by_role)
    raw = good.envelope_bytes
    if kind == 'bytes':
        raw = EqualBytes(raw)
    elif kind == 'dict':
        outputs = EqualDict(outputs)
    elif kind in ('value', 'proxy_bytes'):
        outputs['n1_result'] = EqualBytes(outputs['n1_result'])
        if kind == 'proxy_bytes':
            outputs = MappingProxyType(outputs)
    proposed = (EqualEvidence if kind == 'evidence' else InspectedEvidence)(raw, outputs)
    with pytest.raises(ValueError, match='EVIDENCE_SEMANTIC_MISMATCH'):
        compare_n1_evidence(proposed, expected=good)
    assert called == []


# ---- S3 FULL_E1 assessment vector beside the N1_ONLY one (GO condition b) ----


@pytest.fixture(scope='module')
def campaign_captured_case(tmp_path_factory):
    """The N1_ONLY captured case's own inputs rebuilt as the FULL_E1 family: a
    /v5 release, a campaign checkpoint attestation and snapshot over the same
    canonical plan/worker bytes."""
    root = tmp_path_factory.mktemp('campaign-inspected-source')
    c, domain = signed_source_case(root)
    p = parse_policy(build_qualification_policy())
    admitted = admit_source(c, artifact_root=root, policy=p)
    runtime = {
        'python_version': '3.13.2',
        'platform': 'win32',
        'dependency_lock_sha256': 'd' * 64,
        'signing_configuration_sha256': 'e' * 64,
        'sources': {'consistency.fixture': {'path': 'fixture.py', 'sha256': 'e' * 64}},
    }
    from c1_rail.qualification.execution.profile import (
        diagnostic_budget_profile,
        dispatch_diagnostic_execution_profile,
    )

    base_profile = {
        'schema': 'qualification_execution_profile/v1',
        'protocol_version': 1,
        'supported_checkpoints': ['N1'],
        'capability': 'N1_ONLY',
        'production_execution': False,
        'network': 'none',
        'read_only': True,
        'capabilities': [],
        'no_new_privileges': True,
        'privileged': False,
        'pid_mode': 'private',
        'ipc_mode': 'private',
        'restart': 'no',
        'input_byte_limit': 100000000,
        'output_byte_limit': 10000000,
        'log_byte_limit': 1000000,
        'rpc_byte_limit': 15000000,
        'worker_uid': 65532,
        'memory_bytes': 1000000000,
        'pids_limit': 64,
        'scratch_bytes': 10000000,
        'admission_seconds': 60,
        'capture_seconds': 10,
    }
    profile = dispatch_diagnostic_execution_profile(encode(base_profile))
    release = {
        'schema': 'qualification_execution_release/v5',
        'release_id': 'campaign-vector',
        'profile': profile,
        'profile_sha256': sha(encode(profile)),
        'authority_class': 'TEST_ONLY',
        'qualification_policy_sha256': p.sha256,
        'source_owner_sha256': json.loads(p.canonical_bytes)['source_owner_sha256'],
        'service_id': 'fixture-service',
        'capability': 'FULL_E1',
        'production_execution': False,
        'dispatch_enabled': True,
        'dispatch_checkpoints': ['N1'],
        'worker_image_digest': 'sha256:' + 'e' * 64,
        'runtime_manifests': {name: runtime for name in ('worker', 'g5', 'supervisor')},
        'ordinary_code': {
            'fixture': {'module': 'consistency.fixture', 'path': 'fixture.py', 'sha256': 'e' * 64}
        },
        'worker_entrypoint': [
            '/opt/ops/bin/python',
            '-I',
            '/opt/qualification/bootstrap.py',
            'worker',
        ],
        'port_roles': [
            'aegis_runtime_port',
            'orb_runtime_port',
            'striker_runtime_port',
            'vanguard_runtime_port',
        ],
        'key_roles': {role: [role] for role in ('freeze', 'result', 'seal', 'execution')},
        'trusted_key_sha256': {
            role: str(index) * 64
            for index, role in enumerate(('freeze', 'result', 'seal', 'execution'), 1)
        },
        'campaign_budget_profile': diagnostic_budget_profile(encode(profile)),
    }
    plan = {
        'schema': 'qualification_checkpoint_plan/v2',
        'checkpoint': 'N1',
        'attempt_id': 'attempt-1',
        'contract_sha256': c.contract_sha256,
        'trust_domain_sha256': domain.sha256,
        'policy_sha256': p.sha256,
        'execution_release_sha256': sha(encode(release)),
        'exact_depth_approval_sha256': 'c' * 64,
        'seed_inputs': [
            json.loads(
                seed_input(
                    c, stage='n1', population=pop, panel_index=None, path_index=i, synthetic=True
                ).canonical_bytes
            )
            for pop in ('FULL', 'H1', 'H2')
            for i in range(2)
        ],
    }
    original = json.loads(c.canonical_bytes)
    plan.update(
        authority_class='TEST_ONLY',
        depths=[{'population': pop, 'depth': 2} for pop in ('FULL', 'H1', 'H2')],
        horizon_sessions=c.replay.horizon_sessions,
        initial_state_sha256=sha(encode(original['initial_state'])),
        replay_sha256=sha(encode(original['replay'])),
        budget=original['replay']['budget'],
        mechanics_version='tb-s2-rng-v2',
        source_proofs=[
            {
                'population': pop,
                'horizon_sessions': len(c.populations[pop]),
                'source_session_ids_sha256': sha(encode(list(c.populations[pop]))),
            }
            for pop in ('FULL', 'H1', 'H2')
        ],
        probe=json.loads(
            seed_input(
                c, stage='probe', population='FULL', panel_index=None, path_index=0, synthetic=True
            ).canonical_bytes
        ),
    )
    populations, records = [], []
    for pop in ('FULL', 'H1', 'H2'):
        rows = []
        for i in range(2):
            row = {
                'status': 'UNRESOLVED',
                'sessions_to_pass': None,
                'failure_reason': 'horizon_cap',
                'diagnostics': [],
            }
            rows.append(row)
            seed = seed_input(
                c, stage='n1', population=pop, panel_index=None, path_index=i, synthetic=True
            )
            records.append(
                {
                    'stage': 'N1',
                    'population': pop,
                    'path_index': i,
                    'panel_id': None,
                    'seed_input_sha256': seed.sha256,
                    'outcome_sha256': sha(encode(row)),
                }
            )
        populations.append({'population': pop, 'outcomes': rows})
    worker_result = {
        'schema': 'qualification_worker_result/v1',
        'execution_id': 'n1work',
        'plan_sha256': sha(encode(plan)),
        'source_admission': json.loads(admitted.source_admission_bytes),
        'legality': json.loads(admitted.legality_bytes),
        'populations': populations,
        'path_inventory': {
            'schema': 'qualification_path_inventory/v1',
            'trust_domain_sha256': domain.sha256,
            'records': records,
        },
        'runtime_load_manifest': [
            {'role': role, 'sha256': digest}
            for role, digest in sorted(c.runtime_load_sha256.items())
        ],
        'observations': {
            'worker_compute_wall_ns': 1,
            'worker_cpu_ns': 1,
            'worker_peak_memory_bytes': 1,
        },
    }
    result = encode(
        {
            'schema': 'qualification_campaign_checkpoint_result/v1',
            'attempt_id': 'attempt-1',
            'checkpoint': 'N1',
            'work_id': 'n1work',
            'campaign_id': 'cid',
            'plan_sha256': sha(encode(plan)),
            'plan_byte_length': len(encode(plan)),
            'payload_sha256': sha(encode(worker_result)),
            'payload_byte_length': len(encode(worker_result)),
            'worker_execution_id': 'n1work',
            'container_id': '9' * 64,
            'worker_image_digest': 'sha256:' + 'e' * 64,
            'runtime_manifest_sha256': sha(encode(runtime)),
            'capture': {
                'exit_code': 0,
                'oom_killed': False,
                'started_utc': '2026-09-15T20:00:00Z',
                'completed_utc': '2026-09-15T20:00:01Z',
                'authorized_at_utc': '2026-09-15T19:59:59Z',
                'campaign_scope_id': 'fpq-c',
                'work_scope_id': 'fpq-w',
                'payload_slice': 'fpq-p',
            },
            'limits': {
                'cpu_ns': 120_000_000_000,
                'wall_ns': 300_000_000_000,
                'memory_bytes': 1000000000,
                'orchestration_cpu_ns': 20_000_000_000,
            },
            'observations': {
                'exit_code': 0,
                'oom_killed': False,
                'worker_compute_wall_ns': 1,
                'worker_cpu_ns': 1,
                'worker_peak_memory_bytes': 1,
            },
            'created_utc': '2026-09-15T20:00:02Z',
        }
    )
    attestation_payload = {
        'schema': 'qualification_campaign_checkpoint_attestation_payload/v1',
        'scope': 'ATTEST_CAMPAIGN_CHECKPOINT',
        'attempt_id': 'attempt-1',
        'checkpoint': 'N1',
        'work_id': 'n1work',
        'result_sha256': sha(result),
        'payload_sha256': sha(encode(worker_result)),
        'payload_byte_length': len(encode(worker_result)),
        'plan_sha256': sha(encode(plan)),
        'execution_release_sha256': sha(encode(release)),
        'profile_sha256': release['profile_sha256'],
        'service_id': 'fixture-service',
        'worker_image_digest': 'sha256:' + 'e' * 64,
        'runtime_manifest_sha256': sha(encode(runtime)),
        'container_id': '9' * 64,
        'capture': {
            'exit_code': 0,
            'oom_killed': False,
            'campaign_scope_id': 'fpq-c',
            'work_scope_id': 'fpq-w',
            'payload_slice': 'fpq-p',
        },
        'observations': {
            'exit_code': 0,
            'oom_killed': False,
            'worker_compute_wall_ns': 1,
            'worker_cpu_ns': 1,
            'worker_peak_memory_bytes': 1,
        },
        'authorized_at_utc': '2026-09-15T19:59:59Z',
        'started_utc': '2026-09-15T20:00:00Z',
        'completed_utc': '2026-09-15T20:00:01Z',
        'campaign_revision': 5,
    }
    attestation = encode(
        {
            'schema': 'qualification_campaign_checkpoint_attestation/v1',
            'payload': attestation_payload,
            'signature': {
                'algorithm': 'Ed25519',
                'key_id': 'consistency-only',
                'value_b64': base64.b64encode(bytes(64)).decode('ascii'),
            },
        }
    )
    from c1_rail.qualification.journal_snapshot import encode_campaign_checkpoint_snapshot

    snapshot = encode_campaign_checkpoint_snapshot(
        attempt_id='attempt-1',
        checkpoint='N1',
        contract_sha256=c.contract_sha256,
        trust_domain_sha256=domain.sha256,
        policy_sha256=p.sha256,
        validity='VALID',
        campaign_revision=5,
        authority_head='a' * 64,
        event_head='b' * 64,
        campaign_state='BOUND',
        works=[
            {'work_id': 'admission', 'phase': 'ADMISSION', 'state': 'COMPLETED', 'settled': True},
            {'work_id': 'n1work', 'phase': 'N1', 'state': 'COMPLETED', 'settled': True},
        ],
        capture={
            'work_id': 'n1work',
            'result_sha256': sha(result),
            'payload_sha256': sha(encode(worker_result)),
            'attestation_sha256': sha(attestation),
        },
        intent={'work_id': 'g5work', 'candidate_sha256': None},
        members=[
            {'role': name, 'sha256': sha(raw), 'byte_length': len(raw)}
            for name, raw in (
                ('plan', encode(plan)),
                ('result', result),
                ('payload', encode(worker_result)),
                ('attestation', attestation),
                ('retained_bundle_index', b'index'),
            )
        ],
    )
    return {
        'contract': c,
        'policy': p,
        'worker_result_bytes': encode(worker_result),
        'plan_bytes': encode(plan),
        'checkpoint_attestation_bytes': attestation,
        'checkpoint_snapshot_bytes': snapshot,
        'result_bytes': result,
        'installed_release_bytes': encode(release),
    }


def test_campaign_checkpoint_evidence_reconstructs_the_canonical_core(campaign_captured_case):
    from c1_rail.qualification.evidence import (
        build_checkpoint_evidence,
        compare_checkpoint_evidence,
        InspectedEvidence,
    )

    case = campaign_captured_case
    inspected = build_checkpoint_evidence(
        contract=case['contract'],
        policy=case['policy'],
        worker_result_bytes=case['worker_result_bytes'],
        plan_bytes=case['plan_bytes'],
        checkpoint_attestation_bytes=case['checkpoint_attestation_bytes'],
        checkpoint_snapshot_bytes=case['checkpoint_snapshot_bytes'],
        installed_release_bytes=case['installed_release_bytes'],
    )
    compare_checkpoint_evidence(inspected, expected=inspected)
    core = json.loads(inspected.envelope_bytes)
    # The vector's paths are all UNRESOLVED: a deterministic FAIL, committed as
    # the terminal statistical prefix -- never a full-PASS verdict.
    assert core['n1_decision'] == 'FAIL' and core['decision'] == 'FAILURE'
    assert core['capture']['attestation_sha256'] == sha(case['checkpoint_attestation_bytes'])
    assert core['snapshot']['snapshot_sha256'] == sha(case['checkpoint_snapshot_bytes'])
    assert [row['stage'] for row in core['stages']] == ['LEGALITY', 'N1']
    assert {row['role'] for row in core['artifacts']} == set(inspected.output_bytes_by_role)


def test_campaign_checkpoint_evidence_refuses_substituted_capture(campaign_captured_case):
    from c1_rail.qualification.evidence import build_checkpoint_evidence

    case = campaign_captured_case
    tampered = json.loads(case['worker_result_bytes'])
    tampered['populations'][0]['outcomes'][0]['status'] = 'PASS'
    with pytest.raises(ValueError):
        build_checkpoint_evidence(
            contract=case['contract'],
            policy=case['policy'],
            worker_result_bytes=encode(tampered),
            plan_bytes=case['plan_bytes'],
            checkpoint_attestation_bytes=case['checkpoint_attestation_bytes'],
            checkpoint_snapshot_bytes=case['checkpoint_snapshot_bytes'],
            installed_release_bytes=case['installed_release_bytes'],
        )
