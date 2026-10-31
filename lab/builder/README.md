# `lab/builder/`: strategy builder v1 engine

Build steps 1–3 of Joshua's "Strategy builder v1 spec" (2026-10-30): the trial ledger, the ORB block library and compiler (backtest side), and gates 5a–5g with a traceable report, run locally. Venue MC (5h), Azure wiring, the Pine/NinjaScript compilers and the decay monitor are later build steps.

| Module | Job |
|---|---|
| `cards.py` | YAML card schema; library blocks only; timing checked against the instrument's session; canonical card hash; grid neighbours for the plateau gate |
| `ledger.py` | Append-only, hash-chained JSONL, verified in full on every read. K per instrument = distinct ledgered cards; holdout looks are their own entries, one per card |
| `instruments.py` | Day-session opens and the 17:00 ET day end; geometry from `core/instrument_specs` |
| `data.py` | The engine's own strict BAR EXPORT v0.2 reader (no shared lenient parser, no derived panels); the book file; development is the first 70% of sessions, holdout the last 30% |
| `compile.py` | Card → trades on closed 15m bars, with the conservative fill rules in its docstring; skipped days counted by reason |
| `gates.py` | 5a–5g in order, stopping at the first fail; `THRESHOLDS` holds the spec defaults; stage 8 holdout look |
| `run.py` | `python -m builder.run run.yaml`: validate the spec, ledger every card, load pinned data, evaluate, write `report.json` per card |

Rules the engine enforces:
- **Inputs fail closed.** Every input the engine reads has a stated condition, and a load that breaks one aborts the run before any gate result exists. The invariant table is in the PR that introduced this rebuild, and each row has a test in `tests/lab/test_builder/`. Nothing degrades to a skip, a default or a warning. The one deliberate exception is a day the compiler can't trade, and it is counted in `report.skipped_days`.
- **Ledger first.** A card is appended before any bar is read, and the engine refuses a card that isn't in the ledger.
- **Pinned inputs.** run.yaml pins the sha256 of every data file and of the book. A supplied book must cover `min_overlap` development sessions.
- **Thresholds.** They change only by PR with Joshua's approval, and a pre-registration freezes them before any card runs.
- **Costs.** Commission comes from `FIRM_RULES` through `discovery.cost_model.resolve_commission`. An explicit `commission_per_side` is accepted only for an instrument without a firm row, must be positive, and is cited in the pre-registration. Every result carries a slippage of 1 tick per side.
- **The book's per-session Sharpe** with the card added is reported for every card. It is a description, not a gate.

Real ledgers, data, run files and reports are private. Keep them outside the repo, for example in `local_artifacts/strategy-builder-2026-10/`.
