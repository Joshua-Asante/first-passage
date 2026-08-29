"""Corrected stratified re-run of MYM candidates 2 (overnight-range) and 4 (gap-magnitude)
against the D5 stage-1 $0 cheap falsifier
(docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md SS4).

WHY THIS REPLACES c2_c4_increment_falsifiers.py's run_one/conditional_rate_given:

The original script computed two MARGINAL conditional rates -- P(y=1 | bias_new=1) vs
P(y=1 | bias_hist=1) -- and diffed them. That does not test "does overnight-state
conditioning ADD information BEYOND matched day-session-history conditioning" the way
the spec's own language ("matched day-session-history CONDITIONING", "INCREMENT")
requires. Two correlated predictors can show near-identical marginal rates while one
still carries large incremental information (or vice versa) -- a marginal horse-race
does not isolate that.

The MNQ sibling campaign (candidate2_overnight_rth_transfer.py) used the correct design:
STRATIFY on bias_hist (bias'), then measure bias_new's lift WITHIN each stratum held
fixed. That is what "matched ... conditioning" means -- match on day-history state, then
ask whether overnight-state still moves the needle. This script ports that exact design
to MYM, reusing MYM's own load_sessions.py / iaaft_battery.py helpers so the underlying
bias/bias'/y definitions are UNCHANGED from the original script (verified equivalent to
MNQ's own definitions) -- only the aggregation step changes from "compare two marginals"
to "stratify and compare within each stratum".

Run from lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/ (same directory as the
original c2_c4_increment_falsifiers.py, so the sys.path-relative imports resolve).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from load_sessions import load_bars, session_ohlc, rth_ohlc, overnight_ohlc
import iaaft_battery as B

HERE = Path(__file__).resolve().parent
WINDOW, Q_BIAS, Q_REF = 60, 0.80, 0.50
CI_BLOCK, CI_DRAWS, BOOT_SEED = 60, 4000, 20260829
MIN_LIFT_FLOOR = 0.02  # 2pp -- same "well above noise floor" threshold MNQ's script used


def build_frame():
    """Unchanged from c2_c4_increment_falsifiers.py -- same data, same series."""
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
    rth_open = rth["open"].to_numpy()
    rth_close = rth["close"].to_numpy()
    gap = np.full(len(idx), np.nan)
    gap[1:] = rth_open[1:] - rth_close[:-1]
    abs_gap = np.abs(gap)

    return dict(idx=idx, rth_range=rth_range, on_range=on_range, abs_gap=abs_gap)


def make_bias_biasprime_y(bias_source: np.ndarray, rth_range: np.ndarray):
    """Bias/bias'/y construction -- IDENTICAL in substance to both the original
    c2_c4_increment_falsifiers.py's bias/bias_hist and MNQ's candidate2 script's
    bias/bias_prime_shifted (confirmed equivalent by inspection during review).
    Kept as a single shared function so candidates 2 and 4 use one code path.

    bias_d  = 1{ bias_source_d      >= P80(trailing 60 bias_source, strict prior) }
    bprime_d= 1{ rth_range_{d-1}    >= P80(trailing 60 rth_range ending d-2) }   (yesterday's
              OWN RTH-range state, matched day-history -- shifted forward to align with day d)
    y_d     = 1{ rth_range_d        >  P50(trailing 60 rth_range ending d-1) }   (today's RTH
              range elevated vs its own trailing median, strictly causal)
    """
    n = len(rth_range)

    thresh_bias = B.rolling_pctl_strict_prior(bias_source, WINDOW, Q_BIAS)
    bias = (bias_source >= thresh_bias).astype(float)
    bias[np.isnan(thresh_bias)] = np.nan

    thresh_bp = B.rolling_pctl_strict_prior(rth_range, WINDOW, Q_BIAS)
    bprime_raw = (rth_range >= thresh_bp).astype(float)
    bprime_raw[np.isnan(thresh_bp)] = np.nan
    bprime = np.full(n, np.nan)
    bprime[1:] = bprime_raw[:-1]  # yesterday's state, aligned to today's row

    ref = B.rolling_pctl_strict_prior(rth_range, WINDOW, Q_REF)
    y = (rth_range > ref).astype(float)
    y[np.isnan(ref)] = np.nan

    return bias, bprime, y


def stratified_lifts(bias: np.ndarray, bprime: np.ndarray, y: np.ndarray):
    """For each bprime stratum s in {0,1}: lift_s = P(y=1|bias=1,bprime=s) - P(y=1|bias=0,bprime=s).
    Returns (lifts: dict[int, float|None], counts: dict[int, dict], scored_mask)."""
    scored = (~np.isnan(bias)) & (~np.isnan(bprime)) & (~np.isnan(y))
    b = bias[scored].astype(int)
    bp = bprime[scored].astype(int)
    yy = y[scored].astype(int)

    def rate(mask):
        return (float(yy[mask].mean()), int(mask.sum())) if mask.any() else (float("nan"), 0)

    lifts, counts = {}, {}
    for s in (0, 1):
        s_mask = bp == s
        hi = rate(s_mask & (b == 1))
        lo = rate(s_mask & (b == 0))
        lift = (hi[0] - lo[0]) if (hi[1] > 0 and lo[1] > 0) else None
        lifts[s] = lift
        counts[s] = dict(hi=hi, lo=lo)
    return lifts, counts, scored, b, bp, yy


def min_stratified_lift(b: np.ndarray, bp: np.ndarray, yy: np.ndarray) -> float:
    """The statistic the bootstrap resamples: min over populated strata of
    P(y=1|bias=1,bprime=s) - P(y=1|bias=0,bprime=s). Matches MNQ's own reporting
    convention ("block-bootstrap ... on the MINIMUM stratified lift") -- the
    conservative read across both day-history states, not an average."""
    vals = []
    for s in (0, 1):
        s_mask = bp == s
        hi_mask, lo_mask = s_mask & (b == 1), s_mask & (b == 0)
        if hi_mask.any() and lo_mask.any():
            vals.append(float(yy[hi_mask].mean() - yy[lo_mask].mean()))
    return min(vals) if vals else float("nan")


def block_bootstrap_min_lift(b: np.ndarray, bp: np.ndarray, yy: np.ndarray,
                              n_boot: int, block: int, seed: int):
    """Circular day-block bootstrap on the minimum stratified lift, same block scheme
    as MYM's original paired_diff_bootstrap (block-of-60-days, resampled as contiguous
    blocks so day-to-day autocorrelation in the underlying series is preserved)."""
    rng = np.random.default_rng(seed)
    N = len(yy)
    block = min(block, max(1, N // 2))
    nblocks = int(np.ceil(N / block))
    draws = []
    for _ in range(n_boot):
        st = rng.integers(0, N, size=nblocks)
        idx = (st[:, None] + np.arange(block)[None, :]) % N
        idx = idx.ravel()[:N]
        v = min_stratified_lift(b[idx], bp[idx], yy[idx])
        if np.isfinite(v):
            draws.append(v)
    draws = np.asarray(draws)
    lo, hi = np.percentile(draws, [2.5, 97.5])
    p_lift_le_0 = float((draws <= 0).mean())
    return float(lo), float(hi), float(draws.mean()), int(len(draws)), p_lift_le_0


def run_one(label: str, bias_source: np.ndarray, frame: dict):
    rth_range = frame["rth_range"]
    bias, bprime, y = make_bias_biasprime_y(bias_source, rth_range)
    lifts, counts, scored, b, bp, yy = stratified_lifts(bias, bprime, y)

    lo, hi, mean_boot, n_valid, p_le0 = block_bootstrap_min_lift(
        b, bp, yy, CI_DRAWS, CI_BLOCK, BOOT_SEED)

    populated_lifts = [l for l in lifts.values() if l is not None]
    increment_exists = len(populated_lifts) > 0 and all(l > MIN_LIFT_FLOOR for l in populated_lifts)
    verdict = "INCREMENT" if (lo > 0 and increment_exists) else (
        "NO-INCREMENT" if hi < 0 else "AMBIGUOUS (CI straddles 0)")

    result = dict(
        label=label, n_scored=int(scored.sum()),
        strata=lifts,
        strata_counts={str(s): counts[s] for s in counts},
        min_lift_bootstrap=dict(ci=[lo, hi], mean=mean_boot, n_valid=n_valid, p_lift_le_0=p_le0),
        increment_exists_threshold_check=bool(increment_exists),
        verdict=verdict,
    )
    print(f"\n[{label}] n_scored={result['n_scored']}")
    for s in (0, 1):
        c = counts[s]
        print(f"  stratum bprime={s}: P(y=1|bias=1)={c['hi'][0]:.4f}(n={c['hi'][1]})  "
              f"P(y=1|bias=0)={c['lo'][0]:.4f}(n={c['lo'][1]})  lift={lifts[s]}")
    print(f"  min-stratified-lift bootstrap: mean={mean_boot:.4f}  CI=[{lo:+.4f},{hi:+.4f}]  "
          f"p(lift<=0)={p_le0:.4f}  VERDICT={verdict}")
    return result


def main():
    frame = build_frame()
    out = {}
    out["candidate2_overnight_range_STRATIFIED"] = run_one(
        "candidate2_overnight_range_STRATIFIED", frame["on_range"], frame)
    out["candidate4_gap_magnitude_STRATIFIED"] = run_one(
        "candidate4_gap_magnitude_STRATIFIED", frame["abs_gap"], frame)
    (HERE / "c2_c4_stratified_results.json").write_text(json.dumps(out, indent=2, default=str))
    print("\nWrote c2_c4_stratified_results.json")
    print("Compare against c2_c4_results.json (the original marginal-comparison run) --")
    print("do NOT overwrite it; both should be cited in the corrected Notice-log entries.")


if __name__ == "__main__":
    main()
