"""D7 (JPY month-end, 6J expression) Clause-N power — screening-pass companion.

Frozen Clause-N formula (pre-reg Sec B): power = Phi(sqrt(N)*|delta|/sigma - z_alpha),
z_alpha = 1.96 (two-sided p <= 0.05), N = full declared OOS event count, delta/sigma =
cohort-cited central effect. No JPY-native delta is admissible non-circularly (see
d7_clause_n_screen.md); this reuses the HARV class-analogue (Q-HARV-1 Sec R, 9bddd33)
per Sec B's "nearest analytic analogue... recorded on the axis's screen row" provision.

Zero data pulls, zero K consumed. Pure arithmetic on the same normal-approximation the
pre-reg Sec F hook #3 / Q-GATECART-1 method uses.

Run: python lab/analysis/q_kbudget_1_2026-07/d7_power.py
"""
from __future__ import annotations

import math

Z_ALPHA = 1.96  # two-sided p <= 0.05, campaign default


def phi(x: float) -> float:
    """Standard normal CDF."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def power(n: int, delta: float, sigma: float, z_alpha: float = Z_ALPHA) -> float:
    return phi(math.sqrt(n) * abs(delta) / sigma - z_alpha)


def breakeven_delta_over_sigma(n: int, z_alpha: float = Z_ALPHA) -> float:
    """delta/sigma required for power == 0.50 at N."""
    return z_alpha / math.sqrt(n)


def breakeven_n(delta: float, sigma: float, z_alpha: float = Z_ALPHA) -> float:
    """N required for power == 0.50 at this delta/sigma."""
    return (z_alpha / (abs(delta) / sigma)) ** 2


def main() -> None:
    N = 100  # ~= full declared 6J-era OOS monthly month-end event count (pre-reg-generous)

    # Recommended plug (HARV class-analogue, Q-HARV-1 Sec R, commit 9bddd33)
    delta_harv, sigma_harv = 0.0013, 0.0090  # +13 bp central / ~90 bp per monthly event
    p_harv = power(N, delta_harv, sigma_harv)

    print(f"D7 Clause-N power (N={N} monthly month-end events)\n")
    print("Recommended plug -- HARV class-analogue (Q-HARV-1 Sec R, 9bddd33):")
    print(f"  delta = {delta_harv*1e4:.0f} bp, sigma = {sigma_harv*1e4:.0f} bp, "
          f"delta/sigma = {delta_harv/sigma_harv:.3f}")
    print(f"  power = Phi(sqrt({N})*{delta_harv/sigma_harv:.3f} - {Z_ALPHA}) = {p_harv:.3f}")
    print(f"  verdict: {'PASS' if p_harv >= 0.50 else 'FAIL'} (threshold 0.50)\n")

    be_ds = breakeven_delta_over_sigma(N)
    be_n = breakeven_n(delta_harv, sigma_harv)
    print(f"Break-even at N={N}: delta/sigma >= {be_ds:.3f} needed "
          f"(HARV supplies {delta_harv/sigma_harv:.3f}, {be_ds/(delta_harv/sigma_harv):.2f}x short)")
    print(f"Break-even at this delta/sigma: N >= {be_n:.0f} monthly events needed "
          f"(~{be_n/12:.0f}y; declared panel is ~{N/12:.0f}y)\n")

    print("INVALID sensitivities -- shown only to demonstrate why they are excluded, "
          "never load-bearing:")
    # Circular: JPY P-cohort (n=8) mean/sigma -- forbidden, same data that motivated the close
    delta_pcohort, sigma_pcohort = 1224.59, 1875.0  # USD units, illustrative dispersion
    ds_pcohort = delta_pcohort / sigma_pcohort
    print(f"  P-cohort (FORBIDDEN, circular): delta/sigma~={ds_pcohort:.3f} -> "
          f"power~={power(N, ds_pcohort, 1.0):.3f} (spuriously high)")
    # Category-mismatched: excluded-vs-permitted loss-avoidance contrast
    ds_avoid = 0.49
    print(f"  Loss-avoidance contrast (category-mismatched): delta/sigma~={ds_avoid:.2f} -> "
          f"power~={power(N, ds_avoid, 1.0):.3f} (invalid units splice)")


if __name__ == "__main__":
    main()
