"""Numbers behind a proposed right-sizing of the Q-VOLREGIME-1 C2/C3 pilot.

No real data, no outcome-bearing statistic -- pure design arithmetic:
  1. exact Clopper-Pearson acceptance bands for Binomial(N_outer, 0.05)
  2. detection power of the C2 calibration check against inflated true rates
  3. resulting core-hour budget under the measured per-replicate timings
"""
from __future__ import annotations

from math import comb

# measured on the operator's machine, l5_timing_dryrun.py
SEC_FULL = 1.002      # baseline refit every replicate
SEC_CACHED = 0.689    # baseline cached (volume-free model is rotation-invariant)


def binom_pmf(k: int, n: int, p: float) -> float:
    return comb(n, k) * p**k * (1 - p) ** (n - k)


def binom_cdf(k: int, n: int, p: float) -> float:
    return sum(binom_pmf(i, n, p) for i in range(0, k + 1))


def clopper_pearson_band(n: int, p0: float, alpha: float = 0.05) -> tuple[int, int]:
    """Acceptance region: counts k whose exact two-sided test of H0: p=p0 is NOT
    rejected at `alpha`. Equivalent to the counts whose CP interval covers p0."""
    lo, hi = None, None
    for k in range(n + 1):
        # exact two-sided p-value, minimum-likelihood method's simpler cousin:
        # reject if k is in either tail beyond alpha/2
        left = binom_cdf(k, n, p0)
        right = 1.0 - binom_cdf(k - 1, n, p0) if k > 0 else 1.0
        keep = (left > alpha / 2) and (right > alpha / 2)
        if keep and lo is None:
            lo = k
        if keep:
            hi = k
    return lo, hi


def detection_power(n: int, true_rate: float, band: tuple[int, int]) -> float:
    """P(the calibration check FLAGS the cell) when the true Type-I rate is
    `true_rate` -- i.e. observed count falls outside the acceptance band."""
    lo, hi = band
    inside = sum(binom_pmf(k, n, true_rate) for k in range(lo, hi + 1))
    return 1.0 - inside


print("=" * 78)
print("1. C2 acceptance band and detection power  (H0: true Type-I rate = 5%)")
print("=" * 78)
for n in (100, 60, 40, 30):
    band = clopper_pearson_band(n, 0.05)
    lo, hi = band
    print(f"\nN_outer = {n:>3}   accept if observed rejections in [{lo}, {hi}]  "
          f"({lo/n:.1%} - {hi/n:.1%})")
    for true_rate in (0.08, 0.10, 0.15, 0.25):
        pw = detection_power(n, true_rate, band)
        verdict = "DETECTS" if pw >= 0.80 else ("weak" if pw >= 0.5 else "BLIND")
        print(f"    true rate {true_rate:>5.0%}  ->  flags it {pw:>6.1%} of the time   {verdict}")

print()
print("=" * 78)
print("2. Core-hour budget")
print("=" * 78)


def hours(cells: int, n_outer: int, b: int, sec: float) -> float:
    return cells * n_outer * b * sec / 3600


rows = [
    ("FROZEN C2        (4 cells x 100 x 4000, refit)", hours(4, 100, 4000, SEC_FULL)),
    ("FROZEN C3 primary(4 cells x 100 x 4000, refit)", hours(4, 100, 4000, SEC_FULL)),
    ("FROZEN C3 half   (4 cells x 100 x 4000, refit)", hours(4, 100, 4000, SEC_FULL)),
]
frozen_total = sum(h for _, h in rows)
for label, h in rows:
    print(f"  {label:<48} {h:>8,.0f} core-hours")
print(f"  {'FROZEN TOTAL':<48} {frozen_total:>8,.0f} core-hours "
      f"({frozen_total/24:,.0f} core-days)")

print()
prop = [
    ("C2  Comparison 1 only (2 cells x 40 x 999, cached)", hours(2, 40, 999, SEC_CACHED)),
    ("C3p Comparison 1 only (2 cells x 100 x 999, cached)", hours(2, 100, 999, SEC_CACHED)),
    ("C2  Comparison 2, run only if C1 clears (2 x 40 x 999)", hours(2, 40, 999, SEC_CACHED)),
    ("C3p Comparison 2, run only if C1 clears (2 x 100 x 999)", hours(2, 100, 999, SEC_CACHED)),
]
for label, h in prop:
    print(f"  {label:<48} {h:>8,.0f} core-hours")
gate1 = prop[0][1] + prop[1][1]
prop_total = sum(h for _, h in prop)
print(f"  {'PROPOSED, Comparison-1 gate only':<48} {gate1:>8,.0f} core-hours")
print(f"  {'PROPOSED, both comparisons':<48} {prop_total:>8,.0f} core-hours")
print()
print(f"  reduction, full pilot : {frozen_total:,.0f} -> {prop_total:,.0f} core-hours "
      f"({100*(1-prop_total/frozen_total):.1f}% cut)")
print(f"  reduction, first gate : {frozen_total:,.0f} -> {gate1:,.0f} core-hours "
      f"({100*(1-gate1/frozen_total):.1f}% cut)")

print()
print("  escalation reserve (C3 primary re-run at B=4000 if power lands 0.70-0.90):")
print(f"    {hours(2, 100, 4000, SEC_CACHED):>8,.0f} core-hours for Comparison 1")

print()
print("=" * 78)
print("3. Wall clock")
print("=" * 78)
for label, h in (("frozen", frozen_total), ("proposed (both comps)", prop_total),
                 ("proposed (first gate)", gate1)):
    print(f"  {label:<24} laptop @6 cores: {h/6/24:>5.1f} days   "
          f"64-core box: {h/64:>5.1f} h")
