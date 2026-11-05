# M6E fixed exploratory test implementation plan

> **For agentic workers:** Execute with superpowers:executing-plans. The coordinator retains combined acceptance.

**Goal:** Test whether the single operator-approved European-morning breakout expression merits further research after $6.60 round-trip costs.
**Architecture:** A self-contained research camp consumes hash-pinned private BAR_EXPORT files. Only aggregate results, code, metadata and file hashes are public; raw bars and per-trade details stay ignored.
**Tech Stack:** Approved fp launcher, Python, NumPy, canonical BAR_EXPORT decoders, pytest.
**Spec:** Operator's fixed rule approved in this chat on 2026-11-04; fully restated below.

## Global constraints and roadmap

- One parameter set and one outcome look; no optimization, alternate costs, holdout evaluation, portfolio sizing or builder-gate claims.
- Local work is necessary because vendor exports reside in the operator's primary checkout.
- R2 D9 reserves the final approximately 378 sessions: `docs/notes/2026-11-01-generation-phase-strengthening-DRAFT.md` section 10.1 at dba5b9424a74f77c9897192f5cd4ebc6280c8e4a. No date-pinned M6E R2 card was found. Restrict scoring to 2016-01-04 through 2024-12-31, leaving all 2025-2026 prices unexamined by this return test. Prior structural audit did inspect their metadata/coverage, not outcomes.
- Register the 18 M6E exports only; preserve other manifest entries. Select exactly nine year files (2016-2024) before decoding prices. Rehash all files at registration; rehash selected files before and after scoring.
- Fixed spec: Europe/London weekdays; reference four bars opening 07:00-07:45; first close strictly outside at 08:15, 08:30, 08:45 or 09:00; next bar open entry; stop at opposite range boundary; no target; flat at 10:00 open. One unit, one trade, no re-entry or other filters. Zero range and first-signal entry gaps at/beyond stop skip the day. Incomplete 13-bar 07:00-through-10:00 windows excluded and counted. Signal-bar extrema cannot stop a later entry. Entry-bar stop is active. Gap stops use worse open. The 10:00 bar's high/low are never used for execution.
- Gross P&L uses reference opens/stops; subtract $6.60 once per completed round trip (Tradeify $1.60 fees plus 4 total $1.25 ticks adverse execution). Slippage is not deducted twice. This is a fixed current-cost replay, not a reconstruction of historical fees.
- Report total/directional/yearly counts, gross/net dollars and net mean; net win rate, profit factor and closed-trade drawdown are descriptive. No account pass claims.
- Uncertainty frozen before outcomes: 10,000 circular moving-block bootstrap replicates, 20 eligible-day blocks, seed 20261104, percentile 95% intervals for mean net per trade. Resample days including no-trade days, then divide aggregate P&L by aggregate trade count. Apply same method to long/short and yearly subsets. These intervals do not adjust for wider historical strategy selection or model error.
- Geometry diagnostic: favorable excursion before 10:00 ignoring an earlier stop, divided by initial entry-to-stop distance; a counterfactual upper-bound measure, not realized profit or a new exit.
- Before prices are scored, register K=1 with `lab/discovery/register_search.py`, the sole machine K authority. Use its legacy bookkeeping schema with an explicit prereg and params file for this directly authorized exploratory run; this is not formal channel admission. The instrument ledger points to that manifest rather than becoming a second K authority. Do not fabricate a builder card or mutate the separate hash-chained builder ledger; future R2 registration must reconcile this exposure.
- Budget: three attempt/check cycles for implementation, one fixed empirical run, zero data purchases. Reassess on a boundary or repeated correction; do not weaken acceptance.

## Bounded execution handoff

**Selected outcome:** A reproducible fixed-rule report with registered input hashes and untouched reserved returns.
**Prerequisites:** Raw local files and prior structural audit exist; costs verified from Tradeify/CME on 2026-11-04; R2 reservation source read; fp doctor passes. Synthetic validation precedes returns.
**Ownership:** Codex executes inline and coordinates combined acceptance.
**Verification:** Synthetic cases exercise next-open entry, both signs, stop touches/gaps, signal-versus-entry-bar ordering, no re-entry, exact clock boundaries/DST, missing data, hash rejection, and sample fencing. Arithmetic checks reconcile totals with direction/year partitions. Capture launcher verification record and source/input hashes.
**Checkpoint:** Report sample fence before execution; report validation and then empirical conclusion to Joshua. Record evidence in the camp's RESULTS.md.
**Return boundary:** Stop after verified report and local task commit; leave R2's holdout, builder gates, MCL ORB R1 and EIA untouched. Failed data prerequisites stop outcome evaluation.

## Steps

- [ ] Register M6E-only hashes, save the immutable registration, open K=1 in `discovery_manifests/`, and expose the research look in `ops/instruments/M6E.md`.
- [ ] Write hand-calculated synthetic tests in the camp; run `fp.ps1 python -m pytest <camp>/test_experiment.py -q` and observe missing implementation fail.
- [ ] Implement the fixed simulator/strict loader and bootstrap; repeat the focused tests until valid within budget.
- [ ] Run once with explicit primary-checkout data root and ignored private output directory. Pin source hashes and enforce input hashes before/after.
- [ ] Reconcile results, report exclusions and limitations, add catalog/ledger pointers, inspect task diff, and commit only task files.
