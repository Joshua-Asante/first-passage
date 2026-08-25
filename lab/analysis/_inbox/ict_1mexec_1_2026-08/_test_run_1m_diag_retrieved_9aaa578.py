"""Unit tests for the Part C diagnostic's NEW composition (synthetic, hand-computed).

The archived primitives (pivots, detect_raid, FVG detectors) carry the archive's own
158 tests; these cover only what Part C composes on top: pool-eligibility timing,
raid->FVG pairing (direction + window), and the delayed-fill "spent retrace"
semantics. Each expectation is hand-derived from the frozen rules, never from the
code's output.

Run:  python -m pytest lab/analysis/ict_mnq_2026-08/ -q
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(
    0, str(Path(__file__).resolve().parents[2] / "archive" / "ict_cascade_2026-06-18")
)

import run_1m_diag as D  # noqa: E402


# =============================================================================
# raid_bars -- pool eligibility must be look-ahead-free
# =============================================================================
def _flat(n, px=100.0):
    return (np.full(n, px), np.full(n, px + 0.5), np.full(n, px - 0.5))


def test_pool_registration_timing_and_first_breach():
    """A pvLen=2 pivot at bar t is only KNOWN (registered) at t+pvLen; this runner
    makes it sweepable from t+pvLen+1. With STRICT pivot comparison and
    left==right==pvLen, a pre-registration sweep is structurally impossible -- any
    bar inside the confirmation window that reached the pivot price would have
    destroyed the pivot itself (the eligibility guard in raid_bars is therefore
    defensive, not load-bearing). What IS testable: the pool survives a breach
    that lands after its window, no raid fires before that breach, and the first
    breach raids."""
    o, h, l = _flat(10)
    h = h.copy()
    h[2] = 105.0          # pivot high at bar 2 (bars 0-1 and 3-4 all 100.5 < 105)
    h[6] = 106.0          # first breach, after registration (bar 4) + eligibility (bar 5)
    rb, rs = D.raid_bars(o, h, l, pv_len=2)
    assert not rb[:6].any(), "no raid may fire before the first actual breach"
    assert rb[6], "first eligible breach must raid"


def test_pool_swept_only_once():
    o, h, l = _flat(10)
    h = h.copy()
    h[2] = 105.0
    h[6] = 106.0
    h[8] = 107.0
    rb, rs = D.raid_bars(o, h, l, pv_len=2)
    assert rb[6]
    assert not rb[8], "a pool raids once; the second breach has no pool left"


def test_ssl_raid_from_pivot_low():
    o, h, l = _flat(10)
    l = l.copy()
    l[2] = 95.0    # pivot low at bar 2 -> SSL pool, eligible from bar 5
    l[6] = 94.0    # sweep at bar 6
    rb, rs = D.raid_bars(o, h, l, pv_len=2)
    assert rs[6] and not rb[6]


# =============================================================================
# pair_fvgs_to_raids -- direction mapping + raidWin window
# =============================================================================
def _mk_fvg(bar, bull):
    return {"bar": bar, "top": 101.0, "bot": 100.0, "bull": bull}


def test_bull_fvg_pairs_to_SSL_raid_only():
    raid_buy = np.zeros(30, bool)
    raid_sell = np.zeros(30, bool)
    raid_sell[10] = True
    paired = D.pair_fvgs_to_raids([_mk_fvg(14, True)], raid_buy, raid_sell)
    assert len(paired) == 1, "bull FVG 4 bars after an SSL raid must pair"
    paired = D.pair_fvgs_to_raids([_mk_fvg(14, False)], raid_buy, raid_sell)
    assert len(paired) == 0, "bear FVG must NOT pair to an SSL raid"


def test_pairing_window_boundaries():
    raid_buy = np.zeros(40, bool)
    raid_sell = np.zeros(40, bool)
    raid_sell[10] = True
    # i - r <= 8: bar 18 pairs (18-10=8), bar 19 does not (9 > raidWin).
    assert len(D.pair_fvgs_to_raids([_mk_fvg(18, True)], raid_buy, raid_sell)) == 1
    assert len(D.pair_fvgs_to_raids([_mk_fvg(19, True)], raid_buy, raid_sell)) == 0
    # same-bar pairing allowed (declared boundary): i - r == 0.
    assert len(D.pair_fvgs_to_raids([_mk_fvg(10, True)], raid_buy, raid_sell)) == 1


def test_pairing_uses_most_recent_raid():
    """An FVG after two raids pairs via the most recent one; an old raid beyond
    the window does not rescue it."""
    raid_buy = np.zeros(40, bool)
    raid_sell = np.zeros(40, bool)
    raid_sell[5] = True
    raid_sell[20] = True
    assert len(D.pair_fvgs_to_raids([_mk_fvg(25, True)], raid_buy, raid_sell)) == 1
    assert len(D.pair_fvgs_to_raids([_mk_fvg(16, True)], raid_buy, raid_sell)) == 0


# =============================================================================
# delayed_fill_stats -- the "spent retrace" semantics (the load-bearing rule)
# =============================================================================
def test_touch_before_arm_does_not_fill():
    """Bull FVG, mid=100.5. Price touches mid ONLY at bar t0+1, then stays above.
    d=0 (armed from t0+1) fills; d=1 (armed from t0+2) must NOT -- that retrace
    was spent before the order existed. This is the exact mechanism hypothesis
    (a1) rests on; a sign/offset error here inverts the whole diagnostic."""
    n = 20
    high = np.full(n, 103.0)
    low = np.full(n, 102.0)
    t0 = 5
    low = low.copy()
    low[t0 + 1] = 100.4          # the only mid-touch
    fvg = [{"bar": t0, "top": 101.0, "bot": 100.0, "bull": True}]
    d0 = D.delayed_fill_stats(fvg, high, low, 0)
    d1 = D.delayed_fill_stats(fvg, high, low, 1)
    assert d0["hits"] == 1
    assert d1["hits"] == 0, "a pre-arm touch must not fill a later order"


def test_second_touch_fills_late_arm():
    """If price re-touches mid inside the armed window, the late order DOES fill."""
    n = 20
    high = np.full(n, 103.0)
    low = np.full(n, 102.0)
    t0 = 5
    low = low.copy()
    low[t0 + 1] = 100.4          # first touch (spent for d>=1)
    low[t0 + 4] = 100.3          # second touch (inside d=1's window (t0+1, t0+7])
    fvg = [{"bar": t0, "top": 101.0, "bot": 100.0, "bull": True}]
    d1 = D.delayed_fill_stats(fvg, high, low, 1)
    assert d1["hits"] == 1


def test_window_length_is_k_after_arm():
    """d=2, k=6: window is bars t0+3 .. t0+8 inclusive. A touch at t0+9 misses."""
    n = 20
    high = np.full(n, 103.0)
    low = np.full(n, 102.0)
    t0 = 5
    low = low.copy()
    low[t0 + 9] = 100.4
    fvg = [{"bar": t0, "top": 101.0, "bot": 100.0, "bull": True}]
    assert D.delayed_fill_stats(fvg, high, low, 2)["hits"] == 0
    low[t0 + 8] = 100.4
    assert D.delayed_fill_stats(fvg, high, low, 2)["hits"] == 1


def test_bear_fvg_touch_side():
    """Bear FVG mid touched from below via HIGH, not low."""
    n = 20
    high = np.full(n, 98.0)
    low = np.full(n, 97.0)
    t0 = 5
    high = high.copy()
    high[t0 + 2] = 100.6
    fvg = [{"bar": t0, "top": 101.0, "bot": 100.0, "bull": False}]
    assert D.delayed_fill_stats(fvg, high, low, 0)["hits"] == 1


def test_incomplete_window_censored():
    """An FVG whose armed window runs past the last bar is excluded, not counted."""
    n = 10
    high = np.full(n, 103.0)
    low = np.full(n, 102.0)
    fvg = [{"bar": 6, "top": 101.0, "bot": 100.0, "bull": True}]  # 6+0+6 >= 10
    s = D.delayed_fill_stats(fvg, high, low, 0)
    assert s["n"] == 0


def test_d0_matches_part_b_probe_semantics():
    """At d=0 the window (t0, t0+6] must equal run_1m_probe.retrace_stats' window --
    the two instruments must agree at their shared cell."""
    import run_1m_probe as P
    rng = np.random.default_rng(7)
    n = 400
    high = 100 + np.cumsum(rng.normal(0, 0.3, n)) + 0.4
    low = high - 0.8
    fvgs = [{"bar": i, "top": float(high[i] - 0.2), "bot": float(low[i] + 0.2),
             "bull": bool(i % 2)} for i in range(3, 350, 7)]
    a = D.delayed_fill_stats(fvgs, high, low, 0)
    b = P.retrace_stats(fvgs, high, low, 6)
    assert a["n"] == b["n"]
    assert a["hits"] == b["hits"]


# =============================================================================
# heap raid_bars must be flag-identical to the literal archived-primitive scan
# =============================================================================
def _literal_raid_bars(h, l, pv_len):
    """Reference implementation: per-bar detect_raid over the growing registry --
    the archived primitive used literally (O(n x pools), test-scale only)."""
    import _ict_offline as M
    n = len(h)
    pools = M.pools_from_pivots(h, l, pv_len)
    eligible_at = {}
    for p in pools:
        eligible_at.setdefault(p["bar"] + pv_len + 1, []).append(p)
    active = []
    rb = np.zeros(n, bool)
    rs = np.zeros(n, bool)
    for j in range(n):
        active.extend(eligible_at.get(j, ()))
        b, s = M.detect_raid(active, h[j], l[j], j)
        rb[j], rs[j] = b, s
        active = [p for p in active if not p["swept"]]
    return rb, rs


def test_heap_raid_bars_matches_archived_detect_raid():
    """The performance rewrite must be FLAG-IDENTICAL to the archived detect_raid
    semantics on data with ties, trends, and reversals. 5 seeds x 600 bars."""
    for seed in range(5):
        rng = np.random.default_rng(seed)
        steps = rng.normal(0, 1.0, 600) + 0.05          # slight drift: pools accumulate
        close = 1000 + np.cumsum(steps)
        high = close + np.abs(rng.normal(0, 0.5, 600))
        low = close - np.abs(rng.normal(0, 0.5, 600))
        # inject exact-tie touches (detect_raid is INCLUSIVE: >= / <=)
        high[100] = high[50]
        low[200] = low[150]
        o = close.copy()
        rb_ref, rs_ref = _literal_raid_bars(high, low, 2)
        rb_new, rs_new = D.raid_bars(o, high, low, pv_len=2)
        assert (rb_ref == rb_new).all(), f"BSL raid flags diverge (seed {seed})"
        assert (rs_ref == rs_new).all(), f"SSL raid flags diverge (seed {seed})"


# =============================================================================
# frozen read boundaries
# =============================================================================
def test_read_verdict_boundaries():
    assert D.read_verdict(0.012) == "EXPLAINS"
    assert D.read_verdict(0.0121) == "CONTRIBUTES-INSUFFICIENT"
    assert D.read_verdict(0.20) == "CONTRIBUTES-INSUFFICIENT"
    assert D.read_verdict(0.201) == "REFUTED-AS-EXPLANATION"
    assert D.read_verdict(float("nan")) == "NO-DATA"
