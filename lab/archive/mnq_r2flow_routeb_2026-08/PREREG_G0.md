# Q-R2FLOW-1 — Route B G0 charter (FROZEN; G2 FALSIFIED — STOP)

**Status:** `FROZEN G0 · G2 COMPLETE 2026-08-08 — FALSIFIED` — schema×window×catalogue frozen. **Empty candidates → STOP catalogue.** Cap seat not claimed. CONFIRM reserved, unread.
**Date:** 2026-08-08
**Parent brief:** [`docs/briefs/Q-R2FLOW-1-signed-minute-flow-route-b-scoping.md`](lab/archive/../../../docs/briefs/Q-R2FLOW-1-signed-minute-flow-route-b-scoping.md)
**Route:** Avenue A **Route B** ([`ADR`](lab/archive/../../../docs/adr/2026-08-05-avenue-a-generate-confirm-route.md) `Accepted`)
**Screen:** EM0–EM5 + MNQDTL D1/D2 class attestation — applied **before** this freeze (§2.0a)
**SPEC S6:** [`admission_s6.json`](admission_s6.json) + [`ADMISSION_S6_LOG.md`](ADMISSION_S6_LOG.md) — **ADMIT** 2026-08-08 (`catalogue_k=1`, floor 0.650, power 0.9988 ≥ 0.50).
**Cost so far:** **$0.0000**. EXPLORATION = OFCHAN cache reuse. Explore GO paid 2026-08-08 (cache reuse only).
**`K_intrinsic = 1`**. Cap 1.0 → DSR floor **0.650**.
**Confirm-budget M = 1** — **moot** (no candidates).
**Cap seat:** **not claimed**.
**Confirm $ budget:** **USD 50.00** — unused (CONFIRM unread).

G2 artifacts: [`RESULTS_g2.md`](RESULTS_g2.md) / [`RESULTS_g2.json`](RESULTS_g2.json).

---

## Amendment log

- **2026-08-08 — Explore GO RATIFIED (operator) + G2 COMPLETE → `FALSIFIED` (empty candidates).** Operator explore GO under MNQDTL **R2** (cache reuse only; no new pull). Runner `run_flow_g2.py` + `flow_lib.py` scored C1 on EXPLORATION only. n_retained **48,360** / eligible **48,360** = **100%**. ρ **−0.000701** · CI95 **[−0.014612, +0.013510]** includes 0 → **FALSIFIED**. Candidate list **[]**. CONFIRM untouched. Cap seat not claimed. G3 disposition: **STOP** this catalogue (re-proposal = new G0 / new mechanism; no post-hoc retune).
- **2026-08-08 — G0 FROZEN.** Named successor after Q-R2AGRUN-1 non-promotable close. Explore GO unpaid.

---

## §0 — Rule-0 / cheap falsifier (parent-side, 2026-08-08)

| Check | Result |
|---|---|
| OFCHAN EXPLORATION cache | 155 `*.tbbo.dbn.zst` present |
| Mid + sides on `tbbo` | OK |
| Sampling grid | Clock minutes — **no** EXPLORATION-fit threshold |
| S6 | ADMIT |

**Why not a retune:** feature = **net signed aggressor size** (buy_sz − sell_sz contracts) per completed RTH clock minute — not resting size (OFCHAN), not imbalance **ratio** in volume buckets (R2VBUCK), not run **length** (R2AGRUN).

---

## §1 — Windows (non-overlapping; CONFIRM = fresh holdout)

| Window | ISO bounds (`--end` exclusive) | Role |
|---|---|---|
| **CONFIRM** | **2025-09-01 → 2026-02-06** | Fresh holdout (same shift as R2VBUCK/AGRUN). Unread. |
| **EXPLORATION** | **2026-02-06 → 2026-08-06** | Stage-G only. OFCHAN cache reuse. |

- Symbol: `MNQ.v.0` continuous · Schema: **`tbbo` only** · No NQ/ES cross-book

---

## §2 — Catalogue (size 1 → `K_intrinsic = 1`)

### Cell C1 — clock-minute net signed aggressor size → 60 s mid return

| Element | Frozen definition |
|---|---|
| Sampling grid | CME equity-index **RTH** Mon–Fri **09:30–15:59 ET**; one sample per completed clock minute whose start is in RTH. Drop holiday / early-close sessions lacking a full RTH (same EXCLUDED_SESSION_DATES as AGRUN/OFCHAN EXPLORATION). |
| Feature `A` | Over prints with `action=T` and `ts ∈ [t_minute, t_minute+60s)` and `side ∈ {B,A}`: `A = Σ size·(+1 if B, −1 if A)`. Minutes with zero such prints are **ineligible** (not imputed). |
| Target | Mid return over **[t_end, t_end+60s)`** where `t_end = t_minute+60s`: `r = (mid_{t_end+60s−} − mid_{t_end}) / mid_{t_end}` using last TBBO quote ≤ each endpoint. Horizon **60 s ≥ 5 s**. |
| Unit | One retained `(A, r)` per eligible completed minute. |
| Statistic | Pearson `ρ(A, r)`; session-block bootstrap 95% CI, **10,000** reps, seed **20260808**; within-session r-shuffle placebo **1,000** reps, same seed. |
| Sign / CI | CI excludes 0 |
| Placebo | \|ρ\| > placebo \|·\| p95 |
| Halves | Older/newer EXPLORATION session-date halves; sign disagree → AMBIGUOUS-HOLD |
| Magnitude | AMBIGUOUS-HOLD if \|ρ\| **< 0.02** |
| VOID-COVERAGE | retained / eligible **< 90%** |
| VOID-POWER | retained **n < 2,000** |

**C9 clearance:** tape aggressor **size flow**, not resting ToB size imbalance.

**Forbidden inside the cell:** flicker filter; resting ToB size; volume-bucket imbalance ratio; aggressor-run length; ORB / ICT / MNQSEL restart clocks; CONFIRM peek; D1/D2 μ inside G2.

---

## §3 — Promotion rule (EXPLORATION only)

Promote iff: not VOID-POWER/COVERAGE; CI excludes 0; \|ρ\| > placebo p95; halves agree; \|ρ\| ≥ 0.02. Else empty / AMBIGUOUS-HOLD. Not an edge or harvest PASS.

---

## §4 — Confirm / Cap / Stage-C

- M = 1 · Cap reservation after G3 (≥1 candidate) before C0 · CONFIRM bounds frozen · confirm `$ ≤ 50` · no CONFIRM peek before C0.

---

## §5 — EM / MNQDTL attestation (K=1)

`P U U D D D` + D1/D2 class True — EM1/EM2 U until tradeable stop/R. Not SHAPE-CLEAR.

---

## §6 — Explore path (after operator GO)

1. Explore GO: cache reuse only.
2. G2 EXPLORATION-only → candidates.
3. Empty → STOP; ≥1 → Cap → C0 (separate packet).

---

## §7 — Economic honesty (not a promotion gate)

\|ρ\| ≥ 0.02 is association floor only; converting to points uses EXPLORATION σ(r) disclosed at G2 — do not amend limbs post-hoc.
