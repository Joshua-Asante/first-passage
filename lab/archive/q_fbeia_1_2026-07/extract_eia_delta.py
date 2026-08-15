"""F-B — CL EIA post-release UNCONDITIONAL δ-extraction (K=1).

Databento-authorized own-cohort δ (operator GO 2026-07-20, F-B completed on
request after F-A cost-wall + F-C effect-absent). Data: CL.c.0 ohlcv-1m,
GLBX.MDP3, IS era 2010-06-06→2018-12-31 (est + billed $0.00). Manifest:
fb_eia_cl_reversal (register_search open, K=1).

THE F-B QUESTION (Q-INVENTORY): the published EIA effect (Rousse-Sévi 2019
≈25bp) is CONDITIONAL on the inventory surprise — an informed-flow input
(R2's class). Is there an UNCONDITIONAL post-release edge tradeable WITHOUT
the surprise number? If not, F-B is informed-flow and dies.

PRE-COMMITTED before any return is read (this file authored before results):
  - Event set: EIA Weekly Petroleum Status Report ≈ Wednesday 10:30 ET,
    shifted to Thursday when a US federal holiday falls Mon–Wed of that week.
    2010-06→2018-12. (Residual mis-dating dilutes toward zero — conservative.)
  - PRIMARY expression (REVERSAL, dealer-inventory/overreaction prior):
        m0 = CL log-return 10:30→10:35 ET (immediate release reaction)
        trade = fade: position -sign(m0), entered 10:35, held to 10:50 (15m)
        δ = mean( -sign(m0) · ret[10:35→10:50] ) in bp.
    Conditions ONLY on realized price (m0), never on the EIA number/surprise
    ⇒ unconditional in the sense that matters. (Continuation = −δ, same test.)
  - SANITY (reported, not the verdict): unconditional directional long
    10:30→10:45 — should be ≈0 by surprise symmetry.
  - Gates: Req-4 power δ/σ ≥ 0.122 ; Req-5 cost-law |δ| ≥ 4×RT_frac.
    CL RT: tick $0.01 ≈ 1.43 bp at price ~70; single-RT ≈ 1.5–2 bp → 4× ≈ 6–8 bp;
    two-RT ≈ 2.5–3 bp → 4× ≈ 10–12 bp. Both reported.
  - K=1 (one pre-committed reversal expression).
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
import databento as db
from pandas.tseries.holiday import USFederalHolidayCalendar

HERE = Path(__file__).resolve().parent
CACHE = Path.home() / ".databento_cache"
ET = "America/New_York"


def eia_events(start="2010-06-06", end="2018-12-31") -> pd.DatetimeIndex:
    cal = USFederalHolidayCalendar()
    hols = set(cal.holidays(start="2010-01-01", end="2019-06-01").normalize())
    weds = pd.date_range(start, end, freq="W-WED")
    events = []
    for w in weds:
        # week Mon..Wed
        mon = w - pd.Timedelta(days=2)
        wk_mon_wed = {mon, mon + pd.Timedelta(days=1), w}
        day = w if not (wk_mon_wed & hols) else w + pd.Timedelta(days=1)  # shift to Thu
        events.append(pd.Timestamp(f"{day.date()} 10:30", tz=ET).tz_convert("UTC"))
    return pd.DatetimeIndex(events)


def load_cl_1m() -> pd.Series:
    # newest 1m continuous cache that contains CL.c.0
    caches = sorted(CACHE.glob("ohlcv-1m_continuous_*.dbn"), key=lambda p: p.stat().st_mtime, reverse=True)
    for p in caches:
        d = db.DBNStore.from_file(str(p)).to_df()
        if any(str(s).startswith("CL") for s in d["symbol"].unique()):
            d = d[d["symbol"].astype(str).str.startswith("CL")]
            idx = pd.to_datetime(d.index if isinstance(d.index, pd.DatetimeIndex) else d["ts_event"], utc=True)
            s = pd.Series(d["close"].to_numpy(float), index=idx).sort_index()
            s = s[~s.index.duplicated(keep="last")]
            print(f"CL 1m from {p.name}: {len(s):,} bars  {s.index.min()} → {s.index.max()}")
            return s
    raise SystemExit("no CL 1m cache found")


def px_at(s: pd.Series, ts: pd.Timestamp, tol_min=3):
    i = s.index.searchsorted(ts)
    if i >= len(s):
        return None
    if (s.index[i] - ts) > pd.Timedelta(minutes=tol_min):
        return None
    return float(s.iloc[i])


def main():
    s = load_cl_1m()
    events = eia_events()
    print(f"EIA events: {len(events)} (Wed 10:30 ET, Thu-shifted on holidays)")

    rows = []
    for t in events:
        p_1030 = px_at(s, t)
        p_1035 = px_at(s, t + pd.Timedelta(minutes=5))
        p_1050 = px_at(s, t + pd.Timedelta(minutes=20))
        p_1045 = px_at(s, t + pd.Timedelta(minutes=15))
        if not all([p_1030, p_1035, p_1050, p_1045]) or min(p_1030, p_1035) <= 0:
            continue
        m0 = np.log(p_1035 / p_1030)                       # release reaction
        m1 = np.log(p_1050 / p_1035)                       # subsequent 15m
        rev = -np.sign(m0) * m1                             # fade the reaction
        long_uncond = np.log(p_1045 / p_1030)              # sanity: long 10:30->10:45
        rows.append({"date": str(t.date()), "m0_bp": m0*1e4, "rev_ret_bp": rev*1e4,
                     "long_uncond_bp": long_uncond*1e4})
    df = pd.DataFrame(rows)
    df.to_csv(HERE / "eia_events.csv", index=False)

    def summ(x):
        x = np.asarray(x, float); n = len(x)
        mean = float(np.mean(x)); sd = float(np.std(x, ddof=1))
        return n, mean, sd, (mean/sd if sd else float("nan")), (mean/sd*np.sqrt(n) if sd else float("nan"))

    n, rmean, rsd, rdsig, rt = summ(df["rev_ret_bp"])
    _, lmean, lsd, ldsig, lt = summ(df["long_uncond_bp"])
    _, m0mean, m0sd, *_ = summ(df["m0_bp"].abs())

    print(f"\n=== F-B unconditional post-EIA (CL, N={n}) ===")
    print(f"|m0| mean release reaction (10:30→10:35) = {m0mean:.1f}bp (sanity: EIA moves are large)")
    print(f"PRIMARY reversal (fade m0, 10:35→10:50): δ={rmean:.2f}bp  σ={rsd:.0f}bp  δ/σ={rdsig:.4f}  t={rt:.2f}")
    print(f"SANITY uncond long (10:30→10:45):        δ={lmean:.2f}bp  δ/σ={ldsig:.4f}  t={lt:.2f}  (expect ~0)")

    req4 = abs(rdsig) >= 0.122
    hurdle = (6.0, 10.0)
    req5_lo = abs(rmean) >= hurdle[0]; req5_hi = abs(rmean) >= hurdle[1]
    print(f"\nReq-4 power (|δ/σ| ≥ 0.122): {'PASS' if req4 else 'FAIL'}")
    print(f"Req-5 cost-law (|δ| ≥ 4×RT): vs 6bp {'PASS' if req5_lo else 'FAIL'} | vs 10bp {'PASS' if req5_hi else 'FAIL'}")
    verdict = "SCREEN-PASS" if (req4 and req5_lo) else "SCREEN-FAIL"
    print(f"SCREEN: {verdict}")

    out = {"manifest": "fb_eia_cl_reversal", "K": 1, "N": n,
           "release_reaction_abs_bp": round(m0mean, 1),
           "reversal": {"delta_bp": round(rmean, 3), "sigma_bp": round(rsd, 1),
                        "delta_over_sigma": round(rdsig, 4), "t": round(rt, 2)},
           "uncond_long_sanity": {"delta_bp": round(lmean, 3), "t": round(lt, 2)},
           "req4_power": req4, "req5_vs6bp": req5_lo, "req5_vs10bp": req5_hi,
           "cost_hurdle_bp": list(hurdle), "verdict": verdict}
    json.dump(out, open(HERE / "eia_results.json", "w"), indent=2)
    print(f"\nwrote eia_results.json")


if __name__ == "__main__":
    main()
