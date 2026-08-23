# OPENPRESS-1 closure — FALSIFIED

**Closed:** 2026-07-21
**Verdict:** `FALSIFIED`
**Pre-registration:** [`OPENPRESS-1-verdict-preregistration.md`](../pre-registration/OPENPRESS-1-verdict-preregistration.md), frozen before outcome data (`73000fe` / `249b3c5`).
**Results:** [`lab/archive/opening_pressure_map_2026-07/RESULTS.md`](../../../lab/archive/opening_pressure_map_2026-07/RESULTS.md)

## Gate return

| Instrument | Coverage | Dev slope/t | Holdout slope | Pooled slope/t | Pred P90−P10 vs 4× cost | Pass |
|---|---|---:|---:|---:|---:|---|
| MNQ | 858 / 620 | +93.75 / 1.53 | +18.84 | +57.50 / 1.60 | 8.42 bp ≥ 3.64 bp | FAIL (dev+pooled t) |
| MYM | 859 / 618 | −3.63 / −0.13 | +29.38 | +9.22 / 0.41 | 1.71 bp < 6.41 bp | FAIL (dev+pooled+econ) |

Both instruments fail the frozen PASS set. MNQ clears coverage, holdout sign, and the cost spread, but development and pooled HAC t stay below 2. MYM fails development (wrong-signed), pooled significance, and the economic hurdle.

## Disposition

- Close the opening-volume × directional-efficiency BAR EXPORT mechanism on MNQ/MYM.
- K=0 consumed; no threshold, window, weekday, or single-instrument rescue licensed.
- Re-proposal requires a different modality or mechanism (true order-flow / absorption evidence), not a re-cut of RV or efficiency on the same OHLCV panels.
- No Pine, rail, account, allocation, lifecycle, or live-trading change.

- **Registry:** rejected_candidates.md — ### Opening-volume × directional-efficiency pressure map on MNQ/MYM
