#!/usr/bin/env python3
"""STATE.md roller — recurring deadline rolls plus decision-index keep-15.

Applies the mechanical limb of docs/operational_rules.md Rule 7 STATE currency
that `check_state_currency.py` only reports: rolls the Weekly/Monthly recurring
deadlines forward and moves decision-index overflow rows into the archive. The
output is a pure function of (input bytes, today) — no timestamps, no
randomness, no environment-dependent ordering — so concurrent sessions produce
byte-identical edits and a second run on already-rolled files changes nothing.

Byte preservation: files are read and written with newline translation off and
UTF-8, and only the Weekly/Monthly heading lines and whole overflow index rows
are touched. Coverage text, `**Last curated:**`, the queue and every other
section stay exactly as authored.

Clock is America/New_York. Tests inject --today or STATE_CURRENCY_TODAY.

Exit 0 nothing to roll (or applied cleanly); 1 with --check when a roll is due;
2 on a missing section/heading or an unreadable file.
"""
from __future__ import annotations

import argparse
import os
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
ARCHIVE_LINK_PREFIX = "../../../../../"
EXTERNAL_LINK_PREFIXES = ("http://", "https://", "mailto:", "#", "/", "../")

DECISION_SECTION_RE = re.compile(
    r"^## Executed operator decisions\b.*?(?=^## |\Z)",
    re.M | re.S,
)
FORWARD_SECTION_RE = re.compile(
    r"^## Scheduled forward triggers\b.*?(?=^## |\Z)",
    re.M | re.S,
)
WEEKLY_HEADING_RE = re.compile(
    r"^### Weekly — recurring \(rolling; next deadline "
    r"\*\*(\d{4}-\d{2}-\d{2})\*\*, bucket \d{2}-\d{2}"
    + ARROW
    + r"\d{2}-\d{2}\)([^\r\n]*)(?=\r?$)",
    re.M,
)
MONTHLY_HEADING_RE = re.compile(
    r"^### Monthly — recurring \(rolling; next deadline "
    r"\*\*(\d{4}-\d{2}-\d{2})\*\*\)([^\r\n]*)(?=\r?$)",
    re.M,
)
# Trailing \r is deliberately outside the match so a moved row keeps STATE's
# line ending out of the archived text.
INDEX_ROW_RE = re.compile(r"^- \*\*\d{4}-\d{2}-\d{2}\*\* — [^\r\n]*(?=\r?$)", re.M)
# Matches both the hand-written ordinal headers ("**Seventeenth roll, 2026-09-25**")
# and this script's own date-keyed headers ("**Roll 2026-09-26**").
ARCHIVE_ROLL_HEADER_RE = re.compile(
    r"^\*\*(?:.*[Rr]oll, |Roll )\d{4}-\d{2}-\d{2}\*\*", re.M
)
LINE_END_RE = re.compile(r"\r?\n")
BLANK_LINE_RE = re.compile(r"[ \t]*\r?\n")
LINK_TARGET_RE = re.compile(r"\]\(([^)]+)\)")


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
            "roll the Monthly heading by hand"
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


def roll_weekly(text: str, today: date) -> tuple[str, str | None]:
    """Rewrite the Weekly heading line when its deadline is in the past."""
    section = _forward_section(text)
    body = section.group(0)
    match = WEEKLY_HEADING_RE.search(body)
    if match is None:
        raise StateRollError(
            "no Weekly recurring heading of the form '### Weekly - recurring "
            "(rolling; next deadline **YYYY-MM-DD**, bucket MM-DD->MM-DD "
            "with a U+2192 arrow)'"
        )
    old_deadline = date.fromisoformat(match.group(1))
    if old_deadline >= today:
        return text, None
    new_deadline = first_friday(today)
    monday = new_deadline - timedelta(days=new_deadline.weekday())
    bucket = f"{monday:%m-%d}{ARROW}{new_deadline:%m-%d}"
    heading = (
        "### Weekly — recurring (rolling; next deadline "
        f"**{new_deadline.isoformat()}**, bucket {bucket}){match.group(2)}"
    )
    start, end = match.span()
    new_text = _splice(text, section, body[:start] + heading + body[end:])
    return new_text, f"weekly: {old_deadline.isoformat()} -> {new_deadline.isoformat()}"


def roll_monthly(text: str, today: date) -> tuple[str, str | None]:
    """Rewrite the Monthly heading line when its deadline is in the past."""
    section = _forward_section(text)
    body = section.group(0)
    match = MONTHLY_HEADING_RE.search(body)
    if match is None:
        raise StateRollError(
            "no Monthly recurring heading of the form '### Monthly - recurring "
            "(rolling; next deadline **YYYY-MM-DD**)'"
        )
    old_deadline = date.fromisoformat(match.group(1))
    if old_deadline >= today:
        return text, None
    new_deadline = next_monthly(old_deadline, today)
    heading = (
        "### Monthly — recurring (rolling; next deadline "
        f"**{new_deadline.isoformat()}**){match.group(2)}"
    )
    start, end = match.span()
    new_text = _splice(text, section, body[:start] + heading + body[end:])
    return new_text, f"monthly: {old_deadline.isoformat()} -> {new_deadline.isoformat()}"


def rewrite_links(row: str) -> str:
    """Rebase relative markdown link targets onto the archive directory."""

    def _rebase(match: re.Match[str]) -> str:
        target = match.group(1)
        if target.startswith(EXTERNAL_LINK_PREFIXES):
            return match.group(0)
        return "](" + ARCHIVE_LINK_PREFIX + target + ")"

    return LINK_TARGET_RE.sub(_rebase, row)


def index_rows(text: str) -> list[re.Match[str]]:
    section = DECISION_SECTION_RE.search(text)
    if section is None:
        raise StateRollError("STATE.md has no Executed operator decisions section")
    return list(INDEX_ROW_RE.finditer(section.group(0)))


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


def archive_overflow(text: str, rows: list[str], today: date) -> tuple[str, str]:
    """Insert overflow rows above the archive's newest roll header."""
    header = (
        f"**Roll {today.isoformat()}** "
        "(automated keep-15 roll; `scripts/state_roll.py`):"
    )
    newline = line_ending(text)
    block = "".join(rewrite_links(row) + newline + newline for row in rows)
    newest = ARCHIVE_ROLL_HEADER_RE.search(text)
    mine = re.search("^" + re.escape(header) + r"\r?$", text, re.M)
    if mine is not None and (newest is None or mine.start() <= newest.start()):
        at = _top_of_today_block(text, mine)
        return text[:at] + block + text[at:], f"index: archived {len(rows)} row(s)"
    if newest is None:
        raise StateRollError(
            "archive has no '**... roll, YYYY-MM-DD**' header to insert before"
        )
    addition = header + newline + newline + block
    at = newest.start()
    return text[:at] + addition + text[at:], f"index: archived {len(rows)} row(s)"


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
    overflow and archives it exactly once.
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
) -> tuple[str, str | None, list[str]]:
    """Return (new state text, new archive text or None, change messages)."""
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
        new_archive, message = archive_overflow(archive_loader(), rows, today)
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
        new_state, new_archive, messages = plan(state_text, loader, today_et(args.today))
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
