"""Self-tests for the fixing-reversal cost pre-screen (2026-06-22).

Run from this directory:  python -m pytest test_fixrev_costscreen.py -q

Pure-synthetic — no vendor data needed. Validates the load-bearing primitives:
DST-aware London-fix resolution, the cost-law identity (cost/R = round-trip
cost / stop), the break-even spread, the fade-trade P&L (recovers an injected
post-fix recovery, and a stop-out = -1R), the post-fix reversal magnitude, the
BAR_EXPORT loader (dedupe-on-overlap + entry-price cross-check), and the
graceful skips (missing fix bar, absent input files).
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fixrev_costscreen as F  # noqa: E402


# ── helpers ──────────────────────────────────────────────────────────────────
def _bars(start_utc, closes, *, highs=None, lows=None, opens=None, vol=100, step_min=5):
    """Build a tz-aware-UTC OHLCV frame from a list of closes (5m steps by default)."""
    n = len(closes)
    t0 = pd.Timestamp(start_utc, tz="UTC")
    times = [t0 + pd.Timedelta(minutes=step_min * i) for i in range(n)]
    closes = np.asarray(closes, float)
    opens = np.asarray(opens, float) if opens is not None else closes.copy()
    highs = np.asarray(highs, float) if highs is not None else np.maximum(opens, closes)
    lows = np.asarray(lows, float) if lows is not None else np.minimum(opens, closes)
    return pd.DataFrame(
        {"time": times, "open": opens, "high": highs, "low": lows,
         "close": closes, "volume": vol}
    )


def _write_bar_export(path: Path, bars: pd.DataFrame, *, price_col="Price USD"):
    """Write a minimal BAR_EXPORT v0.1 List-of-Trades CSV (Entry rows only)."""
    cols = ["Trade number", "Type", "Date and time", "Signal", price_col]
    lines = [",".join(cols)]
    for i, row in enumerate(bars.itertuples(index=False), start=1):
        epoch_ms = int(pd.Timestamp(row.time).value // 1_000_000)
        sig = f"{epoch_ms}|{row.open}|{row.high}|{row.low}|{row.close}|{int(row.volume)}"
        disp = pd.Timestamp(row.time).strftime("%Y-%m-%d %H:%M")
        lines.append(f"{i},Entry long,{disp},{sig},{row.close}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ── DST-aware London 16:00 fix → UTC ─────────────────────────────────────────
def test_london_fix_utc_winter_is_1600_utc():
    assert F.london_fix_utc(dt.date(2021, 1, 15)) == pd.Timestamp("2021-01-15 16:00", tz="UTC")


def test_london_fix_utc_summer_is_1500_utc():
    # 16:00 London in BST is 15:00 UTC — the DST trap this resolution guards against
    assert F.london_fix_utc(dt.date(2021, 7, 15)) == pd.Timestamp("2021-07-15 15:00", tz="UTC")


# ── cost-law identity + break-even spread ────────────────────────────────────
def test_cost_law_identity_cost_R_equals_roundtrip_cost_over_stop():
    bars = _bars("2021-01-15 16:00", [1.2000, 1.2000, 1.2000])  # flat → gross 0
    tr = F.simulate_fade(bars, 0, hold_bars=2, stop_pips=10.0,
                         spread_pips=1.0, commission_pips=0.4)
    assert tr["cost_R"] == pytest.approx((1.0 + 0.4) / 10.0)
    assert tr["gross_R"] == pytest.approx(0.0, abs=1e-9)
    assert tr["net_R"] == pytest.approx(-(1.4 / 10.0))


def test_breakeven_spread_formula():
    # mean_net = mean_gross - (spread+comm)/stop = 0  →  spread = mean_gross*stop - comm
    assert F.breakeven_spread_pips(0.5, 10.0, 0.0) == pytest.approx(5.0)
    assert F.breakeven_spread_pips(0.5, 10.0, 1.0) == pytest.approx(4.0)


# ── fade-trade P&L (the cost-law unit) ───────────────────────────────────────
def test_simulate_fade_recovers_injected_post_fix_up_move():
    bars = _bars("2021-01-15 16:00", [1.2000, 1.2005, 1.2010],
                 highs=[1.2000, 1.2006, 1.2011], lows=[1.2000, 1.2004, 1.2009])
    tr = F.simulate_fade(bars, 0, hold_bars=2, stop_pips=10.0,
                         spread_pips=0.0, commission_pips=0.0, side=+1)
    assert tr["exit_reason"] == "time"
    assert tr["gross_R"] == pytest.approx(1.0)  # +10 pips on a 10-pip stop


def test_simulate_fade_stop_out_is_minus_one_R():
    bars = _bars("2021-01-15 16:00", [1.2000, 1.1988, 1.2010],
                 highs=[1.2000, 1.2000, 1.2011], lows=[1.2000, 1.1988, 1.1988])
    tr = F.simulate_fade(bars, 0, hold_bars=2, stop_pips=10.0,
                         spread_pips=0.0, commission_pips=0.0, side=+1)
    assert tr["exit_reason"] == "stop"
    assert tr["gross_R"] == pytest.approx(-1.0)


# ── post-fix reversal magnitude (paper bps frame) ────────────────────────────
def test_fix_window_return_bps_measures_post_fix_move():
    bars = _bars("2021-01-15 16:00", [1.2000, 1.2003, 1.2006])
    bps = F.fix_window_return_bps(bars, 0, post_bars=2)
    assert bps == pytest.approx((1.2006 - 1.2000) / 1.2000 * 1e4)


# ── BAR_EXPORT loader (reuses core decode_bar_signal) ────────────────────────
def test_decode_bars_dedupes_overlap_keep_last(tmp_path):
    b1 = _bars("2021-01-15 15:55", [1.2000, 1.2001])           # 15:55, 16:00
    b2 = _bars("2021-01-15 16:00", [1.2099, 1.2002])           # 16:00 (overlap), 16:05
    p1, p2 = tmp_path / "p1.csv", tmp_path / "p2.csv"
    _write_bar_export(p1, b1)
    _write_bar_export(p2, b2)
    df = F.decode_bars([p1, p2])
    assert len(df) == 3                                         # overlap collapsed
    row = df[df["time"] == pd.Timestamp("2021-01-15 16:00", tz="UTC")].iloc[0]
    assert row["close"] == pytest.approx(1.2099)               # keep='last' (p2 wins)
    assert list(df["time"]) == sorted(df["time"])              # sorted


def test_decode_bars_crosscheck_fails_on_price_mismatch(tmp_path):
    p = tmp_path / "bad.csv"
    epoch = int(pd.Timestamp("2021-01-15 16:00", tz="UTC").value // 1_000_000)
    sig = f"{epoch}|1.2000|1.2000|1.2000|1.2000|100"
    p.write_text(
        "Trade number,Type,Date and time,Signal,Price USD\n"
        f"1,Entry long,2021-01-15 16:00,{sig},1.5000\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        F.decode_bars([p])


# ── graceful skips ───────────────────────────────────────────────────────────
def test_fix_bar_index_missing_returns_none():
    bars = _bars("2021-01-15 15:00", [1.2, 1.2, 1.2])           # no 16:00 bar
    assert F.fix_bar_index(bars, pd.Timestamp("2021-01-15 16:00", tz="UTC")) is None


def test_run_screen_counts_only_valid_fix_days():
    day1 = _bars("2021-01-15 16:00", [1.2000, 1.2005, 1.2010],
                 highs=[1.2000, 1.2006, 1.2011], lows=[1.2000, 1.2004, 1.2009])
    day2 = _bars("2021-01-18 10:00", [1.2, 1.2, 1.2])           # no fix bar that day
    bars = pd.concat([day1, day2], ignore_index=True)
    summary = F.run_screen(bars, hold_grid_bars=[2], stop_grid_pips=[10.0],
                           spread_grid_pips=[0.0], commission_pips=0.0)
    assert summary["cells"][0]["n_trades"] == 1
    assert summary["n_skipped_days"] == 1


def test_find_input_csvs_skips_when_absent(tmp_path):
    assert F.find_input_csvs(tmp_path, pattern="BAR_EXPORT_*_EURUSD_*.csv") == []


# ── verdict classification (the load-bearing conclusion) ─────────────────────
def test_classify_verdict_insufficient_below_floor():
    assert F.classify_verdict(best_breakeven_pips=99.0, fxify_spread_pips=0.5,
                              n_trades=10, n_floor=100) == "INSUFFICIENT-DATA"


def test_classify_verdict_fail_when_breakeven_below_fxify_spread():
    # break-even spread under FXIFY's realistic spread → cost eats it (the paper's prediction)
    assert F.classify_verdict(best_breakeven_pips=0.3, fxify_spread_pips=0.6,
                              n_trades=1500, n_floor=100) == "FAIL-COST"


def test_classify_verdict_pass_provisional_when_breakeven_above_fxify_spread():
    assert F.classify_verdict(best_breakeven_pips=1.2, fxify_spread_pips=0.6,
                              n_trades=1500, n_floor=100) == "PASS-PROVISIONAL"
