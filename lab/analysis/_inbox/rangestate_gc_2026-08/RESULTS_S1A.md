**Theme:** _inbox
**Status:** ACTIVE — NULL, now official under the corrected battery (driving L2+L4; obs at 8.4th pct of GC's own linear-ACF band — near-miss DISSOLVED, CASE A). See the RE-MEASUREMENT addendum at the end of this file.
# `H-RANGESTATE-GC-1` (S1a) — RESULTS: NULL on daily range-state persistence, GC train era

> **⚠ CORRECTION 2026-08-18 — read before citing this file's §3.** The sibling screen
> [`H-RANGESTATE-CL-1` (S1b)](../rangestate_mcl_2026-08/RESULTS_S1B.md) triggered an adversarial
> review that found the **placebo limb both screens share is misspecified** — it does not
> control for ordinary True-Range autocorrelation, and 20 independent zero-mechanism AR(1)
> surrogates cleared the identical battery at a *higher* rate than either real dataset. Full
> finding: [audit note](../../../docs/notes/audits/2026-08-18-block-shuffle-placebo-does-not-control-for-tr-autocorrelation.md).
> **Consequence for this file: the bottom-line verdict is unchanged** (`NULL` — this screen
> already failed the `ci_lb` limb independent of the placebo defect), **but §3's claim that the
> placebo pass is "independent corroboration" against an arbitrary NULL is retracted.** §3 is
> preserved below as originally authored, for audit-trail honesty, followed by a correction.
> Read §3 with that retraction in mind rather than as originally intended.

**Date:** 2026-08-18 · **Verdict: `NULL`** (per the frozen §3 gate — limb `ci_lb` failed;
`n_floor`, `halves`, `placebo` all passed **— `placebo` pass is NOT independent corroboration,
see correction banner above**)
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

**Retraction (added 2026-08-18, does not alter §3's text above):** the paragraph above treats
the placebo's p=0.0095 pass as evidence the result "isn't arbitrary." That reasoning assumed the
placebo null correctly isolates the claimed 1-day-ahead persistence effect from ordinary
True-Range autocorrelation. **It does not** — see the correction banner at the top of this file
and the linked audit note. GC's own True-Range series is autocorrelated the same way CL's is; a
zero-mechanism AR(1) surrogate matched to GC's own lag-1 ACF would very likely also clear this
placebo (not separately re-tested here, since S1a's bottom-line verdict doesn't depend on it —
`ci_lb` already fails on its own). **Read this file's placebo row as "cleared an invalid null,"
not as supporting evidence.** The CI-limb failure remains the operative, trustworthy reason this
screen is `NULL`.

## 4. Disposition

**`NULL` → does not close the daily-geometry class.** Per the Step-0 slate's own §4 falsifier,
the class needs **all GO'd screens** to NULL before it's exhausted — S1a alone is one
instrument/window draw of one row.
**Re-proposal bar (for a GC-specific re-open):** per §6, no second quantile cut, window length,
or horizon on this exact instrument/window — a re-open needs either a longer/different
train-era panel (not this one, not a shortened one) or a named mechanism argument for why P80/60d
specifically undersells the true effect. **Any re-open additionally needs the corrected
autocorrelation-matched null from the audit note above** — the frozen battery as currently
built cannot be trusted to gate this claim family.

**⚠ "Live prior for S1b" (originally below) — RETRACTED 2026-08-18.** S1b ran and returned a
raw `SIGNAL` reading that the same adversarial review found not-confirmed for the identical
reason as this correction: [`RESULTS_S1B.md`](../rangestate_mcl_2026-08/RESULTS_S1B.md). S1b's
near-miss-shaped placebo pass here did not predict anything real about S1b, because neither
screen's placebo tests what it was assumed to test. S2/S3 (Step-0 slate) are **paused** pending
the structural fix named in the audit note.

## 5. Scope limits

GC (parent) train era only; `MGC.v.0` 2019+ untouched by design. One frozen `(P80, 60d, 1-day-
ahead)` object — no sweep. 13 of 2,177 valid TR observations (~0.6%) are gap-adjacent (disclosed
in `PREREG_S1A.md` §7, not excluded — bounded materiality, well under both n-floors). Measurement-
only; no outcome here promotes or blocks the S1b/S2/S3 rows independently.

---

## 6. RE-MEASUREMENT addendum (2026-08-18, official corrected-null re-score — CASE A)

Under the [frozen class battery](../../../docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md)
(IAAFT normal-scores null, M=1000, official seeds; ADDENDUM-1 governs wording):

| | old battery (this file, §1) | corrected battery (official) |
|---|---|---|
| placebo / attribution | block-shuffle p=0.0095 "pass" — **retired, invalid null** | IAAFT band: obs at **8.4th pct**, p_upper 0.9161, p_lower 0.0849 → attribution GENERIC |
| CI limb (L2) | FAIL (0.4545) | FAIL (carried verbatim) |
| by-year (L4, new) | not a limb | **FAIL** — 5 of 9 years > 0.50, required 7 |
| verdict | NULL ("near-miss, 3 of 4 limbs") | **NULL (driving: L2, L4)** — near-miss framing **retracted** |

**CASE A realized:** 0.5299 sits below the center of what GC's own marginal + linear
autocorrelation produces with zero mechanism (band mean 0.5548). The near-miss was never near
anything. No SUB-LINEAR flag (p_lower 0.0849); broad-BORDERLINE vs the 0.07 line disclosed
per A14, wording-layer only; per A13, the real conditional-minus-unconditional lift sits at the
**41st percentile** of the surrogate lift band (dead center) — the low raw placement is
predominantly a base-rate artifact of the band's known upward bias (~+0.02) under this panel's
phase-locked vol decline, not anti-clustering. Full record:
[`RESULTS_CORRECTED.md`](../rangestate_corrected_2026-08/RESULTS_CORRECTED.md).
**MGC ledger cell:** re-typed `DEAD` (measured NULL under a valid test; re-proposal bar = the
corrected battery + a different construction or longer panel, per §4 above).
