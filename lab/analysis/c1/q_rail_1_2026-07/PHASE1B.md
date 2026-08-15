# Q-RAIL-1 Phase 1b — MNQ re-author + D1–D5 apply (operator GO)

**Date:** 2026-07-17  
**Authority:** operator "go for it" after Phase 1 inventory  
**Driver:** [`reauthor_editions.py`](reauthor_editions.py) · hashes [`phase1b_reauthor_hashes.json`](phase1b_reauthor_hashes.json)

## Done

| Item | Result |
|---|---|
| MNQ re-author from `striker_nas100_v1.pine` | **DONE** → `striker_nas100_v1_mnq.pine` |
| MYM pin reconcile | Prior pin unrecoverable; applied D1–D5 to on-disk edition + **re-pin** |
| D1 commission | **0.91** (Tradeify); MFFU 0.95 = TV override note in FUTURES_LOCK |
| D2 microCap | **80** |
| D3 accountSize | **100000** |
| D4 EOD | **15:45 ET** bar → ~16:00 fill (E1 / inside MFFU 16:10) |
| D5 day-stop | MYM **−1.15** retained; MNQ source **−1.5** carried |
| `pine_check.py` | **OK** both editions |
| PORT_MANIFEST | MNQ `a67fd3b4…` · MYM `f89178d2…` |
| FUTURES_LOCK sheets | rewritten for discharge-tier constants |

## Acceptance progress

| Checklist item | Status |
|---|---|
| TV-native compile on MYM1! / MNQ1! 15m | **PASS-implied** — multi-rung CME Strategy Tester exports (1a–1c) |
| Per-candle timing parity vs CFD (force-flat OFF) | **PASS** — MNQ clean; MYM **PASS-via-operator-override** ([`STEP2_PARITY.md`](STEP2_PARITY.md)) |
| C3 attribution (or successor acceptance) | **PASS** — 1a/1b/1c ([`STEP3_1A.md`](STEP3_1A.md), [`STEP3_1B.md`](STEP3_1B.md), [`STEP3_1C.md`](STEP3_1C.md)); MYM 1b retention caveat carried |

**Step-2 override (operator 2026-07-17):** MYM extra entry after T19 on US30 = size→day-stop coupling (larger CFD size soft-halts; MYM still free) — not a port defect. Exit-bar lags T9/T11/T12 absorbed under same override. Evidence: corrected CFD `30a8e` / `4709d` vs venue `15aef` / `2d574`.

F3 → **`PASS`** (locate + re-param + Step-2 + C3 + compile-implied cleared).
