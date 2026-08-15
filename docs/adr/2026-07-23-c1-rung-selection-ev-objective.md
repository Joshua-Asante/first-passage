# ADR 2026-07-23 — c1 book rung-selection objective: EV-per-dollar-day (Q-BUSTGATE-1 fork B)

**Status:** `Accepted` — operator elected fork B (2026-07-23) and **ratified** this ADR the same day, choosing **"keep 0.50× / accept NO-GO on 1.00×"** once the already-run regime gate (1.00× FAIL) was surfaced. §6 downstream sweep complete. **Zero live-sizing effect at ratification:** the c1 rung stayed WATCH-1 0.50× / disarmed; the EV objective selects 0.50× among regime-robust rungs (§2). **AMENDED 2026-08-06 (claim-alignment M28):** read every *"live c1 rung stays WATCH-1 0.50× / disarmed"* as **historical** — both legs withdrawn 2026-08-04; rung selection is **not portable** to an F3 venue without re-measure (Addendum 2026-08-06). Revert triggers 2–3 **dormant, not pending**.
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `2026-08-04-tradeify-venue-descope-eval-included.md` — deployment / live-rung premise only. The EV objective and the both-halves admissibility gate for any rung *above* 0.50× stand; carrying 0.50× itself to a different venue geometry is **not** authorized by this ADR (see Addendum 2026-08-06).
**Retain-until:** none
**Decision date:** 2026-07-23
**Authors:** Joshua (fork-B election) + Claude Code Opus 4.8 (recorder/author)
**Related:** [`../briefs/Q-BUSTGATE-1-bust-gate-re-derivation.md`](../briefs/Q-BUSTGATE-1-bust-gate-re-derivation.md) (the Pre-Q whose fork B this ADR is) + its [pre-reg](../briefs/pre-registration/Q-BUSTGATE-1-verdict-preregistration.md) (`98d0fa6`); [`../briefs/closures/Q-FUNNEL-1-closure-resolved.md`](../briefs/closures/Q-FUNNEL-1-closure-resolved.md) (the EV evidence); [`../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) (the bust-floor gate, **RETAINED** for admission); [`2026-07-12-prop-portfolio-four-friendly-firms.md`](2026-07-12-prop-portfolio-four-friendly-firms.md) (§4 admission falsifier, untouched); [`2026-07-13-dd-protection-concept-not-constant.md`](2026-07-13-dd-protection-concept-not-constant.md) (the change-control chain any live rung change inherits); [`2026-07-17-c1-rail-build-account-registration-go.md`](2026-07-17-c1-rail-build-account-registration-go.md) (WATCH-1 0.50× / disarmed); [`../methodology/strategy_lifecycle.md`](../methodology/strategy_lifecycle.md) (down-only ladder).
**Layer:** execution + portfolio operations (rung-selection governance) — **NOT** locked-parameter. Zero change to any locked allocation, `dd_protection` constant, Pine source, MC anchor, `ACTIVE_FIRM`, or live rung; the live c1 rung stays WATCH-1 0.50× / disarmed until A0b (§2).

---

> ⚠ **Figure caveat 2026-08-06 (claim-alignment LAB-1):** bust cells sourced from
> `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md` were computed under
> defective `dd_lock_offset_usd: 100`. Corrected pins: full-panel **0.11%**, H1 **0.22%**,
> boot-95th **1.20%** (0.50×); H1 **6.78%** (1.00×). See that RESULTS banner +
> `CORRECTED_FULLPANEL.md`. Verdicts unchanged (0.50× PASS / 1.00× FAIL).

## §0 — Rule-0 reads (production-source verification, 2026-07-23)

- `docs/briefs/Q-BUSTGATE-1-bust-gate-re-derivation.md` — anchor `a3a7d71` (2026-07-23). Verdict `FALSIFIED`: the EV-optimal admissible rung (1.00×) busts **4.37% > 3.0%**; 3.0% is a survival, not fee/upside, quantity; fork B = adopt an EV objective.
- `docs/briefs/pre-registration/Q-BUSTGATE-1-verdict-preregistration.md` — anchor `98d0fa6` (2026-07-23). Frozen locational method; §D middle row (`FALSIFIED`) fired.
- `docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md` — anchor `b56c5b3` (2026-07-22). Horizon-robust cell `edge_panel_historical`: 1.00× ≻ 0.50× ≻ 0.25× on EV/dollar-day at every horizon {126,252,504}, both halves; `edge_half_panel` **horizon-fragile** (H1 reverses at 126). Its own disposition: "does **not** mean 1.00× should replace WATCH-1 0.50× today"; any rung change needs "pre-registered re-MC + both-halves regime gate + admitting ADR + very likely a B6 dry-fire re-run."
- `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` — anchor `be6dda6` (2026-07-13). Part A bust ≤ 3.0% / pass ≥ 50% — the candidate-admission falsifier, **retained unchanged** by this ADR (Trap #12).
- `core/firm_rules.py` — anchor `f8f8db1` (2026-07-22). `Tradeify_Select_100K` trailing_locking, max_dd 3.0% / target 6.0% / 40% consistency; `ACTIVE_FIRM="Tradeify_Select_100K"` — **unchanged** by this ADR.
- `STATE.md` / `docs/notes/rail_build/RUNBOOK.md` — c1 rail **disarmed** (`dry_run=true`); WATCH-1 0.50× last ratified rung; B6 PASSED 2026-07-20; B7 separate GO — **unchanged** by this ADR.
- `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md` + its **frozen operator-signed** pre-reg `docs/briefs/pre-registration/2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md` — anchor 2026-07-17 (RESULTS), pre-reg signed 2026-07-16. **The A0b both-halves regime gate, already run.** Verdict: **1.00× GATE FAIL (regime-fragile)** — H1 (2020–23 chop) bust **4.37%**, bootstrap-95th **10.37%** (both > 3.0% floor); H2 (2023–26 trend) 1.70%. **0.50× GATE PASS** on all four partitions (H1 0.14%, boot-95th 0.77%, pass-5th 95.76%). Operator ratified WATCH-1 deployability 2026-07-17. This is the load-bearing input to §2.

---

## §1 — Context

The 08-08 packet routed a live tension to the operator: Q-FUNNEL-1 (`b56c5b3`) established that on EV-per-dollar-day inclusive of eval resets (at the actual-paid fee) and funded payouts, the c1 book's **1.00×** rung strictly beats the ratified **WATCH-1 0.50×** rung — because the eval-fee cost of busting more often is cheap (≈12–36:1 upside:cost) relative to the funded upside forfeited by under-sizing. Q-BUSTGATE-1 (`a3a7d71`) then re-derived the survivor-scoring **Part-A bust ceiling (3.0%)** from that same fee/upside economics and found it `FALSIFIED` as an *economic* quantity: economics tolerate a bust rate far above 3.0% (the EV-optimum busts 4.37%), so the 3.0% ceiling is a **survival** gate, not a fee/upside one. The re-derivation's output was a two-option operator fork; on 2026-07-23 the operator **elected fork B** — adopt an EV-per-dollar-day objective. The c1 book's rung was pinned to WATCH-1 0.50× by the bust-floor logic (Q-COMPOSE-1 disposition); fork B decouples the c1 **rung-selection objective** from that bust-floor and ties it to EV instead.

**Decision driver (one sentence):** the operator has chosen to select the c1 book's live rung by EV-per-dollar-day rather than by the survivor-scoring bust-floor, and that objective change must be recorded structurally (not smuggled in as a silent rung flip) so its scope, falsifier, and downstream gates are explicit.

---

## §2 — Decision

**Decision:** For the **already-admitted c1 book** (Striker DJ30/MYM + Striker NAS100/MNQ), the **rung-selection objective is EV-per-dollar-day** — inclusive of eval resets at the actual-paid fee and funded payouts, per Q-FUNNEL-1's horizon-robust `edge_panel_historical` finding — **superseding the bust-floor rung *rationale*** (survivor-scoring bust ≤ 3.0% / pass ≥ 50%) that had pinned the c1 rung to WATCH-1 0.50×. The EV objective selects the EV-best rung **among the regime-robust admissible rungs** — regime-robustness (the both-halves gate) is a **hard admissibility precondition**, not overridden by EV.

**A0b resolved NO-GO on 1.00× — the live rung stays WATCH-1 0.50×.** The both-halves regime-robustness gate was **already run** under a frozen, operator-signed pre-registration (`class_s_c1_haircut_regime_remc`, 2026-07-17): **1.00× FAILS it** (regime-fragile — H1 chop-half bust 4.37%, bootstrap-95th 10.37%, both > the 3.0% floor), while **0.50× PASSES both halves**. So 1.00× is **not a regime-robust admissible rung**, and the EV objective — correctly constrained — selects **0.50× (WATCH-1)**, the current live rung. There is **no EV-vs-survival tension to resolve at a deployable rung**: once regime-robustness is enforced, EV and the bust-floor converge on 0.50×. **Operator elected "keep 0.50× / accept NO-GO" on 2026-07-23**, consistent with the operator's own 2026-07-17 WATCH-1 ratification.

**A future 1.00× (or any rung above 0.50×) is admissible only on fresh regime evidence.** It would require a new pre-registered both-halves regime re-MC showing that rung **PASSES both halves** (which the current evidence contradicts), then an admitting ADR (`concept-not-constant` chain) + B6 dry-fire re-run + B7 arm. This ADR authorizes **none** of that; it neither overrides the failed regime gate nor changes live sizing. The live c1 rung **stays WATCH-1 0.50× and disarmed**.

**The survivor-scoring bust ≤ 3.0% / pass ≥ 50% gate is RETAINED, unedited, as the candidate-ADMISSION falsifier** for new DISC-CAMP survivors (four-firms ADR §4). This ADR changes only the **rung-selection objective for the already-admitted c1 book** — not the admission gate for new candidates, and not the frozen 3.0% pre-reg (Trap #12).

**Effective:** upon acceptance for the *objective* (which rationale governs c1 rung selection); **zero live-sizing effect** until A0b clears.
**Scope:** the c1 book's rung selection only. Not candidate admission; not the locked strategies' parameters; not `dd_protection` constants; not any other firm/account.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Fork A — retain 3.0% bust-floor as the c1 rung objective** | The operator elected B (EV objective). But once regime-robustness is enforced (1.00× fails the both-halves gate), **both forks select 0.50×** — there is no EV upside to capture at a *deployable* rung, because the only above-0.50× rung EV would prefer (1.00×) is regime-inadmissible. Fork A remains the standing revert target (§4). |
| **Replace the survivor-scoring §4 candidate-ADMISSION gate too (broad EV replacement)** | Over-reach: Q-FUNNEL-1's evidence is c1-rung-specific; a *new, unproven* candidate should still clear a survival gate before admission (a bust-floor is the right instrument for "should this earn capital at all"). Narrow scope preserves the admission falsifier's integrity. |
| **Silently flip c1 to 1.00× in the GO ADR / lifecycle constants** | Forbidden (§5): a rung change is a `concept-not-constant`-class admission needing re-MC + both-halves regime gate + admitting ADR + dry-fire; skipping that is the exact `p`-hacking the pre-reg discipline forbids. |
| **Adopt EV but treat "4.37%" as the new bust ceiling number** | Category error: an EV objective wants a point-optimum, not a survive-threshold; transcribing the EV-optimum's bust as a "looser ceiling" conflates two instruments (Q-BUSTGATE-1 §5). |
| **Status quo — leave the objective ambiguous** | Worse: the Q-FUNNEL/survivor-scoring tension stays unresolved on the 08-08 board and invites an ad-hoc rung flip. The operator elected to resolve it. |

---

## §4 — Falsifier (revert trigger)

> ⚠ **READ FIRST — live-rung premise historical; triggers 2–3 DORMANT (2026-08-06).**
> §2 / §4 text below is **byte-unchanged**. Every *"the live c1 rung stays WATCH-1 0.50× / disarmed"*
> sentence in this ADR is a **dated ratification record**, not a current deployment claim
> (Tradeify de-scoped 2026-08-04; legs withdrawn). Trigger **1** (higher rung without fresh
> both-halves PASS) remains the live binding limb whenever a rung is next proposed.
> Triggers **2** and **3** are **dormant, not pending** — both consume live outcomes; neither
> names Tradeify, so both **re-arm unedited at F3** once a venue and armed book exist.
> **Portability gap:** §2/§4 gate any rung *above* 0.50× on a fresh both-halves PASS but are
> **silent on carrying 0.50× itself to a different geometry** — the selection rests on
> `Tradeify_Select_100K`'s $3,000 rope and 3.0% ceiling and is **not portable**; any F3 venue
> must **re-measure the rung before deployment even if unchanged in name**.
> Full record: §Addendum 2026-08-06.


**Status of the A0b regime gate:** already **run and resolved** (`class_s_c1_haircut_regime_remc`, 2026-07-17, operator-signed pre-reg) — **1.00× GATE FAIL, 0.50× GATE PASS**. It is not a pending future check; the 08-08 calendar dependency is **removed** (operator 2026-07-23) — there was never a real 08-08 gate on the rung, only this already-completed regime result. The triggers below govern the standing **0.50×** selection and any *future* attempt to admit a higher rung.

**Revert / re-open trigger (any one):**
1. **A higher rung is proposed without a fresh both-halves PASS.** Admitting 1.00× (or any rung above 0.50×) requires a **new** pre-registered both-halves regime re-MC showing that rung PASSES **both** halves. The current evidence is a decisive FAIL (H1 4.37% / boot-95th 10.37%); absent a fresh PASS, 1.00× stays inadmissible — attempting it anyway is the forbidden override (§5).
2. **Live EV underperformance.** After B7 arm + the first funded-months window, the c1 book's measured EV-per-dollar-day at 0.50× underperforms its own MC projection — re-open the objective (the EV case was benign-regime-weighted MC, not live).
3. **Un-priced survival cost manifests.** Firm-relations action or account-mortality clustering the week-block MC understates degrades the program — reverts to the pure bust-floor (fork A) framing.

**Revert action:** the c1 rung-selection objective reverts to the **survivor-scoring bust-floor (fork A)** framing; the live rung stays / reverts to WATCH-1 0.50×; this ADR is superseded by a fresh ADR recording the revert.

**Trigger check schedule:** regime re-MC **on demand** when a higher rung is proposed (no calendar gate); live-EV re-measure at the **first funded-months window after B7**; firm-relations monitoring continuous once armed.

---

## §5 — Forbidden moves (under this ADR)

- **Treating this ADR's acceptance as authorization to flip c1 to 1.00×** — it is not; 1.00× is **regime-inadmissible** (it FAILED the already-run both-halves gate: H1 4.37% / boot-95th 10.37%). Flipping to it would **override a failed safety gate** the operator signed on 2026-07-17 — the exact move the operator declined on 2026-07-23. Any future 1.00× needs a fresh both-halves PASS + admitting ADR + B6 re-run + B7, not this ADR's acceptance.
- **Editing the 3.0% survivor-scoring pre-reg in place** — Trap #12; the gate is RETAINED for candidate admission. A revert (fork A) supersedes *this* ADR; it does not un-freeze `be6dda6`.
- **Skipping the both-halves regime gate because "EV prefers 1.00×"** — the EV preference is horizon-robust on **only one** edge axis (`edge_panel_historical`); `edge_half_panel` was horizon-fragile. Reading a benign-regime EV preference as regime-robust is the exact failure the decompound-HOLD warns against.
- **Extending the EV objective to candidate ADMISSION** — a new unproven candidate must still clear the survival gate (§2 scope); EV rung-selection applies only to already-admitted books with an established edge.
- **Sizing above 1.00×** — down-only ladder cap (`strategy_lifecycle.md`); the EV-optimum is read at the ladder maximum, never past it.
- **Re-opening bust-floor compose (Q-COMPOSE-1) or unparking ORB via the EV objective** — Q-COMPOSE-1 stays FALSIFIED; ORB stays PARKED (operator 2026-07-23). This ADR is c1-rung-only.

---

## §6 — Consequences

**Positive consequences:**
- Resolves the Q-FUNNEL-1 / survivor-scoring objective tension the 08-08 packet routed to the operator, with an explicit recorded rationale rather than an ad-hoc rung flip.
- Gives the c1 book an EV-grounded rung objective and defines the A0b path to 1.00× (subject to gates).
- Keeps the candidate-admission survival gate intact — the change is surgically scoped.

**Negative consequences (real cost):**
- The c1 rung is no longer bust-survival-optimized; the objective accepts a higher bust (up to 4.37% at 1.00×) as EV-rational — more busts, more resets, more eval-fee churn, higher account mortality.
- More operator/firm-relations exposure per unit time (higher breach frequency).

**Risks (probabilistic):**
- **Benign-regime artifact.** The EV preference is horizon-robust on only one edge axis; a hostile 2020–2023-style regime could invert it. Mitigation: the A0b both-halves regime gate is a hard precondition to any live rung change (§2, §4.1).
- **MC understates clustering.** The week-block bootstrap understates breach clustering; live mortality could exceed the model. Mitigation: §4.2 live-EV re-measure + §4.3 monitoring.

**Downstream artifacts updated (§6 sweep complete before flip to `Accepted`):**
- [`Q-BUSTGATE-1-bust-gate-re-derivation.md`](../briefs/Q-BUSTGATE-1-bust-gate-re-derivation.md) closure — fork B elected + A0b NO-GO recorded (`closures/Q-BUSTGATE-1-closure-falsified.md`) ✔
- The 08-08 packet A0/A0b rows + §3 P0 — P0 discharged, fork B elected, **A0b resolved NO-GO on 1.00×**, 08-08 calendar dependency removed ✔
- `docs/briefs/INDEX.md` — Q-BUSTGATE-1 → closed; ADR referenced ✔
- `STATE.md` pointer log — the A0b NO-GO + EV-objective line added this session ✔ (minimal; the broader forward-board doc-authority sync stays the deferred session per packet §0.5).

---

## §7 — Implementation plan

**Policy-level — no mechanical live-sizing edits.** The c1 rung stays WATCH-1 0.50× / disarmed; this ADR records the objective and its current selection (0.50×), not a sizing change.

- **Phase 0** — §0 reads confirmed at ratification (incl. the class_s_c1 regime result). ✔
- **Phase 1 — DONE 2026-07-23.** Operator ratified the §2 scope + §4 triggers; §6 downstream sweep complete; status → `Accepted`. A0b resolved **NO-GO on 1.00×** on the already-run regime gate; live rung stays 0.50×.
- **Phase 2 (only if a higher rung is ever pursued; not now)** — a **fresh** pre-registered both-halves regime re-MC showing that rung PASSES both halves; if clear, an admitting ADR (`concept-not-constant` chain) + B6 dry-fire re-run + B7 arm. The current evidence is a decisive FAIL for 1.00×, so Phase 2 is **not** open. Only Phase 2 could change live sizing — its own decision, not authorized here.

---

## §10 — Audit hooks (runnable)

```bash
# The candidate-admission survival gate is RETAINED, unedited (Trap #12).
grep -n "3.0%\|≥ 50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md   # still 3.0% / 50%

# This ADR did NOT change live sizing: c1 stays WATCH-1 0.50× / disarmed until A0b.
grep -n "dry_run\|WATCH-1\|0.50" STATE.md docs/notes/rail_build/RUNBOOK.md | head
# HOOK REPAIRED 2026-08-03 (Rule 11, gate-stack audit R8): ACTIVE_FIRM was deleted 2026-07-30
# (substrate Phase 4, fc14682), so this grep now exits 1 and its "# unchanged" annotation asserted
# the opposite of the truth. The live tier is an explicit key, not a selector.
grep -n "Tradeify_Select_100K" core/firm_rules.py ops/c1_sizing_host_reference.py | head

# The fork-B lineage resolves both ways (this ADR ↔ Q-BUSTGATE-1 ↔ Q-FUNNEL-1).
grep -n "2026-07-23-c1-rung-selection-ev-objective" docs/briefs/closures/Q-BUSTGATE-1-closure-falsified.md
grep -n "Q-BUSTGATE-1\|fork B\|edge_panel_historical" docs/adr/2026-07-23-c1-rung-selection-ev-objective.md | head

# Status stays Proposed until the §6 downstream sweep completes AND operator ratifies.
grep -n "^\*\*Status:\*\*" docs/adr/2026-07-23-c1-rung-selection-ev-objective.md

# A0b regime gate is named as the live-rung precondition (must fire before any 1.00× flip).
grep -n "both-halves regime\|A0b\|regime_gate.py" docs/adr/2026-07-23-c1-rung-selection-ev-objective.md
```

---

## Verification

```bash
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-07-23-c1-rung-selection-ev-objective.md --type adr
python scripts/check_adr_graph.py                 # header vocabulary + edge integrity
git log -1 --format='%h %cs' -- docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md   # b56c5b3
git log -1 --format='%h %cs' -- docs/briefs/Q-BUSTGATE-1-bust-gate-re-derivation.md   # a3a7d71
```

---


## Addendum 2026-08-06 — Live-rung premise historical; 0.50× not portable (claim-alignment M28)

**Type:** dated correction under Rule 14. **§2 decision text and §4 trigger wording are not edited.**
Header gains `Superseded-in-part-by` → [`2026-08-04-tradeify-venue-descope-eval-included.md`](2026-08-04-tradeify-venue-descope-eval-included.md)
(deployment / live-rung premise only).

### Historical reading

At ratification (2026-07-23) the c1 book was deployed-but-disarmed at WATCH-1 0.50× on
`Tradeify_Select_100K`. As of 2026-08-04 both Striker legs are **withdrawn from deployment**;
there is no live c1 rung. Phrases of the form *"the live c1 rung stays WATCH-1 0.50× / disarmed"*
are **historical**.

### Portability (the load-bearing gap)

§2 / §4 correctly require a fresh both-halves PASS before any rung **above** 0.50×. They do
**not** authorize carrying the **0.50× name** onto a different firm-tier geometry. The 0.50×
selection is conditioned on Tradeify Select 100K's rope/ceiling; an F3 successor venue must
**re-measure** before deployment even if the chosen ladder rung is still called 0.50×.

### Revert triggers 2 and 3

| Trigger | Was | Now |
|---|---|---|
| 1 — higher rung without fresh both-halves PASS | binding | **still binding** whenever a rung is proposed |
| 2 — live EV underperformance after B7 / funded window | pending on arm | **dormant, not pending** (no live outcomes); re-arms unedited at F3 |
| 3 — un-priced survival cost / firm-relations | pending on arm | **dormant, not pending**; re-arms unedited at F3 |

| Date | Change | By |
|---|---|---|
| 2026-08-06 | Addendum 2026-08-06 — historical live-rung reading; portability gap; triggers 2–3 dormant; `Superseded-in-part-by` header edge. §2/§4 body byte-unchanged. | claim-alignment Phase 2 (M28) |

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-23 | Initial authoring — `Proposed`; operator elected fork B; c1 rung-selection objective = EV/dollar-day | Joshua + CC (Opus 4.8) |
| 2026-07-23 | **Ratified `Accepted`.** Corrected at ratification: the A0b both-halves regime gate was **already run** (class_s_c1, 2026-07-17) — **1.00× FAILS** it, so the EV objective selects **0.50×** among regime-robust rungs (not 1.00×). Operator chose "keep 0.50× / accept NO-GO"; 08-08 calendar dependency removed; live rung unchanged. | Joshua (ratify) + CC (Opus 4.8) |
