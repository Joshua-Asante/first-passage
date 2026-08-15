# COMPLETE advisory Gate B battery — CONCEPT-USOIL-RGC-001 (B-1…B-6 + floors)

**Date:** 2026-06-20 · **Status:** **ADVISORY — NOT a Gate B verdict (NO-VERDICT, PREREG §10)** · 0 anti-SNAG slots consumed.
**Script:** `gate_b_full_advisory.py` (reuses the parity-validated Python pre-filter + the B-3/B-4/B-5 deflation harness; `exitAtrLength=22`).
**Why:** the 2026-06-15 preview ran only B-3/B-4/B-5. The operator un-parked and directed "run USOIL RGC B." The authoritative path needs the native rank-ρ leg (B-0 leg 2, ~10 operator-manual TV cell exports) which is **not** runnable this session — so this completes the **full** frozen §6 battery on the Python tier to give a comprehensive advisory verdict rather than a single-gate one.

## Authority status (faithful to the frozen pre-reg)

Gate B-0 requires **both** legs: `parity_check` (✅ reconciled 2026-06-15 — 532/533 native trades exact @ exitAtrLength=22) **AND** `rank_correlation_falsifier` ρ≥0.70 on native cell exports (**never run**). Per §6/§10, without the native rank-ρ leg the Python tier carries **no gate authority** → this is **NO-VERDICT / advisory**, consuming **0** anti-SNAG slots. It does not write D4 or move the null count.

## Result (winner = max-Sharpe cell 576/2.5/3.5, n=441)

| Gate | Test | Result |
|---|---|---|
| floor n≥30 | trade-count floor | **PASS** (441) |
| floor cost | expectancy ≥ 4× cost (~0.08R) | **PASS** (≈ +0.10R; per-trade Sharpe 0.084 — near-zero but positive) |
| **B-1 PBO + CPCV** | CSCV PBO (48mo×36cfg, S=12, 924 combos) + purged CPCV OOS | **FAIL** — **PBO = 0.655** (IS-best below OOS median on 66% of splits). CPCV OOS mean +0.0005, 82% folds>0, but PBO ≥ 0.50 fails the gate |
| B-2 sign/label permutation | winner expectancy vs Rademacher sign-flip null (B=2000) | **PASS** — p = 0.042 (marginal). (entry-timing scheme p=0.97; trade-order omitted — mean is order-invariant) |
| **B-3 DSR @ honest N=36** | best-of-36 Sharpe vs E[max SR₃₆] (Bailey & LdP) | **FAIL** — Sharpe 0.0843 vs benchmark 0.0517; **DSR 0.785; p = 0.215** (confirms 2026-06-15) |
| B-4 breadth + drop-top-episode | ≥8/~25 profitable, ≥3↑ ∧ ≥3↓; survive drop-top | **PASS** — 13/27 profitable (7↑/6↓); drop-top-episode net $25.6K (top=44%) |
| B-5 fat-tail exclusion | survive COVID-window AND invasion-episode independently | **PASS** — excl-COVID +$47.1K, excl-invasion +$44.6K |
| B-6 plateau | ±1-step neighbours, dome not cliff (same-feed) | **PASS** — 5/5 neighbours positive; median +0.0004 ≥ ½ centre → dome |

**OVERALL (AND of all legs) = FALSIFIED-direction.** Failing legs: **B-1 PBO, B-3 DSR** — the two **multiplicity** gates, both scale-invariant and properly computed.

## Read

The 2026-06-15 preview FALSIFIED-direction on B-3 alone; the complete battery **strengthens** it — a **second, independent** multiplicity detector (PBO via CSCV) also fails. The candidate is genuinely **broad** (B-4), **not fat-tail-dependent** (B-5 — improves without COVID), **plateau-stable** (B-6, dome), and **marginally** beats a sign-null (B-2, p=0.042) with a positive ~0.10R expectancy (PF 1.33). It looks like a real strategy — and that is exactly the trap the pre-reg §4 named: **on a no-persistence instrument (VR≈1, Hurst≈0.54), a structured-looking grid whose best-of-36 cell does not survive honest-N multiplicity correction is selection noise.** Two independent corrections (PBO 0.655, DSR p=0.215) agree it does not survive. B-2's marginal pass (p=0.042) and B-4/B-5/B-6 passing do **not** rescue it — the multiplicity gates are the load-bearing ones the pre-reg explicitly weighted, and both fail.

## Caveats (advisory — do not over-read)

- **NO authority:** the authoritative verdict still needs the native rank-ρ cert + native B-1…B-6. The Python tier is parity-validated (532/533 exact), so this is a strong predictor, not a verdict.
- **PBO matrix** uses monthly net-R aggregation (48mo × 36cfg) — the standard CSCV construction for trade strategies; DSR (B-3) is partition-independent and corroborates.
- **floor_cost unit fix:** the engine `returns` are per-trade fractional equity returns (1R loss = −riskPerTrade% = −0.005); R-multiple = returns/0.005 → mean ≈ +0.10R. The verdict rests on the **scale-invariant** B-1/B-3, not the floor.
- Episode partition reproduced 32 daily-EMA segments (vs ledger F3 ~25) — segmentation-method-sensitive; B-3/B-1 do not depend on it.

## Disposition

**FALSIFIED-direction (advisory, NO-VERDICT, 0 slots).** Strengthens the 2026-06-15 park: the apparent edge is selection noise on **two** independent multiplicity gates, not one. To convert to a **formal FALSIFIED-REJECT** (register D4 in `docs/rejected_candidates.md` §D + the USOIL ledger; consume 1 of ≤3 concept-run slots; USOIL → **4 nulls**), the operator runs the native rank-ρ 10-cell exports (B-0 leg 2) and the authoritative battery is re-run natively. **EV of doing so is low** — the parity-validated advisory is comprehensive and negative; the native cert would, per the 2026-06-15 reasoning, very likely just confirm FALSIFIED at operator cost + 1 slot. Recommendation: accept the advisory and keep the concept parked/rejected-on-advisory unless the formal corpse-on-record is specifically wanted; the 2026-08-08 regime trigger remains the natural revisit boundary.
