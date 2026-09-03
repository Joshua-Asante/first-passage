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

The loader parses the actual repository `PORT_MANIFEST.sha256` once per inventory load. Every active pinned and dropped ref must name an existing safe repo-relative entry with the same Pine basename and SHA-256. Directory placement is owned by that manifest, not a hardcoded `candidates/` prefix. Malformed, duplicate, dangling and mismatched entries fail closed. An `UNPINNED_MODIFIED` compatibility record must reference a real ancestor pin, without claiming its modified body's hash matches that ancestor. Private Pine bodies need not exist inside the repository.

## D13 continuous-contract disposition

Operator ruling 2026-09-03; `docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md` §6 D13(b): continuous basis is `ACCEPTED_UNMODELED` for Phases 2–4, not modeled or resolved. The exact config object `continuous_contract_roll_policy` freezes disposition, ruling date/reference and both obligations below. It flows explicitly into venue analysis and every manifest/strategy/detail/report; generic callers without a policy still receive the unresolved roll blocker. This campaign retains `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` as a WARNING limitation. Contract-month and seam attribution remain `UNAVAILABLE`; other blockers and the calendar/summary `NEEDS_CONTEXT` cap are unaffected.

- Phase 3 pre-registration states back-adjustment seam risk as a limitation of every campaign claim: fills cannot be attributed to a contract month, and a seam crossing is indistinguishable from a price move.
- A Phase 6 seam-sensitivity check is pre-registered with its severity frozen alongside the other Phase 6 cutoffs.

Generation `tradeify-phase1-normalization-v2` identifies the manifest/report contract. Config, calendar, fee schedule and independent summaries carry hashes from their exact parsed byte snapshots; a later filesystem change cannot silently replace a snapshot digest. This does not establish missing evidence or satisfy either future D13 obligation.

## Venue boundaries

Known F1 contract limitation: the explicitly mandated same-timestamp batching (earlier exits → all entries → zero-duration exits) is retained pending the operator's correction decision. Its reported minimum is not a guaranteed global causal minimum when zero-duration and new lasting entries coincide. For example, prior 50 exits alongside a zero-duration 70 and a new lasting 60: batching reports 130, while a feasible own-entry-before-exit ordering reaches a minimum peak of 70. The five current sources have no such coincident zero-duration/new-entry groups; their peaks and cap classifications are unchanged. Publication remains `NEEDS_CONTEXT` on this unresolved contract; no generic bound-correctness or unconditional software-readiness claim is made.

The per-strategy Tradeify cap remains a Phase 1 blocker check against 80 micro-equivalents (`6J=10`, `MNQ/MYM/MGC=1` per contract). The joint ledger carries that unit on every event, but the joint book-cap verdict is deferred to Phase 4.

Force-flat auditing checks whether a daily Tradeify deadline instant lies in `(entry, exit]`: 16:45 America/New_York on regular days and 12:59 on CME early-close dates. The primary CME page did not expose a complete 2022-09-01 through 2026-09-02 historical calendar, and the CME Reference Data API requires an OAuth API ID. `cme_early_close_calendar.json` therefore freezes the gap as `NEEDS_CONTEXT`; it contains no inferred holiday dates. Regular 16:45 checks still run, while every aggregate report preserves the holiday-short verdict cap.

## Evidence inputs and independent summary checks

The historical calendar coverage target is 2022-09-01 through 2026-09-02. `cme_early_close_calendar.json` retains its exact compatibility metadata and adds `sources: []`; each future yearly source must provide exactly `{year, source_url, page_date, capture_basename, sha256}`, and every calendar row exactly `{date, deadline_local, source_year}`. A source must resolve to actual matching bytes in ignored `local_artifacts/calendar_captures`; a digest-shaped string alone cannot certify evidence. Symlink/traversal escapes, unknown years, duplicate dates/sources, changed bytes and missing covered years are rejected.

The supported capture format is a reviewed yearly primary-source JSON extract with exact `{year, source_url, page_date, rows}` keys and `{date, deadline_local}` rows. Metadata/year and all row years are checked, and the calendar must include precisely the captured rows within its coverage. Raw CME PDF/HTML requires a separately reviewed extraction step; no historical dates are reconstructed or guessed. No yearly extracts have been supplied, so the committed inventory remains empty and `NEEDS_CONTEXT`. Regular daily-deadline checks continue; structural validation does not establish missing historical truth.

The only secondary compatibility path is the separately tagged `tradeify_secondary_early_close/v1` wrapper. It pins the exact in-repository `ops/calendars/cme_holiday_calendar_2022_2026.json` bytes and accepts only its declared account-level union of `EARLY_CLOSE` dates as 12:59 ET rows; a product group (including 6J) marked `NORMAL` does not remove that blanket Tradeify deadline. This remains `NEEDS_CONTEXT` regardless of populated rows. Its CME-trade-date full-closure inventory is preserved only as provenance, never converted to wall-date deadline rows; its pre-12:59 closes, unresolved items, inert source URLs, and post-research revision pins remain explicit limitations in the manifest and report. The committed primary calendar is deliberately not populated from this secondary source while PR291 remains unmerged.

`tv_summary_anchors.json` holds independent operator TradingView Key-stats transcribed in campaign-state §10 at commit `716357e` (DEEP backtest, Default detail/4 OHLC ticks; panel span 2022-09-01 through 2026-09-02), bound to the five active export hashes. Initial capital is recorded in source notes without rescaling. Exact strategy keys are `{strategy_id, export_sha256, source_note, metrics, missing_metrics}`. Metrics are trade count, net P&L USD, win-rate percent, profit factor, max drawdown USD, total commissions USD and a monthly net-P&L USD map. Count is an integer; decimals are finite strings. `missing_metrics` lists absent metrics with null values, distinct from semantically undefined null factor/zero-trade win rate. Commissions and monthly operator anchors have not been supplied; G1.4 remains partial.

The runner emits per-strategy `MATCH`, `MISMATCH`, or `MISSING_ANCHOR` rows, including each month in the union (never silent zero-fill), to the manifest, RESULTS and local detail reports. Trade count is exact; currency and monthly comparisons allow inclusive $0.01, win-rate percent allows inclusive 0.01 percentage point, and profit factor allows inclusive 0.01. Available mismatches produce `TV_SUMMARY_MISMATCH` blockers without changing accounting; missing evidence never creates fabricated matches. Observed drawdown is closed-trade exit equity, not necessarily TradingView panel equity drawdown. The combined cap stays `NEEDS_CONTEXT` until both evidence inventories are complete, regardless of ordinary count/net acceptance checks. Parsed-byte calendar/anchor hashes and source notes are included in outputs.

## Joint-ledger scope

Phase 1 delivers deterministic joint event union and ISO-week exit aggregation only; neither is a joint-flat block builder. The joint-flat block builder is deferred to Phase 3, before Phase 4 composition, because it requires a synchronized all-leg chronology and must prove every included leg is flat at each block edge. ORB-MNQ's three Friday-to-Sunday holds make the affected weekly edges fail that assertion; they are reported and never repaired. No Phase 1 ranking, dependence, composition, Monte Carlo, or Pine rerun occurs.

## Reproduce

```powershell
.venv/Scripts/python.exe lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/run_phase1.py `
  --config lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json `
  --source-dir 'C:\path\to\the\ten\active\frozen\files' `
  --output-dir lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/reanchor_iteration3
```

The aggregate report remains `EXPLORATORY` even when all byte and accounting checks reproduce exactly. Re-running Pine needs a separate, explicitly authorized bar-data and execution-engine project.
