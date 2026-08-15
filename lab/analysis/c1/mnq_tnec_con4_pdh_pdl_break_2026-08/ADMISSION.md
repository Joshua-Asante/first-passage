# Q-TNEC-CON-4 — S6 `evaluate_admission` (pre-score)

**Date:** 2026-08-10  
**Input:** [`ADMISSION.json`](ADMISSION.json) · `registered_k=1`  
**Runner:** `PYTHONPATH=lab python -c "from discovery.admission_schema import load_admission, evaluate_admission; …"`

```
decision: ADMIT
reasons: []
floor_at_k: 0.65
cap: 1.0
```

EM1/EM2 left null (scored after explore; 0.40R remains disclosure per TNEC-1).  
EM3/EM4/EM5 declared true a priori (structural hard stop, session-flat, independent first/session entries, weekly cadence attainable, RTH slot legal).  
MNQDTL D1/D2 not gates (null). Cap not claimed.
