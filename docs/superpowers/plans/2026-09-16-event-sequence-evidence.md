# Local Linux verification and event-sequence evidence

> Execute inline using executing-plans and test-driven-development. Preserve the active PR repair worktree.

Goal: run bounded execution-lifecycle tests on an isolated PR 409 revision in Linux/Python 3.11, retaining evidence that identifies exactly which bytes were tested.

Base: `5b948ca4419d5367862bc4e5d37c8ea222f6105c`. The separate repair task has uncommitted changes; this work does not assert their acceptance or modify them.

The repair task subsequently published `d14d74f9b11c3046439b4879c1b81686de330c5f`.
The isolated branch was fast-forwarded to that revision for current-head testing.
The earlier passing record remains limited to its original base. Final evidence
is retained outside this worktree under `tmp/event-sequence-evidence` in the main checkout.

- [ ] Build a local-only image from the official Python 3.11 digest and `requirements-ops.lock`, with explicitly pinned Hypothesis, coverage and signing supplements. Send only dependency files into the build context. No application services, credentials, broker connections, or deployment.
- [ ] Add a standard-library evidence recorder. Test real child failures, dirty/untracked input fingerprints, and source changes during a run. Record commit, lock hash, tracked/untracked file hashes, exact command, environment metadata, output hashes, exit code and JUnit counts. Reject evidence output inside the measured source tree.
- [ ] Exercise actual owner/runtime and synthetic broker interfaces with generated delayed polls, late fills, cancellation confirmation, partial close, duplicate evidence and restart. Oracle: no close before cancellation is confirmed; no second close while one is unresolved; no duplicate accounting; no restart-driven sends without authority. Confirm valid completed traces too. Preserve failing examples rather than weakening assertions.
- [ ] Run selected existing regressions and generated sequences against the frozen source, with branch coverage as diagnostic evidence. Record skipped cases and distinguish findings in the published revision from ongoing repairs.

Integration owner: this task. Existing broker fixtures supply synthetic events; production owner/runtime code supplies decisions and persistence. Production code and existing fixture contracts are the specification. No new risk constants, sizing policy, external trading or production code changes are planned.

Files: `tools/local_verification/Dockerfile`, `tools/local_verification/requirements-extra.txt`, `tools/local_verification/README.md`, `tools/local_verification/run.ps1`, `scripts/record_verification.py`, `tests/test_record_verification.py`, `tests/sequence_verification/book_event_sequences.py`. Generated tests are opt-in and evidence lives outside the measured worktree.

Acceptance requires a runnable Linux environment and honest revision-specific records, including any failed behavioral assertions. Passing generated examples is bounded evidence, not exhaustive acceptance of PR 409. Current CI uses Ubuntu; the official Python image is Debian and is not an exact runner replica.
