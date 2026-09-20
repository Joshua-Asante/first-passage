---
name: related-case-review
description: Check related cases when fixing a confirmed review finding or bug involving shared validation, duplicated behavior, or state transitions, especially when successive reviews uncover variants of the same defect. Excludes cosmetic edits and unrelated repository-wide hardening.
---

# Related Case Review

Close the confirmed defect across its relevant family of cases. A review comment identifies one example; it does not establish the full affected scope.

Use this as a focused extension of normal debugging and review handling. Verify the finding against the current code and governing requirement first. Do not apply an incorrect or already-fixed finding merely to satisfy a reviewer. Do not infer that a newly discovered issue was introduced by the last fix without historical evidence.

## Identify the failure family

Before choosing the patch, state the trigger, expected outcome, and violated rule in one or two sentences independent of the cited function or field. Derive that rule from the actual contract and implementation; do not invent a stronger requirement.

Distinguish the reported example from its cause. For example, a lookup that crashes on a JSON array suggests checking the related boundary's type assumptions, not just adding a guard to the named field. An operation that proceeds before a prerequisite finishes suggests checking other entry points that depend on the same prerequisite.

## Map the related cases

Read actual producers, consumers, shared helpers, and alternative entry points. Search by behavior and data flow as well as symbol names. Include relevant unchanged code: a diff boundary is not a contract boundary. Bound the family by the concrete input or state boundary and shared cause; a broad principle such as "reject invalid input" does not make every validator in the repository part of the task.

Select only dimensions supported by the defect:

- **Validation:** sibling fields subject to the same contract, nested input, alternate ingestion paths, and downstream operations that assume a type. Distinguish missing, null, wrong-shaped, and invalid scalar values where their outcomes differ.
- **State transitions:** callers that share the prerequisite; accepted versus completed work; partial completion, rejection, timeout, duplicate events, and late events where supported by the interface.
- **Durability:** restart or replay at the affected boundary, retained identities, and whether the fix survives reconstruction.
- **Ownership or authority:** the component that owns the decision, callers that can bypass it, and whether the decision can become stale before use.

Keep a compact working record in existing task notes, a PR draft, or the response; do not create a new document for every small fix:

| Related path or input | Why it shares the rule | Disposition and evidence |
| --- | --- | --- |
| Concrete caller, field, or transition | Shared prerequisite or assumption | Fixed with regression; already safe with code/test reference; not applicable with reason; or unresolved |

An empty search result or a similar name alone is not a disposition. Follow the relevant call chain far enough to establish which component enforces the rule. For a truly local defect, a short explanation that no other path shares the assumption is sufficient.

## Repair and verify the family

Prefer enforcement at the existing common owner when that preserves callers' semantics. If paths intentionally differ, keep separate implementations and verify each affected path. Do not force a refactor merely to remove duplication.

Fix confirmed related defects necessary to fulfill the authorized task. Record unrelated findings separately. If the user explicitly limits edits, inspect related paths and report any remaining exposure without exceeding that limit. This skill grants no permission to publish, merge, deploy, or broaden product behavior.

Choose regression cases from the map, not only the reviewer's example. Demonstrate the reported failure before the fix where feasible, plus materially different affected paths and a valid nearby case. For ordering defects, exercise delayed completion or the relevant event sequence; a mock that immediately completes every request cannot establish asynchronous correctness. For boundary validation, exercise the meaningful input categories across affected fields, using parameterization where useful. Cover distinct behaviors without requiring an exhaustive Cartesian product.

Re-read the changed rule and its consumers after the patch. Run the relevant integration checks when the change crosses a component boundary. Large suite counts and previous approval do not substitute for evidence on the cases in the map.

## Stop and report precisely

The bounded review is complete when every discovered path sharing the rule has a supported disposition, the affected behaviors have appropriate verification, and no known in-scope dependent defect remains unresolved. Stop expanding when additional paths no longer share the cause, contract, or dependency. Do not promise that all possible bugs are eliminated.

If a later review finds another variant, reopen the family map and identify the missed path or assumption before adding another isolated patch. Repeated discoveries call for better boundary coverage; they do not by themselves prove a rewrite is needed.

Report the underlying rule, related cases checked, evidence tied to the tested revision or working-tree state, and remaining limitations. Distinguish a repaired example from a verified family. Refresh completion claims after further changes rather than carrying forward stale validation.
