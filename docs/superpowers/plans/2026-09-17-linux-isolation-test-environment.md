# Disposable Linux Isolation Test Environment Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make real qualification-boundary tests reproducible on a disposable Linux host with early prerequisite failures and revision-bound evidence.

**Architecture:** Use a disposable Linux VM/CI runner with its own Docker Engine and native Linux storage. Administrator setup creates protected test installations and distinct qclient/qexec/qg5 identities; test actions run as the designated identities. Reuse the qualification boundary's canonical ExecutionProfile and the existing verification recorder.

**Tech Stack:** Linux, Docker Engine, Unix peer credentials, separate UIDs, locked operations Python environment, TEST_ONLY Ed25519 keys, existing launcher/recorder.

**Spec:** [Qualification execution-boundary design](../specs/2026-09-17-qualification-execution-boundary-design.md), particularly sections 3, 6, 10 and 11; [boundary implementation plan](2026-09-17-qualification-execution-boundary.md), Task 7. Local workflow improvements are in [the companion plan](2026-09-17-testing-workflow-improvements.md).

## Global Constraints

- Planning only; no provisioning, installation, identity creation or Docker changes occur under this drafting request.
- No production credentials, qualification workloads, deployment or live broker access.
- Use real separate processes/UIDs and containers. A same-owner Docker test harness is not isolation acceptance.
- TEST_ONLY reduces fixture workload, not provenance or permission requirements.
- Follow AGENTS.md and the checkout's launcher. Do not bypass failed environment validation.
- Keep all secrets outside versioned configuration and public evidence logs.
- Canonical ExecutionProfile owns worker security settings; do not duplicate Docker flag inventories here.
- Missing Docker, UID provisioning, approved test image or critical Linux tests is failed setup/acceptance, not a successful skip.

## Ownership and prerequisites

The qualification implementation coordinator owns launch-to-G5 acceptance. This plan owns the reproducible test host and prerequisite evidence; it does not implement or substitute for the qualification service.

The main boundary plan already proposes `scripts/qualification_boundary_verification.py`, integration fixtures and `.github/workflows/qualification-execution-boundary.yml`. Extend those artifacts under one owner rather than build a competing harness.

Administrator/test-host owner supplies a disposable VM or hosted ephemeral Linux runner, Docker endpoint and setup privileges. Build tooling supplies image/runtime manifests. Boundary implementation supplies the profile, approved TEST_ONLY release builder, service, worker and G5 entry points. Those capabilities must exist before end-to-end acceptance can run.

### Task 1: Freeze and reproduce the disposable host configuration

**Outcome:** A fresh test host can create the same declared runtime and record its actual installed identities without depending on a developer's ambient PATH, WSL settings or production host.

**Files:** Create `tools/qualification_verification/host.json`, `tools/qualification_verification/provision.sh`, `tools/qualification_verification/README.md`; coordinate changes to `.github/workflows/qualification-execution-boundary.yml` with the boundary owner.

- [ ] Define one versioned host configuration: schema, supported OS release, Python version, Docker package version, lockfile hashes and installation layout. Resolve actual available versions when implementing; record observed patch versions and resulting image IDs. Do not guess hashes or claim an unpinned OS package set is reproducible.
- [ ] Choose the initial supported target as a disposable Ubuntu 24.04 VM/CI runner with native ext4 storage. Keep provider-specific VM creation outside the harness. Document the required administrator entry point and reject unsupported hosts clearly.
- [ ] Provision isolated operations environments from hash-locked dependencies and an explicitly locked signing dependency. Never change a developer's shared environment. Install trusted source/runtime roots as administrator-owned and not writable by the test principals.
- [ ] Create separate test identities, private key directories and a qexec-owned data root. Give only qexec the required Docker access. Ensure qclient and qg5 cannot gain it through supplementary groups. Generate ephemeral TEST_ONLY keys and obtain release/image bindings through the boundary fixture producer.
- [ ] Track every created resource in a private ownership manifest before depending on it. A failed setup retains diagnostic evidence and cleans only verified owned resources; never blanket-prune Docker or delete paths obtained from untrusted artifacts.

**Acceptance:** Provision twice on fresh disposable hosts. Both pass launcher doctor and emit complete observed manifests. Deliberately altered lock/version inputs fail rather than silently use a cached runtime. This establishes setup reproducibility, not execution-boundary acceptance.

### Task 2: One preflight explains missing prerequisites before replay starts

**Outcome:** The boundary runner fails quickly with actionable evidence when isolation prerequisites are absent; no qualification worker starts during a failed preflight.

**Files:** Create `scripts/qualification_boundary_environment.py`, `tests/test_qualification_boundary_environment.py`; extend the boundary owner's `scripts/qualification_boundary_verification.py`.

**Proposed interfaces:**

```python
def inspect_environment(instance_path: Path, profile_bytes: bytes) -> dict:
    """Return observed prerequisite facts and explicit failures; never provision."""

def require_environment(report: dict) -> None:
    """Raise ValueError when any mandatory prerequisite failed."""
```

The protected instance configuration supplies paths and UIDs. `parse_profile` validates canonical profile bytes. The runner invokes inspection before source computation and retains the report through the existing recorder; inspection does not approve a release or replace runtime launch checks.

- [ ] Add tests for missing daemon, non-Linux host, mismatched image/profile, absent signing dependency, identical role UIDs, writable trusted code, denied evidence directory and insufficient setup privileges. Use parser/unit doubles only for fast diagnostics tests.
- [ ] Probe effective groups and access as each real UID. Check denial of qclient/qg5 journal writes, qclient execution/result key reads, and qclient Docker access. Check qexec and qg5 can access only their intended credentials. Do not log secret bytes.
- [ ] Check Unix peer credential support, native filesystem permissions, Docker server/image identity, required isolation settings, scratch/storage availability and evidence-directory writability. Read the canonical profile instead of inventing a second configuration.
- [ ] Exercise each failure on a disposable host by changing only test-owned resources. Assert a nonzero setup result, named failed prerequisite, no worker launch and safe cleanup. Restore or recreate the test environment before the positive run.

**Acceptance:** Real denied-access probes and positive prerequisite checks are recorded with actual UIDs, groups, paths and runtime identities. A completed preflight is explicitly labeled environment readiness, never boundary-test success.

### Task 3: Run the existing boundary acceptance suite on the provisioned host

**Outcome:** One documented invocation produces real launch-to-G5 evidence and fails on critical skips, incomplete capture or cleanup errors.

**Files:** Integrate with `tests/integration/qualification_boundary/`, `scripts/qualification_boundary_verification.py`, `.github/workflows/qualification-execution-boundary.yml`, and `tools/qualification_verification/README.md`. These overlap the main implementation plan intentionally and require its coordinator's integration.

- [ ] Stage the exact candidate source snapshot, lockfiles and synthetic fixture inputs. Preserve candidate revision and dirty-source hashes; source copied to the VM must match that recorded snapshot. Use no host development checkout mounts in qualification workers.
- [ ] Run doctor and the environment preflight, then the unchanged acceptance selection. Require both real losing-N1 and passing-N1 flows, fabrication rejection, key/UID permissions, duplicate submissions, restart/no-redraw, VOID races and malformed-output cases specified in the boundary plan.
- [ ] Invoke qclient and qg5 as real distinct UIDs. Keep administrator orchestration outside the tested client. Retain container launch events, actual inspected settings and attempted permission failures; fixture counters alone do not prove launch count.
- [ ] Have the wrapper propagate failed tests, critical skips, source drift, malformed reports and cleanup failures. Use `sys.executable` for child Python processes. Extend RunRecord rather than add a second acceptance recorder.
- [ ] Test handled interruption and hard-kill recovery. A hard-killed run remains incomplete; a separate administrator cleanup invocation uses the ownership manifest and exact resource IDs. Keep old evidence immutable.

Required supported-host commands:

```bash
python -I scripts/fp.py doctor
python -I scripts/fp.py python scripts/qualification_boundary_verification.py --test-only
```

**Acceptance:** A fresh-host run completes with no critical skips, stable source, validated reports and confirmed owned cleanup. Deliberate permission weakening, missing Docker and incomplete output each produce nonzero verification. Preserve the distinction between historical signed facts and current validity.

## Supersession, migration and teardown

The current generic Docker harness runs ordinary tests inside a developer-controlled container and records their evidence. That remains useful. The new host replaces any use of that harness as proof of the qclient/qexec/qg5 security boundary; it does not replace ordinary Linux test execution.

| Existing component or capability | Disposition | Reason / retirement condition |
| --- | --- | --- |
| `tools/local_verification/run.ps1`, its Dockerfile/requirements and `scripts/docker_verification.py` | Retain for ordinary Linux regression and sequence tests | The qualification runner has different principals, isolation and source-custody requirements |
| Cached `first-passage-verification:py311` image | Retain while generic tests use it | It is not an approved qualification worker image; do not relabel it as one |
| Developer Docker Desktop and WSL distributions | Retain | Shared infrastructure outside test-run ownership; no uninstall, reset or integration changes are part of teardown |
| Existing `DockerOwner` label/CID cleanup and RunRecord | Reuse where contracts fit | Preserve historical `fp.verification.run` cleanup support while old runs/resources may exist |
| Duplicated environment checks in prospective boundary fixtures/workflow | Consolidate | New environment preflight is the canonical prerequisite implementation; consumers call it |
| Boundary service's launch-time image, permissions, approval and validity checks | Retain | Preflight is a snapshot and cannot replace checks at the authority boundary |
| Same-UID fixture or mocked launch counted as isolation acceptance | Retire that acceptance claim | Real UID/container tests become mandatory; retain useful parser/state-machine unit tests labeled with their narrower scope |
| One-off test-host provisioning commands and host-specific overrides | Replace only when identified | Migrate their required behavior into versioned host configuration; delete maintained duplicates after fresh-host acceptance |
| The boundary plan's proposed verification script, workflow and fixtures | Integrate, do not fork | This plan augments those deliverables under their existing coordinator |

### Task 4: Cut over acceptance and dismantle owned obsolete resources

**Outcome:** Qualification isolation acceptance has one supported execution path, old evidence remains interpretable, and superseded test-owned resources are removed only after their users stop.

**Files:** Extend `tools/qualification_verification/README.md`, `scripts/qualification_boundary_verification.py`, `.github/workflows/qualification-execution-boundary.yml` and environment tests. Create `tools/qualification_verification/cleanup.py` for manifest-scoped cleanup if the boundary harness does not already provide an equivalent implementation; otherwise extend that implementation.

- [ ] Before provisioning, inventory existing boundary jobs, scripts, test identities, test service units, sockets, directories, images, containers and VM resources. Capture exact owner/run identity and consumer references. Do not infer ownership from a familiar name such as `qexec`, an image tag or a directory prefix.
- [ ] Record the cutover map: old entry point, its consumers, successor command, parity evidence and resources eligible for retirement. If no previous real boundary harness exists, mark this as new capability and limit teardown to newly created test resources and genuinely duplicated code.
- [ ] Accept the fresh-host positive and negative runs from Tasks 1–3 before switching required qualification acceptance to the new path. If an old job supplies additional regression coverage, retain it or migrate that coverage explicitly. Avoid duplicate required jobs running the same selection after cutover.
- [ ] Update active documentation and CI callers together. Preserve a small compatibility wrapper only when an identified consumer requires it; it must delegate to the single new implementation, retain exit codes, and have a named removal condition. No fallback from failed isolation to a passing generic Docker run.
- [ ] Drain old test runs before disabling their jobs or stopping resources. Preserve finalized evidence; incomplete runs remain incomplete. Record cleanup in a separate linked receipt instead of altering an old signed artifact or pretending the original run completed successfully.
- [ ] Cleanup verifies an administrator-owned manifest, resolved paths under the designated disposable root and exact resource ownership. Stop only owned test services/processes, confirm termination, remove exact owned containers and test mounts, then sockets and ephemeral keys. Reject links, path escape, ownership mismatch or uncertain liveness.
- [ ] Remove only identities/groups created for that disposable host after confirming no live process or shared use; never delete pre-existing identities. Remove installed test units and their protected configuration only when manifest-owned. Never reset a shared Docker daemon, prune globally, remove shared images or delete a developer's operations environment.
- [ ] Retain versioned image manifests and acceptance evidence before retiring old images. Delete an image only after checking its actual content ID, active/stopped container consumers and other retained test configurations; deleting a tag alone does not establish content ownership. Prefer VM destruction for complete disposable-host retirement, after evidence export is verified.
- [ ] If the VM was supplied externally, its owner performs final VM destruction. If provisioning created it, use its exact recorded provider identity. No resource-name wildcard cleanup. Report anything deliberately retained and its owner; a cleanup failure prevents full teardown acceptance.
- [ ] Add real disposable-host teardown tests: active-run refusal, wrong-owner refusal, path/link escape rejection, repeated cleanup, interruption mid-cleanup followed by restart, unrelated sentinel resource survival and confirmed absence of all owned ephemeral secrets/services/containers.

**Proposed cleanup command contract:** `cleanup.py --manifest <absolute private ownership manifest>` acts only on that manifest's inactive run. Missing resources are idempotent success; ambiguous ownership or active resources fail closed. Cleanup writes a new receipt identifying checks, removed IDs, retained resources and failures. Test-secret bytes never enter the receipt. This command must not be implemented as an unrestricted recursive delete or Docker prune wrapper.

**Acceptance:** Required qualification checks resolve to the real isolated runner; obsolete acceptance routes cannot report success; ordinary sequence coverage remains available; unrelated resources survive cleanup; all owned ephemeral resources are absent or explicitly reported as teardown blockers.

**Rollback:** Keep the previous configuration/source manifests and generic regression path. If the new isolation host fails, block qualification acceptance while repairing or reprovisioning it. Do not restore same-user or mocked tests as equivalent acceptance. Recreate ephemeral TEST_ONLY keys for a replacement host and regenerate approved fixture identities; deleted keys need not be recovered.

## Delivery evidence and remaining decisions

Deliver the provisioning configuration, documented invocation, prerequisite report and complete synthetic acceptance record. Report actual tested revision/fingerprint, interpreter, Docker/image/profile identities, commands, counts, denied-access results and cleanup status.

Before provisioning, the test-host owner must identify the disposable VM/CI execution target and authorize any required infrastructure spend. No remote account or paid service is assumed available. Local Docker Desktop and WSL can support ordinary development tests; neither is automatically accepted as this plan's isolated host.

Environment work can be accepted before the qualification service is ready, but the end-to-end milestone remains blocked until its real entry points and fixtures exist. Production host provisioning, production keys, N2/Part A protection and qualification remain outside this plan.
