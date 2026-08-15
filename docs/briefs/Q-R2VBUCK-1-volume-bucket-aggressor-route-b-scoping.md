# Q-R2VBUCK-1 — Does volume-bucket aggressor imbalance predict 60 s mid returns on MNQ (Route B)?

**Status:** `CLOSED — Stage-G FALSIFIED` — G2 empty candidates; STOP this G0 catalogue
([`RESULTS_g2`](../../lab/archive/mnq_r2vbuck_routeb_2026-08/RESULTS_g2.md)).
**Authored:** 2026-08-08
**Closed:** 2026-08-08
**Authors:** Joshua + Cursor; Rule-0 + cheap falsifier parent-side; SPEC S6 ADMIT logged
**Parent question:** MNQDTL-1 **R2** (live route under S1) · `Q-OFCHAN-1` STOP re-proposal bar (*new G0*, not retune) · `Q-MNQSEL-1` STOP (*different causal candidate set*)
**Sub-questions opened:** none until G2
**Loop:** Inquire-phase Pre-Q — gates whether a single pre-registered Route B cell (volume-bucket aggressor imbalance → 60 s mid) clears Stage-G on EXPLORATION, then (under Cap reservation + confirm GO) Stage-C on a **fresh** CONFIRM half
**Artifact path:** `docs/briefs/Q-R2VBUCK-1-volume-bucket-aggressor-route-b-scoping.md`
**Spend:** $0 · K disclosure only (`K_intrinsic=1`) · no Cap claim · nothing armed · **no new pull** (OFCHAN cache reuse) · CONFIRM unread

> **G2 outcome (2026-08-08, after operator explore GO):** coverage/power PASS
> (77,656/77,656); ρ −0.005478 · CI includes 0 · placebo FAIL → **FALSIFIED**;
> candidates `[]` → STOP. Re-proposal = **new G0 / new mechanism**, not retune.

---

## §0 — Rule 0 reads (verified 2026-08-08)

| Path | Anchor | What it grounds |
|---|---|---|
| [`core/firm_rules.py`](../../core/firm_rules.py) `Tradeify_Select_100K` | `45e3cea` | Incumbent eval geometry |
| [`docs/spec/2026-08-05-eval-mechanism-shape-screen.md`](../spec/2026-08-05-eval-mechanism-shape-screen.md) | `d08537a` | EM0–EM5; G0 act §2.0a |
| [`docs/spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md`](../spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md) | `27c7943` | MNQDTL D1/D2; R2 live; Cap before K-spend; F-B K≤2 |
| [`docs/adr/2026-08-05-avenue-a-generate-confirm-route.md`](../adr/2026-08-05-avenue-a-generate-confirm-route.md) | `b0427fd` | Route B Accepted; fresh holdout rule |
| [`docs/methodology/avenue_a_generate_confirm.md`](../methodology/avenue_a_generate_confirm.md) | `b0427fd` | G0 checklist |
| [`docs/spec/2026-08-07-loop-s6-k-aware-generation-spec.md`](../spec/2026-08-07-loop-s6-k-aware-generation-spec.md) | `45e3cea` | S6 first-campaign gate |
| [`lab/discovery/admission_schema.py`](../../lab/discovery/admission_schema.py) | `cc4142e` | Machine ADMIT/REFUSE |
| [`lab/analysis/c1/mnq_ofchan_routeb_2026-08/RESULTS_g2.md`](../../lab/analysis/c1/mnq_ofchan_routeb_2026-08/RESULTS_g2.md) | `a4b36f8` | VOID-COVERAGE 7.36%; new G0 required |
| [`docs/briefs/rnd-pipeline/Q-MNQSEL-1-selection-value-ceiling-scoping.md`](rnd-pipeline/Q-MNQSEL-1-selection-value-ceiling-scoping.md) | `d56ef6b` | Restart-clock STOP; different universe |
| [`lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md`](../../lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md) | `87b0547` | K=1 floor 0.650; best-ever +0.835 |
| [`ops/instruments/MNQ.md`](../../ops/instruments/MNQ.md) DEAD / N12 / N14 | `45e3cea` | C9 bar quote; Mesfin 2605.04004/17724 only |
| [`docs/notes/2026-08-04-databento-entitlement-inventory.md`](../notes/2026-08-04-databento-entitlement-inventory.md) | `b82ae65` | Rolling 1y `tbbo` free window |
| [`docs/adr/2026-08-07-loop-s1-environment-ratification.md`](../adr/2026-08-07-loop-s1-environment-ratification.md) | on main | Incumbent env; R1 foreclosed |

**Gitignore pre-flight.** No Pine read or cited. No new Databento `pull`.

---

## §1 — Context & motivation

MNQDTL-1 R2 is the live research route on the incumbent Tradeify eval (S1). OFCHAN’s first Route B catalogue died on VOID-COVERAGE because a flicker filter demanded dense same-sign updates at *clock minutes* on trade-tagged TBBO. MNQSEL showed that perfect selection on **restart-clock** event windows sits under EM1 — that is a different universe, not a ban on all intraday association tests.

**Symptom (not fix):** the order-flow channel still has no Route B generate→confirm cell that (a) clears C9’s “not resting ToB size” limb, (b) avoids OFCHAN’s minute-grid coverage pathology, and (c) spends only **K=1** of the R2 F-B budget.

---

## §2 — Prior art / lineage

- **`Q-OFCHAN-1`** — CLOSED VOID-COVERAGE; reopen = **new G0**, not retune (`a4b36f8`).
- **`Q-MNQSEL-1`** — CLOSED-FALSIFIED on restart clocks; re-proposal = different causal candidate set (`d56ef6b`).
- **MNQDTL-1 / S1** — R2 live; Cap reservation before K-spend; incumbent scoring (`27c7943`).
- **MNQFLOW-1 DEAD** — Route 2 not closed beyond cheapest ToB size swing; C9 bar quoted in G0.
- **Mesfin 2605.04004 / 2605.17724 (N12)** — corroboration only; OHLCV families dry; VVG descriptor finding is **inside 04004** (do not cite non-repo IDs).
- **Catalogue K wall** — K=1 favoured; K=2 floor 0.850 vs best-ever +0.835 on Tradeify basis (`87b0547`).
- **SPEC S6** — first campaign under admission schema; ADMIT logged this session.

---

## §3 — Question (Q-R2VBUCK-1)

**Symptom-only rephrase:** OFCHAN’s minute-grid resting-size cell emptied on coverage; MNQSEL’s restart-clock selection ceiling sits under EM1; we still lack a frozen Route B cell that tests whether **tape aggressor imbalance on volume buckets** associates with short-horizon mid returns.

**Q-R2VBUCK-1:** On `MNQ.v.0` RTH, does signed aggressor size imbalance inside completed volume buckets of size **B=2550** predict 60-second mid returns strongly enough to clear the frozen Stage-G promotion rule on the OFCHAN-cache EXPLORATION window, and — under a later Cap reservation + confirm GO — the fresh CONFIRM half at M=1?

The question does **not** presuppose explore GO, new pull, confirm, Cap spend, Pine, or deployment. **Volume-bucket sampling ≠ MNQSEL restart clocks.**

---

## §4 — Falsifiable hypothesis (H-R2VBUCK-1)

**Falsifier (binary):** the cell earns Route B candidate status only if Stage-G promotion clears on EXPLORATION under the frozen G0 limbs and Stage-C clears on the reserved CONFIRM window at M=1 under a later C0 PREREG (after Cap reservation); otherwise the cell is rejected / VOID / AMBIGUOUS without admission.

**H-R2VBUCK-1:** On the frozen G0 catalogue (exactly one cell: volume-bucket aggressor imbalance → 60 s mid, `tbbo`, `MNQ.v.0`, B=2550), EXPLORATION-only promotion limbs fire with coverage/power clear; then, under Cap reservation + separate confirm GO and C0 PREREG, the same limbs clear on CONFIRM **2025-09-01→2026-02-06** at M=1 — establishing a Route B candidate (still not harvest admission / not deployment).

**Reject H-R2VBUCK-1 if:** Stage-G fails promotion (CI/placebo/VOID) **or** Stage-C fails under C0 → STOP this catalogue; re-proposal = new G0 / new mechanism, not post-hoc retune.

**Accept H-R2VBUCK-1 if:** Stage-G emits candidate **and** Stage-C clears at M=1 → candidate recorded; harvest/EM1–EM2 remain independent.

**Ambiguous-hold if:** halves disagree after CI clear, or below \|ρ\| ≥ 0.02 floor, or VOID-POWER/COVERAGE.

---

## §5 — Forbidden moves

- **Issuing explore GO / G2 / confirm from this brief alone** — explore GO is a separate operator act (cache reuse only).
- **New Databento pull for EXPLORATION** — bytes already on disk (OFCHAN cache).
- **`trades`-first schema** — cannot compute mid; `tbbo` only.
- **K=2 / second near-duplicate bucket cell** — spends R2 F-B budget; sibling = new campaign.
- **Retuning OFCHAN flicker / minute grid** — FM-9; this is a new catalogue.
- **Resting ToB size imbalance / MNQFLOW cheapest swing** — C9 bar.
- **MNQSEL restart-clock selection / completed-window ranking** — different STOP universe.
- **Claiming Cap at G0/G2** — Cap spent; reservation only before C0.
- **Re-cutting CONFIRM after G2** — holdout edit; use pre-registered $50 confirm budget instead.
- **Growing catalogue after G0** — Trap #12.
- **Pine / deployment / Striker redeploy** — not licensed.
- **Citing arXiv 2605.11423** — not in estate; VVG lives in 2605.04004 N12.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | G0 frozen ∧ explore GO ∧ G2 promotion PASS ∧ Cap reservation ∧ C0 frozen ∧ confirm GO ∧ Stage-C PASS at M=1 ∧ no CONFIRM peek before C0 | `INTEGRATE` — record candidate; harvest/construct under separate GO |
| `FALSIFIED` | Stage-G fails promotion **or** Stage-C fails at M=1 | `STOP` — new G0 / new mechanism, not retune |
| `AMBIGUOUS-HOLD` | VOID-POWER/COVERAGE, halves disagree, or below magnitude floor | `ITERATE` — dated packet; do not score CONFIRM until resolved |

**This session's gate (closed):** explore GO paid → G2 `FALSIFIED` → STOP catalogue.

---

## §7 — Execution plan

1. Operator: **explore GO** (cache reuse; no new pull).
2. G2 on EXPLORATION only → candidate list.
3. Empty → STOP. ≥1 → **Cap-seat reservation** → C0 PREREG → confirm GO (CONFIRM `$ ≤ 50` estimate).
4. Strategy formation only after confirm RESOLVED (separate packet).

Harness implementation is out of this authoring packet.

---

## §8 — EM attestation (re-derived K=1)

`P U U D D D` + D1/D2 class True — see G0 §5. Not SHAPE-CLEAR.

---

## §10 — Audit hooks

```bash
# G0 freeze present
test -f lab/archive/mnq_r2vbuck_routeb_2026-08/PREREG_G0.md
rg -n "B = 2550|K_intrinsic = 1|2025-09-01" lab/archive/mnq_r2vbuck_routeb_2026-08/PREREG_G0.md

# S6 ADMIT log
rg -n '"decision": "ADMIT"' lab/archive/mnq_r2vbuck_routeb_2026-08/admission_s6.json

# Re-evaluate admission
PYTHONPATH=lab python -c "from discovery.admission_schema import load_admission, evaluate_admission; a=load_admission('lab/archive/mnq_r2vbuck_routeb_2026-08/admission_s6.json'); print(evaluate_admission(a, registered_k=1).decision)"

# Cache still present
python -c "from pathlib import Path; p=Path.home()/'.databento_cache/q_ofchan_1_exploration_tbbo/GLBX-20260807-EHX5KUSF7K'; print(len(list(p.glob('*.tbbo.dbn.zst'))))"
```
