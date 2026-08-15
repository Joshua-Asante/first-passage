# `avg_block_length` Selection Justification — EURUSD Pattern-Enumeration Harness

**Date:** 2026-05-22
**Phase:** 2 (executing Reality-Check Harness ADR §2.2 lock template, `avg_block_length` field)
**Chosen value:** `avg_block_length = 21`
**Selection rule applied:** rule-of-thumb `floor(T^(1/3))` — after the brief-nominated primary rule and the §0.5 Q7 HALT protocol surfaced a 48× primary/secondary disagreement that was resolved by Joshua (CEO) selecting option (i) of four enumerated dispositions.

---

## 1. Selection rule used

Per CC handoff brief §0.5 Q2, three rules were computed:

| Rule | Definition | Value |
|---|---|---|
| (a) Primary — Bartlett-band first ACF crossing | smallest k ≥ 1 where \|ACF(k)\| < 2/√T | **2** |
| (b) Secondary — PACF max significant lag | largest k ≥ 1 where \|PACF(k)\| > 2/√T | **96** |
| (c) Rule-of-thumb — Politis-White-2009 default | floor(T^(1/3)) | **21** ← **chosen** |

The brief §0.5 Q7 HALT protocol fired (primary/secondary disagreement of 96/2 = **48×**, far exceeding the 3× threshold). Per brief §5.5, the selection cannot be made by minimizing test-failure rate or any results-based optimization, so the disposition was surfaced to Joshua. Joshua selected option (i) — adopt rule-of-thumb = 21 — on the methodological grounds described in §3 below.

---

## 2. Computation inputs

| Input | Value |
|---|---|
| IS window | **2018-01-01 → 2023-12-31** (per ADR §2.1 partition; filter predicate `(time ≥ 2018-01-01) & (time < 2024-01-01)`) |
| Bar source | `data/bar_data/EURUSD_H4.csv` (SHA-256 `9f3fc76520fe2d5b697907ff7b2e6d6382b23c0ef7d60a6c060a872f908cb782`) |
| Granularity | H4 (per ADR §5 Q-H3 baked decision) |
| Bars in IS window | 9,337 |
| Returns series | `np.diff(np.log(close))` — log returns per ADR §2.3 stationary-input sub-contract |
| n_returns (T) | **9,336** |
| max_lag | 100 (per brief §0.5 Q3) |
| Bartlett band | ±2/√T = **±0.020699** |
| PACF method | Yule-Walker modified (statsmodels `method="ywm"`) |
| ACF method | FFT-based (statsmodels `fft=True`) |

Computation script: [scripts/acf_analysis.py](scripts/acf_analysis.py).
Raw outputs: [diagnostics/eurusd_h4_acf.json](diagnostics/eurusd_h4_acf.json).

---

## 3. Result + comparison table + rationale

**Chosen:** `avg_block_length = 21`.

### Comparison table

| Rule | Value | In [2, 200] sanity bound? | Reasoning for selection-or-not |
|---|---|---|---|
| Bartlett first crossing (primary) | 2 | ✓ | Sensitive: ACF(1)=-0.0208 just outside band (Δ ≈ 0.0001 from boundary), ACF(2)=-0.0040 well inside. Tiny perturbation flips the answer to 1 or 3. Not robust. |
| PACF max significant lag (secondary) | 96 | ✓ | In the noise tail: 8 significant PACF lags in 1..100 (~5 expected under H0); PACF(96)=+0.026 is one of the deepest-lag random sigs. No structural meaning. |
| **Rule-of-thumb floor(T^(1/3))** | **21** | ✓ | **Chosen.** Conventional automatic for near-i.i.d. series at this T; insensitive to per-lag noise; corresponds to ~3-4 trading days of H4 dependence; harness conftest defaults to 20 (very close, suggesting the design assumption already anticipated this scale). |

### Structural picture

EUR_USD H4 log returns over the IS window are **approximately uncorrelated**, consistent with weak-form market efficiency on liquid FX majors:

- 8 significant ACF lags in 1..100 (expected ~5 under H0 → marginal excess, no clean AR structure)
- 8 significant PACF lags in 1..100 (same picture)
- Strongest near-zero ACF lags: lag 1 (-0.0208, just outside band), lag 3 (-0.0354), lag 6 (+0.0216)

For a near-i.i.d. series, "first ACF crossing" is dominated by where exactly the few small ACF values fall relative to the band boundary — an unstable selection criterion. "PACF max significant" is dominated by the deepest noise-tail false positive — a meaningless selection criterion in this regime. Neither rule meaningfully extracts dependence structure when there isn't much to extract.

The rule-of-thumb T^(1/3) is the Politis-White-2009 automatic for the asymptotic-MSE-optimal block length under no-strong-structure conditions. For T=9,336 it returns 21, corresponding to ~3-4 trading days of H4 bars — a defensible block-of-dependence horizon for the stationary block bootstrap on an FX log-return series of this length.

---

## 4. Plot

![ACF/PACF EUR_USD H4 IS log returns](diagnostics/eurusd_h4_acf.png)

ACF (top) and PACF (bottom) for the 9,336 EUR_USD H4 log returns in the IS window. Bartlett band ±0.0207 shaded. Red dashed verticals mark the primary rule's first crossing (lag 2 on ACF) and the secondary rule's max significant lag (lag 96 on PACF).

---

## 5. Literature anchor

- **Politis, D. N. and Romano, J. P. (1994).** "The Stationary Bootstrap." *Journal of the American Statistical Association*, 89(428), 1303-1313. Defines the stationary block bootstrap with geometric-distributed block lengths (mean = `avg_block_length`); preserves stationarity by construction. Component E (`harness/bootstrap.py`) implements this paper directly.
- **Politis, D. N. and White, H. (2004).** "Automatic Block-Length Selection for the Dependent Bootstrap." *Econometric Reviews*, 23(1), 53-70. Establishes the MSE-optimal block-length selection framework; T^(1/3) is the asymptotic rate this paper's procedures converge to under conditions matching near-i.i.d. financial returns. The rule-of-thumb is the standard fallback when the more sophisticated automatic procedures aren't invoked (deferred in brief §0.5 Q2 to avoid adding the `arch` package dependency).

---

## 6. Disposition if revisited

Phase 3 should reject this `avg_block_length` and require a re-run if any of the following changes:

1. **Re-fetch of `data/bar_data/EURUSD_H4.csv` produces a materially different ACF structure.** If a future fetch produces n_returns ± 5% of 9,336 but the ACF/PACF significant-lag count meaningfully changes (e.g., 8 → 20+ significant lags), the near-i.i.d. premise underlying the rule-of-thumb selection is invalidated; restart Phase 2 with the new data.
2. **The IS window changes** (e.g., shortened, lengthened, or boundaries shifted). T determines the rule-of-thumb output directly via T^(1/3), and a shifted window may produce a different structural picture.
3. **The timeframe locks to something other than H4.** ADR §5 Q-H3 locks H4 for this Pre-Q; if a future Pre-Q opens at 1H or 1D, that Pre-Q runs its own Phase 2.
4. **The bootstrap method changes.** This `avg_block_length` is calibrated to Politis-Romano stationary block bootstrap (Component E). If the method changes (e.g., to circular block bootstrap or moving-block bootstrap), recompute appropriately.
5. **The 8-vs-5 marginal excess of significant ACF lags is shown to be a load-bearing structural signal.** Currently treated as scatter; if a Phase 4 enumeration result hinges on dependence at lag 3 or lag 6 specifically, the rule-of-thumb selection may have over-smoothed and Phase 2 should be re-run with explicit AR-order modeling (out of scope for this Pre-Q).

Disposition cases that do NOT invalidate this selection:
- Phase 4 enumeration produces a pattern with high in-sample PF that fails OOS gate. That's the gate working as designed (per Pre-Q §6 FALSIFIED verdict); the block length is not on trial.
- Round-trip sanity test (Step 2.8) reveals attenuation outside the brief's heuristic tolerance window. Per brief §2.8 gate, this returns `DONE_WITH_CONCERNS` and is surfaced for parent review, not a silent re-pick.
