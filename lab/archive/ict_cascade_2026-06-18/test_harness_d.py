"""Synthetic-fixture unit tests for harness_d.py (Layer D -- Daily DOL).

TDD for Q-ICT-CASCADE-1 Layer D. Every fixture is hand-built in-test on
SYNTHETIC Daily OHLC -- NO external export is touched, so these pass NOW with no
vendor data. The real-export entrypoint (harness_d.main) skips cleanly when the
operator has not yet produced the Daily TV export.

Encodes the FROZEN PREREG-D thresholds:
  * pool t0 = TRUE pivot bar (bar_index - pvLen), pvLen=3        (D-2)
  * FVG t0 = registration bar, touch scanned from f.bar+1        (D-2b / D-1 guard)
  * poolRate / fvgRate per SIDE (BSL / SSL), never pooled
  * drawK = 10 K-window; objects within drawK of last bar are CENSORED (dropped)
  * D-3 radius-matched MC base-rate null, MC >= 5000 per side
  * PASS band: real_rate > base_rate + 95% bootstrap CI half-width
  * block = distinct origin bar; n-floor = 30 EFFECTIVE BLOCKS per side
  * D-4 grid dispMlt{0,1.5,3.0} x pvLen{2,3,5} = 9 cells, report n-per-cell
  * sec 6 verdict per side (RESOLVED / FALSIFIED / AMBIGUOUS-HOLD / INSUFFICIENT-N)

Run directly (the repo default `pytest tests/` does NOT collect lab/):
    python -m pytest lab/analysis/ict_cascade_2026-06-18/test_harness_d.py -q
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness_d as HD  # noqa: E402
import _ict_offline as M  # noqa: E402


def approx(a, b, tol=1e-9):
    assert abs(a - b) < tol, f"{a} != {b}"


# =============================================================================
# Bars container + loader-shape sanity
# =============================================================================
def _bars(o, h, l, c, epoch_ms=None):
    """Build a DailyBars from explicit OHLC. epoch defaults to one-day spacing."""
    n = len(o)
    if epoch_ms is None:
        day = 86_400_000
        start = 1_700_000_000_000
        epoch_ms = [start + i * day for i in range(n)]
    return HD.build_bars(np.array(epoch_ms, dtype="int64"),
                         np.array(o, float), np.array(h, float),
                         np.array(l, float), np.array(c, float))


def test_build_bars_atr_is_wilder():
    # ATR on the DailyBars must equal _ict_offline.wilder_atr exactly.
    rng = np.random.default_rng(0)
    n = 60
    c = 100 + np.cumsum(rng.normal(0, 1, n))
    h = c + rng.uniform(0.5, 2.0, n)
    l = c - rng.uniform(0.5, 2.0, n)
    o = c + rng.normal(0, 0.3, n)
    b = _bars(o, h, l, c)
    ref = M.wilder_atr(h, l, c, 14)
    assert np.allclose(b.atr, ref, equal_nan=True)


def test_build_bars_et_fields_present():
    b = _bars([1, 2, 3], [2, 3, 4], [0, 1, 2], [1, 2, 3])
    assert b.n == 3
    assert len(b.et_date) == 3


# =============================================================================
# POOL CONSTRUCTION -- pool t0 = TRUE pivot bar (D-2), pvLen=3
# =============================================================================
def test_pools_t0_is_true_pivot_bar():
    # A clean peak at index 6 with pvLen=3 (left=right=3). pool.bar must be 6,
    # NOT the confirmation bar 9. This is the D-2 common-origin clock.
    high = np.array([1, 2, 3, 4, 5, 6, 10, 6, 5, 4, 3, 2, 1], float)
    low = np.full(13, 0.5)
    pools = M.pools_from_pivots(high, low, 3)
    bsl = [p for p in pools if p["buyside"]]
    assert any(p["bar"] == 6 and abs(p["price"] - 10.0) < 1e-9 for p in bsl), \
        "BSL pool t0 must be the TRUE pivot bar (index 6), not confirmation bar 9"


# =============================================================================
# THE CORE FIXTURE: a known pool that gets swept + an FVG touched LATE.
# poolRate / fvgRate per side, with the D-1 guard load-bearing.
# =============================================================================
def _pool_sweep_fixture():
    """Daily series with ONE BSL pool (high pivot) that is later swept within K,
    and ONE bull FVG whose near edge is touched on a LATER bar (not its own).

    Layout (index : role):
      0..3  ramp up to a peak at 4 ......... pivot HIGH at 4 (pvLen=3 confirms at 7)
      4     peak high=20 ................... BSL pool t0 = bar 4, price 20
      5..6  pull back .................... (pvLen=3 right side: 5,6,7 all < 20)
      7..8  drift ........................ confirmation window
      9     a bull-FVG displacement candle prints a gap (registered at 9)
      10    re-tests / touches the FVG near edge (LATE touch -> D-1 guard passes)
      11    rallies and SWEEPS the BSL pool (high >= 20) within K of bar 4
      12..  tail
    """
    n = 30
    o = np.full(n, 10.0)
    h = np.full(n, 10.5)
    l = np.full(n, 9.5)
    c = np.full(n, 10.0)
    # ramp to a clean strict peak at index 4 (pvLen=3 needs 3 strictly-lower each side)
    h[0:4] = [11, 12, 13, 14]
    h[4] = 20.0          # the pivot high -> BSL pool at price 20, bar 4
    h[5:8] = [15, 14, 13]
    l[0:9] = 9.0
    c[0:9] = [11, 12, 13, 14, 15, 14, 13, 12, 11]
    o[0:9] = c[0:9]
    return n, o, h, l, c


def test_pool_swept_within_k_counts():
    n, o, h, l, c = _pool_sweep_fixture()
    # bar 11 sweeps the BSL pool (high reaches 20.0); 11 - 4 = 7 <= drawK(10).
    h[11] = 21.0
    b = _bars(o, h, l, c)
    res = HD.compute_rates(b, pv_len=3, disp_mlt=1.5, atr_len=14, draw_k=10)
    bsl = res["BSL"]["pool"]
    assert bsl["hits"] >= 1, "the engineered BSL sweep within K must be counted"
    # the pool's distinct origin bar is 4 -> at least one block on BSL pool side.
    assert bsl["n_blocks"] >= 1


def test_pool_swept_outside_k_not_counted():
    n, o, h, l, c = _pool_sweep_fixture()
    # sweep happens at bar 4 + drawK + 5 = 19 -> OUTSIDE K -> NOT a hit.
    h[19] = 21.0
    b = _bars(o, h, l, c)
    res = HD.compute_rates(b, pv_len=3, disp_mlt=1.5, atr_len=14, draw_k=10)
    bsl = res["BSL"]["pool"]
    # the pool is in-window (origin 4, last bar 29 -> 4 <= 29-10) but never swept in K.
    assert bsl["n"] >= 1
    assert bsl["hits"] == 0, "a sweep beyond drawK must not be credited"


# =============================================================================
# THE D-1 GUARD CHANGES THE FVG COUNT (the load-bearing assertion the prompt names)
# =============================================================================
def _bull_fvg_fixture():
    """Daily series with TWO bull FVGs past the ATR(14) warmup:

      FVG-A (registered bar 20): near edge 101.0 == this bar's own low, and NEVER
        re-touched within K. WITHOUT the D-1 guard it self-touches on bar 20 (a
        false hit); WITH the guard it has NO in-K touch. -> the guard removes this
        hit, so guarded count < unguarded count.

      FVG-B (registered bar 30): near edge 110.0, genuinely RE-touched on a strictly
        later bar 33 (low dips to 109.5 <= 110.0). Both guarded and unguarded count
        it -> a real late touch is still credited under the guard.

    So: unguarded hits = 2 (A self-touch + B late), guarded hits = 1 (B late only).
    The displacement candle for each FVG has range >> 1.5*ATR (quiet ~0.6 baseline).
    """
    n = 45
    # Quiet baseline through the ATR warmup, then a STEP UP so post-gap lows stay
    # above each FVG's near edge (a bull near edge is touched from ABOVE: low<=top).
    o = np.full(n, 100.0)
    h = np.full(n, 100.3)
    l = np.full(n, 99.7)
    c = np.full(n, 100.0)
    # step the price plateau up to ~105 from bar 21 onward (lows ~104.7 > 101.0),
    # so FVG-A's near edge 101.0 is NOT touched after registration unless engineered.
    o[21:] = 105.0
    h[21:] = 105.3
    l[21:] = 104.7
    c[21:] = 105.0

    # ---- FVG-A at registration bar 20 (self-touch ONLY; never re-touched in K) ----
    h[18] = 100.0
    l[18] = 99.0
    o[19] = 100.0; c[19] = 104.0; h[19] = 104.5; l[19] = 99.8   # displacement middle
    o[20] = 101.5; c[20] = 103.0; h[20] = 103.5; l[20] = 101.0  # gap; NEAR=101.0==low
    # bars 21..30 sit on the ~105 plateau (lows 104.7 > 101.0) -> FVG-A near edge
    # 101.0 is never re-touched within K=10 -> guarded hit for A = 0.

    # ---- FVG-B at registration bar 30 (genuine LATE touch) ----
    h[28] = 105.0
    l[28] = 104.0
    o[29] = 105.0; c[29] = 109.0; h[29] = 109.5; l[29] = 104.8  # displacement middle
    o[30] = 106.5; c[30] = 108.0; h[30] = 108.5; l[30] = 106.0  # gap; NEAR=106.0
    # bars 31,32 stay above 106.0 (no touch); bar 33 dips to touch the near edge.
    o[31] = 107.5; c[31] = 107.8; h[31] = 108.0; l[31] = 107.0
    o[32] = 107.2; c[32] = 107.4; h[32] = 107.6; l[32] = 106.5
    o[33] = 107.0; c[33] = 106.4; h[33] = 107.2; l[33] = 105.5  # LATE touch (low<=106.0)
    # tail returns toward the plateau (kept above 106.0 to avoid extra touches).
    o[34:] = 107.0; h[34:] = 107.3; l[34:] = 106.7; c[34:] = 107.0
    return n, o, h, l, c


def test_d1_guard_changes_fvg_touch_count():
    n, o, h, l, c = _bull_fvg_fixture()
    b = _bars(o, h, l, c)
    # WITH the D-1 guard (touch must be at bar > f.bar): the gap candle (bar 10)
    # does NOT self-touch; only the later bar 14 touch counts.
    guarded = HD.compute_rates(b, pv_len=3, disp_mlt=1.5, atr_len=14, draw_k=10,
                               fvg_guard=True)
    unguarded = HD.compute_rates(b, pv_len=3, disp_mlt=1.5, atr_len=14, draw_k=10,
                                 fvg_guard=False)
    g_bull = guarded["BSL"]["fvg"]
    u_bull = unguarded["BSL"]["fvg"]
    # there is at least one bull FVG in window
    assert g_bull["n"] >= 1 and u_bull["n"] >= 1
    # the unguarded count self-touches the gap-forming candle -> >= guarded count,
    # and the two must differ (the guard is load-bearing for this fixture).
    assert u_bull["hits"] > g_bull["hits"], \
        "D-1 guard must reduce the FVG touch count (no self-touch on registration bar)"


def test_d1_guard_late_touch_is_credited():
    n, o, h, l, c = _bull_fvg_fixture()
    b = _bars(o, h, l, c)
    res = HD.compute_rates(b, pv_len=3, disp_mlt=1.5, atr_len=14, draw_k=10,
                           fvg_guard=True)
    bull = res["BSL"]["fvg"]
    # the late (bar 14) touch IS within K of registration (14 - 10 = 4 <= 10) and
    # is strictly later -> credited.
    assert bull["hits"] >= 1, "a strictly-later in-K near-edge touch must count"


# =============================================================================
# DISP_MLT == 0 -- Pine displacement(mult=0) = na(atr)?false:(rng>0) drops warmup
# + zero-range middles (R4-2 / R4-3). The disp_mlt==0 cell is NOT "every gap".
# =============================================================================
def test_disp_mlt_zero_drops_warmup_and_zero_range_middle():
    # R4-2/R4-3: at disp_mlt==0 the displacement gate must STILL apply (Pine
    # displacement returns na(atr)?false:(rng>0)). So a gap whose middle candle is
    # in the ATR(14) warmup window (atr NaN) and a gap whose middle candle has zero
    # range (high==low) must NOT register.
    n = 40
    o = np.full(n, 100.0)
    h = np.full(n, 100.3)
    l = np.full(n, 99.7)
    c = np.full(n, 100.0)

    # --- (1) WARMUP gap: a bull FVG registered at bar 3 (middle candle = bar 2,
    # inside ATR(14) warmup -> atr[3] is NaN). low[3] > high[1] forms the gap.
    h[1] = 100.0
    l[1] = 99.0
    o[2] = 100.0; c[2] = 101.0; h[2] = 101.2; l[2] = 99.9   # middle candle (warmup)
    o[3] = 101.5; c[3] = 102.0; h[3] = 102.2; l[3] = 101.0  # gap: low[3]=101.0 > high[1]=100.0

    # --- (2) ZERO-RANGE-MIDDLE gap past warmup: bull FVG registered at bar 25 with
    # middle candle (bar 24) having high == low (zero range -> rng>0 is False).
    h[23] = 100.0
    l[23] = 99.0
    o[24] = 100.5; c[24] = 100.5; h[24] = 100.5; l[24] = 100.5  # ZERO-range middle
    o[25] = 101.5; c[25] = 102.0; h[25] = 102.2; l[25] = 101.0  # gap: low[25]=101.0 > high[23]=100.0

    b = _bars(o, h, l, c)
    fvg = HD.compute_rates(b, pv_len=3, disp_mlt=0.0, atr_len=14, draw_k=10)
    bull = fvg["BSL"]["fvg"]
    # Neither the warmup gap (bar 3) nor the zero-range-middle gap (bar 25) may be
    # in the registry -> their origin bars must be absent.
    origins = set(int(x) for x in bull["origin_bars"])
    assert 3 not in origins, "disp_mlt==0 must NOT register a warmup (NaN ATR) gap"
    assert 25 not in origins, "disp_mlt==0 must NOT register a zero-range-middle gap"


# =============================================================================
# CENSORING -- objects within drawK of the last bar are DROPPED
# =============================================================================
def test_censoring_drops_objects_near_last_bar():
    # A pool whose pivot bar is within drawK of the last bar has an incomplete
    # K-window -> dropped (right-censored).
    n = 20
    high = np.full(n, 10.0)
    low = np.full(n, 9.0)
    o = np.full(n, 9.5)
    c = np.full(n, 9.5)
    # peak at index 17 (within drawK=10 of last bar 19) -> CENSORED.
    high[14:18] = [11, 12, 13, 30]
    high[18:20] = [13, 12]
    b = _bars(o, high, low, c)
    res = HD.compute_rates(b, pv_len=3, disp_mlt=1.5, atr_len=14, draw_k=10)
    # the only BSL pool (pivot 17) is censored -> 0 in-window pools.
    assert res["BSL"]["pool"]["n"] == 0


def test_censoring_drops_object_at_exactly_age_equals_drawk():
    # R4-1: Pine (ict_daily_dol.pine L82) keeps an unswept object as a MISS only
    # when age > drawK (STRICT). An object at exactly age == drawK is dropped (it
    # is neither hit nor miss -> excluded from the rate population). The offline
    # _censor must mirror this: keep r["bar"] < n-1-drawK, i.e. an origin bar
    # whose age to the last bar is EXACTLY drawK is EXCLUDED.
    draw_k = 10
    n = 30
    # last bar = 29. age == drawK means origin bar = 29 - 10 = 19. That object
    # must be EXCLUDED (age == drawK is not > drawK).
    records_at_drawk = [{"bar": 19, "hit": False}]
    kept = HD._censor(records_at_drawk, n, draw_k)
    assert kept == [], "an object at exactly age==drawK must be censored (Pine strict age>drawK)"
    # one bar earlier (age == drawK+1) is kept.
    records_below = [{"bar": 18, "hit": True}]
    kept2 = HD._censor(records_below, n, draw_k)
    assert len(kept2) == 1, "an object at age==drawK+1 (origin bar 18) must be kept"


def test_censor_drops_right_edge_fast_hit_conservative_vs_pine():
    # DOCUMENTED offline-vs-Pine divergence (PREREG-D 2026-06-19 POST-DATA
    # CLARIFICATION; _censor docstring). Pine ict_daily_dol.pine L80 (pool) / L88
    # (FVG) COUNT a swept/touched-WITHIN-K object as a HIT even when age <= drawK;
    # it drops from the population ONLY the UNSWEPT age<=drawK objects (incomplete
    # window). The offline _censor is deliberately stricter: it drops EVERY
    # age<=drawK object, INCLUDING the within-K right-edge fast-hits Pine keeps
    # (removes a right-edge censoring / immortal-time bias; uniform pool/FVG;
    # strictly conservative for a RESOLVED verdict -- restoring fast-hits only RAISES
    # a rate, so the offline rate is a lower bound on the Pine-faithful rate).
    draw_k = 10
    n = 30                       # last bar = 29; last_complete origin = 18
    # origin bar 25: age = 29-25 = 4 <= drawK but HIT within K -> Pine keeps as a
    # HIT; the offline censor must DROP it (this is the conservative divergence).
    fast_hit = [{"bar": 25, "hit": True}]
    assert HD._censor(fast_hit, n, draw_k) == [], \
        "a right-edge fast-hit (age<=drawK, hit) must be dropped offline (Pine keeps it)"
    # like-for-like: the drop is hit-AGNOSTIC for age<=drawK, so an unswept
    # age<=drawK object is dropped by the SAME rule (here Pine also drops it).
    unswept = [{"bar": 25, "hit": False}]
    assert HD._censor(unswept, n, draw_k) == []
    # a fully-observable object (age == drawK+1 = 11 > drawK) is kept regardless of hit.
    assert len(HD._censor([{"bar": 18, "hit": True}], n, draw_k)) == 1


# =============================================================================
# SIDE SPLIT -- BSL (buyside) vs SSL (sellside) never pooled
# =============================================================================
def test_side_split_keys_present():
    b = _bars([10, 11, 12], [11, 12, 13], [9, 10, 11], [10, 11, 12])
    res = HD.compute_rates(b, pv_len=3, disp_mlt=1.5, atr_len=14, draw_k=10)
    assert set(res.keys()) == {"BSL", "SSL"}
    for side in ("BSL", "SSL"):
        assert set(res[side].keys()) == {"pool", "fvg"}
        for obj in ("pool", "fvg"):
            for key in ("n", "hits", "rate", "n_blocks", "distances",
                        "origin_bars", "hit_flags"):
                assert key in res[side][obj], f"{side}/{obj} missing {key}"


# =============================================================================
# n-FLOOR is EFFECTIVE BLOCKS, not raw objects (PREREG-D genuine choice #3)
# =============================================================================
def test_n_floor_counts_blocks_not_objects():
    # Two objects stamped on the SAME origin bar collapse to ONE block.
    origin_bars = [5, 5, 7, 7, 7]           # 2 distinct bars -> 2 blocks
    assert HD.effective_blocks(origin_bars) == 2
    assert HD.effective_blocks([1, 2, 3, 4]) == 4
    assert HD.effective_blocks([]) == 0


def test_verdict_insufficient_n_below_floor():
    # 29 blocks < 30 floor -> INSUFFICIENT-N regardless of how strong the rate.
    side_res = {
        "pool": dict(n=29, hits=29, rate=1.0, n_blocks=29,
                     distances=np.ones(29), origin_bars=list(range(29)),
                     hit_flags=np.ones(29)),
        "fvg": dict(n=10, hits=2, rate=0.2, n_blocks=10,
                    distances=np.ones(10), origin_bars=list(range(10)),
                    hit_flags=np.zeros(10)),
    }
    v = HD.verdict_for_side(side_res, base_pool=0.1, base_pool_hw=0.02,
                            base_fvg=0.1, base_fvg_hw=0.02,
                            half_pool=(1.0, 1.0), half_fvg=(0.2, 0.2),
                            n_floor=30)
    assert v["verdict"] == "INSUFFICIENT-N"


# =============================================================================
# VERDICT GATE (sec 6) -- RESOLVED / FALSIFIED / AMBIGUOUS-HOLD
# =============================================================================
def _strong_side(n_blocks=40, rate=0.8):
    nb = n_blocks
    return dict(n=nb, hits=int(rate * nb), rate=rate, n_blocks=nb,
                distances=np.ones(nb), origin_bars=list(range(nb)),
                hit_flags=np.array([1] * int(rate * nb) + [0] * (nb - int(rate * nb)),
                                   float))


def test_verdict_resolved_when_clears_and_stationary():
    # rate 0.8 clears base 0.1 + hw 0.02; n_blocks 40 >= 30; both halves > base.
    side_res = {"pool": _strong_side(40, 0.8), "fvg": _strong_side(40, 0.2)}
    v = HD.verdict_for_side(side_res, base_pool=0.10, base_pool_hw=0.02,
                            base_fvg=0.10, base_fvg_hw=0.02,
                            half_pool=(0.78, 0.82), half_fvg=(0.18, 0.22),
                            n_floor=30, selectivity_ok=True)
    assert v["verdict"] == "RESOLVED"
    assert "pool" in v["clearing_objects"]


def test_verdict_falsified_when_neither_clears():
    # both rates below base + hw, both at n-floor -> FALSIFIED.
    side_res = {"pool": _strong_side(40, 0.10), "fvg": _strong_side(40, 0.08)}
    v = HD.verdict_for_side(side_res, base_pool=0.20, base_pool_hw=0.02,
                            base_fvg=0.20, base_fvg_hw=0.02,
                            half_pool=(0.10, 0.10), half_fvg=(0.08, 0.08),
                            n_floor=30)
    assert v["verdict"] == "FALSIFIED"


def test_verdict_ambiguous_when_one_regime():
    # pool clears overall but ONE half is on the WRONG side of base -> AMBIGUOUS-HOLD.
    side_res = {"pool": _strong_side(40, 0.50), "fvg": _strong_side(40, 0.05)}
    v = HD.verdict_for_side(side_res, base_pool=0.10, base_pool_hw=0.02,
                            base_fvg=0.10, base_fvg_hw=0.02,
                            half_pool=(0.55, 0.05),   # second half BELOW base -> not stationary
                            half_fvg=(0.05, 0.05),
                            n_floor=30, selectivity_ok=True)
    assert v["verdict"] == "AMBIGUOUS-HOLD"


def test_verdict_ambiguous_when_selectivity_explains():
    # pool clears + stationary, but selectivity probe explains it -> AMBIGUOUS-HOLD.
    side_res = {"pool": _strong_side(40, 0.50), "fvg": _strong_side(40, 0.05)}
    v = HD.verdict_for_side(side_res, base_pool=0.10, base_pool_hw=0.02,
                            base_fvg=0.10, base_fvg_hw=0.02,
                            half_pool=(0.48, 0.52), half_fvg=(0.05, 0.05),
                            n_floor=30, selectivity_ok=False)
    assert v["verdict"] == "AMBIGUOUS-HOLD"


# =============================================================================
# PASS BAND helper -- real_rate > base_rate + 95% CI half-width
# =============================================================================
def test_pass_band():
    # half-width = (hi - lo)/2.
    assert HD.clears_base(0.80, base_rate=0.50, ci=(0.45, 0.55)) is True   # 0.50+0.05=0.55 < 0.80
    assert HD.clears_base(0.56, base_rate=0.50, ci=(0.45, 0.55)) is True   # 0.55 < 0.56
    assert HD.clears_base(0.55, base_rate=0.50, ci=(0.45, 0.55)) is False  # exactly at band -> strict >
    assert HD.clears_base(0.40, base_rate=0.50, ci=(0.45, 0.55)) is False


# =============================================================================
# D-3 RADIUS-MATCHED BASE RATE wiring (per side, via _ict_offline)
# =============================================================================
def test_base_rate_uses_offline_and_enforces_mc_floor():
    # The harness must route the base-rate null through _ict_offline with MC>=5000.
    n, o, h, l, c = _pool_sweep_fixture()
    h[11] = 21.0
    b = _bars(o, h, l, c)
    res = HD.compute_rates(b, pv_len=3, disp_mlt=1.5, atr_len=14, draw_k=10)
    dists = res["BSL"]["pool"]["distances"]
    if len(dists) == 0:
        return  # nothing to test on this side
    base, ci = HD.pool_base_rate(b, res["BSL"]["pool"], side="BSL",
                                 draw_k=10, B=5000, seed=1)
    assert 0.0 <= base <= 1.0
    assert ci[0] <= ci[1]


def test_base_rate_mc_floor_enforced():
    n, o, h, l, c = _pool_sweep_fixture()
    h[11] = 21.0
    b = _bars(o, h, l, c)
    res = HD.compute_rates(b, pv_len=3, disp_mlt=1.5, atr_len=14, draw_k=10)
    pool = res["BSL"]["pool"]
    if len(pool["distances"]) == 0:
        return
    try:
        HD.pool_base_rate(b, pool, side="BSL", draw_k=10, B=100, seed=1)
    except ValueError as ex:
        assert "5000" in str(ex)
    else:
        raise AssertionError("MC floor (B>=5000) must be enforced (PREREG-D D-3)")


# =============================================================================
# D-4 SELECTIVITY GRID -- 9 cells, n-per-cell reported
# =============================================================================
def test_d4_grid_is_nine_cells_with_n():
    rng = np.random.default_rng(1)
    n = 80
    c = 100 + np.cumsum(rng.normal(0, 1, n))
    h = c + rng.uniform(0.5, 2.5, n)
    l = c - rng.uniform(0.5, 2.5, n)
    o = c + rng.normal(0, 0.3, n)
    b = _bars(o, h, l, c)
    grid = HD.selectivity_grid(b, draw_k=10, atr_len=14)
    # dispMlt {0,1.5,3.0} x pvLen {2,3,5} = 9 cells
    assert len(grid) == 9
    for cell in grid:
        assert "disp_mlt" in cell and "pv_len" in cell
        # every cell reports n-per-cell per side/object
        assert "BSL" in cell and "SSL" in cell
        assert "n" in cell["BSL"]["pool"]
    cells = {(cell["disp_mlt"], cell["pv_len"]) for cell in grid}
    assert cells == {(d, p) for d in (0.0, 1.5, 3.0) for p in (2, 3, 5)}


# =============================================================================
# TWO-PROPORTION DIFF CI on poolRate - fvgRate (per side, via _ict_offline)
# =============================================================================
def test_two_prop_diff_wraps_offline():
    side_res = {"pool": dict(hits=80, n=100), "fvg": dict(hits=50, n=100)}
    diff, lo, hi = HD.pool_minus_fvg_ci(side_res, B=5000, seed=2)
    approx(diff, 0.30, tol=1e-9)
    assert lo < 0.30 < hi


# =============================================================================
# LOADER -- malformed BAR_EXPORT Entry rows are reported (R4-5), not silent
# =============================================================================
def test_loader_reports_dropped_bar_export_rows(tmp_path, capsys):
    # R4-5: a mixed good/garbled-Signal BAR_EXPORT fixture must load the good rows
    # AND print a loud WARN naming the drop count (mirrors core/bar_export_loader).
    day = 86_400_000
    start = 1_700_000_000_000
    good = [
        f"{start + 0 * day}|10.0|10.5|9.5|10.0|100",
        f"{start + 1 * day}|10.1|10.6|9.6|10.1|100",
        f"{start + 2 * day}|10.2|10.7|9.7|10.2|100",
    ]
    garbled = [
        "not-a-bar-export-signal",          # no pipes
        f"{start + 3 * day}|10.3|10.8|9.8",  # too few fields
        f"{start + 4 * day}|10.4|10.9|9.9|10.4|1.5",  # non-integer volume (must NOT decode)
    ]
    rows = ["Type,Signal"]
    for s in good + garbled:
        rows.append(f"Entry long,{s}")
    csv_path = tmp_path / "mixed_bar_export.csv"
    csv_path.write_text("\n".join(rows) + "\n", encoding="utf-8")

    b = HD.load_daily_ohlc(csv_path)
    captured = capsys.readouterr()
    # the 3 good rows load; the 3 garbled rows are dropped and reported.
    assert b.n == 3, "the 3 well-formed Entry rows must load"
    msg = (captured.err + captured.out).lower()
    assert "3" in (captured.err + captured.out), "the drop count (3) must be reported"
    assert "drop" in msg or "skip" in msg or "warn" in msg, \
        "a loud WARN naming the dropped rows must be printed (R4-5)"


# =============================================================================
# main() SKIPS cleanly when the real export is absent
# =============================================================================
def test_main_skips_when_export_absent(capsys):
    rc = HD.main(csv_path=Path("does_not_exist_anywhere_xyz.csv"))
    out = capsys.readouterr().out
    assert rc == 0
    assert "no export" in out.lower() or "skip" in out.lower()
    # it must name the export it needs
    assert "Daily" in out or "daily" in out or ".csv" in out


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for fn in fns:
        try:
            try:
                fn()
            except TypeError:
                fn(_CapsysShim())  # for the capsys test when run standalone
            print(f"PASS {fn.__name__}")
            passed += 1
        except AssertionError as ex:
            print(f"FAIL {fn.__name__}: {ex}")
        except Exception as ex:
            print(f"ERROR {fn.__name__}: {type(ex).__name__}: {ex}")
    print(f"\n{passed}/{len(fns)} passed")


class _CapsysShim:
    """Minimal capsys stand-in for standalone __main__ runs."""
    def readouterr(self):
        import types
        return types.SimpleNamespace(out="", err="")
