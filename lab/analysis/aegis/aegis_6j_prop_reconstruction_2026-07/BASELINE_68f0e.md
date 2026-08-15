# Stage-0 baseline — 68f0e (2026-07-16) — ENVELOPE-YES

**CSV:** `baseline_fill1600_cap8_c310_2026-07-16_68f0e.csv`  
**Source:** `Downloads/Aegis_JPY-Futures_v0.3_PROTOTYPE_(MJY_6J)_CME_6J1!_2026-07-16_68f0e.csv`  
**SHA256:** `056186A2BAF14E19E795FAEFACEFDD332ACC95C35CCDBEA7BBD2850F4E7911AD`  
**Checker:** `stage0_baseline_check.py`  
**Supersedes:** `BASELINE_3cd61.md` (cap=12 FAIL)

## Envelope gates (pre-reg Stage-0)

| Gate | Result |
|---|---|
| (a) overnight = 0% | **PASS** |
| (a2) fills ≤ 16:00 ET | **PASS** (latest 16:00; 13 at 16:00; 0 after) |
| `max_contracts` ≤ 8 | **PASS** (max qty 8; 0 trades >8; mean 7.96) |
| N ≥ 80 | **PASS** (130) |

**Verdict: Stage-0 ENVELOPE-YES — Wave-1 authorized.**

## Headline

| Metric | Value |
|---|---:|
| N | 130 |
| Span | 2022-01-12 → 2026-07-15 |
| Net | +$22,258.00 |
| PF | 1.912 |
| WR | 35.38% |
| maxDD ($100K cum) | −3.12% |
| mean / max qty | 7.96 / **8** |
| EOD Flat | 17 exits · +$16,694.25 (**75.0%** of net) |
| Best day | 2023-03-08 · $3,150.40 · **14.2%** of net |

## vs prior exports

| Export | Cap | Net | PF | Envelope |
|---|---:|---:|---:|---|
| J1 (ref) | 12 | +$39,056 | 2.318 | self-funded / $1.30 |
| 3cd61 | 12 | +$31,386 | 1.932 | FAIL cap |
| **68f0e** | **8** | **+$22,258** | **1.912** | **PASS** |

Cap 12→8 cut net ~29% vs 3cd61 at same EOD/settings family (near-linear in size). EOD Flat still carries most of the edge (~75%).
