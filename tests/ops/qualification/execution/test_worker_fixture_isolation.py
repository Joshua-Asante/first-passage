"""A library capture measures its worker, not accumulated pytest memory usage."""
from pathlib import Path
import os
import subprocess
import sys


def test_captured_fixture_does_not_inherit_parent_peak_memory(tmp_path):
    repository = Path(__file__).resolve().parents[4]
    script = r'''
import json
from pathlib import Path
import sys
repository = Path(sys.argv[1])
sys.path[:0] = [str(repository / 'ops'), str(repository / 'core'), str(repository)]
from c1_rail.qualification.execution.budget import peak_memory_bytes
profile = json.loads((repository / 'deploy/qualification/test-profile.json').read_bytes())
# Touch every page, then release the allocation: the OS high-water mark remains.
allocation = bytearray(profile['memory_bytes'] + 32 * 1024 * 1024)
for offset in range(0, len(allocation), 4096):
    allocation[offset] = 1
del allocation
assert peak_memory_bytes() > profile['memory_bytes']
import pytest
raise SystemExit(pytest.main([
    'tests/ops/qualification/execution/test_artifact_acceptance.py::test_reconstructs_all_five_real_artifact_roles',
    '-q', '-n', '0', '-o', 'addopts=', '--basetemp=' + sys.argv[2],
]))
'''
    environment = os.environ.copy()
    for name in ('PYTEST_ADDOPTS', 'PYTEST_XDIST_WORKER',
                 'PYTEST_XDIST_WORKER_COUNT', 'PYTEST_XDIST_TESTRUNUID'):
        environment.pop(name, None)
    result = subprocess.run(
        [sys.executable, '-I', '-c', script, str(repository), str(tmp_path / 'pytest')],
        cwd=repository, env=environment, capture_output=True, text=True,
        timeout=180, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
