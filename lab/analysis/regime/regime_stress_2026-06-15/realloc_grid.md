# Guardian-removal + reallocation grid (Q-REGIME-STRESS-1 follow-up)

**LoR:** OUTER (INQHIORI). Exploratory portfolio-construction analysis. **Does not modify locked
config — informs a future regime-adaptive-sizing Pre-Q/ADR.** Locked files untouched
(`LOCKED_FILES_CLEAN`). 2026-06-15.

**Question.** Guardian is 57.3% of hostile-regime busts with ~zero hostile edge (PF 1.01). Does
removing it improve regime-robustness — and does it beat an *equivalent uniform de-risk*? Where
should the freed 0.34% budget go?

**Method.** Same harness as Q-REGIME-STRESS-1: uploaded 2020-start CSVs, fixed full-panel
implied-1R (allocation-invariant), production 5-day week-block bootstrap (verbatim), C2
dd_protection, 10k×3 seeds. Judged on the **HOSTILE (2020-22)** cell (full-panel masks the split).
Lock gates = bust < 1% AND p99 DD < 5%.

## Results

| config | Σrisk | **HOST** pass / bust / p99 / med | NORM pass / bust / p99 / med | FULL 2020-26 pass / bust / p99 | regime gap |
|---|---:|---|---|---|---:|
| **REF** 4-strat locked | 2.91% | 65.14% / **33.18%** / 8.99% / 128 | 99.65 / 0.35 / 4.79 / 20 | 98.60 / **1.40** / **5.40** | 34.5pp |
| **U257** uniform k=0.883 | 2.57% | 66.86% / **29.85%** / 8.93% / 172 | 99.80 / 0.20 / 4.43 / 21 | 99.28 / 0.72 / 5.00 | 32.9pp |
| **D1** drop Guardian | 2.57% | 83.34% / **7.24%** / 7.34% / 297 | 99.96 / 0.04 / 3.86 / 31 | 99.90 / 0.10 / 4.22 | 16.6pp |
| **D3** dropG → Strikers (A held) | 2.91% | **87.71%** / **6.75%** / 7.33% / 256 | 99.90 / 0.10 / 4.16 / 27 | 99.80 / 0.20 / 4.48 | **12.2pp** |
| **D2** dropG → prop-3 (A→1.70%⚠) | 2.91% | 83.45% / 10.07% / 7.74% / 256 | 99.87 / 0.13 / 4.26 / 27 | 99.78 / 0.22 / 4.60 | 16.4pp |

Hostile bust attribution: REF G57/A30/DJ8/N5 → U257 G58/A28/DJ8/N5 → **D1 A71/DJ18/N11** → **D3 A64/DJ23/N13** → D2 A69/DJ20/N11.

## Findings

1. **Removing Guardian is the dominant hostile lever — and it is *structural*, not just de-risking.**
   The clean control: **D1 (drop Guardian, Σ2.57%) vs U257 (uniform de-risk to the *same* Σ2.57%)** —
   hostile bust **7.24% vs 29.85%**, a **~4× difference at identical total risk**. Uniform de-risk barely
   moves the hostile needle (33%→30%); removing the zero-hostile-edge / full-drawdown leg cuts it to 7%.
   This is exactly the mechanism uniform de-risk *cannot* target, and it refutes the "targeting buys
   little" prior **for this specific structural move** (PR #157's finding was about *proportional*
   reshaping; removing a harvest-only leg is categorically different).

2. **Reallocate the freed budget to the regime-spanning Strikers, not Aegis.** D3 (→Strikers, Aegis
   held at its 1.5% ceiling) is the best static config: hostile **87.71% / 6.75%**, smallest regime gap
   (12.2pp), and it **clears the gates in both NORMAL and FULL** while *beating REF in every regime*.
   D2 (proportional, feeds Aegis) is worse (hostile bust 10.07%) **and** breaches the documented Aegis
   1.5% ceiling. The Strikers have hostile edge (PF ~2.0) so the budget generates hostile return; Aegis
   is harvest-only (PF 1.06) so feeding it adds drawdown without return.

3. **It is a large improvement, not a fix.** Even D3's hostile cell still **breaches both lock gates**
   (6.75% bust > 1%, 7.33% p99 > 5%). Static reallocation can't fully clear the hard regime — consistent
   with PR #157. Guardian removal gets *far* closer than uniform de-risk, but doesn't reach regime-robust.

4. **After Guardian, Aegis is the next hostile liability** (attribution flips to Aegis 64–71%). Both are
   harvest-only legs; the two Strikers are the regime-spanning core.

5. **The honest full-history headline flips with Guardian out.** On the 2020-26 basis (PR #157's concern),
   REF *breaches* (98.60 / 1.40 / 5.40) but D1/D3 *restore* the gates (D3: 99.80 / 0.20 / 4.48). Uniform
   de-risk to 2.57% sits right on the p99=5.00% edge.

6. **The cost is pass-SPEED and forfeiting the good-regime engine, not pass-probability.** Removing
   Guardian (normal mean-R 3.21, by far the largest earner) slows median pass-time (normal 20→27,
   hostile 128→256) and gives up the dominant trending-regime return — pass *rate* stays high because the
   survivors still reach +5%, just slower.

## Where the data points

The result **sharpens PR #157's "regime-adaptive sizing is the only structural fix"** into a concrete
shape: the legs to **down-weight when a chop/hostile regime is detected** are the **harvest-only** ones
(Guardian first, then Aegis); the legs to **keep** are the regime-spanning **Strikers**. That is
strictly better than permanent removal — it forfeits Guardian's trending-regime return only *while* the
hostile regime is active. **D3 is the data-indicated best *static* config**, but the real answer is
**conditional** (regime-adaptive) reallocation, which a future Pre-Q should design and gate.

## Caveats / what this is NOT

- **Not a relock recommendation.** Locked config is HELD (2026-06-07 ADR). This is analysis that informs
  the future regime-adaptive Pre-Q. No `core/` change.
- **D3/D2 lean HARD on the off-feed Strikers** (DJ30=Vantage 0.92%, NAS100=IC Markets 0.49%). The
  improvement is concentrated in legs on non-canonical feeds, so trade-selection drift matters *more*
  here than in Q-REGIME-STRESS-1. Mitigant: calib-A (same data windowed to 2022) reproduced the anchor
  within tolerance; but any lock candidate must re-validate the Strikers on Pepperstone.
- **Compounding understates hostile risk** (early/low-equity → small $). True (decompounded) hostile
  busts are worse for every config — the *ranking* is what's robust, not the absolute levels.
- **Single-episode hostile bucket** (2020-22; Aegis n=43).
- **Formal gate not yet run.** No candidate here has been through the mandatory regime-robustness gate
  (half-panel + 6-mo block bootstrap, `docs/methodology/regime_robustness_gate.md`). The bucket screen
  suggests D3 is far more regime-robust than the PR #157 uniform candidates that *failed* that gate, but
  that must be confirmed before D3 (or a regime-adaptive policy built on it) becomes a lock candidate.

**Artifacts (gitignored):** `reports/regime_stress/realloc_grid.py` + `realloc_grid.json`.
