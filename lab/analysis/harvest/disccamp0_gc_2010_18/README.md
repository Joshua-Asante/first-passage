**Theme:** harvest
**Status:** ACTIVE — DISC-CAMP-0 binding artifacts (Stage 2/3/5 staging)
# DISC-CAMP-0 binding artifacts (Stage 2/3/5 staging, 2026-07-13)

Pre-result binding utilities for the GC→MGC pipeline shakedown
(`docs/ltm/briefs/rnd-pipeline/DISC-CAMP-0-shakedown.md`; binding freeze
`docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md`).

- `bind_k.py` — T from the pinned volume-lead stitch of the era-tagged Stage-2
  cache (GC.FUT parent ohlcv-1h + 1d, IS 2010-06-06:2018-12-31) → K bracket via
  `discovery.k_count`. **Bound 2026-07-13: T = 51,659 → K_DSR = 3,177**
  (raw-overlap diagnostic 154,912). Deterministic count only — no candidate
  statistic examined. Manifest: `discovery_manifests/disccamp0_gc_2010_18.json`.
- `block_size.py` — pre-reg §4 frozen rule (smallest lag with |ACF| inside the
  95% white-noise band) on stitched IS log returns, roll-boundary returns
  excluded. **Bound 2026-07-13: block_size = 3** (n = 51,616, band ±0.008627;
  ACF re-exceeds the band at lags 7–13 — recorded, rule applied as frozen).

- `series.py` — shared implementation of the pinned stitch + within-contract
  (return-adjusted) log returns, used by the Stage-3+ drivers.
- `run_stage3.py` — Stage-3 mining driver (STUMPY m∈{30,60,90} + catch22 on 1h;
  ruptures PELT on daily; 6 frozen IS rules h=3/q=0.05; IS cost-law + permutation-p
  triage). **Executed 2026-07-13: all-null** — 0/6 clear the cost-law (mean net
  −0.4bp…−2.2bp vs +9.56bp 4× hurdle; p=1.0 all); manifest CLOSED, 0 survivors;
  K_SPA will bind 0. Outputs: `stage3_report.json`, `stage3_frozen_rules.json`
  (shapes + provenance — the frozen candidates), `stage3_regime_labels_daily.csv`
  (1 segment, no breaks at frozen penalty 10.0), `stage3_close_pvalues.csv`.

Data cache is local-only (`~/.databento_cache`, era-tagged
`--campaign-id disccamp0_gc_2010_18 --phase discovery`); nothing here re-bills.
