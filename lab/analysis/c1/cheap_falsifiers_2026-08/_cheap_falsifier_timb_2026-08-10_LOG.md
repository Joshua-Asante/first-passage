# Cheap falsifier — T-IMB (time-occupancy trend gate) · `KILL` — conclusive under BOTH gate authorities

**Date:** 2026-08-10 · **$0.00 · K=0 · no Q-ID spent · no G0 authored** · EXPLORATION only (≤ 2025-08-31; CONFIRM unread)
**Trigger:** operator selected T-IMB from the cell-#3 criterion slate (drafted from causal priors only; no oracle-cluster
read — ADR `TEMPORAL-SELECTIVITY-OPEN-2026-08-10` §2-B attested). Lane-spec step 2: falsifier BEFORE authoring.

## Frozen before running (generous so failure is conclusive)

Decision moment = first bar ≥ 11:00 ET · occupancy = share of 1m closes 09:30–10:59 strictly one side of session
open, ties excluded both sides (generous) · **θ = 0.90** · enter occupied side at decision-bar open · G=10 primary,
G=20 also reported (generous) · session-flat · RT 1.41 pt. **KILL iff mean gross pt/trade < 5.64 (4× bar).**

## Result — KILL fires, and survives the gate-authority cross-check

1,456 EXPLORATION sessions · **θ-days: 773 (53.1% — the criterion barely selects; ~2.7 triggers/week)** · long 404 / short 369.

| G | gross pt/trade | vs 5.64 bar | net R (mean) | t | net-R CI95 | WR | stopped |
|---|---|---|---|---|---|---|---|
| 10 | **+2.449** | 0.43× | +0.1039 | **+0.69** | [−0.192, +0.400] | 0.129 | 87% |
| 20 | **+4.136** | 0.73× | +0.1363 | **+0.84** | [−0.181, +0.454] | 0.219 | 76% |

- **Frozen bar (4× gross):** under at both G → KILL as frozen.
- **Gate-authority cross-check (disclosure, same trades, no new look):** the lane's *ratified* intake gate is TNEC
  N-EDGE (net > 0 with 95% CI excluding 0 + DSR), a weaker bar than the frozen 4× — and T-IMB fails that too:
  t ≈ 0.7–0.8 vs the ≈2 required; the point estimate would need ~8× the n to clear, and EXPLORATION is fixed.
  **The kill is conclusive under both authorities — no election between them is needed.**

## Disclosures worth keeping (none licenses anything)

- **First lane candidate with positive net point estimates and halves-consistent gross** (G=10 older +2.32 / newer
  +2.58; G=20 newer half +6.67 — improving, not decaying). Still inside noise.
- **Extreme right-skew payoff:** ~87% small stopped losses (−1.14R) vs ~13% flat-exits averaging ≈ +8.4R (~+84 pt) —
  the unstopped θ-days are genuine trend days. Long-vol loss-side shape (the trailing-DD-friendly archetype per
  `lesson_trailing_dd_survival_is_skew_governed`) — but shape without a CI-cleared mean is not a candidate.
- θ=0.90 triggering 53% of days falsifies the criterion's *selectivity premise* — 90% one-sided morning occupancy
  is the MNQ norm, not a rare conviction state. Raising θ post-hoc is a K-charged retune and is not taken.

## Disposition

**T-IMB dead pre-authoring.** No G0, no Q-ID, lane cell #3 remains unspent. Re-proposal of a time-occupancy gate
requires a materially different causal criterion, not a θ/decision-time retune. The slate's remaining undrafted
alternative (SWING-1) and the decline option return to the operator.
