#!/usr/bin/env python3
"""Free-data 2022-rates era-split falsifier for the micro-rates intraday-MR chop-native leg.

Closes the TOP-SCORED candidate of the 2026-06-30 chop-native 5th-leg sweep (micro-rates /
STIR mean-reversion on CME Micro 10Y/2YY yield futures). See RESULTS.md for the full sweep.

PRE-REGISTERED (frozen before scoring; the kill rule was fixed before the data was scored):
  Data    : Yahoo ^TNX (10Y CMT yield) primary; ^FVX (5Y) robustness. Daily, 2010-2026.
            (FRED DGS10/DGS2 and Stooq were the first-choice sources but BOTH were egress-blocked
            in the run environment -- FRED reset the connection, Stooq served a JS challenge --
            so Yahoo's v8 chart JSON was used. ^TNX/^FVX here are quoted as the yield in % directly.)
  Proxy   : daily proxy for a 15m intraday fade. Tests the REGIME / tail-co-occurrence mechanism
            (the disqualifier), NOT the precise intraday edge magnitude. A fade bleeds in a trend at
            EVERY timescale, so the regime read transfers; the bp/trade does not.
  Fade    : z_t = (y_t - SMA_n(y))/SD_n(y) over trailing n incl. t (no look-ahead).
            On |z_t|>=thr, fade -> next-day position on YIELD = -sign(z_t).
            Primary metric: daily MR equity. pnl_{t+1} = pos_t * (y_{t+1}-y_t) in bp.
            Canonical: n=20, thr=1.0. Robustness grid reported, NOT optimized over.
  Eras    : PRE 2010-2019 | H1 2020-01-01..2023-03-20 (chop half, contains 2022) |
            H2 2023-03-21..end | + per-year.
  KILL if : (K1) worst-loss year/era in H1 (esp 2022) -> bleeds when the book co-draws;
            (K2) non-positive PRE-2020 but positive only post-2020 (the ORB era-relabel pattern).
  SURVIVE : positive AND era-stable (PRE>0 AND H1>0) AND losses not concentrated in 2022/H1.

VERDICT (2026-06-30): FALSIFIED. K1 fires -- worst year 2022 (10Y -124bp / 5Y -116bp), H1 net-negative
both tenors (Sharpe -0.31 / -0.47). K2 does not fire but the PRE-2020 edge is economically zero
(Sharpe +0.22 / +0.31, mean ~+0.07 bp/day) -- no standalone edge to insert, let alone PF~2.0.

Reproduce:
  # fetch (egress required; the script will fetch if the JSON is missing):
  #   curl -sS -A Mozilla/5.0 "https://query1.finance.yahoo.com/v8/finance/chart/%5ETNX?period1=1262304000&period2=1783000000&interval=1d" -o TNX.json
  #   curl -sS -A Mozilla/5.0 "https://query1.finance.yahoo.com/v8/finance/chart/%5EFVX?period1=1262304000&period2=1783000000&interval=1d" -o FVX.json
  python rates_era_split.py
"""
import json, math, os, ssl, urllib.request, datetime as dt

YF = "https://query1.finance.yahoo.com/v8/finance/chart/{sym}?period1=1262304000&period2=1783000000&interval=1d"


def fetch_if_missing(path, yahoo_symbol):
    """Best-effort fetch of the Yahoo chart JSON. Egress may be blocked; then drop the file in by hand."""
    if os.path.exists(path):
        return
    url = YF.format(sym=yahoo_symbol)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=60, context=ssl.create_default_context()).read()
        open(path, "wb").write(data)
    except Exception as e:  # noqa: BLE001
        raise SystemExit(f"could not fetch {path} ({e!r}); fetch it manually -- see the module docstring")


def load_yahoo(path):
    d = json.load(open(path))
    r = d["chart"]["result"][0]
    ts, cl = r["timestamp"], r["indicators"]["quote"][0]["close"]
    seen = {}
    for t, c in zip(ts, cl):
        if c is None:
            continue
        seen[dt.datetime.fromtimestamp(t, dt.timezone.utc).date()] = c   # yield in % (^TNX/^FVX direct)
    days = sorted(seen)
    return days, [seen[x] for x in days]


def sma_sd(window):
    m = sum(window) / len(window)
    v = sum((w - m) ** 2 for w in window) / len(window)
    return m, math.sqrt(v)


def fade_daily(days, y, n=20, thr=1.0):
    """Daily MR fade equity. Returns [(date, pnl_bp)] for each marked day."""
    recs = []
    for i in range(n, len(y) - 1):
        win = y[i - n + 1:i + 1]            # trailing n incl. i, no look-ahead
        m, sd = sma_sd(win)
        if sd == 0:
            continue
        z = (y[i] - m) / sd
        pos = -1 if z >= thr else (1 if z <= -thr else 0)   # fade toward the mean
        dy = (y[i + 1] - y[i]) * 100.0      # next-day yield change in bp
        recs.append((days[i + 1], pos * dy))
    return recs


def agg(recs, lo=None, hi=None):
    sel = [p for (dd, p) in recs if (lo is None or dd >= lo) and (hi is None or dd <= hi)]
    active = [p for p in sel if p != 0.0]
    if not active:
        return dict(n=0, total=0.0, mean=0.0, hit=float("nan"), sharpe=float("nan"))
    tot = sum(active)
    mean = tot / len(active)
    sd = math.sqrt(sum((p - mean) ** 2 for p in active) / len(active)) if len(active) > 1 else 0.0
    sharpe = (mean / sd * math.sqrt(252)) if sd > 0 else float("nan")
    hit = 100.0 * sum(1 for p in active if p > 0) / len(active)
    return dict(n=len(active), total=tot, mean=mean, hit=hit, sharpe=sharpe)


def regime(days, y, y0, y1):
    seg = [(d, v) for d, v in zip(days, y) if y0 <= d <= y1]
    vs = [v for _, v in seg]
    return dict(start=seg[0][1], end=seg[-1][1], lo=min(vs), hi=max(vs), net=seg[-1][1] - seg[0][1])


def run(tag, path):
    days, y = load_yahoo(path)
    print(f"\n{'='*78}\n{tag}: {days[0]} -> {days[-1]}  ({len(y)} daily obs)")
    r22 = regime(days, y, dt.date(2022, 1, 1), dt.date(2022, 12, 31))
    print(f"  2022 {tag} yield: start {r22['start']:.2f}% -> end {r22['end']:.2f}%  "
          f"(min {r22['lo']:.2f} / max {r22['hi']:.2f}, net {r22['net']:+.2f}pp)  <- one-directional uptrend check")
    recs = fade_daily(days, y, n=20, thr=1.0)
    H1A, H1B = dt.date(2020, 1, 1), dt.date(2023, 3, 20)
    eras = [("PRE  2010-2019", dt.date(2010, 1, 1), dt.date(2019, 12, 31)),
            ("H1   2020-03/23", H1A, H1B),
            ("H2   2023+      ", dt.date(2023, 3, 21), dt.date(2030, 1, 1))]
    print("  --- CANONICAL fade n=20 thr=1.0 (daily MR equity, bp) ---")
    print(f"  {'era':16} {'n':>5} {'total_bp':>10} {'mean_bp':>9} {'hit%':>6} {'sharpe':>7}")
    for name, lo, hi in eras:
        a = agg(recs, lo, hi)
        print(f"  {name:16} {a['n']:5d} {a['total']:10.0f} {a['mean']:9.3f} {a['hit']:6.1f} {a['sharpe']:7.2f}")
    print("  --- per-year ---")
    print(f"  {'year':6} {'n':>5} {'total_bp':>10} {'mean_bp':>9} {'hit%':>6}")
    worst = (None, 1e9)
    for yr in range(2010, 2027):
        a = agg(recs, dt.date(yr, 1, 1), dt.date(yr, 12, 31))
        if a['n'] == 0:
            continue
        if a['total'] < worst[1]:
            worst = (yr, a['total'])
        print(f"  {yr:6} {a['n']:5d} {a['total']:10.0f} {a['mean']:9.3f} {a['hit']:6.1f}")
    print(f"  >> WORST YEAR (lowest total fade P&L): {worst[0]}  ({worst[1]:.0f} bp)")
    print("  --- robustness grid: PRE / H1 / 2022 total_bp (sign-stability, NOT optimized over) ---")
    print(f"  {'n,thr':16} {'PRE':>8} {'H1':>8} {'2022':>8}")
    for nn in (10, 20, 40):
        for th in (0.5, 1.0, 1.5):
            rr = fade_daily(days, y, n=nn, thr=th)
            pre = agg(rr, dt.date(2010, 1, 1), dt.date(2019, 12, 31))['total']
            h1 = agg(rr, H1A, H1B)['total']
            t22 = agg(rr, dt.date(2022, 1, 1), dt.date(2022, 12, 31))['total']
            print(f"  n={nn:<2} thr={th:<3}     {pre:8.0f} {h1:8.0f} {t22:8.0f}")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for name, sym in (("TNX.json", "%5ETNX"), ("FVX.json", "%5EFVX")):
        fetch_if_missing(os.path.join(here, name), sym)
    run("10Y ^TNX", os.path.join(here, "TNX.json"))
    run("5Y  ^FVX", os.path.join(here, "FVX.json"))
