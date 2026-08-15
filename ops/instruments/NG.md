# INSTRUMENT LEDGER — NG

**Symbol:** NYMEX Henry Hub Natural Gas futures (NG; Globex, Databento `GLBX.MDP3`) · **Asset class:** energy
**Status:** **Research venue only — no strategy, no allocation, no live exposure.**
**Last updated:** 2026-07-25

**Purpose:** single source of instrument-level truth (operational rule 10, [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). Created **2026-07-25**. **The DEAD list is the point.**

## PROFILE (machine-readable)

```yaml
symbol: NG
asset_class: energy-futures
family: []
venue_tradable: true
k_bank_source: "../../discovery_manifests/"
cost_hurdle:
  value: 29.6
  units: "bp/event"
  basis: "NG-EIA-1 cost hurdle (announcement-bracket construct)"
  source: "#G3"
cells:
  - mechanism: event-window-reversal
    verdict: DEAD
    date: 2026-07-21
    source: "../../lab/archive/ng_eia_recon_2026-07/RESULTS.md"
structure:
  - claim: "NG's EIA release genuinely moves the instrument (faithfulness anchor ~50.7bp) but produces no exploitable post-announcement drift - mechanism-present, edge-absent, not a mis-dating artifact."
    source: "#G2"
```

---

## STANDING WARNINGS

- **W1 — MONTHLY roll (not quarterly).** NG rolls monthly, so roll-spanning windows are far more frequent than in the equity-index or Treasury complexes. Check roll dates against every window.
- **W2 — `ohlcv-1d` UTC-day bucketing → phantom weekend bars.** Drop settle-date weekday > 4.
- **W3 — the PRE-leg of an announcement bracket is surprise-conditional.** Constructing an EIA (or any announcement) trade as pre+post smuggles in information unavailable ex ante. The NG probe was **corrected pre-run** to post-only after re-reading the workflow's own executioner finding — the same trap F-B (CL/EIA) hit. Any announcement construct here is **post-only** unless a surprise estimate is itself pre-registered and available in real time.

## DURABLE FINDINGS

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **G1** | **No tradable post-EIA drift on NG.** δ = **+8.30 bp**, not distinguishable from zero (δ/σ **0.052** against a **0.109** power floor) and ~**3.6× under** the **29.6 bp** cost hurdle. Per-year sign alternates — noise, not decay. | [`ng_eia_recon_2026-07/RESULTS.md`](../../lab/archive/ng_eia_recon_2026-07/RESULTS.md) | **HIGH** (pre-registered, post-only). |
| **G2** | **The null is real, not a mis-dating artifact.** The faithfulness anchor came back clean at **50.7 bp** — the event set is correctly dated and the release *does* move the instrument; there is simply no exploitable post-announcement drift at the cost hurdle. Mechanism-present / edge-absent is what makes this closure durable rather than re-testable. | [`RESULTS.md`](../../lab/archive/ng_eia_recon_2026-07/RESULTS.md) | **HIGH**. |
| **G3** | **Cost hurdle, pinned: ≈29.6 bp/event.** An order of magnitude above the index complex — any NG construct must clear a much larger bar, which foreclosed this seed before power was even the binding constraint. | [`NG-EIA-1 scoping`](../../docs/briefs/rnd-pipeline/NG-EIA-1-announcement-bracket-premium-scoping.md) | **HIGH**. |

## DEAD / REJECTED (instrument-specific)

| Rejection | Discriminator (the test that killed it) | K | Source |
|---|---|---|---|
| `NG-EIA-1` — short NG across the EIA storage-report post-announcement window | δ **+8.30 bp** vs **29.6 bp** hurdle (~3.6× under); δ/σ 0.052 vs 0.109 power floor; faithfulness anchor clean, so the null is real | 0 | FALSIFIED 2026-07-21 — [`RESULTS.md`](../../lab/archive/ng_eia_recon_2026-07/RESULTS.md) · [`rejected_candidates.md`](../../docs/rejected_candidates.md) |

## ACTIVE / OPEN

Nothing active. NG family K bank **0**.

## SESSION LOG

- **2026-07-25** — Ledger created (attention-efficiency audit). Seeded from the NG-EIA-1 closure. Recorded W3 (post-only announcement construction) as a standing warning. No `core/`, lock, allocation, `dd_protection`, or Pine change.
