"""Candidate 4 -- unsigned overnight-gap magnitude -> RTH-range SAME-DAY conditioning.

Same re-framing as candidate 2, for the same reason: gap magnitude and RTH range
are TWO DIFFERENT series read off the same trading day (not one series lagged
against itself), so this is structurally S2-shaped under the frozen corrected-
null-battery spec's D5 taxonomy, not a single-series S1 magnitude-persistence
claim like candidate 1. The handoff's framing ("same corrected-battery family as
#1/#2") undersells this distinction -- it is family-adjacent (a magnitude
conditioning claim) but STRUCTURALLY like #2 (cross-series), not #1
(single-series autocorrelation). D5's stage-1 $0 cheap falsifier therefore
applies here too, before any IAAFT battery: does gap-magnitude conditioning beat
matched day-session-history conditioning on the same days?

Gap defined as |RTH_open_d - RTH_close_{d-1}| in points (the overnight gap
proper -- the jump across the close of RTH session d-1 to the open of RTH
session d, NOT the open of the full trading-day session which would double-count
the overnight range candidate 2 already covers). bias_d = 1{|gap_d| >=
P80(|gap|_{d-60..d-1})}. bias'_d and y_d defined identically to candidate 2
(matched day-history = yesterday's own RTH range; outcome = today's RTH range
elevated vs its own trailing median).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from data_lib import load_raw, rth_ohlc, range_series  # noqa: E402
from candidate2_overnight_rth_transfer import rolling_pct_strict_prior, rolling_pct_through_yesterday  # noqa: E402

WINDOW, Q_BIAS = 60, 0.80


def main():
    df = load_raw()
    rth = rth_ohlc(df)
    rth = rth.sort_index()
    n = len(rth)
    rth_open = rth["open"].to_numpy()
    rth_close = rth["close"].to_numpy()
    rth_range = range_series(rth).to_numpy()

    gap = np.full(n, np.nan)
    gap[1:] = np.abs(rth_open[1:] - rth_close[:-1])
    print(f"RTH sessions: {n}")
    print(f"gap magnitude describe (pts): {np.nanpercentile(gap, [5,25,50,75,95])}")

    bias = (gap >= rolling_pct_strict_prior(gap, WINDOW, Q_BIAS)).astype(float)
    bias[np.isnan(rolling_pct_strict_prior(gap, WINDOW, Q_BIAS))] = np.nan
    bias[np.isnan(gap)] = np.nan

    bias_prime = (rth_range >= rolling_pct_strict_prior(rth_range, WINDOW, Q_BIAS)).astype(float)
    bias_prime[np.isnan(rolling_pct_strict_prior(rth_range, WINDOW, Q_BIAS))] = np.nan
    bias_prime_shifted = np.full(n, np.nan)
    bias_prime_shifted[1:] = bias_prime[:-1]

    ref = rolling_pct_through_yesterday(rth_range, WINDOW, 0.50)
    y = (rth_range > ref).astype(float)
    y[np.isnan(ref)] = np.nan

    scored = (~np.isnan(bias)) & (~np.isnan(bias_prime_shifted)) & (~np.isnan(y))
    b = bias[scored].astype(int)
    bp = bias_prime_shifted[scored].astype(int)
    yy = y[scored].astype(int)
    n_scored = len(yy)
    print(f"scored days: {n_scored}")

    def rate(mask):
        return (float(yy[mask].mean()), int(mask.sum())) if mask.any() else (float("nan"), 0)

    naive_gap = rate(b == 1)
    naive_dayhist = rate(bp == 1)
    print(f"naive P(y=1|gap-bias=1)     = {naive_gap[0]:.4f} (n={naive_gap[1]})")
    print(f"naive P(y=1|dayhist-bias=1) = {naive_dayhist[0]:.4f} (n={naive_dayhist[1]})")

    strata = {}
    for s in (0, 1):
        s_mask = bp == s
        hi = rate(s_mask & (b == 1))
        lo = rate(s_mask & (b == 0))
        strata[s] = dict(gap_hi=hi, gap_lo=lo, lift=(hi[0] - lo[0]) if (hi[1] and lo[1]) else None)
        print(f"stratum bias'={s}: P(y=1|gap=1)={hi[0]:.4f}(n={hi[1]})  P(y=1|gap=0)={lo[0]:.4f}(n={lo[1]})  lift={strata[s]['lift']}")

    lifts = [v["lift"] for v in strata.values() if v["lift"] is not None]
    increment_exists = len(lifts) > 0 and all(l is not None and l > 0.02 for l in lifts)
    print(f"\nSTAGE-1 $0 FALSIFIER: increment_exists={increment_exists}")

    out = dict(n_scored=n_scored, naive_gap=naive_gap, naive_dayhist=naive_dayhist,
               strata=strata, increment_exists=bool(increment_exists))
    (HERE / "candidate4_results.json").write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
