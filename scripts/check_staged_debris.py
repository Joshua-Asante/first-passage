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
* force-added ignored files (operator ruling 2026-09-26) -- a judged path
  that the repository's own .gitignore rules ignore, i.e. one that only
  ``git add -f`` or a pre-rule stage could put in the index. The rules are
  read from the bytes being committed, never the working tree: the INDEX
  versions of every .gitignore in staged/unborn mode, the HEAD versions in
  HEAD-tree mode. They are materialised into a throwaway mirror repository
  and matched there with ``git check-ignore --no-index``, so an unstaged
  .gitignore edit cannot hide a force-add, and personal rules
  (``.git/info/exclude``, a local or global ``core.excludesFile``) never
  count -- the mirror has no info/exclude, ``core.excludesFile`` points at an
  empty file, and ``core.ignorecase=false`` pins case-sensitive matching, so
  the verdict is the same in every clone. Every judged path is checked --
  staged adds, copies, renames-in and modifies; every index path when the
  stage changes any .gitignore; every HEAD path in HEAD-tree mode. The only
  exemption is TRACKED_IGNORED_GRANDFATHERED, the files tracked on main
  despite a matching rule before this check existed;
* oversize staged blobs -- a single file over MAX_STAGED_FILE_BYTES outside
  the allowlisted roots, or over ALLOWLISTED_MAX_STAGED_FILE_BYTES (2 MB)
  inside them. The allowlist is data-derived, not aspirational:
  the largest tracked file is lab/analysis/mym_breakout_entry_2026_09/
  results.json (988,529 B), so the research-results corpus plus its archived
  form is the one legitimate ~>1 MB shape in this repo today. Files over the
  2 MB ceiling (~2x that blob) are rejected, which blocks multi-year vendor
  bar panels (6.4-11.6 MB) and the larger one-year slices (~1.4-2.7 MB);
  smaller one-year slices and files split into parts under the ceiling pass.
  Anything else large is the blanket-add signature; extend the
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
import os
import subprocess
import sys
import tempfile
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
# Files over it are rejected: that blocks multi-year vendor bar panels (6.4-11.6 MB)
# and the larger one-year slices (~1.4-2.7 MB). Smaller one-year slices and files
# split into parts under the ceiling pass -- the force-added-ignored-file check below
# and review are the controls for those, not this number.
ALLOWLISTED_MAX_STAGED_FILE_BYTES = 2_000_000

# Files tracked on main despite a matching repository .gitignore rule before the
# force-added-ignored-file check existed (verified on main 2026-09-26 against the
# committed rules). Exact-path exemption, in every mode; any other tracked ignored
# path is a finding. Shrink via review when one is untracked or its rule is
# narrowed; never grow it to admit a new force-add.
TRACKED_IGNORED_GRANDFATHERED = frozenset(
    {
        "lab/pine/mnq_mym_mechanism_diagnostic_v0_1.pine",
        "tests/fixtures/c1_image_validation/lifecycle_state.json",
    }
)

# Variables that bind a git process to one repository (`git rev-parse
# --local-env-vars`). Stripped for the rule mirror so a pre-commit hook's GIT_DIR /
# GIT_INDEX_FILE / GIT_CONFIG_PARAMETERS never reach it.
_GIT_LOCAL_ENV_VARS = (
    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_CONFIG", "GIT_CONFIG_PARAMETERS",
    "GIT_CONFIG_COUNT", "GIT_OBJECT_DIRECTORY", "GIT_DIR", "GIT_WORK_TREE",
    "GIT_IMPLICIT_WORK_TREE", "GIT_GRAFT_FILE", "GIT_INDEX_FILE",
    "GIT_NO_REPLACE_OBJECTS", "GIT_REPLACE_REF_BASE", "GIT_PREFIX",
    "GIT_SHALLOW_FILE", "GIT_COMMON_DIR",
)
_REGULAR_FILE_MODES = (b"100644", b"100755")

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


def _is_gitignore(path: str) -> bool:
    return path == ".gitignore" or path.endswith("/.gitignore")


def _index_stage0(root: Path) -> dict[str, tuple[bytes, str]]:
    """path -> (mode, blob sha) for every stage-0 index entry.

    Conflicted entries (stages 1-3) have no single blob and cannot be committed
    anyway, so they are left out.
    """
    records: dict[str, tuple[bytes, str]] = {}
    for record in _git(root, "ls-files", "-s", "-z").split(b"\0"):
        if not record:
            continue
        meta, _, name = record.partition(b"\t")
        parts = meta.split()
        if len(parts) != 3 or parts[2] != b"0":
            continue
        records[_decode(name)] = (parts[0], parts[1].decode("ascii"))
    return records


def _rule_blobs(records: dict[str, tuple[bytes, str]]) -> dict[str, str]:
    """.gitignore path -> blob sha, regular files only (git never follows a
    symlinked .gitignore)."""
    return {
        path: sha
        for path, (mode, sha) in records.items()
        if _is_gitignore(path) and mode in _REGULAR_FILE_MODES
    }


def _read_blobs(root: Path, shas: set[str]) -> dict[str, bytes]:
    """sha -> content via one `git cat-file --batch`; fails closed on a
    missing or non-blob object."""
    ordered = sorted(shas)
    if not ordered:
        return {}
    cmd = ["git", "cat-file", "--batch"]
    out = subprocess.run(
        cmd,
        cwd=root,
        input="".join(sha + "\n" for sha in ordered).encode("ascii"),
        capture_output=True,
        check=True,
    ).stdout
    blobs: dict[str, bytes] = {}
    pos = 0
    for sha in ordered:
        eol = out.find(b"\n", pos)
        header = out[pos:eol].split() if eol >= 0 else []
        if len(header) != 3 or header[1] != b"blob" or header[0].decode() != sha:
            raise subprocess.CalledProcessError(1, cmd)
        start = eol + 1
        end = start + int(header[2])
        blobs[sha] = out[start:end]
        pos = end + 1  # content is followed by a newline
    return blobs


def ignored_paths(root: Path, rules: dict[str, str], paths: list[str]) -> set[str]:
    """The subset of `paths` that the given .gitignore blobs ignore.

    `rules` maps each .gitignore path to the blob sha being judged (index or
    HEAD), so the verdict comes from the committed bytes, never the working
    tree. The blobs are written into a throwaway mirror repository and matched
    there: it is initialised from an empty template (no info/exclude), runs
    with core.excludesFile pointing at an empty file (no global/XDG excludes)
    and core.ignorecase=false, so only repository-owned rules count.
    ``--no-index`` keeps check-ignore from exempting indexed paths.
    """
    if not paths or not rules:
        return set()
    contents = _read_blobs(root, set(rules.values()))
    env = {k: v for k, v in os.environ.items() if k not in _GIT_LOCAL_ENV_VARS}
    with tempfile.TemporaryDirectory(prefix="staged-debris-rules-") as tmp:
        base = Path(tmp)
        template = base / "template"
        template.mkdir()
        empty_excludes = base / "no-excludes"
        empty_excludes.write_bytes(b"")
        mirror = base / "mirror"
        subprocess.run(
            ["git", "init", "-q", f"--template={template}", str(mirror)],
            env=env,
            capture_output=True,
            check=True,
        )
        for rel, sha in rules.items():
            target = mirror.joinpath(*rel.split("/"))
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(contents[sha])
        result = subprocess.run(
            [
                "git",
                "-c", f"core.excludesFile={empty_excludes.as_posix()}",
                "-c", "core.ignorecase=false",
                "check-ignore", "--no-index", "--stdin", "-z",
            ],
            cwd=mirror,
            env=env,
            input=b"\0".join(p.encode("utf-8", "surrogateescape") for p in paths) + b"\0",
            capture_output=True,
            check=False,
        )
    if result.returncode not in (0, 1):  # 1 = none ignored; anything else is a failure
        raise subprocess.CalledProcessError(result.returncode, result.args)
    return {_decode(p) for p in result.stdout.split(b"\0") if p}


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


def index_sizes(
    root: Path, paths: list[str], records: dict[str, tuple[bytes, str]] | None = None
) -> dict[str, int]:
    """Staged blob size in bytes for each path present at index stage 0."""
    if not paths:
        return {}
    if records is None:
        records = _index_stage0(root)
    sha_by_path = {
        p: records[p][1]
        for p in paths
        if p in records and records[p][0] != b"160000"  # gitlink: no blob size
    }
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


def _head_tree_records(root: Path) -> list[tuple[bytes, bytes, str, int | None, str]]:
    """(mode, type, sha, blob size or None, path) for every HEAD tree entry."""
    records: list[tuple[bytes, bytes, str, int | None, str]] = []
    for record in _git(root, "ls-tree", "-r", "-l", "-z", "HEAD").split(b"\0"):
        if not record:
            continue
        meta, _, name = record.partition(b"\t")
        parts = meta.split()
        if len(parts) != 4:
            continue
        size = int(parts[3]) if parts[3].isdigit() else None
        records.append(
            (parts[0], parts[1], parts[2].decode("ascii"), size, _decode(name))
        )
    return records


def tree_entries(root: Path) -> list[tuple[str, int | None]]:
    """(path, blob size) for every blob in the HEAD tree; None size = non-blob."""
    return [(path, size) for _, _, _, size, path in _head_tree_records(root)]


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
        records = _index_stage0(root)
        paths = sorted(records)
        mode = f"index, {len(paths)} path(s) (unborn HEAD)"
        sizes = index_sizes(root, paths, records)
        # First commit: every path is an add, judged by the index's own rules.
        ignored = ignored_paths(root, _rule_blobs(records), paths)
        extra: list[str] = []
    elif entries or anything_staged(root):
        paths = [path for _, path in entries]
        mode = f"staged vs HEAD, {len(paths)} path(s)"
        if not paths:
            mode += " (deletion-only stage)"
        records = _index_stage0(root)
        sizes = index_sizes(root, paths, records)
        index_rules = _rule_blobs(records)
        head_rules = {
            path: sha
            for mode_, type_, sha, _, path in _head_tree_records(root)
            if type_ == b"blob" and _is_gitignore(path) and mode_ in _REGULAR_FILE_MODES
        }
        # A staged .gitignore change (add, edit, delete, rename) can newly ignore
        # a file that is tracked but untouched by this stage, so then every
        # index path is judged against the staged rules; otherwise the staged
        # paths (adds, copies, renames-in and modifies) are.
        scope = sorted(records) if index_rules != head_rules else paths
        ignored = ignored_paths(root, index_rules, scope)
        extra = sorted(ignored.difference(paths))
    else:
        tree = _head_tree_records(root)
        mode = f"HEAD tree, {len(tree)} path(s) (nothing staged)"
        head_rules = {
            path: sha
            for mode_, type_, sha, _, path in tree
            if type_ == b"blob" and _is_gitignore(path) and mode_ in _REGULAR_FILE_MODES
        }
        # Every HEAD path, judged by the HEAD rules: the CI backstop for a
        # force-added .env, vendor CSV or other ignored file anywhere in the tree.
        paths = [path for _, _, _, _, path in tree]
        sizes = {path: size for _, _, _, size, path in tree}
        ignored = ignored_paths(root, head_rules, paths)
        extra = []
    ignored -= TRACKED_IGNORED_GRANDFATHERED
    extra = [path for path in extra if path in ignored]
    findings = [f for f in (_judge(p, sizes.get(p), ignored) for p in paths) if f]
    findings += [(IGNORED, f"{p}: {FORCE_ADDED_IGNORED}") for p in extra]
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
