# ORB MNQ v0.2 — clock audit + Tradeify k-grid scorecard

**Date:** 2026-07-31
**Export:** `ORB_MNQ_v0.2_CME_MINI_MNQ1!_2026-07-31_6ce33.csv` (n=513 trades, 2024-07-30→2026-07-30)
**Harness:** [`run_v02_clock_kgrid.py`](run_v02_clock_kgrid.py)
**Class:** structural / Notice-phase. No Pine edit, no K spend, no campaign.

---

## 1. EOD clock audit

### 1.1 What v0.2 documents

| Path | Order bar (ET) | Fill (ET) | Binding |
|---|---|---|---|
| Full session | 15:45 | **16:00** open | envelope E1 / CME RTH end |
| Reduced session | 12:30 | **12:45** open | Tradeify half-day flat ≤12:59 |

Prior fill-realism audit on v0.1 (`RESULTS_tv_export_realism.md`) measured TV EOD fills at the **16:00 open** (vs harness 15:45 close; median gap 1 tick).

### 1.2 What this export prints

- Duration identity `exit_tod == entry_tod + dur×15`: **PASS** (bar-open labels are internally consistent; timezone is ET — entries cluster at 10:00 post-OR, share=73.9%).
- Non-half EOD exit labels: **274** at 16:00; half-day EOD: **15** at 12:45; **0** other (neither modal-full nor half).
- Half-day EOD ⊆ calendar early-close: **PASS**.
- Full-session EOD ∩ calendar early-close: **empty (PASS)**.
- Commission unique on exits: [1.22] (⇒ $0.61/side Bulenox — matches Pine default, **not** Tradeify).

### 1.3 Verdict

**Half-day path matches v0.2.** All 15 reduced-session EODs fill at 12:45; calendar flags line up; stopped-out early-close days never leak an overnight EOD.

**Full-session path PASS vs documented 16:00.** Modal full-session EOD label is 16:00 (documented fill open).

D5 clock pin confirmed on this export. Half-day cohort should remain byte-stable vs the pre-D5 2026-07-30 panel; full-session EOD cohort is the expected delta. k-grid below is eligible for geometry read (still not a Stage-7/8 substitute).

### 1.4 Early-close trade days in panel

| date | signal | exit | pnl (Bulenox) |
|---|---|---|---:|
| 2024-09-02 | Sx | 10:30 | -64.72 |
| 2024-11-28 | EOD | 12:45 | 0.28 |
| 2024-11-29 | EOD | 12:45 | 147.28 |
| 2024-12-24 | EOD | 12:45 | 124.28 |
| 2025-01-20 | Sx | 11:15 | -1.72 |
| 2025-02-17 | EOD | 12:45 | -11.22 |
| 2025-05-26 | EOD | 12:45 | -42.72 |
| 2025-07-03 | EOD | 12:45 | 136.78 |
| 2025-07-04 | EOD | 12:45 | -65.22 |
| 2025-09-01 | EOD | 12:45 | 12.28 |
| 2025-11-27 | EOD | 12:45 | -29.72 |
| 2025-11-28 | EOD | 12:45 | -54.22 |
| 2025-12-24 | EOD | 12:45 | 75.78 |
| 2026-01-19 | EOD | 12:45 | 178.78 |
| 2026-02-16 | Lx | 10:30 | -182.72 |
| 2026-05-25 | EOD | 12:45 | 9.28 |
| 2026-06-19 | EOD | 12:45 | -16.22 |
| 2026-07-03 | EOD | 12:45 | -39.22 |

### 1.5 ADR §4 **T1** trigger evaluation

T1 asks whether correcting the clock moved full-session cohort P&L **down**, by roughly what the native harness predicted. It is a **halt condition, not a verdict on the candidate** — a contradiction means engine and Pine disagree, which is a defect in the measurement rather than a result about ORB.

**VERDICT: PASS** — $-5.03/day is down and within an order of magnitude of the predicted $-3.17/day.

| | |
|---|---|
| Baseline | baseline export `ORB_MNQ_v0.2_CME_MINI_MNQ1!_2026-07-30_8ef7d.csv` (2024-07-30→2026-07-30) |
| Comparison mode | `paired` (per-common-day) |
| Predicted Δ | **$-3.17/day** (band [$-31.70, $-0.32]) |
| Observed Δ | **$-5.03/day** (total $-2,488 over 495 days) |
| Full-session cohort | baseline 495 trades / $8,312 → observed 495 / $5,824 |
| Days with a different P&L | 286 of 495 |
| Worst / best single-day Δ | $-352 / $+307 |
| Early-close control cohort | unchanged (PASS) |

Reading the controls: D5 moved the **full-session** bounds only, so the early-close cohort is expected byte-stable across the two panels — if it moved, the exports differ by something other than the clock and no clock delta is attributable. The correct clock should also admit **slightly more** trade days, since a day whose only OR breach falls in the final 30 minutes exists on the 16:00 clock and not on the 15:30 one.

**Limits of this check, each load-bearing:**

1. The predictor **$-3.17/day** is the native harness's **full-window** (2019-05+) mean, transcribed from ADR §4. This export is a ~2y window, and the per-day delta is not guaranteed to be regime-stable. The order-of-magnitude band is what absorbs that mismatch — it is deliberately wide, and narrowing it is a falsifier edit that §5 forbids outside a superseding ADR.
2. Baseline was paired per-day against the supplied pre-D5 export, which is the stronger form of this check.
3. A `PASS` here clears the halt only. It **freezes no k policy** and re-scores no gate — that still needs an explicit operator call.

---

## 2. Tradeify-costed structural scorecard + k grid

Recost: `pnl_tfy1 = pnl_bulenox − $0.60` per contract ($0.91 − $0.61) × 2 sides. At size k: `pnl_k = k × pnl_tfy1` (slip already in prices; commission scales).

### 2.1 k=1 headlines (this window)

| | Bulenox (as exported) | Tradeify recost |
|---|---:|---:|
| N | 513 | 513 |
| WR | 43.27% | 43.08% |
| PF | 1.113 | 1.107 |
| Net | $6,298.14 | $5,990.34 |
| Mean / trade | $12.28 | $11.68 |
| Max DD (trade-close) | $-6,443.70 | $-6,464.70 |
| RF | 0.98 | 0.93 |

### 2.2 k grid (Tradeify RT)

Trail buffer reference: **$3,000** (Select 100K floor geometry). Winning-day floor: **$200**. Equity path starts at $100k. `headroom` = $3k + worst_day (>0 ⇒ that day alone cannot bust a fresh peak). `trail episodes` = distinct times the trade-close equity curve went ≥$3k under its peak (EOD proxy — not real-time intraday breach).

| k | Net | PF | mean | maxDD $ | RF | worst day | headroom vs $3k | single-day bust? | days ≥$200 | win-day % | trail episodes |
|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---:|---:|---:|
| 1 | $5,990 | 1.107 | $11.68 | $-6,465 | 0.93 | $-784 | $2,216 | no | 21.1% (108) | 43.1% | 5 |
| 2 | $11,981 | 1.107 | $23.35 | $-12,929 | 0.93 | $-1,568 | $1,432 | no | 33.3% (171) | 43.1% | 10 |
| 3 | $17,971 | 1.107 | $35.03 | $-19,394 | 0.93 | $-2,351 | $649 | no | 37.0% (190) | 43.1% | 13 |
| 4 | $23,961 | 1.107 | $46.71 | $-25,859 | 0.93 | $-3,135 | $-135 | YES | 38.6% (198) | 43.1% | 23 |
| 5 | $29,952 | 1.107 | $58.39 | $-32,323 | 0.93 | $-3,919 | $-919 | YES | 40.2% (206) | 43.1% | 27 |

### 2.3 Reading

- **Payability is not cured by k.** Days ≥$200 rises with k, but the construct remains **one entry/day**; at k=1 only a minority of days clear $200. Larger k scales both the winning-day mass and the left tail.
- **Single-day trail headroom (this window's worst day):** k ∈ {1, 2, 3} keep worst-day > −$3,000.
- **Single-day bustable from a fresh peak:** k ∈ {4, 5} (worst day × k ≤ −$3,000) — matches the Pine tooltip.
- **Path DD ≠ one-day DD.** Even at k with positive single-day headroom, the trade-close equity curve can still print ≥$3k drawdown episodes (see episode column). Real Tradeify breach is stricter still (intraday).
- **This is not a Stage-7/8 substitute.** Full-window Tradeify DSR already **FAIL**ed at $0.91/side on the native harness (`RESULTS_stage7.md`); this scorecard is a ~2y recent window for sizing geometry only.
- **Clock:** PASS on this export — dollar paths above are eligible for k-geometry read. Still freeze no policy without an explicit operator call.

### 2.4 Side / exit / year (Tradeify k=1)

| slice | n | WR | mean | net |
|---|---:|---:|---:|---:|
| long | 272 | 47.4% | $11.93 | $3,244 |
| short | 241 | 38.2% | $11.40 | $2,746 |
| exit=EOD | 289 | 76.5% | $189.27 | $54,699 |
| exit=Lx | 110 | 0.0% | $-223.83 | $-24,621 |
| exit=Sx | 114 | 0.0% | $-211.29 | $-24,087 |
| year=2024 | 110 | 44.5% | $47.33 | $5,206 |
| year=2025 | 256 | 41.0% | $12.56 | $3,215 |
| year=2026 | 147 | 45.6% | $-16.54 | $-2,431 |

---

## 3. Disposition

1. **Clock:** PASS — modal full-session EOD matches the D5 contract (16:00). Half-day path clean. **ADR §4 T1: PASS** — $-5.03/day is down and within an order of magnitude of the predicted $-3.17/day (§1.5).
2. **k policy:** grid above is geometry-ready; freeze still requires an explicit operator call. Pine tooltip's k=2 peak / k≥4 bust band is **directionally reproduced** on this window's worst day when that band appears in the table.
3. **Not in scope here:** BE/targets/DOW/OR-length (pre-killed or pre-reg-voiding); payability redesign (needs a different construct or book role).

Reproduce:

```bash
python lab/analysis/orb_mnq_2026-07/run_v02_clock_kgrid.py \
  --csv lab/analysis/orb_mnq_2026-07/inputs/ORB_MNQ_v0.2_CME_MINI_MNQ1!_2026-07-31_6ce33.csv \
  --baseline-csv lab/analysis/orb_mnq_2026-07/inputs/ORB_MNQ_v0.2_CME_MINI_MNQ1!_2026-07-30_8ef7d.csv
```

Exit code is **2** when ADR §4 T1 returns `HALT`, `0` otherwise.

