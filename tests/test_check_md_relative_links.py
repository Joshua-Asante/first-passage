"""Unit tests for scripts/check_md_relative_links.py — file-relative link scan."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_PATH = REPO_ROOT / "scripts" / "check_md_relative_links.py"
_spec = importlib.util.spec_from_file_location("check_md_relative_links", _PATH)
cml = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cml)


def test_file_relative_miss_is_flagged(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    sessions = docs / "SESSIONS.md"
    sessions.write_text(
        "see [adr](docs/adr/missing.md)\n",
        encoding="utf-8",
    )
    misses = cml.check_file(sessions, tmp_path)
    assert any("docs/adr/missing.md" in m for m in misses), misses


def test_nested_relative_hit_resolves(tmp_path):
    docs = tmp_path / "docs"
    adr = docs / "adr"
    adr.mkdir(parents=True)
    target = adr / "ok.md"
    target.write_text("# ok\n", encoding="utf-8")
    sessions = docs / "SESSIONS.md"
    sessions.write_text("see [adr](adr/ok.md)\n", encoding="utf-8")
    assert cml.check_file(sessions, tmp_path) == []


def test_repo_root_shaped_href_from_nested_doc_is_a_miss(tmp_path):
    """The motivating bug: ](docs/adr/x) inside docs/ looks like docs/docs/adr/x."""
    docs = tmp_path / "docs"
    adr = docs / "adr"
    adr.mkdir(parents=True)
    (adr / "x.md").write_text("# x\n", encoding="utf-8")
    sessions = docs / "SESSIONS.md"
    sessions.write_text("see [x](docs/adr/x.md)\n", encoding="utf-8")
    misses = cml.check_file(sessions, tmp_path)
    assert len(misses) == 1, misses


def test_warn_only_cli_exits_zero_with_misses(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "SESSIONS.md").write_text("[x](nope.md)\n", encoding="utf-8")
    r = subprocess.run(
        [sys.executable, str(_PATH), "--repo-root", str(tmp_path), "--glob", "docs/**/*.md"],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "WARN:" in r.stdout
    assert "unresolved" in r.stdout


def test_strict_cli_exits_nonzero_with_misses(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "SESSIONS.md").write_text("[x](nope.md)\n", encoding="utf-8")
    r = subprocess.run(
        [
            sys.executable,
            str(_PATH),
            "--repo-root",
            str(tmp_path),
            "--glob",
            "docs/**/*.md",
            "--strict",
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 1, r.stdout + r.stderr
