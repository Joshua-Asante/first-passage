# Q-R2AGRUN-1 — Does aggressor-run length predict 60 s mid returns on MNQ (Route B)?

**Status:** `CLOSED — Stage-G AMBIGUOUS-HOLD` — non-promotable STOP (operator);
[`closure`](closures/Q-R2AGRUN-1-closure-ambiguous-hold.md) ·
[`RESULTS_g2`](../../lab/analysis/c1/mnq_r2agrun_routeb_2026-08/RESULTS_g2.md).
Successor named: [`Q-R2FLOW-1`](Q-R2FLOW-1-signed-minute-flow-route-b-scoping.md).
**Authored:** 2026-08-08
**Closed:** 2026-08-08
**Authors:** Joshua + Cursor; Rule-0 + cheap falsifier parent-side; SPEC S6 ADMIT logged
**Parent question:** MNQDTL-1 **R2** (live under S1) · `Q-R2VBUCK-1` STOP (*new G0 / new mechanism*) · `Q-OFCHAN-1` STOP · `Q-MNQSEL-1` STOP (*different causal set*)
**Sub-questions opened:** none until G2
**Loop:** Inquire-phase Pre-Q — gates whether a single pre-registered Route B cell (signed aggressor-run trade-count → 60 s mid) clears Stage-G on EXPLORATION, then (under Cap reservation + confirm GO) Stage-C on a **fresh** CONFIRM half
**Artifact path:** `docs/briefs/Q-R2AGRUN-1-aggressor-run-length-route-b-scoping.md`
**Spend:** $0 · K disclosure only (`K_intrinsic=1`) · no Cap claim · nothing armed · **no new pull** (OFCHAN cache reuse) · CONFIRM unread

> **G2 outcome (2026-08-08, after operator explore GO):** coverage/power PASS
> (22,304,297/22,304,297); ρ −0.001306 · CI excludes 0 · placebo PASS · halves agree ·
> \|ρ\| < 0.02 → **AMBIGUOUS-HOLD**; candidates `[]` → ITERATE (no CONFIRM).
> Re-proposal = operator fork: close non-promotable → new G0, or hold — **not** floor retune.

---

## §0 — Rule 0 reads (verified 2026-08-08 at HEAD `05e17b0`)

| Path | Anchor | What it grounds |
|---|---|---|
| [`core/firm_rules.py`](../../core/firm_rules.py) `Tradeify_Select_100K` | `45e3cea` | Incumbent eval geometry |
| [`docs/spec/2026-08-05-eval-mechanism-shape-screen.md`](../spec/2026-08-05-eval-mechanism-shape-screen.md) | `d93dafd` | EM0–EM5; G0 act §2.0a |
| [`docs/spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md`](../spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md) | `27c7943` | MNQDTL D1/D2; R2 live; Cap before K-spend |
| [`docs/adr/2026-08-05-avenue-a-generate-confirm-route.md`](../adr/2026-08-05-avenue-a-generate-confirm-route.md) | `b0427fd` | Route B Accepted; fresh holdout rule |
| [`docs/methodology/avenue_a_generate_confirm.md`](../methodology/avenue_a_generate_confirm.md) | `b0427fd` | G0 checklist |
| [`docs/spec/2026-08-07-loop-s6-k-aware-generation-spec.md`](../spec/2026-08-07-loop-s6-k-aware-generation-spec.md) | `45e3cea` | S6 admission schema |
| [`lab/discovery/admission_schema.py`](../../lab/discovery/admission_schema.py) | `cc4142e` | Machine ADMIT/REFUSE |
| [`lab/archive/mnq_r2vbuck_routeb_2026-08/RESULTS_g2.md`](../../lab/archive/mnq_r2vbuck_routeb_2026-08/RESULTS_g2.md) | `2dc14db` | Association null; reopen = new mechanism |
| [`lab/analysis/c1/mnq_ofchan_routeb_2026-08/RESULTS_g2.md`](../../lab/analysis/c1/mnq_ofchan_routeb_2026-08/RESULTS_g2.md) | on main | VOID-COVERAGE; new G0 required |
| [`docs/briefs/rnd-pipeline/Q-MNQSEL-1-selection-value-ceiling-scoping.md`](rnd-pipeline/Q-MNQSEL-1-selection-value-ceiling-scoping.md) | on main | Restart-clock STOP |
| [`lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md`](../../lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md) | `87b0547` | K=1 floor 0.650 |
| [`ops/instruments/MNQ.md`](../../ops/instruments/MNQ.md) DEAD / C9 bar | `2dc14db` | Not resting ToB size; not R2VBUCK retune |
| [`docs/notes/2026-08-04-databento-entitlement-inventory.md`](../notes/2026-08-04-databento-entitlement-inventory.md) | `b82ae65` | Rolling 1y `tbbo` free window |
| [`docs/adr/2026-08-07-loop-s1-environment-ratification.md`](../adr/2026-08-07-loop-s1-environment-ratification.md) | on main | Incumbent env; R1 foreclosed |

**Gitignore pre-flight.** No Pine read or cited. No new Databento `pull`.

**Cheap falsifier (parent-side):** OFCHAN EXPLORATION cache present (155 `*.tbbo.dbn.zst`); sample day mid computable; sides `B`/`A` present; **structural** run formation works (`N_min=2` a priori — not fit from EXPLORATION). S6 `evaluate_admission` → **ADMIT**.

---

## §1 — Context & motivation

MNQDTL R2 remains the live research route. OFCHAN died on coverage; R2VBUCK cleared coverage and died on **association** (aggressor *imbalance* inside volume buckets → 60 s mid null). The channel still needs a Route B cell that (a) clears C9’s “not resting ToB size” limb, (b) is **not** a B/horizon retune of R2VBUCK, and (c) spends only **K=1**.

**Symptom (not fix):** we lack a frozen test of whether **consecutive same-side aggressor pressure (run length)** associates with short-horizon mid returns — a herding/exhaustion object, not an imbalance ratio.

---

## §2 — Prior art / lineage

- **`Q-R2VBUCK-1`** — CLOSED FALSIFIED; reopen = **new mechanism**, not B/horizon retune.
- **`Q-OFCHAN-1`** — CLOSED VOID-COVERAGE; flicker/minute-grid barred as retune.
- **`Q-MNQSEL-1`** — CLOSED on restart clocks; different universe.
- **MNQFLOW C9** — named feature ≠ resting ToB size imbalance (tape aggressor run clears).
- **Catalogue K wall** — K=1 favoured.
- **SPEC S6** — ADMIT logged this session.

**Alternatives considered (not frozen):** (i) trade-arrival intensity (activity, weak direction); (ii) contemporaneous impact residual (heavier construct). **Elected:** signed aggressor-run trade-count — directional, coverage-safe, causally distinct from imbalance.

---

## §3 — Question (Q-R2AGRUN-1)

**Symptom-only rephrase:** imbalance-in-buckets and resting-size minute cells both emptied; we still lack a frozen Route B cell testing whether **how long an aggressor run lasts** associates with 60 s mid returns.

**Q-R2AGRUN-1:** On `MNQ.v.0` RTH, does signed trade-count of completed same-side aggressor runs (`N_min=2`) predict 60-second mid returns strongly enough to clear the frozen Stage-G promotion rule on the OFCHAN-cache EXPLORATION window, and — under a later Cap reservation + confirm GO — the fresh CONFIRM half at M=1?

The question does **not** presuppose explore GO, new pull, confirm, Cap spend, Pine, or deployment.

---

## §4 — Falsifiable hypothesis (H-R2AGRUN-1)

**Falsifier (binary):** the cell earns Route B candidate status only if Stage-G promotion clears on EXPLORATION under the frozen G0 limbs and Stage-C clears on the reserved CONFIRM window at M=1 under a later C0 PREREG (after Cap reservation); otherwise rejected / VOID / AMBIGUOUS without admission.

**H-R2AGRUN-1:** On the frozen G0 catalogue (exactly one cell: signed aggressor-run trade-count → 60 s mid, `tbbo`, `MNQ.v.0`, `N_min=2`), EXPLORATION-only promotion limbs fire with coverage/power clear; then, under Cap reservation + separate confirm GO and C0 PREREG, the same limbs clear on CONFIRM **2025-09-01→2026-02-06** at M=1 — establishing a Route B candidate (still not harvest admission / not deployment).

**Reject if:** Stage-G fails promotion **or** Stage-C fails → STOP this catalogue; re-proposal = new G0 / new mechanism, not post-hoc retune of `N_min`/horizon/sign.

**Accept if:** Stage-G emits candidate **and** Stage-C clears at M=1 → candidate recorded; harvest/EM1–EM2 remain independent.

**Ambiguous-hold if:** halves disagree after CI clear, or below \|ρ\| ≥ 0.02 floor, or VOID-POWER/COVERAGE.

---

## §5 — Forbidden moves

- **Issuing explore GO / G2 / confirm from this brief alone** — explore GO is a separate operator act (cache reuse only).
- **New Databento pull for EXPLORATION** — bytes already on disk (OFCHAN cache).
- **`trades`-first schema** — cannot compute mid; `tbbo` only.
- **Retuning R2VBUCK B / OFCHAN flicker / minute grid** — FM-9; this is a new catalogue.
- **Resting ToB size imbalance / MNQFLOW cheapest swing** — C9 bar.
- **Volume-bucket aggressor imbalance** — R2VBUCK STOP; sibling not a reopen.
- **MNQSEL restart-clock selection** — different STOP universe.
- **Fitting `N_min` from EXPLORATION** — `N_min=2` is a priori / definitional.
- **Claiming Cap at G0/G2** — Cap spent; reservation only before C0.
- **Re-cutting CONFIRM after G2** — holdout edit; use pre-registered $50 confirm budget instead.
- **Growing catalogue after G0** — Trap #12.
- **Pine / deployment / Striker redeploy** — not licensed.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | G0 frozen ∧ explore GO ∧ G2 promotion PASS ∧ Cap reservation ∧ C0 frozen ∧ confirm GO ∧ Stage-C PASS at M=1 ∧ no CONFIRM peek before C0 | `INTEGRATE` — record candidate; harvest/construct under separate GO |
| `FALSIFIED` | Stage-G fails promotion **or** Stage-C fails at M=1 | `STOP` — new G0 / new mechanism, not retune |
| `AMBIGUOUS-HOLD` | VOID-POWER/COVERAGE, halves disagree, or below magnitude floor | `ITERATE` — dated packet; do not score CONFIRM until resolved |

**This session's gate (closed):** explore GO paid → G2 `AMBIGUOUS-HOLD` (magnitude) → ITERATE; CONFIRM unread.

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
test -f lab/analysis/c1/mnq_r2agrun_routeb_2026-08/PREREG_G0.md
rg -n "N_min = 2|K_intrinsic = 1|2025-09-01|aggressor-run" lab/analysis/c1/mnq_r2agrun_routeb_2026-08/PREREG_G0.md

# S6 ADMIT
$env:PYTHONPATH='lab'; python -c "from discovery.admission_schema import load_admission, evaluate_admission; a=load_admission('lab/analysis/c1/mnq_r2agrun_routeb_2026-08/admission_s6.json'); print(evaluate_admission(a, registered_k=1).decision)"

# Cache still present
python -c "from pathlib import Path; p=Path.home()/'.databento_cache/q_ofchan_1_exploration_tbbo/GLBX-20260807-EHX5KUSF7K'; print(len(list(p.glob('*.tbbo.dbn.zst'))))"
```
