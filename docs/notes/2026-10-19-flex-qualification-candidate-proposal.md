# Does FLOOR-HALF merit more investment? One cheap screen before any qualification build (proposal, 2026-10-19)

**Status:** PROPOSAL, revision 2. It responds to the review of #877. It is not execution approval: nothing is run, scored, frozen, bought, sent or admitted, and every decision in §9 is Joshua's.

**Question:** which existing portfolio, on which fresh-evaluation basis, deserves one qualification experiment before native implementation?

**Next decision it informs:** whether the one existing candidate, FLOOR-HALF, merits more investment at all. The proposal makes no firm selection and starts no build. Firm questions, basis selection, schedule changes, venue-specific admissions, firm registration and harness construction all follow only after a promising screen. Each needs its own approval (§5 Step 3).

**Sources:** committed records at `origin/main` `772c0b6`; the open PR branches #867, #869 and #875; relay records in the primary checkout; the public FXIFY Futures and FundedNext Futures pages, read 2026-10-19. No Pine, port, effective-input file, `local_artifacts/`, private report, trade CSV or panel was opened. The research workflows did read outcome labels and aggregates from the records in §8, and private ORB figures relayed through an unreviewed diagnosis transcript.

**Labels:** **DOC** = a record or an official firm page; **INF** = inference or rules arithmetic; **UNV** = unverified.

## 1. Answer

**There is still no supported deployment candidate.** No configuration has any result at a FundedNext or FXIFY tier, and every improvement hypothesis is untested. The evidence supports neither a qualification claim nor an improvement claim.

**Candidate for the screen: FLOOR-HALF.** Its identity is frozen for T00 trial 9 ([#733](../briefs/pre-registration/2026-10-08-tradeify-book-successor-screen-prereg-DRAFT.md) §1a, §2 A1):

| Item | Value |
|---|---|
| Book | The declared book at k = 0.5 under the code's round-down rule |
| Live legs | Aegis 6J1 sells 6J; Striker DJ30 MYM p250 buys MYM; Vanguard MGC v0.4 buys MGC |
| Adds / ORB | Adds as frozen; ORB floored to zero |
| Pins | Size vector `139919cd…c271`; r3d contract `c7a82915…` |
| Book protection | 1% combined-peak trigger, 0.40 scale, prior-close timing |

It reads **FALSIFIED on Tradeify** (§2). It is the least-falsified existing object, not a supported candidate.

**Account bases: provisional comparison only.** FundedNext Futures Flex 150K and FXIFY Futures Flex 150K are the two bases worth comparing (§3). Neither is selected:
- FundedNext's advantages (no evaluation time limit, no news rule) justify the comparison, not a selection.
- Its funded account ends after the fifth reward ([FundedNext funded rules](https://helpfutures.fundednext.com/en/articles/17229848-fundednext-futures-flex-fundednext-account-all-rules)).
- FXIFY's 30-day evaluation clock prices a long pass as extension fees of unknown size.

**Best next step.**
1. A short ruling (§5 Step 1) fixes the usefulness criterion, the screening rule and the Q-SFCLEAR-3 exposure handling.
2. Then one bounded summary read of the existing T00 outputs (§5 Step 2), under its own permission. The read is tallies only, with one optional pre-declared median derivation. It involves no replay and no strategy change.

**Highest-value improvement hypothesis:** a lock-conditioned early-phase size schedule (§7 item 1). It is a separate successor and never part of this candidate.

## 2. What is new since #876, and what is not

**What #876 records.** On 2026-10-19, Joshua ruled: "Record that no book-lineage configuration has an evidence case for the Tradeify eval" ([#876 addendum](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-19--no-book-lineage-configuration-has-an-evidence-case-for-the-tradeify-evaluation)). Its scope includes FLOOR-HALF:
- Under #733 §4 H it reads FALSIFIED, with "the configuration is not adopted".
- Its NO-GO is `UNDETERMINED`-dependent. It fails under the pessimistic intrabar assignment, clears under the optimistic one, and its H2 bust is within 5%.
- Its 10-11/12 risk acceptance into F1 lapsed on 2026-10-16.

This proposal does not recreate the declined rung-R1 Tradeify study and does not revive #873. **There is no new strategy evidence. The only ground for further work is the changed account basis.**

**Changed constraints** (firm rules DOC; consequences INF):
1. **Rope at fixed quantities.** The maximum loss limit (MLL) is $4,000 at FundedNext and $4,500 at FXIFY, against Tradeify's $3,000. FLOOR-HALF's frozen quantities therefore sit at roughly 0.75× and 0.67× of its Tradeify drawdown geometry ([venue note §6](2026-10-14-funded-venue-alternatives-assessment.md) method). This is directional only.
2. **Lock.** FundedNext locks the floor at start + $100 during the evaluation. FXIFY's evaluation lock is an interpretation. Tradeify's evaluation never locks. Beyond plain rescaling, the lock is the only favourable change.
3. **Other changes that can move results:**
   - target-recalculating consistency (FundedNext);
   - the protection trigger's position against the rope ($1,500, or 37.5% of a $4,000 rope, against 33.3% at Tradeify);
   - own-flat time;
   - costs;
   - FXIFY's soft daily loss limit and its 30-day clock.
4. **Fresh, pristine start.** This fits the T00 harness's pristine-only rule ([`contract.py:843-849`](../../ops/c1_rail/qualification/contract.py)).

**Not new:**
- **The panels.** The same 2022-09-01..2026-09-02 panels, all fully exposed (T00 lineage K = 12). Any later run is post-exposure, model-fitted feasibility.
- **Target/rope.** It is 2.0 on both 150K tiers, as on Tradeify.

**Estimates, not falsification.** The recorded constant-size bound `T_min(yr) = (target/rope)·(ln(1/b)/2)/annSR²` ([A2 §2–§3](../../lab/analysis/c1/a2_panel_noise_venue_bound_2026-08-24/RESULTS.md)) is a drift-diffusion model estimate. It assumes a constant size and a never-locking rope. It indicates that a bigger rope at fixed target/rope buys lower bust by lengthening time. At b = 5% (INF from the same formula), the annSR it requires is:

| Pass within | annSR needed |
|---|---|
| 6 months | ≈ 2.45 (A2 banner) |
| 1 year | ≈ 1.73 |
| 2 years | ≈ 1.22 |
| 1,500 sessions | ≈ 0.71 |

For scale:
- The highest annSR in A2's scoped corpus is +1.28.
- The estate also records a gross, CFD-era legacy Aegis Sharpe of 1.83, as an upper bound ([Q-GATECART-1](../briefs/closures/Q-GATECART-1-survivor-gate-cartography.md)).
- No book-lineage Sharpe is published.
- Exploratory, protection-off grid rows ([composition grid](../../lab/analysis/c1/tradeify_book_composition_2026-09/RESULTS.md)) suggest that both bust (H1) and time can bind.

None of this proves FLOOR-HALF fails under different drawdown and locking rules. It shows that time, not only bust, is the risk to test first.

**Target-shopping disclosure.** Moving a parked configuration to a firm with a larger rope is the pattern [rejected_candidates](../rejected_candidates.md) (ORB re-proposal bar, ~:1585) declined as target-shopping after seeing data. This proposal is defensible only as follows:
- it is an operator-directed basis comparison;
- the lock is a new mechanism;
- it keeps any later run behind a fresh GO and a pre-registration.

Stopping further venue shopping for FLOOR-HALF after a negative screen is offered as an explicit research-budget decision (§6), not as a logical consequence.

## 3. Account bases: structural comparison and funded economics

This section is a **derived input** to the coordinator's dated FXIFY-vs-FundedNext note (EMERY-RESEARCH-DOCS-1), which owns firm facts. It is not authoritative and is not a rule sheet. FXIFY sheet corrections go to the #867/#869 writers. All facts were read 2026-10-19.

### Structure

| Fact | FundedNext Flex 150K | FXIFY Flex 150K |
|---|---|---|
| MLL | $4,000 end-of-day (EOD) trailing, updated 17:00 CT, from the "highest balance that day" (ambiguous). An intraday floating touch breaches instantly. Locks at $150,100 | $4,500 EOD trailing. Breach clock unstated ("balance"). The start-balance lock names no stage (sheet B1). An add-on gives $4,750 |
| Target / time limit | $8,000 (closed-P&L basis UNV) / none | $9,000 / 30 days. The reset FAQ treats an ended evaluation as failed. Paid extension, fee and repeatability unpublished |
| Consistency (evaluation) | 40% of target; exceeding it raises the target | 50%, soft |
| Daily loss limit | None | $3,000 soft (read-only for the day); an add-on removes it |
| Contract cap | 8 minis / 80 micros at 1:10; full-size 6J counting unstated | 10 / 100 at 1:10; full-size 6J counting unstated |
| Instruments | 6J (full only), MGC, MYM and MNQ listed | Exchanges only; 6J and MGC never named |
| Forced flat | 16:10 ET, a listed breach cause; auto-close may not run on half days. The harness's own-flat rule would give 15:55 (§4) | 16:59 ET auto-close; own-flat stays 16:00 |
| News | No news rule; terms §2.2.14 ban gapped or illiquid trading, including "before major market events" | EA page: "news trading" means immediate breach. News policy: allowed. Unresolved |
| Automation | EAs and bots allowed at both stages. §2.2.6 lets the firm request execution-system materials. §2.1.7: a different dashboard or trading IP needs prior approval | Enabled by default on NinjaTrader, Tradovate and TradingView. Off-platform logic unaddressed. GTC 5.4.1.2 bars an "external or slow data feed" |
| Hedging | Correlated-instrument hedging banned within and across accounts and firms (§1.2.21, §2.2.13); "Asset Group" undefined | Reverse trading across accounts banned; silent within one account |
| Standing | No `firm_rules` row; outside `AUTOMATION_FRIENDLY_PROP_FIRMS` | In the program firm set ([four-firm ADR addendum 2026-10-16 §3](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md)); row provisional on #867, held under SR-4 |

### Funded economics (published rules; arithmetic INF; no strategy data)

| | FundedNext Flex 150K | FXIFY Flex 150K |
|---|---|---|
| Evaluation fee | ≈ $260–$491 (official price pages conflict); reset ≈ $285 | $449 (+$157 bundle); reset $209; extensions unpriced |
| Payout cycle | 5 benchmark days of ≥ $250 and ≥ $500 cycle profit. Each withdrawal ≤ 50% of "accumulated profit" (undefined), capped at $4,000; 95% share of the request | Every 5 winning days of ≥ $250. ≤ 50% of "total trading returns" (undefined), capped at $3,000; $1,500 minimum; 40% consistency at payout; 90% split (100% with add-on) |
| Account life | **Concludes after the 5th reward.** Lifetime ceiling 5 × $4,000 × 95% ≈ **$19,000 net** ($20,000 if the cap applies after the share; UNV). Reaching it needs about $24,000–$40,000 of simulated profit (UNV: the low end applies if unwithdrawn profit counts). Live transition is discretionary, with conflicting criteria | No stated end. At the cap, $2,700–$3,000 net per cycle needs $6,000 of profit in the first cycle and $3,000–$6,000 of new profit in each later one (UNV). Live transition discretionary |
| Floor after the first payout | Set to $150,100 | Locks at the start balance |

**Data cost decides both.** CME non-display licensing for automated use is unresolved (ticket #04738415). The [feed-cost note](2026-10-11-feed-cost-sanity-check.md) §1 lists, per month: $0 if not required; $661 (A9, if eligible); $1,408 (A8, the safe reading; $1,453 from January 2027); and $1,864 (A1, if CME requires it).
- At $1,408, FundedNext's whole net ceiling covers about 13.5 months of data cost across evaluation and funded stages. At $1,864 it covers about 10 months, so a 12-month evaluation alone would exceed it.
- One FXIFY cap cycle covers about 1.4–2.1 months of data cost across those rows.
- At $0, both can be worth operating.

So the CME answer is an economics gate on any basis (§5 Step 3, gate E). Funded economics are an early input, not a final stage.

## 4. Candidate screen

| Candidate | Disposition and reason |
|---|---|
| **FLOOR-HALF** (trial 9) | **Screen object.** It is the only existing, explicitly versioned, ORB-off configuration with joint, integer, capacity-aware, intraday-honest evidence, and that evidence reads FALSIFIED on Tradeify. Its 1%/0.40 policy was selected after results were seen ([selection note](2026-09-10-tradeify-protection-selection.md)) and for a never-locking floor. Its Striker leg (`striker_dj30_mym_pyramid_250`) is admitted for the Tradeify Select 100K evaluation only, with funded deployment barred ([readmission ADR §2](../adr/2026-09-05-tradeify-select-striker-expression-readmission.md)). No leg has a FundedNext or FXIFY venue edition. These are deferred commitments (§5 Step 3), not screen inputs. |
| Rung R1 (Q-SFCLEAR-3) | Rejected. Paused and never scored. Its P0 policy runs only on the personal replay path, and its 15% gates are personal-lane quantities. FLOOR-HALF is R1 with adds on and the 1%/0.40 policy, so FLOOR-HALF reads expose nearly the same information. Disclosure to Q-SFCLEAR-3 is the default. |
| Full four-leg book | Rejected. FALSIFIED early-fail on four 100K tiers (minimum bust 25.28% against 5.0%). Robust NO-GO at T00 step 12. ORB is paused and dominates its round trips. |
| ORB MNQ v7 solo | Rejected. Stopped by Joshua. |
| c1 two-leg Striker book | Rejected for now. The scope of the bar on withdrawn editions needs a ruling. Its only 1.00× intraday-honest read busts 32.33%. No integer arm exists. |
| Striker NAS100 in place of ORB | Rejected. Not selected in the 09-10 exploratory study; Tradeify-evaluation-only admission; no public joint evidence. |
| Single legs and pairs | Rejected. Not portfolios. Aegis solo is FALSIFIED (H-SOLO). |
| MNQ redesign, Q-ORPREM-1, MSL/TNEC lanes, legacy CFD book | Rejected. Research, deferred, falsified, or not futures. |

**Compatibility at the comparison bases** (zero-run; open items are deferred to Step 3):

| Check | FundedNext Flex 150K | FXIFY Flex 150K |
|---|---|---|
| Concurrent positions | Allowed | Allowed |
| Correlated hedging | Short 6J against long MYM and MGC: unknown, pending a firm answer. The cross-firm ban also reaches the Tradeify weekly trade | Within one account: silent |
| News | No rule; §2.2.14 open | The EA ban is unresolved |
| Flatten | Own-flat = min(16:00, deadline − 15 min) ([`production_source.py:258-260`](../../ops/c1_rail/qualification/production_source.py)) gives 15:55. Running unchanged needs a margin ruling (Step 3) | 16:00, unchanged |
| Cap | ~40 micro-equivalents within 80 | ~40 micro-equivalents within 100 |
| Evidence | None at either tier | None at either tier |

**Rejected tiers** (target/rope; equivalent size against FLOOR-HALF on Tradeify; INF):
- FXIFY 100K (1.85; 0.92): close to the parked geometry.
- FXIFY 50K (1.71; cap 30): cap below the ~40 micro-equivalents half size needs.
- FundedNext 100K (2.0; 1.2) and 50K (1.67; 2.0; cap 30): thinner rope, and cap.
- FXIFY Direct 150K: instant-funded, not an evaluation.
- FundedNext Rapid, Legacy and Direct: rope ≤ $3,000 and caps ≤ 6/60. Legacy 100K is the parked Tradeify geometry; Direct is 50K only.

## 5. Proposed sequence

Each step needs its own approval, and approving one step approves nothing after it.

### Step 1: usefulness criterion, screening rule and exposure ruling

This is a Joshua ruling. It is recorded and hashed before Step 2, and nothing in it may change after the read. The proposed values below can be replaced by Joshua before the read.

**Maximum evaluation duration D.** This is simulated account time, not research time. D depends on an external fact, the CME answer, so no choice is made after the read:
- **D = 252 sessions** (about 12 months) if CME confirms no non-display fee, or one of $500 a month or less.
- **D = 126 sessions** (about 6 months) if CME confirms a higher fee. At A8's $1,408, twelve months of data cost would consume about 89% of FundedNext's net ceiling (§3).
- If CME has not answered when Step 2 runs, labels are produced for both values of D. The answer, when it arrives, picks the binding one.
- At FXIFY, any D beyond 30 days must be purchasable through extensions.

**Required probability.** P(pass within D) ≥ 50%. Busts and `UNDETERMINED` paths count as never passing under the pessimistic assignment. So this equals median sessions-to-pass ≤ D under #733's median rule (lower nearest rank, infinity included).

**Populations.** FULL, H1 and H2 must each meet it, under the pessimistic assignment. The optimistic assignment is reported.

**Costs:**
- The screen can only use the existing outputs' single Tradeify cost model. Its direction relative to FundedNext or FXIFY costs is unknown. FXIFY publishes no rate. FundedNext publishes none either: its article uses NQ at $2.88 per side all-in only as an example and refers to the platform's commission pages.
- For any later run the rule is fixed now: per symbol, the higher of the firm's published all-in rate and the existing Tradeify model, at c = 1.5, binding. Step 3 only confirms the figures.

**1,500 sessions:**
- #733's pass-floor and median limbs at 1,500 sessions are a secondary diagnostic, reported only.
- The approved 5.0% bust ceiling stays binding for any later run, measured to 1,500 sessions.

**Q-SFCLEAR-3 exposure.** Q-SFCLEAR-3 is frozen on Joshua's attestation that he has seen no trial-9 outputs, and FLOOR-HALF information nearly matches R1's (§4). So Step 1 names:
- the Step 2 reader: a designated local session that is not a Q-SFCLEAR-3 executor;
- the label's recipients.

The default is to record the read and its labels as a Q-SFCLEAR-3 exposure entry. That entry includes Joshua if he receives the labels.

**Screening rule** (applied in Step 2):
- **One label per basis.** FundedNext uses the target ratio 1.33 ($8,000 / $6,000); FXIFY uses 1.5 ($9,000 / $6,000). Both labels feed basis selection.
- **Per population,** under the pessimistic assignment, using the printed tallies and, if permitted, the Step 2b median m:

| Label | Condition |
|---|---|
| **NOT PROMISING** | (i) m is finite and ratio × m > 2 × D; or (ii) the time limb is the failure: pessimistic bust ≤ 5.0% but pass < 50% at 1,500 sessions (an infinite median) |
| **PROMISING** | m is finite and ratio × m ≤ D |
| **UNCLEAR** | Anything else: bust > 5.0% with pass < 50%; a finite m with D < ratio × m ≤ 2 × D; any summary not available |

- **Combining populations per basis:** any NOT PROMISING → NOT PROMISING; otherwise any UNCLEAR → UNCLEAR; otherwise PROMISING.
- **The ratio × m estimate is a rough heuristic, not proof.** It ignores the lock, the larger rope, consistency, protection and cost differences. The 2× band absorbs that known error.
- **A PROMISING label carries no evidential weight.** The data are in-sample and the configuration is selected. It only permits proposing Step 3.

### Step 2: bounded summary read

This needs Joshua's explicit permission, given after Step 1 is recorded. It approves nothing in Step 3.

**What T00 prints.** The #733 report and its `results.json` print only:
- the A6 label;
- per-assignment, per-population tallies (bust, pass, undetermined, denominator);
- descriptive counts ([`verdict.py:105-112`](../../ops/c1_rail/qualification/t00_screen/verdict.py)).

They print no median and no named failing clause. Hence two parts, each separately permitted:

| Part | What it does | What it can yield |
|---|---|---|
| **2a. Tallies only** | Read the printed label and tallies. The failing A6 limb follows from them: bust > 5% or pass < 50%, per population and assignment. No replay, rescoring or recomputation | NOT PROMISING (ii) or UNCLEAR only |
| **2b. One pre-declared derivation** (optional) | Evaluate #733's own median rule over the existing PATH journal's `sessions_to_pass`, per population and assignment, with the existing verdict code. This is the single recomputation that the "no new scoring" limit would have to allow explicitly. No replay, no strategy change, no other statistic | Also makes PROMISING and NOT PROMISING (i) reachable |

**How it runs:**
- **Must run locally:** in the primary checkout's private run directory, by the reader named in Step 1.
- **Logged as exposure:** reader, time and artifact hashes.
- **Disclosure:** values stay private. The public record carries only the per-basis labels.

**Parallel, no spend:**
- CME ticket #04738415 is already pending.
- The funded economics in §3 are done.

### Step 3: only after PROMISING, or UNCLEAR with Joshua's choice, on at least one basis

These run in this order. Each needs its own approval. They were drafted in revision 1 and stay deferred.

**1. Firm questions.** Agents draft them; Joshua sends them through the coordinator's eligibility register.
- **FundedNext:**
  - how 6J counts;
  - whether short 6J against MGC or MYM is a correlated hedge, and whether the Tradeify weekly trade counts under §1.2.21;
  - native NinjaScript at both stages;
  - "highest balance that day": EOD or intraday high (an intraday-high trail needs a core kernel packet);
  - the target's P&L basis;
  - 16:10 and half-day semantics;
  - the reach of §2.2.14 news;
  - the platform's per-symbol commission schedule;
  - the scope of §2.2.6 materials;
  - the "accumulated profit" definition, and whether the cap applies before or after the share.
- **FXIFY:**
  - repeatable extensions and their fee;
  - the EA news-ban reading (high-leverage only; holding through releases with resting stops);
  - 6J and MGC tradability and counting;
  - the add-on product;
  - readings of GTC 5.4.1.6 and 5.4.1.2;
  - the "total trading returns" definition.

**2. Basis selection.** FundedNext or FXIFY, on the per-basis labels, the firm answers and the funded economics. Reversing the provisional FXIFY-first order is Joshua's call.

**3. Gate E (economics), before items 4–7.** One of two conditions must hold:
- CME has answered in writing, and the funded-economics check is positive. The check is net withdrawal ceiling (or expected cycles × net per cycle) − evaluation fees × expected attempts − data cost over D plus funded life > 0, under stated assumptions.
- Or Joshua records that a PASS may have no funded value.

**4. Rulings:**
- **Own-flat at FundedNext.** Choose (i) or (ii):
  - (i) the 15:55 output as a new candidate, FLOOR-HALF-F, which has non-bar instants and more `UNDETERMINED` exposure;
  - (ii) keep 16:00 through a reviewed 10-minute margin change, with the prop-envelope E1 precedent.
- **Private-source posture** against FundedNext §2.2.6 and §2.1.7.
- **Striker p250 eligibility,** its funded bar, and venue editions for every leg (readmission ADR §4; venue-binding axis).
- **Trial 13** and its ledger.
- **Confirmed cost figures.**
- **CPU budget.**

**5. Firm registration.** A `firm_rules` row with `starting_balance`, `core/mc/preflight.py` and a firm-expansion ADR for FundedNext, or the FXIFY row from #867. The designated writer does this, sequenced against the SR-4 hold.

**6. Harness build** (INF: about 4–6 packets).
- A new r3e contract and purpose profile.
- Tier and consistency threaded from the contract (`runner.py:27` hard-codes Tradeify).
- Deadline, calendar and cost artifacts.
- Verdict support for D.
- Then a new harness H, a P7 rerun, and source and screen approvals.

It must run locally, unless Joshua extends the 2026-10-07 §60 T00 VM admission to an r3e screen.

**7. Stage 1, the frozen joint qualification.** T00 port replay on the selected basis, with the pessimistic assignment deciding, in FULL, H1 and H2.
- **Binding:** P(pass within D) ≥ 50%, and bust ≤ 5.0% measured to 1,500 sessions, at the Step 1 cost rule.
- **Reported only:** A6's pass-floor and median limbs at 1,500 sessions; c = 1; the no-lock stress; co-loss ratios; cells within 2 SE of a threshold, labelled fragile.
- **Outcome rules:**
  - A pessimistic-fail / optimistic-clear result is FAIL (`UNDETERMINED`-dependent).
  - INCONCLUSIVE is VOID or INSUFFICIENT only.
  - At most one VOID rerun.

**8. Stage 2, funded usefulness.** It runs only after a Stage 1 PASS and the Striker eligibility and funded-bar ruling (item 4). It estimates expected net withdrawals under the selected firm's funded rules, after fees and data cost. The criterion is set before any funded output exists.

## 6. What each result permits

| Result | What follows |
|---|---|
| **Screen: NOT PROMISING on both bases** | Stop investing in FLOOR-HALF. The recommended research-budget decision is no further venue shopping for it at target/rope ≈ 2 venues on these panels. This is Joshua's budget choice: one failure does not falsify every such venue. |
| **Screen: PROMISING or UNCLEAR on at least one basis** | Step 3 may be proposed, item by item, in its stated order. A PROMISING label carries no evidential weight. |
| **Stage 1 PASS** | Planning native parity and protection acceptance, not trading. It needs the Striker eligibility ruling first. Each of these is a separate admission: per-leg native specifications and grants, a Grant A host, the v2 parity contract, a protection pilot, venue editions, the instance's own M1, and S1 venue admission (an operator GO overriding S1 through a new ADR). |
| **Stage 1 FAIL** | Park FLOOR-HALF at the scored basis. Extending that to other venues is again a budget decision, not a falsification. |
| **INCONCLUSIVE** | Name the missing fact and its smallest remedy. |

**Successor stopping rule** ([T00 card §8](../briefs/handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md)). It binds any successor screen of this book and §7 item 1. If a screen confirms the pessimistic anchor on H2, no further size vector is proposed.

A bracket-run R1/R2 resolution needs Joshua to lift his 2026-10-10 hold. 1-minute data could recover at most 24 of 190 unlocated splits. It does not reopen #876. None of this is four-firm §4 evidence.

## 7. Improvement backlog

Untested and ranked. None is a prerequisite for §5 or a remedy for a failure. Each is a new candidate with its own pre-registration and trial. **No tested annSR-raising hypothesis exists.** These items at best reshape bust against time.

**1. Lock-conditioned early-phase size schedule** (sizing, firm fit).

| Field | Content |
|---|---|
| Weakness | On the declared book (r3c), busts are grind with no concentrated leg while the cushion is thin (T00 Tier-2 row 5). |
| Mechanism (model implication) | The constant-size bound assumes a never-locking rope. Where the floor locks partway to target, cutting size only before the lock may buy more bust reduction per session of pass time than a uniform cut. On Tradeify the two coincide (T00 desk model, "an assumption, not evidence"). |
| Smallest test | A frozen pre-lock vector (round-down, never above FLOOR-HALF), paired on identical keys against a uniform cut at matched pessimistic median, plus a no-lock control. Run only after the candidate's own verdict. |
| Falsifier | No bust reduction at matched median above a pre-set minimum exceeding MC SE; or the advantage persists with the lock disabled, which makes it plain downsizing. |
| Decision | If supported: a successor through dd_protection change-control. If falsified: no sizing lever remains. |
| Build needs | A state-dependent size vector; a second protection mechanism in `simulate_path`; a lock-day output. |
| Disclosed | Declined on 10-10 (C-1/C-6); readiness map Q4 deferred it. Integer rounding can collapse it (A2 §4; round-down floors small legs). Cushion sizing failed robustness for ORB solo (Q-ORBSURV-1). The stopping rule applies. |

**2. Joint-loss and cost assumptions** (overlapping losses, execution).

| Field | Content |
|---|---|
| Weakness | No co-loss measure exists for Aegis, Striker and Vanguard together; the recorded 1.24 ratio is ORB-MYM v0.4 against MNQ. Add-fill slippage is likely optimistic. |
| Mechanism | Coincident losing days deepen joint drawdown beyond per-leg risk; optimistic add fills understate cost. |
| Smallest test | Co-loss ratios and a c = 1 / 1.5 comparison reported inside Stage 1 (no extra arm or K). |
| Falsifier | Co-loss consistent with independence, and the verdict stable across costs. |
| Decision | Whether a leg-overlap or execution remedy merits its own candidate. |

**3. Vanguard flatten truncation** (exits; FXIFY only).

| Field | Content |
|---|---|
| Weakness | A 10-18/19 timing read, not yet logged, indicates Vanguard often holds past 16:00, which the 16:00 own-flat cuts. |
| Mechanism | The late hold may carry part of its edge or its tail. |
| Smallest test | Vanguard-only port replay at 16:00 against a 16:45 own-flat on the same panels: leg expectancy and share of joint H2 drawdown. |
| Falsifier | No difference above a pre-set floor. |
| Decision | Whether a 16:45 FXIFY expression (a new candidate) merits qualification. |

**4. Aegis regime exposure** (disclosure).

| Field | Content |
|---|---|
| Weakness | Exploratory, protection-off rows show Aegis-alone busts concentrated in 2020-02..2022-07 and H1. |
| Mechanism | The cushion may lean on Aegis's 2022-26 drift; a shuffled-Aegis control matched the real book. |
| Smallest test | Aegis alone on the sanctioned 2020-22 export under the candidate's rules. |
| Falsifier | 2020-22 bust ≤ FULL bust + 2 SE. |
| Decision | A regime limit on the candidate's label. |

**Not ranked: ORB/MNQ** (research only; ORB paused):
- H-C (excursion-triggered add) is the only unclosed ORB sizing lever and needs an EM3 ruling.
- H-A (Q-ORPREM-1) is deferred.
- H-B (stop-and-reverse) conflicts with long-only books and with the hedging rules.

## 8. Evidence reused, gaps, dependencies

**Reused, not rerun:**
- four-firm RESULTS;
- size feasibility;
- the T00 step-12 and FLOOR-HALF labels and the stopping rule;
- the A2 bound;
- the composition grid (exploratory);
- Q-SFCLEAR-3's design;
- #876;
- the ORB closures (Q-RANGECOND-1, Q-ORBCUSH-1, Q-ORBSURV-1, Q-SESSCONF-1, Q-COMPOSE-1);
- the readmission ADR;
- the FXIFY sheets (#867, #869);
- FundedNext's and FXIFY's published rules.

**Pending dependencies** (recorded, not duplicated):
- The ORB underperformance diagnosis (local_da95ffcf, wf_47ae3056-307): unreviewed and uncommitted. H-B and H-C are in a scratchpad only, a custody risk.
- The packet r4 check, then the coordinator's firm note (EMERY-RESEARCH-DOCS-1).
- The #867/#869 FXIFY row (SR-4 hold).
- CME ticket #04738415.
- The parity v2 contract.

**Record gaps** (corrections belong to their owners):
- the S4 terminal stop is not in a committed owner;
- the Q-ORPREM-1 deferral is not on its pre-registration;
- #876's "#873 open" is stale (#873 closed 2 s after the merge);
- the T00 manifest's trial-9 closure is owed;
- the 10-18/19 timing reads are not logged;
- the 10-16 LucidPro alternative is recorded only uncommitted.

**Exposure:** every reader above, plus the Step 2 reader, goes into any later pre-registration.

## 9. Decisions for Joshua

1. **Step 1:** ratify the usefulness criterion, the screening rule and the exposure ruling, with the proposed values or your own:
   - D = 252 or 126 sessions, set by the CME answer;
   - P ≥ 50%;
   - FULL, H1 and H2, under the pessimistic assignment;
   - one label per basis;
   - the 2× band;
   - the cost rule;
   - the reader and recipients.
2. **Step 2:** grant the bounded summary read, as part 2a only or 2a plus the 2b derivation. Each part is a separate permission and approves nothing in Step 3.
3. **After the labels:** whether to fund the Step 3 items, in order.
4. **This note** is open for review as #877; merging is yours.

## Addendum 2026-10-19: Step 1 ratified, Step 2 granted (record made before any read)

**Ruling.** Joshua, 2026-10-19, directly in this session, verbatim: "I ratify Step 1 as proposed and grant the Step 2 read, parts 2a and 2b. Run it locally under the stated limits."

**Frozen by this record.** These are §5 Step 1 as written above, unchanged:

| Parameter | Value |
|---|---|
| D | 252 sessions if CME confirms no non-display fee or one ≤ $500 a month; 126 sessions otherwise |
| CME status | As of 22:46Z, ticket #04738415 is unanswered, so labels are produced for both D. The answer selects the binding one |
| Pass criterion | P(pass within D) ≥ 50%, so the median is ≤ D |
| Populations | FULL, H1 and H2, under the pessimistic assignment; the optimistic assignment is reported |
| Target ratios | 1.33 for FundedNext and 1.5 for FXIFY; one label per basis |
| Label rule | The 2× band, the per-population label table, and the combination order (any NOT PROMISING, then any UNCLEAR, then PROMISING) |
| Cost basis | The existing outputs' single cost model |
| Part 2a | The printed label and tallies |
| Part 2b | #733's median rule (`MEDIAN_RULE = LOWER_NEAREST_RANK_INF_INCLUDED`), evaluated on the existing PATH journal with the existing verdict code: `ops/c1_rail/qualification/t00_screen/verdict.py`, sha256 `c2af4f70…d7d3`, unchanged since the run's H′ `eed60a1`. No replay, no rescoring, no strategy change, and no other statistic |

**Artifacts.** The FLOOR-HALF successor screen as recorded in the T00 card §8:
- `results.json` `f781c716…f495`;
- `REPORT.md` `42c008d1…6b6b`;
- authority `75f03043…9428`.

**Reader and recipients:**
- **Reader:** this Claude session (local_c36ee23a, "Portfolio qualification experiment selection", worktree `portfolio-qualification-experiment-d883a3`). It is not a Q-SFCLEAR-3 executor.
- **Joshua** receives the per-basis labels and each population's limb class. He does not receive tallies or medians.
- **The public record** carries the labels only.
- **Values** stay in a private file in the primary checkout.

**Exposure.** The read and its labels are a Q-SFCLEAR-3 exposure entry. That entry names this session and Joshua, as the labels' recipient.

## Addendum 2026-10-19: Step 2 result (labels only)

**Run.** Parts 2a and 2b, under the record above.
- **Reader and place:** this session, locally in the primary checkout. It used the project launcher (ops environment, Python 3.13.2), with no bytecode written.
- **Time:** read at 22:59:59Z.
- **What was read:** the run directory's printed outputs and journals.
- **What was not done:** nothing was replayed, and nothing was written into the run directory.

**Integrity checks.** All nine passed:
- the pinned `verdict.py`;
- the artifact hashes;
- the #733 values-block hash;
- segment-journal heads against `attestation.json`;
- every plan key present;
- the recorded verdict reproduced;
- `results.json` reproduced byte for byte;
- median inputs equal to the recorded tallies.

The reproduction re-evaluates the existing outcomes with `verdict.evaluate`. It yields no new statistic: it only proves that the median was derived from the same outcomes the verdict used.

**Labels** (the ratified rule; pessimistic assignment; FULL, H1 and H2):

| Basis | D = 252 sessions | D = 126 sessions |
|---|---|---|
| FundedNext Flex 150K | **UNCLEAR** | **NOT PROMISING** |
| FXIFY Flex 150K | **UNCLEAR** | **NOT PROMISING** |

Rounding the FundedNext ratio to 1.33 instead of 8,000/6,000 changes no label.

**Which label binds.** It is set by CME ticket #04738415, still unanswered:
- a confirmed fee ≤ $500 a month, or none, selects D = 252, giving **UNCLEAR** on both bases. Joshua decides whether any Step 3 item is worth funding.
- a higher fee selects D = 126, giving **NOT PROMISING** on both bases. That is a research-budget recommendation to stop investing in FLOOR-HALF, not a falsification.

Neither label carries evidential weight. The data are in-sample and the configuration is selected.

**Exposure entry** (owed to the T00 lineage manifest and to Q-SFCLEAR-3's exposure log; to be written there by their owners):
- **Readers:** session local_c36ee23a, and Joshua as the labels' recipient.
- **Time:** 2026-10-19T22:59:59Z.
- **Artifacts:**
  - `results.json` `f781c716…f495`, `REPORT.md` `42c008d1…6b6b` and `attestation.json` `96af7491…eae`;
  - the s-journals, pinned by the attestation heads.
- **Private record:** `local_artifacts/flex-qualification-2026-10/step2-read-20261019.private.json` (`8a77bdc4…d379`). The read script beside it is `d64efd11…abd`.
