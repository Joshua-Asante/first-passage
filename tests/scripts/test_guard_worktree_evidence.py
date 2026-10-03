"""Regression tests for scripts/guard_worktree_evidence.py.

`scripts/fp.py` writes its verification records into the checkout's own ignored
`.cache/fp-verification/`, so `git worktree remove` deletes the evidence with the
tree. The hook must copy the records into the primary checkout's
`local_artifacts/fp-verification-archive/` *before* the tool call runs, block
(exit 2) when it cannot, and otherwise stay invisible.

These tests build real git repositories and real linked worktrees
(`git worktree add`) in tmp directories and drive the hook the way Claude Code
does: the script as a subprocess, the PreToolUse payload on stdin. The worktree
is never actually removed — the hook runs before the command and must never
touch the tree itself (g).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
GUARD = REPO / "scripts" / "guard_worktree_evidence.py"

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git not on PATH")


def _git(cwd: Path, *args: str) -> None:
    env = dict(os.environ, GIT_AUTHOR_NAME="T", GIT_AUTHOR_EMAIL="t@example.com",
               GIT_COMMITTER_NAME="T", GIT_COMMITTER_EMAIL="t@example.com")
    subprocess.run(["git", *args], cwd=cwd, check=True, env=env,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load():
    spec = importlib.util.spec_from_file_location("guard_worktree_evidence", GUARD)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


RECORD_IDS = ("20260929T101010Z-aaaaaaaaaaaa", "20260929T202020Z-bbbbbbbbbbbb")


def make_site(tmp_path: Path, *, records: bool) -> tuple[Path, Path]:
    """A primary checkout with one linked worktree (optionally holding records)."""
    primary = tmp_path / "primary"
    primary.mkdir()
    _git(primary, "init", "-q", "-b", "main")
    (primary / "README.md").write_text("seed\n", encoding="utf-8")
    _git(primary, "add", "-A")
    _git(primary, "commit", "-q", "-m", "seed")
    worktree = tmp_path / "wt-run"
    _git(primary, "worktree", "add", "-q", "-b", "feature", str(worktree))
    if records:
        for identity in RECORD_IDS:
            folder = worktree / ".cache" / "fp-verification" / identity
            folder.mkdir(parents=True)
            (folder / "record.json").write_text(
                json.dumps({"run_id": identity, "status": "completed"}), encoding="utf-8")
            (folder / "stdout.txt").write_text(f"output of {identity}\n", encoding="utf-8")
            (folder / "junit.xml").write_text(
                f"<testsuite tests='1' failures='0'>{identity}</testsuite>\n", encoding="utf-8")
    return primary, worktree


@pytest.fixture
def site(tmp_path):
    return make_site(tmp_path, records=True)


def run_hook(command: str, cwd: Path) -> subprocess.CompletedProcess:
    """The hook as Claude Code runs it: script path, payload on stdin."""
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command},
                          "cwd": str(cwd)})
    return subprocess.run([sys.executable, str(GUARD)], input=payload, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", cwd=str(cwd),
                          check=False, timeout=120)


def archive_of(primary: Path) -> Path:
    return primary / "local_artifacts" / "fp-verification-archive"


@pytest.fixture(scope="module")
def mod():
    return _load()


def remove_command(worktree: Path) -> str:
    return f'git worktree remove "{worktree}"'


def archived_files(archive: Path, worktree: Path) -> dict[str, str]:
    """Relative archive path -> sha256 for every file this worktree contributed."""
    prefix = archive / worktree.name
    return {p.relative_to(archive).as_posix(): sha256_file(p)
            for p in sorted(prefix.rglob("*")) if p.is_file()}


# --- (a) the records are copied and SHA256SUMS is correct ----------------------

def test_records_are_copied_and_sums_are_correct(site):
    primary, worktree = site
    archive = archive_of(primary)
    result = run_hook(remove_command(worktree), primary)
    assert result.returncode == 0, result.stderr
    assert str(len(RECORD_IDS)) in result.stdout and str(archive) in result.stdout

    records = worktree / ".cache" / "fp-verification"
    expected = {}
    for identity in RECORD_IDS:
        for source in sorted((records / identity).rglob("*")):
            if source.is_file():
                key = (worktree.name / Path(identity)
                       / source.relative_to(records / identity)).as_posix()
                expected[key] = source.read_bytes()
    assert expected
    assert {key: (archive / key).read_bytes() for key in expected} == expected

    lines = (archive / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    assert lines, "SHA256SUMS was not written"
    seen = set()
    for line in lines:
        digest, separator, name = line.partition("  ")
        assert separator and re.fullmatch(r"[0-9a-f]{64}", digest), line
        assert (archive / name).is_file(), line
        assert sha256_file(archive / name) == digest, line
        seen.add(name)
    assert seen == set(expected), "SHA256SUMS must cover exactly the archived files"


# --- (b) a second run changes nothing ------------------------------------------

def test_second_run_is_idempotent(site):
    primary, worktree = site
    archive = archive_of(primary)
    sums = archive / "SHA256SUMS"
    assert run_hook(remove_command(worktree), primary).returncode == 0
    before, listing = sums.read_bytes(), dict(archived_files(archive, worktree))
    assert before and listing

    again = run_hook(remove_command(worktree), primary)
    assert again.returncode == 0, again.stderr
    assert sums.read_bytes() == before, "sum lines were re-appended"
    assert archived_files(archive, worktree) == listing, "archived bytes changed"


# --- (c) commands that do not remove a worktree are silent no-ops -------------

@pytest.mark.parametrize("command", [
    'echo "git worktree remove"',
    "git worktree list",
    "git worktree list --porcelain",
    "git worktree prune",
    "git status",
    "ls .cache/fp-verification",
])
def test_non_matching_commands_are_silent_noops(site, command):
    primary, worktree = site  # records exist: the no-op must not depend on their absence
    result = run_hook(command, primary)
    assert result.returncode == 0, result.stderr
    assert result.stdout == "" and result.stderr == ""
    assert not (primary / "local_artifacts").exists()
    assert not any(archive_of(primary).glob("**/*"))


# --- (d) git -C <dir> worktree remove --force <path> is detected ---------------

def test_dash_c_directory_and_force_flag_are_detected(site):
    primary, worktree = site
    result = run_hook(f'git -C "{primary.parent}" worktree remove --force {worktree.name}',
                      primary)
    assert result.returncode == 0, result.stderr
    assert str(len(RECORD_IDS)) in result.stdout
    assert archived_files(archive_of(primary), worktree)


def test_relative_path_resolves_against_the_dash_c_directory(site):
    primary, worktree = site
    result = run_hook(f'git -C "{primary}" worktree remove --force "../{worktree.name}"',
                      primary.parent)
    assert result.returncode == 0, result.stderr
    assert archived_files(archive_of(primary), worktree)


# --- (e) a worktree without records is a silent no-op ---------------------------

def test_worktree_without_cache_is_a_silent_noop(tmp_path):
    primary, worktree = make_site(tmp_path, records=False)
    result = run_hook(remove_command(worktree), primary)
    assert result.returncode == 0, result.stderr
    assert result.stdout == "" and result.stderr == ""
    assert not (primary / "local_artifacts").exists()
    assert not (worktree / ".cache").exists()


# --- (f) a copy failure blocks with exit 2 and a reason -------------------------

def test_copy_failure_blocks_with_exit_2_and_reason(site):
    primary, worktree = site
    blocker = archive_of(primary)
    blocker.parent.mkdir(parents=True)
    blocker.write_text("occupies the archive path\n", encoding="utf-8")
    result = run_hook(remove_command(worktree), primary)
    assert result.returncode == 2
    assert result.stderr.strip(), "the reason must reach the operator"
    assert "guard_worktree_evidence" in result.stderr
    assert result.stdout == "", "no success summary for a failed retention"
    # nothing was deleted and the records are still in place for a retry
    for identity in RECORD_IDS:
        assert (worktree / ".cache" / "fp-verification" / identity / "record.json").is_file()


# --- (g) the source worktree is never modified ----------------------------------

def _snapshot(root: Path) -> dict:
    return {str(p.relative_to(root)): (p.stat().st_mtime_ns, hashlib.sha256(p.read_bytes()).hexdigest())
            for p in sorted(root.rglob("*")) if p.is_file()}


def test_hook_never_modifies_the_source_worktree(site):
    primary, worktree = site
    before = _snapshot(worktree)
    assert run_hook(remove_command(worktree), primary).returncode == 0
    assert _snapshot(worktree) == before
    # and the removal the hook prepared for was not performed either
    assert (worktree / ".git").exists()
    _git(primary, "worktree", "list")  # the metadata is intact


def test_two_records_from_two_worktrees_do_not_collide(site, tmp_path):
    other = tmp_path / "wt-other"
    _git(site[0], "worktree", "add", "-q", "-b", "second", str(other))
    for identity in RECORD_IDS:
        folder = other / ".cache" / "fp-verification" / identity
        folder.mkdir(parents=True)
        (folder / "record.json").write_text('{"status": "completed"}\n', encoding="utf-8")
    result = run_hook(f'git worktree remove "{site[1]}" && git worktree remove "{other}"',
                      site[0])
    assert result.returncode == 0, result.stderr
    archive = archive_of(site[0])
    assert set(archived_files(archive, site[1])) and set(archived_files(archive, other))
    assert (archive / site[1].name / RECORD_IDS[0] / "record.json").read_bytes() \
        != (archive / other.name / RECORD_IDS[0] / "record.json").read_bytes()


# --- detection unit tests: what the parser reads in command position ------------

@pytest.mark.parametrize("command,name", [    ("git worktree remove wt", "wt"),
    ("git worktree remove --force wt", "wt"),
    ("git worktree remove -f wt", "wt"),
    ("git worktree remove 'wt with spaces'", "wt with spaces"),
    ('git worktree remove "C:/tools/wt"', "wt"),
    ("git -C /repo worktree remove wt", "wt"),
    ("git --no-pager worktree remove wt", "wt"),
    ("sudo git worktree remove wt", "wt"),
    ("env FOO=1 git worktree remove wt", "wt"),
    ("cd /repo && git worktree remove wt", "wt"),
    ("GIT.EXE worktree remove wt", "wt"),
    ("bash -c 'git worktree remove wt'", "wt"),
])
def test_detected_spellings(mod, command, name):
    found = mod.removals(command, Path("/base"))
    assert len(found) == 1, command
    assert found[0][0].name == name and found[0][0].is_absolute()


@pytest.mark.parametrize("command", [
    "",
    "git status",
    "git worktree list",
    "git worktree prune",
    "git worktree add wt -b x",
    "git worktree lock wt",
    "git worktree move wt elsewhere",
    'echo "git worktree remove wt"',
    "git worktree remove",          # no path operand: git itself refuses
    "echo 'unterminated",
])
def test_undetected_spellings(mod, command):
    assert mod.removals(command, Path("/base")) == []


def test_cd_moves_the_base_for_a_later_removal(mod):
    found = mod.removals("cd /repo && git worktree remove wt", Path("/base"))
    assert found[0][0].name == "wt"
    assert found[0][1].name == "repo", "the path must resolve from /repo, not /base"
    found = mod.removals("git -C /repo worktree remove wt", Path("/base"))
    assert found[0][1].name == "repo"


def test_hook_is_registered_for_bash_and_powershell():
    """An unwired retention hook is the silent-loss failure this hook exists to stop."""
    settings = json.loads((REPO / ".claude" / "settings.json").read_text(encoding="utf-8"))
    pre = settings.get("hooks", {}).get("PreToolUse", [])
    for matcher in ("Bash", "PowerShell"):
        entries = [h.get("command", "") for group in pre if group.get("matcher") == matcher
                   for h in group.get("hooks", [])]
        assert any("guard_worktree_evidence.py" in command for command in entries), matcher
