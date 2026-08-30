# Q-RANGEXFER-1 — Does overnight-session range transmit genuine same-day information to RTH range, beyond a shared-regime confound? (MNQ; replicated on MYM)

**Status:** `OPEN`
**Authored:** 2026-08-29
**Amended:** 2026-08-30 — scope broadened from MNQ-only to MNQ+MYM, per `N-2026-08-29-mym-overnight-gap-joint-gate.md`'s recommendation (§4: "this lands as a PR for review; the merge/no-merge call and its execution belong to that review") — this amendment IS that review, executed as a reviewed PR per that notice's own instruction rather than self-executed as a side effect. See §11 Amendment log.
**Closed:** N/A
**Authors:** Claude Code (D-S-A gate + stage-1 falsifier + joint gate on MNQ; MYM amendment + cross-instrument replication read), operator GO owed for Phase 1
**Parent question:** N/A (new investigation thread; forks its own sub-question below)
**Sub-questions opened:** Q-RANGEXFER-1.a (gap-magnitude, nested/conditional — see §3)
**Loop:** Inquire-phase Pre-Q — gates whether the overnight-range→RTH-range conditioner (MNQ; replicated MYM) is a certified, stage-2-validated finding or remains a disclosed-but-uncertified stage-1 result, on each instrument independently
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

**Amendment D-S-A (2026-08-30, MYM scope-broadening):**
```
D: Deleted nothing new — MYM's own two candidates' naive marginal-comparison results were
   already superseded by their own stratified corrections before this amendment (see each
   candidate's own Notice-log); this amendment adds no fresh Delete beyond what those
   corrections already discharged.
S: Reused MNQ's own joint-gate script verbatim (`c24_joint_gate.py` is a direct, same-seeds
   port of `candidate24_joint_gate.py` — same bootstrap parameters (`block=20, draws=4000,
   seeds 100+s/200+s`)) rather than authoring a second, differently-parameterized test that
   would make the two instruments' results incomparable. **Correction, 2026-08-30 (Codex
   review):** "not a redesign" was true of the bootstrap parameters but false of the
   null-calibrated `circular_shift_null_p` construction itself — MYM's own version diverged
   from MNQ's (rotated the full predictor series before masking, excluded the identity
   rotation) in a way that made the two instruments' null-calibrated p-values not directly
   comparable. Fixed in the same commit as this correction — see §0/§4 below and the joint-gate
   notice's own 2026-08-30 update. This is the same "reduce to the
   lowest-dimension representation that still preserves the Noticed anomaly" principle as the
   original S step, applied to cross-instrument comparability instead of cross-series
   dimensionality — the principle held, the null-construction execution did not, until corrected.
A: Cached MYM's own per-day joint frame (`c24_joint_frame.csv`, 1,304 scored days) alongside
   MNQ's, so Phase 1's stage-2 design (§7) can be built once and run against both without
   re-deriving either panel.
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
- `docs/notes/notice/N-2026-08-29-mym-overnight-rth-range-transfer.md` — anchor `19d5ee0` (2026-08-29, verified `git log -1`). MYM's own day-history-stratified stage-1 falsifier for the identical S2 shape: within `bprime=0` (n=1,010) lift +0.3178; within `bprime=1` (n=297) lift +0.2207; block-bootstrap on the minimum stratified lift mean +0.2186, 95% CI [+0.1042, +0.3216], p(lift≤0)=0.00025 — **and, per `c2_c4_stratified_results.json`'s own `min_lift_null_calibrated` field (PR #207 retrofit, re-read this session), a null-calibrated p_ge_obs=3.4×10⁻⁶ against the joint-frame cache, decisively confirming rather than merely repeating the bootstrap read.** Same design, same conclusion (INCREMENT — decisive) as MNQ's.
- `docs/notes/notice/N-2026-08-29-mym-gap-magnitude-rth-range.md` — anchor `19d5ee0` (2026-08-29), re-read this session including its 2026-08-30 Addendum. MYM's own gap-magnitude stage-1 result: within `bprime=0` lift +0.1404, within `bprime=1` lift +0.0672; block-bootstrap mean +0.0594, 95% CI [−0.0419, +0.1477], p(lift≤0)=0.1247 — AMBIGUOUS by the CI rule, weaker than the overnight-range sibling, same qualitative relationship MNQ's own gap candidate showed to its own overnight-range sibling. **The notice's own Addendum (append-only, does not change its §1-§5) discloses a null-calibrated p on the same minimum stratified lift of 0.0117** (MYM.md's own bullet independently cites 0.00860 from a different pass of the same retrofit — both clear a 0.05 bar the CI-based read does not) — **an unresolved disagreement between the CI rule (AMBIGUOUS) and the null-p rule (would read INCREMENT), explicitly left to an operator ruling by that Addendum, not silently resolved here.**
- **Asymmetry disclosed this session (2026-08-30):** MNQ's own day-history-stratified stage-1 scripts (`candidate2_overnight_rth_transfer.py`, `candidate4_gap_magnitude.py`, re-read in full) contain no bootstrap or null-calibration function at all — the "+57.7pp/+38.7pp... block-bootstrap p<0.00025" figure this brief's §2/§4 cites for MNQ's own candidate 2 is a percentile bootstrap on the observed data (same class as MYM's own pre-retrofit figure), and it has never been retrofitted with a `circular_shift_null_p` test the way MYM's own day-history pair was. This does not change either instrument's routing (Phase 1's joint-surrogation null is already, per §5, required regardless of stage-1 confidence on either instrument) but is disclosed for parity: MYM's own stage-1 evidence is, if anything, currently *more* rigorously supported than MNQ's on this specific sub-test, the opposite of what an unexamined reading of "MNQ is the certified original, MYM is the replication" would suggest.
- `docs/notes/notice/N-2026-08-29-mym-overnight-gap-joint-gate.md` — anchor `19d5ee0` (2026-08-29). MYM's own direct, same-seeds port of this brief's own joint-gate script (`c24_joint_gate.py`, ported from `candidate24_joint_gate.py` verbatim — `block=20, draws=4000, seeds 100+s/200+s`), read in full: replicates the identical nested-gap structure MNQ found (overnight range dominant and robust in both gap strata; gap adds small positive lift only when overnight is calm, no positive lift — possibly negative — when overnight is already hot), same sign and same relative ordering on every one of the four compared lifts, though 10.6%-44.8% smaller in magnitude on MYM and NOT uniformly ~20-40% smaller (the notice's own corrected comparison table). Explicitly recommends merging MYM's two ids into this brief's construct, explicitly defers the merge decision itself to PR review or the deferred pooling session, and explicitly flags the joint-gate itself as a **new, unregistered (K-uncounted) look** — its own p-values (bootstrap and null-calibrated alike) are disclosed as exploratory, not multiplicity-corrected, and this amendment does not cite them as pre-registered evidence, only as replication-shape evidence for the amendment decision itself (whether to broaden scope), consistent with how the notice names its own intended use.
- `ops/instruments/MYM.md` #M6 (anchor `beaa98c`, 2026-08-29) and its `cells:` rows for `overnight-range-day-session-transfer` / `overnight-gap-magnitude-range-conditioning` (both `AMBIGUOUS-PARKED`, dated 2026-08-29) — read to confirm no ledger cell rename is implied by this amendment (see §11).

---

## §1 — Context & motivation

The 2026-08-29 MNQ Notice-phase 5-candidate screen found two candidates (overnight-range and gap-magnitude conditioning of same-day RTH range) misframed by the handoff as reusing candidate 1's single-series null; both are actually the frozen corrected-null-battery spec's own cross-series "S2" shape, which the spec explicitly pauses pending a stage-1 $0 falsifier. Both cleared that falsifier independently and decisively (Notice logs `N-2026-08-29-mnq-overnight-rth-range-transfer.md`, `N-2026-08-29-mnq-gap-magnitude-rth-range.md`). Candidate 4's own §3-C flagged the open question this brief's D-S-A gate discharged: are the two candidates redundant, or independently informative? The joint gate run this session (§1 gate trace above; full numbers below) answered that decisively — they are not co-equal, and the parent/sub-question split below reflects the answer.

**Amendment context (2026-08-30):** MYM's own Phase 2 atheoretical harvest, authored the same day and independently (neither session could see the other's work at authoring time), found the identical S2-shaped pair under two separately-named ids (`overnight-range-day-session-transfer`, `overnight-gap-magnitude-range-conditioning`) rather than this brief's combined framing — a parallel-authoring taxonomy collision, first flagged in `ops/instruments/MECHANISMS.md`. Rather than merge on the strength of "these sound like the same thing," the same joint-gate design this brief already used on MNQ was ported verbatim to MYM (`N-2026-08-29-mym-overnight-gap-joint-gate.md`) to test whether MYM's own data actually shows the same nested structure, not merely a superficially similar name. It does: every one of the four compared lifts lands the same sign and the same relative ordering as MNQ, the sign pattern across the 2×2/three-way check matches exactly, and the gap-adds-nothing-when-overnight-is-hot shape replicates cleanly — differing only in magnitude (10.6%-44.8% smaller on MYM, not a uniform ratio) and in the Spearman correlation between the two predictors (larger on MYM, not smaller, the opposite of what a "MYM is just a noisier, weaker MNQ" story would predict). That notice's own §4 recommends the merge and explicitly declines to execute it, naming PR review as the correct venue. This amendment is that review: it broadens Q-RANGEXFER-1's scope to test the SAME question on MYM under the SAME design, rather than opening a second, parallel Q-brief that would re-litigate a question this one already asks.

---

## §2 — Prior art / lineage

- [`N-2026-08-29-mnq-overnight-rth-range-transfer.md`](../notes/notice/N-2026-08-29-mnq-overnight-rth-range-transfer.md) — parent Notice, `GRADUATE`.
- [`N-2026-08-29-mnq-gap-magnitude-rth-range.md`](../notes/notice/N-2026-08-29-mnq-gap-magnitude-rth-range.md) — parent Notice, `GRADUATE`, flagged the joint-test scoping question this brief answers.
- [`docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md`](../spec/2026-08-18-magnitude-persistence-corrected-null-battery.md) §4 (D5) — governing spec; this brief's Phase 1 (§7) is the design work D5's own O1 item names `UNRESOLVED-NEEDS-DESIGN`.
- `lab/analysis/_inbox/rangestate_gc_2026-08/`, `rangestate_mcl_2026-08/`, `rangestate_corrected_2026-08/` — the S1 single-series precedent this construct explicitly does NOT reuse (see §0).
- [`ops/instruments/MECHANISMS.md`](../../ops/instruments/MECHANISMS.md) `daily-range-state-persistence` — sibling single-series class; shares ARCH/GARCH-canon grounding, distinct data-generating shape.
- `docs/briefs/closures/MNQBASE-1-closure-intake-dry.md` — unrelated construct family (Tradeify-shaped base-construct harvest), surfaced by the dedup search, ruled not an owner for this question.
- Empty lineage beyond the above is genuine: no prior Q-brief, ADR, or closure in this repo has tested overnight-range or gap-magnitude as a same-day RTH-range conditioner on any instrument.
- [`N-2026-08-29-mym-overnight-rth-range-transfer.md`](../notes/notice/N-2026-08-29-mym-overnight-rth-range-transfer.md) / [`N-2026-08-29-mym-gap-magnitude-rth-range.md`](../notes/notice/N-2026-08-29-mym-gap-magnitude-rth-range.md) — MYM parent Notices, both GRADUATE-eligible, Pre-Q authoring deferred pending this amendment.
- [`N-2026-08-29-mym-overnight-gap-joint-gate.md`](../notes/notice/N-2026-08-29-mym-overnight-gap-joint-gate.md) — the replication evidence this amendment relies on; recommends, does not execute, the merge.
- [`ops/instruments/MECHANISMS.md`](../../ops/instruments/MECHANISMS.md) `overnight-range-day-session-transfer` / `overnight-gap-magnitude-range-conditioning` headings — carry the "Parallel-authoring taxonomy note" this amendment discharges.

---

## §3 — Question (Q-RANGEXFER-1 / Q-RANGEXFER-1.a)

**Q-RANGEXFER-1:** Does an instrument's Globex overnight-session realized range carry same-day predictive information for RTH-session realized range beyond what a null preserving the two series' shared same-day volatility-regime structure would produce? **Tested on MNQ; replicated (same design, same sign, same relative ordering, smaller magnitude) on MYM (amended 2026-08-30) — each instrument scored independently, not pooled into one statistic.**

**Q-RANGEXFER-1.a** (forked sub-question, nested inside the parent — per the parent-Q convention, Known Trap #11, since the joint gate found these tightly coupled rather than independent): *within the sub-regime where overnight range is itself unremarkable* (below its own trailing P80), does unsigned RTH-open gap magnitude carry same-day predictive information for RTH range beyond the same class of null? **Also replicated on MYM** — the calm-stratum gap effect is weaker there under either test (bootstrap p=0.037 vs MNQ's p=0.0078; corrected null-calibrated p=0.0495 vs MNQ's p=0.0087) but does not flip sign or disappear, though it now only barely clears a nominal 0.05 bar.

Both are symptom-shaped (what is true about the data), not solution-shaped (what to build). Neither is a claim about the *pooled* MNQ+MYM data — each instrument is its own panel, its own stage-1 result, and (per §6) its own stage-2 verdict; "replicated" describes the *shape* of the finding recurring across two independently-authored, independently-run instruments, not a combined sample.

---

## §4 — Falsifiable hypothesis (H-RANGEXFER-1 / H-RANGEXFER-1.a)

**H-RANGEXFER-1:** If overnight-session range's incremental lift over matched day-history conditioning (already measured: +57.7pp / +38.7pp across day-history strata, block-bootstrap p<0.00025, n=1487) survives a joint-surrogation null that preserves the overnight-range/RTH-range same-day cross-dependence (rather than deleting it via independent per-series surrogation), then overnight range is a certified conditioner; otherwise the incremental lift is an artifact of the shared same-day regime and does not survive correction.

**Reject H-RANGEXFER-1 if:** the joint-surrogation battery's presence limbs (n-floor / CI-lower-bound / halves-stability analogues to the frozen corrected battery's L1–L3) fail, OR the by-year floor (L4 analogue) cannot resolve given this panel's ~6 usable calendar years (same structural risk that VOIDed candidate 1's L4 — disclosed here as a known risk, not assumed away), OR the attribution limb (L5 analogue) hits a diagnostic-gate FAIL that the escalation ladder (iter=500 → end-matching trim) cannot clear.
**Accept H-RANGEXFER-1 if:** all presence limbs pass AND the joint-surrogation attribution limb clears at p_upper ≤ 0.05.
**Ambiguous-hold if:** presence limbs pass but the by-year floor is structurally unresolvable (N_valid < 7 given panel length) — the same AMBIGUOUS shape candidate 1 hit, re-test window tied to a longer panel becoming available, not a calendar date.

**H-RANGEXFER-1.a:** If, restricted to the overnight-calm stratum, gap magnitude's incremental lift over day-history (already measured: +10.5pp, block-bootstrap p=0.0078 / null-calibrated p=0.00871, n=175/973 within that stratum) survives the same joint-surrogation discipline applied to the (gap, RTH-range) pair, then gap magnitude is a certified conditioner *in that stratum only*; otherwise it is a stratum-specific artifact.

**Reject H-RANGEXFER-1.a if:** the same limb structure fails, OR the overnight-elevated-stratum's negative point estimate (−8.1pp, not significant) is found to generalize under the joint-surrogation null (which would mean gap actively hurts when overnight is hot, a materially different and more actionable finding than "adds nothing").
**Accept H-RANGEXFER-1.a if:** presence limbs pass in the overnight-calm stratum AND attribution clears at p_upper ≤ 0.05, restricted to that stratum.
**Ambiguous-hold if:** the overnight-calm stratum's n (973 scored days, 175 gap-positive) is judged underpowered once split three ways (overnight-calm × gap × day-history) at Phase 1 design time.

**H-RANGEXFER-1-MYM (amended 2026-08-30, same structure as H-RANGEXFER-1, scored independently):** If MYM's own overnight-range incremental lift over matched day-history conditioning (already measured: +0.3178 / +0.2207 across its own two `bprime` day-history strata, n=1,010/297; block-bootstrap on the minimum stratified lift mean +0.2186, 95% CI [+0.1042, +0.3216], p(lift≤0)=0.00025) survives the same class of joint-surrogation null applied to MYM's own overnight-range/RTH-range pair, then overnight range is a certified conditioner on MYM too; otherwise it is an artifact of MYM's own shared same-day regime. Reject/Accept/Ambiguous-hold conditions mirror H-RANGEXFER-1's verbatim, substituted for MYM's own panel and its own by-year table (MYM's panel spans 2020-07→2026-07, ~6 full years — the same structural by-year risk named for MNQ, not assumed resolved by analogy).

**H-RANGEXFER-1.a-MYM (amended 2026-08-30; estimand corrected same day per Codex review, PR #210 — see below):** If, restricted to MYM's own overnight-calm stratum, gap magnitude's incremental lift over day-history (the actual overnight-calm-restricted analogue of MNQ's own "+10.5pp... n=175/973" figure above — MYM's own joint-gate two-way statistic: **+0.0848**, bootstrap p=0.0370, **corrected** null-calibrated p=**0.0495** (n=991; corrected 2026-08-30 — see §0/§7, the same joint-gate null-construction fix that corrected §0's MNQ-vs-MYM replication claim) survives the same joint-surrogation discipline on MYM's own (gap, RTH-range) pair, then gap magnitude is a certified conditioner in that stratum on MYM too; otherwise it is a stratum-specific artifact on MYM, independent of whatever MNQ's own stage-2 result turns out to be.

**Estimand correction (2026-08-30, Codex review):** an earlier draft of this clause cited `c2_c4_stratified_rerun.py`'s own `bprime=0` figure (+0.1404, CI [−0.0419,+0.1477], null-calibrated p=0.0086 — corrected from an initially-cited 0.0117, itself a stale figure the source notice's own Addendum has since fixed) as if it were "restricted to the overnight-calm stratum." It is not — `bprime` in that script is yesterday's own day-history RTH-range state, computed over the FULL panel, not conditioned on today's overnight range at all. That figure is real and worth keeping on record (it is the day-history-stratified read from candidate 4's own original Notice; **its own CI-vs-null-p disagreement was resolved 2026-08-30 by operator ruling — INCREMENT, the null-calibrated test governs — see that notice's own Addendum**), but it answers a different question than H-RANGEXFER-1.a-MYM asks and must not be substituted for the actual overnight-calm-restricted statistic above.

Reject/Accept/Ambiguous-hold conditions mirror H-RANGEXFER-1.a's verbatim, substituted for MYM's own panel; **Phase 1's design must declare a fresh K for this specific stratum-conditional test on MYM before it runs**, since the joint-gate notice that produced MYM's own calm-stratum figure was itself an unregistered, K-uncounted look (see §0) — this brief's own Phase 1 execution is the first point at which that K gets properly declared, not retroactively borrowed from the notice. **The CI-vs-null-p disagreement on candidate 4's own day-history-level cell was ruled 2026-08-30 (operator: "go with INCREMENT, ... the null-calibrated test is the more reliable one") — that cell now reads INCREMENT, per that notice's own Addendum.** This is a separate ruling from H-RANGEXFER-1.a-MYM's own (overnight-calm-restricted) statistic above, which the ruling does not by itself settle — that statistic is still scored under this brief's own §6, independent of anything Phase 1 here goes on to find.

---

## §5 — Forbidden moves

- **Treating the stage-1 $0 falsifier's result (p<0.00025) as sufficient to call H-RANGEXFER-1 RESOLVED without running the stage-2 joint-surrogation null.** Ruled out because the stage-1 test controls for *yesterday's* regime bleeding into today (day-history) — a genuinely different confound than *today's* own shared overnight/RTH regime, which is exactly what independent-vs-joint surrogation differs on (D5 O1). Stage-1 clearing is necessary, not sufficient, per D5's own three-condition structure.
- **Retuning WINDOW=60 / Q_BIAS=0.80 if the stage-2 result comes back weaker than stage-1.** Ruled out as an outcome-conditional retune — the same forbidden move that would have rescued candidate 1's diagnostic-gate VOID by loosening the IAAFT tolerance after seeing it fail.
- **Silently dropping Q-RANGEXFER-1.a because the parent effect is larger and more robust.** Ruled out per "S preserves N" — the overnight-calm-stratum gap increment (bootstrap p=0.0078 / null-calibrated p=0.00871, both the two-way and three-way checks agree) is a real, disclosed anomaly and must be tested on its own falsifiable terms, not quietly folded into or abandoned alongside the parent.
- **Building any entry/sizing construct on either conditioner before this brief resolves AND before a separate raised-bar Route argument is made.** Both parent Notices already flagged conditioner-role framing as not needing the raised bar (`index-intraday-ohlcv-directional-timing-2026-07-21`) to clear itself — that exemption does not extend to a future entry construct built on top of it, which would need its own Route 1/2/3 argument at that time.
- **Substituting the already-run day-history stage-1 result for D5 condition (3)'s "stage-2 joint-surrogation null design."** These test different confounds (day-history = yesterday's regime; joint-surrogation = today's own two-series shared regime); conflating them would silently skip the harder, unresolved half of D5's requirement.
- **Designing the Phase 1 joint-surrogation null and executing it in the same motion, without the adversarial review D5 condition (3) names.** The design proposed in §7 Phase 1 is a starting sketch, not a frozen gate — running it unreviewed would be the same "declared a test after seeing what it needs to conclude" failure the corrected-battery incident (2026-08-18 audit note) already cost this repo once.
- **Treating MYM's smaller-magnitude replication as evidence the mechanism is weaker or less real, or averaging/pooling MNQ's and MYM's lift figures into one combined statistic.** Amended 2026-08-30: the two instruments are separate panels with separate stage-1 results and will get separate stage-2 verdicts (§6); "replicates" describes matching sign and relative ordering, not matching magnitude, and the magnitude gap itself is not yet explained (candidate mechanisms untested this session) — treating it as noise-to-be-averaged-away or as evidence of a weaker true effect are both unearned conclusions this brief does not draw.
- **Citing the MYM joint-gate's own calm-stratum p-values (bootstrap p=0.037, corrected null-calibrated p=0.0495) as if they were pre-registered, multiplicity-corrected evidence.** Amended 2026-08-30: that notice's own §4 discloses the joint gate as a sixth, unregistered look against a closed K=5 manifest — cited here only as replication-shape evidence motivating this scope amendment, never as a number that clears H-RANGEXFER-1.a-MYM's own Accept bar (which requires a freshly-K-declared Phase 1 execution, not this figure).
- **Substituting `c2_c4_stratified_rerun.py`'s day-history-only `bprime` figure for the actual overnight-calm-restricted statistic when stating H-RANGEXFER-1.a-MYM.** This was this brief's own mistake, caught 2026-08-30 (Codex review) and corrected in §4 — `bprime` conditions on yesterday's own RTH-range state over the full panel, not on today's overnight range; only the joint-gate's own two-way `gap_lifts_within_overnight_strata` figure is actually restricted to the overnight-calm stratum.
- **Renaming or deleting MYM's own `overnight-range-day-session-transfer` / `overnight-gap-magnitude-range-conditioning` PROFILE cells or Notice-log files as a side effect of this amendment.** Amended 2026-08-30: those ids and their own evidence trail stay exactly as they are — this amendment adds a shared Pre-Q on top of them, per §11, it does not retire or rewrite them.

---

## §6 — Gate criteria (closure verdict)

**Scored per instrument, independently — MNQ's verdict does not determine MYM's, and vice versa (amended 2026-08-30).** A closure covering both instruments' verdicts is filed together (§9) once both are scored, but a RESOLVED-on-one/FALSIFIED-on-the-other outcome is a legitimate, fully-disposed result, not a reason to hold either verdict open waiting for the other to match.

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | Both presence limbs (L1–L4 analogues) pass AND attribution limb (L5 analogue) clears p_upper ≤ 0.05, for H-RANGEXFER-1 (parent), scored on that instrument's own panel. H-RANGEXFER-1.a scored independently under the same structure, restricted to the overnight-calm stratum, on that same instrument's own panel. | `INTEGRATE — promote overnight-range-transmission to a live conditioner-role class finding in MECHANISMS.md at CERTIFIED status for that instrument (still conditioner-only; no entry construct authorized by this alone); if H-RANGEXFER-1.a also RESOLVED, note the stratum restriction verbatim wherever quoted. On the instrument where this fires, also fold that instrument's own legacy PROFILE cell(s) (`overnight-range-day-session-transfer` / `overnight-gap-magnitude-range-conditioning` on MYM) into the CERTIFIED cell, citing this closure — the fold happens at verdict time, not before.` |
| `FALSIFIED` | Any presence limb fails outright (not merely AMBIGUOUS on L4), OR the attribution limb VOIDs after the full escalation ladder (iter=500 → end-matching trim), for the relevant hypothesis, on that instrument's own panel. | `STOP — re-proposal bar: a genuinely different joint-surrogation design (not a retuned tolerance on this one) or a longer panel, per whichever limb drove the FALSIFIED verdict, on that instrument. Does not falsify the same hypothesis on the other instrument.` |
| `AMBIGUOUS-HOLD` | Presence limbs pass but the by-year floor (L4 analogue) cannot resolve given panel length (N_valid < 7) — MNQ's own ~6-year panel and MYM's own ~6-year panel (2020-07→2026-07) carry the identical structural wall independently. | `ITERATE — return target: re-score when that instrument's panel extends to ≥7 full calendar years, or a fresh surrogate-class design (ARFIMA/GARCH-fitted, the frozen spec's own O5 remedy) is adopted for the by-year-independent limbs; no re-test date, panel-length-triggered, per instrument.` |

---

## §7 — Execution plan

- **Phase 0 — Rule-0 reads.** Complete (§0 above).
- **Phase 1 — Design the joint-surrogation null (discharges D5's O1 `UNRESOLVED-NEEDS-DESIGN` item).** NOT run this session; requires operator GO before design work proceeds, per D5 condition (3)'s explicit sequencing (design → adversarial review → operator GO → execute). Candidate sketch, offered as a starting point only, not a frozen design: model each day's shared regime as a common latent factor (e.g., a trailing joint EWMA of both overnight and RTH range), generate paired surrogates that preserve (a) each series' own linear ACF (as the existing IAAFT battery already does per-series) and (b) the lag-0 same-day cross-correlation attributable to that shared factor, while randomizing any residual cross-dependence beyond it. This is a coupled/joint IAAFT variant, not the existing per-series routine — genuinely new, and exactly why D5 named it unresolved rather than assuming the S1 machinery ports. **Amended 2026-08-30:** the design, once reviewed, is one design run twice — once against MNQ's cached `candidate24_joint_frame.csv`, once against MYM's cached `c24_joint_frame.csv` — not two separately-designed tests. A fresh K declaration is owed before Phase 3 execution for the MYM leg specifically (per H-RANGEXFER-1.a-MYM's own note in §4), since MYM's own joint gate was an unregistered look; MNQ's Phase 1 K-accounting is unaffected and unchanged by this amendment.
- **Phase 2 — Adversarial review of the Phase 1 design.** A second, independent pass (a fresh session, or `pre-ratification-adversarial-panel`) checking the joint-surrogation design against the same class of failure that invalidated the original block-shuffle placebo (2026-08-18 audit note) — does this design actually control for the shared-regime confound, or does it, like the retired placebo, pass by construction regardless of whether a real effect exists? **Amended 2026-08-30:** this review also covers whether running the identical design on both instruments (rather than a MYM-specific variant) is itself sound, given the magnitude gap noted in §1/§5.
- **Phase 3 — Operator GO, then execute.** Run the reviewed design on the cached joint frame(s) (`candidate24_joint_frame.csv` for MNQ, `c24_joint_frame.csv` for MYM) for H-RANGEXFER-1, H-RANGEXFER-1.a, and (amended) their MYM analogues, producing the same disclosure set the frozen battery requires (diagnostics before any hit rate, both one-sided p's, by-year table, halves) — per instrument.
- **Phase 4 — Verdict assertion.** Run §6 against the actual numbers, per instrument; produce the closure artifact per §9.

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

**Amended 2026-08-30:** one closure file covers both instruments' verdicts (filed once both are scored, per §6), naming each instrument's own verdict explicitly in its own paragraph rather than a single combined verdict — a mixed outcome (e.g., RESOLVED on MNQ, AMBIGUOUS-HOLD on MYM) files under whichever filename matches the *parent* MNQ verdict, per this Q's original numbering, with the MYM verdict stated in the body, not folded into the filename.

---

## §10 — Audit hooks (runnable)

```bash
# Reproduce the stage-1 falsifiers this brief's parent Notices rest on (deterministic, <10s each)
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate2_overnight_rth_transfer.py
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate4_gap_magnitude.py

# Reproduce this brief's own joint gate (the D-S-A Simplify step)
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate24_joint_gate.py
# Expected: gap lift +0.105 (overnight-stratum=0, bootstrap p=0.0078 / null-calibrated p=0.00871)
#           / -0.081 (overnight-stratum=1, bootstrap p=0.998 / null-calibrated p=0.997);
# overnight lift +0.594 (gap-stratum=0, bootstrap p=0.00025 / null p=0.00086)
#           / +0.407 (gap-stratum=1, bootstrap p=0.00025 / null p=0.00306)
# Null-calibrated p is circular_shift_null_p; bootstrap p is block_bootstrap_p (not a Type-I test).

# Confirm the governing D5 text and its O1 unresolved-design item
grep -n "S2 (overnight\|O1:" docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md

# Confirm the MECHANISMS.md class landed in the same commit as this brief
git log --oneline -1 -- ops/instruments/MECHANISMS.md

# Confirm §0 panel hash anchor still resolves
grep MNQ_M15 core/data/bar_data/SHA256SUMS

# If RESOLVED/FALSIFIED: re-run the gate-firing Phase 3 script (not yet authored)
# python lab/analysis/<phase3-script>.py --reproduce-q-rangexfer-1

# --- Amendment 2026-08-30 (MYM scope-broadening) ---

# Reproduce MYM's own stage-1 falsifiers (deterministic, <10s each)
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_stratified_rerun.py
# Expected: overnight-range min-stratified lift mean +0.2186, CI [+0.1042,+0.3216], p=0.00025
#           gap-magnitude min-stratified lift mean +0.0594, CI [-0.0419,+0.1477], p=0.1247 (AMBIGUOUS)

# Reproduce MYM's own joint gate (the replication evidence this amendment relies on).
# Runs against the committed c24_joint_frame.csv cache when MYM_M15.csv is absent
# (public-clone environment) -- fixed 2026-08-30, previously crashed with
# FileNotFoundError in this environment (Codex review, PR #210).
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c24_joint_gate.py
# Expected (corrected 2026-08-30 null construction -- see §0/§7):
#           gap lift overnight=0 +0.0848 (corrected null-calibrated p=0.0495); overnight=1 -0.0724 (p=0.9489)
#           overnight lift gap=0 +0.3822 (p=0.00098); gap=1 +0.2250 (p=0.00352)

# Confirm no MYM PROFILE cell was renamed by this amendment (forbidden move, §5).
# Pinned to the amendment's own first commit (a4e9d95, PR #210) rather than a
# relative HEAD~1, which silently drifts to the wrong diff once later commits
# land (Codex review, PR #210) -- update this hash only if this amendment itself
# is amended again.
git diff a4e9d95^..a4e9d95 -- ops/instruments/MYM.md | grep -A2 "^-.*mechanism:\|^+.*mechanism:"
# Expected: no output, or only additions/context unrelated to the two named cells' `mechanism:` field

# Confirm MECHANISMS.md's parallel-authoring taxonomy note now points at this amendment, not "not yet executed"
grep -n "RECOMMENDS MERGE\|Q-RANGEXFER-1" ops/instruments/MECHANISMS.md
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

---

## §11 — Amendment log

| Date | Change | By |
|---|---|---|
| 2026-08-29 | Initial authoring — MNQ-only scope, D-S-A gate + stage-1 falsifiers + joint gate run, Phase 1 awaiting operator GO | Claude Code |
| 2026-08-30 | Scope broadened to cover MYM's replicated finding (`N-2026-08-29-mym-overnight-gap-joint-gate.md` §4's own recommendation, executed as the PR review that notice named as the correct venue — not self-executed). Title, Status header, §0, §1, §3, §4 (new H-RANGEXFER-1-MYM / H-RANGEXFER-1.a-MYM), §5, §6 (per-instrument scoring), §7, §9, §10 updated. No MYM PROFILE cell, Notice-log file, or MECHANISMS.md heading structure was renamed or deleted — this amendment adds a shared Pre-Q on top of MYM's existing evidence trail, per §5's forbidden-moves addition. Phase 1 (joint-surrogation null design) remains un-run for both instruments, still gated on operator GO + adversarial review; this amendment changes scope, not gating. | Claude Code, per the notice's own instruction to route the merge decision through review |
| 2026-08-30 | Second pass, same day, on merging this branch against `origin/main`: found the base branch had moved since the first pass (PR #207's Codex-reviewed retrofit) and re-read both MYM notices' current state rather than assuming the earlier read still held. Added: MYM candidate 2's own null-calibrated confirmation (p_ge_obs=3.4×10⁻⁶, strengthening H-RANGEXFER-1-MYM, no routing change); the disclosed CI-vs-null-p disagreement on gap-magnitude (bootstrap AMBIGUOUS vs. null-calibrated p=0.0117, per that notice's own Addendum) into H-RANGEXFER-1.a-MYM and §5, explicitly left as the operator ruling that Addendum itself named, not resolved here; and a disclosed asymmetry — MNQ's own day-history-stratified stage-1 scripts (candidate 2/4) were never retrofitted with a null-calibrated test at all, unlike MYM's, so MYM's own stage-1 evidence is currently *more* rigorously supported on this specific sub-test than MNQ's "original" finding. No verdict or routing changed; Phase 1 remains un-run and un-gated by any of this. | Claude Code, triggered by a merge conflict surfacing the upstream correction rather than by a fresh read initiated proactively |
| 2026-08-30 | Third pass, same day, responding to Codex's PR #210 review (6 findings on this brief, verified against the actual scripts before fixing): (1) MYM's own `circular_shift_null_p` in `c24_joint_gate.py` was a genuinely different, less rigorous construction than MNQ's Codex-fixed version (rotated the full predictor series before masking to the stratum, excluded the identity rotation) — ported MNQ's exact construction into the MYM script and re-ran it against the committed `c24_joint_frame.csv` cache (no vendor bars needed); the calm-stratum gap null-p moved from the previously-reported 0.0198/0.020 to a corrected **0.0495**, materially weaker (barely clears 0.05, and now *less* decisive than MNQ's own p=0.0087, the opposite of what was previously claimed) — every other cell's conclusion is unchanged. (2) The same script had no vendor-first/cache-fallback loading, so its own audit hook crashed with `FileNotFoundError` in this public-clone environment — fixed by porting MNQ's `load_cached_frame()` pattern; confirmed by actually running it here. (3) H-RANGEXFER-1.a-MYM conflated `c2_c4_stratified_rerun.py`'s day-history-only `bprime=0` figure (full panel, not overnight-conditioned) with the actual overnight-calm-restricted statistic — corrected to use the joint-gate's own two-way figure as the "already measured" evidence, with the `bprime` figure kept as separate, clearly-labeled context. (4) The pre-registration's own ex-ante power prediction claimed MYM's overnight-calm subpanel (n=991) was smaller than MNQ's (n=973) — reversed; 991 > 973 — corrected to base the prediction on the effect's own marginality, not a (nonexistent) size deficit. (5) The audit-hook diff command used a relative `HEAD~1`, which silently inspects the wrong commit once later commits land — pinned to this amendment's own first commit hash. All corrections are disclosure/methodology fixes; no H-RANGEXFER-1/-1.a/-1-MYM/-1.a-MYM verdict changed, Phase 1 remains un-run and un-gated. | Claude Code, responding to Codex's PR #210 review, each finding independently re-verified against the underlying scripts before any fix |
| 2026-08-30 | Operator ruled on candidate 4's day-history-level CI-vs-null-p disagreement (named in `N-2026-08-29-mym-gap-magnitude-rth-range.md`'s own Addendum): the null-calibrated test governs, that cell now reads INCREMENT rather than AMBIGUOUS. §4 (H-RANGEXFER-1.a-MYM's own estimand-correction note) and §5 updated to cite the ruling instead of leaving it open. Also corrected a stale figure while updating this: the notice's own second Addendum previously cited null-calibrated p=0.0117 for this cell; the authoritative `c2_c4_stratified_results.json` reads p=0.0086 (both clear 0.05; only the exact margin changes). This ruling settles the day-history-level cell only — it does not by itself resolve H-RANGEXFER-1.a-MYM's own overnight-calm-restricted statistic, which remains scored under §6. | Joshua ("I will go with INCREMENT, it seems the null-calibrated test is the more reliable one") |
