"""Candidate 2 -- overnight-range -> RTH-range SAME-DAY transfer on MNQ.

IMPORTANT re-framing (found during grounding, not assumed from the handoff): this
is NOT a single-series magnitude-persistence claim like candidate 1. Overnight
range and RTH range are TWO DIFFERENT series read off the SAME trading day, not
one series lagged against itself. The frozen corrected-null-battery spec's own
D5 section names this exact shape "S2 (overnight->day-session transmission)" and
explicitly says: "the S1 null does NOT port -- bias and outcome are different
series sharing a slow common vol state; joint surrogation preserves the effect
under test, independent surrogation deletes the mundane common-state confound."

D5's un-pause conditions for S2:
  (1) the corrected battery's official re-score PASS on >=1 instrument -- TRUE
      (GC/CL both landed under the spec).
  (2) S2 reframed INCREMENTAL with a stage-1 $0 cheap falsifier FIRST: does
      overnight-state conditioning BEAT matched day-session-history conditioning
      (bias' = 1{DS_{d-1} >= P80 trailing}) on the SAME days? No increment -> S2
      dies for $0.
  (3) only if an increment exists: a stage-2 null design, adversarial review,
      and the slate's operator GO.

This script runs ONLY step (2), which is what a Notice-phase look-around can
honestly do at $0. It does NOT run the IAAFT battery on this candidate -- doing
so before clearing step 2 would be exactly the "S1 null on an S2-shaped claim"
mistake the spec was written to prevent.

Design: on trading day d,
  bias_d      = 1{ON_range_d  >= P80(ON_range_{d-60..d-1})}   (overnight-state)
  bias'_d     = 1{RTH_range_{d-1} >= P80(RTH_range_{d-61..d-2})}  (matched day-history:
                yesterday's OWN RTH range, strictly prior, same window length)
  y_d         = 1{RTH_range_d > P50(RTH_range_{d-60..d-1})}   (today's RTH range, elevated
                vs its own trailing median -- NOTE: through-yesterday only, since RTH_range_d
                is the outcome itself and must not enter its own reference window)
Stratify on bias'_d and compare P(y_d=1 | bias_d=1, bias'_d=s) vs P(y_d=1 | bias_d=0,
bias'_d=s) for s in {0,1} -- overnight-state's INCREMENTAL lift over day-history,
matched on day-history state.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from data_lib import load_raw, rth_ohlc, overnight_ohlc, range_series  # noqa: E402

WINDOW, Q_BIAS, Q_REF = 60, 0.80, 0.50


def rolling_pct_strict_prior(x: np.ndarray, window: int, q: float) -> np.ndarray:
    from numpy.lib.stride_tricks import sliding_window_view
    n = len(x)
    out = np.full(n, np.nan)
    if n > window:
        wins = sliding_window_view(x, window)
        out[window:] = np.percentile(wins[: n - window], q * 100, axis=1)
    return out


def rolling_pct_through_yesterday(x: np.ndarray, window: int, q: float) -> np.ndarray:
    """ref[i] = q-th pct of x[i-window : i] -- same as strict-prior; named
    separately for readability at the call site (this IS the outcome's own
    reference, computed causally, excluding day i itself)."""
    return rolling_pct_strict_prior(x, window, q)


def main():
    df = load_raw()
    rth = rth_ohlc(df)
    on = overnight_ohlc(df)
    # Align on common trading days present in BOTH frames (a handful of trading
    # days have no RTH bars at all -- full-session holidays, MNQ.md's own
    # 11-day gap between 1559 full-session days and 1548 RTH sessions).
    common = rth.index.intersection(on.index)
    rth = rth.loc[common].sort_index()
    on = on.loc[common].sort_index()
    rth_range = range_series(rth).to_numpy()
    on_range = range_series(on).to_numpy()
    n = len(common)
    print(f"aligned trading days (RTH+overnight both present): {n}")

    bias = (on_range >= rolling_pct_strict_prior(on_range, WINDOW, Q_BIAS)).astype(float)
    bias[np.isnan(rolling_pct_strict_prior(on_range, WINDOW, Q_BIAS))] = np.nan

    bias_prime = (rth_range >= rolling_pct_strict_prior(rth_range, WINDOW, Q_BIAS)).astype(float)
    bias_prime[np.isnan(rolling_pct_strict_prior(rth_range, WINDOW, Q_BIAS))] = np.nan
    # bias' must reference d-1's RTH range vs d-1's OWN trailing window (strictly
    # prior to d-1) -- i.e. shift bias_prime computed at index (d-1) forward to
    # align with day d's row.
    bias_prime_shifted = np.full(n, np.nan)
    bias_prime_shifted[1:] = bias_prime[:-1]

    ref = rolling_pct_through_yesterday(rth_range, WINDOW, Q_REF)
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

    naive_overnight = rate(b == 1)
    naive_dayhist = rate(bp == 1)
    print(f"naive P(y=1|overnight-bias=1) = {naive_overnight[0]:.4f} (n={naive_overnight[1]})")
    print(f"naive P(y=1|dayhist-bias=1)   = {naive_dayhist[0]:.4f} (n={naive_dayhist[1]})")

    strata = {}
    for s in (0, 1):
        s_mask = bp == s
        hi = rate(s_mask & (b == 1))
        lo = rate(s_mask & (b == 0))
        strata[s] = dict(overnight_hi=hi, overnight_lo=lo,
                          lift=(hi[0] - lo[0]) if (hi[1] and lo[1]) else None)
        print(f"stratum bias'={s}: P(y=1|overnight=1)={hi[0]:.4f}(n={hi[1]})  "
              f"P(y=1|overnight=0)={lo[0]:.4f}(n={lo[1]})  lift={strata[s]['lift']}")

    # $0 cheap falsifier verdict: does overnight-state supply INCREMENTAL lift
    # over matched day-history, in BOTH strata (or at least not reverse sign)?
    lifts = [v["lift"] for v in strata.values() if v["lift"] is not None]
    increment_exists = len(lifts) > 0 and all(l is not None and l > 0.02 for l in lifts)  # 2pp = well above noise floor for this n
    print(f"\nSTAGE-1 $0 FALSIFIER (D5 un-pause condition 2): increment_exists={increment_exists}")
    print("(threshold: incremental lift > 2pp in EVERY populated bias'-stratum)")

    out = dict(
        n_scored=n_scored,
        naive_overnight=naive_overnight, naive_dayhist=naive_dayhist,
        strata=strata, increment_exists=bool(increment_exists),
    )
    (HERE / "candidate2_results.json").write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
