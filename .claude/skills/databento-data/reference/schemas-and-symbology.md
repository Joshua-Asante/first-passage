# Schemas and symbology — GLBX.MDP3

## Schema selection ladder

Cost and data volume rise steeply down this list. **Start at the coarsest schema
that can express the hypothesis; escalate only after a candidate survives.**

| Schema | Level | What it is | Use for |
|---|---|---|---|
| `ohlcv-1d` / `-1h` / `-1m` / `-1s` | agg | Bar aggregates | Long-horizon structural discovery, regime work, most signal triage |
| `tbbo` | L1+trade | Each trade + the BBO in force at trade time | Trade prints with prevailing quote; execution-price studies |
| `mbp-1` | L1 | Top of book, every update | Spread / quote dynamics at top of book |
| `mbp-10` | L2 | 10 levels of depth, every update | Depth / imbalance features — **only post-candidate** |
| `mbo` | L3 | Full order book, every order event | Order-flow microstructure — highest cost, **only when that IS the hypothesis** |
| `definition` | — | Instrument definitions (specs, tick size, expiry) | Resolving contract specs, roll, tick value. Cheap — pull freely |

Rule of thumb: do the discovery on bars, confirm the mechanism on depth. Pulling
`mbo`/`mbp-10` as a first move is the classic way to burn credits on a hypothesis
that bars would have killed for free.

## Symbology (the `--stype` flag)

Choosing the wrong type silently changes the series you analyze. Pick deliberately;
never mix types inside one analysis without labeling which is which.

- **`parent`** — one symbol resolves to a whole product family.
  `ES.FUT` → all ES expiries; `ES.OPT` → ES options. Use when pulling the full
  family or building your own continuous series from raw expiries.
- **`continuous`** — a smart symbol that tracks contracts across rolls.
  Format `{ROOT}.{roll}.{rank}` (e.g. `ES.c.0`), where `rank` 0 = front month and
  the roll rule ranks by expiration / volume / open interest. Use for a single
  rolling series without hand-rolling.
  ⚠️ **Confirm the exact roll-rule letter AND whether the series is price-adjusted
  against the Databento symbology docs before a deep pull.** The wrong roll rule,
  or an unexpected (non-)adjustment, silently produces a different price series and
  will quietly poison a backtest. Do not assume the letter.
  📌 **Earned pin (Q-TVCOV-1, 2026-07-13): the roll rule changes which bars EXIST,
  not just prices — "counts only, so roll is moot" is a trap.** `.c.0`
  (calendar-rank-0) maps CME currency futures to the near-dead front *monthly
  serial* after each quarterly expiry (6J.c.0 2021-09: 335 covered NY-session 15m
  slots vs 734 actual), and parks equity-index micros on the dying contract for
  quarterly-roll Fridays. **For any TV-`1!` comparison or liquidity/coverage
  measurement, use `.v.0` (volume-rolled)** — verified to match TV bar-for-bar
  (`lab/analysis/c1/tvcov_2026-07/RESULTS.md` §Roll-rule attribution).
- **`raw_symbol`** — the exact CME symbol for one contract, e.g. `ESH4` (Mar 2024
  ES). Use for a specific expiry.
- **`instrument_id`** — Databento's numeric id, from a `definition` pull or
  `symbology.resolve`. Use when you already hold resolved ids.

Limits: up to **2,000 symbols per request**; `'ALL_SYMBOLS'` pulls the whole venue
(expensive — always cost-gate it). Use `client.symbology.resolve(...)` to map
between symbology systems, and the `definition` schema for point-in-time specs
(free of look-ahead / retroactive adjustment).

## Roots for this operation

- **Index parents:** `ES` (S&P 500), `NQ` (Nasdaq-100), `YM` (Dow). Add `RTY`
  (Russell 2000) only if a Russell leg is in scope.
- **Gold parent:** `GC`.
- **JPY:** `6J` is the full-size CME Japanese Yen future, **quoted JPY/USD —
  inverted from USDJPY.** Aegis is specified in USDJPY terms, so the inversion is
  load-bearing. ⚠️ The micro instrument (M6J vs MJY) and its quote convention are
  **unresolved** — see `proxy-discipline.md` and resolve before building the FX
  pipeline.

Micro roots (native-era data, for the OOS gate): `MES`, `MNQ`, `MYM`, `M2K`,
`MGC`, and the resolved JPY micro. Specs in `proxy-discipline.md`.

## Data hygiene (bytes → a valid series)

Three provenance facts that silently poison a backtest if unhandled. They precede any
statistic; the mining-side hygiene that builds on them (vol-U-shape normalization,
which schema's prices to use) lives in `futures-anomaly-discovery`
`reference/tool-discipline.md` §Pre-mining data hygiene.

### Continuous-contract back-adjustment

`continuous` symbols are stitched across rolls, and *how* they stitch changes what is
true of the series:

- **Difference-adjustment** preserves point moves but distorts price *levels* (they can
  even go negative on deep history). **Percentage returns on a difference-adjusted
  series are wrong**, and any *level*-based signal (round numbers, prior highs/lows, a
  fixed price band) is testing phantom levels.
- **Ratio-adjustment** preserves returns but distorts point values (so $-P&L per point
  is off).
- **Roll-date convention** injects a jump whose timing is your choice, not the market's.
- **Discipline:** an indicator may run on an adjusted series for continuity, but
  **entries, exits, and P&L must be evaluated on the actual tradeable contract's
  prices**, and any calendar-adjacent anomaly must be checked against the roll schedule
  so you haven't discovered your own back-adjustment. Pull `definition` for
  point-in-time specs (free of retroactive adjustment); confirm the roll letter +
  whether it price-adjusts before a deep pull (the ⚠️ under `continuous` above).

### Session & clock hygiene (CME Globex)

The leading generators of fake time-of-day anomalies:

- **RTH vs ETH.** GLBX.MDP3 is near-24h Globex (ETH); an RTH-only hypothesis (e.g. the
  equity-index cash session) must be sliced to RTH explicitly — ETH bars are a
  different population.
- **The Globex session boundary is 17:00 America/Chicago** (a new trading *date* opens
  at 17:00 CT the prior calendar day), with a daily maintenance break. A "daily" bar is
  a Globex trade-date, not a midnight-UTC day — do not assume.
- **DST.** A fixed UTC-hour filter silently shifts an exchange-local "open" by an hour
  twice a year; map to exchange-local time (America/Chicago) with a DST-aware
  conversion and spot-check the boundary weeks.
- **Holiday half-sessions** (early closes) truncate the session — exclude or flag them,
  or a session-return statistic mixes full and half days.

### Bid-ask bounce (trade prices vs midpoint)

At `mbo` / `tbbo` / trade granularity, consecutive trade prices bounce between bid and
ask, inducing **spurious negative autocorrelation** in a trade-price return series — the
spread, not mean reversion. For any short-horizon MR / reversal work use the **midpoint**
(`mbp-1` or the `tbbo` quote), not the trade print.
