# `docs/adr/` — current architectural decisions

Open [INDEX.md](INDEX.md) for current decisions and [TOMBSTONES.md](TOMBSTONES.md)
for removed records. Generate the index with
`python scripts/check_adr_graph.py --regenerate-index`; do not hand-edit it.

ADRs are a selective record, not a log of every decision. Use a new one only for
durable architecture/governance rationale or authority that an existing owner cannot
hold clearly. Specifications, campaign records, plans and PRs can own decisions.
[Admission, retention and concise form](2026-08-08-adr-ceremony-tiering.md) govern
authoring, revision and removal; [the template](../../.claude/skills/brief-authoring/references/adr.md)
describes the graph header and verification. Historical full/light forms remain
supported. Neither a citation nor Accepted status makes a file permanent.
