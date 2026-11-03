# 2026-11-08 research checks: prep packet

**Status:** prep only, for Joshua's 2026-11-08 sitting. It decides nothing, edits no owner, and every disposition is his. Read from public `main` at `a0d33b6`. No private surface was read; where a check needs one, it says "needs local read".
**Index:** [STATE §2026-11-08](../../STATE.md#2026-11-08), [§No fixed date](../../STATE.md#no-fixed-date--gated).

## What changed since these checks were set

- **Rule 26, amended 2026-10-31** ([#1006](https://github.com/Joshua-Asante/first-passage/pull/1006); [operational_rules:132-145](../operational_rules.md#rule-26--prior-rejections-are-advisory-priors)): earlier rejections, closures, survey nulls and class bars are advisory priors shown beside a result. Each run's own pre-registered gates, honest K, frozen controls and venue rules still bind. Rule 28 is unchanged: falsifiers don't move, and when one fires its remedy is due and the dated verdict is Joshua's.
- **Research target (10-30): book per-session Sharpe ≥ 0.25 by adding uncorrelated edges through `lab/builder/`.** This comes from the coordinator's brief. No owner on `main` records it: `lab/builder/README.md:21` reports book per-session Sharpe "a description, not a gate". The builder (build steps 1–3, `lab/builder/README.md:3`) is a new candidate generator with its own gates 5a–5g.
- **Requirement 5 (the 4× cost hurdle) was deleted 2026-10-24** ([strategy_harvest:68](../methodology/strategy_harvest.md); [evaluation-order header](../adr/2026-08-30-evaluation-order.md)).
- **One program, 2026-10-29** ([four-firm ADR:426-438](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md#addendum-2026-10-29--one-program-the-multi-firm-operation-accepted)). The self-funded lane is closed. Later firms need distinct strategies, sourced through research (L432).
- **No strategy-signal fill has occurred** ([AGENTS.md §Live-execution posture](../../AGENTS.md#live-execution-posture)). Databento is retired and no depth source is approved.

---

## 1. GSUB-1 PARK expiries: b1, b3, b6

**Owner:** [GRAND-tier ADR §2.3](../adr/2026-08-09-grand-tier-quintessentials-binding.md#23-pursuit-lifecycle-states-canonical); records [b1](../pursuits/b1-aegis-6j-transfer-lane.md), [b3](../pursuits/b3-orb-mnq-payability-line.md), [b6](../pursuits/b6-q-nas-ecr-1.md).
**Criterion** (§2.3, L127-128): "At expiry, PARK converts to SUBTRACT absent explicit operator renewal." SUBTRACT re-entry: "re-opening requires **out-of-frame evidence plus an attached falsifier**" (L129-130).
**Evidence:** all three records say "expiry: 2026-11-08" (b1:10, b3:5, b6:13). The §10 PARK-field hooks (L227-228) return empty, so all four PARK records carry both fields.

| | Re-entry (record) | Met? | Residuals today |
|---|---|---|---|
| b1 Aegis→6J | "a 6J seat opens in the live book composition" (b1:4) | No. The ORB+Aegis native route is queue item 1, with no deployed book | b1:12 says "retained hot", but both directories are archived (`lab/ARCHIVED.json`: `aegis_6j_transfer_2026-07-05`, `aegis_6j_trail_tradeify_2026-07-29`) |
| b3 ORB-MNQ-1 | "new payability / cost-geometry evidence at an admissible venue" (b3:4) | No. 08-24: FAIL at all four firms. 08-26 addendum retracted 08-31. Recon-v3 FAILS (b3:144-164). The ORB v7 §4 candidate is paused, with no re-MC (four-firm ADR:394) | `lab/analysis/orb/orb_mnq_2026-07/RESULTS.md` is hot; `eodadv_mnq_2026-08` is archived |
| b6 Q-NAS-ECR | "a NAS100/MNQ-shaped leg reaches live fills" (b6:4) | No. No strategy-signal fill | `docs/spec/PREREG-NAS-ECR-1-live-edge-capture.md`; "no other pursuit currently owns" the ECR concept (b6:15-16) |

**What changed:** the live ORB and Aegis work is now owned by queue item 1 and the builder, not by these lanes. Rule 26 likely makes the SUBTRACT armor a disclosed prior; §2.3 is a pursuit-layer bar that Rule 26 doesn't list by name.
**Recommend:**
- b1 and b3: let both lapse to SUBTRACT. Their constructs are superseded by queue item 1 and the builder, and their residuals are retrievable.
- b6: renew to 2027-02-08 on the same re-entry. It is the only owner of the live edge-capture measure, and the ORB+Aegis route's first MNQ fill would trigger it.

**Decide:** (a) for each of b1, b3 and b6: renew (with a new expiry), lapse to SUBTRACT, or MERGE (naming a target); (b) whether Rule 26 covers §2.3's SUBTRACT re-entry armor.

## 2. Mechanism boundaries: clauses 2-A and 2-C

**Owner:** [ADR 2026-07-26 §4](../adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md#4--falsifier-revert-trigger).
**Criteria:**
- 2-A (L86): "if the first **three** four-clause-compliant campaigns all die at Stage-2/Stage-6 with the *constraint-observable confirmed present* … revert 1a to its prior wording by superseding ADR."
- 2-C (L88): "any instance of a campaign closed under executed-K where a later audit finds an examined read not enumerated in its closure note → … revert to declared-K banking for ALL closures".

**Evidence:**
- 2-A: no four-clause-compliant campaign has reached Stage-2 or Stage-6. The two closures citing 2-A failed admission: `MNQBASE-1-closure-intake-dry.md:177` and `SLR-MYM-1-closure-falsified-stage0.md:30`. Count: 0 of 3.
- 2-C: four `operator-stopped` manifests exist: `st_eh_supertrend_grid` (`closed 2 84 operator-stopped`, hook L137-139 reproduced), `orb_mnq_intraday_breakout`, `q_txg1_striker_mnq_20260812` and `q_txg1_striker_nas100_mym_20260812`. Each carries `executed_looks`. No audit finding of an unenumerated read was located.

**What changed:** the Requirement 5 deletion removes the 4× hurdle from §5 (L100), so 2-A(iii)'s cost argument no longer has a universal bar. Rule 26 doesn't touch either falsifier.
**Recommend:** 2-A not fired, carry it to 2027-02-08. 2-C not fired, provided the four closures' notes enumerate the same looks as `executed_looks`. That cross-check wasn't run here.
**Decide:** accept "not fired" for both clauses, or order the four-closure look-enumeration audit first.

## 3. Sourcing-channel retirement §4 limb 2: first starvation check

**Owner:** [ADR 2026-08-24 §4](../adr/2026-08-24-sourcing-phase-channel-retirement.md#4--falsifier-revert-trigger).
**Criterion** (L77): "AMBIGUOUS iff: at the next 2 quarterly programme audits after ratification, the surviving sourcing channels (harvest, deep-iteration lane) are themselves found zero-yield/degenerating, **and** no successor ADR reopening either retired channel under corrected design has been authored in the interim." On AMBIGUOUS, the audit "must explicitly rule on whether channel starvation, not channel quality, is now the sourcing phase's binding constraint".
**Evidence:**
- Harvest: no screen-PASS admission since 2026-07-16 (check 4). The 10-21 zero-K pass found "No published rule … clears the existing gates" (`docs/notes/research/2026-10-21-tradeify-published-rule-candidates.md:70`).
- Deep iteration: "campaigns completed **0** … campaigns abandoned **2** … **active campaign: none**" ([charter:119](../adr/2026-08-16-deep-iteration-lane-charter.md)), with nothing since DL-2 (2026-08-22).
- Search for a successor ADR reopening the census or Route B: none (only the two owner ADRs and the 08-08 edge-cohort ADR match).

**What changed:** the builder is a new generator, not a reopened retired channel, so it doesn't fail the second conjunct.
**Recommend:** first reading AMBIGUOUS, since both conjuncts hold. Rule that starvation is binding and that the builder is the response. Don't reopen either retired channel.
**Decide:** (a) accept AMBIGUOUS; (b) is starvation the binding constraint (yes or no); (c) should a retired channel be redesigned and reopened (recommend no).

## 4. Harvest intake §4: doctrine falsifier and idle guard

**Owner:** [ADR 2026-07-15 §4](../adr/2026-07-15-external-mechanism-harvest-intake.md#4--falsifier-revert-trigger) and addenda; partial supersession by [S5](../adr/2026-08-07-loop-s5-bounded-promotion-lane.md), which doesn't touch §4.
**Criteria:**
- Idle guard (L92): "if by **2026-11-08** the intake has admitted zero screen-PASS seeds beyond D5, the intake is idle-not-working — fold its disposition into the 11-08 program review (it may survive as dormant doctrine, but it must be *named* idle, not presumed active)."
- Verdict (L94): "**AMBIGUOUS** if no intake-class campaign closes by 2026-11-08 (then re-test at the following quarterly)". The 08-16 fourth branch reads this as "closes *decisively*".
- Limb 2 (L146, L160): "**Running count (canonical): 0 / 2.**" The 11-08 reading "must disclose the post-mark count and whether limb 2 fired" (L239).

**Evidence:**
- Limb 1: D5 is the only intake-class closure (L357). No second closure, so the verdict is AMBIGUOUS.
- Limb 2: 0/2, with no post-mark increment. The 10-21 pass is a naming pass, which doesn't increment (L154(b)). Not fired.
- Idle guard: H-OD-1 and H-TSMOM-1 scored screen-PASS on 2026-07-16 (`H-TSMOM-1-ES-tsmom-scoping.md:20`). Read literally, they are "screen-PASS seeds beyond D5". The 08-16 addendum (L233) nonetheless treats the intake as parked, with the idle guard "the operative limb". The three `admission-date: 2026-07-20` briefs (NG-EIA-1, RATES-EV-ZF-1, ORB-ZB-1) were UNSCREENABLE δ-extraction probes, not screen-PASS seeds. No admission since.

**What changed:** with Requirement 5 deleted, limb 2's "Stage-2 cost-law" kill class has no 4× bar, so future increments need a cost reading from the run's own pre-registration. Rule 26 doesn't touch §4.
**Recommend:** name the intake idle and keep it as dormant doctrine. Limb 1 AMBIGUOUS, re-test 2027-02-08. Limb 2 0/2, not fired.
**Decide:** (a) name the intake idle (recommend yes), or rule that the 07-16 screen-PASSes satisfy the guard; (b) accept limb 1 AMBIGUOUS and limb 2 0/2.

## 5. Regime-monitor successor (decompound HOLD)

**Owner:** [ADR 2026-06-07, Addendum 2026-08-03 §6](../adr/2026-06-07-decompound-remc-hold.md).
**Criterion** (L316-318): "**AMBIGUOUS** — no live fill has occurred by the **2026-11-08** review, so the successor remains unbuilt. Then the gap is **≥3 months old** and must be re-raised in that cycle's programme audit as a standing-unfalsifiable finding, not rolled forward silently."
**Evidence:** there is no live strategy-signal fill. "The HOLD is now unfalsified and, until the successor lands, unfalsifiable" (L285). M-A's build-gate scope is still unruled ([Q-MONSURF-1:40](../briefs/closures/Q-MONSURF-1-closure-resolved.md)).
**What changed:** the HOLD covers the legacy decompounded CFD book, which has no live venue ([AGENTS.md §Strategy Reference](../../AGENTS.md#strategy-reference-locked-legacy-book--do-not-modify)). The program is now the ORB+Aegis book. Forbidden move 4 (L305) bars closing the gap by deleting the falsifier.
**Recommend:** AMBIGUOUS. Re-raise it as standing-unfalsifiable. Ask whether to retire the HOLD by record as moot for a non-live book, since the falsifier is retired with its object, not deleted.
**Decide:** (a) accept AMBIGUOUS and the re-raise; (b) retire the HOLD by superseding record, or keep it suspended; (c) the M-A build-gate ruling (does it need a live fill?).

## 6. Blind channel status

**Owner:** [ADR 2026-08-15 §4](../adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md#4--falsifiable-hypothesis); [analogue ruling](../adr/2026-08-15-analogue-modality-route-ruling.md).
**Criteria:**
- L79: RESOLVED if "≥1 candidate clears the full battery + N-SURV OOS by 2026-11-08."
- L81: "`AMBIGUOUS-HOLD` if: zero candidates are *sourced* at all (not merely zero finished) by 2026-11-08 — re-test at 2027-02-08".
- N=3 rule (L297): "**N = 3 consecutive countable pre-G0 kills ⇒ the channel reports generation-dry**".
- Analogue gate (ruling L30): "if no algorithmic-analogue construct ever opens a manifest, this ruling was inert and should be recorded as such".

**Evidence:**
- The §10 hook (L121) returns empty: no manifest or lab file cites the channel.
- Pre-G0 count: "2 / 3" (L321), unchanged since 08-23 (L450). N has not fired.
- No analogue manifest exists. `MNQ-ANALOGUE-1` died pre-G0.
- Open item: `Q-VOLREGIME-1-intraday-bar-volume-regime.md:59` calls `discovery_manifests/mnq_dailygeom_notice_20260829.json` "`--lane blind`, K=5, closed". The JSON has no lane field, and K=5 exceeds the channel's K ≤ 3 ceiling, so it doesn't read as a channel candidate.

**What changed:** Rule 26 makes the CON-5 pause and class bars advisory. The K ≤ 3 ceiling is the channel's own frozen gate and still binds.
**Recommend:** AMBIGUOUS-HOLD, with disclosed pre-G0 count 2/3, not generation-dry. Record the analogue ruling as inert. Re-test 2027-02-08.
**Decide:** (a) accept AMBIGUOUS-HOLD; (b) rule that the 08-29 notice manifest is not a channel candidate; (c) record the analogue ruling as inert.

## 7. Regime-candidate flag lane: two-strikes check

**Owner:** [ADR 2026-07-26 §4](../adr/2026-07-26-regime-candidate-flag-lane.md#4--falsifier-revert-trigger).
**Criterion** (L101-104): "**if** the first **two** flag-lane follow-up campaigns both close with their reserved-holdout confirm FALSIFIED … this ADR is reverted".
**Evidence:** hook 4 (`grep -rli "REGIME-FLAG" docs/briefs/closures/`, L199) returns empty. No follow-up has closed. The 08-29 addendum (L325) records "no flag-lane follow-up has closed".
**What changed:** nothing bearing on the check.
**Recommend:** not fired (0 closures). Carry it to 2027-02-08.
**Decide:** accept "not fired".

## 8. Candidate contract and channel review

**Owner:** [candidate contract, First review](../adr/2026-08-30-candidate-contract.md#first-review-and-unresolved-obligations); [liveness contract](../methodology/strategy_harvest.md#channel-liveness-contract).
**Criterion** (L141-145): "For any ceiling that has fired, test whether it was UNREACHABLE or UNBINDING, or needed an ad hoc override to enact its already-declared consequence. … Missing examples are inconclusive, not PASS". L134-137 asks for an inspection of freeze chains for founding/Confirm leakage, duplicate side-records, probe accounting, fixed confirm families and EVIDENCE-VOID retries.
**Evidence:**
- One ceiling has fired: MSL's yield-conversion hard rung, 2026-10-07, enacted by ruling D7 on 2026-10-25 ([MSL ADR:3,10](../adr/2026-08-12-msl-sourcing-channel-ratification.md); [plan:257](../superpowers/plans/2026-10-25-rule-consolidation-step-1.md)). It was reachable and binding, and it enacted its declared consequence (closure) without an override, 18 days after it fired.
- The five adoption amendments are still owed (table, L165-171). The five liveness reconciliations are still owed ([strategy_harvest:91-93](../methodology/strategy_harvest.md)).
- The builder declares no liveness ceiling (no match in `lab/builder/`). The liveness contract applies "to newly authored/amended channels" (strategy_harvest:91).
- No campaign ran in the window, so the freeze-chain items have no examples (inconclusive).

**What changed:** MSL is retired, so four channels remain for adoption. The builder is new.
**Recommend:** record the MSL firing as reachable and binding. Carry the owed adoptions with MSL dropped. Rule whether the builder is a sourcing channel that owes a liveness ceiling. If yes, it needs one before its first campaign.
**Decide:** (a) accept the MSL reading; (b) does the builder need a liveness ceiling (recommend yes); (c) re-date the owed adoptions and reconciliations.

## 9. Evaluation and rejection review

**Owner:** [evaluation order, First review](../adr/2026-08-30-evaluation-order.md#first-review-and-unresolved-obligations).
**Criterion** (L166): "initial consolidated review 2026-11-08; immediately on a change to either cost authority or its scope." Scope (L168-172): out-of-order runs, reachability arithmetic, verdict precedence, register placement and N_expr overrun.
**Evidence:** cost authority changed on 2026-10-24, when Requirement 5 was deleted (header L7). That made the immediate limb due, and no review record was found. No campaign ran since 08-30, so the run-level items are inconclusive.
**What changed:**
- Rule 26 turns rejection-register entries into disclosed priors. "Lifecycle rejection based only on fit" (L170) now sits beside an advisory register.
- The builder's gates 5a–5g are a second evaluation sequence, and their relation to the ten-step order is unstated.

**Recommend:** hold this review now. Rule whether the builder's gates are an expression of the ten-step order or a separately owned order (Rule 29).
**Decide:** (a) accept the overdue 10-24 trigger as discharged by this sitting; (b) the builder-gates relation to this owner.

## 10. Mechanism-sourcing radar: progress and idle checkpoint

**Owner:** [strategy_harvest §2.4](../methodology/strategy_harvest.md#24-standing-radar-cadence--zero-new-code-shape-pre-check-added-2026-08-24).
**Criterion** (L129): the radar "Rides the existing quarterly review dates already on the forward board (2026-08-08, 2026-11-08)"; each pass has steps (1)-(5). STATE (L126) says: "on demand; progress/idle checkpoint 2026-11-08."
**Evidence:** no §2.4 pass is recorded since 08-24. The only sourcing work is the 10-21 zero-K published-rule pass, which used none of steps (1)-(3) and found nothing admissible (note:70).
**What changed:** the shape pre-check (step 4) is scored against `Tradeify_Select_100K`. The 10-29 order of expansion makes later-firm strategies the research need, and the builder now generates candidates internally.
**Recommend:** name the radar idle. Either retire the cadence in favour of the builder, or re-aim one pass at strategies distinct from the Tradeify release (later firms).
**Decide:** idle and retire, idle and keep on demand, or fund one pass (scope).

## 11. GRAND-tier ADR §4: scheduled re-read

**Owner:** [ADR 2026-08-09 §4](../adr/2026-08-09-grand-tier-quintessentials-binding.md#4--falsifiable-hypothesis-this-adrs-own-falsifier).
**Criterion** (L183-185): "zero decision-differences through GSUB-1 **and** through the armed sunset window **falsifies** the tier as load-bearing."
**Evidence:** H held on 08-09, with 19 dispositions and "the sunset review does NOT arm" (L273-276). The §10 PARK hooks pass (check 1). Check 1 itself forces three explicit decisions at this sitting.
**What changed:** nothing in §4. The program audit for this slate rides §2.6 (L155-160).
**Recommend:** re-read, no action. The tier stays load-bearing.
**Decide:** confirm that the re-read is complete.

## 12. MNQFLOW-1-DEPTH revisit

**Owner:** [PREREG_S2B](../../lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG_S2B.md); [STATE:131-135](../../STATE.md#no-fixed-date--gated).
**Criterion** (S2B:3,10-11): "`HOLD 2026-08-23 (operator) — value-uncertain, not cost-blocked.`… naturally revisited at the 2026-11-08 slate". STATE wake: "data source approved".
**Evidence:** MBP-10 depth has no approved source, and TV exports carry none (STATE:132-133). Databento is retired.
**What changed:** the HOLD is now data-blocked as well as value-uncertain. ORB-MNQ is in the target book, so depth-conditioned ORB evidence would bear on the 0.25 target. It can't run until a depth source exists.
**Recommend:** keep the HOLD, with the single wake "data source approved". Drop the dated revisit.
**Decide:** keep the HOLD (wake on data source only), or decline.

## 13. Prop-portfolio §4 primary falsifier (research facts only)

**Owner:** [four-firm ADR §4](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md#4--falsifier-revert-trigger); [withdrawal ADR](../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md).
**Criterion** (L81): "by **2026-11-08**, no pre-registered portfolio candidate clears the pass-rate ceiling on **any** `AUTOMATION_FRIENDLY_PROP_FIRMS` tier in a dated lab re-MC → demote this program to **research-only**". The ceiling is 5.0% (10-16 addendum, L384). Its scope is the falsifier only (10-28, L415-418).
**Evidence:**
- The only dated re-MC returned "**FALSIFIED — early-fail**", and §4 stays undischarged (withdrawal ADR, 10-06 addendum).
- The fresh candidate, ORB MNQ v7, is "paused by Joshua, not closed", and its 10-23 freeze and 10-30 re-MC schedule "is overtaken" (L394).
- No other pre-registered candidate exists on `main`.
- FXIFY Futures counting conditions (a)-(c) (L398-401) are not evidenced here.

**What changed:** the 10-29 ruling makes this program the single operating objective. Its "Not changed" (L435-438) keeps the hard date and the demotion rule. The 10-28 scope addendum keeps the account's own objective separate from §4.
**Recommend:** the revert trigger reads fired on 11-08, because no clearing dated re-MC exists. Under Rule 28 the remedy is due and the verdict is Joshua's. The revert action is "supersede this ADR" (L85).
**Decide:** (a) record the trigger as fired on 11-08; (b) the remedy: demote to research-only by superseding record, or another superseding disposition. This decision is the deployment coordinator's adjacent call, and this packet supplies research facts only.

---

**Needs local read:** none of the 13 verdicts above depends on `local_artifacts/` or the archive. Two cross-checks were not run: check 2's closure-note look enumeration (public), and check 13's FXIFY (a)-(c) status (public owner files). Out of scope: the STATE 11-08 queue attention/order review.
