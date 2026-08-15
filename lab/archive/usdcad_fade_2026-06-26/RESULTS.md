# USDCAD up-spike-fade — RESULTS

**Date:** 2026-06-26 · **Operator:** Joshua · **Engine:** Claude (Opus 4.8), brainstorming → strategy-validation
**Pre-reg:** [`PREREG-USDCAD-FADE-2026-06-26.md`](../../docs/ltm/briefs/pre-registration/PREREG-USDCAD-FADE-2026-06-26.md) (FROZEN before any strategy PnL).
**Data:** `BAR_EXPORT_v0.1_PEPPERSTONE_USDCAD_2026-06-26_422ca.csv` — 15m USDCAD, Pepperstone/TV,
**150,261 bars, 2020-06-11 → 2026-06-25 (~6 years, multi-regime)**. This is the panel the
2026-06-14 NULL closure named as its **sole reopener** ("a multi-year, multi-regime panel … to
test the up-fade asymmetry OOS, esp. a CAD-strength regime").
**Endpoint (operator-chosen):** FXIFY-compliant candidate Pine + verdict; on NULL ship Pine + record.

## Verdict: NULL — the up-fade asymmetry is REAL but SUB-COST and REGIME-FRAGILE.

The reopener panel **confirms the 2026-06-14 NULL rather than overturning it.** Fading USDCAD
up-spikes is directionally genuine (it beats fading down-spikes, corroborating durable #8 on 6
years), but the edge is ~0.03R/trade — far below the cost-law hurdle — and it lives entirely in
the 2023-26 trend regime, going **negative in the 2021 CAD-strength regime** that was the whole
point of the OOS test. "Real ≠ tradeable."

## Step-0 (panel integrity) — PASS

150,261 bars decoded, 0 decode/dup/backwards/OHLC failures, 99.8% 15m-contiguous, 7 calendar
years. **UTC→ET decode verified:** bar-range peaks at ET 10:00 (14.25p), NY-morning ≈1.86× overnight
(durable #8). Weekend gaps are DST-aware holiday opens. (`step0_fade.py`.)

## Frozen grid (8 configs) — short-only up-fade, NY 08-11, volfloor ON

| N | k | tp | n | exp (R) | PF | WR | net R | 4× hurdle | hurdle? |
|--|--|--|--|--|--|--|--|--|--|
| 24 | 2.5 | 1.0 | 782 | −0.0240 | 0.948 | .503 | −18.7 | 0.192 | fail |
| 24 | 2.5 | 1.5 | 775 | −0.0253 | 0.951 | .437 | −19.6 | 0.192 | fail |
| 24 | 3.0 | 1.0 | 755 | −0.0345 | 0.921 | .493 | −26.1 | 0.160 | fail |
| 24 | 3.0 | 1.5 | 747 | −0.0171 | 0.963 | .454 | −12.8 | 0.160 | fail |
| 48 | 2.5 | 1.0 | 679 | +0.0126 | 1.029 | .526 | +8.6 | 0.192 | fail |
| 48 | 2.5 | 1.5 | 674 | +0.0174 | 1.036 | .458 | +11.8 | 0.192 | fail |
| 48 | 3.0 | 1.0 | 659 | +0.0090 | 1.022 | .520 | +5.9 | 0.160 | fail |
| **48** | **3.0** | **1.5** | **652** | **+0.0302** | **1.069** | **.475** | **+19.7** | **0.160** | **fail** |

Selected (best full-panel exp): **N48 / k3.0 / tp1.5, +0.0302R**. Every config is sub-hurdle.

## Gates (frozen §6)

| Gate | Result | Detail |
|---|---|---|
| **G1 cost-hurdle** | **FAIL** | +0.0302R vs required 4× = 0.160R. Cost-sensitivity: +0.0302 @0.8p → +0.0141 @1.2p → **−0.0020 @1.6p**. The cost law (durable #1) is the binding constraint, again. |
| **G2 DSR > 0.95** | **FAIL** | DSR = 0.437. Best-of-8 per-trade SR 0.0298 is **below** E[max SR \| null] 0.0360 — within selection noise. |
| **G3 regime / OOS** | **FAIL** | both-halves same-sign TRUE (H1 +0.0151 / H2 +0.0444), but **walk-forward fails**: H1→H2 OOS +0.0444R (sub-hurdle); **H2→H1 OOS = −0.0388R** (a trend-tuned config loses on 2020-23). |
| **G5 asymmetry** | PASS | up-fade +0.0302 > down-fade −0.0264 > symmetric −0.0019. The asymmetry is real. |
| G4 best-of-N (conf.) | PASS | P(null ≥ obs) = 0.033 (B=30) — beats random entry. Real, not tradeable. |
| G6 stationarity (conf.) | FAIL | thirds [−0.0052, +0.0510, +0.0449] — first third (2020-22) negative. Drop-top-k all positive (not concentration). |

**OVERALL = NULL** (primary gates G1/G2/G3 fail).

## Per-year (selected config) — the smoking gun

| year | n | exp (R) | note |
|--|--|--|--|
| 2020 | 44 | +0.0056 | ≈0 |
| **2021** | 106 | **−0.0402** | **CAD-strength oil rally — the OOS regime the reopener targeted; edge inverts** |
| 2022 | 113 | +0.0177 | USD-hiking |
| 2023 | 118 | +0.0944 | trend |
| 2024 | 126 | +0.0529 | BoC-Fed divergence |
| 2025 | 100 | +0.0442 | trend |
| 2026 | 45 | −0.0116 | recent |

The edge is a **2023-25 trend-regime artifact**. In 2021 (CAD strength) it is the worst year. This is
the regime/directional-graveyard pattern exactly: an OHLC-threshold edge that separates the regimes
it was implicitly fit on, and inverts in the held-out one. The pooled full-panel +0.0302R **masks**
the split (Q-DDTRIG-1 / graveyard lesson — partition INSIDE the test).

## What this confirms (and what would change it)

- **Confirms** the 2026-06-14 NULL on its own named reopener. The 15m USDCAD price-action space is
  exhausted across regimes, not just on one window. Durable #8's up-fade asymmetry is **genuine but
  sub-cost** — it joins durable #2 (no raw directional edge) and the closed reversion null.
- **Graveyard lesson reproduced** (7→8 deaths): revival requires an **exogenous** signal (CA-US rate
  differential — cf. the one USDCAD concept that PASSED, Sovereign/RDM-001 — or WTI/oil), never a
  re-tuned OHLC level. A pure-bars fade cannot be rescued by parameter choice (the grid is the grid).
- **Would change the verdict:** an exogenous CAD-strength regime gate that contemporaneously flags the
  2021-type regime and stands down the fade there — tested as a SINGLE pre-specified cut, not mined.
  That is a new mechanism (rate-diff / oil), not a new parameter, and belongs in the SVRN/RDM lane.

## Native-TV confirmation (2026-06-26 — `UCAD-FADE` export, 494 trades)

The candidate Pine was run in TradingView's Strategy Tester on the Pepperstone USDCAD chart
(2020-03 → 2026-06 — note TV reaches back ~3 months further than the bar export, **including the
COVID crash**). The native arbiter **confirms the NULL**:

| | native TV (event-avoid ON, %-risk, FXIFY halts) | Python pre-filter (event-OFF, fixed-R) |
|--|--|--|
| N | 494 | 652 |
| headline | **+$2,045 = +1.02% over 6.3 yr** · PF 1.046 · WR 48.0% · maxDD 2.51% · RF 0.40 | +0.0302R · PF 1.069 |
| 2021 (CAD-strength) | **−0.19% · PF 0.967** | **−0.0402R** |

Both arbiters agree on the verdict: **PF ≈ 1.05, economically flat (~0.16%/yr), sub-cost; 2021
negative.** The cross-check ties out to the cent (sum of Exit Net $+2045.28 vs TV cumulative
$+2045.26 → Exit-only parse correct, no double-count). The per-year *attribution* differs (native:
strong **2020-COVID +1.85% / PF 1.557**, negative 2022-24; Python: strong 2023-25 trend) for two
reasons: (a) the Pine's **event-avoidance removes the NY-morning event bars** where the post-2022
trades clustered, and (b) TV includes the **COVID-2020 high-vol spike-revert** window the bar export
lacked. That a single config toggle (skip the 10:00 bar) **flips individual-year signs** is itself the
signature of a marginal non-edge — a real edge survives it. FXIFY rails behaved correctly: drawdown
never approached the 4% halt and profit never reached +5%, so no halt fired. Script: `reconcile_tv.py`.

## Artifacts (this directory)

`step0_fade.py` · `run_fade.py` (reuses the audited `../usdcad_reverse_2026-06-14/usdcad_harness.py`
+ `dsr.py`) · `usdcad_fade_v0_1.pine` (FXIFY-compliant candidate, **OUT-OF-EVIDENCE-BASE**, compiles
clean via `scripts/pine_check.py`) · `reconcile_tv.py` (native-TV confirmation parser). No `core/`
touch, no lock/allocation/dd_protection change; locked anchor 99.83/0.17/4.37 stands.

**Forbidden-move audit (§7):** no §3 grid / §5 metric / §6 gate / cost central / split-boundary was
moved after the first PnL number. **Was any criterion moved after data arrived? NO.**
