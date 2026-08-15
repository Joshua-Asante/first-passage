# Custodian-EURUSD v0.1 — mechanism-probe verdict: **CLOSED / SHELVED (probe not completed)**

**Concept:** `custodian-eurusd-v0.1` — month-end equity-hedging rebalancing flow on
EURUSD (the Melvin–Prins equity-hedging channel): when US equities outperform
Eurozone equities over the concluding month, benchmark-tracking managers become
under-hedged in USD and must sell USD / buy EUR into the last London 4 p.m.
WM/Reuters fix → EURUSD up, forecastable ex ante from the period's relative equity
returns.
**Date:** 2026-06-10. **Status:** SHELVED (soft, reversible).

## Disposition

The pre-registered mechanism-probe regression **never ran.** The Dukascopy m15 fetch
(2016–2026; EURUSD + S&P 500 + EuroStoxx 50) hung on closed-hour 503-retry latency
before any panel finished — so there is **no `gate_result.json`, no `monthly_frame.csv`,
and no β / t / p / n result.**

In its place, a hand-authored Pine strategy
(`core/strategies/candidates/custodian-eurusd-v0.1.pine`, gitignored) implementing the
same logic was backtested **manually on TradingView and underperformed** (operator read,
2026-06-10). On that basis the concept is **shelved for now.**

This is a **manual-test rejection, NOT a completed formal falsifier** — the pre-registered
KILL criterion below was never evaluated on data.

## Pre-registered KILL criterion (never evaluated — recorded for the re-proposal bar)

OLS `y ~ const + x` (HC3-robust). **RESOLVED** iff `β>0 ∧ p<0.05 ∧ n≥90`; **FALSIFIED**
iff `p≥0.05 ∨ β≤0` (a significant **negative** β is FALSIFIED, not a pass);
**AMBIGUOUS-HOLD** iff right sign with `0.05≤p<0.10` or `n<90`.

* `y` = `close[16:00 London] / open[12:00 London] − 1` on the last trading day.
* `x` = `[SPX(T-1)/SPX(prevME) − 1] − [ESTX50(T-1)/ESTX50(prevME) − 1]` (local ccy, through T-1).

## What survives (independent of this concept's fate)

* EuroStoxx-50 Dukascopy feed discovered + verified: **`EUSIDXEUR` / point_factor 1e3**
  (re-confirmed by a 3-month smoke fetch: mid-2024 ≈ 5040).
* `gate.py` is built and correct (causal-lag asserted, sign-discipline, HC3 OLS, DST
  spot-check) — runnable as-is if a faster index-close feed is dropped in (the gate needs
  only ~2 daily closes/month for SPX + EStoxx).
* Codification capability-boundary finding: `compose_from_hint` only codifies
  intraday-technical / single-instrument / long-only archetypes; this calendar-flow /
  cross-instrument / two-sided concept needs a primitive-library extension.

## Re-proposal bar

A **completed mechanism probe** (the regression that never ran) **or genuinely new
mechanism evidence** — NOT Pine parameter tweaks, a different fix-window, or a wider
sweep. Logged to `docs/rejected_candidates.md` (composite key `custodian-family × EURUSD`).
