# Q-SFCLEAR-3 — personal clearance of the Tradeify book at R1

**Status:** ACTIVE — Q-SFCLEAR-3 pre-registration FROZEN 2026-10-14, superseding Q-SFCLEAR-2 before run; no scoring output
**In-flight:** yes

Owner: [Q-SFCLEAR-2 brief](../../../../docs/briefs/Q-SFCLEAR-2-personal-clearance-tradeify-book.md) (parent brief of Q-SFCLEAR-3).
Contract: [Q-SFCLEAR-3 pre-registration](../../../../docs/briefs/pre-registration/Q-SFCLEAR-3-verdict-preregistration.md), incorporating the [Q-SFCLEAR-2 pre-registration](../../../../docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md) at F `83867f0` except where its §S changes it.

- `schedule/` — calendar-only inputs, committed before the freeze. `historical_schedule_2022-09-01_2026-09-02.json`
  (sha256 `ab44fada0c059c0d286798239a87c82331d8500ef075bf4cb1180ed552d5d473`) is written by
  [`build_historical_schedule.py`](build_historical_schedule.py); `--check` regenerates and compares.
- `run_records/` — one public record per scoring run (`run_head`, `started_utc`, `private_sha256sums_sha256`),
  committed after F₃ and descending from it (Q-SFCLEAR-3 §S row 8, §10 hook 4). Outputs stay under the private root
  `C:\Users\joshu\t00-step3-console\sfclear2-run-<UTC>\`, never in the repo.
