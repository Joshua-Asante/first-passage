# MSL-C3 Stage-0 — M2K L3 one-shot + WSTRUCT sequencing + W4

**Status:** `STAGE-0 PASS` · **PROCEED 2026-08-13** (plan approval = operator election) · **$0 · K=0**
**Card:** MSL-C3 · instrument **M2K** · mechanism **open** (stories authored at Stage-1, not here)
**Parent:** [MSL charter](../../../docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md) step 1 pins · [slate §MSL-C3](../../../docs/briefs/2026-08-12-msl-first-slate.md) · [program plan §6](../../../docs/briefs/2026-08-12-msl-program-plan.md) · C2 handoff [closure Iterate](../../../docs/briefs/closures/MSL-C2-closure-falsified.md)

This record discharges the slate’s Stage-0 gate: edge-cohort §2-C L3 (“M2K's one-shot bank rule + WSTRUCT sequencing + W4 cost-dry-run gate stand”) and [`M2K.md`](../../../ops/instruments/M2K.md) (“must be sequenced against WSTRUCT-M2K-1 by the operator first”). It is **not** Stage-1.

---

## §0 — Rule 0 reads (verified this session @ `7847ca9`)

| Source | Anchor (`git log -1`) | What it grounds |
|---|---|---|
| [`ops/instruments/M2K.md`](../../../ops/instruments/M2K.md) PROFILE `bars:` / W4 / M4 / SESSION LOG 2026-07-30 | `c0d20bd` | RAISED BAR already on ledger; W4 no local panel; M4 one-shot premise SUPERSEDED; “sequence vs WSTRUCT first” still in session log |
| [`WSTRUCT-M2K-1`](../../../docs/briefs/rnd-pipeline/WSTRUCT-M2K-1-weekly-structure-component-confirm-scoping.md) Status line | `91137fb` | `SUPERSEDED-ON-COST 2026-07-28` — no PREREG, no K, no pull, no GO |
| [`wstruct_cost_geometry` RESULTS §4](lab/analysis/c1/wstruct_cost_geometry_2026-07-28/RESULTS.md) | `92abdbb` | No E1-legal deployable RT count clears 4×; reopen = asymmetric-payoff with own warrant |
| [Edge-cohort ADR §2-C L3](../../../docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md) | `c0d20bd` | One-shot + WSTRUCT sequencing + W4 **stand** (interpret, do not rewrite) |
| [K-bank ADR §2](../../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md) | `2ef7405` | `K_eff = K_intrinsic`; family bank = disclosure, not gate |
| [MSL first slate §MSL-C3](../../../docs/briefs/2026-08-12-msl-first-slate.md) | `cc26ba3` | Stage-0 = record one-shot spend + WSTRUCT ruling **before** electing the card |
| [MSL-C2 closure Iterate](../../../docs/briefs/closures/MSL-C2-closure-falsified.md) | `1178553` | STOP C2 G0; slot → P3.2 C3 Stage-0 |

Local check: no `M2K*` / `RTY*` under `core/data/bar_data/`; `SHA256SUMS` carries neither symbol.

---

## Three Stage-0 answers

### 1. One-shot (post K-bank ADR)

Family-bank “spendable exactly once” is **void** — [`ADR 2026-08-04`](../../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md) §2; M2K.md **M4 SUPERSEDED**. Surviving content: C3 is **not a wide search**. Any later G0 declares `K_intrinsic=1`; slate already freezes 2–3 mechanism stories with **≤1 scored** (each additional scored story = +1 `K_intrinsic`). Disclosure: `K_banked(M2K)=0`. WSTRUCT spent **zero** K.

### 2. WSTRUCT sequencing

[`WSTRUCT-M2K-1`](../../../docs/briefs/rnd-pipeline/WSTRUCT-M2K-1-weekly-structure-component-confirm-scoping.md) is `SUPERSEDED-ON-COST 2026-07-28` ([RESULTS §4](lab/analysis/c1/wstruct_cost_geometry_2026-07-28/RESULTS.md)): no deployable E1-legal expression clears 4×; **no PREREG, no K, no pull**. Reopen bar = **asymmetric-payoff with its own warrant** — not RT / day-set / instrument retune. MSL-C3 is session-scale; slate default route **①** (SLR MR-at-level) — **not** that reopen. WSTRUCT does **not** occupy a first-use K slot. Operator sequencing against WSTRUCT (M2K.md session log) **discharges here**.

### 3. W4 cost-dry-run gate

No M2K/RTY panel locally. Stage-0 **does not pull**. Stage-1 $0 arithmetic does not need bars (C2 pattern). Any later IS path-PnL or Databento pull requires a **fresh W4 dry-run** — the WSTRUCT 1m characterization cache ends **2024-01-01** and does not cover a 2024–2025 IS window. MSL default remains TV exports + existing panels.

---

## What Stage-0 does **not** license

- Mechanism stories / story priority order (Stage-1)
- Route election beyond noting slate default ① (Stage-1 records the pick)
- Door-check verdicts / `instrument_profiles.py` adjudication (Stage-1)
- G0 freeze / B4 / Pine / TV / Cap / CONFIRM peek
- Databento estimate or pull
- Occupancy re-litigation (M2K never occupied; B8 is MYM/MNQ)
- Amending edge-cohort L3 prose (this file *interprets* L3 under 08-04)

---

## Operator sign

| Field | Value |
|---|---|
| Election | **PROCEED** |
| Date | **2026-08-13** |
| Grounds | Plan approval = operator election (HOLD declined) |
| Discharges | “sequenced against WSTRUCT-M2K-1 by the operator first” ([`M2K.md`](../../../ops/instruments/M2K.md) SESSION LOG 2026-07-30) |

**HOLD** (not taken): reserve M2K for a future asymmetric WSTRUCT reopen; defer C3; slot → C1.

---

## Next

**Stage-1** (charter steps 2–4): author 2–3 mechanism stories frozen before data contact; elect ≤1 by delete/flip survival in frozen priority order; declare route (default ①; temporal-selectivity only by explicit operator election outside the paused dense-1m lane); answer RAISED BAR M1; run `msl_preflight` evidence tables; adjudicate three kill limbs at M2K RT **$2.82** / 4× **$11.28** / **2.26** RTY pts/trade; Clause-N power honesty; $200/$750 at declared design point. No G0 until Board **B4**.

**Artifacts not authored this turn:** `card.yaml` · `STAGE1.md` · `PREREG_G0.md`.
