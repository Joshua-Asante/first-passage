"""Strict adapter for the explicitly limited Tradeify secondary calendar."""

from __future__ import annotations

from datetime import date, time
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import re
from types import MappingProxyType
from typing import Mapping


_REPO_ROOT = Path(__file__).resolve().parents[2]
_SOURCE_PATH = "ops/calendars/cme_holiday_calendar_2022_2026.json"
_WRAPPER_KEYS = {
    "schema", "source_url", "page_date", "observed_date", "coverage_start",
    "coverage_end", "coverage_status", "coverage_note", "source_calendar", "rows",
}
_SOURCE_KEYS = {
    "schema", "generated", "coverage_start", "coverage_end", "provenance",
    "provenance_note", "day_basis", "product_groups", "derived", "entries",
    "source_urls", "unresolved", "source_revisions",
}
_ENTRY_KEYS = {
    "date", "holiday", "equity_index_status", "equity_index_close_et",
    "metals_status", "metals_close_et", "fx_status", "fx_close_et", "confidence", "note",
}
_STATUSES = {"EARLY_CLOSE", "FULL_CLOSURE", "NORMAL"}
_GROUPS = ("equity_index", "metals", "fx")
_HASH_RE = re.compile(r"[0-9a-f]{64}")
_GIT_SHA_RE = re.compile(r"[0-9a-f]{40}")


def _freeze(value: object) -> object:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _date(value: object, field: str) -> date:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a canonical ISO date")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be a canonical ISO date") from exc
    if parsed.isoformat() != value:
        raise ValueError(f"{field} must be a canonical ISO date")
    return parsed


def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _clock(value: object, field: str, *, required: bool) -> str:
    if value == "" and not required:
        return ""
    if not isinstance(value, str) or not re.fullmatch(r"[0-2][0-9]:[0-5][0-9]", value):
        raise ValueError(f"{field} must be an HH:MM ET time")
    try:
        time.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be an HH:MM ET time") from exc
    return value


def _dates(value: object, field: str) -> tuple[date, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be an array")
    parsed = tuple(_date(item, field) for item in value)
    if len(parsed) != len(set(parsed)) or tuple(sorted(parsed)) != parsed:
        raise ValueError(f"{field} must contain sorted, unique canonical dates")
    return parsed


def _derived_dates(value: object, field: str) -> tuple[date, ...]:
    if not isinstance(value, dict) or set(value) != {"rule", "count", "dates"}:
        raise ValueError(f"{field} keys mismatch")
    _text(value["rule"], f"{field}.rule")
    if type(value["count"]) is not int or value["count"] < 0:
        raise ValueError(f"{field}.count must be a non-negative integer")
    dates = _dates(value["dates"], f"{field}.dates")
    if value["count"] != len(dates):
        raise ValueError(f"{field}.count does not match dates")
    return dates


def _safe_source_path(value: object, repo_root: Path) -> Path:
    if value != _SOURCE_PATH:
        raise ValueError("source_calendar.repo_path must identify the approved secondary calendar")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts) or "\\" in value:
        raise ValueError("source_calendar.repo_path must be a safe repo-relative path")
    target = (repo_root / Path(*path.parts)).resolve()
    if not target.is_relative_to(repo_root) or target != (repo_root / _SOURCE_PATH).resolve():
        raise ValueError("source_calendar path escapes repository root")
    return target


def _read_json(path: Path, field: str) -> tuple[bytes, dict[str, object]]:
    try:
        raw = path.read_bytes()
        payload = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load {field}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{field} must be a JSON object")
    return raw, payload


def _validate_source(source: dict[str, object]) -> tuple[date, date, set[date], Mapping[str, object]]:
    if set(source) != _SOURCE_KEYS:
        raise ValueError("secondary source calendar keys mismatch")
    if source["schema"] != "cme_holiday_calendar/v1" or source["provenance"] != "SECONDARY":
        raise ValueError("secondary source calendar schema/provenance mismatch")
    _date(source["generated"], "source generated")
    coverage_start = _date(source["coverage_start"], "source coverage_start")
    coverage_end = _date(source["coverage_end"], "source coverage_end")
    if coverage_start > coverage_end:
        raise ValueError("source coverage_start must not be after coverage_end")
    _text(source["provenance_note"], "source provenance_note")
    if not isinstance(source["day_basis"], dict) or set(source["day_basis"]) != {"basis", "note"}:
        raise ValueError("source day_basis keys mismatch")
    if source["day_basis"]["basis"] != "CME_TRADE_DATE":
        raise ValueError("source day_basis must be CME_TRADE_DATE")
    _text(source["day_basis"]["note"], "source day_basis.note")
    if not isinstance(source["product_groups"], dict) or set(source["product_groups"]) != set(_GROUPS):
        raise ValueError("source product_groups keys mismatch")
    for group in _GROUPS:
        _text(source["product_groups"][group], f"source product_groups.{group}")
    if not isinstance(source["source_urls"], list) or not source["source_urls"]:
        raise ValueError("source_urls must be a non-empty array")
    for item in source["source_urls"]:
        _text(item, "source_urls item")  # Inert provenance; never dereferenced.
    if not isinstance(source["unresolved"], list):
        raise ValueError("unresolved must be an array")
    for item in source["unresolved"]:
        if not isinstance(item, dict) or set(item) != {"date", "issue"}:
            raise ValueError("unresolved item keys mismatch")
        _date(item["date"], "unresolved date")
        _text(item["issue"], "unresolved issue")
    revisions = source["source_revisions"]
    if not isinstance(revisions, dict) or set(revisions) != {"pinned_at", "pins", "note"}:
        raise ValueError("source_revisions keys mismatch")
    _date(revisions["pinned_at"], "source_revisions.pinned_at")
    if not isinstance(revisions["pins"], dict) or not revisions["pins"]:
        raise ValueError("source_revisions.pins must be a non-empty map")
    for repository, revision in revisions["pins"].items():
        _text(repository, "source_revisions repository")
        if not isinstance(revision, str) or not _GIT_SHA_RE.fullmatch(revision):
            raise ValueError("source_revisions pins must be lowercase 40-character Git SHAs")
    _text(revisions["note"], "source_revisions.note")

    entries = source["entries"]
    if not isinstance(entries, list) or not entries:
        raise ValueError("entries must be a non-empty array")
    early_dates: set[date] = set()
    full_dates: set[date] = set()
    pre_deadline: dict[date, dict[str, str]] = {}
    entry_dates: set[date] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or set(entry) != _ENTRY_KEYS:
            raise ValueError(f"entries[{index}] keys mismatch")
        entry_date = _date(entry["date"], f"entries[{index}].date")
        if entry_date in entry_dates or not coverage_start <= entry_date <= coverage_end:
            raise ValueError("entry date duplicate or outside source coverage")
        entry_dates.add(entry_date)
        _text(entry["holiday"], f"entries[{index}].holiday")
        _text(entry["note"], f"entries[{index}].note")
        if entry["confidence"] not in {"HIGH", "MEDIUM", "LOW"}:
            raise ValueError("entry confidence must be HIGH, MEDIUM, or LOW")
        statuses = []
        closes: dict[str, str] = {}
        for group in _GROUPS:
            status = entry[f"{group}_status"]
            if status not in _STATUSES:
                raise ValueError("entry status must be EARLY_CLOSE, FULL_CLOSURE, or NORMAL")
            statuses.append(status)
            close = _clock(entry[f"{group}_close_et"], f"entries[{index}].{group}_close_et", required=status == "EARLY_CLOSE")
            if status != "EARLY_CLOSE" and close:
                raise ValueError("only EARLY_CLOSE entries may declare a close time")
            if status == "EARLY_CLOSE":
                closes[group] = close
        if "EARLY_CLOSE" in statuses:
            early_dates.add(entry_date)
        if all(status == "FULL_CLOSURE" for status in statuses):
            full_dates.add(entry_date)
        early_before = {group: close for group, close in closes.items() if close < "12:59"}
        if early_before:
            pre_deadline[entry_date] = early_before

    derived = source["derived"]
    if not isinstance(derived, dict) or set(derived) != {"venue_flat_dates", "full_closure_dates", "sub_deadline_close_dates"}:
        raise ValueError("derived keys mismatch")
    if set(_derived_dates(derived["venue_flat_dates"], "derived.venue_flat_dates")) != early_dates:
        raise ValueError("derived venue_flat_dates disagree with EARLY_CLOSE entry union")
    if set(_derived_dates(derived["full_closure_dates"], "derived.full_closure_dates")) != full_dates:
        raise ValueError("derived full_closure_dates disagree with entries")
    sub = derived["sub_deadline_close_dates"]
    if not isinstance(sub, dict) or set(sub) != {"rule", "count", "dates"}:
        raise ValueError("derived.sub_deadline_close_dates keys mismatch")
    _text(sub["rule"], "derived.sub_deadline_close_dates.rule")
    if type(sub["count"]) is not int or sub["count"] < 0 or not isinstance(sub["dates"], list):
        raise ValueError("derived.sub_deadline_close_dates is malformed")
    supplied_sub: dict[date, dict[str, str]] = {}
    for item in sub["dates"]:
        if not isinstance(item, dict) or set(item) != {"date", "holiday", "closes_et"}:
            raise ValueError("derived.sub_deadline_close_dates item keys mismatch")
        day = _date(item["date"], "derived.sub_deadline_close_dates date")
        _text(item["holiday"], "derived.sub_deadline_close_dates holiday")
        if day in supplied_sub or not isinstance(item["closes_et"], dict) or not item["closes_et"]:
            raise ValueError("derived.sub_deadline_close_dates must have unique, non-empty close maps")
        close_map: dict[str, str] = {}
        for group, close in item["closes_et"].items():
            if group not in _GROUPS or _clock(close, "derived.sub_deadline_close_dates close", required=True) >= "12:59":
                raise ValueError("derived sub-deadline close must name a group and precede 12:59")
            close_map[group] = close
        supplied_sub[day] = close_map
    if sub["count"] != len(supplied_sub) or supplied_sub != pre_deadline:
        raise ValueError("derived sub_deadline_close_dates disagree with entries")
    metadata = {
        "schema": source["schema"], "provenance": source["provenance"],
        "provenance_note": source["provenance_note"], "source_urls": source["source_urls"],
        "day_basis": source["day_basis"], "full_closure_dates": derived["full_closure_dates"],
        "sub_deadline_close_dates": derived["sub_deadline_close_dates"],
        "unresolved": source["unresolved"], "source_revisions": source["source_revisions"],
    }
    return coverage_start, coverage_end, early_dates, MappingProxyType(metadata)


def load_secondary_early_close_calendar(
    path: str | Path, *, repo_root: str | Path | None = None, _raw: bytes | None = None,
):
    """Load the limited secondary evidence without ever certifying COMPLETE."""
    wrapper_path = Path(path)
    if _raw is None:
        raw, wrapper = _read_json(wrapper_path, "secondary early-close wrapper")
    else:
        raw = _raw
        try:
            wrapper = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("cannot load secondary early-close wrapper") from exc
        if not isinstance(wrapper, dict):
            raise ValueError("secondary early-close wrapper must be a JSON object")
    if set(wrapper) != _WRAPPER_KEYS or wrapper["schema"] != "tradeify_secondary_early_close/v1":
        raise ValueError("secondary early-close wrapper keys/schema mismatch")
    for field in ("source_url", "coverage_note"):
        _text(wrapper[field], field)
    if wrapper["coverage_status"] != "NEEDS_CONTEXT":
        raise ValueError("secondary coverage_status must be NEEDS_CONTEXT")
    page_date = _date(wrapper["page_date"], "page_date")
    observed_date = _date(wrapper["observed_date"], "observed_date")
    coverage_start = _date(wrapper["coverage_start"], "coverage_start")
    coverage_end = _date(wrapper["coverage_end"], "coverage_end")
    if coverage_start > coverage_end:
        raise ValueError("coverage_start must not be after coverage_end")
    source_ref = wrapper["source_calendar"]
    if not isinstance(source_ref, dict) or set(source_ref) != {"repo_path", "sha256"}:
        raise ValueError("source_calendar keys mismatch")
    if not isinstance(source_ref["sha256"], str) or not _HASH_RE.fullmatch(source_ref["sha256"]):
        raise ValueError("source_calendar.sha256 must be lowercase SHA256")
    root = Path(repo_root).resolve() if repo_root is not None else _REPO_ROOT.resolve()
    source_path = _safe_source_path(source_ref["repo_path"], root)
    source_raw, source = _read_json(source_path, "secondary source calendar")
    if sha256(source_raw).hexdigest() != source_ref["sha256"]:
        raise ValueError("secondary source calendar SHA256 mismatch")
    source_start, source_end, early_dates, metadata = _validate_source(source)
    if coverage_start < source_start or coverage_end > source_end:
        raise ValueError("secondary wrapper coverage must fit source coverage")
    rows = wrapper["rows"]
    if not isinstance(rows, list):
        raise ValueError("secondary rows must be an array")
    supplied: set[date] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {"date", "deadline_local"}:
            raise ValueError(f"secondary rows[{index}] keys mismatch")
        day = _date(row["date"], f"secondary rows[{index}].date")
        if day in supplied or not coverage_start <= day <= coverage_end:
            raise ValueError("secondary calendar row duplicate or outside coverage")
        if row["deadline_local"] != "12:59 America/New_York":
            raise ValueError("secondary deadline must be 12:59 America/New_York")
        supplied.add(day)
    expected = {day for day in early_dates if coverage_start <= day <= coverage_end}
    if supplied != expected:
        raise ValueError("secondary rows must exactly equal the EARLY_CLOSE union within coverage")

    # Delayed import keeps this schema adapter independent from reconciliation logic.
    from research_utils.trade_reconciliation import EarlyCloseCalendar

    evidence_metadata = dict(metadata) | {
        "source_calendar": {"repo_path": source_ref["repo_path"], "sha256": source_ref["sha256"]},
    }
    return EarlyCloseCalendar(
        source_url=wrapper["source_url"], page_date=page_date, observed_date=observed_date,
        coverage_start=coverage_start, coverage_end=coverage_end, coverage_status="NEEDS_CONTEXT",
        coverage_note=wrapper["coverage_note"], early_close_dates=frozenset(supplied),
        input_sha256=sha256(raw).hexdigest(), evidence_kind="SECONDARY",
        source_calendar_sha256=sha256(source_raw).hexdigest(), evidence_metadata=_freeze(evidence_metadata),
    )
