# Seven-strategy Tradeify Select configuration campaign

**Status:** INTAKE-BLOCKED — the seven strategy definitions and seven four-year backtest exports are
not present in this checkout. This document is an execution plan, not a pre-registration, result,
or authorization to trade.

**Objective:** find the configuration with the shortest defensible time to pass a
`Tradeify_Select_100K` evaluation subject to a bust probability below 5% under the frozen qualifying
bound (decision contract item 3), using the seven supplied strategies without changing their signal
rules after results are viewed. The *out-of-sample* label attaches only under the confirmation-count
rule (item 11); otherwise the claim is model-fitted and says so.

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
8. the confirmation start date **derived** from the later of each included strategy's final
   design-decision date and last result-inspection date (Phase 0 fields, Phase 3 rule) and the
   minimum confirmation length in trading days and expected trades; and
9. every Phase 4 screen cutoff as a number: dominance rule and margin, outlier-removal count and
   surviving floor, single-year/single-strategy dependence test, cost and slippage stress values,
   and the safety-screen threshold. No result-dependent adjective survives into the
   pre-registration;
10. the **multiplicity configuration** required by the
    [campaign-envelope ADR](../../adr/2026-08-30-operator-approvals-campaign-envelope.md): the
    family-wise level `α`, the confirm count `M` (how many shortlist configurations may consume a
    confirmation slot), and the named procedure — **Bonferroni** (per-slot bar `α/M`, a number
    frozen here) or **Holm step-down** (algorithm identity frozen; thresholds `α/(M−i+1)` attach
    only after ordering). Frozen before Phase 4, applied to every slot in Phase 7, never revised
    mid-campaign; and
11. the **confirmation-observation rule**: the number `N_conf` of non-overlapping, joint-flat,
    untouched confirmation evaluations the reserved segment must supply before the out-of-sample
    label may attach. Zero busts in `N_conf` independent evaluations gives a one-sided `1 − α/M`
    binomial upper bound below 5% only when `N_conf ≥ ln(α/M) / ln(0.95)` — **59** at `α = 0.05`,
    `M = 1`, more for any `M > 1`. Rolling starts inside one segment overlap and do not count.
    When the derived segment cannot supply `N_conf`, the claim is frozen here as
    *model-fitted; unfalsified on the reserved segment* and may not be called out-of-sample;
12. every Phase 6 challenge as a number: the block-length set, the commission multiplier and
    adverse-tick values, the delay / missed-trade / outage rates, the added downside-correlation
    and loss-clustering amounts, the top-trade / month / year removal counts, and each challenge's
    verdict cutoff. A severity chosen after Phase 5 results are visible voids that challenge; and
13. the Rule 2 budget in the canon's own unit
    ([`inqhiori-canon.md` §15](../../methodology/inqhiori-canon.md)): loop class and iteration
    count, never a time or compute figure. This campaign is **STRATEGIC** (a funding-tier decision)
    and is composed of at most **3 constituent OUTER investigations** of **8** complete
    attempt-and-check iterations each, with no self-extension — proposed constituents (i) intake,
    normalization, standalone audit (Phases 0–2); (ii) frozen search and robustness (Phases 3–6);
    (iii) confirmation and shadow parity (Phases 7–8). External spend and local core-hours are
    disclosure lines beside the count, not the budget.

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
- the strategy's **last result-inspection date** — the last time the author, or any tool acting
  for them, viewed a backtest, equity curve, trade list, or summary covering any part of the
  export, whether or not a change followed. Viewing without changing still consumes the data.
  `UNKNOWN` is recorded, never guessed, and is treated like an unknown design-decision date;
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

**Reserve the confirmation window now, not in Phase 3.** As soon as the final design-decision and
last-inspection dates exist, compute the derived confirmation start (Phase 3 rule) per strategy and per candidate inclusion
set, split every export at that boundary, and **quarantine the reserved bytes**: a separate
gitignored directory, SHA-256 recorded in the manifest, and a loader assertion — not a convention —
that no Phase 1–6 code path can open them. Metadata (row count, first/last timestamp) may be read
from the whole export; no P&L, drawdown, cadence, or trade statistic is computed on the reserved
segment before Phase 7. Anything that can affect an elimination or a selection reads development
data only, from Phase 1 onward.

**Deliverable:** `INTAKE.md`, a machine-readable manifest, a discrepancy report, and the
reserved-window record (boundary timestamp per strategy, quarantined-file hashes, loader-assertion
test). No ranking is performed in this phase.

## Phase 1 — Normalize and reproduce each strategy independently

Build one canonical event ledger in UTC while retaining exchange-local session dates. Preserve the
original trade stream and add normalized fields; do not silently repair source rows. Reconcile each
strategy to its source report on trade count, gross/net P&L, win rate, profit factor, maximum
drawdown, and monthly totals **over the development segment only** (the report's subtotals or its
trade list filtered to that segment). Whole-period totals are reconciled once, in Phase 7,
immediately before the reserved segment is consumed; a mismatch there is `BLOCKED`, never a tuning
opportunity. Explicitly model:

- commissions and exchange/NFA fees **per instrument** — the tier scalar `cost_per_side_usd` in
  `core/firm_rules.py` is the index-micro row (MNQ/MYM/MES/M2K; its own comment prices MGC
  higher), so fees resolve through the per-instrument specs in `lab/discovery/cost_model.py`,
  never through one scalar — plus bid/ask spread and adverse slippage;
- simultaneous positions, pyramiding, partial exits, overnight positions, and session boundaries;
- futures point values, tick sizes, contract rolls, and quantity multipliers; and
- the rule engine's order of operations at equal timestamps.

Acceptance tolerances are frozen before reconciliation. Material mismatches block that strategy
rather than being tuned away.

**Deliverable:** seven reconciliation reports, a canonical joint ledger, and deterministic tests
for unit conversion, timestamp ordering, firm-barrier behavior, the **calendar-week inactivity
adapter** (Phase 5), the **multi-strategy joint block builder** (Phase 3), and per-instrument fees.

## Phase 2 — Audit standalone quality

Measure each strategy without optimizing it — **on development data only**; the reserved segment
stays quarantined (Phase 0) because every measurement here can feed an elimination: net expectancy,
trade cadence, time in market, drawdown, tail loss, year/quarter/month stability, long/short and
session decomposition, parameter history, and performance under higher costs. **Standalone limbs
only:** nothing in this phase composes two strategies, because the decision contract freezes the
design before the first portfolio result and the pre-registration does not exist until Phase 3.

Use this phase to eliminate malformed, venue-illegal, or economically non-viable inputs, not to
pick the best portfolio. Record every elimination with a reason; each rests on standalone evidence.

The joint-book limbs — daily and intraday P&L correlation; joint-loss frequency and downside-tail
dependence; collisions competing for the same contract cap or daily risk budget; regime /
common-mechanism concentration; contribution to pass speed versus contribution to bust risk — are
**portfolio results** and move to Phase 4, after the Phase 3 freeze, as its first step. They are
recorded there and alter no frozen field.

## Phase 3 — Freeze the search and validation design

Partition chronologically, never by individual trade. The development/confirmation boundary was
reserved and quarantined at intake (Phase 0); Phase 3 restates it, adds walk-forward folds inside
the development segment, and freezes both in the pre-registration. For only four years of history,
prioritize time integrity over maximizing the training sample and disclose the small effective
sample size.

**Confirmation start is derived, not chosen.** The confirmation segment begins strictly after the
**later** of the latest final design-decision date and the latest last result-inspection date
among the strategies a configuration includes (Phase 0 fields) — a viewed result is consumed even
when no change followed. Recording an overlap never converts a development slice into
out-of-sample data. A strategy for which either date post-dates the export, or is `UNKNOWN`, has no
untouched historical segment:
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
strategy. The existing single-series helper (`paired_blocks_from_daily`,
`lab/discovery/prop_survivor_scoring.py`) is the **precedent, not the tool**: it takes one
strategy's daily arrays, replaces real dates with a synthetic business-day index, and cannot assert
joint flatness. Phase 1 delivers a multi-strategy block builder that keeps real timestamps, aligns
holidays and differing active dates, and asserts that every included leg is flat at every block
edge, with tests. Block lengths are integer weeks. A strategy that carries a position across a
week boundary is venue-illegal and leaves in Phase 2; no state-preserving stitching rule is
admitted under this campaign.

**Freeze every Phase 4 cutoff here** (decision contract item 9). Phase 4 may not run while any of
its rejection rules is still an adjective.

**Freeze the multiplicity configuration here** (decision contract item 10): `α`, `M`, and the named
procedure. The shortlist that reaches Phase 7 is the first `M` configurations under the frozen
lexicographic objective on development evidence; no other configuration consumes a confirmation
slot in this campaign, and `N_conf` (item 11) is computed from the frozen `α/M` at the same time.

Define a bounded search space. Start with `{off, 1 contract}` for each strategy, then permit larger
integer quantities or a small frozen set of portfolio risk scales only where standalone geometry
makes them reachable. Prohibit signal-parameter optimization. Count every evaluated configuration
and retain the complete trial ledger, including failures.

**Deliverable:** a committed pre-registration and configuration manifest created before the broad
search is run.

## Phase 4 — Fast deterministic screen

Begin with the joint-book audit deferred from Phase 2 (dependence, collisions, concentration,
contribution), on development data, recorded but permitted to alter no frozen field. Then run
every allowed configuration once on the realized **development-segment** chronology and on
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
plausible execution stress and the venue's **calendar-week inactivity clock** — at least one trade
in each Monday–Friday week, the venue fact recorded in `core/firm_rules.py` — through the adapter
tested in Phase 1, never the engine's default of consecutive idle business days (`simulate_path`
`inactivity_limit`), which diverges on cross-week gaps and holiday-shortened weeks.

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

Every severity and cutoff above is a number frozen in the Phase 3 pre-registration (decision
contract item 12); a challenge whose parameter was chosen after Phase 5 results were visible is
void and clears nothing. A candidate fails if it needs favorable execution, one exceptional regime,
or an arbitrary timestamp convention to remain under the ceiling. No failed candidate is repaired by changing a
strategy's signal parameters inside this campaign.

## Phase 7 — Locked confirmation run

After Phase 6, order the shortlist by the frozen objective on development evidence; only the first
`M` configurations (decision contract item 10) receive confirmation slots, each judged at the frozen
per-slot level (`α/M` under Bonferroni, or the Holm step-down bar after ordering). Commit the
selected-set hash before anything below runs.

**Contract-integrity check, immediately before the reserved segment is touched.** Re-hash and
compare every frozen input (intake manifest, quarantined confirmation files), the code commit, the
configuration manifest, the pre-registration, and the committed selected-set hash; re-verify the
venue snapshot (symbols, sessions, contract caps, rule set, fees, inactivity clock) against a fresh
primary-source capture and against `core/firm_rules.py`; reconcile each strategy's whole-period
source totals (deferred from Phase 1). Any mismatch aborts **before** consumption: the configuration
is `BLOCKED`, the reserved segment stays unconsumed, and the discrepancy is filed. Phase 8 cannot
restore a consumed holdout, so nothing is deferred to it.

Then run the reserved confirmation segment once per slot and the high-precision independent Monte
Carlo with new seeds. New seeds make draws independent only conditional on the same fitted block
distribution, so the final report must include:

- the safety estimand `P(bust before pass)`: point estimate, numerator/denominator with
  unresolved-at-cap paths counted in the numerator, Monte Carlo standard error, and the one-sided
  95% upper bound from simulation error alone — reported, never the qualifying statistic;
- the **qualifying bound**, which carries source-sample, model, **and selection** uncertainty: an
  outer block bootstrap over the historical development weeks in which **every replicate re-runs
  the frozen Phase 4–5 selection procedure on its resampled development data** and then scores
  whichever configuration that replicate selects (B outer replicates, fresh inner seeds — the
  two-level design of the repository's W1 bootstrap-95th packet,
  `lab/analysis/c1/class_s_w1_bootstrap_honest_2026-09-02/`, extended by the selection step).
  Bootstrapping only the already-selected winner conditions on the selection and is not admitted.
  The quantile is taken at `1 − α/M` under Bonferroni (the Holm bar after ordering), not a fixed
  95th, and is paired with the worst pre-registered Phase 6 partition (halves,
  leave-one-year-out). A configuration qualifies only if that quantile and the worst partition
  clear 5% **and** the reserved segment does not falsify it (next bullet). If the
  selection-inclusive bootstrap is infeasible within the frozen budget, only a post-selection
  correction **named and frozen in Phase 3 with its reference** may substitute; otherwise the
  configuration cannot qualify and the claim is limited to *under the fitted simulation model*;
- the **reserved-segment falsifier**: one realized path per slot is one binary observation and
  cannot bound a 5% probability (zero busts in one trial leaves a one-sided 95% upper bound of
  95%). It is a falsifier, not an estimate: a bust on the reserved segment, or a realized
  time-to-pass outside the model's frozen predictive interval, fails the configuration outright; a
  non-bust only leaves the model-fitted claim standing. The *out-of-sample* label attaches only when
  the reserved segment supplies `N_conf` non-overlapping evaluations (decision contract item 11);
  otherwise the report labels the result **`model-fitted; unfalsified on the reserved segment`**
  and never calls it an out-of-sample bust probability;
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

Second Codex pass on `459421b` (2026-09-03) raised four further P1 findings:

| Finding | Where it now binds |
|---|---|
| Shortlist confirmed at 5% each — no multiplicity control | Contract item 10 (`α`/`M`/Bonferroni-or-Holm), Phase 3 freeze, Phase 7 per-slot level |
| No contract-integrity / venue re-check before the one-shot confirmation | Phase 7 integrity check (hashes, selected-set commit, venue snapshot, whole-period reconciliation) |
| One realized path treated as a 5% probability test | Contract item 11 (`N_conf` arithmetic), Phase 7 falsifier semantics, model-fitted label, Objective |
| Phase 2 eliminations read the holdout before Phase 3 reserved it | Phase 0 reservation + quarantine with loader assertion; Phases 1–2 development-only |

Third pass — Codex review of the orchestrator PR (#273, commit `6ca5577`, which carried this plan)
raised six P1 + four P2; the eight that bind the plan land here (the other two bind the
campaign-state artifact):

| Finding | Where it now binds |
|---|---|
| Confirmation start ignored the last result inspection | Phase 0 field, Phase 3 derived start (later of both dates), contract item 8 |
| Outer bootstrap conditioned on the already-selected winner | Phase 7 selection-inclusive outer bootstrap; frozen post-selection correction as the only substitute |
| Phase 2 computed portfolio results before the Phase 3 freeze | Phase 2 standalone-only; joint-book limbs moved to Phase 4 after the freeze |
| Phase 6 severities and cutoffs discretionary | Contract item 12, Phase 6 |
| Inactivity described as "5 idle days" while the venue clock is calendar-week | Phase 5 calendar-week adapter, Phase 1 test |
| `paired_blocks_from_daily` cannot build joint-flat multi-strategy blocks | Phase 3 precedent-not-tool, Phase 1 block-builder deliverable |
| Fees taken from the index-micro tier scalar | Phase 1 per-instrument fee authority |
| Rule 2 budget expressed in core-hours | Contract item 13 (STRATEGIC, ≤3 OUTER × 8 iterations) |
