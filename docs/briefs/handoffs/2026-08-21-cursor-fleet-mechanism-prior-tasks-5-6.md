# Cursor Fleet Handoff — mechanism-prior Tasks 5+6 (ingest CLI + corpus extraction)

**Date:** 2026-08-21
**Parent session:** Claude Code
**Spawn target:** Cursor (2-packet fleet — `.claude/skills/cursor-fleet/SKILL.md`, per
`docs/adr/2026-07-14-cc-cursor-surface-allocation.md` §0.5 Cursor variant)
**Repo:** `first-passage`
**Brief type:** Cursor fleet handoff (2 packets)
**Parent question:** N/A — executes Tasks 5+6 of
`docs/superpowers/plans/2026-08-20-cross-campaign-mechanism-prior.md` (design:
`docs/superpowers/specs/2026-08-20-cross-campaign-mechanism-prior-design.md`)
**Authority:** Joshua (CEO), "move on to tasks 5/6". No commit/merge without operator go.

**Scope note (why this is a real fleet, not N=1):** two genuinely independent packets with
disjoint file footprints — Task 5 (`mechanism_prior_ingest.py` + its test) and Task 6
(`mechanism_prior_extract.py` + its test). Neither imports from the other. Both are fully
frozen-spec (complete code already written in the plan, TDD steps included) — no judgment
calls left for either worker. Both depend only on Task 1/2 modules already merged to `main`
(`mechanism_prior_schema.py`, `mechanism_prior_store.py`, `tests/conftest.py`'s
`valid_tag_record` fixture) — confirmed present via `git log --oneline origin/main -- lab/research_utils/` this session. Neither touches a locked surface (test 1 disqualifiers:
`core/` anchor code, Pine, ADRs/pre-regs/CLAUDE.md/STATE.md — none apply, both packets are
scoped entirely to `lab/research_utils/` + `tests/`).

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any packet work, both workers)

Each worker: read and report contents in your first response, before writing any code.

- `docs/superpowers/plans/2026-08-20-cross-campaign-mechanism-prior.md` — report your own
  packet's Task section (5 or 6, per your assignment below) in full. This is your frozen
  spec; the code in it is complete and tested, not a sketch.
- `lab/research_utils/mechanism_prior_schema.py` — report full contents (this is what your
  packet imports; confirm the function/exception names your Task section cites actually
  match what's on disk).
- `lab/research_utils/mechanism_prior_store.py` — report full contents (Task 5 only —
  imports `append_record`, `DEFAULT_STORE_PATH` from here; Task 6 does not need this file,
  report `N/A — Task 6 has no dependency on the store module`).
- `tests/conftest.py` — report the `valid_tag_record` fixture only (the last ~28 lines).
  Confirm it exists and matches the signature your Task section's tests assume.
- `git log -1 --format='%h %ci' -- lab/research_utils/mechanism_prior_schema.py lab/research_utils/mechanism_prior_store.py tests/conftest.py` —
  report the anchor.

After Phase 0: post the read-report, then proceed directly to your packet appendix below —
both packets are frozen verbatim, so there is no ambiguity to wait on (§0.5 is empty).

---

## §0.75 — Local-only dependency check (required, Spawn target is Cursor)

- **Gitignored vendor data:** neither packet touches `core/data/tv_exports/**`,
  `core/data/bar_data/**`, or `core/data/external/**`. **N/A.**
- **Secrets/API keys:** none needed — both packets are pure Python, stdlib + already-vendored
  test deps only. **N/A.**

---

## §0.5 — Clarifying questions

None. Both packets are frozen-spec (complete code in the plan). If Phase 0 shows the cited
dependency functions/fixtures have drifted from what your Task section assumes, that is a
`NEEDS_CONTEXT` bounce quoting the actual current signature — never a judgment call about
how to adapt.

---

## §1 — Context

`docs/superpowers/plans/2026-08-20-cross-campaign-mechanism-prior.md` is an 8-task plan for a
read-only, disclosure-only cross-campaign mechanism prior (weighted survival-rate report over
First Passage's closed-campaign history). Tasks 1–4 (schema, store, Wilson interval,
report/CLI) are merged to `main` (PR #74). Tasks 5–6 are the next two, independent of each
other, both prerequisites for Task 7 (the one-time tagging pass, which stays local/Claude —
not part of this fleet).

**What each worker is being asked to produce:** exactly the file pair named in its packet
appendix below, implemented exactly as the plan's Task section specifies, TDD order followed
(write failing tests → confirm fail → implement → confirm pass → commit).

**What workers are NOT being asked to do:** touch any file outside their own packet's two
files; touch `docs/SESSIONS.md`, `STATE.md`, the plan file, or this handoff brief (orchestrator-
reserved); run or scope Task 7; deviate from the plan's code even if a "better" approach
occurs to you — this is frozen-spec, not open design (if you believe the plan is wrong, return
`BLOCKED — plan-itself-wrong`, do not silently improve it).

---

## §4 — Falsifiable hypothesis

N/A — no statistical hypothesis under test; executing Tasks 5+6 of an already-approved
implementation plan, not a Pre-Q investigation. This handoff's own accept/reject clause
instead: **ACCEPT** (merge) a packet if it returns `DONE` with its named test suite green and
its diff scoped to exactly its two named files. **REJECT** the dispatch for that packet (fall
back to Claude solo, per `cursor-fleet`'s own rule) if it returns `NEEDS_CONTEXT` or `BLOCKED`
twice in a row — two bounces means the spec wasn't actually freezable.

---

## Claim manifest

| Packet | Task | Branch | Files | Status |
|---|---|---|---|---|
| A | 5 — ingest CLI | `cursor/mechanism-prior-p1` | `lab/research_utils/mechanism_prior_ingest.py`, `tests/test_mechanism_prior_ingest.py` | **MERGED** 2026-08-21T15:04:12Z (PR [#83](https://github.com/Joshua-Asante/first-passage/pull/83)) — clean first attempt, 6/6 tests |
| B | 6 — corpus extraction | `cursor/mechanism-prior-p2` | `lab/research_utils/mechanism_prior_extract.py`, `tests/test_mechanism_prior_extract.py` | **MERGED** 2026-08-21T15:19:50Z (PR [#84](https://github.com/Joshua-Asante/first-passage/pull/84)) — first attempt correctly bounced `NEEDS_CONTEXT` (registry file reorganized upstream since Task 6 was scoped: 6 `##` sections now, not 1; corrected + re-verified against real data before re-dispatch), second attempt clean, 8/8 tests |

Orchestrator (this session) owns this table. Before any session dispatches into this area,
check this table's Status column first.

---

## Packet A — Task 5 (ingest CLI)

**Phase-0 staleness check (no-op condition — run before dispatch AND re-check at dispatch
time, not just now):**
```bash
test -f lab/research_utils/mechanism_prior_ingest.py && echo "ALREADY EXISTS -- return DONE citing the commit that added it, do not re-implement" || echo "NOT YET BUILT -- proceed"
git fetch origin main && git log --oneline origin/main --since="24 hours ago" -- lab/research_utils/ tests/
gh pr list --state open --search "mechanism_prior_ingest"
```

**Frozen scope:** Task 5 in `docs/superpowers/plans/2026-08-20-cross-campaign-mechanism-prior.md`
(section starts `### Task 5: Batch validator/ingest CLI`), read in full per §0 above. Two files,
exact code given (5 TDD steps). No deviation.

**Forbidden moves:** no writes outside `lab/research_utils/mechanism_prior_ingest.py` and
`tests/test_mechanism_prior_ingest.py`; no touching `mechanism_prior_extract.py` (Packet B's
file — even if you think ingest and extract "should" share something, they don't per the
frozen spec); no touching `mechanism_prior_schema.py` or `mechanism_prior_store.py` (already
merged, read-only dependencies); no touching `tests/conftest.py`.

**Return contract:** branch `cursor/mechanism-prior-p1`, PR against `main`, `pytest
tests/test_mechanism_prior_ingest.py -v` green (6 tests per the plan), four-state status
(`DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED`) per §6 below.

---

## Packet B — Task 6 (corpus extraction)

**Phase-0 staleness check (no-op condition — run before dispatch AND re-check at dispatch
time, not just now):**
```bash
test -f lab/research_utils/mechanism_prior_extract.py && echo "ALREADY EXISTS -- return DONE citing the commit that added it, do not re-implement" || echo "NOT YET BUILT -- proceed"
git fetch origin main && git log --oneline origin/main --since="24 hours ago" -- lab/research_utils/ tests/ docs/rejected_candidates.md
gh pr list --state open --search "mechanism_prior_extract"
```

**Frozen scope:** Task 6 in `docs/superpowers/plans/2026-08-20-cross-campaign-mechanism-prior.md`
(section starts `### Task 6: Split rejected_candidates.md into taggable entries`), read in
full per §0 above. Two files, exact code given (5 TDD steps). Note the plan's own Rule-0 note
in that section (verified against the real file: 117 entries under one `## Entries` heading,
demarcated by `### ` headings — the code only needs that structure, nothing more elaborate).
No deviation.

**Forbidden moves:** no writes outside `lab/research_utils/mechanism_prior_extract.py` and
`tests/test_mechanism_prior_extract.py`; no touching `mechanism_prior_ingest.py` (Packet A's
file); no touching `docs/rejected_candidates.md` itself (read-only source, never written by
this packet); no attempting to also implement Task 7's tagging pass — this packet stops at
splitting/loading raw entries, it does not classify or tag anything.

**Return contract:** branch `cursor/mechanism-prior-p2`, PR against `main`, `pytest
tests/test_mechanism_prior_extract.py -v` green (6 tests per the plan), four-state status
per §6 below.

---

## §5 — Fleet-level forbidden moves (both packets)

- Neither packet writes to `docs/SESSIONS.md`, `STATE.md`, this handoff brief, or the plan
  file — orchestrator-reserved, integration-commit only.
- Neither packet branches from the other's branch — both branch from current `origin/main`.
- Neither packet touches a file the claim manifest doesn't name for it.
- No commit/merge without operator go, per this brief's Authority line.

---

## §6 — Gate + status return taxonomy

Each worker reports back with EXACTLY one of these four statuses:

| Status | Meaning | Parent action |
|---|---|---|
| `DONE` | Task section fully implemented, tests green, no scope creep. | Orchestrator reviews diff + gate output, merges in dependency order. |
| `DONE_WITH_CONCERNS` | Complete but flags a doubt. | Orchestrator adjudicates before merge. |
| `NEEDS_CONTEXT` | A dependency (schema/store/fixture) has drifted from what the Task section assumes. | Orchestrator re-anchors, one re-dispatch. |
| `BLOCKED — <sub-case>` | Structural obstruction, or the plan itself looks wrong. | Orchestrator escalates to Joshua; two bounces means the spec wasn't freezable — falls back to Claude solo. |

**Closure report format:**
```
Status: <DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED — <sub-case>>
Branch: cursor/mechanism-prior-p<N>
Tests: <command run> -> <result>
Diffs (files touched): <list -- must match packet's named files exactly>
Concerns (if any): <list>
```

---

## §10 — Audit hooks (orchestrator-side, after both packets return)

```bash
# Diff touches exactly the packet's footprint, nothing else
git diff origin/main..cursor/mechanism-prior-p1 --name-only
# Expected: exactly lab/research_utils/mechanism_prior_ingest.py, tests/test_mechanism_prior_ingest.py

git diff origin/main..cursor/mechanism-prior-p2 --name-only
# Expected: exactly lab/research_utils/mechanism_prior_extract.py, tests/test_mechanism_prior_extract.py

# Both test suites green
pytest tests/test_mechanism_prior_ingest.py tests/test_mechanism_prior_extract.py -v
# Expected: 12 passed (6 + 6)

# Claim manifest updated to MERGED after each merge (orchestrator does this, not workers)
grep -A3 "Claim manifest" docs/briefs/handoffs/2026-08-21-cursor-fleet-mechanism-prior-tasks-5-6.md
```

---

## Verification (parent-side, before declaring this handoff complete)

```bash
$ python /path/to/brief-authoring/scripts/check_brief.py docs/briefs/handoffs/2026-08-21-cursor-fleet-mechanism-prior-tasks-5-6.md --type cc_handoff
# Expected: all 6 general checks + checks 7-10 PASS

$ grep -E "^Status: (DONE|DONE_WITH_CONCERNS|NEEDS_CONTEXT|BLOCKED)" <each worker's return>
```

If either worker returns `NEEDS_CONTEXT` or `BLOCKED`, that packet is not complete;
re-dispatch per §6. The other packet is unaffected (disjoint footprints).
