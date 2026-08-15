#!/usr/bin/env python3
"""session_divergence_hook.py — SessionStart context injection: how stale is this base?

Claude Code SessionStart hook. Prints a short divergence summary so every session
opens knowing whether `origin/main` has moved and, critically, whether it moved on
a GOVERNANCE surface this session is likely to restate.

Why this exists as an unconditional injection rather than a prompt-pattern rule:
`.claude/hookify.build-fetch-first.local.md` fires on build-shaped verbs
("scaffold", "build the pipeline", ...). The 2026-07-24 firing came from a session
whose prompts were "recap", "address", "ratify" — so the rule never fired, and a
§4 discharge was recorded 36 minutes after `origin/main` withdrew it. Predicting
which prompts are build-shaped is the part that failed; this removes the
prediction.

Fails silent and exits 0 on ANY error (offline, no remote, detached HEAD, git
missing). A context-injection hook must never block a session from starting.
"""
from __future__ import annotations

import subprocess
import sys

# DELIBERATE DUPLICATE of scripts/check_push_collision.py's governance class —
# keep the two in sync BY HAND and do not refactor into a shared import. This hook
# runs at SessionStart on every session; coupling it to another module's import
# graph risks bricking session start for a cosmetic dedup of two short tuples.
# ⚠ NOT the same thing as scripts/check_boundaries.py's GOVERNANCE_PREFIXES — that
# is a homonym with a different value and a different purpose. Do not unify them.
# Widened 2026-08-08 (both twins together): frozen pre-registrations live in five
# stores and only docs/briefs/pre-registration/ was guarded.
GOVERNANCE_PREFIXES = (
    "docs/adr/",
    "docs/briefs/pre-registration/",
    "docs/ltm/briefs/pre-registration/",
    "docs/spec/PREREG-",
)
GOVERNANCE_FILES = ("CLAUDE.md", "STATE.md", "docs/SESSIONS.md")
# Campaign-resident frozen prereg bodies (lab/analysis/<theme>/<slug>/PREREG*.md).
# Basename match, not a glob — see the twin for why.
_PREREG_ROOT = "lab/analysis/"
_PREREG_STEM = "PREREG"
MAX_COMMITS_SHOWN = 8


def _git(*args: str, timeout: int = 20) -> str | None:
    try:
        proc = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except Exception:
        return None
    if proc.returncode != 0:
        return None
    return (proc.stdout or "").strip()


def _is_governance(path: str) -> bool:
    if path in GOVERNANCE_FILES or path.startswith(GOVERNANCE_PREFIXES):
        return True
    return (
        path.startswith(_PREREG_ROOT)
        and path.endswith(".md")
        and path.rsplit("/", 1)[-1].startswith(_PREREG_STEM)
    )


def main() -> int:
    # Fetch is best-effort and time-boxed; a slow network must not stall startup.
    _git("fetch", "origin", "main", "--quiet", timeout=25)

    base = _git("merge-base", "HEAD", "origin/main")
    if not base:
        return 0

    log = _git("log", "--oneline", f"{base}..origin/main")
    if log is None:
        return 0
    if not log:
        print("[base check] origin/main: up to date with this branch's merge-base.")
        return 0

    commits = log.splitlines()
    changed = _git("diff", "--name-only", f"{base}..origin/main") or ""
    gov = sorted({p for p in changed.splitlines() if p.strip() and _is_governance(p.strip())})

    print(f"[base check] origin/main is {len(commits)} commit(s) AHEAD of this branch's merge-base.")
    for line in commits[:MAX_COMMITS_SHOWN]:
        print(f"  {line}")
    if len(commits) > MAX_COMMITS_SHOWN:
        print(f"  ... and {len(commits) - MAX_COMMITS_SHOWN} more")

    if gov:
        print("")
        print("  GOVERNANCE surfaces changed upstream — verify current status before")
        print("  restating any decision from these:")
        for path in gov:
            print(f"    - {path}")
        print("")
        print("  A decision you read locally may already be superseded upstream")
        print("  (2026-07-24: a §4 discharge was recorded 36 min after main withdrew it).")
        print("  Read the upstream version before asserting status:")
        print(f"    git diff {base[:12]}..origin/main -- {' '.join(gov[:4])}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)
