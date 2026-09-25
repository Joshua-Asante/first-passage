# Tradeify qualification assurance: session review

Status: discussion record, 2026-09-25. The operator requested a challenge to
expensive assurance mechanisms, then authorized saving the session and opening
a draft PR. This is not an approved replacement design, contract amendment,
implementation handoff, task pause, statistical dispatch or deployment authority.

## Question and evidence

Which plausible failure does each mechanism prevent, and why is a cheaper
control insufficient for the first attended deployment?

The [execution boundary design](../superpowers/specs/2026-09-17-qualification-execution-boundary-design.md)
treats the requesting agent, its workspace and proposed results as untrusted,
while trusting the administrator, privileged supervisor and approved worker.
The [structural audit](audits/2026-09-17-pr415-structural-assessment.md)
records missing legality evidence accepted as PASS, invalid contract contents,
and manufactured completion accepted through shared TEST_ONLY validation. The
last finding was not a demonstrated production-key exploit. These findings
support semantic validation and trustworthy capture; they do not uniquely
establish the cheapest architecture that provides them.

The [B0 comparison](../superpowers/plans/2026-09-19-attended-batch-qualification.md)
retained most security, accounting and signing obligations in both alternatives.
Its service-over-batch decision compared implementations under substantially the
same assurance contract, rather than deciding whether that contract was needed.

The [execution ledger](../superpowers/plans/2026-09-18-full-e1-execution-slices.md)
records S3/N1 acceptance on September 22 and S4 CHANGES REQUIRED on September 24;
STATE's S3-S8 outstanding summary lagged those entries. It also records budget
settlement and stage-generalization defects. Those are evidence of maintenance
cost, not proof that every affected check is dispensable. This session inspected
records and selected source; it did not rerun their historical tests or verify
live infrastructure. Claude's supplied response cites main@ad07d40; this review
does not claim to have independently verified that whole revision or its defect
count. The local session started at 1c5c082.

## Mechanism comparison: proposals, not dispositions

| Mechanism | Failure prevented | Cheaper candidate and its limit | Provisional direction / owner |
|---|---|---|---|
| Protected service and isolated worker | Fabricated completion, mutable inputs or substituted outputs | Operator-triggered protected runner, pinned inputs and externally retained capture; insufficient if the agent can alter the runner, outputs or attempt history | Keep the execution boundary; compare service cost with batch. Execution boundary design |
| Separate execution, G5 and seal principals/keys | Computation grants itself acceptance or release authority | Protected capture, independent verifier and operator-controlled final approval; extra principals may matter when genuinely separate authorities consume evidence | Preserve verification; justify incremental seal-service benefit. [Full E1 contract](../superpowers/specs/2026-09-17-protected-full-e1-campaign.md), S6-S7 ledger |
| Detailed cumulative accounting across admission, compute, verification and signing | Runaway work or renewed allowances through retries | Whole-job time/memory/cost bounds plus separately enforced sampling and attempt limits; insufficient if work escapes the scope or spans resumptions/hosts | Separate statistical sampling limits from infrastructure spending limits. Full E1 contract, S1-S5 ledger |
| No-redraw and terminal interruption rules | Outcome-dependent retries and hidden alternative samples | Predetermined deterministic recovery under identical inputs, runtime and sample addresses, with all attempts retained; insufficient where determinism or attempt completeness is unproven | Retain anti-selection guarantees; investigate a narrower interruption rule before freeze. Full E1 contract and ledger shared contract |
| Atomic result, VOID and exact signing recovery | Partial or revoked evidence becomes current authority | Single writer, atomic completion, protected artifacts and current revocation check; insufficient for concurrent/disconnected consumers requiring stronger receipt semantics | Keep atomic completion/revocation; justify exact signature-recovery obligations. S6-S7 ledger |
| Authenticated chunks and staging APIs | Substitution, truncation and unauthorized artifact access | Read-only files/artifact store with manifests and atomic publication; insufficient where remote role-scoped transport is required | Evaluate avoiding transport interfaces in the first local release. Full E1 contract section 2.2a |
| Extensive Linux lifecycle testing | Mock-only isolation or untested failure transitions | Smaller acceptance suite for a genuinely smaller architecture; not an adequate replacement while retaining all existing transitions | Reduce architecture before reducing its tests. S8 ledger |
| Baked-in deployment GO, rebuild and reseal | Wrong release or unauthorized activation | Detached operator-signed approval bound to exact release/configuration, checked against a protected trust root and current validity; secure runtime consumption must be demonstrated | Evaluate replacement, retaining identity and revocation. [Admission ADR](../adr/2026-09-12-tradeify-book-protection-instance-admission.md), TB-I3/TB-D2 |
| Fresh snapshot and final n3 | Qualification does not apply to current account state | Fresh reconciliation plus a previously qualified operating envelope, only if its coverage and decision value are established | Keep n3 in current scope; any replacement is a separate statistical amendment. Admission ADR, [snapshot contract](../spec/2026-09-12-tradeify-account-snapshot-seal-contract.md) |
| Multiple approval packets | Engineering, evidence, spending and trading authority are conflated | One dossier with distinct decisions and separate session activation; insufficient when authority holders or decision timing actually differ | Consolidate ceremony without merging authority. [Deployment checklist](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) |

## Review of Claude's return

Agreement: B0 did not evaluate a materially reduced assurance contract; runtime
resource accounting and statistical sample limits deserve separate treatment;
a signed detached GO is distinct from an unsigned mutable volume file; final n3
is not merely packaging; useful accepted components should be reused.

Qualifications retained from the session:

1. **Intent is not the right trust boundary.** An honest but mistaken agent can
   rerun, overwrite or bypass controls. Name the actions it must be unable to
   perform, rather than selecting only between honest and adversarial agents.
2. **Permissions must enforce the boundary.** A rule against host administration
   is not equivalent to removing that capability. Review and runtime isolation
   address different failures; trusting reviewed worker code does not remove
   the need to prevent later input or evidence substitution.
3. **Retry requires a complete predetermined contract.** Pin relevant runtime,
   dependencies, inputs and sample addresses; establish reproducibility; retain
   all attempts; define comparisons for complete records and partial prefixes;
   reject discrepancies; bound retries and prescribe which output is accepted.
   One reproducibility test does not prove universal determinism.
4. **S4 R2-R4 are not all disposable accounting.** Custody integrity, snapshot
   shape, release binding, batch membership and actual commit-path verification
   can remain necessary in a smaller design. Correct formulas do not compensate
   for missing populations or accepting the wrong evidence. A pause should follow
   changed requirements, not packet numbers. No pause was issued here.
5. **Acceptance is not a reason to retain every dependency.** Compare remaining
   migration, implementation and operating costs. Keep accepted components when
   they reduce those costs; do not preserve their entire downstream contract
   solely because earlier slices passed.

## Proposed next decision and return boundary

Evaluate this baseline: the requesting agent is fallible and may bypass
instructions; mechanically protect execution, retained evidence and activation;
use independent verification and operator approval; require a specific benefit
for each additional role, accounting rule and publication protocol.

The next useful outcome is a source-bound keep/narrow/drop comparison. For each
proposed contract change, identify the exact owner paragraph, producer and
consumer, replacement control, residual failure, decisive verification and
remaining migration cost. Refresh the implementation state before estimating
savings. No measured time or cost saving is claimed here.

Keep statistical criteria, final n3 and real execution/incident requirements
outside this initial simplification unless the operator separately changes that
scope. Return the comparison for a decision before implementation or redirecting
active work. Existing contracts continue to govern.
