#!/usr/bin/env python3
"""Parse BAR EXPORT v0.1/v0.2 List-of-Trades CSV(s) into core/data/bar_data/<SYMBOL>_M15.csv.

A v0.2 export additionally writes a <SYMBOL>_M15.meta.json instrument sidecar (gitignored;
not hashed by the *.csv-only manifest gate). v0.1 exports behave exactly as before.

Usage:
    python scripts/parse_bar_export.py --symbol USDJPY
    python scripts/parse_bar_export.py --symbol USDJPY --in pageA.csv pageB.csv
    python scripts/parse_bar_export.py --symbol USDJPY --in raw.csv --out /tmp/USDJPY_M15.csv

After landing vendor bytes, regenerate manifests:
    python scripts/check_data_manifests.py --regenerate
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "core"))

from bar_export_loader import (  # noqa: E402
    DEFAULT_BAR_DIR,
    parse_bar_export_with_meta,
    write_bar_data,
    write_bar_meta,
)

DEFAULT_EXPORT_DIR = REPO_ROOT / "core" / "data" / "tv_exports" / "pepperstone" / "bar_export"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Parse BAR EXPORT v0.1 CSV(s) to a canonical bar CSV.")
    ap.add_argument("--symbol", required=True, help="e.g. USDJPY, GBPUSD, US30, XAUUSD, NAS100")
    ap.add_argument(
        "--in", dest="in_paths", nargs="+", default=None,
        help="Input List-of-Trades CSV page(s). Default: "
             "core/data/tv_exports/pepperstone/bar_export/<SYMBOL>_M15_pep.csv",
    )
    ap.add_argument("--out", default=None, help="Output CSV (default: core/data/bar_data/<SYMBOL>_M15.csv)")
    a = ap.parse_args(argv)

    if a.in_paths:
        in_paths = [Path(p) for p in a.in_paths]
    else:
        in_paths = [DEFAULT_EXPORT_DIR / f"{a.symbol}_M15_pep.csv"]

    missing = [p for p in in_paths if not p.exists()]
    if missing:
        for p in missing:
            print(f"=== missing TV export: {p} ===", file=sys.stderr)
        return 2

    df, meta = parse_bar_export_with_meta(in_paths, symbol=a.symbol)

    if a.out:
        out_target = Path(a.out)
        out_dir = out_target.parent
        written = write_bar_data(df, symbol=a.symbol, out_dir=out_dir)
        if written.name != out_target.name:
            written.replace(out_target)
            written = out_target
        out_path = written
    else:
        out_dir = DEFAULT_BAR_DIR
        out_path = write_bar_data(df, symbol=a.symbol, out_dir=out_dir)

    meta_path = write_bar_meta(meta, symbol=a.symbol, out_dir=out_dir)

    print(f"=== parsed {len(df)} bars from {len(in_paths)} page(s) -> {out_path} ===")
    if meta_path is not None:
        print(f"=== instrument metadata (v0.2) -> {meta_path} ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
