"""Candidate 3 -- bar-volume regime -> next-bar range (M15, ToD-deseasonalized).

Constraint-audit catch #2 (this session): plain M15 volume has a strong intraday
U-shape (open/close busy, midday and overnight thin) -- a raw pooled trailing-median
threshold would mostly just rediscover that shape, not a genuine "regime" claim. Every
bias/outcome value below is expressed relative to its OWN time-of-day slot's trailing
median (20 prior same-slot occurrences, ~1 trading month), matching the precedent set
by tod-baseline-range-trigger's "same time-of-day slot's own trailing median" framing
(MECHANISMS.md) rather than inventing a fresh deseasonalization convention.

Constraint-audit catch #3: volume and range are DIFFERENT series. Even at 1-bar lag,
volatility clustering has memory far longer than 15 minutes, so "high-volume bar_t ->
high-range bar_{t+1}" could be entirely explained by both series riding the same slow
regime state, exactly the S2 cross-series confound flagged for candidates 2/4 in
c2_c4_increment_falsifiers.py -- NOT resolved by independent-series IAAFT surrogation.
Scored the same way as 2/4: a $0 increment test against the mundane same-series
comparator (does range_t itself already predict range_{t+1} as well as volume_t does?),
not a full corrected battery. Null-validity grounding for volume clustering as a stylized
fact: the mixture-of-distributions literature (Tauchen & Pitts 1983; Bollerslev &
Jubinski 1999) -- the same general information-arrival-clustering family the frozen
spec cites for range/TR (ARCH/GARCH canon), not a repo-native frozen battery.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from load_sessions import load_bars

HERE = Path(__file__).resolve().parent
TOD_WINDOW = 20  # trailing same-slot occurrences (~1 month of that exact 15m slot)
BOOT_SEED = 20260829
CI_DRAWS = 4000


def tod_ratio(values: np.ndarray, slot: np.ndarray, window: int) -> np.ndarray:
    """values[t] / trailing-median(values at the same slot, strictly prior `window`
    occurrences). NaN until a slot has `window` prior observations."""
    n = len(values)
    out = np.full(n, np.nan)
    by_slot: dict[int, list[float]] = {}
    order_by_slot: dict[int, list[int]] = {}
    for t in range(n):
        s = int(slot[t])
        hist = by_slot.get(s, [])
        if len(hist) >= window:
            med = float(np.median(hist[-window:]))
            if med > 0:
                out[t] = values[t] / med
        hist.append(float(values[t]))
        by_slot[s] = hist
    return out


def main():
    bars = load_bars()
    bars = bars[bars["session"] < bars["session"].max()]  # drop trailing truncated day
    n = len(bars)
    print(f"bars: {n}")

    vol = bars["volume"].to_numpy(dtype=float)
    rng = (bars["high"] - bars["low"]).to_numpy(dtype=float)
    slot = bars["minute"].to_numpy(dtype=int)

    vol_ratio = tod_ratio(vol, slot, TOD_WINDOW)
    rng_ratio = tod_ratio(rng, slot, TOD_WINDOW)
    print(f"vol_ratio valid: {np.sum(~np.isnan(vol_ratio))}  "
          f"rng_ratio valid: {np.sum(~np.isnan(rng_ratio))}")

    # bias_new[t] = 1{vol_ratio[t] > 1} (above-ToD-median-volume bar), predicting
    # y[t+1] = 1{rng_ratio[t+1] > 1} (next bar's range above its own ToD-median)
    bias_new = np.full(n, np.nan)
    valid_v = ~np.isnan(vol_ratio)
    bias_new[valid_v] = (vol_ratio[valid_v] > 1.0).astype(float)

    y = np.full(n, np.nan)
    y[:-1] = np.where(~np.isnan(rng_ratio[1:]), (rng_ratio[1:] > 1.0).astype(float), np.nan)

    # same-series comparator: bias_hist[t] = 1{rng_ratio[t] > 1} (this bar's OWN range
    # already elevated), predicting the SAME y[t+1] -- the mundane same-series
    # persistence a volume-regime claim must beat to be informative.
    bias_hist = np.full(n, np.nan)
    valid_r = ~np.isnan(rng_ratio)
    bias_hist[valid_r] = (rng_ratio[valid_r] > 1.0).astype(float)

    scored_new = (~np.isnan(bias_new)) & (~np.isnan(y))
    scored_hist = (~np.isnan(bias_hist)) & (~np.isnan(y))
    common = scored_new & scored_hist
    n_common = int(common.sum())
    print(f"n_common={n_common}")

    b_new = bias_new[common].astype(int)
    b_hist = bias_hist[common].astype(int)
    y_c = y[common].astype(int)

    obs_new = float(y_c[b_new == 1].mean())
    obs_hist = float(y_c[b_hist == 1].mean())
    n_cond_new = int((b_new == 1).sum())
    n_cond_hist = int((b_hist == 1).sum())
    print(f"n_cond_new(volume)={n_cond_new}  n_cond_hist(own-range)={n_cond_hist}")
    print(f"obs_new(volume-conditioned)={obs_new:.4f}  obs_hist(own-range-conditioned)={obs_hist:.4f}")

    rng_gen = np.random.default_rng(BOOT_SEED)
    N = n_common
    block = 96  # ~1 session of M15 bars, block-preserve intraday/regime structure
    nblocks = int(np.ceil(N / block))
    diffs = []
    for _ in range(CI_DRAWS):
        st = rng_gen.integers(0, N, size=nblocks)
        idx = (st[:, None] + np.arange(block)[None, :]) % N
        idx = idx.ravel()[:N]
        bn, bh, yy = b_new[idx], b_hist[idx], y_c[idx]
        mn, mh = bn == 1, bh == 1
        rn = yy[mn].mean() if mn.any() else np.nan
        rh = yy[mh].mean() if mh.any() else np.nan
        if np.isfinite(rn) and np.isfinite(rh):
            diffs.append(rn - rh)
    diffs = np.asarray(diffs)
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p_two_sided = min(2 * min(float((diffs <= 0).mean()), float((diffs >= 0).mean())), 1.0)
    diff = obs_new - obs_hist
    verdict = "INCREMENT" if lo > 0 else ("NO-INCREMENT" if hi < 0 else "AMBIGUOUS (CI straddles 0)")
    print(f"diff={diff:+.4f}  95% CI=[{lo:+.4f},{hi:+.4f}]  p_two_sided={p_two_sided:.4f}  "
          f"VERDICT={verdict}  (n_valid_boot={len(diffs)})")

    # unconditional base rate + own-series presence check (disclosure, not gating)
    p_unconditional = float(y_c.mean())
    print(f"unconditional P(y=1)={p_unconditional:.4f}")

    out = dict(n_common=n_common, n_cond_new=n_cond_new, n_cond_hist=n_cond_hist,
               obs_new=obs_new, obs_hist=obs_hist, diff=diff, diff_ci=[float(lo), float(hi)],
               p_two_sided=p_two_sided,
               verdict=verdict, p_unconditional=p_unconditional, n_valid_boot=int(len(diffs)))
    (HERE / "c3_results.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
