"""One-time fit of (phi,d) for both real channels via the simulated/SMM
calibration already implemented in longmemory_copula.py, cached to JSON so
downstream ensemble-diagnostic / positive-control scripts don't re-pay the
grid-search cost repeatedly."""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from longmemory_copula import (  # noqa: E402
    acf, rankdata, estimate_phi_d_simulated, ar1_fracdiff_weights, _solve_rho_innov,
)

CSV = HERE.parent / "mnq_dailygeom_notice_2026-08-29" / "candidate24_joint_frame.csv"

def main():
    df = pd.read_csv(CSV)
    x1 = df["on_range"].to_numpy()
    x2 = df["rth_range"].to_numpy()
    n = len(x1)
    lags = min(30, n // 3)
    r1, r2 = rankdata(x1), rankdata(x2)
    real1_spear = acf(r1, lags)
    real2_spear = acf(r2, lags)
    real_crosscorr0 = float(np.corrcoef(r1, r2)[0, 1])
    target_pearson = 2 * np.sin(np.pi * real_crosscorr0 / 6)

    J, burn, n_reps = 1200, 1200, 5
    t0 = time.time()
    phi1, d1, info1 = estimate_phi_d_simulated(real1_spear, n, J, burn, n_reps=n_reps, seed=101,
                                                phi_grid=np.linspace(-0.6, 0.9, 21),
                                                d_grid=np.linspace(0.01, 0.499, 25))
    t1 = time.time()
    print(f"channel1 fit: phi={phi1:.4f} d={d1:.4f} sse={info1['best_sse']:.5f} ({t1-t0:.1f}s)")
    phi2, d2, info2 = estimate_phi_d_simulated(real2_spear, n, J, burn, n_reps=n_reps, seed=102,
                                                phi_grid=np.linspace(-0.6, 0.9, 21),
                                                d_grid=np.linspace(0.01, 0.499, 25))
    t2 = time.time()
    print(f"channel2 fit: phi={phi2:.4f} d={d2:.4f} sse={info2['best_sse']:.5f} ({t2-t1:.1f}s)")

    psi1 = ar1_fracdiff_weights(phi1, d1, J)
    psi2 = ar1_fracdiff_weights(phi2, d2, J)
    rho_innov, achievable = _solve_rho_innov(psi1, psi2, target_pearson)
    rho_innov_clipped = float(np.clip(rho_innov, -0.999, 0.999))

    out = dict(n=n, lags=lags, J=J, burn=burn, n_reps=n_reps,
               phi1=phi1, d1=d1, phi2=phi2, d2=d2,
               real_crosscorr0=real_crosscorr0, target_pearson=target_pearson,
               rho_innov=float(rho_innov), rho_innov_clipped=rho_innov_clipped,
               achievable_ratio=float(achievable))
    (HERE / "_real_fit_cache.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
