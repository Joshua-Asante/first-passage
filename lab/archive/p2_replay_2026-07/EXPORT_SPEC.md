# P2 replay — TV export spec (4 exports, 2 legs)

**For:** Joshua · **Parent:** `docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md` (K2+E1) · **Harness:** this directory
**Bar:** you should need ZERO clarifying questions at export time — except the window pin below, which is yours.

## Window (REQUIRED-PIN — §0.5-b, yours to fill)

> **Window: ______________** (your §0.5-b pin — handoff convention is trailing 12 months; e.g. **2025-07-03 → 2026-07-03, SUGGESTED, not decided**)

The harness applies the pinned window at ingest (`--window-start/--window-end`) — nothing is hardcoded. Exports must **cover at least** the pinned window; exporting full available history is fine and preferred. One window, one shot (P2 §5.5): no re-export over a different range after seeing results.

## The four exports

| # | Leg | Strategy (exact version) | TV symbol | Filename |
|---|-----|--------------------------|-----------|----------|
| 1 | DJ30 | Striker DJ30 **v4.5** (locked) | `PEPPERSTONE:US30` | `P2_DJ30_PEP_US30_<YYYY-MM-DD>.csv` |
| 2 | DJ30 | Striker DJ30 **v4.5** (same script instance as #1) | `CBOT_MINI:MYM1!` | `P2_DJ30_CME_MYM1_<YYYY-MM-DD>.csv` |
| 3 | NAS100 | Striker NAS100 **v1** (locked) | `PEPPERSTONE:NAS100` | `P2_NAS100_PEP_NAS100_<YYYY-MM-DD>.csv` |
| 4 | NAS100 | Striker NAS100 **v1** (same script instance as #3) | `CME_MINI:MNQ1!` | `P2_NAS100_CME_MNQ1_<YYYY-MM-DD>.csv` |

`<YYYY-MM-DD>` = export date. Guardian is benched, Aegis is off-venue (§0.5-a) — no gold/yen exports.

## Identical-settings checklist (per leg, between its two exports)

Zero parameter changes — locks HELD. For each leg, both exports come from the **same applied strategy instance**, changing ONLY the chart symbol:

- [ ] Same `.pine` script + version (v4.5 / v1); every input at its locked value; **no re-tuning to the futures feed** (ADR §5.1).
- [ ] Any TV-side override that is part of the canonical baseline config stays identical on both charts (DJ30: day soft-stop **−1.15%** TV override).
- [ ] Strategy Properties identical: initial capital **200,000 USD**, commission **0**, slippage **0** (swap/fee-unaware baseline convention).
- [ ] Chart timeframe **15m** on both.
- [ ] Chart timezone = **New York** on BOTH charts (chart settings → timezone). Do **not** use "Exchange" — CME symbols default to Chicago and would shift the grid 1h; the harness pairs by ET timestamp.
- [ ] Bar Magnifier **OFF** on both (BT-OFF canonical doctrine, 2026-05-17).
- [ ] If Deep Backtesting is used, use it on BOTH exports of the leg with the identical range.

## CME continuous-contract adjustment mode (§0.5-c — record, don't decide)

On each CME chart (`MYM1!`, `MNQ1!`): chart settings → Symbol → note the **"Adjust for contract changes"** (back-adjustment) state. TV's default continuous is fine — just **screenshot the setting** per CME chart and note it with the delivery. Divergences near roll dates get their own ROLL-SEAM bucket; the harness reports divergence **both with and without** that bucket, and the carve-out decision is yours at scoring time.

## Export steps (per chart)

1. Open the symbol, 15m, New York TZ; apply/verify the locked strategy per the checklist.
2. Strategy Tester → **List of Trades** → export data (CSV). Current or legacy TV export schema both parse — export whatever TV produces; do not hand-edit columns.
3. Name the file per the table above.

## Screenshots to attach (3–4 total)

1. Chart timezone setting (one representative chart).
2. "Adjust for contract changes" setting — one per CME chart (MYM1!, MNQ1!).
3. Strategy inputs panel — one per leg (proves both exports of the leg share it).

## Delivery

Drop the 4 CSVs + screenshots in `Downloads` (or any local path) and give the paths in the go-message together with: (a) the **window pin** above, and (b) **ratification** of the K2/E1 gate values (10% / 0.8× / 0.7× are `[RATIFY]`-pending in the parent ADR). Do **not** commit the CSVs — vendor exports are gitignored by standing policy.
