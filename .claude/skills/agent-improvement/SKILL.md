---
name: agent-improvement
description: Use during authorized work when a concrete plan flaw, preventable mistake, recurring failure, or evidenced inefficiency offers a bounded improvement. Enables in-scope action and reusable learning; does not authorize policy changes or unrelated optimization.
---

# Agent improvement

Make the current work better and retain useful evidence for the next task. Apply
this at ordinary planning, correction and completion moments when a concrete
opportunity appears. Do not create a separate reflection task when none appears.
Authority and recurrence rules live in [AGENTS.md](../../../AGENTS.md#continuous-improvement).

## Establish the opportunity

Name the source-supported mechanism and expected benefit: given this input or
sequence, this step causes an error, rework or unnecessary cost. A proactive finding
can be demonstrated from a plan's producer/consumer sequence before a failure occurs.
Read the affected source and task contract; confidence alone is not evidence.

Search the affected paths and mechanism in existing tests, hooks, skills and owning
plans/records. Search lessons/history when reuse is plausible; use the
[retrieval guidance](../../../docs/ltm/README.md) for cold or removed records.
Do not turn every opportunity into a repository-wide search. Read any relevant
prior improvement entry and its later outcomes before reusing its recommendation.

For an observed defect use [root-cause-first](../root-cause-first/SKILL.md), which
owns diagnosis and regression evidence. For external or frozen handoffs use
[handoff-verify](../handoff-verify/SKILL.md); a contradiction returns to the
coordinator rather than being silently repaired by a worker.

## Choose and carry out the next action

| Evidence and authority | Action |
|---|---|
| Mechanism established; correction is local, reversible, within the current task and role; outcome and acceptance criteria unchanged | Implement and verify it now. Do not ask again for authority already granted. This includes correcting an agent-owned execution sequence before it fails. |
| Benefit uncertain, but a bounded evaluation fits the existing scope and budget | State what result would justify adoption and the stopping condition; run the evaluation. Retain the current approach if the result is inconclusive or adverse. |
| Required change crosses a frozen contract, role, footprint, budget or protected authority | Prepare a concrete finding/proposal and return it to the owning coordinator or operator. Continue independent work only where the handoff permits it. |
| Speculative, incidental, already addressed, or unlikely to repay its interruption cost | Leave it alone. Record a lead only if its owner has a concrete reason or trigger to revisit it. |

Before acting, identify the changed behavior, its permitted scope, verification and
how to undo the change without reverting someone else's work. Prefer a source fix
or existing test/validator over another instruction. At most one durable preventive
intervention per failure mechanism; consolidate existing protection where possible.
A local repair need not become a universal rule. Standing instruction changes still
require an explicit user request; this workflow does not grant self-edit authority.

Do not weaken success criteria, omit required checks, expand permissions or reinterpret
an operational GO to make work cheaper. Preserve the selected handoff and its return
boundary. Repeated failed corrections follow the escalation rule in
[AGENTS.md](../../../AGENTS.md#continuous-improvement) and the lane its
[surface-allocation ADR](../../../docs/adr/2026-07-14-cc-cursor-surface-allocation.md)
names; relabeling the next attempt as an optimization does not reset its count.

## Verify and return to the task

For a defect, demonstrate the failure before and its absence after the change using
the owning diagnostic workflow. For a plan correction, trace the actual inputs,
outputs and final verification through the corrected sequence. For an efficiency
claim, retain comparable before/after observations when available; separate predicted
benefit from measured benefit. Check relevant adjacent behavior, not unrelated work.

Tie evidence to the delivered revision or artifact. Run applicable project checks
through the launcher in [AGENTS.md](../../../AGENTS.md#python-environment-and-local-checks).
A missing check is an unresolved limitation, never a pass. Revert an unsuccessful
candidate where appropriate or report what remains unresolved; do not adopt it merely
because it was implemented. Resume the assigned outcome and disclose material changes
in the normal task return. Verification does not confer merge or release authority.

## Retain useful learning at its owner

For a reusable improvement, append a compact entry to the existing owning plan, PR
or campaign record. Routine local corrections can remain in the normal change report.
Use a stable heading/identifier and this shape; omit unavailable measurements rather
than inventing them:

```text
Improvement: <stable ID / short mechanism name>
Observation: <actual or anticipated failure/waste; source evidence>
Change and authority: <what changed; task/role authority; reversal path>
Verification: <artifact/revision; checks and outcomes; limitations>
Applicability: <where intended to help; where evidence actually demonstrates benefit>
Evidence links: <one or more tasks, experiments or campaign outcomes>
Disposition: <proposed / evaluated / applied / reverted / superseded; decision owner>
Follow-up: <only a concrete reuse/revisit trigger and owner, when useful>
```

Link later experiments and campaigns to this entry rather than copying its conclusion.
Record contrary results and reversals by the owner's mutability class under
[operational rules §14](../../../docs/operational_rules.md#14-corrections-land-where-the-error-is-read-not-where-it-is-convenient-to-write):
correct a living owner (open plan, same-session record) in place at the entry, including
its Disposition; for frozen evidence leave the body unedited, add an addendum and put a
reader intercept upstream of the impeached claim. On reuse, read the current
disposition. Application in one campaign does not establish benefit in another.
Keep private evidence private, using permitted references in public files.
No new registry, ADR or permanent rule is required to capture an ordinary improvement.

## Why this skill exists

The operator requested this workflow on 2026-09-26 (PR #507) after approving its
behavior in chat. That request authorized this skill and the AGENTS.md Continuous
improvement routing only; it is not standing permission to edit instructions. The
prior section fired only after a correction or failure and did not say when an
in-scope improvement may simply be implemented. A registry, telemetry, automatic
policy editor, new hook and historical backfill were deliberately left out. The
source is repository-local and reached through AGENTS.md; publishing it to user-level
skill directories is a separate explicit release under [scripts/README.md](../../../scripts/README.md#skill-lifecycle).

Authoring validation was packaging and reference checks plus author-derived contract
walkthroughs (plan ordering, reproduced defect, uncertain optimization, frozen-handoff
conflict, protected authority, trivial edit, duplicate learning, repeated failed
correction). These are contract checks, not evidence of agent reliability or measured
savings; retain observed outcomes at their owner as described above.
