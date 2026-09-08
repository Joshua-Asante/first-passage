# Evidence and correction foundation

Run from the repository root:

```text
python -m scripts.evidence_store --help
python -m unittest discover -s tests/evidence_store -p test_*.py
```

This is an opt-in, advisory governance tool. It preserves named sources and reviewed
annotations, answers disposition/history questions, and identifies declared
dependents needing review after evidence changes. It does not grant execution or
research authority, infer semantic relationships, or replace either existing search
tool. [Design](../../docs/superpowers/specs/2026-09-08-evidence-foundation-design.md).

## A complete PowerShell example

This creates a synthetic decision in a temporary directory. It does not annotate
or alter First Passage's real decisions. Keep the two printed directories if you
want to inspect the resulting files.

```powershell
$demoRepo = Join-Path $env:TEMP ('evidence-demo-' + [guid]::NewGuid())
$demoStore = Join-Path $demoRepo '.evidence'
New-Item -ItemType Directory -Path $demoRepo | Out-Null
@'
# Example decision
## Ruling
Status: parked
'@ | Set-Content -Encoding utf8 (Join-Path $demoRepo 'decision.md')
$capture = python -m scripts.evidence_store --repo $demoRepo --store $demoStore capture example:F1 decision.md --kind adr | ConvertFrom-Json
@{
  record_id = 'example:F1'; kind = 'decision'
  source_version = $capture.version_id
  section = '## Ruling'; statement = 'Status: parked'; status = 'parked'
  conditions = @{ venue = 'example' }
  effective_at = '2026-08-01T00:00:00Z'
} | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $demoRepo 'annotation.json')
$record = python -m scripts.evidence_store --repo $demoRepo --store $demoStore record (Join-Path $demoRepo 'annotation.json') | ConvertFrom-Json
python -m scripts.evidence_store --repo $demoRepo --store $demoStore decision example:F1
'Changed after the decision' | Set-Content -Encoding utf8 (Join-Path $demoRepo 'decision.md')
python -m scripts.evidence_store --repo $demoRepo --store $demoStore source $capture.version_id
python -m scripts.evidence_store --repo $demoRepo --store $demoStore impact $capture.version_id
python -m scripts.evidence_store --repo $demoRepo --store $demoStore check
python -m scripts.evidence_store --repo $demoRepo --store $demoStore rebuild
python -m scripts.evidence_store --repo $demoRepo --store $demoStore export
$demoRepo
$demoStore
```

Expected: the recorded disposition remains `parked`, its preserved source remains
available, the working source is `changed`, and `example:F1` is `needs_review`.
The tool never substitutes a new conclusion for the recorded one.

## Commands and records

Global `--repo` selects the source checkout; default is the current directory.
Global `--store` selects durable local storage; default is `REPO/.evidence`.
Use a separate store for unrelated repositories and give logical IDs a namespace.

| Command | Input / result |
|---|---|
| `capture SOURCE_ID PATH --kind KIND` | Preserve one relative file; return version ID and SHA-256. Reuse SOURCE_ID when relocating the same source. |
| `capture ... --commit SHA` | Read a blob at an exact full local Git SHA-1. Never fetch. An unavailable object is recorded as unavailable, not globally lost. Trees are rejected. |
| `record FILE.json` | Validate and append a reviewed record revision. |
| `depend FILE.json` | Append an explicit, evidence-cited dependency. |
| `source VERSION_ID` | Verify preserved bytes and compare current working bytes using the latest registered path. |
| `decision RECORD_ID` | History, effective current revision, undated records and source warnings. |
| `decision ... --known-at TIME --as-of TIME` | Recorded-time and effective-time cutoffs independently. |
| `impact VERSION_OR_REVISION_ID` | Direct and transitive declared dependents, cycle-safe. |
| `check` | Changed/missing/corrupt source findings and affected records. Advisory exit 0. |
| `retrieve REQUEST.json` | Select registered evidence by context/IDs and append a durable receipt. |
| `use USE.json` | Report applied/not-applied evidence for an exact decision revision. |
| `receipt ID` | Read original observations and subsequent use records. |
| `assess REVIEW.json` | Preserve a reviewed assessment of an exact belief revision. |
| `belief ID --context CONTEXT.json` | Read a belief, assessment history and current review flags. |
| `review DECISION_REVISION` | Read an exact decision revision, receipts, use reasons and current checks. |
| `review DECISION_REVISION --format markdown` | Emit an attachable Markdown review packet. |
| `use-impact NODE_ID` | Find selected receipt results containing an exact historical source, record or assessment. |
| `rebuild` | Validate durable inputs and atomically recreate SQLite. |
| `export` | Deterministic JSON graph snapshot, including its journal revision digest. |

Record fields: `record_id`, `kind` (`decision`, `finding`, `analysis`, `belief`),
`source_version`, `section`, `statement`, `status`, `conditions`; optional
`effective_at` and `supersedes` (default null). `section` is one unique exact
Markdown ATX heading (`#` through `######`, outside fenced code). The verbatim
statement must occur within that section, including its subsections. Duplicate
headings are deliberately ambiguous: choose an unambiguous source section.
Validation proves excerpt provenance, not whether the status/conditions interpret
it correctly. `conditions` is a JSON object, never executable predicate code.

A later revision must explicitly name the previous revision UUID in `supersedes`.
This prevents accidentally replacing another author's latest revision. Revisions
and original source bytes remain recoverable. Source version identity deduplicates
equal bytes for the same source; it does not establish statistical independence.

Dependency fields: `consumer` (record revision UUID), `dependency` (source version
or record revision), `evidence_version` (preserved source supporting the declaration),
`note`. Both the declared input and evidence supporting the declaration can trigger
review. Every record already depends on its own cited source; no separate `depend`
call is needed for that link. Supersession alone is not a dependency.

Timestamps require a timezone and normalize to UTC. Recorded time is capture or
annotation time, not a reconstructed historical timestamp. Unknown effective time
stays null: history remains visible, but no effective disposition is fabricated.
Future-effective revisions are withheld until their effective time. An undated
later revision makes the effective current disposition unknown. Historical queries
still disclose **present-time** source verification separately; they do not claim
that today's source availability was known in the past.

Commands emit JSON. Input/store errors exit 2 with an `error` object on stderr;
argparse usage errors use its normal help text. Integrity errors differ from
advisory drift findings. Raw documents are not dumped by the CLI, but recorded
excerpts, conditions, paths and hashes may themselves be private.

## Preservation and recovery

Back up `events.jsonl` and `blobs/` together. They are local, durable evidence;
gitignore prevents publication, not data loss. Only `index.sqlite` is disposable.
No source copy is automatically pushed to the public repository. Custom stores
must be outside tracked/public paths or explicitly ignored by their owner.

Each append is serialized with `writer.lock` and flushed to disk. The index is
replaced only after a complete journal validates. A crash may leave an orphan blob
or temporary index; these are not evidence events. A torn journal fails closed;
restore a verified backup, do not truncate it blindly. If a stale lock remains,
verify that no process is using the store before removing it. This is local
single-writer storage, not a network-filesystem/distributed database guarantee.

Changed source bytes trigger review, not automatic invalidation. Missing or corrupt
preserved bytes are surfaced explicitly. An unreachable local Git object may still
exist elsewhere. A rebuild cannot recover evidence whose durable inputs were lost.
Journal validation is not a cryptographic signature or protection against an actor
deliberately rewriting the entire store and its blobs.

Coverage is limited to explicitly captured sources and declared relationships.
No absence-of-dependencies claim applies to unregistered research. Entire-source
hash changes conservatively flag cited records even if their own excerpt did not
change. Automatic adapters, calibrated numerical assessments and reconciliation
of existing FTS tools belong to later slices.

## Retrieval and reported use

Retrieval is an explicit journal write. It considers only registered records and
does not search prose or discover missing evidence. Existing keyword tools remain
assistive source discovery. Request example (`request.json`):

```json
{"context": {"venue": "example"}, "record_ids": ["venue:F1"]}
```

Run `python -m scripts.evidence_store --repo REPO retrieve request.json` using the
same repository/store as your captures. Omit `record_ids` to consider all registered
identities; omit context for explicit-ID inspection. At least one is required.
Optional `known_at` and `as_of` use the existing timestamp conventions.

All results remain visible, ordered matching, unknown, conflicting, then record
ID. Matching means every declared condition equals a provided scalar context
value. Strings, booleans and numbers are distinct types (`1` equals `1.0`, but
not `true`). Missing/null/structured conditions remain unknown; conflicting
supported values take precedence. Empty conditions are unknown. Extra context
keys do not invent restrictions. Conditions and source text never execute.

The registry is current, while revision content is limited by `known_at`; an
identity with no known revision has empty history and no selectable content.
Future-effective or undated revisions do not invent a current disposition.
Sources and transitive dependencies are checked at observation time, even for a
historical request. Superseded dependency revisions require review, not automatic
invalidation. These findings never grant research, capital or execution authority.

The returned event `id` identifies the receipt. Its `data` pins the request,
ordered results, exact revision excerpts, journal digest and observed warnings.
`receipt ID` reads that preserved snapshot; run a new `retrieve` for fresh checks.
A concurrent journal change fails before receipt append: retry the request.
Filesystem checks are observations, not an atomic filesystem snapshot.

Create `use.json` with IDs from your receipt and a registered decision revision:

```json
{
  "receipt_id": "UUID returned by retrieve",
  "decision_revision": "UUID returned by record for the decision",
  "selections": [
    {"revision_id": "current.id from a receipt result", "disposition": "applied", "reason": "Explains the decision's stated condition"}
  ]
}
```

Run `python -m scripts.evidence_store --repo REPO use use.json`, then
`python -m scripts.evidence_store --repo REPO receipt RECEIPT_ID`. Each use record
reports `unassessed` for omitted selectable revisions. Before any use event,
every ID in `selectable` is unassessed. Use `not_applied` with a reason for evidence
considered but rejected; no reason or outcome is inferred from silence.
Only one use event per receipt/decision pair is accepted. Another decision
revision can have a separate assessment. This is reported use, not measured
causal benefit; use edges do not automatically declare substantive dependencies.

## Neo4j projection

`export` schema 3 contains sorted `nodes` and `edges` plus `revision` (SHA-256 of
the exact durable journal). Labels: Source, SourceVersion, RecordRevision.
Relationships: VERSION_OF, BASED_ON, SUPERSEDES, DEPENDS_ON. Each edge has an ID,
`from`, `to`, and `type`; declared edges carry evidence provenance. BASED_ON also
represents the evidence supporting a dependency declaration. Node conditions are
nested JSON; a future Neo4j importer must encode those properties explicitly,
not assume Neo4j property values accept nested objects.

Schema 3 retains RetrievalReceipt and EvidenceUse nodes, with RETRIEVED,
FOR_DECISION, FROM_RECEIPT and ASSESSED relationships. Receipt/use nodes contain
nested event JSON; encode it explicitly in a future importer. RETRIEVED carries
position/applicability; ASSESSED carries disposition/reason. These observational
edges stay separate from correction dependencies. Consumers of older graph schemas
must explicitly support schema 3 before importing. Legacy events remain valid;
new belief records, assessments and retrieval receipts use schema 3, use events
remain schema 2. SQLite schema 3 rebuilds automatically from older or mixed
journals; no durable input migration is needed. Older receipts stay immutable.

Assessment nodes preserve full review events. ASSESSES connects each review to
its belief revision; SUPERSEDES links successive reviews. EVIDENCE edges preserve
every review's supporting/challenging/limiting references. Active belief-to-evidence
edges use SUPPORTING, CHALLENGING and SCOPE_LIMITING; BASED_ON also connects the
belief to its latest review source. Only latest-assessment belief edges contribute
to active correction traversal. Historical assessment nodes remain inspectable.

Byte-identical journal rebuilds yield identical exports. Filesystem verification
is intentionally separate and live; a graph snapshot is not evidence that current
files remain unchanged. A future importer should stage and activate one revision,
reject stale revisions at query time and rebuild from this projection. No Neo4j
service or driver is installed in this slice.

## Beliefs and reviewed assessments

Use `record` with `kind: "belief"` to preserve a claim from an authored source.
The same exact excerpt, conditions, effective-time and supersession rules apply.
A new belief revision starts unassessed; no prior judgment transfers implicitly.

An assessment must cite a preserved review artifact, for example a Markdown file
containing `## Judgment` and a sentence explaining the evidence comparison.
Capture that file before writing the assessment. `review.json` shape:

```json
{
  "belief_revision": "UUID returned by the belief record command",
  "judgment": "supported",
  "reviewer": "Named reviewer or reviewing process",
  "source_version": "version ID returned by capturing the review artifact",
  "section": "## Judgment",
  "statement": "Exact sentence from that section of the review artifact.",
  "evidence": [
    {
      "revision_id": "Exact existing evidence record revision UUID",
      "relationship": "supporting",
      "rationale": "Why this evidence bears on this conditional claim.",
      "resolution": null
    }
  ],
  "supersedes": null
}
```

Run `python -m scripts.evidence_store --repo REPO assess review.json`, then
`python -m scripts.evidence_store --repo REPO belief BELIEF_ID --context context.json`.
The context file is a plain JSON object, such as `{"instrument": "ES"}`.
`belief` accepts `--known-at` and `--as-of` as well; it does not write a receipt.
Use `retrieve` to preserve the result, including its nested `belief` view.

Judgments are `supported`, `contested`, `insufficient`. Supported requires a
supporting entry; contested requires a challenging entry; insufficient may have
no evidence. These checks prove structure, not semantic validity. Attribution in
`reviewer` is reported text, not authentication or operator approval.

Relationships are `supporting`, `challenging`, `scope_limiting`. Each requires a
reason; duplicate revision IDs and self-citations are rejected. A challenging
entry with null `resolution` remains unresolved. Reviewed resolution text can be
supplied on a replacement assessment. Resolutions are not accepted on other
relationship types. Replacement must explicitly supersede the latest assessment
for the same belief revision.

The readout keeps the recorded judgment separate from `review_status`:
`unassessed`, `needs_review`, or `no_flags`. It reports unresolved challenges,
condition mismatches/unknowns, changed or unavailable sources, superseded
revisions, and groups of evidence sharing the same source hash. Shared bytes are
not independent votes; separate hashes do not prove independence either.
`no_flags` means only that these mechanical checks found no review flags.
No numeric confidence or automatic judgment change is implied.

Latest assessment evidence and review-source changes participate in correction
traversal through the belief into declared consuming decisions. Replaced reviews
retain their historical evidence without keeping it active. Historical reads
select the review known at the cutoff, but source and dependency checks describe
present observations. Assessment review time is recorded time, never backdated
effective time. Unknown claim effective dates still prevent current selection.

## Decision reviews and historical use audits

`review` takes the exact UUID returned by `record` for a decision, unlike
`decision`, which takes a stable record ID and selects a revision by time. It
joins that revision's use events to full preserved receipts. Each selected
item has its original observations, disposition/reason, receipt-time provenance
nodes, and separate current source/supersession checks. No recorded use returns
`no_recorded_use`: a coverage gap, not proof that no evidence was used.

```powershell
python -m scripts.evidence_store --repo REPO review DECISION_REVISION
python -m scripts.evidence_store --repo REPO review DECISION_REVISION --format markdown
python -m scripts.evidence_store --repo REPO use-impact EXACT_SOURCE_VERSION_OR_REVISION_OR_ASSESSMENT
```

Both commands are read-only with respect to durable records. They may refresh the
disposable index. Markdown is emitted to stdout for the caller to save or attach;
the command never modifies a source owner. Full receipts/excerpts may be private.
Source text is fenced JSON in the report, not executable document markup.

`use-impact` accepts a source version ID, record revision UUID, or assessment UUID.
It replays the journal prefix preceding each receipt to follow the dependencies
observed then. For a belief, its pinned assessment overrides the latest assessment
at retrieval, including historical `known_at` queries. Later declarations and
replacement evidence are not retroactively attributed to old receipts. Nested
dependencies and cycles are supported; old schema 2 receipts remain usable.

Results group matching selected roots by receipt and show associated decisions
as `applied`, `not_applied`, or `unassessed`. `applied_decisions` includes only
explicit applied selections. A receipt with no use event has no associated
decision; it is still a retrieval match. History-only/future/undated results with
no selected current revision are not treated as used evidence.

Unlike `impact`, this query follows reported use and its historical provenance;
it does not add substantive dependency declarations. Empty results mean no match
within recorded coverage. Current node checks inspect bytes for source versions
and replacement lineage for revisions/assessments; use `review` for the full
associated decision's source checks.

Review summary status reflects current checks on the decision and its applied
evidence. Declined/unassessed items retain their own checks but do not become
applied by association. Original scope, belief judgment and warnings remain in
`as_observed`; `no_flags` is not a semantic approval or an authority grant.
These joins deliberately favor traceability over a cache: per-receipt historical
replay is suitable for bounded local workflows and is not a large-corpus latency
claim. Journal, SQLite and graph schema versions remain unchanged at this slice.
