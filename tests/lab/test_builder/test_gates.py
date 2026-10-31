"""Strategy builder v1, build step 3: gate engine 5a-5g, report and holdout look on synthetic bars."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

from builder import cards, gates, ledger

CARD = """
id: g-001
family: orb
instrument: MCL
entry: {type: breakout, range: first_n_bars, side: both, order: stop}
exit: {stop: range_opposite, target: none, flat_at: "12:30"}
params: {n_bars: {value: 2, step: 1}}
"""
COSTS = gates.Costs(commission_per_side=1.06)


def panel(n_days: int, trend: float = 0.08, seed: int | None = None) -> tuple[pd.DataFrame, list[str]]:
    """Weekday 15m bars 03:00-13:00 ET. Before 10:15 the price sits in a 69.90-70.20 box; from
    10:15 it moves `trend` per bar (up), so the breakout times the move; with `seed` it follows a
    seeded random walk from 09:30 instead."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2023-01-02", periods=n_days)
    rows, idx = [], []
    for d in dates:
        px = 70.05
        for t in pd.date_range(f"{d.date()} 03:00", f"{d.date()} 13:00", freq="15min", tz="America/New_York"):
            hm = t.strftime("%H:%M")
            if hm < ("09:30" if seed is not None else "10:15"):
                o, h, l, c = (70.0, 70.2, 69.9, 70.05) if hm in ("09:00", "09:15") else (70.05, 70.1, 70.0, 70.05)
            else:
                step = trend if seed is None else float(rng.normal(0, 0.08))
                o, c = px, round(px + step, 2)
                h, l = max(o, c) + 0.02, min(o, c) - 0.02
                px = c
            rows.append((o, h, l, c)); idx.append(t)
    b = pd.DataFrame(rows, columns=["open", "high", "low", "close"], index=pd.DatetimeIndex(idx))
    return b, [str(d.date()) for d in dates]


def run(tmp_path, text=CARD, n_days=260, book=None, ledgered=True, **kw):
    c = cards.parse(text)
    p = tmp_path / "ledger.jsonl"
    if ledgered:
        ledger.append_cards(p, "run-1", [c])
    b, dates = panel(n_days, **kw)
    return gates.evaluate(c, b, dates, p, COSTS, "sha-test", book), c, b, dates, p


def test_engine_refuses_an_unledgered_card(tmp_path):
    with pytest.raises(gates.GateError, match="not in the ledger"):
        run(tmp_path, ledgered=False)


def test_cost_per_trade_is_commission_plus_one_tick_each_side():
    assert COSTS.per_trade("MCL") == pytest.approx(2 * (1.06 + 0.01 * 100))


def test_firm_costs_come_from_firm_rules_and_refuse_missing_rows():
    assert gates.Costs.for_firm("Tradeify_Select_100K", "M2K").commission_per_side == 0.91
    assert gates.Costs.for_firm("Tradeify_Select_100K", "MCL").commission_per_side == 1.06
    assert gates.Costs.for_firm("MFFU_Rapid_100K", "MCL").commission_per_side == 0.58
    with pytest.raises(ValueError, match="no commission row for MCL"):
        gates.Costs.for_firm("Bulenox_100K", "MCL")


def test_clean_edge_survives_every_gate_and_report_is_traceable(tmp_path):
    rep, *_ = run(tmp_path)
    assert rep["verdict"] == "survivor" and rep["stopped_at"] is None
    assert [g["gate"][:2] for g in rep["gates"]] == ["5a", "5b", "5c", "5d", "5e", "5f", "5g"]
    assert all({"value", "threshold", "pass"} <= set(g) for g in rep["gates"])
    assert rep["k"] == 1 and len(rep["engine_sha256"]) == 64 and rep["data_sha256"] == "sha-test"
    json.dumps(rep)  # report.json must serialise


def test_small_sample_stops_at_5a(tmp_path):
    rep, *_ = run(tmp_path, n_days=50)
    assert rep["stopped_at"] == "5a sample" and len(rep["gates"]) == 1


def test_random_walk_is_killed(tmp_path):
    rep, *_ = run(tmp_path, seed=7)
    assert rep["verdict"] == "killed" and rep["stopped_at"] in {"5c halves", "5d plateau", "5e placebo", "5f deflated Sharpe"}


def test_placebo_is_reproducible_and_seeded(tmp_path):
    rep1, *_ = run(tmp_path)
    rep2, *_ = run(tmp_path / "b")
    assert rep1["gates"][4]["value"] == rep2["gates"][4]["value"] > 0.95


def test_dsr_falls_as_k_rises():
    x = np.random.default_rng(1).normal(0.1, 1, 500)
    assert gates.dsr(x, 1)[0] > gates.dsr(x, 50)[0] and gates.dsr(x, 1)[1] == 0.0


def test_book_gate_and_descriptive_book_sharpe(tmp_path):
    _, dates = panel(260)
    rng = np.random.default_rng(3)
    book = {d: float(rng.normal(20, 200)) for d in dates}
    rep, *_ = run(tmp_path, book=book)
    b = rep["book"]
    assert b["sessions"] == 260 and b["book_s_with_card"] > b["book_s"]
    assert rep["gates"][-1]["gate"] == "5g book" and rep["gates"][-1]["pass"]


def test_book_gate_fails_when_card_loses_with_the_book(tmp_path):
    rep0, c, bars, dates, p = run(tmp_path)
    x = gates.daily(c, gates.C.simulate(c, bars, dates), dates, COSTS)
    book = {d: (-500.0 if i % 2 else 100.0) for i, d in enumerate(dates)}
    shadow = gates._book(dates, -np.abs(x), book)  # a card that loses every day it trades
    assert shadow["shared_loss_share"] == pytest.approx(0.5, abs=0.05) and shadow["mean_on_book_losing_days"] < 0
    assert shadow["book_losing_share_on_active_days"] == pytest.approx(0.5, abs=0.05)


def test_empty_book_passes_5g(tmp_path):
    rep, *_ = run(tmp_path)
    assert rep["gates"][-1]["value"] == "book empty" and rep["gates"][-1]["pass"]


def test_holdout_look_is_logged_once(tmp_path):
    rep, c, b, dates, p = run(tmp_path)
    look = gates.holdout_look(c, b, dates[-50:], p, "run-1", COSTS)
    assert look["pass"] and look["trades"] == 50
    with pytest.raises(ledger.LedgerError, match="already"):
        gates.holdout_look(c, b, dates[-50:], p, "run-1", COSTS)


def test_run_ledgers_cards_before_reading_data_and_writes_reports(tmp_path):
    from builder import run
    b, _ = panel(260)
    panel_csv = tmp_path / "MCL_M15.csv"
    b.assign(time=b.index.tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%SZ"))[
        ["time", "open", "high", "low", "close"]].to_csv(panel_csv, index=False)
    (tmp_path / "c.yaml").write_text(CARD)
    spec = {"run_id": "r1", "ledger": str(tmp_path / "l.jsonl"), "firm": "Tradeify_Select_100K",
            "data": {"MCL": str(tmp_path / "missing.csv")}, "roll": "as exported", "cards": [str(tmp_path / "c.yaml")],
            "out": str(tmp_path / "out"), "book": None}
    (tmp_path / "run.yaml").write_text(json.dumps(spec))
    with pytest.raises(FileNotFoundError):
        run.main([str(tmp_path / "run.yaml")])
    assert ledger.k(tmp_path / "l.jsonl", "MCL") == 1  # ledgered even though the data read failed
    spec["data"]["MCL"] = str(panel_csv)
    (tmp_path / "run.yaml").write_text(json.dumps(spec))
    assert run.main([str(tmp_path / "run.yaml")]) == 0
    [v] = json.loads((tmp_path / "out" / "verdict.json").read_text())
    assert v["card"] == "g-001" and (tmp_path / "out" / "g-001.report.json").exists()


def test_time_window_range_and_atr_stop_compile():
    from builder import compile as C
    tw = CARD.replace("range: first_n_bars", "range: time_window").replace("stop: range_opposite", "stop: atr_multiple").replace(
        "{n_bars: {value: 2, step: 1}}", "{n_bars: {value: 1, step: 1}, offset_bars: {value: 1, step: 1}, stop_atr: {value: 2, step: 0.5}}")
    c = cards.parse(tw)
    b, dates = panel(5)
    ds = C.days(c, b, dates)
    assert ds and ds[0].first == 2 and (ds[0].hi, ds[0].lo) == (70.2, 69.9)
    assert all(t.side == 1 for t in C.simulate(c, b, dates))


# --- review fixes (Codex, PR #1003 round 1) -------------------------------------------------

def test_book_without_overlap_fails_5g_closed(tmp_path):
    rep, *_ = run(tmp_path, book={"2019-01-02": -100.0})
    assert rep["stopped_at"] == "5g book" and not rep["gates"][-1]["pass"]


def test_halves_gate_fails_when_one_half_has_no_trades():
    c = cards.parse(CARD)
    b, dates = panel(260)
    trades = [t for t in gates.C.simulate(c, b, dates) if t.date < dates[130]]
    g = []
    assert not gates._halves(g, c, trades, COSTS, set(dates[:130]), set(dates[130:]))
    assert g[0]["value"]["trades"][1] == 0


def test_range_reaching_past_flat_is_skipped_not_crashed():
    from builder import compile as C
    late = CARD.replace('flat_at: "12:30"', 'flat_at: "10:30"').replace("value: 2, step: 1", "value: 8, step: 1")
    b, dates = panel(30)
    assert C.simulate(cards.parse(late), b, dates) == []


def _spec(tmp_path, **kw):
    from builder import run
    b, _ = panel(260)
    panel_csv = tmp_path / "MCL_M15.csv"
    b.assign(time=b.index.tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%SZ"))[
        ["time", "open", "high", "low", "close"]].to_csv(panel_csv, index=False)
    (tmp_path / "c.yaml").write_text(CARD)
    spec = {"run_id": "r1", "ledger": str(tmp_path / "l.jsonl"), "firm": "Tradeify_Select_100K",
            "data": {"MCL": str(panel_csv)}, "roll": "as exported", "cards": [str(tmp_path / "c.yaml")],
            "out": str(tmp_path / "out"), "book": None, **kw}
    (tmp_path / "run.yaml").write_text(json.dumps(spec))
    return run, tmp_path / "run.yaml"


def test_override_refused_where_the_firm_has_a_row(tmp_path):
    run, p = _spec(tmp_path, commission_per_side={"MCL": 0.0})
    with pytest.raises(SystemExit, match="has a commission row"):
        run.main([str(p)])
    assert not (tmp_path / "l.jsonl").exists()


def test_override_must_be_positive_where_no_row(tmp_path):
    run, p = _spec(tmp_path, firm="Bulenox_100K", commission_per_side={"MCL": -1})
    with pytest.raises(SystemExit, match="positive commission_per_side"):
        run.main([str(p)])


def test_duplicate_card_ids_rejected_before_ledgering(tmp_path):
    run, p = _spec(tmp_path)
    spec = json.loads(p.read_text())
    (tmp_path / "c2.yaml").write_text(CARD.replace("value: 2, step: 1", "value: 3, step: 1"))
    spec["cards"].append(str(tmp_path / "c2.yaml"))
    p.write_text(json.dumps(spec))
    with pytest.raises(SystemExit, match="duplicate card ids"):
        run.main([str(p)])
    assert not (tmp_path / "l.jsonl").exists()


def test_session_opens_sit_on_the_bar_grid():
    from builder.instruments import INSTRUMENTS
    assert INSTRUMENTS["MGC"].session_open == "08:30"
    assert all(int(i.session_open[3:]) % 15 == 0 for i in INSTRUMENTS.values())


# --- review fixes (Codex, PR #1003 round 3) -------------------------------------------------

def _export(tmp_path, rows, tf="15"):
    hdr = "Trade number,Type,Date and time,Signal,Price USD\n"
    body = "".join(f"{i},Entry long,x,{e}|70|70.1|69.9|70|5|{e + 900000}|2|M|MCL1!|futures|USD||0.01|100|America/New_York|{tf},70\n"
                   for i, e in enumerate(rows, 1))
    p = tmp_path / "BAR_EXPORT.csv"
    p.write_text(hdr + body, encoding="utf-8")
    return p


def test_raw_export_with_duplicate_bars_is_refused(tmp_path):
    from builder import data
    e = 1704204000000  # 2024-01-02 14:00Z
    with pytest.raises(ValueError, match="duplicate"):
        data.load_bars(_export(tmp_path, [e, e + 900000, e + 900000]), "MCL")


def test_raw_export_must_be_15_minute(tmp_path):
    from builder import data
    e = 1704204000000
    with pytest.raises(ValueError, match="15m"):
        data.load_bars(_export(tmp_path, [e, e + 300000], tf="5"), "MCL")


def test_panel_off_the_15m_grid_is_refused(tmp_path):
    from builder import data
    p = tmp_path / "MCL_M15.csv"
    p.write_text("time,open,high,low,close,volume\n2024-01-02T14:00:00Z,70,70.1,69.9,70,1\n"
                 "2024-01-02T14:05:00Z,70,70.1,69.9,70,1\n")
    with pytest.raises(ValueError, match="15m grid"):
        data.load_bars(p, "MCL")


def test_zero_variance_fails_5f_instead_of_crashing():
    g = []
    assert not gates._dsr_gate(g, np.full(300, 5.0), 1)
    assert g[0]["value"].startswith("undefined")


def test_run_requires_a_declared_book(tmp_path):
    run, p = _spec(tmp_path)
    spec = json.loads(p.read_text()); del spec["book"]; p.write_text(json.dumps(spec))
    with pytest.raises(SystemExit, match="missing book"):
        run.main([str(p)])
    (tmp_path / "book.json").write_text("{}")
    spec["book"] = str(tmp_path / "book.json"); p.write_text(json.dumps(spec))
    with pytest.raises(SystemExit, match="empty"):
        run.main([str(p)])
