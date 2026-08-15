"""NG-EIA-1 Phase-0 delta-extraction -- native NG, POST-ONLY announcement bracket.

Scoping brief: docs/briefs/rnd-pipeline/NG-EIA-1-announcement-bracket-premium-scoping.md
K=0 delta-extraction MEASUREMENT (not a registered search). PRIMARY construct is
POST-ONLY (short ~10:25 ET blind entry ahead of the 10:30 ET EIA storage release,
cover 11:00 ET) -- corrected before this run from an earlier pre+post draft after the
brainstorm workflow's executioner verified the citable ~23bp/event net delta attaches
only to the post-window; the pre-leg is surprise-conditional (the F-B/CL-EIA trap).
Modeled directly on the F-B (extract_eia_delta.py) / H-ZNAUC-1 (extract_delta.py)
fixed-bracket pattern -- this is NOT an ORB breakout-with-stop, so orb_lib is not reused.

Battery (brief §3):
  P0.1 faithfulness anchor: |m0| 10:30->10:35 ET (proves correct event dating)
  P0.2 PRIMARY Req-4 power: delta/sigma on the 10:25->11:00 ET window
  P0.3 PRIMARY Req-5 cost-law: |delta|_bp >= 4x RT_frac(NG), single- and two-RT
  P0.4 MNG sizing sanity (informational)
  SANITY-1 (informational, NEVER gating): 09:30->11:00 ET (re-admits the surprise-
    conditional pre-leg) -- comparison only, diagnoses whether PRIMARY vs SANITY-1
    diverge in the direction the R1 sign-inversion concern would predict.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import databento as db
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_calendar import primary_thursdays, secondary_shifted  # noqa: E402

CACHE_NG = Path.home() / ".databento_cache" / "ohlcv-1m_continuous_718110b3fb16eece.dbn"
ET = "America/New_York"

# NG economics (CME public spec, WebSearch-cross-verified two sources, brief §0):
# 10,000 MMBtu contract, tick = $0.001/MMBtu = $10.00/tick. MNG micro = 1,000 MMBtu.
NG_TICK_USD = 10.00
MNG_TICK_USD = 1.00  # 1/10 contract size -> 1/10 tick value at the same $0.001 tick
COMM_PER_SIDE = 0.61  # Bulenox convention (program-standard reference)


def load_ng_1m() -> pd.Series:
    d = db.DBNStore.from_file(str(CACHE_NG)).to_df()
    idx = d.index if isinstance(d.index, pd.DatetimeIndex) else pd.to_datetime(d["ts_event"])
    idx = idx.tz_convert("UTC") if idx.tz else idx.tz_localize("UTC")
    s = pd.Series(d["close"].to_numpy(float), index=idx).sort_index()
    s = s[~s.index.duplicated(keep="last")]
    s = s.tz_convert(ET)
    print(f"NG 1m bars: {len(s):,}  {s.index.min()} -> {s.index.max()}  "
          f"median_close=${s.median():.3f}/MMBtu")
    assert 1.0 < s.median() < 12.0, "unexpected NG median price -- wrong cache?"
    return s


def px_at(s: pd.Series, ts: pd.Timestamp, tol_min: int = 3):
    i = s.index.searchsorted(ts)
    if i >= len(s):
        return None
    if (s.index[i] - ts) > pd.Timedelta(minutes=tol_min):
        return None
    return float(s.iloc[i])


def build_events(s: pd.Series, dates: list[str]) -> pd.DataFrame:
    """For each event date, pull the clock-time price checkpoints needed for every
    limb (P0.1 faithfulness, PRIMARY, SANITY-1) in one pass."""
    rows = []
    for d in dates:
        base = pd.Timestamp(f"{d} 00:00", tz=ET)
        checkpoints = {
            "p_0930": base + pd.Timedelta(hours=9, minutes=30),
            "p_1025": base + pd.Timedelta(hours=10, minutes=25),
            "p_1030": base + pd.Timedelta(hours=10, minutes=30),
            "p_1035": base + pd.Timedelta(hours=10, minutes=35),
            "p_1100": base + pd.Timedelta(hours=11, minutes=0),
        }
        px = {k: px_at(s, ts) for k, ts in checkpoints.items()}
        if any(v is None or v <= 0 for v in px.values()):
            continue
        rows.append({"date": d, **px})
    return pd.DataFrame(rows)


def summ(x: np.ndarray):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n == 0:
        return dict(n=0, mean=float("nan"), sd=float("nan"), dsig=float("nan"), t=float("nan"))
    mean = float(x.mean())
    sd = float(x.std(ddof=1)) if n > 1 else 0.0
    dsig = mean / sd if sd else float("nan")
    t = dsig * np.sqrt(n) if np.isfinite(dsig) else float("nan")
    return dict(n=n, mean=mean, sd=sd, dsig=dsig, t=t)


def cost_law_bp(delta_bp: float, rt_bp_single: float, rt_bp_two: float):
    hurdle_lo, hurdle_hi = 4 * rt_bp_single, 4 * rt_bp_two
    return dict(
        rt_single=rt_bp_single, rt_two=rt_bp_two,
        hurdle_lo=hurdle_lo, hurdle_hi=hurdle_hi,
        pass_lo=bool(abs(delta_bp) >= hurdle_lo),
        pass_hi=bool(abs(delta_bp) >= hurdle_hi),
    )


def main():
    print("=" * 80)
    print("NG-EIA-1 Phase-0 -- native NG.v.0, POST-ONLY announcement bracket (K=0)")
    print("=" * 80)
    s = load_ng_1m()

    primary_dates = primary_thursdays()
    secondary_dates = [d for d, _t in secondary_shifted()]
    print(f"\n[calendar] PRIMARY (holiday-ambiguous weeks dropped): {len(primary_dates)} events")
    print(f"[calendar] SECONDARY (best-effort shift, informational): {len(secondary_dates)} events")

    ev_primary = build_events(s, primary_dates)
    ev_secondary = build_events(s, secondary_dates)
    print(f"[calendar] PRIMARY events with clean price coverage: {len(ev_primary)}/{len(primary_dates)}")

    # returns, log-bp
    def logret_bp(p0, p1):
        return np.log(p1 / p0) * 1e4

    ev_primary = ev_primary.assign(
        m0_bp=logret_bp(ev_primary["p_1030"], ev_primary["p_1035"]),                 # P0.1
        primary_ret_bp=logret_bp(ev_primary["p_1025"], ev_primary["p_1100"]),        # PRIMARY: short 10:25->11:00
        sanity1_ret_bp=logret_bp(ev_primary["p_0930"], ev_primary["p_1100"]),        # SANITY-1: short 09:30->11:00
    )

    # ---- P0.1 faithfulness anchor ----
    print("\n--- P0.1 FAITHFULNESS ANCHOR (|m0| 10:30->10:35 ET) ---")
    m0_abs = ev_primary["m0_bp"].abs()
    print(f"  n={len(m0_abs)}  mean|m0|={m0_abs.mean():.2f}bp  median|m0|={m0_abs.median():.2f}bp  "
          f"(F-B/CL faithfulness anchor was 25.6bp; sanity threshold: non-trivial, non-zero)")
    p01_pass = m0_abs.mean() > 3.0  # a real reaction should clearly exceed typical 15m NG noise
    print(f"  >>> P0.1: {'PASS (dating looks correct)' if p01_pass else 'CONCERN -- near-zero reaction, check dating'}")

    # PRIMARY is a SHORT position: profit = -return (short profits when price falls)
    primary_short_pnl_bp = -ev_primary["primary_ret_bp"]
    sanity1_short_pnl_bp = -ev_primary["sanity1_ret_bp"]

    # ---- P0.2/P0.3 PRIMARY (post-only) ----
    print("\n--- P0.2/P0.3 PRIMARY (short 10:25 ET -> cover 11:00 ET, gross) ---")
    sp = summ(primary_short_pnl_bp.to_numpy())
    print(f"  n={sp['n']}  delta={sp['mean']:+.3f}bp  sigma={sp['sd']:.1f}bp  "
          f"delta/sigma={sp['dsig']:.4f}  t={sp['t']:+.2f}")
    req4_floor = 1.96 / np.sqrt(sp["n"]) if sp["n"] else float("nan")
    req4_pass = abs(sp["dsig"]) >= req4_floor if np.isfinite(sp["dsig"]) else False
    print(f"  Req-4 power floor (delta/sigma >= 1.96/sqrt(N) = {req4_floor:.4f}): "
          f"{'PASS' if req4_pass else 'FAIL'}")

    rt_single_bp = 2 * (COMM_PER_SIDE + NG_TICK_USD) / (s.iloc[-1] * 10_000) * 1e4  # RT in bp of notional
    rt_two_bp = rt_single_bp * 2
    # NG notional varies a lot over the panel (2019 ~$2.50 -> 2022 spikes ~$9) -- use the
    # panel MEDIAN price for a representative RT-in-bp (same convention as ZN/CL harnesses
    # using the in-era median price, not a single latest-tick snapshot).
    med_price = float(s.median())
    rt_single_bp = 2 * (COMM_PER_SIDE + NG_TICK_USD) / (med_price * 10_000) * 1e4
    rt_two_bp = rt_single_bp * 2
    cl = cost_law_bp(sp["mean"], rt_single_bp, rt_two_bp)
    print(f"  RT (single, @ median price ${med_price:.3f}) = {cl['rt_single']:.3f}bp -> "
          f"4x hurdle = {cl['hurdle_lo']:.3f}bp -> {'PASS' if cl['pass_lo'] else 'KILL'}")
    print(f"  RT (two-RT convention)                    = {cl['rt_two']:.3f}bp -> "
          f"4x hurdle = {cl['hurdle_hi']:.3f}bp -> {'PASS' if cl['pass_hi'] else 'KILL'}")

    # ---- P0.4 MNG sizing sanity (informational) ----
    print("\n--- P0.4 MNG SIZING SANITY (informational; same PRIMARY delta, MNG cost) ---")
    rt_single_mng_bp = 2 * (COMM_PER_SIDE + MNG_TICK_USD) / (med_price * 1_000) * 1e4  # 1/10 notional
    hurdle_mng = 4 * rt_single_mng_bp
    print(f"  MNG RT (single) = {rt_single_mng_bp:.3f}bp -> 4x hurdle = {hurdle_mng:.3f}bp -> "
          f"{'PASS' if abs(sp['mean']) >= hurdle_mng else 'FAIL (expected -- coarser relative cost)'}")

    # ---- SANITY-1 (informational, never gating) ----
    print("\n--- SANITY-1 (informational; short 09:30->11:00 ET, re-admits the conditional pre-leg) ---")
    s1 = summ(sanity1_short_pnl_bp.to_numpy())
    print(f"  n={s1['n']}  delta={s1['mean']:+.3f}bp  sigma={s1['sd']:.1f}bp  t={s1['t']:+.2f}")
    print(f"  PRIMARY vs SANITY-1 delta: {sp['mean']:+.3f}bp vs {s1['mean']:+.3f}bp "
          f"({'SANITY-1 larger -- consistent w/ pre-leg inflating the wider bracket' if abs(s1['mean']) > abs(sp['mean']) else 'PRIMARY comparable or larger'})")

    # ---- per-year decay diagnostic ----
    print("\n--- per-year PRIMARY delta (decay diagnostic) ---")
    ev_primary["year"] = pd.to_datetime(ev_primary["date"]).dt.year
    for y, grp in primary_short_pnl_bp.groupby(ev_primary["year"]):
        print(f"  {y}: n={len(grp)}  mean={grp.mean():+.3f}bp")

    # ---- verdict ----
    print("\n" + "=" * 80)
    print("PHASE-0 VERDICT (PRIMARY post-only construct)")
    print(f"  P0.1 faithfulness : {'clean' if p01_pass else 'CONCERN'}")
    print(f"  P0.2 power         : {'PASS' if req4_pass else 'FAIL'} (delta/sigma={sp['dsig']:.4f} vs floor {req4_floor:.4f})")
    print(f"  P0.3 cost-law      : headline {'PASS' if cl['pass_lo'] else 'KILL'} "
          f"({abs(sp['mean']):.3f}bp vs {cl['hurdle_lo']:.3f}bp hurdle)")
    graduate = p01_pass and req4_pass and cl["pass_lo"]
    print(f"  -> {'RESOLVED (graduate to Phase-1)' if graduate else 'FALSIFIED (close on the failing limb(s) above)'}")
    print("=" * 80)

    out = {
        "n_primary": int(sp["n"]), "delta_bp": float(sp["mean"]), "sigma_bp": float(sp["sd"]),
        "delta_over_sigma": float(sp["dsig"]), "t": float(sp["t"]), "req4_floor": float(req4_floor),
        "req4_pass": bool(req4_pass), "rt_single_bp": float(cl["rt_single"]),
        "hurdle_single_bp": float(cl["hurdle_lo"]),
        "req5_pass_single": bool(cl["pass_lo"]), "req5_pass_two_rt": bool(cl["pass_hi"]),
        "faithfulness_mean_abs_m0_bp": float(m0_abs.mean()),
        "sanity1_delta_bp": float(s1["mean"]), "sanity1_t": float(s1["t"]),
        "mng_hurdle_bp": float(hurdle_mng), "mng_pass": bool(abs(sp["mean"]) >= hurdle_mng),
        "verdict": "RESOLVED" if graduate else "FALSIFIED",
    }
    json.dump(out, open(HERE / "phase0_results.json", "w"), indent=2)
    ev_primary.to_csv(HERE / "primary_events.csv", index=False)
    print("\nwrote phase0_results.json + primary_events.csv")


if __name__ == "__main__":
    main()
