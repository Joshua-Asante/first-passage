---
name: s2-linux-run
description: Use for ANY task that needs Linux evidence from the qualification S2 supervision workflow (`qualification-s2-supervision.yml`) — dispatching a run on a branch, reading its artifact, deciding whether a failure is a defect or a re-roll, and sequencing the run against the Windows `fp.ps1` verification lines so the two clocks overlap. Triggers on "S2 run", "fifteen green", "--s2", "qualification_boundary_verification", "S2 workflow", "Linux evidence", "dispatch the workflow", "read the artifact", or any worker packet's Linux verification step. Encodes the 2026-09-19/20 lessons: serial Windows-then-Linux clocks wasted ~25 min per iteration; two 50-minute Windows sequences were voided by writing into the tree mid-record; three Linux runs were cancelled by mid-run pushes; same-SHA re-rolls chased a real race. Does not decide acceptance (coordinator), change the workflow, or touch allowances.
---

# S2 Linux run — dispatch, read, decide, overlap

The S2 workflow provisions one fresh `ubuntu-24.04` host, runs one boundary selection, enforces invariants + cleanup, and uploads the `qualification-s2-supervision` artifact. The default mode is **s3**, which runs the files named by `S3_CASES` in `scripts/qualification_boundary_verification.py` (record scope `S3_N1_CAPTURE`, the acceptance-grade set); `-f mode=s2` runs the subset named by `S2_CASES` (scope `S2_DIAGNOSTIC_SUPERVISION`). The required nodes are the registered nodes of `tests/ops/qualification/invariant_manifest.json` inside the selected files, recorded as `invariants.json`'s `required_nodeids`. **A green check mark is not evidence; the artifact is.** A run is ~25 min: ~6–8 min provisioning plus three cases that are ~300 s each by design (service downtime, deadline-before-bootstrap, two-descendants to the wall).

## 1. Order of operations (saves ~25 min per iteration)

1. Commit on frozen bytes, `git diff --stat` first, push the branch.
2. **Dispatch Linux FIRST**, then run the Windows lines while it executes:
   ```bash
   gh workflow run qualification-s2-supervision.yml --ref <branch>
   gh run list --workflow=qualification-s2-supervision.yml --event workflow_dispatch --commit <sha> --json databaseId,headSha,displayTitle,status,createdAt
   ```
   `<sha>` is the full head you pushed. Poll the list (every ~10 s) until a run created after your dispatch appears: its `createdAt` is later than your dispatch and its `displayTitle` names your mode (`[s3]` by default). Do not use a fixed `sleep`, and never take the newest run of a branch listing (`--limit 1`): the pull_request run on the same SHA is sometimes the newer one. Confirm the `headSha` is your pushed head. Record the run ID in your notes (scratchpad, **not the worktree**).
3. Windows (`./fp.ps1`, PowerShell 7.3+): line 1 (ten execution files, `--workers 2`, zero skips) during iteration; lines 2–3 and `check` only on the final frozen tree. **Nothing may be written into the worktree until the last record closes** — the recorder hashes the tree and voids the record otherwise. Drafts (§7, ledger text) go to the scratchpad.
4. Do not push again to a branch with a run in flight: the per-ref `cancel-in-progress` concurrency kills it. On a PR branch every push refires the workflow (the path filter applies to the PR's whole change set), so batch docs commits until the run you need has finished.
5. Never dispatch the same SHA twice. If a second dispatch happens by accident the first is cancelled; cite the survivor.

Steps 4–5 are enforced by `scripts/guard_s2_runs.py` (Claude PreToolUse hooks for Bash and the GitHub MCP write tools, plus git pre-push): a push while an open PR's run is in flight is refused, and so is a dispatch or rerun that would cancel a live run in the same concurrency group, or re-roll a definitive one. Redundancy compares exact bytes and exact mode: the newest definitive same-mode `workflow_dispatch` run on the dispatched SHA decides, and `[s2]`/`[s3]` are incomparable — an s3 run installs the v5 dispatch profile while an s2 run installs the v4 funded one, so neither's result covers the other's. PR runs tested the merge ref, never the head's bytes; `cases` is accepted in `s3` only. Without `--ref` the guard checks the default branch, as `gh` does. Override only with a reason you can state: `FP_S2_GUARD=off`.

## 2. Reading the artifact (the only acceptance-grade read)

```bash
python scripts/s2_run_evidence.py <id> --expect-head <sha>
python scripts/s2_run_evidence.py <id> --expect-head <sha> --expect-scope S2_DIAGNOSTIC_SUPERVISION
```
The reader downloads the artifact outside the repository, prints the facts below and exits 0 only when every one holds. `--expect-scope` names the one record scope that reads ok: `S3_N1_CAPTURE` (the default, an s3 run) or `S2_DIAGNOSTIC_SUPERVISION` (an s2-mode run, only when asked for); `DIAGNOSTIC_SUBSET` and `N1_ONLY_TEST_ONLY` never read ok. `--expect-head` takes 7–40 hex characters in any case, compared as a prefix of `headSha`, and anything else is refused before any gh call. `facts.tested_commit` is the record's `before.commit`, the commit the host measured (missing = not ok). `facts.tested_commit_kind` is `head` for a `workflow_dispatch` run, whose tested commit must equal `headSha`, or `pull_request_merge` for a pull_request run, which tested `refs/pull/N/merge`: the merge commit is printed, and it is never the head's bytes alone.
The same facts by hand:
```bash
gh run view <id> --json headSha,event,conclusion,createdAt
gh run download <id> -n qualification-s2-supervision -D <scratchpad>/s2-<id>
```
Required facts, all from files under `<scratchpad>/s2-<id>/<record-id>/`:
- `record.json`: `status=completed`, `exit_code=0`, `verification_exit_code=0`, `source_stable=true`, `capture_complete=true`, `cleanup.ok=true`, `metadata.acceptance_scope` the expected scope, and `before.commit` equal to the run's `headSha` for a dispatch run.
- `invariants.json`: `passed=true`, and `required_nodeids` (the selection's required nodes: currently 15 for s2 and 19 for s3) is non-empty.
- `junit.xml`: `tests` at least the number of `required_nodeids`; failures / errors / skipped — **skipped must be 0**.
Report: run ID, head SHA, record ID, counts, cleanup. A run whose head is not your final bytes proves nothing about them.

Quick failure summary without downloading:
```bash
gh run view <id> --log-failed | grep -E "(FAILED|passed|failed in|AssertionError|ValueError:)" | sed -E 's/^[^\t]*\t[^\t]*\t//' | sed -E 's/^[0-9T:.-]+Z //' | sort -u
```

## 3. Deciding: defect or re-roll

A failure on unchanged code is a **finding, not flakiness**. Before any second dispatch:
1. Identify the failing work's attempt: `boundary/linux-<attempt>-budget.json` and the case's own facts file.
2. Pull its chain from `boundary/journal.sqlite` (tables `full_campaign_budgets`, `full_campaign_objects` roles `supervision_event_*`) — transitions, PROCESS/RESUMED/PAYLOAD_EXIT events, observation, recoveries, dispatches — and line it up against `journal.log` (systemd unit start/stop, containerd shim connect/disconnect), `kernel.log` (OOM), `systemd-units.log`.
3. Compare timing against the last green run's same case (shim-connect → first PROCESS → RESUMED). Host speed differences are how the 2026-09-20 pre-exec resume race surfaced (59–77 ms vs 88–122 ms).
4. State the root cause in one sentence with file:line, fix it, then dispatch once. If the evidence says test-only (an over-narrow predicate, a race-tolerant assertion), say so and fix the test — never relax a load-bearing assertion (`charge >= limits.cpu_ns`, zero skips, all nodes required).
Known-benign classes so far: `warm_service` `Slice==''` (unit GC within the same second — read unit facts before waiting for COMPLETED); the OOM/overrun cases legitimately end IN_DOUBT (guardian stop) or BUDGET_* (settle/timer) — both are accepted terminal sets.

## 4. Who may claim what

- Worker packets: report the run as evidence; "Linux acceptance pending" if no green run on the final bytes.
- Coordinator: acceptance needs the integrated PR run on the final head, artifact-read, plus independent review — never a branch run alone.
- Windows/mock/`simulated_control_timer` results are never Linux evidence.

## 5. Diagnostic subset runs, and faster loops still open
Iterating on one failing case: `gh workflow run qualification-s2-supervision.yml --ref <branch> -f mode=s3 -f cases='<pytest -k expr>'` (`cases` is accepted in `s3` mode only). The run is titled `S2 DIAGNOSTIC (…)`, its record is `acceptance_scope=DIAGNOSTIC_SUBSET`, and `s2_run_evidence.py` refuses it (`ok: false`) whatever its outcome — read the printed `junit` totals for the selected cases. It runs in its own concurrency group, so it does not cancel a full run on the same ref. Acceptance still needs a full run on the final head.
A diagnostic run always ends red (exit 2), even when every selected case passed, and two diagnostics on one ref cancel each other (they share the one diagnostic concurrency group).
Still open (S3-era tooling, not for a worker to improvise): shard the suite across two fresh hosts (OOM case last on its shard); cache the provisioned venv/worker image; move Windows line 3 to a hosted runner once the source-bound recorder runs there.
