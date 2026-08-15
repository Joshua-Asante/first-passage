#!/usr/bin/env python3
"""Parse BAR EXPORT v0.1 List-of-Trades CSVs into OHLCV bar files (Q-FEED-1 Phase 1)."""
from __future__ import annotations

import argparse
import csv
import importlib.util
import sys
from pathlib import Path

_LIB_PATH = Path(__file__).resolve().parent / "_lib.py"
_spec = importlib.util.spec_from_file_location("feed_div_lib", _LIB_PATH)
_feed_div_lib = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
sys.modules[_spec.name] = _feed_div_lib
_spec.loader.exec_module(_feed_div_lib)

parse_tv_bar_export = _feed_div_lib.parse_tv_bar_export
tv_panel_path = _feed_div_lib.tv_panel_path

FIELDS = ["time", "open", "high", "low", "close", "volume"]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Parse TV BAR EXPORT v0.1 CSV to OHLCV bar CSV.")
    ap.add_argument("--symbol", required=True, help="USDJPY, GBPUSD, or US30")
    ap.add_argument("--in", dest="in_path", default=None, help="Input List-of-Trades CSV")
    ap.add_argument("--out", default=None, help="Output bar CSV (default: sibling .bars.csv)")
    a = ap.parse_args(argv)

    in_path = Path(a.in_path) if a.in_path else tv_panel_path(a.symbol)
    out_path = Path(a.out) if a.out else in_path.with_suffix(".bars.csv")

    if not in_path.exists():
        print(f"=== missing TV export: {in_path} ===", file=sys.stderr)
        return 2

    bars = parse_tv_bar_export(in_path, symbol=a.symbol)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for _, row in bars.iterrows():
            w.writerow({
                "time": row["tv_time"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                "open": row["open"],
                "high": row["high"],
                "low": row["low"],
                "close": row["close"],
                "volume": int(row["volume"]),
            })

    print(f"=== parsed {len(bars)} bars from {in_path} -> {out_path} ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
