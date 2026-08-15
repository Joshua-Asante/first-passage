# Cheap falsifier — displacement fade (Q-TNEC-CON-2 candidate) — `FALSIFIED`

**Date:** 2026-08-09  
**Q-ID spent:** **none** (killed before G0 / brief)  
**Cost / K:** $0.00 · K=0  
**Lane:** [`docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md`](../../../docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) step 2  
**Runner:** [`_cheap_falsifier_displacement_fade_2026-08-09.py`](_cheap_falsifier_displacement_fade_2026-08-09.py)  
**Panel:** `mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet`

## Frozen geometry (inherited)

G=10 · session-flat · RT 1.41 · EM3 · RTH dense 1m · roll-excluded

## GENEROUS thresholds (a priori)

- prior-bar range ≥ **1.0×** trailing 20-session median range  
- body/range ≥ **0.50**  
- enter **against** bar direction at next open  

Kill rule: both arms powered (n≥100) **and** trade-weighted session-block 95% CI entirely &lt; 0.

## Result

| Arm | n | mean net R | WR | stop rate | session-block 95% CI |
|---|---:|---:|---:|---:|---|
| long | 9,493 | **−0.157** | 0.081 | 0.917 | **[−0.240, −0.069]** |
| short | 9,724 | **−0.165** | 0.072 | 0.925 | **[−0.266, −0.071]** |

eligible sessions (θ warm) 1,648 · displacement clocks 170,295 · elapsed ~177s

**Verdict:** `FALSIFIED` — stop-dominated fade; same shape as CON-1 death (CI entirely below 0 both arms).

## Disposition

- **No** `Q-TNEC-CON-2` · **no** PREREG_G0 · **no** explore GO  
- Lane consecutive-kill counter: still **1/3** (CON-1 only; cheap-falsifier kills do not consume a campaign slot)  
- Next: operator chooses another family (shortlist B compression→expansion, or C / new)

## Note (method)

First pass used equal-weight session-*mean* bootstrap; that CI disagreed in sign with trade-weighted mean_R and falsely printed `CHEAP_FALSIFIER_OK`. Re-run uses session-block resample → concatenate trades → mean (trade-weighted). Corrected run is authoritative.
