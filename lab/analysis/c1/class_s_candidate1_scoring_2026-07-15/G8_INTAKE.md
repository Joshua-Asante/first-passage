# Class-S candidate #1 — G8 intake note

> **⛔ SUPERSEDED 2026-07-22 — the mechanical Part A discharge asserted below is WITHDRAWN.**
> The two `trailing_locking` tiers it rested on were scored with an eval-phase
> drawdown-locking cushion neither firm applies (see
> [`../tradeify_eval_lock_correction_2026-07-22/RESULTS.md`](../tradeify_eval_lock_correction_2026-07-22/RESULTS.md)).
> Corrected, **zero** tiers clear Part A and `discharges_falsifier = False`; the
> prop-portfolio §4 falsifier is **undischarged** (hard date 2026-11-08) —
> [`docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](../../../docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md).
> The **WATCH-1 0.50× ratification** recorded below is a *separate* gate and is not
> withdrawn — but its underlying figures share the defect and are **unmeasured** under
> corrected geometry (RESULTS §5). Retained unedited as the historical record.

**Date:** 2026-07-15 (annotated after local full rider 2026-07-16)
**Mechanical Part A:** `RESOLVED (DISCHARGED)` — **SUPERSEDED 2026-07-22, see banner above**.
  See [`RESULTS.md`](RESULTS.md) (Tradeify 2.65% + MFFU 2.64% Part A PASS).

## Regime-robustness rider (gate §7(7))

| Item | State |
|---|---|
| Driver | [`run_class_s_c1_regime_gate.py`](run_class_s_c1_regime_gate.py) |
| Report | [`REGIME_GATE.md`](REGIME_GATE.md) · [`regime_gate_report.json`](regime_gate_report.json) |
| Floor | Part A: bust ≤ 3.0% + P(pass) ≥ 50% |
| Geometry | Run-2 on `Tradeify_Select_100K` + `MFFU_Rapid_100K` |
| Full run | **`COMPLETE` — GATE FAIL (regime-fragile)** |
| Local log | [`regime_gate_full_run.log`](regime_gate_full_run.log) (~2.6h wall, joblib `-1`) |

## Verdict (G8 intake) — `SUPERSEDED 2026-07-17`, see Ratified disposition below

Admit to lifecycle **CANDIDATE @ 1.00×** (book-level; no `core/lifecycle.py` write
on the four locked CFD legs) **with standing regime-fragile caveat**.

- Full-panel Part A still clears both discharge tiers (Tradeify 2.65% / MFFU 2.64%).
- Part B: H1 (2020–23) fails both tiers (~4.37% / 4.36% bust); H2 (2023–26) passes (~1.70%).
- Part A bootstrap n=100: both tiers FAIL on bust 95th (~10.37% / 10.33% > 3.0%).
- Per candidate §6: this does **not** overturn mechanical Part A DISCHARGED.

This 1.00× measurement stands as the historical record of why the haircut below was tested;
the intake disposition it recommended (CANDIDATE @ 1.00× with a standing caveat) is superseded.

## Ratified disposition (2026-07-17 — supersedes the 1.00× standing caveat above)

Operator ratified (chat, 2026-07-17: "ratify c1 as CANDIDATE deployable at WATCH-1") the
pre-registered lifecycle-haircut regime re-MC finding —
[`../class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md`](../class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md)
(pre-reg [`2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md`](../../../docs/briefs/pre-registration/2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md),
signed §9, full n=100/10k run completed 2026-07-17): the **WATCH-1 (0.50×)** book-level lifecycle
haircut clears the regime-robustness rider on **all four partitions × both discharge tiers**
(H1 bust 4.37%→**0.14%**; bootstrap-95th 10.37%→**0.77%**; full-panel 0.08%; bootstrap pass-5th
95.76%, well clear of the 50% floor — not impractical).

**Ratified intake: lifecycle CANDIDATE, deployable at WATCH-1 (0.50×).** Book-level, per the
pre-reg's own forbidden-moves list — still **no** `core/lifecycle.py` write on the four locked
CFD legs; c1 is a distinct native-futures book (Striker DJ30→MYM + Striker NAS100→MNQ), not a
CFD-leg authorization change.

- **Practicality caveat carried forward:** 0.50× ≈ half risk_pct ⇒ roughly double median
  days-to-pass vs the 1.00× book; pass-rate itself is unaffected (stays ≥95%).
- Mechanical Part A **DISCHARGED** (four-firms ADR §4 falsifier) is untouched by this
  ratification — it was never in question and does not require the regime rider to pass.
- Candidate #2 (S1, 3-leg + Aegis@0.75%, ae744) scored separately 2026-07-16:
  **`FALSIFIED — all-four-fail`** (Tradeify/MFFU 5.69% bust) — dead; does not affect this
  ratification (program §4 was already discharged by candidate #1).

## Still gated

Rail build, account registration, and go-live remain separately gated. Historical
fixture `ACTIVE_FIRM=FXIFY` stays untouched (venue retired).
