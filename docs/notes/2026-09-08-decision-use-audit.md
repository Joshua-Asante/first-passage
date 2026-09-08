# Decision review and historical evidence-use audit

Approved interface design in chat on 2026-09-08; implemented on
`codex/evidence-foundation` from `e0d2698` in `.worktrees/evidence-foundation`.
This completes the query integration identified in the
[belief workflow replay](2026-09-08-belief-workflow-replay.md).

## Delivered behavior

- `review DECISION_REVISION` assembles an exact decision revision, its preserved
  receipts, reported-use dispositions/reasons and pinned belief assessments,
  alongside current byte and supersession checks. Optional `--format markdown`
  emits an attachable report without editing a source owner.
- `use-impact NODE_ID` finds selected receipt results whose receipt-time
  provenance includes an exact source version, record revision or assessment.
  Applied decisions are separate from declined/unassessed associations. Receipts
  without use events remain retrieval matches with no associated decisions.
- Historical dependencies come from replaying the journal prefix preceding each
  receipt. A pinned root-belief assessment overrides the later assessment at
  retrieval time for historical queries. Nested dependencies and cycles preserve
  the old evidence trail; later declarations do not appear in old use records.

Both interfaces are read-only for durable events. Cache refresh remains possible.
No schema change, dependency declaration, source annotation, authority grant,
automatic invalidation, new FTS or Neo4j runtime was added. Source-owner text is
fenced as data in the Markdown report.

## Verification

- All 60 evidence tests passed on Python 3.14 within the full required
  `scripts/gate_manifest.py --tier check` run. The check tier passed with existing
  absent-private-source warnings and advisory notes.
- Targeted Python 3.12 pytest: 80 tests and 26 subtests passed (evidence package,
  gate manifest and repository layer map). Full repository pytest was not run.
- Independent review found no actionable issues. Besides the six new audit
  tests, the reviewer independently checked nested belief assessment replacement:
  old evidence remains associated with use, replacement evidence is excluded,
  and the decision receives current review flags.
- CLI tests exercise JSON review/use-impact and Markdown output, missing sources,
  exact-ID errors and unchanged journal bytes. Historical tests cover legacy
  schema 2 receipts, assessment supersession, declared dependency changes,
  cycles and applied/not-applied/unassessed separation.
- Package pylint score: 8.12/10 against the repository's 8.0 bar. Existing and
  new style/complexity notices and delayed cyclic-import warnings remain.
  Twelve Python files parse under Python 3.11 grammar. `git diff --check` passed.

The new queries also ran against the actual local store from the previous
simulation. They found its one applied decision, retained the original supported
judgment, flagged current source drift and left the journal byte-identical.
Generated local reports are in the ignored exercise directory
`.cache/belief-workflow-c56dfdaf40c2441e92dfe2f544b91ab1/`:
`decision-review.md`, `decision-review.json`, and `use-impact.json`.
These are simulation diagnostics, not new live decisions or operator ratification.

## Continuation checkpoint

Current changes are uncommitted; read Git for integration status. Entry points:
`scripts/evidence_store/audit.py`, package README, and `tests/evidence_store/test_audit.py`.
Source and record ownership remain unchanged. Reports include excerpts that may
be private; generating a packet does not authorize publication.

The mechanics now connect preserved evidence, conditional beliefs, assessments,
receipts, reported use and correction review. Next work should be a bounded
adoption in an explicitly chosen real decision workflow, with operator-confirmed
benefit and an explicit review-closeout policy. Per-receipt historical replay
favors auditability over throughput; large-store performance and shared-host
operation are unmeasured. Retain the Neo4j projection until an actual workload
justifies its runtime, and never infer confidence or causal credit from use counts.
