"""Candidates 2 and 4 -- overnight-range->RTH-range transfer (S2) and gap-magnitude->
RTH-range, BOTH re-scoped after reading the frozen spec's own S4 (D5) un-pause clause.

Constraint-audit catch (this session, before running anything): the user's brief framed
candidate 2 as reusable "verbatim" like candidate 1, and candidate 4 as fully open ground
needing only its own corrected-battery run. On reading
docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md SS4 (D5), BOTH
candidates are actually the PAUSED "S2" shape, not the un-paused "S1" shape candidate 1
is: bias and outcome are DIFFERENT series measured on the SAME session (overnight
range / gap magnitude at the open, vs RTH range unfolding over the rest of that same
day) that share a slow common volatility regime -- independent IAAFT surrogation of
either series alone (as candidate 1 legitimately used, same-series next-session) would
NOT delete that mundane common-state confound, only joint surrogation would, and the
spec explicitly marks joint-surrogate design "UNRESOLVED-NEEDS-DESIGN" (O1). Building a
fresh joint-surrogate design is out of scope for a Notice-phase screen.

Per the spec's own SS4 un-pause path, condition (2) is a $0 cheap falsifier owed BEFORE
any full battery is authored: "does overnight-state conditioning beat matched
day-session-history conditioning (bias' = 1{DS_{d-1} >= P80 trailing}) on the same
days? No increment -> S2 dies for $0." That is exactly what this script runs, for BOTH
candidates' bias source (overnight range for #2, |gap| magnitude for #4) against the
SAME day-session-history comparator (yesterday's own RTH range, top-quintile state) --
a real-data-only, no-surrogate-needed head-to-head. No p_upper/attribution claim is
made here; a positive result would still need condition (3) (a joint-surrogate design
passing adversarial review) PLUS the slate's own operator GO before any full battery --
neither of which this session can self-issue.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from load_sessions import load_bars, session_ohlc, rth_ohlc, overnight_ohlc, wilder_tr
import iaaft_battery as B

HERE = Path(__file__).resolve().parent
WINDOW, Q_BIAS, Q_REF = 60, 0.80, 0.50
CI_BLOCK, CI_DRAWS, CI_SEED = 60, 4000, 42
BOOT_SEED = 20260829


def build_frame():
    bars = load_bars()
    full = session_ohlc(bars)
    full = full[full["n_bars"] >= 20]
    rth = rth_ohlc(bars)
    on = overnight_ohlc(bars)
    idx = full.index
    rth = rth.reindex(idx)
    on = on.reindex(idx)

    rth_range = (rth["high"] - rth["low"]).to_numpy()
    on_range = (on["high"] - on["low"]).to_numpy()
    # standard equity-style gap: today's RTH open - yesterday's RTH close
    rth_open = rth["open"].to_numpy()
    rth_close = rth["close"].to_numpy()
    gap = np.full(len(idx), np.nan)
    gap[1:] = rth_open[1:] - rth_close[:-1]
    abs_gap = np.abs(gap)

    return dict(idx=idx, rth_range=rth_range, on_range=on_range, abs_gap=abs_gap)


def conditional_rate_given(bias_source: np.ndarray, outcome: np.ndarray, window: int,
                            q_bias: float, q_ref: float):
    """bias_d from bias_source (strict-prior window on bias_source itself, i.e. bias_source's
    OWN trailing state -- for overnight range and gap magnitude this is same-day, so 'strict
    prior' here means the window looks at bias_source's own trailing 60 sessions ending at
    d-1, then thresholds bias_source[d] itself -- consistent with 'this session's realized
    range/gap is elevated relative to its own recent history')."""
    n = len(bias_source)
    thresh = B.rolling_pctl_strict_prior(bias_source, window, q_bias)
    bias = (bias_source >= thresh).astype(float)
    bias[np.isnan(thresh)] = np.nan

    ref = B.rolling_pctl_through_today(outcome, window, q_ref)
    # outcome is SAME-DAY (contemporaneous), not d+1, for the overnight/gap->RTH-range role
    y = (outcome > np.roll(ref, 1)).astype(float)
    y[0] = np.nan
    y[np.isnan(np.roll(ref, 1))] = np.nan

    scored = (~np.isnan(bias)) & (~np.isnan(y))
    m = scored & (bias == 1)
    obs = float(y[m].mean()) if m.any() else float("nan")
    return obs, bias, y, scored, int(m.sum())


def paired_diff_bootstrap(bias_a: np.ndarray, bias_b: np.ndarray, y: np.ndarray,
                           n_boot: int, seed: int):
    """Block-bootstrap the DIFFERENCE in conditional hit rate (a - b) on the same
    scored index set, using the same circular block scheme as the frozen CI."""
    rng = np.random.default_rng(seed)
    N = len(y)
    block = min(CI_BLOCK, max(1, N // 2))
    nblocks = int(np.ceil(N / block))
    diffs = []
    for _ in range(n_boot):
        st = rng.integers(0, N, size=nblocks)
        idx = (st[:, None] + np.arange(block)[None, :]) % N
        idx = idx.ravel()[:N]
        ba, bb, yy = bias_a[idx], bias_b[idx], y[idx]
        ma, mb = ba == 1, bb == 1
        ra = yy[ma].mean() if ma.any() else np.nan
        rb = yy[mb].mean() if mb.any() else np.nan
        if np.isfinite(ra) and np.isfinite(rb):
            diffs.append(ra - rb)
    diffs = np.asarray(diffs)
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p_two_sided = 2 * min(float((diffs <= 0).mean()), float((diffs >= 0).mean()))
    p_two_sided = min(p_two_sided, 1.0)
    return float(lo), float(hi), float(diffs.mean()), int(len(diffs)), p_two_sided


def run_one(label: str, bias_source: np.ndarray, frame: dict):
    rth_range = frame["rth_range"]
    obs_new, bias_new, y_new, scored_new, n_cond_new = conditional_rate_given(
        bias_source, rth_range, WINDOW, Q_BIAS, Q_REF)
    # day-session-history comparator: YESTERDAY's own RTH-range state (bias' =
    # 1{DS_{d-1} >= P80 trailing}) predicting TODAY's RTH-range -- built by shifting
    # the RTH-range series forward one session before feeding it through the same
    # strict-prior/through-today machinery, so bias_hist[d] reflects information known
    # as of d-1, never d itself.
    rth_range_lag1 = np.roll(rth_range, 1)
    rth_range_lag1[0] = np.nan
    obs_hist, bias_hist, y_hist, scored_hist, n_cond_hist = conditional_rate_given(
        rth_range_lag1, rth_range, WINDOW, Q_BIAS, Q_REF)

    common = scored_new & scored_hist
    n_common = int(common.sum())
    b_new = bias_new[common].astype(int)
    b_hist = bias_hist[common].astype(int)
    y_common = y_new[common].astype(int)  # y is identical under both constructions (same outcome def)
    obs_new_c = float(y_common[b_new == 1].mean()) if (b_new == 1).any() else float("nan")
    obs_hist_c = float(y_common[b_hist == 1].mean()) if (b_hist == 1).any() else float("nan")

    lo, hi, mean_diff, n_valid, p_two_sided = paired_diff_bootstrap(b_new, b_hist, y_common, 4000, BOOT_SEED)

    increment = obs_new_c - obs_hist_c
    verdict = "INCREMENT" if lo > 0 else ("NO-INCREMENT" if hi < 0 else "AMBIGUOUS (CI straddles 0)")

    result = dict(
        label=label, n_common=n_common,
        n_cond_new=int((b_new == 1).sum()), n_cond_hist=int((b_hist == 1).sum()),
        obs_new=obs_new_c, obs_hist=obs_hist_c, diff=increment,
        diff_ci=[lo, hi], diff_mean_boot=mean_diff, n_valid_boot=n_valid,
        p_two_sided=p_two_sided, verdict=verdict,
    )
    print(f"\n[{label}] n_common={n_common} n_cond_new={result['n_cond_new']} "
          f"n_cond_hist={result['n_cond_hist']}")
    print(f"  obs_new(overnight/gap-conditioned)={obs_new_c:.4f}  "
          f"obs_hist(day-history-conditioned)={obs_hist_c:.4f}  diff={increment:+.4f}")
    print(f"  diff 95% CI=[{lo:+.4f},{hi:+.4f}]  p_two_sided={p_two_sided:.4f}  VERDICT={verdict}")
    return result


def main():
    frame = build_frame()
    out = {}
    out["candidate2_overnight_range"] = run_one("candidate2_overnight_range", frame["on_range"], frame)
    out["candidate4_gap_magnitude"] = run_one("candidate4_gap_magnitude", frame["abs_gap"], frame)
    (HERE / "c2_c4_results.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
