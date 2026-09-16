"""Evidence must describe failures and changing inputs without false acceptance."""
import json
from pathlib import Path
import subprocess
import sys
import importlib.util
import io
import os
import signal

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'record_verification.py'


def make_repo(tmp_path):
    repo = tmp_path / 'source'
    repo.mkdir()
    subprocess.run(['git', 'init', '-q', str(repo)], check=True)
    (repo / 'input.txt').write_text('original')
    subprocess.run(['git', '-C', str(repo), 'add', 'input.txt'], check=True)
    subprocess.run(['git', '-C', str(repo), '-c', 'user.name=Test',
                    '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'fixture'], check=True)
    return repo


def run(repo, output, code):
    return subprocess.run([sys.executable, str(SCRIPT), '--repo', str(repo),
                           '--output', str(output), '--', sys.executable, '-c', code],
                          capture_output=True, text=True, check=False)


def test_failed_child_is_recorded_with_dirty_and_untracked_inputs(tmp_path):
    repo = make_repo(tmp_path)
    (repo / 'input.txt').write_text('changed')
    (repo / 'new.txt').write_text('also tested')
    output = tmp_path / 'failure'
    result = run(repo, output, 'print("diagnostic"); raise SystemExit(7)')
    assert result.returncode == 7
    record = json.loads((output / 'record.json').read_text())
    assert record['exit_code'] == 7 and record['source_stable']
    assert record['before']['files']['new.txt']
    assert record['before']['files']['input.txt']
    assert 'diagnostic' in (output / 'stdout.txt').read_text()


def test_successful_child_cannot_hide_source_drift(tmp_path):
    repo = make_repo(tmp_path)
    output = tmp_path / 'drift'
    result = run(repo, output, 'from pathlib import Path; Path("input.txt").write_text("mutated")')
    assert result.returncode != 0
    record = json.loads((output / 'record.json').read_text())
    assert record['exit_code'] == 0 and not record['source_stable']
    assert record['before']['fingerprint'] != record['after']['fingerprint']


def test_output_inside_source_is_rejected(tmp_path):
    repo = make_repo(tmp_path)
    result = run(repo, repo / 'evidence', 'raise SystemExit(0)')
    assert result.returncode != 0
    assert not (repo / 'evidence').exists()


def test_explicitly_allowed_ignored_output_does_not_contaminate_source(tmp_path):
    repo = make_repo(tmp_path)
    (repo / '.gitignore').write_text('.cache/\n')
    output = repo / '.cache' / 'run'
    result = subprocess.run([sys.executable, str(SCRIPT), '--repo', str(repo),
        '--output', str(output), '--allow-ignored-output', '--', sys.executable,
        '-c', 'import sys; print("live stdout"); print("live stderr",file=sys.stderr)'],
        capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    record = json.loads((output / 'record.json').read_text())
    assert record['source_stable'] and record['duration_seconds'] > 0
    assert 'live stdout' in result.stdout and 'live stderr' in result.stderr
    assert not any(name.startswith('.cache/') for name in record['after']['files'])


def test_launch_error_is_a_retained_failed_verification(tmp_path):
    repo = make_repo(tmp_path)
    output = tmp_path / 'launch-error'
    result = subprocess.run([sys.executable, str(SCRIPT), '--repo', str(repo),
        '--output', str(output), '--', str(tmp_path / 'no-such-executable')],
        capture_output=True, text=True, check=False)
    assert result.returncode == 127
    record = json.loads((output / 'record.json').read_text())
    assert record['launch_error'] and record['verification_exit_code'] == 127


def test_capture_write_failure_cannot_be_accepted(tmp_path, monkeypatch):
    repo = make_repo(tmp_path)
    output = tmp_path / 'capture-error'
    spec = importlib.util.spec_from_file_location('recorder_under_test', SCRIPT)
    recorder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recorder)
    original_open = Path.open

    class FailingLog(io.BytesIO):
        def write(self, data):
            raise OSError('simulated full disk')

    def fault_open(path, *args, **kwargs):
        if path == output / 'stdout.txt' and args == ('wb',):
            return FailingLog()
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, 'open', fault_open)
    code = recorder.main(['--repo', str(repo), '--output', str(output), '--',
                          sys.executable, '-c', 'print("evidence")'])
    assert code != 0
    record = json.loads((output / 'record.json').read_text())
    assert record['exit_code'] == 0
    assert not record['capture_complete']
    assert any('simulated full disk' in error for error in record['capture_errors'])


def test_inherited_pipe_does_not_block_record_creation(tmp_path):
    repo = make_repo(tmp_path)
    output = tmp_path / 'inherited-pipe'
    # Allow Git/process startup overhead, but finish long before the descendant.
    pid_file = tmp_path / 'descendant.pid'
    code = ('import subprocess,sys,pathlib; '
            'p=subprocess.Popen([sys.executable,"-c","import time; time.sleep(60)"]); '
            f'pathlib.Path({str(pid_file)!r}).write_text(str(p.pid))')
    try:
        result = subprocess.run([sys.executable, str(SCRIPT), '--repo', str(repo),
                                 '--output', str(output), '--', sys.executable, '-c', code],
                                capture_output=True, text=True, timeout=20, check=False)
    finally:
        if pid_file.exists():
            try:
                os.kill(int(pid_file.read_text()), signal.SIGTERM)
            except ProcessLookupError:
                pass
    assert result.returncode != 0
    record = json.loads((output / 'record.json').read_text())
    assert record['exit_code'] == 0 and not record['capture_complete']
    assert record['capture_errors']
