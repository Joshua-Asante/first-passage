# PR 420 provisioning lifecycle repairs

> **For agentic workers:** Execute with superpowers:executing-plans. The coordinating agent owns implementation and combined acceptance; no delegation is needed.

**Goal:** Close the four review findings on e45ebf2 without changing the approved qexec trust model.

**Architecture:** Validate the dependency bytes actually staged for installation against the retained host configuration. Bind every provisioning subprocess and descendant to an administrator-owned, run-specific cgroup v2 before executing its payload. Cleanup closes that process boundary before retiring filesystem and account resources.

**Tech Stack:** Python operations launcher, Linux cgroup v2, pytest, existing disposable Ubuntu CI hosts.

**Spec:** PR #420 review comments 4040282116, 4040282123, 4040282129, 4040282135; tools/qualification_verification/README.md.

## Contract and scope

- The manifest owns the retained configuration, source snapshot, role identities and exact child cgroup. The coordinator owns the integrated outcome.
- No installation may consume locks that differ from the retained configuration, including drift during host probes or staging.
- Before payload execution, a child joins the recorded cgroup; descendants inherit it. A delayed join to a removed cgroup fails before payload execution.
- Cleanup holds both existing locks, kills the owned cgroup, waits for removal, then validates/removes other resources. Failure to stop children keeps the reservation and blocks retirement. Retries accept an already-removed child cgroup.
- Ownership schema v3 identifies this child-lifecycle guarantee; old manifests cannot claim it. Previously completed ephemeral hosts require no migration.
- qclient/qg5 have only their configured primary groups; qexec has its primary group plus Docker. Unexpected memberships fail readiness. This does not constrain trusted qexec daemon authority.
- Shared WSL/Docker Desktop and production hosts remain outside qualification ownership. Real lifecycle acceptance runs on the two disposable Ubuntu CI hosts.

## Implementation and evidence

- [ ] Add regression tests for both lockfiles changing during host probes and during staging; keep the original configuration-hash regression.
- [ ] Check snapshot lock identities before claiming resources and staged lock digests before venv/pip activation.
- [ ] Add exact supplementary-group regressions for all roles, missing Docker, wrong primary GID and valid expected sets. Replace the denylist in scripts/qualification_boundary_environment.py.
- [ ] Compare observed Docker version with the manifest configuration in the installed-source readiness test.
- [ ] Add the owned-child cgroup lifecycle and route every mutating provisioning command, including pip, through its execution barrier.
- [ ] Add real Linux tests for hard-killed provisioner with child/grandchild, delayed entry after retirement, interrupted cleanup retry and fail-closed cgroup cleanup. Test wrappers locally without claiming Windows establishes cgroup semantics.
- [ ] Update ownership fixtures and README for schema v3 and cgroup prerequisites/recovery.
- [ ] Run launcher doctor, focused pytest with two workers and repository gates. Inspect verification records for completion, stable source and complete capture.
- [ ] Inspect the final diff, push to the existing PR, answer the four findings and monitor both disposable-host jobs plus other CI checks. Do not merge.

## Related-case map

| Boundary | Cases | Required evidence |
| --- | --- | --- |
| Config to installed dependencies | Both locks; probe-time and staging-time edits; valid unchanged bytes | Rejection before activation, plus successful real provisioning |
| Provisioning to retirement | Account commands, venv, pip and key generation; child and descendant; late spawn; cleanup interruption | One shared execution barrier; real process/cgroup tests; reservation retained on failure |
| OS role identity | Every role; unexpected membership; missing Docker; wrong primary GID | Exact-set checks, valid nearby cases and real UID readiness |
| Canonical host version | Docker observation versus retained config | Existing installed-host assertion reads the retained value |
