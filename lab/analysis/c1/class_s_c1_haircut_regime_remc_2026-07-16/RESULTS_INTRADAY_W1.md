# W1 — intraday-honest both-halves re-run (0.50× arm)

**Status:** `MEASURED` — full-panel + H1/H2 on the honest clock; bootstrap long-pole **not** in this packet
**Date:** 2026-08-09
**Authorization:** operator GO 2026-08-04 on the frozen Phase-4 contract; Cursor execution packet [`docs/spec/2026-08-09-w1-intraday-rerun-execution-spec.md`](../../../docs/spec/2026-08-09-w1-intraday-rerun-execution-spec.md)
**Owner ADR:** [`docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md`](../../../docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md)
**Frozen contract:** [`docs/spec/2026-08-04-phase4-both-halves-intraday-rerun-spec.md`](../../../docs/spec/2026-08-04-phase4-both-halves-intraday-rerun-spec.md)
**Runner / raw:** [`run_w1_intraday_both_halves.py`](run_w1_intraday_both_halves.py) · [`w1_intraday_both_halves_report.json`](w1_intraday_both_halves_report.json)
**Gate (as frozen for this campaign, unedited):** bust ≤ 3.0% ∧ P(pass) ≥ 50% — [`2026-07-13 survivor-scoring prereg`](../../../../docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) — ⚠ **superseded 2026-08-26: the live Part A ceiling is 5.0%** ([`prereg v2`](../../../../docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) §3). Both tiers below PASS at either ceiling, so no verdict here moves; the label is corrected because CLAUDE.md routes readers to this file as the Class-S honest-clock RESULTS of record. ⚠ **These are the 0.50× arm only — no 1.00× honest-clock figure exists for either `trailing_locking` tier**, which is why the ceiling collision on candidate #1 cannot be settled from this file.

---

## Method

- **Channel:** `intraday_low` threaded through `lab/discovery/prop_survivor_scoring.py` → `run_seed` → `simulate_path` (paired week-blocks; same indices).
- **Derivation:** per-trade MTM adverse extreme from MYM/MNQ 15m bars (`core/data/bar_data/`), scaled to the same static×1R book as the frozen class_s panel, then ×0.50 lifecycle haircut co-moving with `daily_100k` (not `dd_scale` — engine applies that).
- **Geometry:** `dd_lock_offset_usd` unreachable on both `trailing_locking` tiers (production default).
- **Scope:** 0.50× arm · full-panel + H1/H2 · discharge tiers only · 10k sims × seeds 42/123/2026 · Run-2 consistency-on. **No bootstrap** (Cursor packet wall-clock; Phase-4 P3 long pole remains separable).
- **Non-vacuity (1.00× book, horizon 400, 200 sims/seed):** EOD bust 2.50% / pass 71.00% → real bust 32.33% / pass 57.17% — channel is load-bearing. Guard run at 1.00× because at 0.50× the deepest bar excursion (~$1.3k) sits inside the $3k trail for the right reason.

---

## Results — WATCH-1 0.50×, intraday-honest clock

| Tier | Full bust / pass | H1 bust / pass | H2 bust / pass | Floor (3.0% / 50%) |
|---|---|---|---|---|
| Tradeify_Select_100K | **0.72% / 99.20%** | **1.77% / 95.08%** | **0.28% / 99.72%** | **PASS** |
| MFFU_Rapid_100K | **0.72% / 99.21%** | **1.77% / 95.08%** | **0.28% / 99.72%** | **PASS** |

Both discharge tiers clear full + both halves. Raw floats in [`w1_intraday_both_halves_report.json`](w1_intraday_both_halves_report.json).

---

## Deltas vs EOD corrected-geometry reference

Reference: [`CORRECTED_FULLPANEL.md`](CORRECTED_FULLPANEL.md) (2026-07-24, close-only, unreachable lock, 0.50×).

| Tier · partition | EOD (corrected) | Intraday (W1) | Δ bust |
|---|---:|---:|---:|
| Tradeify full | 0.11% | 0.72% | **+0.61 pp** |
| Tradeify H1 | 0.22% | 1.77% | **+1.55 pp** |
| Tradeify H2 | 0.04% | 0.28% | **+0.24 pp** |
| MFFU full | 0.11% | 0.72% | **+0.61 pp** |
| MFFU H1 | 0.22% | 1.77% | **+1.55 pp** |
| MFFU H2 | 0.04% | 0.28% | **+0.24 pp** |

The honest clock deepens every published EOD partition and still clears the frozen floor on this arm and these partitions. **Bootstrap-95th remains unmeasured** on the honest clock.

---

## Coverage residual

- Trade panel span: 2020-01-06 → 2026-06-30 (1,692 bdays).
- 15m bars: 2020-07-01 → 2026-07-02. Pre-bar days fall back to `min(0, exit-day pnl)` — residual **optimistic** on the early span (documented, not repaired by inventing bars).
- Bar panels restored this session via `scripts/parse_bar_export.py` from the 2026-07-21 BAR EXPORTs; SHA256 matched `core/data/bar_data/SHA256SUMS` (gitignored CSVs not committed).

---

## What this does **not** license

- No rung / lifecycle / allocation motion from these numbers — disposition is the operator's.
- Does not by itself supersede the 2026-07-17 operator-signed close-only record (frozen Phase-4 §3 / §5).
- Does not close the four-decision W1 campaign — this packet scored the class_s both-halves limb only.
- Does not arm the rail.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-09 | Measured 0.50× full+H1/H2 under bar-derived `intraday_low`; non-vacuity OK; both discharge tiers PASS | Cursor (W1 execution packet) |
