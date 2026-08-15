**Theme:** harvest
# Radar Tier-A burst — first execution instance (2026-07-16)

**Status:** **ACTIVE** — first burst EXECUTED; proceed items 1–3 complete (`H-TSMOM-6J` Clause-N FAIL; carry Table-1 moments recovered / timing still UNSCREENABLE; month-end no new brief). Cadence on-demand; not an archiveable close.  
**Design authority:** [`docs/superpowers/specs/2026-07-16-mechanism-sourcing-strategy-design.md`](../../../docs/superpowers/specs/2026-07-16-mechanism-sourcing-strategy-design.md) §6  
**Doctrine:** [`docs/methodology/strategy_harvest.md`](../../../docs/methodology/strategy_harvest.md) §2  
**Seed axis:** `H-TSMOM-1` (Moskowitz–Ooi–Pedersen 2012 TSMOM / ES)  
**Scope:** Tier-A classes only — TSMOM siblings, carry, term-structure/basis. Not a Q1–Q6 re-run.

## What this burst is / is not

| Is | Is not |
|---|---|
| First radar turn after the sourcing-layer landing | A repeat of Q-KBUDGET-HARVEST-1 |
| Citation-seeded + paper digests + Fig.2 cheap recovery | `register_search open` / pulls / K |
| Candidate **staging** for the existing intake screen | Operator ratification of a screen PASS |

## Artifacts

| File | Role |
|---|---|
| [`SOURCES_LOG.md`](SOURCES_LOG.md) | Papers / channels examined + dispositions |
| [`FIG2_DIGITIZATION.md`](FIG2_DIGITIZATION.md) | Moskowitz Fig.2 vector digitize (equity-validated; FX labels ratified) |
| [`CHEAP_RECOVERY_JPY.md`](CHEAP_RECOVERY_JPY.md) | Demystifying label map → `H-TSMOM-6J` Req-2 clear |
| [`H_TSMOM_6J_N_PIN.md`](H_TSMOM_6J_N_PIN.md) | **Default #1 pin → Clause-N FAIL** |
| [`CARRY_DELTA_EXTRACTION.md`](CARRY_DELTA_EXTRACTION.md) | Koijen Table 1 moments; timing δ still UNSCREENABLE |
| [`MONTH_END_ITEM3_DISPOSITION.md`](MONTH_END_ITEM3_DISPOSITION.md) | No new HARV successor brief (Q-HARV-1 §R already DECLINED) |
| [`CANDIDATE_ROWS.md`](CANDIDATE_ROWS.md) | Staged §C rows + dispositions |
| [`candidates.json`](candidates.json) | Machine-readable rows (may lag prose — prefer CANDIDATE_ROWS) |
| [`digitize_fig2.py`](digitize_fig2.py) | Repro script (PDF fetched locally; not required on CI) |

## Headline outcome

- **`H-TSMOM-6J` CLOSED Clause-N FAIL** under Default #1 (N≈86, power≈0.26). Req-2 had cleared (δ/σ 0.1415); N pin closed the campaign without pull/K.
- **Carry:** Table 1 Japan/Euro/WTI **moments recovered**; **carry-timing Req-2 still UNSCREENABLE** (class SR transplant refused).
- **Month-end (item 3):** no new brief — Q-HARV-1 already DECLINED at §R; A4 real DROP/DEFER still owes operator pull.
- **Cost-law sniff (Req 5):** monthly TSMOM / carry class effects clear at class magnitude; Tier-C graveyard-watch unchanged.

## Remaining recoveries (cheap, zero pull)

1. ~~Confirm Fig.2 white-bar ↔ JPY~~ — **DONE**.  
2. ~~Pin N on `H-TSMOM-6J`~~ — **DONE (FAIL)**.  
3. ~~Attempt Koijen per-contract carry δ~~ — **DONE (moments only; timing still UNSCREENABLE)**.  
4. Optional: named timing-δ source (AQR library / replication) or δ-extraction probe Pre-Q.  
5. Operator: A4 real footprint pass when `ohlcv-1d` panel staged.
