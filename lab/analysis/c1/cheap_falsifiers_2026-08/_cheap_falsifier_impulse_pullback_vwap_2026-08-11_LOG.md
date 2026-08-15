# Cheap falsifier — impulse→pullback→VWAP-reclaim (Q-TNEC-CON-5) — `CHEAP_FALSIFIER_OK`

**Date:** 2026-08-11  
**Q-ID:** licenses authoring `Q-TNEC-CON-5` (not explore / not SHAPE-CLEAR)  
**Cost / K:** $0.00 · K=0 until G0 freeze  
**Lane:** [`docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md`](../../../docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) step 2  
**Runner:** [`_cheap_falsifier_impulse_pullback_vwap_2026-08-11.py`](_cheap_falsifier_impulse_pullback_vwap_2026-08-11.py)  
**Raw:** [`_cheap_falsifier_impulse_pullback_vwap_2026-08-11_RESULTS.json`](_cheap_falsifier_impulse_pullback_vwap_2026-08-11_RESULTS.json)  
**Panel:** `mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet`  
**Distinct from:** CON-1–4 through-break / compression · fade-to-VWAP · ORB · PDH/PDL

## Domain-bar consult (executed 2026-08-11)

```text
python scripts/instrument_profiles.py cell MNQ impulse-pullback-vwap-reclaim
=== MNQ x impulse-pullback-vwap-reclaim ===
verdict: untested — no prior on this cell.
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
```

**Route answer:** ① temporal selectivity (first reclaim / session) outside mapped levers per [`ADR 2026-08-10`](../../../docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md). Hold-time not claimed. Mechanism id `impulse-pullback-vwap-reclaim` NEW in [`MECHANISMS.md`](../../../ops/instruments/MECHANISMS.md). Cost-geometry distinction vs CON-4: pullback-depth stop (~19 pt) vs day-range stop (~257 pt).

## Frozen geometry (a priori)

| Knob | Value |
|---|---|
| Clock | **1m** RTH |
| Bias | first 30m close@09:59 vs open@09:30 |
| VWAP | session typical-price VWAP from RTH open |
| Settle | bias-side reclaim after tag |
| Entry | with-bias reclaim at **next 1m open** |
| Selectivity | **first** valid signal per session |
| Stop | pullback extreme (tag→reclaim) · `R=(pts−1.41)/stop_dist` |
| Exit | session-flat |

Kill: coverage &lt;20% → VOID; both arms n≥100 and session-block CI entirely &lt;0 → FALSIFIED.

## Result

| Check | Value |
|---|---|
| eligible sessions | 1,669 |
| trade sessions | 1,507 (**90.3%**) |
| n trades (first/session) | 1,507 |
| mean signed pts | **+0.60** |
| mean stop_dist | **19.1 pt** |
| gross/(4×RT) | **0.11×** |
| elapsed | ~37s |

| Arm | n | mean net R | WR | session-block 95% CI |
|---|---:|---:|---:|---|
| long | 784 | **+0.0061** | 0.149 | [−0.284, **+0.327**] |
| short | 723 | **−0.4268** | 0.101 | [−0.709, **−0.095**] |

**Verdict:** `CHEAP_FALSIFIER_OK` — coverage clears; not both-arms CI&lt;0 (short alone would kill if both-arm rule were one-sided; formal kill needs both). Licenses G0 freeze only; explore may still FALSIFY. Stop-geometry claim held (~19 pt vs CON-4 ~257); gross still far below 4×RT at the point estimate. Short arm already CI-entirely-negative on the full panel.

## Disposition

- Proceed to `PREREG_G0` + S6 ADMIT + inquire brief under `Q-TNEC-CON-5`
- Explore GO unpaid; CONFIRM unread
- Lane consecutive-kill counter unchanged (**1/3** = CON-1 only)
