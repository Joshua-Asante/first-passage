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
table. Where this design requires a number that can only be produced by touching real data (§4.3's
day-level regime classification uses a trailing distribution; §3.2's regularization strength `C`
uses training-fold nested CV — see §4.4's own accounting of what's fixed once vs. re-estimated
every replicate), it is specified as a **frozen method**, not a frozen number — the number itself
is computed once, as part of Packet C1, not here.

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
- `baseline_1`: time-of-day slot, **trigger-bar realized range as a continuous value** (raw
  `high − low`, already computed in `byyear_l4.py::prepare` as `bar_range`) **and** the trigger
  bar's own-range-elevated indicator (`bias_range`, already computed), a fixed set of recent range
  lags, fixed calendar/session controls. **Both** the continuous value and the binary indicator are
  included — not the binary alone (corrected 2026-08-31, Codex review, B5: an earlier draft of
  this design carried only `bias_range`; since same-bar volume/range correlation is ρ≈0.86–0.88,
  volume can proxy for the continuous range variation a 2-level indicator discards, so an
  augmented-beats-baseline result against a binary-only baseline would not establish attribution
  beyond the trigger bar's own range regime — it could just mean volume measures range better than
  a coarse flag does).
- `augmented_1`: `baseline_1` + the trigger bar's own **volume residual** — a continuous,
  standardized value, not the binary `bias_volume` indicator L1–L4 use. **Changed 2026-08-31
  (Codex second-pass review, B5) — see §4.2 for the full mechanism.** L1–L4's own binary indicator
  is a deliberately coarse presence-limb statistic; L5 is an out-of-sample forecasting comparison,
  where binarizing volume before testing whether it adds anything is a self-imposed information
  loss with no corresponding benefit, and it also would have required a separate, under-specified
  "how does the binary threshold get recomputed under a null replicate" step (a gap the second-pass
  review's Finding 4 named directly). Using the continuous residual removes that step entirely: the
  same real-valued quantity that gets permuted under the null (§4.3) is exactly what the model
  consumes as a feature, under both real and null-replicate data, with no intermediate
  re-binarization.
- This is the primary test of "does volume add incremental forward information beyond intraday
  seasonality and the trigger bar's own range state" — the question H-VOLREGIME-{MNQ,MYM} actually
  asks. `baseline_1`'s own feature set matches the plan doc's own B2 baseline bullet ("trigger-bar
  realized range and own-range-elevated indicator") verbatim.

**Comparison 2 — DISTINCT-WHO (disclosed, never gates):**
- `baseline_2`: `baseline_1` (continuous range + binary indicator, per the correction above) +
  prior trading day's own realized-range state, using `daily-range-state-persistence`'s own
  definition verbatim (prior day's True Range in its own trailing top quintile vs. its own trailing
  median — [`ops/instruments/MECHANISMS.md`](../../../../ops/instruments/MECHANISMS.md)
  `daily-range-state-persistence` heading), not a re-derived threshold.
- `augmented_2`: `baseline_2` + the same volume terms as `augmented_1`.
- Tests whether volume's own increment survives once the sibling single-series mechanism's own
  conditioning variable is also held fixed. See §5 for the frozen quantitative rule mapping this
  comparison's own outcome to mechanism A ("same phenomenon, finer grain") vs. mechanism B
  (genuinely distinct information source). Neither outcome changes the Comparison-1 verdict.

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
- **Trigger-bar realized range, continuous:** raw `bar_range = high − low` (already computed in
  `byyear_l4.py::prepare`), standardized using training-fold-only mean/SD (never fit on test data —
  see §3.4's purge/embargo). Added 2026-08-31 (Codex review, B5) alongside the existing binary
  `bias_range` indicator — see §3.1's corrected `baseline_1`.
- Recent range lags: **lag-1 through lag-4** raw `bias_range` indicators (already binary; no new
  computation). Declared now, not tuned after seeing results, per D2's own "do not invent a new
  threshold after seeing results" discipline extended here to lag count. (Only the trigger bar's
  own range, lag-0, is included in continuous form per the bullet above — the plan doc's own B2
  language names continuous range for the trigger bar specifically, not for the lag structure.)
- Volume feature for `augmented_1`/`augmented_2`: **the trigger bar's own volume residual, lag-0
  only** — a continuous, orthogonalized-against-baseline quantity, not the binary `bias_volume`
  indicator (see §3.1's correction, §4.2 for the exact construction). No volume lags are added —
  B2's "only those volume lags declared before the pilot" is satisfied by declaring zero beyond
  lag-0, since the parent brief's own H-VOLREGIME hypothesis is about the trigger bar's own volume
  state, not a volume-lag structure nobody has hypothesized. Any future volume-lag extension is a
  new design, not a retune of this one.
- **Calendar/session controls:** day-of-week (categorical) and an explicit RTH-vs-overnight session
  flag, **RTH = [09:30, 16:00) America/New_York**, the same equity-index-futures RTH window already
  used throughout this repo's own session-role constructs (e.g. `ops/instruments/MECHANISMS.md`'s
  `close@09:59 vs open@09:30` and `session-flat by 16:00 ET` conventions). **Corrected 2026-08-31
  (Codex review, B5):** an earlier draft pointed this at `byyear_l4.py`'s own trading-day-rollover
  rule (`slots >= 18*60` — the ~18:00 ET Globex-day-boundary convention used to assign a bar to its
  trading *day*), which answers a different question (which calendar day does this bar belong to)
  and does not define an RTH-vs-overnight split at all; there was no existing convention to reuse
  for this specific feature, so this freezes one directly instead.
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
- **Purge — feature side:** drop training rows whose own trailing-lookback window (the longest of
  the predictable-component window, §4.2, and the range-lag window, §3.3) overlaps the test
  block's span, so no training row's own *features* were computed using any test-block bar.
- **Purge — label side (added 2026-08-31, Codex review, B5: closes a real look-ahead gap the
  feature-side purge alone leaves open).** The outcome label is the *next* bar's range state
  (§4.1's own encoding), so a training row's label horizon extends one bar past the row itself.
  The feature-side purge above only checks backward-looking feature windows and does not by
  itself drop the training row immediately preceding a test block, whose own label is computed
  from that test block's first bar — an expanding-window split cannot see this because the purge
  window, as originally specified, only looks backward. **Fix:** additionally drop every training
  row whose label bar index falls at or after the test block's own start index — mechanically,
  the single training row immediately preceding each test block, given a strictly 1-bar-ahead
  label. Applied per fold, before any model is fit on that fold's training data.
- **Embargo:** drop training rows in a fixed window immediately following each test block, sized
  to at least the longest lag/window in the design (so serial dependence across the boundary
  doesn't let a test-adjacent training row leak test-period signal back into the next fold's
  training set).
- **Formal information-interval statement (added 2026-08-31, Codex second-pass review, B5 —
  tightens the two purge bullets and the embargo bullet above into one precise, non-generic
  specification rather than a CPCV analogy).** For a row at bar index *t*: its features use data
  through *t* only (causal by construction — see §4.2's own training-fold-only fitting); its label
  uses bar *t+1* (§4.1's encoding). Consequently: (a) the label-side purge above removes exactly the
  training rows whose *label* index (*t+1*) falls at or after the test block's start — not a
  generic CPCV citation, but this specific one-bar overlap interval; (b) a trailing predictor
  (§4.2's regression, §3.3's range lags) does **not** by itself require purging merely for being
  near the test boundary — it requires purging only when its own backward-looking window's span
  literally includes a test-block bar index, per the feature-side purge above; (c) the embargo
  immediately after a test block is justified specifically by serial dependence in the
  *residual* (§4.2) carrying forward past the test block's own last bar into the next fold's
  earliest training rows — sized to the residual's own dependence scope (bounded by the day-level
  circular-shift construction in §4.3, not an unrelated CPCV default), not a generic "ordinary
  legitimate walk-forward updating" concern this bullet does not intend to describe.
- **Warm-up.** **Corrected 2026-08-31 (Codex review, B5):** an earlier draft of this bullet said
  "the first `window` bars," which would warm up almost immediately (~96 slots/day means a flat
  60-bar cutoff clears in under a trading day) and does not match what `tod_threshold` actually
  requires. The frozen rule: a bar is eligible for scoring only once *its own time-of-day slot*
  has independently accumulated `window` **prior occurrences of that same slot** (60 for MNQ, 20
  for MYM, per `docs/briefs/pre-registration/Q-VOLREGIME-1-verdict-preregistration.md` §A/§F.1 —
  unchanged values, corrected description) — exactly `tod_threshold`'s own per-slot history
  requirement, not a flat leading-row-count cutoff. Different slots individually clear this floor
  at different calendar points, since each slot advances once per trading day; the population this
  produces matches L1–L4's own scored-frame construction exactly, by reusing the identical
  function (§4.2) rather than a re-derived cutoff.
- **Fold layout — frozen exactly, not a range (corrected 2026-08-31, Codex review, B5: an earlier
  draft left a 5–10-fold, quarter-to-half-year range open for Packet C1 to pick within, which is
  not actually frozen — different permissible picks change both which periods are scored and their
  weighting).** Test-block length is **exactly 6 calendar months** (two fiscal quarters), a fixed
  calendar unit, not a tunable count. Blocks walk forward, non-overlapping, starting from the first
  bar that is scoreable under the warm-up rule above (per instrument — MNQ and MYM start on
  different calendar dates since their own warm-up floors clear independently). **Fold count is
  therefore a mechanical consequence of each instrument's own scoreable span, not a separately
  chosen parameter:** `n_folds = floor(scoreable_span_months / 6)`. Any leftover partial period
  shorter than 6 months at the end of the panel is **dropped entirely**, never padded or resized —
  the same "mechanical cap, disclosed, never silently absorbed into the last fold" discipline this
  repo's own truncation conventions already use elsewhere. Given each instrument's own scored-frame
  span (`scored_frame_span_utc` in
  [`volregime_l3_2026-08-31/l3_results.json`](../volregime_l3_2026-08-31/l3_results.json): MNQ
  ≈70 months, MYM ≈71 months, before this design's own warm-up rule narrows it further), this
  produces on the order of 11–12 folds per instrument — a consequence of the frozen 6-month unit
  applied to each instrument's own real span, not a number chosen to hit a target fold count. The
  exact count is Packet C1's own arithmetic, not a free choice.

---

## 4. B3/B4 — Primary statistic, dependence treatment, attribution null

**Reworked in full 2026-08-31 (Codex second-pass review, B5).** The first round of Codex review
(inline, same PR) caught wording-level gaps in this section; a deeper second pass caught something
more serious underneath them — the null construction as first drafted did not actually preserve the
central same-bar volume/range confound it claimed to preserve, which is a correctness problem, not
a specification-clarity one. §4.2–§4.4 below are a full replacement, not a patch, built around one
change: **volume is orthogonalized against the full baseline feature set before anything is
permuted**, so there is little confound-relevant signal left in what gets shuffled. §4.1 (estimand
and replicate-count freezes) is also revised. The old, separate "§4.5 Inference blocking"
subsection is retired outright — the day-level circular-shift construction (§4.3) now carries
dependence-blocking by construction rather than as a bolted-on statement — and its concern is
picked up empirically by the new §4.6 adequacy gate instead. §4.5 is renumbered to a new,
previously-absent subsection on the distinct-WHO comparison's own residual.

### 4.1 Primary statistic

**Frozen: pooled out-of-fold Brier score improvement** (corrected 2026-08-31, Codex second-pass
review, Finding 8 — an earlier draft averaged Brier improvement *per fold* with equal fold
weighting; since test blocks are fixed-*calendar*-length (§3.4) but variable in actual bar count,
equal-fold weighting doesn't correspond to either a clean per-bar or per-calendar-period estimand.
Pooling first is unambiguous): concatenate every test-fold's out-of-sample predictions (baseline
and augmented, each fold using only its own fold-local fitted models) into one pool across all
folds, then compute `improvement = Brier(baseline_pool) − Brier(augmented_pool)` once over the
pooled predictions — every scored bar weighted equally, not every fold. `improvement > 0` favors
the augmented (volume-including) model. **Equal-fold-weighted improvement is reported alongside as
a secondary robustness diagnostic** (does the pooled result depend on one dense fold dominating),
never substituted for the primary statistic.

Brier is chosen over log loss because it is bounded ([0, 1] per prediction) and does not blow up on
a near-certain wrong prediction the way log loss can on a rare, poorly calibrated tail bar — a
property that matters more here than log loss's sharper penalty on confident errors, given this
design has not separately validated calibration robustness in the tails.

**`p_upper` tail definition and replicate count (added 2026-08-31, Codex review, B5; refined in the
second pass with the add-one correction and a frozen replicate count).** One-sided, upper-tail,
matching the declared favorable direction:

```
p_upper = (1 + #{replicates: null_improvement >= observed_improvement}) / (B + 1)
```

the standard finite-replicate (add-one) correction, so `p_upper` can never report exactly 0 off a
finite replicate set. `p_upper ≤ 0.05` clears; no two-sided or absolute-value variant is computed.
**`B = 4000` replicates**, frozen now (not deferred to Packet C1 — replicate count needs no contact
with real data to fix, unlike block length previously and the day-level regime split now, both of
which do). `4000` matches this construct's own precedent (`c3_stratified_rerun.py`'s own
`draws=4000`, cited in the pre-registration §F.1) rather than an unrelated number, and resolves
`p_upper` down to a minimum nonzero value of `1/4001 ≈ 0.00025` — the same floor L1–L4's own
`circular_shift_null_p` already reports at, so a "cleared decisively" L5 result would read on a
directly comparable scale to the precondition's own p-values.

**Companion (unchanged, already computed):** the existing minimum within-own-range-stratum lift
from L1–L3, reported alongside, not recomputed.

### 4.2 Predictable-volume-component estimator — reworked: joint, not ToD-only

**Corrected 2026-08-31 (Codex second-pass review, Finding 1 — the load-bearing fix).** An earlier
draft residualized volume against time-of-day alone (`byyear_l4.py::tod_threshold`), then permuted
that residual within coarse `(slot, bias_range∈{0,1})` cells, on the claim that binary-stratifying
by `bias_range` "preserves same-bar volume/range correlation." That claim does not hold: same-bar
volume/range correlation is continuous and strong (ρ≈0.86–0.88, both instruments), and ToD-only
residualization leaves nearly all of that continuous relationship inside the "residual." Permuting
that residual — even within a binary bucket — reassigns volume values that still carry most of
their originating bar's own range level to a *different* bar's real range, destroying a real,
strong within-cell dependence the null was supposed to hold fixed. Worse: because real (unpermuted)
volume and continuous range are then highly collinear regressors in the fitted model, a regularized
fit can split shared range-signal between them in a way that has nothing to do with volume carrying
independent information — an artifact the coarse-cell null, having stripped out the collinearity
entirely, would never reproduce. That gap could manufacture an apparently significant result out of
a regularization artifact, not a real effect — the opposite of what the null needs to guard against.

**Fix: residualize volume against the full `baseline_1` feature set jointly, in log space, before
any permutation.** Fit, on that fold's real training-fold data only (refit every null replicate —
see §4.4):

```
log(volume_t) ~ β0 + f_ToD(slot_t) + β1·range_t + Σ β_{i+1}·range_lag_i,t + γ·calendar_t
```

where `f_ToD` is the same sine/cosine time-of-day encoding as `baseline_1` (§3.3), `range_t` is the
trigger bar's own continuous realized range (§3.1's correction), `range_lag_i` are the four lagged
binary range indicators (§3.3), and `calendar_t` is the day-of-week/RTH control vector (§3.3) — the
exact same regressors `baseline_1` already uses, no new feature set invented. Ordinary least squares
on log-volume (log space chosen for two reasons: volume is strictly positive and right-skewed, so a
levels-space residual risks reconstructing a negative pseudo-volume under permutation, discussed in
§4.4; and it directly answers the second-pass review's own question about reconstruction space).
`residual_t = log(volume_t) − fitted_value_t`. By ordinary-least-squares construction, this residual
is linearly orthogonal, *within the training fold it was fit on*, to every one of `baseline_1`'s own
regressors — there is materially little range-driven (or ToD-driven, or calendar-driven) signal left
in it to preserve or destroy, which is what makes the block/circular-shift construction in §4.3 safe
regardless of its own granularity. This residual — standardized (training-fold mean/SD) — is
`augmented_1`'s own volume feature (§3.1), under both real and null-replicate data; no separate
binary threshold or reconstruction-to-a-flag step is needed (the second-pass review's own Finding 4
asked how `bias_volume` gets recomputed under a null — it doesn't, because the model no longer uses
`bias_volume` at all).

### 4.3 Null construction — reworked: day-level, regime-stratified circular shift

**Corrected 2026-08-31 (Codex second-pass review, Finding 3 — the permutation unit was
underspecified).** An earlier draft permuted individual bar-level residuals "in contiguous blocks"
within `(slot, bias_range)` cells. Within one exact time-of-day slot, successive same-cell
occurrences are normally a trading day apart, not adjacent bars — a "contiguous block" in
cell-occurrence order is not contiguous in market time, and that construction would have smeared
cross-slot structure (overnight/RTH transitions, intraday runs) the design needs to leave intact.

**Fix: reuse this repo's own already-reviewed `circular_shift_null_p` construction (PR #207,
already governing this construct's own Phase 0.5 precondition — see the parent brief's §0/§4),
applied to whole trading-day residual vectors, stratified by day-level range regime.**

1. Group the fold's own residuals (§4.2's output, training and test rows together — see §4.4) into
   one vector per trading day, ordered by slot within the day. A day's own vector has as many
   entries as that day has scoreable bars (some slots may be excluded by the warm-up rule, §3.4 —
   the vector is exactly as long as that day's own scored population, not padded).
2. Classify each day into a day-level regime bucket using `daily-range-state-persistence`'s own
   threshold rule — that day's own True Range against its own trailing top quintile/median split —
   applied here to classify *the day the residual-vector belongs to* (§3.1's `baseline_2` applies
   the identical rule to a different day, the one *before* the trigger bar; both reuse the same
   underlying construct, not two competing definitions), computed from that fold's own
   training-only trailing history. **Not a re-derived day-level split.**
3. Within each regime bucket independently, enumerate circular shifts of the bucket's own day-index
   sequence — every non-identity rotation, matching L1–L4's own "distinct rotations enumerated"
   convention, rather than a randomly sampled subset. A shift of *k* reassigns day *i*'s real
   position (its real features, its real outcome labels) to receive day *(i−k) mod n_bucket*'s own
   residual vector, wrapping within the bucket. **A day's own internal slot-ordered vector moves as
   one unit** — no within-day scrambling — so intraday cross-slot dependence is carried intact by
   construction, not merely hoped to survive.
4. Each null replicate = one such rotation (one specific *k*, applied independently within each
   regime bucket — a joint draw of one rotation per bucket, not a single shared *k* across buckets).
   Where `B=4000` (§4.1) exceeds the number of distinct enumerable rotations for a given instrument's
   own day count, sample without replacement until exhausted, then resample with replacement,
   disclosed as such in the results artifact — not silently padded.

This retires the earlier draft's separate block-length-selection machinery
(`arch.bootstrap.optimal_block_length` / Politis–White, frozen in the first Codex review round)
entirely: a circular shift needs no block-length parameter, since it moves whole, already-observed
day-vectors rather than synthesizing new blocks of a chosen length. That earlier fix is superseded,
not silently dropped — see §8's amendment log.

### 4.4 Re-estimation discipline and pseudo-volume reconstruction

**Corrected 2026-08-31 (Codex second-pass review, Finding 4 — the reconstruction step was never
made explicit) and (Codex first-pass review, B5 — the null must cover every scored row, not
training only, folded into the same rewrite).** Every null replicate re-runs, end to end, over that
replicate's own single, internally-consistent null draw of the full scored population (training and
test rows together) for the fold being tested:

1. Re-fit §4.2's joint log-volume regression on the fold's real, unpermuted training-fold data only
   (the regression's own coefficients are not part of the null being tested — only the residual's
   pairing with the day it originated from is).
2. Compute `residual_t` for **every scored row in the fold — training and test rows alike** —
   against that fit, group into day-vectors, classify each day's own regime bucket (§4.3 steps 1–2),
   then draw **one** rotation per bucket (§4.3 step 3) over that entire fold's population. Training
   rows and test rows are permuted together, from the same draw — never independently, which is
   exactly what would have broken the replicate statistic's exchangeability with the observed one
   (the first-pass review's own Finding 2).
3. **Reconstruct pseudo-volume**, per row, explicitly: `pseudo_log_volume_t = fitted_value_t
   (step 1, always that row's own real baseline features) + permuted_residual_t (step 2, from the
   day the rotation assigned)`; `pseudo_volume_t = exp(pseudo_log_volume_t)` — strictly positive by
   construction, answering the second-pass review's own positivity question directly. The model
   feature itself (§3.1, §4.2) is the **standardized residual**, real or permuted, not
   `pseudo_volume_t` — the exponentiated levels-space reconstruction exists only for §4.6's own
   adequacy diagnostics, which compare against real volume in its own natural units.
4. Re-fit `baseline_1`/`augmented_1` (and, for the distinct-WHO run, `baseline_2`/`augmented_2`) on
   the replicate's training rows, using that replicate's permuted standardized residual as the
   volume feature — never the real observed value.
5. Score OOS on the replicate's test rows, using those same test rows' **permuted** residual (step
   2) against their **real, unpermuted** outcome labels — never a mix of null-trained-model against
   real volume. Recompute the pooled Brier improvement (§4.1) from this null-world scoring.

**Nuisance parameters computed once, not per replicate — named and defended, not silent.** Two
values are fit from real data once (in Packet C1, before any replicate runs) and then held fixed
across all replicates and Packet D: the logistic regularization strength `C` (§3.2, via nested
cross-validation on real training folds), and — new in this rework — nothing else; §4.3's day-level
circular shift needs no analogous fitted parameter (no block length to select). This is a
deliberate, disclosed exception to "no value fit once on observed data and reused," not an
oversight: `C` calibrates model complexity, it is not itself part of the volume→outcome relationship
under test, and reusing one real-data-selected `C` across replicates is a much narrower fixed value
than the day-level design's own known-true-*model-structure* shortcut that inflated its Type-I rate.
**This is not asserted as harmless — it is a hypothesis Packet C1's own null-size study (its own
C2 gate) must empirically confirm**, exactly the discipline the second-pass review asked for: no
fixed value substitutes for re-estimation without the pilot showing the substitution doesn't matter.
Every other fitted object — §4.2's regression, the baseline/augmented model coefficients themselves,
the OOS scoring — is refit fresh inside every replicate, with no exception.

This is the direct, corrected answer to `Q-RANGEXFER-1`'s own failure: that design's positive
control only validated known-true-parameter behavior, and re-estimating per replicate (the only way
the procedure could run on real data) inflated Type-I from 5% to 25%. §3.2's cheap model family and
§4.2's cheap linear residualization are what keep full re-estimation computationally tractable by
default, at this design's own replicate count and *n*, rather than forcing a shortcut this design
would then have to disclose and hope survives calibration.

### 4.5 Distinct-WHO's own residual — reuses this section, not a separate model

Comparison 2's own volume feature (`augmented_2`, §3.1) is the *same* residual construction as
Comparison 1's — §4.2's joint regression already includes every `baseline_1` regressor, and
`baseline_2` only adds the prior-day range-state control on top. No second residualization is
authored for the distinct-WHO run; only the downstream logistic fit (§4.4 step 4) substitutes
`baseline_2`/`augmented_2` for `baseline_1`/`augmented_1`.

### 4.6 Null-adequacy diagnostics — frozen as a mandatory Packet C1 gate

**Added 2026-08-31 (Codex second-pass review, Finding 1's own required correction).** §4.2's
analytical fix (orthogonalize before permuting) is the design's primary defense, but this document
does not merely assert it works — Packet C1 must empirically confirm it before any pilot power/size
study (its own C2/C3) is meaningful. Before C2 begins, compare **observed vs. null-replicate-pooled**
(across a representative sample of replicates, not just one) on:

- same-bar volume/range Spearman correlation (target: null replicates should reproduce it closely,
  since the *reconstructed* `pseudo_volume_t` — §4.4 step 3 — is built from each row's own real
  baseline features and should therefore still correlate with real range at roughly the real
  strength, even though the *residual* driving it is permuted);
- conditional volume distribution across continuous-range quantiles (real vs. null-replicate-pooled);
- volume autocorrelation and range autocorrelation (bar-level, both series);
- cross-correlation between volume and range at lags −4 through +4;
- time-of-day distribution of `pseudo_volume_t` vs. real volume.

**A finding that any of these diverges materially between real and null-replicate data is a
load-bearing finding under this design's own D8 ("a pilot failure is a designed outcome") — it
routes to a dated amendment of §4.2–§4.4, not a tolerance widening, and not proceeding to Packet
C2/C3 regardless.** This gate is named here so it cannot be quietly skipped when Packet C1 is
actually executed.

---

## 5. B4 (continued) — Distinct-WHO reporting

Comparison 2 (§3.1) is run identically to Comparison 1 — same folds, same null construction, same
re-estimation discipline — substituting `baseline_2`/`augmented_2`. Its own Brier improvement and
attribution p-value are reported in the same results artifact as Comparison 1's, explicitly
labeled `distinct_who`, and never substituted for or averaged with Comparison 1's own figures. The
parent brief's own verdict map (§6) is unchanged by this design and is not consulted for the
distinct-WHO result — there is no verdict for it, only a disclosure.

**Quantitative decision rule (added 2026-08-31, Codex review, B5).** The parent brief's own §4
language — "collapse" implies mechanism A, "survival" implies mechanism B — is qualitative and,
left as-is, would let the mechanism label be chosen after seeing the actual numbers (a smaller-but-
still-significant improvement, a similar point estimate with reduced power, or opposite-signed
results across instruments would all be judgment calls under the original wording). Frozen here,
reusing the same `alpha=0.05` threshold already frozen for Comparison 1 rather than introducing a
new number:

| Comparison 1 (primary) | Comparison 2 (`distinct_who`) | Disclosure |
|---|---|---|
| `p_upper ≤ 0.05` (clears) | `p_upper > 0.05` (does not clear) | Mechanism A — "same phenomenon, finer grain": volume's own increment does not survive once daily-range-state is also held fixed. |
| `p_upper ≤ 0.05` (clears) | `p_upper ≤ 0.05` (also clears) | Mechanism B — genuinely distinct information source: volume's own increment survives daily-range-state conditioning. |
| `p_upper > 0.05` (does not clear) | — (not evaluated) | Moot — Comparison 1 itself did not clear; the mechanism-attribution question does not apply, per the parent brief's own verdict map (§6), which already stops at a non-clearing L5 outcome before any distinct-WHO framing is relevant. |

No other configuration is possible under this table by construction (Comparison 2 is evaluated only
when Comparison 1 clears), so this rule is total over the reachable outcome space, not merely the
common cases.

---

## 6. B5 — Adversarial design review (required questions, pre-answered)

Pre-answered here for the reviewer's convenience; not a substitute for the actual review — see
§7. Any load-bearing finding returns to §3–§5 above and requires a dated amendment before Packet
C1, per the plan doc's own B5 instruction.

1. **Does the null preserve same-bar volume/range association and intraday seasonality closely
   enough for the claim being tested? Rewritten in full 2026-08-31 (Codex second-pass review,
   Finding 1) — the original answer here was wrong.** The original design residualized volume
   against time-of-day alone, then permuted within a coarse binary `(slot, bias_range∈{0,1})`
   stratification, on the claim that the binary cells "preserved" the continuous ρ≈0.86–0.88
   same-bar correlation. They didn't — a binary bucket still contains a wide spread of continuous
   range values, and within-cell permutation of a residual that still carries most of that
   continuous signal destroys it. §4.2 now orthogonalizes volume against the *full* `baseline_1`
   feature set (continuous range included, not just its binary indicator) before any permutation
   happens, so §4.3's day-level circular shift has little confound-relevant signal left to disturb
   regardless of its own granularity — the fix is in what gets permuted, not primarily in how
   coarsely it's stratified. §4.6 freezes a mandatory Packet C1 adequacy gate (same-bar Spearman,
   conditional-volume-by-range-quantile, ACF, cross-correlation, ToD distribution — real vs.
   null-replicate-pooled) precisely so this claim is checked empirically before Packet C2/C3, not
   trusted on the strength of the analytical argument alone.
2. **Can information cross a rolling-fold boundary through normalization, residualization, or
   hyperparameter fitting?** Purge (§3.4) removes training rows whose own trailing *feature* window
   touches a test block **and** rows whose own *label* horizon reaches into the test block (added
   2026-08-31, Codex review, B5 — the original draft only purged on the feature side, which misses
   the one training row per fold whose 1-bar-ahead label is computed from the test block's own
   first bar); embargo removes training rows immediately after a test block, per §3.4's own
   information-interval statement. Every normalization/residualization statistic (§4.2's joint
   log-volume regression, any feature scaling for the logistic fit) is refit per fold using only
   that fold's own purged-and-embargoed training data, never fit once on the full panel and reused
   across folds — with the one named, defended exception in §4.4 (regularization strength `C`,
   fixed once from real data and held constant, not per-replicate).
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
6. **Are session blocks long enough for the dependence visible in both panels? Superseded
   2026-08-31 (Codex second-pass review, Finding 3) — the question no longer applies in its
   original form.** §4.3's earlier bar-level block-permutation (with a Politis–White-selected block
   length) is retired in favor of a day-level circular shift of whole residual vectors, reusing this
   repo's own already-reviewed `circular_shift_null_p` mechanism. That construction needs no
   block-length parameter at all — it moves entire, already-observed trading-day vectors, so
   intraday cross-slot dependence is carried by construction rather than by tuning a length to
   match it. The residual ACF question is not eliminated, only relocated: it becomes part of §4.6's
   own mandatory Packet C1 adequacy gate (does null-replicate-pooled volume autocorrelation match
   real volume's own), checked empirically rather than assumed by construction.

**Review status, round 1 (2026-08-31):** Codex's inline review of this design (via this PR)
returned 9 findings — 4 load-bearing (baseline missing continuous range; null not applied to
test-fold volume; feature-side-only purge missing the label-horizon leak; an internally
inconsistent "two-sided p_upper" carried over from the pre-registration) and 5 lower-severity (fold
layout left as a range rather than frozen exactly; RTH boundary pointed at the wrong existing
convention; block-length selector left as a two-option menu; warm-up worded as a flat bar count
instead of per-slot occurrences; distinct-WHO mechanism labels left qualitative). All 9 addressed.

**Review status, round 2 (2026-08-31) — a deeper pass found the wording fixes above weren't
sufficient.** A second Codex review, run separately from the inline pass, found 8 more findings — 2
P0 (the null did not actually preserve the same-bar volume/range confound it claimed to, even after
round 1's fixes — §4.2's real subject; and this pre-registration's own §C heading contradicted its
own §D verdict map about whether L5 gates, a defect predating Packet B) and 6 P1/P2 (permutation
unit underspecified; pseudo-volume reconstruction never made explicit; regularization-`C`
re-estimation-per-replicate left unanswered; purge/embargo prose imprecise for an expanding
walk-forward; equal-fold-weighting estimand mismatch — plus confirmation that round 1's fold-layout
and block-length fixes were in fact already resolved). **All addressed** — §4 is a full rework, not
a further patch; see §8's own entry for the complete account of what changed and why. This is the
kind of finding B5 exists to catch before Packet C, not after it — round 1's fixes were real but
incomplete, and round 2 is why a from-scratch design gets adversarially reviewed rather than judged
plausible on its own author's say-so.

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
| 2026-08-31 | **Codex review round 1 (PR #241) — 9 findings, all addressed.** 4 load-bearing: (1) baseline was missing the continuous trigger-bar range B2 itself specifies, admitting a volume-as-range-proxy confound the within-stratum null wouldn't catch — added; (2) the attribution null only permuted training-fold volume, scoring against real test-fold volume, breaking the replicate statistic's exchangeability with the observed one — fixed to permute one consistent draw across train and test rows together; (3) purge only covered feature-side lookback, missing that a 1-bar-ahead label leaks the test block's first bar into the preceding training row — added label-horizon purging; (4) the pre-registration's "two-sided p_upper" was internally inconsistent with this repo's one-sided convention and the design's own declared direction — resolved to a precise one-sided upper-tail definition in both this file and the pre-registration. 5 lower-severity: fold layout frozen exactly (6-month blocks, mechanically-derived count) rather than left as a 5-10-fold range; RTH boundary given an explicit, correctly-sourced definition rather than pointing at `byyear_l4.py`'s unrelated trading-day-rollover rule; block-length selector narrowed to one algorithm (Politis-White via `arch.bootstrap`) rather than a two-option menu; warm-up corrected to per-slot occurrence counts rather than a flat bar count; distinct-WHO mechanism-A/B labels given a quantitative decision table reusing the existing `alpha=0.05` threshold. No result computed under any of the corrected wording — all 9 were caught before any pilot code existed. | Claude Code, responding to Codex's PR #241 review |
| 2026-08-31 | **Codex review round 2 — 8 findings, all addressed; §4 reworked in full.** Round 1's fixes were real but did not reach the central defect: the attribution null claimed binary `(slot, bias_range)` stratification "preserved" the continuous ρ≈0.86–0.88 same-bar volume/range correlation it needed to hold fixed; it didn't, and permuting a residual that still carried most of that continuous signal, within a coarse binary bucket, risked crediting volume for a regularization/collinearity artifact the null itself would never reproduce (P0, Finding 1). **Fix, §4.2:** volume is now residualized, in log space, against the full `baseline_1` feature set jointly (continuous range included, not just its binary indicator) — orthogonal to those regressors by OLS construction, leaving little confound-relevant signal for any permutation to mishandle. **Fix, §4.3:** the permutation unit itself was underspecified (Finding 3 — a "contiguous block" in same-cell-occurrence order is not contiguous in market time); replaced bar-level block-permutation with a day-level circular shift of whole residual vectors, stratified by `daily-range-state-persistence`'s own day-level regime split, reusing this repo's own already-reviewed `circular_shift_null_p` mechanism (PR #207) rather than inventing a new one — this also retires the earlier round-1 block-length-selector fix (`arch.bootstrap.optimal_block_length`) as superseded, not silently dropped. **Fix, §4.4:** made the pseudo-volume reconstruction explicit end to end (Finding 4) — `pseudo_log_volume = real fitted value + permuted residual`, exponentiated for strict positivity — and switched `augmented_1`/`augmented_2`'s own volume feature from the binary `bias_volume` indicator to the continuous standardized residual directly, which also eliminates the separate "how does the binary threshold get recomputed under a null" question Finding 4 raised, since there is no threshold to recompute. **Fix, §4.4:** named and defended the one nuisance parameter (logistic `C`) fixed once from real data rather than re-estimated per replicate, and tied that exception's validity to Packet C1's own null-size study rather than asserting it's harmless (part of Finding 6). **Fix, §4.1:** switched the primary estimand from equal-fold-weighted to pooled out-of-fold Brier improvement (Finding 8), with equal-fold reported as a secondary diagnostic; froze the replicate count at `B=4000` (matching this construct's own `c3_stratified_rerun.py` precedent) and added the standard add-one finite-replicate correction to `p_upper`. **Fix, §3.4:** added a precise, interval-based purge/embargo statement (Finding 7) alongside the existing bullets rather than replacing them, since they were not substantively wrong, only insufficiently rigorous. **Fix, pre-registration §C (P0, Finding 2):** the section heading read "NEVER GATES... TYPES the verdict," directly contradicting §D's own verdict map (which already routed a valid-non-clearing L5 to `FALSIFIED`) — a defect that predated Packet B and was inherited, not introduced, by this amendment; corrected the heading to state plainly that L5 gates, matching what §D and this design's own `baseline_1`/Comparison-1 language already implemented. **Added, §4.6:** a mandatory Packet C1 null-adequacy diagnostic gate (same-bar Spearman, conditional-volume-by-range-quantile, ACF, cross-correlation, ToD distribution, real vs. null-replicate-pooled) — Finding 1's own required correction, so the analytical fix above is empirically checked before Packet C2/C3, not merely asserted. No pilot code exists and no real L5 statistic was inspected under any version of this design. | Claude Code, responding to a second Codex review round on PR #241 |
