"""Shared IAAFT normal-scores corrected-null battery machinery for the mymdd_1_2026_08_29
Notice batch. Reuses the FROZEN methodology of
docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md (same generation
domain, same two-phase diagnostic-then-score discipline, same L1-L3 presence-limb shapes)
generalized to an arbitrary real-valued series -- the machinery (IAAFT surrogate
generation + Spearman rank-ACF diagnostic gate) is general-purpose; per the futures-
anomaly-discovery skill's "fresh batteries need the same check reuse gets" rule, EVERY
candidate run through this module gets its own diagnostic-gate check computed fresh on
its own series -- never skipped, never inherited from the GC/CL runs.

Deliberately narrower than the frozen spec for a single Notice-phase screen: M=200
(not 1,000), no by-year L4 gate (kept as disclosure only, computed and reported but not
gating -- a formal L4 gate needs a multi-year confirm-power derivation this session does
not owe), single seed family per candidate. This is disclosed as a LIGHTER-WEIGHT reuse,
not claimed at the same rigor as the GC/CL corrected-null run.
"""
from __future__ import annotations

import numpy as np
from scipy.fft import next_fast_len
from scipy.stats import norm, rankdata

ACF_LAGS = 60
TOL_MED, TOL_P95 = 0.04, 0.07
IAAFT_ITER = 100


def normal_scores(x: np.ndarray) -> np.ndarray:
    n = len(x)
    ranks = np.empty(n, dtype=float)
    ranks[np.argsort(x, kind="stable")] = np.arange(1, n + 1)
    return norm.ppf(ranks / (n + 1))


def iaaft(z: np.ndarray, rng: np.random.Generator, n_iter: int = IAAFT_ITER) -> np.ndarray:
    n = len(z)
    z_sorted = np.sort(z)
    target_amp = np.abs(np.fft.rfft(z))
    s = rng.permutation(z)
    for _ in range(n_iter):
        spec = np.fft.rfft(s)
        phases = np.angle(spec)
        s = np.fft.irfft(target_amp * np.exp(1j * phases), n)
        ranks = np.empty(n, dtype=int)
        ranks[np.argsort(s, kind="stable")] = np.arange(n)
        s = z_sorted[ranks]
    return s


def acf(x: np.ndarray, max_lag: int) -> np.ndarray:
    xc = x - x.mean()
    denom = float(np.dot(xc, xc))
    return np.array([float(np.dot(xc[:-k], xc[k:]) / denom) for k in range(1, max_lag + 1)])


def fast_fft_trim(x: np.ndarray, max_drop_frac: float = 0.05) -> np.ndarray:
    """Trim leading points so len(x) is an FFT-fast length (scipy.fft.next_fast_len),
    dropping at most `max_drop_frac` of the series. A prime-heavy length (e.g.
    141,467 = 241 x 587, both large primes -- measured on this exact MYM bar
    count) makes np.fft.rfft/irfft fall back to a slow path (measured: ~61ms per
    rfft+irfft pair at n=141,467 vs ~5ms at the nearest fast length) -- every
    IAAFT iteration pays that cost, which is what made the untrimmed candidate-5
    run impractically slow (>300s and still <25% done). Trimming from the FRONT
    (not the back) keeps the most recent, most decision-relevant history intact.
    Searches downward from n (via repeated next_fast_len calls, not a naive
    2/3/5/7-only smoothness check -- 7-smooth numbers are too sparse near 1e5 to
    reliably land inside a small window) for the largest fast length <= n."""
    n = len(x)
    floor = int(n * (1 - max_drop_frac))
    target = n
    for _ in range(200):
        cand = next_fast_len(target)
        if cand <= n:
            if cand < floor:
                break  # budget exhausted -- fall back unchanged below
            return x[n - cand:]
        target -= (cand - n) + 1
    return x  # no fast length found within budget -- fall back unchanged


def generate_surrogates(real: np.ndarray, M: int, seed_base: int, code: int,
                         seed_offset: int = 0, acf_lags: int = ACF_LAGS,
                         n_iter: int = IAAFT_ITER):
    """Phase 1: IAAFT normal-scores surrogates + diagnostic gate, computed BEFORE any
    hit rate. Returns (surrogates, diagnostics dict)."""
    real = fast_fft_trim(real)
    z = normal_scores(real)
    real_spear = acf(rankdata(real), min(acf_lags, len(real) // 3))
    lags = min(acf_lags, len(real) // 3)
    real_spear = acf(rankdata(real), lags)
    real_sorted = np.sort(real)
    surrogates, mismatches = [], []
    for i in range(M):
        rng = np.random.default_rng([seed_base, code, seed_offset + i])
        z_s = iaaft(z, rng, n_iter)
        ranks = np.empty(len(z_s), dtype=int)
        ranks[np.argsort(z_s, kind="stable")] = np.arange(len(z_s))
        s = real_sorted[ranks]
        assert np.array_equal(np.sort(s), real_sorted), "multiset identity violated"
        s_spear = acf(rankdata(s), lags)
        mismatches.append(float(np.max(np.abs(s_spear - real_spear))))
        surrogates.append(s)
    mm = np.array(mismatches)
    diag = dict(
        M=M, lags=lags, med=float(np.median(mm)), p95=float(np.percentile(mm, 95)),
        max=float(mm.max()),
        gate="PASS" if (np.median(mm) <= TOL_MED and np.percentile(mm, 95) <= TOL_P95) else "FAIL",
        tol_med=TOL_MED, tol_p95=TOL_P95,
    )
    return surrogates, diag


def rolling_pctl_strict_prior(x: np.ndarray, window: int, q: float) -> np.ndarray:
    n = len(x)
    out = np.full(n, np.nan)
    for i in range(window, n):
        out[i] = np.percentile(x[i - window:i], q * 100)
    return out


def rolling_pctl_through_today(x: np.ndarray, window: int, q: float) -> np.ndarray:
    n = len(x)
    out = np.full(n, np.nan)
    for i in range(window - 1, n):
        out[i] = np.percentile(x[i - window + 1:i + 1], q * 100)
    return out


def conditional_hit_rate_next(bias_series: np.ndarray, outcome_series: np.ndarray,
                               window: int, q_bias: float, q_ref: float):
    """bias_d = 1{bias_series[d] >= P_qbias(bias_series[d-window:d])} (strict prior).
    y_{d+1} = 1{outcome_series[d+1] > P_qref(outcome_series[d-window+1:d+1])} (through
    today). Returns (obs conditional hit rate, bias array, y array, scored mask)."""
    n = len(bias_series)
    bias_thresh = rolling_pctl_strict_prior(bias_series, window, q_bias)
    bias = (bias_series >= bias_thresh).astype(float)
    bias[np.isnan(bias_thresh)] = np.nan
    ref = rolling_pctl_through_today(outcome_series, window, q_ref)
    y = np.full(n, np.nan)
    y[:-1] = (outcome_series[1:] > ref[:-1]).astype(float)
    y[np.isnan(ref)] = np.nan
    scored = (~np.isnan(bias)) & (~np.isnan(y))
    b, yy = bias[scored].astype(int), y[scored].astype(int)
    m = b == 1
    obs = float(yy[m].mean()) if m.any() else float("nan")
    return obs, bias, y, scored


def block_bootstrap_ci(bias: np.ndarray, y: np.ndarray, block: int, n: int, seed: int,
                        q=(2.5, 97.5)):
    rng = np.random.default_rng(seed)
    N = len(bias)
    eff_block = block if N >= block + 1 else max(1, N // 2)
    nblocks = int(np.ceil(N / eff_block))
    pool = np.arange(0, N)
    stats = []
    for _ in range(n):
        st = rng.choice(pool, size=nblocks)
        idx = (st[:, None] + np.arange(eff_block)[None, :]) % N
        idx = idx.ravel()[:N]
        bb, yy = bias[idx], y[idx]
        m = bb == 1
        if m.any():
            stats.append(float(yy[m].mean()))
    stats = np.asarray(stats)
    lo, hi = np.percentile(stats, q)
    return float(lo), float(hi), int(len(stats))


def halves(bias: np.ndarray, y: np.ndarray):
    cond = np.where(bias == 1)[0]
    if len(cond) < 2:
        return float("nan"), float("nan")
    h = len(cond) // 2
    y_ord = y[cond]
    return float(y_ord[:h].mean()), float(y_ord[h:].mean())
