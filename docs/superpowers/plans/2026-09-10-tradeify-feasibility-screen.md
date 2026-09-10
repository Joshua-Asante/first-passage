# Tradeify bounded feasibility screen implementation plan

> **For agentic workers:** Use executing-plans for inline execution of this single component. Do not launch parallel workers or turn its steps into separate review waves.

**Status:** CLOSED - execution returned; disposition not accepted. See [closure record](../../notes/2026-09-10-tradeify-protection-selection.md#feasibility-screen-closure). All other frozen text is retained unedited from plan-only commit `69be794`.

**Goal:** Determine whether existing development histories provide enough evidence to justify further faithful replay engineering for the Tradeify campaign.

**Architecture:** One private analysis script aligns existing normalized trade ledgers, evaluates a fixed diagnostic menu over chronological historical windows, and writes one report. Reuse existing account comparisons where applicable; build no execution simulator.

**Tech stack:** Existing Python environment, standard library and installed NumPy; no new service, dependency purchase or data acquisition.

**Spec:** This document owns the bounded exploratory amendment. The governing campaign remains [Tradeify Select configuration](2026-09-02-seven-strategy-tradeify-select-configuration.md).

## Authority and boundaries

This is a narrow exception to the campaign implementation/data-execution HOLD: implementation and local execution of this daily-ledger diagnostic are permitted. Formal source/native replay, catalogue search, n1/n2/n3, final validation, production integration and deployment remain held. Existing frozen artifacts and the full retained catalogue are unchanged.

The screen uses development data and can influence later development decisions; record that exposure honestly. It is not independent validation, a provisional-winner selection, catalogue exclusion, or a new campaign attempt. No automatic promotion to faithful replay follows a favorable result.

Public artifacts contain this methodology and routing only. Input paths, trade histories, account figures, portfolio outputs and results remain in the existing ignored private audit area. No external transmission is authorized by this plan.

## Question and interpretation

Test whether historical return, loss clustering and speed make further engineering worthwhile. Retain the approved formal objective: unconditional median at most 200 business days, with failures/unresolved paths treated as infinite pass time; full/H1/H2 all-nonpass upper failure bounds at most 5% over the separately frozen overall horizon. This does not mean 95% passing by day 200.

This screen supplies descriptive historical frequencies only. It cannot certify either formal requirement or future-market probabilities. Overlapping starts are dependent. Daily realized PnL is not synchronized marked equity; neither a general upper nor lower bound on actual account failure is claimed, especially under overlapping positions. No confidence intervals or universal infeasibility claims.

## Fixed budget and output

- One component, one author, one consolidated review; no repeated cosmetic review cycles.
- Maximum eight active engineering/analysis hours, including preparation, testing, execution and review. Record elapsed effort. No automatic extension.
- If inputs/calendar semantics or evaluator compatibility cannot be established within this budget, stop with the exact blocker and completed evidence.
- Deliver one report with input/configuration digests, menu, dates, assumptions, descriptive results and an investment-of-effort disposition: reconsider, fragile, or worth a bounded faithful replay proposal. These are judgments with stated reasons, not statistical acceptance labels.

## Files and source grounding

Read-only owners inspected for this plan:

- `core/firm_rules.py`: explicit tier configuration; adding parameters alone does not establish engine support.
- `core/mc/preflight.py`: firm parameter conversion and inactivity assumptions.
- `core/mc/simulation.py`: EvaluationState, _drawdown_outcome, _has_passed and simulate_path. The used-account interface restricts inactivity handling; daily PnL paths are not execution replay.
- `core/dd_protection.py`: historical calibrated controls must not be silently imported as a new campaign policy.
- `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/`: existing frozen config, reconciliation manifest and local normalized ledgers; do not rerun its generator.

Create only under the existing gitignored audit root `.worktrees/tradeify-phase1-population/.superpowers/sdd/2026-09-02-seven-strategy-tradeify-select-configuration/feasibility-screen/`:

- `screen.py`: intake, deterministic diagnostic evaluator and report generation.
- `test_screen.py`: synthetic acceptance tests.
- `screen-config.json`: pre-output menu, calendar, input digests and assumptions.
- `REPORT.md`: sole human-readable output; retain machine-readable rows alongside it if needed for reproduction.

Do not edit production code, strategy ports, frozen inputs or existing reports. Verify this directory is ignored before writing private contents.

## Task 1: Bind inputs and freeze the diagnostic menu

- [ ] Locate the five canonical ledgers through the frozen configuration and manifest. Verify digests and reconcile each net total with its existing report; stop on mismatch rather than repairing or regenerating inputs.
- [ ] Read actual ledger fields and timezone conventions. Build a common weekday axis within the intersection of documented source coverage; preserve genuine no-trade weekdays as zeros, never treat missing coverage as zero. Label the axis weekday-based, not certified exchange sessions. Do not infer coverage from first/last trade dates.
- [ ] Allocate net PnL to its recorded exit date once, using the declared source timezone. Record that entry fees, carried positions and intraday marks are not reconstructed. Do not manufacture intraday lows from unsynchronized trade MAE/MFE.
- [ ] Freeze seven menu entries before evaluating any outcomes: each of the five sources individually at its captured size; Aegis plus Vanguard at their respective captured sizes; all five at their respective captured sizes. Both combinations are arithmetic diagnostics, not executable account configurations. No rankings are used to choose this menu.
- [ ] Freeze three diagnostic cash-flow scenarios for every menu entry: unchanged net PnL; positive daily net PnL multiplied by 0.90 with losses unchanged; negative daily net PnL multiplied by 1.10 with gains unchanged. These are arbitrary robustness probes, not calibrated fees, execution forecasts or new sizing policies. No proportional contract sizing or additional menu after results.
- [ ] Pin all inputs, menu, scenario formulas and calendar in screen-config.json. Any correction after output must preserve old output and explain why it is an input/implementation correction rather than result-driven tuning.

## Task 2: Implement and verify the small daily evaluator

- [ ] Use the explicit incumbent tier's recorded parameters, not legacy default firm constants. Record source/version and staleness; make no current-rule certification claim.
- [ ] Use a pristine hypothetical account for the main screen, explicitly not the used incumbent. A used-account companion is allowed only if an existing accepted snapshot is available without new capture; report it separately and bind its age and assumptions.
- [ ] Reuse _drawdown_outcome and _has_passed through a small local daily loop when compatible. Do not import historical dd scaling into fixed captured cash flows. Evaluate the existing floor against daily closing equity before updating the EOD peak; record the daily-resolution limitation. Count confirmed entry/exit dates for activity, including zero-net days, from ledger events. Do not use nonzero PnL as an activity proxy.
- [ ] Keep inactivity OFF as an explicitly disclosed diagnostic assumption; no claim that the screen verifies the operator's mitigation. Do not implement new governors, clipping, reservations or quantity changes.
- [ ] Before real input execution, write and run synthetic tests for: preserved zero days; total reconciliation; timezone date assignment; zero-net activity; floor touch before pass; correct EOD peak sequence; consistency delaying pass; failure time treated as infinity; insufficient follow-up excluded rather than padded; H1/H2 windows staying inside their own partitions; fixed stress formulas.
- [ ] Test known boundary cases directly against the existing production comparison functions. If compatibility requires production changes or a new accounting model, stop under the budget rather than expanding scope.

Run from the private component directory:

```powershell
python -m unittest discover -s . -p test_screen.py -v
python screen.py --config screen-config.json --output REPORT.md
```

The script must reject missing/nonfinite amounts, duplicate trade identities, input hash mismatch and incomplete coverage with an explicit error before results. No network access or random sampling.

## Task 3: Execute once and make the investment decision

- [ ] Split the aligned date axis chronologically into H1/H2 at its midpoint, assigning the odd extra date to H2. Evaluate full/H1/H2 independently; no windows cross a partition boundary.
- [ ] For each partition and fixed scenario, evaluate every start with 200 subsequent modeled weekdays available (start is day 1). Report counts and descriptive fractions for pass by 200, bust by 200 and unresolved at 200; these partition the eligible starts. Unresolved is not silently counted as eventual bust.
- [ ] Separately evaluate longer-horizon first passage only if the existing campaign has an explicitly frozen overall horizon and sufficient complete windows. Otherwise report longer-horizon failure NOT_ESTIMATED. Never substitute the 200-day horizon or a library default for the campaign horizon.
- [ ] Report unconditional median only when at least half the eligible starts pass within the observed horizon; otherwise state median not established within that horizon. Keep any median among passers separately labeled.
- [ ] Explain window counts, date ranges, dependence, development-data exposure, stress sensitivity and differences across halves. Portfolio sums do not establish admission feasibility or signal fidelity. Do not report binomial confidence bounds or qualification.
- [ ] Conclude with one reasoned disposition: reconsider further spend if even favorable diagnostics are weak; fragile if modest probes or period splits undo the apparent attraction; worth a bounded faithful replay proposal if attraction persists. Mixed or insufficient evidence must remain explicit, without forced numerical thresholds invented after results.
- [ ] Perform one consolidated correctness/interpretation review and close this component within the budget. Propose, but do not execute, a single faithful historical case if warranted. A solo case may avoid shared-symbol machinery; choosing a diagnostic case neither seals a winner nor excludes the remaining catalogue.

## Completion and stopping rule

Complete means a reproducible, honestly limited report or a concrete budget/input/compatibility stop. It never means a qualified strategy. Further simulator work requires a separate scope/cost decision informed by this screen; no automatic new repair wave, data capture, sampling attempt or deployment release.
