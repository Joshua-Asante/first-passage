#!/usr/bin/env python3
"""check_push_collision.py — governance-surface push collision gate (governance tier).

This repo is worked from several concurrent sessions/worktrees (CC, Cursor,
operator). The recurring failure is not "main moved" — main moves constantly and
that is fine — it is **both sides editing the same governance surface from a
stale base**, which merges cleanly and lands a contradiction.

Measured firings of that class (all three logged in
`feedback_check_origin_main_before_multistep_build`):
  2026-07-11  PR #325's planned PR-2 fully mooted by a parallel FXIFY retirement.
  2026-07-14  Q-SFRISK-1 Phase-0 re-derived in parallel; ratified fork abandoned.
  2026-07-24  A §4 discharge was recorded 36 min after `origin/main` WITHDREW it.
              Only docs/adr/INDEX.md conflicted textually; CLAUDE.md and STATE.md
              **auto-merged cleanly into a direct self-contradiction** (WITHDRAWN
              on one line, DISCHARGED on another). The git conflict count was not
              a safety signal.

So the gate is deliberately NOT "did main move" (too noisy to be respected) and
NOT "will git report a conflict" (the 07-24 case proves that misses the danger).
It is the precise collision condition:

    a GOVERNANCE-class path changed on BOTH sides since the merge-base.

Governance class = the surfaces that carry decision status and are restated in
several places, so a stale edit reads as authoritative:
    CLAUDE.md, STATE.md, docs/SESSIONS.md, docs/adr/**,
    docs/briefs/pre-registration/**,
    docs/ltm/briefs/pre-registration/**,   (widened 2026-08-08)
    docs/spec/PREREG-*,                    (widened 2026-08-08)
    lab/analysis/**/PREREG*.md             (widened 2026-08-08)

The 2026-08-08 widening applied the class test above to the whole frozen-prereg
estate, which turned out to live in FIVE stores while only the second line was
guarded — so 0 of 18 campaign-resident bodies were covered. A frozen prereg is
the strongest form of "carries decision status": it is amendable only by
close+reopen, and W4 (2026-08-07) made the live minimal gate set a function of
these bodies. Measured before widening: 5 of 18 campaign bodies carry more than
one commit (they are amended through their own append-only logs), so this is
low-traffic — and a *concurrent* amendment to a frozen decision record from two
branches is the case worth blocking, not a false positive.

``docs/SESSIONS.md`` is in the class because a stale *rewrite* of an existing
entry is the 07-24 shape. Two branches each *adding* a new top heading is the
designed ``merge=union`` merge, not a contradiction — that delta is exempted
when ours is append-only vs the merge-base (see ``roll_sessions.append_only_problems``).
Mutating a heading that already existed on the merge-base still collides.

Fail-open on network: if `git fetch` cannot reach the remote, this reports and
exits 0. You cannot gate on data you cannot fetch, and blocking pushes offline is
hostile. Fail-CLOSED on an actual collision.

Escape hatch (intentional, logged to stderr):
    FIRST_PASSAGE_ALLOW_PUSH_COLLISION=1 git push

Exit codes: 0 = no collision (or offline/no upstream); 1 = collision detected.
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

GOVERNANCE_PREFIXES = (
    "docs/adr/",
    "docs/briefs/pre-registration/",
    # Widened 2026-08-08. The class test is the docstring's own: "carries decision
    # status and is restated in several places". Frozen pre-registrations are the
    # strongest form of that — amendable only by close+reopen — and W4 made the live
    # minimal gate set a function of them, yet the estate lives in FIVE stores and
    # only the one above was guarded.
    "docs/ltm/briefs/pre-registration/",  # rolled preregs; the LTM path does not
                                          # match the hot prefix, so 30 bodies sat outside
    "docs/spec/PREREG-",                  # 3 bodies; PREREG- is a real filename prefix
)
# Frozen prereg bodies that live beside their campaign rather than under a prereg
# directory — not expressible as a path prefix (`lab/analysis/` alone would sweep in
# every RESULTS/script/data file and generate real false positives). Matched by
# basename instead; deliberately NOT `PurePath.full_match` (Python 3.13+, and this
# repo's floor is 3.11) and NOT `fnmatch` (its `*` crosses `/`, so the glob would be
# looser than it reads).
_PREREG_ROOT = "lab/analysis/"
_PREREG_STEM = "PREREG"
GOVERNANCE_FILES = (
    "CLAUDE.md",
    "STATE.md",
    "docs/SESSIONS.md",
)
ESCAPE_ENV = "FIRST_PASSAGE_ALLOW_PUSH_COLLISION"
_SESSIONS = "docs/SESSIONS.md"


def _load_roll_sessions():
    """Load roll_sessions by path — scripts/ is not a package."""
    path = Path(__file__).resolve().parent / "roll_sessions.py"
    spec = importlib.util.spec_from_file_location("_roll_sessions_for_collision", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _git(*args: str) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    return proc.returncode, (proc.stdout or "").strip()


def _is_governance(path: str) -> bool:
    if path in GOVERNANCE_FILES or path.startswith(GOVERNANCE_PREFIXES):
        return True
    # git reports POSIX separators on every platform, so rsplit is safe here.
    return (
        path.startswith(_PREREG_ROOT)
        and path.endswith(".md")
        and path.rsplit("/", 1)[-1].startswith(_PREREG_STEM)
    )


def _drop_append_only_sessions(collision: list[str], merge_base: str) -> list[str]:
    """SESSIONS is not a 07-24 contradiction when ours only added headings."""
    if _SESSIONS not in collision:
        return collision
    code_b, base_doc = _git("show", f"{merge_base}:{_SESSIONS}")
    if code_b != 0:
        base_doc = ""
    code_o, ours_doc = _git("show", f"HEAD:{_SESSIONS}")
    if code_o != 0:
        return collision
    rs = _load_roll_sessions()
    if rs.append_only_problems(base_doc or "", ours_doc or ""):
        return collision
    return [p for p in collision if p != _SESSIONS]


def _changed(rev_range: str) -> set[str]:
    code, out = _git("diff", "--name-only", rev_range)
    if code != 0 or not out:
        return set()
    return {line.strip() for line in out.splitlines() if line.strip()}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument(
        "--base",
        default="origin/main",
        help="Upstream ref to compare against (default: origin/main).",
    )
    ap.add_argument(
        "--no-fetch",
        action="store_true",
        help="Skip the fetch (assume refs are current); used by tests.",
    )
    args = ap.parse_args()

    if os.environ.get(ESCAPE_ENV):
        print(
            f"check_push_collision: SKIPPED via {ESCAPE_ENV}=1 (collision gate bypassed).",
            file=sys.stderr,
        )
        return 0

    remote, _, branch = args.base.partition("/")
    if not args.no_fetch:
        code, _ = _git("fetch", remote, branch or "main", "--quiet")
        if code != 0:
            print(
                f"check_push_collision: could not fetch {args.base} "
                "(offline or no remote) — gate skipped, not failed.",
                file=sys.stderr,
            )
            return 0

    code, base = _git("merge-base", "HEAD", args.base)
    if code != 0 or not base:
        print(
            f"check_push_collision: no merge-base with {args.base} — gate skipped.",
            file=sys.stderr,
        )
        return 0

    theirs = {p for p in _changed(f"{base}..{args.base}") if _is_governance(p)}
    ours = {p for p in _changed(f"{base}..HEAD") if _is_governance(p)}
    collision = _drop_append_only_sessions(sorted(theirs & ours), base)

    if not collision:
        if theirs:
            print(
                f"check_push_collision: OK — {args.base} advanced on "
                f"{len(theirs)} governance path(s), none also touched here."
            )
        else:
            print("check_push_collision: OK — no governance-surface overlap.")
        return 0

    print("", file=sys.stderr)
    print(
        "GOVERNANCE COLLISION — the same decision surface changed on both sides.",
        file=sys.stderr,
    )
    print(f"  base   : {base[:12]}  (merge-base with {args.base})", file=sys.stderr)
    for path in collision:
        print(f"  BOTH   : {path}", file=sys.stderr)
    print("", file=sys.stderr)
    print(
        "A clean `git merge` is NOT evidence these agree — the 2026-07-24 case\n"
        "auto-merged WITHDRAWN and DISCHARGED into the same file with zero\n"
        "conflict markers. Read the other side's change before pushing:\n",
        file=sys.stderr,
    )
    print(f"  git log --oneline {base}..{args.base} -- {' '.join(collision)}", file=sys.stderr)
    print(f"  git diff {base}..{args.base} -- {' '.join(collision)}", file=sys.stderr)
    print("", file=sys.stderr)
    print(
        "Then merge/rebase and RE-READ the merged result for both sides of the\n"
        f"fact you changed. Deliberate override: {ESCAPE_ENV}=1 git push",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
