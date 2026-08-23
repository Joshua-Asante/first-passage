# `docs/ltm/` — long-term memory (search-excluded)

Cursor indexing and default `rg` **exclude** this tree
(`.rgignore` / `.cursorindexingignore`). It is git-tracked.
An empty Grep is not evidence of absence — use
`rg --no-ignore` or Read-by-path.

Lookup order: [`lab/CATALOG.md`](../../lab/CATALOG.md) →
[`docs/briefs/INDEX.md`](../briefs/INDEX.md) → this tree →
historical retrieval. `pre-prune-2026-08-08` is **not a tag on this public
clone** — `git show pre-prune-2026-08-08:<path>` works only in the private
archive; on this tree use `git log --follow -- <path>` or that archive.

| On this public tree today | Job |
|---|---|
| [`adr/`](adr/) | Cold ADR stubs (superseded / retired) |
| [`briefs/rnd-pipeline/discovery-campaign-template.md`](briefs/rnd-pipeline/discovery-campaign-template.md) | Campaign-default template owner |
| [`notes/2026-08-23-substrate-phase-6-completion.md`](notes/2026-08-23-substrate-phase-6-completion.md) | Substrate Phase 6 docs + §10 checklist (destroy-copy still operator-gated) |

Most pre-prune LTM (rolled SESSIONS, closed-brief bodies, notes) is
**not** on this clone — retrieve via `git show` / the private archive.
Do not recreate the evicted corpus here.
