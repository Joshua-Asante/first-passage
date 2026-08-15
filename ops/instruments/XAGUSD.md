# INSTRUMENT LEDGER — XAGUSD

**Symbol:** XAGUSD (Silver spot) · **Tradable:** FXIFY / DXTrade (historical research surface) · **Asset class:** precious metal
**Canonical feed:** TV CSV export — Pepperstone (TV-CSV policy). Staging feeds TV-verified before they gate anything.
**Status:** **NO LIVE STRATEGY.** Guardian-family direction REJECTED (Q-CORR-1). Guardian Silver v1.0 override attempt **CLOSED NOT ADMITTED 2026-07-01**. Not in `firm_rules.py` `_BASE_RISK` (4 keys only).
**Last updated:** 2026-07-16

**Purpose:** Single source of instrument-level truth (operational rule 10, [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). **Created 2026-07-16** under a scoped ADR §5 override (operator GO after coverage inventory — see ADR Addendum 2026-07-16). Seeded from existing registry + lab closures; not a live R&D session on silver. Canonical path: `ops/instruments/XAGUSD.md`.

**Ownership boundary (operational rules 5/7):** instrument findings + concept status + anti-SNAG only. Links out — never restates locked params / risk %.

## PROFILE (machine-readable)

```yaml
symbol: XAGUSD
asset_class: precious-metal-spot
family: []
venue_tradable: false
venue_note: "FXIFY/DXTrade CFD venue closed 2026-07-10; no live venue for this instrument at present."
k_bank_source: "../../discovery_manifests/"
cells:
  - mechanism: trend-following
    verdict: DEAD
    date: 2026-07-01
    source: "../../docs/rejected_candidates.md"
structure:
  - claim: "Silver amplifies H1 (2020-2023) co-drawdown under decompounded MC when inserted as a 5th Guardian-family leg — the 2020-2021 Silver cohort is net-negative; compounded 2022-26 can look Pareto-clean at low risk but that flatters the hard half."
    source: "#F3"
```

---

## STANDING WARNINGS (read first)

- **W1 — Direction is rejected at the Guardian-family bar.** Re-proposal requires **new mechanism evidence**, not new params / wider sweep / longer panel ([`docs/rejected_candidates.md`](../../docs/rejected_candidates.md)).
- **W2 — Operator override did not clear the mechanism bar.** Silver v1.0 BE-off admission (2026-06-11) was explicitly judgment-only and **conditional** on a §9 H1-counterbalance leg that never materialized → CLOSED NOT ADMITTED 2026-07-01.
- **W3 — Do not launder Silver into XAUUSD R&D.** Gold CGB / USOIL-RGC coordination historically referenced Silver; silver status is owned **here**.

---

## DURABLE FINDINGS (instrument characterization)

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **F1** | **Guardian v5.5-parameter port to Silver fails the portfolio bar.** Q-CORR-1.1: DD 11.52% > 8.0%; WR 11.34% below band. Parent Q-CORR-1 closed on SNAG-budget exhaustion. | Registry + Q-CORR-1 closure (evicted brief; retrieve via git history cited in registry) | **HIGH** |
| **F2** | **Surviving belt (portfolio-construction, not a Silver edge):** instrument-level correlation is not a reliable proxy for strategy-level correlation (NAS100/DJ30 decorrelation despite tight instrument corr). Independent of the Silver rejection. | Registry “Surviving belt finding” | **HIGH** (portfolio belt) |
| **F3** | **Silver amplifies H1 (2020–2023) co-drawdown under decompounded MC** when inserted as a 5th Guardian-family leg — 2020–2021 Silver cohort net-negative; H1 bust rises sharply vs 4-strat baseline. Compounded 2022–26 can look Pareto-clean at low risk — that flattery does not survive the hard half. | [`lab/analysis/legacy/silver_regime_2026-06-10/RESULTS.md`](../../lab/analysis/legacy/silver_regime_2026-06-10/RESULTS.md) | **HIGH** (MC characterization) |
| **F4** | **No counterbalance leg ever cleared** for the Silver v1.0 override path (5th-leg target 0/24; chop-native 0/9). Override condition unmet → NOT ADMITTED. | Registry override note; `chop_native_leg_*`; counterbalance labs | **HIGH** |

---

## ACTIVE CONCEPTS

| Concept | Status | Notes |
|---|---|---|
| *(none)* | — | No live silver concept. Pattern research must clear the new-mechanism bar before intake. |

---

## DEAD / REJECTED (instrument-specific)

| # | Rejection | Class | Discriminator | Source |
|---|---|---|---|---|
| **D1** | **Guardian-family strategy on XAGUSD** (v5.5 port + parameter-freedom track) | SNAG-budget exhaustion / edge-failure | Q-CORR-1 closed 2026-05-14; v5.5 port falsified (DD/WR); WFO withdrawn | [`docs/rejected_candidates.md`](../../docs/rejected_candidates.md) |
| **D2** | **Guardian Silver v1.0** (BE-off fair-weather, operator override 2026-06-11) | NOT ADMITTED (override condition failed) | §9 H1-counterbalance never materialized; CLOSED 2026-07-01 | Registry + [`docs/ltm/briefs/2026-06-11-guardian-silver-v1-admission-override.md`](../../docs/ltm/briefs/2026-06-11-guardian-silver-v1-admission-override.md); labs `silver_*`, `guardian_silver_be_*` |

---

## ANTI-SNAG LEDGER

**Guardian-family × XAGUSD:** D1 consumes the family null. **Silver v1.0 (D2)** was an override attempt that never entered the live book — treat re-opens as needing **new mechanism evidence** (same bar as D1), not a revive of BE-off / 0.15% risk.

---

## SESSION LOG

- **2026-07-16** — Ledger created under ADR §5 scoped override (operator GO; inventory A+B). Seeded F1–F4, D1–D2 from registry + silver labs. Cross-refs updated on [`XAUUSD.md`](XAUUSD.md). No core/lock/allocation/Pine change.
