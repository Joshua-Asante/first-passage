"""Measure per-leg hold durations from TV trade exports to test futures-prop EOD-flat compatibility.

Futures-prop firms force-flatten every position by EOD (no overnight/weekend carry) — established
universal across 6 firms in the Q-BTC-3 Phase-0 gate (docs/briefs/Q-BTC-3-closure-falsified.md).
Decisive metric: fraction of trades held past the entry calendar day (exit_date > entry_date),
plus weekend-spanning holds and max hold. A leg with material overnight holds cannot run as-is.

Inputs: the canonical Pepperstone TV exports in ~/Downloads (vendor-licensed, gitignored — same
source the 2026-06-21 decompound run used). Re-export if FileNotFound.
"""
import csv
from datetime import datetime, timedelta
from pathlib import Path

DL = Path.home() / "Downloads"

LEGS = {
    "Guardian (XAUUSD->MGC)": "Guardian_Gold_v5.5_PEPPERSTONE_XAUUSD_2026-06-26_561b8.csv",
    "Striker DJ30 (->MYM)":   "Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-06-28_43a29.csv",
    "Striker NAS100 (->MNQ)": "Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-06-27_92d79.csv",
    "Aegis USDJPY (OANDA fx)":"Aegis_USDJPY_v4.3_PEPPERSTONE_USDJPY_2026-06-26_02af2.csv",
}

def parse_dt(s):
    return datetime.strptime(s.strip(), "%Y-%m-%d %H:%M")

def analyze(path):
    entries, exits = {}, {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        cols = {c.lower().strip(): c for c in r.fieldnames}
        tn_c = cols.get("trade number") or cols.get("trade #") or cols.get("trade")
        ty_c = cols.get("type")
        dt_c = cols.get("date and time") or cols.get("date/time") or cols.get("date")
        for row in r:
            tn, ty, dt = row[tn_c].strip(), row[ty_c].strip().lower(), parse_dt(row[dt_c])
            if "entry" in ty: entries[tn] = dt
            elif "exit" in ty: exits[tn] = dt
    return [(entries[tn], exits[tn]) for tn in entries if tn in exits]

def weekend_spanned(e, x):
    d = e
    while d.date() <= x.date():
        if d.weekday() == 5: return True
        d += timedelta(days=1)
    return False

print(f"{'Leg':<26} {'N':>5} {'medHrs':>7} {'maxDays':>8} {'%>1day':>7} {'%wknd':>6}")
print("-" * 66)
for name, fn in LEGS.items():
    p = DL / fn
    if not p.exists():
        print(f"{name:<26} MISSING {fn}"); continue
    trades = analyze(p); n = len(trades)
    durs_hr = [(x-e).total_seconds()/3600 for e,x in trades]
    pct_on = 100*sum(1 for e,x in trades if x.date() > e.date())/n
    pct_wk = 100*sum(1 for e,x in trades if weekend_spanned(e,x))/n
    med = sorted(durs_hr)[n//2]; maxd = max(durs_hr)/24
    print(f"{name:<26} {n:>5} {med:>7.2f} {maxd:>8.2f} {pct_on:>6.1f}% {pct_wk:>5.1f}%")
