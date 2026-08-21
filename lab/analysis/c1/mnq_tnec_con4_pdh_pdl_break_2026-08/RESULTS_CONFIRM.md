# Q-TNEC-CON-4 — CONFIRM RESULTS (same frozen G0)

**Status:** `AMBIGUOUS-HOLD` — both arms' CIs straddle 0; neither arm clears the live-pass
primary; U1 exception spent, cell reverts to U0 (paused).
**Date:** 2026-08-20 · **Cost:** $0.00 (MNQ 1m panel re-pull, `MNQ.v.0` continuous,
2019-05-06→2026-08-20, billed $0.0000 per `db_fetch.py estimate`) · **K:** unchanged —
same `K_intrinsic=1` disclosed at EXPLORE GO; this is the same G0, not a new one.
**Confirm GO:** [`docs/adr/2026-08-20-dense1m-u1-operator-override-con4-reopen.md`](../../../../docs/adr/2026-08-20-dense1m-u1-operator-override-con4-reopen.md)
(`Accepted`, operator override — U1, no new evidence) — [`CONFIRM_GO.md`](CONFIRM_GO.md)
(window + parameter-non-retune declared before this score existed).
**Parent:** [`PREREG_G0.md`](PREREG_G0.md) (frozen `57dc638`) · [`RESULTS.md`](RESULTS.md)
(EXPLORATION, `AMBIGUOUS-HOLD`, 2026-08-11)
**Machine record:** [`RESULTS_CONFIRM.json`](RESULTS_CONFIRM.json) · lib tests **11/11
green pre-run** (8 original `construct_lib` tests + 3 new `run_confirm_g0` window tests)
**Runner:** [`run_confirm_g0.py`](run_confirm_g0.py) — a window-only sibling of
`run_construct_g0.py`'s `run_explore()`; neither that file nor `construct_lib.py` was
modified.

## Headline (CONFIRM = sessions 2025-09-01 → 2026-08-05, the exact reserved window)

| Arm | n | mean net R | WR | session-block 95% CI | placebo p_emp | annSR (daily, zeros incl.) | halves (older/newer) |
|---|---|---|---|---|---|---|---|
| Long | 113 | **+0.0067** | 0.566 | [−0.0811, +0.0935] | 0.449 | +0.161 | **−0.0720 / +0.0813** ✗ |
| Short | 75 | **−0.0611** | 0.400 | [−0.2006, +0.0806] | 0.806 | −0.920 | **+0.0017 / −0.1131** ✗ |

212 scored sessions · coverage 188 (88.7%) · mean stop_dist ≈ **433.7 pt** · mean signed
gross ≈ +1.99 pt · gross/(4×RT) ≈ **0.35×**.
**TNEC:** `U U U U U | U | U | L0.0067/S-0.0611`.

## Gate walk (identical frozen thresholds — no criterion moved)

- **FALSIFIED?** No — short arm has n=75 (< the n≥100 floor for `arm_fail`); long arm's CI
  upper (+0.0935) is not below 0 regardless.
- **SHAPE-CLEAR-CANDIDATE / live pass?** No — neither arm clears the primary (both CI
  lower bounds < 0; long mean is barely positive but CI straddles 0, short mean is
  negative). Aux limbs also fail on both arms (placebo p 0.449/0.806, both ≫ 0.05;
  halves disagree on both arms).
- → **`AMBIGUOUS-HOLD`**. Per [ADR §4](../../../../docs/adr/2026-08-20-dense1m-u1-operator-override-con4-reopen.md#4--falsifier-revert-trigger),
  this fires the pre-registered **revert trigger**: the U1 exception is spent, `CON-4`
  reverts to `U0` (paused), no further exception is auto-granted.

## EXPLORE vs CONFIRM (disclosure — the honest comparison, not a re-score)

| | EXPLORE (≤2025-08-31) | CONFIRM (2025-09-01→2026-08-05) |
|---|---|---|
| Long mean R | −0.0066 | +0.0067 |
| Short mean R | +0.0053 | **−0.0611** |
| Mean stop_dist | 256.8 pt | 433.7 pt |
| Gross vs 4×RT | 0.27× | 0.35× |
| n (long/short) | 737 / 541 | 113 / 75 |

Both signs are unstable across the two windows (long flips sign, short flips sign and
grows an order of magnitude in magnitude) while both remain statistically
indistinguishable from zero in both windows — consistent with a flat, noisy construct
rather than a near-miss that a longer or different window would resolve. The shorter
CONFIRM window (≈11 months vs EXPLORE's multi-year span) also means substantially wider
CIs; the sign instability is not explained by that alone (short's CONFIRM CI still
excludes most of EXPLORE's short point estimate).

## What this run does NOT license

Cap claim · deploy/Pine/arming · retuning PDH/PDL / first→N / stop geometry · marking U2
· reopening `CON-1/2/3/5` · treating this AMBIGUOUS-HOLD as a near-miss to "finish" with a
parameter change (ADR §5 forbidden moves).

## Consequence

Per the ADR's own revert-action clause: this becomes the **ninth** consecutive
zero-yield close in the short-horizon MNQ microstructure thread (the eight named in the
[`Q-TNEC-CON-5` closure](../../../../docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md),
now plus this out-of-sample read) — strengthening, not weakening, the original pause
rationale. `Q-TNEC-CON-4` reverts to `U0`; a second attempt at this or any other paused
cell needs its own fresh ADR.
