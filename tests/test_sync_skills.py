"""Minimal tests for scripts/sync_skills.py — one-way repo -> deployed sync."""
from __future__ import annotations

import importlib.util
from pathlib import Path

_SS_PATH = Path(__file__).resolve().parent.parent / "scripts" / "sync_skills.py"
_spec = importlib.util.spec_from_file_location("sync_skills", _SS_PATH)
ss = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ss)

_HOOK_PATH = Path(__file__).resolve().parent.parent / "scripts" / "sync_skills_hook.py"
_hook_spec = importlib.util.spec_from_file_location("sync_skills_hook", _HOOK_PATH)
hook = importlib.util.module_from_spec(_hook_spec)
_hook_spec.loader.exec_module(hook)


def _mk(root: Path, skill: str, fname: str, content: str) -> None:
    d = root / skill
    d.mkdir(parents=True, exist_ok=True)
    (d / fname).write_text(content, encoding="utf-8")


def test_check_no_drift(tmp_path):
    repo = tmp_path / "repo"
    target = tmp_path / "deployed"
    _mk(repo, "alpha", "SKILL.md", "hello\n")
    ss.copy_skills(repo, target)
    assert ss.check_drift(repo, target) == []


def test_check_detects_content_drift(tmp_path):
    repo = tmp_path / "repo"
    target = tmp_path / "deployed"
    _mk(repo, "alpha", "SKILL.md", "v1\n")
    ss.copy_skills(repo, target)
    # mutate deployed
    (target / "alpha" / "SKILL.md").write_text("v2\n", encoding="utf-8")
    drift = ss.check_drift(repo, target)
    assert any("content differs" in d for d in drift), drift


def test_check_detects_missing_in_deployed(tmp_path):
    repo = tmp_path / "repo"
    target = tmp_path / "deployed"
    _mk(repo, "alpha", "SKILL.md", "x\n")
    # never copied
    target.mkdir()
    drift = ss.check_drift(repo, target)
    assert any("missing in deployed" in d for d in drift), drift


def test_check_mode_exit_codes(tmp_path):
    repo = tmp_path / "repo"
    target = tmp_path / "deployed"
    _mk(repo, "alpha", "SKILL.md", "x\n")
    ss.copy_skills(repo, target)
    rc = ss.main(["--check", "--repo-skills", str(repo), "--target", str(target)])
    assert rc == 0
    (target / "alpha" / "SKILL.md").write_text("changed\n", encoding="utf-8")
    rc = ss.main(["--check", "--repo-skills", str(repo), "--target", str(target)])
    assert rc == 1


def test_default_copy_creates_target(tmp_path):
    repo = tmp_path / "repo"
    target = tmp_path / "deployed"
    _mk(repo, "alpha", "SKILL.md", "x\n")
    _mk(repo, "beta", "SKILL.md", "y\n")
    rc = ss.main(["--repo-skills", str(repo), "--target", str(target)])
    assert rc == 0
    assert (target / "alpha" / "SKILL.md").exists()
    assert (target / "beta" / "SKILL.md").exists()


def test_check_reports_deployed_only_extra_dir(tmp_path):
    repo = tmp_path / "repo"
    target = tmp_path / "deployed"
    _mk(repo, "alpha", "SKILL.md", "x\n")
    ss.copy_skills(repo, target)
    # A dir living only in the deployed bundle (e.g. an ADR-retired skill still
    # serving) is drift — check_drift must name it and --check must fail.
    _mk(target, "zombie", "SKILL.md", "dead\n")
    drift = ss.check_drift(repo, target)
    assert any("zombie" in d and "no repo copy" in d for d in drift), drift
    rc = ss.main(["--check", "--repo-skills", str(repo), "--target", str(target)])
    assert rc == 1


def test_is_under_worktrees_pure_function():
    wt = Path("C:/u/j/repo/.claude/worktrees/some-wt/.claude/skills")
    assert ss.is_under_worktrees(wt)
    assert hook.is_under_worktrees(wt)
    main_checkout = Path("C:/u/j/repo/.claude/skills")
    assert not ss.is_under_worktrees(main_checkout)
    assert not hook.is_under_worktrees(main_checkout)
    # "worktrees" alone (not under .claude) is not a worktree session.
    assert not ss.is_under_worktrees(Path("C:/u/j/worktrees/repo"))


def test_resolve_targets_default_includes_home(monkeypatch):
    monkeypatch.delenv("SKILLS_DEPLOY_TARGET", raising=False)
    targets = ss.resolve_targets(None)
    assert targets[0] == ss.DEFAULT_DEPLOY_TARGET
    assert ss.HOME_SKILLS_DEPLOY_TARGET in targets


def test_resolve_targets_explicit_is_sole(tmp_path):
    only = tmp_path / "only"
    assert ss.resolve_targets(str(only)) == [only]


def test_resolve_targets_env_primary_plus_home(monkeypatch, tmp_path):
    primary = tmp_path / "primary-bundle"
    monkeypatch.setenv("SKILLS_DEPLOY_TARGET", str(primary))
    targets = ss.resolve_targets(None)
    assert targets[0] == primary
    assert ss.HOME_SKILLS_DEPLOY_TARGET in targets


def test_resolve_targets_dedupes_when_env_is_home(monkeypatch):
    monkeypatch.setenv(
        "SKILLS_DEPLOY_TARGET", str(ss.HOME_SKILLS_DEPLOY_TARGET)
    )
    targets = ss.resolve_targets(None)
    assert targets == [ss.HOME_SKILLS_DEPLOY_TARGET]


def test_default_deploy_writes_home_bundle(tmp_path, monkeypatch):
    """No --target: primary (env) and ~/.claude/skills both receive the copy."""
    repo = tmp_path / "repo"
    primary = tmp_path / "primary"
    home = tmp_path / "home-skills"
    _mk(repo, "alpha", "SKILL.md", "x\n")
    monkeypatch.setenv("SKILLS_DEPLOY_TARGET", str(primary))
    monkeypatch.setattr(ss, "HOME_SKILLS_DEPLOY_TARGET", home)
    rc = ss.main(["--repo-skills", str(repo)])
    assert rc == 0
    assert (primary / "alpha" / "SKILL.md").read_text(encoding="utf-8") == "x\n"
    assert (home / "alpha" / "SKILL.md").read_text(encoding="utf-8") == "x\n"


def test_check_reports_drift_on_home_bundle(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    primary = tmp_path / "primary"
    home = tmp_path / "home-skills"
    _mk(repo, "alpha", "SKILL.md", "v1\n")
    monkeypatch.setenv("SKILLS_DEPLOY_TARGET", str(primary))
    monkeypatch.setattr(ss, "HOME_SKILLS_DEPLOY_TARGET", home)
    assert ss.main(["--repo-skills", str(repo)]) == 0
    (home / "alpha" / "SKILL.md").write_text("stale\n", encoding="utf-8")
    rc = ss.main(["--check", "--repo-skills", str(repo)])
    assert rc == 1


def test_deploy_from_worktree_refused_without_force(tmp_path, capsys):
    wt_repo = tmp_path / ".claude" / "worktrees" / "wt-x" / ".claude" / "skills"
    _mk(wt_repo, "alpha", "SKILL.md", "x\n")
    target = tmp_path / "deployed"
    rc = ss.main(["--repo-skills", str(wt_repo), "--target", str(target)])
    assert rc == 3
    assert not target.exists()
    err = capsys.readouterr().err
    assert "worktree" in err.lower()
    assert "--force" in err


def test_deploy_from_worktree_allowed_with_force(tmp_path):
    wt_repo = tmp_path / ".claude" / "worktrees" / "wt-x" / ".claude" / "skills"
    _mk(wt_repo, "alpha", "SKILL.md", "x\n")
    target = tmp_path / "deployed"
    rc = ss.main(["--repo-skills", str(wt_repo), "--target", str(target), "--force"])
    assert rc == 0
    assert (target / "alpha" / "SKILL.md").exists()


def test_check_detects_extra_deployed_skill(tmp_path):
    repo = tmp_path / "repo"
    target = tmp_path / "deployed"
    _mk(repo, "alpha", "SKILL.md", "x\n")
    ss.copy_skills(repo, target)
    # a whole extra directory deployed with no repo counterpart at all
    _mk(target, "some-unimported-skill", "SKILL.md", "y\n")
    drift = ss.check_drift(repo, target)
    assert any("some-unimported-skill" in d and "no repo copy" in d for d in drift), drift


def test_check_exempts_stock_skills(tmp_path):
    repo = tmp_path / "repo"
    target = tmp_path / "deployed"
    _mk(repo, "alpha", "SKILL.md", "x\n")
    ss.copy_skills(repo, target)
    for name in ss.STOCK_SKILLS_EXEMPT:
        _mk(target, name, "SKILL.md", "stock\n")
    assert ss.check_drift(repo, target) == []
