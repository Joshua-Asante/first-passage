# Q-ORBPOS-1 — Positive-control method fix: does a corrected bucket-construction method recover the known synthetic regime break the original pipeline missed?

**Status:** Apparatus-repair validation, not a candidate-mechanism test. Uses no real economic,
positioning, or price-external data — synthetic classifiers only (the identical d=2.0 design from
[`POSITIVE_CONTROL.md`](POSITIVE_CONTROL.md), plus one new pure-noise variant for a Type-I check).
Consumes **K=0 / $0**, same reasoning as the original positive control.
**Run:** 2026-08-23, Claude Code (Sonnet 5).
**Trigger:** `POSITIVE_CONTROL.md` found the three-window bucket-split + gate-clearance-direction
pipeline could not recover a strongly-designed (Cohen's d=2.0) synthetic regime-break classifier —
`REJECT`, 0/3 date-correlation clearances, unstable gate-clearance direction. §3 of that document
diagnosed the mechanism: the **expanding causal median** converges to a step-change far too slowly
(still 0.10–0.26 short of the true post-break mean nearly five years after the break), and the
post-break era is **~4.2×** longer than the pre-break era in every classifier's own covered window,
so even a modest per-print post-break misclassification rate produces an absolute count of
mislabeled post-break prints that outnumbers the entire pre-break cohort — contaminating the LOWER
bucket past its 40% date-correlation ceiling regardless of how strong the underlying classifier is.
**Does NOT edit:** `POSITIVE_CONTROL.md`, `RESULTS.md`, the `Q-ORBPOS-1-closure-falsified.md`
closure, or `ops/instruments/MNQ.md`. Does NOT re-test volatility, mean-R, or TFF positioning under
the corrected method — that is explicitly out of scope for this pass (separate future decision,
needing its own scoping) per the task that produced this document.

**Bottom line, stated first:** the specific defect `POSITIVE_CONTROL.md` diagnosed — an expanding
causal median that never catches up to a step-change, letting a duration-imbalanced panel contaminate
the LOWER bucket — is **fixed, decisively**: date-correlation-equivalent clearance goes from 0/3 to
**3/3**, with Fisher's-exact p-values of 10⁻¹⁸ to 10⁻²⁷ and post-break classification accuracy rising
from 76–87% to **98.8–100%**. A Type-I sanity check on pure noise correctly stays at 0/3. **But the
overall, H-ORBPOS-§4-shaped composite verdict is still `REJECT`**, because a second, independent axis
this task was not scoped to fix — gate-clearance-direction stability across windows, already flagged
as an open construction-method ambiguity in `POSITIVE_CONTROL.md` §4 — still fails at W3, on what
looks like a small-sample artifact (n=18 blocks) unrelated to the bucket-construction mechanism this
fix targeted. See §4–§6 for the full breakdown and an honest answer on whether re-testing the three
real candidates under this corrected method would now be worthwhile.

---

## §1 — Recap: exactly what failed, and why (from `POSITIVE_CONTROL.md` §3, read in full before designing this fix)

The original pipeline's bucket construction, unchanged across all three real candidates and this
positive control:

1. `roll_W[i] = mean(extremity[i-W+1 .. i])` — a trailing rolling mean over the classifier's own raw
   weekly values, window `W ∈ {4, 13, 26}` per W1/W2/W3.
2. `threshold[i] = expanding median of roll_W[0..i]` — a **fully-expanding**, causal, cumulative
   statistic: every new print permanently join the pool the median is drawn from, forever.
3. `label[i] = HIGHER if roll_W[i] > threshold[i] else LOWER`.
4. **Date-correlation check:** the HIGHER bucket's day-count must be ≥75% post-cutoff; the LOWER
   bucket's day-count must be ≤40% post-cutoff. Needs ≥2 of 3 windows to clear.
5. **Gate-clearance-direction check:** the HIGHER bucket must clear the cushion-sizing survivor gate
   while the LOWER bucket does not (or the reverse), with the **same sign at every window**.

Diagnosed failure mode (§3 of `POSITIVE_CONTROL.md`, mechanistic, not speculative — confirmed against
the actual run's own print-level ground-truth accuracy table):

- **(3b) Self-referential ceiling:** early in the series (which, for this panel, is entirely the
  pre-break era — 60 prints), the expanding median is built almost exclusively from the *same*
  pre-break population being classified. Comparing a pre-break print to a threshold drawn mostly from
  other pre-break prints is close to a coin flip (54–60% correct, empirically, vs. 50% chance).
- **(3c) Slow convergence:** the expanding median's cumulative-median position, once the post-break
  count (`n_post`) begins to dominate the pre-break count (`n_pre`), sits at roughly the
  `50% − n_pre/(2·n_post)` percentile of the post-break population's own rolled distribution — a
  value that only crawls toward the true post-break median as `n_post → ∞`. With `n_pre=60` fixed for
  all time and `n_post` growing to 251 over nearly five years, the median (measured 1.74–1.90 vs a true
  post-break mean of 2.0 at the panel's last print) never gets close. This produces a **persistent**
  14–24% misclassification rate among post-break prints — not a transient boundary effect, confirmed
  in §3c to occur as late as the panel's own final weeks.
- **(3d) Duration-ratio arithmetic:** with `n_pre=60` and `n_post=251` (a 4.2× ratio), even a modest
  14–24% post-break error rate produces an absolute count of mislabeled-LOWER post-break prints
  (34–59) that is **comparable to or larger than** the entire correctly-labeled pre-break LOWER
  cohort (20–31). The LOWER bucket ends up majority post-break (54–75% observed) — the opposite of
  what the ≤40% ceiling needs — independent of how strong or correctly-signed the underlying
  classifier is.

---

## §2 — Options considered, and the reasoning that selected one (written and frozen BEFORE any corrected-method code was run)

The task named three candidate directions. Each is evaluated here **analytically**, against the
mechanism above — not by trial-and-error execution — because running several variants and reporting
only the one that clears the bar is exactly the best-of-K pattern
(`lesson_snag_best_of_k_anchor_graveyard.md`) this whole exercise exists to avoid.

**(a) Rolling (fixed-window, not fully-expanding) causal median — considered, and its literal form
REJECTED analytically before running anything.**
A sliding window fixes (3c)'s "never forgets the old regime" defect — after the window has fully
rolled past the break, it contains zero pre-break observations. But that is exactly the problem: once
a rolling window sits **entirely inside one stable regime** (no longer straddling the break), its
local median re-centers on **that regime's own local distribution**. Comparing a print to a threshold
freshly re-estimated from its own recent same-regime neighbors reproduces (3b)'s coin-flip mechanism
— not just at the *start* of the series, but **deep in the post-break era once the window is fully
past the transition too**. Concretely: with a plausible window (say 52 prints, ~1 year), only the
first ~52 of the 251 post-break prints (≈21%) would sit in the favorable "window still partly
straddles the break, threshold still artificially low" zone; the remaining ~199 (≈79%) would face a
threshold that has fully re-centered on the post-break population's own local median, making their
own classification close to a 50/50 split. That would put roughly 100 post-break prints at risk of
mislabeling — **more** than the 34–59 the original expanding median produced, not fewer. A literal
sliding window was therefore not run as the primary fix; running it only to watch it fail (or, worse,
tuning the window length until it happened not to) would itself be the forbidden pattern. The
*reasoning* that a fixed window is right — "don't let ancient history contaminate the threshold
forever" — is kept; the *mechanism* is changed (§3 below).

**(b) A base-rate-corrected threshold, alone — considered, rejected as the sole fix.**
Replacing the fixed 75%/40% with a threshold that adapts to the panel's own post:pre duration ratio
would stop the check from failing for a purely arithmetic reason unrelated to classifier quality. But
threshold recalibration alone does not touch *why* the LOWER bucket is contaminated (3c) — it would
just re-grade the same contaminated bucket against a more forgiving bar, which risks quietly loosening
the whole apparatus rather than fixing it. It is retained here only as the *pass/fail statistic*,
layered on top of a threshold-construction fix that actually reduces contamination (§3).

**(c) A statistic that avoids the median-bucket-split shape entirely (point-biserial / direct
pre-post comparison) — the theoretically cleanest option, partially adopted as a supplementary
check, not the primary gate.**
A direct two-sample comparison of the classifier's rolled value against the *known* pre/post label
(not a running self-comparison) sidesteps (3b) and (3c) entirely, because it never re-centers on
local history — it uses the full pre-break and full post-break samples simultaneously. This is
almost certainly the statistically correct tool for the underlying question ("does this classifier's
level differ across the two known eras"). It was **not** made the sole/primary mechanism here because
the downstream economic step (`gate_check_bucket`, reused unchanged) requires two **disjoint,
day-level** buckets to run its Monte-Carlo survivor sim on — a pure correlation coefficient does not
by itself produce a bucket assignment. Replacing that architecture too would be a much larger, riskier
redesign for this pass. Instead, a point-biserial correlation is computed and reported **alongside**
the primary criterion below as a confirmatory, non-gating diagnostic — cheap, and it directly checks
whether the chosen threshold-based fix's pass/fail verdict agrees with the cleanest available
statistic.

**Chosen design: a combination of (a) and (b) — an *anchored* (not sliding) causal threshold, paired
with a base-rate-aware, print-level statistical pass/fail criterion — with (c) folded in as a
non-gating cross-check.** This is the smallest, most surgical change to the existing, already-verified
pipeline: it reuses every downstream function (`daily_label_from_weekly`, `blocks_for_label`,
`gate_check_bucket`, `classify_direction`) byte-for-byte, changing only *how the threshold series is
computed* and *how the date-correlation pass/fail is judged*.

---

## §3 — Frozen design (written and committed before the corrected script was run; unchanged after)

### 3a. Anchored causal threshold (replaces the fully-expanding median for post-break prints only)

```
threshold[i] = expanding_median(roll_W[0 .. i])                      if available_date[i] <  CUTOFF
             = expanding_median(roll_W[0 .. i_freeze])  (frozen)     if available_date[i] >= CUTOFF

i_freeze = the LAST index i with available_date[i] < CUTOFF and roll_W[i] valid (non-NaN)
```

For every pre-break print, this is **byte-identical** to the original `A.build_classifier` — the
expanding median is not touched before the break. The *only* change: once the break is crossed, the
threshold **stops updating** and is held at the value the expanding median had already reached using
the full, generously-sized pre-break sample (60 synthetic prints — already noted in
`POSITIVE_CONTROL.md` §1 as 15× the sparsity floor). This is still fully causal — no print's label
ever uses information from after its own `available_date` — and it uses the **already-known, already
pre-registered** 2021-09-28 break date, which is legitimate here for the same reason a standard
before/after interrupted-time-series design is legitimate: that date comes from an **independent**
source (the price-panel's own documented structural break), not from this classifier's own output, so
anchoring the classifier's baseline window to it is not circular. This directly attacks (3c): a print
deep in the post-break era is no longer compared to a threshold that has been dragged toward the
post-break population's own distribution (and therefore sits near its median by construction); it is
compared to the **pre-break population's own level**, against which a d=2.0 (or larger, once
window-averaged) shift should be overwhelming and *not* decay over time.

### 3b. Print-level, base-rate-aware pass/fail criterion (replaces the fixed 75%/40% day-level thresholds)

The original check operated on **day-level** labels (a weekly label forward-filled across ~5-6
business days), which pseudo-replicates each of the 311 independent weekly prints into ~1,150–1,850
highly autocorrelated "days" — inflating apparent sample size without adding information. The
corrected check operates at the **print level** (the classifier's own native cadence, n≈286–308
valid prints per window after warmup):

```
2x2 table:            POST-cutoff   PRE-cutoff
  label = HIGHER          n11           n10
  label = LOWER            n01           n00

fisher_p           = two-sided Fisher's exact test p-value on the table above
frac_higher_post   = n11 / (n11+n10)
frac_lower_post    = n01 / (n01+n00)
separation_pp      = frac_higher_post - frac_lower_post

window "clears" iff:  fisher_p < ASSOC_ALPHA   AND   separation_pp >= MIN_SEPARATION_PP
                       (sign of separation_pp is checked implicitly: it must be positive)

ASSOC_ALPHA        = 0.01    (frozen)
MIN_SEPARATION_PP  = 0.35    (frozen — matches the original 75%-40%=35pp gap's own stringency,
                               expressed as a required SEPARATION rather than two fixed absolute
                               sides, so the criterion does not scale worse the longer the post-break
                               era grows relative to the pre-break era)
```

Overall corrected date-correlation-equivalent criterion: **≥2 of 3 windows must clear** — identical
structural rule to H-ORBPOS's own §4.

### 3c. Supplementary, non-gating diagnostic (option (c), reported not gated)

Point-biserial correlation between each window's valid `roll_W` values and a binary
post-cutoff indicator, at print level. Reported alongside the primary criterion for transparency;
does not affect the verdict.

### 3d. Everything else — reused unchanged

`daily_label_from_weekly`, `blocks_for_label`/`contiguous_runs`, `gate_check_bucket`,
`classify_direction`, the Ambiguous-hold sparsity trigger (`MIN_W1_PREBREAK_PRINTS=4`), the
"direction same sign at every window" rule, `CUTOFF`, `WINDOWS={4,13,26}`, `K=1`, and the fidelity
control (flat policy, m=1.0, full panel, k=1/k=2) are all imported and used **byte-for-byte** from
`run_orbpos_tff_probe.py` / `_imported_run_evalseq_orb_intraday.py` — no new pipeline logic beyond
§3a/§3b/§3c.

One adaptation forced by freezing: the original "degenerate threshold" check (flags a constant
threshold as pathological) would **always** fire under this design, because the post-break threshold
is *deliberately* held constant. The corrected degenerate check is therefore restricted to the
**pre-break segment only** (where the threshold is still the untouched expanding median) — a constant
threshold after the freeze point is the intended mechanism, not a defect.

### 3e. Synthetic design — identical primary run, plus one new null variant for the Type-I check

**Primary (positive-control) run — IDENTICAL to `POSITIVE_CONTROL.md`, unchanged:**
`MU_PRE=0.0, MU_POST=2.0, SIGMA=1.0, SEED=20260823`, weekly Tuesdays 2020-08-04→2026-07-15,
`CUTOFF=2021-09-28`. Same classifier construction, same seed, same windows.

**Bonus Type-I / null-sanity variant (new, frozen here before running):**
`MU_PRE=0.0, MU_POST=0.0` (pure noise, no true regime difference at all), `SIGMA=1.0`,
`SEED_NULL = SEED + 1 = 20260824` (a deterministic increment of the already-frozen primary seed —
not searched, not chosen after looking at any result). Same date range, same corrected pipeline,
run in the same script execution. Expected result if the corrected method is well-calibrated: **does
NOT** clear ≥2/3 windows with the correct sign — i.e., reports REJECT-equivalent, confirming the
corrected criterion does not manufacture a signal out of nothing.

### 3f. Pre-committed non-negotiables

- None of the parameters above (`i_freeze` rule, `ASSOC_ALPHA`, `MIN_SEPARATION_PP`, `SEED_NULL`)
  are changed after seeing a result.
- **Declared fallback, stated here before running (per the task's own instruction):** if this design
  fails to clear an ACCEPT-equivalent verdict on the primary d=2.0 run, the ONE alternative that will
  be tried is dropping the threshold/bucket architecture as the *primary* gate and using the
  point-biserial/direct association test (§3c, option (c)) as the primary criterion instead — retaining
  a full-sample (non-causal, since the gate step is a retrospective regime-characterization, not a
  live-tradeable rule) median split purely to produce the two buckets `gate_check_bucket` requires. If
  that is tried, it will be reported explicitly as a second, disclosed attempt — not silently
  substituted for the first.
- If both fail, the honest REJECT will be reported as evidence about the difficulty of this
  correction, not force-fit into a pass.

$0 / K=0. No real economic, positioning, or price-external data used or referenced by value anywhere
in the new script. Writes only to this directory.

---

## §4 — Results: the corrected method against the SAME frozen d=2.0 synthetic design

Fidelity control reproduced the published anchors exactly (k=1 bust 67.67%, k=2 bust 77.01%, 0.00pp
delta both), confirming the reused harness is unaffected — identical to both prior rounds.

| Window | HIGHER n (post %) | LOWER n (post %) | Separation | Fisher's exact p | Point-biserial r (p) | Corrected assoc. clears? | Ground-truth: POST→HIGHER acc. | Ground-truth: PRE→LOWER acc. | HIGHER cushion pass | LOWER cushion pass | Direction |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W1 | 277 (90.6%) | 31 (0.0%) | +90.6pp | 3.4×10⁻²⁷ | 0.839 (6.1×10⁻⁸³) | **YES** | 100.0% | 54.4% | 79.84% PASS | 64.42% PASS | `BOTH_CLEAR` |
| W2 | 269 (92.9%) | 30 (3.3%) | +89.6pp | 1.9×10⁻²⁶ | 0.875 (1.7×10⁻⁹⁵) | **YES** | 99.6% | 60.4% | 76.58% PASS | 55.24% PASS | `BOTH_CLEAR` |
| W3 | 263 (94.3%) | 23 (13.0%) | +81.3pp | 1.7×10⁻¹⁸ | 0.826 (1.1×10⁻⁷²) | **YES** | 98.8% | 57.1% | 84.59% PASS | 0.55% **FAIL** | `HIGHER_CLEARS_LOWER_DOES_NOT` |

**The diagnosed defect is decisively fixed.** Every window that previously failed date-correlation
by 15–35 percentage points (§2 of `POSITIVE_CONTROL.md`) now clears the corrected association test
by 81–91 percentage points of separation, at p-values so far below any reasonable significance
threshold (10⁻¹⁸ to 10⁻²⁷) that this is not a borderline call. **Corrected association clears
3 of 3 windows** (needs ≥2) — a complete reversal of the original 0/3. The point-biserial correlation
(the fully independent, non-gating cross-check from option (c)) agrees: r=0.83–0.88, overwhelming and
consistent in sign at every window.

**The mechanistic diagnosis is directly confirmed, not just the pass/fail outcome.** Ground-truth
post-break classification accuracy — the specific number §3c of `POSITIVE_CONTROL.md` identified as
never converging under the expanding median (76–87% even after nearly five years) — jumps to
**98.8–100.0%** once the threshold stops drifting after the break. This is exactly the predicted
effect of freezing the threshold at the pre-break level instead of letting it be dragged toward the
post-break population's own median: post-break prints are now compared against a *fixed, distant*
reference (the pre-break baseline) rather than one that re-centers on their own regime. Pre-break
accuracy (54–60%) is essentially unchanged from the original run, exactly as anticipated in §2's
up-front reasoning — the self-referential-ceiling mechanism (3b) was never targeted by this fix and
does not need to be, since it does not materially contaminate either bucket once the post-break side
is fixed (LOWER bucket contamination is now 0.0–13.0% post-break, comfortably under any reasonable
ceiling, driven almost entirely by the untouched pre-break-era coin-flip, not by post-break leakage).

**The overall composite verdict is still `REJECT` — but for a reason unrelated to the mechanism this
fix targeted.** H-ORBPOS's own §4 shape requires *both* (i) date-correlation-equivalent clearance at
≥2/3 windows and (ii) gate-clearance direction the same sign at *every* window, no exceptions.
(i) now passes cleanly (3/3). (ii) fails: W1 and W2 both land on `BOTH_CLEAR` (both buckets separately
clear the cushion-sizing survivor gate — not a "signed" direction under `classify_direction`'s own
definition), while W3 lands on `HIGHER_CLEARS_LOWER_DOES_NOT` (a signed direction) — so
`direction_same_sign_every_window` evaluates `False`, exactly as it did in the *original*, broken-date-
correlation run (which hit the identical `BOTH_CLEAR, BOTH_CLEAR, HIGHER_CLEARS_LOWER_DOES_NOT`
pattern for W1/W2/W3 — see `POSITIVE_CONTROL.md` §2's own table). This is a **pre-existing, already-
disclosed, and independent** open question: `POSITIVE_CONTROL.md` §4's second caveat already flagged
"the gate-clearance-direction axis inherits the same open construction-method ambiguity the real
closure already disclosed" as a *separate* axis from the date-correlation mechanism this task was
scoped to fix. `gate_check_bucket`/`classify_direction` are reused **byte-for-byte** here — nothing
about how the economic/survivor-gate check itself is computed changed in this pass, only how the
buckets fed into it are constructed, and construction is no longer the bottleneck (buckets are now
cleanly separated by era: 90–94% of HIGHER is post-break, 87–100% of LOWER is pre-break).

**A specific, disclosed observation about the W3 anomaly (not chased further — out of this pass's
scope):** W3's LOWER bucket has the *smallest* sample of the three windows (n=23 valid prints, 18
usable 5-day blocks after contiguous-run construction) and the *highest*, not lowest, post-break
contamination among the three windows (13.0% vs 0.0%/3.3%) — yet it is the one bucket whose cushion
pass rate collapses to 0.55%. Contamination magnitude does not explain this ordering. The more likely
explanation is that a small block count (18) makes the Monte-Carlo survivor estimate highly sensitive
to which specific real calendar days happen to fall in that bucket — an artifact of small-N gate
evaluation, not of the synthetic classifier's validity, but this was not separately diagnosed further
here, consistent with the task's own scope boundary (fixing the diagnosed bucket-construction defect,
not re-investigating the gate-clearance-direction step's own construction-method ambiguity, which
`POSITIVE_CONTROL.md` already flagged as follow-on work in its own right).

**Declared fallback (§3f) was NOT invoked.** The one alternative reserved in advance — dropping to a
pure point-biserial/full-sample-median primary criterion — was not tried, and the reasoning is stated
here rather than silently skipped: the mechanism that fix targets (median-split bucket construction)
is not what is failing anymore. The residual failure sits entirely in `classify_direction`'s
"same-sign-every-window" rule interacting with a small-N bucket at W3 — a downstream step reused
unchanged regardless of which upstream discretization method produced the buckets. Trying the
alternative anyway, hoping it happens to also change the W3 gate-clearance outcome, would be
searching for a fix to a problem the alternative was never reasoned to address — exactly the
best-of-K pattern this exercise exists to avoid. The honest report is: **the targeted defect is
fixed; a separate, already-disclosed defect is not, and fixing it was out of scope here.**

---

## §5 — Bonus Type-I / null sanity check: does the corrected method stay quiet on pure noise?

Same corrected pipeline, same panel, same windows — run once more on a synthetic series with
**`MU_PRE=MU_POST=0.0`** (no true regime difference at all), `SIGMA=1.0`, `SEED_NULL=20260824` (a
frozen `SEED+1` increment, not searched).

| Window | HIGHER n (post %) | LOWER n (post %) | Separation | Fisher's exact p | Point-biserial r (p) | Corrected assoc. clears? | Ground-truth accuracy (chance≈50%) |
|---|---|---|---|---|---|---|---|
| W1 | 162 (83.3%) | 146 (79.5%) | +3.9pp | 0.463 | 0.135 (0.018) | no | pre 52.6% / post 53.8% |
| W2 | 174 (83.3%) | 125 (84.8%) | −1.5pp | 0.753 | 0.187 (0.001) | no | pre 39.6% / post 57.8% |
| W3 | 183 (88.5%) | 103 (86.4%) | +2.1pp | 0.707 | 0.160 (0.007) | no | pre 40.0% / post 64.5% |

**Corrected association clears 0 of 3 windows** — none of the Fisher's-exact p-values (0.46–0.75)
come close to `ASSOC_ALPHA=0.01`, and separation is a few percentage points in either direction, not
the 81–91pp seen under the true d=2.0 signal. Ground-truth accuracy sits at 40–65%, consistent with
noise (the ~52–65% band, rather than a flat 50%, reflects the frozen-post-cutoff-threshold's own
mild residual dependence on where the pre-break sample's median happened to land under this
particular noise draw — not a detected relationship; the p-values above are the operative test, and
they are unambiguous). **Verdict: `REJECT`, correctly** — the corrected criterion does not manufacture
a pass out of pure noise. This is the intended Type-I behavior, mirroring the `rho_target=0.00` row
in MNQTAPE-1's own power-check design
([`mnqtape1_power_check_2026-08-23/power_check.py`](../mnqtape1_power_check_2026-08-23/power_check.py)).

Note also that the null run's *own* gate-clearance-direction is unstable in the same
`BOTH_CLEAR`/signed-exception pattern (`BOTH_CLEAR, LOWER_CLEARS_HIGHER_DOES_NOT, BOTH_CLEAR`) —
independent supporting evidence that this axis is noise-sensitive for buckets of this size
*regardless* of whether any real signal is present, reinforcing §4's conclusion that it is a separate,
weaker axis rather than a consequence of the bucket-construction defect fixed here.

---

## §6 — Honest overall assessment

1. **The specific, diagnosed defect — expanding-median bucket construction failing to date-correlate
   with a known step-change under a duration-imbalanced panel — is fixed, decisively and for the
   mechanistic reason predicted in advance, not by accident.** 0/3 → 3/3 clearance, p-values of
   10⁻¹⁸ to 10⁻²⁷, post-break classification accuracy 76–87% → 98.8–100%. This is real, verified
   evidence that an anchored (freeze-after-break) causal threshold plus a print-level, base-rate-aware
   association test is a usable replacement for the fully-expanding-median + fixed-75%/40%-day-level
   construction, for the specific failure mode this positive control exists to probe.
2. **The composite, H-ORBPOS-§4-shaped verdict is still `REJECT`**, because a second, independent,
   already-disclosed axis (gate-clearance-direction stability across windows, governed entirely by
   the unchanged `gate_check_bucket`/`classify_direction` machinery) still fails — and it fails for
   what looks like a small-sample artifact at W3, not for a reason connected to the bucket-
   construction mechanism this task was scoped to repair.
3. **Would re-testing the three real candidates (volatility, mean-R, TFF positioning) under this
   corrected method be worthwhile?** Conditionally yes, but with an explicit caveat that should travel
   with any such re-test: this fix demonstrably repairs the date-correlation half of the pipeline (the
   half `POSITIVE_CONTROL.md` identified as structurally near-incapable of clearing under this panel's
   duration imbalance) — a real candidate that clears the corrected date-correlation test at ≥2/3
   windows would now be meaningful evidence in a way it was not before. But a candidate's overall
   verdict would *still* also depend on the not-yet-repaired gate-clearance-direction axis, which this
   positive control shows can flip on a small-N technicality even when the underlying classifier is
   as clean as it is possible to be (near-perfect era separation). **Recommendation:** re-testing the
   three real candidates under the corrected date-correlation construction is worth doing as a
   separate, explicitly-scoped follow-on (per this task's own instruction not to fold that in here) —
   but any resulting `ACCEPT`-equivalent or `REJECT`-equivalent verdict should be reported with the
   two axes broken out separately (date-correlation pass/fail vs. direction-stability pass/fail),
   rather than collapsed into one composite label, until the gate-clearance-direction
   construction-method ambiguity itself gets the same kind of dedicated scrutiny this document just
   gave the date-correlation half.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Design frozen (§1-§3), corrected method implemented and run once against the identical d=2.0 synthetic design plus one new pure-noise Type-I check. Targeted defect fixed (3/3 date-correlation clearance, up from 0/3); composite verdict remains REJECT due to a separate, already-disclosed gate-clearance-direction instability out of this task's scope. Declared fallback not invoked (reasoned why). Type-I check confirms no false positive on pure noise. | Claude Code (Sonnet 5) |
