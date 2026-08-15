import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent
                       / "lab" / "analysis" / "legacy" / "futures_conversion_2026-07-01"))
import roll_mask as rm


def _bars(rows):
    # rows: list of (iso_time, open, close)
    return pd.DataFrame(rows, columns=["time", "open", "close"])


def test_flags_large_gap_in_quarterly_window():
    bars = _bars([
        ("2024-03-11T20:00:00Z", 100.0, 100.0),
        ("2024-03-12T14:30:00Z", 101.5, 101.5),  # +1.5% gap, Mar 12 = quarterly window
    ])
    out = rm.flag_roll_seams(bars, symbol="NQ", threshold_pct=0.5)
    assert bool(out["roll_seam"].iloc[1]) is True


def test_ignores_large_gap_outside_roll_window():
    bars = _bars([
        ("2024-05-10T20:00:00Z", 100.0, 100.0),
        ("2024-05-13T14:30:00Z", 101.5, 101.5),  # +1.5% but May = not a roll month
    ])
    out = rm.flag_roll_seams(bars, symbol="NQ", threshold_pct=0.5)
    assert bool(out["roll_seam"].iloc[1]) is False


def test_ignores_small_gap_in_window():
    bars = _bars([
        ("2024-03-11T20:00:00Z", 100.0, 100.0),
        ("2024-03-12T14:30:00Z", 100.1, 100.1),  # +0.1% < threshold
    ])
    out = rm.flag_roll_seams(bars, symbol="NQ", threshold_pct=0.5)
    assert bool(out["roll_seam"].iloc[1]) is False


def test_bimonthly_gold_window_end_of_odd_month():
    bars = _bars([
        ("2024-01-27T20:00:00Z", 2000.0, 2000.0),
        ("2024-01-28T14:30:00Z", 2030.0, 2030.0),  # +1.5%, Jan 28 = gold roll window
    ])
    out = rm.flag_roll_seams(bars, symbol="QO", threshold_pct=0.5)
    assert bool(out["roll_seam"].iloc[1]) is True


def test_quarterly_symbol_ignores_gold_window():
    bars = _bars([
        ("2024-01-27T20:00:00Z", 100.0, 100.0),
        ("2024-01-28T14:30:00Z", 101.5, 101.5),  # gold window, but NQ is quarterly
    ])
    out = rm.flag_roll_seams(bars, symbol="NQ", threshold_pct=0.5)
    assert bool(out["roll_seam"].iloc[1]) is False


def test_unknown_symbol_raises():
    bars = _bars([("2024-03-12T14:30:00Z", 100.0, 100.0)])
    with pytest.raises(KeyError):
        rm.flag_roll_seams(bars, symbol="ES", threshold_pct=0.5)


def test_roll_seam_dates_returns_sorted_unique():
    bars = _bars([
        ("2024-03-11T20:00:00Z", 100.0, 100.0),
        ("2024-03-12T14:30:00Z", 101.5, 101.5),
        ("2024-06-12T14:30:00Z", 103.0, 103.0),  # +1.5% Jun window
    ])
    dates = rm.roll_seam_dates(bars, symbol="NQ", threshold_pct=0.5)
    assert [d.isoformat() for d in dates] == ["2024-03-12", "2024-06-12"]
