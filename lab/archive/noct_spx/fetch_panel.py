#!/usr/bin/env python3
# Dukascopy retired 2026-06-17 (docs/adr/2026-06-17-dukascopy-retirement.md) — frozen historical artifact; no longer runs.
"""Fetch the Dukascopy USA500IDXUSD m15 panel for the NOCT-SPX-001 gate.

Thin wrapper over ``core/lib/dukascopy.fetch_candles`` that pulls the panel in
year chunks (progress visibility + bounded memory) and writes the canonical
``core/data/bar_data/*.csv`` schema consumed by ``validation.sweep.feed_loader``.

Closed-market hours (Sunday pre-open, holidays) return **HTTP 503, not 404** on
Dukascopy; the adapter's default (non-strict) mode skips them with a COUNT (never
silent — `stats["closed"]`) rather than aborting the multi-year pull. That
robustness now lives in the adapter itself (PR #153, `core/lib/dukascopy.py`);
this script previously carried a local `_download` monkeypatch for it, removed
once the native fix landed.

point_factor=1e3 verified empirically (Phase 0): Dukascopy raw / OANDA
SPX500_USD close ~= 1000; historical levels track the S&P 500 (2011~1216,
2016~2020, COVID~2452, 2026~7550).

Usage:
    python lab/analysis/noct_spx/fetch_panel.py \
        --out core/data/bar_data/USA500IDXUSD_M15.csv --start 2020-01-01 --end 2026-06-07
"""
from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT / "core"))

from lib import dukascopy as dk  # noqa: E402

INSTRUMENT = "USA500IDXUSD"
POINT_FACTOR = 1000.0
FIELDS = ["time", "open", "high", "low", "close", "volume"]


def _year_chunks(start: str, end: str):
    sy, ey = int(start[:4]), int(end[:4])
    bounds = [start] + [f"{y}-01-01T00:00:00Z" for y in range(sy + 1, ey + 1)] + [end]
    seen, ordered = set(), []
    for b in bounds:
        if b not in seen:
            seen.add(b); ordered.append(b)
    for i in range(len(ordered) - 1):
        yield ordered[i], ordered[i + 1]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Dukascopy USA500IDXUSD m15 fetch (chunked).")
    ap.add_argument("--out", required=True)
    ap.add_argument("--start", default="2020-01-01T00:00:00Z")
    ap.add_argument("--end", default="2026-06-07T00:00:00Z")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--strict", action="store_true",
                    help="abort on any persistent non-404 (closed-market 5xx) instead of skipping")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)

    start = a.start if "T" in a.start else a.start + "T00:00:00Z"
    end = a.end if "T" in a.end else a.end + "T00:00:00Z"

    out = Path(a.out)
    if out.exists() and out.stat().st_size > 1024 and not a.force:
        print(f"=== {out} exists ({out.stat().st_size} bytes) — use --force to refetch ===")
        return 0

    all_rows: list[dict] = []
    total_closed = 0
    for cs, ce in _year_chunks(start, end):
        t0 = time.time()
        stats: dict = {}
        rows = list(dk.fetch_candles(INSTRUMENT, cs, ce, granularity="M15", price="M",
                                     point_factor=POINT_FACTOR, workers=a.workers,
                                     strict=a.strict, stats=stats))
        all_rows.extend(rows)
        total_closed += stats.get("closed", 0)
        print(f"  {cs[:10]}..{ce[:10]}: {len(rows):>6} bars  "
              f"(closed {stats.get('closed', 0)} / missing {stats.get('missing', 0)}, "
              f"{time.time()-t0:.0f}s)", flush=True)

    all_rows.sort(key=lambda r: r["time"])
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(all_rows)

    print(f"=== wrote {len(all_rows)} bars to {out} ===")
    if all_rows:
        print(f"=== first {all_rows[0]['time']} | last {all_rows[-1]['time']} ===")
    print(f"=== total closed-market hours skipped: {total_closed} ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
