# H-FCCARRY-1 — CLOSURE: `SCREEN-FAIL (effect absent)` (carry-timing Sharpe ≈ 0.09, no edge)

**Closed:** 2026-07-20 (same session as the F-C GO). Operator authorized the Databento own-cohort δ-extraction (carry data + 1 family-K).
**Fork:** F-C (carry timing-δ, 6E/6J/CL) from the [`Q-BOOKFIT-1`](Q-BOOKFIT-1-closure-resolved.md) fork program; operator **GO 2026-07-20** (order F-A → F-C → F-B), F-C nod given this session.
**Pre-registration:** manifest [`discovery_manifests/fc_carry_6e6j6cl.json`](../../../discovery_manifests/fc_carry_6e6j6cl.json) (`register_search open`, **K=1**, frozen before any strategy return computed) + the pre-committed construction in [`extract_carry_delta.py`](../../../lab/archive/q_fccarry_1_2026-07/extract_carry_delta.py) header.
**Run artifacts:** [`lab/archive/q_fccarry_1_2026-07/`](../../../lab/archive/q_fccarry_1_2026-07/) — `extract_carry_delta.py`, `carry_results.json`, `combined_monthly_returns.csv`
**Data:** {6E,6J,CL} front (.c.0) + second (.c.1) ohlcv-1d, GLBX.MDP3, IS era 2010-06-06→2018-12-31 (Databento, **est + billed $0.00**, 15.7k bars).

## Verdict

**`SCREEN-FAIL (effect absent)`.** The pre-committed combined carry-timing portfolio earns an annualized Sharpe indistinguishable from zero — it fails Requirement-4 power before the cost-law is even reached.

| Metric | Value |
|---|---|
| N (months) | 103 |
| δ (mean monthly return) | **6.8 bp/mo** |
| σ (monthly) | 253 bp |
| δ/σ (per-month effect) | **0.027** (vs Req-4 ≥ 0.122) |
| **Annualized Sharpe** | **0.092** |
| t / p (one-sided, positive) | 0.27 / **0.394** |
| Manifest survivors (naive α / Bonferroni / BH) | **0 / 0 / 0** |
| Per-leg Sharpe | 6E 0.058 · 6J 0.112 · CL 0.041 |

**Req-4 power FAIL** (δ/σ 0.027 ≪ 0.122). The cost-law (Req-5) is moot — there is no edge to charge cost against.

## Faithfulness (M-15 guard — is the null real or a construction bug?)

The null is **real, not a scoring artifact**:
- **No sign inversion:** all three legs are small-*positive* (0.04–0.11). A defective/inverted carry sign against a genuine factor would read strongly *negative*; it does not.
- **Returns track ground truth:** CL front-month reproduces the known 2014–2016 oil crash (mean ~$105 in 2014-06 → ~$31 in 2016-02).
- The effect is simply ~zero for this construction over this window.

## Construction caveat (bounds what this closes — and what it does NOT)

The pre-committed rule was deliberately the **simplest faithful carry-timing form**: per-instrument *own-carry-sign* (front−second), monthly rebalance, equal-weight across three legs, one combined return series (K=1). This is what Q-BOOKFIT projected as the F-C "carry timing" leg. **This closes that specific construction.** It does **not** falsify carry as a factor in general: a **cross-sectional** carry factor (rank a broad universe, long top / short bottom) or a magnitude-weighted timing rule is a *different hypothesis* requiring its own pre-registration and K — **not a re-run of this** (re-running variants until one works is the multiplicity the K-ledger forbids; Trap #12). Own-sign timing on three instruments is known-weak relative to cross-sectional carry; that is consistent with this null.

## Disposition — the fork program is now exhausted on the edge side

- **H-FCCARRY-1 CLOSED**, **K=1 banked** (manifest committed; `discovery_manifests/` count +1). First non-zero carry-construct bank on record for 6E/6J/CL.

- **Registry:** rejected_candidates.md — ### F-C carry-timing (own-carry-sign) × 6E/6J/CL — SCREEN-FAIL (effect absent)
- **Two of three priced forks fail on edge:** **F-A** (H-ZNAUC-1) died at the Stage-2 **cost-wall** (δ 1bp vs 6–10bp); **F-C** (this) dies at **effect-absence** (Sharpe 0.09). Two distinct null modes. **F-B** (CL EIA) remains formally un-run — lowest priority, and scoping already flagged it as bid-to-cover-style informed-flow + in-session overlap.
- **Q-BOOKFIT-1's book-*fit* finding stands, undisturbed:** the M-21 risk-geometry projection (F-A ρ 0.512, F-C ρ 0.295) was always "the risk geometry fits," never "edge exists." Both forks confirm the edge side fails — exactly the split the M-21 coordinates keep separate. **No re-open of Q-BOOKFIT** (its RESOLVED verdict was risk-geometry-only).
- **The breadth lever is empty at current supply.** This is the disposition Q-BOOKFIT §6 anticipated for its downstream: the priced fork inventory does not yield a deployable book-diversifying edge. It **strengthens the decompound-HOLD "no static counterbalance" finding** (extended from sizing → breadth-leg → now the whole priced fork set). The book's remaining levers are **sizing** and **live-data authorization moves**, not breadth from these seeds.

## Recommendation (operator decision)

1. **Declare the Q-BOOKFIT fork program exhausted** (F-A cost-wall, F-C effect-absent; F-B the weakest remaining and un-run) — the honest 0/2 edge outcome; OR
2. **Run F-B** for completeness (its own δ-extraction; scoping already flags the informed-flow risk) before declaring exhaustion. Low cost, but low prior.
3. New book breadth would require **new mechanism evidence** (a fresh Tier-A seed clearing the harvest §2.1 cost-wall) — not a re-run of these three. The 2026-11-08 idle review is the standing home for that.

## §10 audit-hook discharge

- Databento pull est + billed **$0.00** ✔ · dry-run before pull ✔
- Manifest **opened (K=1) BEFORE the strategy return was computed** ✔ (register_search open timestamp precedes the extraction; construction frozen in the script header)
- Faithfulness anchor run (CL vs known oil crash; per-leg sign sanity) — M-15 discharged ✔
- Manifest closed with survivor p; 0/0/0 at naive/Bonferroni/BH ✔ · K=1 banked ✔
- No construction re-run after seeing the null (Trap #12) ✔
