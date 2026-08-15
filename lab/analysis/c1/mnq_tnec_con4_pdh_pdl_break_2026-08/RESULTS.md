# Q-TNEC-CON-4 — EXPLORATION RESULTS (G0)

**Status:** `AMBIGUOUS-HOLD` — both arms near-zero; CIs straddle 0; aux limbs fail live-pass.
**Date:** 2026-08-11 · **Cost:** $0.00 (MNQSEL-2 cache reuse; no pull) · **K:** disclosure only (`K_intrinsic=1` frozen at G0).
**Explore GO:** operator in-session 2026-08-11 — [`EXPLORE_GO.md`](EXPLORE_GO.md) (window split + placebo
operationalization + downgrade rules all declared at GO, before any score).
**Parent:** [`PREREG_G0.md`](PREREG_G0.md) · [`brief`](../../../../docs/briefs/Q-TNEC-CON-4-pdh-pdl-breakout-scoping.md)
**Machine record:** [`RESULTS.json`](RESULTS.json) · lib tests **8/8 green** pre-run

## Headline (EXPLORATION = sessions ≤ 2025-08-31; CONFIRM 2025-09-01→2026-08-05 RESERVED, never read)

| Arm | n | mean net R | WR | session-block 95% CI | placebo p_emp | annSR (daily, zeros incl.) | halves (older/newer) |
|---|---|---|---|---|---|---|---|
| Long | 737 | **−0.0066** | 0.532 | [−0.0475, +0.0352] | 0.623 | −0.128 | **−0.0035 / −0.0096** ✓ |
| Short | 541 | **+0.0053** | 0.481 | [−0.0458, +0.0568] | 0.435 | +0.085 | **−0.0054 / +0.0167** ✗ |

1,455 scored sessions · coverage 1,278 (87.8%) · mean stop_dist ≈ **256.8 pt** · mean signed gross ≈ +1.50 pt ·
gross/(4×RT) ≈ **0.27×** · EM six-char `P U U P P P`.
**TNEC:** `U U U U U | U | U | L-0.0066/S0.0053`.

## Gate walk (frozen thresholds; declared downgrades)

- **FALSIFIED?** No — neither arm's CI upper bound is below 0 (long +0.035, short +0.057).
- **SHAPE-CLEAR-CANDIDATE / live pass?** No — neither arm clears primary (both CI lo < 0). Aux limbs
  also fail (placebo / annSR / short halves).
- → **`AMBIGUOUS-HOLD`**. Disposition per brief §6: **ITERATE** — lane packet (not θ-retune; not fade;
  not return to compression family). CONFIRM unread; Cap unclaimed.

## Decomposition (disclosure, not a re-score)

Opposite-prior-extreme stops are **very wide** (~257 pt) — RT 1.41 is a tiny R-tax, so net R ≈ gross/stop.
Mean signed gross +1.50 pt is **below** 1×RT and only **0.27×** the 4× cost-law bar. The cell is
economically dead at the point estimate even before CI/placebo; the formal gate does not fire FALSIFIED
because CIs still straddle 0.

## What this run does NOT license

Reading CONFIRM · Cap claim · retuning PDH/PDL / first→N / stop geometry · fade / level-touch
attraction · compression reentry · deploy/Pine/arming.
