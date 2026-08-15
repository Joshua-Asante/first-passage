# INSTRUMENT LEDGER — MJY

**Symbol:** CME Micro JPY/USD futures (MJY; quotes USD per JPY, reciprocal of spot USDJPY) · **TV:** `CME_MINI:MJY1!` · **Asset class:** FX futures (micro)
**Contract:** ¥1,250,000 · tick 0.000001 = **$1.25** (coarser than 6J's $6.25-on-10× — ≈2.6 USDJPY pips vs 6J's ≈1.3) · settlement copied directly from 6J
**Status:** **RETIRED as execution and replay venue** (2026-07-05, Aegis→6J transfer test v0.1 finding). Retained only as a possible *execution unit* via Bulenox's micro/standard mixing (1 standard ≡ 10 micro for limits) — and only if a future DOM sanity check at intended size passes (prototype WORKFLOW STEP 2, never run).
**Last updated:** 2026-07-21

**Purpose:** single source of instrument-level truth (operational rule 10, [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). Created 2026-07-05 to record the retirement verdict so no future session re-runs MJY panels as evidence.

## PROFILE (machine-readable)

```yaml
symbol: MJY
asset_class: fx-futures
family: [6J]
venue_tradable: false
venue_note: "Tradeify offers no micro JPY futures under any name - Currencies Product Group lists 6E/M6E/6B/6J/6A/M6A/6C/6S only, no MJY/M6J - research-only."
k_bank_source: "../../discovery_manifests/"
cells:
  - mechanism: venue-transfer
    verdict: DEAD
    date: 2026-07-05
    source: "#M1"
structure:
  - claim: "MJY is volume-starved at Aegis-relevant size - 120-lot intended sizing vs ~730 contracts/day ADV means the v0.1 replay's fills could not exist; the panel is evidence of venue rejection only, not of anything else."
    source: "#M2"
```

---

## DURABLE FINDINGS

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **M1** | **MJY retired as execution venue.** v0.1 replay (MJY1!, 2025-03→2026-06, n=42): as-run **PF 0.481**, net −$17,591, friction **$604/trade = 0.47R** at 120-lot sizing. Cap 120 binding on 37/42 trades. | v0.1 MJY CSV 2026-07-05 (Downloads; not landed — retirement evidence, not a panel of record) | **HIGH** |
| **M2** | **MJY 15m bars are volume-starved → fill fiction at size.** Missing 15m bars drift order fills **30–60 minutes**; intended 120 lots vs **~730 contracts/day ADV** (OI ~1.8K) means the replay's fills could not exist. **The MJY1! panel is evidence of venue rejection ONLY** — treating it as evidence of anything else is a forbidden move (handoff §5.4). | v0.1 replay fill-timestamp analysis, parent session 2026-07-05 | **HIGH** |
| **M3** | **History too shallow for the canonical 4yr replay.** MJY listed window doesn't cover 2022; deep panels run on 6J1! (full multi-year 15m history, deep book). | contract facts, v0.3 Pine header (hash-pinned `30d35028…`) | **HIGH** |
| **M4** | **GLBX micro-JPY symbology = MJY (not M6J).** Q-BOOKFIT-1 Phase-1b: `M6J.FUT` 422 on GLBX.MDP3 (does not exist); `MJY.FUT` resolves live. MJY is a 1/10 6J clone, same JPY/USD quote convention, no inversion. **Does not overturn M1/M2** — symbology discharge only; retirement-as-execution/replay venue stands. | [`Q-BOOKFIT-1 closure`](../../docs/briefs/closures/Q-BOOKFIT-1-closure-resolved.md); [`.claude/skills/databento-data/reference/proxy-discipline.md`](../../.claude/skills/databento-data/reference/proxy-discipline.md) | **HIGH** |

## DEAD / REJECTED

| Rejection | Discriminator | Source |
|---|---|---|
| MJY as Aegis replay/panel venue | PF 0.481 as-run; fills fictional (M2) | 2026-07-05 v0.1 |
| MJY as standalone execution venue at Aegis size | 120 lots vs ~730 ADV; 0.47R friction/trade | 2026-07-05 v0.1 |

## ACTIVE / OPEN

- **Execution-unit question (dormant):** the v0.3 Pine header's older guidance "execute live in micro units" predates the M1/M2 retirement — any micro-unit execution plan must first pass a DOM sanity check at intended size (WORKFLOW STEP 2, never run) and would still replay/validate on 6J. Do not resurrect MJY panels for validation.
- **Symbology (discharged 2026-07-20):** when a brief needs the CME micro JPY product name, use **MJY** (M4). Do not invent `M6J`.

## SESSION LOG

- **2026-07-21** — Doc-skew repair: recorded M4 (Q-BOOKFIT-1 Phase-1b symbology discharge). Status still RETIRED as execution/replay venue (M1/M2 unchanged).
- **2026-07-05** — Ledger created (CC-HANDOFF-AEGIS-6J §2.7). Retirement verdict recorded from the v0.1 transfer-test replay; panel work moved to [`6J.md`](6J.md). No core/lock/allocation/dd_protection change.
