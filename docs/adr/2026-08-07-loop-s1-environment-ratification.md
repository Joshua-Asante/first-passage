# ADR 2026-08-07 — Loop S1: environment ratification (F2 + F3)

**Status:** `Accepted` — implements [SPEC S1](../spec/2026-08-07-loop-s1-environment-ratification-spec.md); operator direction recorded 2026-08-07 (*"this is going to be our environment, as soon as we solidify a strategy for it"*) + plan-execution GO 2026-08-07
**Decision date:** 2026-08-07
**Authors:** Joshua (direction + plan GO) + Cursor (drafter)
**Supersedes:** `2026-08-04-tradeify-venue-descope-eval-included.md` in part — §7 forks **F2** and **F3** only (rail disposition + successor-venue question). De-scope clauses 1–2 (withdrawn Striker legs; bar on redeploying those two legs) and fork **F1** (§4 reading, 2026-11-08) **stand**.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [SPEC S1](../spec/2026-08-07-loop-s1-environment-ratification-spec.md) · [loop index](../spec/2026-08-07-loop-spec-index.md) · [Q-VENUEGEO-1](../briefs/Q-VENUEGEO-1-f3-successor-venue-geometry-scoping.md) · [MNQDTL-1](../spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md)
**Layer:** environment / rail-disposition only. **$0 / K=0** — authorizes nothing, arms nothing, redeploys no Striker leg, places no trade.

---

## §0 — Rule 0 reads (verified 2026-08-07)

| Source | Anchor | What it pins |
|---|---|---|
| [SPEC S1](../spec/2026-08-07-loop-s1-environment-ratification-spec.md) | `e3272cb` (PR #677) | F2=rail warm/disarmed at incumbent; F3=incumbent eval = environment for **new** strategies; Striker redeploy barred |
| [de-scope ADR §7](2026-08-04-tradeify-venue-descope-eval-included.md) | Accepted 2026-08-04 | F2 / F3 / F1 fork definitions; clauses 1–2 withdrawal of Striker legs |
| [`STATE.md`](../../STATE.md) board rows 0–3 | HEAD at draft | Row 0 RULED 2026-08-05 (venue will not lapse); rows 1/3 named S1 as operator input |
| [Q-VENUEGEO-1](../briefs/Q-VENUEGEO-1-f3-successor-venue-geometry-scoping.md) | OPEN | DP3 bust half measured; EV/$ half owed; evidence for F3 — **unconsumed** by this ruling |
| Platform account liveness | **agent cannot independently verify** | Proceed under board row 0 RULED + S1 FALSIFIED path if account found lapsed/breached |

---

## §1 — Context

The 2026-08-04 de-scope withdrew both Striker legs from Tradeify deployment (eval included) and opened F2 (rail disposition) and F3 (successor venue), both dated 2026-08-08. Closed-loop SPEC S1 commissioned the ruling: keep the rail as the programme environment at the live incumbent `Tradeify_Select_100K` eval for **new** strategies — not a successor migration, and not a Striker redeploy.

Q-VENUEGEO-1 remains valuable evidence (Bulenox/BluSky/MFFU geometry) but is **not consumed** into a migration GO here.

---

## §2 — Decision

**F2 — rail disposition:** Retain the c1 rail **built, warm, and disarmed** (`dry_run=true`), pointed at the incumbent `Tradeify_Select_100K` eval. Account stays registered (dormant-capable). M1 spine retained. No tear-down; no re-point at a successor venue under this ADR.

**F3 — successor venue:** **No successor migration now.** The environment for **new** strategies is the live incumbent eval. Q-VENUEGEO-1 evidence stands recorded and unconsumed (EV/$ half + precision re-run remain available if a future GO reopens migration).

**Unchanged:**
- De-scope clauses 1–2 — both withdrawn Striker legs stay barred from redeploy at this venue.
- Fork F1 (§4 reading of a de-scoped firm) — still due 2026-11-08.
- Attended-only posture, per-armed-session GO, M1 arm-gate, locked `BASE_RISK` / allocation constants.

**Consequence for MNQDTL-1:** the no-successor ruling **forecloses R1** (ORB re-score on an F3 successor-venue basis; its F-A/F-C successor preconditions). **R2** (new construct via Route A/B under EM0–EM5) is the live route. Incumbent-eval scoring of new constructs is in scope; ORB unpark still needs its own GO + survivor-scoring pass.

**Effective:** immediately upon Accept (2026-08-07).
**Spend:** $0 / K=0 / no arming / no agent trade.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Tear down the rail | Discards M1 spine + $208/$700 sunk build; S1 direction keeps it warm for new strategies |
| Migrate to Bulenox/BluSky/MFFU now | Q-VENUEGEO-1 EV/$ half unrun; Bust figures at ceiling indistinguishability; operator chose incumbent environment |
| Redeploy withdrawn Striker legs | Explicitly barred by de-scope clauses 1–2; venue-fit falsifiers stand |
| Leave F2/F3 open past 08-08 | Board owed a ruling; closed-loop programme cannot proceed without an environment |

---

## §4 — Falsifier (revert trigger)

**H:** After Accept, the programme treats the incumbent `Tradeify_Select_100K` eval as the environment for new strategies, the rail stays warm/disarmed there, and no Striker leg is redeployed under cover of this ADR.

**Revert / FALSIFIED (any limb):**
1. Account found **lapsed or breached** → S1 gate FALSIFIED; reroute via Q-VENUEGEO-1 under a fresh GO (DP3 EV/$ + precision re-run still owed).
2. Any Accept-era artifact **redeploys** a withdrawn Striker leg at Tradeify → superseding ADR; redeploy DEAD-listed.
3. Silent redefinition of F3 as “successor chosen” without a new ADR consuming Q-VENUEGEO-1 → supersede.

**Trigger check schedule:** next armed-session GO, or 2026-11-08 programme audit — confirm rail still warm/disarmed at incumbent and Striker bar intact.

---

## §5 — Forbidden moves

- Redeploying either withdrawn Striker leg (de-scope clauses 1–2).
- Arming the rail or setting `dry_run=false` under this ADR.
- Agent-placed trades (board row 0 token-trade path remains operator-only if needed for activity).
- Consuming Q-VENUEGEO-1 into a migration GO without a fresh ADR.
- Editing locked `BASE_RISK` / Pine / lifecycle multipliers.
- Treating this ADR as M1 `RESOLVED` or as B7 Stage-1 discharge.

---

## §6 — Consequences

- STATE board rows **1 (F2)** and **3 (F3)** clear (detail lives here).
- CLAUDE.md posture refreshes: environment = incumbent eval for new strategies; rail warm/disarmed; F2/F3 closed; F1 still open; fills/exits research interest un-suspends when S4 delivers a fill path (not by this ADR alone).
- MNQDTL-1 R1 foreclosed; R2 live.
- Q-VENUEGEO-1 status scoped: evidence recorded, unconsumed.
- Unblocks S2 (signal-host fork), S4 (sensor layer), S5 (promotion lane) per loop index depends.

---

## §7 — Propagation (S7 S1-ADR section)

Discharged in the same commit as Accept — see [alignment manifest](../notes/2026-08-07-posture-a-alignment-manifest.md) §S1-ADR.
