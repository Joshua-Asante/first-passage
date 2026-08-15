# Q-COMPOSE-1 — Does adding ORB-MNQ-1 change the prop book's binding regime-fragility?

**Status:** `CLOSED — FALSIFIED` (2026-07-17, frozen 10k×3 engine) — §6 row-2 fired on **every tier via both limbs** (H1 bust 54–68%, bootstrap-95th 47–60% vs the 3.0% ceiling at ORB @0.37%); breadth does not rescue — it destroys — the book's bust geometry (ORB's $438/day std at the $100K basis exceeds the entire 2-leg book's $273). Closure: [`closures/Q-COMPOSE-1-closure-falsified.md`](closures/Q-COMPOSE-1-closure-falsified.md); run artifacts [`lab/archive/q_compose_1_2026-07/`](../../lab/archive/q_compose_1_2026-07/RESULTS.md). Gate-0 was **GO** (mixed book in scope, no ADR amendment); ORB weight operator-signed **0.37%**; pre-reg [`Q-COMPOSE-1-verdict-preregistration.md`](pre-registration/Q-COMPOSE-1-verdict-preregistration.md) FROZEN 2026-07-16 (`970b5ed`), honored byte-for-byte.
**Authored:** 2026-07-16
**Closed:** 2026-07-17
**Authors:** Joshua (direction) + Claude Code (Opus 4.8, scoping)
**Parent question:** N/A (peer of the Class-S candidate #1 lifecycle-haircut re-MC — the two are **sibling levers on the same defect**, not parent/child; see §1)
**Sub-questions opened:** none (the mixed-book admission question is a Phase-0 **prerequisite gate**, not a forked research question — §7 gate-0)
**Loop:** STRATEGIC — closure gated on whether a pre-registered composed-book re-MC clears the frozen survivor floor on **both** regime halves at ≥2 firm tiers.
**Artifact path:** `docs/briefs/Q-COMPOSE-1-orb-classs-book-regime-breadth.md`

---

## §0 — Rule 0 reads (production-source verification)

All read in full this session (2026-07-16); anchors via `git log -1 --format='%h %ci' -- <path>`:

- `lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py` — anchor `163b0b5` (2026-07-15). The harness this re-MC extends. Injection point `daily_100k = book_daily_at_100k(panel_c1)`; `_floor_ok` = `bust ≤ thr.eval_bust_ceiling AND pass ≥ thr.pass_floor` (L113-117); `part_b_half_panel` index-midpoint split (L120-124); `part_a_bootstrap` `N_PANELS_DEFAULT=100`, `BLOCK_SIZE_BDAYS=126`, `BOOT_SEED=20260715` (L73-75); `DISCHARGE_TIERS = (Tradeify_Select_100K, MFFU_Rapid_100K)` (L72); GATE PASS iff bootstrap ∧ H1 ∧ H2 on both tiers.
- `lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/REGIME_GATE.md` — anchor `163b0b5` (2026-07-15). The **2-leg baseline this fork must beat:** Tradeify H1 bust **4.37%** / bootstrap-95th **10.37%**; MFFU H1 **4.36%** / bootstrap-95th **10.33%**; full-panel + H2 (bust 1.70%) PASS; verdict **GATE FAIL (regime-fragile)**.
- `lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage8_neff.md` — anchor `9620138` (2026-07-16). ORB-MNQ realized breadth vs the 2-leg book: dependence N_eff **1.99→2.95** (near-independent); realized weekly corr ORB↔MNQ-Striker **+0.15**, ORB↔MYM **+0.00**, ORB↔composite **+0.12**; ORB weekly $std **~1761 vs 814 (MYM)/932 (MNQ)** (~2×); ORB **dead in 2020 (−0.029)**, trend-regime-concentrated; risk N_eff **falls** if ORB sized up (0.70%→1.28, 1.50%→1.06).
- `lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md` — anchor `9620138` (2026-07-16). ORB-MNQ-1 = lifecycle **CANDIDATE @ 1.00×**, new mechanism (ORB on native MNQ), admitted **with standing caveats** (regime-conditional / cost-marginal full-window / high-variance). Not a locked-leg expression; not in `core/lifecycle.py::STRATEGY_KEYS`.
- `lab/research_utils/breadth.py` — anchor `d83e0f9` (2026-07-12). `participation_ratio` (scale-invariant N_eff); Stage-8 injects a single candidate as a 5th column and reports the corr/N_eff delta vs the book — the diagnostic this fork reuses for the composed book's breadth declaration.
- `lab/discovery/prop_survivor_scoring.py` — anchor `97011c1` (2026-07-13). `run_tier_remc` / `score_part_a` / `blocks_from_daily_pnl` — the MC primitives; `score_part_a`'s finite-median check is the P(pass) floor.
- `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` — anchor `be6dda6` (2026-07-13, FROZEN). The gate of record: **bust ≤ 3.0% AND P(pass) ≥ 50%**, Run-2, frozen $100K×4 tiers, discharge ≥2 firms incl. ≥1 `trailing_locking`. **Not re-decided here.**
- `docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md` — anchor `58fff1d` (2026-07-15, FROZEN). Parent 2-leg book: §2 fixed MYM+MNQ weights 0.70%/0.37% (venue variables); §5 **forbids re-weighting the 2-leg book**; §6 regime rider rides into G8 as a standing caveat.
- `docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md` — anchor `507761a` (2026-07-15, `Accepted`). §2 admits "prop-envelope portfolios from **either** Gen-2 discovery survivors **or** pre-registered existing-strategy books" — the **either/or that gate-0 must adjudicate** (a *mixed* book is named by neither branch); §4 "each candidate consumes an explicit operator decision"; §5 forbids post-hoc weight tuning + prior-look non-disclosure.
- `docs/adr/2026-06-07-decompound-remc-hold.md` — anchor `fad8984` (2026-07-14, HOLD). The precedent: on the same 2020-23/2023-26 split, **no static de-risk (k=0.55, DD_SCALE→0.20) was regime-robust** without making the challenge impractical. The honest prior for this fork.
- `core/lifecycle.py` — anchor `4441c72` (2026-07-11). `TIER_MULTIPLIER` ladder 1.00/0.50/0.25/0.00; ORB carries no entry (absent ⇒ 1.00×). Confirms this fork runs ORB at neutral lifecycle — the **breadth** lever, orthogonal to the parallel **sizing** (haircut) lever.

---

## §1 — Context & motivation

As of 2026-07-16 the program holds **two live objects**, both regime-caveated: Class-S candidate #1 (2-leg MYM+MNQ Striker book) — Part A DISCHARGED but regime rider **GATE FAIL** (H1 2020-23 chop bust 4.37%/4.36%, bootstrap-95th ~10.4%, above the 3.0% floor); and ORB-MNQ-1 — a full-pipeline discovery survivor, lifecycle CANDIDATE @1.00×. The book's **single binding constraint is the H1 chop-bust** — full panel and the H2 trend half both pass; only the stress window fails. Every path tried against that constraint has failed the same way: the 3-leg Aegis variant (candidate #2) FALSIFIED all-four-fail, and the CFD decompound-HOLD precedent (`docs/adr/2026-06-07`) found **no static de-risk regime-robust** on this exact split.

ORB-MNQ-1's realized Stage-8 breadth (`RESULTS_stage8_neff.md`) reopens exactly one untested lever: **book-level breadth**. ORB is near-independent of the book on the dependence axis (N_eff 1.99→2.95; realized corr +0.15 to the *same-instrument* MNQ leg) and net-positive over the H1 window as a whole — yet it is itself high-variance (~2× the book legs) and dead in 2020 (the book's worst year). Whether a near-independent, positive-over-H1, individually-chop-fragile leg **lowers** the composed book's H1 joint bust (diversification wins) or **raises** it (ORB's variance + 2020-death dominate) is a genuine MC question, not inspectable.

**Relationship to the parallel haircut re-MC (sibling, not parent):** the Class-S c1 lifecycle-haircut re-MC (pre-reg `2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md`, running in a separate session) tests the **sizing** lever — a uniform 0.50×/0.25× haircut on the *fixed 2-leg* book. Q-COMPOSE-1 tests the **breadth** lever — adding a leg at *neutral* 1.00× lifecycle. The two are orthogonal; §5 forbids folding them together in this re-MC. If both individually fail, a combined (composed × haircut) arm is a **separate** future test.

---

## §2 — Prior art / lineage

- **Class-S candidate #1** (`58fff1d`) — CLOSED Part-A DISCHARGED / regime rider GATE FAIL. The book this fork extends; its §5 weight-lock is inherited (the 2 Striker legs stay 0.70%/0.37%; only ORB's weight is new).
- **Class-S candidate #2** (3-leg Aegis, `FALSIFIED all-four-fail` 2026-07-16) — the last composition attempt; a *different* third leg (Aegis@0.75%) pushed bust to 5.69%. Direct evidence that "add a third leg" is not free — the leg's own properties decide.
- **ORB-MNQ-1 campaign** (Stage 2–8 COMPLETE, `ADMISSION.md`) — the leg under composition; admitted with a regime-common-mode + high-variance caveat.
- **Decompound-HOLD ADR** (`fad8984`, HOLD) — the load-bearing precedent: no static de-risk regime-robust on the 2020-23/2023-26 split. This fork tests whether **breadth** (a lever that ADR did not have — it only had sizing/allocation de-risk) escapes that finding.
- **`lesson_fifth_leg_no_regime_robust_static`** + **`lesson_market_neutral_not_regime_neutral`** (MEMORY) — a decorrelated leg is not a regime-neutral leg; the +0.15 average correlation explicitly does **not** capture the chop-tail common-mode. This is the honest prior weighing toward FALSIFIED.
- **`lesson_full_panel_masks_regime_split`** (MEMORY) — why the gate scores H1/H2 separately, not just the pooled panel.

---

## §3 — Question (Q-COMPOSE-1)

**Pre-Q gate test (symptom-only rephrase):** the fix-baked form would be "should we add ORB-MNQ as a third book leg?" The symptom-only form names the defect (regime-fragility / H1 chop-bust) and the lever under test (breadth) without presupposing the answer — the verdict "composition **worsens** the bust" is as admissible as "rescues it."

**Q-COMPOSE-1:** What does composing the 2-leg book with the ORB-MNQ-1 leg do to its binding H1 2020-23 chop-bust — does book-level breadth **improve, worsen, or leave unchanged** the stress-window bust geometry at the frozen floor, relative to the 2-leg baseline that the fixed-composition sizing de-risks (the parallel haircut re-MC) and the CFD-precedent static de-risks could not fix?

---

## §4 — Falsifiable hypothesis (H-COMPOSE-1)

**H-COMPOSE-1:** If the composed 3-leg book {MYM-Striker @0.70%, MNQ-Striker @0.37%, ORB-MNQ-1 @ its frozen weight} clears the frozen survivor floor — **headline bust ≤ 3.0% AND P(pass) ≥ 50%** — on the **full panel, H1 (2020-23), H2 (2023-26), and the 6mo-block bootstrap (95th-pct bust ≤ 3.0%)** on **≥2 of 4 firm tiers incl. ≥1 `trailing_locking`**, then breadth is a regime-robust path to deployability the 2-leg book lacked; otherwise breadth does not rescue the book's regime-fragility.

**Reject H-COMPOSE-1 (FALSIFIED) if:** at the frozen weight, H1 headline bust > 3.0% **OR** bootstrap-95th bust > 3.0% on **every** tier — i.e., the composed book fails the same limb the 2-leg book failed. Extends the decompound-HOLD "no static counterbalance" finding to a breadth-adding leg.
**Accept H-COMPOSE-1 (RESOLVED) if:** all four partitions (full/H1/H2/bootstrap) clear bust ≤ 3.0% AND P(pass) ≥ 50% on **≥2 tiers incl. ≥1 `trailing_locking`** — the composed book does what the 2-leg book + (per its sibling re-MC) the haircut could not.
**Ambiguous-hold if:** all four partitions clear on **exactly 1** tier, OR H1 clears but bootstrap-95th does not (or vice versa) — i.e., a partial pass not pre-committed as pass/fail. Re-test trigger: a fresh pre-registration fixing the unresolved dimension (never an in-place criterion edit — Trap #12).

---

## §5 — Forbidden moves

- **Tuning ORB's weight after seeing per-tier / per-partition results** — the single most tempting move, because ORB's ~2× variance makes weight the dominant knob and a sweep would "find" the weight that passes H1. Ruled out: `2026-07-14` existing-strategy ADR §5 forbids post-hoc weight tuning; the §8 pre-registration freezes **exactly one** weight vector with operator sign-off, and a failed candidate closes — it does not iterate in place. The Stage-8 sizing sweep (ORB @ 0.37%/0.70%/1.50%) is a **prior look and MUST be disclosed** in §8.
- **Re-weighting the 2-leg sub-book** (moving the Striker legs off 0.70%/0.37%) — ruled out: parent candidate #1 pre-reg (`58fff1d`) §5 locks them; only ORB's weight is the new free variable.
- **Folding the haircut arms (0.50×/0.25×) into this re-MC** — tempting ("test everything at once"), ruled out: multi-lever briefs (Trap #11) — this fork isolates breadth at neutral 1.00× lifecycle; the sizing lever is its sibling re-MC's job. A combined arm is a separate future pre-registration if both singles fail.
- **Introducing a separate, laxer "regime floor" for the H1 partition** — ruled out: `regime_robustness_gate.md` — the gate floor MUST equal the full-panel floor (3.0%); a separate regime floor is a hidden fitting parameter.
- **Outcome-conditional construction** (e.g., "drop 2020 from ORB's series since it's a documented-dead year, then test H1") — categorically forbidden; it encodes the conclusion. ORB enters H1 with its 2020 death intact.
- **Citing ORB's clean 2021+ Stage-6/7 pass as evidence the composed book passes H1** — the 2021+ window is the H2-adjacent trend regime the book already survives; H1 is the untested claim. Do not transfer the 2021+ result across the regime boundary.
- **Reading a RESOLVED verdict as go-live authorization** — a cleared composed book produces a lifecycle CANDIDATE intake + §4-falsifier evidence only; Pine/rail/account/live-spend stay separately gated (parent ADR).

---

## §6 — Gate criteria (closure verdict)

Inherited verbatim from the frozen survivor gate (`be6dda6`) + regime-robustness methodology; **no threshold re-decided here.** The only new pre-registered input is ORB's frozen weight (§8).

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | full panel ∧ H1 ∧ H2 ∧ bootstrap-95th all clear (bust ≤ 3.0% AND P(pass) ≥ 50%) on **≥2 tiers incl. ≥1 `trailing_locking`**, at the frozen weight | Composed book = deployable-candidate path; open a lifecycle CANDIDATE intake for the 3-leg book (still Pine/rail/account/spend-gated); feed the four-firms §4 falsifier |
| `FALSIFIED` | H1 bust > 3.0% **OR** bootstrap-95th > 3.0% on **every** tier at the frozen weight | Close; breadth does not rescue regime-fragility; capture as an extension of the decompound-HOLD "no static counterbalance" finding to a breadth leg; c1 disposition falls to accept-with-caveat + tripwires |
| `AMBIGUOUS-HOLD` | all-four clear on exactly 1 tier, OR H1↔bootstrap partition split not pre-committed | Fresh pre-reg fixing the unresolved dimension; re-test date rides 2026-08-08 |

**Pre-registered before any data touches analysis** (§8). Amending this table mid-run is Trap #12.

---

## §7 — Execution plan

**Phase 1 is BLOCKED until both pre-conditions below clear.**

- **Gate-0 (prerequisite — admission-scope adjudication; operator decision). RESOLVED-GO 2026-07-16.** The composed book is a **mixed** object: 2 locked-leg native-futures expressions (admitted by the `2026-07-14` existing-strategy ADR) + 1 discovery-survivor mechanism (ORB, admitted individually by the four-firms ADR). Operator chat directive "GO — mixed book is in scope": read as in-scope as-is ("a prop-envelope portfolio", both constituents individually admitted), **no ADR amendment**; the AMEND/NO branches were not taken. Recorded in the §8 pre-registration §0.
- **Phase 0 — Rule-0 re-reads + Phase-0 architecture confirm.** Re-verify the §0 anchors; confirm the harness injection point accepts a 3-column daily panel (the c1 harness builds a 2-leg `panel_c1`; ORB's daily series must be aligned to the same $200K-decompound frame via `build_scaled_panel`, ORB weight applied at the allocation layer, not post-hoc on `daily_100k` — mirrors the haircut re-reg's §8 fallback discipline). Report the injection shape before Phase 1.
- **§8 weight-freeze — author + commit the verdict pre-registration** (this §6 table + ORB's exact frozen weight + partition/engine params inherited from `be6dda6`/`163b0b5` + full prior-look disclosure incl. the Stage-8 sizing sweep). Operator signs the weight. **Recommended a-priori weight (not yet frozen): ORB @ 0.37%** — the risk-conservative choice, matching the smallest book leg and the Stage-8 primary sweep point, chosen *because* ORB's ~2× variance means any larger weight lets it dominate the risk budget (risk N_eff falls). The freeze commits to one number.
- **Phase 1 — composed-book re-MC.** Extend `run_class_s_c1_regime_gate.py` to the 3-leg panel; run full/H1/H2/bootstrap on the two discharge tiers (min), then the other two tiers for the ≥2-of-4 count. Report per (tier × partition): headline_bust, pass_rate, median_days (diagnostic), floor_ok; bootstrap adds pass_5th/bust_95th. Also emit the composed-book breadth declaration (`breadth.py` participation_ratio, 3-leg) for the intake record.
- **Phase 2 — Verdict assertion.** Run §6 against actual numbers; produce the §9 closure artifact.

---

## §8 — Verdict pre-registration (mandatory before Phase 1)

**FROZEN 2026-07-16** at [`docs/briefs/pre-registration/Q-COMPOSE-1-verdict-preregistration.md`](pre-registration/Q-COMPOSE-1-verdict-preregistration.md): the §6 table verbatim + ORB's frozen weight **0.37%** (operator-signed) + inherited partition/engine params + prior-look disclosure + the gate-0 GO record. Phase 1 may now run.

Pre-registration commit hash: `970b5ed`
Pre-registration date: 2026-07-16

---

## §9 — Closure record format

- **RESOLVED:** `docs/briefs/closures/Q-COMPOSE-1-closure-resolved.md` (+ lifecycle CANDIDATE intake note for the 3-leg book; no `recommendation.md` — go-live stays gated).
- **FALSIFIED:** `docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md`.
- **AMBIGUOUS-HOLD:** `docs/briefs/closures/Q-COMPOSE-1-closure-ambiguous.md` with the re-test trigger + date.

Must include: verdict; per-tier/per-partition anchor numbers vs the 3.0%/50% thresholds; the 2-leg baseline (H1 4.37%/4.36%, bootstrap-95th ~10.4%) vs the composed numbers; what the honest prior (FALSIFIED, per decompound-HOLD) predicted vs what happened; lesson candidates.

---

## §10 — Audit hooks (runnable)

```bash
# §0 anchors still resolve
for f in lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py \
         lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage8_neff.md \
         docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md \
         docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md; do
  git log -1 --format='%h %ci' -- "$f"; done
# Expected: 163b0b5 / 9620138 / be6dda6 / 507761a (or later, if a cited file was touched — re-verify quote if so)

# The frozen gate floor is unchanged (this fork must never relax it)
grep -n "3.0%\|≥ 50%\|50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md | head

# Phase 1 did not run before the §8 pre-registration was committed
ls docs/briefs/pre-registration/Q-COMPOSE-1-verdict-preregistration.md 2>/dev/null \
  && git log --oneline -- docs/briefs/pre-registration/Q-COMPOSE-1-verdict-preregistration.md
# Expected while OPEN — DRAFT: file absent (pre-registration not yet frozen)

# Gate-0 admission adjudication is recorded before any composed-book re-MC lands
grep -rn "Q-COMPOSE-1" docs/adr/ docs/SESSIONS.md 2>/dev/null
```

---

## Verification

```bash
# Discipline checks (mechanical)
python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/Q-COMPOSE-1-orb-classs-book-regime-breadth.md --type inquire

# Production-source verification (Rule 0 confirmation)
git log -1 --format='%h %ci' -- lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/REGIME_GATE.md \
  lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage8_neff.md \
  docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md

# Cross-reference: the 2-leg baseline numbers this fork must beat
grep -n "4.37\|10.37\|GATE FAIL" lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/REGIME_GATE.md
```

---

## Pre-Lock Checklist (LOCKED 2026-07-16)

- [x] All §0 paths read and anchored with commit hash
- [x] §3 question passes the symptom-only rephrase test
- [x] §4 hypothesis falsifiable (binary triggers in §6)
- [x] §5 forbidden moves genuinely tempting (weight-tuning is the live risk)
- [x] §6 gates have specific numerical triggers (3.0% / 50% / ≥2 tiers)
- [x] **Gate-0 admission adjudication — RESOLVED-GO (mixed book in scope, no amendment)**
- [x] **§8 pre-registration FROZEN with operator-signed ORB weight (0.37%) — Phase 1 unblocked**
- [x] §10 audit hooks are runnable commands
