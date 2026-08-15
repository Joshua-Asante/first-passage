"""Synthetic unit tests — no vendor bars. Run before explore GO."""
from __future__ import annotations

from research_utils.camp_import import load_camp_sibling

from pathlib import Path

import numpy as np

C = load_camp_sibling("construct_lib", __file__)


def _session_minutes_overnight_rth() -> np.ndarray:
    """15m bars: overnight 18:00–23:45 + 00:00–09:15 + RTH probe 09:30–11:00."""
    evening = np.arange(C.OVERNIGHT_OPEN_MIN, 24 * 60, 15)
    morning = np.arange(0, C.OVERNIGHT_CLOSE_MIN + 1, 15)
    probe = np.arange(C.PROBE_OPEN_MIN, C.PROBE_OPEN_MIN + 15 * 12, 15)
    return np.concatenate([evening, morning, probe]).astype(int)


def _base_prices(n: int, mid: float = 1900.0) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    o = np.full(n, mid, dtype=float)
    h = np.full(n, mid + 2.0, dtype=float)
    lo = np.full(n, mid - 2.0, dtype=float)
    c = np.full(n, mid, dtype=float)
    return o, h, lo, c


def test_explore_go_present(tmp_path: Path):
    assert C.explore_go_present(tmp_path) is False
    (tmp_path / "EXPLORE_GO.md").write_text("ISSUED 2026-08-13\n", encoding="utf-8")
    assert C.explore_go_present(tmp_path) is True


def test_r_from_pts_matches_usd_formula():
    # 32 pt stop, +32 pt win → pnl $160, stop $160, R = (160-2.82)/160
    r = C.r_from_pts(32.0, 32.0)
    assert abs(r - (160.0 - 2.82) / 160.0) < 1e-9


def test_k_intrinsic_and_dsr_floor():
    assert C.K_INTRINSIC == 2
    assert abs(C.DSR_FLOOR - 0.850) < 1e-12


def test_path_stop_first_same_bar():
    entry = 1900.0
    high = np.array([1905.0])
    low = np.array([1890.0])
    close = np.array([1895.0])
    pts, kind, sd = C.path_pts_stop_target_flat(
        entry, -1, stop_level=1902.0, target_level=1898.0, high=high, low=low, close=close, start=0
    )
    assert kind == "stop"
    assert abs(pts - (-2.0)) < 1e-12
    assert abs(sd - 2.0) < 1e-12


def _first_probe_i(minutes: np.ndarray) -> int:
    """First RTH probe bar — not argmax(minutes>=09:30), which hits overnight 18:00+."""
    idx = np.flatnonzero(
        (minutes >= C.PROBE_OPEN_MIN) & (minutes <= C.PROBE_CLOSE_MIN)
    )
    assert len(idx), "fixture missing probe window"
    return int(idx[0])


def test_axis_a_failed_upside_reclaim_short():
    minutes = _session_minutes_overnight_rth()
    n = len(minutes)
    o, h, lo, c = _base_prices(n, 1900.0)
    pdh, pdl = 1902.0, 1898.0
    probe0 = _first_probe_i(minutes)
    h[probe0] = 1908.0
    c[probe0] = 1905.0
    h[probe0 + 1] = 1904.0
    lo[probe0 + 1] = 1899.0
    c[probe0 + 1] = 1900.0
    o[probe0 + 2] = 1900.0
    trades = C.simulate_axis_a_constrained(o, h, lo, c, minutes, pdh, pdl)
    assert len(trades) == 1
    assert trades[0]["side"] == -1
    assert trades[0]["mode"] == "fade"


def test_axis_b_uses_overnight_levels():
    minutes = _session_minutes_overnight_rth()
    n = len(minutes)
    o, h, lo, c = _base_prices(n, 1900.0)
    # Overnight extremes (evening block is first in the fixture)
    eve0 = int(np.flatnonzero(minutes >= C.OVERNIGHT_OPEN_MIN)[0])
    h[eve0] = 1920.0
    lo[eve0] = 1880.0
    oh, ol = C.overnight_hl(h, lo, minutes)
    assert oh >= 1920.0 - 1e-9
    assert ol <= 1880.0 + 1e-9
    probe0 = _first_probe_i(minutes)
    h[probe0] = 1925.0
    c[probe0] = 1922.0
    c[probe0 + 1] = 1910.0  # reclaim below ONH
    o[probe0 + 2] = 1910.0
    trades = C.simulate_axis_b_constrained(o, h, lo, c, minutes)
    assert len(trades) == 1
    assert trades[0]["side"] == -1


def test_axis_a_delete_sham_uses_overnight():
    minutes = _session_minutes_overnight_rth()
    n = len(minutes)
    o, h, lo, c = _base_prices(n, 1900.0)
    eve0 = int(np.flatnonzero(minutes >= C.OVERNIGHT_OPEN_MIN)[0])
    h[eve0] = 1920.0
    lo[eve0] = 1880.0
    sham = C.simulate_axis_a_delete_sham(o, h, lo, c, minutes)
    assert isinstance(sham, list)
    oh, ol = C.overnight_hl(h, lo, minutes)
    assert oh >= 1920.0 - 1e-9
    assert ol <= 1880.0 + 1e-9


def test_promote_axis_rules():
    assert C.promote_axis("FALSIFIED", "FALSIFIED", -0.1, -0.2) is None
    assert C.promote_axis("SHAPE-CLEAR", "FALSIFIED", 0.1, -0.2) == C.AXIS_A
    assert C.promote_axis("FALSIFIED", "AMBIGUOUS-HOLD", -0.1, 0.05) == C.AXIS_B
    assert C.promote_axis("AMBIGUOUS-HOLD", "AMBIGUOUS-HOLD", 0.1, 0.2) == C.AXIS_B
    assert C.promote_axis("AMBIGUOUS-HOLD", "AMBIGUOUS-HOLD", 0.2, 0.2) == C.AXIS_A


def test_delete_pass_strict():
    assert C.delete_pass(0.1, 0.0) is True
    assert C.delete_pass(0.0, 0.0) is False


def test_flip_pass_strict():
    assert C.flip_pass(0.1, -0.1) is True
    assert C.flip_pass(-0.1, -0.05) is False


def test_cheap_falsifier():
    r = C.cheap_falsifier_freeze_ok()
    assert r.verdict == "CHEAP_FALSIFIER_OK"
    assert abs(r.rt_usd - 2.82) < 1e-9
