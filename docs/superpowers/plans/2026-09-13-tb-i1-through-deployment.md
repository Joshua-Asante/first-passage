# TB-I1 through fixed-book deployment implementation plan

> **For agentic workers:** Execute with superpowers:executing-plans. Preserve one integration owner, the governing contracts and revision-bound acceptance evidence. Use small engineering slices within the four stages below.

**Goal:** Complete the shared production components, qualify the fixed book, and reach the attended initial arm through the existing gates.

**Architecture:** One shared sizing/policy/capacity implementation and one canonical fingerprint implementation serve replay and rail. The coordinator owns combined integration; Joshua owns substantive ratifications, merges and operational GOs.

**Tech stack:** Existing Python/pytest rail and daemon, private adapter ports, digest-pinned artifacts, exchange calendars and verified broker/feed interfaces.

## Current position

Simplified from `2c72294` on 2026-09-13 at the operator's request. Task 1's technical reconciliation and Tasks 2-3's bounded implementation are delivered through PRs #373-#378; the plan is #372. This is not a claim of operator review, merge, ratification or live qualification. Task 1's decisions remain in the ledger below.

**Stage 1 engineering packet verified locally:** canonical policy/geometry/config
fingerprints, explicit manifests, conformance vectors and serializer-to-host/capacity
integration are implemented. See the [fingerprint interface](../../spec/tb-i1-fingerprint-interface.md)
and appendix execution record. The repository-environment core/ops suite passed
1,841 tests (16 skipped); independent review and required local gates passed.
TB-I1 acceptance remains pending its explicit entry authority; mainline integration is complete.
Do not rebuild the completed sizing, context, capacity or transition components.

**Observed integration state, 2026-09-14 UTC:** PR #379 merged at `d53a06e3fa6018c6c36eb63771e5ad6d1ae961cf`, incorporating the fingerprint packet and stacked foundations. Mainline integration is complete; formal TB-I1 entry/acceptance remains distinct. The [rev8 halt/resume design](../../spec/2026-09-14-tb-s3-halt-resume-contract.md) now completes execution and schedule choices for ratification. It replaces the old session-latch proposal; no runtime implementation or policy ratification is inferred.

**Post-merge verification and Stage 2 start, 2026-09-14 UTC:** PR #380 merged at `8101ba498aad812e79c3d80c45f963cd67b55de6`; its tree equals checked head `6f0969b`. The operator explicitly requested Stage 2 commencement. The [runtime integration plan](2026-09-14-stage2-runtime-integration.md) records producer/consumer ownership and the first durable halt rejection slice. This implementation authorization is not a dated policy ratification or operational GO. Stage 1 technical/mainline work is complete; remaining formal acceptance records are still explicit.

The [companion appendix](2026-09-13-tb-i1-through-deployment-appendix.md) retains every original task requirement, governing-source reference, detailed acceptance case and execution record. Its task numbers provide the mapping below. The active plan owns status; the appendix supplies details without a second delivery checklist. Governing specifications and their operator gates remain authoritative.

## Four stages and acceptance matrix

This is the single delivery acceptance matrix. PRs and component plans should reference its rows and the original requirement IDs rather than copy acceptance lists. Each row's detailed requirements remain applicable in full.

| Stage | Deliverable and sequence | Exit evidence | Original requirements |
|---|---|---|---|
| **1. Close TB-I1** | Implement canonical policy/geometry/config fingerprints, runtime/tool manifests and conformance vectors. Integrate them with the completed shared sizing and capacity components in one engineering packet. | Exact-revision host-to-policy-to-capacity and serializer-to-verifier tests; literal byte/hash vectors and rejection cases; core/ops and required gates; independent review; frozen historical risk code, unadmitted registry and inert deployment configuration verified. No TB-I1 acceptance while its entry authority is unresolved. | Appendix Tasks 4-5; Task 1 entry condition |
| **2. Build and integrate the runtime** | One coordinated implementation plan for TB-I2 replay, TB-I3 rail, TB-C1 calendar and TB-T1 snapshots, delivered in bounded slices. Preserve each component's entry gate. | Replay/rail agreement on quantity, refusal, priority and flattening; real persistence and owner interfaces through primitive/producer/account scenarios, crash cuts, recovery and evidence rejection; calendar/closure/DST coverage; snapshot/fingerprint checks. Actual route capability evidence remains separate from model tests. | Appendix Task 6 and its packet table |
| **3. Qualify the fixed book** | TB-F1 freeze and measured compute budget; exact Part A depth ratification; prescribed legality screen, n1, n2/Part A/Part B and seal; TB-D0 policy admission and separate TB-D1 ORB GO. | Frozen sample sizes/streams/criteria and all F1 fields; both dated P2 ratifications at their prescribed points; required parity and calendar evidence; one prescribed qualification sequence and permitted digest/verdict records; non-vacuous admission checks. | Appendix Task 7 |
| **4. Qualify deployment and launch** | Complete M1, approved feed/equivalence, route/symbol capability, dedupe, frozen runtime bindings and attended dry-run integration. Then B7 snapshot/fingerprint -> sole final n3 -> deployment GO/reseal -> attended initial arm. | Exact candidate image and source/route/feedback/recovery evidence; current B7 seal and FBR equality; prescribed n3 verdict; allowed GO-only reseal; boot/request-bound fresh no-activity and image/config/GO checks; durable activation acknowledgement before risk-add admission. | Appendix Tasks 8-9 |

Preparation can overlap stages only within its own gates. Grouping live prerequisites and launch into Stage 4 does not postpone permitted M1 preparation or authorize early feed funding, emission, sampling or arming. Stage 2 code planning names the actual producer and persistence owner for every input; fixtures are not missing production capabilities made complete.

## Parallel prerequisites ledger

Update each row with a dated evidence reference when satisfied. Preparation may continue where already authorized; the blocked consumer may not proceed. Detailed proposals live in the existing contract closeout and governing documents, not a second decision list here.

| Prerequisite | Owner | Current status | Required evidence | Blocks |
|---|---|---|---|---|
| Policy/execution ratifications and TB-I1 entry authority | Joshua; coordinator prepares exact text | Pending | Dated acceptance of the applicable S3/P2 interface and deviations; reconcile TB-I1 entry authority explicitly. A merged PROPOSED ADR is insufficient. | Stage 1 acceptance; affected Stage 2 execution work; Stage 3 F1 |
| Unified regular/early-close schedule | Joshua ratifies; calendar/runtime owners implement | Rev8 design complete; ratification/calendar evidence pending | One accepted schedule including cutoffs, settlement, early closes and source-backed closure/DST coverage, used identically by replay, rail and procedure | Stage 2 calendar-dependent integration; Stage 3 F1 |
| Seven exports and intake/parity | Joshua supplies; coordinator intakes and verifies | Pending | Exact S-P, S-W1, S-W1P, S-W2, S-W2P, O-N and O-P bundles; source/override identity, normalization, coverage and all required parity PASS | Stage 2 decision-bearing replay use; Stage 3 F1 |
| Exact Part A depth | Coordinator derives at F1; Joshua ratifies | Not yet due | Frozen construction, sample/depth values, seeds and measured budget; second dated P2 ratification after F1 and before E1 | Stage 3 E1 |
| M1, feed and feed equivalence | Joshua attends/approves; implementation owners supply evidence | Pending | M1 RESOLVED; A9-gated selection/funding; approved source and TB-I5 equivalence under frozen criteria | Stage 4 live integration |
| Broker capabilities, symbols and dedupe | Broker/evidence owners; Joshua supplies attended evidence | Pending | Actual L1/L2 support for used semantics, all symbol verifications, TB-I4 after its M1/GO/disarmed gates | Stage 4 live use |
| Runtime binding and operational GOs | Joshua authorizes; coordinator verifies | Not yet due | E1/D0/D1 and symbol gates for TB-V1; separately authorized attended dry run; B7, final verdict, deployment GO and activation evidence | Stage 4 binding, integration and initial arm at their respective checkpoints |

Seven-export specifications, private storage paths and intake obligations remain in the appendix's parallel evidence track. P2/C10 snapshot-transition acceptance remains an explicit TB-T1 entry gate in the Stage 2 packet table; it is not implicitly approved by this simplification.

## Engineering and verification rules

- Keep one combined runtime plan and integration owner; add a code-level slice only when its actual base and interfaces are known. A slice must connect its producer, decision, persisted state and consumer through an observable outcome.
- Reuse existing shared components. Replay and rail must not acquire independent sizing, capacity or fingerprint implementations.
- Record each acceptance result once with the tested revision, inputs/environment, command and outcome. Reuse it while those inputs remain unchanged. Run affected regressions after changes, required repository gates before integration, and the combined acceptance suite at stage closure. Repeat broader suites when changed behavior, failures, dependencies or unresolved concerns justify it.
- Synthetic implementation tests cannot substitute for private export parity, authenticated snapshots, live feed/broker capabilities or operator ratification. Review/merge and qualification remain distinct from code completion.
- Preserve operation/fact identities, terminal-only releases, durable reserve-before-send, gross accounting, evidence freshness/completeness, retained uncertainty blocks and restart/concurrency safety.
- Preserve fixed K=1, the accepted sizing laws, disarmed configuration and historical risk-code bytes. Registry admission follows E1/TB-D0. No alternative candidate or additional outcome-bearing samples.
- Freeze qualification sizes, streams, criteria and compute budget before decision-bearing runs; keep qualification single-process. Final n3 is sole, Part A is not repeated there, and failure/void/expiry follows the accepted disposition with operator involvement, never automatic replacement draws.
- Preserve the full B7 -> n3 -> GO/reseal -> attended initial-arm sequence, fresh activation attestations and durable acknowledgement. No agent places trades. Private evidence stays in approved ignored roots; public outputs remain permitted digests/verdicts.

## Execution record

This revision changes delivery organization and evidence reuse only. The original plan body is preserved after the appendix notice (the closeout link is pinned to its historical commit so the plan PR stands alone), including technical vectors, rejection cases, packet entry gates and Tasks 1-3 execution history. No production code, acceptance threshold, quantity law, scope authorization or operational gate changes. Future stage status updates belong here; detailed evidence remains beside the owning component or in a linked dated execution record.

The simplified roadmap now updates PR #372 in place. PRs #373-#378 retain their original implementation scope and are restacked on it; their earlier plan edits are already captured in the appendix. Historical SHAs remain evidence references to the preserved pre-restack revisions.
