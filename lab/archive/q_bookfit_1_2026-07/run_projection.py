"""Q-BOOKFIT-1 — fork composition-coordinate projection (Phases 2-3).

Pre-reg (FROZEN 2026-07-20, commit 0fc1e05):
  docs/briefs/pre-registration/Q-BOOKFIT-1-verdict-preregistration.md
Parent brief: docs/briefs/Q-BOOKFIT-1-fork-composition-coordinate-triage.md

Book: the frozen 2-leg c1 panel (Striker MYM @0.70% + Striker-NAS MNQ @0.37%),
built by the UNTOUCHED Class-S primitives (build_scaled_panel, sha-pinned CSVs,
1R guards intact), collapsed to the $100K basis exactly as Q-COMPOSE-1 did.

Forks (pre-reg §A, fixed): F-A ZN auction unwind (36/yr episodic, ~13:00 ET);
F-B CL EIA (52/yr episodic, 10:30 ET Wed); F-C carry timing (continuous, H=21d).

Frozen formulas (pre-reg §B): R$ = 0.0037*100_000; N_b = events/yr (episodic)
or 252/H (continuous); sigma_d = R$*sigma_R*sqrt(N_b/252), sigma_R=1.0;
rho = sigma_d/sigma_book_d with a ±10% reconcile gate vs the $273 anchor;
risk-delta = PR({l1,l2,v}) - PR({l1,l2}), v = (sigma_d*sqrt(5))^2, corr=0
(best case, stated as upper bound). PASS = rho<1.0 AND delta>0 (§C).

Exit codes: 0 = completed (any verdict); 3 = reconcile HALT.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[2]
_SCORING = _ROOT / "lab" / "analysis" / "class_s_candidate1_scoring_2026-07-15"
for _p in (_ROOT / "core", _ROOT / "lab", _SCORING):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import run_class_s_c1_scoring as S  # noqa: E402  (frozen panel primitives)
from research_utils.breadth import participation_ratio  # noqa: E402

# ── Pre-reg §B frozen constants ──────────────────────────────────────────────
W_REF = 0.0037                 # ORB-precedent reference weight
BASIS = 100_000.0              # $100K common band (Q-COMPOSE basis)
R_DOLLARS = W_REF * BASIS      # $370 per independent risk block
SIGMA_R = 1.0                  # per-block P&L std in R units (frozen; annex below)
ANCHOR_BOOK_STD = 273.0        # Q-COMPOSE-1 closure anchor (daily $-std, $100K)
RECONCILE_TOL = 0.10           # ±10% HALT gate

FORKS = {
    # name: (N_b per year, session window ET, regime class, episodic?)
    "F-A ZN auction unwind":   dict(n_b=36.0,        session="~13:00 ET post-auction", regime="event-flow reversion", episodic=True,  h_days=None),
    "F-B CL EIA expression":   dict(n_b=52.0,        session="10:30 ET Wed",           regime="event drift/reversion", episodic=True,  h_days=None),
    "F-C carry timing 6J/6E/CL": dict(n_b=252.0/21.0, session="continuous hold",        regime="carry (calm/range-alive)", episodic=False, h_days=21),
}
BOOK_SESSION = "08:00-12:00 EST (NY morning, both legs)"

SIGMA_R_ANNEX = (0.5, 1.0, 1.5)
FC_H_ANNEX = (5, 21, 63)


def main() -> int:
    # ── Book panel via frozen primitives (zero edits) ────────────────────────
    panel_200k, meta, _ = S.build_scaled_panel(
        S.C1_STRATS, {"striker": 0.0070, "striker_nas100": 0.0037},
        expect_1r=S.EXPECTED_1R,
    )
    panel_100k = panel_200k * (BASIS / S.ACCOUNT)

    book_daily = panel_100k.sum(axis=1).to_numpy(dtype=float)
    sigma_book_d = float(np.std(book_daily, ddof=1))

    # Reconcile gate (pre-reg §B.4)
    dev = abs(sigma_book_d - ANCHOR_BOOK_STD) / ANCHOR_BOOK_STD
    print(f"[reconcile] measured book daily $-std = ${sigma_book_d:.2f} "
          f"(anchor ${ANCHOR_BOOK_STD:.0f}, dev {dev:.1%}, tol {RECONCILE_TOL:.0%})")
    if dev > RECONCILE_TOL:
        print("HALT: panel-basis mismatch vs Q-COMPOSE anchor — no verdict.")
        return 3

    # Weekly (Mon-anchored, matching breadth.py convention) covariance eigs
    weekly = panel_100k.resample("W-MON").sum()
    cov2 = np.cov(weekly.to_numpy(dtype=float), rowvar=False)
    eig2 = np.clip(np.linalg.eigvalsh(cov2), 0, None)
    pr_book = participation_ratio(cov2)
    print(f"[book] weekly cov eigenvalues = {eig2.round(0).tolist()}  PR = {pr_book:.4f}")
    print(f"[book] panel span {meta['panel_span']}  n_bdays {meta['n_bdays']}")

    # ── Per-fork projection (pre-reg §B.2-B.5) ───────────────────────────────
    def project(n_b: float, sigma_r: float) -> dict:
        sigma_d = R_DOLLARS * sigma_r * np.sqrt(n_b / 252.0)
        rho = sigma_d / sigma_book_d
        v = (sigma_d * np.sqrt(5.0)) ** 2
        m = np.diag(np.concatenate([eig2, [v]]))
        delta = participation_ratio(m) - pr_book
        return dict(sigma_d=sigma_d, rho=rho, v_weekly=v, n_eff_risk_delta=delta)

    results = {}
    print(f"\n{'fork':<28}{'N_b':>6}{'sig_d':>9}{'rho':>7}{'d_riskNeff':>12}  verdict")
    for name, f in FORKS.items():
        p = project(f["n_b"], SIGMA_R)
        ok = (p["rho"] < 1.0) and (p["n_eff_risk_delta"] > 0.0)
        w_star = W_REF / p["rho"]  # weight at rho == 1.0 (disclosure only)
        results[name] = {
            **f, **{k: float(v) for k, v in p.items()},
            "pass": bool(ok), "w_star_rho1": float(w_star),
            "annex_sigma_r": {str(s): {k: float(v) for k, v in project(f["n_b"], s).items()}
                              for s in SIGMA_R_ANNEX},
        }
        if name.startswith("F-C"):
            results[name]["annex_h"] = {
                str(h): {k: float(v) for k, v in project(252.0 / h, SIGMA_R).items()}
                for h in FC_H_ANNEX}
        print(f"{name:<28}{f['n_b']:>6.1f}{p['sigma_d']:>9.2f}{p['rho']:>7.3f}"
              f"{p['n_eff_risk_delta']:>12.4f}  {'PASS' if ok else 'FAIL'}")

    # ── §D verdict assertion ─────────────────────────────────────────────────
    passes = [n for n, r in results.items() if r["pass"]]
    verdict = "RESOLVED" if passes else "FALSIFIED"   # all scoreable by §A construction
    print(f"\nVERDICT (pre-reg §D): {verdict}"
          + (f" — PASS: {passes}" if passes else " — all three FAIL"))

    out = {
        "prereg_commit": "0fc1e05",
        "book": {"sigma_daily_100k": sigma_book_d, "anchor": ANCHOR_BOOK_STD,
                 "reconcile_dev": dev, "weekly_cov_eigs": eig2.tolist(),
                 "pr_risk_2leg": pr_book, "panel_span": meta["panel_span"],
                 "session": BOOK_SESSION},
        "constants": {"w_ref": W_REF, "basis": BASIS, "r_dollars": R_DOLLARS,
                      "sigma_r": SIGMA_R},
        "forks": results,
        "verdict": verdict,
    }
    (_HERE / "projection_results.json").write_text(json.dumps(out, indent=2))
    print(f"\nwrote {(_HERE / 'projection_results.json').name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
