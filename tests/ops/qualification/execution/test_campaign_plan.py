"""FULL_E1 plans describe frozen inputs; they confer no execution authority."""
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest
from c1_rail.qualification import checkpoint_plan as pure
from c1_rail.qualification.execution import plan as adapter
from c1_rail.qualification.contract import canonical_json_bytes as encoded


from bundle_fixture import build_bundle
from test_contract import NOW
from c1_rail.qualification.contract import parse_canonical_json
from c1_rail.qualification.execution.admission import verify_bundle


def test_verified_context_yields_stable_non_authoritative_campaign_plan(tmp_path):
    from c1_rail.qualification.execution.plan import derive_campaign_plan_from_context

    case = build_bundle(tmp_path / 'bundle')
    context = verify_bundle(case['root'], case['release'], case['keys'], NOW)
    first = derive_campaign_plan_from_context(context)
    assert first == derive_campaign_plan_from_context(context)
    doc = parse_canonical_json(first, label='campaign plan')
    assert doc['schema'] == 'qualification_campaign_plan/v1'
    assert doc['purpose'] == 'PLANNING_ONLY'
    assert doc['target_capability'] == 'FULL_E1'
    assert doc['authorizes_dispatch'] is False
    assert doc['authority_class'] == 'TEST_ONLY'
    assert doc['attempt_id'] == context.attempt_id
    assert doc['execution_release_sha256'] == context.release.sha256

@pytest.fixture(scope='module')
def verified(tmp_path_factory):
    case = build_bundle(tmp_path_factory.mktemp('campaign') / 'bundle', root_rng_namespace='test')
    return case, verify_bundle(case['root'], case['release'], case['keys'], NOW)


def bindings(context):
    return dict(contract=context.contract, policy=context.policy,
        execution_release_sha256=context.release.sha256,
        source_bundle_sha256=context.bundle_sha256, attempt_id=context.attempt_id,
        exact_depth_approval_sha256=context.exact_depth_approval.approval_sha256)


def document(context):
    return json.loads(adapter.derive_campaign_plan_from_context(context))


def test_reconstructed_context_and_validating_consumer_agree(verified):
    case, context = verified
    reconstructed = verify_bundle(case['root'], case['release'], case['keys'], NOW)
    raw = adapter.derive_campaign_plan_from_context(context)
    assert raw == adapter.derive_campaign_plan_from_context(reconstructed)
    assert pure.validate_campaign_plan(raw, **bindings(reconstructed)) == json.loads(raw)
    doc = json.loads(raw)
    original = json.loads(context.contract.canonical_bytes)
    assert doc['source_bundle_sha256'] == context.bundle_sha256
    assert doc['budget'] == original['replay']['budget']
    for name in ('initial_state', 'replay'):
        assert doc[name + '_sha256'] == hashlib.sha256(encoded(original[name])).hexdigest()
    assert doc['budget_sha256'] == hashlib.sha256(encoded(doc['budget'])).hexdigest()


def test_n1_reused_and_n2_is_one_ordered_joint_inventory(verified):
    _, context = verified
    doc = document(context)
    assert doc['checkpoint_groups'] == [
        {'checkpoint': 'N1', 'stages': ['N1']},
        {'checkpoint': 'N2', 'stages': ['N2', 'PART_B']},
        {'checkpoint': 'PART_A', 'stages': ['PART_A']}]
    kw = bindings(context)
    del kw['source_bundle_sha256']
    contract = kw.pop('contract')
    assert encoded(doc['n1']) == pure.derive_n1_plan(contract, **kw)
    assert doc['n2']['depths'] == [
        {'population': 'FULL', 'depth': 60, 'statistics_stage': 'N2'},
        {'population': 'H1', 'depth': 60, 'statistics_stage': 'PART_B'},
        {'population': 'H2', 'depth': 60, 'statistics_stage': 'PART_B'}]
    seeds = doc['n2']['seed_inputs']
    assert [(row['population'], row['path_index']) for row in seeds] == [
        (pop, index) for pop in ('FULL', 'H1', 'H2') for index in range(60)]
    assert all(row['stage'] == 'n2' and row['panel_index'] is None for row in seeds)
    assert doc['cutoff']['checkpoint'] == 'CUTOFF'
    assert doc['cutoff']['stages'] == []
    assert doc['cutoff']['seed_inputs'] == []
    assert [row['stage'] for row in doc['cutoff']['thresholds']] == ['N2', 'PART_B']
    assert doc['probes'][0]['seed_inputs'] == doc['probes'][1]['seed_inputs']
    assert doc['probes'][0]['seed_inputs'] == [doc['n1']['probe']]


def test_part_a_prefix_appended_boundaries_and_independent_seed_vectors(verified):
    _, context = verified
    doc = document(context)
    part = doc['part_a']
    assert part['parameters'] == json.loads(context.contract.canonical_bytes)['replay']['part_a']
    assert part['initial_panel_range'] == [0, 2]
    assert part['potential_appended_panel_range'] == [2, 4]
    assert [row['panel_index'] for row in part['potential_panels']] == [0, 1, 2, 3]
    vectors = json.loads((Path(__file__).parent / 'fixtures/seed_consumer_vectors.json').read_bytes())
    selected = [v for v in vectors if v['root'] == 'test' and v['synthetic']]
    inventory = [s for panel in part['potential_panels'] for s in [panel['outer_seed'], *panel['path_seeds']]]
    inventory += [s for probe in doc['probes'] for s in probe['seed_inputs']]
    for seed in inventory:
        vector = next(v for v in selected if all(v[k] == seed[k] for k in
            ('stage', 'population', 'panel_index', 'path_index', 'purpose')))
        assert seed['seed'] == vector['seed']
    # Literal boundary vectors include first/last initial and appended panels.
    assert [p['path_seeds'][-1]['seed'] for p in part['potential_panels']] == [
        17349676559805575382, 12738108447318337774,
        4705594781841923981, 7590384410364307358]
    assert len({s['seed'] for s in inventory}) == len(inventory) - 1  # N1/N2 probe repeats.
    assert [p['checkpoint'] for p in doc['probes']] == ['N1', 'N2', 'PART_A']


@pytest.mark.parametrize('edit', [
    'unknown', 'seed', 'missing', 'extra', 'seed_order', 'population_order', 'depth_bool',
    'budget_rehashed', 'digest', 'probe', 'panel_order', 'outer', 'prefix', 'authority', 'dispatch',
])
def test_caller_declarations_cannot_override_frozen_plan(verified, edit):
    _, context = verified
    doc = document(context)
    seeds = doc['n2']['seed_inputs']
    if edit == 'unknown': doc['outcomes'] = []
    elif edit == 'seed': seeds[0]['seed'] += 1
    elif edit == 'missing': seeds.pop()
    elif edit == 'extra': seeds.append(seeds[-1])
    elif edit == 'seed_order': seeds.reverse()
    elif edit == 'population_order': doc['n2']['depths'].reverse()
    elif edit == 'depth_bool': doc['n2']['depths'][0]['depth'] = True
    elif edit == 'budget_rehashed':
        doc['budget']['maximum_cpu_seconds'] += 1
        doc['budget_sha256'] = hashlib.sha256(encoded(doc['budget'])).hexdigest()
    elif edit == 'digest': doc['contract_sha256'] = '0' * 64
    elif edit == 'probe': doc['probes'][1]['seed_inputs'] = []
    elif edit == 'panel_order': doc['part_a']['potential_panels'].reverse()
    elif edit == 'outer': doc['part_a']['potential_panels'][0]['outer_seed']['purpose'] = 'path'
    elif edit == 'prefix': doc['part_a']['initial_panel_range'] = [0, 3]
    elif edit == 'authority': doc['authority_class'] = 'OPERATOR'
    elif edit == 'dispatch': doc['authorizes_dispatch'] = True
    with pytest.raises(ValueError):
        pure.validate_campaign_plan(encoded(doc), **bindings(context))


@pytest.mark.parametrize('raw', [b' {}', b'{}\n', b'[]', b'null', b'{"x":1,"x":1}', 'not bytes', None])
def test_malformed_noncanonical_and_wrong_type_rejected(verified, raw):
    with pytest.raises(ValueError):
        pure.validate_campaign_plan(raw, **bindings(verified[1]))


@pytest.mark.parametrize('field', ['execution_release_sha256', 'source_bundle_sha256',
                                  'exact_depth_approval_sha256', 'attempt_id'])
def test_valid_but_different_binding_cannot_validate_original(verified, field):
    context = verified[1]
    raw = adapter.derive_campaign_plan_from_context(context)
    kw = bindings(context)
    kw[field] = 'another-attempt' if field == 'attempt_id' else '0' * 64
    with pytest.raises(ValueError):
        pure.validate_campaign_plan(raw, **kw)
    kw[field] = False if field == 'attempt_id' else 'BAD'
    with pytest.raises(ValueError):
        pure.derive_campaign_plan(**kw)


def test_context_cross_binding_rejected(verified, tmp_path):
    original = verified[1]
    case = build_bundle(tmp_path / 'other', attempt_id='another-valid-attempt')
    other = verify_bundle(case['root'], case['release'], case['keys'], NOW)
    assert adapter.derive_campaign_plan_from_context(original) != adapter.derive_campaign_plan_from_context(other)
    for field in ('contract', 'domain', 'release', 'retained_bundle_index', 'retained_bytes',
                  'attempt_id', 'exact_depth_approval'):
        with pytest.raises(ValueError):
            adapter.derive_campaign_plan_from_context(replace(original, **{field: getattr(other, field)}))
    with pytest.raises(ValueError):
        pure.validate_campaign_plan(adapter.derive_campaign_plan_from_context(original), **bindings(other))


def test_operator_and_execution_authority_remain_closed(verified):
    from c1_rail.qualification.execution.admission import ExecutionRelease
    from c1_rail.qualification.execution.release_schema import parse_release
    from c1_rail.qualification.execution.protocol import parse_request
    from c1_rail.qualification.preflight import validate_e1_preflight
    context = verified[1]
    release = context.release.document
    release['authority_class'] = 'OPERATOR'
    with pytest.raises(ValueError, match='TEST_ONLY'):
        adapter.derive_campaign_plan_from_context(replace(context, release=ExecutionRelease(encoded(release))))
    release['authority_class'] = 'TEST_ONLY'
    release['capability'] = 'FULL_E1'
    with pytest.raises(ValueError): parse_release(encoded(release))
    with pytest.raises(ValueError, match='UNKNOWN_OPERATION'):
        parse_request(encoded(dict(operation='SUBMIT_E1', attempt_id=context.attempt_id,
                                  bundle_sha256=context.bundle_sha256)))
    with pytest.raises(ValueError, match='SERVICE_OWNED_PREFLIGHT_REQUIRED'):
        validate_e1_preflight(context.contract, attempt_id=context.attempt_id, output_root=Path('unused'),
            exact_depth_approval_bytes=b'', trusted_keys={}, now=NOW, trust_domain=context.domain)


def test_invalid_workload_counts_rejected_by_canonical_validator(verified):
    workload = verified[1].domain.workload_policy
    with pytest.raises(ValueError, match='expanded panels must exceed'):
        replace(workload, part_a_expanded_panels=workload.part_a_initial_panels)
    counts = {stage: dict(pops) for stage, pops in workload.stage_population_depths.items()}
    counts['PART_A']['REGIME'] = (2, 2)
    with pytest.raises(ValueError, match='sorted unique'):
        replace(workload, stage_population_depths=counts, part_a_expanded_panels=2)
    counts['PART_A']['REGIME'] = (2, 4)
    counts['N2']['FULL'] = (True,)
    with pytest.raises(ValueError): replace(workload, stage_population_depths=counts)


def test_planning_does_not_replay_sample_launch_mutate_or_sign(verified, monkeypatch):
    import builtins
    import sqlite3
    import subprocess
    from c1_rail.qualification import regime, runner, part_a, replay
    from c1_rail.qualification.execution import launcher, store
    from c1_rail.qualification.production_source import ProductionSource
    from c1_rail.qualification.paths import PathAssembler
    def prohibited(*args, **kwargs):
        raise AssertionError('planning invoked an execution side effect')
    for module, names in ((regime, ('sample_outer_panel', 'rebuild_inner_blocks')),
                          (runner, ('_run_stage',)), (part_a, ('_run_part_a',)),
                          (launcher, ('create_worker',)), (subprocess, ('Popen',)),
                          (sqlite3, ('connect',)), (store.ExecutionStore, ('reserve',)),
                          (type(verified[0]['private']['test-freeze']), ('sign',)),
                          (ProductionSource, ('replay', 'verify_for')),
                          (replay.BookReplay, ('run',)), (PathAssembler, ('sample',))):
        for name in names: monkeypatch.setattr(module, name, prohibited)
    monkeypatch.setattr(builtins, 'open', prohibited)
    assert pure.validate_campaign_plan(adapter.derive_campaign_plan_from_context(verified[1]),
                                      **bindings(verified[1]))['authorizes_dispatch'] is False


@pytest.mark.parametrize('edit', ['source', 'path', 'extra', 'freeze'])
def test_coherently_rehashed_retained_source_cannot_borrow_frozen_contract(verified, edit):
    context = verified[1]
    retained = dict(context.retained_bytes)
    index = json.loads(context.retained_bundle_index)
    role = 'freeze_approval' if edit == 'freeze' else 'orb_runtime_port'
    retained[role] += b'\n# edited source\n'
    row = next(row for row in index['entries'] if row['role'] == role)
    row.update(sha256=hashlib.sha256(retained[role]).hexdigest(), byte_length=len(retained[role]))
    if edit == 'path':
        retained = dict(context.retained_bytes)
        index = json.loads(context.retained_bundle_index)
        next(row for row in index['entries'] if row['role'] == role)['path'] = 'another/source.py'
    elif edit == 'extra':
        retained = dict(context.retained_bytes, extra=b'{}')
        index = json.loads(context.retained_bundle_index)
        index['entries'].append(dict(role='extra', path='extra.json',
                                     sha256=hashlib.sha256(b'{}').hexdigest(), byte_length=2))
        index['entries'].sort(key=lambda row: row['role'])
    mixed = replace(context, retained_bytes=retained, retained_bundle_index=encoded(index))
    with pytest.raises(ValueError, match='artifact.*binding|freeze approval binding'):
        adapter.derive_campaign_plan_from_context(mixed)


def test_huge_signed_workload_rejected_before_any_seed_materialization(verified, tmp_path, monkeypatch):
    workload = replace(verified[1].domain.workload_policy, part_a_paths_per_population_per_panel=10**12)
    case = build_bundle(tmp_path / 'huge', workload=workload)
    context = verify_bundle(case['root'], case['release'], case['keys'], NOW)
    def forbidden(*args, **kwargs):
        raise AssertionError('oversized plan started allocating seeds')
    monkeypatch.setattr(pure, 'seed_input', forbidden)
    with pytest.raises(ValueError, match='representation limit'):
        pure.derive_campaign_plan(**bindings(context))
    with pytest.raises(ValueError, match='memory screen'):
        adapter.derive_campaign_plan_from_context(context)


def test_reference_depths_fit_explicit_plan_representation(verified, tmp_path):
    workload = verified[1].domain.workload_policy
    counts = {stage: dict(pops) for stage, pops in workload.stage_population_depths.items()}
    counts.update(N1={pop: (200,) for pop in ('FULL', 'H1', 'H2')}, N2={'FULL': (970,)},
                  PART_B={pop: (970,) for pop in ('H1', 'H2')}, PART_A={'REGIME': (100, 200)})
    workload = replace(workload, stage_population_depths=counts, part_a_initial_panels=100,
                       part_a_expanded_panels=200, part_a_paths_per_population_per_panel=200)
    case = build_bundle(tmp_path / 'reference-depths', workload=workload)
    context = verify_bundle(case['root'], case['release'], case['keys'], NOW)
    raw = adapter.derive_campaign_plan_from_context(context)
    assert len(raw) < context.profile.input_byte_limit
    doc = pure.validate_campaign_plan(raw, **bindings(context))
    assert len(doc['n1']['seed_inputs']) == 600
    assert len(doc['n2']['seed_inputs']) == 2910
    assert len(doc['part_a']['potential_panels']) == 200
    assert sum(len(panel['path_seeds']) for panel in doc['part_a']['potential_panels']) == 40000
    print('Reference-depth plan bytes:', len(raw))


def test_different_valid_approval_and_bundle_identity_reject_original_plan(verified, tmp_path):
    from composition_fixture import signed_approval
    from c1_rail.qualification.preflight import exact_depth_subject
    case = build_bundle(tmp_path / 'approval')
    context = verify_bundle(case['root'], case['release'], case['keys'], NOW)
    original = adapter.derive_campaign_plan_from_context(context)
    # A fresh valid attempt gets a matching real approval and retained index.
    attempt = 'second-approved-attempt'
    approval = signed_approval(exact_depth_subject(context.contract, attempt_id=attempt),
        case['private']['test-freeze'], key_id='test-freeze', scope='APPROVE_E1_EXACT_DEPTH',
        contract_sha256=context.contract.contract_sha256)
    (case['root'] / case['paths']['exact_depth_approval']).write_bytes(approval)
    index = json.loads(case['index'])
    index['attempt_id'] = attempt
    row = next(row for row in index['entries'] if row['role'] == 'exact_depth_approval')
    row.update(sha256=hashlib.sha256(approval).hexdigest(), byte_length=len(approval))
    (case['root'] / 'index.json').write_bytes(encoded(index))
    other = verify_bundle(case['root'], case['release'], case['keys'], NOW)
    assert other.contract.canonical_bytes == context.contract.canonical_bytes
    assert other.release.sha256 == context.release.sha256
    assert other.exact_depth_approval.approval_sha256 != context.exact_depth_approval.approval_sha256
    assert other.bundle_sha256 != context.bundle_sha256
    with pytest.raises(ValueError): pure.validate_campaign_plan(original, **bindings(other))
