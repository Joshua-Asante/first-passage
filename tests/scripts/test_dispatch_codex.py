"""dispatch_codex.ps1 contract: sandbox, worktree, environment and agent-token handling."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "dispatch_codex.ps1"
PWSH = shutil.which("pwsh")
GIT = shutil.which("git")
pytestmark = pytest.mark.skipif(PWSH is None or GIT is None, reason="PowerShell 7 or git not installed")

AGENT = "github_pat_AGENTSECRET123"


def _clean_env():
    # Drop GIT_* so a run from inside a Git hook (GIT_DIR, GIT_INDEX_FILE) cannot redirect git.
    return {k: v for k, v in os.environ.items()
            if k != "FP_AGENT_GH_TOKEN" and not k.startswith("GIT_")}


def _git(*args, cwd):
    subprocess.run([GIT, "-c", "user.name=t", "-c", "user.email=t@example.invalid",
                    "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", *args],
                   cwd=cwd, check=True, capture_output=True, env=_clean_env())


@pytest.fixture
def repo(tmp_path):
    root = tmp_path.resolve() / "repo"
    root.mkdir()
    _git("init", "-q", cwd=root)
    (root / "README.md").write_text("x\n")
    _git("add", "README.md", cwd=root)
    _git("commit", "-q", "-m", "init", cwd=root)
    _git("worktree", "add", "-q", "--detach", str(root / ".claude" / "worktrees" / "wt"), cwd=root)
    return root


@pytest.fixture
def wt(repo):
    return repo / ".claude" / "worktrees" / "wt"


def _run(worktree, *extra, env_token=None, dry=True, prompt="do x", codex=None, parent_env=None):
    env = _clean_env()
    env.update(parent_env or {})
    if env_token:
        env["FP_AGENT_GH_TOKEN"] = env_token
    out_file = worktree.parent / "out.txt"
    # An explicit -Codex keeps the test off Windows package discovery (portable to Linux CI).
    args = [PWSH, "-NoProfile", "-File", str(SCRIPT), "-Worktree", str(worktree),
            *(["-Prompt", prompt] if prompt else []), "-OutputFile", str(out_file),
            "-Codex", str(codex or worktree.parent / "codex-not-run.exe"), *extra]
    if dry:
        args.append("-DryRun")
    return subprocess.run(args, capture_output=True, text=True, env=env)


def test_dry_run_builds_sandboxed_exec(wt):
    # Fails if the dispatch drops the worktree, the sandbox or the last-message file.
    out = _run(wt, "-Model", "gpt-6.1-sol")
    assert out.returncode == 0, out.stderr
    assert f"exec | -C | {wt} | -s | workspace-write | -o |" in out.stdout
    assert "-m | gpt-6.1-sol | do x" in out.stdout


def test_token_is_never_printed(wt):
    # Fails if the agent token's value reaches output.
    out = _run(wt, env_token="github_pat_SECRET123")
    assert "agent token set" in out.stdout
    assert "SECRET123" not in out.stdout + out.stderr


def test_dry_run_lists_env_names_not_values(wt):
    # Fails if dry-run omits the child's variable names, prints a value, or lists a
    # non-allowlisted caller variable.
    out = _run(wt, env_token=AGENT, parent_env={"FP_TEST_SECRET": "sentinel-value-1"})
    assert out.returncode == 0, out.stderr
    env_line = next(line for line in out.stdout.splitlines() if line.startswith("env: "))
    names = env_line[len("env: "):].split(", ")
    assert "PATH" in names and "GH_TOKEN" in names
    assert "FP_TEST_SECRET" not in names and "FP_AGENT_GH_TOKEN" not in names
    assert os.environ["PATH"] not in out.stdout
    assert "sentinel-value-1" not in out.stdout + out.stderr


@pytest.mark.parametrize("token", ["gho_OPERATOR123", "ghp_CLASSIC123"])
def test_refuses_token_that_is_not_a_fine_grained_pat(wt, token):
    # Fails if an OAuth or classic token (likely the operator's) can be handed to Codex, or
    # if the refusal prints it.
    out = _run(wt, env_token=token)
    assert out.returncode != 0
    assert "fine-grained PAT" in out.stderr + out.stdout
    assert token not in out.stdout + out.stderr


def test_refuses_to_launch_without_agent_token(wt):
    # Fails if a real run launches Codex with no agent token, letting gh fall back to the
    # operator's stored credential (Codex #902).
    out = _run(wt, dry=False)
    assert out.returncode != 0
    assert "FP_AGENT_GH_TOKEN" in out.stderr + out.stdout
    assert "Codex app CLI not found" not in out.stderr + out.stdout  # refused before launch


def _stub(tmp_path):
    record = tmp_path / "child-env.txt"
    if sys.platform == "win32":
        stub = tmp_path / "codex-stub.cmd"
        stub.write_text(f'@set > "{record}"\r\n@exit /b 0\r\n')
    else:
        stub = tmp_path / "codex-stub.sh"
        stub.write_text(f'#!/bin/sh\n/usr/bin/env > "{record}"\nexit 0\n')
        stub.chmod(0o755)
    return stub, record


def test_child_gets_only_allowlisted_env_and_agent_token(wt, tmp_path):
    # Fails if any caller variable outside the allowlist (another token, a Fly credential,
    # a private value) reaches Codex, or if GH_TOKEN is not exactly the agent PAT.
    stub, record = _stub(tmp_path)
    sentinels = {"FP_TEST_SECRET": "x", "FLY_API_TOKEN": "x", "GITHUB_TOKEN": "x",
                 "OPENAI_API_KEY": "x", "GH_TOKEN": "gho_OPERATOR_PARENT"}
    out = _run(wt, env_token=AGENT, dry=False, codex=stub, parent_env=sentinels)
    assert out.returncode == 0, out.stdout + out.stderr
    child = {}
    for line in record.read_text().splitlines():
        name, sep, value = line.partition("=")
        if sep:
            child[name.upper()] = value
    for name in ("FP_TEST_SECRET", "FLY_API_TOKEN", "GITHUB_TOKEN", "OPENAI_API_KEY",
                 "FP_AGENT_GH_TOKEN"):
        assert name not in child, name
    assert child["GH_TOKEN"] == AGENT
    assert "PATH" in child
    allow = {"SYSTEMROOT", "SYSTEMDRIVE", "WINDIR", "COMSPEC", "PATH", "PATHEXT", "TEMP", "TMP",
             "USERPROFILE", "USERNAME", "HOMEDRIVE", "HOMEPATH", "HOME", "APPDATA",
             "LOCALAPPDATA", "PROGRAMDATA", "PROGRAMFILES", "PROGRAMFILES(X86)", "PROGRAMW6432",
             "COMMONPROGRAMFILES", "OS", "PROCESSOR_ARCHITECTURE", "NUMBER_OF_PROCESSORS",
             "CODEX_HOME", "GH_TOKEN"}
    shell_added = {"PWD", "OLDPWD", "SHLVL", "_", "PROMPT"}  # set by the stub's own shell
    assert set(child) - allow - shell_added == set()


def test_refuses_worktree_with_env(wt):
    # Fails if a Codex worker could be given a directory holding .env.
    (wt / ".env").write_text("X=1\n")
    out = _run(wt)
    assert out.returncode != 0
    assert ".env" in out.stderr + out.stdout


def test_refuses_worktree_outside_claude_worktrees(repo, tmp_path):
    # Fails if Codex can be pointed at the primary checkout, a worktree elsewhere, a plain
    # directory under .claude/worktrees, or a directory outside any Git checkout.
    elsewhere = tmp_path.resolve() / "elsewhere"
    _git("worktree", "add", "-q", "--detach", str(elsewhere), cwd=repo)
    plain = repo / ".claude" / "worktrees" / "plain"
    plain.mkdir()
    no_git = tmp_path.resolve() / "nogit"
    no_git.mkdir()
    for target in (repo, elsewhere, plain, no_git):
        out = _run(target)
        assert out.returncode != 0, target
        assert "worktrees" in out.stderr + out.stdout, target
        assert "args:" not in out.stdout, target


def test_private_names_are_not_screened(wt):
    # Fails if the launcher again refuses what Codex may read (Joshua's 2026-11-06 ruling):
    # a prompt naming a private file, or a worktree holding one.
    (wt / "notes").mkdir()
    (wt / "notes" / "effective_inputs.json").write_text("{}")
    (wt / "notes" / "anything.pine").write_text("y")
    out = _run(wt, prompt="read effective_inputs.json and anything.pine")
    assert out.returncode == 0, out.stderr


def test_review_mode_is_read_only_with_base_and_no_prompt(wt):
    # Fails if the CLI review fallback could write to the worktree or pass a prompt that
    # `codex exec review --base` rejects.
    out = _run(wt, "-ReviewBase", "origin/main", "-Sandbox", "workspace-write", prompt=None)
    assert out.returncode == 0, out.stderr
    assert f"exec | -C | {wt} | -s | read-only | review | --base | origin/main | -o |" in out.stdout


def test_prompt_required_without_review_base(wt):
    out = _run(wt, prompt=None)
    assert out.returncode != 0
    assert "-ReviewBase" in out.stderr + out.stdout
