# CC handoff — CC-3 ordinary unknown outcome durably ends automation

**Date:** 2026-09-29.
**Status:** ~~PREPARED; implementation not dispatched.~~ FROZEN 2026-09-29 at `b77b6f4`, after the implementation had already run. The coordinator record (§8) states that order and assigns review and commit. Implementation returned; **not accepted**.
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

**Executor return, 2026-09-30 (CC-3 Claude Code session, Sonnet 5.5, seat worker under §8's grants), against the amended card (§8.1, §8.2 and §8.3). Status: DONE_WITH_CONCERNS.** The selected outcome and every criterion named in §6, §8.1, §8.2 and §8.3 are established on the head below. The concern is one disclosed baseline limitation that is unrelated to this patch: the full `tests/ops` suite has one failure, `test_qualification_isolation`, which fails identically on clean `main` (the "Verification" bullet). Nothing here is acceptance. The coordinator's review of the PR follows, and no synthetic result establishes commissioning or whole-route acceptance. This return supersedes two earlier ones, which stay in git history: the first (status DONE against `b77b6f4`, at `ec96a0e`), after which Codex found two P1 defects fixed by amendment 1; and the second (against §8.1 and §8.2, at `1013c22` and `cc7465e`), after which Codex found one P2 fixed by amendment 3.

- **Revision.** Card frozen at `b77b6f4` (SHA-256 `3cda0545…695b1`); coordinator record `98476a1`; amendment 1 (§8.1) `9dc0b64`; amendment 2 (§8.2) `0bfcee6`; amendment 3 (§8.3) `3952356`. Patch head `76a80e9870ca1d4a0ea852e978bb064d6b2ebc18` (code, tests and evidence note), on base `1ca4233b5f486f2946b4bbad3b2d13b427370ecb`. `main` was merged at `cd26d2b`, and Joshua's later `main` merge (`218d7a0`, no CC-3 or takeover file changed) was merged into the executor's branch at `3624d84`. No rebase; `b77b6f4` and every pushed SHA are unchanged. This return is a card-only commit on top of `76a80e9`. Checkout: `C:\Users\joshu\multi_firm_operations\.claude\worktrees\pr-363-babysit-671b91`.
- **Permitted file diff.** Production: `ops/c1_rail/book_account_owner.py`, and, under §8.3, `ops/c1_rail/book_takeover_owner.py` (one hunk only, the tail of `_advance_takeover_locked`). Tests: `test_book_ordinary_unknown_halt.py` (new); the S1 file and `test_book_account_owner.py` (§2); and, under §8.1, §8.2 and §8.3, `test_book_close_reconciliation.py`, `test_book_fence_classification.py`, `test_book_takeover_phases.py`, `test_pr409_owner_lifecycle.py`, `test_pr409_related_cases.py`, `test_pr409_review2.py` (one node), `test_pr409_review3.py`, `test_pr409_review4.py`. Documentation: the halt/resume contract's CC-3 status paragraph, the evidence note (with the per-change table, one row per changed node) and this card's §7, §8.2 and §8.3. `SyntheticBroker`'s empty-queue default is unchanged.
- **Repair.** In the unknown branch of `_dispatch_action_locked`, one transaction runs `_settle_attempt_db`, then `_halt_db("ordinary-unknown:<attempt_id>", "execution")`, then `_observe_locked(fact, ..., db=db)` for every attached fact; any exception sets `_input_send_suppressed` and re-raises. `_observe_locked` opens no transaction of its own when it is given `db`. In `_advance_takeover_locked`'s tail, the `takeover-child:<operation_id>` halt is skipped only when the child's result is `unknown`, has an attempt id, and `ordinary-unknown:<attempt_id>` is already in `incidents`; the `rejected` path and the `break` are unchanged. `_halt_db` already writes the takeover plan's `HALT` event when it inserts the `ordinary-unknown` incident.
- **Baseline failure.** `20260929T160142Z-0fa5f98ce430`: S1 with `--runxfail` on unmodified code. `20260929T160722Z-63341ffc753d`: 15 failed, 14 passed against unmodified code. `20260929T195919Z-96d59d4a2e3d`: `test_attached_fact_failure_rolls_back_halt_and_facts_together` fails against `ec96a0e`'s ordering, 1 failed and 17 passed. `20260930T040908Z-030c28581696` (against `84a2a78`'s production) and `20260930T050702Z-1c1bffc5078d` (against `218d7a0`'s production): both `[unknown]` takeover cases fail and both `rejected` cases pass, 2 failed and 2 passed each.
- **Per-case results.** All eight §6 cases, both mandatory existing cases, the two §8.1 cases and the §8.3 cases (`test_cancel_failure_fences_and_retains_exposure` and `test_flat_failure_fences_and_retains_exposure`, each for `unknown` and `rejected`: one incident, one generation step, one plan `HALT` event, exposure retained) pass in the full run below. The 14 explicit-unknown nodes assert the intervention fence plus reconciliation, and the 8 fixture nodes queue explicit `accepted` results; the evidence note's per-change table lists every changed node.
- **Interpreter and launcher records** (`tmp\ops-env\Scripts\python.exe` 3.13.2, from `.\fp.ps1 doctor`; each `record.json` is under the checkout's `.cache\fp-verification\<dir>\`):
  - `20260930T050730Z-848f1ad45d2c`: full `tests/ops` on the clean merged tree at `3624d84` (`218d7a0` plus the amendment-3 commits), `--workers 2`. Completed, `source_stable: true`, `capture_complete: true`, no capture errors; 1 failed, 2951 passed, 18 skipped (collected 2970).
  - `20260930T040957Z-27e3cdc64cff`: the takeover-related, CC-3 and protection modules with the takeover hunk. 483 passed, completed, exit 0, stable.
  - `20260930T061247Z-5ce1a417f3b7`: `.\fp.ps1 check` on the final bytes of the code, tests, evidence note and card as of `76a80e9`. Completed, exit 0, stable, complete capture, no report errors; the four amendment-3 file hashes in it equal the committed files.
  - `20260929T221943Z-2d4a2ad5a74c`: the same full run on a clean `main` worktree (`6c6759f`, no patch), still the valid baseline (nothing under qualification changed). Completed, stable; 1 failed, 2922 passed, 18 skipped, 1 xfailed.
  - Earlier records, retained: `20260929T211550Z-4b202ed9ff32` (full run at `c310128`, 1 failed, 2941 passed), `20260929T232718Z-1fed924ac92b` (`check` at `1013c22`), `20260929T161059Z-5ccb92360004` (§10 related suite at `b9b72f9`, no longer sufficient for acceptance), `20260929T195953Z-6a90667d1c75` (first full run, 22 failed, which amendments 1 and 2 address), `20260929T160754Z-99c084756091`, `20260929T174520Z-5d897db4ba48`.
- **Handoff validation.** `check_brief.py --type handoff` and `check_handoff_authority.py --all` at `76a80e9`: 0 HARD, 0 WARN, 0 violations. Neither is a recorded launcher command; they were re-run after this §7 edit and the results are in the executor's message on the PR.
- **Verification and retained failures.** The one failure in the full run, `test_qualification_isolation.py::test_qualification_suite_in_clean_process`, is the bridge that runs the whole qualification suite in one serial child under a 3,600 s hang bound. On this machine the child reaches about 68% of its 1,712 tests in that time (CI measured 1,079-1,538 s). It times out the same way on clean `main`, so it is independent of this PR. It is untouched and is not counted as a pass; CI's `pytest (3.11)` on the head is the check for it. The 18 skips are private inputs absent from a public clone. The known Windows acknowledgment failure did not occur and is untouched.
- **Machine-load caveat.** For the current full run (`…050730Z`), no other pytest was running when it started, but three from other sessions were running when it ended, so the load during the run is UNKNOWN. The earlier full run (`…211550Z`) was made while another session's pytest was running. Load can affect timing only; no other node is timing-bound.
- **Source stability.** All records show `source_stable: true`. The current full-run record is bound to the clean tree at `3624d84`; the only later changes are the evidence note and this card, the note being covered by the `check` record above.
- **Deviation and consequences, for review.**
  1. Implementation began before the freeze and dispatch; §8 records this as a procedural deviation, not repaired by re-running.
  2. `test_halt_storage_failure_stops_remaining_cancel_targets` and `test_protection_unknown_keeps_only_its_own_incident` have no fail-on-base evidence; the second is a no-duplicate control. `test_unknown_with_attached_fill_commits_capacity_and_halt_together` passes on both orderings by design.
  3. The cutoff-cancel case expects one `execution` incident at the cutoff, not a later `schedule` incident.
  4. Eight nodes hit an implicit unknown through `SyntheticBroker`'s empty queue; their fixtures were made explicit under §8.2, which was recorded by the executor at the coordinator's direction with no separate operator confirmation.
  5. After an unknown cutoff cancel or scheduled flatten, later automatic deadline sends are suppressed and operator intervention remains necessary. No deadline exception or resume route was added.
  6. Under §8.3 the production footprint was extended to one hunk of `ops/c1_rail/book_takeover_owner.py`. The coordinator admitted it as coordinator, and Joshua was told and has not overruled it; there is no separate operator confirmation.
- **Remaining live-evidence obligations.** The real broker evidence producer and route mapping; actual route recovery; same-session restart design and later-session resume authorization; live incident notification; commissioning and arming; operational GO. Crash-cut ambiguity is preserved, not resolved. The Windows acknowledgment-filename failure stays a separate defect.

Coordinator reviews specification compliance, then implementation quality and the complete composed path.
No synthetic result establishes commissioning or whole-route acceptance.

**Coordinator acceptance (2026-09-30), recorded by the executor at the coordinator's direction.** CC-3 is **RESOLVED in synthetic scope only**, at head `cc08f05` (this card as amended by §8.1-§8.3, executor return DONE_WITH_CONCERNS). The coordinator's acceptance text is the PR comment at https://github.com/Joshua-Asante/first-passage/pull/554#issuecomment-5906152141. Its stated conditions: Codex's review of `76a80e9` found no major issues and all review threads are resolved; the required `skills (3.12)` and `pytest (3.11)` are green on `cc08f05`. The executor checked those against GitHub before recording this line. One caveat is not in the executor's control: the `qualification-windows` check was still running when the coordinator wrote the comment, and was still pending when the executor read it. The disclosed baseline limitation (`test_qualification_isolation`) is unchanged. **Not established by this acceptance:** the real broker evidence producer and route recovery (T09); the durable resume owner (T13); live notification; X-1, S5 and commissioning; any operational GO. The merge is Joshua's.

## §8 — Coordinator record (2026-09-29)

**Coordinator.** The "Coordinate parallel sessions" Claude Code session holds the deployment-coordinator role for CC-3. Joshua assigned it in session on 2026-09-29. The assignment covers CC-3 only and moves no other coordinator work.

**What happened, in order (not backdated).**
1. Codex prepared this card on 2026-09-29 in `C:/Users/joshu/.codex/worktrees/x1-cc3-packets/multi_firm_operations`. It was staged there, uncommitted, at base `1ca4233` (card SHA-256 `3cda0545…695b1`).
2. Joshua pasted the card into a Claude Code session on branch `claude/cc3-ordinary-unknown-outcome-36ba29`, a checkout at `1ca4233` (`C:\Users\joshu\multi_firm_operations\.claude\worktrees\pr-363-babysit-671b91`).
3. That session implemented the repair between about 16:01 and 16:13 UTC. Its first launcher record is `20260929T160142Z`. No committed card revision or coordinator dispatch existed at the time, although this card's Authority line and §10 require both before implementation.
4. Codex reviewed the returns twice at Joshua's request and did not accept them. The executor then ran `check_brief.py --type handoff` read-only against the staged card and got 0 HARD and 0 WARN. That is a draft validation of bytes `3cda0545…`.
5. On Joshua's direct grant of commit and push on its branch, the executor committed the six-file patch as `b9b72f9` and pushed it. No PR was opened.
6. The coordinator froze the card at `b77b6f4`, on top of `b9b72f9`, with bytes identical to `3cda0545…`. This record was added in the next commit.

**Disposition of the missing freeze and dispatch.** This is recorded as a **procedural deviation, not repaired by re-running**. The implementation is not repeated to reconstruct the prescribed order. §0–§6 and §10 are unchanged from the bytes the executor worked against, so `b77b6f4` is the revision the patch is reviewed against. From now on, the executor works under the grants below.

**The patch under review** is commit `b9b72f97ffc020f695e34bc9087be82836cfdcb0`, on base `1ca4233b5f486f2946b4bbad3b2d13b427370ecb`. Four files are modified and two are new; all six are within §2's footprint. The coordinator read these SHA-256 values on 2026-09-29. The working-copy column holds the bytes the records hashed. For three files the working copy is CRLF, and the committed LF blob has no other difference: `git diff` against the commit is empty, and the CR-stripped hashes match.

| File | State | Working copy | Committed blob |
|---|---|---|---|
| `ops/c1_rail/book_account_owner.py` | modified | `09e37cca…3350` | same |
| `tests/ops/test_attended_incident_rehearsal.py` | modified | `b5ae4d93…1f9e` | `eecbc4c1df36…` |
| `tests/ops/test_book_account_owner.py` | modified | `e2640331…2c67` | `b3b456034403…` |
| `docs/spec/2026-09-14-tb-s3-halt-resume-contract.md` | modified | `6e547b08…5c6b` | `4e257631e67e…` |
| `tests/ops/test_book_ordinary_unknown_halt.py` | new | `b4e90948…1143` | same |
| `docs/notes/2026-09-29-cc3-ordinary-unknown-halt-evidence.md` | new | `5212c01c…ed03` | same |

**Evidence** (launcher records in that checkout's `.cache/fp-verification/`):
- `20260929T161059Z-5ccb92360004`: the §10 related suite, 220 passed. The code-file hashes in the record match the patch.
- `20260929T170917Z-44a993effddf`: `check` on the final bytes of all six files. It completed with exit 0, stable source and complete capture.
- `20260929T160142Z-0fa5f98ce430` and `20260929T160722Z-63341ffc753d`: the runs against the unrepaired code. They fail as the card predicts.
- **Coverage gaps:** `test_halt_storage_failure_stops_remaining_cancel_targets` and `test_protection_unknown_keeps_only_its_own_incident` were added after the unrepaired-code run. They have no evidence of failing on the unrepaired code. `check_brief` has not yet been run against the frozen revision.

**The coordinator's specification read.** This is not acceptance; that review follows the PR.
- All eight cases named in §6 exist in the new module.
- The production change stays in `_dispatch_action_locked`. An unknown result commits the attempt observation and `_halt_db("ordinary-unknown:<attempt_id>", "execution")` in one transaction, before any attached fact is observed. Accepted and rejected results keep their existing path.
- No schema, policy or interface change was found.

**Consequences recorded for review (they add no gate).**
- **Scheduled exits:** after an unknown cutoff cancel or scheduled flatten, the account halts to INTERVENTION. Later automatic deadline sends are suppressed, and operator intervention is required. This follows §0.5(A) and matches how the protection path already treats an unknown result. The coordinator found no conflict with owner text, so no decision question is raised. No deadline exception or resume route was added.
- **Changed expectation:** `test_ambiguous_cutoff_cancel_is_retained_and_deadline_revokes_all_sends` now expects a single `execution` incident at the cutoff, where it previously expected a later `schedule` incident. Its no-send and reservation assertions are unchanged.

**Dispatch grant (from this record forward).**

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push, pr.open]
constraints:
  - no_main_write
  - no_merge
  - section_2_footprint_plus_amendments_1_3
  - no_qualification_or_s5_file
  - no_schema_policy_or_interface_change
  - no_rail_deploy
  - no_rail_arm
  - no_account_traffic
  - no_broker_or_vendor_contact
  - no_external_send
  - no_private_source_read
  - no_resend_timeout_closure_or_auto_recovery
  - windows_ack_defect_preserved_not_fixed
  - no_owner_record_edit
acceptance:
  - tests/ops/test_book_ordinary_unknown_halt.py::test_unknown_result_halts_before_return
  - tests/ops/test_book_ordinary_unknown_halt.py::test_send_exception_halts_and_retains_attempt
  - tests/ops/test_book_ordinary_unknown_halt.py::test_terminal_or_fill_after_unknown_never_resumes
  - tests/ops/test_book_ordinary_unknown_halt.py::test_unknown_halt_survives_restart_and_duplicate_occurrence
  - tests/ops/test_book_ordinary_unknown_halt.py::test_concurrent_dispatch_serializes_behind_unknown_halt
  - tests/ops/test_book_ordinary_unknown_halt.py::test_unknown_halts_remaining_cancel_targets
  - tests/ops/test_book_ordinary_unknown_halt.py::test_accepted_rejected_and_refused_do_not_gain_unknown_incident
  - tests/ops/test_book_ordinary_unknown_halt.py::test_halt_storage_failure_suppresses_further_dispatch
  - tests/ops/test_attended_incident_rehearsal.py::test_lost_entry_response_terminal_does_not_restart_automation_in_session
  - tests/ops/test_book_account_owner.py::test_crash_cuts_retain_obligation_and_never_retry_on_boot
  - tests/ops/test_book_ordinary_unknown_halt.py::test_attached_fact_failure_rolls_back_halt_and_facts_together
  - tests/ops/test_book_ordinary_unknown_halt.py::test_unknown_with_attached_fill_commits_capacity_and_halt_together
```

**The executor (the CC-3 session) may:**
1. Fast-forward its branch to this record's commit (`git merge --ff-only claude/cc3-card-freeze`). This is possible because the record sits directly on `b9b72f9`.
2. Run `check_brief.py --type handoff` on this card at that revision.
3. Complete §7's return against the frozen revision, which is this card's only other permitted edit. It does not repeat the unchanged code-test runs.
4. Push `claude/cc3-ordinary-unknown-outcome-36ba29` and open a PR against `main`.

Any change to the six patch files, or any necessary change outside §2's footprint, returns NEEDS_CONTEXT.

**Review and acceptance.** The coordinator reviews the PR for specification compliance, then implementation quality and the composed path, as set out in §7. Codex PR review serves as the independent review (D-codex hybrid). The coordinator may mark CC-3 RESOLVED **in synthetic scope only** after that review and a passing required check, with a note in §7. Joshua retains the merge.

**Not granted.** No synthetic acceptance or RESOLVED status before that review. No real broker evidence producer, route recovery, T09 work, resume design, live notification, X-1, S5, commissioning action, merge or operational GO.

### §8.1 — Coordinator amendment 1 (2026-09-29; confirmed by Joshua in session)

**Why.** Codex's review of `ec96a0e` returned two P1 findings, and the coordinator accepts both ([#554 response](https://github.com/Joshua-Asante/first-passage/pull/554#issuecomment-5897487491)). The coordinator's earlier "no blocking findings" review is withdrawn. Joshua confirmed this amendment in the coordinating session on 2026-09-29 ("I confirm the amendment").

**(1) Attached facts commit with the halt (a production fix, in `book_account_owner.py`).**
- **The defect.** `b9b72f9` commits the halt before any attached fact is journaled. A crash between the two therefore loses the fact bodies and their capacity effects, while the observation still lists their IDs. That is §4's falsifier "discarded valid evidence". The ordering was an implementation choice and was not required by this card, since §2.3 requires facts to be preserved.
- **The fix.** In the unknown branch of `_dispatch_action_locked`, one transaction runs `_settle_attempt_db`, then `_halt_db("ordinary-unknown:<attempt_id>", "execution", now)`, then `_observe_locked(fact, …, db=db)` for each attached fact.
- **On failure.** Any exception in that transaction sets `_input_send_suppressed` before it re-raises.
- **What the executor confirms.** Given `db`, `_observe_locked` opens no transaction of its own.
- **New acceptance cases** (added to the authority block):
  - `test_attached_fact_failure_rolls_back_halt_and_facts_together`: an unknown result with an attached fill, where the fact observation fails partway. There is no incident, no fact and no capacity event; the attempt is `UNKNOWN` with a null observation; later sends are suppressed; and a fresh boot is `HALTED/INTERVENTION`, retains the attempt and sends nothing.
  - `test_unknown_with_attached_fill_commits_capacity_and_halt_together`: the fill's capacity effect and the halt persist together.

**(2) Superseded unknown-continuity tests (test-only).** The footprint widens to these seven files in `tests/ops/`:
- `test_book_close_reconciliation.py`
- `test_book_fence_classification.py`
- `test_book_takeover_phases.py`
- `test_pr409_owner_lifecycle.py`
- `test_pr409_related_cases.py`
- `test_pr409_review3.py`
- `test_pr409_review4.py`

They encode the continuity rule that halt/resume §2 and incident ADR §A11.2 supersede: an unknown blocks until a postdating terminal arrives, and then automatic sends resume. These rules apply:
1. Only the authority expectation changes: `unknown_order` becomes `intervention_fence`, and "resumes after a terminal" becomes "stays halted". Every no-send, reservation, reconciliation, late-fill-retention and restart assertion is kept.
2. A case whose purpose was "later evidence resumes automation" is rewritten to assert the fence plus the reconciliation. It is not deleted.
3. Every change is listed in one table in the evidence note: node, old expectation, new expectation, governing text.
4. Any case whose expectation cannot be expressed as (a) unknown → `INTERVENTION`, (b) no automatic send afterwards, and (c) facts still reconcile and retained obligations survive returns **NEEDS_CONTEXT for that case**. It is not resolved locally.

`test_qualification_isolation.py::test_qualification_suite_in_clean_process` is checked against `main` first. If it fails there too, it is disclosed as independent and left untouched.

**(3) Verification.** The **full `tests/ops` suite** through the launcher is now an acceptance criterion, in addition to §10's list. §10's related list was incomplete: it omitted these seven files. The 220-pass record on that list does not stand in for the full suite. The retained evidence is:
- a completed, stable-source launcher record for full `tests/ops` on the final head;
- `check` on the final bytes.

**(4) Mechanics.**
1. Fast-forward to this amendment's commit (`git merge --ff-only origin/claude/cc3-amendment-1`).
2. Merge `main` into the branch, without rebasing, so the freeze commit `b77b6f4` keeps its SHA.
3. Include the pending docs-only evidence-note correction: label the opening NEEDS_CONTEXT as historical, drop "passes on both", and add the `170917` and `174520` check rows.
4. Push, reply on both Codex threads, and re-request `@codex review`.

**Authority block.** It is updated in place by this amendment:
- The constraint `section_2_footprint_only` became `section_2_footprint_plus_amendment_1_test_files_only`.
- The two acceptance cases above were added.

Nothing else in it changed.

**Acceptance.** RESOLVED, in synthetic scope only, requires all of the following: both Codex threads resolved, green `pytest (3.11)` and `skills (3.12)`, the full `tests/ops` record, and the coordinator's review of the new diff. The merge stays Joshua's. No other grant changes.

### §8.2 — Coordinator amendment 2 (2026-09-29; recorded by the executor at the coordinator's direction)

**Provenance.** The coordinator ruled on the executor's NEEDS_CONTEXT return by cross-session message on 2026-09-29, and directed the executor to record the ruling here in its own commit. Joshua's confirmation of amendment 1 is recorded in §8.1. This section records no separate confirmation from Joshua for amendment 2.

**Why.** Eight test nodes hit an *implicit* unknown outcome through `SyntheticBroker`'s empty-queue default (`book_account_owner.py:227`, which returns `BrokerResult("unknown")` when no result is queued). They never meant to test an unknown, and the repaired owner now halts on it. With that default temporarily flipped to `accepted`, all 12 parameterized nodes passed. The coordinator accepted the diagnosis.

**Ruling.**
1. **Fixture-queue changes are allowed (test-only).** For each of the 8 nodes, queue explicit `BrokerResult("accepted")` for every send the test did not mean to be unknown, and keep every existing assertion. For `test_async_cancel_terminal_resolves_control_attempt[unknown]` the entry is accepted and the cancel is unknown, and the expected authority becomes `INTERVENTION` (was `SCHEDULED_EXIT`), following halt/resume §2 and incident ADR §A11.2. Its reconciliation assertions stay.
2. **`tests/ops/test_pr409_review2.py` is admitted**, test-only, for `test_definitive_rejection_releases_only_its_own_reservation[cancel]` only, under the same rules.
3. **Rejected: changing `SyntheticBroker`'s empty-queue default.** Returning `unknown` for an empty queue is the fail-safe choice for a test double, and changing it is a production-file edit outside the footprint. It stays as it is.
4. **The per-change table.** Each of the 8 nodes gets its own row in the evidence note's per-change table, with the cause marked "implicit unknown via empty queue; fixture made explicit".

**The eight nodes:** `test_book_takeover_phases.py::test_producer_cancel_removes_remainder_and_retains_late_fill`; `test_pr409_owner_lifecycle.py::test_scheduled_close_survives_ticks_and_partial_terminal`, `::test_invalid_cancel_target_never_sends[other-leg]`, `::test_invalid_cancel_target_never_sends[close]`, `::test_async_cancel_terminal_resolves_control_attempt[unknown]`, `::test_scheduled_flatten_handles_late_entry_fill`; `test_pr409_review3.py::test_cutoff_retires_takeover_before_displaced_terminal`; `test_pr409_review2.py::test_definitive_rejection_releases_only_its_own_reservation[cancel]`.

**Qualification isolation.** `test_qualification_isolation.py::test_qualification_suite_in_clean_process` is baselined on a clean `main` worktree and the result is disclosed. If it times out there too, it is independent of this PR. It stays untouched either way. The acceptance record is a full `tests/ops` run made without other load on the machine.

**Authority block.** Its shape is unchanged. The constraint `section_2_footprint_plus_amendment_1_test_files_only` became `section_2_footprint_plus_amendment_1_2_test_files_only`, which adds `tests/ops/test_pr409_review2.py` beside the seven files of §8.1.

**Sequence and ownership.** The executor then adds the evidence-note fix and the per-change table, runs the full `tests/ops` record on the final head and `check`, pushes, and sends the head and record paths to the coordinator. The coordinator replies on both Codex threads and re-requests `@codex review` after the push. No other grant changes.

### §8.3 — Coordinator amendment 3 (2026-09-30; recorded by the executor at the coordinator's direction)

**Provenance.** The coordinator ruled on the executor's NEEDS_CONTEXT return by cross-session message on 2026-09-30, and directed the executor to record the ruling here in its own commit. The coordinator's message says Joshua is being told that the coordinator admitted the file below, and that it will tell the executor before a push if he overrules it. This section records no confirmation from Joshua for amendment 3.

**Why.** Codex's P2 on merge head `84a2a78` (thread `PRRT_kwDOT46Eac6nXbfX`, `book_account_owner.py:1889`): for a takeover-generated cancel or flat that returns unknown, the CC-3 halt records `ordinary-unknown:<attempt_id>`, and `_advance_takeover_locked` then records `takeover-child:<operation_id>` for the same outcome. That contradicts §3 row 1 ("one durable incident") and §0.5(D) (no duplicate incident where another path already halts). The coordinator accepted the finding.

**The executor's read-only probe** (throwaway test on `84a2a78`, deleted; `TakeoverScenario`, the child's result forced to each outcome):
- **Unknown:** generation 1 → 3, two incidents (`ordinary-unknown:<attempt>`, then `takeover-child:control:<operation>`), and two `HALT` events on plan `entry:aegis_6j` (generations 2 and 3). Exposure stays `(1, 1)`.
- **Rejected:** generation 1 → 2, one incident (`takeover-child` only), one `HALT` event. No CC-3 halt exists on that path, so it must not change.
- **Precondition confirmed:** `_halt_db` already writes the takeover plans' `HALT` events when it inserts the `ordinary-unknown` incident (it skips only plans in phase `ATTEMPTED` or `RETIRED`; this plan was in `CONFIRM_CANCELLATIONS`). The later `takeover-child` halt therefore adds, for an unknown, only a second incident, generation and `HALT` event.

**Ruling.**
1. **Keep the CC-3 halt; consolidate the takeover one.** The `ordinary-unknown` incident is committed atomically inside the dispatch serializer before anything else runs; moving ownership back to the takeover halt would reopen the timing gap CC-3 closed.
2. **The footprint extension: `ops/c1_rail/book_takeover_owner.py`, one hunk only,** the tail of `_advance_takeover_locked` (around lines 536–542). Inside the existing transaction, the `_halt_db('takeover-child:' + result.operation_id, ...)` call is skipped only when all three hold: `result.transport_state == 'unknown'`; `result.attempt_id` is set; and `SELECT 1 FROM incidents WHERE incident_id = 'ordinary-unknown:' || attempt_id` finds a row. The `break` stays. The `rejected` path is byte-for-byte unchanged. One comment cites §8.3 and "one durable incident". No other edit to that file.
3. **Rejected alternative:** changing `_halt_db` in `book_account_owner.py` to swallow `takeover-child:` ids. Takeover-specific logic in the shared halt owner could hide a genuinely distinct second incident.
4. **Tests** (in the admitted `test_book_takeover_phases.py`): the strengthened `test_cancel_failure_fences_and_retains_exposure[unknown]` and a new `test_flat_failure_fences_and_retains_exposure[unknown]` (a takeover-generated flat), each asserting exactly one incident `ordinary-unknown:<attempt_id>`, one generation step 1 → 2, exactly one plan `HALT` event, and exposure retained. Both fail on `84a2a78` and pass with the hunk. The `rejected` variants assert the unchanged behavior (one `takeover-child` incident, one generation step, one `HALT` event) and pass before and after.

**Authority block.** Its shape is unchanged. The constraint `section_2_footprint_plus_amendment_1_2_test_files_only` became `section_2_footprint_plus_amendments_1_3`, which now means: the production files `ops/c1_rail/book_account_owner.py` and `ops/c1_rail/book_takeover_owner.py` (that one hunk only), plus the test files admitted by §8.1 and §8.2 and `tests/ops/test_book_takeover_phases.py`.

**Sequence and ownership.** The executor then runs the related suite, the full `tests/ops` (with the machine load disclosed), and `check`, all through the launcher, pushes as a fast-forward, and sends the coordinator the head and record paths. The coordinator handles the Codex thread and re-request. No merge, no RESOLVED, and no other grant changes.

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
