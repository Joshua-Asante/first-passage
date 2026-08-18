**Theme:** _inbox
**Status:** AMBIGUOUS-HOLD — BOUNDED extremes disagree; scored core MISCALIBRATED
# Q-TRAINKILL-1 — joint kill-record likelihood

**Verdict:** `AMBIGUOUS-HOLD`. BOUNDED extremes disagree (`MISCALIBRATED` at ε vs `KILLS-INFORMATIVE` at 1−ε). Scored-only core (n*=8) is `MISCALIBRATED`.
**Date:** 2026-08-18
**Spend / K:** $0 / K=0
**Parent:** [`Q-TRAINKILL-1-train-gate-power.md`](../../../../docs/briefs/Q-TRAINKILL-1-train-gate-power.md)
**Prereg (hashed before TABLE.json was opened by the scorer):**
`91855ed188e6d5268ef2050e21d9f77649c6f21ac9b19716e181b3cc59981730`

Reproduce:

```bash
python lab/analysis/_inbox/q_trainkill_1_2026-08/score_trainkill.py
```

The runner prints the prereg sha256 **before** reading `TABLE.json`.

---

## Fit vs the frozen 0.05 floor

| Object | g(0) | g(+0.10R) | Fits? |
|---|---|---|---|
| Scored core (n*=8) | **0.024365** | **1.807e-05** | neither (`MISCALIBRATED`) |
| Fit floor (frozen) | 0.05 | 0.05 | — |
| all-BOUNDED-at-ε | below floor | below floor | `MISCALIBRATED` |
| all-BOUNDED-at-1−ε | zero rises above floor | bar stays below | `KILLS-INFORMATIVE` |

`AMBIGUOUS-HOLD` because the two BOUNDED extremes **disagree** (prereg §D / brief §6). The floor, μ_bar, event map, and both-arms product were not moved after seeing g.

---

## Scored rows (n*=8)

| id | event | mode | P(v\|μ=0) | P(v\|μ=+0.10) |
|---|---|---|---|---|
| Q-TNEC-CON-2 | AMBIGUOUS | one_arm | 0.950 | 0.508 |
| Q-TNEC-CON-3 | AMBIGUOUS | one_arm | 0.950 | 0.741 |
| Q-TNEC-CON-4 | AMBIGUOUS | one_arm | 0.950 | **0.00272** |
| Q-TNEC-CON-5 | AMBIGUOUS | one_arm | 0.950 | 0.891 |
| MSL-C1 | FALSIFIED | both_arms | **0.000625** | 3.77e-10 |
| MSL-C2 | FALSIFIED | both_arms | **0.000625** | 6.63e-09 |
| MSL-C3-K2 | FALSIFIED | both_arms | **0.000625** | 7.32e-09 |
| Q-MNQDTL-CON-1 | FALSIFIED | both_arms | **0.000625** | 6.79e-10 |

Residue (disclosed, not a retune): four both-arms FALSIFIED rows score as the product of two ~0.025 tails under independence, so P(F\|μ=0)≈0.000625 each. That alone pulls g(0) under 0.05. CON-4's tight CI around 0 makes P(AMB\|μ=+0.10) tiny. Neither DGP produces this formal both-arms-FALSIFIED + tight-straddle mix at these se's.

---

## BOUNDED rows (n=7; not dropped)

| id | reason |
|---|---|
| MSL-S2A | N-ACT kill; mean-R CI did not fire FALSIFIED |
| Q-R2VBUCK-1 | association/ρ cell; no mean-R CI |
| Q-R2FLOW-1 | association/ρ cell; no mean-R CI |
| Q-R2AGRUN-1 | association/ρ cell; no mean-R CI |
| DL-1 | ABANDONMENT on annSR/SPA nomination gates; not a mean-R CI event |
| Q-CAPFLOW-1 | ρ CI, not mean-R; +0.10R bar does not translate |
| H-DSTRUCT-MNQ-1 | gateHit vs 0.50 screen; not a mean-R CI |

Filling those seven at P≈1 dilutes the four both-arms products enough that zero clears 0.05; filling at ε does not. That is the disagreement that holds the verdict.

---

## What this does not license

- Quoting `GATES-UNDERPOWERED` or `KILLS-INFORMATIVE` as the class reading.
- Lowering any gate threshold, or moving 0.05 / μ_bar / the both-arms product after seeing g.
- Rewriting campaign #2 n/panel from a named power finding (there is none).
- Quoting zero-yield streaks as settled supply-drought, or as settled under-power.
- Dropping a named row, or mapping ρ / N-ACT / annSR into +0.10R after this g.
- Treating reachability audits as this answer.
