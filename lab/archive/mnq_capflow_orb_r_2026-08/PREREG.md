# Q-CAPFLOW-1 — Cap cell PREREG: OR-window net signed aggressor → ORB trade R

**Status:** FROZEN — Cap-reservation GO SIGNED + **Cap-spend GO SIGNED** 2026-08-08 / JA (plan-execute). Estimate-before-pull mandatory; single score only.
**Date:** 2026-08-08
**Parent reservation:** [Q-CAPRES-2](../../../../docs/briefs/Q-CAPRES-2-mnq-cap-seat-reservation.md) (RESOLVED)
**Survivor:** ORB-MNQ-1 (Route A tie only; lifecycle PARKED unchanged)
**Cost so far:** $0.00 · K_intrinsic=1 **if** Cap marked spent on accept
**Confirm $ budget:** USD **50.00** (estimate before pull; refuse if estimate > $50)

---

## §0 — Rule-0 / bars

| Source | Pin |
|---|---|
| Cap companion ADR / C11 | N14 L1 A **not** an ORB entry filter |
| N14 / Cap tripwire | Distinct spent cell — do not retune |
| ORB events | Parent mnq_orb_flow_substrate_2026-08-05 triggers only |
| Avenue A Route A | Survivor-tied; Cap arithmetic |

---

## §1 — Question

At each ORB-MNQ-1 **trigger**, does **net signed aggressor size** summed over prints in the
**opening-range window ending at trigger** associate with **realized R of that ORB trade**
with CI excluding 0 and beating placebo — enough to mark a **fresh** Cap seat spent?

---

## §2 — Frozen construct (binds the single Cap-spend run)

| # | Element | Frozen value |
|---|---|---|
| S1 | Schema / symbol | 	bbo, MNQ.v.0 — OFCHAN day-file reuse preferred; estimate before pull |
| S2 | Events | Exact ORB-MNQ-1 trigger set from parent vents.parquet / unmodified uild_events.py |
| S3 | Feature A | Over ction=T, side∈{B,A} prints with 	s in **[OR_start, t_trigger)**: A = Σ size·(+1 B, −1 A). Tape flow — **not** resting ToB |
| S3b | OR_start | ORB engine OR open for that trigger (first OR bar open) |
| S4 | Target | **Realized R** from unmodified orb_backtest keyed by trigger — CapFLOW **intentionally joins outcomes** (breaks N14 FM-1 for this cell only) |
| S5 | Statistic | **Pearson ρ(A, R) primary**; mean-split Δ disclosure twin; session-block bootstrap 95% CI **10,000** reps seed **20260808**; within-session shuffle placebo **1,000** |
| S6 | Coverage / power | VOID-COVERAGE if usable trigger fraction < 90%; VOID-POWER if covered n < 30 |
| S7 | Magnitude | AMBIGUOUS-HOLD if |ρ| < **0.02** |
| S8 | Halves | Sign disagree → AMBIGUOUS-HOLD; Cap not spent |
| S9 | Outputs | n, coverage, ρ/Δ, CI, placebo, halves, cap_spent. **No** ORB gate proposal |

**C11 / F2:** a positive does **not** license an ORB entry filter or Tradeify unpark.

---

## §3 — Cap arithmetic

- Route A, survivor-tied.
- Cap mark-spent only on W5-style RESOLVED after Cap-reservation + Cap-spend GO.
- Floor 0.650 / headroom 0.350 at Cap 1.0.

---

## §4 — Forbidden moves

- Score before Cap-reservation GO **and** Cap-spend GO.
- Pull without estimate or above $50 ceiling.
- Resting L1 A / N14 retune as this cell's feature.
- Converting a positive into ORB gate (C11).
- Horizon / event-set sweep after data.
- Pine / rail / Striker redeploy.

---

## §5 — Verdict gates (Cap disposition)

| Condition | Verdict | Cap |
|---|---|---|
| VOID-POWER / VOID-COVERAGE | typed VOID | held |
| CI includes 0 or fails placebo | FALSIFIED | held |
| Clear except magnitude/halves | AMBIGUOUS-HOLD | not spent |
| All clear | RESOLVED | **mark spent**; companion/monitor research only |

---

## §6 — Protocol order

1. Shape freeze (done).
2. Cap-reservation GO (Q-CAPRES-2) — **SIGNED**.
3. Cap-spend GO + estimate — **SIGNED** this amendment; estimate next.
4. Tests green → reuse/pull → **one** run → RESULTS.
5. Closure + board (orchestrator).

## Amendment log

- **2026-08-08 — shape frozen unpaid** (absolute-path plan). No score.
- **2026-08-08 — Cap-spend amendment:** Pearson ρ primary; |ρ|≥0.02; OR_start = engine OR open; R joined from unmodified orb_backtest; Cap-reservation + Cap-spend GO signed; $≤50 estimate-before-pull.
