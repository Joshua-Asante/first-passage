# Q-MNQSEL-2 — cheap falsifier log (parent-side, pre-PREREG)

**Date:** 2026-08-08  
**Panel:** `~/.databento_cache/ohlcv-1m_continuous_b1fa4ae6b7ba9af2.dbn` (`MNQ.v.0`)  
**sha256:** `0d37054ee4375a6c60f7f2646a9b82547cae247c39a8c5dcbe209a149fedd7c5`  
**Rebuild:** `_mnq_1m.parquet` (gitignored) · 2,556,165 rows · 2019-05-06 → 2026-08-05

| Check | Result |
|---|---|
| RTH 1m clocks on 2024-06-12 | **390** (in [350, 400]) |
| Clean-target R at G=10, RT=1.41 | **0.859** = (10−1.41)/10 |
| Stop R at G=10 | **−1.141** = (−10−1.41)/10 |

**Verdict:** `CHEAP_FALSIFIER_OK` — licenses brief + PREREG authoring; not a Phase-0 path-PnL result.
