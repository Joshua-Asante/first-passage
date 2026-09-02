# Three-leg Tradeify book grid — ORB-MNQ recon × ORB-MYM × Aegis-6J1

**Status:** EXPLORATORY — informal Downloads-lane measurement, not pre-registered, no K entry; the harness reuses `core/mc/simulation.py` and `core/mc/preflight.py` verbatim. Inputs are operator TradingView exports (uncommitted). See `book_grid.py` docstring for the exact files and unit conventions.

## Verdict (2026-09-01)

**No configuration is a clear winner on all three axes (bust, pass, time).** The grid has a genuine bust-versus-speed
frontier, and the two controls change how the Aegis cells should be read. What the 88-cell screen, the six full-N finalists
(30,000 paths each) and the controls do settle:

1. **Any leg at 2 contracts is out.** Every book containing MNQ×2 or MYM×2 busts 40% to 66% on both tiers. Sizing, not
   composition, is the first-order variable; the second is the tier.
2. **Growth beats Select by more than any composition change.** Same books, same clock: MNQ×1 18.9% → 10.8% bust,
   MNQ×1+Aegis×2 14.8% → 7.8%, with identical medians. The $500 wider rope is the biggest lever in the grid.
3. **MYM v0.4 hurts every book it joins.** It buys 40 to 50 days of median time at +9 to +11 points of bust
   (MNQ×1 → MNQ×1+MYM×1: 10.8% → 22.3% on Growth). Its losses coincide with MNQ's 25% more often than independence
   (joint-loss ratio 1.25), its per-trade-day expectancy is a quarter of MNQ's ($12 vs $50 per contract), and its
   active-day skew is 4.5 (rare big wins, many small losses). Drop it as a leg. The measured v0.3 long-only export is
   no better (Growth pair 31.9% bust vs the 19.5% rolling-start figure in MYM.md M9, which this bootstrap does not
   reproduce).
4. **Aegis as ballast improves MNQ×1 on all three axes, but for the wrong reason.** MNQ×1+Aegis×2 vs MNQ×1 on Growth:
   bust 7.8% vs 10.8%, pass 92.2% vs 89.2%, median 161 vs 190 days, all well beyond 2 SE. The shuffled-Aegis control
   (dates permuted within year, drift kept, co-movement destroyed) busts the same or less than the real book on both
   tiers at both sizes. So the gain is Aegis's positive drift over 2022-2026, not diversification. On its excluded
   2020-02 → 2022-07 regime Aegis×2 passes 0.03% of paths in 2.4 years (95% unresolved) and busts 5% (Growth) / 11%
   (Select); ×3 busts 27% / 41%. Aegis×2 beside MNQ×1 is therefore a bet that the 2022+ yen regime persists, with a
   short-side rail change and a 6J Python port as its price. It fits the 30-micro funded start (21 micro-equivalents);
   Aegis×3 (31) does not until the first ladder step.
5. **Aegis alone is the only thing under the frozen 5% ceiling, and only on the favourable window.** Aegis×3 on Growth:
   2.3% bust, 95.4% pass, median 602 days, 47% of weeks with no trade (token trade every other week). On the excluded
   regime the same size busts 27%.

**Defensible picks, in order, under the fee-priced criterion (pass ≥ 60%, median ≤ 200 days, worse half ≥ 50%):**

| Pick | Tier | bust | pass | median days | worse half | Why / cost |
|---|---|---:|---:|---:|---:|---|
| MNQ×1 + Aegis×2 | Growth | 7.8% | 92.2% | 161 | 84% pass | Best bust/pass among fast books; gain is drift, regime-conditional; needs short-side rail + 6J port |
| MNQ×1 | Growth | 10.8% | 89.2% | 190 | 77% pass | Simplest; one port, one leg, no Aegis regime bet; 99% weekly coverage |
| MNQ×1 + Aegis×2 | Select | 14.8% | 85.2% | 154 | 74% pass | Same book on the live account; no Growth purchase |
| MNQ×1 + MYM×1 + Aegis×2 | Growth | 19.2% | 80.8% | 108 | 76% pass | Fastest; pays 11 points of bust for 53 days |

**Bounds, stated plainly.** The bootstrap breaks the realized sequence and is the pessimistic read (every finalist's realized
path passes, day 79 to 156, max drawdown 1.9% to 2.2%, and rolling starts never bust). The intraday channel is a trade-level
sweep-line from TradingView's own adverse-excursion figures, not a bar replay. The window starts 2022-08-01 because MYM v0.4
does; MNQ's own 2020-2021 (the recon_v2 six-year export busts its realized path in 2020 at one contract on Select) and
Aegis's 2020-2022 are outside it. The MNQ recon lineage and MYM v0.4 are tuned charts with no untouched holdout. Export
slippage and commission are whatever the operator set in TradingView; Aegis uses the sanctioned 1-tick `76620` panel
(the 08-28 `cbcc9` export fills one tick better on every shared trade and was not used). Growth's soft $2,500 daily
lockout is not modeled (pessimistic on the rope); Select's 40% consistency rule is.

## Finalists at full N

n_sims=10000 × seeds [42, 123, 2026] = 30,000 bootstrap paths per cell; elapsed 2537.5s. Bootstrap = 5-day block resample through `run_seed`, intraday-honest channel (timestamp-sequenced trade-level floor). Halves split at the window's business-day midpoint. Rolling = deterministic replay from every start day (intraday clock). E[fee] = $265 + $169 × (1−p)/p on resolved paths.

### Tradeify_Growth_100K — window 2022-08-01 → 2026-07-01 (1023 business days)

| Book | micro-eq | bust % (±SE) | pass % | unresolved % | median days | H1 bust/pass | H2 bust/pass | rolling pass/bust/unres | weekly cov | E[fee] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AEGISx3 | 30 | 2.3 ± 0.1 | 95.4 | 2.3 | 602 | 8.1 / 87.2 | 0.3 / 99.2 | 49 / 0 / 51 | 47% | $269 |
| MNQx1 + AEGISx2 | 21 | 7.8 ± 0.2 | 92.2 | 0.0 | 161 | 3.3 / 96.7 | 15.7 / 84.3 | 80 / 0 / 20 | 100% | $279 |
| MNQx1 + AEGISx3 | 31 | 8.5 ± 0.2 | 91.5 | 0.0 | 146 | 3.7 / 96.3 | 15.4 / 84.6 | 84 / 0 / 16 | 100% | $281 |
| MNQx1 | 1 | 10.8 ± 0.2 | 89.2 | 0.0 | 190 | 5.9 / 94.1 | 22.6 / 77.4 | 70 / 0 / 30 | 99% | $286 |
| MNQx1 + MYMx1 + AEGISx2 | 22 | 19.2 ± 0.2 | 80.8 | 0.0 | 108 | 14.2 / 85.8 | 23.9 / 76.1 | 88 / 0 / 12 | 100% | $305 |
| MNQx1 + MYMx1 | 2 | 22.3 ± 0.2 | 77.7 | 0.0 | 121 | 16.7 / 83.3 | 31.2 / 68.8 | 83 / 0 / 17 | 100% | $313 |

**Pareto set (not dominated beyond 2 SE on bust/pass with ≤ median days):** AEGISx3; MNQx1 + AEGISx2; MNQx1 + AEGISx3; MNQx1 + MYMx1 + AEGISx2

Standalone legs on this tier:

- AEGISx3: bust 2.3%, pass 95.4%, median 602.0 days, weekly coverage 47%
- MNQx1: bust 10.8%, pass 89.2%, median 190.0 days, weekly coverage 99%

### Tradeify_Select_100K — window 2022-08-01 → 2026-07-01 (1023 business days)

| Book | micro-eq | bust % (±SE) | pass % | unresolved % | median days | H1 bust/pass | H2 bust/pass | rolling pass/bust/unres | weekly cov | E[fee] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AEGISx3 | 30 | 5.1 ± 0.1 | 93.2 | 1.7 | 596 | 14.7 / 82.3 | 0.9 / 98.6 | 49 / 0 / 51 | 47% | $274 |
| MNQx1 + AEGISx2 | 21 | 14.8 ± 0.2 | 85.2 | 0.0 | 154 | 7.7 / 92.3 | 26.3 / 73.7 | 80 / 0 / 20 | 100% | $294 |
| MNQx1 + AEGISx3 | 31 | 15.3 ± 0.2 | 84.7 | 0.0 | 140 | 8.2 / 91.8 | 25.7 / 74.3 | 84 / 0 / 16 | 100% | $296 |
| MNQx1 | 1 | 18.9 ± 0.2 | 81.1 | 0.0 | 180 | 11.9 / 88.1 | 34.5 / 65.5 | 70 / 0 / 30 | 99% | $304 |
| MNQx1 + MYMx1 + AEGISx2 | 22 | 30.1 ± 0.3 | 69.9 | 0.0 | 102 | 23.8 / 76.2 | 37.7 / 62.3 | 88 / 0 / 12 | 100% | $338 |
| MNQx1 + MYMx1 | 2 | 33.7 ± 0.3 | 66.3 | 0.0 | 115 | 26.7 / 73.3 | 45.4 / 54.6 | 83 / 0 / 17 | 100% | $351 |

**Pareto set (not dominated beyond 2 SE on bust/pass with ≤ median days):** AEGISx3; MNQx1 + AEGISx2; MNQx1 + AEGISx3; MNQx1 + MYMx1 + AEGISx2

Standalone legs on this tier:

- AEGISx3: bust 5.1%, pass 93.2%, median 596.0 days, weekly coverage 47%
- MNQx1: bust 18.9%, pass 81.1%, median 180.0 days, weekly coverage 99%

## Screen grid — MNQ {0,1,2} × MYM v0.4 {0,1,2} × Aegis {0..4}

n_sims=1000 × seeds [42, 123, 2026] = 3,000 bootstrap paths per cell; elapsed 669.0s. Bootstrap = 5-day block resample through `run_seed`, intraday-honest channel (timestamp-sequenced trade-level floor). Halves split at the window's business-day midpoint. Rolling = deterministic replay from every start day (intraday clock). E[fee] = $265 + $169 × (1−p)/p on resolved paths.

### Tradeify_Growth_100K — window 2022-08-01 → 2026-07-01 (1023 business days)

| Book | micro-eq | bust % (±SE) | pass % | unresolved % | median days | H1 bust/pass | H2 bust/pass | rolling pass/bust/unres | weekly cov | E[fee] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AEGISx3 | 30 | 2.5 ± 0.3 | 95.0 | 2.6 | 593 | 7.5 / 87.5 | 0.2 / 99.2 | 49 / 0 / 51 | 47% | $269 |
| AEGISx4 | 40 | 6.9 ± 0.5 | 92.6 | 0.5 | 423 | 18.0 / 81.3 | 1.7 / 98.3 | 64 / 0 / 36 | 47% | $278 |
| MNQx1 + AEGISx2 | 21 | 8.4 ± 0.5 | 91.6 | 0.0 | 159 | 3.4 / 96.6 | 15.1 / 84.9 | 80 / 0 / 20 | 100% | $281 |
| MNQx1 + AEGISx3 | 31 | 9.1 ± 0.5 | 90.9 | 0.0 | 146 | 3.7 / 96.3 | 15.1 / 84.9 | 84 / 0 / 16 | 100% | $282 |
| MNQx1 + AEGISx1 | 11 | 9.3 ± 0.5 | 90.7 | 0.0 | 172 | 3.9 / 96.1 | 17.1 / 82.9 | 72 / 0 / 28 | 100% | $282 |
| MNQx1 + AEGISx4 | 41 | 9.9 ± 0.5 | 90.1 | 0.0 | 135 | 4.3 / 95.7 | 15.8 / 84.2 | 87 / 0 / 13 | 100% | $284 |
| MNQx1 | 1 | 11.9 ± 0.6 | 88.1 | 0.0 | 189 | 6.2 / 93.8 | 21.9 / 78.1 | 70 / 0 / 30 | 99% | $288 |
| AEGISx2 | 20 | 0.3 ± 0.1 | 87.1 | 12.6 | 868 | 1.1 / 75.1 | 0.0 / 95.5 | 15 / 0 / 85 | 47% | $266 |
| MYMx1 + AEGISx2 | 21 | 16.6 ± 0.7 | 83.4 | 0.0 | 280 | 20.8 / 79.2 | 7.3 / 92.7 | 74 / 0 / 26 | 100% | $299 |
| MYMx1 + AEGISx3 | 31 | 17.4 ± 0.7 | 82.6 | 0.0 | 234 | 22.4 / 77.6 | 7.0 / 93.0 | 80 / 0 / 20 | 100% | $301 |
| MYMx1 + AEGISx1 | 11 | 18.2 ± 0.7 | 81.8 | 0.0 | 330 | 21.5 / 78.5 | 12.0 / 88.0 | 69 / 0 / 31 | 100% | $303 |
| MNQx1 + MYMx1 + AEGISx2 | 22 | 19.5 ± 0.7 | 80.5 | 0.0 | 108 | 14.3 / 85.7 | 24.0 / 76.0 | 88 / 0 / 12 | 100% | $306 |
| MNQx1 + MYMx1 + AEGISx3 | 32 | 19.8 ± 0.7 | 80.2 | 0.0 | 100 | 14.1 / 85.9 | 23.5 / 76.5 | 90 / 0 / 10 | 100% | $307 |
| MYMx1 + AEGISx4 | 41 | 19.8 ± 0.7 | 80.2 | 0.0 | 198 | 25.5 / 74.5 | 7.6 / 92.4 | 83 / 0 / 17 | 100% | $307 |
| MNQx1 + MYMx1 + AEGISx4 | 42 | 20.4 ± 0.7 | 79.6 | 0.0 | 92 | 15.2 / 84.8 | 23.2 / 76.8 | 90 / 0 / 10 | 100% | $308 |
| MNQx1 + MYMx1 + AEGISx1 | 12 | 21.1 ± 0.7 | 78.9 | 0.0 | 116 | 15.2 / 84.8 | 27.1 / 72.9 | 86 / 0 / 14 | 100% | $310 |
| MNQx1 + MYMx1 | 2 | 23.8 ± 0.8 | 76.2 | 0.0 | 121 | 16.9 / 83.1 | 31.5 / 68.5 | 83 / 0 / 17 | 100% | $318 |
| MYMx1 | 1 | 25.9 ± 0.8 | 74.1 | 0.0 | 377 | 25.9 / 74.1 | 26.4 / 73.3 | 60 / 0 / 40 | 100% | $324 |
| MNQx2 + AEGISx4 | 42 | 40.0 ± 0.9 | 60.0 | 0.0 | 59 | 27.8 / 72.2 | 44.3 / 55.7 | 84 / 13 / 3 | 100% | $378 |
| MNQx2 + AEGISx3 | 32 | 40.1 ± 0.9 | 59.9 | 0.0 | 62 | 28.4 / 71.6 | 45.2 / 54.8 | 84 / 13 / 3 | 100% | $378 |
| MNQx2 + AEGISx2 | 22 | 41.7 ± 0.9 | 58.3 | 0.0 | 65 | 29.6 / 70.4 | 46.7 / 53.3 | 84 / 13 / 3 | 100% | $386 |
| MNQx2 + AEGISx1 | 12 | 43.1 ± 0.9 | 56.9 | 0.0 | 67 | 31.0 / 69.0 | 48.7 / 51.3 | 70 / 26 / 3 | 100% | $393 |
| MNQx1 + MYMx2 + AEGISx3 | 33 | 44.1 ± 0.9 | 55.9 | 0.0 | 66 | 39.1 / 60.9 | 50.5 / 49.5 | 67 / 24 / 9 | 100% | $399 |
| MNQx2 + MYMx1 + AEGISx1 | 13 | 44.2 ± 0.9 | 55.8 | 0.0 | 51 | 39.5 / 60.5 | 50.0 / 50.0 | 55 / 43 / 2 | 100% | $399 |
| MYMx2 + AEGISx4 | 42 | 44.3 ± 0.9 | 55.7 | 0.0 | 93 | 49.2 / 50.8 | 42.1 / 57.9 | 55 / 33 / 12 | 100% | $399 |
| MNQx1 + MYMx2 + AEGISx4 | 43 | 44.3 ± 0.9 | 55.7 | 0.0 | 62 | 38.2 / 61.8 | 49.4 / 50.6 | 72 / 20 / 8 | 100% | $400 |
| MNQx2 + MYMx1 + AEGISx4 | 43 | 45.0 ± 0.9 | 55.0 | 0.0 | 47 | 37.4 / 62.6 | 48.7 / 51.3 | 73 / 26 / 2 | 100% | $403 |
| MYMx2 + AEGISx3 | 32 | 45.2 ± 0.9 | 54.8 | 0.0 | 102 | 48.8 / 51.2 | 44.2 / 55.8 | 54 / 34 / 12 | 100% | $404 |
| MNQx2 | 2 | 45.2 ± 0.9 | 54.8 | 0.0 | 67 | 34.1 / 65.9 | 51.5 / 48.5 | 69 / 28 / 3 | 99% | $405 |
| MNQx1 + MYMx2 + AEGISx2 | 23 | 45.5 ± 0.9 | 54.5 | 0.0 | 69 | 39.5 / 60.5 | 53.0 / 47.0 | 65 / 25 / 10 | 100% | $406 |
| MNQx2 + MYMx1 | 3 | 45.6 ± 0.9 | 54.4 | 0.0 | 52 | 40.9 / 59.1 | 51.2 / 48.8 | 52 / 47 / 2 | 100% | $407 |
| MNQx2 + MYMx1 + AEGISx3 | 33 | 45.8 ± 0.9 | 54.2 | 0.0 | 49 | 37.8 / 62.2 | 49.8 / 50.2 | 71 / 27 / 2 | 100% | $408 |
| MNQx2 + MYMx1 + AEGISx2 | 23 | 46.6 ± 0.9 | 53.4 | 0.0 | 51 | 38.7 / 61.3 | 50.7 / 49.3 | 58 / 40 / 2 | 100% | $412 |
| MYMx2 + AEGISx2 | 22 | 46.8 ± 0.9 | 53.2 | 0.0 | 110 | 49.4 / 50.6 | 47.6 / 52.4 | 53 / 32 / 15 | 100% | $413 |
| MNQx1 + MYMx2 + AEGISx1 | 13 | 47.3 ± 0.9 | 52.7 | 0.0 | 71 | 40.5 / 59.5 | 55.3 / 44.7 | 65 / 25 / 10 | 100% | $417 |
| MYMx2 + AEGISx1 | 12 | 48.8 ± 0.9 | 51.2 | 0.0 | 117 | 51.0 / 49.0 | 51.5 / 48.5 | 53 / 30 / 17 | 100% | $426 |
| MNQx1 + MYMx2 | 3 | 49.4 ± 0.9 | 50.6 | 0.0 | 74 | 42.1 / 57.9 | 58.6 / 41.4 | 63 / 26 / 10 | 100% | $430 |
| MNQx2 + MYMx2 + AEGISx4 | 44 | 51.9 ± 0.9 | 48.1 | 0.0 | 37 | 49.3 / 50.7 | 55.9 / 44.1 | 60 / 39 / 1 | 100% | $447 |
| MNQx2 + MYMx2 + AEGISx3 | 34 | 52.5 ± 0.9 | 47.5 | 0.0 | 39 | 49.6 / 50.4 | 56.7 / 43.3 | 57 / 41 / 1 | 100% | $452 |
| MNQx2 + MYMx2 + AEGISx2 | 24 | 53.3 ± 0.9 | 46.7 | 0.0 | 39 | 49.9 / 50.1 | 57.7 / 42.3 | 55 / 44 / 1 | 100% | $458 |
| MYMx2 | 2 | 53.8 ± 0.9 | 46.2 | 0.0 | 120 | 52.9 / 47.1 | 57.3 / 42.7 | 50 / 32 / 18 | 100% | $462 |
| MNQx2 + MYMx2 + AEGISx1 | 14 | 54.4 ± 0.9 | 45.6 | 0.0 | 40 | 50.4 / 49.6 | 59.1 / 40.9 | 55 / 44 / 1 | 100% | $466 |
| MNQx2 + MYMx2 | 4 | 55.4 ± 0.9 | 44.6 | 0.0 | 40 | 51.9 / 48.1 | 60.2 / 39.8 | 53 / 45 / 2 | 100% | $475 |
| AEGISx1 | 10 | 0.0 ± 0.0 | 21.2 | 78.8 | 1311 | 0.0 / 13.7 | 0.0 / 34.0 | 0 / 0 / 100 | 47% | $265 |

**Pareto set (not dominated beyond 2 SE on bust/pass with ≤ median days):** AEGISx3; AEGISx4; MNQx1 + AEGISx2; MNQx1 + AEGISx3; MNQx1 + AEGISx1; MNQx1 + AEGISx4; AEGISx2; MNQx1 + MYMx1 + AEGISx2; MNQx1 + MYMx1 + AEGISx3; MNQx1 + MYMx1 + AEGISx4; MNQx1 + MYMx1 + AEGISx1; MNQx2 + AEGISx4; MNQx2 + AEGISx3; MNQx2 + AEGISx2; MNQx2 + MYMx1 + AEGISx1; MNQx2 + MYMx1 + AEGISx4; MNQx2 + MYMx1; MNQx2 + MYMx1 + AEGISx3; MNQx2 + MYMx1 + AEGISx2; MNQx2 + MYMx2 + AEGISx4; MNQx2 + MYMx2 + AEGISx3; MNQx2 + MYMx2 + AEGISx2; MNQx2 + MYMx2 + AEGISx1; AEGISx1

Standalone legs on this tier:

- AEGISx1: bust 0.0%, pass 21.2%, median 1311.0 days, weekly coverage 47%
- AEGISx2: bust 0.3%, pass 87.1%, median 867.5 days, weekly coverage 47%
- AEGISx3: bust 2.5%, pass 95.0%, median 593.0 days, weekly coverage 47%
- AEGISx4: bust 6.9%, pass 92.6%, median 423.0 days, weekly coverage 47%
- MNQx1: bust 11.9%, pass 88.1%, median 189.0 days, weekly coverage 99%
- MNQx2: bust 45.2%, pass 54.8%, median 67.0 days, weekly coverage 99%
- MYMx1: bust 25.9%, pass 74.1%, median 377.0 days, weekly coverage 100%
- MYMx2: bust 53.8%, pass 46.2%, median 120.0 days, weekly coverage 100%

### Tradeify_Select_100K — window 2022-08-01 → 2026-07-01 (1023 business days)

| Book | micro-eq | bust % (±SE) | pass % | unresolved % | median days | H1 bust/pass | H2 bust/pass | rolling pass/bust/unres | weekly cov | E[fee] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AEGISx3 | 30 | 5.0 ± 0.4 | 92.8 | 2.2 | 586 | 14.0 / 82.6 | 1.0 / 98.5 | 49 / 0 / 51 | 47% | $274 |
| AEGISx4 | 40 | 12.7 ± 0.6 | 87.3 | 0.1 | 406 | 26.7 / 73.1 | 4.0 / 96.0 | 64 / 0 / 36 | 47% | $290 |
| AEGISx2 | 20 | 0.6 ± 0.1 | 87.0 | 12.4 | 867 | 2.7 / 74.8 | 0.1 / 95.5 | 15 / 0 / 85 | 47% | $266 |
| MNQx1 + AEGISx2 | 21 | 14.4 ± 0.6 | 85.6 | 0.0 | 155 | 7.9 / 92.1 | 25.8 / 74.2 | 80 / 0 / 20 | 100% | $294 |
| MNQx1 + AEGISx3 | 31 | 15.0 ± 0.7 | 85.0 | 0.0 | 142 | 8.5 / 91.5 | 25.1 / 74.9 | 84 / 0 / 16 | 100% | $295 |
| MNQx1 + AEGISx1 | 11 | 15.6 ± 0.7 | 84.4 | 0.0 | 167 | 9.0 / 91.0 | 28.7 / 71.3 | 72 / 0 / 28 | 100% | $296 |
| MNQx1 + AEGISx4 | 41 | 17.8 ± 0.7 | 82.2 | 0.0 | 127 | 10.1 / 89.9 | 25.6 / 74.4 | 87 / 0 / 13 | 100% | $302 |
| MNQx1 | 1 | 19.4 ± 0.7 | 80.6 | 0.0 | 179 | 12.3 / 87.7 | 33.9 / 66.1 | 70 / 0 / 30 | 99% | $306 |
| MYMx1 + AEGISx2 | 21 | 26.3 ± 0.8 | 73.7 | 0.0 | 280 | 30.9 / 69.1 | 15.8 / 84.2 | 74 / 0 / 26 | 100% | $325 |
| MYMx1 + AEGISx3 | 31 | 28.1 ± 0.8 | 71.9 | 0.0 | 232 | 32.7 / 67.3 | 15.3 / 84.7 | 80 / 0 / 20 | 100% | $331 |
| MYMx1 + AEGISx1 | 11 | 29.1 ± 0.8 | 70.9 | 0.0 | 334 | 31.8 / 68.2 | 23.6 / 76.4 | 64 / 0 / 36 | 100% | $334 |
| MYMx1 + AEGISx4 | 41 | 29.4 ± 0.8 | 70.6 | 0.0 | 196 | 35.6 / 64.4 | 17.4 / 82.6 | 83 / 0 / 17 | 100% | $335 |
| MNQx1 + MYMx1 + AEGISx2 | 22 | 30.3 ± 0.8 | 69.7 | 0.0 | 103 | 24.7 / 75.3 | 37.5 / 62.5 | 88 / 0 / 12 | 100% | $339 |
| MNQx1 + MYMx1 + AEGISx4 | 42 | 30.5 ± 0.8 | 69.5 | 0.0 | 89 | 25.3 / 74.7 | 34.7 / 65.3 | 90 / 0 / 10 | 100% | $339 |
| MNQx1 + MYMx1 + AEGISx3 | 32 | 30.6 ± 0.8 | 69.4 | 0.0 | 95 | 24.3 / 75.7 | 35.3 / 64.7 | 90 / 0 / 10 | 100% | $340 |
| MNQx1 + MYMx1 + AEGISx1 | 12 | 31.4 ± 0.8 | 68.6 | 0.0 | 111 | 25.6 / 74.4 | 41.0 / 59.0 | 86 / 0 / 14 | 100% | $342 |
| MNQx1 + MYMx1 | 2 | 34.1 ± 0.9 | 65.9 | 0.0 | 115 | 27.5 / 72.5 | 45.2 / 54.8 | 83 / 0 / 17 | 100% | $352 |
| MYMx1 | 1 | 38.7 ± 0.9 | 61.3 | 0.0 | 378 | 37.2 / 62.8 | 42.6 / 57.2 | 3 / 41 / 56 | 100% | $372 |
| MNQx2 + AEGISx4 | 42 | 51.1 ± 0.9 | 48.9 | 0.0 | 54 | 41.3 / 58.7 | 54.7 / 45.3 | 66 / 33 / 2 | 100% | $442 |
| MNQx2 + AEGISx3 | 32 | 51.9 ± 0.9 | 48.1 | 0.0 | 56 | 41.0 / 59.0 | 55.4 / 44.6 | 51 / 48 / 2 | 100% | $447 |
| MNQx2 + AEGISx2 | 22 | 53.8 ± 0.9 | 46.2 | 0.0 | 59 | 41.9 / 58.1 | 57.1 / 42.9 | 49 / 49 / 2 | 100% | $462 |
| MNQx1 + MYMx2 + AEGISx3 | 33 | 54.2 ± 0.9 | 45.8 | 0.0 | 61 | 51.0 / 49.0 | 59.7 / 40.3 | 65 / 33 / 2 | 100% | $465 |
| MNQx1 + MYMx2 + AEGISx4 | 43 | 54.5 ± 0.9 | 45.5 | 0.0 | 57 | 50.9 / 49.1 | 59.2 / 40.8 | 69 / 29 / 2 | 100% | $467 |
| MNQx2 + AEGISx1 | 12 | 54.8 ± 0.9 | 45.2 | 0.0 | 60 | 43.1 / 56.9 | 58.9 / 41.1 | 44 / 53 / 3 | 100% | $470 |
| MNQx1 + MYMx2 + AEGISx2 | 23 | 55.5 ± 0.9 | 44.5 | 0.0 | 63 | 51.2 / 48.8 | 61.5 / 38.5 | 62 / 37 / 2 | 100% | $475 |
| MNQx2 | 2 | 56.5 ± 0.9 | 43.5 | 0.0 | 61 | 45.0 / 55.0 | 61.6 / 38.4 | 39 / 58 / 3 | 99% | $484 |
| MNQx2 + MYMx1 + AEGISx4 | 43 | 56.9 ± 0.9 | 43.1 | 0.0 | 45 | 51.4 / 48.6 | 59.5 / 40.5 | 53 / 45 / 1 | 100% | $488 |
| MNQx1 + MYMx2 + AEGISx1 | 13 | 57.3 ± 0.9 | 42.7 | 0.0 | 65 | 52.4 / 47.6 | 63.3 / 36.7 | 61 / 37 / 2 | 100% | $492 |
| MYMx2 + AEGISx4 | 42 | 57.4 ± 0.9 | 42.6 | 0.0 | 90 | 58.5 / 41.5 | 61.3 / 38.7 | 46 / 42 / 12 | 100% | $493 |
| MNQx2 + MYMx1 + AEGISx3 | 33 | 57.6 ± 0.9 | 42.4 | 0.0 | 46 | 51.7 / 48.3 | 59.9 / 40.1 | 50 / 48 / 1 | 100% | $494 |
| MNQx2 + MYMx1 + AEGISx2 | 23 | 58.0 ± 0.9 | 42.0 | 0.0 | 47 | 51.9 / 48.1 | 61.8 / 38.2 | 48 / 51 / 2 | 100% | $498 |
| MYMx2 + AEGISx3 | 32 | 58.4 ± 0.9 | 41.6 | 0.0 | 100 | 58.6 / 41.4 | 63.5 / 36.5 | 42 / 45 / 12 | 100% | $503 |
| MNQx2 + MYMx1 + AEGISx1 | 13 | 59.3 ± 0.9 | 40.7 | 0.0 | 49 | 52.3 / 47.7 | 63.0 / 37.0 | 45 / 53 / 2 | 100% | $511 |
| MNQx1 + MYMx2 | 3 | 59.4 ± 0.9 | 40.6 | 0.0 | 67 | 54.1 / 45.9 | 66.2 / 33.8 | 61 / 38 / 2 | 100% | $512 |
| MYMx2 + AEGISx2 | 22 | 59.8 ± 0.9 | 40.2 | 0.0 | 110 | 59.6 / 40.4 | 67.7 / 32.3 | 36 / 49 / 15 | 100% | $516 |
| MNQx2 + MYMx1 | 3 | 60.4 ± 0.9 | 39.6 | 0.0 | 49 | 53.3 / 46.7 | 65.1 / 34.9 | 42 / 56 / 2 | 100% | $523 |
| MYMx2 + AEGISx1 | 12 | 62.1 ± 0.9 | 37.9 | 0.0 | 117 | 60.7 / 39.3 | 71.9 / 28.1 | 34 / 49 / 17 | 100% | $542 |
| MNQx2 + MYMx2 + AEGISx3 | 34 | 62.2 ± 0.9 | 37.8 | 0.0 | 37 | 58.2 / 41.8 | 68.0 / 32.0 | 37 / 62 / 1 | 100% | $543 |
| MNQx2 + MYMx2 + AEGISx4 | 44 | 62.3 ± 0.9 | 37.7 | 0.0 | 35 | 58.4 / 41.6 | 67.1 / 32.9 | 39 / 60 / 1 | 100% | $544 |
| MNQx2 + MYMx2 + AEGISx2 | 24 | 62.4 ± 0.9 | 37.6 | 0.0 | 37 | 58.1 / 41.9 | 68.5 / 31.5 | 36 / 64 / 1 | 100% | $546 |
| MNQx2 + MYMx2 + AEGISx1 | 14 | 63.3 ± 0.9 | 36.7 | 0.0 | 38 | 58.8 / 41.2 | 69.4 / 30.6 | 36 / 63 / 1 | 100% | $557 |
| MNQx2 + MYMx2 | 4 | 64.5 ± 0.9 | 35.5 | 0.0 | 39 | 59.9 / 40.1 | 70.6 / 29.4 | 31 / 68 / 1 | 100% | $572 |
| MYMx2 | 2 | 66.6 ± 0.9 | 33.4 | 0.0 | 123 | 62.8 / 37.2 | 76.9 / 23.1 | 32 / 49 / 18 | 100% | $602 |
| AEGISx1 | 10 | 0.0 ± 0.0 | 21.2 | 78.8 | 1311 | 0.0 / 13.7 | 0.0 / 34.0 | 0 / 0 / 100 | 47% | $265 |

**Pareto set (not dominated beyond 2 SE on bust/pass with ≤ median days):** AEGISx3; AEGISx4; AEGISx2; MNQx1 + AEGISx2; MNQx1 + AEGISx3; MNQx1 + AEGISx1; MNQx1 + AEGISx4; MNQx1 + MYMx1 + AEGISx2; MNQx1 + MYMx1 + AEGISx4; MNQx1 + MYMx1 + AEGISx3; MNQx1 + MYMx1 + AEGISx1; MNQx2 + AEGISx4; MNQx2 + AEGISx3; MNQx2 + MYMx1 + AEGISx4; MNQx2 + MYMx1 + AEGISx3; MNQx2 + MYMx1 + AEGISx2; MNQx2 + MYMx1 + AEGISx1; MNQx2 + MYMx2 + AEGISx3; MNQx2 + MYMx2 + AEGISx4; MNQx2 + MYMx2 + AEGISx2; MNQx2 + MYMx2 + AEGISx1; MNQx2 + MYMx2; AEGISx1

Standalone legs on this tier:

- AEGISx1: bust 0.0%, pass 21.2%, median 1311.0 days, weekly coverage 47%
- AEGISx2: bust 0.6%, pass 87.0%, median 867.0 days, weekly coverage 47%
- AEGISx3: bust 5.0%, pass 92.8%, median 586.0 days, weekly coverage 47%
- AEGISx4: bust 12.7%, pass 87.3%, median 406.0 days, weekly coverage 47%
- MNQx1: bust 19.4%, pass 80.6%, median 179.0 days, weekly coverage 99%
- MNQx2: bust 56.5%, pass 43.5%, median 61.0 days, weekly coverage 99%
- MYMx1: bust 38.7%, pass 61.3%, median 378.0 days, weekly coverage 100%
- MYMx2: bust 66.6%, pass 33.4%, median 123.0 days, weekly coverage 100%

## Reference cells with the measured MYM v0.3 export (long-only, MYM.md M9)

n_sims=1000 × seeds [42, 123, 2026] = 3,000 bootstrap paths per cell; elapsed 116.4s. Bootstrap = 5-day block resample through `run_seed`, intraday-honest channel (timestamp-sequenced trade-level floor). Halves split at the window's business-day midpoint. Rolling = deterministic replay from every start day (intraday clock). E[fee] = $265 + $169 × (1−p)/p on resolved paths.

### Tradeify_Growth_100K — window 2022-01-03 → 2026-07-01 (1173 business days)

| Book | micro-eq | bust % (±SE) | pass % | unresolved % | median days | H1 bust/pass | H2 bust/pass | rolling pass/bust/unres | weekly cov | E[fee] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MNQx1 | 1 | 11.4 ± 0.6 | 88.6 | 0.0 | 175 | 10.2 / 89.8 | 17.2 / 82.8 | 74 / 0 / 26 | 99% | $287 |
| MNQx1 + MYM_V03x1 + AEGISx2 | 22 | 27.2 ± 0.8 | 72.8 | 0.0 | 99 | 26.1 / 73.9 | 29.0 / 71.0 | 91 / 0 / 9 | 100% | $328 |
| MYM_V03x1 | 1 | 30.1 ± 0.8 | 69.8 | 0.1 | 413 | 20.3 / 79.6 | 42.4 / 57.2 | 53 / 0 / 47 | 100% | $338 |
| MNQx1 + MYM_V03x1 | 2 | 31.9 ± 0.9 | 68.1 | 0.0 | 106 | 30.4 / 69.6 | 35.4 / 64.6 | 85 / 0 / 15 | 100% | $344 |
| MYM_V03x2 | 2 | 55.0 ± 0.9 | 45.0 | 0.0 | 136 | 49.6 / 50.4 | 65.7 / 34.3 | 35 / 42 / 23 | 100% | $472 |

**Pareto set (not dominated beyond 2 SE on bust/pass with ≤ median days):** MNQx1; MNQx1 + MYM_V03x1 + AEGISx2

Standalone legs on this tier:

- MNQx1: bust 11.4%, pass 88.6%, median 175.0 days, weekly coverage 99%
- MYM_V03x1: bust 30.1%, pass 69.8%, median 413.0 days, weekly coverage 100%
- MYM_V03x2: bust 55.0%, pass 45.0%, median 136.0 days, weekly coverage 100%

### Tradeify_Select_100K — window 2022-01-03 → 2026-07-01 (1173 business days)

| Book | micro-eq | bust % (±SE) | pass % | unresolved % | median days | H1 bust/pass | H2 bust/pass | rolling pass/bust/unres | weekly cov | E[fee] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MNQx1 | 1 | 19.5 ± 0.7 | 80.5 | 0.0 | 167 | 18.1 / 81.9 | 27.8 / 72.2 | 74 / 0 / 26 | 99% | $306 |
| MNQx1 + MYM_V03x1 + AEGISx2 | 22 | 38.7 ± 0.9 | 61.3 | 0.0 | 91 | 37.1 / 62.9 | 41.2 / 58.8 | 91 / 5 / 4 | 100% | $372 |
| MYM_V03x1 | 1 | 42.5 ± 0.9 | 57.5 | 0.0 | 408 | 30.4 / 69.6 | 57.5 / 42.4 | 22 / 0 / 78 | 100% | $390 |
| MNQx1 + MYM_V03x1 | 2 | 43.5 ± 0.9 | 56.5 | 0.0 | 99 | 40.9 / 59.1 | 48.6 / 51.4 | 85 / 0 / 15 | 100% | $395 |
| MYM_V03x2 | 2 | 70.9 ± 0.8 | 29.1 | 0.0 | 145 | 62.2 / 37.8 | 83.1 / 16.9 | 16 / 57 / 26 | 100% | $676 |

**Pareto set (not dominated beyond 2 SE on bust/pass with ≤ median days):** MNQx1; MNQx1 + MYM_V03x1 + AEGISx2

Standalone legs on this tier:

- MNQx1: bust 19.5%, pass 80.5%, median 167.0 days, weekly coverage 99%
- MYM_V03x1: bust 42.5%, pass 57.5%, median 408.0 days, weekly coverage 100%
- MYM_V03x2: bust 70.9%, pass 29.1%, median 145.0 days, weekly coverage 100%

## Controls

### (A) Shuffled-Aegis control — is Aegis's benefit co-movement or just positive drift?

Every Aegis trade moved to another Aegis trade-date within the same calendar year (clock times kept): drift, count and per-year P&L preserved, day alignment with MNQ destroyed. Five permutations. If shuffled ≈ real, the benefit is drift, not diversification.

| Tier | Book | Real bust / pass / median | Shuffled bust (5 perms) | Shuffled mean bust | Real H1 / H2 bust | Shuffled mean H1 / H2 |
|---|---|---:|---|---:|---:|---:|
| Tradeify_Growth_100K | MNQx1 + AEGISx2 | 8.4 / 91.6 / 159 | 7.5, 6.4, 8.7, 7.5, 7.5 | 7.5 | 3.4 / 15.1 | 5.7 / 12.3 |
| Tradeify_Growth_100K | MNQx1 + AEGISx3 | 9.1 / 90.9 / 146 | 7.8, 6.0, 9.5, 7.0, 7.7 | 7.6 | 3.7 / 15.1 | 6.8 / 11.0 |
| Tradeify_Select_100K | MNQx1 + AEGISx2 | 14.4 / 85.6 / 155 | 13.4, 12.0, 15.3, 14.2, 14.3 | 13.9 | 7.9 / 25.8 | 11.6 / 22.2 |
| Tradeify_Select_100K | MNQx1 + AEGISx3 | 15.0 / 85.0 / 142 | 14.2, 12.0, 15.9, 13.7, 14.0 | 14.0 | 8.5 / 25.1 | 13.3 / 20.5 |

### (B) Aegis alone on the regime the grid cannot see — 2020-02-24 → 2022-07-31 (sanctioned 1-tick panel)

| Tier | Book | bust % | pass % | unresolved % | median days (passes) | H1 bust | H2 bust |
|---|---|---:|---:|---:|---:|---:|---:|
| Tradeify_Select_100K | AEGISx2 | 11.3 | 0.03 | 88.6 | 883.0 | 32.7 | 2.2 |
| Tradeify_Select_100K | AEGISx3 | 41.4 | 1.50 | 57.1 | 1223.0 | 66.9 | 16.2 |
| Tradeify_Select_100K | AEGISx4 | 66.1 | 6.03 | 27.8 | 1101.0 | 86.1 | 35.7 |
| Tradeify_Growth_100K | AEGISx2 | 5.1 | 0.03 | 94.8 | 883.0 | 18.9 | 0.8 |
| Tradeify_Growth_100K | AEGISx3 | 27.3 | 1.50 | 71.2 | 1223.0 | 54.7 | 8.8 |
| Tradeify_Growth_100K | AEGISx4 | 52.9 | 6.13 | 41.0 | 1115.5 | 78.0 | 24.1 |

### (C) Daily P&L co-movement on the common window (per contract)

| Pair | corr (active days) | P(both lose) | P(independent) | ratio |
|---|---:|---:|---:|---:|
| MNQ–MYM | 0.177 | 0.142 | 0.114 | 1.25 |
| MNQ–AEGIS | 0.034 | 0.009 | 0.018 | 0.49 |
| MYM–AEGIS | -0.018 | 0.037 | 0.035 | 1.06 |

| Leg | trade days | mean $/trade-day per contract | worst day per contract | skew (active days) |
|---|---:|---:|---:|---:|
| MNQ | 560 | $50 | $-1066 | 0.10 |
| MYM | 966 | $12 | $-827 | 4.46 |
| AEGIS | 120 | $26 | $-200 | 1.19 |
