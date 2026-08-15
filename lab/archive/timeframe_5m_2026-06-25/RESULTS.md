# 5-Minute Timeframe Prototypes — RESULTS

- **Date:** 2026-06-25
- **Disposition:** CLOSED — NO-GO — 5m conversion degrades all four strategies. Original: NO-GO. The 5m conversion degrades all four strategies and the portfolio. The locked 15m timeframe is vindicated. Exploratory — no lock implication; locked strategies/constants untouched.
- Spec: [2026-06-25-5m-timeframe-prototypes-design.md](lab/archive/../../docs/superpowers/specs/2026-06-25-5m-timeframe-prototypes-design.md) · Plan: [2026-06-25-5m-timeframe-prototypes.md](lab/archive/../../docs/ltm/superpowers/plans/2026-06-25-5m-timeframe-prototypes.md) · PREREG: [PREREG.md](PREREG.md)

## Headline

Every 5m prototype is **worse** than its locked 15m original on the pre-registered read-direction. None helped. The portfolio re-MC blows both FXIFY lock gates by a wide margin (BUST 14.2% vs 0.17%; p99 DD 8.0% vs 4.37%). Two distinct mechanisms, both adverse:

- **Guardian & Aegis** (similar/higher trade count): finer entries inject **noise** — win-rate and PF fall, drawdown rises 2–6×.
- **Striker DJ30 & NAS100** (trade count *collapses* 4–5×): the ATR-expansion breakout filter, kept on native 5m volatility, rarely fires; the **pyramid pathway — the Strikers' entire profit engine (88–94% of P&L on 15m) — nearly dies** (adds: DJ30 27→2, NAS100 33→1). NAS100 flips net-negative.

## Method (per reconcile skill)

- **Matched window = intersection** of each pair. The 5m protos run from **2020**; the 15m baselines from **2022** — so both sides are clipped to their overlap (the plan assumed proto ⊆ baseline; reality is the reverse). Full-2020 5m span shown as a secondary row.
- **Static-$200K basis** (`Net P&L % / 100 × $200K`), not TV's compounded cumulative (trap #9). DD% = MaxDD / $200K.
- **Anchor cross-check (validation):** Guardian 15m full window → **N=203 (exact), WR 22.17% (exact)** vs the CLAUDE.md anchor. PF 3.447 vs 3.750 is the static-vs-compounded basis difference only — parsing is sound.
- Harness: `run_task12.py` over `io_tv`/`metrics`/`remc` + core MC kernel. 5m CSVs in `data/` (gitignored).

## Per-strategy (matched window, static-$200K)

| Strategy (window) | TF | N | PF | WR | Net | MaxDD | DD% | RF | pyramid adds |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|
| **Guardian** XAUUSD (2022-01→2026-05) | 15m | 203 | 3.447 | 22.2% | $209,060 | $9,320 | 4.66% | 22.43 | — |
| | **5m** | 228 | **2.628** | **16.7%** | **$162,520** | **$17,280** | **8.64%** | **9.41** | — |
| **Striker DJ30** US30 (2022-01→2026-04) | 15m | 218 | 2.662 | 65.1% | $32,780 | $1,440 | 0.72% | 22.76 | 27 |
| | **5m** | **46** | 2.737 | 71.7% | **$7,400** | $1,260 | 0.63% | **5.87** | **2** |
| **Striker NAS100** NAS100 (2022-01→2026-04) | 15m | 196 | 1.598 | 55.6% | $25,440 | $9,220 | 4.61% | 2.76 | 33 |
| | **5m** | **27** | **0.120** | **25.9%** | **−$14,640** | **$14,840** | **7.42%** | **−0.99** | **1** |
| **Aegis** USDJPY (2022-01→2026-05) | 15m | 124 | 3.711 | 37.9% | $11,060 | $660 | 0.33% | 16.76 | — |
| | **5m** | 120 | **1.089** | 35.0% | **$820** | **$4,320** | **2.16%** | **0.19** | — |

(Full-2020 5m span is uniformly equal-or-worse than the matched window — see `run_task12.py` output.)

## Pre-registered read-direction verdicts

| Strategy | Verdict | Why |
|---|---|---|
| Guardian | **HURTS** | PF 3.45→2.63, RF 22.4→9.4, MaxDD 4.66%→**8.64%** (breaches 5% standalone). More trades, lower quality. |
| Striker DJ30 | **HURTS** (portfolio) | Per-trade edge *survives* (PF 2.66→2.74, WR↑), but frequency 218→46 and pyramid 27→2 collapse Net −77% / RF 22.8→5.9. |
| Striker NAS100 | **HURTS** (severe) | PF 1.60→**0.12**, Net **+$25.4K → −$14.6K**. Frequency 196→27, pyramid 33→1. Strategy destroyed. |
| Aegis | **HURTS** | PF 3.71→1.09 (≈break-even), Net −93%, MaxDD 0.33%→2.16% (6.5×). Edge evaporates. |
| **Portfolio** | **HURTS** | Both lock gates blown (below). |

Unanimous. The granularity question is answered: **no.**

## Descriptive portfolio re-MC (NOT a lock gate)

5m streams through the core MC kernel at locked allocations + dd_protection (1.5%/0.40×):

| Window | PASS | BUST | p99 DD |
|---|--:|--:|--:|
| Locked anchor (15m, 2022-26) | 99.83% | 0.17% | 4.37% |
| **5m, matched 2022-26** | **85.79%** | **14.21%** | **7.99%** |
| 5m, full 2020-26 (incl. chop) | 78.27% | 21.73% | 8.58% |

Both gates breach by a wide margin. (Striker/NAS100 1R fell back to median-loss on thin full-stop cohorts, so their MC normalization is soft — but the breach is dominated by Guardian + Aegis drawdown, which do **not** fall back, so the direction is unambiguous.)

## Caveats (honest)

- **1R fell-back** (Striker, NAS100): <5 full stops → median-loss proxy (`portfolio_mc_1r_fallback_trap`). Softens those two strategies' re-MC normalization only; conclusion unchanged.
- **PF basis**: static-$200K (challenge-correct) vs TV compounded — explains the anchor PF 3.45 vs 3.75; internal 15m-vs-5m deltas are same-basis and valid.
- **NAS100 thin panel** (39 trades / 78 rows) is below the harness's 100-row floor; the inventory confirmed it is **complete** (full 2020-26 span), not truncated — the thin count *is* the finding.
- **`request.security` 15m-ATR** ran natively on TV (TV is the arbiter), so this is not an offline fill-port; still, the result's mechanism (Striker frequency collapse) is a *design consequence* of keeping the ATR-expansion signal on native 5m volatility, not a verified bug. If ever revived, that one choice is the first thing to probe.

## Disposition

**5m timeframe: NO-GO / CLOSED.** The locked 15m timeframe is the right choice for all four strategies — it is not an unexamined default. Re-opening would require a *different* conversion hypothesis (e.g. running the Striker expansion filter on 15m-`request.security` volatility instead of native 5m), not a re-run of this one. No lock implication; no locked artifact was touched.
