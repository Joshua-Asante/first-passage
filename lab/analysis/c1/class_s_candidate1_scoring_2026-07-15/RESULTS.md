**Theme:** c1
**Status:** ACTIVE — G0–G8 scoring for Class-S candidate #1 (locked-book MYM+MNQ)
# Class-S candidate #1 — G0–G8 scoring RESULTS

> ## ⛔ SUPERSEDED 2026-07-22 — Part A / G8 figures below are computed on a DEFECTIVE input
>
> The `Tradeify_Select_*` and `MFFU_Rapid_*` eval rows carried `dd_lock_offset_usd: 100`,
> giving the simulated **evaluation** a drawdown-locking cushion neither firm applies in
> eval (Tradeify verbatim: *"Evaluation accounts do not have drawdown locking"* —
> [article 10495897](https://help.tradeify.co/en/articles/10495897-rules-trailing-max-drawdowns),
> re-verified 2026-07-22). The error is **optimistic**.
>
> Corrected: **Tradeify 2.65% → 4.74%**, **MFFU 2.64% → 4.25%** (Run-2 headline bust).
> Both flip Part A **PASS → FAIL** against the frozen 3.0% ceiling. With Bulenox (3.51%)
> and BluSky (4.44%) already failing, there are **zero Part A clearers** and
> **`discharges_falsifier = False`** — the §4 discharge recorded below is **WITHDRAWN**.
>
> The numbers in this file are **retained unedited as the historical record** of what was
> run on 2026-07-15. Do not cite them as current.
> Measurement: [`../tradeify_eval_lock_correction_2026-07-22/RESULTS.md`](../tradeify_eval_lock_correction_2026-07-22/RESULTS.md) ·
> decision: [`docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](../../../docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md)

> ## ⚠ 2026-08-23 reader-intercept (R1 CLOCK repair) — a SECOND, independent defect on top of the
> ## banner above
>
> The banner above corrects the LOCK defect (Tradeify/MFFU only) and, in doing so, cites
> Bulenox 3.51% / BluSky 4.44% as still-valid ("already failing") — that citation is correct for
> the LOCK question but, like every figure in this file, is **EOD-clock only**: the venue's
> real-time intraday breach is not modeled. Honest-clock re-run: Bulenox 3.51%→**26.77%**, BluSky
> 4.44%→**32.26%** — both remain FAIL either way (no verdict flip), but 3.51%/4.44% are not the
> current honest-clock reference. See
> [`../firm_model_repair_r1_7tier_2026-08-23/RESULTS.md`](../firm_model_repair_r1_7tier_2026-08-23/RESULTS.md).
> Body (including the banner above) unedited.

**Status:** `RESOLVED (DISCHARGED)` — **SUPERSEDED 2026-07-22, see banner above**
**Date:** 2026-07-15
**Engine posture:** 10,000 sims × seeds 42/123/2026; horizon 1500; inactivity off;
`dd_protection` OFF; tiers via `firm_kwargs` (never module constants);
headline bust = `preflight.summarize_outcomes` (daily+static+trailing); Part A gated on
**Run-2** where consistency exists. **FXIFY is retired as a live firm** (venue closed
2026-07-10); the config key `ACTIVE_FIRM="FXIFY"` was left **untouched as the historical
MC-anchor regression fixture only** — it is not a claim that FXIFY is operationally
active (see `core/firm_rules.py` + challenge-era rescope ADR).
**Exit code:** `0` (local full run; ~61 min wall).

## Citations (gate §10 hook 6 / candidate §10 hook 6)

- Candidate pre-reg: [`docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md`](../../../docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md)
- Frozen gate: [`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](../../../docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md)
- Driver: [`run_class_s_c1_scoring.py`](run_class_s_c1_scoring.py)
- Machine reports: [`candidate1_report.json`](candidate1_report.json) · [`calibration_report.json`](calibration_report.json)

## §6 verdict (mechanical)

| Clause | Result |
|---|---|
| Candidate #1 Part A on ≥2 frozen tiers incl. ≥1 `trailing_locking` | **YES** — Tradeify_Select_100K + MFFU_Rapid_100K (both `trailing_locking`) |
| §3 calibration clears 3.0% on ≥2 tiers (ceiling-mis-set / AMBIGUOUS) | **NO** — 0/4 tiers (Tradeify Run-2 bust **17.88%**, matches remc prior 17.70%/17.88% band) |
| `discharges_falsifier` | **True** |
| Candidate §6 disposition | **`RESOLVED (DISCHARGED)`** — four-firms ADR §4 falsifier discharged for this candidate; rail/account/go-live stay separately gated |
| Regime-robustness rider (gate §7(7) / candidate §6) | **COMPLETE — GATE FAIL (regime-fragile)** on both discharge tiers (H1 bust ~4.37%; bootstrap bust 95th ~10.4%). Does **not** overturn Part A DISCHARGED. G8 intake = CANDIDATE @ 1.00× **with standing caveat** — [`REGIME_GATE.md`](REGIME_GATE.md) · [`G8_INTAKE.md`](G8_INTAKE.md) |

## Candidate #1 (S2 2-leg MYM+MNQ) — Run-2 headlines

| Tier | `dd_type` | F2 label | Headline bust | P(pass) | Part A |
|---|---|---|---|---|---|
| Bulenox_100K | trailing | optimistic-lower-bound | **3.51%** | 96.49% | FAIL (>3.0%) |
| Tradeify_Select_100K | trailing_locking | — | **2.65%** | 97.34% | **PASS** |
| MFFU_Rapid_100K | trailing_locking | — | **2.64%** | 97.35% | **PASS** |
| BluSky_Premium_100K | trailing | optimistic-lower-bound | **4.44%** | 95.54% | FAIL (>3.0%) |

- **G1:** `R_deploy=551` (267 MYM + 284 MNQ); 0% overnight holds; `DEPLOYABLE-DEFAULT-ENVELOPE: YES`
- **1R pins (asserted):** striker $2,535.61 (n=8) scale 0.5521 · nas $5,899.32 (n=19) scale 0.1254 — no FALLBACK / no thin cohort
- **G6:** STANDALONE · **G7 funded ≤1%:** 0/4 tiers (diagnostic only)
- **Panels:** `…15d8b.csv` / `…beabf.csv` (sha256 match SHA256SUMS); window 2020-01-06 → 2026-06-30 (1692 bdays)

## §3 Calibration reference (3-leg full-Aegis ae744 @ 1.50%) — Run-2 headlines

Non-candidate; ceiling-discrimination check only.

| Tier | Headline bust | P(pass) | Clears 3.0%? |
|---|---|---|---|
| Bulenox_100K | **21.52%** | 78.48% | no |
| Tradeify_Select_100K | **17.88%** | 82.12% | no |
| MFFU_Rapid_100K | **17.74%** | 82.26% | no |
| BluSky_Premium_100K | **26.68%** | 73.32% | no |

Ceiling **discriminates** as designed (excludes falsified-book quality). Gate AMBIGUOUS clause does **not** fire.

## Detail

Candidate #1 `discharges_falsifier=True`; §3 calibration cleared ≥2 tiers = `False` (tiers=[]). Engine sims/seed = `10000`. Live firm posture: FXIFY **retired**; scoring did not switch the historical `ACTIVE_FIRM` fixture (still `"FXIFY"` for anchor byte-repro — not a live venue).

## Candidate #1 (S2 2-leg MYM+MNQ) — full report JSON

```json
{
  "discharges_falsifier": true,
  "halted_at": null,
  "verdict": "RESOLVED (DISCHARGED)",
  "g1": {
    "r_deploy": 551,
    "expectancy_ratio": 0.16282505910165487,
    "deployable_default_envelope": "YES",
    "halted": false
  },
  "tiers": {
    "Bulenox_100K": {
      "clears_part_a": false,
      "clears_funded": false,
      "gated_on": "run1_degenerate",
      "f2_label": "optimistic-lower-bound",
      "run2": {
        "headline_bust": 0.03513333333333334,
        "pass_rate": 0.9648666666666667
      }
    },
    "Tradeify_Select_100K": {
      "clears_part_a": true,
      "clears_funded": false,
      "gated_on": "run2",
      "f2_label": null,
      "run2": {
        "headline_bust": 0.026466666666666666,
        "pass_rate": 0.9734333333333334
      }
    },
    "MFFU_Rapid_100K": {
      "clears_part_a": true,
      "clears_funded": false,
      "gated_on": "run2",
      "f2_label": null,
      "run2": {
        "headline_bust": 0.026433333333333333,
        "pass_rate": 0.9735333333333333
      }
    },
    "BluSky_Premium_100K": {
      "clears_part_a": false,
      "clears_funded": false,
      "gated_on": "run2",
      "f2_label": "optimistic-lower-bound",
      "run2": {
        "headline_bust": 0.04443333333333333,
        "pass_rate": 0.9554333333333332
      }
    }
  }
}
```

See [`candidate1_report.json`](candidate1_report.json) / [`calibration_report.json`](calibration_report.json) for complete rates, panel meta, and per-leg G2.
