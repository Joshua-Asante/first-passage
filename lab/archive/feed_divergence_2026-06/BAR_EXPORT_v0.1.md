# BAR EXPORT v0.1 — comment-encoded OHLCV via TV List-of-Trades

**Status:** frozen for Q-FEED-1 Phase 1
**Parent:** `docs/ltm/briefs/Q-FEED-1-dukascopy-tv-feed-divergence.md`

## Purpose

Extract M15 OHLCV bars from the Pepperstone/TV deployment feed without relying on
strategy-tester fill mechanics. One reversal order per confirmed bar encodes the
bar's OHLCV in the order **comment** field; the List-of-Trades CSV is the transport.

## Pine exporter

Script: `lab/archive/feed_divergence_2026-06/bar_export_v01.pine` (local-only;
`**/*.pine` is gitignored — copy into TradingView manually).

Behavior:
- `strategy()` on M15, `calc_on_every_tick=false`, `process_orders_on_close=true`
- On `barstate.isconfirmed`, place one `strategy.order` reversal
- **Signal** field format (deployed on TV, 2026-06-12):

  ```
  {epoch_ms}|{open}|{high}|{low}|{close}|{volume}
  ```

  Example: `1772409600000|156.64|156.806|156.572|156.574|3915`

- `epoch_ms` = bar-open UTC (milliseconds); parser prefers this over Date and time
- Fill cross-check: Entry `Price` == encoded `close` (`process_orders_on_close`)
- Final backtest row may show `Close position order` on Exit — parser uses Entry rows only

## Manual export procedure

1. Open Pepperstone chart for the symbol (`USDJPY`, `GBPUSD`, `US30`), M15.
2. **Record chart timezone** (Chart settings → Symbol → Timezone). Write it in
   `lab/archive/feed_divergence_2026-06/tv_chart_tz.txt` before exporting.
3. Attach `bar_export_v01.pine` as a strategy.
4. Set backtest window: **2026-03-01 → 2026-06-01** (one pass; ~6,300 M15 bars).
5. Strategy Tester → List of Trades → Export CSV.
6. Save as:
   - `core/data/tv_exports/pepperstone/bar_export/USDJPY_M15_pep.csv`
   - `core/data/tv_exports/pepperstone/bar_export/GBPUSD_M15_pep.csv`
   - `core/data/tv_exports/pepperstone/bar_export/US30_M15_pep.csv`
7. Regenerate manifests after landing vendor bytes:
   `python scripts/check_data_manifests.py --regenerate`

## Parser cross-check (format drift detector)

`parse_tv_export.py` decodes the comment field **and** cross-checks each row's
`Date and time` + `Price` column against the encoded OHLCV:

- Entry row `Price` must equal encoded `open` within symbol tolerance
- Exit row `Price` must equal encoded `close` within tolerance
- Mismatch → hard fail (TV export format drift)

## Limits

- ≤9,000 bars per export pass (TV trade-list cap). The frozen Q-FEED-1 window fits
  in one pass per symbol.
- Long-only reversal semantics: each bar produces Entry long + Exit long pair.
