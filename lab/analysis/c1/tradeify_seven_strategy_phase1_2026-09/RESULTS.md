# Tradeify five-active-source Phase 1 reconciliation

**Theme:** c1

**In-flight:** yes

**Status:** ACTIVE — strict five-source Tradeify source, accounting, deadline, cap, and provenance normalization

> **EXPLORATORY — Phase 0 was skipped.** All supplied history is development data; this report is not confirmatory, qualified, admitted, or deployable.

Campaign status: `BLOCKED_EXPLORATORY`

Phase 1 evidence verdict cap: `NEEDS_CONTEXT`

Runner generation: `tradeify-phase1-normalization-v2`

## Continuous-contract roll disposition

D13: `ACCEPTED_UNMODELED` — contract-month and seam attribution remain unavailable, not modeled or resolved.

Operator ruling 2026-09-03; docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md §6 D13(b).

- Phase 3 pre-registration states back-adjustment seam risk as a limitation of every campaign claim: fills cannot be attributed to a contract month, and a seam crossing is indistinguishable from a price move.
- A Phase 6 seam-sensitivity check is pre-registered with its severity frozen alongside the other Phase 6 cutoffs.

## Strategy inventory

| Strategy | Status | Pine pin status | Pin ref | Divergence | Export bytes | Pine bytes | Rows | Trades | Net P&L | Daily-deadline holds | Fri→Sun sub-count |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aegis_6j1 | BLOCKED_EXPLORATORY | NOT_IN_PORT_MANIFEST | None | None | 28612 | 50184 | 244 | 122 | $28702.75 | 9 | 0 |
| orb_mnq_recon_v7 | BLOCKED_EXPLORATORY | NOT_IN_PORT_MANIFEST | None | None | 160584 | 19878 | 1362 | 681 | $47533.16 | 310 | 3 |
| striker_dj30_mym_pyramid_250 | BLOCKED_EXPLORATORY | PINNED_RESEARCH_VARIANT | core/strategies/PORT_MANIFEST.sha256:core/strategies/candidates/striker_dj30_v4.5_mym_pyramid_250.pine | pyramid 250% vs locked 750% | 47149 | 26726 | 406 | 203 | $31770.36 | 0 | 0 |
| striker_nas100_mnq_dow_wed_excluded | BLOCKED_EXPLORATORY | PINNED_RESEARCH_VARIANT | core/strategies/PORT_MANIFEST.sha256:core/strategies/candidates/striker_nas100_v1_mnq_dow_wed_excluded.pine | day-of-week set {Mon,Tue,Thu,Fri} vs locked {Mon,Tue} | 88131 | 32242 | 756 | 378 | $112253.42 | 0 | 0 |
| vanguard_mgc_v04 | BLOCKED_EXPLORATORY | NOT_IN_PORT_MANIFEST | None | None | 75654 | 39993 | 686 | 343 | $20388.04 | 226 | 0 |

## Dropped source inventory

These exports are provenance only and are never normalized, counted, or used in ledgers or weekly results.

| Previous strategy ID | Export | Export SHA-256 | Pine | Pine SHA-256 | Pin ref | Reason |
|---|---|---|---|---|---|---|
| striker_dj30_qtxg1_swap_body_on_mym | Striker_DJ30_MNQ_Q-TXG-1_PROTOTYPE_CBOT_MINI_MYM1!_2026-09-02_82cba.csv | 2c2d893ba0daa127f1c857e81ec436b535e4e8eb85f0c728e2ba39dc6485826d | striker_dj30_v4.5_mnq_qtxg1_prototype.pine | 178a2a8e1c78e45a5142749f92284c09d286907a7e096883e1133297cb8a806d | core/strategies/PORT_MANIFEST.sha256:core/strategies/_archive/striker/striker_dj30_v4.5_mnq_qtxg1_prototype.pine | SWAP_PORT_BODY_POINT_VALUE_NOT_OVERRIDDEN |
| striker_nas100_qtxg1_swap_body_on_mnq | Striker_NAS100_MYM_QTXG1_CME_MINI_MNQ1!_2026-09-02_304f8.csv | f1e35c4ee1c9735c3ebbed99648a42034d9b3f57b53960f9e41f6e6c09b25f9c | striker_nas100_v1_mym_qtxg1_prototype.pine | 19264da29a3d9a30200600689e1950931f1abfb648e9071a232ee83fdec2756c | core/strategies/PORT_MANIFEST.sha256:core/strategies/_archive/nas/striker_nas100_v1_mym_qtxg1_prototype.pine | SWAP_PORT_BODY_POINT_VALUE_NOT_OVERRIDDEN |

## Evidence boundaries

- The source CSV/Pine bytes, row-level event/trade/weekly ledgers, and five detailed issue reports remain local and gitignored.
- No source row was repaired, dropped for an outcome, re-ranked, composed, simulated, or rerun in Pine.
- Scalar MAE/MFE values are inventory-only excursion bounds, not timestamped paths.
- Per-strategy caps are measured against 80 micro-equivalents; the joint book-cap verdict is deferred to Phase 4.
- CME holiday-short coverage is `NEEDS_CONTEXT`; no historical early-close date was inferred.
- CME early-close coverage note: If the primary-source 2022–2026 CME early-close dates cannot be captured, report a NEEDS_CONTEXT cap, never a silent omission; an early-close hold may go undetected.

## Frozen hashes

- Config: `bc806ace41f899f17fa9cd54960bcd7c6ee6f3b02b28f8574c5b600997667e87`
- Tradeify fee capture: `61c8957a4adfabf6b8e8c4eb984e6d9388a223145f90b0b9ca66b3dd7ca28750`
- CME calendar capture: `742e83508a3addf034ce6536e42553522bea28c96f8e3718629cf5495c405277`
- Independent TradingView anchors: `a3c3ae0c102adf15199a2f68cebe07a97c4cae1b0b5b4f7c07f73c1093c96ff2`
- Canonical events: `c04e2cc8b07a21abb47b70f6c195ea0336ec76087c0e76fb26f37e64f2c945ee`
- Canonical trades: `0336cf3836055fbc951c995725c718e15aaff03e064bfade5f8310a5c382e257`
- Weekly exit blocks: `e33f48c13c3fd4c6438bb755fb6ac070bebbbf308ad0377320468a1a6ef8850e`
- Detail report aegis_6j1: `9b40524e9c06870161ed77fde5cb1cea4a2501d7696cc6899607a2ab0e25b7c5`
- Detail report orb_mnq_recon_v7: `3cdf75dfc2821279f90dbafc0ac100ad227deefe9ab96360db157f880df7b8af`
- Detail report striker_dj30_mym_pyramid_250: `a762cc3b255f879ee3b92c77d6dc27a3de9d443a8c8219b94797e4833eff904e`
- Detail report striker_nas100_mnq_dow_wed_excluded: `c5c3d8f431b4ecdda6943e562ee9f152a924132d9f2d82e286c0293933187a8a`
- Detail report vanguard_mgc_v04: `ab61978d7dc7c6f1428c7d945d6258e0bcab5c5fdd276a84a1cea05bfba73af7`

## Issues by strategy

### aegis_6j1

- `BLOCKER` `FORCE_FLAT_VIOLATION` × 9
- `BLOCKER` `TV_SUMMARY_MISMATCH` × 1
- `WARNING` `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` × 1
- `WARNING` `EARLY_CLOSE_CALENDAR_INCOMPLETE` × 1
- `WARNING` `PINE_EXPORT_COMMISSION_MISMATCH` × 1
- `WARNING` `PINE_VENUE_COMMISSION_MISMATCH` × 1

### orb_mnq_recon_v7

- `BLOCKER` `FORCE_FLAT_VIOLATION` × 310
- `BLOCKER` `TV_SUMMARY_MISMATCH` × 1
- `WARNING` `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` × 1
- `WARNING` `CROSS_DATE_HOLD` × 3
- `WARNING` `EARLY_CLOSE_CALENDAR_INCOMPLETE` × 1

### striker_dj30_mym_pyramid_250

- `BLOCKER` `TV_SUMMARY_MISMATCH` × 1
- `WARNING` `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` × 1
- `WARNING` `EARLY_CLOSE_CALENDAR_INCOMPLETE` × 1

### striker_nas100_mnq_dow_wed_excluded

- `BLOCKER` `TV_SUMMARY_MISMATCH` × 1
- `WARNING` `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` × 1
- `WARNING` `EARLY_CLOSE_CALENDAR_INCOMPLETE` × 1

### vanguard_mgc_v04

- `BLOCKER` `FORCE_FLAT_VIOLATION` × 226
- `BLOCKER` `TV_SUMMARY_MISMATCH` × 1
- `WARNING` `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` × 1
- `WARNING` `EARLY_CLOSE_CALENDAR_INCOMPLETE` × 1

## Independent TradingView summary reconciliation

G1.4 coverage: `NEEDS_CONTEXT`. Operator TradingView Key-stats are supplied for five active sources; independent total commissions and monthly net P&L have not been supplied. G1.4 remains partial; missing anchors are never inferred from exports or computed reports.

Observed max drawdown uses closed-trade exit equity; TradingView panel equity drawdown may differ. Discrepancies remain blockers; no series is repaired.

### aegis_6j1

Operator TradingView Key-stats transcribed by orchestrator in campaign-state section 10 at commit 716357e (origin/claude/orchestrator-role-takeover-yza7vp); panel span 2022-09-01 through 2026-09-02; DEEP backtest; Default detail (4 OHLC ticks); initial capital USD 100000 (inventory only, no rescaling).

| Metric | Observed | Anchor | Difference | Tolerance | Status |
|---|---|---|---|---|---|
| trade_count | 122 | 122 | 0 | 0 | MATCH |
| net_pnl_usd | 28702.75 | 28702.75 | 0.00 | 0.01 | MATCH |
| win_rate_pct | 63.9344262300 | 63.93 | 0.0044262300 | 0.01 | MATCH |
| profit_factor | 3.4827865095 | 3.483 | -0.0002134905 | 0.01 | MATCH |
| max_drawdown_usd | 1298.40 | 1470.40 | -172.00 | 0.01 | MISMATCH |
| total_commissions_usd | 4991.00 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd | {'2022-09': '50.45', '2022-10': '38.70', '2022-11': '-530.90', '2022-12': '25.20', '2023-01': '1056.70', '2023-02': '1062.90', '2023-03': '3163.50', '2023-04': '-1048.90', '2023-05': '1063.25', '2023-06': '0.30', '2023-07': '1882.10', '2023-08': '-749.75', '2023-09': '832.30', '2023-11': '1320.20', '2023-12': '-649.60', '2024-01': '-386.80', '2024-02': '1488.25', '2024-03': '0.40', '2024-04': '351.20', '2024-05': '-49.60', '2024-06': '776.10', '2024-07': '2033.10', '2024-08': '1075.65', '2024-09': '-474.55', '2024-11': '-180.30', '2024-12': '1944.80', '2025-02': '1064.15', '2025-03': '1132.40', '2025-04': '157.40', '2025-05': '1251.00', '2025-06': '1189.10', '2025-07': '-299.20', '2025-08': '1401.60', '2025-09': '-254.70', '2025-10': '1101.20', '2025-11': '2001.20', '2025-12': '951.60', '2026-01': '31.50', '2026-02': '-174.00', '2026-03': '4101.60', '2026-04': '1100.80', '2026-05': '-399.20', '2026-06': '-649.60', '2026-07': '-249.20', '2026-08': '1150.40'} | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-09 | 50.45 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-10 | 38.70 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-11 | -530.90 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-12 | 25.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-01 | 1056.70 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-02 | 1062.90 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-03 | 3163.50 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-04 | -1048.90 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-05 | 1063.25 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-06 | 0.30 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-07 | 1882.10 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-08 | -749.75 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-09 | 832.30 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-11 | 1320.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-12 | -649.60 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-01 | -386.80 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-02 | 1488.25 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-03 | 0.40 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-04 | 351.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-05 | -49.60 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-06 | 776.10 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-07 | 2033.10 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-08 | 1075.65 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-09 | -474.55 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-11 | -180.30 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-12 | 1944.80 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-02 | 1064.15 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-03 | 1132.40 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-04 | 157.40 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-05 | 1251.00 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-06 | 1189.10 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-07 | -299.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-08 | 1401.60 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-09 | -254.70 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-10 | 1101.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-11 | 2001.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-12 | 951.60 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-01 | 31.50 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-02 | -174.00 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-03 | 4101.60 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-04 | 1100.80 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-05 | -399.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-06 | -649.60 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-07 | -249.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-08 | 1150.40 | None | None | 0.01 | MISSING_ANCHOR |

### orb_mnq_recon_v7

Operator TradingView Key-stats transcribed by orchestrator in campaign-state section 10 at commit 716357e (origin/claude/orchestrator-role-takeover-yza7vp); panel span 2022-09-01 through 2026-09-02; DEEP backtest; Default detail (4 OHLC ticks); initial capital USD 100000 (inventory only, no rescaling).

| Metric | Observed | Anchor | Difference | Tolerance | Status |
|---|---|---|---|---|---|
| trade_count | 681 | 681 | 0 | 0 | MATCH |
| net_pnl_usd | 47533.16 | 47533.16 | 0.00 | 0.01 | MATCH |
| win_rate_pct | 56.8281938300 | 56.83 | -0.0018061700 | 0.01 | MATCH |
| profit_factor | 1.4347432725 | 1.435 | -0.0002567275 | 0.01 | MATCH |
| max_drawdown_usd | 6168.20 | 6794.02 | -625.82 | 0.01 | MISMATCH |
| total_commissions_usd | 2478.84 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd | {'2022-09': '-2404.80', '2022-10': '3254.56', '2022-11': '4568.84', '2022-12': '1486.12', '2023-01': '3902.44', '2023-02': '498.20', '2023-03': '1717.88', '2023-04': '283.20', '2023-05': '1389.36', '2023-06': '1935.04', '2023-07': '326.96', '2023-08': '115.32', '2023-09': '-244.68', '2023-10': '1087.84', '2023-11': '1303.32', '2023-12': '1587.04', '2024-01': '808.96', '2024-02': '636.32', '2024-03': '627.32', '2024-04': '332.68', '2024-05': '1042.96', '2024-06': '1701.32', '2024-07': '-323.68', '2024-08': '3710.40', '2024-09': '-717.68', '2024-10': '216.32', '2024-11': '924.60', '2024-12': '1755.04', '2025-01': '-458.04', '2025-02': '2875.88', '2025-03': '215.32', '2025-04': '6194.24', '2025-05': '2175.40', '2025-06': '-438.60', '2025-07': '149.60', '2025-08': '663.68', '2025-09': '626.04', '2025-10': '1216.32', '2025-11': '546.60', '2025-12': '-802.40', '2026-01': '445.60', '2026-02': '1799.60', '2026-03': '1452.32', '2026-04': '2592.04', '2026-05': '-1645.96', '2026-06': '310.68', '2026-07': '-3174.04', '2026-08': '586.32', '2026-09': '681.36'} | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-09 | -2404.80 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-10 | 3254.56 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-11 | 4568.84 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-12 | 1486.12 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-01 | 3902.44 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-02 | 498.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-03 | 1717.88 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-04 | 283.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-05 | 1389.36 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-06 | 1935.04 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-07 | 326.96 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-08 | 115.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-09 | -244.68 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-10 | 1087.84 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-11 | 1303.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-12 | 1587.04 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-01 | 808.96 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-02 | 636.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-03 | 627.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-04 | 332.68 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-05 | 1042.96 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-06 | 1701.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-07 | -323.68 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-08 | 3710.40 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-09 | -717.68 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-10 | 216.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-11 | 924.60 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-12 | 1755.04 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-01 | -458.04 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-02 | 2875.88 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-03 | 215.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-04 | 6194.24 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-05 | 2175.40 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-06 | -438.60 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-07 | 149.60 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-08 | 663.68 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-09 | 626.04 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-10 | 1216.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-11 | 546.60 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-12 | -802.40 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-01 | 445.60 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-02 | 1799.60 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-03 | 1452.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-04 | 2592.04 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-05 | -1645.96 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-06 | 310.68 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-07 | -3174.04 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-08 | 586.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-09 | 681.36 | None | None | 0.01 | MISSING_ANCHOR |

### striker_dj30_mym_pyramid_250

Operator TradingView Key-stats transcribed by orchestrator in campaign-state section 10 at commit 716357e (origin/claude/orchestrator-role-takeover-yza7vp); panel span 2022-09-01 through 2026-09-02; DEEP backtest; Default detail (4 OHLC ticks); initial capital USD 200000 (inventory only, no rescaling).

| Metric | Observed | Anchor | Difference | Tolerance | Status |
|---|---|---|---|---|---|
| trade_count | 203 | 203 | 0 | 0 | MATCH |
| net_pnl_usd | 31770.36 | 31770.36 | 0.00 | 0.01 | MATCH |
| win_rate_pct | 42.3645320200 | 42.36 | 0.0045320200 | 0.01 | MATCH |
| profit_factor | 1.6821573535 | 1.682 | 0.0001573535 | 0.01 | MATCH |
| max_drawdown_usd | 4262.66 | 4568.68 | -306.02 | 0.01 | MISMATCH |
| total_commissions_usd | 7647.64 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd | {'2022-09': '-10.66', '2022-10': '2976.90', '2022-11': '-1084.52', '2022-12': '-42.24', '2023-01': '-655.46', '2023-02': '-34.42', '2023-03': '5298.26', '2023-04': '1128.16', '2023-05': '-1447.16', '2023-06': '4062.66', '2023-07': '-47.30', '2023-08': '-1064.00', '2023-09': '3009.82', '2023-10': '-1139.50', '2023-11': '-755.64', '2023-12': '-328.68', '2024-01': '635.80', '2024-03': '3000.94', '2024-04': '-2013.12', '2024-05': '-1278.48', '2024-06': '392.80', '2024-07': '1639.94', '2024-08': '-775.04', '2024-09': '122.46', '2024-10': '-662.48', '2024-11': '-529.66', '2024-12': '3643.52', '2025-01': '134.20', '2025-02': '-2148.08', '2025-03': '107.14', '2025-04': '-409.58', '2025-05': '518.36', '2025-06': '5419.96', '2025-07': '1775.84', '2025-08': '-763.86', '2025-09': '-1359.12', '2025-10': '6229.82', '2025-11': '3743.46', '2025-12': '-1443.18', '2026-01': '2864.58', '2026-02': '4914.62', '2026-03': '-706.04', '2026-04': '1076.46', '2026-05': '85.20', '2026-06': '-513.20', '2026-07': '-610.12', '2026-08': '-463.52', '2026-09': '-725.48'} | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-09 | -10.66 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-10 | 2976.90 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-11 | -1084.52 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-12 | -42.24 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-01 | -655.46 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-02 | -34.42 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-03 | 5298.26 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-04 | 1128.16 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-05 | -1447.16 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-06 | 4062.66 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-07 | -47.30 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-08 | -1064.00 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-09 | 3009.82 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-10 | -1139.50 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-11 | -755.64 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-12 | -328.68 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-01 | 635.80 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-03 | 3000.94 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-04 | -2013.12 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-05 | -1278.48 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-06 | 392.80 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-07 | 1639.94 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-08 | -775.04 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-09 | 122.46 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-10 | -662.48 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-11 | -529.66 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-12 | 3643.52 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-01 | 134.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-02 | -2148.08 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-03 | 107.14 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-04 | -409.58 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-05 | 518.36 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-06 | 5419.96 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-07 | 1775.84 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-08 | -763.86 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-09 | -1359.12 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-10 | 6229.82 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-11 | 3743.46 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-12 | -1443.18 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-01 | 2864.58 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-02 | 4914.62 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-03 | -706.04 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-04 | 1076.46 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-05 | 85.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-06 | -513.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-07 | -610.12 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-08 | -463.52 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-09 | -725.48 | None | None | 0.01 | MISSING_ANCHOR |

### striker_nas100_mnq_dow_wed_excluded

Operator TradingView Key-stats transcribed by orchestrator in campaign-state section 10 at commit 716357e (origin/claude/orchestrator-role-takeover-yza7vp); panel span 2022-09-01 through 2026-09-02; DEEP backtest; Default detail (4 OHLC ticks); initial capital USD 200000 (inventory only, no rescaling).

| Metric | Observed | Anchor | Difference | Tolerance | Status |
|---|---|---|---|---|---|
| trade_count | 378 | 378 | 0 | 0 | MATCH |
| net_pnl_usd | 112253.42 | 112253.42 | 0.00 | 0.01 | MATCH |
| win_rate_pct | 54.4973545000 | 54.50 | -0.0026455000 | 0.01 | MATCH |
| profit_factor | 2.6038264920 | 2.604 | -0.0001735080 | 0.01 | MATCH |
| max_drawdown_usd | 8197.80 | 8269.62 | -71.82 | 0.01 | MISMATCH |
| total_commissions_usd | 5585.58 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd | {'2022-09': '-620.48', '2022-10': '-361.62', '2022-11': '-3063.38', '2022-12': '-108.76', '2023-01': '4869.64', '2023-02': '-2910.56', '2023-03': '-2241.12', '2023-04': '9353.40', '2023-05': '-1980.90', '2023-06': '17089.56', '2023-07': '8453.54', '2023-08': '-4305.00', '2023-09': '-3425.34', '2023-10': '6912.72', '2023-11': '393.80', '2023-12': '2233.52', '2024-01': '11169.78', '2024-02': '-907.56', '2024-03': '6069.16', '2024-04': '6958.32', '2024-05': '-1053.98', '2024-06': '17058.18', '2024-07': '-413.74', '2024-08': '11509.92', '2024-09': '-417.56', '2024-10': '5477.56', '2024-11': '2661.60', '2024-12': '-645.16', '2025-01': '-2684.02', '2025-02': '-1508.78', '2025-03': '272.52', '2025-04': '184.08', '2025-05': '7246.12', '2025-06': '-600.66', '2025-07': '891.56', '2025-08': '-843.20', '2025-09': '-648.34', '2025-10': '284.42', '2025-11': '-1024.76', '2025-12': '-1232.86', '2026-01': '1598.18', '2026-02': '-113.96', '2026-03': '-107.78', '2026-04': '11260.06', '2026-05': '2936.62', '2026-06': '691.94', '2026-07': '-183.74', '2026-08': '8229.12', '2026-09': '-148.64'} | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-09 | -620.48 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-10 | -361.62 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-11 | -3063.38 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-12 | -108.76 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-01 | 4869.64 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-02 | -2910.56 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-03 | -2241.12 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-04 | 9353.40 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-05 | -1980.90 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-06 | 17089.56 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-07 | 8453.54 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-08 | -4305.00 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-09 | -3425.34 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-10 | 6912.72 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-11 | 393.80 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-12 | 2233.52 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-01 | 11169.78 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-02 | -907.56 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-03 | 6069.16 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-04 | 6958.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-05 | -1053.98 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-06 | 17058.18 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-07 | -413.74 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-08 | 11509.92 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-09 | -417.56 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-10 | 5477.56 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-11 | 2661.60 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-12 | -645.16 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-01 | -2684.02 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-02 | -1508.78 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-03 | 272.52 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-04 | 184.08 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-05 | 7246.12 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-06 | -600.66 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-07 | 891.56 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-08 | -843.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-09 | -648.34 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-10 | 284.42 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-11 | -1024.76 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-12 | -1232.86 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-01 | 1598.18 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-02 | -113.96 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-03 | -107.78 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-04 | 11260.06 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-05 | 2936.62 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-06 | 691.94 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-07 | -183.74 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-08 | 8229.12 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-09 | -148.64 | None | None | 0.01 | MISSING_ANCHOR |

### vanguard_mgc_v04

Operator TradingView Key-stats transcribed by orchestrator in campaign-state section 10 at commit 716357e (origin/claude/orchestrator-role-takeover-yza7vp); panel span 2022-09-01 through 2026-09-02; DEEP backtest; Default detail (4 OHLC ticks); initial capital USD 100000 (inventory only, no rescaling).

| Metric | Observed | Anchor | Difference | Tolerance | Status |
|---|---|---|---|---|---|
| trade_count | 343 | 343 | 0 | 0 | MATCH |
| net_pnl_usd | 20388.04 | 20388.04 | 0.00 | 0.01 | MATCH |
| win_rate_pct | 50.1457725900 | 50.15 | -0.0042274100 | 0.01 | MATCH |
| profit_factor | 1.9653318334 | 1.965 | 0.0003318334 | 0.01 | MATCH |
| max_drawdown_usd | 1785.48 | 1847.60 | -62.12 | 0.01 | MISMATCH |
| total_commissions_usd | 1394.96 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd | {'2022-09': '-153.44', '2022-10': '202.08', '2022-11': '-289.44', '2022-12': '957.04', '2023-01': '-4.64', '2023-02': '-182.24', '2023-03': '133.36', '2023-04': '-183.44', '2023-05': '306.08', '2023-06': '-20.24', '2023-07': '-225.20', '2023-08': '330.32', '2023-09': '-120.48', '2023-10': '600.88', '2023-11': '-345.20', '2023-12': '24.32', '2024-01': '-145.20', '2024-02': '-131.20', '2024-03': '-252.72', '2024-04': '1099.12', '2024-05': '663.12', '2024-06': '169.28', '2024-07': '427.36', '2024-08': '291.60', '2024-09': '-221.92', '2024-10': '503.60', '2024-11': '-104.48', '2024-12': '-98.96', '2025-01': '-92.96', '2025-02': '288.32', '2025-03': '2490.16', '2025-04': '190.32', '2025-05': '1082.32', '2025-06': '-312.72', '2025-07': '-174.24', '2025-08': '865.60', '2025-09': '1185.12', '2025-10': '2055.72', '2025-11': '84.32', '2025-12': '-565.92', '2026-01': '6371.00', '2026-02': '2226.32', '2026-03': '-284.24', '2026-04': '1986.84', '2026-05': '207.28', '2026-06': '-206.48', '2026-07': '-1372.44', '2026-08': '1134.36'} | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-09 | -153.44 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-10 | 202.08 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-11 | -289.44 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2022-12 | 957.04 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-01 | -4.64 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-02 | -182.24 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-03 | 133.36 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-04 | -183.44 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-05 | 306.08 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-06 | -20.24 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-07 | -225.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-08 | 330.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-09 | -120.48 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-10 | 600.88 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-11 | -345.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2023-12 | 24.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-01 | -145.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-02 | -131.20 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-03 | -252.72 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-04 | 1099.12 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-05 | 663.12 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-06 | 169.28 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-07 | 427.36 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-08 | 291.60 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-09 | -221.92 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-10 | 503.60 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-11 | -104.48 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2024-12 | -98.96 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-01 | -92.96 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-02 | 288.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-03 | 2490.16 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-04 | 190.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-05 | 1082.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-06 | -312.72 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-07 | -174.24 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-08 | 865.60 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-09 | 1185.12 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-10 | 2055.72 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-11 | 84.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2025-12 | -565.92 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-01 | 6371.00 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-02 | 2226.32 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-03 | -284.24 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-04 | 1986.84 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-05 | 207.28 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-06 | -206.48 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-07 | -1372.44 | None | None | 0.01 | MISSING_ANCHOR |
| monthly_net_pnl_usd.2026-08 | 1134.36 | None | None | 0.01 | MISSING_ANCHOR |

## Reproduce

Provide the frozen source directory at runtime and run `python run_phase1.py --config phase1_config.json --source-dir <source-dir> --output-dir local_artifacts`.
