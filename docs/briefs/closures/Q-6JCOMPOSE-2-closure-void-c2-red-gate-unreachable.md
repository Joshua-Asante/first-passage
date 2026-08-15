# Closure — Q-6JCOMPOSE-2: `VOID — C2 RED; gate unreachable by construction`

**Date:** 2026-07-29 · **Pre-reg:** [`Q-6JCOMPOSE-2`](../pre-registration/Q-6JCOMPOSE-2-verdict-preregistration.md)
(`SIGNED / FROZEN 2026-07-29 / JA`, commit `fdba9de`)
**Verdict:** **VOID.** Control **C2 is RED**, and §5's last bullet + §4's table make that VOID with
**no verdict read**. **The composed arm was NOT run.**
**Spend:** $0.00 · **K:** unchanged · **6J composed number computed:** **none**.

---

## §1 — C2 result

With the 6J column supplied as **all zeros**, §7 C2 required the 2-leg baseline
**0.11 / 0.22 / 0.04**. Measured (`Tradeify_Select_100K`):

| Partition | §7 C2 expected | Measured | |
|---|---:|---:|---|
| full | 0.11% | **2.6467%** | ✗ |
| H1 | 0.22% | **4.3700%** | ✗ |
| H2 | 0.04% | **1.6967%** | ✗ |
| boot-95th | 1.20% | **10.3743%** | ✗ |

**C2 RED ⇒ VOID.** Rule followed as written, not re-interpreted.

## §2 — But the wrapper is EXONERATED — it reproduced the engine's own baseline exactly

`2.65 / 4.37 / 10.37` are not arbitrary: they are **the compose engine's own un-haircut 2-leg
figures**, which the engine prints in its own output as `(2-leg H1 4.37% boot95 10.37%)`. The
all-zero composition returned the engine's baseline **to the digit**, which is precisely what a
non-perturbation control should show.

**The defect is §2's declared baseline, not the wrapper.** §2 cited
**full 0.11% / H1 0.22% / H2 0.04% / boot-95th 1.20%** — the **WATCH-1 0.50× haircut** figures from
the *sibling* harness `class_s_c1_haircut_regime_remc`. This engine composes against the
**un-haircut 1.00%-rung** 2-leg book: `C1_ALLOCS = {striker: 0.0070, striker_nas100: 0.0037}`.

**The engine's own docstring says so, and I read it.** Lines 8-11:

> *"the 2-leg sub-book runs UN-haircut (the 0.50x/0.25x arms belong to the sibling haircut pre-reg
> and are **forbidden from being folded in** — §5 / Trap #11)."*

It is cited in Q-6JCOMPOSE-2 §0 row 3. **Rule-0 miss:** I read the file and did not reconcile its
docstring against the baseline I wrote into §2 two sections later.

## §3 — The load-bearing finding: H was UNREACHABLE BY CONSTRUCTION

H requires `max(full, H1, H2, boot-95th) ≤ 3.0%`. The **baseline — with no 6J leg at all** — is:

| Partition | Baseline | vs 3.0% ceiling |
|---|---:|---|
| full | 2.65% | PASS |
| **H1** | **4.37%** | **FAIL — already over** |
| H2 | 1.70% | PASS |
| **boot-95th** | **10.37%** | **FAIL — already over** |

Adding a positive-variance leg can only raise bust. **So `max(...) > 3.0%` was guaranteed before 6J
entered the panel.** Running the arm would have produced a **FALSIFIED that says nothing about
Aegis-6J** — it would have been the *baseline* failing, misattributed to the leg. Hence the arm was
not run: a predetermined verdict is worse than no verdict, because it looks like evidence.

This is [`lesson_gate_reachability_preregistration`](../../methodology/lessons/methodology_lessons.md)
firing — and it is the **second time in this instrument family**: the aegis-6j **v1** pre-reg was
closed for exactly *"a gate frozen unreachable on the window it gated."* Same class, same
instrument, and this time the unreachability was in the *rung basis* rather than the window.

## §4 — What the composed question actually needs

**This engine cannot answer the question at the deployed rung.** Composing at WATCH-1 0.50× requires
the 2-leg sub-book at 0.50×, i.e. halving `C1_ALLOCS` — which is a frozen-engine input **and** is
explicitly forbidden by the engine's §5 / Trap #11. Two admissible routes, each a **fresh**
pre-registration:

1. **A harness that composes at the deployed 0.50× rung** — i.e. the sibling haircut harness extended
   to three legs, not this one. The 0.11/0.22/0.04/1.20% baseline is *that* harness's output, so the
   §2 baseline I cited belongs to the harness I did not use.
2. **Re-frame the gate as a delta, not an absolute ceiling** — e.g. "does adding 6J degrade any
   partition by more than X pp versus the same-engine baseline?" That is answerable on this engine
   at 1.00×, is reachable, and isolates the leg's contribution instead of inheriting the baseline's
   failure. **This is the cheaper and more informative of the two.**

**Neither is authored here.** Choosing between them is an operator decision, and after two voids in
this family the next artifact should be adversarially reviewed before it is signed.

## §5 — Also recorded

- **C2 crashed after the verdict**, in `breadth_declaration` → `participation_ratio` →
  `np.linalg.eigvalsh` (`Eigenvalues did not converge`): an all-zero column has **zero variance**, so
  the correlation step divides by zero (`c /= stddev[None, :]`) and the eigensolver receives NaNs.
  **Benign and control-specific** — the crash is at line 343, *after* `compose_verdict_4tier` at 342,
  so the partition artifacts were already written and are the numbers reported in §1. A real
  variance-bearing column would not hit it. Worth knowing: the engine's breadth diagnostic is
  undefined for a degenerate leg, so any future all-zero control on it will fail the same way.
- **C1 remains GREEN and re-usable** ([record](../../../lab/analysis/aegis/aegis_6j_trail_tradeify_2026-07-29/C1_CONTROL.md)) —
  engine equivalence is established and survives this closure.
- **Single-tier restriction worked as intended** (~76 min → the C2 run reached the verdict well
  inside that), and the pre-registered warning that the engine's aggregate `VERDICT` string is
  uninterpretable at `n_tiers = 1` held.

## §6 — Disposition

**D2 (Aegis-6J) remains PARKED, unchanged.** Nothing was measured about the leg, so nothing moved.
The composed question is **re-openable but not re-opened**. Nothing armed; no `core/`, allocation,
`dd_protection`, Pine, rung, or rail byte touched.
