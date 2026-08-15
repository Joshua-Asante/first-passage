#!/usr/bin/env python
"""Make the locked Pine source available inside a git worktree.

WHY THIS EXISTS
---------------
`**/*.pine` is gitignored (the live edge is held privately — see CLAUDE.md
"Public-clone posture"). Gitignored / untracked files are NOT shared between git
worktrees: each worktree has its own working directory, and the locked `.pine`
files exist only in the **primary** checkout where Joshua keeps them. So any
worktree created via `git worktree add` starts with `core/strategies/*/*.pine`
ABSENT — which silently blocks every Pine-dependent task:

  * codification / scaffold extraction (reads the locked Pine as templates),
  * any decision-brief §0 (Rule 0) that must read `*.pine`,
  * local Pine reads for lock / venue-edition work.

This is the operational counterpart to the brief-authoring §0 citation-chain
sub-rule (Q-GUARDIAN-TRAIL-1): that rule says *how to cite Pine when you cannot
read it*; this script *makes it readable* when a local primary checkout has it.

WHAT IT DOES
------------
Copies the locked `core/strategies/*/*.pine` from the primary worktree into the
current worktree's matching paths. Copied files remain gitignored, so they can
never be committed from the worktree — they are read-only fuel for §0 reads and
scaffold extraction. Optionally verifies the synced bytes against
`core/strategies/MANIFEST.sha256`.

USAGE
-----
    # Pre-flight gate (exit 0 if Pine present in CURRENT tree, 1 if absent):
    python scripts/sync_pine_to_worktree.py --check

    # Sync from the auto-detected primary worktree into the current worktree:
    python scripts/sync_pine_to_worktree.py

    # Dry-run / explicit source / verify against manifest:
    python scripts/sync_pine_to_worktree.py --dry-run
    python scripts/sync_pine_to_worktree.py --source "C:/Users/joshu/multi_firm_operations"
    python scripts/sync_pine_to_worktree.py --verify

Exit codes: 0 success / pine present; 1 pine absent (--check) or sync failed;
2 usage / no source found.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

LOCKED_GLOB = "core/strategies/*/*.pine"   # the locked strategy Pine (--check gate target)
MANIFEST = "core/strategies/MANIFEST.sha256"
_EXCLUDE_PARTS = {".git"}             # never recurse into git internals / nested worktrees


def _run(args: list[str], cwd: Path | None = None) -> str:
    return subprocess.run(
        args, cwd=cwd, capture_output=True, text=True, check=True
    ).stdout


def current_toplevel() -> Path:
    return Path(_run(["git", "rev-parse", "--show-toplevel"]).strip())


def primary_worktree(exclude: Path) -> Path | None:
    """The main (non-`.claude/worktrees/...`) working tree from `git worktree list`.

    `git worktree list --porcelain` lists the main worktree first, then linked
    worktrees. We pick the first worktree whose path is not under a
    `worktrees` directory and is not the current tree.
    """
    out = _run(["git", "worktree", "list", "--porcelain"])
    paths: list[Path] = []
    for line in out.splitlines():
        if line.startswith("worktree "):
            paths.append(Path(line[len("worktree "):].strip()))
    exclude = exclude.resolve()
    for p in paths:
        rp = p.resolve()
        if rp == exclude:
            continue
        if "worktrees" in rp.parts:
            continue
        return rp
    # Fall back to the first listed worktree that isn't the current one.
    for p in paths:
        if p.resolve() != exclude:
            return p.resolve()
    return None


def pine_files(root: Path) -> list[Path]:
    """All *.pine under root, EXCLUDING git internals and nested worktrees.

    The primary checkout contains `.claude/worktrees/<name>/` (linked worktrees);
    recursing into those would double-count and copy into wrong relative paths.
    """
    out = []
    for p in root.rglob("*.pine"):
        rel_parts = set(p.relative_to(root).parts)
        if rel_parts & _EXCLUDE_PARTS:
            continue
        if "worktrees" in p.relative_to(root).parts:
            continue
        out.append(p)
    return sorted(out)


def locked_pine_files(root: Path) -> list[Path]:
    """Just the locked strategy Pine (strategies/<strat>/*.pine) — the --check target."""
    return sorted(root.glob(LOCKED_GLOB))


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_against_manifest(root: Path) -> tuple[int, list[str], list[str]]:
    """Compare present .pine bytes to MANIFEST.sha256.

    Returns (n_checked, mismatches, skipped). A manifest entry whose file is
    absent on disk is **skipped** (informational), NOT a failure — the manifest
    may pin archive .pine that aren't kept on disk locally (a pre-existing
    manifest/disk skew, separate from this sync's job). Only HASH MISMATCHES of
    present files are failures.
    """
    man = root / MANIFEST
    if not man.exists():
        return 0, [], [f"(no manifest at {MANIFEST}; verify skipped)"]
    expected: dict[str, str] = {}
    for line in man.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 2:
            digest, name = parts[0], parts[-1].lstrip("*")
            expected[name] = digest
    mismatches: list[str] = []
    skipped: list[str] = []
    checked = 0
    for rel, digest in expected.items():
        if not rel.endswith(".pine"):
            continue
        f = root / rel
        if not f.exists():
            skipped.append(rel)
            continue
        checked += 1
        actual = _sha256(f)
        if actual != digest:
            mismatches.append(f"HASH MISMATCH: {rel} (manifest {digest[:12]} != disk {actual[:12]})")
    return checked, mismatches, skipped


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="pre-flight only: exit 0 if Pine present in current tree, 1 if absent")
    ap.add_argument("--source", default=None,
                    help="source checkout to copy Pine FROM (default: auto-detect primary worktree)")
    ap.add_argument("--dry-run", action="store_true", help="print what would copy, change nothing")
    ap.add_argument("--verify", action="store_true",
                    help="after sync, verify bytes against strategies/MANIFEST.sha256")
    args = ap.parse_args(argv)

    try:
        dest = current_toplevel()
    except subprocess.CalledProcessError:
        print("ERROR: not inside a git repository.", file=sys.stderr)
        return 2

    present = locked_pine_files(dest)   # --check gates on the locked strategy Pine

    if args.check:
        if present:
            print(f"OK: {len(present)} .pine present in {dest}")
            return 0
        print(f"ABSENT: no {LOCKED_GLOB} in {dest} — this is a worktree without Pine. "
              f"Run `python scripts/sync_pine_to_worktree.py` to populate it.",
              file=sys.stderr)
        return 1

    # Resolve source.
    src = Path(args.source).resolve() if args.source else primary_worktree(exclude=dest)
    if src is None:
        print("ERROR: could not auto-detect a primary worktree; pass --source.", file=sys.stderr)
        return 2
    if src.resolve() == dest.resolve():
        print(f"Source == current tree ({dest}); Pine is already local here "
              f"({len(present)} files). Nothing to sync.")
        return 0 if present else 1

    src_pine = pine_files(src)
    if not src_pine:
        print(f"ERROR: source {src} has no {LOCKED_GLOB} — wrong source, or the "
              f"locked Pine is not present there either.", file=sys.stderr)
        return 2

    copied = 0
    for sf in src_pine:
        rel = sf.relative_to(src)
        df = dest / rel
        action = "copy"
        if df.exists() and _sha256(df) == _sha256(sf):
            action = "skip (identical)"
        if args.dry_run:
            print(f"[dry-run] {action}: {rel}")
            continue
        if action.startswith("copy"):
            df.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(sf, df)
            copied += 1
            print(f"copied: {rel}")
        else:
            print(f"skip (identical): {rel}")

    if args.dry_run:
        print(f"[dry-run] {len(src_pine)} source .pine from {src}")
        return 0

    print(f"\nSynced {copied} file(s) ({len(src_pine)} source .pine) from {src} -> {dest}")
    print("These files are gitignored (**/*.pine) and cannot be committed from this worktree.")

    if args.verify:
        checked, mismatches, skipped = verify_against_manifest(dest)
        if skipped:
            print(f"\nMANIFEST VERIFY: {len(skipped)} manifest .pine not present in source "
                  f"(skipped — pre-existing manifest/disk skew, not synced):")
            for s in skipped:
                print(f"  - {s}")
        if mismatches:
            print("\nMANIFEST VERIFY: FAIL")
            for m in mismatches:
                print(f"  {m}")
            return 1
        print(f"\nMANIFEST VERIFY: OK ({checked} present .pine match strategies/MANIFEST.sha256)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
