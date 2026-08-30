# Notice — MYM overnight gap magnitude → RTH-range conditioning (S2 stage-1, stratified — INCREMENT)

**Notice ID:** N-2026-08-29-mym-gap-magnitude-rth-range
**Observed:** 2026-08-29 (marginal-comparison run); **corrected 2026-08-29** (stratified re-run, same day, adversarial-review catch)
**Author:** Joshua | claude.ai
**Source:** backtest CSV (bar panel) — atheoretical mechanism harvest, MYM Phase 2
**Status:** `OPEN` — GRADUATE-eligible.

**Pre-Q:** already nested under [`Q-RANGEXFER-1`](../../briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md) as `H-RANGEXFER-1.a-MYM`.
**Lives in:** `docs/notes/notice/N-2026-08-29-mym-gap-magnitude-rth-range.md`

---

## §0 — Source anchor

- **Source:** `core/data/bar_data/MYM_M15.csv` (sha256
  `24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58`). Gap defined as
  today's RTH open − yesterday's RTH close (standard equity-style gap), magnitude only
  (`|gap|`), sign discarded.
  **Authoritative script (this correction):**
  `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_stratified_rerun.py`.
  **Authoritative results:** `.../c2_c4_stratified_results.json` key
  `candidate4_gap_magnitude_STRATIFIED`. Superseded (secondary, disclosed) script/results:
  `c2_c4_increment_falsifiers.py` / `c2_c4_results.json` key `candidate4_gap_magnitude`.
- **Observed at:** 2026-08-29 (this session, both runs).

---

## §1 — The observation

**Constraint-audit catch #1 (same-day, load-bearing to §0):** the originating brief
scoped this candidate as "fully open ground" needing only its own corrected-battery
run. On inspection, gap magnitude and RTH range are — like candidate 2's overnight
range — different series measured the same session, sharing the same slow
common-volatility-regime confound that pauses the "S2" construct in the frozen spec
(`docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md` §4 D5). No
full battery was run; the spec's own $0 cheap falsifier ran instead.

**Constraint-audit catch #2 (same-day, this correction — SUPERSEDES the original §1
below): the first falsifier design was the wrong statistic, exactly as caught for
candidate 2.** `c2_c4_increment_falsifiers.py` diffed two **marginal** conditional
rates — gap-conditioned 0.6268 (n=284) vs. day-history-conditioned 0.7306 (n=297) —
giving **−0.1039, 95% CI [−0.1636, −0.0404], read as a clean, decisive kill.** The
corrected design stratifies on `bias_hist` and measures the gap predictor's lift
within each day-history stratum held fixed (same verified-equivalent `bias`/`y`
definitions as candidate 2; only the aggregation step changed).

**Corrected (authoritative) result — the sign itself flips.** Within stratum
`bprime=0` (n=1,010): P(y=1|gap=1)=0.5526 (n=190) vs. P(y=1|gap=0)=0.4122 (n=820) —
**lift +0.1404**. Within stratum `bprime=1` (n=297): P(y=1|gap=1)=0.7766 (n=94) vs.
P(y=1|gap=0)=0.7094 (n=203) — **lift +0.0672**. Both strata are now *positive*, not
negative — the original marginal "decisive kill" was itself a compositional artifact
(the same Simpson's-paradox-shaped effect candidate 2 showed, here strong enough to
flip the sign, not just mask the magnitude). Block-bootstrap on the minimum
stratified lift: mean **+0.0594**, 95% CI **[−0.0419, +0.1477]**, straddles 0,
**p(lift ≤ 0) = 0.1247** / **null-calibrated p(null≥obs) = 0.00860**
(within-stratum circular-shift of the gap predictor, distinct rotations
enumerated, identity included; n_null=1304 from the sibling joint-gate cache vs
original n=1307; 3-day difference disclosed; per-stratum 0.00099 / 0.152).
**VERDICT: INCREMENT** (operator ruling, 2026-08-30 — see the Addendum below).
The original decision rule (bootstrap CI, which still straddles 0) and the
null-calibrated rule (p=0.0086, decisively clears a conventional 0.05 bar)
disagreed; the operator ruled the null-calibrated test governs, since it is
the Type-I-controlled statistic — the bootstrap CI is a percentile resample of
the observed data, not a test against a true zero-association null (the same
class of defect Codex flagged and PR #207/#210 fixed elsewhere in this batch).

## §2 — Why it stands out (the N signal)

- **Baseline:** the spec's own precommitted rule — only a clean negative (CI upper
  bound < 0) kills S2 for $0. The corrected CI does not clear that bar in either
  direction.
- **Delta:** the sign of the finding inverted between the marginal and stratified
  designs (−10.4pp marginal vs. +14.0pp / +6.7pp within-strata) — the largest
  correction-driven swing in this batch, larger even than candidate 2's (which stayed
  positive throughout, just went from ambiguous to decisive).
- **Frequency check:** first instance under the corrected design for this construct on
  any instrument; no external corroboration exists for MYM gap-magnitude either way
  (Mesfin 2026 is MNQ-only and concerns fill/fade direction, not magnitude).

## §3 — Candidate mechanisms (informal)

- A real but weaker transmission effect than candidate 2's overnight range — same
  general "information carried through the pre-open period" story, plausibly weaker
  because a single gap value is a noisier, lower-information summary than a full
  overnight range.
- Could still be pure noise around a null increment — the CI does include 0, and the
  point estimate (+5.9pp) is well below candidate 2's (+21.9pp).
- The marginal comparison's sign flip is itself informative: it shows the day-history
  comparator and the gap-magnitude predictor have a non-trivial joint distribution
  (their bias=1 populations differ in composition across the two constructs enough to
  reverse an unconditional comparison) — a caution against ever trusting a marginal
  read for this class of question again, not just for the two candidates corrected
  today.

## §4 — Routing decision

**GRADUATE — superseding the original HOLD-until-2027-03-01 line, struck below.**

Reason (as originally read, HOLD): no longer a clean kill (the original DROP does not
survive the correction — the sign itself was wrong), but also not a demonstrated
increment on the scale candidate 2 showed by the bootstrap CI rule. **Superseded
2026-08-30 by operator ruling** (see the Addendum below): the null-calibrated test
(p=0.0086) is the Type-I-controlled statistic and clears a conventional 0.05 bar
decisively; the bootstrap CI's own straddle-0 reading is not evidence against an
increment, only a limitation of a statistic that was never testing the right null.
Already nested under `Q-RANGEXFER-1` as `H-RANGEXFER-1.a-MYM`, so no separate Pre-Q
opening is owed — see that brief's own §6 for how this candidate's eventual verdict
(RESOLVED/FALSIFIED/AMBIGUOUS-HOLD) gets scored.

~~HOLD until 2027-03-01, re-check trigger: re-run the stratified falsifier on the
grown panel; if the min-stratified-lift CI clears 0 (lower bound > 0), GRADUATE
alongside candidate 2; if it flips to a clean negative, DROP cleanly~~ — struck
2026-08-30, superseded by the operator ruling above; no panel-growth wait needed.

---

## §5 — If HOLD: re-check trigger

N/A — superseded 2026-08-30, routed GRADUATE by operator ruling (see the Addendum below), not HOLD.

---

## §10 — Audit hooks

```bash
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_stratified_rerun.py
# Expected: [candidate4_gap_magnitude_STRATIFIED] min-stratified-lift bootstrap:
#   mean=0.0594  CI=[-0.0419,+0.1477]  p(lift<=0)=0.1247 / null-calibrated p=0.00860
#   (script's own internal "verdict" field still prints AMBIGUOUS -- CI straddles 0;
#   this notice's own §4 GRADUATE routing is the operator-ruled disposition on top of
#   that, not a claim the script itself now says something different)

# Superseded secondary measurement (disclosed, sign-flipped by the correction — do not
# cite as the D5 stage-1 answer):
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_increment_falsifiers.py
# Expected: [candidate4_gap_magnitude] diff=-0.1039  95% CI=[-0.1636,-0.0404]  VERDICT=NO-INCREMENT (marginal, superseded)

# Confirm the ruling is reflected downstream
grep -n "H-RANGEXFER-1.a-MYM" docs/briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md
```

---

## Addendum — joint gate vs. candidate 2 (2026-08-29, append-only, does not change §1-§5 above)

A follow-up joint test
([`N-2026-08-29-mym-overnight-gap-joint-gate.md`](N-2026-08-29-mym-overnight-gap-joint-gate.md))
ran this candidate against candidate 2 (overnight range) directly, mirroring MNQ's
Q-RANGEXFER-1 joint stratification. Result: this candidate's (gap's) own lift within
overnight-range strata is +8.5pp (overnight calm, borderline p=0.037) and −7.2pp
(overnight hot, clearly not positive, p=0.945) — a nested, sign-unstable pattern
closely replicating MNQ's own finding on the identical construct (+10.5pp/−8.1pp).
This does not change this candidate's own day-history-level verdict above (that
verdict tests this candidate alone against the day-history comparator; the joint
result is a different, additional question about this candidate's relationship to
candidate 2, and is disclosed as exploratory/unregistered per that notice's own
K-accounting correction — not cited as evidence for the day-history-level verdict
above). The joint notice recommends, and `Q-RANGEXFER-1`'s own 2026-08-30 amendment
executes, folding this id and `overnight-range-day-session-transfer` under MNQ's
`overnight-range-transmission` Q-brief (as `H-RANGEXFER-1.a-MYM`) — see that notice
and that brief for the full comparison and reasoning.

---

## Addendum — null-calibrated p vs. bootstrap CI (2026-08-29, append-only, does not change §1–§5)

The original §1 / §4 AMBIGUOUS + HOLD-until-2027-03-01 routing used
`block_bootstrap_min_lift`'s percentile CI (still **[−0.0419, +0.1477]**,
p(lift≤0)=0.1247). That statistic resamples the observed series and is **not**
a Type-I test under a true zero-association null — the same defect Codex
flagged on PR #205 and that PR #207 retrofits into this script.

Recomputed against the sibling joint-gate cached frame
(`c24_joint_frame.csv`, n=1304 vs this notice's original n=1307; 3-day
difference disclosed): circular-shift null p on the **minimum** stratified
lift is **p_ge_obs=0.0086** (observed min-lift +0.0637), per-stratum
0.00099 (bprime=0) / 0.1520 (bprime=1) — **correcting this addendum's own
original figures (0.0117 / 0.00025 / 0.1467), which do not match the
authoritative `c2_c4_stratified_results.json` (`min_lift_null_calibrated`
key, re-checked 2026-08-30) and were themselves stale; §1 above already
carried the correct figures.** The two readings do not change which rule
wins (both clear a conventional 0.05 bar), only the exact margin.

Two different decision rules disagreed:

- **CI rule (original, this notice's own §4 owner until 2026-08-30):** lower bound < 0 → AMBIGUOUS / HOLD until 2027-03-01.
- **Null-p rule (0.05 bar, the test `block_bootstrap_min_lift` is not):** p=0.0086 → reads INCREMENT.

Vendor bars were absent this session, so the null p is on the 1304-day
joint-gate cache, not a byte-identical rerun of the original 1307-day
scored set. Script + JSON: PR #207
(`lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_stratified_rerun.py`
/ `c2_c4_stratified_results.json` key `candidate4_gap_magnitude_STRATIFIED`).

---

## Addendum — operator ruling (2026-08-30)

**Ruling: the null-calibrated test governs. This cell flips to INCREMENT** (§1/§4
updated above). Verbatim: *"I will go with INCREMENT, it seems the null-calibrated
test is the more reliable one."* This resolves the disagreement the preceding
addendum named — the CI rule's own straddle-0 reading is a limitation of a
percentile-bootstrap statistic that was never a Type-I-controlled test, not
evidence against an increment. No new computation was run to produce this ruling;
it is a disposition call on the numbers already on record above (and corrected in
the preceding addendum). Already nested under `Q-RANGEXFER-1` as `H-RANGEXFER-1.a-MYM`
(per `Q-RANGEXFER-1`'s own 2026-08-30 amendment) — this ruling settles the
day-history-level verdict this notice itself owns; it does not by itself settle
`H-RANGEXFER-1.a-MYM`'s own (overnight-calm-restricted) hypothesis, which is a
separate statistic scored under that brief's own §6.

---

## Verification

```bash
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
    docs/notes/notice/N-2026-08-29-mym-gap-magnitude-rth-range.md --type notice
# Expected: RESULT: well-formed
```
