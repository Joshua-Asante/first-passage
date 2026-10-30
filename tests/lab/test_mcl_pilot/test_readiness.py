"""MCL-1 readiness adapter: synthetic acceptance cases (spec rev 2 sections 3 and 8)."""
from __future__ import annotations

import csv
from datetime import date, datetime, timedelta, timezone

import pytest

from discovery.mcl_pilot import readiness as R

HDR = ["Trade number", "Type", "Date and time", "Signal", "Price USD"]


def _bar(epoch: int, k: int, flat: bool = False) -> R.Bar:
    o = round(70 + 0.01 * (k % 97), 2)
    return R.Bar(o, o if flat else round(o + 0.2, 2), o if flat else round(o - 0.1, 2),
                 o if flat else round(o + 0.05, 2), 100 + k, epoch + R.BAR_MS)


def day_bars(d: date, start="08:00", end="15:30") -> dict[int, R.Bar]:
    t, stop = R.local_epoch_ms(d, start), R.local_epoch_ms(d, end)
    return {e: _bar(e, i) for i, e in enumerate(range(t, stop + 1, R.BAR_MS))}


def weekdays(lo: date, n: int) -> list[date]:
    out, d = [], lo
    while len(out) < n:
        if d.weekday() < 5 and d not in R.calendar_excluded(d.year):
            out.append(d)
        d += timedelta(days=1)
    return out


def signal(epoch: int, b: R.Bar) -> str:
    return (f"{epoch}|{b.o}|{b.h}|{b.l}|{b.c}|{b.v}|{b.close_ms}|2|M|MCL1!|futures|USD||0.01|100|"
            "America/New_York|15")


def write_inputs(root, bars: dict[int, R.Bar], extra_raw=(), extra_panel=()):
    raw, panel = root / R.RAW, root / R.PANEL
    raw.parent.mkdir(parents=True, exist_ok=True)
    panel.parent.mkdir(parents=True, exist_ok=True)
    with open(raw, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(HDR)
        for i, (e, b) in enumerate(sorted(bars.items())):
            w.writerow([i + 1, "Exit long", "", signal(e, b), b.c])
            w.writerow([i + 1, "Entry long", "", signal(e, b), b.c])
        w.writerows(extra_raw)
    with open(panel, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["time", "open", "high", "low", "close", "volume"])
        for e, b in sorted(bars.items()):
            ts = datetime.fromtimestamp(e / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            w.writerow([ts, b.o, b.h, b.l, b.c, b.v])
        w.writerows(extra_panel)
    return raw, panel


def test_new_york_clock_survives_dst():
    utc = lambda d: datetime.fromtimestamp(R.local_epoch_ms(d, "09:30") / 1000, timezone.utc).hour  # noqa: E731
    assert utc(date(2023, 1, 10)) == 14
    assert utc(date(2023, 3, 13)) == 13  # Monday after spring-forward
    assert utc(date(2023, 11, 6)) == 14  # Monday after fall-back


def test_decision_uses_bar_closing_at_decision_not_bar_opening_at_it():
    d = date(2023, 1, 10)
    bars = day_bars(d)
    assert R.signal_status(bars, d, "09:45") == ("eligible", [])
    del bars[R.local_epoch_ms(d, "09:45")]  # opens at the decision: unavailable, irrelevant
    assert R.signal_status(bars, d, "09:45") == ("eligible", [])
    del bars[R.local_epoch_ms(d, "09:30")]
    assert R.signal_status(bars, d, "09:45") == ("missing_feature", ["09:30"])


def test_short_duration_feature_bar_is_missing_not_forward_filled():
    d = date(2023, 1, 10)
    bars = day_bars(d)
    t = R.local_epoch_ms(d, "08:30")
    b = bars[t]
    bars[t] = R.Bar(b.o, b.h, b.l, b.c, b.v, t + R.BAR_MS - 60_000)
    assert R.signal_status(bars, d, "09:45") == ("missing_feature", ["08:30"])


def test_zero_denominators_exclude_opportunity():
    d = date(2023, 1, 10)
    bars = day_bars(d)
    for hhmm in ("08:30", "08:45", "09:00", "09:15"):  # t-4..t-1 flat: only F4's denominator is zero
        e = R.local_epoch_ms(d, hhmm)
        bars[e] = _bar(e, 0, flat=True)
    assert R.signal_status(bars, d, "09:45") == ("zero_denominator", ["F4"])
    e = R.local_epoch_ms(d, "09:30")
    bars[e] = _bar(e, 0, flat=True)
    assert R.signal_status(bars, d, "09:45") == ("zero_denominator", ["F1", "F2", "F3", "F4"])


def test_invalid_feature_ohlc_stops_phase():
    d = date(2023, 1, 10)
    bars = day_bars(d)
    e = R.local_epoch_ms(d, "09:00")
    bars[e] = R.Bar(70.0, 69.0, 69.5, 70.0, 1, e + R.BAR_MS)  # high below low
    with pytest.raises(R.InputError, match="invalid OHLC"):
        R.signal_status(bars, d, "09:45")


def test_invalid_feature_ohlc_stops_phase_even_when_window_is_missing_a_bar():
    d = date(2023, 1, 10)
    bars = day_bars(d)
    del bars[R.local_epoch_ms(d, "09:30")]
    e = R.local_epoch_ms(d, "09:00")
    bars[e] = R.Bar(70.0, 69.0, 69.5, 70.0, 1, e + R.BAR_MS)
    with pytest.raises(R.InputError, match="invalid OHLC"):
        R.signal_status(bars, d, "09:45")


def test_duplicates_abort_before_decoding(tmp_path):
    d = date(2023, 1, 10)
    e = R.local_epoch_ms(d, "09:00")
    raw, _ = write_inputs(tmp_path, day_bars(d), extra_raw=[[999, "Entry long", "", f"{e}|not|decodable", "1"]])
    with pytest.raises(R.InputError, match="duplicate raw"):
        R.load_raw_phase(raw, "development")


def test_malformed_in_phase_stops_but_replay_rows_are_never_decoded(tmp_path):
    d = date(2023, 1, 10)
    replay_e = R.local_epoch_ms(date(2025, 8, 5), "09:00")
    replay_ts = datetime.fromtimestamp(replay_e / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    raw, panel = write_inputs(tmp_path, day_bars(d),
                              extra_raw=[[998, "Entry long", "", f"{replay_e}|garbage", "garbage"],
                                         [999, "Entry long", "", f"{replay_e}|dup", "dup"]],
                              extra_panel=[[replay_ts, "garbage", "x", "x", "x", "x"]] * 2)
    bars = R.load_raw_phase(raw, "development")  # garbage and duplicated replay rows are skipped unparsed
    assert R.compare_panel(bars, R.load_panel_phase(panel, "development"))["bars"] == len(day_bars(d))
    in_e = R.local_epoch_ms(date(2023, 1, 11), "09:00")
    write_inputs(tmp_path, day_bars(d), extra_raw=[[999, "Entry long", "", f"{in_e}|1|2|3", "1"]])
    with pytest.raises(R.InputError, match="malformed"):
        R.load_raw_phase(raw, "development")
    assert "replay" not in R.PHASES


def test_panel_value_mismatch_stops(tmp_path):
    d = date(2023, 1, 10)
    raw, panel = write_inputs(tmp_path, day_bars(d))
    bars = R.load_raw_phase(raw, "development")
    pan = R.load_panel_phase(panel, "development")
    t = next(iter(pan))
    pan[t] = (pan[t][0] + 0.01, *pan[t][1:])
    with pytest.raises(R.InputError, match="differ"):
        R.compare_panel(bars, pan)


def test_missing_exit_keeps_signal_and_makes_development_inconclusive():
    days = [d for _, lo, _ in R.DEV_BLOCKS for d in weekdays(lo, 21)]
    bars = {e: b for d in days for e, b in day_bars(d).items()}
    gap_day = days[0]
    del bars[R.local_epoch_ms(gap_day, "11:00")]  # 09:45 exit and 10:45 entry
    rep = R.readiness(bars, "development")
    assert rep["status"] == "INCONCLUSIVE-DATA"
    assert rep["opportunities_by_clock"]["09:45"]["eligible"] == len(days)
    assert {(g["clock"], g["endpoint"]) for g in rep["missing_endpoints"]} == {("09:45", "exit"), ("10:45", "entry")}
    assert rep["eligible_sessions_by_block"] == {n: 21 for n, _, _ in R.DEV_BLOCKS}


def test_calibration_ignores_endpoints_and_counts_reasons():
    days = weekdays(date(2022, 3, 1), 5)
    bars = {e: b for d in days for e, b in day_bars(d, end="13:30").items()}  # every 13:45 exit absent
    del bars[R.local_epoch_ms(days[0], "12:30")]
    rep = R.readiness(bars, "calibration")
    assert rep["status"] == "READY" and "missing_endpoints" not in rep
    n_weekdays = sum(v["dates"] - v.get("calendar_excluded", 0) for k, v in rep["weekday_dates"].items()
                     if k not in ("Sat", "Sun"))
    for c, k in (("09:45", 5), ("12:45", 4), ("13:45", 4)):
        assert rep["opportunities_by_clock"][c] == {"eligible": k, "missing_feature": n_weekdays - k}
    assert rep["weekday_dates"]["Sat"] == {"dates": 51, "dates_with_eligible_signal": 0}  # window excludes Sat 1 Jan and Sat 31 Dec
    assert rep["eligible_by_quarter_and_clock"] == {"2022Q1": {c: 5 for c in ("09:45", "10:45", "11:45")}
                                                    | {"12:45": 4, "13:45": 4}}


def test_development_short_block_is_inconclusive():
    days = [d for _, lo, _ in R.DEV_BLOCKS for d in weekdays(lo, 21)][:-2]
    rep = R.readiness({e: b for d in days for e, b in day_bars(d).items()}, "development")
    assert rep["status"] == "INCONCLUSIVE-DATA" and rep["reasons"] == ["block 2025H1 has 19 < 20 eligible sessions"]


def test_run_pins_hashes_and_reports_verdict(tmp_path, monkeypatch):
    days = [d for _, lo, _ in R.DEV_BLOCKS for d in weekdays(lo, 21)] + weekdays(date(2022, 2, 1), 3)
    write_inputs(tmp_path, {e: b for d in days for e, b in day_bars(d).items()})
    (tmp_path / R.SPEC).parent.mkdir(parents=True)
    (tmp_path / R.SPEC).write_text("spec", encoding="utf-8")
    monkeypatch.setattr(R, "PINNED", {k: R.sha256(tmp_path / k) for k in R.PINNED})
    m = R.run(tmp_path, tmp_path / "out", list(R.PHASES))
    assert m["verdict"] == "READY-FOR-BUILD", m
    assert (tmp_path / "out" / "readiness.json").exists()
    (tmp_path / R.SPEC).write_text("edited", encoding="utf-8")
    with pytest.raises(R.InputError, match="hash mismatch"):
        R.run(tmp_path, tmp_path / "out", list(R.PHASES))


SPEC_TABLE = {  # spec rev 3 section 3.1, MM-DD per year
    2022: "01-17 02-21 04-15 05-30 06-20 07-04 09-05 11-24 11-25 12-26",
    2023: "01-02 01-16 02-20 04-07 05-29 06-19 07-04 09-04 11-23 11-24 12-25",
    2024: "01-01 01-15 02-19 03-29 05-27 06-19 07-04 09-02 11-28 11-29 12-24 12-25",
    2025: "01-01 01-20 02-17 04-18 05-26 06-19 07-04 09-01 11-27 11-28 12-24 12-25",
    2026: "01-01 01-19 02-16 04-03 05-25 06-19 07-03 09-07 11-26 11-27 12-24 12-25",
}


def test_calendar_recomputes_spec_table():
    for y, mmdd in SPEC_TABLE.items():
        assert sorted(R.calendar_excluded(y)) == [date.fromisoformat(f"{y}-{x}") for x in mmdd.split()]
    in_window = [d for y in SPEC_TABLE for d in R.calendar_excluded(y) if date(2022, 1, 3) <= d <= date(2026, 6, 30)]
    assert len(in_window) == 51


def test_calendar_date_has_no_opportunity_whatever_bars_exist():
    d = date(2024, 11, 29)  # Friday after Thanksgiving; full synthetic bars present, exit endpoints too
    rep = R.readiness(day_bars(d), "development")
    assert rep["calendar_excluded"].count("2024-11-29") == 1
    assert rep["eligible_sessions"] == 0 and rep["missing_endpoints"] == []
    assert "2024-11-29" not in rep["weekdays_without_eligible_signal"]
