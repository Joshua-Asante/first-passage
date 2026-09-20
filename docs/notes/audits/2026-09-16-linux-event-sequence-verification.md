# Linux environment and revision-bound event-sequence verification

## Result

Docker Desktop 4.91.0 / Docker Engine 29.8.0 is operational with its Linux engine.
The verified container uses Python 3.11.16 and matches all 62 operations-lock
package versions. `pip check` passed. On the final tested PR 409 revision:

- **161 passed, 3 skipped, 0 failures, 0 errors** (48.69 seconds).
- **100 passing generated Hypothesis cases**, across seven parametrized test
  entries. These examples are included in the pytest result, not 100 additional
  pytest tests.
- Source fingerprints were identical before and after execution.
- All retained output hashes were independently recomputed and matched.
- Independent code review accepted the tooling and the added protection-test
  oracle. The reviewer did not rerun Docker tests; execution evidence comes from
  this task's recorded commands.

## Exact scope and evidence

- PR revision: `d14d74f9b11c3046439b4879c1b81686de330c5f`, still the published head
  when checked after the run.
- Source fingerprint, including the uncommitted verification additions:
  `ec86800b70286a80eb16534dbdfaf6df91ff06c4db283c4714933d012335ef59`.
- Operations lock SHA-256:
  `cedbcfb14f91edf73f98872734341445d41e8bb01662c130e16c40d179267fc7`.
- Docker image ID:
  `sha256:f9659aa4a17698a17d1ac1952fd214bf9510d96bc82b57575de230b91ad855c7`.
- Worktree: `C:/Users/joshu/multi_firm_operations/.worktrees/event-sequence-evidence`.
- [Machine-readable record](../../../tmp/event-sequence-evidence/linux-current-004/record.json),
  [raw output](../../../tmp/event-sequence-evidence/linux-current-004/stdout.txt),
  [JUnit](../../../tmp/event-sequence-evidence/linux-current-004/junit.xml), and
  [branch coverage](../../../tmp/event-sequence-evidence/linux-current-004/coverage.json).

The record retains exact command arguments, start/end times, commit and dirty
diff hashes, individual tracked/nonignored-untracked file hashes, Python package
versions, image identity, exit status, skips and artifact hashes. It is historical
evidence for those bytes, not an automatically refreshed claim about later heads.

## What the sequences exercise

The tests call production account-owner/runtime code and existing offline broker
fixtures. They vary delayed polls and snapshot replays around cancellation,
late entry fills, partial close fills, terminal close outcomes, and restart at
different send/effect boundaries. They also exercise ordinary exit, direct flat
and scheduled-flat entry points, plus stale protection replay before a fresh
residual read can release close feedback. No risk policy or production code was
changed. All synthetic broker activity stays local and offline.

Existing selected suites cover takeover phases, account ownership, four-leg
runtime, close reconciliation/review edges, runtime chronology, and close feedback.
Three recorder tests also passed: child failure is retained, source drift defeats
a successful exit, and evidence inside the measured tree is rejected. The recorder
tests were first observed failing before implementation and also pass on Windows.

## Environment repairs and reusable command

The installed Docker CLI lives under the user's `AppData/Local/Programs/DockerDesktop`
directory. The current Codex process had an old PATH, causing both CLI discovery
and credential-helper lookup problems. The wrapper locates that installation and
temporarily exposes the helper directory, restoring PATH afterward. No global
PATH or Docker security settings were changed.

Tests use Linux `/tmp` for temporary databases, avoiding the inaccessible shared
Windows pytest directory and Windows filesystem-lock behavior. Host source is
read-only and container networking is disabled. The build context contains only
three dependency/build files; no repository source, private data or credentials
is sent to the builder. Test containers exit with `--rm`; none remained running.

From the verification worktree:

```powershell
.\tools\local_verification\run.ps1 -EvidencePath C:\Users\joshu\multi_firm_operations\tmp\event-sequence-evidence\next-run
```

Use a new output path each time. Add `-Build` to rebuild. The wrapper refuses a
cached image whose dependency files differ from this checkout. Details are in
`tools/local_verification/README.md` in that worktree. Tooling and tests remain
local and uncommitted; no PR 409 worktree edits, push, merge or deployment occurred.

## Limits and retained failed attempts

The three skips need accepted private runtime inputs absent from this isolated
checkout. They were not replaced with synthetic evidence or counted as passes.
The image is Debian/Python 3.11, not an exact copy of GitHub's Ubuntu runner.
The base image is digest-pinned and Python packages are locked/version-pinned;
Debian package resolution is not fully locked. The actual built image ID is
recorded. The root Windows `.venv` and default Python installation were not repaired
or replaced; the validated operations environment and Docker path are available.

Targeted branch coverage is diagnostic, not a full-suite acceptance claim:

| Module | Branches covered | Missing |
| --- | ---: | ---: |
| book_account_owner | 355 / 536 | 181 |
| book_takeover_owner | 169 / 198 | 29 |
| book_runtime | 116 / 168 | 52 |

The generated tests cover bounded synthetic sequences, not every possible order
or malformed snapshot. Ignored inputs are outside the recorder's source hash;
before/after hashes cannot detect a transient host edit that is reverted during
the run. This task used an isolated checkout without concurrent writers.

Earlier evidence remains under `tmp/event-sequence-evidence`: `linux-baseline`
records an exit-125 launch failure caused by an unquoted PowerShell comma;
`linux-sequences-002` records two test-driver failures that wrongly assumed normal
closes initiate cancellation themselves. Reading the production contract corrected
that oracle: normal closes refuse pending entry remainders, callers issue cancel,
and a new occurrence retries after terminal evidence. `linux-sequences-003` passed
116 tests with three skips on the older `5b948ca` revision. None of those results
was relabeled as evidence for the final revision.
