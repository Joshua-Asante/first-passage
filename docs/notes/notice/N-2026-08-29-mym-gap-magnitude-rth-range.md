# Notice — MYM overnight gap magnitude → RTH-range conditioning (S2 stage-1, stratified — split: bprime=0 INCREMENT / bprime=1 not established)

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
- **K:** [`discovery_manifests/mymdd_1_2026_08_29.json`](../../../discovery_manifests/mymdd_1_2026_08_29.json), K=5, this cell's own naive marginal p=0.0015 (candidate 4, per §1 above; the manifest's own `candidates` array does not label rows by id, unlike MNQ's sibling manifest, so a BH-rank cross-check against the manifest's aggregate table isn't independently verifiable here). Added retroactively 2026-08-30 for parity with MNQ's sibling notices' own `**K:**` bullet convention — this cell's `floor_at_k(5)=1.1150 > CAP=1.0` (the DSR-reachable band), same as MNQ's three K-correction-audit-flagged notices; disclosed, not yet resolved (see `Q-RANGEXFER-1` §11).

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
**p(lift ≤ 0) = 0.1247** / **min-lift null-calibrated p(null≥obs) = 0.00860**
(within-stratum circular-shift of the gap predictor, distinct rotations
enumerated, identity included; n_null=1304 from the sibling joint-gate cache vs
original n=1307; 3-day difference disclosed; per-stratum 0.00099 / 0.152).

**Second correction, 2026-08-30 (Codex review, PR #211): the p=0.0086 "min-lift"
figure does not establish what it was first read to establish.**
`circular_shift_null_min_lift` computes it as the *product* of each stratum's
own tail probability — testing the **sharp joint null that both strata are
simultaneously zero**, not the actual composite claim needed ("gap magnitude
adds lift in both strata"), which requires rejecting the *disjunctive* null
("stratum 0 is zero OR stratum 1 is zero"). The correct test for that
composite claim is an intersection-union test: the **maximum** of the two
per-stratum p-values, not their product. Those per-stratum figures were
already on record: **0.00099** (`bprime=0`, decisive) and **0.152**
(`bprime=1`, does not reject at any conventional threshold). max(0.00099,
0.152) = 0.152 — not significant.

**VERDICT: split by stratum (operator ruling, 2026-08-30 — see the Addendum
below).** **`bprime=0` (day-history NOT elevated): INCREMENT** — the
within-stratum null-calibrated test (p=0.00099) is properly scoped to this
stratum alone and is decisive; this is the same class of per-stratum test
already treated as sufficient stage-1 evidence elsewhere in this batch (e.g.
MYM candidate 2's own p_ge_obs). **`bprime=1` (day-history elevated): NOT
ESTABLISHED** — p=0.152 does not reject; this is not "AMBIGUOUS pending more
data," it is simply unsupported by the evidence on hand. There is no
whole-cell verdict that covers both strata at once; the min-lift statistic
that would have given one was itself the defect.

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

**Split disposition (corrected 2026-08-30, Codex review — supersedes both the
original HOLD-until-2027-03-01 line and the intervening blanket-GRADUATE line,
both struck below).**

**`bprime=0` (day-history NOT elevated): GRADUATE.** The within-stratum
null-calibrated test (p=0.00099) is properly scoped to this stratum alone and
is decisive — the same class of per-stratum evidence already treated as
sufficient stage-1 evidence elsewhere in this batch. Routed to a **new**
hypothesis clause, `H-RANGEXFER-1.b-MYM` (added to `Q-RANGEXFER-1` 2026-08-30),
specifically for this day-history-restricted claim — distinct from
`H-RANGEXFER-1.a-MYM`'s overnight-calm-restricted claim, which is a different
estimand (see that brief's Estimand-correction note). See that brief's own §6
for how this stratum's eventual verdict (RESOLVED/FALSIFIED/AMBIGUOUS) gets
scored.

**`bprime=1` (day-history elevated): stays not established — no GRADUATE
routing.** p=0.152 does not reject at any conventional threshold. There is
also nothing to schedule a re-check against: the struck HOLD trigger below was
written for a whole-cell verdict that no longer exists. This stratum simply
sits open and unsupported pending a fresh mechanism-level reason to look
again, not a scheduled HOLD.

Reason (as originally read, HOLD, whole-cell): no longer a clean kill (the
original DROP does not survive the correction — the sign itself was wrong),
but also not a demonstrated increment on the scale candidate 2 showed by the
bootstrap CI rule.

~~Superseded 2026-08-30 by operator ruling: the null-calibrated test (p=0.0086)
is the Type-I-controlled statistic and clears a conventional 0.05 bar
decisively; the bootstrap CI's own straddle-0 reading is not evidence against
an increment, only a limitation of a statistic that was never testing the
right null.~~ — struck 2026-08-30 (Codex review, PR #211): the cited p=0.0086
tested the wrong composite null (product-of-tails on the sharp joint null, not
the disjunctive composite the "both strata" claim needs — see §1's second
correction). The operator's underlying principle (trust the null-calibrated,
Type-I-controlled test over the bootstrap CI) was sound and is preserved above
for the `bprime=0` stratum, where it is properly scoped and decisive; it does
not extend to a whole-cell claim.

~~HOLD until 2027-03-01, re-check trigger: re-run the stratified falsifier on the
grown panel; if the min-stratified-lift CI clears 0 (lower bound > 0), GRADUATE
alongside candidate 2; if it flips to a clean negative, DROP cleanly~~ — struck
2026-08-30; superseded by the split disposition above (no panel-growth wait
needed for `bprime=0`; `bprime=1` has no scheduled re-check).

---

## §5 — If HOLD: re-check trigger

N/A — superseded 2026-08-30 (see §4's split disposition): `bprime=0` routes
GRADUATE; `bprime=1` stays not-established with no scheduled re-check trigger.
Neither stratum carries a HOLD in the original whole-cell sense.

---

## §10 — Audit hooks

```bash
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_stratified_rerun.py
# Expected: [candidate4_gap_magnitude_STRATIFIED] min-stratified-lift bootstrap:
#   mean=0.0594  CI=[-0.0419,+0.1477]  p(lift<=0)=0.1247
#   min-lift null-calibrated p=0.00860 (product-of-tails on the SHARP joint null --
#   does NOT test the composite "both strata" claim; see §1's second correction)
#   per-stratum null-calibrated p: bprime=0 -> 0.00099 (decisive) / bprime=1 -> 0.15202
#   (does not reject) -- these two per-stratum figures are authoritative for this
#   notice's split verdict, not the blended 0.00860 figure above
#   (script's own internal "verdict" field still prints AMBIGUOUS -- CI straddles 0;
#   this notice's own §4 split routing is the operator-ruled disposition applied to
#   the per-stratum figures, not a claim the script itself now says something
#   different)

# Superseded secondary measurement (disclosed, sign-flipped by the correction — do not
# cite as the D5 stage-1 answer):
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_increment_falsifiers.py
# Expected: [candidate4_gap_magnitude] diff=-0.1039  95% CI=[-0.1636,-0.0404]  VERDICT=NO-INCREMENT (marginal, superseded)

# Confirm the split routing is reflected downstream
grep -n "H-RANGEXFER-1.a-MYM" docs/briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md
grep -n "H-RANGEXFER-1.b-MYM" docs/briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md
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

## Addendum — operator ruling (2026-08-30, corrected same day)

**Original ruling:** *"I will go with INCREMENT, it seems the null-calibrated
test is the more reliable one."* No new computation was run to produce this
ruling; it was a disposition call on the numbers on record at the time. The
operator's judgment on the *principle* — that the null-calibrated,
Type-I-controlled test should govern over the percentile-bootstrap CI where
the two disagree — was sound and stands. The *application* of that principle
was not: the specific figure it was applied to (p=0.0086, the blended
"min-lift" null-calibrated p) turned out to test the wrong null — it is a
product of the two per-stratum tail probabilities, which tests the sharp joint
null that both strata are simultaneously zero, not the disjunctive composite
null a "both strata" claim needs to reject (Codex review, PR #211 — see §1's
second correction and the preceding addendum).

**Corrected disposition — same principle, re-applied to the right statistics:**
the operator's own principle, applied to the two *per-stratum* null-calibrated
p's already on record (0.00099 for `bprime=0`, 0.152 for `bprime=1`), gives a
**split** result, not a blanket one. `bprime=0` clears a conventional 0.05 bar
decisively and reads INCREMENT; `bprime=1` does not clear it and is not
established. This replaces the blanket-INCREMENT reading this addendum
originally recorded — see §1 and §4 above for the full split verdict and
routing.

Already nested under `Q-RANGEXFER-1`: the `bprime=0` result routes to a new
hypothesis clause, `H-RANGEXFER-1.b-MYM` (added 2026-08-30), distinct from
`H-RANGEXFER-1.a-MYM`'s overnight-calm-restricted claim, which is a separate
statistic scored under that brief's own §6 and is not settled by this ruling.

---

## Verification

```bash
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
    docs/notes/notice/N-2026-08-29-mym-gap-magnitude-rth-range.md --type notice
# Expected: RESULT: well-formed
```
