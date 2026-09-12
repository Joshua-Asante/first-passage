import json
import os
from pathlib import Path
import subprocess
import sys

from c1_signal_daemon.m1_stage1_state import CeremonyStore
from c1_signal_daemon import m1_stage1_control as control


SCRIPT = Path(control.__file__).resolve()
PRODUCTION_ROOT = SCRIPT.parents[2]


def _run(cwd, state):
    env = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
    return subprocess.run(
        [sys.executable, str(SCRIPT), "status", "--state", str(state)],
        cwd=cwd, env=env, capture_output=True, text=True, timeout=15,
    )


def test_cli_bootstraps_without_pythonpath_from_repo_and_unrelated_cwd(tmp_path):
    state = tmp_path / "state.json"
    CeremonyStore(state).boot("boot-1")
    for cwd in (PRODUCTION_ROOT, tmp_path):
        result = _run(cwd, state)
        assert result.returncode == 0, result.stderr
        assert json.loads(result.stdout)["boot_id"] == "boot-1"
