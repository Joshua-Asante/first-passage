# Q-RANGEXFER-1 — Does MNQ's overnight-session range transmit genuine same-day information to RTH range, beyond a shared-regime confound?

**Status:** `OPEN`
**Authored:** 2026-08-29
**Closed:** N/A
**Authors:** Claude Code (D-S-A gate + stage-1 falsifier + joint gate), operator GO owed for Phase 1
**Parent question:** N/A (new investigation thread; forks its own sub-question below)
**Sub-questions opened:** Q-RANGEXFER-1.a (gap-magnitude, nested/conditional — see §3)
**Loop:** Inquire-phase Pre-Q — gates whether MNQ's overnight-range→RTH-range conditioner is a certified, stage-2-validated finding or remains a disclosed-but-uncertified stage-1 result
**Artifact path:** `docs/briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md`

---

## Pre-Q gate (D-S-A, data domain — `inqhiori` §3)

```
D: Deleted candidates 1/3/5's data (daily TR self-persistence, M15 volume regime, CLV
   autocorrelation) from the active corpus — test: outside the temporal/instrument-pair scope
   of this question class (same-day cross-series magnitude conditioning of RTH range; those
   three are single-series or different-granularity claims). Deleted the NAIVE (unstratified)
   marginal comparisons from both candidate 2 and candidate 4's original Notice-log analyses —
   test: duplicated by a higher-fidelity source already in the corpus (the day-history-stratified
   reads strictly dominate the naive marginals for the same claim; candidate 4's own naive
   marginal was actively misleading, per its Notice-log §1). Did NOT delete gap magnitude
   entirely despite it turning out weaker than overnight range once jointly tested — that
   would have been a forbidden D-test ("does this fit my model") applied retroactively; the
   joint computation ran first, and only the finding it produced (conditional, sign-unstable
   increment) informed the parent/sub-question split, never the other way around.
S: Reduced the four-series raw panel (overnight range, gap magnitude, RTH range, day-history
   bias) to one joint stratified table (§1 below) — the lowest-dimension representation that
   still preserves both anomalies Noticed: overnight range's large, robust incremental lift,
   AND gap magnitude's smaller, regime-conditional increment. Discarding either collapsed
   representation would have lost one of the two Noticed anomalies.
A: Cached the merged per-day series (`candidate24_joint_frame.csv`, 1487 rows: trading_day,
   bias_overnight, bias_gap, bias_dayhist, y, on_range, gap, rth_range) so a future stage-2
   joint-surrogation design reloads in O(seconds) instead of re-deriving RTH/overnight sessions
   from 141,541 raw M15 bars.
```

---

## §0 — Rule 0 reads (production-source verification)

- `docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md` — anchor: `3c6745a` (verified `git log -1` 2026-08-29). §4 (D5) is the governing text: names this exact cross-series shape "S2," states the S1 null does not port, and specifies the three un-pause conditions this brief discharges condition (2) of.
- `ops/instruments/MNQ.md` — anchor: `6de26d5` (this session's own commit, verified `git log -1` 2026-08-29). No existing `overnight-range-transmission` DEAD/AMBIGUOUS/AUTHORIZED cell prior to this brief.
- `ops/instruments/MECHANISMS.md` — anchor: `b301e44` (verified `git log -1` 2026-08-22; `overnight-range-transmission` class added same commit as this brief per the Growth rule).
- `docs/rejected_candidates.md` — anchor: `0c305d7` (verified `git log -1` 2026-08-24). Confirmed `overnight-range-failed-extension-fade` (M2K, FALSIFIED) is an entry-role fade construct, not a conditioner — distinct class, not reopened here.
- `core/data/bar_data/SHA256SUMS` (MNQ_M15.csv entry) — anchor: `027a729` (verified `git log -1` 2026-08-14); hash `6c86f41a...fa7e00a` matches the panel this brief's analysis ran against (2026-08-29 session, unchanged).
- `lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/{data_lib,candidate2_overnight_rth_transfer,candidate4_gap_magnitude,candidate24_joint_gate}.py` — anchor: `6de26d5` (this session's own commit, verified `git log -1` 2026-08-29).
- `docs/notes/notice/N-2026-08-29-mnq-overnight-rth-range-transfer.md`, `N-2026-08-29-mnq-gap-magnitude-rth-range.md` — anchor: `6de26d5` (same commit). Both routed GRADUATE; this brief is that graduation.
- Sub-rule 8 paste-search (executed 2026-08-29, this session): `grep -ni "overnight\|gap.magnitude\|S2" lab/CATALOG.md docs/briefs/INDEX.md` and `python scripts/check_advisor_dedup.py --keywords "overnight range RTH transfer MNQ gap magnitude"` — no prior-art hit on this exact construct; nearest neighbors are `h_od_1_es_overnight_drift_2026-07` (ES overnight-hour *drift direction*, venue-walled — a different instrument and a directional not magnitude-conditioning claim) and `MNQBASE-1` (Tradeify-shaped base-construct harvest, closed dry — unrelated construct family).

---

## §1 — Context & motivation

The 2026-08-29 MNQ Notice-phase 5-candidate screen found two candidates (overnight-range and gap-magnitude conditioning of same-day RTH range) misframed by the handoff as reusing candidate 1's single-series null; both are actually the frozen corrected-null-battery spec's own cross-series "S2" shape, which the spec explicitly pauses pending a stage-1 $0 falsifier. Both cleared that falsifier independently and decisively (Notice logs `N-2026-08-29-mnq-overnight-rth-range-transfer.md`, `N-2026-08-29-mnq-gap-magnitude-rth-range.md`). Candidate 4's own §3-C flagged the open question this brief's D-S-A gate discharged: are the two candidates redundant, or independently informative? The joint gate run this session (§1 gate trace above; full numbers below) answered that decisively — they are not co-equal, and the parent/sub-question split below reflects the answer.

---

## §2 — Prior art / lineage

- [`N-2026-08-29-mnq-overnight-rth-range-transfer.md`](../notes/notice/N-2026-08-29-mnq-overnight-rth-range-transfer.md) — parent Notice, `GRADUATE`.
- [`N-2026-08-29-mnq-gap-magnitude-rth-range.md`](../notes/notice/N-2026-08-29-mnq-gap-magnitude-rth-range.md) — parent Notice, `GRADUATE`, flagged the joint-test scoping question this brief answers.
- [`docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md`](../spec/2026-08-18-magnitude-persistence-corrected-null-battery.md) §4 (D5) — governing spec; this brief's Phase 1 (§7) is the design work D5's own O1 item names `UNRESOLVED-NEEDS-DESIGN`.
- `lab/analysis/_inbox/rangestate_gc_2026-08/`, `rangestate_mcl_2026-08/`, `rangestate_corrected_2026-08/` — the S1 single-series precedent this construct explicitly does NOT reuse (see §0).
- [`ops/instruments/MECHANISMS.md`](../../ops/instruments/MECHANISMS.md) `daily-range-state-persistence` — sibling single-series class; shares ARCH/GARCH-canon grounding, distinct data-generating shape.
- `docs/briefs/closures/MNQBASE-1-closure-intake-dry.md` — unrelated construct family (Tradeify-shaped base-construct harvest), surfaced by the dedup search, ruled not an owner for this question.
- Empty lineage beyond the above is genuine: no prior Q-brief, ADR, or closure in this repo has tested overnight-range or gap-magnitude as a same-day RTH-range conditioner on any instrument.

---

## §3 — Question (Q-RANGEXFER-1 / Q-RANGEXFER-1.a)

**Q-RANGEXFER-1:** Does MNQ's Globex overnight-session realized range carry same-day predictive information for RTH-session realized range beyond what a null preserving the two series' shared same-day volatility-regime structure would produce?

**Q-RANGEXFER-1.a** (forked sub-question, nested inside the parent — per the parent-Q convention, Known Trap #11, since the joint gate found these tightly coupled rather than independent): *within the sub-regime where overnight range is itself unremarkable* (below its own trailing P80), does unsigned RTH-open gap magnitude carry same-day predictive information for RTH range beyond the same class of null?

Both are symptom-shaped (what is true about the data), not solution-shaped (what to build).

---

## §4 — Falsifiable hypothesis (H-RANGEXFER-1 / H-RANGEXFER-1.a)

**H-RANGEXFER-1:** If overnight-session range's incremental lift over matched day-history conditioning (already measured: +57.7pp / +38.7pp across day-history strata, block-bootstrap p<0.00025, n=1487) survives a joint-surrogation null that preserves the overnight-range/RTH-range same-day cross-dependence (rather than deleting it via independent per-series surrogation), then overnight range is a certified conditioner; otherwise the incremental lift is an artifact of the shared same-day regime and does not survive correction.

**Reject H-RANGEXFER-1 if:** the joint-surrogation battery's presence limbs (n-floor / CI-lower-bound / halves-stability analogues to the frozen corrected battery's L1–L3) fail, OR the by-year floor (L4 analogue) cannot resolve given this panel's ~6 usable calendar years (same structural risk that VOIDed candidate 1's L4 — disclosed here as a known risk, not assumed away), OR the attribution limb (L5 analogue) hits a diagnostic-gate FAIL that the escalation ladder (iter=500 → end-matching trim) cannot clear.
**Accept H-RANGEXFER-1 if:** all presence limbs pass AND the joint-surrogation attribution limb clears at p_upper ≤ 0.05.
**Ambiguous-hold if:** presence limbs pass but the by-year floor is structurally unresolvable (N_valid < 7 given panel length) — the same AMBIGUOUS shape candidate 1 hit, re-test window tied to a longer panel becoming available, not a calendar date.

**H-RANGEXFER-1.a:** If, restricted to the overnight-calm stratum, gap magnitude's incremental lift over day-history (already measured: +10.5pp, block-bootstrap p=0.0078, n=175/973 within that stratum) survives the same joint-surrogation discipline applied to the (gap, RTH-range) pair, then gap magnitude is a certified conditioner *in that stratum only*; otherwise it is a stratum-specific artifact.

**Reject H-RANGEXFER-1.a if:** the same limb structure fails, OR the overnight-elevated-stratum's negative point estimate (−8.1pp, not significant) is found to generalize under the joint-surrogation null (which would mean gap actively hurts when overnight is hot, a materially different and more actionable finding than "adds nothing").
**Accept H-RANGEXFER-1.a if:** presence limbs pass in the overnight-calm stratum AND attribution clears at p_upper ≤ 0.05, restricted to that stratum.
**Ambiguous-hold if:** the overnight-calm stratum's n (973 scored days, 175 gap-positive) is judged underpowered once split three ways (overnight-calm × gap × day-history) at Phase 1 design time.

---

## §5 — Forbidden moves

- **Treating the stage-1 $0 falsifier's result (p<0.00025) as sufficient to call H-RANGEXFER-1 RESOLVED without running the stage-2 joint-surrogation null.** Ruled out because the stage-1 test controls for *yesterday's* regime bleeding into today (day-history) — a genuinely different confound than *today's* own shared overnight/RTH regime, which is exactly what independent-vs-joint surrogation differs on (D5 O1). Stage-1 clearing is necessary, not sufficient, per D5's own three-condition structure.
- **Retuning WINDOW=60 / Q_BIAS=0.80 if the stage-2 result comes back weaker than stage-1.** Ruled out as an outcome-conditional retune — the same forbidden move that would have rescued candidate 1's diagnostic-gate VOID by loosening the IAAFT tolerance after seeing it fail.
- **Silently dropping Q-RANGEXFER-1.a because the parent effect is larger and more robust.** Ruled out per "S preserves N" — the overnight-calm-stratum gap increment (p=0.0078, both the two-way and three-way checks agree) is a real, disclosed anomaly and must be tested on its own falsifiable terms, not quietly folded into or abandoned alongside the parent.
- **Building any entry/sizing construct on either conditioner before this brief resolves AND before a separate raised-bar Route argument is made.** Both parent Notices already flagged conditioner-role framing as not needing the raised bar (`index-intraday-ohlcv-directional-timing-2026-07-21`) to clear itself — that exemption does not extend to a future entry construct built on top of it, which would need its own Route 1/2/3 argument at that time.
- **Substituting the already-run day-history stage-1 result for D5 condition (3)'s "stage-2 joint-surrogation null design."** These test different confounds (day-history = yesterday's regime; joint-surrogation = today's own two-series shared regime); conflating them would silently skip the harder, unresolved half of D5's requirement.
- **Designing the Phase 1 joint-surrogation null and executing it in the same motion, without the adversarial review D5 condition (3) names.** The design proposed in §7 Phase 1 is a starting sketch, not a frozen gate — running it unreviewed would be the same "declared a test after seeing what it needs to conclude" failure the corrected-battery incident (2026-08-18 audit note) already cost this repo once.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | Both presence limbs (L1–L4 analogues) pass AND attribution limb (L5 analogue) clears p_upper ≤ 0.05, for H-RANGEXFER-1 (parent). H-RANGEXFER-1.a scored independently under the same structure, restricted to the overnight-calm stratum. | `INTEGRATE — promote overnight-range-transmission to a live conditioner-role class finding in MECHANISMS.md at CERTIFIED status (still conditioner-only; no entry construct authorized by this alone); if H-RANGEXFER-1.a also RESOLVED, note the stratum restriction verbatim wherever quoted.` |
| `FALSIFIED` | Any presence limb fails outright (not merely AMBIGUOUS on L4), OR the attribution limb VOIDs after the full escalation ladder (iter=500 → end-matching trim), for the relevant hypothesis. | `STOP — re-proposal bar: a genuinely different joint-surrogation design (not a retuned tolerance on this one) or a longer panel, per whichever limb drove the FALSIFIED verdict.` |
| `AMBIGUOUS-HOLD` | Presence limbs pass but the by-year floor (L4 analogue) cannot resolve given panel length (N_valid < 7), matching candidate 1's own structural wall on this same 6-year MNQ panel. | `ITERATE — return target: re-score when the MNQ panel extends to ≥7 full calendar years, or a fresh surrogate-class design (ARFIMA/GARCH-fitted, the frozen spec's own O5 remedy) is adopted for the by-year-independent limbs; no re-test date, panel-length-triggered.` |

---

## §7 — Execution plan

- **Phase 0 — Rule-0 reads.** Complete (§0 above).
- **Phase 1 — Design the joint-surrogation null (discharges D5's O1 `UNRESOLVED-NEEDS-DESIGN` item).** NOT run this session; requires operator GO before design work proceeds, per D5 condition (3)'s explicit sequencing (design → adversarial review → operator GO → execute). Candidate sketch, offered as a starting point only, not a frozen design: model each day's shared regime as a common latent factor (e.g., a trailing joint EWMA of both overnight and RTH range), generate paired surrogates that preserve (a) each series' own linear ACF (as the existing IAAFT battery already does per-series) and (b) the lag-0 same-day cross-correlation attributable to that shared factor, while randomizing any residual cross-dependence beyond it. This is a coupled/joint IAAFT variant, not the existing per-series routine — genuinely new, and exactly why D5 named it unresolved rather than assuming the S1 machinery ports.
- **Phase 2 — Adversarial review of the Phase 1 design.** A second, independent pass (a fresh session, or `pre-ratification-adversarial-panel`) checking the joint-surrogation design against the same class of failure that invalidated the original block-shuffle placebo (2026-08-18 audit note) — does this design actually control for the shared-regime confound, or does it, like the retired placebo, pass by construction regardless of whether a real effect exists?
- **Phase 3 — Operator GO, then execute.** Run the reviewed design on the cached joint frame (`candidate24_joint_frame.csv`) for both H-RANGEXFER-1 and H-RANGEXFER-1.a, producing the same disclosure set the frozen battery requires (diagnostics before any hit rate, both one-sided p's, by-year table, halves).
- **Phase 4 — Verdict assertion.** Run §6 against the actual numbers; produce the closure artifact per §9.

---

## §8 — Verdict pre-registration (mandatory before Phase 1)

Filed at [`docs/briefs/pre-registration/Q-RANGEXFER-1-verdict-preregistration.md`](pre-registration/Q-RANGEXFER-1-verdict-preregistration.md), committed in the same commit as this brief (Phase 1 has not run; no analysis-order violation).

Pre-registration commit hash: `<populated at this commit — see this brief's own commit in `git log --oneline -1 -- docs/briefs/pre-registration/Q-RANGEXFER-1-verdict-preregistration.md`>`
Pre-registration date: 2026-08-29

---

## §9 — Closure record format

Per `references/closure_record.md` when the §6 gate fires:
- **If RESOLVED:** `docs/briefs/closures/Q-RANGEXFER-1-closure-resolved.md`
- **If FALSIFIED:** `docs/briefs/closures/Q-RANGEXFER-1-closure-falsified.md`
- **If AMBIGUOUS-HOLD:** `docs/briefs/closures/Q-RANGEXFER-1-closure-ambiguous.md` with the panel-length re-test trigger named explicitly.

---

## §10 — Audit hooks (runnable)

```bash
# Reproduce the stage-1 falsifiers this brief's parent Notices rest on (deterministic, <10s each)
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate2_overnight_rth_transfer.py
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate4_gap_magnitude.py

# Reproduce this brief's own joint gate (the D-S-A Simplify step)
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate24_joint_gate.py
# Expected: gap lift +0.105 (overnight-stratum=0, p=0.008) / -0.081 (overnight-stratum=1, p=0.998);
# overnight lift +0.594 (gap-stratum=0, p<0.001) / +0.407 (gap-stratum=1, p<0.001)

# Confirm the governing D5 text and its O1 unresolved-design item
grep -n "S2 (overnight\|O1:" docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md

# Confirm the MECHANISMS.md class landed in the same commit as this brief
git log --oneline -1 -- ops/instruments/MECHANISMS.md

# Confirm §0 panel hash anchor still resolves
grep MNQ_M15 core/data/bar_data/SHA256SUMS

# If RESOLVED/FALSIFIED: re-run the gate-firing Phase 3 script (not yet authored)
# python lab/analysis/<phase3-script>.py --reproduce-q-rangexfer-1
```

---

## Verification

```bash
$ python .claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md --type inquire
# Expected: RESULT: well-formed

$ git log -1 -- docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md
# Expected: 3c6745a, 2026-08-20

$ grep -n "S2 (overnight" docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md
# Expected: the "S1 null does NOT port" clause quoted in §1/§4/§5 above

$ git log --oneline docs/briefs/pre-registration/Q-RANGEXFER-1-verdict-preregistration.md
# Expected: pre-registration commit == this brief's own commit (both filed together, before Phase 1)
```
