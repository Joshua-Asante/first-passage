**Theme:** legacy
# COMPLEMENT-XAUUSD-CGB-001 — zero-build kill-test RESULTS

**Date:** 2026-06-15 · **Feed:** canonical Pepperstone TV CSV (`Guardian_Gold_v5.5_PEPPERSTONE_XAUUSD_2026-05-24_1bb97.csv`, N=203) · **Harness:** [`excursion_counterfactual.py`](excursion_counterfactual.py) (self-test verified; 3-agent adversarial verification) · **No `core/` touch.**

## Disposition: AMBIGUOUS (brief §6) / operational HOLD — build NOT triggered

Per the operator's pre-committed rule ("canonical kill-tests first; build the Pine only if those clear"), the tests did **not** clear: the concept is neither RESOLVED nor decisively FALSIFIED. Build deferred. This supersedes the brief's unverified §2.1 Alchemy "precomputation" (no on-disk artifact; non-canonical divergent feed).

## Why this test exists

The CC-handoff brief claimed a §2.1 excursion counterfactual had "already been run" on an Alchemy XAUUSD export and folded its conclusions in. That export + analysis have **no on-disk artifact** anywhere (repo or main checkout), and Alchemy is a documented-divergent, non-canonical feed (N-2026-05-29). Per Rule 0 + the strategy-validation test-ordering principle, this reproduces the cheapest kill-test on **canonical** data before any build.

## Method (excursion-bounded counterfactual)

Guardian is long-only. TV per-trade excursion columns bound a same-bar SHORT: `short FE = |long AE|`, `short AE = long FE`, both censored at Guardian's own exit. R de-compounds via `excursion_USD / (0.34% × equity_before)`. Bucketed per (stop S, target T) into WIN/LOSS/AMBIGUOUS/SCRATCH. Cost-in-R = round-trip cost / stopDist, where stopDist (=1R) = `(0.34%×equity_before)/size_qty`.

## Results (canonical, N=203)

| Quantity | Value | Read |
|---|---|---|
| Guardian long mean / median / WR | +2.033R / **−1.008R** / 22.17% | 1R pin validated (median = LOCK basis); WR = LOCK exactly |
| **Naive Guardian-inverse** (own exits) | **−2.086R/trade** (1× cost) | ☠️ **FALSIFIED** — inverting a PF-3.75 trend-rider loses by construction |
| Stop-disciplined short S=T=1R | **[worst −0.206, best +0.385]R**; **mid +0.089R** | straddles zero; **mid < 4× hurdle 0.211R** |
| categories @ S=T=1R | win 78 / loss 57 / **ambiguous 60** / scratch 8 | 30% path-unknown — the entire positive lean is ambiguous-optimism |
| Targets T ≥ 1.5R | win=0, ambiguous=0 (all S); **max short FE = 1.40R** | 🔒 **censored** — 0/203 trades reach FE ≥ 1.5R |
| Cost-law median cost_R | 0.053R @ $0.30 RT · 0.088R @ $0.50 · 0.123R @ $0.70 | **benign** (below the brief's 0.10R kill line at realistic cost) |

## Three load-bearing conclusions

1. **Naive Guardian-inverse: dead.** −2.09R/trade. A short complement must have its own compression-gated timing + tight stop, not a Guardian inverse. (Ledger D1.)
2. **The cheap test is the WRONG instrument for the proposed design.** The brief wants a *trailing trend-short letting declines RUN past 1R*. That payoff is **100% in the censored region** — 0 of 203 trades show a short FE ≥ 1.5R, because Guardian's long stop ends the trade (and the excursion window) at ≈−1R. The test gives **zero** information about the proposed strategy. Only a bar-level backtest can resolve it.
3. **The only *observable* proxy (a 1R scalp short) is economically marginal.** Realistic mid-case (ambiguous split 50/50) = **+0.089R, below the 4× cost hurdle of 0.211R**. Clearing the hurdle needs a 70.6% ambiguous-win-rate (no evidence for above-coin-flip). So the testable proxy fails its own economic gate; the positive "best" bound is ambiguous-optimism + a thin 8-trade scratch tail.

**Net:** not killed (the trailing thesis is untested, not disproven; cost is benign), not resolved (proxy uneconomic; proposed design unobserved). → **AMBIGUOUS / HOLD.**

## Adversarial verification (3 independent agents, 2026-06-15)

- **Code-correctness** — AGREE. Re-derived all 4 computations from raw CSV; every committed number reproduces exactly. No sign flip / off-by-one / censoring / boundary error. Found 1 MINOR bug (naive double-counted cost 2×→1×; **fixed**, −2.139→−2.086, immaterial) + 1 NOTE (scratch payoff slightly optimistic but verdict robust to scratch=0 / scratch=−S).
- **Independent recompute** — AGREE. Own csv-stdlib harness reproduced every figure within rounding; confirmed max short FE = 1.40R (censoring real).
- **Verdict stress-test** — overturned the draft "BUILD-REQUIRED" label with 2 BLOCKERs (design-test mismatch; mid-case below 4× hurdle) → **HOLD**. Accepted.

## What remains alive (per §6 AMBIGUOUS discipline)

- DEAD: the naive Guardian-inverse (D1).
- MARGINAL: a ≤1R-scalp short (mid-case below cost hurdle; not the intended design).
- UNTESTED: the compression-gated **trailing trend-short** — the actual proposal — resolvable only by a bar-level backtest on Dukascopy/Pepperstone bars.

## Recommendation

**HOLD the build.** If revisited, open a fresh brief with criteria fixed up front (per §6 AMBIGUOUS), testing the trailing design on **bars** (the only instrument that can see past the 1R censoring point), and **sequence it behind the 2026-08-08 regime check** — the shared go/no-go for the complement thesis already carrying USOIL-RGC + Guardian Silver. Do not build a scalp variant (uneconomic). Broker-verify the live XAUUSD round-trip cost before any future cost gate (OQ1).
