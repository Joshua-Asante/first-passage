# Notice — MYM overnight-session range → RTH-range transfer (S2 stage-1, stratified — GRADUATE)

**Notice ID:** N-2026-08-29-mym-overnight-rth-range-transfer
**Observed:** 2026-08-29 (marginal-comparison run); **corrected 2026-08-29** (stratified re-run, same day, adversarial-review catch)
**Author:** Joshua | claude.ai
**Source:** backtest CSV (bar panel) — atheoretical mechanism harvest, MYM Phase 2
**Status:** `OPEN` — GRADUATE-eligible; Pre-Q authoring deliberately deferred to the planned MNQ+MYM pooling session (not opened here)
**Lives in:** `docs/notes/notice/N-2026-08-29-mym-overnight-rth-range-transfer.md`

---

## §0 — Source anchor

- **Source:** `core/data/bar_data/MYM_M15.csv` (sha256
  `24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58`), split into
  overnight (`[00:00, 09:29]` ET, same trading day) and RTH (`[09:30, 15:59]` ET)
  sub-sessions using the session-boundary convention already pinned on this exact panel
  by `lab/archive/msl_c1_mym_2026-08/construct_lib.py`
  (`RTH_OPEN_MIN`/`RTH_CLOSE_MIN`/`OVERNIGHT_CLOSE_MIN`), not invented here — four MSL
  campaigns (C1, C2, C3, S2B) already use this convention on MYM.
  **Authoritative script (this correction):**
  `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_stratified_rerun.py`.
  **Authoritative results:** `.../c2_c4_stratified_results.json` key
  `candidate2_overnight_range_STRATIFIED`. Superseded (secondary, disclosed) script/results:
  `c2_c4_increment_falsifiers.py` / `c2_c4_results.json` key `candidate2_overnight_range`.
- **Observed at:** 2026-08-29 (this session, both runs).
- **K:** [`discovery_manifests/mymdd_1_2026_08_29.json`](../../../discovery_manifests/mymdd_1_2026_08_29.json), K=5, this cell's own naive marginal `p_two_sided=0.372` (per `c2_c4_results.json`'s `candidate2_overnight_range` key — corrected 2026-08-30, Codex review, PR #223: an earlier draft of this bullet claimed no standalone p-value existed and that a BH-rank cross-check wasn't verifiable; both are available and match the manifest's own rank-4 row exactly, `bh_threshold=0.04`, `bh_reject: false`) — this candidate failed **both** naive alpha and BH in the original K=5 screen. Added retroactively 2026-08-30 for parity with MNQ's sibling notices' own `**K:**` bullet convention — this cell's `floor_at_k(5)=1.1150 > CAP=1.0` (the DSR-reachable band), same as MNQ's three K-correction-audit-flagged notices; disclosed, not yet resolved (see `Q-RANGEXFER-1` §11).

---

## §1 — The observation

**Constraint-audit catch #1 (same-day, load-bearing to §0):** the originating brief
framed this candidate as reusable "verbatim" from the corrected magnitude-persistence
battery. On reading the battery's own frozen spec
(`docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md` §4 D5), this
candidate is the **PAUSED "S2" construct**, not the un-paused "S1" one — overnight range
and RTH range are different series sharing a slow common volatility-regime state, and
independent-series IAAFT surrogation does not delete that confound. No full battery was
run; per the spec's own un-pause precondition (2), a $0 cheap falsifier was run instead
— *"does overnight-state conditioning beat matched day-session-history conditioning?"*

**Constraint-audit catch #2 (same-day, this correction — SUPERSEDES the original §1
below):** the first falsifier design (`c2_c4_increment_falsifiers.py`) computed two
**marginal** conditional rates — P(y=1|bias_new=1) = 0.7604 (n=313) vs.
P(y=1|bias_hist=1) = 0.7306 (n=297) — and diffed them: **+0.0297, 95% CI [−0.0325,
+0.0988], AMBIGUOUS.** An adversarial review caught that this does not test what "matched
... conditioning" means: two correlated predictors (both plausible vol-regime proxies)
can show near-identical marginal rates while one still carries large incremental
information the marginal comparison cannot see. The corrected design **stratifies on
`bias_hist` and measures `bias_new`'s lift within each stratum held fixed** — verified
independently before running (the underlying `bias`/`bias_hist`/`y` definitions are
algebraically identical between the two scripts; only the aggregation step changed).

**Corrected (authoritative) result:** within stratum `bprime=0` (day-history NOT
elevated, n=1,010): P(y=1|bias_new=1)=0.6963 (n=191) vs. P(y=1|bias_new=0)=0.3785
(n=819) — **lift +0.3178**. Within stratum `bprime=1` (day-history elevated, n=297):
P(y=1|bias_new=1)=0.8607 (n=122) vs. P(y=1|bias_new=0)=0.6400 (n=175) — **lift
+0.2207**. Both strata show a large, positive lift — the marginal near-tie was masking
real incremental information, not the absence of it. Block-bootstrap (circular,
60-session blocks, seed 20260829, n=4,000) on the **minimum** stratified lift (the
conservative read across both day-history states): mean **+0.2186**, 95% CI **[+0.1042,
+0.3216]**, entirely positive, **p(lift ≤ 0) = 0.00025** / **null-calibrated
p(null≥obs) = 3.4×10⁻⁶** (within-stratum circular-shift of the overnight
predictor, distinct rotations enumerated, identity included; n_null=1304 from
the sibling joint-gate cache vs original n=1307; per-stratum 0.00099 / 0.00338).
**VERDICT: INCREMENT** — decisive, not a near-miss. Recalibration does not
change the verdict.

## §2 — Why it stands out (the N signal)

- **Baseline:** the spec's own precommitted decision rule for the un-pause
  precondition — a clean increment un-pauses the "S2 reframed INCREMENTAL" path.
- **Delta:** the corrected design didn't just resolve the original AMBIGUOUS in one
  direction — it revealed the marginal comparison was the wrong question. Both
  strata's lifts (+31.8pp, +22.1pp) are an order of magnitude larger than the marginal
  diff (+3.0pp) that motivated the original HOLD.
- **Frequency check:** first instance under the corrected design on any instrument in
  this repo (a structurally analogous stratified design was reportedly used on the MNQ
  sibling campaign with a qualitatively similar reversal — cited as reported context
  from the reviewing session, not independently verified here; MYM's own numbers above
  are what this notice stands on).

## §3 — Candidate mechanisms (informal)

- Genuine overnight→RTH information transfer (news/positioning/liquidity carried
  through the Globex overnight session into the RTH open) beyond what yesterday's own
  RTH-range state already predicts — the large, both-strata-consistent lift is
  suggestive of a real transmission mechanism, not the mundane same-series persistence
  candidate 1 already characterized as canon-generic.
- Could still be partially confounded by a common-regime state that the two-predictor
  stratification only partially screens (it controls for ONE lag of same-series
  history, not the fuller joint structure a proper joint-surrogate null would model)
  — this is exactly why the spec's condition (3) still requires that design before a
  full battery-grade verdict, not just a stage-1 falsifier pass.

## §4 — Routing decision

**GRADUATE — to a Pre-Q, authoring deliberately deferred.**

Reason: the D5 stage-1 $0 precondition is now decisively cleared (CI entirely positive,
p=0.00025 / null-calibrated min-lift p=3.4×10⁻⁶, both strata consistent) — per the frozen spec's own un-pause logic this is
exactly the signal that licenses moving past "does S2 die for $0" into scoping the real
investigation. Not opened as a Pre-Q in this session: the operator's own task framing
for this batch explicitly named a follow-up session that pools MNQ's and MYM's GRADUATE
sets together before authoring any Pre-Q — opening one here would pre-empt that
batching decision. **Raised-bar route: none needed.** This is a conditioner-role
magnitude/range-transfer claim (same role class as candidate 1's
`daily-range-state-persistence`, no directional entry proposed) — the single-instrument
index-futures directional-timing raised bar scopes *directional intraday timing*
constructs; a magnitude-transfer conditioner claim sits structurally outside it, the
same reasoning that let candidate 1 skip Route 1/2/3 entirely. **Still outstanding
before a full battery or a build:** spec condition (3) — a joint-surrogate null design
passing its own adversarial review (still unbuilt, still out of a Notice-phase screen's
scope) — and condition (4), a separate operator GO. Both belong to the deferred Pre-Q,
not this notice.

Decision: GRADUATE
Reason: D5 stage-1 $0 precondition decisively cleared (CI entirely positive, p=0.00025 /
null-calibrated min-lift p=3.4×10⁻⁶, both strata consistent); Pre-Q authoring deferred to the planned MNQ+MYM pooling
session per the operator's own batch framing, not opened here.

---

## §5 — If HOLD: re-check trigger

Skip this section unless §4 = HOLD. **N/A here — superseded, not skipped-because-HOLD.**
The original 2026-08-29 marginal-comparison run's routing decision (`HOLD until
2027-03-01`) is superseded by this correction and no longer stands; no re-check trigger
applies to a GRADUATEd notice. Retained as an explicit dead-end pointer, not deleted,
so a future reader does not rediscover the old HOLD date and treat it as live.

---

## §10 — Audit hooks

```bash
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_stratified_rerun.py
# Expected: [candidate2_overnight_range_STRATIFIED] min-stratified-lift bootstrap:
#   mean=0.2186  CI=[+0.1042,+0.3216]  p(lift<=0)=0.00025 / null-calibrated p=3.4e-6
#   VERDICT=INCREMENT (unchanged; within-stratum enumerated null)

# Superseded secondary measurement (disclosed, not the D5 stage-1 answer):
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_increment_falsifiers.py
# Expected: [candidate2_overnight_range] diff=+0.0297  95% CI=[-0.0325,+0.0988]  VERDICT=AMBIGUOUS

grep "N-2026-08-29-mym-overnight-rth-range-transfer" docs/briefs/Q-*.md
# Expected: no matches yet (Pre-Q authoring deferred to the MNQ+MYM pooling session)
```

---

## Addendum — joint gate vs. candidate 4 (2026-08-29, append-only, does not change §1-§5 above)

A follow-up joint test
([`N-2026-08-29-mym-overnight-gap-joint-gate.md`](N-2026-08-29-mym-overnight-gap-joint-gate.md))
ran this candidate against candidate 4 (gap magnitude) directly, mirroring MNQ's
Q-RANGEXFER-1 joint stratification. Result: overnight range adds large, highly
significant lift (+38.2pp / +22.5pp, p≈0.00025) within *both* strata of gap's own
state — the dominant, robust predictor of the pair, replicating MNQ's finding that
overnight range (not gap) is the primary claim. That notice recommends, but does not
execute, merging this id with `overnight-gap-magnitude-range-conditioning` into
MNQ's `overnight-range-transmission` id — see that notice for the full comparison
and the reasoning. Nothing in this candidate's own GRADUATE routing above changes.

---

## Verification

```bash
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
    docs/notes/notice/N-2026-08-29-mym-overnight-rth-range-transfer.md --type notice
# Expected: RESULT: well-formed
```
