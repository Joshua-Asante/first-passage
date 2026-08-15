# Coverage log — Q1 (intraday momentum / hedging-demand price footprint)

**Query family:** Intraday momentum / hedging-demand / dealer-hedging **price footprint** (not γ-sign)
**Target families:** NQ/MNQ, ES, YM (YM liquidity caveat if used)
**Search date:** 2026-07-16
**Queries used:**
1. `intraday momentum hedging demand futures NQ ES YM Baltussen market microstructure JFE`
2. `Gao Han Li Zhou market intradayer momentum JFE futures overnight return anomaly ES NQ`

| Source | Venue / year | Examined | Economic grounding (1a/1b) | Four-field outcome |
|---|---|---|---|---|
| Baltussen, Da, Lammers & Martens — "Hedging demand and market intradayer momentum" | *JFE* 2021 | yes (abstract + DOI/SSRN) | 1a — short-gamma / LETF hedging demand | `EXCLUDE:already-D5` (E.1) |
| Gao, Han, Li & Zhou — "Market intradayer momentum" | *JFE* 2018 | yes (abstract) | 1a/1b-ish — infrequent rebalancing / late-informed | `EXCLUDE:SPY-ETF-cohort-not-futures` — primary cohort is SPY 1993–2013; Baltussen is the futures-native extension already inventoried as D5 |
| Lettermeyer et al. — LETF / option imbalances EOD | working / conference PDF | skim | 1a — LETF + MM gamma | `EXCLUDE:equity-TAQ-not-index-futures-δ` — stock-level TAQ; cites Baltussen; no extractable NQ/ES futures δ independent of D5 |
| Practitioner ORB / HOD blogs (tradingstats.net, etc.) | blog | titles only | — | `EXCLUDE:blog-out-of-scope` (§D) |

**New rows from Q1:** none (D5 already owns the fundable footprint; Gao is the ETF precursor, not a second axis).
