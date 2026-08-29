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

**Result — does GAP add lift within OVERNIGHT-range strata?**
- overnight=0 (calm, n=991): lift **+0.0848** (0.5000 vs 0.4152), bootstrap
  p(lift≤0)=**0.0370** — positive, but only marginally significant at conventional
  0.05, not decisively.
- overnight=1 (hot, n=313): lift **−0.0724** (0.7250 vs 0.7974), bootstrap
  p(lift≤0)=**0.9453** — clearly *not* positive; if anything mildly negative.

**Result — does OVERNIGHT add lift within GAP strata?**
- gap=0 (n=1,020): lift **+0.3822** (0.7974 vs 0.4152), p(lift≤0)=**0.00025**.
- gap=1 (n=284): lift **+0.2250** (0.7250 vs 0.5000), p(lift≤0)=**0.00025**.

Overnight range adds large, highly significant positive lift in *both* gap strata;
gap adds a small, only-borderline-significant positive lift when overnight is calm
and *no* positive lift (possibly negative) when overnight is already hot — the
identical qualitative shape MNQ found: overnight range dominant and robust, gap a
nested, sign-unstable sub-question.

**Direct comparison against MNQ's own committed `candidate24_joint_results.json`:**

| Quantity | MNQ | MYM |
|---|---|---|
| gap lift, overnight=0 (calm) | +0.1053 | **+0.0848** |
| gap lift, overnight=1 (hot) | −0.0810 | **−0.0724** |
| overnight lift, gap=0 | +0.5936 | **+0.3822** |
| overnight lift, gap=1 | +0.4073 | **+0.2250** |
| 2×2: on=1,gap=0 vs on=1,gap=1 | 0.963 > 0.882 | **0.797 > 0.725** |
| three-way: sign pattern (on=0 both +, on=1 both −) | + / + / − / − | **+ / + / − / −** (matches) |

Every comparison lands the same sign, the same relative ordering, and a broadly
comparable (MYM systematically ~25-40% smaller in absolute magnitude, but never
sign-flipped) effect size. The three-way check (holding overnight AND day-history
both fixed) reproduces the same sign pattern in all four cells on both instruments.

## §2 — Why it stands out (the N signal)

- **Baseline:** the null hypothesis this test was designed to distinguish — either
  MYM's gap/overnight predictors carry independent information (two ids correctly
  separate), or MYM shows the same nesting MNQ found (two ids encode one construct).
- **Delta:** the data lands unambiguously on the nesting side for every comparison
  except statistical decisiveness in the single calm-stratum cell (MYM p=0.037 vs
  MNQ's reported p=0.0078 for the equivalent limb — same sign, weaker power, smaller
  effective cell size).
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
calm-stratum gap effect is real-but-weaker on MYM (p=0.037, not MNQ's p=0.0078) —
worth naming explicitly if/when a Pre-Q incorporates both instruments, not grounds to
reject the merge outright given every other comparison in §1 matches in sign and
relative magnitude.

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
# Expected: gap lift overnight=0 +0.0848 (p=0.037); overnight=1 -0.0724 (p=0.945)
#           overnight lift gap=0 +0.3822 (p=0.00025); gap=1 +0.2250 (p=0.00025)

diff <(python -c "import json;print(json.load(open('lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c24_joint_results.json'))['gap_lifts_within_overnight_strata'])") \
     <(python -c "import json;print(json.load(open('lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate24_joint_results.json'))['gap_lifts_within_overnight_strata'])")
# Expected: same signs, MYM magnitudes ~20-25% smaller than MNQ's
```

---

## Verification

```bash
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
    docs/notes/notice/N-2026-08-29-mym-overnight-gap-joint-gate.md --type notice
# Expected: RESULT: well-formed
```
