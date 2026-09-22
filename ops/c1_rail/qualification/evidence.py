"""Pure reconstruction of retained evidence; no signer or persistent authority."""

from dataclasses import dataclass
import hashlib
import re
from typing import Mapping
from types import MappingProxyType

from .contract import (
    canonical_json_bytes,
    parse_canonical_json,
    _fields,
    _sha256,
    _instant,
    _positive_int,
)
from .checkpoint_plan import derive_n1_plan
from .execution.protocol import parse_execution_attestation
from .execution.release_schema import parse_release
from .journal_snapshot import parse_assessment_snapshot
from .legality import geometry_role, parse_source_admission
from .model import PathOutcome
from .seed_identity import seed_input
from .policy import _document, required_output_roles, N1_ARTIFACT_ROLES
from .result_adjudication import adjudicate_replay_outcomes


def _hash(raw):
    if type(raw) is not bytes:
        raise ValueError('IMMUTABLE_EVIDENCE_BYTES_REQUIRED')
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class InspectedEvidence:
    envelope_bytes: bytes
    output_bytes_by_role: Mapping[str, bytes]


def parse_proposed_artifact(role, raw):
    """Validate one candidate's closed shape; commitment still requires reconstruction."""
    if role == 'attempt_journal':
        return parse_assessment_snapshot(raw)
    shapes = {
        'legality_result': (
            'qualification_legality_result/v1',
            {
                'schema',
                'contract_sha256',
                'trust_domain_sha256',
                'policy_sha256',
                'geometry_source_sha256',
                'source_admission_sha256',
                'check_id',
                'status',
            },
        ),
        'n1_result': (
            'qualification_stage_result/v1',
            {
                'schema',
                'contract_sha256',
                'trust_domain_sha256',
                'policy_sha256',
                'stage',
                'input_plan_sha256',
                'outcome_array_sha256',
                'decision',
                'population_counts',
            },
        ),
        'path_inventory': (
            'qualification_path_inventory/v1',
            {'schema', 'trust_domain_sha256', 'records'},
        ),
        'runtime_load_trace': (
            'qualification_runtime_trace/v2',
            {
                'schema',
                'execution_release_sha256',
                'profile_sha256',
                'worker_image_digest',
                'runtime_manifest_sha256',
                'execution_id',
                'execution_attestation_sha256',
                'worker_load_manifest',
            },
        ),
    }
    if role not in shapes:
        raise ValueError('OUTPUT_ROLE_MISMATCH')
    schema, names = shapes[role]
    doc = _fields(parse_canonical_json(raw, label=role), names, label=role)
    if doc['schema'] != schema:
        raise ValueError('ARTIFACT_SCHEMA_MISMATCH')
    for name, value in doc.items():
        if name.endswith('_sha256'):
            _sha256(value, label=name)
    if role == 'legality_result' and (
        doc['status'] != 'PASS' or doc['check_id'] != 'PRE_ADMISSION_REGISTRY_EMPTY'
    ):
        raise ValueError('EVIDENCE_LEGALITY_MISMATCH')
    if role == 'n1_result':
        counts = _fields(doc['population_counts'], {'FULL', 'H1', 'H2'}, label='population counts')
        if (
            doc['stage'] != 'N1'
            or doc['decision'] not in ('PASS', 'FAIL')
            or any(type(n) is not int or n < 1 for n in counts.values())
        ):
            raise ValueError('EVIDENCE_STAGE_MISMATCH')
    if role == 'path_inventory':
        if type(doc['records']) is not list or not doc['records']:
            raise ValueError('PATH_INVENTORY_MISMATCH')
        for row in doc['records']:
            _fields(
                row,
                {
                    'stage',
                    'population',
                    'path_index',
                    'panel_id',
                    'seed_input_sha256',
                    'outcome_sha256',
                },
                label='path record',
            )
            if (
                row['stage'] != 'N1'
                or row['population'] not in ('FULL', 'H1', 'H2')
                or type(row['path_index']) is not int
                or row['path_index'] < 0
                or row['panel_id'] is not None
            ):
                raise ValueError('PATH_INVENTORY_MISMATCH')
            _sha256(row['seed_input_sha256'], label='seed')
            _sha256(row['outcome_sha256'], label='outcome')
    if role == 'runtime_load_trace':
        if type(doc['execution_id']) is not str or not doc['execution_id']:
            raise ValueError('invalid execution identity')
        if (
            type(doc['worker_image_digest']) is not str
            or re.fullmatch('sha256:[0-9a-f]{64}', doc['worker_image_digest']) is None
        ):
            raise ValueError('invalid image identity')
        if type(doc['worker_load_manifest']) is not list or not doc['worker_load_manifest']:
            raise ValueError('invalid load manifest')
        for row in doc['worker_load_manifest']:
            _fields(row, {'role', 'sha256'}, label='load role')
            if type(row['role']) is not str or not row['role']:
                raise ValueError('invalid load role')
            _sha256(row['sha256'], label='loaded bytes')
        roles = [row['role'] for row in doc['worker_load_manifest']]
        if roles != sorted(set(roles)):
            raise ValueError('invalid load role order')
    return doc


def validate_output_roles(policy, roles, *, stages, completion, verdict):
    required = required_output_roles(policy, stages=stages, completion=completion, verdict=verdict)
    optional = _document(policy)['optional_artifact_roles']
    if (
        type(roles) not in (list, tuple)
        or any(type(role) is not str for role in roles)
        or len(roles) != len(set(roles))
        or not set(required) <= set(roles)
        or not set(roles) <= set(required) | set(optional)
    ):
        raise ValueError('OUTPUT_ROLE_MISMATCH')


def _outcomes(raw, *, contract, policy, stage):
    doc = parse_canonical_json(raw, label='stage outcomes')
    populations = _document(policy)['stage_populations'].get(stage)
    if not populations or type(doc) is not list or len(doc) != len(populations):
        raise ValueError('OUTCOME_POPULATION_MISMATCH')
    result = {}
    for item, population in zip(doc, populations):
        _fields(item, {'population', 'outcomes'}, label='outcome population')
        if item['population'] != population or type(item['outcomes']) is not list:
            raise ValueError('OUTCOME_POPULATION_MISMATCH')
        rows = []
        for row in item['outcomes']:
            _fields(
                row,
                {'status', 'sessions_to_pass', 'failure_reason', 'diagnostics'},
                label='path outcome',
            )
            if type(row['diagnostics']) is not list or any(
                type(pair) is not list or len(pair) != 2 for pair in row['diagnostics']
            ):
                raise ValueError('OUTCOME_DIAGNOSTICS_MISMATCH')
            if type(row['status']) is not str or (
                row['failure_reason'] is not None and type(row['failure_reason']) is not str
            ):
                raise ValueError('OUTCOME_STATUS_MISMATCH')
            value = PathOutcome(
                row['status'],
                row['sessions_to_pass'],
                row['failure_reason'],
                tuple(tuple(pair) for pair in row['diagnostics']),
            )
            if value.status == 'PASS' and value.sessions_to_pass > contract.replay.horizon_sessions:
                raise ValueError('OUTCOME_HORIZON_MISMATCH')
            rows.append(value)
        depth = contract.stage_specs[stage].exact_depth
        counts = (
            (
                contract.replay.part_a.initial_panels * depth,
                contract.replay.part_a.expanded_panels * depth,
            )
            if stage == 'PART_A'
            else (depth,)
        )
        if len(rows) not in counts:
            raise ValueError('OUTCOME_DEPTH_MISMATCH')
        result[population] = tuple(rows)
    return doc, result


def _inspect_paths(raw, *, contract, stage, populations):
    inventory = _fields(
        parse_canonical_json(raw, label='path inventory'),
        {'schema', 'trust_domain_sha256', 'records'},
        label='path inventory',
    )
    if (
        inventory['schema'] != 'qualification_path_inventory/v1'
        or inventory['trust_domain_sha256'] != contract.trust_domain_sha256
        or type(inventory['records']) is not list
    ):
        raise ValueError('PATH_INVENTORY_MISMATCH')
    records = inventory['records']
    if len(records) != sum(len(item['outcomes']) for item in populations):
        raise ValueError('PATH_INVENTORY_MISMATCH')
    cursor = 0
    panel_ids = {}
    for population in populations:
        for index, outcome in enumerate(population['outcomes']):
            row = _fields(
                records[cursor],
                {
                    'stage',
                    'population',
                    'path_index',
                    'panel_id',
                    'seed_input_sha256',
                    'outcome_sha256',
                },
                label='path record',
            )
            cursor += 1
            panel = index // contract.stage_specs[stage].exact_depth if stage == 'PART_A' else None
            path = index % contract.stage_specs[stage].exact_depth if panel is not None else index
            if type(row['path_index']) is not int or (
                row['stage'],
                row['population'],
                row['path_index'],
            ) != (stage, population['population'], path):
                raise ValueError('PATH_INVENTORY_MISMATCH')
            if panel is None:
                if row['panel_id'] is not None:
                    raise ValueError('PATH_PANEL_MISMATCH')
            else:
                _sha256(row['panel_id'], label='panel identity')
                if panel not in panel_ids:
                    if row['panel_id'] in panel_ids.values():
                        raise ValueError('PATH_PANEL_MISMATCH')
                    panel_ids[panel] = row['panel_id']
                if panel_ids[panel] != row['panel_id']:
                    raise ValueError('PATH_PANEL_MISMATCH')
            expected = seed_input(
                contract,
                stage='n1' if stage == 'N1' else 'n2',
                population='FULL' if panel is not None else population['population'],
                panel_index=panel,
                path_index=path,
                synthetic=contract.trust_domain.permits_synthetic,
            )
            if row['seed_input_sha256'] != expected.sha256 or row['outcome_sha256'] != _hash(
                canonical_json_bytes(outcome)
            ):
                raise ValueError('PATH_OUTCOME_BINDING_MISMATCH')
    return inventory


def build_stage_artifact(
    *,
    contract,
    policy,
    stage,
    input_plan_sha256,
    outcome_bytes,
    path_inventory_bytes,
    prior_stage_outcomes,
) -> bytes:
    _sha256(input_plan_sha256, label='stage input plan')
    order = _document(policy)['stage_order'][1:]
    if stage not in order:
        raise ValueError('UNSUPPORTED_EVIDENCE_STAGE')
    prior_names = order[: order.index(stage)]
    if type(prior_stage_outcomes) is not dict or set(prior_stage_outcomes) != set(prior_names):
        raise ValueError('STAGE_PREREQUISITE_MISMATCH')
    outcomes = {
        name: _outcomes(prior_stage_outcomes[name], contract=contract, policy=policy, stage=name)[1]
        for name in prior_names
    }
    raw, current = _outcomes(outcome_bytes, contract=contract, policy=policy, stage=stage)
    inventory = _inspect_paths(
        path_inventory_bytes, contract=contract, stage=stage, populations=raw
    )
    outcomes[stage] = current
    decisions = adjudicate_replay_outcomes(contract, outcomes, inventory)
    counts = {
        population: len(rows)
        // (contract.stage_specs[stage].exact_depth if stage == 'PART_A' else 1)
        for population, rows in current.items()
    }
    return canonical_json_bytes(
        {
            'schema': 'qualification_stage_result/v1',
            'contract_sha256': contract.contract_sha256,
            'trust_domain_sha256': contract.trust_domain_sha256,
            'policy_sha256': policy.sha256,
            'stage': stage,
            'input_plan_sha256': input_plan_sha256,
            'outcome_array_sha256': _hash(outcome_bytes),
            'decision': decisions[stage],
            'population_counts': counts,
        }
    )


def build_n1_evidence(
    *,
    contract,
    policy,
    worker_result_bytes,
    plan_bytes,
    execution_attestation_bytes,
    journal_snapshot_bytes,
    installed_release_bytes,
) -> InspectedEvidence:
    """Check captured-byte relationships; callers separately authenticate custody.

    This intentionally does not verify an execution signature or import retained
    source. G5 must perform those checks on the original inputs before calling it.
    """
    resolved = _document(policy)
    release = parse_release(installed_release_bytes)
    plan = parse_canonical_json(plan_bytes, label='N1 plan')
    worker = _fields(
        parse_canonical_json(worker_result_bytes, label='worker result'),
        {
            'schema',
            'execution_id',
            'plan_sha256',
            'source_admission',
            'legality',
            'populations',
            'path_inventory',
            'runtime_load_manifest',
            'observations',
        },
        label='worker result',
    )
    attestation = parse_execution_attestation(execution_attestation_bytes)
    payload = attestation['payload']
    if payload['authority_class'] != contract.trust_domain.authority_class:
        raise ValueError('EVIDENCE_CONTEXT_MISMATCH')
    if (
        type(release) is not dict
        or type(plan) is not dict
        or type(payload) is not dict
        or release.get('schema') != 'qualification_execution_release/v1'
        or release.get('capability') != 'N1_ONLY'
        or release.get('production_execution') is not False
        or release.get('qualification_policy_sha256') != policy.sha256
        or release.get('source_owner_sha256') != resolved['source_owner_sha256']
        or plan.get('schema') != 'qualification_checkpoint_plan/v2'
        or worker['schema'] != 'qualification_worker_result/v1'
        or attestation['schema'] != 'qualification_execution_attestation/v1'
        or payload.get('schema') != 'qualification_execution_attestation_payload/v1'
        or payload.get('scope') != 'ATTEST_CHECKPOINT_EXECUTION'
        or payload.get('completion') != 'COMPLETED'
    ):
        raise ValueError('EVIDENCE_SCHEMA_MISMATCH')
    for name, expected in {
        'contract_sha256': contract.contract_sha256,
        'trust_domain_sha256': contract.trust_domain_sha256,
        'execution_release_sha256': _hash(installed_release_bytes),
        'checkpoint': 'N1',
    }.items():
        if plan.get(name) != expected or payload.get(name) != expected:
            raise ValueError('EVIDENCE_CONTEXT_MISMATCH')
    if (
        plan.get('policy_sha256') != policy.sha256
        or plan.get('attempt_id') != payload.get('attempt_id')
        or worker['execution_id'] != payload.get('execution_id')
        or worker['plan_sha256'] != _hash(plan_bytes)
        or payload.get('plan_sha256') != _hash(plan_bytes)
        or plan.get('exact_depth_approval_sha256') != payload.get('exact_depth_approval_sha256')
    ):
        raise ValueError('EVIDENCE_EXECUTION_MISMATCH')
    _sha256(plan['exact_depth_approval_sha256'], label='depth approval')
    expected_artifacts = [
        {'role': role, 'sha256': _hash(raw), 'byte_length': len(raw)}
        for role, raw in (('plan', plan_bytes), ('worker_result', worker_result_bytes))
    ]
    if canonical_json_bytes(payload.get('artifacts')) != canonical_json_bytes(expected_artifacts):
        raise ValueError('EVIDENCE_CAPTURE_MISMATCH')
    expected_plan = derive_n1_plan(
        contract,
        policy=policy,
        execution_release_sha256=_hash(installed_release_bytes),
        attempt_id=plan['attempt_id'],
        exact_depth_approval_sha256=plan['exact_depth_approval_sha256'],
    )
    if plan_bytes != expected_plan:
        raise ValueError('EVIDENCE_PLAN_MISMATCH')
    admission_bytes = canonical_json_bytes(worker['source_admission'])
    admission = parse_source_admission(
        admission_bytes,
        contract_sha256=contract.contract_sha256,
        domain_sha256=contract.trust_domain_sha256,
        policy=policy,
    )
    expected_roles = [
        {'role': item.role, 'sha256': item.sha256}
        for item in sorted(contract.artifacts, key=lambda item: item.role)
    ]
    if (
        admission['retained_roles'] != expected_roles
        or admission['effective_settings_sha256'] != contract.effective_settings_sha256
        or admission['population_sha256']
        != {
            pop: _hash(canonical_json_bytes(list(contract.populations[pop])))
            for pop in ('FULL', 'H1', 'H2')
        }
    ):
        raise ValueError('EVIDENCE_SOURCE_ADMISSION_MISMATCH')
    geometry = geometry_role(contract.trust_domain.runtime_code_roles)
    geometry_digest = next(item.sha256 for item in contract.artifacts if item.role == geometry)
    legality = {
        'schema': 'qualification_legality_result/v1',
        'contract_sha256': contract.contract_sha256,
        'trust_domain_sha256': contract.trust_domain_sha256,
        'policy_sha256': policy.sha256,
        'geometry_source_sha256': geometry_digest,
        'source_admission_sha256': _hash(admission_bytes),
        'check_id': 'PRE_ADMISSION_REGISTRY_EMPTY',
        'status': 'PASS',
    }
    if canonical_json_bytes(worker['legality']) != canonical_json_bytes(legality):
        raise ValueError('EVIDENCE_LEGALITY_MISMATCH')
    for name in ('service_id', 'profile_sha256', 'worker_image_digest'):
        if payload.get(name) != release.get(name):
            raise ValueError('EVIDENCE_RUNTIME_MISMATCH')
    worker_runtime = _hash(canonical_json_bytes(release['runtime_manifests']['worker']))
    if payload.get('runtime_manifest_sha256') != worker_runtime or worker[
        'runtime_load_manifest'
    ] != [
        {'role': role, 'sha256': digest}
        for role, digest in sorted(contract.runtime_load_sha256.items())
    ]:
        raise ValueError('EVIDENCE_RUNTIME_MISMATCH')
    observations = _fields(
        worker['observations'],
        {'worker_compute_wall_ns', 'worker_cpu_ns', 'worker_peak_memory_bytes'},
        label='worker observations',
    )
    for name, value in observations.items():
        if (
            type(value) is not int
            or value < 0
            or payload.get('observations', {}).get(name) != value
        ):
            raise ValueError('EVIDENCE_OBSERVATIONS_MISMATCH')
    if (
        payload['observations'].get('exit_code') != 0
        or payload['observations'].get('oom_killed') is not False
    ):
        raise ValueError('EVIDENCE_ABNORMAL_EXIT')
    if _instant(payload['completed_utc'], label='completed') < _instant(
        payload['started_utc'], label='started'
    ):
        raise ValueError('EVIDENCE_TIME_MISMATCH')
    snapshot = parse_assessment_snapshot(journal_snapshot_bytes)
    for name, expected in {
        'attempt_id': plan['attempt_id'],
        'contract_sha256': contract.contract_sha256,
        'trust_domain_sha256': contract.trust_domain_sha256,
        'policy_sha256': policy.sha256,
        'validity': 'VALID',
    }.items():
        if snapshot[name] != expected:
            raise ValueError('EVIDENCE_SNAPSHOT_MISMATCH')
    executions = snapshot['executions']
    if (
        len(executions) != 1
        or executions[0]['checkpoint'] != 'N1'
        or executions[0]['state'] != 'ATTESTED'
        or executions[0]['execution_id'] != worker['execution_id']
        or executions[0]['plan_sha256'] != _hash(plan_bytes)
        or executions[0]['attestation_sha256'] != _hash(execution_attestation_bytes)
    ):
        raise ValueError('EVIDENCE_SNAPSHOT_MEMBERSHIP_MISMATCH')
    path_bytes = canonical_json_bytes(worker['path_inventory'])
    stage_bytes = build_stage_artifact(
        contract=contract,
        policy=policy,
        stage='N1',
        input_plan_sha256=_hash(plan_bytes),
        outcome_bytes=canonical_json_bytes(worker['populations']),
        path_inventory_bytes=path_bytes,
        prior_stage_outcomes={},
    )
    stage = parse_canonical_json(stage_bytes, label='N1 result')
    failed = stage['decision'] == 'FAIL'
    completion, verdict = ('COMPLETE', 'FAIL') if failed else ('PARTIAL', 'NONE')
    runtime_bytes = canonical_json_bytes(
        {
            'schema': 'qualification_runtime_trace/v2',
            'execution_release_sha256': _hash(installed_release_bytes),
            'profile_sha256': release['profile_sha256'],
            'worker_image_digest': release['worker_image_digest'],
            'runtime_manifest_sha256': worker_runtime,
            'execution_id': worker['execution_id'],
            'execution_attestation_sha256': _hash(execution_attestation_bytes),
            'worker_load_manifest': worker['runtime_load_manifest'],
        }
    )
    outputs = {
        'attempt_journal': journal_snapshot_bytes,
        'legality_result': canonical_json_bytes(legality),
        'n1_result': stage_bytes,
        'path_inventory': path_bytes,
        'runtime_load_trace': runtime_bytes,
    }
    validate_output_roles(
        policy, list(outputs), stages=('LEGALITY', 'N1'), completion=completion, verdict=verdict
    )
    g5 = release['runtime_manifests']['g5']
    envelope = {
        'schema': 'qualification_result_envelope/v2',
        'attempt_id': plan['attempt_id'],
        'contract_sha256': contract.contract_sha256,
        'trust_domain_sha256': contract.trust_domain_sha256,
        'policy_sha256': policy.sha256,
        'shared_manifest_sha256': next(
            item.sha256 for item in contract.artifacts if item.role == 'shared_manifest'
        ),
        'exact_depth_approval_sha256': plan['exact_depth_approval_sha256'],
        'execution_release_sha256': _hash(installed_release_bytes),
        'producer': {
            'service_id': release['service_id'],
            'g5_code_sha256': _hash(canonical_json_bytes(g5['sources'])),
            'g5_runtime_sha256': _hash(canonical_json_bytes(g5)),
        },
        'started_utc': payload['started_utc'],
        'completed_utc': payload['completed_utc'],
        'completion': completion,
        'verdict': verdict,
        'terminal_reason': 'N1_SCREEN_FAILURE' if failed else None,
        'stage_results': [
            {
                'stage': 'LEGALITY',
                'status': 'PASS',
                'input_sha256': _hash(admission_bytes),
                'output_sha256': _hash(outputs['legality_result']),
                'population_counts': {},
            },
            {
                'stage': 'N1',
                'status': stage['decision'],
                'input_sha256': _hash(plan_bytes),
                'output_sha256': _hash(stage_bytes),
                'population_counts': stage['population_counts'],
            },
        ],
        'outputs': [
            {'role': role, 'sha256': _hash(raw), 'byte_length': len(raw), 'privacy': 'PRIVATE'}
            for role, raw in sorted(outputs.items())
        ],
        'path_inventory_sha256': _hash(path_bytes),
        'runtime_load_trace_sha256': _hash(runtime_bytes),
        'journal_revision': snapshot['campaign_revision'],
        'journal_snapshot_sha256': _hash(journal_snapshot_bytes),
        'execution_attestations': {'N1': _hash(execution_attestation_bytes)},
        'checkpoint_assessment': {
            'checkpoint': 'N1',
            'decision': 'FAILURE' if failed else 'CONTINUE',
        },
        'previous_result_sha256': None,
    }
    return InspectedEvidence(canonical_json_bytes(envelope), MappingProxyType(outputs))


def _inspect_n1_envelope(value):
    doc = _fields(
        parse_canonical_json(value.envelope_bytes, label='N1 envelope'),
        {
            'schema',
            'attempt_id',
            'contract_sha256',
            'trust_domain_sha256',
            'policy_sha256',
            'shared_manifest_sha256',
            'exact_depth_approval_sha256',
            'execution_release_sha256',
            'producer',
            'started_utc',
            'completed_utc',
            'completion',
            'verdict',
            'terminal_reason',
            'stage_results',
            'outputs',
            'path_inventory_sha256',
            'runtime_load_trace_sha256',
            'journal_revision',
            'journal_snapshot_sha256',
            'execution_attestations',
            'checkpoint_assessment',
            'previous_result_sha256',
        },
        label='N1 envelope',
    )
    if doc['schema'] != 'qualification_result_envelope/v2':
        raise ValueError('invalid envelope')
    for key in doc:
        if key.endswith('_sha256') and key != 'previous_result_sha256':
            _sha256(doc[key], label=key)
    if type(doc['attempt_id']) is not str or not doc['attempt_id']:
        raise ValueError('invalid attempt')
    producer = _fields(
        doc['producer'], {'service_id', 'g5_code_sha256', 'g5_runtime_sha256'}, label='producer'
    )
    if type(producer['service_id']) is not str or not producer['service_id']:
        raise ValueError('invalid producer')
    for key in ('g5_code_sha256', 'g5_runtime_sha256'):
        _sha256(producer[key], label=key)
    if _instant(doc['completed_utc'], label='completed') < _instant(
        doc['started_utc'], label='started'
    ):
        raise ValueError('invalid time order')
    assessment = _fields(
        doc['checkpoint_assessment'], {'checkpoint', 'decision'}, label='assessment'
    )
    failed = doc['verdict'] == 'FAIL'
    if (
        (doc['completion'], doc['verdict'], doc['terminal_reason'])
        != (('COMPLETE', 'FAIL', 'N1_SCREEN_FAILURE') if failed else ('PARTIAL', 'NONE', None))
        or assessment != {'checkpoint': 'N1', 'decision': 'FAILURE' if failed else 'CONTINUE'}
        or doc['previous_result_sha256'] is not None
    ):
        raise ValueError('invalid N1 assessment')
    attestations = _fields(doc['execution_attestations'], {'N1'}, label='attestations')
    _sha256(attestations['N1'], label='N1 attestation')
    roles = N1_ARTIFACT_ROLES
    if set(value.output_bytes_by_role) != set(roles) or type(doc['outputs']) is not list:
        raise ValueError('invalid N1 roles')
    expected_outputs = [
        {
            'role': role,
            'sha256': _hash(value.output_bytes_by_role[role]),
            'byte_length': len(value.output_bytes_by_role[role]),
            'privacy': 'PRIVATE',
        }
        for role in roles
    ]
    for entry in doc['outputs']:
        _fields(entry, {'role', 'sha256', 'byte_length', 'privacy'}, label='output')
        if type(entry['byte_length']) is not int:
            raise ValueError('invalid byte length')
    if doc['outputs'] != expected_outputs:
        raise ValueError('output bindings mismatch')
    artifacts = {
        role: parse_proposed_artifact(role, raw) for role, raw in value.output_bytes_by_role.items()
    }
    snapshot = parse_assessment_snapshot(value.output_bytes_by_role['attempt_journal'])
    if (
        type(doc['journal_revision']) is not int
        or doc['journal_revision'] != snapshot['campaign_revision']
        or snapshot['validity'] != 'VALID'
    ):
        raise ValueError('invalid snapshot revision')
    for key in ('attempt_id', 'contract_sha256', 'trust_domain_sha256', 'policy_sha256'):
        if snapshot[key] != doc[key]:
            raise ValueError('snapshot binding mismatch')
    for key, role in (
        ('journal_snapshot_sha256', 'attempt_journal'),
        ('path_inventory_sha256', 'path_inventory'),
        ('runtime_load_trace_sha256', 'runtime_load_trace'),
    ):
        if doc[key] != _hash(value.output_bytes_by_role[role]):
            raise ValueError('artifact binding mismatch')
    legality = _fields(
        artifacts['legality_result'],
        {
            'schema',
            'contract_sha256',
            'trust_domain_sha256',
            'policy_sha256',
            'geometry_source_sha256',
            'source_admission_sha256',
            'check_id',
            'status',
        },
        label='legality',
    )
    stage = _fields(
        artifacts['n1_result'],
        {
            'schema',
            'contract_sha256',
            'trust_domain_sha256',
            'policy_sha256',
            'stage',
            'input_plan_sha256',
            'outcome_array_sha256',
            'decision',
            'population_counts',
        },
        label='N1',
    )
    for artifact in (legality, stage):
        for key in ('contract_sha256', 'trust_domain_sha256', 'policy_sha256'):
            if artifact[key] != doc[key]:
                raise ValueError('stage binding mismatch')
        for key in artifact:
            if key.endswith('_sha256'):
                _sha256(artifact[key], label=key)
    if (
        legality['schema'] != 'qualification_legality_result/v1'
        or legality['status'] != 'PASS'
        or legality['check_id'] != 'PRE_ADMISSION_REGISTRY_EMPTY'
        or stage['schema'] != 'qualification_stage_result/v1'
        or stage['stage'] != 'N1'
        or stage['decision'] != ('FAIL' if failed else 'PASS')
    ):
        raise ValueError('invalid stage decision')
    counts = _fields(stage['population_counts'], {'FULL', 'H1', 'H2'}, label='counts')
    if any(type(n) is not int or n < 1 for n in counts.values()):
        raise ValueError('invalid population count')
    expected_stages = [
        {
            'stage': 'LEGALITY',
            'status': 'PASS',
            'input_sha256': legality['source_admission_sha256'],
            'output_sha256': _hash(value.output_bytes_by_role['legality_result']),
            'population_counts': {},
        },
        {
            'stage': 'N1',
            'status': stage['decision'],
            'input_sha256': stage['input_plan_sha256'],
            'output_sha256': _hash(value.output_bytes_by_role['n1_result']),
            'population_counts': counts,
        },
    ]
    if canonical_json_bytes(doc['stage_results']) != canonical_json_bytes(expected_stages):
        raise ValueError('stage bindings mismatch')
    paths = _fields(
        artifacts['path_inventory'], {'schema', 'trust_domain_sha256', 'records'}, label='paths'
    )
    if (
        paths['schema'] != 'qualification_path_inventory/v1'
        or paths['trust_domain_sha256'] != doc['trust_domain_sha256']
        or type(paths['records']) is not list
    ):
        raise ValueError('invalid paths')
    for row in paths['records']:
        _fields(
            row,
            {
                'stage',
                'population',
                'path_index',
                'panel_id',
                'seed_input_sha256',
                'outcome_sha256',
            },
            label='path',
        )
        if (
            row['stage'] != 'N1'
            or row['population'] not in counts
            or type(row['path_index']) is not int
            or row['path_index'] < 0
            or row['panel_id'] is not None
        ):
            raise ValueError('invalid N1 path')
        for key in ('seed_input_sha256', 'outcome_sha256'):
            _sha256(row[key], label=key)
    if [(row['population'], row['path_index']) for row in paths['records']] != [
        (population, index)
        for population in ('FULL', 'H1', 'H2')
        for index in range(counts[population])
    ]:
        raise ValueError('invalid path count or order')
    runtime = _fields(
        artifacts['runtime_load_trace'],
        {
            'schema',
            'execution_release_sha256',
            'profile_sha256',
            'worker_image_digest',
            'runtime_manifest_sha256',
            'execution_id',
            'execution_attestation_sha256',
            'worker_load_manifest',
        },
        label='runtime',
    )
    if (
        runtime['schema'] != 'qualification_runtime_trace/v2'
        or runtime['execution_release_sha256'] != doc['execution_release_sha256']
        or runtime['execution_attestation_sha256'] != attestations['N1']
    ):
        raise ValueError('invalid runtime binding')
    for key in ('profile_sha256', 'runtime_manifest_sha256'):
        _sha256(runtime[key], label=key)
    if (
        type(runtime['worker_image_digest']) is not str
        or re.fullmatch('sha256:[0-9a-f]{64}', runtime['worker_image_digest']) is None
    ):
        raise ValueError('invalid image identity')
    manifest = runtime['worker_load_manifest']
    if type(manifest) is not list or not manifest:
        raise ValueError('invalid load manifest')
    for row in manifest:
        _fields(row, {'role', 'sha256'}, label='load role')
        if type(row['role']) is not str or not row['role']:
            raise ValueError('invalid load role')
        _sha256(row['sha256'], label='loaded bytes')
    names = [row['role'] for row in manifest]
    if names != sorted(set(names)):
        raise ValueError('invalid load role order')
    if len(snapshot['executions']) != 1:
        raise ValueError('invalid snapshot membership')
    execution = snapshot['executions'][0]
    if (
        execution['checkpoint'] != 'N1'
        or execution['state'] != 'ATTESTED'
        or execution['execution_id'] != runtime['execution_id']
        or execution['plan_sha256'] != stage['input_plan_sha256']
        or execution['attestation_sha256'] != attestations['N1']
    ):
        raise ValueError('invalid execution membership')
    return doc


def compare_n1_evidence(proposed: InspectedEvidence, *, expected: InspectedEvidence) -> None:
    # Exact concrete byte containers prevent overloaded equality from making an
    # unrelated Python object compare equal. Neither object grants authority.
    for value in (proposed, expected):
        if (
            type(value) is not InspectedEvidence
            or type(value.envelope_bytes) is not bytes
            or type(value.output_bytes_by_role) not in (dict, MappingProxyType)
            or any(
                type(role) is not str or type(raw) is not bytes
                for role, raw in value.output_bytes_by_role.items()
            )
        ):
            raise ValueError('EVIDENCE_SEMANTIC_MISMATCH')
        try:
            _inspect_n1_envelope(value)
        except (ValueError, KeyError, TypeError) as exc:
            raise ValueError('EVIDENCE_SEMANTIC_MISMATCH') from exc
    if proposed.envelope_bytes != expected.envelope_bytes or dict(
        proposed.output_bytes_by_role
    ) != dict(expected.output_bytes_by_role):
        raise ValueError('EVIDENCE_SEMANTIC_MISMATCH')


def build_checkpoint_evidence(
    *,
    contract,
    policy,
    worker_result_bytes,
    plan_bytes,
    checkpoint_attestation_bytes,
    checkpoint_snapshot_bytes,
    installed_release_bytes,
    checkpoint='N1',
    predecessor_receipt_bytes=None,
    predecessor_assessment_bytes=None,
    predecessor_plan_bytes=None,
    predecessor_payload_bytes=None,
) -> InspectedEvidence:
    """Check the FULL_E1 checkpoint family's captured-byte relationships (D1).

    Mirrors ``build_n1_evidence`` for the campaign family: the installed
    dispatch release, the campaign checkpoint attestation and the campaign
    checkpoint snapshot are the only accepted shapes, and the canonical
    assessment core below is the signed candidate's exact unsigned content.
    Custody (signatures, current keys) is authenticated separately by the G5
    driver and the service commit. S4 (D2): ``checkpoint='N2'`` builds the
    joint LEGALITY/N1/N2/PART_B assessment from one captured batch and the
    committed N1 predecessor family.
    """
    if checkpoint == 'N2':
        return build_joint_checkpoint_evidence(
            contract=contract,
            policy=policy,
            worker_result_bytes=worker_result_bytes,
            plan_bytes=plan_bytes,
            checkpoint_attestation_bytes=checkpoint_attestation_bytes,
            checkpoint_snapshot_bytes=checkpoint_snapshot_bytes,
            installed_release_bytes=installed_release_bytes,
            predecessor_receipt_bytes=predecessor_receipt_bytes,
            predecessor_assessment_bytes=predecessor_assessment_bytes,
            predecessor_plan_bytes=predecessor_plan_bytes,
            predecessor_payload_bytes=predecessor_payload_bytes,
        )
    from .journal_snapshot import parse_campaign_checkpoint_snapshot

    resolved = _document(policy)
    release = parse_release(installed_release_bytes)
    plan = parse_canonical_json(plan_bytes, label='N1 plan')
    worker = _fields(
        parse_canonical_json(worker_result_bytes, label='worker result'),
        {
            'schema',
            'execution_id',
            'plan_sha256',
            'source_admission',
            'legality',
            'populations',
            'path_inventory',
            'runtime_load_manifest',
            'observations',
        },
        label='worker result',
    )
    snapshot = parse_campaign_checkpoint_snapshot(checkpoint_snapshot_bytes)
    attempt_id = snapshot['attempt_id']
    attestation = parse_checkpoint_attestation(checkpoint_attestation_bytes, attempt_id=attempt_id)
    payload = attestation['payload']
    if (
        type(release) is not dict
        or type(plan) is not dict
        or type(payload) is not dict
        or release.get('schema')
        not in (
            'qualification_execution_release/v5',
            'qualification_execution_release/v6',
        )
        or release.get('capability') != 'FULL_E1'
        or release.get('production_execution') is not False
        or release.get('dispatch_enabled') is not True
        or release.get('dispatch_checkpoints') not in (['N1'], ['N1', 'N2'])
        or release.get('qualification_policy_sha256') != policy.sha256
        or release.get('source_owner_sha256') != resolved['source_owner_sha256']
        or plan.get('schema') != 'qualification_checkpoint_plan/v2'
        or worker['schema'] != 'qualification_worker_result/v1'
        or payload['work_id'] != worker['execution_id']
        or snapshot['checkpoint'] != 'N1'
    ):
        raise ValueError('EVIDENCE_SCHEMA_MISMATCH')
    for name, expected in {
        'contract_sha256': contract.contract_sha256,
        'trust_domain_sha256': contract.trust_domain_sha256,
        'execution_release_sha256': _hash(installed_release_bytes),
        'checkpoint': 'N1',
    }.items():
        if plan.get(name) != expected:
            raise ValueError('EVIDENCE_CONTEXT_MISMATCH')
    if (
        plan.get('policy_sha256') != policy.sha256
        or plan.get('attempt_id') != attempt_id
        or worker['plan_sha256'] != _hash(plan_bytes)
        or payload['plan_sha256'] != _hash(plan_bytes)
    ):
        raise ValueError('EVIDENCE_EXECUTION_MISMATCH')
    if payload['payload_sha256'] != _hash(worker_result_bytes) or payload[
        'payload_byte_length'
    ] != len(worker_result_bytes):
        raise ValueError('EVIDENCE_CAPTURE_MISMATCH')
    expected_plan = derive_n1_plan(
        contract,
        policy=policy,
        execution_release_sha256=_hash(installed_release_bytes),
        attempt_id=attempt_id,
        exact_depth_approval_sha256=plan['exact_depth_approval_sha256'],
    )
    if plan_bytes != expected_plan:
        raise ValueError('EVIDENCE_PLAN_MISMATCH')
    admission_bytes = canonical_json_bytes(worker['source_admission'])
    admission = parse_source_admission(
        admission_bytes,
        contract_sha256=contract.contract_sha256,
        domain_sha256=contract.trust_domain_sha256,
        policy=policy,
    )
    expected_roles = [
        {'role': item.role, 'sha256': item.sha256}
        for item in sorted(contract.artifacts, key=lambda item: item.role)
    ]
    if (
        admission['retained_roles'] != expected_roles
        or admission['effective_settings_sha256'] != contract.effective_settings_sha256
        or admission['population_sha256']
        != {
            pop: _hash(canonical_json_bytes(list(contract.populations[pop])))
            for pop in ('FULL', 'H1', 'H2')
        }
    ):
        raise ValueError('EVIDENCE_SOURCE_ADMISSION_MISMATCH')
    geometry = geometry_role(contract.trust_domain.runtime_code_roles)
    geometry_digest = next(item.sha256 for item in contract.artifacts if item.role == geometry)
    legality = {
        'schema': 'qualification_legality_result/v1',
        'contract_sha256': contract.contract_sha256,
        'trust_domain_sha256': contract.trust_domain_sha256,
        'policy_sha256': policy.sha256,
        'geometry_source_sha256': geometry_digest,
        'source_admission_sha256': _hash(admission_bytes),
        'check_id': 'PRE_ADMISSION_REGISTRY_EMPTY',
        'status': 'PASS',
    }
    if canonical_json_bytes(worker['legality']) != canonical_json_bytes(legality):
        raise ValueError('EVIDENCE_LEGALITY_MISMATCH')
    for name in ('service_id', 'profile_sha256', 'worker_image_digest'):
        if payload.get(name) != release.get(name):
            raise ValueError('EVIDENCE_RUNTIME_MISMATCH')
    worker_runtime = _hash(canonical_json_bytes(release['runtime_manifests']['worker']))
    if payload.get('runtime_manifest_sha256') != worker_runtime or worker[
        'runtime_load_manifest'
    ] != [
        {'role': role, 'sha256': digest}
        for role, digest in sorted(contract.runtime_load_sha256.items())
    ]:
        raise ValueError('EVIDENCE_RUNTIME_MISMATCH')
    observations = _fields(
        worker['observations'],
        {'worker_compute_wall_ns', 'worker_cpu_ns', 'worker_peak_memory_bytes'},
        label='worker observations',
    )
    for name, value in observations.items():
        if (
            type(value) is not int
            or value < 0
            or payload.get('observations', {}).get(name) != value
        ):
            raise ValueError('EVIDENCE_OBSERVATIONS_MISMATCH')
    if (
        payload['observations'].get('exit_code') != 0
        or payload['observations'].get('oom_killed') is not False
    ):
        raise ValueError('EVIDENCE_ABNORMAL_EXIT')
    if _instant(payload['completed_utc'], label='completed') < _instant(
        payload['started_utc'], label='started'
    ):
        raise ValueError('EVIDENCE_TIME_MISMATCH')
    for name, expected in {
        'attempt_id': attempt_id,
        'contract_sha256': contract.contract_sha256,
        'trust_domain_sha256': contract.trust_domain_sha256,
        'policy_sha256': policy.sha256,
    }.items():
        if snapshot[name] != expected:
            raise ValueError('EVIDENCE_SNAPSHOT_MISMATCH')
    if (
        snapshot['capture']['payload_sha256'] != _hash(worker_result_bytes)
        or snapshot['capture']['result_sha256'] != payload['result_sha256']
        or snapshot['capture']['attestation_sha256'] != _hash(checkpoint_attestation_bytes)
    ):
        raise ValueError('EVIDENCE_SNAPSHOT_MEMBERSHIP_MISMATCH')
    path_bytes = canonical_json_bytes(worker['path_inventory'])
    stage_bytes = build_stage_artifact(
        contract=contract,
        policy=policy,
        stage='N1',
        input_plan_sha256=_hash(plan_bytes),
        outcome_bytes=canonical_json_bytes(worker['populations']),
        path_inventory_bytes=path_bytes,
        prior_stage_outcomes={},
    )
    stage = parse_canonical_json(stage_bytes, label='N1 result')
    failed = stage['decision'] == 'FAIL'
    runtime_bytes = canonical_json_bytes(
        {
            'schema': 'qualification_runtime_trace/v2',
            'execution_release_sha256': _hash(installed_release_bytes),
            'profile_sha256': release['profile_sha256'],
            'worker_image_digest': release['worker_image_digest'],
            'runtime_manifest_sha256': worker_runtime,
            'execution_id': worker['execution_id'],
            'execution_attestation_sha256': _hash(checkpoint_attestation_bytes),
            'worker_load_manifest': worker['runtime_load_manifest'],
        }
    )
    outputs = {
        'attempt_journal': checkpoint_snapshot_bytes,
        'legality_result': canonical_json_bytes(legality),
        'n1_result': stage_bytes,
        'path_inventory': path_bytes,
        'runtime_load_trace': runtime_bytes,
    }
    # The same accepted prefixes the N1_ONLY builder uses: a statistical FAIL
    # completes the LEGALITY/N1 evidence, a pass is the CONTINUE prefix only.
    completion, verdict = ('COMPLETE', 'FAIL') if failed else ('PARTIAL', 'NONE')
    validate_output_roles(
        policy, list(outputs), stages=('LEGALITY', 'N1'), completion=completion, verdict=verdict
    )
    n1_stage = contract.stage_specs['N1']
    cutoffs = {
        depth['population']: n1_stage.max_failures_per_population for depth in plan['depths']
    }
    thresholds = [
        {
            'stage': name,
            'exact_depth': contract.stage_specs[name].exact_depth,
            'max_failures_per_population': contract.stage_specs[name].max_failures_per_population,
        }
        for name in ('N2', 'PART_B')
    ]
    assessment = {
        'schema': 'qualification_campaign_checkpoint_assessment/v1',
        'attempt_id': attempt_id,
        'checkpoint': 'N1',
        'work_id': worker['execution_id'],
        'binding': {
            'contract_sha256': contract.contract_sha256,
            'trust_domain_sha256': contract.trust_domain_sha256,
            'policy_sha256': policy.sha256,
            'execution_release_sha256': _hash(installed_release_bytes),
        },
        'snapshot': {
            'campaign_revision': snapshot['campaign_revision'],
            'authority_head': snapshot['authority_head'],
            'snapshot_sha256': _hash(checkpoint_snapshot_bytes),
        },
        'capture': {
            'result_sha256': payload['result_sha256'],
            'payload_sha256': payload['payload_sha256'],
            'attestation_sha256': _hash(checkpoint_attestation_bytes),
        },
        'stages': [
            {
                'stage': 'LEGALITY',
                'status': 'PASS',
                'input_sha256': _hash(admission_bytes),
                'output_sha256': _hash(outputs['legality_result']),
                'population_counts': {},
            },
            {
                'stage': 'N1',
                'status': stage['decision'],
                'input_sha256': _hash(plan_bytes),
                'output_sha256': _hash(stage_bytes),
                'population_counts': stage['population_counts'],
            },
        ],
        'decision': 'FAILURE' if failed else 'CONTINUE',
        'n1_decision': stage['decision'],
        'cutoff': {'checkpoint': 'N1', 'n1_cutoffs': cutoffs},
        'n2_thresholds': {'bound_to': contract.contract_sha256, 'stages': thresholds},
        'artifacts': [
            {'role': role, 'sha256': _hash(raw), 'byte_length': len(raw)}
            for role, raw in sorted(outputs.items())
        ],
    }
    return InspectedEvidence(canonical_json_bytes(assessment), MappingProxyType(outputs))


def _joint_plan_vector(contract, policy):
    """The canonical /v3 joint-plan depths, seeds and thresholds, re-derived."""
    from .seed_identity import seed_input

    resolved = _document(policy)
    depths, seeds, thresholds = [], [], []
    for stage in resolved['checkpoint_groups']['N2']:
        spec = contract.stage_specs[stage]
        thresholds.append(
            {
                'stage': stage,
                'exact_depth': spec.exact_depth,
                'max_failures_per_population': spec.max_failures_per_population,
            }
        )
        for population in resolved['stage_populations'][stage]:
            (depth,) = spec.population_counts[population]
            depths.append(
                {'population': population, 'depth': depth, 'statistics_stage': stage}
            )
            seeds.extend(
                parse_canonical_json(
                    seed_input(
                        contract,
                        stage='n2',
                        population=population,
                        panel_index=None,
                        path_index=index,
                        synthetic=contract.trust_domain.permits_synthetic,
                    ).canonical_bytes,
                    label='seed',
                )
                for index in range(depth)
            )
    return depths, seeds, thresholds


def build_joint_checkpoint_evidence(
    *,
    contract,
    policy,
    worker_result_bytes,
    plan_bytes,
    checkpoint_attestation_bytes,
    checkpoint_snapshot_bytes,
    installed_release_bytes,
    predecessor_receipt_bytes,
    predecessor_assessment_bytes,
    predecessor_plan_bytes,
    predecessor_payload_bytes,
) -> InspectedEvidence:
    """S4-D2: one captured joint batch, one assessment with both stage decisions.

    LEGALITY is rebuilt from the batch's own admission; the N1 row and its
    n1_result artifact are the committed N1 assessment's row, rebuilt from the
    retained N1 custody bytes and cross-checked byte-for-byte; N2 and PART_B are
    rebuilt from this batch through the unchanged frozen adjudication. Never
    trusts a worker verdict; never re-draws.
    """
    from .journal_snapshot import parse_campaign_checkpoint_snapshot

    resolved = _document(policy)
    release = parse_release(installed_release_bytes)
    plan = parse_canonical_json(plan_bytes, label='N2 plan')
    worker = _fields(
        parse_canonical_json(worker_result_bytes, label='worker result'),
        {
            'schema',
            'execution_id',
            'plan_sha256',
            'source_admission',
            'legality',
            'populations',
            'path_inventory',
            'runtime_load_manifest',
            'observations',
        },
        label='worker result',
    )
    snapshot = parse_campaign_checkpoint_snapshot(checkpoint_snapshot_bytes)
    attempt_id = snapshot['attempt_id']
    attestation = parse_checkpoint_attestation(checkpoint_attestation_bytes, attempt_id=attempt_id)
    payload = attestation['payload']
    if (
        type(release) is not dict
        or type(plan) is not dict
        or type(payload) is not dict
        or release.get('schema') != 'qualification_execution_release/v6'
        or release.get('capability') != 'FULL_E1'
        or release.get('production_execution') is not False
        or release.get('dispatch_enabled') is not True
        or release.get('dispatch_checkpoints') != ['N1', 'N2']
        or release.get('qualification_policy_sha256') != policy.sha256
        or release.get('source_owner_sha256') != resolved['source_owner_sha256']
        or plan.get('schema') != 'qualification_checkpoint_plan/v3'
        or plan.get('checkpoint') != 'N2'
        or worker['schema'] != 'qualification_worker_result/v1'
        or payload['work_id'] != worker['execution_id']
        or snapshot['checkpoint'] != 'N2'
    ):
        raise ValueError('EVIDENCE_SCHEMA_MISMATCH')
    for name, expected in {
        'contract_sha256': contract.contract_sha256,
        'trust_domain_sha256': contract.trust_domain_sha256,
        'execution_release_sha256': _hash(installed_release_bytes),
    }.items():
        if plan.get(name) != expected:
            raise ValueError('EVIDENCE_CONTEXT_MISMATCH')
    original = parse_canonical_json(contract.canonical_bytes, label='contract')
    depths, seeds, thresholds = _joint_plan_vector(contract, policy)
    if (
        plan.get('policy_sha256') != policy.sha256
        or plan.get('attempt_id') != attempt_id
        or plan.get('depths') != depths
        or plan.get('seed_inputs') != seeds
        or plan.get('thresholds') != thresholds
        or plan.get('horizon_sessions') != contract.replay.horizon_sessions
        or plan.get('initial_state_sha256')
        != _hash(canonical_json_bytes(original['initial_state']))
        or plan.get('replay_sha256') != _hash(canonical_json_bytes(original['replay']))
        or plan.get('budget') != original['replay']['budget']
        or plan.get('mechanics_version') != 'tb-s2-rng-v2'
        or worker['plan_sha256'] != _hash(plan_bytes)
        or payload['plan_sha256'] != _hash(plan_bytes)
    ):
        raise ValueError('EVIDENCE_PLAN_MISMATCH')
    receipt = parse_canonical_json(predecessor_receipt_bytes, label='predecessor receipt')
    if (
        type(receipt) is not dict
        or receipt.get('schema') != CHECKPOINT_RECEIPT_SCHEMA
        or receipt.get('checkpoint') != 'N1'
        or receipt.get('attempt_id') != attempt_id
        or receipt.get('decision') != 'CONTINUE'
        or receipt.get('campaign_state') != 'N2_READY'
        or plan.get('predecessor') != {
            'checkpoint': 'N1',
            'receipt_sha256': _hash(predecessor_receipt_bytes),
        }
        or snapshot['predecessor'] != {
            'checkpoint': 'N1',
            'assessment_sha256': _hash(predecessor_assessment_bytes),
            'receipt_sha256': _hash(predecessor_receipt_bytes),
        }
    ):
        raise ValueError('predecessor receipt binding differs')
    predecessor = parse_checkpoint_assessment(
        predecessor_assessment_bytes, attempt_id=attempt_id
    )
    if predecessor['decision'] != 'CONTINUE' or predecessor['checkpoint'] != 'N1':
        raise ValueError('committed predecessor decision differs')
    predecessor_plan = parse_canonical_json(predecessor_plan_bytes, label='N1 plan')
    predecessor_payload = parse_canonical_json(predecessor_payload_bytes, label='N1 payload')
    if (
        type(predecessor_plan) is not dict
        or predecessor_plan.get('schema') != 'qualification_checkpoint_plan/v2'
        or predecessor_plan.get('checkpoint') != 'N1'
        or type(predecessor_payload) is not dict
        or type(predecessor_payload.get('populations')) is not list
    ):
        raise ValueError('committed predecessor custody differs')
    admission_bytes = canonical_json_bytes(worker['source_admission'])
    admission = parse_source_admission(
        admission_bytes,
        contract_sha256=contract.contract_sha256,
        domain_sha256=contract.trust_domain_sha256,
        policy=policy,
    )
    expected_roles = [
        {'role': item.role, 'sha256': item.sha256}
        for item in sorted(contract.artifacts, key=lambda item: item.role)
    ]
    if (
        admission['retained_roles'] != expected_roles
        or admission['effective_settings_sha256'] != contract.effective_settings_sha256
        or admission['population_sha256']
        != {
            pop: _hash(canonical_json_bytes(list(contract.populations[pop])))
            for pop in ('FULL', 'H1', 'H2')
        }
    ):
        raise ValueError('EVIDENCE_SOURCE_ADMISSION_MISMATCH')
    geometry = geometry_role(contract.trust_domain.runtime_code_roles)
    geometry_digest = next(item.sha256 for item in contract.artifacts if item.role == geometry)
    legality = {
        'schema': 'qualification_legality_result/v1',
        'contract_sha256': contract.contract_sha256,
        'trust_domain_sha256': contract.trust_domain_sha256,
        'policy_sha256': policy.sha256,
        'geometry_source_sha256': geometry_digest,
        'source_admission_sha256': _hash(admission_bytes),
        'check_id': 'PRE_ADMISSION_REGISTRY_EMPTY',
        'status': 'PASS',
    }
    if canonical_json_bytes(worker['legality']) != canonical_json_bytes(legality):
        raise ValueError('EVIDENCE_LEGALITY_MISMATCH')
    for name in ('service_id', 'profile_sha256', 'worker_image_digest'):
        if payload.get(name) != release.get(name):
            raise ValueError('EVIDENCE_RUNTIME_MISMATCH')
    worker_runtime = _hash(canonical_json_bytes(release['runtime_manifests']['worker']))
    if payload.get('runtime_manifest_sha256') != worker_runtime or worker[
        'runtime_load_manifest'
    ] != [
        {'role': role, 'sha256': digest}
        for role, digest in sorted(contract.runtime_load_sha256.items())
    ]:
        raise ValueError('EVIDENCE_RUNTIME_MISMATCH')
    observations = _fields(
        worker['observations'],
        {'worker_compute_wall_ns', 'worker_cpu_ns', 'worker_peak_memory_bytes'},
        label='worker observations',
    )
    for name, value in observations.items():
        if (
            type(value) is not int
            or value < 0
            or payload.get('observations', {}).get(name) != value
        ):
            raise ValueError('EVIDENCE_OBSERVATIONS_MISMATCH')
    if (
        payload['observations'].get('exit_code') != 0
        or payload['observations'].get('oom_killed') is not False
    ):
        raise ValueError('EVIDENCE_ABNORMAL_EXIT')
    if _instant(payload['completed_utc'], label='completed') < _instant(
        payload['started_utc'], label='started'
    ):
        raise ValueError('EVIDENCE_TIME_MISMATCH')
    for name, expected in {
        'attempt_id': attempt_id,
        'contract_sha256': contract.contract_sha256,
        'trust_domain_sha256': contract.trust_domain_sha256,
        'policy_sha256': policy.sha256,
    }.items():
        if snapshot[name] != expected:
            raise ValueError('EVIDENCE_SNAPSHOT_MISMATCH')
    if (
        snapshot['capture']['payload_sha256'] != _hash(worker_result_bytes)
        or snapshot['capture']['result_sha256'] != payload['result_sha256']
        or snapshot['capture']['attestation_sha256'] != _hash(checkpoint_attestation_bytes)
    ):
        raise ValueError('EVIDENCE_SNAPSHOT_MEMBERSHIP_MISMATCH')

    def section(index):
        row = worker['populations'][index]
        return {'population': row['population'], 'outcomes': row['outcomes']}

    def inventory(stage):
        return canonical_json_bytes(
            dict(
                schema='qualification_path_inventory/v1',
                trust_domain_sha256=worker['path_inventory']['trust_domain_sha256'],
                records=[
                    record
                    for record in worker['path_inventory']['records']
                    if record['stage'] == stage
                ],
            )
        )

    prior = {'N1': canonical_json_bytes(predecessor_payload['populations'])}
    n1_bytes = build_stage_artifact(
        contract=contract,
        policy=policy,
        stage='N1',
        input_plan_sha256=_hash(predecessor_plan_bytes),
        outcome_bytes=prior['N1'],
        path_inventory_bytes=canonical_json_bytes(predecessor_payload['path_inventory']),
        prior_stage_outcomes={},
    )
    committed_row = predecessor['stages'][1]
    n1_stage = parse_canonical_json(n1_bytes, label='N1 result')
    if (
        n1_stage['decision'] != committed_row['status']
        or n1_stage['population_counts'] != committed_row['population_counts']
        or _hash(n1_bytes) != committed_row['output_sha256']
        or _hash(predecessor_plan_bytes) != committed_row['input_sha256']
    ):
        raise ValueError('committed N1 evidence differs')
    n2_outcomes = canonical_json_bytes([section(0)])
    n2_bytes = build_stage_artifact(
        contract=contract,
        policy=policy,
        stage='N2',
        input_plan_sha256=_hash(plan_bytes),
        outcome_bytes=n2_outcomes,
        path_inventory_bytes=inventory('N2'),
        prior_stage_outcomes=dict(prior),
    )
    part_b_outcomes = canonical_json_bytes([section(1), section(2)])
    part_b_bytes = build_stage_artifact(
        contract=contract,
        policy=policy,
        stage='PART_B',
        input_plan_sha256=_hash(plan_bytes),
        outcome_bytes=part_b_outcomes,
        path_inventory_bytes=inventory('PART_B'),
        prior_stage_outcomes={**prior, 'N2': n2_outcomes},
    )
    n2_stage = parse_canonical_json(n2_bytes, label='N2 result')
    part_b_stage = parse_canonical_json(part_b_bytes, label='PART_B result')
    decisions = {
        'N2': n2_stage['decision'],
        'PART_B': part_b_stage['decision'],
    }
    failed = any(item == 'FAIL' for item in decisions.values())
    runtime_bytes = canonical_json_bytes(
        {
            'schema': 'qualification_runtime_trace/v2',
            'execution_release_sha256': _hash(installed_release_bytes),
            'profile_sha256': release['profile_sha256'],
            'worker_image_digest': release['worker_image_digest'],
            'runtime_manifest_sha256': worker_runtime,
            'execution_id': worker['execution_id'],
            'execution_attestation_sha256': _hash(checkpoint_attestation_bytes),
            'worker_load_manifest': worker['runtime_load_manifest'],
        }
    )
    outputs = {
        'attempt_journal': checkpoint_snapshot_bytes,
        'legality_result': canonical_json_bytes(legality),
        'n1_result': n1_bytes,
        'n2_result': n2_bytes,
        'part_b_result': part_b_bytes,
        'path_inventory': canonical_json_bytes(worker['path_inventory']),
        'runtime_load_trace': runtime_bytes,
    }
    completion, verdict = ('COMPLETE', 'FAIL') if failed else ('PARTIAL', 'NONE')
    validate_output_roles(
        policy,
        list(outputs),
        stages=('LEGALITY', 'N1', 'N2', 'PART_B'),
        completion=completion,
        verdict=verdict,
    )
    caps = {
        row['stage']: 0 if row['max_failures_per_population'] is None
        else row['max_failures_per_population']
        for row in thresholds
    }
    assessment = {
        'schema': CHECKPOINT_ASSESSMENT_SCHEMA,
        'attempt_id': attempt_id,
        'checkpoint': 'N2',
        'work_id': worker['execution_id'],
        'binding': {
            'contract_sha256': contract.contract_sha256,
            'trust_domain_sha256': contract.trust_domain_sha256,
            'policy_sha256': policy.sha256,
            'execution_release_sha256': _hash(installed_release_bytes),
        },
        'snapshot': {
            'campaign_revision': snapshot['campaign_revision'],
            'authority_head': snapshot['authority_head'],
            'snapshot_sha256': _hash(checkpoint_snapshot_bytes),
        },
        'capture': {
            'result_sha256': payload['result_sha256'],
            'payload_sha256': payload['payload_sha256'],
            'attestation_sha256': _hash(checkpoint_attestation_bytes),
        },
        'stages': [
            {
                'stage': 'LEGALITY',
                'status': 'PASS',
                'input_sha256': _hash(admission_bytes),
                'output_sha256': _hash(outputs['legality_result']),
                'population_counts': {},
            },
            committed_row,
            {
                'stage': 'N2',
                'status': decisions['N2'],
                'input_sha256': _hash(plan_bytes),
                'output_sha256': _hash(n2_bytes),
                'population_counts': n2_stage['population_counts'],
            },
            {
                'stage': 'PART_B',
                'status': decisions['PART_B'],
                'input_sha256': _hash(plan_bytes),
                'output_sha256': _hash(part_b_bytes),
                'population_counts': part_b_stage['population_counts'],
            },
        ],
        'decision': 'FAILURE' if failed else 'CONTINUE',
        'stage_decisions': decisions,
        'cutoff': {'checkpoint': 'N2', 'stage_thresholds': caps},
        'predecessor': {
            'checkpoint': 'N1',
            'assessment_sha256': _hash(predecessor_assessment_bytes),
            'receipt_sha256': _hash(predecessor_receipt_bytes),
        },
        'artifacts': [
            {'role': role, 'sha256': _hash(raw), 'byte_length': len(raw)}
            for role, raw in sorted(outputs.items())
        ],
    }
    return InspectedEvidence(canonical_json_bytes(assessment), MappingProxyType(outputs))


def _inspect_checkpoint_assessment(value):
    """Closed-shape check of one proposed/expected assessment core (no signature)."""
    parsed = parse_canonical_json(value.envelope_bytes, label='checkpoint assessment')
    joint = type(parsed) is dict and parsed.get('checkpoint') == 'N2'
    doc = _fields(
        parsed,
        {
            'schema',
            'attempt_id',
            'checkpoint',
            'work_id',
            'binding',
            'snapshot',
            'capture',
            'stages',
            'decision',
            'n1_decision',
            'cutoff',
            'n2_thresholds',
            'artifacts',
        }
        - ({'n1_decision', 'n2_thresholds'} if joint else set())
        | ({'stage_decisions', 'predecessor'} if joint else set()),
        label='checkpoint assessment',
    )
    if (
        doc['schema'] != 'qualification_campaign_checkpoint_assessment/v1'
        or doc['checkpoint'] not in ('N1', 'N2')
        or type(doc['attempt_id']) is not str
        or not doc['attempt_id']
        or type(doc['work_id']) is not str
        or not doc['work_id']
    ):
        raise ValueError('invalid checkpoint assessment')
    binding = _fields(
        doc['binding'],
        {'contract_sha256', 'trust_domain_sha256', 'policy_sha256', 'execution_release_sha256'},
        label='binding',
    )
    snapshot = _fields(
        doc['snapshot'],
        {'campaign_revision', 'authority_head', 'snapshot_sha256'},
        label='snapshot binding',
    )
    _positive_int(snapshot['campaign_revision'], label='campaign revision')
    capture = _fields(
        doc['capture'],
        {'result_sha256', 'payload_sha256', 'attestation_sha256'},
        label='capture binding',
    )
    for group in (binding, snapshot, capture):
        for key in group:
            if key != 'campaign_revision':
                _sha256(group[key], label=key)
    expected_stages = ['LEGALITY', 'N1', 'N2', 'PART_B'] if joint else ['LEGALITY', 'N1']
    if type(doc['stages']) is not list or [row.get('stage') for row in doc['stages']] != (
        expected_stages
    ):
        raise ValueError('invalid assessment stages')
    for row in doc['stages']:
        _fields(
            row,
            {'stage', 'status', 'input_sha256', 'output_sha256', 'population_counts'},
            label='stage result',
        )
        if row['status'] not in ('PASS', 'FAIL'):
            raise ValueError('invalid stage status')
        _sha256(row['input_sha256'], label='stage input')
        _sha256(row['output_sha256'], label='stage output')
        if type(row['population_counts']) is not dict:
            raise ValueError('invalid population counts')
    if joint:
        decisions = _stage_decisions(doc['stage_decisions'])
        if (
            doc['decision'] not in ('CONTINUE', 'FAILURE')
            or (doc['decision'] == 'CONTINUE')
            != all(item == 'PASS' for item in decisions.values())
            or doc['stages'][0]['status'] != 'PASS'
            or doc['stages'][1]['status'] != 'PASS'
            or doc['stages'][2]['status'] != decisions['N2']
            or doc['stages'][3]['status'] != decisions['PART_B']
        ):
            raise ValueError('invalid assessment decision')
        predecessor = _fields(
            doc['predecessor'],
            {'checkpoint', 'assessment_sha256', 'receipt_sha256'},
            label='joint predecessor',
        )
        if predecessor['checkpoint'] != 'N1':
            raise ValueError('invalid joint predecessor')
        _sha256(predecessor['assessment_sha256'], label='predecessor assessment')
        _sha256(predecessor['receipt_sha256'], label='predecessor receipt')
        cutoff = _fields(doc['cutoff'], {'checkpoint', 'stage_thresholds'}, label='cutoff')
        if cutoff['checkpoint'] != 'N2' or type(cutoff['stage_thresholds']) is not dict:
            raise ValueError('invalid joint cutoff')
        for cap in cutoff['stage_thresholds'].values():
            _positive_int(cap, label='threshold cap', allow_zero=True)
    else:
        failed = doc['n1_decision'] == 'FAIL'
        if (
            doc['n1_decision'] not in ('PASS', 'FAIL')
            or doc['decision'] not in ('CONTINUE', 'FAILURE')
            or (doc['decision'] == 'FAILURE') != failed
            or doc['stages'][1]['status'] != doc['n1_decision']
            or doc['stages'][0]['status'] != 'PASS'
        ):
            raise ValueError('invalid assessment decision')
        cutoff = _fields(doc['cutoff'], {'checkpoint', 'n1_cutoffs'}, label='cutoff')
        if cutoff['checkpoint'] != 'N1' or type(cutoff['n1_cutoffs']) is not dict:
            raise ValueError('invalid N1 cutoff')
        thresholds = _fields(doc['n2_thresholds'], {'bound_to', 'stages'}, label='N2 thresholds')
        _sha256(thresholds['bound_to'], label='threshold binding')
        if type(thresholds['stages']) is not list:
            raise ValueError('invalid N2 thresholds')
        for row in thresholds['stages']:
            _fields(row, {'stage', 'exact_depth', 'max_failures_per_population'}, label='threshold')
            _positive_int(row['exact_depth'], label='depth')
            if row['max_failures_per_population'] is not None:
                _positive_int(
                    row['max_failures_per_population'], label='threshold cap', allow_zero=True
                )
    if type(doc['artifacts']) is not list:
        raise ValueError('invalid artifact inventory')
    for row in doc['artifacts']:
        _fields(row, {'role', 'sha256', 'byte_length'}, label='artifact')
        _sha256(row['sha256'], label='artifact bytes')
        _positive_int(row['byte_length'], label='artifact length')
    if set(value.output_bytes_by_role) != {row['role'] for row in doc['artifacts']}:
        raise ValueError('invalid assessment artifact roles')
    for row in doc['artifacts']:
        raw = value.output_bytes_by_role[row['role']]
        if row['sha256'] != _hash(raw) or row['byte_length'] != len(raw):
            raise ValueError('assessment artifact binding mismatch')
    return doc


def compare_checkpoint_evidence(
    proposed: InspectedEvidence, *, expected: InspectedEvidence
) -> None:
    """Exact byte equality of the assessment cores and staged outputs (D1)."""
    for value in (proposed, expected):
        if (
            type(value) is not InspectedEvidence
            or type(value.envelope_bytes) is not bytes
            or type(value.output_bytes_by_role) not in (dict, MappingProxyType)
            or any(
                type(role) is not str or type(raw) is not bytes
                for role, raw in value.output_bytes_by_role.items()
            )
        ):
            raise ValueError('EVIDENCE_SEMANTIC_MISMATCH')
        try:
            _inspect_checkpoint_assessment(value)
        except (ValueError, KeyError, TypeError) as exc:
            raise ValueError('EVIDENCE_SEMANTIC_MISMATCH') from exc
    if proposed.envelope_bytes != expected.envelope_bytes or dict(
        proposed.output_bytes_by_role
    ) != dict(expected.output_bytes_by_role):
        raise ValueError('EVIDENCE_SEMANTIC_MISMATCH')


CHECKPOINT_RESULT_SCHEMA = 'qualification_campaign_checkpoint_result/v1'
CHECKPOINT_ATTESTATION_SCHEMA = 'qualification_campaign_checkpoint_attestation/v1'
CHECKPOINT_ASSESSMENT_SCHEMA = 'qualification_campaign_checkpoint_assessment/v1'
CHECKPOINT_RECEIPT_SCHEMA = 'qualification_campaign_checkpoint_receipt/v1'
CHECKPOINT_CUTOFF_SCHEMA = 'qualification_campaign_cutoff_receipt/v1'
CHECKPOINT_INTENT_SCHEMA = 'qualification_campaign_checkpoint_intent/v1'


def _stage_row(stage):
    from .execution.protocol import fields

    fields(stage, {'stage', 'status', 'input_sha256', 'output_sha256', 'population_counts'})
    if stage['stage'] not in ('LEGALITY', 'N1', 'N2', 'PART_B') or stage['status'] not in (
        'PASS',
        'FAIL',
    ):
        raise ValueError('checkpoint assessment stage differs')
    if type(stage['population_counts']) is not dict or any(
        type(value) is not int or value < 0 for value in stage['population_counts'].values()
    ):
        raise ValueError('checkpoint assessment population counts differ')
    return stage


def _stage_decisions(value):
    if (
        type(value) is not dict
        or set(value) != {'N2', 'PART_B'}
        or any(item not in ('PASS', 'FAIL') for item in value.values())
    ):
        raise ValueError('joint stage decisions differ')
    return value


def parse_checkpoint_assessment(raw, *, attempt_id):
    from .execution.protocol import fields, identity, digest

    parsed = parse_canonical_json(raw, label='checkpoint assessment')
    joint = type(parsed) is dict and parsed.get('checkpoint') == 'N2'
    doc = fields(
        parsed,
        {
            'schema',
            'attempt_id',
            'checkpoint',
            'work_id',
            'binding',
            'snapshot',
            'capture',
            'stages',
            'decision',
            'n1_decision',
            'cutoff',
            'n2_thresholds',
            'artifacts',
            'signature',
        }
        - ({'n1_decision', 'n2_thresholds'} if joint else set())
        | ({'stage_decisions', 'predecessor'} if joint else set()),
    )
    if (
        doc['schema'] != CHECKPOINT_ASSESSMENT_SCHEMA
        or doc['attempt_id'] != attempt_id
        or doc['checkpoint'] not in ('N1', 'N2')
    ):
        raise ValueError('checkpoint assessment binding differs')
    identity(doc['work_id'])
    binding = fields(
        doc['binding'],
        {'contract_sha256', 'trust_domain_sha256', 'policy_sha256', 'execution_release_sha256'},
    )
    snapshot = fields(doc['snapshot'], {'campaign_revision', 'authority_head', 'snapshot_sha256'})
    from .execution.campaign_budget import integer

    integer(snapshot['campaign_revision'])
    capture = fields(doc['capture'], {'result_sha256', 'payload_sha256', 'attestation_sha256'})
    for group in (binding, snapshot, capture):
        for name, value in group.items():
            if name != 'campaign_revision' and value is not None:
                digest(value)
    if joint:
        if type(doc['stages']) is not list or len(doc['stages']) != 4:
            raise ValueError('LEGALITY/N1/N2/PART_B stage results required')
        [_stage_row(stage) for stage in doc['stages']]
        if [stage['stage'] for stage in doc['stages']] != [
            'LEGALITY',
            'N1',
            'N2',
            'PART_B',
        ]:
            raise ValueError('checkpoint assessment stage order differs')
        decisions = _stage_decisions(doc['stage_decisions'])
        if doc['decision'] not in ('CONTINUE', 'FAILURE') or (
            doc['decision'] == 'CONTINUE'
        ) != all(item == 'PASS' for item in decisions.values()):
            raise ValueError('checkpoint assessment decision differs')
        if (
            doc['stages'][0]['status'] != 'PASS'
            or doc['stages'][1]['status'] != 'PASS'
            or doc['stages'][2]['status'] != decisions['N2']
            or doc['stages'][3]['status'] != decisions['PART_B']
        ):
            raise ValueError('checkpoint assessment stage decisions differ')
        predecessor = fields(
            doc['predecessor'], {'checkpoint', 'assessment_sha256', 'receipt_sha256'}
        )
        if predecessor['checkpoint'] != 'N1':
            raise ValueError('joint predecessor binding required')
        digest(predecessor['assessment_sha256'])
        digest(predecessor['receipt_sha256'])
        cutoff = fields(doc['cutoff'], {'checkpoint', 'stage_thresholds'})
        if cutoff['checkpoint'] != 'N2' or type(cutoff['stage_thresholds']) is not dict:
            raise ValueError('joint cutoff binding required')
        for value in cutoff['stage_thresholds'].values():
            integer(value)
    else:
        if type(doc['stages']) is not list or len(doc['stages']) != 2:
            raise ValueError('LEGALITY and N1 stage results required')
        [_stage_row(stage) for stage in doc['stages']]
        if [stage['stage'] for stage in doc['stages']] != ['LEGALITY', 'N1']:
            raise ValueError('checkpoint assessment stage order differs')
        if doc['decision'] not in ('CONTINUE', 'FAILURE') or doc['n1_decision'] not in (
            'PASS',
            'FAIL',
        ):
            raise ValueError('checkpoint assessment decision differs')
        if (doc['decision'] == 'FAILURE') != (doc['n1_decision'] == 'FAIL'):
            raise ValueError('checkpoint assessment decision consistency differs')
        cutoff = fields(doc['cutoff'], {'checkpoint', 'n1_cutoffs'})
        if cutoff['checkpoint'] != 'N1' or type(cutoff['n1_cutoffs']) is not dict:
            raise ValueError('N1 cutoff binding required')
        for value in cutoff['n1_cutoffs'].values():
            from .execution.campaign_budget import integer as _integer

            _integer(value)
        thresholds = fields(doc['n2_thresholds'], {'bound_to', 'stages'})
        digest(thresholds['bound_to'])
        if type(thresholds['stages']) is not list:
            raise ValueError('distinct N2 threshold binding required')
    if type(doc['artifacts']) is not list:
        raise ValueError('staged artifact inventory required')
    for row in doc['artifacts']:
        fields(row, {'role', 'sha256', 'byte_length'})
        from .execution.protocol import identity as _identity

        _identity(row['role'])
        digest(row['sha256'])
        from .execution.campaign_budget import integer as _integer

        _integer(row['byte_length'], positive=True)
    signature = fields(doc['signature'], {'algorithm', 'key_id', 'value_b64'})
    if signature['algorithm'] != 'Ed25519':
        raise ValueError('canonical signing algorithm required')
    return doc


def parse_checkpoint_cutoff(raw, *, attempt_id):
    from .execution.protocol import fields, digest, identity
    from .execution.campaign_budget import integer, utc

    parsed = parse_canonical_json(raw, label='checkpoint cutoff receipt')
    joint = type(parsed) is dict and parsed.get('checkpoint') == 'N2'
    doc = fields(
        parsed,
        {
            'schema',
            'attempt_id',
            'checkpoint',
            'assessment_sha256',
            'decision',
            'n1_cutoffs',
            'n2_thresholds',
            'n2_bound_to',
            'created_utc',
        }
        - ({'n1_cutoffs', 'n2_thresholds', 'n2_bound_to'} if joint else set())
        | (
            {'stage_decisions', 'stage_thresholds', 'predecessor_receipt_sha256'}
            if joint
            else set()
        ),
    )
    if (
        doc['schema'] != CHECKPOINT_CUTOFF_SCHEMA
        or doc['attempt_id'] != attempt_id
        or doc['checkpoint'] not in ('N1', 'N2')
        or doc['decision'] not in ('CONTINUE', 'FAILURE')
    ):
        raise ValueError('checkpoint cutoff binding differs')
    digest(doc['assessment_sha256'])
    if joint:
        decisions = _stage_decisions(doc['stage_decisions'])
        if (doc['decision'] == 'CONTINUE') != all(
            item == 'PASS' for item in decisions.values()
        ):
            raise ValueError('checkpoint cutoff decision differs')
        if type(doc['stage_thresholds']) is not dict:
            raise ValueError('joint cutoff thresholds required')
        for value in doc['stage_thresholds'].values():
            integer(value)
        digest(doc['predecessor_receipt_sha256'])
    else:
        digest(doc['n2_bound_to'])
        for value in doc['n1_cutoffs'].values():
            integer(value)
        for row in doc['n2_thresholds']:
            fields(row, {'stage', 'exact_depth', 'max_failures_per_population'})
            identity(row['stage'])
            integer(row['exact_depth'], positive=True)
            # A workload may leave an N2/PART_B failure cap unset (None); the
            # binding still pins the stage and its exact depth.
            if row['max_failures_per_population'] is not None:
                integer(row['max_failures_per_population'])
    utc(doc['created_utc'])
    return doc


def parse_checkpoint_attestation(raw, *, attempt_id):
    """The closed campaign checkpoint attestation envelope (custody, not signature).

    The payload binds exactly the archived capture bytes; signature verification
    against enrolled execution keys belongs to the signing/verification owners.
    """
    from .execution.protocol import fields, identity, digest

    doc = fields(
        parse_canonical_json(raw, label='checkpoint attestation'),
        {'schema', 'payload', 'signature'},
    )
    if doc['schema'] != CHECKPOINT_ATTESTATION_SCHEMA:
        raise ValueError('checkpoint attestation schema required')
    payload = fields(
        doc['payload'],
        {
            'schema',
            'scope',
            'attempt_id',
            'checkpoint',
            'work_id',
            'result_sha256',
            'payload_sha256',
            'payload_byte_length',
            'plan_sha256',
            'execution_release_sha256',
            'profile_sha256',
            'service_id',
            'worker_image_digest',
            'runtime_manifest_sha256',
            'container_id',
            'capture',
            'observations',
            'authorized_at_utc',
            'started_utc',
            'completed_utc',
            'campaign_revision',
        },
    )
    if (
        payload['schema'] != 'qualification_campaign_checkpoint_attestation_payload/v1'
        or payload['scope'] != 'ATTEST_CAMPAIGN_CHECKPOINT'
        or payload['attempt_id'] != attempt_id
        or payload['checkpoint'] not in ('N1', 'N2')
    ):
        raise ValueError('checkpoint attestation binding differs')
    import re

    identity(payload['work_id'])
    for name in (
        'result_sha256',
        'payload_sha256',
        'plan_sha256',
        'execution_release_sha256',
        'profile_sha256',
        'runtime_manifest_sha256',
    ):
        digest(payload[name])
    digest(payload['container_id'])
    if (
        type(payload['worker_image_digest']) is not str
        or re.fullmatch('sha256:[0-9a-f]{64}', payload['worker_image_digest']) is None
    ):
        raise ValueError('immutable worker image identity required')
    from .execution.campaign_budget import integer, utc

    integer(payload['payload_byte_length'], positive=True)
    integer(payload['campaign_revision'])
    for name in ('authorized_at_utc', 'started_utc', 'completed_utc'):
        utc(payload[name])
    capture = fields(
        payload['capture'],
        {'exit_code', 'oom_killed', 'campaign_scope_id', 'work_scope_id', 'payload_slice'},
    )
    integer(capture['exit_code'])
    if type(capture['oom_killed']) is not bool:
        raise ValueError('capture exit facts required')
    for name in ('campaign_scope_id', 'work_scope_id', 'payload_slice'):
        identity(capture[name])
    if type(payload['observations']) is not dict:
        raise ValueError('bounded capture observations required')
    signature = fields(doc['signature'], {'algorithm', 'key_id', 'value_b64'})
    if signature['algorithm'] != 'Ed25519':
        raise ValueError('canonical signing algorithm required')
    return doc


def parse_checkpoint_result(raw, *, attempt_id):
    from .execution.protocol import fields, identity, digest

    doc = fields(
        parse_canonical_json(raw, label='checkpoint result'),
        {
            'schema',
            'attempt_id',
            'checkpoint',
            'work_id',
            'campaign_id',
            'plan_sha256',
            'plan_byte_length',
            'payload_sha256',
            'payload_byte_length',
            'worker_execution_id',
            'container_id',
            'worker_image_digest',
            'runtime_manifest_sha256',
            'capture',
            'limits',
            'observations',
            'created_utc',
        },
    )
    if (
        doc['schema'] != CHECKPOINT_RESULT_SCHEMA
        or doc['attempt_id'] != attempt_id
        or doc['checkpoint'] not in ('N1', 'N2')
    ):
        raise ValueError('checkpoint result binding differs')
    import re

    identity(doc['work_id'])
    identity(doc['worker_execution_id'])
    identity(doc['campaign_id'])
    for name in ('plan_sha256', 'payload_sha256', 'runtime_manifest_sha256'):
        digest(doc[name])
    digest(doc['container_id'])
    if (
        type(doc['worker_image_digest']) is not str
        or re.fullmatch('sha256:[0-9a-f]{64}', doc['worker_image_digest']) is None
    ):
        raise ValueError('immutable worker image identity required')
    for name in ('plan_byte_length', 'payload_byte_length'):
        from .execution.campaign_budget import integer

        integer(doc[name], positive=True)
    capture = fields(
        doc['capture'],
        {
            'exit_code',
            'oom_killed',
            'started_utc',
            'completed_utc',
            'authorized_at_utc',
            'campaign_scope_id',
            'work_scope_id',
            'payload_slice',
        },
    )
    from .execution.campaign_budget import integer, utc

    integer(capture['exit_code'])
    utc(capture['completed_utc'])
    utc(capture['authorized_at_utc'])
    if type(capture['oom_killed']) is not bool:
        raise ValueError('capture exit facts required')
    for name in ('campaign_scope_id', 'work_scope_id', 'payload_slice'):
        identity(capture[name])
    limits = fields(doc['limits'], {'cpu_ns', 'wall_ns', 'memory_bytes', 'orchestration_cpu_ns'})
    for value in limits.values():
        from .execution.campaign_budget import integer

        integer(value, positive=True)
    if type(doc['observations']) is not dict:
        raise ValueError('bounded capture observations required')
    from .execution.campaign_budget import utc as _utc

    _utc(doc['created_utc'])
    return doc
