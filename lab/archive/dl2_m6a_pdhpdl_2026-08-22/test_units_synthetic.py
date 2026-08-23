#!/usr/bin/env python3
"""DL-2 handoff Sec2 Step 2.1 per-step gate: unit-test (a)-(e) against small
hand-constructed synthetic slices before running the full 3.26M-row TRAIN
set. Plain-assert script (matches this lab's runnable-script convention,
not a pytest suite) -- run:

    PYTHONPATH=lab python lab/archive/dl2_m6a_pdhpdl_2026-08-22/test_units_synthetic.py

CI-ignored (validation-controls.yml): the campaign is ABANDONED and this
file's `test_*` names still get swept by a generic `pytest lab/`, but
importing its sibling `stitch.py` pulls in `databento` at module scope --
a research-stack-only package not in requirements-ops.lock. Run the command
above from `.venv-research` instead.
"""
from __future__ import annotations

import sys
from datetime import date

import numpy as np
import pandas as pd

from stitch import daily_volume_leader_from_minute, volume_lead_stitch, roll_days
from engine import (
    build_sessions, is_roll_session_map, trading_calendar, _lookback_reference,
    lookback_level, drift_sign, _trim_to_force_flat, _find_close_confirm_trigger,
    _close_confirm_fill, _retest_limit_fill, _resolve_trade, simulate_variant,
    TICK, DOLLAR_PER_POINT, RT_COST,
)
from variants import Variant, VARIANTS
from score import daily_pnl_series, net_annsr, cost_law_gate, cadence_per_week


def _bar(ts, o, h, l, c, symbol, volume=100):
    return {"ts_event": pd.Timestamp(ts, tz="UTC"), "open": o, "high": h, "low": l,
            "close": c, "symbol": symbol, "volume": volume}


def _mk_minute_df(rows):
    df = pd.DataFrame(rows)
    df = df.set_index("ts_event")
    return df


# ------------------------------------------------------------------ (c) variants
def test_c_variants():
    assert len(VARIANTS) == 10
    assert [v.v for v in VARIANTS] == list(range(1, 11))
    assert {v.lookback for v in VARIANTS} == {1, 2}
    assert {v.drift for v in VARIANTS} == {"unconditional", "aligned"}
    assert {v.entry_style for v in VARIANTS} == {"close_confirm", "retest_limit"}
    assert {v.target_r for v in VARIANTS} == {2.0, 3.0}
    print("PASS (c) 10 frozen variants, closed set, all axes present")


# ------------------------------------------------------------------ (b) roll-day / skip-back
def test_b_roll_day_and_skip_back():
    # Two symbols, leader flips on day 3 (AUX -> AUY).
    rows = []
    for day, (leader, other) in enumerate([
        ("AUX", "AUY"), ("AUX", "AUY"), ("AUY", "AUX"), ("AUY", "AUX"), ("AUY", "AUX"),
    ]):
        d = f"2020-01-0{day+1}"
        rows.append(_bar(f"{d}T10:00", 1.0, 1.0, 1.0, 1.0, leader, volume=1000))
        rows.append(_bar(f"{d}T10:00", 1.0, 1.0, 1.0, 1.0, other, volume=10))
    minute = _mk_minute_df(rows)

    leader_series = daily_volume_leader_from_minute(minute)
    expected_leader = {
        date(2020, 1, 1): "AUX", date(2020, 1, 2): "AUX", date(2020, 1, 3): "AUY",
        date(2020, 1, 4): "AUY", date(2020, 1, 5): "AUY",
    }
    assert dict(leader_series.items()) == expected_leader, leader_series

    stitched, by_day = volume_lead_stitch(minute)
    assert len(stitched) == 5  # one leader-bar per day
    rolls = roll_days(by_day)
    assert rolls == {date(2020, 1, 3)}, rolls  # leader changed AUX->AUY on day 3; day 1 never a roll (no prior)
    print("PASS (b.1) roll-day detection: leader flip on day 3 correctly identified, day 1 not a roll")

    # skip-back: nonroll dates = everything except day 3.
    all_dates = sorted(expected_leader)
    nonroll = [d for d in all_dates if d not in rolls]
    assert nonroll == [date(2020, 1, 1), date(2020, 1, 2), date(2020, 1, 4), date(2020, 1, 5)]
    # lookback=1 for day 4 (2020-01-04): the immediately-prior NON-roll session is day 2
    # (2020-01-02), NOT day 3 (the roll day) -- Sec1's skip-back rule.
    ref = _lookback_reference(nonroll, date(2020, 1, 4), 1)
    assert ref == [date(2020, 1, 2)], ref
    # lookback=2 for day 4: the two most recent non-roll sessions before it, oldest first.
    ref2 = _lookback_reference(nonroll, date(2020, 1, 4), 2)
    assert ref2 == [date(2020, 1, 1), date(2020, 1, 2)], ref2
    print("PASS (b.2) skip-back lookback: day 4's 1-session reference correctly skips the day-3 roll session")


# ------------------------------------------------------------------ (a) session boundary
def test_a_session_boundary():
    # Session labeled 2020-01-02 runs 18:00 ET 2020-01-01 -> 17:00 ET 2020-01-02.
    # ET = UTC-5 in early January (EST, no DST). 18:00 ET = 23:00 UTC.
    rows = [
        _bar("2020-01-01T22:00", 1.0, 1.0, 1.0, 1.0, "6AF0"),   # 17:00 ET Jan1 -> session 2020-01-01
        _bar("2020-01-01T23:00", 2.0, 2.5, 1.9, 2.4, "6AF0"),   # 18:00 ET Jan1 -> session 2020-01-02 (start)
        _bar("2020-01-02T15:00", 2.4, 3.0, 2.3, 2.9, "6AF0"),   # 10:00 ET Jan2 -> session 2020-01-02
        _bar("2020-01-02T21:55", 2.9, 3.1, 2.8, 3.0, "6AF0"),   # 16:55 ET Jan2 -> session 2020-01-02 (force-flat bar)
        _bar("2020-01-02T22:00", 3.0, 3.0, 3.0, 3.0, "6AF0"),   # 17:00 ET Jan2 -> session 2020-01-02 (boundary itself)
        _bar("2020-01-02T23:00", 4.0, 4.0, 4.0, 4.0, "6AF0"),   # 18:00 ET Jan2 -> session 2020-01-03 (next)
    ]
    stitched = _mk_minute_df(rows)
    sessions = build_sessions(stitched)

    assert date(2020, 1, 2) in sessions
    ss = sessions[date(2020, 1, 2)]
    assert len(ss.c) == 4  # the 23:00 Jan1 .. 22:00 Jan2 bars (4), NOT the 22:00 Jan1 bar or the 23:00 Jan2 bar
    assert ss.open_ == 2.0
    assert ss.close_ == 3.0
    assert ss.high == 3.1
    assert ss.low == 1.9

    assert date(2020, 1, 1) in sessions
    assert len(sessions[date(2020, 1, 1)].c) == 1

    o, h, l, c = _trim_to_force_flat(ss)
    assert len(c) == 3  # drops the 17:00 ET (22:00 UTC) boundary bar, keeps up to 16:55 ET
    assert c[-1] == 3.0  # the 16:55 ET bar's own close
    print("PASS (a) session-boundary grouping: 18:00 ET->17:00 ET labeling and force-flat trim both correct")


# ------------------------------------------------------------------ (d) fill engine
def test_d_fill_engine_breakout_and_hold():
    # Hand-constructed break-and-hold: level_high=1.0000, level_low=0.9900.
    # Bar 0: close breaks above level_high (1.0050) -> close-confirm trigger, long.
    # Bar 1 (next): open = 1.0055 (gaps through level_high+TICK=1.0001) -> fill at open (worse).
    #   entry=1.0055, stop=level_low=0.9900, risk=0.0155, target(2R)=1.0055+2*0.0155=1.0365
    # Bar 1 also has high/low that do NOT touch stop or target (hold).
    # Bar 2: high clears target with margin (avoids a float-equality boundary
    # in the test itself) -> target exit.
    c = np.array([1.0050, 1.0060, 1.0100])
    o = np.array([1.0040, 1.0055, 1.0100])
    h = np.array([1.0055, 1.0070, 1.0400])
    l = np.array([1.0030, 1.0050, 1.0090])
    level_high, level_low = 1.0000, 0.9900

    trig = _find_close_confirm_trigger(c, level_high, level_low, {"long", "short"})
    assert trig == (0, "long"), trig

    fill = _close_confirm_fill(o, 0, "long", level_high, level_low)
    assert fill is not None
    entry_idx, entry_price = fill
    assert entry_idx == 1
    assert abs(entry_price - 1.0055) < 1e-12, entry_price  # open (1.0055) > level_high+TICK (1.0001) -> use open

    stop_price = level_low
    risk = entry_price - stop_price
    target_price = entry_price + 2.0 * risk
    assert abs(risk - 0.0155) < 1e-9
    assert abs(target_price - 1.0365) < 1e-9

    exit_price, reason = _resolve_trade(h, l, c, entry_idx, "long", stop_price, target_price, extra_slip_ticks=0)
    assert reason == "target", (exit_price, reason)
    assert abs(exit_price - target_price) < 1e-12
    print("PASS (d.1) close-confirm break-and-hold: entry/stop/target/exit all match hand-worked R geometry")


def test_d_adverse_first_same_bar():
    # A single bar touches BOTH stop and target -> adverse-first means the stop wins.
    h = np.array([2.0])
    l = np.array([0.0])
    c = np.array([1.0])
    exit_price, reason = _resolve_trade(h, l, c, 0, "long", stop_price=0.5, target_price=1.5, extra_slip_ticks=0)
    assert reason == "stop", reason
    assert abs(exit_price - (0.5 - TICK)) < 1e-12, exit_price
    print("PASS (d.2) adverse-first same-bar resolution: stop wins a same-bar double-touch")


def test_d_extra_slip_gate():
    # +1 tick/side (M-16): stop exit slip doubles (1+1 ticks).
    h = np.array([2.0])
    l = np.array([0.0])
    c = np.array([1.0])
    exit_price, reason = _resolve_trade(h, l, c, 0, "long", stop_price=0.5, target_price=1.5, extra_slip_ticks=1)
    assert reason == "stop"
    assert abs(exit_price - (0.5 - 2 * TICK)) < 1e-12, exit_price
    print("PASS (d.3) M-16 extra-slip gate: stop exit slip scales with extra_slip_ticks")


def test_d_retest_limit_exact_fill_and_i3():
    # Confirm bar at index 0 (close breaks above level_high). Retest must NOT
    # fill on bar 0 itself even if its own low already sits at/below level_high
    # (I3: strictly-after discipline) -- it fills on the first bar STRICTLY
    # AFTER the confirm bar that touches the level.
    level_high, level_low = 1.0000, 0.9900
    h = np.array([1.0050, 1.0010, 1.0005])
    l = np.array([0.9990, 1.0010, 0.9995])  # bar0's low (0.9990) is below level_high but must not count
    fill = _retest_limit_fill(h, l, 0, "long", level_high, level_low)
    assert fill == (2, 1.0000), fill  # bar1 doesn't touch (low=1.0010 > level_high), bar2 does (low=0.9995<=1.0000)
    print("PASS (d.4) retest-limit: strictly-after confirm bar, exact-at-level fill (no tick buffer)")


def test_d_no_next_bar_no_entry():
    # Close-confirm trigger on the LAST bar of the trimmed session -> no next
    # bar to fill on -> no entry.
    o = np.array([1.0, 1.0])
    fill = _close_confirm_fill(o, 1, "long", 1.0000, 0.9900)
    assert fill is None
    print("PASS (d.5) close-confirm with no next bar in session correctly yields no entry")


# ------------------------------------------------------------------ (e) cost pin + annSR
def test_e_daily_pnl_and_annsr():
    from engine import Trade
    trades = [
        Trade(date(2020, 1, 1), 1, "long", "close_confirm", 1.0, 1.1, "target", 0.05, 500.0, 1000.0, 1000.0 - RT_COST),
        Trade(date(2020, 1, 3), 1, "long", "close_confirm", 1.0, 0.95, "stop", 0.05, 500.0, -500.0, -500.0 - RT_COST),
    ]
    trading_dates = [date(2020, 1, 1), date(2020, 1, 2), date(2020, 1, 3)]
    daily = daily_pnl_series(trades, trading_dates)
    assert len(daily) == 3
    assert daily.iloc[0] == 1000.0 - RT_COST
    assert daily.iloc[1] == 0.0  # flat day included as zero
    assert daily.iloc[2] == -500.0 - RT_COST

    manual_sr = float(daily.mean() / daily.std(ddof=1) * np.sqrt(252))
    assert abs(net_annsr(daily) - manual_sr) < 1e-9

    cl = cost_law_gate(trades)
    assert abs(cl["median_stop_ticks"] - 500.0) < 1e-9
    expected_ratio = 0.40 * 500.0 * 1.0 / RT_COST
    assert abs(cl["ratio"] - expected_ratio) < 1e-9
    assert cl["passed"] == (expected_ratio >= 4.0)

    cad = cadence_per_week(len(trades), trading_dates)
    assert abs(cad - 2 / (3 / 7.0)) < 1e-9
    print("PASS (e) daily P&L bucketing (flat days=0), net annSR, cost-law ratio, and cadence all match hand calc")


def test_full_simulate_variant_smoke():
    """Wire (a)-(e) together on a tiny synthetic multi-session panel: a
    clean 1-session-lookback long breakout that holds to target, verifying
    simulate_variant end-to-end (not just the unit pieces)."""
    rows = []
    # Session 2020-01-06 (Mon): reference session, high=1.0000 low=0.9900, open=0.9950 close=0.9960 (flat-ish).
    rows += [
        _bar("2020-01-05T23:00", 0.9950, 0.9960, 0.9940, 0.9950, "6AF0"),
        _bar("2020-01-06T10:00", 0.9950, 1.0000, 0.9900, 0.9960, "6AF0"),
    ]
    # Session 2020-01-07 (Tue): close-confirm breakout above 1.0000, holds to 2R target.
    rows += [
        _bar("2020-01-06T23:00", 0.9960, 1.0050, 0.9960, 1.0050, "6AF0"),  # confirm bar: close 1.0050 > 1.0000
        _bar("2020-01-07T00:00", 1.0055, 1.0055, 1.0055, 1.0055, "6AF0"),  # entry bar: open 1.0055 (gaps through)
        _bar("2020-01-07T10:00", 1.0300, 1.0400, 1.0300, 1.0365, "6AF0"),  # target bar: high 1.0400 >= target 1.0365
    ]
    minute = _mk_minute_df(rows)
    stitched, by_day = volume_lead_stitch(minute)
    rolls = roll_days(by_day)
    assert rolls == set()  # single symbol throughout -- no roll

    sessions = build_sessions(stitched)
    is_roll = is_roll_session_map(sessions, rolls)
    session_dates = trading_calendar(sessions)
    nonroll = [d for d in session_dates if not is_roll[d]]

    v = Variant(v=99, lookback=1, drift="unconditional", entry_style="close_confirm", target_r=2.0)
    trades = simulate_variant(sessions, session_dates, nonroll, is_roll, v)
    assert len(trades) == 1, trades
    t = trades[0]
    assert t.session_date == date(2020, 1, 7)
    assert t.direction == "long"
    assert t.exit_reason == "target"
    assert abs(t.entry_price - 1.0055) < 1e-9
    assert abs(t.risk_price - (1.0055 - 0.9900)) < 1e-9
    print("PASS (full) end-to-end synthetic break-and-hold reproduces the hand-worked trade exactly")


def main() -> int:
    test_c_variants()
    test_b_roll_day_and_skip_back()
    test_a_session_boundary()
    test_d_fill_engine_breakout_and_hold()
    test_d_adverse_first_same_bar()
    test_d_extra_slip_gate()
    test_d_retest_limit_exact_fill_and_i3()
    test_d_no_next_bar_no_entry()
    test_e_daily_pnl_and_annsr()
    test_full_simulate_variant_smoke()
    print("\nALL UNIT GATES PASS (a)-(e)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
