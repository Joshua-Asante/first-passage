# Moskowitz 2012 Fig.2 — vector digitization (radar burst)

**Date:** 2026-07-16  
**PDF:** `https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf` (local fetch under this dir; not required for consumers)  
**Script:** [`digitize_fig2.py`](digitize_fig2.py) · results [`fig2_digitize_results.json`](fig2_digitize_results.json)  
**Precedent:** [`lab/analysis/q_kbudget_harvest_1_2026-07/H_TSMOM_1_fig2_scrape.md`](../q_kbudget_harvest_1_2026-07/H_TSMOM_1_fig2_scrape.md)  
**JPY recovery:** [`CHEAP_RECOVERY_JPY.md`](CHEAP_RECOVERY_JPY.md) · [`cheap_recovery_usdjpy.json`](cheap_recovery_usdjpy.json)

## Method

1. Open PDF page with Fig.2 caption (page 10 / print page 237).  
2. Collect filled `re` drawings with width ≈2.6 pt and bottom on empirical baseline **y = 182.3**.  
3. Classify fill: darkgrey ≈ commodities · white ≈ currencies · black ≈ equities · lightgrey ≈ fixed income.  
4. Sharpe scale using bar baseline as 0.0 and text label **1.2** at y=69.87:  
   `SR = 1.2 · (182.3 − y_top) / (182.3 − 69.87)` (Y0/Y12 from text spans in script).  
5. Tolerance: **±0.03 SR** (same honesty band as H-TSMOM-1 scrape).  
6. FX short bars: height filter **h > 3** (not 5) — recovers the near-zero EUR-SEK bar; **n_white = 12**.

## Equity validation (load-bearing)

Black bars left→right vs prior scrape (Appendix A.1 order):

| Contract | Prior scrape SR | This digitize SR | Δ |
|---|---:|---:|---:|
| ASX SPI 200 | 0.35 | 0.328 | −0.022 |
| DAX | 0.66 | 0.627 | −0.033 |
| IBEX 35 | 0.55 | 0.527 | −0.023 |
| CAC 40 | 0.40 | 0.383 | −0.017 |
| FTSE/MIB | 0.84 | 0.801 | −0.039 |
| TOPIX | 0.61 | 0.582 | −0.028 |
| AEX | 0.51 | 0.482 | −0.028 |
| FTSE 100 | 0.34 | 0.325 | −0.015 |
| **S&P 500** | **0.58** | **0.552** | −0.028 |

Systematic ≈ −0.03 bias vs the pixmap scrape — **inside the stated tolerance**. S&P identity of the last equity bar is confirmed. **Do not re-stage H-TSMOM-1.**

## Currencies (white bars) — labels ratified 2026-07-16

n = **12** white bars. Label map from Hurst–Ooi–Pedersen 2013 *Demystifying Managed Futures* Fig.2 (explicit L→R tick labels; same 12-pair set; shared Ooi/Pedersen). Moskowitz Fig.2 itself remains unlabeled — identity is **cross-paper**, not from Moskowitz text.

| Order L→R | Pair | Moskowitz SR | Demystifying 12m SR (labeled) |
|---:|---|---:|---:|
| 1 | AUD-NZD | 0.05 | 0.08 |
| 2 | AUD-USD | 0.35 | 0.52 |
| 3 | EUR-JPY | 0.37 | 0.31 |
| 4 | EUR-NOK | 0.39 | 0.48 |
| 5 | EUR-SEK | 0.02 | 0.12 |
| 6 | EUR-CHF | 0.15 | 0.24 |
| 7 | EUR-GBP | 0.24 | 0.33 |
| 8 | AUD-JPY | 0.37 | 0.45 |
| 9 | GBP-USD | 0.27 | 0.09 |
| 10 | EUR-USD | 0.24 | 0.25 |
| 11 | USD-CAD | 0.49 | 0.43 |
| 12 | **USD-JPY** | **0.49** | **0.54** |

**`H-TSMOM-6J` plug:** conservative central SR **0.49** (Moskowitz bar 12) → δ/σ = 0.1415 → power@N=192 = **0.50**. See [`CHEAP_RECOVERY_JPY.md`](CHEAP_RECOVERY_JPY.md).

## Commodities / FI

- Darkgrey n≈22–24 — SRs in JSON; **no ratified WTI name map this recovery** (Demystifying commodity universe is 19 contracts; Moskowitz differs). Carry stub `H-CARRY-CM-1` still needs Koijen per-contract δ, not a TSMOM bar.  
- Lightgrey n=13 matches Appendix A.2 bond count — FI TSMOM not a current prop leg; not staged.

## Convert SR → δ/σ

Vol-scaled monthly strategy (paper §4): `δ/σ = SR_ann / √12`.  
Clause-N power at N=192 needs SR ≳ 0.49 for power ≥ 0.50 under this formula.
