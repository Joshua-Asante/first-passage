# Q-VOLREGIME-1 — Does an M15 bar's own volume regime carry same-bar-lag predictive information for the next bar's realized range, beyond the trigger bar's own range state? (MNQ; replicated on MYM)

**Status:** `OPEN`
**Authored:** 2026-08-30
**Closed:** N/A
**Authors:** Claude Code (D-S-A gate + joint MNQ+MYM authoring, per the operator's own batch framing naming a pooling session before either instrument's Pre-Q opens)
**Parent question:** N/A (new investigation thread)
**Sub-questions opened:** none — per `MECHANISMS.md`'s own note, this construct "carries no unresolved nested-hypothesis structure blocking a straightforward merge," unlike the sibling `overnight-range-transmission` / gap-magnitude pair (`Q-RANGEXFER-1`)
**Loop:** Inquire-phase Pre-Q — gates whether the bar-volume→next-bar-range conditioner (MNQ; replicated MYM) is a certified, stage-2-validated finding or remains a disclosed-but-uncertified stage-1 result, on each instrument independently
**Artifact path:** `docs/briefs/Q-VOLREGIME-1-intraday-bar-volume-regime.md`

---

## Pre-Q gate (D-S-A, data domain — `inqhiori` §3)

```
D: Deleted the direction limb from both instruments' active corpus for this Q — MNQ's own
   direction test was a clean null (ToD-matched lift +0.01pp, n≈134,678) and MYM's own batch
   scoped direction out entirely (matching MNQ's clean-null result rather than re-testing it).
   Test: a null result is not a symptom to carry into a falsifiable-H Pre-Q; nothing to gate.
   Deleted the NAIVE (unstratified) marginal comparison from both instruments' original
   Notice-log analyses — test: duplicated by a higher-fidelity source already in the corpus
   (the ToD-matched/stratified reads strictly dominate the naive marginals for the same claim;
   MYM's own naive marginal was actively misleading, read NO-INCREMENT when the stratified
   truth is a decisive +16-25pp INCREMENT — see each Notice-log's own §1).
D: Did NOT delete the "same WHO as daily-range-state-persistence, just finer grain" mechanism
   question either notice's own §3 raised, despite it not being resolved by the stratification
   — deleting an unresolved mechanism-attribution question because the statistical result is
   already decisive would be a forbidden D-test (declaring the question closed because the
   easier half of it is closed); it is carried into §4/§7 below as a named design requirement
   for Phase 1, not resolved here.
S: Reduced two instruments' four-quantity raw evidence (naive lift, ToD-matched lift, own-range
   Spearman correlation, incremental-stratified lift) to the one number that actually answers
   "is this informative beyond range's own persistence": the stratified incremental lift. This
   is the lowest-dimension representation that still preserves the one anomaly both sessions
   Noticed (volume adds information beyond contemporaneous range) without carrying forward the
   naive marginal's now-superseded, actively-misleading reading.
A: Both instruments' underlying stratified computations are already cached and committed
   (`candidate3_results.json` / MNQ's own JSON for the naive/ToD-matched split;
   `c3_stratified_results.json` for MYM's authoritative stratified result) — Phase 1's stage-2
   design (§7) reloads these rather than re-deriving from 141k+ raw M15 bars per instrument.
   Accelerated further by reusing `Q-RANGEXFER-1`'s own Phase 1 joint-surrogation design
   *class* (§7 below) rather than authoring a third null design from scratch — this construct
   shares the identical shared-regime confound shape, just at 1-bar instead of same-session lag.
```

---

## §0 — Rule 0 reads (production-source verification)

- `docs/notes/notice/N-2026-08-29-mnq-bar-volume-regime.md` — anchor `6de26d5` (2026-08-29, verified `git log -1`). Read in full: direction limb clean null; range limb ToD-matched lift +18.1pp, CI [0.673, 0.695], n_cond=70,545/n_scored=136,020; incremental-over-own-range stratification +20.6pp (low-range, n=12,430/54,167) / +25.6pp (high-range, n=58,115/11,308); same-bar Spearman(volume,range)=0.88. Routed GRADUATE (range) / DROP (direction).
- `docs/notes/notice/N-2026-08-29-mym-bar-volume-regime.md` — anchor `19d5ee0` (2026-08-29, verified `git log -1`). Read in full: original naive marginal (diff −0.0049, CI [−0.0085,−0.0012]) read NO-INCREMENT, superseded by the same-day stratified correction (`bias_hist=0` lift +0.1649, n=71,492; `bias_hist=1` lift +0.2455, n=68,113; block-bootstrap mean +0.1648, 95% CI [+0.1537,+0.1761], p≈0, n=139,605); Spearman(volume,range)=0.8618, n=141,467. Routed GRADUATE, Pre-Q authoring deliberately deferred to this pooling session (its own §4/§10).
- `ops/instruments/MECHANISMS.md` `intraday-bar-volume-regime` heading — anchor `beaa98c` (2026-08-29, verified `git log -1`). Confirms both instruments' class findings are already cross-referenced under one shared heading (unlike the range/gap-magnitude split), and that MNQ's own candidate is "registered here under MYM's id... no unresolved nested-hypothesis structure blocking a straightforward merge" — the taxonomy question `Q-RANGEXFER-1` needed a full amendment to resolve does not recur here.
- `ops/instruments/MECHANISMS.md` `tod-baseline-range-trigger` heading (`Q-TODVOL-1`, 2026-08-20) — same anchor. Read to confirm the deseasonalization convention both candidate-3 scripts reuse (same-time-of-day-slot trailing median as the causal reference) is an established, already-reviewed pattern, not invented for this construct — both Notice-logs' own §2 make the same claim; verified against the heading directly rather than taken on the notices' word alone.
- `docs/briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md` §7 Phase 1 (this session's own 2026-08-30 amendment) — the joint-surrogation null design sketch this Pre-Q's own Phase 1 (§7 below) adapts rather than re-derives: "model each day's shared regime as a common latent factor... generate paired surrogates that preserve (a) each series' own linear ACF and (b) the lag-0 (here: lag-1) cross-correlation attributable to that shared factor." Confirmed by re-reading, not assumed by memory of authoring it earlier this session.
- `lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/{candidate3_volume_regime.py,candidate3_results.json}` — anchor `6de26d5`. `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/{c3_volume_regime.py,c3_results.json,c3_stratified_rerun.py,c3_stratified_results.json}` — anchor `bb97c9d` (2026-08-30, upstream `main`, pulled via `git fetch`/merge into this branch — this session's own local clone lacks vendor bar data, so this read is of the already-committed script/JSON text, not a re-execution). Both read to confirm the cached JSON figures cited above match the notices' own quoted numbers exactly (spot-checked, not re-derived from raw bars in this session).
- **Load-bearing catch, this authoring session (2026-08-30):** `git log --oneline -- lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c3_stratified_rerun.py` shows Codex's PR #207 review (`bb97c9d fix(lab): Codex #207 — within-stratum null, vendor-first cache, c3 UNRESOLVED`) retrofitted a `circular_shift_null_p` null-calibrated test into MYM's own script and, finding no vendor bars or cached scored-frame available to actually compute it, correctly downgraded MYM's own bar-volume-regime candidate from GRADUATE to **UNRESOLVED** — the observed-series `block_bootstrap_ci` figure this session's own original Notice-log cited is disclosed, in that same review, as "the same non-null statistic this retrofit corrects," i.e. a percentile bootstrap on the observed data, not a Type-I-controlled test against a true zero-association null. **Re-reading `lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate3_volume_regime.py` in full (this session) finds it defines only `block_bootstrap_ci` — no `circular_shift_null_p` or any null-calibrated function exists in that script either.** MNQ's own stage-1 figure rests on the identical class of statistic PR #207 just flagged as insufficient on MYM's side; it has not yet been reviewed for the same defect only because this specific batch's adversarial-review pass happened to scan the MYM-side scripts (candidate 24's joint gate, c2/c4, c3) and not MNQ's own candidate 3. This Pre-Q does not silently inherit that asymmetry — see §4/§7 for the corrected, symmetric treatment.
- **Second, distinct code bug found in MNQ's own script (2026-08-30, Codex review, PR #210) — an indexing error, not a missing null-calibration.** `candidate3_volume_regime.py`'s `outcome_range_tod` compared the *next* bar's realized range against the *trigger* bar's own time-of-day-conditioned threshold (`rng_thresh_tod[:-1]`) rather than the next bar's own slot's threshold (`rng_thresh_tod[1:]`) — since consecutive M15 bars are almost always in different ToD slots with very different typical range levels, this silently reintroduces the exact deterministic seasonality confound the ToD-matched design exists to remove. Fixed in the same commit as this correction; **not re-run** in this environment (no `MNQ_M15.csv`). This means MNQ's own headline range-lift figures (+18.1pp marginal, +20.6pp/+25.6pp incremental-over-own-range) are disclosed as UNVERIFIED pending a fresh run — a stronger caveat than the null-calibration asymmetry above, which affects significance testing on an otherwise-correctly-labeled outcome; this bug means the outcome variable itself may have been mislabeled. See `N-2026-08-29-mnq-bar-volume-regime.md`'s own correction note.
- `discovery_manifests/mnq_dailygeom_notice_20260829.json` (`--lane blind`, K=5, closed) and MYM's own 2026-08-29 batch manifest (`ops/instruments/MYM.md`'s own K-bank section, "MYM family K bank = 1 → 6 as of 2026-08-29") — both candidate-3 results are members of already-closed, already-K-declared manifests; this Pre-Q's own authoring and Phase 1 *design* work spends no new K (mirrors `Q-RANGEXFER-1`'s own $0/K=0 posture at this stage — see §7 for what does need a fresh declaration).
- Sub-rule 8 paste-search (executed 2026-08-30, this session): `grep -rn "N-2026-08-29-mnq-bar-volume-regime\|N-2026-08-29-mym-bar-volume-regime" docs/briefs/Q-*.md` (no output before this file — confirmed no prior Pre-Q referenced either notice) and `python scripts/check_advisor_dedup.py --keywords "bar volume regime range conditioning M15"` (no prior-art hit on this exact construct; nearest neighbor is `tod-baseline-range-trigger`, an entry-role D2-FAILED construct that reuses the same deseasonalization convention but tests a structurally different claim — real-time volatility-threshold entry timing, not a magnitude-only bar-to-bar conditioner).

**Amendment-first search (sub-rule 10), executed output:**
```
$ grep -rln "intraday-bar-volume-regime\|bar-volume-regime" docs/adr/ docs/briefs/
ops/instruments/MECHANISMS.md  (not docs/adr or docs/briefs — confirmed no existing owner)
$ grep -n "N-2026-08-29-mnq-bar-volume-regime\|N-2026-08-29-mym-bar-volume-regime" docs/briefs/Q-*.md
(no output — no existing Pre-Q)
```
No existing owner. New Pre-Q is correct per amendment-first.

---

## §1 — Context & motivation

Both MNQ's and MYM's 2026-08-29 Notice-phase batches independently found the same construct: an M15 bar's own volume, expressed relative to its own time-of-day slot's trailing median (removing the deterministic intraday U-shape seasonality that would otherwise confound a naive pooled comparison), predicts the *next* bar's realized range being elevated — incrementally, beyond what the trigger bar's own already-elevated range already tells you. Both instruments' first-pass analyses used a **naive marginal comparison** that, on MYM, actively read the wrong sign (a −0.49pp "clean NO-INCREMENT" that a same-day stratified re-run reversed into a decisive +16 to +25pp INCREMENT once same-bar volume/range correlation, ρ≈0.86-0.88 on both instruments, was properly accounted for). MNQ's own candidate ran the correct stratified design from the start and found a near-identical shape (+20.6pp/+25.6pp).

Unlike the sibling `overnight-range-transmission` construct (`Q-RANGEXFER-1`), this one was **not** independently split into two differently-named ids across the two instruments — both sessions registered it under the same `intraday-bar-volume-regime` heading in `MECHANISMS.md` from the start, so no taxonomy-merge review is owed here. What both notices' own §3/§4 flag as genuinely unresolved, and what this Pre-Q exists to gate, is narrower and more specific: is this a **distinct mechanism** from `daily-range-state-persistence` (the same repo's own single-series, next-*day* range-persistence class), or is it **the same underlying volatility/activity-clustering regime observed at finer (bar) grain via a different proxy** — in which case "volume regime" would not be adding a genuinely new WHO, just relabeling an already-scored phenomenon at higher frequency. The stratification against own-range already rules out the *weakest* version of that concern (volume adds incremental information beyond contemporaneous range, on both instruments) — it does not by itself rule out the *stronger* version (volume and range at the *daily* time-scale might still be the single latent driver of both this construct and `daily-range-state-persistence`, making them two measurements of one thing rather than two things).

**A second, statistically prior gap this Pre-Q's authoring surfaced (2026-08-30), not present in either instrument's own Notice-log at authoring time:** neither instrument's own stratified incremental-lift figure has an actual null-calibrated significance test behind it. MYM's own leg was caught and corrected by PR #207 (Codex review) — the observed-series `block_bootstrap_ci` figure was found to be a percentile bootstrap on the data itself, not a Type-I-controlled test against a true zero-association null, and MYM's own routing was downgraded GRADUATE → **UNRESOLVED** pending that null (blocked in turn on vendor bars / a cached scored frame, neither available in the session that ran the retrofit). Re-reading MNQ's own script this session finds the identical gap — no null-calibrated function exists there either, only the same class of observed-series bootstrap. Nobody has yet reviewed MNQ's own leg for this defect; that is an omission in the adversarial-review coverage, not evidence MNQ's own figure is more solid than MYM's. **This Pre-Q treats both instruments symmetrically: neither H below is granted a "certified stage-1" framing until this within-stratum null is actually computed on that instrument's own panel** (§4, §7) — the word "decisive" that both original Notice-logs used for their own stratified lift describes the *magnitude and CI width* of an observed-series statistic, not a claim this brief re-asserts as statistically sufficient.

---

## §2 — Prior art / lineage

- [`N-2026-08-29-mnq-bar-volume-regime.md`](../notes/notice/N-2026-08-29-mnq-bar-volume-regime.md) — MNQ parent Notice, `GRADUATE` (range) / `DROP` (direction).
- [`N-2026-08-29-mym-bar-volume-regime.md`](../notes/notice/N-2026-08-29-mym-bar-volume-regime.md) — MYM parent Notice, `GRADUATE`, Pre-Q authoring deliberately deferred to this pooling session.
- [`ops/instruments/MECHANISMS.md`](../../ops/instruments/MECHANISMS.md) `intraday-bar-volume-regime` heading — both class findings, already jointly registered.
- [`ops/instruments/MECHANISMS.md`](../../ops/instruments/MECHANISMS.md) `daily-range-state-persistence` heading — the sibling single-series, next-day class this Pre-Q's own distinct-WHO question is scoped against.
- [`ops/instruments/MECHANISMS.md`](../../ops/instruments/MECHANISMS.md) `tod-baseline-range-trigger` heading (`Q-TODVOL-1`) — source of the reused deseasonalization convention; a structurally different (entry-role, D2-FAILED) construct, not reopened here.
- [`docs/briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md`](Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md) — sibling Pre-Q sharing the same shared-regime-confound problem shape (cross-series, one lag apart) and the joint-surrogation null design class this brief's own Phase 1 adapts.
- Empty lineage beyond the above is genuine: no prior Q-brief, ADR, or closure in this repo has tested plain-OHLCV bar-volume regime as a next-bar range conditioner on any instrument.

---

## §3 — Question (Q-VOLREGIME-1)

**Q-VOLREGIME-1:** Does an M15 bar's own volume, above its own time-of-day-conditioned trailing median, carry predictive information for the *next* bar's realized range being elevated (vs. its own time-of-day-conditioned trailing median), beyond what a null preserving the two series' shared same-bar volatility-regime structure would produce? **Run on MNQ and MYM, same design, same sign, comparable magnitude on the observed-series statistic — each instrument scored independently, not pooled into one statistic. §4's within-stratum precondition is now CLEARED on both instruments (2026-08-30, corrected 2026-08-30 in a Codex review pass — see that §'s own update); what remains open is Phase 1's own joint-surrogation attribution limb, not this precondition.**

Symptom-shaped (what is true about the data), not solution-shaped (what to build). This Pre-Q does not ask whether volume regime is the *same* mechanism as `daily-range-state-persistence` — that mechanism-attribution question is a named design requirement for Phase 1 (§7), not a separate falsifiable hypothesis with its own gate, since it is a question about *interpretation* of a result whose own statistical sufficiency (§4's precondition, now cleared) has been established, not about whether an already-certified full verdict survives correction.

---

## §4 — Falsifiable hypothesis (H-VOLREGIME-MNQ / H-VOLREGIME-MYM)

**Precondition common to both H below (added 2026-08-30 — see §1's second gap; CLEARED same day on both instruments — see the update below).** ~~neither hypothesis may be scored RESOLVED/FALSIFIED/AMBIGUOUS-HOLD (§6) until that instrument's own within-stratum `circular_shift_null_p`...~~ This is a $0, cheap, vendor-bar-dependent precondition (Phase 0.5, §7), materially cheaper than Phase 1's own cross-series joint-surrogation design, and logically prior to it: there is no point running a joint-surrogation null on top of a within-stratum statistic that has not itself cleared its own Type-I bar.

**Precondition CLEARED, both instruments (2026-08-30, live vendor bars present this session — see §7 Phase 0.5).** MNQ: `candidate3_stratified_rerun.py`, per-stratum circular-shift null-calibrated p = **0.00025** (own-range-not-elevated stratum) and **0.00025** (own-range-elevated stratum); re-verified marginal ToD-matched range lift also holds post-fix (+19.1pp, was unverified +18.1pp). MYM: `c3_stratified_rerun.py`, per-stratum p = **0.00025** and **0.00025**. Both instruments' precondition decisively clears alpha on both strata — routes past `PRECONDITION-CLEARED-NULL` (§6) straight to the presence-limb/attribution-limb evaluation (Phase 1 onward) for both legs.

**H-VOLREGIME-MNQ:** If the trigger bar's volume-regime incremental lift over matched own-range conditioning (observed-series figure, re-verified 2026-08-30 against live bars: **+22.3pp** low-range stratum / **+27.4pp** high-range stratum, n=67,417/68,603 — precondition now CLEARED, both strata p=0.00025) survives, first, that within-stratum null (**cleared**) and, second, a joint-surrogation null that preserves the volume/range same-bar cross-dependence (rather than deleting it via independent per-series surrogation), then bar-volume regime is a certified conditioner; otherwise the incremental lift is an artifact of the shared same-bar regime (or of the uncorrected bootstrap itself) and does not survive correction.

**Reject H-VOLREGIME-MNQ if:** the precondition's own within-stratum null fails to clear (mirroring how MYM's own leg would have been routed DEAD/AMBIGUOUS had its own within-stratum null come back non-significant, per PR #207's own disposition logic), OR — once that clears — the joint-surrogation battery's presence limbs (n-floor / CI-lower-bound / halves-stability analogues) fail, OR the by-year floor cannot resolve given this panel's limited usable calendar years (the same structural risk `daily-range-state-persistence` and `Q-RANGEXFER-1` both hit on this identical MNQ panel — disclosed here as a known risk, not assumed away), OR the attribution limb hits a diagnostic-gate FAIL that the escalation ladder (iter=500 → end-matching trim) cannot clear.
**Accept H-VOLREGIME-MNQ if:** the precondition clears AND all presence limbs pass AND the joint-surrogation attribution limb clears at p_upper ≤ 0.05.
**Ambiguous-hold if:** the precondition clears, presence limbs pass, but the by-year floor is structurally unresolvable (N_valid < 7 given panel length) — the same AMBIGUOUS shape `daily-range-state-persistence` and `Q-RANGEXFER-1`'s own H-RANGEXFER-1 both hit, re-test window tied to a longer panel becoming available, not a calendar date. **Also Ambiguous-hold (a distinct sub-state, disposition "PRECONDITION-UNMET" — §6) if the precondition itself cannot be cleared** (no vendor bars, no cached scored frame) — this is not the same as AMBIGUOUS-HOLD on the by-year limb and must not be conflated with it in any closure record.

**H-VOLREGIME-MYM (same structure and same precondition, MYM's own panel, scored independently):** If MYM's own volume-regime incremental lift over matched own-range conditioning (observed-series figure: +0.1649 within `bias_hist=0`, n=71,492; +0.2455 within `bias_hist=1`, n=68,113; block-bootstrap on the minimum stratified lift mean +0.1648, 95% CI [+0.1537,+0.1761], p≈0, n=139,605 — **precondition CLEARED 2026-08-30, both strata p=0.00025, per `N-2026-08-29-mym-bar-volume-regime.md`'s own revised INCREMENT status**) survives, first, the within-stratum null (**cleared** — vendor bars present this session, retry succeeded) and, second, the same class of joint-surrogation null applied to MYM's own volume/range pair, then bar-volume regime is a certified conditioner on MYM too; otherwise it is an artifact of MYM's own shared same-bar regime, independent of whatever MNQ's own stage-2 result turns out to be.

**Reject/Accept/Ambiguous-hold for H-VOLREGIME-MYM:** mirror H-VOLREGIME-MNQ's conditions verbatim, substituted for MYM's own panel (`core/data/bar_data/MYM_M15.csv`, 141,467 bars, 2020-07→2026-07) and its own by-year table (not yet computed for this construct on either instrument — a genuinely open risk on both sides, not merely on MYM's). MYM's own precondition, like MNQ's, is now CLEARED (2026-08-30) — the by-year floor (L4) remains the only unresolved presence limb on either instrument, owed to Phase 1/3, not this precondition.

**Distinct-WHO design requirement (not a separate hypothesis; binds Phase 1's design, §7):** whatever joint-surrogation design Phase 1 produces must include a three-way check — does volume's incremental lift over own-range survive *additionally* conditioning on the prior day's own realized-range state (`daily-range-state-persistence`'s own conditioning variable)? If the lift collapses once daily-TR state is also held fixed, that is evidence for the "same phenomenon, finer grain" reading (mechanism A in both notices' own §3); if it survives, that is evidence for a genuinely incremental, distinct information source (mechanism B). Neither outcome falsifies H-VOLREGIME-MNQ/MYM as stated above — this is an attribution question layered on top of an already-Accepted/Rejected verdict, analogous to how `Q-RANGEXFER-1`'s own L5 attribution limb types a RESOLVED verdict's strength without gating RESOLVED/FALSIFIED itself.

---

## §5 — Forbidden moves

- **Treating the stratified incremental-lift result (+16pp to +26pp across both instruments) as sufficient to call H-VOLREGIME-{MNQ,MYM} RESOLVED without running the stage-2 joint-surrogation null.** The stratification controls for the trigger bar's *own* range state; it does not control for the same-bar volume/range *shared regime* the joint-surrogation null is designed to preserve-and-test — these are different confounds, and clearing the first is necessary, not sufficient, exactly as `Q-RANGEXFER-1`'s own §5 rules for its analogous day-history-vs-joint-surrogation distinction.
- **Treating MNQ's own observed-series bootstrap CI as more solid than MYM's, because only MYM's has been reviewed and flagged.** Amended 2026-08-30: `candidate3_volume_regime.py` (MNQ) defines no null-calibrated function at all, the identical gap PR #207 found and fixed in MYM's own `c3_stratified_rerun.py`. The absence of a review finding is not the presence of a passing result — MNQ's own precondition (§4) is exactly as unmet as MYM's, it has simply not yet been looked at.
- **Computing MNQ's own within-stratum null with a differently-parameterized test than MYM's, or vice versa, without disclosing why.** The precondition (§4) uses the same `circular_shift_null_p` construction PR #207 already built and reviewed — reusing it, not re-deriving a third variant, unless a specific reason to diverge is found and disclosed.
- **Retuning the 20-slot ToD trailing window or the P50 threshold if the stage-2 result comes back weaker than the stratified result.** Ruled out as an outcome-conditional retune — both notices' own §3-C already flagged this exact axis as untested and any retune as a fresh K-charged look, not a free look; this Pre-Q does not create license to spend that look reactively.
- **Treating a RESOLVED verdict on the distinct-WHO design requirement (§4) as either a reason to fold this construct's ledger cell into `daily-range-state-persistence`'s, or as proof the two are unrelated.** Both are premature reads of a single three-way check's outcome — the requirement types the mechanism-attribution question, it does not license a ledger merge (which would need its own review, per the precedent `Q-RANGEXFER-1`'s own amendment just set) or a declaration of independence (which a single conditioning check cannot establish on its own).
- **Building any entry/sizing construct on this conditioner before this brief resolves AND before a separate raised-bar Route argument is made.** Both parent Notices already flagged conditioner-role framing as not needing the raised bar (`index-intraday-ohlcv-directional-timing-2026-07-21`) to clear itself — that exemption does not extend to a future entry construct built on top of it.
- **Averaging or pooling MNQ's and MYM's incremental-lift figures into one combined statistic, or treating MYM's smaller within-stratum lift magnitudes (+16.5pp/+24.5pp vs MNQ's +20.6pp/+25.6pp) as evidence of a weaker true effect.** Each instrument is its own panel with its own stage-1 and (to come) stage-2 verdict (§6); the two are close enough in magnitude that this brief takes no position on whether the residual gap is real or sampling noise — that is untested, not resolved by assertion either way.
- **Designing the Phase 1 joint-surrogation null and executing it in the same motion, without the adversarial review D5-class discipline `Q-RANGEXFER-1` names for the sibling construct.** The design proposed in §7 is a starting adaptation, not a frozen gate — running it unreviewed repeats the "declared a test after seeing what it needs to conclude" failure the 2026-08-18 corrected-battery audit note already cost this repo once.

---

## §6 — Gate criteria (closure verdict)

**Scored per instrument, independently — MNQ's verdict does not determine MYM's, and vice versa**, same convention `Q-RANGEXFER-1` established for its own bi-instrument scope. A single closure covering both instruments' verdicts is filed once both are scored (§9).

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `PRECONDITION-UNMET` (distinct from AMBIGUOUS-HOLD) | The within-stratum `circular_shift_null_p` precondition (§4) cannot be *computed at all*: no vendor bars, no cached scored frame, on that instrument. **No longer either instrument's disposition** — both MNQ and MYM cleared this precondition 2026-08-30 (§4/§7); this row is retained for any future instrument added to this construct. | `HOLD — not a verdict on H itself, a statement that H cannot yet be evaluated. Re-check trigger: vendor bars or a cached scored frame become available (a local-session, vendor-data-access task — see this Pre-Q's own delegation note, §7). Does not close the Q; does not license falling back to the observed-series CI as a substitute.` |
| `PRECONDITION-CLEARED-NULL` (added 2026-08-30, Codex review — distinct from PRECONDITION-UNMET: the precondition *was* computed, it just failed) | Phase 0.5's within-stratum `circular_shift_null_p` is computed but does not clear alpha (p > 0.05) — the construct fails at the cheap $0 gate, on that instrument's own panel, before Phase 1's expensive joint-surrogation design is ever built for it. | `STOP for that instrument — DROP its own H at the cheap gate; do not proceed to Phase 1 on it. Re-proposal bar: a different within-stratum design, not a retune of this one. Does not bear on the other instrument's own precondition or verdict.` |
| `RESOLVED` | Precondition clears (p ≤ alpha) AND presence limbs (L1–L4 analogues) pass AND attribution limb (L5 analogue) is valid (not VOID) AND clears p_upper ≤ 0.05, for the relevant instrument's H. | `INTEGRATE — promote intraday-bar-volume-regime to a live conditioner-role class finding in MECHANISMS.md at CERTIFIED status for that instrument (conditioner-only; no entry construct authorized by this alone). Record the distinct-WHO design requirement's own outcome (§4) alongside the verdict, whichever way it lands — it is disclosed, not gating.` |
| `FALSIFIED` | Precondition clears, then any presence limb fails outright (not merely AMBIGUOUS on L4), OR the attribution limb VOIDs after the full escalation ladder, OR the attribution limb is valid (not VOID) but does not clear (p_upper > 0.05) (added 2026-08-30, Codex review — an ordinary non-VOID non-significant L5 outcome previously had no frozen disposition), for that instrument's own panel. | `STOP — re-proposal bar: a genuinely different joint-surrogation design (not a retuned tolerance on this one) or a longer panel, per whichever limb drove the FALSIFIED verdict, on that instrument. Does not falsify the same hypothesis on the other instrument.` |
| `AMBIGUOUS-HOLD` | Precondition clears, presence limbs L1-L3 pass but the by-year floor (L4) cannot resolve given panel length (N_valid < 7), on that instrument's own panel. | `ITERATE — return target: re-score when that instrument's panel extends to ≥7 full calendar years, or a fresh surrogate-class design is adopted for the by-year-independent limbs; no re-test date, panel-length-triggered, per instrument.` |

---

## §7 — Execution plan

- **Phase 0 — Rule-0 reads.** Complete (§0 above).
- **Phase 0.5 — Compute the within-stratum `circular_shift_null_p` precondition (§4) on BOTH instruments (added 2026-08-30).** **COMPLETE, 2026-08-30** — a later session in the same worktree found the vendor CSVs present in the main checkout (git-worktree gitignore-sharing gap, not a genuine local/remote split) and copied `MNQ_M15.csv`/`MYM_M15.csv` in, hash-verified against the tracked `SHA256SUMS`. On MNQ: new script `candidate3_stratified_rerun.py` ports `circular_shift_null_p` (PR #207's construction, same as `candidate24_joint_gate.py`) onto `candidate3_volume_regime.py`'s own bias_hist stratification — p=0.00025 both strata. On MYM: re-ran `c3_stratified_rerun.py` unchanged — p=0.00025 both strata. Both instruments' precondition CLEARS decisively; no fresh K charged (re-running an already-declared, already-K-counted look with a corrected/completed statistic, per PR #207's own treatment).
- **Phase 1 — Adapt `Q-RANGEXFER-1`'s joint-surrogation null design to 1-bar lag (discharges the same class of D5-analogue unresolved-design gap for this construct).** **Operator GO received 2026-08-30; blocked upstream across two rounds this session, not attempted at bar-level.** `Q-RANGEXFER-1`'s own Phase 1 (the day-level design this construct was meant to adapt) has NOT yet cleared to a certifiable standard — Round 1 (three constructions) triangulated a clean negative (own-ACF fidelity vs. cross-correlation fidelity trading off against each other); Round 2 (a 4-lens GARCH/long-memory judge panel plus a gate-redesign attempt, all independently adversarially reviewed) got materially further, then Round 3 (an external Codex review pass, same day) found that further wasn't as far as Round 2 claimed: one lens (ARFIMA long-memory + Gaussian copula) had its surrogate-testing machinery's MECHANICS confirmed bug-free, but the claimed size/power VALIDATION (an 80-replicate re-run) turns out to have only tested known-true-parameter behavior — re-estimating parameters per replicate (the only way the procedure could ever run on real data) empirically inflates the null false-positive rate from 5% to 25% (a coarse/small-N check, RESULTS.md Round 3). Its MODEL-ADEQUACY check was separately, independently found too weak to trust (it also passes an already-rejected construction) — see that brief's own §7 and the full write-up at [`lab/analysis/_inbox/joint_surrogation_null_2026-08-30/RESULTS.md`](../../lab/analysis/_inbox/joint_surrogation_null_2026-08-30/RESULTS.md). Adapting a day-level design that has cleared neither model-adequacy nor estimation-aware size/power to 1-bar lag would still compound rather than discharge the gap. This construct's own bar-level density (~135,000–140,000 bars vs ~1,300–1,500 days) and its own distinct-WHO three-way check remain to be addressed once a day-level design actually clears model-adequacy, estimation-aware size/power, and its own bug-free-mechanics checks, not before.
- **Phase 2 — Adversarial review of the Phase 1 design.** **Not started — no design ready to review, on either brief.** When one exists, checks whether the 1-bar-lag adaptation actually controls for the shared same-bar regime confound (not merely inherits `Q-RANGEXFER-1`'s design by name without verifying it transfers), and whether the distinct-WHO three-way check is itself well-specified (e.g., does conditioning on daily-TR state at bar granularity introduce its own new confound?).
- **Phase 3 — K declaration, then operator GO, then execute.** Both instruments' own candidate-3 results are members of already-closed manifests (§0); Phase 1's own stage-2 execution is new compute against those same cached JSON/CSV artifacts, not new data-touching — declare K per this program's standing convention before Phase 3 begins, matching `Q-RANGEXFER-1`'s own MYM-leg precedent (see that brief's §7 amendment note) rather than assuming $0/K=0 carries through the execution step. Run on both instruments, producing the same disclosure set the frozen battery requires (diagnostics before any hit rate, both one-sided p's, by-year table, halves) plus the distinct-WHO three-way check's own result.
- **Phase 4 — Verdict assertion.** Run §6 against the actual numbers, per instrument; produce the closure artifact per §9.

---

## §8 — Verdict pre-registration (mandatory before Phase 1)

Filed at [`docs/briefs/pre-registration/Q-VOLREGIME-1-verdict-preregistration.md`](pre-registration/Q-VOLREGIME-1-verdict-preregistration.md), committed in the same commit as this brief (Phase 1 has not run; no analysis-order violation).

Pre-registration date: 2026-08-30.

---

## §9 — Closure record format

Per `references/closure_record.md` when the §6 gate fires:
- **If RESOLVED (either or both instruments):** `docs/briefs/closures/Q-VOLREGIME-1-closure-resolved.md`, naming each instrument's own verdict explicitly.
- **If FALSIFIED (both instruments):** `docs/briefs/closures/Q-VOLREGIME-1-closure-falsified.md`.
- **If AMBIGUOUS-HOLD (either or both, no RESOLVED/FALSIFIED on either):** `docs/briefs/closures/Q-VOLREGIME-1-closure-ambiguous.md` with the panel-length re-test trigger named explicitly, per instrument.

A mixed outcome (e.g., RESOLVED on MNQ, AMBIGUOUS-HOLD on MYM) files under whichever filename matches the stronger verdict (RESOLVED > FALSIFIED > AMBIGUOUS-HOLD, matching `Q-RANGEXFER-1`'s own precedent for this exact situation), with each instrument's own verdict stated in the body.

---

## §10 — Audit hooks (runnable)

```bash
# Reproduce MNQ's own stage-1 result (deterministic, <2 min). Requires MNQ_M15.csv
# (vendor bars, absent in this public-clone environment) -- a local-session task.
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate3_volume_regime.py
# Expected (PRE-2026-08-30-fix numbers, NOT confirmed against the corrected
# outcome_range_tod indexing -- see §0/§1): dir lift ~0.0001 (ToD-matched);
# range lift ~0.181 (ToD-matched), CI [0.673, 0.695];
# incremental-over-own-range +0.206 (low-range) / +0.256 (high-range).
# Re-run and update this brief + the MNQ notice with whatever the corrected code finds.

# Confirm the indexing fix landed (Codex review, PR #210)
grep -n "rng_bar\[1:\] > rng_thresh_tod\[1:\]" lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate3_volume_regime.py
# Expected: one match (was rng_thresh_tod[:-1] before the fix)

# Reproduce MYM's own stratified result, WITH the within-stratum null (precondition CLEARED 2026-08-30)
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c3_stratified_rerun.py
# Expected: min-stratified-lift bootstrap mean=0.1648, CI=[+0.1537,+0.1761], p(lift<=0)=0.0000
# per-stratum circular-shift null-calibrated p: 0.00025 / 0.00025 -- VERDICT=INCREMENT

# Reproduce MNQ's own within-stratum null (new script, precondition CLEARED 2026-08-30)
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate3_stratified_rerun.py
# Expected: strata lifts +22.3pp/+27.4pp, per-stratum circular-shift null-calibrated p: 0.00025 / 0.00025

# Confirm the superseded MYM naive marginal (disclosed, not authoritative)
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c3_volume_regime.py
# Expected: diff=-0.0049, 95% CI=[-0.0085,-0.0012], VERDICT=NO-INCREMENT (marginal, superseded)

# Confirm same-bar volume/range correlation on both instruments (not assumed by analogy)
grep -n "0.88\|Spearman" lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate3_results.json
grep -n "0.8618\|Spearman" lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c3_stratified_results.json

# Confirm the tod-baseline-range-trigger deseasonalization convention this construct reuses
grep -n "tod-baseline-range-trigger" ops/instruments/MECHANISMS.md

# Confirm this Pre-Q references both parent notices
grep -rn "Q-VOLREGIME-1" docs/notes/notice/N-2026-08-29-mnq-bar-volume-regime.md docs/notes/notice/N-2026-08-29-mym-bar-volume-regime.md
```

---

## §11 — Amendment log

| Date | Change | By |
|---|---|---|
| 2026-08-30 | Initial authoring — joint MNQ+MYM Pre-Q, D-S-A gate, symmetric Phase 0.5 precondition (null-calibration gap disclosed on both instruments) | Claude Code |
| 2026-08-30 | Same day, responding to Codex's PR #210 review: (1) froze `TOD_WINDOW=20` for MNQ in the pre-registration when MNQ's own script actually uses `TRAIL_N=60` — corrected to freeze each instrument's own constant separately (pre-registration §A/§F.1); (2) found and fixed a second, distinct code bug in `candidate3_volume_regime.py` — its ToD-matched range outcome compared the next bar's range against the *trigger* bar's own threshold instead of the next bar's own, reintroducing the seasonality confound the design exists to remove; fixed in the script, not re-run (no vendor data here), MNQ's own headline range figures disclosed as unverified (§0/§1, and `N-2026-08-29-mnq-bar-volume-regime.md`'s own correction); (3) the pre-registration's verdict map had no disposition for "precondition computed but non-significant" or "L5 valid but p_upper > alpha" — added `PRECONDITION-CLEARED-NULL` and broadened `FALSIFIED`'s trigger (pre-registration §D, mirrored in this brief's own §6). No H-VOLREGIME-MNQ/-MYM verdict changed; Phase 0.5/Phase 1 remain un-run. | Claude Code, responding to Codex's PR #210 review, each finding re-verified against the underlying scripts before any fix |
| 2026-08-30 | **Phase 0.5 executed and CLEARS, both instruments.** A later same-day session found `MNQ_M15.csv`/`MYM_M15.csv` present in the main checkout (this worktree simply hadn't received the gitignored copies a fresh git-worktree doesn't share automatically — not a genuine local/remote environment split as first assumed), copied them in, and hash-verified against the tracked `SHA256SUMS` before use. Re-ran MNQ's ToD-matched marginal (+19.1pp, confirms the post-fix figure holds and strengthens slightly, does not dissolve); authored `candidate3_stratified_rerun.py` (MNQ) porting `circular_shift_null_p` per this brief's own §7 plan — both strata p=0.00025. Re-ran MYM's `c3_stratified_rerun.py` unchanged — both strata p=0.00025. §4/§6/§7 updated; `N-2026-08-29-mnq-bar-volume-regime.md` and `N-2026-08-29-mym-bar-volume-regime.md` updated to match (MYM's own routing revised UNRESOLVED → INCREMENT). Operator GO received same day for Phase 1 design work (§7) on this brief and `Q-RANGEXFER-1` jointly. | Claude Code |
| 2026-08-30 | Phase 1 blocked upstream: `Q-RANGEXFER-1`'s own day-level joint-surrogation design (this construct's own Phase 1 was meant to adapt it to bar-level) did not clear its own positive control this session — three candidate constructions tried, all failed, two in exactly opposite ways (see that brief's §7 and `lab/analysis/_inbox/joint_surrogation_null_2026-08-30/RESULTS.md`). §7 updated to reflect Phase 1 as not-attempted-at-bar-level pending that upstream resolution, not as a separate failure of this construct's own design. Phase 0.5's own CLEARED precondition (prior entry) is unaffected. | Claude Code |
| 2026-08-30 | Round 2 upstream update: `Q-RANGEXFER-1`'s own day-level design work continued (a 4-lens GARCH/long-memory judge panel plus a gate-redesign attempt, all independently adversarially reviewed) and got materially further — validated surrogate-testing machinery, but model adequacy still not certified (RESULTS.md Round 2). Still blocked upstream for this construct's own Phase 1; §7 updated to reflect the more nuanced (not flat-negative) upstream state. No change to this brief's own hypotheses, precondition, or verdict. | Claude Code |
| 2026-08-30 | Round 3 upstream update, responding to an external (Codex) review pass on the PR carrying Round 1/2's work: `Q-RANGEXFER-1`'s own "machinery CONFIRMED SOUND" claim from the prior entry is corrected — its own positive control validated the surrogate-testing pipeline only under known-true parameters; re-estimating parameters per replicate (the only way the procedure could ever run on real data) empirically inflates the null false-positive rate from 5% to 25% (RESULTS.md Round 3). Also fixed on this Q's own surface: MNQ's `candidate3_stratified_rerun.py`/`candidate3_volume_regime.py` had a NaN-handling bug silently scoring a missing next-bar threshold as "not elevated" instead of excluding it (fixed; figures shifted negligibly, INCREMENT/GRADUATE unchanged); a stale restatement of the pre-clearing precondition status in this brief's own §3, in `N-2026-08-29-mym-bar-volume-regime.md`'s Pre-Q line, and in `ops/instruments/MYM.md`'s entire volume-regime bullet (the last of which had never been touched by the original precondition-clearing edit) — all three corrected to match the already-current ledger cell. §7 updated to reflect Phase 1 as further from resolved than the prior entry stated, not closer. No change to this brief's own hypotheses or precondition (still CLEARED, unaffected by any of the above). | Claude Code, responding to Codex's PR #219 review |
| 2026-08-30 | Round 4 upstream update (the ratified bounded round, executed same day, then corrected same day): `Q-RANGEXFER-1`'s own day-level Phase 1 ran the operator-ratified bounded round — 2 candidate model-adequacy remedies (an out-of-sample forecast evaluation, a near-miss; a formal information-criterion/Whittle-likelihood comparison) plus a mandatory production-grade size/power re-certification. The round's own first pass overstated its results; a same-day Codex review (PR #225, 8 findings) found a truncation-mismatch bug in the size/power check (corrected null rate 24%, not the originally-reported 10%) and an under-specified IC-comparison criterion (relative BIC-best alone cannot establish absolute adequacy; adding the required absolute residual-whiteness check fails `on_range`). **Corrected disposition: neither model adequacy nor estimation-aware size/power clears** (not "model adequacy clears" as first reported). Per the ratified mandate both gates must clear together for Phase 1 to count as resolved — they did not, and the hard stop fires: `Q-RANGEXFER-1`'s own §6 gate table has a disclosed gap for this outcome, raised to the operator for a fresh gate amendment. **This construct's own Phase 1 remains exactly as blocked as the prior entry left it** — per that same prior entry and this brief's own §7, this construct's bar-level design "has never been attempted" and does not inherit any upstream outcome automatically; a day-level design clearing neither required gate does not change that. No change to this brief's own hypotheses, precondition, or verdict. A second same-day Codex review round (3 more findings, load-bearing one: the residual check's degrees of freedom were wrong, corrected) found the IC-comparison remedy actually fails BOTH channels, not `on_range` alone — the disposition (neither gate clears) is unchanged, just confirmed more decisively. Full account: `Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md` §11 and `lab/analysis/_inbox/joint_surrogation_null_2026-08-30/RESULTS.md` "Round 4 correction" / "Round 4, second correction pass." | Claude Code, executing the operator-ratified `Q-RANGEXFER-1` bounded-round mandate (this brief itself untouched in scope) |
| 2026-08-30 | Upstream closure-path proposal filed (PROPOSED) at [`lab/analysis/_inbox/joint_surrogation_null_2026-08-30/BOUNDED_ROUND_PLAN.md`](../../lab/analysis/_inbox/joint_surrogation_null_2026-08-30/BOUNDED_ROUND_PLAN.md), revised after the day-level hard stop fired (PR #225 Round 4, Codex-corrected: neither model adequacy nor estimation-aware size/power clears). Three items touch this brief's reader. (1) **The day-level certification failure must NOT close this brief by inheritance** — both failure mechanisms are n-dependent and materially weaker at this brief's own bar level (estimation noise in the long-memory `d` at n≈1.5k days vs n≈135k–140k bars; the ~6-qualifying-year L4 wall vs 7 spanned calendar years with enormous per-year n), consistent with the ratification's own scoped-to-`Q-RANGEXFER-1`-only clause; this brief's Phase 1 gets its own independent assessment whenever it is next picked up. (2) A cheap, parallel, K-free diagnostic is named as owed here: **this construct's own by-year L4 qualifying-year count** (mirroring the `rangexfer_byyear_l4_2026-08-30` convention including its per-stratum floor correction) — unlike the day-level frames, `N_valid ≥ 7` may PASS at bar level, which would make `RESOLVED`/`FALSIFIED` genuinely reachable here and materially change the value of any future null-certification attempt. Precondition, made explicit per Codex's PR #226 review: hash-verified vendor bars (`MNQ_M15.csv`/`MYM_M15.csv` against the tracked `SHA256SUMS`) present in the executing environment — gitignored bytes do not travel with any checkout, so runnability is environment-relative, never assumed from the PR view. (3) This brief's §6 carries the same FALSIFIED/AMBIGUOUS-HOLD dual-fire precedence ambiguity as the sibling's (unstated which row governs when L5 valid-fails AND L4<7 both hold) — flagged to be frozen alongside the sibling's ⚖ L5-semantics ruling, not separately. No hypothesis, precondition, or verdict changed; no Phase 1 execution. | Claude Code, cross-referencing the upstream closure-path proposal |

---

## Verification

```bash
$ python .claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/Q-VOLREGIME-1-intraday-bar-volume-regime.md --type inquire
# Expected: RESULT: well-formed

$ git log --oneline docs/briefs/pre-registration/Q-VOLREGIME-1-verdict-preregistration.md
# Expected: pre-registration commit == this brief's own commit (both filed together, before Phase 1)

$ grep -n "N-2026-08-29-mnq-bar-volume-regime\|N-2026-08-29-mym-bar-volume-regime" docs/briefs/Q-VOLREGIME-1-intraday-bar-volume-regime.md
# Expected: both notices cited
```
