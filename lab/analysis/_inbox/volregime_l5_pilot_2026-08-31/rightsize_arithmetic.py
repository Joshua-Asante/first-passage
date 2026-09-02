"""Arithmetic behind ACCEPTANCE_BANDS.md section 6 (right-sizing amendment).

No real data, no outcome-bearing statistic -- pure design arithmetic:
  1. exact Clopper-Pearson acceptance bands for Binomial(N_outer, 0.05), and
     the detection power that justifies KEEPING N_outer = 100
  2. the core-hour budget of the frozen sizing vs the proposed sizing

Timing inputs are CPU-seconds per replicate measured by
bench_replicate_timing.py with thread pools pinned to 1 (see that script's
docstring for why CPU time, not wall time, is the budget unit).
"""
from __future__ import annotations

from math import comb

# --- measured, bench_replicate_timing.py --reps 9, thread pools pinned -------
CPU_S_FULL = 0.953    # baseline refit inside every replicate
CPU_S_CACHED = 0.703  # volume-free baseline cached per outer panel
PEAK_MB_PER_WORKER = 258

# --- frozen design constants (sections 1-3, unchanged by the amendment) ------
CELLS = 4             # 2 instruments x 2 comparisons
N_OUTER = 100         # retained; see the detection table below
B_FROZEN = 4000
B_DIAGNOSTIC = 999    # proposed, non-gating C3 half-effect cell only


def binom_pmf(k: int, n: int, p: float) -> float:
    return comb(n, k) * p**k * (1 - p) ** (n - k)


def binom_cdf(k: int, n: int, p: float) -> float:
    return sum(binom_pmf(i, n, p) for i in range(0, k + 1))


def clopper_pearson_band(n: int, p0: float, alpha: float = 0.05) -> tuple[int, int]:
    """Counts k whose exact two-sided test of H0: p = p0 is NOT rejected."""
    lo = hi = None
    for k in range(n + 1):
        left = binom_cdf(k, n, p0)
        right = 1.0 - binom_cdf(k - 1, n, p0) if k > 0 else 1.0
        if (left > alpha / 2) and (right > alpha / 2):
            if lo is None:
                lo = k
            hi = k
    return lo, hi


def detection_power(n: int, true_rate: float, band: tuple[int, int]) -> float:
    """P(the C2 check FLAGS the cell) when the true Type-I rate is `true_rate`."""
    lo, hi = band
    return 1.0 - sum(binom_pmf(k, n, true_rate) for k in range(lo, hi + 1))


def core_hours(cells: int, n_outer: int, b: int, cpu_s: float) -> float:
    return cells * n_outer * b * cpu_s / 3600


print("=" * 78)
print("1. Why N_outer = 100 is RETAINED  (H0: true Type-I rate = 5%)")
print("=" * 78)
print("\nProbability the C2 calibration check flags a cell, by true Type-I rate:\n")
print(f"  {'N_outer':>8}  {'accept band':>13}   {'8%':>7} {'10%':>7} {'15%':>7} {'25%':>7}")
for n in (100, 60, 40, 30):
    band = clopper_pearson_band(n, 0.05)
    powers = [detection_power(n, r, band) for r in (0.08, 0.10, 0.15, 0.25)]
    tag = "  <- RETAINED" if n == N_OUTER else ("  <- rejected" if n == 40 else "")
    print(f"  {n:>8}  {f'[{band[0]}, {band[1]}]':>13}   "
          + " ".join(f"{p:>6.1%}" for p in powers) + tag)
print("\n  N_outer is the only parameter buying detection sensitivity. n=100 is")
print("  already effectively blind below ~15% inflation; cutting to 40 would move")
print("  that blind spot against 25% -- the magnitude Q-RANGEXFER-1 exhibited.")

print()
print("=" * 78)
print("2. Core-hour budget  (CPU-seconds x replicates; pinned threads)")
print("=" * 78)
print(f"\n  measured: {CPU_S_FULL:.3f} core-s/replicate full, "
      f"{CPU_S_CACHED:.3f} cached  ({1-CPU_S_CACHED/CPU_S_FULL:.1%} saving)\n")

frozen = {
    "C2 null-size": core_hours(CELLS, N_OUTER, B_FROZEN, CPU_S_FULL),
    "C3 power, primary": core_hours(CELLS, N_OUTER, B_FROZEN, CPU_S_FULL),
    "C3 power, half-effect": core_hours(CELLS, N_OUTER, B_FROZEN, CPU_S_FULL),
}
proposed = {
    # B stays 4000 for both GATING studies (Codex PR #258, P1): under broken
    # exchangeability -- the case C2 exists to detect -- Monte Carlo error near
    # the 0.05 boundary is B-dependent, so reducing B there could change
    # detection power rather than merely coarsen an irrelevant tail.
    "C2 null-size": core_hours(CELLS, N_OUTER, B_FROZEN, CPU_S_CACHED),
    "C3 power, primary": core_hours(CELLS, N_OUTER, B_FROZEN, CPU_S_CACHED),
    # Non-gating diagnostic: no decision rides on its Monte Carlo precision.
    "C3 power, half-effect": core_hours(CELLS, N_OUTER, B_DIAGNOSTIC, CPU_S_CACHED),
}

print(f"  {'study':<24} {'frozen':>12} {'proposed':>12}   note")
for k in frozen:
    note = ("B 4000 -> 999, non-gating" if "half" in k else "B unchanged, cached")
    print(f"  {k:<24} {frozen[k]:>9,.0f} c-h {proposed[k]:>9,.0f} c-h   {note}")
ft, pt = sum(frozen.values()), sum(proposed.values())
print(f"  {'TOTAL':<24} {ft:>9,.0f} c-h {pt:>9,.0f} c-h   "
      f"{1-pt/ft:.1%} cut")

print()
print("=" * 78)
print("3. Wall clock and memory")
print("=" * 78)
print(f"\n  peak working set: {PEAK_MB_PER_WORKER} MB per worker process (measured)")
for workers in (6, 64):
    print(f"\n  {workers} pinned workers:")
    for label, total in (("frozen", ft), ("proposed", pt)):
        print(f"    {label:<10} {total/workers:>7,.1f} h wall "
              f"({total/workers/24:>4.1f} days)   "
              f"resident ~{PEAK_MB_PER_WORKER*workers/1024:,.1f} GB")
print("\n  Timings are hardware-relative and vary ~15% run to run on a laptop.")
print("  Re-run bench_replicate_timing.py on the machine that will actually")
print("  execute the pilot before quoting a wall-clock or dollar figure.")
