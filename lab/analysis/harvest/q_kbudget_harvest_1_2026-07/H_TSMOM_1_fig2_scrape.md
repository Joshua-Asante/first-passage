# H-TSMOM-1 δ extraction — Moskowitz et al. 2012 Fig. 2 (cheap recovery)

**Date:** 2026-07-16  
**Source PDF:** Moskowitz, Ooi & Pedersen, *Time series momentum*, *JFE* 104 (2012) 228–250  
  (local fetch: `https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf`)  
**What was missing:** per-instrument δ/σ for an equity-index futures cohort (stub was `UNSCREENABLE:per-instrument-delta-sigma-not-extracted`).

## What we tried

| Path | Result |
|---|---|
| Prose / Table 1–6 | No per-contract TSMOM Sharpe or t-stat table. Table 1 = passive excess-return summary only. Table 2 = lookback×holding **alpha t-stats by asset class**, not by instrument. |
| AQR “Time Series Momentum: Original Paper Data” xlsx | Downloads cleanly; contains only **diversified** monthly factors `TSMOM`, `TSMOM^EQ`, `TSMOM^FX`, `TSMOM^FI`, `TSMOM^CM` (1985-01…2009-12). **No per-instrument series.** `TSMOM^EQ` SR_ann ≈ **0.83** (n=300) — equity-*class* only; **not admissible as ES δ** (cross-instrument / pooled transplant forbidden). |
| Fig. 2 (annualized gross Sharpe by instrument) | **Load-bearing extract.** Per-contract bars; equity set = ASX SPI 200, DAX, IBEX 35, CAC 40, FTSE/MIB, TOPIX, AEX, FTSE 100, **S&P 500**. **No NQ / Nasdaq contract in the paper universe.** |

## Digitization method (Fig. 2 top panel)

1. Render PDF page 10 at 2× with PyMuPDF.
2. Locate Sharpe axis from text bboxes: y(1.2) and y(0.0) → linear map `SR = 1.2 · (y0 − y_top)/(y0 − y12)`.
3. Detect bars by walking up from the 0.0 baseline; classify fill color (equity = near-black).
4. Nine contiguous equity bars (x≈654–746 px); map left→right to Appendix A equity list.

| Equity contract | Digitized gross SR (12m/1m TSMOM) |
|---|---|
| ASX SPI 200 | 0.35 |
| DAX | 0.66 |
| IBEX 35 | 0.55 |
| CAC 40 | 0.40 |
| FTSE/MIB | 0.84 |
| TOPIX | 0.61 |
| AEX | 0.51 |
| FTSE 100 | 0.34 |
| **S&P 500** | **0.58** |

Digitization tolerance: ~±0.03 SR (anti-alias / baseline). Conservative central for S&P 500: **SR = 0.58**.

## Convert Sharpe → Clause-N δ/σ

TSMOM positions are vol-scaled to constant ex-ante volatility (paper §4 / Fig. 2 caption). For monthly strategy returns,  
`δ/σ_monthly = SR_ann / √12`.

**S&P 500 plug:** δ/σ = 0.58 / √12 = **0.167**.

## Power at candidate N (informational; ratification picks N)

| Declared N (monthly events) | Power Φ(√N·0.167 − 1.96) |
|---|---|
| 78 (~6.5y OOS) | 0.31 — **FAIL** Clause N |
| 100 | 0.39 — FAIL |
| 192 (~2010–2025 post-publication OOS) | 0.64 — PASS |
| 300 (full 1985–2009 paper sample — **not OOS**) | 0.83 — PASS (IS; do not use as OOS N) |

Haircut SR→0.50 (δ/σ=0.144) at N=192 → power **0.52** (barely PASS). SR→0.45 at N=192 → **0.44 FAIL**. Break-even δ/σ at N=192 = 0.141.

## Admissibility notes (honest)

- **Cohort:** S&P 500 futures only. **NQ is absent** from Moskowitz’s nine equity indexes — do not transplant S&P→NQ.
- **Family for inventory:** ES → K_banked=1 (HARV). MNQ expression would be a *different* axis needing its own δ.
- **Gross-of-cost:** Fig. 2 is gross Sharpe (same class of caveat as D5 / H-OD-1).
- **Path 1b:** scored **PASS** at Phase 2 ([`PHASE2_RATIFICATION.md`](PHASE2_RATIFICATION.md)) — decades / cohorts / class-discovery replication pin / no structural 12m/1m sign-reversal. Digitization cleared **requirement 2 (δ)**; Path 1b is separate.
- **Event frequency:** monthly rebalance ⇒ Clause N is tight vs daily-footprint axes (D5 / H-OD-1).

## Outcome

Missing input **supplied**. Stub `H-TSMOM-1` promoted to a **four-field-complete candidate row** (see `CANDIDATE_ROWS.md`). **Phase-2 ACCEPT 2026-07-16** → inventory addendum **H2**.
