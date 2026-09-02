**Theme:** c1

# Reading, frozen before the result — W1 4th partition (honest-clock bootstrap-95th)

**Written:** 2026-09-02, while the run was executing, **before any full-scale number was read.**
Purpose: fix the decision-consequence mapping in advance so the verdict cannot be framed to fit
whichever number arrives. This adds no hypothesis and moves no threshold — the floor, the
partitions and the verdict semantics were all frozen 2026-07-16 and are quoted, not re-decided.

## What is being measured

The one cell the 2026-08-09 W1 packet declared out of scope. Its own RESULTS:
*"Bootstrap-95th remains unmeasured on the honest clock."* The campaign's pre-registration scores
`bust ≤ 3.0% ∧ pass ≥ 50%` on **{full, H1, H2, bootstrap-95th} × {Tradeify_Select_100K,
MFFU_Rapid_100K}** — eight cells. W1 landed six (all PASS). This run is the remaining two.

## The floor that binds this campaign

**3.0%**, from the 2026-07-13 survivor-scoring pre-registration (`be6dda6`), named as the floor by
the 2026-07-16 haircut pre-registration, whose own forbidden moves include *"Relaxing the 3.0% bust
ceiling or the 50% pass floor, or introducing a separate 'regime floor'."* The harness parses that
value at runtime; it is not retyped here.

⚠ **A second, later ceiling exists and is NOT this campaign's floor.** The §4 falsifier's live gate
was raised 3.0% → 5.0% on 2026-08-26
([`prereg v2`](../../../../docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md),
operator risk-tolerance override). This campaign is frozen against v1's 3.0%. Where the two
disagree, that disagreement is an operator ruling and **must not be resolved here by adopting
whichever number the result makes friendlier.**

## The three readings, fixed in advance

| Honest bust-95th | Reading |
|---|---|
| **≤ 3.0%** (and pass-5th ≥ 50%) | 4th partition PASSES. The class_s 0.50× arm clears all eight cells on the honest clock. `RESOLVED-DEPLOYABLE` is complete as its pre-registration defines it. The de-scope ADR's **T5 first condition** ("0.50× GATE PASS on all four partitions on the venue's honest clock") is **met** — T5 still requires T1 jointly. The §4 discharge-withdrawal ADR's restore condition (≥2 firms ≤3.0%, ≥1 `trailing_locking`) is met on every partition. |
| **> 3.0% and ≤ 5.0%** | 4th partition **FAILS this campaign's frozen floor**. `RESOLVED-DEPLOYABLE` does not complete on the honest clock; T5's first condition is **not** met. The §4 Part A limb would nonetheless clear the *live* v2 ceiling — the two gates disagree, and that is an operator ruling, not a result. Do not report this as a pass. |
| **> 5.0%** | Fails both ceilings. The 0.50× arm is not gate-clearing on the honest clock at the bootstrap partition, and the estate's best-measured cell falls. T5 dead on its own terms. |

In every case the pass-floor limb (pass-5th ≥ 50%) is scored independently and can fail on its own.

## What this run cannot decide

- **It does not fire T5.** T5 requires its first condition **and** T1 (a cadence instrument plus
  measured weekly coverage ≥ 95% and inactivity-ON path death ≤ 10%). T1 is unmeasured with the
  operator token trade modelled. A single trigger read in isolation is named as inadmissible by the
  de-scope ADR itself.
- **It does not re-admit anything to Tradeify.** The eval half of the de-scope stands until a
  superseding ADR, which is an operator act.
- **It does not discharge §4.** §4 discharge is a superseding ADR on the operator's signature.
- **It arms nothing.** `dry_run` stays `true`; M1 stays not-`RESOLVED`.

## Controls that must hold for the number to be readable at all

1. **EOD control arm** reproduces the published corrected-geometry bootstrap-95th
   (Tradeify **1.20%**, `eval_shape_diagnostics_2026-07-28` §(a)) within the same ±2.0pp tolerance
   the haircut runner used on this statistic. A control miss is a harness defect, not a finding.
2. **Non-vacuity** (frozen Phase-4 §1) — reproduced W1's own guard exactly at launch:
   EOD 2.50% vs real 32.33% on the 1.00× book, horizon 400.
3. **Worker-attested geometry** — every panel reports `dd_lock_offset_usd = 1e6`. This defends the
   dated M-23 process-pool leak that produced a wrong published figure on this very harness family
   in July.
4. **Paired-draw equivalence** — the paired resample reproduces the EOD resample's P&L series
   exactly, so the control arm is the published run's path and the arms differ only by the clock.
5. **Block-builder agreement** — `blocks_from_daily_pnl` and `paired_blocks_from_daily` must return
   identical P&L blocks on every panel.

If any control fails, the run reports the defect and no verdict is taken.
