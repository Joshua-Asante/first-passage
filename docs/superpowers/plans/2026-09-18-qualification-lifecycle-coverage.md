# Qualification lifecycle and permission coverage

Roadmap context: Task 8 of the structural-closure plan. Task 9 invariant-gate and
combined qualification acceptance remain separate; this work preserves N1_ONLY.

**Selected outcome:** Concurrent submissions, process death, exact retries,
expiry, both VOID/publication and VOID/commit writer orders, and real client/worker
permission denials preserve at-most-one execution and durable evidence.

**Prerequisites:** Start at `0cc800f` (verified five-fault successor of `6590b61`).
Use isolated `codex/qualification-lifecycle-coverage`; preserve unrelated work.
Existing unfinished tests in `qualification-structural-closure` may be reused
after review. Windows doctor selects operations Python 3.13.2 and 62 locked
packages. Real permission/race acceptance requires the existing two-host Ubuntu
workflow with generated TEST_ONLY credentials and synthetic inputs.

**Ownership:** This task executes inline and owns acceptance of this bounded
outcome. The structural-closure coordinator retains combined release acceptance.

**Verification:** Launcher-recorded focused tests and gates; Linux recorder/JUnit,
stable source revision, complete capture, both writer observations, reopened
journal history, real Docker start events, exact receipts, permission errno/UID
observations and successful owned cleanup. Never count skipped Linux tests as
acceptance. Production fixes require a reproduced failing regression first.

**Checkpoint:** Record findings and evidence here after local tests and each Linux
run. Administrator test checkpoints control timing only, never manufacture
results, signatures, state transitions or acceptance.

**Return boundary:** Deliver implemented changes and verified lifecycle/permission
evidence (or the exact unresolved infrastructure prerequisite). Do not advance
Task 9, full-campaign execution, production qualification, deployment or merge.

## Execution steps

- [x] Enable bounded concurrent RPC handling; verify duplicates/conflicts locally.
- [x] Add administrator-only process/transaction timing checkpoints in test code.
- [ ] Exercise durable interruptions, lost acknowledgments, expiry and both races.
- [ ] Probe actual client UID and running worker filesystem/socket permissions.
- [ ] Run focused local checks and two disposable Linux jobs; inspect retained
  records, review the diff and record the acceptance limits.

The supervisor owns reservation, worker identity and state; SQLite serializes
publication, commit and VOID. The worker supplies captured bytes, the execution
signer signs durable capture, and qg5 reconstructs/signs proposed results. Exact
retries must preserve the original receipt/authentication and history while
reporting present validity and eligibility separately.

## Local checkpoint

- Serial RPC handling was the missing capability. The two dispatcher regressions
  failed before implementation (record `20260918T035745Z-73c1cdb8a657`). The
  production change bounds admission/handlers at four and preserves peer UID
  checks, dispatch locking, thread-local SQLite transactions and response bounds.
- `./fp.ps1 --workers 2 python -m pytest tests/ops/qualification/execution -q
  --tb=short`: 227 passed on the working tree, operations Python 3.13.2, record
  `20260918T040227Z-35826e42fe63`. Removed one copied, unrelated memory-constant
  test afterward. The affected dispatcher/fixture selection then passed 9 tests,
  record `20260918T040802Z-8b4fdb541096`.
- `./fp.ps1 check`: exit 0, 72 evidence-store cases with three existing skips;
  private Pine/data unavailable as disclosed by the gates. Record
  `20260918T040526Z-175b8b56f607`. All records above have stable source and complete
  capture. The deliberately failing red record is not acceptance.
- Linux collection: 34 cases, record `20260918T040802Z-6f08b29c0b40`; collection
  is not process/permission execution. Actual writer attempts are observed from
  SQLite's trace callback, with lock acquisition separately recorded.
- Related-case map: duplicate/conflicting reservation, pre-start uncertainty,
  capture recovery, VOID/publication, VOID/commit, lost acknowledgment and expiry
  preserve the existing single-attempt journal rule. Permission tests probe both
  qclient and the real running container UID. Linux evidence remains pending.
