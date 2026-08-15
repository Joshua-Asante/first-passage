# Q-KBUDGET-1 Phase-2 screen — RESULTS (2026-07-14; D5/D7 re-screened 2026-07-15; D5 ratified → RESOLVED)

**Verdict: `RESOLVED`** (frozen pre-reg §D: ≥1 axis PASSES both clauses) — flipped 2026-07-15 after operator confirm-construct ratification for D5 (intraday-momentum footprint; gamma-sign declined; DJ30 drop/down-weight). Historical path: AMBIGUOUS-HOLD 2026-07-14 → D7 FAIL + D5 hinge narrowed 2026-07-15 morning → D5 ratified afternoon. Live harness output of `floor_scan.py` (this session): **6 FAIL / 1 PASS / 0 UNSCREENABLE**.

Frozen screen: [`Q-KBUDGET-1-screen-preregistration.md`](lab/archive/../../docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md) (freeze `b304f2c`, G1) · Ratified inventory: [`Q-KBUDGET-1-phase1-inventory.md`](lab/archive/../../docs/briefs/Q-KBUDGET-1-phase1-inventory.md) (ratification anchor `ca02030`, G2 2026-07-14 — this directory postdates it, §F hook #1 ordering holds).
Harness: [`floor_scan.py`](floor_scan.py) on production `lab/research_utils/deflated_sharpe.py` — pure arithmetic, zero pulls, zero K consumed. Machine output: [`results.json`](results.json). Re-screen companions: [`d7_clause_n_screen.md`](d7_clause_n_screen.md) + [`d7_power.py`](d7_power.py); [`d5_clause_n_rescreen.md`](d5_clause_n_rescreen.md) + [`d5_power.py`](d5_power.py). Closure: [`docs/briefs/closures/Q-KBUDGET-1-axis-reachability-screen.md`](lab/archive/../../docs/briefs/closures/Q-KBUDGET-1-axis-reachability-screen.md) §5–§6.

## Screen table (§E row-fill; live output of `floor_scan.py` as of D5 ratification)

| Axis | Family | K_intr | K_banked | K_eff | floor | Clause K (Cap 1.0) | N | δ, σ (citation) | Power | Screen |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 GC/MGC successor (any design) | GC/MGC | ≥1 | 3,177 | ≥3,178 | 2.05 | FAIL | — | — | — | **FAIL (K)** |
| D2 wide mining, other GLBX family | ES/NQ/YM | 10³–10⁴ | ≤1 | 10³–10⁴ | 1.93–2.17 | FAIL | — | — | — | **FAIL (K)** |
| D3 HARV-class ES month-end mechanism | ES | 1–2 | 1 | 2–3 | 0.85–0.98 | PASS | ~100 (monthly, 2018+) | +13–19.2 bp (HARV-0 cohort) | **0.24–0.30, joint 0.05–0.06** (inherited: Q-HARV-1 §R DECLINE, `9bddd33`) | **FAIL (N, inherited)** |
| D4 XAU T3b swap-dealer COT (prop expr = GC/MGC) | GC/MGC | 1–2 | 3,177 | ≥3,178 | 2.05 | FAIL | ~10³ (weekly) | no citable δ (T3 partial = 4 bars) | — | **FAIL (K; UNSCREENABLE-moot on N)** |
| D5 NQ/MNQ intraday-momentum footprint (was: gamma-positioning) | MYM/MNQ | 1–3 | 0 | 1–3 | 0.65–0.98 | PASS | ~10³ (daily) | Baltussen et al. 2021 *JFE* NQ cohort δ/σ=0.113; confirm-construct = **intraday-momentum footprint** (operator-ratified 2026-07-15); DJ30 drop/down-weight; gamma-sign declined | **0.947** | **PASS (K+N) — ratified 2026-07-15** |
| D6 eurusd_pattern_enum Phase-4 | 6E/EURUSD | 450 (locked) | 0 | 450 | 1.835 | FAIL | — | — | — | **FAIL (K, declared)** |
| D7 JPY month-end mechanism (6J expr) | 6J | 1–3 | 0 | 1–3 | 0.65–0.98 | PASS | ~10² (monthly) | +13 bp / σ≈90 bp — HARV class-analogue (`9bddd33`); no non-circular JPY-native δ exists | **0.30** (< 0.50) | **FAIL (N, class-analogue) — screened 2026-07-15** |

Screened: 6 FAIL / 1 PASS · UNSCREENABLE: 0 → **RESOLVED** (fundable set non-empty).

## Named missing inputs — both discharged

- **D5 (discharged 2026-07-15 by operator pin):** confirm-construct = intraday-momentum footprint; Baltussen NQ δ/σ=0.113 accepted; NAS100/NQ sole anchor (DJ30 dropped/down-weighted). See [`d5_clause_n_rescreen.md`](d5_clause_n_rescreen.md).
- **D7 (discharged 2026-07-15):** screened FAIL via HARV class-analogue. See [`d7_clause_n_screen.md`](d7_clause_n_screen.md).

**What this licenses:** D5 campaign scoping under standing HARD gates (HARV §R + net-of-cost Sharpe vs Clause-K floor). Screen PASS never blesses a candidate and never authorizes a Databento pull. **Inventory expansion** (additional axes beyond D1–D7) is a separate Pre-Q — [`Q-KBUDGET-HARVEST-1`](lab/archive/../../docs/briefs/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md) — riding the 2026-08-08 re-screen window; it does not reopen this verdict.

## Reproduce

```bash
python lab/archive/q_kbudget_1_2026-07/floor_scan.py
# expect: Screened FAIL: 6/7 · PASS: 1 · UNSCREENABLE: 0
#         Verdict per pre-reg §D: RESOLVED (fundable set non-empty)

python lab/archive/q_kbudget_1_2026-07/d7_power.py
# expect: power=0.303, FAIL

python lab/archive/q_kbudget_1_2026-07/d5_power.py
# expect: Clause K PASS at K_eff 1-3; Clause N power=0.947 at N=1000, delta/sigma=0.113
```

---

## Harvest Phase-3 addendum (2026-07-16) — append-only

D1–D7 historical table above is **unchanged** (Trap-12). Q-KBUDGET-HARVEST-1 ratified rows **H1** (`H-OD-1`) + **H2** (`H-TSMOM-1`) were appended to [`floor_scan.py`](floor_scan.py) and screened via [`axis_screen`](lab/archive/../research_utils/axis_screen.py).

**Harvest §6:** `RESOLVED` — see [`../q_kbudget_harvest_1_2026-07/PHASE3_RESULTS.md`](lab/analysis/q_kbudget_harvest_1_2026-07/PHASE3_RESULTS.md).

Live extended harness (this session): **6 FAIL / 3 PASS / 0 UNSCREENABLE** (PASS = D5 + H-OD-1 + H-TSMOM-1). Parent Q-KBUDGET-1 verdict stays RESOLVED; fundable discovery inventory grows from 1 → 3 axes for the 08-08 packet (scoping licenses only).
