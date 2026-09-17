"""Real pytest observations remain advisory across serial and xdist execution."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def isolated_configuration(tmp_path):
    (tmp_path / 'pyproject.toml').write_text('[tool.pytest.ini_options]\ndisable_test_id_escaping_and_forfeit_all_rights_to_community_support = true\n')


@pytest.mark.parametrize('workers', [0, 2])
def test_progress_observes_completed_not_passed(tmp_path, workers):
    output = tmp_path / 'progress'
    output.mkdir()
    for name, body in {
        'pass': 'import time\ndef test_pass():\n    time.sleep(.3)\n',
        'fail': 'def test_fail():\n    assert False\n',
        'skip': 'import pytest\ndef test_skip():\n    pytest.skip("expected")\n',
        'setup': 'import pytest\n@pytest.fixture\ndef bad():\n    raise ValueError("setup")\ndef test_setup(bad):\n    pass\n',
        'teardown': 'import pytest\n@pytest.fixture\ndef bad():\n    yield\n    raise ValueError("teardown")\ndef test_teardown(bad):\n    pass\n',
    }.items():
        (tmp_path / f'test_{name}.py').write_text(body)
    env = dict(os.environ, FP_PYTEST_PROGRESS_DIR=str(output), FP_PYTEST_PROGRESS_RUN='fixture')
    result = subprocess.run([sys.executable, '-m', 'pytest', '-p', 'scripts.pytest_progress',
        '-c', str(tmp_path / 'pyproject.toml'), '--rootdir=' + str(tmp_path), str(tmp_path),
        '-n', str(workers), '--basetemp=' + str(tmp_path / 'temp'), '-q'],
        cwd=ROOT, env=env, capture_output=True, text=True)
    assert result.returncode == 1, result.stdout + result.stderr
    saved = json.loads((output / 'progress.json').read_text())
    assert saved['collected'] == 5 and saved['completed'] == 5
    assert len(saved['completed_nodeids']) == 5 and saved['active_nodeids'] == []
    assert saved['run_id'] == 'fixture' and saved['observed_at'] > 0
    if workers:
        assert len(list(output.glob('progress-gw*.json'))) == 2


def test_worker_crash_cannot_look_complete(tmp_path):
    output = tmp_path / 'progress'
    output.mkdir()
    (tmp_path / 'test_crash.py').write_text('def test_crash():\n    import os\n    os._exit(9)\n')
    result = subprocess.run([sys.executable, '-m', 'pytest', '-p', 'scripts.pytest_progress',
        '-c', str(tmp_path / 'pyproject.toml'), str(tmp_path), '-n', '2', '--max-worker-restart=0',
        '--basetemp=' + str(tmp_path / 'temp'), '-q'],
        cwd=ROOT, env=dict(os.environ, FP_PYTEST_PROGRESS_DIR=str(output), FP_PYTEST_PROGRESS_RUN='crash'),
        capture_output=True, text=True)
    assert result.returncode != 0
    workers = [json.loads(p.read_text()) for p in output.glob('progress-gw*.json')]
    assert any(p['active_nodeids'] and not p['session_finished'] for p in workers)


def test_snapshot_is_bounded_while_total_counts_remain_accurate(tmp_path):
    output = tmp_path / 'progress'
    output.mkdir()
    (tmp_path / 'test_many.py').write_text('import pytest\n@pytest.mark.parametrize("n", range(300), ids=[(chr(0x1f315) * 300) + str(n) for n in range(300)])\ndef test_many(n):\n    pass\n')
    result = subprocess.run([sys.executable, '-m', 'pytest', '-p', 'scripts.pytest_progress',
        '-c', str(tmp_path / 'pyproject.toml'), str(tmp_path), '-q'], cwd=ROOT,
        env=dict(os.environ, FP_PYTEST_PROGRESS_DIR=str(output), FP_PYTEST_PROGRESS_RUN='bounded'),
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    raw = (output / 'progress.json').read_bytes()
    saved = json.loads(raw)
    assert saved['completed'] == 300 and saved['truncated']
    assert len(saved['completed_nodeids']) <= 128 and len(raw) < 160_000
