# Q-MNQSEL-2 — CLOSURE: `RESOLVED` (dense 1m selection ceiling)

**Verdict:** `RESOLVED` (C4) — selection headroom exists on dense RTH 1m opens at G=10
**Closed:** 2026-08-08
**Pre-registration:** [`PREREG.md`](../../lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/PREREG.md)
**Parent:** [`Q-MNQSEL-2`](../rnd-pipeline/Q-MNQSEL-2-dense-1m-selection-ceiling-scoping.md)
**Spend / K:** $0.00 · K=0 · Cap **not claimed**
**Live effect:** none — no selector, no Pine, no rail
**Artifacts:** [`RESULTS.md`](../../lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/RESULTS.md)

---

## 1. Verdict

| Route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | S3 ≥ 0.40 ∧ S1 &lt; 0.40 on ≥1 arm | S3 long **0.8584** / short **0.8566**; S1 both &lt; 0 | ✓ |
| `FALSIFIED` | S3 &lt; 0.40 both arms | — | — |

---

## 2. Model update

Restart-clock universe (MNQSEL-1) had no EM1 headroom; **dense RTH 1m opens at G=10 do**.
Oracle sits near the clean-target tautology (0.859) because ~every session has a 1R hit among
390 clocks — the ceiling is real, not a free strategy. Next work is a **named construct**
(entry rule + stop + session-complete exit), not denser OF on these clocks.

---

## Iterate — loop exit

- **Verdict used:** `RESOLVED`
- **Next:** ITERATE → [`Q-MNQDTL-CON-1`](../Q-MNQDTL-CON-1-dense-1m-em-construct-scoping.md) (construct; unpaid)
- **Stop / re-proposal:** Re-open of *this* Phase-0 cell requires new mechanism evidence, not G retune
- **Board write:** construct unpaid; Cap reservation separate; R2FLOW STOP stands

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-08 | Closure filed — RESOLVED C4; construct ITERATE | Cursor + JA |
