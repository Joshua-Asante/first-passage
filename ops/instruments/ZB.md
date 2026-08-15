# INSTRUMENT LEDGER — ZB

**Symbol:** CBOT 30-Year U.S. Treasury Bond futures (ZB; Globex, Databento `GLBX.MDP3`) · **Asset class:** rates / Treasury complex
**Status:** **Research venue only — no strategy, no allocation, no live exposure.** **Untradable at Tradeify** (US Treasuries excluded at the live firm, confirmed 2026-07-22), so any ZB result is research-only until a venue that permits it is in play.
**Last updated:** 2026-07-25

**Purpose:** single source of instrument-level truth (operational rule 10, [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). Created **2026-07-25** — the ORB-ZB-1 closure had no ledger home. **The DEAD list is the point.**

## PROFILE (machine-readable)

```yaml
symbol: ZB
asset_class: rates-futures
family: []
venue_tradable: false
venue_note: "US Treasuries untradable at Tradeify (confirmed 2026-07-22) — research-only."
k_bank_source: "../../discovery_manifests/"
cells:
  - mechanism: opening-range-breakout
    verdict: DEAD
    date: 2026-07-20
    source: "../../lab/archive/orb_zb_recon_2026-07/RESULTS.md"
bars:
  - id: treasury-complex-tail-exhaustion
    source: "ZN.md#R1"
structure:
  - claim: "ZB FADES its opening range — opening-range momentum is equity-index-specific and does not port to Treasuries (within-day placebo p=0.0010, sign-reversed)."
    source: "#B1"
  - claim: "Breadth cannot be bought by transplanting ORB to a risk-off instrument; the one cost-viable construct class is mechanistically the book's own instrument family."
    source: "#B2"
```

---

## STANDING WARNINGS

- **W1 — quarterly mid-month roll, unadjusted `.c.0`.** Same geometry as ES/ZN/YM; any window spanning a roll carries a phantom calendar-spread jump.
- **W2 — Databento `ohlcv-1d` UTC-day bucketing → phantom weekend bars.** Drop settle-date weekday > 4 before any trade-date offset work.
- **W3 — venue wall.** US Treasuries are **untradable at Tradeify**. A ZB edge cannot be deployed on the current live account regardless of statistical standing.

## DURABLE FINDINGS

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **B1** | **ZB FADES its opening range — opening-range momentum is equity-index-specific and does NOT port to Treasuries.** The within-day placebo returned **p=0.0010, sign-reversed**. This is a positive structural finding about the mechanism class, not merely a null. | [`orb_zb_recon_2026-07/RESULTS.md`](../../lab/archive/orb_zb_recon_2026-07/RESULTS.md) | **HIGH** (pre-registered placebo). |
| **B2** | **It tightens the portfolio vise rather than loosening it.** The probe existed to find a cost-viable breakout *counter-cyclical* to the index book. Its failure means the one cost-viable construct class this programme has is mechanistically the book's own instrument family — breadth cannot be bought by transplanting ORB to a risk-off instrument. | [`ORB-ZB-1 scoping`](../../docs/briefs/rnd-pipeline/ORB-ZB-1-risk-off-decorrelated-breakout-scoping.md) | **HIGH** (design consequence). |

## DEAD / REJECTED (instrument-specific)

| Rejection | Discriminator (the test that killed it) | K | Source |
|---|---|---|---|
| `ORB-ZB-1` — opening-range breakout transplanted to ZB | **Negative gross edge in every window** (full −0.048 R); cost-law −0.20× headline / −10.66× at 0-slip; net PF 0.59; placebo **p=0.0010 sign-reversed** | 0 | FALSIFIED 2026-07-20 — [`RESULTS.md`](../../lab/archive/orb_zb_recon_2026-07/RESULTS.md) · [`rejected_candidates.md`](../../docs/rejected_candidates.md) |

## ACTIVE / OPEN

Nothing active. ZB family K bank **0**. Any new ZB directional construct is gated by the Treasury-complex tail-exhaustion finding (see [`ZN.md`](ZN.md) R1) — a fourth directional construct in this complex needs the parent question **reformulated**, not a new instrument or window.

## SESSION LOG

- **2026-07-25** — Ledger created (attention-efficiency audit). Seeded from the ORB-ZB-1 closure. No `core/`, lock, allocation, `dd_protection`, or Pine change.
