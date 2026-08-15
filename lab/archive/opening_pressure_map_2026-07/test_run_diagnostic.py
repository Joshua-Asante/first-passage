from __future__ import annotations

from research_utils.camp_import import load_camp_sibling

import math

import numpy as np
import pandas as pd
import pytest

diagnostic = load_camp_sibling("run_diagnostic", __file__)


def _bars(days: int = 20) -> pd.DataFrame:
    rows = []
    for index, day in enumerate(pd.bdate_range("2023-01-02", periods=days)):
        base = 100.0 + index
        opening_close = base + (2.0 if index % 2 == 0 else 0.2)
        high = max(base, opening_close) + 0.5
        low = min(base, opening_close) - 0.5
        volume = 100 + index * 10
        rows.extend(
            [
                {
                    "time": pd.Timestamp(day, tz="America/New_York")
                    + pd.Timedelta(hours=9, minutes=30),
                    "open": base,
                    "high": high,
                    "low": low,
                    "close": (base + opening_close) / 2,
                    "volume": volume // 2,
                },
                {
                    "time": pd.Timestamp(day, tz="America/New_York")
                    + pd.Timedelta(hours=9, minutes=45),
                    "open": (base + opening_close) / 2,
                    "high": high,
                    "low": low,
                    "close": opening_close,
                    "volume": volume - volume // 2,
                },
                {
                    "time": pd.Timestamp(day, tz="America/New_York")
                    + pd.Timedelta(hours=15, minutes=45),
                    "open": opening_close,
                    "high": opening_close + 1,
                    "low": opening_close - 1,
                    "close": opening_close + (1.0 if index % 2 == 0 else -1.0),
                    "volume": 50,
                },
            ]
        )
    frame = pd.DataFrame(rows).set_index("time")
    frame["rth_date"] = frame.index.date
    frame["minute"] = frame.index.hour * 60 + frame.index.minute
    return frame


def test_daily_features_uses_shifted_volume_baseline_and_bounded_efficiency() -> None:
    features = diagnostic.daily_features(_bars())
    assert len(features) == 6
    assert features["efficiency"].between(0, 1).all()
    first = features.iloc[0]
    expected_baseline = np.median([100 + index * 10 for index in range(14)])
    assert first["relative_volume"] == pytest.approx(240 / expected_baseline)


def test_pressure_alignment_encodes_absorption_negative_and_efficiency_positive() -> None:
    features = diagnostic.daily_features(_bars())
    efficient = features.iloc[0]
    absorbed = features.iloc[1]
    assert efficient["pressure_alignment"] > 0
    assert absorbed["pressure_alignment"] < 0


def test_hac_slope_recovers_planted_positive_relationship() -> None:
    x = np.linspace(-1, 1, 200)
    frame = pd.DataFrame(
        {
            "pressure_alignment": x,
            "signed_followthrough_bp": 3.0 * x + np.sin(np.arange(200)) * 0.1,
        }
    )
    result = diagnostic.hac_slope(frame)
    assert result["slope_bp"] == pytest.approx(3.0, abs=0.02)
    assert result["hac_t"] > 2.0


def test_cost_conversion_uses_instrument_multiplier() -> None:
    mnq = diagnostic.round_trip_cost_bp(20_000, 2.0)
    mym = diagnostic.round_trip_cost_bp(40_000, 0.5)
    assert mnq == pytest.approx(0.705)
    assert mym == pytest.approx(1.41)


@pytest.mark.parametrize(
    ("passes", "expected"),
    [
        ({"MNQ": True, "MYM": True}, "RESOLVED"),
        ({"MNQ": True, "MYM": False}, "AMBIGUOUS"),
        ({"MNQ": False, "MYM": False}, "FALSIFIED"),
    ],
)
def test_overall_verdict_requires_cross_instrument_replication(
    passes: dict[str, bool],
    expected: str,
) -> None:
    results = {
        instrument: {"passes": passed}
        for instrument, passed in passes.items()
    }
    assert diagnostic.overall_verdict(results) == expected


def test_zero_variance_response_does_not_manufacture_infinite_t() -> None:
    frame = pd.DataFrame(
        {
            "pressure_alignment": np.linspace(-1, 1, 20),
            "signed_followthrough_bp": np.zeros(20),
        }
    )
    result = diagnostic.hac_slope(frame)
    assert result["slope_bp"] == pytest.approx(0.0)
    assert math.isnan(result["hac_t"])


def test_missing_vendor_input_returns_needs_context(
    tmp_path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    missing = tmp_path / "missing.csv"
    with pytest.raises(diagnostic.InputUnavailable, match="BAR EXPORT input missing"):
        diagnostic.load_panel(missing, "MNQ")
