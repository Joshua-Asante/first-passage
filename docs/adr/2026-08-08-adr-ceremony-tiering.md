# ADR 2026-08-08 — When an ADR is necessary; concise records and verified retirement

**Status:** `Accepted` — operator approved ADR pruning and this policy revision on 2026-09-08.
**Decision date:** 2026-08-08
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Format:** concise
**Revision:** 2026-09-08; prior decision at `4fb2b88f3b7d56d77463c43ba45c87ffadff6a31`.

**Workflow owners:** [Methodology skills — canonical source and one-way deployment](../../scripts/README.md#skill-lifecycle) · [Brief authoring — canonical check_brief checker, type contracts and repo subset](../../.claude/skills/brief-authoring/SKILL.md#checker-ownership).

## Decision

ADRs are not a general decision log. Create a new ADR only when all three apply:

- The choice establishes or changes durable architecture, a standing governance
  rule or an authority boundary that future work must respect.
- Its rationale or tradeoff needs to remain discoverable to guide future choices.
- An update to an existing owner cannot hold that rationale clearly; a distinct
  record has a continuing purpose beyond documenting that a decision occurred.

A consequential decision may still belong in its specification, campaign record,
implementation plan or PR. Importance, approval, or the fact that alternatives were
considered does not by itself require an ADR. Routine fixes, moves, citation repairs
and elections within an approved envelope need no ADR or light-record substitute.
Record decisions where they help continuing work; do not inventory every choice.

Keep an existing ADR only while its distinct rationale or authority boundary is
still needed. One current owner holds each rule. ADRs explain the choice and tradeoff; operating
owners hold procedure, schemas, counters and live evidence. Do not preserve a
standalone ADR merely because it is Accepted, old, cited or contains unique history.

The current form is `Format: concise`: Decision (including scope), Grounds (the
reason and real alternative/tradeoff), and Current owner (contract/implementation
links). Keep the graph header and approval/effective date. Add source-read anchors,
evidence, meaningful reversal conditions and checks where the decision needs them.
There is no mandatory empirical falsifier, quarterly cadence, full/light election,
word-count gate, or quota of retained records. Existing full/light formats remain
readable; they need not be converted merely for appearance.

Approved changes update effective decision text with a dated revision and immutable
prior version. Proposed branches remain separate and unapproved. This does not permit
changing frozen preregistrations, lock artifacts, verdict logic or evidence after a
result. Source-first risk review, authorization requirements and review independence
continue to follow the consequence of the change, regardless of document length.
Required research, lock-change and execution approvals/evidence remain required;
their governing contracts determine the artifact, not a blanket ADR requirement.

Before consolidation/removal, read the complete body and amendments. Migrate every
surviving constraint and actual reader; disposition each obligation as retained,
discharged, superseded or explicitly retired. A lost input is not a passing check.
Preserve incoming file, fragment and section references by repointing current callers
or pinning historical references. Verify retrieval of each removed blob and the
failure behavior of affected tools before deleting it.

Use `TOMBSTONES.md` for removed ADR paths, immutable commit/blob, disposition and
current owner if any. A hot stub plus cold body is optional legacy storage, not a
retention requirement. If a stub remains, its existing A3 body/Status checks still
apply. This replaces earlier rules requiring permanent parent ADRs, new sibling ADRs
for every amendment, or a prohibition on slimming accepted decisions.

## Grounds

The September 8 review found 149 dated ADR files and 394,981 words at the revision
above. The August 8 full/light rule still required a record for routine decisions,
and the stub/body convention kept historical files on disk. Both encouraged growth.
Keeping history verbatim in the live corpus was rejected because it competes with
current instructions; deleting by age or citation count was rejected because prose
can hold live authority or executable inputs. Consolidation requires more migration
work but reduces ongoing reading and duplicate ownership.

The former light-share target and its November 8 omitted-apparatus review are
**retired by this policy replacement**, not marked passed. Their implied-SR example
remains historical evidence that a short record can still change a consequential
gate. Brevity never supplies approval or relaxes the underlying evidence standard.

## Current owner

- [Operational rules](../operational_rules.md): fact ownership, source reads,
  frozen-evidence protection and retention checks.
- [ADR template](../../.claude/skills/brief-authoring/references/adr.md): current
  form and graph/retrieval mechanics; the skill checker validates this form.
- [Tombstone index](TOMBSTONES.md): retrieval of removed records.
- [STATE](../../STATE.md): pointers to actual outstanding obligations. Moving an
  obligation there must also preserve its scanner/reader coverage where applicable.

Verification: `python scripts/check_adr_graph.py` and
`python .claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-08-08-adr-ceremony-tiering.md --type adr`.
Mechanical form checks do not establish semantic equivalence or ratification.
