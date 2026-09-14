# CrossTrade Observer Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Persist read-only CrossTrade observations and their limitations without granting recovery authority.

**Architecture:** A one-shot collector uses a fixed GET transport and an account-bound SQLite journal. Each observation and detected fill revisions commit atomically. CLI output contains summaries only.

**Tech Stack:** Python 3.11+, urllib, sqlite3, argparse, pytest.

**Spec:** [Approved design](../specs/2026-09-14-crosstrade-observer-design.md).

## Global Constraints

- No broker mutations, production host file changes or support contact.
- No conversion of collected data into qualified RecoveryEvidence.
- Credential remains outside reports; journal is private account data.
- Existing worktree at starting revision `ed1c18774fe3da3feff641404a8c56b34a28c903`.

## Task 1: Collect, persist and inspect one bounded run

Integration owner: current task. CrossTrade produces observed facts; the collector
owns local run IDs, observation records, revisions and diagnostic flags. Missing
broker coherence, history coverage and global request fencing remain unproven.

Files: `ops/crosstrade_observer/{__init__,transport,journal,collector,__main__}.py`,
`tests/ops/test_crosstrade_observer.py`, `.gitignore`, and package README.

Interfaces: `ReadClient(secret).get(path)` returns `(status, JSON)`;
`Journal(path, account)` binds persistence to one account;
`collect(client, journal, account, limit=500, max_pages=10)` returns a redacted
summary. `Journal.report(run_id)` returns persisted summary after reopening.

- [x] Write failing behavior tests. First example:

```python
def test_collection_survives_restart(tmp_path):
    with Journal(tmp_path / 'observations.db', 'SYNTHETIC') as journal:
        result = collect(FixtureClient(), journal, 'SYNTHETIC')
    with Journal(tmp_path / 'observations.db', 'SYNTHETIC') as journal:
        assert journal.report(result['run_id']) == result
        assert result['qualification'] == dict(E1='unproven', E2='unproven', E3='unproven')
```

- [x] Run focused pytest and verify missing collector causes failure.
- [x] Implement fixed-route GET transport: reject redirects, timeout, cap bytes,
  parse strict JSON, sanitize credential, return errors without private messages.
- [x] Implement journal schema version/account binding, per-observation atomic
  commits, append-only response bodies and fill versions; persist running/done
  states and conflict/partial flags. Reopen without silently completing old runs.
- [x] Implement sequential bounded collection. Validate each envelope/account;
  follow opaque history cursors, detect loops and exhausted page budget; compare
  snapshot `asOf` with previous observations for cache reuse. Preserve fee changes
  separately from economic conflicts; keep E1–E3 unproven even on empty success.
- [x] Add CLI using config/journal paths and finite page limits; use generic error
  output and nonzero exit for incomplete observations. Write README commands and
  journal privacy/limitations. Example invocation:

```text
python -m ops.crosstrade_observer --config c1_rail_config.json --journal .crosstrade-observer/observations.sqlite3
```

- [x] Verify synthetic failure cases and real SQLite restart. Run:

```text
python -m pytest tests/ops/test_crosstrade_observer.py -q
python scripts/check_boundaries.py
python -m pylint ops/crosstrade_observer --errors-only
```

- [x] Review full changed behavior, fix demonstrated defects, run an authorized
  read-only live smoke where available, and record exact limits.
- [x] Prepare reviewed collector, tests and documentation for the authorized commit/push; publication revision is recorded in the task response and Git history.

## Verification record

Implementation completed inline in the existing worktree. Initial test collection
failed because the package was absent. Subsequent RED cases demonstrated missing
CLI behavior, scoped account checks, history numeric-account mismatch and numeric
JSON overflow. A Windows test-name length issue was fixed with explicit short
parameter IDs. A repeated-run test exposed identical local timestamps; unfinished
run ordering now uses SQLite insertion order, never claimed as broker causality.

Independent reviewer `observer_review` reproduced the account-ID mismatch and
flagged overflow handling. Both fixes have regression coverage; follow-up review
found no remaining blockers. Live smoke exposed timezone-less snapshot `asOf`;
a new regression preceded the fix, which retains valid account binding while
reporting `snapshot_timezone_unavailable`. Follow-up review accepted that behavior.

- CPython 3.11.9: focused observer suite **29 passed**.
- Combined observer and recovery-owner/validation/process suites: **71 passed**
  in 10.79 seconds. Existing recovery code was not changed.
- Error-level pylint passed; import-boundary checker passed (518 modules).
- Private journal is excluded by `.gitignore`; whitespace checks passed.
- Staged-change `gate_manifest.py --tier check` passed, including 72 evidence-store
  checks (3 skipped), with existing absent-private-tree and advisory notes.

Final live smoke used exact transport/journal/collector source loaded only in
memory on the existing disarmed host. The existing credential remained there;
two read batches five seconds apart produced 12 HTTP observations and four stored
fill versions. The second batch added zero duplicate versions. The database was
serialized in memory and returned over SSH into local ignored storage; no host
files, configuration, orders or WebSockets were changed. Credential absence in
the exported database was checked before transfer. SQLite integrity returned `ok`
and both reports compared equal after reopening locally.

Local private journal: `.crosstrade-observer/live-smoke-20260914T232214.sqlite3`.
Run IDs: `b68f2151-b6d1-4844-a8d7-fc029a37d002` and
`7e23c954-5b71-402a-8332-b79b53f2cbf5`. Both reports were `limited` solely by
`snapshot_timezone_unavailable`, both exhausted stored history pagination, and
both retained E1/E2/E3 as `unproven`. This is a working collector, not qualified
recovery evidence. The Fly wrapper again exited 1 after a complete export; the
private database and reopened reports, rather than wrapper exit status, establish
the smoke result. An earlier invocation failed locally before requests, and an
earlier smoke journal is retained privately as evidence for the timestamp fix.
