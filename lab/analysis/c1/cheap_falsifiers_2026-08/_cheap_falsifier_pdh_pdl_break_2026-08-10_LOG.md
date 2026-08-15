# Cheap falsifier — PDH/PDL RTH with-break (Q-TNEC-CON-4) — `CHEAP_FALSIFIER_OK`

**Date:** 2026-08-10  
**Q-ID:** licenses authoring `Q-TNEC-CON-4` (not explore / not SHAPE-CLEAR)  
**Cost / K:** $0.00 · K=0 until G0 freeze  
**Lane:** [`docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md`](../../../docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) step 2  
**Runner:** [`_cheap_falsifier_pdh_pdl_break_2026-08-10.py`](_cheap_falsifier_pdh_pdl_break_2026-08-10.py)  
**Raw:** [`_cheap_falsifier_pdh_pdl_break_2026-08-10_RESULTS.json`](_cheap_falsifier_pdh_pdl_break_2026-08-10_RESULTS.json)  
**Panel:** `mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet`  
**Distinct from:** CON-2/3 compression · ORB · MNQPROX · N9/C10 attraction/fade

## Domain-bar consult (executed 2026-08-10)

```text
python scripts/instrument_profiles.py cell MNQ pdh-pdl-breakout-rth
=== MNQ x pdh-pdl-breakout-rth ===
verdict: untested — no prior on this cell.
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
```

**Route answer:** ① temporal selectivity (first PDH/PDL break / session) outside mapped levers per [`ADR 2026-08-10`](../../../docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md). Hold-time not claimed. Mechanism id `pdh-pdl-breakout-rth` NEW in [`MECHANISMS.md`](../../../ops/instruments/MECHANISMS.md).

## Frozen geometry (a priori)

| Knob | Value |
|---|---|
| Clock | **1m** RTH |
| Levels | prior RTH session high/low (PDH/PDL) |
| Settle | close beyond PDH (long) or PDL (short) |
| Entry | with-break at **next 1m open** |
| Selectivity | **first** valid signal per session |
| Stop | opposite prior extreme · `R=(pts−1.41)/stop_dist` |
| Exit | session-flat |

Kill: coverage &lt;20% → VOID; both arms n≥100 and session-block CI entirely &lt;0 → FALSIFIED.

## Result

| Check | Value |
|---|---|
| eligible sessions (have prior) | 1,667 |
| break sessions | 1,467 (**88.0%**) |
| n trades (first/session) | 1,466 |
| mean signed pts | **+1.56** |
| mean stop_dist | **279.5 pt** |
| gross/(4×RT) | **0.28×** |
| elapsed | ~17s |

| Arm | n | mean net R | WR | session-block 95% CI |
|---|---:|---:|---:|---|
| long | 850 | **−0.0048** | 0.536 | [−0.042, **+0.033**] |
| short | 616 | **−0.0028** | 0.471 | [−0.051, **+0.043**] |

**Verdict:** `CHEAP_FALSIFIER_OK` — coverage clears; not both-arms CI&lt;0. Licenses G0 freeze only; explore may still FALSIFY. Both point estimates near zero / slightly negative; CIs straddle; stop width ~10× CON-3's structural quiet stop.

## Disposition

- Proceed to `PREREG_G0` + S6 ADMIT + inquire brief under `Q-TNEC-CON-4`
- Explore GO unpaid; CONFIRM unread
- Lane consecutive-kill counter unchanged (**1/3** = CON-1 only)
