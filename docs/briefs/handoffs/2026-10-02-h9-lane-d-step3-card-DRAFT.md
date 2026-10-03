# H9 lane D step 3: term 8 joint-batch validators, result-role funding, TEST_ONLY result faults, qseal and dedicated result_g5 provisioning (Codex lane)

**Type:** cc_handoff (worker build card)

**Status:** DRAFT — freezes when the step-2 head is RESOLVED and #614 is merged. It has not been dispatched. Operator ruling D3 and the coordinator (3) resolutions of D1, D2, D5, D6 and D8 (2026-10-02) are applied below (§12). At freeze the coordinator fills the OWED items in §12, re-anchors every code line on the D1 base, commits the frozen revision under the committed-handoff rule and records its SHA in the ledger before any worker starts.

**Citation basis (re-verified 2026-10-02).** Code lines are at `f237178` (`origin/codex/h9-t05-integration`, still that branch's head). Repository documents are at `origin/main` `d716106`. The #614 card is at PR head `2416bf0`; its bytes are unchanged from `7b2d74e`. Step 2 edits the same code files, so every code line number moves; they are **OWED** re-anchoring on the D1 base at freeze.

**Executor:** the H9 Codex executor, routed through the Codex coordinator. It continues on the H9 identity branch after step 2 and is the single writer (#614 card `2416bf0:docs/briefs/handoffs/2026-10-02-h9-cprime-runtime-identity-build-DRAFT.md:250`, D7: "after step 2, on the same branch, under its own separately frozen step-3 card").

**Coordinator:** the deployment coordinator, "Coordinating parallel Claude sessions (3)". New tasks belong to coordinator (3) under Joshua's split. It owns the freeze, the diff review, integration, every Linux dispatch, the Codex relay, PRs and the ledger.

**Owners this card narrows (it changes none of them):**
- S6 freeze amendment **term 8** (operator ruling 2026-10-02, "yes to … term 8"; record merged in #610, `f8a03c2`): `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md:693`. The owed fix is stated at `:2116`.
- The step-3 scope fixed at the step-2 freeze: #614 card `:216-225` (§11) and `:250` (D7), plus the Phase-0 dispositions `:251-258` (`result_g5` and qseal are not provisioned under step 2; both are owed before R1).
- T05 seam table, rows 6a, 11, 11a, 20 and 21: ledger `:707`. Seam edits: T05 handoff `docs/briefs/handoffs/2026-09-21-full-e1-t05-result-and-seal.md:61`. F3 progression names: `:32`. F4 isolated charged processes: `:34`.
- H9 checkpoint R1 and its limits: `docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md:528-585`.
- Campaign spec E03: `docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md:212`.
- The R1 tooling card (selector, workflow mode, reader, guard): `docs/briefs/handoffs/2026-10-02-r1-tooling-build-card.md` on branch `claude/r1-tooling`. As of 2026-10-02 it is uncommitted in its worktree and the branch is not pushed. It assigns the `FP_QUALIFICATION_R1` fixture seam and the node registration to H9 (its `:77`, `:141`, `:225`).

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - no_main_write
  - no_merge
  - no_pr_open
  - no_linux_or_ci_dispatch
  - no_ci_configuration_change
  - identity_branch_only
  - card_section2_files_only
  - no_t00_p7_closure_edit
  - no_stage1c_measured_closure_edit_without_checkpoint
  - measured_closure_edits_d3_admitted_only
  - no_frozen_wire_family_or_db10_change
  - no_budget_deadline_or_allowance_change
  - no_new_key_policy
  - no_route_enabling_release_literal
  - no_private_bytes_committed
  - no_r1_selector_or_workflow_edit
  - single_writer
  - stop_at_coordinator_return
acceptance:
  - tests/ops/qualification/execution/test_result_joint_batch_prefixes.py
  - tests/ops/qualification/execution/test_result_role_funding.py
  - tests/ops/qualification/execution/test_result_seal_faults.py
  - tests/ops/qualification/execution/test_result_seal_provisioning.py
  - tests/ops/qualification/execution/test_campaign_result_commit.py
  - tests/ops/qualification/execution/test_campaign_result_layout.py
  - tests/ops/qualification/execution/test_campaign_seal.py
  - tests/ops/qualification/execution/test_result_seal_guardian_loop.py
  - tests/ops/qualification/execution/test_campaign_funding.py
  - tests/ops/qualification/execution/test_campaign_scheduler.py
  - tests/ops/qualification/execution/test_campaign_supervision.py
  - tests/ops/qualification/execution/test_campaign_cancellation.py
  - tests/ops/qualification/execution/test_protocol.py
  - tests/ops/qualification/execution/test_runtime_identity_pin.py
  - tests/ops/qualification/execution/test_runtime_identity_launch.py
  - tests/ops/qualification/execution/test_runtime_identity_rechecks.py
  - tests/test_qualification_campaign_host.py
  - tests/test_qualification_container_ownership.py
  - tests/test_qualification_host.py
  - tests/test_qualification_invariant_manifest.py
```

The four `test_result_*` files whose names are not in the base are new. Their names are proposed and fixed at D4. Step 2's three `test_runtime_identity_*.py` files (#614 card `:38-40`) are in the set under D8 and are extended in place. Two Linux files are extended here and **collected only**; they run only inside R1 (§9): `tests/integration/qualification_boundary/test_campaign_result_seal_linux.py` (`f237178`, 230 lines, 6 test functions) and step 2's `tests/integration/qualification_boundary/test_runtime_identity_linux.py` (#614 card `:52`).

## 0. Phase 0: premise, Rule-0 reads, and findings returned before any code

1. **Premise.** HEAD is the frozen base (D1): the H9 branch at the step-2 RESOLVED head, with `origin/main` merged in at build start as in step 2. On that head, record the commands below and their output:
   - `git rev-parse HEAD`, and the step-2 RESOLVED SHA it builds on;
   - `git merge-base --is-ancestor f8a03c2 HEAD`, which shows the term 8 record is in the history;
   - `git range-diff` against the step-2 head, covering the `origin/main` merge;
   - the absence of `.env` in the worktree.
2. **Rule-0 reads.** Read each of these yourself; do not rely on this summary.
   - **The three term-8 seams** (`campaign_result.py@f237178`):
     - `parse_receipt_row` `:161-201`. It requires every stage before the last to be PASS and the last stage to equal the row decision (`:188-190`). That refuses a joint N2 row of `[N2 FAIL, PART_B PASS]` and `[N2 FAIL, PART_B FAIL]`.
     - `_row_outcome` `:204-228`. It allows only `failed == [last index]` (`:226-227`).
     - `parse_campaign_result` `:298-348`. It repeats that rule (`:338-339`) and the per-checkpoint "earlier stages PASS" rule (`:341-347`).
   - **Their consumers.** All of these must hold under the fix:
     - `build_campaign_result` `:235-295` and `validate_campaign_result` `:502-570`;
     - `_result_eligibility` `:715-728` and `_result_snapshot` `:970-993`;
     - `persist_result_intent` `:1006`, `commit_campaign_result` `:1070` (reopen at `:1104`) and `result_integrity` `:1243-1265`;
     - `g5_result.validated_result_bytes_for` (`g5_result.py@f237178:78-86`, and `:171`);
     - `campaign_seal.py@f237178:314`;
     - `seal_service._require_committed_pass` (`seal_service.py@f237178:91-98`). It must keep refusing every FAIL outcome.
   - **The governing policy.** `policy.required_output_roles` (`ops/c1_rail/qualification/policy.py:144-154`, identical on `origin/main` and `f237178`) admits `stages == order[:4]` with `('COMPLETE','FAIL')` and does not look at per-stage statuses. Do not edit it: it is a measured-closure module that D3 does not admit.
   - **The existing TEST_ONLY fault mechanism.** The scheduler request field `fault` (`campaign_funding.py@f237178:59-91`) takes only `None` or `'hold_after_intent'`, and only for `n1_g5`, `n2_g5` and `part_a_g5`. The service reads it back from the persisted `full_campaign_bootstraps` request and stops after T1 (`service.py@f237178:711-727`).
   - **Funding roles.** `WORK_PHASES` (`campaign_funding.py@f237178:26-46`) has `probe_result`→RESULT and `probe_seal`→SEAL, but no `result_g5` or `seal` work role. `PROFILE` is `qualification_campaign_budget_profile/v3` (`:25`). `reserved_compute_phases` admits only `ADMISSION`, `N1`, `N2` and `PART_A` (`:169-177`). The reservations are `reserve_result_work` (`campaign_result.py@f237178:769-842`) and `reserve_seal_work` (`campaign_seal.py@f237178:146`). Settlement goes through `ResultStore._settlement_terminal` (`campaign_result.py@f237178:922-933`) and `settle_result_work` (`:935-960`).
   - **Provisioning gaps.**
     - `runtime.ENTRYPOINTS` has only `worker` and `g5` (`runtime.py@f237178:16-18`).
     - `release_schema.PROCESS_ROLES = ('supervisor','worker','g5')` (`release_schema.py@f237178:31`). `KEY_ROLES` already has `result` and `seal` (`:32`).
     - The `bootstrap.py` role whitelist has no `seal` (`deploy/qualification/bootstrap.py@f237178:15`).
     - `role_policy.ROLE_GROUPS` is qclient, qexec and qg5 only (`tools/qualification_verification/role_policy.py@f237178:6`).
     - `seal_service.exchange` refuses unconditionally (`seal_service.py@f237178:116-120`).
     - `campaign_seal.request_seal` falls back to the Windows double `qseal_sign` (`campaign_seal.py@f237178:433`).
     - The result unit is launched "exactly as the N1 G5 unit is" (`campaign_result.py@f237178:1269-1270`), that is, through `g5_unit_spec` (`campaign_supervisor.py@f237178:1691`, `:2518`).
   - **Protocol.** The `campaign_protocol` g5 permissions are `{'STATUS', *CHECKPOINT_OPERATIONS}` (`campaign_protocol.py@f237178:93`).
   - **The C′ identity map (D8).** Step 2's `ops/c1_rail/qualification/execution/runtime_identity.py` (map, expected-identity derivation, checks, coverage labels; #614 card `:113`) on the base. It does not exist at `f237178`.
   - **The R1 fixture seam.** `tests/integration/qualification_boundary/conftest.py@f237178:59-67` reads `FP_QUALIFICATION_S2`–`S5` into the boundary flags. `fixture_install.install` (`fixture_install.py@f237178:35`) installs the roles and keys (`:42-55`). `fixture_producer.py@f237178:49` observes runtimes for `worker`, `supervisor` and `g5` only. The result/seal Linux file skips on `boundary.dispatch` (`test_campaign_result_seal_linux.py@f237178:73-75`).
   - **The required-node derivation.** `scripts/qualification_boundary_verification.py@d716106:143-158`: `--s3`/`--s4`/`--s5` require the registered nodes of their case files; `--test-only` (N1_ONLY) requires **every registered node outside `S5_CASES`**, and the manifest validator refuses a required node that is skipped or never collected.
3. **Findings returned before any code.** The coordinator acknowledges each one.
   - (a) **The joint decision encoding.** Find the literal that S4's joint assessment writes as the N2 row `decision` when exactly one, or both, of `N2` and `PART_B` fail (S4-D2: one assessment with `stage_decisions {N2, PART_B}` plus the campaign decision; ledger `:699`). Cite file:line in S4's parser. The existing test writes `decision='FAIL'` for a joint FAIL (`test_campaign_result_commit.py@f237178:163-169`). Confirm it; do not assume it.
   - (b) **Whether term 8 can be exercised on the synthetic-predecessor overlay.** `_checkpoint_receipts` returns N1 only (`campaign_result.py@f237178:741-766`), and `validate_campaign_result` refuses non-synthetic later rows (`:561-564`). Under D2, term 8's end-to-end cases run on the accepted `synthetic_predecessor` overlay (ledger `:671`); real S5 aggregation is out of scope. If term 8 cannot be exercised that way, return NEEDS_CONTEXT.
   - (c) **The exact seam sites** for each provisioning row (6a, 11/11a, 20, 21; ledger `:707`), plus the `campaign_funding` role and phase map, the `guardian_main` role branches (`campaign_supervisor.py@f237178:1339`, `:1531-1540`), `container_ownership.campaign_scopes`, `campaign_host.cleanup`, the `runtime_identity` map entries (D8) and the fixture seam (§2.6). Give file:line on the base.
   - (d) **Which changed file is in the 68-module Stage 1c measured closure.** The membership is the closure table `docs/notes/2026-09-29-s5-c3-record/stage1c-equivalence/stage1c_closure_table.py.txt`, run on the base. As of `f237178`, the members this card would touch are `runtime.py`, `release_schema.py`, `campaign_protocol.py` and `policy.py`. `campaign_result`, `campaign_seal`, `seal_service`, `g5_result`, `campaign_funding`, `campaign_supervisor`, `service` and `campaign_store` are outside it. Source: the H9 return's closure JSON, `C:/Users/joshu/.codex/worktrees/h9-t05-integration/multi_firm_operations/.cache/h9/rebase-stage1c-closure.json`, local and read-only. Re-run the table on the base. Do not rely on this list. **State explicitly whether step 2's `runtime_identity.py` is a member on the base:** D3 as ruled names only `runtime.py`, `release_schema.py` and `campaign_protocol.py`.
   - (e) **Whether registering the four result/seal operations or the `seal` process role opens the route** under any existing release literal. Before T06, the route must stay closed (`release_schema.py@f237178:27`; staged acceptance `:565`).
   - (f) **Whether the seal credential can be provisioned under the existing `seal` key role and enrollment format** with no change to `keys.py` or to `KEY_ROLES`, and no new key family, signer or rotation rule. If it cannot, stop: NEEDS_CONTEXT (§7).
   - (g) **Manifest registration ordering.** Whether the R1 tooling (`R1_CASES`, `--r1`, and `--test-only` excluding every `R1_CASES` file; R1 tooling card `:76-83`) is on the base. If it is not, registering the result/seal or C′ Linux nodes would put them into the N1_ONLY required set, where they skip, and `--test-only` would fail on every PR. Return the registration plan; do not register until the coordinator acknowledges it.
   - (h) **The proposed fault literals (D6)** and their allowed roles, for the coordinator to fix at acknowledgement.

## 0.5. Routing

This is a Codex lane. H9 is a Codex-coordinator workstream, and the step-2 card fixes the single writer and the same branch (#614 `:250`). It is not a GLM ticket: it changes authority, signing and provisioning code on the protected qualification path, which is security-relevant (AGENTS.md, GLM rule). No secrets, `.env`, Pine, ports, private values or account data are involved. If Phase 0 needs a decision that §12 lists as OWED, return NEEDS_CONTEXT. Never assume the answer.

## 1. Goal

Make the T05 result/seal path agree with the canonical joint-batch policy (term 8). Fund the `result_g5` and `seal` works through the canonical funding. Add the TEST_ONLY result/seal fault cases. Provision the real qseal principal and a dedicated `result_g5` unit, with their C′ identity entries and checks. Install the R1 fixture seam so the result/seal Linux file runs under R1. **No new key policy, and no change to budgets, deadlines, frozen wire families, DB10 or route literals.** The scope boundary is the identity branch plus Windows evidence. Linux evidence belongs to R1, under a separate grant (§9).

## 2. Scope

### 2.1 Term 8: joint-batch validator reconciliation

All three seams accept every authentic complete prefix the policy allows:
- `PASS,PASS,FAIL,PASS`: N2 FULL fails and the halves pass.
- `PASS,PASS,FAIL,FAIL`: both fail.
- `PASS,PASS,PASS,FAIL`: the halves fail and FULL passes.

The three seams are `parse_receipt_row`, `_row_outcome` and `parse_campaign_result` (ledger `:693`). E03 requires "one joint batch, both assessments, no Part A, no seal" (spec `:212`).

The rule becomes: **every failing stage lies in the last present checkpoint, and that checkpoint's decision is FAIL exactly when at least one of its stages fails.**

These stay unchanged:
- LEGALITY is pass-only (`campaign_result.py@f237178:191-192`, `:316-317`).
- The wire shape, `STAGE_ORDER`, `CHECKPOINT_STAGES`, membership, families and operations.
- Every prior-checkpoint failure constraint: a FAIL before the joint batch ends the campaign, and so does any FAIL in the joint batch, so no PART_A row may follow.
- The incomplete-passing-prefix refusal.
- Existing refusal messages for the shapes existing tests already pin, for example `'only the last stage of a complete prefix may fail'` (`test_campaign_result_commit.py@f237178:127-131`).

**Downstream seams.** If the authentic four-stage commit, receipt, snapshot, reopen, integrity walk, G5 rebuild or seal refusal exposes a further defect, name that seam and return it (§7). Examples: `parse_result_snapshot` `:351-408`, `result_integrity` `:1243`, `g5_result.py:171`. Never widen scope silently.

### 2.2 Result-role funding (D5 resolved)

`result_g5` (RESULT) and `seal` (SEAL) become funded work roles in the canonical funding. **D5:** the closed role set widens under the existing `qualification_campaign_schedule_request/v1` literal and `PROFILE` `qualification_campaign_budget_profile/v3` (`campaign_funding.py@f237178:25`), as S3, S4 and S5 widened it (`:32-45`). `reserved_compute_phases` stays exactly `ADMISSION`, `N1`, `N2`, `PART_A`.
- the role and phase map in `campaign_funding`, beside `n1_g5`/`n2_g5`/`part_a_g5` (`campaign_funding.py@f237178:26-52`);
- the `guardian_main` branches to `run_result_g5` (`campaign_result.py@f237178:1322`) and `run_seal_unit` (`campaign_seal.py@f237178:496`).

Each reserves its **installed** phase ceiling from the profile through `reserve_result_work` / `reserve_seal_work`, against the original allowance and the absolute deadline. It settles once from actual counters, and unknown usage consumes the full reservation (ledger `:88`). An overrun or uncertainty ends authority through the existing `ResultStore._settlement_terminal`. Exhaustion refuses. A retry renews no allowance, deadline, attempt, salt, seed or plan. Unifying the two `_settlement_terminal` helpers is out of scope (D2).

No phase cap, ceiling, formula, tolerance or profile value changes.

### 2.3 TEST_ONLY result/seal fault cases (D6 resolved)

These extend the existing diagnostic `fault` mechanism (`campaign_funding.py@f237178:84-91`, `service.py@f237178:711-727`) to the result and seal works. **D6:** the result and seal paths take **new** fault literal(s), proposed at Phase-0 finding (h) and fixed by the coordinator; `'hold_after_intent'` stays byte-unchanged with its existing g5-only role restriction. The case list is fixed by D7 (#614 `:250`):
1. **The fault is bootstrap-frozen and immutable.** It is read only from the persisted `full_campaign_bootstraps` request. A later request cannot add, change or remove it.
2. **A durable T1 pre-sign hold.**
   - Result path: after `persist_result_intent`, before authentication and T2.
   - Seal path: after `prepare_seal_intent`, before the qseal IPC.
   - In both, the intent is durable and the commit waits for the exact retry.
3. **The fault is absent in normal runs.** Absent means absent. Each new literal is refused for every role but its own (`result_g5` or `seal`), and it is never present unless the request is TEST_ONLY.
4. **An exact retry renews nothing:** no key, signing instant, payload or budget. It returns the byte-identical receipt with `historical=true` (T05 F5, handoff `:36`).
5. **The real T1 consumer.** The retry consumes the persisted T1 row through the production path, not a test double.
6. **Startup, funded hold and recovery, exhaustion, and VOID.**
   - A fault at startup.
   - A funded hold, followed by recovery through the exact retry.
   - Exhaustion or the deadline passing during the hold refuses the commit.
   - VOID during the hold refuses the commit, in both publication orderings (VOID before T2; T2 then VOID flips validity only).

### 2.4 qseal and dedicated result_g5 provisioning (D3 ruled)

These are the seam rows (ledger `:707`; T05 handoff `:61`):
- **6a:** `runtime.ENTRYPOINTS['seal']`.
- `release_schema.PROCESS_ROLES` gains `seal`.
- `bootstrap.py` gains the `seal` role.
- **11/11a:** the seal principal (role_policy, provision.sh) and its credential root, with the installed `qualification-installation/seal.json` and a 0400 seal-owned credential.
- **20:** the production service→qseal transport (`seal_service.exchange`). It replaces the Windows double `qseal_sign` at integration.
- **21:** the `permitted` ACL rows in `campaign_protocol`.
- `container_ownership.campaign_scopes` gains `seal_unit`, and `campaign_host.cleanup` gains `*-seal.service`.

`result_g5` gets a **dedicated** unit spec, distinct from `g5_unit_spec`, charged to RESULT (T05 F4, handoff `:34`). qseal has no Docker, worker or result-key access (spec S7, ledger `:294`).

**No new key policy.** The existing `result` and `seal` key roles are used (`release_schema.py@f237178:32`). The following do not change:
- `keys.py`, `KEY_ROLES`, enrollment and rotation;
- the key families;
- the signer set.

Credentials are referenced and never embedded. No key bytes are generated into, committed to or quoted from the repository. Windows tests use the accepted injectable `_loader=` (ledger `:671`).

### 2.5 C′ identity map for result_g5 and qseal (D8 resolved)

Step 3 extends step 2's `runtime_identity` map and checks with `result_g5` and qseal entries, because step 3 creates their producers (#614 `:253-254`: each must have its provisioned producer and identity checks reviewed and merged before R1). The same expected-identity derivation, checks and coverage labels apply; no identity rule changes for existing roles. Windows cases extend the three `test_runtime_identity_*.py` files; the Linux counterparts are nodes of `test_runtime_identity_linux.py`, collected only.

### 2.6 R1 fixture seam and node registration

The R1 tooling card assigns these to H9 (its `:77`, `:141`, `:225`). Names follow that card's recommended D2: environment variable `FP_QUALIFICATION_R1`, set by `--r1` on top of the S2–S5 variables. If the R1 tooling freeze renames them, follow the frozen names.
- **Fixture seam.** `conftest.py` reads `FP_QUALIFICATION_R1`. `fixture_install.install` installs the `result_g5` and `seal` roles under it: the seal principal and UID, the credential root, `seal.json` and the 0400 credential, through the same provisioning as §2.4, referenced and never embedded. `fixture_producer.py` observes the `seal` runtime only if finding (c) requires it. The Linux result/seal file's skip (`:73-75`) keys on the R1 flag instead of `boundary.dispatch`, so it stops skipping under R1. With `FP_QUALIFICATION_R1` unset, every existing mode installs and collects exactly as before.
- **The Linux file's correction.** Before execution, apply the H9 return's correction of the "'seal' role name/UID membership check, implicit seal polling and unit patterns" (`.cache/h9/RETURN.md:72`, "Seal principal/provisioning seam").
- **Registration.** Register the result/seal Linux nodes (and the D8 C′ identity Linux nodes) in `tests/ops/qualification/invariant_manifest.json`, which has 0 `result_seal` rows on `main` and on `f237178`. Register only on the plan acknowledged at finding (g): no registered node may enter an existing mode's required set where it skips.
- **Not this card:** `scripts/qualification_boundary_verification.py`, `scripts/s2_run_evidence.py`, `scripts/guard_s2_runs.py` and the workflow. They belong to the R1 tooling card.

### 2.7 Files

**Allowed** (the final list is frozen at D4):
- **New:** the four `test_result_*` acceptance files in the authority block.
- **Edit, in `ops/c1_rail/qualification/execution/`:**
  - `campaign_result.py`: the three seams and the `result_g5` launch.
  - `campaign_seal.py`: the hold and the transport call.
  - `seal_service.py`: the production `exchange` and the qseal listener.
  - `runtime_identity.py` (step 2's): the `result_g5` and qseal entries and checks (D8), subject to finding (d).
  - `g5_result.py`, only if finding (c) or a §2.1 downstream seam requires it.
  - `campaign_funding.py`, `campaign_supervisor.py`, `service.py` and `campaign_store.py`, only for the seam lines named in finding (c).
- **Edit, measured closure, admitted by D3:** `runtime.py` (`ENTRYPOINTS['seal']`), `release_schema.py` (`PROCESS_ROLES`) and `campaign_protocol.py` (the operations and the `permitted` rows), only to provision `result_g5` and qseal.
- **Edit, host tooling:** `deploy/qualification/bootstrap.py`; `tools/qualification_verification/{role_policy.py, provision.sh, container_ownership.py, campaign_host.py, cleanup.py, host.json}`.
- **Edit, test support:** `tests/ops/qualification/invariant_manifest.json` (§2.6); `tests/ops/qualification/execution/result_fixture.py` (the joint-batch shapes); `tests/integration/qualification_boundary/{conftest.py, fixture_install.py}` and, only per finding (c), `fixture_producer.py` (§2.6); `tests/integration/qualification_boundary/test_campaign_result_seal_linux.py` and `test_runtime_identity_linux.py`, which are extended and collected only.
- **Extend in place, never replace:** the existing test files in the authority block.

**Measured closure (D3, RULED YES).** Joshua, directly to coordinator (3), 2026-10-02 ("all recommended"): lane D step 3 may edit the measured-closure modules `runtime.py`, `release_schema.py` and `campaign_protocol.py` to provision `result_g5` and qseal. It is covered by the one fresh S5 Part A measurement before R1, on the same basis as step-2 D5 (#614 `:248`). Any other measured-closure module, including `runtime_identity.py` if finding (d) shows it is a member, is not admitted: return it, and it goes to the operator under the C3 decision rule (ledger `:1937-1940`).

**Forbidden files:**
- **The T00 P7 first-party closure, all 40 modules.** The list is #614 card `:259-264`; the count is the accepted record `docs/briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md:630`, and the accepted P7 run and its `code_closure_sha256` are at `:743-751`. In `ops/c1_rail/qualification/` it includes `blocks`, `clock`, `contract`, `model`, `p7_driver`, `p7_evidence`, `panel`, `paths`, `production_source`, `regime`, `replay`, `runner`, `sessions` and `trust_domain`. None is needed here. Touching any one of them would owe a P7 re-run under a fresh Joshua-signed approval.
- `ops/c1_rail/qualification/policy.py`. It governs term 8, it is in the measured closure, D3 does not admit it, and it must not be edited.
- `ops/c1_rail/qualification/seal.py`, the legacy authority. Do not import or reactivate it (T05 handoff `:83`).
- `ops/c1_rail/qualification/execution/keys.py`.
- `store.py`, the DB10 layout literals, `RESULT_SCHEMA`/`SEAL_SCHEMA`, and every `/v1` result, seal and supervision family.
- The files of PR #609 (S8 harness): `scripts/check_qualification_invariants.py`, `scripts/qualification_boundary_verification.py`, `tests/integration/qualification_boundary/{campaign_sources.py, fixture_install_s8.py, test_full_campaign_boundary.py}` and `tests/test_qualification_s8_harness.py`. Flipping E03's xfail belongs to S8 after integration.
- The R1 tooling files (§2.6, "Not this card").
- The files of PR #611: `production_source.py` and its test.
- `.github/workflows/**`.
- `core/`, `lab/`, Pine and ports.

**Closure impact.**
- **S5 measured closure:** term 8 alone touches no measured module. The D3-admitted edits to `runtime.py`, `release_schema.py` and `campaign_protocol.py` do. Step 3 is already on the ledger's list of closure changes that precede the one fresh S5 Part A measurement, which is taken after the FINAL closure change with nothing carried (ledger `:2124`; #614 `:248`, `:258`). The return must report the closure table at its head.
- **R1:** `campaign_funding`, `campaign_supervisor` and `service` sit in the Linux selection's closure. R1's combined node set covers them (term 5, ledger `:683`).
- **P7:** none of these files is in the closure (item 15).

## 3. Method

- **Tests first.** Each red→green case in §4 is written and shown failing on the base, with a launcher record, before any production edit. After the change it passes.
- **Preservation cases are not given red evidence.** They pass on the base and on the build. Do not fabricate a red record for one (#614 `:221`).
- **Pinned vectors are extended, never replaced** (the S3 D1 precedent as #614 card §3 states it, `:122`).
- **Windows only.** The qseal process, the UID and the unit launch are exercised as functions with injected fakes (T05 F4). Their real-OS counterparts are nodes of the Linux files.

## 4. Acceptance checks (falsifier-first)

**H:** after step 3, the validators accept exactly the policy's legal complete prefixes, including both joint-batch FAIL shapes, and nothing more. The `result_g5` and `seal` works are funded and settled against the original allowance and deadline. The TEST_ONLY result faults behave as listed. qseal and `result_g5` run as provisioned, separate principals with C′ identity entries and no new key policy. Every existing acceptance test keeps its outcome, and every existing boundary mode's collection and required set is unchanged.

**Reject if:**
- a red→green case cannot be made to fail on the base, or fails on the build;
- a preservation case changes outcome;
- any receipt, retry outcome or budget value from before step 3 differs at the build head.

**Revert trigger:** the same receipt, retry-outcome or budget-value difference.

**Red→green (each fails on the base, then passes):**
1. **`PASS,PASS,FAIL,PASS`** (N2 FAIL, PART_B PASS): accepted by `parse_receipt_row`, `_row_outcome` and `parse_campaign_result`. One test per seam. Then end to end: build, validate, reserve, intent, commit, receipt, reopen and integrity, with `outcome='FAIL'` and `accepted_prefix=[LEGALITY,N1,N2,PART_B]`.
2. **`PASS,PASS,FAIL,FAIL`**: the same four layers.
3. **A scheduler request** with role `result_g5`, and one with role `seal`, is refused on the base (`'private fixed scheduler role required'`, `campaign_funding.py@f237178:68-73`). After the change it is accepted under `schedule_request/v1` and `PROFILE` v3 and reserves its installed phase ceiling.
4. **Result-role funding:**
   - settlement within budget completes;
   - an overrun or uncertainty after commit ends authority, and the receipt survives as history;
   - exhaustion or a passed deadline before reservation refuses;
   - a retry renews no allowance or deadline.

   Exactly which of these is red on the base is **OWED** to Phase 0. A case that already passes on the base moves to preservation.
5. **The TEST_ONLY result/seal faults**, §2.3 items 1–6. Each has at least one test, covering both the result path and the seal path, using the D6 literal(s).
6. **The dedicated `result_g5` unit spec** is distinct from `g5_unit_spec` and charged to RESULT.
7. **qseal provisioning:**
   - `runtime.ENTRYPOINTS['seal']`, the `seal` entry in `PROCESS_ROLES` and the `bootstrap.py` role are present;
   - a seal principal exists with no Docker, worker or result-key access;
   - `seal.json` and the 0400 credential are installed;
   - the production `exchange` works, with bounded 0600 IPC (ledger `:705`);
   - the cleanup and ownership rows are present;
   - a missing principal, a missing credential or a wrong UID refuses.
8. **No new key policy, checked mechanically:** `git diff <base>..HEAD -- ops/c1_rail/qualification/execution/keys.py` is empty, and `KEY_ROLES` is byte-identical.
9. **C′ identity (D8):** the `runtime_identity` map has `result_g5` and qseal entries; a missing entry and a mismatched observed identity for either role refuse, with the same checks and coverage labels as the existing roles.

**Preservation (green before and after):**
10. `PASS,PASS,PASS,FAIL` (`test_campaign_result_commit.py@f237178:88-96`, `:163-174`); the all-PASS result; FAIL after LEGALITY/N1; FAIL after PART_A.
11. **Refusals that stay refusals:**
    - N1 FAIL followed by any row (existing message unchanged);
    - any LEGALITY FAIL;
    - a PART_A row after any joint-batch FAIL (E03: "no Part A");
    - a joint row whose decision disagrees with its stages (decision PASS or CONTINUE with a FAIL stage; decision FAIL with both stages PASS);
    - an incomplete passing prefix;
    - missing, extra or out-of-order rows (`:99-131`).
12. **Seal refusals stay:** `seal_service._require_committed_pass` and `seal_eligibility` refuse every FAIL outcome, including both new shapes. There is no seal for E03.
13. **The existing role and fault refusals are unchanged:** `'hold_after_intent'` is byte-unchanged and still refused for non-g5 roles, the existing probes are unchanged, and `reserved_compute_phases` is exactly `ADMISSION`, `N1`, `N2`, `PART_A` (D5).
14. **Frozen files and vectors pass unchanged:** the frozen RESULT/SEAL and DB10 tests (`test_campaign_result_layout.py`, `test_campaign_seal.py`, `test_result_seal_guardian_loop.py`), the release `/v1`–`/v8` vectors, and the step-2 identity tests for the existing roles.
15. **Exact historical retry** writes nothing and returns byte-identical receipts.
16. **Disjointness:** `git diff --name-only <base>..HEAD` is disjoint from the 40-module P7 closure, from #609's and #611's files and from the R1 tooling files. The measured-closure table at the head shows only `runtime.py`, `release_schema.py` and `campaign_protocol.py` changed (D3).
17. **Boundary modes unchanged without R1:** with `FP_QUALIFICATION_R1` unset, the fixture installs the same roles as on the base, the Linux result/seal file still skips, and `test_qualification_invariant_manifest.py` passes. No newly registered node enters the `--test-only`, `--s2`…`--s5` required sets (finding (g)).

**Runs, each with its launcher record** (`python -I scripts/fp.py` from the executor worktree; cite `record.json` and check `status: completed`, exit 0, `source_stable`):
- `python -I scripts/fp.py --workers 2 python -m pytest <the authority-block acceptance set> -q`
- `python -I scripts/fp.py --workers 2 python -m pytest tests/ops/qualification tests/test_qualification_*.py -q`
- `python -I scripts/fp.py check`
- `python -I scripts/fp.py python -m pytest --collect-only -q tests/integration/qualification_boundary/test_campaign_result_seal_linux.py tests/integration/qualification_boundary/test_runtime_identity_linux.py`: report the collected node count per file; do not run them.
- `git diff --check`

**CI, on the coordinator-opened PR; a CI result is not acceptance:**
- `Tests` (`tests.yml`);
- `Pylint` (`pylint.yml`; the whole-repo 8.00 gate);
- the required `skills (3.12)` (`gate-manifest.yml:30`);
- `Qualification unit tests (Windows)` (`qualification-windows.yml`);
- `Qualification execution boundary (1)/(2)` (`qualification-execution-boundary.yml`);
- the PR-triggered `Qualification S2 supervision` (`qualification-s2-supervision.yml:32-55` path filter; it includes `tests/ops/qualification/invariant_manifest.json` and `tests/integration/qualification_boundary/**`).

The coordinator reads Codex review at the exact head. The result/seal and C′ Linux nodes run only in R1.

## 5. Forbidden

- Any file in §2.7's forbidden list. A measured-closure module that D3 did not admit.
- Editing `policy.py`, or loosening a validator past the policy: any shape `required_output_roles` refuses.
- Changing a frozen wire family (RESULT/SEAL `/v1`, supervision `/v2` and step 2's versions, the snapshots), the DB10 layout, budgets, deadlines, allowances, profiles, ceilings, phase caps, formulas or tolerances.
- New key policy: a new key role or family, a key-generation path, a rotation rule, a `keys.py` edit, or committing or quoting key or credential bytes.
- A route-enabling release literal before T06. An in-process qseal presented as separation. A caller-supplied PASS accepted by qseal. A seal on anything but `RESULT_COMMITTED_PASS`. Fresh time, key or payload on retry. (T05 handoff `:83`.)
- Changing `'hold_after_intent'` bytes or its role restriction.
- Registering a Linux node into an existing mode's required set where it skips.
- Any Linux run, workflow dispatch or CI-configuration change; opening a PR; merging; pushing to `main`; any host, vendor or account action.
- Any replay, screen, Monte Carlo, P7, or candidate-configurable code run.
- Real S5 aggregation and `_settlement_terminal` unification (D2: owed to H9 integration before R1), B4, #611, the R1 tooling, R2 and the S8 harness.

## 6. Return (status taxonomy)

Return DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED. The coordinator's verdict is RESOLVED (every §4 item holds) or FALSIFIED (named items fail; returned to the executor). The return holds:
- the branch, head SHA and base, the `origin/main` merge and its range-diff; `git diff --stat` and the name list;
- Phase-0 findings (a)–(h);
- for each red→green case, the fail-on-base record ID and the pass-on-build record ID;
- for each preservation case, the record ID on the base and on the build;
- the item-8 empty `keys.py` diff and the item-16 disjointness output;
- the measured-closure table at the head;
- each Linux file's collected node count, the result/seal file's seal-role correction, and the registered node IDs;
- the seam table (file:line → T05 call) for rows 6a, 11/11a, 20 and 21, the D8 identity entries and the §2.6 fixture seam;
- any downstream seam named under §2.1;
- concerns.

## 7. Stop conditions (return to the coordinator; do not work around)

- After Phase-0 findings (a)–(h): return them, then wait for the coordinator before writing code.
- Any of these would have to change: a P7 closure file, a measured-closure module that D3 did not admit (including `runtime_identity.py` if it is a member), `policy.py`, a frozen wire family, DB10, a budget, or the key policy.
- Finding (f): the seal credential cannot use the existing `seal` key role. Return NEEDS_CONTEXT.
- Finding (e): registration would open the route. Return NEEDS_CONTEXT.
- Finding (b): term 8 cannot be exercised on the synthetic-predecessor overlay. Return NEEDS_CONTEXT (D2).
- Finding (g): the R1 tooling is not on the base and no registration plan avoids the N1_ONLY required set. Return NEEDS_CONTEXT.
- A downstream seam past the three validators (§2.1).
- A red→green case cannot be made to fail on the base. Reclassify it as preservation and report it; do not fabricate red evidence.
- Two failed corrections of the same issue (AGENTS.md).
- **Operator review-round rule (2026-10-02):** after more than three review rounds that each return two or more P1/P2 findings, stop folding. The coordinator adjudicates a rewrite or a narrower scope.
- **Single writer:** a second writer appearing on the branch is a stop.

## 8. Out of scope and decision unlocked

**Out of scope:**
- The R1 Linux run (§9).
- **Real S5 aggregation** (the `_checkpoint_receipts` composite-key reader and the N2/PART_A canonical verifiers) and **`_settlement_terminal` unification**. D2: OWED to H9 integration before R1 (H9 return, `.cache/h9/RETURN.md:69-70`). Term 8 runs here on the synthetic-predecessor overlay.
- B4, which comes before T06 dispatch and does not block R1 (PR #610 ruling, staged acceptance `:534`).
- #611, the qualification-path items.
- The R1 tooling: workflow mode, scope, selector, reader and guard (#614 D6; `claude/r1-tooling`).
- The S8 harness and its E03 xfail flip (#609).
- R2, T06, and any production use.

**Unlocked:** once the Windows evidence is RESOLVED and the Codex relay is clean, the coordinator folds the term 8, result-funding, fault, provisioning and identity nodes into R1's combined node set. With every closure change landed, it schedules the one fresh S5 Part A measurement, then asks Joshua for the R1 grant.

## 9. R1 (separate grant; held by the coordinator)

This is not this card's work. Recorded so the freeze and R1 agree:
- **The combined order** (ruling 5, ledger `:1998-2006`): service → N1 → N2 → Part A → result/seal → supervision last, plus the C′ and VALID→VOID cases.
- **This step adds:** E03's two joint-batch FAIL shapes, the real `result_g5` unit, the real qseal unit with a separate UID and credential root, budget exhaustion, signing interruption, both VOID orderings, receipt history against current validity, cleanup absence (H9 return, "R1 evidence and acceptance"), and the `result_g5`/qseal identity checks.
- **Frozen at dispatch:** the exact IDs and count.
- **Cited in every R1 packet:** the residual "T05 C′ first-release host environment drift".

## 10. Audit hooks (runnable)

```bash
# Card form and authority. Expected: well-formed; exit 0.
python -I scripts/fp.py python scripts/check_brief.py --type handoff <frozen card path>
python -I scripts/fp.py python scripts/check_handoff_authority.py <frozen card path>
# Premise (Git Bash), in the executor worktree; BASE is the D1 answer.
git rev-parse HEAD; git merge-base --is-ancestor f8a03c2 HEAD && echo "term 8 record in history"
test ! -e .env && echo "no .env" || echo "FAIL: .env present"
# The three seams as they stand (expected: the last-stage-only rule at each).
grep -n "statuses\[:-1\]\|failed != \[len(statuses) - 1\]\|present\[:-1\]" ops/c1_rail/qualification/execution/campaign_result.py
# Role and provisioning gaps on the base.
grep -n "WORK_PHASES\|'hold_after_intent'" ops/c1_rail/qualification/execution/campaign_funding.py
grep -n "ENTRYPOINTS\|PROCESS_ROLES\|KEY_ROLES" ops/c1_rail/qualification/execution/runtime.py ops/c1_rail/qualification/execution/release_schema.py
# Fixture seam and registration (expected on the base: no R1 flag, 0 result_seal rows).
grep -n "FP_QUALIFICATION_R1" tests/integration/qualification_boundary/conftest.py scripts/qualification_boundary_verification.py
grep -c "result_seal" tests/ops/qualification/invariant_manifest.json
# Item 8: no new key policy (expected: empty).
git diff "$BASE"..HEAD -- ops/c1_rail/qualification/execution/keys.py
# Measured-closure re-check at return.
python -I scripts/fp.py python <scratch>/stage1c_closure_table.py . "$BASE" HEAD
git diff --stat "$BASE"...HEAD
```

## 11. Prerequisites (all before dispatch)

1. **Lane D step 2 (C′) is RESOLVED** by the coordinator and integrated on the H9 branch, and its Codex relay is clean. That head becomes this card's base (D1).
2. **#614 is CLEAN** at its exact head (currently `2416bf0`; card bytes identical to `7b2d74e`) and merged, so that the step-2 card, its D1–D10 resolutions and the D9 design are frozen owners.
3. **Term 8's record is merged.** Satisfied: #610 merged at `f8a03c2`, and ledger `:693` is on `main`.
4. **Joshua's ruling under the C3 rule** on step 3's measured-closure edits (D3). Satisfied: ruled YES directly to coordinator (3), 2026-10-02, for `runtime.py`, `release_schema.py` and `campaign_protocol.py`.
5. **The R1 tooling card is committed and its names are frozen** (`claude/r1-tooling`), so that §2.6 uses the frozen environment variable and case names. Registration additionally waits on finding (g).
6. **This card is frozen:** the §12 OWED items answered and every code line citation re-anchored on the base. It is committed under the committed-handoff rule, and its SHA is recorded in the ledger.
7. **The Codex coordinator acknowledges the dispatch** and names the executor.

## 12. Decisions (rulings applied; OWED items for the coordinator at freeze)

- **D1 Base — RESOLVED (SHA OWED).** The lane D step-2 RESOLVED head. `origin/main` is merged in at build start, with the range-diff reported, as in step 2. The SHA is **OWED** until step 2 is RESOLVED.
- **D2 Real S5 aggregation and `_settlement_terminal` unification — RESOLVED.** Both are OUT of step 3 and **OWED to H9 integration before R1**. Term 8 runs on the synthetic-predecessor overlay (finding (b)). The slice owner inside H9 integration is **OWED**.
- **D3 Measured-closure edits — RULED YES** (Joshua, directly to coordinator (3), 2026-10-02, "all recommended"). Step 3 may edit `runtime.py`, `release_schema.py` and `campaign_protocol.py` to provision `result_g5` and qseal, covered by the one fresh S5 Part A measurement before R1, on the same basis as step-2 D5. Whether the `seal` process role enters `/v8` or a later release revision is **OWED** to Phase 0 (finding (e)) and the coordinator. Whether `runtime_identity.py` is a closure member, and so outside D3 as worded, is **OWED** to finding (d).
- **D4 The final allowed file list** and the names of the new test files: **OWED**.
- **D5 Funding role widening — RESOLVED YES.** `result_g5` and `seal` join the closed role set under `schedule_request/v1` and `PROFILE` v3. `reserved_compute_phases` stays `ADMISSION`, `N1`, `N2`, `PART_A`.
- **D6 Fault literals — RESOLVED: new literals.** `'hold_after_intent'` stays byte-unchanged with its role restriction. The literal names and their allowed roles are **OWED** (finding (h)).
- **D7 PR authority — OWED confirmation.** As drafted, the worker has no `pr.open`; the coordinator opens PRs, as in #614 D10.
- **D8 C′ identity map for `result_g5` and qseal — RESOLVED: this step.** The step-2 `runtime_identity` map and checks are extended here (§2.5), and step 2's identity tests join the acceptance set.

## Pre-mortem (README rule)

- **Loop cost:** one Windows build loop and its records. No Linux run.
- **Decisions the executor will hit:** the D6 literal names, the D3 release-revision question, finding (d)'s `runtime_identity.py` membership and finding (g)'s registration order. They are acknowledged in one batch after Phase 0.
- **What makes it moot:** an operator ruling that withdraws term 8 or the T05 seal route, or a step-2 return that changes the result/seal seams.
- **Measurements the return fills in:** Phase-0 findings (a)–(h), the per-case records and the closure re-check. **No numbers are asserted here.** Every budget, ceiling and count comes from the installed configuration and the records.
