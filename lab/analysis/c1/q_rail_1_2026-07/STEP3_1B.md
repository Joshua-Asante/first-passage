# Q-RAIL-1 F3 Step 3 / C3 — rung 1b (2026-07-17)

**Rung:** 1b = 1a + **force-flat ON** only.  
**1a baselines:** [`STEP3_1A.md`](STEP3_1A.md) (`0fe15` / `f9473`).

## Exports

| Leg | File | EOD Flat exits |
|---|---|---:|
| MYM | `Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-17_4829a.csv` | 5 |
| MNQ | `Striker_NAS100_MNQ_CME_MINI_MNQ1!_2026-07-17_54444.csv` | 4 |

All EOD flats print at **15:45** (America/New_York bar) — matches Q-RAIL E1 / D4.

## Mechanism check (load-bearing)

| Check | MYM | MNQ |
|---|---|---|
| Same calendar window as 1a | yes | yes |
| Entry datetime set vs 1a | **identical** (44 / 45) | **identical** (45 / 45) |
| Trade count vs 1a | 44 = 44 | 45 = 45 |
| Force-flat active | yes (5× `EOD Flat`) | yes (4× `EOD Flat`) |

Delta is exit-path only → clean force-flat attribution (not a signal-port miss).

## Retention (Net 1b / Net 1a)

| Leg | 1a Net | 1b Net | Retention | Historical expect |
|---|---:|---:|---:|---|
| **MYM** | $25,802 | $18,728 | **0.726 (72.6%)** | ~**89%** (C4 full-history) |
| **MNQ** | $14,538 | $12,674 | **0.872 (87.2%)** | ~**unchanged** (~100%) |

| Leg | 1b PF | 1b maxDD% |
|---|---:|---:|
| MYM | 3.777 | 1.15 |
| MNQ | 3.618 | 0.82 |

**MYM note:** retention **below** the ~89% C4 reference on this **short** window (2025-09→2026-07). Clipped legs are mostly **open winners** at 15:45 (e.g. 2025-11-25 / 2026-02-06 pyramid stacks). Not scored as port defect — entries match 1a. Treat as **window-specific force-flat cost**; a full-history 1a/1b pair would be needed to re-test the ~89% figure.

**MNQ note:** mild haircut (four EOD winner clips); closer to “mostly unchanged” than MYM.

## Verdict

| Item | Score |
|---|---|
| 1b force-flat wiring / E1 15:45 | **PASS** both legs |
| 1b retention vs C4 ~89% (MYM) | **AMBIGUOUS on short window** (0.726) — mechanism OK |
| 1b MNQ ≈ unchanged | **PASS-with-mild-haircut** (0.872) |

## Ladder status

| Rung | Status |
|---|---|
| 1a | LANDING ([`STEP3_1A.md`](STEP3_1A.md)) |
| **1b** | **LANDING** (this file) |
| 1c | **OWED** — discharge costs/defaults on top of 1b (same window) |
