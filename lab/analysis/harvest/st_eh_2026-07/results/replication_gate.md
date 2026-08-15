# ST-EH-1 — Phase 2 replication fidelity gate

Engine: `lab/analysis/st_eh_2026-07/engine.py` (ST-EH v0.1 spec, verbatim).
Window: **2025-08-31 -> 2026-07-24**, warm-up from 2025-06-01.
Series: **unadjusted** 15m (the TV exports were taken with back-adjustment OFF —
operator confirmed 2026-07-26). Closed trades only; the TV `Open` row is dropped.

Tolerances (frozen, pre-registration §2): count +/-2% · entry-Jaccard >= 0.95 ·
gross profit & gross loss each +/-5% · direction agreement >= 98%.

### MNQ (MNQ.v.0)

- PASS  `closed_trade_count` — 549 vs 551 (0.36% dev, tol 2%)
- PASS  `entry_jaccard` — 0.9713 (tol >= 0.95)
- PASS  `gross_profit` — $81,778 vs $82,278 (0.61% dev, tol 5%)
- PASS  `gross_loss` — $78,714 vs $80,202 (1.86% dev, tol 5%)
- PASS  `direction_agreement` — 0.9926 on 542 matched (tol >= 0.98)

Matched entries: 542 · engine-only: 7 · TV-only: 9

**VERDICT: PASS**

Panel: 27153 bars · 2025-06-01 18:00:00-04:00 -> 2026-07-24 16:45:00-04:00 · integrity **PASS**  
Contract rolls in window: 5 · roll-spanning trades: **4**

| roll time | from | to | offset (pts) |
|---|---|---|---|
| 2025-06-17 20:00:00-04:00 | 42009475 | 42003472 | +233.00 |
| 2025-09-17 20:00:00-04:00 | 42003472 | 42001149 | +236.00 |
| 2025-12-17 19:00:00-05:00 | 42001149 | 42004946 | +236.00 |
| 2026-03-18 20:00:00-04:00 | 42004946 | 42004936 | +200.50 |
| 2026-06-16 20:00:00-04:00 | 42004936 | 42004800 | +331.75 |

### MYM (MYM.v.0)

- PASS  `closed_trade_count` — 548 vs 550 (0.36% dev, tol 2%)
- PASS  `entry_jaccard` — 0.9642 (tol >= 0.95)
- PASS  `gross_profit` — $25,934 vs $25,781 (0.59% dev, tol 5%)
- PASS  `gross_loss` — $24,152 vs $24,580 (1.74% dev, tol 5%)
- PASS  `direction_agreement` — 0.9926 on 539 matched (tol >= 0.98)

Matched entries: 539 · engine-only: 9 · TV-only: 11

**VERDICT: PASS**

Panel: 27153 bars · 2025-06-01 18:00:00-04:00 -> 2026-07-24 16:45:00-04:00 · integrity **PASS**  
Contract rolls in window: 5 · roll-spanning trades: **4**

| roll time | from | to | offset (pts) |
|---|---|---|---|
| 2025-06-17 20:00:00-04:00 | 42003054 | 42001781 | +344.00 |
| 2025-09-16 20:00:00-04:00 | 42001781 | 42005056 | +338.00 |
| 2025-12-16 19:00:00-05:00 | 42005056 | 42001953 | +327.00 |
| 2026-03-17 20:00:00-04:00 | 42001953 | 42002662 | +309.00 |
| 2026-06-16 20:00:00-04:00 | 42002662 | 42004247 | +437.00 |


---

## GATE VERDICT: **PASS**

Engine licensed for the long-panel work (Phases 3-6).
