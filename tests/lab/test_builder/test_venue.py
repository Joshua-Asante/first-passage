"""Gate 5h venue MC (lab/builder/venue.py), synthetic data only."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from builder import venue
from mc import preflight

FIRMS = tuple(venue.CONFIGS)


def book(start="2024-01-01", weeks=20, daily=300.0, seed=None) -> dict[str, float]:
    """Mon-Fri sessions from a Monday; drift `daily`, or a seeded noisy series."""
    days = pd.bdate_range(start, periods=5 * weeks)
    rng = np.random.default_rng(seed)
    vals = np.full(len(days), daily) if seed is None else rng.normal(daily, 900.0, len(days))
    return {d.strftime("%Y-%m-%d"): float(v) for d, v in zip(days, vals)}


def cand(trades=(), window=("2024-01-01", "2024-05-17")) -> venue.Candidate:
    return venue.Candidate(tuple(venue.Trade(*t) for t in trades), window)


@pytest.fixture(scope="module")
def noisy():
    return venue.evaluate(book(seed=7, daily=150.0))


def test_counts_partition_ten_thousand_paths_per_config(noisy):
    for firm in FIRMS:
        r = noisy["configs"][firm]
        assert r["status"] == "ok" and r["paths"] == 10_000
        assert set(r["counts"]) == set(preflight.OUTCOME_KEYS) and sum(r["counts"].values()) == 10_000
        c = r["counts"]
        assert r["gating_bust"] == (c["bust_daily"] + c["bust_static"] + c["bust_trailing"]
                                    + c["bust_inactivity"]) / 10_000
        assert r["p_pass"] == c["pass"] / 10_000 and r["horizon_cap"] == c["horizon_cap"] / 10_000
        assert r["p_payout"] == "not encoded"
    assert noisy["label"] == venue.LABEL and noisy["activity_convention"] == venue.ACTIVITY
    assert noisy["threshold_status"] == "pending Joshua's approval"


def test_seed_determinism(noisy):
    assert venue.evaluate(book(seed=7, daily=150.0)) == noisy


def test_firm_kwargs_pinned(monkeypatch):
    seen = []
    real = preflight.firm_kwargs

    def spy(firm, **kw):
        seen.append((firm, kw))
        return real(firm, **kw)
    monkeypatch.setattr(preflight, "firm_kwargs", spy)
    venue.evaluate(book())
    assert seen == [(f, {"inactivity_off": False, "consistency": c, "account": 100_000,
                         "allow_unsourced_inactivity": False, "allow_provisional_rules": False})
                    for f, c in (("Tradeify_Select_100K", 0.40), ("MFFU_Rapid_100K", 0.50))]


def test_unsourced_inactivity_is_refused_not_overridden(monkeypatch):
    monkeypatch.setitem(preflight.FIRM_RULES["MFFU_Rapid_100K"], "inactivity_rule_sourced", False)
    rep = venue.evaluate(book())
    r = rep["configs"]["MFFU_Rapid_100K"]
    assert r["status"] == "refused" and "inactivity_rule_sourced=False" in r["reason"]
    assert rep["configs"]["Tradeify_Select_100K"]["status"] == "ok" and rep["verdict"] == "refused"


def test_missing_per_symbol_commission_is_refused():
    rep = venue.evaluate(book(), cand([("2024-01-03", 1.0, "MGC")]))
    assert all(rep["configs"][f]["status"] == "refused" and "MGC" in rep["configs"][f]["reason"] for f in FIRMS)
    assert rep["verdict"] == "refused"


def test_costs_applied_per_config():
    c = cand([("2024-01-03", 2.0, "MCL"), ("2024-01-03", -1.0, "MCL"), ("2024-01-04", 0.5, "MCL")])
    # MCL: point value 100, tick 0.01 -> 1 tick = $1; commission per side 1.06 (Tradeify), 0.58 (MFFU)
    rt = {"Tradeify_Select_100K": 2 * (1.06 + 1.0), "MFFU_Rapid_100K": 2 * (0.58 + 1.0)}
    for firm, cost in rt.items():
        d = venue.candidate_daily(c, firm)
        assert d == pytest.approx({"2024-01-03": 100.0 - 2 * cost, "2024-01-04": 50.0 - cost})


def test_panel_is_every_weekday_zero_filled_and_blocks_are_complete_weeks():
    # Wed 2024-01-03 .. Tue 2024-01-23: a partial first week, two complete weeks, a partial last week
    b = {"2024-01-03": 1.0, "2024-01-08": 2.0, "2024-01-12": 3.0, "2024-01-23": 4.0}
    p = venue.panel({"book": b, "candidate": {"2024-01-09": -5.0}}, "2024-01-03", "2024-01-23")
    assert list(p.index) == list(pd.bdate_range("2024-01-03", "2024-01-23")) and list(p.columns) == ["book", "candidate"]
    assert p.loc["2024-01-04", "book"] == 0.0 and p.loc["2024-01-09", "candidate"] == -5.0
    assert p["candidate"].abs().sum() == 5.0
    blk = venue.blocks(p)
    assert blk.shape == (2, 5, 2)
    assert blk[0][:, 0].tolist() == [2.0, 0, 0, 0, 3.0] and blk[1][:, 0].tolist() == [0.0] * 5
    with pytest.raises(venue.VenueError, match="no complete Mon-Fri week"):
        venue.blocks(venue.panel({"book": b}, "2024-01-03", "2024-01-05"))


def test_window_is_the_intersection():
    b = book(weeks=20)  # 2024-01-01 .. 2024-05-17
    assert venue.window(b, None) == ("2024-01-01", "2024-05-17")
    assert venue.window(b, cand(window=("2023-06-01", "2024-03-01"))) == ("2024-01-01", "2024-03-01")
    assert venue.window(b, cand(window=("2024-02-05", "2025-01-01"))) == ("2024-02-05", "2024-05-17")
    with pytest.raises(venue.VenueError, match="do not overlap"):
        venue.window(b, cand(window=("2025-01-01", "2025-02-01")))
    rep = venue.evaluate(b, cand(window=("2024-02-05", "2025-01-01")))
    assert rep["window"] == ["2024-02-05", "2024-05-17"] and rep["complete_weeks"] == 15


def test_inputs_fail_closed():
    with pytest.raises(venue.VenueError, match="outside its window"):
        venue.evaluate(book(), cand([("2024-06-03", 1.0, "MCL")]))
    with pytest.raises(venue.VenueError, match="weekend"):
        venue.evaluate({**book(), "2024-01-06": 1.0})
    with pytest.raises(venue.VenueError, match="empty"):
        venue.evaluate({})
    for bad in (float("nan"), float("inf"), True):
        with pytest.raises(venue.VenueError, match="non-finite points"):
            venue.evaluate(book(), cand([("2024-01-03", -3.0, "MCL"), ("2024-01-03", bad, "MCL")]))
        with pytest.raises(venue.VenueError, match="non-finite amounts"):
            venue.evaluate({**book(), "2024-01-03": bad})


@pytest.mark.parametrize("bust, ok", [(0.0499, True), (0.05, True), (500 / 10_000, True), (0.0501, False),
                                      (501 / 10_000, False)])
def test_ceiling_at_and_around_five_percent(bust, ok):
    assert venue.VENUE_THRESHOLDS == {"5h_bust_ceiling": 0.05}
    assert venue.passes(bust) is ok


def test_verdict_needs_both_configs(monkeypatch):
    rates = iter([0.05, 0.0501])
    monkeypatch.setattr(venue, "simulate", lambda firm, p: {"status": "ok", "gating_bust": next(rates)})
    assert venue.evaluate(book())["verdict"] == "fail"
    rates = iter([0.05, 0.0499])
    assert venue.evaluate(book())["verdict"] == "pass"


def test_book_alone_equals_book_plus_zero_candidate(noisy):
    b = book(seed=7, daily=150.0)
    rep = venue.evaluate(b, cand(window=(min(b), max(b))))
    for firm in FIRMS:
        r, alone = rep["configs"][firm], noisy["configs"][firm]
        assert r["counts"] == alone["counts"] and r["book_alone"] == alone
        assert r["vs_book_alone"] == {"gating_bust": 0.0, "p_pass": 0.0}
    assert rep["verdict"] == noisy["verdict"]


def test_book_costs_are_not_repriced_per_config():
    # A steady book passes everywhere in the same number of days: no per-config cost touched it.
    rep = venue.evaluate(book(daily=300.0))
    assert all(rep["configs"][f]["counts"]["pass"] == 10_000 for f in FIRMS) and rep["verdict"] == "pass"
