# Q-SPX-F09 — CLOSURE: FALSIFIED

**Verdict:** `CLOSED-FALSIFIED` (2026-06-20)
**Pre-registration:** [`PREREG-F09.md`](PREREG-F09.md) (falsifier fixed before `f09_gate.py` existed; HEAD `7a50011`)
**Harness:** [`f09_gate.py`](f09_gate.py) + [`f09_harness_check.py`](f09_harness_check.py) (leakage proofs + power controls ALL PASS)
**Pre-score audit:** 5-agent adversarial audit → **NO HALT defects, leakage unanimously CLEAN, verdict() FAITHFUL, SCORE-OK** (1 MAJOR = calendar-mark documentation, applied; NITs hardened — none move the verdict).
**Feed grade:** staging (BAR_EXPORT 5m, parity not re-validated). A FALSIFIED-direction verdict does not need gate-bearing fidelity — the absence is in the significance, which is comprehensively absent.

---

## Result vs the pre-registered §6 gate

**PRIMARY (L=63, calendar-day-last-close, N=1631, 2021-01-03→2026-06-11):**

| Quantity | Value | PREREG §6 |
|---|---|---|
| Δ = E[m\|mom] − E[m\|rev] | **−2.175 bps** | FALSIFIED if Δ≤0 → **FIRED** |
| E[m\|mom] / E[m\|rev] | −7.327 / −5.153 bps | (both negative; RESOLVED needs E[m\|mom]>0 ∧ E[m\|rev]<0 — fails) |
| cyclic-rotation perm p | **0.6413** | FALSIFIED if p≥0.10 → **FIRED** |
| halves Δ (h1 / h2) | −6.039 / +2.373 bps | FALSIFIED if sign-flip → **FIRED** |
| drop-top-5 / drop-top-10 Δ | −2.873 / −4.629 bps | (more negative — not rescuably few-day-carried) |
| Δ by year (bps) | 2021 −19.1 · 2022 −8.3 · 2023 +1.9 · **2024 −1.0** · 2025 +7.2 · 2026 −11.4 | the +AC1 momentum year (2024) gate Δ is **negative** — the estimator fails exactly where it must work |

**All THREE FALSIFIED triggers fired independently.** This is not a marginal close.

**Payoff framing (interpretability):** pure-momentum = −5.84 bps/day, pure-reversion = +5.84, **GATED = +1.19 bps/day** — acting on the regime state is *worse* than unconditionally fading. The state is descriptive (labels regimes in hindsight) but not predictive with lead.

**Robustness echoes (descriptive only, all corroborate FALSIFIED):**
- L=42: Δ −4.56, perm p 0.81, halves both negative.
- L=126: Δ −3.99, perm p 0.76, halves sign-flip.
- **RTH-close (15:55 ET cash close — the audit's MAJOR tripwire): Δ −2.95, perm p 0.71, halves both negative.** Confirms the 23:55-ET calendar-mark artifact is NOT driving the result.
- ER-sign (alternate Kaufman-efficiency estimator): Δ −2.38, both means negative — failure is not estimator-specific.

---

## What the pre-registration predicted vs what happened

The PREREG framed F09 as the load-bearing gate: *if* the regime state is predictively observable with lead, the trailing estimator separates forward momentum sign (Δ>0, perm-significant, stationary, robust). **None of those held.** The state is anti-predictive at the daily horizon (Δ wrong sign), indistinguishable from chance (perm p 0.64), and non-stationary (halves flip). The hypothesis that you can *switch* between momentum and reversion on an observable regime signal is dead on this corpus.

## Consequence — the directional axis collapses

Per the Identify catalog (2026-06-20), F09 was the gate every regime-conditional directional family hung on. With F09 FALSIFIED:
- **CLOSED by implication:** the directional halves of F01 (opening-range), F02 (compression→expansion), F06 (ETH-ORB), F25 (event-window), F32 (post-large-move) — they all required a feasible regime gate to avoid losing in the wrong regime. No gate → no rationale.
- **SURVIVES:** the direction-agnostic primitives F07 (vol-clock), F08 (vol-clustering), F34 (range-AC), F10 (efficiency) — but as **risk/sizing infrastructure, not alpha** (they predict magnitude/state, not direction; a vol-magnitude edge has no clean directional-CFD expression).

## Side observation (NOT a finding, NOT chased)

The unconditional daily reversion (pure-rev) had gross mean +5.84 bps/day — but it is (a) marginal (~2.3 SE gross, ~1.4 SE net of ~2.3 bps round-trip), (b) the catalog's cost-fragile F19/F22 family, (c) regime-unstable (2021 strong, 2024 weak), and (d) computed on the 23:55-ET calendar mark (overnight microstructure, not a clean cash move). It is a forward-watch belt at most; chasing it would be a fresh Q with its own PREREG and would face the anti-SNAG bar. **Not pursued.**

## Lesson candidates

- **L-F09-1 (methodology, no dollar anchor — candidate):** "Test the gate before the families." One daily-horizon meta-test (the regime-state lead-time question) closed an entire *class* of catalog directional families at ~1/10th the cost of testing each. Generalizes the strategy-validation §0 "selection-level tests outrank parameter-level" principle to "axis-gating tests outrank family-level tests." Promote if it recurs.
- **L-F09-2 (instrument prior):** the SPX500 momentum/reversion regime is real but *discontinuous and lagging* — a trailing estimator cannot front-run the flip (2025 was a tariff-shock discontinuity, not a slow drift). Cross-references the portfolio-side [[project_decompound_remc_canonical_shift_2026_06_07]] lead-time problem (regime is load-bearing but hard to act on predictively).

## Anti-SNAG accounting

F09 ran to a **powered, decisive FALSIFIED** (unlike the un-runnable F9/F10 ICT-execution layers, which couldn't reach a verdict and so did NOT count). It is a **4th null across a 4th distinct family** (regime-state-predictability — distinct from D1 inventory-reversal, F5 calendar, D2 ICT-geometry). **SPX500 → 4 nulls / 4 families.** The SNAG signal intensifies materially; the directional-alpha class is now closed-by-gate. Any future directional concept on US500 faces a strengthened anti-SNAG bar and needs path-independent new-mechanism evidence, not a re-scored family.

## Reproduce

```bash
python lab/analysis/spx500_f09_gate_2026-06-20/f09_harness_check.py  # leakage + controls, expect ALL PASS
python lab/analysis/spx500_f09_gate_2026-06-20/f09_gate.py           # expect FINAL VERDICT: FALSIFIED
```
