# Systematic Trading Lifecycle — Canonical Map

**Path:** `docs/governance/systematic-trading-lifecycle.md`
**Status:** ADOPTED with the three-loop binding ADR (`docs/adr/2026-06-12-three-loop-methodology-binding.md`, ACCEPTED 2026-07-06 — see that ADR's Ratification Note), 2026-06-12
**Scope:** Descriptive doctrine. Names the end-to-end value stream, binds each stage to its governing loop and industry-standard vocabulary. Does not authorize builds; build plans cite this map, not vice versa.

**Current execution posture (2026-07-10):** stages describe the lifecycle, not
an assertion that every stage is live. Manual trading is retired, the CFD/DXTrade
venue is idle, and the prior Copygram/TradersConnect and
TradersPost/Tradovate descriptions are obsolete. The identified futures rail is
TradingView alert → CrossTrade → NinjaTrader 8 via Rithmic; it is not yet built
or authorized for live execution.

---

## The five stages

| # | Internal name | Industry name | Office | Governing loop | Key artifacts |
|---|---|---|---|---|---|
| 1 | Strategy R&D (concept → analysis → codification → validation) | **Alpha research** / research pipeline; validation sub-stage = **model validation** | Front (quant research) | OUTER (INQHIORI), funded by STRATEGIC | ConceptRecords, Pre-Q briefs, kill records, rejected-candidates registry, validation-harness dispositions (CPCV/DSR/PBO/permutation) |
| 2 | Pine strategy & indicator construction, backtesting | **Strategy engineering / productionization**; TV = simulation environment | Front (quant dev) | OUTER (lock decisions) / INNER (build mechanics) | Pine v6 sources, lock decision briefs, parity/fidelity gates, backtest-to-live divergence reconciliation |
| 3 | Approved signal → execution rail → venue fill (**currently uncommissioned**; identified futures design: TV alert → CrossTrade → NinjaTrader 8/Rithmic) | **Order routing & execution (OMS/EMS)**; monitoring = **trade surveillance** | Front (execution) | INNER (OODA) — the perpetual forward test of stage-1 hypotheses once commissioned | Rail configuration, pre-trade risk controls, fill/copy-integrity alerts, operator GO/NO-GO |
| 4 | Telemetry & reporting | **Middle office**: real-time risk monitoring, P&L reporting, **TCA** (ECR program) | Middle | Sensor for all three loops; severity ladder routes each signal to its consuming loop | Three-point reconciler (signal/master/slave), severity ladder w/ loop-routing column, weekly ECR/TCA report, quarterly audit pack |
| 5 | Logging & analysis (strategic / operational / tactical) | **Post-trade analytics & performance attribution** + **reconciliation** (back office); strategic tier = **research feedback loop** | Back + research loop | OUTER (findings) → STRATEGIC (kill/scale verdicts) | live-execution-journal reviews, programme audits, anti-portfolio theses, lessons registries |

Assembly name: **systematic trading lifecycle** (strategy lifecycle management). Stages 1–3 front office, 4 middle, 5 back + feedback — the standard institutional division, converged on from first principles.

## The two bridges (what makes it a loop, not a pipeline)

- **Graduation bridge (stage 2 → 3):** lock → production. Crossing requires: INQHIORI disposition ADVANCE, portfolio-MC admission at portfolio level (never standalone gates — settled doctrine, 2026-03-18), allocation lock, dd_protection integration.
- **Feedback bridge (stage 5 → 1):** telemetry-derived findings (ECR anomalies, copy-integrity patterns, anti-portfolio theses, kill-record durable findings) re-seed Identify/Notice. Anomalies spawn Pre-Qs **through the kill-test ladder**, never directly into briefs.

## Loop overlay

```
STRATEGIC (The Algorithm, quarterly/audit)  — funds stage 1, owns kill/scale verdicts from stage 5
   └── OUTER (INQHIORI, per-investigation)  — runs stages 1–2, consumes stage-4 weekly reports, writes stage-5 dispositions
        └── INNER (OODA, real-time/daily)   — runs stage 3, consumes stage-4 alert tiers
```

Stage 4 is the membrane: one telemetry store, three consumption cadences (alert tiers → INNER; ECR/TCA weekly → OUTER; incident-rate/leakage trends quarterly → STRATEGIC). A stage-4 gap blinds Observe; an INQHIORI loop with a blind Observe phase cannot close regardless of stage-1 quality.

## Strategic-loop instrumentation (reviewed at programme audit)

Sweep runs per supervised hour; fraction of candidates killed pre-brief; add-back rate (per the three-loop binding ADR D4, `docs/adr/2026-06-12-three-loop-methodology-binding.md`); parallel-track incidents (target 0); copy-integrity incidents + time-to-detection; ECR trend vs. the −8%/−23% reconciliation baseline; pipeline commissioning status (GBPUSD-VBR shakeout DONE).

## Pointers

- `docs/adr/2026-06-12-three-loop-methodology-binding.md` — three-loop methodology binding (canonical decision; this map is its D5)
- INQHIORI canon mirror `docs/methodology/inqhiori-canon.md` — carries the binding as §14 (Notion surface RETIRED 2026-06-12 per `docs/adr/2026-06-12-notion-surface-retirement.md`; legacy page `34ddc0b53c1181479d7bdecc61f47078` frozen read-only pending migration)
- Two-loops-on-two-clocks doctrine (R&D automation session, 2026-06-05) — superseded-by-extension: this map adds the Strategic tier and stage names; the two-clock content is unchanged within it.
