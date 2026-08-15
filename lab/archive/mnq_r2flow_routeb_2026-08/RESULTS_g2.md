# Q-R2FLOW-1 — Stage-G (G2) RESULTS

**Status:** `FALSIFIED` — empty candidate list (G3 → **STOP** for this G0 catalogue).
**Date:** 2026-08-08 · **Cost:** $0.00 (OFCHAN cache reuse; no new pull) · **K:** disclosure only (`K_intrinsic=1` frozen at G0).
**Explore GO:** operator-ratified under MNQDTL **R2** 2026-08-08 (OFCHAN cache reuse; no new pull).
**Parent:** [`PREREG_G0.md`](PREREG_G0.md) · [`Q-R2FLOW-1`](lab/archive/../../../docs/briefs/Q-R2FLOW-1-signed-minute-flow-route-b-scoping.md)
**Machine record:** [`RESULTS_g2.json`](RESULTS_g2.json)

---

## Verdict

| Limb | Result |
|---|---|
| VOID-POWER (n ≥ 2,000) | PASS — n_retained = **48,360** |
| VOID-COVERAGE (retained/eligible ≥ 90%) | PASS — **48,360 / 48,360 = 100%** |
| CI excludes 0 | **FAIL** — ρ **−0.000701** · CI95 **[−0.014612, +0.013510]** includes 0 |
| Placebo \|ρ\| > p95 | skipped (PREREG CI precedence — CI already fails) |
| Halves agree on sign | disagree (H1 **−0.020313** / H2 **+0.014732**) — not reached as deciding limb |
| \|ρ\| ≥ 0.02 | FAIL (0.000701) |
| **Candidates** | **[]** |

**Disposition:** Route B G2 emits **zero** candidates. Per brief §6 / Avenue A: empty list → **STOP** this catalogue. CONFIRM window **untouched** (reserved `2025-09-01→2026-02-06`). Cap seat **not claimed**. FM-5: not an edge claim, not harvest PASS, not deployment.

**Read:** denseness cleared (full RTH clock-minute coverage); association null under frozen limbs — distinct from OFCHAN VOID-COVERAGE, R2VBUCK ratio null, and AGRUN magnitude AMBIGUOUS-HOLD.

**Economic honesty (PREREG §7, not a promotion gate):** EXPLORATION σ(r) ≈ **5.29e−4**; \|A\| p05/p50/p95 = **20 / 264 / 1259** (contracts); see `RESULTS_g2.json` `census`. Observed \|ρ\| ≈ 0.0007 implies predicted directional move far under the EM1-relevant band — consistent with CI failure.

---

## Run facts

- Cell C1: clock-minute net signed aggressor size → 60 s mid return from `t_end`
- Window: EXPLORATION **2026-02-06 → 2026-08-06** (CONFIRM reserved, unread)
- Batch / cache: `GLBX-20260807-EHX5KUSF7K` · 155 day files · **124** sessions scored
- Pre-registered holiday exclusions: 2026-02-16, 04-03, 05-25, 06-19, 07-03
- Seed **20260808** · boot **10,000** (suff-stats equiv) · placebo skipped (CI precedence)
- Day scan: `ProcessPoolExecutor` parallel · harness `flow_lib.py` + `run_flow_g2.py` (14 unit tests green before real quotes)
- Eligible = completed RTH minutes with ≥1 B/A print; retained = those with valid mid at `t_end` and `t_end+60s−`

**Re-proposal bar:** new G0 / new mechanism — **not** a retune of grid, horizon, or this catalogue (FM-9).
