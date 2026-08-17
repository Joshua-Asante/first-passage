# MNQ-SIZEDIV-1 — STAGE1_DIAG (outcome-free; confirm-year conditioner)

**Run:** 2026-08-15T21:19:19+00:00 · cache `C:\Users\joshu\.databento_cache\mnq_sizediv_blind_2026-08\confirm_year`
**Panel (calendar only):** `C:\Users\joshu\multi_firm_operations\core\data\bar_data\MNQ_M15.csv` sha256 `6c86f41a17b7dfce…` (time column read; no prices)

> ⚠ **QUARANTINE.** `stage1_sessions.csv` holds A(s) for CONFIRM-era sessions.
> No return series may be joined to it before the Stage-3 battery (FREEZE §3).

| Metric | Value | Frozen rule | Result |
|---|---|---|---|
| Sessions parsed / full | 258 / 244 | full ≥ 240 | ok |
| Signable share | 1.0000 | ≥ 0.5 | ok |
| corr(I_vw, I_cw) | 0.7251 | ≤ 0.995 | ok |
| Tick-rule agreement | 0.8714 (n=121,345,446) | ≥ 0.5 else flip | B=buy confirmed |
| sd(A) / AC1(A) | 0.00731 / -0.029 | report-only | — |

**Verdict: `CLEAN`**

## Monthly A(s) (report-only)

| month   |         mean |        std |   count |
|:--------|-------------:|-----------:|--------:|
| 2025-08 | -0.00140888  | 0.00817338 |      12 |
| 2025-09 | -0.00191245  | 0.0102106  |      21 |
| 2025-10 | -0.000452882 | 0.0091793  |      23 |
| 2025-11 | -0.00192728  | 0.00576374 |      18 |
| 2025-12 | -0.00319067  | 0.00693343 |      21 |
| 2026-01 | -0.000905118 | 0.00682928 |      20 |
| 2026-02 | -0.000963698 | 0.00664287 |      19 |
| 2026-03 | -0.0017149   | 0.00699052 |      22 |
| 2026-04 |  0.000305338 | 0.00735642 |      21 |
| 2026-05 | -0.000503287 | 0.00630624 |      20 |
| 2026-06 | -0.00236701  | 0.00577996 |      21 |
| 2026-07 | -0.0033047   | 0.00587842 |      19 |
| 2026-08 |  0.0022855   | 0.0103342  |       7 |
