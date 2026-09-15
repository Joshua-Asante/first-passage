"""Author a bounded book session calendar (schema ``book_session_calendar/v1``).

Authoring tool only. It writes explicit per-session rows for an operator-named
horizon from named source captures; the runtime loader
(``ops/c1_rail/book_session_calendar.py``) never generates sessions and refuses
anything outside the file. Every denied session must be named on the command
line with its reason; nothing is inferred from weekday arithmetic beyond
enumerating the Monday-Friday account days inside the horizon, and every row
still carries its own sources, deadlines and permission for review.

Schedule times follow TB-S3 rev9 section 5 exactly: V is the earliest mandatory
flat deadline across the venue and the four products; own-flat D = min(16:00 ET,
V - 15 min); entry cutoff D - 15 min; flatten start D - 5 min.

Example (the September 2026 first-release file):

    python scripts/author_book_session_calendar.py \
        --first 2026-09-03 --last 2026-09-30 \
        --deny 2026-09-07 HOLIDAY "CME Globex Labor Day holiday schedule; Tradeify holiday-shortened flat deadline 12:59 ET; product matching halts observed (cme-ui-labor-2026)" \
        --halts 2026-09-07 "6J=17:00,MGC=14:30,MYM=13:00,MNQ=13:00" cme-ui-labor-2026,cme-globex-2026-holiday-schedule \
        --deny 2026-09-08 UNCERTAIN_ADJACENT "Inside the CME 2026 Labor Day schedule dates 6-8 September; post-holiday reopen observed but the full regular session is not separately qualified" \
        --evidence ops/calendars/evidence/2026-09-15-forward-session-source-captures.json \
        --out ops/calendars/book_session_calendar_2026-09.json
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "core"))
from calendar_evidence import halt_evidence, index_captures, read_json_object, require_halt_evidence

SCHEMA = "book_session_calendar/v1"
TZ_NAME = "America/New_York"
ET = ZoneInfo(TZ_NAME)

VENUE = {
    "firm": "Tradeify",
    "edition": "Tradeify_Select_100K",
    "account_identity": "BOUND_AT_RUNTIME",
    "account_day_basis": "TRADEIFY_ACCOUNT_DAY",
    "account_day_note": "A Tradeify trading day spans 18:00 ET to 17:00 ET the next calendar day and is "
                        "independent of the CME business trade date; holiday days are independent days.",
    "timezone": TZ_NAME,
    "account_day_opens_local": "18:00",
    "account_day_closes_local": "17:00",
    "regular_flat_deadline_local": "16:45",
    "holiday_shortened_flat_deadline_local": "12:59",
    "source_ids": ["tradeify-permitted-times-2026-07-14", "tradeify-trading-day-2026-06-18"],
}

SCHEDULE_RULE = {
    "owner": "docs/spec/2026-09-14-tb-s3-halt-resume-contract.md#5-exact-schedule-rule",
    "own_flat_cap_local": "16:00",
    "own_flat_before_v_minutes": 15,
    "cutoff_before_own_flat_minutes": 15,
    "flatten_start_before_own_flat_minutes": 5,
}

PRODUCTS = {
    "6J": {"globex_code": "6J", "description": "Japanese Yen futures",
           "regular_matching_open_local": "18:00", "regular_matching_close_local": "17:00",
           "source_ids": ["cme-spec-6J"]},
    "MGC": {"globex_code": "MGC", "description": "Micro Gold futures",
            "regular_matching_open_local": "18:00", "regular_matching_close_local": "17:00",
            "source_ids": ["cme-spec-MGC"]},
    "MYM": {"globex_code": "MYM", "description": "Micro E-mini Dow futures",
            "regular_matching_open_local": "18:00", "regular_matching_close_local": "17:00",
            "source_ids": ["cme-spec-MYM"]},
    "MNQ": {"globex_code": "MNQ", "description": "Micro E-mini Nasdaq-100 futures",
            "regular_matching_open_local": "18:00", "regular_matching_close_local": "17:00",
            "source_ids": ["cme-spec-MNQ"]},
}

DENIAL_REASONS = ("HOLIDAY", "SHORTENED", "UNCERTAIN_ADJACENT", "MISSING_SOURCE")


@dataclass(frozen=True)
class Denial:
    """A denied account day. HOLIDAY/SHORTENED must carry that date's own observed per-product
    matching halts (ET, HH:MM) and the capture ids that evidence them; nothing is inferred
    from another holiday."""
    reason: str
    note: str
    halts_local: dict | None = None      # {"6J": "17:00", ...} for HOLIDAY/SHORTENED
    source_ids: tuple | None = None      # capture ids evidencing those halts


def parse_halts(text: str) -> dict:
    out = {}
    for item in text.split(","):
        code, _, clock = item.strip().partition("=")
        if code not in PRODUCTS or not re.fullmatch(r"\d{2}:\d{2}", clock):
            raise ValueError(f"bad halt spec {item!r}; expected e.g. MYM=13:00")
        if code in out:
            raise ValueError(f"duplicate product halt: {code}")
        out[code] = clock
    if set(out) != set(PRODUCTS):
        raise ValueError("every product needs a halt clock")
    return out


def _hhmm(text: str) -> time:
    hour, minute = text.split(":")
    return time(int(hour), int(minute))


def _local(day: date, clock: str) -> datetime:
    value = datetime.combine(day, _hhmm(clock), tzinfo=ET)
    # Refuse nonexistent or ambiguous wall times: both folds must agree and round-trip.
    utc = value.astimezone(timezone.utc)
    back = utc.astimezone(ET)
    if back.replace(tzinfo=None) != value.replace(tzinfo=None) or \
            value.replace(fold=1).utcoffset() != value.utcoffset():
        raise ValueError(f"nonexistent or ambiguous local time {day} {clock} {TZ_NAME}")
    return value


def _iso_local(value: datetime) -> str:
    return value.isoformat()


def _iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _account_days(first: date, last: date):
    day = first
    while day <= last:
        if day.weekday() < 5:
            yield day
        day += timedelta(days=1)


def _prior_account_day(day: date) -> date:
    prior = day - timedelta(days=1)
    while prior.weekday() >= 5:
        prior -= timedelta(days=1)
    return prior


def session_id_for(day: date) -> str:
    return f"tradeify-account-day:{day.isoformat()}"


def build_row(day: date, *, denial: Denial | None, evidence_ids: set[str]) -> dict:
    opens = _local(day - timedelta(days=1), VENUE["account_day_opens_local"])
    closes = _local(day, VENUE["account_day_closes_local"])
    holiday = denial is not None and denial.reason in ("HOLIDAY", "SHORTENED")
    if holiday and (not denial.halts_local or not denial.source_ids):
        raise ValueError(f"{day}: a HOLIDAY/SHORTENED denial needs that date's own per-product halts and source ids")
    venue_deadline_clock = VENUE["holiday_shortened_flat_deadline_local"] if holiday \
        else VENUE["regular_flat_deadline_local"]
    venue_deadline = _local(day, venue_deadline_clock)

    products = {}
    deadlines = [venue_deadline]
    for code, spec in PRODUCTS.items():
        if holiday:
            halt = _local(day, denial.halts_local[code])
            products[code] = {
                "qualified": False,
                "cme_trade_date": day.isoformat(),
                "matching_open_utc": None,
                "matching_close_utc": _iso_utc(halt),
                "observed_events": "PREOPEN halt observed on the wall date; preceding open not separately established",
                "source_ids": list(denial.source_ids),
            }
            deadlines.append(halt)
            continue
        m_open = _local(day - timedelta(days=1), spec["regular_matching_open_local"])
        m_close = _local(day, spec["regular_matching_close_local"])
        qualified = denial is None
        products[code] = {
            "qualified": qualified,
            "cme_trade_date": day.isoformat(),
            "matching_open_utc": _iso_utc(m_open),
            "matching_close_utc": _iso_utc(m_close),
            "source_ids": list(spec["source_ids"]) + ["cme-globex-2026-holiday-schedule"],
        }
        deadlines.append(m_close)
    for code in products:
        for sid in products[code]["source_ids"]:
            if sid not in evidence_ids:
                raise ValueError(f"unknown source id {sid}")

    v = min(deadlines)
    cap = _local(day, SCHEDULE_RULE["own_flat_cap_local"])
    own_flat = min(cap, v - timedelta(minutes=SCHEDULE_RULE["own_flat_before_v_minutes"]))
    cutoff = own_flat - timedelta(minutes=SCHEDULE_RULE["cutoff_before_own_flat_minutes"])
    flatten_start = own_flat - timedelta(minutes=SCHEDULE_RULE["flatten_start_before_own_flat_minutes"])
    if not (opens < cutoff < flatten_start < own_flat <= v <= closes):
        raise ValueError(f"no valid trading window for {day}")

    row = {
        "session_id": session_id_for(day),
        "account_date": day.isoformat(),
        "prior_session_id": session_id_for(_prior_account_day(day)),
        "permission": "DENIED" if denial else "PERMITTED",
        "denial_reason": denial.reason if denial else None,
        "denial_note": denial.note if denial else None,
        "opens_local": _iso_local(opens),
        "closes_local": _iso_local(closes),
        "opens_utc": _iso_utc(opens),
        "closes_utc": _iso_utc(closes),
        "venue_flat_deadline_local": _iso_local(venue_deadline),
        "v_utc": _iso_utc(v),
        "own_flat_deadline_utc": _iso_utc(own_flat),
        "flatten_start_utc": _iso_utc(flatten_start),
        "risk_add_cutoff_utc": _iso_utc(cutoff),
        "products": products,
        "source_ids": list(VENUE["source_ids"]) + ["cme-globex-2026-holiday-schedule"],
    }
    return row


def build_calendar(first: date, last: date, denials: dict[date, Denial],
                   evidence_path: Path, generated_utc: str, calendar_id: str) -> dict:
    evidence_bytes = evidence_path.read_bytes()
    evidence = read_json_object(evidence_bytes)
    captures = index_captures(evidence)
    evidence_ids = set(captures)
    halts = halt_evidence(evidence_bytes, captures)
    for day, denial in denials.items():
        if denial.reason not in DENIAL_REASONS:
            raise ValueError(f"unknown denial reason {denial.reason}")
        if denial.source_ids and any(s not in evidence_ids for s in denial.source_ids):
            raise ValueError("denial source ids must name captured sources")
        if denial.reason in ("HOLIDAY", "SHORTENED"):
            if not denial.halts_local or not denial.source_ids:
                raise ValueError(f"{day}: a HOLIDAY/SHORTENED denial needs that date's own per-product halts and source ids")
            for code in PRODUCTS:
                require_halt_evidence(halts, denial.source_ids, day, code, _local(day, denial.halts_local[code]))
    rows = [build_row(day, denial=denials.get(day), evidence_ids=evidence_ids)
            for day in _account_days(first, last)]
    if not rows:
        raise ValueError("empty horizon")
    for day in denials:
        if not any(r["account_date"] == day.isoformat() for r in rows):
            raise ValueError(f"denied date {day} is outside the horizon")
    first_open = datetime.strptime(rows[0]["opens_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    last_close = datetime.strptime(rows[-1]["closes_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    # Monthly-extension review is due six days before expiry, never before the first open.
    review_due = max(first_open + timedelta(days=1), last_close - timedelta(days=6))
    review_due = min(review_due, last_close)
    rows[0]["predecessor_in_file"] = False
    for row in rows[1:]:
        row["predecessor_in_file"] = True
    return {
        "schema": SCHEMA,
        "calendar_id": calendar_id,
        "version": 1,
        "generated_utc": generated_utc,
        "authoring_note": (
            "First attended-release forward session file. Permits only qualified ordinary "
            "sessions; holiday, shortened and uncertain adjacent sessions are denied as a book "
            "permission restriction, not as an assertion of exchange closure. Denied rows keep "
            "their identities and deadlines so account-session chronology and safe flattening "
            "are preserved. Immutable D19 and the typed closure overlay are separate artifacts."
        ),
        "venue": copy.deepcopy(VENUE),
        "schedule_rule": copy.deepcopy(SCHEDULE_RULE),
        "products": copy.deepcopy(PRODUCTS),
        "sources": {
            "evidence_file": evidence_path.as_posix(),
            "evidence_sha256": hashlib.sha256(evidence_bytes).hexdigest(),
            "ids": sorted(evidence_ids),
        },
        "coverage": {
            "first_session_id": rows[0]["session_id"],
            "last_session_id": rows[-1]["session_id"],
            "coverage_start_utc": rows[0]["opens_utc"],
            "coverage_end_utc": rows[-1]["closes_utc"],
            "review_due_utc": _iso_utc(review_due),
            "horizon_authority": "docs/notes/2026-09-15-calendar-account-contract-resolution.md#step-1-closure--approved-design-and-bounded-calendar-route",
        },
        "first_release_policy": {
            "permit_only": "QUALIFIED_ORDINARY",
            "deny": ["HOLIDAY", "SHORTENED", "UNCERTAIN_ADJACENT", "MISSING_SOURCE"],
            "authority": "docs/notes/2026-09-15-calendar-parity-separation-amendment.md",
        },
        "sessions": rows,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--first", required=True, type=date.fromisoformat)
    parser.add_argument("--last", required=True, type=date.fromisoformat)
    parser.add_argument("--deny", nargs=3, action="append", default=[], metavar=("DATE", "REASON", "NOTE"))
    parser.add_argument("--halts", nargs=3, action="append", default=[], metavar=("DATE", "HALTS", "SOURCE_IDS"),
                        help="required for each HOLIDAY/SHORTENED denial: that date's observed per-product ET "
                             "halts, e.g. '6J=17:00,MGC=14:30,MYM=13:00,MNQ=13:00', and the comma-separated "
                             "capture ids that evidence them")
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--calendar-id", default=None)
    parser.add_argument("--generated-utc", default=None)
    args = parser.parse_args(argv)
    evidence_path = args.evidence.resolve()
    try:
        evidence_file = evidence_path.relative_to(Path(__file__).resolve().parents[1]).as_posix()
    except ValueError:
        parser.error("--evidence must be inside the repository root")
    halts = {}
    for d, h, s in args.halts:
        day = date.fromisoformat(d)
        if day in halts:
            parser.error(f"duplicate --halts date: {day}")
        halts[day] = (parse_halts(h), tuple(s.split(",")))
    denials = {}
    for d, reason, note in args.deny:
        day = date.fromisoformat(d)
        if day in denials:
            parser.error(f"duplicate --deny date: {day}")
        h, ids = halts.get(day, (None, None))
        denials[day] = Denial(reason, note, h, ids)
    for day in halts:
        if day not in denials or denials[day].reason not in ("HOLIDAY", "SHORTENED"):
            parser.error(f"--halts date {day} must bind to a HOLIDAY/SHORTENED denial")
    generated = args.generated_utc or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    calendar_id = args.calendar_id or f"tradeify-select-100k/forward/{args.first.isoformat()}..{args.last.isoformat()}"
    payload = build_calendar(args.first, args.last, denials, evidence_path, generated, calendar_id)
    payload["sources"]["evidence_file"] = evidence_file
    data = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
    args.out.write_bytes(data)
    print(f"wrote {args.out} sessions={len(payload['sessions'])} sha256={hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
