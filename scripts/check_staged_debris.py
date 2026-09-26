#!/usr/bin/env python3
"""check_staged_debris.py -- reject staged debris, force-added ignored files and oversized blobs.

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
* force-added ignored files (operator ruling 2026-09-26) -- a staged add,
  copy or rename-in whose path .gitignore would ignore
  (``git check-ignore --no-index``), i.e. one that only ``git add -f`` or a
  pre-rule stage could put in the index. A path already tracked in HEAD is
  exempt, so a file tracked despite an ignore rule is not newly flagged (two
  on main at 2026-09-26: lab/pine/mnq_mym_mechanism_diagnostic_v0_1.pine and
  tests/fixtures/c1_image_validation/lifecycle_state.json, both outside the
  allowlisted roots). In HEAD-tree mode every path is in HEAD, so there the
  check is scoped to the allowlisted roots instead (none tracked-but-ignored
  on main at 2026-09-26) -- the backstop for a force-added vendor CSV under
  lab/analysis/**/inputs/;
* oversize staged blobs -- a single file over MAX_STAGED_FILE_BYTES outside
  the allowlisted roots, or over ALLOWLISTED_MAX_STAGED_FILE_BYTES (2 MB)
  inside them. The allowlist is data-derived, not aspirational:
  the largest tracked file is lab/analysis/mym_breakout_entry_2026_09/
  results.json (988,529 B), so the research-results corpus plus its archived
  form is the one legitimate ~>1 MB shape in this repo today. The 2 MB
  ceiling (~2x that blob) blocks a whole multi-year vendor bar panel
  (6.4-11.6 MB) but not a one-year slice (~1.4-2.7 MB) or a file split into
  parts. Anything else large is the blanket-add signature; extend the
  allowlist via review when a shape proves legitimate, never via an env
  override. The allowlist prefix match is case-sensitive: a case variant
  gets the 1 MB cap.

Each finding kind prints its own remedy line; a size or force-add finding is
never told it is in a local-only root.

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
# Prefix match is case-SENSITIVE on purpose: a case variant ("Lab/Analysis/...") is
# not an allowlisted root and falls to the tighter MAX_STAGED_FILE_BYTES cap.
LARGE_FILE_ALLOWLIST_PREFIXES = (
    "lab/analysis/",  # research-results corpus (988 KB results.json precedent)
    "lab/archive/",   # archived form of the same corpus (archive_lab_analysis.py moves)
)
# Ceiling for the allowlisted roots (operator ruling 2026-09-26). ~2x the largest
# legitimate blob (lab/analysis/mym_breakout_entry_2026_09/results.json, 988,529 B).
# It blocks a whole multi-year vendor bar panel (the 6.4-11.6 MB shape). It does NOT
# block a one-year slice (~1.4-2.7 MB; the smaller ones pass) or a file split into
# parts under the ceiling -- the force-added-ignored-file check below and review are
# the controls for those, not this number.
ALLOWLISTED_MAX_STAGED_FILE_BYTES = 2_000_000

MAX_REPORTED_FINDINGS = 20

# Finding kinds; each gets its own remedy line in the rejection footer.
ROOT, IGNORED, SIZE = "root", "ignored", "size"
FORCE_ADDED_IGNORED = (
    "force-added ignored file (.gitignore excludes this path; an ignore rule does not "
    "stop `git add -f`)"
)


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
        if size <= ALLOWLISTED_MAX_STAGED_FILE_BYTES:
            return None
        return (
            f"{size} B exceeds the {ALLOWLISTED_MAX_STAGED_FILE_BYTES} B ceiling for "
            f"allowlisted roots ({', '.join(LARGE_FILE_ALLOWLIST_PREFIXES)}); vendor bar "
            "panels and other bulk data stay out of git"
        )
    return (
        f"{size} B exceeds the {MAX_STAGED_FILE_BYTES} B single-file limit and is "
        f"not under an allowlisted root ({', '.join(LARGE_FILE_ALLOWLIST_PREFIXES)}); "
        "if this file is legitimate, extend LARGE_FILE_ALLOWLIST_PREFIXES via review"
    )


def _git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=root)


def _decode(data: bytes) -> str:
    return data.decode("utf-8", "surrogateescape")


def staged_entries(root: Path) -> list[tuple[str, str]] | None:
    """(status letter, new-side path) of staged adds/copies/modifies/typechanges/
    renames-in.

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
    entries: list[tuple[str, str]] = []
    i = 0
    while i < len(tokens):
        status = tokens[i][:1].decode("ascii", "replace")
        if not status:
            i += 1
            continue
        if status in ("R", "C") and i + 2 < len(tokens):
            entries.append((status, _decode(tokens[i + 2])))  # the destination side
            i += 3
        elif i + 1 < len(tokens):
            entries.append((status, _decode(tokens[i + 1])))
            i += 2
        else:
            i += 1
    return entries


def staged_paths(root: Path) -> list[str] | None:
    """New-side paths of staged_entries(); None on an unborn HEAD."""
    entries = staged_entries(root)
    return None if entries is None else [path for _, path in entries]


def ignored_paths(root: Path, paths: list[str]) -> set[str]:
    """The subset of `paths` that .gitignore rules would ignore, index or not.

    ``--no-index`` is what makes this see force-added files: without it,
    check-ignore never reports a path that is in the index.
    """
    if not paths:
        return set()
    result = subprocess.run(
        ["git", "check-ignore", "--no-index", "--stdin", "-z"],
        cwd=root,
        input=b"\0".join(p.encode("utf-8", "surrogateescape") for p in paths) + b"\0",
        capture_output=True,
        check=False,
    )
    if result.returncode not in (0, 1):  # 1 = none ignored; anything else is a failure
        raise subprocess.CalledProcessError(result.returncode, result.args)
    return {_decode(p) for p in result.stdout.split(b"\0") if p}


def head_paths(root: Path) -> set[str]:
    """Every path tracked in HEAD."""
    out = _git(root, "ls-tree", "-r", "--name-only", "-z", "HEAD")
    return {_decode(p) for p in out.split(b"\0") if p}


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


def _judge(
    path: str, size: int | None, ignored: set[str]
) -> tuple[str, str] | None:
    """(kind, finding line) for one path, or None. One finding per path, in
    remedy order: a banned root, then a force-add, then size."""
    reason = path_finding(path)
    if reason:
        return ROOT, f"{path}: {reason}"
    if path in ignored:
        return IGNORED, f"{path}: {FORCE_ADDED_IGNORED}"
    reason = size_finding(path, size)
    if reason:
        return SIZE, f"{path}: {reason}"
    return None


def collect_findings(root: Path) -> tuple[list[tuple[str, str]], str]:
    """Return ([(kind, finding line)], mode description) for the staged or
    HEAD-tree state."""
    entries = staged_entries(root)
    if entries is None:
        paths = [
            _decode(p) for p in _git(root, "ls-files", "-z").split(b"\0") if p
        ]
        mode = f"index, {len(paths)} path(s) (unborn HEAD)"
        sizes = index_sizes(root, paths)
        ignored = ignored_paths(root, paths)  # first commit: every path is an add
    elif entries or anything_staged(root):
        paths = [path for _, path in entries]
        mode = f"staged vs HEAD, {len(paths)} path(s)"
        if not paths:
            mode += " (deletion-only stage)"
        sizes = index_sizes(root, paths)
        # Force-add check: adds, copies and renames-in only. A path already
        # tracked in HEAD is exempt, so a file tracked despite an ignore rule
        # (two on main at 2026-09-26) is not newly flagged when modified.
        added = [path for status, path in entries if status in ("A", "C", "R")]
        ignored = ignored_paths(root, added)
        if ignored:
            ignored -= head_paths(root)
    else:
        tree = tree_entries(root)
        mode = f"HEAD tree, {len(tree)} path(s) (nothing staged)"
        # Every path is in HEAD here, so a HEAD exemption would disable the
        # check; it is scoped to the allowlisted roots instead, where main held
        # no tracked-but-ignored file at 2026-09-26 (the two that exist lie
        # outside them). This is the CI backstop for a force-added vendor file
        # committed under lab/analysis/ or lab/archive/.
        ignored = ignored_paths(
            root,
            [path for path, _ in tree if path.startswith(LARGE_FILE_ALLOWLIST_PREFIXES)],
        )
        findings = [f for f in (_judge(p, s, ignored) for p, s in tree) if f]
        return findings, mode
    findings = [f for f in (_judge(p, sizes.get(p), ignored) for p in paths) if f]
    return findings, mode


REMEDY = {
    ROOT: (
        "{n} local-only root path(s): these roots are local-only (see .gitignore "
        "and M-41); unstage them (git rm --cached) instead of committing."
    ),
    IGNORED: (
        "{n} force-added ignored file(s): .gitignore excludes these paths; unstage "
        "them (git rm --cached). If a file belongs in git, change .gitignore through "
        "review rather than `git add -f`."
    ),
    SIZE: (
        "{n} oversize blob(s): keep bulk data out of git (local gitignored path or "
        "first-passage-archive, M-41) and unstage it. If a file is legitimate, change "
        "the allowlist or ceiling in scripts/check_staged_debris.py through review."
    ),
}


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
        print(
            "OK: no local-only debris, force-added ignored files or oversize blobs "
            f"({mode})"
        )
        return 0
    shown = findings[:MAX_REPORTED_FINDINGS]
    for _, line in shown:
        print(f"REJECTED: {line}")
    hidden = len(findings) - len(shown)
    if hidden > 0:
        print(f"... and {hidden} more finding(s)")
    for kind in (ROOT, IGNORED, SIZE):  # each kind gets its own, accurate remedy
        count = sum(1 for k, _ in findings if k == kind)
        if count:
            print(REMEDY[kind].format(n=count))
    print(f"ERROR: {len(findings)} finding(s) ({mode}).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
