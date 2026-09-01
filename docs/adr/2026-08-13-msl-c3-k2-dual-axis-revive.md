# ADR 2026-08-13 — MSL-C3 M2K dual-axis Stage-1 revive (`K_intrinsic=2`)

**Status:** `Accepted` — operator election 2026-08-13
**Decision date:** 2026-08-13
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** light
**Authors:** Joshua (election: fresh Stage-1 licensing `K_intrinsic=2`, both stories as scored axes) + Cursor (recorder)
**Related:** [C3 OPERATOR-KILL](../briefs/closures/MSL-C3-closure-operator-kill.md) · [`STAGE1_K2`](../../lab/archive/msl_c3_m2k_2026-08/STAGE1_K2.md) · [STAGE0](../../lab/archive/msl_c3_m2k_2026-08/STAGE0.md) · [K-bank ADR](2026-08-04-family-k-bank-disclosure-not-gate.md) · [second slate](../briefs/2026-08-13-msl-second-slate.md) · [program plan](../briefs/2026-08-12-msl-program-plan.md)
**Layer:** MSL card-local Stage-1 election only. **$0 / K spent = 0** (disclosure of intended `K_intrinsic=2` at next G0). No arming, no Pine, no panel pull, no `core/`, no estate-wide gate change.

## Decision

Revive MSL-C3 on M2K under the registry re-proposal bar (fresh Stage-1 + new B4) — not a silent reopen of the unpaid G0 path — licensing `K_intrinsic=2` with both pre-registered stories as scored IS axes: `pdh-pdl-failed-break-reclaim` and `overnight-range-failed-extension-fade`. This revive is the next serialized MSL slot ahead of unpaid S2B (do not take the TV seat for S2B while this card is in flight). DSR explore/survivor floor for this G0 = `floor_at_k(2)` = **0.850**; family bank `K_banked(M2K)=0` does not gate.

## Grounds

Operator 2026-08-13: elect fresh Stage-1 at `K_intrinsic=2` with both stories scored; original C3 Stage-1 PASSed then OPERATOR-KILL solely for B4-decline (no IS edge test); prior ≤1-story license was card-local under-license, not an estate dual-axis ban. Does **not** loosen Cap 1.0, `DSR ≥ 0.95`, `V=1/n`, or the floor ladder — paying `K_intrinsic=2` is the existing escape hatch ([K-bank ADR](2026-08-04-family-k-bank-disclosure-not-gate.md) §5).

## Reads

[C3 STAGE1](../../lab/archive/msl_c3_m2k_2026-08/STAGE1.md) @ HEAD · [C3 closure](../briefs/closures/MSL-C3-closure-operator-kill.md) · [rejected_candidates C3](../rejected_candidates.md) · [C1 MYM FALSIFIED](../briefs/closures/MSL-C1-closure-falsified.md) (adjacency) · [axis_screen `floor_at_k`](../../lab/research_utils/axis_screen.py) → `[0.65, 0.85, 0.98, 1.06]` · [STAGE0](../../lab/archive/msl_c3_m2k_2026-08/STAGE0.md) · [`PREREG_G0`](../../lab/archive/msl_c3_m2k_2026-08/PREREG_G0.md) explore FALSIFIED · [closure](../briefs/closures/MSL-C3-K2-closure-falsified.md) · [SESSIONS](../SESSIONS.md).

## Gate

RESOLVED when Accepted and [`STAGE1_K2.md`](../../lab/analysis/c1/msl_c3_m2k_2026-08/STAGE1_K2.md) records STAGE-1 PASS with both axes licensed. Downstream (not this Gate): B4 → PREREG freeze (paid 2026-08-13); explore GO remains unpaid.

## Boundary

Do **not** freeze G0 without a new B4 citing this ADR + STAGE1_K2; score either story on CONFIRM; treat MYM C1 kill as cleared for M2K; score a third mechanism without further `K_intrinsic` + Stage-1; pull M2K/RTY panels without a fresh W4 dry-run; amend Cap / DSR_MIN / floor ladder / family-bank semantics; or arm / `dry_run=false` / Striker redeploy.
