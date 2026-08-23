# Q-ORBPOS-1 — Positive control: does the three-window bucket-split + gate-clearance-direction pipeline recover a KNOWN, designed-to-be-detectable synthetic regime break?

**Status:** Apparatus-validity check, not a candidate-mechanism test. Uses no real economic,
positioning, or price-external data — a synthetic classifier only. Consumes **K=0 / $0** and needed
no fresh pre-registration ceremony, per the same diagnostic-question reasoning
`Q-ORBCUSH-1`/`Q-ORBPOS-1` themselves used (this is one further rung down: a probe of the *pipeline*,
not of any economic construct).
**Run:** 2026-08-23, Claude Code (Sonnet 5).
**Trigger:** an external, non-authoritative second opinion noted that no positive control had ever
been run on the three-window date-correlation + gate-clearance-direction pipeline used to test
volatility, mean-R, and CFTC TFF positioning against ORB-MNQ-1's 2021-09-28 cushion-sizing break
(all three `FALSIFIED`). This document is that positive control.
**Does NOT edit:** `RESULTS.md`, the `Q-ORBPOS-1-closure-falsified.md` closure, or
`ops/instruments/MNQ.md`. Separate, standalone artifact per the task's own instruction.

**Bottom line, stated first:** the pipeline **failed to recover** a synthetic regime-break classifier
that was deliberately constructed to be strongly, if not perfectly, associated with the true
2021-09-28 break (Cohen's d = 2.0 between pre/post regimes). Date-correlation clears **0 of 3**
windows — the identical failure count as the real TFF result — and the gate-clearance direction is
**not stable** across windows either. This is a **surprising, load-bearing finding about the
apparatus itself**, not explained away below: it means the specific bucket-construction method this
pipeline uses (trailing rolling mean, split by the series' own *expanding* causal median, checked
against fixed 75%/40% date-fraction thresholds) has a structural difficulty recovering *any*
persistent, one-time regime shift under a panel shape where the post-break era greatly outlasts the
pre-break era in the classifier's own covered history — which is exactly the shape all three real
candidate tests faced. See §5 for what this does and does not license concluding about those three
nulls.

---

## §1 — Frozen synthetic design (written and committed before the pipeline was run; unchanged after)

Full text also lives in the module docstring of
[`run_orbpos_positive_control.py`](run_orbpos_positive_control.py), reproduced here for the record:

- **Date range:** weekly Tuesdays from **2020-08-04** (the real TFF classifier's own first available
  print date, per `RESULTS.md` Phase 1) through **2026-07-15** (ORB-MNQ-1's own price-panel end,
  `PANEL_END` in `run_orbpos_tff_probe.py`). Both endpoints, and the real break date itself
  (2021-09-28), fall on a Tuesday — verified with the stdlib `datetime` module before writing the
  design, so the synthetic grid's cadence and the real break's own calendar position line up exactly
  as they did for the real TFF pull.
- **Construction — a two-state Gaussian step process, not a trend and not a transient burst:**

  ```
  extremity_synthetic[i] = MU_POST if report_date[i] >= CUTOFF else MU_PRE
                            + SIGMA * eps[i],     eps[i] ~ iid N(0, 1)

  MU_PRE  = 0.0
  MU_POST = 2.0     (Cohen's d = (MU_POST - MU_PRE) / SIGMA = 2.0 — a conventionally "large" effect
                      size, but NOT deterministic: a single raw weekly draw still lands on the wrong
                      side of the population midpoint (1.0) with probability Phi(-d/2) = Phi(-1.0)
                      ≈ 15.9%, per the standard equal-variance two-Gaussian overlap formula)
  SIGMA   = 1.0
  SEED    = 20260823   (np.random.default_rng — today's date at authoring time)
  ```

- **Why a persistent level shift, not a trend or a burst:** this is the same "regime state persists
  for months on either side of the break" shape the real pre-registration's §2.4 argued weekly
  cadence was well-suited to detect. No autocorrelation, drift, or seasonality is added — doing so
  would make this a *less* clean positive control, not a more realistic one, since the object under
  test is whether the pipeline recovers a known step-change, not whether it is robust to nuisance
  structure.
- **Everything downstream is reused, unchanged, by direct import** — no new pipeline logic: the
  causal rolling-window classifier (`build_classifier`), the daily label mapping
  (`daily_label_from_weekly`), the date-correlation check (`date_correlation`), the per-bucket block
  construction (`blocks_for_label`/`contiguous_runs`), and the cushion-sizing gate-clearance check at
  k=1 (`gate_check_bucket`, `classify_direction`) are imported from
  [`run_orbpos_tff_probe.py`](run_orbpos_tff_probe.py) (Implementation A of the real TFF round), and
  the ORB-MNQ-1 panel / firm-rules / fidelity-control machinery is imported unchanged from
  [`_imported_run_evalseq_orb_intraday.py`](_imported_run_evalseq_orb_intraday.py). The only new code
  in [`run_orbpos_positive_control.py`](run_orbpos_positive_control.py) is
  `build_synthetic_tff_like_df()`, which generates the series above and nothing else. This is
  deliberate: the object under test is the *pipeline's* recovery behavior, not a fourth from-scratch
  reimplementation of it.
- **Pre-committed non-negotiable:** none of MU_PRE / MU_POST / SIGMA / SEED / date range would be
  changed after seeing a result. They were not changed. The run reported below is the only run of
  this script's primary pipeline that has ever executed.

**One disclosed, unplanned divergence from the real TFF series, noticed only after running (data
fact, not a parameter change):** the real TFF pull had **45** pre-break prints over
2020-08-04→2021-09-28 (`RESULTS.md` Phase 1) because CFTC's real weekly cadence has gaps (holidays,
irregular publication weeks). A clean Tuesday-anchored `pd.date_range` over the identical calendar
span has no such gaps and produces **60** pre-break prints — 15 more than the real series, i.e. a
*more* generous pre-break sample than the real candidates had, not a less generous one. This is
reported, not corrected after the fact (correcting it now would itself be a form of post-hoc tuning);
it does not favor the REJECT finding below — if anything, extra pre-break history should make
date-correlation *easier* to clear, not harder, so this divergence cannot be the explanation for the
result in §2.

---

## §2 — Results (identical Accept/Reject/Ambiguous-hold shape as H-ORBPOS's own §4)

Fidelity control (flat policy, m=1.0, full panel, k=1/k=2, reused `day_loop_intraday` unchanged)
reproduced the published anchors exactly before any bucket result was trusted: k=1 bust 67.67%/pass
32.33% (0.00pp delta), k=2 bust 77.01%/pass 22.99% (0.00pp delta) — same as both real rounds. The
harness itself is confirmed working; nothing below is contaminated by a broken harness.

Ambiguous-hold-equivalent (sparsity <4 pre-break prints, or a degenerate/constant threshold): **does
not fire** — 60 pre-break prints (15× the floor), no degenerate threshold at any window.

| Window | Higher-bucket post-break frac (day-level) | Lower-bucket post-break frac (day-level) | Date-corr clears? | Higher cushion pass % (gate) | Lower cushion pass % (gate) | Direction |
|---|---|---|---|---|---|---|
| W1 (4 prints) | 89.23% (n=1179 days) | **56.34%** (n=355 days) | No (lower 16.34pp over the 40% ceiling) | 86.23% (PASS) | 98.46% (PASS) | `BOTH_CLEAR` |
| W2 (13 prints) | 91.91% (n=1174 days) | **54.92%** (n=315 days) | No (lower 14.92pp over ceiling) | 86.89% (PASS) | 97.63% (PASS) | `BOTH_CLEAR` |
| W3 (26 prints) | 92.72% (n=1030 days) | **75.38%** (n=394 days) | No (lower 35.38pp over ceiling) | 96.43% (PASS) | 24.89% (FAIL) | `HIGHER_CLEARS_LOWER_DOES_NOT` |

**Date-correlation clears 0 of 3 windows** (needs ≥2 of 3 — the same count of clearances, zero, as
the real TFF result). **Gate-clearance direction is not the same sign at every window** (W1/W2 =
`BOTH_CLEAR`, W3 = `HIGHER_CLEARS_LOWER_DOES_NOT`) — disqualifying under H-ORBPOS's own "same sign at
every window, no exceptions" rule by itself, independent of the date-correlation failure.

**Verdict under H-ORBPOS's own §4 criteria, applied verbatim to this synthetic run: `REJECT` — the
pipeline does NOT recover the known, designed-to-be-strongly-detectable synthetic relationship.**

Full machine-readable output: [`results_orbpos_positive_control.json`](results_orbpos_positive_control.json).
Full run transcript: [`run_log_positive_control.txt`](run_log_positive_control.txt).
Script: [`run_orbpos_positive_control.py`](run_orbpos_positive_control.py).

---

## §3 — Post-hoc mechanistic diagnostic (uses the SAME frozen synthetic series and seed — no new random draw, no parameter change; explains the §2 result, does not revise it)

This section is exploratory and clearly separated from the frozen primary result above. It answers
*why* the REJECT happened, using only deeper decomposition of the one run already committed in §2 —
not a re-run, not a different seed, not a different parameter.

**3a. The raw classifier carries real signal — the failure is downstream of it, not in it.**
Print-level classifier-label-vs-known-ground-truth accuracy (post-warmup):

| Window | Overall accuracy | PRE-break prints correctly LOWER | POST-break prints correctly HIGHER |
|---|---|---|---|
| W1 | 78.6% (n=308) | 31/57 = 54.4% | 211/251 = 84.1% |
| W2 | 82.3% (n=299) | 29/48 = 60.4% | 217/251 = 86.5% |
| W3 | 74.1% (n=286) | 20/35 = 57.1% | 192/251 = 76.5% |

Overall accuracy (74–82%) is far above chance (50%), confirming the synthetic classifier itself is
genuinely informative, as designed. **But it fails asymmetrically, and the asymmetry explains §2:**

**3b. PRE-break prints are classified barely better than a coin flip (54–60%), because they sit at
the start of the series where the expanding causal median is built substantially from themselves.**
The threshold a print at position *i* is compared against is the median of *all prior rolled values up
to and including i* — for the earliest ~60 prints (all of pre-break history), that running statistic
has almost no contrasting future information to lean on yet and is still forming largely from the
same noisy pre-break population being classified. This is a **self-referential ceiling effect**: the
causal design that correctly prevents look-ahead bias also means the classifier is least informative
exactly during the window that most needs to be correctly identified as "LOWER" for the date-fraction
check to pass.

**3c. A meaningful share of POST-break prints (14–24%) still fall below the running median deep into
the new regime, because the expanding median converges to the new regime slowly.** The running
median's value at the *last* valid print of the panel was only 1.74–1.90 (W1/W2/W3) — still short of
the true post-break mean of 2.0, nearly five years after the break. Weeks mislabeled LOWER this way
are not clustered at the boundary; they occur throughout the post-break era (as late as 248–249 weeks
after the break, i.e., near the panel's own end) — a genuine convergence artifact of a *cumulative,
since-inception* expanding statistic, not a transient boundary-smoothing effect.

**3d. The panel-shape asymmetry (post-break era ≈4.2× longer than pre-break era in this classifier's
own covered history: 251 vs 60 prints) turns a modest per-print error rate into a decisive bucket-level
failure.** Even though only 14–24% of POST-break prints are mislabeled LOWER, that minority (34–59
prints) is comparable to or larger than the *entire* correctly-labeled PRE-break LOWER cohort (20–31
prints), because there are so many more POST-break prints for even a modest error rate to draw from.
The LOWER bucket therefore ends up **majority POST-break** (54–75%) despite a genuinely strong,
correctly-signed underlying classifier — the opposite of what the ≤40% ceiling requires.

**Net mechanism:** the combination of (i) a self-referential ceiling on how well the *earliest*
(pre-break) observations can ever be classified under a purely-expanding causal statistic, and (ii) a
slow-converging expanding median that keeps leaking a nontrivial share of *later* (post-break)
observations to the wrong side, compounds with (iii) a panel where post-break duration dwarfs
pre-break duration, to make the specific ≤40%/≥75% date-fraction thresholds very hard to clear —
*independent of how strong or correctly-signed the underlying classifier actually is.*

---

## §4 — Caveats on this diagnosis, stated honestly

- **This positive control used the TFF-shaped windows (4/13/26 weekly prints) and the TFF round's own
  panel-coverage span (2020-08-04 onward, 60 pre-break prints).** It directly and specifically
  stress-tests the exact instantiation the positioning round used. It was **not** separately run
  against the volatility and mean-R rounds' own trade-indexed windows (20/63/126 trades) and their own
  (different) pre/post trade-count ratios — those rounds' own panel-shape asymmetry was not measured
  here. Given both rounds share the *identical* bucket-split mechanism (trailing window, expanding
  causal median, same 75%/40% thresholds) against the *same* break with a similarly long post-break
  history (ORB-MNQ-1's full panel: 2019-05-06→2026-07-15, i.e. ~2.4 years pre-break vs ~4.8 years
  post-break in calendar terms, a smaller but still substantial ~1:2 imbalance in trade-count terms
  per Q-ORBCUSH-1's own panel), the same qualitative mechanism plausibly applies — but this is a
  reasoned inference, not a separately-run, separately-verified positive control for those two rounds.
  A rigorous completion of this check would re-run this same synthetic-step-function design at each
  prior round's own window units and panel coverage; that is flagged as follow-on work, not done here.
- **The gate-clearance-direction axis inherits the same open construction-method ambiguity the real
  closure already disclosed** (`RESULTS.md` Phase 3, point 2): this script reused Implementation A's
  own contiguous-run block-construction method for a non-contiguous bucket mask, not Implementation
  B's alternative method. The real closure found this choice moves the *higher*-bucket's exact
  cushion pass rate by 5–14pp without changing the real Q's Accept/Reject routing. It is not known
  whether it would change this positive control's own direction-stability finding (W3's
  `HIGHER_CLEARS_LOWER_DOES_NOT`) — that is a second, separate axis of the REJECT verdict here, and
  the date-correlation failure (§2, §3) is sufficient on its own regardless.
  Note also that this run's W3 direction sign (`HIGHER_CLEARS_LOWER_DOES_NOT`) is the **opposite**
  sign from the real TFF result's W1/W3 pattern (`LOWER_CLEARS_HIGHER_DOES_NOT`) — a further sign that
  the direction axis is noisy/method-sensitive across runs, not a stable signature of "real edge
  present vs absent."
- **A single seed was run.** This is intentional, per the frozen-before-looking discipline the task
  itself asked for — but it means §2's exact numbers (e.g. 56.3%, not 55.0% or 58.0%) are one draw
  from a stochastic design, not a distributional statement. The qualitative pattern (0/3 date-corr
  clearances, direction instability) is unlikely to be a one-seed fluke given how far every lower-bucket
  fraction misses its ceiling (15–35pp) and given §3's mechanistic explanation predicts the same
  qualitative failure for *any* seed under this panel shape — but this was not verified by re-running
  under multiple seeds, which would itself have been a form of the exact best-of-K pattern this
  design was frozen specifically to avoid.

---

## §5 — Interpretation: what this does and does NOT tell us about the three real nulls

**What it tells us:** the three-window, expanding-causal-median bucket-split, fixed-75%/40%-threshold
date-correlation check — the specific operationalization every one of volatility, mean-R, and TFF
positioning was tested under — **is not a reliable detector of even a strong (d=2.0), correctly-signed,
persistent regime-shift classifier, when applied to a panel whose post-break history dwarfs its
pre-break history** (as ORB-MNQ-1's own break does: the pre-break era is short in every classifier's
own covered history, the post-break era stretches nearly five more years). §3's mechanism (a
self-referential ceiling on pre-break classification quality, plus slow expanding-median convergence
letting a growing absolute count of post-break weeks leak to the wrong side) is a structural property
of *this* bucket-construction choice, not of any one candidate's economic content.

**This means the three real `FALSIFIED` verdicts cannot be safely read as strong evidence that "no
real mechanism exists behind the break."** A real, correctly-signed, even quite strong mechanism could
plausibly have produced the same 0/3-or-near-0/3 date-correlation failure this pipeline already
produced for volatility, mean-R, and positioning — **not because the mechanism was false, but because
this specific test shape may be close to structurally incapable of clearing its own ≤40% lower-bucket
ceiling under this panel's post/pre duration ratio, regardless of the input classifier's truth.** The
positive control was designed generously (d=2.0, a "large" effect by conventional standards, with 15×
the sparsity floor's worth of pre-break history) specifically to give the pipeline every reasonable
chance to succeed, and it still rejected.

**What this does NOT tell us:**
- It does not resurrect volatility, mean-R, or TFF positioning as live candidates. Nothing here
  re-tests any of those three classifiers; this section is not a fourth attempt at any of them, and
  changes zero verdicts on record.
- It does not prove no apparatus-independent economic mechanism could ever pass this pipeline — W2's
  `BOTH_CLEAR` result here shows the *gate-clearance* half of the check (higher-extremity bucket
  clearing the survivor gate) is not itself impossible to trigger; it is specifically the
  *date-correlation* half, combined with the direction-stability requirement, that appears structurally
  hard to clear under this panel shape.
- It does not mean the break itself, or the bust-elimination finding, is in doubt — both remain
  separately triple-verified and untouched by this control either way (same standing caveat every
  real closure in this chain carries forward).
- It is **not** a license to treat the three real nulls as vindicated *or* as invalid outright — the
  honest position is narrower and more uncomfortable: **the apparatus itself has a demonstrated,
  quantified blind spot for exactly the shape of signal the real candidates were being tested for**,
  which means those three nulls carry meaningfully less evidentiary weight against "some mechanism
  exists" than a clean 0/3 might otherwise suggest, without this control having been run.

**Recommended next step (flagged, not executed under this task's scope):** before treating "three
clean nulls" as license to stop searching for a mechanism behind this break (the operator-review
trigger the real closure itself named), the ≤40%/≥75% fixed-threshold, expanding-causal-median
bucket-split design should be reviewed as a methodology question in its own right — independent of
any specific candidate — given this control's finding that it may not be able to confirm *any*
persistent one-time regime-shift classifier under ORB-MNQ-1's specific panel shape. A candidate
redesign (e.g., a locally-adaptive/rolling median instead of an expanding one, or a threshold
calibrated to the panel's own pre/post duration ratio rather than a fixed 75%/40%) is one direction
such a review might take, but is not proposed or endorsed here as a specific fix — this document's
job is to report the apparatus finding, not to redesign the apparatus.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Positive control designed (frozen before running), executed once, and written up. `REJECT` — pipeline does not recover a known, designed-to-be-detectable synthetic regime-break classifier. Mechanistic diagnostic (§3) added post-hoc from the same frozen run's own artifacts, no new random draw. | Claude Code (Sonnet 5) |
