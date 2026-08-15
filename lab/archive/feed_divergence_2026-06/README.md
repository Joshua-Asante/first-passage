# Q-FEED-1 — feed divergence analysis (2026-06)

> **BLOCKED / NON-RUNNABLE (substrate Phase 5, 2026-07-30)** — Dukascopy
> `*_duka.csv` bytes deleted per
> [`docs/adr/2026-07-22-challenge-era-substrate-retirement.md`](lab/archive/../../docs/adr/2026-07-22-challenge-era-substrate-retirement.md)
> disposition B. Hashes:
> [`docs/ltm/notes/2026-07-30-oanda-dukascopy-data-tombstone.md`](lab/archive/../../docs/ltm/notes/2026-07-30-oanda-dukascopy-data-tombstone.md).
> Earlier freeze: 2026-06-17 Dukascopy adapter retirement. `fetch_duka_panels.py`
> was deleted; `measure_divergence.py` / `_lib.py` remain as frozen analysis
> artifacts and **do not run**. Byte-independent parsing tests in
> `tests/test_feed_divergence_parsing.py` still pass.

Measures bar-level Dukascopy ↔ TV/Pepperstone divergence per
`docs/ltm/briefs/Q-FEED-1-dukascopy-tv-feed-divergence.md`. Closure gates ratification of
`docs/adr/2026-06-12-rnd-feed-instrument-class-split.md`.

## Run order

```bash
# NON-RUNNABLE after Phase 5 — historical command sequence only.
# Phase 1 (manual): TV BAR EXPORT v0.1 — see BAR_EXPORT_v0.1.md
# Drop List-of-Trades CSVs into core/data/tv_exports/pepperstone/bar_export/

# Optional: validate parse + cross-check
python lab/archive/feed_divergence_2026-06/parse_tv_export.py --symbol USDJPY

# Phase 2: Dukascopy panels — BYTES DELETED (substrate Phase 5)
# python lab/archive/feed_divergence_2026-06/fetch_duka_panels.py
# python scripts/check_data_manifests.py --regenerate

# Phase 3a/3b/4: blocked — no *_duka.csv on disk
```

Frozen window: **2026-03-01 → 2026-06-01**, M15. Thresholds:
`docs/ltm/briefs/pre-registration/Q-FEED-1-verdict-preregistration.md`.

## BAR EXPORT v0.1

Pine script: `bar_export_v01.pine` (gitignored by `**/*.pine`; copy to TV manually).
Spec: `BAR_EXPORT_v0.1.md`. Record chart timezone in `tv_chart_tz.txt` before export.

## Output files

| Path | Role |
|---|---|
| `FROZEN_CONVENTION.txt` | Week-1 calibration winner (single line) |
| `RESULTS.md` | Decomposition table + `FROZEN-CONVENTION` echo |
| `core/data/bar_data/*_M15_duka.csv` | Phase 2 Dukascopy panels — **DELETED** substrate Phase 5 |
| `core/data/tv_exports/pepperstone/bar_export/*_M15_pep.csv` | Phase 1 TV exports |

## Deferred: ADR Phase-1 provenance rename consumer sweep

Post-ratification rename sweep is **moot for Dukascopy** after Phase 5 byte
deletion. Historical note only — do not restore `*_duka` panels without a new ADR.
