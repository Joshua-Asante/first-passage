"""Strategy builder v1, build step 3: gates 5a-5f, report, holdout look and 5g placement (I-S2, I-S3, I-K3, I-G3..I-G6, I-L4)."""
from __future__ import annotations

import dataclasses
import json

import numpy as np
import pytest

from builder import cards, gates, ledger
from tests.lab.test_builder.builder_inputs import CARD, panel, walk_panel

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
    assert rep1["gates"][4]["value"] == rep2["gates"][4]["value"]
    assert rep1["gates"][4]["value"]["beaten_share"] > 0.95


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
    b, dates = panel(5)
    assert gates.placebo_beaten_share(c, b, dates, [], COSTS, 10, 1)["beaten_share"] == 0.0


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
                         "same-day window slide of the clock frame)")
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


# ---- 5e same-day window-slide placebo (lesson M-17; I-1..I-8 of the PR's invariant table)

JUMP_CARD = """
id: j-001
family: orb
instrument: MCL
entry: {type: breakout, range: first_n_bars, side: both, order: stop}
exit: {stop: range_opposite, target: none, flat_at: "11:00"}
time: {entry_cutoff: "09:45"}
params: {n_bars: {value: 2, step: 1}}
"""
WALK_CARD = JUMP_CARD.replace('flat_at: "11:00"', 'flat_at: "15:00"').replace('"09:45"', '"12:00"')


def _old_timing_shuffle(card, days, trades, costs, runs, seed):
    """The 5e placebo this PR replaces (main before it), kept here only as the regression's foil."""
    by = {d.date: d for d in days}
    pv, c = gates.INSTRUMENTS[card.instrument].point_value, costs.per_trade(card.instrument)
    rng = np.random.default_rng(seed)
    tot = np.zeros(runs)
    for t in trades:
        d = by[t.date]
        e = rng.integers(d.first, d.cutoff, size=runs)
        x = np.minimum(e + (t.exit_i - t.entry_i), d.flat)
        n = len(d.times)
        exit_px = np.where(x < n, d.o[np.minimum(x, n - 1)], d.c[n - 1])
        exit_px = np.where(x == e, d.c[e], exit_px)
        tot += t.side * (exit_px - d.o[e]) * pv - c
    return float((tot < gates.net(card, trades, costs).sum()).mean())


def test_5e_regression_the_slide_does_not_ride_the_breakout_that_chose_the_side():
    """The 09:30 bar jumps out of the opening range; afterwards the day is a symmetric walk. The
    old shuffle enters at that bar's open with the side the jump revealed and beats the card on
    every run; every slide's range sits after the jump and earns nothing from it."""
    c = cards.parse(JUMP_CARD)
    b, dates = walk_panel(120, 1, jump=0.6)
    trades = gates.C.simulate(c, b, dates)
    assert _old_timing_shuffle(c, gates.C.days(c, b, dates), trades, COSTS, 1000, 1) == 0.0
    r = gates.placebo_beaten_share(c, b, dates, trades, COSTS, 1000, 1)
    assert r["beaten_share"] >= 0.95 and r["null_mean"] < 0 < r["real_net"] and r["null_sd"] > 0


def test_5e_zero_edge_false_pass_is_near_the_threshold_tail():
    """Symmetric zero-drift walk, |S| = 7. Exchangeable-window bound at |S| = 7 is 0.077 (the
    draws exclude delta 0). Tolerance: at most 4 of 20 seeds pass (P(X >= 5 | p = 0.077) ~ 0.04)
    and the mean share lies in [0.3, 0.7]."""
    c = cards.parse(WALK_CARD)
    assert gates.slide_line(c)["slides"] == 7
    shares = []
    for seed in range(20):
        b, dates = walk_panel(150, 100 + seed)
        shares.append(gates.placebo_beaten_share(c, b, dates, gates.C.simulate(c, b, dates), COSTS, 1000,
                                                 seed)["beaten_share"])
    shares = np.array(shares)
    assert (shares >= gates.THRESHOLDS["5e_min_beaten_share"]).sum() <= 4 and 0.3 <= shares.mean() <= 0.7


def test_5e_fails_closed_below_the_minimum_slide_count(tmp_path):
    c = cards.parse(WALK_CARD.replace('flat_at: "15:00"', 'flat_at: "16:00"'))
    line = gates.slide_line(c)
    assert (line["slides"], line["meets_min"], line["delta_bars"]) == (3, False, [1, 3]) and gates.SLIDE_MIN == 5
    b, dates = walk_panel(30, 3)
    r = gates.placebo_beaten_share(c, b, dates, gates.C.simulate(c, b, dates), COSTS, 100, 1)
    assert r["beaten_share"] is None and "fewer than 5" in r["reason"]
    none = cards.parse(WALK_CARD.replace('flat_at: "15:00"', 'flat_at: "17:00"'))
    assert gates.slides(none) == [] and gates.slide_line(none)["zero_edge_false_pass_bound"] is None


def test_5e_fails_closed_on_a_zero_variance_null():
    c = cards.parse(JUMP_CARD)
    b, dates = walk_panel(40, 2, jump=0.6)
    flat = b.copy()
    late = flat.index.strftime("%H:%M") >= "09:45"
    flat.loc[late, ["open", "high", "low", "close"]] = 70.0  # no slide ever breaks out
    r = gates.placebo_beaten_share(c, flat, dates, gates.C.simulate(c, flat, dates), COSTS, 100, 1)
    assert r["beaten_share"] is None and r["reason"] == "the slide null has zero variance"


def test_5e_I3_a_slide_moves_only_the_clock_frame():
    c = cards.parse(WALK_CARD)
    s = gates.slid(c, 3)
    diff = {f.name for f in dataclasses.fields(c) if getattr(c, f.name) != getattr(s, f.name)}
    assert diff == {"range", "params", "entry_cutoff", "flat_at", "sha256", "source"}  # identity blanked, as neighbours
    assert (s.range, s.entry_cutoff, s.flat_at, s.range_start()) == ("time_window", "12:45", "15:45", "09:45")
    assert [q for q in s.params if q[0] != "offset_bars"] == list(c.params) and s.p("offset_bars") == 3
    tw = cards.parse(WALK_CARD.replace("range: first_n_bars", "range: time_window").replace(
        "params: {", "params: {offset_bars: {value: 2, step: 2}, "))
    s2 = gates.slid(tw, -1)
    assert s2.range == "time_window" and ("offset_bars", 1, 2) in s2.params and s2.flat_at == "14:45"


def test_5e_I4_only_valid_slides():
    c = cards.parse(WALK_CARD)
    assert gates.slid(c, 0) is None and gates.slid(c, -1) is None  # delta 0; offset below 0
    assert gates.slid(c, 8) is None  # flat_at 17:00 = DAY_END: no flat bar on any day
    assert [d for d, _ in gates.slides(c)] == list(range(1, 8))
    tw = cards.parse(WALK_CARD.replace("range: first_n_bars", "range: time_window").replace(
        "params: {", "params: {offset_bars: {value: 2, step: 1}, "))
    assert [d for d, _ in gates.slides(tw)] == [-2, -1] + list(range(1, 8))
    assert all(cards._timing_error(s) is None for _, s in gates.slides(tw))


def test_5e_I1_I2_slid_trades_are_causal_and_same_day():
    c = cards.parse(WALK_CARD)
    b, dates = walk_panel(12, 5)
    S = gates.slides(c)
    m, *_ = gates.slide_matrix(S, b, dates, COSTS)
    other = b.copy()
    other.loc[other.index.strftime("%Y-%m-%d") == dates[4], "close"] += 0.5  # perturb one day only
    m2, *_ = gates.slide_matrix(S, other, dates, COSTS)
    assert np.array_equal(np.delete(m, 4, 0), np.delete(m2, 4, 0))  # I-2
    for _, s in S:  # I-1: bars after a slid trade's entry bar never change its side or entry
        for d in gates.C.days(s, b, dates):
            for t in gates.C.simulate_day(s, d)[:1]:
                cut = dataclasses.replace(d, h=d.h.copy(), l=d.l.copy(), o=d.o.copy(), c=d.c.copy())
                cut.h[t.entry_i + 1:] += 5; cut.l[t.entry_i + 1:] -= 5
                t2 = gates.C.simulate_day(s, cut)[0]
                assert (t2.side, t2.entry_i, t2.entry_px) == (t.side, t.entry_i, t.entry_px)


def test_5e_I7_I8_holdout_untouched_and_unresolved_slides_count_zero(tmp_path):
    rep, c, b, dates, _ = run(tmp_path)  # the panel ends 13:00: slides flat after it are unresolved
    v = rep["gates"][4]["value"]
    assert rep["verdict"] == "survivor" and v["slid_unresolved_sessions"] > 0 and rep["thresholds"] == gates.THRESHOLDS
    dev = dates[:200]
    tr = gates.C.simulate(c, b, dev)
    later = b.copy()
    later.loc[later.index.strftime("%Y-%m-%d") > dev[-1], "close"] += 1.0
    assert (gates.placebo_beaten_share(c, b, dev, tr, COSTS, 200, 1)
            == gates.placebo_beaten_share(c, later, dev, tr, COSTS, 200, 1))


def test_5e_is_deterministic_and_seeded():
    c = cards.parse(WALK_CARD)
    b, dates = walk_panel(60, 9)
    tr = gates.C.simulate(c, b, dates)
    a1, a2 = (gates.placebo_beaten_share(c, b, dates, tr, COSTS, 500, 7) for _ in range(2))
    assert a1 == a2
    assert gates.placebo_beaten_share(c, b, dates, tr, COSTS, 500, 8)["null_mean"] != a1["null_mean"]
