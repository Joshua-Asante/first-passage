# Q-REGIME-COND-1 (re-scoped, Option B) — FINDINGS

**Verdict: FALSIFIED** (brief §6). The four-axis risk composite carries **no stable conditional
forward second-moment information on SPY independent of trailing realized volatility**. The raw-state
vol/tail separation is genuine but is **substantially repackaged trailing volatility** — it collapses
under orthogonalization. → **vol-target directly; do NOT author Q2.** Spawn return: `DONE`.

**Scope (operator-chosen 2026-06-30):** the one genuinely-new, decision-relevant angle the existing
closures did not cover — composite vs **SPY** forward second-moment at **high daily power**, with the
trailing-RV orthogonalization as the load-bearing null. Pre-registered + frozen at commit `46f47d1`
(`preregistration.md`) **before** any forward return was read (audit anchor; brief §5 #1, §10).

**§7 parent review (4 adversarial passes, all PASS):** spec/scope-creep (no overlay/HMM; prereg precedes
forward returns; nothing post-hoc retuned), code quality (expanding-only normalization, non-overlapping
stats, block-not-iid bootstrap, residual genuinely re-derived, self-tests pass), consolidated read
(verdict follows from the joint raw-strong/residual-collapse evidence), and an independent skeptic that
reimplemented the residual pipeline from scratch (reproduced residual 5d SEP_vol −0.00069 to 5 dp),
enumerated all residual cells (0 are monotone+positive+large+gate-surviving), and closed the residual-PCA1
gap (now baked into the artifacts; null). No blocking issues.

---

## The result in one table (equal-weight composite, non-overlapping windows)

`corr(composite, trailing 20d RV) = +0.648` → the composite is heavily vol-loaded by construction.

| | RAW states | RESIDUAL states (orthogonalized vs trailing RV) |
|---|---|---|
| 5d SEP_vol (off−on) | **+0.0106** · placebo **100th** pct · p_FWER **0.0015** | −0.0007 · placebo 39th · p_FWER 0.93 |
| 5d SEP_cvar | +0.0336 · placebo 99th · p_FWER 0.065 | −0.0023 · placebo 32nd · p_FWER 0.93 |
| 20d SEP_vol | +0.0106 · placebo 90th | +0.0085 · placebo **58th** · p_FWER 0.76 |
| 20d SEP_cvar | +0.0290 · placebo 72nd | +0.0219 · placebo 51st · p_FWER 0.82 |
| monotone (off>neu>on)? | **False everywhere** (it is `off`-vs-rest, not a gradient) | **False everywhere** |

**The load-bearing null (Step 2.6) decides it.** Every residual-state test fails **all three** RESOLVED
conditions simultaneously: (a) **non-monotone** (4/4), (b) **does not beat the 95th-pct placebo** (max
58th), (c) **does not survive the multiplicity discount** (min p_FWER 0.76). The raw separation, by
contrast, is real and survives FWER (5d vol p_FWER 0.0015) — but that is the well-known vol-clustering /
variance-risk-premium effect at the index level, and it lives in the part of the composite that **is**
trailing vol.

## Why this is robust (not a single-test artifact)

- **Block-bootstrap CIs (21d circular block, B=2000):** every residual SEP CI **straddles zero** —
  5d_vol [−0.0050, +0.0002, +0.0052], 20d_vol [−0.0148, +0.0031, +0.0216], cvar likewise.
- **Sign-unstable across subperiods:** residual SEP_vol = **−0.0099** (2009–2017) → **+0.0072**
  (2018–2026) → **−0.0013** (COVID-out). No stable effect; the small full-sample 20d positive is one
  half-sample reversing the other.
- **Orthogonalization-method-independent:** the full-sample-OLS residual cross-check **flips sign** vs
  the point-in-time residual at 20d (+0.0085 PIT vs −0.0025 FS) and is non-monotone under both → the
  residual "separation" is method-dependent noise.
- **No axis carries it (drop-one jackknife):** residual SEP_vol stays within ±0.007 and flips sign as
  any single axis is dropped.
- **Secondary composite (PCA-1) agrees:** the residualized PCA-1 composite is monotone at 5d/20d (20d
  SEP_vol +0.0236) — the most RESOLVED-looking cell in the whole study — yet still **fails every
  confirmatory gate**: placebo 85.5th pct (<95), p_FWER 0.36, bootstrap CI [−0.008, +0.024] straddles
  zero, subperiod sign-flip (−0.0093 → +0.0375), and it nearly vanishes with COVID removed (+0.006). A
  full-sample / COVID-concentration mirage, not a signal. (Monotonicity alone is necessary, not
  sufficient — it fails (b) and (c).)
- **Conservative null:** the point-in-time residual is **not perfectly orthogonal** to trailing RV
  (corr −0.283, vs ≈0 for the full-sample residual which is orthogonal by OLS construction; the early
  expanding-OLS coefficients are unstable). The version that retains the most residual RV-association
  (PIT) shows the **largest** apparent positive 20d separation; improving the orthogonalization
  (full-sample, corr ≈0) shrinks and flips it (+0.0085 → −0.0025). So the apparent residual separation
  is itself a de-volling artifact that *decreases* as cleaning improves — the null is conservative, not
  an under-cleaning false negative.

## Independent operational strike (brief §2.5)

State **median dwell = 3–4 trading days**, **19.5 state-changes/yr** — the indicator **flips faster than
the 5d and 20d horizons it would predict**. Even the (vol-driven) raw separation would be hard to act on
downstream regardless of statistical separation.

## Secondary (recorded, NON-gating — brief §4)

Directional/mean separation is weak-to-absent: 20d off.mean +0.0104 vs on.mean +0.0100; hit-rate off
0.644 vs on 0.682 (risk-off slightly *lower*, the wrong direction for a tradable edge). A null direction
does not falsify H; a clean directional finding in a framework this well-known would itself warrant
heightened overfitting suspicion (brief §4).

## De-coupling (preregistration §7 — binding)

Even a RESOLVED here would establish only an **index-level (SPY)** VRP effect and would **not** authorize
a Q2 book-level overlay. The verdict is FALSIFIED, so the case against a **free-composite portfolio
risk-scaling overlay** is now closed from **both** directions:
- **book-level** (`regime_signal_research_2026-06-25` + extension): 14 free candidates, N=33, NULL;
- **index-level, high power** (this run): composite second-moment content is repackaged trailing vol.

The standing remaining levers are unchanged (regime_signal_battery closure): **PAID** high-resolution
dealer-gamma or **more accrued co-drawdown episodes**; quarterly regime trigger **2026-08-08**. No
overlay built; no `dd_protection`/allocation/lock change (research/`lab` only). Lock unchanged
(99.83/0.17/4.37).

## Limitations (logged)

1. **2008 GFC is in warmup** (double point-in-time warmup: z then tercile → states emit 2009-04). The
   analysis window is 2009–2026; it includes 2011/2015/2018/COVID/2022 but not the GFC.
2. **Credit axis = HYG/LQD proxy** (2007→); the real ICE HY-OAS is free-capped at ~3y (pre-2023 needs
   paid ICE/ALFRED). Credit history is the binding common-sample constraint.
3. **K=3, SPY-as-forward-asset, equal-weight primary** are pre-registered; not re-tuned post-hoc.

## Reproduce

```bash
cd lab/analysis/regime_cond_2026-06-30
python panel.py --selftest && python panel.py   # composite + states (frozen at prereg commit)
python conditional.py                            # raw + residual conditional tables (the §2.6 null)
python robustness.py                             # placebo, block-bootstrap CIs, jackknife, subperiod, WY multiplicity
```
Artifacts: `panel.csv`, `coverage.json`, `conditional_results.json`, `robustness_results.json`.
