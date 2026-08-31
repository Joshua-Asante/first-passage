#!/usr/bin/env python3
r"""check_rule2_trip_log_liveness.py — WARN-tier: is Rule 2's own audit-checklist item executing?

`docs/adr/2026-06-16-rule-2-budget-before-acting.md` §7 makes one thing a standing programme-audit
checklist item: read `docs/notes/audits/rule-2-trip-log.md`, confirm at least one entry per active
loop class. Nothing has ever mechanically checked that this checklist item actually runs. It
already failed once, silently: the 2026-08-08 quarterly audit ran seven other diagnostics and
skipped this one, undetected until an unrelated sweep caught it the next day (see the trip-log's
own 2026-08-09 correction block, and `2026-06-16-rule-2-budget-before-acting.md` Addendum
2026-08-22, WITHDRAWN 2026-08-23).

THIS SCRIPT DOES NOT ADJUDICATE AUDIT-CYCLE COUNTING. That addendum proposed a formal counting
convention for exactly this territory and the operator explicitly declined to ratify it — not
because the reasoning was wrong, but because nothing operational hinges on it (the 2026-08-20
STRATEGIC trip already makes the log non-empty regardless of cycle count) and a convention was
better authored fresh "at the 2026-11-08 gate" than inferred now. This script inherits that
restraint: it reports which programme-audit notes exist and whether they mention Rule 2 / the
trip-log, as raw fact, and leaves classifying "which one is the real quarterly cycle" to a human,
exactly as the withdrawal preserved.

The one thing it DOES check mechanically is narrower than the withdrawn addendum's own proposal,
deliberately: **on or after 2026-11-08** (the trip-log's own named next quarterly gate — the one
date the withdrawal itself points to, "author any needed convention fresh at the 2026-11-08 gate"),
if no programme-audit note dated on/after that day mentions Rule 2 or the trip-log, this script
reports that as a plain fact — the checklist item has no visible record of having run. It does
NOT characterize what that fact means or what should follow from it; the addendum that once
proposed a consequence for exactly this situation was withdrawn, and its governing ADR says any
convention here must be authored fresh, not revived. This script surfaces the fact so a human can
do that authoring, and stops there. Before 2026-11-08, the script only reports stats — it does
not speculate about whether an earlier note "counts" either.

SCOPE AND ITS LIMITS:

  * Date source is each programme-audit file's own `YYYY-MM-DD` filename prefix, and the trip-log's
    own table rows' `Date` column — no git history is read, matching this script's siblings
    (`check_spec_provenance.py`, `check_falsifier_reachability.py`) in avoiding a git dependency.

  * "Mentions Rule 2 / the trip-log" is a cheap case-insensitive regex (`rule[\s-]?2` or
    `trip[\s-]?log`) — it cannot tell a genuine, reasoned disposition (like
    `2026-07-01-methodology-belt-scoped-audit.md` §3 Q-B) from a passing namedrop. A green run here
    means the checklist item was *touched*, not that it was executed well; a human still reads the
    audit note for that, same epistemic humility as `check_falsifier_reachability.py`'s own
    "green != all falsifiers in force."

  * WARN-TIER BY DESIGN. Always exits 0 unless --strict. Wired into `gates.yml` as `tier: always`,
    report-only — the exact failure this script exists to catch is a report-only checklist item
    nobody was prompted to run reliably, so it must not depend on anyone remembering to run this
    either.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TRIP_LOG = REPO_ROOT / "docs" / "notes" / "audits" / "rule-2-trip-log.md"
AUDIT_DIR = REPO_ROOT / "docs" / "notes" / "audits" / "programme-audit"

# The trip-log's own named next quarterly gate (docs/notes/audits/rule-2-trip-log.md's
# 2026-08-09 correction block) and the withdrawn addendum's own named escalation checkpoint.
NEXT_QUARTERLY_GATE = date(2026, 11, 8)

MENTION_RE = re.compile(r"rule[\s-]?2\b|trip[\s-]?log", re.IGNORECASE)
TRIP_ROW_DATE_RE = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|", re.MULTILINE)
FILE_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")


def _safe_date(raw: str) -> date | None:
    """Parses a YYYY-MM-DD string, returning None (not raising) on a date-shaped typo
    like '2026-02-30'. This script is WARN-tier and must never crash a pre-commit run
    over a malformed date in one file -- found by PR #233 review."""
    try:
        return date.fromisoformat(raw)
    except ValueError:
        return None


def last_trip_log_row_date(text: str) -> tuple[date | None, list[str]]:
    """Returns (most recent valid row date, list of malformed date strings found)."""
    bad: list[str] = []
    dates: list[date] = []
    for m in TRIP_ROW_DATE_RE.finditer(text):
        d = _safe_date(m.group(1))
        if d is None:
            bad.append(m.group(1))
        else:
            dates.append(d)
    return (max(dates) if dates else None), bad


def scan_audit_notes(audit_dir: Path) -> tuple[list[tuple[str, date, bool]], list[str]]:
    """Returns ((relpath, filename_date, mentions_rule2) per valid note, malformed filenames)."""
    out: list[tuple[str, date, bool]] = []
    bad: list[str] = []
    for path in sorted(audit_dir.glob("*.md")):
        m = FILE_DATE_RE.match(path.name)
        if not m:
            continue
        d = _safe_date(m.group(1))
        if d is None:
            bad.append(path.name)
            continue
        text = path.read_text(errors="replace")
        out.append((str(path.relative_to(REPO_ROOT)), d, bool(MENTION_RE.search(text))))
    return out, bad


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stats", action="store_true", help="print the liveness summary")
    parser.add_argument(
        "--strict", action="store_true", help="exit 1 on findings (default: always exit 0)"
    )
    parser.add_argument(
        "--today", type=date.fromisoformat, default=None,
        help="override today's date (ISO format), for testing only",
    )
    args = parser.parse_args(argv)
    today = args.today or date.today()

    if not TRIP_LOG.is_file():
        print("check_rule2_trip_log_liveness: WARN -- trip-log file missing: " + str(TRIP_LOG))
        return 1 if args.strict else 0

    trip_text = TRIP_LOG.read_text(errors="replace")
    last_row, bad_rows = last_trip_log_row_date(trip_text)
    notes, bad_filenames = scan_audit_notes(AUDIT_DIR)

    notes_since_last_row = (
        [n for n in notes if last_row is not None and n[1] > last_row] if last_row else notes
    )
    mentioning_since = [n for n in notes_since_last_row if n[2]]
    silent_since = [n for n in notes_since_last_row if not n[2]]

    if args.stats:
        print(f"trip-log last row date        : {last_row.isoformat() if last_row else 'none'}")
        print(f"programme-audit notes total   : {len(notes)}")
        print(f"  since last trip-log row     : {len(notes_since_last_row)}")
        print(f"    mentioning Rule 2/trip-log: {len(mentioning_since)}")
        print(f"    silent on it              : {len(silent_since)}")
        print(f"next named quarterly gate     : {NEXT_QUARTERLY_GATE.isoformat()}")
        print(f"today                         : {today.isoformat()}")
        if bad_rows or bad_filenames:
            print(f"unparseable dates (skipped)   : {len(bad_rows) + len(bad_filenames)} "
                  f"({bad_rows + bad_filenames})")
        print()

    findings: list[str] = []
    if today >= NEXT_QUARTERLY_GATE:
        # Upper-bounded at `today`: an unbounded `>= NEXT_QUARTERLY_GATE` filter would let a
        # note dated in the future (e.g. drafted ahead, or checked in with a typo'd year) that
        # happens to mention Rule 2 silently satisfy a gate that hasn't actually happened yet --
        # the same forward-record/phantom-discharge shape this script exists to catch, not
        # commit (found by PR #233 review round 3).
        gate_notes = [n for n in notes if NEXT_QUARTERLY_GATE <= n[1] <= today]
        if not gate_notes:
            findings.append(
                f"No programme-audit note dated on/after {NEXT_QUARTERLY_GATE.isoformat()} "
                "exists yet -- the next quarterly Rule-2 checklist item (parent ADR Sec7) has "
                "no visible record of having run. This script does not characterize what that "
                "means (the addendum that once proposed a consequence for this was withdrawn; "
                "docs/adr/2026-06-16-rule-2-budget-before-acting.md says author any needed "
                "convention fresh at this gate, not by reviving that text) -- it only reports "
                "the fact."
            )
        elif not any(n[2] for n in gate_notes):
            names = ", ".join(n[0] for n in gate_notes)
            findings.append(
                f"Programme-audit note(s) dated on/after {NEXT_QUARTERLY_GATE.isoformat()} "
                f"exist ({names}) but none mention Rule 2 / the trip-log -- the parent ADR's "
                "own Sec7 checklist item has no visible record of having run at this gate. "
                "This script does not characterize what that means or what should follow "
                "(the addendum that once proposed a consequence for this exact situation was "
                "WITHDRAWN, and its governing ADR instructs authoring any needed convention "
                "fresh at this gate, not reviving that text -- "
                "docs/adr/2026-06-16-rule-2-budget-before-acting.md, Addendum 2026-08-22/"
                "2026-08-23). Read docs/notes/audits/rule-2-trip-log.md and rule on it directly."
            )

    if not findings:
        print(
            "check_rule2_trip_log_liveness: OK "
            f"({len(notes)} programme-audit note(s) scanned, 0 live finding(s))"
        )
        if today < NEXT_QUARTERLY_GATE:
            print(
                f"  NOTE: before {NEXT_QUARTERLY_GATE.isoformat()}, this script only reports "
                "stats -- it does not adjudicate which prior audit 'counts' as the quarterly "
                "cycle (that convention was proposed and the operator declined to ratify it; "
                "see module docstring)."
            )
        return 0

    print("check_rule2_trip_log_liveness: WARN -- Rule 2 audit-checklist item may be silently "
          "skipped again\n")
    for f in findings:
        print(f"  {f}")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
