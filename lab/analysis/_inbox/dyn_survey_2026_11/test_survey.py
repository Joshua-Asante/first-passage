"""DYN-SURVEY-1 rules on synthetic bars; no export is read."""
from __future__ import annotations

import json
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT / "lab"), str(ROOT / "core")]

import pandas as pd  # noqa: E402
import pytest  # noqa: E402

from builder.instruments import minutes as m  # noqa: E402
from research_utils.camp_import import load_camp_sibling  # noqa: E402

S = load_camp_sibling("survey", __file__)
R = load_camp_sibling("run", __file__)


def bar(o, c=None, h=None, l=None):  # noqa: E741
    c = o if c is None else c
    return (o, max(o, c) if h is None else h, min(o, c) if l is None else l, c)


def flat(lo="08:00", hi="16:45", px=100.0):
    return {t: bar(px) for t in range(m(lo), m(hi) + 15, 15)}


def test_ref_uses_only_closed_bars_within_the_hour():
    day = {m("09:15"): bar(1, 2), m("09:30"): bar(3, 4)}
    assert S.ref(day, m("09:30")) == 2                         # the 09:30 bar has not closed
    assert S.ref(day, m("10:15")) == 4                         # 09:30 is inside [09:15, 10:00]
    assert S.ref({m("08:15"): bar(1, 2)}, m("09:30")) is None  # older than T - 60m


def test_fill_window_and_limit():
    day = {m("10:45"): bar(7)}
    assert S.fill(day, m("10:30"), m("15:45")) == 7     # next bar after a missing one
    assert S.fill(day, m("10:15"), m("15:45")) is None  # T + 30m excludes 10:45
    assert S.fill(day, m("10:30"), m("10:45")) is None  # the limit excludes it


def test_c3_worked_example():
    day = flat()
    day[m("09:15")] = bar(100, 100)
    day[m("10:15")] = bar(100, 105)
    day[m("10:30")] = bar(106)
    day[m("15:45")] = bar(110)
    todo = S.plans("C3", "MNQ", day, None, None, None)
    assert todo == [(5, m("10:30"), m("15:45"))]
    [t] = S.session_trades("d", day, todo, 1)
    assert (t.side, t.entry_px, t.exit_px) == (1, 106, 110)
    assert S.session_trades("d", day, todo, -1)[0].side == -1


def test_entry_expires_and_exit_is_unresolved_never_zero():
    day = flat()
    for b in ("10:30", "10:45"):
        del day[m(b)]
    assert S.session_trades("d", day, [(1.0, m("10:30"), m("15:45"))], 1) == []
    [t] = S.session_trades("d", {m("10:30"): bar(100)}, [(1.0, m("10:30"), m("15:45"))], 1)
    assert t.unresolved and t.exit_px is None


def test_exit_cap_is_h_plus_15():
    day = {m("16:30"): bar(100), m("16:45"): bar(101)}
    assert S.fill(day, m("16:30"), S.H + 15) == 100
    del day[m("16:30")]
    assert S.fill(day, m("16:30"), S.H + 15) is None    # 16:45 is past the cap


@pytest.mark.parametrize("symbol,n,first,last", [("MNQ", 5, "10:30", "15:30"), ("MGC", 4, "09:30", "13:30"),
                                                 ("MCL", 4, "10:00", "14:00")])
def test_c5_blocks(symbol, n, first, last):
    got = S.plans("C5", symbol, flat("07:30"), None, None, None)
    assert len(got) == n and got[0][1] == m(first) and got[-1][2] == m(last)
    assert all(a[2] == b[1] for a, b in zip(got, got[1:]))


def test_c5_x_and_same_bar_exit_then_entry():
    day = flat()
    day[m("10:15")] = bar(100, 101)
    day[m("11:15")] = bar(100, 104)
    assert S.plans("C5", "MNQ", day, None, None, None)[1] == (3, m("11:30"), m("12:30"))
    day[m("11:30")] = bar(150)
    a, b = S.session_trades("d", day, [(1.0, m("10:30"), m("11:30")), (1.0, m("11:30"), m("12:30"))], 1)
    assert a.exit_px == b.entry_px == 150


def test_unresolved_exit_skips_later_entries():
    day = {m("10:30"): bar(100), m("12:30"): bar(100), m("13:30"): bar(100)}
    got = S.session_trades("d", day, [(1.0, m("10:30"), m("11:30")), (1.0, m("12:30"), m("13:30"))], 1)
    assert len(got) == 1 and got[0].unresolved


def test_zero_or_undefined_signal_is_no_trade():
    assert S.session_trades("d", flat(), [(0.0, m("10:30"), m("11:30")), (None, m("10:30"), m("11:30"))], 1) == []


def test_c1_c2_use_prev_close_window():
    prev = {m("15:45"): bar(1, 90), m("16:30"): bar(1, 95), m("17:00"): bar(1, 80)}
    day = flat()
    assert S.c_prev(prev) == 95 and S.c_prev({m("15:45"): bar(1)}) is None
    assert S.plans("C1", "MNQ", day, prev, None, None) == [(5, m("09:30"), m("10:30"))]
    assert S.plans("C2", "MNQ", day, prev, None, None) == [(5, m("10:30"), m("15:45"))]
    assert S.plans("C1", "MNQ", day, None, None, None)[0][0] is None


def test_c4_c6_c7():
    day = flat("07:30")
    day[m("14:30")] = bar(100, 110)
    assert S.plans("C4", "MNQ", day, None, None, None) == [(10, m("14:45"), m("15:45"))]
    day = flat("07:30")
    day[m("15:15")] = bar(100, 106)
    assert S.plans("C6", "MNQ", day, None, None, m("16:00")) == [(6, m("15:30"), m("16:00"))]
    assert S.plans("C7", "MNQ", day, None, None, m("16:00")) == [(-6, m("16:00"), m("16:30"))]


def test_settlement_validity():
    assert S.window_valid("C1", "MNQ", None)
    assert not S.window_valid("C6", "MNQ", None) and not S.window_valid("C7", "MNQ", m("14:40"))
    assert S.window_valid("C6", "MNQ", m("16:00")) and S.window_valid("C7", "MNQ", m("16:00"))
    assert not S.window_valid("C6", "MNQ", m("16:30")) and not S.window_valid("C7", "MNQ", m("16:30"))
    assert not S.window_valid("C6", "MNQ", m("10:45"))  # S - 30 is before O + 60


def hour(w):
    """A complete MNQ first hour of width w points from 100."""
    return {m("09:30") + 15 * i: bar(100, 100, 100 + w, 100) for i in range(4)}


def test_c8_rank_warmup_tie_and_incomplete_hour():
    days = {f"d{w:02d}": hour(w) for w in range(1, 21)}  # the 7th smallest of 1..20 is 7
    names = list(days)
    fh = S.first_hours(names + ["tie", "wide", "gap"],
                       {**days, "tie": hour(7), "wide": hour(8), "gap": {m("09:30"): bar(1)}}, "MNQ")
    assert not fh["d20"][2]                             # 19 earlier sessions: warm-up
    assert fh["tie"][2]                                 # ties count as narrow
    assert not fh["wide"][2]                            # the last 20 are now 2..20 and 7: 7th is 7
    assert fh["gap"] is None


def test_c8_signal_bars_and_entry():
    day = flat()
    fh = (102.0, 98.0, True)
    assert S.plans("C8", "MNQ", day, None, fh, None) == []
    day[m("14:45")] = bar(100, 110)                     # after E - 75m: not a signal bar
    assert S.plans("C8", "MNQ", day, None, fh, None) == []
    day[m("14:30")] = bar(100, 97)
    assert S.plans("C8", "MNQ", day, None, fh, None) == [(-1.0, m("14:45"), m("15:45"))]
    assert S.plans("C8", "MNQ", day, None, (102.0, 98.0, False), None) == []
    assert S.plans("C8", "MNQ", day, None, None, None) == []


def test_session_days_is_local_time_and_drops_evening():
    idx = pd.DatetimeIndex(["2026-03-06 09:30", "2026-03-09 09:30", "2026-03-09 18:00"], tz="America/New_York")
    b = pd.DataFrame({"open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0}, index=idx)
    d = S.session_days(b)                               # either side of the March DST change
    assert set(d["2026-03-06"]) == set(d["2026-03-09"]) == {m("09:30")}


def trending(n):
    """n MNQ sessions on which C3 goes long and earns 10 or 11 points."""
    dates = [str(x.date()) for x in pd.bdate_range("2023-01-02", periods=n)]
    days = {}
    for i, d in enumerate(dates):
        day = flat()
        day[m("10:15")] = bar(100, 101)
        day[m("10:30")] = bar(101)
        day[m("15:45")] = bar(111 + i % 2)
        days[d] = day
    return dates, days


def test_series_costs_closed_dates_and_eligibility():
    dates, days = trending(600)
    book = {d: float(i % 3 - 1) for i, d in enumerate(dates)}
    closed = frozenset({dates[5]})
    row = S.evaluate_cell("C3", "cont", "MNQ", dates, dates, days, closed, None, 0.91, book)
    assert row["status"] == "ELIGIBLE" and row["trades"] == 599 and row["sessions"] == 600
    x = S.series(S.cell_trades("C3", "MNQ", 1, dates, dates, days, closed, None), dates, "MNQ", 0.91, 1.0)
    assert x[5] == 0 and x[0] == pytest.approx(10 * 2 - 2 * (0.91 + 0.5))
    rev = S.evaluate_cell("C3", "rev", "MNQ", dates, dates, days, frozenset(), None, 0.91, book)
    assert rev["status"] == "INELIGIBLE" and "base Sharpe below 0.12" in rev["failed"]


def test_unresolved_cell_gets_no_statistics():
    dates, days = trending(5)
    for b in ("15:45", "16:00"):
        del days[dates[2]][m(b)]
    row = S.evaluate_cell("C3", "cont", "MNQ", dates, dates, days, frozenset(), None, 0.91, {})
    assert row["status"] == "UNRESOLVED" and row["unresolved_dates"] == [dates[2]] and "sharpe_base" not in row
    assert row["sessions_traded"] == 5


def test_pre_development_session_gives_no_c_prev():
    dates, days = trending(3)
    for d in dates:
        days[d][m("09:15")] = bar(100, 101)
        days[d][m("16:30")] = bar(100, 100)
    got = S.cell_trades("C1", "MNQ", 1, dates, dates[1:], days, frozenset(), None)
    assert [t.date for t in got] == [dates[2]]


def test_undefined_dsr_and_zero_variance_are_ineligible():
    dates, days = trending(5)
    row = S.evaluate_cell("C8", "cont", "MNQ", dates, dates, days, frozenset(), None, 0.91, {})
    assert row["status"] == "INELIGIBLE"
    assert {"fewer than 200 trades", "zero series variance", "undefined DSR"} <= set(row["failed"])


def rows(*spec):
    return [{"id": i, "status": "ELIGIBLE", "rise": r, "dsr": d} for i, r, d in spec]


def test_selection_ties_and_threshold():
    assert S.select(rows(("B", 0.05, 0.96), ("A", 0.04, 0.99)))["id"] == "B"
    assert S.select(rows(("B", 0.05, 0.96), ("C", 0.05, 0.99)))["id"] == "C"
    assert S.select(rows(("B", 0.05, 0.96), ("A", 0.05, 0.96)))["id"] == "A"
    assert S.select(rows(("A", 0.029, 0.99))) is None   # no card below +0.03
    assert S.select([{"id": "A", "status": "INELIGIBLE"}]) is None


def test_outcomes():
    ne = [{"status": "NOT EVALUATED"}]
    assert S.outcome(ne, None) == "PARTIAL NULL"
    assert S.outcome([{"status": "INELIGIBLE"}], None) == "NULL"
    assert S.outcome(ne, {"id": "A"}) == "ADVANCED"


def test_quality_table():
    idx = pd.DatetimeIndex(["2026-03-06 09:30", "2026-03-09 09:30", "2026-03-09 09:45"], tz="America/New_York")
    b = pd.DataFrame({"open": 1.0, "high": 3.0, "low": 1.0, "close": 1.0}, index=idx)
    t = S.quality(b, pd.Series([5, 7, 9], index=idx), ["2026-03-06", "2026-03-09"], "MNQ", 8.0)
    assert t[0] == {"slot": "09:30", "missing_share": 0, "median_range": 2.0, "median_volume": 6.0,
                    "cost_over_median_range": 2.0}
    assert t[1]["missing_share"] == 0.5 and t[2]["median_range"] is None


def test_commission_gap(monkeypatch):
    monkeypatch.setattr(R, "resolve_commission", lambda f, s: 0.91)
    assert R.commission_gap("MNQ", None).startswith("no fee quote")
    assert "does not match" in R.commission_gap("MNQ", {R.FIRMS[0]: 0.91, R.FIRMS[1]: 0.95})
    assert R.commission_gap("MNQ", {R.FIRMS[0]: 0.91, R.FIRMS[1]: 0.91}) is None


def test_run_refuses_a_second_run_and_a_wrong_head(tmp_path, monkeypatch):
    p = tmp_path / "freeze.json"
    p.write_text(json.dumps({"frozen_sha": "x", "out": str(tmp_path / "out"),
                             "exposure_log": str(tmp_path / "log.md")}))
    with pytest.raises(R.Refused, match="not the frozen SHA"):
        R.main(p)
    monkeypatch.setattr(R, "check_head", lambda sha: None)
    (tmp_path / "out").mkdir()
    (tmp_path / "out" / "report.json").write_text("{}")
    with pytest.raises(R.Refused, match="one run"):
        R.main(p)


def test_export_reaching_the_holdout_refuses_the_run(tmp_path, monkeypatch):
    dates, _ = trending(3)
    idx = pd.DatetimeIndex([f"{d} 09:30" for d in dates], tz="America/New_York")
    bars = pd.DataFrame({"open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0}, index=idx)
    monkeypatch.setattr(R, "commission_gap", lambda *a: None)
    monkeypatch.setattr(R.data, "load_bars", lambda *a: (bars, {}))
    cal = type("Cal", (), {"check_covers": lambda *a: None, "closed": frozenset()})()
    log = tmp_path / "log.md"
    log.write_text("")
    with pytest.raises(R.Refused, match="holdout"):
        R.survey_instrument("MNQ", {"path": "p", "sha256": "abcdefgh", "h_start": dates[-1]}, cal, {}, log)
    assert "MNQ" in log.read_text()                     # logged before the read


def test_dropped_instrument_keeps_its_16_cells_in_k(tmp_path):
    log = tmp_path / "log.md"
    log.write_text("")
    got, detail = R.survey_instrument("MNQ", {"sha256": "abcdefgh", "path": "p"}, None, {}, log)
    assert len({r["id"] for r in got}) == 16 and {r["status"] for r in got} == {"NOT EVALUATED"}
    assert detail == {} and log.read_text() == ""       # nothing was read


def record(tmp_path, quotes=None, **over):
    """A synthetic freeze record with every instrument, seeded log and stub input paths."""
    log = tmp_path / "log.md"
    log.write_text("")
    inst = {s: {"path": f"{s}.csv", "sha256": "abcdefgh", "quoted_commission": quotes} for s in R.SYMBOLS}
    rec = {"frozen_sha": "x", "out": str(tmp_path / "out"), "exposure_log": str(log), "instruments": inst,
           "calendar": {"path": "cal", "sha256": "c"}, "book": {"path": "book", "sha256": "b"}, **over}
    p = tmp_path / "freeze.json"
    p.write_text(json.dumps(rec))
    return p


def test_missing_commission_row_drops_its_cells_and_the_report_records_it(tmp_path, monkeypatch):
    def commission(firm, symbol):
        if (firm, symbol) == (R.FIRMS[1], "MCL"):
            raise KeyError(f"{firm} {symbol}")
        return 0.5

    def no_bars(*a):
        raise R.data.DataError("synthetic")

    monkeypatch.setattr(R, "check_head", lambda sha: None)
    monkeypatch.setattr(R, "resolve_commission", commission)
    monkeypatch.setattr(R.data, "load_calendar", lambda *a: None)
    monkeypatch.setattr(R.data, "load_book", lambda *a: {})
    monkeypatch.setattr(R.data, "load_bars", no_bars)
    p = record(tmp_path, {f: 0.5 for f in R.FIRMS})
    report = R.main(p)
    assert json.loads((tmp_path / "out" / "report.json").read_text())["k"] == S.K
    mcl = [r for r in report["cells"] if r["id"].startswith("MCL")]
    assert len(mcl) == 16 and all(r["status"] == "NOT EVALUATED" for r in mcl)
    assert all(r["reason"].startswith("no commission row") for r in mcl)
    assert report["commissions"][R.FIRMS[1]]["MCL"]["commission"] is None
    assert "MCL" in report["commissions"][R.FIRMS[1]]["MCL"]["missing"]
    assert report["commissions"][R.FIRMS[0]]["MCL"] == {"commission": 0.5, "missing": None}


def test_failed_run_keeps_its_marker_and_a_second_run_is_refused(tmp_path, monkeypatch):
    def boom(*a):
        raise RuntimeError("synthetic failure after the marker")

    monkeypatch.setattr(R, "check_head", lambda sha: None)
    monkeypatch.setattr(R.data, "load_calendar", boom)
    p = record(tmp_path)
    with pytest.raises(RuntimeError, match="synthetic failure"):
        R.main(p)
    marker = tmp_path / "out" / R.MARKER
    assert json.loads(marker.read_text())["frozen_sha"] == "x"
    assert not (tmp_path / "out" / "report.json").exists()
    monkeypatch.setattr(R.data, "load_calendar", lambda *a: pytest.fail("inputs read on a second run"))
    with pytest.raises(R.Refused, match="one run"):
        R.main(p)
    assert marker.exists()


def test_concurrent_claims_admit_one_run(tmp_path):
    start, results = threading.Barrier(8), []

    def claim():
        start.wait()
        try:
            R.claim_run(tmp_path, "x")
            results.append("ran")
        except R.Refused:
            results.append("refused")

    threads = [threading.Thread(target=claim) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(results) == ["ran"] + ["refused"] * 7


@pytest.mark.parametrize("field", ["out", "exposure_log"])
def test_output_path_in_the_tracked_tree_is_refused(tmp_path, monkeypatch, field):
    monkeypatch.setattr(R, "check_head", lambda sha: None)
    monkeypatch.setattr(R.data, "load_calendar", lambda *a: pytest.fail("inputs read"))
    tracked = Path(R.__file__).resolve().parent                 # this survey's tracked source dir
    target = tracked if field == "out" else tracked / "DESIGN.md"
    p = record(tmp_path, **{field: str(target)})
    with pytest.raises(R.Refused, match="tracked by git"):
        R.main(p)
    assert not (tracked / R.MARKER).exists() and not (tmp_path / "out").exists()
