# Coverage log — Q2 (session-timing / opening-range / last-hour)

**Query family:** Session-timing / opening-range / last-hour futures anomalies with **per-contract** stats
**Target families:** NQ, ES, YM, GC
**Search date:** 2026-07-16
**Queries used:**
1. `opening range last hour session timing anomaly futures NQ ES YM GC empirical study`
2. `Boyarchenko Larsen Whelan overnight drift equity futures staff report`

| Source | Venue / year | Examined | Economic grounding (1a/1b) | Four-field outcome |
|---|---|---|---|---|
| Boyarchenko, Larsen & Whelan — "The Overnight Drift" | FRBNY Staff Report 917 (2020; rev. 2022); SSRN 3546173 | yes (PDF + Liberty Street posts) | **1a** — inventory-risk / MM liquidity provision resolving U.S. close imbalance at EU open (Grossman–Miller class) | **`ROW` → see CANDIDATE_ROWS `H-OD-1`** |
| Boyarchenko, Larsen & Whelan — "The Disappearing Overnight Drift" | Liberty Street Economics 2026-07 | yes | same mechanism; documents post-2021 fade (RSV dispersion compression); NQ+YM same signature | logged as **decay/attenuation caveat** on `H-OD-1` (does not void Path 1a; Path 1b's "no sign-reversal" bar is N/A because 1a cleared) |
| Gao et al. 2018 first-half→last-half | *JFE* | yes | see Q1 | `EXCLUDE:SPY-ETF-cohort-not-futures` |
| tradingstats.net ORB / HOD / session-open studies | blog | titles | — | `EXCLUDE:blog-out-of-scope` |
| "NQ Futures Opening Range Breakout Study — 2026" (vercel) | unpublished web | skim | — | `EXCLUDE:non-peer-reviewed-web` |

**New rows from Q2:** `H-OD-1` (overnight drift).
