# ECR summary — Q-REGIME-FIT-1 window (2026-04-13 → 2026-06-17)

PII-free aggregate (no order IDs / account numbers). Counterfactual = locked backtest signal,
Pepperstone feed, **de-compounded to static $200K** (matches live static sizing — skill trap #9).
Realized = live DXTrade settled PnL. Skips on NAS100 before its ~2026-05-07 go-live are tagged
deployment (un-capturable), not behavioral.

| date | strat | disposition | cf static $ | live $ |
|---|---|---|---:|---:|
| 2026-04-13 | NAS100 | SKIP (deploy) | 14,862 | 0 |
| 2026-04-14 | NAS100 | SKIP (deploy) | 12,796 | 0 |
| 2026-04-13 | Aegis | TAKEN | −63 | 1,224 |
| 2026-04-15 | Aegis | TAKEN-DISCRETIONARY | 6,086 | 362 |
| 2026-04-17 | DJ30 | SKIP (behavioral) | 2,839 | 0 |
| 2026-05-07 | Guardian | TAKEN | −677 | −878 |
| 2026-05-11 | NAS100 | TAKEN | −741 | −825 |
| 2026-05-14 | Guardian | SKIP (behavioral) | −686 | 0 |
| 2026-05-19 | Aegis | TAKEN-DISCRETIONARY | 47 | −2,300 |
| 2026-05-25 | Guardian | TAKEN | −684 | −693 |
| 2026-05-26 | NAS100 | TAKEN | 902 | 846 |
| 2026-05-29 | DJ30 | TAKEN | 380 | 30 |
| 2026-06-01 | NAS100 | TAKEN | −392 | −602 |
| 2026-06-02 | NAS100 | TAKEN | 87 | 46 |
| 2026-06-16 | Guardian | TAKEN | −682 | −716 |
| 2026-06-16 | DJ30 | SKIP (behavioral) | 174 | 0 |

OFF-SPEC live (no backtest signal that day): 04-14 DJ30 +12, 04-14 Guardian +848, 04-16 Guardian −2,366,
05-06 Guardian +860, 05-20 Aegis +2,447 → net **+$1,800** (high-variance, off-system).

## Aggregates

| metric | value |
|---|---:|
| Counterfactual (static $200K, all in-window signals) | **+$34,247** |
| Realized on signal-days | **−$3,507** |
| OFF-SPEC realized | +$1,800 |
| Net realized in-window | **−$1,707** |
| **ECR all-in** (realized / counterfactual) | **−10.2%** |
| Deployment-gap counterfactual (NAS 04-13/04-14, excluded) | $27,658 (81%) |
| **ECR behavioral-only** (deployed: cf $6,589 / real −$3,507) | **−53.2%** |

Live account, full challenge 3/10→6/17: balance **$198,563.72**, settled PnL **−$1,271.71**, financing −$164.57.

**Flag:** ECR far below the 0.70 adequacy floor (and below 0 — the account *lost* money where the signals
made +17%). Primary disposition: FIX-EXECUTION. Largest behavioral leaks: Aegis 04-15 decomposition
(−$5.7K, lesson E2), Aegis 05-19 oversizing/early-exit (−$2.3K), DJ30 04-17 skip (−$2.8K).
