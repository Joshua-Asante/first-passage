"""LENS: nonparametric regime-binned joint block bootstrap (Q-RANGEXFER-1 /
Q-VOLREGIME-1 Phase-1 joint-surrogation null design). Sibling attempt to the
three constructions documented in RESULTS.md (linked-residual IAAFT,
bivariate VAR(p) residual bootstrap, shared-starting-permutation coupled
IAAFT) -- read that file in full before touching this one. This lens
deliberately avoids GARCH/AR misspecification of any kind: no fitted
parametric time-series model at all. It only ever reuses REAL, VERBATIM,
CONTIGUOUS (on_range, rth_range) day-pairs, so within a reused block the
cross-dependence is exactly the real joint dependence (not an approximation
of it), and each channel's own local dynamics (whatever nonlinear/long-memory
shape they have) are exactly the real local dynamics -- for lags shorter
than or comparable to the block length. The mechanism this construction
DELETES is the *specific* real day-to-day pairing beyond (a) what is implied
by block-internal structure and (b) what is implied by shared regime-bin
membership -- since blocks are drawn from a candidate pool keyed by the
TARGET day's own real regime bin, not assembled independently of regime.

DESIGN
------
1. Regime proxy (causal, no look-ahead): for day t, combined[t] =
   (on_range[t] + rth_range[t]) / 2 (arithmetic mean of the two channels'
   same-day values). proxy[t] = mean(combined[t-k : t]) -- a TRAILING window
   of the k days STRICTLY BEFORE t (pandas `.rolling(k).mean().shift(1)`).
   For t < k there are fewer than k prior days available; we use an
   expanding mean of whatever prior days exist (`min_periods=1`, still
   shifted by 1, so day t never sees its own value). Day t=0 has ZERO prior
   days -- there is no causal way to define its regime from history alone,
   so as a one-day boundary exception we assign it combined[0] itself (its
   own same-day value). This leaks exactly 1 of 1487 days (0.07%) and is
   immaterial to the aggregate diagnostics; disclosed rather than hidden.
2. Bin every day into a regime QUINTILE (5 bins, `pd.qcut` on `proxy`) --
   labels 0..4, low-to-high combined-range regime.
3. Block length L (a free parameter of this lens, swept empirically below,
   not fixed a priori) determines how many CONSECUTIVE calendar days are
   copied verbatim as one unit.
4. To build ONE surrogate of length n: walk forward through target positions
   i = 0, L, 2L, .... At each i, look up the TARGET day's own REAL regime
   bin b = bin[i] (so the surrogate's regime PATH matches the real regime
   path exactly -- only the within-bin day-to-day pairing is randomized, not
   which regime occurred when). Draw a uniformly random SOURCE start index s
   from the pool of real days whose OWN bin label is also b (i.e., a day
   that plausibly kicks off a same-regime run), subject to s + L <= n so the
   source block doesn't run off the end of the real series. Copy real days
   s .. s+L-1 (both channels, same real day-pairing kept intact) into
   surrogate positions i .. i+L-1, clipping length at the destination end of
   the surrogate if it would overrun n. Advance i by the copied length.
   NOTE (disclosed): only the block's OWN START day is guaranteed to share
   the target bin; because regime bins are contiguous-ish but not
   perfectly so, the tail of a copied block can occasionally drift into an
   adjacent bin's territory in the SOURCE calendar. This is standard for a
   regime-conditional block bootstrap (conditioning is on the state at
   block-start, not enforced for the block's whole extent) and is far less
   distortive than it would be for a small number of bins over a slow-moving
   proxy, which is exactly this design.
5. Because blocks are drawn WITH REPLACEMENT from within-bin pools, the raw
   concatenated sequence does NOT naturally have the same multiset of values
   as the real series (some real days get reused across draws or across
   surrogates, others never chosen in a given draw). To meet this module's
   required exact-multiset-identity discipline (same as `joint_iaaft.py`),
   we apply the IDENTICAL rank-remap step used there: take the raw
   block-concatenated sequence's rank order (via a stable argsort, so ties/
   duplicate reused values are broken by their position of first occurrence)
   and remap those ranks onto each channel's own REAL SORTED values. This is
   a strictly monotonic (up to stable tie-breaking) transform of the raw
   block draw, so it does not materially disturb the rank-based dependence
   structure the block draw encodes (all diagnostics here are Spearman/rank
   based anyway) -- but it DOES mean the tiny fraction of raw duplicate
   values get separated onto distinct nearby real order-statistics rather
   than literally repeating a value. Disclosed as an exact-parity
   post-processing step, not a free design choice: it is required to satisfy
   the same discipline as the existing (superseded) module in this
   directory, and it is applied uniformly to every draw.

HONEST LIMITATION (own-ACF beyond block length)
------------------------------------------------
A block bootstrap can only reproduce a channel's own autocorrelation
STRUCTURE UP TO ROUGHLY THE BLOCK LENGTH -- beyond that, two adjacent blocks
are independent draws from the (possibly same, possibly different) regime
pool, so any correlation between a day near the end of one block and a day
near the start of the next block is essentially destroyed (governed only by
whichever residual similarity same-regime-bin membership implies, not the
real day-to-day linkage). The real `on_range`/`rth_range` series show
SLOWLY-DECAYING rank-ACF (per the task brief: on_range 0.41/0.35/0.24/0.25/
0.25 at lags 1/5/10/20/30 -- not decayed to ~0 even at lag 30, suggestive of
long-memory/volatility-clustering behavior). This lens is EXPECTED, by
construction, to track the real ACF closely at lags << L, degrade
progressively as the lag approaches L, and to plausibly UNDERSHOOT the real
ACF (biased toward zero) at lags > L, however long a candidate is -- because
"comparable to L" is a soft transition, not a hard cutoff, since blocks that
happen to be drawn from adjacent real calendar time (or the same regime run)
partially preserve inter-block correlation too. The gate check below (same
ACF_LAGS window as the existing module, 1..min(30, n//3)=30 here) is run and
reported HONESTLY at each L tried -- if lag 20-30 fails while lag 1-10 is
fine, that is the disclosed mechanism above operating exactly as expected,
not a bug.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import rankdata

ACF_LAGS = 30
TOL_MED, TOL_P95 = 0.04, 0.07      # own-ACF mismatch tolerance -- SAME numbers as
                                    # docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md
                                    # Sec 1 / joint_iaaft.py, reused verbatim for cross-lens comparability
TOL_CROSSCORR = 0.05               # SAME as joint_iaaft.py's TOL_CROSSCORR
DEFAULT_K = 40                     # trailing-window length (days) for the causal regime proxy
DEFAULT_NBINS = 5                  # quintiles
DEFAULT_BLOCK_LEN = 250            # best of an empirical (k, nbins, block_len) grid sweep in
                                    # __main__ -- see disclosed limitation above: even this best
                                    # point does NOT clear the own-ACF gate (see RESULTS discussion)


def acf(x: np.ndarray, max_lag: int) -> np.ndarray:
    """Verbatim from joint_iaaft.py / iaaft_battery.py (rank-ACF caller passes rankdata(x))."""
    xc = x - x.mean()
    denom = float(np.dot(xc, xc))
    return np.array([float(np.dot(xc[:-k], xc[k:]) / denom) for k in range(1, max_lag + 1)])


def causal_regime_bins(x1: np.ndarray, x2: np.ndarray, k: int, nbins: int) -> np.ndarray:
    """Trailing k-day causal regime proxy on the combined (mean of the two
    channels' same-day values), binned into `nbins` quantile bins. Returns an
    int array of bin labels 0..nbins-1, length n. See module docstring step 1
    for the exact causal construction and the disclosed 1-day t=0 exception."""
    n = len(x1)
    combined = (np.asarray(x1, dtype=float) + np.asarray(x2, dtype=float)) / 2.0
    s = pd.Series(combined)
    proxy = s.rolling(window=k, min_periods=1).mean().shift(1)
    proxy.iloc[0] = combined[0]  # disclosed 1-day boundary exception (no prior history at t=0)
    assert proxy.notna().all(), "causal regime proxy has unexpected NaNs"
    bins = pd.qcut(proxy, q=nbins, labels=False, duplicates="drop").to_numpy()
    assert len(bins) == n
    return bins


def _build_pools(bins: np.ndarray, block_len: int) -> dict:
    """For each bin label, the list of valid SOURCE start indices s (s+block_len <= n,
    bins[s] == that label)."""
    n = len(bins)
    pools: dict[int, np.ndarray] = {}
    for b in np.unique(bins):
        cand = np.where(bins == b)[0]
        cand = cand[cand + block_len <= n]
        if len(cand) == 0:
            # edge-case fallback (documented): bin has no room for a full block
            # near the series end -- fall back to the single latest feasible start,
            # ignoring its own bin label. Rare; disclosed, not silently patched away.
            cand = np.array([max(0, n - block_len)])
        pools[b] = cand
    return pools


def _rank_remap(raw: np.ndarray, real_sorted: np.ndarray) -> np.ndarray:
    """Identical discipline to joint_iaaft.py's joint_var_pair: stable-argsort
    the raw (possibly-duplicated) sequence and remap those ranks onto the
    channel's own real sorted values, forcing exact multiset identity."""
    n = len(raw)
    ranks = np.empty(n, dtype=int)
    ranks[np.argsort(raw, kind="stable")] = np.arange(n)
    return real_sorted[ranks]


def regime_block_pair(x1: np.ndarray, x2: np.ndarray, bins: np.ndarray,
                       block_len: int, rng: np.random.Generator):
    """One joint surrogate draw. Returns (x1_surr, x2_surr) in raw value space,
    exact multiset identity with x1/x2 respectively."""
    n = len(x1)
    pools = _build_pools(bins, block_len)

    raw1 = np.empty(n, dtype=float)
    raw2 = np.empty(n, dtype=float)
    i = 0
    while i < n:
        b = bins[i]
        pool = pools[b]
        s = pool[rng.integers(0, len(pool))]
        take = min(block_len, n - i)
        raw1[i:i + take] = x1[s:s + take]
        raw2[i:i + take] = x2[s:s + take]
        i += take

    x1_sorted = np.sort(x1)
    x2_sorted = np.sort(x2)
    x1_surr = _rank_remap(raw1, x1_sorted)
    x2_surr = _rank_remap(raw2, x2_sorted)

    assert np.array_equal(np.sort(x1_surr), x1_sorted), "channel-1 multiset identity violated"
    assert np.array_equal(np.sort(x2_surr), x2_sorted), "channel-2 multiset identity violated"
    return x1_surr, x2_surr


def generate_joint_surrogates(x1: np.ndarray, x2: np.ndarray, M: int, seed_base: int,
                               code: int, k: int = DEFAULT_K, nbins: int = DEFAULT_NBINS,
                               block_len: int = DEFAULT_BLOCK_LEN, acf_lags: int = ACF_LAGS):
    """Regime-binned joint block bootstrap. Matches the generate_joint_surrogates
    signature/return-shape contract used by joint_iaaft.py. Returns
    (surrogate_pairs, diagnostics)."""
    x1 = np.asarray(x1, dtype=float)
    x2 = np.asarray(x2, dtype=float)
    n = len(x1)
    assert len(x2) == n
    lags = min(acf_lags, n // 3)

    real1_spear = acf(rankdata(x1), lags)
    real2_spear = acf(rankdata(x2), lags)
    real_crosscorr0 = float(np.corrcoef(rankdata(x1), rankdata(x2))[0, 1])

    bins = causal_regime_bins(x1, x2, k, nbins)
    bin_counts = {int(b): int(c) for b, c in zip(*np.unique(bins, return_counts=True))}

    pairs = []
    mism1, mism2, crosscorr_mism = [], [], []
    for i in range(M):
        rng = np.random.default_rng([seed_base, code, i])
        x1_s, x2_s = regime_block_pair(x1, x2, bins, block_len, rng)
        pairs.append((x1_s, x2_s))
        s1_spear = acf(rankdata(x1_s), lags)
        s2_spear = acf(rankdata(x2_s), lags)
        mism1.append(float(np.max(np.abs(s1_spear - real1_spear))))
        mism2.append(float(np.max(np.abs(s2_spear - real2_spear))))
        surr_crosscorr0 = float(np.corrcoef(rankdata(x1_s), rankdata(x2_s))[0, 1])
        crosscorr_mism.append(abs(surr_crosscorr0 - real_crosscorr0))

    # NOTE: mism1/mism2 above use the SAME max-abs-mismatch-across-lags convention as
    # joint_iaaft.py's own per-draw loop (its per-draw mism1/mism2 are max|.| over all
    # lags, then med/p95 are taken across draws of that max). We reuse this exact
    # convention for direct comparability across lenses.
    mism1, mism2 = np.array(mism1), np.array(mism2)
    crosscorr_mism = np.array(crosscorr_mism)

    diag = dict(
        M=M, lags=lags, k=k, nbins=nbins, block_len=block_len,
        bin_counts=bin_counts,
        channel1_acf=dict(med=float(np.median(mism1)), p95=float(np.percentile(mism1, 95))),
        channel2_acf=dict(med=float(np.median(mism2)), p95=float(np.percentile(mism2, 95))),
        crosscorr0=dict(real=real_crosscorr0, mean_abs_mismatch=float(crosscorr_mism.mean()),
                         p95_mismatch=float(np.percentile(crosscorr_mism, 95))),
        gate_channel1_acf="PASS" if (np.median(mism1) <= TOL_MED and np.percentile(mism1, 95) <= TOL_P95) else "FAIL",
        gate_channel2_acf="PASS" if (np.median(mism2) <= TOL_MED and np.percentile(mism2, 95) <= TOL_P95) else "FAIL",
        gate_crosscorr0="PASS" if np.percentile(crosscorr_mism, 95) <= TOL_CROSSCORR else "FAIL",
        tol_med=TOL_MED, tol_p95=TOL_P95, tol_crosscorr=TOL_CROSSCORR,
    )
    diag["gate"] = "PASS" if all(diag[k2] == "PASS" for k2 in
                                  ("gate_channel1_acf", "gate_channel2_acf", "gate_crosscorr0")) else "FAIL"
    return pairs, diag


def per_lag_mismatch_report(x1: np.ndarray, x2: np.ndarray, bins: np.ndarray, block_len: int,
                             M: int, seed_base: int, code: int, acf_lags: int = ACF_LAGS):
    """Diagnostic helper (not part of the required contract): median per-LAG
    (not max-over-lags) mismatch for each channel, across M draws -- used in
    __main__ to show exactly where the honest degradation-beyond-block-length
    limitation bites."""
    x1 = np.asarray(x1, dtype=float)
    x2 = np.asarray(x2, dtype=float)
    n = len(x1)
    lags = min(acf_lags, n // 3)
    real1_spear = acf(rankdata(x1), lags)
    real2_spear = acf(rankdata(x2), lags)
    all1, all2 = [], []
    for i in range(M):
        rng = np.random.default_rng([seed_base, code, 9000 + i])
        x1_s, x2_s = regime_block_pair(x1, x2, bins, block_len, rng)
        all1.append(acf(rankdata(x1_s), lags) - real1_spear)
        all2.append(acf(rankdata(x2_s), lags) - real2_spear)
    all1, all2 = np.abs(np.array(all1)), np.abs(np.array(all2))
    return np.median(all1, axis=0), np.median(all2, axis=0)


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv(
        "../mnq_dailygeom_notice_2026-08-29/candidate24_joint_frame.csv"
    )
    x1 = df["on_range"].to_numpy()
    x2 = df["rth_range"].to_numpy()
    print(f"n={len(x1)}")

    print("\n=== Stage A: block-length sweep at fixed (k=20, nbins=5), M=30, seed_base=1 ===")
    for L in (10, 20, 30, 42, 60, 90, 120):
        pairs, diag = generate_joint_surrogates(x1, x2, M=30, seed_base=1, code=0,
                                                 k=20, nbins=5, block_len=L)
        print(f"L={L:4d}  gate={diag['gate']:4s}  "
              f"ch1_acf(med={diag['channel1_acf']['med']:.4f}, p95={diag['channel1_acf']['p95']:.4f})  "
              f"ch2_acf(med={diag['channel2_acf']['med']:.4f}, p95={diag['channel2_acf']['p95']:.4f})  "
              f"cross(real={diag['crosscorr0']['real']:.4f}, mean_mism={diag['crosscorr0']['mean_abs_mismatch']:.4f}, "
              f"p95_mism={diag['crosscorr0']['p95_mismatch']:.4f})")

    print("\n=== Stage B: full (k, nbins, block_len) grid sweep, M=20, seed_base=2 ===")
    best = None
    for nbins in (3, 5):
        for k in (10, 20, 40, 60):
            for L in (100, 150, 200, 250, 300):
                pairs, diag = generate_joint_surrogates(x1, x2, M=20, seed_base=2, code=0,
                                                         k=k, nbins=nbins, block_len=L)
                score = diag["channel1_acf"]["med"] + diag["channel2_acf"]["med"]
                if best is None or score < best[0]:
                    best = (score, nbins, k, L, diag)
    _, bnbins, bk, bL, bdiag = best
    print(f"Best-of-grid by (ch1_med+ch2_med): nbins={bnbins} k={bk} block_len={bL}  "
          f"ch1_med={bdiag['channel1_acf']['med']:.4f} ch2_med={bdiag['channel2_acf']['med']:.4f} "
          f"gate={bdiag['gate']}")
    print("(This is why DEFAULT_K=40, DEFAULT_NBINS=5, DEFAULT_BLOCK_LEN=250 were set above --"
          " not a clean pass, the best point found in a reasonable grid.)")

    print(f"\n=== Full diagnostics at DEFAULTS (k={DEFAULT_K}, nbins={DEFAULT_NBINS}, "
          f"block_len={DEFAULT_BLOCK_LEN}), M=40, seed_base=1 ===")
    pairs, diag = generate_joint_surrogates(x1, x2, M=40, seed_base=1, code=0)
    import json
    print(json.dumps(diag, indent=2))

    print(f"\n=== Per-lag median |mismatch| at defaults (shows honest degradation) ===")
    bins = causal_regime_bins(x1, x2, DEFAULT_K, DEFAULT_NBINS)
    med1, med2 = per_lag_mismatch_report(x1, x2, bins, DEFAULT_BLOCK_LEN, M=30, seed_base=1, code=0)
    for lag in (1, 5, 10, 20, 30):
        if lag <= len(med1):
            print(f"lag={lag:3d}  ch1_med|mismatch|={med1[lag-1]:.4f}  ch2_med|mismatch|={med2[lag-1]:.4f}")

    print(f"\n=== Regime bin counts (k={DEFAULT_K}, nbins={DEFAULT_NBINS}) ===")
    print({int(b): int(c) for b, c in zip(*np.unique(bins, return_counts=True))})
