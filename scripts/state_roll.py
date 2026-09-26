#!/usr/bin/env python3
"""STATE.md roller — recurring deadline rolls plus decision-index keep-15.

Applies the mechanical limb of docs/operational_rules.md Rule 7 STATE currency
that `check_state_currency.py` only reports: rolls the Weekly/Monthly recurring
deadlines forward and moves decision-index overflow rows into the archive. The
output is a pure function of (input bytes, today) — no timestamps, no
randomness, no environment-dependent ordering — so independent sessions produce
byte-identical edits and a second run on already-rolled files changes nothing.

Only the deadline date (plus a Weekly `bucket MM-DD→MM-DD`) inside the
Weekly/Monthly heading lines and whole overflow index rows (with the blank
lines directly above each) change in STATE; coverage text, `**Last curated:**`,
the queue and every other section stay exactly as authored. A Monthly cadence
on day 28-31 rolls only with a `cadence day NN` anchor in its heading.

Invariants
----------
The roller reads STATE.md and the decision-index archive and writes them only
as a pair. A row's identity is its archive form: a STATE row with its relative
links rebased as the archive stores them.

I1  Row conservation. No decision row is lost or duplicated across STATE +
    archive. Each file holds each row at most once. After a run STATE has only
    lost rows, the archive has only gained rows, the union of rows is
    unchanged, and no row is in both files. From a clean pre-state that is
    exact conservation of the row multiset; the one duplicate a pre-state may
    hold is the residue of an interrupted run (an overflow row archived by a
    run that died before its STATE write), and the retry removes it from STATE
    only, never re-archiving it.
I2  Archive shape. A roll header is a line `**Roll YYYY-MM-DD**...`
    (automated) or `**<Ordinal> roll, YYYY-MM-DD**...` (hand-written), read by
    its date key: case, Unicode spacing and the text after the date do not
    change which header it is. Headers are newest first with strictly
    decreasing dates, except that adjacent hand-written ordinal headers may
    share a date (the ordinal tells them apart; the legacy history has such
    pairs); an automated header shares its date with no other header. Below
    the first header every non-blank line is a header or one whole index row
    (`- **YYYY-MM-DD** — ...`), so each header is followed by whole rows; no
    row sits above the first header and no row shares a header's line.
I3  Line endings. Each file uses one line-ending style: all CRLF or all LF (a
    lone CR is a third style and refused). Inserted text uses the file's own
    ending, and a missing final line ending is added before inserting.
I4  One mutator. A writing run creates an exclusive lock file next to STATE
    with O_CREAT|O_EXCL and holds it for the whole read-plan-commit sequence.
    A lock that already exists is never stolen: the run fails closed and names
    it (a run that died leaves its lock; delete it by hand once no run is
    active). `--check` writes nothing and takes no lock.
I5  Exactly one. Every element read as one thing (each section, each
    recurring heading, its deadline field, the Weekly bucket, the Monthly
    cadence anchor) occurs exactly once, and a look-alike of it fails closed
    instead of being skipped. The currency gate reads the forward triggers,
    the recurring headings and the index through this module, so it fails on
    any heading the roller would refuse.
I6  Normalised look-alikes. Every near-miss detector, in this script and in
    `check_state_currency.py`, tests `lookalike_key(line)`: NFKC, format
    (zero-width) characters dropped, every run of Unicode whitespace folded to
    one space, casefolded. Strict readers match ASCII digits only.

`validate()` is the one checker of I1 (given the pre-state), I2, I3 and I5. It
runs on the parsed pre-state before any plan is made and on the composed
post-state before anything is written; a failure either time exits 2 with
nothing written.

Commit order and recovery (under the lock). Both files are re-read and must
still hold the bytes the plan was made from. Each write goes to its own
`tempfile.mkstemp` file in the target directory, is flushed and fsynced, and
replaces the target atomically. The archive is written first, then STATE, so a
row leaves STATE only once it is durably archived:

- the archive write fails: nothing changed;
- the STATE write fails: the archive is restored to its old bytes, but only if
  it still holds exactly the bytes this run wrote (else it is left alone and
  the error says so);
- the process dies between the writes: the pair is the residue state, which
  `validate()` accepts, and the rerun (after the stale lock is removed) drops
  the residue rows from STATE without archiving them again.

Clock is America/New_York. Tests inject --today or STATE_CURRENCY_TODAY.

Exit 0 nothing to roll (or applied cleanly); 1 with --check when a roll is due;
2 when any invariant fails on the pre- or post-state, the lock is held, a file
is unreadable or changed during the run, or a roll cannot be placed
unambiguously. Exit 2 applies nothing: every planned change of that invocation
is withheld.
"""
from __future__ import annotations

import argparse
import calendar
import os
import posixpath
import re
import secrets
import stat
import sys
import tempfile
import time
import unicodedata
from collections import Counter
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import NamedTuple
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parent.parent
DEFAULT_STATE = REPO / "STATE.md"
DEFAULT_ARCHIVE = (
    REPO / "docs/ltm/notes/archive/state/STATE-decision-index-pre-2026-08-23.md"
)
ET = ZoneInfo("America/New_York")

ARROW = "→"  # U+2192, the Weekly bucket separator
KEEP_ROWS = 15
LOCK_SUFFIX = ".state_roll.lock"
TEMP_SUFFIX = ".state_roll.tmp"

# --- strict readers (ASCII digits only) -------------------------------------

DECISION_SECTION_RE = re.compile(
    r"^## Executed operator decisions\b.*?(?=^## |\Z)",
    re.M | re.S,
)
FORWARD_SECTION_RE = re.compile(
    r"^## Scheduled forward triggers\b.*?(?=^## |\Z)",
    re.M | re.S,
)
# The heading contract is check_state_currency.py's (it imports these): any
# `### Weekly|Monthly — recurring` heading carrying `next deadline
# **YYYY-MM-DD**`. Only the date span (and a Weekly bucket span) is rewritten.
RECURRING_HEADING_RE = re.compile(
    r"^### (Weekly|Monthly) — recurring\b.*$",
    re.M,
)
DEADLINE_RE = re.compile(r"next deadline \*\*([0-9]{4}-[0-9]{2}-[0-9]{2})\*\*")
BUCKET_RE = re.compile(r"\bbucket ([0-9]{2}-[0-9]{2})" + ARROW + r"([0-9]{2}-[0-9]{2})\b")
# Trailing \r is deliberately outside the match so a moved row keeps STATE's
# line ending out of the archived text.
INDEX_ROW_RE = re.compile(
    r"^- \*\*([0-9]{4}-[0-9]{2}-[0-9]{2})\*\* — [^\r\n]*(?=\r?$)", re.M
)
CADENCE_DAY_RE = re.compile(r"\bcadence day ([0-9]{1,2})\b")

# --- look-alike detectors (I6: matched against lookalike_key(line)) ---------
#
# Keys are NFKC, casefolded, whitespace-folded and stripped, so these patterns
# are lower case with single spaces and are anchored with re.match.
FORWARD_SECTION_LOOSE_RE = re.compile(r"#{1,6} ?scheduled[ _-]*forward[ _-]*triggers\b")
DECISION_SECTION_LOOSE_RE = re.compile(r"#{1,6} ?executed[ _-]*operator[ _-]*decisions\b")
RECURRING_HEADING_LOOSE_RE = re.compile(r"#{1,6} ?(weekly|monthly)\b.*?\brecurring\b")
DEADLINE_WORD_RE = re.compile(r"\bnext[ _-]*deadline\b")
BUCKET_WORD_RE = re.compile(r"\bbucket\b")
CADENCE_DAY_WORD_RE = re.compile(r"\bcadence[ _-]*day\b")
# Any dated bullet, bolded or not, `-`/`*`/`+`, indented or not. Every such
# line must be an INDEX_ROW_RE row, or keep-15 and the gate's newest-date read
# would miss it.
DATED_BULLET_LOOSE_RE = re.compile(r"[-*+][ *]*\d{4}-\d{2}-\d{2}")
# Archive roll headers (I2). Anything bold that opens with a `roll` word is a
# header candidate and must read as one of the two header forms.
ARCHIVE_HEADER_LOOSE_RE = re.compile(r"\*\*[^*]*\broll")
ARCHIVE_HEADER_KEY_RE = re.compile(
    r"\*\*(?:(?P<auto>roll)|(?P<ordinal>[^\W\d_]+(?:[ -][^\W\d_]+)*) roll,) "
    r"(?P<date>\d{4}-\d{2}-\d{2}):?\*\*(?P<suffix>.*)"
)
ROW_ON_HEADER_LINE_RE = re.compile(r"\*\*\d{4}-\d{2}-\d{2}\*\*")

LINE_END_RE = re.compile(r"\r?\n")
BLANK_LINE_RE = re.compile(r"[ \t]*\r?\n")
LINK_TARGET_RE = re.compile(r"\]\(([^)]+)\)")
LINK_DEST_RE = re.compile(r"(\S+)(.*)", re.S)
URL_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
PATH_SUFFIX_RE = re.compile(r"([^#?]*)(.*)", re.S)


class StateRollError(ValueError):
    """A missing section/heading or otherwise unusable input.

    A ValueError, so the currency gate's ValueError handling reports the
    roller's refusals as gate failures."""


def today_et(override: date | None = None) -> date:
    if override is not None:
        return override
    raw = os.environ.get("STATE_CURRENCY_TODAY", "").strip()
    if raw:
        return date.fromisoformat(raw)
    return datetime.now(ET).date()


def read_text(path: Path) -> str:
    try:
        with open(path, "r", encoding="utf-8", newline="") as handle:
            return handle.read()
    except OSError as exc:
        raise StateRollError(f"cannot read {path}: {exc}") from exc


# --- I6: look-alike normalisation (shared with check_state_currency.py) -----


def lookalike_key(line: str) -> str:
    """The comparison form of one line for near-miss detection.

    NFKC (fullwidth and compatibility forms), format characters such as
    zero-width spaces dropped, every run of Unicode whitespace (NBSP, en/em
    and ideographic spaces, tabs, a trailing CR) folded to one space, then
    stripped and casefolded."""
    text = unicodedata.normalize("NFKC", line)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Cf")
    return " ".join(text.split()).casefold()


def lookalike_lines(
    text: str, pattern: re.Pattern[str]
) -> list[tuple[int, str, re.Match[str]]]:
    """(line start offset, line, key match) for each line whose key matches."""
    found: list[tuple[int, str, re.Match[str]]] = []
    pos = 0
    for line in text.split("\n"):
        match = pattern.match(lookalike_key(line))
        if match is not None:
            found.append((pos, line.rstrip("\r"), match))
        pos += len(line) + 1
    return found


# --- STATE: recurring deadlines ---------------------------------------------


def first_friday(from_date: date) -> date:
    return from_date + timedelta(days=(4 - from_date.weekday()) % 7)


# Days 29-31 do not exist in every month, and a month-end clamp (Jan 31 ->
# Feb 28, Mar 31 -> Apr 30) leaves a deadline on the 28th-30th that no longer
# records the intended day. Rolling it from the date alone would drift (Jan 31
# -> Feb 28 -> Mar 28). So a Monthly deadline on day 28 or later rolls only
# when the heading carries an explicit `cadence day NN` anchor; without one the
# roller fails closed.
MAX_UNANCHORED_MONTHLY_DAY = 27
ANCHOR_HINT = (
    "add 'cadence day NN' (the intended day of month, 1-31) to the Monthly "
    "heading, then rerun (this invocation applied nothing; see "
    "scripts/README.md, STATE currency)"
)


def _month_day(year: int, month: int, day: int) -> date:
    """date(year, month, day), clamped to the month's last day."""
    return date(year, month, min(day, calendar.monthrange(year, month)[1]))


def next_monthly(old_deadline: date, today: date, anchor: int | None = None) -> date:
    """First date >= today on the cadence day (clamped to short months).

    Without an anchor the cadence day is old_deadline's day, which is only
    trusted up to MAX_UNANCHORED_MONTHLY_DAY."""
    if anchor is None:
        if old_deadline.day > MAX_UNANCHORED_MONTHLY_DAY:
            raise StateRollError(
                f"Monthly deadline {old_deadline.isoformat()} is on day "
                f"{old_deadline.day}, which may be a month-end clamp of a later "
                f"cadence day; {ANCHOR_HINT}"
            )
        anchor = old_deadline.day
    year, month = today.year, today.month
    for _ in range(24):
        candidate = _month_day(year, month, anchor)
        if candidate >= today:
            return candidate
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    raise StateRollError("no monthly deadline found within 24 months")


def _one_field(
    body: str,
    heading: re.Match[str],
    word_re: re.Pattern[str],
    field_re: re.Pattern[str],
    problem: str,
) -> re.Match[str] | None:
    """The heading's single field_re match, or None when no look-alike appears.

    Exactly one look-alike (word_re on the heading's key) and exactly one
    strict field; a second copy, a case or Unicode-spacing variant or an
    unreadable value raises `problem` instead of reading only the first."""
    words = word_re.findall(lookalike_key(heading.group(0)))
    fields = list(field_re.finditer(body, heading.start(), heading.end()))
    if not words and not fields:
        return None
    if len(words) != 1 or len(fields) != 1:
        raise StateRollError(problem)
    return fields[0]


def _cadence_anchor(body: str, heading: re.Match[str], deadline: date) -> int | None:
    """The heading's `cadence day NN`, validated against its deadline."""
    anchor = _one_field(
        body,
        heading,
        CADENCE_DAY_WORD_RE,
        CADENCE_DAY_RE,
        "Monthly heading has a cadence day the roller cannot read; it expects "
        "exactly one 'cadence day NN' (lower case) with NN in 1-31",
    )
    if anchor is None:
        return None
    day = int(anchor.group(1))
    if not 1 <= day <= 31:
        raise StateRollError(
            f"Monthly heading has 'cadence day {day}'; the roller expects "
            "exactly one 'cadence day NN' with NN in 1-31"
        )
    expected = _month_day(deadline.year, deadline.month, day)
    if deadline != expected:
        raise StateRollError(
            f"Monthly deadline {deadline.isoformat()} disagrees with its "
            f"'cadence day {day}' (expected {expected.isoformat()}); correct "
            "the heading by hand"
        )
    return day


def single_match(
    pattern: re.Pattern[str],
    text: str,
    name: str,
    loose: re.Pattern[str] | None = None,
) -> re.Match[str]:
    """The one match of pattern in text; zero, several, or a look-alike fail.

    With a duplicate, only the first would be read (and rolled) while a second
    copy went stale silently. `loose` is tested against each line's
    lookalike_key: every hit must be the strict match's own line, or the
    variant is a copy nobody reads."""
    found = list(pattern.finditer(text))
    if not found:
        raise StateRollError(f"STATE.md has no {name}")
    if len(found) > 1:
        raise StateRollError(
            f"STATE.md has {len(found)} copies of the {name}; keep exactly one"
        )
    if loose is not None:
        for at, line, _ in lookalike_lines(text, loose):
            if at != found[0].start():
                raise StateRollError(
                    f"STATE.md has a look-alike of the {name} "
                    f"({line.strip()[:60]!r}); keep exactly one, spelled exactly"
                )
    return found[0]


def forward_section(text: str) -> re.Match[str]:
    return single_match(
        FORWARD_SECTION_RE,
        text,
        "Scheduled forward triggers section",
        FORWARD_SECTION_LOOSE_RE,
    )


def decision_section(text: str) -> re.Match[str]:
    return single_match(
        DECISION_SECTION_RE,
        text,
        "Executed operator decisions section",
        DECISION_SECTION_LOOSE_RE,
    )


def _splice(text: str, section: re.Match[str], new_body: str) -> str:
    return text[: section.start()] + new_body + text[section.end() :]


def _recurring_heading(text: str, section: re.Match[str], kind: str) -> re.Match[str]:
    """The one strict `### {kind} — recurring` heading, offsets in the section.

    A look-alike anywhere in STATE (another case, dash or Unicode spacing, or
    a copy outside the forward section) is a second heading neither script
    would read."""
    body = section.group(0)
    found = [m for m in RECURRING_HEADING_RE.finditer(body) if m.group(1) == kind]
    if not found:
        raise StateRollError(
            f"no {kind} recurring heading of the form '### {kind} - recurring "
            "... next deadline **YYYY-MM-DD** ...' under Scheduled forward triggers"
        )
    if len(found) > 1:
        raise StateRollError(f"duplicate {kind} recurring heading")
    at = section.start() + found[0].start()
    for offset, line, match in lookalike_lines(text, RECURRING_HEADING_LOOSE_RE):
        if match.group(1) == kind.lower() and offset != at:
            raise StateRollError(
                f"duplicate {kind} recurring heading: look-alike "
                f"{line.strip()[:60]!r}; keep exactly one, spelled "
                "exactly, under Scheduled forward triggers"
            )
    return found[0]


def _deadline(body: str, heading: re.Match[str], kind: str) -> re.Match[str]:
    match = _one_field(
        body,
        heading,
        DEADLINE_WORD_RE,
        DEADLINE_RE,
        f"{kind} recurring heading must carry exactly one next deadline "
        "field, spelled 'next deadline **YYYY-MM-DD**'",
    )
    if match is None:
        raise StateRollError(
            f"{kind} recurring heading has no next deadline **YYYY-MM-DD**"
        )
    return match


def _bucket(body: str, heading: re.Match[str]) -> re.Match[str] | None:
    return _one_field(
        body,
        heading,
        BUCKET_WORD_RE,
        BUCKET_RE,
        "Weekly heading has a bucket the roller cannot read; it expects "
        "exactly one 'bucket MM-DD->MM-DD' (lower case) with a U+2192 arrow",
    )


def _iso_date(raw: str, what: str) -> date:
    try:
        return date.fromisoformat(raw)
    except ValueError as exc:
        raise StateRollError(f"{what} {raw} is not a valid date: {exc}") from exc


class Recurring(NamedTuple):
    """One validated recurring heading; match offsets are in the section body."""

    kind: str
    heading: re.Match[str]
    deadline: re.Match[str]
    deadline_date: date
    bucket: re.Match[str] | None
    anchor: int | None


def recurring_fields(text: str) -> tuple[re.Match[str], dict[str, Recurring]]:
    """(forward section, {"Weekly": ..., "Monthly": ...}) validated as one unit.

    This is the single reader of the recurring headings: the roller rolls from
    it and the currency gate checks from it, so a heading the roller refuses
    (duplicate field, bad bucket, bad or disagreeing anchor) fails both."""
    section = forward_section(text)
    body = section.group(0)
    fields: dict[str, Recurring] = {}
    for kind in ("Weekly", "Monthly"):
        heading = _recurring_heading(text, section, kind)
        deadline = _deadline(body, heading, kind)
        deadline_date = _iso_date(deadline.group(1), f"{kind} next deadline")
        bucket = _bucket(body, heading) if kind == "Weekly" else None
        anchor = (
            _cadence_anchor(body, heading, deadline_date) if kind == "Monthly" else None
        )
        fields[kind] = Recurring(kind, heading, deadline, deadline_date, bucket, anchor)
    return section, fields


def _apply_edits(
    text: str, section: re.Match[str], edits: list[tuple[tuple[int, int], str]]
) -> str:
    body = section.group(0)
    for (start, end), value in sorted(edits, reverse=True):
        body = body[:start] + value + body[end:]
    return _splice(text, section, body)


def roll_weekly(text: str, today: date) -> tuple[str, str | None]:
    """Advance the Weekly deadline (and its bucket) when it is in the past."""
    section, fields = recurring_fields(text)
    weekly = fields["Weekly"]
    old_deadline = weekly.deadline_date
    if old_deadline >= today:
        return text, None
    new_deadline = first_friday(today)
    edits = [(weekly.deadline.span(1), new_deadline.isoformat())]
    if weekly.bucket is not None:
        monday = new_deadline - timedelta(days=new_deadline.weekday())
        edits.append((weekly.bucket.span(1), f"{monday:%m-%d}"))
        edits.append((weekly.bucket.span(2), f"{new_deadline:%m-%d}"))
    new_text = _apply_edits(text, section, edits)
    return new_text, f"weekly: {old_deadline.isoformat()} -> {new_deadline.isoformat()}"


def roll_monthly(text: str, today: date) -> tuple[str, str | None]:
    """Advance the Monthly deadline when it is in the past.

    The anchor is validated on every run (recurring_fields), so a bad anchor
    surfaces before a roll is due."""
    section, fields = recurring_fields(text)
    monthly = fields["Monthly"]
    old_deadline = monthly.deadline_date
    if old_deadline >= today:
        return text, None
    new_deadline = next_monthly(old_deadline, today, monthly.anchor)
    new_text = _apply_edits(
        text, section, [(monthly.deadline.span(1), new_deadline.isoformat())]
    )
    return new_text, f"monthly: {old_deadline.isoformat()} -> {new_deadline.isoformat()}"


# --- links -------------------------------------------------------------------


def _rebase_target(target: str, from_dir: Path, to_dir: Path) -> str:
    """Recompute one filesystem-relative link destination for the archive."""
    if target.startswith("<"):
        raise StateRollError(
            f"angle-bracket link destination {target!r} cannot be rebased safely"
        )
    dest_match = LINK_DEST_RE.match(target)
    if dest_match is None:
        return target
    dest, rest = dest_match.groups()
    if dest.startswith(("#", "?", "/")) or URL_SCHEME_RE.match(dest):
        return target
    path_match = PATH_SUFFIX_RE.match(dest)
    assert path_match is not None  # the pattern matches any string
    path, suffix = path_match.groups()
    if not path:
        return target
    # Archive convention: climb from the archive to STATE's directory, then
    # follow STATE's own (normalised) path — `../../../../../docs/x.md`, not
    # the shortest equivalent. Leading `..` segments survive normpath.
    try:
        climb = os.path.relpath(from_dir, to_dir).replace(os.sep, "/")
    except ValueError as exc:
        raise StateRollError(f"cannot rebase link {dest!r}: {exc}") from exc
    rebased = posixpath.normpath(posixpath.join(climb, posixpath.normpath(path)))
    if path.endswith("/") and not rebased.endswith("/"):
        rebased += "/"
    return rebased + suffix + rest


def rewrite_links(
    row: str,
    from_dir: Path = REPO,
    to_dir: Path = DEFAULT_ARCHIVE.parent,
) -> str:
    """Rebase every filesystem-relative link target from STATE's directory to
    the archive's. URL schemes, root-absolute paths and pure `#`/`?` targets
    are left alone."""

    def _rebase(match: re.Match[str]) -> str:
        return "](" + _rebase_target(match.group(1), from_dir, to_dir) + ")"

    return LINK_TARGET_RE.sub(_rebase, row)


# --- STATE: decision index ---------------------------------------------------


def decision_index_rows(text: str) -> list[re.Match[str]]:
    """Every dated bullet of the one decision index, each a readable row.

    Shared with the currency gate (its newest-date read): a dated bullet in
    any other shape (`* **date**`, unbolded, indented, another separator,
    Unicode spacing, non-ASCII digits) is invisible to keep-15 and to the
    newest-date read, so it fails closed."""
    body = decision_section(text).group(0)
    rows = list(INDEX_ROW_RE.finditer(body))
    row_starts = {match.start() for match in rows}
    for at, line, _ in lookalike_lines(body, DATED_BULLET_LOOSE_RE):
        if at not in row_starts:
            raise StateRollError(
                "decision-index bullet is not a '- **YYYY-MM-DD** — ' row: "
                + line.strip()[:80]
            )
    for row in rows:
        _iso_date(row.group(1), "decision-index date")
    return rows


def index_rows(text: str) -> list[re.Match[str]]:
    """Index rows in document order, validated for a positional keep-15.

    Keep-15 moves rows by position, so it is only correct when every dated
    bullet is a readable row, the rows are newest first (same-day rows keep
    their authored order), and a moved row is one whole line. Anything else
    fails closed instead of archiving the wrong rows or half a record.
    """
    body = decision_section(text).group(0)
    rows = decision_index_rows(text)
    for newer, older in zip(rows, rows[1:]):
        if date.fromisoformat(newer.group(1)) < date.fromisoformat(older.group(1)):
            raise StateRollError(
                f"decision index out of date order: {newer.group(1)} sits above "
                f"{older.group(1)}; restore newest-first order by hand"
            )
    for match in rows[KEEP_ROWS:]:
        # Skip blank lines: after them the next line must be another index row
        # or the section end. Anything else (an indented continuation, loose
        # prose, a sub-heading) may belong to this record, so refuse rather
        # than move the row and orphan the rest in STATE.
        following = _next_nonblank_line(body, match.end())
        if following is not None and INDEX_ROW_RE.match(following) is None:
            raise StateRollError(
                f"overflow row {match.group(1)} is followed by a continuation "
                "line (blank lines skipped) before the next row or section end; "
                "archive multi-line rows by hand"
            )
    return rows


def _next_nonblank_line(body: str, pos: int) -> str | None:
    """The first non-blank line after the line ending at pos, or None at the end."""
    line_end = LINE_END_RE.match(body, pos)
    if line_end is None:
        return None
    pos = line_end.end()
    while pos < len(body):
        nxt = body.find("\n", pos)
        end = len(body) if nxt < 0 else nxt + 1
        line = body[pos:end].rstrip("\r\n")
        if line.strip():
            return line
        pos = end
    return None


def _blank_run_start(body: str, pos: int, floor: int) -> int:
    """Start of the blank lines directly above the line starting at pos (>= floor)."""
    while pos > floor:
        prev_start = body.rfind("\n", 0, pos - 1) + 1
        if prev_start < floor or body[prev_start:pos].strip():
            break
        pos = prev_start
    return pos


def drop_overflow_rows(text: str) -> str:
    """Remove index rows KEEP_ROWS+ from STATE, leaving rows 1..KEEP_ROWS alone.

    Each moved row takes the blank lines directly above it, so a
    blank-separated index keeps one separator after row KEEP_ROWS instead of
    accumulating a run of blank lines."""
    section = decision_section(text)
    body = section.group(0)
    pieces: list[str] = []
    last = 0
    for match in index_rows(text)[KEEP_ROWS:]:
        pieces.append(body[last : _blank_run_start(body, match.start(), last)])
        end = match.end()
        line_end = LINE_END_RE.match(body, end)
        if line_end is not None:
            end = line_end.end()
        last = end
    pieces.append(body[last:])
    return _splice(text, section, "".join(pieces))


# --- I3: line endings --------------------------------------------------------


def line_ending(text: str, name: str = "archive") -> str:
    """The file's one line ending; a mix (or a lone CR) fails closed."""
    crlf = text.count("\r\n")
    if text.count("\r") != crlf or (crlf and crlf != text.count("\n")):
        raise StateRollError(
            f"{name} mixes line endings (CRLF, LF or lone CR); normalise it by hand"
        )
    return "\r\n" if crlf else "\n"


# --- I2: the archive ---------------------------------------------------------


class ArchiveHeader(NamedTuple):
    offset: int  # line start in the archive text
    line: str
    day: date
    automated: bool


class Archive(NamedTuple):
    text: str
    newline: str
    headers: tuple[ArchiveHeader, ...]  # document order, newest first
    rows: tuple[str, ...]  # whole index rows, document order


def parse_archive(text: str) -> Archive:
    """The archive, validated against I2, I3 and I5; any defect fails closed."""
    newline = line_ending(text, "archive")
    headers: list[ArchiveHeader] = []
    rows: list[str] = []
    pos = 0
    for raw in text.split("\n"):
        line = raw.rstrip("\r")
        key = lookalike_key(line)
        if ARCHIVE_HEADER_LOOSE_RE.match(key):
            header = ARCHIVE_HEADER_KEY_RE.fullmatch(key)
            if header is None:
                raise StateRollError(
                    "archive line looks like a roll header but is neither "
                    "'**Roll YYYY-MM-DD**' nor '**<Ordinal> roll, YYYY-MM-DD**': "
                    f"{line.strip()[:80]!r}"
                )
            if ROW_ON_HEADER_LINE_RE.search(header.group("suffix")):
                raise StateRollError(
                    "archive roll header shares its line with an index row: "
                    f"{line.strip()[:80]!r}; put the row on its own line by hand"
                )
            headers.append(
                ArchiveHeader(
                    pos,
                    line,
                    _iso_date(header.group("date"), "archive roll header date"),
                    header.group("auto") is not None,
                )
            )
        elif not key:
            pass
        elif (row := INDEX_ROW_RE.fullmatch(line)) is not None:
            if not headers:
                raise StateRollError(
                    f"archive has an index row above its first roll header: {line[:80]!r}"
                )
            _iso_date(row.group(1), "archive row date")
            rows.append(line)
        elif DATED_BULLET_LOOSE_RE.match(key):
            raise StateRollError(
                f"archive bullet is not a whole '- **YYYY-MM-DD** — ' row: {line.strip()[:80]!r}"
            )
        elif headers:
            raise StateRollError(
                "archive line below the first roll header is neither a roll "
                f"header nor a whole index row: {line.strip()[:80]!r}"
            )
        pos += len(raw) + 1
    for newer, older in zip(headers, headers[1:]):
        if newer.day < older.day:
            raise StateRollError(
                f"archive roll headers out of date order: {newer.day} sits "
                f"above {older.day}; restore newest-first order by hand"
            )
        if newer.day == older.day and (newer.automated or older.automated):
            raise StateRollError(
                f"archive has two roll headers for {newer.day}, one of them "
                "automated; merge them by hand"
            )
    _require_unique(rows, "archive")
    return Archive(text, newline, tuple(headers), tuple(rows))


def _require_unique(rows: list[str] | tuple[str, ...], where: str) -> None:
    repeated = [row for row, count in Counter(rows).items() if count > 1]
    if repeated:
        raise StateRollError(
            f"{where} holds the same decision row more than once (I1): "
            f"{repeated[0][:80]!r}; remove the extra copy by hand"
        )


# --- the one validator -------------------------------------------------------


class Snapshot(NamedTuple):
    """A validated STATE + archive pair."""

    state_rows: tuple[str, ...]  # STATE's index rows, in archive form
    archive: Archive


def validate(
    state_text: str,
    archive_text: str,
    from_dir: Path = REPO,
    to_dir: Path = DEFAULT_ARCHIVE.parent,
    before: Snapshot | None = None,
) -> Snapshot:
    """Check I2, I3 and I5 on the pair, and I1 against `before` when given.

    The same function gates the pre-state (refuse to plan on a corrupt pair)
    and the composed post-state (refuse to write one)."""
    line_ending(state_text, "STATE.md")
    recurring_fields(state_text)
    state_rows = tuple(
        rewrite_links(row.group(0), from_dir, to_dir) for row in index_rows(state_text)
    )
    _require_unique(state_rows, "STATE.md decision index")
    snapshot = Snapshot(state_rows, parse_archive(archive_text))
    if before is not None:
        _check_conservation(before, snapshot)
    return snapshot


def _check_conservation(before: Snapshot, after: Snapshot) -> None:
    """I1 across a run (each file already holds each row at most once)."""
    state_before, archive_before = set(before.state_rows), set(before.archive.rows)
    state_after, archive_after = set(after.state_rows), set(after.archive.rows)
    union_before = state_before | archive_before
    union_after = state_after | archive_after
    problems = [
        (state_after - state_before, "STATE.md gained"),
        (archive_before - archive_after, "the archive lost"),
        (union_before - union_after, "both files lost"),
        (union_after - union_before, "the roll invented"),
        (state_after & archive_after, "both files hold"),
    ]
    for rows, what in problems:
        if rows:
            first = sorted(rows)[0]
            raise StateRollError(
                f"post-roll pair breaks row conservation (I1): {what} "
                f"{len(rows)} row(s), e.g. {first[:80]!r}; nothing written"
            )


# --- archive insertion -------------------------------------------------------


def archive_overflow(
    archive: Archive, rows: list[str], today: date
) -> tuple[str, str]:
    """Archive text with `rows` (archive form, newest first) in today's block.

    A row already in the archive is the residue of an interrupted run and is
    not inserted again (STATE still drops it). The block for `today` is the
    newest header when its date key is today and it is automated; otherwise a
    new `**Roll today**` header goes above the newest header. The archive is
    newest first, so a `today` older than the newest header, or a hand-written
    header dated today, is refused rather than written out of order or into a
    hand-counted block."""
    present = set(archive.rows)
    pending = [row for row in rows if row not in present]
    already = len(rows) - len(pending)
    message = f"index: archived {len(pending)} row(s)"
    if already:
        message += f", {already} already in the archive"
    if not pending:
        return archive.text, message
    if not archive.headers:
        raise StateRollError(
            "archive has no '**... roll, YYYY-MM-DD**' header to insert before"
        )
    newest = archive.headers[0]
    if today < newest.day:
        raise StateRollError(
            f"today {today.isoformat()} is older than the archive's newest roll "
            f"header ({newest.day.isoformat()}); the archive is newest first, so "
            "rerun with the real date (--today / STATE_CURRENCY_TODAY)"
        )
    if today == newest.day and not newest.automated:
        raise StateRollError(
            f"the archive's newest roll header is hand-written and dated today "
            f"({newest.line.strip()[:60]!r}); the roller adds neither a second "
            "header for that date nor rows to a hand-written block. Archive "
            "the overflow rows under it by hand, or rerun on a later day"
        )
    newline = archive.newline
    text = archive.text
    if text and not text.endswith("\n"):
        text += newline  # I3: a missing final line ending would fuse lines
    block = "".join(row + newline + newline for row in pending)
    if today == newest.day:
        at = text.index("\n", newest.offset) + 1
        blank = BLANK_LINE_RE.match(text, at)
        if blank is not None:
            return text[: blank.end()] + block + text[blank.end() :], message
        return text[:at] + newline + block + text[at:], message
    header = (
        f"**Roll {today.isoformat()}** "
        "(automated keep-15 roll; `scripts/state_roll.py`):"
    )
    addition = header + newline + newline + block
    return text[: newest.offset] + addition + text[newest.offset :], message


# --- plan --------------------------------------------------------------------


class Plan(NamedTuple):
    state: str
    archive: str | None  # None when the archive is unchanged
    messages: list[str]


def plan(
    state_text: str,
    archive_text: str,
    today: date,
    from_dir: Path = REPO,
    to_dir: Path = DEFAULT_ARCHIVE.parent,
) -> Plan:
    """The post-state, validated; every check runs before anything is returned,
    so a failure anywhere withholds the whole plan (no partial roll)."""
    before = validate(state_text, archive_text, from_dir, to_dir)
    new_state = state_text
    messages: list[str] = []
    for roller in (roll_weekly, roll_monthly):
        new_state, message = roller(new_state, today)
        if message is not None:
            messages.append(message)
    new_archive = archive_text
    overflow = list(before.state_rows[KEEP_ROWS:])
    if overflow:
        new_state = drop_overflow_rows(new_state)
        new_archive, message = archive_overflow(before.archive, overflow, today)
        messages.append(message)
    validate(new_state, new_archive, from_dir, to_dir, before)
    return Plan(new_state, None if new_archive == archive_text else new_archive, messages)


# --- I4: lock and commit -----------------------------------------------------


def lock_path(state_path: Path) -> Path:
    return state_path.with_name(state_path.name + LOCK_SUFFIX)


@contextmanager
def roll_lock(state_path: Path) -> Iterator[Path]:
    """Hold the exclusive roller lock next to STATE; never steal one.

    The lock records a per-run token; release removes it only while it still
    holds that token, so a run never deletes another run's lock."""
    lock = lock_path(state_path)
    token = f"state_roll pid {os.getpid()} token {secrets.token_hex(8)}\n"
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0)
    try:
        fd = os.open(lock, flags, 0o644)
    except FileExistsError:
        raise StateRollError(
            f"lock file {lock} exists: another "
            "state_roll run is writing, or one died holding the lock. Nothing "
            "was written. If no state_roll run is active, delete the lock file "
            "by hand and rerun; the roller validates both files before planning"
        ) from None
    except OSError as exc:
        raise StateRollError(f"cannot create lock file {lock}: {exc}") from exc
    try:
        os.write(fd, token.encode("utf-8"))
    except OSError as exc:
        os.close(fd)
        os.unlink(lock)
        raise StateRollError(f"cannot write lock file {lock}: {exc}") from exc
    os.close(fd)
    released = False
    try:
        yield lock
    except Exception as exc:
        released = True
        try:
            _release_lock(lock, token)
        except StateRollError as release_exc:
            raise StateRollError(f"{exc}; {release_exc}") from exc
        raise
    finally:
        if not released:
            _release_lock(lock, token)


# Only the owner opens the lock file (a refused run names it without reading
# it): on Windows any open handle makes the owner's unlink fail with a sharing
# violation. Other processes (indexers, antivirus) can still hold it briefly,
# so the owner retries for a bounded time and then fails loudly.
LOCK_RELEASE_ATTEMPTS = 50
LOCK_RELEASE_PAUSE_SECONDS = 0.1


def _release_lock(lock: Path, token: str) -> None:
    """Remove the lock if it still holds this run's token; never fail silently."""
    try:
        with open(lock, encoding="utf-8", newline="") as handle:
            held = handle.read()
    except FileNotFoundError:
        return
    except OSError as exc:
        raise StateRollError(
            f"cannot read lock file {lock} to release it ({exc}); the run "
            "itself finished, delete the lock by hand once no state_roll run "
            "is active"
        ) from exc
    if held != token:
        return  # not this run's lock: leave it to its owner
    problem: OSError | None = None
    for _ in range(LOCK_RELEASE_ATTEMPTS):
        try:
            os.unlink(lock)
            return
        except FileNotFoundError:
            return
        except PermissionError as exc:  # Windows sharing violation: retry
            problem = exc
            time.sleep(LOCK_RELEASE_PAUSE_SECONDS)
        except OSError as exc:
            problem = exc
            break
    raise StateRollError(
        f"cannot remove lock file {lock} ({problem}); the run itself finished, "
        "delete the lock by hand once no state_roll run is active"
    )


def _replace(path: Path, text: str) -> None:
    """Write text to a unique temp file beside path, fsync, then replace path."""
    try:
        mode = stat.S_IMODE(os.stat(path).st_mode)
    except OSError:
        mode = None
    tmp_name: str | None = None
    try:
        fd, tmp_name = tempfile.mkstemp(
            dir=path.parent, prefix=f".{path.name}.", suffix=TEMP_SUFFIX
        )
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        if mode is not None:
            os.chmod(tmp_name, mode)
        os.replace(tmp_name, path)
        tmp_name = None
    except OSError as exc:
        raise StateRollError(f"cannot write {path}: {exc}") from exc
    finally:
        if tmp_name is not None and os.path.exists(tmp_name):
            os.unlink(tmp_name)


def commit(
    state_path: Path,
    archive_path: Path,
    state_before: str,
    archive_before: str,
    new_state: str,
    new_archive: str | None,
) -> None:
    """Write the planned pair: archive first, then STATE (see module docstring).

    The caller holds the lock. Both files must still hold the bytes the plan
    was made from; a restore after a failed STATE write happens only while the
    archive still holds exactly the bytes this run wrote."""
    if read_text(state_path) != state_before or read_text(archive_path) != archive_before:
        raise StateRollError(
            "STATE.md or the archive changed on disk after planning; nothing "
            "written, rerun"
        )
    if new_archive is not None:
        _replace(archive_path, new_archive)
    if new_state == state_before:
        return
    try:
        _replace(state_path, new_state)
    except StateRollError as exc:
        if new_archive is not None:
            _restore_archive(archive_path, new_archive, archive_before, exc)
        raise


def _restore_archive(
    archive_path: Path, written: str, original: str, cause: StateRollError
) -> None:
    try:
        current = read_text(archive_path)
    except StateRollError:
        current = None
    if current != written:
        raise StateRollError(
            f"{cause}; the archive changed during the commit, so it was not "
            "restored: STATE.md still lists its rows, check both files by hand"
        ) from cause
    try:
        _replace(archive_path, original)
    except StateRollError as again:
        raise StateRollError(
            f"{cause}; restoring the archive also failed ({again}): the archive "
            "holds the overflow rows and STATE.md still lists them, the residue "
            "state a rerun resolves"
        ) from cause


# --- CLI ---------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=None,
        metavar="YYYY-MM-DD",
        help="freeze the clock (default: STATE_CURRENCY_TODAY, then ET today)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="report pending rolls without writing; exit 1 if any are due",
    )
    args = parser.parse_args(argv)
    from_dir = args.state.resolve().parent
    to_dir = args.archive.resolve().parent
    try:
        today = today_et(args.today)
        if args.check:
            result = plan(
                read_text(args.state), read_text(args.archive), today, from_dir, to_dir
            )
        else:
            with roll_lock(args.state):
                state_text = read_text(args.state)
                archive_text = read_text(args.archive)
                result = plan(state_text, archive_text, today, from_dir, to_dir)
                if result.messages:
                    commit(
                        args.state,
                        args.archive,
                        state_text,
                        archive_text,
                        result.state,
                        result.archive,
                    )
    except (StateRollError, OSError, ValueError) as exc:
        print(f"state-roll: FAIL - {exc}", file=sys.stderr)
        return 2
    if args.check:
        for message in result.messages:
            print(message)
        return 1 if result.messages else 0
    if not result.messages:
        print("state-roll: nothing to roll")
        return 0
    for message in result.messages:
        print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
