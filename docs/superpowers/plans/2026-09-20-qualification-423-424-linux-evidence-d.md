# Qualification #423/#424 — Handoff D: unblock and produce outcomes 1 and 3 (option 4)

> **For agentic workers:** Execute with superpowers:executing-plans. This amends [Handoff C](2026-09-20-qualification-423-424-linux-evidence.md); everything in C's constraints, inspection recipe and return-packet shape still applies. The only new work is one trigger edit on the evidence branch, the runs it makes possible, and their inspection. Do not extend the implementation; if a run exposes a defect, preserve it and return.

**Goal:** Produce Handoff C's outcomes 1 (`--host-only` ownership/permission/interruption evidence for #424) and 3 (nondefault protected Docker client for #423), which C could not dispatch because GitHub had never registered the `workflow_dispatch`-only file.

**Coordinator decision recorded:** option 4 — register the workflow by letting it run once from a `push` trigger scoped to this branch only. Not chosen: merging a workflow-only PR to `main` (a merge the coordinator would own, landing ahead of A/B); a `pull_request` trigger (contradicts the delivered design); recording the outcomes as not produced.

## Source basis

- Branch `claude/qualification-issues-423-424-88fd15` on `origin`, head `3b05e88` (docs only) over `6cd9ca6` (workflow added; tools/tests/scripts byte-identical to `2ff3b5e`) over `2ff3b5e` (B, accepted locally) over `9680ed2` (A) over `f2606b0` = `origin/main` at drafting. Draft PR #437 is open against `main`; leave it open and draft.
- Worktree `C:/Users/joshu/multi_firm_operations/.claude/worktrees/review-leftover-worktrees-d12e00` is clean at `3b05e88`.
- `.github/workflows/qualification-host-evidence.yml` (blob sha256 `944995c837e48edae4c92cd0d832322701fd6a0922562f315f42177ca5fce28c`) already contains both jobs D needs: `host-readiness` (matrix 1–2; provision → umask/parent facts → doctor → `--host-only` → cleanup/export → artifact `qualification-host-evidence-<n>`) and `boundary-nondefault-client` (installs `/opt/fp/bin/docker`, edits the runner checkout's `host.json`, provision → `--test-only` → cleanup/export → `jq` shape assertions → artifact `qualification-boundary-nondefault-client`). Its trigger block is exactly `on:` / `workflow_dispatch:` (lines 9–10).
- Verified (C return, parent plan §"Blocker"): `gh workflow run` and `POST /actions/workflows/<file>/dispatches` both 404 for this file on this ref. Precomputed expected `host_config_sha256` of the runner-edited `host.json`: `d2f1d6bddf08a3813754469af2a29325c09997c00f64b256c1bdeca053d4597c`; branch `host.json` is `ddc5a391480fd322…`.
- Already produced by C and not to be rerun: outcome 2 on four boundary hosts and two S2 hosts (runs 35489412733, 35489451474, 35489451486); the S2 dispatch failure 35489413703 stays preserved and attributed to the pre-existing S2/systemd domain — do not touch it here.

## Selected outcome

Outcomes 1 and 3 of Handoff C produced from this branch, bound to the commit that carries the trigger edit, inspected per C3, with the branch left in a state where the `push` trigger is removed again and the workflow remains dispatchable.

## Steps

### D0 — checkpoint (no repo change)

- [ ] `git fetch origin`; confirm `origin/main` is still `f2606b0` (else report before proceeding) and the worktree is clean at `3b05e88`. `./fp.ps1 doctor`.
- [ ] Report to the coordinator that you are about to push the trigger edit (this push is authorized by the option-4 decision; it stays on the evidence branch). No other authorization is needed unless a step below says so.

### D1 — scoped push trigger (one edit, one commit, one push)

- [ ] Edit only the trigger block of `.github/workflows/qualification-host-evidence.yml`:

```yaml
on:
  workflow_dispatch:
  # Handoff D, temporary: a workflow_dispatch-only file that has never been on
  # main has no workflow ID (dispatch 404s). One push-triggered run on this
  # evidence branch registers it; the trigger is removed again in D4.
  push:
    branches:
      - claude/qualification-issues-423-424-88fd15
```

  Nothing else in the file changes; keep the header comment's "never a required check" statement true (no `pull_request`, no `scripts/gates.yml` or ruleset change).
- [ ] `git commit` normally (pre-commit gates run; no `--no-verify`), message `ci(evidence): temporary branch-scoped push trigger to register the manual host-evidence workflow (Handoff D)`, with the standard co-author trailer. Record the commit SHA `<D1>`.
- [ ] `git push origin claude/qualification-issues-423-424-88fd15` (never force). The push itself starts the three jobs; capture the run with `gh run list --branch … --workflow qualification-host-evidence.yml --limit 3`. PR #437's PR-path workflows will also rerun on this push; that is expected and their results are a bonus re-confirmation of outcome 2, not a required part of D.

### D2 — registration check and dispatch (evidence of the mechanism)

- [ ] After the push-triggered run starts, confirm registration: `gh workflow list --all` shows `Qualification host evidence (manual)` with an ID, and `gh workflow run qualification-host-evidence.yml --ref claude/qualification-issues-423-424-88fd15` now returns 2xx (this dispatched run is the second evidence run; both count). If dispatch still 404s after the push run completed, stop and return that fact — option (1) becomes the coordinator's call; do not add a `pull_request` trigger.
- [ ] `gh run watch` both runs to completion; `gh run download <id> -D C:/Users/joshu/multi_firm_operations/tmp/handoff-423-424/d-linux-evidence-<date>/<label>-<id>/` for each. Preserve everything outside the worktree, including failed jobs.

### D3 — inspect and bind (C3 applies; these are the D-specific checks)

Per run and per host, record run URL, checked-out SHA (must equal `<D1>`), job conclusions, and:

- **host-readiness (outcome 1):** `record.json` under `evidence/<uuid>/` completed, exit 0, `source_stable`, `metadata.purpose == host_readiness`, `test_summary.skipped == 0`; JUnit node-ID list (save as `_nodeids.txt`) contains every case named in C outcome 1 — `test_installed_tree_binding_drift_is_named_and_restorable` (owner, group, mode, setgid), `test_cleanup_after_kill_between_tree_mkdir_and_binding` for all five trees × both umasks (pytest renders the integer umask ids as `18` and `63`), `test_cleanup_retains_drifted_tree_and_reservation_until_the_binding_is_restored` (data/code × group, mode, setgid, owner), `test_legacy_uid_only_records_retire_on_the_producer_owner_and_group` (mode, group), `test_tree_creation_preconditions_use_real_umask_and_parent_mode`, the venv-alias, interrupted-retirement/replacement and process-cleanup-failure cases — each passed; the facts step output (umask, `/var/lib/fp-qualification-tests` owner/mode) copied verbatim; cleanup receipts `ok: true`, five five-field tree records, no `legacy_tree_bindings`; `already_retired` on the second call.
- **boundary-nondefault-client (outcome 3):** the workflow's own `jq` assertion step succeeded; independently re-assert on the downloaded `boundary/environment.json`: `checks.docker_client.observed == "/opt/fp/bin/docker"`, `checks.image.observed` keys exactly `["id"]`, no `RepoDigests`/`RepoTags`/`digests`, `ready: true`, 16 checks; `host-observations.json.host_config_sha256 == d2f1d6bddf08a3813754469af2a29325c09997c00f64b256c1bdeca053d4597c` (the edited config, differing from the branch's `ddc5a391…` by construction); `record.json` completed/exit 0/464 collected with 0 skipped as on C's default-client hosts; the invariant gate passed; cleanup receipt `ok: true`. Note whether `docker build` ran under the copied client without fallback; if the symlink fallback was used, the observed path must still be the configured one — report which.
- Any `tree … mismatch`, `inconsistent …`, `umask …`, `setgid …` or `docker_client` failure on a fresh host is a **defect finding**: keep the artifact, do not rerun to green, return it with the failing invariant and the smallest candidate fix.

### D4 — remove the temporary trigger

- [ ] Revert the D1 trigger edit on the branch (restore `on:` / `workflow_dispatch:` exactly; the file's blob sha256 must return to `944995c8…fce28c` — verify with `git show HEAD:.github/workflows/qualification-host-evidence.yml | sha256sum`). Commit `ci(evidence): drop the temporary push trigger; workflow now registered (Handoff D)`, push. Confirm afterwards that `gh workflow run qualification-host-evidence.yml --ref …` still returns 2xx (registration survives; cancel that extra run with `gh run cancel` if you do not want a third evidence run, and say so).
- [ ] Do not squash, rebase or force-push: the evidence must remain bound to `<D1>` as a reachable commit.

### D5 — return

Append `### Handoff D executor return — <date> UTC` to the parent plan [2026-09-19-qualification-issues-423-424.md](2026-09-19-qualification-issues-423-424.md) (append-only), commit with `[skip ci]` in the subject like C did, push, and return with: `<D1>` and the D4 SHAs; run URLs and checked-out SHAs; artifact names and the preservation directory; the D3 tables; the facts-step output; the registration evidence (the 404 before, the 2xx after); the workflow blob sha256 at the final head; defect findings if any; and the explicit statement of what remains open for #423 and #424.

## Constraints

- Only the trigger block changes, twice (add, then remove). No edits to `host.json`, `scripts/gates.yml`, required checks, `tools/`, `tests/` or `scripts/`.
- Draft PR #437 stays open and draft; no merge, no issue closure, no comments on the issues.
- The legacy-v3 limitation (owner and group validated, mode not) is unchanged and is restated in the return; a green host-only run does not extend it.
- Report faithfully: cancelled, failed or retried runs and any fallback taken are part of the packet.

## Return packet

As in Handoff C, plus: both trigger-edit SHAs, the before/after registration evidence, and confirmation that the final head's workflow blob equals `944995c8…fce28c`.
