"""Synthetic unit tests — no vendor bars. Run before explore GO."""
from __future__ import annotations

from research_utils.camp_import import load_camp_sibling

from pathlib import Path

import numpy as np

C = load_camp_sibling("construct_lib", __file__)


def _session_minutes_london_probe() -> np.ndarray:
    """15m bars: London 03:00–08:15 + probe 08:20–10:00 (enough for signal)."""
    london = np.arange(C.LONDON_OPEN_MIN, C.LONDON_CLOSE_MIN + 1, 15)
    # include 08:15 as last london-ish; PREREG london closes 08:19 so 08:15 open is in
    probe = np.arange(C.PROBE_OPEN_MIN, C.PROBE_OPEN_MIN + 15 * 12, 15)  # through ~11:05
    return np.concatenate([london, probe]).astype(int)


def _base_prices(n: int, mid: float = 2000.0) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    o = np.full(n, mid, dtype=float)
    h = np.full(n, mid + 0.5, dtype=float)
    lo = np.full(n, mid - 0.5, dtype=float)
    c = np.full(n, mid, dtype=float)
    return o, h, lo, c


def test_explore_go_present(tmp_path: Path):
    assert C.explore_go_present(tmp_path) is False
    (tmp_path / "EXPLORE_GO.md").write_text("ISSUED 2026-08-13\n", encoding="utf-8")
    assert C.explore_go_present(tmp_path) is True


def test_r_from_pts_matches_usd_formula():
    # 16 pt stop, +16 pt win → pnl $160, stop $160, R = (160-4.12)/160
    r = C.r_from_pts(16.0, 16.0)
    assert abs(r - (160.0 - 4.12) / 160.0) < 1e-9


def test_path_stop_first_same_bar():
    entry = 100.0
    # short: stop above, target below; same bar hits both → stop-first
    high = np.array([101.0])
    low = np.array([98.0])
    close = np.array([99.0])
    pts, kind, sd = C.path_pts_stop_target_flat(
        entry, -1, stop_level=100.5, target_level=99.0, high=high, low=low, close=close, start=0
    )
    assert kind == "stop"
    assert pts == -0.5
    assert abs(sd - 0.5) < 1e-12


def test_failed_upside_reclaim_short():
    minutes = _session_minutes_london_probe()
    n = len(minutes)
    o, h, lo, c = _base_prices(n, 2000.0)
    # London range ~ 1999.5–2000.5
    # First probe bar: sweep above London high
    probe0 = int(np.argmax(minutes >= C.PROBE_OPEN_MIN))
    h[probe0] = 2002.0
    c[probe0] = 2001.5  # still above — not reclaim yet
    # Next probe bar: close back below London high
    h[probe0 + 1] = 2001.0
    lo[probe0 + 1] = 1999.0
    c[probe0 + 1] = 2000.0  # < london_hi 2000.5
    o[probe0 + 2] = 2000.0
    trades = C.simulate_constrained(o, h, lo, c, minutes)
    assert len(trades) == 1
    assert trades[0]["side"] == -1
    assert trades[0]["mode"] == "fade"


def test_failed_downside_reclaim_long():
    minutes = _session_minutes_london_probe()
    n = len(minutes)
    o, h, lo, c = _base_prices(n, 2000.0)
    probe0 = int(np.argmax(minutes >= C.PROBE_OPEN_MIN))
    lo[probe0] = 1998.0
    h[probe0] = 2000.0  # must stay ≤ london_hi so upside arm does not fire
    c[probe0] = 1998.5
    h[probe0 + 1] = 2000.4  # still ≤ london_hi 2000.5
    lo[probe0 + 1] = 1999.0
    c[probe0 + 1] = 2000.0  # > london_lo 1999.5
    o[probe0 + 2] = 2000.0
    trades = C.simulate_constrained(o, h, lo, c, minutes)
    assert len(trades) == 1
    assert trades[0]["side"] == +1


def test_k1_first_signal_only():
    minutes = _session_minutes_london_probe()
    n = len(minutes)
    o, h, lo, c = _base_prices(n, 2000.0)
    probe0 = int(np.argmax(minutes >= C.PROBE_OPEN_MIN))
    # Two potential upside fails — only first entry
    h[probe0] = 2002.0
    c[probe0] = 2001.5
    c[probe0 + 1] = 2000.0
    o[probe0 + 2] = 2000.0
    h[probe0 + 4] = 2003.0
    c[probe0 + 4] = 2002.0
    c[probe0 + 5] = 2000.0
    trades = C.simulate_constrained(o, h, lo, c, minutes)
    assert len(trades) == 1


def test_no_signal_day():
    minutes = _session_minutes_london_probe()
    n = len(minutes)
    o, h, lo, c = _base_prices(n, 2000.0)
    # never leave London range
    trades = C.simulate_constrained(o, h, lo, c, minutes)
    assert trades == []


def test_delete_sham_different_ref_changes_signals():
    minutes = _session_minutes_london_probe()
    n = len(minutes)
    o, h, lo, c = _base_prices(n, 2000.0)
    probe0 = int(np.argmax(minutes >= C.PROBE_OPEN_MIN))
    h[probe0] = 2002.0
    c[probe0] = 2001.5
    c[probe0 + 1] = 2000.0
    o[probe0 + 2] = 2000.0
    constrained = C.simulate_constrained(o, h, lo, c, minutes)
    # Sham prior RTH far away — no sweep of sham levels → empty
    sham = C.simulate_delete_sham(o, h, lo, c, minutes, 2100.0, 2090.0)
    assert len(constrained) == 1
    assert sham == []


def test_flip_reverses_side():
    minutes = _session_minutes_london_probe()
    n = len(minutes)
    o, h, lo, c = _base_prices(n, 2000.0)
    probe0 = int(np.argmax(minutes >= C.PROBE_OPEN_MIN))
    h[probe0] = 2002.0
    c[probe0] = 2001.5
    c[probe0 + 1] = 2000.0
    o[probe0 + 2] = 2000.0
    # Give room so path doesn't instantly stop both sides identically
    fade = C.simulate_constrained(o, h, lo, c, minutes)
    flip = C.simulate_flip_join(o, h, lo, c, minutes)
    assert len(fade) == 1 and len(flip) == 1
    assert fade[0]["side"] == -1
    assert flip[0]["side"] == +1
    assert abs(fade[0]["stop_dist"] - flip[0]["stop_dist"]) < 1e-12


def test_delete_flip_pass_helpers():
    assert C.delete_pass(0.10, 0.01) is True
    assert C.delete_pass(0.01, 0.10) is False
    assert C.flip_pass(0.05, -0.02) is True
    assert C.flip_pass(-0.02, 0.05) is False
    assert C.delete_pass(float("nan"), 0.0) is False


def test_g0_template_all_u():
    t = C.g0_freeze_verdict_template()
    assert t.startswith("U U U U U |")
