# H9 C′ host-integration: runner/admin, supervisor-parent and owned-command identity, the C′ Linux file and the single C′-final revision (R1 slice 2)

**Type:** cc_handoff (worker build card)

**Status:** DRAFT, 2026-10-03, drafted by a worker for coordinator (3). **NOT DISPATCHABLE:** gate G-C3 (§2.6) is PENDING Joshua, and the §11 prerequisites are open. Coordinator (3) answers §12, re-anchors every code line on the DH1 base, commits the frozen revision under the committed-handoff rule and records its SHA in the ledger before any worker starts.

**Citation basis.** Code and documents at `origin/main@7e409df` (#624 merged there; Amendment A1 pinned at `f179c0b`; #627 merged at `e9fade0`). Steps 2 and 3 edit several of the same files, so code line numbers are **OWED** re-anchoring at freeze.

**Executor:** one coordinator-dispatched worker (C′ card `:353`), the single writer of its build branch (DH1).

**Coordinator:** coordinator (3), owner of the C′ host-integration lane (R1 slice 2). It owns the freeze, the diff review, integration, PRs, every Linux dispatch and the ledger.

**Owners this card narrows (it changes none of them):**
- C′ obligation, finite map, checks, evidence and residual: [ledger, C′ rulings](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-rulings--t05-environment-sealing-c-and-the-first-release-host-environment-drift-residual-2026-10-02) `:1996-:2047` (map `:2021-:2027`, evidence `:2030`, residual `:2033-:2037`).
- The parent [C′ card](2026-10-02-h9-cprime-runtime-identity-build-DRAFT.md) and its Amendment A1, revisions 1–6: the entries moved here `:344-:351`, the five `NOT_COVERED` owners `:299-:304`, "one final revision" `:306`, gating `:308`, D11 reopened `:355`, the 68-module checkpoint `:118` and item 13 `:146`.
- H9 checkpoint R1: [staged acceptance](2026-09-27-staged-acceptance-handoffs.md) `:534-:551`, `:563`.
- R1 tooling: [card](2026-10-02-r1-tooling-build-card.md) and #627 (`scripts/qualification_boundary_verification.py`: `R1_CASES` and `CPRIME_CASE` `:48-:59`, `r1_refusal` `:115-:140`, the `--test-only` exclusion `:201-:206` and `:248`, `FP_QUALIFICATION_R1` set and popped `:241-:242`).
- **D11 = (a), RULED** (Joshua through coordinator (2), 2026-10-03 05:10Z): "the first runner and admin launches are checked against the host provisioning record (interpreter identity recorded by host.py provisioning), labelled PRE_RELEASE. Later launches are checked against the signed final revision." This supersedes "D11 reopened" (C′ card `:355`). Its ledger record is owed by coordinator (3); it is not on `main` at `7e409df`.

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
  - not_dispatchable_until_g_c3_admitted
  - measured_closure_edits_g_c3_admitted_only
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
```

`identity_branch_only` reads "this card's build branch (DH1)"; `card_section2_files_only` reads "§2.10". `tests/test_qualification_host_identity.py` is new (name fixed at DH9). Step 2's three `test_runtime_identity_*.py` files are extended in place. The Linux file `tests/integration/qualification_boundary/test_runtime_identity_linux.py` is written here and **collected only** on Windows; it runs only inside R1 (§8).

## 0. Phase 0: premise, Rule-0 reads and findings before code

1. **Premise.** HEAD is the DH1 base: lane D steps 2 and 3 RESOLVED and integrated, `origin/main` merged in, range-diff reported. #627 is on the base. No `.env` in the worktree.
2. **Rule-0 reads** (anchors at `7e409df`; read them, do not infer them):
   - `tools/qualification_verification/host.py`: the provisioning venv and record `:638-:676`. `manifest['runtime']` (`:672-:676`) holds only `python`, `version`, `signing_requirements_sha256` and `packages`: no interpreter bytes, base interpreter, `pyvenv.cfg` or `.pth` identity. `public_observations` `:67-:74` exports `runtime` verbatim; `validate_inputs` `:77-:87` checks the lock digests. The owned-command wrapper: `ENTER_PROCESS_GROUP` `:309-:317` (ends in `os.execv`), `owned_command` `:320-:322`, `start_owned` `:330-:333`, `run_owned` `:336-:340`.
   - `tools/qualification_verification/host.json` (`python`, `python_version`, `locks`).
   - `scripts/qualification_boundary_verification.py`: the runner's pytest launch `:252-:259` (`owned_command(..., sys.executable)` `:258`, `record.execute` `:259`); the environment `:224-:242`.
   - `scripts/record_verification.py`: the Popen `:211-:212`, the post-exec site. It records every launcher run, so any change here is opt-in.
   - `.github/workflows/qualification-s2-supervision.yml:136-:143`: the runner runs under `$host_root/env/bin/python` through `fp.py --env`.
   - `tests/integration/qualification_boundary/conftest.py`: the mode flags `:59-:69`; `admin` `:78-:87` (every `fixture_install` launch goes through `host.run_owned(..., interpreter=self.python)`; `install` is the first, from `__init__` `:65-:69`); `restart` `:197-:233` (diagnostic modes use `campaign_host.restart` `:200`, others `host.start_owned` `:220`).
   - `tests/integration/qualification_boundary/fixture_install.py`: the isolated-administrator preamble `:14-:16`; `install` `:35-:90` (`install_release` `:78`).
   - `tests/integration/qualification_boundary/fixture_producer.py:47-:90` (`release_document`; revision chosen by profile at `:79-:86`).
   - `tools/qualification_verification/campaign_host.py`: `restart` `:107-:115` is the supervisor parent (`systemd-run ... interpreter -I bootstrap supervisor`); `cleanup` `:118-:195`. Standard library plus `host` only: governance code cannot import `ops` (`scripts/check_boundaries.py`).
   - `deploy/qualification/bootstrap.py:9-:17` (the off-Linux exit and the role whitelist, which includes `supervisor`); `service.main`, `ops/c1_rail/qualification/execution/service.py:1344-:1355` (`measure_runtime(..., 'supervisor', release)`).
   - `ops/c1_rail/qualification/execution/campaign_supervisor.py:345-:380` (supervision events `/v1`–`/v2` are keyed by `attempt_id` and `work_id`) and `_retain_event` `:540-:553`.
   - The release allow-lists C′-final must join: `release.py:64`; `ops/c1_rail/qualification/evidence.py:966-:971`, `:1349-:1350`, `:2431`; `service.py:97-:163`, `:373-:382`; `campaign_store.py:2374-:2381`.
   - `tests/ops/qualification/invariant_manifest.json`; its row IDs are closed (`scripts/check_qualification_invariants.py:19`).
   - On the base only: step 2's `runtime_identity.py` (map, derivation, labels) and `/v8` parser; step 3's `result_g5` and qseal producers and its `FP_QUALIFICATION_R1` seam.
3. **Findings returned before code** (the coordinator acknowledges each):
   - (a) **Launch inventory** for the three host entries (runner/pytest admin fixture, service supervisor, owned-command wrapper): each launch site as `file:line`, with interpreter, UID and wrapper, and whether it precedes the release install (PRE_RELEASE) or follows it.
   - (b) **Provisioning identity:** which §2.1 fields `host.provision` can record from the venv it creates (DH3), and whether the runner's `sys.executable` is `<root>/env/bin/python` on the workflow path.
   - (c) **Post-exec binding:** how the controller's `/proc` observation binds to the exec'd image rather than the pre-exec wrapper, bounded and without retry.
   - (d) **Supervisor-parent route** (DH4): what `campaign_host` can observe of the unit (MainPID, `/proc`, exit properties) with the standard library, and where its versioned events are retained.
   - (e) **C′-final form** (DH2): whether step 2's `/v8` parser can carry bound tuples for the five `NOT_COVERED` names, and the exact `release_schema.py` lines C′-final needs.
   - (f) **Closures on the base:** the table `docs/notes/2026-09-29-s5-c3-record/stage1c-equivalence/stage1c_closure_table.py.txt` run on the base. Name every §2.10 file in the 68 measured (and 63 staging) modules, explicitly including `runtime_identity.py` and the new tools module, and confirm disjointness from the P7 closure.
   - (g) **Shared-file state after step 3** (DH7): what step 3 landed in `conftest.py`, `fixture_install.py`, `fixture_producer.py`, `bootstrap.py`, `campaign_host.py` and `invariant_manifest.json`.

## 0.5. Routing and clarifying questions

`Routing: local`: a Windows build with Windows evidence. A Claude worker, not `glm_agent`: this is identity and authority code on the protected qualification path (AGENTS.md GLM rule). No secrets, `.env`, Pine, ports or account data are involved. If Phase 0 needs an unanswered §12 decision, return NEEDS_CONTEXT; never assume the answer.

## 1. Goal

Finish C′ at the host so that R1 can run. The three host entries A1 moved here (runner/pytest admin fixture, service supervisor, owned-command wrapper) get the full check set: pre-spawn, child self-check, post-exec `/proc`, exit evidence and a versioned record for each check, with D11 = (a) identity sources. Write the C′ Linux file and register its nodes. Ship the **single final signed revision ("C′-final")**, which binds the whole finite map so that no ruled entry stays `NOT_COVERED`. Every mismatch fails closed. **Scope boundary:** the build branch plus Windows evidence. Linux evidence is R1's (§8).

## 2. Scope

### 2.1 Host provisioning identity record (D11 = (a))

The Docker pin (C′ card §2.1, D3) identifies the worker base image. It says nothing about the host Python that runs the runner and the admin fixture, so the provisioning record must carry that interpreter identity.
- `host.provision` records, beside `manifest['runtime']`:
  - the venv executable's path and the SHA-256 of its bytes (the venv is created with `--copies`);
  - the base interpreter (`host.json` `python`): resolved path and SHA-256;
  - the SHA-256 of `pyvenv.cfg`;
  - the `.pth` inventory of the venv's site-packages (sorted names and SHA-256);
  - the three lock digests (`REQUIRED_LOCKS`, already validated at `:77-:87`);
  - the owned-command wrapper digest (SHA-256 of `ENTER_PROCESS_GROUP`);
  - the Python version.
- The shape and schema literal are DH3. A record without these fields is not a C′ source: every check that needs one refuses.

### 2.2 Runner launch (always PRE_RELEASE)

The runner's pytest launch (`:258-:259`) precedes any release install in the run.
- **Pre-spawn** (under `--r1` only): the runner derives the identity of `sys.executable`, the wrapper and UID 0, and compares it with the provisioning record. A mismatch or a missing record refuses before `record.execute`.
- **Post-exec:** an opt-in observer at the Popen (`record_verification.py:211`) reads the child's `/proc` image (finding (c)) and refuses on mismatch. Without the observer, `RunRecord`'s behaviour and `record.json` keys are unchanged.
- **Child self-check:** the wrapper's (§2.4).
- **Evidence:** a versioned launch record (expected identity, observed identity per check, label `PRE_RELEASE`, verdict, exit) in `record.data['metadata']` and in the run's evidence. The runner's exit evidence is the recorded `exit_code`; if it is missing, coverage refuses.

### 2.3 Admin fixture launches

- The **first** admin launch (`install`, from `Boundary.__init__`) is checked against the provisioning record and labelled `PRE_RELEASE`.
- `install` binds the runner/admin and wrapper tuples into C′-final from that same provisioning record. A C′-final whose tuples differ from the record refuses at install.
- **Later** admin launches (`prepare`, `void-approval`) are checked against C′-final.
- Each admin launch gets the controller's pre-spawn check (conftest), the child self-check (`fixture_install.py`, standard library only, beside `:14-:16`, before any other import), the controller's post-exec `/proc` check, exit evidence (`run_owned`'s return) and a versioned record under `evidence/boundary/`.

### 2.4 Owned-command wrapper

`host.owned_command` launches every owned child as `interpreter -I -c ENTER_PROCESS_GROUP`. Under the gate (§2.7):
- **Pre-spawn:** the wrapper's interpreter and digest match the expected source: the provisioning record before install, C′-final after it.
- **Self-check:** the wrapper checks its own interpreter identity, standard library only, before `os.execv`. A mismatch exits non-zero without exec.
- **Post-exec:** the payload's `/proc` image is checked when the payload is itself a mapped entry. Any other payload is an unmediated descendant and is labelled `NOT_COVERED`, never claimed.
- With the gate off, the argv bytes `owned_command` builds, the `ENTER_PROCESS_GROUP` bytes and the behaviour are all unchanged.

### 2.5 Service supervisor and its parent (`campaign_host`)

Under R1 the supervisor starts through `campaign_host.restart` (`:107-:115`, `systemd-run`) after install, so it is checked against C′-final:
- pre-spawn in `campaign_host.restart`, against the supervisor tuple;
- the bootstrap self-check for role `supervisor` in `deploy/qualification/bootstrap.py` (standard library, before any import, placed where step 2 put its self-check);
- post-exec through the unit's MainPID `/proc` image and its cgroup under the enrolled slice;
- exit evidence from the unit's recorded exit, at stop and at cleanup. If it is missing, coverage refuses.

**Event route (DH4).** The supervisor process has no `attempt_id` or `work_id`, so supervision event `/v2` cannot carry its events, and `campaign_host` cannot import `ops`. Proposed: a versioned host-side launch family, written by `campaign_host` to root-owned evidence. No store, DB10 or `/v2` change.

### 2.6 C′-final, the single final signed revision, and gate G-C3

- **What it binds:** the base-pin hash, the built image ID and **every** ruled entry (ledger `:2021-:2027`) with its tuple. The entries are the runner/pytest admin fixture, the service supervisor, the guardian, control and probes, the N1, N2, PART_A and RESULT G5 roles, qseal, and the owned-command wrapper. No ruled entry is `NOT_COVERED`. That label remains only for the residual's classes (`:2033-:2037`).
- **When:** after step 3's `result_g5` and qseal producers exist (C′ card `:306`). It is produced through `fixture_producer`'s release-revision parameter (C′ card `:324`), which gains the C′-final value.
- **Pairing:** C′-final joins the §0 allow-lists and pairs as `/v8` does (C′ card `:332-:335`): instance `/v2`, profile `/v7`, budget profile `/v3`, checkpoints [N1, N2, PART_A]. `/v1`–`/v8` parse and pair as before.
- **Form:** DH2. The recommendation is a new revision beside `/v8` in `release_schema.py`.

**Gate G-C3: NOT DISPATCHABLE, PENDING Joshua.**
- `ops/c1_rail/qualification/execution/release_schema.py` is a member of the 68-module Stage 1c measured closure (Appendix; run at `7e409df`). Either DH2 form edits it, unless finding (e) shows that step 2's `/v8` parser already binds all eleven entries.
- Following C′ D5 (C′ card `:249`) and step 3's D3 (ledger `:2146`), dispatch therefore needs Joshua's admission of that named edit under the [C3 decision rule](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--c3-accepted-s5-accepted-for-test_only-on-landing-2026-10-01).
- Any further member that finding (f) names joins the same gate. An example is `runtime_identity.py`, if step 2 made a measured module import it.
- Coordinator (3) presents the gate. A relayed yes does not count.

**Re-measurement (ENG-2 option C, ledger `:983`).** An admitted edit joins the closure changes covered by the one PART_A re-measurement on the integrated pre-S8 head, which coordinator (3) owns. R1 carries the unmeasured-closure caveat.

### 2.7 Gating

- **Post-install checks** run only when the installed release is `/v8` or C′-final (C′ card `:308`).
- **PRE_RELEASE checks** cannot be gated on a release, because none exists yet. They run only under the R1 selector: `--r1` in the runner, and `FP_QUALIFICATION_R1=1` in conftest (#627 sets it and pops it in every other mode at `:241-:242`). No new environment variable is added.
- **Every other mode** (`--test-only`, `--s2`…`--s5`, `--host-only`) **and every `/v1`–`/v7` installation:** no host-side C′ check runs. The argv bytes, `record.json` keys and evidence are byte-identical. DH3 governs the provisioning record itself.

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
- every ruled entry as `COVERED`, with `PRE_RELEASE` where §2.2 or §2.3 applies;
- `NOT_COVERED` only for the residual's classes;
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
| `tools/qualification_verification/host.py` | §2.1 record; §2.4 wrapper checks | no |
| `tools/qualification_verification/campaign_host.py` | §2.5 supervisor parent | no |
| `scripts/qualification_boundary_verification.py` | §2.2 pre-spawn and evidence at `:252-:259` only; no change to modes, case tuples, scopes, environment or required sets | no |
| `scripts/record_verification.py` | §2.2 opt-in post-exec observer at `:211` | no |
| `deploy/qualification/bootstrap.py` | §2.5 `supervisor` self-check | no |
| `tests/integration/qualification_boundary/conftest.py`, `fixture_install.py`, `fixture_producer.py` | §2.3, §2.6, §2.8 | no |
| `tests/ops/qualification/invariant_manifest.json` | §2.8 registration | not Python |
| `ops/c1_rail/qualification/execution/runtime_identity.py` (step 2's) | full-map entries, the `PRE_RELEASE` label, coverage labels | absent at `7e409df`; finding (f) |
| `ops/c1_rail/qualification/execution/release_schema.py` | the C′-final revision (DH2) | **YES: gate G-C3** |
| `ops/c1_rail/qualification/execution/release.py` | C′-final pairing (instance `/v2` only) | no |
| `ops/c1_rail/qualification/evidence.py` (not `execution/evidence.py`, which is in the 68) | admit C′-final at the three G5 allow-lists | no |
| `ops/c1_rail/qualification/execution/service.py`, `campaign_store.py` | admit C′-final at the release pairings | no |

**Extend in place, never replace:** the existing test files in the authority block.

**P7:** none of these files is in the T00 P7 first-party closure: the 40 modules at C′ card `:260-:265`, plus the three static additions at `:393`. The intersection is empty at `7e409df`.

## 3. Method

- **Tests first.** Each §4 red case fails on the base, with a launcher record, then passes on the build. Preservation cases get no fabricated red record.
- **Pinned vectors are extended, never replaced:** release `/v1`–`/v8`, supervision `/v2` and step 2's event versions, RESULT/SEAL `/v1`, and DB10.
- **Windows only.** `/proc`, systemd, cgroups, UIDs and real interpreters are injected fakes (the accepted `_loader=` and fake-runner pattern). Their real counterparts are nodes of the Linux file.
- **No recovery.** A mismatch, timeout or exhaustion refuses once. There is no retry, relaunch, refresh or replacement (D3 = B, §9).

## 4. Acceptance checks (falsifier-first)

**H:** with this card built on the DH1 base:
- every R1 launch of the runner/admin fixture, the service supervisor and the owned-command wrapper is checked pre-spawn, by the child and post-exec, with exit evidence and a versioned record;
- the expected identity is the provisioning record before install (PRE_RELEASE) and C′-final after it;
- C′-final binds every ruled entry;
- every non-R1 mode and every pre-`/v8` installation is byte-identical.

**Reject if:** a red case cannot fail on the base, or fails on the build; a preservation case changes outcome; any existing acceptance test changes outcome. **Revert trigger:** any pre-existing receipt, record shape, owned-command argv or budget value differs at the build head.

**Red → green:**
1. **Provisioning record:** it carries every §2.1 field. A record without them refuses every check that needs them.
2. **Runner pre-spawn (PRE_RELEASE):** under `--r1`, a mismatch in any one field (executable bytes, base interpreter, `pyvenv.cfg`, `.pth` inventory, lock, wrapper, UID) refuses before `record.execute`, one case per field. A match records the label `PRE_RELEASE`.
3. **Runner post-exec:** a mismatched or unreadable `/proc` image after the Popen refuses. The observation binds the exec'd image, not the wrapper (finding (c)).
4. **Admin launches:**
   - `install` is checked against the provisioning record and labelled `PRE_RELEASE`;
   - `prepare` and `void-approval` are checked against C′-final;
   - a C′-final whose runner/admin or wrapper tuple differs from the provisioning record refuses at install;
   - a later mismatched admin launch refuses;
   - the admin self-check refuses a mismatched interpreter.
5. **Wrapper:** pre-spawn and self-check mismatches refuse. The self-check runs before `execv`. A payload that is not a mapped entry is labelled `NOT_COVERED`.
6. **Supervisor:** a mismatch at pre-spawn, at the `supervisor` bootstrap self-check, or at the MainPID post-exec check each refuses. Missing exit evidence refuses coverage. A versioned host-side event exists for the launch, for each check and for the exit.
7. **C′-final:** `parse_release` and the pure pairing validator accept C′-final with instance `/v2`. They refuse C′-final with instance `/v1`, a C′-final missing any of the eleven ruled entries, and a C′-final labelling a ruled entry `NOT_COVERED`. The G5 evidence builders accept C′-final for N1, N2 and PART_A.
8. **Coverage export:** it lists every ruled entry as `COVERED` (with `PRE_RELEASE` where it applies) and never claims an unchecked launch. It labels a native or tzdata change and an unmediated descendant `NOT_COVERED`, and it names the residual.
9. **Fail closed, no recovery:** a check timeout or exhaustion refuses with no retry or relaunch. A missing C′-final entry refuses.
10. **Linux file:** it collects on Windows (count reported) and skips there. On a tree fixture that has the file and its rows, `--test-only` ignores it, its nodes stay out of every non-R1 required set, and `r1_refusal` no longer names `CPRIME_CASE`.

**Preservation (green on the base and on the build):**
11. **Gate off:** in every non-R1 mode and on `/v1`–`/v7` installations, these are byte-identical: owned-command argv, `ENTER_PROCESS_GROUP`, `record.json` keys, `campaign_host.restart`'s argv, and the evidence. `bootstrap.py` reads nothing new.
12. The release `/v1`–`/v8` vectors, supervision `/v2` and step 2's event vectors, and the frozen RESULT/SEAL and DB10 tests pass unchanged. Step 2's and step 3's acceptance sets keep their outcomes.
13. An exact historical retry writes nothing and returns byte-identical receipts.
14. **Disjointness:** `git diff --name-only <base>..HEAD` is disjoint from the P7 closure (40 plus the three static additions), from #609's and #611's files, and from `scripts/s2_run_evidence.py`, `scripts/guard_s2_runs.py` and `.github/**`. The closure table at the head shows only G-C3-admitted measured modules changed (Appendix).

**Runs.** Each runs through the launcher from the build worktree and cites its `record.json` with `status: completed`, exit 0 and `source_stable`:
- `python -I scripts/fp.py --workers 2 python -m pytest <the authority-block acceptance set> -q`
- `python -I scripts/fp.py --workers 2 python -m pytest tests/ops/qualification tests/test_qualification_*.py tests/test_record_verification.py -q`
- `python -I scripts/fp.py test` (the full suite)
- `python -I scripts/fp.py check` (any pre-existing failure is disclosed, not called a pass)
- `python -I scripts/fp.py python -m pytest --collect-only -q tests/integration/qualification_boundary/test_runtime_identity_linux.py` (the count only)
- `git diff --check`

## 5. Forbidden

- Any T00 P7 closure file. Any measured-closure module not admitted at G-C3. Making a measured module import a new module.
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
- for each §4 case, the fail-on-base and pass-on-build record IDs, and the preservation records;
- the closure table at the head and the item-14 output;
- the Linux file's collected count and the registered node IDs;
- the coverage export's schema and one TEST_ONLY example;
- concerns.

## 7. Stop conditions (return to the coordinator; do not work around)

- After Phase-0 findings (a)–(g): return them and wait for the coordinator.
- A P7 file, an unadmitted measured module, a frozen family, DB10, a budget or the pin would have to change.
- A host-side check would need governance code to import `ops`, or supervisor events would need a store or DB10 change.
- Finding (e) shows that C′-final cannot bind an entry whose producer step 3 did not land: NEEDS_CONTEXT.
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
   - C′-final edits it (DH2), so **Joshua's C3-rule admission of that named edit is a NOT-DISPATCHABLE gate, G-C3, PENDING Joshua**, as C′ D5 and step 3's D3 were.
   - `runtime_identity.py` does not exist at `7e409df`. If finding (f) shows it in the closure on the base, it joins G-C3.
   - **ENG-2 re-measurement is routed to coordinator (3)** (ledger `:983`): one PART_A re-measurement on the integrated pre-S8 head. R1 carries the unmeasured-closure caveat.
2. **T00 P7 disjointness.** At `7e409df`, the §2.10 list is disjoint from the 40-module P7 first-party closure and its three static additions. Item 14 re-checks it at the head.
3. **Sequencing.**
   - **Lane D step 3** (`claude/lane-d-step3-card@3aefa6d`, DRAFT, unmerged) provisions `result_g5` and qseal. C′-final binds both, so this card freezes only after step 3 is RESOLVED. The two cards share `bootstrap.py`, `campaign_host.py`, `conftest.py`, `fixture_install.py`, `fixture_producer.py`, `runtime_identity.py`, `release_schema.py`, `service.py`, `campaign_store.py` and `invariant_manifest.json`, so they run sequentially with a single writer. The step-3 draft predates A1 revision 4: it still calls `test_runtime_identity_linux.py` "step 2's" and registers "the D8 C′ identity Linux nodes" (its `:68`, `:193`, `:200`). DH7 reconciles this at step 3's freeze.
   - **B4** (#655, DRAFT): its release is allocated after C′-final (#655's B4 card `:31`, `:85-:86`), and `/v7`, `/v8` and C′-final keep plan-only behaviour. This card allocates the C′-final revision first and does not wait for B4.
   - **#627** (merged): this card fills `CPRIME_CASE` and its rows and changes no tooling semantics. **#609** (S8 harness, DRAFT) also edits `scripts/qualification_boundary_verification.py`; whichever lands second rebases.
4. **D3 = B** (Joshua, 2026-10-03 20:19Z, relayed by coordinator (3); its ledger record is coordinator (3)'s): H9 R2 compute recovery is deferred for first production. This card adds **no** recovery, relaunch, retry or replacement path. Every identity mismatch, timeout or exhaustion is a single refusal.
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
# Closure membership on the base (68 measured / 63 staging at 7e409df); G-C3 covers every allowed member.
python -I scripts/fp.py python <scratch>/stage1c_closure_table.py . "$BASE" HEAD
# Scope at return. Expected: no workflow, R1-reader, core or lab path.
git diff --stat "$BASE"...HEAD
git diff --name-only "$BASE"...HEAD | grep -E '^(\.github/|scripts/(s2_run_evidence|guard_s2_runs)\.py|core/|lab/)' && echo "FAIL: forbidden path" || echo "scope ok"
```

## 11. Prerequisites (all before dispatch)

1. **G-C3:** Joshua's direct C3-rule admission of the `release_schema.py` edit, and of any further member finding (f) names, recorded by coordinator (3). **PENDING.**
2. Lane D steps 2 and 3 RESOLVED and integrated. That head is DH1.
3. This card frozen: §12 answered, citations re-anchored, the card committed and its SHA in the ledger; DH7 reconciled with the step-3 freeze.
4. The D11 = (a) and D3 = B records entered in the ledger by coordinator (3).

## 12. Open decisions (for coordinator (3) at freeze)

- **DH1 Base and branch.** Recommended: the H9 branch head once step 3 is RESOLVED (or `main` once H9 integration lands), on a new `claude/cprime-host-integration` build branch. The coordinator integrates.
- **DH2 C′-final form.**
  - (i) A new revision beside `/v8` in `release_schema.py`. Recommended; B4 then takes the next revision.
  - (ii) A `/v8` document with every entry bound. Only possible if finding (e) shows step 2's parser already allows it.

  G-C3 applies to either, unless (ii) needs no `release_schema.py` edit.
- **DH3 Provisioning record shape.** Recommended: a nested object with its own schema literal inside `runtime`, leaving the ownership `/v3` and observations `/v1` envelopes unchanged; a historical record without it is refused for C′ purposes only. The alternative bumps the ownership and observations schemas.
- **DH4 Supervisor-parent events.** Recommended: a versioned host-side launch family written by `campaign_host` to root-owned evidence (§2.5). This reads the ledger's "versioned supervision events" (`:2030`) as a versioned event family, because the supervisor, runner and admin launches have no `attempt_id` and happen before, or outside, the store.
- **DH5 Identity producer.** Recommended: one standard-library module in `tools/qualification_verification/` produces the host-side tuples. `runtime_identity.py` compares bound values and never imports it, so the measured closure cannot grow. A Windows test pins agreement on the fields they share.
- **DH6 Reader check.** Recommended: replacing `cprime_coverage_export_check_owed` in `scripts/s2_run_evidence.py` is a separate follow-up in the R1 tooling lane once this schema lands. It is not this card's.
- **DH7 Shared ownership with step 3.** Recommended split:
  - Step 3 keeps the `FP_QUALIFICATION_R1` seam's role installation, the result/seal Linux file and its registration, and its Windows `result_g5`/qseal identity cases.
  - This card creates `test_runtime_identity_linux.py` with every C′ Linux node, including `result_g5` and qseal, and registers the C′ nodes.

  Coordinator (3) amends the step-3 draft at its freeze.
- **DH8 PR authority.** The coordinator opens PRs; the worker pushes its branch only.
- **DH9 The final file list** and the new test file's name.

## Appendix: the 68-module Stage 1c measured closure at `7e409df` (for item 14)

Produced by the §10 closure table, run with `origin/main@7e409df` against itself: measured 68, staging 63.
- `core/` (15): `dd_geometry`, `dd_protection`, `firm_rules`, `historical_challenge`, `lib/atomic_io`, `lib/file_lock`, `lib/mvd`, `lib/validation`, `lifecycle`, `mc/__init__`, `mc/ingest`, `mc/modes`, `mc/preflight`, `mc/simulation`, `tv_schema`.
- `ops/c1_rail/` (5): `__init__`, `book_policy`, `book_schedule`, `ed25519_verify`, `policy_fingerprint`.
- `ops/c1_rail/qualification/` (24): `__init__`, `attempt`, `blocks`, `checkpoint_plan`, `clock`, `contract`, `legality`, `model`, `panel`, `part_a`, `paths`, `policy`, `policy_sources`, `preflight`, `production`, `production_source`, `provider`, `regime`, `replay`, `runner`, `seed_identity`, `sessions`, `source_admission`, `trust_domain`.
- `ops/c1_rail/qualification/execution/` (16): `__init__`, `admission`, `budget`, `campaign_budget`, `campaign_probe`, `campaign_protocol`, `compute`, `evidence`, `files`, `keys`, `plan`, `profile`, `protocol`, `release_schema`, `runtime`, `worker`.
- `ops/c1_signal_daemon/` (6): `__init__`, `book_adapters`, `book_protocol`, `feed`, `pine_ta`, `tv_broker_emulator`.
- `tests/ops/qualification/` (2): `test_contract`, `test_trust_domain`.

## Pre-mortem (README rule)

- **Loop cost:** one Windows build loop and its records. No Linux run.
- **Decisions the executor will hit:** DH2–DH5 and DH7, acknowledged in one batch after Phase 0.
- **What makes it moot:** an operator ruling that withdraws the R1 C′ gate or reverses D11, or a step-2 `/v8` parser that already binds all eleven entries (G-C3 then narrows to finding (f)).
- **Measurements the return fills in:** findings (a)–(g), the per-case records and the closure table at the head. No numbers are asserted here.
