# Koijen axis-2 (Carry, JFE 2018) — OpenAlex substitute traversal — SOURCES_LOG

**Date:** 2026-08-17
**Operator election (fork resolved):** admit an OpenAlex-based substitute traversal — see
[`CANDIDATE_ROWS.md`](../radar_tier_a_burst_2026-07/CANDIDATE_ROWS.md) §Rank-1 axis-2 for the
fork itself (recorded 2026-08-16, `BLOCKED-AT-SOURCE`). This record is the executed traversal.
**Cost / K:** $0.00 · K=0 — a screen, not a pull; no `register_search open`, no Cap claim, no
manifest, no PnL computed. Matches `docs/methodology/strategy_harvest.md` §6 step 3 ("Screen —
zero pulls, zero K") and the sibling axis-1 (TSMOM) run's own discipline.
**Seed paper:** Koijen, Moskowitz, Pedersen & Vrugt, *Carry*, *JFE* 127(2) 2018, DOI
`10.1016/j.jfineco.2017.11.002`, OpenAlex `W4234492972`, cited_by_count 299 at pull time.
**Ad-hoc execution, no checked-in script** — matches the repo's own stated convention for the
axis-1 S2 traversal (`docs/methodology/strategy_harvest.md:83`: "a thin on-demand Semantic
Scholar script is the named automate-later step... not built now"). Data pulled via direct
OpenAlex REST API calls (`api.openalex.org/works?filter=cites:W4234492972`), screened via a
9-agent Workflow (screen → adversarial verify → synthesize), not a reusable tool.

---

## Why OpenAlex, not S2

S2 has no record of the seed paper at all — a genuine index gap, independently re-verified twice
(2026-08-16 recording session; 2026-08-17 this session), not throttling: DOI + NBER-edition 404s,
empty title/author/bulk searches, while axis-1's TSMOM DOI resolves fine on the same S2 endpoint
(health control). OpenAlex resolves the seed DOI instantly. OpenAlex has **no `isInfluential`
equivalent** to S2's citation-importance flag, so this run's funnel differs in shape from axis-1's
(which used influential-flag → futures-cohort keyword). This run went straight from a disclosed
keyword/topic pre-filter to full manual screening of every survivor — arguably *more* exhaustive
than axis-1 on this specific point (no opaque pre-narrowing flag), at the cost of more items to
review by hand.

## Funnel

| Stage | Count | Method |
|---|---:|---|
| Total citing works on OpenAlex | 296 | `cites:W4234492972`, paginated, `select` on id/title/year/cited_by_count/primary_topic/topics/concepts |
| Shortlisted (asset-class OR mechanism-shaped keyword hit in title/topics/concepts) | 234 | disclosed keyword lists — asset: futures/commodity/currency/carry trade/interest rate/bond/cross-asset/CTA/managed futures/term structure/forward/exchange rate/convenience yield/basis/FX; mechanism: seasonality/reversal/momentum/timing/predict/signal/anomaly/microstructure/intraday/daily/liquidity/order flow/high frequency/announcement/drift/day-of-week/turn-of-month/overnight/flow/positioning/sentiment/attention/hedging pressure/roll/seasonal/calendar |
| Manually pre-resolved before the workflow ran | 4 | all REJECT (2 monthly academic factor papers re-explaining an already-dead mechanism class; 2 wrong-instrument-class Indonesian government-bond papers) |
| Screened by 7 parallel screen-agents | 230 | reject fast on title/topics/concepts alone where clear; one targeted abstract lookup for genuinely ambiguous titles |
| → REJECT at screen | 213 | overwhelmingly class (a): monthly-or-slower cross-sectional/time-series academic factor papers — the same construction family as the seed paper itself |
| → FLAGged for adversarial verify | 17 | |
| **Survived adversarial verification** | **7 records / 6 distinct papers** | see below |

**Rejects at screen were not individually logged** (230 one-line verdicts; available in the
workflow journal, not duplicated here per this repo's own anti-accretion discipline) — the
96%-reject composition (221/230 REJECT across pre-resolve + screen + the 10 flags that reverted
on verify) is the headline number, matching the calibration note below.

## The 7 flagged → verified

10 of the 17 screen-stage FLAGs reverted to REJECT under adversarial re-check (disguised
carry/momentum variants once the abstract was read; a COT-positioning-lag data-access wall; one
construction that fails this venue's own hedging-rule / hedging-compliance framing; wrong
instrument class once confirmed). The reject-on-review detail per item is in the workflow journal,
not reproduced here.

**7 records survived — representing 6 distinct papers** (`W4377028459` and `W3103727571` are
duplicate OpenAlex records for the same Da/Tang/Tao/Yang *Management Science* 2023 paper).

| # | Paper | OpenAlex id(s) | WHO | WHEN / horizon | Instrument | Headline result | Load-bearing open question |
|---|---|---|---|---|---|---|---|
| 1 | Financialization and Commodity Markets Serial Dependence (Da, Tang, Tao, Yang, *Mgmt Sci* 2023) | `W4377028459`, `W3103727571` | Commodity-index investors / ETF arbitrageurs propagating nonfundamental noise | Daily rebalance, next-day reversal decay | 12 liquid CME/COMEX/NYMEX/CBOT commodity futures (crude, gold, corn, copper, nat gas, etc.) | After-cost annualized Sharpe 0.45 (GSCI) / 0.31 (BCOM) full-sample, 0.69/0.64 in high-index-exposure regimes (paper's own Table 3, 250-day rolling no-lookahead exposure measure) | How "daily index-trading exposure" is operationalized as a live-reconstructible variable — could reduce to a lagged/proprietary flow proxy, the same wall that has killed other WHO candidates here. Sample window 2006–2018; index-flow intensity may have declined since. |
| 2 | Delta-hedging demand and intraday momentum: Evidence from China | `W4280500240` | Option dealers deferring delta/gamma-hedge rebalancing to end-of-day | Same-day; rest-of-day return → last-30-min return, decaying ~3 days | Chinese SSE50/CSI300 ETF options → plausible CME analog (SPX/ES, NDX/NQ dealer-GEX) | Effect described, not backtested as a standalone strategy in the abstract | Direct study instrument is not CME-native — needs a real transplant test, not an assumption. Adjacent to this repo's own `Q-ORB-GEX-1` (rejected 2026-06-25, edge collapsed to a realized-vol proxy) — different construction, but that orthogonality failure is a named caution. |
| 3 | Market Closure and Short-Term Reversal (Della Corte, Kosowski & Wang, working paper 2015) | `W2261108883` | Risk-averse market makers with limited inventory-risk capacity, compensated for absorbing overnight order imbalance released at the open | Daily, close-to-open (CO-OC) reversal held through the session | 35 CME futures (5 equity indices, 11 rates, commodities, currencies) | Rates 0.06%/day t=11.85 Sharpe 2.20; FX 0.17%/day t=10.84 Sharpe 1.93; commodities 0.04%/day t=6.76 Sharpe 1.26 | Authors' own bid-ask-bounce robustness check ran only on equities, not the futures leg — net-of-cost economics for the futures universe are unverified in the paper. This program's dominant null mode to date (H-OD-1, D5) is exactly "real mechanism, dies at Stage-2 cost-law." |
| 4 | Tomorrow Is Another Day: Stocks Overweighted by Active Mutual Funds Predict the Next-Day Market (Chen, Chen & Cohen, 2021) | `W3217619654` | Active mutual-fund managers' aggregate private information, inferred from holdings-overweight dispersion | Next-day horizon | S&P 500 futures (explicitly backtested); replicates on other global index futures | >15% annualized, Sharpe >0.9 | Real-time availability/lag of the mutual-fund-holdings input (likely 13F/N-Q, quarterly with ~45-day disclosure lag) defining the "overweighted" basket — the load-bearing data-access question, unresolved at screen level. |
| 5 | Exploiting the Dynamics of Commodity Futures Curves (Bianchi, Fan, Miffre & Zhang) | `W3130905024` | Weakest WHO of the six — risk-premium/sentiment-linked, no forced-flow counterparty named | One-day-ahead continuation of Nelson-Siegel curve-slope movements | Commodity futures term structure (NYMEX/COMEX/CBOT) | OOS Sharpe 1.41 before costs | Adjacent to an already-FALSIFIED repo candidate (`commodity-carry-term-structure` on USOIL, "disguised long-oil trend trade") but distinguishable — this trades the *change* in curve slope cross-sectionally, not a static contango/backwardation state. NS-curve depth/liquidity per commodity needs checking before assuming clean CME expressibility across the full set used. |
| 6 | Overnight-Intraday Reversal Everywhere (Della Corte, Kosowski, Liu & Wang) | `W4387717685` | Market makers absorbing overnight order imbalance, unwinding into the day session — same family as #3, larger effect size | Daily overnight-to-open signal, held through intraday | Equity index, rate, commodity, and currency futures (explicit) | Reported Sharpe 2–5× conventional (slower) reversal | **Likely overlaps with #3** — overlapping authors (Della Corte & Kosowski on both), and #6's own verify pass flagged "may lean cross-sectional/multi-instrument rather than a pure single-CME-contract bar-level trigger." Treat #3 and #6 as **one research program, not two independent leads**, until resolved by reading both papers directly. |

## Calibration note (resolves the 2026-08-16 open question)

The repo's own prior — the Carry neighborhood (~299 works, ~1/4.5 of TSMOM's 1,364) is smaller
and more portfolio/cross-sectional than axis-1's — is **confirmed in bulk composition**: ~96% of
everything actually screened (221/230, once the 10 verify-reverts are folded in) died as class (a),
the same monthly-or-slower cross-sectional academic-factor construction as the seed paper. But the
prior's implied trajectory — that a smaller, more cross-sectional neighborhood runs to zero like
axis-1 — is **not confirmed**. This axis produced 6 non-trivial leads where axis-1 produced none,
concentrated specifically in overnight/closure-reversal and hedging/rebalancing-flow mechanisms —
not carry, not trend-following, not cross-sectional factor construction. The smaller neighborhood
is real; it is not uniformly dead.

## What this record does NOT license

- None of the 6 leads is an admitted Req-1a candidate. Every one carries a named, unresolved,
  load-bearing question (see table) that a real Path 1a/1b pass would need to close first — most
  commonly: is the WHO's driving variable actually reconstructible in real time from data this
  repo can access, and does the edge survive this venue's own cost/spread reality (the dominant
  null mode for prior "real mechanism, real WHO" candidates here).
- No `register_search open`, no Q-ID, no G0, no Pine, no Cap claim, no CONFIRM read (there is no
  CONFIRM partition at this stage — no data was pulled beyond citation metadata and abstracts).
- #3 and #6 should not both be staged as independent candidates without first resolving whether
  they are the same research program.
- This is a $0/K=0 screen; staging any of the 6 for a real Path 1a/1b pass is a fresh operator
  decision, not licensed by this record.

## Reproducibility

Ad-hoc, not checked in (matches the axis-1 convention). The OpenAlex pull and keyword pre-filter
used a scratch Python script (`requests` against `api.openalex.org`); the screen/verify/synthesis
ran as a 25-agent Workflow (7 screen batches of 33 items → adversarial verify on 17 flags →
1 synthesis). Full per-item verdicts and tool-call evidence live in that workflow's journal
(session-local, not part of this repo). Re-runnable for $0 by repeating the same OpenAlex query —
the citation graph is append-only forward in time, so a re-run would only ever add works, never
lose the ones found here.
