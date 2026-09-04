"""Tests for scripts/repo_hygiene.py — FileNotFoundError guard on _run.

Packet C of the 2026-09-04 scripts-side fleet: a missing optional binary
(typically ``gh``) must degrade to returncode 127, not raise.
"""
from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_PATH = _REPO / "scripts" / "repo_hygiene.py"
_spec = importlib.util.spec_from_file_location("repo_hygiene", _PATH)
rh = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = rh
_spec.loader.exec_module(rh)

needs_git = pytest.mark.skipif(
    shutil.which("git") is None, reason="git not on PATH"
)


def _git(root: Path, *args: str) -> None:
    env = dict(os.environ)
    env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = "2026-09-04T12:00:00+00:00"
    subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _seed_repo(root: Path) -> None:
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    (root / "README.md").write_text("seed\n", encoding="utf-8")
    _git(root, "add", "README.md")
    _git(root, "commit", "-q", "-m", "seed")


@needs_git
def test_build_report_without_gh_sets_unavailable(tmp_path, monkeypatch):
    _seed_repo(tmp_path)

    real_run = subprocess.run

    def _run_without_gh(args, *a, **kw):
        if args and args[0] == "gh":
            raise FileNotFoundError(args[0])
        return real_run(args, *a, **kw)

    monkeypatch.setattr(rh, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(rh.subprocess, "run", _run_without_gh)

    report = rh.build_report()
    assert report.gh_available is False
    assert any("gh not on PATH" in w for w in report.warnings)


def test_run_missing_binary_returns_127():
    proc = rh._run(["definitely-not-a-binary-xyz"])
    assert proc.returncode == 127
    assert proc.stdout == ""
    assert proc.stderr == "definitely-not-a-binary-xyz: not found"
