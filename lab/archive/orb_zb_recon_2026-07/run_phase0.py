"""ORB-ZB-1 Phase-0 δ-extraction + cheap-falsifier battery — native ZB, frozen NAS100-ORB-30.

Scoping brief: docs/briefs/rnd-pipeline/ORB-ZB-1-risk-off-decorrelated-breakout-scoping.md
This is a K=0 δ-extraction MEASUREMENT (not a registered search). Single fixed ORB-30
construct transplanted VERBATIM from ORB-MNQ-1 (lab/analysis/orb_mnq_2026-07/run_stage2.py)
to ZB. Reuses lab/analysis/orb_universe_2026-06-22/orb_lib.py orb_backtest engine verbatim
(N5/N7 fill-fragility scars — no re-invention).

Phase-0 battery (brief §3), cheapest-decisive first:
  P0.1 cost-law reachability (Req 5): mean gross edge_R >= 4x mean cost_R. THE dominant kill.
  P0.3 tail-timing: per-year net; worst DD must NOT concentrate in the 2020-22 book window.
  P0.2 decorrelation pre-flight: rho = ZB-ORB daily-$std / c1-book daily-$std ($273 = the
       2-leg MYM+MNQ book, Q-COMPOSE-1 / Stage-8 ADR 2026-07-20). risk-N_eff-delta is the
       binding gate but needs the aligned c1 leg series (data-gated — same gate ORB-MNQ hit).
Verdict gates on P0.1 first: a cost-law KILL closes FALSIFIED and P0.2/P0.3 are informational.
"""
from __future__ import annotations

import sys
from pathlib import Path

import databento as db
import numpy as np
import pandas as pd

ORB_LIB_DIR = Path(__file__).resolve().parents[1] / "orb_universe_2026-06-22"
sys.path.insert(0, str(ORB_LIB_DIR))
import orb_lib as ol  # noqa: E402

ET = "America/New_York"
CACHE_DIR = Path.home() / ".databento_cache"

# --- ZB economics. CBOT 30Y T-bond future. point=$1,000; tick=1/32 pt = 0.03125 pt = $31.25.
ZB_POINT_USD = 1000.0
ZB_TICK_PT = 1.0 / 32.0
ZB_TICK_USD = ZB_TICK_PT * ZB_POINT_USD            # $31.25
COMM_PER_SIDE = 0.61                                # Bulenox (ORB-MNQ headline basis)
# RT (headline, ORB-MNQ-equivalent convention): 2 x (comm + 1-tick slip). The 1-tick slip is
# large in $ for ZB's coarse tick — that IS the cost geometry the gate exists to catch.
RT_HEADLINE_PT = 2 * (COMM_PER_SIDE + ZB_TICK_USD) / ZB_POINT_USD    # 0.06372 pt
# RT (optimistic lower bound, deep-liquidity 0-slip): commission only.
RT_COMMONLY_PT = 2 * COMM_PER_SIDE / ZB_POINT_USD                    # 0.00122 pt

BOOK_DAILY_STD_USD = 273.0      # c1 2-leg MYM+MNQ daily-$std @ $100K (Q-COMPOSE-1 / Stage-8 ADR)
REF_WEIGHT = 0.0037             # 0.37% — ORB-MNQ's compose weight (apples-to-apples for rho)
ACCT_USD = 100_000.0


def zb_inst(rt_cost_pt: float) -> ol.Instrument:
    return ol.Instrument(
        name="ZB_native", path=Path("(in-memory)"), loader="none", feed="databento",
        tick=ZB_TICK_PT, spread_pt=ZB_TICK_PT, rt_cost_pt=rt_cost_pt,
        open_tod=ol.OPEN_TOD_US, close_tod=ol.CLOSE_TOD_US, tz=ET,
        note="native ZB.v.0 1m->15m; 30Y T-bond; Bulenox $0.61/side")


ZB = zb_inst(RT_HEADLINE_PT)
ZB_GROSS = zb_inst(0.0)
_PANEL_CACHE = Path(__file__).resolve().parent / "_zb_15m.pkl"


def find_zb_cache() -> tuple[Path, float]:
    """Newest continuous 1m DBN whose median price is bond-like (ZB ~100-180),
    distinguishing it from the MNQ cache (~15,000)."""
    cands = sorted(CACHE_DIR.glob("ohlcv-1m_continuous_*.dbn"),
                   key=lambda p: p.stat().st_mtime, reverse=True)
    for p in cands:
        try:
            med = float(db.DBNStore.from_file(p).to_df()["close"].median())
            if 50 < med < 200:
                return p, med
        except Exception:
            continue
    raise FileNotFoundError("no bond-priced continuous 1m DBN in cache — run the ZB pull first")


def load_zb_15m() -> pd.DataFrame:
    src, med = find_zb_cache()
    if _PANEL_CACHE.exists() and _PANEL_CACHE.stat().st_mtime >= src.stat().st_mtime:
        out = pd.read_pickle(_PANEL_CACHE)
        print(f"[data] cached panel {_PANEL_CACHE.name} (src {src.name}, median_close {med:.2f})")
        return out
    raw = db.DBNStore.from_file(src).to_df()
    raw.index = raw.index.tz_convert(ET)
    o = raw["open"].resample("15min", label="left", closed="left").first()
    h = raw["high"].resample("15min", label="left", closed="left").max()
    lo = raw["low"].resample("15min", label="left", closed="left").min()
    cl = raw["close"].resample("15min", label="left", closed="left").last()
    v = raw["volume"].resample("15min", label="left", closed="left").sum()
    bars = pd.DataFrame({"open": o, "high": h, "low": lo, "close": cl, "volume": v}) \
        .dropna(subset=["open", "high", "low", "close"])
    epoch_ms = bars.index.tz_convert("UTC").view("int64") // 1_000_000
    dfp = pd.DataFrame({
        "epoch": np.asarray(epoch_ms, dtype="int64"),
        "open": bars["open"].to_numpy(), "high": bars["high"].to_numpy(),
        "low": bars["low"].to_numpy(), "close": bars["close"].to_numpy(),
        "volume": bars["volume"].to_numpy().astype("int64"),
    })
    out = ol._finalize(dfp)
    try:
        out.to_pickle(_PANEL_CACHE)
    except Exception:
        pass
    print(f"[data] decoded src={src.name} median_close={med:.2f}")
    return out


def cost_law(bt_gross: dict, rt_pt: float, label: str) -> dict:
    """VERBATIM from lab/analysis/orb_mnq_2026-07/run_stage2.py — the ORB-MNQ Stage-2 gate."""
    R = np.asarray(bt_gross["R"], float)
    rng = np.asarray(bt_gross["range"], float)
    keep = np.isfinite(R) & np.isfinite(rng) & (rng > 0)
    R, rng = R[keep], rng[keep]
    n = len(R)
    cost_R = rt_pt / rng
    mean_edge = float(R.mean())
    mean_cost = float(cost_R.mean())
    hurdle = 4.0 * mean_cost
    sd = R.std(ddof=1) if n > 1 else 0.0
    t = mean_edge / (sd / np.sqrt(n)) if sd > 0 else 0.0
    return dict(label=label, n=n, mean_gross_R=mean_edge, t_gross=float(t),
                median_range_pt=float(np.median(rng)), mean_cost_R=mean_cost, hurdle_4x=hurdle,
                ratio=(mean_edge / mean_cost) if mean_cost > 0 else float("inf"),
                PASS=bool(mean_edge >= hurdle))


def main():
    print("=" * 80)
    print("ORB-ZB-1 Phase-0 — native ZB.v.0, frozen NAS100-ORB-30 construct (K=0 δ-extraction)")
    print("=" * 80)
    df = load_zb_15m()
    print(f"[data] 15m bars={len(df):,}  span={df['et'].min()} -> {df['et'].max()}  "
          f"days={df['d'].nunique():,}")
    print(f"[econ] ZB tick={ZB_TICK_PT:.5f} pt (${ZB_TICK_USD:.2f}); "
          f"RT headline={RT_HEADLINE_PT:.5f} pt (${RT_HEADLINE_PT*ZB_POINT_USD:.2f}); "
          f"RT 0-slip={RT_COMMONLY_PT:.5f} pt (${RT_COMMONLY_PT*ZB_POINT_USD:.2f})")

    piv_all, meta_all = ol.session_panel(df, ZB)

    def windows(y0=None, y1=None):
        if y0 is None:
            return piv_all, meta_all
        yr = meta_all["year"]
        days = meta_all.index[(yr >= y0) & (yr <= (y1 or 9999))]
        return {f: piv_all[f].loc[days] for f in piv_all}, meta_all.loc[days]

    # ---- P0.1 cost-law (dominant gate) ----
    print("\n--- P0.1 COST-LAW (gate: mean gross edge_R >= 4x mean cost_R) ---")
    p01 = {}
    for tag, y0, y1 in [("FULL 2019-05..present", None, None),
                        ("2021+ (regime window)", 2021, None),
                        ("2019 only", 2019, 2019), ("2020 only", 2020, 2020)]:
        p, m = windows(y0, y1)
        gross = ol.orb_backtest(p, m, ZB_GROSS, or_bars=2)
        cl_h = cost_law(gross, RT_HEADLINE_PT, tag)
        cl_0 = cost_law(gross, RT_COMMONLY_PT, tag)
        net = ol.orb_backtest(p, m, ZB, or_bars=2)
        sn = ol.summ(net["R"], net["year"])
        p01[tag] = (cl_h, cl_0, sn)
        print(f"\n[{tag}]  n={cl_h['n']}  median OR range={cl_h['median_range_pt']:.4f} pt "
              f"(= {cl_h['median_range_pt']/ZB_TICK_PT:.1f} ticks)")
        print(f"  mean GROSS edge = {cl_h['mean_gross_R']:+.4f} R  (t={cl_h['t_gross']:+.2f})")
        print(f"  HEADLINE  cost_R={cl_h['mean_cost_R']:.4f}  4x hurdle={cl_h['hurdle_4x']:.4f}  "
              f"ratio={cl_h['ratio']:.2f}x  -> {'PASS' if cl_h['PASS'] else 'KILL'}")
        print(f"  0-SLIP    cost_R={cl_0['mean_cost_R']:.4f}  4x hurdle={cl_0['hurdle_4x']:.4f}  "
              f"ratio={cl_0['ratio']:.2f}x  -> {'PASS' if cl_0['PASS'] else 'KILL'}")
        print(f"  net-of-cost(headline) meanR={sn['mean_R']:+.4f} (t={sn['t']:+.2f}) "
              f"WR={sn['wr']:.3f} PF={sn['pf']:.3f}")

    # ---- structural: within-day OR-window placebo (is the opening range special?) ----
    print("\n--- structural placebo (within-day OR window; is 09:30 OR special?) ---")
    p, m = windows(2021, None)
    net21 = ol.orb_backtest(p, m, ZB, or_bars=2)
    obs = float(net21["R"].mean())
    plc = ol.placebo_within_day(p, m, ZB, obs, or_bars=2, nperm=1000)
    print(f"  2021+ obs meanR={obs:+.4f}  placebo p={plc['p']:.4f}  "
          f"placebo_mean={plc['placebo_mean']:+.4f} p95={plc['placebo_p95']:+.4f} "
          f"parity_ok={plc['parity_ok']}")

    # ---- P0.3 tail-timing (per-year net; worst years vs the 2020-22 book window) ----
    print("\n--- P0.3 TAIL-TIMING (per-year net meanR; worst-DD must avoid 2020-22) ---")
    gross_all = ol.orb_backtest(piv_all, meta_all, ZB_GROSS, or_bars=2)
    net_all = ol.orb_backtest(piv_all, meta_all, ZB, or_bars=2)
    s = ol.summ(net_all["R"], net_all["year"])
    for y in sorted(s["by_year"]):
        print(f"  {y}: {s['by_year'][y]:+.4f}")
    worst = min(s["by_year"], key=s["by_year"].get) if s["by_year"] else None
    print(f"  worst year = {worst} ({s['by_year'].get(worst):+.4f})  "
          f"[book co-draw window = 2020-2022]")

    # ---- P0.2 decorrelation pre-flight (rho; risk-N_eff-delta data-gated) ----
    print("\n--- P0.2 DECORRELATION PRE-FLIGHT (rho vs the $273 c1 book) ---")
    R = np.asarray(net_all["R"], float)
    R = R[np.isfinite(R)]
    std_R = float(R.std(ddof=1))
    zb_daily_std_ref = std_R * REF_WEIGHT * ACCT_USD
    rho_ref = zb_daily_std_ref / BOOK_DAILY_STD_USD
    w_star = BOOK_DAILY_STD_USD / (std_R * ACCT_USD)   # weight giving rho = 1.0
    print(f"  ORB R std = {std_R:.3f}  (~1 trade/day, so per-trade = per-day)")
    print(f"  @ {REF_WEIGHT*100:.2f}% ($100K): ZB-ORB daily-$std = ${zb_daily_std_ref:.0f}  "
          f"-> rho = {rho_ref:.2f}  ({'>=1 presumptive-reject' if rho_ref>=1 else '<1 ok'})")
    print(f"  weight giving rho=1.0 (max non-variance-dominant weight) = {w_star*100:.3f}%")
    print("  NOTE: rho at a fixed weight is ~instrument-invariant (R is OR-normalized), so it")
    print("        is a WEIGHT lever, not the ZB-vs-MNQ decorrelation discriminator. The binding")
    print("        Stage-8 statistic (n_eff_risk_delta) needs the aligned MYM/MNQ leg series")
    print("        (data-gated — the same Stage-8 gate ORB-MNQ-1 left owed).")

    # ---- verdict (gates on P0.1 first) ----
    full_h = p01["FULL 2019-05..present"][0]
    full_0 = p01["FULL 2019-05..present"][1]
    r21_h = p01["2021+ (regime window)"][0]
    print("\n" + "=" * 80)
    print("PHASE-0 VERDICT (gate order: P0.1 cost-law first)")
    print(f"  P0.1 full-window : headline {full_h['ratio']:.2f}x / 0-slip {full_0['ratio']:.2f}x "
          f"(bar 4.0x) -> {'PASS' if full_h['PASS'] else 'KILL'} (headline)")
    print(f"  P0.1 2021+       : headline {r21_h['ratio']:.2f}x -> "
          f"{'PASS' if r21_h['PASS'] else 'KILL'}")
    if full_h["PASS"] or r21_h["PASS"]:
        print("  -> P0.1 PASSES a window; P0.2/P0.3 are decision-binding (see above).")
    else:
        print("  -> P0.1 KILL on every window; ORB-ZB-1 closes FALSIFIED on cost-law.")
        print("     P0.2/P0.3 above are informational only (moot once the edge is sub-cost).")
    print("=" * 80)


if __name__ == "__main__":
    main()
