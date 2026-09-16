# Cursor-fleet worker capability — SUBTRACT

**Class:** (a) active campaign · **Standing:** SUBTRACT — terminal, with re-entry armor.
**Ratified:** 2026-09-15 (operator, in-session: "execute my decisions"), superseding the
2026-08-09 `KEEP` (GSUB-1 Phase 3).

**Grounds.** This pursuit's aim was "offload spec-freezable implementation packets **to Cursor
workers**." The operator retired Cursor as a worker surface on 2026-09-15, having already removed
it from recurring spend on 2026-09-10 ([`d16`](d16-cursor-subscription.md), `SUBTRACT`) and ruled
it "not a lane" for Track B on 2026-09-11 (D-B6). The *capability* — fan out frozen packets to
parallel workers — is not dead and is **not** subtracted here; what is subtracted is this
pursuit's binding of that capability to Cursor, together with its `Survive bound`, which was the
Cursor subscription that no longer exists. A pursuit cannot be measured against a bound that has
been removed.

**Why SUBTRACT and not MERGE.** MERGE requires a named target pursuit to own the residuals. None
exists, and creating one is outside an agent's authority under the GRAND §2.4 domain guard. If
the operator later wants a successor worker-capability pursuit, that is a fresh OPEN and the
residual table below transfers unchanged.

**Re-entry armor (GRAND §2.3).** SUBTRACT is terminal. Re-opening requires **out-of-frame
evidence plus an attached falsifier**, recorded through a governance channel (ADR or equivalent):
specifically, evidence that parallel-worker dispatch is throughput-limiting on a surviving
surface, plus a falsifier stating what result would end the retry. The removal of a vendor
subscription is not, by itself, out-of-frame evidence for re-opening.

## Residual disposition (GRAND §2.3)

Every residual function enumerated and assigned an owner, or it subtracts with the pursuit.

| # | Residual function | Disposition and owner |
|---|---|---|
| R1 | The `cursor-fleet` skill's orchestration loop — disjoint file footprints, umbrella brief + packet appendices, claim manifest, dispatch-moment Phase-0 re-check, four-state return taxonomy, integration discipline | **Re-homed; carrier deleted.** The skill was deleted 2026-09-15 at operator instruction. The load-bearing rules are restated surface-agnostically in [`2026-07-14-cc-cursor-surface-allocation.md`](../adr/2026-07-14-cc-cursor-surface-allocation.md) §Decision ("Orchestrating more than one worker at a time") and its §8 table. Body retrievable at blob `56f728a47d39c9a3eb172858df85f7f6ed679775`; see [`TOMBSTONES.md`](../adr/TOMBSTONES.md#2026-09-15-cursor-agent-retirement). |
| R2 | The per-packet local-only dispatch gate ("Test 0 per packet") | **Retained.** Canonical owner is and always was [`task-routing`](../../.claude/skills/task-routing/SKILL.md); the fleet skill only restated it. |
| R3 | The single-writer rule for `docs/SESSIONS.md`, `STATE.md`, campaign-state and board files | **Retained.** Restated in the ADR's §Decision; cited live by the [Track B campaign state](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md) §Role and by the [MSL program plan](../briefs/programs/2026-08-12-msl-program-plan.md), both repointed at the ADR. |
| R4 | The dated friction ledger (week of 2026-07-18→24 failures that motivated each rule) | **Retained as evidence, not as a live rule.** The incidents remain in `docs/SESSIONS.md`, the programme audits, and the archived umbrella briefs indexed in `lab/ARCHIVED.json`. Deleting the skill did not delete the evidence. |
| R5 | The measure — "packet claim-manifest completion rate; defect rate on dispatched packets" | **Retired with the pursuit.** It was defined against the surface-allocation ADR's falsifier, whose two limbs are retained *at the ADR* (§4, restated surface-agnostically with their revert actions and check schedule). No separate pursuit-level measurement survives. |
| R6 | Three frozen packets "pending dispatch" (2026-08-09: dense-1m entry lane, instrument lane, W1 re-run) | **Subtracts with the pursuit — the §2.3 default, applied after checking.** No surviving carrier was found: no brief file under `docs/briefs/handoffs/`, no `STATE.md` queue row, no live citation anywhere in the tree (searched 2026-09-15). The [2026-08-31 pursuits audit](../notes/audits/2026-08-31-pursuits-personas-reversed-evidence-audit.md) had already found this pursuit's status overstated one lane's outcome. §2.3 is explicit that a residual without an assigned owner subtracts with its pursuit, so that is what happens here rather than leaving three unowned obligations standing. **Re-opening any of the three is a fresh packet on a surviving worker lane under the ADR's routing test — not a revival of these**, and it inherits the re-entry armor above. |

## What this record does not do

It does not touch [`d16`](d16-cursor-subscription.md) (already `SUBTRACT`), does not create a
successor pursuit, and does not settle the [subscription ledger](SUBSCRIPTION_LEDGER.md)'s
outstanding Cursor figures — cancellation date and final charges remain **not supplied**, which is
an operator reconfirmation, not an agent edit.

## Historical disposition — superseded 2026-09-15

**Class:** (a) active campaign · **Standing:** KEEP
**Aim served:** A2/A4 — offload spec-freezable implementation packets to Cursor workers, CC stays orchestrator
**Measure:** packet claim-manifest completion rate; defect rate on dispatched packets (per the surface-allocation ADR)
**Survive bound:** Cursor subscription cost (see d16 — same underlying subscription, tracked once there)
**Review date:** per-packet, no fixed date
**Ratified:** 2026-08-09 (GSUB-1 Phase 3)

**Owner artifacts:** `cursor-fleet` skill · three frozen packets pending dispatch (2026-08-09: dense-1m entry lane, instrument lane, W1 re-run)

**Source:** [`GSUB-1 inventory`](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/docs/briefs/programs/GSUB-1-inventory-and-dispositions.md) row a6
