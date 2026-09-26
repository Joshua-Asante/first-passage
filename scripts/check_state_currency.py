#!/usr/bin/env python3
"""STATE.md currency gate — Last curated, recurring deadlines, past dated sections.

Owns the mechanical limb of docs/operational_rules.md Rule 7 STATE currency
(rolling dates and Last curated must not go stale when the
daily-repo-truth-sync digest is skipped). Reads only STATE.md.

The forward-trigger section, the Weekly/Monthly recurring headings and the
decision index are read through state_roll.py's own parser (loaded from this
directory), so any heading the roller would refuse — a second deadline field,
a malformed bucket, a cadence anchor out of range, duplicated, in another case
or disagreeing with its deadline, a look-alike heading or section — fails this
gate too, on every run and not only when a roll falls due. Every element read
as unique must occur exactly once; a look-alike fails closed. Look-alikes are
detected on state_roll.lookalike_key (the roller's invariant I6: NFKC,
zero-width characters dropped, every Unicode whitespace run folded, casefolded),
so NBSP, ideographic spaces or fullwidth letters cannot hide a second copy. A
dated subsection heading the strict `### YYYY-MM-DD` reader cannot see (another
level, Unicode spacing, non-ASCII digits) fails closed instead of escaping the
staleness check.

Exit 0 if all three invariants hold. Exit 1 on a missing, duplicate or
unreadable field, a stale date, or an unreadable file.

Clock is America/New_York. Tests inject STATE_CURRENCY_TODAY=YYYY-MM-DD.
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from types import ModuleType
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parent.parent
DEFAULT_STATE = REPO / "STATE.md"
ET = ZoneInfo("America/New_York")


def _load_roller() -> ModuleType:
    """state_roll.py by path: works under `python -I` (no script dir on sys.path)."""
    path = Path(__file__).resolve().parent / "state_roll.py"
    spec = importlib.util.spec_from_file_location("_state_roll_contract", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ROLLER = _load_roller()
# One contract, the roller's (tests pin these; do not re-declare copies).
RECURRING_HEADING_RE = ROLLER.RECURRING_HEADING_RE
DEADLINE_RE = ROLLER.DEADLINE_RE
FORWARD_SECTION_RE = ROLLER.FORWARD_SECTION_RE
DECISION_SECTION_RE = ROLLER.DECISION_SECTION_RE
CADENCE_DAY_RE = ROLLER.CADENCE_DAY_RE
MAX_UNANCHORED_MONTHLY_DAY = ROLLER.MAX_UNANCHORED_MONTHLY_DAY

# I6: the one look-alike normalisation, shared with the roller.
lookalike_key = ROLLER.lookalike_key

LAST_CURATED_RE = re.compile(r"^\*\*Last curated:\*\* ([0-9]{4}-[0-9]{2}-[0-9]{2})", re.M)
# Look-alikes are matched against lookalike_key(line) (lower case, single
# spaces, stripped): any variant of the bold field at a line start.
LAST_CURATED_LOOSE_RE = re.compile(r"\*\* ?last[ _-]*curated\b")
DATED_HEADING_RE = re.compile(r"^### ([0-9]{4}-[0-9]{2}-[0-9]{2})\b(.*)$", re.M)
DATED_HEADING_LOOSE_RE = re.compile(r"#{1,6} ?\d{4}-\d{2}-\d{2}\b")
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
# A Monthly deadline on day 28 or later may be a month-end clamp, so the
# roller needs a `cadence day NN` anchor in the heading before it will roll it.
MONTH_END_HINT = (
    "Monthly days 28-31 roll only with a 'cadence day NN' anchor in the "
    "heading; add it, then run the roller (see scripts/README.md, STATE currency)"
)


def today_et() -> date:
    raw = os.environ.get("STATE_CURRENCY_TODAY", "").strip()
    if raw:
        return date.fromisoformat(raw)
    return datetime.now(ET).date()


def last_curated(text: str) -> date:
    match = ROLLER.single_match(
        LAST_CURATED_RE, text, "Last curated field", LAST_CURATED_LOOSE_RE
    )
    return date.fromisoformat(match.group(1))


def newest_decision_index_date(text: str) -> date:
    rows = ROLLER.decision_index_rows(text)
    if not rows:
        raise ValueError("decision index has no dated bullets")
    return max(date.fromisoformat(row.group(1)) for row in rows)


def recurring_headings(text: str) -> list[tuple[str, date, str, int | None]]:
    """(kind, next deadline, heading line, cadence anchor) for Weekly then Monthly.

    Read by state_roll.recurring_fields, the roller's own validator."""
    _, fields = ROLLER.recurring_fields(text)
    return [
        (kind, field.deadline_date, field.heading.group(0), field.anchor)
        for kind, field in fields.items()
    ]


def recurring_deadlines(text: str) -> list[tuple[str, date]]:
    return [(kind, deadline) for kind, deadline, _, _ in recurring_headings(text)]


def roller_needs_anchor(kind: str, deadline: date, anchor: int | None) -> bool:
    """True when state_roll.py would refuse this past deadline for want of an anchor."""
    return kind == "Monthly" and deadline.day > MAX_UNANCHORED_MONTHLY_DAY and anchor is None


def heading_is_discharged(heading: str) -> bool:
    """True when DISCHARGED appears and no occurrence of it is negated.

    Every occurrence is read, not the first: `DISCHARGED; NOT DISCHARGED`
    records something still owed, so it is not discharged."""
    tokens = DISCHARGED_TOKEN_RE.findall(heading.upper())
    positions = [i for i, token in enumerate(tokens) if token == "DISCHARGED"]
    if not positions:
        return False
    return all(i == 0 or tokens[i - 1] not in DISCHARGED_NEGATION for i in positions)


def unreadable_dated_headings(forward_text: str) -> list[str]:
    """Dated-heading look-alikes the strict `### YYYY-MM-DD` reader misses."""
    strict = {match.start() for match in DATED_HEADING_RE.finditer(forward_text)}
    return [
        line.strip()
        for at, line, _ in ROLLER.lookalike_lines(forward_text, DATED_HEADING_LOOSE_RE)
        if at not in strict
    ]


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
    body = ROLLER.forward_section(text).group(0)
    for kind, deadline, _, anchor in recurring_headings(text):
        if deadline < today:
            hint = ROLL_HINT
            if roller_needs_anchor(kind, deadline, anchor):
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
    for heading in unreadable_dated_headings(body):
        out.append(
            "dated subsection heading is not '### YYYY-MM-DD ...' and would "
            f"escape the staleness check: {heading[:80]}"
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
