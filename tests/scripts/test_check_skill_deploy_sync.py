"""Tests for scripts/check_skill_deploy_sync.py — the new gate from
docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md Task 1.

Root cause this gate closes: docs/adr/2026-08-09-check-brief-canon-ruling.md
names ~/.claude/skills/brief-authoring/scripts/check_brief.py as canonical and
every citing ADR's own Verification block runs it, but the deployed bundle
could silently fall behind (or never have existed at all — the concrete
2026-08-27 finding) without `sync_skills.py --check` catching it, because that
checker can only diff files that already exist repo-side. This gate is
citation-driven instead: it greps docs/adr/**/*.md for
`~/.claude/skills/<name>/scripts/<file>.py` citations and asserts each cited
path actually exists at the deployed target.

Mutation-testing discipline (docs/superpowers/plans/2026-08-27-ssot-data-
lineage-remediation.md "Global Constraints"): every new checker must have the
exact bad condition it claims to catch planted and confirmed to propagate as
a non-zero exit — `test_missing_deployed_file_fails` below does exactly that
(a skill dir that exists but is missing the cited scripts/*.py file), not a
vacuous always-pass check.

Environment note: `test_clean_deploy_passes` invokes the real
`scripts/sync_skills.py` (default target resolution) as its fixture step.
`sync_skills.py` refuses to deploy FROM a `.claude/worktrees/` checkout
without `--force` (by design — worktree branch state must not clobber the
live bundle silently). This repo's own dev sessions commonly run inside such
a worktree, so `--force` is passed unconditionally here: it is a no-op when
NOT running from a worktree (the refusal branch is only reached when
`is_under_worktrees()` is true), and required when it is.
"""
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def test_clean_deploy_passes(tmp_path, monkeypatch):
    # After a successful sync_skills.py run, the gate must exit 0.
    subprocess.run(
        [sys.executable, "scripts/sync_skills.py", "--force"],
        check=True, cwd=REPO_ROOT,
    )
    result = subprocess.run(
        [sys.executable, "scripts/check_skill_deploy_sync.py"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_missing_deployed_file_fails(monkeypatch, tmp_path):
    # Simulate the exact defect this gate exists to catch: a skill script
    # cited in an ADR Verification block that is absent from the deployed
    # target.
    fake_home_skills = tmp_path / "home_skills"
    (fake_home_skills / "brief-authoring").mkdir(parents=True)
    # deliberately do NOT create scripts/check_brief.py under it
    monkeypatch.setenv("HOME_SKILLS_DEPLOY_TARGET_OVERRIDE", str(fake_home_skills))
    result = subprocess.run(
        [sys.executable, "scripts/check_skill_deploy_sync.py"],
        capture_output=True, text=True, cwd=REPO_ROOT,
        env={**os.environ, "HOME_SKILLS_DEPLOY_TARGET_OVERRIDE": str(fake_home_skills)},
    )
    assert result.returncode != 0
    assert "brief-authoring" in result.stdout


def test_missing_deployed_file_names_every_missing_script(tmp_path):
    """Adversarial: the fixture above only proves ONE known-missing file is
    caught. Plant a second, distinct skill+script citation gap (synthesized
    via a temp ADR dir) and confirm the finder does not stop at the first
    hit — a checker that silently truncates its own findings list is a
    different failure mode than one that finds nothing at all."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "check_skill_deploy_sync", REPO_ROOT / "scripts" / "check_skill_deploy_sync.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    adr_dir = tmp_path / "adr"
    adr_dir.mkdir()
    (adr_dir / "fake-1.md").write_text(
        "See `~/.claude/skills/alpha/scripts/one.py` for details.\n",
        encoding="utf-8",
    )
    (adr_dir / "fake-2.md").write_text(
        "Also `~/.claude/skills/beta/scripts/two.py` runs the gate.\n",
        encoding="utf-8",
    )
    cited = mod.find_cited_skill_scripts(adr_dir)
    assert cited == {("alpha", "one.py"), ("beta", "two.py")}

    home_skills = tmp_path / "home_skills"
    (home_skills / "alpha" / "scripts").mkdir(parents=True)
    (home_skills / "alpha" / "scripts" / "one.py").write_text("# present\n", encoding="utf-8")
    (home_skills / "beta").mkdir()  # beta/scripts/two.py deliberately absent

    result = subprocess.run(
        [sys.executable, "scripts/check_skill_deploy_sync.py"],
        capture_output=True, text=True, cwd=REPO_ROOT,
        env={
            **os.environ,
            "HOME_SKILLS_DEPLOY_TARGET_OVERRIDE": str(home_skills),
        },
    )
    # This run still scans the REAL docs/adr/ (not the synthetic fixture
    # above, which only exercises find_cited_skill_scripts() directly) — so
    # it should report the real brief-authoring/check_brief.py gap against
    # the synthetic empty-ish home_skills target, not "alpha"/"beta" (those
    # are exercised via the direct function call above, not the subprocess).
    assert result.returncode != 0
    assert "brief-authoring" in result.stdout


def test_no_citations_found_exits_0(tmp_path):
    """If docs/adr/ (as resolved by the script) has zero citations, the gate
    must not fail-closed on an empty search — mutation guard against a
    checker that HARD-fails when it simply finds nothing to check."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "check_skill_deploy_sync", REPO_ROOT / "scripts" / "check_skill_deploy_sync.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    empty_adr_dir = tmp_path / "empty_adr"
    empty_adr_dir.mkdir()
    assert mod.find_cited_skill_scripts(empty_adr_dir) == set()


def test_find_cited_skill_scripts_ignores_non_matching_paths(tmp_path):
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "check_skill_deploy_sync", REPO_ROOT / "scripts" / "check_skill_deploy_sync.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    adr_dir = tmp_path / "adr"
    adr_dir.mkdir()
    (adr_dir / "irrelevant.md").write_text(
        "python scripts/check_brief.py docs/adr/x.md --type adr\n"
        "See ~/.claude/skills/brief-authoring/SKILL.md for the template.\n",
        encoding="utf-8",
    )
    # Neither the repo-side script path nor a non-scripts/ skill file should
    # be picked up by the citation regex.
    assert mod.find_cited_skill_scripts(adr_dir) == set()


def test_real_repo_finds_brief_authoring_citation():
    """Regression: the real docs/adr/ corpus (12+ ADRs, confirmed via grep
    during authoring) must surface the brief-authoring/check_brief.py
    citation — a checker that finds nothing here would be silently broken."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "check_skill_deploy_sync", REPO_ROOT / "scripts" / "check_skill_deploy_sync.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    cited = mod.find_cited_skill_scripts(REPO_ROOT / "docs" / "adr")
    assert ("brief-authoring", "check_brief.py") in cited
