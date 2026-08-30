"""Round 4 (ratified bounded round, 2026-08-30 operator ratification) --
model-adequacy remedy #1: MULTI-HORIZON out-of-sample forecast evaluation.

RESULTS.md's own recommendation (Round 2, "Live option B"): "out-of-sample
forecast evaluation (does the fitted model predict held-out range values
better than a naive benchmark?) ... rather than an absolute ACF-percentile
check, which Round 2 showed cannot discriminate at this n." This is that
check, built and run BEFORE deciding whether a second remedy is needed
(per the ratified bounded-round mandate: at most 2 candidate remedies).

WHY MULTI-HORIZON, NOT JUST ONE-STEP-AHEAD (verified against the actual
mechanism, per Rule 0, not assumed): the property Round 2's own ACF gate was
trying to certify is specifically LONG-RANGE dependence -- the real
on_range/rth_range series' rank-ACF stays elevated (~0.24-0.25) from lag 10
through lag 30 rather than decaying to ~0 the way a short-memory AR/VAR
process does. VAR(20)'s own residual-whitening diagnostic PASSES CLEANLY
(RESULTS.md Round 1: "max |ACF(residual)| <= 0.006 at every p tested"),
meaning VAR(20) already captures essentially all of the exploitable ONE-STEP
persistence -- a 1-step-ahead forecast race would very plausibly show
ARFIMA(1,d,0) and VAR(20) performing near-identically, telling us nothing
about the specific property (long-horizon persistence) the null needs to get
right for SIMULATING valid surrogates. The classical, standard way to test
for genuine long memory via forecasting (Ray 1993 and the subsequent ARFIMA-
forecasting literature) is instead to compare LONG-HORIZON forecast skill:
long memory's defining signature is that a correctly-specified long-memory
model retains forecast skill (relative to a no-memory naive benchmark) far
longer than any finite-order short-memory model, whose forecasts decay to
the unconditional mean geometrically. This script tests exactly that
differential-decay-with-horizon signature at h in {1, 5, 10, 20, 40} trading
days ahead, using the KNOWN-INADEQUATE VAR(20) construction (already
established as failing to reproduce the real series' own generative ACF
shape, RESULTS.md Round 1) as a built-in discriminating negative control --
mirroring the "does the gate also pass VAR(20)?" smoking-gun test that
falsified the ensemble/percentile gate redesign. A gate that cannot show
ARFIMA(1,d,0) forecasting BETTER than VAR(20) at long horizons has the same
non-discriminating defect that killed the percentile gate, and this script
is built to detect that outcome honestly, not to manufacture a pass.

LEAKAGE DISCIPLINE (load-bearing, checked explicitly): all model fitting
uses ONLY the first 80% of the panel (chronological TRAIN split); the
remaining 20% (TEST) is never touched during any parameter estimation
(phi, d, AR(1) coefficients, VAR(20) coefficients all fit on TRAIN only).
Evaluation is done in LOG-RANGE space (log(on_range), log(rth_range)),
NOT the rank/normal-score space the rest of this directory's modules use --
deliberately, because normal_scores() as implemented elsewhere ranks the
WHOLE array (train+test together), which would leak each test point's
relative position among held-out data back into its own transformed value.
log() is a strictly monotonic, per-observation transform with no such
leakage, and (verified directly, not assumed) Spearman/rank-based ACF is
invariant under any monotonic transform, so log-range shares the identical
own-series persistence SHAPE (the property under test) as the rank-ACF this
directory's other modules diagnose -- this is a disclosed, principled
adaptation for OOS-cleanliness, not a different claim about the data.

FIXED-PARAMETER, NOT ROLLING-REFIT (disclosed limitation, not hidden): all
four models are fit ONCE on the initial 80% TRAIN window and used to
generate forecasts across the entire TEST window without re-estimation --
the standard "pseudo out-of-sample, fixed specification" design, testing
whether the MODEL SPECIFICATION identified from history generalizes
forward. A rolling/expanding-window refit would be more thorough but adds
substantial compute (a fresh SMM grid search at every origin) for a
question (does this fixed specification generalize) this design already
answers; noted as a possible future robustness extension, not required here.

PRE-COMMITTED PASS CRITERION (fixed here, in this docstring, BEFORE any
number below was computed -- verified by running this file only after
this text was written):

  MODEL ADEQUACY CLEARS if, on BOTH channels (on_range AND rth_range),
  at h=20 AND/OR h=40:
    (a) ARFIMA(1,d,0)'s forecast R-squared relative to the naive
        trailing-60-day-mean benchmark is POSITIVE and exceeds +0.03
        (explains at least 3% of the naive benchmark's residual variance
        -- a real, non-trivial threshold, not "greater than zero"), AND
    (b) a Diebold-Mariano test shows ARFIMA(1,d,0) has SIGNIFICANTLY LOWER
        squared-error loss than BOTH AR(1) and VAR(20) at that same
        horizon, one-sided p < 0.10 (relaxed from the conventional 0.05
        given the coarse power available from ~250 overlapping-origin,
        serially-correlated long-horizon forecast errors -- disclosed,
        not silently tightened after seeing results).

  If neither channel clears both (a) and (b) at h=20 or h=40 -- or ARFIMA
  is significantly WORSE than a competitor at long horizons -- model
  adequacy is NOT established via this remedy, exactly as honestly as
  Round 2's ACF-percentile gate was found not to discriminate. This is
  the FIRST of at most 2 candidate remedies the ratified bounded round
  allows; a fail here does not itself trigger the hard stop, only a fail
  on 2 remedies plus the mandatory positive-control recertification does.

CORRECTIONS (Codex review, PR #225 -- each independently re-verified against
the actual code/math before fixing, per this repo's own standing discipline):
2 real bugs confirmed and fixed. (1) `hash(name)` for the per-channel SMM
seed is salted per Python process by default (PYTHONHASHSEED), making the
fitted (phi,d) and the whole comparison table non-reproducible across runs
-- confirmed materially outcome-relevant (a different hash seed flips
whether on_range clears at h=20). Fixed with per-channel fixed integer
seeds (101/102, matching `_fit_real_params.py`'s own convention). (2) the
fit TARGET passed to `estimate_phi_d_simulated` was the PEARSON ACF of raw
log-range train data, but that estimator's own simulated side ALWAYS scores
candidates against `acf(rankdata(y), ...)` (rank/Spearman ACF) --
quantified directly: max|Pearson-ACF - rank-ACF| = 0.030 (on_range) / 0.045
(rth_range) on this exact train split, meaning the fit minimized mismatched
moments rather than either a genuine rank-ACF or log-Pearson fit. Fixed by
ranking the TRAIN-ONLY data before computing the target -- this does NOT
reopen the leakage concern the log-space design exists to avoid (that
concern is specifically about ranking train+test JOINTLY, as
`normal_scores()` does elsewhere in this directory; ranking train-only data
for a training-time fit target touches no test-period information). Both
fixes require re-running this file; the table in RESULTS.md's own Round 4
section is the corrected, re-run output, not the pre-correction numbers.

SECOND-PASS CORRECTION (Codex review, PR #225, second review round): fixing
(2) above created a NEW inconsistency this file's own forecasting step
never accounted for -- (phi,d) was now calibrated to RANK-ACF, but
`forecast_arinf_path` applies the resulting linear filter directly to RAW
log-range values and scores raw-scale MSE. A monotone rank transform
preserves Spearman correlation, not Pearson autocovariance, so a
rank-calibrated (phi,d) is not, in general, the correct filter for
raw-scale conditional-mean forecasts. FIXED by decoupling from the shared
rank-based helper entirely: `estimate_phi_d_simulated_pearson` (below)
fits (phi,d) via an internal PEARSON-ACF (not rank-ACF) simulated
comparison, matched to a Pearson-ACF target on RAW train data -- fit,
AR(inf) filter, and MSE scoring are now consistently Pearson/raw-scale
throughout this file. `longmemory_copula.estimate_phi_d_simulated` itself
is untouched (Round 2/3's own reproducibility unaffected).

SCOPE LIMITATION, DISCLOSED (Codex review, PR #225, third review round --
NOT fixed with a third remedy; the ratified bounded round caps
model-adequacy work at 2 attempts, both already spent): this remedy fits
and tests an ARFIMA(1,d,0) model DIRECTLY on log-range Pearson dynamics,
with no rank-remap step. The PRODUCTION construction this Phase 1 design
would actually deploy (`_fit_real_params.py`, `longmemory_copula.py`)
calibrates against RANK-ACF and rank-remaps its latent draws onto the real
raw marginal via `_remap_to_raw` -- a genuinely different model, not just a
different estimation method (log preserves ranks, not Pearson
autocovariance). This remedy's near-miss result therefore characterizes a
related but distinct log-Pearson construction, not the production
rank-based one -- disclosed here and in `information_criterion_
comparison.py`'s own identical scope note, and in RESULTS.md /
`Q-RANGEXFER-1`'s own §11. This does not soften the round's own hard-stop
disposition; it is an additional, independent reason it holds (neither
remedy speaks precisely to the production construction's own adequacy
either way, and both nonetheless failed on the model they DID test).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from joint_iaaft import fit_var  # noqa: E402 -- reused verbatim, generic bivariate VAR(p) OLS fit
from longmemory_copula import acf, ar1_fracdiff_weights, _causal_filter  # noqa: E402

CSV = HERE.parent / "mnq_dailygeom_notice_2026-08-29" / "candidate24_joint_frame.csv"
TRAIN_FRAC = 0.80
J_TRUNC = 500                 # AR(inf) truncation length for the ARFIMA forecast filter
VAR_ORDER = 20                # SAME order as joint_iaaft.py's DEFAULT_VAR_ORDER / Round 1's "smoking gun" comparator
WINDOW_NAIVE = 60              # SAME trailing window as the real stage-1 statistic's own WINDOW
HORIZONS = [1, 5, 10, 20, 40]
NW_LAG = lambda h: max(1, h - 1)   # Newey-West truncation lag, standard Diebold-Mariano convention for h-step loss


# ---------------------------------------------------------------------------
# ARFIMA(1,d,0) AR(infinity) truncated representation (NEW machinery, not
# elsewhere in this directory -- longmemory_copula.py only has the MA(inf)
# simulation filter, not the AR(inf) forecasting filter these two are
# different representations of the same fitted model).
# ---------------------------------------------------------------------------

def fracdiff_diff_weights(d: float, J: int) -> np.ndarray:
    """Coefficients b_k of the DIFFERENCING operator (1-L)^d (note: +d, the
    forecasting/AR-side filter -- NOT longmemory_copula.fracdiff_weights,
    which computes (1-L)^(-d), the simulation/MA-side integration filter),
    via the standard, numerically-stable Hosking (1981) recursion:
    b_0=1, b_k = b_{k-1}*(k-1-d)/k. Verified against the direct binomial-
    series expansion for k=0,1,2 by hand before use (b_1=-d, b_2=d(d-1)/2,
    matching (1-L)^d = 1 - d*L + d(d-1)/2*L^2 - ...)."""
    b = np.empty(J)
    b[0] = 1.0
    for k in range(1, J):
        b[k] = b[k - 1] * (k - 1 - d) / k
    return b


def ar_inf_pi_weights(phi: float, d: float, J: int) -> np.ndarray:
    """AR(inf) truncated coefficients pi_1..pi_{J-1} of the ARFIMA(1,d,0)
    process defined (matching longmemory_copula.ar1_fracdiff_weights's own
    docstring convention) as (1-phi*L) X_t = (1-L)^(-d) e_t, equivalently
    pi(L) X_t = e_t with pi(L) = (1-phi*L)(1-L)^d. Returns pi[0]=1 (unused
    in the forecast sum, included for index alignment) through pi[J-1].
    Forecast recursion: X_hat_t = -sum_{j=1}^{J-1} pi[j] * X_{t-j}."""
    b = fracdiff_diff_weights(d, J)
    pi = np.empty(J)
    pi[0] = b[0]
    pi[1:] = b[1:] - phi * b[:-1]
    return pi


def estimate_phi_d_simulated_pearson(real_acf: np.ndarray, n: int, J: int, burn: int,
                                      n_reps: int, seed: int,
                                      phi_grid: np.ndarray, d_grid: np.ndarray) -> tuple[float, float, dict]:
    """PEARSON-ACF simulated-method-of-moments calibration -- a LOCAL variant
    of `longmemory_copula.estimate_phi_d_simulated`, used ONLY in this file.

    Codex review (PR #225, second pass, finding on oos_forecast_evaluation.py
    line 351): the shared `estimate_phi_d_simulated` ALWAYS scores candidate
    (phi,d) against `acf(rankdata(y), ...)` of its simulated draws -- i.e. it
    calibrates in RANK/Spearman space, unconditionally. The earlier fix for
    finding #4 (see this file's own CORRECTIONS section above) made the FIT
    TARGET consistent with that (ranking train-only data before computing
    the target ACF) -- but this file's OWN forecasting step (`forecast_
    arinf_path`) applies the resulting (phi,d)'s linear AR(inf) filter
    directly to RAW (unranked) log-range values and scores raw-scale MSE.
    A monotonic rank transform preserves Spearman correlation but NOT
    Pearson autocovariances or conditional means -- so a (phi,d) pair
    calibrated to match rank-ACF is not, in general, the correct linear
    filter for raw-scale one-step-ahead conditional expectations. Fitting
    the fit target correctly (finding #4) exposed this SECOND, deeper
    inconsistency between the (now rank-consistent) fit and the (always
    raw-scale) forecast.

    FIXED here by decoupling entirely from the shared rank-based helper:
    this function fits (phi,d) via the IDENTICAL grid-search/SMM structure,
    but its own internal simulated-draw comparison uses PEARSON ACF
    (`acf(y, max_lag)`, no rankdata) of RAW simulated values -- matching the
    Pearson-ACF `real_acf` target this file's caller now passes (raw
    log-range, not ranked). Fitting, the AR(inf) forecast filter, and MSE
    scoring are now ALL consistently Pearson/raw-scale throughout this
    file. This is a disclosed, deliberate departure from the rank-based
    convention the REST of this directory uses (chosen because THIS
    remedy specifically forecasts and scores on the raw log-range scale,
    unlike every other module here, which only ever needs rank-preserving
    generative surrogates) -- `longmemory_copula.estimate_phi_d_simulated`
    itself is left untouched, so Round 2/3's own reproducibility is
    unaffected."""
    rng = np.random.default_rng(seed)
    max_lag = len(real_acf)
    best = (None, None, np.inf)
    for phi in phi_grid:
        for d in d_grid:
            psi = ar1_fracdiff_weights(phi, d, J)
            acc = np.zeros(max_lag)
            for _ in range(n_reps):
                e = rng.standard_normal(n + burn)
                y = _causal_filter(e, psi)[burn: burn + n]
                acc += acf(y, max_lag)   # PEARSON ACF -- the fix (no rankdata)
            mean_acf = acc / n_reps
            sse = float(np.sum((mean_acf - real_acf) ** 2))
            if sse < best[2]:
                best = (phi, d, sse)
    phi_best, d_best, sse_best = best
    info = dict(best_sse=sse_best, n_reps=n_reps, J=J, burn=burn,
                phi_grid_lo=float(phi_grid[0]), phi_grid_hi=float(phi_grid[-1]), n_phi=len(phi_grid),
                d_grid_lo=float(d_grid[0]), d_grid_hi=float(d_grid[-1]), n_d=len(d_grid),
                method="simulation_calibrated_pearson")
    return float(phi_best), float(d_best), info


def forecast_arinf_path(pi: np.ndarray, hist: np.ndarray, h: int) -> np.ndarray:
    """Iterated h-step-ahead forecast from a length-(>=J) real history array
    `hist` (hist[-1] = time-t value), using the truncated AR(inf) filter
    `pi` (pi[0]=1 unused, pi[1:] = the J-1 AR weights). At each iterated
    step k=1..h, previously-forecasted values stand in for the not-yet-
    observed lags within the horizon (standard iterated multi-step linear
    forecasting) -- returns the h forecasted values X_hat_{t+1}..X_hat_{t+h}."""
    J = len(pi)
    ext = list(hist[-(J - 1):]) if len(hist) >= J - 1 else [hist[0]] * (J - 1 - len(hist)) + list(hist)
    out = np.empty(h)
    for k in range(h):
        # ext[-1] is the most recent known/forecasted value (lag 1)
        lagged = np.array(ext[-(J - 1):][::-1])  # lag1..lag(J-1), most-recent first
        val = -float(np.dot(pi[1:], lagged))
        out[k] = val
        ext.append(val)
    return out


def forecast_linear_path(c: np.ndarray | float, A_list, hist, h: int, univariate: bool = False):
    """Iterated h-step-ahead forecast for a finite-order linear AR(p) (
    univariate=True, c scalar, A_list a list of scalars) or VAR(p)
    (univariate=False, c a (2,) vector, A_list a list of (2,2) matrices).
    hist: last >=p rows/values of REAL data (most-recent last)."""
    p = len(A_list)
    if univariate:
        ext = list(hist[-p:])
        out = np.empty(h)
        for k in range(h):
            val = c
            for lag in range(1, p + 1):
                val = val + A_list[lag - 1] * ext[-lag]
            out[k] = val
            ext.append(val)
        return out
    else:
        ext = [row.copy() for row in hist[-p:]]
        out = np.empty((h, 2))
        for k in range(h):
            val = c.copy()
            for lag in range(1, p + 1):
                val = val + A_list[lag - 1] @ ext[-lag]
            out[k] = val
            ext.append(val)
        return out


def fit_ar1(x: np.ndarray) -> tuple[float, float]:
    """OLS fit of x_t = c + phi*x_{t-1} + e_t. Returns (c, phi)."""
    y = x[1:]
    X = np.column_stack([np.ones(len(y)), x[:-1]])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(beta[0]), float(beta[1])


def trailing_mean_forecast(hist: np.ndarray, window: int, h: int) -> np.ndarray:
    """Naive no-memory benchmark: forecast = trailing-`window`-day mean of
    REAL history, held CONSTANT across the forecast horizon (no assumed
    decay/persistence at all -- the honest zero-model comparator)."""
    val = float(np.mean(hist[-window:]))
    return np.full(h, val)


def diebold_mariano(loss_a: np.ndarray, loss_b: np.ndarray, nw_lag: int) -> tuple[float, float]:
    """Diebold-Mariano test statistic for H0: E[loss_a - loss_b] = 0, using
    a Newey-West (Bartlett-kernel) HAC long-run variance of the loss
    differential with `nw_lag` lags (standard DM convention: nw_lag=h-1 for
    an h-step-ahead forecast, since h-step errors are MA(h-1) under correct
    specification). Returns (DM_stat, two_sided_p). DM<0 favors model A
    (lower loss)."""
    d = loss_a - loss_b
    n = len(d)
    dbar = float(np.mean(d))
    dc = d - dbar
    gamma0 = float(np.dot(dc, dc)) / n
    lrv = gamma0
    for lag in range(1, nw_lag + 1):
        if lag >= n:
            break
        w = 1.0 - lag / (nw_lag + 1)   # Bartlett kernel
        cov = float(np.dot(dc[:-lag], dc[lag:])) / n
        lrv += 2 * w * cov
    lrv = max(lrv, 1e-12)
    se = np.sqrt(lrv / n)
    dm = dbar / se
    from scipy.stats import norm
    p = 2 * (1 - norm.cdf(abs(dm)))
    return float(dm), float(p)


def main():
    df = pd.read_csv(CSV)
    log_on = np.log(df["on_range"].to_numpy())
    log_rth = np.log(df["rth_range"].to_numpy())
    n = len(log_on)
    n_train = int(n * TRAIN_FRAC)
    n_test = n - n_train
    h_max = max(HORIZONS)
    n_origins = n_test - h_max   # last scorable origin must leave room for the longest horizon
    print(f"n={n} n_train={n_train} n_test={n_test} h_max={h_max} n_origins={n_origins}")
    assert n_origins > 50, "test window too short for the longest horizon"

    channels = dict(on_range=log_on, rth_range=log_rth)

    # ---------------- Fit all models on TRAIN ONLY ----------------
    # Codex review (PR #225, first pass) finding #2: `hash(name)` is salted
    # per Python process by default (PYTHONHASHSEED), making the seed --
    # and therefore the fitted (phi,d) and the whole downstream forecast
    # comparison -- NON-deterministic across runs/environments (confirmed
    # materially outcome-relevant). FIXED: fixed integer seeds per channel,
    # matching `_fit_real_params.py`'s own convention (101/102).
    #
    # Codex review (PR #225, first AND second pass -- a two-part defect):
    # first pass found the fit TARGET was Pearson-ACF while the shared
    # `estimate_phi_d_simulated` helper always scores its simulated draws
    # via rank-ACF -- a target/metric mismatch (quantified: 0.030/0.045
    # max diff). Fixing that alone (ranking the train-only target) created
    # a SECOND inconsistency the second review pass caught: this file's own
    # forecast step (`forecast_arinf_path`) applies the fitted filter
    # directly to RAW log-range values and scores raw-scale MSE, but a
    # (phi,d) calibrated to rank-ACF does not, in general, describe the
    # RAW series' own linear (Pearson) dynamics -- a monotonic transform
    # preserves rank correlation, not Pearson autocovariance. FIXED
    # properly this time by decoupling from the shared rank-based helper
    # entirely: `estimate_phi_d_simulated_pearson` (this file, above) fits
    # (phi,d) via an internal PEARSON-ACF simulated comparison, matched to
    # a Pearson-ACF target computed on RAW (unranked) train data -- fit,
    # forecast filter, and MSE scoring are now all consistently Pearson/
    # raw-scale throughout this file.
    fits = {}
    channel_seeds = dict(on_range=101, rth_range=102)
    for name, x in channels.items():
        train = x[:n_train]
        lags = min(30, n_train // 3)
        real_acf = acf(train - train.mean(), lags)
        phi, d, info = estimate_phi_d_simulated_pearson(
            real_acf, n_train, J=800, burn=800, n_reps=4,
            phi_grid=np.linspace(-0.6, 0.9, 21), d_grid=np.linspace(0.01, 0.499, 25),
            seed=channel_seeds[name],
        )
        c1, phi1_ar = fit_ar1(train)
        fits[name] = dict(arfima=dict(phi=phi, d=d, sse=info["best_sse"]), ar1=dict(c=c1, phi=phi1_ar))
        print(f"[{name}] ARFIMA(1,d,0) fit on TRAIN: phi={phi:.4f} d={d:.4f} sse={info['best_sse']:.5f}")
        print(f"[{name}] AR(1) fit on TRAIN: c={c1:.4f} phi={phi1_ar:.4f}")

    # VAR(20) is fit on RAW (non-demeaned) log-range pairs -- fit_var's own
    # design matrix includes an intercept column, so it estimates the mean
    # internally; no separate demeaning step is needed or used for VAR.
    Z_train_raw = np.column_stack([log_on[:n_train], log_rth[:n_train]])
    c_var, A_var, resid_var = fit_var(Z_train_raw, VAR_ORDER)
    resid_acf_max = max(np.max(np.abs(acf(resid_var[:, 0], 5))), np.max(np.abs(acf(resid_var[:, 1], 5))))
    print(f"VAR({VAR_ORDER}) fit on TRAIN (raw log-range): resid max|ACF| lag1-5 = {resid_acf_max:.4f} "
          f"(whitening check, informational)")

    # ARFIMA's AR(inf) recursion (pi(L)X_t = e_t, no intercept term) assumes
    # a ZERO-MEAN process -- this is the ONLY model that needs demeaning;
    # AR(1) and VAR(20) both carry their own fitted intercept and forecast
    # directly in raw log-range space, and naive is a raw trailing mean.
    # The mean is added back before scoring so all four models' forecast
    # errors are compared on the SAME (raw log-range) scale.
    mean_on, mean_rth = log_on[:n_train].mean(), log_rth[:n_train].mean()
    pi_on = ar_inf_pi_weights(fits["on_range"]["arfima"]["phi"], fits["on_range"]["arfima"]["d"], J_TRUNC)
    pi_rth = ar_inf_pi_weights(fits["rth_range"]["arfima"]["phi"], fits["rth_range"]["arfima"]["d"], J_TRUNC)

    # ---------------- Roll forward through the TEST window ----------------
    # errors[channel][model][h] -> list of squared errors across origins, ALL
    # computed in raw log-range units (verified consistent above).
    models = ["arfima", "ar1", f"var{VAR_ORDER}", "naive"]
    sq_err = {ch: {m: {h: [] for h in HORIZONS} for m in models} for ch in channels}

    full_Z_raw = np.column_stack([log_on, log_rth])

    for origin in range(n_train, n_train + n_origins):
        # real history available at this origin (index 0..origin-1 inclusive, i.e. up to time origin-1 = "t")
        hist_on_raw = log_on[:origin]
        hist_rth_raw = log_rth[:origin]
        hist_Z_raw = full_Z_raw[:origin]

        fc_arfima_on = forecast_arinf_path(pi_on, hist_on_raw - mean_on, h_max) + mean_on
        fc_arfima_rth = forecast_arinf_path(pi_rth, hist_rth_raw - mean_rth, h_max) + mean_rth
        fc_ar1_on = forecast_linear_path(fits["on_range"]["ar1"]["c"], [fits["on_range"]["ar1"]["phi"]],
                                          hist_on_raw, h_max, univariate=True)
        fc_ar1_rth = forecast_linear_path(fits["rth_range"]["ar1"]["c"], [fits["rth_range"]["ar1"]["phi"]],
                                           hist_rth_raw, h_max, univariate=True)
        fc_var = forecast_linear_path(c_var, A_var, hist_Z_raw, h_max, univariate=False)  # (h_max, 2), raw
        fc_naive_on = trailing_mean_forecast(hist_on_raw, WINDOW_NAIVE, h_max)
        fc_naive_rth = trailing_mean_forecast(hist_rth_raw, WINDOW_NAIVE, h_max)

        for h in HORIZONS:
            target_idx = origin + h - 1   # 0-indexed absolute position of the h-step-ahead target
            actual_on = log_on[target_idx]
            actual_rth = log_rth[target_idx]

            sq_err["on_range"]["arfima"][h].append((actual_on - fc_arfima_on[h - 1]) ** 2)
            sq_err["rth_range"]["arfima"][h].append((actual_rth - fc_arfima_rth[h - 1]) ** 2)
            sq_err["on_range"]["ar1"][h].append((actual_on - fc_ar1_on[h - 1]) ** 2)
            sq_err["rth_range"]["ar1"][h].append((actual_rth - fc_ar1_rth[h - 1]) ** 2)
            sq_err["on_range"][f"var{VAR_ORDER}"][h].append((actual_on - fc_var[h - 1, 0]) ** 2)
            sq_err["rth_range"][f"var{VAR_ORDER}"][h].append((actual_rth - fc_var[h - 1, 1]) ** 2)
            sq_err["on_range"]["naive"][h].append((actual_on - fc_naive_on[h - 1]) ** 2)
            sq_err["rth_range"]["naive"][h].append((actual_rth - fc_naive_rth[h - 1]) ** 2)

    # ---------------- Aggregate: MSE, relative-R^2 vs naive, DM tests ----------------
    results = {}
    for ch in channels:
        results[ch] = {}
        naive_losses = {h: np.array(sq_err[ch]["naive"][h]) for h in HORIZONS}
        for m in models:
            results[ch][m] = {}
            for h in HORIZONS:
                losses = np.array(sq_err[ch][m][h])
                mse = float(losses.mean())
                mse_naive = float(naive_losses[h].mean())
                r2_vs_naive = 1.0 - mse / mse_naive if mse_naive > 0 else float("nan")
                entry = dict(mse=mse, r2_vs_naive=r2_vs_naive, n_origins=len(losses))
                if m != "naive":
                    dm_naive, p_naive = diebold_mariano(losses, naive_losses[h], NW_LAG(h))
                    entry["dm_vs_naive"] = dm_naive
                    entry["p_vs_naive"] = p_naive
                results[ch][m][h] = entry

        # ARFIMA vs each competitor, per horizon
        results[ch]["arfima_vs_competitors"] = {}
        for h in HORIZONS:
            arfima_losses = np.array(sq_err[ch]["arfima"][h])
            row = {}
            for comp in ("ar1", f"var{VAR_ORDER}"):
                comp_losses = np.array(sq_err[ch][comp][h])
                dm, p = diebold_mariano(arfima_losses, comp_losses, NW_LAG(h))
                row[comp] = dict(dm=dm, p_two_sided=p, p_one_sided_arfima_better=(p / 2 if dm < 0 else 1 - p / 2))
            results[ch]["arfima_vs_competitors"][h] = row

    # ---------------- Print summary table ----------------
    print("\n" + "=" * 100)
    print(f"{'channel':<10}{'h':>5}{'model':>10}{'MSE':>12}{'R2_vs_naive':>14}{'DM_vs_ar1':>12}{'p1s':>8}{'DM_vs_var':>12}{'p1s':>8}")
    for ch in channels:
        for h in HORIZONS:
            for m in ("arfima", "ar1", f"var{VAR_ORDER}", "naive"):
                r = results[ch][m][h]
                if m == "arfima":
                    row_dm = results[ch]["arfima_vs_competitors"][h]
                    dm_ar1, p_ar1 = row_dm["ar1"]["dm"], row_dm["ar1"]["p_one_sided_arfima_better"]
                    dm_var, p_var = row_dm[f"var{VAR_ORDER}"]["dm"], row_dm[f"var{VAR_ORDER}"]["p_one_sided_arfima_better"]
                    print(f"{ch:<10}{h:>5}{m:>10}{r['mse']:>12.5f}{r['r2_vs_naive']:>14.4f}"
                          f"{dm_ar1:>12.3f}{p_ar1:>8.3f}{dm_var:>12.3f}{p_var:>8.3f}")
                else:
                    print(f"{ch:<10}{h:>5}{m:>10}{r['mse']:>12.5f}{r['r2_vs_naive']:>14.4f}")

    # ---------------- Evaluate the pre-committed pass criterion ----------------
    print("\n" + "=" * 100)
    print("PRE-COMMITTED MODEL-ADEQUACY CRITERION EVALUATION (h in {20,40}, both channels)")
    clears = {}
    for ch in channels:
        clears[ch] = {}
        for h in (20, 40):
            r2 = results[ch]["arfima"][h]["r2_vs_naive"]
            row_dm = results[ch]["arfima_vs_competitors"][h]
            p_ar1 = row_dm["ar1"]["p_one_sided_arfima_better"]
            dm_ar1 = row_dm["ar1"]["dm"]
            p_var = row_dm[f"var{VAR_ORDER}"]["p_one_sided_arfima_better"]
            dm_var = row_dm[f"var{VAR_ORDER}"]["dm"]
            beats_ar1 = bool(dm_ar1 < 0 and p_ar1 < 0.10)
            beats_var = bool(dm_var < 0 and p_var < 0.10)
            cond_a = bool(r2 > 0.03)
            cond_b = bool(beats_ar1 and beats_var)
            clears[ch][h] = dict(r2_vs_naive=r2, cond_a_r2_gt_0p03=cond_a,
                                  beats_ar1=beats_ar1, p_vs_ar1=p_ar1,
                                  beats_var=beats_var, p_vs_var=p_var,
                                  cond_b_beats_both=cond_b, clears=cond_a and cond_b)
            print(f"  [{ch}] h={h}: R2_vs_naive={r2:.4f} (need >0.03: {cond_a}) | "
                  f"beats AR(1) p={p_ar1:.3f} ({beats_ar1}) | beats VAR20 p={p_var:.3f} ({beats_var}) "
                  f"-> CLEARS={cond_a and cond_b}")

    any_horizon_both_channels = any(
        clears["on_range"][h]["clears"] and clears["rth_range"][h]["clears"] for h in (20, 40)
    )
    verdict = "MODEL ADEQUACY CLEARS (remedy 1: OOS forecast evaluation)" if any_horizon_both_channels else \
        "MODEL ADEQUACY DOES NOT CLEAR via remedy 1 (OOS forecast evaluation) -- proceed to remedy 2 or disclose"
    print(f"\nOVERALL VERDICT: {verdict}")

    out = dict(
        n=n, n_train=n_train, n_test=n_test, n_origins=n_origins, horizons=HORIZONS,
        train_fits={ch: fits[ch] for ch in channels},
        var_fit=dict(order=VAR_ORDER, resid_whitening_max_abs_acf=resid_acf_max),
        results=results, criterion_evaluation=clears,
        overall_clears=any_horizon_both_channels, verdict=verdict,
    )
    (HERE / "oos_forecast_evaluation_results.json").write_text(json.dumps(out, indent=2, default=str))
    print("\nWrote oos_forecast_evaluation_results.json")


if __name__ == "__main__":
    main()
