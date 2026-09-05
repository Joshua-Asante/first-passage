"""Tests for scripts/private_content_scan.py — in-memory needle scan of a commit range.

Campaign-state §47b step 6b (2026-09-04): the pre-push scan builds needles in
memory from private files, scans ADDED lines and commit messages only, reports
locations never tokens, walks trees for forbidden paths, and exits 3 rather than
"clean" when a needle source is missing or a class is empty.
"""
from __future__ import annotations

import base64
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SCRIPT = _REPO / "scripts" / "private_content_scan.py"

needs_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not on PATH")
# Filenames containing a tab, a carriage return, a glob character, or bytes that
# are not valid UTF-8 cannot be CREATED on Windows: the fixture fails before the
# scanner runs. The step 6b preconditions name Windows/PowerShell as a supported
# worker host and require this file to pass there, so these cases skip rather
# than fail. CI is ubuntu-only and would never have surfaced it.
posix_only = pytest.mark.skipif(os.name != "posix", reason="filename form is POSIX-only")

_JSON = '{"strategy_id": "x", "inputs": {"Alpha Length": 3, "Mode": "Aggressive", "Threshold": 1.25, "Enabled": true}}\n'
_CSV = "Trade #,Type,Date/Time,Price,P&L\n1,Long,2026-03-12 09:35,41237.5,312.50\n2,Short,2026-03-13 10:05,41190.25,-88.00\n"


def _env() -> dict[str, str]:
    """Author and committer identity for the temp repos.

    Supplied through the environment, never a global config: CI runners have no
    global git identity, and a git subcommand that needs one aborts there while
    passing on a developer box.
    """
    env = dict(os.environ)
    env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = "2026-09-04T12:00:00+00:00"
    env["GIT_AUTHOR_NAME"] = env["GIT_COMMITTER_NAME"] = "t"
    env["GIT_AUTHOR_EMAIL"] = env["GIT_COMMITTER_EMAIL"] = "t@example.invalid"
    return env


def _git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, check=True, env=_env(), capture_output=True, text=True).stdout


def _git_try(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Same identity, but a non-zero status is a result rather than an error."""
    return subprocess.run(["git", *args], cwd=root, env=_env(), capture_output=True, text=True)


def _run(root: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(_SCRIPT), "--repo", str(root), "--range", "base..HEAD", *extra],
        capture_output=True,
        text=True,
    )


@pytest.fixture()
def repo(tmp_path: Path) -> tuple[Path, Path, Path]:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q", "-b", "main")
    (root / "notes.md").write_text("context line mentions Aggressive mode already\nsecond line\n", encoding="utf-8")
    _git(root, "add", "notes.md")
    _git(root, "commit", "-q", "-m", "base")
    _git(root, "branch", "base")
    private = tmp_path / "private"
    private.mkdir()
    snap = private / "x.json"
    snap.write_text(_JSON, encoding="utf-8")
    export = private / "x.csv"
    export.write_text(_CSV, encoding="utf-8")
    return root, snap, export


@needs_git
def test_clean_range_exits_zero(repo: tuple[Path, Path, Path]) -> None:
    root, snap, export = repo
    (root / "notes.md").write_text("context line mentions Aggressive mode already\nsecond line changed\n", encoding="utf-8")
    _git(root, "commit", "-q", "-am", "harmless edit")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 0, proc.stdout
    assert "SCAN result=CLEAN" in proc.stdout
    # the unchanged context line carrying "Aggressive" is not a hit
    assert "HIT" not in proc.stdout


@needs_git
def test_pair_in_added_line_and_cell_in_message_are_located_without_tokens(repo: tuple[Path, Path, Path]) -> None:
    root, snap, export = repo
    (root / "cfg.json").write_text('{"Mode": "Aggressive", "n": 1}\n', encoding="utf-8")
    _git(root, "add", "cfg.json")
    _git(root, "commit", "-q", "-m", "add cfg\n\nrow was 41237.5 at the time")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2, proc.stdout
    assert "HIT class=PAIR" in proc.stdout and "file=cfg.json line=1" in proc.stdout
    assert "HIT class=CELL" in proc.stdout and "file=<commit message>" in proc.stdout
    for token in ("Aggressive", "41237.5", "1.25", "Alpha Length"):
        assert token not in proc.stdout


@needs_git
def test_detached_trivial_scalar_is_not_a_needle_but_title_is(repo: tuple[Path, Path, Path]) -> None:
    root, snap, export = repo
    (root / "a.txt").write_text("value 3 and true appear here\n", encoding="utf-8")
    _git(root, "add", "a.txt")
    _git(root, "commit", "-q", "-m", "trivial scalars only")
    assert _run(root, "--json", str(snap), "--csv", str(export)).returncode == 0
    (root / "b.txt").write_text("we set Alpha Length on the chart\n", encoding="utf-8")
    _git(root, "add", "b.txt")
    _git(root, "commit", "-q", "-m", "title leak")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "HIT class=TITLE" in proc.stdout and "file=b.txt" in proc.stdout


@needs_git
def test_matching_is_substring_and_fails_closed(repo: tuple[Path, Path, Path]) -> None:
    """A needle extended by more text is still a hit.

    This pinned the opposite until the adversarial panel of 2026-09-05 showed
    the word boundary was a bypass: it counted "_" and digits as word
    characters, so a private value glued into a longer identifier, filename or
    commit message matched nothing -- and the report printed such a path
    verbatim, because ``_redact`` used the same patterns. A coincidental hit is
    adjudicated under the step 6b rule; a missed one is published.
    """
    root, snap, export = repo
    (root / "c.txt").write_text("Aggressively is a longer word; 141237.5 is a longer number\n", encoding="utf-8")
    _git(root, "add", "c.txt")
    _git(root, "commit", "-q", "-m", "needles extended by more text")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2
    assert "HIT class=VALUE" in proc.stdout and "file=c.txt" in proc.stdout


@needs_git
def test_needle_glued_to_an_underscore_is_caught(repo: tuple[Path, Path, Path]) -> None:
    root, snap, export = repo
    (root / "u.txt").write_text("token = Aggressive_backup\n", encoding="utf-8")
    _git(root, "add", "u.txt")
    _git(root, "commit", "-q", "-m", "glued to an underscore")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "file=u.txt" in proc.stdout


@needs_git
@posix_only
def test_filename_bytes_that_are_not_utf8_are_still_scanned(repo: tuple[Path, Path, Path]) -> None:
    """git output is read as bytes and decoded with surrogateescape.

    Under ``errors="replace"`` the name came back with U+FFFD in it, the
    ``:(literal)`` pathspec built from it matched no tree entry, git exited 0
    with an empty diff, and the blob was never scanned -- a regression the
    per-path read introduced and the panel caught.
    """
    root, snap, export = repo
    raw = os.path.join(os.fsencode(str(root)), b"caf\xe9.txt")
    with open(raw, "wb") as handle:
        handle.write(b"Aggressive mode\n")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "name is not valid utf-8")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "HIT class=VALUE" in proc.stdout


@needs_git
@posix_only
def test_carriage_return_in_a_filename_is_still_scanned(repo: tuple[Path, Path, Path]) -> None:
    root, snap, export = repo
    (root / "chart\rexport.txt").write_text("Aggressive\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "cr in the name")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "HIT class=VALUE" in proc.stdout


@needs_git
def test_carriage_return_inside_an_added_line_does_not_hide_the_rest(repo: tuple[Path, Path, Path]) -> None:
    """``text=True`` turned a lone CR into a newline, splitting the record.

    Everything after the CR then landed in a fragment carrying no "+" column and
    was never scanned. git output is now captured as bytes and split on LF only.
    """
    root, snap, export = repo
    (root / "n.txt").write_bytes(b"harmless\rAggressive\n")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "cr inside the line")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "HIT class=VALUE" in proc.stdout


@needs_git
def test_exclusions_drop_public_tokens(repo: tuple[Path, Path, Path], tmp_path: Path) -> None:
    root, snap, export = repo
    (root / "anchors.json").write_text('{"net": "312.50"}\n', encoding="utf-8")
    _git(root, "add", "anchors.json")
    _git(root, "commit", "-q", "-m", "canonical anchor value")
    assert _run(root, "--json", str(snap), "--csv", str(export)).returncode == 2
    excl = tmp_path / "public.txt"
    excl.write_text("312.50\n", encoding="utf-8")
    assert _run(root, "--json", str(snap), "--csv", str(export), "--exclude", str(excl)).returncode == 0


@needs_git
def test_missing_or_empty_needle_source_exits_three_never_clean(repo: tuple[Path, Path, Path], tmp_path: Path) -> None:
    root, snap, export = repo
    proc = _run(root, "--json", str(tmp_path / "absent.json"), "--csv", str(export))
    assert proc.returncode == 3 and "SCAN result=ERROR" in proc.stdout
    empty = tmp_path / "empty.json"
    empty.write_text('{"inputs": {}}\n', encoding="utf-8")
    assert _run(root, "--json", str(empty), "--csv", str(export)).returncode == 3
    header_only = tmp_path / "h.csv"
    header_only.write_text("a,b\n", encoding="utf-8")
    assert _run(root, "--json", str(snap), "--csv", str(header_only)).returncode == 3
    assert _run(root).returncode == 3


@needs_git
def test_path_scan_flags_private_dir_and_forbidden_suffix_in_history(repo: tuple[Path, Path, Path]) -> None:
    root, snap, export = repo
    (root / "inputs" / "private_overrides").mkdir(parents=True)
    (root / "inputs" / "private_overrides" / "p.json").write_text("{}\n", encoding="utf-8")
    _git(root, "add", "-f", "inputs/private_overrides/p.json")
    _git(root, "commit", "-q", "-m", "oops")
    _git(root, "rm", "-q", "inputs/private_overrides/p.json")
    _git(root, "commit", "-q", "-m", "removed again")
    proc = _run(root, "--json", str(snap), "--csv", str(export), "--path-prefix", "inputs/private_overrides/")
    assert proc.returncode == 2 and "HIT class=PATH" in proc.stdout and "inputs/private_overrides/p.json" in proc.stdout
    (root / "data.csv").write_text("h\n1\n", encoding="utf-8")
    _git(root, "add", "data.csv")
    _git(root, "commit", "-q", "-m", "csv added")
    proc = _run(root, "--json", str(snap), "--csv", str(export), "--forbid-suffix", ".csv")
    assert proc.returncode == 2 and "file=data.csv" in proc.stdout


@needs_git
def test_bad_range_exits_four(repo: tuple[Path, Path, Path]) -> None:
    root, snap, export = repo
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--repo", str(root), "--range", "nope..HEAD", "--json", str(snap), "--csv", str(export)],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 4 and "SCAN result=ERROR" in proc.stdout


@needs_git
def test_binary_addition_fails_closed(repo: tuple[Path, Path, Path]) -> None:
    root, snap, export = repo
    (root / "inputs.png").write_bytes(b"\x89PNG\r\n\x1a\n" + bytes(64))
    _git(root, "add", "inputs.png")
    _git(root, "commit", "-q", "-m", "screenshot by mistake")
    _git(root, "rm", "-q", "inputs.png")
    _git(root, "commit", "-q", "-m", "removed again")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "HIT class=BINARY" in proc.stdout and "file=inputs.png" in proc.stdout


@needs_git
def test_merge_introduced_content_is_caught(repo: tuple[Path, Path, Path]) -> None:
    """A conflict resolution differs from BOTH parents, so the merge commit carries the hit."""
    root, snap, export = repo
    _git(root, "checkout", "-q", "-b", "side")
    (root / "shared.txt").write_text("side version\n", encoding="utf-8")
    _git(root, "add", "shared.txt")
    _git(root, "commit", "-q", "-m", "side")
    _git(root, "checkout", "-q", "main")
    (root / "shared.txt").write_text("main version\n", encoding="utf-8")
    _git(root, "add", "shared.txt")
    _git(root, "commit", "-q", "-m", "main")
    merge = _git_try(root, "merge", "--no-edit", "side")
    assert merge.returncode != 0, "the add/add merge was expected to conflict"
    assert (root / ".git" / "MERGE_HEAD").exists(), merge.stderr
    (root / "shared.txt").write_text("resolved with Aggressive\n", encoding="utf-8")
    (root / "resolved.csv").write_text("h\n1\n", encoding="utf-8")
    _git(root, "add", "shared.txt", "resolved.csv")
    _git(root, "commit", "-q", "--no-edit")
    merge = _git(root, "rev-parse", "HEAD").strip()[:8]
    proc = _run(root, "--json", str(snap), "--csv", str(export), "--forbid-suffix", ".csv")
    assert proc.returncode == 2, proc.stdout
    assert f"HIT class=VALUE commit={merge} file=shared.txt" in proc.stdout
    assert f"HIT class=PATH commit={merge} file=resolved.csv" in proc.stdout


@needs_git
def test_merging_an_out_of_range_parent_is_not_reported(repo: tuple[Path, Path, Path]) -> None:
    """Merging a mainline that carries a binary and a .csv must not stop the packet.

    The mainline commits are outside the scanned range; the merge introduces
    nothing that differs from both parents, so a first-parent-only read would
    false-positive here and an all-parents read does not.
    """
    root, snap, export = repo
    _git(root, "checkout", "-q", "-b", "mainline")
    (root / "chart.png").write_bytes(b"\x89PNG\r\n\x1a\n" + bytes(64))
    (root / "vendor.csv").write_text("h\n1\n", encoding="utf-8")
    _git(root, "add", "chart.png", "vendor.csv")
    _git(root, "commit", "-q", "-m", "mainline moves on")
    _git(root, "checkout", "-q", "main")
    (root / "work.txt").write_text("branch work\n", encoding="utf-8")
    _git(root, "add", "work.txt")
    _git(root, "commit", "-q", "-m", "branch work")
    _git(root, "merge", "-q", "--no-ff", "--no-edit", "mainline")
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--repo", str(root), "--range", "mainline..HEAD",
         "--json", str(snap), "--csv", str(export), "--forbid-suffix", ".csv"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stdout
    assert "SCAN result=CLEAN" in proc.stdout


@needs_git
def test_non_ascii_path_under_a_forbidden_prefix_is_caught(repo: tuple[Path, Path, Path]) -> None:
    """core.quotePath would C-quote this path and defeat a startswith test."""
    root, snap, export = repo
    (root / "inputs" / "private_overrides").mkdir(parents=True)
    (root / "inputs" / "private_overrides" / "\u00e9.json").write_text("{}\n", encoding="utf-8")
    _git(root, "add", "-f", "inputs/private_overrides/\u00e9.json")
    _git(root, "commit", "-q", "-m", "non-ascii capture")
    proc = _run(root, "--json", str(snap), "--csv", str(export), "--path-prefix", "inputs/private_overrides/")
    assert proc.returncode == 2, proc.stdout
    assert "HIT class=PATH" in proc.stdout and "\u00e9.json" in proc.stdout


@needs_git
def test_needle_in_a_filename_is_caught(repo: tuple[Path, Path, Path]) -> None:
    """A filename is published and retained exactly like a blob."""
    root, snap, export = repo
    (root / "Aggressive.txt").write_text("nothing private inside\n", encoding="utf-8")
    _git(root, "add", "Aggressive.txt")
    _git(root, "commit", "-q", "-m", "value as a filename")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2, proc.stdout
    assert "HIT class=NAME" in proc.stdout
    # the filename carries the private token, so the reported path is redacted and
    # a digest of the true path stands in for it — the scanner's output is pasted
    # into the PR body, so printing the name verbatim would publish the value
    assert "file=<redacted>.txt" in proc.stdout
    # The redacted path is identified by a per-run INDEX, not by a digest of
    # itself: a truncated SHA-256 over a short private token is brute-forceable,
    # so the handle meant to make the hit actionable handed the token back in
    # the output that gets pasted into the PR body.
    assert "path_index=" in proc.stdout
    assert "path_sha256=" not in proc.stdout
    assert "Aggressive" not in proc.stdout


@needs_git
def test_added_line_that_renders_as_a_patch_header_is_scanned(repo: tuple[Path, Path, Path]) -> None:
    """An added line starting with '++ ' renders as '+++ ' inside the hunk."""
    root, snap, export = repo
    (root / "plus.txt").write_text("++ Aggressive\n", encoding="utf-8")
    _git(root, "add", "plus.txt")
    _git(root, "commit", "-q", "-m", "line that looks like a header")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2, proc.stdout
    assert "HIT class=VALUE" in proc.stdout and "file=plus.txt line=1" in proc.stdout


@needs_git
def test_rename_to_a_forbidden_suffix_is_caught(repo: tuple[Path, Path, Path]) -> None:
    """git classifies a rename R, which --diff-filter=A alone would miss."""
    root, snap, export = repo
    (root / "a.txt").write_text("x\n", encoding="utf-8")
    _git(root, "add", "a.txt")
    _git(root, "commit", "-q", "-m", "add a.txt")
    _git(root, "mv", "a.txt", "captured.csv")
    _git(root, "commit", "-q", "-m", "rename to a vendor suffix")
    proc = _run(root, "--json", str(snap), "--csv", str(export), "--forbid-suffix", ".csv")
    assert proc.returncode == 2, proc.stdout
    assert "HIT class=PATH" in proc.stdout and "file=captured.csv" in proc.stdout


@needs_git
def test_added_line_split_by_a_non_lf_control_character_is_scanned(repo: tuple[Path, Path, Path]) -> None:
    """git delimits patch records with LF; str.splitlines() breaks on much more.

    A needle after a lone vertical tab would land in a fragment carrying no '+'
    marker and never be scanned.
    """
    root, snap, export = repo
    (root / "vt.txt").write_text("safe\vAggressive\n", encoding="utf-8")
    _git(root, "add", "vt.txt")
    _git(root, "commit", "-q", "-m", "control character before the needle")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2, proc.stdout
    assert "HIT class=VALUE" in proc.stdout and "file=vt.txt line=1" in proc.stdout


@needs_git
def test_merge_resolution_caught_when_parents_disagree_on_binaryness(repo: tuple[Path, Path, Path]) -> None:
    """A path binary in one parent and text in the other must not fall between them.

    Intersecting each signal independently drops the text evidence (present only
    against the text parent) and the binary evidence (present only against the
    binary parent), reporting the resolution as clean.
    """
    root, snap, export = repo
    _git(root, "branch", "feature")
    (root / "f.dat").write_bytes(b"bin\x00\x00data\n")
    _git(root, "add", "f.dat")
    _git(root, "commit", "-q", "-m", "mainline binary")
    _git(root, "checkout", "-q", "feature")
    (root / "f.dat").write_text("harmless text\n", encoding="utf-8")
    _git(root, "add", "f.dat")
    _git(root, "commit", "-q", "-m", "feature text")
    merge = _git_try(root, "merge", "--no-edit", "main")
    assert merge.returncode != 0, "the add/add merge was expected to conflict"
    (root / "f.dat").write_text("resolved Aggressive\n", encoding="utf-8")
    _git(root, "add", "f.dat")
    _git(root, "commit", "-q", "--no-edit")
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--repo", str(root), "--range", "main..HEAD",
         "--json", str(snap), "--csv", str(export)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 2, proc.stdout
    # git's combined diff carries no text for a path that is binary in a parent, so
    # the gate holds through the fail-closed BINARY hit rather than a content hit
    assert "HIT class=BINARY" in proc.stdout and "file=f.dat" in proc.stdout


@needs_git
@posix_only
def test_tab_named_file_resolved_in_a_merge_is_caught(repo: tuple[Path, Path, Path]) -> None:
    """git C-quotes a header path with a tab regardless of core.quotePath.

    A header-derived name would never equal the raw NUL-delimited one, so the
    diff is taken per path with a literal pathspec and the header is never read.
    """
    root, snap, export = repo
    _git(root, "branch", "feature")
    (root / "odd\tname.txt").write_text("main side\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "main")
    _git(root, "checkout", "-q", "feature")
    (root / "odd\tname.txt").write_text("feature side\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "feature")
    merge = _git_try(root, "merge", "--no-edit", "main")
    assert merge.returncode != 0
    (root / "odd\tname.txt").write_text("resolved Aggressive\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "--no-edit")
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--repo", str(root), "--range", "main..HEAD",
         "--json", str(snap), "--csv", str(export)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 2, proc.stdout
    assert "HIT class=VALUE" in proc.stdout and "line=1" in proc.stdout


@needs_git
def test_clean_two_sided_edit_of_one_file_is_not_merge_authored(repo: tuple[Path, Path, Path]) -> None:
    """Both sides edit separate hunks of one file; the merge is clean.

    The merged file differs from both parents, but every line came from one of
    them — a needle that was already on the mainline must not be reported at the
    merge, or a routine merge of main would stop a safe packet.
    """
    root, snap, export = repo
    body = "".join(f"line{i}\n" for i in range(1, 11))
    (root / "f.txt").write_text(body, encoding="utf-8")
    _git(root, "add", "f.txt")
    _git(root, "commit", "-q", "-m", "seed f")
    _git(root, "branch", "feature")
    (root / "f.txt").write_text(body.replace("line1\n", "line1 main Aggressive\n"), encoding="utf-8")
    _git(root, "commit", "-q", "-am", "main edits the top")
    _git(root, "checkout", "-q", "feature")
    (root / "f.txt").write_text(body.replace("line10\n", "line10 feature harmless\n"), encoding="utf-8")
    _git(root, "commit", "-q", "-am", "feature edits the bottom")
    _git(root, "merge", "-q", "--no-ff", "--no-edit", "main")
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--repo", str(root), "--range", "main..HEAD",
         "--json", str(snap), "--csv", str(export)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stdout
    assert "SCAN result=CLEAN" in proc.stdout


@needs_git
def test_numeric_lexeme_and_canonical_spelling_both_match(repo: tuple[Path, Path, Path], tmp_path: Path) -> None:
    """A number keeps the spelling written in the snapshot as well as its canonical form."""
    root, _snap, export = repo
    snap = tmp_path / "lex.json"
    snap.write_text('{"inputs": {"Threshold": 1.2500, "Alpha Length": 3}}\n', encoding="utf-8")
    (root / "a.txt").write_text("threshold was 1.2500 on the chart\n", encoding="utf-8")
    _git(root, "add", "a.txt")
    _git(root, "commit", "-q", "-m", "lexeme as written")
    assert _run(root, "--json", str(snap), "--csv", str(export)).returncode == 2
    (root / "b.txt").write_text("threshold was 1.25 on the chart\n", encoding="utf-8")
    _git(root, "add", "b.txt")
    _git(root, "commit", "-q", "-m", "canonical spelling")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "file=b.txt" in proc.stdout


@needs_git
@posix_only
def test_glob_characters_in_a_filename_are_taken_literally(repo: tuple[Path, Path, Path]) -> None:
    """A per-path diff must not let git read `a*b.txt` as a pattern."""
    root, snap, export = repo
    (root / "a*b.txt").write_text("Aggressive\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "glob-looking name")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2, proc.stdout
    assert "HIT class=VALUE" in proc.stdout and "file=a*b.txt line=1" in proc.stdout


@needs_git
def test_noncanonical_numeric_lexeme_is_a_needle(repo: tuple[Path, Path, Path]) -> None:
    """Source spelling ``1.2500`` must remain a VALUE needle after json.loads.

    Parsing collapses it to ``1.25``; a worker who copied the chart's lexeme
    into an added line would otherwise miss the scan.
    """
    root, snap, export = repo
    snap.write_text(
        '{"strategy_id": "x", "inputs": {"Alpha Length": 3, "Mode": "Aggressive", '
        '"Threshold": 1.2500, "Enabled": true}}\n',
        encoding="utf-8",
    )
    (root / "cfg.txt").write_text("threshold was 1.2500 on the chart\n", encoding="utf-8")
    _git(root, "add", "cfg.txt")
    _git(root, "commit", "-q", "-m", "non-canonical numeric copy")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2, proc.stdout
    assert "HIT class=VALUE" in proc.stdout and "file=cfg.txt" in proc.stdout
    assert "1.2500" not in proc.stdout  # never echo the token


@needs_git
@posix_only
def test_cquoted_tab_path_on_merge_is_scanned(repo: tuple[Path, Path, Path]) -> None:
    """A merge resolution on a tab-named file must not evade the path filter.

    Diff headers C-quote such paths even under core.quotePath=false; name-status
    -z does not. Comparing the quoted header to the raw resolved path dropped
    every content hit on the file.
    """
    root, snap, export = repo
    tab = "odd\tname.txt"
    _git(root, "checkout", "-q", "-b", "side")
    (root / tab).write_text("side\n", encoding="utf-8")
    _git(root, "add", "-f", tab)
    _git(root, "commit", "-q", "-m", "side")
    _git(root, "checkout", "-q", "main")
    (root / tab).write_text("main\n", encoding="utf-8")
    _git(root, "add", "-f", tab)
    _git(root, "commit", "-q", "-m", "main")
    merge = _git_try(root, "merge", "--no-edit", "side")
    assert merge.returncode != 0, "the add/add merge was expected to conflict"
    (root / tab).write_text("Aggressive\n", encoding="utf-8")
    _git(root, "add", "-f", tab)
    _git(root, "commit", "-q", "--no-edit")
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--repo", str(root), "--range", "main~1..HEAD",
         "--json", str(snap), "--csv", str(export)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 2, proc.stdout
    assert "HIT class=VALUE" in proc.stdout


@needs_git
def test_merge_does_not_inherit_main_only_needle_on_co_touched_file(
    repo: tuple[Path, Path, Path],
) -> None:
    """When main and the packet edit different hunks, main's needle is not the merge's.

    The merged file differs from both parents, so a path-level union would report
    a needle that arrived solely from main. Packet ranges are ``main..HEAD``, so
    main's own commit is outside the range — only the merge must stay clean.
    """
    root, snap, export = repo
    (root / "shared.txt").write_text(
        "L1\nL2\nL3\nL4\nL5\nL6\nL7\nL8\nL9\nL10\n", encoding="utf-8"
    )
    _git(root, "add", "shared.txt")
    _git(root, "commit", "-q", "-m", "shared base")
    _git(root, "checkout", "-q", "-b", "feature")
    (root / "shared.txt").write_text(
        "L1\nL2\nL3\nL4\nL5\nL6\nL7\nL8\nL9\nL10\nfeature-tail\n", encoding="utf-8"
    )
    _git(root, "add", "shared.txt")
    _git(root, "commit", "-q", "-m", "feature hunk")
    _git(root, "checkout", "-q", "main")
    (root / "shared.txt").write_text(
        "Aggressive\nL1\nL2\nL3\nL4\nL5\nL6\nL7\nL8\nL9\nL10\n", encoding="utf-8"
    )
    _git(root, "add", "shared.txt")
    _git(root, "commit", "-q", "-m", "main hunk")
    _git(root, "checkout", "-q", "feature")
    merge = _git_try(root, "merge", "--no-edit", "main")
    assert merge.returncode == 0, merge.stderr
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--repo", str(root), "--range", "main..HEAD",
         "--json", str(snap), "--csv", str(export)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stdout
    assert "SCAN result=CLEAN" in proc.stdout

@needs_git
def test_gitattributes_cannot_reclassify_a_binary_as_text(repo: tuple[Path, Path, Path]) -> None:
    """BINARY is decided from the blob's own bytes, never from git's rendering.

    ``numstat`` reports binary only for what git *renders* as binary, and a
    ``.gitattributes`` ``diff`` override -- which never travels with the push --
    flips that verdict, so a screenshot could be scanned as if it were readable.
    """
    root, snap, export = repo
    (root / ".gitattributes").write_text("*.png -diff\n*.png diff\n", encoding="utf-8")
    (root / "shot.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 64)
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "screenshot with an attribute override")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "HIT class=BINARY" in proc.stdout


@needs_git
def test_git_lfs_pointer_fails_closed(repo: tuple[Path, Path, Path]) -> None:
    """The tree blob is three ASCII lines; the image goes to the LFS remote."""
    root, snap, export = repo
    (root / "shot.png").write_text(
        "version https://git-lfs.github.com/spec/v1\n"
        "oid sha256:0000000000000000000000000000000000000000000000000000000000000000\n"
        "size 12345\n",
        encoding="utf-8",
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "lfs pointer")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "HIT class=BINARY" in proc.stdout


@needs_git
def test_forbidden_suffix_is_case_insensitive_and_per_component(repo: tuple[Path, Path, Path]) -> None:
    root, snap, export = repo
    (root / "Striker.PINE").write_text("x\n", encoding="utf-8")
    (root / "exports.pine").mkdir()
    (root / "exports.pine" / "a.txt").write_text("y\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "cased suffix and a directory bearing one")
    proc = _run(root, "--json", str(snap), "--csv", str(export), "--forbid-suffix", ".pine")
    assert proc.returncode == 2
    assert "Striker.PINE" in proc.stdout and "exports.pine/a.txt" in proc.stdout


@needs_git
def test_empty_range_is_an_error_not_clean(repo: tuple[Path, Path, Path]) -> None:
    """Exit 0 must never mean "the scanner never looked"."""
    root, snap, export = repo
    proc = _run(root, "--json", str(snap), "--csv", str(export), "--range", "HEAD..HEAD")
    assert proc.returncode == 3
    assert "empty range" in proc.stdout and "CLEAN" not in proc.stdout

@needs_git
def test_a_deletion_only_commit_is_clean(repo: tuple[Path, Path, Path]) -> None:
    """Deletions are explicitly not flagged, and the blob-byte check must respect that.

    ``_blob_is_opaque`` fails closed when ``cat-file`` cannot resolve a path, and
    the candidate set carries every status, so a plain text deletion briefly read
    as an opaque blob and every deleting commit raised BINARY.
    """
    root, snap, export = repo
    (root / "gone.txt").write_text("hello\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "add a file to delete")
    _git(root, "rm", "-q", "gone.txt")
    _git(root, "commit", "-q", "-m", "delete it")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 0, proc.stdout
    assert "class=BINARY" not in proc.stdout


@needs_git
def test_forbidden_suffix_containing_a_slash_still_matches(repo: tuple[Path, Path, Path]) -> None:
    """The per-component test alone silently dropped any suffix with a "/" in it."""
    root, snap, export = repo
    (root / "private_overrides").mkdir()
    (root / "private_overrides" / "a.json").write_text("x\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "nested capture")
    proc = _run(root, "--json", str(snap), "--csv", str(export), "--forbid-suffix", "private_overrides/a.json")
    assert proc.returncode == 2 and "class=PATH" in proc.stdout


@needs_git
def test_needle_matching_is_case_insensitive(repo: tuple[Path, Path, Path]) -> None:
    """A differently-cased copy of a private tag is the same disclosure.

    The NAME class must not be stricter than the suffix and prefix tests applied
    to the same path.
    """
    root, snap, export = repo
    (root / "aggressive-notes.txt").write_text("x\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "lowercased tag in a filename")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "HIT class=NAME" in proc.stdout

@needs_git
def test_value_nested_below_the_json_key_is_a_needle(repo: tuple[Path, Path, Path], tmp_path: Path) -> None:
    """The snapshot walk is recursive; one level meant a nested value had no needle at all."""
    snapshot = tmp_path / "nested.json"
    snapshot.write_text(
        '{"inputs": {"Mode": "Aggressive", "group": {"deep": {"acct_tag": "ZZTESTZZ"}}}}\n',
        encoding="utf-8",
    )
    root, _, export = repo
    (root / "n.txt").write_text("carried ZZTESTZZ across\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "nested value pasted")
    proc = _run(root, "--json", str(snapshot), "--csv", str(export))
    assert proc.returncode == 2 and "HIT class=VALUE" in proc.stdout


@needs_git
def test_csv_identifier_and_whole_dollar_cells_are_needles(repo: tuple[Path, Path, Path], tmp_path: Path) -> None:
    """An identifier has no decimal point and no date; a whole-dollar figure has neither.

    Those are the two classes the threat model names, and the old
    decimal-or-date gate had no pattern for either. The header row is scanned
    too, since an identifier can be a COLUMN NAME.
    """
    export = tmp_path / "acct.csv"
    export.write_text("account,peak_balance,realized\nZZ-ACCT-777788,102500,12.50\n", encoding="utf-8")
    root, snap, _ = repo
    (root / "ledger.md").write_text("reconciled ZZ-ACCT-777788 today\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "identifier pasted")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "HIT class=CELL" in proc.stdout


@needs_git
def test_comma_grouped_spelling_of_a_numeric_cell_matches(repo: tuple[Path, Path, Path], tmp_path: Path) -> None:
    export = tmp_path / "acct.csv"
    export.write_text("account,peak_balance\nZZ-ACCT-777788,102500\n", encoding="utf-8")
    root, snap, _ = repo
    (root / "report.md").write_text("peak was 102,500 on the day\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "grouped spelling")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "HIT class=CELL" in proc.stdout


@needs_git
def test_base64_armoured_binary_fails_closed(repo: tuple[Path, Path, Path]) -> None:
    """A NUL test recognises one ENCODING of unscannable content, not the content.

    The same screenshot carried as a base64 data: URI or a notebook output cell
    is NUL-free, and fixed-string needles cannot match base64 of themselves.
    """
    root, snap, export = repo
    payload = base64.b64encode(b"PNGDATA" * 300).decode()
    (root / "capture.md").write_text(f"![shot](data:image/png;base64,{payload})\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "armoured screenshot")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "HIT class=BINARY" in proc.stdout


@needs_git
def test_branch_name_and_annotated_tag_message_are_scanned(repo: tuple[Path, Path, Path]) -> None:
    """A push carries ref names and tag objects, which no commit range expresses."""
    root, snap, export = repo
    _git(root, "checkout", "-q", "-b", "fix-Aggressive-eval")
    (root / "ok.txt").write_text("harmless\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "clean work")
    _git(root, "tag", "-a", "v9", "-m", "release notes: Aggressive")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2
    assert "HIT class=REF" in proc.stdout
    assert "refs/tags/v9 (message)" in proc.stdout


@needs_git
def test_the_printed_range_is_redacted(repo: tuple[Path, Path, Path]) -> None:
    """The range line echoes an operator-supplied ref name on the CLEAN path."""
    root, snap, export = repo
    _git(root, "checkout", "-q", "-b", "fix-Aggressive-eval")
    (root / "ok.txt").write_text("harmless\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "clean work")
    proc = _run(root, "--json", str(snap), "--csv", str(export), "--range", "base..fix-Aggressive-eval")
    assert "range fix-Aggressive-eval" not in proc.stdout
    assert "<redacted>" in proc.stdout

@needs_git
def test_a_replace_ref_cannot_hide_the_pushed_commit(repo: tuple[Path, Path, Path]) -> None:
    """Git reads follow refs/replace; a push does not carry them.

    A local replacement object redirected every read to a harmless substitute,
    so the scanner examined an object the push would never publish and reported
    CLEAN while the real blob went to the remote.
    """
    root, snap, export = repo
    (root / "leak.txt").write_text("Aggressive\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "real commit")
    real = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, env=_env()
    ).stdout.strip()
    (root / "leak.txt").write_text("harmless\n", encoding="utf-8")
    _git(root, "add", "-A")
    tree = subprocess.run(
        ["git", "write-tree"], cwd=root, capture_output=True, text=True, env=_env()
    ).stdout.strip()
    parent = subprocess.run(
        ["git", "rev-parse", "HEAD^"], cwd=root, capture_output=True, text=True, env=_env()
    ).stdout.strip()
    fake = subprocess.run(
        ["git", "commit-tree", tree, "-p", parent, "-m", "real commit"],
        cwd=root, capture_output=True, text=True, env=_env(),
    ).stdout.strip()
    _git(root, "checkout", "-q", "--", ".")
    _git(root, "replace", "-f", real, fake)
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "HIT class=VALUE" in proc.stdout


@needs_git
def test_diff_noprefix_cannot_corrupt_a_path(repo: tuple[Path, Path, Path]) -> None:
    """The a/ and b/ patch prefixes are pinned before a header path is decoded.

    With ``diff.noprefix=true`` a real path that itself begins with ``b/`` was
    stripped to its tail, so it no longer equalled the raw name and a merge's
    hits on it were dropped.
    """
    root, snap, export = repo
    _git(root, "config", "diff.noprefix", "true")
    (root / "b").mkdir()
    (root / "b" / "f.txt").write_text("base\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "seed the prefixed path")
    _git(root, "checkout", "-q", "-b", "side")
    (root / "b" / "f.txt").write_text("side\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "side")
    _git(root, "checkout", "-q", "-")
    (root / "b" / "f.txt").write_text("mainline\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "mainline")
    _git_try(root, "merge", "--no-commit", "side")
    (root / "b" / "f.txt").write_text("Aggressive\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "resolution carrying a needle")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2
    assert "file=b/f.txt" in proc.stdout

@needs_git
def test_an_external_differ_cannot_silence_the_text_scan(repo: tuple[Path, Path, Path], tmp_path: Path) -> None:
    """diff.external replaces the patch text, emptying every text class at once.

    A comment once claimed --no-ext-diff was passed; it was not. This test is
    what keeps the claim and the code together.
    """
    root, snap, export = repo
    (root / "cfg.json").write_text('{"Mode": "Aggressive"}\n', encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "config with a needle")
    quiet = tmp_path / "quiet.sh"
    quiet.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    quiet.chmod(0o755)
    _git(root, "config", "diff.external", str(quiet))
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "HIT class=VALUE" in proc.stdout


@needs_git
def test_git_external_diff_from_the_environment_is_dropped(repo: tuple[Path, Path, Path], tmp_path: Path) -> None:
    """The variable is inherited from whoever runs the scanner, not from the repo."""
    root, snap, export = repo
    (root / "cfg.json").write_text('{"Mode": "Aggressive"}\n', encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "config with a needle")
    quiet = tmp_path / "quiet.sh"
    quiet.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    quiet.chmod(0o755)
    env = _env()
    env["GIT_EXTERNAL_DIFF"] = str(quiet)
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--repo", str(root), "--range", "base..HEAD",
         "--json", str(snap), "--csv", str(export)],
        capture_output=True, text=True, env=env,
    )
    assert proc.returncode == 2 and "HIT class=VALUE" in proc.stdout


@needs_git
def test_a_replace_ref_on_a_blob_cannot_hide_a_binary(repo: tuple[Path, Path, Path]) -> None:
    """The blob-byte read is the one call that used to bypass the pinned wrapper."""
    root, snap, export = repo
    (root / "shot.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 64)
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "screenshot")
    blob = subprocess.run(
        ["git", "rev-parse", "HEAD:shot.png"], cwd=root, capture_output=True, text=True, env=_env()
    ).stdout.strip()
    placeholder = subprocess.run(
        ["git", "hash-object", "-w", "--stdin"], cwd=root, input="placeholder\n",
        capture_output=True, text=True, env=_env(),
    ).stdout.strip()
    _git(root, "replace", "-f", blob, placeholder)
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "HIT class=BINARY" in proc.stdout


@needs_git
def test_wrapped_base64_carrier_fails_closed(repo: tuple[Path, Path, Path]) -> None:
    """Base64 is conventionally wrapped, which breaks any contiguous-run test."""
    root, snap, export = repo
    payload = base64.b64encode(b"\x89PNG\r\n\x1a\n" + bytes(range(256)) * 40).decode()
    wrapped = "\n".join(payload[i : i + 64] for i in range(0, len(payload), 64))
    (root / "shot.b64").write_text(wrapped + "\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "wrapped carrier")
    proc = _run(root, "--json", str(snap), "--csv", str(export))
    assert proc.returncode == 2 and "HIT class=BINARY" in proc.stdout


@needs_git
def test_a_non_distinctive_value_is_redacted_and_its_drop_reported(
    repo: tuple[Path, Path, Path], tmp_path: Path
) -> None:
    """Too plain to be a needle, still private enough to keep out of the report."""
    snapshot = tmp_path / "short.json"
    snapshot.write_text('{"inputs": {"acct_tag": "ZZTZ", "Mode": "Aggressive"}}\n', encoding="utf-8")
    root, _, export = repo
    (root / "ZZTZ_export.png").write_bytes(b"\x00\x01\x02")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "binary named after the short tag")
    proc = _run(root, "--json", str(snapshot), "--csv", str(export))
    assert proc.returncode == 2
    assert "no VALUE needle" in proc.stdout and "acct_tag" in proc.stdout
    assert "ZZTZ" not in proc.stdout


def test_every_diff_call_pins_the_format() -> None:
    """A new diff call site must not quietly miss the flags.

    The comment block claimed --no-ext-diff/--no-textconv before any call site
    passed them; this asserts the code, not the comment.
    """
    source = _SCRIPT.read_text(encoding="utf-8")
    for call in re.findall(r'_git\(\[("diff"[^\]]*)\]', source):
        assert "--no-ext-diff" in call, call
    assert 'subprocess.run(\n        ["git"' not in source or source.count('["git", "--no-replace-objects"') >= 1
