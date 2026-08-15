---
name: databento-data
description: >-
  Cost-gated access to Databento GLBX.MDP3 CME market data (index, gold, and FX
  futures) for the First Passage / CONSTELLATION research stack. Use whenever
  pulling, estimating, or caching historical or live CME futures data via the
  databento Python client — MBO/L3 full order book, MBP-10 depth, TBBO, trades,
  or OHLCV bars — for ES/NQ/YM/GC parents, MES/MNQ/MYM/MGC micros, or the JPY
  leg. Triggers: "pull tick history", "order-book history", "databento",
  "GLBX.MDP3", "estimate data cost", "get_range", "parent vs continuous
  contract", "micro futures data", building a discovery dataset, or wiring a
  Nautilus/vectorbt data feed. Enforces the mandatory cost dry-run before every
  pull and the parent->micro proxy discipline (re-scale tick value/margin,
  reserve the 2019+ micro era as an out-of-sample gate).
---

# Databento GLBX.MDP3 data access

Single venue: **GLBX.MDP3** (CME Globex — CME/CBOT/NYMEX/COMEX). History back to
**2010-06-06**. The live and historical APIs share identical interfaces and data
structures, so the same pull code serves backtest and live.

Run everything in the **research venv** (where `databento` is installed), isolated
from the execution rail (NT8/Rithmic). The API key lives in the
`DATABENTO_API_KEY` env var — **never inline, never in a committed file.**

## Rule 1 — estimate before every pull (the money guard)

A single `timeseries.get_range` over MBO can be a real billing event. **Never call
a pull without a cost estimate first.** Use the bundled script, which makes the
estimate mandatory and refuses to pull above a ceiling:

```
# Preferred (canonical lab module; research venv):
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate \
    --symbols ES.FUT --stype parent --schema trades \
    --start 2024-02-12 --end 2024-02-17

PYTHONPATH=lab python -m databento_fetch.db_fetch pull \
    --symbols ES.c.0 --stype continuous --schema ohlcv-1m \
    --start 2010-06-06 --end 2026-01-01 --max-cost 5.00

# Skill wrapper (same args; forwards to the lab module):
python scripts/db_fetch.py estimate \
    --symbols ES.FUT --stype parent --schema trades \
    --start 2024-02-12 --end 2024-02-17

python scripts/db_fetch.py pull \
    --symbols ES.c.0 --stype continuous --schema ohlcv-1m \
    --start 2010-06-06 --end 2026-01-01 --max-cost 5.00
```

`estimate` uses metadata endpoints (`get_cost`, `get_billable_size`,
`get_record_count`, `get_dataset_range`) that do **not** bill for the underlying
data — so a dry-run is always free. `pull` re-runs the estimate, enforces the
`--max-cost` ceiling, then streams to a local DBN cache keyed by request params
(re-pulls hit cache, no re-billing). Each team gets **$125 in free historical
credits** — validate the workflow inside that before any large pull.

Never hand-write a bare `client.timeseries.get_range(...)` in analysis code when
this script exists. If a pull genuinely needs to bypass the script, state the
estimated cost first and get explicit sign-off.

## Rule 2 — coarsest schema that answers the question

Cost rises steeply with granularity. Start coarse; escalate only after a
candidate survives. Ladder (cheap → expensive): `ohlcv-1d` / `ohlcv-1h` /
`ohlcv-1m` → `tbbo` → `mbp-1` → `mbp-10` → `mbo`. Plus `definition` (cheap;
instrument specs, tick size, roll). **Do not pull `mbp-10` or `mbo` until a
candidate has survived on bars** — order-flow microstructure is a hypothesis, not
a default. Full schema selection + when-to-use: `reference/schemas-and-symbology.md`.

## Rule 3 — pick symbology deliberately, never mix silently

`parent` (`ES.FUT` → all ES expiries) for pulling a whole family; `continuous`
(`ES.c.0`, ranked front month, rolls automatically) for a single rolling series;
`raw_symbol` (`ESH4`) for a specific contract. Choosing wrong silently changes the
series. The continuous **roll-rule letter and whether it price-adjusts must be
confirmed against the symbology docs before a deep pull** — do not assume.
Details + roots for this operation: `reference/schemas-and-symbology.md`.

## Rule 4 — parent history is valid for discovery, NOT for P&L (proxy discipline)

The micros postdate most useful history (index micros launched 2019-05-06, MGC
2010), so deep-history discovery runs on parents (ES/NQ/YM/GC), which share the
same order book and arbitraged price. That is valid for **structural discovery
only**. Before any parent-derived candidate is trusted: (1) re-scale economics to
micro specs — tick value, multiplier, margin; (2) re-parameterize slippage/fills
on native micro-era data; (3) reserve **2019→present native-micro data as an
out-of-sample / regime-consistency gate**. Spec table + the FX/JPY reconciliation
(unresolved — resolve before building): `reference/proxy-discipline.md`.

## Licensing (confirm, don't assume)

CME data via Databento is licensed through the vendor at Non-Professional
Subscriber rates; internal research-and-trade-your-own-book use is non-display
research/analysis and does **not** need a DDLA to research and trade your own
account. But CME's 2025 non-display/EOD licensing changes put fee structures in
flux — **budget for pass-through non-display/research fees and confirm the exact
non-display category with Databento before scaling pulls.** "Historical = free" is
not a safe assumption.

## Red flags — STOP

- About to `pull` without an `estimate` → estimate first.
- Pulling `mbo`/`mbp-10` before any candidate survived on bars → justify or drop back to bars.
- `parent` / `continuous` / `raw_symbol` mixed in one analysis without noting which → resolve.
- Building the JPY/FX pipeline while the micro code (M6J vs MJY) and quote convention are unresolved → resolve first (`reference/proxy-discipline.md`).
- Using parent tick value / P&L as if it were the micro → re-scale.
- Treating a parent-era backtest as validated without the 2019→present micro OOS gate → hand to `strategy-validation`.
- Era-mix is now a **hard abort**: a `db_fetch.py --phase discovery` pull whose `--end` reads past the ratified IS boundary (2018-12-31, `--end` exclusive) aborts before any API call. Pass `--phase oos` for the hold-out; the cache is era-tagged by `--campaign-id`/`--phase` so a discovery read and an oos read never share a cache file. Omitting the flags is byte-identical legacy behavior.

## Hand-offs

- **Micro-era OOS gate + universe-level correction** live in `strategy-validation`.
- **Any candidate mined off this data carries a trial count K** — log it in `futures-anomaly-discovery`, not here.
- Deep-history multi-GB MBO pulls: prefer batch (`client.batch.submit_job` →
  `list_jobs` → `download`) over streaming. Do this interactively (job polling),
  not via the unattended script.
