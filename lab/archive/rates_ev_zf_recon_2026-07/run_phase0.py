"""RATES-EV-ZF-1 Phase-0 delta-extraction -- native ZF, CPI+NFP-conditioned ORB.

Scoping brief: docs/briefs/rnd-pipeline/RATES-EV-ZF-1-conditional-event-breakout-scoping.md
K=0 delta-extraction MEASUREMENT (not a registered search). The ORB-MNQ-1/ORB-ZB-1
construct (OR breakout, both sides, stop=opposite extreme, exit-at-close), reused
VERBATIM via orb_lib.orb_backtest/session_panel, but (a) OR-anchored at the 08:30 ET
CPI/NFP release instead of the 09:30 ET equity cash open, and (b) day-filtered to
the pre-committed, primary-BLS-sourced event calendar (build_calendar.py) instead of
every session -- the one untested cell in the program's rates-event 2x2 (brief §1).

Phase-0 battery (brief §3), gate order P0.1 -> P0.2/P0.4/P0.5 (P0.3 informational):
  P0.1 event-day range geometry vs ZB's unconditional 4.3:1 (instrument-choice thesis)
  P0.2 PRIMARY cost-law (Req 5): full CPI+NFP cohort, gross edge/cost >= 4.0x
  P0.3 SECONDARY (disclosed, non-gating): high-OR-range subcohort only
  P0.4 Req-4 power: Phi(sqrt(N)*|mean_R/std_R| - 1.96) >= 0.50, on the PRIMARY gross R
  P0.5 decorrelation pre-flight (Stage-8 ADR): rho vs the $273 c1 book, ZERO-PADDED
       on non-event days (this construct is sparse -- ~180 event-days/yr, not every
       day like ORB-ZB-1 -- so the honest daily-$-std must reflect near-zero variance
       on the ~93% of days with no position, not std(R) on event-days alone).
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

from build_calendar import events  # noqa: E402

ET = "America/New_York"
CACHE_ZF = Path.home() / ".databento_cache" / "ohlcv-1m_continuous_3af3c763cfcedd61.dbn"

# --- ZF economics. CBOT 5Y T-Note. face=$100,000; point=$1,000; tick=1/4 of 1/32
# = 0.0078125 pt = $7.8125 (WebSearch-cross-verified two independent sources, §0).
ZF_POINT_USD = 1000.0
ZF_TICK_PT = 0.25 / 32.0            # 0.0078125 pt
ZF_TICK_USD = ZF_TICK_PT * ZF_POINT_USD   # $7.8125
COMM_PER_SIDE = 0.61                 # Bulenox convention (program-standard reference)
RT_HEADLINE_PT = 2 * (COMM_PER_SIDE + ZF_TICK_USD) / ZF_POINT_USD   # 2x(0.61+7.8125)/1000
RT_COMMONLY_PT = 2 * COMM_PER_SIDE / ZF_POINT_USD                   # commission-only floor

# Event-day OR anchor: 08:30 ET (CPI/NFP release), 2 bars (08:30-09:00), breakout
# entries 09:00->close. Treasury futures pit session closes 15:00 ET -- exit there
# (clears the 16:00 ET E1 deadline with an hour to spare, per brief §0).
OPEN_TOD_EVENT = 8 * 60 + 30
CLOSE_TOD_EVENT = 15 * 60

BOOK_DAILY_STD_USD = 273.0     # c1 2-leg MYM+MNQ daily-$std @ $100K (Q-COMPOSE-1 / Stage-8 ADR)
REF_WEIGHT = 0.0037            # 0.37% -- same reference weight as ORB-ZB-1, apples-to-apples
ACCT_USD = 100_000.0

# ZB's own unconditional geometry (this morning's run, RESULTS.md) -- the bar
# this candidate's P0.1 instrument-choice thesis must clear.
ZB_UNCONDITIONAL_RATIO = 4.3


def zf_inst(rt_cost_pt: float) -> ol.Instrument:
    return ol.Instrument(
        name="ZF_event", path=Path("(in-memory)"), loader="none", feed="databento",
        tick=ZF_TICK_PT, spread_pt=ZF_TICK_PT, rt_cost_pt=rt_cost_pt,
        open_tod=OPEN_TOD_EVENT, close_tod=CLOSE_TOD_EVENT, tz=ET,
        note="native ZF.v.0 1m->15m; 5Y T-Note; OR anchored 08:30 ET release")


ZF = zf_inst(RT_HEADLINE_PT)
ZF_GROSS = zf_inst(0.0)
_PANEL_CACHE = Path(__file__).resolve().parent / "_zf_15m.pkl"


def load_zf_15m() -> pd.DataFrame:
    if _PANEL_CACHE.exists() and _PANEL_CACHE.stat().st_mtime >= CACHE_ZF.stat().st_mtime:
        return pd.read_pickle(_PANEL_CACHE)
    raw = db.DBNStore.from_file(CACHE_ZF).to_df()
    raw.index = raw.index.tz_convert(ET)
    med = float(raw["close"].median())
    assert 90 < med < 130, f"unexpected ZF median close {med:.2f} -- wrong cache?"
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
    print(f"[data] decoded ZF.v.0 median_close={med:.2f}")
    return out


def cost_law(bt_gross: dict, rt_pt: float, label: str) -> dict:
    """Verbatim convention from ORB-ZB-1/ORB-MNQ-1 run_phase0.py cost_law()."""
    R = np.asarray(bt_gross["R"], float)
    rng = np.asarray(bt_gross["range"], float)
    keep = np.isfinite(R) & np.isfinite(rng) & (rng > 0)
    R, rng = R[keep], rng[keep]
    n = len(R)
    cost_R = rt_pt / rng
    mean_edge = float(R.mean()) if n else float("nan")
    mean_cost = float(cost_R.mean()) if n else float("nan")
    hurdle = 4.0 * mean_cost
    sd = R.std(ddof=1) if n > 1 else 0.0
    t = mean_edge / (sd / np.sqrt(n)) if sd > 0 else 0.0
    return dict(label=label, n=n, mean_gross_R=mean_edge, t_gross=float(t),
                median_range_pt=float(np.median(rng)) if n else float("nan"),
                mean_cost_R=mean_cost, hurdle_4x=hurdle,
                ratio=(mean_edge / mean_cost) if (mean_cost and mean_cost > 0) else float("nan"),
                PASS=bool(n and mean_edge >= hurdle))


def power(mean_R: float, std_R: float, n: int) -> float:
    """Frozen Req-4 formula: power = Phi(sqrt(N)*|delta/sigma| - 1.96)."""
    from scipy.stats import norm
    if n == 0 or std_R == 0 or np.isnan(std_R):
        return float("nan")
    z = np.sqrt(n) * abs(mean_R / std_R) - 1.96
    return float(norm.cdf(z))


def main():
    print("=" * 80)
    print("RATES-EV-ZF-1 Phase-0 -- native ZF.v.0, CPI+NFP-conditioned event-anchored ORB")
    print("=" * 80)
    df = load_zf_15m()
    print(f"[data] 15m bars={len(df):,}  span={df['et'].min()} -> {df['et'].max()}  "
          f"days={df['d'].nunique():,}")
    print(f"[econ] ZF tick={ZF_TICK_PT:.7f} pt (${ZF_TICK_USD:.4f}); "
          f"RT headline={RT_HEADLINE_PT:.7f} pt (${RT_HEADLINE_PT*ZF_POINT_USD:.2f}); "
          f"RT 0-slip={RT_COMMONLY_PT:.7f} pt (${RT_COMMONLY_PT*ZF_POINT_USD:.2f})")

    ev = events()
    all_event_days = sorted(set(ev["NFP"]) | set(ev["CPI"]))
    event_days_dt = pd.to_datetime(all_event_days).date
    print(f"[calendar] NFP={len(ev['NFP'])} CPI={len(ev['CPI'])} "
          f"union={len(all_event_days)} events, primary-BLS-sourced (build_calendar.py)")

    piv_all, meta_all = ol.session_panel(df, ZF)
    panel_days = set(meta_all.index)
    event_days_in_panel = sorted(set(event_days_dt) & panel_days)
    missing = sorted(set(event_days_dt) - panel_days)
    print(f"[calendar] {len(event_days_in_panel)}/{len(all_event_days)} event days present "
          f"in the ZF panel ({len(missing)} missing -- holidays/no-session/pre-panel-start)")

    def slice_days(days):
        idx = pd.Index(days)
        p = {f: piv_all[f].loc[piv_all[f].index.isin(idx)] for f in piv_all}
        m = meta_all.loc[meta_all.index.isin(idx)]
        return p, m

    piv_ev, meta_ev = slice_days(event_days_in_panel)

    # ---- P0.1 event-day range geometry ----
    print("\n--- P0.1 EVENT-DAY RANGE GEOMETRY (instrument-choice thesis) ---")
    gross_ev = ol.orb_backtest(piv_ev, meta_ev, ZF_GROSS, or_bars=2)
    rng_ev = np.asarray(gross_ev["range"], float)
    rng_ev = rng_ev[np.isfinite(rng_ev) & (rng_ev > 0)]
    median_rng_ev = float(np.median(rng_ev)) if len(rng_ev) else float("nan")
    ratio_headline = median_rng_ev / RT_HEADLINE_PT if median_rng_ev else float("nan")
    print(f"  n event-day breakouts formed = {len(rng_ev)}")
    print(f"  median event-day OR range = {median_rng_ev:.5f} pt "
          f"(= {median_rng_ev/ZF_TICK_PT:.1f} ticks)")
    print(f"  median-range/RT-headline ratio = {ratio_headline:.2f}:1  "
          f"(ZB unconditional benchmark = {ZB_UNCONDITIONAL_RATIO}:1)")
    p01_pass = ratio_headline > ZB_UNCONDITIONAL_RATIO
    print(f"  >>> P0.1: {'PASS (better geometry than ZB)' if p01_pass else 'FAIL (not better than ZB)'}")

    # ---- P0.2 PRIMARY cost-law + P0.4 power (full CPI+NFP cohort) ----
    print("\n--- P0.2 PRIMARY COST-LAW + P0.4 POWER (full CPI+NFP cohort) ---")
    net_ev = ol.orb_backtest(piv_ev, meta_ev, ZF, or_bars=2)
    cl_h = cost_law(gross_ev, RT_HEADLINE_PT, "PRIMARY headline")
    cl_0 = cost_law(gross_ev, RT_COMMONLY_PT, "PRIMARY 0-slip")
    s_net = ol.summ(net_ev["R"], net_ev["year"])
    R_gross = np.asarray(gross_ev["R"], float)
    R_gross = R_gross[np.isfinite(R_gross)]
    pw = power(float(R_gross.mean()), float(R_gross.std(ddof=1)), len(R_gross))
    print(f"  n={cl_h['n']}")
    print(f"  mean GROSS edge = {cl_h['mean_gross_R']:+.4f} R  (t={cl_h['t_gross']:+.2f})")
    print(f"  HEADLINE cost_R={cl_h['mean_cost_R']:.4f}  4x hurdle={cl_h['hurdle_4x']:.4f}  "
          f"ratio={cl_h['ratio']:.2f}x  -> {'PASS' if cl_h['PASS'] else 'KILL'}")
    print(f"  0-SLIP   cost_R={cl_0['mean_cost_R']:.4f}  4x hurdle={cl_0['hurdle_4x']:.4f}  "
          f"ratio={cl_0['ratio']:.2f}x  -> {'PASS' if cl_0['PASS'] else 'KILL'}")
    print(f"  net-of-cost(headline) meanR={s_net['mean_R']:+.4f} (t={s_net['t']:+.2f}) "
          f"WR={s_net['wr']:.3f} PF={s_net['pf']:.3f}")
    print(f"  P0.4 power (Req-4, N={len(R_gross)}) = {pw:.4f}  "
          f"(bar >= 0.50) -> {'PASS' if pw >= 0.50 else 'FAIL'}")

    # ---- SANITY: within-day OR-window placebo (2nd R.2-style check) ----
    print("\n--- structural placebo (within-day OR window, event days only) ---")
    obs = float(net_ev["R"].mean()) if len(net_ev["R"]) else float("nan")
    if len(meta_ev) >= 10:
        plc = ol.placebo_within_day(piv_ev, meta_ev, ZF, obs, or_bars=2, nperm=1000)
        print(f"  obs meanR={obs:+.4f}  placebo p={plc['p']:.4f}  "
              f"placebo_mean={plc['placebo_mean']:+.4f} p95={plc['placebo_p95']:+.4f} "
              f"parity_ok={plc['parity_ok']}")
    else:
        print("  skipped -- too few event days for a stable permutation")

    # ---- P0.3 SECONDARY (informational, top-half OR-range subcohort) ----
    print("\n--- P0.3 SECONDARY (informational; top-half by OR range, NEVER gating) ---")
    med_rng_all = np.median(rng_ev) if len(rng_ev) else float("nan")
    rng_by_day = pd.Series(gross_ev["range"], index=[d for d in meta_ev.index
                            if d in meta_ev.index][:len(gross_ev["range"])]) \
        if len(gross_ev["range"]) == len(meta_ev) else None
    # robust re-derivation: recompute per-day range directly from piv (order-preserving)
    or_hi = piv_ev["high"].iloc[:, :2].max(axis=1)
    or_lo = piv_ev["low"].iloc[:, :2].min(axis=1)
    day_range = (or_hi - or_lo).dropna()
    top_half_days = day_range[day_range >= day_range.median()].index.tolist()
    piv_top, meta_top = slice_days(top_half_days)
    gross_top = ol.orb_backtest(piv_top, meta_top, ZF_GROSS, or_bars=2)
    net_top = ol.orb_backtest(piv_top, meta_top, ZF, or_bars=2)
    cl_top = cost_law(gross_top, RT_HEADLINE_PT, "SECONDARY top-half-range")
    s_top = ol.summ(net_top["R"], net_top["year"])
    print(f"  n={cl_top['n']} (top-half by realized OR range)")
    print(f"  mean GROSS edge = {cl_top['mean_gross_R']:+.4f} R (t={cl_top['t_gross']:+.2f})  "
          f"ratio={cl_top['ratio']:.2f}x -> {'PASS' if cl_top['PASS'] else 'KILL'}")
    print(f"  net-of-cost meanR={s_top['mean_R']:+.4f} (t={s_top['t']:+.2f}) PF={s_top['pf']:.3f}")

    # ---- per-year net (event days only) ----
    print("\n--- per-year net meanR (event days only) ---")
    s_all = ol.summ(net_ev["R"], net_ev["year"])
    for y in sorted(s_all["by_year"]):
        print(f"  {y}: {s_all['by_year'][y]:+.4f}")

    # ---- P0.5 decorrelation pre-flight (Stage-8 ADR; zero-padded daily series) ----
    print("\n--- P0.5 DECORRELATION PRE-FLIGHT (rho; zero-padded on non-event days) ---")
    R_net_ev = np.asarray(net_ev["R"], float)
    R_net_ev = R_net_ev[np.isfinite(R_net_ev)]
    n_trading_days_total = df["d"].nunique()
    n_event_trades = len(R_net_ev)
    daily_pnl_pct = np.zeros(n_trading_days_total)
    daily_pnl_pct[:n_event_trades] = R_net_ev * REF_WEIGHT
    daily_std_pct = float(np.std(daily_pnl_pct, ddof=1))
    zf_daily_std_usd = daily_std_pct * ACCT_USD
    rho = zf_daily_std_usd / BOOK_DAILY_STD_USD
    print(f"  event trades={n_event_trades}  total calendar trading days in panel={n_trading_days_total}")
    print(f"  net R std (event days only) = {R_net_ev.std(ddof=1):.3f}")
    print(f"  zero-padded daily-$std @ {REF_WEIGHT*100:.2f}%/$100K = ${zf_daily_std_usd:.2f}")
    print(f"  rho = ${zf_daily_std_usd:.2f} / ${BOOK_DAILY_STD_USD:.0f} = {rho:.3f}  "
          f"({'<1.0 OK' if rho < 1.0 else '>=1.0 presumptive-reject'})")
    print("  NOTE: unlike ORB-ZB-1 (in-market every day), this construct is sparse "
          f"({n_event_trades}/{n_trading_days_total} = {n_event_trades/n_trading_days_total*100:.1f}% "
          "of days) -- the zero-padded daily series (not std(R) alone) is the honest input;"
          " n_eff_risk_delta itself still needs the aligned c1 leg series (data-gated, same"
          " owed item as ORB-MNQ-1's Stage-8).")

    # ---- verdict ----
    print("\n" + "=" * 80)
    print("PHASE-0 VERDICT (gate order: P0.1 geometry -> P0.2/P0.4/P0.5)")
    print(f"  P0.1 geometry  : {ratio_headline:.2f}:1 vs ZB {ZB_UNCONDITIONAL_RATIO}:1 "
          f"-> {'better' if p01_pass else 'NOT better'}")
    print(f"  P0.2 cost-law  : headline {cl_h['ratio']:.2f}x (bar 4.0x) -> "
          f"{'PASS' if cl_h['PASS'] else 'KILL'}")
    print(f"  P0.4 power     : {pw:.4f} (bar 0.50) -> {'PASS' if pw >= 0.50 else 'FAIL'}")
    print(f"  P0.5 rho       : {rho:.3f} (bar <1.0) -> {'PASS' if rho < 1.0 else 'FAIL'}")
    all_pass = p01_pass and cl_h["PASS"] and pw >= 0.50 and rho < 1.0
    print(f"  -> {'RESOLVED (graduate to Phase-1)' if all_pass else 'FALSIFIED (close on the failing limb(s) above)'}")
    print("=" * 80)


if __name__ == "__main__":
    main()
