# Tradeify five-active-source Phase 1 normalization

**Theme:** c1

**In-flight:** yes

**Status:** ACTIVE — strict five-source Tradeify source, accounting, deadline, cap, and provenance normalization

Strict, deterministic `EXPLORATORY` normalization of five retained Tradeify Select TradingView export/Pine pairs, with source identity, accounting, fee, daily force-flat, micro-equivalent cap, and continuous-contract provenance checks. Two historical swap-port exports remain provenance-only dropped inventory records.

Phase 0 was skipped by operator direction. All supplied history is development data: no result here is untouched, out-of-sample, confirmatory, qualified, admitted, or deployable. Phase 1 does not rank, compare, compose, bootstrap, run Monte Carlo, or rerun Pine.

## Source and output ownership

The ten active source files are provided only through `--source-dir`; their basenames, SHA-256 pins, and byte lengths are frozen in `phase1_config.json`. The vendor bytes are never copied into this repository. Canonical event, trade, and weekly ledgers are vendor-derived and deliberately written only to the campaign's ignored `local_artifacts/` directory. Committed `reconciliation_manifest.json` and `RESULTS.md` contain aggregate values and hashes, never an absolute source path or full row-level ledger. Every canonical event additionally carries `source_row_sha256`, the SHA-256 of its exact raw CSV record bytes, including its original terminator where present.

`source_timezone` is `America/New_York` for all five active inputs. Normalization uses `zoneinfo`, emits UTC timestamps and exchange-session dates, and rejects ambiguous or nonexistent DST wall times instead of guessing. Test commands and counts are frozen separately in `VERIFICATION.md`, which the campaign runner does not overwrite.

## Active and dropped identity inventory

The retained inventory is exactly `aegis_6j1`, `orb_mnq_recon_v7`, `striker_dj30_mym_pyramid_250`, `striker_nas100_mnq_dow_wed_excluded`, and `vanguard_mgc_v04`, in that order. `PORT_MANIFEST.sha256` is authoritative for pin membership. The DJ body is `PINNED_RESEARCH_VARIANT` at `pyramid 250% vs locked 750%`: a pyramid cell of the DJ30 template, never the locked edition. The NAS body is `PINNED_RESEARCH_VARIANT` at `day-of-week set {Mon,Tue,Thu,Fri} vs locked {Mon,Tue}`: a DOW cell of the NAS100 template, never the locked edition, with pyramid still 1000%. Their candidate pin refs and hashes are frozen in config.

The two dropped records, `striker_dj30_qtxg1_swap_body_on_mym` and `striker_nas100_qtxg1_swap_body_on_mnq`, are unusable swap-port exports: point-value sizing was not overridden (a 4× mismatch interacting with cap and pyramid), cannot be rescaled, and will never be repaired. They appear only in the aggregate provenance inventory with their archive pin refs, filenames, and hashes; they are never normalized, counted, or included in ledgers, weekly results, ranking, or composition.

## Venue boundaries

The per-strategy Tradeify cap remains a Phase 1 blocker check against 80 micro-equivalents (`6J=10`, `MNQ/MYM/MGC=1` per contract). The joint ledger carries that unit on every event, but the joint book-cap verdict is deferred to Phase 4.

Force-flat auditing checks whether a daily Tradeify deadline instant lies in `(entry, exit]`: 16:45 America/New_York on regular days and 12:59 on CME early-close dates. The primary CME page did not expose a complete 2022-09-01 through 2026-09-01 historical calendar, and the CME Reference Data API requires an OAuth API ID. `cme_early_close_calendar.json` therefore freezes the gap as `NEEDS_CONTEXT`; it contains no inferred holiday dates. Regular 16:45 checks still run, while every aggregate report preserves the holiday-short verdict cap.

## Joint-ledger scope

Phase 1 delivers deterministic joint event union and ISO-week exit aggregation only; neither is a joint-flat block builder. The joint-flat block builder is deferred to Phase 3, before Phase 4 composition, because it requires a synchronized all-leg chronology and must prove every included leg is flat at each block edge. ORB-MNQ's three Friday-to-Sunday holds make the affected weekly edges fail that assertion; they are reported and never repaired. No Phase 1 ranking, dependence, composition, Monte Carlo, or Pine rerun occurs.

## Reproduce

```powershell
python lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/run_phase1.py `
  --config lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json `
  --source-dir 'C:\path\to\the\ten\active\frozen\files' `
  --output-dir lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts
```

The aggregate report remains `EXPLORATORY` even when all byte and accounting checks reproduce exactly. Re-running Pine needs a separate, explicitly authorized bar-data and execution-engine project.
