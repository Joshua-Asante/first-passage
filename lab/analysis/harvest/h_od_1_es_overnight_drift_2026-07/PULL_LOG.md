# H-OD-1 Stage-1 — cost-gated pull (ES parent IS)

**Campaign:** `h_od_1_es_overnight_drift`
**Pre-reg:** [`docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md`](../../../docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md)
**Manifest:** [`discovery_manifests/h_od_1_es_overnight_drift.json`](../../../discovery_manifests/h_od_1_es_overnight_drift.json) (`open` 2026-07-16T05:44:58Z by Cursor background agent, K=1, lane=mechanism-first; pull executed locally — Cursor cloud lacked `DATABENTO_API_KEY`, `BLOCKED — capability-problem` return on PR #405)

`--max-cost 1.00`; estimate **$0.00**. Inside the free-credit window. Stage-1 billable ≈ 0.244 GB.

## 1. ES parent IS (discovery/tuning era — the only leg pulled)

| Request | Cost | Billable | Records |
|---|---|---|---|
| `ES.FUT` parent `ohlcv-1m` 2010-06-06→2019-01-01 `--phase discovery` | **$0.00** | 243,815,208 B (~0.244 GB) | 4,353,843 |

```
PYTHONPATH=lab .venv-research/Scripts/python.exe -m databento_fetch.db_fetch pull \
  --symbols ES.FUT --stype parent --schema ohlcv-1m \
  --start 2010-06-06 --end 2019-01-01 \
  --campaign-id h_od_1_es_overnight_drift --phase discovery --max-cost 1.00
```

- **Symbology:** parent (all ES expiries — volume-lead stitch at analysis time, DISC-CAMP-0/D5 pattern)
- **IS window:** dataset floor 2010-06-06 → exclusive end 2019-01-01 (last included 2018-12-31)
- **Cache:** `~/.databento_cache/ohlcv-1m_parent_02cd77a6787c9a33.dbn`
- **Vendor note:** BentoWarning — reduced-quality days include 2014-06-11/12/13 (degraded); recorded for the Stage-6 defect log (Stage 6 never ran — Stage-2 KILL)

## Legs NOT pulled (deliberate deviation from handoff §2.2, cheap direction)

The handoff scheduled three pulls before Stage-2. Stage-2 needs only the IS leg; it was run
first and **KILLED**, so the ES-parent OOS leg and the MES OOS realism leg were **not pulled**
(no purpose post-KILL; $0.00 either way but no unnecessary cache/era-tag).

## Stage-1 data complete for the adjudicated stage

**Stage-2/4 run 2026-07-16 — cost-law KILL + gate-geometry defect finding** (see [`RESULTS.md`](RESULTS.md)).
