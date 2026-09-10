"""Weekly activity-decision status for the Tradeify Mon–Fri idle clock.

Report-only. Reads the compliance note's append-only coverage protocol — the
designated authoritative record of a week's operator decision / trade
(TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md).

⚠ That record is **redacted from this public clone** and is expected to be absent
here — see `docs/load_bearing_numbers.md` (venue-inactivity row) and the
[public-visibility transition ADR](../../docs/adr/2026-08-14-repo-public-visibility-transition.md),
which names the file among the artifacts deliberately withheld. Its §2a is the
owner of record for the ENFORCEMENT consequence (irreversible account deletion,
art. 12268494), cited by ``core/firm_rules.py`` and the load-bearing-numbers
table. Do NOT recreate it here to satisfy this reader, and do not renumber its
sections: a public stub would shadow the owner those citations resolve to.

Because of that, an absent file is reported as ``UNAVAILABLE``, never as
``NOT RECORDED`` — "I cannot see the record" and "the record says no row" are
different facts, and only the second is evidence about the account. Conflating
them would hand the operator a false weekly-coverage status on the one clone
where the record is guaranteed missing.

Does not invent a store, does not place trades, and must never read as a
standing licence or a reminder-to-trade. STATE.md owns the recurrence posture,
under "Scheduled forward triggers" -> "Weekly — recurring".

⚠ This module is the venue rule's OPERATIONAL/REPORTING surface (2026-09-03) --
the weekly coverage-decision reader, not the only place the bucket is modelled.
The rule is a per-Mon-Fri-week BUCKET -- ">=1 trade per week" (art. 10468318) --
which is what ``mon_fri_week`` / ``decision_status`` below model. Two research
surfaces model the same bucket and are reusable:
  * ``lab/analysis/c1/tradeify_book_composition_2026-09/book_grid.py``
    ``weekly_coverage`` -- ``pd.period_range(..., freq="W-FRI")`` coverage fraction.
  * ``lab/analysis/c1/msl_monsurf_1_idle_clock_2026-08/idle_clock_monitor.py``
    ``evaluate_week`` -- per-week T-2/T-1 alerts, ``breached`` iff the week has
    zero active days, i.e. the venue predicate exactly. Its frozen semantics are
    ``docs/briefs/pre-registration/Q-MONSURF-1-verdict-preregistration.md`` §3-5
    (that module's own docstring names it); §4 is the frozen T-2/T-1 operational
    definition. Change the monitor's behaviour there, not against the study's
    RESULTS.md, which is an outcome write-up rather than the normative artifact.
Do not treat this report parser as the sole semantic authority; prefer those when
you need the bucket as a computation rather than as a coverage-note read. The MC engine
models something different and stricter: ``core/mc/simulation.py`` counts ROLLING
consecutive idle business days against ``firm_rules`` ``inactivity_max_idle_days:
5``. The two are not interchangeable -- a calendar trading Mon-wk1 / Fri-wk2 /
Mon-wk3 / Fri-wk4 satisfies THIS module in every week while the engine returns
``bust_inactivity`` on day 6 (measured 2026-09-03) -- it over-fires. On a COMPLETE
business-day calendar it cannot miss a real breach, so barrier-ON figures are
conservative ceilings there; on a sparse trade-days-only series the idle days are
dropped before the engine sees them and it UNDER-fires instead (see the
``core/mc/preflight.py`` ``INACTIVITY_OFF`` block).
Do not "reconcile" the two by loosening this module to the engine's shape: the
venue rule is the fact, and the engine's counter is a bound on it.
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
    """Return RECORDED or NOT RECORDED for the Mon–Fri bucket in `text`.

    Callers holding a possibly-absent record must NOT pass ``""`` here and read
    the result as NOT RECORDED — use :func:`coverage_state`, which separates
    "no row" from "no record". This function answers only about text it was given.
    """
    start, end = bucket_mmdd(monday, friday)
    for rx in (_COVERAGE_LIMB, _WEEK_COVERED_HEADING, _HISTORY_COVERED):
        for m in rx.finditer(text):
            if m.group(1) == start and m.group(2) == end:
                return "RECORDED"
    return "NOT RECORDED"


def coverage_state(root: Path, monday: date, friday: date) -> str:
    """RECORDED / NOT RECORDED / UNAVAILABLE for the bucket.

    UNAVAILABLE means the compliance record is not readable on this clone — the
    expected case here, since it is redacted from the public tree (see module
    header). It is a statement about THIS READER, not about the account: absence
    of the record is not evidence that no trade was placed or no row written.
    """
    path = root / COMPLIANCE_REL
    if not path.is_file():
        return "UNAVAILABLE"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return "UNAVAILABLE"
    return decision_status(text, monday, friday)


def format_activity_decision_line(root: Path, asof: date) -> str:
    """One operator-decision status line; never a trade instruction."""
    monday, friday = mon_fri_week(asof)
    state = coverage_state(root, monday, friday)
    days = business_days_remaining(asof, friday)
    label = week_label(monday, friday)
    if state == "UNAVAILABLE":
        # Deliberately does not imply a coverage verdict either way.
        return (
            f"weekly activity decision [{label}]: UNAVAILABLE "
            f"(coverage record redacted from this clone; not a coverage verdict) "
            f"({days} business day{'s' if days != 1 else ''} left) "
            f"— operator call, see STATE scheduled forward triggers"
        )
    return (
        f"weekly activity decision [{label}]: {state} "
        f"({days} business day{'s' if days != 1 else ''} left) "
        f"— operator call, see STATE scheduled forward triggers"
    )
