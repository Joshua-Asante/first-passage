# Q-TXG-1 — ATR / instrument inputs extension

**Scope:** inputs only (atr_map surface + this note). No cell scoring, no election,
no H_A prose. Coordination: campaign PROSE owned elsewhere; this footprint is
`atr_map.py` + this note. M6J envelope row **not** added — venue check closed it.

**Derivation convention (MYM/MNQ known-answer):**
`f2_floors.json` `recent_90d.atr_median_pts` ÷ `INSTRUMENT_SPECS[sym].tick_size`
(ATR period **11**, roll-seam-masked RMA on M15 bars when producing a *new*
median — see `lab/analysis/c1/q_rail_1_2026-07/f2_floors.py`). Committed MYM/MNQ
values are the map authority; live recompute on current `bar_data` panels is
**not** the known-answer path (panel hashes drifted after F2).

**Checkout probe (this land):** `core/data/bar_data/SHA256SUMS` pins
`6J` / `MGC` / `MNQ` / `MYM`. CSV bytes gitignored — presence is per-checkout.

| Instrument | Data source @ pin | ATR(11) ticks / status | Grid cells that flip screenable (stop-map) |
|---|---|---|---|
| MYM | `f2_floors.json` recent_90d `50.6834` pts; bar pin `24e16952…` (bytes present here) | **50.6834** ticks (`ATR_TICKS_MYM_ATR11`) — COMMITTED | already screenable: striker×MYM (WITHDRAWN), striker_nas100×MYM |
| MNQ | `f2_floors.json` recent_90d `45.5095` pts; bar pin `6c86f41a…` (bytes present here) | **182.038** ticks (`ATR_TICKS_MNQ_ATR11`) — COMMITTED | already screenable: striker×MNQ, striker_nas100×MNQ (WITHDRAWN) |
| MES | no `MES_M15.csv` in SHA256SUMS | UNSCREENABLE-INPUT(atr): no bar_data pin | none |
| MGC | SHA256SUMS pin `88da9f15…` @ `ecfdf59`; **bytes ABSENT this checkout** | PENDING: `MGC_M15.csv` absent (pin named) | **none yet** — would unlock ATR(11) stop-map for striker×MGC + striker_nas100×MGC once median transcribed; guardian×MGC stays ATR(14)-UNSCREENABLE + PARKED(b8) |
| M2K | no `M2K_M15.csv` in SHA256SUMS | UNSCREENABLE-INPUT(atr): no bar_data pin | none |
| MCL | no `MCL_M15.csv` in SHA256SUMS | UNSCREENABLE-INPUT(atr): no bar_data pin | none |
| M6A | no `M6A_M15.csv` in SHA256SUMS | UNSCREENABLE-INPUT(atr): no bar_data pin | none |
| M6J | **not venue-legal** — see below | UNSCREENABLE-INPUT(venue) — **closed; no ATR / no envelope row** | none (never enters ENV-1 pool) |

**Cells flipped screenable by this extension:** **0** (no new committed ATR(11) median; MGC PENDING; M6J venue-closed).

## M6J venue-legality (closes the question)

`M6J_VENUE_LEGAL = False` in `atr_map.py`.

| Firm class | Product-set fact | Owner |
|---|---|---|
| Tradeify | micro FX = M6A + M6E only; **NO M6J**; full 6J $3.10/side | `core/firm_rules.py` Tradeify cost block · article 10468222 |
| Bulenox | Rates.pdf has full 6J; **NO M6J row** | `core/firm_rules.py` Bulenox comments |
| MyFundedFutures | **NO M6J** on instrument list | `core/firm_rules.py` MFFU comments |
| Ledger corroboration | "no FRIENDLY firm offers M6J" | `ops/instruments/6J.md` ACTIVE/OPEN |

Symbology (not a venue grant): `.claude/skills/databento-data/reference/proxy-discipline.md` — `M6J.FUT` does not resolve on GLBX.MDP3; live micro code is **MJY**. Irrelevant once product-set fails.

**Stop:** no envelope-constants row, no ATR derivation, no pool membership change for M6J.

## Known-answer check (MYM/MNQ)

Before any new instrument ATR row may be appended to `_ATR_PTS_RECENT90_ATR11`:

```
ATR_TICKS_MYM_ATR11 == 50.6834 / 1.0
ATR_TICKS_MNQ_ATR11 == 45.5095 / 0.25
```

Campaign tests assert these byte-identically via the existing `test_atr_ticks_*` /
`test_stop_ticks_*` suite.
