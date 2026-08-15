"""Synthetic unit tests — no vendor bars. Run before explore GO."""
from __future__ import annotations

from research_utils.camp_import import load_camp_sibling

import numpy as np

C = load_camp_sibling("construct_lib", __file__)


def test_arithmetic_bars():
    b = C.arithmetic_bars()
    assert abs(b["em1_pred_pt"] - 5.41) < 1e-9
    assert abs(b["nedge_pred_pt"] - 1.41) < 1e-9


def test_path_stop_before_flat():
    o, h, l, c = 100.0, np.array([100.0, 99.0]), np.array([99.0, 89.0]), np.array([99.5, 90.0])
    pts, kind = C.path_pts_session_flat(o, +1, h, l, c, 0, stop_pt=10.0)
    assert kind == "stop"
    assert pts == -10.0


def test_path_session_flat_no_stop():
    o = 100.0
    h = np.array([101.0, 102.0, 103.0])
    l = np.array([99.0, 100.0, 101.0])
    c = np.array([100.5, 101.5, 102.5])
    pts, kind = C.path_pts_session_flat(o, +1, h, l, c, 0, stop_pt=10.0)
    assert kind == "flat"
    assert abs(pts - 2.5) < 1e-9


def test_break_side_with_break_long():
    # two narrow bars then close above quiet_hi
    high = np.array([10.0, 10.2, 10.1, 12.0, 12.5])
    low = np.array([9.8, 10.0, 9.9, 10.5, 11.0])
    close = np.array([9.9, 10.1, 10.0, 11.5, 12.0])  # brk at t-1=3 closes 11.5 > quiet_hi~10.2
    med = 1.0  # narrow bars have range 0.2
    # at t=4, compression is bars 1,2 (indices); brk is bar 3
    side = C.break_side_at_t(high, low, close, t=4, med_rng=med)
    assert side == +1


def test_break_side_no_compression():
    high = np.array([10.0, 15.0, 10.1, 12.0, 12.5])  # bar1 wide
    low = np.array([9.0, 9.0, 9.9, 10.5, 11.0])
    close = np.array([9.5, 14.0, 10.0, 11.5, 12.0])
    side = C.break_side_at_t(high, low, close, t=4, med_rng=1.0)
    assert side == 0


def test_simulate_em3_one_position():
    # synthetic session: force one long then ignore further
    n = 20
    open_ = np.full(n, 100.0)
    high = np.full(n, 100.3)
    low = np.full(n, 100.0)
    close = np.full(n, 100.15)
    # craft compression+break at t=5
    high[2], low[2], close[2] = 100.2, 100.0, 100.1
    high[3], low[3], close[3] = 100.2, 100.0, 100.1
    high[4], low[4], close[4] = 101.0, 100.0, 100.8  # break up
    open_[5] = 100.8
    trades = C.simulate_session_trades(open_, high, low, close, med_rng=1.0)
    assert len(trades) >= 1
    assert trades[0]["side"] == +1


def test_tnec_template_all_u():
    s = C.g0_freeze_verdict_template()
    assert s.startswith("U U U U U |")


def test_cheap_falsifier_record():
    r = C.cheap_falsifier_freeze_ok()
    assert r.verdict == "CHEAP_FALSIFIER_OK"
