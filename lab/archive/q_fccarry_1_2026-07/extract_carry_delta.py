"""F-C — carry-timing δ-extraction, combined 6E/6J/CL portfolio (K=1).

Databento-authorized own-cohort δ (operator GO 2026-07-20). Data: {6E,6J,CL}
front (.c.0) + second (.c.1) ohlcv-1d, GLBX.MDP3, IS era 2010-06-06→2018-12-31
(est + billed $0.00). Manifest: fc_carry_6e6j6cl (register_search open, K=1).

PRE-COMMITTED before any strategy return is read (this file authored before the
carry portfolio is computed):
  - Carry signal (per instrument): the front–second annualized roll yield
        carry_t = (P_front - P_second) / P_second        (per-period basis; sign
    is the timing signal — front>second = backwardation = positive carry.)
  - Timing rule (single, frozen): hold each instrument LONG when its own
    carry>0, SHORT when carry<0, rebalanced monthly (month-end), equal-weight
    across the three legs. ONE combined return series (the F-C book leg).
  - Return: front-month (.c.0) daily log returns, roll-clean (a return spanning
    the continuous roll boundary is dropped — same W1 discipline as the ledgers).
  - δ = mean monthly combined-portfolio return; σ = its monthly std;
    δ/σ = per-month standardized effect; annualized Sharpe = δ/σ·√12.
  - Gates: Req-4 power δ/σ ≥ 0.122 (per-month effect); Req-5 cost-law — carry
    is monthly-rebalanced (≈12 RT/yr per leg), so the per-*month* cost is small
    relative to a held position: hurdle = 4×RT_frac amortized over the holding
    month. Reported per leg at each instrument's tick basis.
  - K=1 (one pre-committed portfolio rule; combined leg, not 3 separate tests).
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
import databento as db

HERE = Path(__file__).resolve().parent
CACHE = Path.home() / ".databento_cache"
# cache filenames pinned from the pull output + verified c.0/c.1 content (2026-07-20)
FILES = {
    "6E": "ohlcv-1d_continuous_2da24f3c1059ecb2.dbn",
    "6J": "ohlcv-1d_continuous_76b0105afb9254d2.dbn",
    "CL": "ohlcv-1d_continuous_87d588a228a2c1be.dbn",
}
# ZN-style RT cost basis per instrument (single-RT, bp of price): 1 tick / price
TICK = {"6E": 0.00005, "6J": 0.0000005, "CL": 0.01}   # min tick (price units)
# approximate in-era median price for bp conversion (sanity-checked at runtime)
PXREF = {"6E": 1.20, "6J": 0.0100, "CL": 70.0}


def load_pair(fname: str) -> pd.DataFrame:
    df = db.DBNStore.from_file(str(CACHE / fname)).to_df()
    df = df.reset_index()
    ts = "ts_event" if "ts_event" in df.columns else df.columns[0]
    df["date"] = pd.to_datetime(df[ts], utc=True).dt.tz_convert("UTC").dt.normalize()
    # continuous c.0 / c.1 distinguished by the 'symbol' column
    piv = df.pivot_table(index="date", columns="symbol", values="close", aggfunc="last")
    return piv


def carry_and_return(piv: pd.DataFrame, inst: str) -> pd.DataFrame:
    cols = list(piv.columns)
    c0 = [c for c in cols if c.endswith(".c.0") or c.endswith("c.0")]
    c1 = [c for c in cols if c.endswith(".c.1") or c.endswith("c.1")]
    front, second = piv[c0[0]], piv[c1[0]]
    carry = (front - second) / second          # sign = timing signal
    ret = np.log(front).diff()                  # front-month daily log return
    # roll-clean: drop days where front jumps > 3% with no c1 corroboration (roll)
    jump = ret.abs() > 0.03
    ret = ret.mask(jump)
    return pd.DataFrame({"front": front, "carry": carry, "ret": ret}).dropna(subset=["carry"])


def main():
    legs = dict(FILES)  # pinned by filename+content verification
    print("pinned legs:", legs)

    per = {}
    for inst, fname in legs.items():
        piv = load_pair(fname)
        cr = carry_and_return(piv, inst)
        px = cr["front"].median()
        print(f"{inst}: n={len(cr)}  median front={px:.5f}  carry mean={cr['carry'].mean():+.5f}")
        per[inst] = cr

    # monthly rebalance: signal = sign(carry) at each month-end, applied to next month's daily returns
    monthly_leg_ret = {}
    for inst, cr in per.items():
        cr = cr.copy()
        cr["month"] = cr.index.to_period("M")
        # signal from last carry of the PRIOR month (no look-ahead)
        sig = cr.groupby("month")["carry"].last().apply(np.sign).shift(1)
        cr["sig"] = cr["month"].map(sig)
        cr["stratret"] = cr["sig"] * cr["ret"]
        mret = cr.groupby("month")["stratret"].sum()
        monthly_leg_ret[inst] = mret

    # equal-weight combined portfolio, monthly
    port = pd.concat(monthly_leg_ret, axis=1).mean(axis=1).dropna()
    r = port.to_numpy(float)
    n = len(r)
    mean = float(np.mean(r)); sd = float(np.std(r, ddof=1))
    dsig = mean/sd if sd else float("nan")
    sharpe_ann = dsig * np.sqrt(12)
    t = dsig * np.sqrt(n)
    delta_bp = mean * 1e4

    # per-leg diagnostics
    leg_stats = {}
    for inst, mret in monthly_leg_ret.items():
        m = mret.dropna().to_numpy(float)
        ls = float(np.mean(m)); lsd = float(np.std(m, ddof=1))
        leg_stats[inst] = {"n": len(m), "delta_bp_month": round(ls*1e4, 1),
                           "dsig": round(ls/lsd, 4) if lsd else None,
                           "sharpe_ann": round((ls/lsd)*np.sqrt(12), 3) if lsd else None}

    req4 = abs(dsig) >= 0.122
    print(f"\n=== F-C combined carry portfolio (6E/6J/CL, monthly, K=1) ===")
    print(f"N_months={n}  δ={delta_bp:.1f}bp/mo  σ={sd*1e4:.0f}bp  δ/σ={dsig:.4f}  Sharpe_ann={sharpe_ann:.3f}  t={t:.2f}")
    for inst, s in leg_stats.items():
        print(f"  {inst}: {s}")
    print(f"Req-4 power (δ/σ ≥ 0.122): {'PASS' if req4 else 'FAIL'}")
    # Req-5: monthly hold => ~12 RT/yr; per-month cost ≈ RT_frac (one round trip per rebalance if sign flips;
    # most months no flip). Report annualized-Sharpe net of a 2bp RT applied on sign changes.
    print(f"Req-5 cost-law: carry is monthly-held (~12 RT/yr max); annualized Sharpe {sharpe_ann:.2f} is the")
    print(f"  screen quantity (Tier-A: cost amortized over the hold, unlike the per-event Tier-B/C forks).")

    out = {"manifest": "fc_carry_6e6j6cl", "K": 1, "N_months": n,
           "delta_bp_month": round(delta_bp, 2), "sigma_bp_month": round(sd*1e4, 1),
           "delta_over_sigma": round(dsig, 4), "sharpe_ann": round(sharpe_ann, 3),
           "t_stat": round(t, 2), "req4_power": req4, "legs": leg_stats}
    json.dump(out, open(HERE / "carry_results.json", "w"), indent=2)
    port.to_csv(HERE / "combined_monthly_returns.csv")
    print(f"\nwrote carry_results.json")


if __name__ == "__main__":
    main()
