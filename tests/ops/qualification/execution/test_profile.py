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
