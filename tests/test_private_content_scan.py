"""Tests for scripts/private_content_scan.py — in-memory needle scan of a commit range.

Campaign-state §47b step 6b (2026-09-04): the pre-push scan builds needles in
memory from private files, scans ADDED lines and commit messages only, reports
locations never tokens, walks trees for forbidden paths, and exits 3 rather than
"clean" when a needle source is missing or a class is empty.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SCRIPT = _REPO / "scripts" / "private_content_scan.py"

needs_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not on PATH")

_JSON = '{"strategy_id": "x", "inputs": {"Alpha Length": 3, "Mode": "Aggressive", "Threshold": 1.25, "Enabled": true}}\n'
_CSV = "Trade #,Type,Date/Time,Price,P&L\n1,Long,2026-03-12 09:35,41237.5,312.50\n2,Short,2026-03-13 10:05,41190.25,-88.00\n"


def _git(root: Path, *args: str) -> str:
    env = dict(os.environ)
    env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = "2026-09-04T12:00:00+00:00"
    env.setdefault("GIT_AUTHOR_NAME", "t")
    env.setdefault("GIT_AUTHOR_EMAIL", "t@example.invalid")
    env.setdefault("GIT_COMMITTER_NAME", "t")
    env.setdefault("GIT_COMMITTER_EMAIL", "t@example.invalid")
    return subprocess.run(["git", *args], cwd=root, check=True, env=env, capture_output=True, text=True).stdout


def _run(root: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(_SCRIPT), "--repo", str(root), "--range", "base..HEAD", *extra],
        capture_output=True,
        text=True,
    )


@pytest.fixture()
def repo(tmp_path: Path) -> tuple[Path, Path, Path]:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q", "-b", "main")
    (root / "notes.md").write_text("context line mentions Aggressive mode already\nsecond line\n", encoding="utf-8")
    _git(root, "add", "notes.md")
    _git(root, "commit", "-q", "-m", "base")
    _git(root, "branch", "base")
    private = tmp_path / "private"
    private.mkdir()
    snap = private / "x.json"
    snap.write_text(_JSON, encoding="utf-8")
    export = private / "x.csv"
    export.write_text(_CSV, encoding="utf-8")
    return root, snap, export


@needs_git
def test_clean_range_exits_zero(repo: tuple[Path, Path, Path]) -> None:
    root, snap, export = repo
    (root / "notes.md").write_text("context line mentions Aggressive mode already\nsecond line changed\n", encoding="utf-8")
    _git(root, "commit", "-q", "-am", "harmless edit")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 0, proc.stdout
    assert "SCAN result=CLEAN" in proc.stdout
    # the unchanged context line carrying "Aggressive" is not a hit
    assert "HIT" not in proc.stdout


@needs_git
def test_pair_in_added_line_and_cell_in_message_are_located_without_tokens(repo: tuple[Path, Path, Path]) -> None:
    root, snap, export = repo
    (root / "cfg.json").write_text('{"Mode": "Aggressive", "n": 1}\n', encoding="utf-8")
    _git(root, "add", "cfg.json")
    _git(root, "commit", "-q", "-m", "add cfg\n\nrow was 41237.5 at the time")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2, proc.stdout
    assert "HIT class=PAIR" in proc.stdout and "file=cfg.json line=1" in proc.stdout
    assert "HIT class=CELL" in proc.stdout and "file=<commit message>" in proc.stdout
    for token in ("Aggressive", "41237.5", "1.25", "Alpha Length"):
        assert token not in proc.stdout


@needs_git
def test_detached_trivial_scalar_is_not_a_needle_but_title_is(repo: tuple[Path, Path, Path]) -> None:
    root, snap, export = repo
    (root / "a.txt").write_text("value 3 and true appear here\n", encoding="utf-8")
    _git(root, "add", "a.txt")
    _git(root, "commit", "-q", "-m", "trivial scalars only")
    assert _run(root, "--json", str(snap), "--csv", str(export)).returncode == 0
    (root / "b.txt").write_text("we set Alpha Length on the chart\n", encoding="utf-8")
    _git(root, "add", "b.txt")
    _git(root, "commit", "-q", "-m", "title leak")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "HIT class=TITLE" in proc.stdout and "file=b.txt" in proc.stdout


@needs_git
def test_word_boundary_matching(repo: tuple[Path, Path, Path]) -> None:
    root, snap, export = repo
    (root / "c.txt").write_text("Aggressively is a different word; 141237.5 is a different number\n", encoding="utf-8")
    _git(root, "add", "c.txt")
    _git(root, "commit", "-q", "-m", "near misses")
    assert _run(root, "--json", str(snap), "--csv", str(export)).returncode == 0


@needs_git
def test_exclusions_drop_public_tokens(repo: tuple[Path, Path, Path], tmp_path: Path) -> None:
    root, snap, export = repo
    (root / "anchors.json").write_text('{"net": "312.50"}\n', encoding="utf-8")
    _git(root, "add", "anchors.json")
    _git(root, "commit", "-q", "-m", "canonical anchor value")
    assert _run(root, "--json", str(snap), "--csv", str(export)).returncode == 2
    excl = tmp_path / "public.txt"
    excl.write_text("312.50\n", encoding="utf-8")
    assert _run(root, "--json", str(snap), "--csv", str(export), "--exclude", str(excl)).returncode == 0


@needs_git
def test_missing_or_empty_needle_source_exits_three_never_clean(repo: tuple[Path, Path, Path], tmp_path: Path) -> None:
    root, snap, export = repo
    proc = _run(root, "--json", str(tmp_path / "absent.json"), "--csv", str(export))
    assert proc.returncode == 3 and "SCAN result=ERROR" in proc.stdout
    empty = tmp_path / "empty.json"
    empty.write_text('{"inputs": {}}\n', encoding="utf-8")
    assert _run(root, "--json", str(empty), "--csv", str(export)).returncode == 3
    header_only = tmp_path / "h.csv"
    header_only.write_text("a,b\n", encoding="utf-8")
    assert _run(root, "--json", str(snap), "--csv", str(header_only)).returncode == 3
    assert _run(root).returncode == 3


@needs_git
def test_path_scan_flags_private_dir_and_forbidden_suffix_in_history(repo: tuple[Path, Path, Path]) -> None:
    root, snap, export = repo
    (root / "inputs" / "private_overrides").mkdir(parents=True)
    (root / "inputs" / "private_overrides" / "p.json").write_text("{}\n", encoding="utf-8")
    _git(root, "add", "-f", "inputs/private_overrides/p.json")
    _git(root, "commit", "-q", "-m", "oops")
    _git(root, "rm", "-q", "inputs/private_overrides/p.json")
    _git(root, "commit", "-q", "-m", "removed again")
    proc = _run(root, "--json", str(snap), "--csv", str(export), "--path-prefix", "inputs/private_overrides/")
    assert proc.returncode == 2 and "HIT class=PATH" in proc.stdout and "inputs/private_overrides/p.json" in proc.stdout
    (root / "data.csv").write_text("h\n1\n", encoding="utf-8")
    _git(root, "add", "data.csv")
    _git(root, "commit", "-q", "-m", "csv added")
    proc = _run(root, "--json", str(snap), "--csv", str(export), "--forbid-suffix", ".csv")
    assert proc.returncode == 2 and "file=data.csv" in proc.stdout


@needs_git
def test_bad_range_exits_four(repo: tuple[Path, Path, Path]) -> None:
    root, snap, export = repo
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--repo", str(root), "--range", "nope..HEAD", "--json", str(snap), "--csv", str(export)],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 4 and "SCAN result=ERROR" in proc.stdout
