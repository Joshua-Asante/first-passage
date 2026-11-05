# INSTRUMENT LEDGER — M6E

**Symbol:** CME Micro EUR/USD futures (M6E) · **Parent:** 6E (standard EUR/USD — **un-ledgered**) · **Asset class:** FX futures (micro)
**Contract facts:** CME Micro FX page, read 2026-11-04: "12,500 euros", "0.0001 USD per EUR", "$1.25 per contract" ([source](https://www.cmegroup.com/markets/microsuite/fx.html)). Owner: `core/instrument_specs.py`.
**Status:** **Research/discovery only — exports landed; fixed exploratory expression closed negative.** Not admitted to the builder. No candidate or live allocation; one external exploratory look recorded below.
**Last updated:** 2026-11-05

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
  - claim: "One fixed European-morning expression closed negative under its fixed cost/fill model. Independent code/evidence review found no blocking defect; no raw-data reproduction or builder acceptance is claimed."
    source: "#e3-fixed-european-morning-exploration"
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
- **2026-11-05** — External fixed-rule exploration recorded at K=1; no candidate submitted; 2025–2026 returns excluded. Independent Claude code/evidence review clean. See E3 and the lab owner for the scoped rejection, privacy boundary and limitations.

## E3: fixed European-morning exploration

Direct operator authorization, 2026-11-04: run one fixed rule with $6.60 round-trip costs, register data, preserve R2's reserved sample, do not optimize.

- [Frozen rules and execution plan](../../docs/superpowers/plans/2026-11-04-m6e-fixed-exploration.md).
- [Input registration](../../lab/analysis/fx/m6e_european_breakout_2026_11/registration.json): 18 M6E1! M15 exports hash-registered; exactly nine 2016–2024 files allowed for scoring. Continuous contract and adjustment/roll mapping remain unverified.
- [Authoritative K manifest](../../discovery_manifests/m6e_european_breakout_fixed_20261104.json). One declared exploratory look. This external expression must be reconciled in any subsequent R2 registration; the builder's separate card ledger alone cannot establish no prior exposure. No fabricated builder card is added.
- Sample: 2016-01-04 through 2024-12-31. All 2025–2026 returns remain outside this experiment, conservatively protecting R2 D9's final approximately 378 sessions. The earlier audit inspected structural coverage, not returns.
- Related prior: [R2 Asia-to-London dossier at dba5b94](https://github.com/Joshua-Asante/first-passage/blob/dba5b9424a74f77c9897192f5cd4ebc6280c8e4a/docs/briefs/dossiers/R2/r2-m6e-asialdn.md). Its Asia range differs from this one-hour range; neither is independent evidence for the other. The dossier reports no established mechanism/effect estimate. Its M6A DL-2 stop-geometry warning motivates the report-only geometry diagnostic here.
- Historical cost prior: [M6B ledger W4](M6B.md#standing-warnings-read-first) records M6E's earlier third-leg E-COST rejection. That is a prior on cost feasibility, not a result for this fixed expression; the original archived study was not re-run here.
- [Result and private-evidence references](../../lab/analysis/fx/m6e_european_breakout_2026_11/RESULTS.md): the lab owner records permitted counts and hashes; full performance evidence stays private. No candidate was submitted to validation. Claude code/evidence review found no blocking defect and supports the negative fixed-expression conclusion; direction/year splits were diagnostic. This is not raw-data reproduction or builder acceptance.

Contract units and costs, checked 2026-11-04: [CME FX product guide](https://www.cmegroup.com/markets/fx/fx-product-guide), EUR 12,500 contract and USD 0.0001/EUR tick = $1.25; [Tradeify fees](https://help.tradeify.co/en/articles/10468315-trading-commission-fees), $1.60 round trip.
