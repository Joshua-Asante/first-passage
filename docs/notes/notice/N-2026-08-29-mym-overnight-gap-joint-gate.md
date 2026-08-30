# Notice — MYM candidates 2×4 joint gate: does MYM replicate MNQ's nested-gap pattern?

**Notice ID:** N-2026-08-29-mym-overnight-gap-joint-gate
**Observed:** 2026-08-29
**Author:** Joshua | claude.ai
**Source:** own statistical computation this session — direct port of MNQ's D-S-A pre-Q joint gate
**Status:** `HELD` — recommendation below; **actioned 2026-08-30** via `Q-RANGEXFER-1`'s amendment (§4/§5 below), which is the PR review this notice named as the correct venue
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

**Second correction, 2026-08-30 (Codex review, PR #210): this script's own
`circular_shift_null_p` implementation was NOT the same construction as the
MNQ sibling script's Codex-reviewed (PR #207) version, and the two instruments'
null-calibrated p-values below were not directly comparable as originally
reported.** Two divergences, both fixed: (1) this script rotated `other_label`'s
FULL series before masking to the fixed stratum, which can import label values
from OUTSIDE that stratum into the rotated in-stratum groups — exactly the
cross-stratum leakage a "within-stratum" null is supposed to rule out, and the
opposite of MNQ's construction (`o_s = other_label[fixed]`, rotate only `o_s`);
(2) this script drew `draws` random shifts from {1,...,N−1}, excluding the
identity rotation, rather than MNQ's exhaustive enumeration of every distinct
rotation (including identity) for small strata. Ported MNQ's exact construction
into this script (`c24_joint_gate.py`, same file) and re-ran it against the
committed `c24_joint_frame.csv` cache (vendor bars still absent in this
environment) — the point-estimate lifts and Spearman correlations below are
byte-identical to before (the frame itself did not change), only the
null-calibrated p-values changed:

**Result — does GAP add lift within OVERNIGHT-range strata?**
- overnight=0 (calm, n=991): lift **+0.0848** (0.5000 vs 0.4152), bootstrap
  p(lift≤0)=**0.0370**; **corrected** null-calibrated p(null≥obs)=**0.0495**
  (was 0.0198 under the flawed construction) — still clears a nominal 0.05 bar,
  but only barely, and is now the *weakest* significance reading of any cell in
  this notice, not "more decisive than the bootstrap" as the pre-correction
  text claimed. Still the smallest-magnitude effect of the four.
- overnight=1 (hot, n=313): lift **−0.0724** (0.7250 vs 0.7974), bootstrap
  p(lift≤0)=**0.9453**; **corrected** null-calibrated p(null≥obs)=**0.9489**
  (was 0.8880) — clearly *not* positive under either test; if anything mildly
  negative. Conclusion unchanged by the correction.

**Result — does OVERNIGHT add lift within GAP strata?**
- gap=0 (n=1,020): lift **+0.3822** (0.7974 vs 0.4152), bootstrap
  p(lift≤0)=**0.00025**; **corrected** null-calibrated p(null≥obs)=**0.00098**
  (was 0.00025) — still highly significant; conclusion unchanged.
- gap=1 (n=284): lift **+0.2250** (0.7250 vs 0.5000), bootstrap
  p(lift≤0)=**0.00025**; **corrected** null-calibrated p(null≥obs)=**0.00352**
  (was 0.00125) — still highly significant; conclusion unchanged.

Overnight range adds large, highly significant positive lift in *both* gap strata
under either test; gap adds a small positive lift when overnight is calm — **real
under the corrected null but only barely (p=0.0495), a materially weaker basis
than the pre-correction p=0.0198 suggested** — and *no* positive lift (possibly
negative) when overnight is already hot, under both tests. The qualitative shape
MNQ found (overnight range dominant and robust, gap a nested, sign-unstable
sub-question) still holds. **The correction does not overturn the finding, but it
does weaken the calm-stratum gap cell specifically — the opposite of the
pre-correction text's claim that recalibration "strengthens" that cell.**

**Direct comparison against MNQ's own committed `candidate24_joint_results.json`:**

| Quantity | MNQ | MYM |
|---|---|---|
| gap lift, overnight=0 (calm), null-p | +0.1053, p=0.0087 | **+0.0848, p=0.0495** (barely clears 0.05) |
| gap lift, overnight=1 (hot), null-p | −0.0810, p=0.9970 | **−0.0724, p=0.9489** |
| overnight lift, gap=0, null-p | +0.5936, p=0.00086 | **+0.3822, p=0.00098** |
| overnight lift, gap=1, null-p | +0.4073, p=0.00306 | **+0.2250, p=0.00352** |
| 2×2: on=1,gap=0 vs on=1,gap=1 | 0.963 > 0.882 | **0.797 > 0.725** |
| three-way: sign pattern (on=0 both +, on=1 both −) | + / + / − / − | **+ / + / − / −** (matches) |
| Spearman(overnight, gap) | 0.4711 | **0.5263** (+11.7%, larger not smaller) |
| overnight-calm subpanel size (n) | 973 | **991** (larger, not smaller, than MNQ's) |

The lift magnitudes and Spearman correlations are unaffected by the 2026-08-30
null-construction fix (only the null-calibrated p-values changed). Every lift
comparison still lands the same sign and the same relative ordering — **but the
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
  The calm-stratum cell is the least decisive of the four under every test run so
  far: bootstrap p=0.037; the corrected (2026-08-30) null-calibrated test puts it
  at **p=0.0495** — barely clearing 0.05, and *less* decisive than MNQ's own
  calm-cell null-p of 0.0087, not "closer to MNQ's decisiveness" as an
  earlier, since-corrected pass of this test claimed.
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
calm-stratum gap effect is weaker on MYM than on MNQ under every test (bootstrap
p=0.037 vs MNQ's p=0.0078; corrected null-calibrated p=0.0495 vs MNQ's p=0.0087 —
MYM's own figure barely clears a nominal 0.05 bar) —
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
batch. Consequence for the calm-stratum result (bootstrap p=0.037, corrected
null-calibrated p=0.0495): **read either figure as exploratory, not multiplicity-corrected** — it
has not cleared any pre-registered significance bar and should not be cited as if
it had, and at p=0.0495 it would not survive even a mild multiplicity correction
across the four cells tested here. If the merge recommendation above is
acted on and a Pre-Q is opened to formalize it (for MYM, mirroring `Q-RANGEXFER-1`),
that Pre-Q should carry its own fresh K declaration rather than inherit this
notice's number.

**Explicitly not done here, per instruction:** no edit to `MECHANISMS.md` headings'
structure, no id rename, no `MYM.md` PROFILE cell change beyond citing this notice.
This lands as a PR for review; the merge/no-merge call and its execution belong to
that review, or to the deferred MNQ+MYM pooling session.

**Actioned 2026-08-30:** the recommendation was approved and executed as
[`Q-RANGEXFER-1`'s own amendment](../../briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md)
(§11 Amendment log there) — at the **question** layer only, exactly as this notice's
own §4/§5 scoped: `overnight-range-day-session-transfer` and
`overnight-gap-magnitude-range-conditioning` now share `overnight-range-transmission`'s
Q-brief (as `H-RANGEXFER-1-MYM` / `H-RANGEXFER-1.a-MYM`), scored independently of
MNQ's own verdict per that brief's §6. No `MECHANISMS.md` heading was deleted, no
PROFILE cell was renamed, and no id merge happened on the MYM ledger side —
consistent with this notice's own "not done here" list above, still accurate; only
the amended Q-brief changed. The calm-stratum caveat this notice raised (weaker
effect on MYM, p=0.037/0.020 vs MNQ's p=0.0078) is carried into that amendment's own
`H-RANGEXFER-1.a-MYM`, disclosed as exploratory per the K-accounting correction
above, not as pre-registered evidence.

Decision: HOLD → **actioned** (not GRADUATE/DROP — this notice's own action was
always a recommendation pending human review, closest to the template's HOLD
semantics; the review happened and approved the recommendation, recorded here
rather than restated as still-pending)
Reason: data supports merging the two ids at the question layer; the merge itself
was out of this notice's own authority per instruction and is now executed by the
brief that instruction named.

---

## §5 — If HOLD: re-check trigger

- **Re-check date:** N/A — event-triggered, not date-triggered.
- **Trigger condition — fired 2026-08-30, option (a) below:** operator/reviewer reads
  this notice (via PR review) and either (a) approves the merge — fold
  `overnight-range-day-session-transfer` and `overnight-gap-magnitude-range-
  conditioning`'s content into `overnight-range-transmission`'s **question** (not a
  PROFILE-cell rename — see the Actioned note above for what "fold" turned out to
  mean in practice, narrower than this trigger's original phrasing implied) — or (b)
  declines, in which case the two ids stand as a documented, evidence-examined
  cross-instrument taxonomy difference. **(a) fired:** `Q-RANGEXFER-1`'s 2026-08-30
  amendment folds both ids' questions into its own Q-brief, scored per instrument;
  both MYM.md PROFILE cells and both Notice-log files' cross-reference notes are
  updated to point at that Q-brief, not at a merged mechanism id (none was created).
- **Drop trigger:** none — this is a standing recommendation, not a claim that decays. N/A, fired.
- **Calendar entry:** none; this was a review-gated, not calendar-gated, item.

---

## §10 — Audit hooks

```bash
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c24_joint_gate.py
# Runs against the committed c24_joint_frame.csv cache when MYM_M15.csv is
# absent (public-clone environment) -- fixed 2026-08-30, previously crashed
# with FileNotFoundError in this environment (Codex review, PR #210).
# Expected (corrected 2026-08-30 null construction -- see §1/§2):
#           gap lift overnight=0 +0.0848 (bootstrap p=0.037, null-calibrated p=0.0495)
#           gap lift overnight=1 -0.0724 (bootstrap p=0.945, null-calibrated p=0.9489)
#           overnight lift gap=0 +0.3822 (bootstrap p=0.00025, null-calibrated p=0.00098)
#           overnight lift gap=1 +0.2250 (bootstrap p=0.00025, null-calibrated p=0.00352)
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
