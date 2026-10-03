# H9 C′ host-integration: runner/admin, supervisor-parent and owned-command identity, the C′ Linux file and the single C′-final revision (R1 slice 2)

**Type:** cc_handoff (worker build card)

**Status:** DRAFT, 2026-10-03, drafted by a worker for coordinator (3). Revision 2 folded the review of `b6069da` (1 P1, 5 P2, 6 P3) under coordinator (3)'s rulings on D5 and DH2; revision 3 folds the review of `32e5905` (1 P2, 3 P3) under its rulings on DH2's conditions A and B (§10, §12); revision 4 folds the review of `d2c8124` (0 P1, 0 P2, 2 P3: the condition-A probe and B.3's search scope) and re-cites D11 = (a) and D3 = B against their ledger PRs. **NOT DISPATCHABLE:** the §11 prerequisites are open. They include DH4, which is Joshua's, and gate G-C3 (§2.6) if the freeze closure run names a measured member outside D5. Coordinator (3) answers §12 (DH2 by its own freeze checks of A and B), re-anchors every code line on the DH1 base, commits the frozen revision under the committed-handoff rule and records its SHA in the ledger before any worker starts.

**Citation basis.** Code and documents at `origin/main@7e409df` (#624 merged there; Amendment A1 pinned at `f179c0b`; #627 merged at `e9fade0`). Files that exist only on the H9 branch (`campaign_result.py`, `campaign_seal.py`, `g5_result.py`, `seal_service.py`) were checked at `origin/codex/h9-t05-integration@f237178`. Steps 2 and 3 edit several of the same files, so code line numbers are **OWED** re-anchoring at freeze.

**Executor:** one coordinator-dispatched worker (C′ card `:353`), the single writer of its build branch (DH1).

**Coordinator:** coordinator (3), owner of the C′ host-integration lane (R1 slice 2). It owns the freeze, the diff review, integration, PRs, every Linux dispatch and the ledger.

**Owners this card narrows.** It amends one, the C′ card, and only through coordinator (3): at freeze, coordinator (3) records the chosen DH2 form on the C′ card as an Amendment A1 revision (§11.4). Under (ii) that revision amends D2 as amended (`:246`), the `/v8` `NOT_COVERED` list (`:299`) and the separate final revision (`:306`) for C′-final; under (i), the `/v8`-only gating (`:308`), which §2.7 widens.
- C′ obligation, finite map, checks, evidence and residual: [ledger, C′ rulings](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-rulings--t05-environment-sealing-c-and-the-first-release-host-environment-drift-residual-2026-10-02) `:1996-:2047` (map `:2021-:2027`, evidence `:2030`, residual `:2033-:2037`).
- The parent [C′ card](2026-10-02-h9-cprime-runtime-identity-build-DRAFT.md) and its Amendment A1, revisions 1–6: the entries moved here `:344-:351`, the five `NOT_COVERED` owners `:299-:304`, "one final revision" `:306`, gating `:308`, D11 reopened `:355`, the 68-module checkpoint `:118` and item 13 `:146`.
- **C′ D5, RULED YES** (Joshua, directly to the coordinator, 2026-10-02 ~23:20Z: "yes"; C′ card `:249`). It admits C′ edits to `release_schema.py`, `runtime.py`, `worker.py`, `campaign_probe.py` and `protocol.py`. C′-final is part of the C′ build (A1 `:306`; ledger `:2146`, "D5 for the C′ build"), so D5 is this card's measured-closure admission (§2.6).
- H9 checkpoint R1: [staged acceptance](2026-09-27-staged-acceptance-handoffs.md) `:534-:551`, `:563`.
- R1 tooling: [card](2026-10-02-r1-tooling-build-card.md) and #627 (`scripts/qualification_boundary_verification.py`: `R1_CASES` and `CPRIME_CASE` `:48-:59`, `r1_refusal` `:115-:140`, the `--test-only` exclusion `:201-:206` and `:248`, `FP_QUALIFICATION_R1` set and popped `:241-:242`).
- **D11 = (a), RULED** (Joshua, coordinator (2) chat, 2026-10-03T05:09:53Z, verbatim: "done for the grafana phone connection. D11: a", on the corrected options; recorded by coordinator (4) in ledger PR [#658](https://github.com/Joshua-Asante/first-passage/pull/658)): the first runner and admin launches are checked against the host provisioning record (the interpreter identity recorded by `host.py` provisioning), labelled `PRE_RELEASE`; later launches are checked against the signed final revision. This supersedes "D11 reopened" (C′ card `:355`). The record is owed on `main` until #658 merges.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-10-02-h9-cprime-runtime-identity-build-DRAFT.md
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
  - not_dispatchable_until_g_c3_and_dh4_resolved
  - measured_closure_edits_d5_or_g_c3_admitted_only
  - no_r1_selector_mode_scope_or_reader_change
  - no_new_environment_variable
  - pre_release_checks_under_r1_only
  - no_recovery_relaunch_or_retry_path
  - no_step3_or_b4_scope
acceptance:
  - tests/test_qualification_host_identity.py
  - tests/test_qualification_host.py
  - tests/test_qualification_campaign_host.py
  - tests/test_qualification_boundary_verification.py
  - tests/test_record_verification.py
  - tests/test_qualification_boundary_fixture.py
  - tests/test_qualification_invariant_manifest.py
  - tests/ops/qualification/execution/test_boundary_fixture.py
  - tests/ops/qualification/execution/test_release.py
  - tests/ops/qualification/execution/test_runtime_identity_pin.py
  - tests/ops/qualification/execution/test_runtime_identity_launch.py
  - tests/ops/qualification/execution/test_runtime_identity_rechecks.py
  - tests/ops/qualification/execution/test_launcher.py
  - tests/ops/qualification/execution/test_campaign_supervision.py
  - tests/ops/qualification/execution/test_campaign_result_layout.py
  - tests/ops/qualification/execution/test_campaign_result_commit.py
  - tests/ops/qualification/execution/test_campaign_seal.py
  - tests/ops/qualification/execution/test_result_seal_guardian_loop.py
```

`identity_branch_only` reads "this card's build branch (DH1)"; `card_section2_files_only` reads "§2.10". `tests/test_qualification_host_identity.py` is new (name fixed at DH9). Step 2's three `test_runtime_identity_*.py` files are extended in place. The six campaign tests after them are preservation only (item 14). The Linux file `tests/integration/qualification_boundary/test_runtime_identity_linux.py` is written here and **collected only** on Windows; it runs only inside R1 (§8).

## 0. Phase 0: premise, Rule-0 reads and findings before code

1. **Premise.** HEAD is the DH1 base: lane D steps 2 and 3 RESOLVED and integrated, `origin/main` merged in, range-diff reported. #627 is on the base. No `.env` in the worktree.
2. **Rule-0 reads** (anchors at `7e409df`; read them, do not infer them):
   - `tools/qualification_verification/host.py`: the provisioning venv and record `:638-:676`. `manifest['runtime']` (`:672-:676`) holds only `python`, `version`, `signing_requirements_sha256` and `packages`: no interpreter bytes, base interpreter, `pyvenv.cfg` or `.pth` identity. `public_observations` `:67-:74` exports `runtime` verbatim; `validate_inputs` `:77-:87` checks the lock digests. The owned-command wrapper: `ENTER_PROCESS_GROUP` `:309-:317` (ends in `os.execv`), `owned_command` `:320-:322`, `start_owned` `:330-:333`, `run_owned` `:336-:340`. `owned_environment` (`:325-:327`) is the only environment `start_owned` and `run_owned` pass, so no environment variable reaches an owned child. Provisioning's own launches go through `run_owned` (`:597-:599`); `cleanup`'s run under the base interpreter (`:784-:812`).
   - `tools/qualification_verification/host.json` (`python`, `python_version`, `locks`).
   - `ops/c1_rail/qualification/execution/image.py:57`, `:66`: `build_worker`'s `docker pull` and `docker build`, through `host.run_owned` under `host_config['python']`, called from `Boundary.__init__` before install (conftest `:58`).
   - `scripts/qualification_boundary_verification.py`: the runner's pytest launch `:252-:259` (`owned_command(..., sys.executable)` `:258`, `record.execute` `:259`); the environment `:224-:242`; the cleanup call `:267`, in the same process.
   - `scripts/record_verification.py`: the Popen `:211-:212`, the post-exec site. It records every launcher run, so any change here is opt-in.
   - `.github/workflows/qualification-s2-supervision.yml:136-:143`: the runner runs under `$host_root/env/bin/python` through `fp.py --env`. Provisioning is its own step with no mode input (`provision.sh`, `:105-:108`); a separate cleanup step runs `/usr/bin/python3 -I tools/qualification_verification/cleanup.py` (`:154`).
   - `tests/integration/qualification_boundary/conftest.py`: the mode flags `:59-:69`; `admin` `:78-:87` (every `fixture_install` launch goes through `host.run_owned(..., interpreter=self.python)`; `install` is the first, from `__init__` `:65-:69`); `restart` `:197-:233` (diagnostic modes use `campaign_host.restart` `:200`, others `host.start_owned` `:220`).
   - `tests/integration/qualification_boundary/fixture_install.py`: the docstring `:1-:5` (TEST_ONLY approvals, never outcomes); the isolated-administrator preamble `:14-:16`; `install` `:35-:90` (`install_release` `:78`).
   - `tests/integration/qualification_boundary/fixture_producer.py:47-:90` (`release_document`; revision chosen by profile at `:79-:86`).
   - `tools/qualification_verification/campaign_host.py`: `restart` `:107-:115` is the supervisor parent (`systemd-run --collect ... interpreter -I bootstrap supervisor`, `:112`); `cleanup` `:118-:195`. Standard library plus `host` only: governance code cannot import `ops` (`scripts/check_boundaries.py`).
   - `deploy/qualification/bootstrap.py:9-:17` (the off-Linux exit and the role whitelist, which includes `supervisor`); `service.main`, `ops/c1_rail/qualification/execution/service.py:1344-:1355` (`measure_runtime(..., 'supervisor', release)`).
   - `ops/c1_rail/qualification/execution/campaign_supervisor.py:345-:380` (supervision events `/v1`–`/v2` are keyed by `attempt_id` and `work_id`) and `_retain_event` `:540-:553`.
   - The release allow-lists, which already admit `/v8` after step 2 and which C′-final joins only under DH2 (i): `release.py:64`; `ops/c1_rail/qualification/evidence.py:966-:971`, `:1349-:1350`, `:2431`; `service.py:97-:163`, `:373-:382`; `campaign_store.py:2374-:2381`.
   - `tests/ops/qualification/invariant_manifest.json`; its row IDs are closed (`scripts/check_qualification_invariants.py:19`).
   - On the base only: step 2's `runtime_identity.py` (map, derivation, labels, rechecks) and `/v8` parser; step 3's `result_g5` and qseal producers, their checks and rechecks, and its `FP_QUALIFICATION_R1` seam; every site that gates a step-2 or step-3 check or recheck on the installed release (at least `campaign_supervisor.py`, `launcher.py`, `campaign_result.py`, `campaign_seal.py`, `g5_result.py`, `seal_service.py`, `bootstrap.py`, `runtime_identity.py`; finding (e) derives the full list).
3. **Findings returned before code** (the coordinator acknowledges each):
   - (a) **Launch inventory** for the three host entries (runner/pytest admin fixture, service supervisor, owned-command wrapper): each launch site as `file:line`, with interpreter (venv or base), UID, wrapper and gate source (§2.7), and whether it precedes the release install (PRE_RELEASE) or follows it. Include the base-interpreter wrapper launches inside and outside the run (§2.4), and the authority transitions at which each entry's process is resident (§2.11).
   - (b) **Provisioning identity:** which §2.1 fields `host.provision` can record from the venv it creates (DH3); whether the runner's `sys.executable` is `<root>/env/bin/python` on the workflow path; and whether every reader of the private manifest (`cleanup`, `campaign_host`, `boundary_cleanup_plan`) accepts the one added key.
   - (c) **Post-exec binding:** for the runner, the wrapper and its payload are the same `sys.executable`, so `/proc/<pid>/exe` is identical before and after the exec, and a single read races `execv`. Name the binding: the payload's argv in `/proc/<pid>/cmdline`, or a sync mechanism such as a close-on-exec pipe the wrapper holds, whose EOF marks the exec. Either has a fixed bound. The bounded wait is part of one check; a refusal is never followed by a second launch or a second check.
   - (d) **Supervisor-parent route** (DH4): what `campaign_host` can observe of the unit (MainPID, `/proc`, exit) with the standard library, and where its versioned events are retained. `restart` runs `systemd-run --collect` (`:112`), so the unit's exit properties are gone once it stops. Name the exit-evidence source: the journal, or an R1-only argv change (for example no `--collect`, with the unit reset at cleanup).
   - (e) **C′-final form and gate sites** (DH2 is decided at freeze by coordinator (3)'s checks of conditions A and B, §10): re-run condition A's check on the base and confirm the frozen form; name the exact `release_schema.py` lines C′-final needs (none under (ii)); and, under (i), list **every** site on the base that gates a step-2 or step-3 check or recheck on the installed release, as `file:line`, each marked with its §2.10 row (or none), measured-closure membership and D5 membership. The §2.10 gate-site list is a floor, not the full list.
   - (f) **Closures on the base:** the table `docs/notes/2026-09-29-s5-c3-record/stage1c-equivalence/stage1c_closure_table.py.txt` run on the base. Name every §2.10 file, finding (e)'s gate sites included, in the 68 measured (and 63 staging) modules, explicitly including `runtime_identity.py` and the new tools module. Mark each member as inside or outside D5's five files, and confirm disjointness from the P7 closure.
   - (g) **Shared-file state after step 3** (DH7): what step 3 landed in `conftest.py`, `fixture_install.py`, `fixture_producer.py`, `bootstrap.py`, `campaign_host.py` and `invariant_manifest.json`, and which RESULT G5 and qseal checks and rechecks it landed (§2.11).

## 0.5. Routing and clarifying questions

`Routing: local`: a Windows build with Windows evidence. A Claude worker, not `glm_agent`: this is identity and authority code on the protected qualification path (AGENTS.md GLM rule). No secrets, `.env`, Pine, ports or account data are involved. If Phase 0 needs an unanswered §12 decision, return NEEDS_CONTEXT; never assume the answer.

## 1. Goal

Finish C′ at the host so that R1 can run. The three host entries A1 moved here (runner/pytest admin fixture, service supervisor, owned-command wrapper) get the full check set: pre-spawn, child self-check, post-exec `/proc`, exit evidence, a versioned record for each check and the applicable rechecks (§2.11), with D11 = (a) identity sources. Write the C′ Linux file and register its nodes. Ship the **single final signed revision ("C′-final")**, which binds the whole finite map so that no ruled entry stays `NOT_COVERED`, and on which every step-2 and step-3 check stays active (DH2). Every mismatch fails closed. **Scope boundary:** the build branch plus Windows evidence. Linux evidence is R1's (§8).

## 2. Scope

### 2.1 Host provisioning identity record (D11 = (a))

The Docker pin (C′ card §2.1, D3) identifies the worker base image. It says nothing about the host Python that runs the runner and the admin fixture, so the provisioning record must carry that interpreter identity.
- `host.provision` records:
  - the venv executable's path and the SHA-256 of its bytes (the venv is created with `--copies`);
  - the base interpreter (`host.json` `python`): resolved path and SHA-256;
  - the SHA-256 of `pyvenv.cfg`;
  - the `.pth` inventory of the venv's site-packages (sorted names and SHA-256);
  - the three lock digests (`REQUIRED_LOCKS`, already validated at `:77-:87`);
  - the owned-command wrapper: **one tuple per interpreter**, venv and base (§2.4), each with the SHA-256 of the R1 wrapper program;
  - the Python version.
- **Placement (DH3; review P2-3): outside `public_observations`.** The fields sit in one new key of the private manifest, a sibling of `runtime`, with its own schema literal. `public_observations`' allow-list (`:67-:74`) is unchanged, so `evidence/host-observations.json` stays byte-identical in every mode. Provisioning has no mode input (workflow `:105-:108`), so the private manifest gains that one key in every mode; case 1 pins every existing key and value as unchanged. R1's evidence binds the record through the coverage export's digest (§2.9).
- A record without these fields is not a C′ source: every check that needs one refuses.

### 2.2 Runner launch (always PRE_RELEASE)

The runner's pytest launch (`:258-:259`) precedes any release install in the run.
- **Pre-spawn** (under `--r1` only): the runner sets the in-process gate (§2.7) and derives the identity of `sys.executable`, the venv wrapper tuple and UID 0, and compares it with the provisioning record. A mismatch or a missing record refuses before `record.execute`.
- **Post-exec:** an opt-in observer at the Popen (`record_verification.py:211`) waits, within a fixed bound, for the exec of the pytest payload (finding (c)) and reads its `/proc` image. It refuses on a mismatch, on an unreadable image, or on an exec not seen within the bound. Without the observer, `RunRecord`'s behaviour and `record.json` keys are unchanged.
- **Child self-check:** the wrapper's (§2.4).
- **Evidence:** a versioned launch record (expected identity, observed identity per check, label `PRE_RELEASE`, verdict, exit) in `record.data['metadata']` and in the run's evidence. The runner's exit evidence is the recorded `exit_code`; if it is missing, coverage refuses.

### 2.3 Admin fixture launches

- The **first** admin launch (`install`, from `Boundary.__init__`) is checked against the provisioning record and labelled `PRE_RELEASE`.
- `install` binds the runner/admin tuple and both wrapper tuples into C′-final from that same provisioning record. A C′-final whose tuples differ from the record refuses at install.
- **Later** admin launches (`prepare`, `void-approval`) are checked against C′-final.
- Each admin launch gets the controller's pre-spawn check (conftest), the child self-check (`fixture_install.py`, standard library only, beside `:14-:16`, before any other import, gated by §2.7's R1-only argv flag), the controller's post-exec `/proc` check, exit evidence (`run_owned`'s return) and a versioned record under `evidence/boundary/`.

### 2.4 Owned-command wrapper

`host.owned_command` launches every owned child as `interpreter -I -c ENTER_PROCESS_GROUP`, under two interpreters (review P2-4):
- the venv (`<root>/env/bin/python`): the runner's pytest launch (runner `:258`) and the conftest admin launches (conftest `:78-:87`);
- the base interpreter (`host_config['python']`, `/usr/bin/python3`): `build_worker`'s `docker pull` and `docker build` (`image.py:57`, `:66`, from `Boundary.__init__` before install) and the runner's cleanup (`host.py:784-:812`, from runner `:267`).

Under the gate (§2.7):
- **Tuples:** the record and C′-final carry one wrapper tuple per interpreter. The pre-spawn check selects the tuple by the exact interpreter path; any other interpreter refuses.
- **Expected source:** the provisioning record before install (PRE_RELEASE: `build_worker`'s launches and `install`), C′-final after it. The runner's cleanup uses C′-final if it is installed, and otherwise the record (PRE_RELEASE).
- **Outside the run:** provisioning's own launches (`host.py:597-:599`, which produce the record) and the workflow's separate cleanup step (`:154`) have no gate source without a workflow or environment change, and both are forbidden. The coverage export names them as unchecked and never claims them. Coordinator (3) acknowledges this at finding (a); if they must be covered, stop (§7).
- **Pre-spawn:** the wrapper's interpreter and program digest match the selected tuple.
- **Self-check:** under R1 the wrapper is a separate R1 wrapper program, gated by an R1-only argv flag; `ENTER_PROCESS_GROUP`'s bytes are unchanged. It checks its own interpreter identity, standard library only, before `os.execv`. A mismatch exits non-zero without exec.
- **Post-exec:** when the payload is itself a mapped entry, its `/proc` image is checked as in finding (c). Any other payload is an unmediated descendant or OS helper (the residual) and is labelled `NOT_COVERED`, never claimed.
- With the gate off, the argv bytes `owned_command` builds, the `ENTER_PROCESS_GROUP` bytes and the behaviour are all unchanged.

### 2.5 Service supervisor and its parent (`campaign_host`)

Under R1 the supervisor starts through `campaign_host.restart` (`:107-:115`, `systemd-run`) after install, so it is checked against C′-final:
- pre-spawn in `campaign_host.restart`, against the supervisor tuple;
- the bootstrap self-check for role `supervisor` in `deploy/qualification/bootstrap.py` (standard library, before any import, placed where step 2 put its self-check);
- post-exec through the unit's MainPID `/proc` image and its cgroup under the enrolled slice;
- exit evidence at stop and at cleanup, from the source finding (d) names. `systemd-run --collect` (`:112`) unloads the unit when it stops, so its exit properties cannot be read afterwards. If the evidence is missing, coverage refuses.

**Event route (DH4, Joshua's).** The supervisor process has no `attempt_id` or `work_id`, so supervision event `/v2` cannot carry its events, and `campaign_host` cannot import `ops`. Proposed: a versioned host-side launch family, written by `campaign_host` to root-owned evidence. No store, DB10 or `/v2` change. This reads ruled wording, so it waits for Joshua (§12).

### 2.6 C′-final, the single final signed revision, and the measured-closure admission

- **What it binds:** the base-pin hash, the built image ID and **every** ruled entry (ledger `:2021-:2027`) with its tuple. The entries are the runner/pytest admin fixture, the service supervisor, the guardian, control and probes, the N1, N2, PART_A and RESULT G5 roles, qseal, and the owned-command wrapper (one tuple per interpreter, §2.4). No ruled entry is `NOT_COVERED`. That label remains only for the residual's classes (`:2033-:2037`).
- **When:** after step 3's `result_g5` and qseal producers exist (C′ card `:306`). It is produced through `fixture_producer`'s release-revision parameter (C′ card `:324`), which gains the C′-final form.
- **Form (DH2): coordinator (3) prefers (ii), C′-final IS `/v8` with the full map,** provided coordinator (3)'s freeze checks on the DH1 base show that step 2's parser carries it (condition A) and that no signed `/v8` release document exists in run evidence or the ledger (condition B) (§10, §12). DH2 is decided at freeze, before dispatch. Every `/v8`-gated step-2 and step-3 check then stays active on C′-final with no gate edit. C′-final pairs as `/v8` already does (C′ card `:332-:335`), so no allow-list edit is needed.
- **Fallback (i):** a new revision beside `/v8` in `release_schema.py`. It joins the §0 allow-lists and pairs as `/v8` does (instance `/v2`, profile `/v7`, budget profile `/v3`, checkpoints [N1, N2, PART_A]). Every step-2 and step-3 gate accepts "`/v8` or any later revision that binds the full map" (§2.7, §2.10). `/v1`–`/v8` parse and pair as before.
- **Either form:** case 11 shows a step-2 check and a step-3 check active on C′-final.

**Measured-closure admission: D5, and G-C3 only outside it.**
- `ops/c1_rail/qualification/execution/release_schema.py` is in the 68-module Stage 1c measured closure (Appendix). **D5 admits it.** Joshua ruled D5 YES directly (2026-10-02 ~23:20Z, "yes"; C′ card `:249`) for C′ edits to `release_schema.py`, `runtime.py`, `worker.py`, `campaign_probe.py` and `protocol.py`, and C′-final is part of the C′ build (A1 `:306`; ledger `:2146`, "D5 for the C′ build"). Under DH2 (ii) no `release_schema.py` edit is expected; under (i), D5 covers the new revision.
- **Gate G-C3 (PENDING Joshua, only if it has members):** any measured-closure member this card edits outside D5's five files. At `7e409df`, and at the H9 head `f237178` (closure table run for this fold: 68 measured, 63 staging), no §2.10 file outside D5's five is a member; that includes the listed DH2 (i) gate sites. The candidates on the DH1 base are `runtime_identity.py` (absent on every ref; it joins if step 2 or 3 makes a measured module import it), any §2.10 file that step 2 or 3 pulls into the closure, and, under DH2 (i), any gate site finding (e) adds outside D5's five files.
- Coordinator (3) runs the closure table on the DH1 base at freeze (§10). Each member outside D5 goes to Joshua under the [C3 decision rule](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--c3-accepted-s5-accepted-for-test_only-on-landing-2026-10-01), and the card is not dispatchable until he admits it. With no such member, G-C3 is void. Finding (f) re-confirms; a new member is a stop (§7). Coordinator (3) presents the gate. A relayed yes does not count.

**Re-measurement (ENG-2 option C, ledger `:983`).** An admitted edit joins the closure changes covered by the one PART_A re-measurement on the integrated pre-S8 head, which coordinator (3) owns. R1 carries the unmeasured-closure caveat.

### 2.7 Gating

- **Post-install checks** run only when the installed release is `/v8` (C′ card `:308`); under DH2 (ii), C′-final is `/v8`. Under DH2 (i), every step-2 and step-3 gate site, and this card's, accepts "`/v8` or any later revision that binds the full map".
- **PRE_RELEASE checks** cannot be gated on a release, because none exists yet. They run only under the R1 selector: `--r1` in the runner, and `FP_QUALIFICATION_R1=1` in conftest (#627 sets it and pops it in every other mode at `:241-:242`). No new environment variable is added.
  - **Controller side:** the R1 caller (the runner under `--r1`, conftest under `FP_QUALIFICATION_R1`) sets an in-process gate once. `owned_command`, `start_owned`, `run_owned` and `cleanup` read it. It is off by default.
  - **Child side:** `run_owned` and `start_owned` pass only `owned_environment()` (`host.py:325-:327`), so the variable never reaches a child. The gate reaches children as an R1-only argv flag, on every admin launch (`fixture_install.py`) and on the R1 wrapper program (§2.4).
  - The supervisor's bootstrap self-check gates on the installed release, read with the standard library before any import (C′ card `:308`), and needs no flag.
- **Every other mode** (`--test-only`, `--s2`…`--s5`, `--host-only`) **and every `/v1`–`/v7` installation:** no host-side C′ check runs. The argv bytes, `record.json` keys and evidence are byte-identical. The private provisioning manifest's one added key (§2.1) is the only change in those modes.

### 2.8 Linux file, conftest wiring and registration

- **The Linux file.** Write `tests/integration/qualification_boundary/test_runtime_identity_linux.py` at `CPRIME_CASE`. Under R1 it covers:
  - the real launches of §2.2–§2.5;
  - C′-final's full map;
  - the step-2 and step-3 entries' checks on the real host;
  - a mismatch case per entry, where the host allows one.

  It skips only off-host, through the `real_boundary` fixture. Under `--r1` it has zero skips.
- **`conftest.py`:** under `FP_QUALIFICATION_R1`, install C′-final (beside step 3's role installation, DH7) and run §2.3's admin checks. With the variable unset, every mode installs and collects exactly as on the base.
- **`fixture_install.py`:** the C′-final install path, §2.3's PRE_RELEASE → C′-final binding check, and the admin self-check.
- **Registration:** register the file's nodes in `tests/ops/qualification/invariant_manifest.json` under an existing row. The row IDs are closed; QEXEC-01 is proposed. #627 already keeps these nodes out of every non-R1 required set. Once the file and its rows exist, `r1_refusal` stops naming `CPRIME_CASE`.

### 2.9 Coverage export

A versioned C′ coverage export in the run's evidence, holding:
- every ruled entry as `COVERED`, with `PRE_RELEASE` where §2.2, §2.3 or §2.4 applies, and both wrapper tuples;
- `NOT_COVERED` only for the residual's classes, with the wrapper launches outside the run (§2.4) named as unchecked;
- each recheck of §2.11, with its transition and verdict;
- the expected identity contract (C′-final's `release_sha256` and the provisioning record digest) and the observed coverage;
- the residual's name.

This defines the schema the R1 reader waits for (R1 tooling card `:110`, `:212`). Replacing the reader's `cprime_coverage_export_check_owed` is DH6.

### 2.10 Files

The closure column gives membership at `7e409df` (Appendix); finding (f) re-runs it on the base.

**New:**

| File | Purpose | Measured 68 |
|---|---|---|
| `tools/qualification_verification/interpreter_identity.py` (proposed, DH5) | standard-library identity-tuple producer for the host-side sites | no |
| `tests/integration/qualification_boundary/test_runtime_identity_linux.py` | the C′ Linux file (`CPRIME_CASE`); collected only on Windows | no |
| `tests/test_qualification_host_identity.py` | Windows red→green cases for §2.1–§2.5 | no |

**Edit, each limited to its stated purpose:**

| File | Purpose | Measured 68 |
|---|---|---|
| `tools/qualification_verification/host.py` | §2.1 record (one private manifest key; `public_observations` unchanged); §2.4 wrapper checks, the R1 wrapper program and the in-process gate (§2.7) | no |
| `tools/qualification_verification/campaign_host.py` | §2.5 supervisor parent and its exit evidence (finding (d)) | no |
| `scripts/qualification_boundary_verification.py` | §2.2 pre-spawn, the in-process gate and evidence at `:252-:259` only; no change to modes, case tuples, scopes, environment or required sets. Also a #609 file (§9.3, item 16) | no |
| `scripts/record_verification.py` | §2.2 opt-in post-exec observer at `:211` | no |
| `deploy/qualification/bootstrap.py` | §2.5 `supervisor` self-check; under DH2 (i), the widened gate of step 2's self-check (§2.7) | no |
| `tests/integration/qualification_boundary/conftest.py`, `fixture_install.py`, `fixture_producer.py` | §2.3 (with the R1-only argv flag), §2.6, §2.8 | no |
| `tests/ops/qualification/invariant_manifest.json` | §2.8 registration | not Python |
| `ops/c1_rail/qualification/execution/runtime_identity.py` (step 2's) | full-map entries, the `PRE_RELEASE` label, coverage labels, the supervisor in the recheck set (§2.11); under DH2 (i), the widened gate | absent at `7e409df`; finding (f); G-C3 if a member |
| `ops/c1_rail/qualification/execution/release_schema.py` | DH2 (i) only: the C′-final revision. Under (ii), none expected (condition A, §10; finding (e)) | **YES: admitted by D5** |
| `ops/c1_rail/qualification/execution/release.py` | the full-map tuple check in step 2's pure validator; under DH2 (i), C′-final pairing (instance `/v2` only) | no |
| `ops/c1_rail/qualification/evidence.py` (not `execution/evidence.py`, which is in the 68) | DH2 (i) only: admit C′-final at the three G5 allow-lists | no |
| `ops/c1_rail/qualification/execution/service.py`, `campaign_store.py` | DH2 (i) only: admit C′-final at the release pairings. `campaign_store.py` also takes the supervisor's VALID→VOID recheck at the D9 chokepoint, only as needed (§2.11) | no |
| DH2 (i) only, **at least** these gate sites: `ops/c1_rail/qualification/execution/campaign_supervisor.py`, `launcher.py`, `campaign_result.py`, `campaign_seal.py`, `g5_result.py`, `seal_service.py` | the gate predicate of each step-2 and step-3 check and recheck ("`/v8` or any later revision that binds the full map"); nothing else. Finding (e) re-derives the full list on the base; a site that no row covers is a §7 stop | no, at `7e409df` and `f237178` (the last four exist only on H9); finding (f) |

**Extend in place, never replace:** the existing test files in the authority block.

**P7:** none of these files, the listed DH2 (i) gate sites included, is in the T00 P7 first-party closure: the 40 modules at C′ card `:260-:265`, plus the three static additions at `:393`. The intersection is empty at `7e409df`.

### 2.11 Rechecks (ledger `:2030`; A1 `:296`, `:316`, `:353`)

- **Service supervisor (this card).** Its tuple joins step 2's recheck set at every authority transition its process commits, VALID→VOID included (finding (a) lists them). The VALID→VOID recheck is uncharged. A mismatch refuses the automatic VOID commit and leaves the campaign for the operator-recorded VOID path (D9), never with authority to PASS. Sites: step 2's recheck code in `runtime_identity.py` and, only as needed, the D9 chokepoint in `campaign_store.py`. Case 12.
- **RESULT G5 at the result transition and qseal at the seal transition, from C′-final on** (A1 `:316`). Step 3 builds their checks and rechecks, inert while they are `NOT_COVERED` (step-3 draft §2.5 and D8; DH7). This card activates them by binding their tuples in C′-final, and owns the red case (case 12). If finding (g) shows that step 3 landed none, stop: NEEDS_CONTEXT.
- **Runner/pytest admin fixture and owned-command wrapper: none applies.** They commit no authority transition, and the admin launches produce only TEST_ONLY approvals, never outcomes (`fixture_install.py:1-:5`). Each launch carries its own pre-spawn, self, post-exec and exit evidence, which the coverage export binds. Coordinator (3) acknowledges this at finding (a).

## 3. Method

- **Tests first.** Each §4 red case fails on the base, with a launcher record, then passes on the build. Preservation cases get no fabricated red record.
- **Pinned vectors are extended, never replaced:** release `/v1`–`/v8`, supervision `/v2` and step 2's event versions, RESULT/SEAL `/v1`, and DB10.
- **Windows only.** `/proc`, systemd, cgroups, UIDs and real interpreters are injected fakes (the accepted `_loader=` and fake-runner pattern). Their real counterparts are nodes of the Linux file.
- **No recovery.** A mismatch, timeout or exhaustion refuses once. There is no retry, relaunch, refresh or replacement (D3 = B, §9). A bounded wait for an exec to be seen (finding (c)) is part of one check, not a retry.

## 4. Acceptance checks (falsifier-first)

**H:** with this card built on the DH1 base:
- every R1 launch of the runner/admin fixture, the service supervisor and the owned-command wrapper is checked pre-spawn, by the child and post-exec, with exit evidence and a versioned record;
- the expected identity is the provisioning record before install (PRE_RELEASE) and C′-final after it;
- C′-final binds every ruled entry, and every step-2 and step-3 check stays active on it;
- the applicable rechecks (§2.11) run;
- every non-R1 mode and every pre-`/v8` installation is byte-identical, except for the private manifest's one added key.

**Reject if:** a red case cannot fail on the base, or fails on the build; a preservation case changes outcome; any existing acceptance test changes outcome. **Revert trigger:** any pre-existing receipt, evidence shape, record shape (other than the private provisioning manifest's one added key, case 1), owned-command argv or budget value differs at the build head.

**Red → green:**
1. **Provisioning record:** the private manifest gains exactly one key, a sibling of `runtime`, carrying every §2.1 field (both wrapper tuples included). Every existing key and value is unchanged, in every mode, and `cleanup` accepts manifests with and without the key. A record without the fields refuses every check that needs them.
2. **Runner pre-spawn (PRE_RELEASE):** under `--r1`, a mismatch in any one field (executable bytes, base interpreter, `pyvenv.cfg`, `.pth` inventory, lock, wrapper, UID) refuses before `record.execute`, one case per field. A match records the label `PRE_RELEASE`.
3. **Runner post-exec:** a mismatched or unreadable `/proc` image after the Popen refuses. The observation binds the exec'd payload, not the wrapper, through finding (c)'s binding. An exec not seen within the fixed bound refuses once, with no second launch.
4. **Admin launches:**
   - `install` is checked against the provisioning record and labelled `PRE_RELEASE`;
   - `prepare` and `void-approval` are checked against C′-final;
   - a C′-final whose runner/admin or wrapper tuple differs from the provisioning record refuses at install;
   - a later mismatched admin launch refuses;
   - the admin self-check runs only with the R1-only argv flag, and refuses a mismatched interpreter.
5. **Wrapper:** pre-spawn and self-check mismatches refuse. The self-check runs before `execv`, in the R1 wrapper program, only with the R1-only argv flag. One case per interpreter: a venv launch matches the venv tuple, a base-interpreter launch (`build_worker`'s, the runner's cleanup) matches the base tuple, and any other interpreter refuses. A payload that is not a mapped entry is labelled `NOT_COVERED`.
6. **Supervisor:** a mismatch at pre-spawn, at the `supervisor` bootstrap self-check, or at the MainPID post-exec check each refuses. Missing exit evidence (finding (d)'s source) refuses coverage. A versioned host-side event exists for the launch, for each check and for the exit.
7. **C′-final:** `parse_release` and the pure pairing validator accept C′-final with instance `/v2`. They refuse C′-final with instance `/v1`, and a C′-final missing any of the eleven ruled entries or either wrapper tuple. A release that labels a ruled entry `NOT_COVERED` is refused as C′-final: under DH2 (ii) by the R1 install check, since step 2's `/v8` vectors keep their labels; under (i) by the parser. The G5 evidence builders accept C′-final for N1, N2 and PART_A.
8. **Coverage export:** it lists every ruled entry as `COVERED` (with `PRE_RELEASE` where it applies) and never claims an unchecked launch. It labels a native or tzdata change and an unmediated descendant `NOT_COVERED`, and it names the residual.
9. **Fail closed, no recovery:** a check timeout or exhaustion refuses with no retry or relaunch. A missing C′-final entry refuses.
10. **Linux file:** it collects on Windows (count reported) and skips there. Its runner behaviour is preservation (item 17).
11. **C′-final keeps step 2 and step 3 active (review P1):** on an installed C′-final, in either DH2 form, a step-2 launch check (N1 G5 pre-spawn) and a step-3 check (the RESULT G5 launch check) each run and refuse a mismatch. Neither is skipped, and neither refuses C′-final as an unknown revision. Under DH2 (i) this is red on the base, which refuses or skips the new revision.
12. **Rechecks (§2.11):** on C′-final, a supervisor mismatch at VALID→VOID refuses the automatic VOID commit, uncharged, and leaves the operator-recorded VOID path. A RESULT G5 mismatch at the result transition and a qseal mismatch at the seal transition each refuse. On a step-2-shaped `/v8`, RESULT G5 and qseal stay `NOT_COVERED` (owed) and are never claimed.

Under DH2 (ii), any part of cases 7, 11 and 12 that already passes on the base with a test-built full-map `/v8` is reclassified as preservation and reported (§7).

**Preservation (green on the base and on the build):**
13. **Gate off:** in every non-R1 mode and on `/v1`–`/v7` installations, these are byte-identical: owned-command argv, `ENTER_PROCESS_GROUP`, `fixture_install.py`'s argv, `record.json` keys, `campaign_host.restart`'s argv, and the evidence, including `evidence/host-observations.json` (DH3). The private manifest's one added key (case 1) is the only shape change in any mode. `bootstrap.py` reads nothing new.
14. The release `/v1`–`/v8` vectors, supervision `/v2` and step 2's event vectors, and the frozen RESULT/SEAL and DB10 tests pass unchanged. Step 2's and step 3's acceptance sets keep their outcomes.
15. An exact historical retry writes nothing and returns byte-identical receipts.
16. **Disjointness:** `git diff --name-only <base>..HEAD` is disjoint from the P7 closure (40 plus the three static additions), from #611's files, from #609's files other than `scripts/qualification_boundary_verification.py`, and from `scripts/s2_run_evidence.py`, `scripts/guard_s2_runs.py` and `.github/**`. In that shared runner file, this card's hunks lie inside the runner's launch region (`:252-:259` at `7e409df`, re-anchored at freeze). Textual overlap with #609's `main()` hunks is resolved by rebase (§9.3) and is not a failure. The closure table at the head shows only D5- or G-C3-admitted measured modules changed (Appendix).
17. **Linux file in the runner** (#627 behaviour on tree fixtures, `tests/test_qualification_boundary_verification.py:609-:687`): on a tree fixture that has the file and its rows, `--test-only` ignores it, its nodes stay out of every non-R1 required set, and `r1_refusal` no longer names `CPRIME_CASE`.

**Runs.** Each runs through the launcher from the build worktree and cites its `record.json` with `status: completed`, exit 0 and `source_stable`:
- `python -I scripts/fp.py --workers 2 python -m pytest <the authority-block acceptance set> -q`
- `python -I scripts/fp.py --workers 2 python -m pytest tests/ops/qualification tests/test_qualification_*.py tests/test_record_verification.py -q`
- `python -I scripts/fp.py test` (the full suite)
- `python -I scripts/fp.py check` (any pre-existing failure is disclosed, not called a pass)
- `python -I scripts/fp.py python -m pytest --collect-only -q tests/integration/qualification_boundary/test_runtime_identity_linux.py` (the count only)
- `git diff --check`

## 5. Forbidden

- Any T00 P7 closure file. Any measured-closure module admitted by neither D5 nor G-C3. Making a measured module import a new module.
- Changing frozen wire families (RESULT/SEAL `/v1`, supervision `/v1`–`/v2` and step 2's versions, the snapshots), DB10, budgets, deadlines, allowances, profiles, ceilings or the base pin.
- Changing R1 tooling semantics: modes, `R1_CASES`, scopes, environment variables or the required-set derivation; editing `scripts/s2_run_evidence.py`, `scripts/guard_s2_runs.py` or `.github/**`.
- Any recovery, relaunch, retry, refresh or replacement path (D3 = B).
- Step 3's scope (term 8, result-role funding, faults, `result_g5` and qseal provisioning), B4 (#655), #611, #609, R2 and K3/RC-4.
- Any Linux run, workflow dispatch, PR, merge or push to `main`; any host, vendor or account action.
- Committing or quoting private bytes, host-provisioning artefacts or credentials.
- `core/`, `lab/`, Pine and ports.

## 6. Return (status taxonomy)

Return DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED. The coordinator's verdict is RESOLVED (every §4 item holds on re-run) or FALSIFIED (named items fail and are returned). The return holds:
- the branch, head, base and range-diff; `git diff --stat` and the name list;
- Phase-0 findings (a)–(g);
- finding (e): the frozen DH2 form re-confirmed on the base and, under (i), the full gate-site list;
- for each §4 case, the fail-on-base and pass-on-build record IDs, and the preservation records;
- the closure table at the head and the item-16 output;
- the Linux file's collected count and the registered node IDs;
- the coverage export's schema and one TEST_ONLY example;
- concerns.

## 7. Stop conditions (return to the coordinator; do not work around)

- After Phase-0 findings (a)–(g): return them and wait for the coordinator.
- A P7 file, an unadmitted measured module, a frozen family, DB10, a budget or the pin would have to change.
- A host-side check would need governance code to import `ops`, or supervisor events would need a store or DB10 change.
- Finding (e) contradicts the frozen DH2 form (condition A fails on the base), or shows that C′-final cannot bind an entry whose producer step 3 did not land: NEEDS_CONTEXT.
- Under DH2 (i), finding (e) names a gate site that no §2.10 row covers, for example in `runtime.py` (D5; C′ card `:256`) or a `service.py` gate beyond its pairings (`measure_runtime(..., 'supervisor', release)`, `service.py:1354` at `7e409df`). Coordinator (3) adds the row first: a D5 file needs only the row; any other measured member also needs G-C3's admission (§2.6).
- Finding (g) shows that step 3 landed no RESULT G5 or qseal check or recheck to activate (§2.11): NEEDS_CONTEXT.
- Covering a launch outside the run (§2.4) would need a workflow or environment change.
- A red case cannot fail on the base: reclassify it as preservation and report it. Do not fabricate red evidence.
- Two failed corrections of the same issue (AGENTS.md).
- **Operator review-round rule (2026-10-02):** after more than three review rounds that each return two or more P1/P2 findings, stop; the coordinator adjudicates.
- **Single writer:** a second writer on the build branch is a stop.

## 8. Out of scope and decision unlocked

**Out of scope:** the R1 Linux run and its grant; the R1 reader's coverage check (DH6); the ENG-2 re-measurement (coordinator (3)); step 3; B4; R2; T06/S8; any production use.

**Unlocked:** once the Windows evidence is RESOLVED, the coordinator folds the C′ Linux nodes into R1's node set. C′ is RESOLVED for R1 when step 2, step 3 and this card are all RESOLVED and integrated (C′ card `:195`). The R1 grant still waits on its other gates (staged acceptance `:535-:551`; R1 tooling card `:200`) and on Joshua's express grant.

## 9. Determinations for coordinator (3)

1. **Measured closure.**
   - At `7e409df`, of the §2.10 files only `ops/c1_rail/qualification/execution/release_schema.py` is in the 68-module measured closure; it is also in the 63-module staging closure.
   - The listed DH2 (i) gate sites are in neither closure, at `7e409df` or at the H9 head `f237178`.
   - **D5 admits `release_schema.py`.** Joshua ruled it YES directly (2026-10-02 ~23:20Z; C′ card `:249`), and C′-final is part of the C′ build (A1 `:306`; ledger `:2146`). Coordinator (3) confirms D5's scope at freeze.
   - **G-C3 shrinks** to any measured member outside D5's five files that the freeze closure run on the DH1 base names, for example `runtime_identity.py` (absent at `7e409df`). For those, G-C3 is PENDING Joshua; with none, it is void.
   - **ENG-2 re-measurement is routed to coordinator (3)** (ledger `:983`): one PART_A re-measurement on the integrated pre-S8 head. R1 carries the unmeasured-closure caveat.
2. **T00 P7 disjointness.** At `7e409df`, the §2.10 list is disjoint from the 40-module P7 first-party closure and its three static additions. Item 16 re-checks it at the head.
3. **Sequencing.**
   - **Lane D step 3** (`claude/lane-d-step3-card@3aefa6d`, DRAFT, unmerged) provisions `result_g5` and qseal. C′-final binds both, so this card freezes only after step 3 is RESOLVED. The two cards share `bootstrap.py`, `campaign_host.py`, `conftest.py`, `fixture_install.py`, `fixture_producer.py`, `runtime_identity.py`, `release_schema.py`, `service.py`, `campaign_store.py` and `invariant_manifest.json`, so they run sequentially with a single writer. The step-3 draft predates A1 revision 4: it still calls `test_runtime_identity_linux.py` "step 2's" and registers "the D8 C′ identity Linux nodes" (its `:68`, `:193`, `:200`). Its D3 also leaves "whether the `seal` process role enters `/v8` or a later release revision" OWED (`3aefa6d:412`). That conflicts with A1 `:306` (step 3 ships no revision) and with this card's single C′-final. DH7 reconciles both at step 3's freeze.
   - **B4** (#655, merged at `dfe673a`; the B4 card it added is DRAFT): its release is allocated after C′-final (B4 card `:31`, `:85-:86`), and `/v7`, `/v8` and C′-final keep plan-only behaviour. This card allocates C′-final first (`/v8` itself under DH2 (ii)), and B4 takes the next revision. This card does not wait for B4.
   - **#627** (merged): this card fills `CPRIME_CASE` and its rows and changes no tooling semantics. **#609** (S8 harness, DRAFT) also edits `scripts/qualification_boundary_verification.py`; whichever lands second rebases (item 16 carves this file out).
4. **D3 = B** (Joshua, directly to coordinator (3), 2026-10-03 20:19Z: "D3 = B"). Its ledger record is coordinator (3)'s ledger PR #656, merged at `822c3ea` (2026-10-03T22:13Z). H9 R2 compute recovery is deferred for first production. This card adds **no** recovery, relaunch, retry or replacement path. Every identity mismatch, timeout or exhaustion is a single refusal.
5. **R1 independence.** R1 stays independent of B4 (operator ruling 2026-10-02, sitting 1; staged acceptance `:534`) and of D3/R2 (the #655 recovery note leaves R1 independent under either D3 branch). Nothing in this card makes B4 or R2 an R1 prerequisite.

## 10. Audit hooks (runnable)

```bash
# Card form and authority. Expected: well-formed; exit 0.
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-03-cprime-host-integration-card-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-03-cprime-host-integration-card-DRAFT.md
# Premise (Git Bash), in the build worktree; BASE is the DH1 answer.
git rev-parse HEAD; test ! -e .env && echo "no .env" || echo "FAIL: .env present"
grep -n "CPRIME_CASE\|FP_QUALIFICATION_R1" scripts/qualification_boundary_verification.py   # #627 on the base
# The provisioning record today (expected at 7e409df: no interpreter identity fields).
grep -n "manifest\['runtime'\]" tools/qualification_verification/host.py
# Closure membership on the base (68 measured / 63 staging at 7e409df); D5 admits release_schema.py; G-C3 covers any other allowed member.
python -I scripts/fp.py python <scratch>/stage1c_closure_table.py . "$BASE" HEAD
# DH2 condition A: coordinator (3), at freeze, on the DH1 base; DH2 is decided here, before dispatch.
# Expected: step 2's /v8 vectors keep their outcomes, and a full-map probe passes parse_release and the pure
# pairing/tuple validator. The probe takes fixture_producer's /v8 output (the step-2 entries plus NOT_COVERED
# labels for the five names), replaces the five NOT_COVERED labels with bound tuples (the wrapper with a venv
# and a base tuple), and re-signs it with the TEST_ONLY keys. Any refusal or changed vector fails A. The probe is
# a pytest file under the worktree's gitignored local_artifacts/, run through the launcher; the A1 revision cites
# its record.json and the probe's SHA-256, both copied to the primary checkout's local_artifacts/ before the
# worktree is retired.
python -I scripts/fp.py python -m pytest tests/ops/qualification/execution/test_release.py -q
python -I scripts/fp.py python -m pytest local_artifacts/cprime-probe/test_cprime_final_v8_probe.py -q
# DH2 condition B: coordinator (3), at freeze, after `git fetch origin`. B holds when no SIGNED /v8 release
# document (a release.json with schema qualification_execution_release/v8 and its approval) exists in run
# evidence or the ledger. Allowed matches: this card (and copies or reviews of it); step 2's release_schema.py
# /v8 entry, the allow-lists and checks that admit /v8 (§0 item 2) and its pinned /v8 vectors; the C′ card; and any
# document whose approval is signed only with the TEST_ONLY keys (local pytest output, never a release).
# Any other match is inspected; only a signed /v8 release document fails B. The pattern must not start
# with "/": Git Bash converts such arguments to paths.
P='execution_release/v8'
# B.1 The ledger at the base. Expected: no line (its /v8 lines :711, :1382, :1468 are the S5 snapshot /v8).
git grep -nF "$P" "$BASE" -- docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md
# B.2 Run evidence: .cache/ (the fp-verification records included) of every worktree of the primary
# checkout, lane D's and the H9 Codex worktree C:/Users/joshu/.codex/worktrees/h9-t05-integration included.
# Expected: no file.
for wt in $(git worktree list --porcelain | sed -n 's/^worktree //p'); do grep -rlF "$P" "$wt/.cache" 2>/dev/null; done
# B.3 Retained run artifacts downloaded locally: s2_run_evidence.py's download folders (s2-* under the temp root,
# and any --dest used). Local pytest temp folders are not run evidence. Expected: no file.
find "$(python -c 'import tempfile; print(tempfile.gettempdir())')" -maxdepth 1 -type d -name 's2-*' -print0 2>/dev/null | xargs -0 -r grep -rlF --include=release.json "$P"
# B.4 Unexpired GitHub qualification and S5 artifacts: download and search each one whose run head's
# release_schema.py admits /v8 (parse_release refuses any other revision). Expected: no file.
gh api "repos/Joshua-Asante/first-passage/actions/artifacts?per_page=100" --paginate \
  --jq '.artifacts[]|select(.expired|not)|select(.name|test("^(qualification|s5-part-a)"))|[.workflow_run.id,.name,.workflow_run.head_sha]|@tsv' |
  while IFS=$'\t' read -r run name head; do
    git grep -qF "$P" "$head" -- ops/c1_rail/qualification/execution/release_schema.py &&
      gh run download "$run" -n "$name" -D "<scratch>/$run-$name" && grep -rlF "$P" "<scratch>/$run-$name"
  done
# B.5 History. Expected: allowed matches only.
git log --all --oneline --name-only -S"$P"
# Scope at return. Expected: no workflow, R1-reader, core or lab path.
git diff --stat "$BASE"...HEAD
git diff --name-only "$BASE"...HEAD | grep -E '^(\.github/|scripts/(s2_run_evidence|guard_s2_runs)\.py|core/|lab/)' && echo "FAIL: forbidden path" || echo "scope ok"
```

## 11. Prerequisites (all before dispatch)

1. **D5 and G-C3:** coordinator (3) confirms that D5 admits the `release_schema.py` edit, and runs the closure table on the DH1 base. Any measured member outside D5's five files needs Joshua's direct C3-rule admission, recorded by coordinator (3). **PENDING only if such a member exists** (none at `7e409df` or `f237178`).
2. **DH4:** Joshua's ruling on the supervisor-parent event route (§12), presented by coordinator (3). **PENDING.**
3. Lane D steps 2 and 3 RESOLVED and integrated. That head is DH1.
4. This card frozen: §12 answered, DH2 by coordinator (3)'s freeze checks of conditions A and B on the DH1 base (§10) and recorded on the C′ card as an Amendment A1 revision (owners, above); citations re-anchored; the card committed and its SHA in the ledger; DH7 reconciled with the step-3 freeze.
5. The rulings recorded on `main`: D3 = B through coordinator (3)'s ledger PR #656 (merged at `822c3ea`), and D11 = (a) through coordinator (4)'s ledger PR #658 (owed on `main` until it merges).

## 12. Open decisions (for coordinator (3) at freeze)

- **DH1 Base and branch.** Recommended: the H9 branch head once step 3 is RESOLVED (or `main` once H9 integration lands), on a new `claude/cprime-host-integration` build branch. The coordinator integrates.
- **DH2 C′-final form. Coordinator (3)'s preference: (ii), C′-final IS `/v8` with the full map,** on two conditions:
  - (A) Step 2's `/v8` parser, as built on the DH1 base, carries bound tuples for the five `NOT_COVERED` names, the wrapper with one tuple per interpreter, and every step-2 `/v8` vector keeps its outcome. **Coordinator (3) checks A itself on the DH1 base at freeze** (§10), so DH2 is decided before dispatch; finding (e) only re-confirms it. **Undetermined at this fold:** the parser exists on no ref, and `release_schema.py`'s latest revision is `/v7` (`:30`) on `main` and on every branch.
  - (B) No **signed** `/v8` release document (a `release.json` with schema `qualification_execution_release/v8` and its approval) exists in run evidence or the ledger, checked against the evidence (§10). **Holds at this head** (the §10 check, run for this fold on 2026-10-03 at `32e5905`):
    - the ledger (`main@dfe673a`): no `execution_release/v8` line; its `/v8` lines `:711`, `:1382`, `:1468` are the S5 *snapshot* `/v8`, a different family;
    - run evidence: no match in `.cache/` of any worktree registered to the primary checkout (104 of the 250 have one), the H9 Codex worktree `h9-t05-integration`, where lane D runs, included;
    - retained run artifacts: the 1,066 `release.json` files under the temp root name only `/v1`–`/v7`; 9 of them are in `s2_run_evidence` download folders and the rest are local pytest output (most beside a TEST_ONLY approval), which B.3 no longer searches. The 2,463 unexpired GitHub qualification and S5 artifacts come from 1,147 run heads. No head's release schema admits `/v8` (`parse_release` refuses any other revision, `release_schema.py:113`), so none was downloaded; the only head whose tree contains the literal is `32e5905`, in this card alone;
    - history: `git log --all -S` finds one commit, `32e5905`, this card's own fold. The card itself contains the literal, an allowed match.

    Coordinator (3) re-runs B at freeze. At the DH1 base, step 2's `/v8` sources and vectors are expected matches too.
  - Under (ii), every `/v8`-gated step-2 and step-3 check stays active on C′-final, and no gate, allow-list or `release_schema.py` edit is expected.
  - **If either condition fails: (i)**, a new revision beside `/v8` in `release_schema.py` (D5 admits it), with gate widening: every step-2 and step-3 check accepts "`/v8` or any later revision that binds the full map". The gate sites join §2.10: at least those listed there. Finding (e) re-derives the full list, and any addition outside D5 joins G-C3 (§2.6, §7).
  - Either way, case 11 shows a step-2 and a step-3 check active on C′-final, and B4 takes the next revision.
- **DH3 Provisioning record shape. Chosen: outside `public_observations`** (review P2-3). The fields go in one new key of the private manifest, a sibling of `runtime`, with its own schema literal. `public_observations`' allow-list is unchanged, so the observations `/v1` envelope and `evidence/host-observations.json` stay byte-identical in every mode. **Why not nest it in `runtime` with its own preservation case:** `runtime` is exported verbatim (`host.py:67-:74`), and provisioning has no mode input, so the evidence of every S2–S5 and `--test-only` run would change. R1 still binds the record through the coverage export's digest (§2.9). The manifest gains the key in every mode (case 1). If a manifest reader needs a closed key set (finding (b)), return at Phase 0. A historical manifest without the key is refused for C′ purposes only.
- **DH4 Supervisor-parent events: Joshua's call.** Proposed: a versioned host-side launch family written by `campaign_host` to root-owned evidence (§2.5). This reads the ruled "versioned supervision events" (ledger `:2030`; staged acceptance `:545`) as a separate event family. A reading of ruled wording is not a coordinator-only freeze decision: coordinator (3) presents it to Joshua, and a relayed yes does not count. The reason for the proposal: the supervisor, runner and admin launches have no `attempt_id` and happen before, or outside, the store, so supervision event `/v2` cannot carry them, and `campaign_host` cannot import `ops`. If Joshua declines, the route returns to the coordinator (§7).
- **DH5 Identity producer.** Recommended: one standard-library module in `tools/qualification_verification/` produces the host-side tuples. `runtime_identity.py` compares bound values and never imports it, so the measured closure cannot grow. A Windows test pins agreement on the fields they share.
- **DH6 Reader check.** Recommended: replacing `cprime_coverage_export_check_owed` in `scripts/s2_run_evidence.py` is a separate follow-up in the R1 tooling lane once this schema lands. It is not this card's.
- **DH7 Shared ownership with step 3.** Recommended split:
  - Step 3 keeps the `FP_QUALIFICATION_R1` seam's role installation, the result/seal Linux file and its registration, its Windows `result_g5`/qseal identity cases, and their checks and rechecks, inert until C′-final (§2.11).
  - This card creates `test_runtime_identity_linux.py` with every C′ Linux node, including `result_g5` and qseal, and registers the C′ nodes.
  - Step 3's D3 leaves "whether the `seal` process role enters `/v8` or a later release revision" OWED (`3aefa6d:412`). The amendment: seal is bound only by C′-final (`/v8` under DH2 (ii), the later revision under (i)), and step 3 ships no release revision (A1 `:306`).

  Coordinator (3) amends the step-3 draft at its freeze.
- **DH8 PR authority.** The coordinator opens PRs; the worker pushes its branch only.
- **DH9 The final file list** and the new test file's name.

## Appendix: the 68-module Stage 1c measured closure at `7e409df` (for item 16)

Produced by the §10 closure table, run with `origin/main@7e409df` against itself: measured 68, staging 63. The same table at the H9 head `f237178`, run for this fold, also gives 68 and 63 with the same `execution/` members; none of the listed DH2 (i) gate sites is a member.
- `core/` (15): `dd_geometry`, `dd_protection`, `firm_rules`, `historical_challenge`, `lib/atomic_io`, `lib/file_lock`, `lib/mvd`, `lib/validation`, `lifecycle`, `mc/__init__`, `mc/ingest`, `mc/modes`, `mc/preflight`, `mc/simulation`, `tv_schema`.
- `ops/c1_rail/` (5): `__init__`, `book_policy`, `book_schedule`, `ed25519_verify`, `policy_fingerprint`.
- `ops/c1_rail/qualification/` (24): `__init__`, `attempt`, `blocks`, `checkpoint_plan`, `clock`, `contract`, `legality`, `model`, `panel`, `part_a`, `paths`, `policy`, `policy_sources`, `preflight`, `production`, `production_source`, `provider`, `regime`, `replay`, `runner`, `seed_identity`, `sessions`, `source_admission`, `trust_domain`.
- `ops/c1_rail/qualification/execution/` (16): `__init__`, `admission`, `budget`, `campaign_budget`, `campaign_probe`, `campaign_protocol`, `compute`, `evidence`, `files`, `keys`, `plan`, `profile`, `protocol`, `release_schema`, `runtime`, `worker`.
- `ops/c1_signal_daemon/` (6): `__init__`, `book_adapters`, `book_protocol`, `feed`, `pine_ta`, `tv_broker_emulator`.
- `tests/ops/qualification/` (2): `test_contract`, `test_trust_domain`.

## Pre-mortem (README rule)

- **Loop cost:** one Windows build loop and its records. No Linux run.
- **Decisions the executor will hit:** DH3, DH5 and DH7, acknowledged in one batch after Phase 0. DH2 is coordinator (3)'s, at freeze (§10); finding (e) re-confirms it, and a contradiction is a stop (§7). DH4 is Joshua's, before dispatch.
- **What makes it moot:** an operator ruling that withdraws the R1 C′ gate or reverses D11.
- **Measurements the return fills in:** findings (a)–(g), the per-case records and the closure table at the head. No numbers are asserted here.
