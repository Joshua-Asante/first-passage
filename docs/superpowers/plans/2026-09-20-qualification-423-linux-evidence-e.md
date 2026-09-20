# Qualification #423 — Handoff E: nondefault protected Docker client evidence (path relocation)

> **For agentic workers:** Execute with superpowers:executing-plans. This is the fix assignment returned by Handoff D: relocate the evidence workflow's nondefault client to a protected-path-clean location, dispatch the already-registered workflow once, inspect outcome 3, return. Handoff C's constraints, inspection recipe and return-packet shape still apply. Nothing under `tools/`, `tests/`, `scripts/` or `host.json` changes; if the run exposes anything else, preserve it and return.

**Goal:** Produce Handoff C outcome 3 — the exported `environment.json` of a fresh boundary host whose retained `host_config` selects a **nondefault, protected** Docker client — so #423's remaining half has real-Linux evidence.

**Coordinator decision recorded:** relocate to `/var/lib/fp-docker/bin/docker`. Rationale: `/var/lib` is a standard root-0755 directory and already hosts the project's own protected parent `/var/lib/fp-qualification-tests` (observed `root:root 755` on every D host); `/opt` is `chmod -R 777` on the `ubuntu-24.04` runner image (`actions/runner-images`, `configure-system.sh`), so `protected()` rightly refused it. Alternative if the coordinator prefers: `/usr/local/fp/bin/docker` (the image widens only `/usr/local/bin`); expected digest below.

## Source basis

- Branch `claude/qualification-issues-423-424-88fd15` on `origin`, head `e6180f5` (D return, docs only) over `34f5f7a` (trigger revert) over `f573fb6` (trigger add) over `3b05e88`/`6cd9ca6`/`2ff3b5e`/`9680ed2`/`f2606b0` (= `origin/main` at drafting; recheck). Draft PR #437 open; leave it open and draft.
- `.github/workflows/qualification-host-evidence.yml` at `e6180f5`: blob `944995c837e48edae4c92cd0d832322701fd6a0922562f315f42177ca5fce28c`, `on: workflow_dispatch` only, **registered** (workflow ID `362470213`, active) — `gh workflow run qualification-host-evidence.yml --ref <branch>` returned 2xx after D4. No trigger changes are needed or allowed.
- D evidence: `host-readiness` succeeded on four hosts (runs 35491877585, 35491914564; outcome 1 complete); `boundary-nondefault-client` failed identically in both, 0.08 s into `Provision protected TEST_ONLY host`, with `Host setup/cleanup failed: ValueError: unprotected path` after the install/sed step had succeeded (root:root 0755 copies, 1 file changed). No artifacts (pre-manifest); the step logs are the evidence.
- The three lines to change (current file): 88 `sudo install -d … /opt/fp /opt/fp/bin`, 89 `sudo install … /opt/fp/bin/docker`, 90 `sed -i 's#"docker": "/usr/bin/docker"#"docker": "/opt/fp/bin/docker"#'`, and the assertion at 132 `jq -e '.checks.docker_client.observed == "/opt/fp/bin/docker"'`.
- Precomputed expected `host_config_sha256` of the runner-edited `host.json` (branch `host.json` = `ddc5a391480fd322…`):
  `/var/lib/fp-docker/bin/docker` → `6ca065a50131426862c2df0cd32c995fd732c115852972423978d1bddd63e47e`;
  `/usr/local/fp/bin/docker` → `6bd5cca9287e04dc4f71c796451af85678a48cb92c2e4028f2113827871d3353`.

## Selected outcome

One green `boundary-nondefault-client` job whose exported `boundary/environment.json` shows `checks.docker_client.observed == "/var/lib/fp-docker/bin/docker"`, `checks.image.observed` with exactly the key `id`, no `RepoDigests`/`RepoTags`/`digests`, `ready: true`, 16 checks; `host-observations.json.host_config_sha256 == 6ca065a5…e47e`; the boundary suite and invariant gate passed; cleanup receipt `ok: true`. The `host-readiness` jobs in the same run are a bonus re-confirmation of outcome 1, not required.

## Steps

### E0 — checkpoint (no repo change)

- [ ] `git fetch origin`; confirm `origin/main` is still `f2606b0` (else report first) and the worktree is clean at `e6180f5`. `./fp.ps1 doctor`.
- [ ] Brief report to the coordinator: the exact diff you will push (E1). The push is authorized by this assignment; it stays on the evidence branch.

### E1 — relocate the client (one edit, one commit, one push)

- [ ] In `.github/workflows/qualification-host-evidence.yml`, change only the `boundary-nondefault-client` job:

```bash
sudo install -d -m 0755 -o root -g root /var/lib/fp-docker /var/lib/fp-docker/bin
sudo install -m 0755 -o root -g root /usr/bin/docker /var/lib/fp-docker/bin/docker
sed -i 's#"docker": "/usr/bin/docker"#"docker": "/var/lib/fp-docker/bin/docker"#' \
  tools/qualification_verification/host.json
# make the ancestry self-evidencing in the log (D had to argue it from the image scripts)
for d in / /var /var/lib /var/lib/fp-docker /var/lib/fp-docker/bin /var/lib/fp-docker/bin/docker; do
  sudo stat -c '%U:%G %a %n' "$d"
done
sha256sum tools/qualification_verification/host.json   # expect 6ca065a5…e47e
```

  and the assertion step to `jq -e '.checks.docker_client.observed == "/var/lib/fp-docker/bin/docker"' "$env"`. Update the job's comment/description if it names `/opt`. Nothing else in the file changes; no trigger change.
- [ ] `git commit` normally (gates run; no `--no-verify`): `ci(evidence): nondefault Docker client under /var/lib (runner image leaves /opt world-writable) (Handoff E)` with the standard co-author trailer. Record `<E1>`. `git push origin claude/qualification-issues-423-424-88fd15` (never force). The push reruns #437's PR-path workflows (bonus; not required).

### E2 — dispatch and preserve

- [ ] `gh workflow run qualification-host-evidence.yml --ref claude/qualification-issues-423-424-88fd15`; capture the run ID (`gh run list --workflow qualification-host-evidence.yml --limit 3`); confirm it checked out `<E1>`.
- [ ] `gh run watch <id>`; `gh run download <id> -D C:/Users/joshu/multi_firm_operations/tmp/handoff-423-424/e-linux-evidence-<date>/run-<id>/`; also save `gh run view <id> --log` for the nondefault job (the ancestry `stat` lines and the `sha256sum` line are part of the evidence). Preserve failures too.

### E3 — inspect and bind (outcome 3)

- [ ] `record.json` under `evidence/<uuid>/`: completed, exit 0, `verification_exit_code` 0, `source_stable`, `metadata.purpose == boundary_acceptance`, collected/passed as on C's default-client hosts (464 / 0 skipped), invariants passed.
- [ ] `boundary/environment.json`: the five assertions in "Selected outcome" (re-assert on the download, independently of the workflow's `jq` step). Also record `checks.docker.observed.Version` (must be `28.0.4`) to show the copied client reached the daemon.
- [ ] `host-observations.json`: `host_config_sha256 == 6ca065a5…e47e` (differs from the branch's `ddc5a391…` by construction; say so). `source_commit == <E1>`.
- [ ] Cleanup receipts: `ok: true`, five five-field tree records, second call `already_retired`, no `legacy_tree_bindings`.
- [ ] Log evidence: every ancestor `stat` line shows `root:root` and a mode without group/other write bits (`755`/`700`); note whether `docker build` ran under the copy without any fallback (there must be none — the workflow has no symlink fallback).
- [ ] Any `unprotected path`, `docker_client`, `tree … mismatch` or `inconsistent …` failure on the fresh host is a **defect finding**: preserve, do not rerun to green, return it with the failing invariant and the smallest candidate fix.

### E4 — return

Append `### Handoff E executor return — <date> UTC` to the parent plan [2026-09-19-qualification-issues-423-424.md](2026-09-19-qualification-issues-423-424.md) (append-only; `[skip ci]` subject), push, and return with: `<E1>` and the final head; the run URL, checked-out SHA and per-job conclusions; artifact name and preservation directory; the E3 table; the ancestry `stat` lines verbatim; the workflow blob sha256 at the final head; defect findings if any; and the explicit statement of what remains open for #423 (expected: nothing evidence-wise) and #424 (nothing; acceptance is the coordinator's), restating the legacy-v3 limitation (owner and group validated, mode not).

## Constraints

- Only the nondefault-client job's install/sed/assertion lines and its comment change. No trigger, gate, ruleset, `host.json`, `tools/`, `tests/` or `scripts/` edits.
- PR #437 stays open and draft; no merge, no issue closure, no issue comments.
- No rebase, squash or force-push; the evidence must stay bound to a reachable commit.
- Report faithfully: cancelled, failed or retried runs are part of the packet; a green badge is evidence only for what the JUnit, receipts and logs show executed.
