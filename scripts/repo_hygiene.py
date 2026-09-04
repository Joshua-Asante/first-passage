#!/usr/bin/env python3
"""repo_hygiene.py — report-only git/worktree prune candidates (squash-aware).

Surfaces what multi-hour hygiene sessions kept rediscovering:
  - linked worktrees + orphan dirs under .claude/worktrees/
  - local branches whose PR already merged (incl. squash — git branch --merged misses these)
  - local main lag vs origin/main
  - optional remote topic-branch leftovers

Never deletes. Print a machine-readable JSON report with --json, else a
human table. Operator (or the repo-hygiene skill) confirms before any
`git worktree remove` / `git branch -d` / `git push origin --delete`.

Requires: git. Optional: gh (for squash-merge detection). Offline-safe:
without gh, falls back to `git branch --merged origin/main` only and
flags the squash gap.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKTREE_PARENT = REPO_ROOT / ".claude" / "worktrees"


@dataclass
class WorktreeRow:
    path: str
    branch: str
    head: str
    is_primary: bool
    notes: str = ""


@dataclass
class BranchRow:
    name: str
    reason: str
    pr: str = ""
    safe_delete_hint: str = "git branch -d <name>  # after operator confirm"


@dataclass
class HygieneReport:
    primary_branch: str = ""
    primary_head: str = ""
    origin_main_head: str = ""
    main_behind: int = 0
    main_ahead: int = 0
    worktrees: list[WorktreeRow] = field(default_factory=list)
    orphan_worktree_dirs: list[str] = field(default_factory=list)
    merged_local_branches: list[BranchRow] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    gh_available: bool = False


def _run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd or REPO_ROOT),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _git(*args: str) -> str:
    proc = _run(["git", *args])
    if proc.returncode != 0:
        return ""
    return (proc.stdout or "").strip()


def _parse_worktrees() -> list[WorktreeRow]:
    raw = _git("worktree", "list", "--porcelain")
    rows: list[WorktreeRow] = []
    path = branch = head = ""
    for line in (raw or "").splitlines():
        if line.startswith("worktree "):
            if path:
                rows.append(
                    WorktreeRow(
                        path=path,
                        branch=branch or "(detached)",
                        head=head,
                        is_primary=os.path.normcase(path) == os.path.normcase(str(REPO_ROOT)),
                    )
                )
            path = line[len("worktree ") :].strip()
            branch = head = ""
        elif line.startswith("HEAD "):
            head = line[len("HEAD ") :].strip()[:12]
        elif line.startswith("branch "):
            ref = line[len("branch ") :].strip()
            branch = ref.replace("refs/heads/", "")
        elif line == "":
            continue
    if path:
        rows.append(
            WorktreeRow(
                path=path,
                branch=branch or "(detached)",
                head=head,
                is_primary=os.path.normcase(path) == os.path.normcase(str(REPO_ROOT)),
            )
        )
    return rows


def _orphan_dirs(registered: list[WorktreeRow]) -> list[str]:
    if not WORKTREE_PARENT.is_dir():
        return []
    registered_names = set()
    for wt in registered:
        p = Path(wt.path)
        if p.parent == WORKTREE_PARENT or (
            len(p.parts) >= 2 and p.parts[-2].lower() == "worktrees"
        ):
            registered_names.add(p.name.lower())
    orphans: list[str] = []
    for child in WORKTREE_PARENT.iterdir():
        if not child.is_dir():
            continue
        if child.name.lower() not in registered_names:
            orphans.append(str(child))
    return orphans


def _merged_via_git() -> list[BranchRow]:
    raw = _git("branch", "--merged", "origin/main")
    rows: list[BranchRow] = []
    for line in (raw or "").splitlines():
        name = line.strip()
        if name.startswith("*") or name.startswith("+"):
            name = name[1:].strip()
        # Detached-HEAD markers and empty lines are not branch names.
        if not name or name.startswith("(") or name in ("main", "master"):
            continue
        if " " in name or "\t" in name:
            continue
        rows.append(
            BranchRow(
                name=name,
                reason="ancestor of origin/main (git branch --merged)",
            )
        )
    return rows


def _merged_via_gh() -> tuple[list[BranchRow], list[str]]:
    """Return (rows, warnings). Uses gh to catch squash-merged topic branches."""
    warnings: list[str] = []
    proc = _run(["gh", "pr", "list", "--state", "merged", "--limit", "100",
                 "--json", "number,headRefName,mergedAt,url"])
    if proc.returncode != 0:
        warnings.append(
            "gh pr list failed — squash-merge detection unavailable; "
            "relying on git branch --merged only."
        )
        return [], warnings
    try:
        prs = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        warnings.append("gh pr list returned non-JSON; squash detection skipped.")
        return [], warnings

    local = _git("for-each-ref", "--format=%(refname:short)", "refs/heads/")
    local_set = {b.strip() for b in (local or "").splitlines() if b.strip()}
    rows: list[BranchRow] = []
    for pr in prs:
        name = (pr.get("headRefName") or "").strip()
        if not name or name in ("main", "master") or name not in local_set:
            continue
        rows.append(
            BranchRow(
                name=name,
                reason="PR merged (squash-aware via gh)",
                pr=f"#{pr.get('number')} {pr.get('url', '')}".strip(),
            )
        )
    return rows, warnings


def build_report() -> HygieneReport:
    report = HygieneReport()
    report.primary_branch = _git("rev-parse", "--abbrev-ref", "HEAD") or "(unknown)"
    report.primary_head = (_git("rev-parse", "--short", "HEAD") or "")[:12]
    report.origin_main_head = (_git("rev-parse", "--short", "origin/main") or "")[:12]

    behind_ahead = _git("rev-list", "--left-right", "--count", "HEAD...origin/main")
    if behind_ahead:
        parts = behind_ahead.split()
        if len(parts) == 2:
            # left-right: ahead behind when args are HEAD...origin/main
            report.main_ahead = int(parts[0])
            report.main_behind = int(parts[1])

    report.worktrees = _parse_worktrees()
    for wt in report.worktrees:
        if wt.is_primary and report.main_behind > 0 and wt.branch not in ("main", "master"):
            wt.notes = (
                f"primary not on main; HEAD behind origin/main by "
                f"{report.main_behind} (check if topic already merged)"
            )

    report.orphan_worktree_dirs = _orphan_dirs(report.worktrees)

    try:
        gh_probe = _run(["gh", "--version"])
        report.gh_available = gh_probe.returncode == 0
    except FileNotFoundError:
        report.gh_available = False

    by_name: dict[str, BranchRow] = {}
    for row in _merged_via_git():
        by_name[row.name] = row
    if report.gh_available:
        gh_rows, warns = _merged_via_gh()
        report.warnings.extend(warns)
        for row in gh_rows:
            by_name[row.name] = row  # gh reason wins (squash-aware)
    else:
        report.warnings.append(
            "gh not on PATH — squash-merged branches may be invisible to "
            "`git branch --merged`. Install GitHub CLI for full coverage."
        )

    # Exclude branches currently checked out in any worktree.
    checked_out = {wt.branch for wt in report.worktrees if wt.branch}
    report.merged_local_branches = sorted(
        (r for n, r in by_name.items() if n not in checked_out),
        key=lambda r: r.name,
    )

    for orphan in report.orphan_worktree_dirs:
        report.warnings.append(
            f"Orphan worktree dir (not in `git worktree list`): {orphan} "
            "— close Cursor handles, then remove manually / robocopy empty-dir trick on Windows."
        )
    return report


def _print_human(report: HygieneReport) -> None:
    print(f"Primary: {report.primary_branch} @ {report.primary_head}")
    print(f"origin/main: {report.origin_main_head}  "
          f"(HEAD ahead {report.main_ahead} / behind {report.main_behind})")
    print(f"gh available: {report.gh_available}")
    print()
    print("Worktrees:")
    for wt in report.worktrees:
        tag = "PRIMARY" if wt.is_primary else "linked"
        extra = f"  [{wt.notes}]" if wt.notes else ""
        print(f"  [{tag}] {wt.branch} @ {wt.head}  ->  {wt.path}{extra}")
    if report.orphan_worktree_dirs:
        print("Orphan dirs under .claude/worktrees/:")
        for p in report.orphan_worktree_dirs:
            print(f"  {p}")
    print()
    print("Merged local branch candidates (NOT deleted — operator confirm required):")
    if not report.merged_local_branches:
        print("  (none)")
    for b in report.merged_local_branches:
        pr = f"  {b.pr}" if b.pr else ""
        print(f"  {b.name}  — {b.reason}{pr}")
    if report.warnings:
        print()
        print("Warnings:")
        for w in report.warnings:
            print(f"  - {w}")
    print()
    print("Next: confirm with operator, then delete one-by-one "
          "(`git branch -d`, `git worktree remove`, never `git clean -fdX`).")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON report")
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="run `git fetch --prune` before reporting (network)",
    )
    args = parser.parse_args()
    if args.fetch:
        proc = _run(["git", "fetch", "--prune"])
        if proc.returncode != 0:
            print(proc.stderr or "git fetch failed", file=sys.stderr)
            return 1
    report = build_report()
    if args.json:
        payload = asdict(report)
        print(json.dumps(payload, indent=2))
    else:
        _print_human(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
