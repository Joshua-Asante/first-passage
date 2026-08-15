# Fixing-reversal cost pre-screen — RESULTS (2026-06-22)

**Verdict: FAIL-COST** (best-of-grid break-even 0.277 pip vs FXIFY all-in 0.80 pip).

**Scope:** scouting cost pre-screen on the canonical Pepperstone 5m EURUSD feed. Claims NO edge — measures whether the London-fix fade can clear FXIFY cost. Long EURUSD entered at the fix bar's close (fade the pre-fix USD strength), protective stop, time-exit. Rule is fixed/representative, NOT optimized.

**Coverage:** 2020-06-22 → 2026-06-12, 1550 fix-days used, 316 skipped (no fix bar).


## Per-cell (hold × stop) — gross, no cost

`breakeven_spread_pips` = the gross post-fix edge expressed as the all-in cost (pips) it can absorb before mean net R goes ≤ 0. Above FXIFY's all-in cost ⇒ survives.


| hold (min) | stop (pip) | n | mean gross R | win% | stop-out% | break-even cost (pip) |
|---:|---:|---:|---:|---:|---:|---:|
| 15 | 5 | 1550 | +0.0455 | 44.5 | 37.7 | 0.227 |
| 15 | 10 | 1550 | +0.0095 | 49.0 | 12.0 | 0.095 |
| 15 | 20 | 1550 | +0.0037 | 49.5 | 1.3 | 0.075 |
| 30 | 5 | 1550 | +0.0555 | 39.8 | 50.1 | 0.277 |
| 30 | 10 | 1550 | +0.0050 | 48.2 | 22.3 | 0.050 |
| 30 | 20 | 1550 | +0.0025 | 49.9 | 3.9 | 0.050 |
| 60 | 5 | 1550 | +0.0279 | 33.7 | 60.8 | 0.140 |
| 60 | 10 | 1550 | -0.0093 | 45.3 | 34.5 | -0.093 |
| 60 | 20 | 1550 | -0.0047 | 49.0 | 8.1 | -0.094 |

## Net mean R by all-in cost (the paper's cost-geometry wall)

Each entry = mean net R at that all-in round-trip cost (spread + commission, pips).

| hold/stop | 0.0p | 0.2p | 0.4p | 0.6p | 0.8p | 1.0p |
|---|---|---|---|---|---|---|
| 15m/5p | +0.045 | +0.005 | -0.035 | -0.075 | -0.115 | -0.155 |
| 15m/10p | +0.010 | -0.010 | -0.030 | -0.050 | -0.070 | -0.090 |
| 15m/20p | +0.004 | -0.006 | -0.016 | -0.026 | -0.036 | -0.046 |
| 30m/5p | +0.055 | +0.015 | -0.025 | -0.065 | -0.105 | -0.145 |
| 30m/10p | +0.005 | -0.015 | -0.035 | -0.055 | -0.075 | -0.095 |
| 30m/20p | +0.002 | -0.008 | -0.018 | -0.028 | -0.038 | -0.048 |
| 60m/5p | +0.028 | -0.012 | -0.052 | -0.092 | -0.132 | -0.172 |
| 60m/10p | -0.009 | -0.029 | -0.049 | -0.069 | -0.089 | -0.109 |
| 60m/20p | -0.005 | -0.015 | -0.025 | -0.035 | -0.045 | -0.055 |

## Read

- Even the most favorable grid cell breaks even only at 0.277 pip all-in, **below** FXIFY's ~0.80 pip → the London-fix fade does **not** clear retail cost on EURUSD. This **confirms the paper** (edge negative at full retail spread). 5th-leg slot stays empty on this mechanism; pivot effort to T2 (regime-adaptive sizing).

**Caveats:** scouting-only until re-confirmed under a feed-equivalence pre-flight (a fix-timestamp signal is acutely feed-sensitive). `--fxify-cost` is a parameter — set it from the real FXIFY/DXTrade EURUSD round-trip cost; the break-even column is robust to that choice. The (hold × stop) grid is reported in full to avoid best-cell selection.
