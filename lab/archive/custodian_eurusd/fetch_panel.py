#!/usr/bin/env python3
# Dukascopy retired 2026-06-17 (docs/adr/2026-06-17-dukascopy-retirement.md) — frozen historical artifact; no longer runs.
"""Fetch the three Dukascopy m15 panels for the Custodian-EURUSD mechanism probe.

Thin wrapper over ``core/lib/dukascopy.fetch_candles`` (PR #152), mirroring
``lab/analysis/noct_spx/fetch_panel.py``. Pulls each panel in year chunks
(progress visibility + bounded memory) and writes the canonical
``core/data/bar_data/*.csv`` schema consumed by ``validation.sweep.feed_loader``.

Three panels (brief §2.1):
  * EURUSD       -> EURUSD_M15.csv         (point_factor 1e5, mapped in adapter)
  * USA500IDXUSD -> USA500IDXUSD_M15.csv   (point_factor 1e3; reuse noct panel)
  * EUSIDXEUR    -> EUSIDXEUR_M15.csv      (point_factor 1e3; EuroStoxx-50)

EuroStoxx-50 symbol/factor DISCOVERED + verified empirically (brief §0.5-1,
Phase-0 probe): EUSIDXEUR / 1e3 tracks the EuroStoxx-50 index level across the
whole window — 2016-01 ~3176, 2016-06 ~3035, 2018 ~3677, COVID-low (2020-03-23)
~2473, 2022 ~4391, 2024 ~5078 — matching the published index history (the
COVID-trough ~2450 is the load-bearing cross-check a wrong factor could not
reproduce). Indices are NOT in the adapter's factor map, so the factor is passed
explicitly, exactly as noct passed 1e3 for USA500IDXUSD.

Closed-market hours (Sunday pre-open, holidays) return HTTP 503 (not 404) on
Dukascopy; the adapter's default (non-strict) mode skips them with a COUNT (never
silent — ``stats["closed"]``) rather than aborting the multi-year pull. That
robustness lives in the adapter itself (PR #153) — NO local monkeypatch.

Usage (one symbol at a time; each is a tens-of-minutes job):
    python lab/analysis/custodian_eurusd/fetch_panel.py --symbol EURUSD \
        --point-factor 100000 --out core/data/bar_data/EURUSD_M15.csv \
        --start 2016-01-01 --end 2026-06-09

THROUGHPUT / RATE-LIMIT NOTE (load-bearing, this environment 2026-06-09):
Dukascopy rate-limits high worker concurrency by returning HTTP 503 on hours
that ARE open — the adapter classifies those as "closed" (counted, never silent)
but they become real data gaps. Probed: 8 workers -> ~0 spurious 503s but a full
10.5yr m15 pull is ~4-5h sequential (per-request latency bound); 16-48 workers
-> 24-50% spurious 503s. A full dense panel is therefore impractical here.

TARGETED MODE (--days-window N): the mechanism probe needs only the last
trading day of each month for the EURUSD y-window, and the prev-month-end + T-1
DAILY closes for the SPX/EStoxx x-legs. ``--days-window N`` fetches ONLY the last
N calendar days of each month across the window (a strict subset of the full
panel, identical schema/feed/factor), which both dodges the rate limiter and is
~100x cheaper. The resulting CSV is sparse but the gate reads only those days, so
x/y are byte-identical to what a dense panel would yield. Use the dense (default)
mode if a future dense-feed sweep needs it. This is flagged in README deviations.
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

FIELDS = ["time", "open", "high", "low", "close", "volume"]

# Verified/known factors for the three probe panels.
KNOWN_FACTOR = {
    "EURUSD": 1e5,
    "USA500IDXUSD": 1e3,
    "EUSIDXEUR": 1e3,        # EuroStoxx-50, verified Phase 0 (see module docstring)
}


def _year_chunks(start: str, end: str):
    sy, ey = int(start[:4]), int(end[:4])
    bounds = [start] + [f"{y}-01-01T00:00:00Z" for y in range(sy + 1, ey + 1)] + [end]
    seen, ordered = set(), []
    for b in bounds:
        if b not in seen:
            seen.add(b)
            ordered.append(b)
    for i in range(len(ordered) - 1):
        yield ordered[i], ordered[i + 1]


def _month_tail_chunks(start: str, end: str, days_window: int):
    """Yield (chunk_start, chunk_end) UTC strings covering ONLY the last
    ``days_window`` calendar days of each month in [start, end). Targeted mode:
    a strict subset of the full panel sufficient for the month-end y-window and
    the prev-month-end/T-1 daily closes."""
    import calendar as _cal
    from datetime import date as _date, timedelta as _td
    sy, sm = int(start[:4]), int(start[5:7])
    ey, em = int(end[:4]), int(end[5:7])
    y, m = sy, sm
    while (y, m) <= (ey, em):
        last_dom = _cal.monthrange(y, m)[1]
        month_end = _date(y, m, last_dom)
        # widen by 1 trailing day so the 1st of the next month's early hours are
        # also captured if a month-end print spills; and start days_window back.
        cs = month_end - _td(days=max(1, days_window) - 1)
        ce = month_end + _td(days=1)
        yield (f"{cs.isoformat()}T00:00:00Z", f"{ce.isoformat()}T00:00:00Z")
        m += 1
        if m > 12:
            m = 1
            y += 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Dukascopy m15 fetch (chunked) for Custodian probe.")
    ap.add_argument("--symbol", required=True, help="Dukascopy symbol, e.g. EURUSD / USA500IDXUSD / EUSIDXEUR")
    ap.add_argument("--out", required=True)
    ap.add_argument("--point-factor", type=float, default=None,
                    help="price divisor; defaults to the known factor for the three probe panels")
    ap.add_argument("--start", default="2016-01-01T00:00:00Z")
    ap.add_argument("--end", default="2026-06-09T00:00:00Z")
    ap.add_argument("--workers", type=int, default=8,
                    help="parallel hourly downloads; KEEP LOW (~8) — high concurrency "
                         "triggers Dukascopy rate-limit 503s misclassified as closed hours")
    ap.add_argument("--days-window", type=int, default=None,
                    help="targeted mode: fetch only the last N calendar days of each "
                         "month (sufficient for the month-end probe; dodges the rate limiter)")
    ap.add_argument("--strict", action="store_true",
                    help="abort on any persistent non-404 (closed-market 5xx) instead of skipping")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)

    factor = a.point_factor if a.point_factor is not None else KNOWN_FACTOR.get(a.symbol.upper())
    if factor is None:
        print(f"=== no known point_factor for {a.symbol!r}; pass --point-factor explicitly ===",
              file=sys.stderr)
        return 2

    start = a.start if "T" in a.start else a.start + "T00:00:00Z"
    end = a.end if "T" in a.end else a.end + "T00:00:00Z"

    out = Path(a.out)
    if out.exists() and out.stat().st_size > 1024 and not a.force:
        print(f"=== {out} exists ({out.stat().st_size} bytes) — use --force to refetch ===")
        return 0

    chunks = (list(_month_tail_chunks(start, end, a.days_window))
              if a.days_window else list(_year_chunks(start, end)))
    mode = f"targeted last-{a.days_window}d/month" if a.days_window else "dense (full panel)"
    print(f"=== {a.symbol} fetch mode: {mode}, {len(chunks)} chunks, {a.workers} workers ===",
          flush=True)

    all_rows: list[dict] = []
    total_closed = total_missing = 0
    for cs, ce in chunks:
        t0 = time.time()
        stats: dict = {}
        rows = list(dk.fetch_candles(a.symbol, cs, ce, granularity="M15", price="M",
                                     point_factor=factor, workers=a.workers,
                                     strict=a.strict, stats=stats))
        all_rows.extend(rows)
        total_closed += stats.get("closed", 0)
        total_missing += stats.get("missing", 0)
        print(f"  {cs[:10]}..{ce[:10]}: {len(rows):>6} bars  "
              f"(closed {stats.get('closed', 0)} / missing {stats.get('missing', 0)}, "
              f"{time.time()-t0:.0f}s)", flush=True)

    # Dedupe by timestamp (targeted-mode month windows can overlap by a trailing day).
    dedup = {r["time"]: r for r in all_rows}
    all_rows = [dedup[t] for t in sorted(dedup)]
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(all_rows)

    print(f"=== {a.symbol}: wrote {len(all_rows)} bars to {out} (factor {factor:g}) ===")
    if all_rows:
        print(f"=== first {all_rows[0]['time']} | last {all_rows[-1]['time']} ===")
    print(f"=== total closed-market hours skipped: {total_closed}; missing/404: {total_missing} ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
