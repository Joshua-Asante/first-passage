# Tradeify seven-strategy Phase 1 reconciliation

**Theme:** c1

**In-flight:** yes

**Status:** ACTIVE — strict seven-strategy Tradeify source, accounting, deadline, cap, and provenance normalization

> **EXPLORATORY — Phase 0 was skipped.** All supplied history is development data; this report is not confirmatory, qualified, admitted, or deployable.

Campaign status: `BLOCKED_EXPLORATORY`

Holiday-short verdict cap: `NEEDS_CONTEXT`

## Strategy inventory

| Strategy | Status | Rows | Trades | Net P&L | Daily-deadline holds | Fri→Sun sub-count |
|---|---|---:|---:|---:|---:|---:|
| aegis_6j1 | BLOCKED_EXPLORATORY | 244 | 122 | $28702.75 | 9 | 0 |
| orb_mnq_recon_v7 | BLOCKED_EXPLORATORY | 1362 | 681 | $47533.16 | 310 | 3 |
| striker_dj30_mym_v45 | BLOCKED_EXPLORATORY | 406 | 203 | $10208.62 | 0 | 0 |
| striker_dj30_mym_pyramid_down | BLOCKED_EXPLORATORY | 406 | 203 | $31770.36 | 0 | 0 |
| striker_nas100_mnq_v1 | BLOCKED_EXPLORATORY | 756 | 378 | $112253.42 | 0 | 0 |
| striker_nas100_mnq_native_variant | BLOCKED_EXPLORATORY | 368 | 184 | $170250.58 | 0 | 0 |
| vanguard_mgc_v04 | BLOCKED_EXPLORATORY | 686 | 343 | $20388.04 | 226 | 0 |

## Evidence boundaries

- The source CSV/Pine bytes, row-level event/trade/weekly ledgers, and seven detailed issue reports remain local and gitignored.
- No source row was repaired, dropped for an outcome, re-ranked, composed, simulated, or rerun in Pine.
- Scalar MAE/MFE values are inventory-only excursion bounds, not timestamped paths.
- Per-strategy caps are measured against 80 micro-equivalents; the joint book-cap verdict is deferred to Phase 4.
- CME holiday-short coverage is `NEEDS_CONTEXT`; no historical early-close date was inferred.

## Frozen hashes

- Config: `8881a2af5ab63cb7abec7028d22832ed647cfef10d484eba7d97515fcb0ea227`
- CME calendar capture: `a368dc61c55dd734930414bbc04caa6bc5c4759d078116e7594bff7a7ccbab85`
- Canonical events: `03efac85c4cf67ef9a577ec0844383015eed5d85a5b3239ec47a2c38643d84bf`
- Canonical trades: `900002b84762299273cdfe0dad75e5ab06324b884a22ef1f81e28fa8e3145105`
- Weekly exit blocks: `5bdcef07a717bf32b816c595cfbf6066e1f94a7ca9ad35e31b749bc8bc72cb0a`

## Verification evidence

- Evidence revision: `98e82b230bd63f8d922b76742d650f6e254a0002`; environment: Windows, Python 3.14.3.
- Focused Phase 1 and cost-model contract: `python -m pytest tests/test_tv_trade_ledger.py tests/test_trade_reconciliation.py tests/test_joint_trade_blocks.py tests/test_cost_model.py tests/test_tradeify_phase1_runner.py -q` — 123 passed.
- Unchanged production firm barriers: `python -m pytest tests/core/test_mc_intraday_barrier.py tests/core/test_trailing_dd_boundary.py tests/core/test_trailing_locking_boundary.py tests/core/test_mc_preflight.py -q` — 59 passed.

## Issues by strategy

### aegis_6j1

- `BLOCKER` `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` × 1
- `BLOCKER` `FORCE_FLAT_VIOLATION` × 9
- `WARNING` `EARLY_CLOSE_CALENDAR_INCOMPLETE` × 1
- `WARNING` `PINE_EXPORT_COMMISSION_MISMATCH` × 1
- `WARNING` `PINE_VENUE_COMMISSION_MISMATCH` × 1

### orb_mnq_recon_v7

- `BLOCKER` `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` × 1
- `BLOCKER` `FORCE_FLAT_VIOLATION` × 310
- `WARNING` `CROSS_DATE_HOLD` × 3
- `WARNING` `EARLY_CLOSE_CALENDAR_INCOMPLETE` × 1

### striker_dj30_mym_v45

- `BLOCKER` `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` × 1
- `WARNING` `EARLY_CLOSE_CALENDAR_INCOMPLETE` × 1

### striker_dj30_mym_pyramid_down

- `BLOCKER` `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` × 1
- `WARNING` `EARLY_CLOSE_CALENDAR_INCOMPLETE` × 1

### striker_nas100_mnq_v1

- `BLOCKER` `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` × 1
- `WARNING` `EARLY_CLOSE_CALENDAR_INCOMPLETE` × 1

### striker_nas100_mnq_native_variant

- `BLOCKER` `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` × 1
- `WARNING` `EARLY_CLOSE_CALENDAR_INCOMPLETE` × 1

### vanguard_mgc_v04

- `BLOCKER` `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` × 1
- `BLOCKER` `FORCE_FLAT_VIOLATION` × 226
- `WARNING` `EARLY_CLOSE_CALENDAR_INCOMPLETE` × 1

## Reproduce

Provide the frozen source directory at runtime and run `python run_phase1.py --config phase1_config.json --source-dir <source-dir> --output-dir local_artifacts`.
