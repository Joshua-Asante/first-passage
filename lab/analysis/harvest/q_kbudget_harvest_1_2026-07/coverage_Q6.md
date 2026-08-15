# Coverage log — Q6 (Tier-2 anomaly surveys / instrument-level futures δ)

**Query family:** Tier-2 anomaly surveys / handbooks reporting **instrument-level** futures δ or net Sharpe (not SPX-only)
**Target families:** any unbanked or low-K family
**Search date:** 2026-07-16
**Queries used:**
1. `futures anomaly survey handbook instrument-level Sharpe momentum carry NBER working paper`
2. `Moskowitz Ooi Pedersen 2012 time series momentum Journal of Financial Economics equity index futures Sharpe`

| Source | Venue / year | Examined | Economic grounding (1a/1b) | Four-field outcome |
|---|---|---|---|---|
| Moskowitz, Ooi & Pedersen — "Time series momentum" | *JFE* 2012 | PDF + Fig. 2 digitize + AQR factor xlsx | **1b PASS** (Phase-2 score) | **`ROW` → `H-TSMOM-1` → ACCEPT H2** after cheap recovery 2026-07-16: Fig. 2 S&P 500 gross SR=0.58 → δ/σ=0.167; see [`H_TSMOM_1_fig2_scrape.md`](H_TSMOM_1_fig2_scrape.md). AQR xlsx = class factors only (not used as δ). **No NQ in universe.** |
| Koijen, Moskowitz, Pedersen & Vrugt — "Carry" | NBER w19325 | PDF abstract | 1a/1b carry | `EXCLUDE:multi-asset-carry-portfolio` — no single-instrument NQ/ES/6J confirm δ for mechanism-first K≤3 without a fresh construct pin |
| Hurst / AQR — "A Century of Evidence on Trend-Following" | *JPM* 2017 | PDF skim | 1b corroboration for TSMOM | Tier-2 index into Moskowitz — not an independent δ source (avg Sharpe ~0.4 across 67 markets; not per-NQ) |
| Baltas — momentum in futures / CTA | working | abstract | 1b corroboration | same — no new per-contract δ |

**New rows from Q6:** `H-TSMOM-1` four-field-complete after Fig. 2 scrape (was UNSCREENABLE stub).
