# Cheap falsifier — HTF-native 5m compression break (Q-TNEC-CON-3) — `CHEAP_FALSIFIER_OK`

**Date:** 2026-08-10  
**Q-ID:** licenses authoring `Q-TNEC-CON-3` (not explore / not SHAPE-CLEAR)  
**Cost / K:** $0.00 · K=0 until G0 freeze  
**Lane:** [`docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md`](../../../docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) step 2  
**Runner:** [`_cheap_falsifier_htf_native_break_2026-08-10.py`](_cheap_falsifier_htf_native_break_2026-08-10.py)  
**Raw:** [`_cheap_falsifier_htf_native_break_2026-08-10_RESULTS.json`](_cheap_falsifier_htf_native_break_2026-08-10_RESULTS.json)  
**Panel:** `mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet`  
**Distinct from:** CON-2 (1m / fixed G=10) · HTF-bias→LTF filter (`FALSIFIED`) · T-IMB / SWING-1

## Domain-bar consult (executed 2026-08-10)

```text
python scripts/instrument_profiles.py cell MNQ htf-compression-breakout-5m
=== MNQ x htf-compression-breakout-5m ===
verdict: untested — no prior on this cell.
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
EXIT:1
```

**Route answer:** ① temporal selectivity (first 5m break / session) outside mapped cross-instrument levers per [`ADR 2026-08-10`](../../../docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md) §2-A/B. Price/hold-time levers not claimed as the rescue. Mechanism id declared NEW in [`MECHANISMS.md`](../../../ops/instruments/MECHANISMS.md).

## Frozen geometry (a priori)

| Knob | Value |
|---|---|
| Clock | **5m** RTH (resampled from 1m panel) |
| Compression | `K_NARROW=2` · `NARROW_MULT=1.0` · med20 of 5m ranges |
| Settle | close beyond quiet extreme **and** vs quiet midline |
| Entry | with-break at **next 5m open** |
| Selectivity | **first** valid signal per session only |
| Stop | opposite quiet extreme · `R=(pts−1.41)/stop_dist` |
| Exit | session-flat |

Kill: coverage &lt;20% → VOID; both arms n≥100 and session-block CI entirely &lt;0 → FALSIFIED.

## Result

| Check | Value |
|---|---|
| eligible sessions (θ warm) | 1,648 |
| break sessions | 1,510 (**91.6%**) |
| n trades (first/session) | 1,510 |
| mean signed pts | **+2.99** |
| mean stop_dist | 31.2 pt |
| elapsed | ~62s |

| Arm | n | mean net R | WR | session-block 95% CI |
|---|---:|---:|---:|---|
| long | 794 | **+0.063** | 0.304 | [−0.079, **+0.203**] |
| short | 716 | −0.035 | 0.229 | [−0.216, **+0.151**] |

**Verdict:** `CHEAP_FALSIFIER_OK` — coverage clears; not both-arms CI&lt;0. Licenses G0 freeze only; explore may still FALSIFY. Point estimates mixed; CIs straddle on both arms.

## Disposition

- Proceed to `PREREG_G0` + S6 ADMIT + inquire brief under `Q-TNEC-CON-3`
- Explore GO unpaid; CONFIRM unread
- Lane consecutive-kill counter unchanged (**1/3** = CON-1 only)
