# Pre-registration — Q-GATECAL-1 (mechanism gate false-negative rate)

**Parent brief:** [`docs/briefs/Q-GATECAL-1-mechanism-gate-false-negative-rate.md`](../Q-GATECAL-1-mechanism-gate-false-negative-rate.md)
**Authored:** 2026-08-29
**Status:** `FROZEN` — no item below changes after this file is committed, or after any Phase 3
candidate result is seen, without closing this pre-registration and opening a fresh one (Known
Trap #12).

Frozen ahead of Phase 1 (`register_search open`) and the stratified draw (Phase 2). Nothing here
may be amended after either runs.

---

## Frozen gate table (verbatim from §6)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | ≥1/8 sampled candidates clears cost-law AND DSR AND decay | `ITERATE` — hand finding to a fresh, separately-scoped ADR; no change to 2-A authorized by this brief. |
| `FALSIFIED` | 0/8 sampled candidates clears all three gates | `STOP` — gate measured clean on this K=8 sample; re-proposal bar is a fresh, separately-registered probe. |
| `AMBIGUOUS-HOLD` | ≥2 of 8 slots UNTESTABLE after one substitution attempt each | `ITERATE` — resolve the reconstruction/data-budget blocker before re-drawing. |

## Frozen thresholds

- **Cost-law:** `cost_R < 0.05` via `scripts/cost_geometry_pregate.py` (equivalent to the
  standing ≥4× cost hurdle).
- **DSR:** `DSR ≥ 0.95` via `lab/research_utils/deflated_sharpe.py`, at the candidate's own
  declared K where one exists in `discovery_manifests/` (else K=1, reported explicitly as
  "no declared K").
- **Decay:** H1 and H2 half-sample expectancy (via `lab/research_utils/selection_tests.py
  halves`) both sign-consistent with the full-sample expectancy, and neither negative. This is
  this probe's own adopted substitute — `docs/methodology/regime_robustness_gate.md` is scoped to
  `dd_protection` risk-constant sweeps, not strategy candidates, and has no turnkey candidate-level
  implementation (Part A unimplemented; Part B not wired to a live MC-usable panel). Disclosed
  here rather than silently borrowed.
- **Overall clear:** all three thresholds met. Overall kill: fails any one.

## Frozen sampling parameters

- **K = 8**, registered via `register_search open --lane blind`, run-id `gatecal_1_2026`.
- **Stratification:** 4 DIRECTION / 2 SIZE / 2 CADENCE, drawn from A1's four-table kill census
  restricted to cell-demonstrated rows only (category-inherited rows excluded).
- **Draw method:** seeded random draw within each stratum; the seed and the frozen frame (row
  list, per-row tag) are recorded in the closure record, not chosen after the frame is seen.
- **Substitution rule:** one redraw per irrecoverable slot within the same stratum; a second
  failure marks that slot UNTESTABLE (counts toward the AMBIGUOUS-HOLD trigger, does not silently
  drop out of the denominator).

## Verification

```bash
git log --oneline docs/briefs/pre-registration/Q-GATECAL-1-verdict-preregistration.md
# Expected: this commit predates any `register_search open --run-id gatecal_1_2026` and any
# cost_geometry_pregate.py / deflated_sharpe.py / selection_tests.py run for this probe.
```
