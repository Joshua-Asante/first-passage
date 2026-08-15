"""Tests for the DJ30 force-flat-at-17:00-ET transform (Bulenox futures-prop
pivot). All synthetic — no vendor CSV data required; this module must be
fully verifiable before real Pepperstone/bar data ever lands.
"""

from __future__ import annotations

from datetime import datetime

import pandas as pd

from research_utils.camp_import import load_camp_sibling

_fft = load_camp_sibling("force_flat_transform", __file__)
bars_utc_to_et = _fft.bars_utc_to_et
first_boundary_crossing = _fft.first_boundary_crossing
force_flat_csv = _fft.force_flat_csv
force_flat_trade = _fft.force_flat_trade

ET_HOUR = 17


# ── first_boundary_crossing: pure datetime logic ────────────────────────

def test_no_crossing_same_day_before_boundary():
    """Entry 09:00, exit 16:00 same day — never reaches 17:00. No crossing."""
    entry = datetime(2026, 1, 5, 9, 0)
    exit_ = datetime(2026, 1, 5, 16, 0)
    assert first_boundary_crossing(entry, exit_, ET_HOUR) is None


def test_crossing_when_exit_after_boundary_same_day():
    """Entry 09:00, exit 18:00 same day — crosses 17:00 that day."""
    entry = datetime(2026, 1, 5, 9, 0)
    exit_ = datetime(2026, 1, 5, 18, 0)
    crossing = first_boundary_crossing(entry, exit_, ET_HOUR)
    assert crossing == datetime(2026, 1, 5, 17, 0)


def test_crossing_exactly_at_boundary_counts_as_crossed():
    """Exit at exactly 17:00:00 — the trade is open through the boundary instant."""
    entry = datetime(2026, 1, 5, 9, 0)
    exit_ = datetime(2026, 1, 5, 17, 0)
    assert first_boundary_crossing(entry, exit_, ET_HOUR) == datetime(2026, 1, 5, 17, 0)


def test_entry_after_todays_boundary_looks_to_next_day():
    """Entry at 18:00 (already past today's 17:00) — the next boundary is
    tomorrow's 17:00, not a stale timestamp in the past."""
    entry = datetime(2026, 1, 5, 18, 0)
    exit_ = datetime(2026, 1, 6, 20, 0)
    crossing = first_boundary_crossing(entry, exit_, ET_HOUR)
    assert crossing == datetime(2026, 1, 6, 17, 0)


def test_multi_day_hold_returns_first_crossing_only():
    """A trade spanning several days must truncate at the FIRST boundary,
    not the last — force-flat closes it the very first time it's caught open."""
    entry = datetime(2026, 1, 5, 9, 0)
    exit_ = datetime(2026, 1, 8, 12, 0)  # 3 boundaries would be crossed if held
    crossing = first_boundary_crossing(entry, exit_, ET_HOUR)
    assert crossing == datetime(2026, 1, 5, 17, 0)


def test_entry_exactly_at_boundary_looks_forward_not_backward():
    """Entry at exactly 17:00:00 — the relevant boundary is the NEXT day's
    (a trade can't be 'caught open' by the same instant it opened)."""
    entry = datetime(2026, 1, 5, 17, 0)
    exit_ = datetime(2026, 1, 6, 20, 0)
    crossing = first_boundary_crossing(entry, exit_, ET_HOUR)
    assert crossing == datetime(2026, 1, 6, 17, 0)


# ── force_flat_trade: price-ratio truncation ────────────────────────────

def _bars(rows: list[tuple]) -> pd.DataFrame:
    """rows: list of (time, close) tuples."""
    return pd.DataFrame(rows, columns=["time", "close"])


def test_trade_closed_before_boundary_is_untouched():
    entry_dt = datetime(2026, 1, 5, 9, 0)
    exit_dt = datetime(2026, 1, 5, 16, 0)
    bars = _bars([(datetime(2026, 1, 5, 17, 0), 30_100.0)])
    new_exit_dt, new_pnl, truncated = force_flat_trade(
        entry_dt, exit_dt, entry_price=30_000.0, exit_price=30_050.0, pnl=500.0,
        bars_df=bars, hour_et=ET_HOUR,
    )
    assert not truncated
    assert new_exit_dt == exit_dt
    assert new_pnl == 500.0


def test_trade_open_through_boundary_is_truncated_proportionally():
    """Entry 30,000, original exit 30,100 (pnl=$1,000 for a long), but the
    17:00 bar closes at 30,050 (halfway) -- force-flat pnl must be $500."""
    entry_dt = datetime(2026, 1, 5, 9, 0)
    exit_dt = datetime(2026, 1, 5, 20, 0)  # would have closed after the boundary
    bars = _bars([(datetime(2026, 1, 5, 17, 0), 30_050.0)])
    new_exit_dt, new_pnl, truncated = force_flat_trade(
        entry_dt, exit_dt, entry_price=30_000.0, exit_price=30_100.0, pnl=1_000.0,
        bars_df=bars, hour_et=ET_HOUR,
    )
    assert truncated
    assert new_exit_dt == datetime(2026, 1, 5, 17, 0)
    assert new_pnl == 500.0


def test_truncation_can_flip_a_winner_into_a_loser():
    """Original exit was a winner, but the 17:00 price was still underwater --
    force-flat must show the loss that was actually live at that moment, not
    the eventual (post-boundary) outcome."""
    entry_dt = datetime(2026, 1, 5, 9, 0)
    exit_dt = datetime(2026, 1, 5, 20, 0)
    bars = _bars([(datetime(2026, 1, 5, 17, 0), 29_900.0)])  # below entry
    _, new_pnl, truncated = force_flat_trade(
        entry_dt, exit_dt, entry_price=30_000.0, exit_price=30_200.0, pnl=2_000.0,
        bars_df=bars, hour_et=ET_HOUR,
    )
    assert truncated
    assert new_pnl == -1_000.0  # (29900-30000)/(30200-30000) * 2000 = -1000


def test_zero_price_range_truncated_trade_is_a_scratch():
    """Degenerate case: entry price == original exit price (a scratch trade
    that happened to hold through the boundary). Truncated pnl is 0, not a
    division-by-zero crash."""
    entry_dt = datetime(2026, 1, 5, 9, 0)
    exit_dt = datetime(2026, 1, 5, 20, 0)
    bars = _bars([(datetime(2026, 1, 5, 17, 0), 30_050.0)])
    _, new_pnl, truncated = force_flat_trade(
        entry_dt, exit_dt, entry_price=30_000.0, exit_price=30_000.0, pnl=0.0,
        bars_df=bars, hour_et=ET_HOUR,
    )
    assert truncated
    assert new_pnl == 0.0


def test_missing_bar_raises_instead_of_silently_passing_through():
    """If the nearest prior bar is a full day before the boundary (a real data
    gap, not a session break), this must fail loudly -- truncating at a
    day-stale price would corrupt the MC's whole premise."""
    entry_dt = datetime(2026, 1, 5, 9, 0)
    exit_dt = datetime(2026, 1, 5, 20, 0)
    bars = _bars([(datetime(2026, 1, 4, 17, 0), 29_000.0)])  # 24h before boundary
    try:
        force_flat_trade(
            entry_dt, exit_dt, entry_price=30_000.0, exit_price=30_100.0, pnl=1_000.0,
            bars_df=bars, hour_et=ET_HOUR,
        )
        assert False, "expected a lookup failure for a day-stale boundary bar"
    except KeyError:
        pass


def test_boundary_uses_last_bar_before_session_break():
    """17:00 ET falls in the CME/CFD 17:00-18:00 settlement break, so no bar is
    stamped exactly 17:00. The fill must use the last pre-break bar (16:45,
    whose close is the 17:00 price) via backward-asof, not raise."""
    entry_dt = datetime(2026, 1, 5, 9, 0)
    exit_dt = datetime(2026, 1, 5, 20, 0)  # held past the 17:00 boundary
    bars = _bars([
        (datetime(2026, 1, 5, 16, 30), 30_040.0),
        (datetime(2026, 1, 5, 16, 45), 30_050.0),  # last bar before the break
        (datetime(2026, 1, 5, 18, 0), 30_090.0),   # session resumes (post-flat)
    ])
    new_exit_dt, new_pnl, truncated = force_flat_trade(
        entry_dt, exit_dt, entry_price=30_000.0, exit_price=30_100.0, pnl=1_000.0,
        bars_df=bars, hour_et=ET_HOUR,
    )
    assert truncated
    assert new_exit_dt == datetime(2026, 1, 5, 17, 0)
    assert new_pnl == 500.0  # (30050-30000)/(30100-30000)*1000, using the 16:45 close


# ── bars_utc_to_et: BAR_EXPORT bars are UTC; trades CSVs are chart-TZ ET ──
# (reference_bar_export_epoch_utc) -- force_flat_trade's bars_df lookup is a
# naive tz-less `==`, so bars must be pre-converted or every lookup silently
# misses/mismatches by the UTC-ET offset.

def test_bars_utc_to_et_standard_time():
    """January (EST, UTC-5): 17:00 ET == 22:00 UTC."""
    bars = pd.DataFrame({"time": ["2026-01-15T22:00:00Z"], "close": [30_000.0]})
    out = bars_utc_to_et(bars)
    assert out["time"].iloc[0] == datetime(2026, 1, 15, 17, 0)


def test_bars_utc_to_et_daylight_time():
    """July (EDT, UTC-4): 17:00 ET == 21:00 UTC -- DST-aware, not a flat -5 offset."""
    bars = pd.DataFrame({"time": ["2026-07-15T21:00:00Z"], "close": [30_000.0]})
    out = bars_utc_to_et(bars)
    assert out["time"].iloc[0] == datetime(2026, 7, 15, 17, 0)


def test_bars_utc_to_et_does_not_mutate_input():
    bars = pd.DataFrame({"time": ["2026-01-15T22:00:00Z"], "close": [30_000.0]})
    original = bars.copy()
    bars_utc_to_et(bars)
    pd.testing.assert_frame_equal(bars, original)


# ── force_flat_csv: raw-CSV wrapper against REAL export column names ──────
# Real Pepperstone List-of-Trades exports use "Price USD" (NOT "Price"); this
# fixture mirrors that shape so the wrapper is validated against the true
# column convention (NOTES.md #2 / module docstring's "needs a real-CSV
# sanity pass" caveat). Guards the 2026-07-02 Price->Price USD regression.

def _raw_trades(rows: list[tuple]) -> pd.DataFrame:
    """rows: (trade_num, type_str, date_and_time, price_usd, net_pnl_usd)."""
    return pd.DataFrame(
        rows,
        columns=["Trade #", "Type", "Date and time", "Price USD", "Net P&L USD"],
    )


def test_force_flat_csv_truncates_overnight_trade_using_price_usd_columns():
    """A trade held past 17:00 ET truncates at the boundary; the wrapper must
    read the real 'Price USD' column, not a nonexistent 'Price'. Intraday
    trades are left untouched."""
    raw = _raw_trades([
        # Trade 1: entry 01-05 09:00 @30000, exit NEXT day 01-06 12:00 @30100.
        # Crosses 01-05 17:00 (bar close 30050) -> pnl 1000 * 50/100 = 500.
        (1, "Entry long", "2026-01-05 09:00", 30_000.0, 1_000.0),
        (1, "Exit long",  "2026-01-06 12:00", 30_100.0, 1_000.0),
        # Trade 2: fully intraday 09:00 -> 16:00 same day -> untouched.
        (2, "Entry long", "2026-01-07 09:00", 30_000.0, 200.0),
        (2, "Exit long",  "2026-01-07 16:00", 30_040.0, 200.0),
    ])
    bars = pd.DataFrame({"time": [datetime(2026, 1, 5, 17, 0)], "close": [30_050.0]})

    out = force_flat_csv(raw, bars)

    t1_exit = out[(out["Trade #"] == 1) & out["Type"].str.startswith("Exit")].iloc[0]
    assert pd.to_datetime(t1_exit["Date and time"]) == datetime(2026, 1, 5, 17, 0)
    assert t1_exit["Net P&L USD"] == 500.0

    t2_exit = out[(out["Trade #"] == 2) & out["Type"].str.startswith("Exit")].iloc[0]
    assert t2_exit["Net P&L USD"] == 200.0  # intraday: unchanged
