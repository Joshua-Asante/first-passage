**Theme:** c1

# W1 4th partition — intraday-honest bootstrap-95th at 0.50× — **INTERIM, INCOMPLETE**

**Status:** `INCOMPLETE — 48/100 panels on 1 of 2 tiers; operator stopped the run 2026-09-02.`
**No gate verdict is taken here.** The pre-registration freezes `n_panels=100` across
`{Tradeify_Select_100K, MFFU_Rapid_100K}`; this run covers 48 panels of the first tier and zero of
the second. What follows is an interim measurement with its uncertainty stated, not a partition result.
**Date:** 2026-09-02 · **Spend:** $0 / K=0 · **Wall:** 11,313s (3.1h), 8 cores.
**Owner ADR:** [`W1`](../../../../docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md) ·
**Contract:** [`Phase-4 P3`](../../../../docs/spec/2026-08-04-phase4-both-halves-intraday-rerun-spec.md) ·
**Frozen reading (written before any full-scale number):** [`READING.md`](READING.md)
**Predecessor:** [`RESULTS_INTRADAY_W1.md`](../class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md)
— *"Bootstrap-95th remains unmeasured on the honest clock."*

No locked surface, allocation, Pine, `dd_protection` constant, lifecycle state or rail setting was
touched. Nothing was armed; `dry_run` stays `true`.

---

## §1 — What was measured

The one cell the 2026-08-09 W1 packet declared out of scope. The campaign's 2026-07-16
pre-registration scores `bust ≤ 3.0% ∧ pass ≥ 50%` on **{full, H1, H2, bootstrap-95th} ×
{Tradeify_Select_100K, MFFU_Rapid_100K}** — eight cells. W1 landed six (all PASS) and dropped the
bootstrap for its executor's wall-clock. This run is the remaining two, and it completed neither.

Each resampled panel is scored **twice from one shared block draw** — EOD control and honest clock —
so the two arms differ only by the threaded `intraday_low` channel.

## §2 — Interim numbers (Tradeify_Select_100K, 48/100 panels)

| Arm | bust-95th | bust mean | bust max | panels > 3.0% | panels > 5.0% | pass-5th |
|---|---|---|---|---|---|---|
| EOD control | 0.6755% | 0.2047% | 1.5467% | 0 / 48 | 0 / 48 | 96.17% |
| **Honest clock** | **3.3340%** | 1.1835% | 6.9300% | **4 / 48** | 1 / 48 | 94.14% |

**Paired delta on the 95th: +2.658pp.** Per-panel: mean +0.979pp, median +0.637pp, max +5.383pp.
**The honest arm is worse than the EOD arm on 48 of 48 panels** — the direction carries no sign
ambiguity. The cost is tail-concentrated: the median panel barely moves while the worst moves 5.4pp,
which is why the 95th percentile moves far more than the mean.

**The pass-floor limb is not close to binding** on either arm (94.14% vs a 50% floor).

Stability across prefixes — both series are flat, so the interim is not drifting:

| n | 8 | 16 | 24 | 32 | 40 | 48 |
|---|---|---|---|---|---|---|
| EOD 95th | 0.6292% | 0.7158% | 0.6895% | 0.7285% | 0.7032% | 0.6755% |
| Honest 95th | 3.3882% | 3.3875% | 3.3527% | 3.4042% | 3.3708% | 3.3340% |

## §3 — Controls

| Control | Result |
|---|---|
| Non-vacuity (frozen Phase-4 §1) | **PASS** — reproduced W1's own guard exactly: EOD 2.50% vs real 32.33%, 1.00× book, horizon 400 |
| Worker-attested geometry (M-23 defence) | **PASS** — all 48 panels report `dd_lock_offset_usd = 1e6`; run aborts otherwise |
| Channel liveness under resampling | **PASS** — arms differ on 48/48 panels |
| Paired-draw equivalence | **PASS** — the paired resample reproduces the EOD resample's P&L series exactly on pids 0–9 |
| Block-builder agreement | **PASS** — `blocks_from_daily_pnl` ≡ `paired_blocks_from_daily` on every panel |
| **Reproduction vs the published EOD pin** | ⚠ **OPEN — does not converge (see §4)** |

## §4 — The control that did not reproduce (read this before quoting any absolute level)

The EOD arm should reproduce the published corrected-geometry bootstrap-95th of **1.20%**
([`eval_shape_diagnostics_2026-07-28`](../eval_shape_diagnostics_2026-07-28/RESULTS.md) §(a),
same frozen seeds, block size and panel count). It reads **0.68%**, and it is **flat at ~0.70%
across all six prefix lengths** rather than climbing toward 1.20%.

Panels are independent draws with per-`pid` RNG streams, so the first 48 are a random sample of the
100 and a consistent estimator should not sit at half its target for 48 consecutive panels. This
reads as a systematic divergence from the July run, not small-sample noise. It falls inside the
±2.0pp tolerance the haircut runner used for this statistic, but that tolerance was set to absorb
numpy-version drift, and the observed behaviour looks like exactly that — this tree runs
numpy 2.4.4 / pandas 3.0.2, far newer than the July run.

**Consequence, stated plainly:** the *absolute level* of the honest figure is **not certified**.
A reproduction check of this harness's full/H1/H2 partitions against their published pins
(EOD 0.11%/0.22%/0.04%; honest 0.72%/1.77%/0.28%) was scripted
([`repro_check.py`](repro_check.py)) and is **owed** — it isolates whether the divergence lives in
the panel/engine layer or only in the bootstrap layer.

**What survives the doubt:** the **paired delta**. Both arms ran in one process, on identical draws,
with identical library versions, differing only by the threaded channel. Whatever offset affects the
control affects the honest arm equally. The delta is therefore the robust quantity, and it is large:
**+2.658pp on the 95th, adverse on 48 of 48 panels.**

## §5 — Interim reading, against the frozen mapping in `READING.md`

Anchoring the measured delta two independent ways:

| Anchor | Implied honest bust-95th |
|---|---|
| This run's own EOD arm (0.68% + 2.66pp) | ≈ 3.33% |
| The published EOD pin (1.20% + 2.66pp) | ≈ 3.86% |

**Both land in the same band: above the campaign's frozen 3.0% floor and below 5.0%.** That is the
**middle case** of the three readings frozen in `READING.md` before any number was seen:

> 4th partition **FAILS this campaign's frozen floor**. `RESOLVED-DEPLOYABLE` does not complete on
> the honest clock; T5's first condition is **not** met. The §4 Part A limb would nonetheless clear
> the *live* v2 ceiling — the two gates disagree, and that is an operator ruling, not a result.

This is an **indication, not a verdict.** It is 48 of 100 panels on one of two tiers, and its
absolute level rests on a control that did not reproduce. It is reported because it is
decision-relevant and because suppressing an adverse interim while a favourable one would have been
reported is the asymmetry this repo's conventions exist to prevent.

## §6 — What this does not establish

- **No partition verdict**, no `GATE PASS`/`FAIL`, no change to `RESOLVED-DEPLOYABLE`.
- **T5 is not ruled.** Its first condition is unsettled, and it fires only jointly with T1 —
  whose limbs are measured **adverse**: book weekly coverage **217/297 = 73.1%** against a ≥95%
  floor, and inactivity-ON path death **92.6–97.6%** against a ≤10% floor
  ([`c1_cadence_coverage`](../c1_cadence_coverage_2026-08-03/RESULTS.md) §B ·
  [`c1_cadence_inactivity`](../c1_cadence_inactivity_2026-08-02/RESULTS.md)). T1 additionally
  requires a cadence instrument to **ship**; the coverage study states the mitigation "does not yet
  exist at the execution layer (residual track R8)", and whether the operator-placed weekly token
  trade discharges that clause is **unruled anywhere in the estate**.
- **Nothing is re-admitted to Tradeify**; the eval-included de-scope stands until a superseding ADR.
- **§4 is not discharged**; that is a superseding ADR on the operator's signature.
- **No fallback rung is implied.** If 0.50× ultimately fails, 0.40× is **not** available: the ladder
  is 1.00×/0.50×/0.25×/0.00×, and the campaign pre-registration forbids inventing a fractional
  haircut or bisecting to just clear.

## §7 — Owed to complete this partition

1. **Panels 48→100 on Tradeify, then 0→100 on MFFU.** Resumes from
   `ckpt_Tradeify_Select_100K.json` without recomputing; ~4h + ~7h at observed throughput.
2. **The reproduction check** (`repro_check.py`) — full/H1/H2 on both clocks against published pins.
   Until it lands, no absolute level from this run should be quoted as gate-grade.

## §8 — Provenance

Harnesses vendored **byte-identical** from `283d1de^` (the Great Prune removed them from their
original homes); sha256 verified at vendoring time:

| File | sha256 | Retrieved from |
|---|---|---|
| `run_class_s_c1_scoring.py` | `64357e32b64695be…d2db1824` | `class_s_candidate1_scoring_2026-07-15/` |
| `run_class_s_c1_regime_gate.py` | `e275e81fa8cd2777…23fa9a498` | `class_s_candidate1_scoring_2026-07-15/` |
| `_boot_attested.py` | `34d663b85063b6e8…36c8e9a` | `eval_shape_diagnostics_2026-07-28/` |

Vendor data verified against manifests before use: `MNQ_M15.csv`, `MYM_M15.csv`
(`core/data/bar_data/SHA256SUMS`) and both Striker panels (`core/data/tv_exports/cme/SHA256SUMS`) —
all MATCH. Frozen scoring parameters are parsed at runtime from the pre-registration
(`load_scoring_thresholds`), never retyped: ceiling 3.0%, pass floor 50%, seeds (42, 123, 2026),
10,000 sims/seed, horizon 1500, Run-2 consistency-on. Bootstrap parameters imported from the
retrieved regime-gate module: `N_PANELS_DEFAULT=100`, `BLOCK_SIZE_BDAYS=126`, `BOOT_SEED=20260715`.

**Doc-skew found in passing (not repaired here):**
[`CORRECTED_FULLPANEL.md`](../class_s_c1_haircut_regime_remc_2026-07-16/CORRECTED_FULLPANEL.md)
still reads *"Still unmeasured … the corrected 0.50× bootstrap-95th"*. That was superseded four days
later by `eval_shape_diagnostics_2026-07-28` (1.20%). Its frozen body carries a reader-intercept
about a different row, so the stale line has no correction pointer.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-09-02 | Campaign opened; harnesses vendored; `READING.md` frozen before any full-scale number; run launched | Claude Code (Opus 5) |
| 2026-09-02 | Operator stopped the run at 48/100 panels, tier 1 of 2. Interim recorded; no verdict taken; EOD control reproduction flagged OPEN | Joshua (stop) + Claude Code |
