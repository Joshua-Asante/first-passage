# Attended Batch Qualification Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reach the unchanged portfolio's attended deployment through the smallest accepted qualification and operating architecture.

**Architecture:** Compare a protected operator batch against the active service before switching. Reuse canonical statistical/evidence owners; prepare manual settlement and attended recovery alongside qualification. The coordinator owns combined acceptance.

**Tech Stack:** Existing operations Python launcher, replay/source/adjudication libraries, SQLite journal, signed canonical artifacts, Linux protected execution and platform report ingestion.

**Spec:** [Approved direction and detailed design](../specs/2026-09-19-attended-batch-qualification-design.md).

Status: planning only, September 19. Joshua approved documenting the architecture
direction and replacement comparison. Detailed contract amendments, implementation
and redirection of the active E1 task are not accomplished by this document.

## Roadmap, not a blanket execution assignment

| Outcome | Required result | Dependency / return |
|---|---|---|
| B0: choose implementation path | Current accepted-state comparison, exact contract deltas, evidence reuse map and reasoned service/batch decision | First bounded handoff below; no code |
| B1: complete synthetic batch, if selected | Full real synthetic E1 -> G5 -> atomic commit -> separate seal, including interruption/VOID/resource evidence | Accepted B0 and amendments; coordinator issues implementation handoff |
| B2: production qualification readiness | Actual source/F1/depth package and production-class release; explicit production consumer acceptance | B1 plus source/route feasibility and shared-freeze boundary |
| B3: production E1 and admission | Authorized single E1 disposition, seal on PASS, D0 and separate D1 | B2; governing statistical decisions unchanged |
| B4: final n3 machinery and timed rehearsal | Authorized-plan separation, fresh-account identity and measured whole launch sequence | Engineering can overlap B1/B2; complete before real n3 and resolve timing before F1 |
| O1: actual settlement/route feasibility | Supported close evidence, unknown-request closure and fixed-book order semantics | Starts alongside B0; CAP remains sole verdict owner |
| O2: attended candidate | Feed/route binding, alerts, manual recovery, restoration, session authorization | Preparations overlap; acceptance consumes real route evidence |
| L1: release and launch | Combined candidate, fresh B7, sole n3, deployment GO/reseal and verified authorized activation | All predecessors; existing Phase 6 controls |

Do not interpret row order as serialization. Behavior-changing dependencies must
be settled before F1; exact permitted later bindings need an explicit inventory.
No live activation is authorized here. A phase's acceptance cannot be inferred
from completion of its components or a synthetic result.

## Remaining-work comparison at authoring

| Work | Incumbent service | Batch candidate | Assessment |
|---|---|---|---|
| Pure planning/source/replay | Substantial reusable implementation | Reuse same owners | No statistical rewrite saving |
| Request admission/transport/retries | Implemented in part; remaining budget/authority interactions | Fixed operator entrypoint and registered immutable inputs | Potential interface reduction; secure launch still owed |
| Supervision/recovery | S2 repairs and actual Linux acceptance; durable continuation complexity | One lifetime, terminal interruption, no automatic restart | Main potential saving; enforcement is not optional |
| N1/N2/Part A capture and G5 | S3-S5 integration remains in documented handoff | Same stage coverage remains | Significant common work |
| Commit/seal and invalidation | Remaining full-result integration | Same evidence/atomicity requirements | Limited saving |
| Production authority and n3 | Separate from TEST_ONLY E1 | Explicit B2/B4 outcomes | Neither supplied by a wrapper |
| Report retrieval | Automation may be deferred | Manual export/review accepted | First-release scope saving, no evidence waiver |
| Broker adapter/feed | Real integration and capability qualification owed | Same obligations | Likely independent deployment bottleneck |

This comparison uses inspected source and September 19 handoffs. The active task
may advance; refresh it before estimating effort. No hour/day estimate is supported
yet. Assign ranges only after inspecting actual remaining interfaces, tests and
host dependencies. Count operator attendance and interruption risk in the cost.

## B0 bounded handoff: choose the implementation path

**Selected outcome:** One reviewable decision in this document comparing the
current accepted service with the batch design, including exact reusable source,
remaining work, contract changes and a justified selection. No implementation.

**Prerequisites:** Architecture direction approved; manual daily export/review and
manual incident recovery accepted. Detailed specification now available for review.
Current accepted service head and Linux evidence must be refreshed. Actual route
and settlement remain unproven and may block production, not this comparison.

**Ownership:** Assigned coordinator performs the comparison and owns combined
acceptance. Existing E1 task retains its implementation; this handoff neither
changes its scope nor authorizes another writer in its checkout.

**Verification:** Read actual accepted source and retained verification records;
bind each reuse claim to its revision and each remaining capability to a producer,
consumer, test and acceptance owner. Trace launch through result/seal, cancellation
and interruption. Confirm all proposed removals have either an absent interface
or an explicit accepted contract delta. No Python/runtime suite is required for
document comparison. If running project Python, use the tested checkout's
`./fp.ps1 doctor` first, then `./fp.ps1 python ...`; report interpreter/revision and
actual results. Do not describe source inspection as passing execution tests.

**Checkpoint:** Record findings and unresolved conflicts here and return them to
the coordinator before selecting a replacement. Use CAP references for external
capabilities, not a copied capability ledger. Report a discovered scope-changing
contract conflict immediately; continue independent read-only comparison.

**Return boundary:** Return the completed comparison and proposed selection for
coordinator acceptance. Excludes implementation, changing other tasks, production
runs, signatures, provider contact/spend, broker actions, deployment and activation.
No automatic advance into B1.

- [x] Refresh the active E1 task's accepted head, unfinished repairs and evidence;
  distinguish code written, locally accepted, Linux-verified and production-ready.
- [x] Map reusable `qualification/checkpoint_plan.py`, `policy.py`,
  `policy_sources.py`, `evidence.py`, `journal_snapshot.py`, replay/Part A and
  `execution/{compute,worker,g5,store,campaign_store,profile}.py` responsibilities.
  These are starting paths, not permission to edit them.
- [x] Map batch launch/capture/commit to exact existing interfaces. Name new fixed
  entrypoint, release schema and resource-wrapper work; do not assume direct legacy
  `ProductionExecutor` or `run_production_e1` is admissible.
- [x] Resolve release, resource, interruption, result authority and n3 contract
  deltas against governing owners. Flag anything requiring a changed statistical
  or economic decision instead of silently broadening this design.
- [x] Compare remaining outcome-sized work and verification for both choices,
  including already completed S2 improvements and migration effort. Provide
  effort ranges only where supported, with assumptions and confidence.
- [x] Recommend service or batch. If batch saves no demonstrable work, retain the
  service and still take manual-operations and concurrency savings.
- [x] Return the decision and the next single outcome's proposed handoff. Await
  that assignment rather than implementing from this roadmap.

### B0 decision — 2026-09-19

**Retain the protected service; the operator-launched batch is not adopted.**
Compared read-only: accepted service `main@97d0319` (S1 accepted via
[PR #428](https://github.com/Joshua-Asante/first-passage/pull/428), merged
2026-09-19 11:29Z) against the S2 candidate
[PR #429](https://github.com/Joshua-Asante/first-passage/pull/429) `@8aa5753`
(INCOMPLETE / NOT ACCEPTED by its own record: R1 and R2a locally accepted, R2b
unassigned, R3/R4 open, no Linux run, installed release hash or image digest).
No runtime suite was executed; source inspection only. Coordinator: Joshua.

Grounds, bound to source at `8aa5753`:

1. The batch's main claimed saving — one lifetime, terminal interruption, no
   automatic restart — is already the incumbent's accepted posture (S2-R1
   liveness restriction; `execution/service.py:481-523` `recover_service`
   relaunches nothing). About 1,000 of #429's 2,244 non-test lines are durable
   *anti*-continuation barriers a batch also needs. Nothing to remove.
2. Everything that dominates the remaining schedule is identical on both paths
   and unbuilt: no N2/Part A adapter exists (`execution/compute.py` is N1-only,
   called solely by `execution/worker.py:41`); the only v2 evidence builder
   accepts `N1_ONLY` releases only (`qualification/evidence.py:202`) while campaign
   admission requires `FULL_E1` (`execution/campaign_store.py:73`); the execution
   store is schema-locked to one N1 checkpoint per attempt
   (`execution/store.py:30-36`); no commit, seal, ADJUDICATED/COMMITTED/SEALED
   state or function exists; `execution/compute.py:16` refuses n3. R4, all Linux
   evidence, the production-class release and n3 are owed equally.
3. What the batch removes is small (client campaign ops `SUBMIT_E1`/
   `FETCH_PLAN_CHUNK`, `client.py:55-94` reassembly, the transport half of
   R2b — about 300 lines); what it adds is a new versioned release
   schema/capability/authority path, bootstrap role, entrypoint + registry,
   launch-approval scope, receipt export, the five owner amendments in the design
   table, re-review of accepted S1/R1/R2a under a changed lifecycle, and porting
   the service-keyed tests (`test_campaign_supervision.py` 1,344 lines). Two
   design assumptions are contradicted by source: a single pre-validation envelope
   cannot be contract-derived (`execution/campaign_store.py:678-712` needs
   `contract.replay.budget`; the service's two-tier `begin_admission` →
   `bind_budget` is what any path gets), and "VOID in the same transaction as
   commit/seal eligibility" has no commit or seal to bind to. The design also
   inverts the role model (`execution/campaign_protocol.py:45-47`: operator may
   only STATUS/VOID).

Taken inside the service (the fallback this handoff prescribes): (a) the only
campaign submitter for the first attended release is the local operator/admin
client in the existing `client` role over the Unix socket — no remote transport
is claimed or tested; (b) single-lifetime is recorded as the first-release
posture — interrupted means terminal pending operator disposition, and no
funded-continuation design is owed before launch; (c) R3 is narrowed to a
bounded, still key-authenticated operator-local VOID; (d) manual daily report
export/review and manual incident recovery stay in O2/attended operations.

Conflicts and defects returned to the coordinator: #429 is not self-contained
(`tests/ops/qualification/execution/test_campaign_funding.py:8` imports the
unpublished `test_campaign_scheduler.py`; the `Tests` workflow fails at
collection); `Pylint` red on #429 only (new import cycles among the S2 modules);
the design's §Grounding is two merges stale (`c2e6eb2`, dirty `c77aac4`); the N1
Linux boundary runs on every PR but is exercised, not retained (no in-tree
evidence hash; not a required merge check); no test asserts the S2 cgroup is
empty after cleanup and no seal-race test exists. Verification state at
`8aa5753`: the N1_ONLY boundary is real-Linux on two hosts per PR; every S1/S2
suite is SQLite-real but OS-simulated (`test_campaign_supervision.py:16-21` nulls
`controller_cpu_guard`); the S2 Linux file has never run anywhere.

What would flip the decision: R2b's Linux evidence showing the warm-service
intent producer cannot be bounded — then the operator-launched single process is
the repair, using this design's reservation/envelope contract. The B1 row above
is therefore discharged by S3–S8 of the
[execution-slices plan](2026-09-18-full-e1-execution-slices.md), not by a
separate synthetic batch; B2, B4, O1, O2 and L1 remain as written.

**Next single outcome (assigned 2026-09-19):**
[S2-R2b handoff](../../briefs/handoffs/2026-09-19-full-e1-s2-r2b-warm-service-scheduler.md)
— warm installed service as the sole intent producer, operator-local client only;
R3/R4, Linux acceptance and S3 excluded. Sequence after: R4 → S2 Linux evidence
and combined review → S3.

Independent source-bound review, same day and same selection, from a second
coordinator session: [audit note](../../notes/audits/2026-09-19-b0-path-comparison-source-bound-review.md).
It carries the refreshed state table, reuse map, interface trace, contract deltas,
remaining-work comparison and corrections owed, including two the R2b handoff needs
before dispatch: the red-test file's only surviving copy is commit `1ef91be` (the
checkout its §0.5 (A) names was emptied on 2026-09-19), and the R2a records are lost,
so the handoff's Step 2.1 record becomes the source-bound R2a baseline.

## Implementation verification to preserve in later handoffs

B1 must exercise genuine compute, independent decisions and result/seal together;
not a collection of mocked services. Preserve source/seed and exact-depth tests,
full synthetic PASS/statistical FAIL, duplicate dispatch, crash cuts, forged
capture, source mutation, VOID races, budget exhaustion and actual Linux process
cleanup/permissions. Use the existing invariant/evidence harness where applicable.
Do not rerun unchanged suites solely because a new document was written.

B2 must prove production-class/source consumption separately from a TEST_ONLY
release. B4 must demonstrate that E1 cannot authorize n3, that n3 cannot redraw
E1/Part A, and that the full launch sequence fits actual evidence validity.
All later handoffs name exact tested source/configuration, interpreter, commands,
results, skips/failures and a return boundary. Combined acceptance remains with
the coordinator.
