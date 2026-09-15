"""TB-C1 bounded session-calendar producer for the sizing consumer.

Loads one versioned ``book_session_calendar/v1`` file plus the typed closure
overlay, verifies every row against the ratified TB-S3 rev9 section 5 schedule
rule and the ``America/New_York`` UTC mapping, and produces ``BookSession`` values
only from qualified, permitted rows. It never generates a session: a timestamp
outside the file, a denied or overlay date, expired or unstarted coverage, or a
digest that does not match the operator-pinned value is a refusal, not a fallback.

A refusal here halts *new risk* only. It returns a decision object; it never
touches halt/recovery state, so protective ownership and the scheduled flatten
deadlines of the current row remain available through ``schedule_for``.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from book_sizing_context import BookSession

SCHEMA = "book_session_calendar/v1"
OVERLAY_SCHEMA = "book_closure_overlay/v1"
EVIDENCE_SCHEMA_V1 = "forward_session_source_captures/v1"
EVIDENCE_SCHEMA_V2 = "forward_session_source_captures/v2"
EVIDENCE_V1_WARNING = "evidence_schema_v1_no_product_coverage"
RATIFICATION_SCHEMA = "calendar_ratification/v1"
_RATIFICATION_KEYS = frozenset({
    "calendar_id", "calendar_file", "calendar_sha256", "closure_overlay_file",
    "closure_overlay_sha256", "coverage_start_utc", "coverage_end_utc", "ratified_by",
    "ratified_utc", "instruction", "record", "scope",
})
_TOP_KEYS = frozenset({
    "schema", "calendar_id", "version", "generated_utc", "authoring_note", "venue",
    "schedule_rule", "products", "sources", "coverage", "first_release_policy", "sessions",
})
_ROW_KEYS = frozenset({
    "session_id", "account_date", "prior_session_id", "permission", "denial_reason",
    "denial_note", "opens_local", "closes_local", "opens_utc", "closes_utc",
    "venue_flat_deadline_local", "v_utc", "own_flat_deadline_utc", "flatten_start_utc",
    "risk_add_cutoff_utc", "products", "source_ids", "predecessor_in_file",
})
_PRODUCT_KEYS_REQUIRED = frozenset({"qualified", "cme_trade_date", "matching_open_utc",
                                    "matching_close_utc", "source_ids"})
_PERMISSIONS = frozenset({"PERMITTED", "DENIED"})
_DENIAL_REASONS = frozenset({"HOLIDAY", "SHORTENED", "UNCERTAIN_ADJACENT", "MISSING_SOURCE"})
_SESSION_ID = re.compile(r"^tradeify-account-day:(\d{4}-\d{2}-\d{2})$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class CalendarError(ValueError):
    """The calendar file is malformed, inconsistent with the schedule rule, or unusable."""


@dataclass(frozen=True)
class SessionSchedule:
    session_id: str
    prior_session_id: str
    permission: str
    denial_reason: str | None
    opens_at: datetime
    admits_from: datetime          # account open or the latest qualified product matching open, whichever is later
    risk_add_cutoff: datetime
    flatten_start: datetime
    own_flat_deadline: datetime
    v: datetime
    closes_at: datetime
    overlay_blocked: bool


@dataclass(frozen=True)
class SessionDecision:
    session: BookSession | None
    refusal: str | None
    schedule: SessionSchedule | None
    calendar_digest: str
    warnings: tuple[str, ...] = ()

    @property
    def permitted(self) -> bool:
        return self.session is not None


def _utc_event(text: object, label: str) -> datetime:
    if not isinstance(text, str) or not text.endswith("Z"):
        raise CalendarError(f"{label}: expected UTC 'Z' timestamp, got {text!r}")
    try:
        value = datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise CalendarError(f"{label}: {exc}") from exc
    return value


def _utc(text: object, label: str) -> datetime:
    value = _utc_event(text, label)
    if value.second:
        raise CalendarError(f"{label}: clock-defined boundaries must fall on a whole minute")
    return value


def _local(text: object, tz: ZoneInfo, label: str) -> datetime:
    if not isinstance(text, str):
        raise CalendarError(f"{label}: expected ISO local timestamp")
    try:
        value = datetime.fromisoformat(text)
    except ValueError as exc:
        raise CalendarError(f"{label}: {exc}") from exc
    if value.tzinfo is None:
        raise CalendarError(f"{label}: local timestamp must carry its offset")
    naive = value.replace(tzinfo=None)
    fold0 = naive.replace(tzinfo=tz, fold=0)
    fold1 = naive.replace(tzinfo=tz, fold=1)
    if fold0.utcoffset() != fold1.utcoffset():
        raise CalendarError(f"{label}: ambiguous local time {text} (DST fold)")
    if fold0.astimezone(timezone.utc).astimezone(tz).replace(tzinfo=None) != naive:
        raise CalendarError(f"{label}: nonexistent local time {text} (DST gap)")
    if fold0.utcoffset() != value.utcoffset():
        raise CalendarError(f"{label}: offset {value.utcoffset()} disagrees with {tz.key}")
    if fold0.second or fold0.microsecond:
        raise CalendarError(f"{label}: clock-defined boundaries must fall on a whole minute")
    return fold0


def _clock(text: object, label: str) -> tuple[int, int]:
    if not isinstance(text, str) or not re.fullmatch(r"\d{2}:\d{2}", text):
        raise CalendarError(f"{label}: expected HH:MM")
    hour, minute = int(text[:2]), int(text[3:])
    if not (0 <= hour < 24 and 0 <= minute < 60):
        raise CalendarError(f"{label}: invalid clock {text}")
    return hour, minute


def _minutes(value: object, label: str) -> timedelta:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise CalendarError(f"{label}: expected positive integer minutes")
    return timedelta(minutes=value)


def _read(path: Path) -> tuple[bytes, dict]:
    data = path.read_bytes()
    try:
        payload = json.loads(data)
    except ValueError as exc:
        raise CalendarError(f"{path}: not JSON ({exc})") from exc
    if not isinstance(payload, dict):
        raise CalendarError(f"{path}: expected an object")
    return data, payload


def load_closure_overlay(path: Path) -> tuple[frozenset[date], str]:
    """Return (overlay account dates, overlay digest). Every row must be typed and flagged."""
    data, payload = _read(path)
    if payload.get("schema") != OVERLAY_SCHEMA:
        raise CalendarError("overlay: wrong schema")
    if payload.get("day_basis") != "TRADEIFY_ACCOUNT_DAY":
        raise CalendarError("overlay: day_basis must be TRADEIFY_ACCOUNT_DAY")
    rows = payload.get("dates")
    if not isinstance(rows, list) or not rows:
        raise CalendarError("overlay: dates must be a non-empty list")
    out = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"date", "label", "overrides_d19", "reason"}:
            raise CalendarError("overlay: each row needs exactly date/label/overrides_d19/reason")
        if row["overrides_d19"] is not True:
            raise CalendarError(f"overlay: {row.get('date')} must carry overrides_d19: true")
        try:
            day = date.fromisoformat(row["date"])
        except (TypeError, ValueError) as exc:
            raise CalendarError(f"overlay: bad date {row.get('date')!r}") from exc
        if not isinstance(row["reason"], str) or not row["reason"].strip():
            raise CalendarError(f"overlay: {day} needs a reason")
        if day in out:
            raise CalendarError(f"overlay: duplicate date {day}")
        out.add(day)
    return frozenset(out), hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class SessionCalendar:
    calendar_id: str
    calendar_digest: str
    overlay_digest: str
    timezone: str
    coverage_start: datetime
    coverage_end: datetime
    review_due: datetime
    rows: tuple[SessionSchedule, ...]
    products: tuple[str, ...]
    evidence_warning: str | None = None   # set when the evidence file predates per-capture product coverage

    def schedule_for(self, session_id: str) -> SessionSchedule | None:
        for row in self.rows:
            if row.session_id == session_id:
                return row
        return None

    def row_containing(self, now: datetime) -> SessionSchedule | None:
        for row in self.rows:
            if row.opens_at <= now < row.closes_at:
                return row
        return None

    def next_row_after(self, now: datetime) -> SessionSchedule | None:
        for row in self.rows:
            if row.opens_at > now:
                return row
        return None

    def session_for(self, now: datetime, *, expected_digest: str | None = None) -> SessionDecision:
        """Produce the BookSession that admits new risk at ``now``, or a refusal."""
        if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
            return SessionDecision(None, "invalid_now", None, self.calendar_digest)
        if expected_digest is not None and expected_digest != self.calendar_digest:
            return SessionDecision(None, "calendar_digest_mismatch", None, self.calendar_digest)
        warnings: list[str] = []
        if self.evidence_warning:
            warnings.append(self.evidence_warning)
        if now >= self.review_due:
            warnings.append("calendar_review_due")
        if now < self.coverage_start:
            return SessionDecision(None, "coverage_not_started", None, self.calendar_digest, tuple(warnings))
        if now >= self.coverage_end:
            return SessionDecision(None, "coverage_expired", None, self.calendar_digest, tuple(warnings))
        row = self.row_containing(now)
        if row is None:
            return SessionDecision(None, "no_session_at_now", None, self.calendar_digest, tuple(warnings))
        if row.overlay_blocked:
            return SessionDecision(None, "overlay_closure", row, self.calendar_digest, tuple(warnings))
        if row.permission != "PERMITTED":
            return SessionDecision(None, f"session_denied:{row.denial_reason}", row,
                                   self.calendar_digest, tuple(warnings))
        if now >= row.risk_add_cutoff:
            return SessionDecision(None, "after_risk_add_cutoff", row, self.calendar_digest, tuple(warnings))
        if now < row.admits_from:
            return SessionDecision(None, "before_product_open", row, self.calendar_digest, tuple(warnings))
        session = BookSession(row.session_id, row.prior_session_id, row.admits_from,
                              row.risk_add_cutoff, row.closes_at, self.calendar_digest)
        return SessionDecision(session, None, row, self.calendar_digest, tuple(warnings))


def _verify_row(row: dict, index: int, *, tz: ZoneInfo, venue: dict, rule: dict,
                products: dict, source_ids: set[str], overlay_dates: frozenset[date],
                coverage: dict[str, frozenset[str]] | None = None) -> SessionSchedule:
    label = f"sessions[{index}]"
    if not isinstance(row, dict) or set(row) != _ROW_KEYS:
        missing = _ROW_KEYS - set(row) if isinstance(row, dict) else _ROW_KEYS
        extra = set(row) - _ROW_KEYS if isinstance(row, dict) else set()
        raise CalendarError(f"{label}: key set mismatch (missing={sorted(missing)}, extra={sorted(extra)})")
    match = _SESSION_ID.match(row["session_id"]) if isinstance(row["session_id"], str) else None
    if match is None:
        raise CalendarError(f"{label}: session_id must be tradeify-account-day:YYYY-MM-DD")
    try:
        day = date.fromisoformat(match.group(1))
    except ValueError as exc:
        raise CalendarError(f"{label}: {exc}") from exc
    if row["account_date"] != day.isoformat():
        raise CalendarError(f"{label}: account_date must equal the session_id date")
    if day.weekday() >= 5:
        raise CalendarError(f"{label}: {day} is a weekend; no account session")
    if not isinstance(row["prior_session_id"], str) or not _SESSION_ID.match(row["prior_session_id"]):
        raise CalendarError(f"{label}: prior_session_id malformed")
    if row["prior_session_id"] == row["session_id"]:
        raise CalendarError(f"{label}: prior_session_id equals session_id")
    if row["permission"] not in _PERMISSIONS:
        raise CalendarError(f"{label}: permission must be PERMITTED or DENIED")
    denied = row["permission"] == "DENIED"
    if denied:
        if row["denial_reason"] not in _DENIAL_REASONS:
            raise CalendarError(f"{label}: denied row needs a typed denial_reason")
        if not isinstance(row["denial_note"], str) or not row["denial_note"].strip():
            raise CalendarError(f"{label}: denied row needs a denial_note")
    elif row["denial_reason"] is not None or row["denial_note"] is not None:
        raise CalendarError(f"{label}: permitted row must not carry a denial")
    if not isinstance(row["predecessor_in_file"], bool):
        raise CalendarError(f"{label}: predecessor_in_file must be boolean")

    opens_local = _local(row["opens_local"], tz, f"{label}.opens_local")
    closes_local = _local(row["closes_local"], tz, f"{label}.closes_local")
    venue_deadline_local = _local(row["venue_flat_deadline_local"], tz, f"{label}.venue_flat_deadline_local")
    opens = _utc(row["opens_utc"], f"{label}.opens_utc")
    closes = _utc(row["closes_utc"], f"{label}.closes_utc")
    v = _utc(row["v_utc"], f"{label}.v_utc")
    own_flat = _utc(row["own_flat_deadline_utc"], f"{label}.own_flat_deadline_utc")
    flatten_start = _utc(row["flatten_start_utc"], f"{label}.flatten_start_utc")
    cutoff = _utc(row["risk_add_cutoff_utc"], f"{label}.risk_add_cutoff_utc")
    if opens_local.astimezone(timezone.utc) != opens or closes_local.astimezone(timezone.utc) != closes:
        raise CalendarError(f"{label}: local/UTC mapping disagrees for the account day")

    open_h, open_m = _clock(venue["account_day_opens_local"], "venue.account_day_opens_local")
    close_h, close_m = _clock(venue["account_day_closes_local"], "venue.account_day_closes_local")
    if (opens_local.hour, opens_local.minute) != (open_h, open_m) or opens_local.date() != day - timedelta(days=1):
        raise CalendarError(f"{label}: account day must open at {venue['account_day_opens_local']} on the prior calendar day")
    if (closes_local.hour, closes_local.minute) != (close_h, close_m) or closes_local.date() != day:
        raise CalendarError(f"{label}: account day must close at {venue['account_day_closes_local']} on {day}")

    holiday = denied and row["denial_reason"] in ("HOLIDAY", "SHORTENED")
    expected_clock = venue["holiday_shortened_flat_deadline_local"] if holiday else venue["regular_flat_deadline_local"]
    exp_h, exp_m = _clock(expected_clock, "venue.flat_deadline")
    if (venue_deadline_local.hour, venue_deadline_local.minute) != (exp_h, exp_m) or venue_deadline_local.date() != day:
        raise CalendarError(f"{label}: venue flat deadline must be {expected_clock} on {day}")

    deadlines = [venue_deadline_local.astimezone(timezone.utc)]
    admits_from = opens
    prod_rows = row["products"]
    if not isinstance(prod_rows, dict) or set(prod_rows) != set(products):
        raise CalendarError(f"{label}: products must be exactly {sorted(products)}")
    for code, prow in prod_rows.items():
        plabel = f"{label}.products.{code}"
        if not isinstance(prow, dict) or not _PRODUCT_KEYS_REQUIRED <= set(prow):
            raise CalendarError(f"{plabel}: missing required keys")
        if not isinstance(prow["qualified"], bool):
            raise CalendarError(f"{plabel}: qualified must be boolean")
        if not denied and prow["qualified"] is not True:
            raise CalendarError(f"{plabel}: permitted session requires every product qualified")
        try:
            trade_date = date.fromisoformat(prow["cme_trade_date"])
        except (TypeError, ValueError) as exc:
            raise CalendarError(f"{plabel}: cme_trade_date") from exc
        if not (day - timedelta(days=1) <= trade_date <= day + timedelta(days=1)):
            raise CalendarError(f"{plabel}: cme_trade_date {trade_date} is not adjacent to the account day")
        if not isinstance(prow["source_ids"], list) or not prow["source_ids"] or \
                any(s not in source_ids for s in prow["source_ids"]):
            raise CalendarError(f"{plabel}: source_ids must name captured sources")
        if prow["qualified"] and not set(products[code].get("source_ids", [])) <= set(prow["source_ids"]):
            raise CalendarError(f"{plabel}: a qualified product row must cite its own product's declared sources")
        if coverage is not None and not any(code in coverage.get(s, frozenset()) for s in prow["source_ids"]):
            raise CalendarError(f"{plabel}: no cited capture covers product {code}")
        m_close = _utc(prow["matching_close_utc"], f"{plabel}.matching_close_utc")
        if prow["matching_open_utc"] is not None:
            m_open = _utc(prow["matching_open_utc"], f"{plabel}.matching_open_utc")
            if not (opens <= m_open < m_close <= closes):
                raise CalendarError(f"{plabel}: matching interval must sit inside the account day")
            if prow["qualified"]:
                admits_from = max(admits_from, m_open)
        elif prow["qualified"]:
            raise CalendarError(f"{plabel}: qualified product needs a matching open")
        if not (opens < m_close <= closes):
            raise CalendarError(f"{plabel}: matching close must fall inside the account day")
        deadlines.append(m_close)

    cap_h, cap_m = _clock(rule["own_flat_cap_local"], "schedule_rule.own_flat_cap_local")
    cap = datetime(day.year, day.month, day.day, cap_h, cap_m, tzinfo=tz).astimezone(timezone.utc)
    exp_v = min(deadlines)
    exp_own_flat = min(cap, exp_v - _minutes(rule["own_flat_before_v_minutes"], "own_flat_before_v_minutes"))
    exp_cutoff = exp_own_flat - _minutes(rule["cutoff_before_own_flat_minutes"], "cutoff_before_own_flat_minutes")
    exp_flatten = exp_own_flat - _minutes(rule["flatten_start_before_own_flat_minutes"], "flatten_start_before_own_flat_minutes")
    if (v, own_flat, cutoff, flatten_start) != (exp_v, exp_own_flat, exp_cutoff, exp_flatten):
        raise CalendarError(f"{label}: stored deadlines disagree with the section 5 formula "
                            f"(expected V={exp_v:%H:%MZ} D={exp_own_flat:%H:%MZ} cutoff={exp_cutoff:%H:%MZ} "
                            f"flatten={exp_flatten:%H:%MZ})")
    if not (opens < cutoff < flatten_start < own_flat <= v <= closes):
        raise CalendarError(f"{label}: no valid trading window")
    if not denied and admits_from >= cutoff:
        raise CalendarError(f"{label}: no product is open before the risk-add cutoff")
    if not isinstance(row["source_ids"], list) or not row["source_ids"] or \
            any(s not in source_ids for s in row["source_ids"]):
        raise CalendarError(f"{label}: source_ids must name captured sources")
    if not set(venue.get("source_ids", [])) <= set(row["source_ids"]):
        raise CalendarError(f"{label}: a session row must cite the venue's declared sources")
    return SessionSchedule(
        session_id=row["session_id"], prior_session_id=row["prior_session_id"],
        permission=row["permission"], denial_reason=row["denial_reason"],
        opens_at=opens, admits_from=admits_from, risk_add_cutoff=cutoff, flatten_start=flatten_start,
        own_flat_deadline=own_flat, v=v, closes_at=closes, overlay_blocked=day in overlay_dates,
    )


def load_session_calendar(path: Path, *, overlay_path: Path, repo_root: Path) -> SessionCalendar:
    """Load and fully verify the forward session file. Raises CalendarError on any defect."""
    data, payload = _read(path)
    if set(payload) != _TOP_KEYS:
        raise CalendarError(f"calendar: key set mismatch (missing={sorted(_TOP_KEYS - set(payload))}, "
                            f"extra={sorted(set(payload) - _TOP_KEYS)})")
    if payload["schema"] != SCHEMA:
        raise CalendarError("calendar: wrong schema")
    if not isinstance(payload["calendar_id"], str) or not payload["calendar_id"].strip():
        raise CalendarError("calendar: calendar_id required")
    if isinstance(payload["version"], bool) or not isinstance(payload["version"], int) or payload["version"] < 1:
        raise CalendarError("calendar: version must be a positive integer")
    venue = payload["venue"]
    if not isinstance(venue, dict) or venue.get("account_day_basis") != "TRADEIFY_ACCOUNT_DAY":
        raise CalendarError("calendar: venue.account_day_basis must be TRADEIFY_ACCOUNT_DAY")
    tz_name = venue.get("timezone")
    if tz_name != "America/New_York":
        raise CalendarError("calendar: venue.timezone must be America/New_York")
    tz = ZoneInfo(tz_name)
    for key in ("account_day_opens_local", "account_day_closes_local",
                "regular_flat_deadline_local", "holiday_shortened_flat_deadline_local"):
        _clock(venue.get(key), f"venue.{key}")
    rule = payload["schedule_rule"]
    if not isinstance(rule, dict) or set(rule) != {"owner", "own_flat_cap_local", "own_flat_before_v_minutes",
                                                    "cutoff_before_own_flat_minutes",
                                                    "flatten_start_before_own_flat_minutes"}:
        raise CalendarError("calendar: schedule_rule keys")
    if rule["owner"] != "docs/spec/2026-09-14-tb-s3-halt-resume-contract.md#5-exact-schedule-rule":
        raise CalendarError("calendar: schedule_rule.owner must cite TB-S3 rev9 section 5")
    if (rule["own_flat_cap_local"], rule["own_flat_before_v_minutes"], rule["cutoff_before_own_flat_minutes"],
            rule["flatten_start_before_own_flat_minutes"]) != ("16:00", 15, 15, 5):
        raise CalendarError("calendar: schedule_rule constants differ from section 5")
    products = payload["products"]
    if not isinstance(products, dict) or set(products) != {"6J", "MGC", "MYM", "MNQ"}:
        raise CalendarError("calendar: products must be exactly 6J/MGC/MYM/MNQ")

    sources = payload["sources"]
    if not isinstance(sources, dict) or set(sources) != {"evidence_file", "evidence_sha256", "ids"}:
        raise CalendarError("calendar: sources keys")
    evidence_path = (repo_root / sources["evidence_file"]).resolve()
    if repo_root.resolve() not in evidence_path.parents:
        raise CalendarError("calendar: evidence_file escapes the repository root")
    if not evidence_path.is_file():
        raise CalendarError("calendar: evidence_file missing")
    evidence_bytes = evidence_path.read_bytes()
    if hashlib.sha256(evidence_bytes).hexdigest() != sources["evidence_sha256"]:
        raise CalendarError("calendar: evidence_sha256 does not match the evidence file bytes")
    evidence = json.loads(evidence_bytes)
    captures = evidence.get("captures", [])
    if not isinstance(captures, list) or not captures or any(not isinstance(c, dict) or not isinstance(c.get("id"), str)
                                                              for c in captures):
        raise CalendarError("calendar: evidence captures")
    captured_ids = {c["id"] for c in captures}
    evidence_schema = evidence.get("schema")
    if evidence_schema == EVIDENCE_SCHEMA_V2:
        coverage: dict[str, frozenset[str]] | None = {}
        for c in captures:
            covered = c.get("products")
            if not isinstance(covered, list) or not covered or any(p not in {"6J", "MGC", "MYM", "MNQ"} for p in covered):
                raise CalendarError(f"calendar: capture {c['id']} must declare the products it covers")
            coverage[c["id"]] = frozenset(covered)
        evidence_warning = None
    elif evidence_schema == EVIDENCE_SCHEMA_V1:
        coverage = None                      # v1 captures carry no product coverage; every decision warns
        evidence_warning = EVIDENCE_V1_WARNING
    else:
        raise CalendarError("calendar: unknown evidence schema")
    if set(sources["ids"]) != captured_ids:
        raise CalendarError("calendar: sources.ids must equal the evidence capture ids")
    for spec in products.values():
        if any(s not in captured_ids for s in spec.get("source_ids", [])) or not spec.get("source_ids"):
            raise CalendarError("calendar: product source_ids must name captured sources")
    if any(s not in captured_ids for s in venue.get("source_ids", [])) or not venue.get("source_ids"):
        raise CalendarError("calendar: venue source_ids must name captured sources")

    overlay_dates, overlay_digest = load_closure_overlay(overlay_path)

    rows_raw = payload["sessions"]
    if not isinstance(rows_raw, list) or not rows_raw:
        raise CalendarError("calendar: sessions must be a non-empty list")
    rows: list[SessionSchedule] = []
    for index, raw in enumerate(rows_raw):
        row = _verify_row(raw, index, tz=tz, venue=venue, rule=rule, products=products,
                          source_ids=captured_ids, overlay_dates=overlay_dates, coverage=coverage)
        if index == 0:
            if raw["predecessor_in_file"] is not False:
                raise CalendarError("sessions[0]: predecessor_in_file must be false")
            first_day = date.fromisoformat(row.session_id.split(":")[1])
            expected_prev = first_day - timedelta(days=1)
            while expected_prev.weekday() >= 5:
                expected_prev -= timedelta(days=1)
            if row.prior_session_id.split(":")[1] != expected_prev.isoformat():
                raise CalendarError("sessions[0]: prior_session_id must be the immediately preceding account day")
        else:
            prev = rows[-1]
            if raw["predecessor_in_file"] is not True:
                raise CalendarError(f"sessions[{index}]: predecessor_in_file must be true")
            if row.prior_session_id != prev.session_id:
                raise CalendarError(f"sessions[{index}]: prior_session_id must be the preceding row "
                                    f"({prev.session_id}); denied days stay in the chain")
            if row.opens_at < prev.closes_at:
                raise CalendarError(f"sessions[{index}]: overlaps the preceding session")
            this_day = date.fromisoformat(row.session_id.split(":")[1])
            prev_day = date.fromisoformat(prev.session_id.split(":")[1])
            expected_prev = this_day - timedelta(days=1)
            while expected_prev.weekday() >= 5:
                expected_prev -= timedelta(days=1)
            if prev_day != expected_prev:
                raise CalendarError(f"sessions[{index}]: account day {expected_prev} is missing before "
                                    f"{this_day}; every Monday-Friday account day needs its own row")
        rows.append(row)
    ids = [r.session_id for r in rows]
    if len(set(ids)) != len(ids):
        raise CalendarError("calendar: duplicate session ids")

    coverage = payload["coverage"]
    if not isinstance(coverage, dict) or set(coverage) != {"first_session_id", "last_session_id", "coverage_start_utc",
                                                          "coverage_end_utc", "review_due_utc", "horizon_authority"}:
        raise CalendarError("calendar: coverage keys")
    if coverage["first_session_id"] != rows[0].session_id or coverage["last_session_id"] != rows[-1].session_id:
        raise CalendarError("calendar: coverage session ids disagree with the rows")
    start = _utc(coverage["coverage_start_utc"], "coverage.coverage_start_utc")
    end = _utc(coverage["coverage_end_utc"], "coverage.coverage_end_utc")
    review_due = _utc(coverage["review_due_utc"], "coverage.review_due_utc")
    if start != rows[0].opens_at or end != rows[-1].closes_at:
        raise CalendarError("calendar: coverage bounds must equal the first open and last close")
    if not (start < review_due <= end):
        raise CalendarError("calendar: review_due_utc must fall inside coverage")
    policy = payload["first_release_policy"]
    if not isinstance(policy, dict) or policy.get("permit_only") != "QUALIFIED_ORDINARY" or \
            set(policy.get("deny", [])) != _DENIAL_REASONS:
        raise CalendarError("calendar: first_release_policy must permit only QUALIFIED_ORDINARY and deny the typed reasons")

    return SessionCalendar(
        calendar_id=payload["calendar_id"], calendar_digest=hashlib.sha256(data).hexdigest(),
        overlay_digest=overlay_digest, timezone=tz_name, coverage_start=start, coverage_end=end,
        review_due=review_due, rows=tuple(rows), products=tuple(sorted(products)),
        evidence_warning=evidence_warning,
    )


def load_ratifications(path: Path) -> dict[str, dict]:
    """Return operator ratification rows keyed by calendar digest; malformed files refuse whole."""
    data, payload = _read(path)
    if set(payload) != {"schema", "note", "ratifications"} or payload["schema"] != RATIFICATION_SCHEMA:
        raise CalendarError("ratification: wrong schema or keys")
    rows = payload["ratifications"]
    if not isinstance(rows, list):
        raise CalendarError("ratification: ratifications must be a list")
    out: dict[str, dict] = {}
    for index, row in enumerate(rows):
        label = f"ratifications[{index}]"
        if not isinstance(row, dict) or set(row) != _RATIFICATION_KEYS:
            raise CalendarError(f"{label}: key set mismatch")
        for key in ("calendar_sha256", "closure_overlay_sha256"):
            if not isinstance(row[key], str) or not _HEX64.fullmatch(row[key]):
                raise CalendarError(f"{label}.{key}: expected lowercase 64-hex")
        for key in ("calendar_id", "calendar_file", "closure_overlay_file", "ratified_by",
                    "instruction", "record", "scope"):
            if not isinstance(row[key], str) or not row[key].strip():
                raise CalendarError(f"{label}.{key}: required")
        if row["ratified_by"] != "operator":
            raise CalendarError(f"{label}: only the operator ratifies a calendar")
        start = _utc(row["coverage_start_utc"], f"{label}.coverage_start_utc")
        end = _utc(row["coverage_end_utc"], f"{label}.coverage_end_utc")
        ratified = _utc_event(row["ratified_utc"], f"{label}.ratified_utc")
        if not start < end:
            raise CalendarError(f"{label}: coverage bounds")
        if ratified >= end:
            raise CalendarError(f"{label}: ratified after coverage expiry")
        if row["calendar_sha256"] in out:
            raise CalendarError(f"{label}: duplicate ratification for one digest")
        out[row["calendar_sha256"]] = row
    return out


def load_ratified_calendar(path: Path, *, overlay_path: Path, ratified_path: Path,
                           repo_root: Path) -> SessionCalendar:
    """Load a calendar and refuse it unless the operator ratified exactly these bytes."""
    calendar = load_session_calendar(path, overlay_path=overlay_path, repo_root=repo_root)
    row = load_ratifications(ratified_path).get(calendar.calendar_digest)
    if row is None:
        raise CalendarError("calendar_not_ratified")
    if row["closure_overlay_sha256"] != calendar.overlay_digest:
        raise CalendarError("overlay_not_ratified")
    if row["calendar_id"] != calendar.calendar_id:
        raise CalendarError("ratification_calendar_id_mismatch")
    bounds = (_utc(row["coverage_start_utc"], "coverage_start_utc"),
              _utc(row["coverage_end_utc"], "coverage_end_utc"))
    if bounds != (calendar.coverage_start, calendar.coverage_end):
        raise CalendarError("ratification_coverage_mismatch")
    return calendar
