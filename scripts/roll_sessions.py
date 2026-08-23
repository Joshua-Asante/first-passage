#!/usr/bin/env python3
"""roll_sessions.py — roll old docs/SESSIONS.md entries into quarterly archives.

Keeps the newest N entries (default 20) live in docs/SESSIONS.md; moves older
entries into docs/ltm/notes/archive/sessions/SESSIONS-YYYY-Qn.md (routed by each
entry's own date), preserving entry content while deterministically rebasing
relative Markdown links; and regenerates a managed Archive-Index block at the
bottom of SESSIONS.md, rebuilt by scanning the archive dir (idempotent).

Entry headings are real-date `## YYYY-MM-DD — title` lines; the file's fenced
`## YYYY-MM-DD — <focus title>` template uses literal YYYY, so the digit regex
below excludes it — no code-fence handling needed.

Design: docs/spec/2026-06-27-session-log-rolloff-design.md. Stdlib only;
classified governance in REPO_MAP §2.1. Idempotent; --dry-run writes nothing.
The git history is the lossless backstop regardless.

    python scripts/roll_sessions.py --dry-run     # show the plan, write nothing
    python scripts/roll_sessions.py               # roll (keep newest 20)
    python scripts/roll_sessions.py --keep 30
    python scripts/roll_sessions.py --regenerate-from-git HEAD
    python scripts/roll_sessions.py --next-label 2026-08-11  # next free same-day letter
    python scripts/roll_sessions.py --check-order             # labels + separators + order
    python scripts/roll_sessions.py --check-append-only       # freeze prior entry bodies
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import posixpath
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

SESSIONS_REL = "docs/SESSIONS.md"
ARCHIVE_REL = "docs/ltm/notes/archive/sessions"
INDEX_START = "<!-- ARCHIVE-INDEX:START -->"
INDEX_END = "<!-- ARCHIVE-INDEX:END -->"
ENTRY_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})[a-z]? ", re.M)
ENTRY_SEPARATOR = "\n\n---\n\n"
_MARKDOWN_LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)]+)(\))")
ARCHIVE_LINK_NOTE = (
    "Relative Markdown links are rebased from `docs/` to this archive directory; "
    "all other entry content is preserved."
)
# Same-clone reservation for --next-label. Lives under the process temp dir
# (not the repo) so it needs no .gitignore and cannot leak across machines —
# parallel cloud sessions still collide; this only stops a second invocation
# in the same clone from silently re-issuing a letter already handed out.
_CLAIM_DIR_PREFIX = "fp-session-label-claims-"
_CLAIM_TTL_SEC = 48 * 60 * 60
_HR_LINE_RE = re.compile(r"-{3,}$")


@dataclass(frozen=True)
class Entry:
    date: dt.date
    title: str
    text: str  # heading + body, no surrounding `---` dividers


# --------------------------------------------------------------------------
# Same-date ordering.
#
# `merge=union` keeps both sides' added lines but imposes no order, so two
# branches that each append at the top anchor land in an arbitrary order. Every
# such collision is SAME-DATE by construction — concurrent PRs land the same day
# — and every live entry in this file currently shares its date with 3-9 others.
# A date-only sort is therefore a near-total no-op on exactly the case that
# breaks, which is why `--reorder` never fixed it.
#
# The missing signal is which entry was AUTHORED later, and git already holds
# it: the commit that first ADDED a heading line is that entry's session. Author
# time (not commit time) survives rebase, so it is stable under the rebase-onto-
# main flow that produces these collisions in the first place.
_HEADING_ADDED_RE = re.compile(r"^\+(## \d{4}-\d{2}-\d{2} .+)$")
_NEWEST = dt.datetime.max.replace(tzinfo=dt.timezone.utc)
# Commits scanned when resolving a bounded window. Sessions add ~1 heading per
# commit, so this covers a window several times its size; `intro_times` escalates
# to a full scan only when a committed heading is still unresolved.
_LOG_SCAN_COMMITS = 40

# Entries from the top that union can disturb, and therefore the scope of both
# the order check and the reorder repair. See normalize() for why they match.
ORDER_WINDOW = 12


def _git(root: Path, *args: str) -> str | None:
    """Run a read-only git command. Returns None when git/history is unusable."""
    try:
        out = subprocess.run(
            ["git", *args], cwd=root, capture_output=True, text=True,
            encoding="utf-8", errors="replace", check=False,
        )
    except (OSError, ValueError):
        return None
    return out.stdout if out.returncode == 0 else None


def committed_headings(root: Path, ref: str = "HEAD") -> set[str]:
    """Heading lines present in ``ref``'s SESSIONS.md (default ``HEAD``).

    Anything absent here is new relative to ``ref`` — for the default ``HEAD``
    that means new in the working tree, so it needs no history lookup, which
    is what keeps the gate off the slow path on the common "I just wrote an
    entry" case. Other callers (the duplicate-label grandfather set) ask the
    same question against a different reference point, like the append-only
    base, so an unresolvable ``ref`` degrades the same way HEAD always did:
    empty set, never a guess.
    """
    doc = _git(root, "show", f"{ref}:{SESSIONS_REL}")
    if doc is None:
        return set()
    return {ln for ln in doc.splitlines() if ln.startswith("## ")}


def intro_times(root: Path, wanted: set[str]) -> dict[str, dt.datetime]:
    """Map heading line -> author time of the commit that first added it."""
    if not wanted:
        return {}
    for scan in (["-n", str(_LOG_SCAN_COMMITS)], []):   # bounded, then full
        found: dict[str, dt.datetime] = {}
        out = _git(root, "log", "--reverse", "--format=%x00%aI", "-p",
                   "--unified=0", *scan, "--", SESSIONS_REL)
        if out is None:
            return {}
        stamp: dt.datetime | None = None
        for line in out.splitlines():
            if line.startswith("\x00"):
                try:
                    stamp = dt.datetime.fromisoformat(line[1:].strip())
                except ValueError:
                    stamp = None
                continue
            m = _HEADING_ADDED_RE.match(line)
            if m and stamp is not None and m.group(1) in wanted:
                found.setdefault(m.group(1), stamp)
        if len(found) == len(wanted):
            return found
    return found


# Sentinel: committed heading with no resolvable +## intro line. Callers must
# fall back to file position for these — never datetime.min / inherit-prev,
# which silently sank merge-arriving same-day entries on 2026-08-08.
_FILEPOS = dt.datetime.min.replace(tzinfo=dt.timezone.utc)


def order_keys(root: Path, entries: list["Entry"]) -> dict[str, dt.datetime] | None:
    """Per-heading recency key, or None if history is unusable entirely.

    * absent from HEAD  -> new in the working tree, so newest. Ties among these
      are stable, keeping the on-disk order of entries written together.
    * dated by history  -> the author time of the commit that first added it.
    * committed but un-datable -> ``_FILEPOS`` sentinel. The caller keeps these
      in file order within their calendar-date group (never invents "oldest" by
      inheriting a neighbour's stamp — that stranded merge-arriving entries).

    None means git itself could not answer at all (no repo / no history), where
    the caller falls back to the old date-only sort rather than guessing.
    """
    heads = [e.text.splitlines()[0] for e in entries]
    known = committed_headings(root)
    if not known:
        return None
    resolved = intro_times(root, {h for h in heads if h in known})
    if not resolved and all(h in known for h in heads):
        # Every heading is committed but none are datable — date-only fallback.
        return None
    keys: dict[str, dt.datetime] = {}
    for h in heads:
        if h not in known:
            keys[h] = _NEWEST
        elif h in resolved:
            keys[h] = resolved[h]
        else:
            keys[h] = _FILEPOS
    return keys


def _reorder_entries(
    entries: list["Entry"], keys: dict[str, dt.datetime] | None,
) -> list["Entry"]:
    """Newest-first by calendar date; author-time within a date when complete.

    When any entry in a date group carries ``_FILEPOS`` (unresolved timestamp),
    that whole group keeps on-disk order — uncommitted (``_NEWEST``) rows still
    float to the top of the group. Never silently sink unresolved rows.
    """
    if keys is None:
        return sorted(entries, key=lambda e: e.date, reverse=True)

    indexed = list(enumerate(entries))

    def date_of(ie: tuple[int, Entry]) -> dt.date:
        return ie[1].date

    # Bucket by date (desc), reorder within each bucket.
    dates = sorted({e.date for e in entries}, reverse=True)
    out: list[Entry] = []
    for d in dates:
        group = [ie for ie in indexed if ie[1].date == d]
        heads = [ie[1].text.splitlines()[0] for ie in group]
        group_keys = [keys[h] for h in heads]
        if any(k is _FILEPOS for k in group_keys):
            # Incomplete timestamps: file-position fallback; uncommitted first.
            group.sort(
                key=lambda ie: (
                    0 if keys[ie[1].text.splitlines()[0]] is _NEWEST else 1,
                    ie[0],
                )
            )
        else:
            group.sort(
                key=lambda ie: keys[ie[1].text.splitlines()[0]],
                reverse=True,
            )
        out.extend(ie[1] for ie in group)
    return out


def quarter_of(d: dt.date) -> str:
    return f"{d.year}-Q{(d.month - 1) // 3 + 1}"


def title_of(heading_line: str) -> str:
    """Title = text after the date(+optional letter) prefix, minus em-dash/hyphen."""
    rest = re.sub(r"^## \d{4}-\d{2}-\d{2}[a-z]?\s*", "", heading_line)
    return rest.lstrip("—- ").strip()


def _normalize_entry(chunk: str) -> str:
    """Remove only the structural divider before the next entry."""
    if chunk.endswith(ENTRY_SEPARATOR):
        return chunk[: -len(ENTRY_SEPARATOR)]
    return chunk


def _strip_trailing_debris(text: str) -> str:
    """Strip trailing blank lines and bare `---`-only lines, in any
    interleaving. This is the union-merge failure shape (docs/SESSIONS.md
    merge=union in .gitattributes keeps both sides' added lines but does not
    order or de-duplicate the separators between them) — a doubled `---` or
    stray blank run after an entry body, before the next heading.
    """
    lines = text.splitlines()
    while lines and (lines[-1].strip() == "" or re.fullmatch(r"-{3,}", lines[-1].strip())):
        lines.pop()
    return "\n".join(lines)


def rewrite_links_for_archive(text: str) -> str:
    """Rebase links written relative to ``docs/`` for the archive location."""

    def replace(match: re.Match[str]) -> str:
        target = match.group(2)
        parsed = urlsplit(target)
        if (
            not parsed.path
            or target.startswith(("#", "/", "//"))
            or parsed.scheme
            or parsed.netloc
        ):
            return match.group(0)
        source_path = posixpath.normpath(posixpath.join("docs", parsed.path))
        rebased = posixpath.relpath(source_path, ARCHIVE_REL)
        rewritten = urlunsplit(("", "", rebased, parsed.query, parsed.fragment))
        return f"{match.group(1)}{rewritten}{match.group(3)}"

    return _MARKDOWN_LINK_RE.sub(replace, text)


def split_index(doc: str) -> tuple[str, str]:
    """Return ``(body_without_managed_index, index_block)``."""
    i = doc.find(INDEX_START)
    if i == -1:
        return doc, ""
    j = doc.find(INDEX_END)
    end = j + len(INDEX_END) if j != -1 else len(doc)
    block = doc[i:end]
    before = doc[:i]
    if before.endswith(ENTRY_SEPARATOR):
        before = before[: -len(ENTRY_SEPARATOR)]
    return before, block


def parse(doc: str) -> tuple[str, list[Entry]]:
    """Split a SESSIONS-style document into (header, entries newest-first)."""
    body, _ = split_index(doc)
    matches = list(ENTRY_RE.finditer(body))
    if not matches:
        return body, []
    header = body[: matches[0].start()]
    entries: list[Entry] = []
    for k, m in enumerate(matches):
        start = m.start()
        stop = matches[k + 1].start() if k + 1 < len(matches) else len(body)
        chunk = body[start:stop]
        heading_line = chunk.splitlines()[0]
        entries.append(Entry(
            date=dt.date.fromisoformat(m.group(1)),
            title=title_of(heading_line),
            text=_normalize_entry(chunk),
        ))
    return header, entries


def archive_file(root: Path, quarter: str) -> Path:
    return root / ARCHIVE_REL / f"SESSIONS-{quarter}.md"


def _dedup_by_heading(entries: list[Entry]) -> list[Entry]:
    seen: dict[str, Entry] = {}
    for e in entries:
        key = e.text.splitlines()[0]
        seen.setdefault(key, e)
    return list(seen.values())


def _render_archive(quarter: str, entries: list[Entry]) -> str:
    head = (
        f"# Session archive — {quarter}\n\n"
        f"Rolled from `docs/SESSIONS.md` (newest first).\n\n"
        f"{ARCHIVE_LINK_NOTE}\n\n---\n\n"
    )
    body = ENTRY_SEPARATOR.join(e.text for e in entries)
    return head + body


def migrate_archives(root: Path, *, dry_run: bool = False) -> int:
    """Upgrade legacy archives to the content-preserving rebased-link format."""
    archive_dir = root / ARCHIVE_REL
    migrated = 0
    if not archive_dir.is_dir():
        return migrated
    for path in archive_dir.glob("SESSIONS-*.md"):
        doc = path.read_text(encoding="utf-8")
        if ARCHIVE_LINK_NOTE in doc:
            continue
        quarter = path.stem.replace("SESSIONS-", "")
        _, entries = parse(doc)
        rewritten = [
            Entry(entry.date, entry.title, rewrite_links_for_archive(entry.text))
            for entry in entries
        ]
        if not dry_run:
            path.write_text(_render_archive(quarter, rewritten), encoding="utf-8")
        migrated += 1
    return migrated


def regenerate_archives_from_source(
    root: Path,
    source_doc: str,
    *,
    keep_n: int = 20,
    dry_run: bool = False,
) -> dict[str, int]:
    """Rebuild quarterly archives from an unrolled source document."""
    _, entries = parse(source_doc)
    groups: dict[str, list[Entry]] = {}
    for entry in entries[keep_n:]:
        archived = Entry(
            entry.date,
            entry.title,
            rewrite_links_for_archive(entry.text),
        )
        groups.setdefault(quarter_of(entry.date), []).append(archived)
    for quarter, archived_entries in groups.items():
        archived_entries.sort(key=lambda entry: entry.date, reverse=True)
        if not dry_run:
            path = archive_file(root, quarter)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                _render_archive(quarter, archived_entries),
                encoding="utf-8",
            )
    return {quarter: len(entries) for quarter, entries in groups.items()}


def append_entries(root: Path, rolled: list[Entry], *, dry_run: bool = False) -> dict[str, int]:
    """Merge rolled entries into their quarterly archive files (dedup by heading,
    newest-first). Returns {quarter: count_added}."""
    groups: dict[str, list[Entry]] = {}
    for e in rolled:
        archived = Entry(e.date, e.title, rewrite_links_for_archive(e.text))
        groups.setdefault(quarter_of(e.date), []).append(archived)
    counts: dict[str, int] = {}
    for quarter, new_entries in groups.items():
        path = archive_file(root, quarter)
        existing: list[Entry] = []
        if path.exists():
            _, existing = parse(path.read_text(encoding="utf-8"))
        merged = _dedup_by_heading(existing + new_entries)
        merged.sort(key=lambda e: e.date, reverse=True)
        counts[quarter] = len(new_entries)
        if not dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(_render_archive(quarter, merged), encoding="utf-8")
    return counts


def build_index(root: Path) -> str:
    """Regenerate the managed Archive-Index block by scanning the archive dir.
    Empty string when nothing is archived (so the caller omits the block)."""
    archive_dir = root / ARCHIVE_REL
    rows: list[tuple[dt.date, str, str, str]] = []
    if archive_dir.is_dir():
        for path in archive_dir.glob("SESSIONS-*.md"):
            quarter = path.stem.replace("SESSIONS-", "")
            _, entries = parse(path.read_text(encoding="utf-8"))
            for e in entries:
                rows.append((e.date, e.title, quarter, path.name))
    if not rows:
        return ""
    rows.sort(key=lambda r: r[0], reverse=True)
    lines = [
        INDEX_START,
        "## Archive index",
        "",
        "Older entries rolled to `docs/ltm/notes/archive/sessions/` (newest first).",
        "",
        "| Date | Session | Archive |",
        "|---|---|---|",
    ]
    for d, title, quarter, fname in rows:
        t = (title if len(title) <= 80 else title[:77] + "...").replace("|", "\\|")
        lines.append(f"| {d.isoformat()} | {t} | [{quarter}](ltm/notes/archive/sessions/{fname}) |")
    lines.append(INDEX_END)
    return "\n".join(lines)


def render(header: str, kept: list[Entry], index_block: str) -> str:
    body = ENTRY_SEPARATOR.join(e.text for e in kept)
    out = header + body
    if index_block:
        out += ENTRY_SEPARATOR + index_block
    return out + ("" if out.endswith("\n") else "\n")


def normalize(root: Path, *, reorder: bool = False, dry_run: bool = False,
              window: int = ORDER_WINDOW) -> bool:
    """Re-render docs/SESSIONS.md through parse+render to fix union-merge
    debris (doubled `---` separators, stray blank lines between entries)
    without archiving anything. Cheap enough to run after every merge.

    reorder=True additionally sorts the TOP `window` entries newest-first,
    breaking same-date ties by the author time of the commit that first added
    each heading (see order_keys). Same-date ties are the whole problem — union
    collisions are same-date by construction — so the previous date-only sort
    was a no-op on exactly them.

    Windowed, and the bound is load-bearing rather than an optimisation. Union
    only ever inserts at the top anchor, so that is the only region it can
    disturb; everything below is settled. Sorting the whole file moves entries
    that were placed deliberately — measured, not assumed: a full sort of this
    repo reorders 9 historical entries, including one whose heading literally
    reads "2026-07-29 (later)". Commit time is not session chronology when a
    session is written up afterwards, so repair scope is held equal to detection
    scope and settled entries are left alone.

    Returns True if the on-disk file changed.
    """
    sessions = root / SESSIONS_REL
    doc = sessions.read_text(encoding="utf-8")
    _, index_block = split_index(doc)
    header, entries = parse(doc)
    cleaned = [Entry(e.date, e.title, _strip_trailing_debris(e.text)) for e in entries]
    if reorder:
        head_n, tail = cleaned[:window], cleaned[window:]
        keys = order_keys(root, head_n)
        head_n = _reorder_entries(head_n, keys)
        cleaned = head_n + tail
    new_doc = render(header, cleaned, index_block)
    changed = new_doc != doc
    if changed and not dry_run:
        sessions.write_text(new_doc, encoding="utf-8")
    return changed


def lettered_label_of(heading_line: str) -> str:
    """The `YYYY-MM-DDx` label, or `""` when the heading carries no letter.

    Bare same-day dates are deliberately excluded: this file supports several
    entries on one date ordered by author time, and `reorder` exists to sort
    exactly that case. A *letter* is the thing that claims a unique identity,
    so only a repeated letter is a defect.
    """
    m = re.match(r"^## (\d{4}-\d{2}-\d{2}[a-z])(?![a-z])", heading_line)
    return m.group(1) if m else ""


_DATE_SUFFIX_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})([a-z]?)(?![a-z])")
_LETTERS = "abcdefghijklmnopqrstuvwxyz"


def claimed_letters_for_date(entries: list[Entry], day: dt.date) -> set[str]:
    """Letter slots claimed for ``day`` under the a-first allocator convention.

    Both same-day shapes appear in the live file: bare-then-b.. (2026-08-08) and
    a-first (2026-08-10). ``--check-order`` only rejects *duplicate letters*, so
    either shape is legal. Allocation picks **a-first**: a bare ``## YYYY-MM-DD``
    entry claims the ``a`` slot (so bare + b..d → next is ``e``, matching the
    08-08 progression), and lettered headings claim their own letter.
    """
    claimed: set[str] = set()
    for e in entries:
        if e.date != day:
            continue
        m = _DATE_SUFFIX_RE.match(e.text.splitlines()[0])
        if not m:
            continue
        letter = m.group(2)
        if letter:
            claimed.add(letter)
        else:
            claimed.add("a")  # bare dated entry claims the a-first slot
    return claimed


def _labeled_groups(entries: list[Entry]) -> dict[str, list[Entry]]:
    by_label: dict[str, list[Entry]] = {}
    for e in entries:
        label = lettered_label_of(e.text.splitlines()[0])
        if label:
            by_label.setdefault(label, []).append(e)
    return by_label


def duplicate_labels(
    entries: list[Entry], *, grandfathered: set[str] | None = None,
) -> list[str]:
    """Flag any lettered session label claimed by two entries.

    Concurrent sessions allocate letters at write time with no reservation, so
    two branches can pick the same one (2026-08-08f, 2026-08-09g). Neither the
    union merge nor `_dedup_by_heading` catches it: union keeps both sides, and
    the dedup keys on the whole heading line, which differs by title. Git calls
    such a merge clean, so this content check is the only thing standing between
    a duplicate label and `main`.

    ``grandfathered`` (heading lines already committed on the append-only base
    ref — see ``resolve_append_only_base``) exempts a collision only when
    EVERY colliding heading is grandfathered: that duplicate already landed
    before this check existed to catch it, and append-only forbids renaming
    an old heading to fix it after the fact (``append_only_problems``), so
    the two invariants are reconcilable only by not re-flagging history the
    file is not allowed to touch. A collision with even one non-grandfathered
    heading is a *new* collision — exactly what this check exists to catch —
    and always fails, same as before.
    """
    grandfathered = grandfathered or set()
    problems: list[str] = []
    for label, group in _labeled_groups(entries).items():
        if len(group) <= 1:
            continue
        if all(heading_line(e) in grandfathered for e in group):
            continue
        titles = [e.title for e in group]
        problems.append(
            f"duplicate session label {label!r}: claimed by {' and '.join(repr(t) for t in titles)}"
            f" — renumber the later one (letters are not reserved across sessions)"
        )
    return problems


def grandfathered_duplicate_notes(
    entries: list[Entry], grandfathered: set[str],
) -> list[str]:
    """Informational notes for pre-existing duplicates ``duplicate_labels`` left alone.

    Visible-restraint counterpart to the exemption above: a duplicate that
    predates this check and cannot be renamed without violating append-only
    should still be seen by whoever runs the gate, not silently vanish into a
    clean-looking pass. Never blocking — callers print these as notes/WARNs.
    """
    if not grandfathered:
        return []
    notes: list[str] = []
    for label, group in _labeled_groups(entries).items():
        if len(group) > 1 and all(heading_line(e) in grandfathered for e in group):
            titles = [e.title for e in group]
            notes.append(
                f"pre-existing duplicate label {label!r} "
                f"({' / '.join(repr(t) for t in titles)}) predates this check and is "
                "left as-is (append-only forbids renaming a committed heading)"
            )
    return notes


def heading_line(entry: Entry) -> str:
    return entry.text.splitlines()[0]


# Public-repo transplant (docs/adr/2026-08-14-repo-public-visibility-transition.md):
# historical PR/commit objects live on first-passage-archive. A repo-name-only
# href rewrite is not an Open/next edit. The pattern does not match URLs that
# already say first-passage-archive (next char after first-passage is '-').
_HISTORICAL_GH_REPOINT_RE = re.compile(
    r"https://github.com/Joshua-Asante/first-passage/(pull|commit)/"
)


def _normalize_historical_github_urls(text: str) -> str:
    """Map first-passage PR/commit hrefs onto first-passage-archive.

    Used only by the append-only comparator so the 2026-08-14 transplant
    rewrite does not look like a frozen-entry mutation.
    """
    return _HISTORICAL_GH_REPOINT_RE.sub(
        r"https://github.com/Joshua-Asante/first-passage-archive/\1/",
        text,
    )


def _frozen_entry_body(text: str) -> str:
    return _strip_trailing_debris(_normalize_historical_github_urls(text))


def load_archived_entries_by_heading(root: Path) -> dict[str, Entry]:
    """Map heading line -> entry for every quarterly SESSIONS archive under root.

    Last file wins on duplicate headings (archives are deduped by heading on
    write; a collision here is a repair signal, not a soft merge).
    """
    archive_dir = root / ARCHIVE_REL
    by_heading: dict[str, Entry] = {}
    if not archive_dir.is_dir():
        return by_heading
    for path in sorted(archive_dir.glob("SESSIONS-*.md")):
        _, entries = parse(path.read_text(encoding="utf-8"))
        for e in entries:
            by_heading[heading_line(e)] = e
    return by_heading


def append_only_problems(
    base_doc: str,
    ours_doc: str,
    *,
    archived_by_heading: dict[str, Entry] | None = None,
) -> list[str]:
    """Prior headings must keep their bodies; new headings are allowed.

    Keyed by the heading line. Trailing separator debris is stripped so a
    ``--normalize``-class tidy is not a mutation. A heading present on
    ``base_doc`` but missing or rewritten in ``ours_doc`` is the 2026-08-13z/13y
    class (editing Open/next on an old entry, or a union splice into it).
    Headings absent from the base (this branch's new top entry) may change —
    that is the PR-URL pin. A first-passage → first-passage-archive rewrite
    of ``/pull/`` or ``/commit/`` hrefs is also not a mutation (public-repo
    transplant; objects live only on the archive).

    Keep-20 roll exemption: a heading removed from the live file is legal iff
    ``archived_by_heading`` holds that heading with the frozen body after the
    documented relative-link rebase (``rewrite_links_for_archive``). A drop
    without an archive copy, or with a drifted archive body, still fails.
    """
    _, base_entries = parse(base_doc or "")
    _, ours_entries = parse(ours_doc or "")
    ours_by_heading = {heading_line(e): e for e in ours_entries}
    archived = archived_by_heading or {}
    problems: list[str] = []
    for e in base_entries:
        heading = heading_line(e)
        got = ours_by_heading.get(heading)
        if got is None:
            archived_e = archived.get(heading)
            if archived_e is not None:
                expected = _frozen_entry_body(rewrite_links_for_archive(e.text))
                actual = _frozen_entry_body(archived_e.text)
                if expected == actual:
                    continue
                problems.append(
                    f"append-only: archived body drifted for {e.title!r} "
                    "(live roll must preserve entry bytes after link rebase)"
                )
                continue
            problems.append(f"append-only: removed heading {heading!r}")
            continue
        if _frozen_entry_body(e.text) != _frozen_entry_body(got.text):
            problems.append(
                f"append-only: mutated prior entry {e.title!r} "
                "(edit Open/next on the NEW top entry, not this one)"
            )
    return problems


def resolve_append_only_base(root: Path, explicit: str | None = None) -> str:
    """Frozen-heading ref: explicit, else merge-base with origin/main, else HEAD."""
    if explicit:
        return explicit
    mb = _git(root, "merge-base", "HEAD", "origin/main")
    if mb and mb.strip():
        return mb.strip()
    return "HEAD"


def _sessions_at_ref(root: Path, ref: str) -> str:
    doc = _git(root, "show", f"{ref}:{SESSIONS_REL}")
    return doc if doc is not None else ""


def check_append_only(
    root: Path,
    *,
    base_ref: str | None = None,
    ours_ref: str | None = None,
) -> list[str]:
    """Compare working-tree (or ``ours_ref``) SESSIONS.md against ``base_ref``."""
    base = resolve_append_only_base(root, base_ref)
    base_doc = _sessions_at_ref(root, base)
    if ours_ref is None:
        path = root / SESSIONS_REL
        ours_doc = path.read_text(encoding="utf-8") if path.is_file() else ""
    else:
        ours_doc = _sessions_at_ref(root, ours_ref)
    return append_only_problems(
        base_doc,
        ours_doc,
        archived_by_heading=load_archived_entries_by_heading(root),
    )


def _hr_line_before(body: str, heading_start: int) -> bool:
    """True when a ``---`` rule is the last non-blank line before ``heading_start``.

    The newest-first contract joins entries with ``ENTRY_SEPARATOR``; union merges
    that splice a heading mid-document (2026-08-11y/x/w) drop that rule and leave
    an orphaned entry that ``parse`` still finds but humans/tools mis-read.
    """
    before = body[:heading_start]
    lines = before.splitlines()
    i = len(lines) - 1
    while i >= 0 and lines[i].strip() == "":
        i -= 1
    if i < 0:
        return False
    return bool(_HR_LINE_RE.fullmatch(lines[i].strip()))


def separator_problems(doc: str) -> list[str]:
    """Flag entries missing a leading ``---`` separator (union-merge splice shape).

    Doubled / trailing-debris separators are also a normalize delta, but they still
    have a leading rule — this check only names the cheap-to-miss case: a heading
    with no rule above it. ``--normalize`` (no ``--reorder``) is the repair.
    """
    body, _ = split_index(doc)
    matches = list(ENTRY_RE.finditer(body))
    if not matches:
        return []
    problems: list[str] = []
    for m in matches:
        if _hr_line_before(body, m.start()):
            continue
        heading = body[m.start():].splitlines()[0]
        title = title_of(heading)
        problems.append(
            f"missing --- separator before {title!r} "
            f"(union-merge splice; fix: python scripts/roll_sessions.py --normalize)"
        )
    return problems


def structure_problems(doc: str) -> list[str]:
    """Structural defects that are cheap to miss and expensive to notice later.

    Today this is missing ``---`` rules before entries — the union-merge splice
    shape (2026-08-11y/x/w). Doubled-separator / blank-run debris is left to
    ``--normalize`` (post-merge hook already repairs it): a render round-trip
    would also flag trailing-newline canonicalization noise on otherwise fine
    hand-authored entries, so it is not used as a gate signal.
    """
    return separator_problems(doc)


# ── same-clone --next-label claim markers ─────────────────────────────────────


def claim_dir_for(root: Path) -> Path:
    """Per-clone claim directory under the process temp dir."""
    digest = hashlib.sha256(str(root.resolve()).encode()).hexdigest()[:12]
    return Path(tempfile.gettempdir()) / f"{_CLAIM_DIR_PREFIX}{digest}"


def _claim_path(claim_dir: Path, day: dt.date, letter: str) -> Path:
    return claim_dir / f"{day.isoformat()}{letter}"


def read_claimed_letters(
    claim_dir: Path, day: dt.date, *, now: float | None = None, ttl_sec: int = _CLAIM_TTL_SEC,
) -> set[str]:
    """Letters reserved under ``claim_dir`` for ``day``, ignoring expired markers."""
    if not claim_dir.is_dir():
        return set()
    stamp = time.time() if now is None else now
    prefix = day.isoformat()
    claimed: set[str] = set()
    for path in claim_dir.iterdir():
        name = path.name
        if not (name.startswith(prefix) and len(name) == len(prefix) + 1):
            continue
        letter = name[-1]
        if letter not in _LETTERS or not path.is_file():
            continue
        try:
            age = stamp - path.stat().st_mtime
        except OSError:
            continue
        if age > ttl_sec:
            continue
        claimed.add(letter)
    return claimed


def write_label_claim(
    claim_dir: Path, day: dt.date, letter: str, *, pid: int | None = None,
) -> Path:
    """Reserve ``letter`` for ``day`` in this clone. Overwrites an existing marker."""
    claim_dir.mkdir(parents=True, exist_ok=True)
    path = _claim_path(claim_dir, day, letter)
    payload = (
        f"day={day.isoformat()}\n"
        f"letter={letter}\n"
        f"pid={pid if pid is not None else os.getpid()}\n"
        f"created_unix={int(time.time())}\n"
    )
    path.write_text(payload, encoding="utf-8")
    return path


def next_label_for_date(
    entries: list[Entry],
    day: dt.date,
    *,
    reserved: set[str] | None = None,
) -> str:
    """Next free same-day letter for ``day`` (a-first; gaps filled).

    ``reserved`` adds letters claimed outside the file (same-clone lock markers).
    Returns the first letter in a..z not in :func:`claimed_letters_for_date`
    union ``reserved``. Gap example: ``a`` and ``c`` claimed → ``b`` (checker-
    acceptable; duplicates are the only label defect). Raises ``ValueError``
    when a..z are exhausted.
    """
    claimed = claimed_letters_for_date(entries, day)
    if reserved:
        claimed = claimed | reserved
    for letter in _LETTERS:
        if letter not in claimed:
            return letter
    raise ValueError(f"no free same-day letter left for {day.isoformat()}")


def check_order(root: Path, *, window: int = ORDER_WINDOW) -> list[str]:
    """Return human-readable order / structure / label violations.

    Cheap passes, all no-write:

    1. **Separator structure** (no git): every entry needs a leading ``---``;
       doubled-separator debris also fails. Catches the 2026-08-11 union-splice
       that landed headings mid-document without dividers.
    2. **Duplicate lettered labels** (no git unless history resolves a
       grandfather set — see below): two entries sharing ``YYYY-MM-DDx``.
    3. **Full-file calendar monotonicity** (no git): a newer calendar date must
       never sit below an older one. Catches the 2026-08-08 stranding that sat
       below the top-``window`` author-time horizon.
    4. **Top-``window`` author-time** (git): same-date ties broken by the commit
       that first added each heading — the merge=union collision case.

    Duplicate-label detection is grandfathered against the append-only base
    ref (``resolve_append_only_base`` — merge-base with origin/main, else
    HEAD): a collision entirely inside history this file's own append-only
    invariant forbids editing is left as-is (visible via
    ``grandfathered_duplicate_notes``, not silently dropped); a *new*
    collision — the case this check exists for — still fails regardless.
    History that cannot be resolved degrades to an empty grandfather set,
    i.e. every duplicate still fails, same as before this existed.

    Empty list means "no violation found", which on a history-less clone also
    covers "could not check" author-time — the caller warns rather than blocking,
    matching check_pine_manifest's posture on clones with no .pine present.
    """
    doc = (root / SESSIONS_REL).read_text(encoding="utf-8")
    _, entries = parse(doc)
    problems: list[str] = []
    problems.extend(structure_problems(doc))
    grandfathered = committed_headings(root, ref=resolve_append_only_base(root))
    problems.extend(duplicate_labels(entries, grandfathered=grandfathered))
    for above, below in zip(entries, entries[1:]):
        if above.date < below.date:
            problems.append(
                f"date inversion: {above.date.isoformat()} {above.title!r} sits above "
                f"{below.date.isoformat()} {below.title!r}"
            )
    top = entries[:window]
    if len(top) < 2:
        return problems
    keys = order_keys(root, top)
    if keys is None:
        return problems
    for older, newer in zip(top, top[1:]):
        a, b = keys[older.text.splitlines()[0]], keys[newer.text.splitlines()[0]]
        if a is _FILEPOS or b is _FILEPOS:
            continue  # file-position fallback: not an author-time verdict
        if (older.date, a) < (newer.date, b):
            problems.append(
                f"{older.title!r} sits above {newer.title!r}, but was authored earlier "
                f"({a.isoformat() if a is not _NEWEST else 'working tree'} < "
                f"{b.isoformat() if b is not _NEWEST else 'working tree'})"
            )
    return problems


def roll(root: Path, keep_n: int = 20, dry_run: bool = False) -> dict:
    """Roll SESSIONS.md: keep newest keep_n, archive the rest, regenerate index."""
    sessions = root / SESSIONS_REL
    doc = sessions.read_text(encoding="utf-8")
    header, entries = parse(doc)
    kept, rolled = entries[:keep_n], entries[keep_n:]
    archive_dir = root / ARCHIVE_REL
    # True no-op: nothing to roll AND no existing archive -> leave file pristine.
    if not rolled and not archive_dir.exists():
        return {"kept": len(kept), "rolled": 0, "by_quarter": {}}
    migrate_archives(root, dry_run=dry_run)
    by_quarter = append_entries(root, rolled, dry_run=dry_run)
    new_doc = render(header, kept, build_index(root))
    if not dry_run:
        sessions.write_text(new_doc, encoding="utf-8")
    return {"kept": len(kept), "rolled": len(rolled), "by_quarter": by_quarter}



def _safe_print(msg: str) -> None:
    """Print without crashing on Windows cp1252 consoles (headings contain →)."""
    try:
        print(msg)
    except UnicodeEncodeError:
        enc = getattr(sys.stdout, "encoding", None) or "utf-8"
        print(msg.encode(enc, errors="replace").decode(enc, errors="replace"))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--keep", type=int, default=20, help="entries to keep live (default 20)")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, write nothing")
    ap.add_argument("--root", default=None, help="repo root (default: inferred)")
    ap.add_argument(
        "--regenerate-from-git",
        metavar="REF",
        help="rebuild archives from REF:docs/SESSIONS.md before refreshing the live index",
    )
    ap.add_argument(
        "--normalize",
        action="store_true",
        help="fix union-merge separator/blank-line debris in SESSIONS.md without archiving; combine with --reorder",
    )
    ap.add_argument(
        "--reorder",
        action="store_true",
        help="with --normalize: sort entries newest-first, same-date ties broken by git author time",
    )
    ap.add_argument(
        "--check-order",
        action="store_true",
        help=(
            "report separator / duplicate-label / ordering violations and exit 1; "
            "writes nothing (wired as gates.yml sessions-order)"
        ),
    )
    ap.add_argument(
        "--order-window",
        type=int,
        default=ORDER_WINDOW,
        help=f"entries from the top to order-check/reorder (default {ORDER_WINDOW})",
    )
    ap.add_argument(
        "--next-label",
        metavar="YYYY-MM-DD",
        help=(
            "print the next free same-day letter suffix for DATE and exit 0. "
            "Reads docs/SESSIONS.md plus same-clone claim markers under the "
            "process temp dir (so a second concurrent --next-label in this "
            "clone does not silently re-issue the same letter). No network. "
            "Convention: a-first (2026-08-10 style; checker accepts both "
            "bare-then-b.. and a-first). A bare ## YYYY-MM-DD entry claims "
            "'a'. Gaps are filled (a,c claimed → b)."
        ),
    )
    ap.add_argument(
        "--no-claim",
        action="store_true",
        help="with --next-label: do not read or write same-clone claim markers",
    )
    ap.add_argument(
        "--check-append-only",
        action="store_true",
        help=(
            "report prior-entry body mutations (new headings allowed) and exit 1; "
            "writes nothing (wired as gates.yml sessions-append-only). Default "
            "base is merge-base with origin/main, else HEAD"
        ),
    )
    ap.add_argument(
        "--append-only-base",
        metavar="REF",
        default=None,
        help="with --check-append-only: freeze headings present on REF",
    )
    ap.add_argument(
        "--append-only-ours",
        metavar="REF",
        default=None,
        help="with --check-append-only: compare REF instead of the working tree",
    )
    args = ap.parse_args(argv)

    root = Path(args.root) if args.root else Path(__file__).resolve().parents[1]
    if args.next_label is not None:
        try:
            day = dt.date.fromisoformat(args.next_label)
        except ValueError:
            _safe_print(
                f"error: --next-label expects YYYY-MM-DD, got {args.next_label!r}"
            )
            return 2
        doc = (root / SESSIONS_REL).read_text(encoding="utf-8")
        _, entries = parse(doc)
        reserved: set[str] = set()
        cdir = claim_dir_for(root)
        if not args.no_claim:
            reserved = read_claimed_letters(cdir, day)
            in_file = claimed_letters_for_date(entries, day)
            only_reserved = sorted(reserved - in_file)
            if only_reserved:
                # stderr so stdout stays a single letter for shell capture
                sys.stderr.write(
                    "warning: same-clone claim marker(s) reserve letter(s) "
                    f"{','.join(only_reserved)} for {day.isoformat()} "
                    f"(dir {cdir}); skipping to next free\n"
                )
        try:
            letter = next_label_for_date(entries, day, reserved=reserved or None)
        except ValueError as exc:
            _safe_print(f"error: {exc}")
            return 2
        if not args.no_claim:
            write_label_claim(cdir, day, letter)
        _safe_print(letter)
        return 0
    if args.check_order:
        problems = check_order(root, window=args.order_window)
        doc = (root / SESSIONS_REL).read_text(encoding="utf-8")
        _, entries = parse(doc)
        grandfathered = committed_headings(root, ref=resolve_append_only_base(root))
        for note in grandfathered_duplicate_notes(entries, grandfathered):
            _safe_print(f"NOTE: {note}")
        if not problems:
            _safe_print(
                f"SESSIONS order: OK (structure; labels; top {args.order_window}; "
                "full-file dates)"
            )
            return 0
        _safe_print("SESSIONS.md failed structural / newest-first checks:")
        for p in problems:
            _safe_print(f"  - {p}")
        # Point at the repair that actually fixes each class. --reorder is a
        # pure move and cannot renumber a label or invent a missing ---.
        has_dup = any(p.startswith("duplicate session label") for p in problems)
        has_sep = any(p.startswith("missing ---") for p in problems)
        has_order = any(
            p.startswith("date inversion:") or "authored earlier" in p
            for p in problems
        )
        if has_dup:
            _safe_print(
                "fix (duplicate label): renumber the colliding entry by hand "
                "(letters are claimed, not assigned); "
                "claim the next letter: python scripts/roll_sessions.py --next-label <date>"
            )
        if has_sep and not has_order:
            _safe_print("fix (separators): python scripts/roll_sessions.py --normalize")
        elif has_order:
            _safe_print(
                "fix (order"
                + (" + separators" if has_sep else "")
                + "): python scripts/roll_sessions.py --normalize --reorder"
            )
        return 1
    if args.check_append_only:
        problems = check_append_only(
            root,
            base_ref=args.append_only_base,
            ours_ref=args.append_only_ours,
        )
        if not problems:
            _safe_print("SESSIONS append-only: OK (prior entry bodies frozen)")
            return 0
        _safe_print("SESSIONS.md failed append-only checks:")
        for p in problems:
            _safe_print(f"  - {p}")
        _safe_print(
            "fix: add a new top entry (python scripts/roll_sessions.py "
            "--next-label <date>); do not edit Open/next on an older heading"
        )
        return 1
    if args.normalize:
        changed = normalize(root, reorder=args.reorder, dry_run=args.dry_run,
                            window=args.order_window)
        tag = "[dry-run] " if args.dry_run else ""
        print(f"{tag}normalize: {'changed' if changed else 'no change'}")
        return 0
    if args.regenerate_from_git:
        source_doc = subprocess.check_output(
            [
                "git",
                "show",
                f"{args.regenerate_from_git}:{SESSIONS_REL}",
            ],
            cwd=root,
            encoding="utf-8",
        )
        by_quarter = regenerate_archives_from_source(
            root,
            source_doc,
            keep_n=args.keep,
            dry_run=args.dry_run,
        )
        sessions = root / SESSIONS_REL
        header, kept = parse(sessions.read_text(encoding="utf-8"))
        if not args.dry_run:
            sessions.write_text(
                render(header, kept, build_index(root)),
                encoding="utf-8",
            )
        res = {"kept": len(kept), "rolled": sum(by_quarter.values()), "by_quarter": by_quarter}
    else:
        res = roll(root, keep_n=args.keep, dry_run=args.dry_run)
    tag = "[dry-run] " if args.dry_run else ""
    print(f"{tag}kept {res['kept']}, rolled {res['rolled']} -> {res['by_quarter'] or '(none)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
