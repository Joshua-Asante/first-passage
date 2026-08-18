#!/usr/bin/env python3
"""Parse ECON EXPORT v0.1 List-of-Trades CSVs into per-field ISO date sets.

Transport mirrors BAR_EXPORT (Entry rows, Signal/comment pipe, epoch_ms authority)
but the payload is NOT OHLCV — do not reuse bar_export_loader.SIGNAL_PIPE_V2_RE.

Signal grammar:
    {epoch_ms}|{country}|{field}|{value}|{tz}|{tf}

Usage:
    python scripts/parse_econ_export.py --in path.csv
    python scripts/parse_econ_export.py --in a.csv b.csv --json
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[1]
SIGNAL_RE = re.compile(
    r"^(?P<epoch>\d+)\|(?P<country>[A-Z]{2})\|(?P<field>[A-Z0-9]+)"
    r"\|(?P<value>[^|]*)\|(?P<tz>[^|]*)\|(?P<tf>[^|]*)$"
)
ET = ZoneInfo("America/New_York")


class EconExportError(ValueError):
    """Malformed ECON EXPORT v0.1 row or file."""


def utc_date_from_epoch_ms(epoch_ms: int) -> str:
    return datetime.fromtimestamp(epoch_ms / 1000, tz=timezone.utc).date().isoformat()


def et_date_from_epoch_ms(epoch_ms: int) -> str:
    return datetime.fromtimestamp(epoch_ms / 1000, tz=ET).date().isoformat()


def decode_econ_signal(signal: str) -> dict[str, str | int]:
    text = (signal or "").strip()
    m = SIGNAL_RE.match(text)
    if not m:
        raise EconExportError(f"unrecognized ECON EXPORT signal: {text!r}")
    epoch_ms = int(m.group("epoch"))
    return {
        "epoch_ms": epoch_ms,
        "country": m.group("country"),
        "field": m.group("field"),
        "value": m.group("value"),
        "tz": m.group("tz"),
        "tf": m.group("tf"),
        "utc_date": utc_date_from_epoch_ms(epoch_ms),
        "et_date": et_date_from_epoch_ms(epoch_ms),
    }


def _signal_cell(row: dict[str, str]) -> str:
    for key in ("Signal", "Comment", "signal", "comment"):
        if key in row and row[key]:
            return row[key]
    raise EconExportError(f"row missing Signal/Comment: {row!r}")


def _is_entry(row: dict[str, str]) -> bool:
    typ = (row.get("Type") or row.get("type") or "").strip()
    return typ.startswith("Entry")


def parse_econ_export(paths: Iterable[Path]) -> dict[str, set[str]]:
    """Return {FIELD: set of UTC ISO dates} from one or more LoT CSVs."""
    by_field: dict[str, set[str]] = defaultdict(set)
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(path)
        with path.open(encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames is None:
                raise EconExportError(f"{path}: empty CSV")
            for row in reader:
                if not _is_entry(row):
                    continue
                decoded = decode_econ_signal(_signal_cell(row))
                by_field[str(decoded["field"])].add(str(decoded["utc_date"]))
    return {k: set(v) for k, v in by_field.items()}


def parse_econ_export_rows(paths: Iterable[Path]) -> list[dict[str, str | int]]:
    """All decoded Entry rows (for TZ_SHIFT, which needs ET as well as UTC)."""
    rows: list[dict[str, str | int]] = []
    for path in paths:
        with path.open(encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames is None:
                raise EconExportError(f"{path}: empty CSV")
            for row in reader:
                if not _is_entry(row):
                    continue
                rows.append(decode_econ_signal(_signal_cell(row)))
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Parse ECON EXPORT v0.1 LoT CSV(s).")
    ap.add_argument("--in", dest="in_paths", nargs="+", required=True, help="List-of-Trades CSV path(s)")
    ap.add_argument("--json", action="store_true", help="Emit JSON {field: [dates]}")
    a = ap.parse_args(argv)
    paths = [Path(p) for p in a.in_paths]
    missing = [p for p in paths if not p.is_file()]
    if missing:
        for p in missing:
            print(f"=== missing ECON export: {p} ===", file=sys.stderr)
        return 2
    by_field = parse_econ_export(paths)
    if a.json:
        print(json.dumps({k: sorted(v) for k, v in sorted(by_field.items())}, indent=2))
    else:
        for field, dates in sorted(by_field.items()):
            print(f"{field}\t{len(dates)}")
            for d in sorted(dates):
                print(f"  {d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
