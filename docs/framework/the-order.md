# The Order (v2)

**Adopted** when the holder receives this file's hash by email. Until then, bindings are degraded.

**Objective function:** decisive results per operator hour toward one stated objective. A result is **decisive** if a prior registration maps different outcomes to different actions and the mapped action then happens.

**Premise.** Agents make text nearly free, so a brake binds only if it costs what agents cannot produce: third-party answers, dates, money, a person other than the operator. A rule that cannot cite the failure it prevents is deleted.

## Roles

| Role | Who | Does | Never |
|---|---|---|---|
| Operator | Joshua | Writes the contract, asks counterparties, rules | Delegates the frame; rules on the readout's day |
| Maker | Claude | Builds, runs registered tests, drafts | Reconciles disputes; fills an external cell by inference; drafts contract items 1-2 |
| Checker | Codex | Re-derives results by a separate path; challenges once; runs the audit | Reviews only the maker's summary |
| Holder | A named person, neither Joshua nor an agent | About 15 min/month: matches emailed hashes, confirms the calendar end date, holds a forfeit stake | Judges scope |
| Oracle | Market, untouched holdout, forward data, counterparty human | Outcomes agents cannot produce | — |

Without a holder: a scheduled email to self plus OpenTimestamps, marked "bindings degraded".

## The programme contract (one page)

1. Objective in one sentence; measure of progress.
2. Binding input X; reference class and base rate; can agents raise X per dollar? If not, agent work runs at the rate X arrives.
3. Tuition and income budgets with end dates. Tuition sits on a **separate prepaid card** at the fixed amount.
4. Ask-first ledger: question, party, date asked, dated human answer, scope.
5. Kill rule: a state plus a date, with its action.
6. Caps: operator hours/week including all Order overhead; WIP of one hypothesis, one build item, two open decisions; round ceiling; end date.
7. Holder, forfeit stake, review date.

Stopping or shrinking needs no permission. Starting, continuing, widening or reopening needs a contract.

## The order

A failed gate sends work back to that step.

| # | Step | Gate | Binding |
|---|---|---|---|
| 1 | **Aim** | Contract emailed to the holder before any agent packet | Holder's inbox timestamp |
| 2 | **Ask** | Every premise a third party can refuse has a dated written answer from a human there, for the exact account and route | Blank cell: no spend, at most 2h route-specific work |
| 3 | **Subtract** | Each requirement, datum and module is named by a live claim or registration, or is a holdout or reproducibility manifest. Otherwise it is deleted. Nothing is built for state N+1 before state N has happened | One rule in, one out; CI config hash held by the holder |
| 4 | **Cheapest decisive test** | Tests ranked by P(changes the action) ÷ cost; the top one runs. If money is involved: an economic-null card (pass probability and cost at zero edge) | Checker re-derives the zero-edge probability separately before spend |
| 5 | **Register** | Hash-pinned commit with no results: one-sentence falsifiable H, threshold, action per outcome, ancestry and honest K, forbidden reinterpretations, oracle date, kill date | Emailed to the holder; amendments countersigned before readout |
| 6 | **Verify** | Checker re-derives by a separate path (re-run, blinded re-implementation, primary source); oracle speaks on its date. An oracle date over 14 days out needs an intermediate oracle or a named justification | A date nobody controls |
| 7 | **Rule** | Before opening the packet, the operator emails the holder a five-line note: decision, belief, the fact that would stop him, what he won't risk, an outside source. Mapping applied; both agents quoted verbatim; departures logged as OVERRIDE | Not on the readout's calendar day; checker flags violations |
| 8 | **Stop** | Programme STOP (kill rule, end date, or operator): quarantine complete, paragraph written | External calendar date held by the holder |

**Exits from step 7:**
- **INTEGRATE** executes the mapped action and records the claim as CONFIRMED. Only then may the work be accelerated or automated.
- **ITERATE** returns to step 4 with a fresh registration, counted against the round ceiling.
- **STOP** goes to step 8. Silence is STOP.

**Failure each step prevents:**
1. Three objectives rescuing each other.
2. Tradeify was first asked 82 days after purchase, after the rail had grown from about 5k to about 56k lines (`b7eaff7:docs/notes/2026-10-10-tradeify-exclusive-use-replies.md`).
3. Regrowth after every cut.
4. Purchase before any zero-edge test.
5. The `53e35eb3` ceiling raise and `f977c20f` "§4 consequence narrowed" came after outcomes.
6. Text checked against text: about 1,000 merges with no strategy-signal fill or confirmed positive edge.
7. `53e35eb3` (14:28 ET) and `0290e3c3` (about 15:33 ET) were ruled the same day; "Packet decides".
8. R6 NO-GO `a5de124f`, then a new programme `0e26a7b6` about 19 hours later.

## The claim ledger

Each entry holds:
- ID, claim, status, date;
- evidence (sha:path:line or command);
- fired falsifiers and K;
- forbidden rescues and the reopening condition;
- parents;
- a **New external fact** cell.

The cell takes only evidence that meets three conditions. It is dated after closure. It meets the pre-written reopening condition. The successor registered it as a prediction before observing it. Valid sources are forward data, an untouched dataset or a counterparty's written answer. Relabels, new routes, new firms, agent proposals and risk appetite cannot fill it. While the cell is blank, no build or spend may cite the claim. Successors inherit their parents' verdicts, falsifiers, K and negative evidence.

## Stop protocol

- **Quarantine, 14 days** from programme STOP. Allowed: closure, preservation, retrospective. Not allowed: successors, widening, asset-reuse plans, reopening proposals, "one final round". Agents draft no options.
- **Checkable:** zero commits on programme paths (the checker verifies via git). The holder objects to any registration hash dated inside quarantine.
- **Operator paragraph**, handwritten: should the objective continue, and what would these hours otherwise buy? Its only gate is the date.
- **Declared pause** (exams): an external calendar entry. Everything idles, and it counts as STOP, not a breach.

## Weekly review

Four numbers, first thing:
1. Decisive results.
2. Hypotheses closed.
3. Operator hours from the session log (agents run only in sessions the operator opens).
4. Agent share spent on the next falsifier.

The headline is (1) ÷ (3). After two weeks with (1) = 0 outside a registered wait window, stop everything except the cheapest kill test. If overhead is above 20 min/week for two weeks, cut a rule.

Monthly, count loosenings against tightenings. The record ran about 9 to 5 (`53e35eb3`, `7a7d01c3`, `62c9d93e`, `722b920c`, `f977c20f`). Quarterly, the checker runs the programme audit. A Degenerating or Falsified verdict pauses new spend.

## Entrenched rules (hard core)

Amended only by holder countersignature, and only before the outcome they govern. CI config changes count as amendments.

- **E1.** Consequences before outcomes (re-entrenches Rules 23/24/28, deleted in `722b920c`).
- **E2.** Ask before spend.
- **E3.** Stops are empty and quarantined.
- **E4.** Reopen only on a new, predicted external fact.
- **E5.** A gate counts if CI, permissions, money or a date enforces it.
- **E6.** Silence defaults to STOP.

## Warning signs

| Anti-pattern | Sign |
|---|---|
| Moving the test | The threshold feels unreasonable with the number on screen |
| Inference for an absent fact | "safely infer", "accepted risk", "option-preserving" |
| Successor in the same breath | "supersedes in part", "close v1, open v2", "one final round" |
| Delegated frame | "Packet decides", "accept all recommendations" |
| Imagined states | "so it's ready"; a module in no verdict for 14 days |
| Review economy | A fourth round; nobody asks whether the artifact should exist |
| Governance regrowth | Most commits are docs-only; instruction files grow after a cut |

## Size cap

- This document: 1,800 words by `wc -w`, and 30 rules, counting every sentence with *must, never, only, at most* or *no*. v2 measured 1,767 words and 27 rules before this edit, so re-run both counts before adoption.
- The v3 target is 1,500 words and 20 rules. A new rule displaces one.
- AGENTS.md: 800 words. CI fails on a breach or on dangling references.
- Reviews: one pass, one challenge, one correction.

## Falsifiers of this framework

Reviewed on the later of **2027-01-16** and the round's quarantine end, then quarterly.

- **Hard core:** one E1/E2 breach triggers an audit; two mean Falsified.
- **Compliance** (two hits trigger an audit): something admitted during quarantine; a same-day ruling; a cap breached twice; hours over the cap in three weeks.
- **Outcome:** by round end plus quarantine, either one decisive result executed or a clean STOP. If neither, the verdict is Degenerating.
- **Restraint:** within 60 days of adoption, at least one attractive continuation is declined, logged by the checker at the time.
- **Success:** decisive results per hour in weeks 5-12 are at or above weeks 1-4, with zero E1/E2 breaches.

## Lineage

| Element | His source | External | Match |
|---|---|---|---|
| Aim | GRAND Aim/Measure | Goldratt TOC step 3; outside view | Exact |
| Ask | Q→D→S→A owner clause | Musk step 1; customer development; no-action letters | Strong |
| Subtract | The Algorithm; R1-R5; Great Prune | Musk delete; YAGNI; Gall's law | Near-exact |
| Cheapest test | Cost pre-gate | Value of information | Strong |
| Register | Rules 23/24/28 (deleted); K ledger | Registered Reports; Mayo severe testing | Very close |
| Verify | Codex verifies; Rule 0 | IV&V. Knight-Leveson: diversity reduces correlated error; only the oracle breaks it | Partial |
| Rule | His OODA adaptation | Stage-Gate; Klein pre-mortem; Duke tripwires | Close |
| Stop | Forward stop rule | Shape Up circuit breaker, cool-down, no backlogs; Duke kill criteria; Staw; Argyris double loop | Near-exact |
| Hard core, holder | Negative heuristics | Lakatos hard core/belt; Elster precommitment | Close |
| Reopening | R3 re-proposal bar | Lakatos-Zahar novel prediction | Close |
| Review | Programme audit | Lakatos MSRP; After-Action Review | Direct |

Musk's steps are spread across Ask, Subtract and INTEGRATE.

**What is new:** this is mostly a composite of Shape Up, Registered Reports/Stage-Gate, Duke's kill criteria and Elster's precommitment, appraised in Lakatos's terms. The new part is narrow:
- (a) A counterparty-ask gate and an oracle deadline applied to agent-generated work, with inference banned from the cell.
- (b) The premise that only brakes agents cannot produce count.

## Current round

Already in place: one registration naming all cards, a 4-card ceiling, an end date of 2026-12-31, about 1h/week, and a data-only spend line. Owed before the next readout:
- Name the holder; email the registration hash and end date.
- Write a contract naming the binding input: edge supply, which agents cannot cheaply raise.
- Record each card's mapping. CONFIRMED opens only a separate deployment decision with its own contract, never inside quarantine. Anything else closes the claim.
- Run the cost re-read first, as the cheapest kill test, and log ancestry in K.

Quarantine runs 14 days from round end, with no second round drafted. Joshua writes the paragraph.