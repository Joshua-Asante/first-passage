"""All launcher consumers use one validated resolved isolation profile."""
import importlib
from c1_rail.qualification.contract import canonical_json_bytes
import pytest


def profile_module():
    return importlib.import_module('c1_rail.qualification.execution.profile')


def document():
    return dict(schema='qualification_execution_profile/v1', protocol_version=1,
                supported_checkpoints=['N1'], capability='N1_ONLY', production_execution=False,
                input_byte_limit=100000000, output_byte_limit=10000000,
                log_byte_limit=1000000, rpc_byte_limit=15000000,
                worker_uid=65532, memory_bytes=1000000000, pids_limit=64,
                scratch_bytes=10000000, admission_seconds=60, capture_seconds=10,
                network='none', read_only=True, capabilities=[], no_new_privileges=True,
                privileged=False, pid_mode='private', ipc_mode='private', restart='no')


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
