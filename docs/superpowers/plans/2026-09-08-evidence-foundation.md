# Evidence Foundation Implementation Plan

> **For agentic workers:** Use executing-plans to implement this plan task-by-task.
> Review the completed feature independently with requesting-code-review.

**Goal:** Deliver the first evidence-and-correction slice as a usable local CLI.

**Architecture:** Durable JSONL events and content-addressed source blobs feed a
validated SQLite projection. Explicit record revisions and dependency edges power
temporal disposition, provenance verification and correction-impact queries.

**Tech Stack:** Python 3.11+ standard library, SQLite, unittest, local Git.

**Spec:** [Evidence foundation design](../specs/2026-09-08-evidence-foundation-design.md).

## Global Constraints

- Python 3.11+; standard library only; Windows and POSIX.
- Governance-owned `scripts/evidence_store/`; no imports from `lab` or `ops`.
- Durable inputs `.evidence/events.jsonl` + `.evidence/blobs/`; disposable index.
- No live execution, standing skill edits, broad corpus ingestion or new FTS tool.
- No Neo4j runtime; define deterministic schema-versioned export now.
- Work in `.worktrees/evidence-foundation` on `codex/evidence-foundation`.
- Preserve the parent checkout's staged and untracked work. Leave changes reviewable;
  do not commit or publish without a requested integration step.

## File responsibilities

- `scripts/evidence_store/model.py`: strict event validation and relational replay.
- `scripts/evidence_store/store.py`: writer lock, journal/blob durability, index
  lifecycle, source capture/recovery, public query APIs and graph projection.
- `scripts/evidence_store/__main__.py`: JSON CLI boundary and error exit codes.
- `scripts/evidence_store/__init__.py`: package identity, no side effects.
- `scripts/evidence_store/README.md`: field contract, runnable workflow, backups,
  temporal/coverage limits and Neo4j projection.
- `tests/evidence_store/test_store.py`: real fixture-based integration tests.
- `tests/evidence_store/test_cli.py`: subprocess workflow and malformed input.
- `.gitignore`, `scripts/gates.yml`, `scripts/README.md`: local-store exclusion,
  required mechanical tests and discovery link.
- `tests/test_gate_manifest.py`: extend the required gate-reachability probe for
  the new path-conditional entry.

## Task 1 — Preserved evidence and replay

Interfaces: `Store(repo, root, clock=...)`; `capture(source_id, path, kind,
commit=None)`; `source(version_id)`; `rebuild()`.

- [x] Write failing stdlib tests with TemporaryDirectory fixtures: capture bytes,
  edit/delete them, recover the original blob, reject an escaping path, and rebuild
  after removing the index. Repeated content must share a version ID.
- [x] Run `python -m unittest discover -s tests/evidence_store -p test_store.py -v`.
  Confirm missing-feature failure, then implement schema/replay and durable store.
- [x] Verify torn/invalid journal, unavailable Git object, corrupt blob and writer
  lock behavior using real files, not mocks. Use a clock callback for temporal fixtures.
- [x] Run the tests green before advancing.

## Task 2 — Disposition, dependencies and projection

Interfaces: `record(**annotation)`; `depend(**declaration)`;
`decision(record_id, known_at=None, as_of=None)`; `impact(node_id)`;
`check()`; `export()`.

Test annotation example (source must contain both exact strings):

```python
record = store.record(record_id='venue:F1', kind='decision',
    source_version=version_id, section='## Ruling', statement='Status: parked',
    status='parked', conditions={'venue': 'example'},
    effective_at='2026-08-01T00:00:00Z')
```

Dependency example:

```python
store.depend(consumer=record['id'], dependency=data_version_id,
    evidence_version=version_id, note='Declared inputs for this analysis')
```

- [x] Write failing tests for explicit supersession, invalid provenance, missing
  dates/future effective dates, known-at cutoffs and two scoped F1 records.
- [x] Implement validated revision insertion and temporal SQL queries.
- [x] Write failing dependency tests: A uses dataset V1, B uses A, dataset changes;
  impact returns A and B, unchanged data produces no drift finding, cycles terminate.
- [x] Implement dependency validation, recursive SQL and byte-based checks.
- [x] Test export identity against two independent rebuilds, including provenance
  and supersession edges. Implement sorted export with journal revision digest.
- [x] Run the full new store suite green.

## Task 3 — Usable CLI and integration

- [x] Write subprocess tests that execute capture -> record -> depend -> edit ->
  check -> decision -> export -> delete index -> rebuild, then compare exports.
- [x] Implement argparse commands with explicit repo/store paths, JSON annotation
  files and exit 2 for malformed inputs. Diagnostic drift findings exit 0.
- [x] Add `.evidence/` to `.gitignore`; document durable versus disposable files
  and run every documented command against a temporary synthetic corpus.
- [x] Add an `evidence-store` path-conditional gate invoking:

```text
python -m unittest discover -s tests/evidence_store -p test_*.py
```

- [x] Run new tests and the boundary, layer-map and ADR regression checks.
- [x] Independent review of code, spec coverage, failure handling and privacy;
  resolve substantive findings with regression tests.
- [x] Verify diff scope, report runnable commands, test evidence and known limits.

## Review checks

No placeholder tasks; all public interfaces above have actual consumers. The new
suite validates durable storage, relational behavior and the CLI together. Human
semantic correctness is not claimed by a green schema/test result. The optional
graph export is already consumed by deterministic replay tests; no graph service
is required to deliver the foundation.


## Verification record — 2026-09-08

- 26 stdlib store/CLI tests passed under Python 3.14.
- 46 pytest tests plus 16 subtests passed under Python 3.12 (new suite,
  gate-manifest integration and layer-map regressions). The bundled interpreter
  used compatible existing local test packages; no dependencies were installed.
- Full `python scripts/gate_manifest.py --tier check` passed, with existing
  missing-private-source warnings and advisory notes. Local PyYAML was exposed
  through PYTHONPATH for the gate process. Private manifests were not verified
  against absent source bytes; no claim of live operational verification.
- New package pylint score: 8.81/10, above the repository's 8.0 threshold.
- Python 3.11 syntax validation passed for all six new Python files.
- The documented PowerShell workflow ran successfully: parked disposition,
  changed working source, available preserved bytes, one affected record,
  successful rebuild and graph export schema 1.
- A real First Passage F1 ADR was captured in temporary local storage, recovered
  byte-for-byte and rebuilt to an identical graph export. The source was unchanged.
- Independent review found three defects; regression tests reproduced each before
  fixes. Final focused review found none remaining and independently confirmed
  graph/SQL correction-traversal equivalence, including cycles.
- At verification, changes were uncommitted on `codex/evidence-foundation` in the
  isolated worktree. Joshua subsequently authorized commit and push on 2026-09-08.
  No merge, live source annotation or parent-checkout edit was authorized by that step.

The full repository pytest suite was not run. This delivery is the specified
first slice; later retrieval/use logging, belief assessment and Neo4j runtime are
not claimed as implemented.

## Compact continuation checkpoint

Commit-time verification caught inherited Git hook environment bindings in the
synthetic repository fixture. Fixture Git commands and historical source reads
now isolate the selected repository from caller Git bindings. The new regression
failed before the fix; afterward all 27 evidence tests and the targeted 47 pytest
tests plus 16 subtests passed. The first commit attempt was stopped by the hook;
its fixture changed shared `core.bare`, which was restored to `false` before retry.

- Objective: First Passage continuity, relevance and correction through preserved
  evidence, conditional beliefs, decision-use records and reflection.
- Accepted sequence: SQLite first; define Neo4j projection now, introduce its
  runtime later after the foundation is validated.
- Completed first slice: explicit source capture and preserved bytes; durable
  JSONL annotations; rebuildable SQLite; scoped identities and supersession;
  effective/recorded-time queries; cycle-safe correction impact; CLI and graph export.
- Worktree: `C:/Users/joshu/multi_firm_operations/.worktrees/evidence-foundation`.
  Branch: `codex/evidence-foundation`; base: `4fb2b88f3b7d56d77463c43ba45c87ffadff6a31`.
  Read Git for the current commit and remote status, not this checkpoint.
- Entry points: `scripts/evidence_store/README.md` for use and limitations; the
  linked design above for contracts. The verification record above is the test evidence.
- Next design slice: consolidate the decision retrieval interface, keep caveats and
  corrections with each result, and persist retrieval/applied/not-applied records.
  Inspect existing FTS tools and the closed Q-XMEM-1 prior art before choosing
  reuse/replacement. Do not build a third independent keyword-search engine.
- Preserve explicit unknowns, distinguish record status from review status, and
  do not turn a source change into automatic semantic invalidation. Belief assessment
  must fit the evidence; Wilson intervals are not universal belief confidence.
- The original checkout contains unrelated work. Continue in this worktree;
  never sweep the parent's staged/untracked files into this branch.
