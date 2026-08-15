"""Synthetic unit tests — no vendor bars. Run before explore GO."""
from __future__ import annotations

from research_utils.camp_import import load_camp_sibling

import numpy as np

C = load_camp_sibling("construct_lib", __file__)


def test_tnec_template_all_u():
    assert C.g0_freeze_verdict_template().startswith("U U U U U |")


def test_cheap_falsifier_record():
    assert C.cheap_falsifier_freeze_ok().verdict == "CHEAP_FALSIFIER_OK"


def test_path_structural_stop():
    pts, kind, dist = C.path_pts_structural(
        100.0, +1, 98.0,
        np.array([101.0, 100.5]),
        np.array([99.0, 97.5]),
        np.array([100.5, 98.0]),
        0,
    )
    assert kind == "stop"
    assert abs(pts - (-2.0)) < 1e-9


def test_path_session_flat():
    pts, kind, dist = C.path_pts_structural(
        100.0, +1, 90.0,
        np.array([101.0, 103.0]),
        np.array([99.0, 100.0]),
        np.array([100.5, 102.0]),
        0,
    )
    assert kind == "flat"
    assert abs(pts - 2.0) < 1e-9


def _session_arrays(*, bias_up: bool):
    """30 bias bars + a few search bars with minute stamps."""
    n_bias = 30
    # Bias window minutes 09:30 .. 09:59
    minutes = list(range(C.RTH_OPEN_MIN, C.BIAS_END_MIN))
    assert len(minutes) == n_bias
    # After 10:00: cleared above VWAP, then tag+reclaim
    minutes += [C.BIAS_END_MIN, C.BIAS_END_MIN + 1, C.BIAS_END_MIN + 2]
    n = len(minutes)
    open_ = np.full(n, 100.0)
    high = np.full(n, 100.5)
    low = np.full(n, 99.5)
    close = np.full(n, 100.2 if bias_up else 99.8)
    volume = np.full(n, 10.0)
    # Force open@09:30 and close@09:59 for bias
    open_[0] = 100.0
    close[n_bias - 1] = 101.0 if bias_up else 99.0
    # Search bars: establish above VWAP, then wick-tag reclaim
    # After bias, set prices well above then touch VWAP with close reclaim
    i0 = n_bias  # first search bar — close above
    open_[i0] = 101.0
    high[i0] = 101.5
    low[i0] = 100.8
    close[i0] = 101.2
    volume[i0] = 10.0
    i1 = n_bias + 1  # tag+reclaim
    open_[i1] = 101.0
    high[i1] = 101.2
    # VWAP will be ~100-ish; put low below and close above for long
    low[i1] = 99.0
    close[i1] = 101.0
    volume[i1] = 10.0
    # entry bar
    i2 = n_bias + 2
    open_[i2] = 101.1
    high[i2] = 101.5
    low[i2] = 100.5
    close[i2] = 101.3
    volume[i2] = 10.0
    return (
        open_,
        high,
        low,
        close,
        volume,
        np.asarray(minutes, dtype=int),
    )


def test_first_long_reclaim():
    o, h, lo, c, v, m = _session_arrays(bias_up=True)
    trades = C.first_pullback_reclaim_trade(o, h, lo, c, v, m)
    assert len(trades) == 1
    assert trades[0]["side"] == +1
    assert trades[0]["entry_i"] == 32  # bar after reclaim at index 31


def test_flat_bias_skips():
    o, h, lo, c, v, m = _session_arrays(bias_up=True)
    c[29] = o[0]  # flat bias
    assert C.first_pullback_reclaim_trade(o, h, lo, c, v, m) == []


def test_explore_go_absent_by_default(tmp_path):
    assert C.explore_go_present(tmp_path) is False
    (tmp_path / "EXPLORE_GO.md").write_text("GO\n", encoding="utf-8")
    assert C.explore_go_present(tmp_path) is True
