# Phase 1 verification evidence — final replacement-source freeze

Audit date: 2026-09-03. This is the final `tradeify-phase1-normalization-v3` replacement-source generation. All five sources and outputs remain `EXPLORATORY`; no ranking, composition, Monte Carlo, Pine rerun, locked-edition claim, or book-level cap verdict is made.

## Generation and reproduction

The runner was invoked once after final input and renderer-contract verification:

```powershell
.venv/Scripts/python.exe lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/run_phase1.py --config lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json --source-dir $SOURCE_DIR --output-dir lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/reanchor_replacements_2026-09-03
```

The execution wrapper did not surface a numeric exit field or stdout/stderr after its completion signal. Artifact publication was verified instead: the new ignored output directory, v3 manifest, and RESULTS were atomically published at 2026-09-03 19:30:13 EDT; no Python process remained. A controller's independent read-only audit then exited 0 and verified all source snapshots, hashes, calendar dates, Decimal monthly arithmetic, deadline crossings, and exposure bounds.

- Invocation-time `run_phase1.py` SHA-256: `c7f331ecbb53ab35fc15f0b1ae7d26ba1fd2674db63c5b617300efb59dc4dc83`.
- `lab/research_utils/tv_trade_ledger.py`: `cdd925c0b77efc31ded8b90a9a3ead0cd79dac9fa9af9a0e1e77f272d520b075`.
- `lab/research_utils/trade_reconciliation.py`: `b9197e5c08577012c9400d840b4e71221bafa91e81f0a03ce6d61764208d06ec`.

## Exact source pins

Source bytes are operator-owned and are not committed. All ten physical files matched these basenames, lengths, and SHA-256 values immediately before the one real invocation.

| ID | Export basename / bytes / SHA-256 | Pine basename / bytes / SHA-256 |
|---|---|---|
| aegis_6j1 | `Aegis_6J1_VB_CME_6J1!_2026-09-03_cc310.csv` / 28364 / `71e732fc92d28a56fbc1e4aa358e10b68f317a110f3facc95ed34508fad96eaa` | `aegis_6J1_venue_bound.pine` / 52092 / `db78ecba95ae78aca14501a5eaccfda2a42164d83cac12321cb7f293a9adca7c` |
| orb_mnq_recon_v7 | `ORB-MNQ-1_recon_v7_VB_CME_MINI_MNQ1!_2026-09-03_d03ac.csv` / 160557 / `bff235ea0934dace8a000dbad7eeede8673506718bd020f54f2c04cbae304568` | `orb_mnq_7_reconstruction_venue_bound.pine` / 23765 / `176c4f70c67d58053c4d3b8170d0a9be3733bc6b76b1e2f928bd7a877be052a3` |
| striker_dj30_mym_pyramid_250 | `Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-09-03_9d7ea.csv` / 47348 / `5a5006588fa5c87628df7b1c15c8af8d8ae2250be0abb0371ea4d93665ef998e` | `striker_dj30_v4.5_mym_pyramid_250_cap100k.pine` / 27497 / `712cf395396568ce22ae43f1f15b085eaba23acf1b85502abb92129f277fffd7` |
| striker_nas100_mnq_dow_wed_excluded | `Striker_NAS100_MNQ_CME_MINI_MNQ1!_2026-09-03_30a74.csv` / 88221 / `f6a93bb653d710a77f8ebde8e64639ed913171c814cd13de5f00f76d0c3d1513` | `striker_nas100_v1_mnq_dow_wed_excluded_cap100k.pine` / 33013 / `fa6a70cde002131bbd266bee70defb01e32deae2de79fdc327d661f829115c39` |
| vanguard_mgc_v04 | `Vanguard_Gold_Futures_v0.4_VB_(MGC)_COMEX_MINI_MGC1!_2026-09-03_0e3e3.csv` / 74473 / `7b9cc65c98945055f35d55cdd43f049efc4b5924e2caa59f36d50b3eb872f9f2` | `Vanguard_Gold_MGC_v0.4_venue_bound.pine` / 44177 / `af26899ca94bb0e9ee26d09e0176b6b94bba2f5da252399ce4d899fe7e3bad15` |

## Calendar, D17, and measured acceptance

The calendar is `COMPLETE` only through D19's `ACCEPTED_SECONDARY` venue-date-membership acceptance: 49 exact `EARLY_CLOSE` rows, `SECONDARY` provenance, and no full-closure date applied as a short session. The consumed LF source-calendar SHA-256 is `2698f2688cce582b08df58516fd770fa4a71a18de04870d9c14511731ea181e9`; `git hash-object --no-filters` and `HEAD:ops/calendars/cme_holiday_calendar_2022_2026.json` both equal `6b489a87f6728af5c21c52c48b65bf4b3b5516d9` under the scoped LF attribute.

D19 does not claim a primary-CME source, product close-time model, or exchange-session model. The scheduled 2025-11-28 outage/half-day classification remains conservatively included; potentially missing ad-hoc 2026-05-28 through 2026-09-02 closures remain non-conservative and must be retested if primary evidence arrives. The thirteen unresolved and three sub-deadline inventories remain published.

D17 reconstructs monthly totals from exit timestamps in `America/New_York`; all five local artifacts have zero aggregate residual and zero month-spanning trades. Independent commissions are `AMENDED_OUT`. G1.4 remains `NEEDS_CONTEXT`: fresh scalar panels are missing for all five replacement sources, and DJ30's +$287 replacement-versus-prior-200K net delta remains unexplained.

| Strategy | Rows | Trades | Net P&L | Force-flat | Fri→Sun | Peak micro-equivalent range | Monthly buckets |
|---|---:|---:|---:|---:|---:|---:|---:|
| aegis_6j1 | 242 | 121 | $27996.05 | 0 | 0 | 80–80 | 45 |
| orb_mnq_recon_v7 | 1362 | 681 | $48118.16 | 0 | 0 | 4–6 | 49 |
| striker_dj30_mym_pyramid_250 | 406 | 203 | $32057.36 | 0 | 0 | 77–77 | 48 |
| striker_nas100_mnq_dow_wed_excluded | 756 | 378 | $112253.42 | 0 | 0 | 77–77 | 49 |
| vanguard_mgc_v04 | 676 | 338 | $18709.48 | 0 | 0 | 6–6 | 48 |

Totals are 3442 events and 1721 trades. The controller independently recomputed every local monthly Decimal sum, source/accounting residual, timezone deadline crossing, and exposure range. The upper-bound implementation was independently confirmed byte-identical to reviewed `80abcec` behavior. Per-strategy values are not a Phase 4 joint-book cap finding.

## Frozen hashes

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| phase1_config.json | 9023 | `df238cd78fc0a381fdb86466ef3dfca5522dd8db7ae0cf245165f370df9f3892` |
| tradeify_commission_schedule.json | 428 | `61c8957a4adfabf6b8e8c4eb984e6d9388a223145f90b0b9ca66b3dd7ca28750` |
| cme_early_close_calendar.json | 4330 | `3f114ec021c6d2d15ca88d4063a396612fe9c662ae92d4c25a2758657a1feaa9` |
| tv_summary_anchors.json | 947 | `481e9bb2227578497dbc506d336377a5d51c366161dae6dd7d534c9c2ef88979` |
| canonical_events.csv (ignored) | 1019004 | `3a6b754ec145db0e5c09ce18413d7d42d60fa1ce8ac034bd6d6878ae4251d3ac` |
| canonical_trades.csv (ignored) | 362482 | `7e650599241b8150d0ee31ea04a7406c200e1f009c9530908a9644e56bed765a` |
| weekly_exit_blocks.csv (ignored) | 14718 | `d0b3e5ab840ef0a88c9f7b4b2c7254b3774142b85a55a9cfaeaa04fa5fe7934a` |
| reconciliation_manifest.json | 63592 | `f40856086b4498960dc1fdc485a097d32323d0b5160f93775ff355c37b71ec01` |
| RESULTS.md | 37583 | `40cd23eda0618d68a2237c5d6713123b318f918d01218721aef8b4a753c75290` |

Detail hashes in configuration order: `546cf0e0b1b9fe3d26793f0dc87ea53cb7990decd744bb5ec261110b32c964bc`, `a0ea8a6b27aba3aa6f292322d82c3e38029e1c89cb8bbefbcb329305fcff81ea`, `c7bbab4867e381428da31116c61ea4cb224d8b2b848cf328ce105443988871e3`, `4d2807e40f946f708e270ad66be01451ca0a05d6c05099ac811663532615b5d4`, `a0a9564b1f598f04e68a1a6d56cf2e49d4ef25c7e3b67305a4ddfd2ca142e4d1`. Monthly hashes in the same order: `5242591bbb40a93480e5356011f31a4d6fd0575d1d0f1f73ee1236926c343ca1`, `632382c8bffea9644486b961e706d5f94a7f782235ecc4b7d5b9bab29070e2ad`, `bd34b13a72d6c771cdbb654d3798bb53307f60ac144e1553141efe5df4303070`, `7163605aeddd8953d73e44b46162ec051d4d45587c508701079acbd4a6e7568a`, `5b1f2a5872aac49ef4988b423bc3d042232c16f5056c1816bddc4eeebde56acb`.

## Test and hygiene evidence

Before the real run, the focused Phase 1, D17, D19, safety, cost, and production-barrier command completed with **374 passed, 1 skipped, 2 explicitly stale generated-artifact acceptance tests deselected**. The skip is the Windows file-symlink privilege test. The post-freeze all-selected version of the same focused command completed with **376 passed, 1 skipped in 11.27s**. The new renderer regression first failed because local monthly hashes were absent from RESULTS, then passed after the renderer emitted those five aggregate-only hash lines.

The repository-wide full suite completed at tested commit `9bb31ea`: `.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider --basetemp <external temporary directory>` exited 0 with **2495 passed, 35 skipped, 23 warnings, 6 subtests passed in 399.98s**. The focused evidence command remains **376 passed, 1 Windows-symlink skip in 11.27s**. `python scripts/gate_manifest.py --tier check` and the catalog-only gate each exited 0. Report-only warnings remain explicit: inherited dependency deprecations/fallback, historical scoring notices, and gate governance/inventory warnings. Main `b2d070c` merged as `4729080`; the exact before/after Git tree is `c2918da224f4e39bc81ca451c9327f34e0343364`, so tested bytes are unchanged. Final whole-branch review is software-ready with no Critical or Important findings; this documentation-only wave closes the minor documentation finding. Remaining legacy gross-identity/final cumulative-cent-boundary coverage is nonblocking debt, duplicate-mismatch exactness remains tested, and Phase 1 remains `NEEDS_CONTEXT` for fresh panels and the DJ30 +$287 gap.
