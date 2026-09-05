# Phase 1 verification evidence — single generation-v4 population freeze

Audit date: 2026-09-05. This is the single `tradeify-phase1-normalization-v4` population/re-freeze, constituent (i), iteration 6 of 8. All five sources and outputs remain `EXPLORATORY`; no ranking, composition, Monte Carlo, Pine rerun, locked-edition claim, or book-level cap verdict is made.

## Generation and reproduction

The runner was invoked exactly once for this population generation using the existing local Python 3.11.9 environment:

```powershell
& $PY311 lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/run_phase1.py --config lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json --source-dir $SOURCE_DIR --output-dir lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/population_2026-09-05
```

`$PY311` denotes that existing interpreter and `$SOURCE_DIR` denotes the operator-owned frozen source directory; their machine paths are intentionally omitted. This records the completed invocation and does not authorize an additional real generation. The captured exit code was `0`. The invocation's `_BASE_COMMIT`, serialized as manifest `git_base_commit`, is `00b2bb7a9c50081545acd7f52f4bcd8dd8af964c`.

- Invocation-time `run_phase1.py` SHA-256: `a83cdd68db5815114e1c4c7d5cebdde1a8e99e0cc52a559d947808a21f5c6a3d`.
- Invocation-time `lab/research_utils/tv_trade_ledger.py` SHA-256: `87b9f1fad750a25968d213e83c69b4ab29bd18bcc963da964678f05d71b25845`.
- Invocation-time `lab/research_utils/trade_reconciliation.py` SHA-256: `2af1960d8dae659d3e0688e3eea62a4fdb956d3295d3e7377fc2613e132f88c6`.
- Invocation-time `lab/research_utils/tv_summary_reconciliation.py` SHA-256: `0d2343b2dc26f43f5c2e22eaa5556aa5be53674b2942e53b24a2a92db54672ef`.

All five full private input snapshots are sealed: 211 inputs captured, with six differences from the pinned bodies' defaults. The operator explicitly confirmed that the existing trade-list exports reflect the exact captured chart state. Campaign-state §52 accepts that operator-attested identity together with the unchanged export/Pine byte pins for this intake; no fresh reexport was performed, and no independent reproduction is claimed. The runner verified each snapshot's exact-byte digest against its populated config pin before publication. Input titles, values, screenshots and provenance receipts remain private and ignored.

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

The calendar is `COMPLETE` only through D19's `ACCEPTED_SECONDARY` venue-date-membership acceptance: exactly 40 `EARLY_CLOSE` rows, set-equal to the source calendar's 49-date `venue_flat_dates` inventory intersected with 2022-09-01 through 2026-09-02, `SECONDARY` provenance, and no full-closure date applied as a short session. The consumed LF source-calendar SHA-256 is `2698f2688cce582b08df58516fd770fa4a71a18de04870d9c14511731ea181e9`; `git hash-object --no-filters` and `HEAD:ops/calendars/cme_holiday_calendar_2022_2026.json` both equal `6b489a87f6728af5c21c52c48b65bf4b3b5516d9` under the scoped LF attribute.

D19 does not claim a primary-CME source, product close-time model, or exchange-session model. The scheduled 2025-11-28 outage/half-day classification remains conservatively included; potentially missing ad-hoc 2026-05-28 through 2026-09-02 closures remain non-conservative and must be retested if primary evidence arrives. The thirteen unresolved and three sub-deadline inventories remain published.

D13 remains `ACCEPTED_UNMODELED`, with `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` retained as a WARNING limitation. Contract-month and seam attribution remain `UNAVAILABLE`; the Phase 3 limitation and Phase 6 seam-sensitivity obligations are still owed.

D17 reconstructs monthly totals from exit timestamps in `America/New_York`; all five local artifacts have zero aggregate residual and zero month-spanning trades. Independent commissions are `AMENDED_OUT`. All five independent panels from campaign-state §18a are populated against their own pinned exports. The exact six-key policy includes `max_drawdown: OVERLAP_KEYED`, and the panel anchor is `tv_panel_max_drawdown_usd`. D30 records historical capital-delta attribution as `UNESTABLISHED`; it is not a missing-panel prerequisite.

The runner reports `COMPLETE` evidence coverage. All four non-DD limbs (`trade_count`, `net_pnl_usd`, `win_rate_pct`, `profit_factor`) are `MATCH` on each source. D32 results are:

| Strategy | Four non-DD limbs | Measured overlap/tie | Panel DD status | DD policy |
|---|---|---|---|---|
| aegis_6j1 | MATCH / MATCH / MATCH / MATCH | No | COINCIDENT | OVERLAP_KEYED_D32 |
| orb_mnq_recon_v7 | MATCH / MATCH / MATCH / MATCH | Yes | RECORDED | OVERLAP_KEYED_D32 |
| striker_dj30_mym_pyramid_250 | MATCH / MATCH / MATCH / MATCH | Yes | RECORDED | OVERLAP_KEYED_D32 |
| striker_nas100_mnq_dow_wed_excluded | MATCH / MATCH / MATCH / MATCH | Yes | RECORDED | OVERLAP_KEYED_D32 |
| vanguard_mgc_v04 | MATCH / MATCH / MATCH / MATCH | Yes | RECORDED | OVERLAP_KEYED_D32 |

Drawdown is not a symmetric panel reconciliation. Under non-overlap, the excursion walk is a lower bound that omits intratrade peaks; only a walk exceeding the panel by more than the inclusive cent tolerance blocks. Under overlap/ties, neither computed drawdown measure bounds synchronized account-equity drawdown, and the independent panel is recorded without claiming a match. `COINCIDENT` is INFO, not MATCH.

| Strategy | Rows | Trades | Net P&L | Force-flat | Fri→Sun | Peak micro-equivalent range | Monthly buckets |
|---|---:|---:|---:|---:|---:|---:|---:|
| aegis_6j1 | 242 | 121 | $27996.05 | 0 | 0 | 80–80 | 45 |
| orb_mnq_recon_v7 | 1362 | 681 | $48118.16 | 0 | 0 | 4–6 | 49 |
| striker_dj30_mym_pyramid_250 | 406 | 203 | $32057.36 | 0 | 0 | 77–77 | 48 |
| striker_nas100_mnq_dow_wed_excluded | 756 | 378 | $112253.42 | 0 | 0 | 77–77 | 49 |
| vanguard_mgc_v04 | 676 | 338 | $18709.48 | 0 | 0 | 6–6 | 48 |

Totals remain 3442 events and 1721 trades. The canonical event, trade and weekly ledgers are byte-identical to the previous freeze, as are all five monthly-reconciliation artifacts. The retained upper-bound implementation is the reviewed `80abcec` behavior. Per-strategy values are not a Phase 4 joint-book cap finding. `COMPLETE` describes evidence coverage only: sizing-faithfulness, synchronized replay, and the statistical freeze remain owed; no qualification or search authorization follows.

## Frozen hashes

Every byte count and SHA-256 below was recomputed from this generation's files. Ignored artifact names are relative to `local_artifacts/population_2026-09-05/`; their contents remain local. Strategy-detail and monthly rows are in configuration order.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| phase1_config.json | 9548 | `a00bdd32687744b729510efe16704b0eb2c094d8551a7d91e87c5d6b878d9acb` |
| tradeify_commission_schedule.json | 428 | `61c8957a4adfabf6b8e8c4eb984e6d9388a223145f90b0b9ca66b3dd7ca28750` |
| cme_early_close_calendar.json | 3809 | `6eeb3b9d198eabf0a5a2115c4648f69629720a500616f38e219dff7bc57d0334` |
| tv_summary_anchors.json | 4111 | `22d6ab6e7356b7b3052177b6385783f850a8a43f7a8cc9abd0146e6b0cf69376` |
| canonical_events.csv (ignored) | 1019004 | `3a6b754ec145db0e5c09ce18413d7d42d60fa1ce8ac034bd6d6878ae4251d3ac` |
| canonical_trades.csv (ignored) | 362482 | `7e650599241b8150d0ee31ea04a7406c200e1f009c9530908a9644e56bed765a` |
| weekly_exit_blocks.csv (ignored) | 14718 | `d0b3e5ab840ef0a88c9f7b4b2c7254b3774142b85a55a9cfaeaa04fa5fe7934a` |
| reconciliation_manifest.json | 77650 | `ebf8bab7feb4d13f594f0cf98d5d92c194fe6d55d0cf2650c374644bd16848fa` |
| RESULTS.md | 41201 | `7270042f4727f5e4388d99836544e7ff2b50d6ace6da30d3d82459abfd05932a` |
| strategy_reports/aegis_6j1.json (ignored) | 10232 | `42a784e3b3ccd79e4af82a80a08ad4f40b8f4e690cc3a0a45cc74635b700db2f` |
| strategy_reports/orb_mnq_recon_v7.json (ignored) | 8228 | `31c09388bf94bfcf3b333d5e11aa5df4504a2a75bbff901342d1a0ce725390f2` |
| strategy_reports/striker_dj30_mym_pyramid_250.json (ignored) | 8422 | `09796afb37da8114bef200ce02d46b47d37131c3534914f3a642dc81334e335f` |
| strategy_reports/striker_nas100_mnq_dow_wed_excluded.json (ignored) | 8464 | `87fba3c502e696432f60d094b43209a1bb4ef0cf7e5c0b8167717a6f8c797d3a` |
| strategy_reports/vanguard_mgc_v04.json (ignored) | 8241 | `57e5ed7e06815e14725b90f05a96d01b5aac4f524df3d2695a2079be247ed537` |
| monthly_reconciliation/aegis_6j1.json (ignored) | 1666 | `5242591bbb40a93480e5356011f31a4d6fd0575d1d0f1f73ee1236926c343ca1` |
| monthly_reconciliation/orb_mnq_recon_v7.json (ignored) | 1778 | `632382c8bffea9644486b961e706d5f94a7f782235ecc4b7d5b9bab29070e2ad` |
| monthly_reconciliation/striker_dj30_mym_pyramid_250.json (ignored) | 1779 | `bd34b13a72d6c771cdbb654d3798bb53307f60ac144e1553141efe5df4303070` |
| monthly_reconciliation/striker_nas100_mnq_dow_wed_excluded.json (ignored) | 1825 | `7163605aeddd8953d73e44b46162ec051d4d45587c508701079acbd4a6e7568a` |
| monthly_reconciliation/vanguard_mgc_v04.json (ignored) | 1745 | `5b1f2a5872aac49ef4988b423bc3d042232c16f5056c1816bddc4eeebde56acb` |

The config, summary anchors, manifest, RESULTS, and all five strategy-detail hashes changed. The commission schedule, 40-date calendar, three canonical-ledger hashes and all five monthly-reconciliation hashes are unchanged. All twenty source hashes remain unchanged. Each strategy-detail and monthly hash above agrees with the generated manifest's corresponding entry; the invocation-time code hashes above match the computation checkout bytes. Checkout newline conversion can change raw code-file hashes without changing the committed content.

## Test and hygiene evidence

The prescribed seven-module focused suite passed on both runtimes: Python 3.11.9,
285 passed in 16.82s; Python 3.12.14, 285 passed in 20.84s. It covered
`test_tv_trade_ledger`, `test_tradeify_phase1_runner`,
`test_tradeify_phase1_evidence_integration`, `test_tv_summary_reconciliation`,
`test_tradeify_drawdown_policy`, `test_tradeify_d27_excursion`, and
`test_trade_reconciliation`.

Full-suite commands were `python -m pytest -q -p no:cacheprovider`, with a separate
temporary base per runtime. Both exited 0:

- Python 3.11.9: 2716 passed, 33 skipped, 21 warnings, 6 subtests passed in 516.70s (0:08:36).
- Python 3.12.14: 2703 passed, 35 skipped, 23 warnings, 6 subtests passed in 585.47s (0:09:45).

The first Python 3.11 full run reported five failures because the optional
research temporal-consistency tests required the pruned DISC-CAMP-0 archive
fixture. The exact historical fixture was restored locally from its last
pre-prune bytes under a Git ignore rule; all 12 tests in that module then passed,
followed by the successful full rerun above. No code or test assertion changed.
Python 3.12 skips that optional module because its research dependency is absent.
The archive fixture and failed-run log stay local and are not publication inputs.

`python scripts/gate_manifest.py --tier check` exited 0. Its absent private-vendor
tree warnings are expected in this worktree. `git diff --check` passed.

The final local audit recomputed all 19 frozen-table rows and checked the five
snapshot bindings. All 41 private evidence files and all 13 generated ledger,
detail and monthly artifacts are ignored. Only 14 approved study/test and
orchestrator files enter the publication patch; no CSV, Pine body, input value,
screenshot, account detail or machine path is added. The config diff contains
only the five digest lines; no current artifact/test retains the old config hash.
The publication branch is created directly from the validated main base and
receives reviewed final patches only, without private computation history.
Current-head publication CI remains the separate P8 merge gate.
