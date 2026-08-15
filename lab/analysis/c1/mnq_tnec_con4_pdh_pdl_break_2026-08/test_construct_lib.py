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
    assert abs(dist - 2.0) < 1e-9


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


def test_first_long_pdh_break():
    # PDH=100.5 PDL=99.0; bar0 close above PDH; enter bar1 open
    open_ = np.array([100.0, 100.8, 101.0])
    high = np.array([100.4, 101.2, 101.5])
    low = np.array([99.5, 100.6, 100.7])
    close = np.array([100.6, 101.0, 101.2])
    trades = C.first_pdh_pdl_trade(open_, high, low, close, pdh=100.5, pdl=99.0)
    assert len(trades) == 1
    assert trades[0]["side"] == +1
    assert trades[0]["entry_i"] == 1


def test_first_only_ignores_later_break():
    open_ = np.array([100.0, 100.8, 99.0, 98.5])
    high = np.array([100.4, 101.2, 99.5, 99.0])
    low = np.array([99.5, 100.6, 98.0, 97.5])
    close = np.array([100.6, 101.0, 98.2, 98.0])  # later close below PDL
    trades = C.first_pdh_pdl_trade(open_, high, low, close, pdh=100.5, pdl=99.0)
    assert len(trades) == 1
    assert trades[0]["side"] == +1


def test_no_break_inside_range():
    open_ = np.full(5, 100.0)
    high = np.full(5, 100.2)
    low = np.full(5, 99.8)
    close = np.full(5, 100.0)
    assert C.first_pdh_pdl_trade(open_, high, low, close, pdh=101.0, pdl=99.0) == []


def test_explore_go_absent_by_default(tmp_path):
    assert C.explore_go_present(tmp_path) is False
    (tmp_path / "EXPLORE_GO.md").write_text("GO\n", encoding="utf-8")
    assert C.explore_go_present(tmp_path) is True
