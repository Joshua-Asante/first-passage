# Track B E/P/U ratifications and TB-I1 acceptance

Recorded 2026-09-14 UTC. Operator: Joshua. Source: this task's explicit statement, “i approve your recommendations,” following the recommendation to replace parallel decision E with S3 rev8, retain P2 rev9 decision P, and reconcile U to the merged rev8 schedule. This records that approval, not a decision inferred from a merge.

Publication reconciliation, 2026-09-14: recovered the existing record and six modified addenda/status files from `codex/tb-ratifications` without resetting or modifying that worktree. Its original record SHA-256 was `26a24db6faca10cf15d27887fb5e713ba339a36889a9f7708fdfc7d2e7c19adb`. Reconciled against current main #382 (`420ce3af88ede04ff5503aa1c3f14cd2a16eea10`), retaining #381's Stage 2 start history with updated approval status. The older derived parallel-prerequisites copy contributes no additional approval beyond E/P/U recorded here; its approval, schedule and deferred-depth content is already represented by this record and #382. It is not copied over the merged intake ledger. The seven-bundle interface proposal is preserved separately and remains unapproved/unimplemented. A7 readiness and handoff work remains with Claude's ceremony lane.

## Approved revision

All approved content is present at merge `8101ba498aad812e79c3d80c45f963cd67b55de6` (PR #380):

| Decision | Approved content | Git blob before recording this approval |
|---|---|---|
| E | [S3 rev8](../../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md) and [halt/resume contract](../../spec/2026-09-14-tb-s3-halt-resume-contract.md) | S3 `190b7aa8879cb6f8f6e49d5841b3f8aa45cd41db`; halt/resume `d619b00ed57ce99f209f175fc44aceafde4ccb78` |
| P | [P2 rev9 first decision](../../adr/2026-09-12-tradeify-book-protection-instance-admission.md) | `f94be43e25a9f4e4c0b10ccf3bb115f41aded3ec` (unchanged from #379) |
| U | Halt/resume contract §5 schedule formula, consumed identically by S2/S3/O1 | halt/resume blob above |

## E — accepted execution contract

Ratified: durable account-wide halt; listener-owned qualified recovery; fresh bounded operator approval after reconciliation; no automatic resumption after source recovery, session rollover or restart. Retain the primitive, evidence, sizing, capacity and B1 contracts. Record the revised S2b addendum in its owning ADR. The old rev7 session-cleared latch and daemon-emitted feed-loss flat are not approved by this decision. Actual producers, implementation acceptance and route capability evidence remain required.

## P — first policy ratification accepted

Ratified: P2 rev9 fixed policy/response map and five scoped supersessions, retained Part A construction, stricter B1 statistic, B2 count correction, two-stage admission, canonical fingerprints, GO reseal and effective activation checks. The Part A depth supersession takes effect only on the second, exact-depth approval. C10 invalidation stops for the operator; no automatic replacement outcome-bearing sample. This first ratification admits no registry row and authorizes no qualification run or live action. The second decision must name F1's actual positive depth, measured deterministic budget and frozen contract/tool/runtime/vector digests.

## U — accepted schedule rule

Use America/New_York and the earliest applicable source-backed venue/symbol flat deadline V. Own-flat D is min(16:00 ET, V minus 15 minutes); risk-add cutoff is D minus 15 minutes; mandatory flatten start/evidence check is D minus 5 minutes. Thus covered regular sessions yield 15:45 / 15:55 / 16:00; a verified V=12:59 row yields 12:29 / 12:39 / 12:44. These examples do not verify any particular calendar row. 16:30 is reconciliation only. Reject the parallel packet's alternative 15:30/11:44 flatten-start proposal. Route timing, calendar provenance/coverage and regenerated affected replay/parity evidence remain required; insufficient measured closure time returns for a coordinated schedule amendment.

## TB-I1 combined implementation acceptance

Integration-owner verdict: **ACCEPTED — bounded TB-I1 engineering packet**, following the now-explicit E/P contract authority. Implementation revision is PR #379 merge `d53a06e3fa6018c6c36eb63771e5ad6d1ae961cf`; #380 changes only the reviewed design. Evidence is retained in the [Tasks 4–5 engineering record](../../superpowers/plans/2026-09-13-tb-i1-through-deployment-appendix.md): 1,841 core/ops tests passed, 16 skipped; final 90 fingerprint cases; literal independent byte/hash verification; integration-chain rejection cases; independent review; required gates; inert registry/allocations and unchanged historical risk files. This approval record does not substitute for that implementation evidence.

Stage 1 is closed at the engineering/contract level. This does not qualify the fixed book or accept durable broker recovery/resume. Stage 2 proceeds under rev8; #381 is a separate halt-only implementation PR, not part of this TB-I1 acceptance. Seven exports/parity, calendar/route evidence, later policy depth approval, admission, operational GOs and attended activation remain open. The approval record's repository publication/merge is tracked separately from the operator's actual decision.
