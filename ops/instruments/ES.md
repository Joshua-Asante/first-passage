# INSTRUMENT LEDGER — ES

**Symbol:** CME E-mini S&P 500 futures (ES; Globex, Databento dataset `GLBX.MDP3`) · **Micro sibling:** MES (1/10th notional) · **Asset class:** equity index futures
**Contract (cost-hurdle basis used on file):** MES **$5/pt multiplier, $1.25 tick**, single-RT hurdle ≈ **1.7bp** at the study's ~4373 reference price (HARV-2026-001 cost model)
**Status:** **Research/discovery venue only — no live strategy, no allocation, no sizing implications.** Locked-book futures-prop fan-out is NO-GO ([`docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md`](../../docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md)); self-funded scale (Aegis→M6J + Guardian-MGC) is **PARKED/CLOSED** as of 2026-07-16 ([`docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md`](../../docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md)) — **there is no active self-funded lane**; the standing program is the four-firm prop-portfolio discover→productionalize→execute programme ([`ADR 2026-07-12`](../../docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md)). ⚠ **No deployed book, no live cap allocation, no elected venue** — both Striker legs withdrawn 2026-08-04; disposition forks **F2** (rail) / **F3** (successor venue). Do not compose against, decorrelate from, or size a variance budget on a live MYM+MNQ Tradeify book. ES has hosted one discovery candidate: HARV-2026-001, closed **AMBIGUOUS 2026-07-12** (E3).
**Last updated:** 2026-08-06

**Purpose:** single source of instrument-level truth (operational rule 10, [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). Any session deriving/testing/adjudicating on ES MUST read this at session start and append a dated disposition. **Created 2026-07-12** — Q-HARV-0's Phase-0 Rule-0 read found the card ABSENT ([`PHASE0_REPORT.md §0.8`](../../lab/archive/harv_0_month_end_rebalance_es_2026-07/PHASE0_REPORT.md)). Distinct instrument from the CFD index ledgers [`SPX500.md`](SPX500.md) / [`US500.md`](US500.md) (cash-index CFD, closed FXIFY venue) — findings do not transfer automatically in either direction.

## PROFILE (machine-readable)

```yaml
symbol: ES
asset_class: equity-index-futures
family: []
venue_tradable: true
k_bank_source: "../../discovery_manifests/"
cost_hurdle:
  value: 6.84
  units: "bp"
  basis: "4x MES single-RT hurdle at HARV-2026-001 reference price (~4373)"
  source: "#E4"
cells:
  - mechanism: turn-of-month
    verdict: AMBIGUOUS-PARKED
    date: 2026-07-12
    source: "../../docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md"
bars:
  - id: index-intraday-ohlcv-directional-timing-2026-07-21
    source: "../../docs/rejected_candidates.md"
structure:
  - claim: "The month-end ES-vs-ZN rebalancing fade shows a real pooled effect (+19.21bp, perm p=0.0129) but is era-decaying and reverses the following month (-15.96bp) - a structural caveat for any future turn-of-month construct on this instrument, not a deployable edge."
    source: "#E3"
```

---

## STANDING WARNINGS (read first — bind any GLBX/Databento window work)

- **W1 — `.c.0` continuous is calendar-roll, front-month, UNADJUSTED.** Raw front-month price with a discontinuity at every roll. Measured on ES: **+1.35% (+69.5pt) phantom jump** at the Mar-2024 ESH4→ESM4 roll weekend (5116.25 Fri 2024-03-15 → 5185.75 Sun 2024-03-17, no market move — the calendar spread). ES rolls **quarterly, mid-month** (3rd-Fri expiry: Mar/Jun/Sep/Dec) — any return window spanning a roll date is contaminated by ~135bp-class phantoms. Windows confined to month-end (e.g. close(T-3)→close(T-1)) are roll-clean; month-spanning measures (spread/momentum lookbacks) are NOT for quarter-end months.
- **W2 — Databento `ohlcv-1d` buckets by UTC calendar day → phantom Sunday bars.** The Sunday-evening Globex reopen (Sun 18:00 ET) lands in its own thin bar with a **Sunday** settle-date, shifting every month-end T-k offset (a March-2024 sample resolved T-1 to Sun 03-31 instead of the true Thu 03-28). **Drop settle-date weekday > 4 (Sat/Sun) before any trade-date offset work** — the real Monday session is carried by its own Monday bar, so nothing real is lost. Companion convention: the ohlcv-1d "close" is the last trade of the UTC-day bar (≈19–20:00 ET), NOT the 16:00 ET equity settlement print — consistent close-to-close within the feed, a disclosed offset vs equity settles.

---

## DURABLE FINDINGS

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **E1** | **Roll rule for Databento GLBX continuous (`.c.0`) — calendar roll, front-month rank 0, unadjusted** (W1). Decisive evidence = the measured +1.35%/+69.5pt ESH4→ESM4 level jump. Trading-day calendar derived from bars-present in the feed (not `exchange_calendars`) is the stronger match for offset counting — days used are exactly the days carrying returns. | [`NOTES.md`](../../lab/archive/harv_0_month_end_rebalance_es_2026-07/NOTES.md) roll-rule section, 2026-07-12 | **HIGH** (empirically measured). |
| **E2** | **UTC-day bucketing / Sunday-bar contamination + fix** (W2). Regression-tested (`test_load_symbol_frame_drops_weekend_bars`); pre-existing synthetic tests used `bdate_range` so never exercised a weekend bar — the real-data path was silently wrong. Feed-general across GLBX symbols (ES/YM/ZN/GC/micros). | [`NOTES.md`](../../lab/archive/harv_0_month_end_rebalance_es_2026-07/NOTES.md) data-hygiene fix, 2026-07-12 | **HIGH**. |
| **E3** | **Month-end conditional rebalancing effect — real-but-thin, era-decaying (HARV-2026-001, closed AMBIGUOUS 2026-07-12).** Fading the intra-month ES-vs-ZN outperformer over close(T-3)→close(T-1) = **+19.21bp, perm p=0.0129 pooled** (192 months / 163 qualifying, 2010-07→2026-06), clearing the ≥4×-hurdle gate (6.84bp), **but era-decaying** (2018-26 subset p=0.1049 n.s.; micro-era parent p=0.13 n.s.) and the §6 trigger that fired — the placebo *magnitude* clause — was shown post-closure to be **structurally un-passable at registration (selection arithmetic: every mid-month sub-window of qualifying months mechanically carries ~30-39bp anti-signal drift vs the 9.6bp allowance)**. **Not a roll artifact:** the roll-clean ex-quarter-end subset is *stronger* (+25.13bp, p=0.0164, n=107). Effect is **RTH-concentrated** — intraday (open→close) component **+21.10bp** exceeds the full-window +19bp; overnight gaps contribute negatively. **Next-month reversal −15.96bp** (transient-pressure/reversal, Etula / Parker-Schoar-Sun class). NOT an edge claim: AMBIGUOUS closure, no monitor, no deployment fork (deployability annotation YES is informational only); re-open requires a fresh pre-registered brief (window/threshold drift on this one is a forbidden move, trap #12). | HARV-2026-001, [`RESULTS.md`](../../lab/archive/harv_0_month_end_rebalance_es_2026-07/RESULTS.md) + closure [`docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md`](../../docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md) | **MODERATE** (pooled-significant, corroborated by GC control + MES same-sign; era-decaying; the RESOLVED bar was unreachable by gate geometry). |
| **E4** | **MES cost basis for hurdle math:** $5/pt multiplier, $1.25 tick (0.25pt), single-RT hurdle **1.71bp** at the study's 4373 reference price (4× = 6.84bp; two-RT deployable form 4× = 13.68bp). Any future ES/MES capturability gate should re-derive the hurdle at prevailing price levels (bp hurdle shrinks as the index rises), keeping the 4×-hurdle qualification discipline from the HARV-0 brief. | HARV-2026-001 cost-hurdle model ([`cost_hurdle.py`](../../lab/archive/harv_0_month_end_rebalance_es_2026-07/cost_hurdle.py)) | **HIGH** (contract facts + arithmetic). |

## DEAD / REJECTED (instrument-specific)

None yet. (HARV-2026-001 closed AMBIGUOUS, not FALSIFIED — see E3 for its re-open bar.)

## ACTIVE / OPEN

- **HARV-2026-001 (month-end ES-vs-ZN rebalancing fade) — CLOSED AMBIGUOUS 2026-07-12.** No monitor spec (AMBIGUOUS ⇒ N/A per brief §closure rules); K ledger closed at K=1. Residual facts worth a future fresh brief: era decay (post-2018 weakening), RTH-concentration (the intraday component is where the effect lives; overnight is a drag), the −16bp next-month reversal, and the successor requirement recorded in the closure note (**gate-reachability simulation at registration** — the placebo magnitude clause must be checked against the mechanical conditioning-drift floor before freezing). Any re-open is a **fresh pre-registered brief with its own K** — not a re-run, not a window/threshold nudge.
- **Feed/panel infra is in place:** cost-gated Databento pulls via `.claude/skills/databento-data/scripts/db_fetch.py` (daily-bar chunks estimate ≈ $0); yearly-chunk assembler [`assemble_panels.py`](../../lab/archive/harv_0_month_end_rebalance_es_2026-07/assemble_panels.py) → parquet panels (parents 2010-06→2026-07; micros 2019-05→2026-07). Reusable for any future ES question, subject to W1/W2.

## SESSION LOG

- **2026-08-09** — **MES ledger opened** ([`MES.md`](MES.md)) under instrument-lane SPEC — K-void re-screen; disposition on the child ledger. No ES cell change.
- **2026-07-12** — Ledger created (Q-HARV-0 Phase-0 §0.8 found ES.md ABSENT). Seeded W1/W2 + E1–E4 from the HARV-2026-001 study (closed AMBIGUOUS same day). No core/lock/allocation/dd_protection change; no live strategy on this instrument.
