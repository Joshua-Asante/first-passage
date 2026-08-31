# Q-VOLREGIME-1 — L5 attribution design (Packet B)

**Status:** `DESIGN-DRAFT` — no code has been written or executed against this design. No real
L5 statistic, on either instrument, has been inspected before or during authoring. This document
freezes B2–B4 of
[`docs/superpowers/plans/2026-08-31-q-volregime-next-step.md`](../../../../docs/superpowers/plans/2026-08-31-q-volregime-next-step.md)
and pre-answers B5's six required review questions; it is submitted for adversarial review (B5)
before any pilot code is written.

**Entry gate satisfied:** both MNQ and MYM independently passed Packet A (L3 chronological-halves,
PASS/PASS — [`volregime_l3_2026-08-31/RESULTS.md`](../volregime_l3_2026-08-31/RESULTS.md)). Both
instruments carry forward into this design.

**Authorization boundary (unchanged from the plan doc):** this document specifies the design.
Nothing here authorizes executing it. Packet C (pilot validation of the machinery) and Packet D
(one-shot real execution) each need their own separate operator GO, per the plan doc's own gate
table. Where this design requires a number that can only be produced by touching real data (the
block-permutation length, §4.3), it is specified as a **frozen method**, not a frozen number — the
number itself is computed once, as the first act of Packet C1, not here.

---

## 1. What this replaces, and why

The parent brief's §7 Phase 1 originally instructed adapting `Q-RANGEXFER-1`'s day-level
joint-surrogation null to 1-bar lag. That adaptation is not attempted here, and this design does
not attempt it either. `Q-RANGEXFER-1`'s own day-level design failed on two independent grounds
across four review rounds ([`joint_surrogation_null_2026-08-30/RESULTS.md`](../joint_surrogation_null_2026-08-30/RESULTS.md)):

1. **Model adequacy never cleared** — the long-memory/GARCH candidate models were, at best,
   relatively better than a rejected baseline, never absolutely adequate on their own residual
   diagnostics.
2. **Estimation-aware size control failed** — the surrogate-testing *mechanics* were confirmed
   bug-free, but the positive control that claimed to validate them only exercised
   known-true-parameter behavior. Re-estimating parameters per replicate — the only way the
   procedure can ever run on real data — empirically inflated the null false-positive rate from
   the nominal 5% to 25%.

Both failure modes are specifically parameter-estimation-cost problems: an ARFIMA/GARCH-class
model is expensive enough to fit that the original design could not afford to re-fit it inside
every one of hundreds of null replicates, so it didn't, and that shortcut is exactly what broke
calibration. This design is built to not need that shortcut in the first place — see §3.2's model
choice and §4.4's re-estimation discipline, both selected specifically to stay cheap enough that
full re-estimation per replicate is the default, not an aspiration.

This design also tests a structurally different claim than the day-level design did. Day-level
joint-surrogation modeled two *separate series* (overnight range, gap magnitude) sharing a common
latent day-regime factor. Here there is one series (M15 bars) and the question is whether one
bar's own volume state carries *forward* information for the *next* bar's range beyond what the
trigger bar's own range state, recent history, and calendar position already carry — a forecasting
/ incremental-information question, answerable with a standard nested train/test comparison rather
than a two-series surrogate-generation problem. This is a simpler test for a simpler claim, not a
scaled-down version of the harder one.

---

## 2. Scope and non-goals (carried from the plan doc's §5, restated for this design specifically)

- Scored independently per instrument (MNQ, MYM). No pooling, no cross-instrument inheritance.
- A pass promotes at most a conditioner-role class finding (per D6). It does not license an entry,
  exit, sizing rule, or any Pine/`core/`/`dd_protection`/allocation/rail change.
- No alternate volume quantiles, trailing windows, model families, or loss functions selected
  after seeing real augmented-minus-baseline performance. Every choice below is either frozen now
  or named as an explicit open parameter that Packet C1 freezes before any real data is touched by
  that step.
- The distinct-WHO check (§5 below) types the finding; it does not gate RESOLVED/FALSIFIED.

---

## 3. B2 — Nested forward-prediction comparison

### 3.1 Two comparisons, not one

The parent brief's §4 distinct-WHO requirement ("does the lift survive *additionally* conditioning
on the prior day's own realized-range state") only makes sense as an addition on top of something
narrower. Read literally, the plan doc's B2 baseline bullet list includes prior-day range state
*and* B4 says the distinct-WHO check happens "after adding prior-day range state" — those two
statements are only consistent if there are two comparisons sharing one skeleton, not one. This
document resolves that reading explicitly (flagged for B5's own scrutiny, not silently assumed):

**Comparison 1 — PRIMARY (gates RESOLVED/FALSIFIED):**
- `baseline_1`: time-of-day slot, trigger-bar own-range-elevated indicator (`bias_range`, already
  computed), a fixed set of recent range lags, fixed calendar/session controls.
- `augmented_1`: `baseline_1` + trigger-bar time-of-day-normalized volume state (`bias_volume`,
  already computed) + only those volume lags declared in §3.3.
- This is the primary test of "does volume add incremental forward information beyond intraday
  seasonality and the trigger bar's own range state" — the question H-VOLREGIME-{MNQ,MYM} actually
  asks.

**Comparison 2 — DISTINCT-WHO (disclosed, never gates):**
- `baseline_2`: `baseline_1` + prior trading day's own realized-range state, using
  `daily-range-state-persistence`'s own definition verbatim (prior day's True Range in its own
  trailing top quintile vs. its own trailing median — [`ops/instruments/MECHANISMS.md`](../../../../ops/instruments/MECHANISMS.md)
  `daily-range-state-persistence` heading), not a re-derived threshold.
- `augmented_2`: `baseline_2` + the same volume terms as `augmented_1`.
- Tests whether volume's own increment survives once the sibling single-series mechanism's own
  conditioning variable is also held fixed. Collapse → evidence for "same phenomenon, finer
  grain" (mechanism A); survival → evidence for a genuinely distinct information source
  (mechanism B). Neither outcome changes the Comparison-1 verdict.

Reusing `daily-range-state-persistence`'s own quintile/median convention (rather than inventing a
parallel one) keeps the distinct-WHO check honest about testing *that* mechanism, not a
lookalike.

### 3.2 Model family

**Frozen: L2-regularized logistic regression** (`outcome` is binary — next bar's range elevated or
not, already the exact encoding L1–L4 use). Chosen over a gradient-boosted or other flexible
learner for one load-bearing reason: §4.4 requires the *entire* pipeline — predictable-component
fit, baseline fit, augmented fit, OOS scoring — to re-run inside every null replicate, on the order
of hundreds to a few thousand replicates, on ~136k–140k rows per instrument. A model cheap enough
to fit in well under a second is what makes full re-estimation-per-replicate (D7; the exact
discipline `Q-RANGEXFER-1`'s design could not afford) the default rather than an aspiration this
design also has to compromise on. Regularization strength (`C` in the standard sklearn
parameterization) is a declared open parameter, frozen in Packet C1 by nested cross-validation on
training folds only — never selected against OOS performance.

### 3.3 Feature freeze

- Time-of-day slot: the same `slots = hour*60 + minute` construction `byyear_l4.py` already uses,
  encoded as sine/cosine pair (not raw integer or one-hot, to avoid a coefficient-per-slot blowup
  at 96 slots/day) — a design choice, disclosed for B5 review.
- Recent range lags: **lag-1 through lag-4** raw `bias_range` indicators (already binary; no new
  computation). Declared now, not tuned after seeing results, per D2's own "do not invent a new
  threshold after seeing results" discipline extended here to lag count.
- Volume lags for `augmented_1`/`augmented_2`: **lag-0 (trigger bar) only.** No additional volume
  lags are added — B2's "only those volume lags declared before the pilot" is satisfied by
  declaring zero beyond lag-0, since the parent brief's own H-VOLREGIME hypothesis is about the
  trigger bar's own volume state, not a volume-lag structure nobody has hypothesized. Any future
  volume-lag extension is a new design, not a retune of this one.
- Calendar/session controls: day-of-week (categorical) and RTH-vs-overnight session flag (binary,
  reusing whatever session boundary `byyear_l4.py`'s own trading-day construction already implies).
- No feature is added or removed based on a training-fold coefficient, a validation-fold score, or
  any other data-dependent selection — the feature set above is complete and frozen.

### 3.4 Rolling folds: purge and embargo, not a bare walk-forward

A plain walk-forward split leaks in exactly the way B5's review question 2 asks about: a
time-of-day / volume-threshold trailing statistic computed over "all data up to fold boundary"
can still smear information across the boundary if the boundary falls inside a trailing window
that also touches test-fold bars, or if a fold's early rows sit inside another fold's trailing
lookback. This design uses **purged, embargoed rolling folds**, following the purge+embargo
discipline this repo's methodology already names for exactly this failure mode
(`skfolio.model_selection.CombinatorialPurgedCV`, cited in `strategy-validation` skill §8c) even
though this is a walk-forward, not combinatorial, split:

- **Expanding-window training, fixed-length test blocks.** Training data for fold *k* is every bar
  before that fold's test block; test blocks are contiguous, non-overlapping, and chronologically
  ordered (no CPCV-style path shuffling — the forward-prediction claim is inherently
  chronological, and combinatorial path generation would relitigate an already-settled
  chronological-order question this construct's own L3 already froze).
- **Purge:** drop training rows whose own trailing-lookback window (the longest of the
  predictable-component window, §4.2, and the range-lag window, §3.3) overlaps the test block's
  span, so no training row's own features were computed using any test-block bar.
- **Embargo:** drop training rows in a fixed window immediately following each test block, sized
  to at least the longest lag/window in the design (so serial dependence across the boundary
  doesn't let a test-adjacent training row leak test-period signal back into the next fold's
  training set).
- **Warm-up:** the first `window` bars per instrument (matching L1–L4's own trailing-lookback
  requirement — 60 same-slot occurrences for MNQ, 20 for MYM, already the frozen values in
  `docs/briefs/pre-registration/Q-VOLREGIME-1-verdict-preregistration.md` §A/§F.1) produce no
  scored rows in any fold, exactly as L1–L4 already exclude them.
- **Fold count and test-block length** are declared open parameters, to be frozen in Packet C1
  before any real OOS score is computed — not tuned against real performance once seen. A
  reasonable a-priori range (5–10 folds, test-block length on the order of one quarter to one
  half-year, given ~6 years of data per instrument) is noted for Packet C1's own freeze, not
  adopted here as the frozen value.

---

## 4. B3/B4 — Primary statistic, dependence treatment, attribution null

### 4.1 Primary statistic

**Frozen: mean out-of-fold Brier score improvement**, `improvement = Brier(baseline) −
Brier(augmented)`, averaged across all test folds (equal fold weighting, not sample-size
weighting — a declared choice, since unequal calendar coverage per fold should not let one dense
fold dominate). Brier is chosen over log loss because it is bounded ([0, 1] per prediction) and
does not blow up on a near-certain wrong prediction the way log loss can on a rare, poorly
calibrated tail bar — a property that matters more here than log loss's sharper penalty on
confident errors, given this design has not separately validated calibration robustness in the
tails. `improvement > 0` favors the augmented (volume-including) model.

**Companion (unchanged, already computed):** the existing minimum within-own-range-stratum lift
from L1–L3, reported alongside, not recomputed.

### 4.2 Predictable-volume-component estimator (reused, not reinvented)

The "predictable component" of trigger-bar volume that §4.3's null needs to residualize against
is **the existing frozen `tod_threshold` trailing same-slot-median construction**
(`byyear_l4.py::tod_threshold`, already reviewed and in production for L1–L4), computed using
strictly-prior, training-fold-only data — not a new model. Residual = observed volume − this
threshold (matching the sign convention `bias_volume`'s own ratio-vs-threshold comparison already
uses). Reusing the already-frozen estimator, rather than authoring a new one, avoids introducing a
second definition of "predictable volume" that could quietly disagree with L1–L4's own.

### 4.3 Null construction

**Frozen: stratified block permutation of the volume residual**, within predeclared time-of-day ×
own-range-state cells (the same `(slot, bias_range)` stratification L1–L4 already use), preserving
each cell's own residual values but permuting *which trigger bar* gets which residual, in
contiguous blocks rather than bar-by-bar. Block (not bar-by-bar) permutation is required by the
null-hygiene guidance surfaced during this design's own authoring: a naive bar-by-bar shuffle
would understate significance by destroying real serial dependence in the residual itself, the
same failure mode the block-shuffle discipline names for any autocorrelated continuous series.

**Block length is a frozen METHOD, not a frozen number, at this stage:** an automatic,
data-driven block-length selector (Politis–White optimal block length, or an equivalent
ACF-decay-threshold rule — the specific selector is Packet C1's own choice, disclosed there, not
here) applied to each instrument's own residual series independently, computed once as the first
act of Packet C1 and then held fixed through the rest of the pilot and any eventual Packet D
execution. Freezing the *method* now and the *number* at first real contact with the data (rather
than guessing a number now) avoids both under-blocking (naive small blocks that overstate
significance) and picking a number that happens to flatter or hurt the eventual result, since no
real residual series has been measured yet.

### 4.4 Re-estimation discipline (the load-bearing fix vs. the day-level design's failure)

Every null replicate re-runs, end to end, on that replicate's own block-permuted training data:

1. Re-fit the `tod_threshold` predictable-volume-component estimator (§4.2).
2. Recompute the residual and its block permutation for that replicate.
3. Re-fit both `baseline_1`/`augmented_1` logistic models (and, for the distinct-WHO run,
   `baseline_2`/`augmented_2`) on the replicate's training folds.
4. Re-score OOS on the replicate's test folds, recompute the Brier improvement.

No step in this chain uses a value fit once on the observed data and reused across replicates.
This is the direct answer to `Q-RANGEXFER-1`'s own failure: that design's positive control only
validated known-true-parameter behavior, and re-estimating per replicate (the only way the
procedure could run on real data) inflated Type-I from 5% to 25%. §3.2's cheap model family is
what makes doing this correctly, by default, computationally tractable at this design's own
replicate count and n.

### 4.5 Inference blocking

All resampling and permutation for both the null (§4.3) and any confidence interval on the primary
statistic is blocked at the **trading-day level**, never at the bar level. M15 bars within a day
are strongly dependent (same-bar volume/range Spearman ρ≈0.86–0.88, already measured on both
instruments; L1–L4's own within-stratum circular-shift null already treats dependence at the block
level for the same reason) — treating them as exchangeable units would be the exact IID-resampling
mistake `strategy-validation` skill §8d names for autocorrelated series generally.

---

## 5. B4 (continued) — Distinct-WHO reporting

Comparison 2 (§3.1) is run identically to Comparison 1 — same folds, same null construction, same
re-estimation discipline — substituting `baseline_2`/`augmented_2`. Its own Brier improvement and
attribution p-value are reported in the same results artifact as Comparison 1's, explicitly
labeled `distinct_who`, and never substituted for or averaged with Comparison 1's own figures. The
parent brief's own verdict map (§6) is unchanged by this design and is not consulted for the
distinct-WHO result — there is no verdict for it, only a disclosure.

---

## 6. B5 — Adversarial design review (required questions, pre-answered)

Pre-answered here for the reviewer's convenience; not a substitute for the actual review — see
§7. Any load-bearing finding returns to §3–§5 above and requires a dated amendment before Packet
C1, per the plan doc's own B5 instruction.

1. **Does the null preserve same-bar volume/range association and intraday seasonality closely
   enough for the claim being tested?** The block permutation (§4.3) operates on the *residual*
   after removing the predictable (ToD-conditioned) component, stratified by `(slot,
   own-range-state)` cell — it preserves the cell-level residual distribution and same-bar
   volume/range correlation (since range's own state defines the stratification cells, and
   permutation is within-cell only), while breaking the specific link the hypothesis needs broken:
   which trigger bar's residual volume goes with which next-bar outcome. Open risk for the
   reviewer: whether cell granularity (slot × 2 range states) is fine enough, or whether a coarser
   session-level stratification would preserve dependence better at the cost of statistical power
   — a genuine trade-off, not resolved by assertion here.
2. **Can information cross a rolling-fold boundary through normalization, residualization, or
   hyperparameter fitting?** Purge (§3.4) removes training rows whose own trailing window touches
   a test block; embargo removes training rows immediately after a test block. Every
   normalization/residualization statistic (§4.2's `tod_threshold`, any feature scaling for the
   logistic fit) is refit per fold using only that fold's own purged-and-embargoed training data,
   never fit once on the full panel and reused across folds.
3. **Is every fitted component re-estimated in each replicate?** Yes — §4.4 lists all four steps
   explicitly re-run per replicate. This is the design's central answer to the day-level design's
   own failure mode.
4. **Is the primary statistic declared once, with no best-of-metrics selection?** Yes — mean OOS
   Brier improvement (§4.1) is the sole primary statistic; log loss was considered and rejected in
   the same section, before any real score existed, not selected afterward from among candidates.
5. **Does daily-state conditioning at bar granularity introduce a collider or future-information
   path?** The distinct-WHO check (§5) conditions on the *prior* trading day's own realized-range
   state — strictly past relative to every bar in the current trading day, so no forward
   information enters through it. Open risk for the reviewer: whether `daily-range-state-persistence`'s
   own quintile/median statistic, as computed for that construct, uses a trailing window that
   could itself touch same-day bars under some edge-case trading-day boundary definition — worth an
   explicit check against that construct's own code before Packet C1, not assumed clean here.
6. **Are session blocks long enough for the dependence visible in both panels?** Not yet
   knowable without measuring each instrument's own residual ACF — which is exactly why block
   length (§4.3) is frozen as a method now and a number only after Packet C1 measures it on real
   data, per instrument, rather than guessed here and potentially wrong in a way that only an
   ACF-blind reviewer could miss.

---

## 7. Next step

B5's adversarial design review is routed through this PR's own Codex review pass rather than an
in-session panel — operator decision, 2026-08-31. §6's pre-answers stand as the design's own
opening position for that review, not a substitute for it. Any load-bearing finding is addressed
by a dated amendment to this file (§8) before Packet C1 begins; a finding that changes §3–§5's
frozen choices is not applied silently.

---

## 8. Amendment log

| Date | Change | By |
|---|---|---|
| 2026-08-31 | Initial design draft (B2–B5), submitted for adversarial review. No code written or executed. | Claude Code |
