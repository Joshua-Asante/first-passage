# Q-POLFRONT-1 — policy-augmented seed-target frontier (bust-axis)

**Status:** `OPEN — DRAFT` (commissioned by the [P2 mark](closures/STATE-POLICY-closure-resolved-p2.md); run gated on operator GO)
**Authored:** 2026-08-16 · Claude Code (JA commission)
**Type:** Inquire-phase measurement brief — $0 · K=0 · no manifest · no candidate · no deployment surface
**Parent findings:** [Q-EVALSEQ-1 closure §3](closures/Q-EVALSEQ-1-closure-falsified.md) (cushion-proportional sizing: bust 20.18%→0.00% both halves at 1.06pt of pass, on the book instrument) · [seed-target frontier](../lab/analysis/c1/tradeify_seed_target_spec_2026-08-04/RESULTS.md) (constant-R admissibility cells)
**Feeds:** deep-iteration lane **GO-1** ([charter](../adr/2026-08-16-deep-iteration-lane-charter.md)) — the first lane prereg freezes only after this measurement lands.

---

## §0 — Rule-0 reads (this session @ `a7c6f7b`)

| Path | Supplies |
|---|---|
| [`lab/analysis/c1/tradeify_seed_target_spec_2026-08-04/RESULTS.md`](../lab/analysis/c1/tradeify_seed_target_spec_2026-08-04/RESULTS.md) | The baseline instrument: `(w, b, r, k, d)` cells scored against the ratified gate (`eval_bust_ceiling 0.03 · pass_floor 0.50 · horizon 1500 · inactivity disabled`), engine cross-checked to `core/mc/simulation.py` at 0.000pp; constant-R cells: max risk $350–$425 at the 3.0% ceiling; admissibility to ~+0.10R |
| [`lab/analysis/c1/q_evalseq_1_2026-08/RESULTS.md`](../lab/analysis/c1/q_evalseq_1_2026-08/RESULTS.md) | The measured policy and its three disclosed bounds (EOD clock; integer-floor abstraction; in-panel tails) |
| [`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) | The frozen floors this measurement is denominated in — **byte-untouched by this brief** |
| [`core/dd_protection.py`](../../core/dd_protection.py) | Axis-separation: a policy is a risk_pct-layer multiplier; no constant is edited |

## §1 — Context

Every seed-frontier number is constant-R. Q-EVALSEQ-1 measured (on the barred book, EOD clock)
that cushion-proportional sizing removes essentially all trailing-DD bust at ~1pt of pass cost.
If that carries to synthetic seed geometry, the admissible region for **candidates** widens:
a cell that busts >3.0% at constant R may clear at the same R under the policy — or clear at a
**larger** R, which is more daily μ per unit of edge, which is faster passes and looser edge
floors. This is candidate-independent geometry, the direct input the deep-iteration lane's
family selection (GO-1) needs.

## §3 — Question (symptom-only)

The admission frontier is measured only for constant-R sizing while the one measured
state-dependent policy dominates the survival axis on its test instrument; what does the
frontier look like with the policy layer on?

## §4 — Falsifiable hypothesis

**H:** on the seed-target instrument at the frozen floors (bust ≤ 3.0% ∧ P(pass) ≥ 50%),
the policy-augmented max admissible base-R exceeds the constant-R max by **≥ 1.25×
(median across the frozen cell grid)** with pass-floor still met in every counted cell.
**Falsified** (lever immaterial for admission) if the median ratio < 1.10× or the pass floor
fails in ≥ half the cells where bust headroom appears. **Ambiguous** if the quantized arm
(integer floors) reverses the headline direction — then the abstraction, not the lever, is the
finding.

## §5 — Forbidden moves

- Running before operator GO on this brief; editing any frozen floor or dd_protection constant.
- Adding policy shapes beyond the two frozen arms (§6) — shape search happened in Q-EVALSEQ-1
  and was priced there; this brief measures the carried winner, it does not search.
- Reading any cell as an admission, a candidate, or a WATCH-rung change.
- Citing results against the 3.0% ceiling's level — this measurement is denominated *in* it.
- Skipping the quantized arm or the intraday-sensitivity arm (§6 disclosures are mandatory).

## §6 — Gate (frozen)

- **Arms (2, fixed):** (i) constant-R control (the existing frontier, re-run same-seed for
  comparability); (ii) policy `P_c`: risk_t = R · min(1, cushion_t / 3000), the Q-EVALSEQ-1
  winner generalized to cell geometry with cap 1.0 (the 0.75 cap was book-family-specific;
  the cap change is declared here, pre-run, not fitted).
- **Grid (frozen):** the seed-target spec's §2/§4 cell set (its (w, b) pairs × k ∈ {1, 2, 4}),
  unchanged — no new cells.
- **Outputs:** per-cell R_max^flat, R_max^policy, ratio; median ratio headline; per-cell pass%
  at R_max; two mandatory disclosure arms — **quantized** (1-micro floor at a stated $/R) and
  **intraday-sensitivity** (worst-day-doubled stress, labeled exploratory).
- **Verdict:** RESOLVED-QUANTIFIED (H holds) / FALSIFIED-IMMATERIAL / AMBIGUOUS-ABSTRACTION,
  per §4. Any verdict feeds GO-1; none admits anything.

## §7 — Forks (named, not opened)

- Funded-phase policy inheritance — stays with Q-FUNDPOL-1 (b5, renewed to 2027-02-08).
- Policy adoption for any *actual* candidate — its own governance chain (dd_geometry-class
  admission + both-halves + ADR), untouched here.

## §8 — Verdict pre-registration

No separate file; §4/§6 above are frozen at this brief's commit (Trap #12 — no amendment to
match a later read; a change closes this brief and opens a fresh one).

## §10 — Audit hooks

```bash
grep -n "eval_bust_ceiling = 0.03" lab/discovery/prop_survivor_scoring.py || grep -rn "eval_bust_ceiling" lab/discovery/
grep -n "DD_TRIGGER = 0.015" core/dd_protection.py          # untouched by any run
ls lab/analysis/c1/q_polfront_1_2026-08/ 2>/dev/null || echo "camp not scaffolded (pre-GO state)"
```
