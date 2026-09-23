# Disposable qualification test host

This remains **incomplete qualification-boundary acceptance**. The default run
checks host readiness. `--test-only` now selects the incremental real N1 capture
suite with its canonical profile, protected TEST_ONLY fixture installer and image
builder. Records explicitly hold qualification acceptance pending the complete
lifecycle, legacy cutover and invariant gate. No passing incremental run closes
Tasks 6–9 by itself.
No same-UID test, parser double or generic Docker result can replace that milestone.

## Trust boundary

The selected boundary design trusts the administrator **and qexec**. Docker daemon
control gives qexec root-equivalent host authority: it can mount host files into a
container and bypass direct filesystem denials, including access to the qg5 result
key. This implementation does not confine a malicious/compromised qexec. qexec must
run only approved supervisor code, with no general Docker RPC exposed to qclient.
See [Docker daemon security](https://docs.docker.com/engine/security/#docker-daemon-attack-surface).

Permission reports identify their scope as `direct_os_access_only`, declare
unrestricted daemon-mediated qexec access, and retain the explicit
`trusted_administrator_and_privileged_qexec/v1` trust model. Readiness reports that
omit this assumption are rejected. qclient/qg5 Docker denial remains required;
direct credential separation checks detect accidental permission weakening, not
an isolation boundary against the privileged supervisor. A constrained broker or
separate daemon would require a different supervisor trust and launch design.

## Supported target and reproducibility

Use a fresh GitHub-hosted `ubuntu-24.04` x64 VM, or a fresh administrator-supplied
Ubuntu 24.04 x64 VM with native ext4 and its own Docker Engine. The public
repository already uses Actions. Standard hosted Linux runners are fresh VMs
and free for public repositories ([GitHub documentation](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)).
Provider VM creation and paid infrastructure are outside this harness.

[host.json](host.json) is the single host configuration. It pins the required
system Python patch, Docker server/package version, installation root and raw
dependency input hashes. The signing version comes solely from
`tools/local_verification/requirements-extra.txt`; `signing-wheel.json` supplies
the reviewed Linux wheel hash without repeating that version. Provisioning derives
the hash-locked pip requirement from those protected inputs and records its digest;
its cffi/pycparser dependencies come from the existing operations lock. Only the
x64 glibc wheel is admitted. Changed locks or installed versions fail setup;
there is no ambient PATH selection, cache fallback, system package upgrade or
Docker configuration change. Package installation targets a new owned venv only.
Configured Python and Docker commands must be absolute paths. Setup, cleanup and
the boundary preflight share one executable rule (`protected_executable` in
`scripts/qualification_boundary_environment.py`, re-imported by `host.py`): every
directory and symlink hop through to the executable target is checked, allowing
protected system aliases but rejecting unowned links and writable intermediate
directories. The copied venv interpreter must report the configured Python patch
before package installation; runtime evidence retains that observed version.

The hosted runner label is **not an immutable OS image**. The manifest records
actual OS/kernel/package inventory, Docker server identity, existing image IDs,
source revision, dirty diff and file hashes. This establishes an auditable
runtime constraint and observed host identity, not bit-for-bit OS reproducibility.
A retained immutable VM image/package snapshot is still needed for that stronger
claim. Validate fresh hosts twice before accepting a new configuration. The CI
matrix performs two independent host-readiness runs; it does not enable a required
qualification acceptance check.

`evidence/host-observations.json` exports the observed package/runtime inventory,
Docker/image inventory, role UIDs and source/configuration identities through an
explicit allowlist. The private resource-ownership manifest and credentials are
excluded; this evidence survives hosted-VM destruction as a CI artifact.

## Administrator commands

Run from an exact candidate checkout on that disposable host:

The administrator orchestrator runs from the original Git checkout, whose
snapshot must match the provisioned manifest. The protected staged code tree
contains no Git metadata; it is used for installed doctor and future trusted
service roles, not as the recorder's source repository.

```bash
sudo bash tools/qualification_verification/provision.sh \
  --manifest-output /tmp/qualification-manifest-path
manifest="$(sudo cat /tmp/qualification-manifest-path)"
host_root="$(dirname "$manifest")"
sudo "$host_root/env/bin/python" -I scripts/fp.py --env "$host_root/env" doctor
sudo "$host_root/env/bin/python" -I scripts/fp.py --env "$host_root/env" python \
  scripts/qualification_boundary_verification.py --host-only --manifest "$manifest"
```

The setup bootstrap uses `/usr/bin/python3` and its pip to create the isolated
environment before the launcher can run. The installed checkout passes its own
launcher doctor immediately after installation. It never modifies a developer's
shared operations/research environment. Run identity is a random private manifest,
not a directory prefix, familiar account name or image tag. Existing qclient,
qexec, qg5 names or reserved numeric IDs cause refusal. Only the newly created
roles may use their configured numeric UIDs: setup rejects any live process
holding one of those UIDs, even without an account entry, under the host-wide
identity lock before publishing a manifest or creating resources. Only the new
qexec receives Docker group membership. Accounts have locked authentication,
no home directory and a non-login shell. Actual UID/group access probes execute
in separate processes after dropping supplementary groups, GID and UID.
Readiness requires each primary GID to equal its configured UID. Canonical
`role_policy.py` permits no supplementary groups for qclient, the Docker group
for qexec, and qclient's socket-access group for qg5. It grants qg5 no access to
qexec's private data or credentials.

Setup binds the source snapshot's configuration and lock digests to the loaded configuration and
checks the staged locks again before creating or installing the environment.
Failed manifest publication removes the unreserved run directory. Cleanup allows
qexec's Docker enrollment to be absent after interrupted setup, while rejecting
unexpected supplementary groups; readiness still requires Docker enrollment.
Each top-level owned tree (`code`, `env`, `data`, `keys`, `scratch`) has one canonical
binding — owner role, group role and mode — in `role_policy.py` (`TREE_BINDINGS`,
`qualification_tree_bindings/v1`). Setup resolves the binding from the run's roles,
retains it in the tree's manifest record (`uid`, `gid`, `mode`) together with the
configuration identity (`tree_bindings`: schema and table digest) before creating
anything, then creates the directory `0700`, applies the mode and transfers ownership.
Setup refuses an umask that masks owner bits or a setgid parent, so the only
intermediate an interrupted setup can leave is an empty root-owned `0700` directory.
Cleanup validates every retained record against the canonical resolution for the
manifest's roles (a manually edited binding is a recorded refusal even when the
filesystem matches it), then compares each tree's actual owner, group and 12-bit mode
with the record before any recursive deletion; owner, group or mode drift is a named failure
that retains the tree, its contents and the identity reservation, writes a failure
receipt and no retirement certificate, and cleanup succeeds once the binding is
restored. For interrupted setup only (provisioning/failed setup), cleanup also
accepts that exact empty root-owned `0700` intermediate for any tree.
Manifests written before tree bindings (v3 records carrying only `uid`) are still
retirable on what their producer determined: the record's `uid` must be that
producer's owner for the path (`LEGACY_TREE_OWNERS`), and the tree's owner and
group must both equal it (the producer ran `chown(uid, uid)`); its mode was
umask-dependent, is never synthesized, and is not checked. Such retirements are
listed under `legacy_tree_bindings` in the receipt.
Incomplete setup may also retain venv's root-owned `env/lib64 -> lib` alias.
Cleanup validates that exact alias and unlinks it with the environment tree
without following it; other links and completed-host aliases remain rejected.
Cleanup creates a process group only when an existing account needs a deletion
command. A never-used empty group can be removed without `cgroup.kill`; populated
groups still require successful termination before retirement. This permits
cleanup after initial cgroup creation fails without weakening child isolation.
Setup reserves the ownership manifest before each resource operation. It retains
failed setup state and diagnostics; the CI `always()` cleanup step, or the explicit
command below, retires verifiably owned resources. No worker, service or release
is created by this slice. Ephemeral execution/result keys are TEST_ONLY raw
Ed25519 keys in separate private credential directories; bytes never enter logs.
Additional freeze/seal keys and release enrollment belong to the approved fixture
producer. The source snapshot is copied and hash-checked into administrator-owned
storage; no development checkout is mounted into a worker.

The wrapper reuses `RunRecord`, rejects empty/failed/skipped or malformed JUnit,
checks source stability and propagates cleanup failures. Readiness tests exercise
real access denials, deliberate permission weakening, active-UID cleanup refusal,
wrong-owner refusal, symlink escape refusal, installed source custody and doctor.
Windows unit tests are diagnostic tests only; their symlink skip is not accepted
in either disposable Linux job.

## Running the S2 workflow as evidence

`.github/workflows/qualification-s2-supervision.yml` provisions one fresh
`ubuntu-24.04` host, runs one boundary selection, enforces the invariants and
cleanup, and uploads the `qualification-s2-supervision` artifact. The default
mode is s3, which runs the files named by `S3_CASES` in
`scripts/qualification_boundary_verification.py` (record scope `S3_N1_CAPTURE`);
`-f mode=s2` runs the subset named by `S2_CASES` (scope
`S2_DIAGNOSTIC_SUPERVISION`). The required nodes are the registered nodes of
`tests/ops/qualification/invariant_manifest.json` inside the selected files,
recorded as `invariants.json`'s `required_nodeids`. A run is about
25 minutes: 6-8 minutes of provisioning plus three cases that are about 300 s
each by design (service downtime, deadline-before-bootstrap, two descendants to
the wall). **A green check mark is not evidence; the artifact is.**

Order of operations for an executor (the two clocks are independent; the
`s2-linux-run` project skill carries the same procedure for agents):

1. Commit on frozen bytes (`git diff --stat` first) and push the branch.
2. Dispatch the Linux run **first**, then run the local `fp.ps1` lines while it
   executes:

   ```bash
   gh workflow run qualification-s2-supervision.yml --ref <branch>
   gh run list --workflow=qualification-s2-supervision.yml --event workflow_dispatch --commit <sha> --json databaseId,headSha,displayTitle,status,createdAt
   ```

   `<sha>` is the full head you pushed. Poll the list every few seconds until a
   run created after your dispatch appears (its `createdAt` is later than your
   dispatch and its `displayTitle` names your mode), rather than waiting a fixed
   `sleep`. Never take the newest run of a branch listing (`--limit 1`): the
   pull-request run on the same SHA is sometimes the newer one. Confirm the
   listed `headSha` is the head you pushed.
3. Keep the tree frozen until the last local record closes: the recorder hashes
   the checkout before and after its command and voids the record if any byte
   changed. The `guard_open_verification_record.py` PreToolUse hook refuses
   Edit/Write into a checkout with a `running` record; put drafts in the session
   scratchpad.
4. Do not push again while a run is in flight: the workflow's per-ref
   `cancel-in-progress` cancels it, and on a pull-request branch every push
   refires the path-filtered workflow. Batch docs commits until the run you need
   has finished. Never dispatch the same SHA twice.
5. Read the artifact, not the check:

   ```bash
   python scripts/s2_run_evidence.py <run-id> --expect-head <sha>
   ```

   It downloads the artifact outside the repository and exits 0 only when
   `record.json` (completed, exit 0/0, `source_stable`, `capture_complete`,
   cleanup ok, the expected scope, a measured `before.commit`), `invariants.json`
   (`passed`, and a non-empty `required_nodeids`: the selection's required
   nodes, currently 15 for s2 and 19 for s3) and `junit.xml` (at least that many
   tests, no failures, errors or skips) all hold. The expected scope is
   `S3_N1_CAPTURE` unless `--expect-scope S2_DIAGNOSTIC_SUPERVISION` asks for an
   s2-mode run. A dispatch run must have measured its head (`tested_commit`
   equals `headSha`); a pull-request run tested `refs/pull/N/merge`, which the
   reader prints as `tested_commit_kind: pull_request_merge`. Cite the run ID,
   head SHA, record ID and counts.

   A dispatch with `-f mode=s3 -f cases='<pytest -k expr>'` is a labelled
   diagnostic of that subset (run titled `S2 DIAGNOSTIC (…)`, record scope
   `DIAGNOSTIC_SUBSET`); the script above refuses it whatever its outcome. Use
   it to iterate on one case; it is never evidence.
   A diagnostic run always ends red (exit 2), even when every selected case
   passed, and two diagnostics on one ref cancel each other.

A failure on unchanged code is a finding, not flakiness. Before any second
dispatch, pull the failing work's chain from `boundary/journal.sqlite`
(`full_campaign_budgets`, `full_campaign_objects` roles `supervision_event_*`),
line it up against `journal.log`, `kernel.log` and `systemd-units.log`, and
compare its timing with the last green run's same case; state the cause in one
sentence with a file and line, fix it, then dispatch once. Worker packets report
runs as evidence and say "Linux acceptance pending" when no green run exists on
the final bytes; acceptance needs the integrated pull-request run on the final
head plus independent review, never a branch run alone. Windows or mocked
results are never Linux evidence.

## Boundary integration contract and unresolved acceptance

`scripts/qualification_boundary_environment.py` exposes
`inspect_environment(instance_path, profile_bytes, *, host_config)` and
`require_environment`. `host_config` is the ownership manifest's retained
`host_config` (the fixture passes `manifest['host_config']`); the preflight never
reloads the checkout's `host.json` and never resolves a client through `PATH`.
Its `docker_client` check validates the configured `docker` executable with the
shared protected-executable rule before `docker version` and `docker image
inspect` run through it and the instance's fixed local socket; a missing,
malformed or unprotected client fails readiness without being invoked, and the
`docker`/`image` checks are then absent rather than passed. The `image`
observation retains only the opaque worker content ID (`{"id": ...}`);
`RepoDigests`/`RepoTags` name registries and repositories and never enter
`evidence/boundary/environment.json`, which CI exports with the rest of
`evidence/`. The closed `qualification_test_instance/v1` document
is administrator-owned and supplies `authority_class: TEST_ONLY`, the three role
UIDs, trusted roots, data/key/scratch/evidence paths, fixed local Docker socket,
worker content ID and canonical profile hash. The boundary fixture producer must
write this document from its real approved release, never substitute a fabricated
profile or arbitrary image. `parse_profile` is imported from the canonical
boundary module; the preflight owns no second inventory of worker security flags.

After integration, the supported launcher entry remains:

```bash
python -I scripts/fp.py doctor
python -I scripts/fp.py python scripts/qualification_boundary_verification.py --test-only \
  --manifest /absolute/private/ownership.json
```

`--s2` selects the targeted diagnostic supervision suite
(`tests/integration/qualification_boundary/test_campaign_supervision_linux.py`)
on one fresh host: the installer enrolls the campaign host (qexec's transient-unit
polkit rule plus the common memory slice) and installs the
execution-capable diagnostic release, and every probe goes through the warm
service's funded private route via the forked transport child. The suite runs
alone with one worker and its last case exhausts the common memory group, so the
host is never reused. The `Qualification S2 supervision` workflow runs it on
`workflow_dispatch` or on pull requests touching the qualification surface; its
record is diagnostic evidence for the coordinator, not an acceptance check.

Under the accepted polkit rule, qexec can start arbitrary transient units —
including units that run as `User=root` — because
`org.freedesktop.systemd1.manage-units` carries no `unit` detail on a transient
start (systemd's `StartTransientUnit` check passes none), and a named unit is
authorized only when its name carries this run's slice prefix. Polkit therefore
contributes no containment for unit starts: whether a started unit joins the
campaign slice hierarchy rests on the guardian's own code checks and on
`bootstrap.py`'s fixed `campaign_control` prefix check, not on polkit. This
stays inside the recorded trust model, under which qexec is already
root-equivalent through the Docker daemon.

```bash
sudo "$host_root/env/bin/python" -I scripts/fp.py --env "$host_root/env" python   scripts/qualification_boundary_verification.py --s2 --manifest "$manifest"
```

The administrator fixture producer owns the installed instance/profile; caller
substitutions are rejected. The incremental suite builds the worker from an exact
source allowlist, resolves the Python base to a content digest, installs the shared
hash-locked dependencies and records build identity. The original Python base and
daemon build cache remain for disposal with the fresh VM; cleanup never prunes
shared daemon resources. The workflow's manual `boundary` input selects this suite
on two fresh hosts. Its result is diagnostic until the outstanding acceptance
requirements below are complete.

Still required from the boundary owner: losing and passing N1 through G5;
fabrication rejection; duplicate/concurrent submission; restart/no-redraw;
VOID races; malformed output; exact profile/image/release bindings; real worker
permission probes; daemon loss; handled interruption and hard-kill recovery;
cleanup interruption/restart and owned container/service absence. Critical skips
must fail. Current signing/key validity remains distinct from historical facts.

## Cleanup, migration and rollback

Ownership schema v3 retains the resolved host configuration and exact role IDs,
and requires the owned subprocess lifecycle below.
Cleanup validates each name/ID binding against that retained configuration, so a
later configuration update cannot strand a previously provisioned installation.
Legacy v1/v2 manifests do not prove that subprocesses have stopped; use external
VM-owner retirement instead of certifying cleanup with the new tooling. No live
legacy test host is carried forward by the ephemeral CI jobs.

The disposable host must expose writable administrator-owned cgroup v2 at
`/sys/fs/cgroup`, including `cgroup.kill`. Before any mutating subprocess runs,
the orchestrator durably registers an exact per-run cgroup in private
`process-groups.json`; the child joins it before executing its payload. Descendants
inherit that membership even if they create a new session. `start_owned` applies
the same registration-before-launch rule to installed service children. Docker
cleanup commands also run in a registered group; worker containers have separate
exact identity validation.

Cleanup kills every registered cgroup and removes it before touching account or
filesystem resources. A removed cgroup rejects a delayed child's entry, so that
child cannot execute its payload. Cleanup's account-management commands use a
fresh registered cgroup too; retries stop surviving cleanup children before
continuing. Group names are never reused. Failure to kill/remove any group keeps
the identity reservation and prevents retirement. Registrations survive with the
private ownership metadata; they are not exported as public observations.

One administrator-owned reservation at `/var/lib/fp-qualification-identities`
serializes collision checks, creation and retirement of the shared account names
across all installation roots. Its durable owner survives process termination;
only the owning manifest can retire a partial setup. Both global and per-run
locks are acquired before cleanup reads current ownership state. An atomically
published retirement certificate makes retry safe even after resource deletion
or identity reuse by a later run. Global reservation bookkeeping is retained for
the disposable VM owner; it is never removed by per-run cleanup.

```bash
sudo /usr/bin/python3 -I tools/qualification_verification/cleanup.py \
  --manifest /absolute/private/ownership.json
```

Cleanup validates root-owned private metadata and every resource before removal.
It refuses active principal processes, changed account IDs, tree owner/group/mode
drift from the retained binding (apart from the documented initial-creation
exception), shared role groups, unexpected
links, mounts and unsupported resource kinds. It removes only exact recorded trees and
newly created identities, stops cleanup children, then writes a new immutable linked cleanup receipt.
Missing resources are idempotent success. Private ownership metadata, public
non-secret evidence and prior receipts remain; original run records are not
rewritten. A hard kill leaves an incomplete run; cleanup cannot promote it to
success. A concurrent setup/cleanup lock prevents competing administrators from
retiring a reserved host. A private boundary registry records build intent before
image creation and binds the completed image to its signed release. Cleanup checks
container IDs, host/execution labels, exact names, image IDs and durable journal
dispatch membership before removal. Image retirement requires the exact build
identity and refuses remaining consumers. Unexpected containers block cleanup.
There is no prune, wildcard resource
removal, shared-image deletion, Docker reset or implicit VM destruction.

Cleanup validates each top-level tree's retained owner, group and mode before
recursive deletion ([#424](https://github.com/Joshua-Asante/first-passage/issues/424)).
That is top-level binding validation, not a policy for every descendant and not a
defense against a hostile administrator: do not broaden access to or repurpose these
disposable run directories for unrelated files, because recursive cleanup still
treats their contents as run-owned. It does not by itself establish shared or
reused-host support. Current acceptance is for fresh disposable hosts with the
administrator and qexec trust assumptions above.

Cutover inventory: no real boundary workflow/runner existed on base `24acf9a`.
This is new capability; no old consumers or resources are eligible for retirement.
Retain `tools/local_verification`, `scripts/docker_verification.py`, their cached
image and ordinary sequence tests. Shared Docker Desktop, WSL, existing accounts,
services and production installations are outside ownership. No required checks
are changed. The boundary owner must retain any additional regression coverage
when performing the later acceptance cutover.

Export non-secret evidence and cleanup receipts before the VM owner destroys the
VM. CI exports an allowlist of evidence/receipts, never private manifests or keys.
For complete retirement the external VM owner destroys its exact VM. If host
setup or isolation fails, repair/reprovision and regenerate ephemeral keys; keep
qualification acceptance blocked. Generic Linux tests remain available but cannot
serve as fallback acceptance.
