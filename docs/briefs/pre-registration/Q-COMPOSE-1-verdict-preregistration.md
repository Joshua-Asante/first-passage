# Pre-registration — Q-COMPOSE-1: composed-book (2-leg Class-S + ORB-MNQ-1) regime-breadth re-MC

**Status:** `FROZEN` (operator signed §9, 2026-07-16 — chat directive "GO — mixed book is in scope, freeze the pre-reg"; ORB weight signed **0.37%** via the §9 weight decision same session). No item below changes after any partition/tier result is seen (Known Trap #12 — amendments require closing Q-COMPOSE-1 and opening a fresh question).
**What this is:** a pre-registered composed-book re-MC that tests whether adding the ORB-MNQ-1 leg (book-level **breadth**, at neutral 1.00× lifecycle) restores regime-robustness to the 2-leg Class-S candidate #1 book, which cleared Part A but failed its regime rider (H1 chop-fragile).
**Parent Pre-Q (cited, not re-decided):** [`Q-COMPOSE-1`](../Q-COMPOSE-1-orb-classs-book-regime-breadth.md) (`OPEN`).
**Gate of record (unchanged, cited not re-decided):** [`2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md) (`be6dda6`, FROZEN) — floor bust ≤ 3.0% + P(pass) ≥ 50%.
**Sibling (orthogonal lever, NOT folded here):** [`2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md`](2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md) — the **sizing** lever (0.50×/0.25× on the fixed 2-leg book).
**Loop of record:** STRATEGIC. **Feeds:** the four-firms ADR §4 falsifier + c1's deployability disposition.
**Authored:** 2026-07-16 · Claude Code (Opus 4.8), operator-directed.

---

## §0 — Rule-0 reads (production source, verified 2026-07-16, HEAD `4848cf0`)

Per-file anchors (`git log -1 --format='%h %ci'`), content-read in full this session (also enumerated in the parent Pre-Q §0):

- **`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py` @ `163b0b5`** — the harness this re-MC extends. Injection point `daily_100k = book_daily_at_100k(panel_c1)` (L551); `_floor_ok = bust ≤ thr.eval_bust_ceiling AND pass ≥ thr.pass_floor` (L113-117); `half_panel_split` index-midpoint (L120-124); `part_a_bootstrap` `N_PANELS_DEFAULT=100` / `BLOCK_SIZE_BDAYS=126` / `BOOT_SEED=20260715` (L73-75); `DISCHARGE_TIERS=(Tradeify_Select_100K, MFFU_Rapid_100K)` (L72); GATE PASS iff bootstrap ∧ H1 ∧ H2 on both tiers.
- **`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/REGIME_GATE.md` @ `163b0b5`** — the 2-leg baseline this must beat: Tradeify H1 bust **4.37%** / bootstrap-95th **10.37%**; MFFU H1 **4.36%** / bootstrap-95th **10.33%**; full-panel + H2 (bust 1.70%) PASS; verdict **GATE FAIL**.
- **`lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage8_neff.md` @ `9620138`** — ORB breadth: dependence N_eff 1.99→2.95; realized corr ORB↔MNQ-Striker +0.15 / ↔MYM +0.00; ORB weekly $std ~1761 vs 814/932 (~2×); **dead 2020 (−0.029)**; risk N_eff falls if ORB sized up. **The §7 0.37% risk-dominance disclosure is grounded here.**
- **`lab/discovery/prop_survivor_scoring.py` @ `97011c1`** — `run_tier_remc` / `score_part_a` / `blocks_from_daily_pnl`; `score_part_a` finite-median = the P(pass) floor.
- **`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` @ `be6dda6`** — floor bust ≤ 3.0% + P(pass) ≥ 50%, Run-2, frozen $100K×4 tiers, discharge ≥2 incl. ≥1 `trailing_locking`. **Not re-decided.**
- **`docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md` @ `58fff1d`** — parent 2-leg book: MYM+MNQ weights 0.70%/0.37% (§5 forbids re-weighting them); ORB is the only new free weight.
- **`docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md` @ `507761a`** — §2 either/or candidate classes (the gate-0 admission question, GO'd in §1); §5 forbids post-hoc weight tuning + prior-look non-disclosure.
- **`docs/adr/2026-06-07-decompound-remc-hold.md` @ `fad8984`** — the precedent (no static de-risk regime-robust on this split); the §4 honest prior.
- **`core/lifecycle.py` @ `4441c72`** — ORB absent from `TIER_MULTIPLIER` ⇒ 1.00× (breadth lever at neutral lifecycle, orthogonal to the sizing sibling).

---

## §1 — Context, gate-0 admission (GO), and the lever under test

Class-S candidate #1 (2-leg MYM+MNQ Striker book) **cleared frozen Part A** on Tradeify+MFFU and discharged the four-firms §4 falsifier (banked, not re-opened) — but its regime rider returned **GATE FAIL (regime-fragile)**: full panel + H2 trend half pass, yet H1 2020-23 chop busts **4.37%/4.36%** and the 6mo-block bootstrap-95th hits **10.37%/10.33%**, both above the 3.0% floor. Sizing de-risk (the sibling haircut re-MC) is one untested lever; **book-level breadth is the other**, and ORB-MNQ-1's Stage-8 realized breadth (dependence N_eff 1.99→2.95; +0.15 corr to the same-instrument MNQ leg; net-positive over the H1 window as a whole) makes it the only leg available to test it.

**Gate-0 admission — GO (operator, 2026-07-16).** The composed book is a **mixed** object: 2 locked-leg native-futures expressions (admitted by the [`2026-07-14 existing-strategy ADR`](../../adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md)) + 1 discovery-survivor mechanism (ORB-MNQ-1, admitted individually by the four-firms ADR). Operator chat directive "GO — mixed book is in scope": read as **in-scope as-is** — it is "a prop-envelope portfolio" (four-firms §2 amended) and both constituents are individually admitted classes. **No ADR amendment required** (the AMEND/NO branches of Q-COMPOSE-1 §7 gate-0 were not taken); this consumes the explicit-operator-decision requirement (existing-strategy ADR §4). R5/P2 stay FALSIFIED — this book's claim is native bust-geometry at firm tiers, never CFD-edge transfer.

**Sibling relationship (not folded).** The haircut re-MC tests **sizing** (0.50×/0.25× on the fixed 2-leg book); this tests **breadth** (add a leg at 1.00×). Orthogonal — a combined (composed × haircut) arm is a separate future pre-registration if both singles fail (§5).

---

## §2 — The test (FIXED — the entire specification is this table)

| Item | Frozen value |
|---|---|
| Book | **3 legs:** MYM-Striker @ **0.70%**, MNQ-Striker @ **0.37%** (both byte-pinned from candidate #1, **not re-weighted**), + **ORB-MNQ-1 @ 0.37%** (operator-signed §9; ORB daily series engine-faithful, self-checked against `orb_backtest` in Stage-8). No 4th leg; no re-composition. |
| ORB weight | **0.37% risk_pct — SINGLE frozen weight** (operator §9). Not a sweep, not an arm set; one number, no post-hoc tuning (existing-strategy ADR §5). |
| Injection | ORB weight applied at the **allocation layer** (into `build_scaled_panel` / book-daily construction), NOT post-hoc on `daily_100k`, so the Run-2 consistency interaction is modeled on the true composed daily series. Executor confirms the injection shape in §8 Phase-0 before Phase 1; if `build_scaled_panel` cannot take a 3rd non-locked leg cleanly → `NEEDS_CONTEXT`, not a workaround. |
| Partitions | Full panel · **H1** (business-day first-half, 2020-23 chop) · **H2** (second-half, 2023-26 trend) · **6mo-block bootstrap** (n=100, block=126 bd, seed 20260715) — identical to the c1 rider; not re-parameterized. |
| Tiers | All four $100K tiers: `Bulenox_100K` · `Tradeify_Select_100K` · `MFFU_Rapid_100K` · `BluSky_Premium_100K`. Discharge requires **≥2 incl. ≥1 `trailing_locking`** (Tradeify/MFFU are the `trailing_locking` pair). |
| Engine | Frozen, inherited: 10,000 sims × seeds 42/123/2026, horizon 1500, inactivity disabled, `dd_protection` OFF, **Run-2 (consistency-on) where the firm has a consistency rule** — never re-decided. |
| Floor (per partition, per tier) | **bust ≤ 3.0% AND P(pass) ≥ 50%**; the bootstrap partition additionally requires **95th-pct bust ≤ 3.0%**. No separate "regime floor" (regime-robustness methodology). |
| Reported per (tier × partition) | `headline_bust`, `pass_rate`, `median_days_to_pass` (**diagnostic, non-gating**), `floor_ok`; bootstrap adds `pass_5th` / `bust_95th`. Plus the 3-leg `breadth.participation_ratio` declaration. |

---

## §3 — Inherited unchanged (cited, not re-decided)

Floor (3.0% / 50% / bootstrap-95th ≤ 3.0%), Run-2 semantics, the four $100K tiers, the discharge rule (≥2 incl. ≥1 `trailing_locking`), the engine block, and the H1/H2 index-midpoint split + bootstrap params all come verbatim from `be6dda6` (gate) and `163b0b5` (harness). The 2-leg sub-book weights 0.70%/0.37% come from `58fff1d`. Nothing in this file re-decides any of them; the sole new frozen input is ORB @ 0.37%.

---

## §4 — Falsifiable hypothesis (H-COMPOSE-1; binary)

**H-COMPOSE-1:** the composed 3-leg book {MYM @0.70%, MNQ @0.37%, ORB @0.37%} clears the frozen floor (bust ≤ 3.0% AND P(pass) ≥ 50%; bootstrap 95th ≤ 3.0%) on **full ∧ H1 ∧ H2 ∧ bootstrap**, on **≥2 of 4 tiers incl. ≥1 `trailing_locking`** — i.e., breadth does what the 2-leg book could not.

**Reject (FALSIFIED) if:** H1 headline bust > 3.0% **OR** bootstrap-95th > 3.0% on **every** tier at ORB @ 0.37% (the same limb the 2-leg book failed).
**Accept (RESOLVED) if:** all four partitions clear on **≥2 tiers incl. ≥1 `trailing_locking`**.
**Ambiguous-hold if:** all-four clear on exactly 1 tier, OR an H1↔bootstrap partition split not pre-committed as pass/fail.

**Honest prior (disclosed, not pre-biasing):** FALSIFIED — the decompound-HOLD precedent found no static de-risk regime-robust on this split, and ORB is regime-common-mode in the chop (dead 2020) despite +0.15 average correlation. RESOLVED is live because a near-independent, positive-over-H1 leg can lower a joint tail via diversification even if individually chop-fragile; both outcomes are pre-committed and real, which is why the compute is warranted.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Tuning ORB's weight after seeing results** — the live risk (ORB's variance makes weight the dominant knob); ruled out by existing-strategy ADR §5. One frozen weight; a failed candidate closes.
- **Re-weighting the 2-leg sub-book** — ruled out by parent pre-reg `58fff1d` §5.
- **Folding the haircut arms (0.50×/0.25×) into this re-MC** — Trap #11; breadth is isolated at 1.00×. Combined arm = separate future pre-reg.
- **A separate laxer H1 "regime floor"** — a hidden fitting parameter; regime-robustness methodology forbids it.
- **Outcome-conditional construction** (e.g. dropping 2020 from ORB's series before H1) — encodes the conclusion; ORB enters H1 with its 2020 death intact.
- **Transferring ORB's clean 2021+ Stage-6/7 pass across the regime boundary** to claim H1 — 2021+ is the trend regime the book already survives; H1 is the untested claim.
- **Reading RESOLVED as go-live authorization** — a cleared book = lifecycle CANDIDATE intake + §4 evidence only; Pine/rail/account/spend stay gated.

---

## §6 — Gate criteria (binary dispositions)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | full ∧ H1 ∧ H2 ∧ bootstrap-95th all clear on ≥2 tiers incl. ≥1 `trailing_locking`, at ORB @ 0.37% | 3-leg book = deployable-candidate path; lifecycle CANDIDATE intake (still gated); feeds four-firms §4 |
| `FALSIFIED` | H1 bust > 3.0% **OR** bootstrap-95th > 3.0% on **every** tier | Close; breadth does not rescue regime-fragility; extends decompound-HOLD; c1 → accept-with-caveat + tripwires |
| `AMBIGUOUS-HOLD` | all-four clear on exactly 1 tier, OR H1↔bootstrap split not pre-committed | Fresh pre-reg fixing the unresolved dimension; re-test rides 2026-08-08 |

---

## §7 — Prior-look disclosure (mandatory — existing-strategy ADR §5)

- **ORB sizing sweep already examined** (`RESULTS_stage8_neff.md`): ORB @ **0.37%** / 0.70% / 1.50% → risk N_eff 1.96 / 1.28 / 1.06. **0.37% is the primary sweep point AND the frozen weight** — chosen for continuity with the Stage-8 breadth/N_eff analysis and informativeness (large enough to move H1), *not* for risk-conservatism. **Disclosed risk-dominance:** at 0.37% ORB's weekly $ vol (~1761) is already ~2× the book legs' (814/932); the bootstrap-95th limb is the direct test of whether that dominance helps or hurts.
- **2-leg c1 regime gate** (`REGIME_GATE.md`): the baseline to beat (H1 4.37%/4.36%, bootstrap-95th 10.37%/10.33%). Seen.
- **Candidate #2 (3-leg Aegis)** FALSIFIED all-four-fail (bust 5.69%): a "third leg is not free" prior; ORB's properties are distinct (near-independent, high-variance).
- **2026-07-10/11 Tradeify futures3 runs**: the 2-leg/3-leg-Aegis 50K/100K priors (existing-strategy ADR §0); disclosed, not ORB-specific.

No other weight, partition, tier, or engine setting has been examined for this composed book.

---

## §8 — Run protocol (post-signature)

- **Phase 0** — re-verify §0 anchors; confirm `build_scaled_panel` accepts the 3-leg panel with ORB at the allocation layer (report the injection shape); confirm the Run-2 consistency clause is ratio/scale-correct on the composed daily series. Any architecture contradiction → `NEEDS_CONTEXT`.
- **Phase 1** — run full/H1/H2/bootstrap × 4 tiers; emit the per-cell table + 3-leg breadth declaration.
- **Phase 2** — assert §4/§6 gate against actual numbers; produce the Q-COMPOSE-1 §9 closure artifact.

---

## §9 — Operator signature (gates the run)

- **Gate-0 admission:** GO (mixed book in scope, no amendment) — Joshua, 2026-07-16 chat.
- **ORB weight:** **0.37% risk_pct** — Joshua, 2026-07-16 (weight decision; recommended option accepted after the risk-dominance nuance was surfaced).
- **Freeze authorization:** "GO — mixed book is in scope, freeze the pre-reg" — Joshua, 2026-07-16.

Frozen — no edits post-freeze (Trap #12).

---

## §10 — Audit hooks (runnable)

```bash
# §0 anchors still resolve
for f in lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py \
         lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage8_neff.md \
         docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md; do
  git log -1 --format='%h %ci' -- "$f"; done
# Expected: 163b0b5 / 9620138 / be6dda6 (or later — re-verify quotes if touched)

# Frozen floor unchanged (never relaxed by this fork)
grep -n "3.0%\|50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md | head

# The §2 arm is declared a SINGLE frozen weight (not a sweep); 0.70%/1.50% appear ONLY as §7 disclosed prior looks, never as ORB arms
grep -n "SINGLE frozen weight" docs/briefs/pre-registration/Q-COMPOSE-1-verdict-preregistration.md
# Expected: the §2 ORB-weight row. Any ORB @0.70%/1.50% *arm* outside §7 would be a §5 violation.

# Phase 1 did not run before this file was committed
git log --oneline -- docs/briefs/pre-registration/Q-COMPOSE-1-verdict-preregistration.md | tail -1
ls lab/analysis/*compose* 2>/dev/null || echo "no compose harness yet (expected pre-Phase-1)"
```

---

## Verification

```bash
python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/pre-registration/Q-COMPOSE-1-verdict-preregistration.md --type inquire
git log -1 --format='%h %ci' -- lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py \
  lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage8_neff.md docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-16 | Authored + FROZEN — gate-0 GO, ORB weight 0.37% signed, §0–§10 per the sibling haircut pre-reg convention | Joshua + Claude Code (Opus 4.8) |
