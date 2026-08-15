# Q-CAPRES-2 — Reserve a fresh MNQ Cap seat for one ORB-tied Route A cell

**Status:** RESOLVED — Cap-reservation GO signed; Cap-spend GO signed (CapFLOW PREREG). CapFLOW Cap-spend **`FALSIFIED` 2026-08-14** (Cap held). See [`Q-CAPFLOW-1 closure`](closures/Q-CAPFLOW-1-closure-falsified.md).
**Authored:** 2026-08-08
**Authors:** Joshua + Cursor; absolute-path plan item 3
**Parent:** Cap spent via [`Q-CAPA-1`](closures/Q-CAPA-1-closure-resolved.md) · MNQDTL R2 Cap-reservation requirement · Avenue A Route A
**Loop:** Inquire — Cap **reservation** only (does not spend Cap; does not run the Cap cell)
**Spend:** $0 · K=0 until Cap-spend GO · no pull

---

## §0 — Rule 0 reads (verified 2026-08-08)

| Path | What it grounds |
|---|---|
| [`Q-CAPA-1` closure](closures/Q-CAPA-1-closure-resolved.md) | Cap seat **SPENT** on N14 forward L1 `A` tripwire |
| [`Cap companion ADR`](../adr/2026-08-06-capa-tripwire-pfcusum-companion-registration.md) | Tripwire docs-only; **not** entry filter |
| [`MNQDTL-1`](../spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md) | Fresh Cap reservation before Cap-style K=1 cell |
| [`MNQ.md`](../../ops/instruments/MNQ.md) C11 / N16 / F2 GUARD | No N14 `A` as ORB gate |
| [`Avenue A ADR`](../adr/2026-08-05-avenue-a-generate-confirm-route.md) | Route A survivor-tied default |

---

## §1 — Why Cap is needed

Absolute-path item 3: one **ORB-MNQ-1–tied** Route A Cap cell (K_intrinsic=1, DSR floor 0.650)
measuring whether **net signed aggressor size in the OR window ending at trigger** associates with
**realized R of that ORB trade** — tape flow → existing trade object's path R; **not** 60s mid;
**not** resting ToB size; **not** N14 `A` as a gate (C11).

Without a fresh Cap reservation, that cell cannot mark Cap spent / claim Cap arithmetic.

---

## §2 — Reservation terms (frozen intent; Cap-spend GO separate)

| Term | Value |
|---|---|
| Survivor | **ORB-MNQ-1** (PARKED lifecycle unchanged; Route A tie only) |
| Cell (named, not scored here) | OR-window net signed aggressor → ORB trade R — see [`PREREG`](../../lab/analysis/c1/mnq_capflow_orb_r_2026-08/PREREG.md) |
| K | `K_intrinsic=1` on Cap mark-spent if accept |
| Confirm $ | ≤ $50 estimate-gated before any pull |
| Explicit bars | **C11:** no use of N14 L1 `A` as ORB entry filter/gate; no ORB Tradeify unpark; no Striker redeploy |

---

## §3 — Question

Should the operator **reserve** a fresh MNQ Cap seat for the named CapFLOW cell under the terms
in §2, restoring Cap arithmetic for one Route A discovery spend?

---

## §4 — Falsifiable hypothesis / gate

**Hypothesis H-CAPRES-2:** Operator Cap-reservation GO is issued against §2 terms before any
CapFLOW path score.

**Falsifier:** If Cap-spend / CapFLOW explore proceeds without a dated reservation GO citing this
packet → process FAIL (governance), not a market falsifier.

**Accept if:** Operator signs Cap-reservation GO → CapFLOW PREREG may proceed to Cap-spend GO.
**Reject if:** Operator declines → CapFLOW stays unpaid; Cap remains spent (no second seat).

---

## §5 — Forbidden moves

- Scoring CapFLOW / claiming Cap before reservation GO.
- Converting any CapFLOW positive into an ORB entry filter (C11 / F2).
- Unparking ORB on Tradeify; R1 foreclosed.

---

## §6 — Gate criteria

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | Operator Cap-reservation GO signed | INTEGRATE — CapFLOW Cap-spend path open |
| `FALSIFIED` | Operator declines | STOP reservation; CapFLOW unpaid |
| `AMBIGUOUS-HOLD` | Deferred | dated hold; no CapFLOW score |

**This session:** Cap-reservation GO signed 2026-08-08 / JA → CapFLOW Cap-spend path open (separate Cap-spend GO still required).

---

## §10 — Audit hooks

```bash
test -f docs/briefs/Q-CAPRES-2-mnq-cap-seat-reservation.md
test -f lab/analysis/c1/mnq_capflow_orb_r_2026-08/PREREG.md
rg "C11|Cap-reservation|unpaid" docs/briefs/Q-CAPRES-2-mnq-cap-seat-reservation.md
```
