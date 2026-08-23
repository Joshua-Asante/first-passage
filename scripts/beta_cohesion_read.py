#!/usr/bin/env python3
"""CLI: pairwise lead-lag / cohesion read over named historical panels.

Public-clone posture: a missing vendor CSV is skipped, not a hard fail.
Does not write lifecycle_state.json. Does not set dry_run=false.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "lab"))
sys.path.insert(0, str(REPO / "core"))

from research_utils.beta_cohesion import (  # noqa: E402
    COHESION_CORR_FLOOR,
    DEFAULT_MAX_LAG,
    build_report,
    load_close_series,
)


def _parse_series(raw: list[str]) -> list[tuple[str, Path]]:
    out: list[tuple[str, Path]] = []
    for item in raw:
        if "=" not in item:
            raise SystemExit(f"expected NAME=PATH, got {item!r}")
        name, path = item.split("=", 1)
        out.append((name.strip(), Path(path)))
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Call-4 beta-cohesion diagnostic (report-only)")
    p.add_argument("--series", action="append", default=[], help="NAME=PATH (repeatable)")
    p.add_argument("--max-lag", type=int, default=DEFAULT_MAX_LAG)
    p.add_argument("--floor", type=float, default=COHESION_CORR_FLOOR)
    p.add_argument("--out", type=Path, help="JSON report path")
    p.add_argument("--md", type=Path, help="Markdown report path")
    args = p.parse_args(argv)

    if not args.series:
        print("no --series given; nothing to read", file=sys.stderr)
        return 0

    loaded = {}
    skipped: list[dict[str, str]] = []
    for name, path in _parse_series(args.series):
        series, reason = load_close_series(name, path)
        if series is None:
            print(f"SKIP {name}: {reason}", file=sys.stderr)
            skipped.append({"name": name, "path": str(path), "reason": reason})
            continue
        loaded[name] = series

    report = build_report(loaded, skipped, max_lag=args.max_lag, floor=args.floor)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.out:
        args.out.write_text(text + "\n")
    else:
        print(text)
    if args.md:
        args.md.write_text(_to_md(report) + "\n")
    return 0


def _to_md(report: dict) -> str:
    lines = [
        "# Beta-cohesion diagnostic",
        "",
        f"- cohesion_flag: `{report['cohesion_flag']}`",
        f"- max_lag: {report['max_lag']}",
        f"- series: {', '.join(report['series']) or '(none)'}",
        f"- skipped: {len(report['skipped'])}",
        f"- soft_flag_owner: `{report['soft_flag_owner']}`",
        "",
        "| a | b | lag | corr |",
        "|---|---|-----|------|",
    ]
    for pair in report["pairs"]:
        lines.append(
            f"| {pair['a']} | {pair['b']} | {pair['lag']} | {pair['corr']:.4f} |"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
