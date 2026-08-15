# Q-TNEC-CON-5 — EXPLORATION RESULTS (G0)

**Status:** `AMBIGUOUS-HOLD` — both arms mean-negative; CIs straddle 0; aux limbs fail live-pass.
**Date:** 2026-08-11 · **Cost:** $0.00 (MNQSEL-2 cache reuse; no pull) · **K:** disclosure only (`K_intrinsic=1` frozen at G0).
**Explore GO:** operator in-session 2026-08-11 — [`EXPLORE_GO.md`](EXPLORE_GO.md) (window split + placebo
operationalization + downgrade rules all declared at GO, before any score).
**Parent:** [`PREREG_G0.md`](PREREG_G0.md) · [`brief`](../../../../docs/briefs/Q-TNEC-CON-5-impulse-pullback-vwap-reclaim-scoping.md)
**Machine record:** [`RESULTS.json`](RESULTS.json) · lib tests **7/7 green** pre-run

## Headline (EXPLORATION = sessions ≤ 2025-08-31; CONFIRM 2025-09-01→2026-08-05 RESERVED, never read)

| Arm | n | mean net R | WR | session-block 95% CI | placebo p_emp | annSR (daily, zeros incl.) | halves (older/newer) |
|---|---|---|---|---|---|---|---|
| Long | 679 | **−0.1838** | 0.138 | [−0.4541, +0.1013] | 0.894 | −0.532 | **−0.0832 / −0.2788** ✓ |
| Short | 631 | **−0.3600** | 0.106 | [−0.6841, +0.0390] | 0.975 | −0.805 | **−0.3529 / −0.3673** ✓ |

1,457 scored sessions · trades 1,310 (89.9%) · mean stop_dist ≈ **17.5 pt** · mean signed gross ≈ +0.61 pt ·
gross/(4×RT) ≈ **0.11×** · EM six-char `P U U P P P`.
**TNEC:** `U U U U U | U | U | L-0.184/S-0.360`.

## Gate walk (frozen thresholds; declared downgrades)

- **FALSIFIED?** No — neither arm's CI upper bound is below 0 (long +0.101, short +0.039).
- **SHAPE-CLEAR-CANDIDATE / live pass?** No — neither arm clears primary (both mean &lt; 0 and CI lo &lt; 0).
  Aux limbs also fail (placebo / annSR).
- → **`AMBIGUOUS-HOLD`**. Disposition per brief §6: **ITERATE** — lane packet (not θ-retune; not fade;
  not return to through-break / compression). CONFIRM unread; Cap unclaimed.

## Decomposition (disclosure, not a re-score)

Pullback-extreme stops are **tight** (~17.5 pt) — the cost-geometry distinction vs CON-4 held — but
RT 1.41 is now a **large** R-tax (~0.08R per stop-out). WR ≈11–14% with mean-negative R on both arms
implies the reclaim does not pay for the stop rate. Mean signed gross +0.61 pt is **0.11×** the 4×
cost-law bar. Formal FALSIFIED does not fire because CIs still straddle 0 (short upper barely
positive on the explore window).

## What this run does NOT license

Reading CONFIRM · Cap claim · retuning bias / VWAP / first→N / stop geometry · fade-to-VWAP ·
through-break / compression reentry · deploy/Pine/arming.
