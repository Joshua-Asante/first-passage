# Q-MNQSEL-1 — CLOSURE: `FALSIFIED` (C2; selection ceiling under EM1)

**Verdict:** `FALSIFIED` (C2) — oracle top-1/day S3 below EM1 0.40 on **both** arms; STOP this universe
**Closed:** 2026-08-07
**Pre-registration:** [`PREREG.md`](../../lab/archive/mnq_selection_ceiling_2026-08/PREREG.md)
**Parent:** [`Q-MNQSEL-1`](../rnd-pipeline/Q-MNQSEL-1-selection-value-ceiling-scoping.md)
**Spend / K:** $0.00 · K=0 · Cap **not claimed** · no manifest
**Live effect:** none — no feature campaign licensed
**Artifacts:** [`RESULTS.md`](../../lab/archive/mnq_selection_ceiling_2026-08/RESULTS.md)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` (C4) | S3 ≥ 0.40 on ≥1 arm **and** S1 < 0.40 | S3 long **0.3998** / short **0.3984** — both **< 0.40** | — |
| `FALSIFIED` (C2) | S3 < 0.40 on **both** arms | S3 both under bar; S1 long **−0.0364** / short **−0.0362**; n_sessions **1,674** ≥ 250 (C1 clear); no SURPRISE-DIRECTION | ✓ |
| `AMBIGUOUS` (`INSUFFICIENT-N`) | C1 | n clear | — |

| Arm | S1 all-take | S3 oracle top-1/day | S5 median hits | S6 ≥1 hit |
|---|---:|---:|---:|---:|
| long | −0.0364 | **0.3998** | 98.0 | 99.9% |
| short | −0.0362 | **0.3984** | 97.0 | 99.7% |

---

## 2. What the pre-registration predicted vs what happened

PREREG §4 called **C4 (`RESOLVED`)** most likely. That expectation was **wrong** — S3 sits on the EM1 knife-edge from below (clean target-hit earns ≈0.40R by G construction; no-hit sessions pull the mean a few ten-thousandths under). Recorded as a failed prediction, not retrofitted.

---

## 3. What this closure does NOT license

- A feature campaign or Route B cell on the **same** restart-clock universe (FM-8).
- Denser order-flow on the same clocks, or completed-window ranking, as a rescue.
- Reading S3 ≈ 0.40 as “close enough” to clear EM1.

---

## 4. Defects found in the frozen brief (recorded, not repaired)

None that change the verdict.

---

## 5. Lesson candidates

**2026-08-07 — oracle top-1/day on Step-1 restart clocks can sit under EM1 by averaging in no-hit sessions even when ≥99.7% of sessions have a clean hit.** Cost: $0 Phase-0. Below two-incident bar — watch.

---

## Iterate — loop exit

- **Verdict used:** `FALSIFIED` (C2)
- **Model update:** Perfect one-trade/day selection among causal restart clocks does **not** clear EM1 with margin. All-take is dead (~−0.036R); selection is load-bearing in spirit but the ceiling is under the bar. Density of winners (S5 ≈ 97–98 hits/day) does not rescue the gate.
- **Next:** STOP
- **Routing:** STOP — this universe closed. Any successor must propose a **different causal candidate set** with its own Phase-0 ceiling before a feature campaign.
- **Entry packet:** n/a — STOP
- **Stop rule / re-proposal bar:** Re-proposal = a **different causal candidate set** — **not** denser OF on the same clocks, **not** completed-window ranking.
- **Board write:** none — STOP, nothing owed (roster row deletion is bookkeeping only).

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-09 | Closure authored (verdict landed 2026-08-07; artifact was missing) | Cursor + JA |
