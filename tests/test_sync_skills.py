"""Tests for scripts/sync_skills.py — explicit reviewed-revision publication."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_SS_PATH = Path(__file__).resolve().parent.parent / "scripts" / "sync_skills.py"
_spec = importlib.util.spec_from_file_location("sync_skills", _SS_PATH)
ss = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ss)

_HOOK_PATH = Path(__file__).resolve().parent.parent / "scripts" / "sync_skills_hook.py"
_hook_spec = importlib.util.spec_from_file_location("sync_skills_hook", _HOOK_PATH)
hook = importlib.util.module_from_spec(_hook_spec)
_hook_spec.loader.exec_module(hook)

_REPO = Path(__file__).resolve().parent.parent
_MAKEFILE = _REPO / "Makefile"


def _mk(root: Path, skill: str, fname: str, content: str) -> None:
    d = root / skill
    d.mkdir(parents=True, exist_ok=True)
    (d / fname).write_text(content, encoding="utf-8")


def _git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
    )


def _init_repo(root: Path, *, branch: str = "main") -> Path:
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-b", branch)
    _git(root, "config", "user.email", "tester@example.com")
    _git(root, "config", "user.name", "Tester")
    _git(root, "config", "core.autocrlf", "false")
    return root


def _write_skill(skills: Path, name: str, files: dict[str, str | bytes]) -> None:
    d = skills / name
    d.mkdir(parents=True, exist_ok=True)
    for rel, content in files.items():
        dest = d / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            dest.write_bytes(content)
        else:
            dest.write_text(content, encoding="utf-8", newline="\n")


def _commit_all(repo: Path, message: str) -> str:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", message)
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def _fingerprint(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    out: dict[str, str] = {}
    for f in sorted(p for p in path.rglob("*") if p.is_file()):
        rel = f.relative_to(path).as_posix()
        out[rel] = hashlib.sha256(f.read_bytes()).hexdigest()
    return out


def _primary_release(tmp_path: Path, skills: dict[str, dict[str, str | bytes]] | None = None):
    repo = _init_repo(tmp_path / "src")
    skills_dir = repo / ".claude" / "skills"
    payload = skills or {"alpha": {"SKILL.md": "alpha-v1\n"}}
    for name, files in payload.items():
        _write_skill(skills_dir, name, files)
    sha = _commit_all(repo, "skills")
    target = tmp_path / "deployed"
    return repo, skills_dir, sha, target


def _publish(skills_dir: Path, sha: str, target: Path, extra: list[str] | None = None) -> int:
    argv = [
        "--repo-skills", str(skills_dir),
        "--revision", sha,
        "--target", str(target),
    ]
    if extra:
        argv.extend(extra)
    return ss.main(argv)


def _try_reparse(link: Path, dest: Path) -> bool:
    dest.mkdir(parents=True, exist_ok=True)
    try:
        link.symlink_to(dest, target_is_directory=True)
        return True
    except OSError:
        if os.name != "nt":
            return False
        completed = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(dest)],
            capture_output=True,
            text=True,
        )
        return completed.returncode == 0 and link.exists()


# --- diagnostic helpers still used by check-mode tests ---

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
    (target / "alpha" / "SKILL.md").write_text("v2\n", encoding="utf-8")
    drift = ss.check_drift(repo, target)
    assert any("content differs" in d for d in drift), drift


def test_check_detects_missing_in_deployed(tmp_path):
    repo = tmp_path / "repo"
    target = tmp_path / "deployed"
    _mk(repo, "alpha", "SKILL.md", "x\n")
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


def test_check_never_creates_missing_target(tmp_path):
    repo = tmp_path / "repo"
    target = tmp_path / "deployed"
    _mk(repo, "alpha", "SKILL.md", "x\n")
    assert not target.exists()
    rc = ss.main(["--check", "--repo-skills", str(repo), "--target", str(target)])
    assert rc == 1
    assert not target.exists()
    assert not any(tmp_path.iterdir() if False else tmp_path.glob(".*"))
    leftovers = [p.name for p in tmp_path.iterdir() if p.name != "repo"]
    assert leftovers == []


def test_check_reports_deployed_only_extra_dir(tmp_path):
    repo = tmp_path / "repo"
    target = tmp_path / "deployed"
    _mk(repo, "alpha", "SKILL.md", "x\n")
    ss.copy_skills(repo, target)
    _mk(target, "zombie", "SKILL.md", "dead\n")
    drift = ss.check_drift(repo, target)
    assert any("zombie" in d and "no repo copy" in d for d in drift), drift
    rc = ss.main(["--check", "--repo-skills", str(repo), "--target", str(target)])
    assert rc == 1


def test_check_classifies_rule0_as_separately_owned(tmp_path, capsys):
    repo = tmp_path / "repo"
    target = tmp_path / "deployed"
    _mk(repo, "alpha", "SKILL.md", "x\n")
    ss.copy_skills(repo, target)
    _mk(target, "rule-0", "SKILL.md", "user-owned\n")
    rc = ss.main(["--check", "--repo-skills", str(repo), "--target", str(target)])
    assert rc == 1
    out = capsys.readouterr().out
    assert "rule-0" in out
    assert "docs/pursuits/d3-rule-0-user-skill.md" in out
    assert "import or delete" not in out.lower()
    assert (target / "rule-0" / "SKILL.md").read_text(encoding="utf-8") == "user-owned\n"


def test_is_under_worktrees_pure_function():
    wt = Path("C:/u/j/repo/.claude/worktrees/some-wt/.claude/skills")
    assert ss.is_under_worktrees(wt)
    assert hook.is_under_worktrees(wt)
    main_checkout = Path("C:/u/j/repo/.claude/skills")
    assert not ss.is_under_worktrees(main_checkout)
    assert not hook.is_under_worktrees(main_checkout)
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
    monkeypatch.setenv("SKILLS_DEPLOY_TARGET", str(ss.HOME_SKILLS_DEPLOY_TARGET))
    targets = ss.resolve_targets(None)
    assert targets == [ss.HOME_SKILLS_DEPLOY_TARGET]


def test_check_reports_drift_on_home_bundle(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    primary = tmp_path / "primary"
    home = tmp_path / "home-skills"
    _mk(repo, "alpha", "SKILL.md", "v1\n")
    ss.copy_skills(repo, primary)
    ss.copy_skills(repo, home)
    monkeypatch.setenv("SKILLS_DEPLOY_TARGET", str(primary))
    monkeypatch.setattr(ss, "HOME_SKILLS_DEPLOY_TARGET", home)
    (home / "alpha" / "SKILL.md").write_text("stale\n", encoding="utf-8")
    rc = ss.main(["--check", "--repo-skills", str(repo)])
    assert rc == 1


def test_check_detects_extra_deployed_skill(tmp_path):
    repo = tmp_path / "repo"
    target = tmp_path / "deployed"
    _mk(repo, "alpha", "SKILL.md", "x\n")
    ss.copy_skills(repo, target)
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


def test_check_ignores_generated_caches(tmp_path):
    repo = tmp_path / "repo"
    target = tmp_path / "deployed"
    _mk(repo, "alpha", "SKILL.md", "x\n")
    ss.copy_skills(repo, target)
    cache = target / "alpha" / "__pycache__"
    cache.mkdir()
    (cache / "mod.cpython-312.pyc").write_bytes(b"\x00cache")
    (target / "alpha" / ".DS_Store").write_bytes(b"ds")
    assert ss.check_drift(repo, target) == []
    rc = ss.main(["--check", "--repo-skills", str(repo), "--target", str(target)])
    assert rc == 0


def test_check_normalizes_text_newlines_but_not_binary(tmp_path):
    repo = tmp_path / "repo"
    target = tmp_path / "deployed"
    _mk(repo, "alpha", "SKILL.md", "hello\n")
    _mk(repo, "alpha", "icon.bin", "")
    (repo / "alpha" / "icon.bin").write_bytes(b"BIN\x00\x01")
    ss.copy_skills(repo, target)
    (target / "alpha" / "SKILL.md").write_bytes(b"hello\r\n")
    assert ss.check_drift(repo, target) == []
    (target / "alpha" / "icon.bin").write_bytes(b"BIN\x00\x02")
    drift = ss.check_drift(repo, target)
    assert any("icon.bin" in d and "content differs" in d for d in drift), drift
    assert not any("SKILL.md" in d for d in drift)


def test_check_invalid_utf8_is_byte_compared(tmp_path):
    repo = tmp_path / "repo"
    target = tmp_path / "deployed"
    _mk(repo, "alpha", "SKILL.md", "x\n")
    ss.copy_skills(repo, target)
    (repo / "alpha" / "notes.md").write_bytes(b"ok\xff\n")
    (target / "alpha" / "notes.md").write_bytes(b"ok\xfe\n")
    drift = ss.check_drift(repo, target)
    assert any("notes.md" in d for d in drift), drift


# --- publication CLI ---

def test_publication_refuses_without_revision_and_target(tmp_path, capsys):
    repo, skills_dir, _sha, target = _primary_release(tmp_path)
    before = _fingerprint(target)
    rc = ss.main(["--repo-skills", str(skills_dir), "--target", str(target)])
    assert rc == 2
    assert _fingerprint(target) == before
    err = capsys.readouterr().err
    assert "--revision" in err
    rc = ss.main(["--repo-skills", str(skills_dir), "--revision", "HEAD"])
    assert rc == 2
    assert not target.exists()
    err = capsys.readouterr().err
    assert "--target" in err


def test_publication_does_not_use_implicit_home(tmp_path, monkeypatch, capsys):
    repo, skills_dir, sha, _target = _primary_release(tmp_path)
    primary = tmp_path / "primary"
    home = tmp_path / "home-skills"
    monkeypatch.setenv("SKILLS_DEPLOY_TARGET", str(primary))
    monkeypatch.setattr(ss, "HOME_SKILLS_DEPLOY_TARGET", home)
    rc = ss.main(["--repo-skills", str(skills_dir), "--revision", sha])
    assert rc == 2
    assert not primary.exists()
    assert not home.exists()
    assert "--target" in capsys.readouterr().err


def test_force_does_not_bypass_release_checks(tmp_path, capsys):
    repo, skills_dir, _sha, target = _primary_release(tmp_path)
    rc = ss.main([
        "--repo-skills", str(skills_dir),
        "--target", str(target),
        "--force",
    ])
    assert rc == 2
    assert not target.exists()
    err = capsys.readouterr().err.lower()
    assert "reviewed" in err or "revision" in err
    assert "explicit" in err or "--target" in err


def test_publish_primary_main_at_revision(tmp_path, capsys):
    repo, skills_dir, sha, target = _primary_release(
        tmp_path,
        {"alpha": {"SKILL.md": "alpha-v1\n", "scripts/run.py": "print(1)\n"}},
    )
    rc = _publish(skills_dir, sha, target)
    assert rc == 0
    assert (target / "alpha" / "SKILL.md").read_bytes() == b"alpha-v1\n"
    assert (target / "alpha" / "scripts" / "run.py").read_bytes() == b"print(1)\n"
    out = capsys.readouterr().out
    assert "review verified" not in out.lower()
    assert sha in out
    assert "backup" in out.lower()


def test_publish_wrong_revision_leaves_target(tmp_path):
    repo, skills_dir, sha1, target = _primary_release(tmp_path)
    _write_skill(skills_dir, "alpha", {"SKILL.md": "alpha-v2\n"})
    sha2 = _commit_all(repo, "v2")
    target.mkdir()
    (target / "keep.bin").write_bytes(b"keep")
    before = _fingerprint(target)
    rc = _publish(skills_dir, sha1, target)
    assert rc == 3
    assert _fingerprint(target) == before


def test_publish_feature_branch_refused(tmp_path):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    _git(repo, "checkout", "-b", "feature")
    target.mkdir()
    (target / "keep.txt").write_text("x", encoding="utf-8")
    before = _fingerprint(target)
    rc = _publish(skills_dir, sha, target)
    assert rc == 3
    assert _fingerprint(target) == before


def test_publish_detached_head_refused(tmp_path):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    _git(repo, "checkout", "--detach", sha)
    target.mkdir()
    (target / "keep.txt").write_text("x", encoding="utf-8")
    before = _fingerprint(target)
    rc = _publish(skills_dir, sha, target)
    assert rc == 3
    assert _fingerprint(target) == before


@pytest.mark.parametrize("wt_rel", [".worktrees/wt-a", ".claude/worktrees/wt-b", "arbitrary-linked"])
def test_publish_linked_worktree_refused(tmp_path, wt_rel):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    wt = tmp_path / wt_rel
    wt.parent.mkdir(parents=True, exist_ok=True)
    _git(repo, "worktree", "add", str(wt), sha)
    wt_skills = wt / ".claude" / "skills"
    target.mkdir()
    (target / "keep.txt").write_text("x", encoding="utf-8")
    before = _fingerprint(target)
    rc = _publish(wt_skills, sha, target)
    assert rc == 3
    assert _fingerprint(target) == before


def test_publish_separate_git_dir_refused(tmp_path):
    git_dir = tmp_path / "separate.git"
    repo = tmp_path / "src"
    repo.mkdir()
    _git(repo, "init", "--separate-git-dir", str(git_dir), "-b", "main")
    _git(repo, "config", "user.email", "tester@example.com")
    _git(repo, "config", "user.name", "Tester")
    _git(repo, "config", "core.autocrlf", "false")
    skills_dir = repo / ".claude" / "skills"
    _write_skill(skills_dir, "alpha", {"SKILL.md": "x\n"})
    sha = _commit_all(repo, "init")
    target = tmp_path / "deployed"
    target.mkdir()
    (target / "keep.txt").write_text("x", encoding="utf-8")
    before = _fingerprint(target)
    rc = _publish(skills_dir, sha, target)
    assert rc == 3
    assert _fingerprint(target) == before


def test_publish_unavailable_git_refused(tmp_path, monkeypatch):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    target.mkdir()
    (target / "keep.txt").write_text("x", encoding="utf-8")
    before = _fingerprint(target)

    def _no_git(*_a, **_k):
        raise FileNotFoundError("git")

    monkeypatch.setattr(ss, "_run_git", _no_git)
    rc = _publish(skills_dir, sha, target)
    assert rc in (2, 3)
    assert _fingerprint(target) == before


def test_publish_submodule_refused(tmp_path):
    child = _init_repo(tmp_path / "child")
    child_skills = child / ".claude" / "skills"
    _write_skill(child_skills, "alpha", {"SKILL.md": "sub\n"})
    child_sha = _commit_all(child, "child")
    parent = _init_repo(tmp_path / "parent")
    _git(
        parent,
        "-c",
        "protocol.file.allow=always",
        "submodule",
        "add",
        "--",
        str(child.resolve()),
        "vendor",
    )
    _commit_all(parent, "add submodule")
    sub_skills = parent / "vendor" / ".claude" / "skills"
    target = tmp_path / "deployed"
    target.mkdir()
    (target / "keep.txt").write_text("x", encoding="utf-8")
    before = _fingerprint(target)
    rc = _publish(sub_skills, child_sha, target)
    assert rc == 3
    assert _fingerprint(target) == before


def test_publish_modified_tracked_payload_refused(tmp_path):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    (skills_dir / "alpha" / "SKILL.md").write_text("dirty\n", encoding="utf-8")
    target.mkdir()
    (target / "keep.txt").write_text("x", encoding="utf-8")
    before = _fingerprint(target)
    rc = _publish(skills_dir, sha, target)
    assert rc == 3
    assert _fingerprint(target) == before


def test_publish_deleted_tracked_payload_refused(tmp_path):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    (skills_dir / "alpha" / "SKILL.md").unlink()
    target.mkdir()
    (target / "keep.txt").write_text("x", encoding="utf-8")
    before = _fingerprint(target)
    rc = _publish(skills_dir, sha, target)
    assert rc == 3
    assert _fingerprint(target) == before


def test_publish_untracked_releasable_file_refused(tmp_path):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    (skills_dir / "alpha" / "EXTRA.md").write_text("new\n", encoding="utf-8")
    target.mkdir()
    (target / "keep.txt").write_text("x", encoding="utf-8")
    before = _fingerprint(target)
    rc = _publish(skills_dir, sha, target)
    assert rc == 3
    assert _fingerprint(target) == before


def test_publish_unrelated_dirty_note_allowed(tmp_path):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    (repo / "NOTES.md").write_text("operator scratch\n", encoding="utf-8")
    rc = _publish(skills_dir, sha, target)
    assert rc == 0
    assert (target / "alpha" / "SKILL.md").read_bytes() == b"alpha-v1\n"


def test_publish_cache_only_changes_allowed(tmp_path):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    cache = skills_dir / "alpha" / "__pycache__"
    cache.mkdir()
    (cache / "x.pyc").write_bytes(b"cache")
    rc = _publish(skills_dir, sha, target)
    assert rc == 0
    assert not (target / "alpha" / "__pycache__").exists()
    assert (target / "alpha" / "SKILL.md").read_bytes() == b"alpha-v1\n"


def test_publish_preserves_rule0_and_unknown_extras(tmp_path):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    _mk(target, "rule-0", "SKILL.md", "user-owned\n")
    _mk(target, "zombie", "SKILL.md", "keep-me\n")
    rc = _publish(skills_dir, sha, target)
    assert rc == 0
    assert (target / "rule-0" / "SKILL.md").read_text(encoding="utf-8") == "user-owned\n"
    assert (target / "zombie" / "SKILL.md").read_text(encoding="utf-8") == "keep-me\n"
    assert (target / "alpha" / "SKILL.md").read_bytes() == b"alpha-v1\n"


def test_publish_uses_exact_revision_bytes_not_working_tree_newlines(tmp_path):
    repo, skills_dir, sha, target = _primary_release(
        tmp_path, {"alpha": {"SKILL.md": "line\n"}}
    )
    (skills_dir / "alpha" / "SKILL.md").write_bytes(b"line\r\n")
    _git(repo, "add", ".claude/skills/alpha/SKILL.md")
    # working tree now differs only by newline after reset of index? keep unstaged
    _git(repo, "restore", "--staged", ".claude/skills/alpha/SKILL.md")
    (skills_dir / "alpha" / "SKILL.md").write_bytes(b"line\r\n")
    # CRLF-only working-tree change of a text file is still a modified tracked payload
    rc = _publish(skills_dir, sha, target)
    assert rc == 3
    assert not (target / "alpha").exists() or (target / "alpha" / "SKILL.md").read_bytes() != b"line\r\n"


def test_publish_source_target_overlap_refused(tmp_path):
    repo, skills_dir, sha, _target = _primary_release(tmp_path)
    rc = _publish(skills_dir, sha, repo)
    assert rc == 3
    rc = _publish(skills_dir, sha, skills_dir)
    assert rc == 3


def test_publish_target_inside_git_metadata_refused(tmp_path):
    repo, skills_dir, sha, _target = _primary_release(tmp_path)
    rc = _publish(skills_dir, sha, repo / ".git" / "skills-out")
    assert rc == 3


def test_publish_reparse_source_or_target_refused(tmp_path):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    linked_src = tmp_path / "linked-src"
    if not _try_reparse(linked_src, skills_dir):
        pytest.skip("reparse/symlink creation is not permitted on this host")
    rc = _publish(linked_src, sha, target)
    assert rc == 3
    assert not target.exists() or _fingerprint(target) == {}
    if target.exists():
        shutil.rmtree(target)
    linked_target = tmp_path / "linked-target"
    real_target = tmp_path / "real-target"
    if not _try_reparse(linked_target, real_target):
        pytest.skip("reparse/symlink creation is not permitted on this host")
    rc = _publish(skills_dir, sha, linked_target)
    assert rc == 3
    assert list(real_target.rglob("*")) == [] or not any(real_target.rglob("SKILL.md"))


def test_publish_absent_destination_creates_and_installs(tmp_path):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    assert not target.exists()
    rc = _publish(skills_dir, sha, target)
    assert rc == 0
    assert (target / "alpha" / "SKILL.md").read_bytes() == b"alpha-v1\n"


def test_publish_existing_destination_replaces_and_keeps_backup(tmp_path, capsys):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    _mk(target, "alpha", "SKILL.md", "old\n")
    rc = _publish(skills_dir, sha, target)
    assert rc == 0
    assert (target / "alpha" / "SKILL.md").read_bytes() == b"alpha-v1\n"
    out = capsys.readouterr().out
    backup_paths = [
        Path(line.split("backup", 1)[-1].strip(" :"))
        for line in out.splitlines()
        if "backup" in line.lower() and ":\\" in line or "/." in line or "backup" in line.lower()
    ]
    assert "backup" in out.lower()
    backups = list((tmp_path).glob("**/.skill-release-backup-*"))
    assert backups
    backed = backups[0] / "alpha" / "SKILL.md"
    assert backed.is_file()
    assert backed.read_text(encoding="utf-8") == "old\n"


def test_preparation_failure_leaves_target_unchanged(tmp_path, monkeypatch):
    repo, skills_dir, sha, target = _primary_release(
        tmp_path, {"alpha": {"SKILL.md": "a\n"}, "beta": {"SKILL.md": "b\n"}}
    )
    _mk(target, "alpha", "SKILL.md", "old-a\n")
    _mk(target, "beta", "SKILL.md", "old-b\n")
    before = _fingerprint(target)

    def _boom(*_a, **_k):
        raise OSError("injected preparation failure")

    monkeypatch.setattr(ss, "_stage_release_payload", _boom)
    rc = _publish(skills_dir, sha, target)
    assert rc == 1
    assert _fingerprint(target) == before


def test_backup_failure_leaves_target_unchanged(tmp_path, monkeypatch):
    repo, skills_dir, sha, target = _primary_release(
        tmp_path, {"alpha": {"SKILL.md": "a\n"}, "beta": {"SKILL.md": "b\n"}}
    )
    _mk(target, "alpha", "SKILL.md", "old-a\n")
    before = _fingerprint(target)

    def _boom(*_a, **_k):
        raise OSError("injected backup failure")

    monkeypatch.setattr(ss, "_backup_existing_skill", _boom)
    rc = _publish(skills_dir, sha, target)
    assert rc == 1
    assert _fingerprint(target) == before


def test_failure_after_second_skill_install_rolls_back(tmp_path, monkeypatch):
    repo, skills_dir, sha, target = _primary_release(
        tmp_path,
        {
            "alpha": {"SKILL.md": "new-a\n"},
            "beta": {"SKILL.md": "new-b\n"},
            "gamma": {"SKILL.md": "new-c\n"},
        },
    )
    _mk(target, "alpha", "SKILL.md", "old-a\n")
    _mk(target, "beta", "SKILL.md", "old-b\n")
    _mk(target, "gamma", "SKILL.md", "old-c\n")
    seen: list[str] = []
    real = ss._install_skill

    def _fail_on_third(staged: Path, dest: Path, *a, **k):
        seen.append(dest.name)
        if len(seen) >= 3:
            raise OSError("injected install failure after second skill")
        return real(staged, dest, *a, **k)

    monkeypatch.setattr(ss, "_install_skill", _fail_on_third)
    rc = _publish(skills_dir, sha, target)
    assert rc == 1
    assert (target / "alpha" / "SKILL.md").read_text(encoding="utf-8") == "old-a\n"
    assert (target / "beta" / "SKILL.md").read_text(encoding="utf-8") == "old-b\n"
    assert (target / "gamma" / "SKILL.md").read_text(encoding="utf-8") == "old-c\n"


def test_failure_during_rollback_preserves_recovery_material(tmp_path, monkeypatch, capsys):
    repo, skills_dir, sha, target = _primary_release(
        tmp_path,
        {"alpha": {"SKILL.md": "new-a\n"}, "beta": {"SKILL.md": "new-b\n"}},
    )
    _mk(target, "alpha", "SKILL.md", "old-a\n")
    real_install = ss._install_skill
    real_restore = ss._restore_skill
    installs = {"n": 0}

    def _fail_second(staged: Path, dest: Path, *a, **k):
        installs["n"] += 1
        if installs["n"] >= 2:
            raise OSError("injected install failure")
        return real_install(staged, dest, *a, **k)

    def _fail_restore(*_a, **_k):
        raise OSError("injected rollback failure")

    monkeypatch.setattr(ss, "_install_skill", _fail_second)
    monkeypatch.setattr(ss, "_restore_skill", _fail_restore)
    rc = _publish(skills_dir, sha, target)
    assert rc == 1
    out = capsys.readouterr()
    text = (out.out + out.err).lower()
    assert "unchanged" not in text
    assert "succeeded" not in text or "release" not in text
    assert "manual" in text or "recovery" in text
    leftovers = [
        p for p in tmp_path.iterdir()
        if p.name.startswith(".skill-release-")
    ]
    assert leftovers
    assert (target / "alpha").exists()


def test_target_change_during_staging_refused(tmp_path, monkeypatch):
    repo, skills_dir, sha, target = _primary_release(
        tmp_path, {"alpha": {"SKILL.md": "new-a\n"}, "beta": {"SKILL.md": "new-b\n"}}
    )
    _mk(target, "alpha", "SKILL.md", "old-a\n")
    real = ss._stage_release_payload

    def _mutate_then_stage(*a, **k):
        staged = real(*a, **k)
        (target / "alpha" / "SKILL.md").write_text("raced\n", encoding="utf-8")
        return staged

    monkeypatch.setattr(ss, "_stage_release_payload", _mutate_then_stage)
    rc = _publish(skills_dir, sha, target)
    assert rc == 1
    assert (target / "alpha" / "SKILL.md").read_text(encoding="utf-8") == "raced\n"
    assert not (target / "beta").exists() or (
        target / "beta" / "SKILL.md"
    ).read_text(encoding="utf-8") != "new-b\n"


def test_source_change_during_staging_refused(tmp_path, monkeypatch):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    _mk(target, "alpha", "SKILL.md", "old-a\n")
    before = _fingerprint(target)
    real = ss._stage_release_payload

    def _mutate_source(*a, **k):
        staged = real(*a, **k)
        (skills_dir / "alpha" / "SKILL.md").write_text("edited-during-prep\n", encoding="utf-8")
        return staged

    monkeypatch.setattr(ss, "_stage_release_payload", _mutate_source)
    rc = _publish(skills_dir, sha, target)
    assert rc == 3
    assert _fingerprint(target) == before


def test_rollback_of_absent_original_removes_new_install(tmp_path, monkeypatch):
    repo, skills_dir, sha, target = _primary_release(
        tmp_path, {"alpha": {"SKILL.md": "a\n"}, "beta": {"SKILL.md": "b\n"}}
    )
    assert not target.exists()
    real = ss._install_skill
    seen = {"n": 0}

    def _fail_second(staged: Path, dest: Path, *a, **k):
        seen["n"] += 1
        if seen["n"] >= 2:
            raise OSError("injected install failure")
        return real(staged, dest, *a, **k)

    monkeypatch.setattr(ss, "_install_skill", _fail_second)
    rc = _publish(skills_dir, sha, target)
    assert rc == 1
    assert not target.exists() or not (target / "alpha").exists()


# --- hook ---

def _hook_payload(file_path: str, extra_edits: list[str] | None = None) -> str:
    edits = [{"file_path": file_path}]
    for p in extra_edits or []:
        edits.append({"file_path": p})
    return json.dumps({"tool_input": {"file_path": file_path, "edits": edits}})


def test_hook_unrelated_and_malformed_are_benign(monkeypatch, capsys):
    monkeypatch.setattr(sys, "stdin", __import__("io").StringIO("not-json"))
    assert hook.main() == 0
    monkeypatch.setattr(
        sys, "stdin", __import__("io").StringIO(json.dumps({"tool_input": {"file_path": "docs/x.md"}}))
    )
    calls: list[list[str]] = []

    def _no_run(*_a, **_k):
        raise AssertionError("validators must not run for unrelated edits")

    monkeypatch.setattr(hook.subprocess, "run", _no_run)
    assert hook.main() == 0
    assert calls == []


def test_hook_skill_edit_validates_and_never_publishes(monkeypatch, capsys):
    payload = _hook_payload(".claude/skills/alpha/SKILL.md")
    monkeypatch.setattr(sys, "stdin", __import__("io").StringIO(payload))
    runs: list[list[str]] = []

    def _fake_run(cmd, **kwargs):
        runs.append([str(c) for c in cmd])
        return subprocess.CompletedProcess(cmd, 0, stdout="OK\n", stderr="")

    monkeypatch.setattr(hook.subprocess, "run", _fake_run)
    rc = hook.main()
    assert rc == 0
    joined = " ".join(" ".join(c) for c in runs)
    assert "check_skill_refs.py" in joined
    assert "check_skills_no_constants.py" in joined
    assert "sync_skills.py" not in joined
    err = capsys.readouterr().err
    assert "explicit release" in err.lower() or "release is pending" in err.lower()


def test_hook_multi_edit_and_failing_validator(monkeypatch, capsys):
    payload = _hook_payload(
        ".claude/skills/alpha/SKILL.md",
        [".claude/skills/beta/SKILL.md"],
    )
    monkeypatch.setattr(sys, "stdin", __import__("io").StringIO(payload))

    def _fake_run(cmd, **kwargs):
        if any("check_skill_refs.py" in str(c) for c in cmd):
            return subprocess.CompletedProcess(cmd, 1, stdout="ref-fail\n", stderr="")
        return subprocess.CompletedProcess(cmd, 0, stdout="OK\n", stderr="")

    monkeypatch.setattr(hook.subprocess, "run", _fake_run)
    rc = hook.main()
    assert rc == 2
    err = capsys.readouterr().err
    assert "ref-fail" in err
    assert "NOT" in err or "failed" in err.lower()
    assert "sync_skills.py" not in err


def test_hook_missing_validator_is_not_claimed_passed(monkeypatch, capsys, tmp_path):
    payload = _hook_payload(".claude/skills/alpha/SKILL.md")
    monkeypatch.setattr(sys, "stdin", __import__("io").StringIO(payload))
    fake_dir = tmp_path / "scripts"
    fake_dir.mkdir()
    (fake_dir / "sync_skills.py").write_text("# unused\n", encoding="utf-8")
    monkeypatch.setattr(hook, "_script_dir", lambda: fake_dir)
    rc = hook.main()
    assert rc == 2
    err = capsys.readouterr().err
    assert "missing" in err.lower()
    assert "passed" not in err.lower()


def test_hook_never_creates_backups(monkeypatch, tmp_path):
    payload = _hook_payload(".claude/skills/alpha/SKILL.md")
    monkeypatch.setattr(sys, "stdin", __import__("io").StringIO(payload))

    def _fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(hook.subprocess, "run", _fake_run)
    hook.main()
    assert list(tmp_path.glob("**/.skill-release-backup-*")) == []


# --- Makefile isolation (throwaway fixture; never invoke the repo Makefile live) ---

_MAKEFILE_FIXTURE = """
ifneq ($(filter sync-skills,$(MAKECMDGOALS)),)
ifeq ($(CHECK),)
ifeq ($(REVISION),)
$(error make sync-skills requires REVISION and TARGET, or CHECK=1)
endif
ifeq ($(TARGET),)
$(error make sync-skills requires REVISION and TARGET, or CHECK=1)
endif
endif
endif

sync-skills:
ifdef CHECK
	@python scripts/sync_skills.py --check
else
	@python scripts/sync_skills.py --revision "$(REVISION)" --target "$(TARGET)"
endif
"""


def _make_available() -> str | None:
    return shutil.which("make") or shutil.which("mingw32-make")


def _run_throwaway_make(tmp_path: Path, *args: str) -> subprocess.CompletedProcess:
    make = _make_available()
    if not make:
        pytest.skip("make is not available in this environment")
    makefile = tmp_path / "Makefile"
    makefile.write_text(_MAKEFILE_FIXTURE, encoding="utf-8")
    sentinel = tmp_path / "scripts"
    sentinel.mkdir()
    (sentinel / "sync_skills.py").write_text(
        "import sys\n"
        "print('SENTINEL-RAN', sys.argv)\n"
        "raise SystemExit('throwaway makefile must not execute a real publisher')\n",
        encoding="utf-8",
    )
    return subprocess.run(
        [make, "-n", "-f", str(makefile), *args],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )


def test_makefile_check_does_not_require_publication_args(tmp_path):
    result = _run_throwaway_make(tmp_path, "sync-skills", "CHECK=1")
    assert result.returncode == 0, result.stderr
    assert "--check" in result.stdout
    assert "--revision" not in result.stdout
    assert "SENTINEL-RAN" not in result.stdout


def test_makefile_publication_refuses_missing_args(tmp_path):
    result = _run_throwaway_make(tmp_path, "sync-skills")
    assert result.returncode != 0
    text = result.stdout + result.stderr
    assert "REVISION" in text and "TARGET" in text
    assert "SENTINEL-RAN" not in text
    assert "--force" not in text


# --- coordinator review findings (2026-09-08) ---

def test_publish_refuses_source_under_ancestor_reparse(tmp_path):
    real = tmp_path / "real"
    repo = _init_repo(real / "src")
    skills_dir = repo / ".claude" / "skills"
    _write_skill(skills_dir, "alpha", {"SKILL.md": "alpha-v1\n"})
    sha = _commit_all(repo, "skills")
    target = tmp_path / "deployed"
    via = tmp_path / "via"
    if not _try_reparse(via, real):
        pytest.skip("reparse/symlink creation is not permitted on this host")
    linked_skills = via / "src" / ".claude" / "skills"
    target.mkdir()
    (target / "keep.txt").write_text("x", encoding="utf-8")
    before = _fingerprint(target)
    rc = _publish(linked_skills, sha, target)
    assert rc == 3
    assert _fingerprint(target) == before


def test_publish_refuses_target_under_ancestor_reparse(tmp_path):
    repo, skills_dir, sha, _target = _primary_release(tmp_path)
    real_parent = tmp_path / "real-dest"
    real_parent.mkdir()
    (real_parent / "keep.txt").write_text("x", encoding="utf-8")
    via = tmp_path / "via-dest"
    if not _try_reparse(via, real_parent):
        pytest.skip("reparse/symlink creation is not permitted on this host")
    target = via / "deployed"
    before = _fingerprint(real_parent)
    rc = _publish(skills_dir, sha, target)
    assert rc == 3
    assert _fingerprint(real_parent) == before
    assert not (real_parent / "deployed").exists()


@pytest.mark.parametrize("kind", ["modify", "delete", "extra"])
def test_staged_manifest_mismatch_refuses_before_backup(tmp_path, monkeypatch, kind):
    repo, skills_dir, sha, target = _primary_release(
        tmp_path, {"alpha": {"SKILL.md": "a\n", "refs/n.md": "r\n"}}
    )
    _mk(target, "alpha", "SKILL.md", "old-a\n")
    before = _fingerprint(target)
    real = ss._stage_release_payload

    def _tamper(*a, **k):
        staged = real(*a, **k)
        skill = staged / "alpha"
        if kind == "modify":
            (skill / "SKILL.md").write_text("tampered\n", encoding="utf-8")
        elif kind == "delete":
            (skill / "refs" / "n.md").unlink()
        else:
            (skill / "EXTRA.md").write_text("extra\n", encoding="utf-8")
        return staged

    monkeypatch.setattr(ss, "_stage_release_payload", _tamper)
    rc = _publish(skills_dir, sha, target)
    assert rc in (1, 3)
    assert _fingerprint(target) == before
    assert list(tmp_path.glob(".skill-release-backup-*")) == []


def test_publish_refuses_unrelated_git_hooks(tmp_path):
    repo, skills_dir, sha, _target = _primary_release(tmp_path)
    other = _init_repo(tmp_path / "other")
    (other / "README.md").write_text("x\n", encoding="utf-8")
    _commit_all(other, "other")
    hooks = other / ".git" / "hooks"
    hooks.mkdir(exist_ok=True)
    marker = hooks / "pre-commit"
    marker.write_text("keep\n", encoding="utf-8")
    before = _fingerprint(other / ".git")
    rc = _publish(skills_dir, sha, hooks)
    assert rc == 3
    assert _fingerprint(other / ".git") == before
    assert marker.read_text(encoding="utf-8") == "keep\n"


def test_publish_refuses_separate_git_dir_metadata(tmp_path):
    repo, skills_dir, sha, _target = _primary_release(tmp_path)
    git_dir = tmp_path / "foreign.git"
    work = tmp_path / "foreign-work"
    work.mkdir()
    _git(work, "init", "--separate-git-dir", str(git_dir), "-b", "main")
    hooks = git_dir / "hooks"
    hooks.mkdir(exist_ok=True)
    marker = hooks / "pre-commit"
    marker.write_text("keep\n", encoding="utf-8")
    before = _fingerprint(git_dir)
    rc = _publish(skills_dir, sha, hooks)
    assert rc == 3
    assert _fingerprint(git_dir) == before


def test_publish_refuses_ignored_private_payload(tmp_path):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    (repo / ".gitignore").write_text(".claude/skills/alpha/private.md\n", encoding="utf-8")
    _commit_all(repo, "ignore")
    sha = _git(repo, "rev-parse", "HEAD").stdout.strip()
    (skills_dir / "alpha" / "private.md").write_text("secret\n", encoding="utf-8")
    target.mkdir()
    (target / "keep.txt").write_text("x", encoding="utf-8")
    before = _fingerprint(target)
    rc = _publish(skills_dir, sha, target)
    assert rc == 3
    assert _fingerprint(target) == before


@pytest.mark.parametrize("flag", ["--assume-unchanged", "--skip-worktree"])
def test_publish_refuses_index_hidden_skill_edit(tmp_path, flag):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    rel = ".claude/skills/alpha/SKILL.md"
    _git(repo, "update-index", flag, rel)
    (skills_dir / "alpha" / "SKILL.md").write_text("hidden-edit\n", encoding="utf-8")
    target.mkdir()
    (target / "keep.txt").write_text("x", encoding="utf-8")
    before = _fingerprint(target)
    rc = _publish(skills_dir, sha, target)
    assert rc == 3
    assert _fingerprint(target) == before


def test_publish_allows_ignored_generated_cache(tmp_path):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    (repo / ".gitignore").write_text("__pycache__/\n*.pyc\n", encoding="utf-8")
    _commit_all(repo, "ignore-cache")
    sha = _git(repo, "rev-parse", "HEAD").stdout.strip()
    cache = skills_dir / "alpha" / "__pycache__"
    cache.mkdir()
    (cache / "x.pyc").write_bytes(b"cache")
    rc = _publish(skills_dir, sha, target)
    assert rc == 0
    assert (target / "alpha" / "SKILL.md").read_bytes() == b"alpha-v1\n"
    assert not (target / "alpha" / "__pycache__").exists()


def test_first_install_then_rollback_failure_keeps_staging_and_backup(
    tmp_path, monkeypatch, capsys
):
    repo, skills_dir, sha, target = _primary_release(
        tmp_path,
        {"alpha": {"SKILL.md": "new-a\n"}, "beta": {"SKILL.md": "new-b\n"}},
    )
    _mk(target, "alpha", "SKILL.md", "old-a\n")
    _mk(target, "beta", "SKILL.md", "old-b\n")

    def _fail_install(*_a, **_k):
        raise OSError("injected first install failure")

    def _fail_restore(*_a, **_k):
        raise OSError("injected restore failure")

    monkeypatch.setattr(ss, "_install_skill", _fail_install)
    monkeypatch.setattr(ss, "_restore_skill", _fail_restore)
    rc = _publish(skills_dir, sha, target)
    assert rc == 1
    out = capsys.readouterr()
    text = out.out + out.err
    assert "manual recovery" in text.lower() or "did not complete" in text.lower()
    backups = list(tmp_path.glob(".skill-release-backup-*"))
    stages = list(tmp_path.glob(".skill-release-stage-*"))
    assert backups, text
    assert stages, text
    assert (backups[0] / "alpha" / "SKILL.md").read_text(encoding="utf-8") == "old-a\n"
    assert any(p.name == "alpha" for p in stages[0].iterdir())
    for token in ("staging=", "backup="):
        assert token in text
        reported = next(
            line.split(token, 1)[1].strip()
            for line in text.splitlines()
            if token in line
        )
        assert Path(reported).exists(), reported


def test_snapshot_detects_toplevel_file_added_during_staging(tmp_path, monkeypatch):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    target.mkdir()
    before_extra = "externally-added\n"
    real = ss._stage_release_payload

    def _add_file(*a, **k):
        staged = real(*a, **k)
        (target / "alpha").write_text(before_extra, encoding="utf-8")
        return staged

    monkeypatch.setattr(ss, "_stage_release_payload", _add_file)
    rc = _publish(skills_dir, sha, target)
    assert rc == 1
    assert (target / "alpha").is_file()
    assert (target / "alpha").read_text(encoding="utf-8") == before_extra


def test_snapshot_detects_target_created_during_staging(tmp_path, monkeypatch):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    assert not target.exists()
    real = ss._stage_release_payload

    def _create_target(*a, **k):
        staged = real(*a, **k)
        target.mkdir()
        (target / "sneak.txt").write_text("external\n", encoding="utf-8")
        return staged

    monkeypatch.setattr(ss, "_stage_release_payload", _create_target)
    rc = _publish(skills_dir, sha, target)
    assert rc == 1
    assert (target / "sneak.txt").read_text(encoding="utf-8") == "external\n"
    assert not (target / "alpha").exists() or (target / "alpha").is_file() is False and not (
        target / "alpha" / "SKILL.md"
    ).exists()


def test_snapshot_detects_directory_to_file_transition(tmp_path, monkeypatch):
    repo, skills_dir, sha, target = _primary_release(tmp_path)
    _mk(target, "alpha", "SKILL.md", "old-a\n")
    real = ss._stage_release_payload

    def _replace_dir(*a, **k):
        staged = real(*a, **k)
        shutil.rmtree(target / "alpha")
        (target / "alpha").write_text("now-a-file\n", encoding="utf-8")
        return staged

    monkeypatch.setattr(ss, "_stage_release_payload", _replace_dir)
    rc = _publish(skills_dir, sha, target)
    assert rc == 1
    assert (target / "alpha").is_file()
    assert (target / "alpha").read_text(encoding="utf-8") == "now-a-file\n"


# --- coordinator second review (2026-09-08) ---

@pytest.mark.parametrize(
    "kind",
    ["extra_pyc", "pycache_hidden_md", "nested_junction", "empty_rule0", "empty_nested"],
)
def test_staged_generated_or_reparse_injection_refused_before_backup(
    tmp_path, monkeypatch, kind
):
    repo, skills_dir, sha, target = _primary_release(
        tmp_path, {"alpha": {"SKILL.md": "a\n"}}
    )
    _mk(target, "alpha", "SKILL.md", "old-a\n")
    _mk(target, "rule-0", "SKILL.md", "user-owned\n")
    before = _fingerprint(target)
    real = ss._stage_release_payload

    def _inject(*a, **k):
        staged = real(*a, **k)
        skill = staged / "alpha"
        if kind == "extra_pyc":
            (skill / "extra.pyc").write_bytes(b"injected-pyc")
        elif kind == "pycache_hidden_md":
            cache = skill / "__pycache__"
            cache.mkdir()
            (cache / "hidden.md").write_text("sneak\n", encoding="utf-8")
        elif kind == "empty_rule0":
            (staged / "rule-0").mkdir()
        elif kind == "empty_nested":
            (skill / "unexpected-empty").mkdir()
        else:
            ext = tmp_path / "ext-refs"
            if not _try_reparse(skill / "references", ext):
                pytest.skip("reparse/symlink creation is not permitted on this host")
        return staged

    monkeypatch.setattr(ss, "_stage_release_payload", _inject)
    rc = _publish(skills_dir, sha, target)
    assert rc in (1, 3)
    assert _fingerprint(target) == before
    assert list(tmp_path.glob(".skill-release-backup-*")) == []
    assert (target / "alpha" / "SKILL.md").read_text(encoding="utf-8") == "old-a\n"


def test_backup_failure_after_target_becomes_junction_preserves_external(
    tmp_path, monkeypatch, capsys
):
    repo, skills_dir, sha, target = _primary_release(
        tmp_path, {"alpha": {"SKILL.md": "a\n"}, "beta": {"SKILL.md": "b\n"}}
    )
    _mk(target, "alpha", "SKILL.md", "old-a\n")
    _mk(target, "beta", "SKILL.md", "old-b\n")
    external = tmp_path / "external-via-junction"
    external.mkdir()
    (external / "sentinel.txt").write_text("keep-external\n", encoding="utf-8")
    before_ext = _fingerprint(external)
    real = ss._backup_existing_skill

    def _swap_after_alpha(src: Path, dest: Path, *a, **k):
        real(src, dest, *a, **k)
        if src.name != "alpha":
            raise OSError("injected backup failure")
        displaced = tmp_path / "displaced-target"
        target.rename(displaced)
        if not _try_reparse(target, external):
            displaced.rename(target)
            pytest.skip("reparse/symlink creation is not permitted on this host")
        raise OSError("injected backup failure after target became junction")

    monkeypatch.setattr(ss, "_backup_existing_skill", _swap_after_alpha)
    rc = _publish(skills_dir, sha, target)
    assert rc == 1
    assert _fingerprint(external) == before_ext
    assert (external / "sentinel.txt").read_text(encoding="utf-8") == "keep-external\n"
    assert not (external / "alpha").exists()
    backups = list(tmp_path.glob(".skill-release-backup-*"))
    stages = list(tmp_path.glob(".skill-release-stage-*"))
    assert backups, "backup recovery material must be preserved"
    assert stages, "staging recovery material must be preserved"
    assert (backups[0] / "alpha" / "SKILL.md").read_text(encoding="utf-8") == "old-a\n"
    captured = capsys.readouterr()
    text = captured.out + captured.err
    assert "backup=" in text
    assert "staging=" in text
    for token in ("staging=", "backup="):
        reported = next(
            line.split(token, 1)[1].strip()
            for line in text.splitlines()
            if token in line
        )
        assert Path(reported).exists(), reported


def test_publish_clean_crlf_checkout_installs_revision_lf_bytes(tmp_path):
    repo = _init_repo(tmp_path / "src")
    (repo / ".gitattributes").write_text("*.md text eol=crlf\n", encoding="utf-8")
    skills_dir = repo / ".claude" / "skills"
    _write_skill(skills_dir, "alpha", {"SKILL.md": "alpha-v1\n"})
    sha = _commit_all(repo, "skills")
    skill_md = skills_dir / "alpha" / "SKILL.md"
    skill_md.unlink()
    _git(repo, "checkout", "--", ".claude/skills/alpha/SKILL.md")
    porcelain = _git(repo, "status", "--porcelain")
    assert porcelain.stdout.strip() == ""
    eol = _git(repo, "ls-files", "--eol", "--", ".claude/skills/alpha/SKILL.md")
    if "i/lf" not in eol.stdout or "w/crlf" not in eol.stdout:
        pytest.skip(
            "Git did not materialize a clean CRLF working tree for eol=crlf: "
            + eol.stdout
        )
    working = (skills_dir / "alpha" / "SKILL.md").read_bytes()
    assert working == b"alpha-v1\r\n"
    target = tmp_path / "deployed"
    rc = _publish(skills_dir, sha, target)
    assert rc == 0, "clean eol=crlf checkout must publish, not refuse"
    assert (target / "alpha" / "SKILL.md").read_bytes() == b"alpha-v1\n"


def test_snapshot_detects_nested_dir_replaced_with_junction(tmp_path, monkeypatch):
    repo, skills_dir, sha, target = _primary_release(
        tmp_path, {"alpha": {"SKILL.md": "new-a\n"}}
    )
    _mk(target, "alpha", "SKILL.md", "old-a\n")
    refs = target / "alpha" / "references"
    refs.mkdir()
    external = tmp_path / "external-nested-refs"
    external.mkdir()
    (external / "keep.txt").write_text("external\n", encoding="utf-8")
    before_ext = _fingerprint(external)
    real = ss._stage_release_payload

    def _swap_nested(*a, **k):
        staged = real(*a, **k)
        shutil.rmtree(refs)
        if not _try_reparse(refs, external):
            pytest.skip("reparse/symlink creation is not permitted on this host")
        return staged

    monkeypatch.setattr(ss, "_stage_release_payload", _swap_nested)
    rc = _publish(skills_dir, sha, target)
    assert rc in (1, 3)
    assert (target / "alpha" / "SKILL.md").read_text(encoding="utf-8") == "old-a\n"
    assert _fingerprint(external) == before_ext
    assert (external / "keep.txt").read_text(encoding="utf-8") == "external\n"
    assert not (target / "alpha" / "SKILL.md").read_bytes() == b"new-a\n"
    assert list(tmp_path.glob(".skill-release-backup-*")) == []
