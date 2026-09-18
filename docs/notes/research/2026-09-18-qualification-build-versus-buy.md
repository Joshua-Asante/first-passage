# Qualification infrastructure build-versus-buy decision memo

Date: 2026-09-18. Status: research review accepted by the coordinating review;
recommendation only. This memo records the reviewed state, not current engineering
readiness or authorization to resume work.

## Recommendation and scope

**Retain the current implementation for completion and six-month maintenance of
the protected synthetic N1_ONLY slice. No replacement experiment is justified by
the evidence presently available. Engineering acceptance at the reviewed
checkpoint remains HELD. Full-campaign build-versus-buy remains unresolved.**

The original review concerned qualification infrastructure broadly. The completed
economic comparison covers synthetic N1: protected execution, captured evidence,
independent G5 reconstruction, and atomic acceptance of terminal FAIL or
PARTIAL/CONTINUE. It does not establish N1 correctness, production readiness, or
economic superiority for a full qualification campaign.

The reviewed implementation baseline is
[`6590b61e8d3bb2c2b26d5a47d68951216a3d8835`][baseline]. Local drafts comprised an
unused bounded-connection helper and additional concurrency, peer-handling,
transaction-ordering, and memory-profile tests. Estimates credit work written
while including unfinished integration and verification. These drafts are not
part of the pinned commit or established passing evidence. The
[supporting research record](2026-09-18-qualification-build-versus-buy-research.md)
preserves the responsibility map, estimate packages, assumptions, and sources.

Every option has the same completion boundary: interruption and uncertainty
handling, expiry and permission checks, invalid evidence and lost responses,
both VOID/publication and VOID/commit orderings, stopped-worker and resource-failure
evidence, accountable cleanup, and the invariant manifest, recorder/CI integration,
three targeted mutations, documentation, and independent review. The
[implementation plan][plan] records the outstanding closure obligations.
Production execution, production approval/key-custody tooling, full E1, and
deployment are excluded throughout.

## Alternatives and responsibilities

| Option | Potentially replaced duties | Retained custom responsibilities | Disposition |
|---|---|---|---|
| Retain | None | Execution, capture, recovery, validation, and acceptance | Complete outstanding closure within separately authorized work; recommended |
| Specific simplification | No concrete reduction identified | Same baseline responsibilities | No separate savings case demonstrated |
| Batch/Fargate | Portions of Docker launch, inspection, attachment, discovery, cleanup, and worker-host management | Reservation, uncertain-submission reconciliation, bounded capture, provenance, G5, VOID/acceptance, receipts | Evaluated design has unresolved isolation incompatibilities; conditional comparison only |
| Temporal with existing substrate | Possible coordination duties; no named existing deletion or required future responsibility demonstrated as avoidable | Worker substrate, launch safety, external recovery, artifacts, validation, G5, acceptance, cleanup | Added integration without demonstrated compensating benefit |

Batch replacement requires new submission, reconciliation, capture, identity, and
verification mechanisms. Past implementation effort is sunk cost, not a saving.

Temporal documents that `maximumAttempts=1` provides one Activity execution
attempt without retries. Additional application launch requests, reset/new-workflow
paths, external state, and acceptance still require controls. Its primary unresolved
issue here is demonstrated benefit. Temporal Cloud leaves workers customer-operated.
See [retry policies][temporal-retry] and [execution boundaries][temporal-security].

The evaluated Fargate artifact-fetch/upload design conflicts with the
[networkless worker profile][profile]; Fargate also lacks the evaluated tmpfs and
swap controls. This finding concerns that design, not every AWS Batch deployment.
See [Fargate restrictions][fargate-restrictions].

## Effort and break-even

| Remaining delivery | Low | Central | High |
|---|---:|---:|---:|
| Retain | 44 h | 82 h | 144 h |
| Temporal with existing substrate | 74 h | 140 h | 246 h |
| Conditional Batch/Fargate | 94 h | 174 h | 308 h |

These are reviewer estimates, not measured delivery times or commitments. Shared
delivery work of 22/40/68 hours is included once per option. Past effort and
unattended compute are excluded. Unknown six-month maintenance must be added.
Batch also requires compatibility work, **K**, with no credible finite estimate;
compatibility under unchanged requirements is not established.

Low estimates assume substantial harness reuse; central estimates allow one
repair/review cycle; high estimates allow repeated fixture or integration repairs.
Replacement totals include adapters, configuration and identities, migration,
documentation, bounded experiments, and integration verification. Batch receives
conditional credit for avoided Docker-specific closure work.

At central estimates, Temporal needs **more than 58 hours of net recurring savings
over six months** to reduce total effort; Batch needs **more than 92 hours plus K**.
The delivery premiums are `140 - 82` and `174 - 82`. Recurring savings must be net
of added platform maintenance. Shared maintenance cancels in the comparison but
remains an unknown obligation, not zero. No measured operating frequency or human
effort supports those savings. Unverified cash examples are omitted; no
money-to-hours conversion supports this recommendation.

Retention is supported by identifiable replacement work without demonstrated
compensating savings. The ranges overlap and do not prove unconditional economic
dominance. Shared-host hardening and universal immutable retention of rejected
bytes were already excluded; removing them again creates no saving. No stronger
execution-permit system is assumed mandatory.

The older "no new service" proposal is not an established architectural veto.
The [implementation ledger][ledger] records implementation authorization
superseding planning-only banners; documentation reconciliation remains necessary.

The [retained Linux run][run] recorded 18/19 and 17/19 passing, with successful
cleanup. Its failures remain verification obligations. They establish neither
recurring production incident rates nor accepted invalid results. Verification-host
duties are not assumed to describe production operations.

## Reopening conditions and ownership

Evidence that could reopen this recommendation includes:

- Measured recurring duties, frequency, and human effort sufficient for break-even.
- A concrete compatible Batch design with credible replacement costs.
- Named orchestration responsibilities Temporal could retire or avoid.
- A defined full-campaign scope with matched estimates across options.

These are reopening conditions, not assignments. An experiment may have value if
it resolves a consequential uncertainty; none is presently justified by this
evidence. The broader full-campaign question has only been partially investigated.

The main-task coordinator owns combined review acceptance and the recommendation.
Joshua owns authorization of experiments, requirement changes, or migration.
This memo authorizes no engineering resumption or expansion, provisioning,
purchase, qualification execution, or deployment.

[baseline]: https://github.com/Joshua-Asante/first-passage/commit/6590b61e8d3bb2c2b26d5a47d68951216a3d8835
[plan]: https://github.com/Joshua-Asante/first-passage/blob/6590b61e8d3bb2c2b26d5a47d68951216a3d8835/docs/superpowers/plans/2026-09-17-qualification-structural-closure.md
[ledger]: https://github.com/Joshua-Asante/first-passage/blob/6590b61e8d3bb2c2b26d5a47d68951216a3d8835/docs/superpowers/plans/2026-09-17-qualification-structural-closure.md#L776
[profile]: https://github.com/Joshua-Asante/first-passage/blob/6590b61e8d3bb2c2b26d5a47d68951216a3d8835/ops/c1_rail/qualification/execution/profile.py
[run]: https://github.com/Joshua-Asante/first-passage/actions/runs/35299214700
[temporal-retry]: https://docs.temporal.io/encyclopedia/retry-policies#maximum-attempts
[temporal-security]: https://docs.temporal.io/evaluate/cloud/security
[fargate-restrictions]: https://docs.aws.amazon.com/batch/latest/userguide/fargate-job-definitions.html
