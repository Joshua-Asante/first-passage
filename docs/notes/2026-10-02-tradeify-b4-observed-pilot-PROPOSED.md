# Tradeify B4 observed pilot evidence contract

**PROPOSED evidence contract and documentary reconciliation.** Source pin: `5eb800b50792dd204741f81e668c02f562b59a29`. Timing authority is the direct sitting-1 operator ruling relayed by root: “B4 pilot timing: it lands before T06 dispatch and doesn’t block R1. Yes.” Its pending mirror is PR #610 at `497b937aa01ebc381d6b0b025eafaee454bc5d1e`, H9 :534; this note does not represent it as merged into the source pin. [Pending mirror](https://github.com/Joshua-Asante/first-passage/blob/497b937aa01ebc381d6b0b025eafaee454bc5d1e/docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#L534)

## Timing conflict and preserved obligation

The requested ledger anchors 1422/1458 are now **1445/1481** at this pin. Line 1445 requires strengthening before the acceptance-grade or production run; line 1481 says due with T05, before CP-6. H9 repeats the latter. Read alone, these can incorrectly make B4 an R1 prerequisite. [Ledger :1445](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md#L1445) [Ledger :1481](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md#L1481) [H9 :534](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#L534)

Direct sitting-1 direction governs the timing conflict: before T06, not R1. It preserves the independently observed draw obligation. Proposed owner reconciliation, for coordinator integration:

> B4 plan agreement remains accepted for TEST_ONLY R1. Before T06/S8 dispatch, strengthen it to an independently observed pilot draw, with retained evidence from the executed sampling/replay path. B4 does not block H9 R1. “Acceptance-grade” in the earlier B4 carry means T06/S8 and production. Keep the evidence in the T05 carry inventory.

## Runtime evidence gap

The actual pilot samples an outer panel and an inner path in the probe domain, then invokes replay and checks sampled/replayed occurrence identity. The adapter calls this engine but exposes an initial-prefix custody callback, not a pilot-observation channel. [Engine :140](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/ops/c1_rail/qualification/part_a.py#L140) [Engine :156](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/ops/c1_rail/qualification/part_a.py#L156) [Engine :179](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/ops/c1_rail/qualification/part_a.py#L179) [Compute :169](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/ops/c1_rail/qualification/execution/compute.py#L169)

The wire encoder instead computes pilot seed-input digests from the plan. Both worker parsing and G5 reconstruction compare that record with the same planned identity. This establishes plan agreement, not an independently observed executed draw. [Encoder :142](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/ops/c1_rail/qualification/execution/evidence.py#L142) [Encoder :318](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/ops/c1_rail/qualification/execution/evidence.py#L318) [Parser :604](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/ops/c1_rail/qualification/execution/evidence.py#L604) [G5 evidence :2728](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/ops/c1_rail/qualification/evidence.py#L2728)

## Proposed observable contract

Producer: a bounded observation at the engine's real pilot sampling/replay boundary, within the original metered worker invocation. Emit a canonical private artifact binding the actual ordered outer-panel membership, selected path occurrence/source identities and completed replay association to attempt, work, source and runtime identities. Capture the existing draw; never generate an additional pilot.

Custody: durably retain the observation, its digest and producer binding in the worker capture. Consumer: G5 independently derives the expected probe selection from private admitted inputs, verifies the observed memberships and replay association, and binds the accepted observation to its assessment. Use existing source identities; no new random namespace.

These are proposed interfaces: the current plan-derived pilot field is not their producer. The integration owner must define exact schema, bounded storage, emission/failure ordering and assessment bindings before implementation. [Encoder :142](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/ops/c1_rail/qualification/execution/evidence.py#L142) [Compute :169](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/ops/c1_rail/qualification/execution/compute.py#L169)

Proposed rejection cases: missing observation; planned digest with no executed draw; different seed/selection; reordered or substituted occurrences; incomplete replay; observation from another work; stale digest; interruption before durable capture. Proposed positive case: one observed existing pilot independently reconstructs and remains bound through capture, assessment and reopen. Preserve the engine's existing replay identity checks. [Engine :165](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/ops/c1_rail/qualification/part_a.py#L165) [Engine :173](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/ops/c1_rail/qualification/part_a.py#L173)

## Return questions and dependency

Root accepts this contract; Claude retains campaign combined acceptance. Assign schema/producer/custody/G5 ownership and evidence cases in a separate bounded implementation dispatch. Carry approved term 8's three-validator joint-prefix and result-role/fault work separately; seven S6 terms do not adopt Q1/Q7. [Pending term-8 mirror :693](https://github.com/Joshua-Asante/first-passage/blob/497b937aa01ebc381d6b0b025eafaee454bc5d1e/docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md#L693)

Runtime source trace completed; no runtime tests were run because this note proposes the contract without changing it.
