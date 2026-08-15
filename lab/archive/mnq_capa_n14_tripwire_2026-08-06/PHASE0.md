# Q-CAPA-1 Phase-0 — Cap-seat Route A forward-tripwire charter

**Parent brief:** [`docs/briefs/Q-CAPA-1-cap-seat-route-a-n14-tripwire.md`](lab/archive/../../../docs/briefs/Q-CAPA-1-cap-seat-route-a-n14-tripwire.md)  
**N14 parent:** [`mnq_orb_flow_substrate_2026-08-05`](lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/) (`RESOLVED` W1 @ `be6b94e`)  
**Operator ask:** *"proceed with Q-CAPA-1 — Cap-seat Route A next cell after N14"* (2026-08-06)  
**Cost this Phase-0:** **$0.00** — charter only; no TBBO read; no Cap spend; no manifest.  
**Cap spend / PREREG / pull:** **AUTHORIZED 2026-08-06** — operator: *"affirm charter, commit, then proceed with next steps."* Affirms this charter **and** issues Cap-spend GO for the frozen C0–C11 cell below. PREREG must still freeze **before** any forward-window quote is read.

---

## Verdict

**`CHARTER-CLEARS`.** An outcome-free, Route A, single-cell (`K_intrinsic=1`) forward construct is nameable with projected **n = 255 ≥ 30**. Phase-0 does **not** VOID on power.

**Cap-spend GO (2026-08-06):** operator affirmed this charter and directed Cap-spend next steps. Cap seat is **not yet marked spent** — that fires only on H-CAPA-1 accept limbs after a frozen PREREG + single run. Pre-registered expectation remains **Reject / Cap held**.

**What GO does *not* license:** MBP-10/MBO, horizon/threshold sweep, outcome joins, PROX reopen, PF-CUSUM auto-wire, or a second Cap cell.

---

## Cheap falsifier (parent-side, this session)

| Check | Result |
|---|---|
| N14 `events_summary.json` | `engine_n=255`, controls `1275`, k=5, seed `20260805` |
| N14 `RESULTS.json` | Δ **−0.009367**, CI excludes 0, coverage **1.0**, verdict `RESOLVED` |
| PROX discriminator | STOP B/1 — `MNQPROX-2` VOID-POWER (`n_paired=15`); no Cap path through proximity |
| Parent `quotes.parquet` | **MISSING** in this worktree — and even when present is **pre-touch only** (N14 `WINDOW_S=60` preceding). Forward windows are a **new** read under Cap-spend GO; cache reuse ≠ entitlement expansion |
| Cap seat | still **unspent** (operator-reserved Route A slot) |

---

## Frozen construct (charter — binds any later Cap-spend PREREG)

| # | Element | Frozen value | Why |
|---|---|---|---|
| **C0** | Route / K | **Avenue A Route A**, survivor-tied to **ORB-MNQ-1**; **`K_intrinsic = 1`** if Cap is spent; `K_banked(MNQ)` **disclosed** at PREREG time from `discovery_manifests/` (does not gate — ADR 2026-08-04); Cap 1.0 → floor **0.650**, headroom **0.350** | Catalogue wall favours Route A; Cap seat is a single cell, not Route B generate |
| **C1** | Event set | **Exact N14 S2 set** — rebuild via unmodified parent `build_events.py` / `events.parquet` (255 triggers + 1,275 controls). No new event definition | Survivor-tied; no second search over triggers |
| **C2** | Feature | Signed L1 asymmetry **`A`** exactly as N14 S3: `(bid_sz−ask_sz)/(bid_sz+ask_sz)` signed toward breakout side | Same geometry; no new feature family |
| **C3** | Window | **Forward** mean of `A` over **`[t, t + H)`** with **`H = 60 s`** (one cell). Window is **post-touch**, not pre-touch | Meets MSCHAN/Avenue A **≥ 5 s** floor; matches N14’s 60 s aggregation for flicker dampening; **forbids horizon sweep** (extra H → extra K) |
| **C4** | Stress class | **ORB-MNQ-1 trigger moments** vs ToD-matched non-trigger controls. **No** thresholded subclass of triggers (no “adverse-tail of A_pre” split) | Thresholding A_pre would add a free axis → K≥2 and Cap-seat breach; book-state only; **never** ORB R / win / MFE / MAE |
| **C5** | Controls | Inherit N14 **S4** timestamps (same session, ≥15 min sep, k=5, seed 20260805). Measure **C3** on those timestamps — **not** PROX level-arm | PROX chain STOPPED (B/1) |
| **C6** | Statistic | `mean(A_fwd_trigger) − mean(A_fwd_control)`; session-block bootstrap 95% CI (10,000 reps, seed **20260806**); within-session label-shuffle placebo 1,000 reps, same seed; two-sided \|.\| vs p95 | N14 idiom; new seed so Cap-spend CI is not a silent re-use of N14’s RNG stream |
| **C7** | Coverage | Fraction of triggers with ≥1 usable TBBO quote in `[t, t+H)`; **VOID-COVERAGE** if coverage **< 90%** | N14 S7 |
| **C8** | Power floor | **VOID-POWER** if covered triggers **< 30** before reading Δ | Same floor as PROX-2 Phase-0 |
| **C9** | Schema / spend | **`tbbo`**, `MNQ.v.0`, continuous, S1 calendar **2025-08-06 → 2026-08-04** (same as N14). Windowed transport of **forward** slivers only. Full-S1 estimate was **$0.0000** at N14; re-estimate before Cap-spend GO. **N14 `quotes.parquet` does not contain post-touch quotes** | Coarsest schema first; no MBP-10 without fail-clause + GO |
| **C10** | Magnitude floor (AMBIGUOUS-HOLD) | If CI excludes 0 **and** placebo limb clears **but** \|Δ\| **< 0.00714** (≡ **0.05 contracts** at median L1 total **7**) → **`AMBIGUOUS-HOLD`**; Cap **not** spent until dated re-test | Brief §4 / §6; prevents Cap spend on a tinier-than-N14 forward echo |
| **C11** | Outputs (closed list) | n, coverage, means, Δ, CI, placebo p95/p_emp, H1/H2 halves. **No** per-trade table, win/loss split, MFE/MAE, A_pre join, gate proposal | FM-1 / F2 GUARD |

**Flicker:** handled by **window mean over 60 s** (N14 precedent + MSCHAN salvage). No separate flicker filter parameter in this cell — adding one is a second axis.

---

## What Cap spend would test (H-CAPA-1, operationalized)

**Accept (Cap may be marked spent; tripwire stays candidate — wiring GO separate):**  
C7 coverage ≥ 90% ∧ covered n ≥ 30 ∧ CI excludes 0 ∧ \|Δ\| > placebo p95 ∧ \|Δ\| ≥ 0.00714 ∧ halves agree in sign (else AMBIGUOUS-HOLD path).

**Reject / Cap held:** CI includes 0, **or** \|Δ\| ≤ placebo p95, **or** VOID-POWER / VOID-COVERAGE, **or** only constructions that need outcome joins clear.

**AMBIGUOUS-HOLD:** power OK, significant, but \|Δ\| < magnitude floor **or** halves disagree on sign → Cap not spent; dated packet.

---

## Forbidden moves (Phase-0 + Cap-spend)

Carried from brief §5; load-bearing here:

1. No MNQPROX reopen / τ or S4a(ii) edit.  
2. No outcome joins (R, win/loss, MFE/MAE) — F2 GUARD / FM-1; MSCHAN “breakouts vs failures” **barred**.  
3. No conversion of a positive into an ORB entry filter / fifth gate.  
4. No Route B multi-cell catalogue under Cap seat.  
5. No MBP-10 / MBO without fail-clause + GO.  
6. No Cap spend / manifest / pull before operator Cap-spend GO.  
7. No horizon / threshold / normalization sweep after seeing Δ.  
8. No silent rewrite of N14 as ORB-specific after PROX died.

---

## Phase-0 gate vs Cap-spend gate

| Gate | Fired? | Disposition |
|---|---|---|
| Cannot name outcome-free stress class | **No** — C4 named | — |
| Projected n < 30 | **No** — 255 | — |
| Projected coverage known < 90% | **Unknown** — no forward quotes on disk | Cap-spend run must evaluate C7 **before** Δ; VOID-COVERAGE stops Cap spend |
| Cap-spend GO | **Issued 2026-08-06** | Proceed to PREREG freeze → tests → pull → single run |

---

## Next (operator)

1. ~~**Affirm this charter**~~ — **DONE 2026-08-06** (Cap-spend GO issued).  
2. Freeze cell-local `PREREG.md` **before** any forward-window quote is read → tests green → estimate → windowed forward pull → single run → RESULTS → closure per brief §9.  
3. On reject / VOID / AMBIGUOUS-HOLD: Cap remains **held**; N14 stays disclosure watchlist.

---

## Audit hooks

```bash
# Parent event count (expect 255 / 1275)
python -c "import json; print(json.load(open('lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/events_summary.json')))"

# This charter forbids Cap spend without GO
rg -n "NOT authorized|Cap spend|CHARTER-CLEARS|H = 60" lab/archive/mnq_capa_n14_tripwire_2026-08-06/PHASE0.md

# Pre-touch cache cannot satisfy C3
rg -n "WINDOW_S|preceding" lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/pull_windows.py

# Brief still owns the Q
rg -n "Phase-0 charter|Cap held" docs/briefs/Q-CAPA-1-cap-seat-route-a-n14-tripwire.md
```
