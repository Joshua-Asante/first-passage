"""SUPERSEDED DESIGN NOTE (2026-08-30, same session): this module originally
implemented a "linked-residual IAAFT" construction (normal-score both
channels, IAAFT channel 1, decompose channel 2 into a LAG-0 OLS residual on
channel 1, IAAFT the residual, recombine). Its own positive control
(positive_control.py) caught a real failure BEFORE any real-data scoring or
review: channel 2's own ACF mismatch badly failed the diagnostic gate (med
~0.14 vs a 0.04 tolerance) whenever the shared regime was highly persistent,
because a lag-0-only residual does not remove the shared regime's OWN serial
dependence from what gets IAAFT'd as "channel 2's own residual dynamics" --
the cross-covariance between channel 1 and the residual at NONZERO lags
(disclosed as a known gap in the original design, then found material)
leaks contaminated persistence into channel 2's reconstructed series.

Superseded below by a bivariate VAR(p) residual-bootstrap design (a
parametric-linear surrogate, not a Fourier-based one), which reproduces the
FULL linear dynamics -- each channel's own ACF at all lags AND the cross-lag
structure between channels -- by construction of the fitted model itself,
not as an approximation assembled from independently-generated pieces.

CONFOUND THIS ADDRESSES (D5 spec §4 / Q-RANGEXFER-1 §7): overnight_range and
RTH_range (or, for Q-VOLREGIME-1, bar-level volume and range) are two
DIFFERENT series measured the same day/bar, plausibly both driven by a
shared, slower-moving regime/volatility state. Stage-1's $0 falsifier
already controls for YESTERDAY's regime (day-history conditioning) and
finds overnight range still adds incremental lift beyond it. What stage-1
does NOT control for is TODAY's own shared regime: if both series are just
two noisy same-day measurements of one latent volatility factor, "overnight
range predicts RTH range" could be nothing more than "two measurements of
the same thing correlate," not a genuine transmission effect beyond ordinary
joint linear dynamics. Independent per-series surrogation (the existing
univariate IAAFT battery) would DELETE this same-day correlation entirely
and manufacture a guaranteed "excess" finding regardless of whether one
exists -- exactly the wrong null, which is why D5 named this design
UNRESOLVED rather than assuming the existing S1 machinery ports.

DESIGN -- bivariate VAR(p) residual-bootstrap:

  1. Normal-score BOTH series independently: z1 = normal_scores(series1),
     z2 = normal_scores(series2) (same rank-to-standard-normal convention as
     `iaaft_battery.normal_scores`, duplicated below with attribution).
  2. Fit a bivariate VAR(p) by OLS on Z_t = [z1_t, z2_t]: Z_t = c +
     sum_{k=1..p} A_k Z_{t-k} + e_t. This single fitted model captures BOTH
     channels' own linear autocorrelation (up to lag p) AND the full
     cross-lag linear dependence between channels (including any genuinely
     linear same-day OR lagged transmission effect present in the real
     data -- see the "WHAT THIS NULL ACTUALLY TESTS" section below for why
     that is the correct behavior, not a flaw).
  3. Bootstrap surrogate innovations by IID resampling of the FITTED
     residual PAIRS (e1_t, e2_t) with replacement -- preserves the
     residuals' own empirical joint (contemporaneous) distribution exactly,
     including whatever contemporaneous correlation survives after the VAR's
     own lagged structure is removed; IID resampling (not block resampling)
     is justified by, and gated on, a residual-autocorrelation diagnostic
     (below) confirming the VAR order actually whitens the residuals.
  4. Simulate the surrogate series forward using the FITTED coefficients and
     bootstrapped innovations, fixing the first p points to the real data's
     own first p values (a standard "fixed-design" VAR bootstrap start,
     avoiding a long burn-in and disclosed as such, not treated as a free
     assumption).
  5. Rank-remap each simulated channel onto that channel's own real sorted
     RAW values (exact multiset identity, same discipline the existing
     univariate IAAFT routine already applies).

WHAT THIS NULL ACTUALLY TESTS (important, disclosed precisely -- this differs
from the superseded design's framing and must not be conflated with it):
because VAR fitting does not distinguish "genuine linear transmission" from
"spurious linear regime co-movement" -- it fits whatever linear cross-lag
relationship exists in the real data, full stop -- a surrogate from the
FITTED VAR reproduces any REAL LINEAR (contemporaneous or lagged)
relationship between the two channels, by construction. This null therefore
tests: does the observed threshold/extreme-decile-conditioned incremental
lift (the actual H-RANGEXFER-1-class statistic, built from binary bias
indicators at extreme percentiles) exceed what a bivariate LINEAR-GAUSSIAN
joint dynamics model -- fit to reproduce the real data's own full linear
structure exactly -- would itself produce? This is a test for NONLINEAR or
TAIL-SPECIFIC dependence beyond ordinary linear co-movement (a standard,
meaningful question, analogous to testing for tail dependence beyond a
Gaussian copula), NOT a test for "any dependence beyond a single shared
factor." A real, PURELY LINEAR transmission effect (of any lag) would be
absorbed into the fitted VAR and would NOT be flagged as excess by this
null -- this is the correct, disclosed behavior, not a gap: if the observed
extreme-decile lift is entirely a byproduct of linear same-day/lagged
co-movement, "ordinary joint dynamics" is the right verdict, not "excess
transmission." Phase 2 review should confirm this framing is the one the
brief's H-RANGEXFER-1 / H-VOLREGIME-* actually intend to test.

DIAGNOSTIC GATE (computed before any hit rate, same two-phase discipline as
the frozen spec / existing univariate battery): each channel's own realized
ACF mismatch vs the real series (SAME tolerance numbers as
docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md §1, for
consistency -- not re-derived here), the realized lag-0 cross-correlation
mismatch (a new diagnostic this design introduces), AND a residual
autocorrelation check (max |ACF(residual)| at lags 1..5 <= 0.1, justifying
IID rather than block bootstrap of residual pairs -- if this fails, the
chosen VAR order `p` is too low and should be increased, not silently
tolerated).
"""
from __future__ import annotations

import numpy as np
from scipy.stats import rankdata, norm

ACF_LAGS = 30
TOL_MED, TOL_P95 = 0.04, 0.07          # own-ACF mismatch tolerance -- SAME numbers as
                                        # docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md
                                        # §1, reused for consistency, not re-derived here
TOL_CROSSCORR = 0.05                   # NEW diagnostic this design introduces -- not
                                        # borrowed from the frozen spec (which has no
                                        # multi-series analogue); a Phase 2 review item
TOL_RESID_ACF = 0.10                   # residual-whitening check gating IID (vs block) bootstrap
DEFAULT_VAR_ORDER = 20                 # ~1/3 of ACF_LAGS -- Phase 2 review item, not frozen


def normal_scores(x: np.ndarray) -> np.ndarray:
    """Verbatim from iaaft_battery.py (mym_mechanism_harvest_2026-08-29/), duplicated
    here with attribution rather than cross-directory-imported, matching this
    session's own precedent (candidate3_stratified_rerun.py duplicating
    circular_shift_null_p rather than importing across candidate directories)."""
    n = len(x)
    ranks = np.empty(n, dtype=float)
    ranks[np.argsort(x, kind="stable")] = np.arange(1, n + 1)
    return norm.ppf(ranks / (n + 1))


def acf(x: np.ndarray, max_lag: int) -> np.ndarray:
    """Verbatim from iaaft_battery.py."""
    xc = x - x.mean()
    denom = float(np.dot(xc, xc))
    return np.array([float(np.dot(xc[:-k], xc[k:]) / denom) for k in range(1, max_lag + 1)])


def fit_var(Z: np.ndarray, p: int):
    """Fit a bivariate VAR(p) by OLS. Z is (n,2). Returns (c, A_list, resid)
    where c is (2,), A_list is a list of p (2,2) matrices, resid is (n-p, 2)."""
    n = Z.shape[0]
    assert Z.shape[1] == 2
    X = np.ones((n - p, 1 + 2 * p))
    for k in range(1, p + 1):
        X[:, 1 + 2 * (k - 1): 1 + 2 * k] = Z[p - k: n - k]
    Y = Z[p:]
    B, *_ = np.linalg.lstsq(X, Y, rcond=None)   # B: (1+2p, 2)
    resid = Y - X @ B
    c = B[0]
    A_list = [B[1 + 2 * (k - 1): 1 + 2 * k].T for k in range(1, p + 1)]  # each (2,2): row=output channel
    return c, A_list, resid


def simulate_var(c, A_list, Z_init, resid_boot):
    """Simulate forward from fixed real initial values Z_init (p,2) using
    fitted (c, A_list) and a bootstrap draw of innovations resid_boot (n-p,2).
    Returns the full (n,2) simulated series (first p rows = Z_init, unchanged)."""
    p = len(A_list)
    n = p + resid_boot.shape[0]
    Z = np.empty((n, 2))
    Z[:p] = Z_init
    for t in range(p, n):
        val = c.copy()
        for k in range(1, p + 1):
            val = val + A_list[k - 1] @ Z[t - k]
        Z[t] = val + resid_boot[t - p]
    return Z


def joint_var_pair(x1: np.ndarray, x2: np.ndarray, rng: np.random.Generator,
                    p: int = DEFAULT_VAR_ORDER):
    """One joint surrogate DRAW via bivariate VAR(p) residual bootstrap.
    Returns (x1_surr, x2_surr, diagnostics_for_this_draw)."""
    n = len(x1)
    assert len(x2) == n
    z1 = normal_scores(x1)
    z2 = normal_scores(x2)
    Z = np.column_stack([z1, z2])
    c, A_list, resid = fit_var(Z, p)

    idx = rng.integers(0, resid.shape[0], size=resid.shape[0])  # IID pair bootstrap
    resid_boot = resid[idx]
    Z_surr = simulate_var(c, A_list, Z[:p], resid_boot)

    z1_surr, z2_surr = Z_surr[:, 0], Z_surr[:, 1]

    x1_sorted = np.sort(x1)
    ranks1 = np.empty(n, dtype=int)
    ranks1[np.argsort(z1_surr, kind="stable")] = np.arange(n)
    x1_surr = x1_sorted[ranks1]

    x2_sorted = np.sort(x2)
    ranks2 = np.empty(n, dtype=int)
    ranks2[np.argsort(z2_surr, kind="stable")] = np.arange(n)
    x2_surr = x2_sorted[ranks2]

    assert np.array_equal(np.sort(x1_surr), x1_sorted), "channel-1 multiset identity violated"
    assert np.array_equal(np.sort(x2_surr), x2_sorted), "channel-2 multiset identity violated"
    return x1_surr, x2_surr


def generate_joint_surrogates(x1: np.ndarray, x2: np.ndarray, M: int, seed_base: int,
                               code: int, p: int = DEFAULT_VAR_ORDER, acf_lags: int = ACF_LAGS):
    """Phase-1-design generator with a diagnostic gate computed BEFORE any hit
    rate is examined -- same two-phase discipline as the frozen spec / the
    existing univariate battery. Returns (surrogate_pairs, diagnostics)."""
    n = len(x1)
    lags = min(acf_lags, n // 3)
    real1_spear = acf(rankdata(x1), lags)
    real2_spear = acf(rankdata(x2), lags)
    real_crosscorr0 = float(np.corrcoef(rankdata(x1), rankdata(x2))[0, 1])

    # residual-whitening diagnostic (computed once, from the real-data fit)
    z1r, z2r = normal_scores(x1), normal_scores(x2)
    _, _, resid_fit = fit_var(np.column_stack([z1r, z2r]), p)
    resid_acf1 = np.max(np.abs(acf(resid_fit[:, 0], 5)))
    resid_acf2 = np.max(np.abs(acf(resid_fit[:, 1], 5)))
    resid_gate = "PASS" if max(resid_acf1, resid_acf2) <= TOL_RESID_ACF else "FAIL"

    pairs = []
    mism1, mism2, crosscorr_mism = [], [], []
    for i in range(M):
        rng = np.random.default_rng([seed_base, code, i])
        x1_s, x2_s = joint_var_pair(x1, x2, rng, p)
        pairs.append((x1_s, x2_s))
        s1_spear = acf(rankdata(x1_s), lags)
        s2_spear = acf(rankdata(x2_s), lags)
        mism1.append(float(np.max(np.abs(s1_spear - real1_spear))))
        mism2.append(float(np.max(np.abs(s2_spear - real2_spear))))
        surr_crosscorr0 = float(np.corrcoef(rankdata(x1_s), rankdata(x2_s))[0, 1])
        crosscorr_mism.append(abs(surr_crosscorr0 - real_crosscorr0))

    mism1, mism2 = np.array(mism1), np.array(mism2)
    crosscorr_mism = np.array(crosscorr_mism)
    diag = dict(
        M=M, lags=lags, var_order=p,
        channel1_acf=dict(med=float(np.median(mism1)), p95=float(np.percentile(mism1, 95))),
        channel2_acf=dict(med=float(np.median(mism2)), p95=float(np.percentile(mism2, 95))),
        crosscorr0=dict(real=real_crosscorr0, mean_abs_mismatch=float(crosscorr_mism.mean()),
                         p95_mismatch=float(np.percentile(crosscorr_mism, 95))),
        residual_whitening=dict(max_abs_acf_ch1=float(resid_acf1), max_abs_acf_ch2=float(resid_acf2),
                                 gate=resid_gate),
        gate_channel1_acf="PASS" if (np.median(mism1) <= TOL_MED and np.percentile(mism1, 95) <= TOL_P95) else "FAIL",
        gate_channel2_acf="PASS" if (np.median(mism2) <= TOL_MED and np.percentile(mism2, 95) <= TOL_P95) else "FAIL",
        gate_crosscorr0="PASS" if np.percentile(crosscorr_mism, 95) <= TOL_CROSSCORR else "FAIL",
        tol_med=TOL_MED, tol_p95=TOL_P95, tol_crosscorr=TOL_CROSSCORR, tol_resid_acf=TOL_RESID_ACF,
    )
    diag["gate"] = "PASS" if all(diag[k] == "PASS" for k in
                                  ("gate_channel1_acf", "gate_channel2_acf", "gate_crosscorr0")) and resid_gate == "PASS" else "FAIL"
    return pairs, diag
