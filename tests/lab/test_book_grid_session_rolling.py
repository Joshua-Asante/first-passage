"""Regression guards on the two fixes from the second Codex review of PR #260.

1. `roll_to_session` -- TradingView books a carried position's P&L on its own exit date,
   which for a weekend or exchange-closure carry is a Saturday, Sunday, or closed weekday.
   `build_cell` reindexes onto `pd.bdate_range`, so such a booking was silently DROPPED:
   6 trades, -210.92 per contract of REAL LOSSES, making the book look safer than it was.
   These tests fail if the roll stops landing on a real session.

2. `_et_hhmm` -- the final-print cutoff must be applied in Eastern time. The ~15:50 ET
   print lands at 19:50 UTC in EDT but 20:50 UTC in EST, so a fixed UTC cutoff silently
   excluded every winter print from the candidate set.

Both modules are imported by path because the campaign slug is hyphenated.
"""
from __future__ import annotations

import importlib.util
import pathlib

import pytest

_CAMPAIGN = (pathlib.Path(__file__).resolve().parents[2] / "lab" / "analysis" / "c1"
             / "tradeify_book_composition_2026-09")
_GRID = _CAMPAIGN / "book_grid.py"
_PARSER = _CAMPAIGN / "scrape" / "build_moc_table.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def grid():
    if not _GRID.exists():
        pytest.skip(f"absent: {_GRID}")
    if not (_CAMPAIGN / "data" / "cme_equity_sessions.json").exists():
        pytest.skip("session calendar absent")
    return _load(_GRID, "book_grid_under_test")


@pytest.fixture(scope="module")
def parser():
    if not _PARSER.exists():
        pytest.skip(f"absent: {_PARSER}")
    return _load(_PARSER, "moc_build_under_test")


# ---------------------------------------------------------------- roll_to_session

@pytest.mark.parametrize("booked,expected,why", [
    ("2022-11-27", "2022-11-28", "Sunday carry from the Thanksgiving half-day"),
    ("2024-12-01", "2024-12-02", "Sunday carry"),
    ("2024-12-25", "2024-12-26", "Christmas Day is a weekday the exchange is closed"),
    ("2025-12-25", "2025-12-26", "Christmas Day, second instance"),
    ("2026-04-03", "2026-04-06", "Good Friday rolls across the weekend"),
    ("2025-01-09", "2025-01-10", "2025 national day of mourning"),
])
def test_roll_lands_on_next_real_session(grid, booked, expected, why):
    import pandas as pd
    got = grid.roll_to_session(pd.Timestamp(booked))
    assert str(got.date()) == expected, why


def test_roll_is_identity_on_a_real_session(grid):
    import pandas as pd
    for d in ("2025-06-10", "2024-11-29", "2026-06-30"):
        assert grid.roll_to_session(pd.Timestamp(d)) == pd.Timestamp(d)


def test_roll_never_returns_a_weekend(grid):
    import pandas as pd
    for d in pd.date_range("2022-08-01", "2026-07-01", freq="D"):
        assert grid.roll_to_session(d).weekday() < 5


def test_no_weekend_buckets_survive_in_the_pnl_series(grid):
    """The end-to-end property: after rolling, no leg books P&L on a date the path drops."""
    import os
    for leg in ("mnq", "mym", "aegis"):
        p = os.path.join(grid.DOWNLOADS, grid.LEG_FILES[leg])
        if not os.path.exists(p):
            pytest.skip(f"vendor export absent: {leg}")
        s = grid.daily_per_contract(grid.load_trades(p))
        weekend = [d for d in s.index if d.weekday() >= 5]
        assert not weekend, f"{leg} still books P&L on {weekend[:3]}"


# -------------------------------------------- window selection uses the ROLLED date
#
# Both channels must agree on which window a trade belongs to. `daily_per_contract`
# buckets by `roll_to_session(exit_date)`, so filtering `slice_trades` on the RAW
# `exit_date` split them: a trade exiting on a non-session immediately before a window
# start rolled INTO that window's P&L series while being excluded from the intraday
# reconstruction, and `build_cell`'s reconstruction-mismatch assertion would fire instead
# of a grid being produced. Latent on the committed exports (measured: zero trades fall in
# the gap for any leg against either window), but a real inconsistency introduced by the
# roll fix itself. Raised by Codex on PR #271 (round 7).

def _trade(exit_date, pnl=-100.0):
    import pandas as pd
    ts = pd.Timestamp(exit_date)
    return {"trade_number": exit_date, "entry_time": ts, "exit_time": ts,
            "entry_date": ts, "exit_date": ts, "qty": 1.0, "side": "long",
            "net_pnl_per_contract": pnl, "mae_per_contract": -50.0,
            "signal_entry": "e", "signal_exit": "x"}


def test_slice_trades_keeps_a_trade_whose_roll_lands_inside_the_window(grid):
    """Sunday 2022-07-31 rolls to Monday 2022-08-01, the WINDOW start: it must be kept."""
    import pandas as pd
    assert grid.roll_to_session(pd.Timestamp("2022-07-31")) == pd.Timestamp("2022-08-01")
    kept = grid.slice_trades([_trade("2022-07-31")], "2022-08-01", "2026-07-01")
    assert len(kept) == 1, (
        "trade booked into the window by roll_to_session was dropped by slice_trades; "
        "build_cell would raise its reconstruction-mismatch assertion")


def test_slice_trades_drops_a_trade_whose_roll_lands_outside(grid):
    """The rule must still exclude, not merely include -- otherwise it is not a filter."""
    kept = grid.slice_trades([_trade("2022-07-28")], "2022-08-01", "2026-07-01")
    assert kept == []


def test_slice_trades_agrees_with_daily_per_contract_on_the_real_exports(grid):
    """End-to-end: the two channels must select the same trades on the real data."""
    import os
    import pandas as pd
    start, end = pd.Timestamp("2022-08-01"), pd.Timestamp("2026-07-01")
    for leg in ("mnq", "mym", "aegis"):
        p = os.path.join(grid.DOWNLOADS, grid.LEG_FILES[leg])
        if not os.path.exists(p):
            pytest.skip(f"vendor export absent: {leg}")
        trades = grid.load_trades(p)
        sliced = {t["trade_number"] for t in grid.slice_trades(trades, start, end)}
        booked = {t["trade_number"] for t in trades
                  if start <= grid.roll_to_session(t["exit_date"]) <= end}
        assert sliced == booked, f"{leg}: channels disagree on {sliced ^ booked}"


# ---------------------------------------------------------------- ET cutoff

def test_et_cutoff_is_dst_aware(parser):
    """Both the EDT and the EST print are the same wall-clock time in Eastern."""
    assert parser._et_hhmm("2026-08-31T19:50:59+00:00") == "15:50"   # EDT
    assert parser._et_hhmm("2026-01-30T20:50:00+00:00") == "15:50"   # EST


def test_winter_print_is_not_excluded_by_the_cutoff(parser):
    """A 20:50 UTC (EST) print is 15:50 ET and must sit inside a 17:00 ET cutoff.

    Under the old fixed `<= "20:30"` UTC test it fell outside, so on any winter day that
    also carried an earlier non-early post the earlier post would have been selected.
    """
    assert parser._et_hhmm("2026-01-30T20:50:00+00:00") <= "17:00"
