# H9 lane D step 2: T05 C′ runtime-identity build (Codex lane)

**Type:** cc_handoff (worker build card)

**Status:** DRAFT, 2026-10-02. Drafted by a coordinator worker for the deployment coordinator to freeze; not dispatched. The coordinator answers §12's open decisions, commits the frozen revision under the committed-handoff rule and records its SHA in the ledger before any worker starts.

**Executor:** the H9 Codex executor, routed through the Codex coordinator. It is the single writer of its identity branch (`codex/h9-cprime-identity`, proposed), cut from the frozen base (D1).

**Coordinator:** the deployment coordinator ("Coordinating parallel Claude sessions (2)"). It owns the freeze, the diff review, integration into the H9 branch, every Linux dispatch, the Codex relay, PRs and the ledger.

**Owners this card narrows (it changes none of them):**
- C′ obligation, rulings 1–5 and the residual: [ledger, T05 C′ rulings](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-rulings--t05-environment-sealing-c-and-the-first-release-host-environment-drift-residual-2026-10-02) (`:1983-2034`).
- S6 freeze amendment terms 1–7 ("yes, accept all seven", merged in #600 at `fbfd0c9`): [ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#coordinator-checkpoint-c-r--t05s6-result-commit-accepted-as-an-interface-s7-go-2026-09-21) `:673-694`. Term 8 is **pending** in open PR #610 (`claude/operator-rulings-2026-10-02-sitting1@497b937`) and belongs to §11, not to this step.
- H9 checkpoint R1 and its fail-first C′ case list: [staged acceptance H9](2026-09-27-staged-acceptance-handoffs.md#h9--resultseal-integration-and-bounded-same-sample-recovery-two-checkpoints) `:536-550`.

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
  - no_frozen_wire_family_or_db10_change
  - no_budget_deadline_or_allowance_change
  - no_base_pin_change
  - no_private_bytes_committed
  - single_writer
  - stop_at_coordinator_return
acceptance:
  - tests/ops/qualification/execution/test_runtime_identity_pin.py
  - tests/ops/qualification/execution/test_runtime_identity_launch.py
  - tests/ops/qualification/execution/test_runtime_identity_rechecks.py
  - tests/test_qualification_worker_image.py
  - tests/ops/qualification/execution/test_release.py
  - tests/ops/qualification/execution/test_campaign_supervision.py
  - tests/ops/qualification/execution/test_campaign_cancellation.py
  - tests/ops/qualification/execution/test_campaign_result_layout.py
  - tests/ops/qualification/execution/test_campaign_result_commit.py
  - tests/ops/qualification/execution/test_campaign_seal.py
  - tests/ops/qualification/execution/test_result_seal_guardian_loop.py
  - tests/test_qualification_invariant_manifest.py
```

The three `test_runtime_identity_*.py` files are new (§2.5). The Linux file `tests/integration/qualification_boundary/test_runtime_identity_linux.py` is written here and run only inside R1 (§9).

## 0. Phase 0: premise, Rule-0 reads and the findings returned before code

1. **Premise.** HEAD is the frozen base (D1). As of 2026-10-02, `origin/main@6de7bf9` differs from `c3ab0cc` under `ops/`, `tools/` and `deploy/` by nothing; under `tests/` only `tests/test_repo_map_scripts_table.py` differs. The H9 head `f237178` is one commit on `c3ab0cc` (13 files) and is not on `origin`. No `.env` in the worktree.
2. **Prerequisites the H9 card names, as recorded:** the pin approved (ledger ruling 4, `:1991-1995`); term 7 accepted (S6 amendment, `:685-692`); T00 merged at `c3ab0cc` and H9 rebased to `f237178` (term 6, `:684`). The D-S5 fix slices are merged (#586 `981eb12`, #589 `77cd715`).
3. **Rule-0 reads** (read them; do not infer them):
   - `ops/c1_rail/qualification/execution/image.py:43-75`: `build_worker` pulls the tag `python:<version>-slim-bookworm` at build time (`:56-57`) and accepts its single RepoDigest (`:59-62`). This is what the pin replaces. `prepare_context` (`:13-40`) already refuses a non-digest base.
   - `ops/c1_rail/qualification/execution/release_schema.py`: releases `/v1`–`/v7`, and `worker_image_digest` (`:72`, `:170`), the built image identity term 7 keeps separate from the base.
   - `deploy/qualification/bootstrap.py:1-40`: isolated interpreter, root-owned code, and the fixed roles `worker`, `supervisor`, `g5`, `campaign_guardian`, `campaign_probe`, `campaign_control`.
   - `ops/c1_rail/qualification/execution/campaign_supervisor.py` (`parse_supervision_event`, `SUPERVISION_EVENT_V2`); `campaign_store.py:1340-1360` and `:1682-1760` (supervision-event retention); `campaign_store.py:1987-2075` (`claim_void_authentication`; sequence 0 is the uncharged attempt); `campaign_funding.py:717-805`.
   - `ops/c1_rail/qualification/execution/launcher.py:75-90` (`find_owned_worker(..., image_id, release_sha256)`), `admission.py:176`, `service.py:1261`.
   - On the base: `campaign_result.py`, `campaign_seal.py`, `seal_service.py`, `g5_result.py` (the result/seal commit and qseal sites).
   - `tools/qualification_verification/role_policy.py:6-7` (roles `qclient`, `qexec`, `qg5`).
   - `docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md:90` (`VALID -> VOID` is irreversible).
4. **Findings returned before any code (checkpoint; the coordinator acknowledges each):**
   - (a) the finite entrypoint map as source facts: per entry the role, executable, base interpreter, lock, wrapper, UID and launch site (`file:line`);
   - (b) the site of each recheck (checkpoint, result, seal, every VALID→VOID);
   - (c) whether the operator-recorded VOID path exists in code, and how a recheck mismatch is recorded on it;
   - (d) where the release binding lives, and whether any change touches a module of the 68-module Stage 1c measured closure (§2.5);
   - (e) how the runner's image store reports the platform child and config digests for the pinned index, so the build can verify them.

## 0.5. Routing and clarifying questions

Codex lane: H9 is a Codex-coordinator workstream. Not the GLM lane: this is identity and authority code on the protected qualification path (security-relevant; AGENTS GLM rule). No secrets, `.env`, Pine or account data are involved. The coordinator answers §12 D1–D10 at freeze. An unanswered decision that Phase 0 needs is returned as NEEDS_CONTEXT, never assumed.

## 1. Goal

Build T05's C′ obligation so that R1 can run: a canonical, operator-approved worker base pin; a signed release/runtime revision that binds the finite set of known R1 host entrypoints through the existing `release_sha256`; launch checks and transition rechecks, each leaving versioned evidence; and fail-closed refusal on any mismatch. Exact historical retry, the original budgets and deadlines, frozen v1 RESULT/SEAL and the DB10 two-table layout are preserved. **The scope boundary:** the identity branch plus Windows evidence only. Linux evidence is R1's, under a separate grant (§9).

## 2. Scope

### 2.1 Canonical base pin

- One canonical pin file (proposed `deploy/qualification/worker-base-pin.json`; D3) holding:
  - the index `python@sha256:afc139a0a640942491ec481ad8dda10f2c5b753f5c969393b12480155fe15a63` (the `python:3.12.3-slim-bookworm` manifest list);
  - the required `linux/amd64` child `sha256:fd3817f3a855f6c2ada16ac9468e5ee93e361005bd226fd5a5ee1a504e038c84`;
  - its config `sha256:cf001c2f8af7214144935ae5b37c9e626ccf789117c10c1f691766d4658f1b1e` (`architecture=amd64`, `os=linux`, `PYTHON_VERSION=3.12.3`);
  - the approval reference (ledger ruling 4) and the provenance pointer by path name only (`local_artifacts/h9-t05-base-pin-afc139a0/coordinator-fetch/`). The fetched bytes are never committed or quoted.
- Configuration as code: the builder and the release revision read this one file. No second copy of these digests lives in code or tests; tests load the file.
- `image.build_worker` pulls by the pinned digest, never by a tag. It refuses a missing, tag-only or mismatched pin, and a child or config identity that differs from the pin (per finding (e)). It records the base identity separately from the built `worker_image_digest`.

### 2.2 The finite R1 host-entrypoint map

Exactly the ruling's set (ledger `:2008-2014`): the runner/pytest admin fixture; the service supervisor; the campaign guardian, control and probes; the N1, N2, PART_A and RESULT G5 roles; qseal; the Python bootstrap/owned-command wrapper. Each entry's identity tuple is executable, base interpreter, lock, wrapper and UID (the H9 case list). Unmediated descendants, OS helper binaries (systemctl, busctl, docker), OS daemons and the kernel are outside the map and are labelled NOT_COVERED.

### 2.3 Checks and rechecks

- **Launch:** each mapped launch is checked before it spawns (controller), by the child itself (in `bootstrap.py`, standard library only, before any import), and by the controller through `/proc` after exec.
- **Checkpoint, result and seal commits:** the relevant identity is rechecked inside the original CPU/wall reservation and the absolute deadline, with no refresh and no retry.
- **Every VALID→VOID transition:** rechecked, **uncharged**. The recheck consumes no allowance and does not depend on the deadline, so VOID stays possible in BUDGET_UNCERTAIN, IN_DOUBT or past the deadline. The existing VOID authentication charging (`claim_void_authentication`) is unchanged. A mismatch refuses the *automatic* VOID commit and leaves the campaign for the operator-recorded VOID path, which records the mismatch; it never leaves PASS authority.
- **Fail closed:** a missing pin, a failed tuple check, an image mismatch, a timeout or exhaustion refuses authority.

### 2.4 Evidence

- Versioned supervision events for launch, exit and **every** recheck, each with expected identity, observed identity, transition and verdict. New schema versions sit beside `qualification_campaign_supervision_event/v2`; v2 bytes and parsers are unchanged.
- A coverage-label table that does not overclaim: COVERED for the mapped tuples; NOT_COVERED for installed distribution contents, tzdata and other data files, external mounts, late-loaded native or transitive libraries, unmediated descendants, OS helpers, daemons and the kernel. It names the accepted residual **"T05 C′ first-release host environment drift"**.

### 2.5 Files

**Allowed** (the final list is frozen at D4):
- New: the pin file; `ops/c1_rail/qualification/execution/runtime_identity.py` (map, expected-identity derivation, checks, coverage labels); the three acceptance test files; `tests/integration/qualification_boundary/test_runtime_identity_linux.py` (written, not run).
- Edit: `ops/c1_rail/qualification/execution/image.py`; `campaign_supervisor.py`; `campaign_store.py`; `service.py`; `launcher.py`; the base's `campaign_result.py`, `campaign_seal.py`, `seal_service.py` and `g5_result.py` (result/seal rechecks only); `deploy/qualification/bootstrap.py` (the child self-check); `tests/ops/qualification/invariant_manifest.json` (Linux node registration).
- Extend in place, never replace: `tests/test_qualification_worker_image.py`, `test_release.py`, `test_campaign_supervision.py`, `test_campaign_cancellation.py`, and `tests/test_qualification_invariant_manifest.py` if registration needs it.

**Checkpoint first (return before editing):** any module of the 68-module Stage 1c measured closure. On `main` it includes `release_schema.py`, `runtime.py`, `worker.py`, `campaign_probe.py` and `protocol.py` (closure table `docs/notes/2026-09-29-s5-c3-record/stage1c-equivalence/stage1c_closure_table.py.txt`, run 2026-10-02 against `origin/main` and `f237178`: 68 rows, 0 differences). A measured-closure change returns to the operator under the C3 decision rule (ledger `:1938`). D2 and D5.

## 3. Method

- Tests first: each §4 case is written and shown failing on the base with a launcher record, then passing on the build.
- Pinned vectors are extended, never replaced (the S3 D1 precedent, ledger `:657`): release `/v1`–`/v7`, supervision event `/v2`, RESULT/SEAL `/v1` and the DB10 layout keep their bytes and their refusals.
- The binding enters through `release_sha256` (D2): a release whose map or pin differs has a different `release_sha256`; historical receipts verify unchanged.
- Windows only. The child self-check and the `/proc` controller check are tested through injected fakes (the accepted `_loader=` pattern, ledger `:671`); their real-OS counterparts are nodes of the Linux file.

## 4. Acceptance checks (falsifier-first)

**H:** with C′ built, every mapped R1 launch and every checkpoint, result, seal and VALID→VOID transition refuses authority on a pin, image or tuple mismatch, and retains a versioned event for each check, while historical retry, budgets, deadlines, frozen v1 RESULT/SEAL and DB10 are unchanged. **Reject if** a case below cannot be made to fail on the base, fails on the build, or any existing acceptance test changes outcome. **Revert trigger:** any pre-C′ receipt, retry outcome or budget value differs at the build head.

Fail-first cases (the H9 R1 list, staged acceptance `:539-549`, one test or more each):
1. A missing, tag-only or mismatched base pin refuses; a child or config digest that differs from the pin refuses.
2. A built-image mismatch refuses at launch and at commit.
3. A mapped entrypoint whose executable, base interpreter, lock, wrapper or UID mismatches refuses (one case per field).
4. A missing or failed startup self-check, and a missing or failed controller check, refuse.
5. Missing exit evidence refuses.
6. Drift at checkpoint, result, seal and VALID→VOID refuses. The VOID recheck charges nothing and runs in BUDGET_UNCERTAIN, IN_DOUBT and past the deadline; its mismatch refuses automatic VOID, is recorded on the operator path, and never yields PASS authority.
7. A versioned supervision event is retained for every recheck; a missing event fails coverage.
8. A recheck timeout or exhaustion refuses, with no refresh, no retry and the original deadline.
9. An exact historical retry writes nothing and returns byte-identical receipts.
10. Coverage labels do not overclaim: a native or tzdata change and an unmediated descendant are reported NOT_COVERED.

Preservation checks:
11. The frozen RESULT/SEAL and DB10 tests on the base (`test_campaign_result_layout.py`, `test_campaign_result_commit.py`, `test_campaign_seal.py`, `test_result_seal_guardian_loop.py`) pass unchanged.
12. Release `/v1`–`/v7` and supervision event `/v2` vectors pass unchanged.
13. `git diff --name-only <base>..HEAD` is disjoint from the T00 P7 first-party closure (40 modules; list attached at D8) and, unless D5 rules otherwise, from the 68-module measured closure (closure table: 0 differences).

Runs, each with its launcher record: the acceptance set; `tests/ops/qualification` plus `tests/test_qualification_*.py`; `python -I scripts/fp.py check`; `git diff --check`. The Linux file collects without running.

## 5. Forbidden

- Editing any file of the T00 40-module P7 first-party closure.
- Editing a 68-module measured-closure module before the §2.5 checkpoint.
- Changing frozen wire families (RESULT/SEAL `/v1`, supervision event `/v2`, snapshots), the DB10 layout, budgets, deadlines, allowances, profiles or ceilings.
- Changing the pin, adding another base image, or resolving any tag.
- Any Linux run, workflow dispatch or CI-configuration change (including an R1 workflow mode or evidence scope), opening a PR, merging, or pushing to `main`.
- Committing or quoting the coordinator-fetched registry bytes or any private value.
- New key policy, provisioning or host-side change.
- §11 (lane D step 3) work, B4, the qualification-path fixes, R2.
- `core/`, `lab/`, Pine.

## 6. Return (status taxonomy)

Return DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED. The coordinator's verdict is RESOLVED (every §4 item holds) or FALSIFIED (named items fail; returned to the executor). The return holds:
- branch, head SHA and base; `git diff --stat` and the name list;
- Phase-0 findings (a)–(e);
- per case, the fail-on-base and pass-on-build record IDs;
- the preservation results and the item-13 disjointness output;
- the Linux file's collected node count;
- the coverage-label table and the residual citation;
- concerns.

## 7. Stop conditions (return to the coordinator; do not work around)

- Phase-0 findings (a)–(e): return them, then wait for the coordinator before code.
- A T00 P7 closure file, a measured-closure module (without D5), a frozen wire family, DB10 or a budget would have to change.
- The operator-recorded VOID path is absent or would need a new family: NEEDS_CONTEXT (D9).
- The image store cannot verify the child or config identity: NEEDS_CONTEXT.
- A §4 case cannot be made to fail on the base.
- Two failed corrections of the same issue (AGENTS.md).
- **Operator review-round rule (2026-10-02):** after more than three review rounds that each return two or more P1/P2 findings, the executor stops folding; the coordinator adjudicates a rewrite or a narrower scope.
- **Single writer:** only the executor writes the identity branch; the coordinator integrates. A second writer appearing is a stop.

## 8. Out of scope and decision unlocked

**Out of scope:** the R1 Linux run (§9); lane D step 3 (§11); B4 (before T06 dispatch, not R1: PR #610); the three qualification-path items (#611, merge-held); R2; any production use.

**Unlocked:** with Windows evidence RESOLVED and the Codex relay clean, the coordinator folds the C′ and VALID→VOID cases into R1's node set and asks the operator for the R1 grant.

## 9. R1 Linux combined node set (separate grant; coordinator-held)

Not this card's work. Recorded so the freeze and the R1 dispatch agree:
- **Order (ruling 5, `:1996-2004`):** service → N1 → N2 → Part A → result/seal → supervision last, plus the C′ and VALID→VOID cases. Exact collected IDs and count are frozen at the R1 dispatch.
- **Grant:** R1's express Linux grant (operator), executed by the coordinator under its `ci.dispatch`.
- **Before R1:** C′ RESOLVED; the three qualification-path items (truncated-calendar validation, calendar-role binding, reviewer identity; ledger `:2031-2034`); T00-first integration; independent review.
- **Tooling gap (D6):** the workflow's modes are `s2`–`s5` (`.github/workflows/qualification-s2-supervision.yml:26`) and `scripts/s2_run_evidence.py` reads only S2–S5 scopes (`:101-102`). R1 needs a mode and a scope: a CI-configuration change.
- Every R1 packet cites the residual, the expected identity contract and the observed coverage.

## 10. Audit hooks (runnable)

```bash
# Card form and authority. Expected: RESULT: well-formed; exit 0.
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-02-h9-cprime-runtime-identity-build-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-02-h9-cprime-runtime-identity-build-DRAFT.md
# Premise (Git Bash), in the executor worktree; BASE is the D1 answer.
git rev-parse HEAD; git merge-base --is-ancestor c3ab0cc HEAD && echo "descends from c3ab0cc"
git diff --stat c3ab0cc origin/main -- ops tools deploy   # expected: empty as of 6de7bf9
test ! -e .env && echo "no .env" || echo "FAIL: .env present"
# Image build is tag-resolved today (the line C′ replaces).
grep -n "slim-bookworm\|RepoDigests" ops/c1_rail/qualification/execution/image.py
# Measured-closure re-check at return (0 differences expected unless D5).
python -I scripts/fp.py python <scratch>/stage1c_closure_table.py . "$BASE" HEAD
# Scope at return.
git diff --stat "$BASE"...HEAD
```

## 11. Lane D step 3 (separate card; this block does not dispatch it)

Recorded so the step-2 freeze does not absorb it. Dispatch waits for term 8's merge (PR #610) and a card of its own.
- **Term 8, joint-batch validator reconciliation (pending #610).** The canonical joint-batch policy governs: the S4 joint N2/PART_B ruling, `policy.required_output_roles`, and campaign spec E03 (`docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md:212`). The three T05 seams on `f237178` (`campaign_result.parse_receipt_row` `:161`, `_row_outcome` `:204`, `parse_campaign_result` `:298`) accept every authentic complete prefix the policy allows: PASS,PASS,FAIL,PASS; PASS,PASS,FAIL,FAIL; PASS,PASS,PASS,FAIL. Unchanged: wire shape, stage order, membership, families and operations, and every prior-checkpoint failure constraint (a FAIL before the joint batch ends the campaign). Test split (corrected 2026-10-02 after the Codex source review of #614):
  - **New red→green regressions:** PASS,PASS,FAIL,PASS and PASS,PASS,FAIL,FAIL. Each is refused at `f237178` and accepted after the fix.
  - **Preservation cases, which must stay green before and after:** PASS,PASS,PASS,FAIL, already accepted, since `parse_receipt_row` permits earlier PASSes plus a final FAIL and `_row_outcome` permits exactly a last FAIL. Also every other existing legal shape, and every pre-joint-batch FAIL, which still ends the campaign. No red evidence is fabricated for a preservation case.
  - **Downstream seam to check:** if the authentic all-four-prefix commit, receipt and reopen exposes a further defect past the three validators, name that seam specifically (for example `parse_campaign_result`'s repeated constraint at `:330-347`, or the receipt reconstruction on reopen) and return it to the coordinator. Don't widen scope silently.
- **Result-role funding.** `result_g5` (RESULT) and `seal` (SEAL) works reserve from the canonical funding (`reserve_result_work` `campaign_result.py:769`, `reserve_seal_work` `campaign_seal.py:146`): reservation, settlement, exhaustion refusal and no renewal, against the original allowance and deadline.
- **TEST_ONLY result-fault cases.** Fault injection on the result/seal path under TEST_ONLY (crash cuts around T1/T2, IN_DOUBT, duplicate and conflicting requests, VOID races). The exact list is fixed at D7.
- **Single writer:** step 3 edits `campaign_result.py`, which step 2 also edits. Sequential, not parallel (D7).

## 12. Open decisions (for the coordinator at freeze)

- **D1 Base.** `f237178` as it stands (on `c3ab0cc`), or the H9 head updated onto current `main`. `f237178` is not on `origin`; it must be pushed (a `codex/*` branch) before a fresh worktree can be cut.
- **D2 Release binding form.** A new release revision beside `/v7` in `release_schema.py`, or a separate signed runtime-identity document whose digest the release carries. Both appear to touch `release_schema.py`, a measured-closure module; finding (d) confirms. Recommended: get the operator's C3-rule ruling at freeze, not mid-build.
- **D3 Pin file** path and format.
- **D4 Final allowed file list.**
- **D5 Measured-closure edits.** Whether the operator admits changes to `release_schema.py`, `runtime.py`, `worker.py`, `campaign_probe.py` or `protocol.py`, and with what re-measurement.
- **D6 R1 tooling.** Who builds the R1 workflow mode, evidence scope and selector, under which grant.
- **D7 Step 3.** Its exact TEST_ONLY result-fault list and result-role funding cases; sequential after step 2 (recommended) or behind a file boundary.
- **D8 P7 closure list.** The coordinator attaches the 40 first-party module paths from the accepted record (`docs/briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md:742-749`) so item 13 is executable by the worker.
- **D9 Operator-recorded VOID path.** If finding (c) shows it absent or needing a new record family, who designs it and whether the operator rules first.
- **D10 PR authority.** This draft withholds `pr.open` (the H9 card lists it at `:584`); the coordinator opens PRs.

## Coordinator resolutions, 2026-10-02

These resolve D1–D10 for dispatch. Joshua's direct go for lane D was given in the Codex chat on 2026-10-02. D5 is ruled yes, so the build may be dispatched once step 1 (push and archive) is done.

- **D1 Base.** H9 pushes `f237178` as a `codex/*` branch (lane D step 1). It then **merges current `main`** at build start and reports the range-diff and the Stage 1c 68/63 result before any C′ code. `main` now includes T00 (`c3ab0cc`), #600, #601, #584 and later merges.
- **D2 Release binding.** A new release revision, **`/v8`**, beside `/v7` in `release_schema.py`. It binds the base-pin hash, the built worker image ID, the finite entrypoint mapping and the expected identity tuples. Historical parsers `/v1`–`/v7` stay as they are, and the binding flows through the existing `release_sha256`.
- **D3 Pin file.** `tools/qualification_verification/worker-base-image.json`. It has a closed schema: platform `linux/amd64`, Python `3.12.3`, base `python@sha256:afc139a0a640942491ec481ad8dda10f2c5b753f5c969393b12480155fe15a63`, the selected child `sha256:fd3817f3a855f6c2ada16ac9468e5ee93e361005bd226fd5a5ee1a504e038c84`, the config `sha256:cf001c2f8af7214144935ae5b37c9e626ccf789117c10c1f691766d4658f1b1e`, and an approval-provenance pointer to the ledger's C′ rulings entry.
- **D4 Allowed files.** The card's list, plus the D3 pin file. The measured-closure files listed under D5 are allowed only if Joshua admits them.
- **D5 Measured-closure edits — RULED YES** *(Joshua, directly to the coordinator, 2026-10-02 ~23:20Z: "yes")*. The edits are admitted on the terms below. The re-measurement is a **proposed plan** only: the governing evidence is the actual measured acceptance taken after the last closure change, and nothing carries before it. The proposal is to admit C′ edits to `release_schema.py`, `runtime.py`, `worker.py`, `campaign_probe.py` and `protocol.py`. Trigger 1 has already fired from T00, so the cost is **one** fresh S5 Part A measurement, run before the combined R1 once all closure-changing work has landed (C′, term 8, #611, K3/RC-4) (ledger finding of 2026-10-02, #613).
- **D6 R1 tooling.** The R1 workflow mode, evidence scope and selector are built by a **separate coordinator-dispatched worker**, not this lane, after C′ lands. A `.github/workflows` change needs Joshua's CI-configuration approval.
- **D7 Step 3.** Runs **after** step 2, on the same branch, **under its own separately frozen step-3 card** (§11). This card's §2 file list and out-of-scope limits still govern step 2, so nothing here authorizes step-3 files. The funding module, for example, isn't in §2. The step-3 card will carry term 8's test split (§11), the `result_g5`/seal funding roles, and the TEST_ONLY result-fault cases. Those cases are: a bootstrap-frozen immutable fault; a durable T1 pre-sign hold; the fault absent in normal runs; an exact retry with no renewed key, time, payload or budget; the real T1 consumer; and startup, funded hold and recovery, exhaustion, and VOID. Dispatch waits for #610 to merge and for that card to be frozen.
- **Phase-0 dispositions (2026-10-02, after the lane-D read-only return):**
  - **Step 2 maps existing entrypoints only.** That means the runner/admin fixture, the service supervisor, guardian/control/probes, and the N1, N2 and PART_A G5 launches.
  - **`result_g5` and qseal are not provisioned under this card.** `result_g5` currently reuses `g5_unit_spec`. qseal's `exchange` refuses; there is no seal uid or socket, it is absent from the bootstrap whitelist, and it has no `role_policy` role.
    - **Their inclusion is still owed BEFORE the combined R1.** The accepted R1 finite-map obligation is not narrowed just because they don't exist yet. Each must have its provisioned producer and identity checks reviewed and merged before R1 is granted.
  - **Interpreter identity producers are in scope.** The pre-spawn, child-reported and post-exec producers for interpreter bytes, base interpreter, `pyvenv.cfg` and the `.pth` inventory are in scope. Today `runtime.py` checks only version, platform, locks and source.
  - **Pin linkage.** The pin-metadata producer verifies index → selected linux/amd64 child → config digest linkage, and the declared platform and patch, separately from the built image ID. `image.py`'s tag/RepoDigest path is not accepted as proof. This is an added acceptance check.
  - **D9 is open.** No protected operator-recorded mismatch VOID path exists: VOID `/v1` and `/v2` carry only a reason plus approval bytes. The proposed design is [`docs/notes/2026-10-02-d9-identity-mismatch-void-design.md`](../../notes/2026-10-02-d9-identity-mismatch-void-design.md): a `CampaignStore.void` chokepoint, store-built content-addressed mismatch events, a signed-reason acknowledgement, stickiness, and the no-PASS fence. It needs no protocol, receipt or key-policy change, and no measured-closure edit. **No code until Joshua rules on R-1–R-8 and this card is re-reviewed.**
  - **Re-measurement.** A fresh S5 Part A measurement runs after the FINAL closure change, with no carry.
- **D8 P7 closure (40 first-party paths; none may change).**
  - `core/`: `dd_geometry.py`, `dd_protection.py`, `firm_rules.py`, `historical_challenge.py`, `lib/atomic_io.py`, `lib/mvd.py`, `lib/validation.py`, `lifecycle.py`, `mc/__init__.py`, `mc/ingest.py`, `mc/modes.py`, `mc/preflight.py`, `mc/simulation.py`, `tv_schema.py`.
  - The namespace `lib`.
  - `ops/c1_rail/`: `__init__.py`, `book_policy.py`, `book_schedule.py`, `ed25519_verify.py`.
  - `ops/c1_rail/qualification/`: `__init__.py`, `blocks.py`, `clock.py`, `contract.py`, `model.py`, `p7_driver.py`, `p7_evidence.py`, `panel.py`, `paths.py`, `production_source.py`, `regime.py`, `replay.py`, `runner.py`, `sessions.py`, `trust_domain.py`.
  - `ops/c1_signal_daemon/`: `__init__.py`, `book_adapters.py`, `book_protocol.py`, `feed.py`, `pine_ta.py`, `tv_broker_emulator.py`.
- **D9 Operator-recorded VOID path.** The Phase-0 check comes first. If the path is absent, or needs a new record family, **stop and return** to the coordinator. The coordinator designs it and Joshua rules before any build.
- **D10 PRs.** The coordinator opens them. The worker pushes the `codex/*` branch only.

## Pre-mortem (README rule)

- **Loop cost:** one Windows build loop and its records; no Linux run.
- **Decisions the executor will hit:** D2, D5 and D9. They are ruled in one batch at freeze.
- **What makes it moot:** an operator ruling that withdraws the R1 C′ gate, or a pin change.
- **Measurements the return fills in:** Phase-0 findings (a)–(e), the per-case records and the closure re-check.
