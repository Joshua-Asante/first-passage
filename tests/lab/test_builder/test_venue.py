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
        assert r["p_payout"] == "not encoded" and r["book_target_met"] is (r["gating_bust"] <= 0.05)
    assert noisy["label"] == venue.LABEL and "preservation" in venue.LABEL
    assert noisy["activity_convention"] == venue.ACTIVITY
    assert noisy["threshold_status"] == "approved by Joshua 2026-11-01"
    assert noisy["legs"] == ["book", "preservation"] and noisy["verdict"] == "baseline"


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


def res(gating: int, passed: int, n: int = 10_000) -> dict:
    counts = dict.fromkeys(preflight.OUTCOME_KEYS, 0)
    counts.update(bust_daily=gating, bust_inactivity=0, horizon_cap=n - gating - passed, **{"pass": passed})
    return {"status": "ok", "paths": n, "counts": counts}


@pytest.mark.parametrize("bust, passed, ok", [
    ((500, 600), (9000, 9000), True),    # bust +100 paths = +0.01 exactly
    ((500, 601), (9000, 9000), False),   # +0.0101
    ((0, 100), (9000, 9000), True),
    ((500, 500), (9000, 8900), True),    # pass -100 paths = -0.01 exactly
    ((500, 500), (9000, 8899), False),   # -0.0101
    ((500, 400), (9000, 9500), True),    # improvements pass
])
def test_tolerance_edges(bust, passed, ok):
    assert venue.VENUE_THRESHOLDS == {"book_bust_target": 0.05, "5h_max_bust_increase": 0.01,
                                      "5h_max_pass_decrease": 0.01}
    d = venue.vs_book_alone(res(bust[1], passed[1]), res(bust[0], passed[0]))
    assert venue.passes(d) is ok
    for x, y in ((0.01, 0.0), (0.0, -0.01)):
        assert venue.passes({"gating_bust": x, "p_pass": y})
    assert not venue.passes({"gating_bust": 0.0101, "p_pass": 0.0})
    assert not venue.passes({"gating_bust": 0.0, "p_pass": -0.0101})


def test_relative_verdict_needs_both_configs_and_ignores_the_target(monkeypatch):
    c = cand([("2024-01-03", 1.0, "MCL")])
    # order: Tradeify alone, Tradeify + candidate, MFFU alone, MFFU + candidate
    runs = iter([res(900, 8000), res(1000, 8000), res(900, 8000), res(1001, 8000)])
    monkeypatch.setattr(venue, "simulate", lambda firm, p: next(runs))
    rep = venue.evaluate(book(), c)
    assert [rep["configs"][f]["relative_pass"] for f in FIRMS] == [True, False] and rep["verdict"] == "fail"
    # a book far above the 0.05 target still passes a candidate that keeps within tolerance
    runs = iter([res(900, 8000), res(1000, 8000), res(900, 8000), res(950, 7950)])
    rep = venue.evaluate(book(), c)
    assert rep["verdict"] == "pass"
    with pytest.raises(venue.VenueError, match="unpaired"):
        venue.vs_book_alone(res(0, 0, n=9_000), res(0, 0))


def test_preservation_leg_placement_and_cost():
    # Wed 2024-01-03 .. Tue 2024-01-23: complete weeks start Mon 01-08 and Mon 01-15; Mon 01-22 is partial
    rt = {"Tradeify_Select_100K": 2 * (0.91 + 0.25 * 2.0), "MFFU_Rapid_100K": 2 * (0.95 + 0.25 * 2.0)}
    for firm, cost in rt.items():
        assert venue.preservation_daily(firm, "2024-01-03", "2024-01-23") == pytest.approx(
            {"2024-01-08": -cost, "2024-01-15": -cost})
    # the book's Monday 01-08 is a zero row: the preservation leg makes it active anyway
    b = {"2024-01-03": 1.0, "2024-01-09": 2.0, "2024-01-16": 3.0, "2024-01-23": 4.0}
    legs = {"book": b, "preservation": venue.preservation_daily(FIRMS[0], "2024-01-03", "2024-01-23")}
    blk = venue.blocks(venue.panel(legs, "2024-01-03", "2024-01-23"))
    assert blk.shape == (2, 5, 2) and blk[0][0, 0] == 0.0
    assert blk[:, 0, 1] == pytest.approx([-rt[FIRMS[0]]] * 2) and not blk[:, 1:, 1].any()
    assert (np.abs(blk).sum(axis=2) > 0)[:, 0].all()


def test_book_alone_and_candidate_runs_share_seeds_and_weeks(monkeypatch):
    seen = []
    real = venue.run_seed

    def spy(seed, n, b, **kw):
        seen.append((seed, n, len(b), kw["horizon"], kw["strats"]))
        return real(seed, n, b, **kw)
    monkeypatch.setattr(venue, "run_seed", spy)
    b = book(weeks=6)
    venue.evaluate(b, cand([("2024-01-03", 1.0, "MCL")], window=(min(b), max(b))))
    per_run = len(venue.SEEDS)
    runs = [seen[i:i + per_run] for i in range(0, len(seen), per_run)]
    assert len(runs) == 4
    for alone, with_c in (runs[0:2], runs[2:4]):
        assert [s[:4] for s in alone] == [s[:4] for s in with_c]
        assert [s[0] for s in alone] == list(venue.SEEDS) and alone[0][2] == 6
        assert alone[0][4] == ("book", "preservation") and with_c[0][4] == ("book", "preservation", "candidate")


def test_book_alone_equals_book_plus_zero_candidate(noisy):
    b = book(seed=7, daily=150.0)
    rep = venue.evaluate(b, cand(window=(min(b), max(b))))
    for firm in FIRMS:
        r, alone = rep["configs"][firm], noisy["configs"][firm]
        assert r["counts"] == alone["counts"] and r["book_alone"] == alone
        assert r["vs_book_alone"] == {"gating_bust": 0.0, "p_pass": 0.0} and r["relative_pass"]
    assert rep["verdict"] == "pass"  # a zero candidate passes, whatever the book's target result


def test_book_costs_are_not_repriced_per_config():
    # A steady book passes everywhere: only the small preservation cost differs per config.
    rep = venue.evaluate(book(daily=300.0))
    assert all(rep["configs"][f]["counts"]["pass"] == 10_000 and rep["configs"][f]["book_target_met"]
               for f in FIRMS) and rep["verdict"] == "baseline"
