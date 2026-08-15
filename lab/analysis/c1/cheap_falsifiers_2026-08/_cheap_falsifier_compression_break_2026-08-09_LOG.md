# Cheap falsifier — compression→expansion break (Q-TNEC-CON-2) — `CHEAP_FALSIFIER_OK`

**Date:** 2026-08-09  
**Q-ID:** licenses authoring `Q-TNEC-CON-2` (not explore / not SHAPE-CLEAR)  
**Cost / K:** $0.00 · K=0 until G0 freeze  
**Lane:** [`docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md`](../../../docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) step 2  
**Runner:** [`_cheap_falsifier_compression_break_2026-08-09.py`](_cheap_falsifier_compression_break_2026-08-09.py)  
**Raw:** [`_cheap_falsifier_compression_break_2026-08-09_RESULTS.json`](_cheap_falsifier_compression_break_2026-08-09_RESULTS.json)  
**Panel:** `mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet`  
**Prior kill (no Q-ID):** [displacement fade](_cheap_falsifier_displacement_fade_2026-08-09_LOG.md)

## Frozen geometry (inherited)

G=10 · session-flat · RT 1.41 · EM3 · RTH dense 1m · roll-excluded

## GENEROUS thresholds (a priori)

- **2** consecutive narrow bars (range ≤ **1.0×** trailing 20-session median range)  
- next completed bar **closes** beyond the quiet high/low  
- enter **with** the break at the following open  

Kill rule: both arms powered (n≥100) **and** trade-weighted session-block 95% CI entirely &lt; 0.

## Result

| Arm | n | mean net R | WR | stop rate | session-block 95% CI |
|---|---:|---:|---:|---:|---|
| long | 5,187 | −0.053 | 0.130 | 0.863 | [−0.148, **+0.044**] |
| short | 4,992 | −0.078 | 0.106 | 0.887 | [−0.189, **+0.039**] |

eligible sessions (θ warm) 1,648 · break clocks 90,780 · elapsed ~171s

**Verdict:** `CHEAP_FALSIFIER_OK` — point estimates negative, but CIs straddle 0 on both arms → not a conclusive $0 kill. Licenses G0 freeze only; explore may still FALSIFY.

## Disposition

- Proceed to `PREREG_G0` + S6 ADMIT + inquire brief under `Q-TNEC-CON-2`  
- Explore GO unpaid; CONFIRM unread  
- Lane consecutive-kill counter unchanged (**1/3** = CON-1 only)
