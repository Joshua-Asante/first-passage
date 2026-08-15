"""Tests for the Sentinel memory-base linter (Tier-2 memory hygiene).

The memory base lives OUTSIDE the repo (~/.claude/.../memory). `memory_scan`
takes the dir as a param and no-ops when absent, so the public repo + CI stay
clean. Checks: byte budget, index<->file bijection (both directions), broken
[[wikilinks]], and a conservative SoT-anchored stale-MC-anchor tripwire.
"""
from pathlib import Path

from sentinel.scan import memory_scan


def _mk(mem: Path, index_lines, files):
    mem.mkdir(parents=True, exist_ok=True)
    (mem / "MEMORY.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    for slug, body in files.items():
        (mem / f"{slug}.md").write_text(body, encoding="utf-8")


# --- no-op contract (public-clone / CI safe) ------------------------------- #

def test_memory_scan_noop_when_dir_none():
    assert memory_scan(None) == []


def test_memory_scan_noop_when_dir_missing(tmp_path):
    assert memory_scan(tmp_path / "does_not_exist") == []


def test_memory_scan_noop_when_no_index(tmp_path):
    mem = tmp_path / "memory"
    mem.mkdir()
    (mem / "a.md").write_text("orphan but no index file present", encoding="utf-8")
    assert memory_scan(mem) == []  # fail open: no MEMORY.md -> nothing to check


# --- clean base ------------------------------------------------------------ #

def test_memory_scan_clean_base_is_silent(tmp_path):
    mem = tmp_path / "memory"
    _mk(mem, ["- [A](a.md) — hook", "- [B](b.md) — hook"],
        {"a": "fact a", "b": "fact b links [[a]]"})
    assert memory_scan(mem) == []


# --- budget ---------------------------------------------------------------- #

def test_memory_scan_flags_budget_over(tmp_path):
    mem = tmp_path / "memory"
    mem.mkdir()
    big = "- [x](x.md) — " + ("y" * 200) + "\n"
    (mem / "MEMORY.md").write_text(big * 200, encoding="utf-8")  # ~43KB > 25KB
    (mem / "x.md").write_text("z", encoding="utf-8")
    assert "MEM-budget-over" in {f.id for f in memory_scan(mem)}


def test_memory_scan_budget_ok_is_silent(tmp_path):
    mem = tmp_path / "memory"
    _mk(mem, ["- [A](a.md) — hook"], {"a": "small"})
    assert all(f.id != "MEM-budget-over" for f in memory_scan(mem))


# --- bijection ------------------------------------------------------------- #

def test_memory_scan_flags_orphan_file(tmp_path):
    mem = tmp_path / "memory"
    _mk(mem, ["- [A](a.md) — hook"], {"a": "fa", "b": "on disk, no index line"})
    assert any(f.id == "MEM-orphan-file-b" for f in memory_scan(mem))


def test_memory_scan_flags_dangling_index(tmp_path):
    mem = tmp_path / "memory"
    _mk(mem, ["- [A](a.md) — hook", "- [Ghost](ghost.md) — hook"], {"a": "fa"})
    assert any(f.id == "MEM-dangling-index-ghost" for f in memory_scan(mem))


# --- broken wikilinks ------------------------------------------------------ #

def test_memory_scan_flags_broken_wikilink(tmp_path):
    mem = tmp_path / "memory"
    _mk(mem, ["- [A](a.md) — hook"], {"a": "see [[nonexistent_slug]]"})
    assert any(f.id == "MEM-broken-link-nonexistent_slug" for f in memory_scan(mem))


def test_memory_scan_findings_are_memory_routed(tmp_path):
    mem = tmp_path / "memory"
    _mk(mem, ["- [A](a.md) — hook"], {"a": "see [[gone]]", "b": "orphan"})
    fs = memory_scan(mem)
    assert fs and all(f.category == "memory" and f.routing in ("Action", "Forward") for f in fs)


# --- staleness tripwire (SoT-anchored, conservative) ----------------------- #

def test_memory_scan_flags_stale_anchor_without_marker(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "CLAUDE.md").write_text("current canonical 99.83/0.17/4.37 anchor\n", encoding="utf-8")
    mem = tmp_path / "memory"
    _mk(mem, ["- [Anc](anc.md) — hook"],
        {"anc": "This is the new canonical anchor 98.09/0.36/4.73 for the portfolio."})
    assert any(f.id == "MEM-stale-anchor-anc" for f in memory_scan(mem, repo_root=repo))


def test_memory_scan_stale_anchor_silent_with_historical_marker(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "CLAUDE.md").write_text("canonical 99.83/0.17/4.37 anchor\n", encoding="utf-8")
    mem = tmp_path / "memory"
    _mk(mem, ["- [Anc](anc.md) — hook"],
        {"anc": "HISTORICAL: the 2026-05-08 canonical anchor was 98.09/0.36/4.73 (SUPERSEDED)."})
    assert all(f.id != "MEM-stale-anchor-anc" for f in memory_scan(mem, repo_root=repo))


def test_memory_scan_stale_anchor_silent_when_matches_current(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "CLAUDE.md").write_text("canonical 99.83/0.17/4.37 anchor\n", encoding="utf-8")
    mem = tmp_path / "memory"
    _mk(mem, ["- [Anc](anc.md) — hook"],
        {"anc": "the current canonical anchor is 99.83/0.17/4.37."})
    assert all(not f.id.startswith("MEM-stale-anchor") for f in memory_scan(mem, repo_root=repo))


def test_memory_scan_no_staleness_without_repo_root(tmp_path):
    mem = tmp_path / "memory"
    _mk(mem, ["- [Anc](anc.md) — hook"],
        {"anc": "the new canonical anchor 98.09/0.36/4.73"})
    assert all(not f.id.startswith("MEM-stale-anchor") for f in memory_scan(mem))
