"""Docker ownership and setup failures must share the durable run lifecycle."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import pytest

from test_record_verification import make_repo

ROOT = Path(__file__).resolve().parents[1]


def runner():
    path = ROOT / 'scripts/docker_verification.py'
    assert path.exists(), 'durable Docker owner is not implemented'
    spec = importlib.util.spec_from_file_location('docker_verification_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_missing_docker_retains_setup_failure(tmp_path, monkeypatch):
    module = runner()
    repo = make_repo(tmp_path)
    monkeypatch.setattr(module, 'ROOT', repo)
    output = tmp_path / 'missing-docker'
    result = module.main(['--output', str(output), '--docker', str(tmp_path / 'absent')])
    record = json.loads((output / 'record.json').read_text())
    assert result != 0 and record['status'] == 'not_started'
    assert record['error'] and record['exit_code'] is None


def test_cleanup_failure_is_not_a_success(tmp_path, monkeypatch):
    module = runner()
    repo = make_repo(tmp_path)
    with module.RunRecord(repo, tmp_path / 'cleanup-error', ['test']) as record:
        record.begin()
        owner = module.DockerOwner(record, 'docker')
        def unavailable(*args, **kwargs):
            raise OSError('daemon unavailable during cleanup')
        monkeypatch.setattr(owner, 'call', unavailable)
        record.execute([sys.executable, '-c', 'pass'])
        owner.cleanup()
    assert record.data['verification_exit_code'] != 0
    assert not record.data['cleanup']['ok']


@pytest.mark.parametrize('stage', ['version', 'image', 'run'])
def test_docker_preflight_failure_is_recorded(tmp_path, monkeypatch, stage):
    module = runner()
    monkeypatch.setattr(module, 'ROOT', make_repo(tmp_path))
    monkeypatch.setattr(module, 'find_docker', lambda explicit: sys.executable)
    def fail_stage(owner, arguments, **kwargs):
        if arguments[0] == stage:
            raise RuntimeError(f'{stage} unavailable')
        return '' if arguments[0] == 'ps' else 'fixture'
    monkeypatch.setattr(module.DockerOwner, 'call', fail_stage)
    output = tmp_path / stage
    assert module.main(['--output', str(output)]) != 0
    record = json.loads((output / 'record.json').read_text())
    assert record['status'] == 'not_started' and stage in record['error']
    assert record['cleanup']['ok']


def test_foreign_cid_is_never_removed(tmp_path, monkeypatch):
    module = runner()
    with module.RunRecord(make_repo(tmp_path), tmp_path / 'foreign', ['test']) as record:
        record.begin()
        owner = module.DockerOwner(record, 'docker')
        owner.cid_file.write_text('a' * 64)
        calls = []
        def inspect_foreign(arguments, **kwargs):
            calls.append(arguments)
            return json.dumps([{'Config': {'Labels': {module.LABEL: 'someone-else'}}}]) if arguments[0] == 'inspect' else ''
        monkeypatch.setattr(owner, 'call', inspect_foreign)
        record.execute([sys.executable, '-c', 'pass'])
        owner.cleanup()
    assert not any(command[0] == 'rm' for command in calls)
    assert not record.data['cleanup']['ok'] and record.data['verification_exit_code'] != 0


@pytest.mark.skipif(os.environ.get('FP_TEST_DOCKER') != '1', reason='explicit local Docker integration opt-in')
@pytest.mark.parametrize('boundary', ['attach', 'create-response'])
def test_real_interruption_removes_owned_container_only(tmp_path, monkeypatch, boundary):
    module = runner()
    docker = module.find_docker(None)
    repo = make_repo(tmp_path)
    output = tmp_path / 'real-interruption'
    unrelated = subprocess.check_output([docker, 'create', '--network', 'none',
                                        'first-passage-verification:py311', 'python', '-c', 'pass'], text=True).strip()
    try:
        with module.RunRecord(repo, output, ['interrupt Docker']) as record:
            record.begin()
            owner = module.DockerOwner(record, docker)
            original_call = owner.call
            original_popen = subprocess.Popen
            owned_ids = []

            def interrupted_create(arguments, **kwargs):
                response = original_call(arguments, **kwargs)
                if arguments[0] == 'create':
                    owned_ids.append(response.strip())
                    if boundary == 'create-response':
                        owner.cid_file.unlink()  # Exercise label recovery without a received CID.
                        raise KeyboardInterrupt
                return response

            class InterruptedAttach(original_popen):
                interrupted = False

                def wait(self, timeout=None):
                    if self.args[1:3] == ['start', '-a'] and not self.interrupted:
                        self.interrupted = True
                        deadline = time.monotonic() + 10
                        while time.monotonic() < deadline:
                            running = original_call(['inspect', '-f', '{{.State.Running}}', self.args[-1]])
                            if running.strip() == 'true':
                                break
                            time.sleep(0.05)
                        assert running.strip() == 'true' and self.poll() is None
                        raise KeyboardInterrupt  # At the actual wait for the live attached CLI.
                    return super().wait(timeout=timeout)

            monkeypatch.setattr(owner, 'call', interrupted_create)
            monkeypatch.setattr(subprocess, 'Popen', InterruptedAttach)
            try:
                cid = owner.create(['--network', 'none', 'first-passage-verification:py311',
                                    'python', '-c', 'import time; time.sleep(60)'])
                record.execute([docker, 'start', '-a', cid])
            finally:
                owner.cleanup()
        assert record.data['status'] == 'interrupted'
        assert record.data['cleanup']['ok']
        assert owned_ids
        assert subprocess.run([docker, 'inspect', owned_ids[0]], capture_output=True).returncode != 0
        assert subprocess.run([docker, 'inspect', unrelated], capture_output=True).returncode == 0
    finally:
        subprocess.run([docker, 'rm', '-f', unrelated], capture_output=True)
