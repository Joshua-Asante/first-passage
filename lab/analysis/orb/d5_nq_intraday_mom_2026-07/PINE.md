# D5 Baltussen H1 — NQ Pine reconstruction

**Status:** research reconstruction of a **FALSIFIED** construct. Not a live
candidate, not a re-proposal, not a lock.

**Source:** [`d5_baltussen_h1_nq.pine`](d5_baltussen_h1_nq.pine) (tracked — no
live edge; same durability exception class as the TOM-SPX concept harness).

**Owners (do not restate numbers here):**

- Frozen H1 + Stage-2 IS kill — [`RESULTS.md`](RESULTS.md)
- OOS decay confirmation — [`d5_recost RESULTS`](../../../archive/d5_recost_2026-07/RESULTS.md)
- Stage-0 freeze — [`D5 pre-reg`](../../../../docs/briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md)
- Instrument standing — [`NQ.md` N3](../../../../ops/instruments/NQ.md)

Re-proposal of this cell needs **new mechanism evidence**, not a new window or
cost model.

## Frozen H1 (what the script implements)

| Piece | Pin |
|---|---|
| Clock | America/New_York RTH 09:30–16:00 |
| Predictor | `r_rod = ln(C_15:30 / O_09:30)` |
| Response | `r_last = ln(C_16:00 / O_15:30)` |
| Trade | `sign(r_rod)` at next-bar open after the 15:30 close (= `O_15:30`), exit immediately at the 16:00 close, one RT/session |
| Both sides | long if `r_rod > 0`, short if `r_rod < 0`, skip if 0 |
| Incomplete RTH | no 09:30 open captured, or no bar that closes at 15:30 (early-close holidays) → no trade |

The 15:30 / 16:00 split is a **constant**, not an input. H2 (alternate window)
was dropped at Stage-0; changing the split is a new candidate.

## How to load on TradingView

1. Chart: `NQ1!` (volume-continuous — [`NQ.md` W1](../../../../ops/instruments/NQ.md)). `MNQ1!` is the micro sibling of the same construct.
2. Timeframe: **1m** (research-native) or **30m**. Any TF that opens a bar at 09:30 and closes a bar at 15:30 and 16:00 works (5m / 15m). 1h will not fire — the table flags it.
3. Timezone of the *clock inside the script* is `America/New_York` regardless of chart timezone. Chart timezone ET is still the least confusing.
4. Paste the `.pine` into the Pine Editor → Add to chart. Commission / slippage default to 0; set them in *Properties* if you want a costed TV export. The campaign's Stage-2 economics live on [`RESULTS.md`](RESULTS.md), not in this script.
5. One contract by default. This is not a live-sizing path.

## What a TV export will not reproduce

- The Databento `NQ.FUT` parent stitch used for IS, or `MNQ.v.0` used for OOS.
- The complete-RTH session filter as implemented in the archived Stage-2 runner (TV just skips days with no 09:30 or 15:30 bar).
- The 4× cost-law hurdle. TV's strategy tester is not Stage-2.

A TV export is a **visual / fill-path check** of the frozen H1, not a substitute
for the campaign RESULTS.
