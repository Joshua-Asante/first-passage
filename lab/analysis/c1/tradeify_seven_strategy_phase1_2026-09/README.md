# Tradeify five-active-source Phase 1 normalization

**Theme:** c1

**In-flight:** yes

**Status:** ACTIVE — strict five-source Tradeify source, accounting, deadline, cap, and provenance normalization

Strict, deterministic `EXPLORATORY` normalization of five retained Tradeify Select TradingView export/Pine pairs, with source identity, accounting, fee, daily force-flat, micro-equivalent cap, and continuous-contract provenance checks. Two historical swap-port exports remain provenance-only dropped inventory records.

Phase 0 was skipped by operator direction. All supplied history is development data: no result here is untouched, out-of-sample, confirmatory, qualified, admitted, or deployable. Phase 1 does not rank, compare, compose, bootstrap, run Monte Carlo, or rerun Pine.

## Source and output ownership

D26 migration is pending: the checked-in config, manifest and RESULTS remain historical
v3 artifacts, byte-for-byte unchanged. The v4 runner requires a non-null
`pine_input_overrides_sha256` (exactly 64 lowercase hexadecimal characters) for every
active source; the historical config intentionally cannot run under this schema.
Five full current private input captures are required before digest population and
a single re-freeze of the campaign artifacts. No synthetic digest may stand in for
that evidence. Raw input override maps remain private; only their digests propagate
into new source identities and reports. Historical v3 manifests remain renderable.

Store D26 override maps and their capture evidence under this study's
`inputs/private_overrides/` directory. The entire directory is gitignored,
including JSON, images, text and nested files. Hash the exact private artifact
bytes; publish only that digest. Never force-add these private artifacts.
The runner requires `inputs/private_overrides/<strategy_id>.json` for each
active source, relative to the config directory. It hashes the exact bytes
without decoding or parsing them. Missing, unreadable or mismatched evidence
is a fatal intake failure (exit 3), before any output publication. Only the
verified digest is serialized; no artifact contents are included in diagnostics.

Prospective v4 D27 summary anchors use `tv_panel_max_drawdown_usd`, separate
from both computed measures on every leg, including the five-scalar D17 branch
and the seven-metric non-D17 branch. Both retired anchor names,
`max_drawdown_usd` and `max_drawdown_excursion_bounded_usd`, are rejected.
Accounting retains that closed-trade measure separately as
`LOWER BOUND for non-overlapping trades`. Under overlap, a realized loss can
coincide with an unrealized gain, so closed-trade drawdown can overstate the
true account drawdown. The new measure is labeled
`LOWER BOUND (excursion-tightened) for non-overlapping trades` and uses Decimal arithmetic in an exit-order
walk: sort by exit timestamp then source row, visit realized equity minus the
absolute trade MAE before settlement, and retain both this decline and the
realized exit decline from the realized-equity peak. Missing/non-finite MAE is
rejected. The walk never visits an intratrade peak (MFE), so it misses drawdowns
starting there even without overlap: `closed <= walk <= true`, never equality
with the full path. Under overlap neither computed field bounds synchronized
account-equity drawdown; trade extrema do not identify their relative timing.
Both computed measures, the separate panel anchor, labels and limitations are
included side by side in newly generated reports.

Overlap is measured per leg from canonical entry/exit timestamps, never Pine
pyramiding. Closed intervals apply: an entry at another trade's exit time is a
tie and takes the overlap branch. With no overlap, only `walk > panel + 0.01`
blocks; the cent tolerance is inclusive. A smaller walk creates no finding;
equality is coincident INFO, never MATCH. With overlap or a tie the panel is
RECORDED and the walk-versus-panel difference is INFO, never BLOCKER or MATCH.
The summary row leaves `observed` unset and records the walk separately;
its difference is explicitly walk minus panel, not a panel reconciliation.

D17 monthly/commission policy is unchanged. The new exact-key `max_drawdown`
policy slot must be `null` while D32 is unruled; no accepted value is invented.
Reports carry `PENDING_D32`; complete evidence coverage is not operator
acceptance. The historical policy has no new slot and intentionally fails
the prospective loader. Current private captures
and independent panel population still gate regeneration; no campaign evidence
prerequisite is closed by this code change.

The ten active source files are provided only through `--source-dir`; their basenames, SHA-256 pins, and byte lengths are frozen in `phase1_config.json`. The vendor bytes are never copied into this repository. Canonical event, trade, and weekly ledgers are vendor-derived and deliberately written only to the campaign's ignored `local_artifacts/` directory. Committed `reconciliation_manifest.json` and `RESULTS.md` contain aggregate values and hashes, never an absolute source path or full row-level ledger. Every canonical event additionally carries `source_row_sha256`, the SHA-256 of its exact raw CSV record bytes, including its original terminator where present.

`source_timezone` is `America/New_York` for all five active inputs. Normalization uses `zoneinfo`, emits UTC timestamps and exchange-session dates, and rejects ambiguous or nonexistent DST wall times instead of guessing. Test commands and counts are frozen separately in `VERIFICATION.md`, which the campaign runner does not overwrite.

## Active and dropped identity inventory

The retained inventory is exactly `aegis_6j1`, `orb_mnq_recon_v7`, `striker_dj30_mym_pyramid_250`, `striker_nas100_mnq_dow_wed_excluded`, and `vanguard_mgc_v04`, in that order. The five 2026-09-03 venue-bound source pairs are frozen by filename, byte count and SHA-256 in config. Aegis, ORB, and Vanguard are `NOT_IN_PORT_MANIFEST`. DJ and NAS are hash-frozen 100K `UNPINNED_MODIFIED` bodies that cite the existing candidate pins only as ancestors: their divergence preserves respectively `pyramid 250% vs locked 750%` and `day-of-week set {Mon,Tue,Thu,Fri} vs locked {Mon,Tue}`, plus `initial_capital 100000 vs research-variant pin 200000`. Neither is the locked edition.

The two dropped records, `striker_dj30_qtxg1_swap_body_on_mym` and `striker_nas100_qtxg1_swap_body_on_mnq`, are unusable swap-port exports: point-value sizing was not overridden (a 4× mismatch interacting with cap and pyramid), cannot be rescaled, and will never be repaired. They appear only in the aggregate provenance inventory with their archive pin refs, filenames, and hashes; they are never normalized, counted, or included in ledgers, weekly results, ranking, or composition.

The loader parses the actual repository `PORT_MANIFEST.sha256` once per inventory load. Every active pinned and dropped ref must name an existing safe repo-relative entry with the same Pine basename and SHA-256. Directory placement is owned by that manifest, not a hardcoded `candidates/` prefix. Malformed, duplicate, dangling and mismatched entries fail closed. An `UNPINNED_MODIFIED` compatibility record must reference a real ancestor pin, without claiming its modified body's hash matches that ancestor. Private Pine bodies need not exist inside the repository.

## D13 continuous-contract disposition

Operator ruling 2026-09-03; `docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md` §6 D13(b): continuous basis is `ACCEPTED_UNMODELED` for Phases 2–4, not modeled or resolved. The exact config object `continuous_contract_roll_policy` freezes disposition, ruling date/reference and both obligations below. It flows explicitly into venue analysis and every manifest/strategy/detail/report; generic callers without a policy still receive the unresolved roll blocker. This campaign retains `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` as a WARNING limitation. Contract-month and seam attribution remain `UNAVAILABLE`; other blockers and the calendar/summary `NEEDS_CONTEXT` cap are unaffected.

- Phase 3 pre-registration states back-adjustment seam risk as a limitation of every campaign claim: fills cannot be attributed to a contract month, and a seam crossing is indistinguishable from a price move.
- A Phase 6 seam-sensitivity check is pre-registered with its severity frozen alongside the other Phase 6 cutoffs.

Generation `tradeify-phase1-normalization-v3` identifies the manifest/report contract. Config, calendar, fee schedule and independent summaries carry hashes from their exact parsed byte snapshots; a later filesystem change cannot silently replace a snapshot digest. This does not establish missing evidence or satisfy either future D13 obligation.

## Venue boundaries

The frozen upper-bound implementation is the reviewed `80abcec` behavior; the final replacement bytes measure peak micro-equivalent ranges of `80/80`, `4/6`, `77/77`, `77/77`, and `6/6` in configuration order. These are per-strategy observations only: no Phase 1 book-level cap verdict is claimed.

The per-strategy Tradeify cap remains a Phase 1 blocker check against 80 micro-equivalents (`6J=10`, `MNQ/MYM/MGC=1` per contract). The joint ledger carries that unit on every event, but the joint book-cap verdict is deferred to Phase 4.

Force-flat auditing checks whether a daily Tradeify deadline instant lies in `(entry, exit]`: 16:45 America/New_York on regular days and 12:59 on the D19-accepted 40-date secondary venue-date calendar within 2022-09-01 through 2026-09-02 (the source inventory has 49 dates overall). The final 40-date replacement generation is frozen in `reconciliation_manifest.json` and `RESULTS.md`. D19 does not upgrade this source to primary evidence or model product close times/exchange sessions; its accepted and unresolved residuals remain in `RESULTS.md`. The verdict cap remains `NEEDS_CONTEXT` because fresh independent scalar panels are missing (including DJ30's unexplained +$287 replacement-run delta), not because the D19 calendar is incomplete.

## Evidence inputs and independent summary checks

The primary calendar capture schema remains available for future reviewed yearly extracts, but the checked-in D19 wrapper spans 2022-09-01 through 2026-09-02 and binds exactly 40 account-level `EARLY_CLOSE` venue dates from the source's 49-date inventory. Its source-calendar SHA-256 is `2698f2688cce582b08df58516fd770fa4a71a18de04870d9c14511731ea181e9` on the LF-pinned Git blob; no full-closure date is converted to a short-session deadline.

The only secondary compatibility path is the separately tagged `tradeify_secondary_early_close/v1` wrapper. It pins the exact LF bytes of in-repository `ops/calendars/cme_holiday_calendar_2022_2026.json` and uses only the 40 dates from its declared 49-date account-level `EARLY_CLOSE` union that fall in the declared window as 12:59 ET rows; a product group (including 6J) marked `NORMAL` does not remove that blanket Tradeify deadline. D19 accepts this venue-date membership evidence as `COMPLETE`, not as primary evidence or product-close/exchange-session modeling. CME-trade-date full-closure dates are never converted to wall-date deadlines; the three sub-deadline notes, thirteen unresolved items, 2025-11-28 conservative scheduled-half-day/outage classification, and possible non-conservative missing ad-hoc closures from 2026-05-28 through 2026-09-02 remain explicit limitations.

`tv_summary_anchors.json` is the current empty replacement-panel inventory: its `strategies` array is `[]`, so all five replacement sources remain `MISSING_ANCHOR` and G1.4 remains `NEEDS_CONTEXT`. Its optional `d17_policy` has exactly `{ruling_date, ruling_ref, monthly_totals, commissions, reason}`; with that policy present, any future active, hash-bound strategy anchor has exact `{strategy_id, export_sha256, source_note, metrics, missing_metrics}` keys and exactly five scalar metrics: trade count, net P&L USD, win-rate percent, profit factor, and max drawdown USD. Count is an integer; decimals are finite strings; `missing_metrics` lists absent metrics with null values, distinct from semantically undefined null factor/zero-trade win rate. The generic branch without `d17_policy` has the legacy seven-metric schema, including total commissions and a monthly net-P&L map; it does not describe the current replacement inventory.

D17 does not rebind old panels to replacement hashes. It retains the five independent scalar Key-stats requirements above while reconstructing monthly totals from canonical row-ledger trades by `exit_timestamp_naive` in the configured source timezone, with exact Decimal cross-checks; per-month figures exist only in gitignored local monthly-reconciliation artifacts. Commission evidence is `AMENDED_OUT` as an independent dimension: derived commission remains inventory, while venue/export fee auditing is unchanged. The runner publishes only hashes, bucket counts, basis, status and residual summaries in tracked results.

## Joint-ledger scope

Phase 1 delivers deterministic joint event union and ISO-week exit aggregation only; neither is a joint-flat block builder. The joint-flat block builder is deferred to Phase 3, before Phase 4 composition, because it requires a synchronized all-leg chronology and must prove every included leg is flat at each block edge. The final replacement source has zero Friday-to-Sunday holds; no Phase 1 ranking, dependence, composition, Monte Carlo, or Pine rerun occurs.

## Reproduce

```powershell
.venv/Scripts/python.exe lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/run_phase1.py `
  --config lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json `
  --source-dir 'C:\path\to\the\ten\active\frozen\files' `
  --output-dir lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/remediation_40_dates_2026-09-03
```

The aggregate report remains `EXPLORATORY` even when all byte and accounting checks reproduce exactly. Re-running Pine needs a separate, explicitly authorized bar-data and execution-engine project.
