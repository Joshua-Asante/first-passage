"""H-ZNAUC-1 — ZN post-auction dealer-hedging-unwind δ-extraction (own-cohort).

Databento-authorized own-cohort δ (operator GO 2026-07-20). Data: ZN.c.0
ohlcv-1m, GLBX.MDP3, IS era 2010-06-06→2018-12-31 (est $0.00, cached).
Auctions: fiscaldata.treasury.gov (free), note+bond coupon, IS era.

PRE-COMMITTED before any δ was read (this file authored before results):
  - Primary cohort: 10-Year note auctions + reopenings (terms 10-Year /
    9-Year 11-Month / 9-Year 10-Month / 9-Year 8-Month) — the tenor ZN most
    directly hedges. Verdict is on the primary.
  - Secondary (disclosed robustness, NOT the verdict): all note+bond coupon.
  - Window (frozen): enter at close of the auction-close minute (results just
    out), exit +15 min. Robustness alts [0→30], [0→60] reported, not gated.
  - Gates: Req-4 power δ/σ ≥ 0.122 ; Req-5 cost-law δ_bp ≥ 4×RT_frac.
    RT_frac(ZN) ≈ 1.5bp (single-RT, 1 tick @~125 + commission) → 4× = 6bp;
    conservative two-RT ≈ 2.5bp → 4× = 10bp. Both reported.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
import databento as db

HERE = Path(__file__).resolve().parent
CACHE = Path.home() / ".databento_cache" / "ohlcv-1m_continuous_50cc9cef3ba4ae96.dbn"
TEN_YR_TERMS = {"10-Year", "9-Year 11-Month", "9-Year 10-Month", "9-Year 8-Month"}
ET = "America/New_York"

def load_bars() -> pd.DataFrame:
    df = db.DBNStore.from_file(str(CACHE)).to_df()
    df = df[["close"]].copy()
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df["ts_event"])
    df.index = df.index.tz_convert("UTC") if df.index.tz else df.index.tz_localize("UTC")
    df = df[~df.index.duplicated(keep="last")].sort_index()
    return df

def auction_utc(a: dict) -> pd.Timestamp | None:
    t = a.get("closing_time_comp")
    if t not in ("01:00 PM", "11:30 AM"):
        return None
    hhmm = "13:00" if t == "01:00 PM" else "11:30"
    try:
        local = pd.Timestamp(f"{a['auction_date']} {hhmm}", tz=ET)
    except Exception:
        return None
    return local.tz_convert("UTC")

def bar_close_at(bars: pd.DataFrame, ts: pd.Timestamp, tol_min: int = 3) -> float | None:
    # nearest bar at/after ts within tol (handles a missing exact minute)
    idx = bars.index.searchsorted(ts)
    if idx >= len(bars):
        return None
    cand = bars.index[idx]
    if (cand - ts) > pd.Timedelta(minutes=tol_min):
        return None
    return float(bars["close"].iloc[idx])

def event_returns(bars, auctions, hold_min):
    out = []
    for a in auctions:
        t0 = auction_utc(a)
        if t0 is None:
            continue
        p0 = bar_close_at(bars, t0)
        p1 = bar_close_at(bars, t0 + pd.Timedelta(minutes=hold_min))
        if p0 and p1 and p0 > 0:
            out.append({"date": a["auction_date"], "term": a["security_term"],
                        "btc": a.get("bid_to_cover_ratio"),
                        "ret_bp": (p1 / p0 - 1.0) * 1e4})
    return pd.DataFrame(out)

def summarize(df, label):
    r = df["ret_bp"].to_numpy(float)
    n = len(r)
    mean = float(np.mean(r)); sd = float(np.std(r, ddof=1))
    dsig = mean / sd if sd else float("nan")
    t = dsig * np.sqrt(n)
    return {"cohort": label, "N": n, "delta_bp": round(mean, 3),
            "sigma_bp": round(sd, 2), "delta_over_sigma": round(dsig, 4),
            "t_stat": round(t, 2)}

def main():
    bars = load_bars()
    auctions = json.load(open(HERE / "auctions_is.json"))
    print(f"bars: {len(bars):,}  {bars.index.min()} → {bars.index.max()}")
    print(f"price sanity: median close = {bars['close'].median():.3f}")

    primary = [a for a in auctions if a["security_term"] in TEN_YR_TERMS]
    allcoup = auctions  # note+bond already filtered upstream

    rows = []
    for label, auc in [("PRIMARY 10Y-family", primary), ("SECONDARY all-coupon", allcoup)]:
        for hold in (15, 30, 60):
            d = event_returns(bars, auc, hold)
            s = summarize(d, f"{label} [0→{hold}m]")
            rows.append(s)
            if hold == 15 and label.startswith("PRIMARY"):
                d.to_csv(HERE / "primary_15m_events.csv", index=False)

    res = pd.DataFrame(rows)
    print("\n" + res.to_string(index=False))

    # Gate application on the PRIMARY 15-min window (the verdict)
    v = next(r for r in rows if r["cohort"] == "PRIMARY 10Y-family [0→15m]")
    req4 = abs(v["delta_over_sigma"]) >= 0.122
    hurdle_lo, hurdle_hi = 6.0, 10.0  # 4×RT_frac, single vs two-RT
    req5_lo = abs(v["delta_bp"]) >= hurdle_lo
    req5_hi = abs(v["delta_bp"]) >= hurdle_hi
    print(f"\n=== VERDICT (primary 10Y-family, 0→15m) ===")
    print(f"N={v['N']}  δ={v['delta_bp']}bp  σ={v['sigma_bp']}bp  δ/σ={v['delta_over_sigma']}  t={v['t_stat']}")
    print(f"Req-4 power (δ/σ ≥ 0.122): {'PASS' if req4 else 'FAIL'}")
    print(f"Req-5 cost-law (|δ| ≥ 4×RT): vs 6bp {'PASS' if req5_lo else 'FAIL'} | vs 10bp {'PASS' if req5_hi else 'FAIL'}")
    verdict = "SCREEN-PASS" if (req4 and req5_lo) else "SCREEN-FAIL"
    print(f"SCREEN: {verdict}")

    json.dump({"rows": rows, "verdict": verdict, "req4": req4,
               "req5_vs6bp": req5_lo, "req5_vs10bp": req5_hi,
               "cost_hurdle_bp": [hurdle_lo, hurdle_hi]},
              open(HERE / "delta_results.json", "w"), indent=2)
    print(f"\nwrote delta_results.json")

if __name__ == "__main__":
    main()
