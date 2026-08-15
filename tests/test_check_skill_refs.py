"""Tests for scripts/check_skill_refs.py — the skill path-reference linter.

The linter parses each `.claude/skills/*/SKILL.md` for repo-relative path
references (markdown links + inline-code paths), resolves them, and fails on
any that don't exist.

Test (c) — `--all` against the real migrated skills — also serves as a
migration smoke test: a green run means the 8 migrated keepers + 2 data skills
left no dead repo-path references behind.
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


def test_good_ref_passes(tmp_path):
    # repo with a real file the skill points at
    repo = tmp_path
    (repo / "docs").mkdir()
    (repo / "docs" / "rule_0.md").write_text("x", encoding="utf-8")
    skills = repo / ".claude" / "skills"
    _make_skill(skills, "good", "See `docs/rule_0.md` for the rule.\n")

    bad = csr.check_all(repo)
    assert bad == [], bad


def test_broken_ref_fails(tmp_path):
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    _make_skill(skills, "bad", "See `docs/does_not_exist.md` for the rule.\n")

    bad = csr.check_all(repo)
    assert any("docs/does_not_exist.md" in ref for (_, ref) in bad), bad


def test_main_broken_exits_1(tmp_path, capsys):
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    _make_skill(skills, "bad", "Broken `docs/adr/nope.md` here.\n")

    rc = csr.main(["--all", "--repo-root", str(repo)])
    assert rc == 1
    out = capsys.readouterr().out
    assert "docs/adr/nope.md" in out
    assert "bad" in out  # which skill


def test_skill_asset_ref_not_hard_failed(tmp_path):
    # A skill may reference a bundled references/ asset it hasn't authored yet
    # — that is its own forward contract, not repo rot, and must NOT hard-fail.
    # (scripts/ is dual-homed into REPO_NAV as of the 2026-07-24 gate-estate
    # repair: missing scripts/ cites hard-fail; present skill-local scripts/
    # still resolve — see test_check_skill_refs_navdirs.)
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    _make_skill(
        skills, "promises",
        "Ships `references/adr.md` (not yet here).\n",
    )
    bad = csr.check_all(repo)
    assert bad == [], bad


def test_missing_scripts_cite_hard_fails(tmp_path):
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    _make_skill(
        skills, "promises_script",
        "Promises `scripts/check_brief.py` but has not landed it.\n",
    )
    bad = csr.check_all(repo)
    assert any(ref == "scripts/check_brief.py" for _, ref in bad), bad


def test_bare_directory_ref_skipped(tmp_path):
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    _make_skill(skills, "dirs", "Artifacts live in `docs/briefs/locks/`.\n")
    bad = csr.check_all(repo)
    assert bad == [], bad


def test_main_good_exits_0(tmp_path):
    repo = tmp_path
    (repo / "config").mkdir()
    (repo / "config" / "params.toml").write_text("x", encoding="utf-8")
    skills = repo / ".claude" / "skills"
    _make_skill(skills, "ok", "Points at `config/params.toml`.\n")

    rc = csr.main(["--all", "--repo-root", str(repo)])
    assert rc == 0


def test_skill_relative_reference_resolves(tmp_path):
    # `references/foo.md` should resolve relative to the skill dir, not repo root.
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    d = _make_skill(skills, "withrefs", "See `references/foo.md`.\n")
    (d / "references").mkdir()
    (d / "references" / "foo.md").write_text("x", encoding="utf-8")

    bad = csr.check_all(repo)
    assert bad == [], bad


def test_urls_and_anchors_skipped(tmp_path):
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    _make_skill(
        skills, "urls",
        "[link](https://www.notion.so/abc) and [a](#section) and `not/a/real`.\n",
    )
    bad = csr.check_all(repo)
    # https URL and #anchor are skipped; `not/a/real` has no known top-level
    # prefix and no known extension, so it is not treated as a repo path.
    assert bad == [], bad


def test_placeholder_paths_skipped(tmp_path):
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    _make_skill(
        skills, "ph",
        "Write to `docs/methodology/gate_audits/YYYY-MM-DD_<slug>.md`.\n",
    )
    bad = csr.check_all(repo)
    assert bad == [], bad


def test_ellipsis_and_bracket_templates_skipped(tmp_path):
    """Prose ellipsis + `[placeholder]` templates are not real paths."""
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    d = _make_skill(skills, "tmpl", "SKILL body.\n")
    refs = d / "references"
    refs.mkdir()
    (refs / "note.md").write_text(
        "Cite `data/...` and "
        "`data/backtests/[strategy]_v[X.Y]_x.csv` and "
        "`data/mc/[panel-name].csv`.\n",
        encoding="utf-8",
    )
    warns = csr.check_skill_references_warn(repo, "tmpl")
    assert warns == [], warns
    assert csr.check_all(repo) == []


def test_line_suffix_stripped_before_resolve(tmp_path):
    repo = tmp_path
    (repo / "docs" / "adr").mkdir(parents=True)
    (repo / "docs" / "adr" / "foo.md").write_text("x", encoding="utf-8")
    skills = repo / ".claude" / "skills"
    _make_skill(skills, "lines", "Quoted in `docs/adr/foo.md:52`.\n")
    assert csr.check_all(repo) == []


def test_gitignored_pine_waived(tmp_path):
    """`**/*.pine` citations are correct; bytes are intentionally absent."""
    repo = tmp_path
    (repo / ".gitignore").write_text("**/*.pine\n", encoding="utf-8")
    skills = repo / ".claude" / "skills"
    _make_skill(
        skills, "pine",
        "Read `core/strategies/aegis/aegis_usdjpy_v4.3.pine` for the header.\n",
    )
    # No git repo → pattern fallback from reading .gitignore.
    assert csr.check_all(repo) == []
    # With git check-ignore available too.
    import subprocess
    subprocess.run(
        ["git", "init"], cwd=repo, check=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    csr._gitignore_patterns.cache_clear()
    assert csr.check_all(repo) == []


def test_gitignore_does_not_waive_unignored_dead_path(tmp_path):
    repo = tmp_path
    (repo / ".gitignore").write_text("**/*.pine\n", encoding="utf-8")
    skills = repo / ".claude" / "skills"
    _make_skill(skills, "dead", "See `docs/adr/missing.md`.\n")
    bad = csr.check_all(repo)
    assert any("docs/adr/missing.md" in ref for _, ref in bad), bad


def test_single_skill_mode(tmp_path):
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    _make_skill(skills, "a", "Broken `docs/missing_a.md`.\n")
    _make_skill(skills, "b", "Broken `docs/missing_b.md`.\n")

    rc = csr.main(["--skill", "a", "--repo-root", str(repo)])
    assert rc == 1
    # only skill a is checked
    bad = csr.check_skill(repo, "a")
    assert any("missing_a" in ref for _, ref in bad)
    assert not any("missing_b" in ref for _, ref in bad)


def test_vendor_data_ref_waived_when_parent_dir_exists(tmp_path):
    # Gitignored vendor CSVs are absent on CI / fresh clones; waive only when the
    # parent tree still exists (live feed). Claim-alignment S-22.
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    (repo / "data" / "tv_exports" / "cme").mkdir(parents=True)
    _make_skill(
        skills, "vendor",
        "A CSV at `data/tv_exports/cme/aegis.csv` is not provenance.\n",
    )
    bad = csr.check_all(repo)
    assert bad == [], bad


def test_vendor_data_ref_hard_fails_when_parent_tree_gone(tmp_path):
    # Retired feed: parent directory absent → hard-fail (not blanket waive).
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    (repo / "data" / "tv_exports").mkdir(parents=True)  # pepperstone/ absent
    _make_skill(
        skills, "vendor",
        "A CSV at `data/tv_exports/pepperstone/aegis.csv` is not provenance.\n",
    )
    bad = csr.check_all(repo)
    assert any("pepperstone" in ref for _, ref in bad), bad


def test_glob_zero_matches_hard_fails(tmp_path):
    repo = tmp_path
    skills = repo / ".claude" / "skills"
    (repo / "core" / "strategies").mkdir(parents=True)
    _make_skill(
        skills, "globskill",
        "Locks live at `core/strategies/*/LOCK.md`.\n",
    )
    bad = csr.check_all(repo)
    assert any("glob cites no existing path" in ref for _, ref in bad), bad


def test_all_against_real_migrated_skills():
    """Migration smoke test: the real repo's skills must have zero dead refs."""
    repo = Path(__file__).resolve().parent.parent
    bad = csr.check_all(repo)
    assert bad == [], f"dead refs in real skills: {bad}"


def test_real_skill_references_warn_clean():
    """references/*.md warn inventory must stay empty after Class-1/2/3 triage."""
    repo = Path(__file__).resolve().parent.parent
    warns = csr.check_all_references_warn(repo)
    assert warns == [], f"warn-only refs still open: {warns}"
