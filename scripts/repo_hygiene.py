#!/usr/bin/env python3
"""repo_hygiene.py — report-only git/worktree prune candidates (squash-aware).

Surfaces what multi-hour hygiene sessions kept rediscovering:
  - linked worktrees, each clean / dirty / unknown, + orphan dirs under .claude/worktrees/
  - ignored, non-regenerable files inside each linked worktree (the ones
    `git worktree remove` deletes without asking — M-41)
  - local branches already merged: ancestors of origin/main, or squash-merged
    with the local tip equal to the merged PR's head
  - local branches whose PR merged but whose tip differs (not candidates)
  - primary checkout lag vs origin/main

Never deletes. Print a machine-readable JSON report with --json, else a
human table. Operator (or the repo-hygiene skill) confirms before any
`git worktree remove` / `git branch -d` / `git push origin --delete`.

Works from the primary checkout or any linked worktree. A worktree that cannot
be scanned is `unknown`, never clean.

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
GH_PR_LIMIT = 5000
# Ignored entries a fresh setup regenerates; anything else ignored inside a linked
# worktree may be the only copy of private evidence (M-41).
REGENERABLE = {
    ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "node_modules", ".tox", ".coverage", "htmlcov",
}


@dataclass
class WorktreeRow:
    path: str
    branch: str
    head: str
    is_primary: bool
    notes: str = ""
    state: str = "not scanned"  # linked worktrees: clean, dirty or unknown
    private: list[str] = field(default_factory=list)


@dataclass
class BranchRow:
    name: str
    reason: str
    pr: str = ""
    safe_delete_hint: str = ""


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
    diverged_merged_branches: list[BranchRow] = field(default_factory=list)
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


def _git(*args: str, cwd: Path | None = None) -> str:
    proc = _run(["git", *args], cwd=cwd)
    if proc.returncode != 0:
        return ""
    return (proc.stdout or "").strip()


def _parse_worktrees() -> list[WorktreeRow]:
    """`git worktree list` always names the primary checkout first."""
    raw = _git("worktree", "list", "--porcelain")
    rows: list[WorktreeRow] = []
    for line in (raw or "").splitlines():
        if line.startswith("worktree "):
            rows.append(
                WorktreeRow(
                    path=line[len("worktree ") :].strip(),
                    branch="(detached)",
                    head="",
                    is_primary=not rows,
                )
            )
        elif line.startswith("HEAD ") and rows:
            rows[-1].head = line[len("HEAD ") :].strip()[:12]
        elif line.startswith("branch ") and rows:
            rows[-1].branch = line[len("branch ") :].strip().replace("refs/heads/", "")
    return rows


def _scan_worktree(path: str) -> tuple[str, list[str]]:
    """Return (clean | dirty | unknown, ignored non-regenerable entries).

    `git worktree remove` refuses untracked files but deletes ignored ones without
    asking, so a failed scan is `unknown`, never an empty result."""
    try:
        proc = _run(
            ["git", "status", "--porcelain=v1", "--ignored", "--untracked-files=normal", "-z"],
            cwd=Path(path),
        )
    except OSError:
        return "unknown", []
    if proc.returncode != 0:
        return "unknown", []
    dirty = False
    entries = []
    for item in (proc.stdout or "").split("\0"):
        if not item:
            continue
        if not item.startswith("!! "):
            dirty = True
            continue
        rel = item[3:]
        parts = [p for p in rel.rstrip("/").split("/") if p]
        if any(p in REGENERABLE or p.endswith((".egg-info", ".pyc")) for p in parts):
            continue
        entries.append(rel)
    return ("dirty" if dirty else "clean"), sorted(entries)


def _scan_warnings(worktrees: list[WorktreeRow]) -> list[str]:
    """Scan each linked worktree; warn on any holding ignored entries or unscannable."""
    warnings = []
    for wt in worktrees:
        if wt.is_primary:
            continue
        wt.state, wt.private = _scan_worktree(wt.path)
        if wt.state == "unknown":
            warnings.append(
                f"Could not scan linked worktree {wt.path} — treat it as not removable."
            )
        if wt.private:
            warnings.append(
                f"Linked worktree {wt.path} holds {len(wt.private)} ignored "
                f"entr{'y' if len(wt.private) == 1 else 'ies'} that `git worktree remove` "
                "deletes without asking — archive (`scripts/evidence_archive.py put`) or "
                "move them first (M-41)."
            )
    return warnings


def _path_key(path: str | Path) -> str:
    return os.path.normcase(str(Path(path).resolve()))


def _orphan_dirs(registered: list[WorktreeRow]) -> list[str]:
    if not registered:
        return []
    parent = Path(registered[0].path) / ".claude" / "worktrees"
    if not parent.is_dir():
        return []
    known = {_path_key(wt.path) for wt in registered}
    return sorted(
        str(child) for child in parent.iterdir()
        if child.is_dir() and _path_key(child) not in known
    )


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
                safe_delete_hint=f"git branch -d {name}  # after operator confirm",
            )
        )
    return rows


def _merged_via_gh() -> tuple[list[BranchRow], list[BranchRow], list[str]]:
    """Return (tip-matched rows, diverged rows, warnings) for squash-merged branches."""
    warnings: list[str] = []
    proc = _run(["gh", "pr", "list", "--state", "merged", "--limit", str(GH_PR_LIMIT),
                 "--json", "number,headRefName,headRefOid,mergedAt,url"])
    if proc.returncode != 0:
        warnings.append(
            "gh pr list failed — squash-merge detection unavailable; "
            "relying on git branch --merged only."
        )
        return [], [], warnings
    try:
        prs = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        warnings.append("gh pr list returned non-JSON; squash detection skipped.")
        return [], [], warnings
    if len(prs) >= GH_PR_LIMIT:
        warnings.append(
            f"gh pr list hit its {GH_PR_LIMIT} limit — older merged PRs were not checked."
        )

    local = _git("for-each-ref", "--format=%(refname:short) %(objectname)", "refs/heads/")
    tips = dict(line.rsplit(" ", 1) for line in (local or "").splitlines() if " " in line)
    by_branch: dict[str, list[dict]] = {}
    for pr in prs:
        name = (pr.get("headRefName") or "").strip()
        if name in tips and name not in ("main", "master"):
            by_branch.setdefault(name, []).append(pr)

    rows: list[BranchRow] = []
    diverged: list[BranchRow] = []
    for name, branch_prs in by_branch.items():
        match = next((p for p in branch_prs if p.get("headRefOid") == tips[name]), None)
        pr = match or branch_prs[0]
        label = f"#{pr.get('number')} {pr.get('url', '')}".strip()
        if match:
            rows.append(BranchRow(
                name=name,
                reason="PR merged; local tip equals PR head (squash-aware via gh)",
                pr=label,
                safe_delete_hint=(
                    f"git branch -D {name}  # only if the operator orders -D; "
                    "`-d` refuses squash merges"
                ),
            ))
        else:
            diverged.append(BranchRow(
                name=name,
                reason="PR merged, but local tip differs from every merged PR head",
                pr=label,
            ))
    return rows, diverged, warnings


def build_report() -> HygieneReport:
    report = HygieneReport()
    report.worktrees = _parse_worktrees()
    primary = report.worktrees[0] if report.worktrees else None
    if primary is None:
        report.warnings.append("`git worktree list` returned nothing — no worktree was checked.")
    report.primary_branch = primary.branch if primary else "(unknown)"
    report.primary_head = primary.head if primary else ""
    report.origin_main_head = (_git("rev-parse", "--short", "origin/main") or "")[:12]

    behind_ahead = _git(
        "rev-list", "--left-right", "--count", "HEAD...origin/main",
        cwd=Path(primary.path) if primary else None,
    )
    if behind_ahead:
        parts = behind_ahead.split()
        if len(parts) == 2:
            # left-right: ahead behind when args are HEAD...origin/main
            report.main_ahead = int(parts[0])
            report.main_behind = int(parts[1])

    if primary and report.main_behind > 0 and primary.branch not in ("main", "master"):
        primary.notes = (
            f"primary not on main; HEAD behind origin/main by "
            f"{report.main_behind} (check if topic already merged)"
        )

    report.warnings.extend(_scan_warnings(report.worktrees))
    report.orphan_worktree_dirs = _orphan_dirs(report.worktrees)

    try:
        gh_probe = _run(["gh", "--version"])
        report.gh_available = gh_probe.returncode == 0
    except FileNotFoundError:
        report.gh_available = False

    by_name = {row.name: row for row in _merged_via_git()}
    diverged: list[BranchRow] = []
    if report.gh_available:
        gh_rows, diverged, warns = _merged_via_gh()
        report.warnings.extend(warns)
        for row in gh_rows:
            by_name.setdefault(row.name, row)  # an ancestor proof beats a PR match
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
    report.diverged_merged_branches = sorted(
        (r for r in diverged if r.name not in checked_out and r.name not in by_name),
        key=lambda r: r.name,
    )

    for orphan in report.orphan_worktree_dirs:
        report.warnings.append(
            f"Orphan worktree dir (not in `git worktree list`): {orphan} "
            "— close any editor/agent handles, then remove manually / robocopy empty-dir trick on Windows."
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
        print(f"  [{tag}] {wt.branch} @ {wt.head} ({wt.state})  ->  {wt.path}{extra}")
        for entry in wt.private[:10]:
            print(f"      ignored: {entry}")
        if len(wt.private) > 10:
            print(f"      ... and {len(wt.private) - 10} more (--json lists all)")
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
        print(f"      {b.safe_delete_hint}")
    if report.diverged_merged_branches:
        print()
        print("PR merged but local tip differs (NOT candidates — review first):")
        for b in report.diverged_merged_branches:
            print(f"  {b.name}  — {b.pr}")
    if report.warnings:
        print()
        print("Warnings:")
        for w in report.warnings:
            print(f"  - {w}")
    print()
    print("Next: confirm with operator, then delete one-by-one "
          "(each row's hint, `git worktree remove`, never `git clean -fdX`).")


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
