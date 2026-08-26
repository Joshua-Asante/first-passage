# LESSONS_INDEX.jsonl — the consolidated, queryable lesson registry

**What this is.** One JSON object per line (`docs/methodology/LESSONS_INDEX.jsonl`),
covering every E/M/F-class lesson in [`execution_lessons.md`](lessons/execution_lessons.md)
and [`methodology_lessons.md`](lessons/methodology_lessons.md), the two standalone
`docs/lessons/*.md` captures, and every external `feedback_*` / `lesson_*` / `project_*`
name found cited by name anywhere in this repo.

**Why it exists.** Found during the 2026-08-26 memory-architecture audit: this repo's
institutional memory of its own mistakes was split across two disconnected systems — a
git-tracked, structured in-repo registry, and ~90 more lesson names that exist *only* in
an external Claude-memory / Notion store this checkout cannot read. That split is not
cosmetic — it directly caused a real incident: `M-25`'s lesson-ID collision with the
canonical registry's real `M-19` sat undetected for 40 days specifically because the two
stores had no shared, queryable ID space. `LESSONS_INDEX.jsonl` is that shared space.

## Two kinds of entry

Every entry carries `"content_verified": true|false`:

- **`content_verified: true` — a "full" entry.** Transcribed directly from a primary
  source in this repo by a full read of the source file (not a subagent's paraphrase,
  not copied from a prior research pass). `full_ref` names the exact file + anchor.
  `one_line_lesson`, `cost_if_repeated`, `trigger_globs`, `trigger_keywords` are all
  populated and trustworthy.

- **`content_verified: false` — a "stub" entry.** The name is real (confirmed by a
  `git grep` run at generation time — `citing_files` lists where it's actually cited),
  but its *content* lives only in the external store. `title`, `one_line_lesson`,
  `cost_if_repeated` are deliberately `null`. **Do not infer content from the name.**
  A plausible-sounding guess at what `lesson_dsr_floor_k_governed` probably says is
  exactly the confabulation-under-plausible-cover failure class this index exists to
  prevent — if you need the content, it isn't here yet.

## Schema

| Field | Meaning |
|---|---|
| `id` | Unique key. Full entries use the registry's own ID (`M-21`, `E1`, `F-1`, the standalone-file slug). Stub entries use `<prefix>_<name>` (e.g. `lesson_dsr_floor_k_governed`) — the prefix is the external-pointer class, matching `feedback_*` / `lesson_*` / `project_*` convention. |
| `class` | `E` \| `M` \| `F` \| `standalone` \| `feedback` \| `lesson` \| `project`. |
| `status` | `CANDIDATE` \| `PROMOTED` \| `DORMANT` \| `external-unmigrated`. |
| `status_note` | Free text: dates, promotion/demotion detail, provenance caveats. |
| `title`, `one_line_lesson`, `cost_if_repeated` | `null` on stub entries. |
| `trigger_globs`, `trigger_keywords` | Rough matchers a future forcing-hook could use to surface this lesson when a touched file/keyword looks relevant. Empty on stub entries (no content to derive triggers from). |
| `full_ref` | Where the real content lives — a repo path + anchor for full entries, `"external ..."` for stubs. |
| `siblings` | Other IDs in this index this lesson interlocks with, per the source's own cross-references. |
| `memory_twin` | For a handful of full entries, the external-store name that's this lesson's memory-side counterpart (e.g. `M-Q-REGIME-1`'s twin is `project_2024_regime_shift_accumulating_signal`). |
| `citing_files` | Stub entries only — real files that cite this name, from a `git grep` run at generation time. |
| `last_verified_date` | When the entry's content (or, for stubs, its citation) was last confirmed against the live tree. |

## How to use this

**Query it like any JSONL file** — `grep`, `jq`, or read it whole (115 lines, small).
There is no query CLI yet; this is the consolidation step. A forcing-hook that surfaces
a relevant entry automatically when a matching file/keyword is touched is a natural
follow-up (`trigger_globs`/`trigger_keywords` are shaped for exactly that), not yet built.

**Before authoring a new lesson**, grep this file for the topic first — a stub entry
with a citing file may point you at prior (external) discussion worth chasing down
before re-deriving from scratch.

**When a stub entry's content becomes known** (the external store is consulted, or the
name gets cited again and someone migrates it): promote it to a full entry — populate
`title`/`one_line_lesson`/`cost_if_repeated`/`trigger_*`, set `content_verified: true`,
update `full_ref` to point at wherever the migrated content now lives (per
`methodology_lessons.md`'s own Migration-plan convention — the migrated lesson gets a
real `M-N`/`E-N` slot in the canonical registry, and this index's `full_ref` follows it
there). Do not delete the stub row's history — this file is regenerated wholesale by
`scripts/_build_lessons_index.py` (a one-shot generator, not a standing gate); re-run it
and diff, don't hand-patch entries out of sync with the generator's source data.

## What this does NOT do (yet)

- **No mechanical freshness check.** Nothing currently verifies this index stays in
  sync with `methodology_lessons.md`/`execution_lessons.md` as new lessons are added —
  it was generated once, by hand, 2026-08-26. Re-run the generator when the source
  registries change meaningfully.
- **No forcing hook.** Nothing surfaces a relevant entry automatically when a session
  touches a matching file. `trigger_globs`/`trigger_keywords` exist for this purpose;
  wiring a `PostToolUse` hook that consults them is scoped but not built.
- **No content for the 83 stub entries.** Those need either a real migration (someone
  reads the external store and writes the content here) or they stay pointer-only
  indefinitely — both are honest outcomes; a fabricated middle ground is not.
