#!/usr/bin/env python3
"""Merge non-secret keys into a c1_rail_config.json (volume or local).

W6 ADR: docs/adr/2026-08-07-w6-rail-infra-closures.md

Prefers this (or c1_rail_arm.py for dry_run/armed_until) over hand-editing JSON
— the 07-20/07-27 defect class. Aborts unless dry_run is true in the target
config (use --force-armed only under an attended operator GO).
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

# Keys agents may merge without an arming GO. Secrets stay out of argv — set
# those via sftp of a locally filled example, never logged here.
ALLOWED_KEYS = frozenset({
    "events_log_path",
    "execution_state_path",
    "alert_log_path",
    "alert_ack_dir",
    "equity_source",
    "equity_field",
    "account",
})


def _atomic_write(path: Path, data: dict) -> Path:
    backup = path.with_suffix(path.suffix + ".bak")
    if path.is_file():
        backup.write_bytes(path.read_bytes())
    text = json.dumps(data, indent=2) + "\n"
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", delete=False, dir=str(path.parent),
    ) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)
    return backup


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument(
        "--set",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="merge KEY=VALUE (repeatable); KEY must be in ALLOWED_KEYS",
    )
    ap.add_argument(
        "--force-armed",
        action="store_true",
        help="allow write when dry_run is false (operator GO only)",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="print planned merge; do not write",
    )
    args = ap.parse_args(argv)

    if not args.config.is_file():
        print(f"ERROR: missing config {args.config}", file=sys.stderr)
        return 1
    try:
        cfg = json.loads(args.config.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read config: {exc}", file=sys.stderr)
        return 1

    if cfg.get("dry_run", True) is not True and not args.force_armed:
        print(
            "ERROR: refusing to write — config dry_run is not true. "
            "Disarm first (c1_rail_arm.py --disarm) or pass --force-armed "
            "under an attended operator GO.",
            file=sys.stderr,
        )
        return 1

    updates: dict = {}
    for item in args.set:
        if "=" not in item:
            print(f"ERROR: expected KEY=VALUE, got {item!r}", file=sys.stderr)
            return 1
        key, value = item.split("=", 1)
        if key not in ALLOWED_KEYS:
            print(
                f"ERROR: key {key!r} not in ALLOWED_KEYS {sorted(ALLOWED_KEYS)}",
                file=sys.stderr,
            )
            return 1
        updates[key] = value

    if not updates:
        print("ERROR: no --set KEY=VALUE provided", file=sys.stderr)
        return 1

    new_cfg = dict(cfg)
    new_cfg.update(updates)
    print(f"target : {args.config}")
    for k, v in updates.items():
        print(f"  {k}: {cfg.get(k)!r} -> {v!r}")
    if args.dry_run:
        print("DRY-RUN — no write")
        return 0
    backup = _atomic_write(args.config, new_cfg)
    print(f"wrote  : {args.config}")
    print(f"backup : {backup}")
    print("*** Restart the host process to apply path/ledger keys constructed at boot.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
