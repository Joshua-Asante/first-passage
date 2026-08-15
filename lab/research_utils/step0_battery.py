#!/usr/bin/env python3
"""step0_battery.py — mandatory panel-integrity checks before any backtest metrics.

Usage:
  python step0_battery.py <csv> --timeframe 15 --session 09:30-13:45 \
      --days Tue [--event-dates boc_dates.txt] [--n-bounds 60 120] \
      [--expected-span 2020-01-01 2026-06-01 --span-cover-frac 0.80] \
      [--store runs.json] [--label cfg10] [--tz America/New_York]

Exit codes: 0 = pass (warnings allowed), 2 = hard fail (do NOT compute metrics).
Provenance: 2026-06-11 session — caught wrong-TF, duplicate export, mislabeled subset.
Check 8 (date-span coverage) folded in from the Guardian filter-sweep hardening
(lab/analysis/guardian_filter_sweep_2026-06-20/step0_battery.py, 2026-06-21) — an
isolation export that doesn't actually span the period it claims to silently breaks
any downstream stationarity split (selection_tests.py halves).
"""
import argparse, json, os, sys
import pandas as pd

DAY_MAP = {'Mon':'Monday','Tue':'Tuesday','Wed':'Wednesday','Thu':'Thursday','Fri':'Friday'}

def load(csv):
    df = pd.read_csv(csv, encoding='utf-8-sig')
    df.columns = [c.strip() for c in df.columns]
    ren = {}
    for c in df.columns:
        if c.startswith('Trade number'): ren[c] = 'Trade #'
        if c.startswith('Net PnL'): ren[c] = 'Net P&L'      # USD or CAD suffix
        if c.startswith('Price'): ren[c] = 'Price'
    df = df.rename(columns=ren)
    df['Date and time'] = pd.to_datetime(df['Date and time'])
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csv')
    ap.add_argument('--timeframe', type=int, default=15, help='bar minutes')
    ap.add_argument('--session', default=None, help='HH:MM-HH:MM in --tz (entry exec window)')
    ap.add_argument('--days', nargs='*', default=None, help='allowed entry days, e.g. Mon Tue Wed')
    ap.add_argument('--event-dates', default=None, help='file of YYYYMMDD ints; entries on these = fail')
    ap.add_argument('--n-bounds', nargs=2, type=int, default=None)
    ap.add_argument('--expected-span', nargs=2, default=None, metavar=('START', 'END'),
                     help='YYYY-MM-DD YYYY-MM-DD full period this panel should cover '
                          '(catches a time-clustered/isolation export mislabeled as the full-period panel)')
    ap.add_argument('--span-cover-frac', type=float, default=0.80,
                     help='min fraction of --expected-span the panel must cover (default 0.80)')
    ap.add_argument('--store', default=None, help='json of prior runs for duplicate detection')
    ap.add_argument('--label', default=None)
    ap.add_argument('--tz', default='America/New_York')
    a = ap.parse_args()

    df = load(a.csv)
    en = df[df['Type'].str.startswith('Entry')].copy()
    ex = df[df['Type'].str.startswith('Exit')].copy()
    hard, warn = [], []

    # (1) timeframe via entry-minute census
    mins = sorted(en['Date and time'].dt.minute.unique())
    if a.timeframe < 60 and mins == [0]:
        hard.append(f"All entries at :00 — inconsistent with {a.timeframe}m chart (wrong timeframe?)")
    bad_min = [m for m in mins if m % a.timeframe != 0]
    if bad_min:
        hard.append(f"Entry minutes {bad_min} not multiples of {a.timeframe}")

    # (2) session window (assumes export timestamps are UTC; TV standard)
    et = en['Date and time'].dt.tz_localize('UTC').dt.tz_convert(a.tz)
    if a.session:
        s, e = a.session.split('-')
        lo = int(s.split(':')[0])*60 + int(s.split(':')[1])
        hi = int(e.split(':')[0])*60 + int(e.split(':')[1])
        bm = et.dt.hour*60 + et.dt.minute
        out = ((bm < lo) | (bm > hi)).sum()
        if out: hard.append(f"{out} entries outside session {a.session} {a.tz} (TZ misalignment or wrong window)")

    # (3) day-of-week census
    if a.days:
        allowed = {DAY_MAP.get(d, d) for d in a.days}
        seen = set(et.dt.day_name().unique())
        extra = seen - allowed
        if extra: hard.append(f"Entries on disallowed days {sorted(extra)} (expected {sorted(allowed)}) — mislabel/misconfig")

    # (4) event-day leak
    if a.event_dates and os.path.exists(a.event_dates):
        evset = {int(l.strip()) for l in open(a.event_dates) if l.strip()}
        ymd = et.dt.year*10000 + et.dt.month*100 + et.dt.day
        leak = ymd.isin(evset).sum()
        if leak: hard.append(f"{leak} entries on blocked event dates")

    # (5) n bounds
    n = len(ex)
    if a.n_bounds and not (a.n_bounds[0] <= n <= a.n_bounds[1]):
        warn.append(f"n={n} outside expected [{a.n_bounds[0]},{a.n_bounds[1]}]")

    # (8) date-span coverage — an isolation export that doesn't actually cover the
    # period it claims to silently breaks any downstream stationarity split (a
    # time-clustered subset masquerading as the full panel).
    if a.expected_span and len(en):
        exp_start, exp_end = pd.Timestamp(a.expected_span[0]), pd.Timestamp(a.expected_span[1])
        exp_secs = (exp_end - exp_start).total_seconds()
        p_start, p_end = en['Date and time'].min(), en['Date and time'].max()
        cover = max(0.0, (min(p_end, exp_end) - max(p_start, exp_start)).total_seconds())
        frac = cover / exp_secs if exp_secs > 0 else 0.0
        if frac < a.span_cover_frac:
            hard.append(
                f"panel covers only {frac:.0%} of expected span "
                f"[{exp_start.date()}..{exp_end.date()}] (panel spans "
                f"[{p_start.date()}..{p_end.date()}]) — time-clustered/isolation "
                "export? a stationarity split (selection_tests.py halves) on this "
                "panel would not test what it claims to"
            )

    # (6) duplicate detection vs store
    net = round(float(ex.filter(like='Net P&L').iloc[:,0].sum()))
    if a.store and os.path.exists(a.store):
        prior = json.load(open(a.store))
        for p in prior:
            if p.get('n') == n and p.get('net') == net and p.get('label') != a.label:
                hard.append(f"Exact n/net match with prior run '{p.get('label')}' — duplicate export?")

    # (7) fingerprint tag in filename
    if a.label and a.label.lower() not in os.path.basename(a.csv).lower():
        warn.append(f"Label '{a.label}' not found in filename (fingerprint convention)")

    print(f"STEP-0: {a.csv}  n={n} net={net}  entries={len(en)}")
    for h in hard: print(f"  FAIL  {h}")
    for w in warn: print(f"  warn  {w}")
    if not hard and not warn: print("  clean")
    sys.exit(2 if hard else 0)

if __name__ == '__main__':
    main()
