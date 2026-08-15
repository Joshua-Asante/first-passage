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
  the same data is overfitting.
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
  population/generation budget as the (bounded) declared search. Prefer expressions
  at the **knee** of the Pareto front — a complex expression that barely beats a
  simple one is overfit. Treat any survivor with maximum suspicion: it must clear
  the strictest OOS plus universe-level correction before it is anything but a
  curiosity.

## Pre-mining data hygiene (or you mine the artifact)

Before STUMPY / tsfresh / ruptures touch an intraday series, deseasonalize what the
market puts there for free — otherwise the scan rediscovers structure that is not an
edge:

- **Intraday volatility U-shape.** Volume and |return| follow a within-session U
  (open/close humps). Raw returns at different times of day are not comparable; a
  motif/feature that "fires at the open" is often just the vol hump in a costume.
  Normalize by the time-of-day vol curve before mining any time-of-day effect.
- **Bid-ask bounce.** Returns computed off *trade* prices carry spurious negative
  autocorrelation — the spread bouncing, not mean reversion. Use midpoints (`mbp-1`
  or the `tbbo` quote) for any short-horizon MR / reversal mining.
- **Back-adjustment + session/clock provenance** are data-semantics facts that
  precede mining — they live with the data layer: `databento-data`
  `reference/schemas-and-symbology.md` §Data hygiene (continuous-contract adjustment,
  RTH/ETH, DST, the Globex session boundary). A level-based motif on a
  difference-adjusted series is mining phantom levels.

These are the futures-microstructure counterpart of `strategy-validation`'s §1
Step-0 panel-integrity battery (which is TV/CFD-shaped). Rationale: field guide
`docs/methodology/references/statistics-of-tradable-anomalies.md` Domains 1, 7.

## The unifying rule

Discovery generates candidates and attaches K. It never blesses. Every output
above enters the Notice phase as an observation; only a K-registered candidate
that clears the first-pass multiplicity floor (`register_search.py close`) is
promoted to an Inquire-phase falsifiable hypothesis, where `strategy-validation`
and `inqhiori` take over.
