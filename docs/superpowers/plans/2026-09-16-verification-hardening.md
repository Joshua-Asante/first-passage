# Verification hardening implementation plan

> **For agentic workers:** Execute with superpowers:executing-plans. Preserve the behavioral contract and integration owner. This task owns integration; independent review follows implementation.

**Goal:** Complete the four approved pre-PR improvements: scoped branch, durable run lifecycle, validated pytest evidence, and owned Docker cancellation cleanup.

**Architecture:** A standard-library RunRecord owns reservation, atomic state updates, source snapshots, command capture and acceptance. The launcher and a Python Docker runner use that owner before setup. PowerShell remains a thin argument-preserving entry point.

**Tech Stack:** Python 3.11+, PowerShell 7.3+, installed Git, Docker, pytest and pytest-xdist. No new dependencies.

**Spec:** User-approved items 1–4 in this task. Fast-mode changes (item 5) are excluded.

## Global constraints

- No production trading changes, push, merge or deployment.
- Preserve historical records and branch `codex/event-sequence-evidence-before-hardening`.
- Prepared PR base: `codex/phase2-four-leg-execution`, refreshed at `dfa4394498b6ddb6526197d9e86e51110cd58e6d`. Launcher code is inherited from open PR412; reconcile/drop its duplicate patch when that dependency lands before targeting main.
- Never accept missing/malformed expected reports, incomplete capture, failed cleanup or changed source as success.
- A hard kill leaves the last atomic `running` record, never a completed claim. An unwritable evidence directory cannot itself persist a record and must fail visibly.

## Work and acceptance

- [x] Refresh remotes and PR metadata; preserve old revision; rebase the three tooling commits onto current PR409. Confirm only tooling/launcher files differ against the stacked base.
- [x] Add regressions before changes: invalid launcher environment produces `not_started`; a live child exposes `running`; successful custom JUnit is retained; missing/malformed/inconsistent JUnit rejects success; child failure remains failure; interruption finalizes `interrupted`; Docker cleanup removes only its owned container.
- [x] Implement `RunRecord` in `scripts/record_verification.py`, with atomic replace and explicit `not_started/running/failed/interrupted/completed` status. `begin()` captures source; `execute(command, reports=...)` owns child capture; context finalization owns acceptance. Reserve the output before environment/image checks.
- [x] Route `scripts/fp.py` through this owner. Preserve user JUnit destinations, also copy fresh report bytes into the evidence bundle; summarize testcase outcomes and check declared counts. Reject stale report reuse.
- [x] Move Docker orchestration from `tools/local_verification/run.ps1` into `scripts/docker_verification.py`. The wrapper forwards arguments only. The runner labels containers with a unique run identity, retains CID, and verifies absence of owned containers after removal on success/failure/interruption. Never remove by image or broad name matching.
- [x] Exercise real launcher processes and Docker container interruption, with fake-boundary tests for unavailable daemon/cleanup errors. Re-run selected Linux sequences against the refreshed production base. Run full gates and request independent review.
- [x] Update agent/user docs and record exact verified source plus PR-base/dependency disposition. Keep results local.

## Related-case map

| Shared boundary | Required cases |
| --- | --- |
| Before child starts | Invalid venv, missing Docker, failed image check, initial snapshot failure: reserved record stays not_started with error and nonzero result |
| Child lifetime | Visible running state, child failure, Ctrl-C, retained pipe, write failure, hard termination: no false completed state |
| Pytest report | Default/custom path, nested suites, missing/malformed XML, wrong counts, stale file, failures/skips: retained bytes and validated totals |
| Docker ownership | Create/attach interruption, missing CID, cleanup failure, already-removed container, unrelated container: bounded exact-owner cleanup and recorded outcome |

Acceptance requires all applicable rows to have executable evidence; generic commands and gates do not acquire an invented JUnit requirement.

## Verified outcome

Windows tooling: 63 passed, 2 Docker integration opt-in skips. The separate local
Docker interruption/recorder run passed 20 tests, including both real-container
cases. Full repository gates passed (existing absent-private-input warnings remain).
Linux/Python 3.11 sequence run: 183 passed, 3 absent-private-runtime-input skips,
100 passing generated cases; cleanup confirmed. Independent code review accepted.
OS console signal generation itself was not tested: KeyboardInterrupt was injected
at the wait for a confirmed live attached Docker CLI and at creation response loss.

The rebase exposed CRLF conversion of requirements-extra.txt. Its LF bytes were
restored to the cached-image hash, and .gitattributes now pins both dependency
files to LF. No image rebuild/pull, new package install or paid Docker service was
used. Preflight refusal is retained as not_started evidence, not erased.

Primary records (relative to this worktree):
- Windows: .cache/fp-verification/20260916T215149Z-a554818a7bf7/record.json
- Gates: .cache/fp-verification/20260916T215200Z-dd29603fb519/record.json
- Real interruption: .cache/fp-verification/20260916T214817Z-9880a1362633/record.json
- Linux sequences: .cache/fp-docker-verification/20260916T215513Z-3afacf1dad1f/record.json

The plan completion note and line-ending pins were added after some recorded runs;
relevant executable source/test hashes are unchanged. These records do not claim
private-input acceptance or acceptance of future changes to PR409. Review the
stack against PR409, then reconcile PR412 and retarget/rebase after dependencies
land; do not merge this tooling into the active repair branch as a shortcut.