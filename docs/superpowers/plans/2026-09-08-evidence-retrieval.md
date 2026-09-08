# Evidence Retrieval Implementation Plan

> For agentic workers: use executing-plans for these tightly coupled tasks;
> request independent code review after integration.

**Goal:** Retrieve applicable registered evidence and preserve explicit decision use.
**Architecture:** Extend the existing journal and SQLite projection; implement
context matching and receipt validation in a focused retrieval module.
**Tech Stack:** Python 3.11+, sqlite3, unittest, argparse.
**Spec:** [Approved contract](../specs/2026-09-08-evidence-retrieval-design.md).

## Global constraints

Standard library only; Windows/POSIX; governance-owned; no new FTS or execution
changes. Continue in `.worktrees/evidence-foundation` on
`codex/evidence-foundation`. Preserve unrelated parent-checkout work. Leave this
slice reviewable; previous commit/push covered the foundation delivery.

## Task 1: Retrieval and immutable receipts

Files: new `scripts/evidence_store/retrieval.py` and
`tests/evidence_store/test_retrieval.py`; modify `store.py`, `model.py`.
Interfaces: `Store.retrieve(context=None, record_ids=None, known_at=None,
as_of=None)`, `Store.receipt(receipt_id)`; private matching/validation helpers.

- [x] Write real-store fixtures with matched, conflicting and unknown records:
  `r = store.retrieve(context={'instrument': 'ES'})`;
  `assert r['data']['results'][0]['applicability']['status'] == 'matching'`.
- [x] Run `python -m unittest discover -s tests/evidence_store -p test_retrieval.py -v`
  and confirm missing-method failures.
- [x] Implement matching, shared temporal read, transitive current correction
  context, journal schema 2 receipt validation and SQLite tables. Append receipts
  with `expected_revision` checked under the writer lock.
- [x] Prove immutability: save `receipt['data']`, edit sources and supersede a
  record, rebuild, then compare `store.receipt(id)['receipt']['data']` exactly.
- [x] Test unknown IDs, corrupt journal references, and stale append digest;
  each must raise `EvidenceError` without changing journal bytes.

## Task 2: Use records and graph projection

Files: same modules/test; extend `Store.export()`.
Interfaces: `Store.use(receipt_id, decision_revision, selections)` and graph v2.

- [x] Add failing tests for valid applied/not-applied reasons and remaining
  unassessed revisions, wrong receipt membership, duplicate use, and wrong kind.
- [x] Implement schema/replay validation and SQLite use rows. Return receipts
  with separate subsequent use annotations; never mutate original observations.
- [x] Export stable receipt/use nodes and relationships; test graph equality
  before/after deleting SQLite and rebuilding. Retain legacy-event replay tests.
- [x] Run all evidence tests; fix substantive regressions with reproductions.

## Task 3: CLI, documentation and verification

Files: `__main__.py`, package README, `tests/evidence_store/test_cli.py`.
Interfaces: JSON-file `retrieve`/`use` commands, `receipt ID` query.

- [x] Write a subprocess workflow that captures, records, retrieves, reports use,
  changes evidence, reads the preserved receipt and rebuilds/exports.
- [x] Add CLI commands and runnable JSON examples, explaining unknown context,
  advisory corrections, explicit use and graph v2 migration.
- [x] Run stdlib suite, targeted pytest gate/map regressions, and required gates.
- [x] Request independent review; resolve findings with tests; record results
  and compact next-step checkpoint here. Do not claim broader tests were run.

## Verification and continuation checkpoint — 2026-09-08

- Implemented `retrieve`, `use`, and `receipt` in the existing package and JSON
  CLI. Context matching and temporal selection are deterministic; the old
  single-record decision query shares the temporal helper.
- Receipt/use events use schema 2 alongside legacy schema 1. SQLite and graph
  export are schema 2. Legacy cache regeneration and mixed-journal replay pass.
- All 41 stdlib evidence tests passed on Python 3.14. Targeted pytest on Python
  3.12 passed 61 tests and 20 subtests (evidence, gate manifest, repository map).
- Full `scripts/gate_manifest.py --tier check` passed on the implementation,
  including the then-39-test suite. Two subsequent verification tests cover
  concurrent journal writes and legacy cache migration; the final 41-test run
  includes both. Existing absent-private-source warnings and advisory notes remain.
- Independent review reproduced four defects before fixes: JSON number matching,
  cutoff-empty identities hidden, non-string context keys poisoning replay, and
  boolean/number confusion in pinned receipt validation. Regression tests failed
  first and pass after fixes. Re-review reported no remaining material findings.
- The migration test initially kept its own SQLite connection open on Windows;
  explicit connection closing fixed the fixture. Production rebuild already
  closes its connections before replacing the file.
- Package pylint scored 8.44/10, above the repository's 8.0 bar; it still reports
  style/complexity and delayed cyclic-import notices. Eight Python files parse
  using Python 3.11 grammar. `git diff --check` passed.
- Full repository pytest and live/private corpus validation were not run. No
  claim of broad recall quality, operational benefit, or causal learning is made.

Changes are uncommitted in `.worktrees/evidence-foundation` on
`codex/evidence-foundation`, based on foundation commit `6593786`. No source
annotations, private captures, or parent-checkout edits belong to this delivery.
Read Git for integration status rather than treating this checkpoint as current.

Next architecture slice: reviewed belief revisions and evidence-appropriate
assessment. Before expanding that schema, use these retrieval/use interfaces on
a bounded, explicitly chosen decision workflow and establish what counts as a
useful correction. Keep unknown applicability visible, keep source owners as
authority, and defer Neo4j runtime until graph workflows demonstrate need.
