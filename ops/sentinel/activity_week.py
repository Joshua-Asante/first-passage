"""Weekly activity-decision status for the Tradeify Mon–Fri idle clock.

Report-only. Reads the compliance note's append-only coverage protocol — the
designated authoritative record of a week's operator decision / trade (see
TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md §2a; idle-clock tracking spec §4).

Does not invent a store, does not place trades, and must never read as a
standing licence or a reminder-to-trade. STATE.md row 0 owns the recurrence
posture (RECURRENCE-UNRULED).
"""
from __future__ import annotations

import re
from datetime import date, timedelta
from pathlib import Path

COMPLIANCE_REL = "docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md"

# Append-only Coverage limb row, e.g.
#   | 2026-08-07 (Fri) | **Coverage — 08-03→08-07 bucket** | ... | ✅ **COVERED** ...
_COVERAGE_LIMB = re.compile(
    r"Coverage\s*—\s*(\d{2}-\d{2})\s*→\s*(\d{2}-\d{2})\s+bucket",
    re.IGNORECASE,
)
# Follow-up heading, e.g. "week 08-03→08-07 **COVERED**"
_WEEK_COVERED_HEADING = re.compile(
    r"week\s+(\d{2}-\d{2})\s*→\s*(\d{2}-\d{2})\s+\*\*COVERED\*\*",
    re.IGNORECASE,
)
# Coverage-history table row with a discharged mark (not "in progress").
_HISTORY_COVERED = re.compile(
    r"\|\s*\*?\*?(\d{2}-\d{2})\s*→\s*(\d{2}-\d{2})\*?\*?\s*\|"
    r"[^|\n]*\|"
    r"[^|\n]*(?:✅\s*covered|\*\*COVERED\*\*)",
    re.IGNORECASE,
)


def mon_fri_week(asof: date) -> tuple[date, date]:
    """ISO Mon–Fri bucket containing `asof` (weekend stays in that ISO week)."""
    monday = asof - timedelta(days=asof.weekday())
    friday = monday + timedelta(days=4)
    return monday, friday


def week_label(monday: date, friday: date) -> str:
    # ASCII on purpose: this label reaches __main__.main()'s console print,
    # which has no encoding safety net -- a legacy Windows console (cp1252)
    # cannot encode U+2192 and crashes print() (2026-08-17 weekly run).
    return f"{monday.isoformat()}->{friday.strftime('%m-%d')}"


def bucket_mmdd(monday: date, friday: date) -> tuple[str, str]:
    return monday.strftime("%m-%d"), friday.strftime("%m-%d")


def business_days_remaining(asof: date, friday: date) -> int:
    """Weekdays from `asof` through `friday` inclusive; 0 once the bucket has closed."""
    if asof > friday:
        return 0
    if asof.weekday() >= 5:  # Sat/Sun before that Friday cannot occur for same ISO week
        return 0
    return sum(
        1
        for offset in range((friday - asof).days + 1)
        if (asof + timedelta(days=offset)).weekday() < 5
    )


def decision_status(text: str, monday: date, friday: date) -> str:
    """Return RECORDED or NOT RECORDED for the Mon–Fri bucket in `text`."""
    start, end = bucket_mmdd(monday, friday)
    for rx in (_COVERAGE_LIMB, _WEEK_COVERED_HEADING, _HISTORY_COVERED):
        for m in rx.finditer(text):
            if m.group(1) == start and m.group(2) == end:
                return "RECORDED"
    return "NOT RECORDED"


def format_activity_decision_line(root: Path, asof: date) -> str:
    """One operator-decision status line; never a trade instruction."""
    monday, friday = mon_fri_week(asof)
    path = root / COMPLIANCE_REL
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    status = decision_status(text, monday, friday)
    days = business_days_remaining(asof, friday)
    label = week_label(monday, friday)
    return (
        f"weekly activity decision [{label}]: {status} "
        f"({days} business day{'s' if days != 1 else ''} left) "
        f"— operator call, see STATE row 0"
    )
