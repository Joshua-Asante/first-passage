# Belief Assessment Implementation Plan

> For agentic workers: use executing-plans for tightly coupled changes, then
> requesting-code-review for independent review.

**Goal:** Preserve conditional beliefs, reviewed evidence judgments and corrections.
**Architecture:** Extend existing record revisions and append assessment events;
rebuild SQLite and graph projections, pin belief views in new retrieval receipts.
**Tech Stack:** Python 3.11+, stdlib sqlite3/unittest/argparse.
**Spec:** [Approved design](../specs/2026-09-08-belief-assessment-design.md).

## Global constraints

Worktree `.worktrees/evidence-foundation`, branch `codex/evidence-foundation`, base
`1d441b3`. Standard library only. Preserve source owners, existing receipts and
unrelated parent work. No execution changes, confidence formula or Neo4j runtime.
Leave this delivery uncommitted for review.

## Task 1: Belief and assessment journal

Files: new `scripts/evidence_store/beliefs.py`,
`tests/evidence_store/test_beliefs.py`; modify `model.py`, `store.py`.
Interfaces: existing `record(kind='belief')`; `assess(**review)`.

- [x] Add fixture tests: `belief = store.record(kind='belief', **claim)` and
  `review = store.assess(belief_revision=belief['id'], judgment='supported',
  reviewer='fixture', evidence=[...], **provenance)`. Verify missing behavior fails.
- [x] Add schema 3 validation, exact assessment provenance and linear supersession.
- [x] Reject duplicate evidence IDs, self-reference, wrong kinds, unsupported
  judgments, blank rationale and fabricated excerpts without journal mutation.

## Task 2: Reads, retrieval and correction

Files: above plus `retrieval.py`.
Interfaces: `belief(record_id, context=None, known_at=None, as_of=None)`;
new retrieval receipts pin belief views; old receipts retain schema 2 behavior.

- [x] Write tests asserting `view['belief']['judgment'] == 'supported'` while
  changed evidence yields `view['belief']['review_status'] == 'needs_review'`.
- [x] Implement known-at assessment selection, explicit challenges, scope
  applicability and shared-source grouping. No assessment transfers to new claims.
- [x] Build latest-assessment dependency edges into SQL and traversal; verify
  `impact(changed_version)` includes a declared consuming decision through belief.
- [x] Preserve receipt equality after review replacement and source changes;
  reject a modified assessment snapshot during replay.

## Task 3: Projection, CLI and verification

Files: `store.py`, `__main__.py`, README, CLI/belief tests.
Interfaces: JSON `assess FILE`, read-only `belief ID` with optional context JSON
and known/as-of cutoffs; graph/SQLite schema 3.

- [x] Test `assess`, `belief`, `retrieve`, `receipt`, `export`, `rebuild` through
  the CLI; compare graph before/after removing disposable SQLite.
- [x] Add documented examples and explicit migration/coverage limitations.
- [x] Run stdlib suite, targeted pytest gate/map regressions, required gates,
  Python 3.11 parse check and independent review. Fix findings with reproductions.
- [x] Record verification and a continuation checkpoint here.

## Verification record — 2026-09-08

- All 53 evidence tests passed on Python 3.14 as part of
  `python scripts/gate_manifest.py --tier check`; the full required check tier
  passed. Existing absent-private-source warnings and advisory notes remain.
- Targeted Python 3.12 pytest passed 73 tests and 26 subtests: evidence store,
  gate-manifest integration and repository layer map. No new dependency installed.
- Independent review found a missing ordinary-dependency check in belief views,
  then a historical-cycle path that reintroduced replacement assessment evidence.
  Both were reproduced in failing tests, fixed and re-reviewed. Final focused
  review found no remaining material issues and independently checked historical
  receipt preservation through another review and rebuild.
- Graph/SQL active correction traversal agrees on the assessment fixture. Tests
  cover assessment and belief supersession, contradictory/duplicate evidence,
  conditions, source changes, malformed review provenance and forged snapshots.
- The actual Q-XMEM-1 replay store from the previous delivery migrated to SQLite
  schema 3. Its original schema 2 receipt, dispositions and use event were retained;
  graph export reports schema 3. No source owner was changed.
- Pylint package score 8.24/10 exceeds the repository's 8.0 threshold. Remaining
  style/complexity and delayed cyclic-import notices are not claimed resolved.
  Ten Python files parse under Python 3.11 grammar; `git diff --check` passed.
- Full repository pytest and live/private belief calibration were not run. There
  is no measured probability, independently validated belief confidence, causal
  benefit claim, operational permission or Neo4j runtime in this delivery.

## Continuation checkpoint

Completed on `codex/evidence-foundation` in `.worktrees/evidence-foundation`, based
on `1d441b3`. Current edits are uncommitted. The prior bounded replay report remains
an uncommitted companion artifact from the preceding continuation. Read Git for
integration status; keep original-checkout work separate.

Entry points: `scripts/evidence_store/README.md`, `beliefs.py`, and the linked spec.
New commands: `assess REVIEW.json` and `belief RECORD_ID --context CONTEXT.json`.
New retrieval receipts pin belief views; old receipts remain unchanged. Assessment
judgment, current review status and source-owner authority remain separate.

Next: exercise reviewed belief formation/correction on a bounded real decision
workflow and identify the graph queries that SQLite cannot serve adequately before
introducing Neo4j runtime. Numeric calibration requires an evidence-specific
measurement contract; do not derive confidence from citation/use counts. Shared
source hashes flag shared bytes, not independent evidence. Current dependency
checks are conservative, and historical reads disclose current checks separately
from the historical assessment they select.
