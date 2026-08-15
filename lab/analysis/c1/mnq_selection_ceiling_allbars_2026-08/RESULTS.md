# Q-MNQSEL-2 Phase 0 — RESULTS: dense RTH 1m selection ceiling

**Status:** `RESOLVED` (C4) — oracle top-1/day S3 clears EM1 0.40 on **both** arms while
all-take stays below 0.40. Disposition **ITERATE** → construct packet licensed (separate Q);
this file alone admits no candidate.
**Date:** 2026-08-08
**Pre-registration:** [`PREREG.md`](PREREG.md) — frozen before path PnL (cheap falsifier only).
**Cost:** **$0.00** (`ohlcv-1m_continuous_b1fa4ae6b7ba9af2.dbn` → `_mnq_1m.parquet`) · **K=0** ·
**no manifest** · **Cap untouched**.
**Runner:** [`run_selection_allbars.py`](run_selection_allbars.py) · **7 unit tests** green before
real-bar gate run.
**Raw:** [`RESULTS.json`](RESULTS.json)

---

## 1. Gate verdict — `RESOLVED` (C4)

| Arm | S1 all-take | S2 random-1/day | **S3 oracle top-1/day** | S5 median hits | S6 ≥1 hit |
|---|---:|---:|---:|---:|---:|
| **long** | −0.1590 | −0.1217 | **+0.8584** | 187.0 | 99.9% |
| **short** | −0.1748 | −0.1494 | **+0.8566** | 188.0 | 99.6% |

**Gate (frozen):** S3 ≥ 0.40 on ≥1 arm **and** S1 &lt; 0.40 → `RESOLVED`.  
**Observed:** both arms clear C4. n_sessions = **1,668** ≥ 250. Median clocks/session = **390.0**.

---

## 2. Reading (and what it does not mean)

1. **All-take is dead** on dense 1m opens at G=10 (~−0.16R). Selection is load-bearing.
2. **Oracle top-1 sits near the clean-target ceiling** (0.859 = (10−1.41)/10). With ~390
   clocks/day and S6 ≈ 100%, almost every session has a clean 1R hit — so S3 ≈ 0.858 is the
   expected upper bound under 1R geometry, not evidence of a free edge.
3. **Contrast to MNQSEL-1:** restart clocks at s=40 / G=17.41 failed with S3 ≈ 0.3998 (knife-edge
   under EM1). Dense 1m opens at G=10 **pass** the frozen ceiling — selection headroom exists
   *in this universe*.
4. **Licenses:** construct design on dense 1m opens (named stop G=10 preferred) under a separate
   Q / GO. **Does not license:** a selector, Route B catalogue, Cap claim, ORB unpark, or deploy.

---

## 3. Diagnostics (not gate limbs)

| G | S3 long | S3 short | Informational verdict |
|---|---:|---:|---|
| 5 | +0.7180 | +0.7180 | RESOLVED-shaped |
| 20 | +0.9249 | +0.9197 | RESOLVED-shaped |

Do **not** retune the gate to G=5/20 after seeing these (PREREG §5).

---

## 4. Disposition

**Verdict used:** `RESOLVED` (C4)  
**Next:** **ITERATE** — author EM construct packet (`Q-MNQDTL-CON-1`) unpaid until operator GO.  
**Board write:** STATE / SESSIONS / INDEX / CATALOG / MNQ session log.

---

## 5. Reproduce

```bash
python -m pytest lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/test_run_selection_allbars.py -q
# Rebuild parquet from local DBN (MNQ.v.0 ohlcv-1m), then:
python lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/run_selection_allbars.py <mnq_1m.parquet>
```

Expect: GATE VERDICT `RESOLVED`; S3 long ≈ 0.8584 / short ≈ 0.8566; S1 both negative.
