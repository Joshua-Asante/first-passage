# Skewed-family construction + characterization — Q-GEOFIT-1 successor scoping (2026-08-15)

**Status:** scoping construction, follow-up to [`geofit_skew_probe_2026-07-25`](../../../archive/geofit_skew_probe_2026-07-25/README.md) and [`geofit_iid_sufficiency_power_2026-08-15`](../geofit_iid_sufficiency_power_2026-08-15/README.md). **Not** part of Q-GEOFIT-1 (CLOSED `AMBIGUOUS-PARAMETERIZATION`, 2026-07-25) and **not** a re-open of it. No envelope, no grid, no cells, no candidate claim. **$0.00 spend, zero K.**
**Driver:** [`family_skewed_gamma.py`](family_skewed_gamma.py) (the reusable family: `fit_family`, `draw_series`) · [`run_characterize.py`](run_characterize.py) (pre-declaration in its module docstring) · data [`characterize.json`](characterize.json) · log [`run_characterize.log`](run_characterize.log)

## What this is

The two prior probes closed both open questions from the original Q-GEOFIT-1 closure: skew is the dominant missing dimension, and the true marginals (i.i.d.) are sufficient — no block structure needed. This step builds the actual reusable family a successor grid would sweep, and characterizes what it produces when fit to the real book.

**Design decision (operator-directed):** the win branch's heavy right tail is a measured feature of the real book (n=150, mean $463, median $85, max $4,972 — 10.7× the mean), not a fitting artifact. The choice was to **preserve it, not cap it** — capping would understate exactly the risk a trailing-DD survival gate exists to price. See [`family_skewed_gamma.py`](family_skewed_gamma.py)'s module docstring for the full reasoning. Consequence: the family's win branch is an uncapped Gamma (k≈0.359, method-of-moments matched); the loss branch is well-behaved (k≈0.920, near-exponential) and needed no such decision.

## Result — and it is the load-bearing finding of this step

Fit to the real c1 book, 50 fresh realizations (seeds 20260815100–20260815149), same tier/geometry/engine as both prior probes:

| | value |
|---|---|
| bust mean | **7.46%** |
| bust sd | **7.07pp** |
| bust range | 0.68% – 36.53% |
| bust p10 / p50 / p90 | 1.65% / 5.57% / 14.13% |
| **N-SURV floor_ok (bust≤3.0% ∧ pass≥50%)** | **15/50 = 30.0%** |
| real book's own historical bust (4.7433%) rank | ~44th percentile of this distribution |

**The real book's single historical realization is not a lucky draw — it sits close to the median of what its own statistical shape produces.** And that shape's median (5.57%) is nearly double the 3.0% ceiling; only 30% of resampled realizations clear the gate at all.

## Why this matters beyond this probe

`run_partition_mc` — the engine every N-SURV kill in this estate is built on — resamples **order** (block-bootstraps a fixed, already-observed daily-P&L series into many equity paths). It does not resample **magnitude** — it never asks "would a different, equally-plausible history from the same underlying process have produced a similar bust rate." For a symmetric, thin-tailed book those two questions would answer similarly. For this book's own shape they do not: 7.07pp of spread from resampling magnitude alone, against a single-history point estimate that carries none of it.

Every N-SURV closure this estate has ever produced (Q-TXG-1's two transfer cells, Guardian→MGC, Q-COMPOSE-1, ORB-MNQ-1) reads a single historical bust rate as if it were the candidate's survival probability. This characterization suggests that for any skew-heavy candidate — and skew-heavy is not an edge case here, it is the shape of every trend-following/pyramided strategy in the locked book — a single-history read may be substantially more optimistic than the family's own resampling distribution says is typical. This was not the question this probe set out to answer; it fell out of building the family honestly.

## Open for the successor brief (not decided here — deferred per Trap #12)

1. **z-range** — `draw_series()` already accepts an explicit `z` override, so extending past the closed family's 0.40 ceiling to ≈0.80 (§8 item 2 of the Q-GEOFIT-1 closure) is mechanically ready; no grid has been run with it yet.
2. **CFD-book scope** — this construction targeted the c1 (futures) book only. The CFD book was in Q-GEOFIT-1's original §3 range-check, but CFD trading is fully retired estate-wide; I assumed that retirement makes it out of scope for a successor and did not fit or test against it. Flagging the assumption rather than silently deciding it belongs.
3. **Admission rule against a distribution, not a point** — a future grid's `floor_ok` predicate needs to decide what statistic of a cell's resampled distribution gates admission: the mean (7.46%, itself pulled up by the same right tail under discussion), the median (5.57%), a conservative percentile (p90 = 14.13%), or the existing single-history convention (which this characterization suggests may be too optimistic for this shape class). This is a risk-tolerance decision, not a mechanical one.
4. **Whether the single-history N-SURV convention itself needs a second uncertainty layer** — the larger question in "Why this matters beyond this probe." This is bigger than the Q-GEOFIT successor and touches every closed and future N-SURV verdict on a skew-heavy candidate.
