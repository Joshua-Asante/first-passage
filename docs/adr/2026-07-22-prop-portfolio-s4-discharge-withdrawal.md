# ADR 2026-07-22 — Prop-portfolio §4 falsifier: discharge WITHDRAWN (eval drawdown-locking correction)

**Status:** Accepted
**Superseded-by:** none
**Retain-until:** superseded by a fresh discharge under corrected geometry, or by the §4 hard date 2026-11-08
**Decision date:** 2026-07-22
**Authors:** Claude Code (measurement + recorder); operator authorised the re-MC (chat, 2026-07-22)
**Supersedes:** [`2026-07-12-prop-portfolio-four-friendly-firms.md`](2026-07-12-prop-portfolio-four-friendly-firms.md) in part — the §4 **discharge status only**. The program, its four-firm target set, the envelope, and the 2026-11-08 hard date all stand unchanged.
**Superseded-in-part-by:** none
**Related:** [`2026-07-14-prop-portfolio-existing-strategy-candidates.md`](2026-07-14-prop-portfolio-existing-strategy-candidates.md) (Class-S route) · [`2026-07-17-c1-rail-build-account-registration-go.md`](2026-07-17-c1-rail-build-account-registration-go.md) (**not** overturned — see §6) · measurement [`lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md`](../../lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md) · superseded scoring [`class_s_candidate1_scoring_2026-07-15/RESULTS.md`](../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md)
**Layer:** research-gate status. **No locked parameter, allocation, `dd_protection` constant, or Pine file is touched.**

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

> ⚠ **2026-08-07 reader-intercept (W1):** "remain current" above is scoped to the **EOD breach clock**. Intraday-honest re-measure of the four decisions of record is authorized by [`2026-08-07-w1-intraday-honest-engine-remeasure.md`](2026-08-07-w1-intraday-honest-engine-remeasure.md) (`Proposed`); do not invent new bust % here. Superseded-by on the figure-currency claim lands when W1 RESULTS Accept.
>
> ⚠ **2026-08-09 reader-intercept (W1 successor):** class_s 0.50× full+H1/H2 on the honest clock is published at [`lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md`](../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md) (both discharge tiers PASS the frozen 3.0%/50% floor; bootstrap still unmeasured). §4 restore-trigger rows above remain the gate; this measurement is not a discharge and invents no new Part A clearer for candidate #1. Frozen §4 body unedited.

**Current audit hook** (supersedes §10 hook 3 for any reader checking today's state; that hook is retained above unedited as the historical record of what this ADR verified at the time):

```bash
grep -n "dd_lock_offset_usd" core/firm_rules.py
# Expected (2026-08-04 onward): six occurrences reading 1_000_000.0, zero reading 100
python lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/remc_native_postfix_check_2026-08-04.py --post
# Expected: ALL MATCH (canonical path reproduces this ADR's corrected figures with zero override)
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-22 | Initial authoring; discharge withdrawn on corrected-geometry re-MC (operator-authorised) | Claude Code |
| 2026-08-04 | Addendum appended: the constant §10 hook 3 asserted was "NOT hand-edited" is now fixed at the source by [`ADR 2026-08-04`](2026-08-04-firm-rules-eval-lock-fix-applied.md). §1–§10 above (including hook 3, as historical record) left byte-unchanged; no decision in this ADR is altered. | Joshua (directive) + Claude Code (draft + apply) |
