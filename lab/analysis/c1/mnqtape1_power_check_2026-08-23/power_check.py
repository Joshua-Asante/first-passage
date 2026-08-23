#!/usr/bin/env python3
"""MNQTAPE-1 synthetic-signal power check at the REAL N (Stage-G EXPLORATION).

DESIGN (frozen before any result is inspected -- see RESULTS.md §Design):

  Backdrop: the REAL, reconstructed r_pm(s) series (N usable EXPLORATION sessions,
  in their real chronological order) -- see build_usable_sessions.py / r_pm_series.json.
  r_pm is used EXACTLY as observed: real marginal distribution, real (if any)
  autocorrelation, untouched.

  Synthetic predictor construction (NORTA / Gaussian-copula rank coupling):
    1. z_R = normal scores (rankits) of the fixed r_pm vector:
         z_R[i] = Phi^-1( (rank_i - 0.5) / N ),  average-rank tie handling.
       z_R is a FIXED, deterministic transform of the real data -- not random.
    2. For a target "true" Spearman rho_S, convert to the generating Pearson
       parameter via the exact bivariate-normal relation (Pearson 1907 / Greiner):
         rho_S = (6/pi) * arcsin(rho_N / 2)   <=>   rho_N = 2*sin(pi*rho_S/6)
    3. Each synthetic draw: X = rho_N * z_R + sqrt(1-rho_N^2) * Z,  Z ~ iid N(0,1),
       fresh Z per draw. X's OWN marginal is irrelevant (Spearman is rank-invariant
       to strictly monotone transforms) -- only X's rank-coupling to R matters, so no
       further transform of X back to an "LTI_norm-shaped" bounded marginal is done.
    4. Empirical calibration: for each target rho_S, a first batch of draws is used to
       measure the REALIZED mean sample Spearman rho; if it deviates from the target
       by more than 0.005, rho_N is corrected once (local-derivative Newton step) and
       the batch is redrawn. This removes reliance on the asymptotic arcsin formula
       being exact at finite N=126 -- the reported "true rho" for each level is the
       CALIBRATED generating-process target, and the realized mean is reported
       alongside it for transparency.

  Frozen test (IDENTICAL to PREREG S9-S12, re-run per draw):
    - statistic: Spearman rho(X, r_pm)
    - null: permutation of the session-date PAIRING between X and r_pm (each series'
      own within-window order preserved; only the cross-series alignment is shuffled)
    - M = 2,000 permutations PER DRAW (fresh random permutation per draw -- not a
      shared/reused permutation bank -- so every draw's p_emp is an independent,
      from-scratch application of the exact real-world procedure)
    - p_emp = (1 + #{rho_null >= rho_obs}) / (M + 1)   [one-sided, predicted positive]
    - screening gate actually applied in the real Stage-G run: p_emp < 0.20

  Grid of assumed true rho: 0.00 (pure-null calibration/sanity check), 0.05, 0.075
  (~observed), 0.10, 0.15, 0.20, 0.25, 0.30, 0.35.
  Replicates per level: N_REPS (see CLI / constant below).

  Output: for each rho level, empirical power = fraction of replicates with
  p_emp < 0.20, plus a binomial standard error, plus the realized-mean-rho
  calibration diagnostic.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent

M_PERM = 2000                 # frozen, per PREREG S11
BASE_SEED = 20260823           # this power-check's own freeze date, distinct from
                                # the pre-reg's own 20260822 (never reuse a frozen seed
                                # for a different apparatus)
N_REPS = 2500                  # per rho level (within the task's suggested 2000-5000)
GATE_P = 0.20                  # the real Stage-G screening threshold that governed
                                # the actual near-miss decision (PREREG §7 step 2c)
RHO_GRID = [0.00, 0.05, 0.075, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35]


def normal_scores(x: np.ndarray) -> np.ndarray:
    """Rankit transform: Phi^-1((rank-0.5)/N), average-rank tie handling."""
    n = len(x)
    ranks = stats.rankdata(x, method="average")
    u = (ranks - 0.5) / n
    return stats.norm.ppf(u)


def rho_n_from_rho_s(rho_s: float) -> float:
    """Exact bivariate-normal Pearson<->Spearman relation (Pearson/Greiner formula)."""
    rho_s = float(np.clip(rho_s, -0.999, 0.999))
    return float(2.0 * np.sin(np.pi * rho_s / 6.0))


def batch_spearman_vs_fixed(x_batch: np.ndarray, r_rank_centered: np.ndarray,
                             r_denom: float) -> np.ndarray:
    """Vectorized Spearman rho of each row of x_batch against the FIXED r_pm ranks.

    x_batch: (K, N) synthetic draws (raw values, not yet ranked).
    Returns length-K array of Spearman correlations.
    """
    k, n = x_batch.shape
    ranks = np.apply_along_axis(lambda row: stats.rankdata(row, method="average"), 1, x_batch)
    ranks_centered = ranks - ranks.mean(axis=1, keepdims=True)
    x_denom = np.sqrt((ranks_centered ** 2).sum(axis=1))
    num = ranks_centered @ r_rank_centered
    denom = x_denom * r_denom
    return num / denom


def permutation_p_one(x_row: np.ndarray, r_rank_centered: np.ndarray, r_denom: float,
                       rho_obs: float, rng: np.random.Generator, m: int) -> float:
    """One draw's frozen permutation-null p_emp (fresh M permutations of x's ranks)."""
    n = len(x_row)
    x_rank = stats.rankdata(x_row, method="average")
    x_rank_centered = x_rank - x_rank.mean()
    x_denom = np.sqrt((x_rank_centered ** 2).sum())

    # Fresh random permutations of x_rank_centered (argsort-of-random-matrix trick).
    rand_mat = rng.random((m, n))
    perm_idx = np.argsort(rand_mat, axis=1)
    permuted = x_rank_centered[perm_idx]  # (m, n)

    null_num = permuted @ r_rank_centered
    null_rho = null_num / (x_denom * r_denom)

    n_ge = int(np.sum(null_rho >= rho_obs))
    return (1.0 + n_ge) / (m + 1.0)


def run_level(rho_target: float, r_pm: np.ndarray, n_reps: int, m_perm: int,
              seed_seq: np.random.SeedSequence) -> dict:
    n = len(r_pm)
    z_r = normal_scores(r_pm)
    r_rank = stats.rankdata(r_pm, method="average")
    r_rank_centered = r_rank - r_rank.mean()
    r_denom = float(np.sqrt((r_rank_centered ** 2).sum()))

    rho_n = rho_n_from_rho_s(rho_target)

    # --- calibration pass (skip for rho_target == 0, trivially exact) ---
    gen_seed, perm_seed = seed_seq.spawn(2)
    gen_rng = np.random.default_rng(gen_seed)

    def draw_batch(rn: float, k: int, rng: np.random.Generator) -> np.ndarray:
        z = rng.standard_normal((k, n))
        return rn * z_r[None, :] + np.sqrt(max(0.0, 1.0 - rn ** 2)) * z

    if rho_target != 0.0:
        calib_x = draw_batch(rho_n, 2000, gen_rng)
        calib_rho = batch_spearman_vs_fixed(calib_x, r_rank_centered, r_denom)
        realized0 = float(np.mean(calib_rho))
        deviation = rho_target - realized0
        if abs(deviation) > 0.005:
            # local derivative of rho_S = (6/pi) asin(rho_N/2) wrt rho_N
            deriv = (6.0 / np.pi) * 0.5 / np.sqrt(max(1e-9, 1.0 - (rho_n / 2.0) ** 2))
            rho_n_corrected = rho_n + deviation / deriv
            rho_n_corrected = float(np.clip(rho_n_corrected, -0.999, 0.999))
        else:
            rho_n_corrected = rho_n
    else:
        rho_n_corrected = 0.0
        realized0 = 0.0

    # --- main batch (fresh draws, independent of calibration draws) ---
    x_main = draw_batch(rho_n_corrected, n_reps, gen_rng)
    rho_obs_all = batch_spearman_vs_fixed(x_main, r_rank_centered, r_denom)
    realized_mean = float(np.mean(rho_obs_all))
    realized_std = float(np.std(rho_obs_all))

    perm_ss = np.random.SeedSequence(perm_seed.entropy).spawn(n_reps)
    p_emp = np.empty(n_reps)
    for i in range(n_reps):
        rng_i = np.random.default_rng(perm_ss[i])
        p_emp[i] = permutation_p_one(
            x_main[i], r_rank_centered, r_denom, rho_obs_all[i], rng_i, m_perm
        )

    power = float(np.mean(p_emp < GATE_P))
    se = float(np.sqrt(power * (1 - power) / n_reps))

    return {
        "rho_target": rho_target,
        "rho_n_nominal": rho_n,
        "rho_n_used": rho_n_corrected,
        "calibration_realized_rho_pre_correction": realized0,
        "realized_mean_rho": realized_mean,
        "realized_std_rho": realized_std,
        "n_reps": n_reps,
        "m_perm": m_perm,
        "power_p_lt_0_20": power,
        "power_se": se,
        "median_p_emp": float(np.median(p_emp)),
        "p10_p_emp": float(np.percentile(p_emp, 10)),
        "p90_p_emp": float(np.percentile(p_emp, 90)),
    }


def main() -> None:
    series = json.loads((HERE / "r_pm_series.json").read_text(encoding="utf-8"))
    r_pm = np.asarray(series["r_pm"], dtype=float)
    n = len(r_pm)
    print(f"N_usable r_pm sessions loaded: {n}")

    # descriptive stats of the REAL r_pm backdrop (for RESULTS.md)
    print(f"r_pm mean={r_pm.mean():.6f} std={r_pm.std(ddof=1):.6f} "
          f"skew={stats.skew(r_pm):.4f} kurtosis_excess={stats.kurtosis(r_pm):.4f}")
    if n > 1:
        acf1 = np.corrcoef(r_pm[:-1], r_pm[1:])[0, 1]
        print(f"lag-1 autocorrelation of real r_pm sequence: {acf1:.4f}")

    root_ss = np.random.SeedSequence(BASE_SEED)
    level_seeds = root_ss.spawn(len(RHO_GRID))

    results = []
    t0 = time.time()
    for rho_target, seed_seq in zip(RHO_GRID, level_seeds):
        t1 = time.time()
        res = run_level(rho_target, r_pm, N_REPS, M_PERM, seed_seq)
        dt = time.time() - t1
        print(
            f"rho_true={rho_target:.3f}  rho_N_used={res['rho_n_used']:.4f}  "
            f"realized_mean_rho={res['realized_mean_rho']:.4f}  "
            f"power(p<{GATE_P})={res['power_p_lt_0_20']:.4f} "
            f"(se={res['power_se']:.4f})  [{dt:.1f}s]",
            flush=True,
        )
        results.append(res)
    print(f"TOTAL wall time: {time.time()-t0:.1f}s")

    out = {
        "n_usable": n,
        "m_perm": M_PERM,
        "n_reps": N_REPS,
        "gate_p": GATE_P,
        "base_seed": BASE_SEED,
        "r_pm_mean": float(r_pm.mean()),
        "r_pm_std": float(r_pm.std(ddof=1)),
        "r_pm_skew": float(stats.skew(r_pm)),
        "r_pm_kurtosis_excess": float(stats.kurtosis(r_pm)),
        "r_pm_lag1_acf": float(np.corrcoef(r_pm[:-1], r_pm[1:])[0, 1]) if n > 1 else None,
        "levels": results,
    }
    (HERE / "power_check_results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote {HERE / 'power_check_results.json'}")


if __name__ == "__main__":
    main()
