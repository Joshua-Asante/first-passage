# Q-SFCLEAR-2 — personal clearance of the Tradeify book at R1

**Status:** ACTIVE — successor pre-registration DRAFT, not ratified; calendar-only historical schedule committed; no scoring output
**In-flight:** yes

Owner: [Q-SFCLEAR-2 brief](../../../../docs/briefs/Q-SFCLEAR-2-personal-clearance-tradeify-book.md).
Contract: [Q-SFCLEAR-2 pre-registration](../../../../docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md).

- `schedule/` — calendar-only inputs, committed before the freeze. `historical_schedule_2022-09-01_2026-09-02.json`
  (sha256 `ab44fada0c059c0d286798239a87c82331d8500ef075bf4cb1180ed552d5d473`) is written by
  [`build_historical_schedule.py`](build_historical_schedule.py); `--check` regenerates and compares.
- `run_records/` — one public record per scoring run (`run_head`, `started_utc`, `private_sha256sums_sha256`),
  committed after the freeze (pre-registration §7, §10 hook 4). Outputs stay under the private root
  `C:\Users\joshu\t00-step3-console\sfclear2-run-<UTC>\`, never in the repo.
