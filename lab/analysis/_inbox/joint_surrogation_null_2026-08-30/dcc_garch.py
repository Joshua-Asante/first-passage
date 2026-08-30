"""Joint-surrogation null, LENS: Dynamic Conditional Correlation (DCC) GARCH
(Engle 2002), 2-step estimation, hand-rolled DCC recursion on top of `arch`'s
univariate GARCH(1,1) fits. Fourth lens attempted on Q-RANGEXFER-1's joint
surrogation problem (see RESULTS.md for the first three: linked-residual
IAAFT, bivariate VAR(p) residual bootstrap, shared-starting-permutation
coupled IAAFT -- all three FAILED their own diagnostic gate, in two exactly
opposite directions: VAR trades own-ACF for cross-corr fidelity, shared-start
IAAFT trades the reverse).

MOTIVATION (why DCC, not the constant-correlation CCC lens run in parallel):
CCC assumes ONE fixed lag-0 cross-correlation for the whole sample. If the
real MNQ overnight/RTH range pair's co-movement itself varies over time
(correlation clustering -- calm regimes with weak coupling, stressed regimes
with tight coupling), a constant-correlation model will reproduce the
UNCONDITIONAL lag-0 cross-correlation on average but may show more dispersion
across draws, or a different failure mode, than a model that lets rho_t
evolve. DCC lets the data have a time-varying correlation path while still
targeting the same unconditional correlation in expectation.

DESIGN:

  1. Normal-score BOTH channels independently (verbatim `normal_scores` from
     `joint_iaaft.py`, imported not re-derived): z1, z2.
  2. Per-channel univariate GARCH(1,1), fit via `arch.univariate.arch_model`
     treating each z-channel AS THE MODELED SERIES directly (mean='Zero',
     vol='GARCH', p=1, q=1) -- i.e. z_t = sigma_t * eta_t with sigma_t^2 =
     omega + alpha*z_{t-1}^2 + beta*sigma_{t-1}^2. This is the same framing
     the CCC lens uses. Extract standardized residuals u_t = z_t / sigma_t
     (should be close to iid unit-variance if the GARCH(1,1) spec is
     adequate -- checked below as a residual-ARCH diagnostic).
  3. DCC(1,1) recursion on the standardized-residual PAIR (u1_t, u2_t)
     (Engle 2002, correlation-targeting variance-targeting form):
        Q_t = (1-a-b)*Qbar + a*(u_{t-1} u_{t-1}') + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} Q_t diag(Q_t)^{-1/2}
     where Qbar is the unconditional correlation matrix of (u1,u2) (2x2, off
     -diagonal = rho_bar, the sample correlation). (a,b) are fit by maximizing
     the bivariate-normal DCC quasi-likelihood (closed-form 2x2 determinant/
     inverse), holding the univariate GARCH parameters fixed at their
     step-1 MLEs (Engle's 2-step estimator -- this is what makes hand-rolling
     tractable without `arch`'s multivariate support).
  4. SIMULATE forward jointly: at each step, draw two independent standard
     normals (e1_t, e2_t), correlate them via the Cholesky of the CURRENT
     recursion's R_t (using the running SIMULATED shock history, not the
     real one) to get standardized shocks (eta1_t, eta2_t), then feed those
     into each channel's OWN fitted GARCH(1,1) variance recursion
     (sigma_t^2 updates from the simulated eta, exactly mirroring the fitted
     recursion) to produce z_t = sigma_t * eta_t. A burn-in is discarded so
     the simulated path is not dependent on its literal starting values (this
     differs from the VAR lens's fixed-real-start convention -- GARCH/DCC
     recursions are geometrically mixing under stationarity so burn-in is the
     standard convention, disclosed here rather than silently assumed).
  5. Rank-remap each simulated channel onto that channel's own real sorted
     RAW values (exact multiset identity -- asserted, same discipline as
     `joint_iaaft.py`).

DIAGNOSTIC GATE: identical functions and tolerances to `joint_iaaft.py`
(`normal_scores`, `acf`, TOL_MED=0.04, TOL_P95=0.07 for own-ACF, TOL_CROSSCORR
=0.05 for lag-0 rank cross-correlation), imported not re-derived, so results
are directly comparable across every lens in this panel.

WHAT THIS NULL ACTUALLY TESTS: same framing as the VAR lens's note in
`joint_iaaft.py` -- a DCC-GARCH surrogate reproduces the REAL data's own
volatility-clustering-shaped autocorrelation (via the GARCH recursion applied
directly to the range level, since range is itself a volatility proxy) AND a
GENUINE, possibly TIME-VARYING linear correlation structure between the two
channels, by construction of the fitted model. It does NOT distinguish a
"real transmission effect" from "two series driven by correlated GARCH-type
volatility processes" -- exactly as intended: this null tests whether the
observed extreme-decile lift exceeds what a bivariate GARCH-DCC joint
volatility model, fit to reproduce the real data's own dynamics, would itself
produce.

*** POST-HOC AMENDMENT (same session): the literal Step-1 spec above --
GARCH(1,1), mean='Zero', fit on the NORMAL-SCORED channel via `arch` -- was
implemented and run first (kept below as
`generate_joint_surrogates_zeromean_literal` for the record). It fails
catastrophically: own-channel ACF mismatch med~0.43-0.46 (an order of
magnitude worse than even the VAR lens's ~0.10-0.13 failure in RESULTS.md).

This is NOT an estimation or tuning problem -- it is a mathematical property
of any z_t = sigma_t * eta_t process with iid MEAN-ZERO eta_t: sigma_{t+k} is
a function of eta_t..eta_{t+k-1} only (predetermined, "GARCH" processes are
constructed this way), so Cov(z_t, z_{t+k}) = E[z_t * sigma_{t+k}] * E[eta_{t+k}]
= 0 for any k>=1 whenever E[eta]=0 -- REGARDLESS of the GARCH order, the
fitted (alpha, beta), or the innovation distribution's shape. A mean-zero
GARCH-type process is, BY CONSTRUCTION, white noise in its own LEVEL (only
its squares/absolute value are autocorrelated). Normal-scoring the channel
first (forcing a symmetric, mean-zero marginal) locks in exactly this
structure, so no GARCH(1,1)-on-normal-scores variant can pass the own-ACF
gate on a series whose own RAW level (not its square) is persistent, which
on_range/rth_range demonstrably are (real rank-ACF here does NOT decay to 0
within 30 lags -- consistent with the "range IS itself a volatility proxy"
framing, not a mean-zero return series).

FIX (still within the GARCH family, "iterate on parameters" per the task's
own escalation allowance -- not a lens switch): use a Multiplicative Error
Model (MEM; Engle 2002, same paper that introduces DCC, purpose-built for
exactly this data class -- range/volume/duration) directly on the RAW
positive channel: x_t = mu_t * eta_t, mu_t = omega + alpha*x_{t-1} +
beta*mu_{t-1}, with eta_t a POSITIVE, MEAN-1 (not mean-0) iid shock. Because
E[eta]=1 != 0, the algebra above flips sign and z_t's own level now DOES
inherit mu_t's persistence (Cov(x_t,x_{t+k}) ~ Cov(mu_t,mu_{t+k}) > 0). Fit
by Exponential-QMLE (Engle-Russell ACD convention: consistent for the
conditional mean even if the true eta distribution isn't exactly
Exponential). `arch` has no MEM support, so this step is hand-rolled
(disclosed -- deviates from "via arch" in the literal spec for this reason).
Correlation coupling: normal-score the RECOVERED shocks eta1_t, eta2_t (this
residual-level normal-scoring, not a channel-level one, is what feeds DCC),
fit DCC(1,1) on those exactly as in the literal design, then at simulation
time map the DCC-correlated Gaussian draws back to each channel's own
EMPIRICAL shock quantiles (a Gaussian-copula device) before feeding them into
the MEM recursion -- avoids assuming any particular parametric shape for the
positive shocks while still letting a Gaussian DCC process drive their joint
dependence.

Both constructions are runnable below; `generate_joint_surrogates` (the
required entry point) is the MEM+DCC fix. See the bottom of this file / the
session's final report for the literal attempt's numbers.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm as _norm
from arch import arch_model

from joint_iaaft import normal_scores, acf, ACF_LAGS, TOL_MED, TOL_P95, TOL_CROSSCORR

DEFAULT_BURN_IN = 500


def fit_univariate_garch11(z: np.ndarray):
    """Fit GARCH(1,1), mean='Zero', on a normal-scored channel. Returns
    (omega, alpha, beta, sigma2_series, std_resid) all in-sample."""
    am = arch_model(z, mean="Zero", vol="GARCH", p=1, q=1, dist="normal", rescale=False)
    res = am.fit(disp="off", show_warning=False)
    omega = float(res.params["omega"])
    alpha = float(res.params["alpha[1]"])
    beta = float(res.params["beta[1]"])
    sigma2 = res.conditional_volatility ** 2  # pandas/np array, in-sample fitted variance
    std_resid = (z - 0.0) / res.conditional_volatility  # mean='Zero' => resid == z
    return omega, alpha, beta, np.asarray(sigma2), np.asarray(std_resid)


def _dcc_neg_loglik(params, u1, u2, rho_bar):
    a, b = params
    if a < 0 or b < 0 or a + b >= 0.999:
        return 1e10
    T = len(u1)
    Q11 = np.empty(T); Q22 = np.empty(T); Q12 = np.empty(T)
    Q11[0], Q22[0], Q12[0] = 1.0, 1.0, rho_bar
    for t in range(1, T):
        Q11[t] = (1 - a - b) * 1.0 + a * u1[t - 1] ** 2 + b * Q11[t - 1]
        Q22[t] = (1 - a - b) * 1.0 + a * u2[t - 1] ** 2 + b * Q22[t - 1]
        Q12[t] = (1 - a - b) * rho_bar + a * u1[t - 1] * u2[t - 1] + b * Q12[t - 1]
    rho = Q12 / np.sqrt(Q11 * Q22)
    rho = np.clip(rho, -0.999, 0.999)
    ll = -0.5 * (np.log(1 - rho ** 2) + (u1 ** 2 - 2 * rho * u1 * u2 + u2 ** 2) / (1 - rho ** 2))
    return -float(np.sum(ll))


def fit_dcc11(u1: np.ndarray, u2: np.ndarray):
    """Engle (2002) 2-step DCC(1,1), correlation-targeting. Returns (a, b, rho_bar)."""
    rho_bar = float(np.corrcoef(u1, u2)[0, 1])
    x0 = np.array([0.02, 0.95])
    res = minimize(
        _dcc_neg_loglik, x0, args=(u1, u2, rho_bar),
        method="Nelder-Mead",
        options=dict(xatol=1e-6, fatol=1e-6, maxiter=2000),
    )
    a, b = float(res.x[0]), float(res.x[1])
    a = max(a, 1e-8)
    b = max(b, 0.0)
    if a + b >= 0.999:
        scale = 0.998 / (a + b)
        a, b = a * scale, b * scale
    return a, b, rho_bar


def _simulate_dcc_garch_pair(n, burn_in, rng,
                              omega1, alpha1, beta1,
                              omega2, alpha2, beta2,
                              a, b, rho_bar):
    T = n + burn_in
    uvar1 = omega1 / max(1e-10, (1 - alpha1 - beta1))
    uvar2 = omega2 / max(1e-10, (1 - alpha2 - beta2))

    sigma2_1 = np.empty(T); sigma2_2 = np.empty(T)
    eta1 = np.empty(T); eta2 = np.empty(T)
    z1 = np.empty(T); z2 = np.empty(T)
    Q11 = np.empty(T); Q22 = np.empty(T); Q12 = np.empty(T)

    sigma2_1[0], sigma2_2[0] = uvar1, uvar2
    Q11[0], Q22[0], Q12[0] = 1.0, 1.0, rho_bar
    rho0 = np.clip(Q12[0] / np.sqrt(Q11[0] * Q22[0]), -0.999, 0.999)

    e1, e2 = rng.standard_normal(2)
    eta1[0] = e1
    eta2[0] = rho0 * e1 + np.sqrt(1 - rho0 ** 2) * e2
    z1[0] = np.sqrt(sigma2_1[0]) * eta1[0]
    z2[0] = np.sqrt(sigma2_2[0]) * eta2[0]

    for t in range(1, T):
        Q11[t] = (1 - a - b) * 1.0 + a * eta1[t - 1] ** 2 + b * Q11[t - 1]
        Q22[t] = (1 - a - b) * 1.0 + a * eta2[t - 1] ** 2 + b * Q22[t - 1]
        Q12[t] = (1 - a - b) * rho_bar + a * eta1[t - 1] * eta2[t - 1] + b * Q12[t - 1]
        rho_t = np.clip(Q12[t] / np.sqrt(Q11[t] * Q22[t]), -0.999, 0.999)

        e1, e2 = rng.standard_normal(2)
        eta1[t] = e1
        eta2[t] = rho_t * e1 + np.sqrt(1 - rho_t ** 2) * e2

        sigma2_1[t] = omega1 + alpha1 * z1[t - 1] ** 2 + beta1 * sigma2_1[t - 1]
        sigma2_2[t] = omega2 + alpha2 * z2[t - 1] ** 2 + beta2 * sigma2_2[t - 1]
        z1[t] = np.sqrt(sigma2_1[t]) * eta1[t]
        z2[t] = np.sqrt(sigma2_2[t]) * eta2[t]

    return z1[burn_in:], z2[burn_in:]


def generate_joint_surrogates_zeromean_literal(x1: np.ndarray, x2: np.ndarray, M: int, seed_base: int,
                               code: int, acf_lags: int = ACF_LAGS,
                               burn_in: int = DEFAULT_BURN_IN):
    """LITERAL Step-1-spec DCC-GARCH(1,1): mean='Zero' GARCH(1,1) via `arch`
    fit on the NORMAL-SCORED channel. Kept for the record -- see the module
    docstring's "POST-HOC AMENDMENT": this construction is mathematically
    guaranteed to produce ~zero own-level ACF and fails the gate badly.
    Signature/return shape matches `joint_iaaft.generate_joint_surrogates`."""
    n = len(x1)
    assert len(x2) == n
    lags = min(acf_lags, n // 3)

    real1_spear = acf(pd.Series(x1).rank().to_numpy(), lags)
    real2_spear = acf(pd.Series(x2).rank().to_numpy(), lags)
    real_crosscorr0 = float(np.corrcoef(pd.Series(x1).rank(), pd.Series(x2).rank())[0, 1])

    z1 = normal_scores(x1)
    z2 = normal_scores(x2)

    omega1, alpha1, beta1, sigma2_1_fit, u1 = fit_univariate_garch11(z1)
    omega2, alpha2, beta2, sigma2_2_fit, u2 = fit_univariate_garch11(z2)

    # residual-ARCH diagnostic: max |ACF| of standardized-residual SQUARES at
    # lags 1..5 should be small if GARCH(1,1) adequately whitens the variance
    # dynamics (does not gate the pass/fail verdict -- reported for transparency).
    resid_sq_acf1 = float(np.max(np.abs(acf(u1 ** 2, 5))))
    resid_sq_acf2 = float(np.max(np.abs(acf(u2 ** 2, 5))))

    a, b, rho_bar = fit_dcc11(u1, u2)

    pairs = []
    mism1, mism2, crosscorr_mism = [], [], []
    for i in range(M):
        rng = np.random.default_rng([seed_base, code, i])
        z1_surr, z2_surr = _simulate_dcc_garch_pair(
            n, burn_in, rng, omega1, alpha1, beta1, omega2, alpha2, beta2, a, b, rho_bar
        )

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

        pairs.append((x1_surr, x2_surr))

        s1_spear = acf(pd.Series(x1_surr).rank().to_numpy(), lags)
        s2_spear = acf(pd.Series(x2_surr).rank().to_numpy(), lags)
        mism1.append(float(np.max(np.abs(s1_spear - real1_spear))))
        mism2.append(float(np.max(np.abs(s2_spear - real2_spear))))
        surr_crosscorr0 = float(np.corrcoef(pd.Series(x1_surr).rank(), pd.Series(x2_surr).rank())[0, 1])
        crosscorr_mism.append(abs(surr_crosscorr0 - real_crosscorr0))

    mism1, mism2 = np.array(mism1), np.array(mism2)
    crosscorr_mism = np.array(crosscorr_mism)

    diag = dict(
        M=M, lags=lags, burn_in=burn_in,
        garch1=dict(omega=omega1, alpha=alpha1, beta=beta1, persistence=alpha1 + beta1),
        garch2=dict(omega=omega2, alpha=alpha2, beta=beta2, persistence=alpha2 + beta2),
        dcc=dict(a=a, b=b, rho_bar=rho_bar, persistence=a + b),
        resid_arch_diag=dict(max_abs_acf_sq_ch1=resid_sq_acf1, max_abs_acf_sq_ch2=resid_sq_acf2),
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


# ---------------------------------------------------------------------------
# MEM(1,1) + DCC(1,1) -- the fix, and the construction actually delivered as
# `generate_joint_surrogates` below. See module docstring "POST-HOC AMENDMENT".
# ---------------------------------------------------------------------------

DEFAULT_MEM_BURN_IN = 2000


def fit_mem11(x: np.ndarray):
    """Multiplicative Error Model MEM(1,1) on a RAW positive series, QMLE
    under an Exponential(1) working likelihood (Engle-Russell ACD
    convention -- consistent for the conditional mean mu_t regardless of the
    true shock distribution). x_t = mu_t * eta_t, mu_t = omega + alpha*x_{t-1}
    + beta*mu_{t-1}. Returns (omega, alpha, beta, mu, eta)."""
    n = len(x)
    mu0 = float(x.mean())

    def negll(params):
        omega, alpha, beta = params
        if omega <= 0 or alpha < 0 or beta < 0 or alpha + beta >= 0.999:
            return 1e10
        mu = np.empty(n)
        mu[0] = mu0
        for t in range(1, n):
            mu[t] = omega + alpha * x[t - 1] + beta * mu[t - 1]
        if np.any(mu <= 0) or not np.all(np.isfinite(mu)):
            return 1e10
        nll = np.sum(np.log(mu[1:]) + x[1:] / mu[1:])
        return nll if np.isfinite(nll) else 1e10

    x0 = np.array([mu0 * 0.05, 0.1, 0.85])
    res = minimize(negll, x0, method="Nelder-Mead",
                    options=dict(xatol=1e-8, fatol=1e-8, maxiter=8000, maxfev=8000))
    omega, alpha, beta = res.x
    mu = np.empty(n)
    mu[0] = mu0
    for t in range(1, n):
        mu[t] = omega + alpha * x[t - 1] + beta * mu[t - 1]
    eta = x / mu
    return float(omega), float(alpha), float(beta), mu, eta


def _empirical_quantile_map(g: np.ndarray, sample_sorted: np.ndarray) -> np.ndarray:
    """Map standard-normal draws g to the empirical distribution of
    `sample_sorted` (already sorted ascending) via a Gaussian-copula device:
    eta = F^{-1}(Phi(g)), F^{-1} the empirical quantile function (linear
    interpolation on the order statistics)."""
    n = len(sample_sorted)
    u = _norm.cdf(g)
    u = np.clip(u, 0.5 / n, 1 - 0.5 / n)
    pos = u * (n - 1)
    lo = np.floor(pos).astype(int)
    hi = np.ceil(pos).astype(int)
    frac = pos - lo
    return sample_sorted[lo] * (1 - frac) + sample_sorted[hi] * frac


def _simulate_dcc_mem_pair(n, burn_in, rng,
                            omega1, alpha1, beta1, eta1_sorted,
                            omega2, alpha2, beta2, eta2_sorted,
                            a, b, rho_bar):
    T = n + burn_in
    mu1_0 = omega1 / max(1e-10, (1 - alpha1 - beta1))
    mu2_0 = omega2 / max(1e-10, (1 - alpha2 - beta2))

    mu1 = np.empty(T); mu2 = np.empty(T)
    x1 = np.empty(T); x2 = np.empty(T)
    g1 = np.empty(T); g2 = np.empty(T)
    Q11 = np.empty(T); Q22 = np.empty(T); Q12 = np.empty(T)

    Q11[0], Q22[0], Q12[0] = 1.0, 1.0, rho_bar
    rho0 = np.clip(Q12[0] / np.sqrt(Q11[0] * Q22[0]), -0.999, 0.999)
    e1, e2 = rng.standard_normal(2)
    g1[0] = e1
    g2[0] = rho0 * e1 + np.sqrt(1 - rho0 ** 2) * e2

    mu1[0], mu2[0] = mu1_0, mu2_0
    eta1_0 = _empirical_quantile_map(np.array([g1[0]]), eta1_sorted)[0]
    eta2_0 = _empirical_quantile_map(np.array([g2[0]]), eta2_sorted)[0]
    x1[0] = mu1[0] * eta1_0
    x2[0] = mu2[0] * eta2_0

    for t in range(1, T):
        Q11[t] = (1 - a - b) * 1.0 + a * g1[t - 1] ** 2 + b * Q11[t - 1]
        Q22[t] = (1 - a - b) * 1.0 + a * g2[t - 1] ** 2 + b * Q22[t - 1]
        Q12[t] = (1 - a - b) * rho_bar + a * g1[t - 1] * g2[t - 1] + b * Q12[t - 1]
        rho_t = np.clip(Q12[t] / np.sqrt(Q11[t] * Q22[t]), -0.999, 0.999)

        e1, e2 = rng.standard_normal(2)
        g1[t] = e1
        g2[t] = rho_t * e1 + np.sqrt(1 - rho_t ** 2) * e2

        mu1[t] = omega1 + alpha1 * x1[t - 1] + beta1 * mu1[t - 1]
        mu2[t] = omega2 + alpha2 * x2[t - 1] + beta2 * mu2[t - 1]
        if mu1[t] <= 0:
            mu1[t] = 1e-6
        if mu2[t] <= 0:
            mu2[t] = 1e-6

        eta1_t = _empirical_quantile_map(np.array([g1[t]]), eta1_sorted)[0]
        eta2_t = _empirical_quantile_map(np.array([g2[t]]), eta2_sorted)[0]
        x1[t] = mu1[t] * eta1_t
        x2[t] = mu2[t] * eta2_t

    return x1[burn_in:], x2[burn_in:]


def _mean_realized_crosscorr(n, burn_in, seed_base, code, n_draws,
                              omega1, alpha1, beta1, eta1_sorted,
                              omega2, alpha2, beta2, eta2_sorted,
                              a, b, rho_bar):
    corrs = []
    for i in range(n_draws):
        rng = np.random.default_rng([seed_base, code, i, 777])
        x1s, x2s = _simulate_dcc_mem_pair(
            n, burn_in, rng, omega1, alpha1, beta1, eta1_sorted,
            omega2, alpha2, beta2, eta2_sorted, a, b, rho_bar,
        )
        corrs.append(float(np.corrcoef(pd.Series(x1s).rank(), pd.Series(x2s).rank())[0, 1]))
    return float(np.mean(corrs))


def _calibrate_rho_bar(n, burn_in, seed_base, code, target_corr,
                        omega1, alpha1, beta1, eta1_sorted,
                        omega2, alpha2, beta2, eta2_sorted,
                        a, b, rho_bar_init, n_calib_draws=10, max_iter=10, tol=0.01):
    """The MEM multiplicative recursion + empirical-quantile-copula chain
    dampens whatever correlation is injected at the shock (u1,u2) level --
    the realized rank cross-correlation of the SIMULATED raw channels comes
    out systematically below `rho_bar` itself (confirmed empirically: raw
    shock corr 0.665 -> realized simulated corr ~0.646, and matching the real
    0.772 target requires rho_bar ~0.79-0.80, not 0.665). Bisection search on
    rho_bar (monotonic in the realized correlation, confirmed empirically
    over a coarse grid) rather than trusting the shock-level correlation
    directly -- a legitimate calibration/targeting step, not a different
    lens."""
    lo, hi = 0.05, 0.995
    f_lo = _mean_realized_crosscorr(n, burn_in, seed_base, code, n_calib_draws,
                                     omega1, alpha1, beta1, eta1_sorted,
                                     omega2, alpha2, beta2, eta2_sorted, a, b, lo) - target_corr
    f_hi = _mean_realized_crosscorr(n, burn_in, seed_base, code, n_calib_draws,
                                     omega1, alpha1, beta1, eta1_sorted,
                                     omega2, alpha2, beta2, eta2_sorted, a, b, hi) - target_corr
    if f_lo > 0 or f_hi < 0:
        # target outside the achievable range at the search bracket -- return
        # whichever endpoint is closer, disclosed via the returned flag.
        return (lo if abs(f_lo) < abs(f_hi) else hi), False

    mid = rho_bar_init
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        f_mid = _mean_realized_crosscorr(n, burn_in, seed_base, code, n_calib_draws,
                                          omega1, alpha1, beta1, eta1_sorted,
                                          omega2, alpha2, beta2, eta2_sorted, a, b, mid) - target_corr
        if abs(f_mid) <= tol:
            break
        if f_mid < 0:
            lo = mid
        else:
            hi = mid
    return mid, True


def generate_joint_surrogates(x1: np.ndarray, x2: np.ndarray, M: int, seed_base: int,
                               code: int, acf_lags: int = ACF_LAGS,
                               burn_in: int = DEFAULT_MEM_BURN_IN):
    """PRIMARY delivered DCC lens construction: MEM(1,1) per channel (own-level
    persistence, fit on RAW positive data) + DCC(1,1) on the normal-scored
    recovered shocks (cross-channel correlation dynamics), simulated jointly
    via a Gaussian-copula empirical-quantile mapping. Required entry point;
    signature/return shape matches `joint_iaaft.generate_joint_surrogates`.
    See module docstring for why this replaces the literal Step-1 spec."""
    n = len(x1)
    assert len(x2) == n
    lags = min(acf_lags, n // 3)

    real1_spear = acf(pd.Series(x1).rank().to_numpy(), lags)
    real2_spear = acf(pd.Series(x2).rank().to_numpy(), lags)
    real_crosscorr0 = float(np.corrcoef(pd.Series(x1).rank(), pd.Series(x2).rank())[0, 1])

    omega1, alpha1, beta1, mu1_fit, eta1 = fit_mem11(x1)
    omega2, alpha2, beta2, mu2_fit, eta2 = fit_mem11(x2)
    eta1_sorted = np.sort(eta1)
    eta2_sorted = np.sort(eta2)

    u1 = normal_scores(eta1)
    u2 = normal_scores(eta2)
    a, b, rho_bar_raw = fit_dcc11(u1, u2)

    rho_bar, calibrated = _calibrate_rho_bar(
        n, burn_in, seed_base, code, real_crosscorr0,
        omega1, alpha1, beta1, eta1_sorted, omega2, alpha2, beta2, eta2_sorted,
        a, b, rho_bar_raw,
    )

    pairs = []
    mism1, mism2, crosscorr_mism = [], [], []
    for i in range(M):
        rng = np.random.default_rng([seed_base, code, i])
        x1_surr_raw, x2_surr_raw = _simulate_dcc_mem_pair(
            n, burn_in, rng,
            omega1, alpha1, beta1, eta1_sorted,
            omega2, alpha2, beta2, eta2_sorted,
            a, b, rho_bar,
        )

        x1_sorted = np.sort(x1)
        ranks1 = np.empty(n, dtype=int)
        ranks1[np.argsort(x1_surr_raw, kind="stable")] = np.arange(n)
        x1_surr = x1_sorted[ranks1]

        x2_sorted = np.sort(x2)
        ranks2 = np.empty(n, dtype=int)
        ranks2[np.argsort(x2_surr_raw, kind="stable")] = np.arange(n)
        x2_surr = x2_sorted[ranks2]

        assert np.array_equal(np.sort(x1_surr), x1_sorted), "channel-1 multiset identity violated"
        assert np.array_equal(np.sort(x2_surr), x2_sorted), "channel-2 multiset identity violated"

        pairs.append((x1_surr, x2_surr))

        s1_spear = acf(pd.Series(x1_surr).rank().to_numpy(), lags)
        s2_spear = acf(pd.Series(x2_surr).rank().to_numpy(), lags)
        mism1.append(float(np.max(np.abs(s1_spear - real1_spear))))
        mism2.append(float(np.max(np.abs(s2_spear - real2_spear))))
        surr_crosscorr0 = float(np.corrcoef(pd.Series(x1_surr).rank(), pd.Series(x2_surr).rank())[0, 1])
        crosscorr_mism.append(abs(surr_crosscorr0 - real_crosscorr0))

    mism1, mism2 = np.array(mism1), np.array(mism2)
    crosscorr_mism = np.array(crosscorr_mism)

    diag = dict(
        M=M, lags=lags, burn_in=burn_in, construction="MEM(1,1)+DCC(1,1)",
        mem1=dict(omega=omega1, alpha=alpha1, beta=beta1, persistence=alpha1 + beta1, mean_eta=float(eta1.mean())),
        mem2=dict(omega=omega2, alpha=alpha2, beta=beta2, persistence=alpha2 + beta2, mean_eta=float(eta2.mean())),
        dcc=dict(a=a, b=b, rho_bar_raw_shock_corr=rho_bar_raw, rho_bar_calibrated=rho_bar,
                  calibration_converged=calibrated, persistence=a + b),
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
    import json

    df = pd.read_csv("../mnq_dailygeom_notice_2026-08-29/candidate24_joint_frame.csv")
    x1 = df["on_range"].to_numpy(dtype=float)
    x2 = df["rth_range"].to_numpy(dtype=float)

    print("=== Attempt 1: literal Step-1 spec (GARCH(1,1) on normal-scored channel, mean='Zero') ===")
    _, diag_literal = generate_joint_surrogates_zeromean_literal(x1, x2, M=30, seed_base=7, code=0)
    print(json.dumps(diag_literal, indent=2))

    print()
    print("=== Attempt 2 (delivered, generate_joint_surrogates): MEM(1,1) + DCC(1,1) fix ===")
    pairs, diag = generate_joint_surrogates(x1, x2, M=30, seed_base=7, code=1)
    print(json.dumps(diag, indent=2))
