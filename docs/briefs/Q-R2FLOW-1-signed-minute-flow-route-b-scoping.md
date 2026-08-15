# Q-R2FLOW-1 — Does clock-minute net signed aggressor size predict 60 s mid returns on MNQ (Route B)?

**Status:** `CLOSED — Stage-G FALSIFIED` — empty candidates; STOP this G0 catalogue (2026-08-08)
**Authored:** 2026-08-08
**Authors:** Joshua + Cursor; Rule-0 parent-side; SPEC S6 ADMIT logged
**Parent question:** MNQDTL-1 **R2** · `Q-R2AGRUN-1` closed non-promotable (`AMBIGUOUS-HOLD` magnitude) · `Q-R2VBUCK-1` STOP · `Q-OFCHAN-1` STOP
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — Route B cell (clock-minute net signed aggressor size → 60 s mid) on EXPLORATION; Cap + confirm GO later for Stage-C
**Artifact path:** `docs/briefs/Q-R2FLOW-1-signed-minute-flow-route-b-scoping.md`
**Spend:** $0 · `K_intrinsic=1` · no Cap claim · no new pull (OFCHAN cache) · CONFIRM unread
**G2:** [`RESULTS_g2`](../../lab/archive/mnq_r2flow_routeb_2026-08/RESULTS_g2.md)

---

## §0 — Rule 0 reads (verified 2026-08-08 at HEAD `05e17b0`)

| Path | Anchor | What it grounds |
|---|---|---|
| [`core/firm_rules.py`](../../core/firm_rules.py) `Tradeify_Select_100K` | `45e3cea` | Incumbent eval geometry |
| [`docs/spec/2026-08-05-eval-mechanism-shape-screen.md`](../spec/2026-08-05-eval-mechanism-shape-screen.md) | `d93dafd` | EM0–EM5; G0 act |
| [`docs/spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md`](../spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md) | `27c7943` | MNQDTL R2 live |
| [`docs/adr/2026-08-05-avenue-a-generate-confirm-route.md`](../adr/2026-08-05-avenue-a-generate-confirm-route.md) | `b0427fd` | Route B Accepted |
| [`docs/methodology/avenue_a_generate_confirm.md`](../methodology/avenue_a_generate_confirm.md) | `b0427fd` | G0 checklist |
| [`lab/discovery/admission_schema.py`](../../lab/discovery/admission_schema.py) | `cc4142e` | S6 ADMIT/REFUSE |
| [`docs/briefs/closures/Q-R2AGRUN-1-closure-ambiguous-hold.md`](closures/Q-R2AGRUN-1-closure-ambiguous-hold.md) | this session | Non-promotable close; re-proposal bar |
| [`lab/archive/mnq_r2vbuck_routeb_2026-08/RESULTS_g2.md`](../../lab/archive/mnq_r2vbuck_routeb_2026-08/RESULTS_g2.md) | on main | Imbalance-ratio null |
| [`ops/instruments/MNQ.md`](../../ops/instruments/MNQ.md) C9 / DEAD | on main | Not resting ToB size |

**Gitignore pre-flight.** No Pine. No new Databento pull.

**Cheap falsifier:** OFCHAN cache present (155 days); mid + sides computable; clock-minute aggregation needs no EXPLORATION-fit threshold (grid is calendar). S6 ADMIT.

---

## §1 — Context & motivation

Three Route B OF catalogues on the same EXPLORATION cache:

| Q | Object | G2 |
|---|---|---|
| OFCHAN | Flicker-filtered resting L1 size @ clock minute | VOID-COVERAGE |
| R2VBUCK | Aggressor **imbalance ratio** in volume buckets | FALSIFIED (association null) |
| R2AGRUN | Aggressor-run **trade-count** | AMBIGUOUS-HOLD (magnitude); closed non-promotable |

**Symptom:** still no promotable Route B cell for **net signed aggressor flow** (absolute buy−sell contracts) on a coverage-safe clock grid — distinct from ratio, run length, and resting size.

---

## §2 — Prior art / lineage

- AGRUN closure STOP this run-length catalogue; successor = new mechanism.
- R2VBUCK killed **ratio** imbalance in volume buckets — not absolute signed size on clock minutes.
- OFCHAN killed denseness under flicker — this cell has **no flicker filter**.
- MNQSEL STOP remains a different universe (restart clocks).
- Cap spent; reservation before any C0.

---

## §3 — Question (Q-R2FLOW-1)

**Symptom-only:** ratio, run-length, and resting-size cells emptied; absolute signed aggressor flow on clock minutes is untested under Route B.

**Q-R2FLOW-1:** On `MNQ.v.0` RTH, does **net signed aggressor size** (buy_sz − sell_sz) inside each completed clock minute predict 60-second mid returns strongly enough to clear the frozen Stage-G promotion rule on the OFCHAN-cache EXPLORATION window, and — under Cap reservation + confirm GO — the fresh CONFIRM half at M=1?

---

## §4 — Falsifiable hypothesis (H-R2FLOW-1)

**Falsifier (binary):** the cell earns Route B candidate status only if Stage-G promotion clears on EXPLORATION under the frozen G0 limbs and Stage-C clears on the reserved CONFIRM window at M=1 under a later C0 PREREG (after Cap reservation); otherwise rejected / VOID / AMBIGUOUS without admission.

**H-R2FLOW-1:** On the frozen one-cell catalogue (clock-minute net signed aggressor size → 60 s mid, `tbbo`, `MNQ.v.0`), EXPLORATION promotion limbs clear; then under Cap + C0 + confirm GO the same limbs clear on CONFIRM **2025-09-01→2026-02-06** at M=1.

**Reject if:** Stage-G fails (CI/placebo/VOID/magnitude/halves) **or** Stage-C fails → STOP this catalogue; re-proposal = new G0 / new mechanism.

**Accept if:** G2 candidate ∧ Stage-C PASS → candidate recorded (still not harvest/deploy).

**Ambiguous-hold if:** VOID-* / halves disagree / \|ρ\| < 0.02.

---

## §5 — Forbidden moves

- Explore GO / G2 / confirm from this brief alone.
- New Databento pull for EXPLORATION.
- Flicker filter / resting ToB size (OFCHAN / C9).
- Volume-bucket **imbalance ratio** (R2VBUCK) or aggressor-run **length** (R2AGRUN).
- Fitting lookbacks from EXPLORATION.
- Cap claim at G0/G2; CONFIRM peek; catalogue growth; Pine / deployment / Striker redeploy.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | G2 promote ∧ Cap ∧ C0 ∧ Stage-C PASS | `INTEGRATE` — record candidate |
| `FALSIFIED` | Stage-G CI/placebo fail **or** Stage-C fail | `STOP` — new G0 / new mechanism |
| `AMBIGUOUS-HOLD` | VOID-* / halves / \|ρ\| < 0.02 | `ITERATE` — dated packet; no CONFIRM until resolved |

**Gate fired:** Stage-G CI includes 0 → `FALSIFIED` → **STOP** this catalogue. Re-proposal = new G0 / new mechanism.

---

## §7 — Execution plan

1. Operator **explore GO** (cache reuse).
2. G2 on EXPLORATION → candidate list.
3. Empty → STOP. ≥1 → Cap reservation → C0 → confirm GO (`$ ≤ 50`).

---

## §8 — EM attestation (re-derived K=1)

`P U U D D D` + D1/D2 class True — see G0 §5. Not SHAPE-CLEAR.

---

## §10 — Audit hooks

```bash
test -f lab/archive/mnq_r2flow_routeb_2026-08/PREREG_G0.md
rg -n "net signed|clock.minute|K_intrinsic = 1|2025-09-01" lab/archive/mnq_r2flow_routeb_2026-08/PREREG_G0.md
$env:PYTHONPATH='lab'; python -c "from discovery.admission_schema import load_admission, evaluate_admission; print(evaluate_admission(load_admission('lab/archive/mnq_r2flow_routeb_2026-08/admission_s6.json'), registered_k=1).decision)"
```
