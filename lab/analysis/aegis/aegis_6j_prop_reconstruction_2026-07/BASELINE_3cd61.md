# Stage-0 baseline — 3cd61 (2026-07-16)

**CSV:** `baseline_fill1600_cap8_c310_2026-07-16_3cd61.csv`  
**Source:** `Downloads/Aegis_JPY-Futures_v0.3_PROTOTYPE_(MJY_6J)_CME_6J1!_2026-07-16_3cd61.csv`  
**SHA256:** `749B2DF9E88FD446624AE12C6233D4BE8E72E88CF3E79010B4ABA54CAA64E56B`  
**Checker:** `stage0_baseline_check.py`

## Headline

| Metric | Value |
|---|---:|
| N | 130 |
| Span | 2022-01-12 → 2026-07-15 |
| Net | +$31,385.85 |
| PF | 1.932 |
| WR | 35.38% |
| maxDD ($100K cum) | −3.55% |
| mean / max qty | 11.28 / **12** |
| EOD Flat | 17 exits · +$22,972.20 (**73.2%** of net) |
| Best day | 2025-02-03 · $3,600.60 · **11.5%** of net |
| Latest exit clock | **16:00:00** (13 at exactly 16:00; 0 after) |

## Envelope gates (pre-reg Stage-0)

| Gate | Result |
|---|---|
| (a) overnight = 0% | **PASS** |
| (a2) fills ≤ 16:00 ET | **PASS** (F1 semantics OK at pine trigger 15:45) |
| `max_contracts` ≤ 8 | **FAIL** — max qty **12** (v0.3 default); 118/130 trades qty>8 |
| N ≥ 80 | PASS |

**Verdict:** Stage-0 **NOT envelope-complete** for Wave-1. Re-export with **Max Contracts = 8** (and confirm commission $3.10). Keep EOD Cutoff **15:45** (fill ≤16:00) — that part cleared.

## vs J1

J1: n=129 / PF 2.318 / net +$39,056 / EOD ~60% of net / cap 12 / commission $1.30 placeholder.  
This export: similar N/span, lower PF/net, higher EOD share of net, still cap 12. Net Δ ≈ −$7.7K is consistent with tighter EOD (15:45 vs J1 16:30) and/or $3.10 commission — do not attribute until cap-8 re-export isolates variables.
