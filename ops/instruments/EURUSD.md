# INSTRUMENT LEDGER — EURUSD

**Symbol:** EURUSD · **Tradable:** FXIFY / DXTrade (historical research surface) · **Asset class:** FX major
**Canonical feed:** TV CSV export — Pepperstone (TV-CSV policy). Staging feeds TV-verified before they gate anything.
**Status:** **NO LIVE STRATEGY.** Two registry directions closed/shelved; one active pattern-enumeration harness (Phases 1–3 LOCKED; Phase 4+ not started). Not in the live book.
**Last updated:** 2026-07-16

**Purpose:** Single source of instrument-level truth (operational rule 10, [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). **Created 2026-07-16** under a scoped ADR §5 override (operator GO after coverage inventory — see ADR Addendum 2026-07-16). Seeded from registry + lab cards. Canonical path: `ops/instruments/EURUSD.md`.

**Ownership boundary (operational rules 5/7):** instrument findings + concept status + anti-SNAG only. Links out — never restates locked params / risk %.

## PROFILE (machine-readable)

```yaml
symbol: EURUSD
asset_class: fx-major
family: []
venue_tradable: false
venue_note: "FXIFY/DXTrade CFD venue closed 2026-07-10; no live venue for this instrument at present."
k_bank_source: "../../discovery_manifests/"
cells:
  - mechanism: turn-of-month
    verdict: AMBIGUOUS-PARKED
    date: 2026-06-10
    source: "../../docs/rejected_candidates.md"
  - mechanism: event-window-reversal
    verdict: DEAD
    date: 2026-06-22
    source: "../../docs/rejected_candidates.md"
structure:
  - claim: "The London 16:00 WM/Reuters fix carries a genuine ~2bp gross post-fix reversal (reproducing the source paper's magnitude) but FXIFY retail all-in cost (~0.8 pip) exceeds the 0.277-pip best-of-grid break-even — the edge is real but not retail-tradeable."
    source: "#F1"
```

---

## STANDING WARNINGS (read first)

- **W1 — Cost law binds retail FX on this instrument.** Fix-reversal cost pre-screen (D2) and USDCAD precedent both say thin mean-reversion edges die at FXIFY all-in spreads. Re-tunes of hold/stop grids do not clear venue/cost kills.
- **W2 — Custodian probe never completed formal falsifier.** D1 is SHELVED (soft) — manual TV underperformed; Dukascopy fetch hung. Re-proposal needs a **completed** mechanism probe or new mechanism evidence.
- **W3 — Pattern enum is harness infrastructure, not an edge claim.** Phases 1–3 lock the reality-check apparatus; enumeration / MTC / OOS / verdict are not started.

---

## DURABLE FINDINGS (instrument characterization)

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **F1** | **London 16:00 WM/Reuters fix fade has a real gross post-fix reversal (~2 bps class) but is untradeable at retail cost.** Best-of-grid break-even ≈ **0.277 pip ≪ FXIFY ~0.8 pip all-in**; net R &lt; 0 in every (hold × stop) cell at ≥0.4 pip; robust to spread (gross ≤0.055R even at zero cost). | [`lab/archive/fixrev_costscreen_2026-06-22/`](../../lab/archive/fixrev_costscreen_2026-06-22/); CARD FAIL-COST | **HIGH** (n=1550 fix-days, canonical Pepperstone 5m) |
| **F2** | **Codification boundary (surviving, not a EURUSD edge):** `compose_from_hint` only covers intraday-technical / single-instrument / long-only archetypes — calendar-flow / cross-instrument / two-sided concepts need primitive-library extension. Surfaced by custodian intake. | Registry custodian entry; `custodian_eurusd` probe | **HIGH** (capability finding) |
| **F3** | **Reality-check harness Phases 1–3 LOCKED** for EURUSD pattern enumeration (`avg_block_length=21`, feature_space + K=450). Phase 4 enumeration not started. | [`lab/analysis/legacy/eurusd_pattern_enum/README.md`](../../lab/analysis/legacy/eurusd_pattern_enum/README.md); ADR 2026-05-22 reality-check harness | **HIGH** (infra lock) |

---

## ACTIVE CONCEPTS

| Concept | id / path | Status | Notes |
|---|---|---|---|
| Mechanical pattern enumeration | `lab/analysis/legacy/eurusd_pattern_enum/` | **ACTIVE — harness Phases 1–3 LOCKED; Phase 4+ not started** | Not an admitted edge. Resume only under locked harness phases. |

---

## DEAD / REJECTED (instrument-specific)

| # | Rejection | Class | Discriminator | Source |
|---|---|---|---|---|
| **D1** | **Custodian-family month-end equity-hedging flow on EURUSD** | SHELVED (soft) — incomplete probe | Intake ADMIT 7/7 but regression never completed (Dukascopy hung); manual TV underperformed. Not a completed formal falsifier. | [`docs/rejected_candidates.md`](../../docs/rejected_candidates.md); [`lab/analysis/custodian_eurusd/CARD.md`](../../lab/analysis/custodian_eurusd/CARD.md) |
| **D2** | **FX intraday fixing-reversal (session MR) on EURUSD** | venue/cost-constraint | Cost pre-screen FAIL (F1). Distinct from D1 (daily fix microstructure vs month-end custodial flow). | Registry; [`lab/analysis/fixrev_costscreen_2026-06-22/CARD.md`](../../lab/analysis/fixrev_costscreen_2026-06-22/CARD.md) |

**Re-proposal bar (D1):** completed mechanism probe **or** new mechanism evidence — not Pine param tweaks / different fix-window / wider sweep.  
**Re-proposal bar (D2):** materially better-than-retail fix execution evidence **or** genuinely different mechanism — not hold/stop grid re-tune.

---

## ANTI-SNAG LEDGER

- **Custodian / calendar-flow family:** D1 shelved — soft; budget accounting = incomplete probe (0 formal null slots if graded as non-run).
- **Fixing-reversal / session-MR family:** D2 is a cost-geometry kill (pre-screen, not full Pre-Q) — re-tunes return DUPLICATE.
- **Pattern-enumeration family:** open harness only; no edge null recorded.

---

## SESSION LOG

- **2026-07-16** — Ledger created under ADR §5 scoped override (operator GO; inventory A+B). Seeded F1–F3, D1–D2, active pattern-enum row. No core/lock/allocation/Pine change.
