# Q-FILLTAX-1 / SPEC S3 — Phase-0 / V2 parity limb note

**Status:** `CODE_LANDED` scaffold 2026-08-07 — **no family TV-anchor run yet;
no parity numbers claimed.**
**Date:** 2026-08-07
**Brief:** [`Q-FILLTAX-1`](../../../../docs/briefs/Q-FILLTAX-1-fill-realism-and-parity-scoping.md)
**Spec:** [`SPEC S3`](../../../../docs/spec/2026-08-07-loop-s3-arbiter-two-tier-spec.md)
**Bands:** [`PREREG.md`](PREREG.md) (`FROZEN-PRE-RUN`)
**Cost:** $0 · K=0 · nothing armed

---

## Phase-0 / V2 sequencing under S1

- **V2 (parity automation) executes now at $0** under the S1-ratified incumbent
  environment (`Tradeify_Select_100K` eval for **new** strategies —
  [`S1 ADR`](../../../../docs/adr/2026-08-07-loop-s1-environment-ratification.md)).
  This directory is the Gen-2 harness scaffold: bands frozen before any run,
  synthetic unit tests only.
- **V1 (fill-realism tax) disposition follows S1** — measurement geometry, when
  sequenced, is **Tradeify** (incumbent env), not a successor-venue freeze.
  V1 still does not run in this scaffold; no Databento pull; no fabricated tax.
- **Gate RESOLVED** (S3) still requires the first family manual TV anchor
  (operator). Scaffold ADMIT/FAIL on synthetics is not family authority.

## What is not in this RESULTS

- No engine↔TV ρ, net, or PF figures for any live family.
- No mutation-battery outcome (Q-FILLTAX-1 Phase 1 still owed).
- No deployment-truth fill capture (M1 not `RESOLVED`; rail stays disarmed).

## Harness

| Artifact | Role |
|---|---|
| [`parity_gate.py`](parity_gate.py) | ADMIT/FAIL vs FROZEN-PRE-RUN bands |
| [`test_parity_gate.py`](test_parity_gate.py) | Synthetic pass/fail fixtures |
| [`README.md`](README.md) | How to run + deployment-truth path (read-only) |
