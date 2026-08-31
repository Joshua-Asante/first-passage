"""Round 4 (ratified bounded round, 2026-08-30) -- model-adequacy remedy #2:
formal information-criterion (AIC/BIC) comparison between ARFIMA(1,d,0) and
finite-order short-memory AR(p) competitors, via the WHITTLE (frequency-
domain approximate) likelihood.

Built and run ONLY because remedy #1 (oos_forecast_evaluation.py) did not
clear its own pre-registered criterion -- see that file's printed
"OVERALL VERDICT" and this round's RESULTS.md entry. This is the SECOND and,
per the ratified bounded-round mandate, LAST candidate remedy this round may
try before a hard stop, regardless of outcome.

WHY WHITTLE, NOT AN EXACT GAUSSIAN LIKELIHOOD: an exact Gaussian likelihood
for ARFIMA(1,d,0) requires either a Durbin-Levinson recursion against the
process's own theoretical autocovariance (numerically fine at this n, but a
separate, non-trivial implementation) or direct numerical integration. The
Whittle (1953) approximate likelihood -- standard in the applied long-memory
literature specifically BECAUSE it handles slowly-decaying long-memory
autocovariances cleanly via the spectral density, and is the estimator Fox
& Taqqu (1986) use for ARFIMA -- needs only each candidate model's spectral
density function and the sample periodogram (via FFT), and is used here
UNIFORMLY for every candidate model (not just ARFIMA) so all AIC/BIC values
in the comparison table are computed under the identical likelihood
framework -- avoiding an apples-to-oranges comparison where short-memory
models get an exact likelihood and the long-memory model gets an
approximate one.

CANDIDATES (univariate, per channel -- see "why univariate" below):
  - ARFIMA(1,d,0): genuine 2-D Whittle-MLE grid search over (phi, d),
    profiling out the innovation variance sigma^2 in closed form (the
    standard Whittle concentration trick -- derived in this file's own
    `whittle_neg2loglik` docstring). k=3 free parameters (phi, d, sigma^2).
  - AR(p) for p in {1, 5, 10, 20}: phi's obtained via fast, exact OLS
    (asymptotically Whittle-equivalent for a correctly-specified AR(p); a
    fresh Whittle grid search over 20 dimensions for AR(20) would be
    expensive and unnecessary since OLS already gives a consistent
    estimator), then EVALUATED under the same Whittle likelihood machinery
    (same periodogram, same profiled-sigma^2 formula) so its AIC/BIC is
    directly comparable to ARFIMA's. k=p+1 free parameters (p AR
    coefficients, sigma^2 -- the series is demeaned before periodogram
    computation, so no separate intercept parameter is Whittle-relevant).

WHY UNIVARIATE, NOT THE BIVARIATE VAR(20): the property under dispute
(RESULTS.md Round 1: does a finite-order linear model reproduce the real
series' own long-memory "plateau" ACF shape) is fundamentally a per-channel,
own-dynamics question -- VAR(20)'s own diagnostic failure in RESULTS.md was
specifically about each channel's OWN autocorrelation, not the cross-channel
link. A univariate AR(20) vs ARFIMA(1,d,0) comparison targets the identical
own-dynamics question directly, without the added complexity of a bivariate
cross-spectral density for the copula-linked construction (which would need
its own new derivation and would not change what this remedy is testing).

LEAKAGE / DATA DISCIPLINE: uses the IDENTICAL TRAIN split (first 80%,
n_train=1189, chronological) and the IDENTICAL log-range transform as
oos_forecast_evaluation.py, for direct consistency between this round's two
remedies -- not a fresh data-handling decision. TEST data is never touched
(an IC comparison is inherently in-sample/train-fit; that is what "formal
information-criterion-based comparison... rather than an absolute
ACF-percentile check" in RESULTS.md's own recommendation means -- IC
comparison is a within-sample fit-quality-vs-complexity tradeoff test, a
different kind of check than the OOS remedy, not a redundant one).

SCOPE: this remedy's evidence is MNQ-only (Codex review, PR #225 finding
#7). It is fit and scored exclusively against `candidate24_joint_frame.csv`
(MNQ's own joint frame) and does not evaluate whether ARFIMA(1,d,0)
represents MYM's own panel, or MYM's separately-restricted `bprime=0`
subpanel -- both differently-distributed inputs this construct's eventual
Phase 3 execution also needs. Per the "one design run twice" framing this
brief's own §7 already establishes (Phase 1 design/certification happens
once, Phase 3 execution runs the certified design against each instrument's
own cached frame), a Phase 1 clearance on MNQ licenses ATTEMPTING the same
design on MYM at Phase 3 -- it does NOT itself certify MYM's own model
adequacy, which would need its own instance of this same check before that
instrument's Phase 3 result could be trusted with the same confidence.

SECOND, MORE FUNDAMENTAL SCOPE LIMITATION (Codex review, PR #225 third
pass -- disclosed, NOT fixed with new code; see "why not fixed" below):
this remedy (and remedy 1, oos_forecast_evaluation.py) fits and tests an
ARFIMA(1,d,0) model DIRECTLY on log-range Pearson dynamics, with NO
rank-remap step. The PRODUCTION construction this Phase 1 design would
actually deploy (`_fit_real_params.py`, `longmemory_copula.py`) is
different in kind, not just in estimation method: it calibrates (phi,d)
against the RANK/Spearman ACF (`acf(rankdata(x))`), and its surrogate
generator subsequently RANK-REMAPS the fitted latent Gaussian process onto
the real raw marginal distribution (`_remap_to_raw`, exact order-statistic
matching). A monotone log transform preserves ranks but NOT Pearson
autocorrelation or residual whiteness -- so THIS remedy's pass/fail result
characterizes a related but DISTINCT log-Pearson model, not the production
rank-based ARFIMA+copula+remap construction. Failure here does not, by
itself, prove the production construction is ALSO inadequate; success here
would not, by itself, have proven the production construction adequate
either.

WHY THIS IS DISCLOSED RATHER THAN FIXED WITH A THIRD REMEDY: the ratified
bounded-round mandate caps model-adequacy work at 2 candidate remedies,
already spent (remedy 1: OOS forecast; remedy 2: this file). Building a
rank-scale version of this exact check would be a THIRD attempt, which the
hard-stop discipline this round is built around explicitly forbids
regardless of how well-motivated it is. The honest, disclosed conclusion
given this gap: model adequacy has NOT been established for the
production construction by either remedy -- if anything, the case for
proceeding is WEAKER than "two remedies actively falsified the production
model," it is "neither of the two attempted remedies say anything precise
about it either way, and both nonetheless failed on the closely-related
model they DID test." This does not soften the Round 4 hard-stop
disposition; it is an additional reason the disposition holds.

TWO-PART PASS CRITERION (fixed here, before any number below the FIXES
described next was computed -- Codex review, PR #225 finding #6, corrected
the original one-part criterion described below):

  ORIGINAL (pre-review) criterion -- MODEL ADEQUACY CLEARS if, on BOTH
  channels, ARFIMA(1,d,0) achieves the LOWEST BIC among all five candidates.
  Codex's finding #6 is correct and load-bearing: an information criterion
  is a RELATIVE model-selection tool, not an absolute goodness-of-fit test
  -- if every candidate misrepresents the real dynamics, one of them still
  necessarily "wins" BIC, and the two positive-control self-tests below
  cannot detect that failure mode because their own ground truths are
  members of the candidate set by construction. Relative-BIC-best alone
  does not discharge "does the fitted model represent the real data well
  enough to trust."

  CORRECTED criterion (this version) -- MODEL ADEQUACY CLEARS (via this
  remedy, on MNQ) only if BOTH, on BOTH channels:
    (a) RELATIVE: ARFIMA(1,d,0) achieves the lowest BIC among all five
        candidates (BIC, not AIC, for its stronger complexity penalty --
        unchanged from the original criterion), AND
    (b) ABSOLUTE: a Ljung-Box test on ARFIMA's own in-sample residuals
        (computed via the truncated AR(inf) filter, `ar_inf_pi_weights`,
        reused from oos_forecast_evaluation.py) at lag=30 does NOT reject
        the null of no residual autocorrelation (p > 0.05) -- i.e. after
        fitting ARFIMA(1,d,0), what remains looks like white noise, a
        genuine absolute adequacy signal independent of what it is being
        compared against. The SAME test is also run (disclosed, not
        gating) on the closest AR(p) competitor, to confirm this check has
        real discriminating power rather than passing everything.

  Two positive-control self-tests (true-AR(1) data; true-long-memory data)
  are run and their results PERSISTED in this file's own output BEFORE the
  real-data section runs (Codex review, PR #225 finding #3 -- these were
  previously run as throwaway, uncommitted ad hoc commands, so the
  load-bearing claim that this machinery discriminates in both directions
  was not actually reproducible from the repo). `main()` aborts with a
  clear error if either self-test fails.

  If ARFIMA does not clear BOTH (a) and (b) on both channels, model
  adequacy is NOT established via this remedy either. Per the ratified
  bounded round, this is remedy #2 of at most 2 -- a fail here triggers the
  hard stop (disclose the Q-RANGEXFER-1 §6 gate-table gap), not a third
  attempt.

CORRECTIONS (Codex review, PR #225 -- each independently re-verified before
fixing, per this repo's own standing discipline). In addition to findings
#3, #6, #7 above: **finding #5, a real scaling bug in `whittle_neg2loglik`**
-- an earlier version of that function computed -logL (verified by
re-deriving the Whittle profiling identity from scratch), not -2logL, and
the caller then applied the standard 2k/k*log(n) AIC/BIC penalties as if it
were -2logL, halving the fit term's weight relative to the penalty. FIXED
at the single source of truth (the function itself). Re-derived by hand
whether this changes which model wins BEFORE re-running anything: ARFIMA's
fit-term (raw likelihood) advantage over its closest competitor was
ALREADY favorable pre-fix (ARFIMA's own -logL was lower than AR(5)'s
despite AR(5) having more parameters); doubling the fit term relative to a
penalty term that is unaffected by this fix makes that pre-existing
advantage COUNT FOR MORE, not less -- so this fix was expected to widen
ARFIMA's BIC margin, not overturn the verdict, and the re-run below
confirms that expectation rather than being run blind to it.

SECOND-PASS CORRECTIONS (Codex review, PR #225, second review round on the
first round's own fixes -- both independently re-verified before fixing):

- **Ljung-Box degrees of freedom.** `acorr_ljungbox` was called with its
  default `model_df=0`, but ARFIMA's own residuals come from a model with 2
  fitted dynamic parameters (phi, d) -- the default overstates the
  p-value. Verified directly before fixing: at `model_df=2`, `rth_range`'s
  own lag-30 p drops from 0.0734 to 0.0446, flipping it from PASS to FAIL.
  Fixed for both the ARFIMA residual check (`model_df=2`) and the
  competitor AR(p) residual check (`model_df=p`, that competitor's own
  fitted coefficient count) -- both were previously using the wrong (too
  generous) default.
- **The residual-machinery validation and multi-lag robustness table were
  never actually committed anywhere** -- the same class of defect finding
  #3 already found and fixed once in this file, recurring in a NEW check
  added mid-correction. Fixed by implementing `residual_diagnostic_self_
  test` (validates the Ljung-Box/residual machinery against known-true
  parameters, per channel) and `residual_multilag_table` (the 5/10/15/20/
  25/30-lag table) as real functions, called from `main()` and persisted
  in this file's own JSON output alongside the real-data result.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from longmemory_copula import ar1_fracdiff_weights, _causal_filter  # noqa: E402 -- self-test generative model
from oos_forecast_evaluation import ar_inf_pi_weights  # noqa: E402 -- reused AR(inf) truncated-filter (same directory, not cross-directory)

CSV = HERE.parent / "mnq_dailygeom_notice_2026-08-29" / "candidate24_joint_frame.csv"
TRAIN_FRAC = 0.80
RESID_J = 500   # AR(inf) truncation for the residual-whiteness check -- SAME as oos_forecast_evaluation.py's J_TRUNC
LJUNG_BOX_LAG = 30   # SAME as ACF_LAGS convention used throughout this directory


def periodogram(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Sample periodogram I(w_j) = |FFT(x)[j]|^2 / (2*pi*n) at Fourier
    frequencies w_j = 2*pi*j/n, j=1..floor((n-1)/2) (excludes j=0, the
    sample mean; `x` must already be demeaned). Returns (freqs, I)."""
    n = len(x)
    m = (n - 1) // 2
    fft_x = np.fft.fft(x)
    I = (np.abs(fft_x[1: m + 1]) ** 2) / (2 * np.pi * n)
    freqs = 2 * np.pi * np.arange(1, m + 1) / n
    return freqs, I


def g_arfima(freqs: np.ndarray, phi: float, d: float) -> np.ndarray:
    """Normalized (unit-innovation-variance) spectral density of
    ARFIMA(1,d,0), matching this directory's own model convention
    ((1-phi*L) X_t = (1-L)^(-d) e_t, longmemory_copula.ar1_fracdiff_weights):
    g(w) = (2*sin(w/2))^(-2d) / |1 - phi*e^{-iw}|^2
         = (2*sin(w/2))^(-2d) / (1 - 2*phi*cos(w) + phi^2)."""
    frac_part = (2.0 * np.sin(freqs / 2.0)) ** (-2.0 * d)
    ar_part = 1.0 - 2.0 * phi * np.cos(freqs) + phi ** 2
    return frac_part / ar_part


def g_ar_p(freqs: np.ndarray, phis: np.ndarray) -> np.ndarray:
    """Normalized spectral density of AR(p) with coefficients `phis`
    (phis[0]=phi_1, ..., phis[p-1]=phi_p): g(w) = 1/|1 - sum_k phi_k e^{-iwk}|^2."""
    p = len(phis)
    k = np.arange(1, p + 1)
    # (m, p) matrix of e^{-i*w_j*k}
    expo = np.exp(-1j * np.outer(freqs, k))
    poly = 1.0 - expo @ phis
    return 1.0 / (np.abs(poly) ** 2)


def whittle_neg2loglik(I: np.ndarray, g: np.ndarray) -> tuple[float, float]:
    """Concentrated (profiled-sigma^2) Whittle -2*log-likelihood.

    CORRECTED (Codex review, PR #225 -- re-derived by hand from scratch
    before fixing, not just multiplied in on faith): the asymptotic Whittle
    log-DENSITY of an independent periodogram ordinate I_j ~ Exp(mean=f_j)
    is log p(I_j) = -log(f_j) - I_j/f_j, so
        logL(theta) = -sum_j[log(f_j) + I_j/f_j]   (this is -logL, NOT -2logL)
    With f_j = sigma^2 * g_j and profiling out sigma^2 (sigma2_hat =
    mean(I/g), unchanged by this fix), the concentrated NEGATIVE
    log-likelihood (still -logL, one factor of 2 short of what AIC/BIC need)
    is -logL = m*log(sigma2_hat) + sum(log(g)) + m. An earlier version of
    this function returned exactly that value under the name
    `neg2loglik` and the caller then added the standard `2k`/`k*log(n)`
    penalties as if it were `-2*logL` -- effectively halving the fit term's
    weight relative to the penalty term. FIXED: multiply by 2 here, at the
    single source of truth, so every caller downstream gets the correctly-
    scaled -2*logL without needing its own compensating factor.
    Returns (neg2loglik, sigma2_hat) where neg2loglik is now genuinely
    -2*logL."""
    m = len(I)
    ratio = I / g
    sigma2_hat = float(np.mean(ratio))
    sigma2_hat = max(sigma2_hat, 1e-12)
    neg_loglik = m * np.log(sigma2_hat) + float(np.sum(np.log(g))) + m
    neg2ll = 2.0 * neg_loglik
    return neg2ll, sigma2_hat


def fit_ar_p_ols(x: np.ndarray, p: int) -> np.ndarray:
    """OLS fit of a zero-intercept AR(p) on a DEMEANED series x (matching
    the periodogram's own zero-mean assumption -- no separate intercept
    term is fit or needed): x_t = sum_k phi_k x_{t-k} + e_t. Returns phis
    (length p)."""
    n = len(x)
    X = np.column_stack([x[p - k: n - k] for k in range(1, p + 1)])
    y = x[p:]
    phis, *_ = np.linalg.lstsq(X, y, rcond=None)
    return phis


def fit_arfima_whittle(freqs: np.ndarray, I: np.ndarray,
                        phi_grid: np.ndarray, d_grid: np.ndarray) -> tuple[float, float, float, float]:
    """Grid-search Whittle MLE for ARFIMA(1,d,0): minimize the concentrated
    -2*logL over (phi, d). Returns (phi_hat, d_hat, neg2ll, sigma2_hat)."""
    best = (None, None, np.inf, None)
    for phi in phi_grid:
        for d in d_grid:
            g = g_arfima(freqs, phi, d)
            neg2ll, sigma2 = whittle_neg2loglik(I, g)
            if neg2ll < best[2]:
                best = (phi, d, neg2ll, sigma2)
    return best


def _bic_table(x_demeaned: np.ndarray, phi_grid: np.ndarray, d_grid: np.ndarray, ar_orders: list[int]) -> dict:
    """Shared BIC-table computation for both the self-test and the real-data
    run -- factored out so the two paths cannot silently diverge in method."""
    n = len(x_demeaned)
    freqs, I = periodogram(x_demeaned)
    phi_hat, d_hat, neg2ll_a, sigma2_a = fit_arfima_whittle(freqs, I, phi_grid, d_grid)
    bics = {"arfima": neg2ll_a + 3 * np.log(n)}
    aics = {"arfima": neg2ll_a + 6}
    for p in ar_orders:
        phis = fit_ar_p_ols(x_demeaned, p)
        g = g_ar_p(freqs, phis)
        neg2ll, _ = whittle_neg2loglik(I, g)
        k = p + 1
        bics[f"ar{p}"] = neg2ll + k * np.log(n)
        aics[f"ar{p}"] = neg2ll + 2 * k
    return dict(phi_hat=phi_hat, d_hat=d_hat, bics=bics, aics=aics,
                best_bic=min(bics, key=bics.get))


def self_test() -> dict:
    """Two positive-control sanity checks -- PERSISTED here (Codex review,
    PR #225 finding #3), not run as throwaway ad hoc commands. Both must
    PASS before `main()` trusts the real-data run. See module docstring
    "TWO-PART PASS CRITERION" for what each check establishes."""
    phi_grid = np.linspace(-0.9, 0.95, 60)
    d_grid = np.linspace(0.001, 0.499, 60)
    ar_orders = [1, 5, 10, 20]
    n = 1200

    # Check 1: true AR(1), phi=0.6 -- machinery must NOT invent long memory
    # and must correctly prefer the true (parsimonious) model.
    rng1 = np.random.default_rng(42)
    x1 = np.zeros(n)
    for t in range(1, n):
        x1[t] = 0.6 * x1[t - 1] + rng1.normal()
    x1 = x1 - x1.mean()
    r1 = _bic_table(x1, phi_grid, d_grid, ar_orders)
    check1_pass = bool(r1["best_bic"] == "ar1" and r1["d_hat"] < 0.10)

    # Check 2: true ARFIMA(1,-0.3,0.42) -- machinery must correctly prefer
    # the true long-memory model over every short-memory competitor, by a
    # decisive margin.
    rng2 = np.random.default_rng(7)
    burn = 800
    psi = ar1_fracdiff_weights(-0.3, 0.42, burn)
    e = rng2.standard_normal(n + burn)
    x2 = _causal_filter(e, psi)[burn: burn + n]
    x2 = x2 - x2.mean()
    r2 = _bic_table(x2, phi_grid, d_grid, ar_orders)
    next_best_bic2 = sorted(v for k, v in r2["bics"].items() if k != "arfima")[0]
    margin2 = next_best_bic2 - r2["bics"]["arfima"]
    check2_pass = bool(r2["best_bic"] == "arfima" and margin2 > 5.0)   # decisive margin, not a coin-flip win

    out = dict(
        check1_true_ar1=dict(phi_true=0.6, d_hat=r1["d_hat"], phi_hat=r1["phi_hat"],
                              bics=r1["bics"], best_bic=r1["best_bic"], passes=check1_pass),
        check2_true_longmemory=dict(phi_true=-0.3, d_true=0.42, phi_hat=r2["phi_hat"], d_hat=r2["d_hat"],
                                     bics=r2["bics"], best_bic=r2["best_bic"],
                                     margin_over_next_best=margin2, passes=check2_pass),
        both_pass=bool(check1_pass and check2_pass),
    )
    print("SELF-TEST 1 (true AR(1), phi=0.6): best_bic=%s d_hat=%.4f -> %s" %
          (r1["best_bic"], r1["d_hat"], "PASS" if check1_pass else "FAIL"))
    print("SELF-TEST 2 (true ARFIMA(1,-0.3,0.42)): best_bic=%s margin=%.2f -> %s" %
          (r2["best_bic"], margin2, "PASS" if check2_pass else "FAIL"))
    return out


def arfima_ar_inf_residuals(x_demeaned: np.ndarray, phi: float, d: float, J: int) -> np.ndarray:
    """In-sample residuals of the fitted ARFIMA(1,d,0) via the truncated
    AR(inf) filter (`ar_inf_pi_weights`, reused from
    oos_forecast_evaluation.py): e_hat_t = x_t - X_hat_t where X_hat_t is
    the one-step-ahead conditional mean using REAL past values (in-sample,
    not iterated/forecasted). Drops the first J-1 points (no full lag
    history available for those)."""
    pi = ar_inf_pi_weights(phi, d, J)
    n = len(x_demeaned)
    resid = []
    for t in range(J - 1, n):
        lagged = x_demeaned[t - (J - 1): t][::-1]
        pred = -float(np.dot(pi[1:], lagged))
        resid.append(x_demeaned[t] - pred)
    return np.array(resid)


def ar_p_residuals(x_demeaned: np.ndarray, phis: np.ndarray) -> np.ndarray:
    """OLS residuals of a fitted (zero-intercept) AR(p) -- verbatim
    computation `fit_ar_p_ols` already performs internally, exposed here so
    the residual-whiteness check can reuse the SAME fitted `phis`."""
    p = len(phis)
    n = len(x_demeaned)
    X = np.column_stack([x_demeaned[p - k: n - k] for k in range(1, p + 1)])
    y = x_demeaned[p:]
    return y - X @ phis


def residual_diagnostic_self_test(phi: float, d: float, n: int = 1189, n_reps: int = 10,
                                   seed: int = 999) -> dict:
    """PERSISTED validation of the residual/Ljung-Box machinery (Codex
    review, PR #225 second pass -- this had previously only been run as an
    uncommitted ad hoc check, the same class of defect as finding #3):
    at TRUE (phi,d), the Ljung-Box test on `arfima_ar_inf_residuals` should
    reject at close to its own nominal ~5% rate (a correctly-specified
    model's own residuals should look like white noise), not confirm
    spurious structure. Run once per channel, using THAT channel's own
    fitted (phi,d) as the "true" parameter for the check (directly relevant
    to whether the machinery is trustworthy on the exact real-data regime
    being tested, not a generic unrelated parameter set).

    CORRECTED (Codex review, PR #225 third pass): this control feeds the
    KNOWN true (phi,d) directly into the residual filter -- no parameters
    are estimated from each synthetic replicate here (unlike the real-data
    usage, which fits phi,d first). `model_df` must reflect degrees of
    freedom actually CONSUMED by estimation in the specific test being run,
    not the real-data usage's own count. Verified directly before fixing:
    at model_df=2 (wrong here), `on_range`'s persisted run showed 1/10
    rejections; at model_df=0 (correct -- zero parameters estimated in
    this loop), it is 0/10, both close to the test's own 5% nominal rate.
    Fixed to model_df=0."""
    burn = 800
    psi = ar1_fracdiff_weights(phi, d, burn)
    rng = np.random.default_rng(seed)
    p_values = []
    for _ in range(n_reps):
        e = rng.standard_normal(n + burn)
        x = _causal_filter(e, psi)[burn: burn + n]
        x = x - x.mean()
        resid = arfima_ar_inf_residuals(x, phi, d, RESID_J)
        lb = acorr_ljungbox(resid, lags=[LJUNG_BOX_LAG], model_df=0, return_df=True)
        p_values.append(float(lb["lb_pvalue"].iloc[0]))
    reject_rate = sum(p <= 0.05 for p in p_values) / n_reps
    return dict(phi=phi, d=d, n=n, n_reps=n_reps, p_values=p_values, reject_rate=reject_rate,
                note="machinery-validation check: a correctly-specified model's own residuals "
                     "should reject at roughly this test's own nominal rate, not systematically more")


def residual_multilag_table(x_demeaned: np.ndarray, phi: float, d: float, J: int,
                             lags=(5, 10, 15, 20, 25, 30), model_df: int = 2) -> dict:
    """PERSISTED multi-lag robustness table for the real-data residual
    check (Codex review, PR #225 second pass): confirms a single-lag
    Ljung-Box result is not an artifact of the one lag chosen."""
    resid = arfima_ar_inf_residuals(x_demeaned, phi, d, J)
    lb = acorr_ljungbox(resid, lags=list(lags), model_df=model_df, return_df=True)
    return {int(lag): float(p) for lag, p in zip(lags, lb["lb_pvalue"])}


def main():
    st = self_test()
    if not st["both_pass"]:
        raise SystemExit(
            "SELF-TEST FAILED -- the IC/Whittle machinery does not discriminate correctly on "
            "known-truth synthetic data; refusing to trust the real-data run. See self-test "
            "results above."
        )
    print("\nBoth self-tests PASS -- machinery discriminates correctly in both directions.\n")

    df = pd.read_csv(CSV)
    log_on = np.log(df["on_range"].to_numpy())
    log_rth = np.log(df["rth_range"].to_numpy())
    n = len(log_on)
    n_train = int(n * TRAIN_FRAC)
    print(f"n={n} n_train={n_train} (IDENTICAL train split to oos_forecast_evaluation.py)")

    channels = dict(on_range=log_on[:n_train], rth_range=log_rth[:n_train])
    AR_ORDERS = [1, 5, 10, 20]
    phi_grid = np.linspace(-0.6, 0.9, 61)
    d_grid = np.linspace(0.01, 0.499, 60)

    results = {}
    for name, train in channels.items():
        x = train - train.mean()
        freqs, I = periodogram(x)
        n_local = len(x)
        m = len(freqs)
        print(f"\n[{name}] n_train={n_local} m_freqs={m}")

        row = {}
        # ARFIMA(1,d,0) -- genuine Whittle-MLE grid search
        phi_hat, d_hat, neg2ll_arfima, sigma2_arfima = fit_arfima_whittle(freqs, I, phi_grid, d_grid)
        k_arfima = 3
        aic_arfima = neg2ll_arfima + 2 * k_arfima
        bic_arfima = neg2ll_arfima + k_arfima * np.log(n_local)
        row["arfima"] = dict(phi=phi_hat, d=d_hat, sigma2=sigma2_arfima, k=k_arfima,
                              neg2loglik=neg2ll_arfima, aic=aic_arfima, bic=bic_arfima)
        print(f"  ARFIMA(1,d,0): phi={phi_hat:.3f} d={d_hat:.3f} -2logL={neg2ll_arfima:.2f} "
              f"AIC={aic_arfima:.2f} BIC={bic_arfima:.2f}")

        for p in AR_ORDERS:
            phis = fit_ar_p_ols(x, p)
            g = g_ar_p(freqs, phis)
            neg2ll, sigma2 = whittle_neg2loglik(I, g)
            k = p + 1
            aic = neg2ll + 2 * k
            bic = neg2ll + k * np.log(n_local)
            row[f"ar{p}"] = dict(phis=phis.tolist(), sigma2=sigma2, k=k,
                                  neg2loglik=neg2ll, aic=aic, bic=bic)
            print(f"  AR({p}): -2logL={neg2ll:.2f} AIC={aic:.2f} BIC={bic:.2f}")

        results[name] = row

    print("\n" + "=" * 90)
    print(f"{'channel':<10}{'model':>10}{'k':>4}{'-2logL':>12}{'AIC':>12}{'BIC':>12}{'best_BIC?':>12}")
    bic_clears = {}
    for name in channels:
        row = results[name]
        best_model = min(row.keys(), key=lambda k: row[k]["bic"])
        bic_clears[name] = (best_model == "arfima")
        for m_name, r in sorted(row.items(), key=lambda kv: kv[1]["bic"]):
            flag = " <-- BEST" if m_name == best_model else ""
            print(f"{name:<10}{m_name:>10}{r['k']:>4}{r['neg2loglik']:>12.2f}{r['aic']:>12.2f}{r['bic']:>12.2f}{flag:>12}")
        print(f"  [{name}] BIC-best model: {best_model}  (relative BIC test -- ARFIMA lowest: {bic_clears[name]})")

    # ---------------- ABSOLUTE adequacy complement: Ljung-Box on residuals ----------------
    # Codex review, PR #225 finding #6: relative BIC-best does not by itself
    # discharge whether ARFIMA represents the real dynamics well enough to
    # trust (all 5 candidates could be inadequate and one would still win).
    # This checks, on MNQ (see module docstring SCOPE), whether ARFIMA's OWN
    # in-sample residuals are consistent with white noise -- an absolute
    # signal, disclosed alongside (not substituting for) the relative test.
    print("\n" + "=" * 90)
    print(f"ABSOLUTE ADEQUACY CHECK: Ljung-Box on residuals at lag={LJUNG_BOX_LAG} (MNQ)")
    resid_clears = {}
    resid_detail = {}
    for name, train in channels.items():
        x = train - train.mean()
        row = results[name]
        arfima_resid = arfima_ar_inf_residuals(x, row["arfima"]["phi"], row["arfima"]["d"], RESID_J)
        # Codex review, PR #225 second pass: `acorr_ljungbox` defaults to
        # model_df=0, but these residuals come from a model with 2 fitted
        # dynamic parameters (phi, d) -- the default overstates the
        # p-value (too generous). Verified directly before fixing: at
        # model_df=2, rth_range's own lag-30 p drops from 0.0734 to
        # 0.0446, flipping it from PASS to FAIL. Fixed here.
        lb_arfima = acorr_ljungbox(arfima_resid, lags=[LJUNG_BOX_LAG], model_df=2, return_df=True)
        p_arfima = float(lb_arfima["lb_pvalue"].iloc[0])

        # Closest AR(p) competitor (disclosed, not gating) -- confirms this
        # check has real discriminating power, not that it passes everything.
        # Its own residuals come from a model with `p` fitted coefficients.
        competitor = min((k for k in row if k != "arfima"), key=lambda k: row[k]["bic"])
        comp_p = int(competitor.replace("ar", ""))
        comp_phis = np.array(row[competitor]["phis"])
        comp_resid = ar_p_residuals(x, comp_phis)
        lb_comp = acorr_ljungbox(comp_resid, lags=[LJUNG_BOX_LAG], model_df=comp_p, return_df=True)
        p_comp = float(lb_comp["lb_pvalue"].iloc[0])

        # PERSISTED (Codex review, PR #225 second pass finding): the
        # residual-machinery sanity check and the multi-lag robustness
        # table had previously only been run as uncommitted ad hoc checks
        # during authoring -- the same class of defect as finding #3.
        # Both are now computed and saved as part of this script's own run.
        machinery_check = residual_diagnostic_self_test(row["arfima"]["phi"], row["arfima"]["d"],
                                                          n=len(x), seed=999 if name == "on_range" else 998)
        multilag = residual_multilag_table(x, row["arfima"]["phi"], row["arfima"]["d"], RESID_J)

        resid_clears[name] = bool(p_arfima > 0.05)
        resid_detail[name] = dict(arfima_ljungbox_p=p_arfima, n_resid_arfima=len(arfima_resid),
                                   competitor=competitor, competitor_ljungbox_p=p_comp,
                                   n_resid_competitor=len(comp_resid),
                                   machinery_validation=machinery_check, multilag_robustness=multilag)
        print(f"  [{name}] ARFIMA residual Ljung-Box p={p_arfima:.4f} "
              f"({'PASS -- consistent with white noise' if resid_clears[name] else 'FAIL -- residual structure remains'}) | "
              f"{competitor} (closest competitor) residual Ljung-Box p={p_comp:.4f} "
              f"({'also white' if p_comp > 0.05 else 'still shows structure -- confirms discriminating power'})")
        print(f"    machinery validation (10 reps @ true params): reject_rate={machinery_check['reject_rate']:.2f} "
              f"(expect close to nominal ~0.05-0.10 if machinery is trustworthy)")
        print(f"    multi-lag robustness: {multilag}")

    clears = {name: bool(bic_clears[name] and resid_clears[name]) for name in channels}
    for name in channels:
        print(f"  [{name}] CLEARS (relative BIC-best AND absolute residual-whiteness): {clears[name]}")

    overall_clears = all(clears.values())
    verdict = "MODEL ADEQUACY CLEARS on MNQ (remedy 2: information-criterion comparison)" if overall_clears else \
        "MODEL ADEQUACY DOES NOT CLEAR via remedy 2 either -- both candidate remedies exhausted"
    print(f"\nOVERALL VERDICT: {verdict}")

    out = dict(n=n, n_train=n_train, ar_orders=AR_ORDERS, self_test=st, results=results,
               bic_clears_per_channel=bic_clears, residual_whiteness=resid_detail,
               clears_per_channel=clears, overall_clears=overall_clears, verdict=verdict,
               scope="MNQ-only -- see module docstring SCOPE section")
    (HERE / "information_criterion_comparison_results.json").write_text(json.dumps(out, indent=2, default=str))
    print("\nWrote information_criterion_comparison_results.json")


if __name__ == "__main__":
    main()
