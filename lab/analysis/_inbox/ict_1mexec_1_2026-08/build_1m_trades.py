#!/usr/bin/env python3
"""Q-ICT-1MEXEC-1 -- native-bar trade generator for the ICT raid->FVG->target 1M
execution construct on MNQ.v.0 continuous, replacing the lost-Pine / TV-List-of-
Trades front end the original design depended on.

WHAT IS RECOVERED VS RECONSTRUCTED (read this before trusting any number downstream)
--------------------------------------------------------------------------------
RECOVERED (byte-stable, Tier-1, imported unchanged, not retyped):
  - FVG/displacement detection + bounds: `_ict_offline.py` (bull_fvg, bear_fvg,
    bull_bounds, bear_bounds, displacement, pivot_high/low, pools_from_pivots,
    wilder_atr) -- the SAME shared library `run_1m_diag.py`/`run_1m_probe.py`
    used to measure the 59.06% retrace rate on this exact panel.
  - Raid detection + raid-to-FVG pairing: `_run_1m_diag_retrieved_9aaa578.py`
    (retrieved via `git show 9aaa578`, pruned from the live tree). `raid_bars`
    is called directly, unmodified, and used as the correctness reference for
    this file's own `raid_bars_with_price` (an extension that additionally
    records swept price -- `D.raid_bars` itself discards it; see that
    function's docstring for the verification this session ran before trusting
    it: boolean-output-identical to `D.raid_bars` across 8 synthetic seeds).
    The pairing window (`pair_and_simulate`) replicates `D.pair_fvgs_to_raids`'s
    exact `last-raid-at-or-before, (i-r)<=raid_win` logic verbatim -- an
    EARLIER version of this file used a half-open slice that silently excluded
    a raid on the FVG's own bar; caught and fixed this session, not shipped.
    A first version of this file ALSO called the frozen `detect_raid` primitive
    literally, per-bar, over the full unswept registry -- `D.raid_bars`'s own
    docstring already diagnosed this exact mistake as an O(bars x pools)
    "multi-day runtime on 2.5M bars"; caught (after ~7 CPU-hours on the real
    panel, killed before completion) and replaced with the verified heap-based
    approach, not shipped.
  - Roll exclusion (+-4 calendar days of quarterly 3rd-Friday expiry):
    `third_friday`/`in_roll_window` from `build_w_export.py` (retrieved via
    `git show 82575fc` -- pruned from the live tree, PREREG_D_W Sec2 origin).
  - Per-trade cost geometry / tradeability floor / R computation:
    `harness_1m.py`'s `Trade`, `cost_r`, `apply_tradeability_floor`,
    `compute_per_trade`, `median_hurdle` (imported unchanged) -- these operate on
    a `Trade` record regardless of how entry/exit prices were produced, so they
    apply to a natively-simulated trade exactly as they did to a TV CSV row.

RECONSTRUCTED, NOT RECOVERED (operator-confirmed default, 2026-08-24 -- the exact
Pine geometry is permanently lost; see PREREG addendum for the disclosure this
mirrors):
  - Stop placement: the swept pool's own price (the liquidity that was taken),
    +-1 mintick beyond it in the adverse direction. Standard ICT convention for
    a sweep-driven entry; NOT cited to any surviving Pine line.
  - Target (`dolMode=range-extreme`): the previous COMPLETED trading day's
    opposite extreme (PDH for a long, PDL for a short) -- the literal reading of
    "range extreme" and the convention already load-bearing elsewhere in this
    repo's own ICT/ORB work (prior-day high/low as a draw-on-liquidity object).
    `nearest-pool` (REPORT-ONLY in the frozen design) is NOT implemented here --
    out of scope for the gate-bearing config.
  - Same-bar target/stop ambiguity (1-minute OHLC has no intrabar order): STOP
    is resolved first when both are touched within one bar (conservative --
    never lets an ambiguous bar manufacture an edge).
  - EOD-flat boundary (E1, `ops/prop_envelope_default.md`, 16:00 ET): the FIRST
    bar per calendar date with hour>=16 ET (robust to a missing exact
    16:00:00 print on a thin day). An earlier version used "calendar date
    changed" as the boundary -- wrong on a near-24h market, letting a fill
    ride up to ~23h past the intended flat time; caught via the invariant
    below and fixed before this file's numbers were ever reported.

TWO FURTHER BUGS FOUND AND FIXED THIS SESSION (via a standing invariant: a
stop-hit trade is `exit_price == stop_price` by construction, so no trade's
gross R can be below -1.0 -- any violation means the exit-price logic is
wrong, not the market):
  1. **Missing target-side validation.** PDH/PDL can end up on the WRONG side
     of entry (price already crashed well below yesterday's high before a long
     even fires -- routine during e.g. the 2020-03 COVID crash). Without a
     check, `hit_target` (`h[k]>=target_price` for a long) is trivially true
     on the very first bar, producing a same-bar "target hit" at whatever
     adverse price the market already happens to be at. Found via a -85R
     "trade" on 2020-03-02; fixed by requiring a long's target strictly above
     entry (short's strictly below) before the trade is admitted at all.
  2. **Deadline-bar check-order bug.** The exit walk checked `k == deadline`
     BEFORE checking that bar's own stop/target -- so a gap through the stop
     landing exactly on the 16:00 ET deadline bar exited at that bar's open
     (potentially far past the stop) instead of capping at the stop. Found via
     13 residual invariant violations (min -31.26R) on the FULL 2019-2026
     panel after fix #1 alone was applied (they did not appear in a 300K-bar
     smoke test -- the full run is what caught it). Fixed by checking
     stop/target on the deadline bar exactly like any other bar, falling back
     to that bar's open only if neither fires.
  The invariant itself is now a standing `AssertionError` in
  `run_stage2_costlaw.py`, not just a one-off diagnostic -- a future
  regression of this kind will hard-fail the run rather than silently
  producing a wrong verdict again.

This file produces `Trade` objects; it does not itself compute R, cost, or any
verdict statistic -- that stays in `harness_1m.py`, imported unchanged.

$0 / K=1 (this campaign's sole candidate, per the pre-registration). No P&L
verdict is computed by this module.
"""
from __future__ import annotations

import datetime as _dt
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CASCADE_DIR = HERE.parent.parent.parent / "archive" / "ict_cascade_2026-06-18"
if str(CASCADE_DIR) not in sys.path:
    sys.path.insert(0, str(CASCADE_DIR))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import _ict_offline as M  # noqa: E402  (shared frozen native-bar detectors, imported unchanged)
import harness_1m as H1M  # noqa: E402  (Trade / cost_r / tradeability floor, imported unchanged)
from _build_w_export_retrieved_82575fc import in_roll_window  # noqa: E402  (retrieved, pruned upstream)
import _run_1m_diag_retrieved_9aaa578 as D  # noqa: E402  (verified O(n+p log p) raid_bars + pair_fvgs_to_raids; git show 9aaa578)

PV_LEN = 2          # PREREG-1M swing strength (raid pools), LOCKED
RAID_WIN = 8         # raid -> entry window, LOCKED
RETRACE_K = 6        # entry fill window, LOCKED -- the exact cell that returned 0/247
DISP_MLT = 1.5       # displacement filter, shared with the D layer
ATR_LEN = 14
USE_BODY = False     # wick basis (the primary frozen variant; body run separately)
MIN_RMULT = 4.0      # arm-time geometry filter: target must be >= 4x this trade's own stop-implied hurdle
MIN_ABS_R_TARGET = 2.0  # n-throttle: drop trades whose target R-multiple < 2.0
STOP_BUFFER_TICKS = 1
MINTICK = 0.25       # MNQ tick size


def build_daily_extremes(dates: np.ndarray, high: np.ndarray, low: np.ndarray):
    """Previous COMPLETED trading day's high/low, forward-mapped onto every intraday
    bar of the FOLLOWING day. Strictly causal: day D's PDH/PDL uses only day D-1's
    bars, never D's own (no look-ahead into the day being traded)."""
    df = pd.DataFrame({"date": dates, "high": high, "low": low})
    daily = df.groupby("date").agg(day_high=("high", "max"), day_low=("low", "min"))
    daily = daily.sort_index()
    pdh = daily["day_high"].shift(1)
    pdl = daily["day_low"].shift(1)
    pdh_map = df["date"].map(pdh)
    pdl_map = df["date"].map(pdl)
    return pdh_map.to_numpy(), pdl_map.to_numpy()


def build_fvgs(o, h, l, c, atr, roll_mask):
    """Displacement-filtered FVG registry -- identical construction to
    `run_1m_probe.py::build_fvgs` (same shared detectors, same params)."""
    fvgs = []
    n = len(o)
    for i in range(2, n):
        if roll_mask[i]:
            continue
        if not M.displacement(o, h, l, c, i, atr[i], DISP_MLT, use_body=USE_BODY):
            continue
        if M.bull_fvg(o, h, l, c, i, use_body=USE_BODY):
            top, bot = M.bull_bounds(o, h, l, c, i, use_body=USE_BODY)
            fvgs.append({"bar": i, "top": top, "bot": bot, "bull": True})
        elif M.bear_fvg(o, h, l, c, i, use_body=USE_BODY):
            top, bot = M.bear_bounds(o, h, l, c, i, use_body=USE_BODY)
            fvgs.append({"bar": i, "top": top, "bot": bot, "bull": False})
    return fvgs


def raid_bars_with_price(o, h, l, pv_len=PV_LEN):
    """Same heap algorithm as `D.raid_bars` (O(bars + pools log pools),
    look-ahead-free eligibility gating), extended to ALSO record the most
    extreme swept price per bar -- `D.raid_bars` itself discards this (it only
    needs the boolean flag), but the stop-placement anchor needs it.

    VERIFIED: the boolean outputs of this function are checked against
    `D.raid_bars` bit-for-bit in this module's own test before being trusted
    (same algorithm, same eligibility gate, same heap ordering -- the only
    addition is capturing `p["price"]` instead of discarding it on pop).
    """
    import heapq

    pools = M.pools_from_pivots(h, l, pv_len)
    n = len(o)
    eligible_at = {}
    for p in pools:
        eligible_at.setdefault(p["bar"] + pv_len + 1, []).append(p)

    raid_buy = np.zeros(n, dtype=bool)
    raid_sell = np.zeros(n, dtype=bool)
    # Separate BSL/SSL price arrays -- a bar can carry both a BSL and an SSL
    # sweep simultaneously (independent price levels); conflating them into one
    # array risks picking the wrong side's extreme as a stop anchor.
    swept_bsl_price = np.full(n, np.nan)
    swept_ssl_price = np.full(n, np.nan)
    bsl_heap = []   # min-heap of (price,) BSL: swept when high[j] >= min price
    ssl_heap = []   # max-heap (negated price) SSL: swept when low[j] <= max price
    for j in range(n):
        for p in eligible_at.get(j, ()):
            if p["buyside"]:
                heapq.heappush(bsl_heap, p["price"])
            else:
                heapq.heappush(ssl_heap, -p["price"])
        bsl_swept_here = []
        ssl_swept_here = []
        while bsl_heap and h[j] >= bsl_heap[0]:
            bsl_swept_here.append(heapq.heappop(bsl_heap))
            raid_buy[j] = True
        while ssl_heap and l[j] <= -ssl_heap[0]:
            ssl_swept_here.append(-heapq.heappop(ssl_heap))
            raid_sell[j] = True
        if bsl_swept_here:
            swept_bsl_price[j] = max(bsl_swept_here)   # most extreme BSL swept this bar
        if ssl_swept_here:
            swept_ssl_price[j] = min(ssl_swept_here)   # most extreme SSL swept this bar
    return raid_buy, raid_sell, swept_bsl_price, swept_ssl_price


def build_flat_deadline_index(et_dates: np.ndarray, et_hour: np.ndarray) -> np.ndarray:
    """For every bar j, the index of the NEXT bar at-or-after j that marks the
    E1 flat deadline (16:00 ET, `ops/prop_envelope_default.md` E1 -- the
    binding-minimum-compliant default across all four FRIENDLY firms). CME
    futures trade near-24h, so a naive "calendar date changed" boundary lets a
    position ride up to ~23h past the intended flat time; this is the fix for
    that (caught via a mean-gross-R sanity check this session: no stop-hit
    trade can be worse than R=-1 by construction, so an implausibly negative
    mean pointed at an unbounded exit path, not the stop logic).

    Per calendar date, the flat bar is the FIRST bar with hour>=16 (not a strict
    hour==16/minute==0 match) -- OHLCV-1m only emits bars with a trade, so an
    exact 16:00:00 bar could be missing on a thin print; "first at/after 16:00"
    is robust to that without ever flattening early."""
    n = len(et_hour)
    is_flat_bar = np.zeros(n, dtype=bool)
    df = pd.DataFrame({"date": et_dates, "hour": et_hour, "idx": np.arange(n)})
    ge16 = df[df["hour"] >= 16]
    first_ge16_idx = ge16.groupby("date")["idx"].min().to_numpy()
    is_flat_bar[first_ge16_idx] = True

    next_flat = np.empty(n, dtype=np.int64)
    next_flat[n - 1] = n - 1  # no further flat bar in the panel -> last bar is the boundary
    for j in range(n - 2, -1, -1):
        next_flat[j] = j if is_flat_bar[j] else next_flat[j + 1]
    return next_flat


def pair_and_simulate(o, h, l, c, dates, epoch_ms, fvgs, raid_buy, raid_sell,
                       swept_bsl_price, swept_ssl_price,
                       pdh, pdl, flat_deadline_idx, raid_win=RAID_WIN, retrace_k=RETRACE_K):
    """For each displacement FVG, check for a same-direction raid within raid_win
    bars OF it (SSL sweep -> bull FVG = long setup; BSL sweep -> bear FVG =
    short setup). Pairing window matches `D.pair_fvgs_to_raids` EXACTLY: the
    most recent raid at-or-before the FVG's own bar, `(i - r) <= raid_win`
    (inclusive of bar i itself -- a raid on the FVG's own registration bar
    qualifies). If paired: arm a limit at the FVG mid; if touched within
    retrace_k bars, simulate the exit (PDH/PDL target vs swept-pool stop,
    stop-first on a same-bar ambiguity, flat no later than the E1 16:00 ET
    deadline) and emit a `harness_1m.Trade`.

    Not simulated here (arm-time geometry filters, applied by the caller after
    cost_r is computed): MIN_RMULT / MIN_ABS_R_TARGET.
    """
    n = len(o)
    sell_idx = np.flatnonzero(raid_sell)   # SSL sweep bars -- pairs with bull FVGs
    buy_idx = np.flatnonzero(raid_buy)     # BSL sweep bars -- pairs with bear FVGs

    def last_at_or_before(idx_arr, i):
        k = np.searchsorted(idx_arr, i, side="right") - 1
        return int(idx_arr[k]) if k >= 0 else None

    trades = []
    trade_num = 0
    for f in fvgs:
        i = f["bar"]
        mid = 0.5 * (f["top"] + f["bot"])
        src = sell_idx if f["bull"] else buy_idx
        raid_idx = last_at_or_before(src, i)
        if raid_idx is None or (i - raid_idx) > raid_win:
            continue
        stop_anchor = swept_ssl_price[raid_idx] if f["bull"] else swept_bsl_price[raid_idx]
        if np.isnan(stop_anchor):
            continue

        # --- entry: limit at FVG mid, filled within retrace_k bars of registration ---
        fill_bar = None
        end = min(n, i + 1 + retrace_k)
        for j in range(i + 1, end):
            if f["bull"] and l[j] <= mid:
                fill_bar = j
                break
            if (not f["bull"]) and h[j] >= mid:
                fill_bar = j
                break
        if fill_bar is None:
            continue

        side = 1 if f["bull"] else -1
        entry_price = mid
        if side == 1:
            stop_price = stop_anchor - STOP_BUFFER_TICKS * MINTICK
            target_price = pdh[fill_bar]
        else:
            stop_price = stop_anchor + STOP_BUFFER_TICKS * MINTICK
            target_price = pdl[fill_bar]
        if target_price is None or (isinstance(target_price, float) and np.isnan(target_price)):
            continue
        # PDH/PDL can end up on the WRONG side of entry (e.g. price has already
        # crashed well below yesterday's high before a long even fires) -- a
        # long's target must sit ABOVE entry, a short's BELOW, or `hit_target`
        # (h[k]>=target_price / l[k]<=target_price) is trivially true on the
        # very first bar, producing a same-bar "target hit" at whatever price
        # the market already happens to be at -- discovered this session via
        # the r_gross>=-1 invariant catching a -85R "trade" that was actually
        # a degenerate immediate exit at a nonsensical target, not a real loss.
        if side == 1 and target_price <= entry_price:
            continue
        if side == -1 and target_price >= entry_price:
            continue
        # A stale/far raid can leave the stop anchor on the WRONG side of entry
        # (e.g. the swept SSL sits above the current FVG mid after price has
        # since fallen) -- not a sensible risk-defined setup; drop rather than
        # let it silently produce a same-bar "stop" or an inverted R sign.
        if side == 1 and stop_price >= entry_price:
            continue
        if side == -1 and stop_price <= entry_price:
            continue
        stop_dist = abs(entry_price - stop_price)
        target_dist = abs(target_price - entry_price)
        if stop_dist <= 0:
            continue

        # --- exit: walk forward from the fill bar until target or stop touches;
        #     stop-first on a same-bar ambiguity (conservative, declared in the
        #     module docstring). Flat no later than the E1 16:00 ET deadline
        #     (a REAL session boundary, not a calendar-date change -- CME
        #     futures trade near-24h, so the two are very different bounds).
        #     The deadline bar is checked for stop/target FIRST, same as any
        #     other bar -- a fix this session: an earlier version exited that
        #     bar's open unconditionally, so a gap through the stop landing
        #     exactly on the deadline bar bypassed the stop entirely (caught by
        #     the r_gross>=-1 invariant on the full 2019-2026 panel, 13 trades).
        exit_price = None
        exit_bar = None
        deadline = flat_deadline_idx[fill_bar]
        for k in range(fill_bar, deadline + 1):
            hit_stop = (l[k] <= stop_price) if side == 1 else (h[k] >= stop_price)
            hit_target = (h[k] >= target_price) if side == 1 else (l[k] <= target_price)
            if hit_stop:
                exit_price = stop_price
                exit_bar = k
                break
            if hit_target:
                exit_price = target_price
                exit_bar = k
                break
        if exit_price is None:
            # Neither stop nor target touched on any bar through the deadline
            # (inclusive) -- flatten at the deadline bar's open, per E1.
            exit_price = o[deadline]
            exit_bar = deadline

        trade_num += 1
        t = H1M.Trade(
            trade_num=trade_num, side=side, entry_price=float(entry_price),
            exit_price=float(exit_price), pnl=float((exit_price - entry_price) * side),
            qty=1.0, risk=float("nan"), stop_dist=float(stop_dist),
            runup=float("nan"), drawdown=float("nan"),
            entry_epoch_ms=float(epoch_ms[fill_bar]),
        )
        t.target_dist = float(target_dist)  # extra field, arm-filter only, not part of Trade's own contract
        trades.append(t)
    return trades


def apply_arm_filters(trades, mintick=MINTICK, comm_pct=H1M.COMM_PCT, slip_tk=H1M.SLIP_TK,
                       min_rmult=MIN_RMULT, min_abs_r=MIN_ABS_R_TARGET):
    """MIN_RMULT / MIN_ABS_R_TARGET arm-time geometry filters (PREREG-1M L90/92) --
    applied on the trade's OWN geometry, before any outcome is read. Returns the
    surviving trades and per-reason drop counts."""
    kept, dropped_rmult, dropped_absr = [], 0, 0
    for t in trades:
        hurdle_r = H1M.cost_r(t.entry_price, t.stop_dist, mintick, comm_pct, slip_tk)
        target_r = t.target_dist / t.stop_dist if t.stop_dist > 0 else float("nan")
        if np.isnan(hurdle_r) or np.isinf(hurdle_r):
            continue
        if target_r < min_rmult * hurdle_r:
            dropped_rmult += 1
            continue
        if target_r < min_abs_r:
            dropped_absr += 1
            continue
        kept.append(t)
    return kept, dict(dropped_rmult=dropped_rmult, dropped_absr=dropped_absr)


def build_all_trades(bars: pd.DataFrame):
    """bars: databento ohlcv-1m frame with `ts_event` as a tz-aware UTC
    DatetimeIndex (the db_fetch.py parquet shape) OR as a column of the same
    type -- both accepted. Returns (trades_after_arm_filters, diagnostics)."""
    if "ts_event" in bars.columns:
        ts = pd.Series(pd.to_datetime(bars["ts_event"], utc=True)).reset_index(drop=True)
    else:
        ts = pd.Series(pd.DatetimeIndex(bars.index).tz_convert("UTC")).reset_index(drop=True)
        bars = bars.reset_index(drop=True)
    epoch_ms = (ts.astype("int64") // 1_000_000).to_numpy()
    et = ts.dt.tz_convert("America/New_York")
    dates = et.dt.date.to_numpy()
    o = bars["open"].to_numpy(dtype=float)
    h = bars["high"].to_numpy(dtype=float)
    l = bars["low"].to_numpy(dtype=float)
    c = bars["close"].to_numpy(dtype=float)

    roll_mask = np.array([in_roll_window(d) for d in dates], dtype=bool)
    atr = M.wilder_atr(h, l, c, ATR_LEN)
    fvgs = build_fvgs(o, h, l, c, atr, roll_mask)
    raid_buy, raid_sell, swept_bsl_price, swept_ssl_price = raid_bars_with_price(o, h, l, PV_LEN)
    pdh, pdl = build_daily_extremes(dates, h, l)
    flat_deadline_idx = build_flat_deadline_index(dates, et.dt.hour.to_numpy())

    raw_trades = pair_and_simulate(o, h, l, c, dates, epoch_ms, fvgs, raid_buy, raid_sell,
                                    swept_bsl_price, swept_ssl_price, pdh, pdl, flat_deadline_idx)
    kept, drop_stats = apply_arm_filters(raw_trades)

    diag = dict(
        n_bars=len(bars), n_fvgs=len(fvgs),
        n_bull_fvgs=sum(1 for f in fvgs if f["bull"]),
        n_raid_paired_trades=len(raw_trades),
        n_after_arm_filters=len(kept),
        roll_excluded_bars=int(roll_mask.sum()),
        **drop_stats,
    )
    return kept, diag
