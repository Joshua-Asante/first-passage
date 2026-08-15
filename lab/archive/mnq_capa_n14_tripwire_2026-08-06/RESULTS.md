# Q-CAPA-1 Cap-spend — RESULTS: forward L1 `A` persists; Cap seat **spent**

**Status:** CLOSED — `RESOLVED` (W5) — Cap seat **marked spent** on this Route A cell; companion registered docs-only (Catalog stamp CLOSED = archive-owed HOLD).  
**§6 pre-registered expectation was Cap held (W2/W3) — that prediction was WRONG.** Recorded as a failed prediction, not retrofitted.  
**Date:** 2026-08-06 · **Pre-registration:** [`PREREG.md`](PREREG.md), frozen at **`022c17d`** — strictly before any forward-window quote. Cap-spend GO landed with Phase-0 (`d59abe3`).  
**Cost:** **$0.00.** Full-S1 `tbbo` estimate re-confirmed **$0.0000** / 20.73 GB / 259,177,803 records before the windowed forward pull.  
**`K_intrinsic = 1`** (Cap marked spent). `K_banked(MNQ)` disclosed from `discovery_manifests/` (does not gate — ADR 2026-08-04). Cap 1.0 → floor **0.650**, headroom **0.350**.  
**No `core/`, lock, allocation, `dd_protection`, lifecycle, Pine, rail, or `LEG_MAP` change.** No PF-CUSUM wire.

> ⚠ **Tripwire is a registered companion** (docs-only; not live-wired) —
> [`ADR 2026-08-06`](lab/archive/../../../docs/adr/2026-08-06-capa-tripwire-pfcusum-companion-registration.md).
> Cap spent means the Route A discovery seat is consumed by this cell — **not** that the
> monitor is live. Fire thresholds deferred; Call-1 / entry-filter authority not granted.
> FM-6 / brief §5: no gate conversion.

---

## 1. Verdict — frozen gates, precedence as listed

| # | Frozen trigger | Actual | Fired? |
|---|---|---|---|
| W0 | covered n < 30 | covered **255** | ✗ |
| W1 | coverage < 90% | **100.0%** (255/255) | ✗ |
| W2 | CI includes 0 | CI **[−0.028061, −0.017558]** excludes 0 | ✗ |
| W3 | \|Δ\| ≤ placebo p95 | \|−0.022928\| = **0.022928** > **0.004356** | ✗ |
| W4 | \|Δ\| < 0.00714 **or** halves disagree | \|Δ\| **0.022928** ≥ 0.00714; H1/H2 same sign | ✗ |
| **W5** | clear of W0–W4 | **all clear** | **✓ `RESOLVED`** |

| | value |
|---|---|
| ORB triggers (N14 S2) | **255** |
| Matched controls | **1,275** |
| Forward window | **`[t, t+60s)`** |
| TBBO quotes measured | **4,804,045** |
| Coverage | **255/255 = 100.0%** |
| mean `A_trigger` (fwd) | **−0.022719** |
| mean `A_control` (fwd) | **+0.000210** |
| **difference** | **−0.022928** |
| 95% session-block CI (10,000 reps, seed **20260806**) | **[−0.028061, −0.017558]** |
| placebo \|.\| p95 (1,000 within-session shuffles, same seed) | **0.004356** |
| placebo p_emp | **0.000** (0 of 1,000) |
| Magnitude floor | **0.00714** (0.05 contracts @ L1 median 7) |
| H1 / H2 | **−0.026618** [−0.033343, −0.019999] (n=127) / **−0.019267** [−0.027030, −0.010934] (n=128) |
| **cap_spent** | **True** |

**Sign:** same as N14 — negative = more resting size on the side price is breaking through, now measured **after** the touch. Forward \|Δ\| ≈ **2.4×** N14’s pre-touch \|Δ\| (−0.009367). At median L1 total **7**, ≈ **0.16 contracts** of mean imbalance (still small in absolute contracts; precisely estimated).

---

## 2. Disclosed context — L1 census + degraded days

| | value |
|---|---|
| L1 total size p05 / p50 / p95 | **2 / 7 / 17** |
| Distinct `A` values | **2,735** |
| Frac in a tie group | **99.98%** |
| Exactly `A` = 0 | **14.56%** |

**Degraded Databento days retained and disclosed** (not re-cut — FM-3): **2025-09-17**, **2025-11-28**, **2026-03-16**, **2026-04-10**. Same class as N14’s retention doctrine.

---

## 3. What this does NOT say

- **Nothing about ORB winners vs losers** — FM-1 held; no outcome column read.  
- **Does not wire** PF-CUSUM, live monitors, or entry filters.  
- **Does not discharge** N14’s level-proximity caveat (PROX chain STOPPED B/1; caveat remains disclosure).  
- **Does not** license MBP-10 escalation or a second Cap cell.  
- **Does not** reopen ORB payability / unpark.

---

## 4. Cap seat

**Spent** on this single Route A cell (`K_intrinsic=1`). Re-proposal of another Cap-seat discovery cell on MNQ needs a fresh operator reservation — this seat is no longer idle.

---

## 5. Reproduce

```bash
# Freeze precedes quotes
git log --oneline -- lab/archive/mnq_capa_n14_tripwire_2026-08-06/PREREG.md

# Tests before quotes (expect 11 passed)
.venv-research/Scripts/python.exe -m pytest \
  lab/archive/mnq_capa_n14_tripwire_2026-08-06/test_capa_lib.py -q

# Single run (requires local quotes_fwd.parquet)
.venv-research/Scripts/python.exe lab/archive/mnq_capa_n14_tripwire_2026-08-06/run_capa.py
```

Machine record: [`RESULTS.json`](RESULTS.json).
