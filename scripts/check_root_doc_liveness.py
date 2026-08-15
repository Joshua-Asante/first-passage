#!/usr/bin/env python3
"""check_root_doc_liveness.py — root orientation-doc link gate (governance tier).

The five root orientation docs — README.md, CLAUDE.md, PIPELINES.md, REPO_MAP.md,
STATE.md — are the repo's entry points. They rot in two ways:

  1. **Dead links** — a cited path is retired / moved and the markdown link no
     longer resolves. This is *mechanical* and falsifiable, and this gate catches
     it. (Origin: STATE.md linked `lab/analysis/harv_0.../RESULTS.md` after the
     study body moved to `lab/archive/` — a silent dead link.)
  2. **Stale prose facts** — a version / status / date the doc restates goes
     stale. That is NOT mechanically checkable here (Rule 6 skew audit + Rule 7
     canonical-owner discipline own it); the companion hookify reminder
     (`.claude/hookify.root-doc-skew.local.md`) nudges a human review.

This gate handles class (1) only. It asserts every **repo-relative markdown link**
in the five docs resolves to a path that exists on disk OR is intentionally
gitignored (so a link to a private `.pine` / vendor CSV is not a false positive
on a clone/CI). URLs, mailto:, and pure `#anchor` links are skipped, as are lines
that use the documented historical-retrieval idiom (`git show` / `pre-prune-`),
which deliberately cite evicted blobs.

Sibling of `check_path_liveness.py` (manifest-declared committed paths) and
`check_skill_refs.py` (skill path refs) — same philosophy: a missing committed
target is unambiguously drift, never an environment artifact. Pure stdlib.

Exit codes:
  0 — every markdown link in the five docs resolves (or is gitignored)
  1 — one or more dead links (retired/moved target) — repoint the link
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# The five root orientation docs. Resolution is against REPO_ROOT — correct here
# because all five live AT repo root, so file-relative == root-relative for them.
DEFAULT_DOCS = ("README.md", "CLAUDE.md", "PIPELINES.md", "REPO_MAP.md", "STATE.md")

# [text](target) — non-greedy text, target up to the first ')'
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

# Lines citing an evicted blob on purpose — skip (the target is not meant to be
# on disk). `git show pre-prune-2026-06-05:<path>` is the repo's retrieval idiom.
HISTORICAL_LINE_RE = re.compile(r"git\s+show|pre-prune-", re.IGNORECASE)


def _is_gitignored(target: str, repo_root: Path) -> bool:
    """True if `target` is a gitignored path (legit absence on a clone/CI).

    Tolerant of git being absent (returns False → treat as a real miss)."""
    try:
        result = subprocess.run(
            ["git", "check-ignore", "--quiet", target],
            cwd=repo_root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def check_doc(doc_path: Path, repo_root: Path) -> list[str]:
    """Return dead-link messages for one doc (empty == all links resolve)."""
    if not doc_path.exists():
        return [f"{doc_path.name}: doc itself does not exist"]
    misses: list[str] = []
    text = doc_path.read_text(encoding="utf-8", errors="replace")
    for m in LINK_RE.finditer(text):
        target = m.group(1).strip()
        # Strip a markdown title: [text](path "title") — keep only the path.
        if " " in target:
            target = target.split(" ", 1)[0]
        path_part = target.split("#", 1)[0]  # drop #anchor
        if not path_part:
            continue  # pure in-page anchor
        if path_part.startswith(("http://", "https://", "mailto:", "tel:")):
            continue
        # Skip lines that deliberately cite an evicted blob.
        line_start = text.rfind("\n", 0, m.start()) + 1
        line_end = text.find("\n", m.end())
        line = text[line_start : line_end if line_end != -1 else len(text)]
        if HISTORICAL_LINE_RE.search(line):
            continue
        if (repo_root / path_part).exists():
            continue
        if _is_gitignored(path_part, repo_root):
            continue
        lineno = text.count("\n", 0, m.start()) + 1
        misses.append(f"{doc_path.name}:{lineno}: dead link -> {target}")
    return misses


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--docs", nargs="*", default=list(DEFAULT_DOCS),
        help="doc filenames to check (default: the five root orientation docs)",
    )
    parser.add_argument(
        "--repo-root", type=Path, default=REPO_ROOT,
        help="root path the markdown links are resolved against",
    )
    args = parser.parse_args()

    misses: list[str] = []
    for name in args.docs:
        misses += check_doc(args.repo_root / name, args.repo_root)

    for msg in misses:
        print(f"HARD: {msg}")
    if misses:
        print(
            f"\ncheck_root_doc_liveness: {len(misses)} dead link(s) in the root "
            "orientation docs. A markdown link to a missing committed path is "
            "drift, not an environment artifact — repoint the link to where the "
            "target moved (e.g. lab/analysis/<slug>/ -> lab/archive/<slug>/), do "
            "not relax the gate."
        )
        return 1
    print("check_root_doc_liveness: OK — all root-doc markdown links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
