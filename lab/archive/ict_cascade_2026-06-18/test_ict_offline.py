"""Unit tests for _ict_offline.py -- the SHARED detector + statistics module.

TDD for Q-ICT-CASCADE-1. All fixtures are hand-verified, synthetic, and built
in-test: NO external export is touched, so these pass NOW with no vendor data.

Run directly (the repo default `pytest tests/` does NOT collect lab/):
    python -m pytest lab/analysis/ict_cascade_2026-06-18/test_ict_offline.py -q
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ict_offline as M  # noqa: E402


def approx(a, b, tol=1e-9):
    assert abs(a - b) < tol, f"{a} != {b}"


# =============================================================================
# B1 ORIENTATION FIXTURE (TEST_PLAN B1, worked example line 141)
# =============================================================================
def test_b1_bull_fvg_orientation():
    # bull-displacement 3-bar: high[i-2]=100.0, low[i]=100.5 => bull_fvg TRUE.
    # bar i=2: [0]=i=2 (current), [2]=i-2=0 (two back). Middle bar 1 arbitrary.
    o = [99.5, 100.2, 100.6]
    h = [100.0, 100.8, 100.9]   # high[0]=100.0 (two-back), high[2] arbitrary
    l = [99.4, 100.1, 100.5]    # low[2]=100.5 (current, NEAR)
    c = [99.9, 100.5, 100.7]
    assert M.bull_fvg(o, h, l, c, 2) is True
    top, bot = M.bull_bounds(o, h, l, c, 2)
    approx(top, 100.5)   # NEAR = low[i]
    approx(bot, 100.0)   # FAR  = high[i-2]
    assert top > bot     # NEAR above FAR for a bull gap


def test_b1_no_gap_fixture():
    # low[i]=100.0 NOT > high[i-2]=100.0 -> no bull FVG (strict >).
    o = [99.5, 100.0, 99.8]
    h = [100.0, 100.5, 100.4]
    l = [99.4, 99.7, 100.0]     # low[2]=100.0 == high[0]=100.0 -> not strictly greater
    c = [99.9, 100.2, 100.2]
    assert M.bull_fvg(o, h, l, c, 2) is False


def test_b1_bear_fvg_orientation():
    # bearish: high[i]=99.5 < low[i-2]=100.0 -> bear_fvg TRUE.
    # bear_bounds: top=low[i-2]=100.0, bot=high[i]=99.5; NEAR edge (bot) reached
    # from above first.
    o = [100.4, 99.9, 99.4]
    h = [100.6, 100.0, 99.5]    # high[2]=99.5 (current)
    l = [100.0, 99.6, 99.3]     # low[0]=100.0 (two-back)
    c = [100.2, 99.7, 99.4]
    assert M.bear_fvg(o, h, l, c, 2) is True
    top, bot = M.bear_bounds(o, h, l, c, 2)
    approx(top, 100.0)   # FAR  = low[i-2]
    approx(bot, 99.5)    # NEAR = high[i]
    assert top > bot


def test_b1_body_basis():
    # body bull: min(o[i],c[i]) > max(o[i-2],c[i-2]).
    o = [99.5, 100.2, 100.7]    # max(o[0],c[0]) = max(99.5,99.9)=99.9
    h = [101.0, 100.8, 101.0]
    l = [99.0, 100.1, 100.3]
    c = [99.9, 100.5, 100.6]    # min(o[2],c[2]) = min(100.7,100.6)=100.6 > 99.9
    assert M.bull_fvg(o, h, l, c, 2, use_body=True) is True
    top, bot = M.bull_bounds(o, h, l, c, 2, use_body=True)
    approx(top, 100.6)   # min(o[i],c[i])
    approx(bot, 99.9)    # max(o[i-2],c[i-2])


# =============================================================================
# D-1 SELF-TOUCH GUARD (lib DRAFT L128; TEST_PLAN B3 D-1)
# =============================================================================
def test_d1_guard_no_touch_on_registration_bar():
    # A bull FVG registered at bar 5 with top(NEAR)=100.0. On its OWN bar 5 the
    # low dips to 99.9 (<= top) -- but the D-1 guard requires barIdx > f.bar, so
    # NO touch is recorded.
    fvgs = [M.make_fvg(top=100.0, bot=99.5, bar=5, bull=True)]
    M.mark_touched(fvgs, hi=100.2, lo=99.9, bar_idx=5)
    assert fvgs[0]["touched"] is False, "touch on registration bar must NOT count (D-1)"


def test_d1_guard_touch_on_later_bar():
    fvgs = [M.make_fvg(top=100.0, bot=99.5, bar=5, bull=True)]
    M.mark_touched(fvgs, hi=100.2, lo=99.9, bar_idx=6)   # strictly later
    assert fvgs[0]["touched"] is True
    assert fvgs[0]["touchedBar"] == 6


def test_d1_preguard_would_pin_100pct():
    # The bug this fix addresses: WITHOUT the guard, every FVG self-touches on its
    # registration bar (the near edge IS the current-bar extreme), pinning ~100%.
    # We emulate the pre-guard behavior to assert the fix changes the answer.
    def mark_touched_NO_GUARD(fvgs, hi, lo, bar_idx):
        for f in fvgs:
            if f["touched"]:
                continue
            if f["bull"] and lo <= f["top"]:
                f["touched"] = True
            if (not f["bull"]) and hi >= f["bot"]:
                f["touched"] = True

    # 20 bull FVGs, each self-touched on its own registration bar (low==top).
    fvgs = [M.make_fvg(top=100.0 + i, bot=99.5 + i, bar=i, bull=True) for i in range(20)]
    for i in range(20):
        mark_touched_NO_GUARD([fvgs[i]], hi=101.0 + i, lo=100.0 + i, bar_idx=i)
    pre = sum(f["touched"] for f in fvgs) / len(fvgs)
    approx(pre, 1.0)   # pre-guard pins ~100%

    # Same fixture WITH the guard: none touch on their own bar -> 0%.
    fvgs2 = [M.make_fvg(top=100.0 + i, bot=99.5 + i, bar=i, bull=True) for i in range(20)]
    for i in range(20):
        M.mark_touched([fvgs2[i]], hi=101.0 + i, lo=100.0 + i, bar_idx=i)
    post = sum(f["touched"] for f in fvgs2) / len(fvgs2)
    approx(post, 0.0)
    assert post < pre


def test_d1_bear_guard():
    # bear near edge = bot (high>=bot). Self-touch on registration bar excluded.
    fvgs = [M.make_fvg(top=100.5, bot=100.0, bar=3, bull=False)]
    M.mark_touched(fvgs, hi=100.1, lo=99.8, bar_idx=3)
    assert fvgs[0]["touched"] is False
    M.mark_touched(fvgs, hi=100.1, lo=99.8, bar_idx=4)
    assert fvgs[0]["touched"] is True


# =============================================================================
# DISPLACEMENT (lib L71-73, measured on the middle candle i-1)
# =============================================================================
def test_displacement_true_false_around_threshold():
    # middle candle (i-1) range vs mult*atr. atr=1.0, mult=1.5 -> threshold 1.5.
    o = [0.0, 10.0, 0.0]
    c = [0.0, 10.0, 0.0]
    # range just above threshold (wick basis: high[1]-low[1])
    h = [0.0, 11.6, 0.0]; l = [0.0, 10.0, 0.0]   # rng = 1.6 > 1.5 -> True
    assert M.displacement(o, h, l, c, 2, atr_val=1.0, mult=1.5) is True
    h2 = [0.0, 11.4, 0.0]; l2 = [0.0, 10.0, 0.0]  # rng = 1.4 < 1.5 -> False
    assert M.displacement(o, h2, l2, c, 2, atr_val=1.0, mult=1.5) is False
    # exact boundary rng == 1.5 -> NOT displacement (strict >)
    h3 = [0.0, 11.5, 0.0]; l3 = [0.0, 10.0, 0.0]
    assert M.displacement(o, h3, l3, c, 2, atr_val=1.0, mult=1.5) is False


def test_displacement_na_atr():
    assert M.displacement([0, 0, 0], [0, 5, 0], [0, 0, 0], [0, 0, 0],
                          2, atr_val=float("nan"), mult=1.5) is False


# =============================================================================
# PD ZONE (lib L202-207)
# =============================================================================
def test_pd_zone_premium_discount_eq():
    # range 0..100 -> eq=50, half=50, eqBand=0.05 -> band=2.5.
    z, eq = M.pd_zone(100.0, 0.0, 60.0, 0.05)
    assert z == 1 and eq == 50.0          # 60 > 52.5 -> premium
    z, eq = M.pd_zone(100.0, 0.0, 40.0, 0.05)
    assert z == -1                         # 40 < 47.5 -> discount
    z, eq = M.pd_zone(100.0, 0.0, 50.0, 0.05)
    assert z == 0                          # exact EQ -> 0
    z, eq = M.pd_zone(100.0, 0.0, 51.0, 0.05)
    assert z == 0                          # inside band -> 0


def test_pd_zone_eqband_boundary_strict():
    # px exactly at eq + band = 52.5 -> NOT premium (strict >); just above -> premium.
    z, _ = M.pd_zone(100.0, 0.0, 52.5, 0.05)
    assert z == 0
    z, _ = M.pd_zone(100.0, 0.0, 52.5001, 0.05)
    assert z == 1
    # lower boundary
    z, _ = M.pd_zone(100.0, 0.0, 47.5, 0.05)
    assert z == 0
    z, _ = M.pd_zone(100.0, 0.0, 47.4999, 0.05)
    assert z == -1


def test_pd_zone_zero_band():
    # eqBand=0 -> band=0; only exact eq is 0, everything else +/-1.
    z, _ = M.pd_zone(100.0, 0.0, 50.0, 0.0)
    assert z == 0
    z, _ = M.pd_zone(100.0, 0.0, 50.0001, 0.0)
    assert z == 1


# =============================================================================
# DOL (lib L215-223)
# =============================================================================
def test_dol_nearest():
    assert M.dol(5.0, 10.0) == 1      # up nearer -> draw up
    assert M.dol(10.0, 5.0) == -1     # down nearer -> draw down
    assert M.dol(7.0, 7.0) == 0       # tie
    assert M.dol(np.nan, 5.0) == -1   # only down
    assert M.dol(5.0, np.nan) == 1    # only up
    assert M.dol(np.nan, np.nan) == 0


# =============================================================================
# WILDER ATR (vs a hand-computed small series)
# =============================================================================
def test_wilder_atr_hand_computed():
    # length=3. Build TR by hand. TV ta.atr = ta.rma(ta.tr(true), len) and
    # ta.tr(true) defines the FIRST-bar true range as high[0]-low[0] (NOT nan).
    # So TR[0] = high[0]-low[0] = 1.0 and the RMA seed averages `length` (=3)
    # values INCLUDING TR[0], matching TV ta.atr on every bar.
    high = np.array([10.0, 11.0, 12.0, 11.5, 12.5])
    low = np.array([9.0, 10.0, 11.0, 10.5, 11.5])
    close = np.array([9.5, 10.5, 11.5, 11.0, 12.0])
    # TR: bar0 = high[0]-low[0] = 10.0-9.0 = 1.0  (TV ta.tr(true) first-bar rule)
    # bar1: max(11-10=1.0, |11-9.5|=1.5, |10-9.5|=0.5) = 1.5
    # bar2: max(12-11=1.0, |12-10.5|=1.5, |11-10.5|=0.5) = 1.5
    # bar3: max(11.5-10.5=1.0, |11.5-11.5|=0, |10.5-11.5|=1.0) = 1.0
    # bar4: max(12.5-11.5=1.0, |12.5-11.0|=1.5, |11.5-11.0|=0.5) = 1.5
    # Wilder RMA length 3: seed at idx2 = mean(TR[0:3]) = mean([1.0,1.5,1.5]) = 4.0/3
    seed = (1.0 + 1.5 + 1.5) / 3.0
    # idx3 = (TR3 + 2*seed)/3 = (1.0 + 2*seed)/3
    v3 = (1.0 + 2 * seed) / 3.0
    v4 = (1.5 + 2 * v3) / 3.0
    atr = M.wilder_atr(high, low, close, length=3)
    assert np.isnan(atr[0]) and np.isnan(atr[1])
    # ATR[length-1] is pinned to the TV-faithful seed (tr[0]=high-low included).
    approx(atr[2], seed)
    approx(atr[2], 4.0 / 3.0)
    approx(atr[3], v3)
    approx(atr[4], v4)


def test_wilder_atr_first_tr_is_high_minus_low():
    # R1-1/R1-2/R4-4 regression: TV ta.tr(true) sets the FIRST bar's true range to
    # high[0]-low[0] (finite), NOT nan. length=1 collapses ATR[0] to that TR[0].
    high = np.array([10.0, 11.0, 12.0])
    low = np.array([9.0, 10.0, 11.0])
    close = np.array([9.5, 10.5, 11.5])
    atr = M.wilder_atr(high, low, close, length=1)
    # length=1: ATR[0] = TR[0] = high[0]-low[0] = 1.0 (must be finite, not nan).
    assert not np.isnan(atr[0])
    approx(atr[0], 1.0)


# =============================================================================
# PIVOTS (TV ta.pivothigh/low confirm-lag; pivot bar = t, registered at t+right)
# =============================================================================
def test_pivot_high_confirm_lag():
    # left=right=2. A clean peak at t=4.
    high = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 4.0, 3.0, 2.0, 1.0])
    piv = M.pivot_high(high, 2, 2)
    bars = [t for t, _ in piv]
    assert 4 in bars                  # peak at index 4 (=5.0)
    # the pivot BAR is t=4 (true extreme), not the registration bar t+right=6
    px = dict(piv)[4]
    approx(px, 5.0)


def test_pivot_low_confirm_lag():
    low = np.array([5.0, 4.0, 3.0, 2.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    piv = M.pivot_low(low, 2, 2)
    bars = [t for t, _ in piv]
    assert 4 in bars
    approx(dict(piv)[4], 1.0)


def test_pivot_high_strict_no_plateau():
    # flat plateau -> no strict pivot (TV strictness).
    high = np.array([1.0, 2.0, 3.0, 3.0, 3.0, 2.0, 1.0])
    piv = M.pivot_high(high, 2, 2)
    assert all(t not in (2, 3, 4) for t, _ in piv) or len(piv) == 0


def test_pools_from_pivots_bar_is_true_pivot():
    # pvLen=2; peak at index 4 -> pool.bar must be 4 (the TRUE pivot bar).
    high = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 4.0, 3.0, 2.0, 1.0])
    low = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    pools = M.pools_from_pivots(high, low, 2)
    bsl = [p for p in pools if p["buyside"]]
    assert any(p["bar"] == 4 and abs(p["price"] - 5.0) < 1e-9 for p in bsl)


# =============================================================================
# DETECT RAID (lib L90-109)
# =============================================================================
def test_detect_raid_bsl_ssl():
    pools = [M.make_pool(price=105.0, bar=1, buyside=True),
             M.make_pool(price=95.0, bar=2, buyside=False)]
    rb, rs = M.detect_raid(pools, hi=106.0, lo=104.0, bar_idx=10)   # high sweeps BSL
    assert rb is True and rs is False
    assert pools[0]["swept"] and pools[0]["sweptBar"] == 10
    rb, rs = M.detect_raid(pools, hi=96.0, lo=94.0, bar_idx=11)     # low sweeps SSL
    assert rs is True
    assert pools[1]["swept"] and pools[1]["sweptBar"] == 11


# =============================================================================
# NEAREST OBJECT DISTANCES (lib L152-194)
# =============================================================================
def test_nearest_pool_distances():
    pools = [M.make_pool(110.0, 1, True), M.make_pool(120.0, 2, True),
             M.make_pool(90.0, 3, False)]
    approx(M.nearest_pool(pools, 100.0, above=True), 10.0)   # 110 nearest above
    approx(M.nearest_pool(pools, 100.0, above=False), 10.0)  # 90 nearest below
    # swept pool ignored
    pools[0]["swept"] = True
    approx(M.nearest_pool(pools, 100.0, above=True), 20.0)
    approx(M.nearest_pool_px(pools, 100.0, above=True), 120.0)


# =============================================================================
# MOVING-BLOCK BOOTSTRAP CI (coverage on a known iid series)
# =============================================================================
def test_mbb_ci_brackets_mean_iid():
    rng = np.random.default_rng(0)
    x = rng.normal(0.0, 1.0, size=500)
    lo, hi = M.moving_block_bootstrap_ci(x, block_len=1, B=2000, seed=1)
    assert lo < x.mean() < hi
    # CI should be reasonably tight around the sample mean for n=500
    assert (hi - lo) < 0.5


def test_mbb_ci_binary_rate():
    # a clearly-above-0.5 binary series: CI lower bound should exceed 0.5.
    x = np.array([1] * 80 + [0] * 20, float)   # rate 0.80
    lo, hi = M.moving_block_bootstrap_ci(x, block_len=2, B=3000, seed=7)
    assert lo > 0.5 and hi <= 1.0
    assert lo < 0.80 < hi


def test_mbb_ci_empty():
    lo, hi = M.moving_block_bootstrap_ci(np.array([]), 2, 100, 0)
    assert np.isnan(lo) and np.isnan(hi)


# =============================================================================
# AUTOCORR BLOCK LENGTH (AR(1) -> longer block; white noise -> floor)
# =============================================================================
def test_autocorr_block_len_white_noise_is_floor():
    rng = np.random.default_rng(3)
    x = rng.normal(size=2000)
    L = M.autocorr_block_len(x, cutoff=0.10, floor=1, cap=8)
    assert L == 1     # white noise: lag-1 autocorr ~0 < 0.10 -> floor


def test_autocorr_block_len_ar1_is_longer():
    rng = np.random.default_rng(5)
    n = 4000
    phi = 0.7
    e = rng.normal(size=n)
    x = np.empty(n)
    x[0] = e[0]
    for i in range(1, n):
        x[i] = phi * x[i - 1] + e[i]
    L = M.autocorr_block_len(x, cutoff=0.10, floor=1, cap=8)
    # AR(1) phi=0.7: autocorr at lag k ~ 0.7^k; drops below 0.10 at k where
    # 0.7^k < 0.10 -> k ~ 6.5 -> 7. Clamped to cap 8.
    assert 2 <= L <= 8
    assert L > 1


def test_autocorr_block_len_constant_is_floor():
    assert M.autocorr_block_len(np.ones(50), cutoff=0.10, floor=1, cap=8) == 1


def test_autocorr_block_len_cap():
    # strong long-memory: a ramp has autocorr ~1 for many lags -> hits cap.
    x = np.arange(200, dtype=float)
    L = M.autocorr_block_len(x, cutoff=0.10, floor=1, cap=8)
    assert L == 8


def test_autocorr_block_len_short_series_not_cap():
    # R2-1 regression: a length-truncated scan (n-1 < cap) that never drops below
    # cutoff must NOT charge cap (asserting memory the data could not evidence).
    # n=2 -> max_lag = min(8, 1) = 1; one persistent lag -> collapse to floor (1),
    # NOT cap (8).
    L = M.autocorr_block_len([1.0, 2.0], cutoff=0.10, floor=1, cap=8)
    assert L == 1, f"length-truncated persistent scan must not charge cap; got {L}"


def test_autocorr_block_len_genuine_persistence_reaches_cap():
    # A genuinely-persistent series with enough length (n >= 9 so a FULL cap-length
    # scan is possible) still returns up to cap when autocorr stays >= cutoff.
    x = np.arange(50, dtype=float)   # ramp: autocorr ~1 across all scanned lags
    L = M.autocorr_block_len(x, cutoff=0.10, floor=1, cap=8)
    assert L == 8


# =============================================================================
# MAX-STAT LABEL PERMUTATION (PREREG-W GC-3)
# =============================================================================
def test_max_stat_permutation_null_is_large():
    # 4 inputs, all pure noise: observed_max should NOT be significant.
    # per_input_stat_fn returns a random N(0,1) "permuted statistic".
    def stat_fn(j, rng):
        return rng.normal()
    # observed_max set to the median of a max-of-4 normal (~0.7) -> p ~ 0.5-ish, large.
    p = M.max_stat_label_permutation(stat_fn, n_inputs=4, observed_max=0.7,
                                     B=2000, seed=11)
    assert p > 0.10   # not significant


def test_max_stat_permutation_strong_signal_small_p():
    def stat_fn(j, rng):
        return rng.normal()
    # observed_max far in the tail -> very small p.
    p = M.max_stat_label_permutation(stat_fn, n_inputs=4, observed_max=6.0,
                                     B=2000, seed=12)
    assert p < 0.01


def test_max_stat_permutation_p_bounded():
    def stat_fn(j, rng):
        return rng.normal()
    p = M.max_stat_label_permutation(stat_fn, 4, observed_max=-100.0, B=100, seed=1)
    assert 0.0 < p <= 1.0   # add-one keeps p > 0 even when everything exceeds


# =============================================================================
# DROP-TOP-K
# =============================================================================
def test_drop_top_k():
    v = [1.0, 2.0, 3.0, 10.0]
    approx(M.drop_top_k(v, 0), 4.0)          # mean of all = 16/4
    approx(M.drop_top_k(v, 1), 2.0)          # drop 10 -> mean(1,2,3)=2
    approx(M.drop_top_k(v, 2), 1.5)          # drop 10,3 -> mean(1,2)=1.5
    assert np.isnan(M.drop_top_k(v, 4))      # drop all -> nan
    assert np.isnan(M.drop_top_k([], 0))


# =============================================================================
# TWO-PROPORTION DIFF CI (PREREG-D)
# =============================================================================
def test_two_proportion_diff_ci():
    # p1=0.8 (80/100), p2=0.5 (50/100). diff = +0.30; CI should exclude 0.
    diff, lo, hi = M.two_proportion_diff_ci(80, 100, 50, 100, B=5000, seed=2)
    approx(diff, 0.30, tol=1e-9)
    assert lo > 0.0 and hi < 0.6
    assert lo < 0.30 < hi


def test_two_proportion_diff_ci_zero_n():
    diff, lo, hi = M.two_proportion_diff_ci(0, 0, 5, 10, B=100, seed=0)
    assert np.isnan(diff)


# =============================================================================
# RADIUS-MATCHED BASE RATE (PREREG-D D-3)
# =============================================================================
def test_radius_matched_distance_zero_always_drawn():
    # a level at distance 0 is ALWAYS drawn to (price is already there).
    # price_path_fn: drawn-to iff distance <= some reach; here reach=0 strict,
    # but distance 0 must be "drawn to" -> use <= so 0 hits.
    def path_fn(dist):
        return dist <= 0.0   # only distance-0 levels reached
    base, (lo, hi) = M.radius_matched_base_rate(
        distances_real=np.zeros(50), price_path_fn=path_fn, K=10, B=5000, seed=1)
    approx(base, 1.0)
    approx(lo, 1.0)
    approx(hi, 1.0)


def test_radius_matched_partial_reach():
    # distances uniform in [0, 10]; reach = 5 -> ~half are drawn to.
    rng = np.random.default_rng(0)
    d = rng.uniform(0.0, 10.0, size=400)

    def path_fn(dist):
        return dist <= 5.0
    base, (lo, hi) = M.radius_matched_base_rate(d, path_fn, K=10, B=5000, seed=4)
    assert 0.4 < base < 0.6           # ~50%
    assert lo < base < hi


def test_radius_matched_enforces_mc_floor():
    try:
        M.radius_matched_base_rate(np.zeros(10), lambda d: True, K=10, B=100, seed=0)
    except ValueError as ex:
        assert "5000" in str(ex)
    else:
        raise AssertionError("expected ValueError for B<5000 (PREREG-D D-3)")


def test_radius_matched_empty():
    base, (lo, hi) = M.radius_matched_base_rate([], lambda d: True, K=10, B=5000, seed=0)
    assert np.isnan(base)


# =============================================================================
# ET FIELDS (UTC epoch -> America/New_York, DST-aware)
# =============================================================================
def test_et_fields_dst_aware():
    # 2026-06-18 13:00:00 UTC -> EDT (UTC-4) = 09:00 ET, Thursday (dow=3).
    # epoch ms for 2026-06-18T13:00:00Z:
    import pandas as pd
    ms = int(pd.Timestamp("2026-06-18T13:00:00Z").value // 1_000_000)
    hh, mm, dow, date = M.et_fields(ms)
    assert hh[0] == 9 and mm[0] == 0
    assert dow[0] == 3            # Thursday (Mon=0)
    assert str(date[0]) == "2026-06-18"


def test_et_fields_winter_est():
    # 2026-01-15 14:30:00 UTC -> EST (UTC-5) = 09:30 ET, Thursday.
    import pandas as pd
    ms = int(pd.Timestamp("2026-01-15T14:30:00Z").value // 1_000_000)
    hh, mm, dow, date = M.et_fields(ms)
    assert hh[0] == 9 and mm[0] == 30
    assert str(date[0]) == "2026-01-15"


def test_et_fields_array():
    import pandas as pd
    ms = [int(pd.Timestamp("2026-06-18T13:00:00Z").value // 1_000_000),
          int(pd.Timestamp("2026-06-18T20:00:00Z").value // 1_000_000)]
    hh, mm, dow, date = M.et_fields(ms)
    assert hh[0] == 9 and hh[1] == 16   # 13Z->09 ET, 20Z->16 ET


# =============================================================================
# ROLLING EXTREMES
# =============================================================================
def test_rolling_extremes():
    arr = np.array([3.0, 1.0, 4.0, 1.0, 5.0, 9.0])
    h = M.highest(arr, 3)
    l = M.lowest(arr, 3)
    assert np.isnan(h[0]) and np.isnan(h[1])
    approx(h[2], 4.0); approx(h[5], 9.0)
    approx(l[2], 1.0); approx(l[4], 1.0)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for fn in fns:
        try:
            fn(); print(f"PASS {fn.__name__}"); passed += 1
        except AssertionError as ex:
            print(f"FAIL {fn.__name__}: {ex}")
        except Exception as ex:
            print(f"ERROR {fn.__name__}: {type(ex).__name__}: {ex}")
    print(f"\n{passed}/{len(fns)} passed")
