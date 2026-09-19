# Spec 1: Epistemic foundation and decision traceability

**Status:** Draft sprint specification.
**Timing:** Week-1 assessment; principal delivery in weeks 2-3.
**Parent and shared authority:** [Six-week roadmap](../plans/2026-09-18-epistemic-six-week-roadmap.md).
**Companions:** [Governed learning](2026-09-18-governed-learning-brief.md); [evaluation](2026-09-18-learning-evaluation-brief.md).

## 0. Grounding

The roadmap's source table and commit anchor apply. In particular, `scripts/evidence_store/beliefs.py` already validates supported/contested/insufficient assessments and preserves historical observations. Its README describes decision-use review and derived indexes. Extend/connect these capabilities where gaps are demonstrated; do not create a second authoritative Worldview store.

## Problem and outcome

An agent needs to explain a consequential decision using evidence available then, relevant beliefs and assumptions, alternatives, and independently supplied goals and constraints. Existing advisory tools are a starting point; complete trading-workflow integration is not established here.

Outcome: the selected workflow produces a reconstructable decision, including a permitted decision to wait or decline.

## Scope and ownership

Worldview is the accountable view of versioned beliefs, support, contradictions, applicability and revision conditions. It is not execution authority. Keep observations, interpretations, beliefs, assumptions and user-defined policies distinct.

The evidence foundation owns preserved sources and reviewed annotations; existing source owners retain substantive authority. Indexes are derived and rebuildable. The decision workflow owns the record of actual evidence use; retrieval alone is not evidence of influence.

Reusable capabilities cover evidence, beliefs, inquiry, provenance and decision/evaluation contracts. Trading adapters own market interpretation, signals, costs, simulation and trading-specific constraints. Choose package placement in week 1 while preserving existing imports.

## Required contract

Each consequential decision persists:

- Stable decision/opportunity identities, decision time and knowledge cutoff.
- Source, belief and assessment versions; original availability, applicability context and unresolved contradictions.
- Material assumptions and their revision/falsification conditions.
- Separately referenced objective/constraint versions supplied by the approved policy owner.
- Considered alternatives, action or abstention, explanation and deterministic permission result.
- Evidence actually applied, declined or unassessed; replay code/data/configuration identities.
- Outcome/evaluation references appended without rewriting the original basis.

Reuse existing fields when semantics match. Distinguish event/effective time, availability to the decision-maker and import time. Historical import must not fabricate earlier knowledge.

Retrieval considers declared applicability and decision relevance, exposes unknown scope/conflicts and preserves historical receipts. Similarity rankings and LLM confidence cannot establish applicability or authorization.

## Acceptance cases

| Case | Expected result |
|---|---|
| Historical reconstruction | D uses E1; later E2 changes the belief. Replaying D still identifies E1 and its original assessment; current warnings appear separately. |
| Scope mismatch | A belief for context A is retrieved for B or missing context. Expose mismatch/unknown; do not silently apply it. |
| Policy independence | A supported belief favors a prohibited action. Record refusal and the governing constraint. |
| Abstention | Persist wait/decline for the opportunity with no simulated order; keep it in evaluation. |
| Missing provenance | Required bytes/version or policy binding is unavailable. Report the dependency, not invented certainty or permission. |
| Recovery | Duplicate opportunity delivery after restart preserves one decision and snapshot; rebuilding indexes preserves durable history. |

Accept this slice only with executable evidence for each case tied to the tested revision and a real historical decision mapped with disclosed gaps. Completeness alone does not establish epistemic improvement.

## Boundaries and falsifier

No wholesale directory migration, graph platform, cross-domain ontology, numerical confidence inflation or control changes. Storage replacement requires a demonstrated gap that incremental extension cannot address.

If explaining an earlier decision requires later knowledge, or belief history has conflicting authoritative owners, the outcome fails. Return the ownership/time-semantics defect before promotion integration.

## Delivery boundary

Return traceability slice, ownership map, acceptance evidence and integration gaps to the coordinator. Spec 2 consumes pinned records; Spec 3 owns improvement measures. This slice grants no deployment or learning-success claim.
