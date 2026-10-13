"""G0 forward session calendar for the personal instance (card 2026-10-12, G0-a).

Binds the personal instance to Tradeify-authored ``book_session_calendar/v1`` files,
unchanged, admitted only through the personal ratification registry. Every byte is
checked against the binding's pins before parsing; the schedule rule, first-release
denials and ratification are enforced by the loader in ``book_session_calendar``.
Refusals added here: ``binding_digest_mismatch``, ``coverage_gap`` and
``binding_schema``. No weekday fallback.

Outside the trust domain while no trust-domain module imports it (G0-b is separate).
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from calendar_evidence import read_json_object
from .book_session_calendar import CalendarError, SessionCalendar, SessionDecision, load_ratified_calendar

SCHEMA = "personal_calendar_binding/v1"
_KEYS = frozenset({"_comment", "schema", "instance", "schedule_rule", "first_release_policy_deny",
                   "ratification_registry", "closure_overlay", "calendars"})
_SCHEDULE_RULE = {"owner": "docs/spec/2026-09-14-tb-s3-halt-resume-contract.md#5-exact-schedule-rule",
                  "own_flat_cap_local": "16:00", "own_flat_before_v_minutes": 15,
                  "cutoff_before_own_flat_minutes": 15, "flatten_start_before_own_flat_minutes": 5}
_DENY = {"HOLIDAY", "SHORTENED", "UNCERTAIN_ADJACENT", "MISSING_SOURCE"}


def _schema(ok: bool, what: str) -> None:
    if not ok:
        raise CalendarError(f"binding_schema: {what}")


def _pinned(repo_root: Path, rel: object, pin: object) -> Path:
    _schema(isinstance(rel, str) and isinstance(pin, str), "file/sha256 must be strings")
    path = (repo_root / rel).resolve()
    _schema(repo_root.resolve() in path.parents, f"{rel} escapes the repository root")
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != pin:
        raise CalendarError(f"binding_digest_mismatch: {rel}")
    return path


@dataclass(frozen=True)
class PersonalCalendarBinding:
    calendars: tuple[SessionCalendar, ...]   # listed order; coverage chains without a gap

    def session_for(self, now: datetime) -> SessionDecision:
        covering = [c for c in self.calendars
                    if isinstance(now, datetime) and now.tzinfo is not None
                    and c.coverage_start <= now < c.coverage_end]
        if covering:   # overlap: the later-ratified file wins (ties: later listed)
            chosen = max(enumerate(covering), key=lambda ic: (ic[1].ratified_at, ic[0]))[1]
        elif not isinstance(now, datetime) or now.tzinfo is None or now < self.calendars[0].coverage_start:
            chosen = self.calendars[0]
        elif now >= self.calendars[-1].coverage_end:
            chosen = self.calendars[-1]
        else:
            return SessionDecision(None, "coverage_gap", None, "")
        return chosen.session_for(now, expected_digest=chosen.calendar_digest)


def load_personal_calendar_binding(path: Path, *, repo_root: Path) -> PersonalCalendarBinding:
    """Load the binding; any defect, digest drift, gap or unratified calendar refuses whole."""
    try:
        doc = read_json_object(Path(path).read_bytes())
    except ValueError as exc:
        raise CalendarError(f"binding_schema: not JSON ({exc})") from exc
    _schema(isinstance(doc, dict) and set(doc) == _KEYS, "key set")
    _schema(doc["schema"] == SCHEMA and doc["instance"] == "personal_tradovate", "schema/instance")
    _schema(doc["schedule_rule"] == _SCHEDULE_RULE, "schedule_rule differs from TB-S3 section 5")
    _schema(isinstance(doc["first_release_policy_deny"], list)
            and set(doc["first_release_policy_deny"]) == _DENY, "first_release_policy_deny")
    overlay = doc["closure_overlay"]
    _schema(isinstance(overlay, dict) and set(overlay) == {"file", "sha256"}, "closure_overlay keys")
    rows = doc["calendars"]
    _schema(isinstance(rows, list) and rows and all(isinstance(r, dict) and set(r) == {
        "calendar_file", "calendar_sha256"} for r in rows), "calendars")
    registry = doc["ratification_registry"]
    _schema(registry == "ops/calendars/personal/RATIFIED.json", "ratification_registry must be the personal registry")

    overlay_path = _pinned(repo_root, overlay["file"], overlay["sha256"])
    paths = [_pinned(repo_root, r["calendar_file"], r["calendar_sha256"]) for r in rows]
    calendars = tuple(load_ratified_calendar(p, overlay_path=overlay_path, ratified_path=repo_root / registry,
                                             repo_root=repo_root) for p in paths)
    # The loader re-reads each path; its digests are of the bytes it parsed. Bind those to the pins.
    for row, calendar in zip(rows, calendars):
        if (calendar.calendar_digest, calendar.overlay_digest) != (row["calendar_sha256"], overlay["sha256"]):
            raise CalendarError(f"binding_digest_mismatch: {row['calendar_file']} changed after the pin check")
    for prev, nxt in zip(calendars, calendars[1:]):
        if not prev.coverage_start < nxt.coverage_start <= prev.coverage_end:
            raise CalendarError(f"coverage_gap: {nxt.calendar_id} does not chain from {prev.calendar_id}")
    return PersonalCalendarBinding(calendars)
