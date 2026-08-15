# Tradeify Select Flex 50K — bust-cut Tests 1+2 (2026-07-11)

**DIAGNOSTIC ONLY.** R6 futures-prop NO-GO stands. No change to `ACTIVE_FIRM`,
locked params, or ADRs.

## Scope

Pre-registered bust-cut recommendation order, Select Flex **50K**, geometry-only,
C2-off — same method as [`../tradeify_futures3_remc_2026-07-11/`](../tradeify_futures3_remc_2026-07-11/).

| Test | Book | Allocations |
|---|---|---|
| 1 | Drop Aegis → MYM + MNQ | DJ30 0.70% / NAS 0.37% |
| 2 | Keep 3 legs, Aegis 0.5× | Aegis **0.75%** / DJ30 0.70% / NAS 0.37% |

Aegis input for Test 2: new export `…_5274c.csv` (not prior `ae744`).

## Acceptance screen (pre-registered, not a lock)

- **A:** bust ≤ 5.0% and p99 DD ≤ 5.0%
- **B:** Aegis bust_attr ≤ 55% *or* Aegis dropped
- **C:** median days-to-pass ≤ 150

## Aegis export inventory (5274c vs ae744)

| | ae744 (prior remc) | 5274c (new) |
|---|---|---|
| N | 152 | 152 |
| Span | 2020-02-24→2026-07-01 | same |
| PF (static $200K) | 2.042 | **2.212** |
| Net static @200K | $70,817 | **$49,122** (−31%) |
| Exit qty mean | 11.36 | **7.29** (−36%) |
| Full-stops after decompound | 11 → 1R $2,913 | **0** → pin **fallback median $167** |

**Material change:** same trade count/span, but 5274c is a smaller-sized export.
Primary Test 2 under the prior remc pin method therefore hits the zero-full-stop
median fallback and inflates scale ~9× — not a clean 0.5× risk cut. Sensitivities
2b/2c in `RESULTS.md` isolate the intended haircut.

## Headline (Select Flex 50K geometry-only)

| Test | Bust | p99 | Med | AegAttr | A | B | C | ALL |
|---|---|---|---|---|---|---|---|---|
| Baseline 3-leg 1.50% | 10.33% | 5.06% | 106 | 71.2% | — | — | — | — |
| **1** Drop Aegis | **0.76%** | **3.86%** | 222 | dropped | P | P | F | **FAIL** |
| **2** 5274c @ 0.75% (method pin) | 39.43% | 9.82% | 21 | 96.9% | F | F | P | **FAIL** (pin artifact) |
| 2b ae744 @ 0.75% | 2.02% | 4.10% | 152 | 47.8% | P | P | F | FAIL (C by 2d) |
| 2c 5274c size-adj 1R | 1.28% | 4.01% | 151 | 42.1% | P | P | F | FAIL (C by 1d) |

Neither primary test clears the pre-reg screen. Dropping Aegis clears bust/DD but
median days-to-pass blows out. A clean 0.5× Aegis haircut nearly clears A+B but
misses C by 1–2 days.

## Driver

[`run_bustcut_tests.py`](run_bustcut_tests.py) → [`RESULTS.md`](RESULTS.md).
