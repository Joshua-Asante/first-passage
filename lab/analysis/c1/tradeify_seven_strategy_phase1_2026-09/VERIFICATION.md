# Phase 1 verification evidence

This evidence is separate from generated `RESULTS.md`, so reproducing the campaign cannot erase it.

- Evidence revision: `c24eac0a279716ae16d9c8a17d06f256eb5395e8` (after the required merge of current `origin/main`)
- Environment: Windows, Python 3.14.3
- Focused Phase 1 and cost-model contract: `python -m pytest tests/test_tv_trade_ledger.py tests/test_trade_reconciliation.py tests/test_joint_trade_blocks.py tests/test_cost_model.py tests/test_tradeify_phase1_runner.py -q` — exit 0; 125 passed.
- Unchanged production firm barriers: `python -m pytest tests/core/test_mc_intraday_barrier.py tests/core/test_trailing_dd_boundary.py tests/core/test_trailing_locking_boundary.py tests/core/test_mc_preflight.py -q` — exit 0; 59 passed.
- Full repository suite: `python -m pytest -q` — exit 0; 2,284 passed, 34 skipped, 6 subtests passed, 23 warnings.

All pytest runs used a temporary root outside the repository. The warnings were dependency deprecations and explicit stale-gate notices; no test failed.
