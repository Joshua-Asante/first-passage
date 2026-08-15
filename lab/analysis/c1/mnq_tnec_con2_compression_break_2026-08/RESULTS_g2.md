# Q-TNEC-CON-2 — EXPLORATION RESULTS (G2)

**Status:** `AMBIGUOUS-HOLD` — gross-positive / net-negative; halves sign-flip; non-promotable close.
**Date:** 2026-08-10 · **Cost:** $0.00 (MNQSEL-2 cache reuse; no pull) · **K:** disclosure only (`K_intrinsic=1` frozen at G0).
**Explore GO:** operator in-session 2026-08-10 — [`EXPLORE_GO.md`](EXPLORE_GO.md) (window split + placebo
operationalization + downgrade rules all declared at GO, before any score).
**Parent:** [`PREREG_G0.md`](PREREG_G0.md) · [`brief`](../../../../docs/briefs/Q-TNEC-CON-2-compression-expansion-break-scoping.md)
**Machine record:** [`RESULTS.json`](RESULTS.json) · lib tests **8/8 green** pre-run

## Headline (EXPLORATION = sessions ≤ 2025-08-31; CONFIRM 2025-09-01→2026-08-05 RESERVED, never read)

| Arm | n | mean net R | WR | session-block 95% CI | placebo p_emp | annSR (daily, zeros incl.) | halves (older/newer) |
|---|---|---|---|---|---|---|---|
| Long | 4,321 | **−0.0507** | 0.136 | [−0.1470, +0.0551] | 0.075 | −0.404 | **+0.0238 / −0.1045** ✗ |
| Short | 4,108 | **−0.0440** | 0.112 | [−0.1687, +0.0918] | **0.027** | −0.277 | **+0.1111 / −0.1539** ✗ |

1,436 scored sessions · coverage 1,383 (96.3%) · ~3.0 trades/session/arm · mean MAE ≈ 12.7–12.9 pt ·
mean MFE ≈ 26.5–29.4 pt · EM six-char `P U U P P P`.
**TNEC:** `U U U U U | U | U | L-0.0507/S-0.0440`.

## Gate walk (frozen thresholds; declared downgrades)

- **FALSIFIED?** No — neither arm's CI upper bound is below 0 (long +0.0551, short +0.0918).
- **SHAPE-CLEAR-CANDIDATE?** No — neither arm passes the primary (both means negative; CI lo < 0), so the
  declared aux limbs are moot for promotion.
- → **`AMBIGUOUS-HOLD`**, and with both point estimates negative, both annSR negative, and both arms
  sign-flipping across halves, the honest disposition is a **non-promotable close** of this cell.

## The decomposition that matters (disclosure, not a re-score)

Net R = (pts − 1.41)/10, so the measured means invert to **gross** per-trade capture:
**long +0.90 pt · short +0.97 pt** — a real, placebo-corroborated gross edge (the short arm beats random
same-geometry entries at p_emp 0.027) that the **1.41-pt round trip eats entirely** (gross/RT ≈ 0.65×
against the 4× cost-law bar). At ~3 trades/session/arm this is the EM1 frequency-inversion arithmetic
verbatim: sub-0.40R-gross edges cannot be rescued by trading them more. The halves add the familiar
2024-shape: both arms positive in the older EXPLORATION half, negative in the newer.

## What this run does NOT license

Reading CONFIRM · Cap claim · retuning `K_NARROW`/`NARROW_MULT`/median-20/G/exit (frozen; Trap #12) ·
sign-invert to fade (Family A killed) · a third dense-1m cell without a fresh G0 · deploy/Pine/arming.
