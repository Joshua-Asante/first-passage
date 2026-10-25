"""dispatch_codex.ps1 dry-run contract: sandbox, worktree and token handling."""
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "dispatch_codex.ps1"
PWSH = shutil.which("pwsh")
pytestmark = pytest.mark.skipif(PWSH is None, reason="PowerShell 7 not installed")


def _run(tmp_path, *extra, env_token=None):
    env = {k: v for k, v in __import__("os").environ.items() if k != "FP_AGENT_GH_TOKEN"}
    if env_token:
        env["FP_AGENT_GH_TOKEN"] = env_token
    return subprocess.run(
        [PWSH, "-NoProfile", "-File", str(SCRIPT), "-Worktree", str(tmp_path),
         "-Prompt", "do x", "-OutputFile", str(tmp_path / "out.txt"), "-DryRun", *extra],
        capture_output=True, text=True, env=env)


def test_dry_run_builds_sandboxed_exec(tmp_path):
    # Fails if the dispatch drops the worktree, the sandbox or the last-message file.
    out = _run(tmp_path, "-Model", "gpt-6.1-sol")
    assert out.returncode == 0, out.stderr
    assert f"exec | -C | {tmp_path} | -s | workspace-write | -o |" in out.stdout
    assert "-m | gpt-6.1-sol | do x" in out.stdout


def test_token_is_never_printed(tmp_path):
    # Fails if the agent token's value reaches output.
    out = _run(tmp_path, env_token="SECRET-VALUE-123")
    assert "agent token set" in out.stdout
    assert "SECRET-VALUE-123" not in out.stdout + out.stderr


def test_refuses_worktree_with_env(tmp_path):
    # Fails if a Codex worker could be given a directory holding .env.
    (tmp_path / ".env").write_text("X=1\n")
    out = _run(tmp_path)
    assert out.returncode != 0
    assert ".env" in out.stderr + out.stdout
