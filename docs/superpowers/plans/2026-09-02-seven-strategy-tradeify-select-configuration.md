# Tradeify Select configuration — bounded implementation plan

> For agentic workers: use the executing-plans skill for implementation. This file
> owns the current sequence; the campaign record owns evidence, gate dispositions
> and operator decisions. Read both before work. Do not execute historical dispatches
> whose obligations this plan replaces.

**Goal:** find the fastest qualifying configuration within a frozen, executable
grammar on the incumbent Tradeify Select 100K evaluation, or return no qualifying
configuration from one bounded attempt.

**Status (2026-09-05):** orchestrator transferred to Codex. The operator merged
campaign-only #302; scanner work is deferred to draft #307. Intake is not
complete. No configuration has qualified, no search has run, and the rail remains
disarmed. The operator approved S1/S2 below on 2026-09-05. Source binding,
live-state/replay implementation and the frozen statistical design remain owed.

**Architecture:** privately bound strategy expressions feed canonical ledgers and
synchronized intraday replay. A frozen composition policy feeds one deterministic
account-state transition model in screening, validation and execution parity.
Selection and final validation use separate random streams. The selected book is
a model-fitted proposal; Monte Carlo confidence is not evidence that its true
future-market pass probability is 95%.

**Tech stack:** existing Python core/MC and lab normalization; private Pine and
private strategy ports; c1 daemon, sizing host and venue registry for parity.
**Spec/evidence:** [campaign state](../../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md),
especially §4, §15, §17, §38, §41, §47–49. This revision replaces the old fourteen-item
sequence, which remains in Git history; it incorporates D20 rather than leaving
forward-confirmation requirements beside an incompatible accelerated path.

## Accepted boundaries

| Requirement | Executable consequence |
|---|---|
| Select incumbent; no Growth purchase | Score the incumbent. Growth may remain a comparison only, without a second selection/deployment attempt. |
| Failure probability at most 5% on full, H1 and H2 | Count every outcome other than pass as failure, including horizon_cap and inactivity failure. Use the fixed n3 sample only for final decision bounds. |
| Certified unconditional median no longer than 200 business days | S1 counts failed and horizon-unresolved attempts as infinite pass time. Minimize the frozen speed statistic among qualifying candidates; 200 is a reservation, not an estimated attainable result. |
| Select from five; at most one MNQ expression | Each expression may be off. Include at least one active expression. At most four can be active under the current roster. No forced MNQ allocation. |
| Exact source expressions | `aegis_6j1`, `orb_mnq_recon_v7`, `striker_dj30_mym_pyramid_250`, `striker_nas100_mnq_dow_wed_excluded`, `vanguard_mgc_v04`; identity comes from phase1_config.json and private input bindings, not names alone. |
| Striker election | The [two campaign expressions are admitted](../../adr/2026-09-05-tradeify-select-striker-expression-readmission.md) to selection and conditional evaluation deployment eligibility by operator election. Their ledger rows are CANDIDATE at zero capital. Existing locked editions and funded deployment remain barred; no old trigger is claimed to have fired. |
| S7 and account cap | Keep one controller per order symbol. Simulate the actual integer quantity and entry/add rejection policy under the account-wide cap, including outstanding reservations; do not use the sum of standalone peaks as actual concurrency. Runtime position truth must be proved before deployment. |
| Intraday-honest failure clock | EOD peak ratchets the fixed-dollar floor; synchronized intraday equity tests it. Missing timing evidence cannot qualify a book. |
| No parameter fishing | No post-result signal edits, new template, target relaxation, filter, governor or size added to rescue a loser. |
| D33 | One selected winner, one final validation. Any failed acceptance condition ends the attempt with no qualifying configuration. No runner-up promotion, extra paths or repeated n3. |
| Deployment | Winner parity, M1 RESOLVED and a separate operator GO. No agent places trades. Passing an evaluation does not authorize a funded Striker book. |

Venue specification was rechecked on 2026-09-05 against the
[Select evaluation page](https://help.tradeify.co/en/articles/12853921-select-evaluation-accounts):
100K target 6,000, drawdown 3,000, 80 micros, 40% consistency and at least three
trading days, without an evaluation daily loss limit. `core/firm_rules.py` remains
the implementation owner. Keep per-instrument commissions and session rules in
their existing authorities; never substitute the tier's index-micro fee for 6J/MGC.
The weekly operator token trade remains the accepted inactivity mitigation.

## Approved speed definition and final-validation timing

**S1 — approved 2026-09-05, unconditional speed:** let T be business days from deployment to
pass; T is infinity for a failed or horizon-unresolved attempt. Require a one-sided
95% lower confidence bound on P(T ≤ 200) of at least 0.50 on the full-history n3
sample. This certifies an unconditional median ≤200. A median among passers can
hide slow/failing attempts and is not interchangeable with this statistic.
This is the fourth acceptance condition; H1/H2 retain their failure conditions.
The joint requirement is at least 95% pass probability within the frozen overall
horizon and at least 50% pass probability by day 200, each with its specified bound.
It does not certify 95% passing by day 200. Report the pass-by-day curve from the
same sample to expose the slower tail; the curve adds no acceptance test or sampling.

**S2 — approved 2026-09-05, final validation after parity:** select a provisional winner on n1/n2,
complete its Phase 8 execution parity, capture the fresh live account state, then
consume the one n3 sample immediately before the deployment decision. Do not
validate at Phase 5 and later rerun n3 to refresh the account. If any bound, market
rule, executable fingerprint or account state becomes invalid after n3, stop for
the operator; no automatic second attempt. This sequence supersedes contradictory
pre-parity n3 timing instructions in historical campaign §15/§17. Building the
winner may incur implementation effort before a failing final test; that cost
does not authorize a runner-up or a second final sample.

**Decision record:** on 2026-09-05 the operator instructed, "fold in both
recommendations." S1/S2 are closed. The remaining intake, implementation and
pre-registration gates still control freeze readiness.

## Budget and stop conditions

The operator authorizes **one bounded implementation attempt** beyond the existing
intake effort. This is one end-to-end opportunity to build, freeze, select, validate
and disposition this book, not a reset of the three-constituent budget. Preserve D3:
constituent (i) Phase 1, (ii) Phases 2–3, (iii) Phases 4–8. Phase 1 is at iteration
6 of 8 including the pending population dispatch; two further cycles remain under
§47's accounting. Do not count worker pushes as new campaign attempts or let a
review loop run without a stopping rule. External spend remains zero unless the
operator authorizes it separately; disclose compute before the freeze.

Stop with a concrete disposition when: required inputs cannot be bound, a source
needs an unplanned data/platform dependency, no finite supported grammar remains,
the frozen search yields no provisional winner, the winner cannot execute faithfully,
or the single n3 fails. Missing operator evidence pauses dependent work; it does not
license fabricated inputs. A new venue, source family, repeat search or extra n3
requires a new operator decision. No further scanner research is in this attempt.

## Task 1 — Close the executable source inventory

**Files:** study `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/`, its existing
normalization tests, and campaign §47/§48. Private evidence stays in its ignored area.

- [ ] Complete the three partial captures recorded in §48 and obtain a fresh
  same-state export for each of all five sources. Bind each export byte-for-byte to
  its existing pin before creating the final immutable input snapshot.
- [ ] Read each pinned Pine together with its effective chart inputs. Classify
  quantity rounding, dollar/equity stops, pyramids, margin and account-state feedback.
  A coded default is not evidence that a branch was inactive in the captured run.
- [ ] For a size-dependent expression, require one matching source export per
  admitted size under the full intake gate, preserving D20's scaling-faithfulness
  rule. Reweighting realized trades cannot reconstruct suppressed trades.
  If additional exports are needed, give the operator one finite size menu before
  asking for them; no adaptive second menu after portfolio results.
- [ ] Complete §47's single regeneration and P1–P8 read. Preserve D32's asymmetric
  DD treatment and D30's UNESTABLISHED historical capital attribution. A runner's
  `phase1_verdict_cap=COMPLETE` means evidence coverage only; separately evaluate all
  campaign prerequisites before declaring the freeze ready.
- [ ] Review the final publication patch locally at its validated base; push only
  approved aggregate fields, digests, synthetic fixtures and metadata. #307 is not
  a prerequisite. No private history is transferred into the public branch.

**Acceptance:** five source identities and effective inputs are bound; legal size
sets are explicit; the existing reconciliation tests pass; blockers stay blockers.

## Task 2 — Repair the calculator and build the live-state transition

**Files:** `scripts/certification_power.py`, `tests/test_certification_power.py`;
then `core/mc/simulation.py`, `core/mc/preflight.py` and synthetic MC tests.

- [x] Reproduce the three A2 defects before repair: unattainable unit power,
  conflicting CLI operations, and mass deficit causing a wrong extreme quantile.
- [x] Fix those cases without changing the ordinary campaign pins. Verify the
  extreme quantile using exact integer arithmetic, not the calculator's own helper.
- [ ] Define a validated immutable initial state carrying original account basis,
  current equity, historical EOD peak, prior qualifying trade-day count and maximum
  prior profitable day. Fail closed on invalid/missing fields; source it privately.
- [ ] Keep the original basis in the target, fixed-dollar rope and consistency
  denominator. Initialize equity/peak/day history from the snapshot. Never pass
  current equity as `starting_equity` to emulate an already-used account.
- [ ] Verify synthetic cases: pristine-state legacy equivalence; same current
  equity with different prior peaks yields different floors; prior best day delays
  consistency clearance; prior trade days count; an intraday floor touch fails even
  if the close recovers; terminal pass at the initial state returns zero additional
  days; malformed and already-breached snapshots cannot begin a new evaluation.
- [ ] Build the synchronized bar-to-equity adapter, freezing within-bar conservative
  ordering, fees, partial fills/positions, cross-leg alignment and joint-flat block
  boundaries. Verify same-bar stop/target ambiguity, a cross-leg excursion overlap,
  an entry/add at the cap and an early-close cancellation. A false precision from
  scalar MAE is not a substitute for this adapter.

**Acceptance:** one deterministic transition is usable from both pristine and used
accounts, and the composition/replay outputs represent the eventual quantity policy.
Write the interface-level implementation specification before changing this core
surface; the existing calculator repair is independently testable and can land first.

## Task 3 — Freeze one finite, composable search

**Files:** existing campaign pre-registration location, one contract per retained
template, and the campaign-owned machine-readable configuration catalogue.

- [x] Record operator approval of S1/S2 and propagate the executable requirements.
- [ ] Confirm Task 1 and Task 2 are closed before computing portfolio rankings.
- [ ] Freeze exact source/override/bar/calendar/commission/code digests, the legal
  inclusion and integer size sets, one-MNQ constraint, order-event priority,
  cap/reservation behavior, sessions, and any portfolio protection policy. Reuse
  existing authorities; do not silently substitute locked legacy allocations.
- [ ] Enumerate the finite catalogue and record its size K. Remove structurally
  illegal cells deterministically. No unbounded optimizer or result-driven grammar.
- [ ] Freeze full/H1/H2 dates, horizon, joint-flat sampling family/block lengths,
  independent n1/n2/n3 stream identities and sample sizes, n1 continuation cutoffs,
  objective/tie-breaks, monitoring thresholds and all cost assumptions.
- [ ] Preserve D20's post-deployment robustness battery and freeze its severities,
  verdict cutoffs and down-only actions now: leave-one-year-out, dependence-length
  alternatives, commission/adverse-fill stress, delays/missed trades/outages,
  strategy and best-trade/month/year removal, downside-correlation/loss clustering,
  and rule-faithful tie ordering. Full/H1/H2 acceptance remains pre-deployment;
  the additional battery governs monitoring, never re-selection.
- [ ] Freeze the live time-to-pass predictive interval: quantiles, conditioning
  population, failed/unresolved-path treatment and clock origin at deployment.
  A live bust or time outside that interval falsifies the model-fitted proposal.
- [ ] Size power for the conjunction of all four acceptance conditions under S1.
  The speed and full-safety conditions use the same
  paths: the old equal-q three-limb `q**3` calculation is insufficient. Use explicit
  design alternatives for failure rate and pass-by-200 probability; never present
  these planning alternatives as measured true rates. Freeze a dependence-valid
  joint-power lower bound or a justified joint model before sample allocation.
- [ ] Keep confidence coverage distinct from power. For one fixed winner accepted
  only when every valid one-sided 5%-level test passes, the intersection-union
  false-accept bound does not require a blind Bonferroni division by four. A claim
  of simultaneous confidence coverage would be a different claim. Independent n3
  resolves winner selection; it does not remove historical/model uncertainty.

**Acceptance:** the catalogue, cutoffs, budgets and final decision can be executed
without a discretionary choice after results. No placeholder field is permitted
in the actual freeze. Freeze readiness is a separate orchestrator decision.

## Task 4 — Select once; prepare only the provisional winner

- [ ] Run the finite deterministic legality/cap screen, then n1 and independent n2
  on the frozen survivors. n1 is screening only; n2 alone supplies screening bounds.
  Reuse synchronized draws across candidate comparisons if frozen, while keeping
  stage streams independent. Record total work against the frozen path budget.
- [ ] Under S1, rank safety-screen survivors by the full-history upper confidence
  bound on unconditional median time; use a frozen complete tie order. Recommended
  remaining order: higher pass probability by horizon, lower unconditional p95
  pass time (possibly infinity), lower fees, lower tail DD, fewer active legs,
  then canonical configuration ID. This is selection, not final certification.
- [ ] If none survive, end. Otherwise seal one provisional winner's identity and
  configuration. Build only its private strategy adapters and required venue-edition
  bindings; generic M1 work can proceed independently. Test the actual daemon,
  listener, sizing and order lifecycle, not only offline exports.
- [ ] Prove cap reservations and position reconciliation under stale broker state,
  duplicate signals, rejected/partial orders, disconnect/restart and daily reset;
  fail closed when state is unknown. Prove exits/flattening cannot close another
  controller's position. Quantity and rejection behavior must match the simulation.
- [ ] Use the accepted eval-only admission record and add only the new
  lifecycle/LEG_MAP keys required by this winner. Preserve the
  locked-book and funded bars. If ORB wins, discharge its existing conditional
  superseding-ADR obligation. These are implementation gates, not new return tests.

**Acceptance:** one executable provisional winner with Phase 8 evidence; no promotion
is implied by a promising offline frontier. Do not add infrastructure unrelated to it.

## Task 5 — One final validation and operator decision

- [ ] Under S2, after parity and generic M1 readiness, capture the fresh
  private account state while flat and without pending orders. Record its digest
  and timestamp; token-trade history is included. Seal the implementation fingerprint.
- [ ] Run n3 once on this winner and snapshot. For each of full/H1/H2, require the
  one-sided 95% exact upper failure bound ≤0.05. Under S1 also require the full
  sample's one-sided 95% exact lower pass-by-200 bound ≥0.50. Include unresolved
  attempts in both denominators and treat them as speed infinity.
- [ ] Report the unconditional pass-by-day curve from these same n3 paths,
  retaining every attempt in the denominator. Label it descriptive; do not claim
  simultaneous confidence coverage across the curve or consume extra paths.
- [ ] Fail any condition: no qualifying configuration; no runner-up or extra draw.
  Pass all: publish the model-fitted decision evidence and request separate operator
  deployment GO only when M1 and execution gates are satisfied. Recheck snapshot
  identity before GO; a change invalidates this result's deployment applicability.
- [ ] Start the frozen forward clock at actual deployment. Apply only the frozen
  monitoring triggers and authorized down-only controls. No historical resample
  becomes new out-of-sample evidence, and no failure is repaired by re-selection.

**Deliverable:** one qualified model-fitted book ready for an operator decision, or
one explicit negative/blocked disposition with remaining dependency named. The
claim is fastest found within the frozen grammar, never proven globally fastest.
