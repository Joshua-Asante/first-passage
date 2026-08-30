"""ccc_garch.py -- CONSTANT CONDITIONAL CORRELATION (CCC) GARCH joint-surrogation
null lens for Q-RANGEXFER-1 Stage-2 (4th candidate design this session; see
RESULTS.md attempts #1-#3 -- linked-residual IAAFT, bivariate VAR(p) residual
bootstrap, shared-starting-permutation IAAFT -- all VOIDed on their own
diagnostic gate before this one was attempted).

TWO SUB-ATTEMPTS WERE ACTUALLY RUN. Both are disclosed here; only the second
is exposed as this module's `generate_joint_surrogates`.

--------------------------------------------------------------------------
SUB-ATTEMPT A (rejected, kept only as a documented negative finding):
literal textbook Bollerslev (1990) CCC-GARCH, applied the way the lens brief
describes it: normal-score each channel (z = normal_scores(x)), fit a
constant-mean GARCH(1,1) to z directly via `arch.univariate` (ConstantMean +
GARCH(1,1) + Normal), i.e. z_t = mu + eps_t, eps_t = sigma_t * u_t, sigma_t^2
= omega + alpha*eps_{t-1}^2 + beta*sigma_{t-1}^2, extract standardized
residuals u_t = eps_t/sigma_t, correlate two channels' u_t via a fixed
Cholesky of their real contemporaneous correlation, simulate z_t forward.

This was ACTUALLY FIT AND SIMULATED against the real on_range series before
being rejected (not a theoretical dismissal):

    ConstantMean(z1*10) + GARCH(1,1) params: mu=-0.304, omega=10.22,
    alpha=0.103, beta=0.794
    REAL on_range rank-ACF lags 1-10:      [0.411 0.393 0.367 0.367 0.348
                                             0.329 0.304 0.283 0.300 0.241]
    std_resid (u_t) own rank-ACF lags1-10: [0.371 0.361 0.335 0.335 0.320
                                             0.303 0.279 0.257 0.273 0.217]
       -> the "standardized residuals" the GARCH fit calls white noise still
          carry ~90% of the raw series' own autocorrelation. GARCH(1,1) here
          is barely explaining any of the level persistence.
    SIMULATED level rank-ACF lags1-10 (IID bootstrap of those std_resid,
    forward-simulated through the fitted variance recursion):
                                            [-0.014 -0.027 -0.011 -0.006
                                             -0.026 -0.006 -0.007  0.029
                                             -0.047  0.009]
       -> collapses to ~0, exactly as predicted analytically below.

WHY, mechanistically (not just "it failed empirically" -- this is a structural
fact about the model class, confirmed by the run above): a constant-mean
GARCH(p,q) writes the observed series as z_t = mu + sigma_t*u_t with u_t an
iid mean-zero shock independent of F_{t-1} (sigma_t is F_{t-1}-measurable).
Then for k>=1, Cov(z_t, z_{t-k}) = E[sigma_t*u_t*sigma_{t-k}*u_{t-k}] =
E[sigma_t*sigma_{t-k}*u_{t-k}*E[u_t|F_{t-1}]] = 0 identically, REGARDLESS of
how persistent the fitted variance recursion sigma_t^2 is. GARCH(p,q) is
built to reproduce autocorrelation in squared/absolute shocks (volatility
clustering); it structurally cannot generate autocorrelation in the SIGNED
LEVEL of a constant-mean series, by construction of the model, not by a
fitting failure. on_range/rth_range are themselves level series with a real,
large, own-channel autocorrelation (0.41 at lag 1) -- textbook CCC-GARCH's
mean equation is the wrong object for this data class. This is a distinct,
freshly-diagnosed failure mode from attempts #1-#3 in RESULTS.md, but lands
in the same "own-channel ACF fails the gate" bucket.

--------------------------------------------------------------------------
SUB-ATTEMPT B (what this module actually implements and reports):
a Multiplicative Error Model (MEM / Engle-Russell ACD / Chou's CARR) reading
of "GARCH conditional-variance recursion," which is the literal alternative
reading of the lens brief's own final instruction -- "simulate each channel
forward through its OWN fitted GARCH conditional-variance recursion using
those correlated innovations" -- applied to the OBSERVED POSITIVE LEVEL
directly (the standard MEM/CARR construction for realized-volatility/range
data, Engle 2002 / Chou 2005), rather than to an unobserved return-style
mean equation. This keeps every element the lens brief actually names
(univariate GARCH-type conditional-variance recursion per channel, own
standardized innovations, fixed-Cholesky CCC coupling, own-recursion
forward simulation, rank-remap) but fixes the exact defect diagnosed in
Sub-attempt A by letting the recursion drive the observed level directly:

    h1_t = omega1 + alpha1*y1_{t-1} + beta1*h1_{t-1}      (h1_0 = mean(y1))
    y1_t = h1_t * v1_t,           v1_t iid, E[v1_t] = 1

Because h_t depends on the lagged OBSERVED value y_{t-1} (not on a lagged
unobserved shock), Cov(y_t, y_{t-1}) != 0 in general -- this is the same
mechanism by which GARCH(1,1) gives eps_t^2 its own real autocorrelation;
here it is applied directly to the level because on_range/rth_range are
themselves volatility-proxy magnitudes, not signed returns.

  1. Fit each channel's (omega, alpha, beta) by Gaussian QMLE directly on the
     RAW positive series (no normal-score step needed for the mean-equation
     fit itself -- MEM requires positivity, which normal-scoring destroys;
     normal-scoring is reserved for the diagnostic gate functions below,
     reused verbatim from joint_iaaft.py).
  2. Extract the channel's own standardized multiplicative residuals
     v_t = y_t / h_t (in-sample, fitted h_t path).
  3. Compute the two channels' real lag-0 rank cross-correlation (the
     `crosscorr0.real` diagnostic target).
  4. CALIBRATE a Gaussian-copula correlation rho_u (NOT set equal to the raw
     target correlation) such that Cholesky-correlated standard normals,
     passed through the NORTA construction below, reproduce that target
     correlation in the FINAL simulated series -- the mapping from copula
     correlation to output series correlation is non-linear and amplified by
     the shared recursive feedback, so this requires an explicit numeric
     calibration (bisection against a small calibration bank of draws), done
     once per call, not assumed equal.
  5. Per surrogate draw: draw bivariate Gaussian (u1,u2) with correlation
     rho_u via a FIXED Cholesky factor (this IS the Bollerslev CCC step --
     one constant correlation matrix reused for every innovation draw, not
     re-estimated per draw), map each to a uniform via Phi(u), then to a
     draw from that channel's OWN empirical v_t distribution via its
     empirical quantile function (NORTA: Normal-To-Anything) -- this gives
     v1_sim, v2_sim with (a) each channel's exact own empirical marginal
     distribution and (b) a copula-induced rank association targeting the
     real cross-correlation.
  6. Simulate h1_t, h2_t, y1_t, y2_t forward through the two channels' OWN
     fitted recursions using these correlated v_sim shocks, fixing y_0 = the
     real first observation (fixed-design start, same discipline as the
     existing VAR module's p-point fixed start).
  7. Rank-remap y1_sim, y2_sim onto each channel's own real sorted RAW values
     (exact multiset identity -- ASSERTED).

DIAGNOSTIC GATE: identical tolerances and lag set to
joint_iaaft.py / docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md
Sec 1 (TOL_MED=0.04, TOL_P95=0.07 own-ACF; TOL_CROSSCORR=0.05 lag-0 rank
cross-correlation), reusing `normal_scores`/`acf` VERBATIM from that module.

RESULT (see __main__ / StructuredOutput report for the exact run): the
cross-correlation diagnostic PASSES cleanly. The own-channel ACF diagnostic
FAILS. In-sample, the MEM residuals v_t are excellently whitened (own
rank-ACF ~0 at lags 1-10 for both channels -- confirming the recursion, not
the innovation-bootstrap, is what is supposed to carry the persistence, and
that it is doing so correctly IN-SAMPLE). But the QMLE-fitted persistence
(alpha+beta ~ 0.92 for on_range) implies a SIMULATED level series whose ACF
decays roughly geometrically at that rate -- which decays MUCH faster past
lag ~10 than the real series' own ACF, which falls from 0.41 (lag 1) to
~0.24-0.25 by lag 10 and then goes materially flat (0.24/0.25/0.25 at
lags 10/20/30 per the brief) rather than continuing to decay -- a
near-plateau shape a single-persistence linear recursion cannot produce.
A second beta lag (MEM(1,2): h_t = omega + alpha*y_{t-1} + beta1*h_{t-1} +
beta2*h_{t-2}) was tried as an in-lens order iteration and the QMLE optimizer
drove beta2 to ~0 (i.e. it found no likelihood benefit to a second decay
timescale) -- so a higher MEM order does not, on this data, rescue the own-
ACF gate; the same qualitative conclusion RESULTS.md #2 already reached for
the VAR(p) approach (finite linear order caps out around comparable
persistence and cannot reproduce the observed plateau), reached here by an
independent GARCH-family route. A two-component (Engle-Lee style,
long-run + short-run persistence) MEM extension was attempted as a further
iteration and did NOT converge numerically within this lens's time budget
(optimizer diverged into a non-stationary parameter region) -- disclosed as
an incomplete iteration, not folded into the reported result.
"""
from __future__ import annotations

import numpy as np
from scipy.stats import rankdata, norm
from scipy.optimize import minimize

ACF_LAGS = 30
TOL_MED, TOL_P95 = 0.04, 0.07          # own-ACF mismatch tolerance -- SAME numbers as
                                        # docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md
                                        # Sec 1 / joint_iaaft.py, reused for consistency
TOL_CROSSCORR = 0.05                   # lag-0 rank cross-correlation mismatch tolerance,
                                        # same constant joint_iaaft.py introduced
N_CALIB_DRAWS = 12                     # draws per rho_u trial during copula-correlation calibration


def normal_scores(x: np.ndarray) -> np.ndarray:
    """Verbatim from joint_iaaft.py / iaaft_battery.py, duplicated with attribution."""
    n = len(x)
    ranks = np.empty(n, dtype=float)
    ranks[np.argsort(x, kind="stable")] = np.arange(1, n + 1)
    return norm.ppf(ranks / (n + 1))


def acf(x: np.ndarray, max_lag: int) -> np.ndarray:
    """Verbatim from joint_iaaft.py / iaaft_battery.py."""
    xc = x - x.mean()
    denom = float(np.dot(xc, xc))
    return np.array([float(np.dot(xc[:-k], xc[k:]) / denom) for k in range(1, max_lag + 1)])


# ---------------------------------------------------------------------------
# Sub-attempt B: MEM(1,1) (CARR-style) per-channel fit
# ---------------------------------------------------------------------------

def _mem_filter(y: np.ndarray, omega: float, alpha: float, beta: float) -> np.ndarray:
    n = len(y)
    h = np.empty(n)
    h[0] = y.mean()
    for t in range(1, n):
        h[t] = omega + alpha * y[t - 1] + beta * h[t - 1]
    return h


def _mem_negloglik(params, y):
    omega, alpha, beta = params
    h = _mem_filter(y, omega, alpha, beta)
    if np.any(h <= 0) or not np.all(np.isfinite(h)):
        return 1e10
    resid2 = (y - h) ** 2 / (h ** 2)
    return 0.5 * float(np.sum(np.log(h ** 2) + resid2))


def fit_mem(y: np.ndarray):
    """QMLE fit of a MEM(1,1) (Engle-Russell ACD / Chou CARR form) directly on
    the raw positive series y. Returns (omega, alpha, beta)."""
    ymean = float(y.mean())
    starts = [
        [ymean * 0.05, 0.10, 0.85],
        [ymean * 0.10, 0.15, 0.70],
        [ymean * 0.02, 0.05, 0.90],
    ]
    bounds = [(1e-6, ymean * 2), (1e-6, 0.999), (1e-6, 0.999)]
    best = None
    for x0 in starts:
        res = minimize(_mem_negloglik, x0, args=(y,), method="L-BFGS-B", bounds=bounds)
        if best is None or (res.success and res.fun < best.fun):
            best = res
    assert best is not None
    return tuple(best.x)


def _simulate_mem_pair(y1: np.ndarray, y2: np.ndarray, params1, params2,
                        v1_sorted: np.ndarray, v2_sorted: np.ndarray,
                        rho_u: float, rng: np.random.Generator):
    """One joint MEM-CCC surrogate draw. Fixed Cholesky correlation rho_u
    couples standard-normal shocks; each is mapped via NORTA onto that
    channel's own empirical multiplicative-residual distribution; both
    channels then simulate forward through their OWN fitted MEM recursion."""
    n = len(y1)
    omega1, alpha1, beta1 = params1
    omega2, alpha2, beta2 = params2

    L = np.linalg.cholesky(np.array([[1.0, rho_u], [rho_u, 1.0]]))
    Zraw = rng.standard_normal((2, n - 1))
    U = L @ Zraw
    p1 = norm.cdf(U[0])
    p2 = norm.cdf(U[1])
    idx1 = np.clip((p1 * n).astype(int), 0, n - 1)
    idx2 = np.clip((p2 * n).astype(int), 0, n - 1)
    vsim1 = v1_sorted[idx1]
    vsim2 = v2_sorted[idx2]

    ysim1 = np.empty(n)
    ysim2 = np.empty(n)
    h1 = np.empty(n)
    h2 = np.empty(n)
    ysim1[0], ysim2[0] = y1[0], y2[0]
    h1[0], h2[0] = y1.mean(), y2.mean()
    for t in range(1, n):
        h1[t] = omega1 + alpha1 * ysim1[t - 1] + beta1 * h1[t - 1]
        h2[t] = omega2 + alpha2 * ysim2[t - 1] + beta2 * h2[t - 1]
        ysim1[t] = h1[t] * vsim1[t - 1]
        ysim2[t] = h2[t] * vsim2[t - 1]
    return ysim1, ysim2


def _calibrate_rho_u(y1, y2, params1, params2, v1_sorted, v2_sorted, target_cc,
                      seed_base, code):
    """Bisection search for the Gaussian-copula correlation rho_u whose
    resulting SIMULATED-series rank cross-correlation matches target_cc.
    Needed because the copula correlation is not preserved 1:1 through the
    shared recursive feedback (empirically ~30-40% amplification on this
    data -- rho_u approx 0.81 reproduces a target of approx 0.77)."""
    def mean_cc(rho_u, n_draws=N_CALIB_DRAWS):
        ccs = []
        for i in range(n_draws):
            rng = np.random.default_rng([seed_base, code, 999, i])
            ys1, ys2 = _simulate_mem_pair(y1, y2, params1, params2, v1_sorted, v2_sorted, rho_u, rng)
            ccs.append(np.corrcoef(rankdata(ys1), rankdata(ys2))[0, 1])
        return float(np.mean(ccs))

    lo, hi = 0.0, 0.995
    cc_lo, cc_hi = mean_cc(lo), mean_cc(hi)
    if target_cc <= cc_lo:
        return lo
    if target_cc >= cc_hi:
        return hi
    for _ in range(10):
        mid = 0.5 * (lo + hi)
        cc_mid = mean_cc(mid)
        if cc_mid < target_cc:
            lo, cc_lo = mid, cc_mid
        else:
            hi, cc_hi = mid, cc_mid
    return 0.5 * (lo + hi)


def generate_joint_surrogates(x1: np.ndarray, x2: np.ndarray, M: int, seed_base: int,
                               code: int, acf_lags: int = ACF_LAGS, **kwargs):
    """CCC-GARCH (MEM/CARR sub-attempt) joint-surrogation generator. Matches
    joint_iaaft.generate_joint_surrogates's signature/return shape.
    Returns (surrogate_pairs, diagnostics)."""
    x1 = np.asarray(x1, dtype=float)
    x2 = np.asarray(x2, dtype=float)
    n = len(x1)
    assert len(x2) == n
    lags = min(acf_lags, n // 3)

    real1_spear = acf(rankdata(x1), lags)
    real2_spear = acf(rankdata(x2), lags)
    real_crosscorr0 = float(np.corrcoef(rankdata(x1), rankdata(x2))[0, 1])

    params1 = fit_mem(x1)
    params2 = fit_mem(x2)
    h1_fit = _mem_filter(x1, *params1)
    h2_fit = _mem_filter(x2, *params2)
    v1 = x1 / h1_fit
    v2 = x2 / h2_fit
    v1_sorted = np.sort(v1)
    v2_sorted = np.sort(v2)

    # in-sample residual-whitening diagnostic (own-ACF of the fitted
    # multiplicative residuals -- confirms the recursion, not bootstrap
    # noise, is carrying the persistence)
    resid_acf1 = float(np.max(np.abs(acf(rankdata(v1), min(10, lags)))))
    resid_acf2 = float(np.max(np.abs(acf(rankdata(v2), min(10, lags)))))

    rho_u = _calibrate_rho_u(x1, x2, params1, params2, v1_sorted, v2_sorted,
                              real_crosscorr0, seed_base, code)

    pairs = []
    mism1, mism2, crosscorr_mism = [], [], []
    for i in range(M):
        rng = np.random.default_rng([seed_base, code, i])
        y1_s, y2_s = _simulate_mem_pair(x1, x2, params1, params2, v1_sorted, v2_sorted, rho_u, rng)

        x1_sorted = np.sort(x1)
        ranks1 = np.empty(n, dtype=int)
        ranks1[np.argsort(y1_s, kind="stable")] = np.arange(n)
        x1_surr = x1_sorted[ranks1]

        x2_sorted = np.sort(x2)
        ranks2 = np.empty(n, dtype=int)
        ranks2[np.argsort(y2_s, kind="stable")] = np.arange(n)
        x2_surr = x2_sorted[ranks2]

        assert np.array_equal(np.sort(x1_surr), x1_sorted), "channel-1 multiset identity violated"
        assert np.array_equal(np.sort(x2_surr), x2_sorted), "channel-2 multiset identity violated"

        pairs.append((x1_surr, x2_surr))
        s1_spear = acf(rankdata(x1_surr), lags)
        s2_spear = acf(rankdata(x2_surr), lags)
        mism1.append(float(np.max(np.abs(s1_spear - real1_spear))))
        mism2.append(float(np.max(np.abs(s2_spear - real2_spear))))
        surr_crosscorr0 = float(np.corrcoef(rankdata(x1_surr), rankdata(x2_surr))[0, 1])
        crosscorr_mism.append(abs(surr_crosscorr0 - real_crosscorr0))

    mism1, mism2 = np.array(mism1), np.array(mism2)
    crosscorr_mism = np.array(crosscorr_mism)

    diag = dict(
        M=M, lags=lags, rho_u_calibrated=rho_u,
        mem_params_channel1=dict(omega=params1[0], alpha=params1[1], beta=params1[2]),
        mem_params_channel2=dict(omega=params2[0], alpha=params2[1], beta=params2[2]),
        residual_whitening=dict(max_abs_acf_ch1=resid_acf1, max_abs_acf_ch2=resid_acf2,
                                 gate="PASS" if max(resid_acf1, resid_acf2) <= 0.10 else "FAIL"),
        channel1_acf=dict(med=float(np.median(mism1)), p95=float(np.percentile(mism1, 95))),
        channel2_acf=dict(med=float(np.median(mism2)), p95=float(np.percentile(mism2, 95))),
        crosscorr0=dict(real=real_crosscorr0, mean_abs_mismatch=float(crosscorr_mism.mean()),
                         p95_mismatch=float(np.percentile(crosscorr_mism, 95))),
        tol_med=TOL_MED, tol_p95=TOL_P95, tol_crosscorr=TOL_CROSSCORR,
    )
    diag["gate_channel1_acf"] = "PASS" if (diag["channel1_acf"]["med"] <= TOL_MED and diag["channel1_acf"]["p95"] <= TOL_P95) else "FAIL"
    diag["gate_channel2_acf"] = "PASS" if (diag["channel2_acf"]["med"] <= TOL_MED and diag["channel2_acf"]["p95"] <= TOL_P95) else "FAIL"
    diag["gate_crosscorr0"] = "PASS" if diag["crosscorr0"]["p95_mismatch"] <= TOL_CROSSCORR else "FAIL"
    diag["gate"] = "PASS" if all(diag[k] == "PASS" for k in
                                  ("gate_channel1_acf", "gate_channel2_acf", "gate_crosscorr0")) else "FAIL"
    return pairs, diag


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("../mnq_dailygeom_notice_2026-08-29/candidate24_joint_frame.csv")
    x1 = df["on_range"].to_numpy()
    x2 = df["rth_range"].to_numpy()

    pairs, diag = generate_joint_surrogates(x1, x2, M=40, seed_base=7, code=0)
    print("=== CCC-GARCH (MEM/CARR) joint surrogation -- REAL DATA RUN ===")
    print("n =", len(x1), " lags =", diag["lags"])
    print("MEM params ch1 (omega,alpha,beta):", diag["mem_params_channel1"])
    print("MEM params ch2 (omega,alpha,beta):", diag["mem_params_channel2"])
    print("calibrated rho_u:", diag["rho_u_calibrated"])
    print("residual_whitening (in-sample, own-ACF of v_t=y_t/h_t):", diag["residual_whitening"])
    print("channel1_acf:", diag["channel1_acf"], diag["gate_channel1_acf"])
    print("channel2_acf:", diag["channel2_acf"], diag["gate_channel2_acf"])
    print("crosscorr0:", diag["crosscorr0"], diag["gate_crosscorr0"])
    print("GATE:", diag["gate"])
