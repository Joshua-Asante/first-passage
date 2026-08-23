#!/usr/bin/env python3
"""DL-2 Iterate-block diagnostic (not a Sec6 step; touches no confirm data,
consumes no OUTER-investigation budget slot -- an internal check on TRAIN
data already read, per the geometric-feasibility-ratio proposal ox-alpha
raised and this campaign's own RESULTS.md Iterate block committed to).

Measures whether DL-2's construction (opposite-prior-extreme stop/target,
derived from a 1- or 2-session lookback window, single-session force-flat
hold) is geometrically feasible on M6A -- i.e., whether price can plausibly
travel far enough within the remaining session to reach either the stop or
the target before force-flat -- independent of any specific signal/variant.

Two measures:
  (A) Full-session ratio (unconditional, no signal needed): for EVERY
      eligible session (skip roll sessions and sessions lacking sufficient
      lookback history), R = session's own achievable range (session open
      through the 16:55 ET force-flat bar) / the reference-window width
      that session's own PDH/PDL level would be derived from. Computed
      separately for lookback=1 and lookback=2 (Sec2's two lookback axis
      settings), since the reference width differs.
  (B) Realized-trade MFE ratio (conditional on trades that actually fired):
      for every trade in every one of the 10 frozen variants, the maximum
      favorable excursion from entry to force-flat, as a fraction of that
      trade's own risk (stop distance) -- how close did price actually get
      to a 1R move, among trades that force-flatted.

Run (repo root):
    PYTHONPATH=lab python lab/archive/dl2_m6a_pdhpdl_2026-08-22/geometric_feasibility_diagnostic.py
"""
from __future__ import annotations

import json

import numpy as np

from stitch import load_train_stitched
from variants import VARIANTS
from engine import (
    build_sessions, is_roll_session_map, trading_calendar,
    _lookback_reference, lookback_level, _trim_to_force_flat, TICK,
    simulate_variant,
)


def full_session_ratios(sessions, session_dates, nonroll_dates, is_roll, lookback):
    """Measure (A): per-session R = achievable range / reference-window width,
    for the given lookback length, over every session with sufficient
    non-roll history before it. Roll sessions themselves are skipped (no
    entries fire there per Sec1; the ratio is about the NEXT tradable
    session's own feasibility)."""
    ratios = []
    for d in session_dates:
        if is_roll[d]:
            continue
        refs = _lookback_reference(nonroll_dates, d, lookback)
        if refs is None:
            continue
        level_high, level_low = lookback_level(sessions, refs)
        width = level_high - level_low
        if width <= 0:
            continue
        o, h, l, c = _trim_to_force_flat(sessions[d])
        if len(c) == 0:
            continue
        achievable = float(h.max() - l.min())
        ratios.append(achievable / width)
    return np.array(ratios, dtype=float)


def realized_trade_mfe_ratios(sessions, trades):
    """Measure (B): for each fired trade, MFE (favorable direction) from
    entry to force-flat, as a fraction of that trade's own risk (stop
    distance). MFE=risk would mean price reached exactly a 1R move in the
    favorable direction; MFE=2R/3R would mean it reached target for a
    2R/3R-target variant."""
    out = []
    for t in trades:
        ss = sessions[t.session_date]
        o, h, l, c = _trim_to_force_flat(ss)
        # crude re-locate: scan from session start (entry_idx unknown here,
        # so use the FULL trimmed session's post-entry-price extremes as an
        # upper bound proxy -- entry happens partway through, so this is a
        # conservative OVER-estimate of MFE, disclosed as such, not a
        # precise re-simulation).
        if t.direction == "long":
            mfe = float(h.max() - t.entry_price)
        else:
            mfe = float(t.entry_price - l.min())
        if t.risk_price > 0:
            out.append(mfe / t.risk_price)
    return np.array(out, dtype=float)


def summarize(name, arr):
    if arr.size == 0:
        return {"name": name, "n": 0}
    return {
        "name": name,
        "n": int(arr.size),
        "median": float(np.median(arr)),
        "mean": float(np.mean(arr)),
        "p10": float(np.percentile(arr, 10)),
        "p25": float(np.percentile(arr, 25)),
        "p75": float(np.percentile(arr, 75)),
        "p90": float(np.percentile(arr, 90)),
        "pct_below_1": float(100.0 * (arr < 1.0).mean()),
        "pct_below_0_5": float(100.0 * (arr < 0.5).mean()),
        "pct_above_2": float(100.0 * (arr > 2.0).mean()),
        "pct_above_3": float(100.0 * (arr > 3.0).mean()),
    }


def main() -> int:
    print("[load] stitching TRAIN partition (6A.FUT, 2010-06-06 -> 2019-01-01) ...")
    stitched, roll_days_utc = load_train_stitched()
    sessions = build_sessions(stitched)
    is_roll = is_roll_session_map(sessions, roll_days_utc)
    session_dates = trading_calendar(sessions)
    nonroll_dates = [d for d in session_dates if not is_roll[d]]
    print(f"[load] {len(session_dates)} Globex sessions, {len(nonroll_dates)} non-roll.\n")

    print("=" * 78)
    print("(A) FULL-SESSION GEOMETRIC FEASIBILITY RATIO (unconditional, no signal)")
    print("    R = session's own achievable range (open..16:55 ET force-flat)")
    print("        / reference-window width (1- or 2-session lookback PDH-PDL)")
    print("=" * 78)
    results = {}
    for lookback in (1, 2):
        r = full_session_ratios(sessions, session_dates, nonroll_dates, is_roll, lookback)
        s = summarize(f"lookback={lookback}", r)
        results[f"full_session_lookback_{lookback}"] = s
        print(f"\nlookback={lookback} sessions (n={s['n']}):")
        print(f"  median R={s['median']:.3f}  mean R={s['mean']:.3f}")
        print(f"  p10={s['p10']:.3f}  p25={s['p25']:.3f}  p75={s['p75']:.3f}  p90={s['p90']:.3f}")
        print(f"  % sessions with R<1.0 (can't even reach the reference width itself): {s['pct_below_1']:.1f}%")
        print(f"  % sessions with R<0.5: {s['pct_below_0_5']:.1f}%")
        print(f"  % sessions with R>2.0 (room for a 2R target beyond the level): {s['pct_above_2']:.1f}%")
        print(f"  % sessions with R>3.0 (room for a 3R target beyond the level): {s['pct_above_3']:.1f}%")

    print("\n" + "=" * 78)
    print("(B) REALIZED-TRADE MFE RATIO (conditional on trades that fired)")
    print("    ratio = max favorable excursion (entry->force-flat) / trade's own risk")
    print("    (conservative over-estimate: uses whole-session extremes as an upper")
    print("    bound on post-entry MFE, since exact entry index isn't re-tracked here)")
    print("=" * 78)
    for var in VARIANTS:
        trades = simulate_variant(sessions, session_dates, nonroll_dates, is_roll, var)
        mfe = realized_trade_mfe_ratios(sessions, trades)
        s = summarize(f"V{var.v}", mfe)
        results[f"trade_mfe_V{var.v}"] = s
        if s["n"] == 0:
            print(f"V{var.v}: n=0")
            continue
        print(f"V{var.v} (lookback={var.lookback}, target={var.target_r}R, n={s['n']}): "
              f"median MFE/R={s['median']:.3f}  mean={s['mean']:.3f}  "
              f"%<1.0={s['pct_below_1']:.1f}%  %>={var.target_r:.0f}R equivalent={s[f'pct_above_{int(var.target_r)}']:.1f}%")

    out_path = "lab/archive/dl2_m6a_pdhpdl_2026-08-22/geometric_feasibility_results.json"
    with open(out_path, "w") as fh:
        json.dump(results, fh, indent=2, default=float)
    print(f"\n[done] wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
