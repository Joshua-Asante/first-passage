# INSTRUMENT LEDGER — M6E

**Symbol:** CME Micro EUR/USD futures (M6E) · **Parent:** 6E (standard EUR/USD — **un-ledgered**) · **Asset class:** FX futures (micro)
**Contract facts:** CME Micro FX page, read 2026-11-04: "12,500 euros", "0.0001 USD per EUR", "$1.25 per contract" ([source](https://www.cmegroup.com/markets/microsuite/fx.html)). Owner: `core/instrument_specs.py`.
**Status:** **Research/discovery only — export landed; no mechanism cell, no candidate.** Not admitted to the builder. Not a live leg; no allocation; no K spend here.
**Last updated:** 2026-11-04

**Purpose:** single source of instrument-level truth (Rule 27). Created **2026-11-04** on first touch, in the export landing ([generation note §9.3](../../docs/notes/2026-11-01-generation-phase-strengthening-DRAFT.md#93-d8-decided-by-claude-under-joshuas-delegation)).

## PROFILE (machine-readable)

```yaml
symbol: M6E
asset_class: fx-futures
family: []
venue_tradable: true
venue_note: "Offered at Tradeify, Bulenox and MFFU; BluSky's markets page lists 6E but not M6E (generation note §8.3, correction 2026-11-04). Commissions live in core/firm_rules.py comments; COMMISSION_BINDINGS classes M6E unavailable until a firm_symbol_row exists."
k_bank_source: "../../discovery_manifests/"
structure:
  - claim: "Third-leg Stage-1 outcome E-COST, cited from M6B.md W4; the record itself was not read at ledger creation."
    source: "#E2"
```

---

## STANDING WARNINGS (read first)

- **W1 — Parent 6E is un-ledgered.** M6E inherits **no** bars via `family`.
- **W2 — Costs bind.** R2 was held partly because 0.7–1.0 tick of slip consumes the M6E pre-fix cell ([generation note §11](../../docs/notes/2026-11-01-generation-phase-strengthening-DRAFT.md#11-updates-2026-11-04)).

---

## DURABLE FINDINGS

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **E1** | **TV export:** 18 pages, 409,380 unique bars, 2009-03-23T19:00Z → 2026-11-02T21:45Z, validator PASS. | [landing record](../../docs/notes/2026-11-01-generation-phase-strengthening-DRAFT.md#11-updates-2026-11-04) | **HIGH** |
| **E2** | **Third-leg Stage-1 `E-COST`:** killed on its own cost-tax against the power floor. Read the record before relying on it. | [`M6B.md`](M6B.md) W4 | **MEDIUM** (cited, record not read) |

## ACTIVE / OPEN

- Future intake: `python scripts/instrument_profiles.py cell M6E <mechanism-id>`.
- Builder admission is a separate decision.
- **Parent 6E remains un-ledgered** (W1).

## SESSION LOG

- **2026-11-04** — **Ledger created; TV export landed.** `M6E1!` BAR EXPORT v0.2 at 15m. `PRICE_COL_BY_INSTRUMENT` entry and `INSTRUMENT_SPECS` row added with the CME quote; `COMMISSION_BINDINGS` classes it `unavailable`. No K, no candidate.
