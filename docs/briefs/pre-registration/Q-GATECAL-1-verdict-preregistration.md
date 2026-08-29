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
| `RESOLVED` | ≥1/8 sampled candidates clears cost-law AND DSR AND decay | `ITERATE — hand the finding (raw count/rate + per-candidate detail) to a fresh, separately-scoped ADR deciding whether/how the relevant screen warrants recalibration: 2-A admission clauses if the clearing candidate is DIRECTION/SIZE, the CADENCE activity-floor screen if it is CADENCE. This brief authorizes no change to either screen itself. Entry packet: this closure's per-candidate table. Re-test window: none required.` |
| `FALSIFIED` | 0/8 sampled candidates clears all three gates | `STOP — mechanism gate measured clean on this K=8 blind-lane sample. Re-proposal bar: a fresh probe needs its own newly registered, larger K — not a re-draw of this sample.` |
| `AMBIGUOUS-HOLD` | ≥2 of 8 slots UNTESTABLE after one substitution attempt each (i.e. fewer than 7/8 produce a verdict) | `ITERATE — return target: resolve the reconstruction/data-budget blocker (larger Databento pull budget, or a fresh amendment relaxing the cell-demonstrated-only frame). Re-test window: next session with the blocker resolved.` |

## Frozen thresholds

- **Cost-law:** `cost_R < 0.05` via `scripts/cost_geometry_pregate.py` (equivalent to the
  standing ≥4× cost hurdle).
- **DSR:** `DSR ≥ 0.95` via `lab/research_utils/deflated_sharpe.py`, at the candidate's own
  declared K where one exists in `discovery_manifests/` (else K=1, reported explicitly as
  "no declared K"). **Disclosed in advance:** `discovery_manifests/` (21 files, checked) contains
  no entry for any DIRECTION/SIZE/CADENCE candidate presently eligible for this draw — K=1 (an
  uncorrected significance test, a materially easier bar than a K-adjusted DSR) is the expected
  outcome for nearly every drawn candidate, not a contingent edge case. A RESOLVED verdict must
  not be read as having passed a K-adjusted test unless the per-candidate table says otherwise.
- **Decay:** H1 and H2 half-sample expectancy (via `lab/research_utils/selection_tests.py
  halves`) both sign-consistent with the full-sample expectancy, and neither negative. This is
  this probe's own adopted substitute — `docs/methodology/regime_robustness_gate.md` is scoped to
  `dd_protection` risk-constant sweeps, not strategy candidates, and has no turnkey candidate-level
  implementation (Part A unimplemented; Part B not wired to a live MC-usable panel). Disclosed
  here rather than silently borrowed.
- **Overall clear:** all three thresholds met. Overall kill: fails any one.

## Frozen sampling parameters

- **K = 8**, registered via `register_search open --lane blind`, run-id `gatecal_1_2026`.
- **Stratification:** 5 DIRECTION / 1 SIZE / 2 CADENCE, drawn from A1's four-table kill census
  restricted to cell-demonstrated rows only (category-inherited rows excluded).
- **SIZE stratum is a full census, not a random draw.** A1's cell-demonstrated census carries
  exactly two SIZE-tagged candidates (§3.4 ZC/ZS/ZW grains, §3.5 FGBL). §3.5/FGBL is excluded —
  Eurex-listed, unsourceable by this repo's CME-only data pipeline (`databento-data` skill,
  GLBX.MDP3) — leaving §3.4 as the sole eligible SIZE candidate. Population = draw = 1: zero
  substitution capacity for this stratum (see below). The freed slot moved to DIRECTION.
- **Scope disclosure:** DIRECTION and SIZE strata measure the 2-A four-clause admission gate
  directly (zero-data, ex-ante kills). CADENCE measures a different, downstream, already-computed
  screen (activity-floor failure) — a candidate reaches CADENCE only after surviving 2-A. A
  CADENCE clear does not, by itself, implicate 2-A. See parent brief §1 scope note.
- **Draw method:** seeded random draw within DIRECTION and CADENCE (SIZE is deterministic, see
  above); the seed and the frozen frame (row list, per-row tag) are recorded in the closure
  record, not chosen after the frame is seen.
- **Substitution rule:** one redraw per irrecoverable slot within the same stratum, EXCEPT SIZE
  (population = draw = 1, no spare candidate exists — an irrecoverable SIZE slot goes straight to
  UNTESTABLE with no redraw attempt). For DIRECTION and CADENCE, a second failure after one
  redraw marks that slot UNTESTABLE (counts toward the AMBIGUOUS-HOLD trigger, does not silently
  drop out of the denominator).

## Verification

```bash
git log --oneline docs/briefs/pre-registration/Q-GATECAL-1-verdict-preregistration.md
# Expected: this commit predates any `register_search open --run-id gatecal_1_2026` and any
# cost_geometry_pregate.py / deflated_sharpe.py / selection_tests.py run for this probe.
```
