# Class-S candidate #2 — G0–G8 scoring RESULTS

**Status:** `FALSIFIED — all-four-fail`
**Date:** 2026-07-16
**Engine posture:** 10,000 sims × seeds 42/123/2026; horizon 1500; inactivity off;
`dd_protection` OFF; tiers via `firm_kwargs` (never module constants);
headline bust = `preflight.summarize_outcomes` (daily+static+trailing); Part A gated on
**Run-2** where consistency exists. **FXIFY is retired as a live firm**; config key
`ACTIVE_FIRM="FXIFY"` left untouched as the historical MC-anchor fixture.
**Exit code:** `0` (isolated worktree full run; ~15 min wall).
**H-C2 framing:** program §4 falsifier already discharged by candidate #1 — this result
closes H-C2 only; it does **not** demote the prop program and does **not** re-arm ADR §4
early-fail authorization.

## Citations (gate §10 hook 6 / candidate §10 hook 6)

- Candidate pre-reg: [`docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-2-prereg.md`](lab/archive/../../docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-2-prereg.md)
- Frozen gate: [`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](lab/archive/../../docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md)
- Driver: [`run_class_s_c2_scoring.py`](run_class_s_c2_scoring.py)
- Machine report: [`candidate2_report.json`](candidate2_report.json) · log [`full_run.log`](full_run.log)
- §3 calibration (NOT re-run): candidate #1 RESULTS — 3-leg full-Aegis @ 1.50% **0/4** clear (Tradeify 17.88%)

## §6 verdict (mechanical)

| Clause | Result |
|---|---|
| Candidate #2 Part A on ≥2 frozen tiers incl. ≥1 `trailing_locking` | **NO** — 0/4 tiers clear |
| `discharges_falsifier` (this candidate's Part-A pattern) | **False** |
| Candidate §6 disposition | **`FALSIFIED — all-four-fail`** — candidate closes; program §4 stays discharged by #1; early-fail clause does not re-arm |
| Regime-robustness rider (gate §7(7)) | **Not owed** — only required on RESOLVED |

## Candidate #2 (S1 3-leg MYM+MNQ+6J, Aegis @ 0.75%) — Run-2 headlines

| Tier | F2 label | Gated on | Headline bust | P(pass) | Part A |
|---|---|---|---|---|---|
| Bulenox_100K | optimistic-lower-bound | run1_degenerate | **7.38%** | 92.62% | **FAIL** |
| Tradeify_Select_100K | — | run2 | **5.69%** | 94.31% | **FAIL** |
| MFFU_Rapid_100K | — | run2 | **5.69%** | 94.31% | **FAIL** |
| BluSky_Premium_100K | optimistic-lower-bound | run2 | **8.76%** | 91.24% | **FAIL** |

- **G1:** `R_deploy=703` (267 MYM + 284 MNQ + 152 6J); overnight holds **0%** all three legs; `DEPLOYABLE-DEFAULT-ENVELOPE: YES`
- **1R pins (asserted):** striker $2,535.61 (n=8) scale 0.5521 · nas $5,899.32 (n=19) scale 0.1254 · aegis $2,912.96 (n=11) scale 0.5149 — no FALLBACK / no thin cohort
- **G6:** STANDALONE · **G7 funded ≤1%:** 0/4 (diagnostic)
- **Panels:** `…15d8b.csv` / `…beabf.csv` / `…ae744.csv` (sha256 match); window 2020-01-06 → 2026-07-01 (1693 bdays)
- **vs prior:** bustcut 2b 50K was 2.02%; frozen 100K Run-2 Tradeify/MFFU **5.69%** (above 3.0% ceiling; worse than the coarse ×1.71 ≈3.45% extrapolation)
- **vs §3 calibration:** full-Aegis 1.50% was 17.88% Tradeify — halving Aegis weight cuts bust ~3× but **still fails** Part A on this panel family

## Detail

H-C2 **falsified**. No Aegis-inclusive book examined on this panel family (0.75% or 1.50%) clears the frozen $100K×4 Part A ceiling. Candidate closes per §6; a lower Aegis weight would need a **fresh** pre-registration (forbidden move §5). Provenance caveat on ae744 BEPAD-TEST inputs remains standing and unresolved.
