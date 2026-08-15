# `MNQPOOL-1` — RESULTS: the pool-shield expression carries no session edge

**Status:** FALSIFIED — V2 fired exactly as pre-registered most likely: mean net +0.017R/trade with the week-block 95% CI [−0.011, +0.045] straddling zero, and the placebo shows why — the nearest unswept pool sits a median 572 pt below price, so the shield never binds (stop hit 3.7%) and the construct degenerates to diluted long-RTH drift, indistinguishable from random sessions at identical stop geometry (empirical p = 0.203)

**Date:** 2026-08-04 · **Pre-registration:** [`PREREG.md`](PREREG.md) — **frozen at `9c87f83`, before any
event count existed** (freeze commit precedes this file's commit; §10 hook 1).
**Cost:** **$0.00** (panel on disk, hash-verified) · **K_intrinsic = 1 spent and banked** — manifest
[`mnqpool_shield_probe.json`](lab/archive/../../../discovery_manifests/mnqpool_shield_probe.json) closed
(p = 0.203; 0 of 1 survives at α = 0.05, Bonferroni and BH-FDR agree). `K_banked(MNQ)` **2 → 3**
(disclosure, not a gate, per ADR 2026-08-04).
**Harness:** [`run_pool_probe.py`](run_pool_probe.py) · **15 hand-computed unit tests passing before
the runner read a real bar** · raw [`RESULTS.json`](RESULTS.json).

---

## 1. Verdict — every pre-registered route walked

| § | Route | Frozen trigger | Actual | Fired? |
|---|---|---|---|---|
| V5 | `AMBIGUOUS-UNDERPOWERED` | n < 150 | n = **870** | ✗ |
| **V2** | **`FALSIFIED`** | **mean ≤ 0 OR CI includes 0** | **mean +0.0172, CI [−0.0105, +0.0449]** | **✓** |
| V4 | `AMBIGUOUS-CONFOUND` | CI > 0 but ≤ placebo p95 | would ALSO have fired: +0.0172 < p95 +0.0298 | (moot) |
| V3 | `AMBIGUOUS-EFFECT` | annSR < 0.650 or DSR < 0.95 | would ALSO have fired: annSR 0.450, DSR 0.898 | (moot) |
| V1 | `RESOLVED` | all limbs | not reached | ✗ |

The construct fails **three independent limbs at once** (CI, placebo, floor) — this is not a
marginal miss. Halves were both weakly positive (H1 +0.016 / H2 +0.018, n 411/459), consistent with
mild long drift, not with a pool effect.

## 2. The mechanism of the null — why the shield never engages

The census is the finding:

| | value |
|---|---|
| Sessions / valid / pools / trades | 1,875 / 1,667 / 155 / 870 |
| **Median stop distance (nearest unswept pool below)** | **572 pt (~2.5% of price)** |
| Intraday stop-hit rate | **3.7%** |
| Placebo (random sessions, identical stop geometry): mean / p95 | +0.0049 / +0.0298 |
| Empirical p, pool-eligible vs random sessions | **0.203** |

A `pvLen=3` session-pivot low that has *survived unswept* is, almost by the N9 anomaly itself,
**far below current price** — the anomaly says price avoids returning to these levels, so the
unswept ones recede. With a 572-pt median stop, a single RTH session (6.5h) almost never reaches
it; the trade is effectively "long RTH day, giant stop," its per-trade R is session-drift ÷ 572,
and MNQ's RTH-only drift is ≈ 0 (D5-RECOST). **The loss-side shield is real but never tested
intraday, so it cannot convert into per-session expectancy.** The pool condition added +1.2pp of R
over random sessions — inside noise (p = 0.203).

**The self-defeating structure, stated for the record:** the same property that makes the pool a
good stop-shield (price rarely returns to it) makes it a *distant* stop-shield, which dilutes
per-R expectancy toward zero. The N9 anomaly bounds where price *doesn't go*; a session-scale
expression needs something it *does* do, and RTH drift isn't it.

## 3. What the pre-registration predicted vs what happened

PREREG §4, verbatim: *"The single most likely outcome is V2 or V4 (null-after-costs / base-drift
confound)… the placebo should center near −costs, and the anomaly must supply the entire edge."*
**V2 fired; V4 would also have fired.** One detail ran contrary to the letter of the expectation:
the placebo centered slightly *positive* (+0.005, not near −costs) — at 572-pt median stops the
1.41-pt cost is only ~0.25% of R, so costs barely dent the R-normalized series; the expectation's
cost-drag clause was written for ~40-pt stops and didn't anticipate the census. Recorded as a
(harmless, direction-preserving) miss in the expectation's reasoning, not its conclusion.

## 4. What this does NOT establish

1. **N9 is untouched.** The anti-attractor is a rate fact (0.34 vs 0.65, three instruments); this
   kills one *expression* — the session-carry long at the nearest-pool stop. A rate fact was never
   a strategy; now one specific bridge between them is measured dead.
2. **No other expression is measured.** In particular, *fresher/nearer pools* (shorter windows,
   tighter eligibility) were **not** tested — that is a NEW K-bound axis (PREREG FM-1), not a free
   re-cut, and this file deliberately emits no excursion surfaces to tune one on (FM-6).
3. **The domain bar stands, sharpened.** Route 1 was argued and the probe ran; the result adds a
   fifth in-domain closure to the 2026-07-21 raised bar's tail-count (D5, D5-RECOST, H-TSMOM-1,
   cross-index-RV, **MNQPOOL-1**). The bar's arithmetic moves accordingly at its next review.
4. **Integer-feasibility corroboration (disclosure only):** at the eval's $275 risk cap a 572-pt
   stop sizes to $0.48/pt — **zero micros** ($2/pt). Even a V1 here would have faced a sizing wall
   at these stop widths.

## 5. Iterate — loop exit

- **Verdict used:** `FALSIFIED` (V2), per the frozen precedence ladder.
- **Model update:** the base-construct search's "selection" framing (Step 1: which of ~145
  windows/day carry edge) is NOT advanced by level-avoidance objects at session scale — avoidance
  puts the informative levels too far away to trade against intraday. Whatever selects the good
  windows, it is not "distance from an old unswept low."
- **Next:** STOP.
- **Entry packet:** n/a (STOP). For any future N9-derived proposal: this file's §2 census
  (572-pt median, 3.7% stop-hit, p 0.203) is the arithmetic it must overcome, and FM-1's list of
  untested siblings is the honest K-accounting starting point.
- **Stop rule / re-proposal bar:** new *mechanism* evidence about what price does **near** active
  pools (not re-parameterization of window/pvLen/entry-time, and not a bracket tuned on this
  panel). Any such proposal re-runs the profile consult and re-argues the domain bar's routes at
  the then-current tail count.
- **Board write:** MNQ.md DEAD-list row + session-log entry; STATE decision-index line; SESSIONS
  entry; CATALOG one-liner — all landed with this commit.

## 6. Reproduce

```bash
cd lab/archive/mnq_pool_shield_probe_2026-08-04
python -m pytest test_run_pool_probe.py -q     # 15 passed, before any real bar
python run_pool_probe.py --census              # Step-0 census
python run_pool_probe.py                       # full run -> RESULTS.json
```

Deterministic (seed 20260804 throughout); the placebo reproduction for the manifest p-value
matched the run of record to 1e-12. Data: `MNQ.v.0` 1m 2019-05-06 → 2026-08-04, sha256
`38e29862…` (hash asserted at load).
