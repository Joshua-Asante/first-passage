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
- `augmented_1`: `baseline_1` + trigger-bar time-of-day-normalized volume state (`bias_volume`,
  already computed) + only those volume lags declared in §3.3.
- This is the primary test of "does volume add incremental forward information beyond intraday
  seasonality and the trigger bar's own range state" — the question H-VOLREGIME-{MNQ,MYM} actually
  asks. Matches the plan doc's own B2 baseline bullet ("trigger-bar realized range and
  own-range-elevated indicator") verbatim; the correction above brings this section back into
  conformance with that spec rather than introducing a new requirement.

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
- Volume lags for `augmented_1`/`augmented_2`: **lag-0 (trigger bar) only.** No additional volume
  lags are added — B2's "only those volume lags declared before the pilot" is satisfied by
  declaring zero beyond lag-0, since the parent brief's own H-VOLREGIME hypothesis is about the
  trigger bar's own volume state, not a volume-lag structure nobody has hypothesized. Any future
  volume-lag extension is a new design, not a retune of this one.
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

### 4.1 Primary statistic

**Frozen: mean out-of-fold Brier score improvement**, `improvement = Brier(baseline) −
Brier(augmented)`, averaged across all test folds (equal fold weighting, not sample-size
weighting — a declared choice, since unequal calendar coverage per fold should not let one dense
fold dominate). Brier is chosen over log loss because it is bounded ([0, 1] per prediction) and
does not blow up on a near-certain wrong prediction the way log loss can on a rare, poorly
calibrated tail bar — a property that matters more here than log loss's sharper penalty on
confident errors, given this design has not separately validated calibration robustness in the
tails. `improvement > 0` favors the augmented (volume-including) model.

**`p_upper` tail definition (added 2026-08-31, Codex review, B5 — resolves an inherited
inconsistency).** The pre-registration's own §C originally described this design's attribution
p-value as "two-sided p_upper," which is self-contradictory: this repo's existing `p_upper`
implementations (e.g. the L1–L4 within-stratum `circular_shift_null_p`) are one-sided, upper-tail
tests, and this design already declares a favorable direction (`improvement > 0`). Frozen here,
one-sided: `p_upper = P(replicate_improvement ≥ observed_improvement | null)`, the fraction of null
replicates (§4.4) whose own Brier-score improvement is at least as large as the real, observed
improvement. `p_upper ≤ 0.05` clears; no two-sided or absolute-value variant is computed or
consulted. The pre-registration's own §C is corrected to match, same date.

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

**Block length is a frozen METHOD, not a frozen number, at this stage — one specific algorithm, not
a menu (corrected 2026-08-31, Codex review, B5: an earlier draft named Politis–White "or an
equivalent ACF-decay-threshold rule," which is two different selectors that can produce materially
different block lengths and different null p-values; leaving the choice between them open is the
same un-frozen-parameter problem as the fold-layout fix above, just one level down).** Frozen
algorithm: the **Politis–White (2004) automatic/optimal block-length selector**, with the
Patton–Politis–White (2009) correction, as implemented in
`arch.bootstrap.optimal_block_length` — verified present in this environment (`arch` 8.0.0) rather
than assumed. Use its `b_sb` (stationary-bootstrap) column, matching §4.3's own stationary block
permutation, not `b_cb` (circular). Same package the `strategy-validation` skill's own §8a/§8d
already cite for block-size selection — no second implementation is authored here. Applied to each
instrument's own residual series independently
(§4.2's output, computed on that instrument's full training-eligible panel, not per-fold), producing
a block length in bars; converted to whole trading days by ceiling-dividing by that instrument's own
average bars-per-session count, so the resulting block spans a whole number of sessions rather than
splitting one mid-day. Computed once as the first act of Packet C1 and held fixed through the rest
of the pilot and any eventual Packet D execution. Freezing the algorithm now and its numeric output
at first real contact with the data (rather than guessing a number now) avoids both under-blocking
(a naive small block that overstates significance) and picking a number that happens to flatter or
hurt the eventual result, since no real residual series has been measured yet.

### 4.4 Re-estimation discipline (the load-bearing fix vs. the day-level design's failure)

**Corrected 2026-08-31 (Codex review, B5) — the null must cover every scored row, not training
only.** An earlier draft of this section permuted volume in the training data, then scored the
resulting model against the real, unpermuted test-fold volume. That is not a coherent draw from the
null world: the replicate would train under a fake volume/outcome relationship but evaluate under
the real one, so its Brier-improvement statistic would not be exchangeable with the observed
statistic, and the resulting `p_upper` would not carry the claimed Type-I calibration. The fix
below applies the same replicate's permutation to every scored row — train and test alike — so
training and scoring both happen inside one consistent null draw; only the outcome label is left
real throughout (permuting volume, not outcome, is what makes this a test of volume's own
information content rather than a generic label-shuffle test).

Every null replicate re-runs, end to end, over that replicate's own single, internally-consistent
null draw of the full scored population for the fold being tested:

1. Re-fit the `tod_threshold` predictable-volume-component estimator (§4.2) on the fold's real,
   unpermuted training-fold data (the predictable-component estimator is not itself part of the
   null being tested — only the *residual*'s pairing with outcome is).
2. Compute the residual for **every scored row in the fold — training and test rows alike** —
   against that estimator, then draw **one** stratified block permutation (§4.3) over that entire
   pool, reassigning which row gets which residual. Training rows and test rows are permuted
   together, from the same draw, not independently.
3. Re-fit both `baseline_1`/`augmented_1` logistic models (and, for the distinct-WHO run,
   `baseline_2`/`augmented_2`) on the replicate's training rows, using **that replicate's permuted
   residual** (recombined with the real `tod_threshold` estimate) as the volume feature — never the
   real observed volume.
4. Score OOS on the replicate's test rows, using those same test rows' **permuted** volume feature
   (from step 2) against their **real, unpermuted** outcome labels. Recompute the Brier
   improvement from this null-world scoring, not from a mix of null-trained-model-on-real-data.

No step in this chain uses a value fit once on the observed data and reused across replicates, and
no step scores a null-trained model against real (non-null) volume features.
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
   hyperparameter fitting?** Purge (§3.4) removes training rows whose own trailing *feature* window
   touches a test block **and** rows whose own *label* horizon reaches into the test block (added
   2026-08-31, Codex review, B5 — the original draft only purged on the feature side, which misses
   the one training row per fold whose 1-bar-ahead label is computed from the test block's own
   first bar); embargo removes training rows immediately after a test block. Every
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
   length (§4.3) is frozen as **one specific algorithm** (Politis–White, via `arch.bootstrap` —
   narrowed from an earlier draft's two-selector menu, 2026-08-31, Codex review, B5) applied per
   instrument, with the resulting number produced only after Packet C1 measures it on real data,
   rather than guessed here and potentially wrong in a way that only an ACF-blind reviewer could
   miss.

**Review status (2026-08-31):** Codex's own review of this design (via this PR) returned 9
findings — 4 load-bearing (baseline missing continuous range; null not applied to test-fold
volume; feature-side-only purge missing the label-horizon leak; an internally inconsistent
"two-sided p_upper" carried over from the pre-registration) and 5 lower-severity (fold layout left
as a range rather than frozen exactly; RTH boundary pointed at the wrong existing convention;
block-length selector left as a two-option menu; warm-up worded as a flat bar count instead of
per-slot occurrences; distinct-WHO mechanism labels left qualitative). All 9 are addressed inline
above, each marked with its own dated correction note, rather than summarized only here — this
section records that the review happened and was resolved, not what changed.

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
| 2026-08-31 | **Codex review (PR #241) — 9 findings, all addressed.** 4 load-bearing: (1) baseline was missing the continuous trigger-bar range B2 itself specifies, admitting a volume-as-range-proxy confound the within-stratum null wouldn't catch — added; (2) the attribution null only permuted training-fold volume, scoring against real test-fold volume, breaking the replicate statistic's exchangeability with the observed one — fixed to permute one consistent draw across train and test rows together; (3) purge only covered feature-side lookback, missing that a 1-bar-ahead label leaks the test block's first bar into the preceding training row — added label-horizon purging; (4) the pre-registration's "two-sided p_upper" was internally inconsistent with this repo's one-sided convention and the design's own declared direction — resolved to a precise one-sided upper-tail definition in both this file and the pre-registration. 5 lower-severity: fold layout frozen exactly (6-month blocks, mechanically-derived count) rather than left as a 5-10-fold range; RTH boundary given an explicit, correctly-sourced definition rather than pointing at `byyear_l4.py`'s unrelated trading-day-rollover rule; block-length selector narrowed to one algorithm (Politis-White via `arch.bootstrap`) rather than a two-option menu; warm-up corrected to per-slot occurrence counts rather than a flat bar count; distinct-WHO mechanism-A/B labels given a quantitative decision table reusing the existing `alpha=0.05` threshold. No result computed under any of the corrected wording — all 9 were caught before any pilot code existed. | Claude Code, responding to Codex's PR #241 review |
