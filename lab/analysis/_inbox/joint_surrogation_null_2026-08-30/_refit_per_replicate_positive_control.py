"""Refit-per-replicate positive control (Codex review, PR #219, comment on
ensemble_gate_and_positive_control.py:268).

The original positive control (`ensemble_gate_and_positive_control.py`)
passed the SAME cached real-panel (phi,d,rho_innov) into every synthetic
replicate as ground truth AND as the surrogate-generation parameters --
i.e. it validated the surrogate/statistic/rejection-rate MACHINERY under
"dynamics known exactly," not the full procedure that will actually run on
the real panel, which must ESTIMATE (phi,d) from the data first. Codex's
point: finite-sample fitting error could inflate the false-positive rate
(if estimation noise makes the fitted null too narrow/wide) or make the
alternative's power look artificially high or low (if a boosted series no
longer matches the fitted parameters as well as it matches the true ones).

This script tests that directly rather than just re-disclosing it: for
each replicate, (phi,d) is RE-ESTIMATED from that replicate's OWN
synthetic data (not read from the cache) via the same class of
simulated-method-of-moments calibration `longmemory_copula.py` already
implements, then surrogates are drawn using the RE-ESTIMATED parameters.

COMPUTE-BUDGET SIMPLIFICATION (disclosed, not hidden): the production
calibration grid (phi_grid 21-31 pts x d_grid 25-50 pts x n_reps_calib 5-6,
J/burn=1200-2000) is far too expensive to re-run inside every one of even
a handful of positive-control replicates. This script uses a MUCH coarser
grid (phi_grid 7pts x d_grid 8pts x n_reps_calib=2, J/burn=300) and fewer
replicates (N_REPS=8 per scenario, vs the original 20) -- explicitly a
smaller, faster, noisier stand-in for the real calibration, adequate to
answer the QUALITATIVE question (does refitting change size/power
materially) but not a substitute for re-validating the production-grade
calibration's own robustness at full resolution.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from longmemory_copula import (  # noqa: E402
    acf, rankdata, estimate_phi_d_simulated, ar1_fracdiff_weights,
    _solve_rho_innov, _pair_innovation_link,
)
from positive_control import rolling_pct_strict_prior  # noqa: E402

N_DAYS = 1487
N_REPS = 8            # much smaller than the original 20 -- compute-budget limited
M_SURR = 60           # surrogates per replicate (vs original 100)
WINDOW, Q_BIAS, Q_REF = 60, 0.80, 0.50
ALPHA = 0.05

# Coarse calibration grid -- a fast stand-in for the production grid, not a
# replacement for it (see module docstring).
COARSE_J, COARSE_BURN, COARSE_NREPS = 300, 300, 2
COARSE_PHI_GRID = np.linspace(-0.5, 0.8, 7)
COARSE_D_GRID = np.linspace(0.05, 0.48, 8)


def score_min_stratified_lift(overnight, rth):
    n = len(overnight)
    bias = (overnight >= rolling_pct_strict_prior(overnight, WINDOW, Q_BIAS)).astype(float)
    bias[np.isnan(rolling_pct_strict_prior(overnight, WINDOW, Q_BIAS))] = np.nan
    bias_prime = (rth >= rolling_pct_strict_prior(rth, WINDOW, Q_BIAS)).astype(float)
    bias_prime[np.isnan(rolling_pct_strict_prior(rth, WINDOW, Q_BIAS))] = np.nan
    bias_prime_shifted = np.full(n, np.nan)
    bias_prime_shifted[1:] = bias_prime[:-1]
    ref = rolling_pct_strict_prior(rth, WINDOW, Q_REF)
    y = (rth > ref).astype(float)
    y[np.isnan(ref)] = np.nan
    scored = (~np.isnan(bias)) & (~np.isnan(bias_prime_shifted)) & (~np.isnan(y))
    b = bias[scored].astype(int)
    bp = bias_prime_shifted[scored].astype(int)
    yy = y[scored].astype(int)
    vals = []
    for s in (0, 1):
        m = bp == s
        hi_mask, lo_mask = m & (b == 1), m & (b == 0)
        if hi_mask.any() and lo_mask.any():
            vals.append(float(yy[hi_mask].mean() - yy[lo_mask].mean()))
    return (min(vals) if vals else float("nan")), int(scored.sum())


def gen_synthetic(n, phi1, d1, phi2, d2, rho_innov, seed, boost=0.0):
    """Generate one synthetic (overnight, rth) pair from a known ARFIMA(1,d,0)
    + correlated-innovation-link model, optionally with a genuine incremental
    transmission effect (boost>0) on trailing-P80-overnight-flagged days."""
    rng = np.random.default_rng(seed)
    burn = 300
    psi1 = ar1_fracdiff_weights(phi1, d1, burn)
    psi2 = ar1_fracdiff_weights(phi2, d2, burn)
    e1 = rng.standard_normal(n + burn)
    e_common = rng.standard_normal(n + burn)
    e2 = rho_innov * e1 + np.sqrt(max(0.0, 1 - rho_innov ** 2)) * e_common
    from longmemory_copula import _causal_filter
    z1 = _causal_filter(e1, psi1)[burn: burn + n]
    z2 = _causal_filter(e2, psi2)[burn: burn + n]
    x1 = np.exp(z1 * 0.3)
    x2 = np.exp(z2 * 0.3)
    if boost > 0:
        thresh = rolling_pct_strict_prior(x1, WINDOW, Q_BIAS)
        flagged = np.zeros(n, dtype=bool)
        flagged[WINDOW:] = x1[WINDOW:] >= thresh[WINDOW:]
        x2 = x2.copy()
        x2[flagged] *= (1.0 + boost)
    return x1, x2


def refit_and_score(x1, x2, seed_base, code):
    """Re-estimate (phi,d,rho) from (x1,x2) via a COARSE SMM grid, then
    generate M_SURR surrogates and return p_upper for the observed stat."""
    n = len(x1)
    lags = min(30, n // 3)
    r1, r2 = rankdata(x1), rankdata(x2)
    real1_acf, real2_acf = acf(r1, lags), acf(r2, lags)
    real_crosscorr0 = float(np.corrcoef(r1, r2)[0, 1])
    target_pearson = 2 * np.sin(np.pi * real_crosscorr0 / 6)

    phi1, d1, _ = estimate_phi_d_simulated(real1_acf, n, COARSE_J, COARSE_BURN,
                                            n_reps=COARSE_NREPS, seed=seed_base + 1,
                                            phi_grid=COARSE_PHI_GRID, d_grid=COARSE_D_GRID)
    phi2, d2, _ = estimate_phi_d_simulated(real2_acf, n, COARSE_J, COARSE_BURN,
                                            n_reps=COARSE_NREPS, seed=seed_base + 2,
                                            phi_grid=COARSE_PHI_GRID, d_grid=COARSE_D_GRID)
    psi1 = ar1_fracdiff_weights(phi1, d1, COARSE_J)
    psi2 = ar1_fracdiff_weights(phi2, d2, COARSE_J)
    rho_innov, _ = _solve_rho_innov(psi1, psi2, target_pearson)
    rho_innov = float(np.clip(rho_innov, -0.999, 0.999))

    obs, n_scored = score_min_stratified_lift(x1, x2)
    null_lifts = []
    for i in range(M_SURR):
        rng = np.random.default_rng([seed_base, code, 900, i])
        x1_s, x2_s = _pair_innovation_link(x1, x2, psi1, psi2, COARSE_J, COARSE_BURN, rng, rho_innov)
        lift_s, _ = score_min_stratified_lift(x1_s, x2_s)
        if np.isfinite(lift_s):
            null_lifts.append(lift_s)
    null_lifts = np.asarray(null_lifts)
    p_upper = (1 + int((null_lifts >= obs).sum())) / (len(null_lifts) + 1) if len(null_lifts) else float("nan")
    return obs, p_upper, dict(phi1=phi1, d1=d1, phi2=phi2, d2=d2, rho_innov=rho_innov)


def run_scenario(name, boost, seed_base, true_params):
    rejects, p_uppers = 0, []
    for rep in range(N_REPS):
        t0 = time.time()
        x1, x2 = gen_synthetic(N_DAYS, true_params["phi1"], true_params["d1"],
                                true_params["phi2"], true_params["d2"],
                                true_params["rho_innov"], seed=[seed_base, rep], boost=boost)
        obs, p_upper, fit = refit_and_score(x1, x2, seed_base=seed_base + 5000, code=rep)
        p_uppers.append(p_upper)
        rejects += int(p_upper <= ALPHA)
        print(f"  [{name}] rep {rep}: obs={obs:+.4f} p_upper={p_upper:.4f} "
              f"refit(phi1={fit['phi1']:.2f},d1={fit['d1']:.2f},phi2={fit['phi2']:.2f},"
              f"d2={fit['d2']:.2f},rho={fit['rho_innov']:.2f})  [{time.time()-t0:.1f}s]")
    rate = rejects / len(p_uppers)
    print(f"[{name}] reject rate @alpha={ALPHA}: {rejects}/{len(p_uppers)} = {rate:.3f}\n")
    return rate, p_uppers


def main():
    import json
    cache = json.loads((HERE / "_real_fit_cache.json").read_text())
    true_params = dict(phi1=cache["phi1"], d1=cache["d1"], phi2=cache["phi2"], d2=cache["d2"],
                        rho_innov=cache["rho_innov_clipped"])
    print(f"Ground-truth params (from real-panel cache): {true_params}\n")

    print("=== NULL scenario, REFIT PER REPLICATE (not fixed cached params) ===")
    null_rate, null_ps = run_scenario("NULL", boost=0.0, seed_base=30001, true_params=true_params)

    print("=== ALTERNATIVE scenario (boost=0.4), REFIT PER REPLICATE ===")
    alt_rate, alt_ps = run_scenario("ALTERNATIVE", boost=0.4, seed_base=30002, true_params=true_params)

    print("=== COMPARISON ===")
    print(f"Fixed-params original (20 reps):    null=0.050  alt=0.500")
    print(f"Refit-per-replicate (this, {N_REPS} reps): null={null_rate:.3f}  alt={alt_rate:.3f}")
    print("VERDICT: refitting materially changes size/power" if
          (abs(null_rate - 0.05) > 0.15 or abs(alt_rate - 0.50) > 0.25) else
          "VERDICT: refitting does not materially change size/power at this (coarse, small-N) resolution")

    out = dict(true_params=true_params, n_reps=N_REPS, m_surr=M_SURR,
               coarse_grid=dict(J=COARSE_J, burn=COARSE_BURN, n_reps_calib=COARSE_NREPS,
                                 phi_grid_n=len(COARSE_PHI_GRID), d_grid_n=len(COARSE_D_GRID)),
               null_rate=null_rate, null_p_uppers=null_ps,
               alt_rate=alt_rate, alt_p_uppers=alt_ps)
    (HERE / "_refit_per_replicate_results.json").write_text(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
