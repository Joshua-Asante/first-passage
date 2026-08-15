# Skew probe — Q-GEOFIT-1 successor scoping (2026-07-25)

**Status:** scoping probe. **Not** part of Q-GEOFIT-1, which is CLOSED `AMBIGUOUS-PARAMETERIZATION`. Produces no envelope, no grid, no cells, no candidate claim. **$0.00 spend, zero K.**
**Verdict:** `SKEW-CONFIRMED (dominant) / SUFFICIENCY-UNRESOLVED (underpowered)`
**Driver:** [`run_skew_probe.py`](run_skew_probe.py) (pre-declaration in its module docstring, fixed before any arm ran) · data [`probe.json`](probe.json) · log [`probe.log`](probe.log)

## Question

Q-GEOFIT-1 found that `(σ_d, μ/σ, shape, z)` mis-predicts the real c1 bust by 23.63pp at an exact parameter match, and diagnosed the cause as the family's missing skew / loss-tail dimension. Is that diagnosis right?

Reference: real c1, $100K basis, corrected geometry → **4.7433%**. Tolerance ±0.5pp (inherited from Q-GEOFIT-1 §2). Frozen engine (10k × seeds 42/123/2026, horizon 1500, Run-2, `dd_protection` OFF). 4 arms × 5 realizations = 20 runs.

## Results

| arm | mean bust | sd | SE | residual | resid/SE | |
|---|---|---|---|---|---|---|
| `symmetric_baseline` (the closed family) | 29.44% | 2.38% | 1.07pp | **24.69pp** | **23.18σ** | **decisively different** |
| `skewed_gamma` (adds skew) | 6.59% | 10.85% | 4.85pp | 1.85pp | 0.38σ | within noise |
| `empirical_shuffle` (exact real marginals, i.i.d.) | 5.62% | 1.12% | 0.50pp | 0.87pp | 1.75σ | within noise |
| `empirical_clustered` (idle days in whole weeks) | 5.33% | 2.83% | 1.27pp | 0.58pp | 0.46σ | within noise |

## What is established

**Skew is the dominant missing dimension.** Removing it costs **24.69pp** (symmetric surrogate busts 29.44% against a real 4.74%) at 23.18σ — unambiguous. Restoring it closes **~93% of that gap**. The Q-GEOFIT-1 diagnosis holds.

## What is NOT established — and why the run's own verdict string is wrong

`probe.json` carries `verdict_as_run = "SKEW-INSUFFICIENT / SERIAL-STRUCTURE-BINDING"`. **That output is superseded and should not be cited.** The mechanical rule fired because `empirical_shuffle`'s point estimate landed 0.87pp from target against a 0.50pp tolerance — but that arm's standard error is 0.50pp, making it a **1.75σ** result, not evidence of binding serial structure.

The pre-declared `N = 5` was **too small for the tolerance it was asked to adjudicate**. Minimum resolvable difference (2·SE) by arm: 1.00pp / 2.13pp / 2.53pp / 9.70pp — every one exceeds the 0.50pp tolerance. So no arm except the symmetric baseline can be declared a miss, and the adjudication arm C was built to perform simply did not have the power to perform it.

Resolving it needs roughly **N ≥ 50** for `empirical_shuffle` and **N ≥ 1900** for `skewed_gamma` at its observed dispersion — or a variance-reduced design (common random numbers across arms, paired comparison) rather than brute-force realizations.

## Two side findings

- **`skewed_gamma` is too unstable to be the successor family as-is.** Realization sd **10.85%** — the `Gamma(k=0.359)` win branch throws occasional monster realizations. Its mean is closest in spirit to the real book, but a successor must bound the win tail.
- **R4 placement direction is unmeasured, correcting the closure.** Effect measured **−0.29pp** (clustered minus uniform), combined SE ≈1.37pp → **0.21σ**, indistinguishable from zero. This supersedes the claim carried in the Q-GEOFIT-1 closure §6-defect-3 that uniform placement is the "higher-bust, anti-clearing" choice — that rested on a 2000-sim proxy at different parameters. R4 remains a genuine undeclared reading a successor must fix; only its *direction* is now known to be unmeasured.

## For the successor brief

1. Carry a skew / loss-tail dimension — **confirmed dominant**, 24.69pp at stake.
2. Do **not** assume an i.i.d. family is sufficient, and do not assume it is insufficient. Open question.
3. Bound the win tail; raw Gamma at the fitted shape is unusably dispersed.
4. Power the design to its own tolerance: N ≥ 50 per cell, or common random numbers across arms.
5. R4 still needs an explicit placement law; its direction is unmeasured.
