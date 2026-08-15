# Q-RAIL-1 F3 Step 3 / C3 — rung 1c (2026-07-17)

**Rung:** 1c = 1b + discharge-tier costs (Tradeify **$0.91** / MFFU **$0.95**).  
**Priors:** [`STEP3_1A.md`](STEP3_1A.md) · [`STEP3_1B.md`](STEP3_1B.md).

## Exports (inferred commission via exact $0.04/side×2×qty PnL delta)

| Leg | File | Inferred $/side | Firm path | Net |
|---|---|---:|---|---:|
| MYM | `…MYM1!_2026-07-17_d6502.csv` | **0.91** | Tradeify | $18,122 |
| MYM | `…MYM1!_2026-07-17_6610a.csv` | **0.95** | MFFU | $18,063 |
| MNQ | `…MNQ1!_2026-07-17_06861.csv` | **0.91** | Tradeify | $12,437 |
| MNQ | `…MNQ1!_2026-07-17_1f7f2.csv` | **0.95** | MFFU | $12,414 |

MYM: `d6502 − 6610a` PnL = **+$59.12** = `0.04 × 2 × Σqty` (byte-exact).  
MNQ: `06861 − 1f7f2` PnL = **+$23.04** = same law (note: MNQ hash order is opposite MYM — `1f7f2` is the **dearer** run).

## Mechanism

| Check | Result |
|---|---|
| Exit identity vs 1b (trade#, dt, signal) | **True** all four |
| Entry identity vs 1b | **True** (cost-only delta) |
| EOD Flat retained @ 15:45 | MYM 5 / MNQ 4 |

## Draft bands (vs 1b and vs 1a)

Thresholds: count ±30% · PF ≥ 0.7× · MaxDD ≤ 1.5×; investigate if PF ≥ 1.3× or MaxDD ≤ 0.5×.

| Run | vs 1b count/PF/DD | vs 1a count/PF/DD | Too-good? |
|---|---|---|---|
| MYM 0.91 | 1.00 / 0.95 / 1.03 — **PASS** | 1.00 / 0.76 / 1.06 — **PASS** | no |
| MYM 0.95 | 1.00 / 0.95 / 1.03 — **PASS** | 1.00 / 0.76 / 1.06 — **PASS** | no |
| MNQ 0.91 | 1.00 / 0.98 / 1.02 — **PASS** | 1.00 / 0.89 / 1.02 — **PASS** | no |
| MNQ 0.95 | 1.00 / 0.98 / 1.02 — **PASS** | 1.00 / 0.88 / 1.02 — **PASS** | no |

Net vs 1b retention ≈ **96.5–98.1%** (commission drag only — expected).

## C3 ladder verdict

| Rung | Verdict |
|---|---|
| 1a | LANDING — FF OFF; MYM tight; MNQ Class-S caveat |
| 1b | LANDING — FF @ 15:45 PASS; MYM retention 72.6% **AMBIGUOUS** vs C4 ~89% on short window |
| **1c** | **PASS** both cost paths — bands clear; no too-good triggers |

**C3 overall:** **PASS** (carry MYM 1b short-window retention caveat; does not block discharge-tier cost rung).

## F3 impact

Acceptance checklist C3 limb **discharged**. TV-native compile treated as **PASS-implied** (multi-rung Strategy Tester on MYM1!/MNQ1! produced these exports). → **F3 → PASS**.
