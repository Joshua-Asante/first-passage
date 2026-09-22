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


@pytest.mark.parametrize('mode,extra',[('--host-only',[]),('--test-only',[]),('--s2',[]),
                                        ('--s2',['--s2-select','deadline and not oom'])])
def test_host_cleanup_runs_after_ownership_lock_is_released(tmp_path, monkeypatch,mode,extra):
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
                metadata=self.data['metadata']
                if extra:
                    # Labelled diagnostic: the -k subset runs, the record can never be evidence.
                    assert command[command.index('-k')+1]=='deadline and not oom'
                    assert metadata['acceptance_scope']==module.DIAGNOSTIC_SCOPE
                    assert metadata['qualification_acceptance']=='not_evidence'
                    assert metadata['s2_select']=='deadline and not oom'
                else:
                    assert '-k' not in command and 's2_select' not in metadata
                    assert metadata['acceptance_scope']=='S2_DIAGNOSTIC_SUPERVISION'
            else:
                selection='tests/integration/qualification_host' if mode=='--host-only' else 'tests/integration/qualification_boundary'
                assert selection in command
                if mode=='--test-only':
                    assert all('--ignore='+case in command for case in module.S2_CASES)
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

    assert module.main([mode, '--manifest', str(manifest_path), *extra]) == 0
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


@pytest.mark.parametrize('argv', [
    ['--test-only', '--s2-select', 'deadline'],
    ['--host-only', '--s2-select', 'deadline'],
    ['--s2', '--s2-select', ''],
    ['--s2', '--s2-select', '   '],
    ['--s2', '--s2-select', '-p evil'],
    ['--s2', '--s2-select', 'deadline\nnot oom'],
    ['--s2', '--s2-select', 'x' * 257],
])
def test_diagnostic_selection_is_refused_before_any_host_work(monkeypatch, argv):
    module = runner()
    touched = []
    monkeypatch.setattr(module, 'protected', lambda path: touched.append(path))
    with pytest.raises(SystemExit) as exc:
        module.main(argv)
    assert exc.value.code == 2 and not touched
