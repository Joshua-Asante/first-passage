"""Sentinel CLI — Tier-1 deterministic run. Report-only; always exits 0."""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from sentinel.activity_week import format_activity_decision_line
from sentinel.report import QUEUE_MARKER, QUEUE_PATH, render_run
from sentinel.scan import (
    memory_scan,
    obligation_scan,
    precondition_scan,
    preregistration_scan,
    sessions_scan,
    skew_scan,
)

_QUEUE_HEADER = (
    "# Sentinel proposal queue\n\n"
    "_Reverse-chron. Report-only; the operator authorizes every item "
    "(Action = do it, Forward = schedule it, Closed = log it)._\n\n"
    f"{QUEUE_MARKER}\n"
)


def _repo_root() -> Path:
    # ops/sentinel/__main__.py -> repo root is three parents up.
    return Path(__file__).resolve().parents[2]


def _prepend_run(queue: Path, block: str) -> None:
    prior = queue.read_text(encoding="utf-8") if queue.exists() else _QUEUE_HEADER
    if QUEUE_MARKER in prior:
        head, _, tail = prior.partition(QUEUE_MARKER)
        queue.write_text(f"{head}{QUEUE_MARKER}\n\n{block}\n{tail.lstrip()}", encoding="utf-8")
    else:
        queue.write_text(f"{prior}\n{block}\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="sentinel",
        description="INQHIORI Sentinel — Tier-1 hygiene scan (report-only).",
    )
    ap.add_argument("--asof", default=None, help="YYYY-MM-DD (default: today)")
    ap.add_argument("--horizon-days", type=int, default=60)
    ap.add_argument("--commit-lookback-days", type=int, default=14,
                    help="git-history window for the freeze-before-results scan")
    ap.add_argument("--root", default=None, help="repo root (default: inferred)")
    ap.add_argument("--memory-dir", default=None,
                    help="auto-memory dir to lint (external to repo; omit to skip)")
    ap.add_argument(
        "--activity-decision-line",
        action="store_true",
        help="print only the weekly activity-decision status line and exit 0 (no queue write)",
    )
    args = ap.parse_args()

    asof = date.fromisoformat(args.asof) if args.asof else date.today()
    root = Path(args.root) if args.root else _repo_root()
    mem_dir = Path(args.memory_dir) if args.memory_dir else None

    activity_line = format_activity_decision_line(root, asof)
    if args.activity_decision_line:
        print(activity_line)
        return 0

    findings = (
        skew_scan(root)
        + obligation_scan(root, asof=asof, horizon_days=args.horizon_days)
        + precondition_scan(root, asof=asof, horizon_days=args.horizon_days)
        + sessions_scan(root)
        + preregistration_scan(root, asof=asof, lookback_days=args.commit_lookback_days)
        + memory_scan(mem_dir, repo_root=root)
    )
    block = render_run(asof, findings, status_lines=[activity_line])

    queue = root / QUEUE_PATH
    queue.parent.mkdir(parents=True, exist_ok=True)
    _prepend_run(queue, block)

    print(activity_line)
    print(f"sentinel: {len(findings)} finding(s) at asof {asof.isoformat()} -> {QUEUE_PATH}")
    for f in findings:
        print(f"  [{f.routing}] {f.id} ({f.source})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
