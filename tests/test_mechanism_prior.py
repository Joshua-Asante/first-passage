import json
from datetime import datetime, timezone
from pathlib import Path

from lab.research_utils.mechanism_prior import aggregate_by_field, main, render_report


def test_aggregate_counts_survivors_and_n(valid_tag_record):
    records = [
        valid_tag_record(mechanism_tier="A", outcome="SURVIVED"),
        valid_tag_record(mechanism_tier="A", outcome="KILLED_AT_TEST"),
        valid_tag_record(mechanism_tier="B", outcome="SURVIVED"),
    ]
    table = aggregate_by_field(records, "mechanism_tier")
    assert table["A"][0] == 1  # successes
    assert table["A"][1] == 2  # n
    assert table["B"][0] == 1
    assert table["B"][1] == 1


def test_aggregate_returns_wilson_bounds_within_unit_interval(valid_tag_record):
    records = [valid_tag_record(outcome="SURVIVED"), valid_tag_record(outcome="KILLED_AT_TEST")]
    table = aggregate_by_field(records, "mechanism_tier")
    successes, n, lo, hi = table["A"]
    assert 0.0 <= lo <= hi <= 1.0


def test_aggregate_of_empty_records_is_empty():
    assert aggregate_by_field([], "mechanism_tier") == {}


def test_render_report_contains_all_three_field_sections(valid_tag_record):
    report = render_report([valid_tag_record()], Path("fake/path.json"), datetime(2026, 8, 20, tzinfo=timezone.utc))
    assert "By mechanism tier" in report
    assert "By sourcing channel rank" in report
    assert "By target instrument family" in report


def test_render_report_every_data_row_has_bracketed_interval(valid_tag_record):
    records = [valid_tag_record(), valid_tag_record(outcome="KILLED_AT_TEST")]
    report = render_report(records, Path("fake/path.json"), datetime(2026, 8, 20, tzinfo=timezone.utc))
    data_rows = [line for line in report.splitlines() if line.startswith("| A |")]
    assert data_rows
    for line in data_rows:
        assert "[" in line and "]" in line


def test_render_report_shows_entry_count_and_timestamp(valid_tag_record):
    now = datetime(2026, 8, 20, 12, 0, 0, tzinfo=timezone.utc)
    report = render_report(
        [valid_tag_record(), valid_tag_record()], Path("lab/research_utils/mechanism_prior_tags.json"), now
    )
    assert "2 current records" in report
    assert "2026-08-20T12:00:00" in report


def test_cli_writes_report_to_out_file(tmp_path, valid_tag_record):
    store = tmp_path / "tags.json"
    store.write_text(json.dumps(valid_tag_record()) + "\n", encoding="utf-8")
    out = tmp_path / "report.md"

    exit_code = main(["--store", str(store), "--out", str(out)])

    assert exit_code == 0
    assert out.exists()
    assert "By mechanism tier" in out.read_text(encoding="utf-8")


def test_cli_prints_to_stdout_when_no_out_given(tmp_path, capsys, valid_tag_record):
    store = tmp_path / "tags.json"
    store.write_text(json.dumps(valid_tag_record()) + "\n", encoding="utf-8")

    exit_code = main(["--store", str(store)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "By mechanism tier" in captured.out
