# Phase 1 verification evidence — R4 final five-source freeze

Audit date: 2026-09-03. This evidence is separate from generated RESULTS. Final generation is `tradeify-phase1-normalization-v2`. All five sources remain `EXPLORATORY`; campaign status is `BLOCKED_EXPLORATORY`, verdict cap is `NEEDS_CONTEXT`, and G1.4 is partial. D13(b) is now `ACCEPTED_UNMODELED`: the continuous-roll limitation is WARNING, not a blocker by itself; attribution remains UNAVAILABLE. Nothing here qualifies or deploys a strategy.

The operator addendum's actual pin lookup, version identity, D13 policy, parsed-fee snapshot and wrong-byte-length tests are implemented and verified. The v2 real run supersedes the earlier v1 generation. Code and acceptance literals are frozen; full-suite v2 verification is pending at this review checkpoint.

## Revision, environment and reproduction

- Checkout: `67d65d76722e86b091c422e666d00103a72a7d6a`, incorporating main `8327f14` and both authoritative candidate pins.
- The final v2 real run used uncommitted R4 loader/venue/renderer changes on that checkout; this was not unchanged code at `67d65d7`. Raw code SHA-256: runner `2de2016fcee3d7ff64116a852bca96b71d3b0eb53f8119e0e69e46f4804c569e`; `tv_trade_ledger.py` `cdd925c0b77efc31ded8b90a9a3ead0cd79dac9fa9af9a0e1e77f272d520b075`; `trade_reconciliation.py` `e834db8f5f8d1a1180704e826da71b73659635828c4f39e30d7222ea17cfca67`.
- Manifest `git_base_commit` remains original campaign base `ed181233afd01d8fc128bc76ac626e43c3761f87`, not the run-code revision.
- Windows; `.venv/Scripts/python.exe`, Python 3.14.3, pandas 3.0.5, NumPy 2.5.2, pytest 9.1.1, PyYAML 6.0.3.
- Exact source basenames, byte lengths and SHA-256 pins in `phase1_config.json` were independently verified before parsing and after the replacement run. Dropped exports were never opened or parsed.

From the repository root, supply the operator-owned directory as `$SOURCE_DIR`; its absolute private path is intentionally absent here:

```powershell
.venv/Scripts/python.exe lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/run_phase1.py --config lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json --source-dir $SOURCE_DIR --output-dir lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/reanchor_iteration3
```

Historical v1 runs: both exit 0. The first exposed `Decimal('...')` monthly-map display versus strings after manifest JSON parsing; a controller-authorized renderer fix/replacement changed only RESULTS from `e5c22cfcf29a8a5529bd623589657d59d52796c51979ada4a0d4cb73f3144a35` to `e4dd850635f11389d4d81ed3b17bd0df061a37b77bda88fee6a6ade232671744`. These are superseded audit history, not current hashes.

After the operator addendum and synthetic GREEN, one final v2 invocation of the command above exited 0. The explicit D13 policy changes config, five detail reports, manifest and RESULTS hashes; three ledger hashes, fee/calendar/summary snapshots and all ten source files remain unchanged. No tolerances or accounting changed.

Actual PORT_MANIFEST entries are loaded once; pinned active/dropped refs must match existing target basename/hash, with safe manifest-owned placement and no private in-repo Pine requirement. The immutable D13 object is passed explicitly to venue analysis; default callers without it still see the roll blocker. Fee hashing now uses the exact parsed bytes even if the file changes afterward. Operator ruling 2026-09-03, campaign-state §6 D13(b), binds:

- Phase 3 pre-registration states back-adjustment seam risk as a limitation of every campaign claim: fills cannot be attributed to a contract month, and a seam crossing is indistinguishable from a price move.
- A Phase 6 seam-sensitivity check is pre-registered with its severity frozen alongside the other Phase 6 cutoffs.

Neither future obligation is claimed discharged by this implementation.

## Independent aggregate and boundary checks

| Strategy | Events | Trades | Net P&L USD | Daily violations | Fri→Sun | Closed-trade / TV panel max DD USD |
|---|---:|---:|---:|---:|---:|---|
| aegis_6j1 | 244 | 122 | 28702.75 | 9 | 0 | 1298.40 / 1470.40 |
| orb_mnq_recon_v7 | 1362 | 681 | 47533.16 | 310 | 3 | 6168.20 / 6794.02 |
| striker_dj30_mym_pyramid_250 | 406 | 203 | 31770.36 | 0 | 0 | 4262.66 / 4568.68 |
| striker_nas100_mnq_dow_wed_excluded | 756 | 378 | 112253.42 | 0 | 0 | 8197.80 / 8269.62 |
| vanguard_mgc_v04 | 686 | 343 | 20388.04 | 226 | 0 | 1785.48 / 1847.60 |

Independent `Import-Csv` checks found 3,454 events (244+1362+406+756+686), 1,727 trades (122+681+203+378+343) and 210 weekly rows. All 3,454 event rows contain 64-character lower-case hex `source_row_sha256` and populated UTC timestamps; all 1,727 trades preserve `duration_bars` and both UTC fields. Event and weekly timestamp domains are UTC. Event/trade strategy IDs and wide weekly strategy columns contain only the five retained IDs; dropped IDs are absent.

All five independent drawdown comparisons are `MISMATCH` blockers: closed-trade exit-equity drawdown is not automatically the TradingView panel measure. Available count/net/win-rate/profit-factor anchors match within frozen tolerances. No series or tolerance was changed. Empty historical CME source/row inventories and absent commission/monthly operator anchors remain explicit; no evidence was invented. Both `PINNED_RESEARCH_VARIANT` records and their exact divergence strings are preserved.

## Final raw-byte SHA-256 freeze

Independently hashed with `Get-FileHash -Algorithm SHA256`; the first 12 match manifest fields. The renderer exposes all input, ledger and detail hashes. Tests freeze those plus manifest and RESULTS bytes.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| phase1_config.json | 8828 | `bc806ace41f899f17fa9cd54960bcd7c6ee6f3b02b28f8574c5b600997667e87` |
| tradeify_commission_schedule.json | 428 | `61c8957a4adfabf6b8e8c4eb984e6d9388a223145f90b0b9ca66b3dd7ca28750` |
| cme_early_close_calendar.json | 445 | `742e83508a3addf034ce6536e42553522bea28c96f8e3718629cf5495c405277` |
| tv_summary_anchors.json | 4471 | `a3c3ae0c102adf15199a2f68cebe07a97c4cae1b0b5b4f7c07f73c1093c96ff2` |
| canonical_events.csv (ignored) | 1022275 | `c04e2cc8b07a21abb47b70f6c195ea0336ec76087c0e76fb26f37e64f2c945ee` |
| canonical_trades.csv (ignored) | 363756 | `0336cf3836055fbc951c995725c718e15aaff03e064bfade5f8310a5c382e257` |
| weekly_exit_blocks.csv (ignored) | 14730 | `e33f48c13c3fd4c6438bb755fb6ac070bebbbf308ad0377320468a1a6ef8850e` |
| strategy_reports/aegis_6j1.json (ignored) | 20021 | `9b40524e9c06870161ed77fde5cb1cea4a2501d7696cc6899607a2ab0e25b7c5` |
| strategy_reports/orb_mnq_recon_v7.json (ignored) | 133817 | `3cdf75dfc2821279f90dbafc0ac100ad227deefe9ab96360db157f880df7b8af` |
| strategy_reports/striker_dj30_mym_pyramid_250.json (ignored) | 15496 | `a762cc3b255f879ee3b92c77d6dc27a3de9d443a8c8219b94797e4833eff904e` |
| strategy_reports/striker_nas100_mnq_dow_wed_excluded.json (ignored) | 15791 | `c5c3d8f431b4ecdda6943e562ee9f152a924132d9f2d82e286c0293933187a8a` |
| strategy_reports/vanguard_mgc_v04.json (ignored) | 100615 | `ab61978d7dc7c6f1428c7d945d6258e0bcab5c5fdd276a84a1cea05bfba73af7` |
| reconciliation_manifest.json | 102499 | `89a0d42e97b38ddd12fca29a151e17d26e6395a7d85502482c125303b7cd479c` |
| RESULTS.md | 35825 | `ab69e3a70b461356edfe4218bef6177ae919730c72cab59cb0e8e27310e5b8cc` |

## Tests and gates

All pytest commands use `-p no:cacheprovider` and an external basetemp. Here `$TEST_TMP` names the explicitly writable external visualization directory, not any repository directory. Baseline eight Phase 1/evidence/safety modules: 198 passed, 1 Windows symlink skip, exit 0. Pre-real-run synthetic suite: 198 passed, 1 skipped, 1 stale-manifest acceptance deselected, exit 0. Renderer synthetic RED: 1 failed, 20 deselected; GREEN covering runner/evidence: 116 passed, 1 skipped, 1 stale-RESULTS acceptance deselected, exit 0.

```powershell
.venv/Scripts/python.exe -m pytest tests/test_tv_trade_ledger.py tests/test_trade_reconciliation.py tests/test_joint_trade_blocks.py tests/test_tradeify_phase1_runner.py tests/test_phase1_safety_gates.py tests/test_cme_calendar_evidence.py tests/test_tv_summary_reconciliation.py tests/test_tradeify_phase1_evidence_integration.py tests/test_tradeify_phase1_identity_policy.py tests/test_cost_model.py tests/core/test_mc_intraday_barrier.py tests/core/test_trailing_dd_boundary.py tests/core/test_trailing_locking_boundary.py tests/core/test_mc_preflight.py -p no:cacheprovider --basetemp "$TEST_TMP/r4-v2-final-focused" -q -rs
```

Final v2 focused exit 0: **334 passed, 1 skipped in 8.13s**, no warnings. Sole skip: `test_symlink_capture_cannot_escape_directory`, WinError 1314 (file-symlink creation privilege unavailable). Production barrier files are unchanged. Before the v2 real run, all nine synthetic campaign/evidence/safety modules passed 227 tests, 1 skipped, 2 deliberately stale committed-artifact tests deselected, exit 0. New RED evidence: identity/policy module 14 failed/9 passed; fee/policy integration 2 failed/2 passed. Explicit wrong-byte-length tests already passed the existing implementation. A self-review dot-target diagnostic regression failed then passed after rejecting an empty normalized path.

```powershell
.venv/Scripts/python.exe -m pytest -p no:cacheprovider --basetemp "$TEST_TMP/r4-v2-full" -q -rs
```

Final v2 full suite is pending at this review checkpoint (exec session 16357), with all code/acceptance literals stable before collection and no subsequent code/test edits. Output is streamed to external `r4-v2-full-suite.log`; no final v2 suite result is claimed yet.

Historical v1 full suite: exit 1, 1 failed/2,423 passed/35 skipped/23 warnings/6 subtests passed in 484.58s. Its sole failure collected the old RESULTS literal before the mid-run freeze update (`e5c22cfc...` expected vs `e4dd8506...` actual). This worker invocation-order error is not claimed as an external failure or valid final-tree verification; corrected tests subsequently passed. Warnings were dependency deprecations and explicit historical stale-gate notices; `r4-full-suite.log` retains complete history.

Catalog initially exited 1 (`CATALOG.md stale vs scan`) after generated five-source wording replaced seven-source wording. `.venv/Scripts/python.exe scripts/archive_lab_analysis.py --regenerate-catalog` exited 0. Only this study's 5-column In flight and 7-column c1 Hot bodies row edits remain. Final `.venv/Scripts/python.exe scripts/archive_lab_analysis.py --check --catalog-only` exited 0, with five pre-existing missing-ignored-heavy-artifact warnings.

```powershell
$env:PYTHONPATH = (Resolve-Path -LiteralPath '.venv/Lib/site-packages').Path
.venv/Scripts/python.exe scripts/gate_manifest.py --tier check
```

Initial gate stopped on stale catalog (exit 1); after regeneration the complete gate exited 0. Existing warning/report-only inventory includes absent private Pine/data trees, five missing ignored-heavy inventories, seven P5-WEAK citations, session-label notes, deployment drift, prose-only falsifiers, six notice grade/K flags and five spec-provenance findings. No gate skipped; no dependency installed.

## Byte hygiene and scope

Campaign-local `.gitattributes` pins `*.json text eol=lf` and `RESULTS.md text eol=lf`. Only this study's tracked JSON and RESULTS were mechanically normalized before hashing, never CSV/Pine sources. `git check-attr text eol` confirms all six files. For every final file, `git hash-object --no-filters` equals `git hash-object --path=<path>`: raw bytes equal Git clean/blob bytes under the policy. No staging by this worker.

`git diff --check` passed. `git ls-tree -r -l HEAD` found no tracked blob over 1,000,000 bytes. `git diff --name-only origin/main...HEAD -- '*.csv' '*.pine'` was empty. Local outputs are ignored, no source/row bytes staged, no absolute private source path in tracked study artifacts. Old output directories were preserved.

Orchestrator surfaces, plans, ADRs, campaign-state, core/ops and cost-model logic are untouched by this worker. Original-base cost-model blob materialized with the existing Windows CRLF policy exactly equals current raw bytes; SHA-256 `8397a9d9a34d86121bad9ac41993330d44a4813b5876e20d138bc623f31f9a98`. A `core.autocrlf=false` whole-worktree diagnostic flags pre-existing PORT_MANIFEST CRLF bytes as whitespace; ordinary policy-aware diff is clean and that file was not edited.
