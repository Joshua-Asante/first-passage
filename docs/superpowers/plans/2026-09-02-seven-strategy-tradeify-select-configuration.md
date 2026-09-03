# Seven-strategy Tradeify Select configuration campaign

**Status:** INTAKE-BLOCKED — the seven strategy definitions and seven four-year backtest exports are
not present in this checkout. This document is an execution plan, not a pre-registration, result,
or authorization to trade.

**Objective:** find the configuration with the shortest defensible time to pass a
`Tradeify_Select_100K` evaluation subject to an out-of-sample bust probability below 5%, using the
seven supplied strategies without changing their signal rules after results are viewed.

**Safety boundary:** no strategy is deployed and the c1 rail remains disarmed. Research output can
recommend a configuration; it cannot arm the rail or place a trade.

## Decision contract

Before the first portfolio result is computed, freeze a campaign pre-registration containing:

1. the exact Tradeify product and rule snapshot (including effective date and primary-source
   captures), starting balance, target, drawdown clock and lock behavior, daily limits, consistency
   and inactivity rules, contract caps, permitted instruments/hours, and fees;
2. the primary objective: minimize median trading days to pass among configurations whose
   qualifying bound (item 3) is below 5%;
3. the safety decision rule: the safety estimand is `P(bust before pass)` over the evaluation
   lifecycle (item 5), and the qualifying statistic is a bound that carries **source-sample and
   model uncertainty as well as simulation error** (Phase 7). A Monte Carlo-only one-sided 95%
   upper bound is reported but can never qualify a configuration on its own — more paths shrink
   it toward zero without adding one day of history;
4. tie-breakers, in order: higher pass probability by the evaluation horizon, lower 95th-percentile
   time to pass, lower expected evaluation fees, lower tail drawdown, then fewer active strategies;
5. the evaluation horizon cap and the treatment of unresolved paths: a path still open at the cap
   counts as a bust in every safety statistic (the engine already tags these `horizon_cap`
   outcomes — `core/mc/simulation.py`); disclosing the unresolved share is not a substitute;
6. the allowed configuration grammar (strategy inclusion, integer contract quantities, session
   collision policy, daily loss governor, and any portfolio-level risk scale); and
7. the random seeds, bootstrap family, block-length selection rule, the joint-flat block-boundary
   rule (Phase 3), search budget, and the confirmation set;
8. the confirmation start date **derived** from the included strategies' final design-decision
   dates (Phase 0 field, Phase 3 rule) and the minimum confirmation length in trading days and
   expected trades; and
9. every Phase 4 screen cutoff as a number: dominance rule and margin, outlier-removal count and
   surviving floor, single-year/single-strategy dependence test, cost and slippage stress values,
   and the safety-screen threshold. No result-dependent adjective survives into the
   pre-registration.

If the exact 5% boundary is operational rather than statistical, report both the point-estimate
frontier and the confidence-qualified frontier, but only the latter may be called a pass.

## Phase 0 — Receive and inventory the evidence

Create a read-only intake manifest for each of the seven strategies and exports:

- strategy ID/version/hash, instrument, timezone, session, direction, bar size, and execution venue;
- export hash, row count, first/last timestamp, currency, quantity convention, and whether P&L is
  gross or net;
- complete trades, including entry/exit timestamps and prices, quantity, commission, slippage,
  maximum adverse excursion (MAE), maximum favorable excursion, and stable trade ID where
  available;
- the strategy's **final design-decision date** — the last change to any signal, filter, stop,
  exit, or sizing rule, from the author's own record — and the overlap between development/tuning
  and the reported four-year period. An unknown date is recorded as `UNKNOWN`, never guessed;
  Phase 3 treats `UNKNOWN` as the export's last timestamp;
- whether **synchronized intraday bars** (or timestamped intratrade equity paths) exist for the
  strategy's instrument and session across the full period, as distinct from a per-trade MAE
  scalar; and
- known parameter searches, rejected variants, missing trades, platform assumptions, and changes
  made during the backtest window.

**Hard stop:** summary reports or equity curves alone are insufficient for an intraday-honest bust
estimate. A scalar per-trade MAE is not intraday evidence either: it does not say *when* the
adverse excursion occurred relative to realized gains, the running peak, or the other strategies'
excursions, so it cannot place the trailing floor when trades overlap or several trades share a
session. Decision-grade trailing-floor evaluation needs timestamped intratrade equity paths or
synchronized bar replay across every included strategy. A strategy with MAE only, or neither, is
inventoried as `LOWER BOUND`-capable (the repository's existing honesty label —
`lab/research_utils/msl_score.py`); a configuration containing it can be screened but cannot
qualify (Phase 5, Phase 7). Never infer that an EOD-safe path is intraday-safe.

**Deliverable:** `INTAKE.md` plus a machine-readable manifest and a discrepancy report. No ranking is
performed in this phase.

## Phase 1 — Normalize and reproduce each strategy independently

Build one canonical event ledger in UTC while retaining exchange-local session dates. Preserve the
original trade stream and add normalized fields; do not silently repair source rows. Reconcile each
strategy to its source report on trade count, gross/net P&L, win rate, profit factor, maximum
drawdown, and monthly totals. Explicitly model:

- commissions, exchange/NFA fees, bid/ask spread, and adverse slippage;
- simultaneous positions, pyramiding, partial exits, overnight positions, and session boundaries;
- futures point values, tick sizes, contract rolls, and quantity multipliers; and
- the rule engine's order of operations at equal timestamps.

Acceptance tolerances are frozen before reconciliation. Material mismatches block that strategy
rather than being tuned away.

**Deliverable:** seven reconciliation reports, a canonical joint ledger, and deterministic tests
for unit conversion, timestamp ordering, and firm-barrier behavior.

## Phase 2 — Audit standalone quality and dependence

Measure each strategy without optimizing it: net expectancy, trade cadence, time in market,
drawdown, tail loss, year/quarter/month stability, long/short and session decomposition, parameter
history, and performance under higher costs. Then measure the joint book on the shared chronology:

- daily and intraday P&L correlation;
- joint-loss frequency and downside-tail dependence;
- collisions competing for the same contract cap or daily risk budget;
- regime/common-mechanism concentration; and
- contribution to pass speed versus contribution to bust risk.

Use this phase to eliminate malformed or economically non-viable inputs, not to pick the best
portfolio. Record every elimination with a reason.

## Phase 3 — Freeze the search and validation design

Partition chronologically, never by individual trade. Use a development segment for configuration
search and an untouched terminal segment for confirmation; add walk-forward folds inside the
development segment. For only four years of history, prioritize time integrity over maximizing the
training sample and disclose the small effective sample size.

**Confirmation start is derived, not chosen.** The confirmation segment begins strictly after the
latest final design-decision date among the strategies a configuration includes (Phase 0 field).
Recording an overlap never converts a development slice into out-of-sample data. A strategy whose
final design decision post-dates the export, or is `UNKNOWN`, has no untouched historical segment:
a configuration that includes it cannot qualify from historical data, and its confirmation moves to
a reserved forward interval whose first eligible bar is strictly after the pre-registration
commit. If the derived segment is shorter than the frozen minimum (decision contract item 8), the
outcome for that inclusion set is **no qualifying configuration**, not a shorter window.

**Block boundaries are joint-flat.** Bootstrap block edges may fall only at timestamps where every
included strategy is flat, so no resampled path inherits position state, orphan exits, or duplicate
entries from an unrelated block, and no position is ever forced flat to make a boundary. The
repository's rule snapshot records `weekend_holds: False` for the Tradeify tiers
(`core/firm_rules.py` — a configuration fact, re-verified against the Phase 0 primary-source
capture, not engine-enforced), so calendar-week boundaries are joint-flat for every venue-legal
strategy and match the existing week-block convention (`paired_blocks_from_daily`,
`lab/discovery/prop_survivor_scoring.py`). Block lengths are integer weeks. A strategy that carries
a position across a week boundary is venue-illegal and leaves in Phase 2; no state-preserving
stitching rule is admitted under this campaign.

**Freeze every Phase 4 cutoff here** (decision contract item 9). Phase 4 may not run while any of
its rejection rules is still an adjective.

Define a bounded search space. Start with `{off, 1 contract}` for each strategy, then permit larger
integer quantities or a small frozen set of portfolio risk scales only where standalone geometry
makes them reachable. Prohibit signal-parameter optimization. Count every evaluated configuration
and retain the complete trial ledger, including failures.

**Deliverable:** a committed pre-registration and configuration manifest created before the broad
search is run.

## Phase 4 — Fast deterministic screen

Run every allowed configuration once on the realized **development-segment** chronology and on
rolling start dates inside that segment. The confirmation segment is not loaded in this phase: a
screen that touches it turns Phase 7 into a second look, not a confirmation. Apply the exact
Select rules and event ordering. Reject configurations that:

- bust on the realized development path or breach a contract/session rule;
- cannot reach the target within the frozen horizon;
- are dominated on bust, pass rate, and speed under the frozen Phase 3 dominance rule and margin;
- depend on one year, one strategy, or the frozen number of top trades (Phase 3 outlier test); or
- exceed the frozen Phase 3 safety-screen threshold under the frozen cost and slippage stress
  values.

This phase is a cheap funnel, not evidence of a sub-5% bust rate.

## Phase 5 — Coarse joint Monte Carlo search

For survivors, resample **synchronized, joint-flat time blocks across all included strategies**
(Phase 3 block rule), drawn from the development segment only, so market regimes, flat days,
collisions, cross-strategy dependence, and position state remain aligned. Evaluate the trailing
floor intraday from timestamped intratrade equity paths or synchronized bar replay. A leg that
offers only a scalar MAE, or nothing, is scored on the end-of-day clock and the whole
configuration's result carries the `LOWER BOUND` label; a `LOWER BOUND` result cannot qualify in
Phase 7. Simulate every path to resolution (bust or pass) up to the frozen horizon cap and count
paths still open at the cap as busts in every safety statistic (decision contract item 5). Include
plausible execution stress and the actual inactivity/trading-day clock.

Use sequential allocation of compute:

1. a small common seed set for all survivors;
2. eliminate configurations whose uncertainty interval is clearly unsafe or dominated;
3. allocate more paths near the Pareto frontier and near the 5% boundary; and
4. checkpoint each batch so local compute can resume without changing seeds.

Rank by the frozen lexicographic objective, not by a post-hoc weighted score. Keep the full
bust-versus-speed frontier rather than reporting only a winner.

## Phase 6 — Robustness and falsification

Challenge the shortlist with:

- first-half/second-half and leave-one-year-out runs;
- block lengths spanning the estimated dependence horizon;
- worse commission/slippage and one-tick adverse fills;
- delayed entries, missed trades, and strategy outages;
- removal of each strategy and the best trades/month/year;
- higher downside correlation and clustered-loss stress; and
- alternative but rule-faithful same-timestamp ordering where source resolution is ambiguous.

A candidate fails if it needs favorable execution, one exceptional regime, or an arbitrary
timestamp convention to remain under the ceiling. No failed candidate is repaired by changing a
strategy's signal parameters inside this campaign.

## Phase 7 — Locked confirmation run

After selecting a small shortlist, run the derived confirmation segment (Phase 3) once. Then
perform a high-precision independent Monte Carlo with new seeds. New seeds make draws independent
only conditional on the same fitted block distribution, so the final report must include:

- the safety estimand `P(bust before pass)`: point estimate, numerator/denominator with
  unresolved-at-cap paths counted in the numerator, Monte Carlo standard error, and the one-sided
  95% upper bound from simulation error alone — reported, never the qualifying statistic;
- the **qualifying bound**, which carries source-sample and model uncertainty: an outer block
  bootstrap over the historical development weeks (B outer replicates, each re-fitted and
  re-simulated with fresh inner seeds; the statistic is the 95th percentile of the conservative
  bust estimate across outer replicates — the same two-level design as the repository's W1
  bootstrap-95th packet, `lab/analysis/c1/class_s_w1_bootstrap_honest_2026-09-02/`), together with
  the worst pre-registered Phase 6 partition (halves, leave-one-year-out). A configuration
  qualifies only if the outer-bootstrap 95th percentile, the worst partition, and the realized
  confirmation-segment path all clear 5%. If the outer bootstrap is infeasible within the frozen
  budget, the claim is explicitly limited to *under the fitted simulation model* and may not be
  called an out-of-sample bust probability;
- pass, bust, and unresolved-at-cap shares at the frozen horizon, with the unresolved share also
  shown folded into the bust numerator;
- median and 90th/95th-percentile trading days to pass, conditional and unconditional views clearly
  labeled;
- expected fees/evaluations to first pass;
- maximum drawdown and failure-mode decomposition;
- contract quantities and operational collision rules; and
- sensitivity tables and all disclosed limitations.

Only configurations whose confirmation evidence satisfies the frozen safety rule qualify. If none
does, the correct outcome is **no qualifying configuration**, not a relaxed ceiling.

## Phase 8 — Shadow-operational verification

Translate the winning research configuration into a venue-edition specification and replay it
through the production sizing/rule path in dry-run mode. Verify quantities, symbols, sessions,
duplicate suppression, disconnect behavior, daily reset, inactivity handling, telemetry, and the
operator kill switch. Paper/shadow results are an implementation-parity check, not an opportunity
to optimize the strategy.

Deployment remains separately gated by the repository's M1 acceptance and operator-GO rules.

## Compute and collaboration model

Use one canonical repository and artifact contract; do not let three assistants create three
incompatible simulators.

- **Codex:** own ingestion, the canonical rule-engine integration, reproducible batch runner,
  tests, and committed artifacts.
- **Claude Code:** independently review firm-rule semantics, event ordering, statistical design,
  leakage, and claims against artifacts.
- **Cursor:** assist with targeted implementation/review in the IDE and inspect data-shape issues
  interactively.
- **Local compute:** execute checkpointed simulation shards from immutable manifests. Every shard
  records code commit, input hashes, config range, seed range, environment, start/end time, and
  output hash; a deterministic reducer rejects overlaps and gaps.

Agreement between assistants is not independent statistical evidence. Independence comes from
untouched data, frozen decisions, new random seeds, and reproducible calculations.

## Session handoff protocol

At the end of every session, update a compact campaign state artifact with:

- current phase and gate status;
- input/code/config hashes;
- compute completed and remaining;
- findings labeled `EXPLORATORY`, `CONFIRMATORY`, or `BLOCKED`;
- defects and whether prior outputs are invalidated;
- next exact command(s); and
- decisions requiring operator input.

Never carry a numerical result into the next session without its provenance tuple. Never describe
a partial run as final.

## Immediate next action

Place or copy the seven strategy files and seven backtest exports into an accessible local intake
directory (kept uncommitted if vendor-licensed), then provide the exact path. Phase 0 can begin as
soon as those 14 inputs are visible. The minimum useful export has one row per trade with entry and
exit timestamps, prices, quantity, and net/gross P&L. Replayable intraday bars (or timestamped
intratrade equity paths) covering every strategy's instrument and session, plus each strategy's
final design-decision date, are required for a decision-grade trailing-drawdown result; a scalar
MAE supports only a `LOWER BOUND` result.

## Review reconciliation — 2026-09-03

Codex review of the first draft (PR #272, commit `aebb774`) raised six P1 findings and one P2; each
is folded into the phase it governs rather than appended as an exception:

| Finding | Where it now binds |
|---|---|
| Deterministic screen exposed the confirmation segment | Phase 4 (development segment only) |
| Development overlap recorded but confirmation still called untouched | Phase 0 field, Phase 3 derived start, contract item 8 |
| Monte Carlo-only upper bound ignores source-sample/model uncertainty | Contract item 3, Phase 7 qualifying bound |
| Scalar MAE treated as intraday evidence | Phase 0 hard stop, Phase 5 `LOWER BOUND` rule |
| Unresolved paths excluded from the safety estimand | Contract item 5, Phase 5, Phase 7 |
| Screen cutoffs left as adjectives | Contract item 9, Phase 3, Phase 4 |
| Block resampling silent on open positions | Phase 3 joint-flat rule, Phase 5 |
