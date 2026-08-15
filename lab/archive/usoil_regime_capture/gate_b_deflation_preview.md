# Advisory deflation preview — CONCEPT-USOIL-RGC-001 (B-3/B-4/B-5 on the Python tier)

**Date:** 2026-06-15 · **Status:** **ADVISORY — NOT a Gate B verdict** (sweep ADR 2026-06-05: Python tier has no authority). 0 anti-SNAG slots consumed. Operator-chosen step (cheap pre-screen before the native rank cert).
**Script:** `gate_b_deflation_preview.py` (reuses the parity-validated loader; exitAtrLength=22).
**Why:** the N=36 grid preview showed a structured candidate (best PF 1.33, longer-channel cluster). On a no-persistence-prior instrument (W2/F2: VR≈1, Hurst≈0.5) that is a *candidate, not an edge*; this previews whether it survives deflation before spending 10 operator-manual native TV runs.

## Result

| Gate | Test | Result |
|---|---|---|
| **B-3 DSR @ N=36** | best-of-36 Sharpe vs E[max SR₃₆] (Bailey & López de Prado, `lab/validation/dsr.py`) | **FAIL** — Sharpe 0.0843 vs benchmark 0.0517; DSR 0.785; **p-value 0.215 ≫ 0.05** |
| B-4 breadth | ≥8/~25 profitable episodes, ≥3 up ∧ ≥3 down (daily-EMA 10/50 partition) | PASS — 13 profitable of 27 traded (7 up / 6 down) |
| B-4 drop-top-episode | net survives removing the single best episode | PASS — $45.8K → $25.6K (top episode = 44% of net) |
| B-5 COVID-exclusion | net survives excluding 2020-04..06 | PASS — net $47.1K (improves; 33 trades removed) |
| B-5 invasion-exclusion | net survives excluding 2022-02-24..03-31 | PASS — net $44.6K (13 trades removed) |

Winner = max-Sharpe cell **576/2.5/3.5** (= max-PF cell). cross-trial sr_variance 5.78e-4.

## Read

The candidate is **broad** (B-4) and **not fat-tail-dependent** (B-5 — it survives removing both the COVID crash and the 2022 invasion, even improving without COVID). But it **fails B-3, the multiplicity gate** — the one test that catches "the best cell looks good because it's the best of 36 tries." Best-cell per-trade Sharpe 0.084 only modestly exceeds the selection benchmark 0.052, leaving a 21% chance the result is spurious. On an instrument with no persistence prior, this is the textbook **selection-noise** signature: a structured-looking grid whose best cell does not survive the honest-N correction.

**This is exactly what the pre-reg §4 anticipated:** "because oil shows no autocorrelated drift … a profitable backtest is more likely selection/noise than on a persistent instrument. The edge must survive on fat-tail capture under the DSR/honest-N gauntlet." It does not.

## Caveats (do not over-read; advisory)
- **Advisory tier:** the authoritative verdict needs the native rank-ρ cert + native B-1…B-6. But the Python tier is parity-validated (532/533 exact), so this is a strong predictor of the native result.
- **B-3 is partition-independent** (DSR uses only the winner's return series + cross-trial Sharpe variance), so the FAIL is robust to the episode-partition approximation.
- **Episode partition is approximate:** this run reproduced 32 daily-EMA segments (15 up/16 down) vs the ledger F3's ~25 (13/12) — segmentation-method-sensitive (F3 is LOW-confidence on exact counts). The breadth PASS (13 profitable ≫ 8) is robust to the count; B-3's FAIL does not depend on it.
- Per-trade returns carry the L-WARMUP-PHANTOM left-edge inflation + compounding; removing the phantoms (noise) would not rescue a sub-threshold DSR.

## Disposition — PARKED (operator decision 2026-06-15)
**Operator parked CONCEPT-USOIL-RGC-001 on this advisory evidence** (2026-06-15): no native rank cert / authoritative battery run, **0 anti-SNAG slots consumed**, NOT registry-listed (not a formal FALSIFIED), revisit at the 2026-08-08 regime trigger. Recommendation that drove it, below.

**Park CONCEPT-USOIL-RGC-001.** The advisory deflation says the apparent edge is selection noise (B-3 DSR p=0.21). Running the operator-manual native rank cert + authoritative B-1…B-6 would, on a parity-validated tier, very likely just confirm FALSIFIED at the cost of ~10 native TV runs + 1 anti-SNAG slot. This would be the **4th USOIL null** (D1 transplant, D2 carry, D3 spike-fade, D4 regime-capture) — high instrument-level SNAG density. The 2026-08-08 regime trigger is the natural revisit point. If the operator still wants the *formal* FALSIFIED on the record, run the native cert — but the EV is low and the advisory result is clear.
