r"""Regression tests for scripts/guard_worktree_evidence.py.

`scripts/fp.py` writes its verification records into the checkout's own ignored
`.cache/fp-verification/`, so `git worktree remove` deletes the evidence with the
tree. The hook must copy the records of every linked worktree into the primary
checkout's `local_artifacts/fp-verification-archive/` *before* the tool call runs,
block (exit 2) when it cannot, and otherwise stay invisible.

Design under test:

  * trigger — the case-insensitive regex `\bworktree\b[\s\S]*\bremove\b` over the
    command text; no tokenising, no path parsing (over-triggering is safe because
    the archive is idempotent; the command's paths are never trusted);
  * enumeration — `git -C <cwd> worktree list --porcelain`; the first entry is the
    primary, every other entry that exists on disk is archived; enumeration
    failure fails closed with exit 2;
  * layout — one shelf per linked worktree, named after the worktree's basename:
    `<archive>/<worktree>/<id>/...`, with `SHA256SUMS` alone at the archive root;
    version dirs `<id>`, `<id>~2`, ... are chosen per shelf;
  * immutability — version dirs chosen by record digest, staged in a temp dir,
    verified, then `os.rename`d into place; nothing existing is ever overwritten
    or deleted;
  * manifest — `SHA256SUMS` appends are idempotent and a path with two hashes is
    an exit-2 error;
  * exit codes — 0 silent, 0 with one stdout line, or 2 with one stderr line.

These tests build real git repositories and real linked worktrees
(`git worktree add`) in tmp directories and drive the hook the way Claude Code
does: the script as a subprocess, the PreToolUse payload on stdin. No worktree is
ever actually removed — the hook runs before the command and must never touch the
trees themselves (g).
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
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

RECORD_IDS = ("20260929T101010Z-aaaaaaaaaaaa", "20260929T202020Z-bbbbbbbbbbbb")


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


@pytest.fixture(scope="module")
def mod():
    return _load()


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
        add_records(worktree, RECORD_IDS)
    return primary, worktree


def add_records(worktree: Path, identities, *, marker: str = "") -> None:
    """Populate `<worktree>/.cache/fp-verification/<id>/` with three files."""
    for identity in identities:
        folder = worktree / ".cache" / "fp-verification" / identity
        folder.mkdir(parents=True)
        (folder / "record.json").write_text(
            json.dumps({"run_id": identity, "status": "completed", "note": marker}),
            encoding="utf-8")
        (folder / "stdout.txt").write_text(f"output of {identity} {marker}\n", encoding="utf-8")
        (folder / "junit.xml").write_text(
            f"<testsuite tests='1' failures='0'>{identity} {marker}</testsuite>\n",
            encoding="utf-8")


@pytest.fixture
def site(tmp_path):
    return make_site(tmp_path, records=True)


def run_hook(command: str, cwd: Path, *, payload_cwd: Path | None = None,
             tool_name: str = "Bash") -> subprocess.CompletedProcess:
    """The hook as Claude Code runs it: script path, payload on stdin."""
    payload = json.dumps({"tool_name": tool_name, "tool_input": {"command": command},
                          "cwd": str(payload_cwd if payload_cwd is not None else cwd)})
    return subprocess.run([sys.executable, str(GUARD)], input=payload, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", cwd=str(cwd),
                          check=False, timeout=120)


def run_main(monkeypatch, mod, command: str, cwd: Path) -> int:
    """Call main() in this process, with the payload on a fake stdin."""
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(
        {"tool_name": "Bash", "tool_input": {"command": command}, "cwd": str(cwd)})))
    return mod.main()


def archive_of(primary: Path) -> Path:
    return primary / "local_artifacts" / "fp-verification-archive"


def shelf_of(primary: Path, worktree: Path) -> Path:
    """One worktree's shelf inside the archive: named after the worktree."""
    return archive_of(primary) / worktree.name


def remove_command(worktree: Path) -> str:
    return f'git worktree remove "{worktree}"'


def archived_files(archive: Path) -> dict[str, bytes]:
    """Relative archive path -> bytes for every file in the archive."""
    return {p.relative_to(archive).as_posix(): p.read_bytes()
            for p in sorted(archive.rglob("*")) if p.is_file()}


def snapshot(root: Path) -> dict:
    return {str(p.relative_to(root)): (p.stat().st_mtime_ns, sha256_file(p))
            for p in sorted(root.rglob("*")) if p.is_file()}


# --- (a) the records are copied and SHA256SUMS is correct ----------------------

def test_records_are_copied_and_sums_are_correct(site):
    primary, worktree = site
    archive, shelf = archive_of(primary), shelf_of(primary, worktree)
    result = run_hook(remove_command(worktree), primary)
    assert result.returncode == 0, result.stderr
    assert len(result.stdout.strip().splitlines()) == 1, result.stdout
    assert str(len(RECORD_IDS)) in result.stdout and str(archive) in result.stdout

    records = worktree / ".cache" / "fp-verification"
    expected = {}
    for identity in RECORD_IDS:
        for source in sorted((records / identity).rglob("*")):
            if source.is_file():
                key = (Path(worktree.name) / identity
                       / source.relative_to(records / identity)).as_posix()
                expected[key] = source.read_bytes()
    assert expected
    assert archived_files(archive) == {**expected,
                                       "SHA256SUMS": (archive / "SHA256SUMS").read_bytes()}
    # the shelf is named after the worktree; version dirs carry the record ids
    # verbatim; SHA256SUMS sits alone at the archive root; no staging leftovers
    assert {p.name for p in archive.iterdir()} == {worktree.name, "SHA256SUMS"}
    assert {p.name for p in shelf.iterdir()} == set(RECORD_IDS)
    assert not list(archive.glob(".staging-*")) and not list(shelf.glob(".staging-*"))

    lines = (archive / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    seen = set()
    for line in lines:
        digest, separator, name = line.partition("  ")
        assert separator and re.fullmatch(r"[0-9a-f]{64}", digest), line
        assert (archive / name).is_file(), line
        assert sha256_file(archive / name) == digest, line
        seen.add(name)
    assert seen == set(expected), "SHA256SUMS must cover exactly the archived files"


# --- (b) a second run changes nothing ------------------------------------------

def test_second_run_is_idempotent_and_silent(site):
    primary, worktree = site
    archive = archive_of(primary)
    assert run_hook(remove_command(worktree), primary).returncode == 0
    sums, before = archive / "SHA256SUMS", archived_files(archive)
    tree_before = snapshot(archive)
    assert before and sums.is_file()

    again = run_hook(remove_command(worktree), primary)
    assert again.returncode == 0, again.stderr
    assert again.stdout == "" and again.stderr == "", "a full no-op stays silent"
    assert sums.read_bytes() == before["SHA256SUMS"], "sum lines were re-appended"
    assert archived_files(archive) == before, "archived bytes changed"
    assert snapshot(archive) == tree_before, "files were rewritten in place"


# --- (c) commands that do not mention removing a worktree are silent no-ops ----

@pytest.mark.parametrize("command", [
    "",
    "git status",
    "git worktree list",
    "git worktree list --porcelain",
    "git worktree prune",
    "git worktree add wt -b x",
    "git worktree lock wt",
    "git worktree move wt elsewhere",
    "git worktree repair",
    "ls .cache/fp-verification",
    "rm -rf .claude/worktrees/scratch",   # "worktrees" (plural) is not a match
    "echo remove the worktree",           # the words appear in the wrong order
])
def test_non_matching_commands_are_silent_noops(site, command):
    primary, worktree = site  # records exist: the no-op must not depend on their absence
    result = run_hook(command, primary)
    assert result.returncode == 0, result.stderr
    assert result.stdout == "" and result.stderr == ""
    assert not (primary / "local_artifacts").exists()


# --- (d) the trigger is the regex, not a parse of the command ------------------

@pytest.mark.parametrize("command", [
    "git worktree remove wt",
    "git worktree remove --force wt",
    "git worktree remove -f 'wt with spaces'",
    "git worktree remove",                       # no path operand: still a trigger
    "git -C /repo worktree remove -f wt",
    "GIT WORKTREE REMOVE wt",                    # case-insensitive
    "git worktree add tmp && git worktree remove tmp",
    "echo 'about to worktree remove the scratch'",   # data mention: safe over-trigger
    "sudo env FOO=1 git worktree remove wt",
])
def test_trigger_matches_every_spelling_that_might_remove_a_worktree(mod, command):
    assert mod.triggers(command), command


@pytest.mark.parametrize("command", [
    "",
    "git status",
    "git worktree list --porcelain",
    "git worktree prune",
    "git worktree add wt -b x",
    'echo "git worktree add"',
    "rm -rf worktrees scratch",
    "echo remove the worktree",       # `remove` precedes `worktree`: no match
    "git worktree repair",
])
def test_trigger_ignores_commands_without_both_words(mod, command):
    assert not mod.triggers(command)


def test_a_data_only_mention_still_archives(site):
    """No path parsing means an echo that merely mentions the words also retains
    the records — the safe direction to err."""
    primary, worktree = site
    result = run_hook("echo \"next: worktree remove, then rebuild\"", primary)
    assert result.returncode == 0, result.stderr
    assert len(result.stdout.strip().splitlines()) == 1
    assert (shelf_of(primary, worktree) / RECORD_IDS[0] / "record.json").is_file()


# --- (e) no linked worktree holds records: a silent no-op -----------------------

def test_worktree_without_records_is_a_silent_noop(tmp_path):
    primary, worktree = make_site(tmp_path, records=False)
    result = run_hook(remove_command(worktree), primary)
    assert result.returncode == 0, result.stderr
    assert result.stdout == "" and result.stderr == ""
    assert not (primary / "local_artifacts").exists()
    assert not (worktree / ".cache").exists()


# --- (f) a retention failure blocks with exit 2 and one reason line -------------

def test_retention_failure_blocks_with_exit_2_and_reason(site):
    primary, worktree = site
    blocker = archive_of(primary)
    blocker.parent.mkdir(parents=True)
    blocker.write_text("occupies the archive path\n", encoding="utf-8")
    result = run_hook(remove_command(worktree), primary)
    assert result.returncode == 2
    assert len(result.stderr.strip().splitlines()) == 1, "one reason line"
    assert "guard_worktree_evidence" in result.stderr
    assert result.stdout == "", "no success summary for a failed retention"
    # nothing was deleted and the records are still in place for a retry
    for identity in RECORD_IDS:
        assert (worktree / ".cache" / "fp-verification" / identity / "record.json").is_file()


# --- (g) the source worktrees are never modified --------------------------------

def test_hook_never_modifies_the_source_worktrees(site):
    primary, worktree = site
    before = snapshot(worktree)
    assert run_hook(remove_command(worktree), primary).returncode == 0
    assert snapshot(worktree) == before
    # and the removal the hook prepared for was not performed either
    assert (worktree / ".git").exists()
    _git(primary, "worktree", "list")  # the metadata is intact


# --- (h) every linked worktree is archived; same ids get version dirs -----------

def test_all_linked_worktrees_are_archived_into_their_own_shelves(tmp_path):
    primary, worktree = make_site(tmp_path, records=True)
    other = tmp_path / "wt-other"
    _git(primary, "worktree", "add", "-q", "-b", "second", str(other))
    add_records(other, RECORD_IDS[:1], marker="variant")  # same id, different bytes
    add_records(primary, ("20260929T303030Z-cccccccccccc",))  # the primary is not at risk

    result = run_hook(f'git worktree remove "{worktree}" && git worktree remove "{other}"',
                      primary)
    assert result.returncode == 0, result.stderr
    archive = archive_of(primary)
    assert {p.name for p in archive.iterdir()} == {worktree.name, other.name, "SHA256SUMS"}
    # each shelf holds only its own worktree's ids, under that worktree's name
    assert {p.name for p in (archive / worktree.name).iterdir()} == set(RECORD_IDS)
    assert {p.name for p in (archive / other.name).iterdir()} == {RECORD_IDS[0]}
    # and never the primary's
    assert not list(archive.rglob("20260929T303030Z-cccccccccccc*"))
    # the same id in two trees is two separate, byte-different copies
    first = (archive / worktree.name / RECORD_IDS[0] / "record.json").read_bytes()
    second = (archive / other.name / RECORD_IDS[0] / "record.json").read_bytes()
    assert first and second and first != second
    for shelf_name in (worktree.name, other.name):
        shelf = archive / shelf_name
        for source in sorted(shelf.rglob("*")):
            if source.is_file():
                line = f"{sha256_file(source)}  {source.relative_to(archive).as_posix()}"
                assert line in (archive / "SHA256SUMS").read_text(encoding="utf-8")


def test_identical_records_across_worktrees_get_one_copy_per_shelf(tmp_path):
    primary, worktree = make_site(tmp_path, records=True)
    twin = tmp_path / "wt-twin"
    _git(primary, "worktree", "add", "-q", "-b", "twin", str(twin))
    add_records(twin, RECORD_IDS)  # byte-identical to worktree's records
    result = run_hook(f'git worktree remove "{twin}"', primary)
    assert result.returncode == 0, result.stderr
    archive = archive_of(primary)
    assert {p.name for p in archive.iterdir()} == {worktree.name, twin.name, "SHA256SUMS"}
    for tree in (worktree, twin):
        assert {p.name for p in (archive / tree.name).iterdir()} == set(RECORD_IDS)
        assert not list((archive / tree.name).glob("*~*")), \
            "identical bytes must not spawn ~2 version dirs"


def test_two_worktrees_with_the_same_basename_share_one_shelf(tmp_path):
    """Two shelves with the same name are one directory: identical ids dedupe,
    differing ids sit beside each other — no record is lost either way."""
    primary, worktree = make_site(tmp_path, records=True)
    sibling = tmp_path / "elsewhere" / "wt-run"  # same basename as `worktree`
    sibling.parent.mkdir(parents=True)
    _git(primary, "worktree", "add", "-q", "-b", "third", str(sibling))
    add_records(sibling, (RECORD_IDS[1],), marker="sibling")  # same id, different bytes
    result = run_hook(f'git worktree remove "{sibling}"', primary)
    assert result.returncode == 0, result.stderr
    shelf = shelf_of(primary, worktree)
    assert {p.name for p in shelf.iterdir()} == \
        {RECORD_IDS[0], RECORD_IDS[1], f"{RECORD_IDS[1]}~2"}


# --- (i) worktree enumeration failure fails closed with exit 2 ------------------

def test_enumeration_failure_fails_closed(tmp_path):
    outside = tmp_path / "not-a-repo"
    outside.mkdir()
    primary = tmp_path / "primary"  # only used as the hook process's cwd
    primary.mkdir()
    # GIT_CEILING_DIRECTORIES keeps git from discovering a repo above the tmp dir
    env = dict(os.environ, GIT_CEILING_DIRECTORIES=str(outside))
    payload = json.dumps({"tool_name": "Bash",
                          "tool_input": {"command": "git worktree remove wt"},
                          "cwd": str(outside)})
    result = subprocess.run([sys.executable, str(GUARD)], input=payload,
                            capture_output=True, text=True, encoding="utf-8",
                            errors="replace", cwd=str(primary), env=env,
                            check=False, timeout=120)
    assert result.returncode == 2
    assert len(result.stderr.strip().splitlines()) == 1, "one reason line"
    assert "guard_worktree_evidence" in result.stderr
    assert result.stdout == ""


# --- (j) the manifest: idempotent appends, conflicting hashes refused -----------

def test_manifest_rejects_a_path_with_two_hashes(site):
    primary, worktree = site
    archive = archive_of(primary)
    source = worktree / ".cache" / "fp-verification" / RECORD_IDS[0] / "record.json"
    real = sha256_file(source)
    fake = ("0" if real[0] != "0" else "1") + real[1:]
    archive.mkdir(parents=True)
    name = f"{worktree.name}/{RECORD_IDS[0]}/record.json"
    (archive / "SHA256SUMS").write_text(f"{fake}  {name}\n", encoding="utf-8")
    sums_before = (archive / "SHA256SUMS").read_bytes()

    result = run_hook(remove_command(worktree), primary)
    assert result.returncode == 2
    assert len(result.stderr.strip().splitlines()) == 1
    assert name in result.stderr, "the conflicting path must be named"
    assert result.stdout == ""
    assert (archive / "SHA256SUMS").read_bytes() == sums_before
    # the records are still in place for a retry
    assert source.is_file()


def test_manifest_appends_of_identical_lines_are_idempotent(site):
    primary, worktree = site
    records = worktree / ".cache" / "fp-verification"
    lines = []
    for identity in RECORD_IDS:
        for source in sorted((records / identity).rglob("*")):
            if source.is_file():
                relative = (Path(worktree.name) / identity
                            / source.relative_to(records / identity)).as_posix()
                lines.append(f"{sha256_file(source)}  {relative}")
    archive = archive_of(primary)
    archive.mkdir(parents=True)
    (archive / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")
    before = (archive / "SHA256SUMS").read_bytes()

    result = run_hook(remove_command(worktree), primary)
    assert result.returncode == 0, result.stderr
    assert (archive / "SHA256SUMS").read_bytes() == before, "identical lines re-appended"
    for line in lines:
        assert (archive / "SHA256SUMS").read_text(encoding="utf-8").count(line) == 1


# --- (k) the command's spelling never selects the worktree ---------------------

def test_powershell_spelling_with_a_nonexistent_windows_path(site):
    """(P1) A PowerShell command naming an unquoted Windows path that does not
    exist still archives the real linked worktree: the trigger never trusts the
    command's paths, so a misspelled one cannot cost the evidence."""
    primary, worktree = site
    command = (r"Set-Location C:\Somewhere\Else; "
               r"git worktree remove C:\Users\me\not-the-real-path")
    result = run_hook(command, primary, tool_name="PowerShell")
    assert result.returncode == 0, result.stderr
    assert len(result.stdout.strip().splitlines()) == 1, result.stdout
    assert str(len(RECORD_IDS)) in result.stdout
    shelf = shelf_of(primary, worktree)
    assert {p.name for p in shelf.iterdir()} == set(RECORD_IDS)
    for identity in RECORD_IDS:
        assert (shelf / identity / "record.json").is_file()


@pytest.mark.parametrize("command", [
    "git -Cfoo worktree remove bar",
    "git -C a -C b worktree remove c",
])
def test_dash_c_spellings_archive_the_real_linked_worktree(site, command):
    """(P2a) `-C` points git at some other repo; it never points this hook away
    from the worktrees that actually hold records."""
    primary, worktree = site
    result = run_hook(command, primary)
    assert result.returncode == 0, result.stderr
    assert len(result.stdout.strip().splitlines()) == 1, result.stdout
    assert {p.name for p in shelf_of(primary, worktree).iterdir()} == set(RECORD_IDS)
    assert (shelf_of(primary, worktree) / RECORD_IDS[0] / "record.json").is_file()


def test_a_command_without_both_words_never_spawns_git(monkeypatch, mod, site):
    """A non-match is decided on the command text alone: git is not called."""
    primary, worktree = site

    def must_not_run(*args, **kwargs):
        raise AssertionError(f"git was spawned for a non-match: {args!r}")

    monkeypatch.setattr(mod.subprocess, "run", must_not_run)
    assert run_main(monkeypatch, mod, "git worktree list --porcelain", primary) == 0
    assert not (primary / "local_artifacts").exists()


# --- (l) a record rewritten in place gets a sibling version ---------------------

def test_a_changed_record_gets_a_second_version_and_freezes_the_first(site):
    """(P2b) Same worktree, two runs, a record whose bytes changed in between:
    the shelf then holds `<id>` *and* `<id>~2`, the first version's bytes are
    exactly what the first run archived, and SHA256SUMS still verifies."""
    primary, worktree = site
    archive, shelf = archive_of(primary), shelf_of(primary, worktree)
    record = worktree / ".cache" / "fp-verification" / RECORD_IDS[0] / "record.json"

    def status(value: str) -> None:
        record.write_text(json.dumps({"run_id": RECORD_IDS[0], "status": value}),
                          encoding="utf-8")

    status("running")
    assert run_hook(remove_command(worktree), primary).returncode == 0
    first = (shelf / RECORD_IDS[0] / "record.json").read_bytes()
    assert json.loads(first)["status"] == "running"
    before = snapshot(archive)

    status("completed")
    result = run_hook(remove_command(worktree), primary)
    assert result.returncode == 0, result.stderr
    assert {p.name for p in shelf.iterdir()} == \
        {RECORD_IDS[0], f"{RECORD_IDS[0]}~2", RECORD_IDS[1]}
    # the first version is byte-for-byte what the first run archived
    assert (shelf / RECORD_IDS[0] / "record.json").read_bytes() == first
    assert json.loads((shelf / f"{RECORD_IDS[0]}~2" / "record.json")
                      .read_text(encoding="utf-8"))["status"] == "completed"
    # the untouched record was not rewritten either
    for source in sorted((shelf / RECORD_IDS[1]).rglob("*")):
        if source.is_file():
            key = str(source.relative_to(archive))
            assert (source.stat().st_mtime_ns, sha256_file(source)) == before[key]

    lines = (archive / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    names = [line.partition("  ")[2] for line in lines]
    assert len(names) == len(set(names)) == 9, "each path listed exactly once"
    covered = {p.relative_to(archive).as_posix() for p in archive.rglob("*")
               if p.is_file() and p.name != "SHA256SUMS"}
    assert set(names) == covered
    for line in lines:  # what `sha256sum -c SHA256SUMS` does, recomputed here
        digest, separator, name = line.partition("  ")
        assert separator and re.fullmatch(r"[0-9a-f]{64}", digest), line
        assert (archive / name).is_file(), line
        assert sha256_file(archive / name) == digest, line


# --- (m) a retention failure cleans up after itself -----------------------------

def test_a_copy_failure_blocks_and_leaves_no_staging_dir(monkeypatch, mod, site):
    """A copy that dies mid-record blocks the removal (exit 2) and leaves neither
    a final version dir for that record nor a `.staging-*` directory anywhere
    under the archive; the source records are untouched."""
    primary, worktree = site
    archive = archive_of(primary)
    before = snapshot(worktree)
    copies: list[Path] = []
    real_copyfile = shutil.copyfile

    def flaky(src, dst, **kwargs):
        copies.append(Path(str(src)))
        if len(copies) == 2:  # the second file of the first record
            raise OSError("simulated copy failure")
        return real_copyfile(src, dst, **kwargs)

    monkeypatch.setattr(mod.shutil, "copyfile", flaky)
    assert run_main(monkeypatch, mod, remove_command(worktree), primary) == 2
    assert len(copies) == 2, "the failure was expected on the record's second file"
    assert not list(archive.rglob(".staging-*")), "a staging dir was left behind"
    for identity in RECORD_IDS:  # no final version dir for the failed record
        assert not (archive / worktree.name / identity).exists()
    assert not list(archive.rglob("*~*"))
    assert not (archive / "SHA256SUMS").exists()
    assert snapshot(worktree) == before, "the source records must be unchanged"


# --- the hook must stay wired into Claude Code ----------------------------------

def test_hook_is_registered_for_bash_and_powershell():
    """An unwired retention hook is the silent-loss failure this hook exists to stop."""
    settings = json.loads((REPO / ".claude" / "settings.json").read_text(encoding="utf-8"))
    pre = settings.get("hooks", {}).get("PreToolUse", [])
    for matcher in ("Bash", "PowerShell"):
        entries = [h.get("command", "") for group in pre if group.get("matcher") == matcher
                   for h in group.get("hooks", [])]
        assert any("guard_worktree_evidence.py" in command for command in entries), matcher
