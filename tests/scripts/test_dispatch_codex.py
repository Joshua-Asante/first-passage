"""dispatch_codex.ps1 contract: sandbox, worktree and agent-token handling."""
import os
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "dispatch_codex.ps1"
PWSH = shutil.which("pwsh")
pytestmark = pytest.mark.skipif(PWSH is None, reason="PowerShell 7 not installed")


def _run(tmp_path, *extra, env_token=None, dry=True, prompt="do x"):
    env = {k: v for k, v in os.environ.items() if k != "FP_AGENT_GH_TOKEN"}
    if env_token:
        env["FP_AGENT_GH_TOKEN"] = env_token
    # An explicit -Codex keeps the test off Windows package discovery (portable to Linux CI).
    args = [PWSH, "-NoProfile", "-File", str(SCRIPT), "-Worktree", str(tmp_path),
            *(["-Prompt", prompt] if prompt else []), "-OutputFile", str(tmp_path / "out.txt"),
            "-Codex", str(tmp_path / "codex-not-run.exe"), *extra]
    if dry:
        args.append("-DryRun")
    return subprocess.run(args, capture_output=True, text=True, env=env)


def test_dry_run_builds_sandboxed_exec(tmp_path):
    # Fails if the dispatch drops the worktree, the sandbox or the last-message file.
    out = _run(tmp_path, "-Model", "gpt-6.1-sol")
    assert out.returncode == 0, out.stderr
    assert f"exec | -C | {tmp_path} | -s | workspace-write | -o |" in out.stdout
    assert "-m | gpt-6.1-sol | do x" in out.stdout


def test_token_is_never_printed(tmp_path):
    # Fails if the agent token's value reaches output.
    out = _run(tmp_path, env_token="github_pat_SECRET123")
    assert "agent token set" in out.stdout
    assert "SECRET123" not in out.stdout + out.stderr


@pytest.mark.parametrize("token", ["gho_OPERATOR123", "ghp_CLASSIC123"])
def test_refuses_token_that_is_not_a_fine_grained_pat(tmp_path, token):
    # Fails if an OAuth or classic token (likely the operator's) can be handed to Codex, or
    # if the refusal prints it.
    out = _run(tmp_path, env_token=token)
    assert out.returncode != 0
    assert "fine-grained PAT" in out.stderr + out.stdout
    assert token not in out.stdout + out.stderr


def test_refuses_to_launch_without_agent_token(tmp_path):
    # Fails if a real run launches Codex with no agent token, letting gh fall back to the
    # operator's stored credential (Codex #902).
    out = _run(tmp_path, dry=False)
    assert out.returncode != 0
    assert "FP_AGENT_GH_TOKEN" in out.stderr + out.stdout
    assert "Codex app CLI not found" not in out.stderr + out.stdout  # refused before launch


def test_refuses_worktree_with_env(tmp_path):
    # Fails if a Codex worker could be given a directory holding .env.
    (tmp_path / ".env").write_text("X=1\n")
    out = _run(tmp_path)
    assert out.returncode != 0
    assert ".env" in out.stderr + out.stdout


def test_review_mode_is_read_only_with_base_and_no_prompt(tmp_path):
    # Fails if the CLI review fallback could write to the worktree or pass a prompt that
    # `codex exec review --base` rejects.
    out = _run(tmp_path, "-ReviewBase", "origin/main", "-Sandbox", "workspace-write", prompt=None)
    assert out.returncode == 0, out.stderr
    assert f"exec | -C | {tmp_path} | -s | read-only | review | --base | origin/main | -o |" in out.stdout


def test_prompt_required_without_review_base(tmp_path):
    out = _run(tmp_path, prompt=None)
    assert out.returncode != 0
    assert "-ReviewBase" in out.stderr + out.stdout
