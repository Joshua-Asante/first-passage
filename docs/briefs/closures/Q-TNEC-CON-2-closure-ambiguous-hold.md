# Q-TNEC-CON-2 — CLOSURE: `AMBIGUOUS-HOLD` (gross-positive / net-negative; non-promotable)

**Verdict:** `AMBIGUOUS-HOLD` — non-promotable close of this G0 cell (both arms net-negative with CIs
straddling 0; frozen FALSIFIED trigger did not fire)
**Closed:** 2026-08-10
**Pre-registration:** [`PREREG_G0.md`](../../../lab/analysis/c1/mnq_tnec_con2_compression_break_2026-08/PREREG_G0.md) (FROZEN 2026-08-09) · parent [`brief`](../Q-TNEC-CON-2-compression-expansion-break-scoping.md)
**Explore GO:** operator in-session 2026-08-10; split/placebo/downgrades declared at GO, pre-score — [`EXPLORE_GO.md`](../../../lab/analysis/c1/mnq_tnec_con2_compression_break_2026-08/EXPLORE_GO.md)
**Spend / K:** $0.00 · `K_intrinsic=1` disclosure only · Cap seat **not claimed**
**Live effect:** none — CONFIRM (2025-09-01→2026-08-05) reserved and **unread**; no rail / Pine / arming
**Artifacts:** [`RESULTS_g2.md`](../../../lab/analysis/c1/mnq_tnec_con2_compression_break_2026-08/RESULTS_g2.md) · [`RESULTS.json`](../../../lab/analysis/c1/mnq_tnec_con2_compression_break_2026-08/RESULTS.json)

---

## 1. Verdict against the frozen gate

| Route | Trigger | Actual | Fired? |
|---|---|---|---|
| `FALSIFIED` | both arms n≥100 ∧ CI upper < 0 | CI uppers +0.0551 / +0.0918 | — |
| `SHAPE-CLEAR-CANDIDATE` | an arm: CI lo > 0 ∧ mean > 0 (+ declared aux: placebo <0.05, annSR ≥0.650, halves agree) | both means negative | — |
| `AMBIGUOUS-HOLD` | otherwise; halves sign-disagree | long +0.0238/−0.1045 · short +0.1111/−0.1539 (both flip) | ✓ |

H-CON-2 (brief §4: ≥1 arm CI entirely above 0 and DSR ≥ 0.650) is **not confirmed**.

## 2. Predicted vs happened

The cheap falsifier (pre-freeze, generous) showed negative point estimates with straddling CIs and did not
fire; EXPLORATION reproduced exactly that at 3× the n — plus the decomposition the falsifier could not see:
**gross +0.90/+0.97 pt per trade, placebo-corroborated (short p_emp 0.027), fully consumed by the 1.41-pt
round trip** (0.65× vs the 4× bar), and an older-positive → newer-negative halves flip on both arms.

## 3. What this closure does NOT license

Reading CONFIRM · Cap claim · any retune of frozen constants (Trap #12) · sign-invert to fade (Family A) ·
treating "beats random entries" as candidate status · Striker redeploy / arming.

## 4. Defects found in the frozen packet (recorded, repaired pre-score, not post-hoc)

The G0 froze "EXPLORATION only / CONFIRM unread" **without pinning the boundary**, and specified placebo/
halves/DSR limbs the runner did not implement. Both gaps were closed **at GO, before any score**, in
`EXPLORE_GO.md` (boundary 2025-08-31/2025-09-01 on the family anchor; random-entry placebo operationalization
with declared p<0.05; DSR read as annSR ≥ floor 0.650). Also disclosed there: the pre-freeze cheap falsifier
had computed full-panel arm means once, so CONFIRM is virgin to selection, not to sight.

## 5. Lesson candidates

**2026-08-10 — dense-1m entry families on MNQ keep finding ~1 pt gross that 1.41 pt RT eats.** CON-2 gross
+0.90/+0.97 pt at G=10 sits beside ORB's ~+0.9 pt gross (+0.0626R net) and the seed-target arithmetic. Watch:
a third dense-1m cell that does not change the **cost geometry** (selectivity or hold shape that raises gross
per trade, not another ~1 pt entry family) is the exhausted move. Below the two-incident bar as phrased; watch.

---

## Iterate — loop exit (MANDATORY — closure incomplete without it)

- **Verdict used:** `AMBIGUOUS-HOLD` (gross-positive / net-negative; halves flip)
- **Model update:** Compression→expansion-break at G=10 session-flat carries a real but sub-cost gross edge
  (~+0.9–1.0 pt/trade vs 1.41 pt RT) that decays across the EXPLORATION span. The venue's binding constraint
  is untouched; the construct's is cost geometry, same wall as ORB/D5/H-OD-1.
- **Next:** STOP
- **Routing:** STOP — cell non-promotable; CONFIRM stays reserved and unread. A successor dense-1m cell is a
  **fresh Q / fresh G0** that must attack gross-per-trade (selectivity / hold shape), not another ~1 pt entry
  family and not a retune of this one.
- **Entry packet:** n/a — STOP
- **Stop rule / re-proposal bar:** Re-open of compression-break on MNQ requires new **mechanism** evidence or
  a materially different cost geometry — not `K_NARROW`/`NARROW_MULT`/window/G edits, not the fade inversion.
- **Board write:** `SESSIONS Open/next: dense-1m lane cell #3 needs a fresh G0 aimed at cost geometry — or
  decline and hold TNEC intake on new sourcing channels. Carry: weekly token trade; F1 2026-11-08; PARK
  expiries; M1 arm-harden.` Owner: this closure.

---

## §10 audit-hook discharge

```text
PREREG_G0.md frozen 2026-08-09 (introducing commit precedes all scores)  OK
EXPLORE_GO.md declarations precede RESULTS.json scored_at                OK
CONFIRM rows dropped pre-scoring (runner EXPLORE_END filter)             OK
lib tests 8/8 green pre-run                                              OK
$0.00 / K=1 disclosure / manifests unchanged / Cap unclaimed             OK
```
