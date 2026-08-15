#!/usr/bin/env python3
# =============================================================================
# PHAROS — Event Parser v0.1
# -----------------------------------------------------------------------------
# Ingests the CSV produced by the PHAROS FVG/Pool/Sweep detector (TV export),
# runs a bar-level Step-0 panel-integrity battery, undoes the pivot-confirmation
# lag, and assembles the DIRECTIONAL sweep -> subsequent-FVG -> opposing-pool
# setup set that feeds the pre-registered test.
#
# DISCIPLINE (per strategy-validation skill):
#   * Step-0 first. No assembly before the integrity battery passes.
#   * No look-ahead. The join only pairs a sweep with an FVG that forms at or
#     after the sweep bar; the target is a pool that already existed (and was
#     confirmed) at sweep time. Outcome (path to target vs stop) is NOT computed
#     here — that is a separate forward-simulation step with explicit path-order
#     assumptions and the excursion-bounded counterfactual discipline.
#   * No baked selection. Entry / stop / target RULES are pre-registration
#     choices. This parser emits geometric PRIMITIVES only. The diag_* columns
#     are sizing-feasibility diagnostics for the cost-law pre-flight, NOT a rule.
#
# PROVENANCE NOTE (Rule 0 — file paths/names are not data provenance):
#   TV bar exports embed no symbol header, so provenance cannot be cross-checked
#   in-file. It is asserted from the filename (PEPPERSTONE_US500_15) plus two
#   weak corroborants: 15-min spacing and price magnitude. The user must confirm
#   the chart was the Pepperstone US500 CFD at 15m (the gate-bearing R&D feed).
# =============================================================================

import argparse
import sys
import pandas as pd
import numpy as np
from datetime import timezone

try:
    from zoneinfo import ZoneInfo
    ET = ZoneInfo("America/New_York")
except Exception:  # pragma: no cover
    ET = None

FLAG_COLS = ["fvg_bull", "fvg_bear", "pivot_high", "pivot_low",
             "sweep_high", "sweep_low", "break_high", "break_low"]


# -----------------------------------------------------------------------------
# Load
# -----------------------------------------------------------------------------
def load_bars(path):
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    df["time"] = df["time"].astype("int64")
    df["ts_utc"] = pd.to_datetime(df["time"], unit="s", utc=True)
    df["ts_et"] = df["ts_utc"].dt.tz_convert(ET) if ET is not None else df["ts_utc"]
    df = df.reset_index(drop=True)
    df["bar_pos"] = df.index  # position within THIS export window (not TV bar_index)
    return df


# -----------------------------------------------------------------------------
# Step-0 panel-integrity battery (bar-data adaptation)
# -----------------------------------------------------------------------------
def integrity_report(df, expected_tf_min=15):
    hard_fail = []
    soft_flag = []
    n = len(df)
    t = df["time"]
    diffs = t.diff().dropna()
    modal = int(diffs.mode().iloc[0]) if len(diffs) else 0
    expected_s = expected_tf_min * 60

    # monotonic / duplicates
    mono = t.is_monotonic_increasing
    dups = int(t.duplicated().sum())
    if not mono:
        hard_fail.append("time not monotonic increasing")
    if dups:
        hard_fail.append(f"{dups} duplicate timestamps")

    # spacing
    if modal != expected_s:
        hard_fail.append(f"modal spacing {modal}s != expected {expected_s}s "
                         f"(declared {expected_tf_min}m)")

    # UTC minute census -> must be subset of the declared grid
    mins = sorted(((t % 3600) // 60).unique().tolist())
    allowed = set(range(0, 60, expected_tf_min))
    if not set(mins).issubset(allowed):
        hard_fail.append(f"UTC minute census {mins} not subset of {sorted(allowed)} "
                         f"(wrong chart TF?)")

    # gaps (weekends / daily breaks expected -> soft)
    big = diffs[diffs > 2 * modal] if modal else diffs[diffs > 0]
    largest_h = round(big.max() / 3600, 1) if len(big) else 0.0

    # event presence -> all-zero stream is suspect
    counts = {c: int(df[c].sum()) for c in FLAG_COLS}
    for c, v in counts.items():
        if v == 0:
            soft_flag.append(f"stream '{c}' has zero events")

    print("=" * 70)
    print("STEP-0 PANEL INTEGRITY  (bar data)")
    print("=" * 70)
    print(f"bars                : {n}")
    if ET is not None:
        print(f"window (ET)         : {df['ts_et'].iloc[0]}  ->  {df['ts_et'].iloc[-1]}")
    print(f"window (UTC)        : {df['ts_utc'].iloc[0]}  ->  {df['ts_utc'].iloc[-1]}")
    print(f"modal spacing       : {modal}s  (min {int(diffs.min())}, max {int(diffs.max())})")
    print(f"monotonic / dups    : {mono} / {dups}")
    print(f"UTC minute census   : {mins}   [PASS]" if set(mins).issubset(allowed)
          else f"UTC minute census   : {mins}   [FAIL]")
    print(f"gaps > 2x modal     : {len(big)}  (largest {largest_h}h — weekends/daily breaks)")
    print(f"price magnitude     : {df['close'].min():.1f} – {df['close'].max():.1f} "
          f"(corroborant for US500)")
    print("event counts        : " + "  ".join(f"{c}={v}" for c, v in counts.items()))

    if soft_flag:
        print("\nSOFT FLAGS:")
        for s in soft_flag:
            print(f"  - {s}")
    if hard_fail:
        print("\nHARD FAILS (HALT — do not assemble):")
        for h in hard_fail:
            print(f"  - {h}")
        return False
    print("\nINTEGRITY: PASS")
    return True


# -----------------------------------------------------------------------------
# Pivot-lag inference (build-independent) + m_ph/m_pl cross-check
# -----------------------------------------------------------------------------
def infer_pivot_len(df, max_back=400, tol=0.05):
    h = df["high"].values
    low = df["low"].values
    lags = []

    def back_match(i, level, series):
        for k in range(1, min(i, max_back) + 1):
            if abs(series[i - k] - level) <= tol:
                return k
        return None

    ph_idx = df.index[df["pivot_high"] == 1]
    for i in ph_idx:
        lvl = df.at[i, "pivot_high_lvl"]
        if pd.notna(lvl):
            k = back_match(i, lvl, h)
            if k is not None:
                lags.append(k)
    pl_idx = df.index[df["pivot_low"] == 1]
    for i in pl_idx:
        lvl = df.at[i, "pivot_low_lvl"]
        if pd.notna(lvl):
            k = back_match(i, lvl, low)
            if k is not None:
                lags.append(k)

    inferred = int(pd.Series(lags).mode().iloc[0]) if lags else None
    agree = float(np.mean([l == inferred for l in lags])) if lags else 0.0

    # cross-check against offset markers: m_ph non-null bars should sit
    # inferred-lag bars BEFORE a pivot_high==1 bar.
    mph_ok = None
    if "m_ph" in df.columns and inferred is not None:
        mph_bars = df.index[df["m_ph"].notna()]
        hits = 0
        for j in mph_bars:
            tgt = j + inferred
            if tgt in df.index and df.at[tgt, "pivot_high"] == 1:
                hits += 1
        mph_ok = (hits / len(mph_bars)) if len(mph_bars) else None

    print("\n" + "=" * 70)
    print("PIVOT-LAG INFERENCE")
    print("=" * 70)
    print(f"inferred pivotLen   : {inferred}  (modal backward high/low match)")
    print(f"lag self-agreement  : {agree*100:.1f}% of pivots share the modal lag")
    if mph_ok is not None:
        print(f"m_ph offset check   : {mph_ok*100:.1f}% of marker bars confirm at +{inferred}")
    return inferred


# -----------------------------------------------------------------------------
# Raw event streams
# -----------------------------------------------------------------------------
def extract_events(df, pivot_len):
    def rows(mask, cols):
        sub = df.loc[mask, ["bar_pos", "ts_et"] + cols].copy()
        return sub.reset_index(drop=True)

    fvg = pd.concat([
        rows(df["fvg_bull"] == 1, ["fvg_bull_top", "fvg_bull_btm", "fvg_bull_size"])
            .rename(columns={"fvg_bull_top": "top", "fvg_bull_btm": "btm",
                             "fvg_bull_size": "size"}).assign(dir="bull"),
        rows(df["fvg_bear"] == 1, ["fvg_bear_top", "fvg_bear_btm", "fvg_bear_size"])
            .rename(columns={"fvg_bear_top": "top", "fvg_bear_btm": "btm",
                             "fvg_bear_size": "size"}).assign(dir="bear"),
    ], ignore_index=True).sort_values("bar_pos").reset_index(drop=True)

    piv = pd.concat([
        rows(df["pivot_high"] == 1, ["pivot_high_lvl"])
            .rename(columns={"pivot_high_lvl": "level"}).assign(side="high"),
        rows(df["pivot_low"] == 1, ["pivot_low_lvl"])
            .rename(columns={"pivot_low_lvl": "level"}).assign(side="low"),
    ], ignore_index=True)
    # true swing bar = confirmation bar - pivotLen (may be off-window if < 0)
    piv["swing_bar"] = piv["bar_pos"] - (pivot_len or 0)
    piv["off_window"] = piv["swing_bar"] < 0
    piv = piv.sort_values("bar_pos").reset_index(drop=True)

    swp = pd.concat([
        rows(df["sweep_low"] == 1, ["sweep_low_lvl", "sweep_low_target", "atr", "low"])
            .rename(columns={"sweep_low_lvl": "swept_level",
                             "sweep_low_target": "target_level",
                             "low": "extreme"}).assign(direction="long"),
        rows(df["sweep_high"] == 1, ["sweep_high_lvl", "sweep_high_target", "atr", "high"])
            .rename(columns={"sweep_high_lvl": "swept_level",
                             "sweep_high_target": "target_level",
                             "high": "extreme"}).assign(direction="short"),
    ], ignore_index=True).sort_values("bar_pos").reset_index(drop=True)

    brk = pd.concat([
        rows(df["break_high"] == 1, ["break_high_lvl"])
            .rename(columns={"break_high_lvl": "level"}).assign(side="high"),
        rows(df["break_low"] == 1, ["break_low_lvl"])
            .rename(columns={"break_low_lvl": "level"}).assign(side="low"),
    ], ignore_index=True).sort_values("bar_pos").reset_index(drop=True)

    return fvg, piv, swp, brk


# -----------------------------------------------------------------------------
# Directional setup assembly:  sweep -> first same-direction FVG -> draw target
# -----------------------------------------------------------------------------
def assemble_setups(df, fvg_window):
    out = []
    fb = df.index[df["fvg_bull"] == 1].to_numpy()
    fs = df.index[df["fvg_bear"] == 1].to_numpy()

    sweeps = []
    for i in df.index[df["sweep_low"] == 1]:
        sweeps.append((i, "long"))
    for i in df.index[df["sweep_high"] == 1]:
        sweeps.append((i, "short"))
    sweeps.sort()

    for i, direction in sweeps:
        if direction == "long":
            swept = df.at[i, "sweep_low_lvl"]
            target = df.at[i, "sweep_low_target"]
            extreme = df.at[i, "low"]            # penetration low -> stop reference
            cand = fb
            top_c, btm_c, size_c = "fvg_bull_top", "fvg_bull_btm", "fvg_bull_size"
        else:
            swept = df.at[i, "sweep_high_lvl"]
            target = df.at[i, "sweep_high_target"]
            extreme = df.at[i, "high"]
            cand = fs
            top_c, btm_c, size_c = "fvg_bear_top", "fvg_bear_btm", "fvg_bear_size"

        # first SAME-direction FVG at bar in [sweep_bar, sweep_bar + window]
        future = cand[(cand >= i) & (cand <= i + fvg_window)]
        matched = len(future) > 0
        rec = dict(
            sweep_bar=int(i),
            sweep_ts_et=df.at[i, "ts_et"],
            direction=direction,
            swept_level=swept,
            sweep_extreme=extreme,
            target_level=target,
            target_present=bool(pd.notna(target)),
            atr_at_sweep=df.at[i, "atr"],
            matched=bool(matched),
            fvg_bar=np.nan, fvg_ts_et=pd.NaT, fvg_lag_bars=np.nan,
            fvg_top=np.nan, fvg_btm=np.nan, fvg_mid=np.nan, fvg_size=np.nan,
            diag_risk_dist=np.nan, diag_target_dist=np.nan, diag_rr=np.nan,
            note="",
        )
        notes = []
        if matched:
            j = int(future[0])
            top, btm = df.at[j, top_c], df.at[j, btm_c]
            mid = (top + btm) / 2.0
            rec.update(fvg_bar=j, fvg_ts_et=df.at[j, "ts_et"],
                       fvg_lag_bars=j - int(i), fvg_top=top, fvg_btm=btm,
                       fvg_mid=mid, fvg_size=df.at[j, size_c])
            # diagnostics ONLY (entry=FVG mid, stop=sweep extreme, reward=target)
            if pd.notna(target):
                risk = abs(mid - extreme)
                rwd = abs(target - mid)
                rec.update(diag_risk_dist=risk, diag_target_dist=rwd,
                           diag_rr=(rwd / risk if risk > 0 else np.nan))
            else:
                notes.append("no_target")
        else:
            notes.append("no_fvg_in_window")
            if pd.isna(target):
                notes.append("no_target")
        rec["note"] = "|".join(notes)
        out.append(rec)

    cols = ["sweep_bar", "sweep_ts_et", "direction", "swept_level", "sweep_extreme",
            "target_level", "target_present", "atr_at_sweep", "matched",
            "fvg_bar", "fvg_ts_et", "fvg_lag_bars", "fvg_top", "fvg_btm", "fvg_mid",
            "fvg_size", "diag_risk_dist", "diag_target_dist", "diag_rr", "note"]
    return pd.DataFrame(out, columns=cols).sort_values("sweep_bar").reset_index(drop=True)


def summarize(setups):
    n = len(setups)
    matched = setups["matched"].sum()
    full = setups[setups["matched"] & setups["target_present"]]
    print("\n" + "=" * 70)
    print("SETUP ASSEMBLY  (sweep -> same-direction FVG -> draw target)")
    print("=" * 70)
    print(f"sweeps (candidates)     : {n}")
    print(f"  long / short          : {(setups.direction=='long').sum()} / "
          f"{(setups.direction=='short').sum()}")
    print(f"matched an FVG in window: {matched}  ({matched/n*100:.1f}%)")
    print(f"complete (FVG + target) : {len(full)}  ({len(full)/n*100:.1f}%)")
    print(f"no target available     : {(~setups.target_present).sum()}")
    if matched:
        lag = setups.loc[setups.matched, "fvg_lag_bars"]
        print(f"FVG lag (bars) median   : {lag.median():.0f}  "
              f"(p25 {lag.quantile(.25):.0f} / p75 {lag.quantile(.75):.0f} / max {lag.max():.0f})")
    if len(full):
        rr = full["diag_rr"].replace([np.inf, -np.inf], np.nan).dropna()
        print(f"diag R:R (FVG-mid)      : median {rr.median():.2f}  "
              f"(p25 {rr.quantile(.25):.2f} / p75 {rr.quantile(.75):.2f})  [diagnostic only]")
        risk = full["diag_risk_dist"].dropna()
        px = (full["fvg_mid"]).dropna()
        cost_mult = (px / risk).replace([np.inf, -np.inf], np.nan).dropna()
        print(f"price/stop_dist (median): {cost_mult.median():.0f}x  "
              f"-> cost-law pre-flight is load-bearing (§2)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--pivot-len", type=int, default=None,
                    help="override; default = inferred from data")
    ap.add_argument("--fvg-window", type=int, default=12,
                    help="max bars after a sweep to accept the entry FVG (15m: 12 = 3h)")
    ap.add_argument("--out-dir", default="/mnt/user-data/outputs")
    args = ap.parse_args()

    df = load_bars(args.csv)
    if not integrity_report(df):
        print("\nABORTED on integrity HARD FAIL.")
        sys.exit(1)

    inferred = infer_pivot_len(df)
    pivot_len = args.pivot_len if args.pivot_len is not None else inferred
    if args.pivot_len is not None and inferred is not None and args.pivot_len != inferred:
        print(f"  NOTE: override {args.pivot_len} differs from inferred {inferred} "
              f"— using override.")

    fvg, piv, swp, brk = extract_events(df, pivot_len)
    setups = assemble_setups(df, args.fvg_window)
    summarize(setups)

    od = args.out_dir.rstrip("/")
    setups.to_csv(f"{od}/setups.csv", index=False)
    fvg.to_csv(f"{od}/events_fvg.csv", index=False)
    piv.to_csv(f"{od}/events_pivots.csv", index=False)
    swp.to_csv(f"{od}/events_sweeps.csv", index=False)
    brk.to_csv(f"{od}/events_breaks.csv", index=False)
    print(f"\nwrote: setups.csv ({len(setups)}), events_fvg ({len(fvg)}), "
          f"events_pivots ({len(piv)}), events_sweeps ({len(swp)}), "
          f"events_breaks ({len(brk)})  ->  {od}/")


if __name__ == "__main__":
    main()
