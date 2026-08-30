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

PRE-COMMITTED PASS CRITERION (fixed here, before any number below was
computed):

  MODEL ADEQUACY CLEARS (via this remedy) if, on BOTH channels, ARFIMA(1,d,0)
  achieves the LOWEST BIC among all five candidates (ARFIMA, AR1, AR5, AR10,
  AR20) -- BIC (not AIC) is the pre-registered criterion because BIC's
  stronger complexity penalty (k*log(n) vs AIC's 2k) is the more
  conservative, harder-to-satisfy-by-accident bar, appropriate for a
  genuinely discriminating adequacy check per this round's own stated
  standard. AIC is also reported for disclosure/context but does not gate.

  If ARFIMA does not achieve the lowest BIC on both channels, model adequacy
  is NOT established via this remedy either. Per the ratified bounded round,
  this is remedy #2 of at most 2 -- a fail here triggers the hard stop
  (disclose the Q-RANGEXFER-1 §6 gate-table gap), not a third attempt.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

CSV = HERE.parent / "mnq_dailygeom_notice_2026-08-29" / "candidate24_joint_frame.csv"
TRAIN_FRAC = 0.80


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
    """Concentrated (profiled-sigma^2) Whittle -2*log-likelihood, derived by
    hand (verified against the standard Whittle profiling identity before
    use, see module docstring): given g(w;theta) (unit-variance-normalized
    spectral density), the innovation-variance MLE is
        sigma2_hat = mean(I / g),
    and the concentrated -2*logL (up to an additive constant shared by every
    candidate model, hence irrelevant to AIC/BIC RANKING though included
    here for a complete formula) is
        -2*logL = m*log(sigma2_hat) + sum(log(g)) + m.
    Returns (neg2loglik, sigma2_hat)."""
    m = len(I)
    ratio = I / g
    sigma2_hat = float(np.mean(ratio))
    sigma2_hat = max(sigma2_hat, 1e-12)
    neg2ll = m * np.log(sigma2_hat) + float(np.sum(np.log(g))) + m
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


def main():
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
    clears = {}
    for name in channels:
        row = results[name]
        best_model = min(row.keys(), key=lambda k: row[k]["bic"])
        clears[name] = (best_model == "arfima")
        for m_name, r in sorted(row.items(), key=lambda kv: kv[1]["bic"]):
            flag = " <-- BEST" if m_name == best_model else ""
            print(f"{name:<10}{m_name:>10}{r['k']:>4}{r['neg2loglik']:>12.2f}{r['aic']:>12.2f}{r['bic']:>12.2f}{flag:>12}")
        print(f"  [{name}] BIC-best model: {best_model}  (ARFIMA achieves lowest BIC: {clears[name]})")

    overall_clears = all(clears.values())
    verdict = "MODEL ADEQUACY CLEARS (remedy 2: information-criterion comparison)" if overall_clears else \
        "MODEL ADEQUACY DOES NOT CLEAR via remedy 2 either -- both candidate remedies exhausted"
    print(f"\nOVERALL VERDICT: {verdict}")

    out = dict(n=n, n_train=n_train, ar_orders=AR_ORDERS, results=results,
               clears_per_channel=clears, overall_clears=overall_clears, verdict=verdict)
    (HERE / "information_criterion_comparison_results.json").write_text(json.dumps(out, indent=2, default=str))
    print("\nWrote information_criterion_comparison_results.json")


if __name__ == "__main__":
    main()
