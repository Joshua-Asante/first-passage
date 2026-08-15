# Regime-signal deep research — verified findings (2026-06-25)

**Question.** A free / TradingView-exportable **exogenous** signal to flag the 2020–2023
low-trend "chop" regime, to drive **regime-adaptive position sizing** (priority) and
possibly seed a **5th leg** (secondary). Binding constraint: **orthogonal to realized-vol /
gap / opening-range** — the wall that killed VIX, VVIX, MOVE, VIX term-structure, and GEX
(each collapsed to a vol/gap proxy and flagged CRISIS, not the low-vol 2021 CHOP).

**Method.** deep-research workflow `wf_86c1c04c-7f0` (107 agents, ~6.3M tokens; 6 angles →
24 sources → 88 claims → 25 adversarially verified, **19 confirmed / 6 killed**). Raw output
archived at the session tasks dir (`wbnlmgota.output`).

---

## Ranked candidates

### 1. Implied correlation / dispersion (COR3M, COR1M, DSPX) — best mechanism, WORST orthogonality
- **Mechanism (high conf, unanimous primary sources):** the wedge between index vol and
  average single-stock vol. High dispersion / low implied correlation = "stock-picker's
  market" = a rangebound index while constituents diverge. Mechanistically the
  directionless-vs-trending axis we want — *not* a calm-vs-volatile gauge.
- **Orthogonality: UNCERTAIN → unfavorable.** DSPX = `sqrt(VIX² − VIXEQ²)`, built FROM VIX
  inputs; raw level co-moves positively with VIX. **Three** orthogonality-positive claims were
  REFUTED (0-3): S&P DJI's "orthogonal-in-construction" marketing; that dispersion forecasts
  future realized vol; the DSPX/VIX synchronicity red-flag. **Raw level risks a GEX-style
  collapse.** A usable signal needs a **vol-residualized or ratio form** (DSPX/VIX, or regress
  out VIX), and the chop side is **LOW correlation / HIGH dispersion** (inverting CBOE's own
  HIGH-correlation = crisis headline).
- **Pre-reg test:** residualize COR3M/DSPX on contemporaneous realized-vol + |gap|; does the
  residual flag 2021 low-vol chop distinctly from 2020/2022 crisis (|t| ≥ 2)?

### 2. Hurst exponent — orthogonal BY CONSTRUCTION, but derived + fragile
- **Mechanism:** scalar; H<0.5 mean-reverting / ≈0.5 random / >0.5 trending. Scale-invariant
  to increment variance → **definitionally vol-orthogonal**.
- **Caveats:** estimation-fragile (>~215 points to resolve ΔH=0.1); **MUST be computed on log
  RETURNS, not prices** — our own lesson (`feedback_hurst_rs_log_prices_trap`), which the
  research independently reproduced. Not a data pull — computed in-house from our own bars.
- **Pre-reg test:** rolling Hurst on each leg's 15m log-returns; is mean(H) lower in chop than
  trend with real separation, and ~uncorrelated with realized vol?

### 3. Breadth / advance-decline (S5FI, S5TH, ADD) — distinct by construction, empirically UNTESTED
- **Mechanism:** participation, not magnitude. Breadth divergence / mid-range churn flags
  rangebound / distribution regimes.
- **Caveat:** definitional distinctness ≠ empirical orthogonality (exactly the GEX trap).
  Breadth also *collapses* in crashes → the chop-specific part is the **mid-range churn /
  divergence**, not the absolute level.
- **Pre-reg test:** S5FI (50-DMA) level and the S5FI−S5TH (50 vs 200-DMA) divergence; partial
  against realized-vol + |gap|; does it separate the 2020–2023 chop?

### 4. TSMOM / CTA factor (SG Trend Indicator; DBMF/KMLM proxies) — chop-native but highest leakage
- TSMOM bleeds in chop, but this carries the **highest endogenous-echo risk** (a lagged echo
  of our own trend P&L). Free reconstruction only ≈0.75-correlates to the real series, and the
  chop-vs-vol attribution claim was REFUTED (1-2). **Lowest priority.**

---

## Binding meta-constraint (load-bearing)
Regime-classification **accuracy** is the gate (Dacco & Satchell 1999, J. Forecasting): even a
*true* regime model loses to a random walk under small misclassification. **Qualifier that
saves our use case:** this is strongest for point *forecasts* of the level — **risk-targeting /
SIZING uses can add value despite imperfect detection.** So the **sizing** application is the
defensible framing; a 5th-leg (forecasting) use faces the harsher bar.

---

## Data list — (A) Claude-fetchable vs (B) only-Joshua

**Category A — I can fetch myself:**
- **DSPX daily 2014→2026** — CBOE CDN CSV, unauthenticated, verified live:
  `https://cdn.cboe.com/api/global/us_indices/daily_prices/DSPX_History.csv`.
  ⚠ pre-2023 values are **likely BACKFILLED** (DSPX launched Sep-2023; Joshua's TV export
  starts 2023-09 = the live launch, which *confirms* the CDN's pre-2023 history is
  reconstructed → look-ahead risk for any strict-vintage / live-tradeable claim).
- **Vol-class controls** (VIXCLS, T10Y3M, BAMLH0A0HYM2, NFCI, EBP, OFRFSI) — FRED/ALFRED,
  point-in-time vintages (free key). For **residualization controls**, not the primary signal.
- **Sector-SPDR closes** (XLK…XLC) — free (stooq/public) → compute **realized** dispersion /
  correlation with **full 2020 history**, closing the COR3M coverage gap.

**Category B — ONLY Joshua (TradingView) — the genuinely load-bearing pulls:**
- **Implied CORRELATION — COR3M / COR1M.** ✅ **COR3M SUPPLIED** (2021-05→). COR1M optional
  (adds a term-structure dimension).
- **Breadth — S5FI / S5TH / ADD.** ✅ **S5FI SUPPLIED** (2020-01→, full H1 coverage).
  S5TH (200-DMA) optional, for the 50-vs-200 divergence form.

**Verdict.** The two decisive Category-B families (**correlation + breadth**) are **already in
hand**. DSPX turned out to be Claude-fetchable (and Joshua's DSPX export is still useful — it
dates the live launch and flags the CDN backfill). **No further Joshua pull is strictly
load-bearing**; marginal nice-to-haves are COR1M and S5TH.

---

## Coverage scorecard (data on disk, `core/data/external/`)
| Signal | Family | Cadence | Coverage | H1 chop testable? |
|---|---|---|---|---|
| S5FI | breadth | daily | 2020-01 → now | ✅ full |
| COR3M | implied correlation | 15m | 2021-05 → now | ⚠️ partial (misses 2020) |
| DSPX | dispersion | 15m (TV) / daily (CDN) | 2023-09 (TV) / 2014 backfilled (CDN) | ❌ TV H2-only; CDN look-ahead-risky |

Realized dispersion from sector ETFs (Category-A) is the workhorse for full-2020 coverage of
the correlation/dispersion mechanism; COR3M/DSPX are the *implied* cross-check where they overlap.

---

## Open questions the verification could NOT settle
1. Does a **vol-residualized / ratio** form of DSPX/COR3M actually flag 2020–2023 low-vol chop
   distinctly from crisis on a point-in-time basis — or still collapse to a vol proxy? (the
   decisive pre-registered test)
2. Are the pre-2023 CBOE-CDN DSPX values live-published or back-calculated? (look-ahead)
3. Is a free EOD COR3M/COR1M full history obtainable (CDN analogue), or only via TV export?
4. Which breadth tickers survive an *empirical* orthogonality test, not just the definitional one?

---

## Proposed next step
Pre-register + run the **orthogonality battery** — the crux the research left open. For each
candidate: partial-correlation / residual-t after partialling **realized-vol + |gap|** on the
4-leg 15m bars, evaluated **on the 2020–2023 chop window specifically**, using vol-residualized
forms for COR/DSPX. **Gate = |t| ≥ 2 after partialling** (the same gate that killed GEX).
Survivors → sizing-map design → decompounded re-MC against the H1 tail. Frame as **sizing**, not
forecasting (per the Dacco-Satchell qualifier).
