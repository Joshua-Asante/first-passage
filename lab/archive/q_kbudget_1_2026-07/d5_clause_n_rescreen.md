# D5 (DJ30/NAS gamma-positioning, MYM/MNQ expression) — Clause-N re-screen

**Status:** **RATIFIED 2026-07-15** — confirm-construct = **intraday-momentum footprint**; gamma-sign declined; DJ30 drop/down-weight. D5 screens **PASS (K+N)**; Q-KBUDGET-1 verdict **RESOLVED**. This note remains the derivation record; live row lives in [`RESULTS.md`](RESULTS.md) + `floor_scan.py` + pre-reg §E.
**Frozen screen:** [`docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md`](lab/archive/../../docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md) §B (freeze `b304f2c`). §B/§C/§D are untouched by this note.
**Trigger (historical):** §D's disposition for D5 — "re-screen when [the missing input is] supplied… or 2026-08-08, whichever first." Operator pin discharged the trigger 2026-07-15 (construct pin, not a data buy). §B separately admits "literature median with citation" as a cohort-cited prior — this note supplied that citation.
**Reproduce:** `python lab/archive/q_kbudget_1_2026-07/d5_power.py` (zero pulls, zero K consumed; Clause-K floor reproduced on the production `lab/research_utils/deflated_sharpe.py` module).

---

## The pivotal decision — pin D5's confirm construct (operator-owned; **decided 2026-07-15**)

**Operator pin (2026-07-15):** construct **(i)** — intraday-momentum footprint. Construct (ii) declined. Asks 2–3 below also accepted (Baltussen NQ prior; NAS100/NQ sole anchor).

The Phase-1 inventory declared D5 as "DJ30/NAS **gamma-positioning** mechanism." That phrase was ambiguous between two distinct literatures, which screen oppositely on Clause N:

| Construct | Citable per-index δ+σ? | Clause N |
|---|---|---|
| **(i) Intraday-momentum footprint** — dealer short-gamma hedging → rest-of-day return predicts last-30-min return (Baltussen, Da, Lammers & Martens 2021, *JFE*, "Hedging demand and market intraday momentum") | **Yes** — estimated per-index: NQ futures β=6.36 (t=7.97, OOS-R²=3.76%); YM futures β=5.02 (t=4.12, OOS-R²=1.69%… 2.18% futures) | **PASS** (below) |
| **(ii) Gamma-*sign* mechanism** — net-long gamma suppresses / net-short amplifies (SqueezeMetrics GEX; Amaya, Garcia-Ares, Pearson & Vasquez 2025) | **No** — every peer-reviewed gamma-sign estimate is SPX-only; transplanting the SPX δ to NQ/YM would be a cross-instrument cohort-provenance violation | **stays UNSCREENABLE** |

**Construct (i) is the only reading with a tradeable per-index expression *and* a citable cohort δ;** (ii) has no NDX/Dow cohort and is, even on its native SPX, economically small (Amaya et al. 2025: max +3.3pp annualized vol, mean impact *negative*). Pinning (i) was verdict-determining and is now operator-ratified.

## Clause K — settled PASS (construct-independent)

Clause K depends only on the axis's declared search design, not on which confirm construct is chosen. Declared K_intrinsic 1–3 (mechanism-first), family MYM/MNQ banks K_banked=0 (no closed manifest) → K_eff 1–3.

Reproduced on the production module:

| K_eff | floor(K_eff) | Cap 1.0 |
|---|---|---|
| 1 | 0.65 | PASS |
| 2 | 0.85 | PASS |
| 3 | 0.98 | PASS |
| (4) | (1.06) | (would FAIL — outside declared range) |

**Clause K: PASS at every declared K_eff.** This is the low-K regime the M-19 floor is beatable in — 0.65–0.98, not the 2.05 that killed DISC-CAMP-0 (Q-GATECART-1) or the 1.835 that killed D6.

## Clause N — PASS under construct (i), at the declared panel

Frozen formula: `power = Φ(√N·|δ|/σ − 1.96)`, N = full declared OOS event count (§E: "~10³ daily"), δ/σ = cohort-cited central per-day standardized effect.

Deriving δ/σ from the Baltussen NQ cohort, two independent ways:
- **From OOS-R² (3.76%):** ρ = √0.0376 = **0.194** (upper-bound reading — R² measures explained variance, not the sign-adjusted correlation directly, so this is generous)
- **t-scaled from t=7.97** at the study's own approximate sample size (N_pub ≈ 2,500–5,000 trading days): **0.113–0.159** — the more conservative, "central plausible-true effect" reading per §B's instruction to use the central value, not the top of the range

**Recommended plug: δ/σ = 0.113** (the more conservative t-scaled reading).

```
N = 1,000 (declared axis panel, ~10^3 daily events)
power = Phi(sqrt(1000) * 0.113 - 1.96) = Phi(1.58) = 0.947
```

**0.947 ≥ 0.50 → PASS on Clause N**, with wide margin. Even a further haircut to δ/σ=0.090 (below both derivations) holds power 0.81; only an aggressive haircut to ≈0.062 (the break-even point) fails.

**Null named (§5 hygiene, per `strategy-validation`):** the Baltussen effect is measured as an OOS *timing* signal (rest-of-day conditional on morning dealer-hedging flow → predicts last-30-minute return) against a zero-timing null, not against unconditional drift — it is not a rediscovery of long-only trend exposure.

## Row update — applied 2026-07-15

UNSCREENABLE → `PASS — K_eff 1–3 (floor 0.65–0.98 ≤ Cap 1.0); N≈1000 daily events, delta/sigma=0.113 (Baltussen et al. 2021 JFE, NQ futures cohort, t=7.97), power=0.947`. Live in `floor_scan.py` / `results.json` / [`RESULTS.md`](RESULTS.md) / pre-reg §E.

## Effect on the KBUDGET verdict — **RESOLVED** (2026-07-15)

Combined with D7's screened-FAIL ([`d7_clause_n_screen.md`](d7_clause_n_screen.md)): 6 screened-FAIL, 1 PASS (D5), 0 UNSCREENABLE. Per the frozen §D table, **RESOLVED requires only "≥1 ratified-inventory axis PASSES Clause K and clears Clause N"**. Closure §6 + parent brief status record the flip.

## The honest downstream flag — where D5 actually gets tested

Per §B, "**a PASS never blesses** — it only licenses campaign scoping." The Clause-N PASS confirms the effect is statistically demonstrable at the declared panel — not that it is *tradeable net of costs*. The same OOS-R² that yields high power implies a naive gross annualized Sharpe ≈ 3.08 (daily IC=0.194 × √252), which is manifestly not the net tradeable Sharpe — it is the gross statistical footprint. Baltussen's own headline Sharpe (1.73) is gross and multi-asset; **only SPX-futures is shown to survive tick-level costs — NQ/YM net-of-cost survival is undemonstrated** in the cited literature.

D5's real test, if funded, is therefore the standing campaign HARD gate (§R clause-reachability + the DSR-K ADR power disclosure): does the *net* MNQ intraday-momentum Sharpe clear the Clause-K floor of **0.65–0.98** at K_eff 1–3? That floor is *achievable* (unlike DISC-CAMP-0's 2.05) but unproven on real, cost-inclusive returns.

## DJ30 leg — recommend drop or low-weight only

Per the companion B4 procurement research (see PR description / this branch's D5 procurement summary): Dow gamma is sourceable only via the DIA (ETF) / YM (futures) proxy — DJX index options are too thin (OI ≈ $472M notional). Every vendor "covering Dow" uses this proxy; the Baltussen YM cohort is itself the weakest of the studied indices (t=4.12 vs NQ's t=7.97), and DIA/YM liquidity is ~25–60× thinner than the QQQ/NQ equivalents. **Recommend running NAS100/NQ as the sole anchor leg; drop DJ30 or carry it only as a low-weight confirmation overlay.** Cboe's 2026-05-18 DJX daily-expiry launch may change this — re-check at 2026-08-08.

## Ratification asks — **all three answered 2026-07-15 (operator)**

1. **Pin the confirm construct** — **(i) intraday-momentum footprint** (gamma-sign declined).
2. **Accept the Baltussen NQ prior as the cohort-cited δ** for Clause N (single-study caveat stands — §B "literature median" satisfied loosely).
3. **Scope NAS100/NQ-only** (DJ30 drop/down-weight) per the B4 finding above.

## Audit hooks

```bash
python lab/archive/q_kbudget_1_2026-07/d5_power.py
# expect: Clause K PASS at K_eff 1-3 (floor 0.65/0.85/0.98); Clause N power=0.947 at N=1000, delta/sigma=0.113

git diff b304f2c -- docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md | grep -A2 '## §B' && echo "CHANGED -- investigate" || echo "stable (untouched)"
```
