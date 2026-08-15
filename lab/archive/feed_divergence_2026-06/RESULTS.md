# Q-FEED-1 feed divergence — RESULTS

**Verdict: CLOSED — RESOLVED-BY-RETIREMENT. Q-FEED-1's cross-feed transfer-validity question dissolved with the Dukascopy feed ([docs/adr/2026-06-17-dukascopy-retirement.md](lab/archive/../../docs/adr/2026-06-17-dukascopy-retirement.md)); the byte-reading paths here are banner-marked non-runnable as of 2026-07-22, ahead of substrate-retirement disposition B.**

FROZEN-CONVENTION: name=tv_open_utc shift_minutes=0 week1_matches=1384 week1_fx_p95=0.0700

Window: 2026-03-01 00:00:00+00:00 → 2026-06-01 00:00:00+00:00

## Decomposition table

| symbol | class | matched | duka_eligible | coverage | p95(|Δclose|)/ATR14 | idx_residual_p95 |
|---|---|---:|---:|---:|---:|---:|
| USDJPY | FX | 6179 | 6195 | 99.74% | 0.0971 |  |
| GBPUSD | FX | 6175 | 6175 | 100.00% | 0.1161 |  |
| US30 | IDX | 5682 | 5687 | 99.91% | 0.7957 | 0.1514 |

## Unmatched census (summary)

- **USDJPY**: duka_only=16, tv_only=1
- **GBPUSD**: duka_only=0, tv_only=21
- **US30**: duka_only=5, tv_only=250
