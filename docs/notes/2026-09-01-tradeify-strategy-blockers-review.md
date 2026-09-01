# Tradeify viable-strategy blockers — a contrarian review of the landed PRs

**As of:** 2026-09-01  
**Decision question:** What is actually preventing a viable strategy for Tradeify, and what
should change now?  
**Scope:** the 126 first-parent PR merges visible in this checkout from 2026-08-23 through
2026-09-01. The repository is shallow and its oldest reachable first-parent PR is #103 on
2026-08-22, so this is **not** a complete August review. It covers the most recent nine-day burst,
including PRs #114–#251, but no conclusion below pretends that absent earlier history was read.

## Executive judgment

There is no nearly-viable Tradeify strategy being held up by one missing backtest, one Pine
implementation, or one operator approval. **There is currently no candidate that clears even the
new Vet front door.** The latest apparent lead, gap-conditioned ORB, was already-tested prior art,
violated a standing prohibition, had no demonstrated survival geometry, and was correctly dropped.
The earlier combined-book “pass” also disappeared under both-halves, tail-consistent sizing, and
intraday-honest testing.

The hard blocker is **candidate supply under an unusually hostile payoff requirement**. The current
Tradeify Select geometry demands a low drawdown path, adequate pass probability, weekly activity,
and roughly 65–70% win rate for much of the feasible region. Research has repeatedly produced
interesting predictors, proxy relationships, or pooled-window results—not a complete, costed trade
object with that payoff shape. Q-VOLREGIME is the best live mechanism evidence, but L3/L4 presence
is not L5 attribution and is not a strategy.

The organization is responding to that scientific scarcity mostly by increasing procedural
precision. That has improved honesty, but it is now also a displacement activity. In nine visible
days, 126 PRs landed; 120 touched Markdown, 53 touched `docs/SESSIONS.md`, 34 touched `STATE.md`,
and 29 touched the ADR index. Only 37 touched a `lab/analysis/` or `lab/strategies/` artifact.
Those categories overlap, so they are not a productivity score; they are a strong signal that the
unit of progress has become the repository transaction rather than the independently testable
trading idea.

**My recommendation:** stop treating “find a Tradeify strategy by 2026-11-08” as the base case.
Treat no strategy as the base case, run one bounded final campaign around Q-VOLREGIME, and make a
precommitted commercial decision afterward: either change the venue/tier/objective, accept a
manual or companion activity solution, or pause the programme. A volume-regime-conditioned ORB is
eligible **if** L5 first establishes genuinely new mechanism evidence and the pairing enters as a
new, fully pre-registered candidate—not as an informal overlay or another excuse to keep the funnel
busy.

## What the PRs establish as fact

### 1. The feasible target is narrow, and the strategy does not yet exist

- The 945-cell shape map is explicitly **not a strategy or backtest**. For Select/MFFU, the
  trailing-drawdown bust gate binds before the pass floor across much of the transition region,
  and the practical sourcing conclusion is a mechanism with measured win rate comfortably around
  65–70%, not merely positive expectancy.
- Tradeify Growth's wider rope improves some cells materially—including a feasible modeled cell at
  50% win rate—but that is a different tier and the model omits some real daily-loss semantics.
  It is evidence that **venue geometry is a first-order design choice**, not evidence that the
  current Select objective is solved.
- The current official answer after Vet is unambiguous: no available candidate clears it.

**Nuance:** a high win-rate target is not inherently impossible, but it strongly favors small-win,
large-left-tail strategies. That is precisely the tail shape a trailing drawdown venue punishes.
Optimizing win rate without jointly constraining conditional loss, clustering, and intraday MAE is
therefore likely to create attractive-looking but unpayable candidates.

### 2. The apparent progress has repeatedly been correction, not accumulation

- Q-RANGECOND went from a reported +24.75 percentage-point win-rate lift to +0.75 points after an
  overnight-window look-ahead defect was fixed; its verdict flipped from `RESOLVED` to `FALSIFIED`.
- A separate MYM overnight-window scope defect omitted the evening reopen. The unchanged routing
  does not make the defect immaterial; it shows that common data primitives did not have trusted,
  executable session semantics before outcome-bearing work used them.
- The Aegis+ORB combined book first appeared to have 0.01%/1.51% bust rates. Proper both-halves
  bootstrap, tail-consistent sizing, and intraday honesty left no tested configuration clearing
  the complete gate; representative failures were 4.02% and 4.34% against a 3% ceiling.
- The first Vet card initially passed and then dropped after review found wrong sizing provenance,
  missed prior art, unmeasured cost-R, inadequate reserved-sample power, and an activity-rule gap.

This is good falsification behavior, but it invalidates the comforting interpretation that the
programme is converging monotonically. It is instead still calibrating its measurement apparatus.
Until all candidate-defining clocks, sessions, costs, and sizing policies are contract-tested at
the primitive level, later statistical sophistication cannot rescue the evidence.

### 3. The live supply is mechanism evidence, not trade evidence

Q-VOLREGIME passes the L3 split-half presence test on MNQ and MYM and passes L4 in 7/7 valid years
for each instrument. That is the strongest current lead because it replicates across instruments,
halves, and years. But L5 attribution remains open. A relationship between bar volume and range
does not specify direction, entry, stop, target, holding period, costs, or drawdown path. Calling it
“almost a strategy” would repeat the proxy-to-candidate mistake the new pipeline was designed to
stop.

The correct next question is not immediately “can we condition ORB with it?” but neither is ORB
categorically excluded. The registered failures cover the tested conditioning gates and create a
high revival bar; they do not prove that every future conditioner must fail. If L5 establishes
genuinely independent volume-regime evidence, a volume-conditioned ORB may consume one of the
campaign's template slots as a **new candidate**, with fresh multiplicity, an independent reserve,
the applicable ORB admission floor, and full Tradeify survival testing. The governing question is:
**does the volume-regime observable discriminate one complete, venue-reachable trade template—ORB
or otherwise?** If not, it is useful market-structure knowledge and nothing more.

### 4. The process is rigorous locally but weak at portfolio-level learning velocity

The recent PRs formalized immutable candidate contracts, reachability-before-explore, reserved
confirm windows, multiplicity, terminal taxonomies, and a three-speed funnel. Those are sensible
controls. The uncomfortable problem is timing: much of this architecture arrived after many
candidate kills, while the same nine-day window generated enormous reconciliation traffic.

Review found real defects, so “remove review” is the wrong lesson. The better lesson is to move
review **upstream and reduce artifact surface**:

1. one primitive data/session acceptance suite;
2. one candidate contract;
3. one executable result packet;
4. one independent adversarial read before outcome access; and
5. one final disposition.

The current estate often needs multiple PRs to repair claims, mirrors, indexes, and ADR blast
radius after one empirical result changes. That is not free just because agent-hours are cheap:
it consumes operator attention, increases stale-claim probability, and makes reviewers spend
their best effort on consistency rather than assumptions. Operator attention is already named as
the binding resource, yet merge volume is optimized as if it were not.

### 5. “Tradeify strategy” conflates three different objectives

The repository presently mixes:

1. **an edge:** a confirmed tradeable strategy;
2. **a Tradeify placement:** that strategy clears Select's rules and sizing geometry; and
3. **a programme discharge:** it also contributes to a multi-firm falsifier before 2026-11-08.

The F1 reversal makes Tradeify count toward the firm-count again, but changes no strategy evidence.
This governance election can make the programme score easier without making the account more
profitable. Conversely, a confirmed strategy that fails Select may still be economically valuable
elsewhere. Keeping the axes separate in the candidate record is good; management decisions should
also keep them separate.

The weekly account-preservation trade is another clue. If a sparse high-quality strategy needs a
manual token trade or companion book to satisfy inactivity, then weekly activity is an
**account-level operational constraint**, not necessarily a property the alpha leg should be
forced to synthesize. Requiring every standalone candidate to solve it biases sourcing toward
overtrading. Decide explicitly whether manual preservation is an acceptable permanent operating
model; do not alternate between assuming it and excluding it.

## Main blockers, ranked

| Rank | Blocker | Why it is blocking | What would disconfirm this judgment |
|---:|---|---|---|
| 1 | **No complete candidate with the required payoff shape** | Current ideas are dead prior art, proxies, or fail honest tail/clock tests | A frozen complete template clears Vet, confirmation, and honest Tradeify MC without moved gates |
| 2 | **Select geometry may be commercially mismatched to available alpha** | ~65–70% WR plus low clustered/intraday loss and activity is a severe joint requirement | Two unrelated mechanisms clear the shape frontier at realistic costs and sizes |
| 3 | **Data-semantic trust is not yet foundational** | Two distinct overnight primitives were wrong; one created a false positive | Primitive-level session/clock fixtures cover every candidate feature before research and survive independent review |
| 4 | **Proxy-to-trade translation is missing** | VOLREGIME has replicated presence but no directional expression or L5 attribution | One predeclared full template is discriminated out of sample, not merely correlated with range |
| 5 | **Governance throughput overwhelms learning throughput** | 126 PRs/9 visible days; documentation surfaces dominate and empirical claims require cascaded repair | Fewer, larger decision packets produce more untouched confirmations with no rise in escaped defects |
| 6 | **Objective ambiguity** | Edge discovery, Select placement, account preservation, and four-firm discharge are treated as one finish line | Operator explicitly ranks these and accepts the consequence when one succeeds without the others |

## Assumptions I would challenge now

### “The November deadline creates useful urgency”

Only partly. A fixed falsifier deadline is useful if candidate arrival is roughly controllable. Here,
supply is acknowledged as unschedulable. The date can therefore incentivize near-neighbor reuse,
premature conditioning, or definitional changes such as firm-count rulings. Keep the date as a
programme stop, not as evidence that a candidate must exist by then.

### “More gates mean fewer false discoveries”

Only when inputs are correct and gates are independent enough to add information. The MNQ defect
passed sophisticated downstream gates because the corrupted primitive sat upstream. A smaller
pipeline with stronger data contracts can be safer than a larger pipeline with prose-enforced
semantics.

### “Tradeify is the customer, so Tradeify constraints must define discovery”

That can destroy option value. Use Tradeify reachability as an early placement screen, but retain a
confirmed edge even when the edition fails. If repeated confirmed edges fail only Select geometry,
the venue—not the research—is the falsified hypothesis.

### “Agent-hours are cheap, so exhaustive documentation is cheap”

False at the system level. Every new canonical surface creates review, reconciliation, search, and
operator-comprehension costs. The visible PR distribution and repeated reversed-evidence audits are
evidence of that tax.

## A bounded decision plan

### Next 48 hours: freeze reality, not another framework

1. Declare **zero current candidates**. Do not open an ORB conditioner before L5 attribution; after
   a genuine L5 pass, allow one only through the same two-template cap and new-candidate controls.
2. Freeze a tested data-semantics library for session windows, event clocks, costs, MAE, and sizing;
   require candidate code to import it rather than reimplement it.
3. Decide which commercial objective is primary: Select deployment, any Tradeify tier, or any
   confirmed portable edge. Record whether manual weekly preservation is acceptable.
4. Choose a single Q-VOLREGIME L5 question and precommit the maximum number of templates. If no
   complete trade template has a causal bridge, stop before measurement.

### One final campaign: Q-VOLREGIME only

- Allow at most one mechanism family and a small, frozen template count with multiplicity handled
  in advance.
- Run primitive fixtures and Pine/Python parity before outcome access.
- Require untouched confirmation, both-halves/year robustness, realistic costs, intraday MAE,
  and Tradeify MC in that order.
- Preserve a confirmed-but-venue-failed result as an edge; do not call it a total failure.
- No rescue edits. A changed stop, target, session, or filter is a new candidate and outside this
  campaign.

### Decision after the campaign

- **Confirmed + Select-clear:** deploy through the existing disarmed M1/B7 chain.
- **Confirmed + Select-fail:** change tier/venue or hold the portable edge; stop “fixing” it into
  Select.
- **Market-null/expression-fail:** pause Tradeify strategy discovery until a genuinely new sourcing
  channel appears.
- **Evidence-void/data failure:** repair the primitive once, then decide whether the untouched
  reserve still exists; do not narrate the broken run as progress.

## Bottom line

The programme's strongest achievement this month is not a candidate; it is a more honest account
of why prior candidates were not viable. That honesty should now be used to make a commercial
choice, not to justify another layer of process. **The likely truth is that the current supply of
alpha does not match Tradeify Select's geometry.** One bounded VOLREGIME translation attempt is
defensible. Continuing broad, unbounded search or treating ORB as a privileged rescue route is not.
If that attempt fails, the rational output is a venue/objective change or a pause—not a 127th PR
proving the funnel behaved correctly.

## Reproduction notes

The merge counts above were derived from first-parent history, treating subjects matching
`Merge pull request #` as landed PRs. “Code” and “research artifact” classifications were based on
changed paths and overlap with documentation; they are directional workload indicators, not a
claim about effort or quality. Commands used:

```bash
git log --first-parent --since=2026-08-01 --format='%H%x09%ad%x09%s' --date=short
git diff-tree --no-commit-id --name-only -r -m --first-parent <merge_sha>
git log --all --format='%ad %h %s' --date=short
cat .git/shallow
```
