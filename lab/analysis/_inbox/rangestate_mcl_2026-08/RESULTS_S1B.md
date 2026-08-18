**Theme:** _inbox
**Status:** ACTIVE — SIGNAL-GENERIC under the corrected battery (official 2026-08-18): canon-attributed volatility clustering (69th pct of own linear-ACF band), L4 boundary-exact 6/8; NOT a mechanism, does NOT discharge mechanism-owed, no conditioner license. The interim NOT-CONFIRMED (old invalid placebo) is superseded by the RE-MEASUREMENT addendum at the end of this file — ADDENDUM-1 guard-rails bind all wording.
# `H-RANGESTATE-CL-1` (S1b) — RESULTS: NOT-CONFIRMED (placebo misspecified; effect is regime-concentrated and sub-baseline)

**Date:** 2026-08-18 · **Verdict: `NOT-CONFIRMED`** (downgraded from the raw battery's `SIGNAL`
reading — see §2/§3; this is a program-level methodology finding, not an S1b-specific null)
**Pre-registration:** [`PREREG_S1B.md`](PREREG_S1B.md), byte-identical object to
[`PREREG_S1A.md`](../rangestate_gc_2026-08/PREREG_S1A.md) (GC), a second-instrument replication.
**Spend:** $0.00 (confirmed at pull) · K=1 (disclosed) · no manifest.
**Panel:** `CL.v.0` continuous, `ohlcv-1d`, 2010-06-07 → 2018-12-31 (train era; `MCL.v.0` 2019+
stays unread).
**Runner:** [`run_s1b.py`](run_s1b.py) · full JSON: [`s1b_results.json`](s1b_results.json).
**Audit note (read first):** [`2026-08-18-block-shuffle-placebo-does-not-control-for-tr-autocorrelation.md`](../../../docs/notes/audits/2026-08-18-block-shuffle-placebo-does-not-control-for-tr-autocorrelation.md)

---

## 1. The raw battery result — and why it does not stand

Object: `bias_d = 1{TR_d ≥ P80(trailing 60d, strictly prior)}`; `y_{d+1} = 1{TR_{d+1} >
P50(trailing 60d through today)}`. Verdict cell = `P(y_{d+1}=1 | bias_d=1)`.

| | value |
|---|---|
| population scored days | 2,056 |
| conditional (bias=1) n | 425 |
| unconditional `P(y=1)` | 0.4985 |
| **conditional `gateHit`** | **0.6282** |
| block-bootstrap 95% CI (60-day circular) | **[0.5651, 0.6887]** — clears |
| halves | (0.6368, 0.6197) — both > 0.50, clears |
| placebo (60-day block-permute) mean / p95 / p | 0.5069 / 0.5459 / **0.0005** — clears |
| limbs (as frozen) | `n_floor` ✓ `ci_lb` ✓ `halves` ✓ `placebo` ✓ → raw reading `SIGNAL` |

**This raw reading is not trustworthy, and the reason is structural, not a data quirk.**
Adversarial review (workflow `wf_b2b794d6-380`, 4 lenses + synthesis, launched specifically
because a SIGNAL is the highest-stakes outcome type this program can produce) found:

1. **The placebo is misspecified for this claim family.** It permutes which calendar positions
   carry `bias=1` while holding the outcome sequence `y` fixed. `y` is derived from `TR`, and
   `TR` has ordinary, well-documented autocorrelation (measured on this panel: log-TR lag-1
   ρ ≈ 0.4520 — textbook GARCH-type persistence, nothing exotic). **20 independent synthetic
   AR(1) series, calibrated only to that single measured autocorrelation coefficient and
   carrying zero real day-ahead directional mechanism by construction, were run through the
   identical frozen battery. All 20 cleared both the CI and placebo limbs, with a mean
   conditional hit rate of 0.75 (range 0.72–0.80) — higher than CL's real 0.6282.** A closed-form
   AR(1) calculation and a naive in-sample split independently predicted 0.75–0.77. **The real
   result does not exceed what plain autocorrelation predicts; it falls short of it.**
2. **The effect does not survive regime-concentration testing.** Removing the 2011/2014/2016
   crisis-adjacent years together flips the pooled reading: gateHit 0.6282→0.5455, CI lower
   bound drops below 0.50, placebo p weakens 50× (0.0005→0.0265). A clean crisis-vs-calm year
   split is sharper: **the calm-year bucket alone (n=216) is an independent NULL that fails
   both the CI and its own placebo (p=0.0830)** — the only regime cut in the whole analysis
   where the placebo itself fails. It is robust to any *single* year's removal (context, not a
   rescue) — only the crisis *cluster* breaks it.
3. Both findings point at the same root cause: crisis-transition episodes are exactly where
   short-lag TR autocorrelation is most acute, so a null that doesn't control for autocorrelation
   will look strongest precisely where autocorrelation is strongest — which is what happened.

**Independent reimplementation (a separate lens, built from the frozen prereg text alone,
without reading `run_s1b.py`) reproduced every number above to full float precision — there is
no code defect.** The problem is entirely in what the placebo tests, not in the arithmetic.

## 2. Per-year decomposition (conditional cell) — now read as the diagnostic, not disclosure

```
2010 0.4286   2011 0.8182   2012 0.5476   2013 0.4762   2014 0.7121
2015 0.5946   2016 0.7255   2017 0.4681   2018 0.6338
```

Top-3 (2011, 2016, 2014) are exactly the three crisis-adjacent years (2011 Libya/Arab-Spring
supply shock; 2014–2016 WTI price collapse); bottom-3 (2010, 2017, 2013) are calm years. This is
a near-perfect crisis/calm ordering, not scatter around a stable mean — the opposite of what a
genuinely general, always-on mechanism would produce, and the pattern that led the
regime-concentration lens to the drop-cluster test in §1.

## 3. Disposition — this is a methodology finding, not a routing decision

**Verdict: `NOT-CONFIRMED`.** Per the synthesis: *"A result that both (i) fails to survive its
own regime-concentration test and (ii) is smaller than its own mechanism-free autocorrelation
baseline is not distinguishable from noise dressed as persistence."*

- **Does not discharge `MCL.md`'s "mechanism-owed" status** — the ledger stays as it was.
- **Does not license a deep-lane prereg.** No K beyond this screen's own disclosed 1 is spent.
- **Retroactively affects S1a (GC):** the identical placebo construction produced S1a's
  p=0.0095 "pass" — see the corrected [`RESULTS_S1A.md`](../rangestate_gc_2026-08/RESULTS_S1A.md)
  §3 addendum. S1a's bottom-line verdict (NULL) is unchanged since it already failed the CI limb
  independent of this defect, but the placebo pass is no longer citable as corroboration.
- **S2 and S3 (Step-0 slate) are PAUSED**, not run — both were queued to reuse this exact
  placebo construction on a new instrument/window; running them before a fix would just
  reproduce the same invalid test at a new $0 cost, compounding false-confidence risk rather
  than reducing it.
- **Structural repair owed, not attempted here:** a corrected null (AR/GARCH-calibrated
  surrogate or phase-randomized surrogate) needs its own scrutiny before any future
  magnitude-persistence-class Tier-1 screen runs. Full detail, root cause, and repair plan in
  the audit note linked above.

## 4. Scope limits

CL (parent) train era only; `MCL.v.0` 2019+ untouched. This result says nothing about whether a
*corrected*-null version of this test would find something real on CL — that is an open,
unopened question, not a foreclosed one. The regime-concentration finding is itself a genuine,
disclosed result (crisis-transition TR persistence measured, whatever its cause) even though it
cannot license the mechanism-general claim the frozen hypothesis made.

---

## 5. RE-MEASUREMENT addendum (2026-08-18, official corrected-null re-score — SIGNAL-GENERIC)

The corrected-null question §4 named open has now been answered officially, under the
[frozen class battery](../../../docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md)
+ its pre-official ADDENDUM-1 (which adjudicated, rules-govern, a spec-internal conflict: the
frozen L4 rule's own n_cond<20 exclusion drops 2010 at n=14, making L4 **PASS 6-of-8,
boundary-exact** — not the predicted "known-fail 6/9," which never applied its own exclusion):

| | old battery (this file, §1) | corrected battery (official) |
|---|---|---|
| placebo / attribution | block-shuffle p=0.0005 "pass" — **retired, invalid null** | IAAFT band: obs at **69.0th pct**, p_upper 0.3107 → attribution **GENERIC** |
| CI limb (L2) | PASS (0.5651) | PASS (carried verbatim) |
| by-year (L4, new) | not a limb | PASS — 6 of 8 valid, required 6, boundary-exact (2013/2017 fail; 2010 excluded n=14; realized false-pass 0.1178 vs frozen-representative 0.090, disclosed per A5) |
| verdict | raw SIGNAL → NOT-CONFIRMED (test invalid) | **SIGNAL-GENERIC** (first valid verdict; no rescue — the voided raw SIGNAL claimed MORE than this does) |

**What SIGNAL-GENERIC is:** real predictability at the pooled construction, attributable to
generic volatility clustering (the canon the prereg itself cited) — SURVIVAL-ONLY-class
durability. **What it is not (A6 rails, binding):** not regime-robust beyond "L4 passed at its
frozen threshold (6 of 8 valid years, boundary-exact)"; not a mechanism (D22 never reached);
not a discharge of this ledger's mechanism-owed status; not a conditioner license (O2
arithmetic owed). Standing co-quotes: crisis>calm per-year ordering (2011/2016/2014 top);
drop-{2011,2014,2016} diagnostic; the §1 "calm-subset independent NULL" is provenance-split —
its CI component survives, its placebo component is VOID (retired null); the level-based
disclosure buckets read calm 0.617 / crisis 0.649 vs the review's event-identity split 0.537
(neither travels without its year list — A7). **Routing:** counts toward slate §4 RESOLVED
(H-SLATE RESOLVED); any follow-up = conditioner-engineering prereg, new operator GO, new K,
confronting the calm-regime question + O2 + O3 + the L4 boundary fact. Full record:
[`RESULTS_CORRECTED.md`](../rangestate_corrected_2026-08/RESULTS_CORRECTED.md).
