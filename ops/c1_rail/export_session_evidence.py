#!/usr/bin/env python3
"""Export c1 rail session evidence off the Fly volume (or a local mirror).

W6 ADR: docs/adr/2026-08-07-w6-rail-infra-closures.md

Default is dry-run (prints the copy plan). Pass --apply to copy into --dest.
Never arms the rail; never edits /data config.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

DEFAULT_SOURCES = (
    "c1_rail_events.jsonl",
    "c1_broker_evidence.jsonl",
    "c1_execution_state.json",
)


def plan(src_dir: Path, dest: Path, *, include_acks: bool) -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []
    for name in DEFAULT_SOURCES:
        src = src_dir / name
        if src.is_file():
            pairs.append((src, dest / name))
    ack_dir = src_dir / "c1_rail_alert_acks"
    if include_acks and ack_dir.is_dir():
        for p in sorted(ack_dir.iterdir()):
            if p.is_file():
                pairs.append((p, dest / "c1_rail_alert_acks" / p.name))
    return pairs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--src-dir",
        type=Path,
        default=Path("/data"),
        help="volume or local mirror (default /data)",
    )
    ap.add_argument(
        "--dest",
        type=Path,
        required=True,
        help="local directory to receive copies",
    )
    ap.add_argument(
        "--include-acks",
        action="store_true",
        help="also copy c1_rail_alert_acks/*",
    )
    ap.add_argument(
        "--apply",
        action="store_true",
        help="perform copies (default is dry-run plan only)",
    )
    args = ap.parse_args(argv)

    pairs = plan(args.src_dir, args.dest, include_acks=args.include_acks)
    if not pairs:
        print(f"WARNING: no evidence files found under {args.src_dir}", file=sys.stderr)
        return 1

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{mode}] {len(pairs)} file(s)")
    for src, dst in pairs:
        print(f"  {src} -> {dst}")
        if args.apply:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    if not args.apply:
        print("Re-run with --apply to copy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
