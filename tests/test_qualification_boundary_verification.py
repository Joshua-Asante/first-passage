"""Boundary wrapper must reject unsupported setups before running any tests."""
from contextlib import contextmanager
import importlib
import json
from pathlib import Path
import pytest


def runner():
    name = 'scripts.qualification_boundary_verification'
    assert importlib.util.find_spec(name), 'boundary verification wrapper is missing'
    return importlib.import_module(name)


def test_empty_or_skipped_acceptance_is_not_success():
    module = runner()
    for counts in ({'collected': 0, 'failed': 0, 'errors': 0, 'skipped': 0},
                   {'collected': 10, 'failed': 0, 'errors': 0, 'skipped': 1}):
        with pytest.raises(ValueError):
            module.require_tests(counts)


def test_partial_or_failed_report_is_rejected():
    module = runner()
    for counts in (None, {}, {'collected': 3, 'passed': 2, 'failed': 1, 'errors': 0, 'skipped': 0}):
        with pytest.raises(ValueError):
            module.require_tests(counts)


def test_nonlinux_entry_point_fails_without_provisioning(monkeypatch):
    module = runner()
    monkeypatch.setattr(module.platform, 'system', lambda: 'Windows')
    assert module.main(['--test-only']) != 0


@pytest.mark.parametrize('mode',['--host-only','--test-only','--s2'])
def test_host_cleanup_runs_after_ownership_lock_is_released(tmp_path, monkeypatch,mode):
    module = runner()
    manifest_path = tmp_path / 'run' / 'ownership.json'
    manifest_path.parent.mkdir()
    manifest_path.write_text(json.dumps({
        'host_config_sha256': 'configured',
        'source': {'commit': 'candidate'},
    }))
    events = []

    @contextmanager
    def observed_lock(root):
        assert root == manifest_path.parent
        events.append('lock-enter')
        try:
            yield
        finally:
            events.append('lock-exit')

    class Record:
        def __init__(self, *_args):
            self.data = {'before': {'commit': 'candidate'}}

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def begin(self):
            events.append('begin')

        def execute(self, command, **_kwargs):
            if mode=='--s2':
                # Every S2 file, in S2_CASES order (the last supervision case contaminates the host).
                positions=[command.index(case) for case in module.S2_CASES]
                assert positions==sorted(positions) and len(module.S2_CASES)>1
                assert not any(argument.startswith('--ignore=') for argument in command)
            else:
                selection='tests/integration/qualification_host' if mode=='--host-only' else 'tests/integration/qualification_boundary'
                assert selection in command
                if mode=='--test-only':
                    # The whole S3 file set (S2 files included) stays out of N1_ONLY.
                    assert all('--ignore='+case in command for case in module.S3_CASES)
                    # The unintegrated T05 result/seal file stays out too.
                    assert all('--ignore='+case in command for case in module.T05_CASES)
            if mode=='--test-only':
                assert self.data['metadata']['qualification_acceptance']=='coordinator_review_required'
            self.data['test_summary'] = {
                'collected': 1, 'passed': 1, 'failed': 0, 'errors': 0, 'skipped': 0,
            }
            self.data['verification_exit_code'] = 0

    def observed_cleanup(path):
        assert path == manifest_path
        events.append('cleanup')
        return {'ok': True}

    monkeypatch.setattr(module.platform, 'system', lambda: 'Linux')
    monkeypatch.setattr(module.os, 'geteuid', lambda: 0, raising=False)
    monkeypatch.setattr(module, 'protected', lambda path: path)
    monkeypatch.setattr(module, 'RunRecord', Record)
    monkeypatch.setattr(module, 'require_invariants', lambda *args, **kwargs: {'passed': True})
    monkeypatch.setattr(module, 'ownership_lock', observed_lock)
    monkeypatch.setattr(module, 'cleanup', observed_cleanup)
    monkeypatch.setattr(module,'create_process_group',lambda root:root/'group')
    monkeypatch.setattr(module,'owned_command',lambda group,command,interpreter:command)

    assert module.main([mode, '--manifest', str(manifest_path)]) == 0
    assert events == ['lock-enter', 'begin', 'lock-exit', 'cleanup']


def test_invariant_gate_requires_actual_reports(tmp_path):
    from scripts.qualification_boundary_verification import require_invariants
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from test_qualification_invariant_manifest import manifest, NODE
    raw = json.dumps(manifest()).encode()
    collection = tmp_path / 'collected.json'
    collection.write_text(json.dumps([NODE]))
    with pytest.raises(ValueError, match='Qualification invariants'):
        require_invariants(raw, collection, tmp_path / 'missing.xml', tmp_path)
    diagnostics = json.loads((tmp_path / 'invariants.json').read_bytes())
    assert not diagnostics['passed']


@pytest.mark.parametrize('counts', [{'ok': False}, {}, {'ok': 1}])
def test_cleanup_must_be_explicitly_successful(counts):
    with pytest.raises(ValueError, match='cleanup'):
        runner().require_cleanup(counts)


@pytest.mark.parametrize('mode',['--test-only','--s2','--s3'])
def test_required_nodes_match_the_selected_file_set(tmp_path, monkeypatch, mode):
    """--test-only must never require a node of the S3 file set: those nodes skip
    there by design (no FP_QUALIFICATION_S3) and are ignored by the selection, so
    requiring them fails the required boundary jobs (PR #455, aaf9646)."""
    module = runner()
    manifest_path = tmp_path / 'run' / 'ownership.json'
    manifest_path.parent.mkdir()
    manifest_path.write_text(json.dumps({'host_config_sha256': 'configured', 'source': {'commit': 'candidate'}}))
    seen = {}

    class Record:
        def __init__(self, *_args):
            self.data = {'before': {'commit': 'candidate'}, 'metadata': {}}

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def begin(self):
            pass

        def execute(self, command, **_kwargs):
            self.data['test_summary'] = {'collected': 1, 'passed': 1, 'failed': 0, 'errors': 0, 'skipped': 0}
            self.data['verification_exit_code'] = 0

    def observed_invariants(*_args, required_nodeids, **_kwargs):
        seen['required'] = set(required_nodeids)
        return {'passed': True}

    @contextmanager
    def lock(_root):
        yield

    monkeypatch.setattr(module.platform, 'system', lambda: 'Linux')
    monkeypatch.setattr(module.os, 'geteuid', lambda: 0, raising=False)
    monkeypatch.setattr(module, 'protected', lambda path: path)
    monkeypatch.setattr(module, 'RunRecord', Record)
    monkeypatch.setattr(module, 'require_invariants', observed_invariants)
    monkeypatch.setattr(module, 'ownership_lock', lock)
    monkeypatch.setattr(module, 'cleanup', lambda path: {'ok': True})
    monkeypatch.setattr(module, 'create_process_group', lambda root: root / 'group')
    monkeypatch.setattr(module, 'owned_command', lambda group, command, interpreter: command)

    assert module.main([mode, '--manifest', str(manifest_path)]) == 0
    registered = module._manifest(module.INVARIANT_MANIFEST.read_bytes())
    s2 = tuple(case + '::' for case in module.S2_CASES)
    s3 = tuple(case + '::' for case in module.S3_CASES)
    expected = {'--test-only': {node for node in registered if not node.startswith(s3)},
                '--s2': {node for node in registered if node.startswith(s2)},
                '--s3': {node for node in registered if node.startswith(s3)}}[mode]
    assert seen['required'] == expected and expected
    if mode == '--test-only':
        assert not any(node.startswith(s3) for node in seen['required'])


def test_cases_refuses_when_the_expression_parser_is_unavailable(monkeypatch, capsys):
    """G5: without pytest's -k parser the subset cannot be validated, so it is refused early."""
    import sys
    module = runner()
    monkeypatch.setattr(module.platform, 'system', lambda: 'Linux')
    monkeypatch.setattr(module.os, 'geteuid', lambda: 0, raising=False)
    monkeypatch.setitem(sys.modules, '_pytest.mark.expression', None)
    assert module.main(['--s3', '--cases', 'downtime']) == 2
    err = capsys.readouterr().err
    assert '--cases' in err and '--manifest' not in err
