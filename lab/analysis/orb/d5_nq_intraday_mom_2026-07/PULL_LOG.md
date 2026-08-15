# D5 Stage-1 — cost-gated pulls (MNQ OOS + NQ IS)

**Campaign:** `d5_nq_intraday_mom`  
**Pre-reg:** [`docs/briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md`](../../../docs/briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md)  
**Manifest:** [`discovery_manifests/d5_nq_intraday_mom.json`](../../../discovery_manifests/d5_nq_intraday_mom.json) (`open` 2026-07-16T04:28:30Z, K=1, lane=mechanism-first)

`--max-cost 1.00` on every pull; both estimates **$0.00**. Inside $125 free-credit window. Summed Stage-1 billable ≈ 0.332 GB.

## 1. MNQ OOS (native micro — confirm/realism era)

| Request | Cost | Billable | Records |
|---|---|---|---|
| `MNQ.v.0` continuous `ohlcv-1m` 2019-05-06→2026-07-16 `--phase oos` | **$0.00** | 141,986,040 B (~0.142 GB) | 2,535,465 |
| `MNQ.v.0` continuous `ohlcv-1h` (reference, not pulled) | $0.00 | 2,380,560 B | 42,510 |

```
PYTHONPATH=lab python -m databento_fetch.db_fetch pull \
  --symbols MNQ.v.0 --stype continuous --schema ohlcv-1m \
  --start 2019-05-06 --end 2026-07-16 \
  --campaign-id d5_nq_intraday_mom --phase oos --max-cost 1.00
```

- **Roll:** `.v.0` (volume-rolled — Q-TVCOV-1 pin for equity-index micros)
- **Cache:** `~/.databento_cache/ohlcv-1m_continuous_ce119c1e8f923316.dbn`
- **Rows:** 2,535,465
- **Vendor note:** BentoWarning — reduced-quality days include 2020-02-27/28, 2020-06-30 (degraded)

## 2. NQ IS (parent — discovery/tuning era)

| Request | Cost | Billable | Records |
|---|---|---|---|
| `NQ.FUT` parent `ohlcv-1m` 2010-06-06→2019-01-01 `--phase discovery` | **$0.00** | 190,211,784 B (~0.190 GB) | 3,396,639 |

```
PYTHONPATH=lab python -m databento_fetch.db_fetch pull \
  --symbols NQ.FUT --stype parent --schema ohlcv-1m \
  --start 2010-06-06 --end 2019-01-01 \
  --campaign-id d5_nq_intraday_mom --phase discovery --max-cost 1.00
```

- **Symbology:** parent (all NQ expiries — volume-lead stitch at analysis time, DISC-CAMP-0 pattern)
- **IS window:** dataset floor 2010-06-06 → exclusive end 2019-01-01 (last included = 2018-12-31)
- **Cache:** `~/.databento_cache/ohlcv-1m_parent_de42fcda759883ba.dbn`
- **Rows:** 3,396,639
- **Vendor note:** BentoWarning — reduced-quality days include 2014-06-11/12/13 (degraded); record in Stage-6 defect log if those sessions enter the IS edge series

## Stage-1 data complete

Both OOS-axis legs cached. **Stage-2/4 done 2026-07-16 — cost-law KILL** (see [`RESULTS.md`](RESULTS.md)).
