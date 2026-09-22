"""Coherent substitutions must fail even after all dependent hashes change."""

import json
from types import SimpleNamespace
import pytest
from test_orchestration import contract
from c1_rail.qualification.orchestration import _stage_seeds, _part_a_seeds, canonical_bytes
from c1_rail.qualification.seal import _validate_checkpoint_plan_inputs, ResultValidationError
import hashlib


def case(checkpoint):
    c = contract()
    seeds = (
        _part_a_seeds(c, True)
        if checkpoint == 'PART_A'
        else _stage_seeds(c, 'n1' if checkpoint == 'N1' else 'n2', True)
    )
    plan = {
        'schema': 'e1_checkpoint_plan/v1',
        'checkpoint': checkpoint,
        'contract_sha256': c.contract_sha256,
        'trust_domain_sha256': c.trust_domain_sha256,
        'synthetic': True,
        'exact_depth_approval_sha256': 'c' * 64,
        'horizon_sessions': 500,
        'seed_inputs': [json.loads(s.canonical_bytes) for s in seeds],
        'extra': {'initial_panels': 2, 'expanded_panels': 4} if checkpoint == 'PART_A' else None,
    }
    return c, plan


def validate(c, plan):
    # Rehash every path after mutation, reproducing coherent caller evidence.
    records = []
    for row in plan['seed_inputs']:
        if row['purpose'] != 'path':
            continue
        stage = (
            'PART_A'
            if plan['checkpoint'] == 'PART_A'
            else (
                'N1'
                if plan['checkpoint'] == 'N1'
                else 'N2' if row['population'] == 'FULL' else 'PART_B'
            )
        )
        records.append(
            {'stage': stage, 'seed_input_sha256': hashlib.sha256(canonical_bytes(row)).hexdigest()}
        )
    _validate_checkpoint_plan_inputs(
        canonical_bytes(plan),
        checkpoint=plan['checkpoint'],
        contract=c,
        exact_depth_approval_sha256='c' * 64,
        synthetic=True,
        inventory_records=records,
    )


@pytest.mark.parametrize('checkpoint', ['N1', 'N2', 'PART_A'])
@pytest.mark.parametrize(
    'field,value',
    [
        ('root_rng_namespace', 'foreign'),
        ('stage', 'n3'),
        ('population', 'H2'),
        ('panel_index', 13),
        ('path_index', 101),
        ('seed', 0),
        ('source_session_ids_sha256', '0' * 64),
    ],
)
def test_consistently_substituted_seed_is_rejected(checkpoint, field, value):
    c, p = case(checkpoint)
    p['seed_inputs'][0][field] = value
    with pytest.raises(ResultValidationError):
        validate(c, p)


@pytest.mark.parametrize('mutation', ['reverse', 'missing', 'duplicate', 'outer_missing'])
def test_ordered_complete_plan_required(mutation):
    c, p = case('PART_A')
    if mutation == 'reverse':
        p['seed_inputs'].reverse()
    elif mutation == 'missing':
        p['seed_inputs'].pop()
    elif mutation == 'duplicate':
        p['seed_inputs'].append(p['seed_inputs'][-1])
    else:
        p['seed_inputs'] = [r for r in p['seed_inputs'] if r['purpose'] != 'outer']
    with pytest.raises(ResultValidationError):
        validate(c, p)


@pytest.mark.parametrize('checkpoint', ['N1', 'N2', 'PART_A'])
def test_canonical_frozen_plan_accepts(checkpoint):
    validate(*case(checkpoint))


@pytest.mark.parametrize('mutation', ['source', 'identity', 'index', 'missing', 'order'])
def test_part_a_panel_source_binding_required(mutation):
    from c1_rail.qualification.seal import _validate_part_a_panels
    from c1_rail.qualification.orchestration import panel_identity

    c = contract()
    panels = []
    records = []
    for i in range(2):
        ids = list(c.populations['FULL'])
        if mutation == 'source' and i == 0:
            ids[0] = 'foreign-session'
        identity = panel_identity(c, SimpleNamespace(index=i, source_session_ids=tuple(ids)))
        panels.append({'panel_index': i, 'panel_id': identity, 'source_session_ids': ids})
        records.extend(
            {'stage': 'PART_A', 'population': 'REGIME', 'panel_id': identity, 'path_index': j}
            for j in range(2)
        )
    if mutation == 'identity':
        panels[0]['panel_id'] = 'f' * 64
    elif mutation == 'index':
        panels[0]['panel_index'] = 3
    elif mutation == 'missing':
        panels.pop()
    elif mutation == 'order':
        panels.reverse()
    with pytest.raises(ResultValidationError):
        _validate_part_a_panels(c, {'panels': panels}, records)


def test_canonical_seed_vector_preserves_existing_stream():
    c, p = case('N1')
    first = p['seed_inputs'][0]
    assert first['seed'] == 10869960941191221317
    assert (
        first['source_session_ids_sha256']
        == '0473ef2dc0d324ab659d3580c1134e9d812035905c4781fdd6d529b0c6860e13'
    )


@pytest.mark.parametrize('count', [2, 4])
def test_panel_binding_allows_bootstrap_repetitions_and_expansion(count):
    from c1_rail.qualification.seal import _validate_part_a_panels
    from c1_rail.qualification.orchestration import panel_identity

    c = contract()
    panels = []
    records = []
    for i in range(count):
        ids = ['a', 'a']
        identity = panel_identity(c, SimpleNamespace(index=i, source_session_ids=tuple(ids)))
        panels.append({'panel_index': i, 'panel_id': identity, 'source_session_ids': ids})
        records.extend(
            {'stage': 'PART_A', 'population': 'REGIME', 'panel_id': identity, 'path_index': j}
            for j in range(2)
        )
    _validate_part_a_panels(c, {'panels': panels}, records)


def _sha256_hex(raw):
    import hashlib

    return hashlib.sha256(raw).hexdigest()


# ---- S3: the FULL_E1 checkpoint family's closed validation surface ----------


def test_checkpoint_plan_is_the_retained_n1_subdocument(tmp_path):
    """Prep Q9: derive_checkpoint_plan returns exactly derive_n1_plan's bytes."""
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent / 'execution'))
    from bundle_fixture import build_bundle
    from c1_rail.qualification.contract import canonical_json_bytes as encoded
    from c1_rail.qualification.checkpoint_plan import (
        derive_campaign_plan,
        derive_checkpoint_plan,
        derive_n1_plan,
    )
    from c1_rail.qualification.execution.admission import verify_bundle
    from test_contract import NOW

    case = build_bundle(tmp_path / 'staged', capability='FULL_E1', dispatch=True)
    context = verify_bundle(case['root'], case['release'], case['keys'], NOW)
    plan = derive_campaign_plan(
        context.contract,
        policy=context.policy,
        execution_release_sha256=context.domain.execution_release_sha256,
        source_bundle_sha256=_sha256_hex(case['index']),
        attempt_id=context.attempt_id,
        exact_depth_approval_sha256=context.exact_depth_approval.approval_sha256,
    )
    sliced = derive_checkpoint_plan(plan, 'N1', None)
    direct = derive_n1_plan(
        context.contract,
        policy=context.policy,
        execution_release_sha256=context.domain.execution_release_sha256,
        attempt_id=context.attempt_id,
        exact_depth_approval_sha256=context.exact_depth_approval.approval_sha256,
    )
    assert sliced == direct
    with pytest.raises(ValueError, match='no predecessor receipt'):
        derive_checkpoint_plan(plan, 'N1', b'receipt')
    with pytest.raises(ValueError, match='unsupported checkpoint selection'):
        derive_checkpoint_plan(plan, 'N2', None)
    with pytest.raises(ValueError, match='retained canonical campaign plan'):
        derive_checkpoint_plan(encoded({'schema': 'other'}), 'N1', None)


def test_checkpoint_operations_are_g5_only_with_closed_fields():
    from c1_rail.qualification.contract import canonical_json_bytes as encoded
    from c1_rail.qualification.execution import campaign_protocol as protocol

    for operation in protocol.CHECKPOINT_OPERATIONS:
        assert protocol.permitted('g5', operation)
        assert not protocol.permitted('client', operation)
        assert not protocol.permitted('operator', operation)
    base = {'schema': 'qualification_campaign_request/v2', 'attempt_id': 'a1', 'checkpoint': 'N2'}
    with pytest.raises(ValueError, match='installed checkpoint required'):
        protocol.parse_campaign_request(encoded(dict(base, operation='CHECKPOINT_SNAPSHOT')))
    bad = dict(
        base,
        checkpoint='N1',
        operation='FETCH_CHECKPOINT_MEMBER',
        object_sha256='0' * 64,
        offset=-1,
        length=16,
    )
    with pytest.raises(ValueError, match='bounded integer chunk offset'):
        protocol.parse_campaign_request(encoded(bad))
    bad = dict(
        base, checkpoint='N1', operation='STAGE_CHECKPOINT_ARTIFACT', role='r1', bytes_b64=''
    )
    with pytest.raises(ValueError, match='bounded staged checkpoint artifact'):
        protocol.parse_campaign_request(encoded(bad))
    bad = dict(
        base,
        checkpoint='N1',
        operation='COMMIT_CHECKPOINT_ASSESSMENT',
        work_id='w1',
        candidate_bytes_b64='e30=',
        artifacts=[{'role': 'r'}],
    )
    with pytest.raises(ValueError, match='closed staged artifact inventory'):
        protocol.parse_campaign_request(encoded(bad))


def test_v1_builder_refuses_the_full_e1_family():
    """The N1_ONLY builder keeps refusing the campaign family (fail-on-base
    guard: this refusal already holds on the S2 base and must keep holding)."""
    from c1_rail.qualification.evidence import build_n1_evidence

    with pytest.raises(ValueError):
        build_n1_evidence(
            contract=None,
            policy=None,
            worker_result_bytes=b'{}',
            plan_bytes=b'{}',
            execution_attestation_bytes=b'{}',
            journal_snapshot_bytes=b'{}',
            installed_release_bytes=b'{}',
        )


def test_checkpoint_snapshot_parser_refuses_open_shapes():
    from c1_rail.qualification.journal_snapshot import (
        encode_campaign_checkpoint_snapshot,
        parse_campaign_checkpoint_snapshot,
    )
    from c1_rail.qualification.contract import canonical_json_bytes as encoded

    good = {
        'attempt_id': 'a1',
        'checkpoint': 'N1',
        'contract_sha256': '1' * 64,
        'trust_domain_sha256': '2' * 64,
        'policy_sha256': '3' * 64,
        'validity': 'VALID',
        'campaign_revision': 4,
        'authority_head': '4' * 64,
        'event_head': '5' * 64,
        'campaign_state': 'BOUND',
        'works': [
            {'work_id': 'admission', 'phase': 'ADMISSION', 'state': 'COMPLETED', 'settled': True}
        ],
        'capture': {
            'work_id': 'n1work',
            'result_sha256': '6' * 64,
            'payload_sha256': '7' * 64,
            'attestation_sha256': '8' * 64,
        },
        'intent': {'work_id': 'g5work', 'candidate_sha256': None},
        'members': [
            {'role': 'plan', 'sha256': '9' * 64, 'byte_length': 10},
            {'role': 'result', 'sha256': 'a' * 64, 'byte_length': 10},
            {'role': 'payload', 'sha256': 'b' * 64, 'byte_length': 10},
            {'role': 'attestation', 'sha256': 'c' * 64, 'byte_length': 10},
            {'role': 'retained_bundle_index', 'sha256': 'd' * 64, 'byte_length': 10},
        ],
    }
    raw = encode_campaign_checkpoint_snapshot(**good)
    assert parse_campaign_checkpoint_snapshot(raw)['checkpoint'] == 'N1'
    import json

    doc = json.loads(raw)
    for mutation, pattern in (
        ({'checkpoint': 'N2'}, 'schema required'),
        ({'campaign_state': 'N3_READY'}, 'state differs'),
        ({'validity': 'MAYBE'}, 'state differs'),
        ({'members': doc['members'][:4]}, 'incomplete'),
    ):
        broken = dict(doc)
        broken.update(mutation)
        with pytest.raises(ValueError, match=pattern):
            parse_campaign_checkpoint_snapshot(encoded(broken))
