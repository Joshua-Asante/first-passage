# Notion estate (frozen workspace) — SUBTRACT-complete

**Class:** (c) standing exploration · **Standing:** SUBTRACT (ruling + mechanical follow-up
recorded)
**Test applied:** residual function unowned and unneeded as an open decision — the retirement
ADR's own Phase 3 (`docs/adr/2026-06-12-notion-surface-retirement.md`) had sat undecided through
both the 2026-07-01 and 2026-08-08 quarterly audits, with its own §4 H held throughout (no
workflow has required a Notion write; no load-bearing fact has surfaced Notion-only since Phase 2
reported DONE).

**Ruling:** operator elects **cold archival** (not workspace deletion) as the Phase-3 sub-option,
per this GSUB-1 disposition.

**Mechanical follow-up (2026-08-10):** repo record landed — Addendum 2026-08-10 on
[`docs/adr/2026-06-12-notion-surface-retirement.md`](../adr/2026-06-12-notion-surface-retirement.md)
(PR #709 / branch `cursor/notion-phase3-cold-archive-e902`). Operator GO:
*"cold archive, proceed with next steps"*. Workspace **not** deleted. Notion UI hub-Archive
clicks remain operator-owned (recording session had no Notion MCP). Redirect map + ADR INDEX
gloss updated in the same pass.

**Residuals:** Phase-2 migration artifacts and
[`docs/governance/notion-redirect-map.md`](../governance/notion-redirect-map.md) stand; LTM
Notion export bodies recover via `pre-prune-2026-08-08`. ⚠ Correction 2026-08-31: that tag is
**private-archive-only** — not resolvable on this public clone. `git log --follow -- <path>` only
helps for content that exists somewhere in this clone's own tracked history (a file the public
"Initial public release" commit carried and later modified/renamed); per
[`docs/ltm/README.md`](../ltm/README.md), "most pre-prune LTM ... is **not** on this clone," and
these Notion export bodies are not present here (confirmed: no `docs/ltm/notes/archive/notion/`
directory exists on this tree) — for this specific residual, the private archive is the only
working recovery path, not an alternative among several. Behavioral-archive CSV native export
remains `DONE_WITH_CONCERNS` (accepted on the 2026-08-10 GO).

**Ratified:** 2026-08-09 (GSUB-1 Phase 3) · **Follow-up recorded:** 2026-08-10
**Source:** [`GSUB-1 inventory`](../briefs/GSUB-1-inventory-and-dispositions.md) row c6
