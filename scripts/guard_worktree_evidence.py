#!/usr/bin/env python3
r"""guard_worktree_evidence.py — copy launcher verification records out of linked
worktrees before `git worktree remove` deletes the only copy.

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
as the base directory). The trigger is deliberately dumb: the case-insensitive
regex `\bworktree\b[\s\S]*\bremove\b` over the whole command text, with no
tokenising and no path parsing. Which worktree the command names never matters,
because every linked worktree's records are equally disposable and the archive is
idempotent — so over-triggering (an `echo` that merely mentions both words, a
`worktree`/`remove` pair in unrelated data) only costs a redundant copy check,
while under-triggering on a spelling the parser missed would lose evidence. When
the trigger fires the hook never trusts the command's paths at all; it asks git
what the worktrees are:

    git -C <base> worktree list --porcelain

The first entry is the primary checkout; every later entry that still exists on
disk is a linked worktree whose `.cache/fp-verification/<run-id>/` records are
copied into that worktree's own shelf — the worktree's basename — so a retained
record always says which tree it came from:

    <primary>/local_artifacts/fp-verification-archive/<worktree>/<run-id>/     first copy
    <primary>/local_artifacts/fp-verification-archive/<worktree>/<run-id>~2/   a second,
    ...                                                                        different
                                                                               record with
                                                                               the same id

The `<run-id>` / `<run-id>~k` naming applies *within* one worktree's shelf: two
trees may hold the same id without colliding, while a record rewritten in place
in one tree gets the next `~k` beside its earlier self.

`<primary>` is git's first porcelain entry — the main checkout, whose
`local_artifacts/` is already gitignored and local-only by design, so the archive
survives every later `git worktree remove` too.

Every version directory is immutable. Which suffix a record gets is decided by its
content digest: if the record's bytes already sit in `<run-id>` (or `<run-id>~k`),
nothing is touched; otherwise the copy is staged in a temporary directory inside
the archive, every file is re-hashed and compared with its source, and only then is
the whole directory `os.rename`d into the first free name. Nothing outside the
temp dir is ever created twice, overwritten, or deleted (the staged temp dir on
failure is the one exception). `<sha256>  <worktree>/<run-id>[/~k]/<file>` lines
are appended to the archive root's `SHA256SUMS` (paths relative to
`fp-verification-archive/`, so `sha256sum -c` run there verifies every line).
Appending is idempotent, and a manifest that would end up recording two different
hashes for one path is refused — exit 2 — rather than papered over.

Exit contract:

  * **0, silent** when the command does not match, when no linked worktree holds
    records, or when everything is already archived;
  * **0, one stdout line** summarising the record count and the archive location —
    stdout, not a permission decision, because the removal itself is not judged
    here (`guard_shell_command.py` owns destructive-command asking);
  * **2, reason on stderr** when records exist but could not be retained, when
    worktree enumeration fails (fail closed: the hook cannot know what is at
    risk), or when the manifest contradicts the archive — a blocking exit, so the
    tool call is refused *before* records are destroyed. Losing the evidence is
    not recoverable after the fact; failing closed is the cheap direction to fail.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Where scripts/fp.py writes launcher verification records (scripts/README.md).
RECORDS_DIR = Path(".cache") / "fp-verification"
# Where this hook retains them: under the primary checkout's gitignored local root.
ARCHIVE_REL = Path("local_artifacts") / "fp-verification-archive"
SUMS_NAME = "SHA256SUMS"
# The trigger: "worktree" ... "remove", case-insensitive, anywhere in the command.
TRIGGER = re.compile(r"\bworktree\b[\s\S]*\bremove\b", re.IGNORECASE)
# The manifest line format sha256sum writes and reads: "<64 hex>  <path>".
HEX64 = re.compile(r"[0-9a-f]{64}")


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


def triggers(command: str) -> bool:
    """Does the command mention removing a worktree? Textual, by design."""
    return bool(command) and TRIGGER.search(command) is not None


def sha256_file(path: Path) -> str:
    """Streamed SHA-256 of a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def record_digest(record: Path) -> str:
    """Content digest of a record directory: every file's relative path and bytes.

    Two directories with equal digests hold the same files with the same bytes,
    which is exactly the "already archived" test the version-dir naming needs.
    """
    digest = hashlib.sha256()
    for source in sorted(path for path in record.rglob("*") if path.is_file()):
        relative = source.relative_to(record).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(bytes.fromhex(sha256_file(source)))
    return digest.hexdigest()


def worktrees(base: Path) -> list[Path]:
    """Every worktree of `base`'s repository, the primary checkout first.

    `git worktree list --porcelain` always prints the main worktree as the first
    entry, so `trees[0]` is the primary and every later entry a linked worktree.
    A failure to enumerate is fatal (fail closed): the hook must not guess what
    is at risk.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(base), "worktree", "list", "--porcelain"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=30, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ArchiveError(f"cannot enumerate worktrees of {base}: {exc}") from exc
    if result.returncode:
        raise ArchiveError(f"cannot enumerate worktrees of {base}: "
                           f"{(result.stderr or 'git worktree list failed').strip()}")
    found: list[Path] = []
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            found.append(Path(line[len("worktree "):].strip()))
    if not found:
        raise ArchiveError(f"git listed no worktrees for {base}")
    return found


def version_dir(archive: Path, identity: str, digest: str) -> tuple[Path, bool]:
    """(``<identity>`` or the first free ``<identity>~k``, newly created?).

    A directory whose content digest equals `digest` means the record is already
    retained — return it with False so the caller changes nothing. Existing
    directories are only ever read, never rewritten or deleted.
    """
    candidate = archive / identity
    suffix = 1
    while candidate.exists() or candidate.is_symlink():
        if candidate.is_dir() and not candidate.is_symlink() \
                and record_digest(candidate) == digest:
            return candidate, False
        suffix += 1
        candidate = archive / f"{identity}~{suffix}"
    return candidate, True


def retain_record(archive: Path, record: Path) -> tuple[bool, list[str]]:
    """Copy one record directory into the archive immutably.

    `archive` is the record's worktree shelf (`.../<archive-root>/<worktree>/`),
    so the version dirs `<id>`, `<id>~2`, ... live beside their siblings from the
    same tree. Returns (wrote a new version dir?, manifest lines for the archived
    files). Manifest paths are relative to the *archive root* — they are prefixed
    with the shelf's name, which is the worktree's basename — so one `SHA256SUMS`
    at the archive root covers every shelf.
    The copy is staged inside the archive, verified by re-hashing every file, and
    only then `os.rename`d into place — so an interrupted copy can never leave a
    half-written version dir behind, and nothing existing is ever touched.
    """
    identity = record.name
    digest = record_digest(record)
    destination, fresh = version_dir(archive, identity, digest)
    if fresh:
        staged: Path | None = None
        try:
            archive.mkdir(parents=True, exist_ok=True)
            staged = Path(tempfile.mkdtemp(dir=archive, prefix=f".staging-{identity}-"))
            for source in sorted(path for path in record.rglob("*") if path.is_file()):
                target = staged / source.relative_to(record)
                target.parent.mkdir(parents=True, exist_ok=True)
                source_hash = sha256_file(source)
                shutil.copyfile(source, target)
                if sha256_file(target) != source_hash:
                    raise ArchiveError(f"copy of {source} did not verify")
            os.rename(staged, destination)
        except OSError as exc:
            raise ArchiveError(f"cannot retain {record} into {archive}: {exc}") from exc
        finally:
            if staged is not None and (staged.exists() or staged.is_symlink()):
                shutil.rmtree(staged, ignore_errors=True)  # a no-op after the rename
    lines = [f"{sha256_file(source)}  {destination.parent.name}/{destination.name}/"
             f"{source.relative_to(destination).as_posix()}"
             for source in sorted(destination.rglob("*")) if source.is_file()]
    return fresh, lines


def _append_sums(sums: Path, lines: list[str]) -> None:
    """Append the sum lines that are not recorded yet (idempotent).

    A path that already has a different hash — in the manifest on disk or among
    the new lines — is an error: the manifest would be lying about the archive,
    so the removal is blocked instead.
    """
    recorded: dict[str, str] = {}
    if sums.exists():
        for raw in sums.read_text(encoding="utf-8").splitlines():
            digest, separator, name = raw.partition("  ")
            if not separator or not name or not HEX64.fullmatch(digest):
                raise ArchiveError(f"cannot read {sums}: unparsable line {raw!r}")
            if recorded.setdefault(name, digest) != digest:
                raise ArchiveError(f"{sums} records two hashes for {name}")
    fresh: list[str] = []
    for line in dict.fromkeys(lines):
        digest, _, name = line.partition("  ")
        if recorded.get(name) == digest:
            continue
        if name in recorded:
            raise ArchiveError(f"{sums} already records a different hash for {name}")
        recorded[name] = digest
        fresh.append(line)
    if not fresh:
        return
    with sums.open("a", encoding="utf-8", newline="\n") as handle:
        for line in fresh:
            handle.write(line + "\n")


def main() -> int:
    """Read the PreToolUse payload; retain records; exit 0, or 2 when they cannot
    be retained."""
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if not triggers(command_of(data)):
        return 0
    stated = data.get("cwd") if isinstance(data, dict) else None
    try:
        base = Path(stated).resolve() if isinstance(stated, str) and stated else Path.cwd()
    except OSError:
        base = Path.cwd()
    try:
        trees = worktrees(base)
        archive = trees[0] / ARCHIVE_REL  # git's first entry is the primary checkout
        written, holders, lines = 0, 0, []
        for tree in trees[1:]:
            records = tree / RECORDS_DIR
            if not tree.is_dir() or not records.is_dir():
                continue  # a listed worktree that no longer exists holds no records
            identities = sorted(path for path in records.iterdir() if path.is_dir())
            if identities:
                holders += 1
            for record in identities:
                # each worktree keeps its own shelf, so the record says which
                # tree it came from and identical ids in two trees never collide
                fresh, record_lines = retain_record(archive / tree.name, record)
                written += int(fresh)
                lines.extend(record_lines)
        if lines:
            _append_sums(archive / SUMS_NAME, lines)
        if written:
            print(f"guard_worktree_evidence: archived {written} verification "
                  f"record(s) from {holders} linked worktree(s) to {archive}")
    except (ArchiveError, OSError) as exc:
        print(f"guard_worktree_evidence: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
