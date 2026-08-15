# Q-REGIME-STRESS-1 — hostile-regime stress MC + per-bucket robustness

**LoR:** OUTER (INQHIORI). Structural/statistical investigation. Does **not** modify locked
allocations, dd_protection, or strategy code. May inform a future reweight/gate ADR.
**Date:** 2026-06-15 · **Disposition:** **FALSIFIED-FAIRWEATHER** · **Status:** `DONE_WITH_CONCERNS`
**Artifacts:** `reports/regime_stress/q_regime_stress_1.py` (harness) + `Q-REGIME-STRESS-1.json` (data).
*(`reports/*` is gitignored — these are local-only artifacts; see Concern #5 for preservation.)*

---

## §0 — Rule-0 production reads (git anchors)

| File | `git -1` | Confirmed |
|---|---|---|
| `core/portfolio_mc.py` | `4331e65` | resampler = **non-overlapping Mon-anchored 5-day week-block bootstrap**, sampled with replacement (`build_week_blocks`+`run_seed`). **Not iid; no tunable L.** |
| `core/firm_rules.py` | `4331e65` | allocs G 0.34% / **DJ30 0.70%** / A 1.50% / **NAS 0.37%** |
| `core/dd_protection.py` | `6473809` | **DD_TRIGGER 0.015 / DD_SCALE 0.40** (C2), hard MVD spec-pin |
| `CLAUDE.md` | `ecd4e0c` | anchor 99.83/0.17/4.37 |
| `docs/adr/2026-05-23-allocation-refresh-2.md` | `5b8ff71` | DJ30 0.70%/pyr750, NAS 0.37% |

**Drift flags resolved (Rule 0: code wins over the brief's stale prose):**
- **§0c → C2 = 1.5%/0.40×** (`dd_protection.py:52-53`). Cached `baselines.md` 1.0% figure is stale.
- **§0d → anchor = 99.83 / 0.17 / 4.37, median 26**, machine-pinned in `tests/test_mc_anchors.py:102-104`. The 97.88/0.22/4.55 figure (and its "DJ30 49.2%" bust attribution) is the stale 05-06 cache.
- **§0b allocations stale in the brief.** Brief said confirm "DJ30 1.00% / NAS 0.40%"; production is the 2026-05-23 refresh-2 (**0.70% / 0.37%**). **Appendix A's printed *scale factors* (DJ30 0.464, NAS 0.208) encode the stale 1.00%/0.40% allocations** — so the brief's scaled-$ headline ("hostile ~$14.6K/yr") used superseded sizing. The MC here uses the **locked** 0.70%/0.37%; the raw N/Net/mean-R reconciliation targets are allocation-independent and still hold exactly.
- Current production bust attribution = **Guardian 41.2% / Aegis 37.3% / Striker(DJ30) 19.6% / NAS 2.0%** (verified by re-running `compute_default_config`: 21/19/10/1 of 51 busts).

## §0.5 — operator-confirmed decisions (2026-06-15)

1. **Resampler:** production **5-day week-block bootstrap, used verbatim** (no L=8 — the brief's L=8 premise mischaracterized the engine, which is already non-iid).
2. **Calibration:** **both** — (B) canonical 2026-05-24 Pepperstone panel (anchor-reproduction **gate**, adaptive 1R) + (A) uploaded data windowed to 2022-01-04 (data-equivalence diagnostic, adaptive 1R).
3. **Feed:** accept off-feed Strikers (**DJ30 = Vantage, NAS100 = IC Markets/USTEC**) with prominent caveat; Guardian + Aegis are Pepperstone (canonical feed, longer window).

**Build approach:** standalone harness importing the production primitives (`build_daily_panel`/`build_week_blocks`/`_run_seeds`/`_simulate_path`/`implied_1r`) + PR #157's `decompound.run_mc` wrapper — **zero fork** of locked files (`FIRM_RULES_CLEAN`/`DDP_CLEAN`/`PORTFOLIO_MC_CLEAN` all confirmed).

**1R conventions:** bucket runs use **fixed full-panel implied-1R** (Appendix A design — single scale per strategy, isolates regime P&L pattern from 1R-estimation noise); calibration-A uses **adaptive** 1R (fair anchor-reproduction test).

---

## Step 2.1 — per-bucket robustness layer

Full-panel implied-1R reconciles to Appendix A to the cent: G $739.27 / DJ30 $4,314.45 / A $3,311.16 / NAS $3,853.79. Every per-bucket **mean-R matches Appendix A** (rightmost column). mean-R/median-R use the full-panel 1R as the R-unit.

| Strategy (feed) | bucket | N | Net $ | mean-R | med-R | PF | WR | top3-share | dropTop5-PF | dropTop10-PF | mean-R (AppA) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Guardian** (Pep) | hostile | 142 | 870 | 0.008 | −0.924 | **1.01** | 7.7% | 43.17 | 0.37 | **0.03** | 0.01 |
| | normal | 145 | 344,417 | 3.213 | −1.454 | 3.50 | 20.7% | 0.27 | 2.43 | 1.61 | 3.21 |
| | recent | 24 | 168,793 | 9.513 | −3.104 | 4.98 | 25.0% | 0.74 | 0.34 | 0.00 | 9.51 |
| **DJ30** (Vantage) | hostile | 100 | 60,702 | 0.141 | 0.042 | **2.02** | 64.0% | 0.85 | 0.95 | 0.59 | 0.14 |
| | normal | 155 | 238,001 | 0.356 | 0.059 | 2.41 | 69.0% | 0.60 | 1.30 | 0.94 | 0.36 |
| | recent | 14 | 86,635 | 1.434 | 0.894 | 12.63 | 85.7% | 0.70 | 2.28 | 0.13 | 1.43 |
| **NAS100** (IC Mkts) | hostile | 119 | 64,145 | 0.140 | 0.024 | **2.04** | 52.1% | 0.59 | 1.08 | 0.70 | 0.14 |
| | normal | 146 | 427,815 | 0.760 | 0.058 | 4.54 | 57.5% | 0.37 | 2.84 | 2.03 | 0.76 |
| | recent | 28 | 99,723 | 0.924 | 0.083 | 3.80 | 57.1% | 0.97 | 0.63 | 0.09 | 0.92 |
| **Aegis** (Pep) | hostile | 43 | 1,768 | 0.012 | −0.004 | **1.06** | 46.5% | 10.57 | 0.17 | 0.02 | 0.01 |
| | normal | 95 | 147,548 | 0.469 | 0.025 | 4.31 | 60.0% | 0.25 | 3.05 | 2.05 | 0.47 |
| | recent | 11 | 45,716 | 1.255 | 0.104 | 382.26 | 90.9% | 0.76 | 7.59 | 0.00 | 1.26 |

**The §1 asymmetry is confirmed.** Guardian + Aegis are **harvest-only** in the hostile regime (PF 1.01 / 1.06 — statistical breakeven; drop-top-10 collapses to PF 0.03 / 0.02, i.e. the entire tiny positive net is a handful of tail winners). The Strikers are **regime-spanning** (hostile PF 2.02 / 2.04, positive edge survives). Guardian hostile WR is 7.7% — a trend-rider in a trendless regime is death-by-a-thousand-stops.

## Step 2.2 — NAS100 de-flatter (normal-bucket edge ex-2024)

| | N | mean-R | med-R | PF |
|---|---:|---:|---:|---:|
| normal **with** 2024 | 146 | 0.760 | 0.058 | 4.54 |
| normal **ex** 2024 | 103 | 0.430 | 0.034 | 2.67 |
| 2024 only | 43 | 1.553 | 0.066 | **14.78** |

2024 (PF 14.78) roughly **halves** NAS100's normal-bucket edge when removed (mean-R 0.76 → 0.43, PF 4.54 → 2.67). The "normal" baseline is itself flattered by an outlier year — relevant context for any forward NAS100 sizing assumption.

## Step 2.3 — regime-stress MC

Production 5-day week-block bootstrap, locked allocations + C2 dd_protection, 10,000 × 3 seeds, FXIFY challenge structure read from the engine (PASS +5%≥5d / BUST_DAILY −5%/d / BUST_STATIC −5% cum / INACTIVITY 60d).

| cell | source | pass | bust (daily/static) | inact | p99 DD | median | n_bd / n_blk |
|---|---|---:|---:|---:|---:|---:|---:|
| **(i-B) CALIB canonical** [GATE] | canonical Pep, adaptive | **99.83%** | 0.17% (0.00/0.17) | 0.00% | **4.37%** | 26 | 1141/227 |
| — anchor target | — | 99.83% | 0.17% | — | 4.37% | 26 | — |
| (i-A) CALIB uploaded ≥2022 [diag] | uploaded windowed, adaptive | 99.88% | 0.12% (0.00/0.12) | 0.00% | 4.26% | 23 | 1151/229 |
| (iii) NORMAL 2023-25 | uploaded, fixed-1R | 99.65% | 0.35% (0.00/0.35) | 0.00% | 4.79% | 20 | 779/155 |
| **(ii) HOSTILE 2020-22** | uploaded, fixed-1R | **65.14%** | **33.18%** (0.00/33.18) | 0.00% | **8.99%** | 128 | 778/155 |
| — HOSTILE adaptive (sensitivity) | uploaded, adaptive | 63.77% | 35.32% (0.00/35.32) | 0.00% | 9.05% | 106 | 778/155 |

- **Calibration gate (B) reproduces the anchor exactly** → harness/resampler verified correct.
- **Calibration-A is WITHIN tolerance** (Δpass +0.05pp / Δbust −0.05pp / Δp99 −0.11pp). The uploaded **mixed-feed** data, windowed to the canonical period, reproduces the all-Pepperstone anchor — the off-feed Strikers (Vantage/IC Markets) do **not** materially distort the result. This substantially de-risks the feed concern.
- **Hostile-adaptive ≈ hostile-fixed** → the verdict is robust to the 1R convention.
- **100% of hostile busts are static-DD** (cumulative grind-down clusters); 0.00% daily. The failure mode is losing-streak drawdown, which `dd_protection` reaches but cannot contain at locked sizing.

## Step 2.4 — gap quantification + bust-attribution shift

**Fair-weather inflation, in plain numbers:** the locked anchor projects **99.83% pass / 0.17% bust / 4.37% p99 DD**. Under a portfolio facing the **hostile (2020-22) regime**, the *same locked portfolio* passes only **65.14%** and busts **33.18%** —

- pass over-stated by **−34.69 pp**
- bust under-stated by **~195×** (+33.01 pp)
- p99 DD under-stated by **+4.62 pp** (8.99% vs 4.37%; breaches the 5% firm static cap by ~4 pp)

**Bust attribution flips to Guardian (the brief's hypothesis, confirmed):**

| | Guardian | Aegis | DJ30 | NAS100 |
|---|---:|---:|---:|---:|
| anchor (benign-weighted) | 41.2% | 37.3% | 19.6% | 2.0% |
| **hostile 2020-22** | **57.3%** | 29.5% | 8.2% | 5.0% |

In the hostile regime Guardian's edge ≈ 0 (PF 1.01) but it keeps its full drawdown footprint, so it **drives the bust while contributing ~zero return** — its share rises 41→57%. The Strikers, which retain positive edge, contribute *less* to the tail (DJ30 19.6→8.2%). This is coherent: the bust driver is the harvest-only legs' chop-regime drawdown, not the regime-spanning Strikers.

## §4 — falsifiable hypothesis: **FALSIFIED**

> H: regime-robust IF (calib reproduces anchor) AND hostile pass ≥ **88%** AND bust ≤ **1.0%** AND p99 DD ≤ **7.0%**.

Calibration reproduces the anchor (gate PASS). Hostile: pass **65.14% < 88** ✗, bust **33.18% > 1.0** ✗, p99 DD **8.99% > 7.0** ✗ — **all three breach, decisively.** H is falsified; the anchor is confirmed **fair-weather**. A resilience action (reweight / regime-exit gate / orthogonal sleeve) is warranted — hand to a downstream reweight/gate ADR.

## Cross-reference — PR #157 decompounded sibling (corroboration)

`lab/analysis/decompound_remc_2026-06-07` (closed HOLD, `docs/adr/2026-06-07-decompound-remc-hold.md`) ran the **decompounded full-history** version of this question and is internally consistent with this run:

- `C_2020` (compounded full 2020-26, locked) = **98.22% / 1.78% / 5.48%** — already breaches both gates; the diluted full-panel blend lies between this run's benign (~99.7%) and hostile (65%) cells, as expected.
- Half-panel **H1 2020-2023 bust 8.89–13.50%** at *de-risked* allocations — this run's **pure** ≤2022 slice at *locked* allocations (33%) is the more extreme, consistent endpoint.
- NAS bust share **2.0% → 23.4%** under decompounding + full history; this run's compounded hostile NAS share stays low (5.0%) — see Concern #1.
- PR #157's verdict: **no static sizing config is regime-robust**; the hard regime only clears at ~¼ locked risk (367–591d median) → impractical. Regime-adaptive sizing is the only structural fix. **This run independently re-confirms the regime-fragility from a different instrument.**

---

## Concerns (`DONE_WITH_CONCERNS`)

1. **Compounding understates hostile risk (direction known).** The uploaded CSVs are compounded (TV default); hostile trades sit early/low-equity, so their raw $ P&L is small → the compounded bucket-resample is a **lower bound** on hostile severity. PR #157 showed decompounding adds +0.51pp p99 and un-dilutes NAS's 1000%-pyramid stack (bust share 2→23%). The decompounded hostile would be **worse** than the 33% here — which only strengthens FALSIFIED-FAIRWEATHER. The decompounded full-history is the correct instrument for the *magnitude*; this run is the brief-specified compounded bucket-resample and reconciles to Appendix A.
2. **Single-episode / thin hostile bucket.** Hostile is one regime episode (2020-2022); Aegis hostile = 43 trades. The 33% is a point estimate over bootstrapped week-blocks from a single historical hostile period, not a full-panel statistical weight. Reported per §0.5 item 4.
3. **Off-feed Strikers.** DJ30 = Vantage, NAS100 = IC Markets/USTEC (not the all-Pepperstone anchor feed). Multiplicative contract-spec gaps are absorbed by the 1R normalization; trade-selection drift is not. **Mitigant:** calibration-A (same mixed-feed data, windowed to 2022) reproduced the anchor within tolerance, so the feed mixing does not materially distort. PR #157's all-Pepperstone H1 corroborates directionally.
4. **Brief premise corrections (Rule 0).** The brief's L=8 / "iid is the production default" premise is wrong (engine is 5-day week-block bootstrap); its §0b allocations and Appendix A scale factors are stale (pre-2026-05-23). Verdict unaffected — the raw reconciliation held and the resampler/anchor were used as production defines them.
5. **Deliverable is gitignored** (`reports/*`). If this finding should be preserved/committed to inform the reweight/gate ADR, mirror it into a tracked home (`lab/analysis/`, as PR #157 did).

## §7 — parent-session review (two passes)

**Spec compliance (scope-creep check):** built exactly §2.1–§2.4 — robustness layer (all 4, per bucket) ✓, NAS100-ex-2024 ✓, three MC resamples + calibration ✓, gap + attribution ✓. Block-bootstrap (not iid) used ✓. Calibration control run and reported ✓. Locked params untouched (`git diff` empty on firm_rules / dd_protection / portfolio_mc) ✓. No core refactor — standalone harness, zero fork ✓. One in-scope addition: a hostile-adaptive sensitivity row (verdict-robustness check) + PR #157 cross-reference (corroboration) — both serve the question, neither changes the spec.

**Quality:** stress MC methodologically sound (production resampler verbatim; calibration gate reproduces anchor exactly; calib-A confirms data-equivalence). Single-episode + compounding + off-feed caveats surfaced prominently, not buried. Thresholds applied as written, not amended.

**Final consolidated read (2.1–2.4 together):** internally consistent. The hostile **bust attribution** (Guardian 57.3%) is coherent with the robustness layer — Guardian's hostile PF 1.01 / drop-top-10 PF 0.03 (zero edge, full drawdown footprint) is exactly what makes it the dominant bust driver despite contributing ~zero return. Attribution sums to 100% (57.3+29.5+8.2+5.0). The normal-cell (99.65% pass, clears gates) vs hostile-cell (65% pass) contrast cleanly isolates the regime effect on equal-sized (~155 week-block) panels.

## §10 — audit hook outputs

```
FIRM_RULES_CLEAN · DDP_CLEAN · PORTFOLIO_MC_CLEAN
resample_unit=week_block_5day · block_len_days=5 · block_bootstrap=true · iid=false
CALIB_OK: |99.83−99.83|≤0.5 ∧ |0.17−0.17|≤0.1 ∧ |4.37−4.37|≤0.3  → PASS
hostile: pass 65.14% / bust 33.18% / p99 DD 8.99%
```
