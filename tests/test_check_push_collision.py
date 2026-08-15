"""Push-collision gate: SESSIONS append-only exemption.

Two concurrent PRs each adding a new top SESSIONS entry is the designed
``merge=union`` case — not the 2026-07-24 CLAUDE/STATE contradiction class.
``check_push_collision`` must not demand FIRST_PASSAGE_ALLOW_PUSH_COLLISION=1
for that shape. Mutating a heading that already existed on the merge-base
still collides.
"""
from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def _load():
    spec = importlib.util.spec_from_file_location(
        "check_push_collision", REPO / "scripts" / "check_push_collision.py"
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


PUSH = _load()

needs_git = pytest.mark.skipif(
    shutil.which("git") is None, reason="git not on PATH"
)

SESSIONS_HEADER = (
    "# Session Log\n\nNewest first.\n\n---\n\n"
)


def _entry(date_str: str, title: str) -> str:
    return (
        f"## {date_str} — {title}\n"
        f"**Focus:** focus for {title}.\n"
        f"**Shipped:** shipped for {title}.\n"
    )


def _doc(entries: list[tuple[str, str]]) -> str:
    return SESSIONS_HEADER + "\n\n---\n\n".join(
        _entry(d, t) for d, t in entries
    ) + "\n"


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
    _write(root, "docs/SESSIONS.md", _doc([("2026-08-13w", "older")]))
    _write(root, "CLAUDE.md", "base claude\n")
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
def test_append_only_sessions_both_sides_does_not_collide(tmp_path: Path):
    """Two new top entries (ours + theirs) — union's designed merge; must pass."""
    _seed_repo(tmp_path)
    _git(tmp_path, "checkout", "-q", "-b", "feature")
    _write(
        tmp_path,
        "docs/SESSIONS.md",
        _doc([("2026-08-13z", "ours"), ("2026-08-13w", "older")]),
    )
    _commit(tmp_path, "ours session")

    _git(tmp_path, "checkout", "-q", "main")
    _write(
        tmp_path,
        "docs/SESSIONS.md",
        _doc([("2026-08-13y", "theirs"), ("2026-08-13w", "older")]),
    )
    _commit(tmp_path, "theirs session")
    _git(tmp_path, "update-ref", "refs/remotes/origin/main", "main")
    _git(tmp_path, "checkout", "-q", "feature")

    result = _run_gate(tmp_path)
    assert result.returncode == 0, result.stderr
    assert "docs/SESSIONS.md" not in result.stderr


@needs_git
def test_mutated_prior_sessions_entry_still_collides(tmp_path: Path):
    """Editing an origin/main heading is still the contradiction class."""
    _seed_repo(tmp_path)
    _git(tmp_path, "checkout", "-q", "-b", "feature")
    mutated = _doc([("2026-08-13z", "ours"), ("2026-08-13w", "older")])
    mutated = mutated.replace("shipped for older", "shipped for older — ours rewrite")
    _write(tmp_path, "docs/SESSIONS.md", mutated)
    _commit(tmp_path, "ours mutated prior")

    _git(tmp_path, "checkout", "-q", "main")
    _write(
        tmp_path,
        "docs/SESSIONS.md",
        _doc([("2026-08-13y", "theirs"), ("2026-08-13w", "older")]),
    )
    _commit(tmp_path, "theirs session")
    _git(tmp_path, "update-ref", "refs/remotes/origin/main", "main")
    _git(tmp_path, "checkout", "-q", "feature")

    result = _run_gate(tmp_path)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "docs/SESSIONS.md" in result.stderr


@needs_git
def test_sessions_exemption_does_not_mask_claude_collision(tmp_path: Path):
    _seed_repo(tmp_path)
    _git(tmp_path, "checkout", "-q", "-b", "feature")
    _write(
        tmp_path,
        "docs/SESSIONS.md",
        _doc([("2026-08-13z", "ours"), ("2026-08-13w", "older")]),
    )
    _write(tmp_path, "CLAUDE.md", "ours claude\n")
    _commit(tmp_path, "ours session + claude")

    _git(tmp_path, "checkout", "-q", "main")
    _write(
        tmp_path,
        "docs/SESSIONS.md",
        _doc([("2026-08-13y", "theirs"), ("2026-08-13w", "older")]),
    )
    _write(tmp_path, "CLAUDE.md", "theirs claude\n")
    _commit(tmp_path, "theirs session + claude")
    _git(tmp_path, "update-ref", "refs/remotes/origin/main", "main")
    _git(tmp_path, "checkout", "-q", "feature")

    result = _run_gate(tmp_path)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "CLAUDE.md" in result.stderr
    assert "docs/SESSIONS.md" not in result.stderr
