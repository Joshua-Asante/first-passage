# 5e placebo diagnostic, T1 and T2: results

One-liner: research input only (K = 0, synthetic). On identical paths and identical entry-bar
draws, production 5e (which keeps each trade's realised side) passes 3 of 400 paths both at zero
drift and at a card net annual Sharpe of 1.53. Replacing only the side rule with a causal side or a
coin lifts the pass rate to 0.72–0.998. The generator still carries a fill artefact (V2 miss), but
it favours the card, so it cannot explain production's failures.

> **Correction, 2026-11-04 (review on PR #1072).** Where this file says the failure comes "from the side
> rule, not the generator" and that the fill artefact "cannot explain" production's failures (the
> one-liner and the first two Reading bullets), read instead: **strong side-rule sensitivity on this
> generator; generator-independent attribution remains untested.** The matched intervention holds
> this generator fixed, so it isolates the side-rule contrast within it. It does not rule out an
> interaction between the generator's path and fill assumptions (V2 missed; the card fills at
> crossed levels while every placebo fills at bar opens) and the realised-side statistic, and it
> does not show how the contrast transfers to #1067's generator or to a fill-consistent zero-edge
> generator, which was not measured. The original wording below is kept as written (Rule 30); the
> design, runner, harness and `results.json` are unchanged.

- **Design:** [DESIGN.md](DESIGN.md), frozen at `c0314c1` (sha256 `7b805c02…`) before any run.
- **Engine:** `main` `dfcfcb1`, engine sha256 `10f0eb19…` (in `results.json` `meta`). Production code
  is unchanged.
- **Run:** cloud container, `python -I scripts/fp.py python …/run.py`, Python 3.13.18, 4 processes,
  335 s. The first attempt raised at its final JSON write (a numpy bool) before any output was
  saved or read. The fix (`bool()` casts only, commit after `c0314c1`) re-ran the same frozen
  seeds.
- **Data:** synthetic only.

## Validity

- **V1 passes.** The harness's `realised` share equals production `gates.placebo_beaten_share`
  on every one of the 800 paths.
- **V2 misses.** At zero drift the card's gross annual Sharpe is **1.00** (SE 0.05), and its net
  Sharpe is 0.35 on 100,000 sessions (0.42 mean per path).
  - Cause: one-minute steps (sd 2.58 points) jump past the stop levels, while `compile.py`
    fills at the level. The card keeps the overshoot: about 1.5 points, or 6 MNQ ticks, per
    crossing (Siegmund's 0.58·σ), on entries and on stop exits.
  - Path-consistent minute bars therefore did **not** remove the fill artefact, contrary to the
    design's premise. They only changed its source: #1067's came from short wicks, this one from
    step size.
  - Following the design, the zero-drift row is labelled by its achieved values and is **not a
    zero-edge null**.
- **V3 passes.** Drift 0.236 gives a verified net annual Sharpe of 1.48 (fresh 100,000 sessions)
  and 1.53 mean per path.

## Results (400 paths per cell, 1,000 development sessions, about 996 trades per path)

Pass means beaten share ≥ 0.95. The intervals are Wilson 95%.

| Cell (achieved) | Side rule | Pass | Rate (95% CI) | Mean share | Share 10 / 50 / 90% |
|---|---|---|---|---|---|
| zero drift (gross 1.00, net 0.42) | **realised (production)** | 3 | **0.008** (0.003–0.022) | 0.21 | 0.00 / 0.12 / 0.58 |
| | causal | 372 | 0.930 (0.901–0.951) | 0.98 | 0.96 / 1.00 / 1.00 |
| | coin | 289 | 0.723 (0.677–0.764) | 0.94 | 0.85 / 0.99 / 1.00 |
| S = 1.5 (net 1.53) | **realised (production)** | 3 | **0.008** (0.003–0.022) | 0.28 | 0.02 / 0.21 / 0.70 |
| | causal | 396 | 0.990 (0.975–0.996) | 1.00 | 0.99 / 1.00 / 1.00 |
| | coin | 399 | 0.998 (0.986–1.000) | 1.00 | 1.00 / 1.00 / 1.00 |

## Against the frozen hypotheses

- **H1, mechanically "supported":** the Wilson upper bound is 0.022, below 0.05. The premise
  failed (V2), so this is not the zero-edge null test the design intended. What it does show is
  stronger: a card with a real net Sharpe of 0.42 passes production 5e 0.8% of the time.
- **H2a, contradicted:** at zero drift the `causal` and `coin` pass rates are 0.93 and 0.72, not
  about 5%. The reason is V2: the card has a fill-sourced edge (gross 1.00), and a placebo that
  enters at bar opens cannot match it. The zero-drift cell does not test a null.
- **H2b, supported:** at S = 1.5, `causal` (0.990) and `coin` (0.998) exceed production (0.008)
  by 0.98 and 0.99, against the pre-stated 0.25.

## Reading

- **The production failure comes from the side rule, not the generator.** Paths, entry-bar draws,
  holds and costs are identical; only the side changes. Production passes 0.8% at net Sharpe
  0.42 and again at 1.53. Its beaten-share distribution barely moves when the edge rises from
  0.42 to 1.53 (median 0.12 to 0.21), which is the look-ahead signature: a breakout's direction
  is set by the move that later draws ride.
- **The generator's fill artefact favours the card.** If anything it lifts production's rate. So
  it cannot explain #1067's 0/127 or the 3/400 here.
- **A second finding concerns any replacement.** At zero drift, `causal` and `coin` pass a card
  whose only edge is the fill model, because the card fills at levels while the placebo fills at
  bar opens. A redesigned 5e would need the placebo to share the card's fill model, or it
  rewards execution assumptions instead of timing. That needs a generator that passes V2 (finer
  steps, or fills at the first traded price beyond the level) before any replacement is judged.

## Reading limits

- One card shape, one mechanism, stationary Gaussian minutes. The V2 miss means no zero-edge cell
  was measured. Real MCL bars (fat tails, gaps, rolls) may change magnitudes.
- The diagnostic side rules are harness-only. Neither is proposed as production 5e.
- T3 and T4 were not run (not authorized). No gate, threshold or verdict changes here.
