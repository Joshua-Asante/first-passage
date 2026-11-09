# Continue or stop: the automated futures prop programme (2026-11-09)

**Asked by:** Joshua, 2026-11-09: "make a clear case for and against continuing … I want to know
at this point whether the programme is worth pursuing."
**Method:** seven evidence streams (edge, economics, external base rates, venue, operations,
assets and alternatives, the live pair), then a continue advocate and a stop advocate, a round of
rebuttal and a judge. Claude checked the deciding repo claims directly. External figures come from
the web-research stream and are marked *(external, not re-checked)*. Private figures (backtest
results, per-account dollars) were used in the analysis but are not reproduced here. Builds on the
[programme audit](2026-11-08-programme-audit.md).
**Codex challenge:** first round on cf65fe9 raised four findings, all applied in the next commit. One of them (the data-depth correction in §2.2) changes the recommendation.

## Verdict (Claude)

**Stop the prop operation now. It is not worth pursuing as a business in its current or any
expanded form.** That means sessions, venue work, scaling and the governance machine. There is no
demonstrated edge to scale, the upside is capped and controlled by one counterparty, and the
operation costs Joshua's attention every day.

**Keep one bounded research question open until 2026-12-31: is there an edge at all?** Codex
showed that data depth, the premise behind an outright stop, has eased (§2.2). The landed history
makes a small, pre-registered final round meaningful at no new spend. It is registered now with a
hard kill rule (§4). If it confirms nothing, the programme closes on 2027-01-02 for good.

The owned evaluation is not a reason to continue. Joshua may use it as a capped coda only if he
actively wants to sit the sessions (§4).

Both advocates independently reached "stop", with an optional harvest of the paid ticket. Codex's
challenge then corrected the stop case's strongest research argument, which moves the research
question from "closed" to "one last bounded round".

## 1. The case for continuing (steelmanned)

1. **The one real experiment has never been run.** Three months produced a native, Sim101-tested
   pair on an owned eval, with a hash-registered forward stop rule. No strategy-signal fill has
   ever happened (STATE.md). Stopping now leaves the forward question unread for good.
2. **The marginal cash cost is small.** The eval is paid for. If the AI subscriptions are cut, the
   running cost falls to the data line.
3. **"No confirmed edge" is weak evidence of "no edge".** The engine is underpowered. A true
   annualised Sharpe of 1.0 rarely clears the builder gate at K = 8 on about 3 years of data (that
   gate needs about 1.73; `git show 5510ca96^:docs/notes/2026-11-01-generation-phase-strengthening-DRAFT.md` §8.1).
   Order flow, longer native history and pooled designs are untested, not falsified.
4. **The payoff is asymmetric.** Loss is capped at fees. Tradeify allows owned native bots, and
   the native build ports to other NinjaTrader firms (two affirmed automation in writing on 11-05).
5. **Some mechanism-backed intraday effects exist in the literature** (late-day index momentum,
   *external, not re-checked*).

## 2. The case for stopping

1. **No edge has been demonstrated, and the pair failed the exploratory preservation test.**
   [`pair_evidence_case_2026-11/RESULTS.md`](../../../../lab/analysis/c1/pair_evidence_case_2026-11/RESULTS.md):
   "PRIOR STANDS". The pair fails the August preservation ceiling at eval sizing in both halves
   (Codex-verified, #1151 and #1170). That file also says it "does not show negative expected
   value", and G2 was not run. D1 accepts an unestablished edge, not an established absence of one.
   Commit subjects since 08-14 show 15 FALSIFIED, 3 NULL, 2 ABANDON and 0 confirmed.
2. **The binding research constraint is effect size after costs, not data depth (corrected after
   Codex review).**
   - The figure of about 1.73 applies to R1's 812-session window only.
   - The November landings (`git show 5510ca96^:docs/notes/2026-11-01-generation-phase-strengthening-DRAFT.md`
     §11; `core/data/tv_exports/cme/SHA256SUMS`) give usable windows of about 7.5 years for the index
     micros and about 10.8 years for 6J and M6E (the calendar binds).
   - With the §8.1 formula on those full windows, the floor at K = 8 falls to about 1.13 and 0.94,
     and at K = 1 to about 0.60 and 0.50. Development/holdout splits raise these.
   - So a single pre-registered card now has a reachable floor.
   - What binds instead is cost-adjusted effect size and the look budget:
     - §11 records 6J legs net negative at the builder's 1 tick per side, and M6E worse;
     - index overnight drift has decayed, and intraday momentum is underpowered;
     - the remaining lifetime looks are 2 per index micro and 4 per FX instrument.
   - Recent independent tests of ORB and OHLCV intraday momentum on NQ/MNQ find a small gross signal
     that costs consume *(external, not re-checked)*.
   - This weakens the stop case on the research question. It does not touch the operational case.
3. **The eval barely tells skill from luck.**
   [`PASS63_CHECK.md`](../../../../lab/analysis/_inbox/prop_payout_geometry_2026-10/PASS63_CHECK.md):
   the probability of passing within 63 days is 0.15 at zero edge and 0.39 at an annualised Sharpe
   of 2.0, a Sharpe the pair has never shown.
   - So a pass does not establish skill.
   - The table optimises sizing separately at each Sharpe and models a fresh 63-day account. It is
     not a likelihood calculation for the frozen pair under the coda's stopping rules, so no
     likelihood ratio is claimed here.
   - Comparable books need many months to pass, so any capped run most likely ends inconclusive.
4. **Even success has a low ceiling, and one counterparty controls it.** Exclusivity (D4) keeps the
   logic at Tradeify. Funded accounts are few, correlated and payout-capped, on a simulated account
   the firm can refuse to pay. `core/firm_rules.py` has no funded, payout or scaling rows.
   T1, T2 and Q5 have no written answer from a human, and Q5 has not been sent. Tradeify's
   October 2026 compliance FAQ lists accounts controlled by someone other than the registrant as a
   violation, which bears on the agent-operated premise *(external, not re-checked)*. Industry data
   show that a small minority of evaluation buyers are ever paid *(external, not re-checked)*.
5. **The economics are unmodelled, against a known fixed cost.** The confirmed recurring overhead is
   $370/mo ([ledger](../../../pursuits/SUBSCRIPTION_LEDGER.md)), mostly AI tooling. The break-even
   edge is **unknown**: there is no funded or payout model, G2 was not run, and PASS63 labels its
   funded figures uncalibrated. Spending on an operation whose payoff cannot yet be priced is itself
   a reason not to scale it.
6. **Joshua's attention is the binding cost, and nothing here saves it.**
   - The record: daily merges, rulings on most days, and a 20-decision sitting.
   - Every session needs its own GO and must be attended to the 16:45 ET force-flat.
   - Under D8 he places the weekly trade by hand.
   - The "automated" strategy needs a human throughout.
7. **The programme has shown it will not stop itself.** It loosened gates after adverse results,
   and it narrowed a fired falsifier after the outcome was known (audit Q4 and Q7). A wind-down has
   to be ruled now, before any outcome, or the next result will be absorbed the same way.

## 3. What survived the rebuttal round

- **Continue side.**
  - Survived: the forward read is otherwise lost, and the marginal cash cost is small.
  - Survived after Codex review: data depth no longer caps the research engine at small K (§2.2).
  - Did not survive: "a pass is strongly informative" (PASS63 shows a pass does not establish skill); "ORB has a
    mechanism-backed effect" (that evidence is for ORB-MNQ-1, and D1 says nothing transfers to
    O-0); "the failures were management failures, so fixable" (the market-facing results are
    negative either way).
- **Stop side.**
  - Overstated: the length of an uncapped run, and some economics drawn from unreviewed scenario
    code.
  - Codex corrected the stop case's data-depth premise, the likelihood-ratio bound and the
    break-even claim.
  - The operational verdict rests on points 1, 4, 6 and 7. The research verdict is now "bounded
    final round", not "closed".

## 4. What stopping means

**Ruled now, before any outcome:**
1. The prop operation ends as an investment. No new tooling, rail, gates, venue work or
   governance documents.
2. **One final research round, with an aggregate ceiling frozen before any exploration.** This is
   a channel-level ceiling as D18 requires, not just the per-instrument lifetime looks. Proposed
   terms, for Joshua to accept or change before anything runs:
   - **Aggregate ceiling: 4 cards in total**, across all instruments. That covers every development
     card and every holdout attempt. K = 4 is banked whether or not a card is run to the end. There
     are no replacement batches and no added instruments.
   - **Eligible instruments:** only those with landed, hash-registered data and remaining lifetime
     looks (the index micros, MGC, M6E, 6J).
   - **Selection:** the 4 cards are named in one registration before any exploration. They are
     chosen by stated rationale from existing dossiers and parked cards, never by outcome.
   - Each card must pass a cost re-read at the builder's frozen slip before it spends a look. A card
     that fails the re-read still counts against the 4.
   - No gate is loosened, and no data is purchased.
   - At most about one hour a week of Joshua's time, for acceptance only.
   - Deadline 2026-12-31.

   A card counts only if it reaches CONFIRMED under the frozen gates and Codex verifies it.
   Exhausting the 4 cards or reaching the deadline without that ends the round. The programme then
   closes on 2027-01-02, with no extension, no replacement batch and no repair round.
3. Cut recurring spend to the data line or zero by 2026-11-30, unless the AI subscriptions serve
   other work. Close the open ledger rows.
4. Choose one for the owned eval:
   - **(A) Full stop (default).** Stop the weekly preservation trade, let the eval lapse, write one
     closing RESULTS file (counts and hashes only) and archive.
   - **(B) Coda.** Only if Joshua positively wants to sit the sessions. Register before session 1,
     labels only:
     - a bust retires the pair and ends the prop path;
     - zero resets and zero purchases at any firm;
     - a hard cap of 20 attended sessions or 2026-12-31, whichever comes first, with no extension;
     - a stop-rule drop or halt ends it;
     - any human objection from Tradeify, or silence on Q5, T1 or T2 past 2026-12-01, ends it;
     - a proposal to loosen anything after an outcome ends it;
     - a pass authorises nothing; a funded stage would be a new decision with a payout model built
       first.

     The coda's information value is **unquantified, not ruled out**. The forward stop rule is a
     sequential test on strategy trades with keep, drop and fault outcomes. PASS63 does not
     evaluate this policy, so it neither establishes nor dismisses what the coda could show. What
     the coda cannot do is prove skill from a pass or justify scaling. The default is still (A)
     because the coda's cost is Joshua's attended hours and the venue's open questions, not
     because it carries no evidence.
5. Close the programme by 2027-01-02 in every case unless step 2 yields a Codex-verified CONFIRMED card. A confirmed card reopens only the question of how to deploy it, as a new decision with a payout model built first.

**Kept:** the negative knowledge (the rejection register, closures and K ledgers), the validation
and Monte Carlo engines, the native build, and the operating lessons (requirements first; register
the kill rule before the outcome).

## 5. What would reopen it

Only new evidence, not momentum:
- a pre-registered, Codex-verified CONFIRMED result at an honestly reconciled K, from the final round
  in §4 step 2 or from deeper data obtained later under a rights ruling at a fixed budget;
- or a written answer from a human at Tradeify clearing T1, T2 and Q5, together with a reviewed
  funded and payout model showing positive cash at a Sharpe the candidate has actually shown.
