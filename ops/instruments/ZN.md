# INSTRUMENT LEDGER — ZN

**Symbol:** CBOT 10-Year U.S. Treasury Note futures (ZN; Globex, Databento `GLBX.MDP3`) · **Asset class:** rates / Treasury complex
**Status:** **Research venue only — no strategy, no allocation, no live exposure.** **Untradable at Tradeify** (US Treasuries excluded at the live firm).
**Last updated:** 2026-07-25

**Purpose:** single source of instrument-level truth (operational rule 10, [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). Created **2026-07-25**. **The DEAD list is the point** — this ledger exists mainly to stop a re-run.

## PROFILE (machine-readable)

```yaml
symbol: ZN
asset_class: rates-futures
family: []
venue_tradable: false
venue_note: "US Treasuries untradable at Tradeify - research-only."
k_bank_source: "../../discovery_manifests/"
cells:
  - mechanism: event-window-reversal
    verdict: DEAD
    date: 2026-07-20
    source: "../../docs/briefs/closures/H-ZNAUC-1-closure-screen-fail.md"
bars:
  - id: treasury-complex-tail-exhaustion
    source: "ZN.md#R1"
structure:
  - claim: "Post-auction dealer-hedging direction on ZN is real (confirms the Smales dealer-hedge-unwind mechanism, delta +1.01bp N=134) but the magnitude is 6-10x under the futures cost hurdle - mechanism-real-sub-cost is a more durable fact than a no-effect null."
    source: "#R2"
  - claim: "Tail-exhaustion across the directional Treasury complex - three structurally distinct directional constructs (ZN auction-drift, ZB opening-range breakout, ZF conditional event breakout) have died on three different instruments with zero survivors; a fourth requires reformulating the parent question, not a new instrument or window."
    source: "#R1"
```

---

## STANDING WARNINGS

- **W1 — quarterly mid-month roll, unadjusted `.c.0`** (same as ES/YM/ZB).
- **W2 — `ohlcv-1d` UTC-day bucketing → phantom weekend bars.** Drop settle-date weekday > 4.
- **W3 — venue wall.** Untradable at Tradeify.

## DURABLE FINDINGS

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **R1** | **TAIL-EXHAUSTION across the directional Treasury complex (INQHIORI §6).** Three structurally distinct directional constructs have died on three different instruments: ZN auction-day drift (cost-wall), ZB unconditional opening-range breakout (sign-reversed), ZF conditional event breakout (cost-law + power). Three distinct failure modes, zero survivors. **A fourth directional construct here should not be funded without reformulating the parent question** — not a new instrument, not a new window. Note this is INQHIORI §6 tail-exhaustion, **not** a formal domain-SNAG (that bar is ~17–22 candidates). | [`rejected_candidates.md`](../../docs/rejected_candidates.md) · [`ZB.md`](ZB.md) · [`ZF.md`](ZF.md) | **HIGH** (three independent closures). |
| **R2** | **Dealer-hedging direction is real; the magnitude is not tradable.** Post-auction δ = **1.01 bp/event** (10Y family, N=134, 0→15m) against a Req-5 hurdle of **6–10 bp** → FAIL by 6–10×; power marginal at realized N (t=1.61). Direction *confirms* Smales (dealer-hedge unwind) — mechanism real and sub-cost is a more durable fact than "no effect". | [`q_znauc_1_2026-07/RESULTS.md`](../../lab/archive/q_znauc_1_2026-07/RESULTS.md) | **HIGH** (own-cohort extraction, $0.00). |
| **R3** | **Third Tier-B/C event-drift seed to die at the Stage-2 cost-law**, after D5 and H-OD-1. Published event-drift effects that are real but an order of magnitude under the futures cost hurdle are now this programme's dominant null mode — which is why the cost-law pre-screen runs *before* any edge measurement. | [`H-ZNAUC-1 closure`](../../docs/briefs/closures/H-ZNAUC-1-closure-screen-fail.md) | **HIGH**. |

## DEAD / REJECTED (instrument-specific)

| Rejection | Discriminator (the test that killed it) | K | Source |
|---|---|---|---|
| `H-ZNAUC-1` / fork F-A — Treasury-auction dealer-hedging unwind | δ **1.01 bp/event** vs 6–10 bp hurdle → cost-wall FAIL 6–10×; t=1.61 | 0 | SCREEN-FAIL 2026-07-20 — [`closure`](../../docs/briefs/closures/H-ZNAUC-1-closure-screen-fail.md) |

> **Do not re-run F-A.** On 2026-07-23 a session began re-scraping the Smales full text before dedup caught that `H-ZNAUC-1` had already resolved the same question three days earlier via a $0.00 Databento own-cohort extraction. The scrape was aborted. **Check this ledger before sourcing on ZN.**

## ACTIVE / OPEN

Nothing active. ZN family K bank **0**.

## SESSION LOG

- **2026-07-25** — Ledger created (attention-efficiency audit). Seeded from the H-ZNAUC-1 closure plus the cross-instrument Treasury tail-exhaustion finding. No `core/`, lock, allocation, `dd_protection`, or Pine change.
