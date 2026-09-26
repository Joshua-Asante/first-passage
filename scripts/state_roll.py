#!/usr/bin/env python3
"""STATE.md roller — recurring deadline rolls plus decision-index keep-15.

Applies the mechanical limb of docs/operational_rules.md Rule 7 STATE currency
that `check_state_currency.py` only reports: rolls the Weekly/Monthly recurring
deadlines forward and moves decision-index overflow rows into the archive. The
output is a pure function of (input bytes, today, the archive's position
relative to STATE) — no timestamps, no randomness, no environment-dependent
ordering — so concurrent sessions produce byte-identical edits and a second run
on already-rolled files changes nothing. A retry after an interrupted run is
safe: an overflow row already present in the archive is dropped from STATE
without being archived again.

Byte preservation: files are read and written with newline translation off and
UTF-8, and only the deadline date (plus a Weekly `bucket MM-DD→MM-DD`) inside
the Weekly/Monthly heading lines and whole overflow index rows are touched. Coverage text, `**Last curated:**`, the queue and every other
section stay exactly as authored.

Clock is America/New_York. Tests inject --today or STATE_CURRENCY_TODAY.

Exit 0 nothing to roll (or applied cleanly); 1 with --check when a roll is due;
2 on a missing/duplicate section or heading, a heading or index the roller
cannot read unambiguously, or an unreadable file. Exit 2 applies nothing: every
planned change of that invocation is withheld.
"""
from __future__ import annotations

import argparse
import os
import posixpath
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Callable
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parent.parent
DEFAULT_STATE = REPO / "STATE.md"
DEFAULT_ARCHIVE = (
    REPO / "docs/ltm/notes/archive/state/STATE-decision-index-pre-2026-08-23.md"
)
ET = ZoneInfo("America/New_York")

ARROW = "→"  # U+2192, the Weekly bucket separator
KEEP_ROWS = 15

DECISION_SECTION_RE = re.compile(
    r"^## Executed operator decisions\b.*?(?=^## |\Z)",
    re.M | re.S,
)
FORWARD_SECTION_RE = re.compile(
    r"^## Scheduled forward triggers\b.*?(?=^## |\Z)",
    re.M | re.S,
)
# The heading contract is check_state_currency.py's, byte for byte (a test pins
# the two patterns equal): any `### Weekly|Monthly — recurring` heading carrying
# `next deadline **YYYY-MM-DD**`. Only the date span (and a Weekly bucket span)
# is rewritten; every other byte of the heading stays as authored.
RECURRING_HEADING_RE = re.compile(
    r"^### (Weekly|Monthly) — recurring\b.*$",
    re.M,
)
DEADLINE_RE = re.compile(r"next deadline \*\*(\d{4}-\d{2}-\d{2})\*\*")
BUCKET_WORD_RE = re.compile(r"\bbucket\b")
BUCKET_RE = re.compile(r"\bbucket (\d{2}-\d{2})" + ARROW + r"(\d{2}-\d{2})\b")
# Trailing \r is deliberately outside the match so a moved row keeps STATE's
# line ending out of the archived text.
INDEX_ROW_RE = re.compile(
    r"^- \*\*(\d{4}-\d{2}-\d{2})\*\* — [^\r\n]*(?=\r?$)", re.M
)
# Any dated bullet, as check_state_currency.py counts them. Every such line must
# also be an INDEX_ROW_RE row, or keep-15 would miscount.
DATED_BULLET_RE = re.compile(r"^- \*\*\d{4}-\d{2}-\d{2}\*\*[^\r\n]*", re.M)
# Matches both the hand-written ordinal headers ("**Seventeenth roll, 2026-09-25**")
# and this script's own date-keyed headers ("**Roll 2026-09-26**").
ARCHIVE_ROLL_HEADER_RE = re.compile(
    r"^\*\*(?:.*[Rr]oll, |Roll )\d{4}-\d{2}-\d{2}\*\*", re.M
)
LINE_END_RE = re.compile(r"\r?\n")
BLANK_LINE_RE = re.compile(r"[ \t]*\r?\n")
LINK_TARGET_RE = re.compile(r"\]\(([^)]+)\)")
LINK_DEST_RE = re.compile(r"(\S+)(.*)", re.S)
URL_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
PATH_SUFFIX_RE = re.compile(r"([^#?]*)(.*)", re.S)


class StateRollError(Exception):
    """A missing section/heading or otherwise unusable input."""


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


def write_text(path: Path, text: str) -> None:
    try:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
    except OSError as exc:
        raise StateRollError(f"cannot write {path}: {exc}") from exc


def first_friday(from_date: date) -> date:
    return from_date + timedelta(days=(4 - from_date.weekday()) % 7)


# Days 29-31 do not exist in every month. After a clamp, the heading no longer
# records the intended cadence day, so rolling again would drift (Jan 31 ->
# Feb 28 -> Mar 28). Fail closed and leave those cadences to a hand roll.
MAX_MONTHLY_DAY = 28


def next_monthly(old_deadline: date, today: date) -> date:
    """First date >= today on old_deadline's day-of-month."""
    wanted_day = old_deadline.day
    if wanted_day > MAX_MONTHLY_DAY:
        raise StateRollError(
            f"monthly cadence day {wanted_day} exceeds {MAX_MONTHLY_DAY}; the "
            "heading cannot carry the intended day across short months, so "
            "roll the Monthly heading by hand, then rerun (this invocation "
            "applied nothing)"
        )
    year, month = today.year, today.month
    for _ in range(24):
        candidate = date(year, month, wanted_day)
        if candidate >= today:
            return candidate
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    raise StateRollError("no monthly deadline found within 24 months")


def _forward_section(text: str) -> re.Match[str]:
    section = FORWARD_SECTION_RE.search(text)
    if section is None:
        raise StateRollError("STATE.md has no Scheduled forward triggers section")
    return section


def _splice(text: str, section: re.Match[str], new_body: str) -> str:
    return text[: section.start()] + new_body + text[section.end() :]


def _recurring_heading(body: str, kind: str) -> re.Match[str]:
    found = [m for m in RECURRING_HEADING_RE.finditer(body) if m.group(1) == kind]
    if not found:
        raise StateRollError(
            f"no {kind} recurring heading of the form '### {kind} - recurring "
            "... next deadline **YYYY-MM-DD** ...'"
        )
    if len(found) > 1:
        raise StateRollError(f"duplicate {kind} recurring heading")
    return found[0]


def _deadline(body: str, heading: re.Match[str], kind: str) -> re.Match[str]:
    match = DEADLINE_RE.search(body, heading.start(), heading.end())
    if match is None:
        raise StateRollError(
            f"{kind} recurring heading has no next deadline **YYYY-MM-DD**"
        )
    return match


def _apply_edits(
    text: str, section: re.Match[str], edits: list[tuple[tuple[int, int], str]]
) -> str:
    body = section.group(0)
    for (start, end), value in sorted(edits, reverse=True):
        body = body[:start] + value + body[end:]
    return _splice(text, section, body)


def roll_weekly(text: str, today: date) -> tuple[str, str | None]:
    """Advance the Weekly deadline (and its bucket) when it is in the past."""
    section = _forward_section(text)
    body = section.group(0)
    heading = _recurring_heading(body, "Weekly")
    deadline = _deadline(body, heading, "Weekly")
    bucket: re.Match[str] | None = None
    words = list(BUCKET_WORD_RE.finditer(body, heading.start(), heading.end()))
    if words:
        bucket = BUCKET_RE.search(body, heading.start(), heading.end())
        if len(words) > 1 or bucket is None:
            raise StateRollError(
                "Weekly heading has a bucket the roller cannot read; it expects "
                "exactly one 'bucket MM-DD->MM-DD' with a U+2192 arrow"
            )
    old_deadline = date.fromisoformat(deadline.group(1))
    if old_deadline >= today:
        return text, None
    new_deadline = first_friday(today)
    edits = [(deadline.span(1), new_deadline.isoformat())]
    if bucket is not None:
        monday = new_deadline - timedelta(days=new_deadline.weekday())
        edits.append((bucket.span(1), f"{monday:%m-%d}"))
        edits.append((bucket.span(2), f"{new_deadline:%m-%d}"))
    new_text = _apply_edits(text, section, edits)
    return new_text, f"weekly: {old_deadline.isoformat()} -> {new_deadline.isoformat()}"


def roll_monthly(text: str, today: date) -> tuple[str, str | None]:
    """Advance the Monthly deadline when it is in the past."""
    section = _forward_section(text)
    body = section.group(0)
    heading = _recurring_heading(body, "Monthly")
    deadline = _deadline(body, heading, "Monthly")
    old_deadline = date.fromisoformat(deadline.group(1))
    if old_deadline >= today:
        return text, None
    new_deadline = next_monthly(old_deadline, today)
    new_text = _apply_edits(text, section, [(deadline.span(1), new_deadline.isoformat())])
    return new_text, f"monthly: {old_deadline.isoformat()} -> {new_deadline.isoformat()}"


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


def index_rows(text: str) -> list[re.Match[str]]:
    """Index rows in document order, validated for a positional keep-15.

    Keep-15 moves rows by position, so it is only correct when every dated
    bullet is a readable row, the rows are newest first (same-day rows keep
    their authored order), and a moved row is one whole line. Anything else
    fails closed instead of archiving the wrong rows or half a record.
    """
    section = DECISION_SECTION_RE.search(text)
    if section is None:
        raise StateRollError("STATE.md has no Executed operator decisions section")
    body = section.group(0)
    rows = list(INDEX_ROW_RE.finditer(body))
    row_starts = {match.start() for match in rows}
    for bullet in DATED_BULLET_RE.finditer(body):
        if bullet.start() not in row_starts:
            raise StateRollError(
                "decision-index bullet is not a '- **YYYY-MM-DD** — ' row: "
                + bullet.group(0).strip()[:80]
            )
    for newer, older in zip(rows, rows[1:]):
        if date.fromisoformat(newer.group(1)) < date.fromisoformat(older.group(1)):
            raise StateRollError(
                f"decision index out of date order: {newer.group(1)} sits above "
                f"{older.group(1)}; restore newest-first order by hand"
            )
    for match in rows[KEEP_ROWS:]:
        line_end = LINE_END_RE.match(body, match.end())
        if line_end is None:
            continue
        nxt = body.find("\n", line_end.end())
        following = body[line_end.end() : len(body) if nxt < 0 else nxt].rstrip("\r")
        if following.strip() and INDEX_ROW_RE.match(following) is None:
            raise StateRollError(
                f"overflow row {match.group(1)} is followed by a continuation "
                "line; archive multi-line rows by hand"
            )
    return rows


def overflow_rows(text: str) -> list[str]:
    """Index rows beyond KEEP_ROWS, in document order (newest first)."""
    return [match.group(0) for match in index_rows(text)[KEEP_ROWS:]]


def drop_overflow_rows(text: str) -> str:
    """Remove index rows KEEP_ROWS+ from STATE, leaving rows 1..KEEP_ROWS alone."""
    section = DECISION_SECTION_RE.search(text)
    if section is None:
        raise StateRollError("STATE.md has no Executed operator decisions section")
    body = section.group(0)
    pieces: list[str] = []
    last = 0
    for match in index_rows(text)[KEEP_ROWS:]:
        pieces.append(body[last : match.start()])
        end = match.end()
        line_end = LINE_END_RE.match(body, end)
        if line_end is not None:
            end = line_end.end()
        last = end
    pieces.append(body[last:])
    return _splice(text, section, "".join(pieces))


def line_ending(text: str) -> str:
    match = LINE_END_RE.search(text)
    return match.group(0) if match is not None else "\n"


def _top_of_today_block(text: str, header: re.Match[str]) -> int:
    """Offset just past the header line and its blank separator line."""
    end = header.end()
    line_end = LINE_END_RE.match(text, end)
    if line_end is None:
        return end
    end = line_end.end()
    blank = BLANK_LINE_RE.match(text, end)
    return blank.end() if blank is not None else end


def archive_overflow(
    text: str,
    rows: list[str],
    today: date,
    from_dir: Path = REPO,
    to_dir: Path = DEFAULT_ARCHIVE.parent,
) -> tuple[str, str]:
    """Insert overflow rows above the archive's newest roll header.

    A row whose rebased text is already a whole line of the archive was
    archived by an earlier run that stopped before its STATE write; it is not
    inserted again (STATE still drops it). The retry therefore converges on
    the same archive whether it runs the same day or later.
    """
    header = (
        f"**Roll {today.isoformat()}** "
        "(automated keep-15 roll; `scripts/state_roll.py`):"
    )
    newline = line_ending(text)
    present = set(LINE_END_RE.split(text))
    rebased = [rewrite_links(row, from_dir, to_dir) for row in rows]
    pending = [row for row in rebased if row not in present]
    already = len(rebased) - len(pending)
    message = f"index: archived {len(pending)} row(s)"
    if already:
        message += f", {already} already in the archive"
    if not pending:
        return text, message
    block = "".join(row + newline + newline for row in pending)
    newest = ARCHIVE_ROLL_HEADER_RE.search(text)
    mine = re.search("^" + re.escape(header) + r"\r?$", text, re.M)
    if mine is not None and (newest is None or mine.start() <= newest.start()):
        at = _top_of_today_block(text, mine)
        return text[:at] + block + text[at:], message
    if newest is None:
        raise StateRollError(
            "archive has no '**... roll, YYYY-MM-DD**' header to insert before"
        )
    addition = header + newline + newline + block
    at = newest.start()
    return text[:at] + addition + text[at:], message


def _replace(path: Path, text: str) -> None:
    """Write text to a sibling temp file, then atomically replace path."""
    tmp = path.with_name(path.name + ".state_roll.tmp")
    try:
        write_text(tmp, text)
        os.replace(tmp, path)
    except OSError as exc:
        raise StateRollError(f"cannot write {path}: {exc}") from exc
    finally:
        if tmp.exists():
            tmp.unlink()


def commit(
    state_path: Path,
    new_state: str,
    archive_path: Path,
    new_archive: str | None,
) -> None:
    """Write the archive before STATE; restore the archive if STATE fails.

    Overflow rows leave STATE only after they are safely in the archive. If the
    STATE write then fails, the archive is put back, so a retry sees the same
    overflow and archives it exactly once. If the process dies between the two
    writes (no restore runs), the retry finds those rows already in the archive
    and only drops them from STATE (see archive_overflow).
    """
    if new_archive is None:
        _replace(state_path, new_state)
        return
    old_archive = read_text(archive_path)
    _replace(archive_path, new_archive)
    try:
        _replace(state_path, new_state)
    except StateRollError:
        _replace(archive_path, old_archive)
        raise


def plan(
    state_text: str,
    archive_loader: Callable[[], str],
    today: date,
    from_dir: Path = REPO,
    to_dir: Path = DEFAULT_ARCHIVE.parent,
) -> tuple[str, str | None, list[str]]:
    """Return (new state text, new archive text or None, change messages).

    Every check runs before anything is returned, so a failure anywhere
    withholds the whole plan (no partial roll)."""
    new_state: str = state_text
    messages: list[str] = []
    for roller in (roll_weekly, roll_monthly):
        new_state, message = roller(new_state, today)
        if message is not None:
            messages.append(message)
    rows = overflow_rows(state_text)
    new_archive: str | None = None
    if rows:
        new_state = drop_overflow_rows(new_state)
        old_archive = archive_loader()
        new_archive, message = archive_overflow(
            old_archive, rows, today, from_dir, to_dir
        )
        if new_archive == old_archive:
            new_archive = None
        messages.append(message)
    return new_state, new_archive, messages


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
    loader: Callable[[], str] = lambda: read_text(args.archive)
    try:
        state_text = read_text(args.state)
        new_state, new_archive, messages = plan(
            state_text,
            loader,
            today_et(args.today),
            args.state.resolve().parent,
            args.archive.resolve().parent,
        )
    except (StateRollError, OSError, ValueError) as exc:
        print(f"state-roll: FAIL - {exc}", file=sys.stderr)
        return 2
    if args.check:
        for message in messages:
            print(message)
        return 1 if messages else 0
    if not messages:
        print("state-roll: nothing to roll")
        return 0
    try:
        commit(args.state, new_state, args.archive, new_archive)
    except StateRollError as exc:
        print(f"state-roll: FAIL - {exc}", file=sys.stderr)
        return 2
    for message in messages:
        print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
