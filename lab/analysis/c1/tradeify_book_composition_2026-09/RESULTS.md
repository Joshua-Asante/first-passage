# Three-leg Tradeify book grid — ORB-MNQ recon × ORB-MYM × Aegis-6J1

**Status:** EXPLORATORY — informal Downloads-lane measurement, not pre-registered, no K entry; the harness reuses `core/mc/simulation.py` and `core/mc/preflight.py` verbatim. Inputs are operator TradingView exports (uncommitted). See `book_grid.py` docstring for the exact files and unit conventions.

## Verdict (2026-09-01, corrected 2026-09-02 after Codex review of PR #260)

**No configuration is a clear winner on all three axes (bust, pass, time).** The grid has a genuine bust-versus-speed frontier, and the controls change how the Aegis cells should be read. What the 88-cell screen, the six full-N finalists (30,000 paths each) and the controls settle:

1. **Any leg at 2 contracts is out.** Every book containing MNQ×2 or MYM×2 busts 40% to 66% on both tiers. Sizing, not composition, is the first-order variable; the second is the tier.
2. **Growth beats Select by more than any composition change.** Same books, same clock: MNQ×1 19.4% → 11.2% bust, MNQ×1+Aegis×2 15.2% → 8.1%, at effectively unchanged medians. The $500 wider rope is the biggest lever in the grid.
3. **MYM v0.4 hurts every book it joins.** MNQ×1 → MNQ×1+MYM×1 on Growth: 11.2% → 22.6% bust. Its losses coincide with MNQ's 25% more often than independence (joint-loss ratio 1.25), its per-trade-day expectancy is a quarter of MNQ's ($12 vs $50 per contract), and its active-day skew is 4.5 (rare big wins, many small losses). Drop it as a leg. The v0.3 long-only export is no better, and this bootstrap does not reproduce the 19.5%-bust rolling-start figure in `ops/instruments/MYM.md` M9.
4. **Aegis as ballast improves MNQ×1 on all three axes, but for the wrong reason.** MNQ×1+Aegis×2 vs MNQ×1 on Growth: bust 8.1% vs 11.2%, median 161 vs 190 days. But the shuffled-Aegis control — a true derangement of its trade dates within each year, drift kept, co-movement destroyed — busts 8.27% on Growth (5 draws) against the real book's 8.63% at screen N. The control matches or beats the real book, so the gain is Aegis's positive drift over 2022-2026, not diversification. On its excluded 2020-02→2022-07 window Aegis×2 passes 0.03% of paths (5.1% bust on Growth, 11.3% on Select) and Aegis×3 busts 27%/41%.
5. **Aegis alone is the only thing under the frozen 5% ceiling, and only on the favourable window.** Aegis×3 on Growth: 2.3% bust, 95.4% pass, median 602 days, but only 47% of weeks carry a trade (a token trade roughly every other week) and the same size busts 27% on the excluded regime.

**Defensible picks, in order, under the fee-priced criterion (pass ≥ 60%, median ≤ 200 days, worse half ≥ 50%):**

| Book | Tier | bust | pass | median days | worse-half pass |
|---|---|---:|---:|---:|---:|
| MNQx1 + AEGISx2 | Growth | 8.1% | 91.9% | 161 | 85% |
| MNQx1 | Growth | 11.2% | 88.8% | 190 | 78% |
| MNQx1 + AEGISx2 | Select | 15.2% | 84.8% | 154 | 74% |
| MNQx1 + MYMx1 + AEGISx2 | Growth | 19.5% | 80.5% | 108 | 76% |

The first pick carries a regime bet (Aegis's drift) and needs a short-side rail change plus a 6J Python port. The second needs neither and costs about a month. The fourth is fastest and pays for it in bust.

**Bounds, stated plainly.** The bootstrap breaks the realized sequence and is the pessimistic read: every finalist's realized path passes (day 79-156, max drawdown 1.9-2.2%) and rolling starts never bust. The intraday channel is a trade-level sweep-line from TradingView's own adverse-excursion figures, not a bar replay. The window starts 2022-08-01 because MYM v0.4 does, so MNQ's 2020-2021 and Aegis's 2020-2022 sit outside it. The MNQ and MYM lineages are tuned charts with no untouched holdout. Aegis uses the sanctioned 1-tick `76620` panel; the `cbcc9`/`c59e9` exports fill one tick better on every shared trade and are barred. Growth's soft $2,500 daily lockout is not modelled, so Growth figures are two-sided bounds. P&L booked on a non-session date used to be dropped by the business-day reindex -- 6 trades, -210.92 per contract of real losses; that is fixed and these figures include it (bust rose in 10 of 12 finalist cells, by at most 0.55 pp, and fell in none). See README.md §Disclosed limits for what remains disclosed rather than fixed.

## Finalists at full N

n_sims=10000 × seeds [42, 123, 2026] = 30,000 bootstrap paths per cell; elapsed 3581.7s. Bootstrap = 5-day block resample through `run_seed`, intraday-honest channel (timestamp-sequenced trade-level floor). Halves split at the window's business-day midpoint. Rolling = deterministic replay from every start day (intraday clock). E[fee] = $265 + $169 × (1−p)/p on resolved paths.

### Tradeify_Growth_100K — window 2022-08-01 → 2026-07-01 (1023 business days)

| Book | micro-eq | bust % (±SE) | pass % | unresolved % | median days | H1 bust/pass | H2 bust/pass | rolling pass/bust/unres | weekly cov | E[fee] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AEGISx3 | 30 | 2.3 ± 0.1 | 95.4 | 2.3 | 602 | 8.1 / 87.2 | 0.3 / 99.2 | 49 / 0 / 51 | 47% | $269 |
| MNQx1 + AEGISx2 | 21 | 8.1 ± 0.2 | 91.9 | 0.0 | 161 | 3.7 / 96.3 | 15.5 / 84.5 | 80 / 0 / 20 | 100% | $280 |
| MNQx1 + AEGISx3 | 31 | 8.7 ± 0.2 | 91.3 | 0.0 | 146 | 4.0 / 96.0 | 15.2 / 84.8 | 84 / 0 / 16 | 100% | $281 |
| MNQx1 | 1 | 11.2 ± 0.2 | 88.8 | 0.0 | 190 | 6.5 / 93.5 | 22.1 / 77.9 | 70 / 0 / 30 | 99% | $286 |
| MNQx1 + MYMx1 + AEGISx2 | 22 | 19.5 ± 0.2 | 80.5 | 0.0 | 108 | 14.8 / 85.2 | 23.6 / 76.4 | 88 / 0 / 12 | 100% | $306 |
| MNQx1 + MYMx1 | 2 | 22.6 ± 0.2 | 77.4 | 0.0 | 121 | 17.5 / 82.5 | 30.7 / 69.3 | 83 / 0 / 17 | 100% | $314 |

**Pareto set (not dominated beyond 2 SE on bust/pass with ≤ median days):** AEGISx3; MNQx1 + AEGISx2; MNQx1 + AEGISx3; MNQx1 + MYMx1 + AEGISx2

Standalone legs on this tier:

- AEGISx3: bust 2.3%, pass 95.4%, median 602.0 days, weekly coverage 47%
- MNQx1: bust 11.2%, pass 88.8%, median 190.0 days, weekly coverage 99%

### Tradeify_Select_100K — window 2022-08-01 → 2026-07-01 (1023 business days)

| Book | micro-eq | bust % (±SE) | pass % | unresolved % | median days | H1 bust/pass | H2 bust/pass | rolling pass/bust/unres | weekly cov | E[fee] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AEGISx3 | 30 | 5.1 ± 0.1 | 93.2 | 1.7 | 596 | 14.7 / 82.3 | 0.9 / 98.6 | 49 / 0 / 51 | 47% | $274 |
| MNQx1 + AEGISx2 | 21 | 15.2 ± 0.2 | 84.8 | 0.0 | 154 | 8.3 / 91.7 | 25.9 / 74.1 | 80 / 0 / 20 | 100% | $295 |
| MNQx1 + AEGISx3 | 31 | 15.8 ± 0.2 | 84.2 | 0.0 | 140 | 8.8 / 91.2 | 25.3 / 74.7 | 84 / 0 / 16 | 100% | $297 |
| MNQx1 | 1 | 19.4 ± 0.2 | 80.6 | 0.0 | 181 | 12.7 / 87.3 | 34.0 / 66.0 | 70 / 0 / 30 | 99% | $306 |
| MNQx1 + MYMx1 + AEGISx2 | 22 | 30.4 ± 0.3 | 69.6 | 0.0 | 102 | 24.7 / 75.3 | 37.3 / 62.7 | 88 / 0 / 12 | 100% | $339 |
| MNQx1 + MYMx1 | 2 | 34.1 ± 0.3 | 65.9 | 0.0 | 115 | 27.7 / 72.3 | 44.9 / 55.1 | 83 / 0 / 17 | 100% | $353 |

**Pareto set (not dominated beyond 2 SE on bust/pass with ≤ median days):** AEGISx3; MNQx1 + AEGISx2; MNQx1 + AEGISx3; MNQx1 + MYMx1 + AEGISx2

Standalone legs on this tier:

- AEGISx3: bust 5.1%, pass 93.2%, median 596.0 days, weekly coverage 47%
- MNQx1: bust 19.4%, pass 80.6%, median 181.0 days, weekly coverage 99%

## Screen grid — MNQ {0,1,2} × MYM v0.4 {0,1,2} × Aegis {0..4}

n_sims=1000 × seeds [42, 123, 2026] = 3,000 bootstrap paths per cell; elapsed 1477.9s. Bootstrap = 5-day block resample through `run_seed`, intraday-honest channel (timestamp-sequenced trade-level floor). Halves split at the window's business-day midpoint. Rolling = deterministic replay from every start day (intraday clock). E[fee] = $265 + $169 × (1−p)/p on resolved paths.

### Tradeify_Growth_100K — window 2022-08-01 → 2026-07-01 (1023 business days)

| Book | micro-eq | bust % (±SE) | pass % | unresolved % | median days | H1 bust/pass | H2 bust/pass | rolling pass/bust/unres | weekly cov | E[fee] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AEGISx3 | 30 | 2.5 ± 0.3 | 95.0 | 2.6 | 593 | 7.5 / 87.5 | 0.2 / 99.2 | 49 / 0 / 51 | 47% | $269 |
| AEGISx4 | 40 | 6.9 ± 0.5 | 92.6 | 0.5 | 423 | 18.0 / 81.3 | 1.7 / 98.3 | 64 / 0 / 36 | 47% | $278 |
| MNQx1 + AEGISx2 | 21 | 8.6 ± 0.5 | 91.4 | 0.0 | 160 | 3.7 / 96.3 | 15.0 / 85.0 | 80 / 0 / 20 | 100% | $281 |
| MNQx1 + AEGISx3 | 31 | 9.4 ± 0.5 | 90.6 | 0.0 | 146 | 4.1 / 95.9 | 14.9 / 85.1 | 84 / 0 / 16 | 100% | $282 |
| MNQx1 + AEGISx1 | 11 | 9.4 ± 0.5 | 90.6 | 0.0 | 175 | 4.2 / 95.8 | 16.7 / 83.3 | 72 / 0 / 28 | 100% | $283 |
| MNQx1 + AEGISx4 | 41 | 10.3 ± 0.6 | 89.7 | 0.0 | 135 | 4.7 / 95.3 | 15.5 / 84.5 | 87 / 0 / 13 | 100% | $284 |
| MNQx1 | 1 | 12.3 ± 0.6 | 87.7 | 0.0 | 190 | 6.8 / 93.2 | 21.4 / 78.6 | 70 / 0 / 30 | 99% | $289 |
| AEGISx2 | 20 | 0.3 ± 0.1 | 87.1 | 12.6 | 868 | 1.1 / 75.1 | 0.0 / 95.5 | 15 / 0 / 85 | 47% | $266 |
| MYMx1 + AEGISx2 | 21 | 16.4 ± 0.7 | 83.6 | 0.0 | 280 | 20.9 / 79.1 | 7.3 / 92.7 | 74 / 0 / 26 | 100% | $298 |
| MYMx1 + AEGISx3 | 31 | 17.4 ± 0.7 | 82.6 | 0.0 | 234 | 22.6 / 77.4 | 7.0 / 93.0 | 80 / 0 / 20 | 100% | $301 |
| MYMx1 + AEGISx1 | 11 | 18.2 ± 0.7 | 81.8 | 0.0 | 330 | 21.6 / 78.4 | 11.9 / 88.1 | 69 / 0 / 31 | 100% | $303 |
| MYMx1 + AEGISx4 | 41 | 19.8 ± 0.7 | 80.2 | 0.0 | 198 | 25.6 / 74.4 | 7.6 / 92.4 | 83 / 0 / 17 | 100% | $307 |
| MNQx1 + MYMx1 + AEGISx2 | 22 | 20.1 ± 0.7 | 79.9 | 0.0 | 108 | 14.9 / 85.1 | 23.8 / 76.2 | 88 / 0 / 12 | 100% | $307 |
| MNQx1 + MYMx1 + AEGISx3 | 32 | 20.1 ± 0.7 | 79.9 | 0.0 | 100 | 14.8 / 85.2 | 23.2 / 76.8 | 90 / 0 / 10 | 100% | $307 |
| MNQx1 + MYMx1 + AEGISx4 | 42 | 20.7 ± 0.7 | 79.3 | 0.0 | 92 | 16.0 / 84.0 | 23.0 / 77.0 | 90 / 0 / 10 | 100% | $309 |
| MNQx1 + MYMx1 + AEGISx1 | 12 | 21.6 ± 0.8 | 78.4 | 0.0 | 116 | 16.0 / 84.0 | 26.9 / 73.1 | 86 / 0 / 14 | 100% | $312 |
| MNQx1 + MYMx1 | 2 | 24.2 ± 0.8 | 75.8 | 0.0 | 121 | 17.8 / 82.2 | 31.0 / 69.0 | 83 / 0 / 17 | 100% | $319 |
| MYMx1 | 1 | 26.0 ± 0.8 | 74.0 | 0.0 | 378 | 26.1 / 73.9 | 26.3 / 73.3 | 60 / 0 / 40 | 100% | $324 |
| MNQx2 + AEGISx4 | 42 | 40.5 ± 0.9 | 59.5 | 0.0 | 59 | 28.9 / 71.1 | 44.3 / 55.7 | 84 / 13 / 3 | 100% | $380 |
| MNQx2 + AEGISx3 | 32 | 40.8 ± 0.9 | 59.2 | 0.0 | 62 | 29.6 / 70.4 | 45.0 / 55.0 | 84 / 13 / 3 | 100% | $381 |
| MNQx2 + AEGISx2 | 22 | 42.3 ± 0.9 | 57.7 | 0.0 | 65 | 30.6 / 69.4 | 46.3 / 53.7 | 84 / 13 / 3 | 100% | $389 |
| MNQx2 + AEGISx1 | 12 | 43.2 ± 0.9 | 56.8 | 0.0 | 67 | 32.0 / 68.0 | 48.3 / 51.7 | 70 / 26 / 3 | 100% | $394 |
| MYMx2 + AEGISx4 | 42 | 44.2 ± 0.9 | 55.8 | 0.0 | 93 | 49.3 / 50.7 | 42.0 / 58.0 | 55 / 33 / 12 | 100% | $399 |
| MNQx1 + MYMx2 + AEGISx3 | 33 | 44.3 ± 0.9 | 55.7 | 0.0 | 66 | 39.8 / 60.2 | 50.4 / 49.6 | 67 / 24 / 9 | 100% | $399 |
| MNQx1 + MYMx2 + AEGISx4 | 43 | 44.5 ± 0.9 | 55.5 | 0.0 | 62 | 39.0 / 61.0 | 49.2 / 50.8 | 72 / 20 / 8 | 100% | $401 |
| MNQx2 + MYMx1 + AEGISx1 | 13 | 44.7 ± 0.9 | 55.3 | 0.0 | 51 | 40.7 / 59.3 | 49.7 / 50.3 | 55 / 43 / 2 | 100% | $401 |
| MYMx2 + AEGISx3 | 32 | 45.3 ± 0.9 | 54.7 | 0.0 | 103 | 49.0 / 51.0 | 44.0 / 56.0 | 54 / 34 / 12 | 100% | $405 |
| MNQx2 | 2 | 45.5 ± 0.9 | 54.5 | 0.0 | 67 | 35.2 / 64.8 | 51.2 / 48.8 | 69 / 28 / 3 | 99% | $406 |
| MNQx1 + MYMx2 + AEGISx2 | 23 | 45.5 ± 0.9 | 54.5 | 0.0 | 69 | 40.3 / 59.7 | 52.8 / 47.2 | 65 / 26 / 10 | 100% | $406 |
| MNQx2 + MYMx1 + AEGISx4 | 43 | 45.6 ± 0.9 | 54.4 | 0.0 | 47 | 38.4 / 61.6 | 48.5 / 51.5 | 73 / 26 / 2 | 100% | $406 |
| MNQx2 + MYMx1 | 3 | 45.9 ± 0.9 | 54.1 | 0.0 | 51 | 42.0 / 58.0 | 51.0 / 49.0 | 52 / 47 / 2 | 100% | $409 |
| MNQx2 + MYMx1 + AEGISx3 | 33 | 46.3 ± 0.9 | 53.7 | 0.0 | 49 | 39.0 / 61.0 | 49.6 / 50.4 | 71 / 27 / 2 | 100% | $411 |
| MYMx2 + AEGISx2 | 22 | 46.8 ± 0.9 | 53.2 | 0.0 | 110 | 49.5 / 50.5 | 47.5 / 52.5 | 56 / 30 / 15 | 100% | $413 |
| MNQx2 + MYMx1 + AEGISx2 | 23 | 47.1 ± 0.9 | 52.9 | 0.0 | 51 | 39.9 / 60.1 | 50.5 / 49.5 | 58 / 40 / 2 | 100% | $415 |
| MNQx1 + MYMx2 + AEGISx1 | 13 | 47.5 ± 0.9 | 52.5 | 0.0 | 71 | 41.3 / 58.7 | 54.8 / 45.2 | 64 / 26 / 10 | 100% | $418 |
| MYMx2 + AEGISx1 | 12 | 48.8 ± 0.9 | 51.2 | 0.0 | 117 | 51.1 / 48.9 | 51.4 / 48.6 | 53 / 30 / 17 | 100% | $426 |
| MNQx1 + MYMx2 | 3 | 49.5 ± 0.9 | 50.5 | 0.0 | 74 | 42.7 / 57.3 | 58.4 / 41.6 | 63 / 27 / 10 | 100% | $431 |
| MNQx2 + MYMx2 + AEGISx4 | 44 | 52.3 ± 0.9 | 47.7 | 0.0 | 37 | 50.0 / 50.0 | 55.6 / 44.4 | 60 / 39 / 1 | 100% | $451 |
| MNQx2 + MYMx2 + AEGISx3 | 34 | 52.9 ± 0.9 | 47.1 | 0.0 | 38 | 50.2 / 49.8 | 56.5 / 43.5 | 57 / 41 / 1 | 100% | $455 |
| MNQx2 + MYMx2 + AEGISx2 | 24 | 53.7 ± 0.9 | 46.3 | 0.0 | 39 | 50.5 / 49.5 | 57.4 / 42.6 | 55 / 44 / 1 | 100% | $461 |
| MYMx2 | 2 | 53.9 ± 0.9 | 46.1 | 0.0 | 121 | 53.2 / 46.8 | 57.2 / 42.8 | 50 / 32 / 18 | 100% | $462 |
| MNQx2 + MYMx2 + AEGISx1 | 14 | 54.9 ± 0.9 | 45.1 | 0.0 | 40 | 51.1 / 48.9 | 58.8 / 41.2 | 55 / 44 / 1 | 100% | $470 |
| MNQx2 + MYMx2 | 4 | 55.8 ± 0.9 | 44.2 | 0.0 | 40 | 52.4 / 47.6 | 60.0 / 40.0 | 53 / 45 / 2 | 100% | $478 |
| AEGISx1 | 10 | 0.0 ± 0.0 | 21.2 | 78.8 | 1311 | 0.0 / 13.7 | 0.0 / 34.0 | 0 / 0 / 100 | 47% | $265 |

**Pareto set (not dominated beyond 2 SE on bust/pass with ≤ median days):** AEGISx3; AEGISx4; MNQx1 + AEGISx2; MNQx1 + AEGISx3; MNQx1 + AEGISx1; MNQx1 + AEGISx4; AEGISx2; MNQx1 + MYMx1 + AEGISx2; MNQx1 + MYMx1 + AEGISx3; MNQx1 + MYMx1 + AEGISx4; MNQx1 + MYMx1 + AEGISx1; MNQx2 + AEGISx4; MNQx2 + AEGISx3; MNQx2 + AEGISx2; MNQx2 + MYMx1 + AEGISx1; MNQx2 + MYMx1 + AEGISx4; MNQx2 + MYMx1; MNQx2 + MYMx1 + AEGISx3; MNQx2 + MYMx1 + AEGISx2; MNQx2 + MYMx2 + AEGISx4; MNQx2 + MYMx2 + AEGISx3; MNQx2 + MYMx2 + AEGISx2; MNQx2 + MYMx2 + AEGISx1; AEGISx1

Standalone legs on this tier:

- AEGISx1: bust 0.0%, pass 21.2%, median 1311.0 days, weekly coverage 47%
- AEGISx2: bust 0.3%, pass 87.1%, median 867.5 days, weekly coverage 47%
- AEGISx3: bust 2.5%, pass 95.0%, median 593.0 days, weekly coverage 47%
- AEGISx4: bust 6.9%, pass 92.6%, median 423.0 days, weekly coverage 47%
- MNQx1: bust 12.3%, pass 87.7%, median 190.0 days, weekly coverage 99%
- MNQx2: bust 45.5%, pass 54.5%, median 67.0 days, weekly coverage 99%
- MYMx1: bust 26.0%, pass 74.0%, median 378.0 days, weekly coverage 100%
- MYMx2: bust 53.9%, pass 46.1%, median 121.0 days, weekly coverage 100%

### Tradeify_Select_100K — window 2022-08-01 → 2026-07-01 (1023 business days)

| Book | micro-eq | bust % (±SE) | pass % | unresolved % | median days | H1 bust/pass | H2 bust/pass | rolling pass/bust/unres | weekly cov | E[fee] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AEGISx3 | 30 | 5.0 ± 0.4 | 92.8 | 2.2 | 586 | 14.0 / 82.6 | 1.0 / 98.5 | 49 / 0 / 51 | 47% | $274 |
| AEGISx4 | 40 | 12.7 ± 0.6 | 87.3 | 0.1 | 406 | 26.7 / 73.1 | 4.0 / 96.0 | 64 / 0 / 36 | 47% | $290 |
| AEGISx2 | 20 | 0.6 ± 0.1 | 87.0 | 12.4 | 867 | 2.7 / 74.8 | 0.1 / 95.5 | 15 / 0 / 85 | 47% | $266 |
| MNQx1 + AEGISx2 | 21 | 14.8 ± 0.6 | 85.2 | 0.0 | 155 | 8.7 / 91.3 | 25.6 / 74.4 | 80 / 0 / 20 | 100% | $294 |
| MNQx1 + AEGISx3 | 31 | 15.6 ± 0.7 | 84.4 | 0.0 | 142 | 9.1 / 90.9 | 24.7 / 75.3 | 84 / 0 / 16 | 100% | $296 |
| MNQx1 + AEGISx1 | 11 | 16.1 ± 0.7 | 83.9 | 0.0 | 167 | 9.7 / 90.3 | 28.4 / 71.6 | 72 / 0 / 28 | 100% | $297 |
| MNQx1 + AEGISx4 | 41 | 18.3 ± 0.7 | 81.7 | 0.0 | 127 | 10.6 / 89.4 | 25.3 / 74.7 | 87 / 0 / 13 | 100% | $303 |
| MNQx1 | 1 | 20.1 ± 0.7 | 79.9 | 0.0 | 180 | 13.1 / 86.9 | 33.5 / 66.5 | 70 / 0 / 30 | 99% | $307 |
| MYMx1 + AEGISx2 | 21 | 26.3 ± 0.8 | 73.7 | 0.0 | 280 | 31.0 / 69.0 | 15.7 / 84.3 | 74 / 0 / 26 | 100% | $325 |
| MYMx1 + AEGISx3 | 31 | 28.0 ± 0.8 | 72.0 | 0.0 | 232 | 32.9 / 67.1 | 15.2 / 84.8 | 80 / 0 / 20 | 100% | $331 |
| MYMx1 + AEGISx1 | 11 | 29.1 ± 0.8 | 70.9 | 0.0 | 334 | 32.0 / 68.0 | 23.5 / 76.5 | 65 / 0 / 35 | 100% | $334 |
| MYMx1 + AEGISx4 | 41 | 29.3 ± 0.8 | 70.7 | 0.0 | 196 | 35.8 / 64.2 | 17.3 / 82.7 | 83 / 0 / 17 | 100% | $335 |
| MNQx1 + MYMx1 + AEGISx2 | 22 | 30.7 ± 0.8 | 69.3 | 0.0 | 104 | 25.8 / 74.2 | 37.2 / 62.8 | 88 / 0 / 12 | 100% | $340 |
| MNQx1 + MYMx1 + AEGISx4 | 42 | 30.9 ± 0.8 | 69.1 | 0.0 | 90 | 26.3 / 73.7 | 34.3 / 65.7 | 90 / 0 / 10 | 100% | $340 |
| MNQx1 + MYMx1 + AEGISx3 | 32 | 30.9 ± 0.8 | 69.1 | 0.0 | 96 | 25.4 / 74.6 | 34.8 / 65.2 | 90 / 0 / 10 | 100% | $341 |
| MNQx1 + MYMx1 + AEGISx1 | 12 | 31.6 ± 0.8 | 68.4 | 0.0 | 111 | 26.7 / 73.3 | 40.5 / 59.5 | 86 / 0 / 14 | 100% | $343 |
| MNQx1 + MYMx1 | 2 | 34.5 ± 0.9 | 65.5 | 0.0 | 116 | 28.2 / 71.8 | 44.8 / 55.2 | 83 / 0 / 17 | 100% | $354 |
| MYMx1 | 1 | 38.7 ± 0.9 | 61.3 | 0.0 | 378 | 37.3 / 62.7 | 42.6 / 57.2 | 3 / 41 / 56 | 100% | $372 |
| MNQx2 + AEGISx4 | 42 | 51.6 ± 0.9 | 48.4 | 0.0 | 54 | 42.4 / 57.6 | 54.5 / 45.5 | 66 / 33 / 2 | 100% | $445 |
| MNQx2 + AEGISx3 | 32 | 52.5 ± 0.9 | 47.5 | 0.0 | 56 | 42.3 / 57.7 | 55.2 / 44.8 | 51 / 48 / 2 | 100% | $452 |
| MNQx2 + AEGISx2 | 22 | 54.2 ± 0.9 | 45.8 | 0.0 | 59 | 43.2 / 56.8 | 56.5 / 43.5 | 49 / 49 / 2 | 100% | $465 |
| MNQx1 + MYMx2 + AEGISx3 | 33 | 54.5 ± 0.9 | 45.5 | 0.0 | 60 | 51.4 / 48.6 | 59.6 / 40.4 | 65 / 33 / 2 | 100% | $468 |
| MNQx1 + MYMx2 + AEGISx4 | 43 | 54.7 ± 0.9 | 45.3 | 0.0 | 57 | 51.5 / 48.5 | 59.0 / 41.0 | 69 / 30 / 2 | 100% | $469 |
| MNQx2 + AEGISx1 | 12 | 54.9 ± 0.9 | 45.1 | 0.0 | 60 | 44.0 / 56.0 | 58.5 / 41.5 | 44 / 53 / 3 | 100% | $471 |
| MNQx1 + MYMx2 + AEGISx2 | 23 | 55.6 ± 0.9 | 44.4 | 0.0 | 63 | 51.7 / 48.3 | 61.2 / 38.8 | 62 / 37 / 2 | 100% | $476 |
| MNQx2 | 2 | 56.8 ± 0.9 | 43.2 | 0.0 | 61 | 46.0 / 54.0 | 61.2 / 38.8 | 40 / 57 / 3 | 99% | $487 |
| MYMx2 + AEGISx4 | 42 | 57.4 ± 0.9 | 42.6 | 0.0 | 90 | 58.7 / 41.3 | 61.2 / 38.8 | 46 / 42 / 12 | 100% | $492 |
| MNQx1 + MYMx2 + AEGISx1 | 13 | 57.5 ± 0.9 | 42.5 | 0.0 | 65 | 53.0 / 47.0 | 63.0 / 37.0 | 61 / 37 / 2 | 100% | $494 |
| MNQx2 + MYMx1 + AEGISx4 | 43 | 57.6 ± 0.9 | 42.4 | 0.0 | 45 | 52.4 / 47.6 | 59.3 / 40.7 | 53 / 45 / 1 | 100% | $494 |
| MNQx2 + MYMx1 + AEGISx3 | 33 | 58.1 ± 0.9 | 41.9 | 0.0 | 45 | 52.9 / 47.1 | 59.7 / 40.3 | 50 / 48 / 1 | 100% | $500 |
| MYMx2 + AEGISx3 | 32 | 58.5 ± 0.9 | 41.5 | 0.0 | 100 | 58.8 / 41.2 | 63.4 / 36.6 | 42 / 46 / 12 | 100% | $503 |
| MNQx2 + MYMx1 + AEGISx2 | 23 | 58.6 ± 0.9 | 41.4 | 0.0 | 47 | 53.0 / 47.0 | 61.6 / 38.4 | 48 / 51 / 2 | 100% | $504 |
| MNQx1 + MYMx2 | 3 | 59.4 ± 0.9 | 40.6 | 0.0 | 67 | 54.4 / 45.6 | 66.0 / 34.0 | 60 / 38 / 2 | 100% | $513 |
| MYMx2 + AEGISx2 | 22 | 59.8 ± 0.9 | 40.2 | 0.0 | 110 | 59.8 / 40.2 | 67.6 / 32.4 | 36 / 49 / 15 | 100% | $516 |
| MNQx2 + MYMx1 + AEGISx1 | 13 | 59.9 ± 0.9 | 40.1 | 0.0 | 48 | 53.2 / 46.8 | 62.7 / 37.3 | 45 / 53 / 2 | 100% | $517 |
| MNQx2 + MYMx1 | 3 | 61.0 ± 0.9 | 39.0 | 0.0 | 49 | 54.1 / 45.9 | 64.9 / 35.1 | 42 / 56 / 2 | 100% | $529 |
| MYMx2 + AEGISx1 | 12 | 62.0 ± 0.9 | 38.0 | 0.0 | 117 | 60.9 / 39.1 | 71.8 / 28.2 | 34 / 49 / 17 | 100% | $541 |
| MNQx2 + MYMx2 + AEGISx3 | 34 | 62.5 ± 0.9 | 37.5 | 0.0 | 36 | 59.1 / 40.9 | 67.8 / 32.2 | 37 / 62 / 1 | 100% | $546 |
| MNQx2 + MYMx2 + AEGISx4 | 44 | 62.6 ± 0.9 | 37.4 | 0.0 | 35 | 59.4 / 40.6 | 66.9 / 33.1 | 39 / 60 / 1 | 100% | $547 |
| MNQx2 + MYMx2 + AEGISx2 | 24 | 62.8 ± 0.9 | 37.2 | 0.0 | 37 | 58.9 / 41.1 | 68.3 / 31.7 | 36 / 64 / 1 | 100% | $550 |
| MNQx2 + MYMx2 + AEGISx1 | 14 | 63.8 ± 0.9 | 36.2 | 0.0 | 37 | 59.7 / 40.3 | 69.2 / 30.8 | 36 / 63 / 1 | 100% | $562 |
| MNQx2 + MYMx2 | 4 | 64.7 ± 0.9 | 35.3 | 0.0 | 39 | 60.7 / 39.3 | 70.5 / 29.5 | 31 / 68 / 1 | 100% | $575 |
| MYMx2 | 2 | 66.6 ± 0.9 | 33.4 | 0.0 | 124 | 63.0 / 37.0 | 76.7 / 23.3 | 32 / 49 / 18 | 100% | $602 |
| AEGISx1 | 10 | 0.0 ± 0.0 | 21.2 | 78.8 | 1311 | 0.0 / 13.7 | 0.0 / 34.0 | 0 / 0 / 100 | 47% | $265 |

**Pareto set (not dominated beyond 2 SE on bust/pass with ≤ median days):** AEGISx3; AEGISx4; AEGISx2; MNQx1 + AEGISx2; MNQx1 + AEGISx3; MNQx1 + AEGISx1; MNQx1 + AEGISx4; MNQx1 + MYMx1 + AEGISx2; MNQx1 + MYMx1 + AEGISx4; MNQx1 + MYMx1 + AEGISx3; MNQx1 + MYMx1 + AEGISx1; MNQx2 + AEGISx4; MNQx2 + AEGISx3; MNQx2 + AEGISx2; MNQx2 + MYMx1 + AEGISx4; MNQx2 + MYMx1 + AEGISx3; MNQx2 + MYMx1 + AEGISx2; MNQx2 + MYMx1 + AEGISx1; MNQx2 + MYMx2 + AEGISx3; MNQx2 + MYMx2 + AEGISx4; MNQx2 + MYMx2 + AEGISx2; MNQx2 + MYMx2 + AEGISx1; MNQx2 + MYMx2; AEGISx1

Standalone legs on this tier:

- AEGISx1: bust 0.0%, pass 21.2%, median 1311.0 days, weekly coverage 47%
- AEGISx2: bust 0.6%, pass 87.0%, median 867.0 days, weekly coverage 47%
- AEGISx3: bust 5.0%, pass 92.8%, median 586.0 days, weekly coverage 47%
- AEGISx4: bust 12.7%, pass 87.3%, median 406.0 days, weekly coverage 47%
- MNQx1: bust 20.1%, pass 79.9%, median 180.0 days, weekly coverage 99%
- MNQx2: bust 56.8%, pass 43.2%, median 61.0 days, weekly coverage 99%
- MYMx1: bust 38.7%, pass 61.3%, median 378.0 days, weekly coverage 100%
- MYMx2: bust 66.6%, pass 33.4%, median 124.0 days, weekly coverage 100%

## Reference cells with the measured MYM v0.3 export (long-only, MYM.md M9)

n_sims=1000 × seeds [42, 123, 2026] = 3,000 bootstrap paths per cell; elapsed 228.3s. Bootstrap = 5-day block resample through `run_seed`, intraday-honest channel (timestamp-sequenced trade-level floor). Halves split at the window's business-day midpoint. Rolling = deterministic replay from every start day (intraday clock). E[fee] = $265 + $169 × (1−p)/p on resolved paths.

### Tradeify_Growth_100K — window 2022-01-03 → 2026-07-01 (1173 business days)

| Book | micro-eq | bust % (±SE) | pass % | unresolved % | median days | H1 bust/pass | H2 bust/pass | rolling pass/bust/unres | weekly cov | E[fee] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MNQx1 | 1 | 11.7 ± 0.6 | 88.3 | 0.0 | 176 | 11.0 / 89.0 | 17.1 / 82.9 | 74 / 0 / 26 | 99% | $287 |
| MNQx1 + MYM_V03x1 + AEGISx2 | 22 | 27.3 ± 0.8 | 72.7 | 0.0 | 100 | 26.3 / 73.7 | 28.6 / 71.4 | 91 / 0 / 9 | 100% | $328 |
| MYM_V03x1 | 1 | 30.2 ± 0.8 | 69.7 | 0.2 | 414 | 20.5 / 79.5 | 42.4 / 57.2 | 53 / 0 / 47 | 100% | $338 |
| MNQx1 + MYM_V03x1 | 2 | 32.1 ± 0.9 | 67.9 | 0.0 | 106 | 30.8 / 69.2 | 35.1 / 64.9 | 85 / 0 / 15 | 100% | $345 |
| MYM_V03x2 | 2 | 55.1 ± 0.9 | 44.9 | 0.0 | 136 | 49.7 / 50.3 | 65.7 / 34.3 | 35 / 42 / 23 | 100% | $473 |

**Pareto set (not dominated beyond 2 SE on bust/pass with ≤ median days):** MNQx1; MNQx1 + MYM_V03x1 + AEGISx2

Standalone legs on this tier:

- MNQx1: bust 11.7%, pass 88.3%, median 176.0 days, weekly coverage 99%
- MYM_V03x1: bust 30.2%, pass 69.7%, median 414.0 days, weekly coverage 100%
- MYM_V03x2: bust 55.1%, pass 44.9%, median 136.0 days, weekly coverage 100%

### Tradeify_Select_100K — window 2022-01-03 → 2026-07-01 (1173 business days)

| Book | micro-eq | bust % (±SE) | pass % | unresolved % | median days | H1 bust/pass | H2 bust/pass | rolling pass/bust/unres | weekly cov | E[fee] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MNQx1 | 1 | 19.9 ± 0.7 | 80.1 | 0.0 | 169 | 19.1 / 80.9 | 27.6 / 72.4 | 74 / 0 / 26 | 99% | $307 |
| MNQx1 + MYM_V03x1 + AEGISx2 | 22 | 38.9 ± 0.9 | 61.1 | 0.0 | 91 | 37.4 / 62.6 | 40.9 / 59.1 | 91 / 5 / 4 | 100% | $372 |
| MYM_V03x1 | 1 | 42.5 ± 0.9 | 57.4 | 0.1 | 408 | 30.6 / 69.4 | 57.5 / 42.4 | 22 / 0 / 78 | 100% | $390 |
| MNQx1 + MYM_V03x1 | 2 | 43.7 ± 0.9 | 56.3 | 0.0 | 99 | 41.4 / 58.6 | 48.3 / 51.7 | 85 / 0 / 15 | 100% | $396 |
| MYM_V03x2 | 2 | 71.0 ± 0.8 | 29.0 | 0.0 | 144 | 62.4 / 37.6 | 83.1 / 16.9 | 16 / 57 / 26 | 100% | $678 |

**Pareto set (not dominated beyond 2 SE on bust/pass with ≤ median days):** MNQx1; MNQx1 + MYM_V03x1 + AEGISx2

Standalone legs on this tier:

- MNQx1: bust 19.9%, pass 80.1%, median 169.0 days, weekly coverage 99%
- MYM_V03x1: bust 42.5%, pass 57.4%, median 408.0 days, weekly coverage 100%
- MYM_V03x2: bust 71.0%, pass 29.0%, median 144.0 days, weekly coverage 100%

## Controls

### (A) Shuffled-Aegis control — is Aegis's benefit co-movement or just positive drift?

Every Aegis trade moved to a DIFFERENT Aegis trade-date within the same calendar year (clock times kept): drift, count and per-year P&L preserved, day alignment with MNQ destroyed. Five draws, each a true derangement — a plain permutation leaves ~1 date mapped to itself per draw, which would preserve some of the alignment this control exists to destroy (fixed 2026-09-02, Codex review of PR #260). If shuffled ≈ real, the benefit is drift, not diversification.

| Tier | Book | Real bust / pass / median | Shuffled bust (5 perms) | Shuffled mean bust | Real H1 / H2 bust | Shuffled mean H1 / H2 |
|---|---|---:|---|---:|---:|---:|
| Tradeify_Growth_100K | MNQx1 + AEGISx2 | 8.6 / 91.4 / 160 | 7.6, 7.4, 8.6, 8.2, 9.5 | 8.3 | 3.7 / 15.0 | 5.8 / 11.0 |
| Tradeify_Growth_100K | MNQx1 + AEGISx3 | 9.4 / 90.6 / 146 | 7.3, 7.4, 8.7, 8.9, 10.4 | 8.5 | 4.1 / 14.9 | 6.8 / 9.5 |
| Tradeify_Select_100K | MNQx1 + AEGISx2 | 14.8 / 85.2 / 155 | 13.7, 13.3, 15.7, 15.9, 16.6 | 15.1 | 8.7 / 25.6 | 11.4 / 20.1 |
| Tradeify_Select_100K | MNQx1 + AEGISx3 | 15.6 / 84.4 / 142 | 13.7, 13.7, 15.5, 15.7, 17.5 | 15.2 | 9.1 / 24.7 | 13.2 / 18.0 |

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
| MNQ–MYM | 0.175 | 0.142 | 0.114 | 1.24 |
| MNQ–AEGIS | 0.034 | 0.009 | 0.018 | 0.49 |
| MYM–AEGIS | -0.018 | 0.037 | 0.035 | 1.06 |

| Leg | trade days | mean $/trade-day per contract | worst day per contract | skew (active days) |
|---|---:|---:|---:|---:|
| MNQ | 561 | $49 | $-1066 | 0.10 |
| MYM | 964 | $12 | $-827 | 4.46 |
| AEGIS | 120 | $26 | $-200 | 1.19 |
