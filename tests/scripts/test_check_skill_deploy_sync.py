"""Tests for scripts/check_skill_deploy_sync.py — the new gate from
docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md Task 1.

Current contract: scripts/README.md#skill-lifecycle. Historical root cause:
https://github.com/Joshua-Asante/first-passage/blob/4fb2b88f3b7d56d77463c43ba45c87ffadff6a31/docs/adr/2026-08-09-check-brief-canon-ruling.md
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

2026-08-28 review fix (Critical + Important #2): two defects fixed together.

  1. (Critical) GitHub Actions runners have no ~/.claude/skills/ deploy
     target at all — there is no deploy step in .github/workflows/, by
     design. The prior version of check_skill_deploy_sync.py treated "no
     deploy root" the same as "deploy root exists but script missing",
     exiting 1 either way — hard-failing the sole required CI check on
     every future PR, forever. `test_no_deploy_target_skips_not_passes`
     below pins the fix: a HOME_SKILLS_DEPLOY_TARGET_OVERRIDE pointing at a
     path that does not exist at all must SKIP (exit 0, says NOT CHECKED),
     never silently pass and never hard-fail.

  2. (Important #2) `test_clean_deploy_passes` used to invoke the real
     `scripts/sync_skills.py --force` with DEFAULT target resolution, which
     `resolve_targets()` fans out to BOTH the AppData cloud-synced primary
     target AND ~/.claude/skills/ — the bundle every other Claude Code
     session on this machine actually loads. `--force` was needed only to
     bypass sync_skills.py's own worktree-source refusal (real guard:
     uncommitted branch state must not clobber the live bundle), and that
     bypass, combined with unredirected default targets, is exactly the
     "deploy this unmerged branch over the live bundle" defect. The fix
     below copies the in-repo `.claude/skills` source tree into a pytest
     `tmp_path` that sits outside any `.claude/worktrees/` tree (so
     `is_under_worktrees()` is false and `--force` is never needed at all),
     and passes an explicit `--target` (per `resolve_targets()`'s own
     docstring: "Explicit --target is the sole destination" — no home
     add-on). Neither the AppData target nor ~/.claude/skills/ is ever
     touched by this test.

2026-09-15 fix (second route to the same false-fail): managed remote
sessions (Claude Code on the web) DO have ~/.claude/skills/, but it is
harness-owned -- only `session-start-hook/` and the plugin marketplace's
`synced/<uuid>_<uuid>/<skill>/` copies -- and nothing under it was
published by sync_skills.py. The root-exists test alone took the
real-check branch and red-lined `gate_manifest.py --tier check` on an
unmodified main checkout. The SKIP decision now keys on whether at least
one ADR-cited skill has a directory DIRECTLY under the root.
`test_root_with_only_unrelated_dirs_skips_not_passes` pins the SKIP;
`test_partial_bundle_is_drift_not_skip` pins that the decision is
"any cited skill dir present", never "all present", so a partial deploy
still fails as drift.

Codex review fix on PR #403 (P1): keying the decision on the CITED skill's
directory alone left a hole -- the ADR corpus cites only brief-authoring, so
a real bundle that lost brief-authoring/ itself read as harness-owned and
SKIPped on the exact deletion the gate guards. The marker set is now the
cited skills plus every directory the repo owns under .claude/skills/;
`test_bundle_missing_only_the_cited_skill_still_fails` plants that bundle
and requires exit 1 with brief-authoring listed.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def test_clean_deploy_passes(tmp_path):
    # This checks citation-driven existence, not release authorization.
    # Build a populated target directly under tmp_path: invoking publication
    # would unnecessarily couple this gate to Git/review policy and risks
    # resolving real user targets. Release behavior has its own tests.
    deploy_target = tmp_path / "deploy_target"
    shutil.copytree(
        REPO_ROOT / ".claude" / "skills", deploy_target,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )
    result = subprocess.run(
        [sys.executable, "scripts/check_skill_deploy_sync.py"],
        capture_output=True, text=True, cwd=REPO_ROOT,
        env={**os.environ, "HOME_SKILLS_DEPLOY_TARGET_OVERRIDE": str(deploy_target)},
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_no_deploy_target_skips_not_passes(tmp_path):
    """Critical fix regression: when the resolved deploy root does not exist
    AT ALL (the exact GitHub Actions / fresh-clone condition — no
    ~/.claude/skills/, no deploy step in .github/workflows/), the gate must
    SKIP (exit 0) and say so explicitly — never silently claim OK (that would
    hide a real future drift once a target exists) and never hard-fail (that
    is the Critical bug: it red-lined the sole required CI check forever)."""
    nonexistent = tmp_path / "does_not_exist_at_all"
    assert not nonexistent.exists()
    result = subprocess.run(
        [sys.executable, "scripts/check_skill_deploy_sync.py"],
        capture_output=True, text=True, cwd=REPO_ROOT,
        env={**os.environ, "HOME_SKILLS_DEPLOY_TARGET_OVERRIDE": str(nonexistent)},
    )
    assert result.returncode == 0, result.stdout + result.stderr
    out = result.stdout
    assert "SKIP" in out and "NOT CHECKED" in out
    assert "OK:" not in out
    assert "check_skill_deploy_sync.py" in out
    assert "Publication is not required" in out
    assert "python scripts/sync_skills.py" not in out


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
    assert "--revision" in result.stdout and "--target" in result.stdout
    assert "Run: python scripts/sync_skills.py" not in result.stdout


def test_root_with_only_unrelated_dirs_skips_not_passes(tmp_path):
    """2026-09-15 fix regression: the deploy root EXISTS but holds only
    harness-owned entries -- the exact managed-remote-container condition
    (`/root/.claude/skills/` with `session-start-hook/` and the plugin
    marketplace's `synced/<uuid>_<uuid>/<skill>/` copies, nothing published
    by sync_skills.py). The gate must SKIP (exit 0, says NOT CHECKED), not
    take the real-check branch and red-line `gate_manifest.py --tier check`
    on an unmodified main checkout. The nested marketplace copy of the
    cited script is planted deliberately: existing SOMEWHERE beneath the
    root must not count as this repo's deployed bundle."""
    root = tmp_path / "home_skills"
    (root / "session-start-hook").mkdir(parents=True)
    nested = (
        root / "synced" / "0f9a3c1e-uuid_7b2d4e6f-uuid"
        / "brief-authoring" / "scripts"
    )
    nested.mkdir(parents=True)
    (nested / "check_brief.py").write_text("# marketplace copy\n", encoding="utf-8")
    assert not (root / "brief-authoring").exists()
    result = subprocess.run(
        [sys.executable, "scripts/check_skill_deploy_sync.py"],
        capture_output=True, text=True, cwd=REPO_ROOT,
        env={**os.environ, "HOME_SKILLS_DEPLOY_TARGET_OVERRIDE": str(root)},
    )
    assert result.returncode == 0, result.stdout + result.stderr
    out = result.stdout
    assert "SKIP" in out and "NOT CHECKED" in out
    assert "OK:" not in out
    assert "DRIFT" not in out
    assert "session-start-hook" in out and "synced" in out
    assert "check_skill_deploy_sync.py" in out
    assert "Publication is not required" in out
    assert "python scripts/sync_skills.py" not in out


def test_bundle_missing_only_the_cited_skill_still_fails(tmp_path):
    """Codex P1 on PR #403: a REAL deployed bundle whose brief-authoring/ was
    removed (the external-rewrite class this gate exists to catch) still
    carries the repo's other skills directly under the root. It must take
    the real check and report brief-authoring as drift -- never SKIP as if
    the root were a harness-owned container directory."""
    root = tmp_path / "home_skills"
    for name in ("fable-method", "inqhiori", "verify-source"):
        assert (REPO_ROOT / ".claude" / "skills" / name).is_dir(), name
        (root / name).mkdir(parents=True)
        (root / name / "SKILL.md").write_text("# deployed copy\n", encoding="utf-8")
    assert not (root / "brief-authoring").exists()
    result = subprocess.run(
        [sys.executable, "scripts/check_skill_deploy_sync.py"],
        capture_output=True, text=True, cwd=REPO_ROOT,
        env={**os.environ, "HOME_SKILLS_DEPLOY_TARGET_OVERRIDE": str(root)},
    )
    assert result.returncode != 0, result.stdout + result.stderr
    assert "SKIP" not in result.stdout
    assert "DRIFT" in result.stdout
    assert "brief-authoring/scripts/check_brief.py" in result.stdout


def test_partial_bundle_is_drift_not_skip(tmp_path):
    """Mutation guard on the 2026-09-15 SKIP decision: it asks whether ANY
    cited skill has a directory directly under the root, never whether ALL
    do. With alpha/ deployed and beta/ absent (plus a foreign entry that
    must not flip the decision), the gate must take the real-check branch
    and report beta as drift -- an implementation that skipped whenever
    some cited skill was missing would hide exactly the partial-deploy
    defect this gate exists to catch."""
    adr_dir = tmp_path / "adr"
    adr_dir.mkdir()
    (adr_dir / "fake.md").write_text(
        "Run `~/.claude/skills/alpha/scripts/one.py` then "
        "`~/.claude/skills/beta/scripts/two.py`.\n",
        encoding="utf-8",
    )
    root = tmp_path / "home_skills"
    (root / "alpha" / "scripts").mkdir(parents=True)
    (root / "alpha" / "scripts" / "one.py").write_text("# ok\n", encoding="utf-8")
    (root / "session-start-hook").mkdir()
    assert not (root / "beta").exists()
    result = subprocess.run(
        [sys.executable, "scripts/check_skill_deploy_sync.py"],
        capture_output=True, text=True, cwd=REPO_ROOT,
        env={
            **os.environ,
            "ADR_DIR_OVERRIDE": str(adr_dir),
            "HOME_SKILLS_DEPLOY_TARGET_OVERRIDE": str(root),
        },
    )
    assert result.returncode != 0, result.stdout + result.stderr
    assert "SKIP" not in result.stdout
    assert "beta/scripts/two.py" in result.stdout
    assert "alpha/scripts/one.py" not in result.stdout


def test_multiple_missing_scripts_are_all_reported(tmp_path):
    """Adversarial: with 2 distinct missing skill+script citations, the gate
    must report BOTH — a checker that silently truncates its own findings
    list at the first hit is a different failure mode than one that finds
    nothing at all. (Renamed 2026-08-28 review fix: the prior version of this
    test, despite its name, only ever asserted the same single
    brief-authoring gap the test above it already covers — it never actually
    exercised 2+ missing scripts through the gate. This version drives the
    real subprocess against a synthetic ADR_DIR_OVERRIDE so both planted
    gaps are genuinely checked end-to-end, not just via the direct
    find_cited_skill_scripts() call.)"""
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

    home_skills = tmp_path / "home_skills"
    (home_skills / "alpha" / "scripts").mkdir(parents=True)  # one.py absent
    (home_skills / "beta" / "scripts").mkdir(parents=True)  # two.py absent

    result = subprocess.run(
        [sys.executable, "scripts/check_skill_deploy_sync.py"],
        capture_output=True, text=True, cwd=REPO_ROOT,
        env={
            **os.environ,
            "ADR_DIR_OVERRIDE": str(adr_dir),
            "HOME_SKILLS_DEPLOY_TARGET_OVERRIDE": str(home_skills),
        },
    )
    assert result.returncode != 0
    assert "alpha/scripts/one.py" in result.stdout
    assert "beta/scripts/two.py" in result.stdout


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
