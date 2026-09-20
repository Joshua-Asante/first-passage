# Qualification issues #423 and #424 — implementation handoff

> **For agentic workers:** Execute with superpowers:executing-plans and applicable implementation workflows. Select only the bounded outcome assigned below; return at its boundary. The coordinator owns acceptance and selection of the next outcome.

**Goal:** Close the two deferred PR #420 defects: configuration-bound, non-disclosing boundary preflight and recoverable cleanup that validates retained tree UID/GID/mode bindings.

**Architecture:** Retained host configuration remains the authority for executable selection. One canonical tree-binding definition supplies provisioning and ownership manifests; cleanup validates retained resolved bindings before recursive deletion. Preserve existing ownership locks, reservation authority, retirement receipts and interruption recovery.

**Tech Stack:** Python, pytest, the repository operations launcher, Linux filesystem ownership and Docker on disposable qualification hosts.

**Spec:** [Issue #423](https://github.com/Joshua-Asante/first-passage/issues/423), [issue #424](https://github.com/Joshua-Asante/first-passage/issues/424), and `tools/qualification_verification/README.md` in the implementation checkout.

## Source basis and execution setup

Drafted from remote main `f2606b043fa5b663d5edb9505fb14b2d6885d83a` on 2026-09-19. Both issues remain open. PR #420 merged; these are deferred issues, not pending PRs. The shared local checkout is older and contains unrelated edits; do not implement against it or copy its working tree into the implementation checkout.

At execution, inspect current remote main and the applicable AGENTS.md. Use a fresh isolated checkout through the worktree workflow, based on current main after checking intervening changes. Record the actual base SHA and working-tree state. The source observations below must be rechecked if main has advanced.

The current boundary fixture in `tests/integration/qualification_boundary/conftest.py` loads the ownership manifest, builds/installs the worker, calls `inspect_environment(instance_path, profile_bytes)`, saves `environment.json`, then calls `require_environment(report)`. It already has `self.manifest['host_config']`, but does not pass it to preflight. Preflight hardcodes `/usr/bin/docker` and returns image `id` plus `RepoDigests` as `digests`.

In `tools/qualification_verification/host.py`, provisioning records tree resources with only `kind`, `path`, and `uid`. `validate_owned_tree` checks UID, with root:root/0700/empty validation only for the allowed interrupted-creation exception. A matching UID bypasses general GID/mode checks. Cleanup validates resources before its recorded-tree deletion loop and retains a durable identity reservation until successful retirement. Trace campaign cleanup too before making claims about side-effect ordering.

The issue's historical description of a blocked `--test-only` path is stale: current main runs incremental boundary tests and also supports `--s2`. Preserve both callers and their existing acceptance scopes. Fixing these issues does not establish full qualification acceptance or general shared-host support.

## Roadmap and combined acceptance

1. Handoff A: close #423 across the retained manifest, actual fixture caller, Docker invocation and serialized evidence.
2. Handoff B: close #424 across canonical configuration, provisioning, retained ownership, cleanup and interrupted/retried operation.

These outcomes are independently reviewable. **The initial executor assignment is A only.** After reviewing A, the coordinator can assign B under this same document. An inline coordinator must record A's disposition before advancing. Access to this roadmap is not an instruction for a delegated executor to take both assignments.

Combined acceptance belongs to the originating coordinator: both issue requirements covered, relevant existing recovery behavior preserved, final compatible source state verified, documentation accurate, and Linux-dependent claims supported by real disposable-host evidence. No campaign, deployment, production-account action, statistical-policy change, merge or issue closure is assigned by this draft. Return local reviewable changes; integration actions require their own assignment.

## Global constraints

- Use configuration as code: define reusable tree bindings once, resolve roles explicitly, retain their identity, and validate at consumption. Do not repeat canonical values across provisioning, cleanup and tests.
- Preserve `trusted_administrator_and_privileged_qexec/v1`; do not claim protection against malicious privileged qexec or broaden host support.
- Preserve exact resource ownership, no-follow/link and mount rejection, active-principal checks, locks, durable reservations, and idempotent retirement. No broad Docker pruning or shared-resource deletion.
- Before project Python work run `./fp.ps1 doctor`. Run Python through the checkout's launcher. Without PowerShell 7.3+, use `python -I scripts/fp.py <command>`; this is the documented bootstrap, not a bypass. Diagnose environment failure rather than falling back to system Python.
- Use behavior-first regression tests and related-case review for affected callers and lifecycle states. Do not perform unrelated hardening or refactoring.
- A Windows metadata double does not establish real Linux permission behavior. Record unavailable Linux verification as outstanding, not passed.

## Handoff A — configured preflight and private image evidence (#423)

**Selected outcome:** A real boundary fixture uses the protected Docker executable from its retained host configuration, including a nondefault path; saved image observations contain only the opaque worker content ID and no repository digests/names.

**Prerequisites:** The source basis and actual caller above are confirmed; current main is available in isolation; launcher doctor passes before Python work. Disposable Linux execution is needed for final OS-level evidence, but deterministic implementation can proceed independently of host availability.

**Ownership:** The assigned executor owns A's implementation and evidence. The originating coordinator reviews A, assigns B and owns combined acceptance.

**Verification:** Run the focused command below and the relevant real Linux boundary checks. Prove manifest-to-caller-to-command propagation and inspect serialized `environment.json`, including a private digest fixture. Return exact commands, interpreter, starting/final source identity, results, skips and evidence paths.

**Checkpoint:** Report to the coordinator after tracing callers and observing the regression failures, and at completion. Record progress/evidence in this section. Return consequential trust/configuration conflicts before dependent edits; routine implementation choices do not require approval.

**Return boundary:** Return after A's local implementation, verification and evidence packet, or a concrete scope/dependency conflict. Do not start B, broaden public-evidence redaction into unrelated exports, run full qualification campaigns, push, open a PR, merge or close issues under this assignment.

### Contract and file scope

- Modify `scripts/qualification_boundary_environment.py` and `tests/integration/qualification_boundary/conftest.py`; update every discovered `inspect_environment` caller and affected tests.
- Extend the preflight API with a required keyword-only `host_config` mapping. The real producer is the protected ownership manifest's retained `host_config`; do not reload current default host.json or use PATH fallback.
- Validate configured executable protection using the existing authoritative validation behavior. `host.py` already imports the environment module: avoid introducing a circular import. If extraction is needed, keep one small shared validator and preserve all existing symlink/ancestor tests.
- Docker version/image queries use the validated configured executable and the existing fixed local socket binding. Invalid/missing/unprotected configuration must fail readiness before executing that client.
- Preserve the report envelope and image identity-match check; export the image observation as `{'id': observed[0]['Id']}`. Never copy the raw inspect object into evidence or a diagnostic error. Keep the configured image-ID comparison authoritative.
- Test in `tests/test_qualification_boundary_environment.py`, `tests/test_qualification_boundary_verification.py`, and an appropriate actual-fixture regression. Update `tools/qualification_verification/README.md` with the new input contract.

### Execution steps and acceptance cases

- [x] Search all `inspect_environment` uses and evidence consumers in the actual checkout. Record the caller inventory and any schema dependency before changing the interface.
- [x] Add failing regressions: a protected nondefault client receives both Docker queries; the real fixture passes its retained config; missing/invalid/unprotected clients reject without invocation; mismatched image ID still rejects.
- [x] Add a private-image regression using a sentinel such as `private.example/team/worker@sha256:...`, serialize the resulting report through the evidence-writing path, and assert that neither `RepoDigests`, `digests`, nor the private registry/repository sentinel occurs. Assert that the expected opaque ID remains.
- [x] Run these tests and retain their expected failing results, then implement the API/caller/allowlist change and rerun.
- [x] Check both normal boundary and S2 fixture construction, unsupported-platform reporting, and existing protected-executable symlink rejection. Run the focused suite and `git diff --check`.
- [x] Return the source diff, final interface, verification evidence and remaining Linux dependency to the coordinator. Document the fix without claiming qualification acceptance.

```powershell
./fp.ps1 python -m pytest tests/test_qualification_boundary_environment.py tests/test_qualification_boundary_verification.py tests/test_qualification_host.py -q --tb=short
git diff --check
```

Include any newly added fixture regression module in the command. Real Linux verification must use the repository's disposable-host procedure and installed checkout launcher; do not substitute the developer's Docker host. Record exact host/config/source identities and evidence paths.

**Progress:** Draft only; no implementation or tests executed.

### Handoff A executor return — 2026-09-19 UTC: delivered for coordinator review, not accepted by the executor

Checkout `C:/Users/joshu/multi_firm_operations/.claude/worktrees/review-leftover-worktrees-d12e00`, branch
`claude/qualification-issues-423-424-88fd15` reset to `origin/main` = `f2606b043fa5b663d5edb9505fb14b2d6885d83a`
(the draft's basis; main had not advanced). The branch's prior local-only commit `c2e6eb2` (a launcher
precursor superseded on main) was discarded; the branch has no upstream. One working-tree repair before
any test: `requirements-ops.lock` had been checked out CRLF under `core.autocrlf=true` despite `eol=lf`,
which failed `test_host_config_matches_committed_lock_bytes` (record `20260919T220907Z-ee7a7cf5d70d`);
re-checkout restored the committed bytes (`9aa7c17c…`), no source change. Doctor: interpreter
`C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, Python 3.13.2, 62 locked packages,
cryptography 50.0.1.

**Caller inventory (verified at f2606b0).** `inspect_environment`/`require_environment` have one production
caller: `tests/integration/qualification_boundary/conftest.py::Boundary.__init__`, reached only through the
session-scoped `real_boundary` fixture, which both `--test-only` and `--s2` in
`scripts/qualification_boundary_verification.py` drive via `FP_QUALIFICATION_HOST_MANIFEST` (S2 adds
`FP_QUALIFICATION_S2=1`; same constructor, same manifest). `self.manifest['host_config']` is the parsed
`host.json` retained by `host.provision_reserved`. The report is written once to
`<root>/evidence/boundary/environment.json` via `host.save(..., exclusive=True)`; nothing reads it back
(RunRecord's artifact inventory is non-recursive over `evidence/<uuid>/`), but both qualification workflows
copy `$host_root/evidence/.` wholesale into an uploaded 14-day artifact, so the digest disclosure was real.
`ops/c1_rail/qualification/execution/image.py:59` reads `RepoDigests` in-process for base-image approval
only; not serialized, out of scope. `scripts/check_boundaries.py` (required `skills (3.12)` status)
classifies both `scripts/` and `tools/qualification_verification/` as governance; no new static `ops` import
was added.

**Interface and behavior.** `inspect_environment(instance_path, profile_bytes, *, host_config)` — the
keyword is required (positional or absent → `TypeError`). New readiness check `docker_client` (added to
`REQUIRED`): `configured_docker(host_config)` applies `validate_executable_path(host_config, 'docker')`
(the same per-name predicate `validate_executable_paths` applied at HEAD, plus a `Mapping` guard so a
non-mapping config is a caught `ValueError` rather than an escaping `AttributeError`) and then
`protected_executable`; the `docker version`/`image inspect` commands are composed from the validated path
and the instance's socket only inside `if executable:`, so on failure the `docker`/`image` checks are absent
(reported missing by `require_environment`) and no client runs. `observed` for `docker_client` is the
configured path string (public `host.json` content, pinned by `host_config_sha256`). The `image` observation
is `{'id': observed[0]['Id']}` after the unchanged identity-mismatch check; `RepoDigests`/`RepoTags` never
enter the report. Report envelope and `qualification_environment/v1` unchanged (routine choice: the envelope
keys are identical and `require_environment` is the only consumer; the coordinator may prefer a version bump).
Shared validator: `validate_executable_path`, `validate_executable_paths`, `protected_executable` and the
`EXECUTABLES` tuple now live in `scripts/qualification_boundary_environment.py` next to `protected`;
`host.py` re-imports them by name and keeps `validate_host_executables` (so the existing
`host.protected_executable` / `host.validate_host_executables` monkeypatches still bind); `host.py`'s unused
`deque` import removed. The three unit tests that drove `protected_executable` through `host.protected`
now patch `environment_module().protected` (the function resolves globals in its defining module; without
this retarget the reject variants would false-green on Windows because the real `protected` rejects any
tmp dir). `protected_executable` body is byte-identical to HEAD.

**Files.** Modified: `scripts/qualification_boundary_environment.py`,
`tests/integration/qualification_boundary/conftest.py` (passes `host_config=self.manifest['host_config']`),
`tests/test_qualification_boundary_environment.py`, `tests/test_qualification_host.py`,
`tools/qualification_verification/host.py`, `tools/qualification_verification/README.md` (lines 46–52 and
137–157: shared executable rule; new input contract; `docker_client`; opaque image ID; wholesale CI export).
New: `tests/test_qualification_boundary_fixture.py` (fixture-construction regressions: both boundary and S2
paths pass the retained manifest object itself as `host_config`, event order group→build→install→inspect→
save(exclusive)→require→restart; a `docker_client`-only failure retains `environment.json` and never starts
the service). `tests/test_qualification_boundary_verification.py` needed no change (it never reaches the
fixture); it was run in every focused pass.

**Red → green.**
- Red: `./fp.ps1 python -m pytest tests/test_qualification_boundary_environment.py tests/test_qualification_boundary_fixture.py -q --tb=line`
  → **24 failed, 20 passed**; record `.cache/fp-verification/20260919T222551Z-4ead4eae5e4a/record.json`
  (status failed, exit 1, source_stable true, capture complete; failures were the missing
  `protected_executable` attribute, `TypeError` on the keyword contract, and the fixture kwarg omission).
- Green (final source):

```powershell
./fp.ps1 python -m pytest tests/test_qualification_boundary_environment.py tests/test_qualification_boundary_verification.py tests/test_qualification_host.py tests/test_qualification_boundary_fixture.py -q --tb=short
git diff --check
```

  → **180 passed, 2 skipped** (the two pre-existing Windows skips: symlink creation, POSIX exec), 7.01 s;
  record `.cache/fp-verification/20260919T230501Z-5e6dffe7d33d/record.json` — status completed, exit 0,
  verification_exit_code 0, source_stable true, capture_complete true, no capture/report errors;
  before/after commit `f2606b04…`, tracked `diff_sha256`
  `f1335324f247d8e115a923a8ccb893513de30587bc031fcd8745efd13040d055`. `git diff --check` clean.
  Baseline on unchanged source for comparison: 163 passed, 2 skipped (record `20260919T221753Z-7b90bbfa6b79`).
- Related consumers on the final source: `tests/test_qualification_boundary_cleanup.py
  tests/test_qualification_campaign_host.py tests/test_qualification_container_ownership.py
  tests/test_qualification_worker_image.py tests/integration/qualification_boundary
  tests/integration/qualification_host` → 33 passed, 67 skipped (all skips are the Linux
  administrator-host gates); the new fixture module also passes when collected after the integration
  conftest. `scripts/check_boundaries.py` → OK (812 modules, no illegal edges). Whole-repo
  `pylint --fail-under=8.0` over `git ls-files '*.py'` plus the new test module: 8.04/10 on the exact final
  tree (floor 8.0; the `R0401` cyclic-import line pylint attaches to the last file is a pre-existing
  `test_tradeify_phase1_identity_policy -> test_tv_trade_ledger` cycle, unrelated).
- Independent adversarial review (5 lenses, 2 skeptics per finding): no blocker/major/minor findings;
  mutation checks confirmed the tests catch a restored `/usr/bin/docker` literal, restored `RepoDigests`,
  and validation moved after the queries. Two nits (assertion strength) were folded before the final run.

**Outstanding — real Linux evidence.** Not produced here: no disposable host was available to this session,
and substituting a developer Docker host is forbidden. Required: the documented installed-launcher run
(`qualification_boundary_verification.py --test-only` and `--s2`) on fresh disposable hosts, with the
uploaded `evidence/boundary/environment.json` inspected for `checks.docker_client.observed ==
host_config['docker']`, `checks.image.observed == {"id": <worker id>}` and no `RepoDigests`/`digests`
key; and one host whose `host.json` selects a nondefault protected client (the unit test covers this on a
double only). `tests/integration/qualification_host/test_host.py`'s symlink/ancestor cases run
unchanged there through `host.protected_executable`.

**Observations outside A's scope, for the coordinator.** (1) `build_worker` (conftest.py:58) and
`cleanup → campaign_host.cleanup` (host.py:699–701) invoke `host_config['docker']` before
`validate_host_executables` runs — the same invoke-before-validate class, untouched. (2) README:266 says CI
"exports an allowlist of evidence/receipts"; both workflows actually `cp -a` the whole `evidence/` tree
(the step label says only "no keys or private manifest"). (3) `probe_access` still runs the literal
`/usr/bin/python3` for the access-probe child (deliberately the system interpreter; #423 names Docker only).
(4) `environment.json` is durable only as a 14-day artifact; it is not hash-pinned in any `record.json`.

Return boundary respected: no commit, push, PR, merge or issue closure; B not started. This entry was
written after the recorder closed; runtime/test bytes match the final record.

## Handoff B — retained tree permissions and recoverable cleanup (#424)

**Selected outcome:** Cleanup rejects an existing tree whose retained UID, GID or permission mode has drifted, preserving the tree and reservation; supported provisioning interruptions and cleanup retries remain recoverable.

**Prerequisites:** Coordinator assigns B explicitly after A's disposition. Inspect current host provisioning, cleanup, schema consumers and tests; doctor passes. Inventory supported existing ownership-manifest versions before selecting compatibility behavior. No live legacy manifests were inspected while drafting this handoff.

**Ownership:** The assigned executor owns B. The originating coordinator accepts its lifecycle behavior and the combined result; executor completion does not authorize shared-host operation.

**Verification:** Exercise provisioning-to-manifest-to-cleanup using actual retained bindings; independently vary UID, GID and mode and verify retention. Exercise interrupted setup, partial cleanup and repeated retirement. Run the commands below plus real Linux ownership/mode cases, with exact revision/interpreter/evidence identification.

**Checkpoint:** Report the canonical binding shape and legacy-manifest disposition to the coordinator before changing persistence; this is a technical review checkpoint, not automatically a user approval request. Report any supported intermediate state that cannot be recovered, and return the completed evidence packet for acceptance.

**Return boundary:** Return after B's verified local changes or a concrete compatibility/scope conflict. Do not activate shared/reused-host support, migrate live resources, weaken ownership checks to make tests pass, advance qualification campaigns, push, open a PR, merge or close issues.

### Contract and file scope

- Primary implementation: `tools/qualification_verification/host.py`; canonical binding configuration belongs in its existing configuration layer or a small dedicated shared module, chosen after inspecting current conventions. Update `host.json` only if it is the appropriate canonical owner.
- Tests: `tests/test_qualification_host.py`, `tests/integration/qualification_host/test_host.py`, and relevant `tests/test_qualification_boundary_cleanup.py` cases. Inspect `campaign_host.py` and other ownership-schema readers for compatibility; change only necessary consumers.
- Define each top-level owned tree's desired UID role, GID role and mode once. Resolve them from retained role/configuration inputs during provisioning. Persist the resolved binding and a stable schema/configuration identity before creating resources; provisioning and cleanup must refer to the same resolved configuration.
- Exact resolved-binding validation must reject malformed, missing, extra or inconsistent authority fields. Do not trust a manually weakened manifest binding merely because it matches the current filesystem.
- Validate all applicable owned-tree bindings before recursive tree deletion. GID-only drift must reject even if mode remains private; mode-only drift must reject even if UID/GID match. Preserve original tree contents and the identity reservation on rejection; emit a failure receipt and no successful retirement certificate.
- Preserve missing-resource idempotence. Preserve the narrowly scoped empty root:root/0700 data/scratch intermediate before chown only in supported incomplete setup states, and the exact root-owned `env/lib64 -> lib` exception only in incomplete setup. Do not generalize either exception to completed hosts.
- Trace mkdir, chown, mode application and durable recording order, including restrictive umasks. If the new invariant introduces an intermediate state, make that state both narrowly attributable and recoverable; do not solve it by accepting arbitrary permission drift.
- Choose an explicit legacy-manifest policy grounded in historical producer code. Do not silently synthesize missing GID/mode from today's defaults, and do not strand supported old reservations by blanket schema rejection. If safe recovery needs a separately authorized migration or operator decision, return that concrete conflict before declaring B complete.
- Keep validation/deletion serialized under the existing locks and trust assumptions. This is top-level ownership-binding validation, not a new recursive policy for every descendant or a defense against a hostile administrator.
- Update the README's explicit matching-UID limitation and recovery descriptions to match verified behavior; retain the disposable-host support scope.

### Execution steps and acceptance matrix

- [x] Trace all tree producers, schema readers, cleanup entry points and supported lifecycle states. Define canonical bindings and compatibility handling in the return record before editing persistence.
- [x] Add failing completed-host regressions for data and scratch: correct UID with wrong GID; correct UID/GID with group-accessible mode; incorrect UID; all bindings correct. Include another canonical root-owned tree so validation is not special-cased only to qexec trees.
- [x] For each drift rejection, verify contents remain, reservation owner remains, failure is recorded and successful retirement is absent. Restore the canonical metadata and retry: cleanup must succeed once and subsequent cleanup must remain idempotent.
- [x] Add interruption cases: manifest recorded before mkdir; mkdir before chown; completed chown/mode transition; restrictive-umask creation; incomplete venv alias; partial resource deletion; completed retirement with a replacement run's reservation. Test invalid lookalikes for the initial-owner and alias exceptions.
- [x] Add schema/configuration tests proving provisioning retains the same resolved binding cleanup validates, malformed/tampered bindings reject, and the chosen legacy policy supports safe recovery without fabricating authority.
- [x] Observe the intended failures, implement the minimal canonical binding/persistence/validation changes, then run the focused suites and existing recovery regressions.
- [ ] Run real Linux cases on a disposable host with real chown/chmod and interruption/retry behavior. Windows doubles are supplemental. Preserve failed-state resources for diagnosis and recover them only through the supported owned cleanup procedure.
- [x] Update documentation, run the final gate and return source/evidence to the coordinator. Distinguish local passing results from outstanding Linux or legacy compatibility evidence.

```powershell
./fp.ps1 python -m pytest tests/test_qualification_host.py tests/test_qualification_boundary_cleanup.py tests/test_qualification_container_ownership.py tests/test_qualification_campaign_host.py -q --tb=short
./fp.ps1 check
git diff --check
```

The coordinator performs one final combined focused run covering A and B on the same final source state, extending coverage only for changed consumers or unresolved failures. Report pre-existing gate failures and skips explicitly. Tests requiring Linux must run using the documented installed host procedure, not be counted as passing from a skipped local collection.

**Progress:** Draft only; unassigned until A is reviewed.

### Handoff B assignment and design checkpoint — 2026-09-19 UTC

Assigned by the coordinator after A's delivery ("preserve A's tested changes; report the canonical
tree-binding design and legacy-manifest recovery policy before changing persistence; return B for
coordinator review; no push, PR, merge or issue closure"). A was preserved first: local commit
`9680ed2` on `claude/qualification-issues-423-424-88fd15` (unpushed) plus a copy of A's patch, new files
and all verification records at `C:/Users/joshu/multi_firm_operations/tmp/handoff-423-424/a-delivered-2026-09-19/`
(`SHA256SUMS.txt` there matches the delivered identities). #423 stays open pending real Linux evidence.

**Lifecycle trace (verified at 9680ed2).** Single producer: `host.provision_reserved` records
`{'kind':'tree','path','uid'}` via `own()` (durable `save`) → `mkdir(mode)` → `os.chown(uid, uid)`, with no
chmod and no umask pin anywhere (sudo's default 022 on the hosted runners is unpinned). Under umask 027/077
the root-owned trees are created 0750/0700 while data/scratch are umask-invariant 0700. Manifest states are
exactly `provisioning`, `host_ready_boundary_unconfigured`, `setup_failed` (hand-built fixture manifests
carry none). No later operation touches the five top-level directories' own metadata (fixture_install,
campaign_host, image/service/launcher/store only create descendants; the worker's sole bind mount is a
read-only descendant). Single shape-strict reader: `validate_resources` (`set(item) != {...}`) plus the
cleanup loop; `campaign_host`, `boundary_cleanup_plan`, `public_observations` and the invariant/record
tooling never read tree items. Retirement identity is bound to the bytes of `ownership.json`
(`retired.json`/receipt `manifest_sha256`), so cleanup may never rewrite the manifest. The host-wide identity
reservation is released only inside cleanup and `provision()` refuses while it is held, so a cleanup that
rejects a legacy manifest would strand the host, not just the run. `validate_resources` cross-checks
`manifest['roles']` against `host_config` only in the user/group branch, and `ROLES` has no name for uid 0.
No CI workflow runs the real-Linux recovery tests: `--test-only`/`--s2` select only two
`tests/integration/qualification_host` node IDs from the invariant manifest; the whole directory runs only
under the documented manual `--host-only` procedure.

**Canonical binding shape.** In `tools/qualification_verification/role_policy.py` (the existing shared
configuration layer for setup, probes and cleanup):

- `TREE_BINDINGS_SCHEMA = 'qualification_tree_bindings/v1'`; `ADMINISTRATOR = 'administrator'` (uid/gid 0,
  never a provisioned role, never an identity resource).
- `TREE_BINDINGS`: `code (administrator, administrator, 0o755)`, `env (…, 0o755)`,
  `data (qexec, qexec, 0o700)`, `keys (…, 0o755)`, `scratch (qexec, qexec, 0o700)` — creation order preserved.
- `resolve_tree_binding(name, roles) -> {'uid': int, 'gid': int, 'mode': '0755'}`; `mode` is the 12-bit
  `S_IMODE` as a four-digit octal string (setgid/sticky drift is drift; consistent with the existing exact
  `S_IMODE == 0o700` checks in host.py and service.py).
- `tree_bindings_identity() -> {'schema': …, 'sha256': digest of the table}` so an unbumped table edit
  becomes a named cleanup failure instead of unexplained "drift".

**Persistence.** The manifest gains `tree_bindings` (the identity above) at creation, before any resource.
Each tree record becomes `{'kind':'tree','path','uid','gid','mode'}`, written by `own()` before creation.
Creation order per tree: record → `os.mkdir(target, 0o700)` → `chmod(mode)` → `chown(uid, gid)`. The only
non-final intermediate is therefore root:root/0700/empty for every tree; provisioning refuses an
owner-masking umask or a setgid parent before creating anything so that intermediate is deterministic.

**Validation (read-side only).** `validate_resources`: `manifest['roles'] == resolve_roles(host_config)`
for every manifest; exact key sets; `tree_bindings == tree_bindings_identity()`; each retained binding
equal to `resolve_tree_binding(path, roles)` (a manually edited binding is "inconsistent" even when the
filesystem matches it). `validate_owned_tree(path, binding, *, allow_initial_creation, allow_initial_venv_alias)`
compares uid, gid and mode with per-field failure text (`tree owner|group|mode mismatch`); the
root:root/0700/empty exception now covers all five trees, still only in `provisioning`/`setup_failed`; the
`env/lib64 -> lib` alias exception is unchanged. All validation precedes deletion; rejection keeps the
existing path (failure receipt, no `retired.json`, reservation retained, trees untouched).

**Legacy-manifest policy.** Legacy = a v3 manifest without `tree_bindings` whose tree items are exactly
`{'kind','path','uid'}` (the only shape main ever produced, 2026-09-17 → this change; no live host with one
is known — CI hosts are destroyed). Grounded in that producer's code (`host.py` 1339604..9680ed2): it owned
each path by a fixed role (`LEGACY_TREE_OWNERS` in `role_policy.py`) and ran `chown(uid, uid)`, so cleanup
requires the record's `uid` to be that owner and the tree's owner **and group** to equal it; its
`mkdir(mode)` was umask-dependent, so the mode is not retained, never synthesized and not checked. The two
incomplete-state exceptions apply unchanged; mixed shapes reject; retirements are labelled
`legacy_tree_bindings: [paths]` in the receipt. (Revised during the adversarial review from a UID-only
legacy check: the group rule is producer-determined, not a default.) Blanket rejection was not chosen
because it would strand the whole host's identity reservation; a `--accept-legacy-tree-bindings` cleanup
flag remains available to the coordinator as an override. Residual: an administrator who downgrades a
bindings-era manifest to the legacy shape loses mode validation only, and the receipt records it.

### Handoff B executor return — 2026-09-20 UTC: delivered for coordinator review, not accepted by the executor

Same checkout and branch; base `9680ed2` (A's local commit on `f2606b0`); B is uncommitted on top. Doctor
unchanged (`tmp/ops-env/Scripts/python.exe`, Python 3.13.2, 62 locked packages, cryptography 50.0.1).

**Files.** `tools/qualification_verification/role_policy.py` (`TREE_BINDINGS_SCHEMA`, `ADMINISTRATOR`,
`TREE_BINDINGS`, `TREES`, `LEGACY_TREE_OWNERS`, `principal`, `resolve_tree_binding`,
`resolve_legacy_tree_owner`, `tree_bindings_identity`); `tools/qualification_verification/host.py`
(`INITIAL_TREE`, `INCOMPLETE_STATES`, `require_deterministic_tree_creation`, `observed_binding`,
`tree_binding`, `validate_owned_tree(path, binding, *, allow_initial_creation, allow_initial_venv_alias)`,
`validate_legacy_owned_tree`, `validate_resources` → legacy paths, provisioning order
record→`mkdir(0o700)`→`chmod`→`chown` with the precondition before `root.mkdir`, `tree_bindings` in the
manifest, cleanup loop and receipt `legacy_tree_bindings`, resource validation moved inside the receipt
try so a malformed/inconsistent record is a recorded refusal); `tools/qualification_verification/README.md`
(three passages: binding/creation/validation contract, cleanup refusal list, the former UID-only
limitation replaced by the top-level-binding scope statement); `tests/test_qualification_host.py`
(helpers `tree_record`, `canonical_metadata`, `model_tree_metadata`, `minimal_manifest`,
`failure_receipts`, `first_mismatch`; migrated literals; new cases below);
`tests/integration/qualification_host/test_host.py` (fixture manifest carries `tree_bindings`; records
migrated and directories bound explicitly; new real-Linux cases below). `campaign_host.py` and every other
manifest reader needed no change (verified by trace: none reads tree items).

**Schema/interface changes.** Ownership manifest v3 gains `tree_bindings: {schema, sha256}`; tree records
gain `gid` and `mode` (`"0755"`-style 12-bit octal string). Cleanup receipt `qualification_host_cleanup/v1`
gains optional `legacy_tree_bindings`. `validate_resources` returns the legacy tree paths.
`validate_owned_tree` takes a binding mapping instead of a UID (its one direct caller, the integration
test, updated). Failure texts: `tree owner|group|mode mismatch`, `inconsistent tree binding`,
`inconsistent tree resource`, `invalid tree resource`, `tree binding configuration mismatch`,
`roles do not match the retained host configuration`, `umask must not mask owner permissions`,
`setgid parent directory`.

**Acceptance matrix (unit, Windows doubles via `Path.stat`).** Completed host, data/scratch/code: correct
→ retired; wrong UID / wrong GID with private mode / group-accessible mode with matching UID+GID /
setgid → `tree <field> mismatch`, contents and reservation retained, failure receipt, no `retired.json`;
restore → retired once, then `already_retired`. Weakened record matching the filesystem → recorded
refusal `inconsistent tree binding`. Twelve malformed/tampered shapes each rejected with their named
message (including `False`/`0.0` on a root-owned tree, identity digest/schema edits, mixed shapes, roles
drift). Interruption: recorded-before-mkdir (absent) and partial deletion → idempotent; root:root/0700
empty for all five trees in `provisioning`/`setup_failed` → retired, and rejected when non-empty, 0750,
foreign owner/group, or in the ready state; venv alias cases unchanged; completed retirement with a
replacement reservation untouched. Provisioning double proves record precedes `os.mkdir(…, 0o700)`, then
`chmod(mode)`, then `chown(uid, gid)`, the retained record equals the canonical resolution, and cleanup
retires that host. Preconditions: umask 000/022/027/077 accepted; 0177/0277/0477 and a setgid parent
refused before anything is created. Legacy: producer owner + group validated, mode not, receipt labelled.

**Red → green.** Red (unchanged host.py): **105 failed / 94 passed / 2 skipped**, record
`.cache/fp-verification/20260920T000403Z-4e2817a7da86` (missing binding API, missing `tree_bindings`,
new precondition messages). Green on the final source:

```powershell
./fp.ps1 python -m pytest tests/test_qualification_host.py tests/test_qualification_boundary_cleanup.py tests/test_qualification_container_ownership.py tests/test_qualification_campaign_host.py -q --tb=short
./fp.ps1 check
git diff --check
```

→ **235 passed, 2 skipped** (the two pre-existing Windows skips), record
`.cache/fp-verification/20260920T033845Z-832d22be43a5/record.json` (completed, exit 0,
verification_exit_code 0, source_stable, capture complete, no errors; commit `9680ed2`, tracked
`diff_sha256 321147dec63cfc020604032d528ccfefa1ffba1753e998f91159086733adc8e2`). `./fp.ps1 check` →
record `20260920T033925Z-292628fa9fa3` completed, exit 0, same diff (its only WARNs are the pre-existing
absent vendor-data trees of a bare worktree). `git diff --check` clean. A's suites plus both
`tests/integration` collections on the same tree: 59 passed, 89 skipped (all Linux administrator-host
gates), record `20260920T033905Z-ebec173a62fe`. `scripts/check_boundaries.py` OK. Whole-repo pylint
8.04/10. B baseline on `9680ed2` before edits: 154 passed, 2 skipped.

**Adversarial review** (5 lenses, 2 skeptics per finding, 37 agents, 38 single-point mutants of the
validator/producer all caught by the new tests except test-only gaps): no blocker/major code findings.
Folded: legacy validation tightened from UID-only to the producer-determined owner **and** group
(`LEGACY_TREE_OWNERS`, `chown(uid, uid)`), with mode still unchecked; per-case rejection messages in the
tamper test; the legacy type guard exercised on a uid-0 tree; the identity digest tested as
table-derived; umask boundaries (077 accepted, 0177/0277/0477 refused); manifest-level refusals now
produce a failure receipt; a wrong docstring rationale removed. Refuted/out of scope and left as noted:
a consistent `roles`+`host_config` co-edit re-resolves bindings (root-level tamper under the trust model,
still masked on real hosts by the account records); a future `TREE_BINDINGS` edit must bump the schema
and retain the old table or retained manifests become unretirable (documented in `role_policy.py`);
umask 077 still makes the run root non-traversable for roles (pre-existing, outside the binding).

**Outstanding — real Linux evidence.** Not produced here (no disposable host in this session). The
real-Linux cases live in `tests/integration/qualification_host/test_host.py` and run only under the
documented manual procedure (`qualification_boundary_verification.py --host-only --manifest …` on a fresh
disposable host); no CI workflow selects them. Required there: `test_installed_tree_binding_drift_is_named_and_restorable`
(installed data tree exactly `qexec:qexec 0700`; owner/group/mode/setgid drift named and restored),
`test_cleanup_after_kill_between_tree_mkdir_and_binding` (all five trees, umask 022 and 077, intermediate
`0:0:0700`), `test_cleanup_retains_drifted_tree_and_reservation_until_the_binding_is_restored` (real
chown/chmod, receipt, repair, idempotence), `test_legacy_uid_only_records_retire_on_the_producer_owner_and_group`,
`test_tree_creation_preconditions_use_real_umask_and_parent_mode`, the migrated venv-alias and
retirement/replacement cases, and a full `provision.sh` → boundary → `cleanup.py` cycle on the new record
shape (both `--test-only` and `--s2` workflows exercise that path on PR). Record the host's umask and
`config['parent']` mode in that packet.

Return boundary respected: no commit of B, no push, PR, merge or issue closure; the additional
observations from A remain separate (B's trace found no dependency on them). This entry was written after
the recorder closed; the tools/tests/README bytes match the records above.

## Return packet and coordinator disposition

For each handoff return: checkout path, base and final commit or checksummed working-tree identity, changed-file inventory, behavioral/interface/schema changes, regression evidence, exact commands/interpreter, result counts and skips, verification record paths, remaining dependencies and compatibility limitations. Preserve new source and evidence outside any disposable checkout before it is removed.

The coordinator records A and B as delivered, accepted or blocked separately, checks the complete issue requirements against the final source, and owns any later PR/merge/issue-closure assignment. Closure requires the implementation and verification evidence, not merely this plan or a green unrelated campaign run.

### Handoff C executor return — 2026-09-20 UTC: outcome 2 produced on fresh hosts; outcomes 1 and 3 blocked by a workflow-dispatch platform constraint; one S2 dispatch failure preserved

Coordinator GO received 2026-09-20 for (a) pushing the branch, (b) dispatching the workflows, plus draft PR
and best-judgment execution. Note: the `superpowers:executing-plans` skill was not available in this
session; the plan steps were executed directly.

**Checkout and identity.** Worktree `C:/Users/joshu/multi_firm_operations/.claude/worktrees/review-leftover-worktrees-d12e00`,
branch `claude/qualification-issues-423-424-88fd15`, base chain `f2606b0` → `9680ed2` (A) → `2ff3b5e` (B) →
**`6cd9ca6`** (Handoff C: `.github/workflows/qualification-host-evidence.yml` only, 143 lines; commit
`6cd9ca63940054d0209c1a17fe66262688a7c76e`, workflow blob `dbe9a42417d60f9e2a7c8d522724a785e2addbfb`,
blob sha256 `944995c837e48edae4c92cd0d832322701fd6a0922562f315f42177ca5fce28c`). `git diff --stat
2ff3b5e..6cd9ca6` = that one file; tools/tests/scripts bytes identical to `2ff3b5e`. `origin/main`
rechecked before push: no commits in `f2606b0..origin/main`. C0 recheck: doctor OK (`tmp/ops-env`,
Python 3.13.2, 62 locked packages); B focused suite rerun once → **235 passed / 2 skipped**, record
`.cache/fp-verification/20260920T041955Z-560d94024f8a` (exit 0, source_stable). `scripts/check_boundaries.py`
via launcher OK; pre-commit gate manifest passed on the workflow commit. Branch pushed
`-u origin` (no force); draft PR **#437** opened (authorized). PR-path runs checked out merge commit
`84fa36f1f8ce40d2ae898cebd42c2b8ba51c81e2` (parents `f2606b0` + `6cd9ca6`); **verified locally that its
tree equals `6cd9ca6`'s tree**, so PR-path and dispatch runs executed identical content.

**Runs (all on `ubuntu-24.04`).**

| Run | URL | Checked out | Conclusion |
|---|---|---|---|
| Boundary dispatch | https://github.com/Joshua-Asante/first-passage/actions/runs/35489412733 | `6cd9ca6` | success (hosts 1, 2) |
| Boundary PR path | https://github.com/Joshua-Asante/first-passage/actions/runs/35489451474 | `84fa36f` (tree == head) | success (hosts 1, 2) |
| S2 dispatch | https://github.com/Joshua-Asante/first-passage/actions/runs/35489413703 | `6cd9ca6` | **failure** (defect finding below) |
| S2 PR path | https://github.com/Joshua-Asante/first-passage/actions/runs/35489451486 | `84fa36f` (tree == head) | success |
| Tests / Pylint / Gate manifest (PR) | runs/35489451489, /35489451482, /35489451458 | `84fa36f` | all success |

**Outcome 2 (fresh provision → boundary → cleanup) — produced.** All four boundary hosts (dispatch + PR
path): `record.json` completed, exit 0, `verification_exit_code` 0, `source_stable` true, purpose
`boundary_acceptance`, scope `N1_ONLY_TEST_ONLY`, invariant manifest sha `ee8c5771b652…`, `test_summary`
**464 collected / 464 passed / 0 failed / 0 skipped**, `invariants.json` `passed: true`. JUnit total 464 on
every host; executed inventory: 25 `tests/integration/qualification_boundary` cases plus the required
ops-qualification nodes, including exactly two `tests/integration/qualification_host/test_host.py` nodes —
`test_installed_source_and_runtime_are_protected`, `test_real_distinct_uids_and_denied_permissions` (the
invariant-manifest readiness nodes; the rest of the host suite is `--host-only` and did not run — see
blocker). Full node-ID list preserved at `<artifact>/<uuid>/_nodeids.txt` in the local copy.
`host-observations.json`: `host_config_sha256` == branch `host.json` (`ddc5a391480fd322…`) on all hosts;
`source_commit` as in the table. `boundary/environment.json` on all six qualification hosts (4 boundary +
2 S2): `ready: true`, exactly 16 checks, `checks.docker_client.observed == "/usr/bin/docker"` (ok),
`checks.image.observed == {'id': 'sha256:…'}` only, and no `RepoDigests`/`RepoTags`/`"digests"` substring
anywhere in the file. Cleanup receipts per boundary host: first call `ok: true`, removed 27 (18 containers,
1 image, 3 users, **5 trees all five-field `{uid, gid, mode, path, kind}`** — `code`/`env`/`keys`
`0:0 0755`, `data`/`scratch` `61001:61001 0700`), `failures: []`; second (workflow `cleanup.py`) call
`ok: true`, removed 0 — the idempotent already-retired observable. S2 hosts: same pattern, confirmed
against the in-run cleanup embedded in `record.json` (`ok: true`, removed 9 incl. the five five-field
trees; workflow second call `ok: true`, removed 0). No `legacy_tree_bindings` key on any freshly
provisioned host.

**Defect finding (S2 dispatch run, preserved, not rerun to green).**
`tests/integration/qualification_boundary/test_campaign_supervision_linux.py::test_s2_warm_service_starts_one_guardian_per_work_with_no_scheduler_unit`
failed at line 196: `assert facts['Slice'] == scopes['work_slice']` → observed `''` (empty) vs expected the
work-slice name; `systemctl show <guardian_unit> --property=Slice` returned an empty value on that host.
9 collected / 8 passed / 0 skipped; `require_tests` then rejected the run (`Critical tests missing, failed,
skipped or malformed`), exit 1; `source_stable` true; cleanup receipts still `ok: true`. Attribution:
`git diff --stat f2606b0..6cd9ca6` shows the branch did not touch that test file or any S2 supervision
code (its last change `cf4c6d8` is on main below the base); the same suite passed 9/9 on the PR-path host
with a byte-identical tree. So: pre-existing S2/systemd-domain failure on one fresh host, not introduced
by A or B, second data point green. Evidence preserved under `s2-dispatch-failed-35489413703/` (junit,
record, budget/memory facts, journal, receipts, environment.json). Smallest candidate fix is the
coordinator's to assign; a re-observation (retry `systemctl show` after a settle, or assert on
`ControlGroup` fallback) would be my starting hypothesis, not applied.

**Blocker — outcomes 1 (host-only) and 3 (nondefault client) not produced.**
`qualification-host-evidence.yml` is `workflow_dispatch`-only and has never existed on the default branch.
GitHub registers workflow files from the default branch only: the file has no workflow ID
(`GET /actions/workflows` does not list it), `gh workflow run` and a direct
`POST /actions/workflows/<file>/dispatches` both 404. No dispatch route (UI, CLI, REST, `repository_dispatch`)
can fire it before the file reaches `main`; a `pull_request` trigger would have been the historical
mechanism (the retired `33d3ea1` job ran that way) but is explicitly excluded by this plan. Within this
assignment's constraints (no merge) the executor cannot unblock it. Options for the coordinator:
(1) smallest — merge a tiny PR adding only `.github/workflows/qualification-host-evidence.yml` to `main`,
then dispatch from the evidence branch (the branch's tools/tests/scripts are what runs; the workflow file
on the branch is the one dispatched); (2) authorize a narrowly scoped `pull_request` + paths trigger for a
temporary evidence pass (contradicts the delivered design); (3) accept outcomes 1 and 3 as not produced
and record the gap. For option (1), the expected `host_config_sha256` for the nondefault-client run's
edited `host.json` is precomputed: `d2f1d6bddf08a3813754469af2a29325c09997c00f64b256c1bdeca053d4597c`
(branch value `ddc5a391480fd322…` + the single sed replacement), so the assertion "differs from the
branch's host.json by construction" is checkable on arrival. Host umask and `/var/lib/fp-qualification-tests`
parent mode were **not** recorded (they are captured by the blocked workflow's facts step).

**Commands.** Push: `git push -u origin claude/qualification-issues-423-424-88fd15`. Dispatch:
`gh workflow run qualification-execution-boundary.yml --ref <branch>`, `…qualification-s2-supervision.yml…`,
attempted `gh api -X POST …/workflows/qualification-host-evidence.yml/dispatches -f ref=<branch>` (404, see
blocker). PR: `gh pr create --draft --base main` (#437). Artifacts: `gh run download <id> -D <dir>`.

**Local preservation.** `C:/Users/joshu/multi_firm_operations/tmp/handoff-423-424/c-linux-evidence-2026-09-20/`:
`boundary-dispatch-35489412733/{qualification-boundary-1,2}`, `boundary-pr-35489451474/{…,2}`,
`s2-pr-35489451486/qualification-s2-supervision`, `s2-dispatch-failed-35489413703/qualification-s2-supervision`,
plus `inspect_evidence.py` (the read-only inspection script whose output the numbers above summarize).

**Coverage honesty.** A green badge is evidence only for what JUnit and receipts show executed: the four
boundary hosts prove the new record shape end-to-end on fresh Linux (provision → fixture build → boundary
suite → five-field tree retirement → idempotent second cleanup) and the environment-preflight shape with
the **default** client. They do **not** execute the `--host-only` suite (ownership/permission/interruption
cases), the nondefault protected client, or the umask/parent-mode observation, and they do not change the
standing legacy-v3 limitation (owner+group validated, mode not). No merge, no issue closure, no
required-check change, no `host.json` edit on the branch; trust model
`trusted_administrator_and_privileged_qexec/v1` unchanged; no shared/reused-host claims.

**Outstanding.** #423: nondefault-client evidence (outcome 3) pending the dispatch unblock; the default-client
half of A's preflight evidence is now real-Linux-green on six hosts. #424: boundary-cycle evidence produced;
the full `--host-only` ownership/permission/interruption evidence (outcome 1) pending the same unblock;
final acceptance remains the coordinator's.
