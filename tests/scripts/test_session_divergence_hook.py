"""SessionStart must measure the stdin checkout, regardless of process cwd."""
import importlib.util
import io
import json
import subprocess
from pathlib import Path

import pytest


HOOK = Path(__file__).resolve().parents[2] / "scripts/session_divergence_hook.py"
spec = importlib.util.spec_from_file_location("session_divergence_hook", HOOK)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True, capture_output=True, text=True, timeout=10,
    ).stdout.strip()


def make_repo(path, ahead=0):
    path.mkdir()
    git(path, "init", "-b", "session-test")
    commit = ("-c", "user.name=Hook Test", "-c", "user.email=hook@example.invalid",
              "-c", "core.hooksPath=/dev/null", "commit", "--allow-empty", "-m")
    git(path, *commit, "base")
    base = git(path, "rev-parse", "HEAD")
    for i in range(ahead):
        git(path, *commit, f"upstream {i}")
    git(path, "update-ref", "refs/remotes/origin/main", git(path, "rev-parse", "HEAD"))
    git(path, "reset", "--hard", base)
    # No remote is configured: fetch fails locally without network access.
    return path


def run_hook(monkeypatch, capsys, cwd, stdin):
    monkeypatch.chdir(cwd)
    monkeypatch.setattr("sys.stdin", io.StringIO(stdin))
    assert hook.main() == 0
    captured = capsys.readouterr()
    assert captured.err == ""
    return captured.out


def assert_checkout(output, repo):
    assert output.splitlines()[0].startswith(
        f"[base check] {git(repo, 'rev-parse', '--show-toplevel')} on session-test: "
    )


def test_stdin_checkout_overrides_process_checkout(tmp_path, monkeypatch, capsys):
    repo_a = make_repo(tmp_path / "repo-a", ahead=2)
    repo_b = make_repo(tmp_path / "repo-b", ahead=4)
    output = run_hook(monkeypatch, capsys, repo_b, json.dumps({"cwd": str(repo_a)}))
    assert_checkout(output, repo_a)
    assert "2 commit(s) AHEAD" in output
    assert "4 commit(s) AHEAD" not in output


def test_up_to_date_names_checkout_and_branch(tmp_path, monkeypatch, capsys):
    repo = make_repo(tmp_path / "repo")
    output = run_hook(monkeypatch, capsys, repo, json.dumps({"cwd": str(repo)}))
    assert_checkout(output, repo)
    assert "up to date with this branch's merge-base" in output


def test_counts_upstream_commits(tmp_path, monkeypatch, capsys):
    repo = make_repo(tmp_path / "repo", ahead=3)
    output = run_hook(monkeypatch, capsys, repo, json.dumps({"cwd": str(repo)}))
    assert_checkout(output, repo)
    assert "3 commit(s) AHEAD" in output


@pytest.mark.parametrize("stdin", ["", "not json", "[]", "null", '{}',
                                  '{"cwd": 42}', '{"cwd": "missing-directory"}'])
def test_invalid_input_falls_back_to_process_checkout(tmp_path, monkeypatch, capsys, stdin):
    repo = make_repo(tmp_path / "repo")
    output = run_hook(monkeypatch, capsys, repo, stdin)
    assert_checkout(output, repo)
    assert "up to date" in output


def test_detached_head_still_reports(tmp_path, monkeypatch, capsys):
    repo = make_repo(tmp_path / "repo", ahead=1)
    git(repo, "checkout", "--detach", "HEAD")
    output = run_hook(monkeypatch, capsys, repo, json.dumps({"cwd": str(repo)}))
    assert output.splitlines()[0].startswith(
        f"[base check] {git(repo, 'rev-parse', '--show-toplevel')} on detached HEAD: ")
    assert "1 commit(s) AHEAD" in output


def test_non_repository_fails_silent(tmp_path, monkeypatch, capsys):
    assert run_hook(monkeypatch, capsys, tmp_path, json.dumps({"cwd": str(tmp_path)})) == ""
