"""SHARED offline detector + statistics module for Q-ICT-CASCADE-1.

This is the single source of truth that the W / D / 1H / 1M harnesses import. It
does two jobs:

  1. DETECTORS -- a faithful numpy port of the CONSTELLATION ICT core primitives
     (`constellation_ict_lib_DRAFT.pine`, bytes 10587, LastWriteUTC
     2026-06-18T22:42:47Z). The Pine uses bar-offset indexing [0]=current /
     [1]=mid / [2]=two-back; this port operates on numpy OHLC arrays indexed by
     absolute bar i, so the offset map is:
         Pine [0] -> arr[i]      (current bar)
         Pine [1] -> arr[i-1]    (middle candle)
         Pine [2] -> arr[i-2]    (two bars back)
     Every detector below cites the lib DRAFT line range it ports.

  2. STATISTICS -- the campaign's pre-registered methods (moving-block bootstrap,
     autocorr block-length rule, max-stat label permutation, drop-top-k,
     two-proportion diff CI, radius-matched base rate, ET timezone fields).
     Each cites the PREREG it serves: PREREG-W (GC-1/GC-2/GC-3), PREREG-D
     (D-3 radius-match + n-floor blocks), PREREG-1H (de-overlap / placebo).

Conventions (all PREREGs + repo): look-ahead-free, PnL net of cost / R-denominated
(consumers), ET = America/New_York (DST-aware), TV BAR_EXPORT epoch is UTC ->
convert UTC->ET for sessions/DOW. ASCII only. No external data is read here; the
real-export entrypoints live in the per-layer harnesses and must skip cleanly when
the export is absent.

Rule-0 source (gitignored, outside the repo, read verbatim this session):
  C:/Users/joshu/Downloads/constellation_ict_lib_DRAFT.pine
  bytes 10587 / LastWriteUTC 2026-06-18T22:42:47Z
A resuming session MUST re-anchor (Downloads is mutable; line numbers drift).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

ET = "America/New_York"

# =============================================================================
# SECTION 1 -- DETECTORS (numpy port of constellation_ict_lib_DRAFT.pine)
# =============================================================================

# ----------------------------------------------------------------------------
# FVG DETECTION -- three-candle inefficiency. Standard ICT (BISI/SIBI).
# Pine lib L45-53. At bar i: Pine [0]=i, [2]=i-2.
#   bull (wick): low[0] > high[2]              -> arr: low[i] > high[i-2]
#   bull (body): min(open[0],close[0]) > max(open[2],close[2])
#   bear symmetric.
# B1 worked example (TEST_PLAN B1 / line 141): high[i-2]=100.0, low[i]=100.5
#   => bull_fvg = (100.5 > 100.0) = TRUE.
# ----------------------------------------------------------------------------
def bull_fvg(o, h, l, c, i, use_body=False):
    """Bullish FVG at bar i (lib L45-48). i>=2 required."""
    if i < 2:
        return False
    if use_body:
        upper2 = max(o[i - 2], c[i - 2])
        lower0 = min(o[i], c[i])
    else:
        upper2 = h[i - 2]
        lower0 = l[i]
    return bool(lower0 > upper2)


def bear_fvg(o, h, l, c, i, use_body=False):
    """Bearish FVG at bar i (lib L50-53). i>=2 required."""
    if i < 2:
        return False
    if use_body:
        lower2 = min(o[i - 2], c[i - 2])
        upper0 = max(o[i], c[i])
    else:
        lower2 = l[i - 2]
        upper0 = h[i]
    return bool(upper0 < lower2)


def bull_bounds(o, h, l, c, i, use_body=False):
    """Bull FVG bounds at bar i (lib L56-59). Returns (top, bot).

    top = low[0]  -> NEAR edge (= arr low[i])
    bot = high[2] -> FAR  edge (= arr high[i-2])
    B1 worked example: top = 100.5 (NEAR), bot = 100.0 (FAR).
    """
    if use_body:
        top = min(o[i], c[i])
        bot = max(o[i - 2], c[i - 2])
    else:
        top = l[i]
        bot = h[i - 2]
    return float(top), float(bot)


def bear_bounds(o, h, l, c, i, use_body=False):
    """Bear FVG bounds at bar i (lib L61-64). Returns (top, bot).

    top = low[2]  (= arr low[i-2]); bot = high[0] (= arr high[i]).
    For a bear FVG the NEAR edge (first reached from below) is `bot` = high[i],
    and the FAR edge is `top` = low[i-2] (consumer markTouched uses hi>=f.bot).
    """
    if use_body:
        top = min(o[i - 2], c[i - 2])
        bot = max(o[i], c[i])
    else:
        top = l[i - 2]
        bot = h[i]
    return float(top), float(bot)


# ----------------------------------------------------------------------------
# DISPLACEMENT -- energetic candle that printed the gap (lib L71-73).
# Measured on the MIDDLE candle [1] == arr index i-1.
#   rng = use_body ? abs(close[1]-open[1]) : (high[1]-low[1])
#   displacement = rng > mult * atr_val      (na atr -> False)
# ----------------------------------------------------------------------------
def displacement(o, h, l, c, i, atr_val, mult, use_body=False):
    """Displacement on the middle candle (lib L71-73). i>=1 required."""
    if i < 1 or atr_val is None or (isinstance(atr_val, float) and np.isnan(atr_val)):
        return False
    if use_body:
        rng = abs(c[i - 1] - o[i - 1])
    else:
        rng = h[i - 1] - l[i - 1]
    return bool(rng > mult * atr_val)


# ----------------------------------------------------------------------------
# PIVOTS -- == TV ta.pivothigh / ta.pivotlow.
# A pivot at bar t is confirmed `right` bars later (registered at t+right). The
# pivot BAR index returned is t (the true extreme bar), NOT the registration bar.
# Strict comparison both sides (TV convention: strictly greater/less).
# Returns a list of (pivot_bar_t, price). lib consumers register at t = bar_index
# - pvLen (lib L78 pushPool + daily L43), i.e. registration bar minus `right`.
# ----------------------------------------------------------------------------
def pivot_high(high, left, right):
    """TV ta.pivothigh. Returns list of (t, price) for confirmed pivot highs."""
    high = np.asarray(high, float)
    n = len(high)
    out = []
    for t in range(left, n - right):
        v = high[t]
        if np.isnan(v):
            continue
        ok = True
        for k in range(1, left + 1):
            if not (high[t - k] < v):
                ok = False
                break
        if ok:
            for k in range(1, right + 1):
                if not (high[t + k] < v):
                    ok = False
                    break
        if ok:
            out.append((t, float(v)))
    return out


def pivot_low(low, left, right):
    """TV ta.pivotlow. Returns list of (t, price) for confirmed pivot lows."""
    low = np.asarray(low, float)
    n = len(low)
    out = []
    for t in range(left, n - right):
        v = low[t]
        if np.isnan(v):
            continue
        ok = True
        for k in range(1, left + 1):
            if not (low[t - k] > v):
                ok = False
                break
        if ok:
            for k in range(1, right + 1):
                if not (low[t + k] > v):
                    ok = False
                    break
        if ok:
            out.append((t, float(v)))
    return out


# ----------------------------------------------------------------------------
# POOL / FVG registries (light dataclasses-as-dicts; the lib uses Pine UDTs).
# A pool's `bar` is the TRUE pivot bar (lib L78 pushPool stores barIdx; the Daily
# consumer passes bar_index - pvLen, daily L43 -> pivot bar). detectRaid marks
# sweeps (lib L90-109): BSL swept when hi >= price; SSL when lo <= price.
# ----------------------------------------------------------------------------
def make_pool(price, bar, buyside):
    """Pool registry entry. buyside=True -> BSL (old high); False -> SSL (old low)."""
    return {"price": float(price), "bar": int(bar), "buyside": bool(buyside),
            "swept": False, "sweptBar": None}


def make_fvg(top, bot, bar, bull):
    """FVG registry entry. bar = registration bar (lib pushFVG / daily L51)."""
    return {"top": float(top), "bot": float(bot), "bar": int(bar), "bull": bool(bull),
            "touched": False, "touchedBar": None, "filled": False, "filledBar": None}


def pools_from_pivots(high, low, pv_len):
    """Build the Daily pool registry from confirmed pivots (lib L78 + daily L43/45).

    pool.bar = TRUE pivot bar = registration bar - pvLen. With ta.pivothigh/low
    left==right==pvLen, pivot_high/low already returns the true pivot bar t, so we
    register directly at t (no further subtraction -- the subtraction in the Pine
    converts registration bar -> t, which this offline port already gives).
    Returns list of pool dicts (BSL from highs, SSL from lows).
    """
    pools = []
    for t, px in pivot_high(high, pv_len, pv_len):
        pools.append(make_pool(px, t, True))
    for t, px in pivot_low(low, pv_len, pv_len):
        pools.append(make_pool(px, t, False))
    pools.sort(key=lambda p: p["bar"])
    return pools


def detect_raid(pools, hi, lo, bar_idx):
    """Mark pools swept on bar bar_idx (lib L90-109). Inclusive: BSL hi>=price,
    SSL lo<=price. Mutates pools in place; returns (raid_buy, raid_sell)."""
    raid_buy = False
    raid_sell = False
    for p in pools:
        if p["swept"]:
            continue
        if p["buyside"] and hi >= p["price"]:
            p["swept"] = True
            p["sweptBar"] = bar_idx
            raid_buy = True
        elif (not p["buyside"]) and lo <= p["price"]:
            p["swept"] = True
            p["sweptBar"] = bar_idx
            raid_sell = True
    return raid_buy, raid_sell


def mark_touched(fvgs, hi, lo, bar_idx):
    """Near-edge touch with the D-1 guard (lib DRAFT L121-134, L128 is the guard).

    A touch counts only at `barIdx > f.bar` -- a touch on the FVG's own
    registration bar is the gap FORMING, not a draw. Without this guard fvgRate is
    pinned ~100% (TEST_PLAN D-1). Bull near-edge: lo <= f.top. Bear near-edge:
    hi >= f.bot. Mutates fvgs in place.
    """
    for f in fvgs:
        if f["touched"]:
            continue
        if not (bar_idx > f["bar"]):       # D-1 guard (lib DRAFT L128)
            continue
        if f["bull"] and lo <= f["top"]:
            f["touched"] = True
            f["touchedBar"] = bar_idx
        if (not f["bull"]) and hi >= f["bot"]:
            f["touched"] = True
            f["touchedBar"] = bar_idx


def mark_filled(fvgs, hi, lo, bar_idx):
    """Far-edge fill (lib L136-146). Bull filled when lo<=f.bot; bear when hi>=f.top.
    No D-1 guard in the lib for fill (matches L140-145). Mutates fvgs in place."""
    for f in fvgs:
        if f["filled"]:
            continue
        if f["bull"] and lo <= f["bot"]:
            f["filled"] = True
            f["filledBar"] = bar_idx
        if (not f["bull"]) and hi >= f["top"]:
            f["filled"] = True
            f["filledBar"] = bar_idx


# ----------------------------------------------------------------------------
# NEAREST-OBJECT DISTANCES (lib L152-194). Positive distance to the nearest
# qualifying object on the requested side, or NaN.
# ----------------------------------------------------------------------------
def nearest_fvg(fvgs, px, above):
    """Nearest UNFILLED FVG mid on a side (lib L152-164). Returns positive dist or nan."""
    best = np.nan
    for f in fvgs:
        if f["filled"]:
            continue
        mid = (f["top"] + f["bot"]) / 2.0
        d = mid - px
        if above and d > 0:
            best = d if np.isnan(best) else min(best, d)
        if (not above) and d < 0:
            best = -d if np.isnan(best) else min(best, -d)
    return best


def nearest_pool(pools, px, above):
    """Nearest UNSWEPT pool on a side (lib L166-177). BSL above, SSL below.
    Returns positive distance or nan."""
    best = np.nan
    for p in pools:
        if p["swept"]:
            continue
        d = p["price"] - px
        if above and p["buyside"] and d > 0:
            best = d if np.isnan(best) else min(best, d)
        if (not above) and (not p["buyside"]) and d < 0:
            best = -d if np.isnan(best) else min(best, -d)
    return best


def nearest_pool_px(pools, px, above):
    """Price of the nearest unswept pool on a side (lib L180-194). nan if none."""
    best_px = np.nan
    best_d = np.nan
    for p in pools:
        if p["swept"]:
            continue
        d = p["price"] - px
        if above and p["buyside"] and d > 0 and (np.isnan(best_d) or d < best_d):
            best_d = d
            best_px = p["price"]
        if (not above) and (not p["buyside"]) and d < 0 and (np.isnan(best_d) or -d < best_d):
            best_d = -d
            best_px = p["price"]
    return best_px


# ----------------------------------------------------------------------------
# PREMIUM / DISCOUNT (lib L202-207). Returns (zone, eq).
#   zone +1 = premium (sell ctx), -1 = discount (buy ctx), 0 = equilibrium.
#   band = eqBand * half-range; px above eq+band -> +1, below eq-band -> -1.
#   Exact EQ (px==eq) -> 0. Boundary px == eq+band -> NOT premium (strict >).
# ----------------------------------------------------------------------------
def pd_zone(r_high, r_low, px, eq_band):
    """Premium/discount zone (lib L202-207). Returns (zone, eq)."""
    eq = (r_high + r_low) / 2.0
    half = (r_high - r_low) / 2.0
    band = eq_band * half
    if px > eq + band:
        zone = 1
    elif px < eq - band:
        zone = -1
    else:
        zone = 0
    return zone, float(eq)


# ----------------------------------------------------------------------------
# DRAW ON LIQUIDITY (lib L215-223). method 0 = NEAREST.
#   Returns +1 (draw up) / -1 (draw down) / 0 (no read).
#   up_dist / dn_dist are the POSITIVE nearest_* outputs combined per side.
# ----------------------------------------------------------------------------
def dol(up_dist, dn_dist, method=0):
    """Draw-on-liquidity bias from nearest-object distances (lib L215-223)."""
    up_na = up_dist is None or np.isnan(up_dist)
    dn_na = dn_dist is None or np.isnan(dn_dist)
    bias = 0
    if not up_na and not dn_na:
        if up_dist < dn_dist:
            bias = 1
        elif up_dist > dn_dist:
            bias = -1
        else:
            bias = 0
    elif not up_na:
        bias = 1
    elif not dn_na:
        bias = -1
    return bias


# ----------------------------------------------------------------------------
# WILDER ATR (Wilder RMA of true range == TV ta.atr). Matches usdcad_harness _rma.
# ----------------------------------------------------------------------------
def _rma(x, length):
    """Wilder RMA (== TV ta.atr smoothing). NaN warmup."""
    x = np.asarray(x, float)
    out = np.full_like(x, np.nan, dtype=float)
    if len(x) < length:
        return out
    seed = np.nanmean(x[:length])
    out[length - 1] = seed
    for i in range(length, len(x)):
        prev = out[i - 1]
        out[i] = (x[i] + (length - 1) * prev) / length if not np.isnan(prev) else x[i]
    return out


def wilder_atr(high, low, close, length=14):
    """ATR via Wilder RMA of true range (== TV ta.atr). NaN until bar length-1."""
    high = np.asarray(high, float)
    low = np.asarray(low, float)
    close = np.asarray(close, float)
    prev_c = np.concatenate([[np.nan], close[:-1]])
    tr = np.maximum(high - low, np.maximum(np.abs(high - prev_c), np.abs(low - prev_c)))
    # TV ta.tr(true) defines the FIRST-bar true range as high[0]-low[0] (there is no
    # prior close, so prev_c[0]=NaN propagates a NaN through np.maximum). Without
    # this, the RMA seed nanmean(tr[:length]) averages length-1 TRs and diverges
    # from TV ta.atr on every bar (and length=1 -> ATR[0]=NaN). Set tr[0] finite.
    if len(tr):
        tr[0] = high[0] - low[0]
    return _rma(tr, length)


# ----------------------------------------------------------------------------
# ROLLING extremes (for lookback-extremes ranges; NaN warmup). Excludes nothing
# by default -- the [1]-lag (exclude current) is the caller's shift, matching the
# 1H gate basis `ta.highest(high,lookN)[1]` (PREREG-1H DRAFT L65-66).
# ----------------------------------------------------------------------------
def highest(arr, n):
    """Rolling max over the trailing n bars INCLUSIVE of current (NaN warmup)."""
    return pd.Series(np.asarray(arr, float)).rolling(n).max().to_numpy()


def lowest(arr, n):
    """Rolling min over the trailing n bars INCLUSIVE of current (NaN warmup)."""
    return pd.Series(np.asarray(arr, float)).rolling(n).min().to_numpy()


# =============================================================================
# SECTION 2 -- STATISTICS (campaign pre-registered methods)
# =============================================================================

# ----------------------------------------------------------------------------
# MOVING-BLOCK BOOTSTRAP CI (PREREG-W / PREREG-D / PREREG-1H verdict instrument).
# CIRCULAR moving blocks (overlapping, wrap-around) so every observation has equal
# resampling weight and short series do not waste a tail. Block length is the
# autocorrelation horizon (see autocorr_block_len / drawK / fwdK per layer).
# Returns the (alpha/2, 1-alpha/2) percentile CI of the block-resampled MEAN.
# ----------------------------------------------------------------------------
def moving_block_bootstrap_ci(x, block_len, B, seed, alpha=0.05):
    """Percentile CI of the mean under a CIRCULAR moving-block bootstrap.

    x          : 1-D array of per-unit observations (e.g. 0/1 hits, or R).
    block_len  : block length L (>=1); circular blocks of this length are drawn.
    B          : number of bootstrap resamples.
    seed       : RNG seed (reproducibility -- every harness pins its own).
    alpha      : two-sided level (default 0.05 -> 95% CI).
    Returns (lo, hi). Empty x -> (nan, nan).
    """
    x = np.asarray(x, float)
    n = len(x)
    if n == 0:
        return (np.nan, np.nan)
    L = max(1, int(block_len))
    L = min(L, n)
    rng = np.random.default_rng(seed)
    n_blocks = int(np.ceil(n / L))
    # circular index template: each block is L consecutive (mod n) indices.
    offsets = np.arange(L)
    means = np.empty(B)
    for b in range(B):
        starts = rng.integers(0, n, size=n_blocks)
        idx = (starts[:, None] + offsets[None, :]).ravel() % n
        idx = idx[:n]  # trim to exactly n observations
        means[b] = x[idx].mean()
    lo = float(np.quantile(means, alpha / 2.0))
    hi = float(np.quantile(means, 1.0 - alpha / 2.0))
    return (lo, hi)


# ----------------------------------------------------------------------------
# AUTOCORRELATION BLOCK LENGTH (PREREG-W GC-1, PREREG-1H item 6).
# Smallest lag at which |autocorr(x)| < cutoff, clamped [floor, cap]. Lag 0 is
# trivially 1.0 and is skipped; we scan lag = 1, 2, ... If none drop below the
# cutoff up to `cap`, return cap. If the lag-1 autocorr is already < cutoff,
# return floor (white-noise-like -> shortest block).
# ----------------------------------------------------------------------------
def autocorr_block_len(x, cutoff=0.10, floor=1, cap=8):
    """PREREG-W GC-1 block-length rule. Returns int in [floor, cap]."""
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 2:
        return int(floor)
    xc = x - x.mean()
    denom = np.dot(xc, xc)
    if denom <= 0:
        return int(floor)        # constant series -> no autocorr -> shortest block
    max_lag = min(cap, n - 1)
    chosen = None
    for lag in range(1, max_lag + 1):
        ac = np.dot(xc[:-lag], xc[lag:]) / denom
        if abs(ac) < cutoff:
            chosen = lag
            break
    if chosen is None:
        # Only charge cap when a FULL cap-length scan genuinely stayed >= cutoff.
        # max_lag < cap means a length-truncated scan (n-1 < cap), not evidenced
        # persistence -- return the truncated max_lag (collapses to floor for tiny n).
        chosen = cap if max_lag == cap else max_lag
    return int(min(cap, max(floor, chosen)))


# ----------------------------------------------------------------------------
# MAX-STATISTIC LABEL-PERMUTATION (PREREG-W GC-3, B=10000; vote importance).
# Best-of-K importance: under the null (labels permuted), recompute each input's
# statistic, take the MAX across inputs, repeat B times. p = P(null max >=
# observed max). per_input_stat_fn(input_index, perm_rng) -> float must return a
# permuted-label statistic for one input given an RNG (so the caller controls how
# labels are shuffled per input). observed_max = max over the n_inputs of the
# real (unpermuted) statistic.
# ----------------------------------------------------------------------------
def max_stat_label_permutation(per_input_stat_fn, n_inputs, observed_max, B, seed):
    """Max-of-K label-permutation p-value (PREREG-W GC-3). Returns p in [1/(B+1), 1]."""
    rng = np.random.default_rng(seed)
    ge = 0
    for _ in range(B):
        mx = -np.inf
        for j in range(n_inputs):
            s = per_input_stat_fn(j, rng)
            if s > mx:
                mx = s
        if mx >= observed_max:
            ge += 1
    # add-one (Davison-Hinkley) so p is never exactly 0:
    return (ge + 1) / (B + 1)


# ----------------------------------------------------------------------------
# DROP-TOP-K (concentration check, PREREG-D / campaign drop-top-k discipline).
# Mean after removing the k largest values. Guards against a rate / expectancy
# carried by a handful of extreme objects.
# ----------------------------------------------------------------------------
def drop_top_k(values, k):
    """Mean of `values` after removing the k largest. Empty/over-drop -> nan."""
    v = np.asarray(values, float)
    v = v[~np.isnan(v)]
    if len(v) == 0:
        return np.nan
    k = int(max(0, k))
    if k >= len(v):
        return np.nan
    if k == 0:
        return float(v.mean())
    kept = np.sort(v)[:len(v) - k]
    return float(kept.mean())


# ----------------------------------------------------------------------------
# TWO-PROPORTION DIFFERENCE CI (PREREG-D D-4 poolRate - fvgRate; bootstrap).
# Independent-sample bootstrap of the difference in two binary rates. hit1/n1 and
# hit2/n2 are integer counts. Returns (diff, lo, hi) where diff = p1 - p2.
# ----------------------------------------------------------------------------
def two_proportion_diff_ci(hit1, n1, hit2, n2, B, seed, alpha=0.05):
    """Bootstrap CI of (p1 - p2) for two independent binary samples (PREREG-D)."""
    if n1 <= 0 or n2 <= 0:
        return (np.nan, np.nan, np.nan)
    p1 = hit1 / n1
    p2 = hit2 / n2
    diff = float(p1 - p2)
    rng = np.random.default_rng(seed)
    s1 = rng.binomial(n1, p1, size=B) / n1
    s2 = rng.binomial(n2, p2, size=B) / n2
    d = s1 - s2
    lo = float(np.quantile(d, alpha / 2.0))
    hi = float(np.quantile(d, 1.0 - alpha / 2.0))
    return (diff, lo, hi)


# ----------------------------------------------------------------------------
# RADIUS-MATCHED BASE RATE (PREREG-D D-3, MC >= 5000).
#
# Contract (frozen by PREREG-D genuine-choice #2):
#   For one side (BSL or SSL), the real objects sit at observed distances
#   `distances_real` from price at their origin bars. The null asks: "did price
#   wander K bars far enough to reach a level placed at *this distance profile*?"
#   We draw random pseudo-levels whose distances are sampled (with replacement)
#   from the SAME empirical `distances_real` distribution, then score each
#   pseudo-level over the same K-window using `price_path_fn`.
#
#   price_path_fn(distance) -> bool : returns True iff a level at signed-by-side
#     `distance` from its origin price would be "drawn to" (swept/touched) within
#     the K-window. The harness builds this closure from the reconstructed bars
#     (it owns the side sign, the origin sampling, the K scan, and the censoring),
#     so this primitive stays bar-agnostic and pre-registration-faithful.
#
#   K  : the K-window length (passed through for documentation / the harness may
#        bake it into price_path_fn; kept in the signature so the contract is
#        explicit and the MC count can be size-checked against it).
#   B  : MC draw count (PREREG-D requires >= 5000; asserted).
#   seed : RNG seed.
#
# Returns (base_rate, (lo, hi)):
#   base_rate = fraction of `B` pseudo-levels drawn to within K.
#   (lo, hi)  = bootstrap percentile CI of that fraction.
#
# Sanity (test): a pseudo-level at distance 0 is ALWAYS drawn to (price is already
# there), so an all-zero distance pool -> base_rate == 1.0.
# ----------------------------------------------------------------------------
def radius_matched_base_rate(distances_real, price_path_fn, K, B, seed, alpha=0.05):
    """Radius-matched MC base rate + bootstrap CI (PREREG-D D-3)."""
    d_real = np.asarray(distances_real, float)
    d_real = d_real[~np.isnan(d_real)]
    if len(d_real) == 0:
        return (np.nan, (np.nan, np.nan))
    if B < 5000:
        raise ValueError(f"PREREG-D D-3 requires MC >= 5000 draws; got B={B}")
    rng = np.random.default_rng(seed)
    drawn = rng.choice(d_real, size=B, replace=True)
    hits = np.fromiter((1.0 if price_path_fn(float(dist)) else 0.0 for dist in drawn),
                       dtype=float, count=B)
    base_rate = float(hits.mean())
    # bootstrap CI of the mean of the 0/1 hit vector (iid resample -- the MC draws
    # are already independent, so an iid bootstrap is the matched CI here). Reps is
    # bounded (not B) so memory stays flat regardless of how large B is; each rep
    # draws B samples one row at a time.
    reps = 2000
    boot = np.empty(reps)
    for r in range(reps):
        boot[r] = rng.choice(hits, size=B, replace=True).mean()
    lo = float(np.quantile(boot, alpha / 2.0))
    hi = float(np.quantile(boot, 1.0 - alpha / 2.0))
    return (base_rate, (lo, hi))


# ----------------------------------------------------------------------------
# ET FIELDS (UTC epoch ms -> America/New_York, DST-aware).
# TV BAR_EXPORT epoch is UTC; convert to ET for sessions / DOW (repo convention
# platform-display-tz / PREREG ET rule). Returns numpy arrays.
# ----------------------------------------------------------------------------
def et_fields(epoch_ms_utc):
    """Convert UTC epoch-ms -> (et_hour, et_min, et_dow, et_date).

    et_dow : Monday=0 .. Sunday=6 (pandas convention).
    et_date: object array of datetime.date in ET.
    Scalars are accepted (returns length-1 arrays).
    """
    arr = np.atleast_1d(np.asarray(epoch_ms_utc))
    t_utc = pd.to_datetime(arr, unit="ms", utc=True)
    t_et = t_utc.tz_convert(ET)
    return (t_et.hour.to_numpy(), t_et.minute.to_numpy(),
            t_et.dayofweek.to_numpy(), np.array(t_et.date, dtype=object))
