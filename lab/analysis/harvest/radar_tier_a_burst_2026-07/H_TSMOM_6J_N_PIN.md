# H-TSMOM-6J — N pin + Clause-N disposition

**Date:** 2026-07-16  
**Status:** `CLOSED — Clause-N FAIL` (Default-#1-compliant; no Stage-0, no `register_search`, no pull, no K)  
**Parent row:** [`CANDIDATE_ROWS.md`](CANDIDATE_ROWS.md) · Req-2 recovery [`CHEAP_RECOVERY_JPY.md`](CHEAP_RECOVERY_JPY.md)  
**Precedent:** [`H-TSMOM-1-ES-tsmom-scoping.md`](../../../docs/briefs/rnd-pipeline/H-TSMOM-1-ES-tsmom-scoping.md) P1=(c)

---

## Pin (operator "proceed 1–3" 2026-07-16)

Apply the **same ratified Default #1** that closed H-TSMOM-1 — no §8 override granted for a post-2010 / N=192 reading on this sibling either.

| Reading | OOS window | N (months) | δ/σ | Power `Φ(√N·δ/σ − 1.96)` | Screen |
|---|---|---|---|---|---|
| (a) Full post-2010 panel | 2010→≈2026 | 192 | 0.1415 | **0.50** | PASS at floor |
| **(c) Default #1 (PINNED)** | 2019-05-06→present | **≈86** | 0.1415 | **0.26** | **FAIL** |
| (c) + Demystifying-primary SR 0.54 | same | ≈86 | 0.1559 | 0.30 | **FAIL** |

Break-even N at δ/σ=0.1415 for power≥0.50 ≈ **192**. Demystifying-primary does not rescue N=86.

**Authority:** Campaign-defaults ADR 2026-07-11 Default #1 (temporal-not-instrument OOS); inheritance semantics forbid silent override. H-TSMOM-1 operator pin (c) is the standing class precedent for monthly TSMOM confirms.

---

## Disposition

- **Clause K:** PASS (K_eff=1, floor 0.65) — moot under Clause-N FAIL.  
- **Clause N:** **FAIL** under pinned (c).  
- **Campaign:** does **not** proceed to Stage-0 pre-reg / `register_search open` / any pull.  
- **K:** none consumed; **6J family bank stays 0**.  
- **Failure class:** screen-stage event-frequency/power (same as H-TSMOM-1) — **not** a Stage-6-confirm closure; does **not** feed harvest-intake §4 doctrine falsifier; does **not** feed radar Stage-2 cost-law falsifier (never reached Stage-2).  
- **Re-open bar:** new N-extending evidence **or** a stated §8 override of Default #1 with reason — not a re-argued δ.

---

## Sync targets (same session)

- [`CANDIDATE_ROWS.md`](CANDIDATE_ROWS.md) — H-TSMOM-6J → CLOSED Clause-N FAIL  
- [`STATE.md`](../../../STATE.md) radar line — N pin closed  
- [`docs/SESSIONS.md`](../../../docs/SESSIONS.md) — top entry  
