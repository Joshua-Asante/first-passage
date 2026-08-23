#!/usr/bin/env python3
"""Thin CLI: event-study + detector kit JSON report. Not a lock decision.

Public-clone posture: a missing vendor CSV is skipped, not a hard fail.
Does not write lifecycle_state.json. Does not set dry_run=false.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "lab"))


def _load_returns(path: Path, column: str | None) -> tuple[pd.Series | None, str | None]:
    if not path.exists():
        return None, f"missing file {path}"
    try:
        df = pd.read_csv(path)
    except Exception as exc:  # pragma: no cover — skip path
        return None, f"unreadable {path}: {exc}"
    if df.empty:
        return None, f"empty {path}"
    time_col = next(
        (c for c in df.columns if str(c).lower() in {"date", "time", "datetime", "timestamp"}),
        df.columns[0],
    )
    value_col = column or next(
        (c for c in df.columns if str(c).lower() in {"return", "ret", "r", "close"}),
        df.columns[-1],
    )
    try:
        idx = pd.to_datetime(df[time_col], utc=False)
    except Exception as exc:
        return None, f"bad time column {time_col!r}: {exc}"
    series = pd.Series(df[value_col].to_numpy(), index=idx, name=value_col)
    if str(value_col).lower() == "close":
        series = series.astype(float).pct_change().dropna()
    return series.dropna(), None


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="T2 event-study + detector kit (report-only)")
    p.add_argument("--returns", type=Path, help="CSV with a time column and a return/close column")
    p.add_argument("--column", help="return column name")
    p.add_argument("--calendar", choices=("month-end",), default="month-end")
    p.add_argument("--window-pre", type=int, default=-1)
    p.add_argument("--window-post", type=int, default=1)
    p.add_argument("--out", type=Path, help="JSON report path")
    args = p.parse_args(argv)

    if args.returns is None:
        print("no --returns given; nothing to read", file=sys.stderr)
        return 0

    from research_utils.detector_kit import detector_report
    from research_utils.event_study import event_study, month_end_events

    series, reason = _load_returns(args.returns, args.column)
    if series is None:
        print(f"SKIP: {reason}", file=sys.stderr)
        report = {"skipped": True, "reason": reason, "lock_decision": None}
    else:
        events = month_end_events(series.index) if args.calendar == "month-end" else []
        report = {
            "skipped": False,
            "event_study": event_study(
                series, events, window=(args.window_pre, args.window_post)
            ),
            "detectors": detector_report(series.to_numpy()),
            "lock_decision": None,
        }

    text = json.dumps(report, indent=2, sort_keys=True)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
