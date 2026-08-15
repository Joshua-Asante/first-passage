# SPEC S6 admission log — Q-R2VBUCK-1

**Date:** 2026-08-08  
**Input:** [`admission_s6.json`](admission_s6.json)  
**Command:** `PYTHONPATH=lab python -c "from discovery.admission_schema import load_admission, evaluate_admission; …"`

| Field | Value |
|---|---|
| decision | **ADMIT** |
| reasons | `()` |
| floor_at_k(1) | 0.650 |
| Cap | 1.0 |
| power | 0.998817 (≥ power_min 0.50) |
| EM1/EM2 | omitted — SHAPE-UNSCREENABLE until tradeable stop/R |
| n_events basis | conservative floor under VOID-POWER=2000; EXPLORATION ~155 RTH days at B=2550 ≈1 bucket/RTH-minute implies ≫10k eligible if coverage clears |
| Spec | [`2026-08-07-loop-s6-k-aware-generation-spec.md`](lab/archive/../../../docs/spec/2026-08-07-loop-s6-k-aware-generation-spec.md) — first-campaign attempt |

Exploration remains free on frozen EXPLORATION windows; K spends only at CONFIRM (S6 step 3). Cap seat not claimed at G0.
