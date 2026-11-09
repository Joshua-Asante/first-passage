# The Order (v4, draft)

A method for using AI agents to reach one stated objective without turning failed tests into endless work.

**In one line:** choose a goal, decide what evidence would change your mind, run the cheapest useful test, and do what you agreed to do. If you stop, actually stop.

**Status:** draft. Adopted only when Joshua approves it and its hash is received by the holder or recorded by scheduled self-email.

**Purpose.** Maximise decisive results per hour of Joshua's time. A result is *decisive* only when different possible outcomes were assigned different actions before the test, and the action the actual outcome requires then happens. Stopping can count.

**Principle.** Agents generate explanations cheaply. A constraint binds only if it depends on something they can't generate or rewrite: external evidence, another person's consent, restricted access, money or elapsed time. Delete any rule that can't name the failure it prevents.

Why each rule exists, and where the method comes from: [appendix](the-order-lineage.md).

## Responsibilities

- **Joshua, the operator:** sets the objective and constraints, asks outside parties, and rules. Agents can't choose the objective or write the contract's first two items.
- **Claude, the maker:** builds, runs registered tests and drafts findings. It can't resolve disputes or fill a missing external answer by inference.
- **Codex, the checker:** checks original evidence by a separate method, raises one challenge, and audits compliance. Reviewing Claude's summary alone is not a check.
- **The holder:** a named person who is neither Joshua nor an agent. Receives hashes, records deadlines, and executes any agreed stake. Never judges the project's merits.
- **External evidence:** market results, future observations, untouched test data, or written answers from the relevant outside party.

## The one-page contract

Before work begins, record:

1. The objective and how progress is measured.
2. The scarce input that limits progress, comparable cases and their typical success rate. Can agents increase that input per dollar? If not, pace agent work to its availability.
3. Budgets and expiry dates. Keep learning spend separate from expected income, and fund learning from a prepaid card with a fixed balance.
4. Required outside answers: question, recipient, date asked, dated human response, and exactly what it covers.
5. The conditions and deadlines that require stopping or shrinking.
6. Weekly operator hours (including this framework's administration), the maximum number of test rounds, and the end date. At most one active hypothesis, one build item and two open decisions.
7. Holder, optional stake, and review date.

Stopping or shrinking needs no permission. Anything else needs a contract.

## The eight steps

A failed requirement blocks progress and sends the work back to that step.

1. **Aim.** Write the contract, hash it, and send the hash before agents prepare any work packet. One objective may not become an excuse to continue another.
2. **Ask.** Get a dated written answer from a human for every dependency an outside party can refuse, covering the actual account and route. Until it arrives: no related spending, and at most two hours of route-specific work.
3. **Subtract.** Propose removing anything that no live claim, registered test, reserved dataset or reproducibility record needs. Build nothing for a future stage before the current stage exists. Deletions still go through normal review and merge. Money, safety, legal, review, CI and frozen-parameter controls stay unless Joshua explicitly authorises a change.
4. **Choose the test.** Prefer the test with the highest chance of changing the action per unit of cost. If money is involved, calculate the pass probability and the cost assuming no genuine edge; the checker re-derives that figure before any spend. Exploratory analysis is labelled *exploratory* and can't trigger an action.
5. **Register.** Before the test runs, commit and hash: a one-sentence falsifiable hypothesis, the threshold, the outcome-to-action mapping, related prior attempts, K, prohibited reinterpretations, the evidence date and the stop date. **K** is the number of variants tried on the same question and data, counting every configuration, filter, window and abandoned attempt in the claim's ancestry; the threshold must be deflated for it. Send the hash to the holder. Changes before the test starts need a new hash. **The registration freezes when the test starts.**
6. **Run and verify.** Run only the registered test. The checker uses a separate route: a rerun, a blinded re-implementation, an independent calculation, or the primary source. External evidence arrives on its stated date; if that is more than 14 days away, add an intermediate external check.
7. **Rule.** Before opening the results packet, Joshua writes five lines: his intended decision, his current belief, what would stop him, what he won't risk, and one outside source. He doesn't rule on the calendar day the results appear. Record the evidence verdict (CONFIRMED, FALSIFIED or NULL, as registered), then execute the mapped action. Quote both agents verbatim and log any departure as OVERRIDE. The checker flags breaches.
8. **Stop.** Complete the quarantine and the handwritten paragraph below.

**The mapping governs what happens next.** It must say, for each verdict, whether to apply the result, run another test, or stop; the result never reopens as a fresh menu. Another test needs a fresh registration and counts against the round limit. Acceleration or automation needs CONFIRMED. Record separately what the evidence showed and whether the mapped action happened. Silence means STOP.

## The claim ledger

For each claim record: ID, wording, verdict, date, a reproducible evidence reference (sha:path:line or command), failed criteria, K, parent claims, prohibited reinterpretations and the reopening condition.

A closed claim can support new building or spending only when its **New external fact** field holds evidence that:

- is dated after closure;
- meets the reopening condition written before closure;
- was predicted and registered by the successor before it was observed.

Eligible evidence is future data, untouched data, or a counterparty's written answer. A new name, route, firm, agent proposal or appetite for risk never qualifies. Successors inherit their parents' verdicts, K and negative evidence.

## Make stopping real

A programme STOP starts a **14-day quarantine.**

- Only closure work is allowed: results, ledger verdicts, preservation and retrospectives, in commits prefixed `closure:`.
- No successors, widening, asset-reuse plans, reopening proposals or "one final round". Agents draft no options.
- The checker inspects the commits; the holder rejects registrations dated inside quarantine.
- Joshua writes a paragraph by hand: should this objective continue at all, and what else could these hours buy? Quarantine ends on its date, not on a persuasive argument.

A declared pause (exams, say) goes on an external calendar. Work idles, and it counts as STOP, not a breach.

## Holder or witness mode

**Stake (optional).** A fixed sum held for a recipient chosen in advance, not Joshua. The holder sends it, without discussion, if:

- a registration changes after its test starts, or a contract changes after the outcome it governs;
- money is spent without the required outside answer;
- a successor is registered during quarantine;
- work continues past the contract's end date.

Otherwise it's returned at review. Without a stake, the holder is a witness.

**Witness mode (no holder).** Scheduled self-email plus an OpenTimestamps proof. This proves timing, not independent consent, so contracts and registrations can't be amended at all. Replacements apply only going forward and erase no existing obligation. Spending is limited to an explicitly approved data budget, still subject to Ask.

## Weekly review

Record four numbers:

1. decisive results;
2. hypotheses closed;
3. operator hours, from the session log (agents run only in sessions Joshua opens);
4. the share of agent work spent on the next test that could disprove the claim.

The headline is (1) ÷ (3) over **active weeks only**; quarantine and declared pauses are excluded.

- Two active weeks with no decisive result, outside a registered waiting period, stop everything except the cheapest test that could end the project.
- Administration above 20 minutes a week for two weeks means a rule is removed.

Monthly, count loosenings against tightenings. Quarterly, the checker audits the programme; a Degenerating or Falsified verdict pauses new spending.

## Six protected rules

- **E1.** Set consequences before outcomes.
- **E2.** Ask before spending.
- **E3.** Keep stops empty and quarantined.
- **E4.** Reopen only on a new, predicted external fact.
- **E5.** A gate counts only if CI, permissions, money or a date enforces it.
- **E6.** No ruling means STOP.

Changing one needs the holder's countersignature before the outcome it affects. Changes to CI enforcement count as amendments. In witness mode these rules can't be changed.

## Keep it small

- This document: target 1,500 words, maximum 1,800 (`wc -w`). A new rule displaces an old one.
- AGENTS.md: at most 800 words.
- Reviews: one pass, one challenge, one correction.
- No CI check yet enforces these caps or catches dangling links, and AGENTS.md is currently about 2,100 words. Until one exists, E5 means these caps are not gates.

## Test the framework itself

Reviewed on the later of **2027-01-16** and the round's quarantine end, then quarterly.

- One E1 or E2 breach triggers an audit; two mean Falsified.
- Any two of these trigger an audit: work during quarantine, a same-day ruling, a cap breached twice, operator hours over the cap in three weeks.
- By the end of the round plus quarantine there must be an executed decisive result or a clean STOP; otherwise the framework is Degenerating.
- A STOP taken on time by the registered mapping, with no E1 or E2 breach, counts as success even if nothing follows it.
- Within 60 days, at least one attractive continuation is declined and logged at the time.
- Decisive results per hour in active weeks 5–12 match or beat weeks 1–4.

## The current round

1. Name the holder, or declare witness mode.
2. Write the contract. Its limiting input is the supply of genuine edge, which agents can't cheaply increase.
3. Register each test's outcome-to-action mapping **before** its cost calculation is re-run. CONFIRMED permits only a separate deployment decision under its own contract, after quarantine. Any other verdict closes the claim.
4. Then the 14-day quarantine, no second round drafted, and Joshua's paragraph.
