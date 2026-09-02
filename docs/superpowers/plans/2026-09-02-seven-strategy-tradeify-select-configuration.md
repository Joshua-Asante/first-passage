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
   conservative bust estimate is below 5%;
3. the safety decision rule: the **one-sided 95% upper confidence bound**, not only the point
   estimate, must be below 5% in the final independent simulation;
4. tie-breakers, in order: higher pass probability by the evaluation horizon, lower 95th-percentile
   time to pass, lower expected evaluation fees, lower tail drawdown, then fewer active strategies;
5. the evaluation horizon and treatment of unresolved paths;
6. the allowed configuration grammar (strategy inclusion, integer contract quantities, session
   collision policy, daily loss governor, and any portfolio-level risk scale); and
7. the random seeds, bootstrap family, block-length selection rule, search budget, and untouched
   confirmation set.

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
- overlap between strategy development/tuning and the reported four-year period; and
- known parameter searches, rejected variants, missing trades, platform assumptions, and changes
  made during the backtest window.

**Hard stop:** summary reports or equity curves alone are insufficient for an intraday-honest bust
estimate. If MAE is absent, obtain bar data for replay or label the first result EOD-only and
non-decision-grade. Never infer that an EOD-safe path is intraday-safe.

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

Define a bounded search space. Start with `{off, 1 contract}` for each strategy, then permit larger
integer quantities or a small frozen set of portfolio risk scales only where standalone geometry
makes them reachable. Prohibit signal-parameter optimization. Count every evaluated configuration
and retain the complete trial ledger, including failures.

**Deliverable:** a committed pre-registration and configuration manifest created before the broad
search is run.

## Phase 4 — Fast deterministic screen

Run every allowed configuration once on the realized joint chronology and on rolling start dates.
Apply the exact Select rules and event ordering. Reject configurations that:

- bust on the realized path or breach a contract/session rule;
- cannot reach the target within the frozen horizon;
- are clearly dominated on bust, pass rate, and speed;
- depend on one year, one strategy, or a small number of outlier trades; or
- already exceed a loose safety screen under modest cost and slippage stress.

This phase is a cheap funnel, not evidence of a sub-5% bust rate.

## Phase 5 — Coarse joint Monte Carlo search

For survivors, resample **synchronized time blocks across all seven strategies** so market regimes,
flat days, collisions, and cross-strategy dependence remain aligned. Where trade-level MAE or bar
replay exists, evaluate the trailing floor intraday. Include plausible execution stress and the
actual inactivity/trading-day clock.

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

After selecting a small shortlist, run the untouched chronological confirmation once. Then perform
a high-precision independent Monte Carlo with new seeds. The final report must include:

- bust point estimate, numerator/denominator, Monte Carlo standard error, and one-sided 95% upper
  confidence bound;
- pass and unresolved probabilities at the frozen horizon;
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
exit timestamps, prices, quantity, and net/gross P&L; MAE or replayable intraday bars are required
for a decision-grade trailing-drawdown result.
