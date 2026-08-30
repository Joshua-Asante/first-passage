"""Candidate 3 -- bar-volume regime -> next-bar conditioning on MNQ M15.

Null-validity citation (required by futures-anomaly-discovery's "fresh batteries
need the same check reuse gets" rule -- this is NOT the TR magnitude-persistence
battery, and does not borrow it): M15 volume carries a strong DETERMINISTIC
intraday seasonality (U-shape around the RTH open/close, a step at the RTH open
itself, near-zero overnight troughs). A naive "volume above its POOLED trailing
median" bias computed across all bars regardless of time-of-day is confounded by
this seasonality on BOTH sides of the test: the 09:30 ET bar is mechanically
almost always "high volume" and the FOLLOWING 09:45 ET bar is also mechanically
almost always "high volume" for the same seasonal reason, independent of any
genuine volume-clustering mechanism. This is the identical class of confound
that this repo's own `tod-baseline-range-trigger` class (Q-TODVOL-1,
MECHANISMS.md) was built to avoid, by conditioning the trailing-median reference
on the SAME time-of-day slot rather than pooling across slots. This script
adopts that same design as its null-validity argument: the causal reference for
"is this bar's volume elevated" is that SAME intraday slot's own trailing
history (e.g. every 09:30 bar compared only against prior 09:30 bars), which
structurally removes the seasonal confound by construction -- not by a
statistical correction after the fact.

Both designs are run and disclosed side by side (naive pooled vs ToD-matched)
specifically so the seasonality artifact's SIZE is visible, mirroring the
frozen battery's own AR(1) positive-control discipline (show what the naive
version gets wrong, not just what the fixed version gets right).

Outcome tested: next M15 bar's (a) range (H-L) elevated vs ITS OWN ToD-matched
trailing median, and (b) directional continuation (sign of next bar's
close-open matches sign of the trigger bar's close-open). Both are entry-free
conditioner claims, following candidate 1's framing.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from data_lib import load_raw  # noqa: E402

TRAIL_N = 60  # trailing observations for the causal median/quantile reference
Q_BIAS = 0.50  # "above trailing median volume" (candidate framing: "above-trailing-median-volume")


def rolling_pct_strict_prior_by_group(values: np.ndarray, group: np.ndarray, window: int, q: float) -> np.ndarray:
    """ToD-matched causal reference: threshold[i] = q-th pct of the `window`
    most recent PRIOR observations sharing group[i]'s label (e.g. same
    time-of-day slot). O(n * window) but n here is ~141k and window=60 -- fine."""
    n = len(values)
    out = np.full(n, np.nan)
    history: dict = {}
    for i in range(n):
        g = group[i]
        hist = history.get(g)
        if hist is not None and len(hist) >= window:
            out[i] = np.percentile(hist[-window:], q * 100)
        buf = history.setdefault(g, [])
        buf.append(values[i])
    return out


def rolling_pct_strict_prior_pooled(values: np.ndarray, window: int, q: float) -> np.ndarray:
    from numpy.lib.stride_tricks import sliding_window_view
    n = len(values)
    out = np.full(n, np.nan)
    if n > window:
        wins = sliding_window_view(values, window)
        out[window:] = np.percentile(wins[: n - window], q * 100, axis=1)
    return out


def score(bias, outcome):
    scored = (~np.isnan(bias)) & (~np.isnan(outcome))
    b, o = bias[scored].astype(int), outcome[scored].astype(int)
    m = b == 1
    n_cond = int(m.sum())
    obs = float(o[m].mean()) if n_cond else float("nan")
    base = float(o.mean())
    return dict(n_scored=int(scored.sum()), n_cond=n_cond, obs=obs, base_rate=base, lift=obs - base)


def block_bootstrap_ci(bias, outcome, block, n_draws, seed):
    rng = np.random.default_rng(seed)
    scored = (~np.isnan(bias)) & (~np.isnan(outcome))
    b, o = bias[scored].astype(int), outcome[scored].astype(int)
    N = len(b)
    nblocks = int(np.ceil(N / block))
    stats = []
    for _ in range(n_draws):
        st = rng.integers(0, N, size=nblocks)
        idx = (st[:, None] + np.arange(block)[None, :]) % N
        idx = idx.ravel()[:N]
        bb, oo = b[idx], o[idx]
        m = bb == 1
        if m.any():
            stats.append(float(oo[m].mean()))
    stats = np.asarray(stats)
    return float(np.percentile(stats, 2.5)), float(np.percentile(stats, 97.5))


def main():
    df = load_raw().reset_index(drop=True)
    n = len(df)
    vol = df["volume"].to_numpy(dtype=float)
    op, hi, lo, cl = df["open"].to_numpy(), df["high"].to_numpy(), df["low"].to_numpy(), df["close"].to_numpy()
    rng_bar = hi - lo
    dir_bar = np.sign(cl - op)
    et_minute = df["et_minute"].to_numpy()

    # trigger bar t: bias_t = 1{vol_t >= trailing-median(vol, same ToD slot)}
    # outcome bar t+1: elevated range vs ITS OWN ToD-matched trailing median; and
    # directional continuation vs bar t's own direction.
    print(f"n bars: {n}, distinct ToD slots (et_minute): {len(np.unique(et_minute))}")

    # -- naive pooled design --
    thresh_pooled = rolling_pct_strict_prior_pooled(vol, TRAIL_N, Q_BIAS)
    bias_pooled = np.where(np.isnan(thresh_pooled), np.nan, (vol >= thresh_pooled).astype(float))

    rng_thresh_pooled = rolling_pct_strict_prior_pooled(rng_bar, TRAIL_N, Q_REF := 0.50)
    outcome_range_pooled = np.full(n, np.nan)
    outcome_range_pooled[:-1] = (rng_bar[1:] > rng_thresh_pooled[:-1]).astype(float)
    outcome_range_pooled[np.isnan(rng_thresh_pooled)[:-1].tolist() + [True]] = np.nan  # last has no t+1

    outcome_dir_pooled = np.full(n, np.nan)
    same_dir = (dir_bar[1:] != 0) & (dir_bar[1:] == dir_bar[:-1])
    outcome_dir_pooled[:-1] = same_dir.astype(float)
    outcome_dir_pooled[dir_bar == 0] = np.nan  # trigger bar itself flat -> no directional claim

    naive_range = score(bias_pooled, outcome_range_pooled)
    naive_dir = score(bias_pooled, outcome_dir_pooled)
    print(f"\n[NAIVE POOLED, ToD-confounded]  range: {naive_range}")
    print(f"[NAIVE POOLED, ToD-confounded]  dir:   {naive_dir}")

    # -- ToD-matched design --
    thresh_tod = rolling_pct_strict_prior_by_group(vol, et_minute, TRAIL_N, Q_BIAS)
    bias_tod = np.where(np.isnan(thresh_tod), np.nan, (vol >= thresh_tod).astype(float))

    rng_thresh_tod = rolling_pct_strict_prior_by_group(rng_bar, et_minute, TRAIL_N, Q_REF)
    outcome_range_tod = np.full(n, np.nan)
    # Fixed 2026-08-30 (Codex review, PR #210): this compared the NEXT bar's range
    # against the TRIGGER bar's own ToD-conditioned threshold (rng_thresh_tod[:-1]),
    # not the next bar's own slot's threshold -- reintroducing exactly the ToD
    # seasonality confound this design exists to remove, since consecutive M15
    # bars are almost always in different ToD slots. Corrected to compare each
    # next bar against ITS OWN slot's threshold (rng_thresh_tod[1:]), matching
    # this module's own docstring ("elevated vs ITS OWN ToD-matched trailing
    # median") and the MYM sibling script's already-correct `rng_ratio[1:]`
    # design. NOT re-run in this environment (no MNQ_M15.csv) -- the corrected
    # code is committed; the headline +18.1pp/[0.673,0.695] range-lift figure in
    # this repo's Notice-log and downstream artifacts needs re-verification
    # against a fresh run before being treated as confirmed.
    outcome_range_tod[:-1] = (rng_bar[1:] > rng_thresh_tod[1:]).astype(float)
    outcome_range_tod[-1] = np.nan

    outcome_dir_tod = outcome_dir_pooled  # direction-continuation def is ToD-independent already

    tod_range = score(bias_tod, outcome_range_tod)
    tod_dir = score(bias_tod, outcome_dir_tod)
    print(f"\n[ToD-MATCHED]  range: {tod_range}")
    print(f"[ToD-MATCHED]  dir:   {tod_dir}")

    ci_range = block_bootstrap_ci(bias_tod, outcome_range_tod, block=96, n_draws=4000, seed=42)  # block=~1 trading day
    ci_dir = block_bootstrap_ci(bias_tod, outcome_dir_tod, block=96, n_draws=4000, seed=42)
    print(f"\nToD-matched range CI: {ci_range}   (base rate {tod_range['base_rate']:.4f})")
    print(f"ToD-matched dir   CI: {ci_dir}   (base rate {tod_dir['base_rate']:.4f})")

    out = dict(naive_pooled=dict(range=naive_range, dir=naive_dir),
               tod_matched=dict(range=tod_range, dir=tod_dir, range_ci=ci_range, dir_ci=ci_dir))
    (HERE / "candidate3_results.json").write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
