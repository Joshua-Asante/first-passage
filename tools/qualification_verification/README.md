# Disposable qualification test host

This is a **host-readiness implementation**, not completed qualification-boundary
acceptance. The boundary service, canonical ExecutionProfile, approved TEST_ONLY
release/image fixture producer, and launch-to-G5 integration suite are not present
on the base revision. `--test-only` fails closed until that owner integrates them.
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

Use a fresh GitHub-hosted `ubuntu-24.04` x64 VM, or an administrator-supplied
Ubuntu 24.04 x64 VM with native ext4 and its own Docker Engine. The public
repository already uses Actions. Standard hosted Linux runners are fresh VMs
and free for public repositories ([GitHub documentation](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)).
Provider VM creation and paid infrastructure are outside this harness.

[host.json](host.json) is the single host configuration. It pins the required
system Python patch, Docker server/package version, installation root and raw
lockfile hashes. The signing wheel hash was resolved from PyPI's 50.0.1 release;
its cffi/pycparser dependencies come from the existing operations lock. Only the
x64 glibc wheel is admitted. Changed locks or installed versions fail setup;
there is no ambient PATH selection, cache fallback, system package upgrade or
Docker configuration change. Package installation targets a new owned venv only.

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
qexec receives Docker group membership. Accounts have locked authentication,
no home directory and a non-login shell. Actual UID/group access probes execute
in separate processes after dropping supplementary groups, GID and UID.

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

## Boundary integration contract and unresolved acceptance

`scripts/qualification_boundary_environment.py` exposes `inspect_environment`
and `require_environment`. The closed `qualification_test_instance/v1` document
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
  --manifest /absolute/private/ownership.json \
  --instance /absolute/protected/instance.json --profile /absolute/protected/profile.json
```

The current wrapper retains the preflight, then rejects boundary acceptance even
if readiness passes. The integration owner must replace that explicit blocker
with the real unchanged acceptance selection, add launch/inspection/event evidence,
verify staged-source identity and extend exact container/service ownership cleanup.
Do not remove it merely because host-readiness tests pass.

Still required from the boundary owner: losing and passing N1 through G5;
fabrication rejection; duplicate/concurrent submission; restart/no-redraw;
VOID races; malformed output; exact profile/image/release bindings; real worker
permission probes; daemon loss; handled interruption and hard-kill recovery;
cleanup interruption/restart and owned container/service absence. Critical skips
must fail. Current signing/key validity remains distinct from historical facts.

## Cleanup, migration and rollback

Ownership schema v2 retains the resolved host configuration and exact role IDs.
Cleanup validates each name/ID binding against that retained configuration, so a
later configuration update cannot strand a previously provisioned installation.
Legacy v1 manifests are diagnostic evidence only for this version; use the v1
tooling or external VM-owner retirement rather than guessing their reservation
ownership. No live v1 test host is carried forward by the ephemeral CI jobs.

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
It refuses active principal processes, changed owners/IDs, shared groups, links,
mounts and unsupported resource kinds. It removes only exact recorded trees and
newly created identities, then writes a new immutable linked cleanup receipt.
Missing resources are idempotent success. Private ownership metadata, public
non-secret evidence and prior receipts remain; original run records are not
rewritten. A hard kill leaves an incomplete run; cleanup cannot promote it to
success. A concurrent setup/cleanup lock prevents competing administrators from
retiring a reserved host. Unexpected boundary containers block cleanup until their
owner supplies exact-ID lifecycle integration. There is no prune, wildcard resource
removal, shared-image deletion, Docker reset or implicit VM destruction.

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
