# Q-VOLREGIME-1 — L5 attribution design (Packet B)

**Status:** `DESIGN-FROZEN` — B5's adversarial review is complete (updated 2026-08-31; see §6's
review-status entries: five Codex review rounds on PR #241, the fifth returning no findings). No
code has been written or executed against this design. No real L5 statistic, on either instrument,
has been inspected before or during authoring or review. This document freezes B2–B5 of
[`docs/superpowers/plans/2026-08-31-q-volregime-next-step.md`](../../../../docs/superpowers/plans/2026-08-31-q-volregime-next-step.md).
The next gate is Packet C1's own pilot GO — a separate operator decision, not implied by this
status (see §7).

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
- `augmented_1`: `baseline_1` + the trigger bar's own `bias_volume` — the **binary**,
  above-own-slot-median indicator, matching L1–L4's own construction exactly. **Reverted
  2026-08-31 (Codex third-pass review, Finding 9 — a real course-correction, not a wording
  tweak).** The immediately preceding round of this design switched this feature to a continuous
  standardized residual, specifically to avoid re-specifying how a binary threshold gets
  recomputed under a null replicate. That traded a real, more serious problem for a smaller one:
  H-VOLREGIME-{MNQ,MYM} and L1–L4 are specifically claims about the *binary* above/below-median
  volume state — a continuous linear-improvement test is a different, more general claim, which
  could clear or fail for reasons that have nothing to do with the specific binary-threshold effect
  L1–L4 established presence for. A clearing continuous-L5 result would not have attributed the
  same hypothesis it was supposed to test. Reverted to the binary feature; §4.4 now specifies the
  null-reconstruction step this reversion re-requires, using the pseudo-volume machinery already
  built for §4.6's own diagnostics rather than leaving it unspecified a second time.
- This is the primary test of "does volume add incremental forward information beyond intraday
  seasonality and the trigger bar's own range state" — the question H-VOLREGIME-{MNQ,MYM} actually
  asks. `baseline_1`'s own feature set matches the plan doc's own B2 baseline bullet ("trigger-bar
  realized range and own-range-elevated indicator") verbatim.

**Comparison 2 — DISTINCT-WHO (disclosed, never gates):**
- `baseline_2`: `baseline_1` (continuous range + binary indicator, per the correction above) +
  prior trading day's own realized-range state, using `daily-range-state-persistence`'s own
  **conditioning** threshold specifically — that prior day's own True Range in its own trailing
  top quintile (P80), a single binary flag. **Corrected 2026-08-31 (Codex third-pass review,
  Finding 5) — the construct actually defines two different thresholds, not one:** a top-quintile
  (P80) trigger used to classify a day's own state (what this design reuses), and a separate
  trailing-median (P50) reference used only to measure *next-day's* outcome in that construct's own
  claim (`daily-range-state-persistence`'s own subject — "does a day's TR being in the trailing top
  quintile predict elevated next-day TR vs. its own trailing median"). An earlier draft's "top
  quintile vs. trailing median" phrasing conflated these into one ambiguous rule; this design uses
  the P80 conditioning threshold alone, never the P50 outcome threshold, as its own stratification
  variable — [`ops/instruments/MECHANISMS.md`](../../../../ops/instruments/MECHANISMS.md)
  `daily-range-state-persistence` heading, not a re-derived threshold.
- `augmented_2`: `baseline_2` + the trigger bar's own `bias_volume`, same feature as `augmented_1`
  — reconstructed under the null via **its own, separate residualization** (§4.5, corrected —
  reusing Comparison 1's own residual here would leave the same collinearity-artifact risk Finding
  1 fixed for Comparison 1, open for Comparison 2's own added control).
- Tests whether volume's own increment survives once the sibling single-series mechanism's own
  conditioning variable is also held fixed. See §5 for the frozen statistic mapping this
  comparison's own outcome to mechanism A ("same phenomenon, finer grain") vs. mechanism B
  (genuinely distinct information source). Neither outcome changes the Comparison-1 verdict.

Reusing `daily-range-state-persistence`'s own P80 conditioning threshold (rather than inventing a
parallel one, or conflating it with that construct's own separate P50 outcome threshold) keeps the
distinct-WHO check honest about testing *that* mechanism, not a lookalike.

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
- Volume feature for `augmented_1`/`augmented_2`: **the trigger bar's own `bias_volume`, lag-0
  only** — the same binary above-own-slot-median indicator L1–L4 use (reverted 2026-08-31, Codex
  third-pass review, Finding 9 — see §3.1's correction, §4.4 for how it is reconstructed under a
  null replicate). No volume lags are added — B2's "only those volume lags declared before the
  pilot" is satisfied by declaring zero beyond lag-0, since the parent brief's own H-VOLREGIME
  hypothesis is about the trigger bar's own volume state, not a volume-lag structure nobody has
  hypothesized. Any future volume-lag extension is a
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
- **Embargo — frozen exactly, not a vague minimum (corrected 2026-08-31, Codex third-pass review,
  Finding 10: "at least the longest lag/window" is not an exact duration, and the day-level
  circular-shift construction doesn't bound the residual's own real serial dependence — that's an
  empirical property of the data, not something a null's own permutation scheme can constrain by
  construction).** Embargo = **4 trading days**, drop training rows in this fixed window
  immediately following each test block. Tied to an already-frozen constant rather than a fresh
  number: 4 matches the range-lag depth already fixed in §3.3 (lag-1 through lag-4), not a value
  chosen for this bullet alone. §4.6's own adequacy diagnostics (residual ACF, cross-correlation at
  lags −4 through +4) empirically check whether 4 trading days is in fact sufficient — this bullet
  fixes the number Packet C1 tests, it does not itself certify the number is adequate.
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
- **Setup period — reserved before fold 1, added 2026-08-31 (Codex third-pass review, Finding 2 —
  a real gap: starting the first test block at the first warm-up-cleared bar leaves fold 1 with
  zero training rows, since "training for fold *k* is every bar before that fold's test block."
  You cannot fit anything — the joint regression, the logistic models, or Finding 11's own
  nested-CV `C` selection — on zero rows).** Reserve **12 calendar months** (2× the frozen
  6-month test-block unit, not a freshly invented number) of scoreable, warm-up-cleared bars,
  immediately following each instrument's own warm-up-clearing point, as a **training-only setup
  period that itself scores no fold.** Fold 1's own test block begins only after this period ends.
  This period serves two purposes, both requiring only real, unpermuted data: it gives fold 1 a
  non-trivial training set, and it is the **only** data `C` (§3.2) is ever selected against — see
  §4.4's own accounting of why nested CV needs to be scoped this narrowly, not pooled across
  folds. By the end of this 12-month period, every slot has long since individually cleared its
  own warm-up floor (60 same-slot occurrences for MNQ ≈ 60 trading days ≈ 3 months; 20 for MYM ≈ 1
  month) — so every scoreable day inside any test fold has the full, identical slot-mask, which is
  what makes Finding 3's own slot-mask-matching requirement (§4.3) bind in practice only at the
  panel's earliest days, not throughout the scored region.
- **Fold layout — frozen exactly, not a range (corrected 2026-08-31, Codex review, B5: an earlier
  draft left a 5–10-fold, quarter-to-half-year range open for Packet C1 to pick within, which is
  not actually frozen — different permissible picks change both which periods are scored and their
  weighting).** Test-block length is **exactly 6 calendar months** (two fiscal quarters), a fixed
  calendar unit, not a tunable count. Blocks walk forward, non-overlapping, starting immediately
  after the setup period above ends (per instrument — MNQ and MYM start on different calendar
  dates since their own warm-up floors, and therefore their own setup periods, clear
  independently). **Fold count is therefore a mechanical consequence of each instrument's own
  scoreable span net of warm-up and the setup period, not a separately chosen parameter:**
  `n_folds = floor((scoreable_span_months − 12) / 6)`. Any leftover partial period shorter than 6
  months at the end of the panel is **dropped entirely**, never padded or resized — the same
  "mechanical cap, disclosed, never silently absorbed into the last fold" discipline this repo's
  own truncation conventions already use elsewhere. Given each instrument's own scored-frame span
  (`scored_frame_span_utc` in
  [`volregime_l3_2026-08-31/l3_results.json`](../volregime_l3_2026-08-31/l3_results.json): MNQ
  ≈70 months, MYM ≈71 months, before this design's own warm-up rule and the 12-month setup period
  above narrow it further), this produces on the order of 9–10 folds per instrument — a
  consequence of the frozen 6-month unit and 12-month setup reservation applied to each
  instrument's own real span, not a number chosen to hit a target fold count. The exact count is
  Packet C1's own arithmetic, not a free choice.

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

### 4.2 Predictable-volume-component estimator — global per replicate, raw (not standardized)

**Corrected 2026-08-31 (Codex second-pass review, Finding 1 — the load-bearing fix; corrected again
same date, Codex fourth-pass review, Finding 5 — a units bug in what this section feeds §4.4).** An
earlier draft residualized volume against time-of-day alone (`byyear_l4.py::tod_threshold`), then
permuted that residual within coarse `(slot, bias_range∈{0,1})` cells, on the claim that
binary-stratifying by `bias_range` "preserves same-bar volume/range correlation." That claim does
not hold: same-bar volume/range correlation is continuous and strong (ρ≈0.86–0.88, both
instruments), and ToD-only residualization leaves nearly all of that continuous relationship inside
the "residual." Permuting that residual — even within a binary bucket — reassigns volume values
that still carry most of their originating bar's own range level to a *different* bar's real range,
destroying a real, strong within-cell dependence the null was supposed to hold fixed. Worse: because
real (unpermuted) volume and continuous range are then highly collinear regressors in the fitted
model, a regularized fit can split shared range-signal between them in a way that has nothing to do
with volume carrying independent information — an artifact the coarse-cell null, having stripped
out the collinearity entirely, would never reproduce.

**Fix: residualize volume against the full `baseline_1` feature set jointly, in log space, before
any permutation — fit once per replicate, over the whole scoreable panel, not per fold (see §4.3's
own note on why this is global).**

```
log(volume_t) ~ β0 + f_ToD(slot_t) + β1·range_t + β2·bias_range_t + Σ β_{i+2}·range_lag_i,t + γ·calendar_t
```

where `f_ToD` is the same sine/cosine time-of-day encoding as `baseline_1` (§3.3), `range_t` is the
trigger bar's own continuous realized range (§3.1's correction), `bias_range_t` is the trigger bar's
own **binary** own-range-elevated indicator (added round 3, Finding 1's own continuation — OLS
orthogonality to *continuous* `range_t` does not imply orthogonality to `bias_range_t`, since the
threshold defining it is itself a trailing, drifting quantity, not a linear transform of `range_t`),
`range_lag_i` are the four lagged binary range indicators (§3.3), and `calendar_t` is the
day-of-week/RTH control vector (§3.3) — the exact same regressors `baseline_1` already uses, no new
feature set invented. Ordinary least squares on log-volume (log space: volume is strictly positive
and right-skewed, so a levels-space residual risks reconstructing a negative pseudo-volume under
permutation). `residual_t = log(volume_t) − fitted_value_t` — kept **raw, never standardized**
(corrected round 4, Finding 5: an earlier draft standardized this residual by its own training mean/
SD for use as a direct model feature; round 3 already retired that use — `augmented_1`'s own feature
is the *binary* `pseudo_bias_volume`, not the residual itself, per Finding 9 — so nothing consumes a
standardized value anymore, and §4.4's reconstruction formula adds this residual directly to a
log-volume-scale fitted value, which is only unit-consistent if it is *not* rescaled first. Dropping
standardization removes the bug and a step nothing needed).

By ordinary-least-squares construction, this residual is linearly orthogonal, *within the panel it
was fit on*, to every one of `baseline_1`'s own regressors — there is materially little range-driven
(continuous or threshold-based), ToD-driven, or calendar-driven signal left in it to preserve or
destroy, which is what makes the circular-shift construction in §4.3 safe regardless of its own
granularity. This raw residual feeds §4.3–§4.4's own pseudo-volume reconstruction, from which
`augmented_1`'s actual feature (`bias_volume`, binary) is recomputed under both real and
null-replicate data.

### 4.3 Null construction — reworked again: one global replicate, not one per fold

**Corrected 2026-08-31 (Codex fourth-pass review, Finding 9 — a structural gap, not a wording
issue) — folded together with Findings 1 and 7 from the same round, since all three are the same
underlying problem at different points in the pipeline.** An earlier draft drew a rotation
**independently per fold** ("draw one rotation per group... over that entire fold's population").
Because folds expand — a calendar day appears as a test row in exactly one fold and as a training
row in every later fold — an independent per-fold draw means the *same* day can receive a
*different* donor day's residual depending on which fold happens to be computing it. "Replicate `j`"
was therefore not one well-defined alternate version of the observed panel; it was a patchwork of
different per-fold worlds stitched together and pooled (§4.1) as if they were one. That is a
mechanism for miscalibrating the pooled null's own variance, not merely a conceptual untidiness —
the real, observed statistic has exactly one fixed value per day, and the null construction owes it
the same property.

Two more round-4 findings turned out to be the same defect surfacing elsewhere in the pipeline:
**Finding 1** (the threshold used to reconstruct `pseudo_bias_volume` was frozen at a fold's real-
data fit rather than recomputed causally along each replicate's own reconstructed path) and
**Finding 7** (the day-level regime bucket was classified once at a fold boundary, which goes stale
across a 6-month test block whose own trailing window would, causally, reach into earlier test
days). All three are resolved together by making the null a **single, global, causally-consistent
construction per replicate**, computed once over the whole panel, with only the *scored* predictive
models (`baseline_1`/`augmented_1` themselves) remaining fold-local:

1. **Day-level regime classification — global, real-data-only, shared across every replicate
   (Finding 7's fix).** Day-level True Range is never permuted in this design — only volume is — so
   the P80 conditioning threshold (§3.1, §4.3's own prior definition) can be computed **once**, via
   a single causal pass over each day's own real trailing history across the *entire* scoreable
   panel (not frozen at any fold boundary, not restricted to any one fold's training-only slice).
   This one classification is reused identically by the real/observed scoring, by every null
   replicate, and by both Comparison 1 and Comparison 2 — it does not depend on the null draw at
   all, so there is nothing to recompute per replicate here.
2. Group the panel's own residuals (§4.2's global fit) into one vector per trading day, ordered by
   slot within the day, across the **entire scoreable panel** — not per fold. Record each day's own
   slot mask alongside its vector, exactly as before.
3. **Stratify by (regime bucket, slot mask) exactly as before** — a day's own vector may only be
   reassigned to another day with an identical slot mask (round 3, Finding 3's fix, unchanged in
   substance, now applied globally rather than per fold). A group with fewer than 2 member days is
   excluded from the rotation pool. **Corrected 2026-08-31 (Codex fourth-pass review, Finding 6) —
   an earlier draft excluded such a group from the *rotation pool* without saying what happens to
   its own days' rows in scoring.** Days belonging to an excluded (singleton) group are **excluded
   from both real/observed and every null-replicate's own scoring entirely** — not silently scored
   with their real, unpermuted pairing surviving in every replicate (which would let any signal
   concentrated in those specific rows go un-nulled, biasing the pooled statistic toward the real
   result). This is expected to be a rare, near-empty exclusion in practice, given the setup
   period's own slot-mask-completing effect (§3.4), but is now handled consistently rather than
   left to default silently to the wrong behavior.
4. Within each (regime bucket, slot mask) group, enumerate circular shifts of the group's own
   day-index sequence — **including the identity rotation** (round 3, Finding 6's fix, unchanged),
   matching L1–L4's own `circular_shift_null_p` convention.
5. **Draw ONE joint rotation assignment — one `k` per group — for the WHOLE PANEL, once per
   replicate `j` (the Finding-9 fix itself).** This single global assignment is what "replicate `j`"
   *means*: for every day in the entire scoreable panel, a fixed, single donor-day mapping, used
   identically no matter which fold's own training or test set that day later falls into. Where
   `B=4000` (§4.1) exceeds the number of distinct enumerable joint combinations for a given
   instrument's own day count, sample without replacement until exhausted, then resample with
   replacement, disclosed as such — not silently padded.

This retires the earlier draft's separate block-length-selection machinery
(`arch.bootstrap.optimal_block_length` / Politis–White, frozen in the first Codex review round)
entirely: a circular shift needs no block-length parameter, since it moves whole, already-observed
day-vectors rather than synthesizing new blocks of a chosen length.

### 4.4 Reconstruction (one causal pass over the whole panel) and fold-local scoring

**Reworked 2026-08-31 (Codex fourth-pass review, Findings 1, 2, 9) to reflect §4.3's global
construction, and to fix a real-vs-real comparator mismatch (Finding 2).** For a given replicate —
including the real/observed case, treated as the identity assignment for every group, so this
recipe is one procedure, not two:

1. Fit §4.2's joint log-volume regression once, globally, on the panel's real training-eligible
   data (this fit is a nuisance step in constructing the null — it is not itself scored for OOS
   accuracy — so a global fit does not reopen any leakage concern; what remains strictly fold-local,
   below, is the actual *scored* model). Compute the raw residual (§4.2) for every scored row in the
   panel; apply §4.3's own global rotation assignment to reassign residuals by day.
2. **Reconstruct pseudo-volume via one continuous causal pass over the whole panel, in chronological
   order (Finding 1's fix — replaces a single frozen threshold).** For each bar, in time order:
   `pseudo_log_volume_t = fitted_value_t (step 1's global fit, always that row's own real baseline
   features) + permuted_residual_t (§4.3's assignment)`; `pseudo_volume_t = exp(pseudo_log_volume_t)`
   — strictly positive by construction. The trailing same-slot threshold used in the next step is
   **recomputed causally from this same pass's own already-reconstructed `pseudo_volume` values**
   (transitioning from real historical volume in the pre-scoreable warm-up region, where nothing has
   been reconstructed yet, to reconstructed `pseudo_volume` once the scoreable region begins) — not
   a single value frozen at any fold's own real-data fit. This is what makes `pseudo_bias_volume`
   (next step) a self-consistent object: its own generative process now mirrors exactly how the real
   `bias_volume` is defined — a continuously causally-updating rolling comparison — rather than a
   comparison against a threshold that never updates through the null world it is supposed to
   describe.
3. **`pseudo_bias_volume_t`, using each instrument's own real comparator (Finding 2's fix — an
   earlier draft used strict `>` uniformly).** `byyear_l4.py::prepare` defines MNQ's real feature
   with `volume >= volume_threshold` (inclusive) and MYM's with strict `>` — carried verbatim here:
   `pseudo_bias_volume_t = 1[pseudo_volume_t >= pseudo_tod_threshold_t]` for MNQ,
   `1[pseudo_volume_t > pseudo_tod_threshold_t]` for MYM. Volume is discrete and ties against a
   rolling median are not rare; using the wrong comparator meant even the identity rotation (which
   must exactly reproduce the observed data) would not reproduce MNQ's own real `bias_volume` on
   tied rows — this is why the mismatch is load-bearing, not cosmetic. `pseudo_volume_t` itself is
   retained for §4.6's own adequacy diagnostics, which compare against real volume in its own
   natural units.
4. **Fold-local scoring — unchanged discipline, now consuming one globally-consistent input.** For
   each fold independently: fit `baseline_1`/`augmented_1` on that fold's own purged/embargoed
   training rows, using each row's `pseudo_bias_volume` (or real `bias_volume`, for the observed
   case) from steps 2–3 — the *same* value regardless of whether this fold sees that row as training
   or (in its own fold) as test data, since step 2's reconstruction was global. Score OOS on that
   fold's own test rows the same way. Pool every fold's own OOS predictions for this one replicate
   into the primary statistic (§4.1) — now genuinely one coherent transformation of the whole panel,
   not a patchwork.

**Nuisance parameters computed once, not per replicate — named, defended, and scoped to avoid
leakage.** One value is fit from real data once (before any replicate runs) and held fixed across
all replicates and Packet D: the logistic regularization strength `C` (§3.2), selected by nested CV
using **only** §3.4's own 12-month setup-period data — the reserved period that itself scores no
fold and, by construction, contains no bar from any fold's own test block, in either direction
(round 3, Finding 11's fix, unchanged by this round's rework). `C` calibrates model complexity; it
is not itself part of the volume→outcome relationship under test. **This is not asserted as
harmless — it is a hypothesis Packet C1's own null-size study (its own C2 gate) must empirically
confirm.** The day-level regime classification (§4.3 step 1) is also computed once and shared
across replicates, but for a different, non-discretionary reason: it depends only on real,
never-permuted range data, so there is nothing for it to be re-estimated *against* per replicate.
Every other object — §4.2's regression, the causal `pseudo_tod_threshold` reconstruction, the
baseline/augmented model coefficients themselves, the OOS scoring — is refit fresh for every
replicate, with no further exception.

This is the direct, corrected answer to `Q-RANGEXFER-1`'s own failure: that design's positive
control only validated known-true-parameter behavior, and re-estimating per replicate (the only way
the procedure could run on real data) inflated Type-I from 5% to 25%. §3.2's cheap model family and
§4.2's cheap linear residualization are what keep full re-estimation computationally tractable by
default, at this design's own replicate count and *n*, rather than forcing a shortcut this design
would then have to disclose and hope survives calibration.

### 4.5 Distinct-WHO's own residual — a second, separate residualization

**Corrected 2026-08-31 (Codex third-pass review, Finding 4) — the previous draft's claim that
Comparison 2 needs no second residualization was wrong.** Reusing Comparison 1's own residual
(orthogonal to `baseline_1` only) for Comparison 2 leaves it non-orthogonal to `baseline_2`'s own
*added* regressor (prior-day range-state) — real, unpermuted volume can still be collinear with
that control in the observed fit. That reopens Finding 1's exact collinearity-artifact mechanism,
specifically for Comparison 2's own added control.

**Fix: a second joint log-volume regression, adding the one control `baseline_2` adds on top of
`baseline_1`, fit globally per replicate exactly as §4.2 now is:**

```
log(volume_t) ~ β0 + f_ToD(slot_t) + β1·range_t + β2·bias_range_t + Σ β_{i+2}·range_lag_i,t
                + γ·calendar_t + δ·prior_day_regime_t
```

— identical to §4.2's formula plus `prior_day_regime_t` (the prior trading day's own P80
conditioning flag, §3.1's `baseline_2`), raw, never standardized (§4.2's own correction applies
here too). §4.3's global rotation-assignment and §4.4's reconstruction steps 1–4 apply verbatim to
Comparison 2, substituting this regression and its own `pseudo_bias_volume_2`.

**What is separate vs. shared between the two comparisons (disambiguated for §5's own paired
test).** Separate: the regression/residual itself. **Shared, for replicate index *j* specifically:
the global (regime-bucket, slot-mask, rotation-*k*) draw itself (§4.3 step 5)** — replicate *j*
applies the identical panel-wide day-index rotation to *both* comparisons' own residual vectors,
same which-day-swaps-with-which-day arrangement, different residual values being swapped. This is
what makes "replicate *j* of Comparison 1" and "replicate *j* of Comparison 2" a genuine matched
pair (§5) rather than an arbitrary same-index coincidence between two independently-randomized
processes.

### 4.6 Null-adequacy diagnostics — frozen as a mandatory Packet C1 gate

**Added 2026-08-31 (Codex second-pass review, Finding 1's own required correction).** §4.2's
analytical fix (orthogonalize before permuting) is the design's primary defense, but this document
does not merely assert it works — Packet C1 must empirically confirm it before any pilot power/size
study (its own C2/C3) is meaningful.

**Gated per replicate, not on a pooled average (corrected 2026-08-31, Codex third-pass review,
Finding 7).** An earlier draft compared observed values against a **pooled** average across a
sample of replicates. That can hide exactly the failure this gate exists to catch: replicates that
individually distort a correlation or an ACF in *opposite* directions can average back to
approximately the real value even though no single replicate actually preserves the nuisance
structure — and what feeds `p_upper` is each replicate's own individual statistic, not a pooled
aggregate, so pooled-average adequacy is not the right thing to check. **Fix:** compute each
diagnostic below **per replicate**, across a large representative sample (at minimum a few hundred
of the `B=4000` draws, §4.1), and require **at least 95% of sampled replicates to individually
fall within a frozen tolerance band** of the real value — the pass rule is a passing *fraction*
across replicates, not a single pooled number:

- same-bar volume/range Spearman correlation (target: each sampled replicate's own
  `pseudo_volume_t` should individually reproduce it closely, since `pseudo_volume_t` — §4.4 step 3
  — is built from each row's own real baseline features and should therefore still correlate with
  real range at roughly the real strength, even though the *residual* driving it is permuted);
- conditional volume distribution across continuous-range quantiles (real vs. each sampled
  replicate's own reconstruction);
- volume autocorrelation and range autocorrelation (bar-level, both series, per replicate);
- cross-correlation between volume and range at lags −4 through +4 (per replicate — this is also
  where §3.4's frozen 4-trading-day embargo gets its own empirical check, not just an analytical
  one);
- time-of-day distribution of `pseudo_volume_t` vs. real volume (per replicate).

**A finding that fewer than 95% of sampled replicates individually clear any of these is a
load-bearing finding under this design's own D8 ("a pilot failure is a designed outcome") — it
routes to a dated amendment of §4.2–§4.5, not a tolerance widening, and not proceeding to Packet
C2/C3 regardless.** This gate is named here so it cannot be quietly skipped, or quietly weakened to
a pooled check, when Packet C1 is actually executed.

**Per-diagnostic pass criterion — a frozen method, not a number chosen after seeing the data
(corrected 2026-08-31, Codex fourth-pass review, Finding 3) — an earlier draft froze the 95%
passing *fraction* but never said what "individually clear" *means* per diagnostic, which would
have let Packet C1 pick tolerance bands after already seeing the real-vs-null values.** Frozen now,
uniformly across every diagnostic listed above, following this design's own established pattern of
freezing a *method* where the *number* can only come from real data (§4.3's block-length precedent
in the retired round-2 draft, now generalized): a sampled replicate **passes** a given diagnostic
if that diagnostic's own real-data value falls inside a **90% day-blocked bootstrap confidence
interval**, computed from the real (observed) panel alone via day-level block resampling (matching
this design's own trading-day dependence-blocking convention, §4.5's own inference-blocking
discipline) — not an arbitrary manually-chosen numeric band, and not refit per replicate (the CI is
a property of the real data, computed once). This converts "does this replicate look adequate" into
a single, reproducible, pre-specified statistical test per diagnostic per replicate, closing the
degree of freedom Finding 3 named.

---

## 5. B4 (continued) — Distinct-WHO reporting

Comparison 2 (§3.1) is run through the same fold structure and re-estimation discipline as
Comparison 1, with its **own, separately-orthogonalized residualization** (§4.5) but the **same
global rotation draw** for a given replicate index (§4.3 step 5, §4.5's own disambiguation of what
is separate vs. shared between the two comparisons). Its own Brier improvement and attribution
p-value are reported in the same results artifact as Comparison 1's, explicitly labeled
`distinct_who`, and never substituted for or averaged with Comparison 1's own figures. The parent
brief's own verdict map (§6) is unchanged by this design and is not consulted for the distinct-WHO
result — there is no verdict for it, only a disclosure.

**Quantitative decision rule — round 3's own fix was itself flawed; reworked once more as a
bootstrap-CI attenuation test, not a permutation test against a joint-zero-effect null (corrected
2026-08-31, Codex fourth-pass review, Finding 4).** Round 1's original mapping ("Comparison 1
clears, Comparison 2 doesn't" → mechanism A) committed the difference-in-significance fallacy.
Round 3's own fix (a paired permutation test on `diff_j = improvement_1_j − improvement_2_j` over
null replicates) does not actually repair this: every null replicate independently nulls out
*both* comparisons' own volume associations to zero, so `diff_j`'s own reference distribution
describes "what the difference between two noise statistics looks like when neither effect is
real" — not the question actually being asked, which presupposes Comparison 1's effect **is**
real (it already cleared) and asks only whether adding the extra control *attenuates* that
already-established, nonzero effect. A test built from a joint-zero-effect null cannot answer a
question that starts from "the effect is real."

**Fix: a day-blocked bootstrap confidence interval on the observed difference itself, not a
permutation test against any null.** This sidesteps the wrong-null problem entirely — it asks
directly what the real data's own sampling variability says about `diff_obs =
comparison1_observed_improvement − comparison2_observed_improvement`, without needing to specify
what "the null world" should look like for a quantity that is not being tested against zero-effect
in the first place. Resample trading days with replacement (day-blocked, matching §4.5's own
inference-blocking convention — never bar-level IID resampling), recompute both comparisons'
observed improvements and their difference on each resample, and form a two-sided 90%
percentile confidence interval for `diff_obs` (matching `alpha=0.05` per tail, the same threshold
already frozen for Comparison 1, not a second number).

| Comparison 1 (primary) | Result | Disclosure |
|---|---|---|
| `p_upper ≤ 0.05` (clears) | 90% CI for `diff_obs` excludes 0, lower bound `> 0` — Comparison 2's own improvement is confidently smaller | Mechanism A — "same phenomenon, finer grain": volume's own increment is confidently reduced once daily-range-state is also held fixed. |
| `p_upper ≤ 0.05` (clears) | 90% CI for `diff_obs` includes 0 — no confident reduction | Mechanism B — genuinely distinct information source: volume's own increment survives daily-range-state conditioning with no confidently-detected shrinkage. |
| `p_upper > 0.05` (does not clear) | — (CI not evaluated) | Moot — Comparison 1 itself did not clear; the mechanism-attribution question does not apply, per the parent brief's own verdict map (§6), which already stops at a non-clearing L5 outcome before any distinct-WHO framing is relevant. |

No other configuration is possible under this table by construction (Comparison 2 and the CI are
evaluated only when Comparison 1 clears), so this rule is total over the reachable outcome space,
not merely the common cases.

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
   coarsely it's stratified. **Sharpened once more, round 3:** orthogonality to continuous
   `range_t` alone does not imply orthogonality to `bias_range_t` (a nonlinear function of a
   drifting trailing threshold, not a linear transform of `range_t`) — §4.2's formula now includes
   `bias_range_t` explicitly. §4.6 freezes a mandatory Packet C1 adequacy gate (same-bar Spearman,
   conditional-volume-by-range-quantile, ACF, cross-correlation, ToD distribution — checked **per
   replicate against a frozen bootstrap-CI pass criterion**, round 4, not pooled, round 3, and not
   left to an unspecified tolerance, round 4's own Finding 3) precisely so this claim is checked
   empirically before Packet C2/C3, not trusted on the strength of the analytical argument alone.
2. **Can information cross a rolling-fold boundary through normalization, residualization, or
   hyperparameter fitting?** Purge (§3.4) removes training rows whose own trailing *feature* window
   touches a test block **and** rows whose own *label* horizon reaches into the test block (added
   2026-08-31, Codex review, B5 — the original draft only purged on the feature side, which misses
   the one training row per fold whose 1-bar-ahead label is computed from the test block's own
   first bar); embargo removes training rows immediately after a test block, per §3.4's own
   information-interval statement. **Corrected 2026-08-31 (Codex fourth-pass review, Finding 9) —
   what's fold-local vs. global changed.** §4.2's residualization is now fit *globally* per
   replicate (§4.3's own note on why — it is a nuisance step in constructing the null, not itself
   scored, so a global fit carries no leakage risk), which is what makes a single replicate one
   coherent transformation of the whole panel rather than a per-fold patchwork. What remains
   strictly fold-local, purged, and embargoed is the *scored* object: `baseline_1`/`augmented_1`
   themselves, refit fresh per fold per replicate on only that fold's own training rows — this is
   where OOS purity actually needs to live, and it is unchanged. `C` remains the one named, defended
   exception (fixed once from the setup period alone, never per-replicate).
3. **Is every fitted component re-estimated in each replicate?** Yes, with one narrowly-scoped and
   defended exception — §4.4 lists all five steps explicitly re-run per replicate, and separately
   names `C` as the sole value fixed once (from the setup period alone, round 3's own Finding 11
   fix — never from any fold's own test-adjacent data). This is the design's central answer to the
   day-level design's
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

**Review status, round 3 (2026-08-31) — no P0s this time; the round-2 architecture holds.** A
third Codex review, triggered explicitly after the round-2 push, found 12 more findings — 6 P1
(the residualization still didn't include `bias_range_t`, only continuous range; fold 1 had zero
training rows by construction; day-vectors with mismatched slot masks had no defined swap rule;
the day-level regime bucket definition conflated two different thresholds from the cited
construct; `C` selected via nested CV risked leaking later folds' test labels if pooled across
folds; and — the most consequential — L5's own feature had drifted from the frozen binary
hypothesis L1–L4 and H-VOLREGIME actually make, onto a continuous stand-in that tests a different,
more general claim) and 6 P2 (Comparison 2 reused Comparison 1's own residual rather than its own;
excluding identity within each rotation group narrowed the null space relative to
`circular_shift_null_p`'s own established convention; adequacy diagnostics gated on a pooled
average rather than a per-replicate passing fraction; the parent brief's own summary text still
described the retired block-permutation null; the embargo length was still an unfrozen minimum,
not an exact number; and the distinct-WHO table compared two separate significance decisions
rather than testing the difference between them directly). **All addressed** — see §8's own entry.
No P0s this round means the core architecture from round 2 (orthogonalize-then-permute, day-level
circular shift reusing `circular_shift_null_p`) held up under a third pass; what remained were
real implementation-completeness gaps, one of which (the binary-vs-continuous feature drift) was
serious enough to warrant reverting a round-2 decision rather than patching around it.

**Review status, round 4 (2026-08-31) — one structural finding, folded together with two others
from the same round into a single architectural fix.** A fourth Codex review, triggered explicitly
after the round-3 push, found 9 more findings — 5 P1 and 4 P2, no formal P0 label, though Finding 9
was treated with P0-level seriousness. **Finding 9:** null replicates were drawn *independently per
fold*; since expanding folds overlap (a day is a test row in one fold and a training row in every
later one), independent per-fold draws meant a single "replicate `j`" was not one coherent
transformation of the observed panel, undermining the pooled statistic's own calibration. **Finding
1** (the reconstruction threshold was frozen at a fold's real-data fit rather than recomputed
causally) and **Finding 7** (the day-level regime bucket was classified once at a fold boundary,
going stale across a 6-month test block) turned out to be the same underlying problem surfacing
elsewhere — all three resolved together by making the null a single global, causally-consistent
construction per replicate, computed once over the whole panel, with only the *scored* predictive
models remaining fold-local. Also fixed: `pseudo_bias_volume`'s comparator didn't match MNQ's own
inclusive `>=` convention (Finding 2); the residual was standardized before being added to a
log-volume-scale fitted value, a units bug left over from a feature no longer used that way (Finding
5); the adequacy gate's 95%-passing-fraction rule had no frozen per-diagnostic pass criterion
(Finding 3); Comparison 2's own singleton-group exclusion wasn't propagated to scoring (Finding 6);
the plan doc's own original B4 task description still read as the retired block-permutation
instruction (Finding 8); and round 3's own paired-difference fix for the distinct-WHO table tested
against the wrong null (a joint-zero-effect world, when Comparison 1 has already established a
nonzero effect) — replaced with a day-blocked bootstrap CI on the observed difference directly
(Finding 4). **All addressed** — see §8's own entry. This round's central lesson: a finding rated
P1 rather than P0 is not a signal to treat it as isolated — Findings 1, 7, and 9 were three symptoms
of one design gap, and fixing them separately would have left the seams between the fixes exactly
where the next review would have found them.

**Review status, round 5 (2026-08-31) — clean. B5 is complete.** A fifth Codex review, triggered
explicitly after the round-4 push (`74693d7`), returned **no findings** — no inline comments, and
the review's own completion state matches Codex's documented "reacts with 👍 once all reviews
finish with no findings" convention for a clean pass. Four consecutive rounds each surfaced real,
independently-verified defects (9, 8, 12, and 9 findings respectively — 3 P0 total, concentrated in
rounds 2 and 3); round 4's fix (one global, causally-consistent replicate construction, resolving
three separately-numbered findings that traced to the same gap) held up under this fifth pass with
nothing further surfaced. That is the convergence signal this process was watching for, not merely
the absence of a sixth round: **B5's adversarial design review is satisfied as of this entry.** No
pilot code has been written or executed under any version of this design, and no real L5 statistic
has been inspected at any point across all five rounds.

---

## 7. Next step

**B5 complete (2026-08-31).** B5's adversarial design review was routed through this PR's own Codex
review pass rather than an in-session panel — operator decision, 2026-08-31 — and ran five rounds
(§6's own review-status entries), the fifth returning no findings after four rounds of real,
addressed defects. §6's pre-answers stood as the design's own opening position for that review, not
a substitute for it; the actual review is what closed it out.

**Next gate: Packet C1 — pilot validation of the machinery, not the hypothesis.** This design
document does not authorize Packet C1 by itself; per the plan doc's own gate table, Packet C needs
its own separate operator GO, distinct from this design being frozen. Packet C1 must not run the
observed L5 statistic — its job is to freeze pilot acceptance bands, then run the null-size study
(C2), the planted-effect power study (C3), and the absolute model-adequacy checks (C4) this design
specifies, including §4.6's own mandatory adequacy-diagnostic gate. Only if Packet C passes does
Packet D (one-shot real execution) become reachable, and Packet D needs its own separate GO plus a
K declaration on top of that.

Any load-bearing finding discovered during Packet C1 itself still returns here as a dated amendment
to this file (§8) before proceeding further; freezing B5 closes the design-review gate, it does not
retroactively immunize §3–§5's choices from correction if the pilot's own empirical checks
disagree with them.

---

## 8. Amendment log

| Date | Change | By |
|---|---|---|
| 2026-08-31 | Initial design draft (B2–B5), submitted for adversarial review. No code written or executed. | Claude Code |
| 2026-08-31 | **Codex review round 1 (PR #241) — 9 findings, all addressed.** 4 load-bearing: (1) baseline was missing the continuous trigger-bar range B2 itself specifies, admitting a volume-as-range-proxy confound the within-stratum null wouldn't catch — added; (2) the attribution null only permuted training-fold volume, scoring against real test-fold volume, breaking the replicate statistic's exchangeability with the observed one — fixed to permute one consistent draw across train and test rows together; (3) purge only covered feature-side lookback, missing that a 1-bar-ahead label leaks the test block's first bar into the preceding training row — added label-horizon purging; (4) the pre-registration's "two-sided p_upper" was internally inconsistent with this repo's one-sided convention and the design's own declared direction — resolved to a precise one-sided upper-tail definition in both this file and the pre-registration. 5 lower-severity: fold layout frozen exactly (6-month blocks, mechanically-derived count) rather than left as a 5-10-fold range; RTH boundary given an explicit, correctly-sourced definition rather than pointing at `byyear_l4.py`'s unrelated trading-day-rollover rule; block-length selector narrowed to one algorithm (Politis-White via `arch.bootstrap`) rather than a two-option menu; warm-up corrected to per-slot occurrence counts rather than a flat bar count; distinct-WHO mechanism-A/B labels given a quantitative decision table reusing the existing `alpha=0.05` threshold. No result computed under any of the corrected wording — all 9 were caught before any pilot code existed. | Claude Code, responding to Codex's PR #241 review |
| 2026-08-31 | **Codex review round 2 — 8 findings, all addressed; §4 reworked in full.** Round 1's fixes were real but did not reach the central defect: the attribution null claimed binary `(slot, bias_range)` stratification "preserved" the continuous ρ≈0.86–0.88 same-bar volume/range correlation it needed to hold fixed; it didn't, and permuting a residual that still carried most of that continuous signal, within a coarse binary bucket, risked crediting volume for a regularization/collinearity artifact the null itself would never reproduce (P0, Finding 1). **Fix, §4.2:** volume is now residualized, in log space, against the full `baseline_1` feature set jointly (continuous range included, not just its binary indicator) — orthogonal to those regressors by OLS construction, leaving little confound-relevant signal for any permutation to mishandle. **Fix, §4.3:** the permutation unit itself was underspecified (Finding 3 — a "contiguous block" in same-cell-occurrence order is not contiguous in market time); replaced bar-level block-permutation with a day-level circular shift of whole residual vectors, stratified by `daily-range-state-persistence`'s own day-level regime split, reusing this repo's own already-reviewed `circular_shift_null_p` mechanism (PR #207) rather than inventing a new one — this also retires the earlier round-1 block-length-selector fix (`arch.bootstrap.optimal_block_length`) as superseded, not silently dropped. **Fix, §4.4:** made the pseudo-volume reconstruction explicit end to end (Finding 4) — `pseudo_log_volume = real fitted value + permuted residual`, exponentiated for strict positivity — and switched `augmented_1`/`augmented_2`'s own volume feature from the binary `bias_volume` indicator to the continuous standardized residual directly, which also eliminates the separate "how does the binary threshold get recomputed under a null" question Finding 4 raised, since there is no threshold to recompute. **Fix, §4.4:** named and defended the one nuisance parameter (logistic `C`) fixed once from real data rather than re-estimated per replicate, and tied that exception's validity to Packet C1's own null-size study rather than asserting it's harmless (part of Finding 6). **Fix, §4.1:** switched the primary estimand from equal-fold-weighted to pooled out-of-fold Brier improvement (Finding 8), with equal-fold reported as a secondary diagnostic; froze the replicate count at `B=4000` (matching this construct's own `c3_stratified_rerun.py` precedent) and added the standard add-one finite-replicate correction to `p_upper`. **Fix, §3.4:** added a precise, interval-based purge/embargo statement (Finding 7) alongside the existing bullets rather than replacing them, since they were not substantively wrong, only insufficiently rigorous. **Fix, pre-registration §C (P0, Finding 2):** the section heading read "NEVER GATES... TYPES the verdict," directly contradicting §D's own verdict map (which already routed a valid-non-clearing L5 to `FALSIFIED`) — a defect that predated Packet B and was inherited, not introduced, by this amendment; corrected the heading to state plainly that L5 gates, matching what §D and this design's own `baseline_1`/Comparison-1 language already implemented. **Added, §4.6:** a mandatory Packet C1 null-adequacy diagnostic gate (same-bar Spearman, conditional-volume-by-range-quantile, ACF, cross-correlation, ToD distribution, real vs. null-replicate-pooled) — Finding 1's own required correction, so the analytical fix above is empirically checked before Packet C2/C3, not merely asserted. No pilot code exists and no real L5 statistic was inspected under any version of this design. | Claude Code, responding to a second Codex review round on PR #241 |
| 2026-08-31 | **Codex review round 3 — 12 findings, all addressed; no P0s, round 2's architecture holds.** **Fix, §3.1/§3.3/§4.4 (P1, Finding 9 — a course-correction, not a patch):** L5's own feature had drifted, in round 2, from H-VOLREGIME's and L1–L4's frozen *binary* `bias_volume` claim onto a continuous residual stand-in — a different, more general test than the hypothesis actually makes. Reverted to `bias_volume`; §4.4 now reconstructs it under a null replicate by applying the same real `tod_threshold` rule to reconstructed pseudo-volume, closing the exact gap the round-2 switch was trying to avoid, this time with the machinery to do it properly. **Fix, §4.2 (P1, Finding 1, continued):** the joint regression was still missing `bias_range_t` — orthogonality to continuous range does not imply orthogonality to its own nonlinear, drifting-threshold binary indicator; added explicitly. **Fix, §3.4 (P1, Finding 2):** fold 1 had zero training rows by construction (test blocks started at the first scoreable bar); added a 12-month training-only setup period, reserved before fold 1 begins. **Fix, §4.3 (P1, Finding 3):** day-vectors could have mismatched scoreable-slot sets with no defined swap rule; added slot-mask matching as a second stratification dimension alongside the day-level regime bucket. **Fix, §3.1/§4.3 (P1, Finding 5):** `daily-range-state-persistence` defines two different thresholds (P80 trigger, P50 outcome), and this design's "top quintile vs. trailing median" phrasing conflated them; pinned to the P80 conditioning threshold alone throughout. **Fix, §4.4 (P1, Finding 11):** `C`-selection via nested CV, if pooled across expanding folds, leaks later folds' test labels into earlier folds' own "OOS" scoring; scoped `C`-selection to the 12-month setup period alone, which by construction touches no fold's own test block. **Fix, §4.5 (P2, Finding 4):** Comparison 2 had been reusing Comparison 1's own residual, leaving it non-orthogonal to `baseline_2`'s own added prior-day-regime control — the same collinearity-artifact mechanism Finding 1 fixed for Comparison 1, reopened for Comparison 2; added a second, separate residualization including that control, sharing only the rotation *draw* (not the residual) with Comparison 1, for a valid paired design. **Fix, §4.3 (P2, Finding 6):** excluding identity within every rotation group was more restrictive than `circular_shift_null_p`'s own established "identity included" convention; corrected to include it, handling only the single global all-identity combination via the existing add-one correction. **Fix, §4.6 (P2, Finding 7):** adequacy diagnostics gated on a pooled average across replicates, which can hide individual replicates that fail in opposite directions and average out; switched to a per-replicate passing-fraction gate (≥95%). **Fix, parent brief §7/§11 (P2, Finding 8):** the brief's own summary text still described the retired block-permutation/`tod_threshold`-only null; synchronized with the current design. **Fix, §3.4 (P2, Finding 10):** embargo was "at least the longest lag/window," not an exact number; frozen at 4 trading days, tied to the already-frozen lag-4 range-lag depth. **Fix, §5 (P2, Finding 12):** the distinct-WHO table compared two separate significance decisions (a difference-in-significance fallacy); replaced with a direct paired-difference test (`p_upper_diff`) over the same, now-paired replicate draws. No pilot code exists and no real L5 statistic was inspected under any version of this design. | Claude Code, responding to a third Codex review round on PR #241 |
| 2026-08-31 | **Codex review round 4 — 9 findings, all addressed; §4.2–§4.5 reworked again around one architectural fix.** Findings 1, 7, and 9 turned out to be the same underlying gap: null replicates were drawn *independently per fold* — since expanding folds overlap (a day is a test row in exactly one fold and a training row in every later one), independent per-fold draws meant "replicate `j`" was not one coherent transformation of the observed panel (Finding 9), the reconstruction threshold was frozen at a fold's real-data fit rather than recomputed causally (Finding 1), and the day-level regime bucket was classified once at a fold boundary, going stale across a 6-month test block (Finding 7). **Fix, §4.2–§4.4:** the null is now a single, global, causally-consistent construction per replicate — one global rotation draw (§4.3 step 5), one causal reconstruction pass over the whole panel in chronological order (§4.4 step 2), one global day-level regime classification shared across all replicates (§4.3 step 1, since it depends only on never-permuted real range data). Only the *scored* predictive models (`baseline_1`/`augmented_1` themselves) remain fold-local, purged, and embargoed — that is where OOS purity actually needs to live. **Fix, §4.4 (Finding 2):** `pseudo_bias_volume`'s comparator now matches each instrument's own real convention (`>=` for MNQ, `>` for MYM) rather than a uniform strict `>` — the earlier mismatch meant even the identity rotation wouldn't reproduce MNQ's own real feature on tied rows. **Fix, §4.2 (Finding 5):** dropped residual standardization entirely — a leftover from when the residual was directly the model's own feature (retired in round 3); adding a standardized (unitless) residual to a log-volume-scale fitted value was a real units bug. **Fix, §4.6 (Finding 3):** froze a per-diagnostic pass criterion (real value falls inside a 90% day-blocked bootstrap CI) rather than leaving Packet C1 free to pick tolerance bands after seeing the data. **Fix, §4.3 (Finding 6):** singleton (regime, slot-mask) groups are now excluded from scoring entirely, not merely from the rotation pool while silently retaining their real pairing in every replicate. **Fix, plan doc B4 (Finding 8):** the original task-description text still read as the retired block-permutation instruction; marked explicitly superseded, pointing at `DESIGN.md` as the controlling spec. **Fix, §5 (Finding 4):** round 3's own paired-difference fix tested against a joint-zero-effect null, which cannot answer an attenuation question once Comparison 1 has already established a nonzero effect; replaced with a day-blocked bootstrap CI on the observed difference directly. No pilot code exists and no real L5 statistic was inspected under any version of this design. | Claude Code, responding to a fourth Codex review round on PR #241 |
