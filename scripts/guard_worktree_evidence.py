#!/usr/bin/env python3
"""guard_worktree_evidence.py — copy launcher verification records out of a worktree
before `git worktree remove` deletes the only copy.

Why. `scripts/fp.py` writes every `test` / `test-ops` / `python -m pytest` / `check`
run's evidence into the *checkout's own* ignored `.cache/fp-verification/<run-id>/`
directory (scripts/README.md, "Automatic verification evidence"). A linked worktree
is exactly as disposable as the scratch it holds: `git worktree remove` deletes the
whole tree, records included, and the citation the operator is left holding ("the
printed record path is the evidence to cite") then points at nothing.
scripts/README.md's baseline procedure already requires "retained finalized evidence
outside the worktree" before `git worktree remove <exact registered path>` — this
hook is the mechanical half of that rule, so the retention cannot depend on the
remover remembering it. Same loss class as M-41 (private artifacts inside a worktree
die with the worktree); this hook covers the launcher records specifically.

What it does. Registered as a `PreToolUse` hook for both the Bash and the PowerShell
matcher in `.claude/settings.json` (the entry mirrors `guard_shell_command.py`'s):

    {"matcher": "Bash"|"PowerShell",
     "hooks": [{"type": "command",
                "command": "python \\"$CLAUDE_PROJECT_DIR/scripts/guard_worktree_evidence.py\\""}]}

It reads the tool payload on stdin (`tool_input.command`, with the payload's `cwd`
for relative paths). Commands are tokenized with `scripts/_shell_tokens.py` in strict
mode, as `guard_shell_command.py` reads them, and judged in command position, so data
(an `echo "git worktree remove"`, a grep pattern) never triggers a copy. Detected:
`git worktree remove [-f|--force] <path>`, with git global options (`git -C <dir>
worktree remove ...`), wrappers (`sudo`/`env`/`bash -c`), and a leading `cd <dir> &&
...` resolving a relative `<path>`.

For each removal whose `<path>/.cache/fp-verification/` holds record directories, it
copies every file to

    <primary>/local_artifacts/fp-verification-archive/<worktree-basename>/<record-id>/

and appends `<sha256>  <worktree-basename>/<record-id>/<file>` lines to the archive's
`SHA256SUMS` (paths relative to `fp-verification-archive/`, so `sha256sum -c` works
from there). `<primary>` is the parent of `git rev-parse --path-format=absolute
--git-common-dir` run in `<path>` — the main checkout for a linked worktree, whose
`local_artifacts/` is already gitignored and local-only by design. A second run is
idempotent: byte-identical copies are left alone and already-recorded sum lines are
not appended again.

The hook never deletes anything and never writes outside the archive directory; the
source worktree is only ever read.

Exit contract:

  * **0, silent** when the command does not match or the worktree holds no records
    (printing an `allow` decision would bypass the operator's permission rules, and
    a summary with nothing archived is noise);
  * **0, one stdout line** summarizing the record count and the archive location —
    stdout, not a permission decision, because the removal itself is not judged
    here (`guard_shell_command.py` owns destructive-command asking);
  * **2, reason on stderr** when records exist but could not be copied — a blocking
    exit, so the tool call is refused *before* the records are destroyed. Losing the
    evidence is not recoverable after the fact; asking the operator to clear the
    failure (or archive by hand) is the cheap direction to fail.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

try:  # imported as `scripts.guard_worktree_evidence` (tests, repo root on sys.path)
    from scripts._shell_tokens import ShellSyntaxError, expand, program, segments
except ImportError:  # run as `python scripts/guard_worktree_evidence.py`
    from _shell_tokens import ShellSyntaxError, expand, program, segments

# Where scripts/fp.py writes launcher verification records (scripts/README.md).
RECORDS_DIR = Path(".cache") / "fp-verification"
# Where this hook retains them: under the primary checkout's gitignored local root.
ARCHIVE_REL = Path("local_artifacts") / "fp-verification-archive"
SUMS_NAME = "SHA256SUMS"
# git global options that take the next word as their value — the same table
# scripts/guard_shell_command.py walks to find the subcommand.
GIT_GLOBAL_VALUES = frozenset({"-C", "-c", "--git-dir", "--work-tree", "--namespace",
                               "--config-env", "--super-prefix", "--attr-source",
                               "--shallow-file"})


class ArchiveError(RuntimeError):
    """Records exist but could not be retained; the removal must not proceed."""


def command_of(data: dict) -> str:
    """Extract the shell command from the payload shapes we accept.

    Same tolerant reader as `scripts/guard_shell_command.py`: Claude Code's
    PreToolUse `tool_input.command` first, then the legacy flat keys. An
    unrecognised shape yields "" (no match, exit 0).
    """
    if not isinstance(data, dict):
        return ""
    for key in ("command", "shell_command", "cmd"):
        val = data.get(key)
        if isinstance(val, str) and val:
            return val
    tool_input = data.get("tool_input")
    if isinstance(tool_input, dict):
        val = tool_input.get("command")
        if isinstance(val, str):
            return val
    return ""


def _worktree_removal(words: list[str]) -> tuple[str, str | None] | None:
    """(`<path>`, `-C <dir>` value or None) when `words` run `git worktree remove`,
    else None.

    git global options are skipped to find the subcommand; every `-`-prefixed word
    after `remove` (``-f``, ``--force``, ...) is skipped to find the path operand.
    """
    if program(words[0], strict=True) != "git":
        return None
    index, chdir = 1, None
    while index < len(words) and words[index].startswith("-"):
        word = words[index]
        if word in GIT_GLOBAL_VALUES and index + 1 < len(words):
            if word == "-C":
                chdir = words[index + 1]
            index += 2
            continue
        index += 1  # a valueless global option, or one with an attached `=value`
    if index >= len(words) or words[index] != "worktree":
        return None
    index += 1
    while index < len(words) and words[index].startswith("-"):
        index += 1
    if index >= len(words) or words[index] != "remove":
        return None
    index += 1
    while index < len(words) and words[index].startswith("-"):
        index += 1
    if index >= len(words):
        return None
    return words[index], chdir


def removals(command: str, base: Path) -> list[tuple[Path, Path]]:
    """(worktree path, the directory it resolves from) for every `git worktree
    remove` in `command`, in the order the shell runs them.

    A `cd <dir>` command moves the base for everything after it, as in bash;
    `git -C <dir>` moves it for that git invocation alone. A command the strict
    reader cannot parse yields nothing — bash would reject it before running any
    removal, so there is nothing to retain for.
    """
    try:
        parsed = segments(command, strict=True)
    except (ShellSyntaxError, IndexError, RecursionError):
        return []
    found: list[tuple[Path, Path]] = []
    running = base
    for segment in parsed:
        try:
            commands = expand(segment, strict=True)
        except (ShellSyntaxError, IndexError, RecursionError):
            continue  # this segment is unreadable; the next may still remove a worktree
        for words in commands:
            if not words:
                continue
            if program(words[0], strict=True) == "cd":
                operands = [word for word in words[1:] if not word.startswith("-")]
                if len(operands) == 1:
                    running = (running / operands[0]).resolve()
                continue
            hit = _worktree_removal(words)
            if hit is None:
                continue
            path_text, chdir = hit
            origin = (running / chdir).resolve() if chdir else running
            found.append(((origin / path_text).resolve(), origin))
    return found


def sha256_file(path: Path) -> str:
    """Streamed SHA-256 of a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def primary_checkout(where: Path) -> Path:
    """The main checkout `where` belongs to: the parent of the common git directory.

    `git rev-parse --path-format=absolute --git-common-dir` reports the shared
    `<primary>/.git` from inside any linked worktree and `.git` itself from the
    primary, so the parent is the primary either way.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
            cwd=str(where), capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=30, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ArchiveError(f"cannot locate the primary checkout from {where}: {exc}") from exc
    common = result.stdout.strip()
    if result.returncode or not common:
        raise ArchiveError(f"cannot locate the primary checkout from {where}: "
                           f"{(result.stderr or 'git rev-parse --git-common-dir failed').strip()}")
    path = Path(common)
    if not path.is_absolute():
        path = where / path
    return path.resolve().parent


def _append_sums(sums: Path, lines: list[str]) -> None:
    """Append the sha256 lines that are not recorded yet (idempotent)."""
    try:
        known = set(sums.read_text(encoding="utf-8").splitlines()) if sums.is_file() else set()
    except ValueError as exc:  # a corrupt manifest: fail loudly, never double-append
        raise ArchiveError(f"cannot read {sums}: {exc}") from exc
    fresh = [line for line in dict.fromkeys(lines) if line not in known]
    if not fresh:
        return
    with sums.open("a", encoding="utf-8", newline="\n") as handle:
        for line in fresh:
            handle.write(line + "\n")


def archive_records(target: Path, cwd: Path) -> tuple[int, Path]:
    """Copy every verification record under `target` into the primary's archive.

    Returns (record count, archive directory). A worktree with no records is a
    no-op and returns (0, ...) — the caller stays silent. Never deletes anything
    and never writes outside `archive`.
    """
    records = target / RECORDS_DIR
    identities = sorted(path for path in records.iterdir() if path.is_dir()) \
        if records.is_dir() else []
    if not identities:
        return 0, target
    primary = primary_checkout(target if target.is_dir() else cwd)
    archive = primary / ARCHIVE_REL
    name = target.name
    lines: list[str] = []
    try:
        for record in identities:
            for source in sorted(record.rglob("*")):
                if source.is_dir():
                    continue
                digest = sha256_file(source)
                relative = Path(name) / record.name / source.relative_to(record)
                destination = archive / relative
                if not (destination.is_file() and sha256_file(destination) == digest):
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source, destination)
                    if sha256_file(destination) != digest:
                        raise ArchiveError(f"copy of {source} did not verify")
                lines.append(f"{digest}  {relative.as_posix()}")
        _append_sums(archive / SUMS_NAME, lines)
    except OSError as exc:
        raise ArchiveError(f"cannot retain verification records from {target}: {exc}") from exc
    return len(identities), archive


def main() -> int:
    """Read the PreToolUse payload; retain records; exit 0, or 2 when they cannot
    be retained."""
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    command = command_of(data)
    if not command:
        return 0
    stated = data.get("cwd") if isinstance(data, dict) else None
    base = Path(stated) if isinstance(stated, str) and stated else Path.cwd()
    try:
        base = base.resolve()
    except OSError:
        base = Path.cwd()
    try:
        targets: list[Path] = []
        for target, _origin in removals(command, base):
            if target not in targets:
                targets.append(target)
        for target in targets:
            count, archive = archive_records(target, base)
            if count:
                print(f"guard_worktree_evidence: archived {count} verification "
                      f"record(s) from {target} to {archive}")
    except (ArchiveError, OSError) as exc:
        print(f"guard_worktree_evidence: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
