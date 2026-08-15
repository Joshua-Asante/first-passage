"""Parent-side GENEROUS cheap falsifier — impulse→pullback→VWAP-reclaim (CON-5).

Mechanism id: impulse-pullback-vwap-reclaim. No Q-ID until CHEAP_FALSIFIER_OK.

First 30m bias (close@09:59 vs open@09:30) → after 10:00 require close on bias
side of session VWAP → tag (long low<=VWAP / short high>=VWAP) → reclaim close
back through VWAP with bias → enter next 1m open; stop at pullback extreme
(tag→reclaim); first/session; session-flat; RT 1.41.

Distinct from CON-1–4 through-break / compression, fade-to-VWAP, ORB, PDH/PDL.

Kill:
  VOID-COVERAGE if trade-session frac < 0.20
  FALSIFIED if both arms powered (n>=100) and session-block CI entirely < 0
"""
from __future__ import annotations

import datetime as _dt
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
PANEL = _HERE / "mnq_selection_ceiling_allbars_2026-08" / "_mnq_1m.parquet"

RT_PT = 1.41
N_MIN_ARM = 100
N_BOOT = 2000
BOOT_SEED = 20260811
TRADE_SESSION_FRAC_MIN = 0.20
RTH_OPEN_MIN = 9 * 60 + 30
BIAS_END_MIN = 10 * 60  # exclusive end of bias window (= 10:00)
RTH_CLOSE_MIN = 16 * 60
COST_BAR_PT = 4.0 * RT_PT
BIAS_BARS = 30

ROLL_MONTHS = (3, 6, 9, 12)
ROLL_BUFFER_DAYS = 4


def _third_friday(year: int, month: int) -> _dt.date:
    d = _dt.date(year, month, 1)
    offset = (4 - d.weekday()) % 7
    return d + _dt.timedelta(days=offset + 14)


def in_roll_window(day: _dt.date, buffer_days: int = ROLL_BUFFER_DAYS) -> bool:
    for yr in (day.year - 1, day.year, day.year + 1):
        for mo in ROLL_MONTHS:
            if abs((day - _third_friday(yr, mo)).days) <= buffer_days:
                return True
    return False


def sessionize_rth(df: pd.DataFrame) -> pd.DataFrame:
    ts = pd.to_datetime(df["ts_event"], utc=True)
    et = ts.dt.tz_convert("America/New_York")
    minute = et.dt.hour * 60 + et.dt.minute
    keep = (minute >= RTH_OPEN_MIN) & (minute < RTH_CLOSE_MIN)
    et_k = et[keep]
    return pd.DataFrame(
        {
            "ts_et": et_k.to_numpy(),
            "minute": minute[keep].to_numpy(dtype=int),
            "session": pd.DatetimeIndex(et_k).normalize().date,
            "open": df.loc[keep, "open"].to_numpy(dtype=float),
            "high": df.loc[keep, "high"].to_numpy(dtype=float),
            "low": df.loc[keep, "low"].to_numpy(dtype=float),
            "close": df.loc[keep, "close"].to_numpy(dtype=float),
            "volume": df.loc[keep, "volume"].to_numpy(dtype=float),
        }
    )


def path_pts_structural(
    entry: float,
    side: int,
    stop_level: float,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    start: int,
) -> tuple[float, str, float]:
    stop_dist = abs(entry - stop_level)
    if stop_dist <= 0:
        return float("nan"), "invalid", float("nan")
    n = len(high)
    for j in range(start, n):
        if side > 0 and low[j] <= stop_level:
            return -stop_dist, "stop", stop_dist
        if side < 0 and high[j] >= stop_level:
            return -stop_dist, "stop", stop_dist
    pts = side * (float(close[n - 1]) - entry)
    return pts, "flat", stop_dist


def session_vwap(high, low, close, volume) -> np.ndarray:
    tp = (high + low + close) / 3.0
    vol = np.maximum(volume.astype(float), 0.0)
    # Zero-volume bars contribute 0 to both sums (typical for sparse early prints).
    cum_pv = np.cumsum(tp * vol)
    cum_v = np.cumsum(vol)
    out = np.full_like(tp, np.nan, dtype=float)
    ok = cum_v > 0
    out[ok] = cum_pv[ok] / cum_v[ok]
    return out


def first_pullback_reclaim_trade(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    minute: np.ndarray,
) -> dict | None:
    """First bias-side VWAP reclaim after pullback tag → next open; pullback stop."""
    n = len(close)
    if n < BIAS_BARS + 2:
        return None
    bias_mask = (minute >= RTH_OPEN_MIN) & (minute < BIAS_END_MIN)
    if int(bias_mask.sum()) < BIAS_BARS:
        return None
    bias_idx = np.flatnonzero(bias_mask)
    open_0930 = float(open_[bias_idx[0]])
    close_0959 = float(close[bias_idx[-1]])
    if close_0959 > open_0930:
        side = +1
    elif close_0959 < open_0930:
        side = -1
    else:
        return None

    vwap = session_vwap(high, low, close, volume)
    search_start = int(bias_idx[-1]) + 1
    if search_start >= n - 1:
        return None

    cleared = False
    tagged = False
    tag_i = -1
    pull_ext = float("nan")

    for t in range(search_start, n - 1):
        vw = float(vwap[t])
        if not np.isfinite(vw):
            continue
        c = float(close[t])
        h = float(high[t])
        lo = float(low[t])

        if side > 0:
            if not cleared:
                if c > vw:
                    cleared = True
                continue
            if not tagged:
                if lo <= vw:
                    tagged = True
                    tag_i = t
                    pull_ext = lo
                    if c > vw:
                        # same-bar tag+reclaim
                        entry_i = t + 1
                        entry = float(open_[entry_i])
                        stop_level = pull_ext
                        pts, kind, stop_dist = path_pts_structural(
                            entry, side, stop_level, high, low, close, entry_i
                        )
                        if not np.isfinite(pts) or not np.isfinite(stop_dist) or stop_dist <= 0:
                            return None
                        return {
                            "side": side,
                            "pts": pts,
                            "kind": kind,
                            "R": (pts - RT_PT) / stop_dist,
                            "stop_dist": stop_dist,
                        }
                continue
            pull_ext = min(pull_ext, lo)
            if c > vw:
                entry_i = t + 1
                entry = float(open_[entry_i])
                stop_level = pull_ext
                pts, kind, stop_dist = path_pts_structural(
                    entry, side, stop_level, high, low, close, entry_i
                )
                if not np.isfinite(pts) or not np.isfinite(stop_dist) or stop_dist <= 0:
                    return None
                return {
                    "side": side,
                    "pts": pts,
                    "kind": kind,
                    "R": (pts - RT_PT) / stop_dist,
                    "stop_dist": stop_dist,
                }
        else:  # short
            if not cleared:
                if c < vw:
                    cleared = True
                continue
            if not tagged:
                if h >= vw:
                    tagged = True
                    tag_i = t
                    pull_ext = h
                    if c < vw:
                        entry_i = t + 1
                        entry = float(open_[entry_i])
                        stop_level = pull_ext
                        pts, kind, stop_dist = path_pts_structural(
                            entry, side, stop_level, high, low, close, entry_i
                        )
                        if not np.isfinite(pts) or not np.isfinite(stop_dist) or stop_dist <= 0:
                            return None
                        return {
                            "side": side,
                            "pts": pts,
                            "kind": kind,
                            "R": (pts - RT_PT) / stop_dist,
                            "stop_dist": stop_dist,
                        }
                continue
            pull_ext = max(pull_ext, h)
            if c < vw:
                entry_i = t + 1
                entry = float(open_[entry_i])
                stop_level = pull_ext
                pts, kind, stop_dist = path_pts_structural(
                    entry, side, stop_level, high, low, close, entry_i
                )
                if not np.isfinite(pts) or not np.isfinite(stop_dist) or stop_dist <= 0:
                    return None
                return {
                    "side": side,
                    "pts": pts,
                    "kind": kind,
                    "R": (pts - RT_PT) / stop_dist,
                    "stop_dist": stop_dist,
                }
    _ = tag_i  # silence unused when no fill
    return None


def session_block_ci(
    session_trade_rs: list[np.ndarray], n_boot: int = N_BOOT
) -> tuple[float, float]:
    blocks = [a for a in session_trade_rs if len(a) > 0]
    if len(blocks) < 2:
        return float("nan"), float("nan")
    rng = np.random.default_rng(BOOT_SEED)
    idx = np.arange(len(blocks))
    boots = np.empty(n_boot, dtype=float)
    for i in range(n_boot):
        pick = rng.choice(idx, size=len(blocks), replace=True)
        boots[i] = float(np.concatenate([blocks[j] for j in pick]).mean())
    return float(np.quantile(boots, 0.025)), float(np.quantile(boots, 0.975))


def main() -> int:
    t0 = time.perf_counter()
    if not PANEL.is_file():
        print(f"MISSING_PANEL {PANEL}")
        return 2
    raw = pd.read_parquet(PANEL)
    df = sessionize_rth(raw)
    sessions = sorted(df["session"].unique())
    by_sess = {s: g for s, g in df.groupby("session", sort=False)}

    long_rs: list[float] = []
    short_rs: list[float] = []
    long_blocks: list[np.ndarray] = []
    short_blocks: list[np.ndarray] = []
    gross_pts: list[float] = []
    stop_dists: list[float] = []
    n_eligible = 0
    n_trade_sessions = 0

    for s in sessions:
        if in_roll_window(s):
            continue
        grp = by_sess[s]
        if len(grp) < BIAS_BARS + 2:
            continue
        n_eligible += 1
        o = grp["open"].to_numpy(dtype=float)
        h = grp["high"].to_numpy(dtype=float)
        lo = grp["low"].to_numpy(dtype=float)
        c = grp["close"].to_numpy(dtype=float)
        v = grp["volume"].to_numpy(dtype=float)
        m = grp["minute"].to_numpy(dtype=int)
        tr = first_pullback_reclaim_trade(o, h, lo, c, v, m)
        if tr is None:
            continue
        n_trade_sessions += 1
        gross_pts.append(float(tr["pts"]))
        stop_dists.append(float(tr["stop_dist"]))
        if tr["side"] > 0:
            long_rs.append(tr["R"])
            long_blocks.append(np.asarray([tr["R"]], dtype=float))
        else:
            short_rs.append(tr["R"])
            short_blocks.append(np.asarray([tr["R"]], dtype=float))

    def arm_summary(rs: list[float], blocks: list[np.ndarray]) -> dict:
        arr = np.asarray(rs, dtype=float)
        if len(arr) == 0:
            return {
                "n": 0,
                "mean_R": float("nan"),
                "wr": float("nan"),
                "ci_lo": float("nan"),
                "ci_hi": float("nan"),
            }
        ci_lo, ci_hi = session_block_ci(blocks)
        return {
            "n": int(len(arr)),
            "mean_R": float(arr.mean()),
            "wr": float((arr > 0).mean()),
            "ci_lo": ci_lo,
            "ci_hi": ci_hi,
        }

    long = arm_summary(long_rs, long_blocks)
    short = arm_summary(short_rs, short_blocks)
    trade_frac = (n_trade_sessions / n_eligible) if n_eligible else 0.0
    mean_signed_pts = float(np.mean(gross_pts)) if gross_pts else float("nan")
    mean_stop = float(np.mean(stop_dists)) if stop_dists else float("nan")
    elapsed = time.perf_counter() - t0

    def arm_killed(a: dict) -> bool:
        return a["n"] >= N_MIN_ARM and np.isfinite(a["ci_hi"]) and a["ci_hi"] < 0.0

    killed = arm_killed(long) and arm_killed(short)
    void_cov = trade_frac < TRADE_SESSION_FRAC_MIN

    if void_cov:
        verdict = "VOID-COVERAGE"
        detail = (
            f"trade session frac {trade_frac:.3f} < floor {TRADE_SESSION_FRAC_MIN}"
        )
    elif killed:
        verdict = "FALSIFIED"
        detail = "both arms n>=100 and session-block CI entirely < 0"
    else:
        verdict = "CHEAP_FALSIFIER_OK"
        detail = (
            "coverage clears; not both-arms CI<0 under impulse-pullback-VWAP-reclaim / "
            "pullback-extreme stop / first-per-session"
        )

    out = {
        "verdict": verdict,
        "detail": detail,
        "mechanism_id": "impulse-pullback-vwap-reclaim",
        "n_eligible_sessions": n_eligible,
        "n_trade_sessions": n_trade_sessions,
        "trade_frac": trade_frac,
        "n_trades": len(gross_pts),
        "mean_signed_pts": mean_signed_pts,
        "mean_stop_dist": mean_stop,
        "gross_vs_4x_rt": (
            (mean_signed_pts / COST_BAR_PT) if np.isfinite(mean_signed_pts) else None
        ),
        "long": long,
        "short": short,
        "elapsed_s": elapsed,
        "cost_usd": 0.0,
        "panel": str(PANEL),
    }
    stamp = "2026-08-11"
    results_path = _HERE / f"_cheap_falsifier_impulse_pullback_vwap_{stamp}_RESULTS.json"
    results_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    print(f"WROTE {results_path}")
    print(f"VERDICT {verdict}")
    return 0 if verdict == "CHEAP_FALSIFIER_OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
