# ADR 2026-08-04 — The Tradeify venue is de-scoped as a program target, **evaluation included**

**Status:** `Accepted` — operator ruling recorded 2026-08-04 in session, against an options card that named every consequence listed in §6 below; the ruling was made with those consequences in front of it. **§6 downstream sweep COMPLETE 2026-08-04 at its six enumerated sites only** (§7 Phase 3 / §6 Downstream list): 08-02 ADR withdrawn to LTM · CLAUDE.md posture + suspended research interest · STATE.md queue reset, forward board, decision index · `ops/instruments/{MYM,MNQ}.md` status + dated dispositions · INDEX regenerated · SESSIONS entry. ⚠ **Bound reading (Addendum 2026-08-06 / claim-alignment M8):** `COMPLETE` certifies those six sites — **not** a repo-wide live-target sweep. Wider-pass residue named in that addendum. **AMENDED 2026-08-04, operator-ratified (Addendum 2026-08-04): §2 clause 3 is narrowed to work whose sole justification is redeploying the locked Striker book at this venue — Tradeify-shaped base-construct *research* is not barred.** The de-scope itself (both phases, both legs, both forks F2/F3, the §4 falsifier) is unchanged.
**Decision date:** 2026-08-04
**Supersedes:** `2026-07-17-c1-rail-build-account-registration-go.md` in part — the **deployment limb only**: Tradeify ceases to be a deployment target for the locked Striker book, evaluation included, and both legs are withdrawn from the c1 eval deployment. That ADR's rail build, account registration, attended-only posture, $700 spend ceiling and arm gate are **untouched and stand**; the rail is retained and disarmed pending fork F2.
**Supersedes:** `2026-07-23-c1-rung-selection-ev-objective.md` in part — the **live-rung / deployment-premise limb only**: every "live c1 rung stays WATCH-1 0.50× / disarmed" sentence becomes historical; carrying 0.50× to a different venue geometry is not authorized by that ADR. Its EV objective and both-halves gate for rungs *above* 0.50× **stand**.
**Superseded-by:** none
**Superseded-in-part-by:** `2026-08-07-loop-s1-environment-ratification.md` — §7 forks **F2** and **F3** only (rail kept warm/disarmed at incumbent eval; no successor migration now). Clauses 1–2 and fork **F1** stand.
**Superseded-in-part-by:** `2026-08-07-loop-s5-bounded-promotion-lane.md` — Addendum 2026-08-04 *“separate operator GO before any capital or account action”* **only for in-ceiling sandbox admits** (budget approval replaces per-candidate GO there). Clauses 1–2, Striker redeploy bar, and ceiling-crossing GOs **stand**.
**Retain-until:** superseded by a venue re-scope under §4, or by registration of a successor execution venue
**Withdraws:** [`2026-08-02-striker-tradeify-funded-phase-descope.md`](2026-08-02-striker-tradeify-funded-phase-descope.md) — that ADR was `Proposed`, never ratified, and decided the **funded phase only**; its §3 row 2 considered this wider scope and declined it as *"larger than the evidence."* The operator has now elected the wider scope. Because that ADR never reached `Accepted`, it is **withdrawn, not superseded** — nothing was in force to replace. Its §1 measurements and its §7 F1 ruling are carried forward here by citation (§1, §6) rather than lost. **Measurement cells are byte-faithful; two Source cells were narrowed in the first draft and are restored — see the correction note under the §1 table.**
**Authors:** Joshua (ruling, 2026-08-04) + Claude Code (Opus 5, recorder)
**Related:** [`2026-07-12-prop-portfolio-four-friendly-firms.md`](2026-07-12-prop-portfolio-four-friendly-firms.md) (§4 falsifier — **not** pre-empted, §5) · [`2026-07-10-strategies-never-locked-lifecycle-governance.md`](2026-07-10-strategies-never-locked-lifecycle-governance.md) (the axis this ADR deliberately does **not** move) · [`2026-08-05-strategy-venue-binding-axis.md`](2026-08-05-strategy-venue-binding-axis.md) (`Accepted` 2026-08-22 — de-scope re-expressed as an edition WITHDRAWN, not book decay; registry still owed) · [`2026-08-03-lifecycle-ladder-intermediate-rung.md`](2026-08-03-lifecycle-ladder-intermediate-rung.md) (`Withdrawn` 2026-08-22 — lost its decision driver; §6) · [`2026-08-03-c1-cadence-leg-preregistration.md`](../briefs/pre-registration/2026-08-03-c1-cadence-leg-preregistration.md) (moot in its deployment limb — §6)
**Re-expressed under the venue-binding axis:** WITHDRAWN is the Tradeify_Select_100K edition state; book authorization is unchanged. Ledger: [`ops/venue_editions/Tradeify_Select_100K.md`](../../ops/venue_editions/Tradeify_Select_100K.md).
**Layer:** deployment scope. **No locked parameter, allocation, `dd_protection` constant, `core/lifecycle.py` state, Pine file, or `LEG_MAP` entry is touched.**

---

## §0 — Rule 0 reads (production source, verified 2026-08-04 at `289535d`, worktree clean)

| Source | Anchor (`git log -1`, verified 2026-08-04) | What it grounds |
|---|---|---|
| `core/lifecycle.py` L34–36, L43, L180–202 | `4441c72` 2026-07-11 | `TIER_MULTIPLIER = {AUTHORIZED 1.00, WATCH-1 0.50, WATCH-2 0.25, RETIRED 0.00}`; the import-time `_validate_ladder()` that **hard-fails** on any multiplier change. **The axis this ADR does not move.** Read with surrounding context per the §0 surrounding-context sub-rule. |
| `core/firm_rules.py` L469ff + `Tradeify_Select_100K` block | `2345095` 2026-08-03 | `AUTOMATION_FRIENDLY_PROP_FIRMS` = {bulenox, tradeify, myfundedfutures, blusky} — Tradeify is **1 of the 4** firms in the §4 falsifier's frozen set. Tier facts: `max_dd_pct 3.0`, `profit_target_pct 6.0`, `min_trading_days 3`, `micro_contract_cap 80`, `cost_per_side_usd 0.91`, `consistency_rule_pct 40.0`, **`inactivity_max_idle_days 5`** (the eval-phase activity rule — a VENUE FACT, art. 10468318), `dd_lock_offset_usd 100` (known-defective for eval, two OPEN DEFECT blocks). |
| `ops/c1_rail/c1_sizing_host_reference.py` `LEG_MAP` | `2345095` 2026-08-03 | Both c1 legs are Striker (`dj30_mym`→`Striker`, `nas100_mnq`→`Striker NAS100`); `cap_alloc` MYM 69 / MNQ 11. Scope claim in §2. |
| `lab/discovery/prop_survivor_scoring.py` `discharges_falsifier` | `97011c1` 2026-07-13 | §4 discharges on **simulation** — frozen seeds/sims/horizon over the frozen $100K×4 set. **No live outcome enters it.** Grounds §5's non-pre-emption clause. |
| [`2026-08-02-striker-tradeify-funded-phase-descope.md`](2026-08-02-striker-tradeify-funded-phase-descope.md) §1, §3, §7 | `2345095` 2026-08-03 | The three measured funded-phase misfits carried forward in §1; the §3 row-2 alternative now elected; the F1(b) ruling this ADR reverses. |
| [`2026-07-17-c1-rail-build-account-registration-go.md`](2026-07-17-c1-rail-build-account-registration-go.md) §B4, §8 | `2345095` 2026-08-03 | Spend ceiling **$700**; committed tally **$208/$700** (eval paid $159, 2026-07-18). Grounds the sunk-cost figure in §6. |
| [`STATE.md`](../../STATE.md) operator queue rows 1–4 | worktree, `289535d` | The **four** queue items this ADR moots, verbatim, including the **B7-REFIRE Stage 1 desk card dated Tue 2026-08-04 — today**. Row 4 (rule-pin / `(d)`-clause) is Tradeify-scoped on both limbs — see §6. |

**Gitignore pre-flight.** `**/*.pine` is ignored. **No Pine source is read or cited**, and no numeric constant here derives from Pine — this decision is entirely at the deployment layer. Citation-chain mode not required (§0 gitignore sub-rule).

**Contingency note:** none required. Every number below traces to a committed artifact named in **this table or in the §10 / Verification blocks**. (Narrowed from "named in this table": §1 item 2's cadence-coverage figures — 73.1%, +14.6%, 39-of-80, the ≥90% floor — live in `lab/analysis/c1/c1_cadence_coverage_2026-08-03/RESULTS.md` and the cadence pre-registration, both cited below rather than in the §0 table.)

---

## §1 — Context

On 2026-08-02 the operator proposed retiring Striker at Tradeify. The ADR authored in response ([`2026-08-02`](2026-08-02-striker-tradeify-funded-phase-descope.md)) narrowed that to the **funded phase only**, on the ground that all three measured misfits are funded-phase properties and the eval carries none of them. That ADR was never ratified. On 2026-08-04 the operator elected the wider scope its §3 row 2 had declined.

**The three funded-phase misfits stand — measurements carried forward byte-faithful, Source cells restored (see the correction note under the table):**

| Misfit | Measurement | Source |
|---|---|---|
| Winning-day cadence vs the **$200** threshold | **1.01** qualifying winning days/month; 22.2% of trading days ≥$200 → ~5-month payout cycles | [`cadence RESULTS`](../../lab/analysis/c1/c1_cadence_inactivity_2026-08-02/RESULTS.md) §0–§1 (**both figures live here** — L30, L52); book-composition §2 (rounded "1.0/month" only) |
| Pyramid stack vs the funded **start tier** | **104.7%** of 2-leg net comes from days needing **>40** micros; verified funded start tier is **30**, laddering 30→40→50→80 | book-composition §2(d); [rule-pin verification 2026-07-29](../notes/2026-07-24-tradeify-rulepin-verification.md) |
| Funded economics | chain **$299.80**/acct-mo; funded 1-yr mortality **49.06%** | book-composition §Addendum 2026-07-29 |

⚠ **Accuracy correction to this table's own provenance, recorded rather than silently fixed.** The first draft attributed row 1 solely to "book-composition §2" and dropped the `cadence RESULTS` half — but **neither 1.01 nor 22.2% appears in that brief** (it carries only the rounded "1.0 qualifying winning day/month"); both live in the cadence RESULTS. Row 2 had likewise lost ", laddering 30→40→50→80" and its rule-pin source. So the header above this table originally read *"carried forward unedited"*, which was **false as written**: the measurement cells were faithful, the **Source** cells were narrowed. Both are restored above. Caught by this branch's own pre-merge verification pass, and it is a live instance of `lesson_borrowed_numbers_need_connecting_arithmetic` — errors enter at transcription boundaries.

**What is new, and what makes the wider scope defensible where it was not on 08-02, is an eval-phase limb the 08-02 ADR did not have.** Two measurements landed 2026-08-03:

1. **The eval's activity rule is priced and its mitigation is undelivered.** `core/firm_rules.py` records `inactivity_max_idle_days: 5` as a venue fact binding the **evaluation** (not only the funded phase), and the inactivity-ON re-MC prices the barrier at **92.6–97.6% path death** with the mitigation undelivered (residual track R8). The book delivers a trade in **73.1%** of weeks — not because its rate is low but because the two legs go quiet together, **+14.6%** more than independence. Every c1 pass-rate figure in the repo presumes a cadence mitigation that does not exist.
2. **The cadence gap is not closable by a leg on current evidence.** Q-CADENCE-1's arithmetic shows one incumbent-shaped leg leaves **39** of 80 idle weeks — halving the gap, not closing it — and reaching under one expected idle week per eval window needs a leg firing in **≥90%** of weeks. The one construct that clears that floor (ORB-MNQ) is terminated at the screen on **S7 order-symbol occupancy** — see the companion adjudication.

**The limb that runs the other way is recorded here rather than omitted, exactly as the 08-02 ADR recorded it.** Q-GEOFIT-1 measured the c1 book's active-day distribution: skew **+3.633**, worst single day **−$744** against the $3,000 trail; a synthetic matched on σ, μ/σ, zero-day fraction *and* tail class busts at **28.38%** versus the real book's **4.74%**. Striker's *drawdown* geometry is the best-fitting property in the estate, and the deployed WATCH-1 0.50× rung measures 0.11% full-panel / 1.20% bootstrap-95th — the only cell anywhere clearing the frozen 3.0% ceiling on a close-only clock. **This ADR de-scopes the venue despite that, not in ignorance of it.** The honest statement is that survival geometry was never the binding constraint at Tradeify; payability (funded) and activity (eval) are, and they bind at opposite ends of the same skew.

**Decision driver (one sentence):** with the funded phase de-scoped on measured payability grounds and the evaluation now shown to carry its own undelivered-mitigation activity blocker whose only ≥90% candidate is screen-dead, the operator has elected to stop treating Tradeify as a destination rather than continue committing operator-attention to a venue neither phase of which is a viable target.

---

## §2 — Decision

**The Tradeify venue is de-scoped as a deployment target for the locked Striker book, in both phases.** `Tradeify_Select_100K` is no longer a deployment destination for the locked Striker book; the two Striker legs are withdrawn from the c1 eval deployment; and no further work is authorized whose sole justification is reaching, holding, or passing a Tradeify account **to deploy those two legs**. *(Clause narrowed 2026-08-04 — see the Addendum below; the original clause is quoted there in full and this is the only wording changed in this section.)*

**Effective:** immediately upon acceptance.
**Scope:** the `Tradeify_Select_100K` evaluation **and** funded phases, for the two c1 Striker legs (`dj30_mym`, `nas100_mnq`). Nothing else.

What this decision explicitly does **not** do — each listed because each is a live misreading available today:

| Unchanged | Status after this ADR |
|---|---|
| Striker authorization (both legs) | **`AUTHORIZED · MECHANISM @ 1.00×`.** No `core/lifecycle.py` write, no `lifecycle_state.json`. **Not WATCH, not RETIRED.** Venue-fit is not decay; the ladder is a decay instrument and there are zero live fills to trigger Call 1. |
| Striker parameter axis | **LOCKED**, untouched. This ADR is not a decay finding and not a re-fit licence. |
| The c1 rail itself | **Built and retained, disarmed.** This ADR de-scopes a venue, not the rail. Rail disposition (keep warm / tear down / re-point) is a **named open fork**, §7 F2. |
| The M1 monitoring spine | **Retained.** It is venue-agnostic structured-event/reconcile machinery; its *arming-gate* duty lapses with the venue, its engineering does not. |
| `dd_protection`, allocations, MC anchor, Pine, `LEG_MAP` | **All untouched.** |
| Prop-portfolio §4 falsifier + 2026-11-08 hard date | **Unchanged and NOT pre-empted.** §4 discharges on simulation over the frozen $100K×4 set; Tradeify stays in that set. See §5 and the §7 F1 fork. |
| The other three FRIENDLY firms | **Untouched and unmeasured** on this axis. Bulenox / MFFU / BluSky publish different payout mechanics and different activity rules; none was measured against Striker's cadence. |

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Funded-phase-only de-scope** (the 08-02 ADR as authored) | The alternative actually on the table, and the one the evidence supported on 08-02. Ruled out by the operator on 08-04 after the eval-phase activity limb landed: holding an evaluation whose activity rule is priced at 92.6–97.6% path death with an undelivered mitigation, in order to reach a funded phase already de-scoped, spends operator-attention on a path with no destination. **Recorded as the narrower decision this one replaces, not as a strawman** — it remains the correct reading of the 08-02 evidence set. |
| **Lifecycle `RETIRED` (0.00×) for both Striker legs** | Blocked on the same three grounds the 08-02 ADR established and this ADR does not disturb: wrong instrument (the ladder is decay-triggered via Call 1's rolling live PF; **zero live fills exist**, so there is no evidentiary basis); one-way door (Call 5 bars automation from ever re-entering a RETIRED strategy, foreclosing every future venue); and it removes the survival asset (§1's skew limb) rather than the liability. **Venue-fit is not decay.** |
| **Hold the eval to 2026-11-08** (the 08-02 F1(b) ruling) | The standing ruling until today. Its stated purchase was five items — B7 Stage 1, M1 signoff, first live fill, execution-quality data, and the venue option held open. The operator has elected to surrender all five rather than fund ~14 weeks of attended sessions and ~4 activity-rule instances against a venue no longer targeted in either phase. **§6 records the full cost of that surrender.** |
| **Park the eval unattended and let it lapse** | Cheaper in attention but dishonest in the record: the account would still be registered, the rail still pointed at it, and the repo would still carry Tradeify as a live target while nobody tended it. A de-scope that is not written down decays into an undocumented abandonment — the failure shape the 07-16 charter ADR exists to prevent. |
| **Register a successor venue in the same motion** | Over-reach, and unmeasured. Bulenox / MFFU / BluSky have different payout mechanics and activity rules and **none has been scored against Striker's cadence**. Choosing a successor inside a de-scope ADR would repeat the 08-02 error in the opposite direction — deciding wider than the evidence. Named as fork F3 instead. |
| **Status quo — no decision** | Leaves an operator queue whose top item is a desk card for **today** pointed at a venue the operator has decided against, and leaves ~14 weeks of attended sessions nominally owed. Silence would be read as intent at the 08-08 checkpoint. |

---

## §4 — Falsifier (revert trigger)

**H (what this ADR asserts, binary):** *the Tradeify venue is not a viable deployment target for the locked Striker book in either phase — because the funded phase's per-winning-day payout mechanic and contract-scaling ladder, and the evaluation's weekly-activity rule, are each mismatched to a positively-skewed, low-cadence, pyramid-dependent book; and these are properties of the venue's rules and the book's shape, not of a fixable configuration.*

**H is FALSIFIED — and the venue is re-scoped in by a superseding ADR — if any trigger below fires.**

| # | Trigger | Threshold | Action |
|---|---|---|---|
| T1 | **The eval-activity limb is wrong or repaired.** A cadence instrument ships (R8, or a leg licensed through Q-CADENCE-1's unchanged gate) and the combined book's measured weekly coverage clears the frozen floor | coverage **≥ 95%** of calendar weeks on a dated panel, **and** inactivity-ON re-MC path death **≤ 10%** | Eval-phase limb falls; re-open §2's eval half |
| T2 | **The funded cadence diagnosis is wrong.** Measured qualifying winning days on funded data | **≥ 2.0**/month sustained over **≥ 6** funded months | Re-scope funded phase in; supersede |
| T3 | **The funded economics claim is wrong.** Dated, pre-registered re-derivation at verified pins with the `eval_sim` lock fix in place | chain rate **≥ $600**/acct-mo **and** funded 1-yr mortality **≤ 30%** | Re-scope; supersede |
| T4 | **The venue changes the mechanic.** Primary-source re-verify (help.tradeify.co, Rule-13 form) | winning-day threshold removed or lowered below **$100**, **or** funded start tier raised to **≥ 50** micros, **or** `inactivity_max_idle_days` removed/raised above **10**, **or** Flex payout ceases to count winning *days* | Re-run T2/T3 derivations; may re-scope |
| T5 | **The eval-geometry ground is stronger than assumed.** The Phase-4 both-halves re-run (companion GO, 2026-08-04) returns **0.50× GATE PASS on all four partitions** on the venue's honest clock (`intraday_low` fed from 15m bars, `dd_lock_offset_usd` unreachable) **and** T1 has fired | both conditions jointly | The eval half of §2 loses its geometric ground; re-open on the joint evidence only |

**Not admissible as a re-scope route:** re-sizing the legs to manufacture winning days (measured flat-to-negative — *"size converts extraction to breach"*); composing ORB in to buy cadence (Q-COMPOSE-1 `FALSIFIED` 2.65%→38.75%, and ORB is independently S7-dead); re-deriving the chain rate on a friendlier harness without the eval-lock fix; or reading a single trigger in isolation where the table says *jointly*.

**Revert action:** author a superseding ADR. **Never edit this ADR's §2 in place** (Known Trap #12).

**Trigger check schedule:** **T4 at the 2026-08-08 checkpoint** and at each 90-day venue-fact re-verify. T5 at the Phase-4 run's completion. T1 on any cadence-instrument landing. T2/T3 are evidence-driven and **cannot fire before funded data exists**, which — with the venue de-scoped — is the honest state: they are dormant, not pending. All triggers ride the **2026-08-08 quarterly programme audit** vehicle now booked on the STATE.md forward board.

---

## §5 — Forbidden moves (under this ADR)

- **Converting this into a lifecycle demotion or retirement.** Genuinely tempting — it is cleaner, feels decisive, and matches the operator's original 08-02 framing. Barred for the three §3 reasons. **Venue-fit is not decay.** If Striker is ever demoted it must be on Call-1 evidence through the Call-1 mechanism, and this ADR makes that evidence *less* available, not more (§6).
- **Citing this ADR to pre-empt, discharge, or moot the prop-portfolio §4 falsifier at 2026-11-08.** §4 discharges on **simulation** — `discharges_falsifier`, frozen seeds/sims/horizon over the frozen $100K×4 set (`97011c1`). No live outcome enters that computation and de-scoping a deployment target does not remove a firm from a frozen simulation set. The §7 F1 fork exists precisely so this question is answered deliberately at 11-08 rather than assumed here.
- **Reading this as "the program is over."** It de-scopes one venue of four. Three FRIENDLY firms are untouched and unmeasured on this axis (§3). ⚠ **But see §6** — with no successor registered, the *operational* state is research-only, and pretending otherwise is the mirror error.
- **Tearing down the rail, deleting the M1 spine, or closing the account as an implied consequence.** Each is a distinct action with its own cost and reversibility. F2 is the fork; until it is ruled, the rail stays built and disarmed.
- **Widening to the other three FRIENDLY firms without measuring them.** The arithmetic here is Tradeify-specific — its winning-day threshold, its funded ladder, its `inactivity_max_idle_days`. The §3 row is not a placeholder.
- **Reading the withdrawal of the 08-02 ADR as erasing its measurements.** Its §1 misfit table and its Q-GEOFIT-1 skew limb are carried forward in §1 here — measurements byte-faithful, Source cells restored after a first-draft narrowing (see the §1 correction note), and including the limb that runs against the decision.
- **Quoting a stale chain rate.** The figure has been retargeted twice ($339 → $318 → **$299.80**). Only $299.80 is current.
- **Loosening any §4 trigger without a superseding ADR** — Known Trap #12.

---

## §6 — Consequences

**Verdict carried into this section:** this ADR records a *scope* decision, not a verdict on Striker or on the rail. H is asserted, not proven; §4 names what would refute it.

**Positive:**
- Operator-attention stops being committed to a venue neither phase of which is a target. The 08-08 slate loses the funded-economics rows *and* the ~14 weeks of attended eval sessions.
- The eval-vs-funded distinction, made explicit for the first time on 08-02, is now resolved rather than left as a live tension between a de-scoped destination and a funded journey.
- A governance error is again avoided: an irreversible authorization action (`RETIRED`) is not spent to express a reversible deployment fact.
- The undelivered-cadence-mitigation finding stops being a footnote on live pass-rate figures and becomes a recorded reason.

**Negative (real cost — this is the expensive half, and it is larger than the 08-02 decision's):**

- **The first live fill never happens, and it was the unblocking event for five separate threads.** Per STATE.md queue item 3 verbatim, a first fill unblocks the Q-NAS-ECR successor, lifecycle **Call-1** (whose rolling-PF σ-source has *no live data today*), and the ORB decay re-scope; the forward board adds the **venue-native regime-monitor successor** (explicitly *"gated on first live fill"*) and **B7 Stage 2b add-slippage capture**. All five are now stranded with no live source anywhere in the estate.
- **The standing research interest becomes unreachable.** CLAUDE.md names *"c1 execution quality (better fills and exits)"* as the standing interest under the prop-portfolio program. With no live execution surface, it has no data source. This is not a re-scoping of that interest — it is its suspension, and it should be recorded as such rather than left standing as a live line.
- **Operator-queue items 1, 2, 3 *and 4* are mooted**, including the **B7-REFIRE Stage 1 desk card dated Tue 2026-08-04 — today**. B7-REFIRE Stage 1 (the first real TV strategy entry at non-zero size) remains permanently owed and permanently undischargeable at this venue. **Row 4 (Tradeify rule-pin / Q-CAPALLOC-1 `(d)`-clause adjudication) is included and is stated here rather than only on the board:** both limbs were Tradeify-scoped — (a) book-comp D1 SHIP dies with the funded phase, and (b) the `69/11` cap-allocation `(d)` adjudication governs an account no longer deployed to. Its already-discharged half (pins verified 2026-07-29) survives as the §4 **T4** venue-fact re-verify.
- **$208 of the $700 committed spend is sunk** (eval $159 paid 2026-07-18, plus prior tally), against a ceiling signed for "all-in to first live fill" — a fill that will not occur.
- **The 08-02 F1(b) operator ruling is reversed** four days after it was made. Recorded as a reversal, not quietly dropped.
- **The operation has no live execution surface at all.** With no successor venue registered, the program is **research-only in fact** — which is precisely the state the prop-portfolio §4 falsifier would *impose* at 2026-11-08 if undischarged. The de-scope reaches that state ~3 months early and by election rather than by falsification. §5 forbids reading this as discharging or pre-empting §4; it does not permit pretending the operational state is unchanged.
- **Two 2026-08-03 artifacts lose their driver.** The `WATCH-1H` rung ADR's stated decision driver was closing a ladder-granularity gap *"before the re-measurement lands rather than under its pressure,"* with a first armed send pending — there is now no armed send and no live rung to protect, so its §3 "status quo" row loses its force. **Q-CADENCE-1** is moot in its deployment limb (a cadence leg for *this* eval), though its frozen ≥90% floor and its C1–C5 structure survive as a reusable gate for any successor venue.
- Dormant-H drift: the 08-02 brief's §4 H1 and §6 D4 were already headed for DORMANT; they are now dormant against a wider scope. §10 hook 4 guards the re-read.

**Risks:**
- **The scope may now be too wide** — the mirror of the 08-02 risk. If a cadence instrument turns out cheap (R8 is ~13 maintenance trades/year at ~$1.82 RT, and the operator's objection to it was preference, not arithmetic), the eval half of this de-scope was purchased against a blocker that had a $24/year fix. **Mitigation: §4 T1 is written exactly to catch this, and it is the cheapest trigger in the table.**
- **Successor-venue drift.** "Three firms untouched" can decay into "three firms assumed viable." None is measured on the cadence axis. Mitigation: F3 is a named fork with a required measurement, not an assumption.

**Downstream artifacts needing update (gated on acceptance — §7 Phase 1):**
- [`2026-08-02-striker-tradeify-funded-phase-descope.md`](2026-08-02-striker-tradeify-funded-phase-descope.md) — status → `Withdrawn`, with a header pointer here.
- [`CLAUDE.md`](../../CLAUDE.md) §Live-execution posture — one pointer line; **and** the standing-research-interest line marked suspended.
- [`STATE.md`](../../STATE.md) — decision-index line; operator-queue rows **1/2/3/4 removed** (all four were Tradeify-scoped; see the row-4 note below); F1/F2/F3 forks booked on the **operator queue** (not the dated forward-trigger board), F2/F3 carrying their 2026-08-08 dates inline.
- [`ops/instruments/MYM.md`](../../ops/instruments/MYM.md) / [`ops/instruments/MNQ.md`](../../ops/instruments/MNQ.md) — status blocks ("LIVE c1 leg (disarmed)") no longer true; dated disposition appended per Rule 10.
- [`docs/adr/INDEX.md`](INDEX.md) — regenerate.
- [`docs/SESSIONS.md`](../SESSIONS.md) — session entry.

---

## §7 — Implementation plan

- **Phase 0** — §0 anchors re-verified at implementation time (`git log -1` on the seven targets). **DONE 2026-08-04.**
- **Phase 1** — downstream pointer sync per §6. **Doc-only; no `core/`, `ops/`, Pine, `LEG_MAP`, `lifecycle_state.json`, or rail-config edit.** The rail is left built and disarmed (`dry_run=true`) pending F2.
- **Phase 2** — grep-sweep for text reading Tradeify (either phase) as a live target; §10 hook 3.
- **Phase 3** — `check_brief.py` + `check_adr_graph.py` + `check_status_consistency.py` + `check_falsifier_reachability.py` green; status → `Accepted`.

**Three forks are named and NOT decided here.** Each is a distinct decision with its own evidence:

| # | Fork | Owner | Date |
|---|---|---|---|
| **F1** | **How the §4 falsifier reads a de-scoped firm at 2026-11-08.** §4 scores eval-phase bust on the frozen $100K×4 set by simulation, and Tradeify stays in that set — so the arithmetic is unchanged. What needs an operator reading is whether a discharge resting *on Tradeify* counts as discharging a program that no longer targets it. **Deciding this here would pre-empt §4, which §5 forbids.** | Operator | **2026-11-08** |
| **F2** | **Rail disposition** — keep warm (disarmed, no venue), tear down, or re-point at a successor. Also governs the registered account (leave dormant / close) and the M1 spine's retention. | Operator | **2026-08-08** |
| **F3** | **Successor venue, if any.** Requires scoring Bulenox / MFFU / BluSky against Striker's *cadence* axis — the measurement none of them has. Until it exists, "three firms remain" is a fact about the firm set, not about viability. | Operator (GO) + CC (measurement) | **2026-08-08** (scope), measurement dated separately |

---

## §10 — Audit hooks (runnable)

```bash
# 1. The authorization axis was NOT touched — both Striker legs still at 1.00x.
#    NOTE import shape: core/lifecycle.py does `from lib.validation import ...`,
#    so 'core' goes on sys.path, NOT the repo root (Trap M-AHF, recorded 2026-08-02).
python -c "
import sys; sys.path.insert(0,'core')
from lifecycle import get_lifecycle_multipliers, TIER_MULTIPLIER
keys = ['Striker', 'Striker NAS100']
m = get_lifecycle_multipliers(keys); print(m, TIER_MULTIPLIER)
assert all(m[k] == 1.0 for k in keys), 'Striker lifecycle moved - this ADR forbids it'
assert TIER_MULTIPLIER['RETIRED'] == 0.0, 'ladder edited'
"
# Expected: {'Striker': 1.0, 'Striker NAS100': 1.0} + ladder 1.0/0.5/0.25/0.0, exit 0

# 2. No code/config change rode along with this doc-only decision.
git diff --stat HEAD -- core/ ops/c1_rail/ 2>/dev/null
# Expected: empty

# 3. No text reads Tradeify (either phase) as a live program target.
#    HOOK WIDENED 2026-08-06 (claim-alignment M8 / H19): pattern covers phrasings
#    actually in use after the 08-04 sweep, not only the original five tokens.
rg -n "chain rate|acct-mo|funded phase|Select Flex|live-but-disarmed|LIVE c1 leg|live c1 leg|live 2-leg book|is deployed at|the live account|69 MYM|MNQ 11" \
  CLAUDE.md STATE.md ops/instruments/MYM.md ops/instruments/MNQ.md \
  ops/instruments/YM.md ops/instruments/NQ.md docs/notes/rail_build/RUNBOOK.md
# Expected: every hit historical/record-only or carrying a de-scope / withdrawn marker

# 4. The withdrawn ADR is marked, and its measurements survive here.
rg -n "^\*\*Status:\*\*" docs/adr/2026-08-02-striker-tradeify-funded-phase-descope.md
# Expected: Withdrawn, pointing at this ADR
rg -n "1\.01|104\.7%|299\.80|49\.06%|3\.633" docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md
# Expected: the misfit table AND the contrary skew limb both present

# 5. §4 was NOT pre-empted — the falsifier and its frozen set are untouched.
rg -n "3\.0%|≥ 50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md | head
rg -n '"tradeify":' core/firm_rules.py
# Expected: frozen thresholds byte-unchanged; exactly 1 hit for the tradeify family key.
# NOTE the shape: the dict opens at L469 and "tradeify": is at L477, so an `-A 6` window
# STOPS SHORT and exits 1 on a claim that is TRUE (Trap M-AHF — corrected after the hook
# was executed and returned empty).

# 6. The eval-activity limb this ADR rests on is still true at HEAD.
rg -n "inactivity_max_idle_days" core/firm_rules.py
rg -n "92\.6|97\.6|residual track R8" core/firm_rules.py lab/analysis/c1/c1_cadence_inactivity_2026-08-02/RESULTS.md

# 7. T4 re-verify (venue facts, Rule 13 form) — browser read; WebFetch 403s this host.
rg -n "Winning Day|winning-day|start tier|30 micro|10468318" docs/notes/2026-07-24-tradeify-rulepin-verification.md

# 8. Addendum 2026-08-04 landed at all six normative sites (expect a hit in each).
rg -ln "to deploy those two legs|Addendum 2026-08-04" \
  docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md CLAUDE.md STATE.md \
  ops/instruments/MYM.md ops/instruments/MNQ.md

# 9. The addendum did NOT touch clauses 1-2, the falsifier table, or the forbidden-moves list.
git log -p --follow -- docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md | \
  grep -A2 "^-.*deployment destination for the locked Striker book"
# Expected: clause "Tradeify_Select_100K is no longer a deployment destination..." shows no
# removal line (only clause 3's sentence changes; the falsifier table in section 4 is untouched)
rg -n "^\| T[1-5] \|" docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md | wc -l
# Expected: 5 (all five triggers still present, unedited)
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python "$HOME/.claude/skills/brief-authoring/scripts/check_brief.py" \
  docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md --type adr
python scripts/check_adr_graph.py
python scripts/check_status_consistency.py
python scripts/check_falsifier_reachability.py

# §0 anchors still current
for f in core/lifecycle.py core/firm_rules.py ops/c1_rail/c1_sizing_host_reference.py \
         lab/discovery/prop_survivor_scoring.py; do
  git log -1 --format="%h %cs $f" -- "$f"; done
# Expected: 4441c72 / 2345095 / 2345095 / 97011c1 as recorded in §0

# Every §1 measurement traces to a committed artifact
rg -n "104\.7|299\.80|49\.06" docs/briefs/2026-07-23-tradeify-book-composition.md
# ⚠ 1.01 and 22.2 are NOT in that brief (it carries the rounded "1.0"); they live here:
rg -n "1\.01|22\.2" lab/analysis/c1/c1_cadence_inactivity_2026-08-02/RESULTS.md
rg -n "3\.633|744|28\.38" lab/archive/q_geofit_1_2026-07/RESULTS.md
rg -n "73\.1%|14\.6%|80 idle|39" lab/analysis/c1/c1_cadence_coverage_2026-08-03/RESULTS.md

# Withdrawal reciprocity (this ADR withdraws; the target points back)
rg -n "Withdraws|Withdrawn" docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md \
  docs/adr/2026-08-02-striker-tradeify-funded-phase-descope.md
```

---

## Addendum 2026-08-04 — Decision clause 3 narrowed to the locked Striker book; base-construct research on this venue is not barred

**Status: `Accepted` — operator ratified in-session 2026-08-04** (having been shown the exact narrow scope below — clause 3 and the title's plain-English reading only, everything else in this ADR untouched — the operator's instruction was *"draft the addendum, then open the pr"*).

**The tension, stated precisely.** This ADR's own §2 clause 1 is already Striker-scoped and matches the operator's same-day clarification exactly: *"`Tradeify_Select_100K` is no longer a deployment destination for the locked Striker book…"* The conflict was **clause 3**, read literally: *"…and no further work is authorized whose sole justification is reaching, holding, or passing a Tradeify account."* Taken at face value that bars *any* Tradeify-directed work, including pure research that never touches the account. The **title** ("de-scoped as a program target, evaluation included") carries the same venue-wide framing and is quoted verbatim in six other places across the repo (CLAUDE.md ×2, `ops/instruments/MYM.md`, `ops/instruments/MNQ.md`, STATE.md, plus this file) — a reader working from any of those inherits the wider bar without ever seeing this addendum unless it is propagated, so this addendum updates them in the same commit (§normative sites below).

**What already happened under the corrected reading, before this addendum existed.** `MNQBASE-1` (harvest-intake brief, operator-directed 2026-08-04) recorded the divergence in its own §1.1 rather than silently proceeding, on the operator's in-session clarification that *"the Select 100K evaluation is still live — the Striker strategies were de-scoped from the eval, not the eval itself."* It ran two steps on that reading — Step 1 `RESOLVED` (event-ceiling), Step 2 `FALSIFIED` intake-dry (closure: [`MNQBASE-1-closure-intake-dry.md`](../briefs/closures/MNQBASE-1-closure-intake-dry.md)) — at **$0.00, K=0, no manifest, the account never reached or armed**. This addendum does not retroactively permit that work; it corrects the written text so a future reader does not have to re-derive the same divergence-resolution from scratch.

**Corrected clause 3 (old → new, quoted for the permanent record).**

> **Old:** *"…and no further work is authorized whose sole justification is reaching, holding, or passing a Tradeify account."*
> **New (applied in §2 above):** *"…and no further work is authorized whose sole justification is reaching, holding, or passing a Tradeify account **to deploy those two legs**."*

**Corrected reading of the title.** The H1 title text is left as filed — it is a stable cross-link identifier quoted by exact text elsewhere, and no ADR addendum in this repo's history rewrites a ratified title in place (the 07-31b precedent amends body wording and narrates via the Status line, never the H1). Read it as: *the venue is de-scoped as a **deployment** target for the locked Striker book, evaluation included* — not as a bar on research.

**What this does NOT do** (mirroring §5's discipline for the addendum itself):

- **Does not widen to the other three FRIENDLY firms.** Fork **F3** still requires scoring Bulenox/MFFU/BluSky against Striker's cadence axis before any of them is a target; this addendum is Tradeify-only and creates no precedent for the others.
- **Does not reopen Striker's Tradeify deployment.** Clauses 1–2 (the actual de-scope) are byte-unchanged. A future admissible Tradeify-shaped construct discovered under the narrowed clause 3 is a **new** candidate, not a re-entry route for the two withdrawn legs.
- **Does not pre-empt §4 or fork F1.** The falsifier still discharges on simulation over the frozen $100K×4 set; Tradeify stays in it; this addendum touches no number in §4's trigger table.
- **Does not license deployment of anything discovered.** Research surviving intake still needs its own Stage-0 pre-registration, `K_intrinsic` bound, cost-law cleared, and a **separate operator GO** before any capital or account action — per `strategy_harvest.md` §1, unchanged.
  ⚠ **Superseded in part 2026-08-07** ([`S5 ADR`](2026-08-07-loop-s5-bounded-promotion-lane.md)): for **in-ceiling sandbox admits** only, the operator approves **budgets** rather than per-candidate GOs. Ceiling-crossings, account funding, size past sandbox, and unattended loops remain operator-GO.
- **Is not itself a finding that Tradeify is viable again.** `MNQBASE-1` Step 2 found the intake well dry (L2) under this exact reading — the correction is textual, not a reopening of the venue-fit question §1–§6 already settled.

**Normative sites this addendum touches** (six, all doc-only):

1. This ADR, §2 clause 3 — wording amended in place (above), old text preserved here.
2. This ADR, Status line — `AMENDED` gloss appended.
3. [`CLAUDE.md`](../../CLAUDE.md) — posture paragraph + posture bullet, both carrying the "program target, evaluation included" paraphrase — narrowing clause appended to each.
4. [`STATE.md`](../../STATE.md) — new decision-index row (the existing 2026-08-04 de-scope row is left as filed per this repo's newest-first, append-don't-edit convention).
5. [`ops/instruments/MYM.md`](../../ops/instruments/MYM.md) — status header gloss appended.
6. [`ops/instruments/MNQ.md`](../../ops/instruments/MNQ.md) — status header gloss appended.

---


## Addendum 2026-08-06 — Bound "COMPLETE"; widen §10 hook 3 (claim-alignment M8)

**Type:** dated correction under operational-rules Rule 14 (corrections land where the claim is read).
**This addendum decides nothing new** — no §2 clause, no §4 trigger, no fork, no header-edge redo
(B1 already moved `Supersedes … in part` out of `Related`; `check_adr_graph` passes).

### Bound certification

The Status line's **§6 downstream sweep COMPLETE 2026-08-04** certifies **only** the six sites
enumerated in §6 Downstream / the Status gloss:

1. `2026-08-02-striker-tradeify-funded-phase-descope.md` → Withdrawn (LTM)
2. `CLAUDE.md` posture + suspended research interest
3. `STATE.md` queue reset, forward board, decision index
4. `ops/instruments/{MYM,MNQ}.md` status + dated dispositions
5. `docs/adr/INDEX.md` regenerated
6. `docs/SESSIONS.md` entry

All six verified landed. The defect was the **unbounded word** `COMPLETE`, not missing work at
those sites.

### Wider-pass residue (named, not silently absorbed into COMPLETE)

A pass wider than the six sites still finds live-target / live-rung phrasing (or deployment
geometry restated off the micro ledgers) in at least:

- the GO ADR [`2026-07-17-c1-rail-build-account-registration-go.md`](2026-07-17-c1-rail-build-account-registration-go.md)
- [`docs/notes/rail_build/RUNBOOK.md`](../notes/rail_build/RUNBOOK.md) §B7 / §B8
- the activity / inactivity specs under `docs/spec/`
- the book-composition brief
- the ladder-rung ADR [`2026-08-03-lifecycle-ladder-intermediate-rung.md`](2026-08-03-lifecycle-ladder-intermediate-rung.md) (driver-dead; operator O-D discharged 2026-08-22 — Status on that ADR)
- parent instrument ledgers [`ops/instruments/{YM,NQ}.md`](../../ops/instruments/)
- the 08-08 packet / pretriage surfaces

Those are **out of scope for this ADR's COMPLETE claim**. They are remediated (or operator-gated)
under their own claim-alignment rows — not by re-opening §6.

### §10 hook 3

Pattern widened in place to the phrasings actually in use:
`live-but-disarmed|LIVE c1 leg|live 2-leg book|is deployed at|the live account|69 MYM|MNQ 11`
(plus the original chain-rate / funded-phase tokens). Surfaces widened to include YM/NQ parents
and `RUNBOOK.md`.

| Date | Change | By |
|---|---|---|
| 2026-08-06 | Addendum 2026-08-06 — bound COMPLETE to six enumerated sites; name wider-pass residue; widen §10 hook 3. No §2/§4/fork change; B1 header edge not redone. | claim-alignment Phase 2 (M8) |

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-04 | **Addendum 2026-08-04 RATIFIED** — operator ruling *"draft the addendum, then open the pr,"* given after being shown the exact narrow scope (clause 3 + title reading only). **§2 clause 3 narrowed**: "no further work is authorized whose sole justification is reaching, holding, or passing a Tradeify account" → "…**to deploy those two legs**" — old text quoted verbatim in the addendum. Title left as-filed (stable cross-link identifier); its reading corrected via the Status-line gloss instead, per this repo's addendum convention (07-31b precedent). Grounds: `MNQBASE-1` §1.1 recorded the same-session divergence between clause 1 (Striker-scoped, matches the operator's clarification) and clause 3 (read literally, venue-wide) rather than resolving it silently, and had already run two $0/K=0 research steps under the corrected reading before this addendum existed. Propagated to 6 normative sites same commit: this ADR (§2 + Status), CLAUDE.md (posture paragraph + bullet), STATE.md (new decision-index row), `ops/instruments/{MYM,MNQ}.md` (status headers). Does **not** touch clauses 1–2, §4's falsifier/frozen set, or forks F1/F2/F3; does **not** widen to the other three friendly firms; does **not** license deployment of anything a future construct might find — that still needs its own Stage-0 pre-registration and operator GO. | Joshua (ruling) + Claude Code (draft + apply) |
| 2026-08-04 | Initial authoring — `Proposed`. Operator elected the wider scope (whole venue, eval included) that the 2026-08-02 ADR's §3 row 2 had declined, against an options card naming every §6 consequence. That ADR is **withdrawn** (never ratified) rather than superseded; its §1 measurements and the contrary Q-GEOFIT-1 skew limb are carried forward here unedited. Three forks (F1 §4-reading, F2 rail disposition, F3 successor venue) named and deliberately left undecided. | Joshua (ruling) + Claude Code (recorder) |
