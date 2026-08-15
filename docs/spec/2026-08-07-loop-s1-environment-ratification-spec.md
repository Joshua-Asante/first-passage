# SPEC S1: environment ratification (F2 + F3)

Status: RESOLVED · 2026-08-07 · ADR Accepted [`2026-08-07-loop-s1-environment-ratification.md`](../adr/2026-08-07-loop-s1-environment-ratification.md) · authorizes nothing ($0 · K=0) · depends: —
Objective: Rule forks F2/F3 (due 2026-08-08) by ADR: the environment is the live incumbent
`Tradeify_Select_100K` eval for **new** strategies, and the rail stays built + disarmed,
pointed at it (operator direction, this conversation: *"this is going to be our
environment, as soon as we solidify a strategy for it"*).

Steps:
1. Verify at the platform: account live, activity week covered (board row 0 ruled
   2026-08-05 — act-by was Fri 2026-08-07).
2. Author the ADR: F2 = retain rail warm/disarmed at the incumbent venue; F3 = incumbent
   eval, no successor migration now (Q-VENUEGEO-1 Bulenox/BluSky/MFFU evidence stands
   recorded, unconsumed); scope excludes the two withdrawn Striker legs (de-scope ADR
   clauses 1–2 unchanged).
3. Propagate one posture line each to `CLAUDE.md` + `STATE.md`; clear board rows 1/3;
   record the consequence for `MNQDTL-1`: the no-successor ruling **forecloses** its R1
   route (successor-venue precondition, its F-A/F-C), leaving R2 the live route.

Gate: RESOLVED if ADR Accepted and board rows 1/3 cleared; FALSIFIED if the account is
found lapsed/breached — reroute via Q-VENUEGEO-1 (DP3 EV/$ half + precision re-run still
owed; no survivor is settled) under a fresh GO.
Boundary: no Striker-leg redeploy · no arming · `dry_run` stays `true` · no agent places
any trade.
Reads (at HEAD `a6a5fe6` 2026-08-07): `STATE.md` board rows 0–3 ·
[de-scope ADR §7](../adr/2026-08-04-tradeify-venue-descope-eval-included.md) ·
[Q-VENUEGEO-1](../briefs/Q-VENUEGEO-1-f3-successor-venue-geometry-scoping.md)
Owner: forks F2/F3 (de-scope ADR §7).
