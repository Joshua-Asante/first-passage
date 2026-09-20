# Qualification #423/#424 — disposable-Linux evidence handoff

> **For agentic workers:** Execute with superpowers:executing-plans. This is a bounded evidence assignment: run the documented disposable-host procedures on the delivered source, inspect the exported evidence, and return source-bound results. Do not extend the implementation unless a run exposes a defect, and then return the defect rather than fixing it broadly. The coordinator owns acceptance and issue closure.

**Goal:** Produce the real-Linux evidence that Handoffs A (#423) and B (#424) could not produce on the Windows development host, so the coordinator can decide final acceptance of both issues.

**Spec:** [Issue #423](https://github.com/Joshua-Asante/first-passage/issues/423), [issue #424](https://github.com/Joshua-Asante/first-passage/issues/424), the parent plan [2026-09-19-qualification-issues-423-424.md](2026-09-19-qualification-issues-423-424.md) (both executor returns and the B design checkpoint), and `tools/qualification_verification/README.md` on the branch below.

## Source basis

- Branch `claude/qualification-issues-423-424-88fd15`, local only (no upstream, never pushed), in the worktree
  `C:/Users/joshu/multi_firm_operations/.claude/worktrees/review-leftover-worktrees-d12e00`:
  - `f2606b0` = `origin/main` at drafting time (recheck: `git fetch origin main && git log --oneline f2606b0..origin/main`).
  - `9680ed2` — Handoff A (#423): `inspect_environment(…, *, host_config)`, `docker_client` readiness check, image observation `{'id': …}` only; delivered, **not yet accepted**.
  - `2ff3b5e` — Handoff B (#424): canonical tree bindings; **accepted as a local implementation** on 2026-09-20.
- Durable copies of both patches and every Windows verification record: `C:/Users/joshu/multi_firm_operations/tmp/handoff-423-424/{a-delivered-2026-09-19,b-delivered-2026-09-20}/`.
- Windows state at `2ff3b5e`: focused suites 235 passed / 2 skipped (record `.cache/fp-verification/20260920T033845Z-832d22be43a5`), `./fp.ps1 check` exit 0 (`20260920T033925Z-292628fa9fa3`), whole-repo pylint 8.04. These prove nothing about Linux ownership, modes, umask or Docker; that is what this assignment supplies.
- Standing limitation to carry into every claim: legacy v3 manifests (records with `uid` only) validate the producer-determined owner **and group** but **not mode**; documented in the README and excluded from any "full permission-drift protection" claim.

## What "disposable host" means here

The repository's only supported procedure is `tools/qualification_verification/provision.sh` → the installed checkout's launcher → `scripts/qualification_boundary_verification.py` → `tools/qualification_verification/cleanup.py` on a **fresh Ubuntu 24.04 x86_64** machine with docker-ce `28.0.4` (`5:28.0.4-1~ubuntu.24.04~noble`) and `/usr/bin/python3` 3.12.3 (`host.json`). The developer's Docker Desktop/WSL is explicitly not a substitute. The reachable fresh hosts are GitHub Actions `ubuntu-24.04` runners, which the existing workflows already use:

| Path | Trigger today | Covers |
|---|---|---|
| `.github/workflows/qualification-execution-boundary.yml` (`--test-only`, 2 hosts) | `pull_request`, `workflow_dispatch` | fresh provision → boundary fixture → cleanup on the new record shape; A with the **default** client; exports `evidence/` wholesale incl. `boundary/environment.json` and `cleanup-*.json` |
| `.github/workflows/qualification-s2-supervision.yml` (`--s2`) | `pull_request`, `workflow_dispatch` | same cycle through the S2 fixture path |
| `--host-only` (runs all of `tests/integration/qualification_host`, i.e. B's real chown/chmod, mkdir-kill, legacy, umask and precondition cases plus the retained readiness tests) | **manual only** (README §"host readiness"); no workflow selects it since `1339604`; a retired job at `33d3ea1` is the template |
| nondefault protected Docker client (A) | nothing | needs a host whose `host.json` selects a protected copy of the client |

Everything above requires the branch to exist on `origin`. **Pushing is the first outward-facing action of this assignment and needs the coordinator's explicit GO** (no earlier assignment authorized a push, PR, merge or issue closure). `workflow_dispatch` on a pushed branch needs no PR (`gh workflow run <file> --ref <branch>`); opening a draft PR additionally triggers the two PR-path workflows and is a separate GO.

## Selected outcome

Four artifacts, each bound to commit `2ff3b5e` (or the recorded successor if a defect forces a change), returned for coordinator review:

1. **Host ownership/permission/interruption evidence (B):** a `--host-only` run on a fresh host with every case in `tests/integration/qualification_host/test_host.py` executed (not skipped), including `test_installed_tree_binding_drift_is_named_and_restorable`, `test_cleanup_after_kill_between_tree_mkdir_and_binding` (5 trees × umask 022/077), `test_cleanup_retains_drifted_tree_and_reservation_until_the_binding_is_restored`, `test_legacy_uid_only_records_retire_on_the_producer_owner_and_group`, `test_tree_creation_preconditions_use_real_umask_and_parent_mode`, the venv-alias, partial-retirement and replacement-reservation cases, and the invariant-manifest readiness nodes. Record the host's umask (`sudo sh -c umask`) and `stat -c '%U:%G %a' /var/lib/fp-qualification-tests`.
2. **Fresh provision → boundary → cleanup cycle:** `--test-only` on two hosts (existing workflow) with the manifest carrying `tree_bindings` and five-field tree records, boundary tests passing, and cleanup receipts `ok: true` whose `removed` tree items carry `uid`/`gid`/`mode`.
3. **A with a nondefault protected client:** one boundary host where `host.json` selects `/opt/fp/bin/docker` (a root-owned 0755 copy of `/usr/bin/docker` in root-owned 0755 directories), with the exported `evidence/boundary/environment.json` showing `checks.docker_client.observed == "/opt/fp/bin/docker"`, `checks.image.observed` with exactly the key `id`, and no `RepoDigests`/`RepoTags`/`digests` anywhere in the file.
4. **Return packet** as specified at the end.

## Steps

### C0 — checkpoint and authorization (no repo change)

- [ ] Open the worktree; confirm `git status` clean at `2ff3b5e` and `git log --oneline -3` shows `2ff3b5e`, `9680ed2`, `f2606b0`. If the worktree is gone, recreate a branch from `origin/main` and apply `handoff-a-tracked.patch` + `test_qualification_boundary_fixture.py` + the plan doc, then `handoff-b-tracked.patch`, from the durable copies; verify `git diff -- tools tests | sha256sum` of B equals `1a44804ceb9aee2ca48da260fdb1505994fd10dc83bad64e6f75499d1c414e45` before committing.
- [ ] `./fp.ps1 doctor`; rerun the B focused command once and confirm 235 passed / 2 skipped.
- [ ] Report to the coordinator: base SHAs, the workflow you will add (C1), and request GO for **(a)** pushing the branch and **(b)** dispatching the workflows; ask separately whether a draft PR is wanted for the PR-path runs. Do not push before the GO.

### C1 — evidence workflow (one new file, `workflow_dispatch` only)

Add `.github/workflows/qualification-host-evidence.yml`, derived from the retired job at `git show 33d3ea1:.github/workflows/qualification-execution-boundary.yml` and the export/cleanup steps of the current boundary workflow. It must not be `pull_request`-triggered and must not become a required check. Two jobs:

**`host-readiness`** (matrix `host: [1, 2]`): checkout → `sudo /bin/bash tools/qualification_verification/provision.sh --manifest-output "$RUNNER_TEMP/qualification-manifest"` → record `umask`/parent mode → doctor via the installed launcher → `qualification_boundary_verification.py --host-only --manifest "$manifest"` → the existing `if: always()` cleanup/export step (`cleanup.py`, `cp -a "$host_root/evidence/."`, `cleanup-*.json`) → upload artifact `qualification-host-evidence-<n>` (14 days).

**`boundary-nondefault-client`** (one host): before provisioning,

```bash
sudo install -d -m 0755 -o root -g root /opt/fp /opt/fp/bin
sudo install -m 0755 -o root -g root /usr/bin/docker /opt/fp/bin/docker
sed -i 's#"docker": "/usr/bin/docker"#"docker": "/opt/fp/bin/docker"#' tools/qualification_verification/host.json
git diff --stat   # the dirty state is recorded in the manifest's source snapshot; this is TEST_ONLY evidence, not a change to main
```

then provision → doctor → `--test-only` → cleanup/export → upload `qualification-boundary-nondefault-client`, plus an inspection step that fails the job unless the exported evidence satisfies outcome 3:

```bash
env="$RUNNER_TEMP/qualification-evidence/boundary/environment.json"
jq -e '.checks.docker_client.observed == "/opt/fp/bin/docker"' "$env"
jq -e '.checks.image.observed | keys == ["id"]' "$env"
! grep -Eq 'RepoDigests|RepoTags|"digests"' "$env"
jq -e '.ready == true and (.checks | keys | length) == 16' "$env"
```

Notes: a copied client still finds CLI plugins (buildx) through the normal plugin directories; if `docker build` fails only under the copy, retry with a root-owned symlink `/opt/fp/bin/docker -> /usr/bin/docker` (also a protected path) and report the difference — do not hide it. `validate_inputs` requires `host.json`'s package/version values to match the runner exactly as the existing workflow already does.

- [ ] Run `python -I scripts/fp.py python scripts/check_boundaries.py` and the pre-commit gates via a normal `git commit` of the workflow (local). Do not edit `scripts/gates.yml` or any required-check configuration.

### C2 — push and dispatch (after GO)

- [ ] `git push -u origin claude/qualification-issues-423-424-88fd15` (never `--force`; the branch has no upstream).
- [ ] `gh workflow run qualification-host-evidence.yml --ref claude/qualification-issues-423-424-88fd15`; `gh workflow run qualification-execution-boundary.yml --ref …`; `gh workflow run qualification-s2-supervision.yml --ref …`. Capture each run URL/ID (`gh run list --branch … --limit 10`).
- [ ] Wait for completion (`gh run watch <id>`); download every artifact (`gh run download <id> -D <dir>`). Preserve the downloads outside the worktree under `C:/Users/joshu/multi_firm_operations/tmp/handoff-423-424/c-linux-evidence-<date>/`.

### C3 — inspect and bind the evidence

For each run, record: run URL, commit SHA the run checked out (must equal the pushed head), job conclusions, and:

- `record.json` under `evidence/<uuid>/`: `status`, `exit_code`, `verification_exit_code`, `source_stable`, `test_summary` (collected/passed/failed/skipped — **skipped must be 0**; `require_tests` already rejects skips), `metadata.purpose`.
- JUnit: the full list of executed `tests/integration/qualification_host` node IDs on the host-only job; every case named in outcome 1 present and passed.
- `cleanup-*.json` receipts: `ok: true`, `already_retired` on the second call where applicable, tree items in `removed` carrying `uid`/`gid`/`mode`, and **no** `legacy_tree_bindings` key on freshly provisioned hosts.
- `boundary/environment.json` (boundary and nondefault-client jobs): the outcome-3 assertions; on the default-client job `checks.docker_client.observed == "/usr/bin/docker"`.
- `host-observations.json`: `host_config_sha256` equals `sha256sum` of the `host.json` the run used (on the nondefault-client job that is the edited file, so it differs from the branch's `host.json` by construction — say so).
- Anything a run rejects (a `tree … mismatch`, `inconsistent …`, `umask …` or `setgid …` failure on a fresh host) is a **defect finding**: preserve the artifact, do not rerun to green, return it.

### C4 — return

Append a dated `### Handoff C executor return — <date> UTC` section to the parent plan (append-only, verbatim handoff kept), with: worktree, pushed head SHA, workflow file SHA, run URLs and artifact names, the per-run table from C3, exact commands, and the outstanding list. Then return to the coordinator.

## Constraints

- Preserve `trusted_administrator_and_privileged_qexec/v1`; no shared/reused-host claims; the legacy mode limitation stays stated.
- No merge, no issue closure, no changes to required checks, no edits to `host.json` on the branch (the nondefault-client edit happens only inside the runner's checkout).
- No broad implementation and no large agent review. If a run exposes a defect: preserve evidence, describe the failing invariant and the smallest candidate fix, and return; the coordinator assigns the fix.
- A green hosted run is evidence only for what its JUnit and receipts show executed; do not infer coverage from a green badge.
- Report faithfully: failed or cancelled runs, skips, and any manual retry are part of the packet.

## Return packet

Checkout path and head SHA(s); workflow file path and SHA; run URLs with checked-out SHA and conclusions; artifact names and the local preservation directory; per-run `record.json` fields and test counts; executed node-ID list for the host-only job; environment.json assertions (default and nondefault client); receipt findings; host umask/parent mode; any defect findings with evidence paths; the updated parent-plan section; and the explicit statement of what remains open for #423 and #424.
