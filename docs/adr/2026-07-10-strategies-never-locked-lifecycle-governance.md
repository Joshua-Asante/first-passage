# ADR 2026-07-10 — Strategies are never locked: separate parameter-immutability (LOCKED) from revocable capital-authorization (lifecycle); govern decaying edges by graded de-risk

**Status:** `Accepted` — operator **ratified all five §2 numeric calls as recommended on 2026-07-10** (the day they were proposed). This ADR records the governance-model decision and its reasoning; the ratified values, forbidden moves and implementation status live in [`docs/methodology/strategy_lifecycle.md`](../methodology/strategy_lifecycle.md) (canonical owner); effective multipliers are read from `core/lifecycle.py` and its state.
**Superseded-by:** none
**Superseded-in-part-by:** `2026-08-07-loop-s5-bounded-promotion-lane.md` — **Call 5** “no autonomous promotion” invariant only (bounded sandbox-up exception: micro size · fixed loss/attempt budget · capped concurrency; operator approves budgets not candidates; ceiling-crossings operator-only). Demotion, retirement GO/NO-GO, RETIRED re-entry bar, and re-optimization bar **stand**.
**Retain-until:** none
**Revision:** 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): the stale Phase-2 status clauses; §0 reads (reduced to a pointer); the RECOMMENDED and OPERATOR-RATIFIES value blocks of Calls 1–5, Call 2's pre-wiring mechanism text, the Call 5 rail caveat and the Status-vocabulary section (ratified values and vocabulary live in `strategy_lifecycle.md`); the §5 list, §6 gate items and ratification status, §7, §10 hooks (one still-runnable hook kept), the Verification block, the Change history and the 2026-09-01 diagnostic body removed. §1, §3, §4 (with its trigger schedule), the §6 FALSIFIED/AMBIGUOUS clause, the Call 5 Addendum 2026-08-07 and the 2026-09-01 ruling kept verbatim. Pre-trim text at blob `8bb300fa20a39904daaf01b7e50e2e276572b2d2` (commit `dad73e3d2c6b78a2ca10a4ba90df2765a05286e8`).
**Decision date:** 2026-07-10
**Authors:** Joshua (decision) + Claude (drafter, this session)
**Supersedes:** none. **Refines** the standing "The portfolio and strategies are LOCKED" Key Principle (`CLAUDE.md`) by splitting the word "locked" into its two silent meanings (see §1). Does **not** supersede any allocation, `dd_protection`, or lock-decision ADR — those remain the canonical owners of their constants.
**Related:** `docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md` (the discretion-governance precedent: pre-authorize the one legitimate intervention rather than pretend intervention never happens — this ADR is the *ex-ante* generalization of that *ex-post* move); `docs/adr/2026-06-07-decompound-remc-hold.md` (the regime-split evidence base — the shared-beta regime dependence this ADR's Call 4 monitors); `CLAUDE.md` §Protection (the existing pre-registered decay-style trigger this ADR extends — quarterly C2→C0 revert, rolling-6mo MC-pass <95% for two consecutive windows); `docs/methodology/observation_routing.md` (Closed/Action/Forward — the observation-disposition axis, *orthogonal* to the authorization axis added here); `docs/methodology/regime_robustness_gate.md`; `docs/rejected_candidates.md` / `docs/methodology/rejected_signals.md` (re-proposal requires new mechanism / dated incident, not new parameters — the doctrinal parent of §5's "decay is never a re-optimization trigger"); the Q-MECH-1 family finding (one shared long-continuation beta across all four legs; NY-morning entry; 2023–26 trend era; zero free external monitors — the load-bearing premise, carried in memory/session, not re-derived here).
**Layer:** methodology + operational (governance model for capital authorization over a strategy's life; a new sizing *factor*). **Not** strategy/risk-control parameters — no SL/TP/ATR/risk%/pyramid/session/BE/trail constant, no `dd_protection` constant, no allocation, no Pine source is touched by this ADR. The locked MC anchor (99.83/0.17/4.37) is untouched and needs no re-MC.

---

## §0 — Rule 0 reads (production/source verification)

Spent: the 2026-07-10 working-tree reads (`core/dd_protection.py`, `ops/accounts.py` and `ops/cli.py` at `6f5480bf`; `CLAUDE.md`, `docs/methodology/observation_routing.md` and the 2026-06-30 precedent ADR) are in the pre-trim blob (see **Revision**).

---

## §1 — Context

Four conversation-level findings force a governance change:

1. **Edges decay; "consistent over time" is not verifiable, only not-yet-falsified.** Every busted quant strategy was significant, non-random, and consistent — until it wasn't. An unexplained edge in particular carries *no prior on durability*: when it degrades, the first evidence is losses (an explained edge often telegraphs its death — the roll changed, the fix moved, a competitor arrived). So a live strategy is a **decaying asset of unknown half-life**, not a permanent fact.

2. **Therefore no strategy can be "locked" in the sense of *authorized to hold capital indefinitely*.** But the word "LOCKED" in this repo has been doing **two jobs at once**: (a) *parameters are immutable* — an anti-overfitting promise to self, and (b) *this earns capital indefinitely* — a durability claim about the future. Finding 1 kills only (b). Job (a) should get **stronger**, not weaker. The fix is not to rename "LOCKED" (it already means (a), correctly, everywhere in the repo — renaming is pure churn). The fix is to make **authorization** — the thing (b) was silently asserting — an **explicit, separate, always-revocable axis** that was previously bundled into "LOCKED" and into the static MC anchor.

3. **Commitment migrates from the strategy to the lifecycle that governs it.** You stop freezing the *answer* (indefinite authorization) and start freezing the *procedure that decides when the answer expires*. Everything about *how you decide to pull capital* gets locked harder than any parameter ever was. This is the only way "never locked" (authorization) coexists with "locked" (parameters) without contradiction — they are different axes.

4. **The repo already does a version of this and already has the beta-death dataset.** §Protection's C2→C0 revert is a pre-registered, two-consecutive-window, MC-pass-based decay trigger — this ADR generalizes that one instance into a standing model. And the 2026-06-07 regime HOLD already quantified the shared beta's regime dependence (the 2020–23 chop half is the adverse-regime training set). This ADR is an **extension of existing patterns**, gated by The Algorithm (Question → Delete → Simplify → Accelerate): it adds one axis and reuses the quarterly regime-check cadence rather than standing up a parallel framework.

**The premise that makes Call 4 the priority:** Q-MECH-1 found all four legs express **one** long-continuation beta. Decay may therefore arrive **portfolio-wide in a single regime shift**, not leg-by-leg — four simultaneous drawdowns could be the shared beta dying, not coincidence. Renaissance could ignore explanation because *breadth* (thousands of uncorrelated weak bets) was its significance-and-survival machine; at n≈hundreds/yr and one shared beta, that insurance is structurally absent. This is the operation's **stated largest structural exposure** (the monitor gap), and it is why Call 4 sequences first.

**Decision driver (one sentence):** because live edges decay and "consistent over time" can only be disproven (never confirmed), capital authorization must be an explicit, always-revocable, graded axis governed by pre-registered triggers — while strategy parameters stay LOCKED harder than before — so that decay is met by a cheap reversible de-risk fired by a rule, not by the in-the-moment discretion that produced the 2026-06-30 receipt.

---

## §2 — Decision

**Meta-decision.** Split the overloaded "LOCKED" into two orthogonal axes and add the second as first-class state:

- **Parameter axis — `LOCKED` (unchanged meaning, strengthened enforcement):** every SL/TP/ATR/risk%/pyramid/session/BE/trail constant + Pine source is immutable. Retained verbatim; no rename. Decay **never** authorizes editing these (§5).
- **Authorization axis — NEW, explicit lifecycle:** `CANDIDATE → AUTHORIZED → WATCH → RETIRED`, plus a **durability-source tag** `{MECHANISM | SURVIVAL-ONLY}` that selects the surveillance regime. A live strategy is now described by *both* axes, e.g. **"Guardian v5.5 · LOCKED · AUTHORIZED · MECHANISM."** "Locked but never locked" ceases to be a paradox: LOCKED was only ever about parameters; authorization is the axis that is always live and revocable. The 99.83/0.17/4.37 allocation is, under this model, an **AUTHORIZED-state fact whose inputs are LOCKED** — not a permanent guarantee. (And because the lifecycle multiplier only ever *reduces* size, any WATCH-active book is strictly lower-risk than this AUTHORIZED-state config — the bust/DD gates move only safe-side, so a de-risk never requires a re-MC.)

This axis is **orthogonal** to `dd_protection` (intra-challenge drawdown, this account, this window) and to observation-routing Closed/Action/Forward (finding disposition). It composes with them; it replaces neither.

The five judgment calls below are the substance. Each states what is **DETERMINED** (structure/direction — not the operator's to re-litigate), the **RECOMMENDED** starting value (anchored to existing repo patterns), and the **OPERATOR-RATIFIES** hook (the free parameter no computation can set — a risk/regret preference).

---

### Call 1 — Decay-detection threshold (the Type-I/Type-II regret preference)

**DETERMINED.** A live edge in a normal drawdown and a dead edge are *statistically indistinguishable in the window where you must act*. So this is not a detection rule you can make "correct" — it is a **regret preference** set in advance and in writing (the 2026-06-30 episode is the archive evidence of what setting it in-the-moment produces). It must have the same **structural shape as the existing §Protection revert trigger**: a rolling metric vs a pre-registered floor, requiring **persistence** (≥2 consecutive readings) so a single drawdown cannot trip it. Its action is **de-risk (→ WATCH), never kill** — which is what makes an aggressive/early setting affordable (see interlock note).

**Interlock with Call 2 (the key move).** Because the response is graded, reversible sizing (Call 2), a false positive costs only *one size step*, not a killed edge. Therefore the threshold should be set **tight/early**, biased toward Type-I (de-risk a live edge too soon) over Type-II (feed a dead one too long) — the opposite of what you'd choose if the trigger killed the strategy. The terror of the binary dissolves once the action is cheap.

**Ratified values:** [`strategy_lifecycle.md` Call 1](../methodology/strategy_lifecycle.md#call-1--decay-detection-threshold-the-regret-preference) (provisional-until-data; §6 AMBIGUOUS governs).

---

### Call 2 — Sizing as the response variable (stepped, not smooth)

**DETERMINED.** The escape from the binary is to make authorization **continuous in effect but discrete in mechanism**: size becomes a function of durability confidence, so no single decay reading ever bets the strategy's life — it nudges an allocation. The tiers are **stepped, not a smooth curve**: a smooth `size = f(confidence)` invites continuous discretionary micro-adjustment, which is the tinkering failure mode wearing a lab coat. Steps are auditable.

**Mechanism (ratified):** the lifecycle multiplier is a per-strategy risk-authorization haircut at the risk_pct layer, compounding multiplicatively with `DD_SCALE` — two independent de-risk signals stack (WATCH-1 in DD ⇒ 0.20×); current code paths and the quantity-layer fallback for pyramided legs: [`strategy_lifecycle.md` Call 2](../methodology/strategy_lifecycle.md#call-2--sizing-as-the-response-variable-stepped-not-smooth).

**Axis-separation (the load-bearing invariant).** Implementation adds a per-strategy authorization scalar to dd_protection's `scaled_risk` computation **without altering `BASE_RISK`, `DD_SCALE`, or `DD_TRIGGER`** (they stay byte-identical; the new factor multiplies them at compute time, it does not edit them). The §4-trigger-3 axis-separation test (`tests/test_lifecycle.py`) pins exactly that: a lifecycle tier change must leave every locked constant untouched. The lifecycle factor is a pure authorization scalar; round-down/never-up is preserved at the sizing host's integer-quantity floor (Call 2 in `strategy_lifecycle.md`).

**Ratified values:** [`strategy_lifecycle.md` Call 2](../methodology/strategy_lifecycle.md#call-2--sizing-as-the-response-variable-stepped-not-smooth).

---

### Call 3 — The explained/unexplained differential (pricing the dropped explanation-filter)

**DETERMINED.** Dropping the explanation requirement does not make a signal cheaper — it moves the invoice from the "mechanism" line to the "statistics + surveillance" line, and **the bar must rise to pay it**. Direction is fixed: `SURVIVAL-ONLY ⟹ smaller starting size, faster review, tighter trigger` than `MECHANISM`. The **durability-source tag** is what carries this: it selects the surveillance regime. Magnitudes are the operator's call.

**Ratified values and portfolio nuance:** [`strategy_lifecycle.md` Call 3](../methodology/strategy_lifecycle.md#call-3--the-explainedunexplained-differential).

---

### Call 4 — The beta-level trigger (the portfolio killer) — SEQUENCE FIRST

**DETERMINED.** Because the four legs are one beta, decay can arrive **portfolio-wide at once**; correlated simultaneous degradation is the signature of the *shared beta dying*, categorically different from one leg drifting. This is the only **portfolio-fatal** call and it is structurally **low-n** (possibly zero calibration events before the real one) — so it must be pre-registered from the **existing regime-split evidence** (the 2026-06-07 decompound HOLD's 2020–23 adverse half), not calibrated after the fact, and its action must be the **most conservative** (graded portfolio-wide de-risk + **mandatory operator GO/NO-GO**, not silent full kill). It was framed as an **extension of the then-existing quarterly regime trigger**, not a new monitor (that trigger was retired 2026-07-22; evaluation record: Call 4 in `strategy_lifecycle.md`).

**Ratified values:** [`strategy_lifecycle.md` Call 4](../methodology/strategy_lifecycle.md#call-4--the-beta-level-trigger-the-portfolio-killer--sequence-first).

Rationale for 3-of-4 as the act line: 2-of-4 is plausibly coincidental even in a shared-beta book; 3-of-4 simultaneous is strong correlated-degradation evidence. The soft 2-of-4 flag buys an early look without over-triggering.

---

### Call 5 — The automation boundary (what fires without the operator)

**DETERMINED.** Continuous surveillance + revocable capital forces the question of what acts autonomously. The boundary is **reversibility**, and it inherits the repo's existing asymmetry (`dd_protection` already *computes* 0.40× with no sign-off; sizing always rounds **down, never up**):

Rail status and the "rules-mandated" reading: [`strategy_lifecycle.md` Call 5](../methodology/strategy_lifecycle.md#call-5--the-automation-boundary-reversibility).

- **Reversible de-risk → autonomous, rules-based** ("rules-mandated": no fresh in-the-moment judgment). Tier demotions (AUTHORIZED→WATCH-1→WATCH-2), Call-1 firings, and the Call-4 **soft flag + 0.5× beta de-risk** fire without fresh operator judgment. Cheap to be wrong, expensive to hesitate.
- **Irreversible retirement → operator-confirmed against pre-registered criteria.** WATCH-2→`RETIRED` (capital to zero) and **full beta shutdown** require an operator GO/NO-GO — but the operator's role is **verification of pre-registered criteria**, not fresh judgment at maximum emotional load (this mirrors the R6 GO/NO-GO pattern).
- **Hard asymmetry (the load-bearing constraint):** automation may move authorization **down** only. It may **never** promote a tier, re-enter a RETIRED strategy, increase size beyond the authorized tier, or re-optimize — those are all operator-ratified, always. Automate the protective direction; gate every risk-adding direction. (Direct analogue of "always round down, never up.")

#### Addendum 2026-08-07 — Call 5 superseded in part by S5 bounded promotion lane

**Status:** binding on Accept of [`2026-08-07-loop-s5-bounded-promotion-lane.md`](2026-08-07-loop-s5-bounded-promotion-lane.md). Historical Call 5 body above is **frozen**; this addendum is the operative amendment.

Call 5’s absolute “no autonomous promotion” invariant gains **exactly one** bounded up-exception: automation may admit a gate-validated candidate into a capped sandbox (micro size · fixed per-candidate loss/attempt budget · capped concurrency) when the promotion packet Passes the S5 validator + refuter. The operator approves **budgets**, not candidates; every ceiling-crossing remains operator-only; demotion remains universal and instant. RETIRED re-entry, re-optimization, full AUTHORIZED size-up, and unattended-loop authorization are **not** granted by this addendum. Canonical values / wording live in [`strategy_lifecycle.md`](../methodology/strategy_lifecycle.md) Call 5.

---

Vocabulary: [`strategy_lifecycle.md` §The two orthogonal axes](../methodology/strategy_lifecycle.md#the-two-orthogonal-axes).

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Keep the binary lock (LOCKED ⇒ permanent authorization)** | Contradicts the decaying-asset reality (§1). Leaves only "hold or panic-kill" when an edge dies — which *is* the in-the-moment discretion that produced the 2026-06-30 receipt. No graded response = the failure mode re-imported. |
| **Rename `LOCKED` → `FROZEN` repo-wide, add lifecycle** (my earlier session proposal) | Pure process-gravity. "LOCKED" already means parameter-immutability *everywhere* in the repo + the whole lock-decision-brief apparatus. Renaming is churn for zero conceptual gain. The actual gap is an *added* authorization axis, not a relabel — so add the axis and leave LOCKED alone. |
| **Unified sizing product** `final_lots = base_mult × dd_factor × lifecycle × indicator_lots` (an earlier draft of Call 2) | **Falsified by §0 production reads.** No such product exists: `dd_protection` scales `risk_pct` (inside TV) and `calc_multiplier` scales the account (outside TV); they never meet in code. The "`min()` vs product" question was malformed. Corrected: lifecycle lands at the risk_pct layer, multiplicative with `DD_SCALE` (Call 2). Kept in this table as the concrete anti-pattern (precision exceeding grounding). |
| **Continuous smooth sizing curve** `size = f(confidence)` | Mathematically neat, operationally corrosive: a smooth curve invites continuous discretionary micro-adjustment (tinkering in a lab coat). Stepped tiers are auditable and cannot be nudged between steps without an explicit, logged tier change. |
| **Kill-only: binary AUTHORIZED/RETIRED, no WATCH tiers** | Forces the terrifying binary in exactly the window where live-vs-dying is statistically indistinguishable. Graded sizing is the *only* escape from that binary and the thing that lets Call 1's trigger be set tight/cheap. Removing tiers removes the interlock. |
| **Leave decay handling to in-the-moment operator discretion** | This is the 2026-06-30 failure mode by definition. The entire point is pre-registration (§0 precedent 2026-06-30). A "we'll judge it when we see it" policy is the anti-policy. |
| **Full autonomy incl. retirement + re-entry + re-optimization** | Irreversible actions at max emotional/uncertainty load need operator verification; autonomous re-entry/re-opt is `p`-hacking at the execution layer. The reversibility boundary (Call 5) exists precisely to keep the cheap direction automated and the expensive direction gated. |
| **Stand up a parallel "decay framework" separate from the regime check** | Fails The Algorithm (Delete/Simplify). §Protection already runs a quarterly MC-based revert trigger and the 08-08 regime check already exists. Reuse the cadence; add one axis. A parallel framework reproduces the forward-loaded-artefact problem `observation_routing.md` was written to kill. |

---

## §4 — Falsifier (revert trigger)

This ADR accepts real costs (§6): surveillance overhead, and the risk that graded de-risk clips a live edge (Type-I) that would have recovered.

**Revert trigger (binary; the lifecycle model is falsified *as implemented* if either fires):**
1. **Type-I dominance:** over **two consecutive** regime-check cycles, the WATCH machinery produces **zero** true decay detections **and** ≥ **2** de-risk firings each later shown (by the metric recovering to baseline within one further window with no parameter change) to have clipped a live edge — i.e. surveillance is measurably costing more edge than it protects. → recalibrate thresholds via a fresh ADR, or revert to static locks.
2. **Type-II failure:** a strategy or the shared beta suffers a sustained, unrecoverable PF collapse (below baseline − 2σ for ≥2 windows) with **no prior WATCH signal** — the machinery did not see it coming, so it is not doing its job. → the trigger design is falsified; redesign (fresh ADR) or revert.
3. **Axis-contamination (integrity failure, immediate):** the authorization/lifecycle multiplier is ever found to have altered a **LOCKED parameter** (the two axes bled — e.g. a tier change mutated `BASE_RISK`, `DD_SCALE`, or `DD_TRIGGER` rather than multiplying against them). → immediate stop-and-fix; this is the one non-negotiable invariant of the whole model.

**Revert action:** supersede this ADR with a fresh one stating which trigger fired as the anchor. **Never edit §2's ratified values or §4 in place** (inherited from 2026-06-30 §5). The discomfort of a Type-I clip is a *named cost*, not grounds to silently loosen a floor.

**Trigger check schedule:** at each quarterly programme audit / regime trigger — next **2026-08-08**, then 2026-11-08, 2027-02-08, 2027-05-08 — plus event-driven for trigger 3; plus (carried from removed ADR 2026-08-06-candidate-call1-action-on-breach, rule now in strategy_lifecycle.md Call 1): Cap companion arming GO (packet 3), any ORB unpark GO, and 2026-11-08 programme audit if still open — check every hot mirror says operator-review-flag-only for a CANDIDATE breach and no code path autonomously demotes or retires from CANDIDATE.

---

## §5 — Forbidden moves (the "locked-harder" column)

- Owned by [`strategy_lifecycle.md` §Forbidden moves](../methodology/strategy_lifecycle.md#forbidden-moves-the-locked-harder-column) (amended for S5). Prior text: pre-trim blob (see **Revision**).

---

## §6 — Gate (binary closure criteria)

Gate items 1–2 met (values in [`strategy_lifecycle.md`](../methodology/strategy_lifecycle.md); authorization-axis vocabulary in AGENTS.md §Strategy Authorization Lifecycle). Item 3 (STATE.md forward-board bullets) retired by the Addendum 2026-09-01 ruling.

**FALSIFIED / re-open** per any §4 trigger. **AMBIGUOUS** if, at the 2026-08-08 first evaluation, the Call-1 metric has < the minimum trade count to compute a rolling PF for ≥2 legs — in which case the calls' *structure* stands but the numeric floors are provisional and re-confirmed at 2026-11-08 (recorded, not silently amended).

---

## §7 — Implementation plan

Implementation status, scope note and sequencing: [`strategy_lifecycle.md` §Implementation status](../methodology/strategy_lifecycle.md#implementation-status).

---

## §10 — Audit hooks (runnable)

The other 2026-07-10 hooks targeted the retired `CLAUDE.md`, `core/config/params.toml` and `ops/accounts.py` (pre-trim blob, see **Revision**). Still runnable:

```bash
# §4 trigger 3 axis-separation invariant: a tier change alters no locked constant
python -m pytest -q tests/test_lifecycle.py
```

---

## Addendum 2026-09-01 -- STATE.md forward-board entries missing (verdict-free diagnostic)

Diagnostic (2026-09-01): §6 gate item 3 / §10 hook #6 found STATE.md carrying no decay-review or beta-death bullets; the 2026-08-08 evaluation is recorded in docs/notes/audits/programme-audit/2026-08-08-quarterly-audit.md row 7.

**Ruling (direct operator instruction, 2026-09-01): elect option (b).** This ADR's §6 gate item 3
and §10 audit hook #6 (the requirement that STATE.md's forward-trigger board carry standing
"decay review"/"beta-death review" bullets) is **retired**, superseded by the quarterly-audit-note
convention already in live use (docs/notes/audits/programme-audit/) — the 2026-08-08 review already
happened and is correctly recorded there, and that convention is adopted as the standing mechanism
for future quarterly re-confirms of the lifecycle Call-1 sigma-source question, not a second
STATE.md-bullet system running in parallel. §6 gate item 3's own text and §10 hook #6 stay
byte-unedited above (Rule 14/Trap #12) as the historical record of what this ADR originally required;
this ruling is the discharge. No STATE.md row is added by this ruling. This does not touch §2's five
ratified Calls, §4's revert triggers, or any risk-control code — it retires a documentation-bookkeeping
requirement only. [Editorial, 2026-10-15: §6 gate item 3 and §10 hook #6 were removed in the 2026-10-15 retention trim; their original text is in the pre-trim blob (see **Revision**).]
