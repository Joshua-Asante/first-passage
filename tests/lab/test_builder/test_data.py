"""Strict BAR EXPORT reader, book file and split: one test per invariant row (I-B*, I-S1, I-K1, I-R2)."""
from __future__ import annotations

import inspect
import json
from pathlib import Path

import pandas as pd
import pytest

from builder import data
from tests.lab.test_builder.builder_inputs import HEADER, export_lines, panel, signal, write


@pytest.fixture
def ex():
    """Three weekdays of 03:00-16:45 bars and their raw export lines (line 0 is the header)."""
    b, _ = panel(3, end="16:45")
    return b, export_lines(b)


def entry_line(lines: list[str], hhmm: str, day: int = 0) -> int:
    """Index in `lines` of the Entry row for the bar at hhmm on the day-th date."""
    b, _ = panel(3, end="16:45")
    t = [i for i, ts in enumerate(b.index) if ts.strftime("%H:%M") == hhmm][day]
    return 1 + 2 * t


def load(tmp_path, lines):
    p, _ = write(tmp_path, lines)
    return data.read_bar_export(p, "MCL")


def with_signal(line: str, sig: str) -> str:
    f = line.split(","); f[3] = sig
    return ",".join(f)


def test_clean_export_round_trips(tmp_path, ex):
    b, lines = ex
    bars, summary = load(tmp_path, lines)
    pd.testing.assert_frame_equal(bars, b.set_axis(b.index.as_unit("ns")), check_freq=False, check_names=False)
    assert summary["bars"] == len(b) and summary["early_close_sessions"] == 0


def test_reader_does_not_use_the_shared_lenient_parser():
    src = inspect.getsource(data)
    assert "import bar_export_loader" not in src and "from bar_export_loader" not in src


def test_I_B1_header_must_be_a_raw_export(tmp_path):
    p = tmp_path / "MCL_M15.csv"
    p.write_text("time,open,high,low,close,volume\n2024-01-02T14:00:00Z,70,70.1,69.9,70,1\n")
    with pytest.raises(data.DataError, match="header lacks"):
        data.read_bar_export(p, "MCL")


@pytest.mark.parametrize("bad", ["Entry", "entry long", "Comment", ""])
def test_I_B2_unknown_row_type_aborts(tmp_path, ex, bad):
    _, lines = ex
    i = entry_line(lines, "10:00")
    lines[i] = lines[i].replace("Entry long", bad).replace("Entry short", bad)
    with pytest.raises(data.DataError, match="unknown Type"):
        load(tmp_path, lines)


@pytest.mark.parametrize("mutate", [
    lambda s: "garbage",                                           # R4: undecodable Entry signal
    lambda s: "|".join(s.split("|")[:6]),                           # v0.1 six-field prefix only
    lambda s: s.replace("|5|", "|5.5|", 1),                         # non-integer volume
    lambda s: "|".join(["x" if i == 2 else f for i, f in enumerate(s.split("|"))]),  # undecodable high
    lambda s: s + "|extra",                                         # 18 fields
    lambda s: "",                                                   # empty signal
])
def test_I_B3_any_undecodable_entry_aborts_not_skipped(tmp_path, ex, mutate):
    _, lines = ex
    i = entry_line(lines, "10:30")  # inside the day session, where a hole could hide a stop touch
    lines[i] = with_signal(lines[i], mutate(lines[i].split(",")[3]))
    with pytest.raises(data.DataError, match=f":{i + 1}: Signal"):
        load(tmp_path, lines)


def test_I_B3_non_numeric_trade_number_or_price_aborts(tmp_path, ex):
    _, lines = ex
    i = entry_line(lines, "10:30")
    bad = lines.copy(); bad[i] = "x" + bad[i]
    with pytest.raises(data.DataError, match="Trade number"):
        load(tmp_path, bad)
    bad = lines.copy(); f = bad[i].split(","); f[4] = "n/a"; bad[i] = ",".join(f)
    with pytest.raises(data.DataError, match="Price USD"):
        load(tmp_path, bad)


def test_I_B4_entry_price_must_equal_encoded_close(tmp_path, ex):
    _, lines = ex
    i = entry_line(lines, "11:00")
    f = lines[i].split(","); f[4] = f"{float(f[4]) + 0.01:.2f}"; lines[i] = ",".join(f)
    with pytest.raises(data.DataError, match="encoded close"):
        load(tmp_path, lines)


@pytest.mark.parametrize("ohlc", [("70.00", "69.95", "69.90", "70.00"),   # high below close
                                  ("70.00", "70.10", "70.05", "70.00"),   # low above open
                                  ("70.00", "70.10", "69.90", "70.005")])  # off the 0.01 tick grid
def test_I_B5_ohlc_shape_and_tick_grid(tmp_path, ex, ohlc):
    _, lines = ex
    i = entry_line(lines, "11:00")
    f = lines[i].split(",")
    sig = f[3].split("|"); sig[1:5] = ohlc
    f[3], f[4] = "|".join(sig), ohlc[3]
    lines[i] = ",".join(f)
    with pytest.raises(data.DataError, match="OHLC"):
        load(tmp_path, lines)


@pytest.mark.parametrize("kw", [{"ticker": "MCL2!"}, {"tf": "5"}, {"tf": "60"}, {"mintick": "0.1"},
                                {"pv": "10"}, {"tz": "Etc/UTC"}])
def test_I_B6_instrument_constants_on_every_row(tmp_path, ex, kw):
    _, lines = ex
    i = entry_line(lines, "12:00", day=2)  # one drifted row deep in the file
    p = lines[i].split(",")[3].split("|")
    lines[i] = with_signal(lines[i], signal(int(p[0]), *map(float, p[1:5]), **kw))
    with pytest.raises(data.DataError, match="instrument constants"):
        load(tmp_path, lines)


def test_I_B7_every_bar_must_be_15_minutes_long(tmp_path, ex):
    _, lines = ex
    i = entry_line(lines, "12:00")
    p = lines[i].split(",")[3].split("|")
    lines[i] = with_signal(lines[i], signal(int(p[0]), *map(float, p[1:5]), close_ms=int(p[0]) + 300_000))
    with pytest.raises(data.DataError, match="15 minutes long"):
        load(tmp_path, lines)


def test_I_B8_bar_open_off_the_15m_grid(tmp_path, ex):
    _, lines = ex
    i = entry_line(lines, "16:45", day=2)  # last bar: moving it 5 min keeps the order intact
    p = lines[i].split(",")[3].split("|")
    lines[i] = with_signal(lines[i], signal(int(p[0]) + 300_000, *map(float, p[1:5])))
    with pytest.raises(data.DataError, match="off the 15m grid"):
        load(tmp_path, lines)


def test_I_B9_duplicate_bars_abort(tmp_path, ex):
    _, lines = ex
    i, j = entry_line(lines, "10:00"), entry_line(lines, "10:15")
    fi, fj = lines[i].split(","), lines[j].split(",")
    fj[3:5] = fi[3:5]  # same bar and price under a different trade number
    lines[j] = ",".join(fj)
    with pytest.raises(data.DataError, match="duplicate bar timestamps"):
        load(tmp_path, lines)


def test_I_B9_duplicate_trade_numbers_abort(tmp_path, ex):
    _, lines = ex
    i, j = entry_line(lines, "10:00"), entry_line(lines, "10:15")
    lines[j] = lines[i].split(",")[0] + lines[j][lines[j].index(","):]
    with pytest.raises(data.DataError, match="duplicate Entry trade numbers"):
        load(tmp_path, lines)


def test_I_B10_bar_opens_must_increase_with_trade_number(tmp_path, ex):
    _, lines = ex
    i, j = entry_line(lines, "10:00"), entry_line(lines, "10:15")
    ni, nj = lines[i].split(",")[0], lines[j].split(",")[0]
    lines[i], lines[j] = nj + lines[i][len(ni):], ni + lines[j][len(nj):]
    with pytest.raises(data.DataError, match="do not increase"):
        load(tmp_path, lines)


def test_I_B11_gap_inside_the_day_session_aborts(tmp_path, ex):
    _, lines = ex
    i = entry_line(lines, "10:30", day=1)
    del lines[i:i + 2]
    with pytest.raises(data.DataError, match="gap inside the day session"):
        load(tmp_path, lines)


def test_I_B11_early_close_and_overnight_gaps_are_allowed_and_counted(tmp_path, ex):
    b, _ = ex
    keep = ~((b.index.strftime("%Y-%m-%d") == "2023-01-03") & (b.index.strftime("%H:%M") >= "13:30"))
    keep &= ~(b.index.strftime("%H:%M") == "06:00")  # an overnight hole every day
    bars, summary = load(tmp_path, export_lines(b[keep]))
    assert summary["early_close_sessions"] == 1 and summary["gaps_between_bars"] == 5
    assert len(data.session_dates(bars, "MCL")) == 3


def test_I_B12_missing_session_open_bar_aborts(tmp_path, ex):
    _, lines = ex
    i = entry_line(lines, "09:00", day=1)
    del lines[i:i + 2]
    with pytest.raises(data.DataError, match="none at the 09:00 open"):
        load(tmp_path, lines)


def test_I_B13_no_entry_rows_aborts(tmp_path):
    with pytest.raises(data.DataError, match="no Entry rows"):
        load(tmp_path, [HEADER])


def test_I_R2_data_hash_must_match_the_pin(tmp_path, ex):
    _, lines = ex
    p, sha = write(tmp_path, lines)
    assert data.load_bars(p, "MCL", sha)[1]["sha256"] == sha
    with pytest.raises(data.DataError, match="does not match the pinned"):
        data.load_bars(p, "MCL", "0" * 64)


SESSIONS = [f"2024-01-{d:02d}" for d in range(1, 11)]


def test_I_S1_pinned_split_by_date_excludes_sessions_after_holdout_end():
    dev, hold = data.pinned_split(SESSIONS, "2024-01-05", "2024-01-08")
    assert dev == SESSIONS[:5] and hold == SESSIONS[5:8]  # 2024-01-09 and -10 are in neither


@pytest.mark.parametrize("dev_end,holdout_end,msg", [
    ("2024-01-04T", "2024-01-08", "dev_end .* not a session"),
    ("2024-01-05", "2024-01-11", "holdout_end .* not a session"),   # past the export
    ("2023-12-29", "2024-01-08", "dev_end .* not a session"),       # before the export
    ("2024-01-01", "2024-01-08", "need >= 2"),
    ("2024-01-08", "2024-01-08", "need >= 2 and >= 1"),
])
def test_I_S1_pinned_split_refuses_non_session_ends_and_empty_sides(dev_end, holdout_end, msg):
    with pytest.raises(data.DataError, match=msg):
        data.pinned_split(SESSIONS, dev_end, holdout_end)


CAL = Path(__file__).resolve().parents[3] / "ops" / "calendars" / "cme_holiday_calendar_2022_2026.json"


def test_admitted_calendar_loads_every_entry_date_whatever_its_status():
    cal = data.load_calendar(CAL, data.file_sha256(CAL))
    raw = json.loads(CAL.read_text(encoding="utf-8"))
    assert cal.closed == {e["date"] for e in raw["entries"]} and len(cal.closed) == len(raw["entries"])
    assert {"2023-01-02", "2023-01-16", "2023-11-24"} <= cal.closed  # FULL_CLOSURE and EARLY_CLOSE rows
    assert (cal.start, cal.end) == ("2022-01-01", "2026-12-31")
    cal.check_covers(["2022-01-03", "2026-12-31"], "MCL")
    with pytest.raises(data.DataError, match="outside the calendar coverage"):
        cal.check_covers(["2021-12-31"], "MCL")


@pytest.mark.parametrize("mutate,msg", [
    (lambda d: d.update(schema="other"), "schema"),
    (lambda d: d.pop("coverage_end"), "coverage"),
    (lambda d: d["entries"][0].update(date="2023-1-2"), "entries"),
    (lambda d: d["entries"][0].pop("date"), "entries"),
    (lambda d: d.update(entries=[]), "entries"),
    (lambda d: d["entries"][0].update(date="2030-01-01"), "outside the coverage"),
])
def test_calendar_is_strict(tmp_path, mutate, msg):
    d = json.loads(CAL.read_text(encoding="utf-8"))
    mutate(d)
    p = tmp_path / "cal.json"
    p.write_text(json.dumps(d), encoding="utf-8")
    with pytest.raises(data.DataError, match=msg):
        data.load_calendar(p, data.file_sha256(p))
    with pytest.raises(data.DataError, match="pinned"):
        data.load_calendar(CAL, "0" * 64)


@pytest.mark.parametrize("text,msg", [
    ('{"2024-01-02": 1, "2024-01-02": 2}', "duplicate dates"),
    ('{"2024-13-01": 1}', "bad book entry"),
    ('{"2024-1-2": 1}', "bad book entry"),
    ('{"2024-01-02": "1"}', "bad book entry"),
    ('{"2024-01-02": true}', "bad book entry"),
    ('{"2024-01-02": NaN}', "bad book entry"),
    ("{}", "non-empty object"),
    ("[1, 2]", "non-empty object"),
    ("{not json", "not JSON"),
])
def test_I_K1_book_file_is_strict(tmp_path, text, msg):
    p = tmp_path / "book.json"
    p.write_text(text, encoding="utf-8")
    with pytest.raises(data.BookError, match=msg):
        data.load_book(p, data.file_sha256(p))


def test_I_K1_book_hash_must_match_the_pin(tmp_path):
    p = tmp_path / "book.json"
    p.write_text(json.dumps({"2024-01-02": -5.0}), encoding="utf-8")
    assert data.load_book(p, data.file_sha256(p)) == {"2024-01-02": -5.0}
    with pytest.raises(data.DataError, match="pinned"):
        data.load_book(p, "0" * 64)
