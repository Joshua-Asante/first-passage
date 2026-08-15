# ORB-MNQ-1 Stage-8 realized N_eff RESULTS — the owed completion (legs procured)

**Campaign:** `orb_mnq_intraday_breakout` · **Harness:** [`run_stage8_neff.py`](run_stage8_neff.py). Completes the data-gated item flagged in [`RESULTS_stage8.md`](RESULTS_stage8.md).
**Book legs procured:** the two sha-pinned Class-S candidate #1 CSVs from `core/data/tv_exports/cme/` (main-repo gitignored store) — `Striker_DJ30_v4.5_MYM…15d8b.csv` (sha `9acfa29…` ✓) + `Striker_NAS100_v1…MNQ…beabf.csv` (sha `8884e6d…` ✓). Panel built via the **Class-S scorer's own `build_scaled_panel`** (exact panel of record: $200K-decompound, 1R-pinned n=8/n=19, EXPECTED_1R-guarded). ORB-MNQ daily series is engine-faithful (self-checked against `orb_backtest`). N_eff = production `research_utils.breadth.participation_ratio` on the weekly (Mon-anchored) frame.

---

## Verdict — the realized data **corrects my earlier structural claim**: ORB-MNQ is a near-independent bet on the correlation axis (NOT instrument-concentrating); the concentration is real only on the regime and risk-mass axes

| Metric (weekly, overlap 2020-01-06 → 2026-06-30, 339 weeks) | 2-leg book | + ORB-MNQ | Δ |
|---|---|---|---|
| **Dependence N_eff** (PR corr, scale-invariant — headline) | 1.9948 | **2.9502** | **+0.955** (max 3.0) |
| Risk N_eff (PR cov, ORB @0.37%) | 1.9593 | 1.9628 | +0.003 |
| ENB (entropy corroboration) | 1.9974 | 2.9747 | +0.977 |

**Realized weekly correlations:**
- ORB vs **MNQ_striker (same instrument!)**: **+0.1506**
- ORB vs MYM_striker: +0.0018
- ORB vs composite (MYM+MNQ): +0.1177

### Correction I owe (the empirical result overturned my prior reasoning)

My [`RESULTS_stage8.md`](RESULTS_stage8.md) structural verdict said ORB-MNQ "CONCENTRATES the book
… instrument (2nd Nasdaq/MNQ leg)." **On the measured correlation axis that is wrong.** The realized
weekly correlation between ORB-MNQ and the *same-instrument* MNQ-Striker leg is only **+0.15**, and
adding ORB lifts the dependence N_eff from ~2 to **2.95** — a nearly fully-independent third bet. This
is the standing **"instrument-level correlation ≠ strategy-level correlation" belt finding**
(NAS100/DJ30 anchor) confirmed on real returns: same instrument (MNQ), decorrelated *strategy*
(intraday cash-open breakout, both-sides vs Mon/Tue swing/pyramid long-only). The structural
"instrument-concentration" hypothesis was exactly the thing the belt finding warns against, and the
data sided with the belt finding, not the hypothesis.

### What the concentration IS (two real axes, both survive the realized computation)

1. **Regime / tail axis (stands — separate from average correlation).** The +0.15 correlation is an
   *average over 2020–2026*, dominated by the benign post-2020 regime. It does **not** capture tail
   co-movement in the chop that binds the book: ORB-MNQ is dead in **2020** (−0.029, the book's worst
   year; book H1 2020-23 busts ~4.37%) and its edge is trend-regime-concentrated (N2). So ORB and the
   book are **decorrelated on average yet regime-common-mode in the stress window** — a low mean
   correlation and a shared chop-fragility are not contradictory. This is the dominant standing risk.
2. **Risk-mass axis (new, from the cov N_eff).** ORB-MNQ is a **high-variance** leg: at 0.37% its
   weekly $ std is **~1761 vs 814 (MYM) / 932 (MNQ)** — already ~2× each book leg. So the risk N_eff
   barely moves at 0.37% (1.96→1.96) and *falls* if ORB is sized up (0.70%→1.28, 1.50%→1.06): ORB
   would **dominate the risk budget** rather than balance it. Adding an uncorrelated-but-large-variance
   leg adds a new risk direction but concentrates risk mass in itself. Sizing must be conservative.

---

## Reading

- **Correlation/direction breadth: ORB-MNQ ADDS it** — near-independent (dependence N_eff +0.96),
  which materially *improves* the earlier read. It is not the redundant Nasdaq leg the structural
  argument feared.
- **Risk-balance + regime breadth: ORB-MNQ does NOT add** — it is high-variance (risk-dominant if
  sized up) and regime-common-mode with the book's binding chop fragility.
- **Net for admission:** the breadth caveat is **revised, not removed** — from "instrument-concentrating"
  (wrong) to "adds correlation breadth but is regime-common-mode + high-variance/risk-dominant." The
  CANDIDATE @1.00× admission stands; the caveat is now more precise (and the low measured correlation is
  a genuine point in ORB's favor as a book member, tempered by the regime + variance facts).

## Faithfulness notes

- Book panel = the **exact panel of record** (Class-S `build_scaled_panel`, sha-pinned CSVs, EXPECTED_1R
  guards passed: MYM 1R $2535.61/n8/scale0.5521, MNQ $5899.32/n19/scale0.1254).
- ORB daily-dated series **self-checked** against `orb_backtest` (identical R multiset; assertion in-harness).
- Dependence N_eff is **scale-invariant** (no sizing assumption); risk N_eff states ORB@0.37% and reports
  the full sizing sweep so the risk conclusion isn't a hidden single-allocation artifact.
- Overlap window only (2020-01-06→2026-06-30); zero-fill confined to the shared active window (no fake
  co-silence — breadth.py design §6 discipline).
- No vendor bytes copied into the repo or committed — legs read from the main-repo gitignored store.

## Disposition

- **Stage-8 realized N_eff: COMPLETE.** The owed data-procurement item is discharged. Dependence N_eff
  1.99→2.95 (adds a near-independent bet); regime-common-mode + high-variance concentration are the real,
  narrower caveats. Earlier structural "instrument-concentration" verdict **corrected**.
- Manifest may now close as a fully-evaluated survivor (all stages 2–8 complete); left open pending an
  operator note if a live venue is designated (decay-monitor calibration owed at that point).

Reproduce:

```bash
PYTHONPATH="lab;core" .venv-research/Scripts/python.exe lab/analysis/orb_mnq_2026-07/run_stage8_neff.py
```
