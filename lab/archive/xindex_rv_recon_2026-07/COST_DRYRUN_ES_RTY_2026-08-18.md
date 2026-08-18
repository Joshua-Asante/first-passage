# Cost dry-run — ES + RTY addback (estimate only)

**Date:** 2026-08-18
**Owner:** [`RESULTS.md`](RESULTS.md) · closure row in [`docs/rejected_candidates.md`](../../../docs/rejected_candidates.md) (cross-index relative-volume ranking)
**Disposition of the candidate:** unchanged — **FALSIFIED / DROP (lean)**. This file prices the closure's own `addback_condition`. It does not reopen the thread, does not pull, and does not score a bar.

**Commands run:** `PYTHONPATH=lab python3 -m databento_fetch.db_fetch estimate` only. No `pull`. No `--force`. Metadata endpoints only (`get_cost` / `get_billable_size` / `get_record_count`) — the estimate itself does not bill for the underlying data (databento-data skill Rule 1).

## Framing (operator)

The 2026-07-21 pre-screen already killed the core mechanism on real cached intraday data (MNQ vs MYM only): RV-rank selection *diluted* edge relative to always-trading-MNQ, Class line `edge-failure (the selection dilutes rather than concentrates edge) + data/universe-constraint (secondary)`. The missing ES+RTY pull is the closure's own DEFER-procurement trigger with a **poor prior** — same venue-wall class as the closed BTC-trend pattern (index aggregation compresses the idiosyncratic dispersion that makes cross-sectional selection work). Adding ES alone is inadmissible. This dry-run only prices the cheapest schema that could *test* whether small-cap (RTY) idiosyncrasy rescues dispersion **and** the failed (B) limb (higher-RV → better ORB edge). That is a low-expectancy falsifier, not an unexplored lead.

## Primary request (matches the addback)

Opening-30m RV + first-break ORB cannot be reconstructed from daily bars, so the coarsest schema that can discharge the addback is **`ohlcv-1m`**. Volume-rolled continuous (`.v.0`) per the Q-TVCOV-1 pin — front-month RV ranking, not `parent` all-expiries. Window matches the pre-screen (`2020-07` → `2026-07`; `--end` exclusive).

```
PYTHONPATH=lab python3 -m databento_fetch.db_fetch estimate \
  --symbols ES.v.0,RTY.v.0 --stype continuous --schema ohlcv-1m \
  --start 2020-07-01 --end 2026-08-01
```

| Field | Value |
|---|---|
| **Streaming estimate** | **`$0.0000` USD** |
| Billable size | 237,197,744 bytes (~0.2372 GB) |
| Records | 4,235,674 |
| Dataset range (schema `ohlcv-1m`) | 2010-06-06 → 2026-08-18 (request inside) |

`$0.0000` streaming is the vendor metadata figure for this window/schema. It is not a license opinion — the skill still requires confirming non-display/research category before *scaling* pulls. This request is one scoped pair, not a scale-up.

## Ladder / alt (priced, not chosen)

| Request | Why priced | Streaming estimate | Size / records |
|---|---|---|---|
| `ES.v.0,RTY.v.0` `ohlcv-1d` same window | Rule 2 coarsest-first; **cannot** rebuild opening-30m RV or ORB — would be an RV-window re-tune the closure forbids | `$0.0000` | 212,240 B / 3,790 |
| `ES.v.0,M2K.v.0` `ohlcv-1m` same window | User-allowed RTY-or-M2K-micro alt; mixed parent+micro volume is a worse RV apples-to-apples than ES+RTY parents | `$0.0000` | 236,902,960 B / 4,230,410 |

## Operator decision (not taken here)

Spend $0 streaming + ~0.24 GB local cache on a poor-prior falsifier that can only *fail to rescue* a mechanism already dominated on the 2-index universe — or leave the addback un-discharged. No pull from this session.
