# ADR 2026-08-04 — `core/firm_rules.py`: apply the 2026-07-22 eval-locking correction as the default

**Status:** `Accepted` — operator directive this session (2026-08-04): *"Yes, run the corrected re-MC and draft the amending ADR."* Authorizes both the confirmatory re-MC and the source-level edit this ADR records.
**Decision date:** 2026-08-04
**Authors:** Joshua (directive) + Claude Code (measurement + draft + apply)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** superseded by a firm rule change (§4 T2) or by a fix to the intraday-clock residual (§6) that supersedes this ADR's scope
**Related:** [`2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](2026-07-22-prop-portfolio-s4-discharge-withdrawal.md) (the decision this ADR codifies at the source — **not** superseded; that ADR's substantive verdict, §4 undischarged, is untouched) · measurement [`lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md`](../../lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md) · [`2026-08-04-tradeify-venue-descope-eval-included.md`](2026-08-04-tradeify-venue-descope-eval-included.md) (the eval this fix's correctness now matters for, since Tradeify-shaped research is not barred)
**Layer:** production config correctness (data-entry fix). **No `dd_protection` constant, allocation, Pine file, or lifecycle state is touched. No frozen gate threshold moves.**

---

## §0 — Rule 0 reads (production source, verified 2026-08-04)

| Source | Anchor | What it grounds |
|---|---|---|
| `core/firm_rules.py` L294–348, L385–414 | worktree, this session | Six `dd_type: "trailing_locking"` tiers carry `dd_lock_offset_usd: 100` on rows whose other fields (`profit_target_pct` 6.0, eval-only `min_trading_days`/`consistency_rule_pct`, eval micro caps) model the **evaluation** phase: `Tradeify_Select_{25K,50K,100K,150K}` and `MFFU_Rapid_{50K,100K}`. Both firm blocks carry their own dated OPEN DEFECT comment naming this exact fact and citing "re-MC + amending ADR, not a hand-edit." |
| `core/firm_rules.py` — `grep -n dd_lock_offset_usd` | worktree, this session | Confirms exactly six occurrences of the field, all six on the tiers above. `Bulenox_*` (5 tiers) and `BluSky_Premium_*` (2 tiers) are `dd_type: "trailing"` and carry **no** `dd_lock_offset_usd` key — structurally immune, not merely untested. |
| `core/mc/simulation.py:152-164` | verified this session | The `trailing_locking` branch: `floor = min(peak - max_dd_usd, starting_equity + dd_lock_offset_usd)`. The `min()` is what caps the floor's ascent; only this branch reads the field at all. |
| `tests/core/test_trailing_locking_boundary.py` | verified this session | The engine's own idiom for "pure fixed-$ trail, no lock": `dd_lock_offset_usd=1_000_000.0`. **Not `None`** — `None` makes the whole branch inert (no DD check at all), a different and much larger error. |
| `lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md` + `remc_eval_lock_fix.py` | committed 2026-07-22 | The measurement this ADR applies. Baseline-reproduction check built in: uncorrected arm returns 2.64% vs published 2.65% → `MATCH`, so the delta below is measured against a verified baseline. |
| `core/firm_rules.py` L354–364 (MFFU comment block) | worktree, this session | MFFU carries the **identical** defect, independently primary-sourced (article 13286542, "Rapid Plan Evaluation Stage Account Parameters" lists only the EOD MLL, no lock) and independently measured same day: Run-2 bust 2.64% → 4.25%. |
| `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` | frozen | Gate this fix does **not** move: `eval_bust_ceiling` 3.0%, `pass_floor` 50%, seeds (42,123,2026), 10k sims/seed, horizon 1500, inactivity disabled. |
| `docs/superpowers/specs/2026-07-30-tradeify-native-fade-program-design.md` §3.2a | verified this session | A **second, independent** defect on the same tiers: the breach is enforced intraday but the engine tests only at EOD close. Named here as an explicit residual (§6), **not** fixed by this ADR. |

**Gitignore pre-flight.** `**/*.pine` is ignored; no Pine source is read or cited. Three frozen CME panel CSVs (07-11 vintage, hash-pinned in `core/data/tv_exports/cme/SHA256SUMS`) were restored from the operator's local Downloads folder to re-run the existing correction harness; SHA256 verified byte-identical to the tracked manifest before use.

---

## §1 — Context

On 2026-07-22 a 90-day overlay re-verification of Tradeify's help centre found that **neither Tradeify nor MFFU applies drawdown locking during the evaluation phase** — Tradeify verbatim: *"Evaluation accounts do not have drawdown locking."* `core/firm_rules.py`'s eval-modeled rows for both firms nonetheless carried `dd_lock_offset_usd: 100`, giving the simulated eval a cushion the real eval does not have. [`ADR 2026-07-22`](2026-07-22-prop-portfolio-s4-discharge-withdrawal.md) recorded the consequence (the §4 falsifier discharge is withdrawn) but deliberately did **not** edit the constant — its own §6 states: *"the constant is not hand-edited... needs its own ADR + re-pin pass."* That ADR's own §10 audit hook #3 still asserts today that the constant is unedited; this ADR is the promised follow-up, twelve days later.

In the interim, every consumer that needed the corrected geometry applied it as a **per-script runtime monkey-patch** — `c1_band_rescore_2026-07-24`, `c1_cadence_inactivity_2026-08-02`, and the 07-22 study's own two scripts all mutate `firm_rules.FIRM_RULES[tier]["dd_lock_offset_usd"]` at runtime rather than reading a corrected default. That is real, accumulating technical debt: `prop_survivor_scoring.py` ships a documented CLI (`python -m discovery.prop_survivor_scoring --daily-pnl-csv ... --tiers Tradeify_Select_100K`), and any direct or naive invocation of it — including scoring the **first real seed candidate** for the currently-live Tradeify eval — silently inherits the wrong, optimistic geometry with no signal that a patch is expected. The next consumer inherits the stale default; that is exactly the failure this ADR closes.

**Decision driver (one sentence):** the correction has been measured, Rule-0-verified, and unanimously applied by every downstream consumer for twelve days by hand; the only thing not yet true is that the source of truth agrees with its own consumers, and the seed-sourcing effort now underway is about to produce candidates that will be scored against this exact config.

---

## §2 — Decision

**`dd_lock_offset_usd` is changed from `100` to `1_000_000.0` (the engine's own "unreachable lock" idiom) on all six `trailing_locking` eval tiers in `FIRM_RULES`:** `Tradeify_Select_25K`, `Tradeify_Select_50K`, `Tradeify_Select_100K`, `Tradeify_Select_150K`, `MFFU_Rapid_50K`, `MFFU_Rapid_100K`.

`dd_type` stays `"trailing_locking"` on all six — the fixed-dollar EOD trail itself is correct; only the lock's reachability changes. This is **not** a new modeling choice: it reproduces exactly the correction the 2026-07-22 re-MC already measured and every downstream consumer has already applied by hand.

**Effective:** immediately upon acceptance.
**Scope:** `core/firm_rules.py` only. No `core/mc/simulation.py`, `core/dd_protection.py`, `core/lifecycle.py`, allocation, or Pine file is touched.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Status quo — leave `100` in the source, keep relying on per-harness monkey-patches** | This is the state the 2026-07-22 ADR left standing for twelve days, explicitly as an interim, not a resting state. The risk it defers is concrete and imminent: seed sourcing for the live Tradeify eval is now the program's active work, and the first candidate scored via a fresh, undocumented invocation of `prop_survivor_scoring` would silently get the wrong answer. |
| **Set `dd_lock_offset_usd` to `None`** | Rejected in the original 2026-07-22 measurement and reaffirmed here: `None` makes the entire `trailing_locking` branch inert (no drawdown check of any kind), a materially larger and different error than the one being fixed. |
| **Re-derive a new "no lock" sentinel value instead of reusing `1_000_000.0`** | No reason to diverge from the engine's own established idiom (`tests/core/test_trailing_locking_boundary.py`) and the exact value every corrected harness since 07-22 already uses. A different sentinel would be a second thing to remember, not a simplification. |
| **Fix the intraday-clock defect (§3.2a) in the same pass** | Genuinely tempting — it is the same defect *family* (both make the eval geometry optimistic) on the same six tiers. Ruled out because it requires a materially larger change: per-day intraday-low derivation from trade-level data, threaded through the block-bootstrap resampling while preserving day-level pairing between a day's total P&L and its intraday excursion — an architecture change to `blocks_from_daily_pnl`/`run_tier_remc`, not a one-line data correction. Bundling it here would violate the one-ADR-one-decision discipline and risk rushing a resampling change under time pressure. Scoped explicitly as a tracked residual, §6. |
| **Re-run and re-publish every historical RESULTS.md that used the old default** | 15+ active scripts reference an affected tier by name; only three actually exercise the buggy branch (§0 grep confirms the rest read cost/cap constants only, never `dd_lock_offset_usd`). Of those three, two (`class_s_candidate1_scoring_2026-07-15`) already carry a `SUPERSEDED` banner from the 07-22 ADR; the third-party (`inactivity_on_remc.py`, 08-02) already monkey-patches correctly. Two older, pre-07-22, `DIAGNOSTIC ONLY` studies from a since-superseded R6 3-leg book (`tradeify_futures3_remc_2026-07-11`, `tradeify_futures3_bustcut_2026-07-11`) had no pointer and now do (§7). Recomputing dated historical artifacts, rather than pointer-correcting them, is not this repo's convention (see the 07-15 study's own banner: *"retained unedited as the historical record... do not cite as current"*) and was rejected for the same reason here. |

---

## §4 — Falsifier (what would revert this fix)

**H (what this ADR asserts, binary):** *`dd_lock_offset_usd: 1_000_000.0` on these six tiers correctly models each firm's evaluation-phase drawdown rule as currently published, and the canonical scoring path (`firm_kwargs` → `simulate_path`) now returns the same Part A figures the 07-22 correction study measured by hand, with zero runtime override.*

**H is FALSIFIED — and the fix is reverted or amended by a superseding ADR — if any trigger below fires.**

| # | Trigger | Threshold | Action |
|---|---|---|---|
| T1 | Post-fix confirmation (§7 Phase 2) does not reproduce the 07-22 corrected figures | \|measured − 07-22 corrected\| > 0.5pp on either tier's Run-2 bust | Do not flip `Accepted`; investigate before merging |
| T2 | Either firm re-publishes a rule stating the evaluation phase **does** apply drawdown locking | primary source, re-verified | Revert `dd_lock_offset_usd` to the venue-published lock amount on the affected tier(s) only; supersede |
| T3 | A future firm added to `FIRM_RULES` with `dd_type: "trailing_locking"` inherits a lock offset without an explicit eval-vs-funded check | any new tier added without a comment stating which phase it models | Block at engine pre-flight; this ADR's §5 forbidden-move list applies to new tiers too |

**Not admissible as a revert route:** reinstating `100` "to match old published numbers" — those numbers are already superseded and banner-stamped; reverting the source would re-introduce the exact drift this ADR closes.

**Revert action:** author a superseding ADR. Never edit this ADR's §2 in place.

**Trigger check schedule:** T1 at Phase 2 completion (this session). T2 at each 90-day venue-fact re-verify (next due ~2026-10-20, per the standing re-verification cadence). T3 on any new `FIRM_RULES` tier addition.

---

## §5 — Forbidden moves (under this ADR)

- **Treating this as a re-decision of the 2026-07-22 §4 falsifier discharge.** That ADR's substantive verdict — the prop-portfolio §4 falsifier is undischarged, hard date 2026-11-08 unchanged — is untouched. This ADR only makes the already-decided correction the *default*; it manufactures no new Part A clearer and discharges nothing.
- **Fixing the intraday-clock defect (§3.2a) opportunistically inside this same edit.** Named and ruled out in §3. Tracked as an open residual in §6, not silently dropped and not rushed.
- **Recomputing dated historical RESULTS.md files to match the new default.** The repo's convention is a pointer banner on the historical artifact, not a rewrite (§3, §7). The two banners added by this ADR follow the exact form of the existing 07-15 banner.
- **Widening this fix to Bulenox or BluSky.** Confirmed structurally immune (§0) — `dd_type: "trailing"` never reads `dd_lock_offset_usd`. Touching those blocks would be an unrelated, unmeasured change.
- **Loosening any §4 trigger without a superseding ADR** (Known Trap #12).

---

## §6 — Consequences

**Positive:**
- The source of truth agrees with every downstream consumer for the first time since the defect was found. A fresh, undocumented invocation of `prop_survivor_scoring`'s CLI — exactly what scoring a new seed candidate will require — now gets the correct geometry by default, with no tribal knowledge required.
- The 2026-07-22 ADR's own promised follow-up ("needs its own ADR + re-pin pass") is discharged.
- Removes a live risk to the seed-sourcing effort: the eval remains live for research (per the 2026-08-04 de-scope Addendum), and the first candidate scored against `Tradeify_Select_100K` or `MFFU_Rapid_100K` will be scored honestly.

**Negative consequences (real, not theatrical):**
- Three CME panel CSVs (07-11 vintage) that were gitignored and absent from this checkout were restored from a local Downloads copy to re-run the verification harness. This is normal per the standing Downloads→local workflow, not a new data dependency, but is recorded because it is a real local-environment action this ADR's verification depended on.
- Two dated, pre-07-22 diagnostic studies (`tradeify_futures3_remc_2026-07-11`, `tradeify_futures3_bustcut_2026-07-11`) needed a banner they had not yet received, twelve days after the sibling 07-15 study got one. Recorded as a gap this ADR closes, not a new problem it creates.

**Risks:**
- **The intraday-clock defect (§3.2a) remains live and unfixed on exactly these same six tiers.** Every bust figure produced by the now-corrected engine is *still* a lower bound against the venue's real-time breach enforcement — this ADR narrows the gap between modeled and real eval geometry, it does not close it. Direction is certain (further bust-rate increase); magnitude is unmeasured. Mitigation: named explicitly here rather than left implicit; a dedicated follow-up (per §3's alternative-considered reasoning) is the correct venue for the resampling-architecture work this would require.
- **A future engineer restoring `dd_lock_offset_usd: 100` "to make a candidate pass" would silently re-introduce the exact defect this ADR removes.** Mitigated by §5's explicit forbidden-move listing and by the six occurrences now all reading the corrected value with an inline comment citing this ADR.

**Downstream artifacts needing update (this commit):**
- [`core/firm_rules.py`](../../core/firm_rules.py) — the six `dd_lock_offset_usd` values; OPEN DEFECT comment blocks updated to state APPLIED, citing this ADR.
- [`lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md`](../../lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md) — `SUPERSEDED` banner added (done, this session).
- [`lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md`](../../lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md) — `SUPERSEDED` banner added (done, this session).
- [`docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](2026-07-22-prop-portfolio-s4-discharge-withdrawal.md) — Addendum appended noting §10 hook #3's "NOT hand-edited" assertion is now historical (true as of 07-22; superseded by this ADR). Decision prose (§2) not touched.
- [`docs/adr/INDEX.md`](INDEX.md) — regenerate.
- [`docs/SESSIONS.md`](../SESSIONS.md) — session entry.

---

## §7 — Implementation plan

- **Phase 0** — §0 anchors re-verified at implementation time. **DONE 2026-08-04.**
- **Phase 1** — banner two pre-07-22, previously-unflagged diagnostic studies. **DONE 2026-08-04**, this session.
- **Phase 2** — apply the six-value fix in `core/firm_rules.py`; run the new native-postfix confirmation script (`remc_native_postfix_check_2026-08-04.py --post`) with **zero runtime override**, confirm it reproduces the 07-22 corrected figures (T1 falsifier check). Attach the result below in §8.
- **Phase 3** — append the Addendum to the 2026-07-22 ADR. Regenerate `docs/adr/INDEX.md`. Add a `docs/SESSIONS.md` entry.
- **Phase 4** — `check_brief.py` + `check_adr_graph.py` + `check_status_consistency.py` + `check_falsifier_reachability.py` green; status stays `Accepted`.

---

## §8 — Verification result (Phase 2) — `T1 DISCHARGED`

**Pre-fix reproduction (before the edit landed).** `remc_eval_lock_fix.py` re-run at HEAD `b812667` against the frozen 07-11 panel bytes: baseline Run-2 bust **2.65%** vs published **2.65%** → `MATCH`, corrected Run-2 bust **4.74%** — exact match to the 2026-07-22 measurement, zero drift in twelve days.

**Post-fix native confirmation (after the edit landed) — `remc_native_postfix_check_2026-08-04.py --post`, ZERO runtime override:**

```
[phase] post  (no override applied in this script; reading firm_rules.py as committed)
[source] Tradeify_Select_100K.dd_lock_offset_usd = 1000000.0
[source] MFFU_Rapid_100K.dd_lock_offset_usd = 1000000.0
  Tradeify_Select_100K: run2 bust 4.74% vs expected 4.74% (post-fix) -> MATCH
  MFFU_Rapid_100K: run2 bust 4.25% vs expected 4.25% (post-fix) -> MATCH

[verdict] ALL MATCH -- the canonical path already returns the post-fix numbers with zero override.
```

Both tiers reproduce the 2026-07-22 corrected figures **exactly** (Tradeify 4.7433% ≈ 4.74%, MFFU 4.2533% ≈ 4.25%) via `firm_kwargs` → `simulate_path`, with no monkey-patch anywhere in the call chain. **T1 does not fire.**

**Regression check.** `tests/core/test_trailing_locking_boundary.py`: 9/9 pass. Full suite (`pytest tests/`): **1251 passed, 22 skipped, 0 failed** — no regression anywhere in the repo from this edit. One pre-existing test (`test_mc_preflight.py::test_firm_kwargs_dd_type_dispatch`) had hardcoded the *old* `100.0` value as its expected result; it failed on the fix landing (correctly — it was asserting the bug) and was rewritten to assert against the live `FIRM_RULES` value plus a `>= 1_000.0` sanity floor, so it can no longer silently re-encode a future stale default.

**Self-caught defects during verification (recorded, not silently fixed):** the first draft of `remc_native_postfix_check_2026-08-04.py` wiped `sys.argv` (needed so the imported `run_class_s_c1_scoring` module's own argparse doesn't choke) *before* parsing this script's own `--pre`/`--post` flag, silently discarding it; caught by an immediate `--help` smoke-test before the full run. A second draft reused a loop variable across two separate loops for the JSON report's metadata field — harmless in this run only because both affected tiers share the identical fix value, but a real bug, fixed before commit.

---

## §10 — Audit hooks (runnable)

```bash
# 1. All six tiers carry the corrected, unreachable offset — no hand-revert.
grep -n "dd_lock_offset_usd" core/firm_rules.py
# Expected: six occurrences, all reading 1_000_000.0 (or a comment immediately above
# a 1_000_000.0 assignment), zero reading 100

# 2. Bulenox/BluSky remain structurally untouched (different dd_type, no lock field).
grep -n '"dd_type": "trailing"' core/firm_rules.py | wc -l
# Expected: 7 (5 Bulenox + 2 BluSky), unchanged by this ADR

# 3. No dd_protection, lifecycle, allocation, or Pine file changed.
git diff --stat HEAD~1 -- core/dd_protection.py core/lifecycle.py core/strategies/ 2>/dev/null
# Expected: empty

# 4. The canonical path reproduces the 07-22 corrected figures with ZERO override.
python lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/remc_native_postfix_check_2026-08-04.py --post
# Expected: ALL MATCH

# 5. Both pre-07-22 diagnostic studies now carry a correction pointer.
grep -l "SUPERSEDED 2026-07-22" lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md \
  lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md
# Expected: both files listed

# 6. The 07-22 ADR carries the addendum pointing here; its decision prose is untouched.
grep -n "Addendum 2026-08-04" docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md
git log -p --follow -- docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md | \
  grep -A2 "^-.*falsifier discharge is WITHDRAWN"
# Expected: addendum present; the §2 decision line shows no removal line

# 7. The intraday-clock residual is named, not silently dropped.
grep -n "3.2a\|intraday" docs/adr/2026-08-04-firm-rules-eval-lock-fix-applied.md | head -5
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python "$HOME/.claude/skills/brief-authoring/scripts/check_brief.py" \
  docs/adr/2026-08-04-firm-rules-eval-lock-fix-applied.md --type adr
python scripts/check_adr_graph.py
python scripts/check_status_consistency.py
python scripts/check_falsifier_reachability.py

# §0 anchors still current
git log -1 --format="%h %cs core/firm_rules.py" -- core/firm_rules.py
git log -1 --format="%h %cs core/mc/simulation.py" -- core/mc/simulation.py

# The fix reproduces the measured delta
python lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/remc_native_postfix_check_2026-08-04.py --post
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-04 | Initial authoring, `Accepted` on operator directive this session. Six `dd_lock_offset_usd` values corrected in `core/firm_rules.py`; two pre-07-22 diagnostic studies banner-stamped; Addendum appended to the 2026-07-22 ADR. Intraday-clock defect (§3.2a) named and explicitly scoped as a tracked, not-executed-here residual. | Joshua (directive) + Claude Code (draft + apply) |
