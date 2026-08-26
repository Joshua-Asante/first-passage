"""Task 2 (S10) prerequisite: recover genuine, non-degenerate 6J M15 OHLC from the
raw ``BAR_EXPORT_v0.2`` trade-list export.

Why this exists: this repo's own committed panel (``core/data/bar_data/6J_M15.csv``)
decodes 6J's OHLC from a 5-decimal-place-rounded text field, which at 6J's mintick
(5e-7) is a 20-tick quantisation -- measured 51.4% of bars decode to O==H==L==C on
this exact file (verified directly, 2026-08-26; matches the independently-discovered
figure in ``lesson_bar_export_ohlc_degenerate_fine_tick`` of 67%, same defect,
different sample). Using that panel's low/high directly for an excursion
reconstruction would be silently wrong for roughly half the bars.

Recovery method (verified elsewhere on this exact file, reused verbatim, not
re-derived): the bar-exporter Pine reverses a synthetic 1-contract position every
bar (``process_orders_on_close``), so each "Entry" row's own Price USD (7dp) is
the bar's CLOSE, and the *next* bar's high/low come from that entry's own
Favorable/Adverse excursion USD columns (direction-aware: long -> favorable=up,
adverse=down; short -> swapped). Consecutive entries chronologically give a
continuous, non-degenerate close series; the excursion columns give high/low.

Output: ``data/6j_m15_recovered.csv`` (time,open,high,low,close columns, best-effort
open = previous bar's close) plus validation stats printed to stdout.
"""
from __future__ import annotations

import csv
import sys

RAW_PATH = r"C:\Users\joshu\Downloads\BAR_EXPORT_v0.2_CME_6J1!_2026-07-13_99781.csv"
OUT_PATH = "data/6j_m15_recovered.csv"

MINTICK = 0.0000005
POINTVALUE = 12_500_000.0
TICK_VALUE = MINTICK * POINTVALUE  # $6.25/tick at qty=1


def load_entries():
    with open(RAW_PATH, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    entries = [r for r in rows if r["Type"].startswith("Entry")]
    for r in entries:
        qty = float(r["Size (qty)"])
        if qty != 1.0:
            raise ValueError(f"expected qty=1 throughout the synthetic harness export, got {qty}")
    entries.sort(key=lambda r: r["Date and time"])
    return entries


def recover(entries):
    """-> list of dict(time, open, high, low, close), one per bar (len == len(entries) - 1,
    since bar k's high/low need entry k-1's excursion columns and bar k's close needs
    entry k's own price -- the very first entry only anchors bar 0's close, never a
    full bar with a known high/low of its own from THIS file)."""
    bars = []
    for k in range(1, len(entries)):
        prev, cur = entries[k - 1], entries[k]
        direction = "long" if "long" in prev["Type"].lower() else "short"
        entry_price = float(prev["Price USD"])
        fav_usd = float(prev["Favorable excursion USD"])
        adv_usd = float(prev["Adverse excursion USD"])  # <= 0 by TV convention
        if direction == "long":
            up_usd, down_usd = fav_usd, -adv_usd
        else:
            up_usd, down_usd = -adv_usd, fav_usd
        up_ticks = up_usd / TICK_VALUE
        down_ticks = down_usd / TICK_VALUE
        high = entry_price + up_ticks * MINTICK
        low = entry_price - down_ticks * MINTICK
        close = float(cur["Price USD"])
        bars.append({
            "time": prev["Date and time"],
            "open": entry_price,
            "high": max(high, entry_price, close),
            "low": min(low, entry_price, close),
            "close": close,
        })
    return bars


def validate(bars):
    n = len(bars)
    degenerate = sum(1 for b in bars if b["open"] == b["high"] == b["low"] == b["close"])
    ranges_ticks = sorted((b["high"] - b["low"]) / MINTICK for b in bars)
    median_range = ranges_ticks[n // 2]
    bracket_violations = sum(
        1 for b in bars
        if b["high"] < max(b["open"], b["close"]) - 1e-12
        or b["low"] > min(b["open"], b["close"]) + 1e-12
    )
    print(f"n_bars={n}")
    print(f"degenerate_frac={degenerate / n:.4f}")
    print(f"median_range_ticks={median_range:.2f}")
    print(f"bracket_violations={bracket_violations}")
    # magnitude guard (memory's own warning: a one-sided bracket assert is vacuous
    # against a units bug -- pair with a plausible-magnitude check)
    max_range_ticks = ranges_ticks[-1]
    print(f"max_range_ticks={max_range_ticks:.1f} (sanity ceiling: 6J daily range rarely exceeds ~400 ticks)")
    if bracket_violations:
        raise AssertionError(f"{bracket_violations} bracket violations -- recovery is broken")
    if max_range_ticks > 2000:
        raise AssertionError(f"max single-bar range {max_range_ticks:.0f} ticks is implausible -- likely a units bug")


if __name__ == "__main__":
    entries = load_entries()
    print(f"n_entries={len(entries)}", file=sys.stderr)
    bars = recover(entries)
    validate(bars)
    with open(OUT_PATH, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["time", "open", "high", "low", "close"])
        for b in bars:
            w.writerow([b["time"], b["open"], b["high"], b["low"], b["close"]])
    print(f"wrote {len(bars)} bars -> {OUT_PATH}")
