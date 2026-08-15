# Q-CAPA-1 — Cap-spend PREREG: does forward L1 `A` at ORB triggers persist?

**Status:** `FROZEN — CAP-SPEND GO ISSUED; FORWARD PULL AUTHORIZED UNDER THIS FREEZE.`  
**Date:** 2026-08-06  
**Phase-0:** [`PHASE0.md`](PHASE0.md) (`CHARTER-CLEARS`)  
**Parent brief:** [`docs/briefs/Q-CAPA-1-cap-seat-route-a-n14-tripwire.md`](lab/archive/../../../docs/briefs/Q-CAPA-1-cap-seat-route-a-n14-tripwire.md)  
**N14 parent:** [`../mnq_orb_flow_substrate_2026-08-05/`](lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/) (`RESOLVED` W1)  
**Operator Cap-spend GO:** 2026-08-06 — *"affirm charter, commit, then proceed with next steps."*  
**Cost so far:** **$0.00** (charter + freeze). Full-S1 `tbbo` estimate at N14: **$0.0000**; re-estimate before pull.  
**`K_intrinsic = 1`** if Cap is marked spent on accept. `K_banked(MNQ)` disclosed at run time from `discovery_manifests/` (does not gate — ADR 2026-08-04). Cap 1.0 → floor **0.650**, headroom **0.350**.

Frozen before any forward-window book-state quantity exists for this construct.

---

## §0 — Rule-0 reads (this freeze)

| Source | What it pins |
|---|---|
| [`PHASE0.md`](PHASE0.md) | C0–C11 charter; Cap-spend GO; magnitude floor; forward window |
| N14 [`PREREG.md`](lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/PREREG.md) / [`RESULTS.md`](lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md) | Event set, signed `A`, ToD controls, FM-1, watchlist disposition |
| N14 [`pull_windows.py`](lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/pull_windows.py) | Pre-touch only (`[t−60s, t)`); **does not** satisfy C3 |
| MNQ **F2 GUARD** | No outcome joins |
| Avenue A Route A + checklist ≥5 s | Survivor-tied; horizon floor met by H=60 s |

---

## §1 — Question

Does mean signed L1 asymmetry `A` over the **60 s after** ORB-MNQ-1’s frozen triggers differ from ToD-matched same-session controls with CI excluding 0 and beating within-session placebo — enough to mark the Cap seat spent on this Route A tripwire candidate — or is Cap correctly held?

---

## §2 — Frozen construct (binds the single run)

| # | Element | Frozen value |
|---|---|---|
| S1 | Schema / symbol / calendar | `tbbo`, `MNQ.v.0`, continuous, **2025-08-06 → 2026-08-04** (N14 S1) |
| S2 | Events | Exact N14 set: parent `events.parquet` / rebuild via unmodified parent `build_events.py` — **255** triggers + **1,275** controls (k=5, seed 20260805, ≥15 min sep) |
| S3 | Feature | Signed `A = (bid_sz−ask_sz)/(bid_sz+ask_sz)` toward breakout side (N14 S3) |
| S4 | Window | **Forward** mean of `A` on **`[t, t+60s)`** — one cell; no horizon sweep |
| S5 | Stress class | ORB trigger moments vs controls — **no** A-threshold subclass |
| S6 | Statistic | `mean(A_fwd_trigger) − mean(A_fwd_control)`; session-block bootstrap 95% CI, **10,000** reps, seed **20260806**; within-session label-shuffle placebo **1,000** reps, same seed; two-sided \|.\| vs p95 |
| S7 | Coverage | ≥1 usable quote in `[t, t+60s)`; **VOID-COVERAGE** if coverage **< 90%** |
| S8 | Power | **VOID-POWER** if covered triggers **< 30** (evaluated before Δ) |
| S9 | Magnitude floor | **AMBIGUOUS-HOLD** if accept limbs clear except \|Δ\| **< 0.00714** (≡ 0.05 contracts at median L1 total 7) |
| S10 | Halves | H1/H2 of panel in session-date order; disagree on sign → **AMBIGUOUS-HOLD** (Cap not spent) |
| S11 | Outputs | n, coverage, means, Δ, CI, placebo p95/p_emp, halves. **No** outcomes, MFE/MAE, gate proposal |

**Transport:** windowed forward slivers only (strict subset of S1). N14 `quotes.parquet` must **not** be read as this cell’s input.

---

## §3 — Avenue A / Cap arithmetic

- **Route A**, survivor-tied to ORB-MNQ-1 (monitors limb).  
- **`K_intrinsic = 1`** on Cap mark-spent; bank disclosed, not summed.  
- Cap 1.0 → floor 0.650 / headroom 0.350.

---

## §4 — Forbidden moves

- FM-1 — Outcome joins (R, win/loss, MFE/MAE) — F2 GUARD.  
- FM-2 — A-threshold subclass / stress retune after data.  
- FM-3 — Horizon / normalization / instrument sweep.  
- FM-4 — MNQPROX reopen.  
- FM-5 — MBP-10/MBO without fail-clause + GO.  
- FM-6 — Gate / filter conversion of a positive (fresh K-bound axis).  
- FM-7 — Auto-wire to PF-CUSUM (INTEGRATE packet / separate GO).  
- FM-8 — Reading Δ before coverage/power gates.  
- FM-9 — Editing this freeze after seeing a number (Trap #12).

---

## §5 — Verdict gates (precedence)

| # | Condition | Verdict | Cap disposition |
|---|---|---|---|
| W0 | covered n < 30 | `VOID-POWER` | Cap **held** |
| W1 | coverage < 90% | `VOID-COVERAGE` | Cap **held** |
| W2 | CI includes 0 | `FALSIFIED` | Cap **held** |
| W3 | CI excludes 0 ∧ \|Δ\| ≤ placebo p95 | `FALSIFIED` | Cap **held** |
| W4 | clear of W0–W3 ∧ (\|Δ\| < 0.00714 **or** halves disagree on sign) | `AMBIGUOUS-HOLD` | Cap **not** spent; dated packet |
| W5 | clear of W0–W4 | `RESOLVED` | Cap seat **marked spent**; tripwire **candidate** only — wiring GO separate |

---

## §6 — Pre-registered expectation

**Reject / Cap held** (W2 or W3 most likely). N14’s contemporaneous Δ ≈ 0.07 contracts; forward persistence is the unlikely branch. A null discharges that prediction.

---

## §7 — Protocol order

1. This file committed (**freeze**) — before any forward-window quote.  
2. Cap-spend GO — **discharged** 2026-08-06 (Phase-0 affirmation).  
3. Harness + unit tests green before runner reads real forward quotes.  
4. Re-estimate S1 `tbbo` (free metadata) → windowed forward pull.  
5. Single run → RESULTS discharges exactly one §5 branch → closure + boards.

---

## §8 — Audit hooks

```bash
git log --oneline -- lab/archive/mnq_capa_n14_tripwire_2026-08-06/PREREG.md | Select-Object -Last 1
rg -n "F2 GUARD|FM-1|0\\.00714|20260806" lab/archive/mnq_capa_n14_tripwire_2026-08-06/PREREG.md
PYTHONPATH=lab .venv-research/Scripts/python.exe -m databento_fetch.db_fetch estimate \
  --symbols MNQ.v.0 --stype continuous --schema tbbo --start 2025-08-06 --end 2026-08-04
```

---

## Amendment log (append-only)

- **2026-08-06 — FROZEN.** Cap-spend GO already issued; no forward-window quantity yet.
- **2026-08-06 — RUN EXECUTED; §7 steps 3–5 DISCHARGED; verdict `RESOLVED` (W5); Cap seat marked spent.** 11 unit tests green before the runner read a real forward quote; full-S1 estimate $0.0000; windowed forward pull 4,804,045 quotes / 1,530 events; single run. Difference **−0.022928**, CI95 **[−0.028061, −0.017558]**, placebo \|.\| p95 **0.004356** (p_emp 0.000), coverage **100%**; halves agree; \|Δ\| > magnitude floor. **§6 pre-registered Cap-held expectation was WRONG** — recorded as a failed prediction. Tripwire was **candidate** at Cap close; wiring GO later discharged as docs-only companion registration — [`ADR 2026-08-06`](lab/archive/../../../docs/adr/2026-08-06-capa-tripwire-pfcusum-companion-registration.md). [`RESULTS.md`](RESULTS.md)
