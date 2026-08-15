# Q-TXG-1 Block 2 — election packet (Striker sibling-swap pair)

**Status:** ELECTED · 2026-08-12 · **operator election via task start** (design §5: operator elects ≤2 OPEN cells)
**Parent:** [design](lab/archive/../../docs/superpowers/specs/2026-08-11-transfer-expression-grid-design.md) §5 · [GRID_RESULTS](GRID_RESULTS.md) H_A OPEN n=25 · Block 1 PR [#754](https://github.com/Joshua-Asante/first-passage/pull/754)
**Spend:** $0 · K=0 · no PnL/return reads · no manifest · no scoring (Blocks 4–5 gated on operator native-TV exports)
**Authorizes:** cell PREREG freezes + port builds + RUNSPECs for the two cells below — **not** scoring, N-SURV, or CANDIDATE admission

---

## Ranking (design §5)

OPEN cells ranked by (fewest UNSCREENABLE inputs → same-underlying first → widest W-COST margin).
Compile fact: only **two** OPEN cells carry a mapped stop cell (ATR(11) MYM/MNQ committed). All other OPEN cells are `stop_cell: UNSCREENABLE`. Same-underlying Striker×{MYM,MNQ} are **WITHDRAWN(F1)**; Guardian×MGC is **PARKED(b8)** / pursuit SUBTRACT — not elected.

| Rank | Cell | Transfer | stop_map | cost_tax_r | qty | ENV-1 | Why elected |
|---|---|---|---:|---:|---:|---|---|
| **1** | `striker_nas100` × **MYM** | cross-underlying | 80 | 0.060R | 9 @ 0.37% | **OPEN** (power floor 0.0891) | Fully screened envelope; cleanest mapped OPEN |
| **2** | `striker` × **MNQ** | cross-underlying | 160 (raw 218.45) | 0.030R | 8 @ 0.70% | **OPEN-CONDITIONAL(power)** | Mapped sibling; power condition disclosed, not resolved |

**Operator election GO:** 2026-08-12 · recorded as *"operator election via task start"* in each cell PREREG header.

---

## Pre-committed lane rule (design §6 — written before results)

**Two consecutive elected-cell FALSIFIEDs force a re-argument of H_A before a third election.**
This pair is election #1 (two cells). If both falsify, do **not** elect a third OPEN cell from the Block-1 grid without reopening H_A. Registry rows + grid update still apply per cell.

---

## Cell PREREGs (freeze-first)

| # | Cell | PREREG |
|---|---|---|
| 1 | striker_nas100 × MYM | [`docs/briefs/pre-registration/2026-08-12-q-txg-1-striker-nas100-mym-cell-prereg.md`](lab/archive/../../docs/briefs/pre-registration/2026-08-12-q-txg-1-striker-nas100-mym-cell-prereg.md) |
| 2 | striker × MNQ | [`docs/briefs/pre-registration/2026-08-12-q-txg-1-striker-mnq-cell-prereg.md`](lab/archive/../../docs/briefs/pre-registration/2026-08-12-q-txg-1-striker-mnq-cell-prereg.md) |

Ordering defect this packet refuses to repeat: MGC cell PREREG was retroactive
([closure §4](lab/archive/../../docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md)).
**Both PREREGs freeze and commit before any port bytes or panel contact.**

---

## Explicitly not elected

- WITHDRAWN(F1) same-underlying redeploys (striker×MYM, striker_nas100×MNQ)
- PARKED(b8) / SUBTRACT Guardian×MGC (requires re-entry armor — not this GO)
- Any UNSCREENABLE-stop OPEN cell (ATR commit is a separate campaign)
