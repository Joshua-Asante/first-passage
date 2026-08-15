# Q-RAIL-1 F3 Step 3 / C3 — rung 1a (2026-07-17)

**Rung:** 1a pure transplant — venue edition on CME, **force-flat OFF**.  
**Note:** Operator labeled “Step 2, 1a”; files are CME `MYM1!` / `MNQ1!` → this is **C3 Step 3 rung 1a**, not Step-2 Pepperstone parity (already closed in [`STEP2_PARITY.md`](STEP2_PARITY.md)).

## Exports

| Leg | File | Chart |
|---|---|---|
| MYM | `Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-17_0fe15.csv` | CBOT_MINI:MYM1! |
| MNQ | `Striker_NAS100_MNQ_CME_MINI_MNQ1!_2026-07-17_f9473.csv` | CME_MINI:MNQ1! |

**Window (both):** ~2025-09 → 2026-07 (short panel — OK if 1b/1c use the **same** range).

## Config gate

| Check | MYM 1a | MNQ 1a |
|---|---|---|
| Force-flat / EOD Flat signals | **0** | **0** |
| Integer micro sizes | yes (e.g. 9 / 67 add) | yes (6, 5, …) |

## Headline metrics (CSV reconstruct @ $200K initial)

| Run | Trades | WR | PF | Net | maxDD% |
|---|---:|---:|---:|---:|---:|
| MYM 1a `0fe15` | 44 | 63.6% | 4.725 | $25,802 | 1.12 |
| MNQ 1a `f9473` | 45 | 55.6% | 4.003 | $14,538 | 0.82 |

## Transplant reads (same calendar window)

### MYM — vs PoR `15d8b` (prior MYM edition on MYM1!)

- Entries: **43 shared**; only 1a-only = `2026-07-17 09:45` (PoR ends 2026-06-30) → **tight**.
- Exits: not comparable 1:1 — PoR window still contains **EOD Flat** (force-flat was ON on that panel). 1a correctly has none.
- vs CFD-on-MYM1 `7127d`: entries similarly tight (+ Jul-17 tail); small exit-bar lags only.

**MYM 1a:** **PASS** as force-flat-OFF baseline (entry transplant tight on overlap).

### MNQ — vs CFD-on-MNQ1 `beabf` (locked CFD Pine on MNQ1!)

- Entries: **34 shared**, **11 only on MNQ edition**, **0 only on CFD** in-window.
- Most 1a-only entries fire while CFD is already **flat** (extra signals, not “CFD still in trade”). One overlap conflict: `2026-03-02 10:00` while CFD still long from 09:30.
- Dollar Net not comparable (integer MNQ sizing vs CFD equity sizing on same chart).

**MNQ 1a:** **PASS-with-Class-S caveat** — not bar-identical to CFD-on-MNQ1 (expected under Class-S / size→state; Step-2 already showed MNQ edition timing PASS vs CFD on Pepperstone). Use `f9473` as the **1a ladder baseline**, not as a CFD-identity proof.

## Ladder status

| Rung | Status |
|---|---|
| **1a** | **LANDING recorded** — FF OFF confirmed; MYM tight; MNQ baseline accepted w/ caveat |
| 1b | **OWED** — same charts/range, force-flat **ON** only |
| 1c | **OWED** — discharge costs/defaults on top of 1b |

Do not score full C3 / F3 PASS until 1b retention + 1c bands are in.
