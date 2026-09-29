# CC handoff — CC-3 ordinary unknown outcome durably ends automation

**Date:** 2026-09-29.
**Status:** PREPARED; implementation not dispatched.
**Parent session:** X-1 decision and CC-3 handoff preparation.
**Spawn target:** Codex local, isolated checkout; no private inputs.
**Brief type:** CC handoff, bounded repair.
**Parent question:** TB-I3/T09 ordinary-unknown halt under halt/resume §2 and incident ADR §A11.2.
**Authority:** Joshua requested this handoff directly. The coordinator freezes a committed revision and records dispatch before implementation. No operational authority follows.

**Selected outcome:** When ordinary dispatch receives an unknown transport result or catches a send exception, the existing account owner records a durable incident and stays HALTED/INTERVENTION after later evidence and restart.
**Prerequisites:** Read-report against the frozen dispatch revision; no competing writer of the named files; committed handoff and coordinator dispatch. The current S5 build is separate and is not a prerequisite.
**Ownership:** One local executor owns the repair; the dispatching deployment coordinator owns review and combined acceptance. Joshua retains merges and operational GOs.
**Verification:** Named synthetic acceptance cases in §6, source-bound launcher records, related existing regressions and required checks.
**Checkpoint:** Report source anchors and the failing reproduction before editing; return on any scope/contract conflict; report integrated evidence at §7.
**Return boundary:** Reviewed synthetic repair and evidence, or a precise blocker. No real broker producer, adapter, same-session restart, later-session resume design, live notification, S5 work or commissioning action.

## §0 — Production reads

Starting source inspected for this handoff: main `1ca4233b5f486f2946b4bbad3b2d13b427370ecb`.
At dispatch re-read and report current anchors:
- `ops/c1_rail/book_account_owner.py`: _boot_locked; _ordinary_unknown_orders_db (825); _dispatch_locked; _dispatch_action_locked (1716); attempt insertion/send/result handling (1855-1887); _halt_db (2050); _observe_locked (2070).
- `ops/c1_rail/book_protection_owner.py`: send/result handling (643-666) and _protection_fault. It already halts on unknown protection results.
- `ops/c1_rail/book_bootstrap.py`: activation eligibility and incident invalidation.
- `tests/ops/test_attended_incident_rehearsal.py`: S1's two tests, strict XFAIL and helpers.
- `tests/ops/test_book_account_owner.py`: crash cuts, observation and ordinary dispatch fixtures.
- `tests/ops/test_book_halt.py`, `tests/ops/test_book_bootstrap_migration.py`, `tests/ops/test_feed_omission_session_end.py`.
- [Halt/resume §2/§4.1](../../spec/2026-09-14-tb-s3-halt-resume-contract.md), [incident ADR §A11.2](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md), and [H5(b) acceptance](2026-09-27-h5b-attended-incident-rehearsal.md).
- [Deployment roadmap](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md): T13 and staged acceptance. The roadmap does not dispatch follow-on work.

## §0.5 — Clarifications and recommended defaults

(A) **Recommended default:** repair explicit ordinary UNKNOWN/send-exception handling across entry, add, close and cancel paths that use _dispatch_action_locked. Do not reinterpret an accepted resting order, stale order-level evidence or a correctly handled refusal as a new incident.
(B) **Recommended default:** use existing _halt_db and persisted attempt identity. No schema, policy, allocation or broker-interface change.
(C) **Recommended default:** ordinary unknown is an incident even if later valid terminal facts arrive in the same transport result or immediately afterward. Evidence may settle an obligation; it cannot undo that observed incident.
(D) **Recommended default:** preserve existing protection-fault ownership. Do not add a second incident merely because the protection path already halts.
(E) **Recommended default:** preserve current restart fail-closed behavior. A journalled crash-cut UNKNOWN is retained and never resent; do not invent evidence that bytes were or were not sent.
A contradicted default, missing producer or necessary wider edit returns NEEDS_CONTEXT. Frozen behavior is not permission to resolve a new contract choice.

## §0.75 — Local dependency check

Vendor data: none. Credentials: none. Pine/runtime ports: none.
All fixtures are synthetic. The executor uses a public-only isolated checkout and the checkout's validated operations launcher.
No account, host, broker or external notification call is part of any test.

## §1 — Context and observed defect

Ordinary dispatch commits an UNKNOWN attempt before send. A caught send exception becomes BrokerResult("unknown").
At the inspected revision, returned facts are observed and attempts.state/observation are updated, but this path does not call _halt_db.
H5(b) proves that terminal evidence can therefore unblock admissions in the same session.
H4's classification repair and R-2's investigation closure do not discharge CC-3.

The existing _halt_db writes HALTED/INTERVENTION, increments generation for a new incident, invalidates bootstrap eligibility and records HALT events for applicable takeover plans.
Use that owner so the repair preserves all existing consequences.
The ordinary dispatch serializer encloses the send/result path. The worker must verify that no later subcommand or concurrent sender can pass between recognizing UNKNOWN and committing the halt.

## §2 — Execution steps and allowed files

Allowed production edit: `ops/c1_rail/book_account_owner.py`.
Allowed tests: `tests/ops/test_book_ordinary_unknown_halt.py` (new);
`tests/ops/test_attended_incident_rehearsal.py`;
`tests/ops/test_book_account_owner.py` only where existing expectations contradict the now-enforced halt.
Allowed documentation: this card's §7 return, a new `docs/notes/2026-09-29-cc3-ordinary-unknown-halt-evidence.md`, and the CC-3 implementation-status paragraph in the halt/resume contract.
A necessary edit outside this footprint returns to the coordinator. No qualification/S5 file is allowed.

- [ ] 2.1 Record source identity and source anchors. Reproduce S1 with its XFAIL disabled using pytest --runxfail on that node only. Retain the failing record.
- [ ] 2.2 Add the §6 cases using the existing synthetic owner/broker fixtures. Demonstrate the missing incident and post-terminal behavior before implementation.
- [ ] 2.3 In ordinary result handling, atomically persist the unknown observation and call _halt_db under the existing serializer before returning or allowing another automatic command. Use a deterministic attempt-derived incident id such as ordinary-unknown:<attempt_id> and reason execution. Validate the chosen placement against facts attached to the result and existing crash cuts. Preserve facts, reservations, operation ids and occurrence receipts.
- [ ] 2.4 Remove only S1's CC-3 XFAIL after the repair passes. Update its prior unknown_order-only assertions to the expected intervention fence. Update other affected assertions only when they concern this exact incident transition, retaining the underlying reservation/no-resend assertions.
- [ ] 2.5 Run §6/§10 verification, inspect all failures and skips, and return the complete diff and evidence. Update the CC-3 status only to synthetic repair demonstrated; real producer/route acceptance stays owed.

Concrete first reproduction after removing the S1 variance, using its existing helpers:

```python
account, broker = _rehearsal_owner(tmp_path, [BrokerResult("unknown")])
sent = _dispatch(account, intent(), "base", NOW)
assert sent.transport_state == "unknown"
assert (account.permission, account.authority) == ("HALTED", "INTERVENTION")
assert account.unresolved_attempts == (sent.attempt_id,)
assert len(broker.commands) == 1
```

The transaction placement is the executor's implementation task; merely adding a halt after return or at the next bar fails the contract.

## §3 — State and interface contract

| Event | Required observable outcome |
|---|---|
| Valid ordinary unknown result / send exception | Same attempted identity retained; one durable incident; HALTED/INTERVENTION; bootstrap ineligible |
| Later valid fill or postdating terminal | Existing observation consumer accepts and reconciles it; no authority restoration, no resend |
| Replay of the same occurrence | Existing receipt/retained attempt semantics; no new send or duplicate generation increment |
| Next member of a multi-target cancel / concurrent dispatch | No automatic command after the halt; retained obligations survive |
| Restart after result or before/after-send crash cut | Existing boot remains halted, obligations retained, no resend; do not claim crash ambiguity resolved |
| Accepted ordinary result / correctly handled rejection / pre-send refusal | No new CC-3 incident; preserve any independently required incident |
| Protection-path unknown | Existing protection incident remains effective without a duplicate CC-3 incident |

No new evidence producer is required for this synthetic repair. BrokerResult, the attempt journal, _halt_db and observe are existing interfaces.
Real evidence mapping and actual route recovery remain T09's. A notification pipeline and later-session authorization are separately owned.

## §4 — Hypothesis and falsifier

**H:** One incident at the ordinary unknown-result boundary prevents all same-session automatic sends after reconciliation while preserving evidence and unresolved obligations.
**Falsifier:** Any post-unknown automatic send, lost reservation, discarded valid evidence, renewed attempt, authority restoration, or new halt on an otherwise correctly handled refusal.
Passing an admission-refusal assertion without asserting durable incident, authority and restart behavior does not establish H.

## §5 — Constraints

- No S5/qualification changes, private input reads, host/account traffic, deployed configuration change, arm, trade or vendor contact.
- No timeout-based negative closure, request resend, automatic recovery or new resume API.
- No weakening H4's classification, incident identity, capture or existing protection tests.
- Preserve the Windows acknowledgment-filename failure as a disclosed separate defect; do not repair it in this footprint.
- Commit and push only within the coordinator's dispatch grant; merge remains Joshua's.

## §6 — Acceptance and return taxonomy

Parent-named acceptance cases in the new module:
- `test_unknown_result_halts_before_return`: parameterized ordinary entry/add/close/cancel, with valid existing fixtures/preconditions.
- `test_send_exception_halts_and_retains_attempt`.
- `test_terminal_or_fill_after_unknown_never_resumes`: later facts and facts attached to an unknown result; quantities/obligations reconcile without authority.
- `test_unknown_halt_survives_restart_and_duplicate_occurrence`.
- `test_concurrent_dispatch_serializes_behind_unknown_halt`: a second sender waits for the first result, then sends nothing after the durable incident.
- `test_unknown_halts_remaining_cancel_targets`: first target becomes unknown, later target is not sent.
- `test_accepted_rejected_and_refused_do_not_gain_unknown_incident`.
- `test_halt_storage_failure_suppresses_further_dispatch`: retain rollback semantics; no successful halt claim after storage failure.
Existing mandatory acceptance:
`tests/ops/test_attended_incident_rehearsal.py::test_lost_entry_response_terminal_does_not_restart_automation_in_session` passes without XFAIL;
`tests/ops/test_book_account_owner.py::test_crash_cuts_retain_obligation_and_never_retry_on_boot` remains satisfied.
Also run the related modules in §10, including the protection lifecycle, ownership and evidence modules. The coordinator may mark CC-3 RESOLVED in synthetic scope only when every required case passes; missing evidence is AMBIGUOUS, not acceptance.

Return exactly one status:
- DONE: every required criterion established, no unresolved concern.
- DONE_WITH_CONCERNS: selected outcome established with disclosed unrelated baseline limitations.
- NEEDS_CONTEXT: missing input or conflicting owner text; name it.
- BLOCKED: use context-problem, capability-problem, scope-problem or plan-itself-wrong and explain the exact obstruction.
A failed required acceptance criterion is not DONE_WITH_CONCERNS.

## §7 — Coordinator acceptance / executor return

Awaiting dispatch and implementation. Return:
revision, permitted file diff, baseline failure, per-case results, interpreter and launcher record paths, retained failures/skips, source stability, and exact remaining live-evidence obligations.
Coordinator reviews specification compliance, then implementation quality and the complete composed path.
No synthetic result establishes commissioning or whole-route acceptance.

## §10 — Audit hooks

Run from the checkout under test; use its configured --env when needed:

```powershell
.\fp.ps1 doctor
.\fp.ps1 python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-09-29-cc3-ordinary-unknown-halt.md
.\fp.ps1 --workers 2 python -m pytest tests/ops/test_book_ordinary_unknown_halt.py tests/ops/test_attended_incident_rehearsal.py tests/ops/test_book_account_owner.py tests/ops/test_book_halt.py tests/ops/test_book_bootstrap_migration.py tests/ops/test_feed_omission_session_end.py tests/ops/test_book_protection_lifecycle.py tests/ops/test_book_protection_ownership.py tests/ops/test_book_protection_evidence.py -q
.\fp.ps1 check
git diff --check
```

Report the full regression outcome first. If the known Windows acknowledgment node fails, retain that failed record and a separate run excluding that exact node; never label the full run passing.
Require completed records, zero verification exit, stable source, complete capture and expected reports for each claimed pass.
Before dispatch add the frozen committed handoff revision and the executor's seat/grants; this prepared card grants no implementation or operational action by itself.
