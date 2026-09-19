# Attended release and operator-launched qualification batch

Status: architecture direction approved by Joshua in conversation on 2026-09-19;
this is the resulting detailed design for review. It is not an implemented
replacement, a production qualification approval, or authorization to redirect
the active Protected E1 task. Existing contracts remain authoritative until the
specific amendments below are accepted and propagated.

## Purpose and scope

Reduce time to the unchanged four-strategy Tradeify portfolio's first attended
release. Joshua accepted manual daily report export/review and manual incident
recovery for that release. Preserve portfolio economics, statistical criteria,
source provenance and independent acceptance. Trade automatic availability for
a smaller supported operational surface.

The first bounded design is an operator-launched qualification batch. Settlement,
broker integration and attended operations remain separate outcomes with one
deployment coordinator owning combined acceptance. This document does not
specify a new trading engine or change sizing, allocation or protection policy.

## Grounding and limits

Main documentation checkout is the older `c2e6eb2` with unrelated local files.
Read-only source inspection used
`C:/Users/joshu/.codex/worktrees/full-e1-s2-supervision/multi_firm_operations`:
`book_policy.py`, `book_sizing_context.py`, `account_close_evidence.py`,
`account_close_calculation.py`, `book_account_owner.py` and qualification
`execution/compute.py`, `worker.py`, `g5.py`, `campaign_store.py`.
These are observations of a developing candidate, not renewed acceptance of it.
Execution must refresh the accepted baseline and source-bound evidence.
At final authoring inspection its HEAD was
`c77aac476127a31e58ede2c1c0ff03e6406474ce` with dirty funding/scheduler, supervision,
store, profile and test changes, including new `campaign_funding.py`. No isolated
snapshot or execution test of those changes was performed here; do not attribute
the working bytes to the committed HEAD or treat the comparison as final.

Observed: compute has a store-free N1 adapter; worker/G5 explicitly reject
production authority; the service roadmap still owes full-stage integration.
The account owner retains UNKNOWN intent before transport and still exposes
`production_route_unavailable` outside its SyntheticBroker seam. A real route
adapter remains necessary. Manual operation does not supply it.

Owners read:
- [Full E1 governing design](2026-09-17-protected-full-e1-campaign.md).
- [N1 boundary](2026-09-17-qualification-execution-boundary-design.md).
- [Settlement/route feasibility](2026-09-16-tradeify-settlement-order-feasibility-design.md).
- [Phase 3 completion](../plans/2026-09-17-phase3-completion-handoff.md).
- [Phase 4 completion](../plans/2026-09-17-phase4-completion-handoff.md).
- [Current E1 coordinator handoff](../../briefs/handoffs/2026-09-19-full-e1-coordinator-handoff.md).

Joshua supplied a Tradeify support reply on September 19 to the September 16
inquiry: Tradeify has no proprietary certified EOD snapshot/API; timestamp,
filter, report availability and revision semantics belong to Tradovate. This
is operator-supplied correspondence, not an independently captured support
artifact. It closes the proprietary Tradeify producer avenue, not platform
report feasibility. It does not establish any report's missing semantics.

## Architecture comparison and decision

| Choice | Remaining work and trade-off | Disposition |
|---|---|---|
| Finish protected service | Continue supervision repairs, stage captures, G5, commit/seal and Linux integration; separately enable production and n3 | Valid incumbent; active task remains unchanged |
| Protected operator batch | Reuse statistical and evidence owners; replace request-serving and automatic continuation with fixed launch, a single campaign lifetime and terminal interruption | Recommended candidate, subject to measured remaining-work comparison |
| Same-user script with operator checkbox | Small wrapper but caller could modify inputs, outputs or claimed execution; loses the reason the protected boundary exists | Rejected |

Savings are architectural hypotheses, not measured dates. Batch removes remote
submission/chunk/retry APIs, repeated client admission and multi-lifetime compute
recovery from the new release's acceptance scope. It does not eliminate stage
integration, budget enforcement, atomic invalidation, independent G5/seal,
production source acceptance or n3. Do not delete already accepted service code;
retain historical inspection and keep legacy execution closed.

## Batch behavioral contract

### Owners and producers

| Owner | Produces/owns | Boundary |
|---|---|---|
| Operator/installation administrator | Approved installed release, registered immutable input bundle, exact launch approval | Trusted as in incumbent design; launch is a fixed entrypoint, never arbitrary code/path execution |
| Existing freeze/source owners | Contract, exact-depth authority, canonical source/config/runtime inventory | No seeds, depths, thresholds or source substitutions from command-line flags |
| Protected batch controller | Attempt journal, launch intent, resource scope, capture membership, current validity and commit | Agent cannot edit its installation, records or credentials |
| Isolated compute worker | Existing replay outputs and source proofs | No journal writes, signing keys or subsequent-stage authority |
| Independent installed G5 | Reconstructed decisions from retained capture and canonical plan | No replacement draws; no caller objects as execution evidence |
| Separate installed sealer | Signature over complete committed PASS and current validity | No compute or statistical decision authority |

Retain the existing trust assumption: administrator and privileged controller
are trusted. Operator initiation alone is not isolation. Worker, G5 and sealer
retain constrained identities and distinct keys; no agent-facing launch or
credential capability is introduced. Status can be read from exported receipts.

### Interfaces and state

Proposed interfaces, not currently callable:

1. `launch_registered_batch(bundle_id, approval_id)`: fixed installed command,
   available only to the operator role. Registry resolves IDs to original bytes.
   Validates release, authority class and immutable configuration. A protected
   attempt reservation and bounded outer execution scope precede expensive
   bundle validation; a crash there cannot grant another uncharged launch.
2. Controller invokes existing canonical plan/source/replay routines, extending
   their adapters for N1, joint N2/Part B and prescribed Part A. G5 runs after each
   required capture before the next stage. Stage selection is internal.
3. `read_batch_receipt(attempt_id)` exports immutable status/artifact identities.
   Repeated reads never launch work. Duplicate launch returns the existing
   disposition or refuses; it never starts another worker.
4. Operator invalidation durably marks VOID under the same journal transaction
   boundary as commit/seal eligibility. It also requests whole-job termination.
   A stop request is not proof of process death; publication remains forbidden
   even if cleanup is delayed. Final activation rechecks current validity.

Use existing canonical JSON, plan, artifact-role, snapshot and signature owners.
One protected persistence owner serializes launch, captures, validity and result
membership; do not create another independently writable acceptance database.
A distinct versioned batch release/authority prevents old service receipts or
TEST_ONLY output being mistaken for production batch acceptance.

States: RESERVED -> RUNNING -> CAPTURED -> ADJUDICATED -> COMMITTED -> SEALED.
Per-stage progression is recorded within RUNNING. Validity is separate and VOID
is irreversible. Statistical failure is a captured adjudicated terminal result;
interruption, malformed output, unknown execution or exhausted budget is not a
statistical FAIL. Record the precise terminal operational disposition.

There is no automatic continuation after controller/host restart. A started
attempt with incomplete capture stays interrupted/uncertain and cannot compute
again. Complete retained output remains inspectable but inspection alone cannot
publish fresh authority. Any salvage or replacement follows an explicit existing
disposition or accepted amendment; no automatic new attempt or namespace.

### Resource and publication boundary

One non-renewable CPU/wall/memory envelope covers expensive admission, workers,
capture, G5 and sealing, including descendants. Reuse proven host enforcement
where suitable. The original deadline must be enforced before campaign bootstrap;
a trusted outer launcher owns limits and physical termination. Child process
placement, counter loss, suspend/boot changes and cleanup require Linux evidence.
Conservative per-phase ceilings may partition the original allowance but may not
replenish it. Loss of trustworthy accounting blocks publication.

No generic multi-restart budget service is required for this batch. Durable
attempt identity and terminal-state persistence are still required. After a
captured result, publication verifies the current attempt revision, validity,
release, complete artifact membership and authority in the commit transaction.
Sealing binds exactly that committed result; VOID cannot be bypassed with a stale
assessment. Atomic write/finalization prevents partial capture from being PASS.

### Production and final n3

Synthetic full E1 acceptance is only engineering acceptance. Production requires
actual source acceptance, production-class installation/keys, F1, exact-depth
approval and all existing pre-freeze feasibility gates. This is an explicit
roadmap outcome; do not leave it implicit after TEST_ONLY completion.

n3 uses the same protected launch/capture machinery but its own fixed authorized
plan, fresh B7/account binding, frozen RNG/depth, final adjudication and launch
timing rules. E1 launch cannot request n3; n3 cannot rerun Part A or E1. Rehearse
the complete B7-to-activation timing synthetically before consuming real n3.
No freshness bound or permitted reseal rule is changed here.

## Attended operations boundary

Daily: operator exports originals plus query/account/timezone context; existing
parsers and settlement verifier construct/reconcile the package; operator reviews
the exact subject; account owner accepts its authenticated receipt before session
authorization. Collection may be manual; calculations and refusal rules remain
machine-checked. Preserve full-history comparison and correction handling.

Unknown close state, report meaning, costs, historical continuity or corrections
blocks that session. A later flat snapshot does not prove flatness at close.
September 14 is mandatory only if the accepted production chain requires it;
first inspect the chain. Do not reset history or bootstrap a new origin to avoid
missing evidence. Use existing CAP as the source-capability verdict owner.

Incident: durably stop new strategy commands, notify the operator, retain all
outstanding requests/exposure/protection obligations, and use the qualified
platform intervention procedure. No automatic resend or same-session strategy
restart. A later session still needs reconciliation and fresh authorization.
The proposed bounded platform-protection amendment must be reconciled with
governing contracts before relying on continued native protection. Native ATM
is an option only where actual behavior matches the portfolio and dependencies.

Manual recovery does not prove a lost-response request has no future effect.
That broker capability, ownership/partial-fill behavior and actual transport
integration remain critical-path work. Feed equivalence also remains required.

## Required amendments and acceptance

| Owner | Precise proposed change | Preserved |
|---|---|---|
| N1/full-E1 boundary and release schemas | Add a versioned operator-batch authority path; remove service RPC/automatic continuation as prerequisites for that path | Isolation, original source derivation, independent G5/seal, validity |
| Resource/recovery contract | Single-lifetime enforcement; interrupted batch is terminal pending disposition | Original allowance, no redraw, no fabricated completion |
| Phase 3/6 plans | Explicit production and n3 batch outcomes; shared inventory/freeze-change mapping | F1/depth, admission/ORB decisions, B7, sole n3, GO/activation |
| Settlement procedure | Manual collection supported as first-release procedure | Source semantics, history, original bytes and exact close evidence |
| Incident/Phase 5 contracts | Align operator recovery with already selected bounded-protection direction | Uncertainty, ownership and later-session authorization gates |

Review must resolve these deltas before implementation treats the batch as an
accepted replacement. No statistical or economic amendment is proposed.

Acceptance traces:
- Genuine synthetic N1 PASS advances to one joint N2/Part B and prescribed Part A;
  independent G5, complete commit and separate seal describe the same attempt.
- N1 or later statistical failure stops downstream computation as prescribed.
- Duplicate/concurrent launch, source/seed substitution, forged output, mixed
  TEST_ONLY/production authority and partial capture refuse acceptance.
- Kill before launch, during compute, after capture and during publication:
  preserve evidence and original attempt; never redraw or restart automatically.
- VOID racing G5/commit/seal prevents subsequent valid publication; stale receipt
  cannot activate. Actual Linux tests prove permissions and process enforcement.
- Production-source rehearsal establishes source consumption without a real
  outcome-bearing attempt. Separate synthetic n3 proves timing and identity.
- Actual settlement and broker traces are independently accepted; synthetic
  batch success never qualifies the live route.

## Next outcome

Use the [roadmap and bounded comparison handoff](../plans/2026-09-19-attended-batch-qualification.md).
Compare both paths at their current accepted revisions before switching work.
Choose batch only if its remaining integration, amendment and verification work
is smaller than the incumbent's remaining work. Do not restart architecture on
the strength of a shorter diagram.
