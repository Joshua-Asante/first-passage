**Theme:** c1
**Status:** ACTIVE — two Part A clearers at 50K band; RIDER FAIL stands a fortiori
# c1 band re-score under corrected eval geometry — RESULTS

> ⚠ **Partly SUPERSEDED — see the Addendum (2026-07-28) before citing the bootstrap rows.** The
> rider's bootstrap arm ran defective geometry through a process pool; the published boot-95th
> figures (4.54% / 4.49%) are superseded (corrected T-50K **6.69%**; MFFU not re-measured). The
> `RIDER FAIL` verdict stands a fortiori. Body unedited (Trap #12); this banner is the
> reader-intercept (operational_rules.md Rule 14).

**Status:** `RESOLVED-CLEARER-FOUND` (pre-reg §6 row 1)
**Date:** 2026-07-24
**Pre-registration:** [`2026-07-24-c1-band-rescore-corrected-geometry-prereg.md`](../../../docs/briefs/pre-registration/2026-07-24-c1-band-rescore-corrected-geometry-prereg.md) (`FROZEN` under the operator's same-day "proceed with the two unmeasured arms" directive)
**Runner:** [`run_band_rescore.py`](run_band_rescore.py) · report [`band_rescore_report.json`](band_rescore_report.json)
**Engine:** frozen primitives (`run_partition_mc` → `run_tier_remc`), 10K sims × seeds 42/123/2026, horizon 1500, Run-2 consistency-on, corrected geometry (`dd_lock_offset_usd → 1_000_000.0`, restored after). Floor: bust ≤ 3.0% ∧ P(pass) ≥ 50%.
**Reproduction control:** `Tradeify_Select_100K` @ 1.00× corrected → **4.74%** vs published pin 4.74% — **MATCH**.

## Headline

**Two Part A clearers exist at the 50K band under corrected geometry — at two
different firms, both `trailing_locking`:**

| Tier | Arm | bust | pass | Floor | Cap check (est/cap) |
|---|---|---|---|---|---|
| Tradeify_Select_25K | 1.00× | 1.06% | 98.93% | PASS | **FAIL (20/10)** |
| Tradeify_Select_25K | 0.50× | 0.01% | 99.89% | PASS | OK (10/10) |
| **Tradeify_Select_50K** | **1.00×** | **1.06%** | **98.93%** | **PASS** | **OK (40/40 — cap-exact)** |
| Tradeify_Select_50K | 0.50× | 0.01% | 99.89% | PASS | OK (20/40) |
| Tradeify_Select_150K | 1.00× | 4.74% | 95.25% | FAIL | OK (118/120) |
| Tradeify_Select_150K | 0.50× | 0.11% | 99.80% | PASS | OK (59/120) |
| **MFFU_Rapid_50K** | **1.00×** | **0.96%** | **99.03%** | **PASS** | **OK (40/50)** |
| MFFU_Rapid_50K | 0.50× | 0.01% | 99.89% | PASS | OK (20/50) |

Clearers per the pre-registered accept rule (1.00× floor PASS + cap OK on the
feasibility-eligible set): **`Tradeify_Select_50K`, `MFFU_Rapid_50K`**.

## Why the 50K band clears when the 100K band does not

The effect is the **firms' own tier geometry, not anything about the book**:
Tradeify Select 25K/50K and MFFU Rapid 50K carry a **4.0% trail** ($1,000/$2,000)
where the 100K tiers carry **3.0%** ($3,000), with the same 6% target. Linear
scaling preserves the book's P&L ratios exactly, so bust is a function of the
tier's (trail%, target%, consistency) triple: 4.0%-trail tiers → ~1% bust;
3.0%-trail tiers (100K, 150K) → 4.74%. The identical 25K/50K figures are this
mechanism made visible (identical ratio triples). MFFU-50K differs slightly
(0.96%) via consistency 50% vs 40% and `min_trading_days` 2 vs 3.

## What this does and does not mean (governance — pre-reg §5 kept strictly)

1. **The 2026-11-08 demotion clause is defeated on its own terms.** The §4
   revert trigger fires only if "no pre-registered portfolio candidate clears
   the pass-rate ceiling on **any** AUTOMATION_FRIENDLY_PROP_FIRMS tier in a
   dated lab re-MC." This dated, pre-registered run produces two clearing
   tiers.
2. **This is NOT a §4 discharge.** The frozen survivor-scoring pre-registration
   discharges on ≥2 firms clearing **at the frozen $100K×4 set** — chosen
   precisely to foreclose band-grinding. The two-firm / ≥1-trailing_locking
   *shape* is present at 50K, but reading it as a discharge requires an
   operator decision + an amending ADR that re-pins the scoring band, not this
   study. Routed to operator review.
3. **The regime rider ran to completion — verdict `RIDER FAIL (regime-fragile)`;
   the Part A read stands with a standing caveat**
   ([`run_band_regime_rider.py`](run_band_regime_rider.py) ·
   [`band_regime_rider_report.json`](band_regime_rider_report.json)):

   | Tier | Full | H1 | H2 | boot-95th (n=100) | pass-5th | Rider |
   |---|---|---|---|---|---|---|
   | Tradeify_Select_50K | 1.06% | 1.83% PASS | 0.63% PASS | **4.54% FAIL** | 94.9% | FAIL |
   | MFFU_Rapid_50K | 0.96% | 1.67% PASS | 0.57% PASS | **4.49% FAIL** | 95.3% | FAIL |

   The halves both PASS (the 100K corrected H1 was 6.78% FAIL — the 4%-trail
   band survives the 2020-23 chop half), but the 6mo-block bootstrap-95th
   sits ~1.5pp above the 3.0% ceiling on both tiers. Per the inherited
   candidate §6 semantics, a rider FAIL does **not** overturn the mechanical
   Part A clear — it rides as a **standing regime-fragile caveat**. For
   calibration: this is the same standing shape the original 2026-07-15 100K
   discharge carried (its rider also FAILED, at boot-95th 10.37%/10.33%
   defective-geometry); the 50K band shrinks the fragility ~2.3× but does not
   clear it. The deployed-rung contrast also holds here as at 100K: fragility
   is a 1.00×-basis property.
4. **T-50K is cap-exact (40/40)** — the linearly-scaled book at 1.00× sits at
   the eval contract cap with zero headroom. The pre-committed
   integer-quantization check (F2-floor pattern: derive per-leg integer
   quantities at the 50K basis, confirm the pyramid legs don't floor to
   degenerate sizes and the cap_alloc split fits) is owed before this tier is
   acted on. MFFU-50K has real headroom (40/50).
5. **The 25K floor-pass is not a clearer** (cap-infeasible at 1.00× by
   pre-declared construction) and the 0.50× column is diagnostic-only
   (deployed-rung context; the frozen gate scores the candidate basis).
6. **Operational implications are operator territory:** the registered live
   account is a Tradeify Select **100K**; whether a 50K-band eval (cheaper
   entry, smaller funded ceiling, same firm class) belongs in the program is an
   ops/economics decision this study does not touch.

## Limitations (stated, not discovered later)

- Linear P&L scaling assumes continuous position divisibility; integer
  granularity at 50K is unmodeled here (item 4 above owes the check).
- The consistency clause is scale-invariant (ratio-based), so Run-2 semantics
  transfer under linear scaling; `min_trading_days` and inactivity semantics
  are inherited from the frozen engine configuration.
- No claim is made about tiers outside the measured set (Bulenox/BluSky bands
  carry no correction defect and were not looked at — a new look needs its own
  pre-registration).

## Addendum 2026-07-28 — the rider's bootstrap arm ran DEFECTIVE geometry; boot-95th figures superseded

**The published rider bootstrap-95th values (T-50K 4.54% / MFFU-50K 4.49%) are
defective-geometry numbers and must not be cited.** The rider's *full-panel and
half-panel* figures are unaffected and stand.

**Mechanism (confirmed by code read, not inference).**
[`run_band_regime_rider.py:54`](run_band_regime_rider.py) patches
`dd_lock_offset_usd → 1_000_000.0` on the **parent process's** `FIRM_RULES` dict.
Full/halves are computed in-parent, so they inherit the corrected value — which is
why those pins still reproduce. But `part_a_bootstrap`
([`run_class_s_c1_regime_gate.py:227`](../class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py))
fans out via `Parallel(prefer="processes")` passing only the **firm-key string**;
each worker re-imports `firm_rules` from disk and rebuilds config from the
**defective** on-disk `dd_lock_offset_usd: 100`. The bootstrap therefore scored a
drawdown lock that does not exist in eval, with entirely plausible-looking output.
This is the exact trap surfaced by Q-GEOFIT-1 on **2026-07-25** — one day *after*
this rider ran — and now recorded as **M-23** in
[`docs/methodology/lessons/methodology_lessons.md`](../../../docs/methodology/lessons/methodology_lessons.md).

**Corrected values** (worker-local patch + per-panel attestation; same frozen
`BOOT_SEED=20260715`, n=100, block=126bd, seeds 42/123/2026, 10K sims/seed) —
[`../eval_shape_diagnostics_2026-07-28/RESULTS.md`](../eval_shape_diagnostics_2026-07-28/RESULTS.md)
Part B, report `rider_tail_attribution.json`:

| Cell | Published (defective) | Corrected (attested) | Ceiling | Verdict |
|---|---|---|---|---|
| `Tradeify_Select_50K` @ 1.00× | 4.54% | **6.69%** | 3.0% | RIDER FAIL (a fortiori) |
| `Tradeify_Select_100K` @ 1.00× | (none published) | **17.79%** | 3.0% | FAIL |
| `Tradeify_Select_100K` @ 0.50× (deployed) | 0.77% | **1.20%** | 3.0% | **PASS** |
| `MFFU_Rapid_50K` @ 1.00× | 4.49% | **NOT RE-MEASURED** | 3.0% | impeached; expected worse |

**What changes and what does not.** The **`RIDER FAIL (regime-fragile)` verdict
stands and strengthens** — the corrected fragility is larger, not smaller, so §6's
disposition (a rider FAIL does not overturn the mechanical Part A clear, but rides
as a standing caveat) is untouched. **Part A headline figures are unaffected**
(T-50K 1.06% / MFFU 0.96% reproduce as MATCH under attested corrected geometry).
The "~2.3× fragility shrink vs the 100K band" calibration in §item-3 above is
**withdrawn** — it compared a corrected 50K number against a defective 100K one;
the honest corrected comparison is 6.69% (50K) vs 17.79% (100K @ 1.00×), a ~2.7×
shrink, still not clearing. **MFFU-50K's corrected boot-95th is unknown** — cite it
as impeached, never as 4.49%.

**Attribution (new, no prior decomposition existed).** Top-decile-bust resamples are
separated by a **small set of recurring 6-month block starts** (top-5 block-start
mass ≥0.45 on both tiers; starts near panel indices 470/487), **not** by H1-vs-H2
share, **not** by MYM-vs-MNQ loss share, and **not** by Tuesday co-fire density (all
near-zero deltas). Fragility is concentrated in identifiable windows, not diffuse.
Cohort is n=10 of 100 — descriptive, not inferential.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-24 | Run executed per FROZEN pre-reg; verdict `RESOLVED-CLEARER-FOUND` (T-50K + MFFU-50K at 1.00× corrected); control MATCH 4.74%; routed to operator review; regime rider queued | Joshua (directive) + Claude Code (Fable 5) |
| 2026-07-28 | Addendum: rider **bootstrap** arm ran defective geometry (parent-only patch + process pool); boot-95th 4.54%/4.49% superseded — corrected T-50K **6.69%**, MFFU **not re-measured**; RIDER FAIL stands a fortiori; full/halves unaffected; ~2.3× shrink calibration withdrawn; block-level attribution added | Claude Code (Opus 5) — adjudication of PR #541 |
