# Prop survivor-scoring pre-registration v2 — Addendum 1: universal ≥4× cost hurdle removed

**Applies to:** `2026-08-26-prop-survivor-scoring-prereg-v2.md`. The v2 file itself is frozen and unchanged.
**Effective:** 2026-10-24T21:01:41Z (recorded timestamp). Prospective only: a run before this time is governed by v2 alone, and its results are unchanged.
**Authority:** Joshua, 2026-10-24: "Approve a dated, prospective addendum removing only the universal ≥4× admission hurdle. Preserve frozen v2 unchanged, and have future runs identify v2 plus the addendum as their governing specification." This follows his [subtraction ruling](../../notes/2026-10-24-assumption-challenge-rulings-proposal.md#operator-ruling-joshua-2026-10-24).

**Removes: G2** — v2's "gross-edge vs ≥4× cost hurdle at `R_deploy`" admission gate. Nothing replaces it: no threshold, and no review step.

**Unchanged:**
- every other v2 requirement: ceilings, tiers, seeds, sims, horizon, G1 and G3 onward;
- candidate-specific net-return estimates and execution-cost sensitivity, which remain part of evaluating each candidate.

**Governing specification for runs from the effective time:** v2 + this addendum. `lab/discovery/prop_survivor_scoring.load_scoring_thresholds()` applies it by default and records both files.
