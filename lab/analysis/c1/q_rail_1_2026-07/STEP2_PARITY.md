# Q-RAIL-1 F3 Step 2 — per-candle CFD timing parity (2026-07-17)

**Limb:** FUTURES_LOCK acceptance — per-candle parity vs CFD source (force-flat OFF).  
**Verdict:** **PASS** (MNQ clean; MYM **PASS-via-operator-override**).

## Exports compared

| Role | File |
|---|---|
| MYM venue on PEPPERSTONE:US30 | `Striker_DJ30_v4.5_MYM_PEPPERSTONE_US30_2026-07-17_15aef.csv` |
| CFD DJ30 (corrected) | `Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-07-17_30a8e.csv` |
| MNQ venue on PEPPERSTONE:NAS100 | `Striker_NAS100_MNQ_PEPPERSTONE_NAS100_2026-07-17_2d574.csv` |
| CFD NAS100 (corrected) | `Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-07-17_4709d.csv` |

Prior CFD pair (`ab1df` / `8aee7`) superseded — CFD ran with DD enforcement (`DD Limit` exits); corrected pair has no force-flat / no DD Limit signals.

## MNQ — PASS

- 48/48 trades; entry + exit `(trade#, side, dir, dt)` identical.
- Signal column identical; size differs by construction.
- Force-flat OFF both sides.

## MYM — PASS-via-operator-override

**Clean:** entries match through T19; no force-flat / no DD Limit on corrected CFD.

**Divergence (not scored as port defect):**

1. **Extra MYM entry `2025-12-02 10:45`** after shared T19 `10:00→10:15`, then trade-# cascade.  
   **Mechanism (operator-accepted):** same day-stop % with **larger CFD size** → larger day P&L hit after T19 → CFD soft-halts; MYM (smaller integer size) still free to re-enter. Size→state coupling on the shared Pepperstone chart — not a signal-port miss.  
   **Operator override 2026-07-17:** do **not** FAIL Step 2 on this limb.

2. **Residual exit lags** (same `Exit Long`/`Add` signal, MYM later than CFD) — **corrected census, 2026-07-18** (adversarial re-audit; original wording understated this): **9 lagged exits**, not 3, bound **not** "1–3 bars":

   | Pair | Lag | Date |
   |---|---:|---|
   | T9 | +3 bars | — |
   | T11 | +2 bars | — |
   | T12 | +2 bars | — |
   | T25 | +1 bar | 2026-01-06 |
   | T26 | +1 bar | 2026-01-06 |
   | T29 | **+10 bars (2.5h)** | 2026-02-08 22:30 → 02-09 01:00 |
   | T30 | **+10 bars (2.5h)** | 2026-02-08 22:30 → 02-09 01:00 |
   | T37 | +1 bar | 2026-05-29 |
   | T42 | +3 bars | 2026-06-30 |

   Absorbed under the same override as fill-path / size-coupling residual on the CFD chart; not treated as halt-grade port defect. Revisit if CME-native 1a rung shows the same lag vs a same-size control (still deferred, per original wording).

**Operator re-affirmation (2026-07-18):** the override granted 2026-07-17 was granted against the understated 3-lag/"1–3 bars" characterization above. Operator instruction, chat, 2026-07-18: *"re-affirm the override against the corrected census."* Re-affirmed as-is — MYM Step-2 parity stays `PASS-via-operator-override`, entry-cascade mechanism and exit-lag absorption both stand, corrected census carried forward verbatim into [`F_SCORECARD.md`](F_SCORECARD.md) and the GO ADR's standing risk framing. The discharging same-size control (T29/T30's +10-bar lag is the sharpest candidate to re-test) remains the pre-registered revisit condition — unchanged by the re-affirmation, still open before any live-fill claim leans on MYM CME-native timing precision.

## F3 impact

Step-2 parity limb **discharged** (re-affirmed 2026-07-18 against the corrected census above). F3 remains `BLOCKED-ON-INPUT` on **TV-native compile** + **C3 attribution ladder** only.
