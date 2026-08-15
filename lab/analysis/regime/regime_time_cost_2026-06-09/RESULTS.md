# Regime-stagnation time-cost — Q-REGIME-TIME-1 candidate (2026-06-09)

**Status:** ACTIVE — Q-REGIME-TIME-1 RESOLVED-LARGE, but stagnation's recoverable cost is tail-risk/survivability, NOT speed; both LARGE cells sit at the band edges and F1 discounts the benefit to an upper bound
**Brief:** [`docs/ltm/briefs/Q-REGIME-TIME-1-cc-handoff.md`](../../../../docs/ltm/briefs/Q-REGIME-TIME-1-cc-handoff.md)
**Script:** [`regime_time_cost.py`](regime_time_cost.py) (`--all`, 10K × 3 seeds (42, 123, 2026), C2 dd_protection 1.5%/0.40×)
**Prior path:** `ops/reports/regime_time_cost/RESULTS.md` (relocated 2026-08-03; now under `lab/analysis/regime/`; `ops/reports/` deleted)
**Panel:** 2020-01 → 2026-06 Pepperstone BT-OFF + daily-cap, decompounded static (roe × $200K), 1R pinned = alloc × $200K, 334 week-blocks (same basis as the 2026-06-07 HOLD ADR)
**Gates:** pre-registered 2026-06-09 (§0.5 A3, BEFORE execution) — LARGE: any non-stress cell Δmedian ≥ 5d OR Δp90 ≥ 15d at Δbust ≤ +0.25pp; SMALL: all cells Δmedian < 2d AND Δp90 < 5d. Δmedian/Δp90 = baseline − cell (positive = faster); Δbust = cell − baseline.

## Verdict — **RESOLVED-LARGE** (with the F1 discount stated below)

Two non-stress cells clear the pre-registered LARGE band — `PF 2.0 / 2 trades / 0.50%` (Δp90 +15d) and `PF 2.0 / 3 trades / 0.50%` (Δmedian +5d, Δp90 +22d) — both at strongly *negative* Δbust (−1.6 / −2.0pp), trivially inside the ≤ +0.25pp constraint. The stress variant (forced losses in the 2020-04→06 and 2021-12→2022-02 bust-archetype windows) does **not** flip the sign (Δmedian +5d, Δbust −0.93pp). Per §6 this opens the full Pre-Q (Q-REGIME-TIME-1) for regime-conditional R&D intake. **F1 (mandatory):** these numbers are an *upper bound* on the benefit, not a forecast — they assume a strategy that trades *only* dead weeks at PF 2.0 with zero correlation to the existing four outside the stress windows; the R&D pipeline's validated-concept base rate is **0/4**, which discounts the expected value of chasing this ceiling. The honest characterization: at realistic validated quality the **median stage-pass barely moves (0–5 days)**; the recoverable cost of stagnation lives in the **bust rate (−0.4 to −2.0pp) and the slow-path tail (p90 −1 to −22 days)**. The efficiency case for regime-complementary R&D is a *tail-risk and survivability* case, not a speed case — and both LARGE cells sit exactly at the band edges, so a Pre-Q should treat this as a threshold-grade signal, not a comfortable margin.

## Step 2.1 — Labeled panel (A1: dead = calendar week, total portfolio entries < 2)

- 334 Mon-anchored week-blocks, 2020-01-06 → 2026-06-02; **77 dead (23.1%)**.
- Dead share by year: 2020 **29%**, 2021 **38%**, 2022 **29%**, 2023 **8%**, 2024 21%, 2025 12%, 2026 **29%** (partial year). Stagnation is regime-concentrated — same H1-heavy split as the bust risk in the HOLD ADR.
- Run-length distribution (the serial-dependence object): median **1w**, p90 **2w**, longest **5w**. Alive runs: median 2w, p90 8w.
- A1 sensitivity (trailing-2-week |net P&L| < 0.25% × $200K): only 5.4% dead, 75.8% agreement — almost any single trade moves > $500, so the P&L band rarely fires. The **activity definition is the binding one**; results below use it.
- Live-texture note: the motivating 7-week flat (Apr 20 →) **exceeds the longest dead run in the 6.4-year panel (5w)** under this definition — the live episode is more extreme than anything the backtest panel contains, which itself argues for pricing the tail, not the median.

## Step 2.2 — Baseline MC (resampler that preserves dead-run serial dependence)

**Resampler choice (load-bearing §7 check):** contiguous multi-week block bootstrap over the chronological week-block sequence, block length pre-registered as L = max(8, p90 dead-run) = **8 weeks**. Justification against the Step 2.1 run-length distribution: L = 8 ≥ 4× the p90 dead-run (2w) and ≥ the longest observed run (5w), so every historical dead run can be reproduced intact inside a single block; a fitted two-state (Markov) resampler was rejected because it imposes geometric run lengths instead of preserving the empirical distribution directly. The production iid weekly sampler was run **once, for reconciliation only** (§5-F2: it destroys exactly the structure being priced).

| config | pass | bust | median d | p90 d | p99 DD |
|---|---|---|---|---|---|
| iid weekly (reconcile only) | 97.04% | 2.96% | 31 | 125 | 5.93% |
| **block L=8 (BASELINE)** | **96.57%** | **3.43%** | **31** | **133** | **5.78%** |

- **Reconciliation:** the iid run reproduces the pinned S_2020 anchor (97.04 / 2.96 / 5.93, median 31) to the decimal — harness fidelity confirmed. Divergence vs the locked 26d anchor is fully accounted for by the panel: window 2022-26 → 2020-26 plus decompounding (attribution table in `lab/analysis/decompound_remc_2026-06-07/RESULTS.md`); no new divergence introduced by this analysis.
- **Serial-dependence premium:** preserving dead-run clustering costs **+0.46pp bust and +8 p90 days** vs iid (median unchanged). This is the stagnation structure the iid sampler was hiding — modest at this panel's run lengths, but real and in the harmful direction.

**A2 secondary — banded skim-cycle proxy** (descriptive only; $805K mechanics undocumented, so this prices "+5% skim" cycles, not the firm's scaling path):

| k-th skim | reach rate | median days | p90 days |
|---|---|---|---|
| 1 | 96.6% | 31 | 133 |
| 2 | 94.0% | 82 | 217 |
| 4 | 88.9% | 191 | 370 |
| 8 | 79.3% | 403 | 649 |
| 12 | 70.3% | 617 | 907 |

Cycle time stretches as horizon grows (31 → ~50d/cycle by k=8–12) because later cycles inevitably traverse dead-regime stretches; ~30% of paths die (bust) before 12 skims.

## Step 2.3 — Counterfactual sweep (synthetic strategy active ONLY in dead weeks)

Win p=0.5; win = +PF × risk × $200K, loss = −risk × $200K; trades Mon/Wed/Fri of dead weeks; synthetic column participates in dd_protection scaling; paired block draws vs baseline (same seeds, separate synth RNG stream) so deltas sit above the MC noise floor.

| cell (PF / trades / risk) | median d | p90 d | bust | Δmedian | Δp90 | Δbust |
|---|---|---|---|---|---|---|
| 1.5 / 1 / 0.25% | 31 | 132 | 3.01% | +0 | +1 | −0.42pp |
| 1.5 / 1 / 0.50% | 31 | 132 | 3.02% | +0 | +1 | −0.41pp |
| 1.5 / 2 / 0.25% | 31 | 132 | 2.70% | +0 | +1 | −0.73pp |
| 1.5 / 2 / 0.50% | 30 | 126 | 2.54% | +1 | +7 | −0.89pp |
| 1.5 / 3 / 0.25% | 30 | 128 | 2.45% | +1 | +5 | −0.98pp |
| 1.5 / 3 / 0.50% | 27 | 123 | 2.37% | +4 | +10 | −1.05pp |
| 2.0 / 1 / 0.25% | 31 | 131 | 2.70% | +0 | +2 | −0.73pp |
| 2.0 / 1 / 0.50% | 31 | 128 | 2.58% | +0 | +5 | −0.85pp |
| 2.0 / 2 / 0.25% | 30 | 127 | 2.24% | +1 | +6 | −1.19pp |
| **2.0 / 2 / 0.50%** | 27 | 118 | 1.83% | +4 | **+15** | −1.60pp |
| 2.0 / 3 / 0.25% | 27 | 122 | 1.83% | +4 | +11 | −1.59pp |
| **2.0 / 3 / 0.50%** | **26** | **111** | **1.47%** | **+5** | **+22** | **−1.96pp** |
| STRESS (2.0 / 3 / 0.50%, archetype-window losses) | 26 | 117 | 2.49% | +5 | +16 | −0.93pp |

Pattern: benefit scales with weekly synthetic edge (n × risk × (PF−1)/2) and is monotone; the conservative half of the grid (PF 1.5 and/or 0.25%) is **SMALL-grade** (Δmedian ≤ 1d except the 3-trade cell). The bust-archetype stress costs ~1pp of the bust reduction but leaves time recovery intact — dead-week income is additive even when it loses exactly in the historical bust windows, because those windows' busts are driven by the live strategies' own drawdowns.

## Disposition

Per §6, RESOLVED-LARGE opens a full Pre-Q (Q-REGIME-TIME-1) on regime-conditional R&D intake — **authoring that Pre-Q (and any intake-filter design) is explicitly out of scope here (F3)**. This report is an input to, not a pre-emption of, the 2026-08-08 quarterly HOLD disposition (F5). What the Pre-Q must confront up front: (1) the gate fired at the band edges and only at the aggressive corner of a grid whose realism is already an upper bound (F1, 0/4 base rate); (2) the payoff is bust-tail reduction, not pass speed — if the programme's binding constraint is survivability in the 2020-23-like regime (per the HOLD ADR), that is exactly the constraint a dead-week-complementary stream relieves; if the constraint is median pass time, this analysis says R&D will not buy it.

**Status: DONE_WITH_CONCERNS** — concerns: (a) verdict sits exactly on the pre-registered thresholds (threshold-grade, not margin-grade); (b) the live 7-week flat exceeds the panel's longest dead run, so the panel may understate current-regime stagnation; (c) $805K milestone metric re-scoped to stage-pass + skim proxy (mechanics undocumented — supply them to upgrade A2). Step 2.2 reconciliation is clean (no unexplained divergence).
