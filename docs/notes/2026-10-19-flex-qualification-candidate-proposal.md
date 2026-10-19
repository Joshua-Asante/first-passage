# One qualification experiment: candidate and fresh-evaluation basis (proposal, 2026-10-19)

**Status:** PROPOSAL. It is not execution approval. Nothing is run, scored, frozen, bought, sent or admitted, and every decision in §9 is Joshua's.

**Question:** which existing portfolio, on which exact fresh-evaluation basis, deserves one qualification experiment before native implementation?

**Decision it informs:**
- whether to fund the Stage 0 checks (§5);
- only if those clear, whether to build Stage 1.

A Stage 1 PASS opens native parity and protection planning only (§6), and only once G0-1(g) is granted.

**Sources:**
- committed records at `origin/main` `772c0b6`;
- the open PR branches #867, #869 and #875;
- relay records in the primary checkout;
- the public FXIFY Futures and FundedNext Futures pages, read 2026-10-19.

No Pine, port, effective-input file, `local_artifacts/`, private report, trade CSV or panel was opened. Two disclosures:
- the research workflows read outcome labels and aggregates from the records in §8;
- they also took in private ORB figures that were relayed through an unreviewed diagnosis transcript.

**Labels:** **DOC** = a record or an official firm page; **INF** = inference; **UNV** = unverified.

## 1. Answer

**The current evidence supports neither a qualification claim nor an improvement claim.** No configuration has any result at a FundedNext or FXIFY tier, and every improvement hypothesis is untested. What the evidence does support is naming one object for a cheap futility check. One bounded run per signed cost authority follows only if that check clears.

**Candidate: FLOOR-HALF.** Its identity is frozen for T00 trial 9 ([#733](../briefs/pre-registration/2026-10-08-tradeify-book-successor-screen-prereg-DRAFT.md) §1a and §2 A1):
- the declared book at k = 0.5 under the code's round-down rule: Aegis 6J1 selling 6J, Striker DJ30 MYM p250 buying MYM, Vanguard MGC v0.4 buying MGC, adds as frozen, ORB floored to zero;
- size vector `139919cd…c271` and r3d contract `c7a82915…`;
- book protection: 1% combined-peak trigger, 0.40 scale, prior-close timing.

It is **FALSIFIED on Tradeify** (§2). It is chosen as the least-falsified existing object, not as a supported candidate.

**Primary basis (recommended; Joshua's decision, §9):** a fresh, pristine FundedNext Futures Flex 150K evaluation.
- This reverses the brief's provisional FXIFY-first order. That order was conditional on portfolio fit, and FXIFY's 30-day evaluation clock is an unpriced horizon cost against a lineage whose recorded pass times run to hundreds of sessions.
- The cost of choosing FundedNext: its 16:10 forced flat makes the harness compute a 15:55 own-flat, so the existing expression runs unchanged only through the G0-1(a)(ii) margin ruling. Its §2.2.14 news scope is also open. FXIFY would run the expression unchanged at 16:00.
- FXIFY Futures Flex 150K is the pre-declared alternative. It replaces FundedNext only through G0-3, before freeze.

**Highest-value improvement hypothesis:** a lock-conditioned early-phase size schedule (§7 item 1). It is a separate successor and never part of this candidate.

## 2. What is new since #876, and what is not

**What #876 records.** On 2026-10-19, Joshua ruled: "Record that no book-lineage configuration has an evidence case for the Tradeify eval" ([#876 addendum](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-19--no-book-lineage-configuration-has-an-evidence-case-for-the-tradeify-evaluation)). The ruling's scope includes FLOOR-HALF:
- under #733 §4 H it reads FALSIFIED, with "the configuration is not adopted";
- its NO-GO is `UNDETERMINED`-dependent: it fails under the pessimistic intrabar assignment, clears under the optimistic one, and its H2 bust is within 5%;
- its 10-11/12 risk acceptance into F1 lapsed on 2026-10-16.

This proposal does not recreate the declined rung-R1 Tradeify study and does not revive #873. **There is no new strategy evidence. The only ground for a new trial is the changed account basis.**

**Changed constraints.** The firm rules are DOC; the consequences are INF.
1. **Rope at fixed quantities.** FundedNext 150K's maximum loss limit (MLL) is $4,000, against $3,000 on Tradeify Select 100K. FLOOR-HALF's frozen integer quantities therefore sit at roughly 0.75× its Tradeify drawdown geometry, using the [venue note §6](2026-10-14-funded-venue-alternatives-assessment.md) rescaling method. This is directional only: rescaled exports do not reproduce rail quantities.
2. **Lock.** FundedNext locks the floor at start + $100 during the evaluation, reached at an end-of-day (EOD) balance of $154,100, about 51% of the target. Tradeify's evaluation never locks. Beyond plain rescaling, the lock is the only favourable change.
3. **Other changes that can move results:**
   - FundedNext's 40% consistency rule raises the target instead of failing the account.
   - The 1%-of-peak protection trigger ($1,500 at 150K) sits at 37.5% of the rope, against 33.3% at Tradeify.
   - The own-flat time and the costs differ.
   - At FXIFY there are adverse changes: a soft daily loss limit (DLL) lockout and the 30-day clock.
4. **Fresh, pristine start.** This fits the T00 harness's pristine-only rule ([`contract.py:843-849`](../../ops/c1_rail/qualification/contract.py)) and removes R-2's used-account dependence.

**Not new.**
- **The panels.** They are the same 2022-09-01..2026-09-02 panels, all fully exposed. This would be trial 13 after the T00 lineage's K = 12, so a PASS would be post-exposure, model-fitted feasibility, not validation.
- **Target/rope.** It is 2.0 on both 150K tiers, as on Tradeify. Under the recorded constant-size bound `T_min(yr) = (target/rope)·(ln(1/b)/2)/annSR²` ([A2 §2–§3](../../lab/analysis/c1/a2_panel_noise_venue_bound_2026-08-24/RESULTS.md)), a bigger rope at fixed target/rope buys lower bust only by lengthening the time to target.
  - At b = 5%, a six-month pass needs annSR ≈ 2.45 (A2 banner). INF from the same formula: a 1-year pass needs ≈ 1.73 and a 30-day pass ≈ 6.0.
  - At the pinned harness horizon of 1,500 sessions (≈ 5.95 years), the requirement falls to ≈ 0.71 (INF).
  - The highest annSR in A2's scoped corpus is +1.28. The estate also records a gross, CFD-era legacy Aegis Sharpe of 1.83 ([Q-GATECART-1](../briefs/closures/Q-GATECART-1-survivor-gate-cartography.md); an upper bound). No book-lineage Sharpe is published.
  - So the bound alone predicts FAIL only for a short business horizon. FLOOR-HALF nonetheless failed A6 at 1,500 sessions on Tradeify's equal target/rope, so a 1,500-session FAIL remains a live outcome. The bound also ignores the lock and the protection trigger, so it errs toward parking.
  - Context, exploratory and protection-off ([composition grid](../../lab/analysis/c1/tradeify_book_composition_2026-09/RESULTS.md)): Aegis-alone rows on Select bust far more in H1 than in H2, and their medians run to hundreds of days. **Both bust and time may bind.** FLOOR-HALF's own failing A6 clause is named only in the private #733 report.

**Target-shopping disclosure.** Moving a parked configuration to a firm with a larger rope is the pattern [rejected_candidates](../rejected_candidates.md) (ORB re-proposal bar, ~:1585) declined as target-shopping after seeing data. This proposal can be defended only on three grounds:
- it is an operator-directed basis comparison;
- the firm offers a new mechanism, the lock;
- it takes the shape that bar requires: a fresh GO, a pre-registration, and scoring at the firm's geometry before any unparking.

Its FAIL rule parks the candidate across every target/rope ≈ 2 venue (§6).

## 3. Account basis: structural comparison

This section is a **derived input** to the coordinator's dated FXIFY-vs-FundedNext note (EMERY-RESEARCH-DOCS-1), which owns firm facts. It is not authoritative and is not a firm rule sheet. FXIFY sheet corrections go to the #867/#869 writers. All facts were read 2026-10-19.

| Fact | FundedNext Flex 150K | FXIFY Flex 150K |
|---|---|---|
| MLL | $4,000 EOD trailing, updated 17:00 CT, from the "highest balance that day" (wording ambiguous). An intraday floating touch breaches instantly. Locks at $150,100 | $4,500 EOD trailing. The breach clock is unstated ("balance"). The lock at the start balance names no stage (sheet B1). The add-on gives $4,750 |
| Target / time limit | $8,000; closed-P&L basis UNV / none | $9,000 / 30 days. The reset FAQ treats an ended evaluation as failed; the time-limit FAQ is silent. Paid extension available, fee and repeatability unpublished |
| Consistency (evaluation) | 40% of target; exceeding it raises the target | 50%, soft |
| Daily loss limit | None | $3,000 soft (read-only for the rest of the day). An add-on removes it |
| Contract cap | 8 minis / 80 micros at 1:10. Full-size 6J counting unstated | 10 / 100 at 1:10. Full-size 6J counting unstated |
| Instruments | 6J (full only), MGC, MYM and MNQ listed | Exchanges only; 6J and MGC never named |
| Forced flat | 16:10 ET; failing to close is a listed breach cause. Auto-close may not run on half days | 16:59 ET auto-close |
| News | No news rule. Terms §2.2.14 ban gapped or illiquid trading, including "before major market events" | EA page: "news trading" means immediate breach. News policy: news trading allowed. Unresolved |
| Automation | Expert advisers (EAs) and bots allowed at both stages. §2.2.6: the firm may request execution-system materials. §2.1.7: a different dashboard or trading IP needs prior approval | Enabled by default on NinjaTrader, Tradovate and TradingView. Off-platform logic unaddressed. GTC 5.4.1.2 bars an "external or slow data feed" |
| Hedging | Correlated-instrument hedging banned within and across accounts and across firms (§1.2.21, §2.2.13). "Asset Group" undefined | Reverse trading across accounts banned. Silent within one account |
| Funded stage | No consistency rule, no DLL, 95% split. Each withdrawal ≤ 50% of profit and ≤ $4,000 per cycle. **The account concludes after the 5th reward** | Recurring payouts every 5 winning days of ≥ $250. ≤ 50% of profit, ≤ $3,000 per cycle, $1,500 minimum, 40% consistency at payout, soft DLL, 90/10 split. Floor locks after a payout |
| Standing | No `firm_rules` row; outside `AUTOMATION_FRIENDLY_PROP_FIRMS`; needs an expansion ADR | In the program firm set ([four-firm ADR addendum 2026-10-16 §3](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md)). Row provisional on #867, held under SR-4 |

**Why FundedNext is primary (INF).** On documented rules it is the only basis with no evaluation time limit (article 17229829). The costs against it:
- its §2.2.14 news scope is open (G0-2);
- the 16:10 flat gives a 15:55 own-flat, so the existing expression runs unchanged only through G0-1(a)(ii).

FXIFY runs the expression unchanged at 16:00. So the choice (§9 item 1) weighs FundedNext's margin ruling against FXIFY's 30-day clock.

**What FXIFY keeps:**
- the wider rope and the 16:59 close, which leave the harness's 16:00 own-flat unchanged;
- program-set standing, so a future result could count toward four-firm §4;
- a funded stage that INF looks more durable, depending on how many payout cycles occur.

Its 30-day clock is a horizon cost of unknown size until G0-3(i) is answered.

**Tiers screened** (target/rope; at fixed quantities, equivalent size relative to FLOOR-HALF-on-Tradeify; INF):

| Tier | Target / rope | Equivalent size | Cap | Disposition |
|---|---|---|---|---|
| FundedNext Flex 150K | 2.0 | 0.75 | 80 | **Primary** |
| FXIFY Flex 150K | 2.0 (1.89 with the +$250 add-on) | 0.67 (0.63) | 100 | **Alternative (G0-3)** |
| FXIFY Flex 100K | 1.85 | 0.92 | 60 | Rejected: close to the parked Tradeify geometry |
| FXIFY Flex 50K | 1.71 | 1.71 | 30 | Rejected: cap below the ~40 micro-equivalents half size needs (venue note §2) |
| FundedNext Flex 100K | 2.0 | 1.2 | 50 | Rejected: thinner than Tradeify at the same quantities |
| FundedNext Flex 50K | 1.67 | 2.0 | 30 | Rejected: cap |
| FXIFY Direct 150K | n/a | n/a | n/a | Rejected: instant-funded, not an evaluation (outside the brief); $2,500 DLL; 25% consistency |
| FundedNext Rapid Pro/Daily, Legacy, Direct | n/a | n/a | n/a | Rejected: rope ≤ $3,000 and caps ≤ 6/60. Legacy 100K ($3,000 rope, $6,000 target, 5/50) is the parked Tradeify geometry; Rapid Pro ≤ $2,500; Direct is 50K only |

## 4. Candidate screen

| Candidate | Disposition and reason |
|---|---|
| **FLOOR-HALF** (trial 9) | **Selected for the futility check.** It is the only existing, explicitly versioned, ORB-off configuration with joint, integer, capacity-aware, intraday-honest evidence. That evidence reads FALSIFIED on Tradeify (§2). Its 1%/0.40 policy is the one the prop replay accepts. That policy was selected after its results were seen ([selection note](2026-09-10-tradeify-protection-selection.md)) and for a never-locking floor. Here it is reused unchanged and unvalidated at a locking tier; a locking reference mode would be a new candidate. **Eligibility gap:** its Striker leg is the campaign expression `striker_dj30_mym_pyramid_250`, admitted "for the Tradeify Select 100K evaluation only", with funded deployment barred ([readmission ADR §2](../adr/2026-09-05-tradeify-select-striker-expression-readmission.md)). No leg has a FundedNext or FXIFY venue edition (G0-1 g). |
| Rung R1 (Q-SFCLEAR-3) | Rejected. Its work is paused. It has never been scored. Its P0 policy runs only on the personal replay path, not the T00 prop path. Its 15% halt and G1/G3 gates are personal-lane quantities. Q-SFCLEAR-3's frozen design informs §5 (calendar denials, the data-exclusion zero day, cost stress). **Exposure note:** FLOOR-HALF is R1 with adds on and the 1%/0.40 policy, so a FLOOR-HALF run on these panels exposes nearly the same information as R1. Disclosure to Q-SFCLEAR-3 is the default (G0-1 d). |
| Full four-leg book | Rejected. FALSIFIED early-fail on four 100K tiers (minimum bust 25.28% against 5.0%). Robust NO-GO at T00 step 12. ORB is paused and dominates its round trips. It holds past 16:10 on 403 of 1,020 weekdays. |
| ORB MNQ v7 solo | Rejected. Stopped by Joshua. |
| c1 two-leg Striker book | Rejected for now. AGENTS.md bars withdrawn Striker editions without a venue qualifier, while the owner ADRs are venue-scoped, so a ruling is needed. Its only 1.00× intraday-honest read busts 32.33%. No integer arm exists. |
| Striker NAS100 in place of ORB | Rejected. Not selected in the 09-10 exploratory study. Tradeify-evaluation-only admission. No public joint evidence. |
| Single legs and pairs | Rejected. Not portfolios. Aegis solo is FALSIFIED (H-SOLO). No public pair evidence. |
| MNQ redesign, Q-ORPREM-1, MSL/TNEC lanes, legacy CFD book | Rejected. Research, deferred, falsified, or not futures. |

**Compatibility screen for FLOOR-HALF at FundedNext 150K:**

| Check | Status |
|---|---|
| Concurrent positions | Allowed |
| Correlated hedging | **Unknown pending G0-2.** Short 6J is held against long MYM and long MGC; 6J against MGC is the pair to ask about. The cross-firm ban also reaches the Tradeify weekly preservation trade |
| News | No rule; §2.2.14 is open |
| Flatten | The harness computes own-flat = min(16:00, venue deadline − 15 min) ([`production_source.py:258-260`](../../ops/c1_rail/qualification/production_source.py)). That is 16:00 at Tradeify and **15:55 at FundedNext**, so the existing expression cannot run unchanged (G0-1 a) |
| Contract cap | About 40 micro-equivalents against 80 (6J counting is G0-2) |
| Evidence | None at this tier |

## 5. Proposed experiment: Q-FLEXQ-1

### Stage 0 — zero-run gates

**Order:** G0-1 → G0-2 / G0-3 (basis fixed) → freeze record (hashed) → G0-4 → G0-5 → Stage 1 build. G0-4 may only apply a rule recorded in G0-1. A gate that fails parks the proposal. The exception is G0-1(g): a declined (g) leaves Stage 1 research-only and does not park it.

**G0-1, rulings (Joshua):**
- **(a) Own-flat at 16:10.** Choose one; neither is the status quo.
  - (i) FLOOR-HALF-F: accept the 15:55 output as a new candidate. Its cutoff (15:40), flatten (15:50) and deadline (15:55) are all non-bar instants.
    - The T00 bracket places them as R1/R2 splits, so more paths become eligible for `UNDETERMINED`, and the deciding pessimistic assignment can only get worse.
    - Whether the bracket supports a non-bar cutoff and deadline is unverified (build scope).
  - (ii) Keep 16:00 through a reviewed change to the 15-minute margin.
    - This keeps today's T00 schedule, including its intrabar 15:55 flatten, with a 10-minute buffer to 16:10.
    - It is a production schedule-law change and a new harness source revision.
    - Precedent: the prop envelope's E1 ratified a 16:00 build with a 10-minute buffer to a 16:10 deadline ([envelope §1](../../ops/prop_envelope_default.md)).
- **(b) Private-source posture.** Is FundedNext §2.2.6 compatible with it? Is the intended host compatible with §2.1.7? If not, FundedNext is out.
- **(c) Acceptance.**
  - Reuse #733's A6 whole at 1,500 sessions (the approved criterion for this configuration).
  - Optionally add a business horizon H in sessions, with its basis, for a P(pass ≤ H) cell computed from the PATH journal's `sessions_to_pass`. State whether that cell is binding.
  - If H is binding, also record the lock allowance G0-4 applies: a stated multiplier on the target-scaled median.
- **(d) Q-SFCLEAR-3.** Disclose to its executors by default. A sequencing ruling must come before any Stage 1 output and does not lift its pause.
- **(e) Trial 13.** Authorize it, either on the open T00 ledger (scope amendment) or on a successor ledger that carries K = 12. Authorize a new screen purpose.
- **(f) Costs.** A per-symbol assumption; FundedNext publishes only NQ, at $2.88 per side all-in. Also whether ×1.5 is a binding second authority or reported.
- **(g) Eligibility.** A successor decision under the readmission ADR §4 extending, or declining, `striker_dj30_mym_pyramid_250` to this evaluation, and ruling on its funded bar. Plus a venue-edition election for every leg (venue-binding axis). **Until granted, Stage 1 is research-only: it cannot open §6 planning, and Stage 2 is not run.**
- **(h) Budget.** CPU seconds in the signed parameters block.

**G0-2, FundedNext written answers.** Drafted by agents, sent by Joshua, routed through the coordinator's eligibility register:
- How full-size 6J counts against 8/80.
- Whether short 6J against long MGC or long MYM falls under §2.2.13 (correlated hedging), and whether the Tradeify weekly trade counts under §1.2.21.
- Whether native NinjaScript on NT8 with FundedNext credentials is allowed at both stages.
- **Hard gate:** whether "highest balance that day" means the EOD balance or the intraday high. An intraday-high trail is not expressible on the current kernel: it needs a scoped core packet with its own re-MC and ADR, or the pairing parks.
- Whether the target is measured on closed or open P&L.
- The 16:10 breach semantics and the half-day calendar.
- Whether §2.2.14 covers holds or entries around scheduled releases.
- Per-symbol commissions.
- Whether §2.2.6 materials include source code.

**G0-3, FXIFY switch test (pre-declared).** FXIFY 150K replaces FundedNext as primary only if all of the following hold in writing before freeze:
- (i) repeatable extensions at a stated fee, so that 1,500 sessions or H can be bought, and the expiry outcome;
- (ii) the EA news ban means high-leverage news trading only, and automated strategies may hold through releases with resting stops;
- (iii) full 6J (short) and MGC are tradable, and how they count;
- (iv) the add-on product is fixed;
- (v) a reading of GTC 5.4.1.6 for entries ≤ 2 h before the Friday close and around releases;
- (vi) a reading of GTC 5.4.1.2 for the intended runtime feed.

An FXIFY rules row must then encode the clock and extension assumption, the soft DLL or its add-on, 50% soft consistency, and the 16:59 close.

**G0-4, futility read.** Must run locally: it reads the private T00 run directory. It needs Joshua's OK and is logged as exposure. It reuses the deferred FLOOR-HALF pass-time check ("E1 kill check", [checklist](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) 10-13 addendum; its parent branch was withdrawn 10-16).
- **Read** (labels plus pre-declared statistics; no new replay):
  - which A6 clause failed, and in which population;
  - FLOOR-HALF's Tradeify median sessions-to-pass under each assignment.
- **Park if:**
  - the failing clause is the pass-floor or median limb in a population whose bust cleared, because fixed quantities and a larger target lengthen time (INF); or
  - H is binding, and the chosen basis's target ratio (1.33 for FundedNext, 1.5 for FXIFY) × the pessimistic median exceeds H after the lock allowance recorded in G0-1(c).

A bust-driven failure, including an infinite median caused by busts, is not parked here: the wider rope may cure it, and that is the question Stage 1 answers. This is a one-sided, no-lock approximation that errs toward parking. **A G0-4 clear carries no evidential weight**: the data are in-sample and the configuration is selected.

**G0-5, data-cost gate.** Before any Stage 1 build, either CME ticket #04738415 is answered in writing, or Joshua records a ruling to build Stage 1 knowing a PASS may have no funded value (Stage 2).

### Stage 1 — frozen joint qualification

Built only if Stage 0 clears. **Must run locally:** port replay reads the private runtime ports. The exception is a ruling by Joshua that the 2026-10-07 §60 T00-screen VM admission, which names r3c's bound artifacts, extends to an r3e screen. The local host previously lost the FLOOR-HALF run to a full disk and a power loss (T00 card §8).

| Freeze item | Value |
|---|---|
| Identity | A new FundedNext contract (r3e) derived from r3d by a named rule. r3d binds Tradeify deadline facts and a $100,000 initial state, so it is not reused. r3e changes more than `contract_id` and the startup row, so it fails `_derived_from_r3c` and needs a new purpose profile (build scope). Size vector `139919cd…`, startup policy v2 `53dea292…`, `BOOK_SOURCES.sha256` pins with the corrected Striker port. Own-flat per G0-1(a). Protection 1%/0.40, as disclosed in §4. No other change; any change is a new candidate. |
| Firm rules | A `FundedNext_Flex_150K` row with `starting_balance`, a passing `core/mc/preflight.py` check, and a firm-expansion ADR. Written by the designated `firm_rules` writer and sequenced against the SR-4 hold. The kernel consumes the row; no rule values live in harness code. Encoded: $4,000 EOD-trailing MLL, intraday touch = bust, lock at $150,100, $8,000 target, 40% target-recalculating consistency, no DLL, 8/80 cap with excess profit deducted, 16:10 deadline facts, no time limit, inactivity barrier OFF (convention; 30-day rule noted). |
| Data and exposure | CME M15 TradingView panels 2022-09-01..2026-09-02; FULL/H1/H2 and path construction as #733 §3 item 4, on fresh RNG roots, with N and SE stated. Label: "post-exposure, model-fitted". Reader log: this session's workflows, the T00 readers and the G0-4 reader. |
| Costs | G0-1(f), one level per signed authority. Add-fill slippage is disclosed as likely optimistic. |
| Intrabar and missing data | The ratified bracket runs R1/R2. **The pessimistic assignment decides.** §4-A data-exclusion zero days as in Q-SFCLEAR-3. Shortened and holiday sessions are denied. |
| Harness | T00 port replay, the only route that brackets R1/R2 over BookReplay paths. E1 does not, and it counts censored paths as failures. |
| PASS | The complement of #733's §4 falsifier on the FundedNext row, under the pessimistic assignment, in each of FULL, H1 and H2, at every binding cost level: bust ≤ 5.0% to 1,500 sessions, and P(pass ≤ 1,500) ≥ 50% with a finite median. Plus the H cell if G0-1(c) made it binding. |
| FAIL | Any binding cell fails. A pessimistic-fail / optimistic-clear result is FAIL, labelled `UNDETERMINED`-dependent, unless Joshua lifted the 2026-10-10 bracket hold before G0 approval. |
| INCONCLUSIVE | VOID (pin mismatch or harness fault) or A6 INSUFFICIENT only. |
| Reported, not binding | No-lock stress (S1); cost ×1.5 if not binding; sessions-to-pass; co-loss ratios among the three legs; cells within 2 SE of a threshold labelled fragile. |
| Budget and stopping | One run per signed authority, and at most one VOID rerun of the same design across the study. Stop at the CPU bound and return to Joshua. $0 spend. |
| Build scope (INF) | About 4–6 packets: the firm row and preflight; tier and consistency threaded from the contract into the replay evaluation (`runner.py:27` hard-codes Tradeify); the r3e derivation rule and purpose profile; deadline, calendar and cost artifacts; and any verdict changes for H. Then a new harness H, a P7 rerun, and source and screen approvals. |

### Stage 2 — funded usefulness

Run later, and only after a Stage 1 PASS with G0-1(g) granted.
- **Model:** the funded account's own rules. That means the 5-reward end, the 50%-of-profit and $4,000-per-cycle caps, the benchmark days, and the floor reset after the first withdrawal.
- **Criterion:** expected net withdrawals, after fees and the CME data cost, set before any funded output is seen. Lifetime gross withdrawals are capped at 5 × $4,000 (INF), against a possible non-display feed of up to ~$16.9K a year (venue note §9). So **a Stage 1 PASS implies no usefulness until CME ticket #04738415 is answered.**
- **Method:** Q-FUNDPOL-1's retained method may serve, with its own fresh derivation ([b5](../pursuits/b5-q-fundpol-1.md)).

## 6. What each result permits

**PASS:** planning native parity and protection acceptance, not trading. It requires G0-1(g) granted. Each item below is a separate admission:
- per-leg native specifications and grants;
- a host that passes the Grant A canary;
- the v2 parity contract;
- a protection pilot;
- FundedNext venue editions;
- the instance's own M1;
- **S1 venue admission**: an operator GO overriding S1's no-migration ruling through a new ADR.

Nothing here selects a successor venue: Stage 1 is research under S1.

**FAIL, or a G0-4 park:** park FLOOR-HALF on every target/rope ≈ 2 venue on these panels, FXIFY included.
- No size, rope or tier search follows.
- Another venue needs new strategy evidence, or a rule difference recorded before any output that changes the bound's assumptions.

**INCONCLUSIVE:** name the missing fact and its smallest remedy.

**Successor stopping rule** ([T00 card §8](../briefs/handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md)). It binds this screen and §7 item 1. If the screen confirms the pessimistic anchor on H2 (`UNDETERMINED` resolved as bust), successor work on this book stops and no further size vector is proposed.

A bracket-run R1/R2 resolution:
- needs Joshua to lift his 2026-10-10 hold;
- 1-minute data could recover at most 24 of 190 unlocated splits, and no 1-minute exports exist;
- does not reopen the Tradeify qualification (#876).

This study is not four-firm §4 evidence.

## 7. Improvement backlog

Untested and ranked. None is a prerequisite for §5 or a remedy for a Stage 1 FAIL. Each is a new candidate with its own pre-registration and trial. **No tested annSR-raising hypothesis exists in the inspected evidence.** The items below at best reshape bust against time.

**1. Lock-conditioned early-phase size schedule** (sizing, firm fit).
- **Weakness:** on the declared book (r3c), busts are grind with no concentrated leg while the cushion is thin (T00 Tier-2 row 5).
- **Mechanism (model implication):**
  - the constant-size bound assumes a never-locking rope;
  - where the floor locks partway to target, cutting size only before the lock may buy more bust reduction per session of pass time than a uniform cut;
  - on Tradeify the two coincide (T00 desk model, "an assumption, not evidence").
- **Smallest test:** a frozen pre-lock vector (round-down, never above FLOOR-HALF), paired on identical keys against a uniform cut at matched pessimistic median sessions-to-pass, plus a no-lock (S1) control. Run only after the candidate's verdict is recorded.
- **Falsifier:** either of
  - no bust reduction at matched median above a pre-set minimum exceeding MC SE;
  - the advantage persists with the lock disabled, which would make it plain downsizing.
- **Decision:**
  - if supported, a successor through dd_protection change-control (pre-registration → re-MC → both-halves gate → ADR);
  - if falsified, the lineage keeps no sizing lever.
- **Build needs:** a state-dependent size vector, a second protection mechanism in `simulate_path`, and a lock-day output.
- **Disclosed:**
  - the early-phase reading was declined on 10-10 (C-1/C-6), and readiness map Q4 deferred it to a funded-stage study;
  - integer rounding can collapse it: A2 §4 shows integer cushion sizing reproducing flat sizing, and a stand-down converting bust into timeout. Under the round-down rule, small legs also floor to zero (T00 card §8 basis);
  - cushion sizing failed robustness for ORB solo (Q-ORBSURV-1);
  - the successor stopping rule applies.

**2. Joint-loss and cost assumptions** (overlapping losses, execution).
- **Weakness:** no direct co-loss measure exists for Aegis, Striker and Vanguard together. The 1.24 joint-loss ratio on record is ORB-MYM v0.4 against MNQ. Add-fill slippage is likely optimistic.
- **Mechanism:** co-incident losing days deepen joint drawdown beyond what per-leg risk implies, and optimistic add fills understate the adds' cost.
- **Smallest test:** report co-loss ratios and a cost ×1.5 cell inside Stage 1. No extra arm and no extra K.
- **Falsifier:** co-loss consistent with independence, and the verdict stable at ×1.5.
- **Decision:** whether a leg-overlap or execution remedy is worth a separate candidate.

**3. Vanguard flatten truncation** (exits; FXIFY only).
- **Weakness:** a 10-18/19 timing read, not yet in the exposure log, indicates that Vanguard often holds past 16:00, which the harness's 16:00 own-flat cuts.
- **Mechanism:** the late-session hold may carry part of Vanguard's edge, or of its tail.
- **Smallest test:** a Vanguard-only port replay at 16:00 against a 16:45 own-flat on the same panels. Measure leg expectancy and the leg's share of joint H2 drawdown.
- **Falsifier:** no difference above a pre-set floor.
- **Decision:** whether a 16:45 FXIFY expression (a new candidate) is worth qualifying. Moot at FundedNext.

**4. Aegis regime exposure** (disclosure).
- **Weakness:** exploratory, protection-off grid rows show Aegis-alone busts concentrated in 2020-02..2022-07 and H1. In the smallest 2020-22 cell the failures are mostly timeouts.
- **Mechanism:** the lineage's cushion may lean on Aegis's 2022-26 drift. A shuffled-Aegis control matched the real book, which points to drift rather than diversification.
- **Smallest test:** Aegis alone on the sanctioned 2020-22 export under the candidate's rules.
- **Falsifier:** Aegis-alone 2020-22 bust under the candidate's rules is at or below its FULL bust plus 2 SE.
- **Decision:** a regime limit on the candidate's label.

**Not ranked: ORB/MNQ** (research only; ORB paused). For the record:
- **H-C,** an excursion-triggered conditional add, is the only unclosed ORB sizing lever. It needs an EM3 ruling first.
- **H-A** (Q-ORPREM-1) is deferred by Joshua.
- **H-B,** stop-and-reverse, conflicts with long-only books and with the hedging rules.
- None can report before 11-08.

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
- the FXIFY sheets (#867, #869).

**Pending dependencies** (recorded, not duplicated):
- **ORB underperformance diagnosis** (session local_da95ffcf, wf_47ae3056-307). Its output is unreviewed and uncommitted. H-B and H-C live only in a session scratchpad, a custody risk.
- **The packet r4 acceptance check**, then the coordinator's dated firm note (EMERY-RESEARCH-DOCS-1).
- **The #867/#869 FXIFY row**, held under SR-4.
- **CME ticket #04738415.**
- **The parity v2 contract.**

**Record gaps** (corrections belong to their owners):
- The S4 terminal stop is absent from committed owners.
- The Q-ORPREM-1 deferral is absent from its pre-registration.
- #873 closed 2 s after #876 merged, so #876's "open" is now stale.
- The T00 manifest's trial-9 closure is owed.
- The 10-18/19 timing reads are not in the exposure log.
- The 10-16 LucidPro alternative is recorded only uncommitted; this brief names FundedNext instead.

**Exposure:** every reader above goes into any trial-13 pre-registration.

## 9. Decisions for Joshua

1. Approve FundedNext Flex 150K as primary, with the G0-3 switch rule, reversing the provisional FXIFY-first order. That means accepting the G0-1(a) own-flat ruling in place of FXIFY's 30-day clock. Or keep FXIFY primary and price its clock through extensions.
2. Approve Stage 0 (G0-1 to G0-5), or stop here.
3. The G0-1 rulings, (a)–(h).
4. Send the G0-2 and G0-3 questions, through the coordinator's eligibility register.
5. The G0-4 private read, only after items 1, 3 and 4 and the hashed freeze record (§5 order).
6. Whether to land this note as a docs PR, after the coordinator's firm note or folded into it.
