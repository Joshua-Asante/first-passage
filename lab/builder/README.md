# `lab/builder/`: strategy builder v1 engine

Build steps 1–3 of Joshua's "Strategy builder v1 spec" (2026-10-30): the trial ledger, the ORB block library and compiler (backtest side), and gates 5a–5g with a traceable report, run locally. Venue MC (5h), Azure wiring, the Pine/NinjaScript compilers and the decay monitor are later build steps.

| Module | Job |
|---|---|
| `cards.py` | YAML card schema; library blocks only; timing checked against the instrument's session; canonical card hash; grid neighbours for the plateau gate |
| `ledger.py` | Append-only, hash-chained JSONL, verified in full on every read. K = distinct ledgered cards, per instrument or across the ledger (`k_scope`); holdout looks are their own entries, one per card |
| `instruments.py` | Day-session opens and the 17:00 ET day end; geometry from `core/instrument_specs` |
| `data.py` | The engine's own strict BAR EXPORT v0.2 reader (no shared lenient parser, no derived panels); the book file; the frozen calendar; the date-pinned split |
| `compile.py` | Card → trades on closed 15m bars, with the conservative fill rules in its docstring; skipped days counted by reason; no exit price without a bar at or after `flat_at` |
| `gates.py` | 5a–5g in order, stopping at the first fail; `THRESHOLDS` holds the spec defaults; verdict `survivor`, `killed` or `unresolved`; stage 8 holdout look |
| `run.py` | `python -m builder.run run.yaml`: validate the spec, ledger every card, load pinned data, evaluate, write `report.json` per card |
| `holdout.py` | `python -m builder.holdout run.yaml`: after a finished development run, one ledgered look per survivor in card-id order, `<card id>.holdout.json` each |

Rules the engine enforces:
- **Inputs fail closed.** Every input the engine reads has a stated condition, and a load that breaks one aborts the run before any gate result exists. The invariant table is in the PR that introduced this rebuild, and each row has a test in `tests/lab/test_builder/`. Nothing degrades to a skip, a default or a warning. The one deliberate exception is a day the compiler can't trade, and it is counted in `report.skipped_days`.
- **Ledger first.** A card is appended before any bar is read, and the engine refuses a card that isn't in the ledger.
- **Pinned inputs.** run.yaml pins the sha256 of every data file, the book and the calendar. A supplied book must cover `min_overlap` development sessions.
- **Causal exits.** A position still open on a day with no bar at or after `flat_at` (and not stopped or targeted out) is `unresolved`, with no exit price. One unresolved trade in a card's development sessions, or in a 5d neighbour's, makes the card's verdict `unresolved`, reported with the count and dates; it is never a survivor. In the holdout it spends the look and fails it. Entries read only the bars up to the entry bar.
- **Splits pinned by date.** Each `data` entry carries `split: {dev_end, holdout_end}`. Development = sessions ≤ dev_end; holdout = dev_end < sessions ≤ holdout_end; later sessions are in no gate and not in the holdout. Both ends must be session dates of the loaded export.
- **Frozen calendar.** `calendar: {path, sha256}` names the admitted `ops/calendars/cme_holiday_calendar_2022_2026.json` (sha256 `2698f2688cce582b08df58516fd770fa4a71a18de04870d9c14511731ea181e9` at admission). The engine reads only `schema` (must be `cme_holiday_calendar/v1`), `coverage_start`, `coverage_end` and every `entries[].date` (any status). A session on an entry date is not traded (skip reason `calendar_exception`) but stays a session for the split and the daily series, at zero P&L. Every development and holdout session must lie in the coverage window. The file keys closures to the CME trade date; for the day session the engine reads (session open to 17:00 ET) the wall-clock date is that trade date.
- **Search-wide K.** `k_scope: instrument` counts the instrument's distinct ledgered cards for 5f; `k_scope: ledger` counts every instrument's. Reports carry `k` and `k_scope`.
- **Holdout runner.** Refuses unless `out/verdict.json` lists every run.yaml card and each report is final for this run_id with the card hash and split run.yaml gives now. Survivors are the `survivor` reports; each look is ledgered before its holdout bars are simulated.
- **5e wording.** The timing placebo is reported as `placebo_rank (descriptive; timing shuffle with realised side and hold)`; its maths and threshold are unchanged.
- **Thresholds.** They change only by PR with Joshua's approval, and a pre-registration freezes them before any card runs.
- **Costs.** Commission comes from `FIRM_RULES` through `discovery.cost_model.resolve_commission`. An explicit `commission_per_side` is accepted only for an instrument without a firm row, must be positive, and is cited in the pre-registration. Every result carries a slippage of 1 tick per side.
- **The book's per-session Sharpe** with the card added is reported for every card. It is a description, not a gate.

Real ledgers, data, run files and reports are private. Keep them outside the repo, for example in `local_artifacts/strategy-builder-2026-10/`.
