# Closure — Q-HARV-0 / HARV-2026-001

**Brief:** [`docs/ltm/briefs/Q-HARV-0-month-end-rebalance-ES.md`](../Q-HARV-0-month-end-rebalance-ES.md)
**Lab RESULTS:** [`lab/archive/harv_0_month_end_rebalance_es_2026-07/RESULTS.md`](../../../lab/archive/harv_0_month_end_rebalance_es_2026-07/RESULTS.md)
**Closed:** 2026-07-12 (Phase 5). Analysis flow complete; K manifest closed.

---

## Verdict (exactly one)

**AMBIGUOUS** (reporting taxonomy: `DONE_WITH_CONCERNS`).

The mechanism's primary prediction is **corroborated at H1** — the sign-aligned
conditional fade of the intra-month ES-vs-ZN outperformer over T-3→T-1 is
**+19.21 bp**, permutation **p=0.0129** (0.0042 under the alternative fix-qualifying
null), clearing the **4× cost hurdle (6.84 bp)**, with the GC negative control clean
(p=0.70), covariance monotone (high 38.5 > low 30.4 bp), and the native-MES micro-OOS
same-signed (+15 bp). But it is **not RESOLVED**: one bundled prediction fails and two
diagnostics raise durability concerns.

## Deployability annotation (§4; accompanies all closures; never alters verdict)

`DEPLOYABLE-DEFAULT-ENVELOPE:` **YES** — capturable intraday component C = +21.10 bp
(same-signed as H1) ≥ 4× the two-round-trip hurdle (13.68 bp). The edge is
mostly capturable in the E1-compliant enter-at-reopen / flat-by-deadline
decomposition (the settlement-gap component does not dominate). **Informational
only** — an AMBIGUOUS mechanism verdict does not open the deployment fork.

## Which §6 trigger fired

**P-placebo magnitude clause.** The identical rule on the mid-month T-13→T-11 window
returns **−29.07 bp** (permutation p=0.98, i.e. not significantly positive) — but its
*magnitude* exceeds 50% of the primary (9.6 bp), so `placebo_ok` is False.

Interpretation (post-closure diagnostic 2026-07-12; for the fresh brief, not a
rescue): the placebo trigger is **gate geometry, not a market phenomenon**. The
frozen placebo window T-13→T-11 sits **inside the conditioning window**
(prev-T-1→T-4), so months selected on R_spread mechanically carry anti-signal
drift in *every* sub-window of the conditioning period. Measured: signed ES drift
over the full conditioning window = **−363 bp** (mean |R_spread| among qualifying
= 412 bp over ~18.6 trading days) ⇒ pro-rata prediction for any 2-day sub-window
= **−39 bp**; observed signed means: T-16→T-14 **−38.2**, T-13→T-11 (frozen)
**−29.1**, T-10→T-8 **−28.3**, T-7→T-5 **−29.8 bp** — uniform across the month
and matching the selection-arithmetic prediction. No mid-month momentum
phenomenon is needed; nothing is special about the frozen window. Consequence:
with a ~30–39 bp mechanical floor against a 9.6 bp allowance (50% of the 19.2 bp
primary), **the placebo magnitude clause was structurally un-passable at
registration** — the primary would have needed to be ~60–80 bp (no calendar
effect is that large) for RESOLVED to be reachable. The p-clause half of the
placebo (p > 0.10) did pass (0.98). The frozen partition still binds — the honest
verdict is AMBIGUOUS, and per §5 this diagnosis is not permitted to promote it —
but the trigger should be read as "the gate measured its own conditioning
overlap," not "the mechanism failed a control." The next-month reversal
(signal·T-1→next-T3 = −15.96 bp) independently fits the transient-pressure story.

**Compounding concerns (diagnostics, non-gating):**
- **Era decay:** 2010-2017 +26.3 bp (p=0.015) vs 2018-2026 +13.4 bp (**p=0.10, not
  significant**). The edge is front-loaded.
- **Micro-era-parent non-significance:** on 2019-05→ (the deployable era) the parent
  effect is +14.9 bp but **p=0.13**. Native MES same-sign still holds (the frozen
  proxy gate), but significance weakens exactly where deployment would live.
- Roll robustness is *good news*: the effect is **stronger ex-quarter-end** (+25.1 bp,
  p=0.016) than in the roll-contaminated quarter-end subset (+7.9 bp, p=0.19), so the
  headline is not a `.c.0` roll-phantom artifact.

## What a fresh brief would need (new ID + K increment; §5/§8)

1. A **placebo disjoint from the conditioning window** — either end the conditioning
   earlier (e.g. prev-T-1→T-14, placebo T-13→T-11, accepting staler conditioning) or
   make the magnitude clause sign-aware (fire only on *same-signed* placebo ≥50%).
   The current geometry (placebo ⊂ conditioning) makes the clause structurally
   un-passable (see trigger interpretation above). Plus a **gate-reachability check
   at registration**: simulate every bundled clause under a plausible-true-mechanism
   world before freezing — H1 got a power disclosure; the placebo clause never got a
   reachability one.
2. Address **decay**: pre-register on the 2018→ era (or a walk-forward) so the verdict
   isn't carried by 2010-2017; the current post-2018 p=0.10 is the load-bearing risk.
3. Resolve **micro-era significance** (native MES, not just same-sign) before any
   deployability claim is trusted.
None of these may edit the frozen §4 (T-3→T-1, T-4 cutoff, 100bp) — they are a
*new* candidate.

## Monitor spec

**N/A** — AMBIGUOUS. [`MONITOR_SPEC.md`](../../../lab/analysis/harv_0_month_end_rebalance_es_2026-07/MONITOR_SPEC.md)
stays a template (a monitor is a RESOLVED-only deliverable). Forward note: if a
successor RESOLVES, the era-decay finding makes the "|est| < hurdle for 12 consecutive
months" weakening trigger especially load-bearing.

## K accounting

- Candidate: HARV-2026-001; confirmatory trials **K = 1** (one rule × one window × one
  driver × one threshold). Frozen pre-data per §8.
- Ledger **closed** 2026-07-12: `discovery_manifests/harv2026_001_es_monthend.json`,
  survivor p = **0.0129** (primary H1, frozen null). At K=1 the Bonferroni floor = 0.05,
  so the primary clears the crude multiplicity floor — but the *verdict* is AMBIGUOUS on
  the bundled-prediction adjudication, not on multiplicity. No promotion (ledger verdict
  is always a hand-off to strategy-validation).

## Lane observations (for deferred HARV ADR — appendix harvest)

- **Register-record YAML** was sufficient; no missing fields surfaced during execution.
- **A/B mechanism-grade discount** was operationally meaningful: the monitor spec fell
  out of the frozen operationalization by construction (the Q-DECAY-1 payoff), and the
  bundled predictions (placebo/instrument/covariance/micro) did real adjudication work —
  the placebo in particular converted a clean-looking primary into a defensible
  AMBIGUOUS. Mechanism-first paid for itself vs a bare unconditional test.
- **Gate-reachability is a missing registration step (the load-bearing lane lesson):**
  the frozen placebo clause was structurally un-passable (placebo window ⊂ conditioning
  window ⇒ ~30–39 bp mechanical floor vs a 9.6 bp allowance), so RESOLVED was
  mathematically near-unreachable *before any data arrived* — and neither authoring,
  G1 ratification, Phase-0, check_brief, nor the executor caught it until a post-closure
  diagnostic. Freezing is necessary but freezing an unreachable gate wastes the K. The
  HARV lane ADR should add a mandatory pre-registration **reachability simulation of
  every bundled clause under a plausible-true world** (H1-style power disclosure alone
  is insufficient — it covered the primary, not the bundle).
- **Databento spend vs estimate:** est ≪ $5; **actual ≈ $0.00** (daily bars; global
  cache re-serve). Wall-clock cost was dominated by databento streaming latency (large
  requests stall; small single-symbol yearly chunks + concurrency was the working
  pattern) — a lane-tooling note, not a science note.
- **Wall-clock of the mechanism-conditional battery** (H1 + 4 bundled + deployability +
  micro-OOS) was seconds once the panel was built; the cost was entirely in data
  assembly and the two harness bugs found in execution (weekend-bar offsets, absent-GC
  auto-pass — both fixed, see NOTES / PR).

## Audit hooks (§10)

```bash
grep -E "RESOLVED|FALSIFIED|AMBIGUOUS" docs/briefs/closures/Q-HARV-0*
grep -in "DEPLOYABLE-DEFAULT-ENVELOPE" docs/briefs/closures/Q-HARV-0*
grep -in "monitor" docs/briefs/closures/Q-HARV-0*
python .claude/skills/futures-anomaly-discovery/scripts/register_search.py status --run-id harv2026_001_es_monthend
```
