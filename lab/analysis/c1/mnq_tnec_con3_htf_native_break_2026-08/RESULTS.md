# Q-TNEC-CON-3 — EXPLORATION RESULTS (G0)

**Status:** `AMBIGUOUS-HOLD` — long mean net-positive but CI straddles 0; short net-negative; aux limbs fail live-pass.
**Date:** 2026-08-10 · **Cost:** $0.00 (MNQSEL-2 cache reuse; no pull) · **K:** disclosure only (`K_intrinsic=1` frozen at G0).
**Explore GO:** operator in-session 2026-08-10 — [`EXPLORE_GO.md`](EXPLORE_GO.md) (window split + placebo
operationalization + downgrade rules all declared at GO, before any score).
**Parent:** [`PREREG_G0.md`](PREREG_G0.md) · [`brief`](../../../../docs/briefs/Q-TNEC-CON-3-htf-native-compression-break-scoping.md)
**Machine record:** [`RESULTS.json`](RESULTS.json) · lib tests **8/8 green** pre-run

## Headline (EXPLORATION = sessions ≤ 2025-08-31; CONFIRM 2025-09-01→2026-08-05 RESERVED, never read)

| Arm | n | mean net R | WR | session-block 95% CI | placebo p_emp | annSR (daily, zeros incl.) | halves (older/newer) |
|---|---|---|---|---|---|---|---|
| Long | 713 | **+0.0733** | 0.303 | [−0.0732, +0.2256] | 0.165 | +0.405 | **+0.1172 / +0.0304** ✓ |
| Short | 610 | **−0.0255** | 0.228 | [−0.2249, +0.1885] | 0.592 | −0.101 | **+0.0417 / −0.0864** ✗ |

1,436 scored sessions · coverage 1,323 (92.1%) · ~0.50 long / 0.42 short trades/session ·
mean stop_dist ≈ 29.2 pt · mean signed gross ≈ +4.14 pt · gross/(4×RT) ≈ **0.73×** (cost-law bar 4×) ·
EM six-char `P U U P P P`.
**TNEC:** `U U U U U | U | U | L0.0733/S-0.0255`.

## Gate walk (frozen thresholds; declared downgrades)

- **FALSIFIED?** No — neither arm's CI upper bound is below 0 (long +0.226, short +0.189).
- **SHAPE-CLEAR-CANDIDATE / live pass?** No — neither arm clears primary (both CI lo < 0). Long
  would additionally fail declared aux (placebo p=0.165; annSR 0.405 < 0.650) even if primary passed.
- → **`AMBIGUOUS-HOLD`**. Long point estimate and halves agree positive; short is net-negative with
  halves flip. Disposition per brief §6: **ITERATE** — lane packet (not θ-retune; not fade; not
  return to 1m/G=10). CONFIRM unread; Cap unclaimed.

## Decomposition (disclosure, not a re-score)

Structural stops are wide (~29 pt), so RT 1.41 is a smaller R-tax than CON-2's fixed G=10 path.
Signed mean gross +4.14 pt clears 1×RT on the pooled sample, but **gross/(4×RT) ≈ 0.73×** still
fails the cost-law bar. The long arm's session-block CI still includes 0 at powered n=713 — the
edge is not yet SHAPE-clear under the frozen limbs.

## What this run does NOT license

Reading CONFIRM · Cap claim · retuning `K_NARROW`/`NARROW_MULT`/median-20/HTF minutes/first→N
(frozen; Trap #12) · sign-invert to fade · reintroducing 1m/G=10 · deploy/Pine/arming.
