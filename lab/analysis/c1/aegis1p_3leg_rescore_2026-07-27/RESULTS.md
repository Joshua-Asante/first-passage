**Theme:** c1
**Status:** ACTIVE — Aegis@1.00% 3-leg corrected-geometry re-MC under Tradeify envelope
# Aegis@1.00% 3-leg corrected-geometry re-MC — RESULTS

**Status:** `GEOMETRY-FAIL` (§6 asserted against actual numbers; no §6 criterion moved after data)
**Date:** 2026-07-27
**Pre-registration (FROZEN before run):** [`docs/briefs/pre-registration/2026-07-27-aegis-1p-3leg-corrected-geometry-prereg.md`](../../../docs/briefs/pre-registration/2026-07-27-aegis-1p-3leg-corrected-geometry-prereg.md)
**Frozen gate:** [`2026-07-13-prop-survivor-scoring-prereg.md`](../../../docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) (floor bust ≤ 3.0% ∧ P(pass) ≥ 50%, Run-2)
**Runner / report:** [`run_aegis1p_rescore.py`](run_aegis1p_rescore.py) · [`aegis1p_report.json`](aegis1p_report.json) · input inventory [`inventory_aegis1p.json`](inventory_aegis1p.json)
**Engine:** frozen — 10K sims × seeds 42/123/2026, horizon 1500, Run-2 consistency-on, `dd_protection` OFF, corrected geometry (`dd_lock_offset_usd → 1_000_000.0` runtime patch, restored to 100; production constant untouched).

## Controls (2-leg reproduction — all MATCH, harness sound)

| Tier | This run | Published pin | Δ |
|---|---|---|---|
| Tradeify_Select_100K | 4.74% | 4.74% | 0.00pp |
| Tradeify_Select_50K | 1.06% | 1.06% | 0.00pp |
| MFFU_Rapid_50K | 0.96% | 0.96% | 0.00pp |

## Gating cells — 3-leg (MYM 0.70% + MNQ 0.37% + Aegis→6J @ 1.00%, native-1% export `ac331`)

| Tier | Bust | Pass | Floor (≤3.0% ∧ ≥50%) | Δ vs 2-leg |
|---|---|---|---|---|
| Tradeify_Select_100K | **10.96%** | 89.04% | **FAIL** | +6.22pp |
| Tradeify_Select_50K | **3.78%** | 96.22% | **FAIL** | +2.72pp |
| MFFU_Rapid_50K | **3.54%** | 96.46% | **FAIL** | +2.58pp |

0 of 3 tiers clear; no cell in the (3.0%, 3.2%] noise band (closest is 3.54% — a clean
miss, not an AMBIGUOUS re-run trigger). **H-AEGIS1P falsified.**

## Diagnostics (non-gating, pre-declared)

**Halves (regime split — H1 is the killer, consistent with every prior Aegis look):**

| Tier | H1 (≈2020-23) | H2 (≈2023-26) |
|---|---|---|
| Tradeify_Select_100K | 23.64% FAIL | 6.90% FAIL |
| Tradeify_Select_50K | 11.35% FAIL | 1.86% PASS |
| MFFU_Rapid_50K | 10.78% FAIL | 1.73% PASS |

**COST-TRUE (Tradeify 6J $3.10/side actual vs $1.30 modeled, −$3.60/RT/contract on the
Aegis leg):** 13.80% / 5.18% / 4.88% — real commissions make every cell materially worse;
the headline cells are therefore *optimistic* bounds.

**Bootstrap:** not run (pre-committed to full-panel passers only; there were none).

## Verdict + dispositions

- **GEOMETRY-FAIL.** The Aegis risk bracket in the c1 book is now closed with three
  measured points at the friendliest tiers: **0.75% → 2.02%/1.28%** (defective geometry,
  2026-07-11 sensitivity arms) · **1.00% → 3.54–3.78%** (corrected, this run) ·
  **1.50% → 10.33–17.70%** (defective, 2026-07-11). Under corrected geometry even the 1%
  arm fails the 3.0% floor everywhere, and the H1 half shows why: the 2020-23 chop regime
  busts 10–24% — the same regime concentration every prior Aegis-in-book look found.
- **The lane is dead at both layers.** Geometry (this run) AND feasibility (pre-declared:
  6J = 10 micro-equivalents ⇒ Aegis cap-12 ≈ 120 equiv vs caps 40–80 already consumed by
  the 2-leg; M6J at no FRIENDLY firm). Per pre-reg §4: **no further risk-arm measurement
  is owed**; any future re-open requires new mechanism evidence, not a new parameter.
- **c1 2-leg book unchanged** — controls only; no gate, pin, or posture touched.
  §4-falsifier state (UNDISCHARGED, hard date 2026-11-08) untouched.
- **Panel-of-record note:** the fresh `ac331` export is front-truncated vs the pinned
  ae744 (starts 2020-07-27 vs 2020-02-24, N=143 vs 152) — disclosed in the pre-reg; the
  ae744 panel-of-record pin is untouched.

## Audit hook (append-only)

Was any criterion moved after data arrived? **No.** Floor, tier set, arm, partitions,
control pins/tolerances, 1R pin ($2,163.57/n7, frozen pre-run in the inventory JSON), and
verdict vocabulary all match the FROZEN 2026-07-27 pre-registration; the §8 protocol ran
in order (inventory → freeze → smoke wiring check → full run → this assertion).
