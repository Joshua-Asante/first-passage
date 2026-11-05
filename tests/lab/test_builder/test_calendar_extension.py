"""The 2016-2026 CME holiday calendar extension (accepted by Joshua 2026-11-04): it parses under the
builder's loader and the strict v1 adapter, and its 2022-2026 part equals the accepted D19 file."""
from __future__ import annotations

import json
from pathlib import Path

from builder import data
from research_utils import secondary_calendar_evidence as sce

CAL = Path(__file__).resolve().parents[3] / "ops" / "calendars"
NEW, OLD = CAL / "cme_holiday_calendar_2016_2026.json", CAL / "cme_holiday_calendar_2022_2026.json"
OLD_SHA = "2698f2688cce582b08df58516fd770fa4a71a18de04870d9c14511731ea181e9"  # the D19 file at admission


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def test_the_accepted_file_is_unchanged():
    assert data.file_sha256(OLD) == OLD_SHA


def test_2022_2026_date_membership_equals_the_accepted_file():
    new = {e["date"] for e in load(NEW)["entries"] if e["date"] >= "2022-01-01"}
    assert new == {e["date"] for e in load(OLD)["entries"]}


def test_2022_2026_entries_are_copied_verbatim():
    assert [e for e in load(NEW)["entries"] if e["date"] >= "2022-01-01"] == load(OLD)["entries"]


def test_builder_loader_parses_schema_and_coverage():
    cal = data.load_calendar(NEW, data.file_sha256(NEW))
    assert (cal.start, cal.end) == ("2016-01-01", "2026-12-31")
    assert all(cal.start <= d <= cal.end for d in cal.closed)
    assert min(cal.closed) < "2022-01-01" and cal.closed >= data.load_calendar(OLD, OLD_SHA).closed
    cal.check_covers(["2016-01-04", "2019-05-06", "2026-12-31"], "MES")  # 2019 sessions are now covered


def test_strict_v1_adapter_accepts_the_file_and_its_derived_lists():
    """The adapter checks exact key sets, statuses, close times and that every derived list
    re-derives from the entries, so this also shows no extra field (e.g. energy) was added."""
    start, end, early, _ = sce._validate_source(load(NEW))  # pylint: disable=protected-access
    assert (start.isoformat(), end.isoformat()) == ("2016-01-01", "2026-12-31")
    _, _, old_early, _ = sce._validate_source(load(OLD))  # pylint: disable=protected-access
    assert {d for d in early if d.year >= 2022} == old_early


def test_extension_rows_are_weekdays_with_a_non_normal_group_and_unique():
    rows = [e for e in load(NEW)["entries"] if e["date"] < "2022-01-01"]
    dates = [e["date"] for e in rows]
    assert dates == sorted(set(dates)) and len(rows) == 67
    from datetime import date
    assert all(date.fromisoformat(d).weekday() < 5 for d in dates)
    assert all(any(e[f"{g}_status"] != "NORMAL" for g in ("equity_index", "metals", "fx")) for e in rows)
