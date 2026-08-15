# INSTRUMENT LEDGER — ZF

**Symbol:** CBOT 5-Year U.S. Treasury Note futures (ZF; Globex, Databento `GLBX.MDP3`) · **Asset class:** rates / Treasury complex
**Status:** **Research venue only — no strategy, no allocation, no live exposure.** **Untradable at Tradeify.**
**Last updated:** 2026-07-25

**Purpose:** single source of instrument-level truth (operational rule 10, [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). Created **2026-07-25**. **The DEAD list is the point.**

## PROFILE (machine-readable)

```yaml
symbol: ZF
asset_class: rates-futures
family: []
venue_tradable: false
venue_note: "US Treasuries untradable at Tradeify - research-only."
k_bank_source: "../../discovery_manifests/"
cells:
  - mechanism: opening-range-breakout
    verdict: DEAD
    date: 2026-07-21
    source: "../../lab/archive/rates_ev_zf_recon_2026-07/RESULTS.md"
bars:
  - id: treasury-complex-tail-exhaustion
    source: "ZN.md#R1"
structure:
  - claim: "ZF's event-day range concentrates 17.6:1 vs ZB's unconditional 4.3:1 - CPI/NFP-conditioning genuinely concentrates range where cost is payable, but the edge itself is absent (cost-law 1.15x vs 4.0x required, power 0.30 vs 0.50 floor)."
    source: "#F1"
```

---

## STANDING WARNINGS

- **W1 — quarterly mid-month roll, unadjusted `.c.0`.** **W2 — `ohlcv-1d` UTC-day bucketing → phantom weekend bars.** **W3 — venue wall:** untradable at Tradeify.
- **W4 — event calendars must be SOURCED, not inferred.** The ZF probe pulled the CPI/NFP calendar live from `bls.gov`'s eight per-year schedule pages rather than a first-Friday heuristic, and that independently confirmed a 2025 government-shutdown reference-month gap. A heuristic calendar would have mis-dated the event set. Note `bls.gov` **403s WebFetch** — browse it.

## DURABLE FINDINGS

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **F1** | **Two supporting theses VALIDATED even though the edge died.** Instrument choice: ZF event-day range/RT is **17.6:1** (vs ZB's unconditional 4.3:1) — conditioning on releases genuinely concentrates range where the cost hurdle is payable. Decorrelation: **ρ=0.28** (zero-padded) against the index book. Both are reusable design facts for any future event-conditioned construct, on any instrument. | [`rates_ev_zf_recon_2026-07/RESULTS.md`](../../lab/archive/rates_ev_zf_recon_2026-07/RESULTS.md) | **HIGH** (measured). |
| **F2** | **The edge itself is absent.** Cost-law KILL (**1.15× vs 4.0×** required, t=+1.45 n.s.) **and** power FAIL (**0.30 vs 0.50** floor). Validated selection plus validated decorrelation still yields nothing tradable — the clearest available demonstration that supporting-thesis validation does not imply an edge. | [`RESULTS.md`](../../lab/archive/rates_ev_zf_recon_2026-07/RESULTS.md) | **HIGH** (pre-registered). |

## DEAD / REJECTED (instrument-specific)

| Rejection | Discriminator (the test that killed it) | K | Source |
|---|---|---|---|
| `RATES-EV-ZF-1` — CPI/NFP-conditioned opening-range breakout on ZF | Cost-law **1.15× vs 4.0×** (t=+1.45 n.s.) **and** power **0.30 vs 0.50** floor | 0 | FALSIFIED 2026-07-21 — [`RESULTS.md`](../../lab/archive/rates_ev_zf_recon_2026-07/RESULTS.md) · [`rejected_candidates.md`](../../docs/rejected_candidates.md) |

## ACTIVE / OPEN

Nothing active. ZF family K bank **0**. Gated by the Treasury-complex tail-exhaustion finding ([`ZN.md`](ZN.md) R1).

**Explicitly NOT barred by it** (named so a future session does not over-read the exhaustion): mean-reversion / fade at native intraday resolution, and a conditional **fixed-hold** drift construct (no breakout, no stop). Neither has been run on any Treasury instrument. Both still require their own mechanism case and pre-registration.

## SESSION LOG

- **2026-07-25** — Ledger created (attention-efficiency audit). Seeded from the RATES-EV-ZF-1 closure. Recorded W4 (sourced-not-heuristic event calendars) as a standing warning. No `core/`, lock, allocation, `dd_protection`, or Pine change.
