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
