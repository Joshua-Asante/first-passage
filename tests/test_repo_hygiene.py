"""Tests for scripts/repo_hygiene.py — gh probe degrades; git stays required.

Packet C of the 2026-09-04 scripts-side fleet: a missing optional ``gh`` must
set ``gh_available`` False. A missing ``git`` must still raise.
"""
from __future__ import annotations

import importlib.util
import json
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


@needs_git
def test_build_report_without_git_raises(tmp_path, monkeypatch):
    _seed_repo(tmp_path)

    real_run = subprocess.run

    def _run_without_git(args, *a, **kw):
        if args and args[0] == "git":
            raise FileNotFoundError(args[0])
        return real_run(args, *a, **kw)

    monkeypatch.setattr(rh, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(rh.subprocess, "run", _run_without_git)

    with pytest.raises(FileNotFoundError):
        rh.build_report()


@needs_git
def test_private_entries_lists_ignored_files_but_not_regenerable_caches(tmp_path):
    """M-41: `git worktree remove` deletes ignored files without asking, so the
    scout names every ignored entry a fresh setup would not regenerate."""
    _seed_repo(tmp_path)
    (tmp_path / ".gitignore").write_text("*.csv\n*.pine\n__pycache__/\n.venv/\n", encoding="utf-8")
    (tmp_path / "evidence.csv").write_text("x\n", encoding="utf-8")
    (tmp_path / "book").mkdir()
    (tmp_path / "book" / "edge.pine").write_text("x\n", encoding="utf-8")
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "m.pyc").write_bytes(b"x")
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "pyvenv.cfg").write_text("x\n", encoding="utf-8")
    # git collapses a directory holding only ignored files into one entry
    assert rh._scan_worktree(str(tmp_path))[1] == ["book/", "evidence.csv"]


def _linked_worktree(root: Path, name: str = "wt") -> Path:
    path = root / ".claude" / "worktrees" / name
    _git(root, "worktree", "add", "-q", "-b", f"topic-{name}", str(path))
    return path


def _same(a: str | Path, b: str | Path) -> bool:
    return Path(a).resolve() == Path(b).resolve()


@needs_git
def test_report_from_linked_worktree_finds_true_primary_and_orphans(tmp_path, monkeypatch):
    """Sessions run in linked worktrees: the script's own checkout is not the primary."""
    _seed_repo(tmp_path)
    linked = _linked_worktree(tmp_path)
    orphan = tmp_path / ".claude" / "worktrees" / "orphan"
    orphan.mkdir()
    (linked / ".gitignore").write_text("*.csv\n", encoding="utf-8")
    (linked / "evidence.csv").write_text("x\n", encoding="utf-8")
    monkeypatch.setattr(rh, "REPO_ROOT", linked)

    report = rh.build_report()

    primary = [wt for wt in report.worktrees if wt.is_primary]
    assert len(primary) == 1 and _same(primary[0].path, tmp_path)
    assert report.primary_branch == "main"
    assert [Path(p).name for p in report.orphan_worktree_dirs] == ["orphan"]
    row = next(wt for wt in report.worktrees if not wt.is_primary)
    assert _same(row.path, linked) and row.private == ["evidence.csv"]


@needs_git
def test_scan_states_clean_dirty_and_ignored_only(tmp_path):
    _seed_repo(tmp_path)
    assert rh._scan_worktree(str(tmp_path)) == ("clean", [])
    (tmp_path / ".gitignore").write_text("*.csv\n", encoding="utf-8")
    _git(tmp_path, "add", ".gitignore")
    _git(tmp_path, "commit", "-q", "-m", "ignore")
    (tmp_path / "evidence.csv").write_text("x\n", encoding="utf-8")
    assert rh._scan_worktree(str(tmp_path)) == ("clean", ["evidence.csv"])
    (tmp_path / "new.txt").write_text("x\n", encoding="utf-8")
    assert rh._scan_worktree(str(tmp_path)) == ("dirty", ["evidence.csv"])
    _git(tmp_path, "config", "status.showUntrackedFiles", "no")
    assert rh._scan_worktree(str(tmp_path)) == ("dirty", ["evidence.csv"])


def test_scan_failure_is_unknown_not_empty(tmp_path, monkeypatch):
    """A failed scan must never read as "nothing private" (M-41)."""
    assert rh._scan_worktree(str(tmp_path / "missing"))[0] == "unknown"
    monkeypatch.setattr(
        rh, "_run", lambda *a, **k: subprocess.CompletedProcess(a, 128, "", "fatal")
    )
    assert rh._scan_worktree(str(tmp_path)) == ("unknown", [])


@needs_git
def test_unscannable_worktree_is_warned(tmp_path, monkeypatch):
    _seed_repo(tmp_path)
    linked = _linked_worktree(tmp_path)
    monkeypatch.setattr(rh, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        rh, "_scan_worktree", lambda path: ("unknown", [])
    )
    report = rh.build_report()
    row = next(wt for wt in report.worktrees if not wt.is_primary)
    assert row.state == "unknown"
    assert any("Could not scan" in w and linked.name in w for w in report.warnings)


def _tip(root: Path, ref: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", ref], cwd=root, check=True, capture_output=True, text=True
    ).stdout.strip()


def _branch_with_commit(root: Path, name: str) -> str:
    _git(root, "checkout", "-q", "-b", name, "main")
    (root / f"{name}.txt").write_text("x\n", encoding="utf-8")
    _git(root, "add", f"{name}.txt")
    _git(root, "commit", "-q", "-m", name)
    _git(root, "checkout", "-q", "main")
    return _tip(root, name)


def _fake_gh(monkeypatch, prs: list[dict]) -> list[list[str]]:
    real_run = subprocess.run
    calls: list[list[str]] = []

    def _run(args, *a, **kw):
        if args[:3] == ["gh", "pr", "list"]:
            calls.append(args)
            return subprocess.CompletedProcess(args, 0, json.dumps(prs), "")
        if args[:2] == ["gh", "--version"]:
            return subprocess.CompletedProcess(args, 0, "gh", "")
        return real_run(args, *a, **kw)

    monkeypatch.setattr(rh.subprocess, "run", _run)
    return calls


@needs_git
def test_squash_candidate_needs_tip_match_and_gets_named_hint(tmp_path, monkeypatch):
    _seed_repo(tmp_path)
    _git(tmp_path, "update-ref", "refs/remotes/origin/main", "main")
    _git(tmp_path, "branch", "ancestor", "main")
    squashed = _branch_with_commit(tmp_path, "squashed")
    reused = _branch_with_commit(tmp_path, "reused")
    _branch_with_commit(tmp_path, "drifted")
    prs = [
        {"number": 1, "headRefName": "squashed", "headRefOid": squashed, "url": "u1"},
        {"number": 2, "headRefName": "drifted", "headRefOid": "0" * 40, "url": "u2"},
        {"number": 3, "headRefName": "reused", "headRefOid": "1" * 40, "url": "u3"},
        {"number": 4, "headRefName": "reused", "headRefOid": reused, "url": "u4"},
        {"number": 5, "headRefName": "ancestor", "headRefOid": "2" * 40, "url": "u5"},
    ]
    _fake_gh(monkeypatch, prs)
    monkeypatch.setattr(rh, "REPO_ROOT", tmp_path)

    report = rh.build_report()

    rows = {r.name: r for r in report.merged_local_branches}
    assert set(rows) == {"ancestor", "reused", "squashed"}
    assert rows["ancestor"].safe_delete_hint.startswith("git branch -d ancestor")
    assert rows["squashed"].safe_delete_hint.startswith("git branch -D squashed")
    assert "#4" in rows["reused"].pr
    assert [r.name for r in report.diverged_merged_branches] == ["drifted"]


@needs_git
def test_checked_out_drifted_branch_is_not_listed(tmp_path, monkeypatch):
    _seed_repo(tmp_path)
    _branch_with_commit(tmp_path, "drifted")
    _git(tmp_path, "checkout", "-q", "drifted")
    _fake_gh(
        monkeypatch,
        [{"number": 1, "headRefName": "drifted", "headRefOid": "0" * 40, "url": "u"}],
    )
    monkeypatch.setattr(rh, "REPO_ROOT", tmp_path)
    assert rh.build_report().diverged_merged_branches == []


@needs_git
def test_merged_pr_list_reaches_past_100_and_warns_at_limit(tmp_path, monkeypatch):
    _seed_repo(tmp_path)
    prs = [{"number": 1, "headRefName": "x", "headRefOid": "0" * 40, "url": "u"}]
    calls = _fake_gh(monkeypatch, prs)
    monkeypatch.setattr(rh, "REPO_ROOT", tmp_path)

    assert int(rh.GH_PR_LIMIT) > 100
    rh.build_report()
    assert calls[0][calls[0].index("--limit") + 1] == str(rh.GH_PR_LIMIT)

    monkeypatch.setattr(rh, "GH_PR_LIMIT", 1)
    assert any("older merged PRs" in w for w in rh.build_report().warnings)
