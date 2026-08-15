# Q-R2AGRUN-1 — Stage-G (G2) RESULTS

**Status:** `AMBIGUOUS-HOLD` — empty candidate list (magnitude floor; G3 → **ITERATE**, not promote).
**Date:** 2026-08-08 · **Cost:** $0.00 (OFCHAN cache reuse; no new pull) · **K:** disclosure only (`K_intrinsic=1` frozen at G0).
**Explore GO:** operator-ratified under MNQDTL **R2** 2026-08-08 (OFCHAN cache reuse; no new pull).
**Parent:** [`PREREG_G0.md`](PREREG_G0.md) · [`Q-R2AGRUN-1`](../../../../docs/briefs/Q-R2AGRUN-1-aggressor-run-length-route-b-scoping.md)
**Machine record:** [`RESULTS_g2.json`](RESULTS_g2.json)

---

## Verdict

| Limb | Result |
|---|---|
| VOID-POWER (n ≥ 2,000) | PASS — n_retained = **22,304,297** |
| VOID-COVERAGE (retained/eligible ≥ 90%) | PASS — **22,304,297 / 22,304,297 = 100%** |
| CI excludes 0 | PASS — ρ **−0.001306** · CI95 **[−0.002589, −0.000020]** |
| Placebo \|ρ\| > p95 | PASS — \|ρ\| = 0.001306 > placebo \|·\| p95 **0.000398** |
| Halves agree on sign | PASS — H1 **−0.002842** / H2 **−0.000351** (both negative) |
| \|ρ\| ≥ 0.02 | **FAIL** — 0.001306 < 0.02 |
| **Candidates** | **[]** |

**Disposition:** Route B G2 emits **zero** candidates. Per brief §6 / Avenue A: **AMBIGUOUS-HOLD → ITERATE** (dated packet; do **not** score CONFIRM until resolved). Not a post-hoc floor retune. CONFIRM window **untouched** (reserved `2025-09-01→2026-02-06`). Cap seat **not claimed**. FM-5: not an edge claim, not harvest PASS, not deployment.

**Read:** association is *detectable* at n≈22M (CI + placebo) but **below** the pre-registered interpretable magnitude floor — non-promotable under this G0.

**Economic honesty (PREREG §7, not a promotion gate):** EXPLORATION census \|A\| p05/p50/p95 = **2 / 3 / 9** (trade-count); see `RESULTS_g2.json` `census` for r moments. Observed \|ρ\| ≪ 0.02 is consistent with a predicted directional move far under the EM1-relevant band.

---

## Run facts

- Cell C1: signed aggressor-run trade-count (`N_min=2`) → 60 s mid return
- Window: EXPLORATION **2026-02-06 → 2026-08-06** (CONFIRM reserved, unread)
- Batch / cache: `GLBX-20260807-EHX5KUSF7K` · 155 day files · **124** sessions scored
- Pre-registered holiday exclusions: 2026-02-16, 04-03, 05-25, 06-19, 07-03
- Seed **20260808** · boot **10,000** (suff-stats equiv) · placebo **1,000** (`SeedSequence.spawn` + 6 threads)
- Day scan: `ProcessPoolExecutor` parallel · harness `agrun_lib.py` + `run_agrun_g2.py` (16 unit tests green before real quotes)
- Eligible = completed RTH runs with `n_trades ≥ 2`; retained = those with valid mid at `t` and `t+60s−`
