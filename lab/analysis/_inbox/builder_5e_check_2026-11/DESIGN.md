# 5e placebo diagnostic, T1 and T2: design (frozen before any run)

**Status:** frozen at the commit that adds this file, before any result-producing run. Before it,
only engineering checks ran: the V1 unit test in `test_harness.py` (equality, no gate outcome
printed) and a timing probe that printed elapsed seconds (0.8 s per path, 15 s per 20,000-session
chunk).

**Authority:** Joshua, 2026-11-04 05:29:32 UTC, relayed as RELAY-BUILDER-5E-20261104-2: "I authorize the
synthetic checks", for T1 and T2 only (T3 and T4 are not authorized).

**K = 0:** synthetic data only. No market data, private input, holdout, ledgered look, trading,
threshold change or production-code change. Production code is called, never edited.

**Engine:** `main` `dfcfcb1`, engine sha256 `10f0eb19f302533ffc3ad56f8e06f76734d011ab4a851488e767b41bd4cfa363`.
The 5e code (`gates.placebo_beaten_share`) and `compile.py` are unchanged since `8745b40`, the
engine PR #1067 ran on.

**Budget (Rule 2):** one run, at most 3,600 s wall on 4 processes (the runner stops adding paths at
that limit and reports partial cells), one write-up. $0.

## Question and decision it changes

Is #1067's 0 passes of 5e at true Sharpe 1.52 produced by the production placebo (it keeps each
trade's realised side, which for a breakout card is chosen by the move that follows earlier draws)
or by #1067's generator (short-wick bars whose stop fills start in profit)? This decides whether
5e needs a gate decision (change, or report-only, for cards whose side is set by their entry
trigger) before R1 freezes.

## Generator (path-consistent; fixes #1067's V2 artefact)

- Each 15m bar, 09:30–16:45 ET on weekdays, is the open, high, low and close of 15 one-minute
  steps of a Gaussian walk with per-minute sd 10/√15 points (per-bar sd 10, as #1067). Prices
  are rounded to the 0.25 grid after the path is built.
- Planted edge: from the bar after the first 15m close outside the 09:30–10:00 range, every
  minute drifts `d`/15 points in the breakout's direction. At `d` = 0 there is no edge.
- Under a continuous martingale path a stop filled at its level starts at zero expected profit,
  so the card's gross expectation at `d` = 0 is zero except for 0.25-tick rounding. V2 checks it.

## Card, costs and fills (unchanged production)

- The card is #1067's: MNQ two-sided `first_n_bars` breakout, n_bars = 2, stop entries one
  tick beyond the range, range-opposite stop, no target, entry cutoff 12:00, flat 15:45.
- Trades come from `compile.days` + `compile.simulate_day`, as `gates.evaluate` builds them.
- Costs: `Costs.for_firm("Tradeify_Select_100K", "MNQ")`, i.e. firm commission plus 1 tick per
  side (`THRESHOLDS["5b_slippage_ticks_per_side"]`). The placebo charges the same per trade.

## Statistics

The 5e statistic is the share of placebo runs whose net total is below the card's net total;
pass is ≥ `THRESHOLDS["5e_min_beaten_share"]` (0.95). There are `THRESHOLDS["5e_placebo_runs"]`
runs (1,000), with seed `THRESHOLDS["5e_seed"]`.

- **Production (T1):** `gates.placebo_beaten_share`, called unchanged.
- **Diagnostic side rules (T2)** run on exactly the same entry-bar and hold draws (same RNG
  stream). Only the side changes:
  - `realised`: the trade's realised side. This equals production, checked as V1.
  - `causal`: +1 if the drawn bar opens above the range midpoint, −1 if below, coin on a tie.
    This is known at the drawn bar's open, so there is no look-ahead.
  - `coin`: a fair coin.

  Coins and ties come from a separate generator, `SeedSequence([20261111, cell, path])`, so they
  never perturb the shared draws. The diagnostic side rules are harness-only and are not
  candidate gate definitions.

## Grid, paths and seeds

| Cell | Drift | Development sessions | Paths |
|---|---|---|---|
| 0 `zero_drift` (T1; T2 null) | 0 | 1,000 | 400 |
| 1 `S1.5` (T2 high signal) | calibrated to card net annual Sharpe 1.5 | 1,000 | 400 |

- **Calibration (before any gate is evaluated, on seeds separate from the paths):**
  - the card's net and gross annual Sharpe at `d` ∈ {0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0}, each
    on 5 × 20,000 sessions with seed 20261108;
  - linear interpolation of the net value to 1.5;
  - re-estimation at the chosen `d` on a fresh 100,000 sessions with seed 20261109.

  The drift is never re-tuned after a 5e result is seen.
- **Paths:** `SeedSequence([20261110, cell, path])`.
- **Uncertainty:** each cell's pass rate gets a Wilson 95% interval. With 400 paths, binomial SE
  is about 0.011 at a rate of 0.05.

## Validity checks

- **V1:** `realised` equals the production beaten share exactly on every path. A miss voids T2.
- **V2:** at `d` = 0, the card's gross annual Sharpe on 100,000 sessions is within ±0.10 of 0
  (the fill-consistency check #1067 missed). A miss is reported and labels the row.
- **V3:** the achieved net annual Sharpe at the chosen drift is within ±0.10 of 1.5. A miss is
  reported, and the achieved value labels the row.

## Hypotheses, stated before the run (not targets; outcomes are reported whatever they are)

- **H1 (T1):** at zero drift on path-consistent bars, production 5e passes far less often than a
  valid null's nominal 5%. *Supported* if the Wilson 95% upper bound of the pass rate is below
  0.05. *Contradicted* if the interval contains 0.05 or lies above it.
- **H2a (T2, null):** with the `causal` or the `coin` side, the zero-drift pass rate's Wilson 95%
  interval contains 0.05.
- **H2b (T2, high signal):** at S = 1.5, the `causal` and `coin` pass rates each exceed the
  production (`realised`) pass rate by at least 0.25 absolute.

Reported alongside: each cell's mean and 10/50/90% quantiles of the beaten share per side rule,
mean trades, and mean per-path net annual Sharpe.

## Reading limits

- One card shape (two-sided ORB), one planted mechanism (post-breakout drift), stationary Gaussian
  minutes. Real MCL bars have fat tails, regimes, gaps and roll effects, so magnitudes do not
  transfer. The test separates the gate's mechanism from #1067's fill artefact; it does not
  predict R1.
- The `causal` midpoint rule is one choice of causal side, picked for this diagnostic. It is not a
  proposal for production 5e.
- T3 (the before/after-entry split) and T4 (a card whose side is fixed before entry) are not run.
