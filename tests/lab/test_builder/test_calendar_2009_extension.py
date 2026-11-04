"""The 2009-2026 CME holiday calendar (accepted by Joshua 2026-11-04): it parses under the builder's loader and
the strict v1 adapter, its 2016-2026 part equals the accepted file, and every 2009-2015 row cites a primary source."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from builder import data
from research_utils import secondary_calendar_evidence as sce

CAL = Path(__file__).resolve().parents[3] / "ops" / "calendars"
NEW = CAL / "cme_holiday_calendar_2009_2026.json"
ACCEPTED = CAL / "cme_holiday_calendar_2016_2026.json"
EVIDENCE = CAL / "evidence" / "2026-11-04-cme-2009-2015-wayback-captures.json"
PINS = {
    NEW: "067a7a5b73b07c55de1102be39c90e11fc6479d66e013c59592aa3d4a86efadd",
    ACCEPTED: "407d93bb815ee6b297b2b58d56a71724506f1304756d698bb9c6e52ca5b60ad4",
    CAL / "cme_holiday_calendar_2022_2026.json": "2698f2688cce582b08df58516fd770fa4a71a18de04870d9c14511731ea181e9",
}
GROUPS = ("equity_index", "metals", "fx")


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def early_rows():
    return [e for e in load(NEW)["entries"] if e["date"] < "2016-01-01"]


def test_pinned_calendars_are_unchanged():
    for path, sha in PINS.items():
        assert data.file_sha256(path) == sha


def test_2016_2026_date_membership_equals_the_accepted_file():
    new = {e["date"] for e in load(NEW)["entries"] if e["date"] >= "2016-01-01"}
    assert new == {e["date"] for e in load(ACCEPTED)["entries"]}


def test_2016_2026_entries_are_copied_verbatim():
    assert [e for e in load(NEW)["entries"] if e["date"] >= "2016-01-01"] == load(ACCEPTED)["entries"]


def test_builder_loader_parses_schema_and_coverage():
    cal = data.load_calendar(NEW, data.file_sha256(NEW))
    assert (cal.start, cal.end) == ("2009-01-01", "2026-12-31")
    assert cal.closed >= data.load_calendar(ACCEPTED, PINS[ACCEPTED]).closed
    assert {e["date"] for e in early_rows()} <= cal.closed
    cal.check_covers(["2009-03-02", "2010-10-01", "2015-12-31"], "M6E/MGC")


def test_strict_v1_adapter_accepts_the_file_and_its_derived_lists():
    """Exact key sets and derived-list re-derivation, so no energy column or other v1 field was added."""
    start, end, early, _ = sce._validate_source(load(NEW))  # pylint: disable=protected-access
    assert (start.isoformat(), end.isoformat()) == ("2009-01-01", "2026-12-31")
    _, _, accepted, _ = sce._validate_source(load(ACCEPTED))  # pylint: disable=protected-access
    assert {d for d in early if d.year >= 2016} == accepted


def test_every_2009_2015_row_is_a_unique_non_normal_weekday_with_a_primary_citation():
    rows = early_rows()
    dates = [e["date"] for e in rows]
    assert dates == sorted(set(dates)) and {d[:4] for d in dates} == {str(y) for y in range(2009, 2016)}
    assert all(date.fromisoformat(d).weekday() < 5 for d in dates)
    assert all(any(e[f"{g}_status"] != "NORMAL" for g in GROUPS) for e in rows)
    for e in rows:
        assert "provenance PRIMARY" in e["note"] and "Accessed 2026-11-04" in e["note"]
        assert re.search(r"https://\S+", e["note"]), e["date"]


def test_every_cited_url_has_a_recorded_hash():
    captured = {c["url"]: c["sha256"] for c in load(EVIDENCE)["captures"]}
    assert all(re.fullmatch(r"[0-9a-f]{64}", h) for h in captured.values())
    for e in early_rows():
        for url in re.findall(r"https://[^\s;,]+?(?=[\s;,]|\.\s|\.$)", e["note"]):
            assert url in captured, (e["date"], url)


def test_the_disputes_resolve_as_cme_published():
    rows = {e["date"]: e for e in early_rows()}
    # Lean's 11:30 ET equity holiday close is right until CME moved it to 13:00 ET in 2014.
    assert rows["2014-02-17"]["equity_index_close_et"] == "11:30"
    assert rows["2014-05-26"]["equity_index_close_et"] == "13:00"
    # The Friday FX early closes are real; equity trades a regular day.
    assert (rows["2013-08-30"]["fx_close_et"], rows["2013-08-30"]["equity_index_status"]) == ("16:15", "NORMAL")
    # Sandy closed equity only, shortly after the morning, and left metals and FX open.
    for day in ("2012-10-29", "2012-10-30"):
        e = rows[day]
        assert (e["equity_index_status"], e["equity_index_close_et"]) == ("EARLY_CLOSE", "09:15")
        assert (e["metals_status"], e["fx_status"]) == ("NORMAL", "NORMAL")
