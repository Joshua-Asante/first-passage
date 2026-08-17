# MNQ-SIZEDIV-1 — STAGE2_FALSIFIER (TRAIN semester; outcome-coupled)

**Run:** 2026-08-15T21:32:13+00:00 · cache `C:\Users\joshu\.databento_cache\mnq_sizediv_blind_2026-08\train_sem` · panel `C:\Users\joshu\multi_firm_operations\core\data\bar_data\MNQ_M15.csv`

| Metric | Value | Frozen rule | Fired |
|---|---|---|---|
| n trades / exec sessions | 252 / 126 | — | — |
| mean signed gross (bp) | -2.0603 | F1 KILL if ≤ +0.911 | True |
| hit rate vs base | 0.4960 vs 0.5357 | F2 KILL if ≤ base | True |
| relabel corr sign(A) vs sign(R_s) | +0.7226 | F3 KILL if \|·\| ≥ 0.5 | True |
| session-block 95% CI (bp) | [-9.426, +5.138] | F4 report | — |

**Verdict: `KILL`** (PASS ≥ +1.822 bp; HOLD ∈ (+0.911, +1.822]; else KILL)

PASS is a spend license only (~36% false-go at this n — FREEZE §4); the battery is the evidence standard.
