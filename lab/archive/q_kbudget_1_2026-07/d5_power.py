"""D5 (DJ30/NAS gamma-positioning, MYM/MNQ expression) Clause-K + Clause-N re-screen.

Frozen formulas (pre-reg Sec B, freeze b304f2c):
  Clause K: floor(K_eff) = min annualized Sharpe clearing DSR >= 0.95 at (K, V=1/n)
            -- production lab/research_utils/deflated_sharpe.py, most-permissive
            across trade frequencies f in {0.5,1,2,4}/day, 6.5y, Gaussian moments.
            PASS iff floor(K_eff) <= Cap (1.0).
  Clause N: power = Phi(sqrt(N)*|delta|/sigma - z_alpha), z_alpha=1.96, N = full
            declared OOS event count, delta/sigma = cohort-cited central effect.
            "Effect priors must be cohort-cited (in-house measured value where one
            exists; else literature median with citation)."

D5 was UNSCREENABLE on Clause N (no vendor dataset, no cohort delta) per the ratified
Phase-1 inventory. This re-screen supplies a literature-cited delta for ONE reading of
the axis's confirm-construct (the intraday-momentum footprint, Baltussen/Da/Lammers/
Martens 2021 JFE) -- see d5_clause_n_rescreen.md for why this construct is recommended
over the alternative (gamma-SIGN mechanism, which has no NDX/Dow-specific delta and
stays UNSCREENABLE).

Zero data pulls, zero K consumed.

Run: python lab/analysis/q_kbudget_1_2026-07/d5_power.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # lab/
from research_utils.deflated_sharpe import deflated_sharpe, expected_max_sharpe

Z_ALPHA = 1.96
CAP = 1.0
DSR_MIN = 0.95
YEARS = 6.5
FREQS = (0.5, 1.0, 2.0, 4.0)


def phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def floor_at_k(k: int, years: float = YEARS, freqs=FREQS, t: float = DSR_MIN) -> float:
    """Reproduces the production Clause-K floor method exactly (pre-reg Sec F hook #3)."""
    best = None
    for f in freqs:
        n = int(round(252 * f * years))
        sr0 = expected_max_sharpe(k, 1.0 / n)
        s = 0.01
        while s < 6.0:
            if deflated_sharpe(s / math.sqrt(252 * f), n, 0.0, 3.0, sr0) >= t:
                break
            s += 0.005
        best = s if best is None else min(best, s)
    return round(best, 3)


def power(n: int, delta_over_sigma: float, z_alpha: float = Z_ALPHA) -> float:
    return phi(math.sqrt(n) * delta_over_sigma - z_alpha)


def main() -> None:
    print("=== Clause K (K_eff = K_intrinsic + K_banked; family MYM/MNQ banks 0) ===\n")
    for k in (1, 2, 3, 4):
        f = floor_at_k(k)
        verdict = "PASS" if f <= CAP else "FAIL"
        print(f"  K_eff={k}: floor={f}  ({verdict}, Cap={CAP})")

    print("\n=== Clause N (intraday-momentum footprint construct, Baltussen et al. 2021 JFE) ===\n")
    print("  Per-index effect (NQ futures): beta_ROD=6.36, t=7.97, OOS-R^2=3.76%")
    r2 = 0.0376
    rho = math.sqrt(r2)
    print(f"  delta/sigma from OOS-R^2: sqrt({r2}) = {rho:.4f}  (upper-bound reading)")
    for n_pub in (2500, 5000):
        d = 7.97 / math.sqrt(n_pub)
        print(f"  delta/sigma t-scaled @ N_pub={n_pub}: {d:.4f}")

    print("\n  Power grid: Phi(sqrt(N)*delta/sigma - 1.96)\n")
    ns = [250, 500, 1000, 1500]
    labels = [
        ("0.194 (OOS-R^2, upper)", rho),
        ("0.130 (central, t-scaled)", 0.130),
        ("0.113 (t-scaled @N_pub=5000)", 0.113),
        ("0.090 (haircut)", 0.090),
        ("0.060 (near break-even)", 0.060),
    ]
    header = "  delta/sigma".ljust(30) + "".join(f"N={n:<8}" for n in ns)
    print(header)
    for label, d in labels:
        row = label.ljust(30) + "".join(f"{power(n, d):<10.3f}" for n in ns)
        print(row)

    n_decl = 1000  # declared axis panel, ~10^3 daily events (pre-reg Sec E)
    d_central = 0.113
    p_central = power(n_decl, d_central)
    be = Z_ALPHA / math.sqrt(n_decl)
    print(f"\n  At declared N={n_decl}, central delta/sigma={d_central:.3f}: "
          f"power={p_central:.3f}  ({'PASS' if p_central >= 0.50 else 'FAIL'}, threshold 0.50)")
    print(f"  Break-even delta/sigma at N={n_decl}: {be:.4f}")

    ann_sharpe_upper = rho * math.sqrt(252)
    print(f"\n  Sanity check (NOT a Clause-N input): naive gross annualized Sharpe implied "
          f"by daily IC={rho:.3f} ~= {ann_sharpe_upper:.2f}")
    print("  This is a GROSS, pre-cost upper bound -- Baltussen's own Sharpe 1.73 is gross/")
    print("  multi-asset, and only SPX-futures is shown to survive tick-level costs. Net-of-")
    print("  cost NQ/YM survival is UNDEMONSTRATED. This is the downstream campaign-level")
    print("  question (DSR floor 0.65-0.98 at K_eff 1-3), not part of the Clause-N screen.")


if __name__ == "__main__":
    main()
