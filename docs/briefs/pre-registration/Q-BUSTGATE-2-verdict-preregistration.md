# Q-BUSTGATE-2 — Verdict pre-registration (H-BUSTGATE-2)

**Frozen:** 2026-08-15, ahead of Phase 3 execution. **Two adversarial stress-test rounds ran against this spec before any candidate-specific number was read** (workflow `wf_5013860c-86a`, phase "Ceiling pre-registration") — the tightenings each round required are already incorporated below; this is the post-tightening frozen text, not the initial draft. No revision after this point is legal without a fresh freeze (Trap #12 / Known Trap #12).

---

## §A — Pinned inputs

| Input | Value | Source |
|---|---|---|
| First-attempt fee (NEW) | $159 (promo code AUG, binds until **2026-08-31 23:59 EST**) / $265 list | `docs/notes/2026-08-13-tradeify-select-100k-checkout-price.md:23,48` |
| First-attempt fee (OLD, for comparison) | $111 promo / $181 list | `lab/analysis/c1/q_rail_1_2026-07/PHASE4.md:35` |
| Reset fee (NEW) | $169 | `docs/notes/2026-08-13-tradeify-select-100k-checkout-price.md:28,49` |
| Reset fee (OLD, for comparison) | $239 | `lab/analysis/c1/q_rail_1_2026-07/PHASE4.md:37` |
| Activation fee | $0 (both vintages) | same sources |
| Retry horizon N | **3** (frozen) — population-disclosed median evals-per-participant | `docs/notes/notice/N-2026-08-13-external-eval-population-data.md:19` ("initiated a median of 3 each") — a **behavioral budget bound**, not a probability substitution |
| Unselected-population per-attempt pass rate | 17.2% (Tradeify, Aug25–Jul26) | same, `:19,25` |
| Credibility-margin floor | **51.6%** (= 3.0 × 17.2%) — pinned, not a judgment call at read time | round multiple in the spirit of the incumbent 3.0% ceiling's own bracketing between 1% and 17.70% (`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md:139-145`) |
| Admissible rung set | **{0.50×} only** | inherited, not re-derived: `docs/adr/2026-07-23-c1-rung-selection-ev-objective.md:43,45` — the both-halves regime-robustness gate already ran; 1.00× FAILS (regime-fragile), 0.50× PASSES all four partitions. This precondition is **not overridden by EV** under the already-ratified ADR. No optimization over rung is performed by this artifact — the set has exactly one member. |
| p_bust governing engine, 0.50× rung | **Intraday-honest**, full-panel = **0.72%** | `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md:27` — per CLAUDE.md's own posture, EOD-clock bust figures are lower bounds unless they cite an intraday-honest RESULTS path; this is that path, pre-specified now, not chosen at execution time. |
| p_bust, 1.00× rung (reported for Thread 1 only — NOT an admissible-set member) | 6.78% (H1, corrected-EOD) | `docs/briefs/closures/Q-BUSTGATE-1-closure-falsified.md:13` (2026-08-06 correction banner). **No intraday-honest full remeasure exists for 1.00× at execution time** — only a reduced-horizon non-vacuity guard exists (2.50% EOD → 32.33% intraday-honest at that horizon), so any 1.00×-rung reading in this artifact is flagged an EOD lower bound, consistent with CLAUDE.md's standing caveat, and is **descriptive context only** (Thread 1), never load-bearing for the §4 decision. |
| V_payout | **Not sourced** — no primary Tradeify payout-split disclosure is among this pre-registration's named input set. **Hard precondition, not a placeholder**: no absolute-dollar EV_N may be computed until a specific primary disclosure (page/tier/gross-vs-net-of-split) is named. Cost-side-only comparisons (fee schedule vs. fee schedule, at fixed p) do not require V_payout and are licensed under §B below. |

## §B — Frozen EV model (cost-side, licensed for execution without V_payout)

Bounded-retry expected cost per pass-cycle, horizon N=3, per-attempt bust probability p (iid):

```
E[C] = w1*C1 + w2*C2 + (w3 + w_fail)*C3
  where w1 = (1-p), w2 = (1-p)*p, w3 = (1-p)*p^2, w_fail = p^3
  C1 = first-attempt fee; C2 = C1 + reset; C3 = C1 + 2*reset
```

Full absolute-dollar EV_N (payout-inclusive) is defined but **not executable** under this freeze absent V_payout:

```
EV_N = sum_{k=1..N} (1-p)*p^(k-1) * [V_payout*(1-delta_consistency) - C_k]  -  p^N * C_N
```

`delta_consistency` — payout-timing/dilution discount from the 40%-at-eval consistency rule (`N-2026-08-13-external-eval-population-data.md:67`: "a withdrawal gate, not a survival gate... attacks P(payout) invisibly"). Enters V_payout realization only, never p_bust.

## §C — Estimand-mismatch firewall (hard constraint, unchanged from draft)

The population conversion chain (17.2% per-attempt / 40.3% per-participant / 28.5% funded→payout) measures discretionary retail humans with no validated edge — a different estimand from p_bust, which is sourced exclusively from the candidate's own MC. Population figures enter this model **only** as N (behavioral bound, §A) and the §D credibility precondition — never substituted for p_bust or the 50% pass floor.

## §D — Decision rule (binary, no free tolerance parameter)

**Precondition (credibility gate, non-vacuity pre-verified):** the admissible rung's own MC per-attempt pass rate must exceed 51.6% (§A). Non-vacuity check performed at freeze time, not execution time: 0.50×'s own EOD pass-5th (95.76%, `docs/adr/2026-07-23-c1-rung-selection-ev-objective.md:29` — flagged `⛔ SUPERSEDED` banner at its source `RESULTS.md`; no corrected pass-5th is published anywhere in that campaign as of this freeze, so this specific figure is cited with its supersession caveat attached, not as clean) clears; ORB-MNQ's P(pass) 32.33%/22.99%/19.82% at k=1/2/3 (`docs/rejected_candidates.md:622`) fails the same margin — the gate is not vacuous.

- **`RESOLVED`** — the sole admissible rung's p_bust ≤ 3.0%.
- **`FALSIFIED`** — the sole admissible rung's p_bust > 3.0%.
- **`AMBIGUOUS-HOLD`** — the admissible set is empty (regime gate fails all ladder rungs), or the credibility precondition fails.

**No disposition may write a new ceiling number.** Both RESOLVED and FALSIFIED leave 3.0% byte-unedited; only a superseding ADR — never this artifact — can change it. This mirrors Q-BUSTGATE-1's own §5 forbidden move ("treating the EV-optimum as itself 'the new ceiling'... conflates two instruments").

**Pinned ex-ante expectation (discipline check — a surprise-if-wrong marker, per Q-BUSTGATE-1's own §E pattern):** given the admissible set collapses to a single member (0.50×) whose intraday-honest bust (0.72%) is already an order of magnitude inside 3.0%, the expected outcome of this freeze is **RESOLVED**, trivially, by construction of the already-ratified regime-robustness precondition — not because this artifact discovers anything new about economics. A `FALSIFIED` or `AMBIGUOUS-HOLD` outcome would be the genuine surprise (e.g., if the intraday-honest remeasure for the admissible rung had moved materially, or if the regime gate's own admissible set had changed since 2026-07-23) and should be treated as evidence something upstream shifted, not as this model finding new information.

**Thread 1 (context only, not decision-governing):** the unconstrained EV/dollar-day objective (Q-BUSTGATE-1's original framing, ignoring the regime-admissibility precondition) is computed separately at execution time, using §B's cost-side formula, purely to show whether the 2026-08-13 fee update narrows or widens the fee/upside asymmetry Q-BUSTGATE-1 found (≈12–36:1). This thread **cannot fire §D** — it is explicitly out-of-scope for the decision rule, reported for continuity with the prior brief only.

## §E — Re-litigation cap (SNAG-style budget, new — required by stress-test round 2)

This is the **second and, absent a materially new input class, final** re-derivation of the Part-A bust ceiling under an economic objective (Q-BUSTGATE-1 was the first). If this freeze resolves RESOLVED or FALSIFIED and a third re-derivation is proposed on the basis of a further price-page or population-data update alone (not a new instrument, not a new venue, not a new mechanism class), it is **out of scope** absent an explicit operator ruling naming what changed structurally since this freeze — mirroring the DJ30 Q-DJ30-1/2/3 SNAG-exhaustion pattern this repo already tracks. A ceiling re-derivation is not a standing invitation to re-ask the same question on every fee-page refresh.

## §F — Forbidden moves

1. In-place edit to the 2026-07-13 prereg (Trap #12).
2. Substituting population pass/payout rates for p_bust or the 50% pass floor (§C).
3. Welding Tradeify's 3.0% Live call-up rate to this ceiling — a fourth, unrelated 3.0% in this lineage (`N-2026-08-13-external-eval-population-data.md:73`: "Do not weld them").
4. Re-scoping into rung-selection — owned by `docs/adr/2026-07-23-c1-rung-selection-ev-objective.md:49`, not this artifact.
5. Computing an absolute-dollar EV_N without a specifically-named primary V_payout disclosure.
6. Letting Thread 1's unconstrained-EV reading override or qualify the §D verdict — Thread 1 is context, never a decision input.
7. Re-opening a third re-derivation absent the §E structural-change condition.

---

**Verification note:** every anchor above was read directly at freeze time from the four sources named in the parent brief's §0 (`docs/briefs/Q-BUSTGATE-2-bust-gate-re-derivation-2026-08.md`); all exist as cited, quotes verbatim. This freeze incorporates the required changes from both stress-test rounds: rung pre-named (no execution-time optimization discretion), credibility margin pinned as a number, two-tier cost formula fixed, engine choice pre-specified per rung with the 1.00×-side lower-bound caveat stated up front, fee-direction framing stated both ways (§A shows both fees moved, one up one down), and a re-litigation cap added (§E).
