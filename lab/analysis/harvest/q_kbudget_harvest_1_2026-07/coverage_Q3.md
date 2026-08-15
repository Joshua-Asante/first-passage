# Coverage log — Q3 (order-flow / inventory-hedging footprints)

**Query family:** Order-flow or inventory-hedging footprints with per-index **futures** cohorts
**Target families:** NQ, ES
**Search date:** 2026-07-16
**Queries used:**
1. `dealer inventory hedging order flow futures ES NQ gamma exposure empirical paper JFE RFS`
2. `Bogousslavsky infrequent rebalancing intraday momentum futures OR inventory risk E-mini overnight drift paper`

| Source | Venue / year | Examined | Economic grounding (1a/1b) | Four-field outcome |
|---|---|---|---|---|
| Boyarchenko et al. overnight drift (inventory + RSV close) | FRBNY SR 917 | yes | 1a | counted under Q2 as `H-OD-1` (same paper — do not double-count) |
| Bogousslavsky — "Infrequent Rebalancing, Return Autocorrelation, and Seasonality" | *JF* 2016 | abstract | 1a — infrequent institutional rebalancing | `EXCLUDE:equity-cross-section-model-paper` — no extractable ES/NQ **futures** cohort δ/σ |
| Bookmap / NexusFi / CrossVol GEX explainers | blog/vendor | titles | — | `EXCLUDE:blog-vendor-out-of-scope` |
| Baltussen γ-hedging channel | *JFE* 2021 | yes | 1a | already D5 (E.1) |

**New rows from Q3:** none beyond `H-OD-1` (already emitted under Q2).
