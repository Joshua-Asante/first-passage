# Global Market Map registry

[registry.json](registry.json) is the authoritative, public metadata registry for the
configured TradingView dashboard. Audit: 2026-10-10/11, markets closed. The watchlist
contains 19 available symbols and one retained unavailable concept. Feed status was
inspected in the signed-in account; moving ticks and actual delivery latency were
not tested. Premium alone is not evidence of exchange entitlements.

## Production contract: global-market-map/v1

This README owns the schema; the JSON owns the dated values. Consumers must reject
unsupported schema versions, duplicate keys/IDs, unknown references and unavailable
measurement targets. Additive metadata may be ignored only if it cannot alter
identity, units, timing, availability or measurement semantics. Breaking field or
convention changes require a new schema version. Pin both Git revision and the
SHA-256 of the exact UTF-8 registry bytes in downstream evidence.

- `series` contains exactly 20 unique, stable `series_id` values:
  `spx, sxxp, topix, mchi, eem, us02y, us10y, dfii10, de10y, jp10y, dxy,
  usdjpy, usdcnh, oas, brent, copper, gold, vix, move, funding_basis`.
  These identify concepts, not tickers. Legacy IDs `mchi` and `eem` identify
  China and emerging-market equity concepts even if their ETF substitutes change.
  A symbol/provider change requires a new pinned registry revision, never an
  automatic splice of historical observations.
- `instrument` records the chosen symbol, observed loaded-feed alias, provider,
  machine unit and explanatory unit notes. Provider text is the canonical source
  identity for evidence matching. Do not equate an ETF listing exchange with its
  actual Cboe One delivery feed.
- `availability` is `available` or `unavailable`. The funding-basis row has
  null symbol/provider/unit and no measurement conventions. Its intended 3-month
  FX-swap construction is not verified; neither a longer-tenor cross-currency
  swap nor another stress indicator fills it.
- `observation` records frequency, clock context and publication notes.
  `published_at`, `available_at`, `max_age_seconds` and exact vendor session
  timezone are null where not established. These registry nulls do not forbid
  timestamped evidence in a future observation packet. Examples in notes are
  dated source-page updates, not recurring schedules or TradingView receipt times.
  Observation date, bar label, publication time and first usable availability
  must remain separate. Never manufacture midnight publication or freshness limits.
- `entitlement` records observed status, documented delay in minutes when known,
  the real-time exchange entitlement finding and evidence references. Null delay
  is unknown/not applicable, not zero. `not_present` describes the inspected
  exchange package; `not_verified` does not mean denied. Live labels are qualified
  by the closed-market audit. FRED data are daily publications, not live quotes.
- `proxy` gives kind and distinctions. ETFs introduce fees, tracking, dividends,
  USD trading prices and US hours; the regional cash indices retain local currency.
  DXY, COMEX copper and ICE BofA OAS are explicitly accepted substitutions.
- `measurement_conventions` declares unique IDs, exact definitions and output
  units. `level` uses the instrument unit. `change_bp` multiplies a difference
  of percent levels by 100; VIX/MOVE changes remain index points. Price percent
  change requires positive endpoints. These are measurement definitions, not
  signal thresholds, sampling rules or approved hypotheses.
- `futures` is null for non-futures. Brent/copper retain B-ADJ off and settlement
  daily closes. Exact historical switches and contract mappings remain null.
  Unadjusted roll discontinuities are not investment returns. A valid futures
  test must freeze actual contract histories and roll treatment separately.
- `history` records retrieved sample boundaries, counts, anomalies and export
  hashes when available. These are monthly loaded samples except the limited
  Brent daily sample, not complete daily coverage or maximum vendor depth.
  Private CSVs are not in this public repository. Early splices, unfinished
  monthly bars and the future-labelled Brent row must not become realized outcomes.
- `authorized_access`, `limitations` and `source_refs` preserve access routes,
  provenance limits and official documentation. Documented APIs do not establish
  a paid licence, key or exact external symbol mapping. TradingView manual CSV
  export is distinct from a customer market-data API.
- `verification.evidence` contains public audit transcriptions; references are
  local IDs. Private screenshots/exports are retained outside this repository.
  This handoff preserves the prior audit rather than claiming a new inspection.
- `derived_views` contains four extra chart panels, outside the 20-series
  identity set. `layouts.panels[].ref` resolves to a series or view ID.
  Funding & Stress has eight intended slots but seven populated charts; the
  unavailable entry is a logical slot, not a fabricated eighth chart.
  `chart_settings` describes the inspected display, including observed UTC-4
  chart clock; its named IANA setting was not verified.

## Observation bridge coordination

Dependency: [PR #786](https://github.com/Joshua-Asante/first-passage/pull/786),
README inspected at
[`c948e9e4e2f2948bad796ffb08819e584e5323ab`](https://github.com/Joshua-Asante/first-passage/blob/c948e9e4e2f2948bad796ffb08819e584e5323ab/scripts/global_pulse/README.md).

That revision deliberately accepts only `global-pulse-synthetic-registry/v1`.
Its fixture is a test interface and is **not** this production specification.
This PR publishes the registry; it does not add production support to the bridge.
The bridge must continue rejecting this registry until a separately reviewed
adapter and compatibility tests land. Do not relabel production metadata synthetic.

The adapter should validate this contract and retain the full pinned registry
alongside its internal projection:

| Bridge lookup | Production source / required behavior |
| --- | --- |
| `id` | `series_id`; preserve all 20 identities, block measurement of unavailable funding |
| `provider` | `instrument.provider`; evidence provider identity must match |
| `unit` | `instrument.unit`; exact source-level unit, no silent conversion |
| `conventions` | Key `measurement_conventions` by `id`; preserve exact definition/output unit and scale |
| `proxy` | Preserve kind and notes; only kind `none` permits no substitution warning |
| `futures_roll` | Preserve futures settings, unknown mapping and roll warning; null means non-futures |
| `max_age_seconds` | `observation.max_age_seconds`; null remains unknown, not unlimited-fresh |
| `watchlist.path/sha256` | Exact production file bytes; also retain its Git revision externally |

The packet's `observed_at`, `published_at` and `available_at` come from each
observation's evidence, not the registry audit date. Preserve the bridge timing
validation and unknown-time limitations. Verify that source evidence uses a
compatible observation clock: a daily bar's session start is not the completed
observation time. The bridge must not promote delayed, stale, unavailable or
publication-unknown measurements into timely evidence by dropping metadata.
Derived panels require separately defined adapter support; they are not extra
base-series IDs.

Adapter acceptance: run compatibility tests pinned to this registry's actual
revision and hash; cover unavailable funding rejection, percent-to-bp units,
ETF/provider aliases, all delay warnings, futures settings, unknown publication
times, and preservation of limitations. Synthetic fixture tests remain useful
but cannot discharge production compatibility.

## Saved setup and historical use

- [Global Pulse](https://www.tradingview.com/chart/WMYb20tE/) — eight charts.
- [Funding & Stress](https://www.tradingview.com/chart/fmsYFkbN/) — seven populated charts, funding gap.
- [Regional & Cross-Asset](https://www.tradingview.com/chart/4EZiX8Mc/) — eight panels.

Daily displays cover approximately one year. The regional comparison is a mixed
USD/EUR/JPY price comparison from the first visible bar, not a currency-neutral
fixed-base research feature. US ETF hours, European/Japanese closes, FX sessions,
futures settlement and daily FRED publication are asynchronous. Formal comparisons
need fixed sampling and information-availability cutoffs, common currency policy,
holiday handling and revision/vintage policy. FRED matched constant-maturity
spreads/breakevens avoid mixing live TVC benchmarks with lagged real yields.

## Bounded handoff and verification

Outcome: authoritative metadata and schema, preserved setup links and integrity
tests. Return boundary: registry PR; production bridge adapter, signal definitions
and hypothesis journal are subsequent work. No signal outcomes are tested here.

Run from this checkout with its supported launcher:

```powershell
.\fp.ps1 python -m pytest tests/ops/test_global_market_map_registry.py -q
.\fp.ps1 check
```

The tests cover stable identities, explicit gaps/unknowns, references, units,
delays, substitutions, chart slots and exclusion of private exports. They validate
the registry contract, not current vendor entitlements or source correctness.
