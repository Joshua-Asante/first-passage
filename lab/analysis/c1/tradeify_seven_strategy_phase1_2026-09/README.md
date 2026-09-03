# Tradeify seven-strategy Phase 1 normalization

**Theme:** c1

**In-flight:** yes

**Status:** ACTIVE — strict seven-strategy Tradeify source, accounting, deadline, cap, and provenance normalization

Strict, deterministic `EXPLORATORY` normalization of the seven supplied Tradeify Select TradingView export/Pine pairs, with source identity, accounting, fee, daily force-flat, micro-equivalent cap, and continuous-contract provenance checks.

Phase 0 was skipped by operator direction. All supplied history is development data: no result here is untouched, out-of-sample, confirmatory, qualified, admitted, or deployable. Phase 1 does not rank, compare, compose, bootstrap, run Monte Carlo, or rerun Pine.

## Source and output ownership

The fourteen source files are provided only through `--source-dir`; their basenames and SHA-256 pins are frozen in `phase1_config.json`. The vendor bytes are never copied into this repository. Canonical event, trade, and weekly ledgers are vendor-derived and deliberately written only to the campaign's ignored `local_artifacts/` directory. Committed `reconciliation_manifest.json` and `RESULTS.md` contain aggregate values and hashes, never an absolute source path or full row-level ledger.

`source_timezone` is `America/New_York` for all seven inputs. Normalization uses `zoneinfo`, emits UTC timestamps and exchange-session dates, and rejects ambiguous or nonexistent DST wall times instead of guessing. Test commands and counts are frozen separately in `VERIFICATION.md`, which the campaign runner does not overwrite.

## Strategy lineage and pyramid inventory

The source-grounded inventory has five entry/exit templates represented by seven exports. Exactly one export is a reduced-pyramid parameterization: `striker_dj30_mym_pyramid_down` uses the Pine's 250% setting versus 750% in `striker_dj30_mym_v45`. Both NAS100 Pines specify 1000%, so `striker_nas100_mnq_native_variant` is a distinct frozen source lineage, not a pyramid-down cell. The source basenames and bytes are unchanged even where their historical filenames contain obsolete instrument or Q-TXG-1 labels.

## Venue boundaries

The per-strategy Tradeify cap remains a Phase 1 blocker check against 80 micro-equivalents (`6J=10`, `MNQ/MYM/MGC=1` per contract). The joint ledger carries that unit on every event, but the joint book-cap verdict is deferred to Phase 4.

Force-flat auditing checks whether a daily Tradeify deadline instant lies in `(entry, exit]`: 16:45 America/New_York on regular days and 12:59 on CME early-close dates. The primary CME page did not expose a complete 2022-09-01 through 2026-09-01 historical calendar, and the CME Reference Data API requires an OAuth API ID. `cme_early_close_calendar.json` therefore freezes the gap as `NEEDS_CONTEXT`; it contains no inferred holiday dates. Regular 16:45 checks still run, while every aggregate report preserves the holiday-short verdict cap.

## Reproduce

```powershell
python lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/run_phase1.py `
  --config lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json `
  --source-dir 'C:\path\to\the\fourteen\frozen\files' `
  --output-dir lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts
```

The aggregate report remains `EXPLORATORY` even when all byte and accounting checks reproduce exactly. Re-running Pine needs a separate, explicitly authorized bar-data and execution-engine project.
