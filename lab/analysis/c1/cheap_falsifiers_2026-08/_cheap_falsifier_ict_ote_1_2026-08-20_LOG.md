# Cheap falsifier — Optimal Trade Entry (`Q-ICT-OTE-1`) — `FALSIFIED`

**Date:** 2026-08-20
**Licensed by:** [`docs/adr/2026-08-20-analogue-modality-override-ict-ote-1-admit.md`](../../../docs/adr/2026-08-20-analogue-modality-override-ict-ote-1-admit.md)
(`Accepted`, operator override) §7 Phase 1 — the analogue-modality pause otherwise blocks this
construct on construct-type grounds ([`Q-ICT-OTE-1` scoping](../../../docs/briefs/rnd-pipeline/Q-ICT-OTE-1-optimal-trade-entry-scoping.md)).
**Cost / K:** $0.00 · K=0 (never reached G0, no Q-ID/manifest opened)
**Runner:** [`_cheap_falsifier_ict_ote_1_2026-08-20.py`](_cheap_falsifier_ict_ote_1_2026-08-20.py)
**Raw:** [`_cheap_falsifier_ict_ote_1_2026-08-20_RESULTS.json`](_cheap_falsifier_ict_ote_1_2026-08-20_RESULTS.json)
**Panel:** `mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet`

**Reconstruction note:** the original raid/sweep detector
(`lab/analysis/_inbox/ict_mnq_2026-08/run_1m_diag.py`) is not present in this public worktree — never
committed to the public seed, pre-transition history lives only in the private archive. This falsifier
reconstructs the sweep/pivot logic fresh from the frozen prose parameters already on record
(`pvLen=2` pivot, `raidWin=8` same-direction pairing — `PREREG_EXP.md`/`PREREG_D_W.md`) rather than
importing lost code. Accepted for a cheap falsifier (deliberately fast/generous, not a G0-grade
artifact); moot here since the result is decisive either way (see below).

## Frozen geometry (a priori, per the scoping doc §2)

| Knob | Value |
|---|---|
| Sweep | pivot (`pvLen=2`) swept within `raidWin=8` bars, then closes back on origin side |
| Impulse leg | displacement ≥ `1.5×ATR(14)` from the sweep extreme, reversal direction, within 30 bars |
| Entry zone | 0.62–0.79 Fibonacci retracement of the leg, first touch within 20 bars |
| Stop | beyond the sweep extreme (1.0 Fib) |
| Target | frozen 1H range-extreme DOL (`h1High`/`h1Low`, `lookN=60`, `[1]`-lagged) — reused verbatim |
| Exit | target touch, else session-flat |
| Cost | Tradeify RT 1.41pt |

Kill: coverage &lt;20% → VOID; both arms n≥100 and session-block CI entirely &lt;0 → FALSIFIED.

## Result

| Check | Value |
|---|---|
| eligible sessions | 1,679 |
| trade sessions | 1,675 (**99.8%**) |
| n trades | 1,675 |
| mean signed pts | **−1.78** |
| mean stop_dist | **13.16 pt** |
| gross/(4×RT) | **−0.32×** |
| elapsed | ~38s |

| Arm | n | mean net R | WR | session-block 95% CI |
|---|---:|---:|---:|---|
| long | 781 | **−0.525** | **11.9%** | [−0.779, **−0.244**] |
| short | 894 | **−0.518** | **8.2%** | [−0.793, **−0.241**] |

**Verdict:** `FALSIFIED` — decisive, not a close call. Both arms powered (n≥100), both CIs entirely
below 0, both point estimates deeply negative. Mean stop_dist (13.16pt) confirms the scoping doc's own
§2.4 prediction exactly: this is CON-5-shaped, not CON-4-shaped — a leg-scale stop, not a session-range
stop — and win rate (8–12%) is even worse than CON-5's own 11–14%. Gross is negative even before R
(mean signed pts −1.78), meaning the raw price movement is net-adverse across both arms combined, not
merely eaten by RT-tax on a flat gross.

## Disposition

- `Q-ICT-OTE-1` **STOP**s here — per the override ADR's own §4 revert trigger, the exception is spent.
  No `PREREG_G0` ever frozen, no mechanism id registered in `MECHANISMS.md` (registration happens at
  G0 freeze, never reached).
- Re-proposal bar: new mechanism evidence, not a Fib-band retune, not a different sweep/pivot
  parameterization, not a different DOL target.
- This is the **10th** consecutive zero-yield close in the short-horizon MNQ microstructure thread
  (following `Q-TNEC-CON-4`'s CONFIRM score earlier this session) — on a construct that reused two
  already-tested pieces and only introduced the impulse-leg/Fib-zone entry as new. The pattern extends
  cleanly to a fourth entry-geometry family (through-break, pullback-reclaim, PDH/PDL-through, now
  sweep-retracement), reinforcing rather than narrowing the tail-exhaustion diagnosis.
