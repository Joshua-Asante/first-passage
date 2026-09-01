# ADR 2026-07-10 — Strategies are never locked: separate parameter-immutability (LOCKED) from revocable capital-authorization (lifecycle); govern decaying edges by graded de-risk

**Status:** `Accepted` — operator **ratified all five §2 numeric calls as recommended on 2026-07-10** (the day they were proposed). This ADR records a governance-model decision; the five ratified values live in [`docs/methodology/strategy_lifecycle.md`](../methodology/strategy_lifecycle.md) (canonical owner). **Phase-2 status (2026-07-17):** docs + risk_pct wiring + Call-4 control + Call-1 pure logic + ~~`ops/cli.py lots` read-only auth surface~~ are **DONE** (behavior-neutral at all-AUTHORIZED 1.0×). **Superseded 2026-07-22:** the `ops/cli.py lots` surface named above was itself retired by challenge-era substrate Phase 2 ([`docs/adr/2026-07-22-challenge-era-substrate-retirement.md`](2026-07-22-challenge-era-substrate-retirement.md) §2-D) — lifecycle haircuts now live solely in `dd_protection.py`'s risk_pct layer (`scaled_risk = BASE_RISK × DD_SCALE × lifecycle`), with no read-only CLI surface. Call-1 σ-source harness + state writer landed 2026-07-14. **Pine pyramid-parity CONFIRMED-FALLBACK 2026-07-17** ([`Q-PYRPARITY-1` closure](../briefs/closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md)). **Beta-cohesion diagnostic landed 2026-08-23** (report-only: [`lab/research_utils/beta_cohesion.py`](../../lab/research_utils/beta_cohesion.py)). Does not write `lifecycle_state.json`. Not yet `RESOLVED` — a 2026-08-08 live review is not claimed.
**Superseded-by:** none
**Superseded-in-part-by:** `2026-08-07-loop-s5-bounded-promotion-lane.md` — **Call 5** “no autonomous promotion” invariant only (bounded sandbox-up exception: micro size · fixed loss/attempt budget · capped concurrency; operator approves budgets not candidates; ceiling-crossings operator-only). Demotion, retirement GO/NO-GO, RETIRED re-entry bar, and re-optimization bar **stand**.
**Retain-until:** none
**Decision date:** 2026-07-10
**Authors:** Joshua (decision) + Claude (drafter, this session)
**Supersedes:** none. **Refines** the standing "The portfolio and strategies are LOCKED" Key Principle (`CLAUDE.md`) by splitting the word "locked" into its two silent meanings (see §1). Does **not** supersede any allocation, `dd_protection`, or lock-decision ADR — those remain the canonical owners of their constants.
**Related:** `docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md` (the discretion-governance precedent: pre-authorize the one legitimate intervention rather than pretend intervention never happens — this ADR is the *ex-ante* generalization of that *ex-post* move); `docs/adr/2026-06-07-decompound-remc-hold.md` (the regime-split evidence base — the shared-beta regime dependence this ADR's Call 4 monitors); `CLAUDE.md` §Protection (the existing pre-registered decay-style trigger this ADR extends — quarterly C2→C0 revert, rolling-6mo MC-pass <95% for two consecutive windows); `docs/methodology/observation_routing.md` (Closed/Action/Forward — the observation-disposition axis, *orthogonal* to the authorization axis added here); `docs/methodology/regime_robustness_gate.md`; `docs/rejected_candidates.md` / `docs/methodology/rejected_signals.md` (re-proposal requires new mechanism / dated incident, not new parameters — the doctrinal parent of §5's "decay is never a re-optimization trigger"); the Q-MECH-1 family finding (one shared long-continuation beta across all four legs; NY-morning entry; 2023–26 trend era; zero free external monitors — the load-bearing premise, carried in memory/session, not re-derived here).
**Layer:** methodology + operational (governance model for capital authorization over a strategy's life; a new sizing *factor*). **Not** strategy/risk-control parameters — no SL/TP/ATR/risk%/pyramid/session/BE/trail constant, no `dd_protection` constant, no allocation, no Pine source is touched by this ADR. The locked MC anchor (99.83/0.17/4.37) is untouched and needs no re-MC.

---

## §0 — Rule 0 reads (production/source verification)

Read this session **via local filesystem (working-tree bytes on 2026-07-10)**. Constant-carrying reads are additionally commit-anchored where a hash is in hand; the doctrine anchors below are the in-file curation dates each document carries, per the brief-authoring §0 sub-rule allowing a `last-modified`/curation anchor when a commit hash is not in hand. This ADR touches **no** risk-control code; the §0 reads exist to (a) prove that, (b) anchor the existing-doctrine hooks this ADR extends rather than reinvents, and (c) — added this revision — ground the sizing-composition mechanism (Call 2) against the *actual* code paths instead of an assumed unified product.

- `CLAUDE.md` — read 2026-07-10; internal live-execution posture dated **2026-07-06**. Confirms: the four LOCKED strategies + their risk%/versions (G 0.34% v5.5 / DJ30 0.70% pyr750 v4.5 / Aegis 1.50% v4.3 / NAS100 0.37% pyr1000 v1); the sizing formula `multiplier = (account_balance × account_risk_pct) / (200,000 × baseline_risk_pct)` with **always round down, never up**; the MC anchor **99.83/0.17/4.37**; and — load-bearing for this ADR — the **existing pre-registered decay-style trigger** in §Protection: *"if rolling 6-month MC pass-rate falls below 95% for two consecutive 6-month windows, revert to C0,"* run via `python lab/analysis/time_to_pass.py --regime-check`, next dates **2026-08-08 → 2026-11-08 → 2027-02-08 → 2027-05-08**. Also confirms the "The portfolio and strategies are LOCKED" Key Principle this ADR refines, and that `params.toml` is a derived mirror (Pine + `dd_protection.py`/`firm_rules.py` canonical).
- `core/dd_protection.py` — read 2026-07-10 (last-touching commit `6f5480bf`, 2026-07-06). **Finding (load-bearing for Call 2):** dd_protection scales **`risk_pct`**, not lots — `calculate_protection` returns `scaled_risk = {k: base_risk × multiplier}` where `multiplier ∈ {1.0, DD_SCALE=0.40}` (line 112; `DD_SCALE`, `DD_TRIGGER=0.015`, and the `BASE_RISK` allocation dict at lines 53/64). It is a **standalone morning tool**: the operator runs `python dd_protection.py <equity>`, reads the scaled `risk_pct`, and types it into the TradingView strategy input, where Pine then sizes the $200K-baseline lots. dd_protection **does not import, call, or feed** the account-multiplier path.
- `ops/accounts.py` + `ops/cli.py` — read 2026-07-10 (last-touching commit `6f5480bf`, 2026-07-06). **Finding (load-bearing for Call 2):** `calc_multiplier` (accounts.py:308) computes the **account-scaling** multiplier `(balance × tier_risk) / (200,000 × baseline_risk)`, `math.floor`-ed to 2 dp (the "never round up" invariant, line 328). `cmd_lots` (cli.py:157–174) calls only `get_multipliers` → `calc_multiplier` and prints *"Multiply indicator lot size by account multiplier."* **Neither references dd_protection.** ⇒ **The two size-affecting scalars live in two independent layers that never meet in one expression** — `dd_protection_factor` at the risk_pct layer (inside TV), `account multiplier` at the post-Pine account-scaling layer (outside TV). This **corrects an earlier draft of this ADR**, which assumed a single unified `final_lots = base_multiplier × dd_protection_factor × …` product and framed the only open question as "`min()` vs product." That framing was malformed: there is no combining point to be `min()` or product. Call 2 is rewritten accordingly.
- `docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md` — read 2026-07-10; `Accepted` 2026-06-30. The precedent: the operator removed himself as the execution layer after a **−$4,188.85 / 2-day / 100%-off-spec** discretionary episode against flat systems. Its §5 forbidden-moves ("no recovery exception"; "fire the trigger openly (supersede) or hold — don't loosen in place") are inherited near-verbatim into §5 here. Its structural lesson — *pre-authorize the single legitimate intervention so it cannot mutate into ad-hoc discretion* — is exactly what this ADR does for decay-driven de-risk. **Also load-bearing for Call 5:** it establishes that **no autonomous execution rail exists today** (manual trading retired; the identified CrossTrade/NT8/Rithmic rail unbuilt; R6 GO/NO-GO not made).
- `docs/methodology/observation_routing.md` — read 2026-07-10; established 2026-04-25, Active. Confirms the Closed/Action/Forward gate is an **observation-disposition** axis (what to do with a finding), which does **not** collide with the **authorization-lifecycle** axis added here (what capital a strategy is cleared to hold). Its discipline — *"permission to look is not permission to act; Action requires a triggering rule, observation alone never lands there"* — is the direct parent of §2 Call 1's "surveillance is scheduled measurement, not continuous discretionary staring."
- `CLAUDE.md` §Protection + the regime caveat block (read 2026-07-10) — the decompound full-history re-MC (`docs/adr/2026-06-07-decompound-remc-hold.md`, summarized in `CLAUDE.md`) shows the shared beta is **regime-split**: 2020–23 chop bust ~9–13% / p99 ~7.5% vs 2023–26 trend bust ~0% / p99 ~3–4%; clean-vintage locked-config H1 bust **13.84%**; both lock gates breach on decompounded full history (98.53% / 1.47% / 5.32%). This is the pre-existing **"what beta-death looks like" dataset** that makes Call 4 pre-registerable *now* rather than after the fact.
- `C:/Users/joshu/.claude/skills/brief-authoring/SKILL.md` — read 2026-07-10. The six discipline checks + the ceremonial-section traps this ADR is written against.

**Not read this session (relied on as summarized in the above / in memory, not as primary source):** the Q-MECH-1 closure artifact; `ops/live_journal/scripts/ecr_rolling.py` internals (Call 1 names ECR as a *confirming* metric, not a tripping one — its exact rolling window is a Phase-2 build detail). Consequence: the §7 step that wires the `lifecycle_multiplier` into the risk_pct layer remains **Rule-0-at-build for the exact diff** — but, unlike the earlier draft, the *architecture* is now verified (§0 reads above), so the open build item is narrow: **Pine pyramid-nonlinearity parity** of the compounded risk_pct haircut (DJ30 750% / NAS100 1000%), plus the axis-separation pin. This ADR proposes the *model* and the *integration layer*; the diff lands in Phase 2.

---

## §1 — Context

Four conversation-level findings force a governance change:

1. **Edges decay; "consistent over time" is not verifiable, only not-yet-falsified.** Every busted quant strategy was significant, non-random, and consistent — until it wasn't. An unexplained edge in particular carries *no prior on durability*: when it degrades, the first evidence is losses (an explained edge often telegraphs its death — the roll changed, the fix moved, a competitor arrived). So a live strategy is a **decaying asset of unknown half-life**, not a permanent fact.

2. **Therefore no strategy can be "locked" in the sense of *authorized to hold capital indefinitely*.** But the word "LOCKED" in this repo has been doing **two jobs at once**: (a) *parameters are immutable* — an anti-overfitting promise to self, and (b) *this earns capital indefinitely* — a durability claim about the future. Finding 1 kills only (b). Job (a) should get **stronger**, not weaker. The fix is not to rename "LOCKED" (it already means (a), correctly, everywhere in the repo — renaming is pure churn). The fix is to make **authorization** — the thing (b) was silently asserting — an **explicit, separate, always-revocable axis** that was previously bundled into "LOCKED" and into the static MC anchor.

3. **Commitment migrates from the strategy to the lifecycle that governs it.** You stop freezing the *answer* (indefinite authorization) and start freezing the *procedure that decides when the answer expires*. Everything about *how you decide to pull capital* gets locked harder than any parameter ever was. This is the only way "never locked" (authorization) coexists with "locked" (parameters) without contradiction — they are different axes.

4. **The repo already does a version of this and already has the beta-death dataset.** §Protection's C2→C0 revert is a pre-registered, two-consecutive-window, MC-pass-based decay trigger — this ADR generalizes that one instance into a standing model. And the 2026-06-07 regime HOLD already quantified the shared beta's regime dependence (the 2020–23 chop half is the adverse-regime training set). This ADR is an **extension of existing patterns**, gated by The Algorithm (Question → Delete → Simplify → Accelerate): it adds one axis and reuses the quarterly regime-check cadence rather than standing up a parallel framework.

**The premise that makes Call 4 the priority:** Q-MECH-1 found all four legs express **one** long-continuation beta. Decay may therefore arrive **portfolio-wide in a single regime shift**, not leg-by-leg — four simultaneous drawdowns could be the shared beta dying, not coincidence. Renaissance could ignore explanation because *breadth* (thousands of uncorrelated weak bets) was its significance-and-survival machine; at n≈hundreds/yr and one shared beta, that insurance is structurally absent. This is the operation's **stated largest structural exposure** (the monitor gap), and it is why Call 4 sequences first.

**Decision driver (one sentence):** because live edges decay and "consistent over time" can only be disproven (never confirmed), capital authorization must be an explicit, always-revocable, graded axis governed by pre-registered triggers — while strategy parameters stay LOCKED harder than before — so that decay is met by a cheap reversible de-risk fired by a rule, not by the in-the-moment discretion that produced the −$4,188.85 receipt.

---

## §2 — Decision

**Meta-decision.** Split the overloaded "LOCKED" into two orthogonal axes and add the second as first-class state:

- **Parameter axis — `LOCKED` (unchanged meaning, strengthened enforcement):** every SL/TP/ATR/risk%/pyramid/session/BE/trail constant + Pine source is immutable. Retained verbatim; no rename. Decay **never** authorizes editing these (§5).
- **Authorization axis — NEW, explicit lifecycle:** `CANDIDATE → AUTHORIZED → WATCH → RETIRED`, plus a **durability-source tag** `{MECHANISM | SURVIVAL-ONLY}` that selects the surveillance regime. A live strategy is now described by *both* axes, e.g. **"Guardian v5.5 · LOCKED · AUTHORIZED · MECHANISM."** "Locked but never locked" ceases to be a paradox: LOCKED was only ever about parameters; authorization is the axis that is always live and revocable. The 99.83/0.17/4.37 allocation is, under this model, an **AUTHORIZED-state fact whose inputs are LOCKED** — not a permanent guarantee. (And because the lifecycle multiplier only ever *reduces* size, any WATCH-active book is strictly lower-risk than this AUTHORIZED-state config — the bust/DD gates move only safe-side, so a de-risk never requires a re-MC.)

This axis is **orthogonal** to `dd_protection` (intra-challenge drawdown, this account, this window) and to observation-routing Closed/Action/Forward (finding disposition). It composes with them; it replaces neither.

The five judgment calls below are the substance. Each states what is **DETERMINED** (structure/direction — not the operator's to re-litigate), the **RECOMMENDED** starting value (anchored to existing repo patterns), and the **OPERATOR-RATIFIES** hook (the free parameter no computation can set — a risk/regret preference).

---

### Call 1 — Decay-detection threshold (the Type-I/Type-II regret preference)

**DETERMINED.** A live edge in a normal drawdown and a dead edge are *statistically indistinguishable in the window where you must act*. So this is not a detection rule you can make "correct" — it is a **regret preference** set in advance and in writing (the −$4,188.85 episode is the archive evidence of what setting it in-the-moment produces). It must have the same **structural shape as the existing §Protection revert trigger**: a rolling metric vs a pre-registered floor, requiring **persistence** (≥2 consecutive readings) so a single drawdown cannot trip it. Its action is **de-risk (→ WATCH), never kill** — which is what makes an aggressive/early setting affordable (see interlock note).

**Interlock with Call 2 (the key move).** Because the response is graded, reversible sizing (Call 2), a false positive costs only *one size step*, not a killed edge. Therefore the threshold should be set **tight/early**, biased toward Type-I (de-risk a live edge too soon) over Type-II (feed a dead one too long) — the opposite of what you'd choose if the trigger killed the strategy. The terror of the binary dissolves once the action is cheap.

**RECOMMENDED starting value (anchored to §Protection's 95%/two-window pattern + `baselines.md` PF distribution + `regime_robustness_gate` half-split logic):**
- **Metric:** rolling live **PF vs its MC/backtest baseline** (per-strategy baseline in `.claude/skills/trade-csv-reconcile/references/baselines.md`), evaluated at each scheduled review. (ECR from `ops/live_journal/scripts/ecr_rolling.py` is the *confirming* metric but accrues too slowly for the add-cohort per Q-NAS-ECR-1 — it corroborates, it does not trip.)
- **Floor:** rolling live PF below **[baseline PF − 1.0σ of the MC PF distribution]** for **two consecutive** review windows → demote one authorization tier (→ WATCH-1).
- **σ and window length** are the regret dials. Recommended window = the review cadence in Call 3; recommended σ = 1.0 (tighter than the 2σ a kill-trigger would use, *because* the action is reversible).

**Provisional-until-data caveat.** With manual trading retired and the automated rail unbuilt (§0, live posture), live per-strategy PF may not accrue to a minimum trade count for a long time. Ratifying σ/window now is **pre-registration against future data**, not a threshold that is live-evaluable at the first (2026-08-08) check — §6's AMBIGUOUS clause governs that case, and the numeric floors re-confirm at 2026-11-08 if the count is short.

> **OPERATOR-RATIFIES:** the σ multiple (recommend 1.0), the window length, and the consecutive-window count (recommend 2). Committed to `docs/methodology/strategy_lifecycle.md` on ratification.

---

### Call 2 — Sizing as the response variable (stepped, not smooth)

**DETERMINED.** The escape from the binary is to make authorization **continuous in effect but discrete in mechanism**: size becomes a function of durability confidence, so no single decay reading ever bets the strategy's life — it nudges an allocation. The tiers are **stepped, not a smooth curve**: a smooth `size = f(confidence)` invites continuous discretionary micro-adjustment, which is the tinkering failure mode wearing a lab coat. Steps are auditable.

**Mechanism (corrected against production, §0 — supersedes the earlier draft's unified-product claim).** There is **no single sizing product** in the code. Size is set across **two independent layers** that never meet in one expression:

- **risk_pct layer** — [`core/dd_protection.py`](core/dd_protection.py) scales each strategy's `risk_pct` (the value typed into TradingView; Pine then sizes the $200K-baseline lots from it). This is where `DD_SCALE` (0.40×) already lives.
- **account-multiplier layer** — [`ops/accounts.py`](ops/accounts.py) `calc_multiplier` scales the baseline lot output to the actual account balance, floored to 2 dp. Orthogonal to the risk_pct layer; unaffected by dd_protection.

The lifecycle multiplier is a **per-strategy risk-authorization haircut** and lands at the **risk_pct layer, compounding multiplicatively with `DD_SCALE`** — i.e. the risk_pct set each morning becomes:

```
risk_pct_live[strategy] = BASE_RISK[strategy] × DD_SCALE × lifecycle_multiplier[strategy]
```

Rationale: (i) it co-locates with the existing dd_protection tool and reuses the operator's existing morning workflow (one knob, already in the loop); (ii) it keeps `calc_multiplier` a pure account-scaling ratio — single responsibility, no authorization state leaking into the reference card; (iii) multiplicative compounding is the *intended* semantics — a strategy that is **both** decaying (WATCH-1, 0.50×) **and** in portfolio drawdown (`DD_SCALE`, 0.40×) sizes to **0.20×** risk_pct, which is correct (two independent signals each say de-risk, so they stack). Because Pine lot-sizing is ~linear in risk_pct, this placement is ~mathematically equivalent to an account-multiplier-layer placement; the choice is **operational**, and the one build-time check is **Pine pyramid-nonlinearity parity** (DJ30 750% / NAS100 1000% may not scale exactly linearly with the base risk_pct).

**Axis-separation (the load-bearing invariant).** Implementation adds a per-strategy authorization scalar to dd_protection's `scaled_risk` computation **without altering `BASE_RISK`, `DD_SCALE`, or `DD_TRIGGER`** (they stay byte-identical; the new factor multiplies them at compute time, it does not edit them). The §4-trigger-3 / §10-hook-5 axis-separation test pins exactly that: a lifecycle tier change must leave every locked constant untouched. The lifecycle factor is a pure authorization scalar; round-down/never-up is preserved at `calc_multiplier`.

**RECOMMENDED starting value (4 tiers):**

| Tier | Lifecycle multiplier | Meaning |
|---|---|---|
| `AUTHORIZED` | **1.00×** | full durability confidence |
| `WATCH-1` | **0.50×** | one decay trigger fired; degrading |
| `WATCH-2` | **0.25×** | second trigger / deeper degradation |
| `RETIRED` | **0.00×** | capital withdrawn; authorization revoked |

Tier boundaries are set by Call 1's trigger firing (AUTHORIZED→WATCH-1) and a second firing / deeper floor breach (WATCH-1→WATCH-2). WATCH-2→RETIRED is the one irreversible edge and is operator-gated (Call 5).

> **OPERATOR-RATIFIES:** tier count (recommend 4); the multiplier ladder (recommend 1.0/0.5/0.25/0); the **integration layer + compounding rule** (recommend: risk_pct layer, multiplicative with `DD_SCALE`); and confirmation that a WATCH-1 strategy simultaneously in DD sizing to **0.20×** is intended. Committed to `strategy_lifecycle.md`.

---

### Call 3 — The explained/unexplained differential (pricing the dropped explanation-filter)

**DETERMINED.** Dropping the explanation requirement does not make a signal cheaper — it moves the invoice from the "mechanism" line to the "statistics + surveillance" line, and **the bar must rise to pay it**. Direction is fixed: `SURVIVAL-ONLY ⟹ smaller starting size, faster review, tighter trigger` than `MECHANISM`. The **durability-source tag** is what carries this: it selects the surveillance regime. Magnitudes are the operator's call.

**RECOMMENDED starting differential:**
- **Starting tier:** `MECHANISM` strategies may enter at `AUTHORIZED` (1.0×). `SURVIVAL-ONLY` strategies enter one tier down at `WATCH-1` (0.5×) and may promote to `AUTHORIZED` **only** after surviving a pre-registered out-of-sample interval (recommend: **one full regime-check cycle AND ≥ a minimum live trade count**), committed before go-live. (This is the "raised significance bar" from the doctrine, priced as a size haircut + a survival gate.)
- **Review cadence:** `SURVIVAL-ONLY` reviewed at **2× the MECHANISM cadence** (i.e. the quarterly regime check *plus* one interim). `MECHANISM` at the standard quarterly regime-check dates.
- **Trigger tightness:** `SURVIVAL-ONLY`'s Call-1 floor acts on **one** window (not two).

**Portfolio nuance (load-bearing).** All four *current* legs are mechanism-adjacent, but Q-MECH-1 says they share **one** beta — so at portfolio level the durability-source question is really about *the beta*, not each leg. The per-leg `SURVIVAL-ONLY` regime therefore bites hardest on **new** additions: the residual-program lanes (R5 DJ30/MYM edition, Aegis→6J, Guardian-MGC/R7) and — the reason this matters now — **any unexplained signal minted by the new discovery stack** (STUMPY/PySR/matrix-profile candidates). Those enter `SURVIVAL-ONLY` by default and pay the full differential. (This is also why the per-leg tier apparatus can be *built* later than the beta monitor — see §7 scope note.)

> **OPERATOR-RATIFIES:** the starting-tier haircut (recommend one tier), the OOS promotion gate (recommend one regime cycle + min trade count), the cadence multiple (recommend 2×), and the one-vs-two-window tightness. Committed to `strategy_lifecycle.md`.

---

### Call 4 — The beta-level trigger (the portfolio killer) — SEQUENCE FIRST

**DETERMINED.** Because the four legs are one beta, decay can arrive **portfolio-wide at once**; correlated simultaneous degradation is the signature of the *shared beta dying*, categorically different from one leg drifting. This is the only **portfolio-fatal** call and it is structurally **low-n** (possibly zero calibration events before the real one) — so it must be pre-registered from the **existing regime-split evidence** (the 2026-06-07 decompound HOLD's 2020–23 adverse half), not calibrated after the fact, and its action must be the **most conservative** (graded portfolio-wide de-risk + **mandatory operator GO/NO-GO**, not silent full kill). It is an **extension of the existing quarterly regime trigger** (next 2026-08-08), not a new monitor.

**RECOMMENDED starting value (two-tier, mirroring the two-window persistence pattern):**
- **Soft flag (raise to interim review):** **2 of 4** legs simultaneously in `WATCH` within one regime-check window → pull the next review forward; run the transfer-entropy / lead-lag coupling check across the four legs + parents (the beta-cohesion monitor proposed in session).
- **Beta-death trigger (act):** **3 of 4** legs simultaneously in `WATCH` within one regime-check window → **portfolio-wide de-risk to 0.50×** (apply a beta-level lifecycle multiplier across all legs) **AND** raise a **mandatory operator GO/NO-GO** on full shared-beta shutdown. Autonomous action stops at the 0.5× de-risk; going to zero is operator-confirmed (Call 5).
- **First evaluation:** the **2026-08-08** regime check, reusing `time_to_pass.py --regime-check` plus a new beta-cohesion read.

Rationale for 3-of-4 as the act line: 2-of-4 is plausibly coincidental even in a shared-beta book; 3-of-4 simultaneous is strong correlated-degradation evidence. The soft 2-of-4 flag buys an early look without over-triggering.

> **OPERATOR-RATIFIES:** the soft-flag count (recommend 2/4), the act count (recommend 3/4), the de-risk depth (recommend 0.5×), and confirmation that full beta shutdown is operator-GO/NO-GO. Committed to `strategy_lifecycle.md` + registered on the STATE.md forward-trigger board.

---

### Call 5 — The automation boundary (what fires without the operator)

**DETERMINED.** Continuous surveillance + revocable capital forces the question of what acts autonomously. The boundary is **reversibility**, and it inherits the repo's existing asymmetry (`dd_protection` already *computes* 0.40× with no sign-off; sizing always rounds **down, never up**):

**Rail caveat (§0, live posture) — read first.** **No autonomous execution rail exists today.** Manual trading is retired, dd_protection's 0.40× is *computed by a tool and typed into TradingView by the operator*, and the identified CrossTrade/NT8/Rithmic rail is unbuilt (R6 GO/NO-GO not made). Call 5 therefore **pre-registers the automation policy that binds the future rail**; until it is built, every de-risk is operator-applied and "autonomous / fires without the operator" means **"rules-mandated, no fresh in-the-moment judgment,"** not "machine-executed." The distinction is doctrinal, not implementation status.

- **Reversible de-risk → autonomous, rules-based** (in the "rules-mandated" sense above). Tier demotions (AUTHORIZED→WATCH-1→WATCH-2), Call-1 firings, and the Call-4 **soft flag + 0.5× beta de-risk** fire without fresh operator judgment. Cheap to be wrong, expensive to hesitate.
- **Irreversible retirement → operator-confirmed against pre-registered criteria.** WATCH-2→`RETIRED` (capital to zero) and **full beta shutdown** require an operator GO/NO-GO — but the operator's role is **verification of pre-registered criteria**, not fresh judgment at maximum emotional load (this mirrors the R6 GO/NO-GO pattern).
- **Hard asymmetry (the load-bearing constraint):** automation may move authorization **down** only. It may **never** promote a tier, re-enter a RETIRED strategy, increase size beyond the authorized tier, or re-optimize — those are all operator-ratified, always. Automate the protective direction; gate every risk-adding direction. (Direct analogue of "always round down, never up.")

**RECOMMENDED:** adopt as written above; the only operator input is confirming the two operator-gated events (WATCH-2→RETIRED; full beta shutdown) and that **no** autonomous size-up path exists anywhere.

> **OPERATOR-RATIFIES:** confirmation of the two GO/NO-GO events and the no-autonomous-promotion invariant. Committed to `strategy_lifecycle.md`.

#### Addendum 2026-08-07 — Call 5 superseded in part by S5 bounded promotion lane

**Status:** binding on Accept of [`2026-08-07-loop-s5-bounded-promotion-lane.md`](2026-08-07-loop-s5-bounded-promotion-lane.md). Historical Call 5 body above is **frozen**; this addendum is the operative amendment.

Call 5’s absolute “no autonomous promotion” invariant gains **exactly one** bounded up-exception: automation may admit a gate-validated candidate into a capped sandbox (micro size · fixed per-candidate loss/attempt budget · capped concurrency) when the promotion packet Passes the S5 validator + refuter. The operator approves **budgets**, not candidates; every ceiling-crossing remains operator-only; demotion remains universal and instant. RETIRED re-entry, re-optimization, full AUTHORIZED size-up, and unattended-loop authorization are **not** granted by this addendum. Canonical values / wording live in [`strategy_lifecycle.md`](../methodology/strategy_lifecycle.md) Call 5.

---

### Status vocabulary (the update to make "never locked" legible)

Add to `CLAUDE.md` **outside** the `## Strategy Reference (LOCKED — do not modify)` table, and make `docs/methodology/strategy_lifecycle.md` the canonical owner:

- **Parameter axis:** `LOCKED` (unchanged — immutable parameters/Pine; the Key Principle keeps its word).
- **Authorization axis:** `CANDIDATE → AUTHORIZED → WATCH{-1,-2} → RETIRED`, each with a fixed lifecycle multiplier (Call 2).
- **Durability-source tag:** `{MECHANISM | SURVIVAL-ONLY}` (Call 3), sets the surveillance regime.
- A strategy's live descriptor is the triple **`<version> · LOCKED · <authorization> · <durability-source>`**.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Keep the binary lock (LOCKED ⇒ permanent authorization)** | Contradicts the decaying-asset reality (§1). Leaves only "hold or panic-kill" when an edge dies — which *is* the in-the-moment discretion that produced the −$4,188.85 receipt. No graded response = the failure mode re-imported. |
| **Rename `LOCKED` → `FROZEN` repo-wide, add lifecycle** (my earlier session proposal) | Pure process-gravity. "LOCKED" already means parameter-immutability *everywhere* in the repo + the whole lock-decision-brief apparatus. Renaming is churn for zero conceptual gain. The actual gap is an *added* authorization axis, not a relabel — so add the axis and leave LOCKED alone. |
| **Unified sizing product** `final_lots = base_mult × dd_factor × lifecycle × indicator_lots` (an earlier draft of Call 2) | **Falsified by §0 production reads.** No such product exists: `dd_protection` scales `risk_pct` (inside TV) and `calc_multiplier` scales the account (outside TV); they never meet in code. The "`min()` vs product" question was malformed. Corrected: lifecycle lands at the risk_pct layer, multiplicative with `DD_SCALE` (Call 2). Kept in this table as the concrete anti-pattern (precision exceeding grounding). |
| **Continuous smooth sizing curve** `size = f(confidence)` | Mathematically neat, operationally corrosive: a smooth curve invites continuous discretionary micro-adjustment (tinkering in a lab coat). Stepped tiers are auditable and cannot be nudged between steps without an explicit, logged tier change. |
| **Kill-only: binary AUTHORIZED/RETIRED, no WATCH tiers** | Forces the terrifying binary in exactly the window where live-vs-dying is statistically indistinguishable. Graded sizing is the *only* escape from that binary and the thing that lets Call 1's trigger be set tight/cheap. Removing tiers removes the interlock. |
| **Leave decay handling to in-the-moment operator discretion** | This is the −$4,188.85 failure mode by definition. The entire point is pre-registration (§0 precedent 2026-06-30). A "we'll judge it when we see it" policy is the anti-policy. |
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

**Trigger check schedule:** at each quarterly programme audit / regime trigger — next **2026-08-08**, then 2026-11-08, 2027-02-08, 2027-05-08 — plus event-driven for trigger 3.

---

## §5 — Forbidden moves (the "locked-harder" column)

These are the commitments that get locked *tighter* than any parameter, so that "living authorization" cannot decay into "fiddling." Each was genuinely tempting in-session (passes the brief-authoring check-3 test: removing it changes behavior).

- **Decay is never a re-optimization trigger.** A decayed strategy is retired to zero; it is **not** re-fit. Re-fitting a fading edge is overfitting with extra steps — tuning a corpse. Any replacement is a **new hypothesis with fresh K-accounting and fresh out-of-sample**, not a "tuned version" of the dead one. (Direct inheritance of `rejected_candidates.md` / `rejected_signals.md`: re-proposal requires new *mechanism* / dated incident, not new *parameters*.)
- **Decay/kill thresholds are themselves LOCKED at authorization.** You may revoke a strategy's capital; you may **not** move the line that triggers revocation once it is live. This is the meta-lock, and it directly answers the programme-audit degeneration signal (falsifier drift toward "we'd never hit this"). Approaching a threshold is not license to move it.
- **Surveillance is scheduled measurement against pre-set thresholds — not continuous discretionary staring at P&L.** The whole risk of un-locking is that you are now *permitted* to look, and permission to look becomes permission to meddle. You look **on cadence**, against criteria fixed in advance, and the only permitted outputs are the fixed menu {hold / de-risk one tier / retire}. No threshold-editing in the moment, no re-fit, no fifth option invented under drawdown stress. (Inherits `observation_routing.md`: Action requires a triggering rule; observation alone never lands there.)
- **No autonomous size-up, ever.** Automation may move authorization **down** only. It may never promote a tier, re-enter a RETIRED strategy, or increase size beyond the authorized tier. (Analogue of "always round down, never up.")
- **No loosening a trigger in place because a drawdown got uncomfortable.** "We wished we were still earning, so we lowered the bar" is methodology-layer `p`-hacking. The discomfort *is* the named cost (§6); fire the trigger openly (supersede) or hold. (Verbatim posture from 2026-06-30 §5.)
- **The lifecycle multiplier is forbidden from touching any LOCKED strategy parameter.** It is a pure authorization scalar in the risk_pct computation; it may not change any SL/TP/ATR/risk%/pyramid/session/BE/trail constant, and it must multiply against `BASE_RISK`/`DD_SCALE`/`DD_TRIGGER` rather than edit them. A "while we're wiring lifecycle, let's tweak X" is a separate lock decision with its own MC re-validation. (§4 trigger 3 makes a violation an integrity failure.)

---

## §6 — Gate (binary closure criteria)

This ADR is `Proposed`. It becomes **`Accepted` / RESOLVED** when **all** hold:
1. The five §2 calls have **ratified numeric values committed** to `docs/methodology/strategy_lifecycle.md` (σ+windows for Call 1; tier ladder + integration-layer/compounding rule for Call 2; the four differential magnitudes for Call 3; the 2/4 + 3/4 + 0.5× for Call 4; the two GO/NO-GO events + no-autonomous-promotion invariant for Call 5).
2. The **authorization-axis vocabulary** is added to `CLAUDE.md` **outside** the LOCKED table (verifiable by grep, §10).
3. The STATE.md **forward-trigger board** gains two entries — per-strategy decay review and the beta-death review (Call 4) — each pointing at `strategy_lifecycle.md` as owner, first evaluation **2026-08-08**.

**Ratification status (2026-07-10):** the operator-owed input — the five §2 calls — is **RATIFIED as recommended** (values enumerated in the change history). Gate items 1–3 above are the remaining *implementation* follow-through (Phase 2/3); until they land, this ADR is `Accepted` (decision made) but not yet `RESOLVED` (implemented).

**FALSIFIED / re-open** per any §4 trigger. **AMBIGUOUS** if, at the 2026-08-08 first evaluation, the Call-1 metric has < the minimum trade count to compute a rolling PF for ≥2 legs — in which case the calls' *structure* stands but the numeric floors are provisional and re-confirmed at 2026-11-08 (recorded, not silently amended).

---

## §7 — Implementation plan

Policy + one sizing-factor addition. No risk-control *constant* changes.

- **Phase 0** — §0 reads verified this session (no locked source touched; existing decay-trigger + regime-split evidence confirmed as the extension points; **sizing architecture verified** — two independent layers, lifecycle lands at the risk_pct layer, correcting the earlier unified-product assumption).
- **Phase 1 — operator ratifies the five §2 numeric calls** (Call 2 now also confirms the integration layer + compounding rule). Until then this ADR stays `Proposed`. (This is the operator-owed step the whole ADR exists to surface.)
- **Phase 2 (on ratification)** —
  - Create `docs/methodology/strategy_lifecycle.md` as the **canonical owner** of the two axes, the tier ladder, the durability-source regimes, and the five ratified values.
  - Add the authorization-axis note to `CLAUDE.md` (outside the LOCKED table).
  - **Rule-0-at-build (now narrow):** wire the per-strategy `lifecycle_multiplier` into the **risk_pct layer** — i.e. into `dd_protection.py`'s `scaled_risk` computation as `BASE_RISK[k] × DD_SCALE × lifecycle_multiplier[k]` — **without altering `BASE_RISK`, `DD_SCALE`, or `DD_TRIGGER`** (byte-identical; the MVD spec-pin at `dd_protection.py:176/181` must still pass). **Addendum 2026-08-06 (C20):** the pin is the literals `if DD_TRIGGER != 0.015:` / `if DD_SCALE != 0.40:` (currently ~L292/L297) — line numbers in the preceding clause are historical; do not treat 176/181 as current. Verify **Pine pyramid-nonlinearity parity** for DJ30 (750%) / NAS100 (1000%): confirm scaling the input risk_pct scales the whole pyramided stack proportionally (if it does not, the haircut must be applied at the account-multiplier layer instead — the operational fallback). Add a test pinning axis-separation (a lifecycle tier change must not alter any Pine/`params.toml`/`dd_protection` constant).
  - Extend the decay metric: a read-only rolling-PF-vs-baseline check (reusing `baselines.md` + `ecr_rolling.py` outputs) that emits the Call-1 tier-demotion signal.
- **Phase 3** — STATE.md forward-trigger entries (per-strategy decay review + beta-death review, first eval 2026-08-08 alongside the existing regime check); memory (`project_strategy_lifecycle_governance` recall hook + `MEMORY.md` line); `docs/SESSIONS.md` entry at wrap-up.
- **Scope note (Delete-until-needed).** All four current legs are one mechanism-adjacent beta, so the **per-leg tier apparatus is largely inert for today's book** — Call 4 (beta-level) is what actually bites. Phase 2 may ship the **beta-cohesion monitor + the risk_pct lifecycle hook (default AUTHORIZED/1.0×) only**, deferring the full per-strategy tier state-machine/UI until the first `SURVIVAL-ONLY` addition (a residual-program lane or a discovery-stack candidate) actually needs it. Build the per-leg framework when it has a customer; do not gold-plate a four-leg one-beta book. (The §6 forward-board *reviews* still register on cadence regardless — a review date is not the tier machinery.)
- **Sequencing (operator-stated priority):** build **Call 4 (beta-death monitor) first** — it defends existing capital and maps to the stated largest structural exposure. The transfer-entropy/lead-lag beta-cohesion read is the concrete first artifact, evaluated at 2026-08-08.

---

## §10 — Audit hooks (runnable)

```bash
cd "C:/Users/joshu/multi_firm_operations"

# 1. This ADR changes NO locked constant — manifest byte-untouched by it.
git diff --stat HEAD -- core/config/params.toml core/dd_protection.py core/firm_rules.py
# Expected under this ADR (pre-Phase-2): empty. (Post-Phase-2, dd_protection.py
# gains the lifecycle FACTOR, but BASE_RISK/DD_SCALE/DD_TRIGGER stay byte-identical —
# verified by hook 5 + the MVD spec-pin literals `if DD_TRIGGER != 0.015:` /
# `if DD_SCALE != 0.40:` in core/dd_protection.py (currently ~L292/L297).
# HOOK REPAIRED 2026-08-06 (claim-alignment C20): prior comment cited
# dd_protection.py:176/181 — those lines now hold `_validate_state`'s multiplier
# guard; the pin itself still passes. Cite by literal so the hook cannot re-stale.)

# 2. The locked MC anchor is unchanged (no re-MC under this ADR).
grep -n "99.83\|0.17\|4.37" core/config/params.toml
# Expected: the [mc_anchor_pepperstone] lines, unchanged.

# 3. (Post-Phase-2) Authorization-axis note lands OUTSIDE the LOCKED table.
#    Use DISTINCTIVE compound tokens: a bare grep for RETIRED/WATCH/AUTHORIZED also hits
#    pre-existing unrelated prose (e.g. "Q-SWAP domain RETIRED" at CLAUDE.md:63, inside the
#    LOCKED table) — Trap M-AHF (match the stored token, not the English word).
grep -n "Strategy Authorization Lifecycle\|durability tag\|risk_pct-layer" CLAUDE.md
# Expected: matches only at/after the "## Strategy Authorization Lifecycle" section (~L82+)
# and the Key Principle refinement (~L238); NONE inside "## Strategy Reference (LOCKED — do
# not modify)" (L49-81).

# 4. (Post-Phase-2) The five ratified values are present in the canonical owner.
grep -nE "sigma|window|WATCH-1|WATCH-2|SURVIVAL-ONLY|MECHANISM|2 of 4|3 of 4|GO/NO-GO|risk_pct layer" docs/methodology/strategy_lifecycle.md
# Expected: Call-1..5 ratified values (incl. Call-2 integration layer), each present.

# 5. Axis-separation invariant (the §4-trigger-3 integrity check) has a pinning test.
grep -rn "lifecycle" tests/ | grep -i "param\|lock\|separation\|base_risk\|dd_scale"
# Expected (post-Phase-2): a test asserting a tier change alters no locked constant.

# 6. Beta-death + per-strategy decay reviews are on the forward board, first eval 08-08.
grep -n "decay review\|beta-death\|strategy_lifecycle" STATE.md
# Expected (post-Phase-3): two entries, owner = strategy_lifecycle.md, next 2026-08-08.

# 7. Existing regime check remains the cadence carrier (reused, not duplicated).
grep -n "regime-check\|2026-08-08" CLAUDE.md STATE.md
# Expected: the existing quarterly trigger dates, now also carrying the decay reviews.

# §4 trigger reminder — next programme audit / regime check: 2026-08-08.
```

---

## Verification

```bash
# Brief-authoring discipline (mechanical) — their standard ADR gate.
python "C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py" \
  docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md --type adr
# Expected: all 6 checks PASS.

# No risk-control source touched by this ADR (proposed state).
git diff --stat HEAD -- core/ | grep -E "dd_protection|firm_rules|params.toml" || echo "none (expected)"

# Sizing-architecture claims in §0/Call 2 match production (the finding that drove the revision).
grep -n "scaled_risk\|DD_SCALE" core/dd_protection.py       # risk_pct layer
grep -n "def calc_multiplier\|math.floor" ops/accounts.py    # account-multiplier layer
grep -n "dd_protection" ops/cli.py || echo "none (expected — the two layers never meet)"
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-10 | Initial draft, `Proposed`. Five judgment calls surfaced with recommended starting values + operator-ratification hooks; meta-decision (LOCKED = parameters / lifecycle = authorization) recorded. Awaits Phase-1 operator ratification of the five numeric calls before `Accepted`. | Joshua + Claude |
| 2026-07-10 | Drafter correction (same session, post-review). §0 gains verified reads of `core/dd_protection.py` + `ops/accounts.py`/`ops/cli.py` (commit `6f5480bf`, 2026-07-06). **Call 2's fictional unified `final_lots` product removed** and replaced with the real two-layer architecture: lifecycle lands at the **risk_pct layer, multiplicative with `DD_SCALE`** (WATCH-1 + DD ⇒ 0.20×), with axis-separation pinned to leave `BASE_RISK`/`DD_SCALE`/`DD_TRIGGER` byte-identical. Added: Call 5 rail caveat (no autonomous rail exists yet — policy pre-registers the future one), Call 1 provisional-until-data caveat, §7 Delete-until-needed scope note (ship beta-monitor first; defer per-leg tiers), §3 anti-pattern row, and the safe-side re-MC one-liner. Still `Proposed`; Call 2's ratification now also confirms the integration layer + compounding rule. | Claude (drafter) |
| 2026-07-10 | **Operator ratified all five §2 calls as recommended** (`Proposed`→`Accepted`). Ratified: **Call 1** σ=1.0 / window=review cadence / 2 consecutive windows; **Call 2** 4 tiers, ladder 1.0/0.5/0.25/0.00, integration at the **risk_pct layer multiplicative with `DD_SCALE`** (WATCH-1+DD ⇒ 0.20×, confirmed intended); **Call 3** one-tier `SURVIVAL-ONLY` haircut / OOS promotion = one regime cycle + min live-trade count / 2× review cadence / one-window tightness; **Call 4** soft-flag 2/4 / act 3/4 / portfolio de-risk 0.5× / full beta shutdown operator-GO/NO-GO; **Call 5** both GO/NO-GO events + no-autonomous-promotion invariant confirmed. Implementation (create `strategy_lifecycle.md`, CLAUDE.md authorization-axis note, STATE.md forward-board entries, risk_pct wiring + axis-separation test) is Phase 2/3, **pending**. | Joshua (ratify) + Claude (record) |
| 2026-07-11 | **Phase-2 partial landed — status header corrected.** Canonical owner `strategy_lifecycle.md` + CLAUDE.md note + STATE.md entries + `core/lifecycle.py`/`dd_protection.py` wiring + Call-4/`decay_breach` + `ops/cli.py lots` read-only auth surface are **DONE** (neutral at 1.0×). Pending remains data-dependent Call-1 harness + state writer, beta-cohesion diagnostic, Pine pyramid parity. Header no longer claims "Implementation is pending" for the whole Phase-2. | Cursor (doc-skew repair) |
| 2026-07-17 | **Pine pyramid-parity CONFIRMED-FALLBACK.** [`Q-PYRPARITY-1`](../briefs/closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md) `FALSIFIED-NONPROPORTIONAL` (MYM TV qty ceiling 17/127); WATCH haircuts on pyramided legs realize at account-multiplier layer. Call-1 harness already landed 2026-07-14. Pending remains beta-cohesion diagnostic only. | Cursor (Phase 3 close) |
| 2026-08-23 | **Beta-cohesion diagnostic landed** (lagged-correlation lead-lag; CLI skip-if-missing). Report-only. No `lifecycle_state.json` write. No Call-1 σ-source claim. | Cursor Cloud Agent |
| 2026-08-07 | **Call 5 superseded in part** by S5 ADR (bounded sandbox-up exception). Header `Superseded-in-part-by` + Call 5 addendum; historical body frozen; demotion/retirement/re-entry/re-opt bars stand. | Cursor (drafter) · Joshua (plan GO) |
| 2026-09-01 | Addendum: STATE.md forward-board entries this ADR's own §6/§10 require (decay review, beta-death review) are missing -- diagnostic only, operator call on remediation | Claude Code (ADR-corpus reconciliation sweep) |

---

## Addendum 2026-09-01 -- STATE.md forward-board entries missing (verdict-free diagnostic)

**Status:** diagnostic only -- no disposition chosen here; see operator-call note below.

This ADR's §6 gate item 3 ("The STATE.md forward-trigger board gains two entries -- per-strategy
decay review and the beta-death review (Call 4) -- each pointing at strategy_lifecycle.md as owner,
first evaluation 2026-08-08") and its §10 audit hook #6 (`grep -n "decay review\|beta-death\|strategy_lifecycle" STATE.md`)
both currently fail against the working tree: none of those three terms appear anywhere in STATE.md
as of 2026-09-01, including the dated 2026-11-08 section where this ADR's own §6 AMBIGUOUS clause
promises a recorded re-confirm ("re-confirmed at 2026-11-08 (recorded, not silently amended)").

The 2026-08-08 evaluation itself DID occur and IS accurately recorded off-ADR:
docs/notes/audits/programme-audit/2026-08-08-quarterly-audit.md row 7 flags the lifecycle Call-1
sigma-source as dark/reachability-blocked, and STATE.md's own "No fixed date / gated" block (the
"lifecycle Call-1" bullet) corroborates the AMBIGUOUS-on-thin-data reading this ADR's own §6
anticipated. What's missing is only the standing STATE.md forward-board *bullet(s)* this ADR's own
gate/hook require -- they appear to have been folded into the deleted ~90-line rider blockquote at
the 2026-08-08 discharge (STATE.md's own note: "the former ~90-line rider blockquote is deleted per
the retention test -- it restated obligations the audit note now owns"), with no successor row
created for the 2026-11-08 re-confirm.

**Operator call owed (not decided here):** whether to (a) add a STATE.md 2026-11-08 forward-board
row pointing at strategy_lifecycle.md / this ADR for the Call-1 re-confirm, mirroring the pattern
already used by the mechanism-boundaries, sourcing-phase-retirement, and GRAND-tier ADRs' own
2026-11-08 rows, or (b) treat the quarterly-audit-note pointer as the standing mechanism going
forward and retire this ADR's §6/§10 STATE.md-bullet requirement as superseded by that convention.
Either resolution should land as its own dated addendum (or a supersession, per §4 trigger 1's own
revert-action rule) -- this addendum only names the gap.
