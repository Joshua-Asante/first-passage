# H-ZNAUC-1 — CLOSURE: `SCREEN-FAIL (cost-wall)` (ZN post-auction δ ≈ 1 bp vs ~6–10 bp hurdle)

**Closed:** 2026-07-20 (same session as scoping + GO; own-cohort δ-extraction authorized by operator, resolving the earlier `NEEDS_CONTEXT`)
**Parent brief:** [`../rnd-pipeline/H-ZNAUC-1-zn-auction-unwind-scoping.md`](../rnd-pipeline/H-ZNAUC-1-zn-auction-unwind-scoping.md) (now `CLOSED — SCREEN-FAIL`)
**Run artifacts:** [`lab/archive/q_znauc_1_2026-07/`](../../../lab/archive/q_znauc_1_2026-07/) — `extract_delta.py`, `delta_results.json`, `primary_15m_events.csv`, `auctions_is.json`
**Data:** ZN.c.0 ohlcv-1m, GLBX.MDP3, 2010-06-06→2018-12-31 (Databento, **est + billed $0.00**, 2.19M bars cached); auction dates from fiscaldata.treasury.gov (free). K consumed **0**; ZN family bank stays **0**; no `register_search open`; no manifest opened.

## Verdict (§3 gate asserted against measured numbers)

**`SCREEN-FAIL (cost-wall)`.** The pre-committed primary cohort clears power marginally but misses the Requirement-5 cost-law by **6–10×** — the same Stage-2 wall that closed D5 and H-OD-1.

| Cohort (pre-committed) | N | δ (bp/event) | σ (bp) | δ/σ | t | Req-5 vs 6bp / 10bp |
|---|---|---|---|---|---|---|
| **PRIMARY 10Y-family, 0→15m** | 134 | **1.01** | 7.29 | 0.139 | 1.61 | **FAIL / FAIL** |
| PRIMARY 10Y-family, 0→30m | 132 | 0.28 | 8.33 | 0.034 | 0.39 | FAIL |
| PRIMARY 10Y-family, 0→60m | 133 | 1.45 | 9.72 | 0.149 | 1.72 | FAIL |
| SECONDARY all-coupon, 0→15m | 715 | 0.39 | 7.35 | 0.053 | 1.41 | FAIL |
| SECONDARY all-coupon, 0→60m | 707 | 0.83 | 10.25 | 0.081 | 2.15 | FAIL |

- **Req-5 cost-law (binding kill):** ZN RT cost ≈ 1.5 bp single-RT (1 tick = 1/64 point = $15.625 ≈ 1.25 bp at the in-era median price 126.4, + commission) → 4× hurdle **6 bp**; conservative two-RT ≈ 2.5 bp → **10 bp**. Measured δ = **1.01 bp** ⇒ **6–10× under** the hurdle at every window and both cohorts.
- **Req-4 power (also fails at realized N):** the "δ/σ ≥ 0.122" threshold was calibrated at N≈259; at the realized **N=134** the break-even for power 0.50 rises to ≈0.170, above the measured 0.139 (t=1.61, not significant at p<0.05). Even taken at face value the margin is razor-thin. The cost-wall is decisive regardless.
- **Direction confirms Smales (2021):** the sign is positive (prices drift up post-auction, consistent with dealer short-hedge unwind) — the mechanism is *real in direction*, just far too small to trade net of ZN microstructure cost. The bid-to-cover-conditional risk flagged in scoping did not even need adjudication: the *unconditional* δ is already sub-hurdle.

## Disposition

- **F-A CLOSED at the screen** — third Tier-B/C futures event-drift seed to confirm a mechanism yet die at the Stage-2 cost-law (**D5, H-OD-1, H-ZNAUC-1**). No pull beyond the $0.00 IS bars; no K; ZN bank 0.
- **F-C (carry timing-δ, 6J/6E/CL) steps up** per the fork priority order (F-A → F-C → F-B) and the scoping §3 route. **F-C requires its own operator nod** — it consumes **1 family-K** (unlike F-A's no-K probe), which the 2026-07-20 GO explicitly did **not** bundle. Awaiting that decision.
- **Q-BOOKFIT-1 composition finding stands, undisturbed:** F-A's book-*fit* (ρ 0.512, risk-N_eff Δ +0.787) was always "risk geometry fits," never "edge exists." This closure confirms the edge side fails — exactly the split the M-21 coordinates are careful to keep separate. No re-open of Q-BOOKFIT.
- **ZN instrument-ledger card (`ops/instruments/ZN.md`) deferred** — was a Stage-0 *prerequisite for SCREEN-PASS only*; not owed for a screen-stage close. Cost facts recorded here for re-use if ZN is ever re-proposed with new mechanism evidence.

- **Registry:** rejected_candidates.md — ### H-ZNAUC-1 post-auction dealer-hedging-unwind drift × ZN — SCREEN-FAIL (cost-wall)

## Lesson candidate

**(strengthens existing §2.1 doctrine, third instance)** Futures event-drift mechanisms (Tier-B auction-drift + Tier-C microstructure) are **structurally cost-walled**: D5 (11.06bp hurdle vs 2.97bp), H-OD-1 (5.05bp vs 1.5bp), now H-ZNAUC-1 (6–10bp vs 1.01bp) all **confirmed the mechanism direction** and all died on per-event δ being ~1/4 to ~1/10 of the round-trip cost. The pattern is now 3/3 — sourcing effort in these tiers should treat the cost-law as the *first* screen (it was here: the δ-extraction was cheap, $0.00), and the §2.1 "Tier-A fund-first" priority is empirically re-validated. Not a new registry entry — this is the exact pattern `strategy_harvest.md` §2.1 already encodes; logged as its third corroborating instance.

## §10 audit-hook discharge

- Databento pull est + billed **$0.00** (delta_results provenance) ✔ · cost dry-run ran before pull ✔
- Cohort + window + gates **pre-committed in `extract_delta.py` header before any δ was read** ✔ (no post-hoc window/threshold drift, Trap #12)
- `discovery_manifests/` delta 0 ✔ · no `register_search open` ✔ · ZN family bank stays 0 ✔
- Verdict robust to the cohort-definition ambiguity (primary 10Y-family AND secondary all-coupon both FAIL) ✔
