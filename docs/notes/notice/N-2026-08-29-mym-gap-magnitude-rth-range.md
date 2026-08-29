# Notice — MYM overnight gap magnitude → RTH-range conditioning (S2 stage-1, stratified — HOLD)

**Notice ID:** N-2026-08-29-mym-gap-magnitude-rth-range
**Observed:** 2026-08-29 (marginal-comparison run); **corrected 2026-08-29** (stratified re-run, same day, adversarial-review catch)
**Author:** Joshua | claude.ai
**Source:** backtest CSV (bar panel) — atheoretical mechanism harvest, MYM Phase 2
**Status:** `HELD until 2027-03-01`
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
**p(lift ≤ 0) = 0.1247**. **VERDICT: AMBIGUOUS** — no longer a kill, not yet a pass.

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

**HOLD until 2027-03-01.**

Reason: no longer a clean kill (the original DROP does not survive the correction —
the sign itself was wrong), but also not a demonstrated increment on the scale
candidate 2 showed. The CI straddles 0 with a positive-leaning point estimate half
candidate 2's size. Re-checking on a grown panel (same ~6-month / ~125-session horizon
already used for candidate 2's now-superseded HOLD, reused here for consistency) can
resolve the sign with more data before any heavier design work is warranted.

---

## §5 — If HOLD: re-check trigger

- **Re-check date:** 2027-03-01 (~6 months / ~125 more sessions of panel growth).
- **Trigger condition:** re-run the stratified falsifier on the grown panel; if the
  min-stratified-lift CI clears 0 (lower bound > 0), candidate 4 GRADUATEs alongside
  candidate 2 (same S2 role, same outstanding conditions 3/4). If it flips to a clean
  negative (upper bound < 0), it DROPs cleanly this time — a corrected kill, not the
  first one.
- **Drop trigger:** CI on the grown panel still straddles 0 with no meaningful
  narrowing, or flips clean negative.
- **Calendar entry:** none set; operator to set if desired.

---

## §10 — Audit hooks

```bash
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_stratified_rerun.py
# Expected: [candidate4_gap_magnitude_STRATIFIED] min-stratified-lift bootstrap:
#   mean=0.0594  CI=[-0.0419,+0.1477]  p(lift<=0)=0.1247  VERDICT=AMBIGUOUS

# Superseded secondary measurement (disclosed, sign-flipped by the correction — do not
# cite as the D5 stage-1 answer):
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_increment_falsifiers.py
# Expected: [candidate4_gap_magnitude] diff=-0.1039  95% CI=[-0.1636,-0.0404]  VERDICT=NO-INCREMENT (marginal, superseded)

# Re-check due: 2027-03-01 -- verify in Calendar / Todoist if the operator sets one
```

---

## Verification

```bash
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
    docs/notes/notice/N-2026-08-29-mym-gap-magnitude-rth-range.md --type notice
# Expected: RESULT: well-formed
```
