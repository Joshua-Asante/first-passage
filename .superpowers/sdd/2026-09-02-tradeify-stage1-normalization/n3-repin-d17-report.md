# N3 re-pin, D17, and D19 report

## Scope and source checks

- Bound the five approved 2026-09-03 CSV/Pine pairs in `phase1_config.json`; all ten `Downloads` bytes, lengths, and SHA-256 values were checked before binding. DJ30 and NAS100 are `UNPINNED_MODIFIED` with their existing candidate pins as ancestors and the required 100K divergence suffix.
- Added the single scoped LF attribute for `ops/calendars/cme_holiday_calendar_2022_2026.json`. Its checkout is now `i/lf w/lf`; `git hash-object --no-filters` is `6b489a87f6728af5c21c52c48b65bf4b3b5516d9`, equal to `HEAD:path`. The raw LF SHA-256 frozen by the wrapper is `2698f2688cce582b08df58516fd770fa4a71a18de04870d9c14511731ea181e9`. No semantic source-calendar edit was made.
- Populated the D19 wrapper with exactly the 49 `derived.venue_flat_dates`, never the 16 full-closure dates. It remains explicitly `SECONDARY`; D19 accepts venue-date membership only. The coverage note preserves the 2025-11-28 conservative classification and non-conservative possible missing ad-hoc closures from 2026-05-28 through 2026-09-02, while adapter metadata keeps the 13 unresolved and 3 sub-deadline inventories.

## TDD evidence

RED commands/results:

- `python -m pytest tests/test_tv_summary_reconciliation.py -k d17_policy ...` — failed because the old summary schema rejected `d17_policy`.
- `python -m pytest tests/test_tv_summary_reconciliation.py -k d17_ ...` — failed because `reconstruct_d17_monthly` did not exist.
- `python -m pytest tests/test_tradeify_phase1_evidence_integration.py -k d17_runner ...` — failed on runner v2/no local D17 monthly ledger contract.
- `python -m pytest tests/test_secondary_calendar_evidence.py -k 'd19_complete or complete_secondary' ...` — failed because COMPLETE secondary evidence was prohibited/no acceptance schema existed.
- `python -m pytest tests/test_secondary_calendar_evidence.py -k checked_in_d19 ...` — failed because the checked-in wrapper was not yet the D19 49-date wrapper.
- `python -m pytest tests/test_secondary_calendar_evidence.py -k runner_keeps_secondary ...` — failed because the renderer omitted D19 while showing SECONDARY evidence.

GREEN command/result:

- `python -m pytest tests/test_tv_trade_ledger.py tests/test_tv_summary_reconciliation.py tests/test_secondary_calendar_evidence.py tests/test_tradeify_phase1_evidence_integration.py -p no:cacheprovider --basetemp C:/Users/joshu/.codex/visualizations/2026/09/02/01a06481-886b-7123-ada1-6c5a02cbf4aa/n3-d17` — **134 passed**.

## Interfaces changed

- `tv_summary_anchors.json` optionally carries exact-key `d17_policy`; when present its anchors are scalar-only. Empty replacement panels remain five `MISSING_ANCHOR` requirements.
- D17 creates per-strategy, atomically published, gitignored `monthly_reconciliation/<id>.json` artifacts. Tracked manifest/detail/report data retain only hash, exit-month basis, bucket count, status, and aggregate residual; no per-month map or monthly comparison row is published. Commissions are explicitly `AMENDED_OUT` as independent evidence; derived commission remains inventory.
- Secondary calendar wrappers optionally carry the exact D19 acceptance. `COMPLETE` requires it and nonempty EARLY_CLOSE membership in every covered year; absent/invalid acceptance cannot complete. Renderer retains SECONDARY caveats under COMPLETE.
- Runner contract is v3.

## Deferred assertions and concerns

- No real campaign/output generation ran; N4 owns the one final re-freeze and all actual numeric results, `RESULTS.md`, `reconciliation_manifest.json`, `VERIFICATION.md`, local artifacts, and their hash-literal assertions.
- Existing generated-artifact regressions in `tests/test_tradeify_phase1_runner.py` remain unchanged and were deliberately not selected: `test_committed_manifest_matches_frozen_five_strategy_acceptance` and `test_committed_results_match_the_deterministic_renderer` still describe stale pre-freeze artifacts.
- Full-suite execution is deferred to the controller after N4. Focused tests cover source schema identity, D17 policy/reconstruction/mismatch/zero-trade behavior, local payload hashes, and D19 wrapper/renderer behavior.

## Self-review

- Checked that the D19 path never adds full-closure dates, never hides SECONDARY metadata, and cannot claim COMPLETE without the exact acceptance plus per-year venue-flat rows.
- Checked that D17 does not weaken the five scalar requirements, never treats monthly or commission dimensions as independent anchors, and does not alter fee-audit severity behavior.
