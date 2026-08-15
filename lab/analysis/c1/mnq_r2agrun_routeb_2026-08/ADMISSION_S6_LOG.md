# SPEC S6 admission log — Q-R2AGRUN-1

**Date:** 2026-08-08  
**Input:** [`admission_s6.json`](admission_s6.json)  
**Command:** `$env:PYTHONPATH='lab'; python -c "from discovery.admission_schema import load_admission, evaluate_admission; …"`

| Field | Value |
|---|---|
| decision | **ADMIT** |
| reasons | `()` |
| floor_at_k(1) | 0.650 |
| Cap | 1.0 |
| power | 0.998817 (≥ power_min 0.50) |
| EM1/EM2 | omitted — SHAPE-UNSCREENABLE until tradeable stop/R |
| n_events basis | conservative floor under VOID-POWER=2000; RTH aggressor runs with `N_min=2` are dense on `tbbo` (structural sanity ≫10k/day class) — do not treat as measured EXPLORATION n |
| Spec | [`2026-08-07-loop-s6-k-aware-generation-spec.md`](../../../../docs/spec/2026-08-07-loop-s6-k-aware-generation-spec.md) |

Exploration remains free on frozen EXPLORATION windows; K spends only at CONFIRM (S6 step 3). Cap seat not claimed at G0.
