# Q-MNQSEL-2 — Does perfect selection among dense RTH 1m bar opens clear EM1?

**Status:** `CLOSED — RESOLVED` — Phase 0 C4; S3 long 0.8584 / short 0.8566; construct ITERATE
([`closure`](../closures/Q-MNQSEL-2-closure-resolved.md) · [`RESULTS`](../../../lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/RESULTS.md))
**Authored:** 2026-08-08
**Authors:** Joshua + Cursor; absolute-path plan (items 1–2–3); Rule-0 + cheap falsifier OK
**Parent question:** `Q-MNQSEL-1` CLOSED-FALSIFIED (restart clocks) · MNQDTL R2 · absolute-path item 2
**Sub-questions opened:** none until Phase 0
**Loop:** Inquire-phase Pre-Q — Phase-0 selection ceiling on a **new** causal entry universe
**Artifact path:** `docs/briefs/rnd-pipeline/Q-MNQSEL-2-dense-1m-selection-ceiling-scoping.md`
**Spend:** $0 · K=0 · no manifest · Cap untouched ·
[`PREREG`](../../../lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/PREREG.md)

> **Cheap falsifier (parent-side, discharged):** RTH clocks on 2024-06-12 = **390**;
> G=10 clean-target R = **0.859**; stop R = **−1.141**; panel sha256
> `0d37054ee4375a6c60f7f2646a9b82547cae247c39a8c5dcbe209a149fedd7c5`
> ([`ADMISSION_FALSIFIER_LOG`](../../../lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/ADMISSION_FALSIFIER_LOG.md)).

---

## §0 — Rule 0 reads (verified 2026-08-08)

| Path | Anchor | What it grounds |
|---|---|---|
| [`core/firm_rules.py`](../../../core/firm_rules.py) `Tradeify_Select_100K` | `45e3cea` | RT cost → 1.41 pt |
| [`Q-MNQSEL-1` RESULTS](../../../lab/archive/mnq_selection_ceiling_2026-08/RESULTS.md) | on main | Restart clocks FALSIFIED; all-bars unbound |
| [`eval-mechanism-shape-screen`](../../spec/2026-08-05-eval-mechanism-shape-screen.md) | ratified | EM1 ≥0.40R |
| [`catalogue_k_wall` RESULTS](../../../lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md) | | Stop band 5–20 pt |
| [`MNQDTL-1`](../../spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md) | ratified | R2 live; Cap reservation separate |
| [`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) | | F2 GUARD; Cap spent |

**Gitignore pre-flight.** No Pine. No new Databento pull.

---

## §1 — Context & motivation

`Q-MNQSEL-1` proved perfect selection among Step-1 **restart clocks** at s=40 cannot clear
EM1 (S3 ≈ 0.3998 / 0.3984). Its scope limit left **dense RTH 1m bar opens** unbound.
Catalogue wall names viable new-construct stops in **5–20 pt**. This Phase 0 asks the
selection-ceiling question on that denser causal set at **G=10** (mid-band gate).

**Symptom-only:** restart-clock selection headroom absent; all-bars not yet measured.

---

## §2 — Prior art / lineage

- MNQSEL-1 STOP — different universe required.
- R2 OF cells (OFCHAN / R2VBUCK / R2AGRUN / R2FLOW) — association only; not selection ceilings.
- ORB/ICT DEAD + F2 GUARD — no filter laundering.

---

## §3 — Question (Q-MNQSEL-2)

On dense RTH 1m bar-open candidates at G=10 (1R target = G), does oracle top-1/day mean net R
clear ≥0.40 on ≥1 arm while all-take stays &lt;0.40?

---

## §4 — Falsifiable hypothesis (H-SEL-2)

**Hypothesis H-SEL-2:** On ≥1 arm, oracle top-1/day mean net R (S3) ≥ 0.40 while all-take
(S1) stays &lt; 0.40 on dense RTH 1m opens at G=10.

**Falsifier:** Phase-0 gate table in [`PREREG.md`](../../../lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/PREREG.md) §4
(C1/C2/C3/C4). `FALSIFIED` if S3 &lt; 0.40 both arms. `RESOLVED` if S3 ≥ 0.40 and S1 &lt; 0.40
on a non-surprise arm.

**Reject if:** C2 fires → STOP dense-bar selection; re-proposal = yet another causal set
(not denser OF on 1m opens; not G retune into the gate).

**Accept if:** C4 → selection headroom exists; construct ITERATE licensed (separate Q).

**Ambiguous / other:** `INSUFFICIENT-N` / `SURPRISE-DIRECTION` per PREREG.

---

## §5 — Forbidden moves

- Restart-clock re-open; completed-window ranking; Cap claim; OF feature hunt from this brief alone.
- Elevating G=5/20 diagnostics to gate after seeing numbers.
- ORB filter laundering; Pine; rail arming; Striker redeploy.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | C4 | ITERATE → construct packet unpaid |
| `FALSIFIED` | C2 | STOP this universe |
| `SURPRISE-DIRECTION` / `INSUFFICIENT-N` | C3 / C1 | dated packet; no construct |

---

## §7 — Execution plan

1. PREREG frozen (this campaign).
2. Unit tests green → run Phase 0 on local parquet.
3. RESULTS + closure disposition → board writes.

---

## §10 — Audit hooks

```bash
test -f lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/PREREG.md
test -f lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/ADMISSION_FALSIFIER_LOG.md
rg "Falsifier|falsified" docs/briefs/rnd-pipeline/Q-MNQSEL-2-dense-1m-selection-ceiling-scoping.md
```
