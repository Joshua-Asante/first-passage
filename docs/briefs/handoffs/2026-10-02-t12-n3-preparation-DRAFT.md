# T12 preparation: map final n3 onto the existing engine, list the final-stage gaps, and carry the launch-timing envelope

**Type:** cc_handoff (worker preparation card)

**Status:** ACCEPTED narrowing 2026-10-06 (Joshua via hyper; deployment coordinator concurs; card owner coordinator (4)), effective on the merge of the final re-checked revision. No build, run or operational GO.

**Decision record.** Joshua, 2026-10-06, via hyper (verified by the deployment coordinator): YES to the narrowing, effective after the final wording re-check; the deployment coordinator concurs. Scope as accepted: the interface map (§2a), coverage matrix (§4), gap list (§2b) and timing envelope (§9) **replace** the standalone preparation prototype of the 2026-10-02 draft (`final_stage.py` plus synthetic tests). T12 keeps its final-stage implementation and qualification responsibilities (checklist `:259`-`:265`). **No ownership transfer is approved**: §12 P-AMEND is NOT APPROVED and kept only as a record. Narrowing basis: the coordinator (4) assessment of 2026-10-05 (read-only); its evidence is carried in §2a, §2b and §4 rather than in a separate note.

**Executor:** any one Claude reader named at freeze. Read-only: no branch, no files, no PR. The return goes to the coordinator.

**Coordinator:** Claude coordinator (4), owner of this card by succession (Joshua's direct ruling, inherited from coordinator (2)). It owns freeze-impact and launch-feasibility acceptance (checklist T12 *Ownership*), the review and the ledger.

**Owner this card narrows:** the [deployment checklist T12 row](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#t12--final-n3-machinery-and-launch-timing-proven-750k1m) (`:256-265`), its dependency line (`:334`: "T12 can prepare against stable interfaces earlier but needs integrated acceptance and a timing answer before F1") and the D-GO reopen trigger (`:599`: "Reopen it only if T12 timing shows the reseal does not fit B7").

**Base:** every `path:line` in this card is pinned at `origin/main` = `debc13363ff3b85ed5ee41bca97a0ae9d76c5767` (`debc133`, 2026-10-05). In §2a, §2b and §4, code paths are relative to `ops/c1_rail/qualification/` and test paths to `tests/ops/qualification/`, unless a path is written in full. T05 material is not on main; it is read at `origin/codex/h9-t05-integration` @ `f237178` and labelled.

```yaml authority
seat: worker
parent: docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md
max_risk: low
capabilities: [repository.read]
constraints:
  - read_only
  - no_file_write
  - no_branch_push
  - no_main_write
  - no_merge
  - no_pr_open
  - no_linux_or_ci_dispatch
  - no_existing_module_edit
  - no_t00_p7_closure_edit
  - no_stage1c_measured_closure_edit
  - no_statistical_criterion_depth_or_namespace_change
  - no_real_n3_b7_account_or_route_access
  - no_private_bytes_committed
  - stop_at_coordinator_return
acceptance:
  - "scripts/check_handoff_authority.py --all: 0 violations"
  - "scripts/check_handoff_brief_form.py: 0 failing"
  - "scripts/check_brief.py --type handoff on this card: RESULT well-formed"
  - "§10 anchor hooks: every path:line in §2a, §2b and §4 resolves at the frozen base"
```

No test is run or written under this card. The pins it cites are evidence read at the base, not acceptance it re-executes.

## 0. Phase 0: premise and Rule-0 reads

1. **Premise.** HEAD is the frozen revision on `origin/main` (as of 2026-10-05, `debc133`). No `.env`. Read only.
2. **Rule-0 reads** (read them; do not infer them):
   - The T12 row and its owners: checklist `:256-265`, `:334`, `:599`; the Phase 6 plan `docs/superpowers/plans/2026-09-16-phase6-exact-release-launch.md` (`:19`, `:32`, `:39`, `:58-68`, `:74`, `:80-83`, `:114-118`).
   - n3's statistics and no-redraw rule: `docs/briefs/pre-registration/2026-09-12-track-b-final-validation-prereg.md` (`:24`, `:45`, `:49`, `:59`, `:103`); admission chain `docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md` (`:68`, `:97`, `:99`, `:105`, `:120`, `:140`, `:153-154`, `:183`).
   - B7 seal: `docs/spec/2026-09-12-tradeify-account-snapshot-seal-contract.md` (`:40`; C5 and C10 at `:46`); `scripts/seal_account_snapshot.py:30-31`, `:70-81`.
   - Separation of E1 and n3: `docs/superpowers/specs/2026-09-19-attended-batch-qualification-design.md:154-158`, `:210`.
   - Cost model: `docs/briefs/phase3-preparation/2026-09-15/compute-depth.md` (`:62`, `:81`, `:93`, `:99`, `:138`, `:170-171`, `:179`).
   - Code: every symbol in §2a. The **post-S5** interfaces govern, not the T02 freeze alone: S4-D1 parameterized T1/T2 with `checkpoint=` and widened the layout to v9 (`execution/campaign_store.py:282-298`); S5 added PART_A and snapshot `/v8` (`:300-325`); the D-S5 fixes merged (#586 `981eb12`, #589 `77cd715`). T02's freeze (ledger `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md:649-660`, acceptance `:727-750`) remains the origin of the T1/T2 contract.
3. **Interface finding.** §2a is the finding, pre-computed at the base. The executor re-verifies it at the frozen SHA and returns any drift; it does not extend it into code.

## 0.5. Routing and clarifying questions

Claude reader lane (protected qualification authority design; not a GLM ticket). No secrets, account data, private originals or Pine. No Linux. The coordinator answers §12 at freeze; anything Phase 0 needs and §12 leaves open returns as NEEDS_CONTEXT.

## 1. Goal

T12's preparation half, against the stable post-S5 interfaces, **without a prototype**: (1) the map of existing engine interfaces final n3 can reuse unchanged (§2a); (2) the final-stage gaps no interface covers, each with the T12 checkbox it belongs to, its dependencies and the evidence it needs (§2b); (3) the eight checklist verification cases as a coverage matrix (§4); (4) the launch-timing envelope with every figure cited or labelled ASSUMPTION (§9). Integrated acceptance and the timing answer stay owed before F1 (checklist `:258`, `:334`). T12's final-stage executor (checklist `:259`) remains the owner of the three T12 checkboxes (`:260`, `:261`, `:262`); §2b names the other parties as **dependencies** whose interfaces those checkboxes need, not as owners. Any reassignment of a checkbox is a **proposed checklist amendment** (§12 P-AMEND, NOT APPROVED), not part of this card.

**Why narrowed.** Most of the authority model the 2026-10-02 draft would have prototyped already exists: `attempt.py:AttemptStore` has a `TB_E2_N3` stage with one reservation, a single start into `STARTED_IN_DOUBT`, VOID, terminal failure and a boot fence (§2a), and the kernel, RNG and adjudicator already accept `n3`. What is missing is wiring that changes existing files or pins (§2b, G1-G5), which a new-file prototype cannot reach. One T12 verification case (8) also lacks a refusal test (G10). The Phase 6 plan also forbids a second runtime authority (`:32`).

## 2. Scope and deliverable

- **Files:** none. No module, test, note or branch.
- **Deliverable:** the executor's return, holding §2a re-verified at the frozen SHA, §2b with each dependency's acknowledgement or NEEDS_CONTEXT, §4 completed, and §9 reproduced.

### 2a. Interface map

"Unchanged need" means what final n3 requires from the interface without modifying it.

| Concern | module:symbol (path:line) | What it already guarantees | Tests (path:line) | Unchanged need | Fit |
|---|---|---|---|---|---|
| Kernel and stage compute | `runner.py:SyntheticStageRequest` (`runner.py:47-64`; `'n3'` accepted at `:56`); `runner.py:_run_stage` (`:88-123`) | Independent FULL/H1/H2 depths; probe before any path; fixed depth; `NeedsContext` on overrun, "no continuation draws authorized" (`:117`); synthetic discriminator | `test_runner.py:34`, `:43`, `:53`; `test_production_budget_boundaries.py:31`; `test_seed_probability_vectors.py:44-46` (runner over n1/n2/n3) | Run at the contract's N3 depth on the B7 initial state | Reusable. The entry adapters refuse n3 (`execution/compute.py:20-21`, `production.py:80-81`; pin `test_production.py:33-38`), so an n3 adapter is a new function (G5) |
| RNG streams | `regime.py:domain_seed` (`regime.py:10-24`; stage label hashed at `:22-23`); `seed_identity.py:seed_input` (`seed_identity.py:29-41`) | `'n3'` valid; stream disjoint from n1/n2 under one `root_rng_namespace`; seed input bound to contract, trust domain and source session IDs | `test_regime.py:41-45`; `test_seed_probability_vectors.py:44-46`, `:101-103`; `tests/ops/qualification/execution/fixtures/seed_consumer_vectors.json` | The disjoint n3 stream | As is (see §13 UNVERIFIED on `rng_namespace`) |
| Statistical decision | `adjudication.py:adjudicate_stage` (`adjudication.py:33-62`) | Accepts `'n3'`; certifying failure cutoffs per population and the speed minimum on FULL via `scripts/certification_power`; PASS or FAILURE | `test_adjudication.py:21-27` (n3 at 970) | Prereg `:49` bounds from `contract.replay.decision_rules` | Reusable. The retained-evidence adapter `result_adjudication.py:adjudicate_replay_outcomes` (`:337-341`) refuses N3 (G4) |
| Contract shape | `contract.py:699-727` (N3 at `:721-724`); budget `:780-800` | N3 FULL/H1/H2 at one frozen depth, namespace `n3`, `included_in_e1_seal` false; `n3_paths = 3 × depth` | Validator only for the N3 namespace and seal role: no test changes N3 `rng_namespace` or `included_in_e1_seal` (`test_contract.py:124` is the N3 fixture row; `:413` changes N1 depth and Part A values, not N3; `:443-447` is a positive N3 depth derivation) | Depth and namespace, read only | As is for the validator; a refusal test is owed (G10) |
| Checkpoint custody (T1/T2) | `execution/campaign_store.py:CheckpointStoreMixin.persist_checkpoint_intent` (`:879`), `.commit_checkpoint_assessment` (`:1007`); `execution/service.py:ExecutionService.dispatch_lock` (`:222`), `_commit_checkpoint` (`:614-637`) | Atomic CAPTURED + SIGNING_INTENT + candidate; exact retry idempotent, different candidate refuses; byte-identical receipt on retry; VOID serialized through the lock; predecessor COMMITTED | `execution/test_campaign_n1.py:612`; `execution/test_campaign_n2.py:652`, `:757`; `execution/test_checkpoint_widening.py:174`, `:219`; `execution/test_service_assessment.py:35`; `execution/test_atomic_assessment.py:54`, `:108` | The same T1/T2 semantics for an N3 family | Pattern reusable; symbols closed: `_family` refuses keys outside `{N1,N2,PART_A}` (`campaign_store.py:300-303`); no N3 in `CHECKPOINT_*_PHASES` (`:196-197`) or `PROGRESSION_PHASES` (`:190-193`) (G2) |
| Reservation | `execution/campaign_store.py:reserve_work` (`:2987`) | Installed phase limits only; "compute phase already reserved; no replacement draws" for ADMISSION/N1/N2/PART_A (`:3052-3057`); signing serialized; exhaustion terminal | `execution/test_campaign_n1.py:525` (no-replacement refusal at `:543`); `execution/test_campaign_budget.py:96`, `:127` | No-redraw at reservation | Pattern reusable; phase closed: N3 absent from that tuple and from `execution/campaign_funding.py:WORK_PHASES` (`:26-46`) (G2) |
| Settlement | `execution/campaign_store.py:settle_work` (`:3144`), `_observe_resources` | Idempotent observation, conflict refuses; wall overrun → `BUDGET_EXHAUSTED`; unknown termination → `BUDGET_UNCERTAIN` (terminal) | `execution/test_campaign_budget.py:107`; `execution/test_campaign_recovery.py:41`; `execution/test_g5_settlement_wait.py:156`, `:179` | IN_DOUBT on uncertain compute, no replacement | As is, given an N3 phase; consistent with D3 = B (2026-10-03, no compute relaunch for first production) |
| Execution service | `execution/service.py:ExecutionService` (`:177`); `dispatch_eligibility` / `part_a_dispatch_eligibility` (`:112-175`); `serve` flock on `service.lock` (`:1282-1283`) | Sole journal and container authority; eligibility fixed at startup per release/profile; one service per root | `execution/test_service.py:10`, `:46`, `:65` | Single-writer protected dispatch | Pattern reusable; eligibility closed at `execution/profile.py:123` (`['N1','N2','PART_A']`); pins refuse N3 (`execution/test_profile.py:166-170`, `execution/test_release.py:245-249`) (G3) |
| Release / profile | `execution/admission.py:verify_release` (`:48`); `execution/release_schema.py:parse_release` (`:49`); `execution/release.py:install_release` (`:56`) | Signed, installed, byte-verified release and profile; runtime hash per role | `execution/test_release.py:36`, `:71`; `execution/test_profile.py:47`; `execution/test_admission.py:73` | The exact `release_sha256` binding | As is for binding; an N3-capable revision is G3 |
| Result / seal | main: `seal.py:validate_result_envelope` (`:360`), `seal_e1_pass` (`:1005`), E1 payload `grants_n3: False` (`:994`). T05 (`f237178`, not on main): `execution/campaign_seal.py` intent → signature → receipt, PASS-only, separate qseal principal | Authenticated envelopes; the E1 seal grants no n3 | `test_seal.py:654`; `test_seal_ordering.py:26`, `:46`; T05 `execution/test_campaign_seal.py` (branch only) | n3 binds to the E1 seal digest as predecessor | E1 seal reusable as input; no n3 envelope (G4). T05 is unmerged (`6cf2732`, `f237178` not ancestors of `debc133`) |
| Attempt journal (Phase 6 `:39`) | `attempt.py:AttemptStore`: `STAGES` (`:22`); `reserve` (`:605`; TB_E1 PASS predecessor `:617-620`); `start_once` (`:675`, → `STARTED_IN_DOUBT`); `void` (`:1003`); `mark_ambiguous` (`:1018`); result verdict RESOLVED on TB_E2_N3 PASS (`:958`); boot fence (`:320-321`) | One reservation per stage bound to its bytes; single start, never reopened; VOID; terminal FAILURE/AMBIGUOUS; boot fence; hash-chained events | `test_attempt.py:82`, `:102`, `:117`, `:139`, `:162`, `:176`, `:259` | One reservation, single start, IN_DOUBT, VOID | Strong candidate with a caveat: it is the Phase 3 controller's journal (consumers `production.py`, `seal.py`, `ops/c1_rail/qualification_cli.py`); `execution/*` does not import it. Which journal carries n3 is G1 |
| Run lock and journal (T00) | `t00_screen/journal.py:append` (`:225`), `read` (`:263`), `read_lock` (`:287`); `screen_authority.py:validate_screen_authority` (`:519`), `_lock_held` (`:560-579`), `_check_run` (`:582-599`) | Hash-chained fsynced JSONL, torn-tail tolerance, corruption refusal; a separately signed "second door" authority revalidated on every use; parent-held run lock | `test_t00_screen_state.py:532` (row S3 chain), `:1212`, `:1241`; `test_screen_authority.py:483`, `:739` | A pattern for a separately signed final-stage authorization (§12 T2, option b) | Pattern only: the lock is Windows `msvcrt` (`_lock_held` returns False on POSIX, `:563-565`) and the authority is bound to r3c; the service is Linux (`fcntl`, BOOTTIME) |
| B7 seal tool | `scripts/seal_account_snapshot.py` (`:30-31`; `boundary` `:70-81`) | C1-C10 checks incl. the C2 `EvaluationState` construct; `valid_until` with no holiday inference | Refusals: `tests/test_seal_account_snapshot.py:194` (C5/C10 rows), `:199` (C5). Positive `valid_until` derivation: `:208` | `valid_until` and the snapshot digest | As is (input only) |

### 2b. Final-stage gaps

**Owner** is T12's final-stage executor (checklist `:259`) for every row: the gaps are the content of T12's own checkboxes `:260` (define and implement the n3 authority), `:261` (bind seal, release, depth/streams, no-redraw) and `:262` (measure the synthetic sequence). The **Dependencies** column names the parties whose interfaces or measurements the owner needs; it assigns them nothing. TB-E2 is an admission-ADR gate row (ADR `:97`, `:120`), cited as a constraint, not a checklist seat. Reassigning any row was proposed as §12 P-AMEND, which is NOT APPROVED; every row, including G1 and G7, stays with T12.

| # | Gap | Checkbox | Dependencies (not owners) | Evidence it needs |
|---|---|---|---|---|
| G1 | **Journal of record for the sole n3.** Two readings exist. (a) Phase 6 `:39` ("existing qualification authority and one-attempt journal") and `:74` ("the accepted qualification controller/attempt store") point at `attempt.py:AttemptStore`, whose `TB_E2_N3` needs TB_E1 PASS in the same journal (`attempt.py:617-620`), while production E1 runs in `CampaignStore`. (b) Attended-batch design `:154` ("the same protected launch/capture machinery") points at `CampaignStore`, where an N3 family would need a predecessor bound to the E1 seal receipt | `:260` | **Stays with T12.** Inputs: Phase 6 plan owner (reading a); qualification design owner (reading b); T11 (service) | A ruling between (a) and (b); a test that an n3 reservation without a matching E1 seal refuses |
| G2 | No N3 checkpoint family, work phase or no-redraw entry (`execution/campaign_store.py:300-303`, `:190-197`, `:3054`; `execution/campaign_funding.py:26-46`) | `:260`, `:261` | T11, following the S4/S5 widening precedent (`/v7`, `/v8`) | Snapshot widening, checkpoint key and progression rule; tests modelled on `execution/test_checkpoint_widening.py:174` and `execution/test_campaign_part_a.py`; a Linux record |
| G3 | Dispatch refuses N3 (`execution/profile.py:123`; pins `execution/test_profile.py:166-170`, `execution/test_release.py:245-249`); the PART_A wall ceiling is 300 s per work (ledger `:1825`, `:1832`) against about 8-11 h of n3 compute (§9) | `:260` | T11 (release/profile revision); B_n3 freeze (§12 T3) | A release/profile revision with N3 limits from the measured production envelope; the pins changed by their owner |
| G4 | No n3 result envelope or retained-evidence adjudicator: `result_adjudication.py:339-341` refuses N3; G5 handles only N1/N2/PART_A (`execution/g5.py:407`, `:506`); `seal.py:994` grants no n3 | `:260` | T05 (result/seal family); ADR gate rows TB-E2 (`:97`, `:120`) as constraints | An n3 result schema bound to FBR, S, release and the E1 seal (ADR `:99`, `:120`); an adapter over the unchanged `adjudicate_stage`; PASS, FAILURE and partial/corrupt-output cases (Phase 6 `:83`) |
| G5 | n3's initial state must be S's (prereg `:103`; ADR `:97`), but compute reads `contract.initial_state` (`execution/compute.py:13-16`; `production.py:58-61`) | `:261` | Qualification contract owner; ADR gate row TB-E2 as constraint | A seal → `EvaluationState` binding with the seal digest in the result; a mismatched or expired seal refuses at dispatch |
| G6 | B7 `valid_until` and no-activity are not enforced at n3 start or at arm: C10's consumer obligation is not enforceable by the tool (seal contract `:46`); `ops/c1_rail/deployment_go.py` is absent at the base | `:261` | TB-I3 (arm and activation gate; ADR `:105`); ADR gate row TB-E2 as constraint | Refusal tests for a stale seal and for intervening fill/order/adjustment at the n3 start and at the arm |
| G7 | No binding of EF1, FBR and S at an n3 reservation. The release already binds a `policy_fingerprint` source-owner digest (`execution/release_schema.py:117`; `policy.py:67`); what is missing is the n3-time comparison of EF1, FBR and the seal digest | `:261` | **Stays with T12.** Inputs: T16 (bound candidate); ADR gate row TB-E2 as constraint | A drift-refusal test: differing EF1, FBR or seal digest at n3 reservation |
| G8 | Unmeasured timing terms: C_adjudication, C_GO, C_reseal_build_restart, activation acknowledgment, operator availability, the seal's offset from the close | `:262` | Phase 6 WP2 (`:58-68`); T13 (attended operations); T17 keeps only the final exact-candidate rehearsal (`:264`) | Synthetic measurements of the build, deploy and read-back path |
| G9 | n3 compute duration at production depth on production hardware: I8 is a single-path figure not measured on the Linux service | `:262` | T10 (representative full-workload measurement); T11 (realistic measured resource envelope) | The N2 + Part B joint batch at 970 has the same path count and kernel, so its production measurement is the n3 compute term; parallelism (§12 T5) needs a ruling |
| G10 | No test refuses a contract whose N3 `rng_namespace` is not `n3` or whose N3 `included_in_e1_seal` is true; only the validator does (`contract.py:721-724`) | `:261` | Qualification contract owner (`contract.py`, `test_contract.py`) | A refusal test for each field, modelled on `test_contract.py:413` |

## 3. Method

- Read only, at the frozen SHA. Canonical owners are consumed, never restated or changed: the statistical criteria (prereg `:49`) and adjudication (`adjudication.py`, `test_adjudication.py:21-27`).
- Any needed change to an existing interface is a gap routed to its §2b dependency, never applied here (the T05 precedent, ledger `:661-663`).

## 4. Acceptance checks (falsifier-first)

**H:** at the frozen SHA, every §2a cite resolves and states what the row says, and every verification case below is either refused by a cited existing test or names a §2b gap and its dependency. **Reject if** a cite fails to resolve, a row overstates what the code or test does, or a case is marked covered without a refusing test. **Revert trigger:** a cited pin changes outcome or moves before freeze; re-pin and re-read.

Coverage matrix (checklist T12 *Verification*, `:263`). Every gap is T12's own (owner: the final-stage executor, `:259`); the last column names the gap and the dependency it waits on.

| # | Case | Existing test that refuses it | Coverage | Gap → dependency |
|---|---|---|---|---|
| 1 | Stale B7: an n3 start or arm at or after `valid_until` | Only the seal tool refuses sealing at or after the boundary: `tests/test_seal_account_snapshot.py:194` (C10 rows), `:199` (C5). No consumer refuses a stale seal at n3 start or at arm | GAP | G6 → TB-I3 (arm); n3 start under ADR gate TB-E2 |
| 2 | Intervening activity between seal and arm voids the seal and the n3 result and stops for the operator | None | GAP | G6 → TB-I3; ADR gate TB-E2 |
| 3 | Identity drift: release, execution fingerprint, seal digest or depth/namespace | Changed reservation binding conflicts (`test_attempt.py:102`); release key aliasing refuses (`execution/test_admission.py:73`); N1 depth and budget drift refuses (`test_contract.py:413`) | Partial | G7 → T16 (EF1, FBR, seal digest); G5 → contract owner (seal-bound initial state); G10 → contract owner (N3 namespace) |
| 4 | Uncertain dispatch ends IN_DOUBT; a second draw refuses | Legacy journal: `test_attempt.py:82`, `:176`. Protected path for E1 phases: `execution/test_campaign_recovery.py:41`, `execution/test_service.py:65`, `execution/test_campaign_n1.py:525` | Partial (no N3 phase) | G1 → Phase 6 / design owners (which journal); G2 → T11 |
| 5 | Expiry/VOID refuses; a failed n3 is terminal (prereg `:59`) | VOID: `test_attempt.py:162`; VOID ordering: `execution/test_atomic_assessment.py:108`, `test_seal_ordering.py:26`. Terminal failure is tested for `TB_E1` only (`test_attempt.py:139`); no test commits a `TB_E2_N3` FAILURE | Partial | Failed-n3 terminal test and authorization expiry: G1 (journal), G6 → TB-I3 |
| 6 | Timing margin: modelled duration plus reserve exceeds the window | None (arithmetic only, §9) | GAP | G8 → Phase 6 WP2 / T13; G9 → T10/T11; reserve → §12 T3 |
| 7 | Separation: E1 cannot request n3, n3 cannot request E1 stages or rerun Part A | E1 side: `test_production.py:33-38`; `execution/test_profile.py:166-170`; `execution/test_release.py:245-249`; Part A refuses n3: `test_part_a.py:80`; n3 needs E1 PASS: `test_attempt.py:117` | Partial (E1 side only) | n3-side refusal of E1 requests: no n3 authority exists yet → G1/G2 → T11 |
| 8 | Contract shape: N3 namespace `n3`, `included_in_e1_seal` false | None. The validator refuses (`contract.py:721-724`), but no test changes either N3 field (`test_contract.py:124` is the fixture row; `:413` changes N1 and Part A only) | GAP (validator only) | G10 → qualification contract owner (refusal test owed) |

## 5. Forbidden

- Writing, creating or deleting any file; branches, pushes, PRs, merges, CI or Linux dispatch.
- Changing or restating a statistical criterion, depth (970 is proposed and OWED-BY TB-F1, prereg `:45`), namespace or stream.
- Any real n3, real B7 seal, account, route or private-root access.
- Building or specifying code for the deployment-GO validator or interlock (`ops/c1_rail/deployment_go.py`, owned by TB-I3; ADR `:105`), or for any §2b gap.
- `core/`, `lab/`, Pine.

## 6. Return (status taxonomy)

Return DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED. The coordinator's verdict is RESOLVED or FALSIFIED (named items). The return holds: the frozen SHA read; §2a with every drifted cite corrected or flagged; §2b with each dependency's acknowledgement or NEEDS_CONTEXT; §4's matrix as verified; §9's envelope table with each figure's citation or ASSUMPTION label; the provisional D-GO reading; concerns.

## 7. Stop conditions (return to the coordinator; do not work around)

- A statistical owner, the contract or the seal contract disagrees with this card.
- A §2a row cannot be verified as stated at the frozen SHA.
- Two failed corrections of the same issue (AGENTS.md).
- **Operator review-round rule (2026-10-02):** after more than three review rounds that each return two or more P1/P2 findings, stop folding; the coordinator adjudicates a rewrite or a narrower scope.

## 8. Out of scope and decision unlocked

**Out of scope:** implementing any §2b gap; dispatch wiring into the service, profiles or releases; integrated acceptance (after T05/T06); the timed exact-candidate rehearsal (T17/H10; checklist `:264`); real route or report timing (T07/T08 facts); the deployment-GO module.

**Unlocked:** an accepted return lets the coordinator (a) put each §2b gap to its dependency before F1, and (b) read the D-GO trigger against a cited envelope.

## 9. Launch-timing envelope: starting computation (the return reproduces and extends it)

**Cited inputs.**

| # | Input | Value | Source |
|---|---|---|---|
| I1 | Capture spread / seal delay | captures within 30 min of each other; seal within 24 h of the latest capture | seal contract C5, `:46` |
| I2 | Session boundary | weekday 17:00 ET close → next 18:00 ET reopen; or Fri 17:00 ET → Sun 18:00 ET | C5, `:46` |
| I3 | `valid_until` | the 18:00 ET reopen ending that boundary, exclusive | `:40`; C10 `:46` |
| I4 | Consumer obligation | sole n3 starts and the arm occurs before `valid_until`, with no fill, order or adjustment between | C10 `:46` |
| I5 | Activation | the initial arm is effectively active after restart before expiry | Phase 6 `:19` |
| I6 | GO | GO `valid_until` = the seal's; one artifact-only redeploy between n3 and the arm inside the window | ADR `:99`, `:183` |
| I7 | n3 size | 3 × 970 = 2,910 paths (970 proposed, OWED-BY TB-F1) | compute-depth `:62`; prereg `:45` |
| I8 | Per-path time | 9.489 / 10.090 / 10.352 s (min/median/max, one 500-session path); a single-path figure, not measured on the Linux service | compute-depth `:81` |
| I9 | n3 illustration | 8.16 h; component proxy 10.98 h; "illustrations, not approved budgets" | compute-depth `:93`, `:138`, `:99` |
| I10 | Cost formula, reserve | `C_n3 = 970*(tFULL+tH1+tH2) + C_adjudication + C_GO + C_reseal_build_restart`; B_n3 in elapsed seconds, proposed 2× reserve | compute-depth `:179`, `:170-171` |
| I11 | Holidays | the seal tool infers no holiday hours | `scripts/seal_account_snapshot.py:71` |
| I12 | Current per-work wall ceiling | 300 s (PART_A, TEST_ONLY profile) | ledger `:1825`, `:1832` |
| I13 | Compute-shape equivalence | the N2 + Part B joint batch is FULL at the N2 depth and H1/H2 at the Part B depth through the same `_run_stage` (`execution/compute.py:19-26`, `:57-60`); at n2 = n3 = 970 it is the n3 compute shape | ASSUMPTION A4: n2 = n3 = 970 (OWED-BY TB-F1) |

**Derived (arithmetic on the inputs).**
- Window from the close: weekday ≤ 18:00 − 17:00 = **1 h**; weekend ≤ Fri 17:00 → Sun 18:00 = **49 h** (I2, I3). The usable span starts at the seal, not the close.
- n3 compute: 2,910 × 10.090 s = 29,362 s = **8.16 h** (I7, I8; matches I9); at the per-path maximum 2,910 × 10.352 s = 8.37 h; proxy 10.98 h (I9).
- With the proposed 2× reserve (I10, not approved): 16.31 h (median) to 21.97 h (proxy).
- **Weekday:** 8.16 h > 1 h. It fits only with at least an 8.2× speed-up of n3 alone (16.3× with the reserve), and even then leaves nothing for the other terms. ASSUMPTION A1: n3 is single-process at I8's rate; no parallel measurement exists.
- **Weekend:** 49 h − n3 leaves **40.84 h** (median, no reserve), **32.69 h** (median, 2×) or **27.03 h** (proxy, 2×), less the seal's own offset from the close, for C_adjudication + C_GO + C_reseal_build_restart, the restart and activation, and operator availability.
- **Profile:** n3 is about 100× the current per-work wall ceiling (I12), so production limits need a profile revision (G3).

**Unmeasured (labelled; the return must not fill them by guess, Phase 6 `:64`):** C_adjudication, C_GO, C_reseal_build_restart (image build, deploy, host start, read-back), activation acknowledgment, operator availability, the seal's offset from the close (G8). The only related measurement is the qualification worker's launch allowance, 4.848 s (ledger `:1833`), which is not the listener's restart. The n3 compute term itself is owed by T10/T11's production measurement (G9, I13).

**Provisional reading (for the coordinator, not a finding):** on these inputs the reseal cannot fit a weekday boundary, and can fit a Friday→Sunday boundary only if the unmeasured terms total less than about 27–41 h after the seal. The D-GO trigger (checklist `:599`) is therefore not met by this computation, but stays open until Phase 6 WP2 measures G8. Restricting launch to weekend boundaries is a scheduling consequence for the operator (T6). ASSUMPTION A2: no holiday-extended boundary (I11). ASSUMPTION A3: the weekly account-preservation trade (STATE `:67`) is not placed between the seal and the arm, since I4 forbids any order in that span.

## 10. Audit hooks (runnable)

```bash
# Card form and authority. Expected: RESULT: well-formed; 0 violations; 0 failing.
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-02-t12-n3-preparation-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py --all
python -I scripts/fp.py python scripts/check_handoff_brief_form.py
# Premise (Git Bash).
test ! -e .env && echo "no .env" || echo "FAIL: .env present"
git rev-parse HEAD   # expect the frozen SHA
# Anchor spot-checks (each must print the named line).
grep -n "n3 requires its own authorization" ops/c1_rail/qualification/execution/compute.py ops/c1_rail/qualification/production.py
grep -n "dispatch_checkpoints=\['N1', 'N2', 'PART_A'\]" ops/c1_rail/qualification/execution/profile.py
grep -n 'STAGES = ("TB_E1", "TB_E2_N3")' ops/c1_rail/qualification/attempt.py
grep -n "if set(family) - {'N1', 'N2', 'PART_A'}" ops/c1_rail/qualification/execution/campaign_store.py
grep -n "compute phase already reserved; no replacement draws" ops/c1_rail/qualification/execution/campaign_store.py
grep -n "order = ('N1', 'N2', 'PART_B', 'PART_A')" ops/c1_rail/qualification/result_adjudication.py
grep -n '"grants_n3": False' ops/c1_rail/qualification/seal.py
grep -n "stage not in ('n1','n2','n3')" ops/c1_rail/qualification/runner.py
# Envelope arithmetic (reproduce I7 x I8).
python -c "print(2910*10.090/3600, 2910*10.352/3600, 49-2910*10.090/3600)"
# Scope at return: nothing written.
git status --porcelain
```

## 11. Pre-mortem (README rule)

- **Loop cost:** reading only; no build loop, no Linux.
- **Decisions the executor will hit:** none of its own; §12 is ruled at freeze, and G1-G10 are routed, not decided.
- **What makes it moot:** a change to n3's statistical design (TB-F1), to the seal contract's boundary rule, or a G1 ruling that moves n3 to a journal not mapped in §2a.
- **Measurements the return fills in:** none new; it re-verifies §2a and reproduces §9.

## 12. Open decisions (for the coordinator at freeze)

- **T1 Form.** Decided (Joshua, 2026-10-06, via hyper (verified by the deployment coordinator)): interface map, coverage matrix, gaps and envelope replace the standalone prototype.
- **T2 Dispatch seam.** n3 through the protected service (an N3 phase, profile and release revision; G2/G3) or a separate final-stage authorization (the T00 second-door pattern, §2a). Either is a seam for the owners, not this card.
- **T3 B_n3 and reserve.** The 2× reserve is a proposal (compute-depth `:170-171`); who freezes B_n3.
- **T4 Depth.** 970 stays OWED-BY TB-F1; the contract supplies depth only.
- **T5 Parallelism.** Whether n3 may be parallelized, which decides the weekday case.
- **T6 Launch window.** Whether launch is restricted to Friday→Sunday boundaries (an operator scheduling decision).
- **T7 Holidays.** Whether a holiday-extended boundary is ever usable (the seal tool says no today).
- **T8 Fit threshold.** The margin at which "the reseal fits B7" is read, so the D-GO trigger is decidable.
- **T9 Executor.** Any Claude reader; the card writes nothing.
- **T10 Journal of record (G1).** Reading (a), Phase 6 `:39`/`:74`: the legacy `AttemptStore` `TB_E2_N3` stage. Reading (b), design `:154`: a `CampaignStore` N3 family bound to the E1 seal. The Phase 6 plan owner and the design owner both need to be heard.
- **P-AMEND — proposed checklist amendment: NOT APPROVED (Joshua, 2026-10-06, via hyper (verified by the deployment coordinator); kept only as a record).** Not to be confused with checklist task T11. The checklist gives T12 to the final-stage executor (`:259`) with checkboxes `:260`-`:262`. If the narrowing is accepted, the proposal is to amend the T12 row so that: `:260`/`:261`'s implementation lands as seams in T11 (G2, G3), T05 (G4) and TB-I3 (G6), with the contract owner taking G5 and G10; `:262`'s synthetic sequence measurement is read from Phase 6 WP2 and T10/T11 (G8, G9). It was not approved: T12's final-stage executor owns all three checkboxes, and §2b's parties are dependencies only.

## 13. UNVERIFIED

- Whether any production path consumes `StageSpec.rng_namespace` for N3, or whether the stage label alone keeps the n3 stream disjoint. The code read shows the label only (`regime.py:22-23`; `seed_identity.py:32`).
- Whether the `CampaignStore` budget already charges `n3_paths` against the E1 campaign (`n3_paths` appears in `execution/test_campaign_budget.py:39`).
- Whether the protected service could legally run one N3 phase as several parallel works (T5).
- Whether n2 = n3 = 970 will be ratified (OWED-BY TB-F1); I13's timing equivalence depends on it.
- T05's final n3-relevant seal surface: read on `codex/h9-t05-integration` only; it may change at R1.
- Which journal carries the sole n3 (G1): Phase 6 `:39`/`:74` read as the attempt store, design `:154` as the protected machinery; `AttemptStore.TB_E2_N3` is live and tested on main, but no test commits a `TB_E2_N3` FAILURE.
