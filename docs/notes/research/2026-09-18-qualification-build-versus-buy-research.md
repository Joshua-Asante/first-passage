# Qualification build-versus-buy: supporting research

Date: 2026-09-18. Companion to the
[decision memo](2026-09-18-qualification-build-versus-buy.md).
This is a consolidated record of the accepted review findings and estimates,
not a new test run, implementation plan, or production-readiness claim.

## Question, method, and scope change

The original question was which qualification infrastructure, if any, should be
simplified or replaced to reduce remaining development and maintenance effort.
The review compared retention, specific simplification, AWS Batch, and Temporal.
It excluded live execution, strategy behavior, and changes to qualification
acceptance criteria. Monitoring and key custody received only a brief screen.

Five bounded tasks produced: (1) the burden inventory, (2) the execution trace,
(3) the capability comparison and corrective addendum, (4) the same-scope
break-even analysis, and (5) the decision memo. The reviewed reports were supplied
to the coordinator; this record incorporates accepted corrections rather than
preserving superseded claims as competing conclusions.

The economic comparison narrowed to completing the protected synthetic N1_ONLY
slice and maintaining it for six months. Production and full-campaign development
were excluded equally across options. The result therefore does not close the
original broader question. Future full-campaign benefits require a matched scope
and estimates before they can change this recommendation.

## Evidence baseline and limitations

- Implementation: committed `6590b61e8d3bb2c2b26d5a47d68951216a3d8835` on the
  structural-closure branch. Reviewed local drafts were an unused bounded-connection
  helper and concurrency, peer-handling, ordering, and memory-profile tests.
  They were not credited as verified behavior.
- Historical execution evidence: [Linux run 35299214700][run], at
  `67b93dd853113f7bb693cae9256ad3b2cb65f356`. The committed execution implementation
  was unchanged at the reviewed baseline; later changes included documentation
  and a byte-identical test rename.
- Retained reports: host 1 had 18 passes and one failure; host 2 had 17 passes and
  two failures; both had zero skips and successful cleanup. Stopped-worker readiness
  failed on both hosts; host 2's memory case exited 137 with `OOMKilled=false`.
  Both memory cases recorded `IN_DOUBT`; this is not evidence of invalid acceptance.
- The [implementation ledger][plan] records the retained evidence and remaining
  lifecycle/invariant work. This publication does not include raw CI artifacts;
  hosted artifacts may expire. The reported historical counts are not a fresh
  verification claim.
- History inspected in the inventory covered 2026-09-15 through 2026-09-18,
  including the PR 415 repair history and structural-closure work.
- Production artifacts, custody arrangements, actual run frequency, intervention
  rates, maintenance history, and operating costs were not established.
- All engineering-hour estimates below are reviewer estimates. None is a measured
  delivery time, commitment, or approved budget. No new qualification run or
  experiment was performed for this research.

## Responsibility trace

References in this table point to the reviewed commit, not moving main.

| Boundary | Current decision owner and durable evidence | Failure/retry behavior and evidence limit |
|---|---|---|
| Approval and staging | External approval/source authorities; administrator stages signed, hash-bound inputs; [admission][admission] validates them | Production producer remains an external prerequisite; partial staging recovery is not defined in the execution journal |
| Admission/reservation | [Supervisor][service] and [store][store]; attempt identity, plan, context, and DISPATCHED event | Exact resubmission returns the same execution; changed binding conflicts; duplicate submission was observed in retained runs |
| Container creation/start | Supervisor; container identity and START_INTENT before start | Create-before-record gap uses owned-container discovery; uncertain active states become IN_DOUBT, without replacement execution |
| Computation/capture | Isolated worker computes; [launcher][launcher] bounds output and runtime observations; validated bytes precede CAPTURED | Exit zero is insufficient; missing or invalid frames reject. Reliable stopped-worker and consistent OOM evidence remain open |
| Attestation | Execution authority signs exact durable CAPTURED bytes | Restart may re-sign captured bytes; validity is checked again before publication |
| Reconstruction | [G5][g5] independently reconstructs evidence and authenticates a proposed result | Candidate artifacts grant no acceptance; N1 cannot produce complete E1 PASS |
| Acceptance/VOID | Supervisor/store serialize validity and first acceptance with SQLite transactions | VOID first prevents fresh acceptance; acceptance first preserves history; exact receipt replay remains available; real concurrent ordering proof was incomplete |
| Recovery/cleanup | Supervisor discovers and stops owned work; resumes eligible captured signing | Cleanup observations and pending issues remain application responsibilities; uncertain execution is never promoted to success |

The current trust model trusts the administrator, runtime, approved service/G5/
worker code, and enrolled authorities. The client, its objects, paths, and proposed
results are untrusted. qexec's Docker access places it inside the privileged trusted
base. API restrictions are not protection against a malicious host administrator.
See the [execution-boundary design][design].

## Burden inventory and adjacent screen

| Burden | Disposition at the review |
|---|---|
| Stopped-worker readiness and memory-failure evidence | Open fixture/infrastructure verification work; no supported recurring incident rate |
| Bounded RPC handling and actual lifecycle/transaction races | Local drafts existed; integration and real-process evidence remained open |
| Invariant manifest, CI wiring, mutations, and independent closure | Required N1 work; existing parser/model libraries are reused |
| Full campaign, cumulative budgets, sealing, production source/approval/custody | Outside the N1 estimate; retained as broader prerequisites, not vendor-removable work by assumption |
| Fresh verification hosts and evidence inspection | Verification duty; frequency and human time unknown; not presumed production topology |
| Shared/reused-host hardening | Conditional future work, excluded from the disposable-host N1 baseline |
| Historical authority and fixture defects | Resolved/superseded items were not charged again as unfinished work |

Monitoring warranted a separate follow-up screen: alert delivery, heartbeat
detection, acknowledgment, and attended recovery remained operational questions.
Key custody had insufficient operational evidence to estimate duties or savings.
Neither screen authorized new work or contributed savings to the N1 comparison.

## Candidate boundaries and corrected conclusions

| Responsibility | Retain/simplify | Batch on Fargate | Temporal Cloud with existing substrate |
|---|---|---|---|
| Approval, domain validation, G5, acceptance/VOID, receipts | Custom | Custom | Custom |
| Submission/scheduling | Existing service | Product capability plus application reservation/reconciliation | Workflow/Activity scheduling plus controlled attempt identity |
| Worker substrate/isolation | Docker/Linux | Managed substrate; evaluated design incompatible with current profile as written | Customer-operated substrate remains |
| Output custody/validation | Custom | Logs supplied; authoritative bounded result custody and validation remain integration/custom work | External artifacts and validation remain custom |
| Recovery | Existing journal and owned-worker recovery | Job state supplied; qualification uncertainty/acceptance recovery remains custom | Durable workflow history; external launch, artifacts, acceptance, and cleanup still need integration |
| Concrete simplification | None demonstrated | Conditional partial replacement | No demonstrated deletion or avoidable required N1 work |

Batch assumptions were a fixed job-definition revision, digest-pinned image,
`attempts=1`, explicit timeout, logs, and external artifacts. The documented
[SubmitJob API][batch-submit] has no client idempotency token: do not blindly retry
an ambiguous submission. [Retry settings][batch-retry] control additional job
attempts. [Timeouts][batch-timeout] are best effort and do not replace all
application budget checks. These facts do not establish an unconditional physical
exactly-once guarantee.

The [profile][profile] fixes no network and other isolation controls.
Artifact fetch/upload changes that boundary; [Fargate restrictions][fargate]
exclude the evaluated tmpfs/swap settings. A compliant replacement design was not
established. This conclusion does not disqualify other Batch compute environments.

Temporal's [retry policy][temporal-retry] explicitly supports one Activity attempt
without retries. [Workflow ID reuse rejection][temporal-id] is retention-bound.
Repeated application calls, new/reset workflows, and external side effects need
their own controls. [Temporal Cloud][temporal-security] does not host the workers.
Tests demonstrate specified fault scenarios; they do not manufacture stronger
vendor guarantees. Apply comparable trust assumptions to the current system.

The old no-new-service proposal was planning-only. The implementation ledger
records that implementation authorization superseded planning-only banners;
documentation reconciliation is needed, not an invented architectural veto.
Universal rejected-output retention and a stronger execution-permit service were
not established requirements. Neither is silently included in the estimates.

### Conditional retirement register

| Existing component/duty | Batch disposition | Temporal disposition |
|---|---|---|
| Launcher create/inspect/start/attach/discover/stop | Replace portions with submission, inspection, reconciliation, capture, and termination adapters | Retain |
| Service execution/recovery | Adapt Docker-specific stages; keep admission, intent, binding, capture validity, attestation, and uncertainty handling | Retain/adapt; Activity integration adds work; no whole-function deletion established |
| Store reservation/start/capture/attestation | Retain/adapt identities and evidence consumers | Retain conservatively; replacement safety design not demonstrated |
| G5, VOID, atomic acceptance, snapshots, receipt replay | Retain | Retain |
| Worker-host provisioning/patching | Potentially avoid for Fargate workers; acceptance hosting remains | Retain |
| Verification host harness and permission probes | Replace/adapt with cloud verification; not free production savings | Retain/adapt |

Disposable-host-only scope and omission of universal rejected-byte retention were
already in the baseline. They cannot be counted again as new simplification savings.
No equivalent role-consolidation design was demonstrated.

## Estimate packages and arithmetic

Triples are low / central / high focused engineering hours. Low assumes harness
reuse; central allows one repair/review cycle; high allows repeated repairs.
Unattended compute and past effort are excluded. Shared delivery work is added once.

| Group | Work package | Hours |
|---|---|---:|
| Shared | Manifest/recorder/CI wiring | 4 / 8 / 14 |
| Shared | Acceptance negatives and three mutations | 8 / 14 / 24 |
| Shared | Combined evidence audit and independent review | 8 / 14 / 24 |
| Shared | Document reconciliation/operator documentation | 2 / 4 / 6 |
| Retention | Bounded RPC handling and real peer verification | 4 / 8 / 14 |
| Retention | Stopped-worker/OOM fixture and evidence closure | 4 / 8 / 16 |
| Retention | Process, ordering, expiry, permission drivers | 8 / 16 / 28 |
| Retention | Linux execution, targeted reruns, evidence inspection | 6 / 10 / 18 |
| Temporal added | Workflow/Activity adapters and external-state mapping | 8 / 16 / 28 |
| Temporal added | Namespace identity, SDK, credentials, configuration | 6 / 10 / 18 |
| Temporal added | Attempt/artifact compatibility, cutover/docs | 4 / 8 / 12 |
| Temporal added | Bounded failure/replay experiment | 6 / 12 / 22 |
| Temporal added | Integrated cancellation/acceptance/replay verification | 6 / 12 / 22 |
| Batch added | Submission-intent/reconciliation/cancellation adapter | 12 / 24 / 40 |
| Batch added | Input staging, bounded capture, provenance/artifacts | 12 / 22 / 40 |
| Batch added | Infrastructure/IAM/job/image/storage/log configuration | 12 / 20 / 36 |
| Batch added | Historical identity handling, cutover/docs | 4 / 8 / 12 |
| Batch added | Bounded submission/failure experiment | 14 / 26 / 48 |
| Batch added | Provider-specific isolation/acceptance/export/cleanup verification | 8 / 16 / 32 |
| Batch avoided | Docker-specific stopped-worker/OOM closure | 4 / 8 / 16 |
| Batch avoided | Docker-specific lifecycle/permission driver work | 4 / 8 / 14 |
| Batch avoided | Worker-specific verification effort | 4 / 8 / 14 |

Shared totals: `22 / 40 / 68`. Retention-specific: `22 / 42 / 76`.
Temporal added: `30 / 58 / 102`. Batch added: `62 / 116 / 208`.
Conditional Batch avoided work: `12 / 24 / 44`.

| Delivery total | Calculation | Low / central / high |
|---|---|---:|
| Retain | Shared + retention-specific | 44 / 82 / 144 |
| Temporal | Retain + Temporal added | 74 / 140 / 246 |
| Batch | Retain + Batch added - Batch avoided | 94 / 174 / 308, plus K |

K is unresolved isolation-compatibility work, not zero; a finite compliant design
was not established. The costed provider-verification package assumes a resolved
design and is distinct from that unresolved design/equivalence work.

Let Ms be shared six-month maintenance, Mr current substrate maintenance/operator
effort, Mt/Mb added platform maintenance, and Dt/Db recurring duties avoided.
All are unknown hours, not zeros. Total retention is delivery + Ms + Mr;
Temporal is delivery + Ms + Mr + Mt - Dt; Batch is delivery + K + Ms + Mr + Mb - Db.

Net effort saved versus retention is therefore:

```text
Temporal = Dt - Mt - (30 / 58 / 102)
Batch    = Db - Mb - K - (50 / 92 / 164)
```

Central monthly break-even thresholds are 9.7 hours for Temporal and 15.3 + K/6
hours for Batch. Low/high thresholds are 5/17 and 8.3/27.3 + K/6 respectively.
A favorable Batch sensitivity uses 62 added hours against 44 avoided hours:
18 + K net recurring hours over six months are still needed. These are thresholds,
not observed savings or proof of economic dominance.

For a demonstrated net saving d per verification campaign, the equal-cost campaign
count is delivery premium / d; positive savings require exceeding that threshold.
No campaign frequency or per-campaign saving was measured. Cash stays separate;
uncited illustrative prices and any money-to-hours conversion are excluded.

## Disposition and return boundary

Retain is the best-supported immediate choice for N1. No experiment is presently
justified; this is not a claim that experiments can never have value. Full-campaign
economics remain unresolved. Reopening requires actual recurring-duty evidence,
a compatible candidate design, a named avoided-work package, or a broader matched
scope. None of those conditions assigns new work.

The coordinator accepted the scoped review. Engineering acceptance was HELD at
the recorded checkpoint. Joshua retains authority over experiments, requirement
changes, and migration. Publication records the research and does not authorize
implementation, qualification, or deployment.

[run]: https://github.com/Joshua-Asante/first-passage/actions/runs/35299214700
[plan]: https://github.com/Joshua-Asante/first-passage/blob/6590b61e8d3bb2c2b26d5a47d68951216a3d8835/docs/superpowers/plans/2026-09-17-qualification-structural-closure.md
[design]: https://github.com/Joshua-Asante/first-passage/blob/6590b61e8d3bb2c2b26d5a47d68951216a3d8835/docs/superpowers/specs/2026-09-17-qualification-execution-boundary-design.md
[admission]: https://github.com/Joshua-Asante/first-passage/blob/6590b61e8d3bb2c2b26d5a47d68951216a3d8835/ops/c1_rail/qualification/execution/admission.py
[service]: https://github.com/Joshua-Asante/first-passage/blob/6590b61e8d3bb2c2b26d5a47d68951216a3d8835/ops/c1_rail/qualification/execution/service.py
[store]: https://github.com/Joshua-Asante/first-passage/blob/6590b61e8d3bb2c2b26d5a47d68951216a3d8835/ops/c1_rail/qualification/execution/store.py
[launcher]: https://github.com/Joshua-Asante/first-passage/blob/6590b61e8d3bb2c2b26d5a47d68951216a3d8835/ops/c1_rail/qualification/execution/launcher.py
[g5]: https://github.com/Joshua-Asante/first-passage/blob/6590b61e8d3bb2c2b26d5a47d68951216a3d8835/ops/c1_rail/qualification/execution/g5.py
[profile]: https://github.com/Joshua-Asante/first-passage/blob/6590b61e8d3bb2c2b26d5a47d68951216a3d8835/ops/c1_rail/qualification/execution/profile.py
[batch-submit]: https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html
[batch-retry]: https://docs.aws.amazon.com/batch/latest/userguide/job_retries.html
[batch-timeout]: https://docs.aws.amazon.com/batch/latest/userguide/job_timeouts.html
[fargate]: https://docs.aws.amazon.com/batch/latest/userguide/fargate-job-definitions.html
[temporal-retry]: https://docs.temporal.io/encyclopedia/retry-policies#maximum-attempts
[temporal-id]: https://docs.temporal.io/workflow-execution/workflowid-runid
[temporal-security]: https://docs.temporal.io/evaluate/cloud/security
