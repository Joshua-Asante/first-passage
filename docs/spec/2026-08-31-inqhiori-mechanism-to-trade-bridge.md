# INQHIORI mechanism-to-trade bridge and weighted phase budgets

**Status:** PROPOSED — draft for operator review; this document does not amend the canonical
INQHIORI phase contract or Rule 2 until ratified by an ADR.
**Date:** 2026-08-31
**Scope:** Trading investigations only. The general-purpose INQHIORI loop remains unchanged.
**Proposed owner after ratification:**
[`docs/methodology/inqhiori-canon.md`](../methodology/inqhiori-canon.md), at the end of Notice and
in the phase-budget section.

## 1. Purpose

The bridge sits at the **end of Notice, before Question**. It does not select a mechanism or
prematurely design the winning strategy. It forces the enriched Notice corpus to show how a
possible answer could reach an executable and economically meaningful test. That constraint
sharpens the Questions that follow: a Question must be capable of changing belief about either
the market relationship or its usefulness to a trade.

The bridge prevents two symmetric errors:

1. promoting a predictive proxy that has no entry, stop, exit, horizon, or costed payoff; and
2. forcing every useful market primitive to pretend it is standalone directional alpha.

A volatility, range, timing, or regime observation may honestly declare a **conditioner** role.
It must still name the independently signed trade family it could condition, or remain a
diagnostic pursuit with the smaller budget in §4.

## 2. Notice exit addition — mechanism-to-trade bridge

Every trading Notice that proposes graduation to Question appends the following block. Answers
are provisional and may be revised by later evidence, but no field may be silently omitted.

```markdown
## Mechanism-to-trade bridge (Notice exit)

### A. Observed object
- Phenomenon:
- Instrument(s), session, and resolution:
- Minimum observation that must remain true for this pursuit to matter:
- Adjacent nulls / prior failed families:

### B. Candidate role — choose one primary role
- [ ] Direction source
- [ ] Entry trigger
- [ ] Exit / target source
- [ ] Stop-placement source
- [ ] Sizing / risk conditioner
- [ ] Abstention / regime conditioner
- [ ] Diagnostic only — no candidate status; use the diagnostic budget

### C. Provisional trade expression
- Independently signed trade family, if this is a conditioner:
- Signal available at decision time:
- Entry event and clock:
- Initial stop / invalidation:
- Exit / target / time stop:
- Maximum holding horizon:
- Trade frequency or opportunity-rate prior:
- Payoff unit (ticks / points / R / currency):
- Round-trip cost and slippage basis:
- Minimum gross move and net edge required:
- Intended generic futures expression:
- Intended venue edition, if any (kept separate from the generic expression):

### D. Two discriminators
- Mechanism discriminator: what observable, statistic, null, direction, threshold, and
  coverage/power rule would distinguish a genuine market relationship from its strongest
  alternative explanation?
- Expression discriminator: what net-payoff result would show that the frozen trade wrapper
  usefully expresses the relationship?
- Separation rule: which outcomes mean MARKET-NULL, EXPRESSION-FAIL, VENUE-FAIL, or
  EVIDENCE-VOID / AMBIGUOUS-DESIGN?

### E. Reachability and budget
- Cheapest generous-input mechanism falsifier:
- Cheapest trade-expression falsifier:
- Data already available:
- TradingView data / tester limitations known now:
- Proposed INQHIORI weight: LIGHT | STANDARD | HEAVY
- Weight rationale (stakes, novelty, uncertainty, reversibility, and data cost):
- Phase budget selected from §4:
- Stop condition before Pine construction:
```

### Exit rule

The Notice may graduate only when one of these routes is explicit:

- **TRADE-BRIDGED:** a provisional complete trade expression and both discriminators exist;
- **CONDITIONER-BRIDGED:** the primitive names an independently signed trade family and states
  how it changes that family's stop, target, sizing, or abstention decision; or
- **DIAGNOSTIC:** no trade bridge is presently honest. The work may continue only under the LIGHT
  diagnostic budget and cannot reserve a confirmation window or claim candidate status.

Failure to bridge is not evidence against the phenomenon. It is a routing result: return to
Notice for missing context, keep it diagnostic, or STOP.

## 3. Two-level Question contract

Question authors write both levels before Hypothesize. The levels are distinct but paired.

### Q-M — mechanism question

> Does the noticed observable carry the pre-declared relationship, in the pre-declared direction
> and magnitude, beyond the strongest named alternative explanation?

Q-M owns the mechanism discriminator. It may resolve `SUPPORTED`, `MARKET-NULL`, or
`EVIDENCE-VOID / AMBIGUOUS-DESIGN`. It does not earn a strategy claim by itself.

### Q-E — expression question

> When encoded in the provisional trade expression or conditioner role, does that relationship
> improve a frozen, executable payoff distribution enough to clear costs and the declared
> economic threshold?

Q-E owns the expression discriminator. It may resolve `EXPRESSED`, `EXPRESSION-FAIL`,
`VENUE-FAIL`, or `EVIDENCE-VOID`. A generic expression and a firm-specific edition are scored
separately so a venue failure does not erase a market or strategy finding.

### Joint interpretation

| Q-M | Q-E | Interpretation |
|---|---|---|
| Supported | Expressed | Eligible to proceed through the remaining evidence and venue gates |
| Supported | Expression-fail | Mechanism primitive survives; this wrapper stops |
| Supported | Venue-fail | Generic expression survives; named venue edition stops |
| Market-null | Any apparent payoff | Stop and audit the payoff for selection, leakage, or an unnamed mechanism |
| Evidence-void / ambiguous-design | Any | No positive claim; Iterate only with a named design repair and remaining budget |

The two levels do **not** require two unrelated campaigns. They require two separately readable
claims in one campaign envelope so evidence about the market is not confused with evidence about
one implementation.

## 4. Weighted phase budgets

### 4.1 Weight selection

Weight is frozen at the Notice exit, before Questions are formed.

| Weight | Use when | Total OUTER attempt-and-check cycles |
|---|---|---:|
| **LIGHT** | Cheap, reversible, adjacent to known work; or diagnostic / conditioner work without a complete trade expression | **4** |
| **STANDARD** | A new but bounded mechanism-to-trade investigation with available data and ordinary implementation risk | **8** |
| **HEAVY** | Novel mechanism or null, material data/platform uncertainty, high-cost evidence, or a result that could cause a low-reversibility lock/capital decision | **8 + a reserved extension of up to 4, requiring operator GO at the cycle-8 tripwire** |

LIGHT and STANDARD fit within canonical Rule 2's current OUTER ceiling of eight. HEAVY does not
silently replace that rule: cycles 9–12 are a pre-disclosed **possible** extension, not an
entitlement, and cannot begin without the structured stop and operator decision Rule 2 already
requires. Ratification should amend Rule 2 to recognize this weighted form explicitly.

Weight reflects the **cost of being wrong and the difficulty of obtaining discriminating
evidence**, not enthusiasm for the idea. A pursuit may be downgraded to a smaller unspent budget;
an upgrade requires a structured stop, a reason the original Notice estimate was wrong, and
operator approval. Budgets are maxima, never targets.

### 4.2 Phase allocation

One cycle is one complete attempt-and-check unit: for example, one corpus construction and review,
one paired falsifier run and adjudication, or one Pine version plus parity check. Reading,
discussing, or making several trivial edits does not manufacture extra cycles; a materially new
data look, hypothesis variant, parameter search, or test implementation does.

| Phase deliverable | LIGHT (4) | STANDARD (8) | HEAVY (up to 12) |
|---|---:|---:|---:|
| Identify + Notice + bridge | 1 | 2 | 2 |
| Question + Hypothesize + frozen Pine test instrument | 1 | 1 | 2 |
| Investigate — Python Explore + frozen TradingView confirmation | 1 | 3 | 5 |
| Observe + Reflect + Integrate / Iterate / Stop packet | 1 | 2 | 3 |

Allocations are planning bounds. A phase may borrow an unused cycle from a later phase only if the
campaign still preserves at least one cycle for Observe/Reflect/closure. It may not borrow from
an untouched confirmation read by consulting that read early. Any phase exhausting its allocation
produces the Rule-2 structured stop; it does not quietly consume the next phase.

### 4.3 Early stop and escalation rules

- A failed generous-input mechanism falsifier stops Q-M without building Pine.
- An economically unreachable provisional expression stops Q-E before deep robustness work.
- Two failed design attempts on the same obstacle route to `AMBIGUOUS-DESIGN` unless the operator
  approves the HEAVY extension with a specific repair.
- No investigation receives HEAVY weight merely because STANDARD reached an attractive ambiguous
  result.
- A LIGHT diagnostic that discovers a complete expression returns to Notice and opens a fresh
  weighted envelope; it does not spend diagnostic observations as undeclared Explore.

## 5. Hypothesize exit — frozen Pine test instrument

For a trading investigation, Hypothesize now exits with both the ranked hypotheses and an
executable **Pine Script test instrument** for the paired Q-M/Q-E investigation. Pine construction
here is test design, not Integrate: it must not modify a production strategy or imply authorization.

The exit packet contains:

1. **Ranked hypotheses:** null plus distinct alternatives, each tied to predictions under Q-M and
   Q-E.
2. **Pine source:** a versioned `strategy()` when Q-E is tradeable; an `indicator()` is permitted
   for Q-M-only diagnostics, but it cannot establish Q-E.
3. **Frozen semantics:** symbol, timezone/session, bar resolution, signal timing, next-bar versus
   same-bar execution, pyramiding, stop/target ordering, commissions, slippage, position sizing,
   date windows, and every exposed input.
4. **Python/Pine parity contract:** common fixture dates or event rows, expected signal counts,
   entry/exit timestamps, and tolerated numeric differences. Known irreducible differences are
   declared before either result is interpreted.
5. **Search contract:** parameters eligible for TradingView exploration, their ranges or discrete
   values, total look count/K charge, selection rule, and a confirmation configuration/window that
   optimization cannot read.
6. **Export contract:** required Strategy Tester CSV(s), naming convention, settings/hash record,
   and fields needed by Observe.

If a faithful Pine test instrument cannot be written, Hypothesize does not exit. The honest routes
are to revise the expression, return to Question, or STOP. A Pine implementation that changes the
hypothesis is a loop-back, not a coding detail.

## 6. Investigate — Python Explore, TradingView confirmation

### 6.1 Role of Python

Python is the fast, inspectable **Explore and falsification environment**. It is used for data
integrity, feature construction, nulls/placebos, cohort diagnostics, parameter exploration declared
in the search contract, and inexpensive rejection. Python may produce the candidate configuration
that advances to TradingView.

### 6.2 Role of TradingView

TradingView is the required **platform confirmation environment** for a Pine-deployable finding.
The frozen Pine instrument is run in Strategy Tester using its pre-declared settings. This checks
whether the finding survives TradingView's data, bar construction, order model, and strategy-engine
semantics—the environment in which the Pine implementation will actually be evaluated and used.

TradingView confirmation is not automatically an independent statistical holdout. If Python and
TradingView read overlapping dates or equivalent market data, agreement is **platform/execution
confirmation**, not a second independent replication. A claim of statistical confirmation also
requires a window or sample untouched by Python selection.

Required parity reporting includes:

- Python-only result;
- TradingView-only result;
- signal/trade-count difference;
- matched-event timing and price differences;
- net-performance difference under cost-equivalent settings;
- discrepancies explained, unresolved, or large enough to void comparability; and
- which environment governs each final claim.

A wide difference is a finding to investigate, not a reason to select the better backtest.

### 6.3 TradingView optimization

TradingView may expose useful optimizations that the Python implementation did not find. Those
looks are legitimate only under one of two routes:

1. **Pre-declared TV Explore:** inputs/ranges, look count, and selection rule were frozen in the
   Hypothesize search contract. The selected configuration is then read once on the reserved
   confirmation window.
2. **New observation:** an unplanned optimization or Tester discovery is recorded for Observe,
   but it cannot improve the current campaign's confirmation verdict. Reflect may ITERATE to a
   newly budgeted Question/Hypothesis packet with fresh confirmation evidence.

The best TradingView configuration is never silently substituted for the frozen Pine configuration.
Every tried configuration counts toward the campaign's declared multiplicity/K record, including
manual Tester changes.

## 7. Observe — CSV analysis and minimum observation packet

Investigate exports the frozen Python results and TradingView Strategy Tester CSVs. Observe
analyzes the exports rather than relying on the Tester headline panel or visual chart memory.

At minimum, Observe reports:

- settings, source/version hashes, symbol, resolution, and exact date range;
- gross and net results in common units;
- trade count, opportunity count, exposure, and activity cadence;
- win/loss shape, MAE/MFE where available, drawdown, and tail concentration;
- full window plus pre-declared temporal/regime partitions;
- Python-versus-TradingView reconciliation;
- Q-M discriminator result and Q-E discriminator result separately;
- surprises, thin cells, unresolved platform differences, and every exploratory TV look; and
- whether the observation minimum frozen at Notice has been met.

“Enough observations” is defined before Investigate as a coverage/power or decision threshold,
not as a favorable-looking equity curve. Until that threshold is met, Reflect may only conclude
`EVIDENCE-VOID`, ITERATE with a named evidence acquisition route, or STOP.

## 8. Reflect and terminal routing

Reflect interprets the observation packet only after the minimum observation threshold is met or
the evidence route is demonstrably exhausted. It records:

- what changed in the model;
- the separate Q-M and Q-E verdicts;
- whether Python/TradingView divergence changed confidence;
- which hypothesis is supported, refuted, or undetermined;
- remaining K and phase budget; and
- exactly one route:

### ITERATE

Deepen the investigation only when a named surprise, platform discrepancy, or unresolved
discriminator changes the next Question. The entry packet states the phase to return to, the new
information, a fresh or explicitly remaining budget, and what confirmation evidence remains
untouched. Optimization discovered after the frozen TradingView run normally routes here.

### INTEGRATE

Integrate a strategy or indicator only when the relevant claim cleared its minimum evidence,
Python/TradingView reconciliation is acceptable, and all separate lifecycle, risk, venue, and
human-authorization gates pass. Integration creates the production Pine/version, documentation,
and revalidation artifacts; the Hypothesize-phase Pine test instrument is not silently promoted.

### STOP

Stop when Q-M is null, Q-E is economically unreachable, platform results cannot be reconciled,
the evidence/design budget is exhausted, or the result is not valuable enough to fund another
loop. Record the re-proposal bar and preserve any surviving mechanism primitive without implying
that it is a strategy.

## 9. Proposed canon edits on ratification

Ratification should make four coordinated changes rather than inserting the bridge alone:

1. append §2's bridge template and routing rule to the canonical Notice exit;
2. replace a single undifferentiated Question with the paired Q-M/Q-E contract;
3. amend Hypothesize's exit to require the frozen Pine test instrument for trading work; and
4. amend Rule 2 with the LIGHT/STANDARD/HEAVY phase allocations and HEAVY extension tripwire.

The existing closure-resident `INTEGRATE | ITERATE | STOP` contract remains intact. This proposal
adds the Python/TradingView evidence packet that Reflect must interpret; it does not authorize
automatic promotion or capital changes.
