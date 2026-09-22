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
