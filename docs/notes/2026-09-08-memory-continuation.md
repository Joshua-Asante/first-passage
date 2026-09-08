# Compact memory-architecture handoff

## Objective and current state

First Passage continuity, relevance and correction. User chose SQLite first;
Neo4j projection defined, runtime deferred pending demonstrated need.

Worktree: `C:/Users/joshu/multi_firm_operations/.worktrees/evidence-foundation`.
Branch: `codex/evidence-foundation`. Latest pushed implementation: `eb46044`
(decision review/use audit). Remote: `origin` / Joshua-Asante/first-passage.
Read Git for fresh status. Parent checkout contains unrelated work; do not touch it.

Implemented in `scripts/evidence_store/`: preserved sources, immutable JSONL,
disposable SQLite, explicit revisions/dependencies, conditional retrieval,
receipts/use records, beliefs/reviewed assessments, correction traversal,
JSON/Markdown decision review, historical use-impact, graph schema 3. Python 3.11+
stdlib only. Existing FTS tools and source owners unchanged; no live execution.

## Verification and contracts

Latest implementation: 60 evidence tests; targeted pytest 80 tests + 26 subtests;
required check tier and actual commit/push hooks passed. Independent review found
no actionable audit issues. Earlier findings fixed with regression tests.
Pylint 8.12/10 (bar 8.0); style/complexity/cyclic-import notices remain.
Full repo pytest, large-store performance and live/operator benefit unmeasured.

Entry point: `scripts/evidence_store/README.md`. Specs/plans are in
`docs/superpowers/{specs,plans}/2026-09-08-*`; latest integration record is
`docs/notes/2026-09-08-decision-use-audit.md`.

Keep recorded judgment separate from review status and authority. Preserve
unknown conditions and historical receipts. Reconstruct use provenance from the
receipt-time journal, not today's graph. Applied, declined and unassessed differ.
Shared hashes do not imply independent evidence; never infer confidence from
citation/use counts. Graph export exists; no Neo4j service installed.

## Current continuation: first real advisory adoption

Adoption note: `docs/notes/2026-09-08-architecture-evidence-adoption.md`.
Uses the current architecture review itself, not trading/campaign execution.
Claim: SQLite supports the demonstrated bounded queries; scale/multi-user behavior
unmeasured. Codex advisory assessment is supported with explicit scope limitation.
No real source was changed to fabricate a correction, and no historical approval
or use time was invented. Registration and use describe this present review.

Local ignored store: `.evidence/architecture-adoption/`; back up its journal and
blobs together. `adoption.json` contains IDs, `review.md` is the review packet,
`review.json` and `use-impact.json` are machine-readable outputs.
Decision revision: `2408289d-d8bc-48c6-a007-2ca5e5f65b51`.
Receipt: `69e86a87-62dc-4ab3-9c99-a19e3a52f065`.
Current mechanical status: no_flags; operator-confirmed benefit: pending.
Do not rerun registration blindly: reuse these identities/store and append explicit
revisions only if evidence changes. Changing the adoption source will flag drift.

## Next action

Have Joshua assess whether the packet makes provenance, limitations and use easier
to review. Record his actual feedback rather than claiming benefit from successful
execution. Continue the bounded adoption; a real correction needs reviewed source
evidence and explicit assessment/record revision, not automatic closeout. Further
workflow policy, calibration or Neo4j runtime needs a concrete justified design.
No unfinished implementation or failing check is currently known.
