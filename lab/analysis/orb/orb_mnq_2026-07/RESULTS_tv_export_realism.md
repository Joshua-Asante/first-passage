# ORB-MNQ-1 — TV-export fill-realism audit + excursion-bounded exit kill tests

**Date:** 2026-07-21 · **Data:** OCA-fixed TV export (`ORB_MNQ_v0.1_..._fe29d.csv`, n=1,040,
2022-07→2026-07) joined to the TV-feed bar panel (`core/data/bar_data/MNQ_M15.csv`, same
`CME_MINI:MNQ1!` chart the backtest ran on; 1,026/1,040 trades have bar coverage).
**Class:** zero-run, zero-K measurements (strategy-validation §3 excursion-bounded
counterfactual + fill-realism audit). No construct change proposed; no re-run consumed.
**Cost convention:** RT $2.22 (comm $1.22 + 2×1-tick slip) → cost_R = 1.11/OR-range.

---

## 1. Fill-realism penetration audit — the 1-tick slip assumption SURVIVES its stress test

Stage-7 made the full-window pass Bulenox-and-≤1-tick-slip-specific, so the 1-tick
assumption is the single most load-bearing realism input. Measured intrabar penetration
*beyond* the trigger level on every fill bar:

| Fill class | n | median pen. | p10 | frac ≤1 tick | frac ≤4 ticks |
|---|---|---|---|---|---|
| Entry (through OR level) | 1,026 | **81 ticks** | 18 | **0.7%** | 1.5% |
| Stop exit (through opposite extreme) | 378 | **64 ticks** | 14 | 0.0% | 2.9% |

On >99% of entries the market traded *well* through the trigger — a 1-lot MNQ stop order
fills at the level ±1 tick in that liquidity picture. The shallow-touch cohort (market
barely kissed the level, where a live fill could sit at the bar extreme) is **0.7–1.5%** of
trades — far too thin to move the Stage-7 slip grid rows. Feed cross-check: **zero** entry
bars where the panel says the level never traded (perfect level agreement with the export).
EOD basis gap (harness 15:45-close vs TV 16:00-open fill): median **1 tick**, p99 5 ticks —
immaterial and sign-symmetric.

**Verdict: the full-window cost fragility is a COMMISSION sensitivity, not a fill-mechanics
one.** Live-fill risk on this construct is concentrated in queue/latency tail events, not in
the systematic slip the offline numbers assume.

## 2a. Tighter-stop counterfactual — the entire space is DEAD (order-free, certain)

A stop at f×OR-range from entry fires iff AE_R ≥ f — path-order-free, so this counterfactual
is exact up to bar granularity (method noise floor: the f=1.0 row should reproduce baseline;
it lands −0.004R off, so read deltas against ±0.004R).

| f | E[R] | Δ vs baseline +0.0992 |
|---|---|---|
| 0.3 | +0.062 | −0.038 |
| 0.4 | +0.041 | **−0.058** |
| 0.5 | +0.049 | −0.050 |
| 0.7 | +0.061 | −0.039 |
| 0.9 | +0.066 | −0.033 |

Every tighter stop loses. Mechanism, not accident: **winners sit through deep drawdown**
(median winner AE 0.34R; 32% of winners survive ≥0.5R adverse excursion). The full-range
stop is load-bearing. Kill margins (0.03–0.06R) are ~10× the method noise floor.

## 2b. Fixed profit target — DEAD at every T, even under best-case ambiguity resolution

| T | E_best (all ambiguous → hit) | E_worst |
|---|---|---|
| 0.50 | +0.039 | −0.145 |
| 1.00 | +0.076 | −0.020 |
| 2.00 | +0.088 | +0.068 |

**E_best never reaches baseline (+0.099) at any T** — the fixed-target space is killed
without even needing the ambiguous (stopped-but-FE≥T) bucket resolved. Exit-at-close
captures more than any fixed R-multiple target could.

## 2c. Give-back at the close — real, but unharvestable by any admissible instrument

EOD trades give back median **0.50R** (mean 0.62R) from peak favorable excursion to the
close; the perfect-exit ceiling is +0.388R/trade (unattainable — requires clairvoyant
exits). The only instrument classes that could touch this headroom are: fixed targets —
**killed above**; and give-back/trailing exits — the **N5/N7 fill-fragile class**, already
falsified on native re-export, and in any case a new candidate at K_eff=3 (DSR floor 0.98).
The exit question is now closed as thoroughly as offline data can close it: the give-back is
the price of the only exit basis that survives.

## 3. 2026-partial "sign disagreement" — RESOLVED: no feed disagreement; a stale local join

The prior session's claim that the harness (−0.012) and TV export (+0.028) disagreed on
sign for 2026 was **wrong, and the error was in the comparison, not either feed.** The
+0.028 figure joined the TV export's 2026 trades against `core/data/bar_data/MNQ_M15.csv`
for OR-range normalization — a committed panel that silently ends **2026-07-01** — which
truncated that year-bucket to n=126 and dropped exactly the ten trading days
2026-07-02→07-15 that turn out to contain a sharp adverse cluster (net **−$2,548**, six of
ten days full stop-outs at R≈−1.00).

Rebuilt on a matched window (the harness's own decode, which ends 2026-07-15, n=136 both
sides): entry-day/side agreement is **136/136 (100%)** — OR-range computation from the two
bar sources agrees closely on overlapping days (mean Δ −0.08pt, only 3/128 days differ by
>0.01pt). On the *identical* 136-day window:

| | meanR | net |
|---|---|---|
| Harness (thru 2026-07-15) | **−0.0118** | — |
| TV export (thru 2026-07-15) | **−0.0246** | — |

**Same sign.** The residual magnitude gap (0.013R) is within the noise floor for n=136 at
R-σ≈1.2 (SE≈0.10R) — not a material disagreement. Extending to the TV export's true full
2026 window (n=140, thru 2026-07-21, including 4 trading days beyond the harness's current
decode): net **−$1,762** overall, with the 07-16→07-21 tail (+$312) partially offsetting
the mid-July cluster.

**Read for the decay monitor:** 2026 is negative on **both** feeds once measured on the
same window — the live-decay tripwire (N2's watch item) should be read as **confirmed
negative-to-date for 2026**, not as an open sign question. The mid-July adverse cluster
(6 full stops in 10 days) is itself the kind of dated event a CUSUM monitor should register;
it is not evidence the construct is broken (regime-conditional edges have negative stretches
by construction), but it is exactly the signal the standing N2/2026-partial watch exists to
catch.

## Disposition

- No change to `orb_mnq_v0_1.pine`; no new candidate opened; K untouched.
- The 1-tick slip input to Stage-6/7 is now empirically underwritten (item 1).
- Tighter-stop and fixed-target redesigns are pre-killed in writing — cite this note if
  either is ever re-proposed (re-proposal bar: new mechanism evidence, not new parameters).
- The 2026-partial "feed sign disagreement" (item 3) is closed — it was a stale local join,
  not a feed discrepancy. Both feeds read 2026 negative on a matched window; no correction
  needed elsewhere (no prior decision cited the wrong +0.028 figure as load-bearing).
- Standing dominant risk unchanged: regime dependence (N2; 2026-partial tripwire), which no
  exit/stop/fill refinement addresses — and item 3 confirms the tripwire is currently reading
  negative, not ambiguous.

Reproduce (main tree, where the bar panel lives):

```bash
.venv-research/Scripts/python.exe lab/analysis/orb_mnq_2026-07/run_tv_export_realism.py \
    --csv <path-to-fe29d-export>
```

The export CSV is operator-held (TV Strategy Tester export of the `df05512d…` edition,
n=1,040, 2022-07-01→2026-07-21); the bar panel is the manifested
`core/data/bar_data/MNQ_M15.csv`.
