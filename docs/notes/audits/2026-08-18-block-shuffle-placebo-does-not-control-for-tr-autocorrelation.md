# Audit Note — block-shuffle placebo does not control for True-Range autocorrelation

**Audit ID:** AUDIT-2026-08-18-tr-placebo-misspecified
**Date:** 2026-08-18
**Triggered by:** unexpected outcome (adversarial review of a claimed SIGNAL)
**Authors:** Joshua (GO) + Claude Code (drafter, adversarial-verify workflow `wf_b2b794d6-380`)
**Scope:** the `daily-range-state-persistence` Tier-1 screen template (`run_s1a.py`/`run_s1b.py`,
shared byte-for-byte) — [Step-0 slate](../../briefs/2026-08-18-step0-daily-geometry-mechanism-slate.md)
rows S1a/S1b, and by direct exposure S2/S3 which were queued to reuse the same battery.
**Lives in:** `docs/notes/audits/2026-08-18-block-shuffle-placebo-does-not-control-for-tr-autocorrelation.md`

---

## §0 — Source anchors

- [`PREREG_S1B.md`](../../../lab/analysis/_inbox/rangestate_mcl_2026-08/PREREG_S1B.md) /
  [`run_s1b.py`](../../../lab/analysis/_inbox/rangestate_mcl_2026-08/run_s1b.py) /
  [`s1b_results.json`](../../../lab/analysis/_inbox/rangestate_mcl_2026-08/s1b_results.json) —
  the run that surfaced the finding.
- [`PREREG_S1A.md`](../../../lab/analysis/_inbox/rangestate_gc_2026-08/PREREG_S1A.md) /
  [`run_s1a.py`](../../../lab/analysis/_inbox/rangestate_gc_2026-08/run_s1a.py) — the sibling
  screen sharing the identical `block_shuffle_conditional_p95` function, retroactively affected.
- Adversarial-verify workflow `wf_b2b794d6-380` (4 lenses + synthesis), full transcript in this
  session's task journal — the placebo-design-skeptic lens is the primary evidence source.

---

## §1 — Trigger

On 2026-08-18, `H-RANGESTATE-CL-1` (S1b, daily True-Range top-quintile persistence on CME crude
oil, train era 2010–2019) returned **SIGNAL** — the mechanism program's first — clearing all
four frozen limbs including its placebo decisively (p=0.0005). Given SIGNAL is the highest-stakes
outcome type (a false positive could seed a K-costly lane campaign on a phantom mechanism), a
heavier adversarial-verify workflow was launched before trusting the result, including a lens
specifically hunting for null-misspecification rather than code defects. That lens found the
placebo itself does not test what the pre-registration claimed it tested.

**Failure class:** Methodology failure — a discipline check (the placebo limb) fired and
appeared to pass, but the null it was built against does not isolate the claimed effect from an
adjacent, mundane one.

---

## §2 — What actually happened

1. `run_s1a.py`'s frozen battery (four limbs: n-floor, 60-day circular block-bootstrap CI,
   both-halves, 60-day contiguous-block placebo) was designed for `H-DSTRUCT-MNQ-1` (a
   *directional* bias-matches-outcome test) and reused, parameter-identical, for
   `H-RANGESTATE-GC-1`/`-CL-1` (a *magnitude-conditioning* test: does top-quintile True Range
   predict tomorrow's elevated True Range).
2. S1a (GC) returned NULL (CI limb failed) but its placebo limb passed (p=0.0095) — read at the
   time as partial corroboration ("three of four limbs pass... the placebo answers 'does
   temporal order matter'", `RESULTS_S1A.md` §3, now corrected).
3. S1b (CL) returned SIGNAL, all four limbs clearing, gateHit 0.6282, placebo p=0.0005.
4. The adversarial-verify workflow's placebo-design-skeptic lens measured CL's own True-Range
   lag-1 autocorrelation directly (log-TR ρ₁ = 0.4520 — ordinary, textbook GARCH-type
   persistence, nothing unusual for a commodity) and then fed 20 independent synthetic AR(1)
   series — calibrated *only* to that single autocorrelation coefficient, with **zero** real
   day-ahead directional mechanism by construction — through the identical frozen pipeline.
   **20 of 20 surrogates cleared both the CI limb and the placebo limb**, with a mean conditional
   hit rate of 0.75 (range 0.72–0.80) — *higher* than CL's real observed 0.6282. A closed-form
   AR(1)/Gaussian-copula calculation and a naive in-sample quintile/median split independently
   predicted 0.75–0.77 for the same reason. The real result did not exceed what plain
   autocorrelation predicts; it undershot it.
5. The same lens diagnosed the mechanism: the placebo permutes *which calendar positions* carry
   `bias=1` while holding the outcome sequence `y` fixed. Since `y` is itself derived from `TR`,
   and `TR` is genuinely autocorrelated, the *unshuffled* (real) bias days are mechanically more
   likely to sit where `TR` is already elevated — predicting tomorrow's outcome via nothing more
   than ordinary short-lag persistence. Shuffling the bias-block *order* does not break this,
   because the null still measures "conditional rate given `bias=1`" against a `y` sequence that
   carries its own un-shuffled autocorrelation.
6. Separately (regime-concentration lens, same workflow): the pooled SIGNAL evaporates when the
   2011/2014/2016 crisis-adjacent years are removed as a cluster (CI lower bound drops below
   0.50, placebo p weakens 50× to 0.0265), and a clean crisis-vs-calm year split shows the calm
   bucket alone is an independent NULL failing *both* the CI and placebo limbs on its own. This
   is a second, independent line of evidence pointing at the same root cause: crisis-transition
   episodes are exactly where short-lag TR autocorrelation is most acute.
7. Synthesis verdict: **NOT-CONFIRMED**. Not "SIGNAL with caveats" — a result that (a) fails its
   own regime-concentration test and (b) is *smaller* than its own mechanism-free autocorrelation
   baseline is not distinguishable from noise dressed as persistence.

---

## §3 — Discipline checks that should have caught it

| Check | Should have caught | Actual behavior |
|---|---|---|
| §2 Falsifiable hypothesis | Partially — the frozen claim (§2 of both preregs) named "exceeds its block-shuffled null" as the test, without separately stating the null must preserve the outcome series's own autocorrelation structure | The hypothesis was falsifiable but the **operationalization** of "exceeds the null" was the defect, not the hypothesis statement itself |
| §6 Audit hooks runnable | N/A — this is a design-validity question, not a reproducibility question | — |
| `strategy-validation` §5 Null hygiene ("name the null explicitly... permutation drift-handling") | **Yes — this is exactly the documented failure mode.** The skill's own text: *"Leave drift in a long-only-on-a-trending-series test and it beats its permutations by being long — the honest null includes the unconditional drift... This is the most common way a permutation flatters a strategy."* This screen's failure is the volatility-analogue of that exact warning: "leave autocorrelation in an autocorrelated-series test and it beats its permutations by being autocorrelated." | **Missed at design time** — the skill's drift-handling warning was read (it informed the base-rate-matched placebo design used earlier in the same program for `H-DSTRUCT-MNQ-1`/`Q-WLEGB-1`, which *does* correctly neutralize a directional base-rate confound), but its generalization to a *magnitude/persistence* claim on an *autocorrelated continuous series* was not made. The lesson was applied to the family of test it was written for (directional bias vs. a skewed marginal) and not re-derived for a structurally different family (conditioning on one point of a persistent process to predict a nearby point of the same process) |

The check that fired correctly was the **adversarial-verify workflow itself** — specifically the
decision to scope a dedicated "placebo-design skeptic" lens for a SIGNAL result, per this
session's own stated reasoning that "the asymmetry cuts hard against under-scrutinizing" a
positive finding. That discipline is what caught this before it reached a ledger's "resolved"
state or a lane-campaign K spend.

---

## §4 — Root cause analysis

- **Immediate cause:** the placebo null (permute bias-block order, hold outcome fixed) does not
  preserve the outcome series's own short-lag autocorrelation, so it under-corrects for
  ordinary volatility clustering.
- **Contributing factor:** the four-limb battery was designed once (for `H-DSTRUCT-MNQ-1`, a
  *directional* claim on a series whose relevant confound was a skewed base rate, not
  autocorrelation) and then reused verbatim for a *different claim family* (persistence of a
  continuous, autocorrelated magnitude) without re-deriving whether the same null construction
  remains valid for the new claim shape. "Reuse the frozen battery" is good discipline against
  p-hacking (no per-screen null-shopping) but was applied one level too generically here — the
  *battery* was frozen, but the battery's own fitness for a new claim family was never itself
  gated.
- **Structural cause:** there is no standing rule requiring a new claim family (as opposed to a
  new instrument replicating an existing claim family) to re-justify its null construction
  against the *specific* confound that family is exposed to. `strategy-validation` §5's drift
  warning exists but is stated for directional/base-rate confounds; it has no explicit
  extension to autocorrelation/persistence confounds on continuous series. This is the
  load-bearing repair target.

---

## §5 — Repair plan

### Immediate

- [x] S1b re-verdicted `NOT-CONFIRMED` (not SIGNAL) in `RESULTS_S1B.md`.
- [x] S1a's `RESULTS_S1A.md` §3 ("why this is a defensible NULL") corrected — the placebo pass
  is no longer citable as independent corroboration; overall verdict (NULL) is unchanged since
  it already failed on the CI limb independent of this defect.
- [x] `MECHANISMS.md`'s `daily-range-state-persistence` heading corrected — both class findings
  now state the test itself is invalidated pending a corrected null, not that the mechanism is
  measured-and-absent.
- [x] `MGC.md` G4 and the new `MCL.md` row corrected to match.
- [x] Step-0 slate S2/S3 **paused** — both were queued to reuse the identical placebo
  construction; running them before a fix would repeat the defect at $0 cost each time but
  compound the false-confidence risk.

### Structural

- [x] **Design a corrected null** — DONE 2026-08-18, same day, with its own scrutiny (not a
  same-session patch in the improvised sense): 4-lens design panel + synthesis
  (`wf_ebc728eb-2ef`), frozen spec
  [`2026-08-18-magnitude-persistence-corrected-null-battery.md`](../../spec/2026-08-18-magnitude-persistence-corrected-null-battery.md)
  (IAAFT normal-scores surrogates — NOT the AR(1)/GARCH parametric option this note originally
  floated: AR(1) was measured a strawman, +13pp band displacement; presence-gates/
  attribution-types wiring; NEW L4 by-year regime limb), 4-lens pre-official verification with
  bit-exact independent reimplementation (`wf_e06ebc90-c3e`), pilot→ADDENDUM-1→operator
  PROCEED→official run. Official outcomes: S1a NULL (L2+L4; near-miss dissolved, 8.4th pct of
  own band); S1b SIGNAL-GENERIC (canon-attributed; guard-railed).
- [x] `strategy-validation` §5 clause — landed 2026-08-18 (repo copy, authoring path).
- [x] `futures-anomaly-discovery` battery-reuse-per-claim-family note — landed 2026-08-18.

---

## §6 — Lessons to capture

- **Candidate lesson:** *"A block-shuffle placebo that holds the outcome series fixed only
  controls for a directional/base-rate confound; on a magnitude-persistence claim over an
  autocorrelated continuous series, the correct null must itself be autocorrelation-matched
  (AR/GARCH surrogate), or a zero-mechanism series with the outcome's own ACF will clear the
  same battery."*
  - Anchor: this audit — AR(1) surrogates calibrated to CL's own ρ₁=0.4520 cleared the
    battery at a *higher* rate (0.75–0.80) than the real data (0.6282), across 20/20 trials.
  - Counterfactual cost: would have discharged `MCL.md`'s "mechanism-owed" ledger status and
    licensed a K-spending deep-iteration-lane prereg on an artifact.
  - Lesson registry destination: `docs/methodology/references/statistics-of-tradable-anomalies.md`
    Domain 3 (permutation/null design) or a new `lesson_block_shuffle_needs_acf_match.md`
    memory entry.
  - Promotion status: single strong firing with a decisive, quantified counterfactual (20/20
    surrogates, closed-form cross-check) — meets the E1/E2 "structural-argument approval" bar
    without needing repeat firings.

---

## §7 — Programme-audit signal check

- [x] Belt-patches without independent corroboration? — No; caught by independent adversarial
  review, not patched over.
- [ ] Belt that only grows, never prunes? — No.
- [ ] Falsifier thresholds drifting toward "we'd never hit this"? — No.
- [ ] Methodology invoked to rationalize a decision already made? — No; the opposite — the
  workflow was scoped *because* the result was exciting, specifically to counteract that.
- [ ] SNAG pattern? — No, single thread.
- [ ] Cross-layer contamination? — No.
- [x] Negative heuristic crossed without repair? — Borderline: the battery was reused across
  claim families without re-validating null fitness (§4). Repaired here (paused S2/S3, corrected
  records); structural fix (§5) still owed before the next screen of this shape.

No escalation to a full programme-audit needed — single-thread, immediately contained.

---

## §10 — Audit hooks

```bash
# Any future daily-range-state-persistence (or sibling magnitude-persistence) screen must cite
# a corrected/ACF-matched null before its placebo limb can be trusted:
grep -rn "block_shuffle_conditional_p95\|AR.*surrogate\|GARCH.*surrogate" \
  lab/analysis/_inbox/*/run_*.py ops/instruments/MECHANISMS.md
# Expected: any new run_*.py reusing block_shuffle_conditional_p95 on a magnitude-persistence
# claim names this audit and its own ACF-validity check in its prereg §0.

# S2/S3 pause is lifted only after a structural fix lands:
grep -n "PAUSED\|AUDIT-2026-08-18-tr-placebo" \
  docs/briefs/2026-08-18-step0-daily-geometry-mechanism-slate.md
```

---

## §11 — Closure

- **Status:** `Closed (immediate + structural complete)` — 2026-08-18, same day
- **Immediate repair completed:** 2026-08-18
- **Structural repair completed:** 2026-08-18 (corrected battery designed via its own 4-lens
  panel, frozen, verified bit-exact, run officially on operator PROCEED; both skill clauses
  landed — see §5). One structural item transferred forward rather than closed here: S2's
  cross-series null remains UNRESOLVED-NEEDS-DESIGN (spec §4 / O1) and S2 stays paused behind
  its stage-1 cheap falsifier.
- **Lessons graduated to standing rule:** the autocorrelation-confound clause is now standing
  text in `strategy-validation` §5 (the memory lesson `lesson_block_shuffle_needs_acf_match`
  anchors it)
- **Follow-up audits triggered:** none; S3's un-pause is a design-review condition (matched-day
  prereg), not an audit

---

## Verification

```bash
git log --oneline -1   # anchor commit at authoring
grep -n "NOT-CONFIRMED" lab/analysis/_inbox/rangestate_mcl_2026-08/RESULTS_S1B.md
grep -n "AUDIT-2026-08-18" ops/instruments/MECHANISMS.md ops/instruments/MGC.md \
  ops/instruments/MCL.md docs/briefs/2026-08-18-step0-daily-geometry-mechanism-slate.md
```
