#!/usr/bin/env python3
"""check_staged_debris.py -- reject staged local-only debris and oversized blobs.

Gate id ``staged-debris`` (tier ``always``, scripts/gates.yml). A 2026-09-24
blanket ``git add`` in the main checkout staged ~1,115 files / ~94 MB of
local-only roots: ``recovery/`` evidence packets (untracked by definition --
scripts/check_boundaries.py exempts exactly this root as the local-only
evidence-packet store), ``tmp/`` session scratch, and root ``tmp-*`` /
editor debris. The root-anchored .gitignore rules added the same day hide
these roots from status, but an ignore rule cannot reject an explicit
``git add -f`` or a stage made before the rule existed; this gate is that
rejection (M-41: a local-only root is ignored, never blanket-added -- and an
ignored root is still not an archive).

Same rules in every mode:

* banned staged paths -- ``recovery/...``, ``tmp/...``, and any root-level
  ``tmp-*`` path. Root-anchored like the .gitignore rules (do not widen to
  nested paths; the incident class is root debris, and nested ``tmp``-named
  dirs under tracked trees are not this gate's business), but not a
  one-for-one mirror: ``recovery/`` and ``tmp/`` match their ignore rules,
  the ``tmp-*`` ban covers the whole root ``tmp-*`` namespace (a superset of
  the ignored ``/tmp-*/``, ``/tmp-*.md``, ``/tmp-*.py`` shapes), and
  ``.zcodeignore`` is ignored but not banned. Root names compare
  case-insensitively: on a case-insensitive checkout (Windows,
  core.ignorecase=true) ``Recovery/`` or ``TMP/`` is the same on-disk root;
* oversize staged blobs -- a single file over MAX_STAGED_FILE_BYTES outside
  the allowlisted roots. The allowlist is data-derived, not aspirational:
  the largest tracked file is lab/analysis/mym_breakout_entry_2026_09/
  results.json (988,529 B), so the research-results corpus plus its archived
  form is the one legitimate ~>1 MB shape in this repo today. Anything else
  large is the blanket-add signature; extend the allowlist via review when a
  shape proves legitimate, never via an env override.

Modes, in order: staged changes -> inspect the index diff vs HEAD (the
pre-commit contract; deletes and rename-away sources are never findings, a
cleanup must not be blocked -- a deletion-only stage is still a staged
change, never mistaken for "nothing staged"). Nothing staged -> inspect the
HEAD tree, so CI (``--tier check``) and ``make check`` also reject a branch
that already committed debris. Unborn HEAD -> inspect the whole index (first
commit).

Known scope limit of the staged mode: it judges only the staged delta, so
debris already in HEAD (e.g. committed with ``--no-verify``) is not
re-reported by a later unrelated commit. The backstop is the nothing-staged
HEAD-tree mode that CI's clean checkout runs.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Root-anchored like the .gitignore rules; compared lower-cased (see docstring).
BANNED_ROOT_DIRS = ("recovery", "tmp")
BANNED_ROOT_STEM_PREFIX = "tmp-"

MAX_STAGED_FILE_BYTES = 1_000_000  # "~1 MB"; largest tracked file today: 988,529 B
LARGE_FILE_ALLOWLIST_PREFIXES = (
    "lab/analysis/",  # research-results corpus (988 KB results.json precedent)
    "lab/archive/",   # archived form of the same corpus (archive_lab_analysis.py moves)
)

MAX_REPORTED_FINDINGS = 20


def path_finding(path: str) -> str | None:
    """Ban reason for a repo-rooted staged path, or None if allowed."""
    stem = path.split("/", 1)[0]
    folded = stem.lower()  # case-insensitive checkouts share one on-disk root
    if folded in BANNED_ROOT_DIRS:
        return f"local-only root '{stem}/' (untracked by definition; .gitignore)"
    if folded.startswith(BANNED_ROOT_STEM_PREFIX):
        return "root-level 'tmp-*' debris path (.gitignore)"
    return None


def size_finding(path: str, size: int | None) -> str | None:
    """Oversize reason for one staged blob, or None if allowed."""
    if size is None or size <= MAX_STAGED_FILE_BYTES:
        return None
    if path.startswith(LARGE_FILE_ALLOWLIST_PREFIXES):
        return None
    return (
        f"{size} B exceeds the {MAX_STAGED_FILE_BYTES} B single-file limit and is "
        f"not under an allowlisted root ({', '.join(LARGE_FILE_ALLOWLIST_PREFIXES)}); "
        "if this file is legitimate, extend LARGE_FILE_ALLOWLIST_PREFIXES via review"
    )


def _git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=root)


def _decode(data: bytes) -> str:
    return data.decode("utf-8", "surrogateescape")


def staged_paths(root: Path) -> list[str] | None:
    """New-side paths of staged adds/copies/modifies/typechanges/renames-in.

    None means git could not diff against HEAD (unborn branch); the caller
    falls back to the whole index. Rename-away sources and deletes are not
    returned -- removing debris must never be blocked.
    """
    try:
        out = _git(
            root, "diff", "--cached", "--name-status", "-z", "--diff-filter=ACMRT"
        )
    except subprocess.CalledProcessError:
        return None
    tokens = out.split(b"\0")
    paths: list[str] = []
    i = 0
    while i < len(tokens):
        status = tokens[i][:1].decode("ascii", "replace")
        if not status:
            i += 1
            continue
        if status in ("R", "C") and i + 2 < len(tokens):
            paths.append(_decode(tokens[i + 2]))  # judge the destination side
            i += 3
        elif i + 1 < len(tokens):
            paths.append(_decode(tokens[i + 1]))
            i += 2
        else:
            i += 1
    return paths


def anything_staged(root: Path) -> bool:
    """True when the index differs from HEAD at all -- deletions included.

    staged_paths() drops deletes by design, so its empty result cannot tell a
    clean index from a deletion-only cleanup stage.
    """
    result = subprocess.run(  # rc 1 is an answer here, not a failure
        ["git", "diff", "--cached", "--quiet", "--no-ext-diff"], cwd=root, check=False
    )
    if result.returncode not in (0, 1):
        raise subprocess.CalledProcessError(result.returncode, result.args)
    return result.returncode == 1


def index_sizes(root: Path, paths: list[str]) -> dict[str, int]:
    """Staged blob size in bytes for each path present at index stage 0."""
    if not paths:
        return {}
    wanted = set(paths)
    sha_by_path: dict[str, str] = {}
    for record in _git(root, "ls-files", "-s", "-z").split(b"\0"):
        if not record:
            continue
        meta, _, name = record.partition(b"\t")
        parts = meta.split()
        if len(parts) != 3 or parts[2] != b"0" or parts[0] == b"160000":
            continue  # conflicted entry or submodule gitlink: no single blob size
        decoded = _decode(name)
        if decoded in wanted:
            sha_by_path[decoded] = parts[1].decode("ascii")
    if not sha_by_path:
        return {}
    batch = subprocess.run(
        ["git", "cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)"],
        cwd=root,
        input=b"\n".join(s.encode("ascii") for s in sha_by_path.values()),
        capture_output=True,
        check=True,
    ).stdout
    size_by_sha = {
        parts[0].decode("ascii"): int(parts[2])
        for parts in (line.split() for line in batch.splitlines())
        if len(parts) == 3 and parts[1] == b"blob"
    }
    return {p: size_by_sha[s] for p, s in sha_by_path.items() if s in size_by_sha}


def tree_entries(root: Path) -> list[tuple[str, int | None]]:
    """(path, blob size) for every blob in the HEAD tree; None size = non-blob."""
    entries: list[tuple[str, int | None]] = []
    for record in _git(root, "ls-tree", "-r", "-l", "-z", "HEAD").split(b"\0"):
        if not record:
            continue
        meta, _, name = record.partition(b"\t")
        parts = meta.split()
        if len(parts) != 4:
            continue
        size = int(parts[3]) if parts[3].isdigit() else None
        entries.append((_decode(name), size))
    return entries


def collect_findings(root: Path) -> tuple[list[str], str]:
    """Return (findings, mode description) for the staged or HEAD-tree state."""
    findings: list[str] = []
    paths = staged_paths(root)
    if paths is None:
        paths = [
            _decode(p) for p in _git(root, "ls-files", "-z").split(b"\0") if p
        ]
        mode = f"index, {len(paths)} path(s) (unborn HEAD)"
        sizes = index_sizes(root, paths)
    elif paths or anything_staged(root):
        mode = f"staged vs HEAD, {len(paths)} path(s)"
        if not paths:
            mode += " (deletion-only stage)"
        sizes = index_sizes(root, paths)
    else:
        entries = tree_entries(root)
        mode = f"HEAD tree, {len(entries)} path(s) (nothing staged)"
        for path, size in entries:
            reason = path_finding(path) or size_finding(path, size)
            if reason:
                findings.append(f"{path}: {reason}")
        return findings, mode
    for path in paths:
        reason = path_finding(path) or size_finding(path, sizes.get(path))
        if reason:
            findings.append(f"{path}: {reason}")
    return findings, mode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="repository root to inspect (default: this checkout)",
    )
    args = parser.parse_args(argv)
    try:
        findings, mode = collect_findings(args.root)
    except FileNotFoundError:
        print("SKIP: git is unavailable; cannot inspect staged state")
        return 0
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git failed ({' '.join(exc.cmd)}; rc={exc.returncode})")
        return 1
    if not findings:
        print(f"OK: no local-only debris or oversize blobs ({mode})")
        return 0
    shown = findings[:MAX_REPORTED_FINDINGS]
    for line in shown:
        print(f"REJECTED: {line}")
    hidden = len(findings) - len(shown)
    if hidden > 0:
        print(f"... and {hidden} more finding(s)")
    print(
        f"ERROR: {len(findings)} staged-path finding(s) ({mode}). These roots are "
        "local-only (see .gitignore and M-41); unstage them instead of committing."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
