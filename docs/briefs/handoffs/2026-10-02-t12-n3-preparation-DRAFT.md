# T12 preparation: final n3 machinery against T02's interfaces, plus the launch-timing envelope

**Type:** cc_handoff (worker preparation card)

**Status:** DRAFT, 2026-10-02. Drafted by a coordinator worker for the deployment coordinator to freeze; not dispatched. The coordinator answers §12's open decisions, commits the frozen revision under the committed-handoff rule and records its SHA before any worker starts.

**Executor:** one worker named at freeze (the coordinator's plan lists it as remote lane J: branch-only, no PR). It is the single writer of `claude/t12-n3-prep` (proposed), cut from `origin/main` at the frozen revision.

**Coordinator:** the deployment coordinator ("Coordinating parallel Claude sessions (2)"). It owns freeze-impact and launch-feasibility acceptance (checklist T12 *Ownership*), the diff review, PRs and the ledger.

**Owner this card narrows:** the [deployment checklist T12 row](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#t12--final-n3-machinery-and-launch-timing-proven-750k1m) (`:254-263`), its dependency line (`:331`: "T12 can prepare against stable interfaces earlier but needs integrated acceptance and a timing answer before F1") and the D-GO reopen trigger (`:594`: "Reopen it only if T12 timing shows the reseal does not fit B7").

```yaml authority
seat: worker
parent: docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - no_main_write
  - no_merge
  - no_pr_open
  - no_linux_or_ci_dispatch
  - new_files_only
  - no_existing_module_edit
  - no_t00_p7_closure_edit
  - no_stage1c_measured_closure_edit
  - no_statistical_criterion_depth_or_namespace_change
  - no_real_n3_b7_account_or_route_access
  - no_private_bytes_committed
  - single_writer
  - stop_at_coordinator_return
acceptance:
  - tests/ops/qualification/execution/test_final_stage_n3.py
  - tests/ops/qualification/test_production.py
  - tests/ops/qualification/test_contract.py
  - tests/ops/qualification/test_adjudication.py
  - tests/ops/qualification/execution/test_release.py
  - tests/ops/qualification/execution/test_profile.py
```

`test_final_stage_n3.py` is new (§2). The other five are existing pins that must pass unchanged.

## 0. Phase 0: premise and Rule-0 reads

1. **Premise.** HEAD is the frozen revision on `origin/main` (as of 2026-10-02, `6de7bf9`). No `.env`. `git status` clean.
2. **Rule-0 reads** (read them; do not infer them):
   - The T12 row and its owners: checklist `:254-263`, `:331`, `:594`; the Phase 6 plan `docs/superpowers/plans/2026-09-16-phase6-exact-release-launch.md` (`:19`, `:58-68`, `:74`, `:80-83`, `:114-118`).
   - n3's statistics and no-redraw rule: `docs/briefs/pre-registration/2026-09-12-track-b-final-validation-prereg.md` (`:24`, `:45`, `:49`, `:59`, `:103`); admission chain `docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md` (`:68`, `:97`, `:99`, `:120`, `:140`, `:153-154`, `:183`).
   - B7 seal: `docs/spec/2026-09-12-tradeify-account-snapshot-seal-contract.md` (`:40`, C5 and C10 at `:46`); `scripts/seal_account_snapshot.py:30-31`, `:70-81`.
   - Separation of E1 and n3: `docs/superpowers/specs/2026-09-19-attended-batch-qualification-design.md:154-158`, `:210`.
   - Cost model: `docs/briefs/phase3-preparation/2026-09-15/compute-depth.md` (`:62`, `:81`, `:93`, `:99`, `:138`, `:170-171`, `:179`).
   - Code: `ops/c1_rail/qualification/contract.py:699-727` (N3 depth and namespace `n3`, excluded from the E1 seal), `:780`, `:797`; the n3 refusals `ops/c1_rail/qualification/execution/compute.py:20-21` and `ops/c1_rail/qualification/production.py:80-81`; `execution/profile.py:123` (dispatch stops at `['N1','N2','PART_A']`); `execution/campaign_funding.py:26-46` (`WORK_PHASES`).
   - **T02's accepted interfaces** (S3, accepted 2026-09-22 at `a8a983e`; C1 freeze, ledger `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md:649-660`, acceptance `:726-750`): checkpoint families `qualification_campaign_checkpoint_{result,attestation,assessment}/v1`; T1 `CampaignStore.persist_checkpoint_intent` (`campaign_store.py:879`) and T2 `commit_checkpoint_assessment` (`:1007`), re-validated by the service under `dispatch_lock`, with VOID serialized through it; `reserve_work` (`:2987`) and `settle_work` (`:3144`).
3. **Interface finding returned before code (checkpoint):** for each T12 requirement, the T02 interface it reuses, or the seam it needs (for example an `N3` phase, a profile/release dispatch revision, or a separate final-stage authorization). Seams are listed, not applied (the T05 precedent, ledger `:661-663`).

## 0.5. Routing and clarifying questions

Claude worker lane (protected qualification authority design; not a mechanical GLM ticket). No secrets, account data, private originals or Pine. Linux is not needed for this preparation. The coordinator answers §12 T1–T9 at freeze; anything Phase 0 needs and §12 leaves open returns as NEEDS_CONTEXT.

## 1. Goal

T12's preparation half, against T02's accepted interfaces: a protected n3 authorization and binding model with synthetic tests, behind a new-file boundary, and a launch-timing envelope note that answers, with every number cited or labelled an assumption, whether the GO reseal fits B7. Final engineering consumes T05/T06; integrated acceptance and the timing answer are owed before F1 (checklist `:256`, `:331`).

## 2. Scope (new files only)

- **`ops/c1_rail/qualification/execution/final_stage.py`** (name proposed; T1): a model imported by no existing module, so it enters no measured closure. It binds an n3 authorization to:
  - the B7 seal digest and its `valid_until`;
  - the exact `release_sha256` and the execution fingerprint;
  - the frozen N3 depth, namespace `n3` and streams, read from the contract (never chosen here);
  - the E1 decision it follows.

  It enforces one use (no redraw), terminal failure, expiry and VOID, IN_DOUBT on uncertain dispatch (never a replacement draw), and refusal of any E1 stage request, and it keeps a per-step timing ledger.
- **`tests/ops/qualification/execution/test_final_stage_n3.py`:** synthetic fixtures only, at a reduced depth passed as a parameter (no depth value is asserted).
- **`docs/notes/<return-date>-t12-n3-preparation.md`:** the interface map (§0.3) and the launch-timing envelope (§9 is its starting point; the worker reproduces each figure and adds any synthetic measurement it takes).

## 3. Method

- Tests first; each §4 case fails before the model exists and passes after it, with launcher records.
- Canonical owners only: the statistical criteria (prereg `:49`) and adjudication (`adjudication.py`, `test_adjudication.py:27`) are consumed, never restated or changed.
- The T02 interfaces are reused through their public methods in tests; any needed change to them is a listed seam.

## 4. Acceptance checks (falsifier-first)

**H:** an n3 authorization model bound to B7, release, frozen depth/namespace and the E1 decision refuses every case below, while the existing E1-side n3 refusals and the N3 contract shape stay unchanged. **Reject if** a case cannot be made to fail first, any listed existing pin changes outcome, or the diff touches an existing file outside `docs/notes/`. **Revert trigger:** any existing module or test byte changes.

Cases (the checklist T12 *Verification* line, `:261`, one test or more each):
1. **Stale B7:** an authorization at or after `valid_until` refuses.
2. **Intervening activity:** a fill, order or adjustment between the seal and the arm voids the seal and the n3 result and stops for the operator, with no replacement draw (seal C10; ADR `:154`).
3. **Identity drift:** a differing release, execution fingerprint, seal digest or depth/namespace refuses.
4. **Uncertain dispatch:** a lost response ends IN_DOUBT; a second draw for the same authorization refuses.
5. **Expiry/VOID:** an expired or voided authorization refuses; a failed n3 is terminal (prereg `:59`).
6. **Timing margin:** the envelope check refuses when the modelled duration plus the declared reserve exceeds the window.
7. **Separation:** an n3 authorization refuses N1/N2/PART_B/PART_A requests and Part A reruns; the E1-side refusals (`compute.py:20-21`, `production.py:80-81`) and `test_production.py:38` pass unchanged.
8. **Contract shape:** `contract.py:721-724` (namespace `n3`, `included_in_e1_seal` false) passes unchanged in `test_contract.py`.

Runs, each with its launcher record: the acceptance set; `tests/ops/qualification`; `python -I scripts/fp.py check`; `git diff --check`; `git diff --name-only origin/main...HEAD` (new files only).

## 5. Forbidden

- Editing any existing file: modules, tests, profiles, releases, `WORK_PHASES`, the contract, the T00 P7 closure or the 68-module measured closure.
- Changing or restating a statistical criterion, depth (970 is proposed and OWED-BY TB-F1, prereg `:45`), namespace or stream.
- Any real n3, any real B7 seal, any account, route or private-root access.
- Building the deployment-GO validator or interlock (`ops/c1_rail/deployment_go.py`, owned by TB-I3; ADR `:105`).
- Linux runs, CI changes, PRs, merges, pushes to `main`.
- `core/`, `lab/`, Pine.

## 6. Return (status taxonomy)

Return DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED. The coordinator's verdict is RESOLVED or FALSIFIED (named items). The return holds: branch and head SHA; the name list (new files only); the §0.3 interface map with its seams; per case, the fail-first and pass record IDs; the note's envelope table with each figure's citation or ASSUMPTION label; the provisional D-GO reading (§9); concerns.

## 7. Stop conditions (return to the coordinator; do not work around)

- The §0.3 interface finding: return it, then wait for the coordinator before code.
- Any case needs an existing file changed, or a seam applied.
- A statistical owner, the contract or the seal contract disagrees with this card.
- Two failed corrections of the same issue (AGENTS.md).
- **Operator review-round rule (2026-10-02):** after more than three review rounds that each return two or more P1/P2 findings, stop folding; the coordinator adjudicates a rewrite or a narrower scope.
- **Single writer:** only the executor writes `claude/t12-n3-prep`. A second writer appearing is a stop.

## 8. Out of scope and decision unlocked

**Out of scope:** dispatch wiring into the service, profiles or releases; integrated acceptance (after T05/T06); the timed exact-candidate rehearsal (T17/H10); real route or report timing (T07/T08 facts); the deployment-GO module.

**Unlocked:** an accepted preparation return lets the coordinator (a) put the seams to their owners before F1 and (b) read the D-GO trigger against a cited envelope.

## 9. Launch-timing envelope: starting computation (the note reproduces and extends it)

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
| I8 | Per-path time | 9.489 / 10.090 / 10.352 s (min/median/max, one 500-session path) | compute-depth `:81` |
| I9 | n3 illustration | 8.16 h; component proxy 10.98 h; "illustrations, not approved budgets" | compute-depth `:93`, `:138`, `:99` |
| I10 | Cost formula, reserve | `C_n3 = 970*(tFULL+tH1+tH2) + C_adjudication + C_GO + C_reseal_build_restart`; B_n3 in elapsed seconds, proposed 2× reserve | compute-depth `:179`, `:170-171` |
| I11 | Holidays | the seal tool infers no holiday hours | `scripts/seal_account_snapshot.py:71` |

**Derived (arithmetic on the inputs).**
- Window from the close: weekday ≤ 18:00 − 17:00 = **1 h**; weekend ≤ Fri 17:00 → Sun 18:00 = **49 h** (I2, I3). The usable span starts at the seal, not the close.
- n3 compute: 2,910 × 10.090 s = 29,362 s = **8.16 h** (I7, I8; matches I9); at the per-path maximum 2,910 × 10.352 s = 8.37 h; proxy 10.98 h (I9).
- With the proposed 2× reserve (I10, not approved): 16.31 h (median) to 21.97 h (proxy).
- **Weekday:** 8.16 h > 1 h. It fits only with at least an 8.2× speed-up of n3 alone (16.3× with the reserve), and even then leaves nothing for the other terms. ASSUMPTION A1: n3 is single-process at I8's rate; no parallel measurement exists.
- **Weekend:** 49 h − n3 leaves **40.84 h** (median, no reserve), **32.69 h** (median, 2×) or **27.03 h** (proxy, 2×), less the seal's own offset from the close, for C_adjudication + C_GO + C_reseal_build_restart, the restart and activation, and operator availability.

**Unmeasured (labelled; the note must not fill them by guess, Phase 6 `:64`):** C_adjudication, C_GO, C_reseal_build_restart (image build, deploy, host start, read-back), activation acknowledgment, operator availability, the seal's offset from the close. The only related measurement is the qualification worker's launch overhead, 4.848 s (ledger `:1821`), which is not the listener's restart.

**Provisional reading (for the coordinator, not a finding):** on these inputs the reseal cannot fit a weekday boundary, and can fit a Friday→Sunday boundary only if the unmeasured terms total less than about 27–41 h after the seal. The D-GO trigger (checklist `:594`) is therefore not met by this computation, but stays open until T12 measures the unmeasured terms. Restricting launch to weekend boundaries is a scheduling consequence for the operator (T6). ASSUMPTION A2: no holiday-extended boundary (I11). ASSUMPTION A3: the weekly account-preservation trade (STATE `:64-66`) is not placed between the seal and the arm, since I4 forbids any order in that span.

## 10. Audit hooks (runnable)

```bash
# Card form and authority. Expected: RESULT: well-formed; exit 0.
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-02-t12-n3-preparation-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-02-t12-n3-preparation-DRAFT.md
# Premise (Git Bash), in the executor worktree.
test ! -e .env && echo "no .env" || echo "FAIL: .env present"
grep -n "n3 requires its own authorization" ops/c1_rail/qualification/execution/compute.py ops/c1_rail/qualification/production.py
grep -n "dispatch_checkpoints=\['N1', 'N2', 'PART_A'\]" ops/c1_rail/qualification/execution/profile.py
# Envelope arithmetic (reproduce I7 x I8).
python -c "print(2910*10.090/3600, 2910*10.352/3600, 49-2910*10.090/3600)"
# Scope at return: only new files.
git diff --name-status origin/main...HEAD
```

## 11. Pre-mortem (README rule)

- **Loop cost:** one Windows build loop; no Linux.
- **Decisions the executor will hit:** T1 (module or note-only), T2 (dispatch seam shape). Ruled at freeze.
- **What makes it moot:** a change to n3's statistical design (TB-F1) or to the seal contract's boundary rule.
- **Measurements the return fills in:** the interface map, the per-case records and the cited envelope table.

## 12. Open decisions (for the coordinator at freeze)

- **T1 Form.** A new model module plus tests (this draft), or the interface note and envelope only.
- **T2 Dispatch seam.** n3 through the protected service (a new `N3` phase, profile and release revision) or a separate final-stage authorization. Either is a seam for the owners, not this card.
- **T3 B_n3 and reserve.** The 2× reserve is a proposal (compute-depth `:170-171`); who freezes B_n3.
- **T4 Depth.** 970 stays OWED-BY TB-F1; the model takes depth from the contract only.
- **T5 Parallelism.** Whether n3 may be parallelized, which decides the weekday case.
- **T6 Launch window.** Whether launch is restricted to Friday→Sunday boundaries (an operator scheduling decision).
- **T7 Holidays.** Whether a holiday-extended boundary is ever usable (the seal tool says no today).
- **T8 Fit threshold.** The margin at which "the reseal fits B7" is read, so the D-GO trigger is decidable.
- **T9 Executor.** Remote lane J (branch-only) or another worker; the card is lane-neutral.
