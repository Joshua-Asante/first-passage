# Q-REGIME-OOS-1 · Phase 1 — gold-gate face-validity (DESCRIPTIVE, UNSCORED)

**Date:** 2026-06-21 · **Status:** PARTIAL (descriptive) — does **NOT** falsify T1; scored T1 pending the Guardian pre-2020 trade export.
**Firewall:** pre-registration committed **`40feb9c`** BEFORE this run. FROZEN gate `ker`/`tsmom`/`gate_label`/`THR_KER126` reused **verbatim** from `ops/regime_gate/gold_gate_shadow.py` (no refit). Driver: `phase1_gold_facevalidity.py`.

## What ran
Frozen gate `DEPLOY iff gold KER_126 ≥ 0.12 AND TSMOM_252 > 0` on **canonical TV-Pepperstone** gold daily close, 2012-07 → 2026-06 (4311 daily closes; gate valid from **2013-06-02** after the 252-day lookback).

## Result — by-year DEPLOY fraction
`2013-2015: 0% DEPLOY (100% WAIT)` — the gold bear · `2016: 30%` (H1 rally, then collapses post-election) · `2017: 0%` · `2018: 0%` · `2019: 44%` (breakout) · `2020: 38%` · `2021: 2%` · `2022: 11%` (in-sample chop) · `2023: 27%` · `2024: 70%` · `2025: 81%` (the bull) · `2026: 42%`.

## Verification — 3-agent adversarial (workflow `wf_664671b1`)
- **compute-audit: CLEAN** — look-ahead clean (features strictly trailing), resample faithful to production `daily_close`, production functions reused verbatim, NA/lookback correct, output reproduced.
- **data-consistency: CONSISTENT** — by-year calls match realized gold history (independently re-derived); identical on the OANDA-staging *and* canonical TV-Pepperstone feeds.
- **interpretation-skeptic** — caught a rationalization (below).

## Load-bearing finding: a LABEL mis-specification, not a gate failure
The pre-reg §5 expected **2017 trend → DEPLOY**; the gate returned **WAIT**. The skeptic ruled the initial "designed cheap-error" framing a **post-hoc rationalization** (it re-labels a pre-registered miss). Honest read: at 2017-06-30 the gate's own FROZEN inputs were **KER_126 = 0.038** / **TSMOM_252 = −8.0%** (gold *down* YoY — the trailing-252d window still spanned the Nov-Dec 2016 drop; gold rose *intra*-2017 but not year-over-year). WAIT is the only correct GOLD call. The "2017 benign" label conflated the **equity** 2017 melt-up with the **gold** regime the gold-keyed gate sees. **Error in the label, not the gate.**

The dangerous error (false-DEPLOY-into-hostile) **never fired**: 2013-15 bear and 2021-22 chop are correctly WAIT; 2018-Q4 (documented gold blind spot) stayed WAIT on gold's own weak momentum. 3 of 4 episode cells as-expected.

## Disposition — option B (operator-approved 2026-06-21)
Face-validity **demoted to descriptive corroboration**; `RESOLVED-T1` rests on **AUC ≥ 0.70** vs the forward-start portfolio label — **bar unmoved**. Recorded via the append-only CORRECTION in the pre-registration (original criteria preserved).

## Lesson candidate
**Face-validity episode labels for a single-asset-keyed gate must be specified on THAT asset's own regime, not a cross-asset/portfolio framing.**

## Next (scored T1)
Guardian XAUUSD pre-2020 trade export (re-run the locked Guardian Pine in TV, start ~2012, export List-of-Trades) → forward-start label → AUC of the frozen features vs that label, back through the 2013 crash.
