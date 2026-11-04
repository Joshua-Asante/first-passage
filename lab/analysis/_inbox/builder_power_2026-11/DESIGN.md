# Builder whole-stack power calibration: design (frozen before any run)

**Status:** frozen at the commit that adds this file, before any result-producing run.
Only an engineering timing probe ran first: it printed elapsed seconds, not gate outcomes.
**K = 0:** synthetic data only. No vendor CSV, private input or real strategy result is read.
**Authority:** the coordinator's commission of 2026-11-04 (gate-stack calibration). Lesson
M-49 asks this question: which gates can't fire or never bind before looks are spent.
**Engine:** `main` at `8745b40`. That includes #1054, under which 5g is post-holdout placement
(branch B), so the stack is 5a → 5b (applied, not a gate) → 5c → 5d → 5e → 5f → stage-8 look,
then 5g placement. The whole-stack pass set is the same in either 5g order; only kill
attribution differs.

## Question and decision it changes

What is the builder's whole-stack pass probability at a known true annual Sharpe, and which
gate binds at D9's windows? This decides whether a round's looks are worth spending (D7/D9),
and whether any gate is unreachable or never binds.

## Layers

**(a) Series layer (exact).** Per path, each session trades with probability *q*. A trade's net
P&L after the engine's own per-trade cost (Tradeify_Select_100K MNQ commission + 1 tick/side) is
`(μ + Z)·$100`, with Z a standardised payoff draw. μ solves the per-session Sharpe of the daily
series exactly (`harness.trade_mean`; zero on no-trade days, as `gates.daily` builds it). The
trades are `compile.Trade` objects and go through the real code: 5a (`THRESHOLDS`),
5c (`gates._halves`), 5f (`gates._dsr_gate`, each K), and `gates.holdout_look`, which runs
the pass rule and 5g placement. Only its two bar-reading calls are patched to return the
synthetic holdout trades; its ledger is real. 5d and 5e need bars and are not in this layer.

- Payoff shapes: `normal`, and `orb_skew` (a stopped −1 with p = 0.6, else 1.5·Exp(1), standardised).
- Book for 5g: per session active with p = 0.9, normal, annual Sharpe 1.0. It is tied to the
  card by a Gaussian copula with latent ρ.

**(b) Bar layer.** Synthetic 15m MNQ bars 09:30–16:45, a random walk with per-bar sd 10 points
on the 0.25 tick grid. After the first close outside the 09:30–10:00 range, each bar drifts *d*
points in the breakout direction. The card is a two-sided `first_n_bars` breakout,
n_bars = 2 (step 1), range_opposite stop, no target, entry cutoff 12:00, flat 15:45. It runs
through `gates.evaluate` (compile.py, 5a–5f including the 5d neighbours n_bars = 1, 3 and the
5e placebo) and `gates.holdout_look`.

The true Sharpe for each target is set by drift calibration, before any gate is evaluated, on
seeds separate from the evaluation seeds:

1. Estimate the card's net annual Sharpe at d ∈ {0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0} on 100,000
   sessions each (5 × 20,000, seed 20261106).
2. Interpolate linearly to each target.
3. Re-estimate at the chosen d on a fresh 100,000 sessions (seed 20261107). That
   re-estimate is the row's reported true Sharpe, with its standard error.

## Grid, paths and seeds

| | Series layer | Bar layer |
|---|---|---|
| True annual Sharpe | 0, 0.5, 0.85, 0.89, 1.0, 1.5 | 0, 0.85, 1.5 at n = 1,510; 0.85 at n = 2,350 |
| Development sessions n | 1,510 (7.5 y) and 2,350 (10.8 y) | as left |
| Holdout | 378 sessions, same process | 378 |
| K | 1, 2, 4 (5f on the same series) | 1, 2, 4 (evaluate at K = 1; 5f recomputed at 2 and 4) |
| Trade rate q | 0.15, 0.40, 0.85 | set by the card (about daily) |
| Payoff | normal, orb_skew | set by the bars |
| ρ (5g only) | 0 everywhere; 0.3 at q = 0.40, orb_skew | none (no book; 5g not in this layer) |
| Paths per cell | 2,000 (ρ = 0.3 cells: 1,000) | 200 |
| Seed | `SeedSequence([20261104, cell])` | `SeedSequence([20261105, cell])` |

The cell index is the row order `run_series.py` and `run_bar.py` enumerate.
Binomial SE is at most 0.011 per series cell and 0.035 per bar cell.

## Outputs

For each cell and K:

- whole-stack pass probability;
- each gate's first-fail kill share in engine order (series: 5a, 5c, 5f, holdout; bar: 5a, 5c,
  5d, 5e, 5f, holdout);
- each gate's standalone pass rate;
- P(5g clear | stack pass);
- the 5f closed form (`gates.reachability`'s normal approximation) beside the measured 5f rate.

The false-pass rate is the stack pass at true Sharpe 0.

## Criteria (fixed now)

- **V1, harness validity.** In the series layer, normal shape and q = 0.85, the measured
  standalone 5f rate is within 3 binomial SE + 0.02 of the closed form in every (S, n, K) cell.
  A miss means the harness, not the gate, is wrong; it is reported, and no result is quoted
  until it is fixed. Departures for other shapes and rates are findings, not failures.
- **V2, bar calibration.** Achieved true Sharpe within ±0.10 of target. A miss is reported, and
  the achieved value labels the row. Drift is never re-tuned after a gate result is seen.
- **Binds.** The gate with the largest kill share at S = 0.85 and 0.89, per (n, K).
- **Cannot fire.** Standalone fail rate < 1% at S = 0 in every cell where the gate is reached.
- **Never binds.** Kill share < 1% in every cell with S ≥ 0.85.
- **Unreachable.**
  - A gate: standalone pass < 0.50 at S = 0.89 in every cell.
  - The stack: whole-stack pass < 0.50 at S = 0.89, which is D7's "reachable" read across the
    whole stack.

## Where it runs

All of it runs in the cloud container through `python -I scripts/fp.py python …` with 4
processes. The estimate is under an hour; no VM run is needed for this grid. If a run exceeds 3
hours, it stops, and the remaining cells are packaged for the VM under the public-only rule. That
rule is pending, so the package is not run.

## Reading limits

- Synthetic processes have stationary edges and no regime change, so real cards will do worse
  in the 5c halves and the holdout.
- The series layer has no 5d or 5e, so its stack is an upper bound on the real stack.
- The bar layer has one card shape and one planted mechanism.
- No result here predicts any registered round.
