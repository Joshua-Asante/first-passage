# Backtesting execution and reproducibility

Use this before running or interpreting a backtest. Record decisions in the
existing campaign/run output, not a new approval ledger. Resolve only ambiguities
that could change the claim. A missing execution assumption limits the verdict;
it is not permission to invent favorable fills.

## Choose the existing route

| Need | Use | Evidence limit |
|---|---|---|
| Inspect a TradingView backtest or supplied export | `pinescript-v6` for code semantics; `trade-csv-reconcile` for parsing and metric definitions; Step-0 in the parent skill for panel integrity | Export reconciliation checks the reported trades; it does not independently simulate their fills. Record tester settings and coverage. |
| Offline price-based or native-oriented research | Locate the campaign-owned runner through `REPO_MAP.md`, `lab/CATALOG.md` and its specification; inspect the actual code and CLI before reuse | A research port, TradingView emulator and native platform have distinct execution models. Compare event traces under a named model; matching totals alone is insufficient. Do not create a replacement framework merely to run a candidate. |
| Recompute trade accounting | `lab/research_utils/tv_static_equity.py`; stricter source/fee and simple-trade reconstruction in `lab/research_utils/tv_trade_ledger.py` and `lab/research_utils/trade_reconciliation.py` | Static recompute requires explicit point value and commission. Strict reconstruction has its own supported trade shapes; do not force pyramid/partial histories through a simple-trade model. Closed/excursion DD is not synchronized intraday equity DD. |
| Portfolio path or bootstrap simulation | Existing `core/mc/simulation.py` via the owning campaign's command | Consumes trade/path assumptions; it is not a price-to-order fill simulator. |
| Selection and uncertainty | Parent skill statistical sections; `futures-anomaly-discovery` for searched alternatives | Follow the owning specification and existing dormancy rules; a discovery result does not become untouched validation. |

From the checkout, use `fp.ps1 doctor` and the launcher instructions in
`scripts/README.md` before project Python work. Keep the separately pinned research
environment separate. Skill launchers require the repository; copied global
scripts are not standalone engines. Typical existing command shapes are:

```powershell
.\fp.ps1 python .claude/skills/strategy-validation/scripts/step0_battery.py --help
.\fp.ps1 python .claude/skills/trade-csv-reconcile/scripts/reconcile.py --help
```

Pass actual declared timeframe/session/coverage to Step-0. Select the reconciler's
supported archetype only when it fits; do not apply legacy baseline/scaling
options to unrelated futures research. Use `--help` and inspect current code for
exact arguments rather than assuming example/default settings fit the candidate.
Native comparators available in a working checkout can compare already captured
evidence; inspect their owning contract and provenance requirements first. Their
presence does not authorize platform capture or prove native behavior.

## Pin identity and chronology

- Pin exact candidate/code revision or hash, all effective settings, engine and
  dependency versions, seed where relevant, and baseline identity. Record symbol,
  contract, venue, vendor, data hashes/coverage, bar or tick resolution, missing
  periods and adjustments. A filename or continuous symbol alone is insufficient.
- State timestamp timezone, whether bars are open- or close-stamped, session
  calendar including DST/holidays/early closes, and roll schedule/adjustment.
  Avoid stitching adjusted signal prices to unadjusted execution prices silently.
- Trace feature availability -> signal -> decision -> order submission/change ->
  earliest eligible fill. Include higher-timeframe publication, warmup, fitting
  and normalization cutoffs. A close-derived signal cannot fill earlier within
  that same bar. Any same-close processing convention needs an explicit model.
- For bar-close and stop-entry logic, distinguish detecting a crossing at close
  from an order resting before the crossing. Specify activation, cancellation,
  expiry, gaps, stop-market versus stop-limit behavior and first eligible price.

For TradingView, pin calculation/order-processing and bar-magnifier settings,
chart type, timeframe, session and test-range mode with effective inputs. Verify
behavior against the actual Pine/runtime version when needed. Intrabar data may
cover less than the headline test range. Historical OHLC, realtime recalculation
and a native tick replay do not establish interchangeable fill behavior.

## Declare fill and accounting assumptions

- If a fixed stop and target are both touched within an OHLC bar, their order is
  unknown without adequate path data. Bound both feasible outcomes or label the
  engine's chosen ordering; do not present it as observed chronology.
- A trailing stop also depends on when favorable movement updates the stop. An
  OHLC bar's high and low do not establish that the raised stop existed before
  the low. Model the update path or bound feasible paths; fixed-bracket
  touch checks alone do not resolve a trail. Excursions stop at the original
  exit and cannot reconstruct an uncensored counterfactual.
- For limits, distinguish touch, trade-through and executable fills. State queue,
  liquidity, partial-fill, quantity and cancellation assumptions. OHLC touches
  prove neither queue position nor full execution. Do not infer live fill rates
  from a synthetic fill rule.
- Make commissions and slippage explicit, including zero values, currency,
  per-side/per-contract or percentage basis, tick/point values, quantity rounding,
  spread and gap handling. Avoid subtracting costs twice from net exports. Use
  relevant cost sensitivity, not a universal 4x hurdle.

Reproduce the named baseline on identical code/settings/data/model before
interpreting a difference; explain any mismatch rather than moving the anchor.
Use existing small synthetic accounting checks suited to the touched path: long
and short price-to-cash signs, round trips, quantity/fees, partial exits if
supported, timestamp ties and stop/target ambiguity. Hand-check a tiny known
trade. These establish implementation/accounting behavior, not predictive edge or
live execution realism.

## Evaluate and leave a reproducible return

Use chronological discovery, tuning and untouched validation periods. Fit features
and choose settings using information available at the decision time. Purge
overlapping labels/positions and account for dependence where relevant; do not
treat correlated trades as independent evidence. Match uncertainty and sample
sufficiency to the actual claim and effective independent information.

Record every searched alternative, including filters, exits, instruments,
abandoned variants and informal trials, using the existing K/search ledger where
applicable. Report unknown prior search as unknown. Once a validation window has
guided a change, label it discovery; preserve existing protected windows and
frozen configurations under their owners.

Return the exact command/environment and source/data/settings identities, run
status, baseline comparison, machine-readable trade/event ledger and summary
locations, searched alternatives, period roles, and decision-relevant limitations.
Retain enough timing and fill detail to explain the first divergence between
engines. Save private data/results only in their authorized project homes, never
in portable skill instructions. Separate reproduced accounting, execution-model
sensitivity and evidence of edge; state which conclusion the artifacts support.
