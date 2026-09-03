# ADR 2026-07-22 — Prop-portfolio §4 falsifier: discharge WITHDRAWN (eval drawdown-locking correction)

**Status:** Accepted
**Disposition note:** §4/§5 **overridden 2026-09-03** by the operator ruling in the addendum below — candidate #1 re-admitted, §4 discharge restored, EOD-clock only. The ADR itself stands.
**Superseded-by:** none
**Retain-until:** superseded by a fresh discharge under corrected geometry, or by the §4 hard date 2026-11-08
**Decision date:** 2026-07-22
**Authors:** Claude Code (measurement + recorder); operator authorised the re-MC (chat, 2026-07-22)
**Supersedes:** [`2026-07-12-prop-portfolio-four-friendly-firms.md`](2026-07-12-prop-portfolio-four-friendly-firms.md) in part — the §4 **discharge status only**. The program, its four-firm target set, the envelope, and the 2026-11-08 hard date all stand unchanged.
**Superseded-in-part-by:** none
**Related:** [`2026-07-14-prop-portfolio-existing-strategy-candidates.md`](2026-07-14-prop-portfolio-existing-strategy-candidates.md) (Class-S route) · [`2026-07-17-c1-rail-build-account-registration-go.md`](2026-07-17-c1-rail-build-account-registration-go.md) (**not** overturned — see §6) · measurement [`lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md`](../../lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md) · superseded scoring [`class_s_candidate1_scoring_2026-07-15/RESULTS.md`](../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md)
**Layer:** research-gate status. **No locked parameter, allocation, `dd_protection` constant, or Pine file is touched.**

> ## ⚠ Reader-intercept 2026-09-03 — every "3.0%" below is the **superseded** ceiling, and candidate #1's own figures now sit under the live one
>
> **The live Part A eval bust ceiling is 5.0% (since 2026-08-26** —
> [`prereg v2`](../briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) §3, an
> operator risk-tolerance override; `DEFAULT_PREREG` points at it**).** **All four** of §2's
> corrected-geometry figures — Bulenox 3.51%, **Tradeify_Select_100K 4.74%**, **MFFU_Rapid_100K
> 4.25%**, BluSky 4.44% — sit strictly between 3.0% and 5.0%. Read mechanically, "zero clearers,
> `discharges_falsifier = False`" becomes **four** clearers including **both** `trailing_locking`
> tiers, and §4's "≥2 firms, ≥1 `trailing_locking`" is satisfied on numbers already published here.
>
> **That is exactly the move §5 forbids** — and on **2026-09-03 the operator elected it anyway.**
> Candidate #1 is **RE-ADMITTED** and the §4 discharge is **RESTORED** on those §2 figures; §4's
> restore-trigger table and §5's forbidden move are **overridden but unedited**, kept as the record
> of what was overridden. See
> [Addendum 2026-09-03](#addendum-2026-09-03--candidate-1-re-admitted-at-the-50-ceiling-accepted)
> for the ruling, the collision it settles, and the superseded prospective-only case.
>
> ⚠ **The discharge is EOD-clock only.** The sole 1.00× intraday-honest measurement of candidate #1
> puts real bust at **32.33%** — a failure at 3.0% and 5.0% alike — and it is not gate-grade, so it
> settles nothing either way. Cite this discharge **only** with that qualifier. It is not a finding
> that candidate #1 survives an honest clock, and it is not a pass, a deployment, or a capital
> authorization.
>
> Frozen body below unedited (Trap #12); banner placed upstream of §2/§4/§5 per
> [`operational_rules.md`](../operational_rules.md) §14.

---

## §0 — Rule 0 reads (production source, this session)

- `core/firm_rules.py` — the six `trailing_locking` eval rows carrying `dd_lock_offset_usd: 100`.
- `core/mc/simulation.py:123-135` — `floor = min(peak - max_dd_usd, starting_equity + dd_lock_offset_usd)`; the `min()` caps the floor's ascent.
- `tests/core/test_trailing_locking_boundary.py` — the engine's own "no lock" idiom (`dd_lock_offset_usd=1_000_000.0`).
- `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` — frozen gate: bust ceiling 3.0%, pass floor 50%, seeds (42,123,2026), 10k sims/seed, horizon 1500. **Unchanged by this ADR.**
- `lab/discovery/prop_survivor_scoring.py::discharges_falsifier` — "≥2 firms clear Part A, of which ≥1 is `trailing_locking`."
- Primary sources re-verified 2026-07-22: [Tradeify 10495897](https://help.tradeify.co/en/articles/10495897-rules-trailing-max-drawdowns), [MFFU 13286542](https://help.myfundedfutures.com/en/articles/13286542).

## §1 — Context

The 2026-07-12 prop-portfolio ADR carries a §4 falsifier discharged on 2026-07-15 by Class-S candidate #1: two firms cleared Part A (headline bust ≤ 3.0%), including at least one `trailing_locking` tier — **Tradeify_Select_100K at 2.65% and MFFU_Rapid_100K at 2.64%**.

A 90-day overlay re-verification of Tradeify's help centre on 2026-07-22 found that **neither firm applies drawdown locking during the evaluation phase** — Tradeify verbatim: *"Evaluation accounts do not have drawdown locking."* The `firm_rules.py` eval rows nonetheless carried `dd_lock_offset_usd: 100`, giving the simulated eval a cushion the real eval does not have. The two tiers carrying the defect are exactly the two tiers the discharge rested on.

## §2 — Decision

**The §4 falsifier discharge is WITHDRAWN.** Under corrected eval geometry, **zero** frozen tiers clear Part A and `discharges_falsifier = False`.

| Tier | dd_type | Run-2 bust (corrected) | Part A |
|---|---|---|---|
| Bulenox_100K | trailing | 3.51% | False *(control, unchanged)* |
| Tradeify_Select_100K | trailing_locking | **4.74%** (was 2.65%) | **False** *(was True)* |
| MFFU_Rapid_100K | trailing_locking | **4.25%** (was 2.64%) | **False** *(was True)* |
| BluSky_Premium_100K | trailing | 4.44% | False *(control, unchanged)* |

The program's §4 falsifier is **undischarged**, hard date **2026-11-08** unchanged. The frozen gate thresholds are **not** touched — this is a corrected *input*, not a moved goalpost. Moving the 3.0% ceiling to re-admit the candidate is a forbidden move (§5).

**Effective:** immediately. **Scope:** discharge status only.

## §3 — Evidence quality

- **Baseline reproduces**: the uncorrected arm returns **2.64%** against the published **2.65%** → `MATCH`. The delta is measured against a verified baseline, not an assumed one.
- **Controls behave**: both `dd_type="trailing"` tiers (no lock field) return unchanged values — the correction touched only what it should.
- **Same everything else**: identical panel bytes, frozen seeds/sims/horizon, same `score_candidate` path at the $100K basis. The arms differ only in `dd_lock_offset_usd`.
- **A discarded first attempt** (baseline 15.83%, caused by summing the raw $200K panel instead of rescaling to $100K) was caught *by* the reproduction check and never reported. Recorded in the RESULTS as the reason the check earns its cost.

## §4 — Falsifier (what would restore the discharge)

**If** a pre-registered candidate scores ≥2 firms at headline bust **≤3.0%** including **≥1 `trailing_locking`** tier, at the frozen seeds/sims/horizon under **corrected** eval geometry, **then** the §4 discharge is restored by a superseding ADR; **otherwise** §4 remains undischarged through the 2026-11-08 hard date.

| Trigger | Threshold | Action |
|---|---|---|
| Corrected-geometry Part A re-score | ≥2 tiers ≤3.0% bust, ≥1 `trailing_locking` | Restore discharge (superseding ADR) |
| Firm publishes eval-phase locking | primary source, re-verified | Re-run; may restore discharge |
| 2026-11-08 reached undischarged | — | §4 falsifier fires per the 2026-07-12 ADR |

Admissible routes: a new candidate book, a corrected-geometry re-score of an existing one, or a documented firm rule change (re-verify before relying on it).

**Not** admissible: relaxing the 3.0% ceiling, dropping the `trailing_locking` requirement, re-scoring at a haircut the gate does not define, or reinstating the lock in `firm_rules.py` without primary-source evidence that the firms apply it in eval.

**Check schedule:** at the 2026-08-08 checkpoint and again before the 2026-11-08 hard date.

## §5 — Forbidden moves (under this ADR)

- **Moving the 3.0% ceiling, the 50% pass floor, or the `trailing_locking` requirement to re-admit candidate #1.** The gate is frozen and pre-registered; the input was wrong, not the bar. Tempting because 4.74% "only just" misses — that framing is the degeneration move this ADR exists to block.
- **Quietly restoring `dd_lock_offset_usd: 100` semantics** in any harness's local copy to recover the old numbers.
- **Citing the published 2.65% / 2.64% Part A figures** as current. They are superseded; the artifacts are banner-stamped.
- **Treating this as overturning the c1 rail GO** — different gate, different harness (§6).
- **Scaling the +2.10pp 1.00× delta down to 0.50×** to "estimate" the WATCH-1 arm. Halved risk interacts with the barrier non-linearly; that number must be run, not inferred.

## §6 — Consequences

**The c1 rail GO stands.** It rests on Q-RAIL-1 execution fidelity and the WATCH-1 0.50× haircut re-MC — a different harness and a different gate from the Part A screen withdrawn here. Nothing about the rail build, the registered account, or the attended posture changes.

**But one real open input to B7:** the GO's §6 risk framing cites WATCH-1 0.50× figures (full-panel bust 0.08%, H1 0.14%, bootstrap-95th 0.77%) computed under the **defective** geometry. They are known-optimistic by an **unmeasured** amount — the corrected run was stopped on runtime cost before reaching that arm. Closing it needs only the full-panel reference (≈3 min), not the n=100 bootstrap. **Recommend closing before B7 arms.**

**Program-level:** the prop-portfolio §4 falsifier returns to undischarged with ~3.5 months to the hard date. Whether that shifts research priority is an operator call, not a consequence this ADR asserts.

**Positive:** the gate now measures the geometry the firms actually apply. A discharge earned under corrected inputs will mean what it says.

## §10 — Audit hooks (runnable)

```bash
# The measurement reproduces, with its own baseline check
python lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/remc_g8_discharge_check.py

# Frozen gate thresholds untouched by this ADR
grep -n "3.0%\|50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md | head

# The defect is recorded at the config, and the constant is NOT hand-edited
grep -n "dd_lock_offset_usd" core/firm_rules.py | head
grep -c "Evaluation accounts do not have drawdown locking" core/firm_rules.py   # expect >= 1

# Superseded figures are banner-stamped, not silently edited
grep -n "SUPERSEDED" lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md | head
```

## Verification

```bash
python "$HOME/.claude/skills/brief-authoring/scripts/check_brief.py" docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md --type adr
python scripts/check_adr_graph.py
python scripts/check_status_consistency.py
```

## Addendum 2026-08-04 — the constant this ADR left unedited is now fixed; §10 hook 3 is historical

**Status: `Accepted` — operator directive this session, "run the corrected re-MC and draft the amending ADR."**

This ADR's §10 audit hook 3 asserts:

```bash
# The defect is recorded at the config, and the constant is NOT hand-edited
grep -n "dd_lock_offset_usd" core/firm_rules.py | head
grep -c "Evaluation accounts do not have drawdown locking" core/firm_rules.py   # expect >= 1
```

That was true on 2026-07-22 and remains true of the *state this ADR recorded* — but is no longer true of `core/firm_rules.py` at HEAD. [`ADR 2026-08-04`](2026-08-04-firm-rules-eval-lock-fix-applied.md) applies the correction this ADR's §6 promised ("needs its own ADR + re-pin pass") twelve days later: all six `trailing_locking` eval tiers now read `dd_lock_offset_usd: 1_000_000.0` (the engine's own unreachable-lock idiom) instead of `100`.

**This addendum does not alter anything in §1–§10 above.** The decision this ADR records — the §4 falsifier discharge is withdrawn, `discharges_falsifier = False`, hard date 2026-11-08 unchanged — is untouched. Applying the correction to the source does not create a new Part A clearer; it only makes the *default* agree with what every downstream harness (`c1_band_rescore_2026-07-24`, `c1_cadence_inactivity_2026-08-02`, this ADR's own `remc_eval_lock_fix.py`/`remc_g8_discharge_check.py`) has been applying via runtime monkey-patch since this ADR was accepted.

**Re-confirmed at HEAD 2026-08-04, before the fix landed:** `remc_eval_lock_fix.py` reproduced this ADR's own baseline (2.64% vs published 2.65%, `MATCH`) and its corrected delta (Run-2 bust 2.65% → 4.74%, +2.10pp) exactly — no drift in twelve days. The corrected-geometry figures in §2/§3 above remain current **as EOD-clock lower bounds**.

> ⚠ **2026-08-07 / 2026-08-22 reader-intercept (W1):** "remain current" above is scoped to the **EOD breach clock**. Intraday-honest re-measure is authorized by [`2026-08-07-w1-intraday-honest-engine-remeasure.md`](2026-08-07-w1-intraday-honest-engine-remeasure.md) (`Accepted` 2026-08-22). Class-S 0.50× honest-clock RESULTS landed; do not invent new bust % here. Remaining three decisions of record still owed as measurement.
>
> ⚠ **2026-08-09 reader-intercept (W1 successor):** class_s 0.50× full+H1/H2 on the honest clock is published at [`lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md`](../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md) (both discharge tiers PASS the frozen 3.0%/50% floor; bootstrap still unmeasured). §4 restore-trigger rows above remain the gate; this measurement is not a discharge and invents no new Part A clearer for candidate #1. Frozen §4 body unedited.

**Current audit hook** (supersedes §10 hook 3 for any reader checking today's state; that hook is retained above unedited as the historical record of what this ADR verified at the time):

```bash
grep -n "dd_lock_offset_usd" core/firm_rules.py
# Expected (2026-08-04 onward): six occurrences reading 1_000_000.0, zero reading 100
python lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/remc_native_postfix_check_2026-08-04.py --post
# Expected: ALL MATCH (canonical path reproduces this ADR's corrected figures with zero override)
```

## Addendum 2026-09-03 — candidate #1 re-admitted at the 5.0% ceiling (`Accepted`)

**Status:** `Accepted` — **operator ruling, 2026-09-03** (chat, verbatim: *"I am allowing
Candidate 1 to be readmitted. No need for the superceding ADR, I just need to edit the existing
one"*). The operator elected the **retroactive** reading and **waived** the superseding-ADR
requirement this addendum's own §"What the operator is actually being asked" had set for that
election, directing the ruling be recorded here instead. Recorded, not decided, by the author.

It moves no number, touches no `core/`, Pine, allocation, `dd_protection`, or rail surface, and
opens no re-MC — the discharge rests on figures already published in §2 above. $0 / K=0.

> ⚠ **The adverse evidence is not repealed by this ruling and is restated here so no reader
> mistakes a discharge for a survival claim.** Every §2 figure is an **EOD-clock lower bound**. The
> only 1.00× intraday-honest measurement that exists for candidate #1 puts real bust at **32.33%**
> against EOD 2.50%
> ([`RESULTS_INTRADAY_W1`](../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md)
> §Non-vacuity) — a failure at 3.0% and 5.0% alike. It is **not** gate-grade (horizon 400 / 200 sims
> per seed at book level, not the frozen 10k × 3 / horizon-1500 contract) and it does not resolve
> `MFFU_Rapid_100K` separately, so it cannot *settle* the question either way. **What this ruling
> discharges is the §4 falsifier on the EOD clock. It is not a finding that candidate #1 survives an
> honest clock, and it must never be cited as one.** The gate-grade honest-clock re-score remains
> unrun and is the measurement that would settle it.

### The collision

Two ratified documents now point opposite ways on the same arithmetic:

| | Says |
|---|---|
| This ADR, §4 + §5 | §4 restores only at **bust ≤3.0%**; *"Moving the 3.0% ceiling … to re-admit candidate #1"* is a **forbidden move** — *"the input was wrong, not the bar"* |
| [`prereg v2`](../briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) §3 | Part A ceiling is **5.0%**, live since 2026-08-26 |

Candidate #1's corrected-geometry figures, published in §2 above, are **Tradeify_Select_100K
4.74%** and **MFFU_Rapid_100K 4.25%** — two firms, both `trailing_locking`, **both under 5.0%**.
Bulenox (3.51%) and BluSky (4.44%) clear it too, so the raise turns a **zero**-clearer table into a
**four**-clearer one. The ceiling raise does not merely *permit* re-admission; applied mechanically
it **performs** it, with no new measurement, on the exact candidate §5 names.

**The clock axis is the second, independent bar — and it does not resolve the question either.**
Every figure in §2 is an **EOD-clock lower bound**, as this ADR's own 2026-08-07/08-22 intercept
already says. On the intraday-honest clock the two `trailing` controls collapse — Bulenox
3.51% → **26.77%**, BluSky 4.44% → **32.26%** at 1.00×
([`R1 7-tier`](../../lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23/RESULTS.md)) — failing at
either ceiling. On the `trailing_locking` side W1 published the 0.50× arm at gate grade (0.72%) —
but it also carries a **1.00×** honest-clock guard run, and that run is **strongly adverse**:
**real bust 32.33%** / pass 57.17% against EOD 2.50% / 71.00%
([`RESULTS_INTRADAY_W1`](../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md)
§Non-vacuity). At 32.33% candidate #1 fails at **3.0% and 5.0% alike**, so the clock axis, as far as
it has been measured, points the same way this ruling does.

**It is not gate-grade, and that is the point.** That run is horizon 400 / 200 sims per seed at book
level, not the frozen 10k × 3 / horizon-1500 contract, and it does not resolve `MFFU_Rapid_100K`
separately. So the `trailing_locking` limb is **undetermined at gate grade** — no reader can
*settle* this collision by pointing at the clock, and equally no reader should be told the clock is
silent. The only honest summary is: the sole 1.00× honest-clock evidence that exists is adverse, and
the measurement that would settle it has not been run.

**Neither document saw this.** v2's §5 is careful to bar reading the `aegis_orbmnq_combined_book_2026-08-26`
study as having cleared any gate — but it never mentions candidate #1, this ADR, or the forbidden
move. ⚠ **Corrected 2026-09-03:** an earlier draft of this line claimed v2 "greps clean" for
`withdrawal` / `forbidden` / `candidate #1`. It does not — v2's own §5 heading (line 171) is
"Forbidden moves", so that disjunction always hits, and the prose disagreed with its own hook 3.
What is actually absent from v2 is any reference to **candidate #1** or to **this ADR**; hook 3
below is narrowed to those collision-specific terms. v2's §1 states *"no
DISC-CAMP-0 survivor has been scored under this version"*, which is true and is precisely why the
gap went unnoticed: candidate #1 was scored under **v1**, so it is invisible to a
"nothing-scored-yet" check while remaining fully re-admissible by arithmetic.

### Ruling (operator, 2026-09-03)

> **The 5.0% ceiling applies to candidate #1. Class-S candidate #1 is RE-ADMITTED, and the §4
> falsifier discharge of 2026-07-15 is RESTORED on the corrected-geometry figures published in §2
> — `Tradeify_Select_100K` 4.74% and `MFFU_Rapid_100K` 4.25%, two firms, both `trailing_locking`,
> both under 5.0%. §5's forbidden move is overridden by operator election, not repealed by
> argument.**

**Reading this correctly.** §5 barred *"moving the 3.0% ceiling … to re-admit candidate #1"* on the
grounds that *"the input was wrong, not the bar."* That reasoning is not refuted here and is not
withdrawn. What happened instead is that the bar moved for independent reasons two months later
([`prereg v2`](../briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) §8, an
operator risk-tolerance dial), and the operator has now elected to let candidate #1 be read at the
moved bar. **This is an operator override of a frozen pre-registered gate, exercised on the
operator's own authority over risk tolerance — it is not a measurement result, and no measurement
changed.** The three sections it overrides (§4's restore-trigger table, §5's forbidden move, and
this addendum's own superseding-ADR requirement) stay in the file, unedited, as the record of what
was overridden.

**What the discharge now rests on.** Nothing new. The §2 table, scored 2026-07-15 under prereg v1
geometry and re-scored 2026-07-22 under the corrected eval geometry, read against a 5.0% instead of
a 3.0% ceiling. Four tiers clear — Bulenox 3.51%, Tradeify_Select_100K 4.74%, MFFU_Rapid_100K 4.25%,
BluSky_Premium_100K 4.44% — and §4's *"≥2 firms clear Part A, of which ≥1 is `trailing_locking`"*
is satisfied twice over. `discharges_falsifier` reads **True** on those inputs.

**What is still owed.** The gate-grade intraday-honest re-score (see the Status warning above). Until
it runs, every citation of this discharge must carry the EOD-clock qualifier, exactly as
[`docs/mc_anchor_history.md`](../mc_anchor_history.md) requires of the historical MC anchor. A
discharged falsifier is not a pass, a deployment, or a capital authorization — those remain
separate, always-revocable axes.

### The prospective-only reading, superseded 2026-09-03 (retained as the record of what was overridden)

The four arguments below were this addendum's `Proposed` case for the opposite disposition. The
operator's ruling supersedes them. They are kept unedited because §5's reasoning is what the
override overrides, and a reader who cannot see it cannot audit the override.

- **It is what both documents already say.** §5 bars the ceiling move *"to re-admit candidate #1"*
  — a purpose-scoped bar, not a bar on the number. v2 §8 frames its own change as *"a general
  risk-tolerance dial, not a verdict on any one candidate."* Prospective-only is the unique
  reading under which both sentences are simultaneously true.
- **v2's own grounds do not reach candidate #1.** §8 rests the raise on the operator's tolerance
  for *modeled* risk going forward. Nothing in it re-argues the 2026-07-22 correction, and §8
  explicitly disclaims being *"a re-derivation."* A raise that silently reverses a withdrawal it
  never discusses is decided by side effect, not by decision.
- **The alternative is the named degeneration move.** §5 calls the 4.74%-only-just-misses framing
  *"the degeneration move this ADR exists to block."* Discharging §4 at 4.74% because the bar
  moved two months later is that move with a delay.
- **It costs the program nothing it is entitled to.** Candidate #1 can still be re-admitted — by
  the routes §4 already lists (a fresh pre-registered candidate, a corrected-geometry re-score, a
  documented firm-rule change), or by an explicit operator ADR that re-admits it *on stated
  grounds*. What this ruling bars is re-admission **by arithmetic drift alone**.

### What the operator was asked, and what they elected

Ratify prospective-only, **or** elect the opposite (the 5.0% ceiling is retroactive and §4
is discharged by candidate #1 on the 4.74% / 4.25% figures) — which this addendum said would be a §4
**discharge** and therefore need a superseding ADR under §4's own restore-trigger table, not an
addendum. A third option: ratify prospective-only *and* commission the corrected-geometry re-score
at 5.0% as a fresh, pre-registered candidate.

**Elected 2026-09-03: the second option, with the superseding-ADR requirement waived.** The operator
directed that the ruling be recorded by editing this ADR rather than by a new one. Recorded above.
⚠ Consequence a future reader must not miss: the §4 restore-trigger table in §4 and the forbidden
move in §5 are now **overridden but unedited**. Read them as history, and read this addendum for the
live disposition. The third option is not foreclosed — the gate-grade honest-clock re-score is still
the measurement that would put this discharge on measured rather than elected footing.

**Already owed, now answered:** three surfaces log this as an open ruling and can cite this
addendum — [`class_s_w1_bootstrap_honest_2026-09-02/RESULTS.md`](../../lab/analysis/c1/class_s_w1_bootstrap_honest_2026-09-02/RESULTS.md)
§(c), [`SESSIONS.md`](../SESSIONS.md) (owed-items line), and
[`2026-09-03-seven-strategy-select-campaign-state.md`](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md)
row D5, which gates Phase 7 on it.

**Not decided here:** anything about the 2026-11-08 hard date (unchanged), the 50% pass floor
(unchanged), the `trailing_locking` requirement (unchanged), Part B's 1.0% funded ceiling
(unchanged), or the four-firm set (restored 2026-09-01 by the
[F1 reversal](2026-08-04-tradeify-venue-descope-eval-included.md#addendum-2026-09-01--f1-reversed-a-tradeify-resting-discharge-now-counts-toward-4)
— election only, no code change; `AUTOMATION_FRIENDLY_PROP_FIRMS` and both preregs' frozen
`$100K×4` tier set always contained Tradeify and never moved).

### Audit hooks (runnable)

```bash
# 1. The live ceiling is 5.0% and the loader agrees.
grep -n "2026-08-26-prop-survivor-scoring-prereg-v2" lab/discovery/prop_survivor_scoring.py

# 2. §5's forbidden move is still present and unedited.
grep -n "Moving the 3.0% ceiling" docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md

# 3. v2 still does NOT address candidate #1 or this ADR (the gap this addendum names).
#    Collision-specific terms ONLY: v2's own §5 heading is "Forbidden moves", so that phrase
#    is not a discriminator and must never appear in this hook (it made the hook self-hitting).
grep -ni "candidate #1\|candidate 1\|s4-discharge-withdrawal\|discharge WITHDRAWN" \
  docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md   # expect: empty

# 4. INVERTED BY THE 2026-09-03 RULING. 4.74%/4.25%-under-5.0% IS now a discharge — but an
#    EOD-clock one. Every hit must carry that qualifier; a bare "discharges" with no clock
#    caveat is the defect this hook now looks for.
grep -rn "4.74\|4.25" --include="*.md" docs/ lab/ STATE.md | grep -i "discharg"
# Known surfaces as of 2026-09-03: this ADR; tradeify_eval_lock_correction_2026-07-22/RESULTS.md;
# class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md; the 2026-08-05 claim-alignment audit
# (frozen). Anything NEW in that list needs checking.

# 5. The override is visible, not silent: §5's forbidden move is still in the file, unedited.
grep -n "Moving the 3.0% ceiling" docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md
grep -n "overridden but unedited" docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-22 | Initial authoring; discharge withdrawn on corrected-geometry re-MC (operator-authorised) | Claude Code |
| 2026-08-04 | Addendum appended: the constant §10 hook 3 asserted was "NOT hand-edited" is now fixed at the source by [`ADR 2026-08-04`](2026-08-04-firm-rules-eval-lock-fix-applied.md). §1–§10 above (including hook 3, as historical record) left byte-unchanged; no decision in this ADR is altered. | Joshua (directive) + Claude Code (draft + apply) |
| 2026-09-03 | Head reader-intercept + **Addendum 2026-09-03 (`Proposed`)**: names the collision between §5's forbidden move and prereg v2's 5.0% ceiling — candidate #1's own §2 figures (4.74% / 4.25%, both `trailing_locking`) clear 5.0%, so the raise would re-admit it by arithmetic. Proposes prospective-only. §1–§10 byte-unchanged; no discharge, no re-MC, no number moved. $0/K=0. | Claude Code (Opus 5) |
| 2026-09-03 | **Addendum ratified as `Accepted`, in the OPPOSITE disposition to the one it proposed** — operator ruling: candidate #1 **re-admitted** at the 5.0% ceiling, §4 discharge **restored** on the §2 corrected-geometry figures, superseding-ADR requirement **waived** by operator direction. §1–§10 still byte-unchanged; §4's restore-trigger table and §5's forbidden move overridden but unedited. No re-MC, no number moved, no `core/`/Pine/allocation/`dd_protection`/rail surface touched. Discharge is **EOD-clock only** — the 32.33% honest-clock guard run stands unrepealed. $0/K=0. | Joshua (ruling) + Claude Code (record) |
