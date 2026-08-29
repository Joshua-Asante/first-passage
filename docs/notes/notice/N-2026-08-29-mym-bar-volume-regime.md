# Notice — MYM M15 bar-volume regime → next-bar range (ToD-deseasonalized, stratified — GRADUATE)

**Notice ID:** N-2026-08-29-mym-bar-volume-regime
**Observed:** 2026-08-29 (marginal-comparison run); **corrected 2026-08-29** (stratified re-run, same-shape correction as candidates 2/4)
**Author:** Joshua | claude.ai
**Source:** backtest CSV (bar panel) — atheoretical mechanism harvest, MYM Phase 2
**Status:** `OPEN` — GRADUATE-eligible; Pre-Q authoring deliberately deferred to the planned MNQ+MYM pooling session (not opened here)
**Lives in:** `docs/notes/notice/N-2026-08-29-mym-bar-volume-regime.md`

---

## §0 — Source anchor

- **Source:** `core/data/bar_data/MYM_M15.csv` (sha256
  `24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58`), all 141,467 bars
  (RTH + overnight; last truncated session dropped).
  **Authoritative script (this correction):**
  `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c3_stratified_rerun.py`.
  **Authoritative results:** `.../c3_stratified_results.json`. Superseded (secondary,
  disclosed) script/results: `c3_volume_regime.py` / `c3_results.json`.
- **Observed at:** 2026-08-29 (original run and this same-day correction).

---

## §1 — The observation

**Two constraint-audit catches, before running anything (original session, unchanged
by this correction):**

1. Plain M15 volume has a strong intraday U-shape — every value is expressed relative
   to its **own time-of-day slot's** trailing median (20 prior same-slot occurrences),
   the `tod-baseline-range-trigger` deseasonalization convention, reused not invented.
2. Volume and range are **different series** sharing a slow common regime state, the
   same cross-series confound flagged for candidates 2/4 (S2-shaped), just at 1-bar
   instead of same-session lag. Scored as a $0 increment test against the mundane
   same-series comparator, not a full corrected battery.

**Constraint-audit catch #3 (this correction, 2026-08-29 — SUPERSEDES the original
result below): the aggregation step had the identical marginal-comparison flaw found
and fixed in candidates 2/4, just not caught the first time because this construct
doesn't cite the D5 spec — it's a different mechanism family
(`intraday-bar-volume-regime`, not the magnitude-persistence "S2" family) — so the
adversarial review that scanned 2/4 for that pattern didn't scan this one. It should
have; the shape is identical.** `c3_volume_regime.py` computed two **marginal**
conditional rates — volume-conditioned obs=0.6546 vs. own-range-conditioned obs=0.6596
— and diffed them: **−0.0049, 95% CI [−0.0085, −0.0012], read as a clean, well-powered
NO-INCREMENT.** Same-bar volume and range are highly correlated — independently
verified on MYM's own data before rerunning (Spearman(volume, range) = **0.8618**,
n=141,467; not merely assumed by analogy to the cited MNQ figure of 0.88) — exactly the
regime where a marginal comparison can miss real incremental value or get the sign
wrong, which is precisely what happened on candidates 2 and 4.

**Corrected (authoritative) result — decisive, and the largest-magnitude reversal in
this batch.** Stratifying on the bar's own already-elevated range (`bias_hist`) and
measuring volume's (`bias_new`'s) lift within each stratum: within `bias_hist=0`
(own range NOT elevated, n=71,492): P(y=1|volume=1)=0.4528 (n=15,772) vs.
P(y=1|volume=0)=0.2879 (n=55,720) — **lift +0.1649**. Within `bias_hist=1` (own range
elevated, n=68,113): P(y=1|volume=1)=0.7150 (n=52,737) vs. P(y=1|volume=0)=0.4695
(n=15,376) — **lift +0.2455**. Block-bootstrap (circular, 96-bar blocks ≈1 session,
seed 20260829, n=4,000) on the minimum stratified lift: mean **+0.1648**, 95% CI
**[+0.1537, +0.1761]**, entirely positive, **p(lift ≤ 0) ≈ 0** (n=139,605 scored
pairs — the CI is 2.2pp wide on a huge sample) / **null-calibrated p uncomputed
this session** (no scored-frame cache; vendor bars absent). **VERDICT: INCREMENT** —
the largest, tightest-estimated effect of any correction run in this batch.
Recalibration cannot flip this verdict: the CI is entirely positive on n=139,605.

## §2 — Why it stands out (the N signal)

- **Baseline:** the mundane own-range persistence comparator, and the spec-agnostic
  version of the same "no increment → not informative" logic used for candidates 2/4.
- **Delta:** the marginal comparison's near-zero, slightly negative diff (−0.49pp) was
  not a near-miss dissolving into noise — it was hiding a real +16 to +25pp effect,
  masked because volume and range are correlated (ρ=0.86) enough that their marginal
  rates converge even when one carries substantial incremental information the other
  doesn't.
- **Cross-instrument corroboration (reported context, not independently re-verified
  here — MYM's own numbers above stand on their own):** the MNQ sibling campaign's
  own candidate 3 (informally named `bar-volume-regime` there, no MECHANISMS.md
  heading or PROFILE cell registered for it yet — its own Pre-Q is also not yet
  opened) ran the correctly-stratified design from the start and found a strikingly
  similar shape: +20.6pp / +25.6pp incremental lift across its own two range-matched
  strata, and routed the same construct to **GRADUATE**. Two independent instruments,
  independently authored the same day, landing on the same effect size and the same
  routing decision is a meaningfully stronger basis than either instrument alone.
- **Frequency check:** first instance under the corrected design on MYM.

## §3 — Candidate mechanisms (informal)

- **Genuine incremental information in volume** beyond contemporaneous range — order-
  arrival intensity may anticipate the *next* bar's range even when the current bar's
  own realized range doesn't fully reflect it yet (participation/urgency vs. realized
  outcome decorrelating enough at M15 to matter) — the MNQ session's own candidate-B
  mechanism framing, and the most natural read of an effect this large surviving a
  correlation as high as 0.86.
- Could still be the same underlying volatility/activity-clustering phenomenon as
  candidate 1 (`daily-range-state-persistence`), observed at finer (bar) grain via a
  different proxy — not a distinct WHO, just the same regime-level phenomenon at
  higher frequency. The Pre-Q, whenever authored, should confront this directly rather
  than assume incremental = distinct-mechanism.
- Window/threshold-choice noise (the specific 20-slot ToD window, P50/ratio>1
  thresholds) is untested at other settings this session; any retune would be a fresh
  K-charged axis, not a free look.

## §4 — Routing decision

**GRADUATE — to a Pre-Q, authoring deliberately deferred.**

Reason: a decisively powered ($0, n=139,605, CI width 2.2pp, p≈0), economically large
(+16 to +25pp, an order of magnitude bigger than candidates 2/4's corrected effects)
incremental-information finding, cross-instrument-corroborated by MNQ's independently
stratified, independently GRADUATEd same-day result. Not opened as a Pre-Q here, for
the same reason candidate 2 wasn't: the operator's own batch framing named a follow-up
session that pools MNQ's and MYM's GRADUATE sets together before authoring any Pre-Q.
**Raised-bar route: none needed.** This is a conditioner-role magnitude/range claim
(predicts elevated range, not direction — the direction limb was scoped out of this
MYM batch entirely, matching MNQ's own clean-null direction result) — the
single-instrument index-futures directional-timing raised bar does not apply, the same
reasoning that exempted candidates 1 and 2. **Still outstanding:** whether this
incremental effect is a distinct WHO from candidate 1's daily-TR persistence (mechanism
question above) — a question for the Pre-Q, not resolved here.

---

## §5 — If HOLD: re-check trigger — N/A, superseded.

The original 2026-08-29 marginal-comparison run's routing decision (`DROP`) is
superseded by this correction and does not stand; no re-check trigger applies to a
GRADUATEd notice.

---

## §10 — Audit hooks

```bash
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c3_stratified_rerun.py
# Expected: min-stratified-lift bootstrap: mean=0.1648  CI=[+0.1537,+0.1761]
#   p(lift<=0)=0.0000 [NOT null-calibrated]  VERDICT=INCREMENT
#   null-calibrated p: UNCOMPUTED this session unless MYM_M15.csv or
#   c3_stratified_frame.csv is present; INCREMENT cannot flip (CI entirely +).

# Superseded secondary measurement (disclosed, not the authoritative answer):
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c3_volume_regime.py
# Expected: diff=-0.0049  95% CI=[-0.0085,-0.0012]  VERDICT=NO-INCREMENT (marginal, superseded)

grep "N-2026-08-29-mym-bar-volume-regime" docs/briefs/Q-*.md
# Expected: no matches yet (Pre-Q authoring deferred to the MNQ+MYM pooling session)
```

---

## Verification

```bash
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
    docs/notes/notice/N-2026-08-29-mym-bar-volume-regime.md --type notice
# Expected: RESULT: well-formed
```
