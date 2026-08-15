# Session-log roll-off — design

**Date:** 2026-06-27
**Status:** design (approved via brainstorming 2026-06-27)
**Scope:** governance/ops tooling. No core / lock / allocation / dd_protection / Pine / data change.

## Problem

`docs/SESSIONS.md` is append-only, newest-first, ~105 entries each carrying ~5 dense
fields. Two of the fields (`Open / next`, `Live-ops state`) go stale within ~2–6 weeks;
the durable atoms already live in `MEMORY.md` and git history. The file grows unbounded,
diluting the "read the top entry's Open/next" purpose stated in its own header.

## Decision (hybrid; operator-selected)

- **Live window = newest N=20 entries** (count-based) stay in `SESSIONS.md`.
- **Roll older entries** into **quarterly archive files** under
  `docs/ltm/notes/archive/sessions/SESSIONS-YYYY-Qn.md`, routed by each entry's own
  date. Entry bytes are preserved except for a deterministic rewrite of relative
  Markdown-link targets from the original `docs/` base to the archive directory.
- **Archive Index** — a regenerated one-line-per-entry table at the **bottom of
  `SESSIONS.md`** (single-file top-to-bottom scan: recent full entries → index).
- **Sentinel size-flag** nags (report-only) when the file exceeds the window.

Approaches considered and rejected (brainstorming): git-as-archive-only (history exists
but isn't scannable); compact-on-roll-off (lossy vs git, which is already lossless).

## Components

### 1. `scripts/roll_sessions.py` (governance; add to REPO_MAP §2.1)

Parse `docs/SESSIONS.md` into three parts:
- **header** = everything before the first real entry heading (preserved byte-for-byte;
  it contains a fenced `## YYYY-MM-DD — <focus title>` *template* line that is NOT an entry).
- **entries** = blocks starting at a real `## YYYY-MM-DD — …` heading
  (newest-first), each running to the next entry heading; only the exact
  structural `\n\n---\n\n` separator is removed during parsing. Entry trailing
  whitespace and internal horizontal rules are content and remain untouched.
- **managed index block** = between `<!-- ARCHIVE-INDEX:START -->` / `<!-- …:END -->`
  markers (stripped before re-parse so it never double-nests).

Behavior:
- `keep = entries[:keep_n]`, `roll = entries[keep_n:]` (default `keep_n=20`).
- Each rolled entry → `docs/ltm/notes/archive/sessions/SESSIONS-<YYYY>-Q<n>.md` (quarter from the
  entry date), newest-first, **dedup by exact heading line** (idempotent append; file created
  with a one-line header if missing). Relative Markdown links are rebased with
  POSIX path semantics; absolute URLs, root links, and in-page anchors are unchanged.
- Rewrite `SESSIONS.md` = header + `keep` (joined by `\n\n---\n\n`) + a **regenerated**
  Archive-Index block whose rows are built by scanning **all** archive files' headings
  (`date · title · relative link`), newest-first. Rebuilding from the archive dir (not
  appending) makes the index idempotent and self-healing.
- CLI: `--keep N` (default 20), `--dry-run` (print keep/roll counts + target files, write
  nothing), `--root PATH`. `--regenerate-from-git REF` rebuilds archives from
  the unrolled `REF:docs/SESSIONS.md` backstop, then refreshes the live index;
  this is the repair path for an earlier lossy/incorrect roll. Always exit 0 on
  a successful operation.

### 2. `ops/sentinel/scan.py :: sessions_scan(root, max_entries=20)`

Counts real `## YYYY-MM-DD` entry headings in `docs/SESSIONS.md` (excluding the fenced
template line in the header block). If `> max_entries`, emit one
`Finding(category="hygiene", routing="Forward", id="SESSIONS-over-window",
source="docs/SESSIONS.md", next_step="run python scripts/roll_sessions.py")`.
Fail-open (missing file → `[]`). Wired into the `__main__.py` composition alongside the
existing scans.

### 3. Tests — `tests/test_roll_sessions.py` (+ a `sessions_scan` case)

- keep/roll split at the boundary (21 entries, keep 20 → 1 rolled).
- quarter routing across Q1/Q2 → correct archive files.
- **idempotent re-run** (second run is a no-op; files byte-identical).
- index regenerated with correct rows + markers present.
- `--dry-run` writes nothing.
- header block (incl. the fenced template) preserved byte-for-byte.
- every entry's parsed content preserved exactly apart from the documented
  relative-link rewrite, including trailing spaces.
- legacy archive migration rewrites links once, adds the format note, and is
  byte-idempotent thereafter.
- `≤ keep_n` entries → no-op.
- `sessions_scan`: fires over threshold, silent at/under, fail-open on missing file,
  ignores the fenced template heading.

## Conventions / boundaries

- Archive dir `docs/ltm/notes/archive/sessions/` mirrors the existing `docs/ltm/notes/archive/notion/`.
- `roll_sessions.py` classified **governance** in REPO_MAP §2.1.
- **First roll executed 2026-07-10**; legacy archive migration to rebased links
  is automatic and idempotent.
- Idempotent + dry-run-first → safe; git history is the lossless backstop regardless.
