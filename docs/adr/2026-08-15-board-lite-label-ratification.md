# ADR 2026-08-15 — Ratify "Board-lite" as shorthand for two existing MSL bars (no new rule)

**Status:** `Accepted` — ratified by operator (JA) 2026-08-15, in-session instruction
**Decision date:** 2026-08-15
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** light
**Layer:** governance convention. **$0 / K=0.**

## Decision

"Board-lite" is ratified as standing shorthand for exactly two already-ratified MSL rules: **(a)** no index-futures continuation entry, and **(b)** no third MR-at-level rr≈1 card. It creates no new bar, changes no scope, and revives nothing — this closes a documentation gap (an unratified label), not a substantive question.

## Grounds

The [2026-08-15 wall-scope audit](../notes/audits/programme-audit/2026-08-15-msl-wall-scope-audit.md) §3 found the label first used in `N-2026-08-14-msl-who-track.md`, which cites it as though pre-existing doctrine while no ADR, closure, or `BINDING BAR` registry entry names it anywhere in the corpus. The two rules it bundles are each independently, soundly grounded — (a) traces to [MSL-S2B's ratified Stage-1 FAIL](../briefs/closures/MSL-S2B-closure-stage1-fail-route.md) (resting on the machine-wired `index-intraday-ohlcv-directional-timing-2026-07-21` bar); (b) traces to [C1](../briefs/closures/MSL-C1-closure-falsified.md)/[C2](../briefs/closures/MSL-C2-closure-falsified.md)/[C3](../briefs/closures/MSL-C3-closure-operator-kill.md)'s own prior dispositions. Retiring the label (rewriting every citation across closed, dated notices) would violate forward-only discipline for no benefit; papering it here is the cheaper, correct fix.

## Reads

`N-2026-08-14-msl-who-track.md` @ `56be680b` (label's first use, :67,84,170,225) · `N-2026-08-14-msl-slate-3-constraints.md` @ `c4dc069d` (label's origin commit — same two rules stated unlabeled) · [2026-08-15 wall-scope audit](../notes/audits/programme-audit/2026-08-15-msl-wall-scope-audit.md) §3 wall #14.

## Gate

RESOLVED — this record is the label's paper trail. Future citations of "Board-lite" may point here.

## Boundary

Do not use this ADR to add a third rule under the "Board-lite" name without a fresh decision record — it ratifies exactly the two rules named above, nothing broader.
