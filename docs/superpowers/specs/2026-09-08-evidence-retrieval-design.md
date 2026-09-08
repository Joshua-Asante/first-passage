# Decision retrieval and evidence use

Approved by Joshua on 2026-09-08 after review of the bounded design in chat.
Extends [the foundation](2026-09-08-evidence-foundation-design.md).

## Contract

`retrieve(context={}, record_ids=None, known_at=None, as_of=None)` searches
registered decision/finding/analysis records, preserving one receipt in the
existing journal. At least nonempty context or explicit IDs is required. Explicit
IDs restrict the candidate set; otherwise every known registered identity is
considered. Unknown explicit IDs fail. No keyword engine or corpus ingestion.
The candidate registry is current; `known_at` restricts revision content. A
registered identity with no revisions by that cutoff remains visible with empty
history, unknown applicability and no selected content.

Conditions remain finite JSON data. Each condition is compared against the same
context key using type-sensitive scalar equality (string, boolean, number).
Integers and floating-point values share the JSON number type; booleans do not.
Null, absent values, arrays and objects are unknown, never executable predicates.
Any unequal supported pair means conflicting; otherwise unresolved conditions
mean unknown; all conditions resolved equally means matching. Empty conditions
are unknown. Extra context keys do not invent additional record restrictions.
Candidates with no temporally selected revision are unknown and unselectable.
Order: matching, unknown, conflicting, then stable record ID. Nothing is hidden
or truncated; ranking describes applicability, never confidence or authority.

Each result retains the existing temporal decision envelope, including history,
conditions, source locator and direct verification. Correction context traverses
declared dependencies and declaration evidence, with cycle-safe traversal, and
reports changed/unavailable sources and superseded dependency revisions. Checks
describe current filesystem/journal observations, even for historical queries;
they do not claim historical filesystem verification. Unknowns and future records
stay visible. Reading receipts never recalculates their stored observations.

Receipts pin normalized request, observation time, journal digest before the
receipt append, ordered results and warnings. A concurrent journal change between
selection and append fails with a retryable error, rather than recording a mixed
snapshot. Filesystem checks are observations, not an atomic filesystem snapshot.

`use(receipt_id, decision_revision, selections)` appends a use event. The decision
must name an existing decision revision; selections contain exact retrieved
revision IDs, disposition `applied` or `not_applied`, and a nonempty reason.
No duplicate selections, nonexistent revisions, or future observations are
accepted. One use event per receipt/decision pair avoids ambiguous replacement.
Unlisted selectable revisions remain `unassessed`. Conflicting/unknown evidence
can be explicitly used with a reason; this records judgment without granting GO.

`receipt(id)` returns the preserved receipt and subsequent use events, with
unassessed IDs made explicit. Use means reported use, not proof of causal benefit.
Receipt/use events use event schema 2; legacy schema 1 events remain readable.
SQLite schema 2 adds receipt/use tables. Graph schema 2 adds RetrievalReceipt,
EvidenceUse, RETRIEVED, FOR_DECISION, FROM_RECEIPT and ASSESSED edges. These
observational edges do not become automatic correction dependencies. Existing
record/source graph identities and declared dependency semantics remain intact.

## Boundaries and acceptance

Python 3.11+, standard library only, governance package, local ignored store.
No ops/lab imports, source-owner edits, execution changes, Neo4j runtime, or
resumption of Q-XMEM-1. Existing keyword tools remain assistive discovery tools.
Test exact/incomplete/conflicting/unsupported context, temporal unknowns,
transitive and cyclic corrections, receipts after edits and supersession,
invalid use references, journal validation, concurrency, legacy rebuild, graph
identity and CLI workflow. No claim of comprehensive corpus recall or learning.
