# Evidence and correction foundation

Status: Implementation of the first slice authorized by Joshua on 2026-09-08.
Basis: memory/worldview architecture discussion and Claude audit, checked against
working-tree code at `4fb2b88f3b7d56d77463c43ba45c87ffadff6a31`.

## Outcome and boundaries

First Passage can inspect a decision's recorded history and current disposition,
recover the exact bytes behind a record, and enumerate declared dependents of a
changed source. This is advisory governance tooling. It grants no research,
capital, deployment, or execution authority. Existing source owners remain owners.

Python 3.11+; standard library only; Windows and POSIX; governance-owned package
`scripts/evidence_store/`. No imports from `lab` or `ops`. Existing retrieval
systems, production controls, ADR headers and standing skills remain unchanged.
The closed Q-XMEM-1 pilot is prior art, not silently reopened or re-authorized.

## Durable records and disposable index

The explicit local store defaults to `.evidence/` (gitignored, potentially private).
`events.jsonl` and `blobs/<sha256>` are durable inputs and must be backed up together.
`index.sqlite` is disposable. SQLite is a relational projection, never the sole
copy of an annotation or source. A single-writer lock excludes concurrent writes
and reads during journal append/index replacement. Interrupted writes fail closed;
no automatic truncation or stale-lock removal. Orphan blobs are harmless.

Every event has schema version, UUID, contiguous sequence, UTC recorded time,
type and data. Journal replay validates shapes, references and temporal ordering.
Malformed, conflicting or torn input never replaces a valid index. Source content
is SHA-256 verified on recovery. Index generation is identified by a digest of
the journal bytes; it is rebuilt atomically when those bytes change, including
uncommitted annotations, and a cached projection is trusted only when its rows
and schema objects (tables, indexes, and derived views) authenticate against
that journal. No timestamp or HEAD-only freshness heuristic.

## Identity and source capture

The caller supplies a stable `source_id` independent of the path. A source version
is identified by source identity plus content hash; repeated captures do not create
independent evidence, and a conflicting `kind` on the same version identity is
rejected. Renaming a source preserves identity when the caller reuses
its ID. Each capture preserves its path and recorded time. Optional full Git commit
IDs resolve historical bytes locally; no fetch is performed (including promisor
lazy-fetch), and replace refs are ignored. Failed local recovery
is `missing` or `unavailable`, never a claim of global irrecoverability. Such
observations are indexed explicitly even when no bytes are available.

Only repository-relative regular files within the resolved repository are accepted;
absolute paths, traversal, symlinks in any path component, non-regular files,
Git internals and the store itself
are rejected. Capture is opt-in, one named source at a time, not a whole-repository
copy. Reads compare actual present bytes against the pinned version without
following symlinks. A rename
registered through the same source ID updates the current locator.

## Reviewed records and dependencies

A record has a stable caller-supplied `record_id` and immutable revision UUIDs.
Kinds are decision, finding and analysis. Each revision cites a preserved source
version, an exact section string and a verbatim statement present in those bytes,
an explicit status, structured conditions, and optional effective time. Conditions
are data only; no predicates or source instructions execute. Validation proves
provenance presence, not the truth of an interpretation.

A replacement must explicitly supersede the latest revision of the same record;
conflicting branches are rejected. Effective time and recorded time are distinct.
Historical queries support `known_at` and `as_of`. Undated records are disclosed
as undated and never assigned an invented effective date. A future-effective
revision does not become current early. Each query exposes the history and current
source-verification warnings alongside the selected revision.

Dependencies link an exact consumer record revision to a source version or record
revision, with a supporting source version and note. A record's cited source is an
automatic provenance dependency. Supersession is a distinct relationship, not an
assertion that the replacement depends on the old result. Recursive SQL returns
direct and indirect declared dependents, with cycle-safe traversal. Findings say
`needs_review`, never automatically `false`. Unregistered dependencies remain a
known coverage limit; no semantic extraction is claimed.

## Delivery interfaces

`python -m scripts.evidence_store` exposes JSON commands:

- `capture`: name and preserve a working-tree or local Git source version.
- `record`: accept a JSON annotation containing the fields above.
- `depend`: accept a JSON dependency declaration.
- `source`: report preserved-byte and current-locator verification for a version.
- `decision`: return record history, selected revision and caveats.
- `impact`: return declared dependents of an exact version/revision.
- `check`: report changed/unavailable sources and affected records; findings are
  advisory (exit 0); malformed input and store integrity failures exit 2.
- `rebuild`: validate the durable inputs and regenerate SQLite.
- `export`: return the deterministic graph projection contract.

Every read refreshes against the journal, and source verification checks bytes,
not just a Git commit. Full source bytes remain local; the CLI reports metadata
and deliberately recorded excerpts rather than dumping complete source documents.

## Neo4j contract (defined now, service deferred)

Export schema version 1 includes a journal revision digest, sorted nodes and sorted
edges. Nodes: Source, SourceVersion, RecordRevision. Edges: VERSION_OF, BASED_ON,
SUPERSEDES, DEPENDS_ON. IDs remain identical across rebuilds. Relationship records
carry provenance where declared. Neo4j may consume this snapshot later, atomically
activate one revision, and must expose its revision to readers. A mismatched
revision is stale; rebuild rather than merge divergent stores. No Neo4j driver,
server, credentials, installation or latency claim is included in this slice.

## Acceptance

Tests exercise actual filesystem, Git fixtures, JSON journal, SQLite and CLI:
exact byte recovery after edit/deletion; rename/repeated-capture identity; missing
archive availability; temporal decisions including unknown/future effective times;
scoped IDs; explicit supersession and conditions; direct/transitive/cyclic
dependencies; same-HEAD drift; malformed journals and corrupt blobs; writer lock;
path escapes; deterministic rebuild/export; CLI failures and advisory findings.

The stdlib unittest suite is also pytest-discoverable. A path-conditional entry in
`scripts/gates.yml` runs it in the required gate composition; no live/private store
is needed in CI. A fixture-based end-to-end replay must demonstrate all three
target questions. Existing boundary/map/ADR checks are regression checks.

## Subsequent slices and falsifier

Next: one decision retrieval interface with applicability filtering and durable
retrieval/use logs; then reviewed belief revisions and evidence-appropriate
assessment; then evaluate Neo4j against actual graph workflows. No universal
numeric belief confidence is introduced. This first slice does not fix or replace
the old FTS implementations, automatically annotate the corpus, or connect live
execution. Keep it only if the replay cases resolve provenance/corrections more
reliably than current manual lookup; do not expand a schema without a consumer.
