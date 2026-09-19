# B0 path comparison — source-bound review (2026-09-19)

**Status:** evidence record. The decision it supports is owned by the plan's
[B0 decision](../../superpowers/plans/2026-09-19-attended-batch-qualification.md#b0-decision--2026-09-19)
(retain the protected service; next single outcome S2-R2b). This note holds an
independent read-only comparison that reached the same selection, the coordinator's
spot-checks of it at `8aa5753`, and the corrections it owes to the decision's
neighbours. It authorizes nothing and changes no contract.

**Provenance:** a second coordinator session executed the plan's B0 handoff on
2026-09-19 through a bounded read-only Claude subagent, concurrently with the
session that recorded the decision. Both worked from PR #430 head `f879d68` and
PR #429 head `8aa5753eac8a533e1921c2b796c00cb376513614`. The comparison was
originally returned into the plan document; after the decision landed as
`7a1bcb3` it was moved here to keep one decision in the plan. No runtime suite,
harness, Docker, workflow, provisioning, spend or broker action was run by either
session for B0.

**Coordinator spot-checks (all confirmed at `8aa5753`):** the diagnostic
`SUBMIT_E1` path returns `diagnostic_status` for an existing row and never
re-enters `run_campaign_work` (`service.py:283-298`); the guardian polls
`cpu.stat` and kills through Docker (`campaign_supervisor.py:836-839`) and breaks
out on an already-exited container (`:843-845`); `recover_service` calls only
`recover_campaign_work`; none of the S3–S8 interfaces exist under `ops/` and
there is no `seal_service.py`; the fifteen snapshot tests call
`prepare_scheduled_work`, which does not exist, while the funding API is
`claim_scheduler_bootstrap` (`campaign_funding.py:265`) and
`materialize_scheduler_bootstrap` (`:317`).

## Reconciliation with the recorded decision and the R2b handoff

| Point | Recorded decision / handoff (`7a1bcb3`) | This review | Disposition |
|---|---|---|---|
| Selection | Retain the protected service | Same | Agree |
| What the batch removes | About 300 lines: client campaign ops, `client.py:55-94` reassembly, the transport half of R2b | About 30 lines: the two `SUBMIT_E1` RPC branches (`service.py:234-248`, `:283-298`) | Different counting scope; both small against the batch-only additions. No conflict |
| Single-lifetime posture (delta D2) | Recorded as the first-release posture: interrupted means terminal pending operator disposition | Routed as an operator ruling because it retires governing spec §2.6 rows 2, 5, 6 and 7 and slices decision 6 | The R2b handoff §5 forbids editing the governing spec, so an amendment to §2.6 and the slices plan is still owed to keep the owner text consistent with the recorded posture. Owner: coordinator, after the operator confirms |
| Red R2b tests | Handoff §0.5 (A): they exist only in `C:/Users/joshu/.codex/worktrees/full-e1-s2-supervision/multi_firm_operations`; if absent, re-derive | That checkout was emptied on 2026-09-19 at 07:16 local. The only copy is commit `1ef91be` (parent `966b9f6`), held by the local ref `refs/codex/snapshots/147f94c9c3eb0dd2f9c0b261eddc39cf44b66902`, on no branch | Correction to §0.5 (A): recover with `git show 1ef91be:tests/ops/qualification/execution/test_campaign_scheduler.py`, record its SHA-256, and only then fall back to re-derivation. The file targets `prepare_scheduled_work`, `parse_schedule_request` and `scoped_boottime_deadline`, none of which exist at `8aa5753`; re-targeting to the claim/materialize API is Step 2.1 work, not a discrepancy to report |
| R2a acceptance evidence | Handoff cites the R2a fingerprint and three final record IDs | Those records (`20260919T110352Z-59d6fa6a497e`, `20260919T110450Z-2380d5ed6980`, `20260919T110920Z-a2365379e666`) lived in the emptied checkout and are in no `recovery/` packet; acceptance is narrative-backed | The handoff's Step 2.1 and 2.7 selections re-establish R2a behaviour on frozen bytes; the Step 2.1 record becomes the source-bound R2a baseline and should be cited instead of the lost IDs |
| Pylint on #429 | "new import cycles among the S2 modules" | Log: 34 `R0401` lines, 7 naming S2 modules; `main` 8.08, #429 7.99 | Compatible; the cycle attribution is partially supported |
| Adversarial review | Handoff Pass 3 expects independent Codex review of the R2b PR | Codex reported its code-review usage limit on #430 at 11:59Z on 2026-09-19 | Until credits are restored, the parent's fable-judge pass is the only independent review; state this in the R2b return |
| Authority statements | "Coordinator: Joshua"; "assigned by the operator on 2026-09-19" | Not verifiable from the repository | Treated as the operator session's record; nothing here depends on it |

## Comparison as returned (2026-09-19, source at `8aa5753`)

Read-only comparison. Incumbent bound to PR #429 head `8aa5753eac8a533e1921c2b796c00cb376513614`
(contains R2a commit `966b9f6` and `origin/main` `97d0319`, the PR #428 merge). Batch design bound to
`../specs/2026-09-19-attended-batch-qualification-design.md` at this branch. Line numbers are at
`8aa5753`. No test, harness, Docker, workflow, provisioning, spend or broker action was run; every claim
below is source inspection plus retained records. CAP references are to `CAP-20260916`
(`docs/briefs/phase4-preparation/2026-09-16/capability-decision.md`). Acceptance stays with the
coordinator; the service/batch ruling stays with the operator.

### (a) Refreshed incumbent state

| Component / slice | Written | Locally accepted | Linux-verified | Production-ready | Evidence pointer |
|---|---|---|---|---|---|
| Protected N1 foundation, PR425 merge `1e49283`, `N1_ONLY` | yes | yes | yes: two-host `--test-only` run, 464/464 per host; #429 boundary (1)/(2) PASS re-run the same N1 selection | no: `release_schema.py:38-41` requires `N1_ONLY`, `production_execution=False` | governing spec §0; `.github/workflows/qualification-execution-boundary.yml:26-31` |
| Task 1a canonical campaign plan: `checkpoint_plan.derive_campaign_plan` `:70`, `validate_campaign_plan` `:150` | yes | yes | n/a (pure) | no: PLANNING_ONLY | `recovery/full-e1-20260919/README.md`, record `20260919T010503Z-d08fafc388e1` (182 passed) |
| Task 1b dormant admission: `campaign_store.admit/retry/status/context/chunk/void_retry/void`; release v2 `dispatch_enabled=False` | yes | yes | no | no | same packet; `release_schema.py:34-37` |
| S1 durable budget/recovery + two repairs + PR428 review overlay: `begin_admission` `:621`, `bind_budget` `:678`, `reserve_work` `:729`, `settle_work` `:810`, `record_work_transition` `:835`, `recover_work` `:893`, `budget_snapshot` `:943`; `campaign_budget.py`; snapshot v1/v2 | yes; on `main` at `97d0319` | yes: `430fc72`; 166 passed `20260919T025423Z-77702de7e430`; overlay 127 passed in `recovery/pr428-review-20260919` | no: trusted observations are simulated | no | `recovery/full-e1-s1-repaired-20260919/README.md`; `recovery/full-e1-s1-pr-20260919/README.md` |
| S2 candidate: `campaign_supervisor.py` guardian/runtime/probes; diagnostic release v3, profile v3, budget profile v2, observation v2, snapshot v3; `campaign_host.py`; `campaign_driver.py`; seven `test_s2_*` cases under manifest `QEXEC-01` (`invariant_manifest.json:345-372`) | yes | NO: INCOMPLETE / NOT ACCEPTED, four source defects | no: `--s2` never invoked by the workflow (`:31` runs `--test-only`) | no | `recovery/full-e1-s2-20260919/README.md`; 197 passed `20260919T044917Z-4ae4f65a973d`; check FAILED `20260919T044939Z-219eec8aef71` |
| S2-R1 recovery barrier + physical-dispatch acknowledgement: snapshot/v4 `recoveries`/`dispatches`; `claim_supervision_control` `:110`, `launch_gate` `:177`, `acknowledge_dispatch` `:222`, `complete_recovery` `:272` | yes | yes (local): 272 passed `20260919T053710Z-bb97fb5412e6`; reviewer no findings | no | no | `recovery/full-e1-s2-r1-20260919/README.md`; `docs/briefs/handoffs/2026-09-19-full-e1-s2-r1-review.md` |
| S2-R2 contract + 15 red scheduler tests | tests only, unpublished: commit `1ef91be` held by `refs/codex/snapshots/147f94c9…`, on no branch/PR | no: deliberately red; red record `20260919T100953Z-42977cf0e724` found in no packet | no | no | `tmp/full-e1-coordinator-20260919/r2-return.md`; `git show 1ef91be:tests/ops/qualification/execution/test_campaign_scheduler.py` |
| S2-R2a compact funding persistence: `campaign_funding.FundingStore` (`claim_scheduler_bootstrap` `:265`, `materialize_scheduler_bootstrap` `:317`), DB v7, profile v4, budget profile v3, snapshot v5 | yes: commit `966b9f6` in #429 | narrative-backed only: `r2a-return.md` and the ledger cite `20260919T110352Z-59d6fa6a497e` (47), `20260919T110450Z-2380d5ed6980` (257), `20260919T110920Z-a2365379e666` (check); those records lived in the emptied Codex checkout and are in no packet found | no | no: runtime disabled, `release_schema.py:47-48` rejects profile/v4; `service.recover_service` `:492-495` reports `FUNDING_*` and skips | ledger "Coordinator acceptance — S2-R2a"; `progress.md` "R2a accepted" |
| S2-R2b warm scheduler / runtime activation | not written | UNASSIGNED (operator: STOP AT R2a) | no | no | `tmp/full-e1-coordinator-20260919/r2b-handoff.md` (draft) |
| S2-R3 VOID authentication metering; S2-R4 original deadline before guardian bootstrap | not written | open | no | no | `service.py:305-324`; `campaign_supervisor.py:691-707` (timer armed at `:707` after `ExecutionService` construction at `:691`) |
| S2 Linux acceptance + independent combined review | — | — | none: no `--s2` run, no installed S2 release hash, no image digest | no | `progress.md` Linux notes; `scripts/qualification_boundary_verification.py:52,79-82` |
| S3–S8 | not written: `derive_checkpoint_plan`, `validate_campaign_checkpoint`, `run_n2_compute`, `run_part_a_compute`, `validate_campaign_result`, `authenticate_campaign_result`, `commit_campaign_result`, `prepare_seal_intent`, `commit_campaign_seal`, `sign_committed_pass`, `seal_service.py`, `COMMIT_CHECKPOINT_ASSESSMENT`, `COMMIT_E1_RESULT`, `SIGN_COMMITTED_PASS`: zero hits in `ops/` `deploy/` `tools/` `scripts/` | blocked | no | no | slices plan S3–S8; `g5.py:86-97` rejects any stage list but `['LEGALITY','N1']` |
| Legacy `ProductionExecutor` (`production.py:125`, `__init__` raises) and `run_production_e1` (`orchestration.py:291-294` raises) | present | closed | — | closed | inspected |
| Settlement/route side: `book_account_owner.py:1682-1684` returns `production_route_unavailable` without the `SyntheticBroker` seam (`:303-304`) | seam only | CAP-20260916: R1 QUALIFIED (local engineering only); S1–S5, R2–R5, N1 UNPROVEN | — | no: BLOCKED FOR LIVE RELEASE | `capability-decision.md` "Current capability disposition" |
| PR #429 CI at `8aa5753` | — | — | boundary (1)/(2) PASS, N1 coverage only | — | `pytest (3.11)` FAILED: isolation child cannot collect `test_campaign_funding.py` (`:8` imports uncommitted `test_campaign_scheduler`); `build (3.11)` FAILED: pylint 7.99 < 8.0 |

### (b) Reuse map

| Owner path @ `8aa5753` | Batch disposition | Note |
|---|---|---|
| `ops/c1_rail/qualification/checkpoint_plan.py` | reuse as-is | `derive_n1_plan` `:9`, `derive_campaign_plan` `:70`, `validate_campaign_plan` `:150`; bounds `:40-41`. Per-checkpoint derivation for N2/PART_A is NEW on both paths |
| `qualification/policy.py`, `policy_sources.py` | reuse as-is | `required_output_roles` `:138-146` permits PARTIAL/NONE only for the two-stage prefix (`:142`); the passing N2/PART_B continuation shape is NEW on both paths (spec §2.3) |
| `qualification/evidence.py` | reuse as-is for N1 | `build_stage_artifact` `:158`, `build_n1_evidence` `:182`, `compare_n1_evidence` `:428`; N2/PART_A reconstruction NEW both paths |
| `qualification/journal_snapshot.py` | reuse as-is | assessment snapshot `:14/:50`; campaign budget snapshot v1–v5 `:67/:187` |
| `qualification/production.py`, `orchestration.py` | not reusable | closed; batch must not call (plan checklist item 3) |
| `execution/compute.py` | reuse as-is | `stage_request` `:14-21` (n1/n2 only, n3 refused), `run_n1_compute` `:24-45`; `run_n2_compute`/`run_part_a_compute` NEW both paths |
| `execution/worker.py` | adapt | `run_worker` `:23-58` is N1_ONLY (`:30-31`, compares `derive_n1_plan` `:33-36`); FULL_E1 checkpoint worker NEW both paths |
| `execution/g5.py` | adapt | `validate_n1_evidence` `:20`, `validate_result_envelope_v2` `:86-101` raise `UNSUPPORTED_ATTESTED_CHECKPOINT_SET` beyond N1; aggregate G5 NEW both paths |
| `execution/store.py` (`ExecutionStore`) | reuse as-is | single transaction/validity owner; `void` `:411`, `commit_assessment` `:476` (ATTESTED precondition `:490`, CUTOFF `:520-527`), `store_proposed_result` `:591`. Design's "one protected persistence owner" is this object |
| `execution/campaign_store.py` (`CampaignStore`) | reuse as-is | this is the batch's "attempt journal": provisional intent `:621-676`, budget binding `:678-712`, reservations `:729`, R1 barriers `:110/:177/:222/:272`, diagnostic receipt `:380-465` (`dispatch_enabled=False` `:453`), VOID `:503-521`, gate `:589-604` |
| `execution/campaign_funding.py` | reuse as-is | claim-before-work (`:265-315`) and live-owner transfer (`:317-356`) already implement "reservation precedes expensive validation"; no runtime consumer exists (R2b) on either path |
| `execution/campaign_supervisor.py` | adapt | guardian `:673-762`, runtime `:358-531`, `run_campaign_work` `:261-286`, recovery `:204-246/:869-878`, timers `:596-629`, probe runner `:787-866`; the batch's "single-lifetime resource wrapper" is this file plus `campaign_host.py`; all three Codex findings live here or in its caller |
| `execution/campaign_budget.py`, `campaign_probe.py` | reuse as-is | `PHASES` `:12-13`, `remaining_cpu` `:22`, recovery/dispatch validators `:143-225` |
| `execution/campaign_protocol.py`, `client.py` | adapt | request schema v1 `:6`, 1 MiB chunk `:7`, 2 MiB RPC floor `:8`; batch keeps the immutable request bytes as the journal key even if the socket front is closed |
| `execution/profile.py`, `release.py`, `release_schema.py`, `runtime.py` | adapt | `CAMPAIGN_RESOURCE_SCOPE` `profile.py:37-44`; diagnostic fixed `:47-51`; ceilings `:118-120` (120 s CPU, 300 s wall, 20 s controller per phase); `parse_release` `:22-111`; a versioned batch release/authority schema is NEW; `KEY_ROLES` `:11` already names `seal` but no seal process exists |
| `deploy/qualification/bootstrap.py` | adapt | fixed roles `:16` (`worker`,`supervisor`,`g5`,`campaign_guardian`,`campaign_probe`,`campaign_control`); a `campaign_launch` operator entrypoint is NEW |
| `tools/qualification_verification/campaign_host.py`, `README.md`, `provision.sh`, workflow | reuse as-is | host slice `install` `:11-38` (MemoryMax, swap 0, OOM group), `restart` `:40-49`, `cleanup` `:51-98`; explicit `--s2` selection is owed on both paths |
| `scripts/qualification_boundary_verification.py --s2` | reuse as-is | `:52`, `S2_CASES` `:19`, required-node filter `:79-82` |
| `tests/integration/qualification_boundary/campaign_driver.py`, `test_campaign_supervision_linux.py` | adapt | driver constructs `ExecutionService` `:10-14,:27` before any reservation (the R2 defect); Linux `probe()` `:48-56` spawns it per request; R2b replaces it with bounded transport, batch would replace it with the launcher: same work, different shape |
| `tests/ops/qualification/invariant_manifest.json` | reuse, extend | `QEXEC-01` `:345-372`; E01–E12 registration NEW both paths |
| `ops/c1_rail/book_account_owner.py`, `account_close_evidence.py` | out of E1 scope | O1/O2 owners; CAP rows unchanged by this choice |

### (c) Batch interface map, with the launch → capture → G5 → commit → seal trace

| Proposed batch interface / step | Existing interface it would call | NEW work | Interruption / VOID at this boundary today |
|---|---|---|---|
| `launch_registered_batch(bundle_id, approval_id)`: registry resolves IDs | `release.stage_bundle` `:83` (content-addressed staging); `ExecutionService._context` `service.py:117-121` → `admission.verify_bundle` `:101`; approval bytes travel inside the staged bundle | operator-role fixed entrypoint (`bootstrap.py:16` role + `uid_roles`/`permitted` `service.py:59-70` operator peer) and an ID→bytes registry; today the request carries `bundle_sha256` and the operator is not a request role | none before durable intent (spec §2.6 row 1) |
| protected attempt reservation before expensive validation | `CampaignStore.begin_admission` `:621-676` (provisional intent + ADMISSION reservation, DB v6/v7 upgrade `:644-654`); `controller_cpu_guard` `campaign_supervisor.py:605-629` around it (`service.py:284`) | none for admission; the launcher process's own construction before `begin_admission` is the R2 defect in a new coat (`campaign_driver.py:10-14`) | exact resubmit returns `diagnostic_status` `service.py:289-292` and never re-enters `run_campaign_work` `:298`: crash between `:293` and `:298` leaves the admission work RESERVED forever with its reservation consumed (Codex P1 #2). Spec §2.6 row 2 ("continue same reservation") is not implemented |
| single lifetime / outer envelope | `prepare_campaign_work` `:89-118` (START_OWNER `:109`, START_INTENT `:110-114`); `run_campaign_work` `:261-286`; `LinuxCampaignRuntime.start` `:429`; `launch_gate`/`acknowledge_dispatch` `campaign_store.py:177-243` (R1 dispatch barrier, committed before the OS effect); `guardian_unit_spec` `:121` (LimitCPU 13, TasksMax 1); `arm_boottime_deadline` `:596`; host slice `campaign_host.install` `:11-38` | R4: deadline before bootstrap (`guardian_main` builds `ExecutionService` `:691` before arming `:707`); Codex P1 #1: cumulative payload CPU is the guardian poll `_run_probe:836-839` (kill via Docker), not a kernel ceiling; Codex P2: `seen_pids` UID check `:822-835` is skipped when the container has already exited `:843-845`. The design's "reuse proven host enforcement" points at unproven enforcement | crash after START_INTENT → guardian `except` `:758-762` → `recover_campaign_work` `:869` → IN_DOUBT before cleanup (`_recover_campaign_work` `:204-246`); lost owner token = permanent block (R1) |
| controller runs N1 → G5 → joint N2/Part B → G5 → Part A → G5 (stage selection internal) | `compute.run_n1_compute` `:24`, `stage_request('n2')` `:14`; `worker.run_worker` `:23` (N1_ONLY); `g5.validate_n1_evidence` `:20`; `store.commit_assessment` `:476` (N1 only). Diagnostic probes (`_run_probe` `:787-866`) are the only campaign work that launches today; `supported_checkpoints=[]` `profile.py:49` | identical to S3–S5: `derive_checkpoint_plan`, FULL_E1 worker role, `validate_campaign_checkpoint`, checkpoint attestation schema, campaign progression field, private G5 fetch/commit route (qg5 is a separate UID on both paths; slices decision 5) | not reachable: no checkpoint dispatch exists |
| `read_batch_receipt(attempt_id)` | `CampaignStore.status` `:54`, `diagnostic_status` `:351`, `scheduler_status` `campaign_funding.py:256`; `chunk` `:477` (FETCH_PLAN_CHUNK); `client.request` `:31`, `fetch_campaign_plan` `:55` | file export for an operator without socket access, or keep the socket with an operator role | reads never launch: STATUS/FETCH never dispatch; exact SUBMIT_E1 retry returns status `service.py:236-237,:289-292` |
| operator VOID + whole-job termination | `CampaignStore.void_retry/void` `:494-521` (writes `VOID` budget event `:516-520`); `queue_diagnostic_void` `:333`; pending-VOID authentication inside `finish_diagnostic_admission` `:416-433`; `_check_budget` `:601-602` refuses VOID at every positive gate; cleanup via `_recover_campaign_work` `:234` and `campaign_host.cleanup` `:51` | VOID→kill wiring: the campaign VOID branch `service.py:305-324` returns without stopping anything; termination relies on the guardian's `_assert_authority` poll `:815` (same descheduled-guardian weakness as Codex P1 #1). R3 unmetered authentication `:316-323` is inherited unchanged | VOID first → publication refused (`:601-602`); publication first → historical receipt with `validity` (`store.py:543`) |
| capture → ADJUDICATED → COMMITTED (atomic) | `store.record_capture` `:283`, `sign_captured` (execution key), `store_proposed_result` `:591`, `commit_assessment` `:476-543` with snapshot/revision recheck `:492-496` | S6: `validate_campaign_result`, `authenticate_campaign_result`, `commit_campaign_result`, `COMMIT_E1_RESULT`; identical both paths | crash after CAPTURED → `recover_service` re-signs exact bytes `service.py:519-523`; crash during commit → `retry_assessment` `:372` returns the receipt; both are N1_ONLY-only today |
| SEALED (separate installed sealer) | none: `KEY_ROLES` names `seal` (`release_schema.py:11`), `seal_probe_uid` exists (`release.py:23-35`), a harmless `probe_seal` role exists; no signer, intent, receipt or process | S7 in full: qseal process, `prepare_seal_intent`, `commit_campaign_seal`, `sign_committed_pass`, both VOID orderings | not reachable |
| removal: remote submission/chunk/retry APIs | SUBMIT_E1 branches `service.py:234-248` (dormant) and `:283-298` (diagnostic); `FETCH_PLAN_CHUNK` `:251-252,:301-304`; `retry` `:236`; transport is a local Unix socket with SO_PEERCRED (`serve` `:525`), not remote | delete or role-restrict about 30 lines; chunk retrieval must survive for qg5 retained-input access (slices decision 5, spec §2.2a); "duplicate launch returns the existing disposition" is the retry API under another name | — |
| removal: repeated client admission | `begin_admission` is idempotent on exact bytes `:635-641` and refuses N1 promotion `:642-643` | nothing exists to remove | — |
| removal: multi-lifetime compute recovery | only negative recovery exists: `recover_service` `:485-504` runs `recover_campaign_work` (IN_DOUBT + cleanup) for profile v2 works and skips funded attempts `:492-495`; spec §2.6 rows 2, 5, 6, 7 (continue reservation, retry exact candidate, dispatch next checkpoint, byte-identical receipt) are unimplemented; R1 already leaves a lost owner permanently blocked | nothing implemented is removed; a spec obligation is removed (contract delta D2) | — |
| removal: automatic continuation | none exists; `recover_service` never relaunches | nothing to remove | — |

### (d) Contract deltas

| Owner document | Precise delta the batch needs | Statistical / economic decision changes? |
|---|---|---|
| Governing spec §2.2 ownership table; §2.2a bounded plan transport | D1: Client row → operator/installation administrator; SUBMIT_E1 RPC no longer a prerequisite; chunk retrieval retained for qg5 only | no |
| Governing spec §2.6 restart/retry table rows 2, 5, 6, 7; §6 E06/E07/E12; slices plan decision 6 (durable signing recovery) | D2: interrupted attempt is terminal pending explicit disposition; no continue-same-reservation, no candidate/receipt recovery across lifetimes; duplicate submission cases collapse to duplicate launch | no threshold, depth, seed, budget or sizing change. Flag: an interruption after computation now consumes the attempt; a replacement is a separately authorized fresh attempt (spec §2.6 last paragraph already governs). Operator ruling, because it raises expected attempt consumption per PASS |
| N1 boundary design §4 release manifest; `release_schema.parse_release` `:22-111`; spec §2.1 | D3: new versioned batch release/authority schema (capability, `dispatch_enabled`, operator launch role) distinct from N1_ONLY v1 and admission-only v2/v3; profile/v4 pairing (R2a) becomes activatable only under it | no |
| S2 handoff coordinator decisions (resource boundary, finalization CPU); spec §2.5 | D4: none in numbers; documentation that per-phase ceilings partition one non-renewable envelope. `PHASES` `campaign_budget.py:12-13` and `profile.py:118-120` unchanged | no |
| Phase 3 plan (E1 seal grants no n3), Phase 4 plan WP4 (E1 seal + D0 + separate D1 before TB-V1), Phase 5 plan | D5: add explicit B2 (production-class release/source acceptance) and B4 (n3 machinery, fresh B7/account identity, timed rehearsal) outcomes; `compute.stage_request` already refuses n3 `:14-16` | no |
| Settlement design §4.3 route B; CAP-20260916 S1–S5 | D6: none in evidence law; manual collection is route B as written. CAP stays the sole verdict owner; S1–S5 remain UNPROVEN | no |
| Phase 5 WP1, halt/resume rev9, proposed bounded-platform-protection ADR | D7: reconcile before relying on continued native protection; still AMENDMENT_REQUIRED; not a B0 decision | no |

Nothing in D1–D7 changes a statistical or economic decision. D2 is the only delta that alters an
operational outcome (attempt loss on interruption) and is routed to the operator.

### (e) Remaining outcome-sized work, both paths

Sunk on the incumbent: Task 1a/1b, S1 + repairs + overlay, S2 candidate, R1, R2a. Migration and
amendment effort is a batch cost. "required" means the outcome must be delivered before a genuine
synthetic E1 can reach SEALED_PASS on that path.

| Outcome | Incumbent service | Batch candidate | Evidence pointer |
|---|---|---|---|
| R2b: funded scheduler/runtime activation (profile v4 into a release, warm producer, Linux driver replacement, 15 red tests re-targeted to `claim_scheduler_bootstrap`/`materialize_scheduler_bootstrap`) | required | required, reshaped: the launcher must be funded before campaign imports; same R2a consumers; driver replaced by launcher instead of by fork transport. No saving | `r2b-handoff.md`; `campaign_driver.py:10-14`; `1ef91be` tests still call `prepare_scheduled_work` (absent) |
| R3: metered post-admission VOID authentication | required | required (same branch) | `service.py:316-323`; `campaign_store.py:416-433` |
| R4: original deadline before guardian bootstrap | required | required ("trusted outer launcher owns limits and physical termination" is R4) | `campaign_supervisor.py:691,:707` |
| Codex P1 #1: kernel-enforced cumulative payload CPU | required | required; no proven enforcement to reuse | `campaign_supervisor.py:836-839` |
| Codex P1 #2: death between `begin_admission` commit and START_INTENT | required: re-enter from durable RESERVED admission work (spec §2.6 row 2) or make the exact resubmit resume | required: the design's "a crash there cannot grant another uncharged launch" leaves the attempt RESERVED and consumed; an explicit disposition is still owed | `service.py:289-298` |
| Codex P2: UID verification when the payload exits before first inspection | required | required (same runner) | `campaign_supervisor.py:843-845` |
| S2 real Linux acceptance (`--s2` route, installed release hash, image digest, expanded cases incl. client death, lost counters, cleanup failure, actual UID membership) | required | required plus harness re-baseline (`probe()` `:48-56` and `QEXEC-01` re-bound to the launcher) | workflow `:31`; `progress.md` Linux notes |
| S2 independent combined review | required | required | coordinator handoff |
| S3 N1 checkpoint route | required | required | absent interfaces, (a) row S3–S8 |
| S4 joint N2/Part B | required | required | same |
| S5 Part A with prefix | required | required | same |
| S6 aggregate result + atomic commit | required | required | same |
| S7 qseal + seal publication | required | required | same |
| S8 E01–E12 Linux acceptance + combined review | required | required; E06/E07/E12 narrower under D2 (fewer crash-recovery orderings, duplicate launch instead of duplicate submission); manifest/evidence rebinding is a cost | slices plan "Combined acceptance coverage" |
| #429 CI: isolation import defect; pylint 7.99 | required before merge (R2b publishing `test_campaign_scheduler.py` clears the import) | required if batch starts from `8aa5753`; if it starts from `main` `97d0319` it drops R2a (sunk work lost) | coordinator-verified CI facts |
| Batch-only: operator fixed entrypoint + ID registry + operator peer role; versioned batch release/authority schema (D3); amendments D1–D5 across spec, slices plan, boundary design, Phase 3/4/5 plans; close SUBMIT_E1 RPC; re-target R2b tests; correct the two dead design links | not needed | required | design "Interfaces and state", "Required amendments" |
| O1 settlement/route feasibility; O2 attended candidate; feed equivalence | required, independent | required, independent | CAP-20260916 rows; `book_account_owner.py:1682-1684` |

Effort ranges: unsupported for every row except the RPC removal, which is bounded by
`service.py:234-248` and `:283-298` plus `campaign_protocol._OPERATION_FIELDS` `:9` (tens of lines,
high confidence) and is smaller than the batch-only additions row. Hour/day estimates for R2b, R3, R4,
the Codex findings and S3–S8 are not supported by any interface inspected here: the interfaces do not
exist, so their size cannot be measured. Operator attendance: the batch adds one attended launch and
one attended disposition per interruption; the service adds none for E1 (the operator's daily
export/review and incident recovery belong to O1/O2 on both paths). Interruption risk: identical
enforcement code on both paths until Linux evidence exists; the batch turns every interruption after
compute into a consumed attempt (D2).

### (f) Recommendation (proposed)

Retain the protected service. The batch saves no demonstrable implemented work: its four removals
target roughly thirty lines of local-socket RPC and three spec obligations that were never implemented
(the positive-continuation rows of §2.6). Every remaining outcome (R2b, R3, R4, the three Codex
findings, S2 Linux acceptance, S3–S8, CI repair) is required on both paths, and the batch adds a fixed
entrypoint, a registry, a versioned batch release, five document amendments, a harness re-baseline
and re-targeting of the R2b tests, while re-creating the S2 "construction before funding" defect inside
its launcher process.

Take the savings inside the service by amendment, not by re-architecture: (1) D1 in policy form,
one operator principal on the local socket, no remote transport (already true); (2) narrow E07 to
duplicate launch (already idempotent at `begin_admission` and `retry`); (3) put D2 to the operator as
a scope trim, since R1's lost-owner block already behaves as "no positive continuation" and the
remaining continuation rows are unbuilt; (4) keep manual daily export/review and manual incident
recovery as O1/O2 items, which this choice does not touch.

Falsifier, any one flips the recommendation: (i) an R2b return shows that the warm-service preload,
bounded fork transport, deferred funded open and compact recovery producers cost more than a minimal
funded launcher prelude would, measured on the same `claim_scheduler_bootstrap`/`materialize` seam;
(ii) the operator rules that the SUBMIT/STATUS/FETCH/VOID socket front must not exist regardless of
cost; (iii) Linux evidence shows the guardian-per-work design cannot enforce the single-lifetime
envelope while a single launcher process can.

### (g) Proposed next handoff

Superseded by the recorded handoff
`docs/briefs/handoffs/2026-09-19-full-e1-s2-r2b-warm-service-scheduler.md`
(same outcome, predecessor `8aa5753`). The prerequisites that handoff lacked at
authoring are in the reconciliation table above.

### (h) Unresolved conflicts and routed decisions

| Conflict | Routed to |
|---|---|
| D2 (interrupted attempt terminal; attempt consumed) against spec §2.6 rows 2/5/6/7 and slices decision 6 | operator ruling; coordinator drafts the amendment only if the batch or the scope trim is chosen |
| Batch "trusted outer launcher owns limits and physical termination" against the guardian-per-work + qexec design; R1 dispatch barriers remain necessary for the Docker payload start either way | coordinator |
| Batch removal of chunk retrieval against qg5's need for authenticated retained-input access (slices decision 5) | coordinator |
| Batch starting point: `8aa5753` (CI red) versus `main` `97d0319` (drops R2a) | coordinator; operator owns the service/batch ruling |
| Codex P1 #1 (kernel cumulative CPU) and P2 (UID check) are not covered by R2b/R3/R4 | coordinator: bounded repair or fold into the S2 Linux acceptance handoff |
| `production_route_unavailable` seam, CAP S1–S5/R2–R5/N1 UNPROVEN, feed equivalence | O1/O2 owners; unaffected by B0 |
| Proposed bounded-platform-protection ADR still unratified | Phase 5 WP1 / operator |

### (i) Corrections owed elsewhere (findings only; nothing fixed here)

1. Design doc links `../plans/2026-09-17-phase3-completion-handoff.md` and
   `../plans/2026-09-17-phase4-completion-handoff.md` resolve nowhere; the owners on `main` are
   `2026-09-15-phase3-qualification-control.md`, `2026-09-16-phase4-real-capability-qualification.md`
   and `2026-09-16-phase5-attended-operations.md`. Its coordinator-handoff link exists only on the
   #429 branch.
2. Design "Grounding" cites HEAD `c77aac4` in `C:/Users/joshu/.codex/worktrees/full-e1-s2-supervision`;
   that checkout no longer exists and `966b9f6` supersedes the dirty state it describes.
3. #429 at `8aa5753`: `tests/ops/qualification/execution/test_campaign_funding.py:8` imports the
   unpublished `test_campaign_scheduler`; `pytest (3.11)` and `build (3.11)` (pylint 7.99 < 8.0) fail.
4. Lost records: R2a `20260919T110352Z-59d6fa6a497e`, `20260919T110450Z-2380d5ed6980`,
   `20260919T110920Z-a2365379e666`; also the R2 checkpoint records `20260919T100953Z-42977cf0e724`,
   `20260919T100454Z-c75cc600d7a0`, `20260919T101422Z-44f9ee67e1cf` and intermediate R2a records are
   in no `recovery/` packet (grep). R2a acceptance is narrative-backed until re-run.
5. `1ef91be` is snapshot-ref-held, unpublished; its tests call `prepare_scheduled_work`,
   `parse_schedule_request` and `scoped_boottime_deadline`, none of which exist at `8aa5753`.
6. `test_campaign_supervision_linux.py` reads `works[-1]` as newest despite sorted work IDs
   (`campaign_funding.py:343` sorts) and the 305 s deadline case asserts only terminal state after
   restart (`progress.md`); owed to R2b/Linux handoffs.
7. Slices plan S2 checklist boxes remain unticked while the ledger records the candidate, R1 and R2a;
   ledger/checklist consistency owed to the roadmap owner.
8. This plan's "Remaining-work comparison at authoring" row "Request admission/transport/retries:
   implemented in part" understates: Task 1b admission/transport/retry and the diagnostic v3 route are
   implemented; only funding-before-construction (R2b) is missing.
