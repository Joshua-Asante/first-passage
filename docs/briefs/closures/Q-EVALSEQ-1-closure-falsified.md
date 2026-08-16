# Q-EVALSEQ-1 — CLOSURE: `FALSIFIED` (schedule lever spent for eval-pass lift)

**Verdict:** `FALSIFIED` — no frozen schedule lifts eval pass-probability by > 5pt at ≤ control bust; flat WATCH-1 stands (the prereg's own falsifier branch, verbatim)
**Closed:** 2026-08-16
**Lane:** UNASSIGNED
**Pre-registration:** [frozen 2026-07-24](../pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md) (§0–§10 byte-unedited; un-dormed scoring-only 2026-08-16, [P2 mark](STATE-POLICY-closure-resolved-p2.md)) + [camp operationalizations](../../lab/analysis/c1/q_evalseq_1_2026-08/OPERATIONALIZATION.md) (frozen pre-read; gate-v2 amendment recorded pre-read)
**Spend / K:** $0 · K_intrinsic = 3 consumed at this read (the prereg's banked count) · no Pine / TV / arming · no deployment surface touched
**Artifacts:** [RESULTS](../../lab/analysis/c1/q_evalseq_1_2026-08/RESULTS.md) · `out/evalseq_results.json`

---

## 1. Verdict (frozen §6 asserted)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` (adopt-eligible) | best pass-prob > control + 5pt AND bust ≤ control AND both-halves survival | best lift **−1.06pt** (c_cushion) | — |
| `FALSIFIED` (lever spent) | any limb fails | lift limb failed by 6.06pt | ✓ |
| `AMBIGUOUS` (power short) | power insufficient | n/a — 30K paths/arm, decisive margins | — |

Numbers: control (flat 0.50×) pass 75.01% / bust 20.18%; (b) −8.47pt / 15.38%;
(c) −1.06pt / **0.00%**; (d) −4.52pt / 19.63%. Halves and placebo recorded in RESULTS (moot
for the verdict). Fidelity: v1 gate FIRED (38.17 vs recorded 37.78), diagnosed as
environment/panel vintage — the recovered original itself prints 38.2 on this environment —
and gate v2 (port ≡ original) PASSED before any policy read.

## 2. What died, exactly

The **front-load schedule hypothesis**: that any of the three frozen schedules raises
Select-100K eval pass-probability > 5pt at equal-or-lower bust on the 2-leg book. The prereg's
§2 prior (weakly negative for eval-pass) was correct; the flat-sweep intuition extends to
schedules on the pass axis. Sprint-shaped size-early ideas on this book are now measured-dead
twice (flat sweep; this).

## 3. Surviving finding (NOT rejected)

**Cushion-proportional sizing (policy c) eliminated trailing-DD bust — 20.18% → 0.00%, both
halves — at 1.06pt of pass.** First measured evidence that the within-attempt state-dependent
lever is real and large on the **survival** axis. Three disclosed bounds (EOD clock;
integer-floor abstraction; in-panel tails) in RESULTS. This is a lever finding on a barred
book — it admits nothing and re-proposes nothing by itself.

## 4. What this closure does NOT license

- θ-retune of the three schedules or a fourth schedule under this prereg (family spent).
- Reading policy (c) as an N-SURV admission, a deployment, a dd_protection change, or a
  WATCH-1 rung change — sizing-policy adoption has its own governance chain, untouched.
- Opening Q-POLFRONT-1 without its own brief (commissioned by the P2 mark; reframed below).

## 5. Lesson candidates

Below the two-incident bar — watch: a pass-prob-shaped H can falsify while the same run
surfaces a survival-axis effect 20× the H's own margin; the prereg's verdict vocabulary had no
slot for the off-axis finding, and the closure's surviving-finding block is where it lives.

## Iterate — loop exit

- **Verdict used:** `FALSIFIED` (lever spent for eval-pass lift)
- **Model update:** schedules do not buy pass-probability on this book; state-dependent
  sizing buys survival, cheaply — the lever the diagnostic hypothesized is real, on the other
  axis. Constant-policy N-SURV numbers are conservative against exactly this policy class.
- **Next:** ITERATE
- **Routing:** successor is **Q-POLFRONT-1** (already commissioned by the [P2 mark](STATE-POLICY-closure-resolved-p2.md); still unopened) with its question REFRAMED by §3: how much
  base-R headroom does cushion-proportional sizing buy at the frozen bust ≤ 3.0% ceiling on
  synthetic (w, b, r, k, d) seed cells — N-SURV admissible-region widening, candidate-independent
- **Entry packet:** frozen inputs = this closure's §3 finding + its three disclosed bounds; the
  four policy shapes as measured (no new shapes without their own accounting); the
  seed-target-spec frontier tables as the baseline grid; forbidden re-opens = §4 above
- **Stop rule / re-proposal bar:** re-proposal of a *pass-prob* schedule H on this book needs
  new mechanism evidence, not a reweighted schedule; Q-POLFRONT-1 opens only on its own brief
  with operator GO
- **Board write:** `SESSIONS Open/next: Q-POLFRONT-1 brief (bust-axis reframe) → then deep-lane GO-1.` Owner: this closure · [RESULTS](../../lab/analysis/c1/q_evalseq_1_2026-08/RESULTS.md)
- **Registry:** n/a — policy-lever falsification on the operational layer, not a
  strategy-mechanism rejection (no `rejected_candidates.md` row; the prereg's own falsifier
  text is the record)

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-16 | Frozen run executed under the P2 mark; FALSIFIED recorded; surviving finding routed to Q-POLFRONT-1 | Claude Code (JA mark) |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-EVALSEQ-1-closure-falsified.md
python lab/analysis/c1/q_evalseq_1_2026-08/run_evalseq.py   # reproduces (fidelity-gated)
```
