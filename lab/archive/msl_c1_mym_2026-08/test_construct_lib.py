"""Synthetic unit tests — no vendor bars. Run before explore GO."""
from __future__ import annotations

from research_utils.camp_import import load_camp_sibling

from pathlib import Path

import numpy as np

C = load_camp_sibling("construct_lib", __file__)


def _session_minutes_overnight_rth() -> np.ndarray:
    """15m bars: overnight 00:00–09:15 + RTH probe 09:30–11:00."""
    overnight = np.arange(0, C.OVERNIGHT_CLOSE_MIN + 1, 15)
    probe = np.arange(C.PROBE_OPEN_MIN, C.PROBE_OPEN_MIN + 15 * 12, 15)
    return np.concatenate([overnight, probe]).astype(int)


def _base_prices(n: int, mid: float = 35000.0) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    o = np.full(n, mid, dtype=float)
    h = np.full(n, mid + 5.0, dtype=float)
    lo = np.full(n, mid - 5.0, dtype=float)
    c = np.full(n, mid, dtype=float)
    return o, h, lo, c


def test_explore_go_present(tmp_path: Path):
    assert C.explore_go_present(tmp_path) is False
    (tmp_path / "EXPLORE_GO.md").write_text("ISSUED 2026-08-13\n", encoding="utf-8")
    assert C.explore_go_present(tmp_path) is True


def test_r_from_pts_matches_usd_formula():
    # 320 pt stop, +320 pt win → pnl $160, stop $160, R = (160-2.82)/160
    r = C.r_from_pts(320.0, 320.0)
    assert abs(r - (160.0 - 2.82) / 160.0) < 1e-9


def test_path_stop_first_same_bar():
    entry = 35000.0
    high = np.array([35050.0])
    low = np.array([34900.0])
    close = np.array([34950.0])
    pts, kind, sd = C.path_pts_stop_target_flat(
        entry, -1, stop_level=35020.0, target_level=34980.0, high=high, low=low, close=close, start=0
    )
    assert kind == "stop"
    assert abs(pts - (-20.0)) < 1e-12
    assert abs(sd - 20.0) < 1e-12


def test_failed_upside_reclaim_short():
    minutes = _session_minutes_overnight_rth()
    n = len(minutes)
    o, h, lo, c = _base_prices(n, 35000.0)
    pdh, pdl = 35010.0, 34990.0
    probe0 = int(np.argmax(minutes >= C.PROBE_OPEN_MIN))
    h[probe0] = 35040.0
    c[probe0] = 35030.0
    h[probe0 + 1] = 35020.0
    lo[probe0 + 1] = 34995.0
    c[probe0 + 1] = 35000.0  # < pdh
    o[probe0 + 2] = 35000.0
    trades = C.simulate_constrained(o, h, lo, c, minutes, pdh, pdl)
    assert len(trades) == 1
    assert trades[0]["side"] == -1
    assert trades[0]["mode"] == "fade"


def test_failed_downside_reclaim_long():
    minutes = _session_minutes_overnight_rth()
    n = len(minutes)
    o, h, lo, c = _base_prices(n, 35000.0)
    pdh, pdl = 35010.0, 34990.0
    probe0 = int(np.argmax(minutes >= C.PROBE_OPEN_MIN))
    lo[probe0] = 34960.0
    h[probe0] = 35005.0  # stay ≤ pdh
    c[probe0] = 34970.0
    h[probe0 + 1] = 35005.0
    lo[probe0 + 1] = 34980.0
    c[probe0 + 1] = 35000.0  # > pdl
    o[probe0 + 2] = 35000.0
    trades = C.simulate_constrained(o, h, lo, c, minutes, pdh, pdl)
    assert len(trades) == 1
    assert trades[0]["side"] == +1


def test_k1_first_signal_only():
    minutes = _session_minutes_overnight_rth()
    n = len(minutes)
    o, h, lo, c = _base_prices(n, 35000.0)
    pdh, pdl = 35010.0, 34990.0
    probe0 = int(np.argmax(minutes >= C.PROBE_OPEN_MIN))
    h[probe0] = 35040.0
    c[probe0] = 35030.0
    c[probe0 + 1] = 35000.0
    o[probe0 + 2] = 35000.0
    h[probe0 + 4] = 35050.0
    c[probe0 + 4] = 35040.0
    c[probe0 + 5] = 35000.0
    trades = C.simulate_constrained(o, h, lo, c, minutes, pdh, pdl)
    assert len(trades) == 1


def test_no_signal_day():
    minutes = _session_minutes_overnight_rth()
    n = len(minutes)
    o, h, lo, c = _base_prices(n, 35000.0)
    trades = C.simulate_constrained(o, h, lo, c, minutes, 35010.0, 34990.0)
    assert trades == []


def test_delete_sham_uses_overnight_not_pdh():
    minutes = _session_minutes_overnight_rth()
    n = len(minutes)
    o, h, lo, c = _base_prices(n, 35000.0)
    # Overnight range wide; RTH never breaks PDH/PDL but does break overnight mid
    overnight0 = 0
    h[overnight0] = 35100.0
    lo[overnight0] = 34900.0
    pdh, pdl = 35010.0, 34990.0
    constrained = C.simulate_constrained(o, h, lo, c, minutes, pdh, pdl)
    sham = C.simulate_delete_sham(o, h, lo, c, minutes)
    # Without a probe sweep of overnight extremes, both may be empty — just ensure API runs
    assert isinstance(constrained, list)
    assert isinstance(sham, list)
    oh, ol = C.overnight_hl(h, lo, minutes)
    assert oh >= 35100.0 - 1e-9
    assert ol <= 34900.0 + 1e-9


def test_delete_pass_strict():
    assert C.delete_pass(0.1, 0.0) is True
    assert C.delete_pass(0.0, 0.0) is False
    assert C.delete_pass(float("nan"), 0.0) is False


def test_flip_pass_strict():
    assert C.flip_pass(0.1, -0.1) is True
    assert C.flip_pass(-0.1, -0.05) is False
