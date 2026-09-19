# Codex handoff — Protected Full E1 / S2-R2b: fund private scheduler work before construction (warm installed service, operator-local client)

**Type:** cc_handoff (frozen-spec implementation; Codex variant with parent-recommended defaults)
**Date:** 2026-09-19
**Status:** dispatch now — assigned by the operator on 2026-09-19 after the [B0 decision](../../superpowers/plans/2026-09-19-attended-batch-qualification.md#b0-decision--2026-09-19) to retain the protected service. Supersedes the "R2b is UNASSIGNED / STOP AT R2a" stop in the [execution-slices ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md) for R2b only; R3, R4, Linux acceptance and S3–S8 stay stopped.
**Spawn target:** Codex — cloud or local at the coordinator's choice; the default executor identity is the existing S2/R2 writer named by the [R2 contract](2026-09-19-full-e1-s2-r2-funded-scheduler.md) (sole writer of `service.py`, `campaign_store.py`, `campaign_funding.py`, `campaign_supervisor.py`, `profile.py`, `release_schema.py`). A Claude Code cloud session is admissible for Steps 2.1–2.5 and 2.7 only; Step 2.6's real-host half needs the enrolled Linux host on any surface. Branch `codex/full-e1-s2-r2b-warm-scheduler` stacked on `codex/full-e1-s2-supervision@8aa5753`; PR targets that branch; no merge.
**Parent:** [S2-R2 contract and R2a acceptance](2026-09-19-full-e1-s2-r2-funded-scheduler.md) (the frozen spec) · [coordinator handoff §S2-R2](2026-09-19-full-e1-coordinator-handoff.md) · [execution-slices plan, S2 + ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md) · [governing spec §2.5–2.6](../../superpowers/specs/2026-09-17-protected-full-e1-campaign.md). Parent adjudicates with fable-judge, then Codex review; the root coordinator accepts.
**Authority:** code, tests, harness selection and the ledger append only. No new allowance (the 20 s orchestration charge and its guardian 14 / START_OWNER 2 / START_CLIENT 2 / RECOVERY_OWNER 2 decomposition are fixed), no R3 or R4 repair, no Linux provisioning spend, no installed-release activation on a real host, no statistical dispatch, no publication of S2 acceptance, no merge. A `DONE` status supplies no permission.

## 0. Rule 0 reads (Phase 0 — post the read-report before writing code)

Currency: `git fetch origin codex/full-e1-s2-supervision main`; record both SHAs. At authoring `codex/full-e1-s2-supervision` was `8aa5753eac8a533e1921c2b796c00cb376513614` (merge of `main@97d0319` into the S2 candidate; contains R2a commit `966b9f6`) and `main` was `97d0319` (PR #428, S1 accepted). Hard checks: `git merge-base --is-ancestor 97d0319 8aa5753` exits 0; `git ls-tree --name-only 8aa5753 tests/ops/qualification/execution/ | grep -c test_campaign_scheduler.py` prints `0` (the R2b regressions are unpublished — §0.5 (A)); `grep -c "STOP AT R2a" docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md` prints `1`. Anchor every file with `git log -1 --format=%h -- <path>` in the report; all anchors below are at `8aa5753`.

- `docs/briefs/handoffs/2026-09-19-full-e1-s2-r2-funded-scheduler.md` @ `966b9f6` — the frozen spec: "Proposed interfaces and transaction contract" items 1–5, "Accounting, failure and timer behavior", "Required regressions and acceptance", "Coordinator review constraints before implementation", "R2a implemented interface and verification boundary" (quote the R2b sentence beginning "R2b must replace the unfunded per-request scheduler" verbatim).
- `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md` @ `966b9f6` — S2 slice, contract decisions 2 and 5, ledger entries "Successor coordinator checkpoint — S2-R2 funding interface" and "Coordinator acceptance — S2-R2a persistence" (the R2a fingerprint `0ec013d2…` and the three final record IDs), and the closing "STOP AT R2a" line.
- `docs/briefs/handoffs/2026-09-19-full-e1-coordinator-handoff.md` @ `292f283` — §"S2-R2 — reserve before scheduler/bootstrap campaign work" and "Shared decisions that successors must preserve".
- `docs/superpowers/plans/2026-09-19-attended-batch-qualification.md` (this PR) — §"B0 decision — 2026-09-19": the narrowing this handoff applies (operator-local client only; single-lifetime posture; no batch entrypoint).
- `ops/c1_rail/qualification/execution/campaign_funding.py` @ `966b9f6` — `WORK_PHASES` :25, `scheduler_status` :256-263, `claim_scheduler_bootstrap(request_bytes, clock_bytes) -> (token | None, status)` :265-315 (exact duplicate returns no token :271-274; terminal overlay :297-305; pending debit :312-313), `materialize_scheduler_bootstrap(attempt_id, work_id, owner_token, host_run_id) -> (reservation_bytes, enrollment_bytes)` :317-356 (retains START_INTENT, START_OWNER control object and enrollment atomically; `funding_transfer`), the compact request parser it calls at :266 (report its schema literal and field set), `_funding_gate`.
- `ops/c1_rail/qualification/execution/service.py` @ `966b9f6` — `handle_request` :123-210, `_campaign_request` :212-278, `_diagnostic_campaign_request` :280-325 (`dispatch_lock` + `controller_cpu_guard()` :284; `begin_admission` :293; post-admission VOID :305-324 — R3, untouched), `schedule_campaign_probe` :327-359 (**the unfunded path this handoff retires**: `RLIMIT_CPU` check :333, process-wide `arm_boottime_deadline` :338, reservation bytes built :341-354 before `reserve_work` :355, `run_campaign_work` :359), `recover_service` :481-523 (v3 funding rows → `FUNDING_PENDING`, no auto-materialization :493-495), socket/threads :525-567, `main` :570-576.
- `ops/c1_rail/qualification/execution/campaign_supervisor.py` @ `966b9f6` — `prepare_campaign_work` :89-118, `guardian_unit_spec` :121-154, `run_campaign_work` :261-286 (the tail to split), `LinuxCampaignRuntime` :365-443 (`_control` :388-427, `launch_gate` use, `acknowledge_dispatch`), `arm_boottime_deadline` :596-598, `controller_cpu_guard` :604-629, `_assert_authority` :640-647, `guardian_main` :673-762 (profile/v3 requirement :692; construction before the timer :691-707 — R4, untouched).
- `ops/c1_rail/qualification/execution/campaign_store.py` @ `966b9f6` — `retry` :43-52, `launch_gate` :177-220, `acknowledge_dispatch` :222-243, `begin_admission` :621-676, `reserve_work` :729-808, `_check_budget` :597-602, `_save_budget` :569-585, `FundingStore` base :29-32.
- `ops/c1_rail/qualification/execution/release_schema.py` @ `966b9f6` — `parse_release` :22-111: campaign releases forced `FULL_E1`/`TEST_ONLY`/`dispatch_enabled=False` :34-37; **profile/v4 refused** :47-48 (`'funding profile is persistence-only; runtime release not enabled'`) — the activation gate Step 2.4 opens.
- `ops/c1_rail/qualification/execution/profile.py` @ `966b9f6` — `parse_profile` :54, `parse_campaign_budget_profile` :84, `diagnostic_*` producers :123-155 and the `funded_diagnostic_execution_profile` producer (report its name/line).
- `ops/c1_rail/qualification/execution/campaign_protocol.py` @ `292f283` — `permitted` :45-47 (client: SUBMIT_E1/STATUS/FETCH_PLAN_CHUNK; g5: STATUS; operator: STATUS/VOID) — unchanged by this handoff.
- `ops/c1_rail/qualification/execution/runtime.py` @ `8aa5753` — `ENTRYPOINTS` :16-18, `source_closure` :26-64, `measure_runtime` :98-136 (startup import inventory lives here).
- `deploy/qualification/bootstrap.py` @ `292f283` — closed role set (:15) and `campaign_control` (:20-35).
- `tests/integration/qualification_boundary/campaign_driver.py` @ `292f283` — the per-request scheduler: `ExecutionService(...)` constructed :26 before `schedule_campaign_probe` :27 — removed by Step 2.6.
- `tests/integration/qualification_boundary/conftest.py` @ `292f283` — `RAW_DRIVER` :29-45 (a per-call Python exec), `raw_request` :82-85, `FP_QUALIFICATION_S2` :51; `tests/integration/qualification_boundary/test_campaign_supervision_linux.py` @ `292f283` — the seven S2 cases and `probe()` (`systemd-run … LimitCPU=1` per the R2 contract).
- `tests/ops/qualification/execution/test_campaign_funding.py` @ `966b9f6` — line 8 `from test_campaign_scheduler import schedule`: the import that makes the module uncollectable on the published branch (CI `Tests` run 35439558971 failed at collection inside `tests/ops/test_qualification_isolation.py::test_qualification_suite_in_clean_process`).
- `tests/ops/qualification/execution/test_campaign_supervision.py` @ `966b9f6` — :1 and the autouse `simulated_control_timer` :16-21 (persistence tests replace `controller_cpu_guard`; never kernel evidence); `test_service.py` @ `966b9f6`; `lifecycle_model.py` @ `966b9f6`; `tests/ops/qualification/invariant_manifest.json` @ `292f283` (the seven S2 node IDs under `QEXEC-01`); `scripts/qualification_boundary_verification.py` @ `292f283` (`--s2` selection :82-99).

## 0.75. Local-only dependency check

`N/A for cloud or local dispatch — no gitignored vendor data, no secrets.` Two environment facts are not vendor data but still gate where steps can run: (1) the checkout launcher (`./fp.ps1` on Windows; `python -I scripts/fp.py --env <ops-env>` on Linux) and its locked operations environment (Python 3.13.2, 62 locked packages on the operator's host) — record the interpreter actually used; a hosted 3.11/3.12 interpreter is acceptable for Steps 2.1–2.5/2.7 if `doctor` passes there, and must be reported as such; (2) Step 2.6's real-host half requires the enrolled disposable Ubuntu 24.04 host (root, cgroup v2, Docker 28.0.4, systemd/busctl/polkit, `FP_QUALIFICATION_HOST_MANIFEST`, `FP_QUALIFICATION_S2=1`). Without it, return with `Linux acceptance pending` stated exactly — never a Windows/mock result described as Linux evidence.

## 0.5. Clarifications — parent-recommended defaults (apply unless Phase 0 contradicts; then bounce `NEEDS_CONTEXT` quoting the conflict)

- (A) **The 15 red R2b regressions are unpublished.** They exist only as `tests/ops/qualification/execution/test_campaign_scheduler.py` in the operator's checkout `C:/Users/joshu/.codex/worktrees/full-e1-s2-supervision/multi_firm_operations` (record `20260919T100953Z-42977cf0e724`, 15 failures). Default: if the file is present in your checkout, use it byte-for-byte and record its SHA-256; if absent, write the regressions fresh from the R2 contract's "Required regressions and acceptance" list (nine bullets) plus the two "Coordinator review constraints" cases (expiry discovered at each clock sample; competing duplicate around commit), name the file the same, and return `DONE_WITH_CONCERNS` noting that the red-test identity differs from the local record. Either way the file is published in this PR.
- (B) **CI stays red until R2b is green.** `test_campaign_funding.py:8` imports the scheduler test; with the file present the module collects, but its 15 tests are red by contract, so `tests/ops/test_qualification_isolation.py` fails until Step 2.5 turns them green. Default: do not mark them xfail/skip, do not move the import, do not gate them behind an environment variable; make them pass.
- (C) **Producer wiring.** The private route calls `claim_scheduler_bootstrap` first; only a returned token proceeds to `materialize_scheduler_bootstrap`, then to the split launch tail. No `reserve_work` call from the route (materialization already transfers the exact reservation). Exact duplicates get `scheduler_status` (historical) and never a second claim. Default: keep `schedule_campaign_probe`'s body only as the internal tail after materialization, or delete it — report which; nothing may still reach `reserve_work` before funding.
- (D) **Release activation.** `release_schema.py:47-48` refuses profile/v4. Default: add one execution-capable diagnostic release revision (schema `qualification_execution_release/v4` or the next closed literal the executor reports) pairing execution profile/v4 + budget profile/v3 + snapshot/v5; campaign releases remain `FULL_E1`/`TEST_ONLY`/`production_execution=False`; `dispatch_enabled` stays `False` (statistical checkpoints remain disabled — probes only); v1/v2/v3 parsing unchanged; `guardian_main` :692 accepts the new revision. Fresh attempts only — never backfill v3 diagnostic attempts into v4 funding.
- (E) **Peer identity and preload.** The schedule schema is routed in `handle_request` only when `SO_PEERCRED` uid equals the configured `service_uid` and the installed release eligibility was cached at startup; all campaign-specific modules (`campaign_store`, `campaign_supervisor`, `campaign_funding`, `admission`, `plan`, `source_admission`) are imported at service startup, never lazily on first request. Default: assert this with a first-request import fault test (R2 contract bullet 8).
- (F) **Timer ownership.** Default: an owned timer context (`with owned_boottime_deadline(deadline):` or equivalent) retired in `finally` on success, exception and historical-duplicate paths; `controller_cpu_guard` (1 s thread CPU / 10 s BOOTTIME) wraps the whole active tail and consumes START_OWNER's existing 2 s allowance. No process-wide `arm_boottime_deadline` from the request path. This does not claim to cover R4's pre-bootstrap interval.
- (G) **Harness transport (B0 narrowing).** Default: the harness's private-route caller is an already-initialized transport child (fork after generic socket/framing modules are preloaded; qexec credentials set before opening the socket; one pre-encoded frame in, one reply out), and the only campaign *submitter* exercised anywhere is the local admin client acting in the existing `client` role over the Unix socket. `RAW_DRIVER` may remain for public historical STATUS/FETCH/VOID retries; it may not carry the schedule schema. Delete `campaign_driver.py`. If the harness identity or process constraints make the fork child impossible, return `NEEDS_CONTEXT` with the exact constraint — do not substitute another per-request Python scheduler.
- (H) **Branch/PR.** Default: `codex/full-e1-s2-r2b-warm-scheduler` from `8aa5753`; PR against `codex/full-e1-s2-supervision`; the coordinator decides whether to fold it into #429 or merge after #429.

## 1. Context and deliverables

R2a delivered the persistence half of the accepted R2 contract (DB v7 compact funding, one-use `PENDING → MATERIALIZED` bootstrap intents, pending/terminal barriers, offline integrity) and was locally accepted on 2026-09-19; the ledger then stopped at "R2b is UNASSIGNED". The runtime half is still the S2 blocker B1: in the published candidate, `campaign_driver.py:26-27` constructs `ExecutionService` per request before `schedule_campaign_probe`, and `schedule_campaign_probe` itself builds reservation bytes and arms a process-wide deadline before `reserve_work`, so repeated import/construction failures and duplicate requests are never charged to the campaign lifetime. B0 (2026-09-19) compared finishing this service against an operator-launched batch and retained the service, narrowing the first attended release to an operator-local client and a single-lifetime posture; that narrowing is applied here and removes the remote-transport half of the original R2b scope.

**Six-field summary (execution-slices convention):**
- **Selected outcome:** The installed, already-running `ExecutionService` is the sole campaign intent producer. A private scheduler request cannot import campaign-specific code, construct campaign context or a `LinuxCampaignRuntime`, or cause any OS lifecycle effect until `claim_scheduler_bootstrap` has durably funded its one-use controller operation from the original allowance; repeated failures and duplicates obtain no free work and no new allowance; the only campaign submitter is the local operator/admin client.
- **Prerequisites:** `codex/full-e1-s2-supervision@8aa5753` (R1 and R2a locally accepted; R2b tests unpublished — §0.5 (A)); the B0 decision recorded in this PR; the R2 contract accepted for implementation ("Coordinator accepted this contract for implementation"). Real Linux evidence is not a prerequisite for the local return.
- **Ownership:** one R2b writer (§Spawn target); root coordinator accepts R2b, S2 and combined E1; no parallel writers on `service.py`, `campaign_store.py`, `campaign_funding.py`, `campaign_supervisor.py`, `profile.py`, `release_schema.py`, `journal_snapshot.py`.
- **Verification:** §2 gates and §10 hooks through the checkout launcher; source-stable, capture-complete records; `git diff --check`.
- **Checkpoint:** after Phase 0 and before runtime edits, return the exact pre-funding boundary — the ordered list of everything that executes between socket accept and `claim_scheduler_bootstrap`'s commit (framing, peer-cred, schema parse, indexed historical comparison, compact projection read) with its byte/CPU bound — and the service-startup import inventory. Return immediately on: any need to enlarge the controller allowance; any R1 ownership/acknowledgement conflict; inability to keep pre-intent preparation genuinely cheap and bounded.
- **Return boundary:** R2b only. Excludes R3 (VOID authentication accounting), R4 (pre-bootstrap absolute deadline), Linux S2 acceptance, S3–S8, production authority, provisioning, activation, merge.

**Deliverables (one PR):**
1. `tests/ops/qualification/execution/test_campaign_scheduler.py` — published; green at return (Step 2.1, 2.5).
2. `ops/c1_rail/qualification/execution/service.py` — startup preload + cached eligibility; `service_uid`-only schedule route; funded producer call chain; owned timer context; `schedule_campaign_probe` retired or reduced to the post-materialization tail (Steps 2.2, 2.3, 2.5).
3. `ops/c1_rail/qualification/execution/campaign_supervisor.py` — `launch_prepared_campaign_work(context, reservation_bytes, enrollment_bytes)` split from `run_campaign_work`; construction strictly after commit (Step 2.3).
4. `ops/c1_rail/qualification/execution/release_schema.py`, `profile.py`, `release.py` (+ `campaign_funding.py` / `campaign_store.py` only where the producer chain needs a narrow accessor) — execution-capable diagnostic release revision (Step 2.4).
5. Harness: `tests/integration/qualification_boundary/conftest.py` (bounded transport child for the private route), delete `campaign_driver.py`, `test_campaign_supervision_linux.py` selection by explicit `work_id`, `tools/qualification_verification/campaign_host.py` admin submit path if a local operator client helper is needed (Step 2.6).
6. Tests updated, never deleted: `test_campaign_funding.py`, `test_campaign_supervision.py`, `test_service.py`, `test_release.py`, `test_profile.py`, `lifecycle_model.py` as affected; `invariant_manifest.json` node IDs updated only if a registered S2 node is renamed (Step 2.7).
7. Ledger append in `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md` ("S2-R2b executor return"), delivered not self-accepted (Step 2.8).

**Not asked:** R3 (`service.py:305-324` stays unmetered), R4 (`guardian_main` :691-707 ordering stays), the governing spec, the R2 contract text, `campaign_protocol.permitted`, any batch entrypoint or new bootstrap role, the N1_ONLY route, `store.py` schema, statistical checkpoints, any real-host provisioning, any change to phase ceilings or the 20 s orchestration charge, the B0 plan document.

## 2. Execution plan — the frozen spec

### Step 2.1 — Red baseline and collection repair
- **Inputs:** §0.5 (A); `test_campaign_funding.py:8`.
- **Action:** place `test_campaign_scheduler.py`; run `./fp.ps1 doctor` (or the Linux launcher) then `python -m pytest tests/ops/qualification/execution/test_campaign_scheduler.py tests/ops/qualification/execution/test_campaign_funding.py -q --tb=short` and retain the record: funding tests pass, scheduler tests fail (expected 15 failures, or the re-derived count with the discrepancy stated). Confirm `python -m pytest tests/ops/qualification/execution --collect-only -q` reports zero collection errors.
- **Per-step gate:** collection clean; the red record retained with its ID; `DONE_WITH_CONCERNS` if the file was re-derived.

### Step 2.2 — Closed private route in the warm service
- **Inputs:** the R2a compact request parser (§0 `campaign_funding.py:266`); `service.py:123-210`, `:525-567`.
- **Action:** route the schedule schema in `handle_request` after `SO_PEERCRED` uid == `service_uid` and startup-cached eligibility; bound request bytes explicitly; reject malformed/oversize/extra-field requests in framing; preload every campaign-specific module at `ExecutionService.__init__`/`main` startup; never construct a second `ExecutionService` for a request. Other release versions reject the route; public v1/v2 STATUS/FETCH/VOID retries keep their behavior.
- **Per-step gate:** the non-service-peer, malformed/oversize and first-request-import-fault regressions pass; `grep -n "import" ops/c1_rail/qualification/execution/service.py` shows no request-path lazy import of `campaign_supervisor`/`campaign_store`/`campaign_funding`/`admission`/`plan`.

### Step 2.3 — Funded producer and split launch tail
- **Inputs:** `campaign_funding.py:265-356`; `campaign_supervisor.py:89-118, 261-286, 388-427`; `campaign_store.py:177-243`.
- **Action:** route → `claim_scheduler_bootstrap(request_bytes, clock_bytes)`; no token → return `scheduler_status` (historical or terminal) with no effect; token → `materialize_scheduler_bootstrap(attempt, work, token, host_run_id)` → `launch_prepared_campaign_work(context, reservation_bytes, enrollment_bytes)`, which consumes the committed enrollment without claiming START_OWNER again, constructs `LinuxCampaignRuntime` only now, and runs the existing R1 `launch_gate` → physical start → `acknowledge_dispatch` sequence unchanged. Inject repeated `LinuxCampaignRuntime` construction failure after materialization: exactly one invocation per request; reservation/START_OWNER/START_INTENT durable before it; reopen and duplicate neither retry nor refund; the existing R1 recovery path settles or blocks.
- **Per-step gate:** concurrent identical requests → one claim, one materialization, one tail; changed role/probe/retry under the same work identity → conflict; crash before claim commit → nothing survives; crash after materialization → intent survives, duplicate is historical, positive authority obeys R1 barriers; insufficient CPU / expired deadline / changed boot / VOID / recovery pending / dispatch pending refuse before any construction or lifecycle effect (R2 contract bullets 2–6).

### Step 2.4 — Execution-capable diagnostic release revision
- **Inputs:** `release_schema.py:22-111`; `profile.py:54-155`; `release.py` install/verify; `guardian_main` :692.
- **Action:** per §0.5 (D). Old profiles remain historical-compatible; missing projection never self-heals outside first `BEGIN_ADMISSION` (R2a rule); `recover_service` reports `FUNDING_PENDING` for v4 attempts and still never auto-materializes.
- **Per-step gate:** `test_release.py`/`test_profile.py` pairing tests: v4 profile + v3 budget profile accepted only under the new release literal; every older literal still rejects v4 (`release_schema.py:47-48` semantics preserved for them); `test_campaign_funding.py::test_funded_profile_cannot_activate_old_release` still passes.

### Step 2.5 — Timer ownership and green R2b suite
- **Inputs:** §0.5 (F); `service.py:327-359`; `campaign_supervisor.py:596-629`.
- **Action:** owned timer context retired in `finally`; `controller_cpu_guard` over the active tail; retire `schedule_campaign_probe`'s process-wide `arm_boottime_deadline`. Run the full R2b file until green on source-stable bytes.
- **Per-step gate:** stale-timer regression (success, exception, historical duplicate leave no timer); all `test_campaign_scheduler.py` cases pass, zero skips; controller charge arithmetic, shared memory membership and recovery slots unchanged (existing `test_campaign_supervision.py`/`test_campaign_budget.py` cases still pass).

### Step 2.6 — Harness: bounded transport, no per-request scheduler, explicit work_id selection
- **Inputs:** §0.5 (G); `conftest.py:29-45, 82-85`; `campaign_driver.py`; `test_campaign_supervision_linux.py`; `scripts/qualification_boundary_verification.py:82-99`.
- **Action:** implement the transport child; delete `campaign_driver.py`; select the seven S2 cases' work by explicit `work_id`; make the local admin client the only submitter path. On the enrolled host only: verify peer UID on the private route, absence of any `campaign_driver` scheduler unit, one guardian start per work, common hierarchy membership, source/config identity and owned cleanup, through `scripts/qualification_boundary_verification.py --s2 --manifest …` with unconditional cleanup.
- **Per-step gate:** local: the harness unit tests for the transport child pass; `git grep -n campaign_driver -- tests tools ops scripts` returns nothing. Real host (if available): the seven S2 node IDs plus the new peer-UID/no-scheduler-unit cases pass with `source_stable=true`, `capture_complete=true`, cleanup success; otherwise the return states `Linux acceptance pending` and lists exactly which cases were not run.

### Step 2.7 — Verification selection on frozen bytes
- **Action:** from the checkout launcher, in this order, once on stable final sources:
  ```
  ./fp.ps1 doctor
  ./fp.ps1 --workers 2 python -m pytest tests/ops/qualification/execution/test_campaign_scheduler.py tests/ops/qualification/execution/test_campaign_funding.py tests/ops/qualification/execution/test_campaign_supervision.py tests/ops/qualification/execution/test_campaign_budget.py tests/ops/qualification/execution/test_campaign_recovery.py tests/ops/qualification/execution/test_campaign_admission.py tests/ops/qualification/execution/test_profile.py tests/ops/qualification/execution/test_release.py tests/ops/qualification/execution/test_service.py -q --tb=short
  ./fp.ps1 python -m pytest tests/ops/qualification/execution/test_lifecycle_model.py tests/ops/qualification/execution/test_artifact_acceptance.py tests/test_qualification_invariant_manifest.py tests/ops/test_qualification_isolation.py -q --tb=short
  ./fp.ps1 check
  git diff --check
  ```
  (Linux launcher: `python -I scripts/fp.py --env <ops-env> …` for each.) Record interpreter, source inventory, commands, exits, counts, skips and record IDs.
- **Per-step gate:** every command exits 0; zero skips in the first selection; `test_qualification_isolation.py` passes (the CI collection defect is gone and the child suite is green).

### Step 2.8 — Ledger append and return
- **Action:** append "S2-R2b executor return — <date>" to the execution-slices ledger after recorder closure: predecessor identity, changed interfaces (route schema literal, release literal, split tail name), exact records, Linux status, review findings, limitations. Do not edit the "STOP AT R2a" line (this handoff is the assignment that supersedes it; the coordinator rewrites the ledger disposition on acceptance). Open the PR per §0.5 (H) with the §6 status line, the record IDs and `git diff --stat 8aa5753...HEAD`.
- **Per-step gate:** ledger entry present; PR body contains the closure report format below.

## 4. Falsifiable hypothesis

**H:** the accepted R2 contract's runtime half is implementable inside the §1 deliverable surface, on `8aa5753`, without enlarging any allowance: after Step 2.5 no private scheduler request can cause a campaign-specific import, campaign context construction, `LinuxCampaignRuntime` construction, or an OS lifecycle effect before `claim_scheduler_bootstrap` has committed, and every one of the R2 contract's required regressions passes on source-stable records with zero skips.
**Reject if:** any surface outside §1 must change; the START_OWNER 2 s / 20 s orchestration bound must grow; the pre-funding boundary cannot be shown cheap and bounded (Checkpoint); `schedule_campaign_probe` or any harness path can still reach `reserve_work` or construct `ExecutionService` per request → return `BLOCKED — plan-itself-wrong`; the parent re-authors.
**Ambiguous-hold if:** a §0.5 default contradicts a Phase 0 read → `NEEDS_CONTEXT` quoting the conflict.

## 5. Forbidden moves

- Marking the 15 red tests `xfail`/`skip`, moving the `test_campaign_funding.py:8` import, or gating them behind an environment variable to turn the `Tests` workflow green before R2b is green.
- Enlarging the 20 s orchestration charge, START_OWNER's 2 s, or the 1 s / 10 s controller guard to make the warm handler fit — return `BLOCKED — plan-itself-wrong` instead.
- Reusing `conftest.raw_request`'s `RAW_DRIVER` (a per-call Python exec) for the private route, or leaving `campaign_driver.py` alive "for the Linux tests".
- Inheriting `schedule_campaign_probe`'s process-wide `arm_boottime_deadline`, or describing a relative timer as R4 coverage.
- Calling `reserve_work` from the route "as a fallback" when `claim_scheduler_bootstrap` returns no token — a refused claim is a historical status, never a second path to work.
- Backfilling existing v3 diagnostic attempts into v4 funding, or letting the new release literal accept `dispatch_enabled=True` or `production_execution=True`.
- Fixing R3 (metering post-admission VOID authentication) or R4 (deadline before guardian bootstrap) "while in there" — log the observation under `DONE_WITH_CONCERNS`.
- Describing Windows/mock/`simulated_control_timer` results as Linux enforcement, or claiming S2 acceptance.
- Editing the R2 contract, the governing spec, the B0 plan, `campaign_protocol.permitted`, or the "STOP AT R2a" ledger line.
- A "while I was in there" refactor of `campaign_store`, `journal_snapshot`, or the cyclic-import graph among the S2 modules (report it; do not restructure).

## 6. Gate and return taxonomy

RESOLVED = every Step 2.x gate met; §2.7 records complete with zero skips in the first selection; `test_qualification_isolation.py` green; `git diff --stat 8aa5753...HEAD` confined to the §1 surface; Linux status stated exactly (run with records, or pending with the unrun cases listed). FALSIFIED = a §4 reject fired (report; do not work around it). AMBIGUOUS = a §0.5 conflict.

Return exactly one of `DONE` · `DONE_WITH_CONCERNS` · `NEEDS_CONTEXT` · `BLOCKED — context-problem | capability-problem | scope-problem | plan-itself-wrong`.

```
Status: <DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED — <sub-case>>
Predecessor: 8aa5753eac8a533e1921c2b796c00cb376513614 (verified <date>)
Per-step gates: 2.1 [..], 2.2 [..], 2.3 [..], 2.4 [..], 2.5 [..], 2.6 [local ..; linux run|pending], 2.7 [..], 2.8 [..]
Pre-funding boundary (Checkpoint): <ordered list + bound>
Interpreter / launcher: <path, version, locked-package count>
Records: <IDs, counts, skips, source_stable, capture_complete>
Diffs (files touched): <list>
Branch / PR: <ref / URL>
Concerns surfaced (if any): <list>
Next action recommended: <one sentence>
```

## 7. Parent-session review

**Pass 1 — spec compliance:** diff confined to the §1 surface; no R3/R4 edits; no allowance change (`grep -n "orchestration_cpu_ns\|LimitCPU" …` values unchanged); `campaign_protocol.permitted` unchanged; no xfail/skip added; `campaign_driver.py` gone; the new release literal forces `dispatch_enabled=False`; the ledger append is a return, not an acceptance.
**Pass 2 — quality (fable-judge):** re-run §2.7 from the coordinator's launcher on the returned bytes; read the route for the exact pre-funding boundary and compare with the Checkpoint list; read `launch_prepared_campaign_work` for construction-after-commit and single START_OWNER use; read the timer context for `finally` retirement on all three paths; confirm `recover_service` still never auto-materializes; confirm every claim about Linux carries a record ID or reads "pending".
**Pass 3 — consolidated read (multi-step):** route + producer + tail + release revision + harness together: one request → one claim → one materialization → one tail → one guardian; duplicates and crashes at each boundary; then independent Codex review of the PR. Acceptance of R2b, S2 and E1 remains the root coordinator's; this review supplies no permission.

## 10. Audit hooks

```bash
# Predecessor and ancestry
git rev-parse codex/full-e1-s2-supervision            # expect 8aa5753eac8a533e1921c2b796c00cb376513614 at dispatch
git merge-base --is-ancestor 97d0319 8aa5753 && echo ancestor-ok
# The unpublished-test defect is closed and collection is clean
git ls-tree --name-only HEAD tests/ops/qualification/execution/ | grep -c test_campaign_scheduler.py   # expect 1
python -m pytest tests/ops/qualification/execution --collect-only -q | tail -1                        # expect no "error"
python -m pytest tests/ops/test_qualification_isolation.py -q                                          # expect pass
# No per-request scheduler or unfunded path remains
git grep -n "campaign_driver" -- tests tools ops scripts                                               # expect nothing
git grep -n "schedule_campaign_probe" -- ops tests tools                                               # expect only the post-materialization tail, if retained
git grep -n "reserve_work" -- ops/c1_rail/qualification/execution/service.py                           # expect nothing on the request path
# Allowance and role model unchanged
git diff 8aa5753...HEAD -- ops/c1_rail/qualification/execution/campaign_protocol.py | wc -l            # expect 0
git diff 8aa5753...HEAD -- ops/c1_rail/qualification/execution/profile.py | grep -n "orchestration_cpu_ns\|120\|300\|20" # ceilings unchanged
# Release activation gate
grep -n "persistence-only; runtime release not enabled" ops/c1_rail/qualification/execution/release_schema.py   # still present for the older literals
# Anchors
git log -1 --format=%h -- ops/c1_rail/qualification/execution/campaign_funding.py   # 966b9f6 at the predecessor
git log -1 --format=%h -- tests/integration/qualification_boundary/campaign_driver.py  # 292f283 at the predecessor; absent after
```

## Verification (parent-side, before declaring handoff complete)

```bash
$ python scripts/check_brief.py docs/briefs/handoffs/2026-09-19-full-e1-s2-r2b-warm-service-scheduler.md --type cc_handoff
# Expected: RESULT: well-formed
$ python .claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/handoffs/2026-09-19-full-e1-s2-r2b-warm-service-scheduler.md --type cc_handoff
# Expected: RESULT: well-formed
$ git ls-tree --name-only pr/429 tests/ops/qualification/execution/ | grep -c test_campaign_scheduler.py   # 0 at authoring (defect confirmed)
$ git log -1 --format='%h %ad' --date=short pr/429 -- ops/c1_rail/qualification/execution/campaign_funding.py   # 966b9f6 2026-09-19
```
