"""Synthetic unit tests — no vendor bars. Run before explore GO."""
from __future__ import annotations

from research_utils.camp_import import load_camp_sibling

import numpy as np

C = load_camp_sibling("construct_lib", __file__)


def test_tnec_template_all_u():
    s = C.g0_freeze_verdict_template()
    assert s.startswith("U U U U U |")


def test_cheap_falsifier_record():
    r = C.cheap_falsifier_freeze_ok()
    assert r.verdict == "CHEAP_FALSIFIER_OK"


def test_settle_long_with_midline():
    # narrow bars at 0,1; break bar 2 closes above quiet_hi and midline
    high = np.array([10.2, 10.2, 12.0, 12.5])
    low = np.array([10.0, 10.0, 10.5, 11.0])
    close = np.array([10.1, 10.1, 11.8, 12.0])
    side, q_hi, q_lo = C.settle_side_at_t(high, low, close, t=2, med_rng=1.0)
    assert side == +1
    assert q_hi == 10.2
    assert q_lo == 10.0


def test_settle_rejects_without_midline():
    # close beyond quiet_hi but NOT above midline (mid=10.1, close=10.15 — wait need beyond hi)
    # quiet 10.0-10.2 mid=10.1; close must be >10.2 AND >10.1. If close=10.15 it's not beyond hi.
    # Dual: close below quiet_lo but above mid would fail dn clause.
    high = np.array([10.2, 10.2, 10.25, 10.3])
    low = np.array([10.0, 10.0, 9.5, 9.8])
    close = np.array([10.1, 10.1, 10.05, 10.0])  # close 10.05 is between lo/hi — no break
    side, _, _ = C.settle_side_at_t(high, low, close, t=2, med_rng=1.0)
    assert side == 0


def test_path_structural_stop():
    entry = 100.0
    stop = 98.0  # long stop below
    high = np.array([101.0, 100.5])
    low = np.array([99.0, 97.5])
    close = np.array([100.5, 98.0])
    pts, kind, dist = C.path_pts_structural(entry, +1, stop, high, low, close, 0)
    assert kind == "stop"
    assert abs(pts - (-2.0)) < 1e-9
    assert abs(dist - 2.0) < 1e-9


def test_path_session_flat():
    entry = 100.0
    stop = 90.0
    high = np.array([101.0, 103.0])
    low = np.array([99.0, 100.0])
    close = np.array([100.5, 102.0])
    pts, kind, dist = C.path_pts_structural(entry, +1, stop, high, low, close, 0)
    assert kind == "flat"
    assert abs(pts - 2.0) < 1e-9


def test_simulate_first_only():
    n = 12
    open_ = np.full(n, 100.0)
    high = np.full(n, 100.3)
    low = np.full(n, 100.0)
    close = np.full(n, 100.15)
    # compression bars 2,3 then break at 4
    high[2], low[2], close[2] = 100.2, 100.0, 100.1
    high[3], low[3], close[3] = 100.2, 100.0, 100.1
    high[4], low[4], close[4] = 101.0, 100.0, 100.8
    open_[5] = 100.8
    # second potential break later — must be ignored (first only)
    high[7], low[7], close[7] = 100.2, 100.0, 100.1
    high[8], low[8], close[8] = 100.2, 100.0, 100.1
    high[9], low[9], close[9] = 102.0, 100.5, 101.5
    open_[10] = 101.5
    trades = C.simulate_session_trades(open_, high, low, close, med_rng=1.0)
    assert len(trades) == 1
    assert trades[0]["side"] == +1
    assert trades[0]["entry_i"] == 5


def test_explore_go_absent_by_default(tmp_path):
    assert C.explore_go_present(tmp_path) is False
    (tmp_path / "EXPLORE_GO.md").write_text("GO\n", encoding="utf-8")
    assert C.explore_go_present(tmp_path) is True
