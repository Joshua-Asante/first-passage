# ADR — [decision title]

**Status:** `Proposed` — record the actual approval and effective scope when accepted
**Decision date:** YYYY-MM-DD
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Format:** concise

## Decision

[State the durable architecture, governance or authority choice, its scope and
effective behavior. Use a new ADR only when the rationale guides future work and
an existing owner cannot hold it clearly. Importance or approval alone is insufficient.
A Proposed branch is not permission; routine work belongs in its PR or current owner.]

## Grounds

[Name the current source evidence, why the choice is necessary and the actual
alternative/tradeoff. For risk-sensitive claims, read production sources before
authoring and retain path/verification anchors. Do not manufacture a falsifier for
an operator scope election or a quarterly review for a completed maintenance act.]

## Current owner

[Link the operating contract, implementation or campaign that owns present procedure
and evidence. This ADR may own the durable rationale or scope itself. Avoid copying
the runbook or creating another wrapper.]

Add evidence, constraints, reversal conditions and verification commands when they
change a future action. Do not pad the three sections into a fixed apparatus.

## Authoring and revision guidance

Policy: [consequential-decision retention](../../../../docs/adr/2026-08-08-adr-ceremony-tiering.md).
Filename: `docs/adr/YYYY-MM-DD-slug.md`; the filename is the identifier. Search for
an existing owner before creating a sibling. Existing full/light records retain
their own validation contracts; concise is the form for new or substantively
consolidated ADRs, not a new category of risk.

Accepted effective text may be revised after the required decision is approved.
Record the date, changed scope and immutable previous revision. Keep Proposed
material explicitly separate. Frozen research preregistrations, lock artifacts,
verdict logic and evidence do not become editable merely by linking this policy.
An unimplemented decision stays distinguishable from an implemented control.

## Graph header and removal

Keep header fields before the first `##` heading or `---` separator. The parser
ignores Status declarations inside later amendments. Tokens are `Proposed`,
`Accepted`, `Superseded`, `Withdrawn`, `Retired`; partial supersession remains
`Accepted` and uses `Superseded-in-part-by`.

For a new successor, use `Supersedes: YYYY-MM-DD-slug.md full` or `in part — scope`.
Repeat the field for multiple targets. Once Accepted, a surviving predecessor needs
the corresponding reverse edge. A partial non-ADR replacement can use
`Superseded-in-part-by: event:<id> — scope`; do not claim a new ADR exists.

Before removing a file, read its full body/amendments, map current clauses and
obligations, migrate actual consumers, verify incoming file/fragment/section routes,
and prove every removed blob remains retrievable. Add original path, commit/blob,
disposition and current owner to `docs/adr/TOMBSTONES.md`. Remove a legacy stub/body
pair together when both are cleared. A2 recognizes tombstoned predecessor names;
A4 checks bodies still present, not deleted records.

If keeping the legacy cold form, `scripts/retire_adr.py` remains available: hot
stub with `Body:` pointer, matching cold Status in the LTM body, and reverse edge
for supersession. A3 still validates that form. The helper is not a required
intermediate step before verified deletion; never weaken its safety checks to
avoid migrating a consumer.

## Verification

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py <adr.md> --type adr
python scripts/check_adr_graph.py --regenerate-index
python scripts/check_adr_graph.py
```

The canonical skill checker validates concise Decision/Grounds/Current owner;
the repo-side subset reports `NOT CHECKED` for this form. Neither checker proves
the truth, completeness or approval of a decision. Run affected negative-case
tests and required gates for the actual change; deletion work also runs the
repository-required test suites. Preserve meaningful checks, not historical prose
fixtures. An obligation moved out of an ADR needs its reader migrated too.
