# Belief revisions and reviewed assessments

Approved by Joshua in chat on 2026-09-08. Builds on the
[retrieval contract](2026-09-08-evidence-retrieval-design.md) and
[bounded replay](../../notes/2026-09-08-evidence-retrieval-replay.md).

## Claims and judgments

`record(kind='belief', ...)` preserves a claim using existing exact source,
conditions, effective-time and explicit-supersession contracts. Source owners
remain authoritative. A belief revision is a reviewed artifact, not an inferred
fact or execution instruction.

`assess(belief_revision, judgment, reviewer, source_version, section, statement,
evidence, supersedes=None)` appends an immutable assessment. Judgments are
`supported`, `contested`, `insufficient`. Reviewer is explicit reported attribution,
not an authenticated identity or operator approval. The assessment cites an exact
verbatim section/statement in a captured review artifact. Its evidence list names
unique existing record revision IDs with `relationship` (`supporting`,
`challenging`, `scope_limiting`), nonempty `rationale`, and `resolution` (nonempty
text or null). Resolution is allowed only on challenging entries; null means an
unresolved challenge. References to the assessed belief itself are rejected.

An empty evidence list is allowed only for `insufficient`. `supported` requires a
supporting entry; `contested` requires a challenging entry. These are structural
checks, not proof of the judgment. Supported judgments with unresolved challenges
remain recorded as supported and expose an explicit review warning.

One linear assessment history exists per exact belief revision. Replacement must
supersede the latest assessment for that revision. Assessment time is recorded
review time, not retroactively reconstructed effective time. A revised belief
starts unassessed; historical assessments are retained on their original target.

## Reads and correction

`belief(record_id, context=None, known_at=None, as_of=None)` is read-only. It
selects the belief revision using existing temporal semantics, then the latest
assessment known at `known_at` for that exact revision. It exposes assessment
history, judgment, evidence relationships, condition applicability, unresolved
challenges, and same-source-hash groups (shared bytes, not independence counts).
`review_status` is `unassessed`, `needs_review`, or `no_flags`; no_flags means only
that the mechanical checks found nothing requiring review.

Current source/record supersession observations remain distinct from the preserved
judgment, including on historical reads. Evidence conditions use existing scalar
matching; unknown/conflicting scope stays visible. Scope-limiting entries always
remain in the assessment. No numeric confidence, vote counting, causal credit or
automatic judgment rewrite is introduced.

Latest assessments attach correction dependencies from their belief revision to
the assessment source and evidence revisions. Thus changed sources propagate
through beliefs into declared consuming decisions. Replaced assessment evidence
does not remain an active dependency; old assessments/receipts retain it as
history. Read-time assessment checks also inspect its own selected evidence,
including historical assessments. Conditional disagreement is surfaced for review,
never automatically adjudicated.

Retrieval schema 3 pins a `belief` view (null for other kinds) on every result.
Old schema 2 receipts remain readable and immutable. Newly added belief records
and assessments use event schema 3; legacy event forms remain valid. SQLite and
graph schema 3 add assessment history and evidence projections. Beliefs retain
RecordRevision identity with kind belief. Assessment nodes and ASSESSES,
SUPERSEDES, SUPPORTING, CHALLENGING, SCOPE_LIMITING and BASED_ON relationships
preserve provenance; only latest-assessment belief edges drive active correction.

## Boundaries and verification

Python 3.11+, standard library only, existing isolated worktree. No private/live
data, broad ingestion, new FTS, external service, Neo4j runtime, risk-control or
standing instruction changes. Reject malformed data before journal append;
replay revalidates references and provenance. Test contradictory and repeated
evidence, conditional scope, belief/assessment supersession, temporal reads,
correction propagation, immutable receipts, legacy migration and graph rebuilds.
