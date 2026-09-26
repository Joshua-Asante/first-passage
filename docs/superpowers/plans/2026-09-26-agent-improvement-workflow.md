# Agent Improvement Workflow Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner.

**Goal:** Enable bounded, evidence-backed agent improvements during ordinary work.
**Architecture:** AGENTS.md supplies the trigger and authority; one project skill supplies the procedure and compact owner-local evidence format. Existing verification and diagnostic skills retain ownership.
**Tech Stack:** Markdown skill and project instructions; existing Python validators.
**Spec:** ../specs/2026-09-26-agent-improvement-workflow-design.md

## Global Constraints

- Preserve task scope, acceptance criteria, protected controls and operator GOs.
- Frozen worker contracts remain frozen; coordinator acceptance remains separate.
- No standing-instruction self-edit authority beyond this requested build.
- No telemetry runtime, registry, publication or unrelated workspace changes.
- No independent seat dispatch without the repository's committed handoff contract.

## Roadmap and combined acceptance

1. Deliver a discoverable workflow and compatible root instruction entrypoint.
2. Verify packaging, references and concrete decision paths; record limitations.
Combined acceptance belongs to the inline coordinator in this chat. Successful
validation establishes repository-source readiness, not installation or reliability.
Starting revision: 1c5c08213f7edad9b7480fceddc075f2252bea22.
Workspace: managed agent-improvement worktree; primary checkout contains unrelated work.

### Task 1: Discoverable improvement workflow

**Selected outcome:** An agent reading AGENTS.md can act on an evidenced in-scope improvement and find the full workflow.
**Prerequisites:** User approved building this workflow; design above; existing owners read.
**Ownership:** Inline assistant executes and coordinates; same coordinator retains combined acceptance.
**Verification:** Inspect root/skill contract against the frozen scenarios in the audit note; verify relative references and frontmatter.
**Checkpoint:** Report authority conflicts or discovery gaps before expanding the scope; record the resolution here.
**Return boundary:** Return to inline coordinator after the root/skill pair is authored and reviewed. No runtime or publication work follows from this handoff.

- [x] Freeze scenarios and acceptance criteria before editing behavioral instructions.
- [x] Replace AGENTS.md Continuous improvement section, retaining the recurrence, instruction-change and escalation boundaries.
- [x] Write `.claude/skills/agent-improvement/SKILL.md` with act/probe/return decisions and owner-local evidence.
- [x] Trace the root entrypoint through the skill and its existing handoff/root-cause owners.

### Task 2: Verified repository source

**Selected outcome:** Workflow source passes relevant artifact checks with an honest evidence record.
**Prerequisites:** Task 1 accepted by inline coordinator after contract inspection.
**Ownership:** Inline assistant executes and coordinates; combined acceptance stays here.
**Verification:** Run launcher doctor, skill quick_validate, skill-refs and skills-no-constants with recorded command evidence; inspect all scenario outcomes and final diff.
**Checkpoint:** Record evidence and any pre-existing failures in the audit note; do not infer behavior gains from packaging checks.
**Return boundary:** Return source, verification and limitations to the user. No commit, push, PR, merge, external skill publication or autonomous deployment is included.

- [x] Run artifact validation through the checkout launcher and inspect the final record.
- [x] Complete scenario contract walkthroughs, including nearby simple cases.
- [x] Record final diff review, evidence locations and limitations.

## Execution record

Environment doctor passed: Python 3.13.2 at the primary checkout's `tmp/ops-env/Scripts/python.exe`; 62 locked packages matched.
Task 1 accepted by inline coordinator: root-to-skill routing and authority contract inspected. Task 2 artifact checks and eight inline contract traces completed; final recorded replay is the delivery check. Combined source acceptance is limited to these checks; see ../../notes/2026-09-26-agent-improvement-workflow-validation.md for evidence and remaining behavioral/distribution limitations.
