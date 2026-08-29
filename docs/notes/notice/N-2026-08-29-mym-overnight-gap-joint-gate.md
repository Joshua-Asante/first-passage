# Notice — MYM candidates 2×4 joint gate: does MYM replicate MNQ's nested-gap pattern?

**Notice ID:** N-2026-08-29-mym-overnight-gap-joint-gate
**Observed:** 2026-08-29
**Author:** Joshua | claude.ai
**Source:** own statistical computation this session — direct port of MNQ's D-S-A pre-Q joint gate
**Status:** `HELD` — recommendation below, no action taken; flagged for operator/review decision
**Lives in:** `docs/notes/notice/N-2026-08-29-mym-overnight-gap-joint-gate.md`

---

## §0 — Source anchor

- **Source:** `core/data/bar_data/MYM_M15.csv`, joint frame built from the same
  `bias_overnight`/`bias_gap`/`bias_dayhist`/`y` definitions already verified in
  `c2_c4_stratified_rerun.py` (traced by hand before running — identical formulas,
  confirmed not by inference). Script:
  `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c24_joint_gate.py` — a direct,
  same-seeds port of MNQ's sibling script
  [`candidate24_joint_gate.py`](https://github.com/Joshua-Asante/first-passage/blob/main/lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate24_joint_gate.py)
  (`block=20, draws=4000, seeds 100+s/200+s`), so the two runs are comparable rather
  than superficially similar. Results: `.../c24_joint_results.json` +
  `c24_joint_frame.csv` (cached per-day frame for any future stage-2 design).
- **Comparison source:** MNQ's own
  `lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate24_joint_results.json`
  (already on `origin/main` via PR #194), read directly for this comparison, not from
  memory.
- **Observed at:** 2026-08-29 (this session).

---

## §1 — The observation

**Why this test exists:** MYM currently carries two separate mechanism ids for
constructs MNQ combined into one — `overnight-range-day-session-transfer` (candidate
2, GRADUATE) and `overnight-gap-magnitude-range-conditioning` (candidate 4, HOLD).
Both `MECHANISMS.md` headings already carry a "Parallel-authoring taxonomy note"
(added during the 2026-08-29 merge) flagging that MNQ's combined `overnight-range-
transmission` id (Q-RANGEXFER-1) rests on a joint stratification MYM had not yet run,
and declining to merge/rename anything without that data. This is that data.

**Design (D-S-A Simplify step, symmetric by construction):** swap the conditioning
variable from day-history to each candidate's own bias, and test the other
candidate's incremental lift within strata of it — neither candidate privileged as
"base" a priori.

**Two p-values are reported per cell (corrected after review, see the note
below the table): the original `block_bootstrap_p` figure is a percentile-bootstrap
tail probability, not a null-calibrated significance level — it resamples the
observed data (with the actual effect baked in), so it measures how much of that
distribution sits at/below zero, not how often a lift this large would arise under
a true zero-association null. `circular_shift_null_p` is the null-calibrated
figure: it circularly shifts the other predictor's full series (preserving its own
autocorrelation, destroying its pairing with y) to build an actual zero-association
null, then reports how often that null produces a lift ≥ the observed one.**

**Result — does GAP add lift within OVERNIGHT-range strata?**
- overnight=0 (calm, n=991): lift **+0.0848** (0.5000 vs 0.4152), bootstrap
  p(lift≤0)=**0.0370**; null-calibrated p(null≥obs)=**0.0198** (seed-stable at
  0.017-0.022 across reruns) — positive and, under the correct null, *more*
  decisive than the original bootstrap figure suggested, though still the
  smallest effect of the four.
- overnight=1 (hot, n=313): lift **−0.0724** (0.7250 vs 0.7974), bootstrap
  p(lift≤0)=**0.9453**; null-calibrated p(null≥obs)=**0.8880** — clearly *not*
  positive under either test; if anything mildly negative.

**Result — does OVERNIGHT add lift within GAP strata?**
- gap=0 (n=1,020): lift **+0.3822** (0.7974 vs 0.4152), bootstrap
  p(lift≤0)=**0.00025**; null-calibrated p(null≥obs)=**0.00025**.
- gap=1 (n=284): lift **+0.2250** (0.7250 vs 0.5000), bootstrap
  p(lift≤0)=**0.00025**; null-calibrated p(null≥obs)=**0.00125**.

Overnight range adds large, highly significant positive lift in *both* gap strata
under either test; gap adds a small positive lift when overnight is calm (borderline
under the original bootstrap, more decisive at p=0.02 under the corrected
null-calibrated test) and *no* positive lift (possibly negative) when overnight is
already hot, under both tests — the identical qualitative shape MNQ found: overnight
range dominant and robust, gap a nested, sign-unstable sub-question. **Recalibration
does not overturn the finding; if anything it strengthens the one borderline cell.**

**Direct comparison against MNQ's own committed `candidate24_joint_results.json`:**

| Quantity | MNQ | MYM |
|---|---|---|
| gap lift, overnight=0 (calm) | +0.1053 | **+0.0848** (−19.5%) |
| gap lift, overnight=1 (hot) | −0.0810 | **−0.0724** (−10.6%) |
| overnight lift, gap=0 | +0.5936 | **+0.3822** (−35.6%) |
| overnight lift, gap=1 | +0.4073 | **+0.2250** (−44.8%) |
| 2×2: on=1,gap=0 vs on=1,gap=1 | 0.963 > 0.882 | **0.797 > 0.725** |
| three-way: sign pattern (on=0 both +, on=1 both −) | + / + / − / − | **+ / + / − / −** (matches) |
| Spearman(overnight, gap) | 0.4711 | **0.5263** (+11.7%, larger not smaller) |

Every comparison lands the same sign and the same relative ordering — **but the
magnitude gap is not a single uniform percentage.** The four lift comparisons range
from 10.6% to 44.8% smaller on MYM (not "~25-40%" as an earlier draft of this notice
claimed — corrected after review); the Spearman correlation between the two
predictors is actually *larger* on MYM, not smaller. No sign flips anywhere, but
"broadly comparable magnitude" overstated how tight the match is — report the actual
spread, not a compressed range. The three-way check (holding overnight AND
day-history both fixed) reproduces the same sign pattern in all four cells on both
instruments.

## §2 — Why it stands out (the N signal)

- **Baseline:** the null hypothesis this test was designed to distinguish — either
  MYM's gap/overnight predictors carry independent information (two ids correctly
  separate), or MYM shows the same nesting MNQ found (two ids encode one construct).
- **Delta:** the data lands unambiguously on the nesting side for every comparison.
  The calm-stratum cell is the least decisive of the four under the original
  bootstrap (MYM p=0.037 vs MNQ's reported p=0.0078), but the corrected
  null-calibrated test (see §1) puts MYM at p=0.020 for that same cell — same
  sign either way, and closer to MNQ's decisiveness than the bootstrap figure
  suggested, not further from it.
- **Frequency check:** first joint (as opposed to each-vs-day-history) test of these
  two MYM constructs against each other.

## §3 — Candidate mechanisms (informal)

- Genuine shared mechanism: overnight range is the primary information carrier
  (news/positioning/liquidity building through the Globex overnight session), and the
  RTH-open gap is largely a downstream *symptom* of that same overnight state rather
  than an independent information source — consistent with the strong overnight/gap
  co-occurrence measured here (P(gap=1|overnight=1)=0.511 vs P(gap=1|overnight=0)=0.125).
- Gap could still carry a small amount of genuinely independent information in the
  calm-overnight regime specifically (the one cell where its own lift clears 0.05) —
  MNQ's own framing kept this as a nested *sub-question*, not zero, and MYM's data
  doesn't contradict that finer read either.

## §4 — Routing decision / recommendation

**Not a GRADUATE/DROP/HOLD routing decision — this notice recommends, it does not
execute, a taxonomy action, per explicit instruction.**

**Recommendation: MYM replicates MNQ's nested-gap pattern closely enough to merge
`overnight-range-day-session-transfer` and `overnight-gap-magnitude-range-
conditioning` into MNQ's `overnight-range-transmission` id**, treating overnight
range as the primary claim and gap magnitude as a nested, calm-regime-scoped
sub-question on MYM too — the same parent/sub-question structure Q-RANGEXFER-1
already uses for MNQ. Caveat attached to the recommendation, not withheld: the
calm-stratum gap effect is weaker on MYM than on MNQ under either test (bootstrap
p=0.037 vs MNQ's p=0.0078; null-calibrated p=0.020) —
worth naming explicitly if/when a Pre-Q incorporates both instruments, not grounds to
reject the merge outright given every other comparison in §1 matches in sign and
relative magnitude.

**K-accounting correction (added after review): this is a new, unregistered look,
not a $0 re-measurement.** An earlier draft of this notice claimed "no new K
(re-measurement/joint-test of two already-registered/closed looks under
`mymdd_1_2026_08_29`)." That is wrong on inspection of the manifest itself —
`discovery_manifests/mymdd_1_2026_08_29.json`'s own `hypothesis` field lists exactly
the five original candidates; the joint overnight-vs-gap question is not among them.
It was formed only after seeing candidates 2 and 4's individual results (and after
seeing MNQ's own joint-gate finding) — the textbook shape of a post-hoc look, not a
re-measurement of an already-declared hypothesis. `register_search.py`'s own design
refuses to accept a K declaration after results are already known ("you cannot
re-declare K after seeing results"), so this look **cannot be retroactively folded
into the closed K=5 manifest, and does not get a fresh `open` now either** — either
path would launder a post-hoc look as pre-registered. The honest disclosure is
instead to name it plainly: this is a sixth, unregistered examination of this data
batch. Consequence for the calm-stratum result (bootstrap p=0.037, null-calibrated
p=0.020): **read either figure as exploratory, not multiplicity-corrected** — it
has not cleared any pre-registered significance bar and should not be cited as if
it had. If the merge recommendation above is
acted on and a Pre-Q is opened to formalize it (for MYM, mirroring `Q-RANGEXFER-1`),
that Pre-Q should carry its own fresh K declaration rather than inherit this
notice's number.

**Explicitly not done here, per instruction:** no edit to `MECHANISMS.md` headings'
structure, no id rename, no `MYM.md` PROFILE cell change beyond citing this notice.
This lands as a PR for review; the merge/no-merge call and its execution belong to
that review, or to the deferred MNQ+MYM pooling session.

Decision: HOLD (not GRADUATE/DROP — this notice's own action is a recommendation
pending human review, closest to the template's HOLD semantics: re-check trigger is
"reviewer/operator decides," not a calendar date)
Reason: data supports merging the two ids, but the merge itself is explicitly out of
this notice's own authority per instruction; recorded as a flagged recommendation
rather than self-executed.

---

## §5 — If HOLD: re-check trigger

- **Re-check date:** N/A — event-triggered, not date-triggered.
- **Trigger condition:** operator/reviewer reads this notice (via PR review or the
  deferred MNQ+MYM pooling session) and either (a) approves the merge — fold
  `overnight-range-day-session-transfer` and `overnight-gap-magnitude-range-
  conditioning`'s content into `overnight-range-transmission`, updating both
  MYM.md PROFILE cells and both existing Notice-log files' cross-reference notes to
  point at the merged id — or (b) declines, in which case the two ids stand as a
  documented, evidence-examined cross-instrument taxonomy difference (not merely an
  unexamined naming collision) and this notice's recommendation is recorded as
  declined, with reasoning.
- **Drop trigger:** none — this is a standing recommendation, not a claim that decays.
- **Calendar entry:** none; this is a review-gated, not calendar-gated, item.

---

## §10 — Audit hooks

```bash
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c24_joint_gate.py
# Expected: gap lift overnight=0 +0.0848 (bootstrap p=0.037, null-calibrated p=0.020)
#           gap lift overnight=1 -0.0724 (bootstrap p=0.945, null-calibrated p=0.888)
#           overnight lift gap=0 +0.3822 (bootstrap p=0.00025, null-calibrated p=0.00025)
#           overnight lift gap=1 +0.2250 (bootstrap p=0.00025, null-calibrated p=0.00125)
# Null-calibrated p is circular_shift_null_p; bootstrap p is block_bootstrap_p, which
# is NOT null-calibrated (see both docstrings) -- report the null-calibrated figure
# as the significance claim.

python3 -c "
import json, sys
mym = json.load(open('lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c24_joint_results.json'))['gap_lifts_within_overnight_strata']
mnq = json.load(open('lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate24_joint_results.json'))['gap_lifts_within_overnight_strata']
mismatches = [k for k in mym if (mym[k] > 0) != (mnq[k] > 0)]
sys.exit(1 if mismatches else 0)
"
# Explicit sign comparison, not a raw diff of two dicts with different numbers --
# the original 'diff <(...) <(...)' always exits 1 because the values differ, even
# when the signs (the actual invariant under test) agree. Exits 0 iff every stratum's
# sign matches between MYM and MNQ; exits 1 and prints nothing on the sign(s) that
# disagree if the invariant breaks (add printing of `mismatches` there if debugging).
# Expected: exit 0. Magnitudes themselves are NOT ~20-25% uniformly smaller -- see
# the corrected comparison table in §1 (range is 10.6%-44.8% across the four lifts,
# and the Spearman correlation runs the other way, larger on MYM).
```

---

## Verification

```bash
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
    docs/notes/notice/N-2026-08-29-mym-overnight-gap-joint-gate.md --type notice
# Expected: RESULT: well-formed
```
