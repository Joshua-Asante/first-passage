"""Independent adversarial re-run of the positive control in
ensemble_gate_and_positive_control.py, with (a) more replicates for a
tighter estimate of null false-positive rate and alternative power,
(b) a uniformity check on the null p_upper distribution (KS test vs
Uniform(0,1)) to distinguish genuine calibration from a degenerate
never-rejects null, and (c) a second, smaller transmission_boost to see
whether power is a cliff-edge artifact of the specific boost=0.4 tuning.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ensemble_gate_and_positive_control as m
from ensemble_gate_and_positive_control import run_scenario  # noqa

import pandas as pd

CSV = HERE.parent / "mnq_dailygeom_notice_2026-08-29" / "candidate24_joint_frame.csv"
FIT_CACHE = HERE / "_real_fit_cache.json"


def main():
    df = pd.read_csv(CSV)
    x1 = df["on_range"].to_numpy()
    x2 = df["rth_range"].to_numpy()
    fit = json.loads(FIT_CACHE.read_text())
    m.psi1_phi, m.psi1_d = fit["phi1"], fit["d1"]
    m.psi2_phi, m.psi2_d = fit["phi2"], fit["d2"]
    rho_innov = fit["rho_innov_clipped"]
    J, burn = fit["J"], fit["burn"]

    psi1 = m.ar1_fracdiff_weights(m.psi1_phi, m.psi1_d, J)
    psi2 = m.ar1_fracdiff_weights(m.psi2_phi, m.psi2_d, J)

    N_REPS = 80  # 4x the original 20, different seed bases (independent draws)
    M_PC = 100

    print("=== INDEPENDENT RE-RUN: NULL, N_REPS=80, fresh seeds ===")
    null_rate, null_ps, null_obs = run_scenario(
        "NULL", x1, x2, psi1, psi2, rho_innov, transmission_boost=0.0,
        n_reps=N_REPS, M=M_PC, J=J, burn=burn, seed_base=7182390,
    )

    print("=== INDEPENDENT RE-RUN: ALTERNATIVE boost=0.4, N_REPS=80, fresh seeds ===")
    alt_rate_04, alt_ps_04, alt_obs_04 = run_scenario(
        "ALT_boost0.4", x1, x2, psi1, psi2, rho_innov, transmission_boost=0.4,
        n_reps=N_REPS, M=M_PC, J=J, burn=burn, seed_base=7182391,
    )

    print("=== INDEPENDENT RE-RUN: ALTERNATIVE boost=0.2 (smaller/more subtle effect), N_REPS=80 ===")
    alt_rate_02, alt_ps_02, alt_obs_02 = run_scenario(
        "ALT_boost0.2", x1, x2, psi1, psi2, rho_innov, transmission_boost=0.2,
        n_reps=N_REPS, M=M_PC, J=J, burn=burn, seed_base=7182392,
    )

    # Uniformity check on the null p_upper distribution (KS test vs Uniform(0,1))
    null_ps_arr = np.array(null_ps)
    ks_stat, ks_p = stats.kstest(null_ps_arr, "uniform")
    print(f"\nNull p_upper distribution: n={len(null_ps_arr)} mean={null_ps_arr.mean():.4f} "
          f"sd={null_ps_arr.std():.4f} (Uniform(0,1) reference: mean=0.5, sd={1/np.sqrt(12):.4f})")
    print(f"KS test vs Uniform(0,1): stat={ks_stat:.4f} p={ks_p:.4f}")

    # Clopper-Pearson-ish binomial CI for null_rate at N_REPS=80
    from scipy.stats import beta
    k = int(round(null_rate * len(null_ps)))
    n = len(null_ps)
    lo = 0.0 if k == 0 else beta.ppf(0.025, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(0.975, k + 1, n - k)
    print(f"\nNull false-positive rate: {k}/{n} = {null_rate:.3f}  95% CI=[{lo:.3f},{hi:.3f}]")
    print(f"Alt power (boost=0.4): {alt_rate_04:.3f}   Alt power (boost=0.2): {alt_rate_02:.3f}")

    out = dict(
        n_reps=N_REPS, M=M_PC,
        null_rate=null_rate, null_ps=null_ps,
        alt_rate_boost04=alt_rate_04, alt_ps_boost04=alt_ps_04,
        alt_rate_boost02=alt_rate_02, alt_ps_boost02=alt_ps_02,
        null_p_ks_stat=float(ks_stat), null_p_ks_p=float(ks_p),
        null_rate_ci95=[float(lo), float(hi)],
    )
    (HERE / "_adversarial_rerun_results.json").write_text(json.dumps(out, indent=2))
    print("\nWrote _adversarial_rerun_results.json")


if __name__ == "__main__":
    main()
