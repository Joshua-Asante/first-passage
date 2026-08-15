"""Synthetic tests for Q-FEED-1 feed-divergence parsing and join math."""
from __future__ import annotations

import importlib.util
import io
import sys
from pathlib import Path

import pandas as pd
import pytest

_LIB_PATH = Path(__file__).resolve().parents[1] / "lab/archive/feed_divergence_2026-06/_lib.py"
_spec = importlib.util.spec_from_file_location("feed_div_lib", _LIB_PATH)
lib = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
sys.modules[_spec.name] = lib
_spec.loader.exec_module(lib)


def _tv_csv(rows: list[tuple]) -> str:
    """Build minimal List-of-Trades CSV with BAR EXPORT pipe signals."""
    buf = io.StringIO()
    buf.write("Trade number,Type,Date and time,Signal,Price USD\n")
    for trade_num, ts, epoch_ms, o, h, l, c, v in rows:
        sig = f"{epoch_ms}|{o}|{h}|{l}|{c}|{v}"
        buf.write(f"{trade_num},Entry long,{ts},{sig},{c}\n")
        buf.write(f"{trade_num},Exit long,{ts},{sig},{c}\n")
    return buf.getvalue()


def test_decode_bar_signal_pipe():
    enc = lib.decode_bar_signal("1772409600000|1.1|1.2|1.0|1.15|99")
    assert enc["o"] == pytest.approx(1.1)
    assert enc["c"] == pytest.approx(1.15)
    assert enc["epoch_ms"] == 1772409600000


def test_decode_bar_comment_legacy():
    enc = lib.decode_bar_comment("BAR|o=1.23456|h=1.24000|l=1.23000|c=1.23500|v=99")
    assert enc["o"] == pytest.approx(1.23456)
    assert enc["v"] == 99


def test_parse_tv_bar_export_cross_check(tmp_path):
    csv_text = _tv_csv([
        (1, "2026-03-03 12:00", 1772548800000, 1.10000, 1.10100, 1.09900, 1.10050, 100),
        (2, "2026-03-03 12:15", 1772549700000, 1.10050, 1.10150, 1.10000, 1.10100, 110),
    ])
    path = tmp_path / "GBPUSD_export.csv"
    path.write_text(csv_text, encoding="utf-8")
    bars = lib.parse_tv_bar_export(path, symbol="GBPUSD")
    assert len(bars) == 2
    assert bars.iloc[0]["close"] == pytest.approx(1.10050)


def test_parse_tv_bar_export_rejects_price_mismatch(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text(
        "Trade number,Type,Date and time,Signal,Price USD\n"
        "1,Entry long,2026-03-03 12:00,1772548800000|1.1|1.2|1.0|1.15|100,9.9\n"
        "1,Exit long,2026-03-03 12:15,1772549700000|1.1|1.2|1.0|1.15|100,1.15\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Cross-check fail"):
        lib.parse_tv_bar_export(path, symbol="GBPUSD")


def test_match_bars_and_coverage():
    duka = pd.DataFrame({
        "time": pd.to_datetime([
            "2026-03-03T12:00:00Z", "2026-03-03T12:15:00Z", "2026-03-03T12:30:00Z",
        ], utc=True),
        "open": [1.0, 1.1, 1.2],
        "high": [1.1, 1.2, 1.3],
        "low": [0.9, 1.0, 1.1],
        "close": [1.05, 1.15, 1.25],
        "volume": [1, 1, 1],
    })
    tv = pd.DataFrame({
        "tv_time": pd.to_datetime([
            "2026-03-03T12:00:00Z", "2026-03-03T12:15:00Z",
        ], utc=True),
        "open": [1.0, 1.1],
        "high": [1.1, 1.2],
        "low": [0.9, 1.0],
        "close": [1.04, 1.14],
        "volume": [1, 1],
    })
    matched, d_only, t_only = lib.match_bars(duka, tv, shift_minutes=0)
    assert len(matched) == 2
    assert len(d_only) == 1
    assert len(t_only) == 0
    cov = lib.coverage_ratio(matched, duka.assign(
        bar_open=duka["time"].dt.floor("15min"),
    ))
    assert cov == pytest.approx(2 / 3)


def test_idx_residual_basis_removal():
    matched = pd.DataFrame({
        "bar_open": pd.to_datetime([
            "2026-03-03T14:00:00Z", "2026-03-03T14:15:00Z",
            "2026-03-03T15:00:00Z", "2026-03-03T15:15:00Z",
        ], utc=True),
        "close_duka": [40100.0, 40110.0, 40120.0, 40130.0],
        "close_tv": [40000.0, 40010.0, 40020.0, 40030.0],
    })
    basis = lib.rolling_day_median_basis(matched)
    assert (basis == 100.0).all()
    atr = pd.Series(
        {t: 50.0 for t in matched["bar_open"]},
    )
    resid = lib.idx_residual_p95(matched, atr)
    assert resid == pytest.approx(0.0, abs=1e-9)


def test_load_thresholds_from_prereg():
    if not lib.PREREG_PATH.is_file():
        pytest.skip(
            "Q-FEED-1 prereg lives under docs/ltm/ (excluded from the public seed)"
        )
    thr = lib.load_thresholds()
    assert thr.fx_p95_accept == pytest.approx(0.10)
    assert thr.fx_p95_reject == pytest.approx(0.25)
    assert thr.fx_cov_accept == pytest.approx(0.99)
    assert thr.idx_residual_p95_reject == pytest.approx(0.40)


def test_shift_minus_15_inflates_p95_vs_shift_zero():
    """Regression: epoch_ms is bar-open; -15min shift misaligns by one bar."""
    duka = pd.DataFrame({
        "time": pd.to_datetime([
            "2026-03-03T12:00:00Z", "2026-03-03T12:15:00Z", "2026-03-03T12:30:00Z",
            "2026-03-03T12:45:00Z", "2026-03-03T13:00:00Z",
        ], utc=True),
        "open": [1.0, 1.1, 1.2, 1.3, 1.4],
        "high": [1.1, 1.2, 1.3, 1.4, 1.5],
        "low": [0.9, 1.0, 1.1, 1.2, 1.3],
        "close": [1.05, 1.15, 1.25, 1.35, 1.45],
        "volume": [1, 1, 1, 1, 1],
    })
    tv = pd.DataFrame({
        "tv_time": pd.to_datetime([
            "2026-03-03T12:00:00Z", "2026-03-03T12:15:00Z",
            "2026-03-03T12:30:00Z", "2026-03-03T12:45:00Z", "2026-03-03T13:00:00Z",
        ], utc=True),
        "open": [1.0, 1.1, 1.2, 1.3, 1.4],
        "high": [1.1, 1.2, 1.3, 1.4, 1.5],
        "low": [0.9, 1.0, 1.1, 1.2, 1.3],
        "close": [1.05, 1.15, 1.25, 1.35, 1.45],
        "volume": [1, 1, 1, 1, 1],
    })
    m0, _, _ = lib.match_bars(duka, tv, shift_minutes=0)
    m15, _, _ = lib.match_bars(duka, tv, shift_minutes=-15)
    atr = pd.Series({t: 0.1 for t in m0["bar_open"]})
    p0 = lib.p95_abs_delta_close_norm(m0, atr)
    p15 = lib.p95_abs_delta_close_norm(m15, atr)
    assert p0 == pytest.approx(0.0, abs=1e-9)
    assert p15 > 0.5


def test_weekend_boundary_exclusion():
    fri = pd.Timestamp("2026-03-06T21:00:00Z")
    sun = pd.Timestamp("2026-03-08T12:00:00Z")
    mon = pd.Timestamp("2026-03-09T12:00:00Z")
    assert lib.is_weekend_boundary(fri) is True
    assert lib.is_weekend_boundary(sun) is True
    assert lib.is_weekend_boundary(mon) is False
