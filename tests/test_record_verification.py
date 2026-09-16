"""Evidence must describe failures and changing inputs without false acceptance."""
import json
from pathlib import Path
import subprocess
import sys

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
