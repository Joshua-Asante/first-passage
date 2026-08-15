# Cheap recovery — Fig.2 FX label map → `H-TSMOM-6J`

**Date:** 2026-07-16  
**Stub cleared:** `H-TSMOM-6J` Req-2 (per-instrument δ/σ)  
**Machine log:** [`cheap_recovery_usdjpy.json`](cheap_recovery_usdjpy.json)

## What was blocked

Moskowitz, Ooi & Pedersen 2012 *JFE* Fig.2 digitizes cleanly (12 white FX bars after loose height filter), but the figure itself has **no extractable tick labels**. Appendix A.3 lists 10 USD-linked rates while the body says **12 cross-currency pairs** — forced assignment refused.

## What cleared it (zero pull)

**Hurst, Ooi & Pedersen (2013), *Demystifying Managed Futures*, *JOIM*** Fig.2 prints the **same 12 FX pairs with explicit L→R labels**:

`AUD-NZD, AUD-USD, EUR-JPY, EUR-NOK, EUR-SEK, EUR-CHF, EUR-GBP, AUD-JPY, GBP-USD, EUR-USD, USD-CAD, USD-JPY`

Shared coauthors (Ooi, Pedersen) with Moskowitz 2012; identical 12-pair set.

| Panel | USD-JPY digitized SR (±0.03) |
|---|---:|
| Demystifying Fig.2 **12-Month TSMOM** (labeled) | **0.54** (0.536 raw) |
| Demystifying Fig.2 1-Month TSMOM (labeled) | 0.41 |
| Moskowitz Fig.2 rightmost white bar under Demystifying L→R order | **0.49** (0.494 raw) |

12-Month is the lookback matching Moskowitz Fig.2 / H-TSMOM-1.

## Plug for Clause N

- **Label authority:** Demystifying labeled **USD-JPY** (CME expression → **6J** family).  
- **Conservative central SR:** **0.49** (lower of the two 12m corroborating reads — Moskowitz mapped).  
- `δ/σ = 0.49 / √12 = **0.1415**`  
- At N=192: `power = Φ(√192·0.1415 − 1.96) = **0.50**` — Clause N **PASS** at the floor.  
- Break-even SR at N=192 ≈ **0.490**; haircut to 0.45 → power 0.44 **FAIL**. Margin is thin — record explicitly.

Demystifying-primary alternate (SR 0.54 → δ/σ 0.155 → power 0.57) is available if operator prefers the labeled panel as the sole plug; conservative path uses the lower corroborating read.

## What this does **not** clear

- `H-CARRY-FX-1` / `H-CARRY-CM-1` — still need per-contract carry δ (Koijen class SRs remain inadmissible).  
- Gold / GC TSMOM — still Req-3 FAIL-K.  
- No `floor_scan` append / inventory addendum until operator pins N **and** ratifies.
Under Campaign-defaults Default #1 (OOS from 2019-05-06, N≈86) Clause N **FAILS** at this δ
(power≈0.26) — same fork that closed H-TSMOM-1. Demystifying-primary SR 0.54 does not rescue N=86.
