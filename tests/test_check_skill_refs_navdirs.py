"""Nav-dir + tombstone + references-warn coverage for check_skill_refs.

Companion to tests/test_check_skill_refs.py — pins the 2026-07-24 gate-estate
repairs (Algorithm brief #3): ops/core/lab/scripts join REPO_NAV_DIRS;
tombstone markers exempt deliberate dead cites; references/*.md warn-only.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_CSR_PATH = Path(__file__).resolve().parent.parent / "scripts" / "check_skill_refs.py"
_spec = importlib.util.spec_from_file_location("check_skill_refs", _CSR_PATH)
csr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(csr)


def _make_skill(skills_root: Path, name: str, body: str) -> Path:
    d = skills_root / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(body, encoding="utf-8")
    return d


def test_ops_dead_ref_fails(tmp_path):
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    _make_skill(skills, "opsdead", "See `ops/does_not_exist.py`.\n")
    bad = csr.check_all(repo)
    assert any(ref == "ops/does_not_exist.py" for _, ref in bad), bad


def test_core_dead_ref_fails(tmp_path):
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    _make_skill(skills, "coredead", "See `core/does_not_exist.py`.\n")
    bad = csr.check_all(repo)
    assert any(ref == "core/does_not_exist.py" for _, ref in bad), bad


def test_lab_and_scripts_dead_refs_fail(tmp_path):
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    _make_skill(
        skills, "both",
        "See `lab/gone.py` and `scripts/gone.py`.\n",
    )
    bad = {ref for _, ref in csr.check_all(repo)}
    assert "lab/gone.py" in bad
    assert "scripts/gone.py" in bad


def test_vendor_subtree_exemption_still_passes(tmp_path):
    # Waiver requires the parent feed directory to still exist (S-22).
    repo = tmp_path
    (repo / "data" / "tv_exports" / "pepperstone").mkdir(parents=True)
    (repo / "core" / "data" / "bar_data").mkdir(parents=True)
    skills = repo / ".claude" / "skills"
    _make_skill(
        skills, "vendor",
        "Legacy `data/tv_exports/pepperstone/a.csv` and "
        "monorepo `core/data/bar_data/x.csv` are gitignored.\n",
    )
    assert csr.check_all(repo) == []


def test_tombstone_marked_dead_path_passes(tmp_path):
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    _make_skill(
        skills, "tomb",
        "The spine (`ops/accounts.py` (deleted) + CLI) is gone.\n"
        "Also `core/old.py` (retired) stays as prose.\n",
    )
    assert csr.check_all(repo) == []


def test_unmarked_dead_path_still_fails(tmp_path):
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    _make_skill(
        skills, "notomb",
        "Still cites `ops/accounts.py` without a marker.\n",
    )
    bad = csr.check_all(repo)
    assert any(ref == "ops/accounts.py" for _, ref in bad), bad


def test_references_md_dead_link_warns_without_failing(tmp_path, capsys):
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    d = _make_skill(skills, "withrefs", "SKILL is clean — see `docs/rule_0.md`.\n")
    (repo / "docs").mkdir()
    (repo / "docs" / "rule_0.md").write_text("x", encoding="utf-8")
    refs = d / "references"
    refs.mkdir()
    (refs / "notes.md").write_text(
        "Historical cite `ops/missing_from_refs.py`.\n", encoding="utf-8",
    )

    rc = csr.main(["--all", "--repo-root", str(repo)])
    assert rc == 0
    err = capsys.readouterr().err
    assert "ops/missing_from_refs.py" in err
    assert "WARN" in err


def test_skill_relative_scripts_still_resolve(tmp_path):
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    d = _make_skill(skills, "bundled", "Runs `scripts/helper.py`.\n")
    (d / "scripts").mkdir()
    (d / "scripts" / "helper.py").write_text("# ok\n", encoding="utf-8")
    assert csr.check_all(repo) == []


def test_repo_nav_dirs_include_four_new_prefixes():
    for d in ("ops/", "core/", "lab/", "scripts/"):
        assert d in csr.REPO_NAV_DIRS
