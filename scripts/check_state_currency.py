#!/usr/bin/env python3
"""STATE.md currency gate — Last curated, recurring deadlines, past dated sections.

Owns the mechanical limb of the 2026-06-30 STATE role-reduction addendum
2026-09-03 (rolling dates and Last curated must not go stale when the
daily-repo-truth-sync digest is skipped). Reads only STATE.md.

Exit 0 if all three invariants hold. Exit 1 on a missing field, a stale
date, or an unreadable file.

Clock is America/New_York. Tests inject STATE_CURRENCY_TODAY=YYYY-MM-DD.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parent.parent
DEFAULT_STATE = REPO / "STATE.md"
ET = ZoneInfo("America/New_York")

LAST_CURATED_RE = re.compile(r"^\*\*Last curated:\*\* (\d{4}-\d{2}-\d{2})", re.M)
DECISION_SECTION_RE = re.compile(
    r"^## Executed operator decisions\b.*?(?=^## |\Z)",
    re.M | re.S,
)
BULLET_DATE_RE = re.compile(r"^- \*\*(\d{4}-\d{2}-\d{2})\*\*", re.M)
FORWARD_SECTION_RE = re.compile(
    r"^## Scheduled forward triggers\b.*?(?=^## |\Z)",
    re.M | re.S,
)
RECURRING_HEADING_RE = re.compile(
    r"^### (Weekly|Monthly) — recurring\b.*$",
    re.M,
)
DEADLINE_RE = re.compile(r"next deadline \*\*(\d{4}-\d{2}-\d{2})\*\*")
DATED_HEADING_RE = re.compile(r"^### (\d{4}-\d{2}-\d{2})\b(.*)$", re.M)


def today_et() -> date:
    raw = os.environ.get("STATE_CURRENCY_TODAY", "").strip()
    if raw:
        return date.fromisoformat(raw)
    return datetime.now(ET).date()


def last_curated(text: str) -> date:
    match = LAST_CURATED_RE.search(text)
    if match is None:
        raise ValueError("STATE.md has no Last curated field")
    return date.fromisoformat(match.group(1))


def newest_decision_index_date(text: str) -> date:
    section = DECISION_SECTION_RE.search(text)
    if section is None:
        raise ValueError("STATE.md has no Executed operator decisions section")
    dates = [date.fromisoformat(m.group(1)) for m in BULLET_DATE_RE.finditer(section.group(0))]
    if not dates:
        raise ValueError("decision index has no dated bullets")
    return max(dates)


def recurring_deadlines(forward_text: str) -> list[tuple[str, date]]:
    found: dict[str, date] = {}
    for match in RECURRING_HEADING_RE.finditer(forward_text):
        kind = match.group(1)
        heading = match.group(0)
        deadline = DEADLINE_RE.search(heading)
        if deadline is None:
            raise ValueError(f"{kind} recurring heading has no next deadline **YYYY-MM-DD**")
        found[kind] = date.fromisoformat(deadline.group(1))
    missing = [k for k in ("Weekly", "Monthly") if k not in found]
    if missing:
        raise ValueError("missing recurring heading: " + ", ".join(missing))
    return [(k, found[k]) for k in ("Weekly", "Monthly")]


def past_dated_headings(forward_text: str, today: date) -> list[str]:
    stale: list[str] = []
    for match in DATED_HEADING_RE.finditer(forward_text):
        heading_date = date.fromisoformat(match.group(1))
        rest = match.group(2)
        if "DISCHARGED" in rest.upper() or "DISCHARGED" in match.group(0).upper():
            continue
        if heading_date < today:
            stale.append(match.group(0).strip())
    return stale


def problems(text: str, today: date) -> list[str]:
    out: list[str] = []
    curated = last_curated(text)
    newest = newest_decision_index_date(text)
    if curated < newest:
        out.append(
            f"Last curated {curated.isoformat()} is behind newest "
            f"decision-index date {newest.isoformat()}"
        )
    forward = FORWARD_SECTION_RE.search(text)
    if forward is None:
        raise ValueError("STATE.md has no Scheduled forward triggers section")
    body = forward.group(0)
    for kind, deadline in recurring_deadlines(body):
        if deadline < today:
            out.append(
                f"{kind} next deadline {deadline.isoformat()} is in the past "
                f"(today {today.isoformat()} ET)"
            )
    for heading in past_dated_headings(body, today):
        out.append(f"past dated subsection is not DISCHARGED: {heading}")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    args = parser.parse_args(argv)
    try:
        text = args.state.read_text(encoding="utf-8")
        today = today_et()
        found = problems(text, today)
    except (OSError, ValueError) as exc:
        print(f"state-currency: FAIL — {exc}", file=sys.stderr)
        return 1
    if found:
        print("state-currency: FAIL — " + "; ".join(found), file=sys.stderr)
        return 1
    print(
        f"state-currency: OK — Last curated and forward-trigger dates "
        f"are current as of {today.isoformat()} ET"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
