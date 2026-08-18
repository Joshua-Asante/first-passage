**Theme:** _inbox
**Status:** AMBIGUOUS-HOLD — both named alternates fit (NEG and DEP-ZERO)
# Q-TRAINKILL-2 — bounded recovery + named alternate DGPs

**Verdict:** `AMBIGUOUS-HOLD`. Limb 1 did not fire (1 promotion; extremes still disagree). Limb 2: both `NEG` and `DEP-ZERO` fit.
**Date:** 2026-08-18
**Spend / K:** $0 / K=0
**Parent:** [`Q-TRAINKILL-2-bounded-recovery-alt-dgp.md`](../../../../docs/briefs/Q-TRAINKILL-2-bounded-recovery-alt-dgp.md)
**Prereg (hashed before TABLE.json was opened by the scorer):**
`86049b89b413b33430e7dfe31d9fc5de5cc46b81c0f23f3ea7877d78c7605b5d`

Reproduce:

```bash
python lab/analysis/_inbox/q_trainkill_2_2026-08/score_trainkill2.py
```

The runner prints the prereg sha256 **before** reading `TABLE.json`.

---

## Limb 1 — recovery

| id | Outcome |
|---|---|
| MSL-S2A | **promoted** — committed mean-R CIs long [−0.464, +0.144] · short [−0.287, +0.146]; event AMBIGUOUS both-arms (CI route did not fire; n<100) |
| Q-R2VBUCK-1 | still BOUNDED — ρ CI |
| Q-R2FLOW-1 | still BOUNDED — ρ CI |
| Q-R2AGRUN-1 | still BOUNDED — ρ CI |
| DL-1 | still BOUNDED — annSR/SPA |
| Q-CAPFLOW-1 | still BOUNDED — ρ CI |
| H-DSTRUCT-MNQ-1 | still BOUNDED — gateHit vs 0.50 |

n*=9 · n_bounded=6 · n_promoted=1.

| Object | g(0) | g(+0.10R) | Reading |
|---|---|---|---|
| Scored core | 0.0364 | 0.000961 | `MISCALIBRATED` |
| all-BOUNDED-at-ε | below | below | `MISCALIBRATED` |
| all-BOUNDED-at-1−ε | zero clears | bar stays below | `KILLS-INFORMATIVE` |

Extremes disagree → Limb 1 does **not** fire (prereg §D: promotion alone is not enough).

---

## Limb 2 — named alternates (scored-core only)

| DGP | g | Fits (≥0.05)? |
|---|---|---|
| `NEG` (μ=−0.10R, independence) | **0.239** | **yes** |
| `DEP-ZERO` (μ=0, Fréchet-hi) | **0.189** | **yes** |
| inherited zero (independence) | 0.0364 | no (disclosed; not a Limb-2 fire) |
| inherited bar (independence) | 0.000961 | no |
| Fréchet-lo (disclosed, not a fire) | 0.00208 | no |

S = {`NEG`, `DEP-ZERO`} → **`AMBIGUOUS-HOLD`**. Do not pick one after seeing g.

---

## What this does not license

- Quoting `NEG-FAMILIES` or `KILLS-INFORMATIVE-DEP` as the singleton class reading.
- Quoting `GATES-UNDERPOWERED` (bar still misses).
- Lowering any gate, or moving 0.05 / μ / the product after seeing g.
- A one-arm re-read of a both-arms cell.
- Translating the six remaining ρ/annSR/gateHit rows into R.
- Naming a third μ to break the tie.
