# ADR 2026-08-12 — MSL B8: release MYM1!/MNQ1! occupancy for new non-Striker candidates

**Status:** `Accepted` — operator election (Board B8) 2026-08-12
**Decision date:** 2026-08-12
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** light
**Authors:** Joshua (ruling) + Cursor (recorder)
**Related:** [MSL ratification](2026-08-12-msl-sourcing-channel-ratification.md) · [S1](2026-08-07-loop-s1-environment-ratification.md) · [de-scope](2026-08-04-tradeify-venue-descope-eval-included.md) · [MSL-C1 slate](../briefs/2026-08-12-msl-first-slate.md) · `ops/instruments/{MYM,MNQ,MES,M2K,MCL}.md`
**Layer:** instrument-occupancy posture only. **$0 / K=0.** No arming, no Pine, no `core/`, no `LEG_MAP` code edit.

## Decision

Release **`MYM1!` and `MNQ1!` symbol/cap occupancy** for **new non-Striker** MSL and Tradeify-shaped research and G0 (including MSL-C1). Withdrawn Striker legs no longer reserve headroom in ledger posture. Occupancy is a **ledger/doctrine** fact — `LEG_MAP` code may remain as historical map and is **not** silently deleted by this record.

## Grounds

S1 already closed de-scope **F2** as keep-warm/disarmed at the incumbent ([S1](2026-08-07-loop-s1-environment-ratification.md)); that ruling stands. The 2026-08-04 MYM disposition still said any candidate reasoning from a freed `MYM1!` needed F2 ruled — MSL Board B8 is that **narrow occupancy** ruling, not a re-litigation of rail keep-warm / tear-down / re-point.

## Reads

`ops/instruments/MYM.md` @ `e20e240` (2026-08-04 occupancy bar) · [S1](2026-08-07-loop-s1-environment-ratification.md) §2 F2 · [de-scope](2026-08-04-tradeify-venue-descope-eval-included.md) clauses 1–2 · [MSL plan](../briefs/2026-08-12-msl-program-plan.md) B8 · MES/M2K/MCL `venue_note` “retained-not-released” lines.

## Gate

RESOLVED when this ADR is Accepted and MYM/MNQ ledgers carry a dated disposition pointing here; MSL-C1 door-check may answer occupancy by citing this ADR.

## Boundary

Do **not** read this as authorizing Striker-leg redeploy (de-scope clauses 1–2 stand). Do not arm the rail or set `dry_run=false`. Do not delete or rewrite `LEG_MAP` under cover of this record. Do not treat S1 F2 keep-warm as reopened.
