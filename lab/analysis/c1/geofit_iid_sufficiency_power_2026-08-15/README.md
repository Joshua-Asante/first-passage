# i.i.d.-sufficiency power-up — Q-GEOFIT-1 successor scoping (2026-08-15)

**Status:** ACTIVE — scoping probe, follow-up to [`geofit_skew_probe_2026-07-25`](../../../archive/geofit_skew_probe_2026-07-25/README.md). Stay hot: `aegis3leg_engine_param` imports this scoring tree. **Not** a re-open of Q-GEOFIT-1. Produces no envelope, no grid, no cells, no candidate claim. **$0.00 spend, zero K.**
**Verdict:** `MARGINALS-SUFFICIENT`
**Driver:** [`run_power_up.py`](run_power_up.py) (pre-declaration in its module docstring, fixed before it ran) · [`combine_verdict.py`](combine_verdict.py) (pooling arithmetic) · data [`power_up_new45.json`](power_up_new45.json), [`combined_n50_verdict.json`](combined_n50_verdict.json) · log [`run_power_up.log`](run_power_up.log)

## Question

The prior probe confirmed skew is the dominant missing dimension in Q-GEOFIT-1's closed family (24.69pp at stake, 23.18σ) but left one question explicitly unresolved: does the *true* empirical marginal distribution, drawn i.i.d. (`empirical_shuffle`), reproduce the real c1 book's trailing-DD bust rate — or is within-week serial structure load-bearing? At N=5 the arm landed 1.75σ from target, underpowered (minimum resolvable difference 2.53pp, looser than the 0.5pp tolerance itself) — not a pass, not a miss.

The prior probe's own README named the fix: *"Resolving it needs roughly N ≥ 50 for `empirical_shuffle`."* This probe runs that N.

## What ran

45 new `empirical_shuffle` realizations (seeds 20260815000–20260815044), pooled with the original 5 (seeds 20260725–20260729, `geofit_skew_probe_2026-07-25/probe.json`) for N=50 total. Same tier (`Tradeify_Select_100K`), same corrected geometry (`dd_lock_offset_usd → 1e6`), same frozen engine, same real active-day values (350 non-zero days rebuilt from the same panel, verified byte-identical: `n_bdays=1692`, `z=0.7931` match the original study exactly). Decision rule inherited unchanged: ±0.5pp on `|mean_bust − 4.7433%|`.

## Result

| | N=5 (original) | N=50 (pooled) |
|---|---|---|
| mean bust | 5.62% | **4.95%** |
| SE | 0.50pp | **0.10pp** |
| residual vs real (4.7433%) | 0.87pp | **0.21pp** |
| residual / SE | 1.75σ | 2.02σ |
| 2×SE (resolving power) | 2.53pp | **0.21pp** |
| vs 0.5pp tolerance | underpowered | **within, decisively** |

**`MARGINALS-SUFFICIENT`.** The residual (0.21pp) now sits *inside the test's own resolving power* (2×SE = 0.21pp) — the opposite of the N=5 attempt, where the resolving power (2.53pp) was five times looser than the tolerance it was meant to adjudicate. This is not a lucky pass from a weak test; it is a decisive one.

**Read the σ honestly, not just the boolean.** residual/SE rose slightly (1.75σ → 2.02σ) even as the raw gap shrank, because SE fell faster than the residual did. A ~2σ deviation from a literal zero-gap match cannot be ruled out — there may be a small, real difference between the i.i.d.-resampled process and the single historical realization. But its *magnitude* (0.21pp on a 4.74% target) is well inside the ±0.5pp band that was set in advance as substantively sufficient, and that tolerance — not a zero-gap significance test — is the pre-declared decision instrument. The verdict stands on that basis.

## What this settles, combined with the prior probe

Both questions the original skew probe left open are now closed:

1. **Skew is the dominant missing dimension** (confirmed 2026-07-25, unchanged here).
2. **The true marginals, drawn i.i.d., are sufficient** (confirmed here) — no within-week block/serial structure needs to be modeled. `no i.i.d. family can work` is refuted; the earlier concern that a successor might need a materially bigger re-scope (block structure) does not hold.

Together this narrows the successor family class precisely: an **i.i.d. family with an explicit skew/loss-tail dimension**, matched to the real book's win/loss asymmetry, is the correct shape. `skewed_gamma`'s own instability (raw Gamma win-tail, sd 10.85% at N=5) remains a live design defect — bounding that tail is what separates "the right family class" from "a family ready to build a grid on." That is the one item this probe does not resolve; it is a construction choice for the successor brief, not a power problem.

## For the successor brief

Everything [`Q-GEOFIT-1`'s own §8](../../../../docs/briefs/closures/Q-GEOFIT-1-closure-ambiguous-parameterization.md#8-forward--what-a-successor-brief-must-carry) already required, unchanged, plus:

1. Family shape is now doubly-validated: i.i.d., skew-aware, matched on win-rate + separate win/loss scales — not block-structured.
2. The win-tail must be bounded (Gamma at the fitted shape throws unbounded monster realizations); this is a design decision for the successor to make explicitly, not inherited from either probe.
3. `z` range must extend to ≈0.80 (§8 item 2, unchanged — both real books exceed the closed family's 0.40 ceiling).

## Retrieval note (repo hygiene, not a probe finding)

The MC engine and panel-building code this probe depends on (`run_class_s_c1_regime_gate.py`, `run_class_s_c1_scoring.py`) were deleted from `lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/` by the Great Prune class-2 sweep (commit `283d1de`, 2026-08-08) along with that closed campaign's other scaffolding. Retrieved read-only from `pre-prune-2026-08-08` and vendored into this probe directory unmodified (see each file's header) — not a revival of that campaign, which stays pruned. No other still-open thread was found depending on the same deleted files during this session; if the successor brief is authored, it will need the same retrieval step.
