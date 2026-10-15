# Discovery tool discipline

Each tool below is a candidate generator. For each: what it produces, the K it
adds to the multiplicity burden, and the least-overfit default. None of these
outputs is a signal until it survives the gate on native micro-era data. All API
usage is left to the investigation — the discipline is what's fixed.

## STUMPY — matrix profile (motif / discord)

- **Produces:** repeated patterns (motifs) and anomalies (discords) via the matrix
  profile over subsequences of length `m`.
- **K:** roughly (number of subsequences) × (number of window lengths `m` tried).
  Every distinct `m` is a separate search. A discord is an anomaly *by
  construction* — its "surprise" is not evidence of edge.
- **Discipline:** pre-register the window-length set and the series scope as part of
  K. Prefer a small, principled set of `m` over a sweep. Use `scrump`/`stumpi` for
  scale, but the K accounting is unchanged. Route discords/motifs to the gate as
  observations, never entries.

## ruptures — change-point / regime segmentation

- **Produces:** break points partitioning a series into regimes (Pelt, binseg,
  window, kernel methods).
- **K:** the penalty (or `n_bkps`) is a researcher degree of freedom. A penalty
  *sweep* multiplies K by the grid size; reporting only the "best" segmentation
  hides that.
- **Discipline:** fix the penalty by a principled criterion, or pre-register the
  sweep grid as part of K. Change points are **conditioning variables** (regime
  labels feeding regime-consistency tests), not signals.

## tsfresh + catch22 / pycatch22 — feature extraction

- **Produces:** tsfresh extracts up to ~800 features with built-in FRESH
  hypothesis-test selection; catch22 is the 22-feature canonical, minimally-
  redundant subset.
- **K:** the feature count. tsfresh's FRESH FDR control is **per-run**, not
  program-level — selected features are already multiplicity-contaminated relative
  to your whole research program.
- **Discipline:** **catch22 first** (lower K, less overfit-prone). Escalate to full
  tsfresh only when catch22 is demonstrably insufficient, and carry the full
  feature count into K. A selected feature is a covariate, not a strategy.

## hmmlearn / pomegranate — HMM regime states

- **Produces:** latent state sequences (regime detection) to condition anomalies on
  market state.
- **K:** the number-of-states choice is a degree of freedom; selecting it by fit on
  the same data is overfitting. Declared K includes restart / seed / init
  attempts (HMM random inits). A re-run with a new seed is a new search
  increment, not a free peek.
- **Discipline:** choose state count by held-out likelihood or a pre-registered
  criterion, not in-sample fit. States are conditioning variables. **Filtered, not
  smoothed:** `predict` / `predict_proba` / `decode` run the forward–backward (or
  full-series Viterbi) pass, so each state label is informed by *future* bars — a
  smoothed posterior. Any label that conditions a real-time test or trade must use
  **filtered** (forward-only, information-up-to-t) probabilities, or a trailing
  realized-vol bucket; a full-sample decode is a look-ahead leak. Fit the HMM on IS
  only, never re-fit on the OOS era.

## gplearn / PySR — symbolic regression (highest snooping risk)

- **Produces:** closed-form expressions mapping features to a target. PySR is the
  stronger engine (multi-population search, Pareto front of complexity vs error);
  gplearn is the simpler scikit-style GP.
- **K:** effectively enormous and hard to bound — the expression space. This is the
  highest false-discovery risk in the stack.
- **Discipline:** pre-register the operator set, complexity ceiling, and
  population/generation budget as the (bounded) declared search. Declared K also
  includes restart / seed / init attempts (independent PySR / gplearn runs). A
  re-run with a new seed is a new search increment, not a free peek. Prefer
  expressions at the **knee** of the Pareto front — a complex expression that
  barely beats a simple one is overfit. Treat any survivor with maximum
  suspicion: it must clear the strictest OOS plus universe-level correction
  before it is anything but a curiosity.

## Pre-mining data hygiene (or you mine the artifact)

Before STUMPY / tsfresh / ruptures touch an intraday series, deseasonalize what the
market puts there for free — otherwise the scan rediscovers structure that is not an
edge:

- **Intraday volatility U-shape.** Volume and |return| follow a within-session U
  (open/close humps). Raw returns at different times of day are not comparable; a
  motif/feature that "fires at the open" is often just the vol hump in a costume.
  Normalize by the time-of-day vol curve before mining any time-of-day effect.
- **Bid-ask bounce.** Returns computed off *trade* prices carry spurious negative
  autocorrelation — the spread bouncing, not mean reversion. Use the prevailing
  top-of-book midpoint, not the trade print, for any short-horizon MR / reversal mining.

Provenance facts precede any statistic; unhandled, they silently poison the series:

- **Continuous-contract back-adjustment.** How a continuous series stitches across
  rolls changes what is true of it. Difference-adjustment preserves point moves but
  distorts price *levels* (they can go negative on deep history): percentage returns
  on it are wrong, and any *level*-based signal (round numbers, prior highs/lows, a
  fixed price band) tests phantom levels. Ratio-adjustment preserves returns but
  distorts point values ($-P&L per point is off). The roll date injects a jump whose
  timing is a convention, not the market's. An indicator may run on an adjusted series
  for continuity, but **entries, exits and P&L are evaluated on the tradeable
  contract's prices**, and any calendar-adjacent anomaly is checked against the roll
  schedule so you haven't discovered your own back-adjustment. Confirm the source's
  roll rule and whether it price-adjusts before a deep build; do not assume either.
- **The roll rule changes which bars exist, not just prices** (Q-TVCOV-1,
  2026-07-13) — "counts only, so roll is moot" is a trap. A calendar-rank front-month
  series maps CME currency futures to the near-dead monthly serial after each
  quarterly expiry (6J 2021-09: 335 covered NY-session 15m slots vs 734 actual) and
  parks equity-index micros on the dying contract over quarterly-roll Fridays. For any
  TradingView `1!` comparison or liquidity/coverage measurement, use a volume-rolled
  series — verified to match TV bar-for-bar
  ([`RESULTS.md`](../../../../lab/analysis/c1/tvcov_2026-07/RESULTS.md) §Roll-rule
  attribution).
- **Session & clock (CME Globex)** — the leading generators of fake time-of-day
  anomalies:
  - **RTH vs ETH.** Globex trades near-24h (ETH); an RTH-only hypothesis (e.g. the
    equity-index cash session) must be sliced to RTH explicitly — ETH bars are a
    different population.
  - **Session boundary: 17:00 America/Chicago.** A new trade date opens at 17:00 CT
    the prior calendar day, with a daily maintenance break. A "daily" bar is a Globex
    trade date, not a midnight-UTC day.
  - **DST.** A fixed UTC-hour filter shifts an exchange-local open by an hour twice a
    year; convert to America/Chicago DST-aware and spot-check the boundary weeks.
  - **Holiday half-sessions** (early closes) truncate the session — exclude or flag
    them, or a session-return statistic mixes full and half days.

These are the futures-microstructure counterpart of `strategy-validation`'s §1
Step-0 panel-integrity battery (which is TV/CFD-shaped). Rationale: field guide
`docs/methodology/references/statistics-of-tradable-anomalies.md` Domains 1, 7.

## The unifying rule

Discovery generates candidates and attaches K. It never blesses. Every output
above enters the Notice phase as an observation; only a K-registered candidate
that clears the first-pass multiplicity floor (`register_search.py close`) is
routed as an Inquire-phase falsifiable hypothesis, where `strategy-validation`
and `inqhiori` take over.
