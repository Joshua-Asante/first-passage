# Spec 2: Persistent research and governed revision

**Status:** Draft sprint specification.
**Timing:** Contract alignment in week 1; principal delivery in weeks 4-5.
**Parent and shared authority:** [Six-week roadmap](../plans/2026-09-18-epistemic-six-week-roadmap.md).
**Companions:** [Foundation](2026-09-18-epistemic-foundation-brief.md); [evaluation](2026-09-18-learning-evaluation-brief.md).

## 0. Grounding

Use the roadmap's commit-pinned source table. INQHIORI and evaluation-order already govern inquiry/research. The evidence store is advisory; production protection, lifecycle and arm-gate owners remain authoritative. Mapping methodology to persistent workflow is a week-1 output, not justification for assuming a new workflow engine.

## Problem and outcome

Evidence can justify proposing a revision without authorizing its use. Durable research state must separate findings, reviewed beliefs, decision policies and activation.

Outcome: one existing simulated workflow completes evidence -> decision -> outcome -> evaluation -> revision proposal, with rejection, authorized sandbox activation and rollback demonstrated.

## Required workflow

1. Identify a material uncertain assumption from a decision or historical revision; record how resolving it could affect consequential choices.
2. Persist an inquiry: question, falsifiable hypothesis, scope, sources and budget. Map it to INQHIORI and existing campaign owners without duplicating authority.
3. Freeze protocol/criteria before inspecting evaluation outcomes; separate development from evaluation evidence.
4. Evaluate through a reproducible numerical runner. Preserve negative, null, invalid and incomplete results distinctly.
5. Propose a revision naming its predecessor, affected scope, evidence, uncertainty, expected benefit and rollback target.
6. Route it to the correct authority. Reviewed belief annotation, decision-policy change, strategy admission and operational activation are different actions.
7. If authorized for the bounded sandbox, activate the exact validated revision for future decisions and emit a receipt. Otherwise preserve the incumbent and rejection reason.
8. Evaluate subsequent outcomes; persist continued-use or rollback decisions under the frozen protocol.

Autonomous collection/proposals remain within existing authorization and budgets. LLMs assist interpretation/inquiry; asserted confidence cannot replace numerical evaluation or permission checks. This spec grants no new authority over objectives, controls, locked strategies, allocation behavior or execution permissions.

## State and interface ownership

The inquiry/campaign owner persists research state and unsuccessful experiments. Spec 3's evaluator produces a pinned result; the proposal links to it and Spec 1's evidence versions.

The authorized reviewer/policy owner decides eligibility. A proposed sandbox activation component owns the active revision pointer and receipts; validation and activation must refer to the same resolved configuration. Week 1 selects placement and the permitted revision family.

Durable semantics include open inquiry, frozen protocol, evaluating, evaluated, proposed, rejected/inconclusive, approved, active and rolled back. Map to existing statuses where possible. Approval does not imply activation. Interrupted activation remains recoverable and cannot be reported as active.

## Acceptance cases

| Case | Expected result |
|---|---|
| Complete loop | A pinned decision receives a complete simulated outcome; frozen evaluation produces a proposal linked to its original assumption. |
| Failed experiment | Failed criterion and supporting evidence remain discoverable; incumbent is unchanged. |
| Insufficient evidence | Missing/delayed outcomes or inadequate support produce incomplete/inconclusive disposition, not promotion. |
| Validation identity | Candidate/configuration changes after validation; activation rejects mismatch and requires fresh affected checks. |
| Authority boundary | A proposal exceeds the sandbox authority; activation is refused and governing controls remain authoritative. |
| Concurrent proposals | Two proposals target the incumbent; activating one makes the other's predecessor stale and prevents silent overwrite. |
| Restart/duplication | Retried outcome/proposal/activation contributes once; reconcile durable activation state before future decisions consume it. |
| Rollback | B replaces A in sandbox; rollback restores A for future decisions while preserving earlier B records. |

These establish workflow behavior, not revision benefit. Real records seed the workflow; synthetic fixtures verify recovery/rejection mechanics but cannot prove trading value.

## Boundaries and falsifier

No strategy optimizer, unconstrained self-modification, live execution path or automatic revival of rejected candidates. Existing re-proposal bars/research gates remain effective; resolve any conflict explicitly before implementation.

If learning silently mutates active behavior, erases failures, bypasses authority or rewrites prior evidence, acceptance fails. If no permitted revision family is feasible, report that finding rather than expanding authority.

## Delivery boundary

Return one sandbox loop, durable inquiry/proposal records, promotion/rollback evidence and missing producers to the coordinator. The roadmap owns combined acceptance; Spec 3 separately judges benefit.
