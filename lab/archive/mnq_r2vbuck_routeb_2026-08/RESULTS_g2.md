# Q-R2VBUCK-1 — Stage-G (G2) RESULTS

**Status:** `FALSIFIED` — empty candidate list (G3 → **STOP** for this G0 catalogue).
**Date:** 2026-08-08 · **Cost:** $0.00 (OFCHAN cache reuse; no new pull) · **K:** disclosure only (`K_intrinsic=1` frozen at G0).
**Explore GO:** operator-ratified under MNQDTL **R2** 2026-08-08 (OFCHAN cache reuse; no new pull).
**Parent:** [`PREREG_G0.md`](PREREG_G0.md) · [`Q-R2VBUCK-1`](lab/archive/../../../docs/briefs/Q-R2VBUCK-1-volume-bucket-aggressor-route-b-scoping.md)
**Machine record:** [`RESULTS_g2.json`](RESULTS_g2.json)

---

## Verdict

| Limb | Result |
|---|---|
| VOID-POWER (n ≥ 2,000) | PASS — n_retained = **77,656** |
| VOID-COVERAGE (retained/eligible ≥ 90%) | PASS — **77,656 / 77,656 = 100%** |
| CI excludes 0 | **FAIL** — ρ **−0.005478** · CI95 **[−0.016881, +0.005984]** includes 0 |
| Placebo \|ρ\| > p95 | FAIL — \|ρ\| = 0.005478 < placebo \|·\| p95 **0.007958** |
| Halves agree on sign | disagree (H1 **−0.017417** / H2 **+0.002439**) — not reached as deciding limb |
| \|ρ\| ≥ 0.02 | FAIL (0.005478) |
| **Candidates** | **[]** |

**Disposition:** Route B G2 emits **zero** candidates. Per Avenue A checklist G3: empty list → **STOP** this catalogue. CONFIRM window **untouched** (reserved `2025-09-01→2026-02-06`). Cap seat **not claimed**. FM-5: not an edge claim, not harvest PASS, not deployment.

**Coverage success (disclosure):** volume-bucket sampling cleared the OFCHAN minute-grid pathology (that campaign died at 7.36% coverage). Failure here is **association**, not denseness.

**Economic honesty (PREREG §7, not a promotion gate):** EXPLORATION 60 s mid-return σ(r) ≈ **6.85e−4** (fractional); \|r\| p50/p95 ≈ **3.32e−4 / 1.42e−3**. At a ~22k mid that is roughly **~15 pts** 1σ / **~7–31 pts** for \|r\| p50–p95. Observed \|ρ\| ≈ 0.005 implies a predicted directional move ≪ the **3–9 pt** EM1-relevant band from the K-wall stop band — consistent with CI/placebo failure.

---

## Run facts

- Cell C1: aggressor imbalance inside **B = 2550** volume buckets → 60 s mid return
- Window: EXPLORATION **2026-02-06 → 2026-08-06** (CONFIRM reserved, unread)
- Batch / cache: `GLBX-20260807-EHX5KUSF7K` · 155 day files · **124** sessions scored
- Pre-registered holiday exclusions: 2026-02-16, 04-03, 05-25, 06-19, 07-03
- Seed **20260808** · boot **10,000** · placebo **1,000**
- Harness: `r2vbuck_lib.py` + `run_r2vbuck_g2.py` (13 unit tests green before real quotes)
- Eligible denominator = completed RTH volume-buckets; retained = those with finite A and valid mid at `t` and `t+60s−`

**Re-proposal bar:** new G0 / new mechanism — **not** a retune of B, horizon, or this catalogue (FM-9 / Trap #12).
