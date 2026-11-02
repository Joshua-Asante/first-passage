# `lab/builder/`: strategy builder v1 engine

Build steps 1–3 of Joshua's "Strategy builder v1 spec" (2026-10-30): the trial ledger, the ORB block library and compiler (backtest side), and gates 5a–5g with a traceable report, run locally, plus the gate 5h venue MC as a standalone module, not yet wired into `gates.py` or `run.py`. Azure wiring, the Pine/NinjaScript compilers and the decay monitor are later build steps.

| Module | Job |
|---|---|
| `cards.py` | YAML card schema; library blocks only; timing checked against the instrument's session; canonical card hash; grid neighbours for the plateau gate |
| `ledger.py` | Append-only, hash-chained JSONL, verified in full on every read. K = distinct ledgered cards, per instrument or across the ledger (`k_scope`); holdout looks are their own entries, one per card |
| `instruments.py` | Day-session opens and the 17:00 ET day end; geometry from `core/instrument_specs` |
| `data.py` | The engine's own strict BAR EXPORT v0.2 reader (no shared lenient parser, no derived panels); the book file; the frozen calendar; the date-pinned split |
| `compile.py` | Card → trades on closed 15m bars, with the conservative fill rules in its docstring; skipped days counted by reason; no exit price without a bar at or after `flat_at` |
| `gates.py` | 5a–5g in order, stopping at the first fail; `THRESHOLDS` holds the spec defaults; verdict `survivor`, `killed` or `unresolved`; stage 8 holdout look |
| `venue.py` | Gate 5h: venue MC of the book plus at most one candidate at two eval configs; see below |
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
- **Holdout runner.** `run.binding` is every development input in canonical form: run.yaml's fields with each file reduced to its pinned sha256 (paths and `out` excluded), the card hashes, the resolved per-instrument costs and the engine sha256. `verdict.json` carries it and its sha256 with each report's sha256; it is deleted before a run ledgers and written last by an atomic rename. Every report carries the binding sha256. The holdout refuses, before any look, unless the current run.yaml recomputes to that sha256 (naming the changed fields), every listed report matches its sha256 and is final for this run_id. Survivors are the `survivor` reports; each look is ledgered before its holdout bars are simulated.
- **5e wording.** The timing placebo is reported as `placebo_rank (descriptive; timing shuffle with realised side and hold)`; its maths and threshold are unchanged.
- **Thresholds.** They change only by PR with Joshua's approval, and a pre-registration freezes them before any card runs.
- **Costs.** Commission comes from `FIRM_RULES` through `discovery.cost_model.resolve_commission`. An explicit `commission_per_side` is accepted only for an instrument without a firm row, must be positive, and is cited in the pre-registration. Every result carries a slippage of 1 tick per side.
- **The book's per-session Sharpe** with the card added is reported for every card. It is a description, not a gate.

Real ledgers, data, run files and reports are private. Keep them outside the repo, for example in `local_artifacts/strategy-builder-2026-10/`.

## Gate 5h: venue MC (`venue.py`)

Settings are pinned by the research coordinator's ticket (2026-11-01) and live as module constants:
`Tradeify_Select_100K` (consistency 0.40) and `MFFU_Rapid_100K` (0.50) through `mc.preflight.firm_kwargs` with inactivity on, a $100,000 fresh account, fixed size and no protection (`dd_trigger=10.0`, `dd_scale=1.0`), seeds 20261101-20261110 at 1,000 paths each. The panel is every weekday in the window shared by the book and the candidate, zero where a leg has no session, cut to complete Mon-Fri weeks. The book is used as given; the candidate's per-trade points are priced per config like gate 5b (firm commission + 1 tick per side). Every run, book alone and book plus candidate, carries a **preservation leg**: minus one micro MNQ round trip at the config's costs on the first weekday (Monday) of each complete week, standing in for the operator's weekly preservation trade, so that day is active. `gating_bust` = headline bust + inactivity bust; horizon-cap paths are reported, not counted.

The gate is relative (thresholds approved by Joshua 2026-11-01). Book alone and book plus candidate run on the same seeds and weeks, so each path draws the same weeks in both (common random numbers). A candidate passes when, in both configs, `gating_bust` rises by at most `VENUE_THRESHOLDS["5h_max_bust_increase"]` (0.01) and P(pass) falls by at most `VENUE_THRESHOLDS["5h_max_pass_decrease"]` (0.01). `book_bust_target` (0.05) is reported as `book_target_met` for the book alone and with the candidate; it never gates a candidate. A book-alone run's verdict is `baseline`. A config the preflight or the cost table refuses gives `refused`. P(payout) is not encoded. Every result is an end-of-day research screen: venues enforce drawdown intraday and this panel has no intraday path.

Book alone: `python -m builder.venue --book <json> --sha256 <hex> --out <json>` (with `lab` and `core` on the path). Results are private, like every other builder output.
