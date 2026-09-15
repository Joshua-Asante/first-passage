# Cursor-fleet worker capability — KEEP (SUBTRACT **proposed**, operator-gated)

> ⚠ **PROPOSED SUBTRACT 2026-09-15 — not executed.** Standing remains **KEEP** until the
> operator rules. Pursuit dispositions are operator-gated under the
> [GRAND tier](../adr/2026-08-09-grand-tier-quintessentials-binding.md) §2.3; an agent may
> propose, never execute. The proposal and its residual assignments are below; the ratified
> record above the fold is unchanged.

**Class:** (a) active campaign · **Standing:** KEEP
**Aim served:** A2/A4 — offload spec-freezable implementation packets to Cursor workers, CC stays orchestrator
**Measure:** packet claim-manifest completion rate; defect rate on dispatched packets (per the surface-allocation ADR)
**Survive bound:** Cursor subscription cost (see d16 — same underlying subscription, tracked once there)
**Review date:** per-packet, no fixed date
**Ratified:** 2026-08-09 (GSUB-1 Phase 3)

**Owner artifacts:** the `cursor-fleet` skill (deleted 2026-09-15 — see residual R1) · three frozen packets pending dispatch (2026-08-09: dense-1m entry lane, instrument lane, W1 re-run)

**Source:** [`GSUB-1 inventory`](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/docs/briefs/programs/GSUB-1-inventory-and-dispositions.md) row a6

---

## Proposed disposition (2026-09-15) — SUBTRACT

**Grounds.** This pursuit's aim is "offload spec-freezable implementation packets **to Cursor
workers**." The operator retired Cursor as a worker surface on 2026-09-15 ("cursor is being
retired altogether… it will be just claude and codex"), having already removed it from
recurring spend on 2026-09-10 ([`d16`](d16-cursor-subscription.md), `SUBTRACT`) and ruled it
"not a lane" for Track B on 2026-09-11 (D-B6). The *capability* — fan out frozen packets to
parallel workers — is not dead and is not being subtracted; what is dead is **this pursuit's
binding of that capability to Cursor**, along with its `Survive bound`, which was the Cursor
subscription that no longer exists. A pursuit whose survive bound has been removed cannot be
measured against it.

**Why SUBTRACT rather than MERGE into a Codex-worker pursuit.** MERGE would require a named
target that owns the residuals. No such pursuit exists today, and inventing one here would be
an agent creating a pursuit — outside the GRAND §2.4 domain guard. If the operator prefers a
successor pursuit, that is a MERGE ruling they make, and the residual table below transfers
unchanged.

**Re-entry armor (GRAND §2.3).** SUBTRACT is terminal. Re-opening requires **out-of-frame
evidence plus an attached falsifier**, recorded through a governance channel (ADR or
equivalent). Specifically: evidence that parallel-worker dispatch is throughput-limiting on a
surviving surface, plus a falsifier stating what result would end the retry. The removal of a
vendor subscription is not, by itself, out-of-frame evidence for re-opening.

**Residuals (GRAND §2.3: enumerate every residual function and assign an owner, or it
subtracts with the pursuit).**

| # | Residual function | Disposition and owner |
|---|---|---|
| R1 | The `cursor-fleet` skill's orchestration loop — disjoint file footprints, umbrella brief + packet appendices, claim manifest, dispatch-moment Phase-0 re-check, four-state return taxonomy, integration discipline | **Re-homed, carrier deleted.** The skill was deleted 2026-09-15 at operator instruction. The load-bearing rules are restated surface-agnostically in [`2026-07-14-cc-cursor-surface-allocation.md`](../adr/2026-07-14-cc-cursor-surface-allocation.md) §Decision ("Orchestrating more than one worker at a time") and its §8 table. Body retrievable at blob `56f728a47d39c9a3eb172858df85f7f6ed679775`; see [`TOMBSTONES.md`](../adr/TOMBSTONES.md#2026-09-15-cursor-agent-retirement). |
| R2 | The per-packet local-only dispatch gate ("Test 0 per packet") | **Retained.** Canonical owner is and always was [`task-routing`](../../.claude/skills/task-routing/SKILL.md); the fleet skill only restated it. |
| R3 | The single-writer rule for `docs/SESSIONS.md`, `STATE.md`, campaign-state and board files | **Retained.** Restated in the ADR's §Decision; cited live by the [Track B campaign state](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md) §Role, which now points at the ADR. |
| R4 | The dated friction ledger (week of 2026-07-18→24 failures that motivated each rule) | **Retained as evidence, not as a live rule.** The incidents remain in `docs/SESSIONS.md`, the programme audits, and the archived umbrella briefs indexed in `lab/ARCHIVED.json`. Deleting the skill does not delete the evidence. |
| R5 | The measure — "packet claim-manifest completion rate; defect rate on dispatched packets" | **Retired with the pursuit.** It was defined per the surface-allocation ADR's falsifier, whose limb 1 is retained at the ADR and re-scoped to worker PRs on the surviving surfaces. No separate pursuit-level measurement survives. |
| R6 | Three frozen packets "pending dispatch" (2026-08-09: dense-1m entry lane, instrument lane, W1 re-run) | **UNRESOLVED — operator input needed.** Their current state was not verified by this task, and the [2026-08-31 pursuits audit](../notes/audits/2026-08-31-pursuits-personas-reversed-evidence-audit.md) already found this pursuit's status overstated one lane's outcome. They are not dispatched by the retirement either way. The operator should rule: re-target to Codex, close, or leave parked. **A SUBTRACT ruling should not be read as closing them.** |

**What this proposal does NOT do.** It does not close R6's packets, does not create a successor
pursuit, does not touch [`d16`](d16-cursor-subscription.md) (already `SUBTRACT`), and does not
edit the [subscription ledger](SUBSCRIPTION_LEDGER.md) — whose Cursor row still records a
cancellation date and final charges as *not supplied*, an operator reconfirmation rather than
an agent edit.
