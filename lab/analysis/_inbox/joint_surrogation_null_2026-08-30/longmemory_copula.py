"""LONG-MEMORY (fractionally-integrated) MARGINALS + GAUSSIAN-COPULA LINKING.

Panel lens for Q-RANGEXFER-1 Phase-1 joint-surrogation null design. Reads
RESULTS.md's account of three prior failed constructions (linked-residual
IAAFT, bivariate VAR(p) residual bootstrap, shared-starting-permutation
coupled IAAFT) before designing this. Does NOT repeat any of the three.

MOTIVATION: the real on_range/rth_range series' own rank-ACF does not decay
to ~0 by lag 30 (stays ~0.24-0.25 from lag 10 through lag 30 -- see
diagnostics below), consistent with long-memory / fractionally-integrated
dynamics (ARFIMA(0,d,0)-type slow hyperbolic decay), NOT a short-memory
linear AR/VAR process. RESULTS.md's own VAR(p) attempt directly confirmed
this: own-ACF mismatch does NOT improve from p=20 to p=40, meaning the gap
is a functional-form mismatch (finite linear AR order cannot reproduce
hyperbolic decay), not an order-selection problem. This lens targets that
functional-form gap directly: an ARFIMA(0,d,0)-consistent linear filter with
d estimated from the real decay rate, which has genuine long-range
dependence built into its transfer function (infinite-order MA in the
fractional-difference filter, psi_j ~ j^(d-1) decay) rather than a truncated
finite AR/VAR expansion.

DESIGN -- two variants tried, in order (per the task's own escalation
license: iterate on parameters/copula construction within this lens if the
first attempt fails; do not switch lens):

VARIANT A -- "rank_reorder" (literal Iman-Conover, as originally specified):
  1. Estimate d1, d2 for each normal-scored channel via grid search matching
     the theoretical ARFIMA(0,d,0) autocorrelation function
     rho(h) = Gamma(h+d)Gamma(1-d) / [Gamma(h-d+1)Gamma(d)] against the real
     rank-ACF at lags 1..min(30, n//3).
  2. Generate each channel's marginal surrogate INDEPENDENTLY: filter fresh
     iid Gaussian white noise through the truncated fractional-differencing
     filter psi_j = Gamma(j+d)/[Gamma(d)Gamma(j+1)], j=0..J-1, with burn-in
     to avoid a cold-start transient.
  3. Build an iid bivariate-normal REFERENCE pair (r1, r2) with the Pearson
     correlation equivalent (2*sin(pi*rho_s/6)) of the real rank
     cross-correlation rho_s.
  4. Reorder each channel's independent long-memory draw into the RANK ORDER
     of its reference column (textbook Iman-Conover): this induces the
     target rank correlation between the two channels' FINAL sequences.
  DISCLOSED, EXPECTED FAILURE MODE (same caveat class as RESULTS.md's
  shared-starting-permutation IAAFT attempt): the rank-reorder step is a
  time-index PERMUTATION driven by an iid (no own memory) reference. It
  necessarily scrambles whatever time-ordering produced each channel's own
  long-memory ACF -- the marginal VALUES are exactly right (same realized
  set, rank-remapped later onto the real raw values), but the SEQUENCE in
  which they occur is reshuffled toward whatever order the iid reference
  happens to want, destroying serial dependence. This is measured, not
  assumed -- see VARIANT A diagnostics below, run against the real data.

VARIANT B -- "innovation_link" (the iteration after Variant A's measured
failure; still a Gaussian-copula construction, just applied at the
INNOVATION level instead of via post-hoc rank reordering -- a copula-family
change within this lens, not a different lens):
  1. Same per-channel d1, d2 estimation as Variant A.
  2. Instead of two INDEPENDENT noise streams, draw one bivariate Gaussian
     white-noise pair (e1_t, e2_t) correlated CONTEMPORANEOUSLY (same t) with
     correlation rho_innov, independent across t (a Gaussian copula linking
     the two channels' innovation processes at each time step, i.e. a
     copula applied to the noise BEFORE fractional filtering rather than to
     the final values AFTER).
  3. Filter e1 through psi1 (channel 1's own d) and e2 through psi2
     (channel 2's own d) -- unchanged, deterministic linear filters, so
     each channel's own ACF is a property of its own psi weights alone and
     is NOT touched by rho_innov.
  4. Because filtering is linear, the lag-0 cross-correlation of the two
     filtered series has a closed form:
         corr(X1,X2) = rho_innov * sum_j(psi1_j*psi2_j)
                       / sqrt(sum_j psi1_j^2 * sum_j psi2_j^2)
     so rho_innov is solved analytically (once, from the real target
     correlation) rather than searched.
  This keeps each channel's own dynamics EXACTLY the same linear
  fractional-integration process used in Variant A (whose own-ACF quality
  is unaffected by rho_innov by construction) while inducing the
  cross-channel link through the shared innovation copula instead of a
  rank permutation -- the mechanism that broke Variant A.

Both variants reuse `normal_scores` and `acf` VERBATIM from joint_iaaft.py
(duplicated here with attribution, matching that module's own precedent of
duplicating from iaaft_battery.py rather than cross-directory-importing),
and the SAME tolerance constants (TOL_MED, TOL_P95, TOL_CROSSCORR) -- not
re-derived here.

WHAT THIS NULL ACTUALLY TESTS: same framing as joint_iaaft.py's VAR(p)
design, generalized from "linear at a finite lag order" to "linear
fractionally-integrated" -- a surrogate from this construction reproduces
any dependence expressible as (a) each channel's own long-memory linear
dynamics and (b) a CONSTANT (lag-0, Gaussian-copula) contemporaneous linear
link between channels. It does NOT and cannot reproduce genuine LAGGED
transmission (overnight range at day t predicting RTH range at day t
specifically, beyond a same-day linear copula link) or NONLINEAR /
regime-dependent linkage. A real observed stage-1 lift that exceeds this
null is evidence of something beyond "two long-memory series with a
constant linear same-day coupling" -- narrower than "any dependence beyond
independence," and this narrowing should be confirmed against the brief's
actual H-RANGEXFER-1 statistic definition at Phase 2, exactly as
joint_iaaft.py's docstring flags for its own construction.
"""
from __future__ import annotations

import numpy as np
from scipy.stats import rankdata, norm
from scipy.special import gammaln
from scipy.signal import fftconvolve

ACF_LAGS = 30
TOL_MED, TOL_P95 = 0.04, 0.07     # own-ACF mismatch tolerance -- SAME as joint_iaaft.py / frozen spec
TOL_CROSSCORR = 0.05              # SAME as joint_iaaft.py -- not re-derived here


def normal_scores(x: np.ndarray) -> np.ndarray:
    """Average-rank tie-breaking (Codex review, PR #219) -- see joint_iaaft.py's
    own normal_scores docstring for the full rationale (ordinal ties invent a
    spurious time ordering; this module's own diagnostics already use
    rankdata's average-tie convention)."""
    n = len(x)
    ranks = rankdata(x, method="average")
    return norm.ppf(ranks / (n + 1))


def acf(x: np.ndarray, max_lag: int) -> np.ndarray:
    """Verbatim from joint_iaaft.py / iaaft_battery.py."""
    xc = x - x.mean()
    denom = float(np.dot(xc, xc))
    return np.array([float(np.dot(xc[:-k], xc[k:]) / denom) for k in range(1, max_lag + 1)])


# ---------------------------------------------------------------------------
# Fractional-integration machinery
# ---------------------------------------------------------------------------

def arfima_theoretical_acf(d: float, max_lag: int) -> np.ndarray:
    """Theoretical ARFIMA(0,d,0) autocorrelation at lags 1..max_lag:
    rho(h) = Gamma(h+d) Gamma(1-d) / [Gamma(h-d+1) Gamma(d)], via gammaln
    for numerical stability (avoids overflow for large h). Kept for
    reference/diagnostics; superseded as the FIT target by the
    ARFIMA(1,d,0) numeric-filter fit below once a pure d=0-AR fit was found
    (see MODEL UPGRADE note on estimate_phi_d) not to track the real ACF's
    shape well enough for the diagnostic gate."""
    h = np.arange(1, max_lag + 1, dtype=float)
    log_rho = gammaln(h + d) - gammaln(h - d + 1) + gammaln(1 - d) - gammaln(d)
    return np.exp(log_rho)


def estimate_d(real_acf: np.ndarray, d_grid: np.ndarray | None = None) -> tuple[float, dict]:
    """Grid search over d in (0, 0.499] minimizing SSE between the
    theoretical ARFIMA(0,d,0) ACF and the real empirical rank-ACF, at every
    lag the empirical ACF was computed on (lags 1..len(real_acf)). Kept for
    reference (first-attempt fit); see estimate_phi_d for the fit actually
    used by generate_joint_surrogates."""
    if d_grid is None:
        d_grid = np.linspace(0.001, 0.499, 999)
    max_lag = len(real_acf)
    best_d, best_sse = None, np.inf
    for d in d_grid:
        theo = arfima_theoretical_acf(d, max_lag)
        sse = float(np.sum((theo - real_acf) ** 2))
        if sse < best_sse:
            best_sse, best_d = sse, d
    info = dict(best_sse=best_sse, d_grid_lo=float(d_grid[0]), d_grid_hi=float(d_grid[-1]),
                n_grid=len(d_grid))
    return float(best_d), info


def compute_filter_acf(psi: np.ndarray, max_lag: int) -> np.ndarray:
    """Numeric autocorrelation at lags 1..max_lag of an MA(inf) linear
    process X_t = sum_j psi_j * e_{t-j} (iid unit-variance e), from the
    TRUNCATED psi array actually used for simulation -- gamma(h) =
    sum_{j=0}^{len(psi)-1-h} psi[j]*psi[j+h], rho(h)=gamma(h)/gamma(0). Using
    the truncated psi (not a closed-form infinite-lag formula) means the FIT
    target already reflects whatever truncation bias the simulation itself
    will carry, rather than fitting against an idealized infinite-order
    curve the simulated draws could never exactly reach."""
    g0 = float(np.dot(psi, psi))
    out = np.empty(max_lag)
    for h in range(1, max_lag + 1):
        out[h - 1] = float(np.dot(psi[:-h], psi[h:])) / g0
    return out


def ar1_fracdiff_weights(phi: float, d: float, J: int) -> np.ndarray:
    """MA(inf) coefficients (truncated to length J) of an ARFIMA(1,d,0)
    process: (1 - phi*L) X_t = (1-L)^(-d) e_t, i.e. psi = ar1_weights *
    frac_weights (convolution), truncated to the first J terms. Adding the
    single AR(1) root on top of the pure fractional-noise filter lets the
    model capture a SHARP initial decay (real lag-1 ACF ~0.41 dropping to
    ~0.35 by lag 5) simultaneously with a slowly-decaying persistent floor
    (~0.22-0.25 through lag 30) -- pure ARFIMA(0,d,0) (see MODEL UPGRADE
    note) cannot do both with one parameter: the single d that best matches
    the lag-10..30 floor over-predicts lag-1 by ~0.13, already exceeding the
    0.07 p95 tolerance before any simulation noise is added."""
    ar1 = phi ** np.arange(J, dtype=float)
    frac = fracdiff_weights(d, J)
    full = fftconvolve(ar1, frac)
    return full[:J]


def estimate_phi_d(real_acf: np.ndarray, J_fit: int = 1000,
                    phi_grid: np.ndarray | None = None,
                    d_grid: np.ndarray | None = None) -> tuple[float, float, dict]:
    """MODEL UPGRADE (this session, after the pure-d fit above measurably
    failed the diagnostic gate on real data -- see RESULTS.md/this file's own
    run log): joint 2-D grid search over (phi, d) for an ARFIMA(1,d,0)
    filter, minimizing SSE between compute_filter_acf(that filter) and the
    real empirical rank-ACF at every lag 1..len(real_acf). Still squarely
    inside the long-memory/fractional-differencing lens (ARFIMA(1,d,0) is
    the standard ARFIMA family with p=1, not a different model class) --
    this is the "iterate on parameters within your own lens" escalation the
    task license anticipates, not a lens switch."""
    if phi_grid is None:
        phi_grid = np.linspace(-0.6, 0.9, 61)
    if d_grid is None:
        d_grid = np.linspace(0.01, 0.48, 48)
    max_lag = len(real_acf)
    best = (None, None, np.inf)
    for phi in phi_grid:
        for d in d_grid:
            psi = ar1_fracdiff_weights(phi, d, J_fit)
            theo = compute_filter_acf(psi, max_lag)
            sse = float(np.sum((theo - real_acf) ** 2))
            if sse < best[2]:
                best = (phi, d, sse)
    phi_best, d_best, sse_best = best
    info = dict(best_sse=sse_best, J_fit=J_fit,
                phi_grid_lo=float(phi_grid[0]), phi_grid_hi=float(phi_grid[-1]), n_phi=len(phi_grid),
                d_grid_lo=float(d_grid[0]), d_grid_hi=float(d_grid[-1]), n_d=len(d_grid))
    return float(phi_best), float(d_best), info


def estimate_phi_d_simulated(real_acf: np.ndarray, n: int, J: int, burn: int,
                              n_reps: int = 5, seed: int = 12345,
                              phi_grid: np.ndarray | None = None,
                              d_grid: np.ndarray | None = None) -> tuple[float, float, dict]:
    """SECOND MODEL UPGRADE (this session): estimate_phi_d fits (phi,d) to
    the INFINITE-SAMPLE theoretical ACF of the composite filter -- but a
    length-n=1487 realization of a near-nonstationary long-memory process
    (d approx 0.4, close to the d=0.5 boundary) has a well-known LARGE
    negative finite-sample bias in its own rank-ACF estimate, worsening with
    lag (measured directly here: at the estimate_phi_d fit, the finite-n
    simulated mean ACF undershoots both the real data's ACF and the fitted
    filter's own infinite-sample theoretical ACF by ~0.05-0.10 at lags
    15-30 -- see this file's own run log). Matching a theoretical
    infinite-sample curve to a biased finite-sample estimate, then drawing
    finite-length surrogates from it, compounds that bias rather than
    correcting it.

    This function instead calibrates (phi,d) via INDIRECT INFERENCE /
    simulated method of moments: for each candidate (phi,d), simulate
    `n_reps` independent length-n realizations (same n, J, burn the FINAL
    surrogates will use) and compare the AVERAGE realized finite-sample ACF
    to the real data's ACF -- so whatever finite-sample bias the simulation
    procedure itself carries is present on both sides of the comparison and
    the fit targets what the generator can actually deliver at this n, not
    an idealized infinite-sample curve it cannot reach in a finite draw."""
    if phi_grid is None:
        phi_grid = np.linspace(-0.6, 0.9, 31)
    if d_grid is None:
        d_grid = np.linspace(0.01, 0.499, 50)
    max_lag = len(real_acf)
    rng = np.random.default_rng(seed)
    best = (None, None, np.inf)
    for phi in phi_grid:
        for d in d_grid:
            psi = ar1_fracdiff_weights(phi, d, J)
            acc = np.zeros(max_lag)
            for _ in range(n_reps):
                e = rng.standard_normal(n + burn)
                y = _causal_filter(e, psi)[burn: burn + n]
                acc += acf(rankdata(y), max_lag)
            mean_acf = acc / n_reps
            sse = float(np.sum((mean_acf - real_acf) ** 2))
            if sse < best[2]:
                best = (phi, d, sse)
    phi_best, d_best, sse_best = best
    info = dict(best_sse=sse_best, n_reps=n_reps, J=J, burn=burn,
                phi_grid_lo=float(phi_grid[0]), phi_grid_hi=float(phi_grid[-1]), n_phi=len(phi_grid),
                d_grid_lo=float(d_grid[0]), d_grid_hi=float(d_grid[-1]), n_d=len(d_grid),
                method="simulation_calibrated")
    return float(phi_best), float(d_best), info


def fracdiff_weights(d: float, J: int) -> np.ndarray:
    """psi_j = Gamma(j+d) / [Gamma(d) Gamma(j+1)], j=0..J-1 (the MA(inf)
    coefficients of the fractional-differencing filter (1-L)^(-d)), via
    gammaln for stability. psi_0 = 1 always."""
    j = np.arange(J, dtype=float)
    log_psi = gammaln(j + d) - gammaln(d) - gammaln(j + 1)
    return np.exp(log_psi)


def _causal_filter(noise: np.ndarray, psi: np.ndarray) -> np.ndarray:
    """y[t] = sum_{k=0}^{len(psi)-1} psi[k] * noise[t-k], noise[negative]=0
    (zero initial condition), via FFT convolution. Returns len(noise) values;
    the first len(psi)-1 carry a startup transient (missing pre-sample
    history) and MUST be discarded by the caller via a burn-in window."""
    full = fftconvolve(noise, psi, mode="full")
    return full[: len(noise)]


def _simulate_channel_from_psi(psi: np.ndarray, n: int, burn: int, e: np.ndarray) -> np.ndarray:
    """Filter a length-(n+burn) noise stream through a precomputed composite
    ARFIMA(1,d,0) filter `psi`, discard the first `burn` (transient-affected)
    outputs, return the trailing n values (full filter memory support,
    since burn >= J-1)."""
    y = _causal_filter(e, psi)
    return y[burn: burn + n]


# ---------------------------------------------------------------------------
# Rank-remap to raw values (exact multiset identity -- same discipline as
# joint_iaaft.py / iaaft_battery.py)
# ---------------------------------------------------------------------------

def _remap_to_raw(z_surr: np.ndarray, x_raw: np.ndarray) -> np.ndarray:
    n = len(x_raw)
    x_sorted = np.sort(x_raw)
    ranks = np.empty(n, dtype=int)
    ranks[np.argsort(z_surr, kind="stable")] = np.arange(n)
    x_surr = x_sorted[ranks]
    assert np.array_equal(np.sort(x_surr), x_sorted), "channel multiset identity violated"
    return x_surr


# ---------------------------------------------------------------------------
# VARIANT A -- rank_reorder (literal Iman-Conover)
# ---------------------------------------------------------------------------

def _pair_rank_reorder(x1, x2, psi1, psi2, J, burn, rng, target_pearson):
    n = len(x1)
    e1 = rng.standard_normal(n + burn)
    e2 = rng.standard_normal(n + burn)
    z1_indep = _simulate_channel_from_psi(psi1, n, burn, e1)
    z2_indep = _simulate_channel_from_psi(psi2, n, burn, e2)

    # iid bivariate-normal reference at the Pearson-equivalent target corr
    r1 = rng.standard_normal(n)
    r2 = target_pearson * r1 + np.sqrt(max(0.0, 1 - target_pearson ** 2)) * rng.standard_normal(n)

    # Iman-Conover: reorder each channel's independent long-memory draw into
    # the rank order of its own reference column
    z1_sorted = np.sort(z1_indep)
    z2_sorted = np.sort(z2_indep)
    ranks_r1 = np.empty(n, dtype=int)
    ranks_r1[np.argsort(r1, kind="stable")] = np.arange(n)
    ranks_r2 = np.empty(n, dtype=int)
    ranks_r2[np.argsort(r2, kind="stable")] = np.arange(n)
    z1_final = z1_sorted[ranks_r1]
    z2_final = z2_sorted[ranks_r2]

    x1_surr = _remap_to_raw(z1_final, x1)
    x2_surr = _remap_to_raw(z2_final, x2)
    return x1_surr, x2_surr


# ---------------------------------------------------------------------------
# VARIANT B -- innovation_link (Gaussian copula on the innovations)
# ---------------------------------------------------------------------------

def _solve_rho_innov(psi1: np.ndarray, psi2: np.ndarray, target_pearson: float) -> tuple[float, float]:
    """Closed-form rho_innov for corr(X1,X2) = target_pearson, X_i a linear
    filter of contemporaneously-correlated (rho_innov), temporally-white
    unit-variance innovations. Returns (rho_innov_raw, achievable_ratio) --
    achievable_ratio = max |corr| attainable at rho_innov=+-1, so the caller
    can see whether the target was inside the feasible range BEFORE clipping."""
    s12 = float(np.dot(psi1, psi2))
    s11 = float(np.dot(psi1, psi1))
    s22 = float(np.dot(psi2, psi2))
    achievable_ratio = s12 / np.sqrt(s11 * s22)   # correlation at rho_innov=1
    rho_innov = target_pearson / achievable_ratio if achievable_ratio != 0 else np.nan
    return rho_innov, achievable_ratio


def _pair_innovation_link(x1, x2, psi1, psi2, J, burn, rng, rho_innov):
    n = len(x1)
    e1 = rng.standard_normal(n + burn)
    e2 = rho_innov * e1 + np.sqrt(max(0.0, 1 - min(abs(rho_innov), 1.0) ** 2)) * rng.standard_normal(n + burn)
    z1 = _simulate_channel_from_psi(psi1, n, burn, e1)
    z2 = _simulate_channel_from_psi(psi2, n, burn, e2)
    x1_surr = _remap_to_raw(z1, x1)
    x2_surr = _remap_to_raw(z2, x2)
    return x1_surr, x2_surr


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def generate_joint_surrogates(x1: np.ndarray, x2: np.ndarray, M: int, seed_base: int, code: int,
                               method: str = "innovation_link",
                               calibration: str = "simulated",
                               phi1: float | None = None, d1: float | None = None,
                               phi2: float | None = None, d2: float | None = None,
                               J: int = 2000, J_fit: int = 1000, n_reps_calib: int = 5,
                               burn: int | None = None,
                               acf_lags: int = ACF_LAGS):
    """Matches joint_iaaft.py's signature/return-shape convention. Each
    channel is modeled as ARFIMA(1,d,0) (phi=AR(1) root, d=fractional order);
    pass phi1/d1 (and/or phi2/d2) explicitly to skip the grid-search fit for
    that channel. calibration: 'simulated' (default -- indirect-inference /
    simulated-method-of-moments fit against the finite-n realized ACF, see
    estimate_phi_d_simulated; corrects for long-memory finite-sample ACF
    bias) or 'theoretical' (fit to the idealized infinite-sample ACF, see
    estimate_phi_d; kept for disclosure/comparison -- this is the fit that
    measurably undershoots on real data, see this file's own run log).
    method: 'innovation_link' (default, Variant B: Gaussian copula applied
    to the innovations) or 'rank_reorder' (Variant A, literal Iman-Conover
    post-hoc rank reordering, kept for disclosure/comparison -- see module
    docstring for both). Returns (surrogate_pairs, diagnostics)."""
    n = len(x1)
    assert len(x2) == n
    if burn is None:
        burn = J

    lags = min(acf_lags, n // 3)
    r1, r2 = rankdata(x1), rankdata(x2)
    real1_spear = acf(r1, lags)
    real2_spear = acf(r2, lags)
    real_crosscorr0 = float(np.corrcoef(r1, r2)[0, 1])
    target_pearson = 2 * np.sin(np.pi * real_crosscorr0 / 6)   # Gaussian-copula Pearson equivalent of the real Spearman corr

    # (phi, d) estimation (once, from the real data) -- shared by both variants
    if phi1 is None or d1 is None:
        if calibration == "simulated":
            phi1, d1, d1_info = estimate_phi_d_simulated(real1_spear, n, J, burn, n_reps=n_reps_calib,
                                                           seed=seed_base * 1000 + 1)
        elif calibration == "theoretical":
            phi1, d1, d1_info = estimate_phi_d(real1_spear, J_fit=J_fit)
        else:
            raise ValueError(f"unknown calibration {calibration!r}")
    else:
        d1_info = dict(fixed=True)
    if phi2 is None or d2 is None:
        if calibration == "simulated":
            phi2, d2, d2_info = estimate_phi_d_simulated(real2_spear, n, J, burn, n_reps=n_reps_calib,
                                                           seed=seed_base * 1000 + 2)
        elif calibration == "theoretical":
            phi2, d2, d2_info = estimate_phi_d(real2_spear, J_fit=J_fit)
        else:
            raise ValueError(f"unknown calibration {calibration!r}")
    else:
        d2_info = dict(fixed=True)

    psi1_full = ar1_fracdiff_weights(phi1, d1, J)
    psi2_full = ar1_fracdiff_weights(phi2, d2, J)
    rho_innov, achievable_ratio = _solve_rho_innov(psi1_full, psi2_full, target_pearson)
    rho_innov_clipped = float(np.clip(rho_innov, -0.999, 0.999))

    pairs = []
    mism1, mism2, crosscorr_mism = [], [], []
    for i in range(M):
        rng = np.random.default_rng([seed_base, code, i])
        if method == "rank_reorder":
            x1_s, x2_s = _pair_rank_reorder(x1, x2, psi1_full, psi2_full, J, burn, rng, target_pearson)
        elif method == "innovation_link":
            x1_s, x2_s = _pair_innovation_link(x1, x2, psi1_full, psi2_full, J, burn, rng, rho_innov_clipped)
        else:
            raise ValueError(f"unknown method {method!r}")
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
        M=M, lags=lags, method=method, calibration=calibration,
        phi1=phi1, d1=d1, phi2=phi2, d2=d2, J=J, J_fit=J_fit, burn=burn,
        d1_fit=d1_info, d2_fit=d2_info,
        rho_innov_solved=float(rho_innov), rho_innov_used=rho_innov_clipped,
        achievable_corr_ratio_at_rho1=float(achievable_ratio),
        target_pearson_equiv=float(target_pearson),
        channel1_acf=dict(med=float(np.median(mism1)), p95=float(np.percentile(mism1, 95))),
        channel2_acf=dict(med=float(np.median(mism2)), p95=float(np.percentile(mism2, 95))),
        crosscorr0=dict(real=real_crosscorr0, mean_abs_mismatch=float(crosscorr_mism.mean()),
                         p95_mismatch=float(np.percentile(crosscorr_mism, 95))),
        gate_channel1_acf="PASS" if (np.median(mism1) <= TOL_MED and np.percentile(mism1, 95) <= TOL_P95) else "FAIL",
        gate_channel2_acf="PASS" if (np.median(mism2) <= TOL_MED and np.percentile(mism2, 95) <= TOL_P95) else "FAIL",
        gate_crosscorr0="PASS" if np.percentile(crosscorr_mism, 95) <= TOL_CROSSCORR else "FAIL",
        tol_med=TOL_MED, tol_p95=TOL_P95, tol_crosscorr=TOL_CROSSCORR,
    )
    diag["gate"] = "PASS" if all(diag[k] == "PASS" for k in
                                  ("gate_channel1_acf", "gate_channel2_acf", "gate_crosscorr0")) else "FAIL"
    return pairs, diag


if __name__ == "__main__":
    import pandas as pd
    import json
    from pathlib import Path

    # Repository-relative path (Codex review, PR #219 -- the original hardcoded
    # the author's own absolute Windows worktree path, breaking on any other
    # checkout even though the CSV is tracked in the adjacent analysis dir).
    DATA_CSV = (Path(__file__).resolve().parent.parent
                / "mnq_dailygeom_notice_2026-08-29" / "candidate24_joint_frame.csv")
    df = pd.read_csv(DATA_CSV)
    x1 = df["on_range"].to_numpy()
    x2 = df["rth_range"].to_numpy()
    print(f"n={len(x1)}")

    for method in ("rank_reorder", "innovation_link"):
        pairs, diag = generate_joint_surrogates(x1, x2, M=40, seed_base=7, code=0, method=method,
                                                 calibration="simulated", J=2000, n_reps_calib=6)
        print("=" * 70)
        print(f"method={method} calibration=simulated")
        print(json.dumps(diag, indent=2))
