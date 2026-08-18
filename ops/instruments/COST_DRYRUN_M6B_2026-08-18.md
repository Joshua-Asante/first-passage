<!-- no-profile: cost dry-run companion to M6B.md; not an instrument ledger -->

# Cost dry-run — M6B initial census (estimate only)

**Date:** 2026-08-18
**Owner ledger:** [`M6B.md`](M6B.md)
**Disposition:** estimate only. No `pull`. No `--force`. Does not admit a candidate.

**Commands run:** `PYTHONPATH=lab python3 -m databento_fetch.db_fetch estimate` only. Metadata endpoints (`get_cost` / `get_billable_size` / `get_record_count`) — the estimate itself does not bill for the underlying data (databento-data skill Rule 1).

## Framing

M6B had no ledger and no prior census in this repo (dedup: only `core/firm_rules.py` L58). Sibling M6E was Stage-1 `E-COST`; that kill does not transfer. This dry-run prices the coarsest volume-rolled continuous panel that opens a native-micro geometry surface for a future operator GO — same micro-era confirm window used for sibling FX/metal micros in the deep-lane charter addendum (`2019-05-06` → present).

## Primary request (initial census)

```
PYTHONPATH=lab python3 -m databento_fetch.db_fetch estimate \
  --symbols M6B.v.0 --stype continuous --schema ohlcv-1d \
  --start 2019-05-06 --end 2026-08-18
```

| Field | Value |
|---|---|
| **Streaming estimate** | **`$0.0000` USD** |
| Billable size | 126,672 bytes (~0.0001 GB) |
| Records | 2,262 |
| Schema available end | `ohlcv-1d` through 2026-08-18T00:00Z (request `--end` exclusive, inside range) |

`.v.0` = volume-rolled continuous (Q-TVCOV-1 pin). `$0.0000` streaming is the vendor metadata figure — not a license opinion.

## Ladder / contrast (priced, not chosen)

| Request | Why priced | Streaming estimate | Size / records |
|---|---|---|---|
| `M6B.v.0` `ohlcv-1m` same window | Next rung if daily census survives and intraday work is elected | `$0.0000` | 65,038,848 B / 1,161,408 |
| `6B.v.0` `ohlcv-1d` same window | Parent contrast only — parent is un-ledgered; not the micro census | `$0.0000` | 127,120 B / 2,270 |

## Operator decision (not taken here)

Spend $0 streaming + ~0.0001 GB local cache on a first M6B daily panel, or leave the instrument ledger geometry-only until a mechanism touch needs bars. No pull from this session.
