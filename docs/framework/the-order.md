# The Order (v3, draft)

**Status:** draft; adopted when Joshua says so and the holder (or his self-email) receives its hash.

**What it optimises:** decisive results per operator hour toward one stated objective. A result is *decisive* when a registration made before the outcome maps different outcomes to different actions, and the mapped action then happens.

**Premise.** Agents make text nearly free, so a brake binds only if it costs what agents can't produce: a third party's answer, a date, money, or another person. A rule that can't name the failure it prevents is deleted.

## Roles

| Role | Who | Does | Never |
|---|---|---|---|
| Operator | Joshua | Writes the contract, asks counterparties, rules | Delegates the frame; rules on the same calendar day as a readout |
| Maker | Claude | Builds, runs registered tests, drafts | Reconciles disputes; fills an external cell by inference; drafts contract items 1–2 |
| Checker | Codex | Re-derives results by a separate path; challenges once; runs the audit | Reviews only the maker's summary |
| Holder | A named person who is neither Joshua nor an agent | About 15 min a month: receives hashes, holds dates, executes the stake (below) | Judges scope or merit |
| Oracle | Market, untouched holdout, forward data, a human at the counterparty | Outcomes that agents can't produce | — |

**Stake (optional).** Joshua gives the holder a fixed sum and a recipient chosen in advance, not himself. The holder sends it, without discussion, on any of these mechanical triggers:
- a registration or contract amended after its readout;
- spend recorded against a blank ask-first cell;
- a successor registered inside quarantine;
- work continuing past a contract's end date.

Otherwise it's returned at the review date. With no stake, the holder is a **witness**, not an enforcer, and is described as one.

**No holder (witness mode).** Joshua emails himself, with a scheduled send and an OpenTimestamps proof. That witnesses *timing*, so E1 remains checkable. It can't supply independent consent. So in witness mode registrations and contracts **can't be amended at all**, only replaced prospectively, and no money is spent beyond the data line.

## The programme contract (one page)

1. Objective in one sentence, and how progress is measured.
2. Binding input X, with its reference class and base rate. Can agents raise X per dollar? If not, agent work runs only at the rate X arrives.
3. Budgets with end dates. Tuition (learning) is kept separate from expected income. Tuition sits on a **separate prepaid card** loaded with the fixed amount.
4. The ask-first ledger: question, party, date asked, dated human answer, and what the answer covers.
5. Kill rule: a state and a date, with the action each triggers.
6. Caps:
   - operator hours a week, including this framework's own overhead;
   - work in progress: one hypothesis, one build item, two open decisions;
   - the round ceiling;
   - the end date.
7. Holder, stake (if any), review date.

Stopping or shrinking needs no permission; anything else needs a contract.

## The order

A failed gate sends the work back to that step.

| # | Step | Gate | Binding | Failure it prevents |
|---|---|---|---|---|
| 1 | **Aim** | Contract hashed and sent before any agent packet | Inbox or timestamp | Objectives rescuing one another |
| 2 | **Ask** | Every premise a third party can refuse has a dated written answer from a human there, for the exact account and route | Blank cell: no spend, at most 2h of route-specific work | Venue asked 82 days after purchase |
| 3 | **Subtract** | *Propose* deleting anything no live claim, registration, holdout or reproducibility manifest needs. Build nothing for state N+1 before state N exists | Deletions go through normal review and merge. Money controls, frozen parameters, review and CI requirements, and safety or legal controls stay until Joshua rules explicitly | Governance regrowth |
| 4 | **Choose the test** | Rank tests by P(changes the action) ÷ cost and specify the top one. If money is involved, add an economic-null card (pass probability and cost at zero edge). Exploratory calculations are labelled *exploratory* and can't trigger an action | Checker re-derives the zero-edge figure before any spend | Purchase before a zero-edge test |
| 5 | **Register** | Hash-pinned and committed **before the test runs**, with no results: a one-sentence falsifiable H, the threshold, the action for each outcome, ancestry and honest K, forbidden reinterpretations, oracle date, kill date | Hash sent to the holder; amendments only before readout, countersigned (never in witness mode) | `53e35eb3`, `f977c20f` |
| 6 | **Run and verify** | Run only the registered test. Checker re-derives by a separate path (re-run, blinded re-implementation, primary source). The oracle speaks on its date. An oracle more than 14 days away needs an intermediate oracle | A date nobody controls | Text checked only against text |
| 7 | **Rule** | Before opening the packet, the operator sends a five-line note: the decision, his belief, the fact that would stop him, what he won't risk, and an outside source. Then the mapping is applied, both agents are quoted verbatim, and any departure is logged as OVERRIDE | Not on the readout's calendar day; checker flags breaches | Same-day rulings; "Packet decides" |
| 8 | **Stop** | Quarantine finished and the paragraph written | An external date | `a5de124f` then `0e26a7b6` in about 19 hours |

**Exits from step 7.** The evidence verdict (CONFIRMED, FALSIFIED or NULL, as the registration defines them) is recorded first, separately from whether the mapped action happened.
- **INTEGRATE:** the mapped action is executed. Work may be accelerated or automated only when the verdict is CONFIRMED.
- **ITERATE:** back to step 4 with a fresh registration, counted against the round ceiling.
- **STOP:** go to step 8. Silence means STOP.

## The claim ledger

Each entry holds:
- ID, claim, verdict, date;
- evidence (sha:path:line or command);
- fired falsifiers and K;
- forbidden rescues and the reopening condition;
- parents;
- a **New external fact** cell.

The cell accepts only evidence that is dated after closure, meets the reopening condition written beforehand, and was registered by the successor as a prediction before it was observed. Valid sources are forward data, an untouched dataset, or a counterparty's written answer. Relabels, new routes, new firms, agent proposals and risk appetite never count. While the cell is blank, no build or spend may cite the claim. Successors inherit their parents' verdicts, falsifiers, K and negative evidence.

## Stop protocol

- **Quarantine, 14 days** from a programme STOP.
  - Allowed: closure-only commits (`closure:` prefix) that record RESULTS, ledger verdicts, preservation or a retrospective.
  - Not allowed: successors, widening, plans to reuse assets, reopening proposals, "one final round". Agents draft no options.
- **Check:** the checker verifies via git that quarantine commits are closure-only; the holder rejects registrations dated inside it.
- **Operator paragraph,** handwritten: should the objective continue at all, and what would these hours buy otherwise? Its only gate is the date.
- **Declared pause** (e.g. exams): an external calendar entry; everything idles; it counts as STOP, not a breach.

## Weekly review

Four numbers come first:
1. decisive results;
2. hypotheses closed;
3. operator hours, from the session log (agents run only in sessions the operator opens);
4. the share of agent work on the next falsifier.

The headline is (1) ÷ (3), computed over **active weeks only**. Quarantine and declared pauses are excluded.
- Two active weeks with (1) at zero, outside a registered wait window, stop everything except the cheapest kill test.
- Overhead above 20 minutes a week for two weeks means a rule gets cut.

Monthly, count loosenings against tightenings (First Passage ran about 9 to 5). Quarterly, the checker runs the programme audit; Degenerating or Falsified pauses new spend.

## Entrenched rules (hard core)

Amended only before the outcome they govern, with the holder's countersignature. In witness mode they can't be amended at all. CI configuration changes count as amendments.

- **E1.** Consequences before outcomes. This restores Rules 23, 24 and 28, deleted in `722b920c`.
- **E2.** Ask before spending.
- **E3.** Stops are empty and quarantined.
- **E4.** Reopen only on a new, predicted external fact.
- **E5.** A gate counts only if CI, permissions, money or a date enforces it.
- **E6.** Silence defaults to STOP.

## Warning signs

| Anti-pattern | What it sounds like |
|---|---|
| Moving the test | The threshold feels unreasonable while the number is on screen |
| Inference for an absent fact | "safely infer", "accepted risk", "option-preserving" |
| Successor in the same breath | "supersedes in part", "close v1, open v2", "one final round" |
| Delegated frame | "Packet decides", "accept all recommendations" |
| Imagined states | "so it's ready" |

## Size cap

- This document: at most 1,800 words by `wc -w`. The v4 target is 1,500. A new rule displaces an old one.
- AGENTS.md: at most 800 words.
- Reviews: one pass, one challenge, one correction.
- **Enforcement is pending.** No CI check yet enforces these caps or catches dangling references, and AGENTS.md is currently about 2,100 words. Until a CI check exists, E5 means these caps don't count as gates.

## Falsifiers of this framework

Reviewed on the later of **2027-01-16** and the round's quarantine end, then quarterly.

- **Hard core:** one E1 or E2 breach triggers an audit; two mean Falsified.
- **Compliance:** two of the following trigger an audit:
  - work admitted during quarantine;
  - a same-day ruling;
  - a cap breached twice;
  - hours over the cap in three weeks.
- **Outcome:** by the end of the round plus quarantine, either a decisive result has been executed or there has been a clean STOP. If neither, the framework is Degenerating.
- **Stopping success:** a STOP taken by the registered mapping, on or before its date, with no E1 or E2 breach, counts as success even if no week after it has any activity.
- **Restraint:** within 60 days, at least one attractive continuation is declined and logged at the time.
- **Yield:** across active weeks, decisive results per hour in weeks 5–12 match or beat weeks 1–4.

Lineage (sources and how close each match is): [the-order-lineage.md](the-order-lineage.md).

## Current round

Owed before any card runs:
- Name the holder, or declare witness mode.
- Write the contract. The binding input is edge supply, which agents can't cheaply raise.
- Register each card's mapping **before** its cost re-read runs. A CONFIRMED verdict opens only a separate deployment decision with its own contract, never during quarantine. Anything else closes the claim.

Then a 14-day quarantine, no second round drafted, and Joshua's paragraph.
