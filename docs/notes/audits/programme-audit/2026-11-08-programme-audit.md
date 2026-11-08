# Programme audit: First Passage, 2026-08-14 to 2026-11-08

**Requested by:** Joshua, 2026-11-08. **Window:** the public repo's start (2026-08-14, the switch to
automation-friendly CME futures firms) to today. **Trigger:** directed audit, plus degeneration
signals (a fired falsifier, gate changes after outcomes, three-month zero-fill streak).
**Method:** Lakatos programme audit (seven diagnostic questions per layer, five verdicts). Nine
parallel stream auditors read the repo and full git history: firm strategy, candidate funnel, live
pair, execution path, risk and falsifiers, governance, methodology, engineering and critical path.
One skeptic per stream re-checked every finding. A completeness critic added four gap streams
(economics, verifier independence, third-party exposure, human attention), which had no skeptic pass
and are marked **[unverified]**. Object-layer and meta-layer sections were synthesised separately and
do not cite each other. The orchestrating session spot-checked the headline counts (DD constants via
`git log -S`, verdict words in commit subjects, rail line counts at 59912c6c and HEAD, AGENTS.md
word counts). **Codex challenge: pending** (requested on this PR).

No backtest dollar figures, parameters, account data or Licensed data appear in this note. The
gate thresholds it mentions are already public in the registrations.

**Bottom line.** The programme is not yet progressing toward passing and scaling Tradeify accounts. It has made progress toward being able to *attempt* a pass. A native NinjaScript build (S-PAIR) is tested on Sim101, a spec and session procedure are accepted, and native-only is now a hard rule. But nothing has been shown about whether the strategy can pass. Over 12 weeks, commit subjects record 15 FALSIFIED, 3 NULL, 2 ABANDON and 0 CONFIRMED. The only market claim marked RESOLVED was retracted the next day (48d55e7e). The nominated pair failed its own exploratory re-test ("PRIOR STANDS"), and D1 accepted that as risk. No strategy-signal fill has happened on the account (STATE.md:58-59). The only content test left is the forward stop rule, and it is private. "Scale" has no model behind it: there are no funded, payout or scaling rows in `core/firm_rules.py`, and exclusivity limits scaling to Tradeify.

## Key findings

1. **Gates moved after adverse results, always toward looser.** Examples: the ceiling raise (53e35eb3), the §5 override (7a7d01c3), G2 removed with "Nothing replaces it", the ceiling scoped off the account (786b6921), Rule 26 made advisory (62c9d93e), and Rules 23-28 deleted (722b920c). By hand count, rule-level changes ran about 9 loosenings to 5 tightenings. Every admission-bar change loosened.
2. **A falsifier's consequence was rewritten after it fired.** The §4 four-firm test came back FALSIFIED on 10-06 (b2d6c934). Its consequence was narrowed on 11-03, while Rule 28 ("falsifiers never move") was still in force. Rule 28 was deleted two days later.
3. **The cheapest falsifier ran last.** The rail grew from about 5.2k to about 56k lines on a route the venue was never asked about. One question, answered on 10-12, barred it. The native route, dismissed "for convenience" on 07-18, is the one that survived.
4. **Measurement got more honest even as decisions loosened.** Since 09-12, registrations carry no results in the same commit. Hashes are pinned in public, the K ledger was re-banked strictly (D14) and retractions stay on the record. The 11-05 cut was a real prune: gates went from 42 to 7.
5. **The controls that matter can't be audited.** The frozen DD constants are untouched (`git log -S` returns only 027a7295). But the binding controls are private and, apart from the stop rule, not hash-registered: the operator loss stop (B6), the native DD tier and the 10-28 account objective. Load-bearing venue facts (T1, T2, Q5) have no written answer from a human.

## Verdicts

| Sub-programme | Layer | Verdict | Reason |
|---|---|---|---|
| Multi-firm scaling | Object | Falsified | §4 failed (10-06, formally 11-08); exclusivity also blocks it |
| Tradeify Select 100K route | Object | Degenerating | Eligibility trigger not assessed; tier never compared to alternatives; venue facts unanswered |
| Live pair (O-0 + A-0) | Object | Degenerating (one test pending) | No gate passed; standing rests on gate removals and D1 |
| ORB-MNQ/legacy generation | Object | Degenerating | No corroborated content; at least 9 repair loops |
| November generation channel | Object | Ambiguous | Clean method, no yield yet; re-test by 2026-12-18 |
| Execution: native | Object | Progressive (provisional) | Tested build in about 3.5 weeks; not yet run on the eval |
| Execution: rail | Object | Falsified | Venue barred it; code deleted (#1002, #1122, #1152) |
| Risk parameters | Object | Stable, wrong surface | Constants intact; binding controls private |
| Governance | Meta | Degenerating | AGENTS.md regrew to 1,944 words in about 3 days; authority rules reversed; Claude settled disputed rulings |
| Methodology: decisions | Meta | Degenerating | One-way loosening; negative heuristic deleted |
| Methodology: measurement | Meta | Progressive | Freeze-before-run, hash pins, K re-bank |
| Pre-registration | Meta | Progressive | Result-free registrations since 09-12 (exception: 8107fef8) |
| Verification (agent review) | Meta | Ambiguous | Substantive on code; unproven on private data and rulings |
| Engineering | Meta | Degenerating, now Stable | 56k lines on an unasked route; now clean but off the live path |

## Decisions for Joshua

1. **Gate and falsifier freeze.** (a) Gates stay open to change. (b) Freeze the gate set until session 1 is scored, and add the AGENTS.md rule that a fired remedy changes only through a new registration made before the outcome is known. *Recommend (b).*
2. **What counts as a result.** (a) Keep D1 as it is. (b) Before session 1, publish which stop-rule outcome labels count as corroboration and which retire a leg (labels only), pre-register that a bust retires the pair, and cap resets. *Recommend (b).*
3. **Venue falsifier.** (a) Handle case by case. (b) Register a dated Tradeify-route falsifier, and send Q5, T1 and T2 as one ticket right after the 11-10 rehearsal. *Recommend (b).*
4. **Disputed rulings.** (a) Claude settles them at your direction. (b) You see Claude's and Codex's positions side by side, verbatim, and rule. *Recommend (b).*
5. **Keeping the 100K.** (a) Keep it and record that the reason is ownership, not evidence. (b) Also make any reset or new purchase depend on a pre-registered comparison of native-friendly tiers. *Recommend (a) and (b) together.*

Caveats: Codex has not yet challenged either section. The meta layer's gap-stream claims (review-rule counts, Codex positions on the loosenings) are unverified. STATE.md:15-16 still lists the August-gate re-run as Research's next task, though it ran on 11-07.

---

# Part A. Object layer: mission and portfolio

Scope: firm choice, candidates, the live pair, the execution path, risk parameters and falsifiers. Governance and methodology quality are not used as evidence here. Only findings the skeptic pass marked confirmed or partly are used; partly findings appear in their corrected form. Private items are marked unverifiable. No dollar figures, parameter values, bust rates or account data appear below. Ceilings are named "the v1 ceiling" and "the raised ceiling".

## 1. Programme statement

**Hard core**, as the window's record states it: automated futures strategies, run on automation-friendly CME prop-firm evaluations (Tradeify Select 100K first), can pass an evaluation and then scale across funded accounts. Since 2026-10-29/30 the operative core is narrower: pass the owned Select 100K with a native NinjaScript strategy (ORB + Aegis), then scale within Tradeify (four-firm ADR 10-29/10-30 addenda, 99c67ec5; STATE.md:9-11).

**Protective belt** (main items):
- the AUTOMATION_FRIENDLY_PROP_FIRMS registry (core/firm_rules.py:649-669);
- the survivor-scoring bust ceiling and its scope rulings (53e35eb3, 786b6921);
- the §4 multi-firm falsifier and its addenda;
- the rejection register's re-proposal bars (Rule 26, 62c9d93e);
- the G2 cost hurdle;
- the T00 book-lineage K ledger;
- the ORB v7 §4 pre-registration;
- the execution route: c1 Python rail via CrossTrade until 10-29, native NinjaScript after;
- the frozen DD constants and locked allocations (money control 4);
- the forward stop rule plus Addendum 1 (879b5896, PR #1005/#1010);
- sitting rulings D1-D3 and D8.

**Negative heuristic**: do not abandon "pass the Tradeify eval with automation". Adverse results are absorbed by changing the route, the firm set, the gate or the candidate, never by giving up the venue-and-automation core.

## 2. Diagnostic questions

### Q1. Hard core integrity

The core term was redefined without running its own trigger. Tradeify was admitted on 07-12 under the "attended-automation bar + CrossTrade/NT8 rail" (f2c4ae3 four-firm ADR:23). That ADR's secondary eligibility trigger (:84) says to remove a family if the firm bans the route. On 10-12, Tradeify support barred bridges and external engines on evaluation accounts (f2c4ae3 route assessment:368-383). The trigger was never formally assessed for Tradeify, even though the 10-16 addendum applied it to FXIFY four days later (ADR:400). Tradeify is still in the registry, and tests/core/test_automation_friendly_prop_firms.py:7-15 still asserts five families.

Correction from the skeptic pass: the trigger text targets a ban on webhook/EA/semi-auto. Tradeify still allows native NinjaScript, which is the EA analogue, so whether the trigger fired is contestable. The label "automation-friendly" was informally reclassified to mean "native-only" (10-14 screen; 10-25 pointer). It was never re-screened.

The "scale" half of the core has no model behind it. firm_rules.py holds evaluation rows only, with no funded, payout or scaling rows (register T8 at b7eaff7:259). D3 says "Admission is owed before any scaling". Tradeify's 10-24 exclusivity guidance (a strategy run at Tradeify may not run at another firm), and D4's extension of that bar to "the same logic on any instrument", mean scaling can only happen inside Tradeify.

The code-level frozen controls are intact. `git log -S` on DD_TRIGGER and on DD_SCALE returns only 027a7295. The allocations moved verbatim under a GO (94041d94). BOOK_SOURCES.sha256 has had no hash edit since ee49308f. These controls guard surfaces that no longer trade, though: the live account loss stop is operator-held and private (spec B6, :61), and the native DD tier runs "under an explicit exception, not an admission" (D3).

### Q2. Belt churn balance

Method: dated rule, gate or ruling changes and registry entries per sub-stream, counted from ADR addenda (`git show f2c4ae3:<adr> | grep '^## (Addendum|Evidence note)'`), gates and registrations. The numbers below are the skeptic pass's corrected ones.

| Sub-stream | Adds | Removes | Ratio | Note |
|---|---|---|---|---|
| Firm/venue (4 venue ADRs: 6+5+4+9 = 24 addenda; registry; prereg v2) | ~18-20 | ~8-10 | ~2:1 | Registry is append-only: 4 families/13 tiers at 027a7295, 5/15 at HEAD. Personal_Tradovate (:613) is still listed after the 10-29 lane closure |
| Candidate funnel (gates and bars on admission) | ~15-20 | ~8-11 | ~2:1 | 10de23ba deleted 12 register headings under an additions-only rule |
| Live candidate (gating status of the pair) | ~22-40 (granularity) | ~6-8 true gate removals | 3:1 or more | Almost every remove is a loosening (G2, M1, P2, U-tests, ceiling scope) |
| Execution path | ~35-40 | ~20-22 | ~2:1 | Rail code: ~5.2k lines at 09-10, ~56.2k at 10-12 (59912c6c), ~2.3k at HEAD |

**Direction.** For ceilings and bars, every change loosened. The exceptions are the 10-02 tightening to an intraday-honest clock, the honoured FLOOR-HALF NO-GO and the D14 K re-bank. Across the window, rule-level gate changes come to roughly 9 loosenings against 5 tightenings.

**Venue pivot count.** 8 in-window pivots, 4 of them reversals of earlier rulings: F1 ruled 08-23 and reversed 09-01; the 09-03 re-admission withdrawn 10-02; the personal lane reopened 10-09 and closed 10-29; Track B superseded 10-16.

### Q3. Progressive evidence (novel content predicted before the outcome)

- **The 08-22 base case predicted that the §4 falsifier would read FALSIFIED by 11-08** (0723587d:STATE.md:28). It did, through the 10-06 pre-registered dated re-MC (PR #715, 11c6007b) and formally on 11-08. That is a correct pre-registered prediction, but it is a refutation of the programme's own multi-firm claim.
- **The 10-19 composition grid predicted that adding ORB legs to Aegis increases bust** (f96a657 checklist:999). The 11-07 re-test is consistent with that. Caveat: the grid used book ORB legs, not O-0, so this counts as a prior, not a test.
- **Native-route adoption**: a Sim101-tested private build (S-PAIR) existed by 11-06, about 3.5 weeks after the 10-13 compliant-routes note (84101f6c). The rail ran from July to October and sent no strategy order. Native beat rail to a deployable artefact. This is provisional, because the build has not yet run on the eval.
- **Absent: any corroborated market prediction.** Commit subjects since 08-14 show FALSIFIED 15, NULL 3, ABANDON 2, CONFIRMED/CORROBORATED 0. The one RESOLVED market claim, Q-RANGECOND-1, was retracted the next day (48d55e7e). D1 records "no out-of-sample edge is established". The only weak positives:
  - a solo Aegis cell cleared the v1 ceiling on the EOD clock only (062e0288, §11);
  - size-feasibility returned FEASIBLE at fractional sizing (982f3edd). It is a necessary condition only, and it is exposed to the 10-20 cost-basis bias (c022e8b3).
- **The "honest clock predicted, then corroborated" claim is not established.** Help article 10495897's 10-15 modified date does not show priority. Tradeify's own marketing also contradicts the article (register A2.2).

### Q4. Degeneration evidence

1. **Gate loosening after adverse results on the incumbent target.**
   - 08-26: the ceiling was raised (53e35eb3) after a measured combined-book result failed the v1 ceiling. The both-halves corrections that reversed the headline (1d7a1a5f, 08b03365) were already committed before the raise. The raise followed Known Trap #12 procedure (v1 closed, v2 opened) and was disclosed, but it is post hoc in substance. 5% had been declined on 07-13. Mitigation: the 09-04 D20 criterion already used a 5% figure, so the number was not invented after the failure.
   - 09-03: candidate #1 was re-admitted through the move §5 forbids, with the superseding-ADR requirement waived (discharge-withdrawal ADR:177-186). It was withdrawn 10-02.
   - 10-24: G2 removed, "Nothing replaces it".
   - 10-28: the ceiling scoped so it does not bind the account. The account's objective now sits in a private owner record and cannot be audited.
   - 10-30/31: Rule 26 made rejections advisory priors. Honest K and in-run gates still bind.
   - 11-05: M1, P2 and the U-tests were replaced.
   - 11-08: D1 waived the pre-session evidence case.
2. **The nominated pair re-enters guarded ground and failed its own re-test.** The register's 08-03 rejection of ORB-MNQ-1 on Select 100K (rejected_candidates.md:1352-1400) and the Aegis H-SOLO bar against "composing ... to dilute" (:390-397) both guarded this area. Correction: the ORB entry's literal scope is the frozen ORB-MNQ-1 construct, so O-0 is arguably outside it. The 11-07 exploratory re-test failed in both halves and its verdict was "PRIOR STANDS" (pair_evidence_case RESULTS.md:3-14). D1 accepted that verdict as risk (rulings:85-100). The test carried no pre-committed action mapping, so it worked as disclosure, not as a gate.
3. **The candidate's own pre-registered test was bypassed.** ORB v7 S4 was ratified on 10-17 and re-ratified on 10-18 (0da31012, 1ee3f07b). Its status still reads "NOT FREEZE READY". It was paused 10-19, marked "overtaken" 10-26 (b2e25b8c) and withdrawn unscored by a ruling on 11-03. The v1→v7 tuning K stays "explicitly unreconciled".
4. **Lineage lanes expired by name while their constructs continued.** b1 (Aegis→6J) and b3 (ORB-MNQ payability) moved PARK→SUBTRACT on 11-03 (6596640b), while Aegis A-0 and ORB O-0 are the nominated pair.
5. **The candidate is not uniquely identified.** STATE.md:9 says "ORB MNQ v7"; the stop rule and evidence case say "O-0"; trial 13 used O-N; the eval build is O-0 plus four D7 changes, with parity described as "limited". D1 states that no O-N or model evidence transfers to O-0.
6. **SNAG shield.** The ORB-MNQ domain had at least 9 repair or conditioner loops in the window (bcef3e07, d0dcdada, 1e17bcc1, 9d70a64e, 48d55e7e, e7cef29a and others). Domain SNAG escalation requires the incumbent to be retired to 0 (rejected_candidates.md:1469,1496). That shield was inherited from before the window.

### Q5. Boundary respected

- **Money control 4 held at code level** (see Q1).
- **A bridged order crossed what proved to be a venue boundary.** X-1 (09-30) sent one REST order through CrossTrade to the eval, on a conditional 09-28 answer. Joshua placed it by hand. The drill plan itself had noted that a firm-level classification is not enough (e997eb20:87). The 10-12 replies then barred that route class.
- **Venue facts the attempt rests on are not confirmed by a human in writing.**
  - T1 (preservation-trade shape) and T2 (agent operation) are open; Q5 has not been sent (D8-D10).
  - The different-instrument exclusivity answer is AI-authored.
  - The Tradeify rows cite a 07-10 verification with a "re-verify" warning (firm_rules.py:235-237).
  - The help centre returned 403 and was read through a mirror.
- **The registry contradicts STATE.** It still calls the set the "operational target" (firm_rules.py:12-15, :649) after the 11-08 demotion.
- **The deciding controls are unauditable.** The live falsifier (stop rule v11), the account loss threshold (B6) and the account objective (10-28) are all private and, apart from the stop rule, not hash-registered.

### Q6. Theory comparison

Firm and tier choice was never re-selected inside the window. The Select 100K was bought on 07-18 for a book and a route that both died in the window: Striker was withdrawn 08-04, CrossTrade was barred 10-12, and c1 was retired 10-29. Three model analyses favour the lower target-to-drawdown 50K tiers over the owned 100K: the 10-21 payout memo, PASS63 (acf4a038) and the 11-04 atlas (RESULTS.md:55-79). These are synthetic inferences, not performance of the live pair.

Option C ("Fresh Select 50K") was declined on 11-08 for spend approval, re-registration and consistency with 11-05, not on a comparison (sitting-options.md:120-130). The 10-14 screen of 54 firms recommended written permission questions to four alternatives. None was sent before 11-03, and the later outreach asked about exclusivity, not automation permission. The retained 100K therefore rests on ownership, the existing registration and timing.

On routes, the native route rejected on 07-18 "for convenience" (c1_nt8_sizing_host_impl.md:138) is the one that survived.

### Q7. Falsifier check

| Falsifier | Original threshold | Current | Fired? | Honoured? |
|---|---|---|---|---|
| §4 four-firm programme falsifier (07-12) | Candidate clears the pre-registered ceiling on ≥2 friendly tiers by 2026-11-08, else demote "this program" to research-only and revert to R6 | Consequence narrowed by a 11-03 ruling: only the multi-firm claim is demoted; Tradeify scaling continues; R6 declined (its lane was closed 10-29) | Yes (10-06 re-MC; formally 11-08) | **Partly.** Recorded honestly; remedy rewritten after the outcome was known |
| Survivor-scoring ceiling (v1, 07-13) | v1 ceiling, with 5% explicitly declined | Raised (08-26), then scoped off the account (10-28) | Yes (failed 08-26) | **No.** Moved |
| 10-06 four-firm dated re-MC (frozen 10-05, 575141b2) | Intraday-honest clear | Closed | Yes (FALSIFIED early-fail) | **Yes** |
| 07-12 secondary eligibility trigger | Remove a family that bans the route | Not run for Tradeify | Contestable (bridge banned, native allowed) | **Not assessed** |
| 07-17 c1 revert trigger (c) | Tradeify ToS/automation change detected during wiring | Rail retired | No: keyed to public-text change; the ban was pre-existing and unasked | **N/A.** Mis-specified |
| Register re-proposal bars (ORB-MNQ 08-03; Aegis H-SOLO) | Binding until stated evidence | Advisory (Rule 26) | Pair re-enters guarded ground (scope contestable for O-0) | **No.** Demoted |
| G2 cost hurdle | Universal hurdle | Removed 10-24 | Not tested on the pair | **No.** Removed |
| August combined-book gate, re-run on the pair 11-07 (exploratory) | v1 ceiling, both halves | Accepted as risk (D1) | Yes ("PRIOR STANDS") | **No.** Informational only by design |
| ORB v7 S4 prereg (10-17/18) | Freeze by 10-23, re-MC by 10-30 | Withdrawn unscored | Never ran | **No.** Bypassed |
| b1/b3 PARK lanes | Expire 11-08 → SUBTRACT | SUBTRACT recorded | Yes | **Formally yes**; constructs continue under new names |
| FLOOR-HALF successor screen (10-11) | Ratified | NO-GO | Yes | **Yes** |
| Forward stop rule + Addendum 1 (10-30/31) | Private (hash-pinned) | Unchanged; any post-session-1 change ends the record | Not yet (no session) | **Unverifiable.** The only live falsifier |

## 3. Disposition verdicts

**Multi-firm scaling route: Falsified.** The pre-registered §4 test failed (10-06; formally 11-08). Venue exclusivity (10-24, D4) also independently prevents any Tradeify strategy from running at other firms. Multi-firm work with distinct strategies remains open only as research.

**Firm/venue route (Tradeify Select 100K): Degenerating.**
- A core term was redefined without running its trigger.
- The falsifier's consequence was narrowed after the outcome was known.
- The registry is append-only.
- The tier was never compared to alternatives on the live pair.
- Load-bearing venue facts (T1, T2, Q5) are unanswered by a human.

Mitigation: Tradeify was questioned before any breach, and the 10-02 tightening was real.

**Live pair (ORB O-0 + Aegis A-0): Degenerating, with one pending test.** No gate on the tradeable pair, or on either leg at tradeable size on the intraday-honest clock, has passed. Its standing comes from successive gate removals and D1's acceptance of risk. The forward stop rule is a legitimate pre-registered falsifier. It is the only content test left, and it is not publicly auditable. If session results corroborate under a criterion written down before session 1, re-score this verdict.

**Candidate generation: two parts.**
- *ORB-MNQ/legacy domain: Degenerating.* No novel corroborated content in 12 weeks; repair loops; register frozen since 09-01 (7db489c4) and pruned against its own rule.
- *November generation channel* (m6e at K=1, DYN-SURVEY-1, builder): *Ambiguous.* The method is clean, but the output so far is one negative result, 16 parked cards and one un-run survey. Re-test conditions: DYN-SURVEY-1 run and recorded, and a ruling on unsealing the 16 cards, both by 2026-12-18. If the channel yields no candidate that passes a frozen gate by 2027-02-08, mark it Degenerating.

**Execution path: Progressive for native NinjaScript; Falsified for the rail.** The rail grew from ~5.2k to ~56k lines (nearly all after 09-10) on a route that was never asked about; it was deleted in #1002, #1122 and #1152. The native route reached a tested build in about 3.5 weeks, and native-only is now a hard rule (money control 3). The progressive verdict is provisional: no strategy-signal fill has occurred in 86 days (STATE.md:58-59).

**Risk parameters: Stable, but guarding the wrong surface.** The frozen constants are untouched. The controls that actually bind the live eval (operator loss stop, native DD tier, account objective) are private, unadmitted or not hash-registered.

## 4. Follow-up actions

| # | Action | Owner | Date | Resolves |
|---|---|---|---|---|
| 1 | Write down publicly, before session 1, which stop-rule outcome labels count as corroboration and which retire ORB O-0 or Aegis A-0. Labels only, no figures | Claude drafts; Joshua accepts | Before session-1 GO (target 2026-11-13) | Live pair, Q3, Q7 |
| 2 | Name one forward-test identity (O-0 eval build hash) in STATE and the stop-rule record; say which evidence it inherits; fix STATE.md:9 and :15-16 | Claude | 2026-11-12 | Q4 identity gap |
| 3 | Hash-register the operator's account loss threshold, the native DD tier configuration and the 10-28 account objective (private bodies, public sha256 in PRIVATE_EVIDENCE.sha256) | Joshua (private); Claude (public index) | Before session-1 GO | Risk params, Q5 |
| 4 | Codex verifies the stop-rule and Addendum 1 hashes in place, and confirms whether the rule can drop a leg before the account's own drawdown is likely to end the attempt (answer in open classes only) | Codex; Joshua starts it | Before session-1 GO | Q7 forward falsifier |
| 5 | Record the secondary-trigger assessment for Tradeify against the 10-12 replies. Relabel the registry as reference/research and record the Futureify rename. Comment-only edits to firm_rules.py need money control 4 approval | Claude; Joshua approves | 2026-11-20 | Firm route Q1, Q5 |
| 6 | Send Q5, T1 and T2 as one compliance ticket right after the 11-10 rehearsal. Log the author type (human or AI) and any clause cited | Joshua | 2026-11-11 | Q5 venue facts |
| 7 | Encode the Tradeify funded-stage rows from primary sources, dated, before any second-account purchase | Claude; Codex reviews | Before any purchase | Scale half of core |
| 8 | Run a pre-registered tier comparison on the pair's own shape, restricted to firms that allow native strategies | Claude; Codex challenges | Before any reset or new purchase | Q6 |
| 9 | Add pointer stubs for the 12 deleted register entries, and override notes on the ORB-MNQ and Aegis entries citing D1 | Claude | 2026-11-27 | Funnel Q2 |
| 10 | Run the deferred size-feasibility FEASIBLE re-read under the corrected 6J cost basis, or mark FEASIBLE superseded | Claude | 2026-11-27 | Live pair evidence |
| 11 | Record DYN-SURVEY-1's result and propose a K for the 16 parked builder cards | Claude | 2026-12-18 | Generation channel (Ambiguous) |

**Decisions for Joshua:**

1. **Venue-level falsifier for the Tradeify-only programme.**
   - (a) None; handle case by case.
   - (b) Register a short venue falsifier before session 1, with a hard date, naming which written answers or outcomes (a "no" on T1/T2/Q5, a source-review objection, a deletion warning, N busts) end or redirect the Tradeify route.

   *Recommend (b).*
2. **What a bust means for the pair.**
   - (a) Keep D1 as is ("a bust ends the attempt; any reset is a fresh spend decision").
   - (b) Pre-register that a bust retires the pair unless forward stop-rule evidence says otherwise, and cap attempts and resets before any re-buy.

   *Recommend (b).*
3. **Keeping the 100K.**
   - (a) Keep it and record that the reason is ownership, not evidence.
   - (b) Make any later reset or purchase depend on action 8.

   *Recommend both (a) and (b).*
4. **Gate freeze.**
   - (a) Allow further gate changes before session 1.
   - (b) Freeze the current gate set until session 1 is scored; any later change needs a fresh registration made before the outcome is known.

   *Recommend (b).*

Codex has not yet challenged this section. This subagent had no route to it, so the orchestrator should send it to Codex for review before publication.

---

# Part B. Meta layer: methods and operating model

**Scope.** This section covers methods and the operating model: governance, agent roles, research methodology, pre-registration, verification and engineering practice. Strategy performance is not used as evidence here. Only findings that the skeptic pass rated confirmed or partly confirmed are used, and partly-confirmed ones appear in their corrected form. The four gap streams (economics, verifier independence, third-party exposure, human attention) had no skeptic pass. Their claims are marked **[unverified]**. Codex has not yet challenged this section.

---

## 1. Programme statement

**Hard core (meta).** First Passage's methods rest on four commitments:

1. Decisions about candidates and venues come from gates registered before results exist, with an honest count of trials (K).
2. Every head is checked by the *other* agent, and no agent verifies its own work.
3. Joshua alone rules and holds the money controls. Agents do the work, and no agent decides a ruling by default (AGENTS.md:22-23).
4. Frozen risk parameters and private sources are not touched.

**Protective belt (main items).**
- The rule corpus: CLAUDE.md, then docs/operational_rules.md (42 rules at f2c4ae3), now AGENTS.md.
- The gate stack in scripts/gates.yml.
- ADRs and their addenda, briefs and notes.
- The pre-registration files and their addenda.
- The rejection register (docs/rejected_candidates.md) and its re-proposal bars.
- The review and merge rules.
- The repo skills.
- Sitting rulings (D1-D20).

**Negative heuristic.**
- Do not move a falsifier or its consequence after the outcome is known (deleted Rule 28: "falsifiers and kill thresholds never move", f2c4ae3:docs/operational_rules.md:152-154).
- Do not re-propose rejected ground without new mechanism evidence (Rule 26 before 10-31).
- Do not let the author settle its own disputes.

---

## 2. Seven diagnostic questions

### Q1. Is the hard core intact?

Partly. Two parts held and two eroded.

**Held: frozen controls.**
- `git log -S` on DD_TRIGGER and on DD_SCALE returns only 027a7295.
- The locked allocations moved verbatim under a recorded GO (94041d94).
- BOOK_SOURCES.sha256 has had no hash edit since ee49308f.
- A pin test exists (tests/core/test_dd_geometry.py:78-79). (RF-1, ENG-11)

**Held: native-only absorbed into the hard rules.** Money control 3 and the Code Review Rules make an external engine or bridge on the Tradeify path a blocking finding. (EX-10)

**Eroded: "gates decide".**
- The written negative heuristic is gone. 722b920c deleted operational_rules.md, which held Rule 23 ("pre-register; count K honestly"), Rule 24 and Rule 28. Current AGENTS.md mentions registration only for the forward stop rule (money control 5). (M8)
- Rule 26 survives only as a banner in docs/rejected_candidates.md:5, which links to the deleted file. (M3, corrected)
- Frozen files still cite deleted rules. The stop-rule registration cites "Rule 23" at line 3.
- The strategy-validation skill links to 4 deleted method documents. (M8)

**Eroded: "no agent decides by default".** At the 11-08 sitting, the disputed rulings were "settled" by Claude "at his direction" (sitting-rulings.md:5-7). Claude wrote the options packet. (Governance verifier's missed item; GOV-05 corrected)

**Caveat.** The frozen controls guard surfaces that are largely inert for the live path. The binding loss control on the eval is operator-held and private (spec B6, docs/spec/2026-11-06-orb-aegis-eval-build-design.md:61). The native drawdown tier runs as "an explicit exception, not an admission" (D3). (RF-2, corrected: the literals are still imported by lab scoring code.)

### Q2. Belt churn: adds against removes

| Belt measure | Adds | Removes | Method |
|---|---|---|---|
| Governance documents (docs/adr, briefs, notes, .claude/skills) plus gate ids | ~960 | ~1,355 | `git log --no-merges --diff-filter={A,D} --name-only` per month, unique paths. August adds are net of the 027a7295 import. Moves count once on each side. (GOV belt; verifier reproduced removes exactly, adds within a few files) |
| Gate ids in scripts/gates.yml | 26 | 36 | First-parent walk since 08-14, diffing `  - id:` sets. 17 at start, 42 at peak (f710fce9, 10-31), 10 after d603e819/#1099, 7 at HEAD. (ENG belt, verifier reproduced) |
| Rule-level methodology changes | 5 tightenings | ~9 loosenings | Hand count, judgement-based. Tightenings: intraday-honest clock (10-02), forward stop rule (879b5896), hash-pinned registrations, D14 re-bank (ae91b388), builder ledger (c6621efe). Loosenings: ceiling raise (53e35eb3), §5 anti-rescue override (7a7d01c3), 4x gate deleted (3cb08f66), component hurdles, Rule 26 made advisory (62c9d93e), Rules 23-28 deleted (722b920c), §4 consequence narrowed (f977c20f), D13, D15. (Methodology verifier's re-derivation) |
| AGENTS.md size after the cut | 511 → 1,944 words in ~3 days | — | `git show <sha>:AGENTS.md \| wc -w` at d603e819 … 3a75bc38. Pre-cut it was 3,303. (GOV-01, reproduced) |
| Review-rule changes | ~13 | ~8 | Hand enumeration. **[unverified, gap-1]** |

**Reading.** The file belt was built and torn down inside the window: 842 deletions came in the 11-05 cut alone. That is churn, not steady growth or steady pruning.

The pre-cut prunes mostly grew back. The tree went from 1,503 files (09-07) to 2,654 (10-09). The one exception is a late-October notes prune that held (2,645 → 2,328). (GOV-01, corrected)

At the rule level the direction was one-way loosening of admission bars, alongside tightening of measurement (clock, K). The October "rule consolidation" grew the rulebook rather than shrinking it: operational_rules went from 8,513 to 11,077 words in a528bcc0. (GOV-03)

### Q3. Progressive evidence

- **Freeze-before-run discipline improved and held.**
  - In August, about 12 commits added about 19 pre-registrations in the same commit as their results, so git cannot show the criteria came first (M5, corrected list).
  - Every pre-registration add-commit from 86f713a0 (09-12) through 89a5ebf9 (11-07) carries no result files.
  - Registrations from late October are SHA-256-pinned in public before any check runs.
  - The atlas froze its design before running (a59a94f7 precedes b7591a10). (FS-8)
- **Self-corrections were real and kept on the record.** Examples:
  - The Q-RANGECOND-1 look-ahead retraction (48d55e7e, found by Codex in PR #227).
  - The promotion-rule violation caught on PR #265 (25028e87).
  - A positive control that invalidated three FALSIFIED verdicts (1e17bcc1).
  - The 10-02 withdrawal of the EOD-clock discharge.
  - The D14 K re-bank, where Joshua chose the stricter option A over Codex's option H. (M6, M7)
- **Fixed-K single-expression probes in November were clean.** m6e ran at K=1, registered before outcomes, and was independently reviewed. DYN-SURVEY-1 fixes K=80 and pins its holdout in code. (CF-8)
- **ADR production stopped once policy changed.** New ADRs ran 46, then 8, then 1, then 0 by month after 5699cdaa. (GOV-09)
- **The 11-05 cut was a real prune, not a relocation.**
  - Gates went 42 → 7 and scripts from about 35k to about 10k LOC.
  - The core/ file count was unchanged, and its only edits were comment-only.
  - D15 retired obligations openly, with named survivors. (GOV-02, ENG-3)
- **Post-cut documents serve the mission by file count.** The spec, the procedure and the sitting notes. By word count the sitting notes outweigh the specs. (GOV-13, corrected)
- **Missing: any corroborated novel prediction.** Commit subjects in the window show 15 FALSIFIED, 3 NULL, 2 ABANDON and 0 positive CONFIRMED. The one market RESOLVED was retracted the next day. (M9, confirmed) The apparatus progressed. The theory it serves did not.

### Q4. Degeneration evidence

- **Thresholds were moved after outcomes, with an anti-rescue clause overridden.**
  - 53e35eb3 raised the survivor-scoring ceiling about six hours after 01e64c5f. Its own message ties the raise to a same-day failing result.
  - Ruling D5 (7a7d01c3, 09-03) then re-admitted candidate #1 "in the OPPOSITE disposition" to its addendum, and waived the superseding-ADR requirement that §5 of the withdrawal ADR imposed.
  - Procedurally, v1 was closed and v2 opened as Known Trap #12 requires. In substance the move was post hoc. (M2; methodology verifier's missed item 1)
- **The falsifier consequence was rewritten after the verdict.**
  - The dated re-MC returned FALSIFIED on 10-06 (b2d6c934).
  - On 11-03 Joshua narrowed §4's consequence, recorded as "changing the falsifier's recorded consequence" (f2c4ae3 four-firm ADR:472-486). This came while Rule 28 was live, and Rule 28 was deleted two days later.
  - Mitigation: Rule 28 reserved "dated verdicts" to the operator. (RF-4)
  - The revert destination (the R6 lane) had been closed on 10-29 (99c67ec5), ten days before the hard date. (FS-2 verifier)
- **Methodology now informs but does not gate.**
  - Under D1, the exploratory 11-07 re-application of the August gate ("prior stands") was accepted as risk.
  - Gating moved to the forward stop rule. Its text is private (registration :7) and cannot be audited publicly. (M1 corrected, LC-7)
  - The pair-evidence options packet recommending no evidence case was committed about 19.5 hours before that verdict. The gate had no pre-committed action mapping, so it worked as disclosure. (LC-4, corrected)
- **Bars were relaxed, but not wholesale.** Rule 26 made rejections "advisory priors" (62c9d93e). The G2 4x cost hurdle was deleted with "Nothing replaces it" (addendum-1:7). Rule 26 still binds honest K, frozen controls and in-run gates. (M3, RF-10)
- **Authority rules reversed faster than they were exercised.**
  - Merge authority: granted 10-24 (f2c4ae3 AGENTS.md:255), revoked 11-07 (7f9a91bb).
  - Agent eval orders: standing GO 10-25 (6b41ac6a), a 'no agents on eval' ruling, reversed 11-05 (ba2d2c86), suspended 11-08 (D8).
  - D8 has an external trigger (Q5). D12 narrows the GO rule rather than reversing it. (GOV-04, corrected)
- **Rulings were made in parallel sessions.** The 11-08 packet "missed rulings Joshua made in other sessions". Five rulings changed and D19 was overtaken (rulings.md:9-24). Q-SFCLEAR-2 and Q-SFCLEAR-3 were ratified and frozen, then superseded or never run. (GOV-06)
- **Output was mostly documents.** Docs-only commits were about 59-74% per month in Aug–Oct, peaking in October. Research-touching commits were 6-7% in Sep–Oct. Percentages depend on the classifier. Merged PRs in the window number about 1,044. (GOV-07, corrected)
- **The cheapest falsifier ran last.**
  - The 07-17 ADR had a venue trigger, but it watched for *changes* in public ToS text. It could never fire on a constraint that was already true and simply unasked (027a7295 ADR:73).
  - P-1 venue permission first appears on 09-26 (028daa8c, e997eb20), and d42c4679 records it as "evidence owed".
  - Building continued. The rail went from about 5.2k to about 56k production lines by 10-12.
  - The 10-12 replies barred bridges. Native-only became the planning default through the 10-13 rule. (EX-1, EX-2, ENG-1; corrected)

### Q5. Boundary respected?

Mostly, with three gaps.

- **Money control 4 held** (RF-1). The only edits to frozen-parameter files after the cut were comment-only (2ce09f30, 62382794).
- **Public CI does not cover the thing that trades.**
  - No .py file mentions NinjaScript (one README does).
  - No public code scores the forward stop rule.
  - nt_readonly_mcp is not referenced by any spec.
  - The Pine and data gates WARN and pass in CI because their sources are absent. (ENG-2, ENG-5)
- **The cut left debris.**
  - 376 of 387 docs paths cited from code, tests and config are missing.
  - check_path_liveness was deleted but is still listed in repo_map_layers.yml:28.
  - 20 dead ADR links remain in .claude/skills.
  - pinescript-v6/SKILL.md:3 cites a nonexistent AGENTS.md section.
  - User-level skills outside the repo (brief-authoring, fxify-challenge, inqhiori) still prompt agents to write ADRs and briefs, against AGENTS.md:9. (ENG-3, GOV-11)
- **Codex lacked the governing text for about three weeks.** Codex was formally excluded at release (027a7295 .gitignore:58-66). It became reviewer around 08-29 (499cde9b), but AGENTS.md was untracked until 09-16 and disjoint from CLAUDE.md until 09-20 (5fae4d2d). (GOV-08, corrected from five weeks)
- **Data and credential exposure.** The third-party-exposure gap stream raised two data-classification and credential-hygiene items. They were reported to Joshua directly and are left out of this public note on purpose.

### Q6. Theory comparison

Three operating models were run in sequence:

| Period | Operating model | Result |
|---|---|---|
| Aug–Sep | Rail-era: heavy governance (42 gates, 42 rules, about 140 ADRs), external engine, research-first | No strategy order, a route the venue bars, belt deleted |
| Oct | Mid-course correction | Native-only, rule consolidation (which grew the rules) |
| 11-05 onward | Post-cut lean model | Spec, procedure and pair-verdict acceptance in four days |

The post-cut stretch is the fastest on record, but the comparison is confounded. Those acceptances depended on 10-12, 10-29 and 10-30 work, and 11-08 was a long-scheduled deadline and sitting date. Causation is not shown. (CP-6, corrected)

The rejected alternative was native NinjaScript. It was available on 07-18, dropped as unnecessary on convenience grounds (027a7295 c1_nt8_sizing_host_impl.md:138), and reached a Sim101-tested build about 3.5 weeks after revival. (EX-3, corrected: PR #807 slightly predates 10-13)

**Verifier comparison.**
- Codex review is substantive at the code and document level. 97 of 559 research-touching commits name Codex, and its findings flipped verdicts and made gates fail closed. (M13)
- For private-data verdicts, the only re-derivation was "an independent Claude reviewer" (pair RESULTS:111-117), the same model family as the author. (LC-9 nuance)
- **[unverified, gap-1]** Codex never blocked any of the seven loosenings. Three have no review recorded in git.

The deleted programme-audit skill defined this audit's own questions. The audit now runs against a framework that no longer exists in the repo. (Methodology verifier's missed item)

### Q7. Falsifier check

| Falsifier | Original threshold | Current | Fired? | Honoured? |
|---|---|---|---|---|
| Rule 28 "falsifiers never move" | Binding rule | Deleted 11-05 (722b920c). No successor in AGENTS.md | Tested by the 11-03 §4 narrowing | **No.** Rescoped, with procedural cover from Rule 28's own "dated verdicts are the operator's" clause |
| Prereg v1 ceiling plus Known Trap #12 and §5 anti-rescue | v1 ceiling. 5% dial declined 07-13 | Raised ceiling (v2). Later scoped off the eval (786b6921) | Yes, 08-26 and 09-03 | **Partly.** v1 closed and v2 opened as Trap #12 requires. §5 overridden by D5 (7a7d01c3). Discharge withdrawn 10-02 |
| §4 four-firm programme falsifier (meta handling) | Hard date 11-08, demote "this program" | Fired. Consequence narrowed 11-03 | Yes (10-06 verdict, 11-08 date) | **Rescoped**, not honoured (RF-4) |
| Rule 26 re-proposal bars | Binding | Advisory priors (62c9d93e) | n/a, loosened pre-emptively | n/a |
| Size-feasibility automatic stop | Stop on no-clear | Replaced by a decision tree 32 minutes after freeze, before scoring (103c5ea5, d104e139) | No | Borderline (RF-12) |
| D14 clause 2-C (K accounting) | Executed-K closures must bank declared K | Fired. Remedy A enacted (ae91b388) | Yes | **Yes.** Stricter than Codex's preference |
| D13 clause 2-A | Research falsifier | Retired by judgement, with a re-arm condition | No | n/a (retired untested) |
| 11-03 checks carried to 2027-02-08 | Dated re-checks | Retired by D15 unless a kept file carries them | No | Retired untested. No public list |
| Q-GATESTACK-1 | "CI is disabled" claim | Falsified (96eaf098) | Yes | Yes |
| Codex-review revert trigger (8-week signal comparison) | Revert if lower signal than Claude | Never computed. Clause deleted 11-05 | Unknown | **[unverified, gap-1]** |
| Forward stop rule (10-31) plus Addendum 1 | Private, hash-pinned (PRIVATE_EVIDENCE.sha256:366-367, :378-379) | Binding. Changes allowed only before session 1 | Not yet | Pending. Not auditable in public |

---

## 3. Dispositions

Written after §2.

- **Governance: Degenerating.**
  - The 11-05 cut is a genuine repair (GOV-02).
  - But AGENTS.md regrew to 59% of its pre-cut size in three days.
  - Authority rules reversed several times without measured cause.
  - Rulings were cut from stale state across sessions.
  - Joshua's ruling role was partly exercised by the author (Claude settling disputes).
  - Recovery condition: by 2026-12-08, AGENTS.md is no larger than about 2,500 words, there are no authority reversals without a recorded trigger, and disputed rulings are shown to Joshua side by side.
- **Research methodology: Degenerating at the decision layer; Progressive at the measurement layer.**
  - Measurement became more honest: freeze-before-run, hash pins, K re-bank, retractions.
  - But every admission-bar change loosened, the written negative heuristic was deleted, a falsifier consequence was rewritten after its verdict, and the gate result no longer decides deployment (D1).
  - No corroborated novel content in 12 weeks.
- **Pre-registration practice: Progressive.** Result-free registration commits since 09-12, public hash pins, and an atlas frozen before running. Exception: the pair DECISION-RULE hash was first published together with its results (8107fef8).
- **Verification (agent review): Ambiguous.**
  - Substantive on code and documents (M13).
  - Unproven as an independent falsifier of private-data evidence or of rulings.
  - Re-test by 2026-11-22: pull the review threads for #176, #291, #894, #895, #949, #1006, #1091 and #1120 at their merged heads. Record Codex's position on each loosening. Score a reviewer-effectiveness metric (findings by class, and the share that changed a verdict or gate).
- **Engineering: Degenerating over the window; currently Stable.**
  - About 56k production lines were built for a route that a single venue question falsified. Venue legality was checked by watching public text, not by asking.
  - Post-cut, the code is healthy: boundaries OK, frozen values pinned. But it sits off the live path, and its gates are vacuous in CI.

---

## 4. Follow-up actions

| # | Action | Owner | By | Resolves |
|---|---|---|---|---|
| 1 | Draft a five-line research core for AGENTS.md (below), plus a one-line falsifier-immutability rule: a fired remedy changes only through a new registration made before the outcome is known | Claude drafts, Codex reviews, Joshua accepts | 2026-11-15 | Q1 erosion; methodology Degenerating |
| 2 | Publicly list every falsifier and dated check retired by D13 and D15, with its trigger condition | Claude | 2026-11-15 | Q7 untested retirements |
| 3 | Add a pre-committed action mapping to any future evidence read (verdict → action), or label it disclosure-only | Claude | Next read | LC-4 |
| 4 | Restore a minimal path-liveness gate (repo paths, including .claude/skills), fix the 4 dead links in strategy-validation, and remove stale entries from repo_map_layers.yml | Claude (Codex reviews) | 2026-11-22 | ENG-3, GOV-11 |
| 5 | Record publicly which gates are vacuous in CI. Log a private-checkout run of the Pine and data gates before each session GO | Claude, run by Joshua | Before the session-1 GO | ENG-5 |
| 6 | Pull PR review threads at the merged heads for the eight loosening PRs. Record Codex's positions, including on the disputed 11-08 items | Codex | 2026-11-22 | Verification Ambiguous; **[unverified]** gap-1 |
| 7 | Venue-permission preflight: no route-specific build without a written venue answer for the exact account and route | Claude (design) | 2026-11-15 | EX-2, ENG-1 |
| 8 | Measure AGENTS.md size, authority changes and docs-only commit share | Claude | 2026-12-08 | Governance re-test |

**Decisions for Joshua**

1. **Disputed rulings.**
   - (a) Claude keeps settling disputes at your direction.
   - (b) **Recommended:** disputed items come to you with Claude's and Codex's positions side by side, verbatim, and you rule.
2. **Falsifier immutability.**
   - (a) Leave it as now: no general rule.
   - (b) **Recommended:** add the one-line rule from action 1 to AGENTS.md.
3. **Authority freeze.**
   - (a) Rules on merges, eval orders and GO cadence stay open to change.
   - (b) **Recommended:** freeze them until session 1 is scored, and allow changes only on a named trigger (a Tradeify answer, an incident).
4. **Belt-only merges.**
   - (a) You click every merge.
   - (b) **Recommended:** you batch belt-only PRs into one daily window, so your attention goes to critical-path heads first.
5. **Private-data verification.**
   - (a) Label such verdicts "single-vendor verified".
   - (b) **Recommended:** give Codex the same read-in-place, hash-checked access for verdict re-derivation that it has for the eval build. Under the current rules Codex is barred from those inputs, so this widens its access and is your call.

---

## Audit hooks for the next cycle

- `git log -S DD_TRIGGER -- core/dd_protection.py` and the same for `DD_SCALE`: expect only 027a7295.
- `git log --since=<last audit> --no-merges --format=%s | grep -cwE 'FALSIFIED|NULL|ABANDON(ED|MENT)?|CONFIRMED|CORROBORATED'`, counting positive verdicts separately.
- `git show HEAD:AGENTS.md | wc -w`. The governance recovery condition is about 2,500 words or fewer by 2026-12-08.
- `grep -c '  - id:' scripts/gates.yml` (7 at this audit).
- The falsifier table: re-read each registration under `docs/briefs/pre-registration/` and diff it against its hash in `docs/evidence/PRIVATE_EVIDENCE.sha256`.
- Re-score the live-pair verdict after forward stop-rule session 1, against the labels committed before the session (Part A action 1).
- Re-test dates: verification (Ambiguous) by 2026-11-22; the November generation channel (Ambiguous) by 2026-12-18.
