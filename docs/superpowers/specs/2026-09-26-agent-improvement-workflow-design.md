# Agent improvement workflow design

Date: 2026-09-26
Status: implementation of the operator-approved workflow in this chat

## Outcome and scope

Enable agents to notice a concrete plan flaw, prevent a mistake, repair a recurring
failure, or remove evidenced waste while doing authorized work. Complete bounded
improvements without a new approval round; return decisions outside that authority.
The operator requested this workflow first after approving its behavior in chat.
This authorizes the targeted AGENTS.md routing change and new project skill, not
future blanket permission to rewrite standing instructions.

## Existing and new responsibilities

AGENTS.md owns authority and the continuous-improvement entrypoint. Replace its
reactive-only wording with proactive triggers and an explicit in-scope action lane.
The new canonical project skill `.claude/skills/agent-improvement/SKILL.md` owns the
procedure. Existing root-cause-first and handoff-verify retain their contracts.
Frozen worker handoffs still return contradictions to their coordinator; correcting
an agent-owned execution approach is different from changing a frozen specification.

Use ordinary planning, correction and completion moments; no mandatory reflection
artifact when no useful opportunity exists. Confidence means a source-supported
mechanism, a bounded reversible intervention and a verification criterion, not a
self-reported probability. Unknown benefit permits an already-authorized bounded
probe, not automatic adoption or expansion of the task.

Keep durable evidence in the existing owning plan, PR or campaign record. A compact
improvement entry links observations, change, authority, verification, applicability
and later outcomes; multiple experiments and campaigns can reference the same entry.
Intended transfer is distinct from demonstrated transfer. Do not build a registry,
telemetry service, automatic policy editor, new hook or historical backfill in v1.

## End-to-end acceptance

An agent sees a concrete opportunity during authorized work, reads the relevant
source and existing protections, selects act/probe/return/leave alone, preserves
acceptance criteria, verifies any change, records only reusable evidence, and resumes
the assigned outcome. Future work can find and link the existing entry by mechanism
and affected path. No local verification implies merge, release, deployment or arm.

Validation covers plan ordering, a reproduced defect, uncertain optimization,
frozen-handoff conflict, protected authority, a trivial edit, duplicate learning,
and the existing two-failed-corrections return. Check frontmatter and references
with existing validators. Scenario walkthroughs are contract checks, not evidence
of agent reliability or measured efficiency. Independent behavioral trials and live
cross-campaign benefit remain unestablished until actually observed.

## Distribution

Source is repository-local and reached via AGENTS.md, including on surfaces that
do not automatically discover `.claude/skills/`. Publication to home/AppData is a
separate explicit release under scripts/README.md; it is outside this build.
