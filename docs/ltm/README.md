# `docs/ltm/` — long-term memory (search-excluded)

Default `rg` **excludes** this tree (`.rgignore`, sole owner of that
exclusion since the 2026-09-15 Cursor retirement). It is git-tracked.
An empty Grep is not evidence of absence — use
`rg --no-ignore` or Read-by-path.

Lookup order: [`lab/CATALOG.md`](../../lab/CATALOG.md) →
[`docs/briefs/INDEX.md`](../briefs/INDEX.md) → this tree →
historical retrieval. `pre-prune-2026-08-08` is **not a tag on this public
clone** — `git show pre-prune-2026-08-08:<path>` works only in the private
archive; on this tree use `git log --follow -- <path>` or that archive.

**2026-09-06 tracked-file reduction:** 1,542 paths left this tree. Their
study rows stay in [`lab/CATALOG.md`](../../lab/CATALOG.md) (Archived table,
body cell = archive URL) via [`lab/ARCHIVED.json`](../../lab/ARCHIVED.json),
which records every removed path's baseline blob and the preservation commit
in `first-passage-archive` (branch `archive/preserve-2026-09-06`). Retrieval:
`git show 2d40dbeb56c167844cab5136742d70787835f8e2:<path>` here, or that
commit in the archive. Owner:
[reduction ADR](../adr/2026-09-06-tracked-file-reduction-prune.md).

| On this public tree today | Job |
|---|---|
| [`adr/`](adr/) | Cold ADR stubs (superseded / retired) |
| [`briefs/rnd-pipeline/discovery-campaign-template.md`](briefs/rnd-pipeline/discovery-campaign-template.md) | Campaign-default template owner |
| [`notes/2026-08-23-substrate-phase-6-completion.md`](notes/2026-08-23-substrate-phase-6-completion.md) | Substrate Phase 6 docs + §10 checklist (destroy-copy still operator-gated) |
| [`notes/archive/state/STATE-decision-index-pre-2026-08-23.md`](notes/archive/state/STATE-decision-index-pre-2026-08-23.md) | STATE executed-decision index older than keep-15 (P8) |

## Removal batches

One row per removal PR ([cleanup spec D3](../superpowers/specs/2026-10-28-org-cleanup-programme-spec.md)).
Retrieve any listed path with `git show <parent>:<path>`.

| Merge | Pre-removal parent | Paths | Retrieval | Path list |
|---|---|---|---|---|
| #971 merge commit | `128989543d94d38d0962ee2d3c37eac7384efa8a` | 16 | `git show 128989543d94d38d0962ee2d3c37eac7384efa8a:<path>` | `docs/notes/2026-09-15-account-close-calculation-component.md`<br>`docs/notes/2026-09-15-account-close-evidence-component.md`<br>`docs/notes/2026-09-15-tradeify-packet1-intake-progress.md`<br>`docs/notes/2026-09-16-production-capability-inquiries.md`<br>`docs/notes/2026-09-16-tradeify-production-feasibility-decision.md`<br>`docs/notes/2026-09-24-t10-step4-representative-measurement.md`<br>`docs/notes/2026-09-25-tradeify-assurance-review.md`<br>`docs/notes/2026-09-26-ub8-availability-comparison.md`<br>`docs/notes/2026-09-27-h8c-omission-incident-evidence.md`<br>`docs/notes/2026-09-27-s5-owner-text-and-rc6-draft.md`<br>`docs/notes/2026-10-02-dot-deployment-responsibility.md`<br>`docs/notes/2026-10-02-openai-dots-portfolio-deployment-brainstorm.md`<br>`docs/notes/2026-10-02-tradeify-b4-observed-pilot-PROPOSED.md`<br>`docs/notes/2026-10-02-tradeify-q7-d3-recovery-PROPOSED.md`<br>`docs/notes/2026-10-04-feed-overlap-and-october-exception-proposals.md`<br>`docs/notes/2026-10-05-four-firm-remc-616-open-items-sheet.md` |
| this PR's merge commit | `cfe5be6ec581fccfad0ca7a4a2ad104569db6c7a` | 8 | `git show cfe5be6ec581fccfad0ca7a4a2ad104569db6c7a:<path>` | `lab/databento_fetch/README.md`<br>`lab/databento_fetch/__init__.py`<br>`lab/databento_fetch/db_fetch.py`<br>`ops/global_market_map/README.md`<br>`ops/global_market_map/registry.json`<br>`tests/test_db_fetch_datecap.py`<br>`tests/test_db_fetch_pd1_pd2.py`<br>`tests/ops/test_global_market_map_registry.py` |
| this PR's merge commit | `066d22b250cff97785b6cf142aacf84e2d7e1301` | 5 | `git show 066d22b250cff97785b6cf142aacf84e2d7e1301:<path>`, or archive branch `archive/c1-retire-batch1` commit `44e14f1a9171fa5c2335a4aeb0aba7b30dd9d86f` (kept unmerged, same blobs; do not prune) | `deploy/c1_rail_personal/calendar_binding.json`<br>`ops/c1_rail/instance_binding.py`<br>`ops/c1_rail/personal_calendar_binding.py`<br>`tests/ops/test_instance_binding.py`<br>`tests/ops/test_personal_calendar_binding.py` |

Most pre-prune LTM (rolled SESSIONS, closed-brief bodies, notes) is
**not** on this clone — retrieve via `git show` / the private archive.
Do not recreate the evicted corpus here.
