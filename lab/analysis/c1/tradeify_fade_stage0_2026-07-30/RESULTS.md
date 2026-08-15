**Theme:** c1
# Tradeify-native fade — Stage 0 + Stage 1

**Status:** **ACTIVE** -- Stage 0 instrumentation complete; Stage 1 region computed at 1x/2x/4x; no mechanism scored, K=0, $0 spend

**Screens only; admits nothing.** No candidate performance was read, no trial count opened, no data purchased.

## Stage 0.1 — 1m panel integrity

- panel: `MYM` — **2,480,324 bars**, 1,871 trade dates
- span: 2019-05-05 20:00:00-04:00 -> 2026-07-29 19:59:00-04:00
- verdict: **FAIL**

**Zero-bar business days (18):** exchange holidays are expected members; the load-bearing one is **2020-02-28**, a non-holiday Friday genuinely absent for MYM (PD-8). Any 2020-spanning day count is off by one, and the missing day is a maximum-volatility outlier, so 2020 statistics are biased calm.

```
2019-12-25, 2020-01-01, 2020-02-28, 2020-04-10, 2020-12-25, 2021-01-01, 2021-12-24, 2022-04-15, 2022-12-26, 2023-01-02, 2023-12-25, 2024-01-01, 2024-03-29, 2024-12-25, 2025-01-01, 2025-04-18, 2025-12-25, 2026-01-01
```

**Short sessions:** **82** trade dates hold fewer than 388 of 390 RTH bars, of which **1** are below 25% completeness (worst: 2020-06-30 at 41/390). Exchange half-days are legitimate members — this is a review list. It is reported separately from the zero-bar list because a session that EXISTS but is 89% empty is invisible to both a zero-bar scan and a median-completeness check.

**16:15-16:30 ET maintenance slot.** The HALT was in force through ~2021-Q2 and was removed afterwards, so the count below is the count of bars that PRINTED in that quarter-hour: **a low count means the halt was active, a high count means it was gone.** The series therefore rises. Any per-day bar-count normalization will read this as a spurious 2019-21 vs 2022+ regime break that is pure exchange calendar — and it sits exactly where the 16:45 ET flat deadline binds. Zero-count years are printed, not dropped; they are the informative ones.

| year | bars printed in the 16:15-16:30 slot | halt in force? |
|---|---:|---|
| 2019 | 0 | yes (slot empty) |
| 2020 | 3 | yes (slot empty) |
| 2021 | 1,912 | no |
| 2022 | 3,747 | no |
| 2023 | 3,663 | no |
| 2024 | 3,678 | no |
| 2025 | 3,664 | no |
| 2026 | 2,139 | no |

## Stage 0.2 — TV/Databento roll exposure

- rolls detected: **29**
- exposure windows: **29**
- sessions exposed: **87** (4.65%)

TradingView rolls 1-2 sessions earlier than Databento. Signals originate on TV and are scored on Databento, so on these sessions the feeds disagree about which contract is in force. **Disposition is an operator ruling** — see `docs/notes/2026-07-30-tv-databento-roll-window-ruling.md`. It must be frozen before any mechanism is scored; choosing after seeing scores is a selection effect.

## Stage 0.3 — cost per notional

The third-leg screen's `cost_tax` normalizes per contract against a fixed $125/day ceiling, so symbols with equal tick value and commission score identically there regardless of notional. Per **notional** the ordering separates them, and that is the denominator a cost-law question needs. MNQ and MYM carry an IDENTICAL $2.82 round trip and differ ~2x in bp purely because MNQ's contract is ~2x the notional.

**Index levels are the median close over 2023-01-01 to 2023-12-31** — not current levels. `cost_bp` moves inversely with the index, so a pin taken in a lower-priced window OVERSTATES cost relative to today. Read the `index_level` column before quoting any bp figure.

| symbol   | product_group   |   index_level |   point_value_usd |   rt_cost_usd |   notional_usd |   cost_bp |   cost_points |
|:---------|:----------------|--------------:|------------------:|--------------:|---------------:|----------:|--------------:|
| MNQ      | Equity Index    |      14823    |               2   |          2.82 |        29646   |    0.9512 |         1.41  |
| MYM      | Equity Index    |      34027    |               0.5 |          2.82 |        17013.5 |    1.6575 |         5.64  |
| M2K      | Equity Index    |       1853.2  |               5   |          2.82 |         9266   |    3.0434 |         0.564 |
| MCL      | Energy          |         77.12 |             100   |          4.12 |         7712   |    5.3423 |         0.041 |

Stage-0 item-3 debt discharged: M2K and MCL now have measured 2023 medians (alongside MNQ/MYM). Ordering by `cost_bp` is the §4.2 input-1 ranking — never invented levels.

## Stage 1 — feasible region

`COST_LAW_MULTIPLE = 4.0` is a T1 pre-screen constant, **not a ratified gate**. Which multiple governs admission is an operator decision, so all three are reported. Moving the multiple to clear a gate is the spec's section 7 goalpost move — a region non-empty only at 1x is a reported result, not a pass.

> **Governing multiple: 4.0x**, fixed in advance of scoring.

A cell is `feasible` only if **all four** limbs hold: payability (all-win day ≥ $200), the $750 worst-day bound, the σ window (`min_sharpe` ≤ **1.83**, the best annualized Sharpe this estate has ever validated — Aegis; the other locked legs run 1.11–1.48), and **expressibility** (the nearer bracket leg must fit inside the instrument's own measured full-session σ). The σ limb is the only one that TIGHTENS as the stop widens, which is why a larger multiple is more demanding, not less.

**`min_sharpe` is NOT comparable across R:R columns.** The grid pins `p`, while the random-walk baseline `S/(T+S)` moves with R:R — so a low-`min_sharpe` cell in the R:R 1.0 column is buying that Sharpe with a much larger edge over a coin flip, not with a friendlier multiple. Compare on `excess_wr_required` (the `c/(T+S)` quantity out of which R:R cancels, §3.1). Reading the columns as interchangeable produced a published claim that 4× left one cell needing Sharpe 1.81 — it leaves two, and the second needs 0.814. Corrected 2026-07-31.

### multiple 1.0x — **0 of 12 cells feasible**

|   rr |   n_trades |   stop_pts |   target_pts |   sigma_d |   min_sharpe |   excess_wr_required |   all_win_day |   all_lose_day | payable   | worst_day_ok   | sharpe_reachable   | expressible   | feasible   |
|-----:|-----------:|-----------:|-------------:|----------:|-------------:|---------------------:|--------------:|---------------:|:----------|:---------------|:-------------------|:--------------|:-----------|
| 0.66 |          1 |       71.4 |         47.1 |      28.3 |        2.247 |              0.04759 |          20.7 |           38.5 | False     | True           | False              | True          | False      |
| 0.66 |          2 |       71.4 |         47.1 |      40   |        1.589 |              0.04759 |          41.5 |           77   | False     | True           | True               | True          | False      |
| 0.66 |          3 |       71.4 |         47.1 |      49   |        1.297 |              0.04759 |          62.2 |          115.5 | False     | True           | True               | True          | False      |
| 0.66 |          4 |       71.4 |         47.1 |      56.5 |        1.123 |              0.04759 |          83   |          154.1 | False     | True           | True               | True          | False      |
| 0.66 |          5 |       71.4 |         47.1 |      63.2 |        1.005 |              0.04759 |         103.7 |          192.6 | False     | True           | True               | True          | False      |
| 0.66 |          6 |       71.4 |         47.1 |      69.2 |        0.917 |              0.04759 |         124.4 |          231.1 | False     | True           | True               | True          | False      |
| 1    |          1 |       18.8 |         18.8 |       9   |        7.081 |              0.15    |           6.6 |           12.2 | False     | True           | False              | True          | False      |
| 1    |          2 |       18.8 |         18.8 |      12.7 |        5.007 |              0.15    |          13.2 |           24.4 | False     | True           | False              | True          | False      |
| 1    |          3 |       18.8 |         18.8 |      15.5 |        4.089 |              0.15    |          19.7 |           36.7 | False     | True           | False              | True          | False      |
| 1    |          4 |       18.8 |         18.8 |      17.9 |        3.541 |              0.15    |          26.3 |           48.9 | False     | True           | False              | True          | False      |
| 1    |          5 |       18.8 |         18.8 |      20.1 |        3.167 |              0.15    |          32.9 |           61.1 | False     | True           | False              | True          | False      |
| 1    |          6 |       18.8 |         18.8 |      22   |        2.891 |              0.15    |          39.5 |           73.3 | False     | True           | False              | True          | False      |

### multiple 2.0x — **2 of 12 cells feasible**

|   rr |   n_trades |   stop_pts |   target_pts |   sigma_d |   min_sharpe |   excess_wr_required |   all_win_day |   all_lose_day | payable   | worst_day_ok   | sharpe_reachable   | expressible   | feasible   |
|-----:|-----------:|-----------:|-------------:|----------:|-------------:|---------------------:|--------------:|---------------:|:----------|:---------------|:-------------------|:--------------|:-----------|
| 0.66 |          1 |      142.8 |         94.2 |      56.5 |        1.123 |              0.04759 |          44.3 |           74.2 | False     | True           | True               | True          | False      |
| 0.66 |          2 |      142.8 |         94.2 |      79.9 |        0.794 |              0.04759 |          88.6 |          148.4 | False     | True           | True               | True          | False      |
| 0.66 |          3 |      142.8 |         94.2 |      97.9 |        0.907 |              0.04759 |         132.9 |          222.6 | False     | True           | True               | True          | False      |
| 0.66 |          4 |      142.8 |         94.2 |     113.1 |        1.047 |              0.04759 |         177.2 |          296.8 | False     | True           | True               | True          | False      |
| 0.66 |          5 |      142.8 |         94.2 |     126.4 |        1.17  |              0.04759 |         221.5 |          371.1 | True      | True           | True               | True          | True       |
| 0.66 |          6 |      142.8 |         94.2 |     138.5 |        1.282 |              0.04759 |         265.8 |          445.3 | True      | True           | True               | True          | True       |
| 1    |          1 |       37.6 |         37.6 |      17.9 |        3.541 |              0.15    |          16   |           21.6 | False     | True           | False              | True          | False      |
| 1    |          2 |       37.6 |         37.6 |      25.4 |        2.504 |              0.15    |          32   |           43.2 | False     | True           | False              | True          | False      |
| 1    |          3 |       37.6 |         37.6 |      31.1 |        2.044 |              0.15    |          47.9 |           64.9 | False     | True           | False              | True          | False      |
| 1    |          4 |       37.6 |         37.6 |      35.9 |        1.77  |              0.15    |          63.9 |           86.5 | False     | True           | True               | True          | False      |
| 1    |          5 |       37.6 |         37.6 |      40.1 |        1.583 |              0.15    |          79.9 |          108.1 | False     | True           | True               | True          | False      |
| 1    |          6 |       37.6 |         37.6 |      43.9 |        1.446 |              0.15    |          95.9 |          129.7 | False     | True           | True               | True          | False      |

### multiple 4.0x — **2 of 12 cells feasible**

|   rr |   n_trades |   stop_pts |   target_pts |   sigma_d |   min_sharpe |   excess_wr_required |   all_win_day |   all_lose_day | payable   | worst_day_ok   | sharpe_reachable   | expressible   | feasible   |
|-----:|-----------:|-----------:|-------------:|----------:|-------------:|---------------------:|--------------:|---------------:|:----------|:---------------|:-------------------|:--------------|:-----------|
| 0.66 |          1 |      285.6 |        188.5 |     113.1 |        1.047 |              0.04759 |          91.4 |          145.6 | False     | True           | True               | True          | False      |
| 0.66 |          2 |      285.6 |        188.5 |     159.9 |        1.48  |              0.04759 |         182.8 |          291.2 | False     | True           | True               | True          | False      |
| 0.66 |          3 |      285.6 |        188.5 |     195.8 |        1.813 |              0.04759 |         274.3 |          436.8 | True      | True           | True               | True          | True       |
| 0.66 |          4 |      285.6 |        188.5 |     226.1 |        2.094 |              0.04759 |         365.7 |          582.4 | True      | True           | False              | True          | False      |
| 0.66 |          5 |      285.6 |        188.5 |     252.8 |        2.341 |              0.04759 |         457.1 |          728   | True      | True           | False              | True          | False      |
| 0.66 |          6 |      285.6 |        188.5 |     276.9 |        2.564 |              0.04759 |         548.5 |          873.6 | True      | False          | False              | True          | False      |
| 1    |          1 |       75.2 |         75.2 |      35.9 |        1.77  |              0.15    |          34.8 |           40.4 | False     | True           | True               | True          | False      |
| 1    |          2 |       75.2 |         75.2 |      50.7 |        1.252 |              0.15    |          69.6 |           80.8 | False     | True           | True               | True          | False      |
| 1    |          3 |       75.2 |         75.2 |      62.1 |        1.022 |              0.15    |         104.3 |          121.3 | False     | True           | True               | True          | False      |
| 1    |          4 |       75.2 |         75.2 |      71.7 |        0.885 |              0.15    |         139.1 |          161.7 | False     | True           | True               | True          | False      |
| 1    |          5 |       75.2 |         75.2 |      80.2 |        0.792 |              0.15    |         173.9 |          202.1 | False     | True           | True               | True          | False      |
| 1    |          6 |       75.2 |         75.2 |      87.9 |        0.814 |              0.15    |         208.7 |          242.5 | True      | True           | True               | True          | True       |

## Stage 1 — expressibility limb (added 2026-07-31)

The other three limbs derive `sigma_d` **from** the assumed bracket and trade count, so none of them can ask whether the instrument is capable of producing `n` such excursions. This limb asks it directly: the **nearer** bracket leg (a trade resolves at whichever barrier is reached first, not at the stop) must fit inside the instrument's own measured full-session σ.

σ is the LARGEST cell on each instrument's 72-cell surface, ex-FOMC primary — the most generous reading, so a cell failing here fails at every shorter hold. The converse does **not** hold: passing against the max says nothing about the cell a configuration is actually held on. An instrument with no measured σ compares `NaN` ⇒ **False**: unmeasured is not expressible until someone measures it. Silent-pass on absence is the failure this limb closes.

**Provenance is mixed, deliberately.** MYM / M2K / M6A are borrowed from `c1_thirdleg_instrument_map_2026-07-27/RESULTS_stage2.md` (2021-08 → 2023-12, n=219 at the max cell). **MCL is native** — `RESULTS_sigma_native.md`, `mcl_1m.parquet` 2023-01-02 → 2023-12-29, n=90 — per the operator ruling `SIGMA-NATIVE-2026-07-31`, which retired the borrowed $112.70 for the **$112.17** measured on the panel this program holds. Same function, same basis, same max-cell rule; only the cohort differs. MCL is the ruled instrument (`CONFIG-B-MCL-2026-07-31`) and the only one whose σ is load-bearing for an admission decision here.

| symbol   |   rr |   n_trades |   barrier_usd |   session_sigma_usd | expressible   |   subperiod_ratio |   min_sharpe |   implied_annualized_sr | feasible   |
|:---------|-----:|-----------:|--------------:|--------------------:|:--------------|------------------:|-------------:|------------------------:|:-----------|
| MYM      | 0.66 |          3 |         94.24 |              119.44 | True          |             1.367 |        1.813 |                    2.74 | True       |
| MYM      | 1    |          6 |         37.6  |              119.44 | True          |             0.771 |        0.814 |                   12.23 | True       |
| M2K      | 0.66 |          3 |         94.24 |              115.58 | True          |             1.412 |        1.813 |                    2.74 | True       |
| M2K      | 1    |          6 |         37.6  |              115.58 | True          |             0.797 |        0.814 |                   12.23 | True       |
| MCL      | 1    |          4 |         54.93 |              112.17 | True          |             0.979 |        0.97  |                    9.98 | True       |
| MCL      | 1    |          5 |         54.93 |              112.17 | True          |             1.095 |        1.085 |                   11.16 | True       |
| MCL      | 1    |          6 |         54.93 |              112.17 | True          |             1.2   |        1.189 |                   12.23 | True       |
| M6A      | 1    |          5 |         50.93 |               30.91 | False         |             3.685 |        1.006 |                   11.16 | False      |
| M6A      | 1    |          6 |         50.93 |               30.91 | False         |             4.036 |        1.102 |                   12.23 | False      |

`subperiod_ratio` = `barrier·√n / σ_session` is a **DIAGNOSTIC, not a gate** — the tighter reading in which the session is partitioned into `n` intervals of `σ/√n`. Promoting it to a gate is a modelling choice and belongs to an operator ruling, like the cost multiple.

## Stage 1 — the implied-edge diagnostic (added 2026-07-31)

**All four limbs interrogate the GEOMETRY. None interrogates the EDGE the geometry assumes.** `sharpe_reachable` looks like it does — it is the limb carrying `SHARPE_CEILING`, whose docstring reads *"plausibility ceiling on the Sharpe a mechanism could deliver … a cell needing more than the best thing ever found here is not a design, it is a wish"*. But it applies that ceiling to `min_sharpe_for_sigma(σ_d)`, a σ-**window compatibility** bound, and a **lower** bound at that. Different quantity. This is the same defect class the `expressible` limb was added to close — every prior limb derives `σ_d` *from* the assumed bracket — one level up.

`implied_annualized_sr` reports what a cell actually assumes: `per_trade_sharpe(p, rr) · √n · √252`. It is **REPORTED, NOT GATED**, and is deliberately absent from the `feasible` conjunction.

**2026-08-13 intercept:** the 2026-08-10 promotion of this column to a freeze-time FAIL is **superseded** ([`ADR 2026-08-13`](../../../docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)). The three frozen MCL cells below remain `feasible = True` and are **reinstated as geometry**. A Sharpe above the Aegis 1.83 cohort is not a kill. Measured results still gate on DSR-at-K. No mechanism is admitted by the reopen.

Promoting it was an operator modelling ruling (2026-08-10); that ruling is reversed. The cost multiple remains a separate frozen ruling.

**The finding, swept over `p`, both R:R columns and n=1..8: the minimum implied annualized Sharpe anywhere in the admitted region is ≈2.98 — 1.63× the 1.83 ceiling.** Not one admitted cell is plausible on the estate's own yardstick. At the pinned `p`=0.65 the three frozen MCL cells imply 9.98 / 11.16 / 12.23, i.e. 5.5–6.7×.

Units are like-for-like: 1.83 is Aegis at **1.828**, the annualized Sharpe of a daily P&L stream measured by `breadth.load_baseline_panel` over **1141 business days** (Pepperstone 2026-05-24 vintage; Q-GATECART-1 pre-registration §B, which also records Guardian 1.48 · DJ30 1.11 · NAS100 1.45 and a portfolio-of-4 reference of 2.80). The implied figure is the same statistic. The frequency difference is not an artefact of the comparison — trading a real edge more often genuinely does produce a better daily equity curve.

Two further properties of the region, recorded because both were previously unstated:

- **`excess_wr_required` is an algebraic identity**, `p − 1/(1+rr)`. The cost and the multiple cancel *exactly* (verified: 0 mismatches over 4 instruments × 4 multiples × 8 cells). It restates the assumed `p` and carries no information about the instrument or the cost law. The cost-multiple ruling's **verdict** survives — cell counts depend on the multiple through the other limbs — but its stated reasoning, that this column is "the comparable axis", does not.
- **Payability caps the assumed win rate from ABOVE.** A higher assumed edge means a tighter cost-floor stop, hence a smaller target, hence an all-win day that fails the $200 threshold. At n=4 the cap is `p ≤ 0.6523`; the pinned `P_WIN = 0.65` sits essentially **on** it, clearing payability at $203.30 against $200. The region is not centred on a neutral edge assumption — it is pressed against the maximum the venue permits.

## What this does NOT establish

A feasible region is not an edge. It states which bracket geometries could survive the venue if a mechanism delivered the required Sharpe — it says nothing about whether any mechanism does. Admission remains the frozen Part A gate (bust <= 3.0% and pass >= 50%) on a pre-registered mechanism, at Stage 2.
