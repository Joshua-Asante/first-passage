"""Fault injection for the image validator, without a Docker daemon.

Run the real shell orchestration with a failing Docker boundary. A broken image
must produce a complete failing table, not terminate at the first launch.
"""

import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
LISTENER = "L1 L2 L3 L4 L5a L5b L6 L6b L7 L8 L9".split()
DAEMON = "D1 D2 D3 D4 D5 D6 D7 D8 D9 D10".split()


@pytest.fixture
def shell():
    """Use Git Bash on Windows, rather than the unrelated WSL launcher."""
    executable = (
        Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Git/bin/bash.exe"
        if os.name == "nt" else shutil.which("bash")
    )
    if not executable or not Path(executable).exists():
        pytest.skip("Bash is required for the Linux image harness")
    return str(executable)


@pytest.mark.parametrize("target,expected", [("listener", LISTENER), ("daemon", DAEMON),
                                           ("all", LISTENER + DAEMON)])
@pytest.mark.parametrize("failure", ["build", "runtime"])
def test_docker_failure_emits_every_result(shell, tmp_path, target, expected, failure):
    """Docker create/exec failures must not suppress later checks or the summary."""
    stub = tmp_path / "boundary.sh"
    docker_body = (
        'if [ "$1" = build ] && [ "$FAILURE" != build ]; then exit 0; fi\n'
        'echo "injected Docker failure: $*" >&2\n'
        "exit 125\n"
    )
    # Python probes spawn Docker directly, outside Bash functions. Shadow that
    # executable too so Linux CI cannot accidentally use its real Docker daemon.
    bindir = tmp_path / "bin"
    bindir.mkdir()
    docker = bindir / "docker"
    docker.write_text("#!/bin/sh\n" + docker_body, encoding="utf-8")
    docker.chmod(0o755)
    stub.write_text(
        "docker() {\n"
        '  if [[ "$1" == build && "$FAILURE" != build ]]; then return 0; fi\n'
        '  echo "injected Docker failure: $*" >&2\n'
        "  return 125\n"
        "}\n"
        "sleep() { :; }\n"
        'python3() { "$TEST_PYTHON" "$@"; }\n',
        encoding="utf-8",
    )
    logs = tmp_path / "logs"
    env = dict(os.environ, BASH_ENV=stub.as_posix(), FAILURE=failure,
               PATH=str(bindir) + os.pathsep + os.environ["PATH"],
               TEST_PYTHON=Path(sys.executable).as_posix(),
               C1_IMAGE_VALIDATION_LOG_DIR=logs.as_posix())
    result = subprocess.run(
        [shell, "scripts/c1_image_validation.sh", target], cwd=ROOT, env=env,
        capture_output=True, text=True, timeout=90, check=False,
    )
    summary = logs / "summary.txt"
    assert summary.exists(), result.stdout + result.stderr
    lines = summary.read_text(encoding="utf-8").splitlines()
    wanted = [f"{'PASS' if failure == 'runtime' and key in ('L1', 'D1') else 'FAIL'} {key}"
              for key in expected]
    assert lines[:-1] == wanted, result.stdout + result.stderr
    assert result.returncode == 1, result.stdout + result.stderr
    if failure == "runtime":
        last_logs = (["L9_inimage.log"] if target == "listener" else
                     ["D10.err"] if target == "daemon" else ["L9_inimage.log", "D10.err"])
        for name in last_logs:
            assert "injected Docker failure" in (logs / name).read_text(encoding="utf-8")
