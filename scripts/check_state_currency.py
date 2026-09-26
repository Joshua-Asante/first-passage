#!/usr/bin/env python3
"""STATE.md currency gate — Last curated, recurring deadlines, past dated sections.

Owns the mechanical limb of docs/operational_rules.md Rule 7 STATE currency
(rolling dates and Last curated must not go stale when the
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
from datetime import date, datetime, timedelta
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
# Whole-token DISCHARGED only. UNDISCHARGED is one token and does not match;
# NOT/NEVER/NON/UN immediately before DISCHARGED is a negation, not a discharge.
DISCHARGED_TOKEN_RE = re.compile(r"[A-Z]+")
DISCHARGED_NEGATION = frozenset({"NOT", "NEVER", "NON", "UN"})
WEEKLY_HORIZON_DAYS = 7
MONTHLY_HORIZON_DAYS = 31
HORIZON_BY_KIND = {
    "Weekly": WEEKLY_HORIZON_DAYS,
    "Monthly": MONTHLY_HORIZON_DAYS,
}
# Remediation is per problem: state_roll.py only advances PAST recurring
# deadlines, so only that failure names it. A future deadline beyond the
# horizon, Last curated and past dated subsections are corrected by hand.
ROLL_HINT = "for deadline rolls run: python -I scripts/fp.py python scripts/state_roll.py"
MANUAL_HINT = (
    "correct the heading by hand (the roller only advances past deadlines)"
)
# Mirrors state_roll.py (a test pins them equal): a Monthly deadline on day 28
# or later may be a month-end clamp, so the roller needs a `cadence day NN`
# anchor in the heading before it will roll it.
MAX_UNANCHORED_MONTHLY_DAY = 27
CADENCE_DAY_RE = re.compile(r"\bcadence day (\d{1,2})\b")
MONTH_END_HINT = (
    "Monthly days 28-31 roll only with a 'cadence day NN' anchor in the "
    "heading; add it, then run the roller (see scripts/README.md, STATE currency)"
)


def today_et() -> date:
    raw = os.environ.get("STATE_CURRENCY_TODAY", "").strip()
    if raw:
        return date.fromisoformat(raw)
    return datetime.now(ET).date()


def _single(pattern: re.Pattern[str], text: str, name: str) -> re.Match[str]:
    """The one match of pattern; a duplicate would leave all but the first unchecked."""
    found = list(pattern.finditer(text))
    if not found:
        raise ValueError(f"STATE.md has no {name}")
    if len(found) > 1:
        raise ValueError(f"STATE.md has {len(found)} {name} copies; keep exactly one")
    return found[0]


def last_curated(text: str) -> date:
    match = _single(LAST_CURATED_RE, text, "Last curated field")
    return date.fromisoformat(match.group(1))


def newest_decision_index_date(text: str) -> date:
    section = _single(DECISION_SECTION_RE, text, "Executed operator decisions section")
    dates = [date.fromisoformat(m.group(1)) for m in BULLET_DATE_RE.finditer(section.group(0))]
    if not dates:
        raise ValueError("decision index has no dated bullets")
    return max(dates)


def recurring_headings(forward_text: str) -> list[tuple[str, date, str]]:
    """(kind, next deadline, heading line) for Weekly then Monthly."""
    found: dict[str, tuple[date, str]] = {}
    for match in RECURRING_HEADING_RE.finditer(forward_text):
        kind = match.group(1)
        heading = match.group(0)
        deadline = DEADLINE_RE.search(heading)
        if deadline is None:
            raise ValueError(f"{kind} recurring heading has no next deadline **YYYY-MM-DD**")
        if kind in found:
            raise ValueError(f"duplicate {kind} recurring heading")
        found[kind] = (date.fromisoformat(deadline.group(1)), heading)
    missing = [k for k in ("Weekly", "Monthly") if k not in found]
    if missing:
        raise ValueError("missing recurring heading: " + ", ".join(missing))
    return [(k, *found[k]) for k in ("Weekly", "Monthly")]


def recurring_deadlines(forward_text: str) -> list[tuple[str, date]]:
    return [(kind, deadline) for kind, deadline, _ in recurring_headings(forward_text)]


def roller_needs_anchor(kind: str, deadline: date, heading: str) -> bool:
    """True when state_roll.py would refuse this past deadline for want of an anchor."""
    return (
        kind == "Monthly"
        and deadline.day > MAX_UNANCHORED_MONTHLY_DAY
        and CADENCE_DAY_RE.search(heading) is None
    )


def heading_is_discharged(heading: str) -> bool:
    tokens = DISCHARGED_TOKEN_RE.findall(heading.upper())
    try:
        idx = tokens.index("DISCHARGED")
    except ValueError:
        return False
    if idx > 0 and tokens[idx - 1] in DISCHARGED_NEGATION:
        return False
    return True


def past_dated_headings(forward_text: str, today: date) -> list[str]:
    stale: list[str] = []
    for match in DATED_HEADING_RE.finditer(forward_text):
        heading_date = date.fromisoformat(match.group(1))
        if heading_is_discharged(match.group(0)):
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
    forward = _single(FORWARD_SECTION_RE, text, "Scheduled forward triggers section")
    body = forward.group(0)
    for kind, deadline, heading in recurring_headings(body):
        if deadline < today:
            hint = ROLL_HINT
            if roller_needs_anchor(kind, deadline, heading):
                hint = MONTH_END_HINT
            out.append(
                f"{kind} next deadline {deadline.isoformat()} is in the past "
                f"(today {today.isoformat()} ET) — {hint}"
            )
            continue
        horizon = HORIZON_BY_KIND[kind]
        latest = today + timedelta(days=horizon)
        if deadline > latest:
            out.append(
                f"{kind} next deadline {deadline.isoformat()} is beyond the "
                f"{horizon}-day next-occurrence horizon "
                f"(today {today.isoformat()} ET) — {MANUAL_HINT}"
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
