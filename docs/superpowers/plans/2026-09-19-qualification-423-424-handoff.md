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

- [ ] Search all `inspect_environment` uses and evidence consumers in the actual checkout. Record the caller inventory and any schema dependency before changing the interface.
- [ ] Add failing regressions: a protected nondefault client receives both Docker queries; the real fixture passes its retained config; missing/invalid/unprotected clients reject without invocation; mismatched image ID still rejects.
- [ ] Add a private-image regression using a sentinel such as `private.example/team/worker@sha256:...`, serialize the resulting report through the evidence-writing path, and assert that neither `RepoDigests`, `digests`, nor the private registry/repository sentinel occurs. Assert that the expected opaque ID remains.
- [ ] Run these tests and retain their expected failing results, then implement the API/caller/allowlist change and rerun.
- [ ] Check both normal boundary and S2 fixture construction, unsupported-platform reporting, and existing protected-executable symlink rejection. Run the focused suite and `git diff --check`.
- [ ] Return the source diff, final interface, verification evidence and remaining Linux dependency to the coordinator. Document the fix without claiming qualification acceptance.

```powershell
./fp.ps1 python -m pytest tests/test_qualification_boundary_environment.py tests/test_qualification_boundary_verification.py tests/test_qualification_host.py -q --tb=short
git diff --check
```

Include any newly added fixture regression module in the command. Real Linux verification must use the repository's disposable-host procedure and installed checkout launcher; do not substitute the developer's Docker host. Record exact host/config/source identities and evidence paths.

**Progress:** Draft only; no implementation or tests executed.

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

- [ ] Trace all tree producers, schema readers, cleanup entry points and supported lifecycle states. Define canonical bindings and compatibility handling in the return record before editing persistence.
- [ ] Add failing completed-host regressions for data and scratch: correct UID with wrong GID; correct UID/GID with group-accessible mode; incorrect UID; all bindings correct. Include another canonical root-owned tree so validation is not special-cased only to qexec trees.
- [ ] For each drift rejection, verify contents remain, reservation owner remains, failure is recorded and successful retirement is absent. Restore the canonical metadata and retry: cleanup must succeed once and subsequent cleanup must remain idempotent.
- [ ] Add interruption cases: manifest recorded before mkdir; mkdir before chown; completed chown/mode transition; restrictive-umask creation; incomplete venv alias; partial resource deletion; completed retirement with a replacement run's reservation. Test invalid lookalikes for the initial-owner and alias exceptions.
- [ ] Add schema/configuration tests proving provisioning retains the same resolved binding cleanup validates, malformed/tampered bindings reject, and the chosen legacy policy supports safe recovery without fabricating authority.
- [ ] Observe the intended failures, implement the minimal canonical binding/persistence/validation changes, then run the focused suites and existing recovery regressions.
- [ ] Run real Linux cases on a disposable host with real chown/chmod and interruption/retry behavior. Windows doubles are supplemental. Preserve failed-state resources for diagnosis and recover them only through the supported owned cleanup procedure.
- [ ] Update documentation, run the final gate and return source/evidence to the coordinator. Distinguish local passing results from outstanding Linux or legacy compatibility evidence.

```powershell
./fp.ps1 python -m pytest tests/test_qualification_host.py tests/test_qualification_boundary_cleanup.py tests/test_qualification_container_ownership.py tests/test_qualification_campaign_host.py -q --tb=short
./fp.ps1 check
git diff --check
```

The coordinator performs one final combined focused run covering A and B on the same final source state, extending coverage only for changed consumers or unresolved failures. Report pre-existing gate failures and skips explicitly. Tests requiring Linux must run using the documented installed host procedure, not be counted as passing from a skipped local collection.

**Progress:** Draft only; unassigned until A is reviewed.

## Return packet and coordinator disposition

For each handoff return: checkout path, base and final commit or checksummed working-tree identity, changed-file inventory, behavioral/interface/schema changes, regression evidence, exact commands/interpreter, result counts and skips, verification record paths, remaining dependencies and compatibility limitations. Preserve new source and evidence outside any disposable checkout before it is removed.

The coordinator records A and B as delivered, accepted or blocked separately, checks the complete issue requirements against the final source, and owns any later PR/merge/issue-closure assignment. Closure requires the implementation and verification evidence, not merely this plan or a green unrelated campaign run.
