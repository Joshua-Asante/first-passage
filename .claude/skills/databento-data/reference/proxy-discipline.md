# Parent → micro proxy discipline

## Why parents at all

The micros postdate most useful history — index micros (MES/MNQ/MYM/M2K) launched
**2019-05-06**, Micro Gold (MGC) in **2010**. Deep-history discovery therefore runs
on the parents (`ES/NQ/YM/GC`), which share the same order book and are arbitraged
tightly to the micros — effectively the same underlying price series.

This makes parent history valid for **structural discovery only**. It is **not**
valid as-is for P&L, position sizing, or fill modeling. A candidate discovered on
parent history is a hypothesis about structure, not a validated micro strategy.

## The three mandatory adjustments

Before any parent-derived candidate is trusted:

1. **Re-scale economics to the micro spec** — multiplier, tick, tick value, and
   margin. Micro : parent = **1:10** for every root in the table below. Every P&L,
   drawdown, and Monte-Carlo bust-probability input must be recomputed on micro
   tick value, not the parent's.
2. **Re-parameterize slippage / fills on native micro-era data** — micro liquidity,
   spread, and queue behavior differ from the parent. Do **not** inherit the
   parent's fill model. Pull native micro data (`MES`, `MNQ`, … from 2019+; `MGC`
   from 2010) and fit the slippage model there.
3. **Reserve 2019→present native-micro data as an out-of-sample / regime-consistency
   gate.** A parent-discovered anomaly must survive on native micro data before
   deployment. This is a genuine OOS hold-out, not a second in-sample fit. Hand the
   gate to `strategy-validation`.

## Contract specs (micro vs parent)

All 1:10. Confirm live values with a `definition`-schema pull before sizing —
CME can revise specs.

| Micro | Micro multiplier | Micro tick | Micro tick $ | Parent | Parent tick $ |
|---|---|---|---|---|---|
| **MES** | $5 × index | 0.25 | $1.25 | ES | $12.50 |
| **MNQ** | $2 × index | 0.25 | $0.50 | NQ | $5.00 |
| **MYM** | $0.50 × index | 1.0 | $0.50 | YM | $5.00 |
| **M2K** | $5 × index | 0.10 | $0.50 | RTY | $5.00 |
| **MGC** | 10 troy oz | 0.10 $/oz | $1.00 | GC | $10.00 |

## FX / JPY — RESOLVED 2026-07-20 (Q-BOOKFIT-1 Phase 1b)

Resolved with live GLBX.MDP3 data (symbology.resolve + cost-gated ohlcv-1d
verification pull, estimated then billed $0.00; record:
`docs/briefs/closures/Q-BOOKFIT-1-closure-resolved.md`):

1. **Instrument code: `MJY` (Micro JPY/USD).** `M6J.FUT` does **not** resolve on
   GLBX.MDP3 (422 symbology_invalid_request) — the reported "Micro USD/JPY M6J"
   does not exist on this dataset. `MJY.FUT` resolves live (outrights MJYU6 /
   MJYZ6 + calendar spread, 2026-07-13). Listing is thin (2 outrights) — check
   liquidity fresh before any campaign sizing.
2. **Quote convention: identical to `6J` (JPY/USD).** MJYU6 closes 0.006188 /
   0.006194 vs 6JU6 0.006188 / 0.006195 on 2026-07-13/14 — the micro is a 1/10
   `6J` clone, no micro-specific inversion exists. The **Aegis mapping rule
   therefore stands as a fixed requirement, not an ambiguity**: Aegis is
   specified in USDJPY terms, so any pipeline mapping it onto `6J`/`MJY` must
   handle "long USDJPY" ≈ "short 6J/MJY", with USD tick value off the JPY/USD
   price. Get the sign right before a single backtest row is generated.

Also: pull the micro's margin/liquidity fresh (the Bulenox margin row is an
operator-owed task). Record the resolved instrument, tick value, and quote
convention in the repo so this reconciliation happens once, not every session.

## Hand-offs

- OOS gate mechanics + universe-level multiple-testing correction: `strategy-validation`.
- Trial-count (K) accounting for anything mined off parent data: `futures-anomaly-discovery`.
