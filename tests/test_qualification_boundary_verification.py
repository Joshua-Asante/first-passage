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


def test_host_cleanup_runs_after_ownership_lock_is_released(tmp_path, monkeypatch):
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

        def execute(self, *_args, **_kwargs):
            self.data['test_summary'] = {
                'collected': 1, 'passed': 1, 'failed': 0, 'errors': 0, 'skipped': 0,
            }
            self.data['verification_exit_code'] = 0

    def observed_cleanup(path):
        assert path == manifest_path
        events.append('cleanup')
        return {'status': 'retired'}

    monkeypatch.setattr(module.platform, 'system', lambda: 'Linux')
    monkeypatch.setattr(module.os, 'geteuid', lambda: 0, raising=False)
    monkeypatch.setattr(module, 'protected', lambda path: path)
    monkeypatch.setattr(module, 'RunRecord', Record)
    monkeypatch.setattr(module, 'ownership_lock', observed_lock)
    monkeypatch.setattr(module, 'cleanup', observed_cleanup)

    assert module.main(['--host-only', '--manifest', str(manifest_path)]) == 0
    assert events == ['lock-enter', 'begin', 'lock-exit', 'cleanup']
