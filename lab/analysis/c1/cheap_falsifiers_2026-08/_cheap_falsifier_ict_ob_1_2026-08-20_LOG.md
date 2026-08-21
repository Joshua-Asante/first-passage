# Cheap falsifier — Order Blocks (`Q-ICT-OB-1`) — `FALSIFIED`

**Date:** 2026-08-20
**Licensed by:** [`docs/adr/2026-08-20-analogue-modality-override-ict-ob-1-admit.md`](../../../docs/adr/2026-08-20-analogue-modality-override-ict-ob-1-admit.md)
(`Accepted`, operator override, pre-approved) §7 Phase 1.
**Cost / K:** $0.00 · K=0 (never reached G0, no Q-ID/manifest opened)
**Runner:** [`_cheap_falsifier_ict_ob_1_2026-08-20.py`](_cheap_falsifier_ict_ob_1_2026-08-20.py)
**Raw:** [`_cheap_falsifier_ict_ob_1_2026-08-20_RESULTS.json`](_cheap_falsifier_ict_ob_1_2026-08-20_RESULTS.json)
**Panel:** `mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet`

**Reconstruction note:** identical to `Q-ICT-OTE-1`'s own falsifier — the original displacement/FVG
detector is absent from this public worktree; displacement detection here is reconstructed fresh from
the frozen `dispMlt=1.5×ATR(14)` parameter already on record, not imported code.

## Frozen geometry (a priori, per the scoping doc §2)

| Knob | Value |
|---|---|
| Displacement | `\|close[t]-close[t-1]\| ≥ 1.5×ATR(14)` |
| Order block | last opposing-color candle before the displacement bar (no sweep precondition) |
| Entry | first touch of the OB candle's `[low, high]` range, within 30 bars of displacement |
| Stop | beyond the OB candle's far edge |
| Target | frozen 1H range-extreme DOL (`h1High`/`h1Low`, `lookN=60`) — reused verbatim |
| Exit | target touch, else session-flat |
| Cost | Tradeify RT 1.41pt |

Kill: coverage &lt;20% → VOID; both arms n≥100 and session-block CI entirely &lt;0 → FALSIFIED.

## Result

| Check | Value |
|---|---|
| eligible sessions | 1,679 |
| trade sessions | 995 (**59.3%**) |
| n trades | 995 |
| mean signed pts | **−2.60** |
| mean stop_dist | **14.75 pt** |
| gross/(4×RT) | **−0.46×** |
| elapsed | ~20s |

| Arm | n | mean net R | WR | session-block 95% CI |
|---|---:|---:|---:|---|
| Long | 376 | **−1.039** | **12.0%** | [−1.381, −0.681] |
| Short | 619 | **−0.379** | **11.6%** | [−0.704, −0.044] |

**Verdict:** `FALSIFIED` — decisive, worse than `Q-ICT-OTE-1`'s own null on every axis measured. Mean
stop_dist (14.75pt) confirms the scoping doc's §2.4 prediction: a single-candle range is even tighter
than OTE's sweep-extreme anchor (13.16pt), and win rate (11–12%) is essentially identical to both OTE
and CON-5 — the same catastrophic shape recurring a third time on a third distinct entry-geometry
definition. Long arm's mean R of −1.04 (a loss exceeding the full risked stop, on average) reflects
stop-outs concentrated against a very tight box next to a target that, when missed, is expensive
relative to that box.

## Disposition

- `Q-ICT-OB-1` **STOP**s here — per the override ADR's own §4 revert trigger, the exception is spent.
  No `PREREG_G0` frozen, no mechanism id registered.
- Re-proposal bar: new mechanism evidence — not a sweep-precondition add-on, not a body-only OB
  redefinition, not a different displacement threshold.
- This is the **11th** consecutive zero-yield close in the short-horizon MNQ microstructure thread, and
  the third of three same-session entry-geometry constructs (CON-4 CONFIRM, `Q-ICT-OTE-1`,
  `Q-ICT-OB-1`) to die on the identical tight-stop/low-WR/RT-dominant shape. That recurrence across
  three genuinely different entry definitions, all anchored to the same frozen 1H DOL target, is itself
  the more informative finding than any single result: the target may be the shared point of failure,
  not any one entry rule.
