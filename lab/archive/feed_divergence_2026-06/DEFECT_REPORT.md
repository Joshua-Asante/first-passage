# Q-FEED-1-D1 — Convention calibration misalignment (code defect)

**Date:** 2026-06-12  
**Route:** `FALSIFIED (FX)` → `code-defect-debugging` (brief §4)  
**Status:** fixed in pipeline; re-measurement below

## Symptom

First Phase 3–4 run: coverage 99.5–99.9% but p95(|Δclose|)/ATR14 ≈ 1.37–1.42 (FX) with
frozen convention `tv_close_as_open` (shift −15 min). Gates: `FALSIFIED (FX)`.

## Root cause

BAR EXPORT v0.1 **Signal** field carries `epoch_ms` = **bar-open UTC** (verified:
`1772402400000` → 2026-03-01 22:00 UTC matches Entry Date/Time).

Applying `shift_minutes=-15` before M15 floor **joins each Dukascopy bar to the
previous TV bar's OHLCV**. Match count rises by only 2 / 1384 in week 1, but
|Δclose|/ATR14 jumps from ~0.10 to ~1.4.

| GBPUSD | shift=0 | shift=-15 |
|---|---:|---:|
| coverage | 100.00% | 99.81% |
| p95/ATR | **0.116** | 1.424 |

Same pattern on USDJPY (0.097 vs 1.376) and US30 residual (0.151 vs 1.486).

## Fix

1. Removed `tv_close_as_open` (−15) from `CONVENTION_CANDIDATES` — invalid when
   `epoch_ms` is authoritative.
2. Week-1 tie-break: among candidates within 5 matches of the leader, prefer lower
   mean FX week-1 p95/ATR (still week-1-only; not full-window shopping).

## Re-measurement (shift=0, post-fix)

Frozen convention: `tv_open_utc`, shift=0.

| Symbol | coverage | p95/ATR | Gate |
|---|---:|---:|---|
| USDJPY | 99.74% | 0.097 | FX ACCEPT |
| GBPUSD | 100.00% | 0.116 | FX AMBIGUOUS (0.10–0.25) |
| US30 | 99.91% | 0.796 raw / **0.151 residual** | IDX AMBIGUOUS (0.15–0.40) |

**Overall: `AMBIGUOUS-HOLD`** — not `FALSIFIED (FX)`. Prior falsified verdict was
artifact of the −15 min misalignment, not feed divergence.

ADR 2026-06-12: hold on conservative (split) side per pre-registration; no FX-leg
revocation. One re-test on extended window due by 2026-07-15 if still ambiguous.
