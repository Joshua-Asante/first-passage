# Q-ICT-MNQ-1 — RESULTS (Layers 1H + 1M, MNQ native, databento)

**Date:** 2026-08-03
**Pre-registration:** [`PREREG_1H_1M.md`](PREREG_1H_1M.md) — frozen at commit `9720ffa`, after the
$0.00 cost dry-run and **before any bar was pulled**.
**Companion:** [`RESULTS.md`](RESULTS.md) (Layers D + W).
**Governance:** these are **FRESH verdicts, not confirmations** — US500's 1H was FALSIFIED and its
1M INSUFFICIENT-N, so there is no closed RESOLVED finding to confirm, and
`CONFIRM-FREE-NODEPLOY-2026-08-03` explicitly excludes them. Still $0 / K=0 / no manifest.

**Data:** `MNQ.v.0` continuous, databento GLBX.MDP3, both pulled at **$0.0000**:
1H = 42,786 bars (2019-05-06 → 2026-08-02); 1m = 2,552,025 bars.

---

## 1. Layer 1H — **FALSIFIED** (and this time the verdict is well-powered)

Harness `harness_1h.verdict_1h()` run **UNMODIFIED**. Zones computed by its own
`zone_series`/`gate_zone_series` from OHLC; its internal look-ahead audit returned
**`ok=True`, mismatch 0.0000** on both zones — the reconstruction is consistent across
Pine's resolution-bar and the decision-bar indexings.

> **The re-proposal bar is now discharged.** US500's 1H FALSIFIED verdict rested on a single
> benign regime (3,039 bars, 2025-12 → 2026-06), and its bar was *"multi-regime 1H data, not
> re-tuning."* This run is 42,786 bars spanning 2020 chop, the 2022 bear, and the 2023-26 trend,
> at **effective N 1,852 (prem) / 1,199 (disc)** versus US500's 151 / 92 — roughly **12× the
> power**, on the exact data the bar demanded.

| Zone | stride rate | stride CI | block rate | block CI | clears ≥2pp? |
|---|---|---|---|---|---|
| **premium → down** | 0.4537 | [0.4328, 0.4746] | 0.4542 | [0.4382, 0.4698] | **No** (below 0.5 entirely) |
| **discount → up** | 0.5394 | [0.5145, 0.5643] | 0.5420 | [0.5224, 0.5607] | **No** (stride lb 0.5145 < 0.52) |

**VERDICT[1H] = FALSIFIED** — *"both premium-down AND discount-up de-overlapped rate CIs straddle
0.5 after the 9-cell penalty — the split is decorative."* `licenses_1m_gate = False`.

Three independent limbs each kill it, so the result is not a single-threshold artifact:

1. **Premium→down is dead, not marginal** — 0.4537, with the whole CI *below* 0.5. The premium
   zone resolves **upward** more often than down, i.e. **opposite** to the ICT claim.
2. **Discount→up fails the ≥2pp margin under stride** (lb 0.5145 vs the 0.52 required), and the
   gate demands both stride *and* block.
3. **Discount→up does not beat its own placebo floor** — measured 0.5394 against a sign-shuffle
   placebo of **0.5485**. The real effect is *weaker than its null*. This is the cleanest kill of
   the three and needs no threshold at all.

The 9-cell selection penalty is consistent with that: the best discount cell (`lookN=80,
eqBand=0.05`, rate 0.5517) passes DSR but **fails Bonferroni** (`bonf_lo` 0.5135 vs `winner_ci_lo`
0.5275 — reported by the harness as `pass_bonf: False`).

**Transfer pre-gate:** the **range-LAG** axis clears comfortably (agreement **0.9939**, gap
**0.0044** vs the ≥0.90 / ≤3pp requirement). The **price-BASIS** axis is `NOT-RUN`, declared in
advance — it needs the lost Pine's `netBias`/`inKZ` columns. This is **not** what killed the
layer: the falsification lands at the unconditional gate, exactly as it did on US500 ("1H needs
NO 1M export — it falsified at the unconditional gate").

**Reading:** the premium/discount mean-reversion gate is now falsified on **two instruments**, and
on MNQ under the multi-regime condition its own re-proposal bar named. The structural tension the
original campaign flagged — the 1H mean-reversion gate fights the trend bias the 1M layer needs —
is confirmed and quantified: premium continues **up** (0.4537 down-rate) in a secular uptrend.

---

## 2. Layer 1M — fill-mechanics probe: **WALL-NOT-CONFIRMED** (and the reason matters)

Order-free measurement, per [`PREREG_1H_1M.md`](PREREG_1H_1M.md) §3. Not the archived 16-cell
strategy ablation (that would be K-bound candidate generation).

| | |
|---|---|
| 1m bars | 2,552,025 |
| roll-window bars excluded as FVG origins | 274,864 |
| displacement FVGs detected | **128,089** (bull 61,579 / bear 66,510) |
| eligible (complete 6-bar window) | 128,089 |
| retraced to FVG mid within 6 bars | **75,646** |
| **RETRACE RATE at the frozen `retraceK=6`** | **59.06%** |
| median bars to touch | 2.0 |

Against the pre-registered boundaries (<5% / 5–20% / >20%): **WALL-NOT-CONFIRMED**.

**Sensitivity curve (disclosure only — the verdict reads `retraceK=6` and only `retraceK=6`):**

| `retraceK` | n | hits | rate | median bars |
|---|---|---|---|---|
| 3 | 128,089 | 59,799 | 46.69% | 1.0 |
| **6** | 128,089 | 75,646 | **59.06%** | 2.0 |
| 12 | 128,088 | 88,661 | 69.22% | 2.0 |
| 30 | 128,088 | 102,176 | 79.77% | 3.0 |

### 2.1 The regime confound was tested and eliminated

US500's 0/247 came from a ~2-day single-regime window, so "different regime, not different
instrument" was the obvious alternative explanation. It does not survive contact with the data —
the rate is **flat to within 2.4 percentage points across eight years**, including the 2020 crash,
the 2022 bear, and the 2023-26 melt-up:

| year | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| retrace rate @ k=6 | 58.39% | 58.31% | 58.49% | 58.03% | 59.95% | 60.47% | 59.90% | 58.71% |
| n | 12,379 | 18,660 | 18,050 | 17,557 | 17,119 | 17,166 | 17,105 | 10,053 |

**Regime does not explain the gap.** A 0% fill rate is not a draw from this distribution under any
year.

### 2.2 What this does and does not license — read before citing 59%

**It does NOT mean the ICT 1M strategy would have filled.** The measured quantity is narrower than
the strategy's fill rate, and one difference is load-bearing:

- **This probe measures from the FVG registration bar.** The deployed strategy places its limit
  only *after* the raid → FVG → DOL-target chain validates, which is some number of bars later —
  by which time price may already have left the zone. A retrace that this probe counts may be one
  the strategy's order was never resting for.
- The probe applies **no gate stack** (bias / PD / killzone). US500's 0/247 came from the
  all-gates-off cell, which narrows but does not close this gap.

**What it does establish** is that the archived closure's stated mechanism claim — *"on a fast 1m
index, displacement FVGs continue rather than retrace within 6 bars,"* logged as instrument-general
with HIGH confidence — is **false on MNQ**, decisively (59% vs 0%, n=128,089, stable across eight
years). Whatever produced 0/247 on US500, it is **not** the price-behavior law the closure named.
The honest residual hypotheses are (a) order-placement timing inside the strategy, (b) a US500
CFD-feed or venue artifact, or (c) a defect in the deployed 1M script — and this study does not
discriminate among them.

> **Discriminated 2026-08-04 — see [`RESULTS_1M_DIAG.md`](RESULTS_1M_DIAG.md).** (a) refuted in
> both forms (raid-conditioning leaves the rate at 59.01%; the arm-delay curve is nearly flat —
> 55.91% even armed 8 bars late); (b) refuted (ES retraced **62.33%** in the exact 2026-06-24→26
> window). **(c) platform-side leads by elimination** — script/tester/feed, not further separable
> (the script is lost and the feed retired).

**Governance:** per the frozen §3, `WALL-NOT-CONFIRMED` **names, and does not open,** a follow-up.
A real 1M execution design would need its own pre-registration and, on this family's K arithmetic
(bank 2 → `K_eff` 3 → DSR floor 0.98 vs Cap 1.0), very likely the last MNQ Cap seat. **Not opened
here.**

---

## 3. Cascade status after this session

| Layer | US500 (2026-06) | **MNQ / NQ (2026-08)** |
|---|---|---|
| **W** weekly structure | RESOLVED 0.5571 | **RESOLVED** — NQ 0.5880, MNQ 0.5751 (confirmation) |
| **D** SSL bear-FVG | RESOLVED 0.795 | **RESOLVED** — NQ 0.8630 (confirmation); MNQ AMBIGUOUS-HOLD |
| **D** pools (both sides) | FALSIFIED | **FALSIFIED** — far below base on both instruments |
| **1H** premium/discount | FALSIFIED (single regime, n_eff 151/92) | **FALSIFIED** (multi-regime, n_eff 1852/1199) |
| **1M** execution | INSUFFICIENT-N (0/247 fills, 2-day window) | fill wall **NOT CONFIRMED** (59.06%, n=128,089) — but see §2.2 |

**Net, unchanged from the original campaign: no layer licenses a deployable edge.** The two
structural components are now confirmed on independent instruments; the gate layer between them is
falsified with 12× the power; and the execution layer's blocker has been re-characterized rather
than removed — it is no longer "price does not retrace," but it is not yet "the strategy fills."

---

## 4. Reproduce

```bash
python lab/analysis/_inbox/ict_mnq_2026-08/run_1h_layer.py  <mnq_1h.parquet>
python lab/analysis/_inbox/ict_mnq_2026-08/run_1m_probe.py  <mnq_1m.parquet>
git diff HEAD -- lab/archive/ict_cascade_2026-06-18/   # must be EMPTY
```

Data (gitignored, regenerable at $0.00):

```bash
python lab/databento_fetch/db_fetch.py pull --symbols MNQ.v.0 --stype continuous \
  --schema ohlcv-1h --start 2019-05-06 --end 2026-08-03 --phase oos --max-cost 1.00 --out mnq_1h.parquet
python lab/databento_fetch/db_fetch.py pull --symbols MNQ.v.0 --stype continuous \
  --schema ohlcv-1m --start 2019-05-06 --end 2026-08-03 --phase oos --max-cost 1.00 --out mnq_1m.parquet
```
