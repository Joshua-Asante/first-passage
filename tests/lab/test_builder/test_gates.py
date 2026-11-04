"""Strategy builder v1, build step 3: gates 5a-5f, report, holdout look and 5g placement (I-S2, I-S3, I-K3, I-G3..I-G6, I-L4)."""
from __future__ import annotations

import json

import numpy as np
import pytest

from builder import cards, gates, ledger
from tests.lab.test_builder.builder_inputs import CARD, panel

COSTS = gates.Costs(commission_per_side=1.06)


def run(tmp_path, text=CARD, n_days=260, book=None, ledgered=True, dates=None, closed=frozenset(),
        k_scope="instrument", **kw):
    c = cards.parse(text)
    p = tmp_path / "ledger.jsonl"
    if ledgered:
        ledger.append_cards(p, "run-1", [c])
    b, all_dates = panel(n_days, **kw)
    return gates.evaluate(c, b, all_dates if dates is None else dates, p, COSTS, "sha-test", book,
                          closed=closed, k_scope=k_scope), c, b, all_dates, p


def test_I_L4_engine_refuses_an_unledgered_card(tmp_path):
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
    assert [g["gate"][:2] for g in rep["gates"]] == ["5a", "5b", "5c", "5d", "5e", "5f"]  # 5g is placement, after holdout
    assert rep["gates"][1]["gate"] == "5b costs applied (not a gate)" and rep["gates"][1]["pass"]
    assert all({"value", "threshold", "pass"} <= set(g) for g in rep["gates"])
    assert rep["k"] == 1 and len(rep["engine_sha256"]) == 64 and rep["data_sha256"] == "sha-test"
    assert rep["skipped_days"] == {}
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


@pytest.mark.parametrize("bad,msg", [
    (lambda d: [], "non-empty"),
    (lambda d: d[::-1], "sorted"),
    (lambda d: d[:5] + d[4:], "unique"),
    (lambda d: d + ["2030-01-01"], "not sessions"),
    (lambda d: d[:1], "two development halves"),
])
def test_I_S2_evaluated_dates_must_be_sessions_sorted_and_unique(tmp_path, bad, msg):
    _, dates = panel(260)
    with pytest.raises(gates.GateError, match=msg):
        run(tmp_path, dates=bad(dates))


def test_I_S3_trades_outside_the_evaluated_dates_abort():
    c = cards.parse(CARD)
    b, dates = panel(20)
    trades = gates.C.simulate(c, b, dates)
    with pytest.raises(gates.GateError, match="outside the evaluated sessions"):
        gates.daily(c, trades, dates[:10], COSTS)


def test_I_G3_halves_gate_fails_when_one_half_has_no_trades():
    c = cards.parse(CARD)
    b, dates = panel(260)
    trades = [t for t in gates.C.simulate(c, b, dates) if t.date < dates[130]]
    g = []
    assert not gates._halves(g, c, trades, COSTS, set(dates[:130]), set(dates[130:]))
    assert g[0]["value"]["trades"][1] == 0


def test_I_G4_plateau_needs_a_positive_base_and_names_skipped_neighbours(tmp_path):
    c = cards.parse(CARD.replace("value: 2, step: 1", "value: 1, step: 1"))
    b, dates = panel(30)
    g = []
    assert not gates._plateau(g, c, b, dates, COSTS, base=-1.0) and g[0]["value"] == {"base_net": -1.0}
    g = []
    gates._plateau(g, c, b, dates, COSTS, base=100.0)
    assert g[0]["value"]["skipped_invalid"] == ["n_bars-"] and list(g[0]["value"]["kept"]) == ["n_bars+"]


def test_I_G5_placebo_with_no_trades_is_zero():
    c = cards.parse(CARD)
    assert gates.placebo_beaten_share(c, [], [], COSTS, 10, 1) == 0.0


def test_I_G6_zero_variance_fails_5f_instead_of_crashing():
    g = []
    assert not gates._dsr_gate(g, np.full(300, 5.0), 1)
    assert g[0]["value"].startswith("undefined")


BOOK_SHA = "b" * 64


def pinned(b):
    """The pinned sha256 holdout.py passes beside the report's book statistics (None for book: null)."""
    return BOOK_SHA if isinstance(b, dict) and b.get("supplied") else None


def look(tmp_path, book=None, n_hold=50, **kw):
    """Development report on all but the last ``n_hold`` sessions, then the holdout look on those
    sessions with the report's book stats; the two windows are disjoint."""
    _, all_dates = panel(260)
    rep, c, b, dates, p = run(tmp_path, book=book, dates=all_dates[:-n_hold], **kw)
    return rep, gates.holdout_look(c, b, dates[-n_hold:], p, "run-1", COSTS, closed=frozenset(),
        book=rep["book"], book_sha256=pinned(rep["book"]))


def test_book_placement_clear_and_descriptive_book_sharpe(tmp_path):
    _, dates = panel(260)
    rng = np.random.default_rng(3)
    rep, h = look(tmp_path, book={d: float(rng.normal(20, 200)) for d in dates})
    b = rep["book"]
    assert b["sessions"] == 210 and b["book_s_with_card"] > b["book_s"]
    assert rep["verdict"] == "survivor" and all(g["gate"][:2] != "5g" for g in rep["gates"])
    assert h["pass"] and h["placement"] == "clear"
    assert h["placement_gate"]["gate"] == gates.PLACEMENT_LABEL and h["placement_gate"]["pass"]
    assert h["placement_book_sha256"] == BOOK_SHA


def test_book_statistics_when_card_loses_with_the_book(tmp_path):
    rep0, c, bars, dates, p = run(tmp_path)
    x = gates.daily(c, gates.C.simulate(c, bars, dates), dates, COSTS)
    book = {d: (-500.0 if i % 2 else 100.0) for i, d in enumerate(dates)}
    shadow = gates._book(dates, -np.abs(x), book)  # a card that loses every day it trades
    assert shadow["shared_loss_share"] == pytest.approx(0.5, abs=0.05) and shadow["mean_on_book_losing_days"] < 0
    assert shadow["book_losing_share_on_active_days"] == pytest.approx(0.5, abs=0.05)
    assert gates.placement(shadow)["placement"] == "fail"


def test_I_K3_book_without_losing_days_fails_placement_closed(tmp_path):
    # also the gate-level case of a card failing fit: its look is taken, verdicts intact, placement fail
    _, dates = panel(260)
    rep, h = look(tmp_path, book={d: 100.0 for d in dates})
    assert rep["verdict"] == "survivor" and rep["book"]["mean_on_book_losing_days"] is None
    assert h["pass"] and h["placement"] == "fail" and not h["placement_gate"]["pass"]


@pytest.mark.parametrize("book", [{"2019-01-02": -100.0}, {}])
def test_I_K2_supplied_book_without_overlap_fails_placement_closed(tmp_path, book):
    rep, h = look(tmp_path, book=book)
    assert rep["verdict"] == "survivor" and rep["book"] == {"sessions": 0, "supplied": True}
    assert h["pass"] and h["placement"] == "fail"
    assert h["placement_gate"]["value"] == "book supplied, no overlapping development sessions"


def test_declared_empty_book_leaves_placement_not_evaluated_never_clear(tmp_path):
    rep, h = look(tmp_path)
    assert rep["verdict"] == "survivor" and h["pass"]  # the look and the development verdict are unaffected
    assert (h["placement"], h["placement_gate"], h["placement_book_sha256"]) == ("not_evaluated", None, None)
    assert gates.placement(rep["book"]) == {"placement": "not_evaluated", "placement_gate": None}
    with pytest.raises(gates.GateError, match="not evaluated"):
        gates._book_gate([], rep["book"])  # 5g has no rule that passes without a book


@pytest.mark.parametrize("book, sha", [(None, BOOK_SHA), ({"2019-01-02": -1.0}, None)])
def test_book_statistics_and_pinned_book_must_agree_before_the_look(tmp_path, book, sha):
    rep, c, b, dates, p = run(tmp_path, book=book)
    with pytest.raises(gates.GateError, match="do not match the pinned book"):
        gates.holdout_look(c, b, dates[-50:], p, "run-1", COSTS, closed=frozenset(), book=rep["book"], book_sha256=sha)
    assert not any(e["kind"] == "holdout_look" for e in ledger.read(p))


def test_placement_reads_only_the_development_window(tmp_path):
    _, dates = panel(260)
    dev = {d: 100.0 for d in dates[:-50]}  # no development losing day: placement fails closed
    _, h1 = look(tmp_path / "a", book=dev)
    _, h2 = look(tmp_path / "b", book={**dev, **{d: -500.0 for d in dates[-50:]}})  # holdout-window losses
    assert h1["placement"] == h2["placement"] == "fail" and h1["placement_gate"] == h2["placement_gate"]


def test_placement_runs_only_after_a_holdout_pass(tmp_path):
    _, dates = panel(260)
    rep, c, b, all_dates, p = run(tmp_path, book={d: 100.0 for d in dates})
    h = gates.holdout_look(c, _halt(b, all_dates, [all_dates[-3]]), all_dates[-50:], p, "run-1", COSTS,
                           closed=frozenset(), book=rep["book"], book_sha256=pinned(rep["book"]))
    assert h["verdict"] == "unresolved" and h["placement"] is None and h["placement_gate"] is None


@pytest.mark.parametrize("bad", [None, {}, {"sessions": 3, "supplied": True}, {"sessions": 0, "supplied": "yes"},
                                 {"sessions": 2, "supplied": True, "mean_on_book_losing_days": 1.0,
                                  "shared_loss_share": None, "book_losing_share_on_active_days": 0.5},
                                 {"sessions": 2, "supplied": True, "mean_on_book_losing_days": 1.0,
                                  "shared_loss_share": -1.0, "book_losing_share_on_active_days": 0.5},
                                 {"sessions": 2, "supplied": True, "mean_on_book_losing_days": 1.0,
                                  "shared_loss_share": 0.2, "book_losing_share_on_active_days": 1.5}])
def test_malformed_book_statistics_are_refused_before_the_look(tmp_path, bad):
    rep, c, b, dates, p = run(tmp_path)
    with pytest.raises(gates.GateError, match="malformed"):
        gates.holdout_look(c, b, dates[-50:], p, "run-1", COSTS, closed=frozenset(), book=bad, book_sha256=None)
    assert not any(e["kind"] == "holdout_look" for e in ledger.read(p))


def test_I_L5_holdout_look_is_logged_once_and_checks_dates_first(tmp_path):
    rep, c, b, dates, p = run(tmp_path)
    with pytest.raises(gates.GateError, match="not sessions"):
        gates.holdout_look(c, b, ["2030-01-01"], p, "run-1", COSTS, closed=frozenset(),
            book=rep["book"], book_sha256=pinned(rep["book"]))
    assert not any(e["kind"] == "holdout_look" for e in ledger.read(p))
    look = gates.holdout_look(c, b, dates[-50:], p, "run-1", COSTS, closed=frozenset(),
        book=rep["book"], book_sha256=pinned(rep["book"]))
    assert look["pass"] and look["verdict"] == "pass" and look["trades"] == 50
    with pytest.raises(ledger.LedgerError, match="already"):
        gates.holdout_look(c, b, dates[-50:], p, "run-1", COSTS, closed=frozenset(),
            book=rep["book"], book_sha256=pinned(rep["book"]))


def test_time_window_range_and_atr_stop_compile():
    from builder import compile as C
    tw = CARD.replace("range: first_n_bars", "range: time_window").replace("stop: range_opposite", "stop: atr_multiple").replace(
        "{n_bars: {value: 2, step: 1}}", "{n_bars: {value: 1, step: 1}, offset_bars: {value: 1, step: 1}, stop_atr: {value: 2, step: 0.5}}")
    c = cards.parse(tw)
    b, dates = panel(5)
    ds = C.days(c, b, dates)
    assert ds and ds[0].first == 2 and (ds[0].hi, ds[0].lo) == (70.2, 69.9)
    assert all(t.side == 1 for t in C.simulate(c, b, dates))


def _halt(bars, dates, halted):
    """Drop every bar from 12:00 on the given dates, so those days have no bar at the 12:30 flat_at."""
    hm, day = bars.index.strftime("%H:%M"), bars.index.strftime("%Y-%m-%d")
    return bars[~((hm >= "12:00") & day.isin(halted))]


def test_an_unresolved_exit_voids_the_card(tmp_path):
    c = cards.parse(CARD)
    p = tmp_path / "ledger.jsonl"
    ledger.append_cards(p, "run-1", [c])
    b, dates = panel(260)
    rep = gates.evaluate(c, _halt(b, dates, dates[3:5]), dates, p, COSTS, "sha", closed=frozenset(), k_scope="instrument")
    assert rep["verdict"] == "unresolved" and rep["gates"] == [] and rep["stopped_at"] is None
    assert rep["unresolved"] == {"source": "card", "count": 2, "dates": dates[3:5]}
    json.dumps(rep)


def test_calendar_exception_day_is_skipped_but_stays_a_zero_pnl_session(tmp_path):
    rep0, *_ = run(tmp_path / "a")
    _, dates = panel(260)
    rep, *_ = run(tmp_path / "b", closed=frozenset(dates[5:7]))
    assert rep["skipped_days"] == {"calendar_exception": 2} and rep["dev_sessions"][2] == 260
    assert rep["trades"] == rep0["trades"] - 2


def test_k_scope_ledger_counts_cards_across_instruments(tmp_path):
    p = tmp_path / "ledger.jsonl"
    ledger.append_cards(p, "other", [cards.parse(CARD.replace("instrument: MCL", "instrument: M2K"))])
    by_inst, *_ = run(tmp_path, k_scope="instrument")
    whole, *_ = run(tmp_path, k_scope="ledger")
    assert (by_inst["k"], by_inst["k_scope"]) == (1, "instrument") and (whole["k"], whole["k_scope"]) == (2, "ledger")
    with pytest.raises(gates.GateError, match="k_scope"):
        run(tmp_path, k_scope="family")


def test_placebo_is_labelled_timing_only_with_unchanged_threshold(tmp_path):
    rep, *_ = run(tmp_path)
    g = rep["gates"][4]
    assert g["gate"] == ("5e placebo_rank (timing-only, not the mechanism discriminator; "
                         "timing shuffle with realised side and hold)")
    assert g["threshold"] == 0.95 == gates.THRESHOLDS["5e_min_beaten_share"]


def test_unresolved_holdout_trade_spends_the_look_and_fails_it(tmp_path):
    rep, c, b, dates, p = run(tmp_path)
    look = gates.holdout_look(c, _halt(b, dates, [dates[-3]]), dates[-50:], p, "run-1", COSTS, closed=frozenset(),
                              book=rep["book"], book_sha256=pinned(rep["book"]))
    assert look["verdict"] == "unresolved" and not look["pass"]
    assert look["unresolved"] == {"source": "holdout", "count": 1, "dates": [dates[-3]]}
    assert sum(e["kind"] == "holdout_look" for e in ledger.read(p)) == 1


def test_a_plateau_neighbour_with_an_unresolved_trade_voids_the_card(tmp_path, monkeypatch):
    real = gates.C.simulate

    def sim(card, bars, dates, closed=frozenset()):
        out = real(card, bars, dates, closed)
        if card.sha256 == "":  # a neighbour: its last trade loses its exit
            out[-1] = gates.C.Trade(out[-1].date, out[-1].side, out[-1].entry_i, None, out[-1].entry_px, None, "unresolved")
        return out

    monkeypatch.setattr(gates.C, "simulate", sim)
    rep, *_ = run(tmp_path)
    assert (rep["verdict"], rep["stopped_at"]) == ("unresolved", "5d plateau")
    assert rep["unresolved"]["source"].startswith("neighbour n_bars") and rep["unresolved"]["count"] == 1


@pytest.mark.parametrize("k, n, floor, reachable", [
    (8, 812, 1.73, False), (1, 812, 0.92, False), (2, 1512, 0.88, True), (2, 1323, 0.95, False)])
def test_reachability_matches_the_d7_hand_values(k, n, floor, reachable):
    r = gates.reachability(k, n)
    assert round(r["floor_annual"], 2) == floor and r["reachable"] is reachable
    assert r["floor_annual"] == pytest.approx(r["floor_per_session"] * 252 ** 0.5)
    assert (r["k"], r["dev_sessions"], r["reachable_at"]) == (k, n, 0.89)


def test_reachability_pass_probabilities_follow_the_normal_approximation():
    r = gates.reachability(8, 812)  # the note's §8.1 table: 0.06 at a true 0.85, about 0.07 at 0.89
    assert round(r["p_pass"]["0.85"], 2) == 0.06 and round(r["p_pass"]["0.89"], 2) == 0.07
    assert round(gates.reachability(1, 812)["p_pass"]["0.85"], 2) == 0.45


def test_reachability_floor_is_where_5f_flips_under_normal_moments():
    """A normal series at the floor's per-session Sharpe has DSR 0.95 at the same K, up to the
    dropped (1 + SR^2/2) denominator term."""
    from research_utils.deflated_sharpe import deflated_sharpe, expected_max_sharpe
    k, n = 4, 900
    r = gates.reachability(k, n)
    assert deflated_sharpe(r["floor_per_session"], n, 0.0, 3.0, expected_max_sharpe(k, 1 / (n - 1))) \
        == pytest.approx(gates.THRESHOLDS["5f_min_dsr"], abs=1e-3)


def test_reachability_needs_two_sessions():
    with pytest.raises(ValueError, match="at least 2"):
        gates.reachability(1, 1)
