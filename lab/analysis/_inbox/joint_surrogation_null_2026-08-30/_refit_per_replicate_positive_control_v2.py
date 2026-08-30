"""Properly-powered, finer-grid, larger-N refit-per-replicate positive control
(Round 4, ratified bounded round -- 2026-08-30 operator ratification: "pursue
... a properly-powered, finer-grid, larger-N refit-per-replicate positive
control" as the mandatory size/power re-certification, separate from and in
addition to whichever model-adequacy remedy this round also tries).

Round 3's own `_refit_per_replicate_positive_control.py` found a real, load-
bearing Type-I inflation (5% nominal -> 25% empirical, 2/8 replicates) but
explicitly disclosed it as a "coarse/small-N" check: phi_grid 7pts x d_grid
8pts x n_reps_calib=2, J/burn=300, N_REPS=8 per scenario -- a deliberately
cheap stand-in, not a production-grade re-certification. This script re-runs
the IDENTICAL refit-per-replicate design (same generative model, same
estimator class -- simulated-method-of-moments via
`longmemory_copula.estimate_phi_d_simulated`, same `score_min_stratified_lift`
statistic) at:

  - the FULL PRODUCTION calibration grid: phi_grid 21pts x d_grid 25pts x
    n_reps_calib=5, J/burn=1200 -- IDENTICAL to `_fit_real_params.py`'s own
    real-data fit grid, not a new stand-in invented for this check. This
    directly answers Round 3's own stated caveat ("The coarse grid likely
    overstates the true production-grade inflation... a finer grid should
    estimate (phi,d) more precisely, reducing estimation noise") with the
    ACTUAL production grid, not a moderately-less-coarse one.
  - N_REPS=50 per scenario (vs the original 8) -- at the nominal 5% rate,
    the binomial standard error shrinks from sqrt(.05*.95/8)=0.077 (a single
    extra-or-fewer rejection swings the estimate by 12.5 points) to
    sqrt(.05*.95/50)=0.031, a ~2.5x tightening. This is still a Monte Carlo
    estimate, not exact, and is reported with its own binomial CI below --
    not treated as noise-free.
  - M_SURR=100 surrogates per replicate (vs the original 60), matching
    `ensemble_gate_and_positive_control.py`'s own positive-control M.

Timed empirically before committing to this configuration (not guessed):
one full replicate (both channels' production-grid SMM fits + 100 surrogate
draws + scoring) measured at ~4.3s on this machine, so N_REPS=50 x 2
scenarios is a ~7-minute run -- well within budget, and no longer a
compute-forced simplification the way the original N=8/coarse-grid choice
explicitly was.

Everything else (generative model `gen_synthetic`, the boost=0.4 alternative
effect definition, the statistic under test) is REUSED VERBATIM from
`_refit_per_replicate_positive_control.py` -- this script changes only the
calibration-grid and replicate-count knobs, not the design itself.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(HERE))
from longmemory_copula import (  # noqa: E402
    acf, rankdata, estimate_phi_d_simulated, ar1_fracdiff_weights,
    _solve_rho_innov, _pair_innovation_link,
)
from _refit_per_replicate_positive_control import gen_synthetic, score_min_stratified_lift  # noqa: E402

N_REPS = 50            # vs the original coarse check's 8
M_SURR = 100           # vs the original coarse check's 60
ALPHA = 0.05

# PRODUCTION calibration grid -- IDENTICAL to _fit_real_params.py's own
# real-data fit, not a new intermediate stand-in.
PROD_J, PROD_BURN, PROD_NREPS = 1200, 1200, 5
PROD_PHI_GRID = np.linspace(-0.6, 0.9, 21)
PROD_D_GRID = np.linspace(0.01, 0.499, 25)


def refit_and_score(x1, x2, seed_base, code):
    """Identical structure to the coarse script's own function of the same
    name, with the calibration grid swapped to production scale."""
    n = len(x1)
    lags = min(30, n // 3)
    r1, r2 = rankdata(x1), rankdata(x2)
    real1_acf, real2_acf = acf(r1, lags), acf(r2, lags)
    real_crosscorr0 = float(np.corrcoef(r1, r2)[0, 1])
    target_pearson = 2 * np.sin(np.pi * real_crosscorr0 / 6)

    phi1, d1, _ = estimate_phi_d_simulated(real1_acf, n, PROD_J, PROD_BURN,
                                            n_reps=PROD_NREPS, seed=seed_base + 1,
                                            phi_grid=PROD_PHI_GRID, d_grid=PROD_D_GRID)
    phi2, d2, _ = estimate_phi_d_simulated(real2_acf, n, PROD_J, PROD_BURN,
                                            n_reps=PROD_NREPS, seed=seed_base + 2,
                                            phi_grid=PROD_PHI_GRID, d_grid=PROD_D_GRID)
    psi1 = ar1_fracdiff_weights(phi1, d1, PROD_J)
    psi2 = ar1_fracdiff_weights(phi2, d2, PROD_J)
    rho_innov, _ = _solve_rho_innov(psi1, psi2, target_pearson)
    rho_innov = float(np.clip(rho_innov, -0.999, 0.999))

    obs, n_scored = score_min_stratified_lift(x1, x2)
    null_lifts = []
    for i in range(M_SURR):
        rng = np.random.default_rng([seed_base, code, 900, i])
        x1_s, x2_s = _pair_innovation_link(x1, x2, psi1, psi2, PROD_J, PROD_BURN, rng, rho_innov)
        lift_s, _ = score_min_stratified_lift(x1_s, x2_s)
        if np.isfinite(lift_s):
            null_lifts.append(lift_s)
    null_lifts = np.asarray(null_lifts)
    p_upper = (1 + int((null_lifts >= obs).sum())) / (len(null_lifts) + 1) if len(null_lifts) else float("nan")
    return obs, p_upper, dict(phi1=phi1, d1=d1, phi2=phi2, d2=d2, rho_innov=rho_innov)


def wilson_ci(k, n, z=1.96):
    """Wilson score interval for a binomial proportion -- better-behaved than
    the normal approximation at small n / extreme rates (both apply here)."""
    if n == 0:
        return (float("nan"), float("nan"))
    phat = k / n
    denom = 1 + z ** 2 / n
    center = (phat + z ** 2 / (2 * n)) / denom
    half = (z * np.sqrt(phat * (1 - phat) / n + z ** 2 / (4 * n ** 2))) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def run_scenario(name, boost, seed_base, true_params):
    rejects, p_uppers, fits = 0, [], []
    for rep in range(N_REPS):
        t0 = time.time()
        x1, x2 = gen_synthetic(1487, true_params["phi1"], true_params["d1"],
                                true_params["phi2"], true_params["d2"],
                                true_params["rho_innov"], seed=[seed_base, rep], boost=boost)
        obs, p_upper, fit = refit_and_score(x1, x2, seed_base=seed_base + 5000, code=rep)
        p_uppers.append(p_upper)
        fits.append(fit)
        rejects += int(p_upper <= ALPHA)
        print(f"  [{name}] rep {rep}: obs={obs:+.4f} p_upper={p_upper:.4f} "
              f"refit(phi1={fit['phi1']:.2f},d1={fit['d1']:.2f},phi2={fit['phi2']:.2f},"
              f"d2={fit['d2']:.2f},rho={fit['rho_innov']:.2f})  [{time.time()-t0:.1f}s]")
    rate = rejects / len(p_uppers)
    ci = wilson_ci(rejects, len(p_uppers))
    print(f"[{name}] reject rate @alpha={ALPHA}: {rejects}/{len(p_uppers)} = {rate:.3f} "
          f"(Wilson 95% CI [{ci[0]:.3f},{ci[1]:.3f}])\n")
    return rate, ci, p_uppers, fits


def main():
    cache = json.loads((HERE / "_real_fit_cache.json").read_text())
    true_params = dict(phi1=cache["phi1"], d1=cache["d1"], phi2=cache["phi2"], d2=cache["d2"],
                        rho_innov=cache["rho_innov_clipped"])
    print(f"Ground-truth params (from real-panel cache): {true_params}")
    print(f"Production grid: J={PROD_J} burn={PROD_BURN} n_reps_calib={PROD_NREPS} "
          f"phi_grid={len(PROD_PHI_GRID)}pts d_grid={len(PROD_D_GRID)}pts; "
          f"N_REPS={N_REPS} M_SURR={M_SURR}\n")
    t_start = time.time()

    print("=== NULL scenario, REFIT PER REPLICATE, PRODUCTION GRID ===")
    null_rate, null_ci, null_ps, null_fits = run_scenario("NULL", boost=0.0, seed_base=40001,
                                                            true_params=true_params)

    print("=== ALTERNATIVE scenario (boost=0.4), REFIT PER REPLICATE, PRODUCTION GRID ===")
    alt_rate, alt_ci, alt_ps, alt_fits = run_scenario("ALTERNATIVE", boost=0.4, seed_base=40002,
                                                        true_params=true_params)

    print("=== COMPARISON ===")
    print(f"Fixed-params original (20 reps, known-true params):        null=0.050  alt=0.500")
    print(f"Coarse refit-per-replicate (Round 3, N=8, coarse grid):     null=0.250  alt=0.500")
    print(f"Production refit-per-replicate (this, N={N_REPS}, prod grid): "
          f"null={null_rate:.3f} [{null_ci[0]:.3f},{null_ci[1]:.3f}]  "
          f"alt={alt_rate:.3f} [{alt_ci[0]:.3f},{alt_ci[1]:.3f}]")

    # Pre-committed size/power criterion (stated here, before the numbers
    # above existed in the file that will be read -- this docstring text
    # was written before the first replicate ran):
    #  - size_controlled: the null rate's Wilson lower CI bound does not
    #    exclude a rate compatible with material inflation being ABSENT is
    #    the WRONG framing (a positive control's job is to catch inflation,
    #    not presume it away) -- the actual criterion is the direct one:
    #    is the point estimate close to nominal (<=0.10, double the nominal
    #    5%, a real but not gross departure) AND does its own CI upper bound
    #    stay comfortably under the coarse check's alarming 0.25?
    #  - power_adequate: alt_rate exceeds null_rate by a wide, unambiguous
    #    margin (>=0.25), consistent with every prior round's power reads.
    size_controlled = null_rate <= 0.10 and null_ci[1] <= 0.20
    power_adequate = (alt_rate - null_rate) >= 0.25
    verdict = "SIZE/POWER GATE CLEARS" if (size_controlled and power_adequate) else \
        "SIZE/POWER GATE DOES NOT CLEAR -- inflation confirmed at production grid/N, not a coarse-grid artifact"
    print(f"\nsize_controlled (null_rate<=0.10 AND CI_hi<=0.20): {size_controlled}")
    print(f"power_adequate (alt_rate - null_rate >= 0.25): {power_adequate}")
    print(f"VERDICT: {verdict}")
    print(f"\nTotal wall-clock: {time.time()-t_start:.1f}s")

    out = dict(
        true_params=true_params, n_reps=N_REPS, m_surr=M_SURR,
        production_grid=dict(J=PROD_J, burn=PROD_BURN, n_reps_calib=PROD_NREPS,
                              phi_grid_n=len(PROD_PHI_GRID), d_grid_n=len(PROD_D_GRID)),
        null_rate=null_rate, null_ci_wilson=list(null_ci), null_p_uppers=null_ps,
        null_fits=null_fits,
        alt_rate=alt_rate, alt_ci_wilson=list(alt_ci), alt_p_uppers=alt_ps,
        alt_fits=alt_fits,
        size_controlled=size_controlled, power_adequate=power_adequate, verdict=verdict,
        comparison=dict(fixed_params_original=dict(null=0.05, alt=0.50, n_reps=20),
                        coarse_refit_round3=dict(null=0.25, alt=0.50, n_reps=8)),
    )
    (HERE / "_refit_per_replicate_v2_results.json").write_text(json.dumps(out, indent=2, default=str))
    print("\nWrote _refit_per_replicate_v2_results.json")


if __name__ == "__main__":
    main()
