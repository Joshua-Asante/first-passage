"""All launcher consumers use one validated resolved isolation profile."""
import importlib
import json
from pathlib import Path
from c1_rail.qualification.contract import canonical_json_bytes
import pytest


def profile_module():
    return importlib.import_module('c1_rail.qualification.execution.profile')


def document():
    return json.loads((Path(__file__).resolve().parents[4]/'deploy/qualification/test-profile.json').read_bytes())


@pytest.mark.parametrize('field,value', [
    ('production_execution', True), ('supported_checkpoints', ['N1', 'N2']),
    ('worker_uid', 0), ('network', 'host'), ('read_only', False),
    ('capabilities', ['SYS_ADMIN']), ('privileged', True), ('pid_mode', 'host'),
    ('ipc_mode', 'host'), ('no_new_privileges', False), ('restart', 'always'),
    ('output_byte_limit', True), ('admission_seconds', 0), ('command', ['sh'])])
def test_profile_rejects_runtime_escape_and_unsupported_activation(field, value):
    doc = document()
    doc[field] = value
    with pytest.raises(ValueError):
        profile_module().parse_profile(canonical_json_bytes(doc))


def test_profile_retains_canonical_identity_for_launch_and_inspection():
    raw = canonical_json_bytes(document())
    profile = profile_module().parse_profile(raw)
    assert profile.canonical_bytes == raw
    assert profile.worker_uid == 65532
    assert profile.supported_checkpoints == ('N1',)


# ---- S3 v5 profile vectors (C1 GO condition b; extended, never replaced) -----

def dispatch_profile_document():
    """The resolved diagnostic v5 profile from the same deployment limits."""
    import importlib
    module = importlib.import_module('c1_rail.qualification.execution.profile')
    return module.dispatch_diagnostic_execution_profile(canonical_json_bytes(document()))


def test_dispatch_profile_enables_exactly_n1(tmp_path):
    import importlib
    module = importlib.import_module('c1_rail.qualification.execution.profile')
    doc = dispatch_profile_document()
    profile = module.parse_profile(canonical_json_bytes(doc))
    assert profile.values['schema'] == 'qualification_execution_profile/v5'
    assert profile.supported_checkpoints == ('N1',) and profile.dispatch_checkpoints == ('N1',)
    assert profile.dispatch_enabled is True and profile.capability == 'FULL_E1'
    assert profile.production_execution is False


@pytest.mark.parametrize('field,value', [
    ('dispatch_enabled', False), ('dispatch_checkpoints', []), ('dispatch_checkpoints', ['N1', 'N2']),
    ('supported_checkpoints', ['N1', 'N2']), ('supported_checkpoints', []),
    ('production_execution', True), ('capability', 'N1_ONLY')])
def test_dispatch_profile_refuses_open_dispatch_facts(field, value):
    import importlib
    module = importlib.import_module('c1_rail.qualification.execution.profile')
    doc = dispatch_profile_document()
    doc[field] = value
    with pytest.raises(ValueError):
        module.parse_profile(canonical_json_bytes(doc))


def test_v4_profile_with_dispatch_enabled_is_still_refused():
    import importlib
    module = importlib.import_module('c1_rail.qualification.execution.profile')
    doc = dispatch_profile_document()
    doc.update(schema='qualification_execution_profile/v4', protocol_version=4)
    doc.pop('dispatch_checkpoints')
    with pytest.raises(ValueError):
        module.parse_profile(canonical_json_bytes(doc))
    doc.update(dispatch_enabled=False, supported_checkpoints=[])
    module.parse_profile(canonical_json_bytes(doc))


# ---- S4 v6 joint vectors (D3; beside the v5 pins, never replacing them) ------


def test_joint_dispatch_profile_enables_exactly_n1_n2():
    import importlib
    module = importlib.import_module('c1_rail.qualification.execution.profile')
    doc = module.joint_dispatch_diagnostic_execution_profile(canonical_json_bytes(document()))
    profile = module.parse_profile(canonical_json_bytes(doc))
    assert profile.values['schema'] == 'qualification_execution_profile/v6'
    assert profile.supported_checkpoints == ('N1', 'N2')
    assert profile.dispatch_checkpoints == ('N1', 'N2')
    assert profile.dispatch_enabled is True and profile.capability == 'FULL_E1'
    assert profile.production_execution is False


@pytest.mark.parametrize('field,value', [
    ('dispatch_enabled', False), ('dispatch_checkpoints', ['N1']),
    ('dispatch_checkpoints', ['N1', 'N2', 'PART_A']), ('supported_checkpoints', ['N1']),
    ('supported_checkpoints', ['N1', 'N2', 'PART_A'])])
def test_joint_dispatch_profile_refuses_open_dispatch_facts(field, value):
    import importlib
    module = importlib.import_module('c1_rail.qualification.execution.profile')
    doc = module.joint_dispatch_diagnostic_execution_profile(canonical_json_bytes(document()))
    doc[field] = value
    with pytest.raises(ValueError):
        module.parse_profile(canonical_json_bytes(doc))


def test_v5_profile_with_the_joint_set_is_still_refused():
    import importlib
    module = importlib.import_module('c1_rail.qualification.execution.profile')
    doc = module.joint_dispatch_diagnostic_execution_profile(canonical_json_bytes(document()))
    doc.update(schema='qualification_execution_profile/v5', protocol_version=5)
    with pytest.raises(ValueError):
        module.parse_profile(canonical_json_bytes(doc))


def test_joint_v6_budget_profile_widens_only_the_n2_compute_phase():
    """S4-R5b: the operator-ruled N2 ceiling (360 s CPU / 900 s wall) lives in
    the TEST_ONLY v6 diagnostic budget profile alone; v5 and every other phase
    keep the shared 120 s / 300 s diagnostic ceiling and controller charge."""
    import importlib

    module = importlib.import_module('c1_rail.qualification.execution.profile')
    v6 = module.joint_dispatch_diagnostic_execution_profile(canonical_json_bytes(document()))
    v5 = dispatch_profile_document()
    memory = v6['memory_bytes']
    assert v5['memory_bytes'] == memory
    joint = module.diagnostic_budget_profile(canonical_json_bytes(v6))
    dispatched = module.diagnostic_budget_profile(canonical_json_bytes(v5))
    shared = dict(cpu_ns=120_000_000_000, wall_ns=300_000_000_000, memory_bytes=memory)
    assert joint['phases']['N2'] == dict(
        cpu_ns=360_000_000_000, wall_ns=900_000_000_000, memory_bytes=memory
    )
    for phase, limits in joint['phases'].items():
        if phase != 'N2':
            assert limits == shared, phase
    for phase, limits in dispatched['phases'].items():
        assert limits == shared, phase
    assert joint['orchestration_cpu_ns'] == dispatched['orchestration_cpu_ns']
    assert set(joint['orchestration_cpu_ns'].values()) == {20_000_000_000}

# ---- S5 v7 part-a vectors (S5-D3; beside the v6 pins, never replacing them) --


def part_a_dispatch_profile_document():
    """The resolved diagnostic v7 profile from the same deployment limits."""
    return profile_module().part_a_dispatch_diagnostic_execution_profile(
        canonical_json_bytes(document())
    )


def test_part_a_dispatch_profile_enables_exactly_n1_n2_part_a():
    module = profile_module()
    doc = part_a_dispatch_profile_document()
    profile = module.parse_profile(canonical_json_bytes(doc))
    assert profile.values['schema'] == 'qualification_execution_profile/v7'
    assert profile.protocol_version == 7
    assert profile.supported_checkpoints == ('N1', 'N2', 'PART_A')
    assert profile.dispatch_checkpoints == ('N1', 'N2', 'PART_A')
    assert profile.dispatch_enabled is True and profile.capability == 'FULL_E1'
    assert profile.production_execution is False


@pytest.mark.parametrize('field,value', [
    ('dispatch_enabled', False), ('dispatch_checkpoints', ['N1', 'N2']),
    ('dispatch_checkpoints', ['N1', 'N2', 'PART_A', 'N3']), ('dispatch_checkpoints', []),
    ('supported_checkpoints', ['N1', 'N2']), ('supported_checkpoints', ['N1', 'N2', 'PART_A', 'N3'])])
def test_part_a_dispatch_profile_refuses_open_dispatch_facts(field, value):
    module = profile_module()
    doc = part_a_dispatch_profile_document()
    doc[field] = value
    with pytest.raises(ValueError):
        module.parse_profile(canonical_json_bytes(doc))


def test_v6_profile_with_the_part_a_set_is_still_refused():
    module = profile_module()
    doc = part_a_dispatch_profile_document()
    doc.update(schema='qualification_execution_profile/v6', protocol_version=6)
    with pytest.raises(ValueError):
        module.parse_profile(canonical_json_bytes(doc))


@pytest.mark.parametrize('key,value', [
    ('measurement_override', dict(within_pp=1.0)), ('within_pp', 1.0)])
def test_part_a_v7_profile_key_set_stays_closed_to_measurement_keys(key, value):
    """P-4: the /v7 profile's closed key set admits no measurement seam."""
    module = profile_module()
    doc = part_a_dispatch_profile_document()
    doc[key] = value
    with pytest.raises(ValueError):
        module.parse_profile(canonical_json_bytes(doc))


def test_part_a_v7_budget_profile_widens_only_the_n2_compute_phase():
    """S5-D3 build notes (RC-6): /v7 keeps the ruled /v6 N2 ceiling (360 s CPU /
    900 s wall, CP-1a decision (3)); every other phase, PART_A included, keeps
    the shared 120 s / 300 s diagnostic ceiling -- there is no PART_A constant,
    and the controller charge stays 20 s."""
    module = profile_module()
    v7 = part_a_dispatch_profile_document()
    memory = v7['memory_bytes']
    budget = module.diagnostic_budget_profile(canonical_json_bytes(v7))
    shared = dict(cpu_ns=120_000_000_000, wall_ns=300_000_000_000, memory_bytes=memory)
    assert budget['phases']['N2'] == dict(
        cpu_ns=360_000_000_000, wall_ns=900_000_000_000, memory_bytes=memory
    )
    for phase, limits in budget['phases'].items():
        if phase != 'N2':
            assert limits == shared, phase
    assert set(budget['orchestration_cpu_ns'].values()) == {20_000_000_000}


def test_v7_diagnostic_budget_profile_is_not_refused_by_the_accept_tuple():
    """P1 (#519 S5 build pitfall): a schema outside the accept tuple raises
    'fresh diagnostic execution profile required'; /v7 must be inside it.
    The base behavior is shown without monkeypatching: the base deployment
    profile is well-formed and its schema stays outside the fresh-diagnostic
    tuple, so exactly that check refuses it, while the real /v7 bytes are
    accepted."""
    module = profile_module()
    from c1_rail.qualification.execution.protocol import sha256

    doc = part_a_dispatch_profile_document()
    budget = module.diagnostic_budget_profile(canonical_json_bytes(doc))
    assert budget['installed_profile_sha256'] == sha256(canonical_json_bytes(doc))
    assert 'N1' in budget['phases'] and 'PART_A' in budget['phases']
    module.parse_profile(canonical_json_bytes(document()))
    with pytest.raises(ValueError, match='fresh diagnostic execution profile required'):
        module.diagnostic_budget_profile(canonical_json_bytes(document()))


def test_v7_diagnostic_budget_profile_is_funded_with_v3_intents():
    """P2 (#519 S5 build pitfall): extending only the accept tuple leaves /v7
    unfunded (budget v2 with no funding_intents); /v7 must reach the funded
    budget v3 exactly as v6 does."""
    module = profile_module()
    doc = part_a_dispatch_profile_document()
    budget = module.diagnostic_budget_profile(canonical_json_bytes(doc))
    assert budget['schema'] == 'qualification_campaign_budget_profile/v3'
    assert budget['funding_intents'] == 'qualification_campaign_funding/v1'


def test_v7_n2_phase_keeps_the_360s_900s_ceiling_not_the_shared_fallback():
    """P3 (#519 S5 build pitfall): a /v7 missed by the N2 branch silently falls
    back to the shared 120 s CPU, below the measured 211 s N2 CPU -- the
    silent-SIGKILL failure checkpoint C2 found."""
    module = profile_module()
    doc = part_a_dispatch_profile_document()
    budget = module.diagnostic_budget_profile(canonical_json_bytes(doc))
    assert budget['phases']['N2'] == dict(
        cpu_ns=360_000_000_000, wall_ns=900_000_000_000, memory_bytes=doc['memory_bytes']
    )


def test_v7_release_binds_the_10000s_test_only_cap_in_the_fixture_producer(tmp_path):
    """P4 (#519 S5 build pitfall): the fixture producer raises the TEST_ONLY cap
    (10,000 s CPU / 10,000 s wall / memory_limit) only for the named release
    revisions; a /v7 release left outside binds 120 s / 180 s / 90% memory and
    is BUDGET_EXHAUSTED at binding. Lives here because test_profile.py owns the
    profile literals; fixture_producer is loaded exactly as
    test_boundary_fixture.py loads it."""
    import importlib.util
    from c1_rail.qualification.execution.profile import (
        diagnostic_budget_profile,
        part_a_dispatch_diagnostic_execution_profile,
    )

    root = Path(__file__).resolve().parents[4]
    profile = part_a_dispatch_diagnostic_execution_profile(canonical_json_bytes(document()))
    spec = importlib.util.spec_from_file_location(
        'qualification_boundary_v7_producer',
        root / 'tests/integration/qualification_boundary/fixture_producer.py',
    )
    fixture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixture)
    private, keys, _ = fixture.fresh_keys(execution_seed=b'a' * 32, result_seed=b'b' * 32)
    release = fixture.release_document(root, profile, 'sha256:' + 'c' * 64, keys)
    release.update(
        schema='qualification_execution_release/v7',
        capability='FULL_E1',
        dispatch_enabled=True,
        dispatch_checkpoints=['N1', 'N2', 'PART_A'],
        campaign_budget_profile=diagnostic_budget_profile(canonical_json_bytes(profile)),
    )
    bundle = fixture.build_real_bundle(
        tmp_path / 'retained',
        repo=root,
        release=canonical_json_bytes(release),
        private=private,
        keys=keys,
        attempt_id='fixture-v7-cap',
        idle=True,
    )
    budget = bundle['contract'].replay.budget
    assert budget.maximum_wall_seconds == 10000
    assert budget.maximum_cpu_seconds == 10000
    assert budget.maximum_memory_bytes == release['profile']['memory_bytes']
