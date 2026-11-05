"""Push-collision gate: a governance path changed on both sides collides.

SESSIONS.md and its append-only exemption went in the 2026-11 governance cut.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]

needs_git = pytest.mark.skipif(
    shutil.which("git") is None, reason="git not on PATH"
)


def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = "2026-08-13T12:00:00+00:00"
    env.pop("FIRST_PASSAGE_ALLOW_PUSH_COLLISION", None)
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=check,
        env=env,
        capture_output=True,
        text=True,
    )


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _commit(root: Path, msg: str) -> None:
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", msg)


def _seed_repo(root: Path) -> None:
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _write(root, "README.md", "base readme\n")
    _write(root, "AGENTS.md", "base claude\n")
    _commit(root, "base")


def _run_gate(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "check_push_collision.py"),
            "--no-fetch",
            "--base",
            "origin/main",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        env={k: v for k, v in os.environ.items()
             if k != "FIRST_PASSAGE_ALLOW_PUSH_COLLISION"},
    )


@needs_git
def test_agents_md_changed_on_both_sides_collides(tmp_path: Path):
    _seed_repo(tmp_path)
    _git(tmp_path, "checkout", "-q", "-b", "feature")
    _write(tmp_path, "AGENTS.md", "ours claude\n")
    _commit(tmp_path, "ours claude")

    _git(tmp_path, "checkout", "-q", "main")
    _write(tmp_path, "AGENTS.md", "theirs claude\n")
    _commit(tmp_path, "theirs claude")
    _git(tmp_path, "update-ref", "refs/remotes/origin/main", "main")
    _git(tmp_path, "checkout", "-q", "feature")

    result = _run_gate(tmp_path)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "AGENTS.md" in result.stderr


@needs_git
def test_non_governance_path_on_both_sides_does_not_collide(tmp_path: Path):
    _seed_repo(tmp_path)
    _git(tmp_path, "checkout", "-q", "-b", "feature")
    _write(tmp_path, "README.md", "ours readme\n")
    _commit(tmp_path, "ours readme")

    _git(tmp_path, "checkout", "-q", "main")
    _write(tmp_path, "README.md", "theirs readme\n")
    _commit(tmp_path, "theirs readme")
    _git(tmp_path, "update-ref", "refs/remotes/origin/main", "main")
    _git(tmp_path, "checkout", "-q", "feature")

    result = _run_gate(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
