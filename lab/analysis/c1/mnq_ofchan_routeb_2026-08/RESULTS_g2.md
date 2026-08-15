# Q-OFCHAN-1 — Stage-G (G2) RESULTS

**Status:** `VOID-COVERAGE` — empty candidate list (G3 → STOP for this G0 catalogue).
**Date:** 2026-08-07 · **Cost:** $0.00 (cache reuse; no pull) · **K:** disclosure only (`K_intrinsic=1` already frozen).
**Parent:** [`PREREG_G0.md`](PREREG_G0.md) · [`Q-OFCHAN-1`](../../../../docs/briefs/Q-OFCHAN-1-orderflow-channel-route-b-scoping.md)
**Machine record:** [`RESULTS_g2.json`](RESULTS_g2.json)

---

## Verdict

| Limb | Result |
|---|---|
| VOID-POWER (n ≥ 2,000) | PASS — n_retained = **3,558** |
| VOID-COVERAGE (retained/eligible ≥ 90%) | **FIRE** — **3,558 / 48,360 = 7.36%** |
| CI excludes 0 | not scored (coverage precedes) — observed CI95 **[−0.048, +0.024]** includes 0 |
| Placebo \|ρ\| > p95 | not scored — \|ρ\| = 0.012 < placebo p95 0.029 |
| Halves agree on sign | disagree (H1 −0.033 / H2 +0.011) |
| \|ρ\| ≥ 0.02 | FAIL (0.012) |
| **Candidates** | **[]** |

**Disposition:** Route B G2 emits **zero** candidates. Per Avenue A checklist G3: empty list → **STOP** this catalogue. CONFIRM untouched. Cap seat not claimed. FM-5: this is not an edge claim and not a harvest PASS.

**Likely driver of coverage failure (disclosure, not a retune):** the frozen flicker filter requires ≥5 same-sign TBBO updates in the trailing 1 s at each RTH clock minute. The EXPLORATION batch’s day files are trade-tagged TBBO (`action=T`); quiet minutes rarely clear that density, so most grid minutes drop before ρ is computed. Reopening needs a **new G0** (new catalogue / filter definition), not a post-hoc edit of this freeze (FM-9 / Trap #12).

---

## Run facts

- Window: EXPLORATION **2026-02-06 → 2026-08-06** (CONFIRM reserved, unread)
- Batch: `GLBX-20260807-EHX5KUSF7K` · 155 day files · 124 sessions scored
- Pre-registered holiday exclusions: 2026-02-16, 04-03, 05-25, 06-19, 07-03
- Seed **20260806** · boot **10,000** · placebo **1,000**
- Harness: `ofchan_lib.py` + `run_ofchan_g2.py` (unit tests green before real quotes)
