# G1 Operator gate — Q-HARV-0

**Date:** 2026-07-11  
**Authority:** Operator implement instruction on the ratified multitask plan (plan attach + “Implement the plan… Don’t stop until you have completed all the to-dos”).

## §0.5 answers (binding for this run)

| # | Ambiguity | Decision |
|---|---|---|
| 1 | Micro-era OOS wording | **§4 P-micro-OOS only:** same-signed native-MES conditional effect vs parent. Full SPA/DSR/PBO ladder is out of scope for HARV-0 (DISC-CAMP territory). |
| 2 | Envelope 16:00 ET / 40% | **Accepted as PROVISIONAL annotation frame** for `DEPLOYABLE-DEFAULT-ENVELOPE`. Clock-print contradiction vs repo 17:00 ET MC harnesses logged in ENVELOPE_RECONCILE.md; does not block research H1. |
| 3 | CME holiday calendar | **pandas `CustomBusinessDay` with CME Globex equity-index holidays** pinned in `NOTES.md` / `step0_checks.py` (NYSE holidays as proxy for equity-index futures trading days is insufficient — use exchange calendar where available; else CME equity-index session holidays from a pinned list). Executor: prefer `exchange_calendars` `CMES` if installed in research venv; else hard-coded CME holiday set + weekday mask, documented in NOTES. |
| 4 | ohlcv-1d close print | **Deferred to Wave 1 definition/docs confirmation** before C/G; do not assume. |

## §4 / §6 ratification

Frozen operationalization (T-3→T-1, T-4 cutoff, 100bp, bundled P-*, C/G annotation, §6 verdict partition) **RATIFIED** unchanged. No parameter edits.

## Envelope

`ops/prop_envelope_default.md` v0.1 accepted as **PROVISIONAL** deployment frame. ADR to v1.0 deferred (envelope §5 open items stand).

## Registration stamp

- `registration.date`: 2026-07-11
- `run_id`: `harv2026_001_es_monthend`
- `K`: 1
