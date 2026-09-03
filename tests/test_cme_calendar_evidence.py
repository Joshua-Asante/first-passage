"""Synthetic captures exercise provenance, completeness, and deadline consumption."""
import json
from hashlib import sha256
import os

import pytest

from research_utils.trade_reconciliation import load_early_close_calendar, analyze_venue
from test_trade_reconciliation import _trades, _trade, _spec, fee_schedule


def calendar_fixture(tmp_path):
    capture_dir = tmp_path / "local_artifacts" / "calendar_captures"
    capture_dir.mkdir(parents=True)
    payload = {
        "source_url": "https://www.cmegroup.com/trading-hours.html",
        "page_date": None, "observed_date": "2026-09-03",
        "coverage_start": "2025-01-01", "coverage_end": "2026-12-31",
        "coverage_status": "COMPLETE", "coverage_note": "Synthetic evidence only",
        "sources": [], "rows": [],
    }
    for year in (2025, 2026):
        row = {"date": f"{year}-01-05", "deadline_local": "12:59 America/New_York"}
        capture = {"year": year, "source_url": payload["source_url"],
                   "page_date": "2026-09-03", "rows": [row]}
        raw = json.dumps(capture).encode()
        basename = f"{year}.json"
        (capture_dir / basename).write_bytes(raw)
        payload["sources"].append({k: capture[k] for k in ("year", "source_url", "page_date")}
                                  | {"capture_basename": basename, "sha256": sha256(raw).hexdigest()})
        payload["rows"].append(row | {"source_year": year})
    path = tmp_path / "calendar.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path, payload, capture_dir


def test_loaded_capture_drives_deadline_and_freezes_input_bytes(tmp_path, fee_schedule):
    path, payload, captures = calendar_fixture(tmp_path)
    calendar = load_early_close_calendar(path)
    assert calendar.input_sha256 == sha256(path.read_bytes()).hexdigest()
    assert len(calendar.sources) == 2
    venue = analyze_venue(_trades(_trade(1, "2026-01-05 13:00", "1.00", "1.82")), _spec(), fee_schedule,
                          early_close_calendar=calendar)
    assert venue.overnight_holds == 1
    assert any(i.code == "FORCE_FLAT_VIOLATION" for i in venue.issues)


@pytest.mark.parametrize("mutation", [
    "duplicate_source", "hash", "page_date", "url", "source_bool", "unknown_year",
    "inconsistent_year", "row_bool", "missing_year", "missing_rows", "extra_top",
    "extra_source", "extra_row", "traversal", "missing_capture", "mismatch_capture",
    "wrong_capture_year", "wrong_capture_metadata", "wrong_capture_row_year",
    "removed_captured_row", "empty_complete", "capture_extra_key",
])
def test_invalid_evidence_cannot_certify_complete(tmp_path, mutation):
    path, p, captures = calendar_fixture(tmp_path)
    assert load_early_close_calendar(path).coverage_status == "COMPLETE"
    s = p["sources"][0]
    if mutation == "duplicate_source": p["sources"].append(dict(s))
    elif mutation == "hash": s["sha256"] = "A" * 64
    elif mutation == "page_date": s["page_date"] = None
    elif mutation == "url": s["source_url"] = "https://cmegroup.com.evil.test/calendar"
    elif mutation == "source_bool": s["year"] = True
    elif mutation == "unknown_year": p["rows"][0]["source_year"] = 2024
    elif mutation == "inconsistent_year": p["rows"][0]["source_year"] = 2026
    elif mutation == "row_bool": p["rows"][0]["source_year"] = True
    elif mutation == "missing_year": p["sources"].pop()
    elif mutation == "missing_rows": p["rows"].pop()
    elif mutation == "extra_top": p["extra"] = 1
    elif mutation == "extra_source": s["extra"] = 1
    elif mutation == "extra_row": p["rows"][0]["extra"] = 1
    elif mutation == "traversal": s["capture_basename"] = "../2025.json"
    elif mutation == "missing_capture": (captures / "2025.json").unlink()
    elif mutation == "mismatch_capture": (captures / "2025.json").write_bytes(b"different")
    elif mutation == "empty_complete": p["rows"] = []; p["sources"] = []
    else:
        c = json.loads((captures / "2025.json").read_bytes())
        if mutation == "wrong_capture_year": c["year"] = 2024
        elif mutation == "wrong_capture_metadata": c["page_date"] = "2026-09-02"
        elif mutation == "wrong_capture_row_year": c["rows"][0]["date"] = "2024-01-05"
        elif mutation == "capture_extra_key": c["extra"] = 1
        elif mutation == "removed_captured_row": c["rows"].append({"date": "2025-02-05", "deadline_local": "12:59 America/New_York"})
        raw = json.dumps(c).encode()
        (captures / "2025.json").write_bytes(raw)
        s["sha256"] = sha256(raw).hexdigest()
    path.write_text(json.dumps(p), encoding="utf-8")
    with pytest.raises(ValueError):
        load_early_close_calendar(path)


def test_invalid_utf8_is_configuration_error(tmp_path):
    path = tmp_path / "calendar.json"
    path.write_bytes(b"\xff")
    with pytest.raises(ValueError, match="cannot load CME"):
        load_early_close_calendar(path)


def test_symlink_capture_cannot_escape_directory(tmp_path):
    path, p, captures = calendar_fixture(tmp_path)
    original = captures / "2025.json"
    outside = tmp_path / "outside.json"
    outside.write_bytes(original.read_bytes())
    link = captures / "escape.json"
    try:
        os.symlink(outside, link)
    except OSError as exc:
        pytest.skip(f"OS does not grant file symlink privilege: {exc}")
    p["sources"][0]["capture_basename"] = "escape.json"
    path.write_text(json.dumps(p), encoding="utf-8")
    with pytest.raises(ValueError, match="escapes"):
        load_early_close_calendar(path)


def test_fully_covered_year_cannot_have_no_observed_rows(tmp_path):
    path, p, captures = calendar_fixture(tmp_path)
    p["rows"] = p["rows"][1:]
    capture = json.loads((captures / "2025.json").read_bytes())
    capture["rows"] = []
    raw = json.dumps(capture).encode()
    (captures / "2025.json").write_bytes(raw)
    p["sources"][0]["sha256"] = sha256(raw).hexdigest()
    path.write_text(json.dumps(p), encoding="utf-8")
    with pytest.raises(ValueError, match="fully covered year"):
        load_early_close_calendar(path)
