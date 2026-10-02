# CC handoff — T00 step-1b Tasks 3–4: retained source pack and P7 verification

**Date:** 2026-09-30.
**Status:** DISPATCHED to one local Claude Code session (Opus, high effort) by the coordinating session. Task 3 stops at the operator-signature checkpoint. Task 4 continues only after the operator has signed.
**Parent session:** "Coordinating parallel Claude sessions" (coordinator for this dispatch; Joshua assigned the coordinating role in session on 2026-09-29).
**Spawn target:** a local Claude Code session with an isolated worktree on branch `claude/t00-p7-tasks-3-4`, plus read access to the primary checkout's ignored private inputs.
**Brief type:** CC handoff, bounded continuation of an authorized packet.
**Parent question:** T00 step 1b (candidate 3′ P7 closure) under the [P7-closure packet](2026-09-24-tradeify-t00-p7-closure.md). The route is the operator's 2026-09-29 "option 1" ruling ([T00 §7.9](2026-09-22-tradeify-t00-step1-producer-inventory.md#79-recovery-accepted-shortest-path-continuation-2026-09-24)): T00's own Task 3 produces P7 (b).
**Authority:** the P7-closure packet's §7 "Authorized continuation boundary" authorizes Tasks 2–4 under that packet. Task 2 is complete on this branch's base (`672d49f`, packet §7 "Task 2 return"). Joshua asked the coordinator on 2026-09-30 to hand Tasks 3–4 to a local session. This card only binds that dispatch and adds nothing to the packet's authority.

**Selected outcome:** P7 scored honestly for candidate 3′. Either `DONE` (P7 MET under packet §4), or a precise non-MET verdict with its evidence.
**Prerequisites:**
- Task 2 is in place at `672d49f`.
- The packet §0.1 private bytes are reverified before the first write.
- The operator signs the Task 3 OPERATOR contract before Task 4 starts.
- S5 is not a prerequisite. See the merge hold under §5.
**Ownership:** one executor owns Tasks 3–4 and the private source pack. The coordinator reviews the canonical contract bytes before the signature and reviews the return. Joshua signs the contract and retains merges. The coordinator, not the executor, updates the parent T00 verdict.
**Verification:** packet §5 in full: launcher records, private-byte hashes (no contents), real-path R1/R2 evidence digest, hand-recompute equality labels, a separate-session refute-first review, and no private byte in Git.
**Checkpoint:** (1) after the §0 reads and the §0.1 reverification; (2) at the Task 3 signature checkpoint (stop and return); (3) at final P7 scoring.
**Return boundary:** packet §6's taxonomy, with the return recorded in packet §7. No T00 step 2, screen or MC.

## §0 — Production reads

Starting source for this dispatch: `claude/t00-p7-tasks-3-4` at the commit that adds this card, whose parent is `672d49f`. Read, and record `git log -1 --format='%h %as' -- <path>` for each:
- the [P7-closure packet](2026-09-24-tradeify-t00-p7-closure.md) in full, especially §0–§0.6, §2, §3 Tasks 3–4, §4–§6, §7 "Task 1 checkpoint" and §7 "Task 2 return";
- [T00 step-1 packet §7.9](2026-09-22-tradeify-t00-step1-producer-inventory.md#79-recovery-accepted-shortest-path-continuation-2026-09-24), for the route ruling;
- every owner and production file listed in packet §0, at this branch's head, at least:
  - `ops/c1_rail/qualification/production_source.py`
  - `ops/c1_rail/qualification/replay.py`
  - `ops/c1_rail/qualification/model.py`
  - `ops/c1_rail/book_policy.py`
  - `core/dd_protection.py` (Rule-0 cross-check only; never edited)
  - `ops/c1_signal_daemon/book_adapters.py`
  - `docs/briefs/handoffs/2026-09-21-tradeify-t10-source-and-freeze-packet.md`
  - `docs/notes/2026-09-21-t10-phase1-source-reconciliation.md`
  - `docs/load_bearing_numbers.md`

The exact `ProductionSource.build` required-role set is in `production_source.py`; packet §0 cites it at lines 777–778 at an earlier head, so re-read it here. Also read the T10 phase-1 source reconciliation note for R1 reading (a) and R2 panel-derived, because the shared session-index producer must match T10 by exact identity.

## §0.5 — Clarifications and recommended defaults

(A) **Private output root:** packet §0.5 item 3: `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/t00-p7-closure-2026-09-24/`, **in the primary checkout** (`C:/Users/joshu/multi_firm_operations/…`), addressed by absolute path. Never write private bytes inside your worktree: they would be deleted with it. If a harness hook refuses a write there, stop and return the refusal. Do not route around the guard.
(B) **Private inputs** are read in place in the primary checkout (the AGENTS.md private read surface). Use `FP_PORT_ROOT` for the corrected ports root. Never copy Pine or ports into the worktree, commit them, quote them, or send them to GLM or any external service.
(C) **Shared producer:** the session-index producer is built once and shared with T10 by exact identity (T00 §7.9). Record its identity so T10 can bind to the same bytes.
(D) **Signature checkpoint:** Task 3 ends by assembling the successor OPERATOR contract's canonical bytes. Stop and return their SHA-256 and inventory. The coordinator reviews the bytes, and Joshua signs through the existing detached-approval ceremony. No agent signs, and no test key substitutes.
(E) **Carry-forward items from the Task 2 return,** to settle in Tasks 3–4:
- the run-local provider ignores reviewed intrabar rows, so Task 3's `schedule_execution_evidence` schema decides this;
- `replay_bracket` records a run's `ReplayDeadlineFailure` as that run's result, which is a Task 4 review item.
A contradicted default or a missing fact returns `NEEDS_CONTEXT`.

## §0.75 — Local dependency check

- **Vendor data:** the four M15 panels in `core/data/bar_data/` in the primary checkout, verified against `SHA256SUMS` before use. The panels are absent from worktrees.
- **Credentials:** none. The OPERATOR signature is the operator's act.
- **Pine/runtime ports:** the accepted ports, read in place under the private read surface, plus the corrected Striker bytes `efd479b6…` in the approved staging root (packet §7, Task 1).
- **Confirmed-present check:** run packet §0.1's reverification this session, before any write. The dispatch observations are not acceptance.

## §1 — Context

- **Task 2** delivered the frozen bracket interface: `ScheduleExecutionBracket.for_run`, `ScheduleSplit`, `replay_bracket`, exposure capture that enforces the reservation invariant, and ported consumers with byte-identical benchmark output. Evidence is in packet §7, "Task 2 return".
- **P7 (a)** (private inputs match their pins) was MET on 2026-09-24.
- **P7 (b)**, the eight reviewed retained roles, does not exist yet. Producing it is Task 3.

## §2 — Execution steps and allowed files

- [ ] 2.1 Run `./fp.ps1 doctor`, do the §0 reads, and run the §0.1 reverification. Return at once on any mismatch.
- [ ] 2.2 **Task 3:** produce the eight roles under the private root, as packet §3 Task 3 specifies, each bound by exact path and SHA-256. Each review companion is its own artifact.
- [ ] 2.3 Assemble the successor OPERATOR contract's canonical bytes and validate them through the existing parsers. **Stop and return** the contract SHA-256, the role → digest inventory and the parser results. Wait for the coordinator's review and the operator's signature.
- [ ] 2.4 **Task 4,** after signing: packet §3 Task 4 in full. That covers bindings by exact identity, `ProductionSource.build`, and `replay_bracket` on a real retained path with at least one consumed intrabar split. It also covers the independent one-day hand recompute of R1 and R2, `intraday_low` checks, a separate-session refute-first review, and focused re-review of any fixes.
- [ ] 2.5 Run packet §5 verification, then record the return in packet §7.

**Tracked files allowed:** exactly packet §3's list:
- `production_source.py`, `replay.py`, and `model.py` for immutable types only;
- `test_production_source.py`, `test_replay.py`, `test_runner.py` (wiring only), `tests/ops/test_book_adapters_parity.py`;
- the packet's §7.

**Also allowed:** this card, only to record status lines. Private artifacts are never tracked.

## §3 — State and interface contract

| Event | Required outcome |
|---|---|
| A §0.1 byte mismatches | Stop; `NEEDS_CONTEXT` with the path and both hashes |
| A source date cannot be qualified | An explicit `UNKNOWN_SOURCE_DATE` / coverage gap. No extrapolation, no guessed closure |
| The contract is assembled | Stop at the signature checkpoint. Nothing downstream runs unsigned |
| Replay on a real path | R1 and R2 each from a fresh engine. Each run's own P&L/low pair is emitted and never combined |
| The hand recompute differs | P7 NOT MET, with the differing field named |
| Output | Private values stay private. The public return carries hashes, counts and equality/verdict labels only |

## §4 — Hypothesis and falsifier

**H:** packet §4's H. **Falsifier:** packet §4's FALSIFIED list, applied mechanically. No GO-evidence or NO-GO-evidence verdict is produced.

## §5 — Constraints

- Everything in packet §6 "Forbidden" applies, including no T00 step 2, no screen or MC, no change to the 1%/0.40 policy, no edit to `core/dd_protection.py`, no agent signing, no provider, account or broker action, and no publishing of private bytes.
- **Merge hold:** this branch and its parent `claude/t00-task2-bracket` stay unmerged until S5 has merged (S5's Stage 1c-measured closure imports `production_source`, `replay` and `model`). Do not open a PR. Pushing the branch is allowed.
- Do not merge `main` into this branch without the coordinator's instruction.
- If a hook or guard refuses an action, raise it; don't work around it.
- Commit and push only on `claude/t00-p7-tasks-3-4`. Merges are Joshua's.

## §6 — Acceptance and return taxonomy

Acceptance is packet §4's RESOLVED condition with all of packet §5's evidence. Named acceptance cases:
- the existing Task 2 cases stay green;
- Task 4's real-path replay with a consumed intrabar split;
- the hand-recompute equality for R1 and R2;
- the `intraday_low` horizon, sign and pairing checks.

Return exactly one status:
- DONE: P7 MET, with all evidence.
- DONE_WITH_CONCERNS: the bounded work is complete and a named non-P7 concern remains, with P7 scored honestly.
- NEEDS_CONTEXT: a missing identity, source fact, ruling or signature. Name it.
- BLOCKED: context-problem, capability-problem, scope-problem or plan-itself-wrong, with the exact obstruction.

A failed required acceptance criterion is not DONE_WITH_CONCERNS.

## §7 — Coordinator acceptance / executor return

Awaiting the executor. Checkpoint returns go to the coordinator session; the final return goes in packet §7.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - no_main_write
  - no_merge
  - no_pr_until_s5_merged
  - packet_section_3_plus_amendment_2_files
  - private_bytes_primary_checkout_root_only
  - no_private_bytes_in_git
  - no_agent_signature
  - no_t00_step2_screen_or_mc
  - no_policy_or_sizing_change
  - no_dd_protection_edit
  - no_rail_deploy
  - no_rail_arm
  - no_account_traffic
  - no_broker_or_vendor_contact
  - no_external_send
  - no_glm_for_private_inputs
acceptance:
  - tests/ops/qualification/test_production_source.py::test_t2_item7_replay_bracket_builds_two_fresh_engines_with_separate_results
  - tests/ops/qualification/test_replay.py::test_t2_item6_reservation_order_sum_mismatch_is_refused_before_any_split
  - tests/ops/qualification/test_replay.py::test_t2_item3_r2_pending_only_cancels_before_gap_open_fill_on_ordinary_bar
  - tests/ops/test_book_adapters_parity.py
```

## §8 — Amendments

### §8.1 — Coordinator sequencing after the Checkpoint 1 return (2026-09-30)

*Recorded by the executor at the coordinator's direction.* At Checkpoint 1 the executor returned `NEEDS_CONTEXT` on two blockers:
- the only OPERATOR contract the code accepts is the full F1 qualification contract;
- no accepted fact supplies historical venue deadlines.

Joshua ruled on both on 2026-09-30. The rulings are recorded verbatim in the [P7-closure packet §7](2026-09-24-tradeify-t00-p7-closure.md#operator-rulings-2026-09-30). This amendment sequences the work that follows:

1. **Phase A, design only, with no code.** Write `docs/superpowers/specs/2026-09-30-t00-source-only-contract-design.md`. It is a behavioral contract for a separately signed source-only contract that `ProductionSource.build` accepts. It covers:
   - the schema and canonical bytes;
   - a signing scope and approval name distinct from the qualification approval;
   - the trust-domain binding and key-class separation;
   - the exact role set;
   - what `build` does and what it refuses (no stages, budget, decision rules or screen);
   - the labelling of P7 evidence produced under it;
   - the files it would touch, plus a state/event table;
   - named acceptance tests with falsifiers.

   Then stop and return the spec's path and SHA-256. The coordinator reviews it, Codex reviews it, and Joshua accepts it. Implementation files are admitted only by a later amendment.
2. **Task 3 source pack, in parallel with the design review.** Produce the eight role artifacts under the approved private root, applying the deadline ruling, each bound by path and SHA-256. Stop before assembling any contract.
3. **Wait for the accepted design.** Signing, implementation and Task 4 all wait for it.

**Allowed now:** the design spec file, this §8.1 and packet §7. Private writes go only to the approved root. No production or test code edits yet.

### §8.2 — Amendment 2: implementation files admitted (2026-09-30)

*Recorded by the executor at the coordinator's direction.*

**Basis.** Joshua accepted the [source-only contract design](../../superpowers/specs/2026-09-30-t00-source-only-contract-design.md) ("option 1") at revision 4.2: commit `3543b24`, spec SHA-256 `7f80277cc1576920f0fc863bd071834ff7687654673504a76d4087113eb2b794`. That spec is the frozen contract for the implementation, and any change to it needs a new operator acceptance.

**Admitted files.** These are exactly spec §4, plus test homes for A13–A23.
- **Production:**
  - `ops/c1_rail/qualification/contract.py`
  - `ops/c1_rail/qualification/trust_domain.py`
  - `ops/c1_signal_daemon/book_adapters.py` (the `_source_domain` / `_resolve_domain` additions only)
  - `ops/c1_rail/qualification/production_source.py`
  - `ops/c1_rail/qualification/clock.py` (`SOURCE_TRUNCATED` only)
  - `ops/c1_rail/qualification/p7_evidence.py` (new)
  - `ops/c1_rail/qualification/p7_driver.py` (new)
- **Tests:**
  - `tests/ops/qualification/test_source_contract.py` (new)
  - `tests/ops/qualification/test_source_consumers.py` (new)
  - `tests/ops/qualification/test_p7_evidence.py` (new; A16–A23)
  - `tests/ops/qualification/test_production_source.py`, `test_contract.py`, `test_trust_domain.py` and `test_clock.py` (A13/A18)
- **Records:** this card's §7/§8, the P7-closure packet §7, and the spec's **status lines only**.

**Still forbidden:** `runner.py`, `replay.py`, `model.py`, `book_policy.py`, `core/`, policy files and every other file.

**Spec inconsistency.** Spec §4's `production_source.py` row still names "the inner-result registry", which revision 4 removed (§2.6c). Revision 4 governs, so no registry is built. The §4 row gets a dated status note, not a design change.

**Rules:**
1. **Fail-first.** The A-tests are authored first and recorded failing on `3543b24`'s production code through the launcher; the implementation follows. They include A6b, A21, A22 (with a no-launch spy) and A23 (with a live control).
2. **`SOURCE_SIGNING_KEYS` ships empty.** No agent enrolls a key. Test keys exist only inside the test process.
3. **Verification.** Run the new and affected modules, the full `tests/ops/qualification` suite, `tests/ops/test_book_adapters_parity.py` and `check`, all through the launcher. Report every skip and failure, and show any pre-existing failure against the base.
4. **Return after green.** Push, then return the head, the red and green records, and a test → A-ID table. Codex reviews the code next. The r3 pack, the coordinator's reviewer companions, the operator's key-enrollment PR and the operator's signature come after that code review.
5. **Merge hold.** No PR until S5 merges, then rebase and re-verify. Do not merge `main` without the coordinator's instruction.

## §10 — Audit hooks

Run from the checkout under test:

```powershell
.\fp.ps1 doctor
.\fp.ps1 python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-09-30-t00-p7-tasks-3-4-dispatch.md
.\fp.ps1 --workers 2 python -m pytest tests/ops/qualification/test_production_source.py tests/ops/qualification/test_replay.py tests/ops/qualification/test_runner.py tests/ops/qualification/test_panel.py tests/ops/qualification/test_cost_schedule_validation.py tests/ops/test_book_adapters_parity.py -q
.\fp.ps1 check
git diff --check
git ls-files --others --exclude-standard
```

Report every failure, skip and pre-existing gate failure plainly. Never describe a run with a failure as passing.
