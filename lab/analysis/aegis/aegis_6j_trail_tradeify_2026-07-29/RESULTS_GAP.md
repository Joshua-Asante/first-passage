# RESULTS — closing the survival gap for Aegis→6J

> ## ⛔ NEXT-STEP PRESCRIPTION SUPERSEDED 2026-07-29 (banner 2026-08-05)
>
> The §4/§5 next step — "a pre-registered composed re-MC at constant 0.50× on the frozen
> engine" — was attempted twice and closed VOID the same week. **Q-6JCOMPOSE-1: VOID
> (unexecutable). Q-6JCOMPOSE-2: VOID — C2 RED, gate unreachable by construction** — halving
> `C1_ALLOCS` to reach the 0.50× rung is forbidden by the engine's §5 / Trap #11, and the no-6J
> baseline (H1 4.37%, boot-95th 10.37%) already exceeds the 3.0% ceiling. The two admissible
> replacements are named in
> [`Q-6JCOMPOSE-2` closure](../../../docs/briefs/closures/Q-6JCOMPOSE-2-closure-void-c2-red-gate-unreachable.md) §4;
> each needs a fresh pre-registration + operator GO. The composed question is "re-openable but
> not re-opened" — this engine and this framing are barred, composition itself is not.
> **Separately**, this file's composition target is gone: both Striker legs were withdrawn from
> the c1 eval deployment 2026-08-04, so there is no deployed c1 book and no "$55,206" baseline.
> D2 stays PARKED. Body unedited.


**Date:** 2026-07-29 (later) · **Scripts:** [`commission_breakeven.py`](commission_breakeven.py) ·
[`trail_survival_tradeify.py`](trail_survival_tradeify.py) (imported, not edited)
**Logs:** [`run_breakeven.log`](run_breakeven.log)
**Follows:** [`RESULTS.md`](RESULTS.md) (J4b) · [`RESULTS_R1.md`](RESULTS_R1.md) (J7)

**Headline: the standalone survival objection is RESOLVED at the deployed lifecycle rung — but the
gate that matters is composed bust, which has NOT been run. This is not an admission.**

---

## §1 — The "0.88pp gap" was not a measured gap

J4b's best cell was quoted as 3.88% vs a 3.0% ceiling. That row is the **exhaustive rotation, n=129**
— i.e. **5 breaching paths**, with the PASS/FAIL boundary between 3 and 4 paths:

| row | estimate | 95% CI (Clopper-Pearson) | resolves 3.0%? |
|---|---:|---|---|
| rotation (n=129) | 3.88% | **[1.27%, 8.81%]** | **No — 3.0% is inside** |
| bootstrap L13 (n=10,000) | 5.31% | [4.88%, 5.77%] | yes |
| bootstrap L26 (n=10,000) | 5.00% | [4.58%, 5.45%] | yes |

**The 0.88pp figure is the most optimistic reading of the least precise estimator.** The honest gap
against the trusted-precision rows was **~2.0–2.3pp**. (Bootstrap CIs are Monte-Carlo precision
*conditional on one 129-trade panel*; panel uncertainty is irreducible without more data.)

## §2 — Commission: the only non-selection lever, and it cannot close the gap

Commission is a **venue fact, not a knob** — we look it up, we do not choose it. The J4b matrix
showed the verdict flips on it alone, so the well-posed question is a **break-even**, not a search.
Config **frozen before running** (cap 8, 0.5×-until-freeze, Tradeify geometry); decisive rows
declared as L13 **and** L26 ≤ 3.0%; only commission varies.

| $/side | 3.10 | 2.75 | 2.56 | 2.36 | 2.10 | 1.85 | 1.60 | **1.30** | 1.00 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| L13 | 4.69% | 3.91% | 3.59% | 3.44% | 2.99% | 2.65% | 2.58% | **2.30%** | 1.95% |
| L26 | 5.07% | 4.47% | 4.08% | 3.81% | 3.55% | 3.35% | 3.09% | **2.65%** | 1.94% |
| verdict | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | **PASS** | PASS |

**BREAK-EVEN: ≤ $1.30/side.** Against published full-size 6J rate cards:

| venue | $/side | verdict |
|---|---:|---|
| Tradeify (registered) | 3.10 | fails |
| MFFU | 2.56 | fails |
| Bulenox (Sept-2024, stale) | 2.36 | fails |
| *panel placeholder — not a real card* | *1.30* | *clears* |

**No friendly firm clears it, and the requirement is ~45% below the cheapest published card.** The
gap is not a negotiation gap. **Venue shopping cannot close it.** (Note the only value that clears
is the panel's own placeholder — a reminder that the original J4 "PASS-adjacent" reading was an
artifact of an unpriced input.)

## §3 — The lifecycle ladder: J4's matrix never contained the configuration a c1 leg would use

The lifecycle multiplier is a **constant** risk_pct haircut (`AUTHORIZED 1.00× / WATCH-1 0.50× /
WATCH-2 0.25×`). Testing all three is **exhaustive over a pre-existing discrete set**, not a search.

| rung | panel net | rotation | L13 | L26 | eval pass | consistency-OK @ pass |
|---|---:|---:|---:|---:|---:|---:|
| 1.00× | $23,701 | 12.40% | 10.79% | 14.66% | 89.30% | 83.5% |
| **0.50× (WATCH-1 — the deployed c1 rung)** | **$11,851** | **0.00%** | **0.67%** | **0.77%** | **97.46%** | **100.00%** |
| 0.25× (WATCH-2) | $5,925 | 0.00% | 0.01% | 0.00% | 53.92% | — |

**Constant 0.50× clears the 3.0% ceiling by ~4×, with the 40% consistency rule satisfied on 100% of
passing paths.**

**Root cause — a framing error in J4b, mine.** J4's arm (b) is **"0.5× until floor-freeze, then FULL
size"** — a *Bulenox ramp-up tactic*, not a lifecycle haircut. It reverts to full size once the floor
locks at start+$100, and **post-freeze full-size drawdowns are what generate its breaches** (4.69%
vs 0.67% for the constant rung, same panel, same costs, same geometry). I inherited J4's two arms
and reported the ramp as "the best achievable sizing" without asking whether it was the
configuration a **c1 book leg** would actually run at. It is not: every deployed c1 leg runs a
constant lifecycle multiplier, currently **WATCH-1 0.50×**.

**0.25× is not the answer and shows the ladder is not degenerate.** It drives breach to ~0 but panel
net **$5,925 falls below the $6,000 eval target**, collapsing eval pass to 53.92%. Survival bought
by making the leg unable to pass. That 0.50× satisfies *both* survival and economics — and is
simultaneously the already-deployed rung — is what makes it a principled configuration rather than
a fitted one.

## §4 — What this does NOT establish

**A standalone PASS is not book admission, and this repo has the scar to prove it.** Q-COMPOSE-1:
the 2-leg book busts **2.65%**; adding ORB@0.37% took it to **38.75%**. ORB's standalone behaviour
was never the problem — **composition was**. The ratified gate is composed bust on the frozen
engine, across all four partitions.

Everything below remains open:

1. **Composed re-MC not run.** The decisive test. Needs the frozen engine + a pre-registration,
   and it is the only thing that can convert this into an admission.
2. **New arm outside the frozen J4 matrix.** The constant-rung arm is justified *doctrinally*
   (it is the deployed rung), not empirically. It is declared here as a new arm, not smuggled in.
3. **S2** still excludes 6J by text (non-micro). Its E5 rationale is weak for this candidate
   (see [`RESULTS_R1.md`](RESULTS_R1.md) §5) but moving it is a **§6.1 event and an operator call**.
4. **Cap 8 is inferred**, not verbatim. **Linear cap re-scale**, not a native replay (±2%, F2).
5. **Single 129-trade / 4.5-year panel**; bootstrap reuses its marginals.
6. **Leg economics at 0.50×: $11,851 over 4.5 yr** vs c1 book net $55,206 — material, but the
   deployable-weight composition is what prices it, not this figure.

## §5 — Disposition

**The gap the operator asked to close is closed on the standalone measurement — but by discovering
that the failing configuration was the wrong one, not by shrinking anything to fit.** Commission,
the only legitimate external lever, was tested to break-even and **cannot** close it; the ladder was
tested exhaustively and the deployed rung clears with margin.

**D2 remains PARKED.** Nothing here admits a leg. The next step is a **pre-registered composed
re-MC at constant 0.50×** on the frozen engine — and per §4.2 it should be adversarially reviewed
before it is trusted, precisely because a verdict-flipping arm appeared late and from my own
framing error.

No `core/`, allocation, `dd_protection`, Pine, rung, or rail byte touched. Nothing armed. K unchanged.
