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

The source-grounded inventory has five entry/exit templates represented by seven exports. `core/strategies/PORT_MANIFEST.sha256` is authoritative for pin membership. `striker_dj30_native_pyramid_down_on_mym` is a provisional D10 name for the unpinned DJ30 modified body at 250%, versus 750% in the pinned swap prototype `striker_dj30_qtxg1_swap_body_on_mym`; both that ID and the two `*_swap_body_*` IDs remain provisional pending the remaining D10 naming answers. `striker_nas100_mnq_dow_wed_excluded` is an unpinned parameter cell of the NAS100 template with day-of-week set `{Mon,Tue,Thu,Fri}` versus the locked `{Mon,Tue}` set; it is never the locked edition and remains at pyramid 1000%. The swap-body sources are literal `EXPLORATORY` chart runs only: neither is locked/native-edition evidence or proof of correct swap-port point-value overrides. The source basenames and bytes are unchanged even where their historical filenames contain obsolete instrument or Q-TXG-1 labels.

## Venue boundaries

The per-strategy Tradeify cap remains a Phase 1 blocker check against 80 micro-equivalents (`6J=10`, `MNQ/MYM/MGC=1` per contract). The joint ledger carries that unit on every event, but the joint book-cap verdict is deferred to Phase 4.

Force-flat auditing checks whether a daily Tradeify deadline instant lies in `(entry, exit]`: 16:45 America/New_York on regular days and 12:59 on CME early-close dates. The primary CME page did not expose a complete 2022-09-01 through 2026-09-01 historical calendar, and the CME Reference Data API requires an OAuth API ID. `cme_early_close_calendar.json` therefore freezes the gap as `NEEDS_CONTEXT`; it contains no inferred holiday dates. Regular 16:45 checks still run, while every aggregate report preserves the holiday-short verdict cap.

## Joint-ledger scope

Phase 1 delivers deterministic joint event union and ISO-week exit aggregation only; neither is a joint-flat block builder. The joint-flat block builder is deferred to Phase 3, before Phase 4 composition, because it requires a synchronized all-leg chronology and must prove every included leg is flat at each block edge. ORB-MNQ's three Friday-to-Sunday holds make the affected weekly edges fail that assertion; they are reported and never repaired. No Phase 1 ranking, dependence, composition, Monte Carlo, or Pine rerun occurs.

## Reproduce

```powershell
python lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/run_phase1.py `
  --config lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json `
  --source-dir 'C:\path\to\the\fourteen\frozen\files' `
  --output-dir lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts
```

The aggregate report remains `EXPLORATORY` even when all byte and accounting checks reproduce exactly. Re-running Pine needs a separate, explicitly authorized bar-data and execution-engine project.
