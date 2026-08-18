**Theme:** _inbox
**Status:** ACTIVE — NULL: daily range-state (top-quintile TR) persistence on GC train era; 3 of 4 limbs pass, CI lower bound is the sole failing limb (near-miss, 4.55pp under threshold)
# `H-RANGESTATE-GC-1` (S1a) — RESULTS: near-miss NULL on daily range-state persistence, GC train era

**Date:** 2026-08-18 · **Verdict: `NULL`** (per the frozen §3 gate — limb `ci_lb` failed;
`n_floor`, `halves`, `placebo` all passed)
**Pre-registration:** [`PREREG_S1A.md`](PREREG_S1A.md), frozen before compute, corrected via
adversarial review before the trusted run (§8 there; workflow `wf_7ad6ac61-126`).
**Spend:** $0.00 (confirmed at pull) · K=1 (disclosed, one frozen object) · no manifest.
**Panel:** `GC.v.0` continuous, `ohlcv-1d`, 2010-06-07 → 2018-12-31 (train era; `MGC.v.0`
2019+ stays unread — reserved for a lane confirm if this family signals elsewhere).
**Runner:** [`run_s1a.py`](run_s1a.py) · full JSON: [`s1a_results.json`](s1a_results.json).

## 1. Headline

Object: `bias_d = 1{TR_d ≥ P80(trailing 60d, strictly prior)}`; `y_{d+1} = 1{TR_{d+1} >
P50(trailing 60d through today)}`. Verdict cell = `P(y_{d+1}=1 | bias_d=1)`.

| | value |
|---|---|
| population scored days | 2,116 |
| conditional (bias=1) n | 451 (21.3% share — inside the frozen [0.15, 0.25] prediction band) |
| unconditional `P(y=1)` | 0.4778 (inside the frozen [0.46, 0.54] prediction band) |
| **conditional `gateHit`** | **0.5299** |
| block-bootstrap 95% CI (60-day circular) | **[0.4545, 0.6040]** — lower bound fails |
| halves | (0.5511, 0.5088) — both > 0.50, **passes** |
| placebo (60-day block-permute) mean / p95 / p | 0.4747 / 0.5100 / **0.0095** — observed beats p95, **passes** |
| limbs | `n_floor` ✓ `ci_lb` ✗ `halves` ✓ `placebo` ✓ |

**Three of four limbs pass, including the primary placebo limb** (`p = 0.0095` — the observed
conditional rate beats 99.05% of 2,000 block-shuffled draws). Per the frozen §3 gate this is
still `NULL`: all four limbs are required, and `ci_lb` — the block-bootstrap lower bound sitting
at 0.4545, **4.55 percentage points under the 0.50 threshold** — is the one that fails. This is
the mirror image of `H-DSTRUCT-MNQ-1`'s failure shape (which failed on structure and needed the
placebo to catch it); here the structure and the placebo both clear, and the estimation-precision
limb is what's missing.

## 2. Per-year decomposition (conditional cell, disclosure)

```
2010 0.6071   2011 0.7377   2012 0.4348   2013 0.5424   2014 0.4038
2015 0.5208   2016 0.5345   2017 0.4773   2018 0.4909
```

No monotonic trend; 2011 (crisis-era gold spike/reversal) is the strongest year, 2014 the
weakest. Not a pre-registered test — disclosure only, consistent with §6's forbidden-moves bar
on reading anything into a post-hoc year slice.

## 3. Why this is a defensible NULL, not an arbitrary one

The frozen four-limb bar (imported from `H-DSTRUCT-MNQ-1`) is deliberately strict — a construct
that clears structure (CI, halves) but not the placebo is the Q-WLEGB-1 failure mode this
template exists to catch; a construct that clears the placebo but not a properly-calibrated CI
is the opposite failure mode, and just as real: **the placebo answers "does temporal order
matter, given this many bias=1 draws," while the CI answers "how precisely is the conditional
rate itself pinned down."** A p=0.0095 placebo result on n=451 can still carry genuine sampling
uncertainty wide enough to include 0.50 — that is exactly what happened here, and the two limbs
are not redundant. Requiring both is the correct design, not double-counting.

**This was verified honestly, not tuned to this answer.** Adversarial review caught that the
first-draft CI used a 10-day block (copied unexamined from the DSTRUCT template) while the
prereg's own text argued for 60-day blocks; the fix widens the CI and moves the lower bound
*away* from 0.50, not toward it (0.4676→0.4545 after both corrections — see `PREREG_S1A.md` §3
limb 2). A p-hacked screen would have kept the narrower, more favorable interval; this one
doesn't.

## 4. Disposition

**`NULL` → does not close the daily-geometry class.** Per the Step-0 slate's own §4 falsifier,
the class needs **all GO'd screens** (minimum S1a+S1b+S2) to NULL before it's exhausted — S1a
alone is one instrument/window draw of one row. The near-miss shape (placebo p=0.0095, CI
lower bound only 4.55pp short) is disclosed as a **live prior for S1b (MCL)**: the mechanism's
evidence-robustness grounding (§2, volatility clustering) predicts it should generalize across
instruments if real, so S1b is not a blind re-test — it's the first opportunity to see whether
this near-miss replicates or was this instrument/window's own sampling noise.
**Re-proposal bar (for a GC-specific re-open):** per §6, no second quantile cut, window length,
or horizon on this exact instrument/window — a re-open needs either a longer/different
train-era panel (not this one, not a shortened one) or a named mechanism argument for why P80/60d
specifically undersells the true effect.
**Routing:** proceeds to S1b (MCL) per the slate's queue order (§3 there), GO owed separately.

## 5. Scope limits

GC (parent) train era only; `MGC.v.0` 2019+ untouched by design. One frozen `(P80, 60d, 1-day-
ahead)` object — no sweep. 13 of 2,177 valid TR observations (~0.6%) are gap-adjacent (disclosed
in `PREREG_S1A.md` §7, not excluded — bounded materiality, well under both n-floors). Measurement-
only; no outcome here promotes or blocks the S1b/S2/S3 rows independently.
