# SPEC: ECON EXPORT v0.1 — `request.economic()` calendar-provenance cross-check

Status: TOOL · 2026-08-18 · authorizes nothing ($0 · K=0) · depends: —

Objective: Export TradingView `request.economic()` series-update dates as a List-of-Trades CSV and diff them against the hand-pinned calendars already used by closed campaigns.

Gate: parser + diff tests pass on synthetic fixtures; first-run without a TV CSV reports `AWAIT_TV_EXPORT` / `NO_TV_FIELD` / `UNRECOVERABLE_PIN` rather than inventing dates.

Boundary: provenance/hygiene only. Do not re-test or reopen RATES-EV-ZF-1 or NG-EIA-1 ([`docs/rejected_candidates.md`](../rejected_candidates.md), both FALSIFIED 2026-07-21 on cost/power). Do not build an Aegis BOJ/FOMC pause gate ([`aegis_CHANGELOG.md`](../../core/strategies/_archive/aegis/aegis_CHANGELOG.md)). Do not treat `INTR` as FOMC. Do not invent first-Friday / mid-month / always-Thursday dates.

Reads: TV Help Center field list (2026-08-18) · [`BAR_EXPORT_v0.1.md`](../../lab/archive/feed_divergence_2026-06/BAR_EXPORT_v0.1.md) · [`lab/archive/rates_ev_zf_recon_2026-07/build_calendar.py`](../../lab/archive/rates_ev_zf_recon_2026-07/build_calendar.py) · [`lab/archive/ng_eia_recon_2026-07/build_calendar.py`](../../lab/archive/ng_eia_recon_2026-07/build_calendar.py) · [`lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_eventday_2026-08-10_LOG.md`](../../lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_eventday_2026-08-10_LOG.md)

Owner: this spec + [`lab/tools/econ_export/`](../../lab/tools/econ_export/)

---

## Constraint

`request.economic(country_code, field)` returns a **macro time series**, not TradingView’s economic-calendar UI. A “release date” here is the daily bar on which the series **prints or changes**.

| Wanted event | TV field | Limb |
|---|---|---|
| CPI release | `CPI` | exportable |
| NFP release | `NFP` | exportable |
| FOMC decision day | **none** | always `NO_TV_FIELD` — do not use `INTR` |
| EIA NG storage calendar | **none** | closest series `NGSC` (stocks-change updates), never a Thursday heuristic |

## Transport (BAR_EXPORT discipline, not OHLCV)

Reuse List-of-Trades + `comment`/`Signal` pipe + `epoch_ms` authority. Do **not** reuse [`core/bar_export_loader.py`](../../core/bar_export_loader.py) `SIGNAL_PIPE_V2_RE` (OHLCV).

```
{epoch_ms}|{country}|{field}|{value}|{tz}|{tf}
```

Example: `1704931200000|US|CPI|308.5|America/New_York|D`

Filename: `ECON_EXPORT_v0.1_TV_{COUNTRY}{FIELD}_{YYYY-MM-DD}_{5hex}.csv`

Parser: [`scripts/parse_econ_export.py`](../../scripts/parse_econ_export.py) — Entry rows only; `epoch_ms` wins over `Date and time`.

Diff: [`scripts/diff_econ_calendar.py`](../../scripts/diff_econ_calendar.py)

Statuses: `MATCH` · `MISSING_TV` · `EXTRA_TV` · `TZ_SHIFT` (±1 calendar day) · `NO_TV_FIELD` · `AWAIT_TV_EXPORT` · `UNRECOVERABLE_PIN` (EVT-1 FOMC 2019–2021; `stage2_run.py` absent on this public clone).

Windows: RATES / NG `2019-01-01`–`2026-07-15`; EVT-1 CPI/NFP `≤2025-08-31`. Hand-pinned lists are **imported**, not copied.

## Pine (durable listing)

Working copy (gitignored): `lab/tools/econ_export/econ_export_v01.pine`. Pin: [`lab/tools/econ_export/PINE_MANIFEST.sha256`](../../lab/tools/econ_export/PINE_MANIFEST.sha256). Not a `core/strategies/MANIFEST.sha256` entry.

```pine
//@version=6
strategy("ECON EXPORT v0.1", shorttitle="ECON_EXP", overlay=false,
     calc_on_every_tick=false, process_orders_on_close=true, pyramiding=3)

// Provenance-only exporter. request.economic() is a macro SERIES, not a calendar.
// A confirmed bar is an event iff the series prints or changes. No INTR-as-FOMC.
// No first-Friday / Thursday heuristic. Copy into TradingView; **/*.pine is gitignored.

country = input.string("US", "Country code", group="Series")
exportCpi = input.bool(true, "Export CPI", group="Series")
exportNfp = input.bool(true, "Export NFP", group="Series")
exportNgsc = input.bool(true, "Export NGSC (stocks-change proxy, not EIA calendar)", group="Series")

cpi = request.economic(country, "CPI")
nfp = request.economic(country, "NFP")
ngsc = request.economic(country, "NGSC", ignore_invalid_symbol=true)

cpiEvent = exportCpi and not na(cpi) and (na(cpi[1]) or cpi != cpi[1])
nfpEvent = exportNfp and not na(nfp) and (na(nfp[1]) or nfp != nfp[1])
ngscEvent = exportNgsc and not na(ngsc) and (na(ngsc[1]) or ngsc != ngsc[1])

encode(field, val) =>
    str.format("{0}|{1}|{2}|{3}|{4}|{5}",
         str.tostring(time), country, field, str.tostring(val),
         syminfo.timezone, timeframe.period)

if barstate.isconfirmed
    if cpiEvent
        strategy.entry("CPI", strategy.long, qty=1, comment=encode("CPI", cpi))
        strategy.close("CPI")
    if nfpEvent
        strategy.entry("NFP", strategy.long, qty=1, comment=encode("NFP", nfp))
        strategy.close("NFP")
    if ngscEvent
        strategy.entry("NGSC", strategy.long, qty=1, comment=encode("NGSC", ngsc))
        strategy.close("NGSC")
```

## Operator export

1. Daily chart, max history (`ECONOMIC:USCPI` or any liquid daily). Record chart timezone.
2. Paste the listing above into the Pine editor; add as a strategy.
3. Strategy Tester → List of Trades → Export CSV.
4. Save as `lab/tools/econ_export/exports/ECON_EXPORT_v0.1_TV_USCPI_<YYYY-MM-DD>_<5hex>.csv` (and/or USNFP / USNGSC). One mixed-field file is also valid.
5. Diff (default reports `AWAIT_TV_EXPORT` when no CSV is present):

```bash
python scripts/diff_econ_calendar.py
python scripts/diff_econ_calendar.py --in lab/tools/econ_export/exports/*.csv
python scripts/diff_econ_calendar.py --require-tv-export --in path.csv
```

## Limits

- TV List-of-Trades cap (~9,000 rows). Daily CPI+NFP+NGSC over 2019–2026 is well under it.
- `NGSC` may be unavailable for `US`; then the export has zero NGSC rows → `NO_TV_FIELD`.
- This Cloud / public clone cannot run TradingView. First-run without CSVs is the intended finding until an operator lands an export.
