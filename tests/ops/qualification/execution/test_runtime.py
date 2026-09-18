"""Entrypoint-derived source inventories, independent of imported test fixtures."""
import importlib
from pathlib import Path


def test_worker_closure_includes_deferred_source_dependencies_without_authorities():
    runtime = importlib.import_module('c1_rail.qualification.execution.runtime')
    closure = runtime.source_closure(Path(__file__).resolve().parents[4], 'worker')
    assert 'c1_rail.qualification.execution.worker' in closure
    assert 'c1_rail.qualification.production_source' in closure
    assert 'c1_rail.qualification.replay' in closure
    assert not set(closure).intersection({'c1_rail.qualification.execution.signing',
        'c1_rail.qualification.execution.store', 'c1_rail.qualification.attempt'})


def test_runtime_lock_parser_checks_hash_continuation_requirements():
    runtime = importlib.import_module('c1_rail.qualification.execution.runtime')
    values = runtime.locked_versions('cryptography==50.0.1 \\\n    --hash=sha256:abc\npytest==8.4.2\n')
    assert values == {'cryptography': '50.0.1', 'pytest': '8.4.2'}
def test_g5_closure_contains_no_execution_or_source_loader():
    runtime = importlib.import_module('c1_rail.qualification.execution.runtime')
    closure = runtime.source_closure(Path(__file__).resolve().parents[4], 'g5')
    assert 'c1_rail.qualification.execution.g5' in closure
    assert not set(closure).intersection({'c1_rail.qualification.execution.worker',
        'c1_rail.qualification.execution.signing', 'c1_rail.qualification.execution.store',
        'c1_rail.qualification.execution.launcher', 'c1_rail.qualification.production_source'})





def test_runtime_manifest_binds_canonical_signing_configuration():
    from c1_rail.qualification.execution.protocol import sha256
    runtime=importlib.import_module('c1_rail.qualification.execution.runtime')
    root=Path(__file__).resolve().parents[4]
    observed=runtime.observe_runtime(root,'g5')
    assert observed['signing_configuration_sha256']==sha256((root/'tools/local_verification/requirements-extra.txt').read_bytes())
