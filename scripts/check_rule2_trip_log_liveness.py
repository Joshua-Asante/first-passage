#!/usr/bin/env python3
"""check_rule2_trip_log_liveness.py — WARN-tier: is Rule 2's own audit-checklist item executing?

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

The one thing it DOES check mechanically, because the withdrawn addendum's own text already
settled what should happen here without needing further ratification: **on or after 2026-11-08**
(the trip-log's own named next quarterly gate, and the addendum's own named escalation checkpoint
— "a second consecutive skip is no longer a single-cycle miss... escalates to a process-compliance
defect in its own right"), if no programme-audit note dated on/after that day mentions Rule 2 or
the trip-log, this is a live finding. Before that date, the script only reports stats — it does
not speculate about whether an earlier note "counts."

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


def last_trip_log_row_date(text: str) -> date | None:
    dates = [date.fromisoformat(m.group(1)) for m in TRIP_ROW_DATE_RE.finditer(text)]
    return max(dates) if dates else None


def scan_audit_notes(audit_dir: Path) -> list[tuple[str, date, bool]]:
    """Returns (relpath, filename_date, mentions_rule2) for every programme-audit note."""
    out: list[tuple[str, date, bool]] = []
    for path in sorted(audit_dir.glob("*.md")):
        m = FILE_DATE_RE.match(path.name)
        if not m:
            continue
        d = date.fromisoformat(m.group(1))
        text = path.read_text(errors="replace")
        out.append((str(path.relative_to(REPO_ROOT)), d, bool(MENTION_RE.search(text))))
    return out


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
    last_row = last_trip_log_row_date(trip_text)
    notes = scan_audit_notes(AUDIT_DIR)

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
        print()

    findings: list[str] = []
    if today >= NEXT_QUARTERLY_GATE:
        gate_notes = [n for n in notes if n[1] >= NEXT_QUARTERLY_GATE]
        if not gate_notes:
            findings.append(
                f"No programme-audit note dated on/after {NEXT_QUARTERLY_GATE.isoformat()} "
                "exists yet -- the next quarterly Rule-2 checklist item (parent ADR Sec7) "
                "cannot have executed."
            )
        elif not any(n[2] for n in gate_notes):
            names = ", ".join(n[0] for n in gate_notes)
            findings.append(
                f"Programme-audit note(s) dated on/after {NEXT_QUARTERLY_GATE.isoformat()} "
                f"exist ({names}) but none mention Rule 2 / the trip-log. Per the parent ADR's "
                "own Sec7 checklist item and the 2026-08-22 addendum's (withdrawn, but "
                "undisputed) escalation clause: a second consecutive skip is no longer a "
                "single-cycle miss -- read docs/notes/audits/rule-2-trip-log.md and either log "
                "a disposition or record why none applies."
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
